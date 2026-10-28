# -*- coding: utf-8 -*-
"""发布前脱敏工具：把仓库里的个人痕迹（凭据 / 内网地址 / 私人文件路径）替换掉。

设计要点
--------
* 本脚本**只含通用规则**（正则），不含任何真实 IP、账号、文件名，可以安全提交。
* 需要按字面量精确替换时，放在同目录的 ``tools/sanitize.local.json``
  （``{"旧串": "新串"}``）；该文件已写进 .gitignore，**不进仓库**。
* 所有规则都**幂等**：跑第二遍不会再改（替换结果不会再被自己的规则命中）。

用法
----
    python tools/sanitize.py --check        # 只报告，不改文件
    python tools/sanitize.py                # 就地脱敏
    python tools/sanitize.py --paths data docs README.md
"""

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEXT_EXTS = {".py", ".md", ".js", ".json", ".html", ".txt", ".css", ".svg",
             ".yaml", ".yml", ".sh", ".cfg", ".ini", ".toml", ".jsx", ".ts"}
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", "node_modules",
             ".idea", "build", "dist", "captures", "web-cache"}
SKIP_FILES = {"sanitize.local.json"}

# ---------------------------------------------------------------- 网络地址

# 私有网段 → 统一换成 192.168.1.0/24（保留最后一段，可读且幂等）
_PRIVATE_IP4 = re.compile(
    r"\b192\.168\.(?!1\.)(\d{1,3})\.(\d{1,3})\b"
    r"|\b10\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})\b"
    r"|\b172\.(?:1[6-9]|2\d|3[01])\.(\d{1,3})\.(\d{1,3})\b"
)

# 公网 IPv4 → 文档保留段 203.0.113.10（只在网络类字段/上下文里替换，避免误伤版本号）
_PUBLIC_IP4_CTX = re.compile(
    r'(?P<pre>ipv4[a-zA-Z]*|ipv4Addr|ip|addr|host|base|url|gateway|dns)'
    r'(?P<sep>["\']?\s*[:=]\s*["\']?)'
    r'(?P<ip>(?!(?:192\.168|10\.|172\.(?:1[6-9]|2\d|3[01])|127\.|0\.|255\.|203\.0\.113\.)'
    r')(?:\d{1,3}\.){3}\d{1,3})(?P<post>["\']?)',
    re.IGNORECASE,
)

# IPv6 全局单播（运营商前缀）→ 文档保留段 2001:db8::/32
_IPV6 = re.compile(r"\b(?:2[0-9a-f]{3}|3[0-9a-f]{3}):[0-9a-f]{1,4}(?::[0-9a-f]{1,4}){2,7}\b", re.I)
_IPV6_RESERVED = re.compile(r"^2001:db8:", re.I)

# MAC 地址：统一成文档用的 00:11:22:33:44:XX（保留末尾一段以便区分多网卡）
_MAC = re.compile(r"\b00:11:22:33:44:(?P<a>[0-9A-Fa-f]{2})\b"
                  r"|\b(?!(?:00:11:22:33:44:))[0-9A-Fa-f]{2}:[0-9A-Fa-f]{2}:"
                  r"(?:[0-9A-Fa-f]{2}:){2}(?P<tail>[0-9A-Fa-f]{2})\b")

# 设备指纹 si / 会话号（13~19 位纯数字串）
_SI = re.compile(r'(?P<pre>\bsi["\']?\s*[:=]\s*["\']?)(?P<val>\d{13,19})(?P<post>["\']?)')

# 临时下载签名 sign=...
_SIGN = re.compile(r"(?P<pre>\bsign=)(?P<val>[A-Za-z0-9+/=]{20,})")

# ---------------------------------------------------------------- 文件路径

# 数据盘路径：/volN/<uid>/a/b/c —— 逐段判断，只把「私人命名」的段换成 sample。
#
# 两种上下文分开处理，否则中文/空格会把路径截断、留下半截私人文件名：
#   1) 引号里的路径（JSON / JS / 转义 JSON / HTML 的 &quot;）：一路吃到收尾引号；
#   2) 正文里的裸路径（Markdown、注释）：吃到空白或中日韩标点为止，宁可少匹配。
_SEG_CHARS_QUOTED = r"[^/\\\n\"']"          # 引号内：允许空格、中文，但不能含分隔符
_SEG_CHARS_BARE = r"[^/\s\"'\\\n<>&`\u3000-\u303f\uff00-\uffef]"

_VOLUME_QUOTED = re.compile(
    r"(?<=[\"';])/?(?P<head>vol(?P<vol>\d+)/(?P<uid>\d+))"
    r"(?P<rest>(?:/" + _SEG_CHARS_QUOTED + r"+)*)"
    r"(?=\\?[\"']|$)"
)
_VOLUME_BARE = re.compile(
    r"(?<![\w\u4e00-\u9fff])/?(?P<head>vol(?P<vol>\d+)/(?P<uid>\d+))"
    r"(?P<rest>(?:/" + _SEG_CHARS_BARE + r"+)*)"
)

# 通用目录名（fnOS 或本仓库文档里到处都有的，保留不影响隐私）
GENERIC_SEGMENTS = {"tmp", "tmp_img", "photo", "video", "document", "music", "code",
                    "backup", "download", "downloads", "book", "books"}
# 抓包时自造的临时目录/文件名（不含任何个人信息）
SAFE_SEGMENTS = {"sub", "out", "dst", "sample", "samples", "test", "tests",
                 "a.jpg", "a.zip", "b.jpg", "b.zip", "arch.zip", "renamed.jpg",
                 "upload.txt", "fresh.txt", "trash-victim.txt", "__not_exist__.bin",
                 ".@#local", "20260127_195353.jpg", "test.txt", "interfaces.html",
                 "fnnas-api"}
_SAFE_SEGMENT_RX = re.compile(r"^(?:fnapi_[A-Za-z0-9_]+|\.@#local)$")


def _is_safe_segment(seg):
    """这个路径段本身不含个人信息（通用目录名 / 抓包自造名 / 格式化占位符）"""
    if "%" in seg or "{" in seg:
        return True
    return seg in GENERIC_SEGMENTS or seg in SAFE_SEGMENTS or bool(_SAFE_SEGMENT_RX.match(seg))


def _map_volume(m):
    rest = (m.group("rest") or "").rstrip()
    if not rest:
        return m.group(0)
    path, sep, query = rest.partition("?")     # 查询串（?t=…&sign=…）单独保留
    segs = path.split("/")[1:]                 # path 以 / 开头，第 0 项是空串
    if not any(segs):
        return m.group(0)
    out = []
    for i, seg in enumerate(segs):
        if not seg or _is_safe_segment(seg):
            out.append(seg)
            continue
        if i == len(segs) - 1:                 # 最后一段可能是文件，保留扩展名
            _stem, ext = os.path.splitext(seg)
            out.append("sample" + ext if re.fullmatch(r"\.[A-Za-z0-9]{1,6}", ext or "") else "sample")
        else:
            out.append("sample")
    return "/%s/%s%s%s" % (m.group("head"), "/".join(out), sep, query)


# 响应样例里的「文件字段」：只处理明确装文件名的键，且只看样例里才出现的形态。
# 注意不能碰 name/title（MCP 工具名、UI 标题、通知标题都叫 name），也不能碰 path
# （WebDAV 等真路径字段），否则会把功能文案改坏。
_Q = r'(?:\\?["\']|&quot;)'          # 引号 token（普通 / 转义 / HTML 实体三种写法）
_FILE_NAME_FIELD = re.compile(
    r"(?P<pre>" + _Q +
    r"(?:fileName|filename|originalName|origName|albumName|photoName|newName)" + _Q +
    r"\s*:\s*" + _Q + r")"
    r"(?P<val>(?:(?!" + _Q + r")[^\\\n\r]){4,120}?)"
    r"(?P<post>" + _Q + r")"
)
_KEEP_NAME_RX = re.compile(
    r"^(?:|sample|samples|test|tests|tmp|sub|out|dst|a\.jpg|a\.zip|b\.jpg|b\.zip|arch\.zip|"
    r"renamed\.jpg|upload\.txt|fresh\.txt|trash-victim\.txt|__not_exist__\.bin|"
    r"20260127_195353\.jpg|fnapi_[A-Za-z0-9_]+|\.@#local|%s|.*%[sd].*)$"
)


def _map_file_name(m):
    val = m.group("val")
    if _KEEP_NAME_RX.match(val) or "/" in val:
        return m.group(0)          # 走 /vol 规则的路径不在这里重复处理
    ext = os.path.splitext(val)[-1]
    if not re.fullmatch(r"\.[A-Za-z0-9]{1,6}", ext or ""):
        ext = ""
    return "%ssample%s%s" % (m.group("pre"), ext, m.group("post"))


# Windows 用户目录（保留路径形式，去掉真实用户名）
_WIN_USER = re.compile(r"(?P<pre>\b[A-Za-z]:[\\/]{1,2}Users[\\/]{1,2})(?P<user>[A-Za-z0-9_.\-]+)",
                       re.IGNORECASE)
_WIN_USER_KEEP = {"user", "username", "yourname", "demo-user", "<user>"}

# ---------------------------------------------------------------- 凭据

# 明文口令 / token 赋值兜底：password 或 secret 键后面直接跟一串真口令
_PASSWORD_ASSIGN = re.compile(
    r"""(?P<pre>\b(?:password|passwd|pwd|passphrase|secret|token|api_key|apikey|newPassword)\b"""
    r"""\s*[:=]\s*(?:['"]|&quot;))(?P<val>[^'"&<>\s]{6,})(?P<post>(?:['"]|&quot;))""",
    re.IGNORECASE,
)
_PASSWORD_PLACEHOLDER = {
    "your-password", "your_password", "password", "passwd", "secret", "token",
    "redacted", "示例密码", "密码", "demo-password", "******", "new-password",
}
# 测试夹具 / 分享提取码一类的明显假值，不该被打码（否则测试会挂）
_FAKE_SECRET = re.compile(r"^(?i:test|demo|live|fake|mock|other|example|sample|dummy|stub)"
                          r"|^\d{1,8}$|^[*x]{3,}$")
# login(账号, 口令) 形式
_LOGIN_CALL = re.compile(r"""(?P<pre>\blogin\(\s*(?:['"])[^'"]*(?:['"])\s*,\s*(?:['"]))"""
                         r"""(?P<val>[^'"]{6,})(?P<post>['"])""")


def _map_private_ip(m):
    if m.group(1):
        return "192.168.1.%s" % m.group(2)
    if m.group(5):
        return "192.168.1.%s" % m.group(5)
    return "192.168.1.%s" % m.group(8)


def _map_public_ip(m):
    return "%s%s203.0.113.10%s" % (m.group("pre"), m.group("sep"), m.group("post"))


def _map_ipv6(m):
    if _IPV6_RESERVED.match(m.group(0)):
        return m.group(0)
    return "2001:db8::1"


def _map_mac(m):
    if m.group("a"):
        return m.group(0)
    return "00:11:22:33:44:%s" % m.group("tail").upper()


def _map_password(m):
    val = m.group("val")
    if val.lower() in _PASSWORD_PLACEHOLDER or _FAKE_SECRET.match(val):
        return m.group(0)
    return "%s***%s" % (m.group("pre"), m.group("post"))


def _map_login(m):
    val = m.group("val")
    if val.lower() in _PASSWORD_PLACEHOLDER or _FAKE_SECRET.match(val):
        return m.group(0)
    return "%s***%s" % (m.group("pre"), m.group("post"))


def _map_win_user(m):
    if m.group("user").lower() in {k.lower() for k in _WIN_USER_KEEP}:
        return m.group(0)
    return "%suser" % m.group("pre")


RULES = [
    ("private-ip", _PRIVATE_IP4, _map_private_ip),
    ("public-ip", _PUBLIC_IP4_CTX, _map_public_ip),
    ("ipv6", _IPV6, _map_ipv6),
    ("mac", _MAC, _map_mac),
    ("si", _SI, lambda m: '%s0%s' % (m.group("pre"), m.group("post"))),
    ("sign", _SIGN, lambda m: "%sREDACTED" % m.group("pre")),
    ("volume-path", _VOLUME_QUOTED, _map_volume),
    ("volume-path", _VOLUME_BARE, _map_volume),
    ("file-name", _FILE_NAME_FIELD, _map_file_name),
    ("password", _PASSWORD_ASSIGN, _map_password),
    ("login-call", _LOGIN_CALL, _map_login),
    ("win-user", _WIN_USER, _map_win_user),
]


def load_local_map(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    # 长串优先，避免短前缀（如 .1）抢先匹配掉长地址（如 .181）
    return sorted(((k, v) for k, v in data.items() if k and not k.startswith("_")),
                  key=lambda kv: -len(kv[0]))


def iter_files(paths):
    for p in paths:
        full = p if os.path.isabs(p) else os.path.join(ROOT, p)
        if os.path.isfile(full):
            if os.path.basename(full) not in SKIP_FILES:
                yield full
            continue
        for base, dirs, files in os.walk(full):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for name in files:
                if name in SKIP_FILES:
                    continue
                if os.path.splitext(name)[1].lower() in TEXT_EXTS:
                    yield os.path.join(base, name)


def sanitize_text(text, local_map):
    hits = []

    def apply(name, rx, repl):
        nonlocal text
        new, n = rx.subn(repl, text)
        if n:
            hits.append((name, n))
            text = new

    for old, new in local_map:
        if old in text:
            hits.append(("local-map", text.count(old)))
            text = text.replace(old, new)
    for name, rx, repl in RULES:
        apply(name, rx, repl)
    return text, hits


def main():
    ap = argparse.ArgumentParser(description="发布前脱敏：去掉凭据 / 内网地址 / 私人路径")
    ap.add_argument("paths", nargs="*", default=["data", "docs", "README.md", "api.md",
                                                "sdk", "mcp", "tools", "tests", "fnnas-api-js",
                                                ".gitignore"],
                    help="要处理的文件或目录（默认仓库里的源码与文档）")
    ap.add_argument("--check", action="store_true", help="只报告差异，不写文件")
    ap.add_argument("--map", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                  "sanitize.local.json"),
                    help="本地精确映射表（默认 tools/sanitize.local.json）")
    ap.add_argument("-v", "--verbose", action="store_true")
    args = ap.parse_args()

    local_map = load_local_map(args.map)
    if args.verbose:
        print("本地映射 %d 条；通用规则 %d 条" % (len(local_map), len(RULES)))

    total_files = changed_files = total_hits = 0
    for path in iter_files(args.paths):
        total_files += 1
        try:
            with open(path, encoding="utf-8", newline="") as f:
                original = f.read()
        except (UnicodeDecodeError, OSError):
            continue
        text, hits = sanitize_text(original, local_map)
        if text == original:
            continue
        changed_files += 1
        total_hits += sum(n for _, n in hits)
        rel = os.path.relpath(path, ROOT)
        detail = ", ".join("%s×%d" % (n, c) for n, c in hits)
        print("%s %s  (%s)" % ("[check]" if args.check else "[fix]  ", rel, detail))
        if not args.check:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(text)

    print("\n共扫描 %d 个文本文件，%s %d 个，替换 %d 处" %
          (total_files, "命中" if args.check else "改写", changed_files, total_hits))
    if args.check and changed_files:
        print("还有未脱敏内容，去掉 --check 再跑一次即可就地修复。")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
