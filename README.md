目前已经实现ws断开自动重连（会重新登录）

飞牛 NAS 接口已抓取并封装：真机实测确认 **476 个 WebSocket 接口**（只读 184 / 写 292），
另外爬了 `/p` 相册应用的 **151 个 HTTP 接口**（REST，不走 WebSocket）。

📖 **全量接口文档：[`docs/api/interfaces.html`](docs/api/interfaces.html)（单文件 HTML，浏览器直接打开）**
—— 带搜索/筛选，每个接口都有「用途 / 参数 / 返回字段与数据类型」表格和实测原始报文。
Markdown 版见 [`docs/api/README.md`](docs/api/README.md)，抓取流程见 [`docs/capture.md`](docs/capture.md)，
`/p` 相册应用的 HTTP 接口见 [`docs/api/http.md`](docs/api/http.md)，
相册接口的功能与用法见 [`docs/modules/album.md`](docs/modules/album.md)
（**相册文档也已内嵌进上面那个 HTML**，打开后左侧导航「相册（/p 相册应用）」一节）。

🧩 **MCP Server + 飞牛专属应用：[`docs/nasapp.md`](docs/nasapp.md)**
—— 476 个 WS + 151 个 HTTP 接口封装成 39 个 MCP 工具，打包成飞牛 fnOS 应用装到 NAS 上：
自带 Web 界面（接口文档 + 两种 MCP 连接开关 + 可用接口清单），
`http://<NAS>:8686/mcp`（Streamable HTTP）或 `/sse`（HTTP+SSE）直接接 Claude Code / Cursor 等客户端。

#### 快速入门

> Linux、Macos设置环境变量
```shell
export fn_username=你的账号
export fn_password=你的密码
```

> Windows设置环境变量
```cmd
set fn_username=你的账号
set fn_password=你的密码
```


> 示例代码
```python
import asyncio
from sdk import FnOsClient
from sdk.handlers import HandlerUserInfo
import os


async def main():
    # 启动飞牛连接
    client = FnOsClient(ping_interval=60)
    await client.connect('ws://127.0.0.1:5666/websocket?type=main')
    client.add_handler('user.info', HandlerUserInfo)

    try:
        login_res = await client.login(os.getenv("fn_username"), os.getenv('fn_password'))
        print("login_res", login_res)
        res = await client.user_info()
        print("user_info", res)
        res = await client.authToken() # 非必须
        print("authToken", res)
        
        # 上传文件（地址取自身连接的 ws 地址，不用再改源码）
        local_path = r'C:\Users\user\Pictures\bg.jpg'
        nas_path = f'/vol1/1001/tmp_img/sample.jpg' # NAS绝对路径
        res = await client.upload(local_path, nas_path)
        print("upload res", res)

        # 修改端口
        res = await client.setting_port()
        print("setting_port", res)

        # 永久运行（直到手动停止）
        await asyncio.Event().wait()

        # 运行60s停止
        # await asyncio.sleep(60)
        # await client.close()
    except KeyboardInterrupt:
        print('中断进程')
        print('关闭client')
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
```

#### 调用任意接口（自动生成的封装）

`client.api` 是按接口名自动生成的命名空间，覆盖抓到的全部 476 个接口，
方法带 docstring、能 tab 补全，参数原样透传：

```python
# 点出来的调用方式（推荐）
res = await client.api.file.ls(path='vol4/1000')          # 列目录
res = await client.api.stor.list_disk()                   # 硬盘列表
res = await client.api.appcgi.sysinfo.get_uptime()        # 开机时长

# 参数不确定时用通用调用
res = await client.api.call('file.prop', {'path': 'vol4/1000'})

# 探索用的小工具
client.api.find('disk')            # 关键字搜接口
client.api.groups()                # 有哪些分组
client.api.readonly_methods()      # 只看只读（安全）接口
print(client.api.help('stor.listDisk'))
```

高频接口另有一层手写封装，会自动剥掉 `data`/`rsp` 外壳、失败抛 `BadRequestError`：

```python
await client.sysinfo_hostname()      # 主机名 + 版本
await client.resmon_cpu()            # CPU 占用
await client.network_interfaces()    # 网卡列表
await client.network_gateway()       # 网关配置
await client.storage_calc_space()    # 存储用量汇总
await client.storage_disks()         # 硬盘列表
await client.notify_unread_total()   # 未读通知数
await client.notify_list(1, 20)      # 通知列表
await client.file_favorites()        # 收藏夹
```

#### 文件操作（参数已按真机实测修正）

批量查询用 `files` 数组、`file.size` 用 `file`、复制移动用 `pathTo`——都是拿
`/vol1/1000/tmp` 真机跑出来的（复现：`python tools/probe_file.py --yes`）：

```python
await client.file_prop('/vol1/1000/tmp/a.jpg')        # → prop 数组（参数是 files，不是 path）
await client.file_size('/vol1/1000/tmp')              # → {size, space}
await client.file_calc('/vol1/1000/tmp')              # → 文件数 / 目录数 / 占用
await client.file_access('/vol1/1000/tmp/a.jpg')      # → [权限位掩码]
await client.file_download('/vol1/1000/tmp/a.jpg')    # → [{uri}] 带签名的下载地址

# ⚠️ 写接口是「异步任务」：接口只回 ack，成败要看同 reqid 的推送
resp = await client.file_cp('/vol1/1000/tmp/a.jpg', '/vol1/1000/tmp/dst')
result = await wait_file_task(client, resp['reqid'])   # None = 超时
if not is_task_ok(result):
    raise RuntimeError(result)

await client.file_rename('/vol1/1000/tmp/dst/a.jpg', 'b.jpg')     # 同步接口
await client.file_compress('/vol1/1000/tmp/dst/b.jpg', '/vol1/1000/tmp/b.zip')
await client.file_extract('/vol1/1000/tmp/b.zip', '/vol1/1000/tmp/out')
await client.file_rm('/vol1/1000/tmp/dst', move_to_trashbin=False)
```

参数总表、上传的 HTTP 流程、回收站的坑见 [`docs/modules/file.md`](docs/modules/file.md)。

#### 相册（`/p` 相册应用，HTTP REST）

相册应用不走 WebSocket，用的是 `GET/POST /p/api/v1/...` + cookie `fnos-token` + `authx` 签名，
SDK 里封了 `sdk/http_photo.py`：

```python
from sdk.http_photo import PhotoHttpClient

photo = await PhotoHttpClient.login('http://192.168.1.10:5666', 'demo-user', '密码')

albums = await photo.albums()                    # 相册列表
album  = await photo.album_create('旅行照片')     # → {'albumId': 8, ...}
aid    = album['albumId']

# 浏览照片：先取时间线桶，再按「冒号日期」格式拿列表
tl = await photo.gallery_timeline()              # [{year, month, day, itemCount}, ...]
b = tl['list'][0]
photos = await photo.photos('%04d:%02d:%02d 00:00:00' % (b['year'], b['month'], b['day']),
                            '%04d:%02d:%02d 23:59:59' % (b['year'], b['month'], b['day']))

await photo.album_add_photos(aid, [photos['list'][0]['id']])   # 加进相册
await photo.album_timeline(aid)                  # 相册时间线（注意参数是 camelCase）
await photo.album_rename(aid, '旅行照片-2026')
await photo.album_delete(aid)                    # 删相册（里面的照片不会被删）
```

数据模型、全部相册/分享接口、三个可复制的完整流程和几个坑见
[`docs/modules/album.md`](docs/modules/album.md)；实测脚本 `python tools/probe_album.py`。

#### MCP Server（给 AI 客户端用）

接口已经封装成 MCP Server，NAS 上装好应用后直接连：

```bash
# 应用在 http://<NAS>:8686，两种传输都在界面上有开关
claude mcp add --transport http fnnas-nas http://192.168.1.10:8686/mcp
```

39 个精选工具（系统/存储/文件/分享/相册/通用检索），写操作自动等异步任务完成；
接口文档、可用接口清单、两个 MCP 连接开关都在应用界面里。

界面首页有 **「飞牛连接配置」**：IP/主机名、端口、账号、密码、HTTP 地址，配好点
「保存并重连」立即生效（密码只写不回显，已配置时留空表示不修改），旁边还能「测试连接」。
详见 [`docs/nasapp.md`](docs/nasapp.md)。

本地开发也可以直接跑（不用装到 NAS）：

```bash
python -m mcp.server --selftest                # 自检：协议层 + 工具清单
python -m mcp.server --http --port 8686        # Web UI + 两个 MCP 端点
python -m mcp.server --stdio                   # 只支持 stdio 的客户端
```

包里**不含任何账号密码**（首次在界面里填，凭据只存在 NAS 的
`/vol1/@appconf/fnnas-mcp/config.json`，权限 600）；想装完即用就加 `--provision`：

打包成飞牛应用并安装：

```bash
python tools/build_nas_app.py                  # → dist/fnnas-mcp-1.0.0.fpk
python tools/install_nas_app.py                # 上传 → 解析 → 安装 → 启动
```

#### 分享链接（已全链路真机实测）

分享接口在 `appcgi.sharesvr.share.link.*`，**参数必须包在 `data` 里**（平铺会报
`errno 3000001 Invalid Params`），SDK 已经封装好：

```python
# 创建分享：文件路径 / 提取码 / 有效期（秒级时间戳）/ 可访问次数（0=不限）
share = await client.share_link_create('/vol1/1000/tmp/20260127_195353.jpg',
                                       name='给同事的照片', passwd='1234',
                                       max_access=10, valid_to=1792172307)
print(client.share_url(share['id']))     # http://<NAS>:5666/s/<id>

await client.share_links()                                   # 列表（含 total/list）
await client.share_link(share['id'])                         # 详情（含 files 列表）
await client.share_link_update(share['id'], name='改名', valid_to=0)  # 0=永久有效
await client.share_link_remove(share['id'])                  # 删除
await client.share_link_default()                            # 分享域名/限速默认配置
```

也可以直接调底层接口，只是要显式说明参数封装方式：

```python
await client.call('appcgi.sharesvr.share.link.list',
                  {'page': 1, 'pageSize': 100}, nested=True)  # nested=True = 包一层 data
await client.call_auto(req, params)                          # 懒得判断时用它，会自动试并记住
```

完整字段表、原始报文和踩坑记录见 [`docs/modules/share.md`](docs/modules/share.md)。

#### 抓包 / 录制报文

```bash
# 1) 静态扫描前端产物，挖出接口名
python tools/scan_web.py --base http://192.168.1.10:5666

# 2) 真机只读实测（只发白名单里的只读接口），判断接口是否存在
python tools/probe.py --reqs data/reqs.json --tier endpoint

# 2.5) 有副作用的接口小范围实测（分享：创建→查→改→删，测完自动清理）
python tools/probe_share.py --yes

# 2.6) 文件管理实测（只在自己建的临时目录里做可逆操作，测完核对目录复原）
python tools/probe_file.py --yes

# 2.7) 想从打包后的 JS 里翻参数：查某个接口名的上下文
python tools/js_context.py "file\.prop"

# 2.8) 爬 /p 相册应用的 HTTP 接口（REST，不是 WebSocket）
python tools/scan_http.py                  # 提取 → data/http_api.json + docs/api/http.md
python tools/extract_write_params.py       # 挖写接口的请求体字段（hook 别名链 → 调用点）

# 2.9) 真机实测（WebSocket 登录拿 token → cookie fnos-token + authx 签名调 /p/api）
python tools/probe_http.py                 # GET 全量实测 + 可逆写场景（建相册→改名→加/移照片→删相册）
python tools/probe_http.py --no-writes     # 只测 GET
python tools/probe_album.py                # 相册接口专项：跑完整流程并生成样例数据
python tools/scan_http.py --render-only    # 把实测结果渲染回 http.md

# 3) 生成 SDK 封装 + docs/api/*.md
python tools/gen_api.py

# 3.5) 生成单文件 HTML 接口文档 + 校验完整性
python tools/gen_html.py
python tools/verify_html.py

# 4) 监听并录制 NAS 主动推送的消息
python tools/watch.py --seconds 120
```

代码里也可以挂录制器，录全量收发报文（默认脱敏，不会把密码写进文件）：

```python
from sdk.recorder import TrafficRecorder

recorder = TrafficRecorder('captures/all.jsonl')
client = FnOsClient(ping_interval=60, recorder=recorder)
...
print(recorder.stats())   # {'records': ..., 'sent': ..., 'received': ..., 'pushes': ...}
recorder.close()
```

#### 接收 NAS 主动推送的消息

服务端会在没请求的情况下推通知、任务进度、状态变化。挂个回调就能接：

```python
from sdk.push import extract_notify, event_of

def on_notify(client, payload):
    for item in extract_notify(payload):          # 自动解析 content 里的 JSON
        print(item["title"], item.get("event"), item.get("data"))

client.add_push_handler("notify", on_notify)      # 只关心通知类推送
client.add_push_handler(None, lambda c, p: print("push:", event_of(p)))  # 全都要

# 装饰器写法，也支持 async def
@client.add_push_handler("diskDegraded")
async def on_disk(client, payload):
    ...
```

#### 关闭日志输出

> 默认日志输出为DEBUG等级，如果需要关闭日志输出，可以参考下面代码

```python
import asyncio
import logging
from sdk import FnOsClient
import os

async def main():
    # 启动飞牛连接
    client = FnOsClient(ping_interval=60, logger=logging.getLogger("null"))
    await client.connect('ws://192.168.1.8:5666/websocket?type=main')
    login_res = await client.login(os.getenv("fn_username"), os.getenv('fn_password'))
    print(login_res)

if __name__ == "__main__":
    asyncio.run(main())
```

SDK没有优化，很多异常没有处理，只是能用，不好用。大佬们封装吧

#### 测试

```bash
python -m unittest discover -s tests -v
```

离线用例覆盖 reqid/签名/地址推导/连接状态、录制脱敏、只读安全分级、
推送回调分发、生成封装的完整性、HTML 文档生成器的结构回归（`tests/test_html.py`）、
分享接口的参数封装与 `call_auto` 自适应（`tests/test_share_api.py`）、
文件接口的参数形态与异步任务等待器（`tests/test_file_ops.py`），
以及 `client.api` 的调用行为，不需要连 NAS。

真机联调用例在 `tests/test_share_live.py`（默认跳过，会在 NAS 上创建并自动删除分享）：

```bash
# Windows PowerShell
$env:FN_LIVE_SHARE='1'; $env:FN_LIVE_SHARE_PATH='/vol1/1000/tmp'
python -m unittest tests.test_share_live -v
```

它会跑「创建（带提取码/有效期/次数）→ 列表 → 详情 → 打开分享地址 → 修改 → 删除 →
条数回到基线」，并额外验证「同样参数平铺发一定被拒、`call_auto` 会自动改包 `data`」。

#### TODO

 - [x] 登录
 - [x] 验证Token
 - [x] 心跳
 - [x] 用户详细信息
 - [x] 文件列表
 - [x] 文件上传
 - [x] 端口修改
 - [x] 磁盘信息
 - [x] 搜索文件
 - [x] 接口全量抓取 + 自动封装（476 个，`client.api.*`）
 - [x] 只读接口真机实测与安全分级（`sdk/safety.py`）
 - [x] 报文录制（`sdk/recorder.py` + `tools/watch.py`）
 - [x] 服务端推送消息回调封装（`client.add_push_handler` + `sdk/push.py`）
 - [x] 全量接口 HTML 文档（用途 + 数据类型表格，`tools/gen_html.py` → `docs/api/interfaces.html`）
 - [x] 分享链接接口全链路真机实测与封装（创建/列表/详情/修改/删除，`tools/probe_share.py` + `client.share_link_*`）
 - [x] 文件管理接口真机实测与参数修正（`tools/probe_file.py`；顺手修了 `ping_interval=None` 的心跳死循环）
 - [x] 异步任务（复制/移动/压缩/删除…）的结果等待封装（`sdk/filetasks.py`）
 - [x] 文件下载（取签名 URL + GET，见 `client.file_download`）
 - [x] `/p` 相册应用 HTTP 接口抓取（151 个 REST 接口 + `authx` 签名算法，`tools/scan_http.py` → `docs/api/http.md`）
 - [x] `/p` 写接口参数挖掘（`tools/extract_write_params.py`：hook 别名链 → 调用点，37 个写接口挖到请求体字段）
 - [x] `/p` HTTP 接口真机实测（`tools/probe_http.py`：破解 authx + `fnos-token` cookie，GET 53/62 成功，
       5 个可逆写接口验证并清理干净）
 - [x] 相册接口功能与用法文档 + SDK 客户端（`docs/modules/album.md` + `sdk/http_photo.py`，
       `tools/probe_album.py` 跑通建相册→加照片→改名→设封面→删除全流程）
 - [ ] 文件双向同步 [我改了SMB方案，所以可能不更新了]
 - [ ] 写接口参数补全（写接口不自动实测，需人工逐个确认参数名）
 - [ ] 旧的 `file.share.add2` 参数未测通（当前 Web UI 已改用 `appcgi.sharesvr.share.link.*`）
 - [ ] `file.cancel` / `file.trimacl.conv` 参数形态未确认（试过的写法都报 8192）
 - [ ] `file.trash.restore` 的 `files` 路径形态未确认（回 succ 但没真的还原）
 - [ ] 浏览器端流量代理（HTTP+WS 反向代理，用于抓真实网页操作的完整参数）
 - [ ] 其他接口
