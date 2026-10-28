# 文件管理

- 需要登录：是
- 需要签名：是
- 参数外壳：**平铺**（参数直接放在报文根上，不用包 `data`）
- 实测状态：2026-01 在真机（fnOS 1.2.0800，`demoNAS`）上用 `/vol1/1000/tmp` 跑通了
  只读 → 上传 → 复制/改名/移动 → 压缩/解压 → 权限 → 回收站 → 删除的完整链路，
  全程只在自己新建的临时目录里操作，原文件 `size/mtim/btim` 未变
  （复现：`python tools/probe_file.py --yes`，日志 `data/file_probe.json`）

## ⚠️ 两条最容易踩的协议级结论

### 1. 写接口是**异步任务**：接口只回 ack，成败看推送

`file.cp` / `file.mv` / `file.rm` / `file.compress` / `file.extract` / `file.setAcl2` /
`file.chown` / `file.usage` 这些接口的 WebSocket 返回值**只是「任务已受理」**：

```jsonc
// 发请求
{"req":"file.cp","reqid":"6ad274126ad2741000000336002e",
 "files":["/vol1/1000/tmp/a.jpg"],"pathTo":"/vol1/1000/tmp/dst","overwrite":1,
 "details":{"name":"a.jpg","count":1}}

// 立刻返回（注意：没有 result，只有 taskId）
{"sysNotify":"taskId","taskId":"OdkhlbCaRg+61xHFGLc29w==","reqid":"6ad274126ad2741000000336002e"}

// 随后是**同 reqid** 的推送：任务回显 → 进度 → 最终结果
{"sysNotify":"taskInfo","taskInfo":{"req":"file.cp","reqid":"…002e","pathTo":"…/dst", …}}
{"percent":100,"time":0,"speed":0,"size":1880200,"sizeTotal":1880200,"reqid":"…002e"}
{"result":"succ","reqid":"…002e"}
```

失败时长这样（实测：源文件不存在时，**ack 依然是 succ**，只有推送才是 fail）：

```json
{"result":"fail","reqid":"…0032","failedFilesCount":1,
 "failedFiles":[{"file":"/vol1/1000/tmp/dst/renamed.jpg","errno":4100}]}
```

> 所以「发了写接口 + 返回没报错」**不等于成功**。SDK 里用
> `sdk/filetasks.py` 的 `wait_file_task()` 等这个推送：

```python
from sdk import wait_file_task, is_task_ok

resp = await client.file_cp('/vol1/1000/tmp/a.jpg', '/vol1/1000/tmp/dst')
result = await wait_file_task(client, resp['reqid'])      # None = 超时
assert is_task_ok(result), result
```

> 同步接口只有少数：`file.rename`（出错直接回 `errno`）、`file.mkdir`、
> 只读那一批。`file.calc` 小目录会**同步**返回 `fileCount/dirCount/fileSizeTotal/space`，
> 前端同时支持订阅进度推送。

### 2. 参数名别猜：批量接口是 `files` 数组，`file.size` 是 `file`

实测（前端产物 `data/web-cache/assets/index-B0cXg_s1.js` 的接口映射 + 真机验证）：

| 接口 | ✅ 实测可用 | ❌ 常见错误写法（报 `errno 8192`） |
|------|------------|--------------------------------|
| `file.prop` | `{"files":["/a.jpg","/b.jpg"]}` | `{"path":"/a.jpg"}` |
| `file.access` | `{"files":["/a.jpg"]}` | `{"path":"/a.jpg"}` |
| `file.calc` | `{"files":["/a.jpg"]}` | `{"path":"/a.jpg"}` |
| `file.size` | `{"file":"/a.jpg"}` | `{"path":…}`、`{"files":[…]}`、`{"paths":[…]}` |
| `file.cp` / `file.mv` | `{"files":[…],"pathTo":"目标目录","overwrite":1,"details":{…}}` | `{"src":…,"dst":…}` |
| `file.chown` | `{"files":[…],"uid":1000,"gid":1000}` | `{"path":…,"uid":…}` |
| `file.getAcl` | `{"path":"/a.jpg","getProp":true}` | — |

`overwrite` 的取值（上传/复制/移动通用）：`0` = 跳过同名、`1` = 覆盖、`2` = 保留两者。

> `pathTo` 是**目标目录**，不是新文件名；复制过去保持原文件名
> （实测 `cp a.jpg → /tmp/dst/` 得到 `/tmp/dst/a.jpg`，想改名再调 `file.rename`）。

## 参数总表（实测）

`path` 类参数：`file.ls` / `file.lsDir` 用 `vol{存储ID}/{用户ID}/子路径`
（实测带前导斜杠 `/vol1/1000/tmp` 也能列同一目录）；其余接口用 `/vol1/1000/sample` 绝对路径。

| 接口 | 参数 | 返回 / 说明 |
|------|------|------------|
| `file.ls` | `{path}` | `{files:[{name,uid,size,mtim,btim,dir?,v?}], uver}`，**成功时没有 result 字段** |
| `file.lsDir` | `{path}` | 精简版列表 |
| `file.prop` | `{files:string[]}` | `{prop:[{uid,size,space,mtim,btim,dir?}]}`；不存在的路径**外层仍 succ**，条目里 `errno:4100` |
| `file.size` | `{file}` | `{size, space}`（单文件/目录） |
| `file.calc` | `{files:string[]}` | `{fileSizeTotal, space, fileCount, dirCount}`（大目录会异步推送进度） |
| `file.access` | `{files:string[]}` | `{access:[位掩码]}`，`access[0] & 6` 非 0 = 可读写 |
| `file.getAcl` | `{path, getProp?}` | `{permset:[…], defaultPermset:[…]}` |
| `file.download` | `{files:string[]}` | `{download:[{uri}]}`，uri 是带签名的 HTTP 地址，GET 下来字节数与原文件一致 |
| `file.fav.list` / `add` / `del` | `{}` / `{path}` / `{path}` | `{fav:[…]}`；增删会推 `sysNotify=fileFav` |
| `file.recent.list` / `add` / `del` / `clear` | `{}` / `{path}` / `{path:string[]}` / `{}` | 注意 **del 是数组**，fav 的 del 是单值 |
| `file.trash.list` | `{}`、`{uid}`，或 `{path}` | 见下面「回收站」一节 |
| `file.mkdir` | `{path}` | 新建文件夹（含新目录名） |
| `file.rename` | `{path, newName}` | 同步接口，失败直接回 errno（4100 = 路径不存在） |
| `file.rm` | `{files:string[], moveToTrashbin, details}` | 异步任务；`details={name,count,dir}` 只影响任务中心显示 |
| `file.cp` / `file.mv` | `{files,pathTo,overwrite,details}` | 异步任务 |
| `file.compress` | `{description,path,files,level,passwd?,details}` | 异步任务；`path` = 输出压缩包全路径 |
| `file.extract` | `{description,path,file,overwrite,details}` | 异步任务；`path` = 输出目录 |
| `file.setAcl2` | `{files,permset,details,sub?}` | 异步任务；`sub:1` 连带子目录 |
| `file.chown` | `{files,uid,gid}` | 异步任务 |
| `file.checkUpload` | `{size,path,overwrite?}` | 返回 `uploadName`（形如 `upload.txt.~#0`），HTTP 上传要用 |
| `file.usage` | `{}` | 异步任务：回 `taskId`，分类用量（app/docker/vm/iscsi/…）靠推送回 |
| `file.team.lsDir` | `{}` | 本机没有团队空间，只回 `uver` |
| `file.cancel` | ❓ | 实测 `taskId` / `taskIds` / `id` 都报 `8192`，**参数形态未确认** |
| `file.trimacl.conv` / `.report` | ❓ | 同上，`path` / `files` / `taskId` 都报 `8192`，前端也没调用 |
| `file.setAcl` | — | 实测 `errno 10000002`：**接口不存在**，用 `file.setAcl2` |

## 上传：真正的上传走 HTTP，不是 WebSocket

```
① WS  file.checkUpload {size, path, overwrite}  →  {uploadName:"upload.txt.~#0", …}
② HTTP POST http://<NAS>:5666/upload
        headers: Trim-Token / Trim-Sign / Trim-Mtim / Trim-Overwrite / Trim-Path
        body:    multipart/form-data，字段名 trim-upload-file
③ 服务端按 uploadName 落盘，file.ls / file.prop 立刻能查到
```

`Trim-Sign` 是对 `Trim-Path`（`<目标目录>/<uploadName>`）做签名，和 WS 签名同一套 key。
`Trim-Overwrite` 与 `checkUpload` 的 `overwrite` 一致（0 跳过 / 1 覆盖 / 2 保留两者）。
SDK 里 `client.upload(local, nas_path, overwrite)` 已封好（内部用 `requests`；
如果环境里没有 `requests`，可参考 `tools/probe_file.py:_upload()` 用标准库 `urllib` 自己拼）。

## 下载：拿签名 URL 再 GET

```python
items = await client.file_download('/vol1/1000/tmp/a.jpg')
url = client.base_url + items[0]['uri']     # /download//vol1/1000/tmp/a.jpg?t=…&sign=…
```

实测 `uri` 直接 GET 就能下到完整文件（`file.prop` 的 size 与下载字节数一致）。

## 收藏 / 最近访问

```json
// 加收藏（会推 sysNotify=fileFav）
{"req":"file.fav.add","reqid":"…","path":"/vol1/1000/tmp"}
// 取消收藏（一次一个）
{"req":"file.fav.del","reqid":"…","path":"/vol1/1000/tmp"}
// 最近访问：加是单值，删是数组 ← 容易写错
{"req":"file.recent.add","reqid":"…","path":"/vol1/1000/tmp/a.jpg"}
{"req":"file.recent.del","reqid":"…","path":["/vol1/1000/tmp/a.jpg"]}
{"req":"file.recent.clear","reqid":"…"}
```

## 回收站：能删进去，但**还原的路径形态没确认**

实测结论（别踩）：

| 调用 | 结果 |
|------|------|
| `file.rm {files:[x], moveToTrashbin:true}` | 任务 `succ`，文件从原位置消失 ✅ |
| `file.trash.list {}` / `{uid:1000}` | 返回**顶层**回收站条目（本机 10 条），字段 `{name,v,uid,mtim,btim,dir,rmUid,rmTime}` |
| `file.trash.list {path:"/vol1/1000/tmp"}` | 行为等同**列目录**（返回的是活文件，字段里没有 `rmTime`）——不是「浏览该目录的回收站」 |
| `file.trash.list {key:"xxx", type:"trash-search"}` | 关键字没生效，仍返回顶层列表 |
| `file.trash.restore {files:[原路径], overwrite:1}` | ack `succ`、任务推送也 `succ`，但**文件没有回到原位置**；`files` 应该传的「回收站内部路径」在 `file.trash.list` 里拿不到 → **未确认，别依赖** |
| `file.trash.clear` | 会清空回收站（可能波及别人的条目）→ **没测** |

> 所以「删到回收站」在 API 上是单向的：能进去，暂时不知道怎么用接口捞回来
> （Web UI 里可以还原/清空）。实测脚本因此只用 21 字节的小文件试回收站。

## 常见错误码

| errno | 含义 | 出现场景 |
|-------|------|---------|
| `8192` | 参数不合法（缺参数 / 参数名不对） | `file.size` 传 `path`、`file.cancel` 的未知参数 |
| `4100` | 路径不存在 | `file.rename` 源路径不在、`file.prop` 结果条目里 |
| `10000002` | 接口不存在 | `file.setAcl` |
| `65535` | 服务端命令执行失败 | 解压时传了空 `fromCharset` → `Too short switch: -fromcharset` |
| `4386` | 上传相关（前端会据此中止任务） | 上传流程 |

## Python SDK 用法

```python
from sdk import FnOsClient, wait_file_task, is_task_ok

client = FnOsClient(ping_interval=60)
await client.connect('ws://192.168.1.10:5666/websocket?type=main')
await client.login('demo-user', '密码')

# 只读
files  = (await client.api.file.ls(path='/vol1/1000/tmp'))['files']
props  = await client.file_prop('/vol1/1000/tmp/a.jpg')        # → prop 数组
size   = await client.file_size('/vol1/1000/tmp')              # → {size, space}
calc   = await client.file_calc('/vol1/1000/tmp')              # → 文件数/目录数/占用
access = await client.file_access('/vol1/1000/tmp/a.jpg')      # → [位掩码]
acl    = await client.file_acl('/vol1/1000/tmp/a.jpg')
urls   = await client.file_download('/vol1/1000/tmp/a.jpg')    # → [{uri}]

# 写操作：拿到 reqid，等任务结果
resp   = await client.file_cp('/vol1/1000/tmp/a.jpg', '/vol1/1000/tmp/dst')
result = await wait_file_task(client, resp['reqid'])
print(is_task_ok(result), result)

await client.file_rename('/vol1/1000/tmp/dst/a.jpg', 'b.jpg')          # 同步
await client.file_compress('/vol1/1000/tmp/dst/b.jpg', '/vol1/1000/tmp/b.zip')
await client.file_extract('/vol1/1000/tmp/b.zip', '/vol1/1000/tmp/out')
await client.file_rm('/vol1/1000/tmp/dst', move_to_trashbin=False)     # 直接删
```

`client.api.*` 那套自动生成的封装是**平铺发参**的，参数名以本文档为准；
不确定时用 `await client.api.call('file.prop', {'files': [...]})`。

## 复现实测

```bash
python tools/probe_file.py            # dry-run：只打印计划
python tools/probe_file.py --yes      # 真跑（自己建临时目录，测完删掉并核对目录复原）
python tools/probe_file.py --yes --keep   # 保留临时目录，手工看
```

脚本保证：只动 `<--path>/fnapi_filetest_<时间戳>/` 里的东西；删除前校验路径前缀；
结束复查 `--path` 列表与开始时逐项一致、原文件 `size/mtim/btim` 未变。
唯一残留：一个 21 字节的测试文件在回收站里（原因见上）。
