# -*- coding: utf-8 -*-
"""
`tools/probe*.py` 系列实测工具的公共部分：状态判定、调用记录、结论合并。

为什么需要它：
    `probe.py` 做「有没有这个接口」的批量探测，`probe_share.py` / `probe_file.py`
    做「有副作用的接口」的链路实测。三者的「怎么判断成功、怎么记录、怎么写回
    data/probe_status.json」是同一套逻辑，抽出来避免各写一份。
"""

import json
import time

from tools.probe import PARAM_ERROR_ERRNO

DEFAULT_URL = "ws://192.168.1.10:5666/websocket?type=main"


UNKNOWN_ERRNO = 10000002          # 服务端对不存在的 req 返回的错误码


def errno_of(resp):
    return resp.get("errno") if isinstance(resp, dict) else None


def classify(resp):
    """
    和 tools/probe.py 一致的状态判定。

    关键点：`file.*` / `stor.*` 这类**平铺外壳**的接口，成功响应里没有 `result` 字段
    （例如 `file.ls` 只回 `{"files":[...],"uver":...}`），所以「没有 errno 也没有
    result」要判成 succ，而不是 other。
    """
    if not isinstance(resp, dict):
        return "other", None
    errno = resp.get("errno")
    if resp.get("result") == "succ":
        return "succ", errno
    if errno == UNKNOWN_ERRNO:
        return "unknown", errno
    if errno in PARAM_ERROR_ERRNO:
        return "param_error", errno
    if errno is not None:
        return "error", errno
    # 没有 errno：平铺外壳（成功时无 result）算成功，显式 {"result":"fail"} 算 other
    return ("succ", None) if "result" not in resp else ("other", None)


def resumable_status(call):
    """这条调用记录能不能当作实测结论写进文档"""
    if call.get("status") not in ("succ", "error", "param_error", "other"):
        return False
    # 10000002 = 接口不存在，多半是工具把 req 名写错了，不能当成实测结论
    return call.get("errno") != UNKNOWN_ERRNO


class Prober:
    """带记录能力的调用器：每次请求都把参数、状态、原始响应存下来"""

    source = "tools/probe_common.py"

    def __init__(self, client, sample_limit=4000):
        self.client = client
        self.sample_limit = sample_limit
        self.calls = []

    async def call(self, req, params=None, nested=False, note="", retry_unknown=True,
                   allow_repeat=True):
        started = time.time()
        record = {"req": req, "params": params, "nested": bool(nested), "note": note}
        try:
            resp = await self.client.call(req, params, nested=nested)
            # 10000002 = 「接口不存在」，但服务偶尔还没就绪也会这么回，
            # 表现为同一接口有时成功有时失败 —— 隔 0.5 秒重试一次再下结论。
            if retry_unknown and errno_of(resp) == 10000002:
                import asyncio
                await asyncio.sleep(0.5)
                again = await self.client.call(req, params, nested=nested)
                if errno_of(again) != 10000002:
                    record["retried"] = True
                    resp = again
        except Exception as exc:                                   # pragma: no cover
            record.update(status="exception", error=f"{type(exc).__name__}: {exc}"[:300])
            self.calls.append(record)
            print(f"  !! {req} 异常：{type(exc).__name__}: {exc}")
            return {}
        status, errno = classify(resp)
        sample = json.dumps(resp, ensure_ascii=False)
        record.update(status=status, errno=errno,
                      elapsed_ms=round((time.time() - started) * 1000, 1),
                      resp_keys=sorted(k for k in resp if k not in ("reqid", "result", "errno")),
                      sample=sample if len(sample) <= self.sample_limit
                      else sample[:self.sample_limit] + "...")
        self.calls.append(record)
        flag = "OK " if status == "succ" else "!! "
        hint = ""
        if errno == 10000002:
            hint = "  <- 接口不存在：本工具里的 req 名写错了？"
        print(f"  {flag}{req:<44} {'data' if nested else 'flat':<5} "
              f"{json.dumps(params, ensure_ascii=False)[:56]:<56} -> {status}"
              f"{'' if errno is None else f' errno={errno}'}"
              f"{'（重试后成功）' if record.get('retried') else ''}{hint}")
        return resp


def merge_probe_status(path, calls, source, stamp_key, note_key=None, note=""):
    """把实测结论并进 data/probe_status.json 的 results（供 gen_api.py 使用）"""
    with open(path, encoding="utf-8") as f:
        probe = json.load(f)
    results = probe.setdefault("results", {})
    merged = 0
    for call in calls:
        if call.get("skip_merge"):
            print(f"  !! 跳过 {call['req']}（{call.get('skip_reason') or '结论不可靠，不写进文档'}）")
            continue
        if not resumable_status(call):
            if call.get("errno") == 10000002:
                print(f"  !! 跳过 {call['req']}（errno 10000002 = 接口不存在，请检查 req 名）")
            continue
        # 同一个接口可能测了多次（老参数失败 + 正确参数成功），以成功的那次为准
        old = results.get(call["req"])
        if old and old.get("status") == "succ" and call["status"] != "succ":
            continue
        results[call["req"]] = {
            "req": call["req"], "status": call["status"], "errno": call.get("errno"),
            "elapsed_ms": call.get("elapsed_ms"), "resp_keys": call.get("resp_keys", []),
            "sample": call.get("sample", ""), "params": call.get("params"),
            "nested": call.get("nested"), "note": call.get("note", ""),
            "source": source,
        }
        merged += 1
    # 顺带修正历史结论：errno 属于「参数错误」的，状态应该是 param_error 而不是 error
    for rec in results.values():
        if rec.get("status") == "error" and rec.get("errno") in PARAM_ERROR_ERRNO:
            rec["status"] = "param_error"
            rec["status_note"] = "参数不合法（Invalid Params），见 docs/protocol.md 的参数封装一节"
    by_status = {}
    for rec in results.values():
        by_status[rec.get("status")] = by_status.get(rec.get("status"), 0) + 1
    probe["probed"] = len(results)
    probe["by_status"] = dict(sorted(by_status.items()))
    probe[stamp_key] = time.strftime("%Y-%m-%d %H:%M:%S")
    if note and note_key:
        probe[note_key] = note
    with open(path, "w", encoding="utf-8") as f:
        json.dump(probe, f, ensure_ascii=False, indent=2)
    return merged, probe["by_status"]
