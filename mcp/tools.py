# -*- coding: utf-8 -*-
"""
MCP 工具注册表。

原则：
    - 只把**真机实测可用**的接口做成「精选工具」（`verified=True`），避免模型踩坑；
    - 另外给 3 个通用工具，覆盖全部 476 个 WebSocket 接口 + 151 个 /p HTTP 接口；
    - 每个工具都是 (bridge, args) -> JSON 可序列化结果，异常统一由协议层转成 isError。
"""

import json
import os

# ---------------------------------------------------------------- 元数据加载
_INTERFACES = None
_HTTP_INTERFACES = None
_DATA_DIR = None

# 实测状态里这些算「接口存在/可用」
_AVAILABLE_STATUS = {"succ", "param_error", "error"}


def set_data_dir(path):
    global _DATA_DIR, _INTERFACES, _HTTP_INTERFACES
    _DATA_DIR = path
    _INTERFACES = None
    _HTTP_INTERFACES = None


def _data_dir():
    if _DATA_DIR:
        return _DATA_DIR
    if os.environ.get("FN_MCP_DATA_DIR"):
        return os.environ["FN_MCP_DATA_DIR"]
    return os.path.join(os.environ.get("TRIM_APPDEST") or _default_app_dir(), "data")


def _default_app_dir():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_interfaces():
    """476 个 WebSocket 接口 + 实测状态 + 中文用途"""
    global _INTERFACES
    if _INTERFACES is not None:
        return _INTERFACES
    data_dir = _data_dir()
    spec_path = os.path.join(data_dir, "api_spec.json")
    meta_path = os.path.join(data_dir, "interfaces_meta.json")
    probe_path = os.path.join(data_dir, "probe_status.json")
    spec = {}
    if os.path.exists(spec_path):
        with open(spec_path, encoding="utf-8") as f:
            spec = json.load(f).get("spec") or {}
    meta = {}
    if os.path.exists(meta_path):
        with open(meta_path, encoding="utf-8") as f:
            meta = json.load(f)
    probe = {}
    if os.path.exists(probe_path):
        with open(probe_path, encoding="utf-8") as f:
            probe = (json.load(f).get("results") or {})
    items = []
    for req, info in spec.items():
        p = probe.get(req) or {}
        status = p.get("status") or "unverified"
        items.append({
            "req": req,
            "group": info.get("group") or req.split(".")[0],
            "method": info.get("method") or "",
            "readonly": bool(info.get("readonly")),
            "status": status,
            "available": status in _AVAILABLE_STATUS,
            "verified": status == "succ",
            "params": info.get("params") or "",
            "keys": p.get("resp_keys") or [],
            "sample": (p.get("sample") or "")[:600],
            "purpose": (meta.get(req) or {}).get("purpose") or "",
            "protocol": "ws",
        })
    items.sort(key=lambda x: (x["group"], x["req"]))
    _INTERFACES = items
    return items


def load_http_interfaces():
    """151 个 /p（相册应用）HTTP 接口 + 实测结果"""
    global _HTTP_INTERFACES
    if _HTTP_INTERFACES is not None:
        return _HTTP_INTERFACES
    path = os.path.join(_data_dir(), "http_api.json")
    items = []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            doc = json.load(f)
        for e in doc.get("endpoints") or []:
            code = e.get("probe_code")
            items.append({
                "req": ("%s %s" % (e.get("method"), e.get("url"))).strip(),
                "method": e.get("method"),
                "url": e.get("url"),
                "group": (e.get("url") or "").rsplit("/", 1)[0].split("/v1/")[-1].split("/v2/")[-1],
                "params": ", ".join(e.get("params_keys") or []) or "",
                "probe": e.get("probe") or "",
                "code": code,
                "available": code == 0,
                "verified": code == 0,
                "keys": e.get("probe_keys") or [],
                "purpose": e.get("purpose") or "",
                "protocol": "http",
            })
    _HTTP_INTERFACES = items
    return items


def menu_entries():
    """UI 用的可用接口清单（WS + HTTP 合并）"""
    out = []
    for it in load_interfaces():
        out.append({
            "protocol": "ws", "name": it["req"], "group": it["group"],
            "method": it["method"], "readonly": it["readonly"],
            "status": it["status"], "available": it["available"],
            "verified": it["verified"], "params": it["params"],
            "keys": it["keys"][:12], "purpose": it["purpose"],
        })
    for it in load_http_interfaces():
        out.append({
            "protocol": "http", "name": it["req"], "group": it["group"],
            "method": it["method"], "readonly": it["method"] == "GET",
            "status": "succ" if it["verified"] else ("probe:" + str(it["code"])),
            "available": it["available"], "verified": it["verified"],
            "params": it["params"], "keys": it["keys"][:12],
            "purpose": it["purpose"], "url": it["url"],
        })
    return out


# ---------------------------------------------------------------- 工具定义
TOOLS = []


def tool(name, title, description, schema=None, verified=True):
    def wrapper(fn):
        TOOLS.append({
            "name": name,
            "title": title,
            "description": description,
            "inputSchema": schema or {"type": "object", "properties": {},
                                      "required": []},
            "verified": verified,
            "handler": fn,
        })
        return fn
    return wrapper


def _obj(**props):
    # 注意：默认值是 False —— 只有显式标了 _required=True 的才算必填
    required = [k for k, v in props.items() if v.pop("_required", False)]
    return {"type": "object", "properties": props, "required": required}


def _s(desc, required=True, enum=None):
    d = {"type": "string", "description": desc}
    if enum:
        d["enum"] = enum
    if required:
        d["_required"] = True
    return d


def _i(desc, required=True):
    d = {"type": "integer", "description": desc}
    if required:
        d["_required"] = True
    return d


def _b(desc, required=False):
    d = {"type": "boolean", "description": desc}
    if required:
        d["_required"] = True
    return d


def _a(desc, required=True):
    d = {"type": "array", "items": {"type": "string"}, "description": desc}
    if required:
        d["_required"] = True
    return d


# ---------------------------------------------------------------- 系统 / 存储
@tool("fnnas_system_info", "系统信息",
      "飞牛 NAS 的硬件/系统信息（型号、CPU、内存、系统版本等）。已实测可用。")
def _(bridge, args):
    return bridge.call_data("appcgi.sysinfo.getHardwareInfo")


@tool("fnnas_system_uptime", "开机时长", "开机运行时长与当前系统时间。已实测可用。")
def _(bridge, args):
    return bridge.call_data("appcgi.sysinfo.getUptime")


@tool("fnnas_system_hostname", "主机名", "读取 NAS 主机名。已实测可用。")
def _(bridge, args):
    return bridge.call_data("appcgi.sysinfo.getHostName")


@tool("fnnas_cpu_usage", "CPU 占用", "当前 CPU 使用率 / 各核心占用。已实测可用。")
def _(bridge, args):
    return bridge.call_data("appcgi.resmon.cpu")


@tool("fnnas_disk_usage", "磁盘 IO", "磁盘读写速率与占用。已实测可用。")
def _(bridge, args):
    return bridge.call_data("appcgi.resmon.disk")


@tool("fnnas_storage_disks", "硬盘列表", "所有物理硬盘（型号、容量、SMART 概要、状态）。已实测可用。")
def _(bridge, args):
    return bridge.call_data("stor.listDisk", key="disk")


@tool("fnnas_storage_spaces", "存储空间", "存储池/存储空间（容量、可用空间、RAID 类型）。已实测可用。")
def _(bridge, args):
    return bridge.call_data("stor.listStor", key="array")


@tool("fnnas_network_interfaces", "网卡列表", "网卡与 IP 地址列表。已实测可用。")
def _(bridge, args):
    return bridge.call_data("appcgi.netsvr.getNetworkCardList")


@tool("fnnas_notifications", "通知列表",
      "系统通知列表（分页）。已实测可用。",
      _obj(page=_i("页码，从 1 开始", required=False),
           size=_i("每页条数", required=False)))
def _(bridge, args):
    page = int(args.get("page") or 1)
    size = int(args.get("size") or 20)
    return bridge.call_data("notify.list", {"page": page, "size": size})


@tool("fnnas_notify_unread", "未读通知数", "未读通知数量。已实测可用。")
def _(bridge, args):
    return bridge.call_data("notify.unreadTotal", key="unreadTotal")


@tool("fnnas_user_info", "当前用户", "当前登录账号信息（uid、是否管理员、用户组）。已实测可用。")
def _(bridge, args):
    return bridge.call_data("user.info", key="userInfo")


@tool("fnnas_users", "用户列表", "NAS 上的所有用户。已实测可用。")
def _(bridge, args):
    return bridge.call_data("user.list", key="users")


# ---------------------------------------------------------------- 文件
@tool("fnnas_file_ls", "列目录",
      "列出目录内容（文件/文件夹、大小、修改时间）。路径可写 /vol1/1000/sample 或 /vol1/1000/sample。已实测可用。",
      _obj(path=_s("目录路径，例如 /vol1/1000")))
def _(bridge, args):
    return bridge.call_data("file.ls", {"path": args["path"]}, key="files")


@tool("fnnas_file_prop", "文件属性",
      "批量查询文件/目录属性（是否存在、大小、修改时间、权限）。已实测可用。",
      _obj(paths=_a("要查询的路径数组")))
def _(bridge, args):
    return bridge.call_data("file.prop", {"files": args["paths"]}, key="prop")


@tool("fnnas_file_size", "路径占用",
      "目录/文件的递归大小与文件数量统计。已实测可用。",
      _obj(path=_s("目录或文件路径")))
def _(bridge, args):
    return bridge.call_data("file.size", {"file": args["path"]}, key="size")


@tool("fnnas_file_download_link", "下载直链",
      "生成文件的临时下载地址（带签名，可直接用 HTTP GET 下载）。已实测可用。",
      _obj(path=_s("文件路径")))
def _(bridge, args):
    items = bridge.call_data("file.download", {"files": [args["path"]]}, key="download")
    base = bridge.config.http_base
    for item in items or []:
        uri = item.get("uri") or ""
        if uri.startswith("/"):
            item["url"] = base + uri
    return items


@tool("fnnas_file_mkdir", "新建文件夹",
      "创建目录。已实测可用。",
      _obj(path=_s("要创建的目录路径")))
def _(bridge, args):
    return bridge.call_data("file.mkdir", {"path": args["path"]})


@tool("fnnas_file_rename", "重命名",
      "重命名文件/目录（同目录内改名，同步接口）。已实测可用。",
      _obj(path=_s("原路径"), new_name=_s("新名字（不含路径）")))
def _(bridge, args):
    return bridge.call_data("file.rename", {"path": args["path"],
                                            "newName": args["new_name"]})


@tool("fnnas_file_copy", "复制",
      "批量复制文件到目标**目录**（异步任务，工具会等任务结束）。已实测可用。",
      _obj(files=_a("要复制的文件路径数组"),
           dest_dir=_s("目标目录"),
           overwrite=_b("同名是否覆盖")))
def _(bridge, args):
    files = args["files"]
    details = {"name": os.path.basename(files[0].rstrip("/")), "count": len(files)}
    return bridge.task_call("file.cp", {
        "files": files, "pathTo": args["dest_dir"],
        "overwrite": 1 if args.get("overwrite") else 0, "details": details})


@tool("fnnas_file_move", "移动",
      "批量移动文件到目标**目录**（异步任务，工具会等任务结束）。已实测可用。",
      _obj(files=_a("要移动的文件路径数组"),
           dest_dir=_s("目标目录"),
           overwrite=_b("同名是否覆盖")))
def _(bridge, args):
    files = args["files"]
    details = {"name": os.path.basename(files[0].rstrip("/")), "count": len(files)}
    return bridge.task_call("file.mv", {
        "files": files, "pathTo": args["dest_dir"],
        "overwrite": 1 if args.get("overwrite") else 0, "details": details})


@tool("fnnas_file_delete", "删除",
      "删除文件/目录（默认进回收站，可 recover=True 直接删）。异步任务。已实测可用。",
      _obj(paths=_a("要删除的路径数组"),
           direct=_b("True=不进回收站，直接删掉")))
def _(bridge, args):
    paths = args["paths"]
    details = {"name": os.path.basename(paths[0].rstrip("/")), "count": len(paths)}
    return bridge.task_call("file.rm", {
        "files": paths,
        "moveToTrashbin": not bool(args.get("direct")),
        "details": details})


@tool("fnnas_file_compress", "压缩",
      "把文件/目录打成 zip（异步任务）。已实测可用。",
      _obj(files=_a("要压缩的路径数组"),
           dest=_s("压缩包完整路径，例如 /vol1/1000/a.zip")))
def _(bridge, args):
    files = args["files"]
    return bridge.task_call("file.compress", {
        "description": "MCP 压缩", "path": args["dest"], "files": files, "level": 0,
        "details": {"name": os.path.basename(args["dest"]), "count": len(files)}})


@tool("fnnas_file_extract", "解压",
      "解压压缩包到目录（异步任务）。已实测可用。",
      _obj(archive=_s("压缩包路径"), dest_dir=_s("解压到哪个目录")))
def _(bridge, args):
    return bridge.task_call("file.extract", {
        "description": "MCP 解压", "path": args["dest_dir"], "file": args["archive"],
        "overwrite": 1,
        "details": {"name": os.path.basename(args["archive"]), "count": 1}})


@tool("fnnas_trash_list", "回收站列表", "列出回收站内容。已实测可用。")
def _(bridge, args):
    return bridge.call_data("file.trash.list", key="files")


# ---------------------------------------------------------------- 分享
@tool("fnnas_share_link_create", "创建分享链接",
      "给文件/目录创建公开分享链接（可选密码、有效期）。已实测可用。",
      _obj(path=_s("要分享的文件/目录路径，例如 /vol1/1000/tmp/a.jpg"),
           password=_s("访问密码（4 位，可选）", required=False),
           valid_hours=_i("有效期小时数（可选，默认 168 小时=7 天）", required=False)))
def _(bridge, args):
    params = {"data": {"filePath": args["path"], "shareName": "mcp-share"}}
    if args.get("password"):
        params["data"]["passwd"] = args["password"]
    if args.get("valid_hours"):
        params["data"]["validTo"] = int(args["valid_hours"])
    data = bridge.call_data("appcgi.sharesvr.share.link.create", params, nested=False)
    share_id = data.get("id")
    return {"share": data, "url": "%s/s/%s" % (bridge.config.http_base, share_id)}


@tool("fnnas_share_link_list", "分享链接列表", "当前所有分享链接。已实测可用。")
def _(bridge, args):
    return bridge.call_data("appcgi.sharesvr.share.link.list", {"data": {}},
                            key="data")


@tool("fnnas_share_link_remove", "删除分享链接",
      "按分享 id 删除分享链接。已实测可用。",
      _obj(share_id=_s("分享 id（share.link.list 里的 id）")))
def _(bridge, args):
    return bridge.call_data("appcgi.sharesvr.share.link.remove",
                            {"data": {"id": args["share_id"]}})


# ---------------------------------------------------------------- 相册（HTTP /p）
@tool("fnnas_photo_albums", "相册列表", "相册应用的相册列表（含照片数、封面）。已实测可用。")
def _(bridge, args):
    return bridge.http_call("GET", "/api/v1/album/list",
                            params={"sort_by": "createTime",
                                    "sort_direction": "desc",
                                    "offset": 0, "limit": 200}).get("data")


@tool("fnnas_photo_album_create", "新建相册", "创建相册。已实测可用。",
      _obj(name=_s("相册名")))
def _(bridge, args):
    return bridge.http_call("POST", "/api/v1/album/create",
                            body={"album_name": args["name"], "ids": []}).get("data")


@tool("fnnas_photo_album_add", "照片加相册",
      "把照片加入相册。已实测可用。",
      _obj(album_id=_i("相册 id（创建相册返回的 albumId）"),
           photo_ids=_a("照片 id 数组（gallery/getList 里的 id）")))
def _(bridge, args):
    return bridge.http_call("POST", "/api/v1/gallery/addTo/album",
                            body={"ids": args["photo_ids"],
                                  "album_id": args["album_id"]}).get("data")


@tool("fnnas_photo_album_delete", "删除相册", "删除相册（相册里的照片不会被删）。已实测可用。",
      _obj(album_id=_i("相册 id")))
def _(bridge, args):
    return bridge.http_call("POST", "/api/v1/album/delete",
                            body={"album_id": args["album_id"]}).get("data")


@tool("fnnas_photo_timeline", "照片时间线",
      "照片按年月日的时间线桶（先查桶，再用 fnnas_photo_list 按天取照片）。已实测可用。")
def _(bridge, args):
    return bridge.http_call("GET", "/api/v1/gallery/timeline").get("data")


@tool("fnnas_photo_list", "照片列表",
      "某时间段的照片列表。注意 start_time/end_time 必须是 `YYYY:MM:DD HH:mm:ss`（冒号日期）。已实测可用。",
      _obj(start_time=_s("开始时间，例如 2026:10:04 00:00:00"),
           end_time=_s("结束时间，例如 2026:10:04 23:59:59"),
           offset=_i("偏移", required=False),
           limit=_i("条数", required=False)))
def _(bridge, args):
    return bridge.http_call("GET", "/api/v1/gallery/getList", params={
        "start_time": args["start_time"], "end_time": args["end_time"],
        "offset": int(args.get("offset") or 0),
        "limit": int(args.get("limit") or 50),
        "mode": "datetime"}).get("data")


@tool("fnnas_photo_detail", "照片详情", "单张照片/视频详情。已实测可用。",
      _obj(photo_id=_i("照片 id")))
def _(bridge, args):
    return bridge.http_call("GET", "/api/v1/gallery/getOne",
                            params={"id": args["photo_id"]}).get("data")


@tool("fnnas_photo_stat", "相册统计", "照片/视频总数与占用。已实测可用。")
def _(bridge, args):
    return bridge.http_call("GET", "/api/v1/user_photo/stat").get("data")


# ---------------------------------------------------------------- 通用
@tool("fnnas_interfaces_search", "搜索接口",
      "在 476 个 WebSocket 接口里搜索（按 req 名 / 分组 / 中文用途）。返回是否实测可用。",
      _obj(keyword=_s("关键词，例如 file / 分享 / stor.list", required=False),
           only_available=_b("只看实测可用（默认 true）"),
           limit=_i("返回条数（默认 20）", required=False)))
def _(bridge, args):
    keyword = (args.get("keyword") or "").lower()
    only = args.get("only_available", True)
    limit = int(args.get("limit") or 20)
    out = []
    for it in load_interfaces():
        if only and not it["available"]:
            continue
        if keyword and keyword not in (it["req"] + " " + it["group"] + " " +
                                       it["purpose"] + " " + it["method"]).lower():
            continue
        out.append({k: it[k] for k in ("req", "group", "status", "readonly",
                                       "available", "params", "keys", "purpose")})
        if len(out) >= limit:
            break
    return {"total": len(out), "interfaces": out}


@tool("fnnas_interface_call", "调用任意接口",
      "直接调一个 WebSocket 接口（req 名用 fnnas_interfaces_search 查）。"
      "注意：appcgi.sharesvr.* 这类接口参数要包在 data 里，其余平铺；写接口只回 ack。",
      _obj(req=_s("接口名，例如 file.ls"),
           params={"type": "object", "description": "参数对象（可选）",
                   "additionalProperties": True},
           nested=_b("参数是否包在 data 里（appcgi.sharesvr.* 需要 true）"),
           wait_task=_b("写接口是否等异步任务结果")))
def _(bridge, args):
    if args.get("wait_task"):
        return bridge.task_call(args["req"], args.get("params") or {})
    return bridge.call(args["req"], args.get("params") or {},
                       nested=bool(args.get("nested")))


@tool("fnnas_http_interfaces_search", "搜索 HTTP 接口",
      "在 151 个 /p 相册应用 HTTP 接口里搜索。返回路径、方法、参数与实测状态。",
      _obj(keyword=_s("关键词，例如 album / photo", required=False),
           only_available=_b("只看实测可用（默认 true）"),
           limit=_i("返回条数（默认 20）", required=False)))
def _(bridge, args):
    keyword = (args.get("keyword") or "").lower()
    only = args.get("only_available", True)
    limit = int(args.get("limit") or 20)
    out = []
    for it in load_http_interfaces():
        if only and not it["available"]:
            continue
        if keyword and keyword not in (it["req"] + " " + (it["purpose"] or "")).lower():
            continue
        out.append({k: it[k] for k in ("req", "method", "url", "params",
                                       "probe", "available", "purpose")})
        if len(out) >= limit:
            break
    return {"total": len(out), "interfaces": out}


@tool("fnnas_http_api_call", "调用 HTTP 接口",
      "调 /p 相册应用的 HTTP 接口（自带 cookie fnos-token + authx 签名）。"
      "path 用 fnnas_http_interfaces_search 查到的 url，例如 /api/v1/album/list。",
      _obj(path=_s("接口路径，例如 /api/v1/album/list"),
           method=_s("GET / POST", enum=["GET", "POST"], required=False),
           params={"type": "object", "description": "GET 查询参数（可选）",
                   "additionalProperties": True},
           body={"type": "object", "description": "POST 请求体（可选）",
                 "additionalProperties": True}))
def _(bridge, args):
    return bridge.http_call(args.get("method") or "GET", args["path"],
                            params=args.get("params"), body=args.get("body"))


# ---------------------------------------------------------------- 导出
def tool_definitions(include_unverified=False):
    """给 MCP tools/list 用：去掉 handler，只留协议字段"""
    defs = []
    for t in TOOLS:
        if not include_unverified and not t["verified"]:
            continue
        defs.append({
            "name": t["name"],
            "title": t["title"],
            "description": t["description"],
            "inputSchema": t["inputSchema"],
        })
    return defs


def find_tool(name):
    for t in TOOLS:
        if t["name"] == name:
            return t
    return None


def stats():
    interfaces = load_interfaces()
    http = load_http_interfaces()
    return {
        "ws_total": len(interfaces),
        "ws_available": sum(1 for i in interfaces if i["available"]),
        "ws_verified": sum(1 for i in interfaces if i["verified"]),
        "http_total": len(http),
        "http_available": sum(1 for i in http if i["available"]),
        "tools": len(TOOLS),
    }
