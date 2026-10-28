# -*- coding: utf-8 -*-
"""
离线测试：分享接口封装（sdk/api/curated.py 的 ShareApiMixin）与参数封装自适应。

重点验证两件实测出来的事：
    1. appcgi.sharesvr.* 的参数必须包在 data 里（平铺会 3000001 Invalid Params）
    2. id 必须是字符串

跑法：在仓库根目录 `python -m unittest discover -s tests -v`
"""

import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from sdk.api.curated import ShareApiMixin, data_of                 # noqa: E402
from sdk.exceptions import BadRequestError                          # noqa: E402


class FakeShareClient(ShareApiMixin):
    """只记录调用、按脚本返回响应的假客户端"""

    def __init__(self, *responses):
        self.script = list(responses)
        self.calls = []
        self.base_url = "http://192.168.1.10:5666"

    async def call(self, req, params=None, timeout=None, nested=False):
        self.calls.append({"req": req, "params": params, "nested": nested})
        if not self.script:
            raise AssertionError(f"没准备 {req} 的响应")
        return self.script.pop(0)

    def last(self):
        return self.calls[-1]


SUCC_LIST = {"result": "succ", "data": {"total": 1, "list": [
    {"id": "c55bd4d2b4e5404a90", "name": "apitest", "type": 1, "status": "valid",
     "accessStatus": "valid", "maxAccess": 0, "access": 0, "validTo": 0,
     "createdTime": 1792168641874, "uid": 1000, "passwd": "",
     "uploadConfig": {"path": "", "desc": "", "fileSizeLimit": 0, "fileType": ""}}]}}


class TestShareLinks(unittest.TestCase):
    def test_list_uses_nested_data_and_full_params(self):
        c = FakeShareClient(SUCC_LIST)
        data = self._run(c.share_links())
        self.assertEqual(data["total"], 1)
        call = c.last()
        self.assertEqual(call["req"], "appcgi.sharesvr.share.link.list")
        self.assertTrue(call["nested"], "sharesvr 家族必须包 data")
        self.assertEqual(call["params"], {"page": 1, "pageSize": 100, "keyword": "",
                                          "isAdmin": False, "type": 0,
                                          "sortColumn": "createdTime", "sortType": "DESC"})

    def test_list_normalizes_null_to_empty(self):
        c = FakeShareClient({"result": "succ", "data": {"total": 0, "list": None}})
        data = self._run(c.share_links())
        self.assertEqual(data, {"total": 0, "list": []})

    def test_count_uses_total(self):
        c = FakeShareClient({"result": "succ", "data": {"total": 7, "list": None}})
        self.assertEqual(self._run(c.share_link_count()), 7)

    def test_get_casts_id_to_str(self):
        c = FakeShareClient({"result": "succ", "data": {"id": "1"}})
        self._run(c.share_link(1))
        self.assertEqual(c.last()["params"], {"id": "1"})
        self.assertTrue(c.last()["nested"])

    def test_create_minimal(self):
        c = FakeShareClient({"result": "succ", "data": {"id": "abc", "name": "a.jpg"}})
        data = self._run(c.share_link_create("/vol1/1000/tmp/a.jpg"))
        self.assertEqual(data["id"], "abc")
        call = c.last()
        self.assertEqual(call["req"], "appcgi.sharesvr.share.link.create")
        self.assertEqual(call["params"]["name"], "a.jpg")
        self.assertEqual(call["params"]["files"], ["/vol1/1000/tmp/a.jpg"])
        self.assertEqual(call["params"]["maxAccess"], 0)
        self.assertNotIn("passwd", call["params"])
        self.assertNotIn("validTo", call["params"])

    def test_create_with_options(self):
        c = FakeShareClient({"result": "succ", "data": {"id": "abc"}})
        self._run(c.share_link_create(["/vol1/1000/tmp"], name="临时", max_access=3,
                                      passwd="1234", valid_to=1792172307))
        params = c.last()["params"]
        self.assertEqual(params["name"], "临时")
        self.assertEqual(params["files"], ["/vol1/1000/tmp"])
        self.assertEqual(params["maxAccess"], 3)
        self.assertEqual(params["passwd"], "1234")
        self.assertEqual(params["validTo"], 1792172307)

    def test_create_extra_upload_config(self):
        c = FakeShareClient({"result": "succ", "data": {"id": "abc"}})
        self._run(c.share_link_create("/vol1/1000/tmp/a.jpg", extra={
            "type": 4, "uploadConfig": {"desc": "收作业", "path": "/vol1/1000/tmp"}}))
        params = c.last()["params"]
        self.assertEqual(params["type"], 4)
        self.assertEqual(params["uploadConfig"]["desc"], "收作业")

    def test_update_only_sends_given_fields(self):
        c = FakeShareClient({"result": "succ", "data": {"id": "abc"}})
        self._run(c.share_link_update("abc", name="新名字", max_access=5))
        self.assertEqual(c.last()["params"], {"id": "abc", "name": "新名字", "maxAccess": 5})

    def test_update_can_make_permanent(self):
        c = FakeShareClient({"result": "succ", "data": {"id": "abc"}})
        self._run(c.share_link_update(5, valid_to=0))
        self.assertEqual(c.last()["params"], {"id": "5", "validTo": 0})

    def test_remove_multiple(self):
        c = FakeShareClient({"result": "succ", "data": {"failedCount": 0, "failedIdList": []}})
        data = self._run(c.share_link_remove("a1", "b2"))
        self.assertEqual(data["failedCount"], 0)
        self.assertEqual(c.last()["params"], {"idList": ["a1", "b2"]})
        self.assertEqual(c.last()["req"], "appcgi.sharesvr.share.link.remove")

    def test_clear(self):
        c = FakeShareClient({"result": "succ", "data": {"clear": 2}})
        self.assertEqual(self._run(c.share_link_clear())["clear"], 2)
        self.assertEqual(c.last()["params"], {"isAdmin": False})

    def test_permission_getters_and_setters(self):
        c = FakeShareClient({"result": "succ", "data": {"mode": "all"}},
                            {"result": "succ", "data": {"mode": "all"}},
                            {"result": "succ", "data": {"mode": "admin"}},
                            {"result": "succ", "data": {"mode": "admin"}})
        self.assertEqual(self._run(c.share_permission())["mode"], "all")
        self.assertIsNone(c.last()["params"])
        self._run(c.share_permission_set("all"))
        self.assertTrue(c.last()["nested"])
        self.assertEqual(c.last()["params"], {"mode": "all"})
        self.assertEqual(self._run(c.share_upload_permission())["mode"], "admin")
        self._run(c.share_upload_permission_set("admin"))
        self.assertEqual(c.last()["params"], {"mode": "admin"})

    def test_default_config(self):
        c = FakeShareClient({"result": "succ", "data": {"mode": "default", "ddns": "",
                                                        "fnDefault": "http://192.168.1.11:5666"}})
        self.assertEqual(self._run(c.share_link_default())["mode"], "default")

    def test_failure_raises(self):
        c = FakeShareClient({"result": "fail", "errno": 3000001, "errmsg": "Invalid Params"})
        with self.assertRaises(BadRequestError):
            self._run(c.share_links())

    def test_share_url(self):
        c = FakeShareClient()
        self.assertEqual(c.share_url("abc"), "http://192.168.1.10:5666/s/abc")
        self.assertEqual(c.share_url("abc", base="https://pan.example.com/"),
                         "https://pan.example.com/s/abc")
        c.base_url = None
        with self.assertRaises(BadRequestError):
            c.share_url("abc")

    @staticmethod
    def _run(coro):
        import asyncio
        return asyncio.new_event_loop().run_until_complete(coro)


class TestCallAuto(unittest.TestCase):
    """参数封装自适应：平铺失败（Invalid Params）才改成 data 重发"""

    def _stub(self, script):
        try:
            from sdk.FnOsClient import BaseClient
        except ImportError:                                   # pragma: no cover
            self.skipTest("缺少 websockets 等依赖")

        class Stub(BaseClient):
            async def _init(self):
                pass

            async def call(self_, req, params=None, timeout=None, nested=False):
                self_.seen.append((req, dict(params or {}), nested))
                return self_.script.pop(0)

        s = Stub()
        s.seen = []
        s.script = script
        return s

    def test_flat_success_no_retry(self):
        import asyncio
        s = self._stub([{"result": "succ", "files": []}])
        r = asyncio.new_event_loop().run_until_complete(
            s.call_auto("file.ls", {"path": "vol1/1000"}))
        self.assertEqual(r["result"], "succ")
        self.assertEqual(s.seen, [("file.ls", {"path": "vol1/1000"}, False)])
        self.assertEqual(s.nested_reqs, set())

    def test_invalid_params_retries_nested_and_learns(self):
        import asyncio
        loop = asyncio.new_event_loop()
        s = self._stub([{"result": "fail", "errno": 3000001, "errmsg": "Invalid Params"},
                        {"result": "succ", "data": {"total": 0, "list": None}}])
        r = loop.run_until_complete(s.call_auto("appcgi.sharesvr.share.link.list", {"page": 1}))
        self.assertEqual(r["result"], "succ")
        self.assertEqual([c[2] for c in s.seen], [False, True])
        self.assertIn("appcgi.sharesvr.share.link.list", s.nested_reqs)
        # 学到之后第二次直接走 data，不再先撞一次错
        s.script = [{"result": "succ", "data": {"total": 0, "list": None}}]
        loop.run_until_complete(s.call_auto("appcgi.sharesvr.share.link.list", {"page": 2}))
        self.assertEqual(s.seen[-1][2], True)

    def test_other_errors_not_retried(self):
        import asyncio
        s = self._stub([{"result": "fail", "errno": 8192}])
        loop = asyncio.new_event_loop()
        r = loop.run_until_complete(s.call_auto("file.share.add2", {"path": "x"}))
        self.assertEqual(r["errno"], 8192)
        self.assertEqual(len(s.seen), 1)

    def test_empty_params_never_retried(self):
        import asyncio
        s = self._stub([{"result": "fail", "errno": 3000001}])
        loop = asyncio.new_event_loop()
        loop.run_until_complete(s.call_auto("appcgi.sharesvr.share.link.list", {}))
        self.assertEqual(len(s.seen), 1)


class TestDocMetaConsistency(unittest.TestCase):
    """分享相关接口的文档元数据必须存在（避免文档漏掉新实测的接口）"""

    def test_share_reqs_have_meta(self):
        from tools.api_doc_meta import PURPOSE, FIELD_CN, PARAM_HINTS
        from sdk.api.spec import SPEC
        share_reqs = [r for r in SPEC if r.startswith("appcgi.sharesvr.share")]
        self.assertGreaterEqual(len(share_reqs), 12)
        for req in share_reqs:
            with self.subTest(req=req):
                self.assertIn(req, PURPOSE, f"{req} 缺用途说明")
        for field in ("maxAccess", "validTo", "accessStatus", "remainingAccess",
                      "failedIdList", "fnDefault", "uploadConfig"):
            with self.subTest(field=field):
                self.assertIn(field, FIELD_CN)
        self.assertIn("appcgi.sharesvr.share.link.list", PARAM_HINTS)
        self.assertIn("appcgi.sharesvr.share.link.create", PARAM_HINTS)


if __name__ == "__main__":
    unittest.main(verbosity=2)
