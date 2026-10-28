# WebSocket 通信协议说明

本节说明 fnOS 的 WebSocket 通信格式、字段定义、心跳机制等。

## 基础结构

### 请求格式
```json
{
  "reqid": "uuid",
  "req": "模块.动作",
  "data": {},
  "any": "any"
}
```
> ⚠️ 参数**不一定**放在 `data` 里。`file.*` / `stor.*` / `user.*` 是把参数平铺在根上
> （`{"req":"file.ls","reqid":"...","path":"vol1/1000"}`）；而 `appcgi.sharesvr.*` 这类
> 模块的参数**必须**放进 `data`（`{"req":"...","data":{"page":1}}`），平铺会报
> `errno 3000001 Invalid Params`。详见下面「请求参数放在哪里」一节。

### 响应格式

```json
{
  "reqid": "uuid",
  "req": "模块.动作",
  "result": "succ",
  "rev": "0.1",
  "data": {},
  "errno": null,
  "any": "any"
}
```
> Tips：在后面的模块中，可选字段和通用没有写出，但可能返回。

| 字段      | 类型     | 说明                                   |
| ------- | ------ | ------------------------------------ |
| `reqid` | string | 客户端生成的唯一请求 ID，用于匹配响应                 |
| `req`   | string | 命令字符串，如 `"auth.login"`、`"file.list"` |
| `data`  | object | 请求参数体(可选)                                |
| `result`   | string | 错误或提示信息                              |
| `data`  | object | 响应数据体(可选)                                |
| `errno`  | int |  错误码，失败时返回(可选)   |
| `any`  | any | 其他业务数据(查看具体接口)                                |


## 鉴权与签名机制

**部分接口需要签名验证，请求示例：**

```
{sign}{"req":"user.info","reqid":"uuid"}
```

**签名算法**

 > 签名使用 **HMAC-SHA256** 算法，密钥由登录接口返回的`secret`AES解密后得到。

**签名步骤说明**

 - 1、将请求体（字典）转换为 JSON 字符串，无空格、无换行；
 - 2、使用 AES 解密后的密钥对 JSON 字符串进行 HMAC-SHA256 计算；
 - 3、将计算结果再进行 Base64 编码，得到最终签名字符串；
 - 4、在请求数据前拼接签名字符串后再发送。

**Python实现示例**
```python
import hmac
import hashlib
import base64
import json

def get_signature(data: str, key: str) -> str:
    key_bytes = base64.b64decode(key)
    hmac_obj = hmac.new(key_bytes, data.encode('utf-8'), hashlib.sha256)
    signature = base64.b64encode(hmac_obj.digest()).decode('utf-8')
    return signature
```

## 请求与响应匹配

客户端需为每个请求生成唯一 `reqid`，
服务端响应时会带回相同 `reqid` 用于对应。

例如：

**请求**

```json
TvZJMueyhbrH/BtEmr1zU/Eb/WtvrmkACx+5pio2PfE={"req":"file.ls","reqid":"6915841c6915841b000000440003","path":null}
```

**响应**

```json
{
    "files": [
        {
            "name": "测试文件搜索",
            "v": 1,
            "uid": 1001,
            "mtim": 1762967182,
            "btim": 1762967152,
            "dir": 1
        }
    ],
    "uver": 115537670504450,
    "reqid": "6915841c6915841b000000440003"
}
```

## 心跳机制

客户端定时（建议 60 秒）发送：

```json
{"req":"ping"}
```

服务端回应：

```json
{"res":"pong"}
```

若连续多次未收到 `pong`，应主动断开并重连, 关闭协议的心跳帧，服务端疑似已读不回。

## 示例交互流程

1. 客户端连接 `ws://192.168.1.14:5666/websocket?type=main`
2. 发送 `auth.login` 获取 `token`、`secret`
3. 后续请求需附带签名
4. 定时发送 `ping` 保持连接
5. 使用 `reqid` 匹配响应结果


## 错误码

| 错误码 | 错误信息 |
|--------|----------|
| 4096 | 系统内部错误 |
| 4097 | 系统繁忙 |
| 4098 | 内存不足 |
| 4099 | 磁盘空间不足 |
| 4100 | 文件或目录不存在 |
| 4101 | 无效的文件名或路径 |
| 4102 | 文件或目录已存在 |
| 4103 | 存储空间不存在或未挂载 |
| 4104 | 文件名或文件路径长度超过限制 |
| 4105 | 目的路径是目录 |
| 4112 | 目的路径不是目录 |
| 4121 | 文件系统只读 |
| 4128 | I/O错误 |
| 4208 | 数据库读写错误 |
| 4224 | 没有登录 |
| 4352 | 权限不足 |
| 4386 | 可用容量不足 |
| 8192 | 参数错误 |
| 36872 | 需要解压缩密码或解压缩密码错误 |
| 37120 | 下载错误 |
| 37376 | 读取配置文件错误 |
| 37377 | 写入配置文件错误 |
| 65280 | 无效的操作 |
| 65281 | 无权限操作 |
| 65296 | 已存在 |
| 65534 | 验签失败 |
| 65535 | 未知错误 |
| 2031616 | 检查更新失败 |
| 2031620 | 已是最新版本 |
| 2031621 | 执行更新脚本出错 |
| 2031632 | 正在更新中 |
| 131072 | 用户名或密码错误 |
| 131073 | 用户名不存在 |
| 131074 | 用户名已存在 |
| 131329 | 用户群组不存在 |
| 131330 | 用户群组已存在 |
| 135168 | 无效的凭证 |
| 139264 | 不能对当前登录用户执行该操作 |
| 139296 | 不能对系统默认用户组执行该操作 |
| 196608 | 磁盘繁忙 |
| 196609 | 磁盘数量不足以执行该操作 |
| 196610 | 磁盘数量超过需要 |
| 196624 | 存储池当前状态下不允许该操作 |
| 196640 | diskGroup不一致 |
| 196752 | 创建用户目录失败 |
| 196753 | 设置用户配额失败 |
| 258048 | 存储管理器繁忙，请稍后再试 |
| 196656 | 硬盘逻辑扇区大小不一致 |
| 262144 | App安装路径错误 |
| 266240 | 该App未安装或未启动 |
| 327681 | 无可用存储空间 |
| 327685 | 目标目录是源目录的子目录 |
| 327697 | 错误的文件大小 |
| 327848 | 共享权限设置失败 |
| 327849 | 该路径已被共享 |
| 327850 | 共享名称已存在 |
| 327851 | 远程目录已存在 |
| 393232 | 不可用的外部访问域名 |
| 51380224 | 无效的挂载类型 |
| 51380225 | 无法连接到远端服务，请检查输入的信息 |
| 51380226 | 此远程挂载已存在，请勿重复添加 |
| 51380227 | 查询挂载路径失败 |
| 51380228 | 用户名或密码错误 |
| 51380229 | 连接被对方服务器拒绝 |
| 51380230 | 路径不存在，连接失败 |
| 51380231 | 指定的路径错误，请检查输入的信息 |
| 51380232 | 没有权限进行此操作 |
| 51380233 | 请求超时，请重试 |
| 52428823 | 连接失败，请确认容器是否已启动 |
| 33554944 | 端口号已被占用 |
| 33554945 | 系统预留端口号 |
| 100000001 | 操作太频繁，请稍后重试 |
| 100000002 | 参数错误 |
| 100000003 | 重复的请求 |
| 100000004 | 无效的操作 |
| 100000006 | 服务器开小差了，请稍后重试 |
| 84934657 | 无效的任务 ID |
| 84934658 | 无效的存储类型 |
| 84934659 | 不支持的存储类型 |
| 84934660 | 无效的地址 |
| 84934661 | 任务 ID 与 UID 不匹配，无法操作 |
| 84934662 | 用户任务数已超过最大限量 |
| 84934663 | 不支持的存储类型 |
| 84934664 | 本地备份时目录冲突，有相互包含的情况 |
| 84934665 | 本地源目录不存在 |
| 84934666 | 任务名称已存在 |
| 84934667 | 内部错误，无法执行 |
| 84934668 | 源目录为空，无可备份文件 |
| 84934669 | 源路径存在重复 |
| 84934688 | 无效的存储位置 ID |
| 84934689 | 连接错误 |
| 84934690 | 存储位置 ID 与 UID 不匹配，无法操作 |
| 84934691 | 有任务正在使用此目的地，无法删除 |
| 84934692 | 调用授权服务失败 |
| 849346923 | 非法的 Token |
| 849346924 | 已经存在相同的存储配置 |
| 84934736 | 操作异常 |
| 84934737 | 连接失败 |
| 84934738 | 查询的目录不存在 |
| 84934739 | 目录已经存在，无法重复创建 |
| 84934740 | 创建目录失败 |
| 84934741 | 下载时出错 |
| 84934742 | 上传时出错 |
| 84934743 | 目录不存在 |
| 84934744 | 创建文件失败 |
| 84934745 | 本地文件不存在 |
| 84934746 | 网盘授权不可用或过期 |
| 84934747 | 云盘非法目录名 |
| 84934748 | 目标目录权限错误 |
| 84934749 | 来源文件权限错误 |
| 84934750 | 文件写入错误 |
| 84934751 | 用户名或者密码错误 |
| 84934752 | 服务端拒绝，需要查看服务设置 |
| 84934753 | 目标存储空间不足 |
| 100010001 | 添加任务失败 |
| 100010002 | 请求缺少outputDir参数 |
| 100010003 | 拷贝目录不存在 |
| 100010004 | 创建目录失败 |
| 100010005 | 拷贝目录无法写入 |
| 100010006 | 磁盘空间不足 |
| 100010007 | 请求缺少taskId参数 |
| 100010008 | 重复任务 |
| 100010009 | 获取文件信息失败 |
| 100010010 | 打开目录失败 |
| 100010011 | 打开文件失败 |
| 100010012 | 任务不存在 |
| 100000201 | 入参错误 |
| 100000202 | 保存配置失败 |
| 100000203 | 加载配置失败 |
| 100000204 | 重启网关失败 |
| 100000205 | 端口被占用 |
| 100000206 | 广播失败 |
| 100000207 | 重启avahi失败 |
| 33555718 | 操作不支持 |
| 33555719 | 端口被占用 |
| 100020001 | 网口不存在 |
| 100020002 | 添加网口失败 |
| 100020003 | ovs 网桥绑定失败 |
| 100020004 | ovs 网桥解绑失败 |
| 100020005 | 无线网络修改失败 |
| 100020006 | 找不到指定的无线网络 |
| 100020007 | 无线网络连接失败 |
| 100020008 | 密码不正确 |
| 100020009 | 无线网络安全类型不匹配 |
| 3000005 | 分享失败，无分享权限 |
| 3000011 | 分享失败，不支持分享挂载目录 |
| 3000012 | 分享失败，文件不存在 |
| 3000013 | 分享失败，不支持分享软链、挂载等 |
| 100000210 | 系统关键端口被防火墙规则拦截 |

## 真机抓包补充的错误码

下面这些是 2026-10 在真机（fnOS 1.2.0800）用 `tools/probe.py` 批量实测时抓到的，
报文字段原样记录，供排查用：

| errno | 服务端 errmsg | 实测接口示例 | 说明 |
|-------|--------------|-------------|------|
| `1` | `unexpected end of JSON input` | `appcgi.accountsrv.v1.token.list` | 参数体没传导致的解析错误（和 8192 一样属于「缺参数」） |
| `1001` | `unexpected end of JSON input` | `appcgi.mountmgr.task.detail` | 同上，该模块自己的一套错误码 |
| `3000001` | `Invalid Params` | `appcgi.netsvr.ddns.record.detail` | 参数不合法 |
| `10000001` | `unexpected end of JSON input` | `appcgi.sac.ups.v1.check` | 参数解析失败 |
| `10000002` | `接口不存在` | `__probe__.does.not.exist` | **未知 req**：拿它当「接口是否存在」的探针 |
| `100000004` | - | `appcgi.network.gen.info` | 无效操作（该子功能在当前版本未启用） |
| `100030002` | - | `appcgi.resmon.battery` | 无电池设备 |
| `100060001` | - | `appcgi.sysinfo.getReservedPartition` | 无保留分区 |
| `100060031` | - | `appcgi.sysinfo.getBootOnPowerFlag` | 该机型不支持来电自启 |
| `100160045` | - | `appcgi.sysrestore.getSysBackupTask` | 系统备份任务不存在 |
| `102550007` | `Bad Request` | `appcgi.license.soft.get` | 授权模块参数不合法 |
| `266240` | - | `appcgi.iscsimgr.iscsi.lun.list` | 「该 App 未安装或未启动」——功能未开时所有子接口都会报它 |
| `3000006` | `Not Found Error` | `appcgi.sharesvr.share.link.get` | 资源不存在（参数格式对，但那条分享没有） |
| `65534` | - | 未登录时任意 appcgi 接口 | 未登录 / 会话失效（`0xfffe`） |
| `135168` | - | `file.share.info`、`share.link.get` 传假 token | 分享 token / 资源找不到 |
| `4101` | - | `file.share.add2` 传空 `shareName` | 分享名称校验失败（空值） |
| `4112` | - | `file.share.add2` 传非空 `shareName` | 分享名称相关校验失败（该接口还缺别的必填参数，未测通） |
| `4100` | - | `file.prop` / `file.rename` | 路径不存在（`file.prop` 里是**条目级** errno，外层仍 succ） |
| `65535` | - | `file.extract` 传空 `fromCharset` | 服务端命令执行失败（`Too short switch: -fromcharset`） |

> 判断接口是否存在，看 `errno` 是不是 `10000002`；
> `8192 / 100000002 / 1001 / 1 / 3000001 / 102550007` 都表示**接口存在，只是参数不对**。

## 响应外层结构不止一种

同一个 WebSocket 连接里，不同模块的响应「外壳」不一样，写客户端时必须都兼容：

| 结构 | 典型模块 | 示例 |
|------|---------|------|
| `{result, req, reqid, rev, data:{...}}` | `appcgi.network.*`、`appcgi.resmon.*`、`appcgi.sysinfo.*`、`appcgi.security.*` | 数据在 `data` 里 |
| `{result, reqid, rsp:{...}}` | `appcgi.mountmgr.*` | 数据在 `rsp` 里 |
| `{result, reqid, data:{...}}` | `appcgi.sac.*`、`appcgi.netsvr.*` | 数据在 `data` 里 |
| 平铺（`{业务字段..., reqid}`） | `file.*`、`stor.*` | 如 `{"files":[...],"uver":1,"reqid":"..."}`，业务字段直接挂在根上 |

> ⚠️ **成功响应可能没有 `result` 字段**。实测 `file.ls`、`stor.listDisk` 成功时返回的 JSON
> 只有业务字段 + `reqid`（`reqid` 还在最后面）；只有**失败**时才会出现 `"result":"fail"` 和 `errno`。
> 所以判断成功不能只看 `result == "succ"`，应该看「没有 `errno` / 有预期业务字段」。

SDK 里的 `sdk/api/curated.py:unwrap()` 就是干这个的：
依次尝试 `data`、`rsp`，都没有就返回原响应；`check()` 只在 `result == "fail"` 时抛异常。

## 请求参数放在哪里：平铺 还是 data

和响应外壳一样，**请求参数的位置也是分模块的**，这一条是 2026-01 实测分享接口时才发现并确认的：

| 写法 | 报文 | 适用模块 |
|------|------|---------|
| 平铺 | `{"req":"file.ls","reqid":"...","path":"vol1/1000"}` | `file.*`、`stor.*`、`user.*`、`notify.*`、`appcgi.share.*` |
| `data` 封装 | `{"req":"appcgi.sharesvr.share.link.list","reqid":"...","data":{"page":1,"pageSize":100}}` | `appcgi.sharesvr.*` 的带参接口（`share.link.list/get/create/update/remove/clear`、`share.permission.set` 等） |

实测对照（同一个接口、同一份参数，只改封装方式）：

```jsonc
// 平铺 —— 服务端说参数不合法
{"req":"appcgi.sharesvr.share.link.list","reqid":"...","page":1,"pageSize":100,"keyword":"","isAdmin":false,"type":0,"sortColumn":"createdTime","sortType":"DESC"}
{"result":"fail","errno":3000001,"errmsg":"Invalid Params","data":null}

// 包一层 data —— 正常返回
{"req":"appcgi.sharesvr.share.link.list","reqid":"...","data":{"page":1,"pageSize":100,"keyword":"","isAdmin":false,"type":0,"sortColumn":"createdTime","sortType":"DESC"}}
{"result":"succ","data":{"total":0,"list":null}}
```

另外两个实测出来的细节：

- `appcgi.sharesvr.*` 里 **`id` 必须是字符串**：`{"data":{"id":"c55bd4d2b4e5404a90"}}` 正常，
  `{"data":{"id":1}}` 直接 `Invalid Params`（连「找不到」都不给你）。
- 反过来，`file.*` 传 `data` 不会报错但**参数会被忽略**（`file.ls` 会安静地列错目录），
  所以不能「不管三七二十一都包 data」。

**怎么判断该用哪种：**

1. 先按模块猜（上表）；
2. 拿到 `errno 3000001 Invalid Params` / `1001` 就换另一种写法重试——这两种错误表示
   请求体没被解析，**请求没有执行**，重试是安全的；
3. 不想记就交给 SDK：
   - `await client.call(req, params, nested=True)` —— 强制包 `data`
   - `await client.call_auto(req, params)` —— 先平铺，只有报「参数非法」才自动改包 `data`
     重发，并把该接口的正确写法记进 `client.nested_reqs`，下次直接走对的那条

> 分享接口的完整实测记录（含原始报文）见 [docs/modules/share.md](modules/share.md)
> 与 `data/share_probe.json`；复跑用 `python tools/probe_share.py --yes`。

## 写接口是异步任务：ack + 同 reqid 的推送

`file.*` 里的写操作（`file.cp` / `file.mv` / `file.rm` / `file.compress` / `file.extract` /
`file.setAcl2` / `file.chown` / `file.usage` …）**不是「一问一答」**：先回一个「任务已受理」，
真正结果**用同一个 `reqid` 推送回来**。

```jsonc
// 1) 请求
{"req":"file.cp","reqid":"6ad…002e","files":["/vol1/1000/tmp/a.jpg"],
 "pathTo":"/vol1/1000/tmp/dst","overwrite":1,"details":{"name":"a.jpg","count":1}}

// 2) 立刻返回：没有 result，只有 taskId
{"sysNotify":"taskId","taskId":"OdkhlbCaRg+61xHFGLc29w==","reqid":"6ad…002e"}

// 3) 推送：任务回显（taskInfo 里是原参数）
{"sysNotify":"taskInfo","taskInfo":{"req":"file.cp","reqid":"6ad…002e", …}}

// 4) 推送：进度
{"percent":100,"time":0,"speed":0,"size":1880200,"sizeTotal":1880200,"reqid":"6ad…002e"}

// 5) 推送：最终结果
{"result":"succ","reqid":"6ad…002e"}
{"result":"fail","reqid":"6ad…0032","failedFilesCount":1,
 "failedFiles":[{"file":"/vol1/1000/tmp/dst/renamed.jpg","errno":4100}]}
```

必须记住的几点：

- **只发请求、不看推送 = 不知道成败**。实测源文件不存在时 `file.mv` 的 ack 仍是
  `succ`，只有推送是 `fail`；
- 判定标准是「带 `result` 字段且 `reqid` 相同的那条推送」；`taskInfo` 和进度是过程消息
  （前端看到 `sysNotify` 就跳过）；
- SDK 里 `sdk/filetasks.py` 的 `wait_file_task(client, reqid)` 把这套封好了：
  客户端 `__init__` 时挂常驻嗅探器，结果不会漏；`remove_push_handler()` 清空时也不会
  误删它。另有 `is_task_ok()` / `task_error()` / `call_file_task()`；
- 只读接口（`file.ls` / `file.prop` / `file.calc` / `file.access` …）和 `file.rename` /
  `file.mkdir` 是同步的，失败直接回 `errno`。
- `file.usage` 这类接口还会**推多条分类结果**（`{category:"docker", fileSizeTotal:…}`）
  再推 `{"result":"succ"}`，所以「一条推送」并不等于全部数据。

## 心跳：`ping_interval=None` 曾经是死循环（已修）

`_ping_loop` 的逻辑是「发 ping → `asyncio.sleep(ping_interval)`」。如果 `ping_interval`
传 `None`，`asyncio.sleep(None)` 会抛 `TypeError`，被循环里的 `except Exception` 吞掉后
立刻重试 —— 变成疯狂发 ping 的死循环，实测 1 分钟刷出十几万条 `{"res":"pong"}`
（把推送回调打爆）。现在 `_ping_loop` 会在 `ping_interval` 为空/≤0 时直接返回，
即「不发应用层心跳」。要长期挂着连接就老老实实传 `ping_interval=60`。

## 服务端主动推送

有两类报文没有对应的请求：

1. **心跳回包**：`{"res":"pong"}`
2. **业务推送**：形如 `{"notify":[{"title":..., "content":"{...json...}", ...}]}`，
   或者 `{"result":"succ","data":{...}}` 这种「迟到的异步结果」。

它们都**不带 `reqid`**（或者 reqid 对不上任何在途请求），
用 `sdk/recorder.py` 录制、`tools/watch.py` 做归类统计。
推送内容里的 `content` 字段经常是一段 JSON 字符串，需要二次 `json.loads`。

## 连接类型（type 参数）

`ws://<host>:5666/websocket?type=main`、`?type=file`、`?type=timer`
**共用同一套接口**——实测同一批接口在三种 `type` 下返回完全一致，
所以只需要连一个（推荐 `main`），不用为不同业务分别建连。
