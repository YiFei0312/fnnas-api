# FnOS API Client (JavaScript Version)

这是 FnOS API 客户端的 JavaScript 实现版本，基于原有的 Python 版本转换而来。该客户端提供了与 FnOS 系统进行交互的能力，包括用户认证、文件操作、系统设置等功能。

## 目录结构

```
fnnas-api-js/
├── package.json          # 项目配置文件
├── index.js              # 项目入口文件
├── README.md             # 使用文档
└── lib/
    ├── FnOsClient.js     # 主要客户端类
    ├── exceptions.js     # 异常处理类
    ├── utils.js          # 工具函数
    ├── encryption.js     # 加密功能
    └── handlers.js       # 请求处理函数
```

## 安装

1. 确保已安装 Node.js (推荐 v14.0 或更高版本)
2. 克隆或下载项目到本地
3. 进入项目目录并安装依赖：

```bash
cd fnnas-api-js
npm install
```

## 快速开始

### 基本使用

```javascript
const { FnOsClient } = require('./fnnas-api-js');

async function main() {
  try {
    // 创建客户端实例
    const client = new FnOsClient();
    
    // 连接到服务器
    await client.connect('ws://your-server-address:port');
    console.log('连接成功');
    
    // 登录
    await client.login('username', 'password');
    console.log('登录成功');
    
    // 获取用户信息
    const userInfo = await client.user_info();
    console.log('用户信息:', userInfo);
    
    // 获取存储信息
    const storageInfo = await client.get_user_storage();
    console.log('存储信息:', storageInfo);
    
    // 关闭连接
    await client.close();
    console.log('连接已关闭');
  } catch (error) {
    console.error('错误:', error);
  }
}

main();
```

## API 文档

### 客户端初始化

```javascript
const client = new FnOsClient(ping_interval, logger);
```
- `ping_interval` (可选): 心跳间隔时间（秒），默认为 30
- `logger` (可选): 自定义日志对象，需包含 debug、info、error、exception 方法

### 连接管理

#### connect(url)
连接到 WebSocket 服务器
- `url`: WebSocket 服务器地址

#### close(timeout)
关闭连接
- `timeout` (可选): 关闭超时时间（秒），默认为 5.0

#### connected()
检查连接是否活跃，返回 Promise<boolean>

### 用户认证

#### login(username, password, options)
用户登录
- `username`: 用户名
- `password`: 密码
- `options` (可选):
  - `deviceType`: 设备类型，默认为 'Browser'
  - `deviceName`: 设备名称，默认为 'Windows-Google Chrome'
  - `stay`: 是否保持登录，默认为 false

#### user_info()
获取用户信息

### 系统设置

#### setting_port(options)
修改端口设置
- `options`:
  - `force_https`: 是否强制使用 HTTPS，默认为 false
  - `redirect`: 是否重定向，默认为 true
  - `http_port`: HTTP 端口，默认为 5666
  - `https_port`: HTTPS 端口，默认为 5667

### 存储管理

#### get_user_storage()
获取磁盘信息，包括配额、空间和存储信息

### 文件操作

#### fileList(path)
列出指定路径下的文件
- `path` (可选): NAS 路径，默认为 null

#### upload(local_path, nas_path, overwrite)
上传文件
- `local_path`: 本地文件路径
- `nas_path`: NAS 文件路径
- `overwrite`: 覆盖策略，0 跳过，1 覆盖，2 保留两者，默认为 2

#### download()
下载文件（待实现）

#### file_search(key, path)
搜索文件
- `key`: 搜索关键词
- `path`: 搜索路径数组

### 文件监听

#### start_observer(options)
启动文件变化监听，定期检查本地和 NAS 文件的变化
- `options`:
  - `nas_path`: NAS 路径，默认为 null
  - `local_path`: 本地路径，默认为当前工作目录
  - `recursive`: 是否递归监听，默认为 false
  - `interval`: 轮询间隔（秒），默认为 5
  - `exclude`: 排除的文件列表，默认为 null

## 事件处理

客户端通过注册处理器来处理不同类型的请求响应：

```javascript
client.add_handler('util.crypto.getRSAPub', async (client, data) => {
  // 处理获取 RSA 公钥的响应
  console.log('获取到 RSA 公钥:', data);
});
```

## 异常处理

客户端可能抛出以下异常：
- `WebSocketConnectionError`: WebSocket 连接错误
- `BadRequestError`: 服务器返回的错误，包含错误代码和消息

## 示例

- 详见 `example.js`

## 注意事项

1. 确保服务器地址和端口正确
2. 确保用户名和密码正确
3. 对于文件上传，确保本地文件路径存在且有读取权限
4. 对于文件监听，确保本地目录存在且有读写权限
5. 连接过程中可能会遇到网络问题，请适当处理异常

## 依赖

- `ws`: WebSocket 客户端
- `crypto`: 加密功能（Node.js 内置）
- `fs`: 文件系统操作（Node.js 内置）
- `path`: 路径处理（Node.js 内置）
- `http`: HTTP 客户端（Node.js 内置）

## 硬编码修改

- 将 `192.168.1.12` 替换为 `你的ip`
- 将 `5666` 替换为 `你的端口`
- 将 `wcz` 替换为 `你的用户名`
- 将 `wcz520178` 替换为 `你的密码`
- 将 `/vol1`相关的路径 替换为 `你的NAS路径`


## 许可证

MIT
