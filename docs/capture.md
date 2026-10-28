# 接口抓取与封装流程

> 目标：不靠猜、不靠翻源码，把飞牛 NAS 的接口**批量、可复现**地抓下来，
> 并且用真机实测确认它到底存不存在，最后自动生成 SDK 封装 + 文档。

整条链路共 8 步，全部可重复执行、产出都落在仓库里：

```
① 静态扫描        ①b HTTP 接口        ② 真机只读探测      ②b 分享链路实测      ②c 文件管理实测      ③ 生成封装与文档      ④ 录制推送      ⑤ 生成 HTML
tools/scan_web.py → tools/scan_http.py → tools/probe.py  → tools/probe_share.py → tools/probe_file.py → tools/gen_api.py → tools/watch.py → tools/gen_html.py
  data/reqs.json     data/http_api.json   probe_status.json  （结论并入 ②）        （结论并入 ②）        sdk/api/spec.py     captures/*.jsonl  docs/api/interfaces.html
  data/reqs.md       docs/api/http.md                         data/share_probe.json  data/file_probe.json  docs/api/*.md      （+ verify_html.py 校验）
                     ↑ tools/probe_http.py（全量实测）                                                      ↑ tools/probe_album.py（相册全流程取样例）
                     ↑ tools/extract_write_params.py（挖请求体字段）                                         ↑ tools/md_subset.py（模块文档渲染进 HTML）
```

> ① 抓的是 **WebSocket 接口**（`appcgi.*` / `file.*` …），①b 抓的是 **HTTP 接口**：
> 飞牛有两个前端，`/` 是 WebSocket RPC 的桌面，`/p` 是**相册 / AI 相册**应用，
> 后者完全走 REST（`/api/v1/...`），两套接口不重叠。

> ② 是「带空参数发一次」的通用探测：只能判断**接口在不在**，判断不了参数长什么样，
> 也碰不了写接口。分享和文件管理这类「必须真的操作一条数据才能验证」的接口，
> 用 ②b / ②c 的专用工具 —— 见 [分享模块](modules/share.md)、[文件管理模块](modules/file.md)。

> 挖参数的小工具：`python tools/js_context.py "file\.prop"` 能在打包后的 JS 里
> 按正则查命中点并打印上下文（压缩过的产物是一整行，普通 grep 没用）。
> `file.prop` / `file.cp` / `file.extract` 的真实参数就是这么从
> `data/web-cache/assets/` 里翻出来的。

## ① 静态扫描：从网页产物里挖接口名

飞牛的前端是打包过的 JS，但接口名都硬编码在里面，形如：

```js
ZG = { ls: `file.ls`, lsDir: `file.lsDir`, prop: `file.prop`, ... }
```

```bash
python tools/scan_web.py                     # 默认扫 http://<你的NAS>:5666
python tools/scan_web.py --base http://192.168.1.10:5666 --workers 16
```

产出：

- `data/reqs.json`：所有候选名字 + 来源证据（`direct`/`alias`/`assign`/…）+ 出现在哪个 js + 分档
- `data/reqs.md`：人看的版本

分档规则（`tier` 字段）：

| tier | 含义 | 可信度 |
|------|------|--------|
| `endpoint` | 出现在前端接口映射表，或真实调用点 | 高（仍可能误报） |
| `event` | 事件/状态枚举常量 | 不是接口 |
| `unverified` | 只是长得像接口的字符串 | 低，多为 i18n 文案键 |

> 踩过的坑：`{field:\`uploadConfig.desc\`}`、`{i18nKey:\`photoWall.xxx\`}`、
> `{address:\`pan.baidu.com\`}` 这类**配置项/文案键**长得和接口一模一样，
> 扫描器按「对象键名」过滤掉了一批；剩下的靠第②步实测证伪。

## ①b 抓 `/p` 相册应用的 HTTP 接口

飞牛的 `/p` 是**相册 / AI 相册**应用（照片时间线、相册、人物、智能识别、地图、回收站…），
它**不用 WebSocket**，全部走 REST，所以 ① 的 WS 扫描器抓不到它。它的接口定义在前端是
RTK Query 形态，直接结构化提取即可：

```js
reducerPath: `albumApi`, endpoints: e => ({
  getList: e.query({query: e => ({url: `/api/v1/album/list`, params: {...}})}),
  create:  e.mutation({query: e => ({url: `/api/v1/album/create`, method: `post`, body: e})}),
})
```

```bash
python tools/scan_http.py                       # 用缓存提取 → data/http_api.json + docs/api/http.md
python tools/scan_http.py --force               # 先重新抓一遍 /p 产物

# 写接口的请求体字段：定义里只有 body:e，字段名在调用点，再跑一步「别名链」解析
python tools/extract_write_params.py            # 就地补 params_keys / param_evidence

# 真机实测：WebSocket 登录拿 token → cookie fnos-token + authx 调 /p/api
python tools/probe_http.py                      # GET 全量 + 可逆写场景（建相册→…→删相册）
python tools/probe_http.py --no-writes          # 只测 GET
python tools/scan_http.py --render-only         # 把实测结果渲染回 docs/api/http.md

# 相册接口专项：跑一遍「建相册→加照片→改名→设封面→删相册」，样例写进 data/album_probe.json
python tools/probe_album.py
```

相册接口的功能/数据模型/完整用法单独整理在 [相册（/p 相册应用）](modules/album.md)，
客户端封装是 `sdk/http_photo.py`：

**鉴权（实测跑通，和 WebSocket 那套完全不同）**：

```
请求头 Cookie: fnos-token=<WebSocket 登录返回的 token>
请求头 authx : nonce=<6位>&timestamp=<13位毫秒>&sign=<md5>
sign = md5(APPKEY_/p路径_nonce_timestamp_md5(反编码参数串)_应用密钥)
```
`fnos-token` 就是 WS 登录的 token（前端 `ro.set('fnos-token', token)` 写进 cookie）；
`authx` 签名里 GET 参数要**按 key 排序**再 md5、POST 算 `JSON.stringify(body)`，
所以签名和发包必须是同一份数据。只缺任一个都会失败（缺 authx → `code 5000 invalid sign`，
缺 token → HTTP 401）。`python tools/probe_http.py` 已经把这套封好了。

产出 `data/http_api.json`（url / method / 参数或请求体 / 前端端点名 / 所属 api 分组 / 探活结果）
和 `docs/api/http.md`，也会渲染进 `docs/api/interfaces.html` 的「HTTP 接口」一节。

**写接口参数是怎么挖的**：RTK Query 定义里通常写 `body: e`（透传调用参数），字段名在调用点：

```
定义 chunk：{useCreateShareLinkMutation: o} ... export{... o as i ...}
使用 chunk：import{i as h}from"./B8RasvHeFEYlBmIA2.js"
调用点：    const [k] = h();  k({album_name: …, ids: …})
```

`tools/extract_write_params.py` 就做这条链的解析（模块 import/export 图 + hook 解构 + 调用点
作用域内取对象字面量），所以 `album/create` 能挖到 `album_name, ids`、
`ai-face/run` 能挖到 `allowGpuDecoding, selectedGpuSequence, allowCpuDecoding`。
挖不到的（参数由变量/表单值传入）会如实标成「未解析」，宽松匹配的字段带 `?` 标记，不硬编。

**相册接口的功能与用法**单独写在 [相册（/p 相册应用）](modules/album.md)：数据模型（相册对象 /
照片对象字段）、三组浏览/管理/分享接口、三个可直接复制的流程（浏览照片、建相册到删除、
相册分享）、以及「参数命名风格不统一 / 时间是冒号格式 / 新 id 在返回体里」这几个坑。

## ② 真机实测：确认接口是否存在

只发**只读接口**（`sdk/safety.py` 里维护白名单，拒绝删/写/格式化等操作），
每个接口带空参数发一次，用返回值判断它到底存不存在：

```bash
export fn_username=你的账号          # Windows: set fn_username=...
export fn_password=你的密码
python tools/probe.py --reqs data/reqs.json --tier endpoint --limit 400
python tools/probe.py --names file.ls,stor.listDisk,appcgi.resmon.cpu
python tools/probe.py --dry-run            # 只看会打哪些接口，不真发
```

判读规则（详见 [通信协议](protocol.md#真机抓包补充的错误码)）：

| 状态 | 依据 | 结论 |
|------|------|------|
| `succ` | `result=succ` | 接口存在，能直接用 |
| `param_error` | `errno ∈ {8192, 100000002, 3000001}`（`tools/probe.py:PARAM_ERROR_ERRNO`） | 接口存在，缺参数 |
| `error` | 其它 errno | 接口存在，业务上拒绝了（如「未安装」） |
| `unknown` | `errno=10000002`（用 `__probe__.does.not.exist` 探针标定） | **接口不存在**，静态误报 |
| `timeout`/`exception` | 超时或异常 | 待复查 |

产出 `data/probe_status.json`（含状态、errno、响应字段、样例报文）。

**安全边界**：写接口（`file.rm`、`stor.format`、`user.del`、`power.poweroff` …）
一律不自动发请求，只在文档里标注为「未实测（写接口）」。
要自己试某个写接口，用 `client.api.call(...)` 手动来。

### `/p` HTTP 接口的实测原则

`tools/probe_http.py` 对 `/p` 的 151 个 HTTP 接口做实测，但同样守只读原则：

| 类型 | 做法 |
|------|------|
| GET（62 个） | **全部实测**，需要 id/时间的接口先从别的接口取真实值再回填（`album_id`、照片 `id`、`start_time` 时间桶…） |
| 写接口（89 个） | **只测可逆场景**：建相册 → 查详情/时间线 → 改名 → 加照片进相册 → 查归属 → 移出照片 → 删相册 → **核对列表已清空** |
| 破坏性写接口 | `clean-all` / `delete` / `remove person` / `install` 等**一律不发**，文档里标「未实测（写接口）」 |

实测结果直接写回 `data/http_api.json` 的 `probe*` 字段（`probe_code` / `probe_msg` /
`probe_keys` / `probe_sample` / `probe_params`），文档的「实测」和「参数」两列就是这么来的
——**实测成功的参数比从 JS 里挖出来的更可靠**，所以 `record_probe()` 会把它们回填到
`params_keys`。

## ②b 有副作用的接口：小范围真机实测

有些接口光发空参数是没用的——参数名、参数放哪里（平铺还是 `data`）、返回字段，
都得**真的造一条数据**才能测出来，典型就是分享。这类接口用一个专用工具，
逻辑写死成「创建 → 查 → 改 → 删」，测完自己清理：

```bash
python tools/probe_share.py                    # dry-run，只打印计划
python tools/probe_share.py --yes              # 执行：创建 1 条测试分享，跑完自动删除
python tools/probe_share.py --yes --keep       # 保留（调试用，记得手工删）
python tools/probe_share.py --yes --path /vol1/1000/tmp
```

- 只操作 `--path` 指定的路径，实测完删除自己创建的分享并复查 `total == 0`；
- 产出 `data/share_probe.json`（每次调用的参数 + 原始响应），
  并把实测结论（状态 / 字段 / 样例）**合并**进 `data/probe_status.json`，
  所以顺序是：先 `probe.py`，再 `probe_share.py`，最后 `gen_api.py`；
- 顺带会把历史上「errno 属于参数错误却记成 error」的结论修正为 `param_error`。

> 实测挖出来的最大一个坑：**`appcgi.sharesvr.*` 的参数必须包在 `{"data": {...}}` 里**，
> 平铺发（哪怕参数名全对）只会得到 `errno 3000001 Invalid Params`。
> 详见 [通信协议 · 请求参数放在哪里](protocol.md#请求参数放在哪里平铺-还是-data)。

## ②c 文件管理：在一次性临时目录里跑可逆操作

文件接口的参数名得试（`file.prop` 是 `files` 数组、`file.size` 是 `file`、
`file.cp` 是 `pathTo`），而且 `file.rm` 真的会删东西。所以这个工具的做法是：
**在 `--path` 下面新建一个带时间戳的临时目录，所有写操作只发生在里面**，
原目录里的文件只读（ls / prop / access / calc / getAcl / download）：

```bash
python tools/probe_file.py                     # dry-run，只打印计划
python tools/probe_file.py --yes               # 真跑，跑完删掉临时目录并核对复原
python tools/probe_file.py --yes --keep        # 保留临时目录（调试用）
```

跑的顺序：只读探测 → 建临时目录 → 上传（HTTP）→ checkUpload 三种 overwrite →
收藏/最近访问（加完就删）→ 复制/改名/移动 → 压缩/解压 → 权限原样写回（不产生净变化）
→ 回收站（只用一个 21 字节的小文件）→ 删除临时目录 → **核对 `--path` 列表与开始时
逐项一致、原文件 size/mtim/btim 未变**。

- 删除前会断言目标就是 `fnapi_filetest_*` 前缀且位于 `--path` 之下，否则拒绝执行；
- 产出 `data/file_probe.json`（参数 + 原始响应 + **期间收到的推送**，异步任务的结果就在推送里）；
- 结论同样合并进 `data/probe_status.json`。

> 实测挖出来的两个大坑：
> ① **写接口是异步任务**，ack 回 `succ` 不代表成功，成败要看同 `reqid` 的推送 → 于是有了
> `sdk/filetasks.py` 的 `wait_file_task()`；
> ② `file.trash.restore` 会回 `succ` 但**并没有真的还原**，`files` 参数形态没确认
> （结论因此没有写进文档，工具里也标了 `skip_merge`）。
> 详见 [文件管理 · 两条协议级结论](modules/file.md)。

## ③ 自动生成 SDK 封装与文档

```bash
python tools/gen_api.py
```

产出：

- `sdk/api/spec.py`：接口元数据（接口名 → 分组/方法名/实测状态/只读标记）
- `data/api_spec.json`：同样内容的 JSON 版
- `docs/api/README.md`：总览 + 用法
- `docs/api/<分组>.md`：每个分组的接口表 + 实测样例报文
- `docs/api/events.md`：推送事件名清单
- `docs/api/excluded.md`：被剔除的名字及原因（实测证伪 / 模块存疑）

生成时会做三件清洗：

1. 实测 `unknown` 的（接口不存在）剔除；
2. 一级模块名不属于实测确认过的模块（`appcgi`/`file`/`stor`/`user`/`util`/`usrdat`/`notify`/
   `taskState`/`liveupdate`/`power`）的剔除——那些基本是 App id、日期格式串；
3. 方法名保证是合法且可访问的 Python 标识符（`user.2fa.loginVerify` → `user_2fa_login_verify`）。

## ④ 录制推送消息

除了「一问一答」，NAS 还会主动推通知、任务进度、状态变化。用录制器把它们抓下来：

```bash
# 方式一：命令行工具，边操作网页边抓
python tools/watch.py --seconds 120
python tools/watch.py --seconds 120 --verbose

# 方式二：代码里挂录制器（推荐，能录全量收发报文）
from sdk.recorder import TrafficRecorder

recorder = TrafficRecorder("captures/all.jsonl")     # 传 None 则只统计不落盘
client = FnOsClient(recorder=recorder)
...
recorder.close()
print(recorder.stats())      # records / sent / received / pushes / unique_reqs
```

录制器默认**脱敏**：`password`/`token`/`secret`/`aes`/`rsa`/`sign` 等字段写盘前会被替换成
`***`，签名前缀也会被抹掉，所以 `captures/` 可以放心留存（但仍建议不要提交到公开仓库）。

### 把推送接成回调

不想自己解析 JSON，直接把消息挂成处理函数即可：

```python
from sdk.push import extract_notify, event_of, is_pong

def on_notify(client, payload):
    for item in extract_notify(payload):        # 自动把 content 里的 JSON 解析出来
        print(item["title"], item.get("event"), item.get("data"))

client.add_push_handler("notify", on_notify)                    # 只收带 notify 的推送
client.add_push_handler(lambda p: "entryChange" in str(p), cb)  # 条件过滤
client.add_push_handler(None, lambda c, p: print(event_of(p)))  # 全都要

# 装饰器写法
@client.add_push_handler("diskDegraded")
async def on_disk(client, payload):
    ...

client.remove_push_handler(on_notify)       # 注销；不传参数则清空
```

回调签名统一是 `callback(client, payload)`，普通函数和 `async def` 都支持，
单个回调抛异常不会影响其它回调。

`_listen` 里还会把**「reqid 对不上任何在途请求」的迟到响应**也当作推送分发，
所以异步任务结果同样能在 `add_push_handler(None, ...)` 里收到。

## ⑤ 生成 HTML 接口文档

最后把「接口清单 + 实测样例」拼成一份**单文件 HTML**，给别人看/自己查都方便：

```bash
python tools/gen_html.py                      # → docs/api/interfaces.html
python tools/gen_html.py --sample-limit 8000  # 详情里的原始报文最多留多少字符
python tools/gen_html.py --doc docs/modules/album.md   # 把模块文档（Markdown）也渲染进单文件 HTML
                                              # --doc 可重复，默认就内嵌 docs/modules/album.md
python tools/verify_html.py                   # 校验完整性（会用 Edge/Chrome 真解析一遍）
python tools/check_doc_fields.py              # 可选：连真机核对文档字段是否过时（只读接口）
```

文档里每个接口都有：

| 列 / 区块 | 内容 |
|-----------|------|
| 方法 / req | `snake_case` 方法名 + 原始 req（点开行看详情） |
| 用途 | 接口做什么；写接口没实测，标 <kbd>推断</kbd> 徽标，不编造语义 |
| 权限 | 只读 / 写（来自 `sdk/safety.py` 的同一份判定） |
| 实测状态 | 已实测通过 / 缺参数 / 业务报错 / 未实测（写接口） |
| 返回字段（类型） | 实测报文推导出的顶层字段与类型，如 `files: array<object>` |
| 详情展开 | 参数表（名称/类型/说明）、完整字段类型表（含数组元素字段、嵌套对象）、实测原始报文 |

其它：顶部统计卡片、关键字搜索、分组/状态/只读筛选，附录里还有推送事件名、
被剔除的候选名字和通用字段中文对照表。

> 生成器踩过的坑：`<table>` **不能直接放在 `<tbody>` 里**（嵌套字段表必须包一层 `<td>`），
> 否则浏览器会提前闭合外层表格，后面的 `<tr>/<td>` 会被当纯文本丢掉——页面看着正常，
> 实际少一半接口，而 Python 的宽松 HTML 解析查不出来。所以 `verify_html.py`
> 用真实浏览器 `--dump-dom` 再解析一遍、逐个比对接口 id。
>
> `tests/test_html.py` 里也留了同一条回归用例，防止再犯。

## 用生成的封装

```python
from sdk import FnOsClient

client = FnOsClient(ping_interval=60)
await client.connect('ws://192.168.1.10:5666/websocket?type=main')
await client.login(user, password)

# 1) 自动生成的全量接口（覆盖 476 个，带 docstring）
await client.api.file.ls(path='vol4/1000')
await client.api.stor.list_disk()
await client.api.appcgi.sysinfo.get_uptime()
await client.api.call('file.prop', {'files': ['/vol1/1000/a.jpg']})   # 通用调用

# 2) 手写的高频接口（自动解包 data/rsp，失败抛 BadRequestError）
await client.sysinfo_uptime()
await client.resmon_cpu()
await client.network_interfaces()
await client.storage_calc_space()
await client.notify_unread_total()

# 3) 文件操作：写接口是异步任务，用 wait_file_task 等结果
await client.file_prop('/vol1/1000/a.jpg')                      # → prop 数组
resp = await client.file_cp('/vol1/1000/a.jpg', '/vol1/1000/dst')
result = await wait_file_task(client, resp['reqid'])            # 成败看推送
print(is_task_ok(result), result)
await client.file_rename('/vol1/1000/dst/a.jpg', 'b.jpg')       # 同步接口

# 4) 分享链接（appcgi.sharesvr.* 要包 data，这里已经封好）
share = await client.share_link_create('/vol1/1000/tmp/a.jpg', name='给同事', passwd='1234')
print(client.share_url(share['id']))            # http://<NAS>:5666/s/<id>
await client.share_links()                      # 列表
await client.share_link_update(share['id'], valid_to=0)   # 改成永久有效
await client.share_link_remove(share['id'])     # 删除

# 5) 探索用辅助方法
client.api.find('disk')             # 按关键字找接口
client.api.groups()                 # 有哪些分组
client.api.readonly_methods()       # 只看只读接口
print(client.api.help('stor.listDisk'))
```

## 回归测试

```bash
python -m unittest discover -s tests -v
```

离线用例覆盖：reqid 格式、HMAC 签名向量、地址推导、连接状态判断、
录制脱敏、只读安全分级、生成封装的完整性与命名规范、`client.api` 行为、
分享接口的参数封装（`data` 嵌套）与 `call_auto` 自适应、
文件接口的参数形态（`files` 数组 / `file.size` 用 `file` / `pathTo` 是目录）
与异步任务等待器（`sdk/filetasks.py`）。
不需要连 NAS，但依赖 `websockets`/`pycryptodome` 的用例会自动跳过。

有副作用的接口另外留了**真机联调用例**（默认跳过，会创建并自动删除分享）：

```bash
# Windows: $env:FN_LIVE_SHARE='1'; $env:FN_LIVE_SHARE_PATH='/vol1/1000/tmp'
FN_LIVE_SHARE=1 python -m unittest tests.test_share_live -v
python tools/probe_share.py --yes      # 分享：同样的链路，带完整报文日志
python tools/probe_file.py --yes      # 文件管理：临时目录里跑可逆操作，带推送日志
```
