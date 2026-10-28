# -*- coding: utf-8 -*-
"""
**真机联调测试**（默认跳过）：把分享链接的完整生命周期用 SDK 高层方法跑一遍。

它会在 NAS 上**真的创建一条分享**，所以不会在 `unittest discover` 时自动执行，
必须显式打开：

    # Windows PowerShell
    $env:FN_LIVE_SHARE='1'
    $env:fn_username='账号'; $env:fn_password='密码'
    $env:FN_LIVE_SHARE_PATH='/vol1/1000/tmp'      # 可选，默认这个
    python -m unittest tests.test_share_live -v

安全：只操作 FN_LIVE_SHARE_PATH 里的文件；无论断言是否失败，finally 里都会删掉
自己创建的分享，并复查条数回到测试前的基线。
"""

import asyncio
import os
import sys
import time
import unittest
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

LIVE = os.environ.get("FN_LIVE_SHARE") == "1"
PATH = os.environ.get("FN_LIVE_SHARE_PATH", "/vol1/1000/tmp")
HOST = os.environ.get("FN_LIVE_HOST", "192.168.1.10")
PORT = os.environ.get("FN_LIVE_PORT", "5666")

# 整个类共用一个事件循环：client 的监听任务绑在它上面，
# 每次新建 loop 会让响应派发不到（请求永远等不到结果）。
_LOOP = None


def run(coro):
    return _LOOP.run_until_complete(coro)


@unittest.skipUnless(LIVE, "真机联调测试：设置 FN_LIVE_SHARE=1 才跑（会在 NAS 上创建并删除分享）")
class TestShareLive(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global _LOOP
        try:
            from sdk import FnOsClient
        except ImportError:                                     # pragma: no cover
            raise unittest.SkipTest("缺少 websockets / pycryptodome")
        if not os.environ.get("fn_username") or not os.environ.get("fn_password"):
            raise unittest.SkipTest("请先设置 fn_username / fn_password")

        _LOOP = asyncio.new_event_loop()
        asyncio.set_event_loop(_LOOP)
        cls.client = FnOsClient(ping_interval=None)
        cls.client.logger.setLevel(50)
        run(cls.client.connect(f"ws://{HOST}:{PORT}/websocket?type=main"))
        run(cls.client.login(os.environ["fn_username"], os.environ["fn_password"]))
        cls.created = []

    @classmethod
    def tearDownClass(cls):
        ids = [i for i in cls.created if i]
        if ids:
            try:
                run(cls.client.share_link_remove_ids(ids))
            except Exception as exc:                            # pragma: no cover
                print(f"清理分享失败，请手工删除 {ids}: {exc}")
        try:
            run(cls.client.close())
        finally:
            _LOOP.close()

    # ------------------------------------------------------------------
    def test_full_lifecycle(self):
        c = self.client
        baseline = run(c.share_link_count())
        print(f"\n基线分享条数：{baseline}")

        # 挑一个文件（挑不到就用目录本身）
        entries = (run(c.api.file.ls(path=PATH.lstrip("/"))) or {}).get("files") or []
        target = PATH if not entries else next(
            (f"{PATH.rstrip('/')}/{e['name']}" for e in entries if not e.get("dir")), PATH)
        print(f"分享对象：{target}")

        # 1) 创建：带提取码 + 1 小时有效 + 限 3 次
        name = "sdk-live-%d" % int(time.time())
        share = run(c.share_link_create(target, name=name, max_access=3,
                                       passwd="live1234", valid_to=int(time.time()) + 3600))
        share_id = share.get("id")
        self.created.append(share_id)
        print("创建响应：", share)
        self.assertTrue(share_id, "创建分享应返回 id")
        self.assertEqual(share["name"], name)
        self.assertEqual(share["maxAccess"], 3)
        self.assertEqual(share["passwd"], "live1234")
        self.assertGreater(share["validTo"], int(time.time()))
        self.assertEqual(share["status"], "valid")
        # createdTime 是毫秒级时间戳
        self.assertGreater(share["createdTime"], int(time.time() * 1000) - 60000)

        # 2) 列表里能查到
        listed = run(c.share_links(keyword=name))
        self.assertGreaterEqual(listed["total"], 1)
        self.assertIn(share_id, [x["id"] for x in listed["list"]])
        self.assertEqual(listed["list"][0]["id"], share_id)

        # 3) 详情里能看到分享的文件
        detail = run(c.share_link(share_id))
        self.assertTrue(detail["files"], "详情应包含 files")
        f0 = detail["files"][0]
        self.assertIn("path", f0)
        self.assertIn("file", f0)
        self.assertIn("isDir", f0)
        print("详情 files：", f0)

        # 4) 分享地址能打开（页面标题就是分享名）
        url = c.share_url(share_id)
        print("分享地址：", url)
        with urllib.request.urlopen(url, timeout=10) as resp:
            html = resp.read().decode("utf-8", "replace")
        self.assertEqual(resp.status, 200)
        self.assertIn(name, html)

        # 5) 修改：改名 + 永久有效 + 不限次数
        updated = run(c.share_link_update(share_id, name=name + "-edit", max_access=0, valid_to=0))
        self.assertEqual(updated["name"], name + "-edit")
        self.assertEqual(updated["validTo"], 0)
        self.assertEqual(updated["maxAccess"], 0)
        self.assertEqual(run(c.share_link(share_id))["name"], name + "-edit")

        # 6) 删除后条数回到基线
        result = run(c.share_link_remove(share_id))
        self.assertEqual(result["failedCount"], 0)
        self.created.remove(share_id)
        self.assertEqual(run(c.share_link_count()), baseline)
        with self.assertRaises(Exception):
            run(c.share_link(share_id))

    def test_flat_params_rejected(self):
        """对照组：同样参数平铺发一定被拒（证明 data 封装不是可选的美化）"""
        resp = run(self.client.call("appcgi.sharesvr.share.link.list",
                                    {"page": 1, "pageSize": 10}, nested=False))
        self.assertEqual(resp.get("errno"), 3000001)
        self.assertEqual(resp.get("errmsg"), "Invalid Params")
        # call_auto 会自动换成 data 并记住
        ok = run(self.client.call_auto("appcgi.sharesvr.share.link.list",
                                       {"page": 1, "pageSize": 10}))
        self.assertEqual(ok.get("result"), "succ")
        self.assertEqual(ok.get("data", {}).get("total"), run(self.client.share_link_count()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
