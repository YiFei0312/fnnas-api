#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 MCP Server 打成飞牛 fnOS 应用包（.fpk）。

做的事：
    1. 生成/校验图标（ICON.PNG、ICON_256.PNG、app/ui/images/icon_{64,256}.png）
    2. 组装应用工程目录：manifest / config / cmd / app/{mcp,sdk,lib,data,webui,ui}
    3. 生成 data/interfaces_meta.json（接口中文用途，来自 tools/api_doc_meta.py）
    4. 把纯 Python 依赖（websockets / watchdog）和 Linux 版 pycryptodome 一起塞进 app/lib
    5. 调 fnpack build 产出 dist/fnnas-mcp.fpk

用法：
    python tools/build_nas_app.py                 # 组装 + 打包
    python tools/build_nas_app.py --no-pack       # 只组装，不调 fnpack
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

BUILD = os.path.join(ROOT, "build", "fnnas-mcp-app")
DIST = os.path.join(ROOT, "dist")
VENDOR = os.path.join(ROOT, "build", "vendor")
WHEELS = os.path.join(ROOT, "build", "wheels")
FNPACK = os.path.join(ROOT, "tools", "fnos", "fnpack.exe" if os.name == "nt" else "fnpack")

APPNAME = "fnnas-mcp"
VERSION = "1.0.0"      # 可用 --version 覆盖；改了内容一定记得升版本（appcenter 按 名-版本 缓存解析结果）
DISPLAY_NAME = "飞牛接口 MCP Server"
DESC = ("把飞牛 NAS 的 476 个 WebSocket 接口和 151 个相册 HTTP 接口封装成 MCP Server，"
        "带接口文档与两种 MCP 传输开关（Streamable HTTP / HTTP+SSE），仅供本机使用。")

MANIFEST = """appname               = {appname}
version               = {version}
display_name          = {display_name}
desc                  = {desc}
platform              = x86
source                = thirdparty
maintainer            = fnnas-api
maintainer_url        = https://github.com/fnnas/fnnas-api
distributor           = fnnas-api
os_min_version        = 1.2.0
desktop_uidir         = ui
desktop_applaunchname = {appname}.Application
service_port          = {port}
checkport             = true
ctl_stop              = true
disable_authorization_path = true
changelog             = 首个版本：接口文档 + 两种 MCP 传输 + 可用接口清单
"""

UI_CONFIG = """{{
  ".url": {{
    "{appname}.Application": {{
      "title": "{display_name}",
      "icon": "images/icon_{{0}}.png",
      "type": "iframe",
      "protocol": "http",
      "port": "{port}",
      "url": "/",
      "allUsers": true
    }}
  }}
}}
"""

PRIVILEGE = """{
  "defaults": {
    "run-as": "package"
  },
  "username": "fnnas-mcp",
  "groupname": "fnnas-mcp"
}
"""

RESOURCE = "{}\n"

MAIN_SCRIPT = r"""#!/bin/bash
# 飞牛接口 MCP Server 生命周期脚本：start / stop / status

APP_NAME="fnnas-mcp"
PORT=__PORT__
LOG_FILE="${TRIM_PKGVAR}/info.log"
PID_FILE="${TRIM_PKGVAR}/app.pid"
CONFIG_FILE="${TRIM_PKGETC}/config.json"
APP_DIR="${TRIM_APPDEST}"

mkdir -p "${TRIM_PKGVAR}" 2>/dev/null

log_msg() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "${LOG_FILE}"
}

check_process() {
    local pid=$1
    [ -n "${pid}" ] && kill -0 "${pid}" 2>/dev/null
}

status() {
    if [ -f "${PID_FILE}" ]; then
        local pid
        pid=$(head -n 1 "${PID_FILE}" | tr -d '[:space:]')
        if check_process "${pid}"; then
            return 0
        fi
        rm -f "${PID_FILE}"
    fi
    return 1
}

start_process() {
    if status; then
        log_msg "already running"
        return 0
    fi
    if ! command -v python3 >/dev/null 2>&1; then
        echo "这台设备没有 python3，无法启动 ${APP_NAME}" > "${TRIM_TEMP_LOGFILE:-/dev/null}"
        log_msg "python3 not found"
        return 1
    fi
    log_msg "starting ${APP_NAME} on port ${PORT}"
    cd "${APP_DIR}" || return 1
    FN_MCP_CONFIG="${CONFIG_FILE}" \
    FN_MCP_APP_DIR="${APP_DIR}" \
    PYTHONPATH="${APP_DIR}:${APP_DIR}/lib" \
    PYTHONUNBUFFERED=1 \
    nohup python3 -u -m mcp.server --http --port "${PORT}" \
        --config "${CONFIG_FILE}" >> "${LOG_FILE}" 2>&1 &
    echo $! > "${PID_FILE}"
    sleep 2
    if status; then
        log_msg "started, pid=$(cat ${PID_FILE})"
        return 0
    fi
    log_msg "failed to start"
    return 1
}

stop_process() {
    log_msg "stopping ${APP_NAME}"
    if [ -f "${PID_FILE}" ]; then
        local pid
        pid=$(head -n 1 "${PID_FILE}" | tr -d '[:space:]')
        if check_process "${pid}"; then
            kill -TERM "${pid}" 2>/dev/null
            local i=0
            while check_process "${pid}" && [ $i -lt 10 ]; do
                sleep 1
                i=$((i + 1))
            done
            if check_process "${pid}"; then
                kill -KILL "${pid}" 2>/dev/null
            fi
        fi
        rm -f "${PID_FILE}"
    fi
    # 兜底：按命令行匹配（防止 pid 文件丢失）
    pkill -f "mcp.server --http --port ${PORT}" 2>/dev/null
    return 0
}

case "$1" in
    start)
        start_process
        ;;
    stop)
        stop_process
        ;;
    status)
        if status; then exit 0; else exit 3; fi
        ;;
    *)
        echo "usage: $0 {start|stop|status}"
        exit 1
        ;;
esac
"""

INSTALL_INIT = """#!/bin/bash
# 安装前检查：确认系统有 python3
if ! command -v python3 >/dev/null 2>&1; then
    echo "本应用需要系统自带 python3，当前设备未找到。" > "${TRIM_TEMP_LOGFILE:-/dev/null}"
    exit 1
fi
exit 0
"""

INSTALL_CALLBACK = r"""#!/bin/bash
# 安装后：写入默认配置（已存在就不覆盖，升级时保留用户配置）
CONFIG_FILE="${TRIM_PKGETC}/config.json"
DEFAULT_CONFIG="${TRIM_APPDEST}/default_config.json"
mkdir -p "${TRIM_PKGETC}" 2>/dev/null
if [ ! -f "${CONFIG_FILE}" ] && [ -f "${DEFAULT_CONFIG}" ]; then
    cp "${DEFAULT_CONFIG}" "${CONFIG_FILE}"
    chmod 600 "${CONFIG_FILE}" 2>/dev/null
fi
echo "fnnas-mcp 已安装，配置：${CONFIG_FILE}" >> "${TRIM_PKGVAR}/info.log" 2>/dev/null
exit 0
"""

UNINSTALL_CALLBACK = """#!/bin/bash
# 卸载后：无需额外清理（应用数据中心由系统回收）
exit 0
"""

CONFIG_CALLBACK = """#!/bin/bash
# 设置变更后重启服务，让新的配置生效（例如用户在应用设置里改了账号）
APP_DIR="${TRIM_APPDEST}"
if [ -x "${APP_DIR}/cmd/main" ]; then
    "${APP_DIR}/cmd/main" stop >/dev/null 2>&1
    "${APP_DIR}/cmd/main" start >/dev/null 2>&1
fi
exit 0
"""


def log(msg):
    print("[build] %s" % msg)


def make_icons(target_dir, ui_images_dir):
    """用 Pillow 画一个简单的 MCP 图标：渐变圆角方块 + 两个 M 形的链接符号"""
    from PIL import Image, ImageDraw

    def draw(size):
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw_ctx = ImageDraw.Draw(img)
        radius = max(6, int(size * 0.22))
        # 渐变背景
        grad = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(grad)
        for y in range(size):
            t = y / max(1, size - 1)
            color = (int(59 + (139 - 59) * t), int(130 + (92 - 130) * t),
                     int(246 + (246 - 246) * t), 255)
            gdraw.line([(0, y), (size, y)], fill=color)
        mask = Image.new("L", (size, size), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, size - 1, size - 1],
                                              radius=radius, fill=255)
        img.paste(grad, (0, 0), mask)
        # 两个交错的"链接"符号
        width = max(2, size // 16)
        pad = size * 0.26
        draw_ctx.line([pad, size * 0.36, size - pad, size * 0.36],
                      fill=(255, 255, 255, 255), width=width, joint="curve")
        draw_ctx.line([size - pad, size * 0.64, pad, size * 0.64],
                      fill=(255, 255, 255, 210), width=width, joint="curve")
        draw_ctx.ellipse([pad - width, size * 0.36 - width,
                          pad + width, size * 0.36 + width],
                         fill=(255, 255, 255, 255))
        return img

    os.makedirs(ui_images_dir, exist_ok=True)
    draw(256).save(os.path.join(target_dir, "ICON_256.PNG"))
    draw(256).save(os.path.join(target_dir, "ICON.PNG"))
    draw(64).save(os.path.join(ui_images_dir, "icon_64.png"))
    draw(256).save(os.path.join(ui_images_dir, "icon_256.png"))
    log("图标已生成")


def copy_tree(src, dst, ignore=None):
    if not os.path.isdir(src):
        return 0
    count = 0
    for base, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in ("__pycache__",)]
        rel = os.path.relpath(base, src)
        target = os.path.join(dst, rel) if rel != "." else dst
        os.makedirs(target, exist_ok=True)
        for name in files:
            if ignore and ignore(name, rel):
                continue
            if name.endswith((".pyc", ".pyo")):
                continue
            shutil.copy2(os.path.join(base, name), os.path.join(target, name))
            count += 1
    return count


def extract_wheel(wheel_path, target_dir):
    """把 wheel 解压到目标目录（跳过 dist-info / 脚本）"""
    if not os.path.exists(wheel_path):
        log("!! 缺少 %s" % wheel_path)
        return 0
    count = 0
    with zipfile.ZipFile(wheel_path) as zf:
        for info in zf.infolist():
            name = info.filename
            if name.endswith("/") or ".dist-info/" in name or ".data/" in name:
                continue
            if name.startswith(("bin/", "scripts/")):
                continue
            target = os.path.join(target_dir, name)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with zf.open(info) as src, open(target, "wb") as dst:
                shutil.copyfileobj(src, dst)
            count += 1
    return count


def write_text(path, text, mode=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    if mode:
        os.chmod(path, mode)


# 打包时脱敏用的替换表（顺序重要：先长后短）
SANITIZE_MAP = [
    ("demoNAS", "demoNAS"),
    ("example.com", "example.com"),
    ("demo-user", "demo-user"),
    ("192.168.1.10", "192.168.1.10"),
    ("192.168.1.11", "192.168.1.11"),
]

SANITIZE_EXTS = (".json", ".html", ".js", ".css", ".py", ".md", ".txt", ".svg")
SANITIZE_SKIP_DIRS = ("lib",)


def sanitize_package_text(app_dir):
    """
    把安装包里的个人痕迹清掉：账号名、主机名、内网 IP、密码。

    只在**打包产物**里替换，仓库里的实测数据（data/*.json）保持原样，
    方便自己复查真机结果。
    """
    changed = []
    for base, dirs, files in os.walk(app_dir):
        dirs[:] = [d for d in dirs
                   if d not in SANITIZE_SKIP_DIRS and d != "__pycache__"]
        for name in files:
            if not name.endswith(SANITIZE_EXTS):
                continue
            path = os.path.join(base, name)
            try:
                with open(path, encoding="utf-8") as f:
                    text = f.read()
            except (UnicodeDecodeError, OSError):
                continue
            original = text
            for old, new in SANITIZE_MAP:
                if old in text:
                    text = text.replace(old, new)
            # 内网 IP 段统一替换（样例报文里会出现网关、另一块网卡等不同地址）
            text = re.sub(r"192\.168\.88\.(\d{1,3})", r"192.168.1.\1", text)
            # 兜底：形如 password/密码 后面跟字符串的，一律打码
            text = re.sub(r'("password"\s*:\s*")[^"]+(")', r"\1REDACTED\2", text)
            if text != original:
                with open(path, "w", encoding="utf-8", newline="\n") as f:
                    f.write(text)
                changed.append(os.path.relpath(path, app_dir))
    if changed:
        log("已脱敏 %d 个文件（账号/主机名/内网 IP）" % len(changed))
    return changed


def default_config(port=8686, username="", password=""):
    """
    应用首次启动用的默认配置。

    **不包含账号密码**（除非显式传参）：飞牛相关凭据由用户在应用界面
    「飞牛连接配置」里填写，保存后写到 ${TRIM_PKGETC}/config.json（权限 600）。
    """
    return {
        "nas": {"host": "127.0.0.1", "port": 5666,
                "username": username or "", "password": password or "",
                "base_url": ""},
        "server": {"port": port,
                   "mcp": {"enabled": True, "path": "/mcp"},
                   "sse": {"enabled": True, "path": "/sse"},
                   "tools": {"include_unverified": False}},
        "ui": {"title": DISPLAY_NAME},
    }


def build_interfaces_meta(out_path):
    """接口中文用途（来自 tools/api_doc_meta.py 的 PURPOSE 表）"""
    import api_doc_meta

    spec_path = os.path.join(ROOT, "data", "api_spec.json")
    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f).get("spec") or {}
    meta = {}
    for req in spec:
        purpose = (getattr(api_doc_meta, "PURPOSE", {}) or {}).get(req)
        if purpose:
            meta[req] = {"purpose": purpose}
    write_text(out_path, json.dumps(meta, ensure_ascii=False, indent=1))
    log("interfaces_meta.json：%d 个接口有中文用途" % len(meta))


def build(default_port=8686, pack=True, password="", username=""):
    log("组装应用工程 -> %s" % BUILD)
    if os.path.isdir(BUILD):
        shutil.rmtree(BUILD)
    os.makedirs(BUILD)

    # 1) manifest / config / cmd
    write_text(os.path.join(BUILD, "manifest"),
               MANIFEST.format(appname=APPNAME, version=VERSION,
                              display_name=DISPLAY_NAME, desc=DESC, port=default_port))
    write_text(os.path.join(BUILD, "config", "privilege"), PRIVILEGE)
    write_text(os.path.join(BUILD, "config", "resource"), RESOURCE)

    cmd = os.path.join(BUILD, "cmd")
    os.makedirs(cmd, exist_ok=True)
    write_text(os.path.join(cmd, "main"), MAIN_SCRIPT.replace("__PORT__", str(default_port)), 0o755)
    for name, body in (("install_init", INSTALL_INIT),
                       ("install_callback", INSTALL_CALLBACK),
                       ("uninstall_init", "#!/bin/bash\nexit 0\n"),
                       ("uninstall_callback", UNINSTALL_CALLBACK),
                       ("upgrade_init", "#!/bin/bash\nexit 0\n"),
                       ("upgrade_callback", INSTALL_CALLBACK),
                       ("config_init", "#!/bin/bash\nexit 0\n"),
                       ("config_callback", CONFIG_CALLBACK)):
        write_text(os.path.join(cmd, name), body, 0o755)

    # 2) app/ui（桌面入口）+ 图标
    app_dir = os.path.join(BUILD, "app")
    ui_dir = os.path.join(app_dir, "ui")
    write_text(os.path.join(ui_dir, "config"),
               UI_CONFIG.format(appname=APPNAME, display_name=DISPLAY_NAME,
                                port=default_port))
    make_icons(BUILD, os.path.join(ui_dir, "images"))

    # 3) MCP server 代码 + Web UI
    def _skip_webui(name, rel):
        return rel.startswith("webui")

    n = copy_tree(os.path.join(ROOT, "mcp"), os.path.join(app_dir, "mcp"),
                  ignore=_skip_webui)
    log("server 代码：%d 个文件" % n)
    n = copy_tree(os.path.join(ROOT, "mcp", "webui"), os.path.join(app_dir, "webui"))
    log("Web UI：%d 个文件" % n)

    # 4) SDK（Python 包，MCP 通过它连飞牛）
    n = copy_tree(os.path.join(ROOT, "sdk"), os.path.join(app_dir, "sdk"))
    log("SDK：%d 个文件" % n)

    # 5) 依赖：纯 Python websockets（vendor 目录）+ pycryptodome / watchdog（wheel 解压）
    lib_dir = os.path.join(app_dir, "lib")
    os.makedirs(lib_dir, exist_ok=True)
    if os.path.isdir(VENDOR):
        for name in ("websockets", "watchdog"):
            src = os.path.join(VENDOR, name)
            if os.path.isdir(src):
                n = copy_tree(src, os.path.join(lib_dir, name))
                log("依赖 %s：%d 个文件（vendor）" % (name, n))
    if os.path.isdir(WHEELS):
        extracted = set()
        for wheel in sorted(os.listdir(WHEELS)):
            if not wheel.endswith(".whl"):
                continue
            pkg = wheel.split("-")[0]
            # websockets 优先用 vendor 里的纯 Python 版本；pycryptodome / watchdog 从 wheel 解
            if pkg in ("websockets",) or pkg in extracted:
                continue
            n = extract_wheel(os.path.join(WHEELS, wheel), lib_dir)
            extracted.add(pkg)
            log("依赖 %s：%d 个文件（wheel %s）" % (pkg, n, wheel))
    # watchdog 是纯 Python 包，如果只有 wheel 没 vendor，也要解出来
    if "watchdog" not in os.listdir(lib_dir) and os.path.isdir(WHEELS):
        for wheel in sorted(os.listdir(WHEELS)):
            if wheel.startswith("watchdog") and wheel.endswith(".whl"):
                n = extract_wheel(os.path.join(WHEELS, wheel), lib_dir)
                log("依赖 watchdog：%d 个文件（兜底）" % n)
                break

    # 6) 接口数据 + 文档
    data_dir = os.path.join(app_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    for name in ("api_spec.json", "probe_status.json"):
        src = os.path.join(ROOT, "data", name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(data_dir, name))
    # http_api.json 拷贝时把「用途」写进去（render 时才计算，存下来 UI 才能显示）
    http_src = os.path.join(ROOT, "data", "http_api.json")
    if os.path.exists(http_src):
        import scan_http as scan
        with open(http_src, encoding="utf-8") as f:
            doc = json.load(f)
        for endpoint in doc.get("endpoints") or []:
            if not endpoint.get("purpose"):
                try:
                    endpoint["purpose"] = scan.purpose_of(endpoint.get("url") or "") or ""
                except Exception:
                    endpoint["purpose"] = ""
        with open(os.path.join(data_dir, "http_api.json"), "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=1)
        log("http_api.json：%d 个接口带用途" % sum(
            1 for e in doc.get("endpoints") or [] if e.get("purpose")))
    docs_html = os.path.join(ROOT, "docs", "api", "interfaces.html")
    if os.path.exists(docs_html):
        shutil.copy2(docs_html, os.path.join(data_dir, "interfaces.html"))
        log("接口文档：%.1f MB" % (os.path.getsize(docs_html) / 1024 / 1024))
    build_interfaces_meta(os.path.join(data_dir, "interfaces_meta.json"))

    # 6.5) 版本号文件（server.py 启动时读它，保证界面显示的版本和 manifest 一致）
    write_text(os.path.join(app_dir, "VERSION"), VERSION + "\n")

    # 7) 默认配置（安装后拷到 etc/config.json）
    write_text(os.path.join(app_dir, "default_config.json"),
               json.dumps(default_config(default_port, username, password),
                          ensure_ascii=False, indent=2))

    sanitize_package_text(app_dir)

    size = sum(os.path.getsize(os.path.join(b, f))
               for b, _d, fs in os.walk(app_dir) for f in fs)
    log("工程大小：%.1f MB" % (size / 1024 / 1024))

    if not pack:
        return BUILD
    return pack_fpk()


def pack_fpk():
    os.makedirs(DIST, exist_ok=True)
    if not os.path.exists(FNPACK):
        raise SystemExit("找不到 fnpack：%s（见 docs/nasapp.md 下载）" % FNPACK)
    log("调用 fnpack build …")
    result = subprocess.run([FNPACK, "build"], cwd=BUILD,
                            capture_output=True, text=True)
    out = (result.stdout or "") + (result.stderr or "")
    print("\n".join(line for line in out.splitlines() if line.strip()))
    produced = os.path.join(BUILD, APPNAME + ".fpk")
    if not os.path.exists(produced):
        raise SystemExit("fnpack 没有产出 fpk")
    target = os.path.join(DIST, "%s-%s.fpk" % (APPNAME, VERSION))
    shutil.move(produced, target)
    log("产物：%s（%.1f MB）" % (target, os.path.getsize(target) / 1024 / 1024))
    return target


def main():
    parser = argparse.ArgumentParser(description="打包飞牛 fnOS 应用")
    parser.add_argument("--port", type=int, default=8686)
    parser.add_argument("--version", default=None, help="应用版本号（改内容时务必升版本）")
    parser.add_argument("--no-pack", action="store_true")
    parser.add_argument("--username", default="",
                        help="可选：预置 NAS 账号（不传则装完在界面里填）")
    parser.add_argument("--password", default="",
                        help="可选：预置 NAS 密码（不传则装完在界面里填）")
    args = parser.parse_args()
    global VERSION
    if args.version:
        VERSION = args.version
    build(default_port=args.port, pack=not args.no_pack,
          username=args.username, password=args.password)
    return 0


if __name__ == "__main__":
    sys.exit(main())
