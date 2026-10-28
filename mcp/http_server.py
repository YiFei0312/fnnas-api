# -*- coding: utf-8 -*-
"""
HTTP 服务：Web UI + 两个 MCP 传输端点。

路由：
    GET  /                      Web UI（单页）
    GET  /static/*              UI 静态资源
    GET  /docs                 接口文档（476 WS + 151 HTTP，单文件 HTML）
    GET  /api/status           状态（连接、可用接口数、两个 MCP 端点地址）
    GET  /api/interfaces       可用接口清单（支持 keyword / protocol / only_available）
    GET  /api/config           当前配置（密码遮罩）
    POST /api/config           保存配置（两个 MCP 开关、NAS 账号等）
    POST /api/test             测试 NAS 连接（重新登录）
    POST /api/reconnect        强制重连
    GET  /api/logs             最近日志
    GET  /healthz              健康检查

    MCP Streamable HTTP:  POST/GET/DELETE /mcp
    MCP HTTP+SSE（旧版）:  GET /sse + POST /messages?sessionId=...
"""

import json
import logging
import mimetypes
import os
import queue
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from .protocol import McpServer
from . import tools as tools_mod

log = logging.getLogger("fnnas.http")

MIME = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
    ".woff2": "font/woff2",
}


class SseSession:
    """旧版 HTTP+SSE 传输：一个 GET /sse 连接 + 对应的一串 POST /messages"""

    def __init__(self):
        self.id = uuid.uuid4().hex
        self.queue = queue.Queue()
        self.closed = threading.Event()
        self.created = time.time()


class FnMcpHttpServer:
    def __init__(self, config, bridge, app_dir=None, version="1.0.0"):
        self.config = config
        self.bridge = bridge
        self.app_dir = app_dir or os.environ.get("TRIM_APPDEST") or \
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.version = version
        data_dir = os.path.join(self.app_dir, "data")
        self.mcp = McpServer(bridge, config, data_dir=data_dir, version=version)
        self.sessions = {}
        self.sessions_lock = threading.Lock()
        self.started_at = time.time()
        self.server = None

    # ------------------------------------------------------------- 启动
    def serve_forever(self, host="0.0.0.0", port=None):
        port = int(port or self.config.server.get("port") or 8686)

        outer = self

        class Handler(BaseHTTPRequestHandler):
            server_version = "fnnas-mcp/1.0"
            protocol_version = "HTTP/1.1"

            def log_message(self, fmt, *args):                      # noqa: A003
                log.debug("%s - %s", self.address_string(), fmt % args)

            # ------------------------------------------------- 便捷
            def _send(self, status, body=b"", ctype="application/json; charset=utf-8",
                      extra=None):
                if isinstance(body, (dict, list)):
                    body = json.dumps(body, ensure_ascii=False).encode()
                elif isinstance(body, str):
                    body = body.encode("utf-8")
                self.send_response(status)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                for k, v in (extra or {}).items():
                    self.send_header(k, v)
                self.end_headers()
                try:
                    self.wfile.write(body)
                except (BrokenPipeError, ConnectionResetError):
                    pass

            def _json(self, status, payload, extra=None):
                self._send(status, payload, extra=extra)

            def _read_json(self, limit=4 * 1024 * 1024):
                length = int(self.headers.get("Content-Length") or 0)
                if length > limit:
                    raise ValueError("请求体太大")
                raw = self.rfile.read(length) if length else b""
                if not raw:
                    return {}
                return json.loads(raw.decode("utf-8", "replace"))

            def _base_url(self):
                host = self.headers.get("Host") or ("127.0.0.1:%s" %
                                                    outer.config.server.get("port"))
                return "http://" + host

            def _sse_headers(self):
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream; charset=utf-8")
                self.send_header("Cache-Control", "no-cache, no-transform")
                self.send_header("Connection", "keep-alive")
                self.send_header("X-Accel-Buffering", "no")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()

            def _write_event(self, event, data):
                chunk = ""
                if event:
                    chunk += "event: %s\n" % event
                chunk += "data: %s\n\n" % data
                self.wfile.write(chunk.encode("utf-8"))
                self.wfile.flush()

            # ------------------------------------------------- 路由
            def do_OPTIONS(self):
                self.send_response(204)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Access-Control-Allow-Methods",
                                 "GET, POST, DELETE, OPTIONS")
                self.send_header("Access-Control-Allow-Headers",
                                 "Content-Type, Accept, Mcp-Session-Id, "
                                 "Last-Event-ID, Authorization")
                self.send_header("Content-Length", "0")
                self.end_headers()

            def do_GET(self):
                path = urlparse(self.path).path
                try:
                    if path in ("/", "/index.html"):
                        return self._static("index.html")
                    if path.startswith("/static/"):
                        return self._static(path[len("/static/"):])
                    if path in ("/docs", "/docs.html", "/interfaces.html"):
                        return self._docs()
                    if path in ("/healthz", "/api/health"):
                        return self._json(200, {"ok": True})
                    if path == "/api/status":
                        return self._json(200, outer.status_payload(self._base_url()))
                    if path == "/api/interfaces":
                        return self._interfaces()
                    if path == "/api/config":
                        return self._json(200, outer.config.public_view())
                    if path == "/api/logs":
                        return self._json(200, {"lines": outer.recent_logs()})
                    if path == outer.config.server["sse"].get("path", "/sse"):
                        return self._sse_stream()
                    if path == outer.config.server["mcp"].get("path", "/mcp"):
                        return self._mcp_stream()
                    self._json(404, {"error": "not found", "path": path})
                except (BrokenPipeError, ConnectionResetError):
                    pass
                except Exception as exc:                            # noqa: BLE001
                    log.exception("GET %s 出错", path)
                    try:
                        self._json(500, {"error": str(exc)})
                    except Exception:
                        pass

            def do_POST(self):
                parsed = urlparse(self.path)
                path = parsed.path
                try:
                    if path == "/api/config":
                        return self._save_config()
                    if path == "/api/test":
                        return self._test_connection()
                    if path == "/api/reconnect":
                        return self._reconnect()
                    if path == "/messages":
                        return self._sse_post(parse_qs(parsed.query))
                    if path == outer.config.server["mcp"].get("path", "/mcp"):
                        return self._mcp_post()
                    self._json(404, {"error": "not found", "path": path})
                except (BrokenPipeError, ConnectionResetError):
                    pass
                except json.JSONDecodeError:
                    self._json(400, {"jsonrpc": "2.0", "id": None,
                                     "error": {"code": -32700, "message": "JSON 解析失败"}})
                except Exception as exc:                            # noqa: BLE001
                    log.exception("POST %s 出错", path)
                    try:
                        self._json(500, {"jsonrpc": "2.0", "id": None,
                                         "error": {"code": -32603,
                                                   "message": str(exc)}})
                    except Exception:
                        pass

            def do_DELETE(self):
                path = urlparse(self.path).path
                if path == outer.config.server["mcp"].get("path", "/mcp"):
                    sid = self.headers.get("Mcp-Session-Id")
                    if sid:
                        outer.remove_session(sid)
                    return self._send(200, b"")
                self._send(404, b"")

            # ------------------------------------------------- 静态 / 文档
            def _static(self, rel):
                rel = rel.replace("\\", "/").lstrip("/")
                if ".." in rel.split("/"):
                    return self._json(403, {"error": "forbidden"})
                # 打包后是 <app>/webui；直接在仓库里跑时是 <repo>/mcp/webui
                for base in (os.path.join(outer.app_dir, "webui"),
                             os.path.join(outer.app_dir, "mcp", "webui")):
                    path = os.path.join(base, rel)
                    if os.path.isfile(path):
                        ctype = MIME.get(os.path.splitext(path)[1].lower(),
                                         "application/octet-stream")
                        with open(path, "rb") as f:
                            body = f.read()
                        return self._send(200, body, ctype)
                return self._json(404, {"error": "static not found", "file": rel})

            def _docs(self):
                # 打包后：<app>/data/interfaces.html；仓库里：docs/api/interfaces.html
                for path in (os.path.join(outer.app_dir, "data", "interfaces.html"),
                             os.path.join(outer.app_dir, "docs", "api",
                                          "interfaces.html")):
                    if os.path.isfile(path):
                        with open(path, "rb") as f:
                            return self._send(200, f.read(),
                                              "text/html; charset=utf-8")
                self._json(404, {"error": "文档还没生成"})

            # ------------------------------------------------- 业务 API
            def _interfaces(self):
                query = parse_qs(urlparse(self.path).query)
                keyword = (query.get("keyword") or [""])[0].strip().lower()
                protocol = (query.get("protocol") or ["all"])[0]
                only_available = (query.get("only_available") or ["1"])[0] not in ("0", "false")
                limit = int((query.get("limit") or ["300"])[0])
                offset = int((query.get("offset") or ["0"])[0])
                items = tools_mod.menu_entries()
                out = []
                for it in items:
                    if protocol != "all" and it["protocol"] != protocol:
                        continue
                    if only_available and not it["available"]:
                        continue
                    if keyword:
                        hay = " ".join([it["name"], it["group"], it["purpose"],
                                        it["params"], it["status"]]).lower()
                        if keyword not in hay:
                            continue
                    out.append(it)
                total = len(out)
                self._json(200, {"total": total,
                                 "items": out[offset:offset + limit],
                                 "offset": offset, "limit": limit})

            def _save_config(self):
                payload = self._read_json()
                nas_changed = any(k in (payload.get("nas") or {})
                                  for k in ("host", "port", "username", "password"))
                outer.config.update(payload)
                outer.config.save()
                log.info("配置已保存（MCP=%s, SSE=%s）",
                         outer.config.mcp_enabled(), outer.config.sse_enabled())
                if nas_changed:
                    threading.Thread(target=outer.safe_reconnect, daemon=True).start()
                self._json(200, {"ok": True, "config": outer.config.public_view()})

            def _test_connection(self):
                result = outer.bridge.test()
                self._json(200, result)

            def _reconnect(self):
                threading.Thread(target=outer.safe_reconnect, daemon=True).start()
                self._json(200, {"ok": True, "message": "正在重连"})

            # ------------------------------------------------- MCP：旧版 SSE
            def _sse_stream(self):
                if not outer.config.sse_enabled():
                    return self._json(404, {"error": "SSE 传输已在界面上关闭",
                                            "enable_at": "/api/config"})
                session = outer.new_session()
                log.info("SSE 客户端接入：%s", session.id)
                self._sse_headers()
                try:
                    self._write_event("endpoint",
                                      "/messages?sessionId=" + session.id)
                    while not session.closed.is_set():
                        try:
                            item = session.queue.get(timeout=15)
                        except queue.Empty:
                            self.wfile.write(b": ping\n\n")
                            self.wfile.flush()
                            continue
                        if item is None:
                            break
                        self._write_event("message",
                                          json.dumps(item, ensure_ascii=False))
                except (BrokenPipeError, ConnectionResetError):
                    pass
                finally:
                    outer.remove_session(session.id)
                    log.info("SSE 客户端断开：%s", session.id)

            def _sse_post(self, query):
                if not outer.config.sse_enabled():
                    return self._json(404, {"error": "SSE 传输已关闭"})
                sid = (query.get("sessionId") or [""])[0]
                session = outer.get_session(sid)
                if session is None:
                    return self._json(404, {"error": "会话不存在或已过期，请重新连 /sse"})
                message = self._read_json()
                response = outer.mcp.handle(message)
                if response is not None:
                    session.queue.put(response)
                self._send(202, b"", "text/plain; charset=utf-8")

            # ------------------------------------------------- MCP：Streamable HTTP
            def _mcp_post(self):
                if not outer.config.mcp_enabled():
                    return self._json(404, {"jsonrpc": "2.0", "id": None,
                                            "error": {"code": -32000,
                                                      "message": "Streamable HTTP 传输已在界面上关闭"}})
                message = self._read_json()
                response = outer.mcp.handle(message)
                if response is None:
                    return self._send(202, b"", "text/plain; charset=utf-8")
                sid = self.headers.get("Mcp-Session-Id")
                extra = {}
                if not sid:
                    sid = uuid.uuid4().hex
                    outer.add_session(sid)
                extra["Mcp-Session-Id"] = sid
                accept = (self.headers.get("Accept") or "").lower()
                if "text/event-stream" in accept:
                    body = "event: message\ndata: %s\n\n" % json.dumps(
                        response, ensure_ascii=False)
                    return self._send(200, body,
                                      "text/event-stream; charset=utf-8", extra)
                self._json(200, response, extra)

            def _mcp_stream(self):
                """GET /mcp：服务端主动消息流（当前只会发心跳，保证客户端不超时）"""
                if not outer.config.mcp_enabled():
                    return self._json(404, {"error": "Streamable HTTP 传输已关闭"})
                self._sse_headers()
                try:
                    while True:
                        self.wfile.write(b": ping\n\n")
                        self.wfile.flush()
                        time.sleep(15)
                except (BrokenPipeError, ConnectionResetError):
                    pass
                except Exception:                                   # noqa: BLE001
                    pass

        self.server = ThreadingHTTPServer((host, port), Handler)
        self.server.daemon_threads = True
        log.info("HTTP 服务已启动：http://%s:%s/（MCP: %s, SSE: %s）",
                 host, port,
                 self.config.server["mcp"].get("path", "/mcp"),
                 self.config.server["sse"].get("path", "/sse"))
        self.server.serve_forever()

    # ------------------------------------------------------------- 会话
    def new_session(self):
        session = SseSession()
        with self.sessions_lock:
            self.sessions[session.id] = session
        return session

    def get_session(self, sid):
        with self.sessions_lock:
            return self.sessions.get(sid)

    def add_session(self, sid):
        with self.sessions_lock:
            self.sessions[sid] = SseSession()

    def remove_session(self, sid):
        with self.sessions_lock:
            session = self.sessions.pop(sid, None)
        if session is not None:
            session.closed.set()
            session.queue.put(None)

    # ------------------------------------------------------------- 状态
    def status_payload(self, base_url=None):
        base = (base_url or ("http://127.0.0.1:%s" % self.config.server.get("port"))).rstrip("/")
        mcp_cfg = self.config.server["mcp"]
        sse_cfg = self.config.server["sse"]
        stats = tools_mod.stats()
        return {
            "ok": True,
            "server": {
                "version": self.version,
                "port": self.config.server.get("port"),
                "uptime": round(time.time() - self.started_at),
                "started_at": self.started_at,
            },
            "mcp": {
                "enabled": self.config.mcp_enabled(),
                "path": mcp_cfg.get("path", "/mcp"),
                "url": base + mcp_cfg.get("path", "/mcp"),
                "transport": "streamable-http",
            },
            "sse": {
                "enabled": self.config.sse_enabled(),
                "path": sse_cfg.get("path", "/sse"),
                "url": base + sse_cfg.get("path", "/sse"),
                "messages_url": base + "/messages",
                "transport": "http+sse",
                "sessions": len(self.sessions),
            },
            "connection": self.bridge.status(),
            "stats": stats,
            "desktop_url": base,
        }

    def safe_reconnect(self):
        try:
            self.bridge.connect(force=True)
            log.info("重连成功")
        except Exception as exc:                                    # noqa: BLE001
            log.warning("重连失败：%s", exc)

    def recent_logs(self, limit=300):
        handler = getattr(self, "log_handler", None)
        if handler is None:
            return []
        return handler.lines(limit)
