# -*- coding: utf-8 -*-
"""
飞牛连接层：把异步 SDK（`sdk.FnOsClient`）包成一个线程安全的同步门面。

MCP server 是「多客户端并发调用」的模型，而 WebSocket 客户端是 asyncio 的，
所以这里单独起一个后台事件循环线程，所有 SDK 调用都通过队列丢进去执行，
同一时刻只跑一个协程（fnOS 的 WS 是 reqid 配对的，串行最稳），调用方阻塞等结果。

两类接口都能调：
    - WebSocket RPC：`call("file.ls", {"path": "/vol1/1000"})`
    - HTTP REST（/p 相册应用）：`http_call("GET", "/api/v1/album/list", params={...})`
"""

import asyncio
import json
import logging
import os
import sys
import threading
import time
import traceback

log = logging.getLogger("fnnas.bridge")


class BridgeError(Exception):
    """连接/登录/接口错误"""

    def __init__(self, message, code=None, detail=None):
        self.code = code
        self.detail = detail
        super().__init__(message)


class FnOsBridge:
    """
    一个进程里只该有一个实例。所有方法都是同步阻塞的（内部切到事件循环线程）。
    """

    def __init__(self, config, app_dir=None):
        self.config = config
        self.app_dir = app_dir or _guess_app_dir()
        self._loop = None
        self._thread = None
        self._ready = threading.Event()
        self._client = None
        self._token = None
        self._lock = asyncio.Lock() if False else None       # asyncio 对象在循环线程里建
        self._alock = None
        self._run_lock = threading.Lock()                    # 跨线程串行化
        self._last_error = None
        self._connected_at = None
        self._login_lock = threading.Lock()
        self._calls = 0
        self._calls_failed = 0
        self._start_loop()

    # ------------------------------------------------------------- 事件循环
    def _start_loop(self):
        def runner():
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._alock = asyncio.Lock()
            self._ready.set()
            self._loop.run_forever()

        self._thread = threading.Thread(target=runner, name="fnnas-loop", daemon=True)
        self._thread.start()
        self._ready.wait(5)

    def _submit(self, coro, timeout):
        if not self._ready.is_set() or self._loop is None:
            raise BridgeError("内部事件循环没起来")
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        try:
            return future.result(timeout)
        except BridgeError:
            raise
        except Exception as exc:                                    # noqa: BLE001
            raise BridgeError("%s: %s" % (type(exc).__name__, exc),
                              detail=traceback.format_exc()[-1200:])

    # ------------------------------------------------------------- SDK 装载
    def _load_sdk(self):
        """把仓库里的 sdk/ 和 vendor 依赖加进 sys.path"""
        candidates = [
            os.path.join(self.app_dir, "lib"),
            os.path.join(self.app_dir, "vendor"),
            # 开发模式（直接在仓库里跑）时的依赖目录
            os.path.join(self.app_dir, "build", "vendor"),
            os.path.join(self.app_dir, "build", "lib"),
            os.path.join(self.app_dir),
        ]
        for path in reversed(candidates):
            if path and os.path.isdir(path) and path not in sys.path:
                sys.path.insert(0, path)
        import sdk                                                  # noqa: F401
        return sdk

    async def _connect_and_login(self):
        sdk = self._load_sdk()
        if self._client is not None:
            try:
                await self._client.close()
            except Exception:
                pass
            self._client = None
        nas = self.config.nas
        if not (nas.get("username") or "").strip() or not (nas.get("password") or "").strip():
            raise BridgeError(
                "还没配置 NAS 账号密码：请在界面顶部「飞牛连接配置」里填写 IP / 账号 / 密码，"
                "然后点「保存并重连」", code="not_configured")
        client = sdk.FnOsClient(ping_interval=60)
        client.logger.setLevel(logging.WARNING)
        await asyncio.wait_for(client.connect(self.config.ws_url), timeout=20)
        ok = await asyncio.wait_for(
            client.login(nas["username"], nas.get("password") or ""), timeout=40)
        if not ok:
            raise BridgeError("登录失败（账号或密码不对）", code="login_failed")
        self._client = client
        self._token = client.token
        self._last_error = None
        self._connected_at = time.time()
        return client

    # ------------------------------------------------------------- 连接管理
    def connect(self, force=False, timeout=60):
        """确保已连接并登录；失败抛 BridgeError"""
        with self._login_lock:
            if self._client is not None and not force:
                ws = getattr(self._client, "websocket", None)
                if ws is not None and getattr(ws, "state", None) is not None:
                    try:
                        from websockets.protocol import State
                        if ws.state is State.OPEN:
                            return self._client
                    except Exception:
                        pass

            async def _do():
                return await self._connect_and_login()

            try:
                client = self._submit(_do(), timeout)
            except Exception as exc:
                self._last_error = str(exc)
                self._client = None
                raise
            log.info("已登录飞牛 NAS：%s", self.config.ws_url)
            return client

    def close(self):
        if self._client is None:
            return
        async def _do():
            try:
                await self._client.close()
            except Exception:
                pass
        try:
            self._submit(_do(), 10)
        finally:
            self._client = None

    # ------------------------------------------------------------- WS 调用
    def call(self, req, params=None, nested=False, timeout=60, retry=True):
        """
        调一个 WebSocket RPC，返回**完整响应**（含 result / errno / data 等）。

        写接口（file.cp/rm/...）只回 ack，任务结果要用 `task_call` 等推送。
        """
        params = params or {}
        started = time.time()

        async def _do():
            client = self._client or await self._connect_and_login()
            async with self._alock:
                return await asyncio.wait_for(
                    client.call(req, params, nested=nested), timeout=timeout)

        self._calls += 1
        try:
            try:
                return self._submit(_do(), timeout + 15)
            except BridgeError:
                if not retry:
                    raise
                log.warning("调用 %s 失败，重连后重试一次", req)
                self.connect(force=True)
                return self._submit(_do(), timeout + 15)
        except Exception:
            self._calls_failed += 1
            raise
        finally:
            log.debug("%s 用时 %.0fms", req, (time.time() - started) * 1000)

    @staticmethod
    def unwrap(resp, key=None):
        """
        把响应变干净：有 errno / result=fail 就抛错，否则返回 data（或 key 指定的字段）。
        """
        if resp is None:
            raise BridgeError("接口没有返回")
        errno = resp.get("errno")
        result = resp.get("result")
        if errno not in (None, 0) or result == "fail":
            raise BridgeError(resp.get("errmsg") or "接口返回失败",
                              code=errno or result, detail=resp)
        data = resp.get("data")
        if isinstance(data, dict):
            if key:
                return data.get(key, data)
            return data
        if data is None:
            # 有些接口把结果直接放在顶层（file.ls -> files, file.prop -> prop ...）
            inner = {k: v for k, v in resp.items()
                     if k not in ("result", "reqid", "errno", "errmsg", "rev")}
            if key:
                return inner.get(key, inner)
            return inner
        return data

    def call_data(self, req, params=None, nested=False, timeout=60, key=None, retry=True):
        return self.unwrap(self.call(req, params, nested=nested, timeout=timeout,
                                     retry=retry), key)

    def task_call(self, req, params, timeout=180):
        """
        写接口（异步任务）：发请求拿到 reqid，再等同 reqid 的推送，返回最终结果。
        成功返回任务结果字典，失败抛 BridgeError。
        """
        async def _do():
            client = self._client or await self._connect_and_login()
            async with self._alock:
                from sdk.filetasks import call_file_task, is_task_ok, task_error
                resp = await asyncio.wait_for(
                    client.call(req, params), timeout=30)
                reqid = resp.get("reqid")
                result = await asyncio.wait_for(
                    call_file_task(client, reqid, timeout=timeout), timeout=timeout + 10)
                if result is None:
                    raise BridgeError("等待任务结果超时（%s）" % req, code="task_timeout")
                if not is_task_ok(result):
                    raise BridgeError("任务失败：%s" % task_error(result),
                                      code="task_failed", detail=result)
                return result

        return self._submit(_do(), timeout + 30)

    # ------------------------------------------------------------- HTTP 调用
    def http_call(self, method, path, params=None, body=None, timeout=30):
        """
        调 `/p`（相册应用）的 HTTP API：cookie `fnos-token` + `authx` 签名。
        返回 `{code, msg, data}`，code != 0 抛 BridgeError。
        """
        self.connect()                       # 顺便保证有 token
        from sdk.http_photo import make_authx
        import urllib.error
        import urllib.parse
        import urllib.request

        method = method.upper()
        if not path.startswith("/"):
            path = "/" + path
        api_path = "/p" + path if not path.startswith("/p/") else path
        base = self.config.http_base
        url = base + api_path
        query = ("?" + urllib.parse.urlencode(params)) if params else ""
        payload = body if body is not None else ({} if method != "GET" else None)
        headers = {
            "User-Agent": "fnnas-mcp/1.0",
            "Cookie": "fnos-token=" + (self._token or ""),
            "authx": make_authx(method, api_path, params=params, body=payload),
        }
        data = None
        if method != "GET":
            headers["Content-Type"] = "application/json"
            data = json.dumps(payload, separators=(",", ":")).encode()
        request = urllib.request.Request(url + query, data=data, headers=headers,
                                        method=method)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as resp:
                raw = resp.read()
        except urllib.error.HTTPError as exc:
            raise BridgeError("HTTP %s（%s）" % (exc.code, path),
                              code=exc.code)
        except Exception as exc:                                    # noqa: BLE001
            raise BridgeError("请求 %s 失败：%s" % (path, exc))
        try:
            doc = json.loads(raw.decode("utf-8", "replace"))
        except Exception:
            raise BridgeError("%s 返回的不是 JSON" % path)
        if doc.get("code") != 0:
            raise BridgeError(doc.get("msg") or ("code=%s" % doc.get("code")),
                              code=doc.get("code"), detail=doc)
        return doc

    # ------------------------------------------------------------- 状态
    def status(self):
        nas = self.config.nas
        return {
            "configured": bool((nas.get("username") or "").strip()
                               and (nas.get("password") or "").strip()),
            "connected": self._client is not None,
            "host": self.config.nas.get("host"),
            "port": self.config.nas.get("port"),
            "username": self.config.nas.get("username"),
            "ws_url": self.config.ws_url,
            "http_base": self.config.http_base,
            "connected_at": self._connected_at,
            "calls": self._calls,
            "calls_failed": self._calls_failed,
            "last_error": self._last_error,
        }

    def test(self):
        """连通性 + 登录测试（UI 上的「测试连接」）"""
        started = time.time()
        try:
            self.connect(force=True)
            info = self.call_data("user.info", key="userInfo") or {}
            # user.info 里的用户名字段叫 "user"；顺手算一下是否管理员
            user = {
                "name": info.get("user") or info.get("name") or "",
                "uid": info.get("uid"),
                "admin": bool(info.get("admin")),
            }
            self._last_error = None
            return {"ok": True, "elapsed_ms": round((time.time() - started) * 1000),
                    "user": user, "host": self.config.nas.get("host"),
                    "port": self.config.nas.get("port")}
        except Exception as exc:                                    # noqa: BLE001
            self._last_error = str(exc)
            return {"ok": False, "elapsed_ms": round((time.time() - started) * 1000),
                    "error": str(exc), "host": self.config.nas.get("host"),
                    "port": self.config.nas.get("port")}


def _guess_app_dir():
    """应用安装目录：优先 TRIM_APPDEST，否则用包所在目录"""
    if os.environ.get("TRIM_APPDEST"):
        return os.environ["TRIM_APPDEST"]
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
