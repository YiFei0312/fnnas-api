#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
对照检查：`docs/api/interfaces.html` 里记录的接口字段，和真机**当前**返回的字段是否一致。

只调用只读接口（`sdk.safety.is_readonly` 把关），用来发现「文档过时」——比如系统升级后
某个接口多返回了字段、字段类型变了。文档里没写到的字段会报 `文档缺字段`。

用法：
    set fn_username=账号 & set fn_password=密码      # Linux/Mac: export ...
    python tools/check_doc_fields.py
    python tools/check_doc_fields.py --host 192.168.1.10 --only file.ls,stor.listDisk
"""

import argparse
import asyncio
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import gen_html as G                                                    # noqa: E402
from sdk.safety import is_readonly                                      # noqa: E402

META = {"reqid", "result", "errno", "errmsg", "req", "rev"}

# 默认抽查：覆盖平铺 / data / rsp 三种外壳，以及数组对象、嵌套对象两类字段结构
DEFAULT_CASES = [
    ("file.ls", {"path": "vol4/1000"}),
    ("file.fav.list", {}),
    ("stor.listDisk", {}),
    ("stor.calcSpace", {}),
    ("appcgi.resmon.cpu", {}),
    ("appcgi.resmon.mem", {}),
    ("appcgi.sysinfo.getHostName", {}),
    ("appcgi.network.net.list", {}),
    ("notify.unreadTotal", {}),
    ("user.info", {}),
    ("taskState.list", {}),
    # 分享（appcgi.sharesvr.*：参数要包 data）
    ("appcgi.sharesvr.share.link.default.get", {}),
    ("appcgi.sharesvr.share.permission.get", {}),
    ("appcgi.sharesvr.share.uploadpermission.get", {}),
    ("appcgi.sharesvr.share.link.list", {"page": 1, "pageSize": 100, "keyword": "",
                                         "isAdmin": False, "type": 0,
                                         "sortColumn": "createdTime", "sortType": "DESC"}),
    # link.get / create / update / remove 需要真实存在的分享，默认不查；
    # 用 tools/probe_share.py 或 --only appcgi.sharesvr.share.link.get 配合已有分享查。
]


def load_doc(path_spec, path_probe):
    with open(path_spec, encoding="utf-8") as f:
        spec = json.load(f)
    probe = None
    if os.path.exists(path_probe):
        with open(path_probe, encoding="utf-8") as f:
            probe = json.load(f)
    return {r["req"]: r for r in G.build_records(spec["spec"], probe, {}, 4000)}, spec


def unwrap(resp):
    if isinstance(resp.get("data"), dict):
        return resp["data"]
    if isinstance(resp.get("rsp"), dict):
        return resp["rsp"]
    return {k: v for k, v in resp.items() if k not in META}


async def run(args):
    from sdk import FnOsClient

    recs, spec = load_doc(args.spec, args.probe)
    cases = DEFAULT_CASES
    if args.only:
        wanted = [x.strip() for x in args.only.split(",") if x.strip()]
        cases = [(req, dict(DEFAULT_CASES).get(req, {})) for req in wanted]

    client = FnOsClient(ping_interval=None, recorder=None)
    await client.connect(f"ws://{args.host}:{args.port}/websocket?type=main")
    await client.login(os.environ["fn_username"], os.environ["fn_password"])

    ok = skipped = bad = 0
    problems = []
    try:
        for req, params in cases:
            meta = spec["spec"].get(req)
            if not meta:
                print(f"  · {req:<34} 不在封装范围，跳过")
                skipped += 1
                continue
            if not is_readonly(req):
                print(f"  · {req:<34} 是写接口，跳过（不实测写接口）")
                skipped += 1
                continue
            # 用 call_auto：平铺 / data 封装两种接口都能查（分享那一族必须包 data）
            resp = await client.call_auto(req, params)
            shape = "data" if req in client.nested_reqs else "平铺"
            if not isinstance(resp, dict) or resp.get("result") == "fail" or "errno" in resp:
                print(f"  ✗ {req:<34} 调用失败：{resp}")
                problems.append(f"{req}: 调用失败 {resp}")
                bad += 1
                continue
            body = unwrap(resp)
            keys = {k for k in body if k not in META}
            types = {f["name"]: f["type"] for f in recs[req]["fields"]}
            doc_keys = set(types) or set(recs[req]["resp_keys"])
            missing = sorted(keys - doc_keys)
            wrong = []
            for key in sorted(keys & set(types)):
                live, doc = G.jtype(body[key]), types[key]
                # 文档里可以写联合类型（如 `array<object> | null`）：命中任意一种就算对
                parts = [p.strip() for p in doc.split("|")]
                ok_type = any(p == live or (p.startswith("array") and live.startswith("array"))
                              for p in parts)
                if not ok_type:
                    wrong.append(f"{key}: 文档={doc} 实测={live}")
            if missing or wrong:
                print(f"  ✗ {req:<34} 文档缺字段={missing} 类型不符={wrong}")
                problems.append(f"{req}: 缺字段={missing} 类型不符={wrong}")
                bad += 1
            else:
                print(f"  ✓ {req:<34} [{shape}] {sorted(keys) or '（无业务字段）'}")
                ok += 1
    finally:
        await client.close()

    print(f"\n结果：一致 {ok} 个，有差异 {bad} 个，跳过 {skipped} 个")
    for p in problems:
        print("  - " + p)
    return 1 if bad else 0


def main():
    parser = argparse.ArgumentParser(description="校验文档字段与真机响应是否一致")
    parser.add_argument("--host", default="192.168.1.10")
    parser.add_argument("--port", type=int, default=5666)
    parser.add_argument("--spec", default=os.path.join(ROOT, "data", "api_spec.json"))
    parser.add_argument("--probe", default=os.path.join(ROOT, "data", "probe_status.json"))
    parser.add_argument("--only", default=None, help="只查这些接口（逗号分隔）")
    args = parser.parse_args()

    if not os.environ.get("fn_username") or not os.environ.get("fn_password"):
        print("请先设置环境变量 fn_username / fn_password")
        return 2
    return asyncio.run(run(args))


if __name__ == "__main__":
    sys.exit(main())
