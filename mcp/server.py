# -*- coding: utf-8 -*-
"""
飞牛接口 MCP Server —— 进程入口。

两种运行方式：
    python -m mcp.server --stdio                      # 本地 MCP 客户端（Claude Desktop 等）
    python -m mcp.server --http --port 8686           # 飞牛 NAS 应用模式：Web UI + 两个 MCP 传输

在飞牛 NAS 上由应用的 `cmd/main` 用第二种方式拉起，端口由 manifest 的 service_port 决定。
"""

import argparse
import json
import logging
import os
import sys
import threading
import time

def _read_version(default="1.0.0"):
    """优先读 app 目录下的 VERSION 文件（打包时写入，与 manifest 保持一致）"""
    import os as _os
    app_dir = _os.environ.get("TRIM_APPDEST") or \
        _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
    path = _os.path.join(app_dir, "VERSION")
    try:
        with open(path, encoding="utf-8") as fh:
            value = fh.read().strip()
        return value or default
    except OSError:
        return default


VERSION = _read_version()
APP_NAME = "fnnas-mcp"


class RingBufferHandler(logging.Handler):
    """把日志留在内存里给 UI 看（/api/logs）"""

    def __init__(self, capacity=500):
        super().__init__()
        self.capacity = capacity
        self._lines = []
        self._lock = threading.Lock()

    def emit(self, record):
        try:
            msg = "%s %-7s %s: %s" % (
                time.strftime("%m-%d %H:%M:%S", time.localtime(record.created)),
                record.levelname, record.name, record.getMessage())
            with self._lock:
                self._lines.append(msg)
                if len(self._lines) > self.capacity:
                    del self._lines[:len(self._lines) - self.capacity]
        except Exception:
            pass

    def lines(self, limit=300):
        with self._lock:
            return self._lines[-limit:]


def setup_logging(level=logging.INFO, to_stdout=False):
    root = logging.getLogger()
    root.setLevel(level)
    for old in list(root.handlers):
        root.removeHandler(old)
    stream = sys.stdout if to_stdout else sys.stderr
    fmt = logging.Formatter("%(asctime)s %(levelname)-7s %(name)s: %(message)s",
                            "%Y-%m-%d %H:%M:%S")
    sh = logging.StreamHandler(stream)
    sh.setFormatter(fmt)
    root.addHandler(sh)
    ring = RingBufferHandler()
    root.addHandler(ring)
    return ring


# ---------------------------------------------------------------- stdio 模式
def run_stdio(config, bridge):
    """按行读 JSON-RPC，按行写响应（stdout 只走协议，日志走 stderr）"""
    from .protocol import McpServer

    setup_logging(logging.WARNING)                       # stdio 模式别把日志写 stdout
    app_dir = os.environ.get("TRIM_APPDEST") or \
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    server = McpServer(bridge, config, data_dir=os.path.join(app_dir, "data"),
                       version=VERSION)
    log = logging.getLogger("fnnas.stdio")
    log.info("stdio 模式启动（等待 MCP 客户端）")
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            sys.stdout.write(json.dumps({
                "jsonrpc": "2.0", "id": None,
                "error": {"code": -32700, "message": "JSON 解析失败"}}) + "\n")
            sys.stdout.flush()
            continue
        response = server.handle(message)
        if response is not None:
            sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
            sys.stdout.flush()
    return 0


# ---------------------------------------------------------------- HTTP 模式
def run_http(config, bridge, port=None):
    from .http_server import FnMcpHttpServer

    ring = setup_logging(logging.INFO)
    log = logging.getLogger("fnnas.main")
    app_dir = os.environ.get("TRIM_APPDEST") or \
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    server = FnMcpHttpServer(config, bridge, app_dir=app_dir, version=VERSION)
    server.log_handler = ring

    # 后台先连一次（连不上也照常起服务，UI 上会显示未连接，可点「重连」）
    def warmup():
        for attempt in range(3):
            try:
                bridge.connect()
                log.info("已连接飞牛 NAS：%s（账号 %s）",
                         config.ws_url, config.nas.get("username"))
                return
            except Exception as exc:                            # noqa: BLE001
                log.warning("第 %d 次连接飞牛失败：%s", attempt + 1, exc)
                time.sleep(5)

    threading.Thread(target=warmup, daemon=True).start()
    log.info("%s v%s 启动，端口 %s", APP_NAME, VERSION,
             port or config.server.get("port"))
    try:
        server.serve_forever(port=port or config.server.get("port"))
    except KeyboardInterrupt:
        log.info("收到退出信号")
    finally:
        bridge.close()
    return 0


def run_selftest(config, bridge):
    """本地自检：不连 NAS，只跑协议层 + 工具清单"""
    from . import tools as tools_mod
    from .protocol import McpServer

    setup_logging(logging.INFO, to_stdout=True)
    app_dir = os.environ.get("TRIM_APPDEST") or \
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tools_mod.set_data_dir(os.path.join(app_dir, "data"))
    server = McpServer(bridge, config, data_dir=os.path.join(app_dir, "data"),
                       version=VERSION)
    init = server.handle({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                          "params": {"protocolVersion": "2025-06-18",
                                     "capabilities": {},
                                     "clientInfo": {"name": "selftest", "version": "0"}}})
    print("initialize ->", json.dumps(init["result"]["serverInfo"], ensure_ascii=False))
    listed = server.handle({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    names = [t["name"] for t in listed["result"]["tools"]]
    print("tools/list -> %d 个：%s" % (len(names), ", ".join(names[:8]) + " ..."))
    print("可用接口：", json.dumps(tools_mod.stats(), ensure_ascii=False))
    search = server.handle({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                            "params": {"name": "fnnas_interfaces_search",
                                       "arguments": {"keyword": "file.ls", "limit": 3}}})
    text = search["result"]["content"][0]["text"]
    print("搜索 file.ls ->", text.replace("\n", " ")[:220])
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(description="飞牛接口 MCP Server")
    parser.add_argument("--stdio", action="store_true", help="stdio 模式（本地 MCP 客户端）")
    parser.add_argument("--http", action="store_true", help="HTTP 模式（NAS 应用/远程客户端）")
    parser.add_argument("--port", type=int, default=None, help="HTTP 端口")
    parser.add_argument("--config", default=None, help="配置文件路径")
    parser.add_argument("--data-dir", default=None, help="data/ 目录（api_spec.json 等）")
    parser.add_argument("--selftest", action="store_true", help="本地自检")
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args(argv)

    from .config import Config
    from .fnnas import FnOsBridge

    config = Config.load(args.config)
    if args.port:
        config.server["port"] = args.port
    app_dir = os.environ.get("TRIM_APPDEST") or \
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if args.data_dir:
        os.environ["FN_MCP_DATA_DIR"] = args.data_dir
    bridge = FnOsBridge(config, app_dir=app_dir)

    level = getattr(logging, str(args.log_level).upper(), logging.INFO)
    setup_logging(level)

    if args.selftest:
        return run_selftest(config, bridge)
    if args.stdio:
        return run_stdio(config, bridge)
    return run_http(config, bridge, port=args.port)


if __name__ == "__main__":
    sys.exit(main())
