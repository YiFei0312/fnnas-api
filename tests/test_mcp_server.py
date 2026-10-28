# -*- coding: utf-8 -*-
"""
离线用例：MCP Server（`mcp/`）——配置、协议层、工具注册、HTTP 状态。

不连 NAS、不联网：桥接层用假对象替身。
"""

import json
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from mcp import tools as tools_mod                                    # noqa: E402
from mcp.config import Config                                         # noqa: E402
from mcp.protocol import McpServer                                    # noqa: E402


class FakeBridge:
    """假的飞牛桥：记录调用、按需返回数据"""

    def __init__(self, data=None, error=None):
        self.calls = []
        self.data = data if data is not None else {"ok": True}
        self.error = error
        self.config = Config({})
        self._status = {"connected": True, "host": "fake", "port": 5666,
                        "username": "tester", "ws_url": "ws://fake:5666/websocket?type=main",
                        "http_base": "http://fake:5666", "connected_at": 1.0,
                        "calls": 0, "calls_failed": 0, "last_error": None}

    def call(self, req, params=None, nested=False, timeout=60, retry=True):
        self.calls.append(("call", req, params, nested))
        if self.error:
            raise self.error
        return {"result": "succ", "data": self.data}

    def call_data(self, req, params=None, nested=False, timeout=60, key=None, retry=True):
        self.calls.append(("call_data", req, params, nested))
        if self.error:
            raise self.error
        return self.data

    def task_call(self, req, params, timeout=180):
        self.calls.append(("task_call", req, params, None))
        return {"result": "succ"}

    def http_call(self, method, path, params=None, body=None, timeout=30):
        self.calls.append(("http", method, path, params or body))
        if self.error:
            raise self.error
        return {"code": 0, "msg": "", "data": self.data}

    def status(self):
        return dict(self._status)


def make_server(include_unverified=False, bridge=None):
    config = Config({})
    config.data["server"]["tools"]["include_unverified"] = include_unverified
    data_dir = os.path.join(ROOT, "data")
    tools_mod.set_data_dir(data_dir)
    return McpServer(bridge or FakeBridge(), config, data_dir=data_dir, version="test"), \
        (bridge or FakeBridge())


class TestConfig(unittest.TestCase):
    def test_defaults(self):
        cfg = Config({})
        self.assertEqual(cfg.nas["host"], "127.0.0.1")
        self.assertEqual(cfg.nas["port"], 5666)
        self.assertTrue(cfg.mcp_enabled())
        self.assertTrue(cfg.sse_enabled())
        self.assertEqual(cfg.ws_url, "ws://127.0.0.1:5666/websocket?type=main")
        self.assertEqual(cfg.http_base, "http://127.0.0.1:5666")

    def test_http_base_override(self):
        cfg = Config({"nas": {"base_url": "http://192.168.1.9:5666/"}})
        self.assertEqual(cfg.http_base, "http://192.168.1.9:5666")

    def test_update_toggles(self):
        cfg = Config({})
        cfg.update({"server": {"mcp": {"enabled": False}, "sse": {"enabled": False}}})
        self.assertFalse(cfg.mcp_enabled())
        self.assertFalse(cfg.sse_enabled())
        cfg.update({"server": {"mcp": {"enabled": True}}})
        self.assertTrue(cfg.mcp_enabled())

    def test_update_password_keeps_when_empty(self):
        cfg = Config({})
        cfg.update({"nas": {"password": "新密码"}})
        self.assertEqual(cfg.nas["password"], "新密码")
        cfg.update({"nas": {"password": ""}})          # 空字符串 = 不改
        self.assertEqual(cfg.nas["password"], "新密码")
        cfg.update({"nas": {"password": "••••••••"}})  # UI 里的遮罩占位也不该覆盖
        self.assertEqual(cfg.nas["password"], "新密码")

    def test_public_view_masks_password(self):
        cfg = Config({"nas": {"password": "secret"}})
        view = cfg.public_view()
        self.assertNotIn("secret", json.dumps(view))
        self.assertTrue(view["nas"]["password_set"])

    def test_save_and_reload(self, tmpdir=None):
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "config.json")
            cfg = Config({"nas": {"username": "abc"}}, path=path)
            cfg.save()
            self.assertTrue(os.path.exists(path))
            again = Config.load(path)
            self.assertEqual(again.nas["username"], "abc")


class TestProtocol(unittest.TestCase):
    def test_initialize(self):
        server, _ = make_server()
        resp = server.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                              "params": {"protocolVersion": "2025-06-18"}})
        result = resp["result"]
        self.assertEqual(result["protocolVersion"], "2025-06-18")
        self.assertEqual(result["serverInfo"]["name"], "fnnas-mcp")
        self.assertIn("tools", result["capabilities"])
        self.assertTrue(result["instructions"])

    def test_initialize_negotiates_unknown_version(self):
        server, _ = make_server()
        resp = server.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                              "params": {"protocolVersion": "1999-01-01"}})
        self.assertEqual(resp["result"]["protocolVersion"], "2025-06-18")

    def test_notification_returns_none(self):
        server, _ = make_server()
        self.assertIsNone(server.handle({"jsonrpc": "2.0",
                                         "method": "notifications/initialized"}))

    def test_ping(self):
        server, _ = make_server()
        resp = server.handle({"jsonrpc": "2.0", "id": 2, "method": "ping"})
        self.assertEqual(resp["result"], {})

    def test_unknown_method(self):
        server, _ = make_server()
        resp = server.handle({"jsonrpc": "2.0", "id": 3, "method": "nope/nope"})
        self.assertEqual(resp["error"]["code"], -32601)

    def test_tools_list(self):
        server, _ = make_server()
        resp = server.handle({"jsonrpc": "2.0", "id": 4, "method": "tools/list"})
        tools = resp["result"]["tools"]
        self.assertGreaterEqual(len(tools), 30)
        names = {t["name"] for t in tools}
        for expected in ("fnnas_system_uptime", "fnnas_file_ls",
                         "fnnas_interfaces_search", "fnnas_interface_call",
                         "fnnas_http_api_call", "fnnas_share_link_create",
                         "fnnas_photo_albums"):
            self.assertIn(expected, names)
        for tool in tools:
            self.assertEqual(tool["inputSchema"]["type"], "object")
            self.assertIsInstance(tool["description"], str)
            self.assertTrue(tool["description"])

    def test_tool_required_params_declared(self):
        server, _ = make_server()
        resp = server.handle({"jsonrpc": "2.0", "id": 5, "method": "tools/list"})
        by_name = {t["name"]: t for t in resp["result"]["tools"]}
        self.assertEqual(by_name["fnnas_file_ls"]["inputSchema"]["required"], ["path"])
        self.assertEqual(by_name["fnnas_system_uptime"]["inputSchema"]["required"], [])
        self.assertEqual(sorted(by_name["fnnas_file_copy"]["inputSchema"]["required"]),
                         ["dest_dir", "files"])

    def test_unknown_tool(self):
        server, _ = make_server()
        resp = server.handle({"jsonrpc": "2.0", "id": 6, "method": "tools/call",
                              "params": {"name": "nope", "arguments": {}}})
        self.assertEqual(resp["error"]["code"], -32602)

    def test_missing_required_argument(self):
        server, _ = make_server()
        resp = server.handle({"jsonrpc": "2.0", "id": 7, "method": "tools/call",
                              "params": {"name": "fnnas_file_ls", "arguments": {}}})
        self.assertEqual(resp["error"]["code"], -32602)
        self.assertIn("path", resp["error"]["message"])

    def test_tool_calls_bridge(self):
        bridge = FakeBridge(data={"uptime": 123})
        server, _ = make_server(bridge=bridge)
        resp = server.handle({"jsonrpc": "2.0", "id": 8, "method": "tools/call",
                              "params": {"name": "fnnas_system_uptime",
                                         "arguments": {}}})
        result = resp["result"]
        self.assertFalse(result["isError"])
        self.assertIn("123", result["content"][0]["text"])
        self.assertEqual(bridge.calls[0][1], "appcgi.sysinfo.getUptime")

    def test_tool_error_becomes_iserror(self):
        bridge = FakeBridge(error=RuntimeError("NAS 断线"))
        server, _ = make_server(bridge=bridge)
        resp = server.handle({"jsonrpc": "2.0", "id": 9, "method": "tools/call",
                              "params": {"name": "fnnas_system_uptime",
                                         "arguments": {}}})
        self.assertTrue(resp["result"]["isError"])
        self.assertIn("NAS 断线", resp["result"]["content"][0]["text"])

    def test_share_link_tool_nests_data(self):
        bridge = FakeBridge(data={"id": "abc123"})
        server, _ = make_server(bridge=bridge)
        resp = server.handle({"jsonrpc": "2.0", "id": 10, "method": "tools/call",
                              "params": {"name": "fnnas_share_link_create",
                                         "arguments": {"path": "/vol1/1000/tmp/a.jpg"}}})
        self.assertFalse(resp["result"]["isError"])
        kind, req, params, nested = bridge.calls[0]
        self.assertEqual(req, "appcgi.sharesvr.share.link.create")
        self.assertIn("data", params)
        self.assertEqual(params["data"]["filePath"], "/vol1/1000/tmp/a.jpg")
        self.assertIn("/s/abc123", json.loads(resp["result"]["content"][0]["text"])["url"])

    def test_http_tool_uses_http_call(self):
        bridge = FakeBridge(data={"list": []})
        server, _ = make_server(bridge=bridge)
        resp = server.handle({"jsonrpc": "2.0", "id": 11, "method": "tools/call",
                              "params": {"name": "fnnas_photo_albums", "arguments": {}}})
        self.assertFalse(resp["result"]["isError"])
        self.assertEqual(bridge.calls[0][0], "http")
        self.assertEqual(bridge.calls[0][2], "/api/v1/album/list")

    def test_resources(self):
        server, _ = make_server()
        listed = server.handle({"jsonrpc": "2.0", "id": 12, "method": "resources/list"})
        uris = [r["uri"] for r in listed["result"]["resources"]]
        self.assertIn("fnnas://status", uris)
        read = server.handle({"jsonrpc": "2.0", "id": 13, "method": "resources/read",
                              "params": {"uri": "fnnas://status"}})
        payload = json.loads(read["result"]["contents"][0]["text"])
        self.assertTrue(payload["ok"])
        self.assertIn("stats", payload)

    def test_batch_request(self):
        server, _ = make_server()
        resp = server.handle([
            {"jsonrpc": "2.0", "id": 1, "method": "ping"},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        ])
        self.assertEqual(len(resp), 2)


class TestToolsData(unittest.TestCase):
    def setUp(self):
        tools_mod.set_data_dir(os.path.join(ROOT, "data"))

    def test_stats(self):
        stats = tools_mod.stats()
        self.assertEqual(stats["ws_total"], 476)
        self.assertEqual(stats["http_total"], 151)
        self.assertGreater(stats["ws_available"], 100)
        self.assertGreater(stats["http_available"], 30)
        self.assertGreaterEqual(stats["tools"], 30)

    def test_interfaces_have_status_and_purpose(self):
        items = tools_mod.load_interfaces()
        self.assertTrue(any(i["purpose"] for i in items))
        self.assertTrue(all("available" in i for i in items))
        verified = [i for i in items if i["verified"]]
        self.assertTrue(verified)

    def test_menu_entries_merge_both_protocols(self):
        entries = tools_mod.menu_entries()
        protocols = {e["protocol"] for e in entries}
        self.assertEqual(protocols, {"ws", "http"})
        self.assertTrue(any(e["available"] and e["protocol"] == "http" for e in entries))

    def test_search_tool_only_returns_available(self):
        server, _ = make_server()
        resp = server.handle({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                              "params": {"name": "fnnas_interfaces_search",
                                         "arguments": {"keyword": "file.ls", "limit": 5}}})
        payload = json.loads(resp["result"]["content"][0]["text"])
        self.assertGreaterEqual(payload["total"], 1)
        self.assertTrue(all(i["available"] for i in payload["interfaces"]))


class TestWebUi(unittest.TestCase):
    """界面里必须有「配置 NAS IP / 账号 / 密码」的地方，而且要在首页显眼位置"""

    @classmethod
    def setUpClass(cls):
        root = os.path.join(ROOT, "mcp", "webui")
        cls.html = open(os.path.join(root, "index.html"), encoding="utf-8").read()
        cls.js = open(os.path.join(root, "app.js"), encoding="utf-8").read()
        cls.css = open(os.path.join(root, "style.css"), encoding="utf-8").read()

    def test_connection_card_on_main_page(self):
        self.assertIn("飞牛连接配置", self.html)
        card_pos = self.html.index("飞牛连接配置")
        tabs_pos = self.html.index('class="tabs"')
        self.assertLess(card_pos, tabs_pos, "连接配置应该放在首页（标签页之前）")

    def test_has_ip_account_password_fields(self):
        for field_id in ("fHost", "fPort", "fUser", "fPass", "fBase",
                         "saveCfg", "testConn", "connTarget"):
            self.assertIn('id="%s"' % field_id, self.html, "缺少输入项 %s" % field_id)
        # 不能有重复的 id（之前设置页里那份已经挪到首页）
        self.assertEqual(self.html.count('id="fHost"'), 1)
        self.assertEqual(self.html.count('id="fPass"'), 1)
        self.assertIn('type="password"', self.html)

    def test_password_is_write_only(self):
        """密码框不应把真实密码回填到页面上"""
        self.assertIn("不修改请留空", self.html)
        self.assertIn("passHint", self.html)

    def test_js_wires_config_and_reconnect(self):
        self.assertIn("useLocal", self.js)              # 「本机」快捷按钮
        self.assertIn("connTarget", self.js)            # 首页连接目标显示
        self.assertIn("/api/config", self.js)
        self.assertIn("/api/test", self.js)
        self.assertIn("保存并重连", self.html)

    def test_css_has_grid(self):
        self.assertIn(".conn-grid", self.css)
        self.assertIn(".conn-card", self.css)



class TestNoBakedCredentials(unittest.TestCase):
    """打包出来的应用不能带任何默认账号密码（凭据由用户在界面里填）"""

    def test_config_defaults_have_no_credentials(self):
        cfg = Config({})
        self.assertEqual(cfg.nas["username"], "")
        self.assertEqual(cfg.nas["password"], "")
        # 但主机/端口有合理默认，装完只差账号密码
        self.assertEqual(cfg.nas["host"], "127.0.0.1")
        self.assertEqual(cfg.nas["port"], 5666)

    def test_instances_do_not_pollute_defaults(self):
        a = Config({})
        a.update({"nas": {"password": "临时密码", "username": "tmp"}})
        b = Config({})
        self.assertEqual(b.nas["password"], "")
        self.assertEqual(b.nas["username"], "")
        from mcp.config import DEFAULTS
        self.assertEqual(DEFAULTS["nas"]["password"], "")

    def test_public_view_reports_not_configured(self):
        view = Config({}).public_view()
        self.assertFalse(view["nas"]["password_set"])

    def test_build_default_config_has_no_credentials(self):
        sys.path.insert(0, os.path.join(ROOT, "tools"))
        import build_nas_app
        cfg = build_nas_app.default_config()
        self.assertEqual(cfg["nas"]["username"], "")
        self.assertEqual(cfg["nas"]["password"], "")
        self.assertEqual(cfg["nas"]["host"], "127.0.0.1")
        self.assertEqual(cfg["server"]["port"], 8686)
        # 显式传参时才预置
        preset = build_nas_app.default_config(9000, "someone", "secret")
        self.assertEqual(preset["nas"]["username"], "someone")
        self.assertEqual(preset["server"]["port"], 9000)

    def test_ui_shows_setup_hint_when_unconfigured(self):
        js = open(os.path.join(ROOT, "mcp", "webui", "app.js"), encoding="utf-8").read()
        self.assertIn("待配置账号", js)
        self.assertIn("还没有账号密码", js)
        self.assertIn("configured", js)

    def test_bridge_reports_not_configured(self):
        from mcp.fnnas import FnOsBridge, BridgeError
        bridge = FnOsBridge(Config({}), app_dir=ROOT)
        try:
            with self.assertRaises(BridgeError) as ctx:
                bridge.connect()
            self.assertEqual(ctx.exception.code, "not_configured")
            self.assertFalse(bridge.status()["configured"])
        finally:
            bridge.close()



if __name__ == "__main__":
    unittest.main(verbosity=2)
