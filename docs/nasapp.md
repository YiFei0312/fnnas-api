# MCP Server 与飞牛应用（fnnas-mcp）

把本项目封装成 **MCP Server**（Model Context Protocol），并打包成飞牛 fnOS 的专属应用，
装到 NAS 上以后：

- **AI 客户端**（Claude Code / Cursor / Cherry Studio / n8n …）可以直接连上来，
  用自然语言操作 NAS 的 476 个 WebSocket 接口 + 151 个相册 HTTP 接口；
- **应用界面**里能看到接口文档、两个 MCP 连接方式的开关，以及**实测可用接口的清单**。

- 应用名：`fnnas-mcp`　显示名：飞牛接口 MCP Server　版本：1.0.0
- 安装位置：`/vol1/@appcenter/fnnas-mcp`（数据 `/vol1/@appdata/fnnas-mcp`，配置 `/vol1/@appconf/fnnas-mcp/config.json`）
- 服务端口：**8686**　桌面入口：应用中心 → 飞牛接口 MCP Server（iframe 打开）

## 界面

`http://<NAS>:8686/`　（从 fnOS 桌面点应用图标也会打开这个地址）

| 区块 | 内容 |
|------|------|
| 顶部状态 | NAS 连接状态（已登录账号 / 未连接，会显示最后错误） |
| **飞牛连接配置** | **首页显眼位置**：IP/主机名、端口、账号、密码、HTTP 地址（可选）+「保存并重连」「测试连接」「本机」快捷按钮；保存后立即重连，密码只写不回显（已配置时提示"留空表示不修改"） |
| 指标卡 | 476 个 WebSocket 接口 / 实测可用数 / 151 个相册 HTTP 接口 / 实测可用数 / MCP 工具数 |
| **MCP 连接方式** | 两张卡片各带一个开关：**Streamable HTTP**（推荐）与 **HTTP + SSE**；显示完整 URL、一键复制、客户端配置片段 |
| **可用接口** | 搜索 + 协议筛选（WS/HTTP）+ 「只看实测可用」；每行标 **✅ 实测通过 / ⚠ 需要参数 / — 未实测**，附接口名、分组、中文说明、参数 |
| 接口文档 | 内嵌整份 `interfaces.html`（搜索、分组、返回字段、实测报文），也可新标签打开 `/docs` |
| 设置 | 是否在 `tools/list` 里包含未实测工具、客户端配置示例（NAS 连接已挪到首页） |
| 日志 | 应用最近日志（连接失败排查用） |

## 两种 MCP 连接方式

两种传输都实现了，在界面上各有一个开关，**即时生效**（关闭后该端点返回 404）。

| 方式 | 地址 | 适合 |
|------|------|------|
| **Streamable HTTP**（推荐） | `http://<NAS>:8686/mcp` | 新版 MCP 客户端（Claude Code、Cursor、Cherry Studio、n8n…） |
| **HTTP + SSE**（兼容旧版） | `http://<NAS>:8686/sse`（消息端点 `/messages?sessionId=…`） | 只支持旧版 SSE 传输的客户端 |

客户端配置（JSON）：

```json
{
  "mcpServers": {
    "fnnas-nas":     { "type": "http", "url": "http://192.168.1.10:8686/mcp" },
    "fnnas-nas-sse": { "type": "sse",  "url": "http://192.168.1.10:8686/sse" }
  }
}
```

Claude Code 命令行：

```bash
claude mcp add --transport http fnnas-nas http://192.168.1.10:8686/mcp
```

> stdio 方式也在包里（`python3 -m mcp.server --stdio`），适合在本机直接把
> `mcp/` 目录挂给只支持 stdio 的客户端；NAS 应用里默认不开。

## MCP 工具

`tools/list` 返回 **39 个工具**（可用接口都是真机实测过的）：

| 分类 | 工具 |
|------|------|
| 系统 | `fnnas_system_info`、`fnnas_system_uptime`、`fnnas_system_hostname`、`fnnas_cpu_usage`、`fnnas_disk_usage`、`fnnas_network_interfaces`、`fnnas_notifications`、`fnnas_notify_unread` |
| 用户 | `fnnas_user_info`、`fnnas_users` |
| 存储 | `fnnas_storage_disks`、`fnnas_storage_spaces` |
| 文件 | `fnnas_file_ls`、`fnnas_file_prop`、`fnnas_file_size`、`fnnas_file_download_link`、`fnnas_file_mkdir`、`fnnas_file_rename`、`fnnas_file_copy`、`fnnas_file_move`、`fnnas_file_delete`、`fnnas_file_compress`、`fnnas_file_extract`、`fnnas_trash_list` |
| 分享 | `fnnas_share_link_create`、`fnnas_share_link_list`、`fnnas_share_link_remove` |
| 相册 | `fnnas_photo_albums`、`fnnas_photo_album_create`、`fnnas_photo_album_add`、`fnnas_photo_album_delete`、`fnnas_photo_timeline`、`fnnas_photo_list`、`fnnas_photo_detail`、`fnnas_photo_stat` |
| 通用 | `fnnas_interfaces_search`、`fnnas_interface_call`、`fnnas_http_interfaces_search`、`fnnas_http_api_call` |

写操作（复制/移动/删除/压缩/解压）是异步任务，工具内部会等同 `reqid` 的推送直到任务结束，
不会只回一个 ack。

**「可用接口」怎么算的**：`data/probe_status.json` 里真机探测为 `succ` 的算「✅ 实测通过」，
`param_error` / `error` 算「⚠ 存在（需要参数/业务拒绝）」，`unknown` 不算；
相册 HTTP 接口按 `/p` 实测 `code == 0` 算可用。界面上可切换「包含未实测」查看全量。

## 账号密码怎么处理（重要）

**应用包里不含任何账号密码**，这是刻意的：

| 环节 | 凭据 |
|------|------|
| `dist/*.fpk` 应用包 | 不含账号密码；`default_config.json` 里 `username`/`password` 都是空串 |
| 打包时脱敏 | 包内文本会把个人痕迹替换掉：账号名 → `demo-user`、主机名 → `demoNAS`、内网 IP → `192.168.1.x`、密码 → `REDACTED`（仓库里的实测数据保持原样，方便自己复查） |
| 首次启动 | `configured=false`，界面顶部状态显示「待配置账号」，MCP 调用会返回「还没配置 NAS 账号密码」的提示 |
| 用户配置后 | 存到 `${TRIM_PKGETC}/config.json`（`/vol1/@appconf/fnnas-mcp/config.json`，权限 600），界面里密码只写不回显 |
| 卸载 | 系统会保留 `@appconf`/`@appdata`（用户数据不丢），重装后沿用原配置 |

如果想**装完即用**（自动化/私有分发），有两种方式：

```bash
# 方式 1：安装时预置（写进应用配置，不写进包）
python tools/install_nas_app.py --username 你的管理员账号 --password 你的密码 --provision

# 方式 2：已经装好了，只补配置
python tools/install_nas_app.py --provision-only --username 账号 --password 密码

# 也支持：打包时就把默认账号塞进 default_config.json（⚠ 会写进 fpk，仅限内部测试）
python tools/build_nas_app.py --username 账号 --password 密码
```

## 打包与安装

```bash
# 1) 打包（Windows/Linux 都行，需要 tools/fnos/fnpack）
python tools/build_nas_app.py                      # 产物 dist/fnnas-mcp-1.0.0.fpk
python tools/build_nas_app.py --version 1.0.1      # 改了内容就升版本

# 2) 安装到 NAS（走应用中心的 HTTP API，等价于界面「手动安装」）
python tools/install_nas_app.py --dump             # 只上传 + 查看包信息，不安装
python tools/install_nas_app.py                    # 上传 → 解析 → 安装 → 启动
python tools/install_nas_app.py --status           # 看是否已安装/运行
python tools/install_nas_app.py --uninstall        # 卸载
```

安装流程（反编译 App Center 前端 + 实测确认）：

```
POST /upload                    上传 fpk（multipart 字段名必须是 trim-upload-file，带 Trim-* 签名头）
POST /app-center/v1/download/task  {packageSourceType:"file", path:"<NAS 路径>"} → downloadTaskId
GET  /app-center/v1/download/status?downloadTaskId=…   轮询到 status=2
GET  /app-center/v1/install/info?appName=…&version=…&packageType=path
POST /app-center/v1/install/task  {appName, version, packageType:"path",
                                   systemParameters:{installVolumeID:1, dataVolumeId:1}}
POST /app-center/v1/install/status {taskId}             轮询到 status=2
POST /app-center/v1/start/start    {appName, ignoreDependencies:true}
```

鉴权：这些接口只认 cookie **`fnos-token`**（WebSocket 登录返回的 token），不需要 `authx`。

## 应用包结构

```
fnnas-mcp/
├── manifest            # appname/version/display_name/desc/platform/service_port=8686/ctl_stop…
├── config/privilege    # {"defaults":{"run-as":"package"},"username":"fnnas-mcp",…}
├── config/resource     # {}（不需要共享目录）
├── ICON.PNG / ICON_256.PNG
├── cmd/                # install_init/install_callback/main/upgrade_*/uninstall_*/config_*
└── app/                # 打包成 app.tgz，解压到 /vol1/@appcenter/fnnas-mcp
    ├── mcp/            # MCP Server（协议层 + 工具 + HTTP 服务）
    ├── sdk/            # 本项目 SDK（Python，走 WebSocket）
    ├── lib/            # 纯 Python 依赖：websockets、watchdog；Linux 版 pycryptodome
    ├── data/           # api_spec.json、http_api.json、probe_status.json、interfaces.html
    ├── webui/          # 应用界面（原生 JS，无构建步骤）
    ├── ui/             # fnOS 桌面入口 config + 图标
    └── default_config.json
```

生命周期：`cmd/main` 支持 `start|stop|status`，用 pid 文件管理 `python3 -m mcp.server`，
日志写到 `$TRIM_PKGVAR/info.log`（也就是 `/vol1/@appdata/fnnas-mcp/info.log`）。

**运行时**：用系统自带的 `python3`（实测 NAS 是 3.11），第三方依赖全部随包携带：
`websockets`（纯 Python）、`watchdog`（纯 Python 轮子）、`pycryptodome`（manylinux cp39-abi3 轮子，
负责登录用的 RSA/AES）。所以**不需要**在 NAS 上 pip install，也不依赖应用商店的运行时包。

## 实测记录（2026-10-19）

| 项目 | 结果 |
|------|------|
| 打包 | `dist/fnnas-mcp-1.0.0.fpk`，2.7 MB（解包后 12.5 MB） |
| 安装 | 应用中心 `install/task` 成功，`/vol1/@appcenter/fnnas-mcp` 落地，23 个应用中可见 |
| 启动 | `cmd/main start` 成功，端口 8686 监听；日志显示**已登录 fnOS**（127.0.0.1） |
| 界面 | `GET /` 200（含标题）、`/static/*` 200、`GET /docs` 1.7 MB |
| 状态 | `/api/status`：连接 true、476/202/145 WS、151/58 HTTP、39 工具 |
| MCP | `initialize` / `tools/list`(39) / `tools/call` 全部通，`uptime`、`file.ls`、`stor.listStor`、`album/list`、`share.link.list` 都返回真实数据 |
| SSE | `GET /sse` 收到 endpoint 事件 → `POST /messages` 202 → 响应从 SSE 流返回 |
| 开关 | 关闭 Streamable HTTP → `POST /mcp` 返回 404 且带「已在界面上关闭」；关闭 SSE 同理 |

## 踩过的坑

| 坑 | 说明 |
|----|------|
| 应用中心接口只认 cookie | `/app-center/*` 用 `fnos-token` 就行，不用 `/p` 那套 `authx` 签名 |
| `checkUpload` 对已存在文件改名 | 会返回 `xxx.~#1` 这种新名字；**不要**拿它当 `Trim-Path`，直接用目标文件名上传才能覆盖，否则应用中心解析不到包 |
| 上传字段名 | `/upload` 的 multipart 字段名必须是 `trim-upload-file`，写 `file` 直接 400 |
| `download/status` 没有外层 | 返回 `{status,message,progress,…}` 而不是 `{code,msg,data}`；`status=5` 表示「还没解析出来」，要等 |
| 安装参数 | `install/task` 的 `systemParameters` **只给** `{installVolumeID, dataVolumeId}`：少了 `dataVolumeId` → 异步任务 `code 10208`（ErrCodeVolumeIDException）；多给 `agreedToProtocol` / `apiScope` / `immediateStart`，或带 `customParameters`（哪怕 `{}`）→ 接口 HTTP 500 + `code 10000`（OpenAPI 参数异常） |
| 解析缓存按 appName | `/vol1/appcenter-downloads/<appName>-<版本>-tpk` 会复用；改了包内容务必升版本，否则装上去还是旧内容（首次踩坑就是漏带 `watchdog`） |
| 依赖要随包 | 系统 python 没有 websockets/pycryptodome/watchdog，必须放进 `app/lib` |
| 安装参数别混用 | 装应用要**管理员**账号（`--username/--password`）；写进应用的账号用 `--app-username/--app-password`。空账号去登录会让 SDK 在加密环节直接抛 TypeError |
| 安装脚本的执行用户 | `run-as=package` 的专用用户（本机 uid 973），改文件/端口都受它限制 |

## 卸载

```bash
python tools/install_nas_app.py --uninstall
```

或在应用中心里点卸载。卸载会删掉 `/vol1/@appcenter/fnnas-mcp`、`@appdata`、`@appconf`
里的应用数据（配置里的 NAS 账号也会一起没）。
