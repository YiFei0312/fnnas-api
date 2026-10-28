# -*- coding: utf-8 -*-
"""
分享接口实测工具：用 NAS 上的真实文件跑一遍分享链接的完整生命周期并录制报文。

为什么单独一个工具：
    `tools/probe.py` 只做「带不带参数都能判断存在性」的探测，不能去创建分享；
    而分享接口的参数必须一个个试（而且参数还得包在 data 里），需要「创建 → 查详情 →
    列表 → 修改 → 删除」这条有副作用的链路才能验证，所以单独一个可复现的工具。

安全性：
    - 默认是 dry-run，只打印计划，什么都不会做；必须显式加 --yes 才会真的创建分享。
    - 只会操作 --path 指定的路径，测完立刻删除自己创建的分享（--keep 可保留）。
    - 只会删自己创建出来的那些 id，不会碰别人已有的分享。

用法：
    # 只用 /vol1/1000/tmp 里第一个文件试跑（不创建，看看计划）
    python tools/probe_share.py

    # 真的跑一遍，并把实测结论合并进 data/probe_status.json
    python tools/probe_share.py --yes

    # 保留测试分享（调试用），只处理指定目录
    python tools/probe_share.py --yes --keep --path /vol1/1000/tmp

    # 不合并实测结论（只写自己的报告）
    python tools/probe_share.py --yes --no-merge

产物：
    data/share_probe.json    本次实测的完整调用日志（含参数与原始响应）
    captures/share-*.jsonl   报文录制（可选，--capture-dir）
    data/probe_status.json   --merge 时把 succ/error 结论并进去（供 gen_api.py 使用）
"""

import argparse
import asyncio
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sdk import FnOsClient                                            # noqa: E402
from tools.probe_common import DEFAULT_URL, Prober                    # noqa: E402
from tools.probe_common import merge_probe_status                     # noqa: E402

# 注意两个不同的前缀：分享链接是 share.link.*，权限是 share.permission.* / share.uploadpermission.*
SHARE = "appcgi.sharesvr.share.link."
SHARE_ROOT = "appcgi.sharesvr.share."
LIST_PARAMS = {"page": 1, "pageSize": 100, "keyword": "", "isAdmin": False, "type": 0,
               "sortColumn": "createdTime", "sortType": "DESC"}


class ShareProber(Prober):
    source = "tools/probe_share.py"

    @staticmethod
    def pick_target(entries, path):
        """目录里挑一个用来分享的文件（挑不到就用目录本身）"""
        for item in entries:
            if not item.get("dir"):
                return f"{path.rstrip('/')}/{item['name']}"
        return path

    async def run(self, path, keep=False):
        client = self.client
        print("--- 1) 只读接口（顺带记录实测结论）")
        await self.call(f"{SHARE}default.get", note="分享域名/限速默认值")
        await self.call(f"{SHARE_ROOT}permission.get", note="谁能创建分享")
        await self.call(f"{SHARE_ROOT}uploadpermission.get", note="谁能上传")
        await self.call("file.share.list", note="旧接口：我的分享列表")
        await self.call("file.share.listOthers", note="旧接口：别人分享给我的")

        listing = await client.api.file.ls(path=path.lstrip("/"))
        entries = listing.get("files") or []
        target = self.pick_target(entries, path if path.startswith("/") else "/" + path)
        print(f"  目录 {path} 内 {len(entries)} 项，选中分享对象：{target}")

        await self.call("file.share.info", {"path": target}, note="旧接口：按路径查分享")
        await self.call(f"{SHARE}get", {"id": "probe-not-exists"},
                        nested=True, note="不存在的 id → Not Found")

        print("--- 2) 列表（写成 data 嵌套才被接受）")
        await self.call(f"{SHARE}list", dict(LIST_PARAMS), nested=True, note="分享列表")
        self.baseline_total = await self.client.share_link_count()
        print(f"  测试前的分享条数（可能包含用户自己的分享）：{self.baseline_total}")
        print("--- 3) 平铺 vs data 嵌套对照（论证必须包 data）")
        await self.call(f"{SHARE}list", dict(LIST_PARAMS), nested=False,
                        note="平铺：Invalid Params")
        flat_status = self.calls[-1]["status"]

        print("--- 4) 创建分享（带密码 / 1 小时有效 / 限 3 次）")
        name = "probe-share-%d" % int(time.time())
        created = await self.call(f"{SHARE}create", {
            "name": name, "files": [target], "maxAccess": 3,
            "passwd": "probe1234", "validTo": int(time.time()) + 3600},
            nested=True, note="创建分享")
        share_id = (created.get("data") or {}).get("id") if isinstance(created, dict) else None
        if not share_id:
            print("!! 创建失败，后面的流程跳过（检查上面的响应）")
            return {"share_id": None, "flat_status": flat_status}

        print("--- 5) 详情 / 列表里能查到")
        await self.call(f"{SHARE}get", {"id": share_id}, nested=True, note="详情（含 files）")
        await self.call(f"{SHARE}list", dict(LIST_PARAMS), nested=True, note="列表应出现 1 条")

        print("--- 6) 修改（改名 + 永久有效 + 不限次数）")
        await self.call(f"{SHARE}update", {"id": share_id, "name": name + "-edit",
                                           "maxAccess": 0, "validTo": 0},
                        nested=True, note="修改分享")
        await self.call(f"{SHARE}get", {"id": share_id}, nested=True, note="改完复查")

        print("--- 7) 分享地址（HTTP 打开）")
        base = client.base_url or ""
        url = f"{base}/s/{share_id}" if base else None
        print(f"  分享地址：{url}")
        if url:
            print(f"  用浏览器/curl 打开 {url} 应该看到分享名称「{name}-edit」")

        if keep:
            print(f"--- 保留分享 {share_id}（--keep）：记得手工删除！")
        else:
            print("--- 8) 删除并确认列表回到 0")
            await self.call(f"{SHARE}remove", {"idList": [share_id]},
                            nested=True, note="删除分享")
            after = await self.call(f"{SHARE}list", dict(LIST_PARAMS),
                                    nested=True, note="删除后列表")
            total = ((after.get("data") or {}).get("total")
                     if isinstance(after, dict) else None)
            baseline = getattr(self, "baseline_total", 0)
            print(f"  删除后 total={total}（测试前 {baseline}）")
            if total is None or total > baseline:
                print("!! 还有残留分享，请手工检查！")
            else:
                print("  测试分享已清理干净（用户自己的分享没动）")
        return {"share_id": share_id, "target": target, "flat_status": flat_status,
                "name": name}


async def main_async(args):
    client = FnOsClient(ping_interval=None)
    client.logger.setLevel(50)
    await client.connect(args.url)
    ok = await client.login(args.username, args.password)
    if not ok:
        print("登录失败，请检查用户名/密码")
        return 1
    prober = ShareProber(client)
    result = await prober.run(args.path, keep=args.keep)
    await client.close()

    report = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "url": args.url, "username": args.username,
        "path": args.path, "share_id": result.get("share_id"),
        "kept": bool(args.keep), "flat_list_status": result.get("flat_status"),
        "calls": prober.calls,
    }
    out = os.path.join("data", "share_probe.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n完整调用日志 -> {out}（{len(prober.calls)} 次调用）")

    if args.merge:
        note = ""
        if args.keep and result.get("share_id"):
            note = (f"⚠ 本次用 --keep 保留了测试分享 {result['share_id']}"
                    f"（{result.get('name')}），请手工删除")
            print("\n" + note)
        merged, by_status = merge_probe_status(
            args.probe, prober.calls, source=ShareProber.source,
            stamp_key="share_probe_at", note_key="share_probe_note", note=note)
        print(f"实测结论合并 -> {args.probe}（写入/更新 {merged} 条，按状态 {by_status}）")
        print("下一步：python tools/gen_api.py && python tools/gen_html.py "
              "&& python tools/verify_html.py")
    return 0


def main():
    parser = argparse.ArgumentParser(description="分享接口实测（会创建并删除一条测试分享）")
    parser.add_argument("--url", default=os.environ.get("FNNAS_WS", DEFAULT_URL))
    parser.add_argument("--username", default=os.environ.get("fn_username", "demo-user"))
    parser.add_argument("--password", default=os.environ.get("fn_password", ""))
    parser.add_argument("--path", default="/vol1/1000/tmp",
                        help="拿去分享的路径（文件或目录），默认 /vol1/1000/tmp")
    parser.add_argument("--probe", default="data/probe_status.json", help="实测结论文件")
    parser.add_argument("--no-merge", dest="merge", action="store_false", default=True,
                        help="不合并进 probe_status.json")
    parser.add_argument("--keep", action="store_true", help="保留测试分享（默认测完删除）")
    parser.add_argument("--yes", action="store_true", help="确认执行（不加只打印计划）")
    args = parser.parse_args()

    print("=" * 72)
    print("分享接口实测（appcgi.sharesvr.share.link.*）")
    print(f"  NAS        : {args.url}")
    print(f"  分享对象   : {args.path}")
    print(f"  测完处理   : {'保留（--keep，需手工删除）' if args.keep else '自动删除'}")
    print(f"  合并实测   : {args.probe if args.merge else '否'}")
    print("=" * 72)
    if not args.yes:
        print("这是 dry-run：上面就是将要执行的计划。确认无误后加 --yes 真正执行。")
        print("执行时会做：只读接口探测 → 创建 1 条测试分享 → 查详情/列表 → 改名 → 删除 → 复查。")
        return 0
    print("开始执行 ...\n")
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    sys.exit(main())
