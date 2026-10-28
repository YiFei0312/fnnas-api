# `/p`（相册 / AI 相册）HTTP 接口

> 自动生成：`python tools/scan_http.py --probe`。数据源 `data\web-cache\p, data\web-cache\assets`，共 **151** 个 HTTP 接口。

`/p` 是飞牛的**相册 / AI 相册**应用（照片时间线、相册、人物、智能识别、地图、回收站、预览、上传…）。它**不用 WebSocket**，全部走 REST，所以没有 `appcgi.*` 那套 req 名。

> 顺带验证过：用 `tools/scan_web.py --entry /p/` 扫它的 WebSocket 接口，1331 个候选里 `endpoint` 档为 **0**（全是日期格式串、编解码器串、i18n 文案键），说明这个应用确实一个 WS 接口都没有、全部走下面的 HTTP。

## 怎么发请求

```
请求地址 = http://192.168.1.10:5666/p + 下表路径        # 例如 http://192.168.1.10:5666/p/api/v1/album/list
响应外壳 = {code, data, msg}     # code == 0 才算成功
```

鉴权（反编译前端产物 + 真机实测确认）：

```
请求头 Cookie : fnos-token=<WebSocket 登录拿到的 token>
请求头 authx  : nonce=<6位随机>&timestamp=<13位毫秒>&sign=<md5>
sign = md5( APPKEY + "_" + /p路径 + "_" + nonce + "_" + timestamp + "_"
           + md5(反编码后的参数串) + "_" + 应用密钥 )
APPKEY  = NDzZTVxnRKP8Z0jXg1VAMonaG8akvh              # 硬编码在产物里
应用密钥 = EAECCF25-80A6-4666-A7C2-A76904A74AB6   # 产物里 XOR 混淆，tools/scan_http.py:decode_auth_key() 可解
```

两个坑（都实测过）：

1. **只带 token 不带 authx** → `{"code":5000,"msg":"invalid sign"}`；**只带 authx 不带 token** → HTTP 401（响应体为空）。两个都要带。
2. 签名必须和实际发出去的数据一致：GET 的参数**按 key 排序**拼成 `k=v&k=v` 再解码后算 md5；POST 算的是 `JSON.stringify(body)`。差一个空格/顺序就是 5000。

`fnos-token` 就是 WS 登录返回的 `token`（前端 `ro.set('fnos-token', token)` 写进 cookie），所以 `tools/probe_http.py` 直接 WS 登录后用这个 token 就能调通，不用去浏览器里抄 Cookie。

> 封装好的客户端：`sdk/http_photo.py` 的 `PhotoHttpClient`（`albums()` / `album_create()` / `photos()` …）；相册接口的功能与用法、数据模型、完整流程见 [../modules/album.md](../modules/album.md)，实测取样例脚本 `tools/probe_album.py`。

## 分组

| 分组 | 接口数 |
|------|-------|
| `v1/ai-base` | 7 |
| `v1/ai-face` | 9 |
| `v1/ai-person` | 14 |
| `v1/ai-smart-rec` | 14 |
| `v1/album` | 16 |
| `v1/album_grant` | 5 |
| `v1/app` | 1 |
| `v1/config` | 2 |
| `v1/explore` | 3 |
| `v1/file` | 6 |
| `v1/fixer` | 2 |
| `v1/folder_view` | 4 |
| `v1/gallery` | 4 |
| `v1/google_takeout` | 3 |
| `v1/maintain` | 1 |
| `v1/map` | 3 |
| `v1/media_category` | 1 |
| `v1/photo` | 9 |
| `v1/preview` | 5 |
| `v1/recycle-bin` | 5 |
| `v1/repeat-photo` | 4 |
| `v1/search` | 2 |
| `v1/server` | 6 |
| `v1/share_link` | 6 |
| `v1/sys_config` | 6 |
| `v1/task-panel` | 3 |
| `v1/thumbnail` | 2 |
| `v1/user` | 1 |
| `v1/user_photo` | 1 |
| `v1/video` | 3 |
| `v2/photo` | 1 |
| `v2/search` | 1 |
| `v2/server` | 1 |

探活：共 67 个 GET 接口，其中 1 个返回 HTTP 401（路由存在、鉴权未过）。

## 真机实测结果（账号 `demo-user`，2026-10-17 16:25:51）

- **GET 62 个：53 个成功（`code 0`）**，9 个失败/需特定参数（见下表「实测」列）
- 写接口 89 个：**只实测了 5 个可逆场景**（建相册 → 查详情/时间线 → 改名 → 加照片 → 移出 → 删相册，最后核对相册列表已清空）；其余写接口涉及删除/清空/人物合并等，默认不发请求，避免改数据
- 失败原因主要是缺必填参数（`code 400 invalid params`）或资源不存在，不代表接口有问题

> 「参数/请求体（挖到的字段）」一列来自 `tools/extract_write_params.py`：顺着 RTK Query 的 hook 别名链（hook 变量 → 导出名 → 导入别名 → 调用点）找到前端实际传的参数对象，取顶层字段名。带 `?` 的是宽松匹配（可能混入同名函数的噪声，仅供参考）；空白表示参数由变量传入、没解析出来。

## v1/ai-base（7）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `checkRequirement` | GET | `/api/v1/ai-base/check-requirement` | - | AI 相关：检查运行条件 | HTTP 200 / code 0 |
| `setDataVol`（mutation） | POST | `/api/v1/ai-base/data-vol` | body | AI 相关：模型数据所在存储空间 | - |
| `setGPU`（mutation） | POST | `/api/v1/ai-base/gpu` | body | AI 相关：GPU 列表 | - |
| `getGPU` | GET | `/api/v1/ai-base/gpus` | - | AI 相关：GPU 列表 | HTTP 200 / code 0 |
| `initAIAction`（mutation） | POST | `/api/v1/ai-base/init` | body | AI 相关：初始化状态 | - |
| `getBaseSetting` | GET | `/api/v1/ai-base/setting` | - | AI 相关：AI 设置 | HTTP 200 / code 0 |
| `validateGPU`（mutation） | POST | `/api/v1/ai-base/validate-gpu` | body | AI 相关：校验 GPU 可用性 | - |

## v1/ai-face（9）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `cancelInstallFaceModel`（mutation） | POST | `/api/v1/ai-face/cancel-install` | - | 人脸识别：取消安装（写） | - |
| `getAIFaceRunParamsDefault` | GET | `/api/v1/ai-face/default-run-params` | - | 人脸识别：默认运行参数 | HTTP 200 / code 0 |
| `enabledAIFace`（mutation） | POST | `/api/v1/ai-face/enabled` | body | 人脸识别：是否启用 | - |
| `installAIFace`（mutation） | POST | `/api/v1/ai-face/install` | body | 人脸识别：安装模型（写） | - |
| `getAIFaceInstallOptions` | GET | `/api/v1/ai-face/install-options` | - | 人脸识别：安装模型（写） | HTTP 200 / code 0 |
| `startRunAIFaceTask`（mutation） | POST | `/api/v1/ai-face/run` | allowGpuDecoding, selectedGpuSequence, allowCpuDecoding | 人脸识别：开始识别任务（写） | - |
| `updateAIFaceRunParams`（mutation） | POST | `/api/v1/ai-face/run-params` | body | 人脸识别：开始识别任务（写） | - |
| `getAIFaceStatus` | GET | `/api/v1/ai-face/status` | ids | 人脸识别：任务状态 | HTTP 200 / code 0 |
| `unInstallAIFaceModel`（mutation） | POST | `/api/v1/ai-face/uninstall` | - | 人脸识别：卸载模型（写） | - |

## v1/ai-person（14）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `addFaceToPerson`（mutation） | POST | `/api/v1/ai-person/addFacesToPerson` | body | 把人脸加入人物（写） | - |
| `createPerson`（mutation） | POST | `/api/v1/ai-person/create` | body | 新建人物（写） | - |
| `getPerson` | GET | `/api/v1/ai-person/detail` | id | 人物详情 | HTTP 200 / code 0 |
| `getPersons` | GET | `/api/v1/ai-person/list` | offset, limit | 人物列表（人脸聚类结果） | HTTP 200 / code 0 |
| `mergePersons`（mutation） | POST | `/api/v1/ai-person/mergePeople` | id, candidateList | 合并人物（写） | - |
| `getPersonTimeline` | GET | `/api/v1/ai-person/photoLibrary/timeLine` | id, offset, limit | 人物照片时间线 | HTTP 200 / code 0 |
| `posterFromPhoto`（mutation） | POST | `/api/v1/ai-person/posterFromPhoto` | id, userPhotoId | 设置人物封面（写） | - |
| `removePerson`（mutation） | POST | `/api/v1/ai-person/remove` | ids | 删除人物（写） | - |
| `removeFacesFromPerson`（mutation） | POST | `/api/v1/ai-person/removeFacesFromPerson` | body | 删除人物（写） | - |
| `removePhotoFromPerson`（mutation） | POST | `/api/v1/ai-person/removePhotosFromPerson` | personId, userPhotoIds | 删除人物（写） | - |
| `renamePerson`（mutation） | POST | `/api/v1/ai-person/rename` | id, name | 人物改名（写） | - |
| `separatePhotoFromPerson`（mutation） | POST | `/api/v1/ai-person/separatePhotoFromPerson` | personId, userPhotoIds | 把照片从人物中拆出（写） | - |
| `setVisibility`（mutation） | POST | `/api/v1/ai-person/setVisibility` | visibleList, hiddenList | 人物是否可见（写） | - |
| `transferPhotoToPerson`（mutation） | POST | `/api/v1/ai-person/transferPhotosFromPerson` | body | 在人物间转移照片（写） | - |

## v1/ai-smart-rec（14）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `cancelInstallSmartRecModel`（mutation） | POST | `/api/v1/ai-smart-rec/cancel-install` | props, current, keyframes ? | 智能识别：取消安装（写） | - |
| `getAiCategories` | GET | `/api/v1/ai-smart-rec/categories` | data, ind, pos, key, parentPos, level ? | 智能识别：分类列表 | HTTP 200 / code 400 invalid params |
| `enabledCategory`（mutation） | POST | `/api/v1/ai-smart-rec/category-enabled` | body | 智能识别：开启/关闭分类（写） | - |
| `getSmartRecRunParamsDefault` | GET | `/api/v1/ai-smart-rec/default-run-params` | - | 智能识别：默认运行参数 | HTTP 200 / code 0 |
| `enabledAISmartRec`（mutation） | POST | `/api/v1/ai-smart-rec/enabled` | body | 智能识别：是否启用 | - |
| `installAISmartRec`（mutation） | POST | `/api/v1/ai-smart-rec/install` | body | 智能识别：安装模型（写） | - |
| `getAISmartRecInstallOptions` | GET | `/api/v1/ai-smart-rec/install-options` | - | 智能识别：安装模型（写） | HTTP 200 / code 0 |
| `startRunAISmartRecTask`（mutation） | POST | `/api/v1/ai-smart-rec/run` | ABORT, AFTER_DEFINITION_CHANGE, AUTOPLAY_PREVENTED, AUTOPLAY_STARTED, BEFORE_DEFINITION_CHANGE, BUFFER_CHANGE, CANPLAY, CANPLAY_THROUGH ? | 智能识别：开始识别任务（写） | - |
| `updateSmartRecRunParams`（mutation） | POST | `/api/v1/ai-smart-rec/run-params` | body | 智能识别：开始识别任务（写） | - |
| `enabledCheckSimilar`（mutation） | POST | `/api/v1/ai-smart-rec/similarity-enabled` | body | 智能识别：相似照片检测开关（写） | - |
| `getAISmartRecStatus` | GET | `/api/v1/ai-smart-rec/status` | params | 智能识别：任务状态 | HTTP 200 / code 0 |
| `unInstallAISmartRecModel`（mutation） | POST | `/api/v1/ai-smart-rec/uninstall` | - | 智能识别：卸载模型（写） | - |
| `updateSmartCategory`（mutation） | POST | `/api/v1/ai-smart-rec/update-smart-category` | - | 智能识别：更新分类（写） | - |
| `enabledVideoRec`（mutation） | POST | `/api/v1/ai-smart-rec/video-enabled` | body | 智能识别：视频识别开关（写） | - |

## v1/album（16）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `getBabyAlbumTimeline` | GET | `/api/v1/album/baby/timeline` | params | 宝宝相册时间线 | 跳过（本次没有可用的 id 参数） |
| `addConditionalAlbum`（mutation） | POST | `/api/v1/album/condition/add` | body | 按条件创建相册（写） | - |
| `getConditionalAlbumList` | GET | `/api/v1/album/condition/list` | params, providesTags | 列表 | HTTP 200 / code 400 invalid params |
| `delConditionalAlbum`（mutation） | POST | `/api/v1/album/condition/remove` | body | 删除 | - |
| `addAlbum`（mutation） | POST | `/api/v1/album/create` | album_name, ids | 创建相册（写） | HTTP 200 / code 0 |
| `delete`（mutation） | POST | `/api/v1/album/delete` | album_id | 删除相册（写） | HTTP 200 / code 0 |
| `downLoadAll` | POST | `/api/v1/album/download/all` | body | 下载整本相册（写：打包任务） | - |
| `getItem` | GET | `/api/v1/album/item` | album_id | 相册里的单张照片 | HTTP 200 / code 0 |
| `getList` | GET | `/api/v1/album/list` | sort_direction, sort_by, offset, limit | 相册列表（分页/排序） | HTTP 200 / code 0 |
| `getAlbumTimeline` | GET | `/api/v1/album/normal/timeline` | startTime, endTime, albumId | 普通相册时间线 | HTTP 200 / code 0 |
| `getAlbumsByPhoto` | GET | `/api/v1/album/photo/belong` | album_id | 某张照片属于哪些相册 | HTTP 200 / code 0 |
| `deletePhotoFromAlbum`（mutation） | POST | `/api/v1/album/photo/remove` | ids, album_id | 删除 | HTTP 200 / code 0 |
| `remove`（mutation） | POST | `/api/v1/album/remove` | body | 删除 | - |
| `updateName`（mutation） | POST | `/api/v1/album/update/name` | album_id, album_name | 更新相册（写） | HTTP 200 / code 0 |
| `updatePoster`（mutation） | POST | `/api/v1/album/update/poster` | album_id, id | 更新相册（写） | - |
| `updateAlbumSetting`（mutation） | POST | `/api/v1/album/update/setting` | albumId, conditionSettings | 更新相册（写） | - |

## v1/album_grant（5）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `cancel` | POST | `/api/v1/album_grant/cancel` | body | 取消相册分享授权（写） | - |
| `create` | POST | `/api/v1/album_grant/create` | body | 分享相册给他人（写） | - |
| `getAlbumGrantListMine` | GET | `/api/v1/album_grant/list_mine` | offset, limit | 我分享出去的相册 | HTTP 200 / code 0 |
| `getAlbumGrantListToMe` | GET | `/api/v1/album_grant/list_to_me` | offset, limit | 别人分享给我的相册 | HTTP 200 / code 0 |
| `update` | POST | `/api/v1/album_grant/update` | body | 更新相册分享授权（写） | - |

## v1/app（1）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `getVersion` | GET | `/api/v1/app/version` | - | 应用版本 | HTTP 200 / code 0 |

## v1/config（2）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `getSetting` | GET | `/api/v1/config/detail` | props, current, keyframes ? | 详情 | HTTP 200 / code 0 |
| `updateSetting`（mutation） | POST | `/api/v1/config/update` | body | 更新 | - |

## v1/explore（3）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `getGeos` | GET | `/api/v1/explore/geos` | params | 按地理位置探索照片 | HTTP 200 / code 0 |
| `getRecentPhotosTimeline` | GET | `/api/v1/explore/recent_timeline` | offset, limit | 最近照片时间线 | HTTP 200 / code 0 |
| `getTags` | GET | `/api/v1/explore/tags` | params | 按标签探索照片 | HTTP 200 / code 0 |

## v1/file（6）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `copyFolderOrFile`（mutation） | POST | `/api/v1/file/copy` | body | 复制文件/文件夹（写） | - |
| `removeFolderOrFile`（mutation） | POST | `/api/v1/file/delete` | body | 删除 | - |
| `moveFolderOrFile`（mutation） | POST | `/api/v1/file/move` | body | 移动文件/文件夹（写） | - |
| `renameFolderOrFile`（mutation） | POST | `/api/v1/file/rename` | body | 重命名文件/文件夹（写） | - |
| `cancelTask`（mutation） | POST | `/api/v1/file/task/cancel` | body | 取消 | - |
| `deleteTask`（mutation） | POST | `/api/v1/file/task/delete` | body | 删除 | - |

## v1/fixer（2）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `reIdentifyMotionPhoto`（mutation） | POST | `/api/v1/fixer/photoType` | - | 修复照片类型识别（写） | - |
| `getReIdentifyMotionPhotoStatus` | GET | `/api/v1/fixer/photoType/status` | - | 修复照片类型识别（写） | HTTP 501 / code None  |

## v1/folder_view（4）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `getFolderPoster` | POST | `/api/v1/folder_view/cover` | body | 设置文件夹封面（写） | - |
| `setFolderPoster`（mutation） | POST | `/api/v1/folder_view/cover/setting` | body | 设置文件夹封面（写） | - |
| `getFileList` | GET | `/api/v1/folder_view/getFileList` | params | 文件视图：列文件 | HTTP 200 / code 0 |
| `getFolderList` | GET | `/api/v1/folder_view/getFolderList` | params | 文件视图：列文件夹 | HTTP 200 / code 4023 Does not exist or no permission |

## v1/gallery（4）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `addPhoto`（mutation） | POST | `/api/v1/gallery/addTo/album` | ids, album_id, album_name, albumId | 把照片加进相册（写） | HTTP 200 / code 0 |
| `getList` | GET | `/api/v1/gallery/getList` | start_time, end_time, limit, offset, mode | 照片列表（分页） | HTTP 200 / code 0 |
| `getOne` | GET | `/api/v1/gallery/getOne` | id | 单张照片详情 | HTTP 200 / code 0 |
| `getTimeline` | GET | `/api/v1/gallery/timeline` | offset, limit | 照片时间线（按月/日分桶） | HTTP 200 / code 0 |

## v1/google_takeout（3）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `heartBeat`（mutation） | POST | `/api/v1/google_takeout/heartbeat` | taskId | Google Takeout 导入：心跳 | - |
| `noticeGoogleTakeoutUploaded`（mutation） | POST | `/api/v1/google_takeout/notice` | folderPath, taskId | Google Takeout 导入：进度通知 | - |
| `prepareGoogleTakeout`（mutation） | POST | `/api/v1/google_takeout/prepare` | ids, queryCb, id, albumId, name, to, params, personId ? | Google Takeout 导入：准备（写） | - |

## v1/maintain（1）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `executeFixTask`（mutation） | POST | `/api/v1/maintain/task/${e.taskType}` | body | 维护任务（按 taskType 拼路径，写） | - |

## v1/map（3）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `getCenter` | GET | `/api/v1/map/preview/initCenter` | - | 地图初始中心点 | HTTP 200 / code 0 |
| `getBoundary` | GET | `/api/v1/map/preview/mapBoundary` | - | 地图可视范围边界 | HTTP 200 / code 0 |
| `getTimeline` | GET | `/api/v1/map/timeLine` | params | 地图模式时间线 | HTTP 200 / code 400 invalid params |

## v1/media_category（1）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `getMediaCategories` | GET | `/api/v1/media_category/list` | offset, limit | 列表 | HTTP 200 / code 0 |

## v1/photo（9）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `addScanFolder`（mutation） | POST | `/api/v1/photo/folder/add` | folder_path, is_default | 添加照片文件夹（写） | - |
| `getBackupLocation` | GET | `/api/v1/photo/folder/defaultInit` | to ? | 默认照片文件夹初始化 | HTTP 200 / code 0 |
| `getSelectedFolderList` | GET | `/api/v1/photo/folder/list` | offset, limit | 列表 | HTTP 200 / code 0 |
| `addNewFolder`（mutation） | POST | `/api/v1/photo/folder/new` | to ? | 新建照片文件夹（写） | - |
| `reConnectFolder`（mutation） | POST | `/api/v1/photo/folder/reconnect` | body | 重新连接照片文件夹（写） | - |
| `delScanFolder`（mutation） | POST | `/api/v1/photo/folder/remove` | folder_id | 删除 | - |
| `getSelectedFolderManage` | GET | `/api/v1/photo/folder/view` | - | 照片文件夹视图 | HTTP 200 / code 0 |
| `getUploadSupportList` | GET | `/api/v1/photo/support/list` | offset, limit | 列表 | HTTP 200 / code 0 |
| `getUploadPath` | GET | `/api/v1/photo/upload/path` | - | 取上传路径（v1） | HTTP 200 / code 0 |

## v1/preview（5）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `addTag`（mutation） | POST | `/api/v1/preview/tag/add` | tag_name, tagName | 新建照片标签（写） | - |
| `addForPhoto`（mutation） | POST | `/api/v1/preview/tag/addForPhoto` | ids, tag_ids | 新建照片标签（写） | - |
| `delForPhoto`（mutation） | POST | `/api/v1/preview/tag/delForPhoto` | ids, tag_ids | 去掉照片标签（写） | - |
| `updateDateTime`（mutation） | POST | `/api/v1/preview/update/dateTime` | ids, date_time, time_zone_offset, dateTime, timeZoneOffset | 修改照片拍摄时间（写） | - |
| `updateGeo`（mutation） | POST | `/api/v1/preview/update/geo` | ids, latitude, longitude, poiId | 修改照片地理位置（写） | - |

## v1/recycle-bin（5）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `addToRecycleBin`（mutation） | POST | `/api/v1/recycle-bin/add` | ids | 移入回收站（写） | - |
| `cleanAll`（mutation） | POST | `/api/v1/recycle-bin/clean-all` | ids ? | 清空回收站（写，不可恢复） | - |
| `deleteFromRecycleBin`（mutation） | POST | `/api/v1/recycle-bin/delete` | ids | 删除 | - |
| `restoreFromRecycleBin`（mutation） | POST | `/api/v1/recycle-bin/restore` | ids | 从回收站还原（写） | - |
| `getTimeline` | GET | `/api/v1/recycle-bin/timeline` | offset, limit | 回收站时间线 | HTTP 200 / code 0 |

## v1/repeat-photo（4）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `startCheckSimilar`（mutation） | POST | `/api/v1/repeat-photo/check` | checkSimilarity | 重复照片检测（写） | - |
| `excludePhoto`（mutation） | POST | `/api/v1/repeat-photo/exclude` | type, photoIds, groupId | 重复照片：排除某些（写） | - |
| `keepPhoto`（mutation） | POST | `/api/v1/repeat-photo/keep` | photoId | 重复照片：保留某张（写） | - |
| `mergePhotos`（mutation） | POST | `/api/v1/repeat-photo/merge` | type, groupId | 重复照片：合并（写） | - |

## v1/search（2）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `searchIndex` | GET | `/api/v1/search/index` | - | 重建搜索索引（写） | HTTP 200 / code 0 |
| `searchIndexStatus` | GET | `/api/v1/search/index/status` | - | 重建搜索索引（写） | HTTP 200 / code 4016 Index is rebuilding, please do not repeat operation |

## v1/server（6）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `getArchitecture` | GET | `/api/v1/server/architecture` | props, current, keyframes ? | 设备架构 | HTTP 200 / code 0 |
| `getTargetSelectedFolder`（mutation） | POST | `/api/v1/server/file_list` | body | 列文件（POST 形式） | - |
| `getServerFolderManage` | GET | `/api/v1/server/folder_manage` | ids | 可管理的文件夹列表 | HTTP 200 / code 0 |
| `getSeverSysInfo` | GET | `/api/v1/server/sys_info` | - | 系统信息 | HTTP 200 / code 0 |
| `getUsersGroupAll` | GET | `/api/v1/server/user_group_all` | - | 全部用户组 | HTTP 200 / code 0 |
| `getUsersAll` | GET | `/api/v1/server/users_all` | - | 全部用户 | HTTP 200 / code 0 |

## v1/share_link（6）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `cleanupInvalidLink`（mutation） | POST | `/api/v1/share_link/cleanupInvalid` | to ? | 清理失效的分享链接（写） | - |
| `removeLink`（mutation） | POST | `/api/v1/share_link/delete` | ids | 删除 | - |
| `getShareLinkDetail` | GET | `/api/v1/share_link/detail` | params | 详情 | 跳过（本次没有可用的 id 参数） |
| `getShareLinkList` | GET | `/api/v1/share_link/list` | params | 列表 | HTTP 200 / code 0 |
| `createShareLink`（mutation） | POST | `/api/v1/share_link/new` | body | 新建分享链接（写） | - |
| `updateShareLink`（mutation） | POST | `/api/v1/share_link/update` | body | 更新 | - |

## v1/sys_config（6）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `getSysConfig` | GET | `/api/v1/sys_config/list` | offset, limit | 列表 | HTTP 200 / code 0 |
| `updateSysConfig`（mutation） | POST | `/api/v1/sys_config/setting` | ids | 系统设置写入（写） | - |
| `getTimezoneList` | GET | `/api/v1/sys_config/time_zone/support` | - | 支持的时区列表 | HTTP 200 / code 0 |
| `getVideoDecodeConfig` | GET | `/api/v1/sys_config/video_decode` | - | 视频解码配置 | HTTP 200 / code 0 |
| `setVideoDecodeConfig`（mutation） | POST | `/api/v1/sys_config/video_decode` | allowGpuDecoding, selectedGpuSequence, allowCpuDecoding | 视频解码配置 | - |
| `getVideoDecodeGPUList` | GET | `/api/v1/sys_config/video_decode/list_gpu` | offset, limit | 视频解码配置 | HTTP 200 / code 0 |

## v1/task-panel（3）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `getErrorTaskList` | GET | `/api/v1/task-panel/fail` | params | 失败任务列表 | 跳过（本次没有可用的 id 参数） |
| `detSingleFace`（mutation） | POST | `/api/v1/task-panel/retry-one` | id, taskId, taskType | 重试单个任务（写） | - |
| `skipSingleFace`（mutation） | POST | `/api/v1/task-panel/skip-one` | id, taskId, taskType | 跳过单个任务（写） | - |

## v1/thumbnail（2）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `refreshThumbnail`（mutation） | POST | `/api/v1/thumbnail/refresh` | ids | 刷新缩略图（写） | - |
| `getThumbnailStatus` | GET | `/api/v1/thumbnail/status` | ids | 缩略图任务状态 | HTTP 200 / code 0 |

## v1/user（1）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `getCurrentUser` | GET | `/api/v1/user/info` | - | 当前用户信息 | HTTP 200 / code 0 |

## v1/user_photo（1）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `getStat` | GET | `/api/v1/user_photo/stat` | params | 照片统计（数量/占用） | HTTP 200 / code 0 |

## v1/video（3）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `getDecodeInfo` | GET | `/api/v1/video/decode/info` | id | 视频解码信息 | HTTP 200 / code 0 |
| `playVideo`（mutation） | POST | `/api/v1/video/decode/play` | id, bitrate, resolution, audioIndex, audioEncoder, videoEncoder, channels | 视频播放地址（写：会创建转码任务） | - |
| `updateQuality`（mutation） | POST | `/api/v1/video/decode/quality` | id, bitrate, playLink, resolution, startTimestamp | 切换视频清晰度（写） | - |

## v2/photo（1）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `getUploadPathV2` | GET | `/api/v2/photo/upload/path` | - | 取上传路径（v1） | HTTP 200 / code 0 |

## v2/search（1）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `searchResults` | POST | `/api/v2/search/results` | body | 接口 search/results | - |

## v2/server（1）

| 端点名 | 方法 | 路径 | 参数/请求体（挖到的字段） | 用途 | 实测 |
|--------|------|------|------------------------|------|------|
| `getPools` | GET | `/api/v2/server/pools` | - | 接口 server/pools | HTTP 200 / code 0 |
