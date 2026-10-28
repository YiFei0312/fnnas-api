# -*- coding: utf-8 -*-
"""
离线测试：不需要连 NAS，也不需要 websockets/pycryptodome 之外的东西。

    在仓库根目录运行：
        python -m unittest discover -s tests -v

覆盖点：
    1. reqid / 签名 / 地址推导 / 连接状态判断等协议基础
    2. 报文录制器的脱敏与统计
    3. 只读接口安全分级（防止误调用写接口）
    4. 自动生成的接口封装（spec.py）完整性与命名规范
    5. 动态命名空间 client.api 的行为
    6. 需要第三方库的部分（加密/客户端 import）自动跳过
"""

import json
import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from sdk.safety import is_readonly                                  # noqa: E402
from sdk.utils import get_reqid, http_base_from_ws, ws_is_open       # noqa: E402
from sdk.recorder import TrafficRecorder, load_jsonl, redact, MASK   # noqa: E402
from sdk.api.spec import SPEC, META, ALIASES, SAMPLE_KEYS            # noqa: E402
from sdk.api.base import ApiNamespace, build_api                     # noqa: E402
from sdk.api.curated import unwrap, check, data_of                   # noqa: E402
from sdk.push import push_matches, extract_notify, event_of, is_pong  # noqa: E402
from sdk.exceptions import BadRequestError                           # noqa: E402


# ---------------------------------------------------------------- 协议基础
class TestUtils(unittest.TestCase):
    def test_reqid_format_and_uniqueness(self):
        ids = [get_reqid() for _ in range(50)]
        self.assertEqual(len(set(ids)), 50, "reqid 必须唯一")
        for rid in ids:
            self.assertRegex(rid, r"^[0-9a-f]{8}[0-9a-f]{16}[0-9a-f]{4}$")
        self.assertEqual(len(get_reqid("6819e65000000004")), 28)
        self.assertIn("6819e65000000004", get_reqid("6819e65000000004"))

    def test_http_base_from_ws(self):
        self.assertEqual(http_base_from_ws("ws://192.168.1.4:5666/websocket?type=main"),
                         "http://192.168.1.4:5666")
        self.assertEqual(http_base_from_ws("wss://nas.example.com/websocket"),
                         "https://nas.example.com")
        self.assertEqual(http_base_from_ws("ws://host:5666/ws"), "http://host:5666")
        self.assertEqual(http_base_from_ws("ws://host:5666"), "http://host:5666")

    def test_ws_is_open(self):
        self.assertFalse(ws_is_open(None))

        class Old:            # websockets<=15 风格
            closed = False

        class New:            # websockets>=17 风格
            class state:
                name = "OPEN"

        class NewClosed:
            class state:
                name = "CLOSED"

        self.assertTrue(ws_is_open(Old()))
        self.assertTrue(ws_is_open(New()))
        self.assertFalse(ws_is_open(NewClosed()))

    def test_signature_algorithm(self):
        try:
            from sdk.encryption import get_signature, get_signature_req
        except ImportError:
            self.skipTest("缺少 pycryptodome")
        import base64
        import hashlib
        import hmac
        key = base64.b64encode(b"0123456789abcdef0123456789abcdef").decode()
        data = '{"req":"file.ls","reqid":"x"}'
        expect = base64.b64encode(
            hmac.new(base64.b64decode(key), data.encode(), hashlib.sha256).digest()).decode()
        self.assertEqual(get_signature(data, key), expect)

        # 免签接口（getRSAPub/getSI/登录加密帧）不加签名前缀
        self.assertEqual(get_signature_req({"req": "util.crypto.getRSAPub"}, key),
                         '{"req":"util.crypto.getRSAPub"}')
        self.assertEqual(get_signature_req({"req": "encrypted", "aes": "x"}, key),
                         '{"req":"encrypted","aes":"x"}')

        # 需要签名的请求 = 签名 + 原始 JSON
        body = '{"req":"file.ls"}'
        signed = get_signature_req({"req": "file.ls"}, key)
        self.assertTrue(signed.endswith(body))
        self.assertEqual(signed[:len(signed) - len(body)], get_signature(body, key))


# ---------------------------------------------------------------- 录制器
class TestRecorder(unittest.TestCase):
    def test_redact(self):
        raw = {
            "user": "admin", "password": "secret-pw", "token": "abc", "secret": "xyz",
            "nested": {"newPassword": "p", "path": "/vol1/a"},
            "list": [{"aes": "aaa"}],
        }
        out = redact(raw)
        self.assertEqual(out["user"], "admin")
        self.assertEqual(out["password"], MASK)
        self.assertEqual(out["token"], MASK)
        self.assertEqual(out["secret"], MASK)
        self.assertEqual(out["nested"]["newPassword"], MASK)
        self.assertEqual(out["nested"]["path"], "/vol1/a")
        self.assertEqual(out["list"][0]["aes"], MASK)

    def test_signed_frame_redacted(self):
        frame = "AbCdEfGhIjKlMnOpQrStUvWxYz0123456789+/==" + '{"req":"file.ls"}'
        out = redact(frame)
        self.assertTrue(out.startswith(MASK))
        self.assertIn('"req":"file.ls"', out)

    def test_jsonl_roundtrip_and_stats(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "t.jsonl")
            rec = TrafficRecorder(path)
            rec.on_send("file.ls", "req1", params={"password": "p", "path": "/a"},
                        raw='Sig=="' '{"req":"file.ls"}')
            rec.on_recv('{"result":"succ","files":[]}', reqid="req1")
            rec.on_recv('{"notify":[]}', payload={"notify": []})       # 推送
            rec.close()

            rows = load_jsonl(path)
            self.assertEqual(len(rows), 3)
            self.assertEqual(rows[0]["dir"], "send")
            self.assertEqual(rows[0]["params"]["password"], MASK)
            self.assertNotIn("p\"", json.dumps(rows, ensure_ascii=False))
            self.assertEqual(rows[1]["elapsed_ms"] >= 0, True)
            self.assertTrue(rows[2]["push"])
            stats = rec.stats()
            self.assertEqual((stats["sent"], stats["received"], stats["pushes"]), (1, 1, 1))
            self.assertEqual(stats["unique_reqs"], 1)

    def test_no_path_records_nothing_on_disk(self):
        rec = TrafficRecorder(None)
        rec.on_send("user.info", "r", params={}, raw="{}")
        rec.on_recv("{}", reqid="r")
        self.assertEqual(rec.stats()["records"], 2)      # 仍然计数，只是不落盘
        rec.close()


# ---------------------------------------------------------------- 安全分级
class TestSafety(unittest.TestCase):
    def test_readonly_true(self):
        for req in ["file.ls", "file.prop", "file.fav.list", "user.info", "user.list",
                    "stor.listDisk", "stor.calcSpace", "stor.diskSmart", "app.list",
                    "appcgi.resmon.cpu", "notify.unreadTotal", "util.crypto.getRSAPub",
                    "appcgi.share.smb.opt", "appcgi.network.gw.getting",
                    "appcgi.sysinfo.getUptime"]:
            self.assertTrue(is_readonly(req), f"{req} 应该被判为只读")

    def test_write_false(self):
        for req in ["file.rm", "file.mkdir", "file.cp", "file.mv", "file.rename",
                    "user.del", "user.add", "user.setAdmin", "user.changePassword",
                    "stor.format", "stor.stop", "stor.umount", "stor.runSmartTest",
                    "stor.zImport", "app.start", "app.stop", "app.uninstall",
                    "appcgi.network.gw.setting", "appcgi.network.ssh.set",
                    "appcgi.screen.setScreenImage", "file.trash.clear",
                    "notify.delAll", "power.poweroff", "power.reboot",
                    "appcgi.backup.storage.add", "appcgi.tfa.sendEmailCode"]:
            self.assertFalse(is_readonly(req), f"{req} 必须被判为写接口")

    def test_spec_flags_match_policy(self):
        for req, meta in SPEC.items():
            expected = "r" if is_readonly(req) else "w"
            self.assertEqual(meta[3], expected, f"{req} 的只读标记与安全策略不一致")


# ---------------------------------------------------------------- 生成的封装
class TestGeneratedSpec(unittest.TestCase):
    def test_spec_not_empty(self):
        self.assertGreater(len(SPEC), 200, "接口封装数量异常偏少")

    def test_method_names_legal(self):
        seen = {}
        for req, (group, method, status, flags, params) in SPEC.items():
            self.assertRegex(method, r"^[a-z_][a-z0-9_]*$", f"{req} 方法名不合法: {method}")
            self.assertFalse(method.startswith("_"), f"{req} 方法名不能以下划线开头")
            self.assertNotIn(method, {"call", "find", "help", "methods", "groups"},
                             f"{req} 方法名与命名空间内置方法冲突")
            self.assertIn(status, {"succ", "param_error", "error", "timeout", "other",
                                   "unverified", "unknown"})
            self.assertIn(flags, {"r", "w"})
            self.assertNotIn((group, method), seen,
                             f"{req} 与 {seen.get((group, method))} 方法名重复")
            seen[(group, method)] = req

    def test_unknown_reqs_excluded(self):
        for req in META["unknown_reqs"]:
            self.assertNotIn(req, SPEC, f"实测不存在的 {req} 不应被封装")

    def test_all_spec_reqs_exist_in_scan(self):
        path = os.path.join(ROOT, "data", "reqs.json")
        if not os.path.exists(path):
            self.skipTest("没有 data/reqs.json")
        with open(path, encoding="utf-8") as f:
            scan = json.load(f)["reqs"]
        for req in SPEC:
            self.assertIn(req, scan, f"{req} 不在静态扫描结果里")

    def test_verified_endpoints_have_status(self):
        # 实测通过的接口必须真的被探过
        self.assertGreater(sum(1 for m in SPEC.values() if m[2] == "succ"), 50)


# ---------------------------------------------------------------- 命名空间
class FakeClient:
    """假装是 FnOsClient，用来离线验证命名空间转发是否正确"""

    def __init__(self):
        self.calls = []

    async def call(self, req, params=None, timeout=None):
        self.calls.append((req, params, timeout))
        return {"result": "succ", "req": req, "data": {"echo": params}}


class TestNamespace(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.client = FakeClient()
        self.api = build_api(self.client)

    async def test_namespace_call(self):
        res = await self.api.file.ls(path="vol1/1000")
        self.assertEqual(self.client.calls[-1][0], "file.ls")
        self.assertEqual(self.client.calls[-1][1], {"path": "vol1/1000"})
        self.assertEqual(res["result"], "succ")

    async def test_nested_namespace(self):
        await self.api.appcgi.network.net_list()
        self.assertEqual(self.client.calls[-1][0], "appcgi.network.net.list")

    async def test_params_dict_and_timeout(self):
        await self.api.file.ls({"path": "x"}, timeout=3)
        self.assertEqual(self.client.calls[-1], ("file.ls", {"path": "x"}, 3))

    async def test_generic_call(self):
        await self.api.call("file.prop", {"path": "a"}, timeout=1)
        self.assertEqual(self.client.calls[-1], ("file.prop", {"path": "a"}, 1))

    async def test_unknown_attribute_raises(self):
        with self.assertRaises(AttributeError) as ctx:
            self.api.file.not_a_real_method
        self.assertIn("没有", str(ctx.exception))

    async def test_dir_and_search(self):
        names = dir(self.api.file)
        self.assertIn("ls", names)
        self.assertIn("rm", names)
        found = self.api.find("listDisk")
        self.assertIn("stor.listDisk", found)
        self.assertIn("stor", self.api.groups())
        self.assertIsInstance(self.api.help("file.ls"), str)
        self.assertIn("file.ls", self.api.help("file.ls"))

    async def test_method_metadata(self):
        m = self.api.file.ls
        self.assertEqual(m.req, "file.ls")
        self.assertTrue(m.readonly)
        self.assertIn("file.ls", m.__doc__)
        self.assertFalse(self.api.file.rm.readonly)

    async def test_caching_identity(self):
        self.assertIs(self.api.file, self.api.file)
        self.assertIs(self.api.file.ls, self.api.file.ls)


# ---------------------------------------------------------------- 手写封装
class TestCuratedHelpers(unittest.TestCase):
    def test_unwrap(self):
        self.assertEqual(unwrap({"data": {"a": 1}, "result": "succ"}), {"a": 1})
        self.assertEqual(unwrap({"rsp": {"b": 2}}), {"b": 2})
        self.assertEqual(unwrap({"files": []}), {"files": []})

    def test_check_raises_on_fail(self):
        with self.assertRaises(BadRequestError) as ctx:
            check({"result": "fail", "errno": 8192})
        self.assertEqual(ctx.exception.error_code, 8192)
        self.assertEqual(check({"result": "succ"})["result"], "succ")

    def test_data_of(self):
        self.assertEqual(data_of({"result": "succ", "data": {"x": 1}}), {"x": 1})
        with self.assertRaises(BadRequestError):
            data_of({"result": "fail", "errno": 100000002})


class TestMixinPresence(unittest.TestCase):
    def test_client_has_curated_methods(self):
        try:
            from sdk import FnOsClient
        except ImportError:
            self.skipTest("缺少 websockets 等依赖")
        for name in ["sysinfo_version", "sysinfo_uptime", "resmon_cpu", "network_interfaces",
                     "storage_disks", "storage_calc_space", "file_prop", "file_favorites",
                     "notify_unread_total", "share_options", "api"]:
            self.assertTrue(hasattr(FnOsClient, name) or name == "api", f"缺少 {name}")


# ---------------------------------------------------------------- 推送消息
class TestPush(unittest.TestCase):
    PONG = {"res": "pong"}
    NOTIFY = {"notify": [{"from": "trim", "title": "磁盘警告", "level": 2,
                          "content": '{"eventId":"diskDegraded","title":"磁盘降级"}'}]}

    def test_is_pong(self):
        self.assertTrue(is_pong(self.PONG))
        self.assertFalse(is_pong(self.NOTIFY))

    def test_matcher(self):
        self.assertTrue(push_matches(None, self.PONG))
        self.assertTrue(push_matches("*", self.NOTIFY))
        self.assertTrue(push_matches("notify", self.NOTIFY))
        self.assertFalse(push_matches("notify", self.PONG))
        self.assertTrue(push_matches("res", self.PONG))                 # 顶层键
        self.assertTrue(push_matches(lambda p: "notify" in p, self.NOTIFY))
        self.assertFalse(push_matches(lambda p: "nope" in p, self.NOTIFY))
        self.assertTrue(push_matches("eventId", {"data": {"eventId": "x"}}))

    def test_extract_notify(self):
        items = extract_notify(self.NOTIFY)
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["title"], "磁盘警告")
        self.assertEqual(items[0]["data"]["eventId"], "diskDegraded")
        self.assertEqual(items[0]["event"], "diskDegraded")
        self.assertEqual(extract_notify(self.PONG), [])
        self.assertEqual(extract_notify("not-a-dict"), [])

    def test_event_of(self):
        self.assertEqual(event_of(self.PONG), "pong")
        self.assertTrue(event_of(self.NOTIFY).startswith("notify:trim:"))
        self.assertEqual(event_of({"event": "entryChange"}), "event=entryChange")
        self.assertEqual(event_of("x"), "non-json")

    def test_handler_registration(self):
        try:
            from sdk import FnOsClient
        except ImportError:
            self.skipTest("缺少 websockets 等依赖")
        client = FnOsClient()
        got = []

        @client.add_push_handler("notify")
        def on_notify(c, payload):
            got.append((c, payload))

        # SDK 自带一个内部嗅探器（等异步文件任务结果用），所以这里会多一个
        self.assertEqual(len(client.push_handlers), 2)
        import asyncio
        asyncio.run(client._dispatch_push(self.NOTIFY))
        asyncio.run(client._dispatch_push(self.PONG))          # 不该命中
        self.assertEqual(len(got), 1)
        self.assertIs(got[0][0], client)

        client.remove_push_handler(on_notify)
        # 只留下 SDK 内部的处理函数
        self.assertEqual(len(client.push_handlers), 1)
        self.assertTrue(getattr(client.push_handlers[0][1], "_internal", False))
        client.remove_push_handler()                            # 清空全部也不该动内部那个
        self.assertEqual(len(client.push_handlers), 1)

    def test_async_handler(self):
        try:
            from sdk import FnOsClient
        except ImportError:
            self.skipTest("缺少 websockets 等依赖")
        import asyncio
        client = FnOsClient()
        got = []

        async def on_all(c, payload):
            got.append(payload)

        client.add_push_handler(None, on_all)
        asyncio.run(client._dispatch_push(self.PONG))
        self.assertEqual(got, [self.PONG])

    def test_handler_exception_isolated(self):
        try:
            from sdk import FnOsClient
        except ImportError:
            self.skipTest("缺少 websockets 等依赖")
        import asyncio
        import logging
        logger = logging.getLogger("null")
        logger.addHandler(logging.NullHandler())
        logger.propagate = False
        client = FnOsClient(logger=logger)
        got = []

        def boom(c, payload):
            raise RuntimeError("boom")

        client.add_push_handler(None, boom)
        client.add_push_handler(None, lambda c, p: got.append(p))
        asyncio.run(client._dispatch_push(self.PONG))
        self.assertEqual(got, [self.PONG], "一个回调炸了不该影响其它回调")


if __name__ == "__main__":
    unittest.main(verbosity=2)
