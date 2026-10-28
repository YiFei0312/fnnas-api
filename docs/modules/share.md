# 分享（分享链接）

- 需要登录：是
- 需要签名：是
- 参数封装：**这一族接口的参数必须包在 `data` 里**（平铺会报 `errno 3000001 Invalid Params`）
- 实测状态：2026-01 在真机（fnOS 1.2.0800，`demoNAS`）上用 `/vol1/1000/tmp` 里的文件
  跑通了「创建 → 列表 → 详情 → 修改 → 打开链接 → 删除」全流程，原始报文见
  `data/share_probe.json`，一键复跑：`python tools/probe_share.py --yes`

飞牛有两套「分享」接口，别混：

| 接口族 | 用途 | 状态 |
|--------|------|------|
| `appcgi.sharesvr.share.link.*` | **公开分享链接**：给别人一个 `http://<NAS>:5666/s/<id>`（可设提取码/有效期/次数） | 本文档，已全链路实测 ✅ |
| `file.share.*` | 旧版按路径的分享接口（`info`/`del2` 还认 `path`，`add2` 参数未测通） | 见文末「旧接口」 |

---

## 1. 列表 `appcgi.sharesvr.share.link.list`

**请求示例**（注意 `data` 这一层）

```json
{sign}{"reqid":"reqid","data":{"page":1,"pageSize":100,"keyword":"","isAdmin":false,"type":0,"sortColumn":"createdTime","sortType":"DESC"},"req":"appcgi.sharesvr.share.link.list"}
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `data.page` | number | 页码，从 1 开始 |
| `data.pageSize` | number | 每页条数 |
| `data.keyword` | string | 按分享名称搜索；也可以直接粘贴分享地址（服务端会从 `/s/xxx` 里解析出 id） |
| `data.isAdmin` | boolean | 管理员视角：`true` 时能看全部用户的分享 |
| `data.type` | number | `0` = 全部，`1` = 分享链接，`4` = 文件收集（上传请求） |
| `data.sortColumn` | string | 排序字段，如 `createdTime` |
| `data.sortType` | string | `DESC` / `ASC` |

**响应示例**（没有分享时 `list` 是 `null` 而不是 `[]`）

```json
{
  "result": "succ",
  "data": {
    "total": 1,
    "list": [
      {
        "id": "c55bd4d2b4e5404a90",   // 分享 ID，就是 /s/<id>
        "name": "apitest-share",      // 分享名称（分享页标题）
        "maxAccess": 0,               // 可访问次数上限，0=不限
        "access": 0,                  // 已访问次数
        "validTo": 0,                 // 失效时间（秒级时间戳），0=永久
        "passwd": "",                 // 提取码（明文返回！）
        "uid": 1000,                  // 创建者 uid
        "type": 1,                    // 1=分享链接，4=文件收集
        "status": "valid",            // valid / invalid
        "accessStatus": "valid",      // valid / expired / exceed
        "createdTime": 1792168641874, // 创建时间（毫秒！比 validTo 多 3 位）
        "uploadConfig": {"path": "", "desc": "", "fileSizeLimit": 0, "fileType": ""}
      }
    ]
  },
  "reqid": "reqid"
}
```

## 2. 详情 `appcgi.sharesvr.share.link.get`

```json
{sign}{"reqid":"reqid","data":{"id":"c55bd4d2b4e5404a90"},"req":"appcgi.sharesvr.share.link.get"}
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `data.id` | string | 分享 ID，**必须是字符串**（传数字直接报 Invalid Params） |

比列表多一个 `files` 字段，说明这条分享分享了什么：

```json
"files": [
  {"path": "/vol1/1000/tmp", "file": "20260127_195353.jpg", "isDir": 0}
]
```

> `path` 是**所在目录**，`file` 才是文件名；分享目录时 `path` 是上级目录、`isDir` 为 `1`
> （实测分享 `/vol1/1000/tmp` 目录返回 `{"path":"/vol1/1000","file":"tmp","isDir":1}`）。
> 不存在的 id 返回 `{"result":"fail","errno":3000006,"errmsg":"Not Found Error"}`。

## 3. 创建 `appcgi.sharesvr.share.link.create`

**请求示例**（带提取码 + 1 小时有效 + 限 3 次）

```json
{sign}{"reqid":"reqid","data":{"name":"apitest-pwd","files":["/vol1/1000/tmp/20260127_195353.jpg"],"maxAccess":3,"passwd":"apitest123","validTo":1792172307},"req":"appcgi.sharesvr.share.link.create"}
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `data.name` | string | 分享名称（会显示在分享页标题上） |
| `data.files` | string[] | 要分享的路径数组，**以 `/` 开头的绝对路径**（如 `/vol1/1000/tmp/a.jpg`），可多个 |
| `data.maxAccess` | number | 可访问次数，`0` = 不限 |
| `data.passwd` | string | 提取码；**不设就整个字段不传**（传 `""` 也算不设） |
| `data.validTo` | number | 失效时间（**秒级**时间戳）；不传 = 永久有效 |
| `data.type` | number | 不传默认 `1`（分享链接）；`4` = 文件收集，要配合 `uploadConfig` |
| `data.uploadConfig` | object | 文件收集配置：`{desc, fileType, path, fileSizeLimit}` |

**响应示例**：直接返回这条分享的完整信息（结构同列表里的元素，`id` 就在这里）

```json
{
  "result": "succ",
  "data": {
    "id": "5218712898484821a6", "name": "apitest-pwd", "maxAccess": 3, "access": 0,
    "validTo": 1792172307, "passwd": "apitest123", "uid": 1000, "type": 1,
    "status": "valid", "accessStatus": "valid", "createdTime": 1792168708398,
    "uploadConfig": {"path": "", "desc": "", "fileSizeLimit": 0, "fileType": ""}
  },
  "reqid": "reqid"
}
```

> ⚠️ **`passwd` 是明文返回的**，接口不做脱敏。别把响应体整段写进日志或贴给别人。
>
> 分享地址 = `http://<NAS>:5666/s/<id>`，实测 HTTP 200，页面标题就是分享名称；
> 它不需要 NAS 账号即可打开（虽然 WebSocket 接口本身要登录）。
> 域名前缀可以先用 `appcgi.sharesvr.share.link.default.get` 拿 `fnDefault`。

## 4. 修改 `appcgi.sharesvr.share.link.update`

```json
{sign}{"reqid":"reqid","data":{"id":"5218712898484821a6","name":"apitest-share-edit","maxAccess":0,"validTo":0},"req":"appcgi.sharesvr.share.link.update"}
```

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `data.id` | string | 要改的分享 ID（必填） |
| `data.name` | string | 新名称 |
| `data.maxAccess` | number | 新的可访问次数，`0` = 不限 |
| `data.passwd` | string | 新提取码 |
| `data.validTo` | number | 新的失效时间（秒级时间戳），`0` = 改成永久 |

响应是修改后的完整分享信息。**只传要改的字段**即可（实测只传
`{"id","name","maxAccess"}` 也能成功，未传的字段保持原值）。

## 5. 删除 `appcgi.sharesvr.share.link.remove` / 清空 `...clear`

```json
{sign}{"reqid":"reqid","data":{"idList":["5218712898484821a6","9e4cf6a5ee1e4a9783"]},"req":"appcgi.sharesvr.share.link.remove"}
```

响应（逐条报告失败项，方便重试）：

```json
{"result":"succ","data":{"failedCount":0,"failedIdList":[]},"reqid":"reqid"}
```

清空用 `appcgi.sharesvr.share.link.clear`，参数 `{"isAdmin": false}`（管理员传 `true`
可清全部用户的分享），返回 `{"clear": 删除条数}`。

## 6. 权限与默认配置

| 接口 | 参数 | 响应 | 说明 |
|------|------|------|------|
| `appcgi.sharesvr.share.permission.get` | 无 | `{"mode":"all"}` | 谁能创建分享链接 |
| `appcgi.sharesvr.share.permission.set` | `{"mode":"all\|admin"}` | 同 get | 写操作 |
| `appcgi.sharesvr.share.uploadpermission.get` | 无 | `{"mode":"admin"}` | 分享里谁能上传 |
| `appcgi.sharesvr.share.uploadpermission.set` | `{"mode":"..."}` | 同 get | 写操作 |
| `appcgi.sharesvr.share.link.default.get` | 无 | 见下 | 分享地址域名模式与限速 |
| `appcgi.sharesvr.share.link.default.set` | `{mode,customize,rateLimit}` | 同 get | 写操作 |

```json
{
  "mode": "default",                 // default=用默认地址；customize=自定义域名
  "ddns": "",                        // DDNS 域名
  "customize": {"protocol": "", "domain": "", "port": "", "host": ""},
  "fnDefault": "http://192.168.1.11:5666",   // 默认分享地址前缀
  "rateLimit": {"upload": 0, "download": 0}    // 限速，0=不限
}
```

> 带参接口（`list/get/create/update/remove/clear` 和两个 `set`）记得包 `data`。

---

## Python SDK 用法

```python
from sdk import FnOsClient

client = FnOsClient(ping_interval=60)
await client.connect('ws://192.168.1.10:5666/websocket?type=main')
await client.login('demo-user', '密码')

# 创建（passwd/valid_to 不传就是不设）
share = await client.share_link_create('/vol1/1000/tmp/20260127_195353.jpg',
                                       name='给同事的照片', passwd='1234',
                                       max_access=10, valid_to=1792172307)
print(client.share_url(share['id']))       # http://<NAS>:5666/s/<id>

# 查 / 改 / 删
await client.share_links(keyword='照片')                      # {"total": n, "list": [...]}
await client.share_link(share['id'])                          # 详情（含 files）
await client.share_link_update(share['id'], name='改名', valid_to=0)   # 改成永久
await client.share_link_remove(share['id'])                   # 返回 failedIdList

# 直接调底层接口也可以（nested=True 就是包 data）
await client.call('appcgi.sharesvr.share.link.list',
                  {'page': 1, 'pageSize': 100}, nested=True)
```

- `client.api.appcgi.sharesvr.share_link_list(data={...})` 这种自动生成的封装是**平铺**发参的，
  分享这一族要用上面的高层方法，或者自己加 `nested=True`。
- 懒得判断封装方式时用 `await client.call_auto(req, params)`，它会自动试并记住结果。

## 一键复跑实测

```bash
python tools/probe_share.py              # dry-run：只打印计划
python tools/probe_share.py --yes        # 真正创建 1 条测试分享，跑完自动删除
python tools/probe_share.py --yes --keep --path /vol1/1000/tmp   # 保留下来手工看
```

脚本只操作 `--path`（默认 `/vol1/1000/tmp`）里的文件，测完会删掉自己创建的分享并复查
`total == 0`；实测结论会合并进 `data/probe_status.json`，完整调用日志（含原始报文）写到
`data/share_probe.json`。

---

## 旧接口：`file.share.*`

这一族按**路径**操作，当前版本的 Web UI 已经不用它了（UI 走 `appcgi.sharesvr.share.link.*`），
实测结论如下，封装时别踩坑：

| 接口 | 实测行为 |
|------|---------|
| `file.share.list` | 无分享时只返回 `{"result":"succ"}`；有分享时字段未知（本机没有旧版分享可测） |
| `file.share.listOthers` | 只返回 `{"uver":117436739026944,"result":"succ"}`（`uver` 是目录版本号） |
| `file.share.info` | 只认**平铺**的 `path`（传 `/vol1/1000/tmp` 这种不带前导斜杠的路径）；没有分享时只回 `uver`；传假 `token` 报 `errno 135168` |
| `file.share.del2` | 认 `path`，**幂等**：即使该路径没有分享也返回 `succ` |
| `file.share.add` | `errno 10000002`，**接口不存在** |
| `file.share.add2` | 认 `path` 和 `shareName`：少参数报 `8192`、`shareName` 空报 `4101`、非空报 `4112`；还缺别的必填字段（试过 `uid/users/files/type/mode/...` 都不行），**没测通，别用** |

> 结论：要分享就用 `appcgi.sharesvr.share.link.*`。
