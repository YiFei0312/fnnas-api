# -*- coding: utf-8 -*-
"""
飞牛接口 MCP Server。

把 fnnas-api 项目里的 476 个 WebSocket 接口 + 151 个 /p 相册 HTTP 接口
封装成一个 MCP（Model Context Protocol）Server，同时提供：
    - MCP Streamable HTTP 传输（POST /mcp）
    - MCP HTTP+SSE 传输（GET /sse）
    - Web UI（接口文档 + 两个传输开关 + 可用接口清单）
    - stdio 传输（本地客户端用）

用法见 `mcp/server.py` 顶部说明。
"""

__version__ = "1.0.0"
__all__ = ["server", "protocol", "tools", "fnnas", "config", "http_server"]
