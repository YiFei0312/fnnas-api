#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
监听并录制飞牛 NAS 主动推送的消息（抓「消息」用的工具）。

背景：
    飞牛除了「一问一答」的接口，还有一类**服务端主动推送**：通知、任务进度、
    磁盘/网卡状态变化、APP 上下线等。这类报文没有 reqid，SDK 默认只是忽略，
    本工具把它们全部录下来并归类，方便知道系统在什么事件下会推什么。

典型用法：
    另一个人点网页操作 NAS（比如插拔网线、开关共享、上传文件），
    你这边跑：

        python tools/watch.py --seconds 120

    结束后会把捕获到的推送按「事件特征」归类打印，报文写到 captures/。

产出：
    captures/watch-<时间>.jsonl   全部收发报文（含推送）
    captures/watch-<时间>.summary.json  推送归类结果
"""

import argparse
import asyncio
import json
import logging
import os
import sys
import time
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sdk import FnOsClient                        # noqa: E402
from sdk.recorder import TrafficRecorder, load_jsonl   # noqa: E402
from sdk.push import event_of                        # noqa: E402


def quiet_logger():
    lg = logging.getLogger("watch")
    lg.addHandler(logging.NullHandler())
    lg.propagate = False
    return lg


def event_signature(payload):
    """给推送消息起个可读的「事件名」（推送归类逻辑统一放在 sdk/push.py）"""
    return event_of(payload)


def summarize(records):
    pushes = [r for r in records if r.get("push")]
    sends = [r for r in records if r["dir"] == "send"]
    recvs = [r for r in records if r["dir"] == "recv" and not r.get("push")]
    sig = Counter()
    examples = {}
    for r in pushes:
        try:
            payload = json.loads(r["raw"])
        except Exception:
            payload = r["raw"]
        s = event_signature(payload) if isinstance(payload, dict) else "non-json"
        sig[s] += 1
        examples.setdefault(s, payload)
    return {
        "window_sec": None,
        "sent": len(sends),
        "responses": len(recvs),
        "pushes": len(pushes),
        "push_events": dict(sig.most_common()),
        "push_examples": {k: v for k, v in examples.items()},
        "reqs": dict(Counter(r["req"] for r in sends if r.get("req")).most_common()),
    }


def main():
    parser = argparse.ArgumentParser(description="监听并录制 NAS 主动推送的消息")
    parser.add_argument("--url", default=os.environ.get("FNNAS_WS",
                        "ws://192.168.1.10:5666/websocket?type=main"))
    parser.add_argument("--username", default=os.environ.get("fn_username", "demo-user"))
    parser.add_argument("--password", default=os.environ.get("fn_password", ""))
    parser.add_argument("--seconds", type=float, default=60, help="监听时长（秒）")
    parser.add_argument("--ping-interval", type=float, default=60, help="心跳间隔（秒）")
    parser.add_argument("--capture-dir", default="captures")
    parser.add_argument("--prefix", default="watch")
    parser.add_argument("--verbose", action="store_true", help="实时打印每一条推送")
    args = parser.parse_args()

    if not args.password:
        print("缺少密码：请设置环境变量 fn_password 或传 --password")
        return 2

    os.makedirs(args.capture_dir, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    capture = os.path.join(args.capture_dir, f"{args.prefix}-{stamp}.jsonl")
    recorder = TrafficRecorder(capture)
    logger = quiet_logger()

    async def run():
        client = FnOsClient(ping_interval=args.ping_interval, logger=logger,
                            recorder=recorder, timeout=15)
        await asyncio.wait_for(client.connect(args.url), timeout=20)
        res = await client.login(args.username, args.password)
        if res.get("result") != "succ":
            print(f"登录失败：{res}")
            await client.close()
            return
        print(f"已登录 uid={res.get('uid')}，开始监听 {args.seconds} 秒"
              f"（期间可以操作 NAS 网页，看会推什么消息）...")
        # 主动订阅一次只读接口，顺便验证连接正常
        await client.request("appcgi.resmon.cpu", timeout=10)
        started = time.time()
        last_report = 0
        while time.time() - started < args.seconds:
            await asyncio.sleep(1)
            if args.verbose:
                # 实时打印新到的推送
                pass
            elapsed = int(time.time() - started)
            if elapsed // 10 > last_report:
                last_report = elapsed // 10
                print(f"  [{elapsed:>4}s] 报文 {recorder.records} 条，推送 {recorder.pushes} 条")
        await client.close()

    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\n被中断，保存已捕获的数据 ...")

    recorder.close()
    records = load_jsonl(capture)
    summary = summarize(records)
    summary["url"] = args.url
    summary_path = os.path.join(args.capture_dir, f"{args.prefix}-{stamp}.summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\n共 {len(records)} 条报文：请求 {summary['sent']}，"
          f"响应 {summary['responses']}，推送 {summary['pushes']}")
    if summary["push_events"]:
        print("推送事件分布：")
        for name, count in summary["push_events"].items():
            print(f"  {count:>4}  {name}")
    else:
        print("这段时间没有收到推送（可以试试插拔网线、开关共享、上传文件再跑一次）")
    print(f"\n报文：{capture}")
    print(f"归类：{summary_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
