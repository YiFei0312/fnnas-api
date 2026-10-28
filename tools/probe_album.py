#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
相册接口的「功能与用法」实测脚本：用 `sdk/http_photo.py` 的客户端跑一遍真实相册流程，
把每一步的**请求 + 响应**记录下来，给 `docs/modules/album.md` 当样例数据。

流程（全部可逆：最后会删掉自己建的相册并核对列表复原）：
    用户/存储信息 → 相册列表 → 照片时间线 → 照片列表取真实 id → 建相册
    → 相册详情 → 相册时间线 → 加照片 → 再看详情 → 照片归属
    → 改名 → 设封面 → 删相册 → 核对列表复原

安全性：只新建/删除自己建的相册；不改用户的照片文件；破坏性接口（清空、删除照片、
条件相册删除等）都不碰。

用法：
    set fn_username=demo-user & set fn_password=...
    python tools/probe_album.py                 # 跑一遍并写 data/album_probe.json
    python tools/probe_album.py --dry-run       # 只看步骤，不真发
"""

import argparse
import asyncio
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from sdk.http_photo import PhotoHttpClient, PhotoHttpError          # noqa: E402

OUT = os.path.join(ROOT, "data", "album_probe.json")
BASE = "http://192.168.1.10:5666"
WS = "ws://192.168.1.10:5666/websocket?type=main"
# 写进文档的样例别太长：列表只留前 2 条、长字符串截断
TRIM_LIST = 2
TRIM_TEXT = 400


def trim(value, depth=0):
    if isinstance(value, list):
        return [trim(v, depth + 1) for v in value[:TRIM_LIST]]
    if isinstance(value, dict):
        return {k: trim(v, depth + 1) for k, v in value.items()}
    if isinstance(value, str) and len(value) > TRIM_TEXT:
        return value[:TRIM_TEXT] + "…"
    return value


class Recorder:
    def __init__(self):
        self.steps = []
        self.started = time.strftime("%Y-%m-%d %H:%M:%S")

    async def step(self, title, note, coro, params=None):
        """跑一步：记录请求与响应（失败也记下来）"""
        print("  %-46s" % title, end="")
        try:
            data = await coro
            print("OK")
            self.steps.append({"title": title, "note": note, "ok": True,
                               "data": trim(data)})
            return data
        except PhotoHttpError as exc:
            print("失败 code=%s %s" % (exc.code, exc.msg))
            self.steps.append({"title": title, "note": note, "ok": False,
                               "code": exc.code, "msg": exc.msg,
                               "data": trim(exc.data)})
            return None
        except Exception as exc:                                    # pragma: no cover
            print("异常 %s" % type(exc).__name__)
            self.steps.append({"title": title, "note": note, "ok": False,
                               "error": "%s: %s" % (type(exc).__name__, exc)})
            return None


async def run(args):
    print("WebSocket 登录 %s ..." % args.username)
    client = await PhotoHttpClient.login(args.base, args.username, args.password, ws_url=args.ws)
    print("拿到 fnos-token（%d 字符）\n" % len(client.token))
    rec = Recorder()
    ctx = {}

    print("=== 1) 基础信息（只读）")
    ctx["user"] = await rec.step("当前用户", "GET /api/v1/user/info", client.user_info())
    await rec.step("照片统计", "GET /api/v1/user_photo/stat", client.photo_stat())
    await rec.step("存储空间", "GET /api/v2/server/pools", client.pools())
    await rec.step("应用版本", "GET /api/v1/app/version", client.app_version())

    print("\n=== 2) 相册列表 / 分享（只读）")
    albums_before = await rec.step("相册列表（空）",
                                   "GET /api/v1/album/list?sort_by=…&offset=0&limit=…",
                                   client.albums())
    await rec.step("我分享出去的相册", "GET /api/v1/album_grant/list_mine",
                   client.album_grants_mine())
    await rec.step("别人分享给我的相册", "GET /api/v1/album_grant/list_to_me",
                   client.album_grants_to_me())
    ctx["albums_before"] = len((albums_before or {}).get("list") or [])

    print("\n=== 3) 照片时间线 → 照片列表（拿真实 photo_id）")
    timeline = await rec.step("照片时间线（按年月日分桶）", "GET /api/v1/gallery/timeline",
                              client.gallery_timeline())
    buckets = (timeline or {}).get("list") or []
    bucket = buckets[0] if buckets else {"year": 2026, "month": 1, "day": 1}
    start = "%04d:%02d:%02d 00:00:00" % (bucket.get("year"), bucket.get("month"),
                                         bucket.get("day"))
    end = "%04d:%02d:%02d 23:59:59" % (bucket.get("year"), bucket.get("month"),
                                       bucket.get("day"))
    photos = await rec.step("照片列表（冒号日期格式）",
                            "GET /api/v1/gallery/getList?start_time=…&end_time=…",
                            client.photos(start, end, limit=5))
    items = (photos or {}).get("list") or []
    photo_ids = [p.get("id") for p in items[:2] if p.get("id")]
    ctx["photo_ids"] = photo_ids
    if photo_ids:
        await rec.step("单张照片详情", "GET /api/v1/gallery/getOne?id=…",
                       client.photo(photo_ids[0]))
        await rec.step("缩略图状态", "GET /api/v1/thumbnail/status?ids=…",
                       client.thumbnail_status(photo_ids[0]))

    print("\n=== 4) 建相册 → 详情 → 时间线 → 加照片 → 改名 → 设封面 → 删除")
    name = "接口文档示例-%d" % int(time.time())
    created = await rec.step("创建相册", "POST /api/v1/album/create {album_name, ids}",
                             client.album_create(name, []))
    album_id = (created or {}).get("albumId")
    ctx["album_id"] = album_id
    print("     新相册 albumId =", album_id)
    try:
        if album_id:
            await rec.step("相册详情", "GET /api/v1/album/item?album_id=…",
                           client.album(album_id))
            await rec.step("相册时间线（camelCase 参数）",
                           "GET /api/v1/album/normal/timeline?startTime=…&albumId=…",
                           client.album_timeline(album_id))
            if photo_ids:
                await rec.step("把照片加进相册",
                               "POST /api/v1/gallery/addTo/album {ids, album_id}",
                               client.album_add_photos(album_id, photo_ids))
                await rec.step("再看相册详情（photoCount 变了）",
                               "GET /api/v1/album/item?album_id=…", client.album(album_id))
                await rec.step("照片归属哪些相册",
                               "GET /api/v1/album/photo/belong?id=…",
                               client.album_of_photo(photo_ids[0]))
            await rec.step("相册改名",
                           "POST /api/v1/album/update/name {album_id, album_name}",
                           client.album_rename(album_id, name + "-改名"))
            if photo_ids:
                await rec.step("设置相册封面",
                               "POST /api/v1/album/update/poster {album_id, id}",
                               client.post("/api/v1/album/update/poster",
                                           {"album_id": album_id, "id": photo_ids[0]}))
            if photo_ids:
                await rec.step("把照片移出相册",
                               "POST /api/v1/album/photo/remove {ids, album_id}",
                               client.album_remove_photos(album_id, photo_ids))
    finally:
        if album_id:
            await rec.step("删除相册", "POST /api/v1/album/delete {album_id}",
                           client.album_delete(album_id))

    print("\n=== 5) 核对复原")
    albums_after = await rec.step("删完再看相册列表", "GET /api/v1/album/list",
                                  client.albums())
    left = len((albums_after or {}).get("list") or [])
    ok = left == ctx["albums_before"]
    print("     相册数：测试前 %d，测试后 %d -> %s"
          % (ctx["albums_before"], left, "已复原" if ok else "有残留！"))

    result = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "base": args.base, "username": args.username,
        "album_id_used": ctx.get("album_id"), "photo_ids_used": ctx.get("photo_ids"),
        "albums_before": ctx["albums_before"], "albums_after": left,
        "restored": ok,
        "steps": rec.steps,
    }
    if not args.dry_run:
        with open(OUT, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print("\n样例数据 -> %s（%d 步）" % (os.path.relpath(OUT, ROOT), len(rec.steps)))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="相册接口实测 + 取样例")
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--ws", default=WS)
    ap.add_argument("--username", default=os.environ.get("fn_username", ""))
    ap.add_argument("--password", default=os.environ.get("fn_password", ""))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    if not args.username or not args.password:
        print("请先设置 fn_username / fn_password")
        return 2
    return asyncio.run(run(args))


if __name__ == "__main__":
    sys.exit(main())
