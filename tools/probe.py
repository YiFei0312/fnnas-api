#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对飞牛 NAS 实测接口：连接 -> 登录 -> 逐个发请求 -> 记录真实响应。

安全策略（重要）：
    默认只探测**只读**接口，规则是「最后一段以 get/list/query/check/... 开头，
    且不以 set/add/del/remove/start/stop/... 开头」，另外还有一份人工确认过的
    只读清单 EXTRA_ALLOW。写接口、删除、重启、格式化等一律不探测，
    只做静态登记。所有实测结果都会写进 data/probe_status.json，
    并可通过 --dry-run 先看探测计划。

用法：
    python tools/probe.py --dry-run                 # 只看计划，不连 NAS
    python tools/probe.py --yes                     # 实测全部只读接口
    python tools/probe.py --names file.ls,user.info # 实测指定接口
    python tools/probe.py --tier endpoint --limit 50

产出：
    captures/traffic-<时间>.jsonl   原始报文（含推送）
    data/probe_status.json          每个接口的实测结论
"""

import argparse
import asyncio
import json
import logging
import os
import re
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sdk import FnOsClient                                  # noqa: E402
from sdk.recorder import TrafficRecorder                    # noqa: E402
from sdk.safety import is_readonly, ALLOW_PREFIX, DENY_PREFIX, EXTRA_ALLOW   # noqa: E402
from sdk.utils import ws_is_open                             # noqa: E402

DEFAULT_URL = "ws://192.168.1.10:5666/websocket?type=main"
UNKNOWN_ERRNO_DEFAULT = 10000002          # 服务端对不存在的 req 返回的错误码
PARAM_ERROR_ERRNO = {8192, 100000002, 3000001}   # 参数错误
# 3000001 是 appcgi.sharesvr.* 等模块的「参数不合法」（errmsg: Invalid Params）：
# 这一族接口的参数必须包在 {"data": {...}} 里，平铺发就会拿到这个错误码。


def load_candidates(path, tiers=("endpoint",)):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    out = {}
    for name, info in data.get("reqs", {}).items():
        if info.get("tier") in tiers:
            out[name] = info
    return out


class Prober:
    def __init__(self, url, username, password, recorder, *, timeout=8.0, delay=0.15,
                 sample_limit=3000, logger=None):
        self.url = url
        self.username = username
        self.password = password
        self.recorder = recorder
        self.timeout = timeout
        self.delay = delay
        # 样例报文最大保存长度（<=0 表示不限）；完整样例才能推导出字段类型
        self.sample_limit = sample_limit
        self.logger = logger or logging.getLogger("prober")
        self.client = None
        self.unknown_errno = UNKNOWN_ERRNO_DEFAULT
        self.results = {}

    async def connect(self):
        self.client = FnOsClient(ping_interval=120, logger=self.logger,
                                 recorder=self.recorder, timeout=self.timeout)
        await asyncio.wait_for(self.client.connect(self.url), timeout=20)
        res = await asyncio.wait_for(
            self.client.login(self.username, self.password), timeout=20)
        if res.get("result") != "succ":
            raise RuntimeError(f"登录失败: {res}")
        self.logger.info(f"登录成功 uid={res.get('uid')} admin={res.get('admin')}")
        return res

    async def reconnect(self):
        try:
            if self.client:
                await self.client.close()
        except Exception:
            pass
        for attempt in range(3):
            try:
                await self.connect()
                return True
            except Exception as e:
                self.logger.warning(f"重连失败({attempt + 1}/3): {e}")
                await asyncio.sleep(2)
        return False

    async def probe_one(self, name):
        """返回一条实测记录"""
        started = time.time()
        record = {"req": name, "status": None, "errno": None, "elapsed_ms": None}
        try:
            data = await asyncio.wait_for(self.client.request(name, timeout=self.timeout),
                                          timeout=self.timeout + 2)
        except asyncio.TimeoutError:
            record["status"] = "timeout"
            record["elapsed_ms"] = round((time.time() - started) * 1000, 1)
            return record
        except Exception as e:
            record["status"] = "exception"
            record["error"] = f"{type(e).__name__}: {e}"[:300]
            record["elapsed_ms"] = round((time.time() - started) * 1000, 1)
            return record

        record["elapsed_ms"] = round((time.time() - started) * 1000, 1)
        errno = data.get("errno")
        record["errno"] = errno
        if data.get("result") == "succ":
            record["status"] = "succ"
        elif errno == self.unknown_errno:
            record["status"] = "unknown"
        elif errno in PARAM_ERROR_ERRNO:
            record["status"] = "param_error"
        elif errno is not None:
            record["status"] = "error"
        else:
            record["status"] = "succ" if "result" not in data else "other"
        # 记录响应结构，供生成文档/封装方法用
        record["resp_keys"] = sorted(k for k in data.keys()
                                     if k not in ("reqid", "result", "errno"))
        sample = json.dumps(data, ensure_ascii=False)
        limit = getattr(self, "sample_limit", 3000)
        record["sample"] = sample if limit <= 0 or len(sample) <= limit else sample[:limit] + "..."
        return record

    async def run(self, names, on_progress=None):
        # 先探一个不存在的接口，拿到「未知 req」的错误码作为分类基准
        control = await self.probe_one("__probe__.does.not.exist")
        self.unknown_errno = control.get("errno") or UNKNOWN_ERRNO_DEFAULT
        self.results["__probe__.does.not.exist"] = control
        self.logger.info(f"对照组（不存在的接口）errno={self.unknown_errno}")

        consecutive_fail = 0
        for idx, name in enumerate(names, 1):
            if not ws_is_open(self.client.websocket if self.client else None):
                self.logger.warning("连接已断开，重连中 ...")
                if not await self.reconnect():
                    self.logger.error("重连失败，停止探测")
                    break
            record = await self.probe_one(name)
            self.results[name] = record
            status = record["status"]
            if on_progress:
                on_progress(idx, len(names), name, record)
            if status in ("succ", "param_error"):
                consecutive_fail = 0
            elif status == "unknown":
                consecutive_fail = 0     # 接口不存在属于正常结论
            else:
                consecutive_fail += 1
                if consecutive_fail >= 8:
                    self.logger.error("连续 8 个异常/超时，为保护 NAS 停止探测")
                    break
            if record.get("errno") == 100000001:      # 操作太频繁
                self.logger.warning("触发限频，等待 5 秒")
                await asyncio.sleep(5)
            if self.delay:
                await asyncio.sleep(self.delay)
        return self.results


def main():
    parser = argparse.ArgumentParser(description="实测飞牛接口并录制报文（只读安全模式）")
    parser.add_argument("--url", default=os.environ.get("FNNAS_WS", DEFAULT_URL),
                        help="websocket 地址")
    parser.add_argument("--username", default=os.environ.get("fn_username", "demo-user"))
    parser.add_argument("--password", default=os.environ.get("fn_password", ""))
    parser.add_argument("--reqs", default="data/reqs.json", help="静态扫描结果")
    parser.add_argument("--tier", action="append", default=["endpoint"],
                        help="要实测的分档，默认 endpoint")
    parser.add_argument("--names", default=None, help="逗号分隔的接口名，指定后忽略 --reqs")
    parser.add_argument("--out", default="data/probe_status.json", help="实测结论输出")
    parser.add_argument("--capture-dir", default="captures", help="报文录制目录")
    parser.add_argument("--limit", type=int, default=0, help="最多探测多少个（0=全部）")
    parser.add_argument("--delay", type=float, default=0.15, help="每个请求间隔秒数")
    parser.add_argument("--timeout", type=float, default=8.0, help="单请求超时秒数")
    parser.add_argument("--sample-limit", type=int, default=3000,
                        help="样例报文最大保存字符数（<=0 不限）；文档要推导字段类型时调大")
    parser.add_argument("--include-write", action="store_true",
                        help="危险：连写接口也探测，仅在明确知道后果时使用")
    parser.add_argument("--dry-run", action="store_true", help="只打印探测计划")
    parser.add_argument("--yes", action="store_true", help="确认执行")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    logger = logging.getLogger("prober")

    if args.names:
        candidates = {n.strip(): {"tier": "manual"} for n in args.names.split(",") if n.strip()}
    else:
        candidates = load_candidates(args.reqs, tiers=tuple(args.tier))

    # 排除 util.* 之外的非接口名和登录/加密前置接口
    skip = {"user.login", "user.loginIntl", "user.logout"}
    plan, blocked = [], []
    for name in sorted(candidates):
        if name in skip:
            continue
        if is_readonly(name):
            plan.append(name)
        else:
            blocked.append(name)
    if args.include_write:
        plan += blocked
        blocked = []
    if args.limit:
        plan = plan[:args.limit]

    print(f"静态候选接口：{len(candidates)}")
    print(f"只读可探测：{len(plan)}")
    print(f"跳过（写/危险操作）：{len(blocked)}")
    if blocked:
        print("  例如：" + ", ".join(blocked[:12]) + (" ..." if len(blocked) > 12 else ""))
    print(f"预计耗时：{len(plan) * (args.delay + 0.05):.0f} 秒")
    if args.dry_run:
        print("\n[--dry-run] 实际不连接 NAS，探测清单：")
        for n in plan:
            print("   ", n)
        return 0
    if not args.yes:
        print("\n未加 --yes，仅打印计划。确认后重跑：python tools/probe.py --yes")
        return 0
    if not args.password:
        print("\n缺少密码：请设置环境变量 fn_password 或传 --password")
        return 2

    capture = os.path.join(args.capture_dir,
                           f"traffic-{time.strftime('%Y%m%d-%H%M%S')}.jsonl")
    recorder = TrafficRecorder(capture)

    prober = Prober(args.url, args.username, args.password, recorder,
                    timeout=args.timeout, delay=args.delay,
                    sample_limit=args.sample_limit, logger=logger)

    def progress(idx, total, name, record):
        logger.info(f"[{idx}/{total}] {name} -> {record['status']}"
                    + (f" (errno={record['errno']})" if record.get("errno") else ""))

    async def main_async():
        await prober.connect()
        await prober.run(plan, on_progress=progress)
        await prober.client.close()

    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        logger.warning("被中断")

    # 汇总
    by_status = {}
    for name, rec in prober.results.items():
        by_status[rec["status"]] = by_status.get(rec["status"], 0) + 1
    out = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "url": args.url,
        "username": args.username,
        "unknown_errno": prober.unknown_errno,
        "sample_limit": args.sample_limit,
        "planned": len(plan),
        "probed": len(prober.results),
        "by_status": by_status,
        "capture": capture.replace("\\", "/"),
        "results": prober.results,
    }
    d = os.path.dirname(os.path.abspath(args.out))
    if d:
        os.makedirs(d, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"\n实测 {len(prober.results)} 个接口，结果分布：{by_status}")
    print(f"结论写入 {args.out}")
    print(f"报文写入 {capture}")
    recorder.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
