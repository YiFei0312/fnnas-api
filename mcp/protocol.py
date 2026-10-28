# -*- coding: utf-8 -*-
"""
MCP 协议实现（JSON-RPC 2.0 + MCP 2025-06-18 的方法子集）。

这个文件不碰传输层：stdio / SSE / Streamable HTTP 都把消息丢给 `McpServer.handle()`，
拿回一个 JSON-RPC 响应（通知类返回 None）。

支持的方法：
    initialize / notifications/initialized / ping
    tools/list / tools/call
    resources/list / resources/read（把接口文档当资源暴露）
    prompts/list / logging/setLevel
"""

import json
import logging

from . import tools as tools_mod

log = logging.getLogger("fnnas.mcp")

PROTOCOL_VERSION = "2025-06-18"
SUPPORTED_PROTOCOL_VERSIONS = ["2025-06-18", "2025-03-26", "2024-11-05"]

SERVER_INFO = {
    "name": "fnnas-mcp",
    "title": "飞牛接口 MCP Server",
    "version": "1.0.0",
}

INSTRUCTIONS = (
    "这是飞牛 fnOS NAS 的 MCP Server，封装了 476 个 WebSocket 接口和 151 个 /p 相册应用 "
    "HTTP 接口。\n"
    "- 先用 fnnas_interfaces_search / fnnas_http_interfaces_search 找接口（只会返回实测可用的），"
    "再用 fnnas_interface_call / fnnas_http_api_call 调用；\n"
    "- 常用操作有精选工具（fnnas_file_ls、fnnas_share_link_create、fnnas_photo_list 等），优先用它们；\n"
    "- 写操作（复制/移动/删除/压缩）是异步任务，工具内部会等任务结束；\n"
    "- 相册接口的时间参数必须是 `YYYY:MM:DD HH:mm:ss` 这种冒号日期格式。"
)


class JsonRpcError(Exception):
    def __init__(self, code, message, data=None):
        self.code = code
        self.message = message
        self.data = data
        super().__init__(message)


PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603


class McpServer:
    def __init__(self, bridge, config, data_dir=None, version="1.0.0"):
        self.bridge = bridge
        self.config = config
        if data_dir:
            tools_mod.set_data_dir(data_dir)
        self.server_info = dict(SERVER_INFO, version=version)
        self._init_done = False
        self.sessions = set()

    # ------------------------------------------------------------- 入口
    def handle(self, message):
        """
        处理一条 JSON-RPC 消息。
        返回响应 dict；如果消息是通知（没有 id）返回 None。
        批量请求（list）也能处理，返回 list。
        """
        if isinstance(message, list):
            if not message:
                return self._error(None, INVALID_REQUEST, "空的批量请求")
            responses = [self._handle_one(m) for m in message]
            responses = [r for r in responses if r is not None]
            return responses or None
        return self._handle_one(message)

    def _handle_one(self, message):
        if not isinstance(message, dict):
            return self._error(None, INVALID_REQUEST, "消息必须是 JSON 对象")
        msg_id = message.get("id")
        method = message.get("method")
        params = message.get("params") or {}
        is_notification = "id" not in message

        if not isinstance(method, str):
            return self._error(msg_id, INVALID_REQUEST, "缺少 method")
        try:
            result = self._dispatch(method, params)
        except JsonRpcError as exc:
            if is_notification:
                log.warning("通知 %s 处理失败：%s", method, exc.message)
                return None
            return self._error(msg_id, exc.code, exc.message, exc.data)
        except Exception as exc:                                    # noqa: BLE001
            log.exception("处理 %s 出错", method)
            if is_notification:
                return None
            return self._error(msg_id, INTERNAL_ERROR,
                               "%s: %s" % (type(exc).__name__, exc))
        if is_notification:
            return None
        return {"jsonrpc": "2.0", "id": msg_id, "result": result}

    def _dispatch(self, method, params):
        handler = {
            "initialize": self._initialize,
            "ping": lambda p: {},
            "tools/list": self._tools_list,
            "tools/call": self._tools_call,
            "resources/list": self._resources_list,
            "resources/read": self._resources_read,
            "prompts/list": lambda p: {"prompts": []},
            "logging/setLevel": lambda p: {},
            "notifications/initialized": lambda p: {},
            "notifications/cancelled": lambda p: {},
        }.get(method)
        if handler is None:
            raise JsonRpcError(METHOD_NOT_FOUND, "不支持的方法：%s" % method)
        return handler(params)

    # ------------------------------------------------------------- MCP 方法
    def _initialize(self, params):
        requested = params.get("protocolVersion") or PROTOCOL_VERSION
        version = requested if requested in SUPPORTED_PROTOCOL_VERSIONS else PROTOCOL_VERSION
        self._init_done = True
        return {
            "protocolVersion": version,
            "capabilities": {
                "tools": {"listChanged": False},
                "resources": {"subscribe": False, "listChanged": False},
            },
            "serverInfo": self.server_info,
            "instructions": INSTRUCTIONS,
        }

    def _tools_list(self, params):
        defs = tools_mod.tool_definitions(
            include_unverified=self.config.include_unverified())
        return {"tools": defs}

    def _tools_call(self, params):
        name = params.get("name")
        arguments = params.get("arguments") or {}
        tool = tools_mod.find_tool(name)
        if tool is None:
            raise JsonRpcError(INVALID_PARAMS, "没有这个工具：%s" % name)
        if not isinstance(arguments, dict):
            raise JsonRpcError(INVALID_PARAMS, "arguments 必须是对象")
        # 参数校验：必填项
        schema = tool["inputSchema"] or {}
        missing = [k for k in schema.get("required") or [] if k not in arguments]
        if missing:
            raise JsonRpcError(INVALID_PARAMS,
                               "缺少必填参数：%s" % ", ".join(missing))
        try:
            result = tool["handler"](self.bridge, arguments)
        except Exception as exc:                                    # noqa: BLE001
            log.warning("工具 %s 调用失败：%s", name, exc)
            return {
                "content": [{"type": "text",
                             "text": "调用失败：%s" % exc}],
                "isError": True,
            }
        text = _dumps(result)
        out = {"content": [{"type": "text", "text": text}], "isError": False}
        if isinstance(result, dict):
            out["structuredContent"] = result
        return out

    def _resources_list(self, params):
        return {"resources": [
            {"uri": "fnnas://docs/interfaces", "name": "接口文档（476 WS + 151 HTTP）",
             "description": "单文件 HTML 接口文档：每个接口的用途、参数、返回字段与实测状态",
             "mimeType": "text/html"},
            {"uri": "fnnas://status", "name": "服务状态",
             "description": "飞牛连接状态、可用接口数量、工具数量",
             "mimeType": "application/json"},
        ]}

    def _resources_read(self, params):
        uri = params.get("uri")
        if uri == "fnnas://status":
            return {"contents": [{"uri": uri, "mimeType": "application/json",
                                  "text": _dumps(self._status_payload())}]}
        if uri == "fnnas://docs/interfaces":
            html = _read_docs()
            return {"contents": [{"uri": uri, "mimeType": "text/html",
                                  "text": html or "文档文件不存在"}]}
        raise JsonRpcError(INVALID_PARAMS, "没有这个资源：%s" % uri)

    def _status_payload(self):
        stats = tools_mod.stats()
        return {"ok": True, "connection": self.bridge.status(), "stats": stats}

    # ------------------------------------------------------------- 工具函数
    @staticmethod
    def _error(msg_id, code, message, data=None):
        err = {"code": code, "message": message}
        if data is not None:
            err["data"] = data
        return {"jsonrpc": "2.0", "id": msg_id, "error": err}


def _dumps(value):
    try:
        return json.dumps(value, ensure_ascii=False, indent=1, default=str)
    except Exception:                                               # noqa: BLE001
        return str(value)


def _read_docs():
    import os
    from .tools import _data_dir
    app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for path in (os.path.join(_data_dir(), "interfaces.html"),
                 os.path.join(app_dir, "data", "interfaces.html"),
                 os.path.join(app_dir, "docs", "api", "interfaces.html")):
        if os.path.exists(path):
            try:
                with open(path, encoding="utf-8", errors="replace") as f:
                    return f.read()
            except Exception:
                continue
    return None
