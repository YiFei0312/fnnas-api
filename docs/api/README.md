# fnOS 接口封装总览

> 自动生成，来源：前端产物静态扫描 + 真机只读实测。
> 生成时间：2026-10-17 03:16:18，目标 NAS：`http://192.168.1.10:5666`

- 已封装接口：**476** 个（只读 184，写 292）
- 实测状态：已实测存在（业务错误码） 29，实测返回非标准结构 1，已实测存在（缺参数） 28，已实测通过 145，实测超时 1，未实测（写接口） 272
- 实测被证伪（静态误报，已剔除）：16 个
- 一级模块存疑（App id / 日期格式串等，未封装）：23 个
- 服务端推送事件名：56 个（见 events.md）

## 📖 交互式单文件文档

**推荐先看 [interfaces.html](interfaces.html)**：一个文件装下全部接口，带搜索、分组筛选、
状态筛选，以及每个接口的「用途 / 参数 / 返回字段与数据类型」表格和实测原始报文。
（`python tools/gen_html.py` 生成，双击即可用浏览器打开，不依赖网络。）

下面是按分组拆分的 Markdown 版本，适合在编辑器/仓库里检索。

## 用法

```python
from sdk import FnOsClient

client = FnOsClient()
await client.connect('ws://<nas>:5666/websocket?type=main')
await client.login(user, password)

# 1. 命名空间调用（推荐，有 docstring 和参数提示）
await client.api.file.ls(path='vol1/1000')
await client.api.stor.list_disk()          # 磁盘列表
await client.api.appcgi.network.net_list() # 网卡信息

# 2. 通用调用（临时试验新接口）
await client.api.call('file.prop', {'path': '/vol1/1000/a.jpg'})

# 3. 查找接口
client.api.find('disk')        # 关键字搜索
client.api.groups()            # 全部分组
client.api.readonly_methods()  # 只看只读接口
print(client.api.help('stor.listDisk'))
```

## 响应结构提醒

`reqid` 在响应里可能出现得很靠后；`file.*`/`stor.*` 这种平铺结构的
成功响应**没有 `result` 字段**（只有业务字段 + `reqid`），失败才有 `result=fail` + `errno`。
其它模块的外层是 `data` 或 `rsp`，详见 [protocol.md](../protocol.md)。

## 服务端主动推送

```python
from sdk.push import extract_notify, event_of

def on_notify(client, payload):
    for item in extract_notify(payload):
        print(item['title'], item.get('event'), item.get('data'))

client.add_push_handler('notify', on_notify)          # 只收通知类推送
client.add_push_handler(None, lambda c, p: print(event_of(p), p))  # 全都要
```

## 分组一览

| 分组 | 接口数 | 文档 |
| --- | --- | --- |
| `stor` | 64 | [stor.md](stor.md) |
| `file` | 44 | [file.md](file.md) |
| `appcgi.network` | 39 | [appcgi_network.md](appcgi_network.md) |
| `appcgi.sac` | 39 | [appcgi_sac.md](appcgi_sac.md) |
| `user` | 33 | [user.md](user.md) |
| `appcgi.netsvr` | 32 | [appcgi_netsvr.md](appcgi_netsvr.md) |
| `appcgi.sysinfo` | 27 | [appcgi_sysinfo.md](appcgi_sysinfo.md) |
| `appcgi.share` | 23 | [appcgi_share.md](appcgi_share.md) |
| `appcgi.backup` | 21 | [appcgi_backup.md](appcgi_backup.md) |
| `appcgi.tfa` | 20 | [appcgi_tfa.md](appcgi_tfa.md) |
| `appcgi.resmon` | 16 | [appcgi_resmon.md](appcgi_resmon.md) |
| `appcgi.mountmgr` | 15 | [appcgi_mountmgr.md](appcgi_mountmgr.md) |
| `appcgi.sharesvr` | 13 | [appcgi_sharesvr.md](appcgi_sharesvr.md) |
| `appcgi.sysrestore` | 12 | [appcgi_sysrestore.md](appcgi_sysrestore.md) |
| `appcgi.license` | 10 | [appcgi_license.md](appcgi_license.md) |
| `appcgi.ipblocker` | 9 | [appcgi_ipblocker.md](appcgi_ipblocker.md) |
| `appcgi.screen` | 9 | [appcgi_screen.md](appcgi_screen.md) |
| `appcgi.security` | 8 | [appcgi_security.md](appcgi_security.md) |
| `appcgi.eventlogger` | 7 | [appcgi_eventlogger.md](appcgi_eventlogger.md) |
| `notify` | 6 | [notify.md](notify.md) |
| `usrdat` | 5 | [usrdat.md](usrdat.md) |
| `appcgi.filestor` | 4 | [appcgi_filestor.md](appcgi_filestor.md) |
| `appcgi.finder` | 4 | [appcgi_finder.md](appcgi_finder.md) |
| `liveupdate` | 4 | [liveupdate.md](liveupdate.md) |
| `appcgi.accountsrv` | 3 | [appcgi_accountsrv.md](appcgi_accountsrv.md) |
| `util` | 3 | [util.md](util.md) |
| `appcgi.usersrv` | 2 | [appcgi_usersrv.md](appcgi_usersrv.md) |
| `power` | 2 | [power.md](power.md) |
| `appcgi.iscsimgr` | 1 | [appcgi_iscsimgr.md](appcgi_iscsimgr.md) |
| `taskState` | 1 | [taskState.md](taskState.md) |
