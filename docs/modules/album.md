# 相册（`/p` 相册应用）

- 所属应用：`/p`（飞牛的**相册 / AI 相册**应用，前端版本 `0.9.13`）
- 接口形式：**HTTP REST**（`/p/api/v1/...`），不用 WebSocket
- 鉴权：cookie `fnos-token` + `authx` 签名（和 WebSocket 那套完全不同，见下面「怎么调」）
- 实测：2026-10 在真机（`demoNAS`）上用一个测试账号跑通「浏览 → 建相册 → 加照片 → 改名 →
  设封面 → 移出照片 → 删相册」全流程；相册数测试前后一致（0 → 0），用户的照片文件未改动
- 复现：`python tools/probe_album.py`（样例数据落在 `data/album_probe.json`）
- 全量 151 个 `/p` 接口见 [api/http.md](../api/http.md)

## 怎么调

```bash
请求地址  http://<NAS>:5666/p + 路径          # 例如 /p/api/v1/album/list
请求头    Cookie: fnos-token=<WS 登录返回的 token>
请求头    authx: nonce=<6位>&timestamp=<13位毫秒>&sign=<md5>
响应      {"code": 0, "msg": "", "data": {...}}     # code != 0 即失败
```

`sign = md5(APPKEY_路径_nonce_时间戳_md5(反编码后的参数串)_应用密钥)`；
GET 的参数要**按 key 排序**再算，POST 算的是 `JSON.stringify(body)`。
只缺 token → HTTP 401，只缺 authx → `code 5000 invalid sign`。

用 SDK 一行搞定（`sdk/http_photo.py`）：

```python
from sdk.http_photo import PhotoHttpClient

client = await PhotoHttpClient.login("http://192.168.1.10:5666", "demo-user", "密码")
print(await client.albums())          # 相册列表
```

## 三个「反直觉」的坑（实测踩过）

| 坑 | 说明 |
|----|------|
| **参数命名风格不统一** | 同一组接口里：`album/item`、`album/photo/belong`、`gallery/addTo/album` 用 **snake_case**（`album_id`）；`album/normal/timeline`、`album/update/setting` 用 **camelCase**（`albumId`）；而**响应字段一律是 camelCase**（`albumId` / `albumName`） |
| **时间格式是冒号日期** | 照片时间线/列表的 `start_time`、`end_time` 要写成 `2026:10:04 00:00:00`（不是 `2026-10-04`），写错只会得到 `code 400 invalid params` |
| **新建相册的 id 在返回体里** | `POST /album/create` 回的是 `{"albumId": 8, "repeatCount": 0, "successCount": 0}`，**不是** `data: 8`；而改名/删相册/设封面都成功返回 `data: null` |

## 数据模型

### 相册对象（`album/list`、`album/item` 的 `list[]` / 根对象）

| 字段（类型） | 说明 |
|---|---|
| `albumId` (int) | 相册 ID，后续所有操作的 `album_id` |
| `albumName` (string) | 相册名 |
| `source` (string) | 来源：`user` = 手动建的相册 |
| `photoCount` / `videoCount` (int) | 相册内**照片数 / 视频数**（分开计数：加进去的是 mp4 时 `photoCount` 仍是 0） |
| `posterUrl` / `posterImgUrl` (string) | 封面地址；设过封面才有，形如 `/p/api/v1/stream/p/t/<照片id>/s/<uuid>` |
| `posterUpId` / `posterUUID` | 封面照片的 id / uuid（`album/photo/belong` 里返回） |
| `startDateTime` / `endDateTime` (string) | 相册内照片的时间范围，格式 `2026:10:04 08:15:01`；空相册是空串 |
| `shared` (int) / `grants` (array) / `grantPermission` (string) | 分享状态 / 被授权用户列表 / 权限 |
| `ownerId` / `ownerName` | 相册所有者 |
| `category` (int) / `displayType` (int) | 相册分类（0 = 普通）与展示方式（0 = 普通 / 1 = 宝宝相册等） |
| `birthday` / `babyYear` / `babyMonth` / `babyDay` / `lunarMonth` / `lunarDay` / `specialNode` | 宝宝相册才用到的生日与"特别节点" |
| `hasOtherUserPhoto` / `readableUsers` | 是否含他人照片 / 可读用户 |
| `modTime` (int) | 修改时间（**毫秒**时间戳） |

### 照片对象（`gallery/getList`、`gallery/getOne`）

| 字段 | 说明 |
|---|---|
| `id` (int) | 照片 ID（加相册、查详情、取缩略图都用它） |
| `dateTime` / `photoDateTime` | 拍摄时间（`2026:10:04 16:30:20`，冒号格式） |
| `timeZoneOffset` (int) | 时区偏移，分钟（480 = UTC+8） |
| `fileType` / `category` | `mp4` / `video`、`jpg` / `photo` 等 |
| `fileName` / `fileSize` / `filePath` | 文件名、字节数、NAS 上的绝对路径 |
| `height` / `width` / `mp` | 分辨率与"11.1MP"这种描述 |
| `isLive` / `mediaDuration` | 实况照片 / 视频时长（秒） |
| `isRaw` / `isCollect` | RAW 格式 / 是否收藏 |
| `ownerId` / `ownerName` | 归属用户（`getOne` 里有 `ownerName`） |
| `thumbnailStatus` (int) | 缩略图状态（`thumbnail/status` 返回，1 = 已就绪） |

## 接口清单（按功能）

### 1. 浏览

| 接口 | 参数 | 说明 |
|---|---|---|
| `GET /api/v1/album/list` | `sort_by`、`sort_direction`、`offset`、`limit` | 相册列表 → `{list:[相册对象]}` |
| `GET /api/v1/album/item` | `album_id` | 单个相册详情 → 相册对象 |
| `GET /api/v1/album/normal/timeline` | **`startTime`、`endTime`、`albumId`** | 相册时间线（按天分桶，`list` 为空表示这段时间没照片） |
| `GET /api/v1/album/baby/timeline` | 同上 | 宝宝相册时间线（本机无宝宝相册，未实测成功） |
| `GET /api/v1/album/photo/belong` | `album_id`（实际传照片 id 也行，见坑） | 照片归属哪些相册 |
| `GET /api/v1/gallery/timeline` | — | 照片时间线：`{list:[{year,month,day,itemCount}], nasDate}` |
| `GET /api/v1/gallery/getList` | `start_time`、`end_time`、`offset`、`limit`、`mode` | 某段时间内的照片（**冒号日期**） |
| `GET /api/v1/gallery/getOne` | `id` | 单张照片详情 |
| `GET /api/v1/thumbnail/status` | `ids`（可逗号分隔） | 缩略图状态 → `{list:[{id, thumbnailStatus}]}` |
| `GET /api/v1/user_photo/stat` | — | 照片/视频总数 → `{photoCount: 7253, videoCount: 272}` |
| `GET /api/v1/explore/tags` / `explore/geos` | `offset`、`limit` | 按标签 / 地理位置探索 |
| `GET /api/v1/map/timeLine`、`map/preview/*` | — | 地图模式（时间线需要中心点/边界参数） |

### 2. 管理

| 接口 | 参数 | 说明 |
|---|---|---|
| `POST /api/v1/album/create` | `album_name`、`ids`（创建时带照片，可空） | 建相册 → `{albumId, repeatCount, successCount}` |
| `POST /api/v1/album/update/name` | `album_id`、`album_name` | 改名 |
| `POST /api/v1/album/update/poster` | `album_id`、`id`（照片 id） | 设置封面 |
| `POST /api/v1/album/update/setting` | `albumId`、`conditionSettings` | 相册设置（**camelCase**） |
| `POST /api/v1/album/delete` | `album_id` | 删相册（**相册里的照片不会被删**） |
| `POST /api/v1/gallery/addTo/album` | `ids`（照片 id 数组）、`album_id` | 把照片加进相册 → `{albumId, albumName, repeatCount, successCount}` |
| `POST /api/v1/album/photo/remove` | `ids`、`album_id` | 把照片移出相册 |
| `POST /api/v1/album/download/all` | — | 打包下载整本相册（异步任务） |
| `POST /api/v1/album/condition/add`、`condition/list`、`condition/remove` | 条件相册（"按时间/地点自动收录"） | 条件相册的增删查；`list` 需要额外参数，未调通 |

### 3. 分享（`album_grant`）

| 接口 | 说明 |
|---|---|
| `GET /api/v1/album_grant/list_mine` | 我分享出去的相册 → `{list:[相册对象+grants]}` |
| `GET /api/v1/album_grant/list_to_me` | 别人分享给我的相册 |
| `POST /api/v1/album_grant/create` | 把相册分享给某个用户（参数名来自 JS 调用点：`album_id` / `uid` / `permission`；本机没有第二个用户，**未真机验证**） |
| `POST /api/v1/album_grant/update` | 改分享权限（未验证） |
| `POST /api/v1/album_grant/cancel` | 取消分享（未验证） |

> 「分享相册」和「生成公开分享链接」是两件事：公开链接那套是
> `appcgi.sharesvr.share.link.*`（WebSocket），见 [分享链接](share.md)。

## 用法一：浏览照片（时间线 + 分页）

照片列表不能一次全拿，正确姿势是先取时间线桶，再按桶里的日期去拿：

```python
from sdk.http_photo import PhotoHttpClient

client = await PhotoHttpClient.login("http://192.168.1.10:5666", "demo-user", "密码")

tl = await client.gallery_timeline()
# {'list': [{'year': 2026, 'month': 10, 'day': 4, 'itemCount': 10}, …], 'nasDate': '2026-10-17'}

b = tl["list"][0]
start = "%04d:%02d:%02d 00:00:00" % (b["year"], b["month"], b["day"])
end = "%04d:%02d:%02d 23:59:59" % (b["year"], b["month"], b["day"])
photos = await client.photos(start, end, limit=50)      # GET gallery/getList
# {'list': [{'id': 6958, 'fileName': 'sample', 'category': 'video', 'filePath': '…', …}]}

detail = await client.photo(photos["list"][0]["id"])     # GET gallery/getOne
status = await client.thumbnail_status(photos["list"][0]["id"])
```

真实响应（截断）：

```json
{"count": null, "hasNext": null, "list": [
  {"id": 6958, "dateTime": "2026:10:04 16:30:20", "timeZoneOffset": 480,
   "fileType": "mp4", "category": "video", "fileName": "sample.MP4",
   "fileSize": 4603763329, "filePath": "/vol3/1000/photo/sample/sample/sample",
   "height": 3840, "width": 2880, "isLive": 0, "mediaDuration": 302}]}
```

## 用法二：建相册 → 加照片 → 设封面 → 改名 → 删除（可逆）

```python
album = await client.album_create("旅行照片")          # → {'albumId': 8, …}
aid = album["albumId"]

await client.album(aid)                                # 详情
await client.album_timeline(aid)                       # 相册时间线（camelCase 参数）
await client.album_add_photos(aid, [6958, 6957])       # → {'successCount': 2, …}
await client.album(aid)                                # 再看：videoCount=2、posterUrl 出现了
await client.album_of_photo(6958)                      # 照片归属哪些相册
await client.album_rename(aid, "旅行照片-2026")
await client.post("/api/v1/album/update/poster",       # 设封面
                 {"album_id": aid, "id": 6958})
await client.album_remove_photos(aid, [6958, 6957])    # 移出（照片本身不删）
await client.album_delete(aid)                         # 删相册（照片本身不删）
```

真实响应（关键几步）：

```jsonc
// 创建
{"albumId": 8, "repeatCount": 0, "successCount": 0}

// 加照片（成功后相册详情里的计数/封面/时间范围会变）
{"albumId": 8, "albumName": "sample", "repeatCount": 2, "successCount": 2}

// 加完再看详情：封面与时间范围自动算出来了
{"albumId": 8, "albumName": "sample", "photoCount": 0, "videoCount": 2,
 "posterUrl": "/p/api/v1/stream/p/t/6958/s/b3d32e71-…",
 "startDateTime": "2026:10:04 08:15:01", "endDateTime": "2026:10:04 08:30:20"}

// 改名 / 设封面 / 移出照片 / 删相册 → data 都是 null（code 0 即成功）
```

## 用法三：相册分享

```python
mine = await client.album_grants_mine()      # 我分享出去的
tome = await client.album_grants_to_me()     # 别人分享给我的

# 分享给某个 NAS 用户（参数名来自 JS 调用点，本机只有 demo-user 一个用户，未真机验证）
await client.album_grant_create(album_id, granted_uid=1001, permission="read")
await client.album_grant_cancel(album_id, granted_uid=1001)
```

> **不用账号登录的公开分享链接**请用 `appcgi.sharesvr.share.link.*`（WebSocket），
> 见 [分享链接](share.md)；`album_grant` 是「分享给 NAS 内的其它用户」。

## 错误码

| 响应 | 含义 | 常见原因 |
|------|------|---------|
| `code 0` | 成功 | `data` 可能是 `null`（改名/删除/设封面这类） |
| `code 400 invalid params` | 参数错/缺 | 少了 id、时间格式写成 `2026-10-04`、参数名用了 camelCase 而接口要 snake_case |
| `code 4023 Does not exist or no permission` | 路径/资源不存在或无权限 | 列了内部目录（`.@#local`） |
| `code 4029 Person does not exist` | 人物不存在 | AI 人物未聚类出一致的人 |
| `code 4004 Photo does not exist` | 照片不存在 | 用了不存在的 photo id |
| `code 4016 Index is rebuilding` | 搜索索引重建中 | 稍后重试 |
| `code 5000 invalid sign` | 签名不对 | 缺 authx / 参数没排序 / POST 签名和 body 不一致 |
| HTTP 401（空体） | 没登录/缺 cookie | 漏了 `fnos-token` |

## 实测状态

| 范围 | 结果 |
|------|------|
| `/p` 全部 GET | 62 个里 **53 个返回 `code 0`**，其余是缺必填参数或资源不存在（见 [api/http.md](../api/http.md)） |
| 相册写接口 | `album/create`、`album/update/name`、`album/update/poster`、`gallery/addTo/album`、`album/photo/remove`、`album/delete` **全部实测成功**，且测试相册已删除、列表复原 |
| 相册分享 | `album_grant/create|update|cancel` 因为本机没有第二个用户，**未真机验证**（参数名取自 JS 调用点） |
| 条件相册 / 宝宝相册 | `album/condition/list`、`album/baby/timeline` 缺必需参数，**未调通** |

复现：

```bash
python tools/probe_album.py      # 跑一遍相册全流程，样例写进 data/album_probe.json
python tools/probe_http.py       # 全量 151 个 /p 接口的实测
```
