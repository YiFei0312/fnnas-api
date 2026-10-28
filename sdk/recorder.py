# -*- coding: utf-8 -*-
"""
WebSocket 报文录制器。

作用：把 SDK 与服务端之间**所有**收发报文按行记录成 JSONL，
      用于抓包分析、接口文档生成、离线回放。

设计原则：
    1. 不侵入业务流程，所有方法都吞掉自身异常（录制失败不能影响业务）；
    2. 默认脱敏，密码 / token / secret / 密钥等字段不会落盘；
    3. 记录足够还原协议：方向、req、reqid、耗时、逻辑参数、线上原始帧。

用法：
    from sdk import FnOsClient
    from sdk.recorder import TrafficRecorder

    recorder = TrafficRecorder('captures/traffic.jsonl')
    client = FnOsClient(recorder=recorder)
    ...
    recorder.close()          # 或 with TrafficRecorder(...) as recorder:

JSONL 每行字段：
    ts          时间戳（秒，浮点）
    dir         send / recv
    req         接口名，推送消息为 null
    reqid       请求 id
    elapsed_ms  收到响应时距发出请求的毫秒数（仅 recv 有）
    params      逻辑参数（已脱敏；登录接口会带明文参数，方便分析）
    raw         线上原始帧（已脱敏）
    push        是否是服务端主动推送（无 reqid）
"""

import json
import os
import re
import time

# 需要脱敏的字段名（小写包含匹配）
SENSITIVE_KEY_PATTERNS = (
    "password", "passwd", "secret", "token", "sign", "aes", "rsa", "iv",
    "code", "credential", "private", "machineid", "pub",
)
MASK = "***REDACTED***"


def _is_sensitive(key):
    low = str(key).lower()
    return any(p in low for p in SENSITIVE_KEY_PATTERNS)


def redact(obj, depth=0):
    """递归脱敏：命中敏感字段名则替换值，字符串里的签名前缀也会被打码"""
    if depth > 12:
        return obj
    if isinstance(obj, dict):
        return {k: (MASK if _is_sensitive(k) else redact(v, depth + 1)) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [redact(v, depth + 1) for v in obj]
    if isinstance(obj, str):
        # 签名帧形如 <base64 hmac>{json}，把签名部分打码，保留 JSON 正文
        m = re.match(r"^([A-Za-z0-9+/=]{40,})\{", obj)
        if m:
            return MASK + obj[m.end(1):]
        if len(obj) > 200000:            # 超大字段（例如 base64 图片）只留摘要
            return obj[:200] + f"...<truncated {len(obj)} chars>"
        return obj
    return obj


class TrafficRecorder:
    """把 SDK 收发报文写入 JSONL 文件"""

    def __init__(self, path=None, *, redact_sensitive=True, ensure_ascii=False,
                 record_push=True, logger=None):
        self.path = path
        self.redact_sensitive = redact_sensitive
        self.ensure_ascii = ensure_ascii
        self.record_push = record_push
        self.logger = logger

        self.records = 0
        self.sent = 0
        self.received = 0
        self.pushes = 0
        self.errors = 0
        self.reqs = {}                  # req -> 次数
        self._pending = {}              # reqid -> (req, 发出时间)
        self._fh = None
        if path:
            d = os.path.dirname(os.path.abspath(path))
            if d:
                os.makedirs(d, exist_ok=True)
            self._fh = open(path, "a", encoding="utf-8")

    # ---------- 生命周期 ----------
    def close(self):
        if self._fh:
            try:
                self._fh.close()
            finally:
                self._fh = None

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    # ---------- 记录 ----------
    def _write(self, record):
        self.records += 1
        if self._fh:
            self._fh.write(json.dumps(record, ensure_ascii=self.ensure_ascii, default=str) + "\n")
            # 立刻落盘，进程被 Ctrl+C 也能拿到数据
            self._fh.flush()

    def _clean(self, value):
        return redact(value) if self.redact_sensitive else value

    def on_send(self, req, reqid, params=None, raw=None):
        """SDK 发出请求时调用"""
        try:
            now = time.time()
            self.sent += 1
            self.reqs[req] = self.reqs.get(req, 0) + 1
            self._pending[reqid] = (req, now)
            self._write({
                "ts": round(now, 4),
                "dir": "send",
                "req": req,
                "reqid": reqid,
                "params": self._clean(params),
                "raw": self._clean(raw),
            })
        except Exception:
            self.errors += 1

    def on_recv(self, raw_message, req=None, reqid=None, payload=None):
        """SDK 收到报文时调用；reqid 为 None 表示服务端推送"""
        try:
            now = time.time()
            started = None
            if reqid:
                item = self._pending.pop(reqid, None)
                if item:
                    if req is None:
                        req = item[0]
                    started = item[1]
            if reqid is None:
                self.pushes += 1
                if not self.record_push:
                    return
            else:
                self.received += 1
            record = {
                "ts": round(now, 4),
                "dir": "recv",
                "req": req,
                "reqid": reqid,
                "raw": self._clean(raw_message),
            }
            if started is not None:
                record["elapsed_ms"] = round((now - started) * 1000, 2)
            if payload is not None and not isinstance(payload, (str, bytes)):
                record["result"] = payload.get("result")
                record["errno"] = payload.get("errno")
            if reqid is None:
                record["push"] = True
            self._write(record)
        except Exception:
            self.errors += 1

    # ---------- 统计 ----------
    def stats(self):
        return {
            "records": self.records,
            "sent": self.sent,
            "received": self.received,
            "pushes": self.pushes,
            "errors": self.errors,
            "unique_reqs": len(self.reqs),
        }

    def __repr__(self):
        return f"<TrafficRecorder path={self.path!r} {self.stats()}>"


def load_jsonl(path):
    """读取录制文件，返回记录列表"""
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out
