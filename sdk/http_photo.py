# -*- coding: utf-8 -*-
"""
`/p` 相册应用的 HTTP 客户端（REST，不是 WebSocket）。

为什么单独一个客户端
    - 主 SDK（`FnOsClient`）走 WebSocket RPC；相册应用（`/p`）**完全不用 WebSocket**，
      它是 `POST/GET /p/api/v1/...` 的普通 REST，鉴权也是另一套；
    - 这套 REST 的鉴权是「cookie `fnos-token` + `authx` 签名」，签名覆盖请求参数，
      手工拼很容易踩 `code 5000 invalid sign`，所以封成客户端。

鉴权（真机实测跑通）
    请求地址  http://<NAS>:5666/p + 路径，例如 /p/api/v1/album/list
    请求头    Cookie: fnos-token=<WebSocket 登录返回的 token>
    请求头    authx: nonce=<6位>&timestamp=<13位毫秒>&sign=<md5>
              sign = md5(APPKEY + "_" + 路径 + "_" + nonce + "_" + timestamp + "_"
                         + md5(反编码后的参数串) + "_" + 应用密钥)
    响应外壳  {"code": 0, "msg": "", "data": {...}}    # code != 0 表示失败

用法
    from sdk.http_photo import PhotoHttpClient

    client = await PhotoHttpClient.login("http://192.168.1.10:5666", "用户名", "密码")
    albums = await client.albums()                       # 相册列表
    album  = await client.album_create("旅行照片")       # 建相册
    await client.album_add_photos(album["albumId"], [6958])
    timeline = await client.album_timeline(album["albumId"])
    await client.album_delete(album["albumId"])          # 删相册

    # 需要自己拼其它接口时：
    data = await client.request("GET", "/api/v1/thumbnail/status", params={"ids": 6958})

详细端点/字段/坑见 `docs/modules/album.md`。
"""

import asyncio
import hashlib
import json
import random
import time
import urllib.error
import urllib.parse
import urllib.request

# 前端产物里硬编码的 APPKEY 和 XOR 混淆过的「/p 应用密钥」（tools/scan_http.py:decode_auth_key 能解）
APP_KEY = "NDzZTVxnRKP8Z0jXg1VAMonaG8akvh"
APP_SECRET = "EAECCF25-80A6-4666-A7C2-A76904A74AB6"


class PhotoHttpError(Exception):
    """接口返回 code != 0"""

    def __init__(self, code, msg, path="", data=None):
        self.code = code
        self.msg = msg
        self.path = path
        self.data = data
        super().__init__("code=%s %s" % (code, msg or ""))


def make_authx(method, path, params=None, body=None, secret=APP_SECRET,
               app_key=APP_KEY, nonce=None, stamp=None):
    """
    生成 `authx` 头。算法照抄前端 `at()`：

    - GET：参数按 key 排序拼成 `k=v&k=v`，再 `decodeURIComponent` 后取 md5；
    - POST/PUT：对 `JSON.stringify(body)` 反编码后取 md5；
    - 再把 `APPKEY_路径_nonce_时间戳_上面那个md5_应用密钥` 拼起来取 md5 作为 sign。
    """
    def md5(text):
        return hashlib.md5(text.encode("utf-8")).hexdigest()

    if method.upper() == "GET":
        merged = {k: v for k, v in (params or {}).items() if v is not None}
        raw = urllib.parse.urlencode(sorted(merged.items()),
                                     quote_via=urllib.parse.quote).replace("+", "%20")
    else:
        raw = json.dumps(body, separators=(",", ":")) if body is not None else ""
    inner = md5(urllib.parse.unquote(raw))
    nonce = str(nonce if nonce is not None else random.randint(100000, 999999))
    stamp = str(stamp if stamp is not None else int(time.time() * 1000))
    sign = md5("_".join([app_key, path, nonce, stamp, inner, secret]))
    return "nonce=%s&timestamp=%s&sign=%s" % (nonce, stamp, sign)


class PhotoHttpClient:
    """
    相册应用 HTTP 客户端。

    :param base_url: 例如 http://192.168.1.10:5666（不要带 /p）
    :param token: WebSocket 登录返回的 token；不传就调 `login()`
    :param secret: `/p` 应用密钥（默认是本机产物里解出来的那个）
    """

    def __init__(self, base_url, token=None, secret=APP_SECRET, app_key=APP_KEY,
                 timeout=20):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.secret = secret
        self.app_key = app_key
        self.timeout = timeout
        self.last = None            # 最近一次请求的原始响应（调试用）

    # ------------------------------------------------------------- 登录
    @classmethod
    async def login(cls, base_url, username, password,
                    ws_url="ws://192.168.1.10:5666/websocket?type=main",
                    **kwargs):
        """
        先用 WebSocket 登录拿 token，再返回可用的 HTTP 客户端。
        `/p` 的 `fnos-token` cookie 就是 WebSocket 登录返回的 token。
        """
        from sdk import FnOsClient
        ws = FnOsClient(ping_interval=60)
        ws.logger.setLevel(50)
        await ws.connect(ws_url)
        ok = await ws.login(username, password)
        token = ws.token if ok else None
        await ws.close()
        if not token:
            raise PhotoHttpError(None, "WebSocket 登录失败（检查账号密码）")
        return cls(base_url, token=token, **kwargs)

    # ------------------------------------------------------------- 底层
    def _request_sync(self, method, path, params=None, body=None):
        if not self.token:
            raise PhotoHttpError(None, "没有 token，先 login() 或构造时传 token")
        method = method.upper()
        url = self.base_url + "/p" + path
        if params:
            url += "?" + urllib.parse.urlencode(params)
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Cookie": "fnos-token=" + self.token,
            "authx": make_authx(method, "/p" + path, params=params, body=body,
                                secret=self.secret, app_key=self.app_key),
        }
        data = None
        if method != "GET":
            headers["Content-Type"] = "application/json"
            data = json.dumps(body if body is not None else {},
                              separators=(",", ":")).encode()
        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as resp:
                text = resp.read()
                status = resp.status
        except urllib.error.HTTPError as exc:
            text = exc.read()
            status = exc.code
        try:
            payload = json.loads(text.decode("utf-8", "replace"))
        except Exception:
            raise PhotoHttpError(None, "响应不是 JSON（HTTP %s）：%r"
                                 % (status, text[:200]), path)
        self.last = payload
        code = payload.get("code")
        if code != 0:
            raise PhotoHttpError(code, payload.get("msg"), path, payload.get("data"))
        return payload.get("data")

    async def request(self, method, path, params=None, body=None):
        """通用调用：成功返回 data，失败抛 PhotoHttpError"""
        return await asyncio.to_thread(self._request_sync, method, path, params, body)

    async def get(self, path, **params):
        return await self.request("GET", path, params=params or None)

    async def post(self, path, body=None):
        return await self.request("POST", path, body=body)

    # ------------------------------------------------------------- 用户/存储
    async def user_info(self):
        """当前用户信息"""
        return await self.get("/api/v1/user/info")

    async def photo_stat(self):
        """照片/视频数量与占用统计"""
        return await self.get("/api/v1/user_photo/stat")

    async def pools(self):
        """存储空间列表"""
        return await self.get("/api/v2/server/pools")

    async def app_version(self):
        return await self.get("/api/v1/app/version")

    # ------------------------------------------------------------- 相册
    async def albums(self, sort_by="createTime", sort_direction="desc", limit=1000):
        """相册列表。返回 `{list: [{albumId, albumName, photoCount, posterUrl, …}]}`"""
        return await self.get("/api/v1/album/list", sort_by=sort_by,
                              sort_direction=sort_direction, offset=0, limit=limit)

    async def album(self, album_id):
        """单个相册的详情（参数名是 album_id）"""
        return await self.get("/api/v1/album/item", album_id=album_id)

    async def album_create(self, name, photo_ids=None):
        """
        创建相册（请求参数是 snake_case）。

        :param name: 相册名（`album_name`）
        :param photo_ids: 可选，创建时就把这些照片放进去
        :return: `{albumId, repeatCount, successCount}`；albumId 在**返回体**里
        """
        return await self.post("/api/v1/album/create",
                               {"album_name": name, "ids": list(photo_ids or [])})

    async def album_rename(self, album_id, name):
        """相册改名"""
        return await self.post("/api/v1/album/update/name",
                               {"album_id": album_id, "album_name": name})

    async def album_delete(self, album_id):
        """删除相册（相册里的照片不会被删）"""
        return await self.post("/api/v1/album/delete", {"album_id": album_id})

    async def album_add_photos(self, album_id, photo_ids):
        """把照片加进相册"""
        return await self.post("/api/v1/gallery/addTo/album",
                               {"ids": list(photo_ids), "album_id": album_id})

    async def album_remove_photos(self, album_id, photo_ids):
        """把照片移出相册"""
        return await self.post("/api/v1/album/photo/remove",
                               {"ids": list(photo_ids), "album_id": album_id})

    async def album_of_photo(self, photo_id):
        """某张照片属于哪些相册"""
        return await self.get("/api/v1/album/photo/belong", id=photo_id)

    async def album_timeline(self, album_id, start_time="2000:01:01 00:00:00",
                             end_time="2030:01:01 00:00:00"):
        """
        相册时间线。⚠ 注意这个接口的参数是 **camelCase**：
        `startTime` / `endTime` / `albumId`，时间是 `YYYY:MM:DD HH:mm:ss`（冒号日期）。
        """
        return await self.get("/api/v1/album/normal/timeline", startTime=start_time,
                              endTime=end_time, albumId=album_id)

    # ------------------------------------------------------------- 相册分享
    async def album_grants_mine(self):
        """我分享出去的相册"""
        return await self.get("/api/v1/album_grant/list_mine")

    async def album_grants_to_me(self):
        """别人分享给我的相册"""
        return await self.get("/api/v1/album_grant/list_to_me")

    async def album_grant_create(self, album_id, granted_uid, permission="read"):
        """
        把相册分享给指定用户（参数名按前端调用点：album_id / uid / permission）
        实测本机没有其它用户，这条没做真机验证，参数名来自 JS 调用点。
        """
        return await self.post("/api/v1/album_grant/create",
                               {"album_id": album_id, "uid": granted_uid,
                                "permission": permission})

    async def album_grant_cancel(self, album_id, granted_uid):
        """取消相册分享"""
        return await self.post("/api/v1/album_grant/cancel",
                               {"album_id": album_id, "uid": granted_uid})

    # ------------------------------------------------------------- 照片
    async def gallery_timeline(self):
        """照片时间线（按年月日分桶：`{year, month, day, itemCount}`）"""
        return await self.get("/api/v1/gallery/timeline")

    async def photos(self, start_time, end_time, offset=0, limit=50, mode="datetime"):
        """
        照片列表。`start_time`/`end_time` 必须是 `YYYY:MM:DD HH:mm:ss`（冒号日期）。

        :param mode: `datetime`（按拍摄时间）或 `createdAt`（按导入时间）
        """
        return await self.get("/api/v1/gallery/getList", start_time=start_time,
                              end_time=end_time, offset=offset, limit=limit, mode=mode)

    async def photo(self, photo_id):
        """单张照片详情"""
        return await self.get("/api/v1/gallery/getOne", id=photo_id)

    async def thumbnail_status(self, photo_id):
        """缩略图生成状态（ids 可以是逗号分隔的多个 id）"""
        return await self.get("/api/v1/thumbnail/status", ids=photo_id)

    async def photo_tags(self):
        """标签列表"""
        return await self.get("/api/v1/explore/tags")
