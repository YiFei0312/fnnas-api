#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
`/p`（相册应用）HTTP 接口的**带登录态实测**工具。

鉴权（反编译前端 + 实测确认，和 WebSocket 那套完全不同）：

    请求头  Cookie: fnos-token=<WebSocket 登录返回的 token>
    请求头  authx: nonce=<6位>&timestamp=<13位毫秒>&sign=<md5>
            sign = md5(APPKEY_/p路径_nonce_timestamp_md5(反编码参数串)_应用密钥)

    - `fnos-token` 是 Web UI 登录后写进浏览器的 cookie（前端 `ro.set('fnos-token', token)`）；
    - 只带 token 不带 authx，或只带 authx 不带 token，都会被拒：
      缺 authx -> `{"code":5000,"msg":"invalid sign"}`；缺 token -> HTTP 401。

本工具做三件事：
    1. WebSocket 登录拿 token；
    2. 把接口清单里的 **GET 接口全部实测一遍**（带真实参数：先从列表接口里取 album_id /
       photo_id / person_id / share_id，再回填给需要 id 的接口）；
    3. 跑一组**可逆的写接口**场景（建相册 → 改名 → 加照片 → 移出 → 删相册），
       每步都验证，最后清理干净；破坏性接口（clean-all / delete / remove person …）不碰。

结果写回 `data/http_api.json`（`probe_*` 字段），再：
    python tools/scan_http.py --render-only && python tools/gen_html.py

用法：
    set fn_username=demo-user & set fn_password=...
    python tools/probe_http.py                 # 全部 GET + 可逆写场景
    python tools/probe_http.py --only gallery  # 只测含 gallery 的
    python tools/probe_http.py --no-writes     # 只测 GET
"""

import argparse
import json
import os
import sys
import time
import urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import scan_http as S                                                # noqa: E402

HTTP_JSON = os.path.join(ROOT, "data", "http_api.json")


class Ctx:
    """实测过程中攒下来的真实 id，给需要参数的接口回填"""

    def __init__(self):
        self.album_id = None
        self.photo_id = None
        self.person_id = None
        self.share_id = None
        self.task_type = None
        self.folder_path = None
        self.date_start = None       # 相册时间线参数用 `YYYY:MM:DD HH:mm:ss`（冒号日期）
        self.date_end = None
        self.notes = []


def get(rec, token, base, params=None, label=""):
    result = S.http_call(base, rec, token, params=params)
    payload = result.get("payload") or {}
    code = payload.get("code")
    print("  %-6s %-44s %-26s %s" % (rec["method"], rec["url"],
                                     "code=%s" % code, (payload.get("msg") or "")[:40]))
    return code, payload.get("data"), result


def find(records, url):
    for rec in records:
        if rec["url"] == url:
            return rec
    return None


# 需要参数的 GET 接口：url -> 从 ctx 生成查询参数（返回 None 表示这次没有可用的 id，跳过）
# 注意：同一个 API 里参数命名风格不统一，实测出来的写法都写在这里（别凭直觉改）
PARAM_RULES = {
    # snake_case 组
    "/api/v1/album/item": lambda c: {"album_id": c.album_id} if c.album_id else None,
    "/api/v1/gallery/getList": lambda c: ({"start_time": c.date_start, "end_time": c.date_end,
                                          "limit": 5, "offset": 0, "mode": "datetime"}
                                         if c.date_start else None),
    "/api/v1/gallery/getOne": lambda c: {"id": c.photo_id} if c.photo_id else None,
    "/api/v1/thumbnail/status": lambda c: {"ids": c.photo_id} if c.photo_id else None,
    "/api/v1/video/decode/info": lambda c: {"id": c.photo_id} if c.photo_id else None,
    "/api/v1/ai-person/detail": lambda c: {"id": c.person_id} if c.person_id else None,
    "/api/v1/ai-person/photoLibrary/timeLine": lambda c: ({"id": c.person_id, "offset": 0,
                                                          "limit": 10}
                                                         if c.person_id else None),
    "/api/v1/share_link/detail": lambda c: {"id": c.share_id} if c.share_id else None,
    "/api/v1/task-panel/fail": lambda c: ({"taskType": c.task_type} if c.task_type else None),
    "/api/v1/folder_view/getFolderList": lambda c: {"path": c.folder_path} if c.folder_path else None,
    # camelCase 组（相册时间线）
    "/api/v1/album/normal/timeline": lambda c: ({"startTime": c.date_start, "endTime": c.date_end,
                                                "albumId": c.album_id}
                                               if c.album_id and c.date_start else None),
    "/api/v1/album/baby/timeline": lambda c: ({"startTime": c.date_start, "endTime": c.date_end,
                                              "albumId": c.album_id}
                                             if c.album_id and c.date_start else None),
}


def phase_get(records, token, base, only=None):
    print("\n=== 第一阶段：GET 接口实测 ===")
    ctx = Ctx()
    ok = fail = 0

    def run(url, params=None, label=""):
        nonlocal ok, fail
        rec = find(records, url)
        if not rec:
            return None
        if only and only not in url:
            return None
        code, data, result = get(rec, token, base, params=params, label=label)
        S.record_probe(rec, result)
        if code == 0:
            ok += 1
        else:
            fail += 1
        return data if code == 0 else None

    # 1) 先跑一遍普通 GET（列表类带上分页）
    for rec in records:
        if rec["method"] != "GET":
            continue
        if only and only not in rec["url"]:
            continue
        if rec["url"] in PARAM_RULES:
            continue                        # 需要 id 的留到第二轮
        params = None
        if any(k in rec["url"] for k in ("list", "timeline")) and \
                rec["url"] not in ("/api/v1/album/list", "/api/v1/share_link/list"):
            params = {"offset": 0, "limit": 10}
        code, data, result = get(rec, token, base, params=params)
        S.record_probe(rec, result, sent_params=params)
        if code == 0:
            ok += 1
        else:
            fail += 1
        # 收集真实 id
        if code == 0 and isinstance(data, dict):
            items = data.get("list") or data.get("files") or []
            if items and isinstance(items[0], dict):
                first = items[0]
                if rec["url"] == "/api/v1/album/list" and not ctx.album_id:
                    ctx.album_id = first.get("albumId") or first.get("id")
                if rec["url"] == "/api/v1/ai-person/list" and not ctx.person_id:
                    ctx.person_id = first.get("id")
                if rec["url"] == "/api/v1/share_link/list" and not ctx.share_id:
                    ctx.share_id = first.get("id")
            if rec["url"] == "/api/v1/album/list" and items:
                ctx.notes.append("相册数 %d" % len(items))
            if rec["url"].endswith("upload/path") and isinstance(data.get("upload"), dict):
                # 形如 /vol3/1000/photo/.@#local，去掉内部后缀才是可列的目录
                folder = (data["upload"].get("path") or "").rstrip("/")
                folder = folder.split("/.@#")[0]
                ctx.folder_path = folder or None
    # 照片 id：先用 timeline 的日期桶拼 start_time（格式是 `YYYY:MM:DD HH:mm:ss`，冒号日期）
    if not ctx.date_start:
        tl = find(records, "/api/v1/gallery/timeline")
        if tl:
            _, d, _r = get(tl, token, base)
            buckets = ((d or {}).get("list") or [])
            if buckets:
                b = buckets[0]
                ctx.date_start = "%04d:%02d:%02d 00:00:00" % (
                    b.get("year") or 2026, b.get("month") or 1, b.get("day") or 1)
                ctx.date_end = "%04d:%02d:%02d 23:59:59" % (
                    b.get("year") or 2026, b.get("month") or 1, b.get("day") or 1)
    if not ctx.photo_id and ctx.date_start:
        gl = find(records, "/api/v1/gallery/getList")
        code, d2, result = get(gl, token, base,
                               params={"start_time": ctx.date_start, "end_time": ctx.date_end,
                                       "limit": 5, "offset": 0, "mode": "datetime"})
        S.record_probe(gl, result, sent_params={"start_time": ctx.date_start, "end_time": ctx.date_end, "limit": 5, "offset": 0, "mode": "datetime"})
        items = (d2 or {}).get("list") or []
        if items:
            ctx.photo_id = items[0].get("id")
        if code == 0:
            ok += 1
        else:
            fail += 1

    print("\n--- 收集到的真实 id：album=%s photo=%s person=%s share=%s folder=%s"
          % (ctx.album_id, ctx.photo_id, ctx.person_id, ctx.share_id, ctx.folder_path))

    # 2) 需要 id 的再跑一轮
    print("\n--- 带真实 id 重试需要参数的 GET")
    for url, rule in PARAM_RULES.items():
        rec = find(records, url)
        if not rec or (only and only not in url):
            continue
        try:
            params = rule(ctx)
        except Exception:
            params = None
        if params is None:                    # 没拿到对应 id，如实标注
            rec["probe"] = "跳过（本次没有可用的 id 参数）"
            continue
        code, data, result = get(rec, token, base, params=params)
        S.record_probe(rec, result, sent_params=params)
        if code == 0:
            ok += 1
        else:
            fail += 1
    return ctx, ok, fail


def phase_writes(records, token, base):
    """可逆写场景：建相册 → 改名 → 加照片 → 移出 → 删相册（每步验证 + 兜底清理）"""
    print("\n=== 第二阶段：可逆写接口实测（建相册 → 查详情/时间线 → 改名 → 加/移照片 → 删除）===")
    results = {}
    name = "fnapi-test-%d" % int(time.time())

    # 先拿一张真实照片的 id（照片时间线接口支持时间桶，getList 用冒号日期格式）
    photo_id = None
    ctx_date = ("2000:01:01 00:00:00", "2030:01:01 00:00:00")
    tl = find(records, "/api/v1/gallery/timeline")
    if tl:
        _, d, _r = get(tl, token, base)
        buckets = (d or {}).get("list") or []
        if buckets:
            b = buckets[0]
            ctx_date = ("%04d:%02d:%02d 00:00:00" % (b.get("year"), b.get("month"), b.get("day")),
                        "%04d:%02d:%02d 23:59:59" % (b.get("year"), b.get("month"), b.get("day")))
    gl = find(records, "/api/v1/gallery/getList")
    if gl:
        code, d, result = get(gl, token, base,
                              params={"start_time": ctx_date[0], "end_time": ctx_date[1],
                                      "limit": 5, "offset": 0, "mode": "datetime"})
        S.record_probe(gl, result, sent_params={"start_time": ctx_date[0], "end_time": ctx_date[1], "limit": 5, "offset": 0, "mode": "datetime"})
        items = (d or {}).get("list") or []
        if items:
            photo_id = items[0].get("id")
    print("  用于测试的照片 id =", photo_id)

    def call(url, body, note):
        rec = find(records, url)
        if not rec:
            print("  !! 清单里没有", url)
            return None, None, None
        result = S.http_call(base, rec, token, body=body)
        payload = result.get("payload") or {}
        print("  %-6s %-42s body=%-46s -> code=%s %s"
              % (rec["method"], url, json.dumps(body, ensure_ascii=False)[:46],
                 payload.get("code"), (payload.get("msg") or "")[:40]))
        S.record_probe(rec, result, sent_body=body)
        results[url] = payload.get("code")
        return payload.get("code"), payload.get("data"), rec

    def get_and_record(url, params=None):
        rec = find(records, url)
        if not rec:
            return None
        result = S.http_call(base, rec, token, params=params)
        payload = result.get("payload") or {}
        print("  %-6s %-42s -> code=%s %s" % (rec["method"], url,
                                              payload.get("code"),
                                              (payload.get("msg") or "")[:40]))
        S.record_probe(rec, result, sent_params=params)
        return payload.get("data")

    # 1) 建相册（请求用 snake_case：album_name / ids；响应是 camelCase：albumId）
    code, data, rec = call("/api/v1/album/create", {"album_name": name, "ids": []},
                           "建相册")
    album_id = None
    if isinstance(data, dict):
        album_id = data.get("albumId") or data.get("id") or data.get("album_id")
    print("     新相册 id =", album_id)
    if album_id:
        # 从列表里核对确实建出来了（列表字段是 albumId / albumName）
        lst = find(records, "/api/v1/album/list")
        _, d, _r = get(lst, token, base, params={"offset": 0, "limit": 100})
        names = [(x.get("albumId"), x.get("albumName")) for x in ((d or {}).get("list") or [])]
        print("     列表核对：", names[:6])

    try:
        if album_id:
            # 2) 相册详情 / 时间线（注意这俩接口参数是 camelCase）
            get_and_record("/api/v1/album/item", {"album_id": album_id})
            get_and_record("/api/v1/album/normal/timeline",
                           {"startTime": ctx_date[0], "endTime": ctx_date[1],
                            "albumId": album_id})
            # 3) 改名
            call("/api/v1/album/update/name",
                 {"album_id": album_id, "album_name": name + "-renamed"}, "相册改名")
            # 4) 照片相关（拿得到照片 id 才测）
            if photo_id:
                call("/api/v1/gallery/addTo/album",
                     {"ids": [photo_id], "album_id": album_id}, "照片加入相册")
                get_and_record("/api/v1/album/photo/belong", {"album_id": album_id})
                call("/api/v1/album/photo/remove",
                     {"ids": [photo_id], "album_id": album_id}, "照片移出相册")
    finally:
        # 5) 删相册（兜底一定要删掉）
        if album_id:
            code, _, _ = call("/api/v1/album/delete", {"album_id": album_id}, "删相册")
            if code != 0:
                call("/api/v1/album/remove", {"album_id": album_id}, "删相册（备用接口）")

    # 6) 验证相册已经删掉
    print("\n--- 清理验证：相册列表里还有没有 %s" % name)
    lst = find(records, "/api/v1/album/list")
    _, d, _r = get(lst, token, base, params={"offset": 0, "limit": 100})
    names = [x.get("album_name") or x.get("name") for x in ((d or {}).get("list") or [])]
    left = [n for n in names if n and name in str(n)]
    print("     剩余同名相册：", left or "无（已清理干净）")
    return results, left


def main():
    ap = argparse.ArgumentParser(description="/p 相册应用 HTTP 接口实测")
    ap.add_argument("--http", default=HTTP_JSON)
    ap.add_argument("--base", default="http://192.168.1.10:5666")
    ap.add_argument("--ws", default=os.environ.get(
        "FNNAS_WS", "ws://192.168.1.10:5666/websocket?type=main"))
    ap.add_argument("--username", default=os.environ.get("fn_username", ""))
    ap.add_argument("--password", default=os.environ.get("fn_password", ""))
    ap.add_argument("--only", default=None)
    ap.add_argument("--no-writes", action="store_true", help="只测 GET，不碰写接口")
    ap.add_argument("--dry-run", action="store_true", help="不写回 http_api.json")
    args = ap.parse_args()

    if not args.username or not args.password:
        print("请先设置 fn_username / fn_password")
        return 2
    with open(args.http, encoding="utf-8") as f:
        doc = json.load(f)
    records = doc["endpoints"]

    print("WebSocket 登录 %s ..." % args.username)
    token = S.ws_token(args.username, args.password, args.ws)
    if not token:
        print("登录失败")
        return 2
    print("拿到 fnos-token（%d 字符）\n" % len(token))

    ctx, ok, fail = phase_get(records, token, args.base, only=args.only)
    write_results, left = ({}, [])
    if not args.no_writes and not args.only:
        write_results, left = phase_writes(records, token, args.base)

    gets = [r for r in records if r["method"] == "GET"]
    ok_get = sum(1 for r in gets if r.get("probe_code") == 0)
    print("\n=== 汇总 ===")
    print("  GET 接口 %d 个：code 0 = %d 个，失败 = %d 个"
          % (len(gets), ok_get, len(gets) - ok_get))
    if write_results:
        print("  可逆写接口实测：%s" % json.dumps(write_results, ensure_ascii=False))
        print("  清理残留：", left or "无")

    doc["meta"]["probed_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
    doc["meta"]["probe_account"] = args.username
    doc["meta"]["probe_note"] = ("cookie fnos-token + authx 签名；GET 全量实测，"
                                 "写接口只测可逆场景（建/改/删相册）")
    if not args.dry_run:
        with open(args.http, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
        print("已更新 %s" % os.path.relpath(args.http, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
