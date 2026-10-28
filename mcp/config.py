# -*- coding: utf-8 -*-
"""
MCP Server 配置。

配置文件位置（优先级）：
    1. 命令行 --config 指定的路径
    2. 环境变量 FN_MCP_CONFIG
    3. /etc/fnnas-mcp/config.json（fnOS 应用里的 $TRIM_PKGETC/config.json）
    4. 当前目录 config.json

fnOS 应用里 cmd/install_callback 会把默认配置写到 $TRIM_PKGETC/config.json，
所以装完就能直接用，UI 里也可以改（改完写回同一个文件）。
"""

import json
import os

DEFAULTS = {
    "nas": {
        "host": "127.0.0.1",
        "port": 5666,
        # 账号密码不写进包里：安装后在界面「飞牛连接配置」里填，存到 etc/config.json
        "username": "",
        "password": "",
        # 用 HTTP 调 /p 相册接口时的地址；留空则按 host/port 拼
        "base_url": "",
    },
    "server": {
        "port": 8686,
        "mcp": {"enabled": True, "path": "/mcp"},
        "sse": {"enabled": True, "path": "/sse"},
        "tools": {"include_unverified": False},
    },
    "ui": {"title": "飞牛接口 MCP Server"},
}


def _merge(base, extra):
    """深合并：extra 覆盖 base（用 deepcopy，否则改一个实例会污染 DEFAULTS）"""
    import copy
    out = copy.deepcopy(base)
    for k, v in (extra or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = v
    return out


def default_config_path():
    if os.environ.get("FN_MCP_CONFIG"):
        return os.environ["FN_MCP_CONFIG"]
    trim_etc = os.environ.get("TRIM_PKGETC")
    if trim_etc:
        return os.path.join(trim_etc, "config.json")
    return os.path.join(os.getcwd(), "config.json")


class Config:
    def __init__(self, data=None, path=None):
        self.path = path or default_config_path()
        self.data = _merge(DEFAULTS, data or {})

    # ------------------------------------------------------------- 读写
    @classmethod
    def load(cls, path=None):
        path = path or default_config_path()
        data = {}
        if os.path.exists(path):
            try:
                with open(path, encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                data = {}
        return cls(data, path)

    def save(self):
        directory = os.path.dirname(os.path.abspath(self.path))
        os.makedirs(directory, exist_ok=True)
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, self.path)

    # ------------------------------------------------------------- 取字段
    @property
    def nas(self):
        return self.data["nas"]

    @property
    def server(self):
        return self.data["server"]

    @property
    def ws_url(self):
        return "ws://%s:%s/websocket?type=main" % (self.nas["host"], self.nas["port"])

    @property
    def http_base(self):
        base = (self.nas.get("base_url") or "").rstrip("/")
        if base:
            return base
        return "http://%s:%s" % (self.nas["host"], self.nas["port"])

    def mcp_enabled(self):
        return bool(self.server["mcp"].get("enabled"))

    def sse_enabled(self):
        return bool(self.server["sse"].get("enabled"))

    def include_unverified(self):
        return bool(self.server["tools"].get("include_unverified"))

    def public_view(self):
        """给 UI 看的配置（密码做遮罩）"""
        data = json.loads(json.dumps(self.data))
        pwd = data["nas"].get("password") or ""
        data["nas"]["password"] = "••••••••" if pwd else ""
        data["nas"]["password_set"] = bool(pwd)
        return data

    def update(self, payload):
        """UI 提上来的局部更新；密码传空字符串表示不改"""
        payload = payload or {}
        if "nas" in payload:
            nas = payload["nas"] or {}
            for k in ("host", "base_url", "username", "password"):
                if k in nas:
                    value = nas.get(k)
                    # 密码：空字符串或 UI 里的遮罩占位都表示「不修改」
                    if k == "password" and (not value or str(value).startswith("•")):
                        continue
                    self.data["nas"][k] = value
            if "port" in nas and nas["port"]:
                self.data["nas"]["port"] = int(nas["port"])
        if "server" in payload:
            srv = payload["server"] or {}
            for key in ("mcp", "sse"):
                if key in srv and "enabled" in (srv[key] or {}):
                    self.data["server"][key]["enabled"] = bool(srv[key]["enabled"])
            tools = srv.get("tools") or {}
            if "include_unverified" in tools:
                self.data["server"]["tools"]["include_unverified"] = bool(
                    tools["include_unverified"])
        if "ui" in payload and isinstance(payload["ui"], dict):
            if payload["ui"].get("title"):
                self.data["ui"]["title"] = payload["ui"]["title"]
        return self.data

    def replace_password(self, pwd):
        """把配置里的占位密码换成真实密码（保存时用）"""
        if pwd and not pwd.startswith("•"):
            self.data["nas"]["password"] = pwd
