#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 `/p`（相册 / AI 相册应用）的前端产物里提取 **HTTP 接口**。

为什么单独一个工具：
    `tools/scan_web.py` 抓的是 WebSocket 接口名（`appcgi.*` / `file.*` …）。
    但 `/p/` 这个应用**完全不用 WebSocket**，它是一套 REST API（`/api/v1/...`），
    用 RTK Query 定义在前端产物里，形如：

        reducerPath: `albumApi`, baseQuery: s, endpoints: e => ({
            getList:  e.query({query: e => ({url: `/api/v1/album/list`, params: {...}})}),
            create:   e.mutation({query: e => ({url: `/api/v1/album/create`,
                                                method: `post`, body: e})}),
        })

    所以这里按「url + method + 是否有 params/body + 所属 api 分组」把它们挖出来。

鉴权（实测，和 WebSocket 那套不同）：
    baseUrl = `/p`，即真实 URL = `/p` + url；
    签名放在 **`authx`** 头里，签名串是对 `{method, url: "/p"+url, data: body}` 计算，
    密钥是产物里 XOR 混淆的一段字符串（见 `tools/scan_http.py:decode_auth_key()`）。

用法：
    python tools/scan_http.py                          # 用本地缓存提取
    python tools/scan_http.py --force                  # 先重新抓一遍 /p 再提取
    python tools/scan_http.py --probe                  # 顺便用 GET 探活（只读，绝不发 POST）
    python tools/scan_http.py --out data/http_api.json --md docs/api/http.md
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))

DEFAULT_DIRS = [os.path.join(ROOT, "data", "web-cache", "p"),
                os.path.join(ROOT, "data", "web-cache", "assets")]

URL_RE = re.compile(r"url\s*:\s*[`'\"]([^`'\"]+)[`'\"]")
KEY_RE = re.compile(r"([A-Za-z_$][\w$]*)\s*:\s*e\.(query|mutation)\s*\(\s*\{\s*query\s*:")
API_RE = re.compile(r"reducerPath\s*:\s*[`'\"]([A-Za-z0-9_$]+)[`'\"]")
METHOD_RE = re.compile(r"method\s*:\s*[`'\"]([A-Za-z]+)[`'\"]")
FIELD_RE = re.compile(r"\b(params|body|transformResponse|providesTags|invalidatesTags)\s*:")

# 归类：/api/v1/<x>/... 或 /api/v2/<x>/...
GROUP_RE = re.compile(r"^/api/v(\d+)/([^/]+)")

# 用途字典（人工补；没写到的自动从 url 路径猜）
PURPOSE = {
    "album/list": "相册列表（分页/排序）",
    "album/detail": "相册详情",
    "album/create": "创建相册（写）",
    "album/update": "更新相册（写）",
    "album/delete": "删除相册（写）",
    "album/timeline": "相册时间线",
    "album_grant/create": "分享相册给他人（写）",
    "album_grant/update": "更新相册分享授权（写）",
    "album_grant/cancel": "取消相册分享授权（写）",
    "gallery/timeline": "照片时间线（按月/日分桶）",
    "gallery/getList": "照片列表（分页）",
    "explore/geos": "按地理位置探索照片",
    "explore/tags": "按标签探索照片",
    "explore/recent_timeline": "最近照片时间线",
    "photo/upload/path": "取上传路径（v1）",
    "folder_view/getFileList": "文件视图：列文件",
    "folder_view/getFolderList": "文件视图：列文件夹",
    "file/copy": "复制文件/文件夹（写）",
    "file/move": "移动文件/文件夹（写）",
    "video/decode/info": "视频解码信息",
    "video/decode/play": "视频播放地址（写：会创建转码任务）",
    "video/decode/quality": "切换视频清晰度（写）",
    "ai-base/gpus": "AI 相关：GPU 列表",
    "ai-base/gpu": "AI 相关：设置所用 GPU（写）",
    "ai-base/init": "AI 相关：初始化状态",
    "ai-base/setting": "AI 相关：AI 设置",
    "ai-base/check-requirement": "AI 相关：检查运行条件",
    "ai-base/data-vol": "AI 相关：模型数据所在存储空间",
    "ai-base/validate-gpu": "AI 相关：校验 GPU 可用性",
    "ai-face/enabled": "人脸识别：是否启用",
    "ai-face/install": "人脸识别：安装模型（写）",
    "ai-face/uninstall": "人脸识别：卸载模型（写）",
    "ai-face/cancel-install": "人脸识别：取消安装（写）",
    "ai-face/run": "人脸识别：开始识别任务（写）",
    "ai-face/status": "人脸识别：任务状态",
    "ai-face/run-params": "人脸识别：运行参数",
    "ai-face/default-run-params": "人脸识别：默认运行参数",
    "ai-face/install-options": "人脸识别：安装选项",
    "ai-person/list": "人物列表（人脸聚类结果）",
    "ai-person/detail": "人物详情",
    "ai-person/create": "新建人物（写）",
    "ai-person/remove": "删除人物（写）",
    "ai-person/rename": "人物改名（写）",
    "ai-person/mergePeople": "合并人物（写）",
    "ai-person/setVisibility": "人物是否可见（写）",
    "ai-person/addFacesToPerson": "把人脸加入人物（写）",
    "ai-person/removeFacesFromPerson": "从人物移除人脸（写）",
    "ai-person/removePhotosFromPerson": "从人物移除照片（写）",
    "ai-person/transferPhotosFromPerson": "在人物间转移照片（写）",
    "ai-person/separatePhotoFromPerson": "把照片从人物中拆出（写）",
    "ai-person/posterFromPhoto": "设置人物封面（写）",
    "ai-person/personInPhoto": "照片里都有谁",
    "ai-person/getPhotoIds": "按人物取照片 id",
    "ai-person/photoLibrary/list": "人物照片库列表",
    "ai-person/photoLibrary/timeLine": "人物照片时间线",
    "ai-person/searchSimilarFaces": "搜索相似人脸",
    "ai-smart-rec/categories": "智能识别：分类列表",
    "ai-smart-rec/category-enabled": "智能识别：开启/关闭分类（写）",
    "ai-smart-rec/enabled": "智能识别：是否启用",
    "ai-smart-rec/install": "智能识别：安装模型（写）",
    "ai-smart-rec/uninstall": "智能识别：卸载模型（写）",
    "ai-smart-rec/install-options": "智能识别：安装选项",
    "ai-smart-rec/run": "智能识别：开始识别任务（写）",
    "ai-smart-rec/video-enabled": "智能识别：视频识别开关（写）",
    "ai-smart-rec/cancel-install": "智能识别：取消安装（写）",
    "ai-smart-rec/default-run-params": "智能识别：默认运行参数",
    "ai-smart-rec/similarity-enabled": "智能识别：相似照片检测开关（写）",
    "ai-smart-rec/status": "智能识别：任务状态",
    "ai-smart-rec/update-smart-category": "智能识别：更新分类（写）",
    # ---- 相册 ----
    "album/baby/timeline": "宝宝相册时间线",
    "album/normal/timeline": "普通相册时间线",
    "album/item": "相册里的单张照片",
    "album/photo/belong": "某张照片属于哪些相册",
    "album/condition/add": "按条件创建相册（写）",
    "album/download/all": "下载整本相册（写：打包任务）",
    "album_grant/list_mine": "我分享出去的相册",
    "album_grant/list_to_me": "别人分享给我的相册",
    # ---- 照片/搜索/标签 ----
    "gallery/getOne": "单张照片详情",
    "gallery/addTo/album": "把照片加进相册（写）",
    "search/index": "重建搜索索引（写）",
    "search/index/status": "搜索索引状态",
    "thumbnail/refresh": "刷新缩略图（写）",
    "thumbnail/status": "缩略图任务状态",
    "repeat-photo/check": "重复照片检测（写）",
    "repeat-photo/exclude": "重复照片：排除某些（写）",
    "repeat-photo/keep": "重复照片：保留某张（写）",
    "repeat-photo/merge": "重复照片：合并（写）",
    # ---- 预览编辑 ----
    "preview/tag/add": "新建照片标签（写）",
    "preview/tag/addForPhoto": "给照片打标签（写）",
    "preview/tag/delForPhoto": "去掉照片标签（写）",
    "preview/update/dateTime": "修改照片拍摄时间（写）",
    "preview/update/geo": "修改照片地理位置（写）",
    # ---- 回收站 ----
    "recycle-bin/add": "移入回收站（写）",
    "recycle-bin/restore": "从回收站还原（写）",
    "recycle-bin/clean-all": "清空回收站（写，不可恢复）",
    "recycle-bin/timeline": "回收站时间线",
    # ---- 文件夹/文件 ----
    "folder_view/cover": "设置文件夹封面（写）",
    "folder_view/cover/setting": "文件夹封面设置（写）",
    "file/rename": "重命名文件/文件夹（写）",
    "server/file_list": "列文件（POST 形式）",
    "server/folder_manage": "可管理的文件夹列表",
    # ---- 照片文件夹（外接存储/挂载） ----
    "photo/folder/add": "添加照片文件夹（写）",
    "photo/folder/new": "新建照片文件夹（写）",
    "photo/folder/reconnect": "重新连接照片文件夹（写）",
    "photo/folder/defaultInit": "默认照片文件夹初始化",
    "photo/folder/view": "照片文件夹视图",
    # ---- 地图 ----
    "map/timeLine": "地图模式时间线",
    "map/preview/initCenter": "地图初始中心点",
    "map/preview/mapBoundary": "地图可视范围边界",
    # ---- 任务面板 / 维护 / 修复 ----
    "task-panel/fail": "失败任务列表",
    "task-panel/retry-one": "重试单个任务（写）",
    "task-panel/skip-one": "跳过单个任务（写）",
    "maintain/task/": "维护任务（按 taskType 拼路径，写）",
    "fixer/photoType": "修复照片类型识别（写）",
    "fixer/photoType/status": "照片类型修复进度",
    # ---- 系统 / 服务 / 用户 ----
    "server/sys_info": "系统信息",
    "server/architecture": "设备架构",
    "server/users_all": "全部用户",
    "server/user_group_all": "全部用户组",
    "user/info": "当前用户信息",
    "user_photo/stat": "照片统计（数量/占用）",
    "sys_config/setting": "系统设置写入（写）",
    "sys_config/time_zone/support": "支持的时区列表",
    "sys_config/video_decode": "视频解码配置",
    "sys_config/video_decode/list_gpu": "可用于解码的 GPU 列表",
    "app/version": "应用版本",
    # ---- 其它 ----
    "google_takeout/prepare": "Google Takeout 导入：准备（写）",
    "google_takeout/heartbeat": "Google Takeout 导入：心跳",
    "google_takeout/notice": "Google Takeout 导入：进度通知",
    "share_link/cleanupInvalid": "清理失效的分享链接（写）",
    "share_link/new": "新建分享链接（写）",
}


# --------------------------------------------------------------------- 提取
def find_enclosing_object(text, pos, max_back=400):
    """从 url: 的位置向前找到所属的对象起点 `({`，返回 (start, end)"""
    start = text.rfind("({", max(0, pos - max_back), pos)
    if start < 0:
        start = text.rfind("{", max(0, pos - max_back), pos)
    if start < 0:
        return None
    depth = 0
    for i in range(start, min(len(text), pos + 500)):
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return start, i + 1
    return start, min(len(text), pos + 500)


def extract_file(text, asset):
    """从一个 js 产物里提取 RTK Query 的 HTTP 接口定义"""
    out = []
    api = None
    api_matches = list(API_RE.finditer(text))
    for m in URL_RE.finditer(text):
        url = m.group(1)
        if not url.startswith("/api/"):
            continue
        span = find_enclosing_object(text, m.start())
        if not span:
            continue
        start, end = span
        obj = text[start:end]
        # 所属 api 分组：向前找最近的 reducerPath
        prev = [x for x in api_matches if x.start() < m.start()]
        if prev:
            api = prev[-1].group(1)
        method = "GET"
        mm = METHOD_RE.search(obj)
        if mm:
            method = mm.group(1).upper()
        fields = sorted({f.group(1) for f in FIELD_RE.finditer(obj)})
        # RTK 端点名：向对象头前面找 `key: e.query({query:`
        head_start = max(0, start - 200)
        key_match = None
        for km in KEY_RE.finditer(text, head_start, end):
            if km.start() > m.start():
                break
            key_match = km
        name = key_match.group(1) if key_match else ""
        kind = key_match.group(2) if key_match else ""
        out.append({"api": api or "", "name": name, "kind": kind, "url": url,
                    "method": method, "fields": fields, "asset": asset})
    return out


def load_assets(dirs):
    files = []
    for d in dirs:
        if not os.path.isdir(d):
            continue
        for base, _dirs, names in os.walk(d):
            for n in names:
                if n.endswith((".js", ".mjs")):
                    files.append(os.path.join(base, n))
    return files


def collect(paths):
    found = {}
    for path in paths:
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                text = f.read()
        except OSError:
            continue
        asset = os.path.basename(path)
        for item in extract_file(text, asset):
            key = (item["url"], item["method"])
            old = found.get(key)
            if old is None:
                found[key] = item
            else:                     # 同一个 url 出现多次（封装的 v1/v2）：合并信息来源
                for f in item["fields"]:
                    if f not in old["fields"]:
                        old["fields"].append(f)
                if not old["name"] and item["name"]:
                    old["name"] = item["name"]
    return found


def group_of(url):
    m = GROUP_RE.match(url)
    if m:
        return "v%s/%s" % (m.group(1), m.group(2))
    return url.strip("/").split("/")[0]


def purpose_of(url):
    tail = url.split("/api/v", 1)[-1]
    tail = tail.split("/", 1)[-1] if "/" in tail else tail
    for key, text in PURPOSE.items():
        if tail.startswith(key) or key.startswith(tail):
            return text
    verb = {"list": "列表", "detail": "详情", "create": "新建", "update": "更新",
            "delete": "删除", "remove": "删除", "get": "查询", "set": "设置",
            "run": "执行", "install": "安装", "uninstall": "卸载", "cancel": "取消"}
    last = tail.split("/")[-1]
    return verb.get(last, "") or ("接口 " + tail)


# ----------------------------------------------------------- 鉴权密钥（解码）
def decode_auth_key(js_dir=None):
    """
    产物里把签名密钥 XOR 了一下：

        _s = (() => {
            let e = new Uint8Array([...]);
            let t = new Uint8Array(36);
            for (let n = 0; n < 36; n++) t[n] = e[n] ^ 119;
            return new TextDecoder('utf-8').decode(t);
        })();

    这里照着解出来。
    """
    js_dir = js_dir or os.path.join(ROOT, "data", "web-cache", "p", "assets")
    pattern = re.compile(
        r"new Uint8Array\(\[([\d,\s]+)\]\)[\s\S]{0,200}?for\s*\(\s*let\s+\w+\s*=\s*0;\s*\w+\s*<\s*(\d+);"
        r"[\s\S]{0,120}?(\w+)\[\w+\]\s*=\s*\w+\[\w+\]\s*\^\s*(\d+)")
    for base, _dirs, names in os.walk(js_dir):
        for n in names:
            if not n.endswith(".js"):
                continue
            text = open(os.path.join(base, n), encoding="utf-8", errors="replace").read()
            m = pattern.search(text)
            if not m:
                continue
            nums = [int(x) for x in m.group(1).replace(" ", "").split(",") if x]
            size = int(m.group(2))
            xor = int(m.group(4))
            key = bytes(b ^ xor for b in nums[:size]).decode("utf-8", "replace")
            return key, os.path.basename(os.path.join(base, n))
    return None, None


# ----------------------------------------------------------------- 鉴权
def make_authx(method, url, params=None, body=None, key=None, nonce=None, stamp=None):
    """
    按前端 at() 的算法生成 authx 头（md5 + 固定 APPKEY + 解码后的参数串）。

    nonce / stamp 可以不传（正常调用），测试时传固定值就能比对签名。
    """
    import hashlib
    import random

    appkey = "NDzZTVxnRKP8Z0jXg1VAMonaG8akvh"
    key = key or decode_auth_key()[0] or ""

    def md5(text):
        return hashlib.md5(text.encode("utf-8")).hexdigest()

    path = url.partition("?")[0]
    if method.upper() == "GET":
        merged = {k: v for k, v in (params or {}).items() if v is not None}
        # 前端 nt() 会按 key 排序（Object.keys.sort()），签名必须一致
        raw = urllib.parse.urlencode(sorted(merged.items()),
                                     quote_via=urllib.parse.quote).replace("+", "%20")
    else:
        raw = json.dumps(body, separators=(",", ":")) if body is not None else ""
    inner = md5(urllib.parse.unquote(raw))
    nonce = str(nonce) if nonce is not None else str(random.randint(100000, 999999))
    stamp = str(stamp) if stamp is not None else str(int(time.time() * 1000))
    sign = md5("_".join([appkey, path, nonce, stamp, inner, key]))
    return "nonce=%s&timestamp=%s&sign=%s" % (nonce, stamp, sign)


def ws_token(username, password, url="ws://192.168.1.10:5666/websocket?type=main"):
    """用 WebSocket 登录拿 token —— /p 的 HTTP API 要把它放进 fnos-token cookie"""
    import asyncio

    sys.path.insert(0, ROOT)
    from sdk import FnOsClient

    async def _login():
        client = FnOsClient(ping_interval=60)
        client.logger.setLevel(50)
        await client.connect(url)
        ok = await client.login(username, password)
        token = client.token if ok else None
        await client.close()
        return token

    return asyncio.run(_login())


def http_call(base, rec, token, params=None, body=None, timeout=15):
    """/p/api 一次调用：cookie fnos-token + authx 签名，响应 {code, msg, data}

    注意：POST 的签名覆盖的是**实际发出去的 JSON body**，签名和发包必须是同一份数据，
    否则服务端回 `code 5000 invalid sign`。
    """
    url = base + "/p" + rec["url"]
    method = rec["method"]
    query = ("?" + urllib.parse.urlencode(params)) if params else ""
    payload = body if body is not None else ({} if method != "GET" else None)
    headers = {"User-Agent": "Mozilla/5.0",
               "Cookie": "fnos-token=" + token,
               "authx": make_authx(method, "/p" + rec["url"],
                                   params=params, body=payload)}
    data = None
    if method != "GET":
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload, separators=(",", ":")).encode()
    request = urllib.request.Request(url + query, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as r:
            text = r.read()
            code = r.status
    except urllib.error.HTTPError as exc:
        text = exc.read()
        code = exc.code
    except Exception as exc:                                        # pragma: no cover
        return {"http": None, "error": "%s: %s" % (type(exc).__name__, exc)}
    payload = None
    try:
        payload = json.loads(text.decode("utf-8", "replace"))
    except Exception:
        pass
    return {"http": code, "payload": payload,
            "text": text[:600].decode("utf-8", "replace")}


def record_probe(rec, result, sent_params=None, sent_body=None):
    """
    把一次实测结果写进接口记录。

    sent_params / sent_body 是**实际发出去**的参数：调用成功（code 0）时把它们记下来，
    并补进 `params_keys`（实测参数比从 JS 里挖出来的更可靠）。
    """
    payload = result.get("payload")
    code = payload.get("code") if isinstance(payload, dict) else None
    if isinstance(payload, dict):
        rec["probe_code"] = code
        rec["probe_msg"] = (payload.get("msg") or "")[:120]
        data = payload.get("data")
        rec["probe_keys"] = sorted(data) if isinstance(data, dict) else (
            "array[%d]" % len(data) if isinstance(data, list) else type(data).__name__)
        sample = json.dumps(data, ensure_ascii=False)
        rec["probe_sample"] = sample[:400]
        ok = code == 0
        rec["probe"] = ("HTTP %s / code 0" % result.get("http")) if ok else (
            "HTTP %s / code %s %s" % (result.get("http"), code,
                                      rec["probe_msg"]))
    else:
        ok = False
        rec["probe"] = "HTTP %s" % result.get("http") if result.get("http") else (
            result.get("error") or "失败")
    if ok:
        if sent_params:
            rec["probe_params"] = sent_params
        if sent_body:
            rec["probe_body"] = sent_body
        used = list((sent_body or {}).keys()) or list((sent_params or {}).keys())
        if used:
            rec["params_keys"] = list(dict.fromkeys((rec.get("params_keys") or []) + used))
    return rec


# ----------------------------------------------------------------- 探活
def probe_authed(records, base, token, only=None, skip_writes=True):
    """
    带登录态探活：cookie `fnos-token` + `authx` 签名。

    默认只发 GET（只读原则）；写接口跳过，除非在 `WRITE_TESTS` 白名单里
    （可逆场景：建相册→删相册、建标签→删标签）。
    """
    for rec in records:
        if only and only not in rec["url"]:
            continue
        if rec["method"] != "GET" and rec["url"] not in WRITE_TESTS:
            rec["probe"] = "未实测（写接口；默认不自动发，避免改数据）"
            continue
        params = None
        if rec["method"] == "GET" and any(k in rec["url"] for k in ("list", "timeline")):
            params = {"offset": 0, "limit": 10}
        result = http_call(base, rec, token, params=params)
        record_probe(rec, result)
        print("  %-6s %-46s %-30s %s" % (rec["method"], rec["url"],
                                         rec["probe"][:30], (rec.get("probe_sample") or "")[:60]))
    return records


# 可逆的写接口测试白名单（默认不自动发写请求，只有显式 --probe-writes 才动这些）
WRITE_TESTS = {
    "/api/v1/album/create",
    "/api/v1/album/remove",
    "/api/v1/album/delete",
    "/api/v1/preview/tag/add",
}


def probe(records, base, cookie=None, timeout=8):
    """
    未鉴权的探活（旧行为）：只发 GET，记录 HTTP 状态码。

    实测结论：`/p/api/*` 这层网关要求 cookie `fnos-token` + `authx` 签名，
    没有登录态一律 401（响应体为空）：401 = 路由存在、只是没鉴权；
    404/501 = 后端没这个路由。带登录态的真探活用 `probe_authed()`。
    """
    for rec in records:
        if rec["method"] != "GET":
            rec["probe"] = "跳过（写接口，不发请求）"
            continue
        url = base + "/p" + rec["url"]
        headers = {"User-Agent": "Mozilla/5.0"}
        if cookie:
            headers["Cookie"] = cookie
        try:
            with urllib.request.urlopen(
                    urllib.request.Request(url, headers=headers), timeout=timeout) as r:
                rec["probe"] = "HTTP %s" % r.status
                rec["probe_sample"] = r.read()[:200].decode("utf-8", "replace")
        except urllib.error.HTTPError as exc:
            body = exc.read()[:200].decode("utf-8", "replace")
            if exc.code == 401 and not cookie:
                rec["probe"] = "HTTP 401（路由存在，需要浏览器会话 cookie）"
            else:
                rec["probe"] = "HTTP %s" % exc.code
            rec["probe_sample"] = body
        except Exception as exc:                                    # pragma: no cover
            rec["probe"] = "失败：%s" % type(exc).__name__
    return records


# ------------------------------------------------------------------ 输出
def write_json(path, records, meta):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                   "meta": meta, "endpoints": records}, f, ensure_ascii=False, indent=2)


def param_text(rec):
    """表格里「参数/请求体」一列：优先用挖出来的字段名，否则显示定义里的字段标记"""
    keys = rec.get("params_keys") or []
    loose = rec.get("params_keys_loose") or []
    if keys:
        return ", ".join(keys)
    if loose:
        return ", ".join(loose[:8]) + " ?"
    fields = rec.get("fields") or []
    return ", ".join(fields) if fields else "-"


def write_md(path, records, meta):
    groups = {}
    for r in records:
        groups.setdefault(group_of(r["url"]), []).append(r)
    probed = [r for r in records if r.get("probe")]
    lines = [
        "# `/p`（相册 / AI 相册）HTTP 接口",
        "",
        "> 自动生成：`python tools/scan_http.py --probe`。数据源 `%s`，共 **%d** 个 HTTP 接口。"
        % (meta.get("source"), len(records)),
        "",
        "`/p` 是飞牛的**相册 / AI 相册**应用（照片时间线、相册、人物、智能识别、地图、回收站、"
        "预览、上传…）。它**不用 WebSocket**，全部走 REST，所以没有 `appcgi.*` 那套 req 名。",
        "",
        "> 顺带验证过：用 `tools/scan_web.py --entry /p/` 扫它的 WebSocket 接口，"
        "1331 个候选里 `endpoint` 档为 **0**（全是日期格式串、编解码器串、i18n 文案键），"
        "说明这个应用确实一个 WS 接口都没有、全部走下面的 HTTP。",
        "",
        "## 怎么发请求",
        "",
        "```",
        "请求地址 = %s/p + 下表路径        # 例如 %s/p/api/v1/album/list"
        % (meta.get("base"), meta.get("base")),
        "响应外壳 = {code, data, msg}     # code == 0 才算成功",
        "```",
        "",
        "鉴权（反编译前端产物 + 真机实测确认）：",
        "",
        "```",
        "请求头 Cookie : fnos-token=<WebSocket 登录拿到的 token>",
        "请求头 authx  : nonce=<6位随机>&timestamp=<13位毫秒>&sign=<md5>",
        "sign = md5( APPKEY + \"_\" + /p路径 + \"_\" + nonce + \"_\" + timestamp + \"_\"",
        "           + md5(反编码后的参数串) + \"_\" + 应用密钥 )",
        "APPKEY  = NDzZTVxnRKP8Z0jXg1VAMonaG8akvh              # 硬编码在产物里",
        "应用密钥 = %s   # 产物里 XOR 混淆，tools/scan_http.py:decode_auth_key() 可解"
        % (meta.get("auth_key") or "（未解出）"),
        "```",
        "",
        "两个坑（都实测过）：",
        "",
        "1. **只带 token 不带 authx** → `{\"code\":5000,\"msg\":\"invalid sign\"}`；"
        "**只带 authx 不带 token** → HTTP 401（响应体为空）。两个都要带。",
        "2. 签名必须和实际发出去的数据一致：GET 的参数**按 key 排序**拼成 "
        "`k=v&k=v` 再解码后算 md5；POST 算的是 `JSON.stringify(body)`。"
        "差一个空格/顺序就是 5000。",
        "",
        "`fnos-token` 就是 WS 登录返回的 `token`（前端 `ro.set('fnos-token', token)` 写进 cookie），"
        "所以 `tools/probe_http.py` 直接 WS 登录后用这个 token 就能调通，不用去浏览器里抄 Cookie。",
        "",
        "> 封装好的客户端：`sdk/http_photo.py` 的 `PhotoHttpClient`（`albums()` / `album_create()` / "
        "`photos()` …）；相册接口的功能与用法、数据模型、完整流程见 "
        "[../modules/album.md](../modules/album.md)，实测取样例脚本 `tools/probe_album.py`。",
        "",
        "## 分组",
        "",
        "| 分组 | 接口数 |",
        "|------|-------|",
    ]
    for g in sorted(groups):
        lines.append("| `%s` | %d |" % (g, len(groups[g])))
    if probed:
        lines += ["", "探活：共 %d 个 GET 接口，其中 %d 个返回 HTTP 401（路由存在、鉴权未过）。"
                  % (len(probed), sum(1 for r in probed if "401" in (r.get("probe") or "")))]
    if meta.get("probed_at"):
        gets = [r for r in records if r["method"] == "GET"]
        ok = sum(1 for r in gets if r.get("probe_code") == 0)
        writes = [r for r in records if r["method"] != "GET"]
        tested = [r for r in writes if (r.get("probe") or "").startswith("HTTP")]
        lines += ["", "## 真机实测结果（账号 `%s`，%s）" % (meta.get("probe_account") or "-",
                                                          meta.get("probed_at")),
                  "",
                  "- **GET %d 个：%d 个成功（`code 0`）**，%d 个失败/需特定参数（见下表「实测」列）"
                  % (len(gets), ok, len(gets) - ok),
                  "- 写接口 %d 个：**只实测了 %d 个可逆场景**（建相册 → 查详情/时间线 → 改名 → "
                  "加照片 → 移出 → 删相册，最后核对相册列表已清空）；其余写接口涉及删除/清空/"
                  "人物合并等，默认不发请求，避免改数据"
                  % (len(writes), len(tested)),
                  "- 失败原因主要是缺必填参数（`code 400 invalid params`）或资源不存在，"
                  "不代表接口有问题"]
    if meta.get("param_extracted_at"):
        lines += ["", "> 「参数/请求体（挖到的字段）」一列来自 `tools/extract_write_params.py`："
                  "顺着 RTK Query 的 hook 别名链（hook 变量 → 导出名 → 导入别名 → 调用点）"
                  "找到前端实际传的参数对象，取顶层字段名。带 `?` 的是宽松匹配（可能混入同名函数的"
                  "噪声，仅供参考）；空白表示参数由变量传入、没解析出来。"]
    for g in sorted(groups):
        lines += ["", "## %s（%d）" % (g, len(groups[g])), "",
                  "| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |",
                  "|--------|------|------|------------------------|------|------|"]
        for r in sorted(groups[g], key=lambda x: x["url"]):
            kind = "（mutation）" if r["kind"] == "mutation" else ""
            lines.append("| `%s`%s | %s | `%s` | %s | %s | %s |" % (
                r["name"] or "-", kind, r["method"], r["url"], param_text(r),
                purpose_of(r["url"]), r.get("probe") or "-"))
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main():
    ap = argparse.ArgumentParser(description="提取 /p 应用的 HTTP 接口")
    ap.add_argument("--dirs", nargs="*", default=DEFAULT_DIRS, help="前端产物目录")
    ap.add_argument("--out", default=os.path.join(ROOT, "data", "http_api.json"))
    ap.add_argument("--md", default=os.path.join(ROOT, "docs", "api", "http.md"))
    ap.add_argument("--base", default="http://192.168.1.10:5666")
    ap.add_argument("--force", action="store_true", help="先重新抓一遍 /p 前端产物")
    ap.add_argument("--probe", action="store_true", help="用 GET 探活（只读，绝不发写请求）")
    ap.add_argument("--cookie", default=os.environ.get("FN_HTTP_COOKIE", ""),
                    help="浏览器会话 Cookie（探活 /p/api 需要；也可用环境变量 FN_HTTP_COOKIE）")
    ap.add_argument("--render-only", action="store_true",
                    help="不重新提取，只按现有 data/http_api.json 重渲染 md"
                         "（extract_write_params.py 补完字段后用）")
    ap.add_argument("--login", action="store_true",
                    help="先 WebSocket 登录拿 token，再用 cookie fnos-token + authx 真探活")
    ap.add_argument("--username", default=os.environ.get("fn_username", ""))
    ap.add_argument("--password", default=os.environ.get("fn_password", ""))
    ap.add_argument("--ws", default=os.environ.get(
        "FNNAS_WS", "ws://192.168.1.10:5666/websocket?type=main"))
    ap.add_argument("--only", default=None, help="只探活 url 含该子串的接口")
    args = ap.parse_args()

    if args.render_only:
        with open(args.out, encoding="utf-8") as f:
            doc = json.load(f)
        write_md(args.md, doc["endpoints"], doc.get("meta") or {})
        print("已按 %s 重渲染 %s" % (os.path.relpath(args.out, ROOT),
                                     os.path.relpath(args.md, ROOT)))
        return 0

    if args.force:
        os.system('%s "%s" --base %s --entry /p/ --force '
                  '--out %s --md %s' % (
                      sys.executable, os.path.join(ROOT, "tools", "scan_web.py"),
                      args.base, os.path.join(ROOT, "data", "reqs_p.json"),
                      os.path.join(ROOT, "data", "reqs_p.md")))

    files = load_assets(args.dirs)
    print("扫描 %d 个前端产物 ..." % len(files))
    found = collect(files)
    records = sorted(found.values(), key=lambda x: (group_of(x["url"]), x["url"]))
    print("提取到 %d 个 HTTP 接口（去重后）" % len(records))

    key, key_file = decode_auth_key(os.path.join(ROOT, "data", "web-cache", "p", "assets"))
    if key:
        print("鉴权密钥（XOR 解码自 %s）：%s" % (key_file, key))
    else:
        print("没能解出 authx 密钥（产物结构可能变了）")

    token = None
    if args.login:
        print("WebSocket 登录 %s@%s 拿 fnos-token ..." % (args.username, args.base))
        token = ws_token(args.username, args.password, args.ws)
        if not token:
            print("登录失败，无法带登录态探活")
            return 2
        print("  拿到 token（%d 字符）" % len(token))

    if args.probe or args.login:
        if token:
            print("带登录态探活（cookie fnos-token + authx；写接口默认不发）...")
            probe_authed(records, args.base, token, only=args.only)
        else:
            print("无登录态探活（预期 401，用来判断路由是否存在）...")
            probe(records, args.base, cookie=args.cookie or None)
        ok = sum(1 for r in records if (r.get("probe") or "").endswith("code 0"))
        print("  code 0（成功）：%d 个；有响应的：%d 个"
              % (ok, sum(1 for r in records if (r.get("probe") or "").startswith("HTTP"))))

    meta = {"source": ", ".join(os.path.relpath(d, ROOT) for d in args.dirs),
            "base": args.base, "auth_header": "authx", "auth_key": key,
            "auth_key_file": key_file,
            "auth_cookie": "fnos-token",
            "note": "真实地址 = base + /p + 路径；请求头 authx + Cookie: fnos-token=<WS登录token>"}
    write_json(args.out, records, meta)
    write_md(args.md, records, meta)
    groups = {}
    for r in records:
        groups[group_of(r["url"])] = groups.get(group_of(r["url"]), 0) + 1
    print("分组：")
    for g in sorted(groups, key=lambda x: -groups[x]):
        print("   %-24s %d" % (g, groups[g]))
    print("写入 %s / %s" % (os.path.relpath(args.out, ROOT), os.path.relpath(args.md, ROOT)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
