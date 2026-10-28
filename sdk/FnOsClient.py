from abc import ABC, abstractmethod
import websockets
import json
import logging
import signal
from typing import Optional, List, Union
import asyncio
from .exceptions import WebSocketConnectionError
from .handlers import *
from .utils import *
from .encryption import login_encrypt, get_signature_req, get_signature
from .api.curated import (SystemApiMixin, StorageApiMixin, FileOpsApiMixin,
                          ShareApiMixin)
from .push import push_matches

# 「参数非法」错误码：这几个只可能是参数没被服务端识别，请求没有执行，可以安全重试
INVALID_PARAMS_ERRNOS = frozenset({3000001, 1001})


def _is_invalid_params(resp):
    return (isinstance(resp, dict) and resp.get("result") == "fail"
            and resp.get("errno") in INVALID_PARAMS_ERRNOS)


class BaseClient(ABC):
    def __init__(self, ping_interval=30, logger=None, recorder=None, timeout=None):
        self.websocket = None
        self.handlers = {}
        self.pending_requests = {}
        self.req_mapping = {}
        self.ping_interval = ping_interval

        self._listen_task = None
        self._ping_task = None
        self.__url = None

        # 报文录制器（sdk.recorder.TrafficRecorder），为 None 时不录制
        self.recorder = recorder
        # 单次请求默认超时（秒）；None 表示一直等
        self.timeout = timeout
        # 由 ws 地址推导出的 http 地址，上传/下载等 http 接口用
        self.base_url = None
        # 封装好的接口命名空间（client.api.file.ls ...），首次访问时创建
        self._api_root = None
        # 已确认「参数要包 data」的接口（client.call_auto 自动学习结果）
        self.nested_reqs = set()
        # 服务端主动推送的处理函数列表 [(matcher, callback), ...]
        self.push_handlers = []
        # 常驻嗅探「异步文件任务的最终结果」推送（ack + 同 reqid 推送的模型，
        # 详见 sdk/filetasks.py 与 docs/modules/file.md）
        from .filetasks import install_sniffer
        install_sniffer(self)

        # 下面数据自动初始化
        self.sign_key = None
        self.key = generate_random_string(32)
        self.iv = os.urandom(16)

        # 网站数据, 不用赋值，自动赋值
        self.si = None
        self.pub = None
        # 以下登录返回
        self.backId = '0000000000000000'
        self.token = None
        self.secret = None
        self.uid = None
        self.admin = None

        # 设置日志
        if not logger:
            self.logger = logging.getLogger(self.__class__.__name__)
            self.logger.setLevel(logging.DEBUG)
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
        else:
            self.logger = logger

        # 确保日志被正确传播
        # self.logger.propagate = True

    @property
    async def connected(self):
        """检查连接是否活跃"""
        if not ws_is_open(self.websocket):
            return False
        try:
            # 快速发送 Ping 测试
            await asyncio.wait_for(self.websocket.ping(), timeout=2)
            return True
        except (websockets.ConnectionClosed, asyncio.TimeoutError):
            return False

    @property
    def api(self):
        """
        封装好的接口命名空间，覆盖 tools/scan_web.py 扫到的全部接口：

            await client.api.file.ls(path='vol1/1000')          # 文件列表
            await client.api.appcgi.sysinfo.get_uptime()        # 开机时长
            await client.api.stor.list_disk()                   # 硬盘列表
            await client.api.call('file.prop', {'path': '...'}) # 通用调用

        支持的辅助方法：find(关键字) / groups() / methods(分组) /
        readonly_methods() / help(req)
        """
        if self._api_root is None:
            from .api import build_api
            self._api_root = build_api(self)
        return self._api_root

    @abstractmethod
    async def _init(self, *args, **kwargs):
        "传递给connect方法的参数，会全部传递给_init方法"
        raise NotImplementedError("子类必须实现 _init 方法")

    async def connect(self, url: str = None, *args, **kwargs):
        if url is not None:
            self.__url = url
        if self.__url:
            self.base_url = http_base_from_ws(self.__url)
        try:
            # 坑 服务器不会响应ping，他是使用消息进行ping测活， 所以关闭框架的自动ping
            # 15.x 是 ping_interval=None，17.x 已不推荐 None，这里显式关闭心跳并自己发 ping
            self.websocket = await websockets.connect(
                self.__url, ping_interval=None, open_timeout=getattr(self, 'open_timeout', 15)
            )
            # 创建监听任务
            self._listen_task = asyncio.create_task(self._listen())
            # 创建心跳任务
            self._ping_task = asyncio.create_task(self._ping_loop())

            # 初始化， 继承的类实现
            await self._init(*args, **kwargs)
        except websockets.WebSocketException as e:
            raise WebSocketConnectionError(f"Failed to connect: {str(e)}")

    async def _listen(self):
        while True:
            try:
                message = await self.websocket.recv()
                data = json.loads(message)
                self.logger.debug(f"Received: {message}")
                if 'reqid' in data:
                    reqid = data['reqid']
                    req_type = self.req_mapping.get(reqid)
                    # 录制报文（在 pop 之前拿到 req，方便推送/异常时也能对上号）
                    if self.recorder is not None:
                        self.recorder.on_recv(message, req=req_type, reqid=reqid, payload=data)
                    # 返回响应
                    if reqid in self.pending_requests:
                        handler = self.pending_requests.pop(reqid)
                        handler(data)
                    # TODO：尝试使用默认处理器抛出错误
                    # 检查错误放在这里，放在前面request一直卡
                    # check_response(data)
                    # 处理响应
                    if reqid in self.req_mapping:
                        req_type = self.req_mapping.pop(reqid)
                        handler = self.handlers.get(req_type, HandlerDefault)
                        await handler(self, data)
                    elif reqid not in self.pending_requests:
                        # reqid 对不上任何在途请求 = 迟到的异步结果/服务端消息
                        await self._dispatch_push(data)
                else:
                    # 没有 reqid 的消息 = 服务端主动推送（状态变化、任务进度等）
                    if self.recorder is not None:
                        self.recorder.on_recv(message, payload=data)
                    self.logger.debug(f"Received push: {message}")
                    await self._dispatch_push(data)
            except asyncio.CancelledError:
                break
            except websockets.ConnectionClosed as e:
                self.logger.exception(e)
                self.logger.debug(f"Websocket connection closed")
                break
            # 如果不except Exception程序会停止吗？？  会 但是主进程不会抛出错误 卡死
            except Exception as e:
                self.logger.exception(e)
        self.logger.debug(f"_listen end...")

    # ---------------- 服务端主动推送（消息） ----------------
    def add_push_handler(self, matcher=None, callback=None):
        """
        注册服务端推送的处理函数。

        :param matcher: 过滤条件，三选一
            - None 或 "*"：所有推送（包括 {"res":"pong"} 心跳回包）
            - 字符串：payload 顶层有这个键，或事件字段值等于它（常用 "notify"）
            - callable：matcher(payload) 返回真时触发
        :param callback: callback(client, payload)，可以是普通函数或协程函数

        支持装饰器写法：
            @client.add_push_handler("notify")
            def on_notify(client, payload): ...

        相关工具（sdk.push）：extract_notify(payload) 解析通知内容，
        event_of(payload) 起可读事件名。
        """
        def register(func):
            self.push_handlers.append((matcher, func))
            return func

        if callback is None:
            return register
        return register(callback)

    def remove_push_handler(self, callback=None):
        """
        注销推送处理函数；不传参数则清空全部（SDK 内部的处理函数会保留，
        比如 sdk/filetasks.py 用来等异步任务结果的嗅探器）。"""
        if callback is None:
            self.push_handlers = [(m, cb) for m, cb in self.push_handlers
                                  if getattr(cb, "_internal", False)]
        else:
            self.push_handlers = [(m, cb) for m, cb in self.push_handlers if cb is not callback]

    async def _dispatch_push(self, data):
        """把一条推送分发给所有命中的处理函数（单个回调出错不影响其它）"""
        for matcher, callback in list(self.push_handlers):
            if not push_matches(matcher, data):
                continue
            try:
                result = callback(self, data)
                if asyncio.iscoroutine(result):
                    await result
            except Exception as e:
                self.logger.exception(f"推送处理函数异常: {e}")

    async def _ping_loop(self):
        # ping_interval 传 None / 0 / 负数 表示「不发应用层心跳」。
        # 注意：不能直接进循环，否则 asyncio.sleep(None) 会抛 TypeError，
        # 被下面的 except 吞掉后立刻重试 —— 变成疯狂发 ping 的死循环
        # （实测 1 分钟能刷出十几万个 {"res":"pong"}）。
        if not self.ping_interval or self.ping_interval <= 0:
            self.logger.debug("ping_interval 未开启，跳过应用层心跳")
            return
        while True:
            try:
                await self.send_ping()
                await asyncio.sleep(self.ping_interval)
            except asyncio.CancelledError:
                break
            except websockets.ConnectionClosedError:
                await self.connect()
                # if not await self.connected:  self.logger.error(f"Error in ping loop: {str(e)}")
                break
            except Exception as e:
                self.logger.exception(e)
        self.logger.debug(f"_ping_loop end...")

    async def send_ping(self):
        try:
            await self.websocket.send(json.dumps({"req": "ping"}))
            self.logger.debug("Sent ping to server")
        except Exception as e:
            self.logger.error(f"Failed to send ping: {str(e)}")
            raise

    async def send_request(self, req, **kwargs):
        reqid = get_reqid(self.backId)
        data = {'req': req, 'reqid': reqid, **kwargs}
        logical = dict(data)          # 录制用的逻辑参数（加密前）
        if req in ['user.login', 'user.add']:
            # 加密
            data = json.dumps(data, separators=(',', ':'))
            data = login_encrypt(data, self.pub, self.key, self.iv)

        # 签名
        message = get_signature_req(data, self.sign_key)

        await self.websocket.send(message)
        self.req_mapping[reqid] = req
        if self.recorder is not None:
            self.recorder.on_send(req, reqid, params=logical, raw=message)
        self.logger.debug(f"Sent: {req} {message}")
        return reqid

    def add_handler(self, req, handler):
        self.handlers[req] = handler

    async def request(self, req, timeout=None, **kwargs):
        """
        发送请求并等待响应。
        :param timeout: 单次请求超时秒数，默认用构造函数里的 timeout，None 表示一直等
        """
        reqid = await self.send_request(req, **kwargs)
        future = asyncio.Future()
        self.pending_requests[reqid] = lambda data: future.set_result(data)
        wait = self.timeout if timeout is None else timeout
        try:
            if wait is None:
                return await future
            return await asyncio.wait_for(future, timeout=wait)
        except asyncio.TimeoutError:
            self.pending_requests.pop(reqid, None)
            self.req_mapping.pop(reqid, None)
            raise

    async def call(self, req, params=None, timeout=None, nested=False):
        """
        通用调用入口，参数用字典传，方便动态构造请求：
            await client.call('file.ls', {'path': 'vol1/1000'})
            await client.call('appcgi.resmon.cpu')

        :param nested: 把参数包一层 data 再发。部分 appcgi 接口（appcgi.sharesvr.*、
                       appcgi.mountmgr.*）的参数必须写成 {"data": {...}}，平铺发会被判定
                       为参数非法（errno 3000001 Invalid Params）。详见 docs/protocol.md。

            await client.call('appcgi.sharesvr.share.link.list', {'page': 1}, nested=True)
            # 实际发出：{"req": "...", "data": {"page": 1}}
        """
        if nested:
            return await self.request(req, timeout=timeout, data=(params or {}))
        return await self.request(req, timeout=timeout, **(params or {}))

    async def call_auto(self, req, params=None, timeout=None):
        """
        自动适配参数封装方式：先平铺发，只有明确返回「参数非法」时才改成 data 嵌套重发。

        为什么要自动试：飞牛的接口分两派 —— file.* / stor.* 参数平铺，
        appcgi.sharesvr.* 等要包 data；凭记忆很容易写错，报错又只有一句 Invalid Params。
        只有 errno 属于「参数不合法」（3000001 / 1001）且参数非空时才重试，
        这几种错误意味着请求根本没有执行，重发不会产生副作用。
        成功用哪种写法会记进 client.nested_reqs，之后同一接口直接走对的那种。

        想完全掌控报文形状时请用 client.call(..., nested=True/False)。
        """
        merged = dict(params or {})
        if req in self.nested_reqs:
            return await self.call(req, merged, timeout=timeout, nested=True)
        resp = await self.call(req, merged, timeout=timeout)
        if merged and _is_invalid_params(resp):
            retry = await self.call(req, merged, timeout=timeout, nested=True)
            if not _is_invalid_params(retry):
                self.nested_reqs.add(req)
            return retry
        return resp

    async def close(self, timeout: float = 5.0):
        """关闭连接并取消所有任务"""
        tasks = []
        if self._ping_task:
            self._ping_task.cancel()
            tasks.append(self._ping_task)
        if self._listen_task:
            self._listen_task.cancel()
            tasks.append(self._listen_task)
        if self.websocket is not None:
            try:
                await self.websocket.close()
            except Exception:
                pass
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        # 未完成的请求直接放弃，避免调用方永远挂着
        self.pending_requests.clear()
        self.logger.info("Connection closed.")

    def run_polling(
        self,
        *,
        stop_signals: Optional[List[int]] = None,
        close_timeout: float = 5.0,
    ):
        """
        同步方法：启动事件循环并运行 WebSocket 监听，直到收到停止信号。
        用法：
            client = BaseClient(url)
            client.run_polling()  # 阻塞直到 Ctrl+C
        """
        if stop_signals is None:
            stop_signals = [signal.SIGINT, signal.SIGTERM]  # 默认监听 Ctrl+C 和 kill

        # 定义异步主逻辑
        async def _async_main():
            await self.connect()
            stop_event = asyncio.Event()
            # 注册信号处理器
            loop = asyncio.get_running_loop()
            for sig in stop_signals:
                loop.add_signal_handler(sig, stop_event.set)

            self.logger.info("Client started. Press Ctrl+C to stop...")
            await stop_event.wait()  # 阻塞直到收到信号
            await self.close(timeout=close_timeout)

        # 启动事件循环
        try:
            asyncio.run(_async_main())
        except KeyboardInterrupt:
            self.logger.info("User interrupted, shutting down...")
        finally:
            self.logger.info("Client stopped.")


class MainClient(BaseClient):
    async def _init(self):
        await super()._init()
        # 这里注册回调函数，如果要给MainClient加处理请求，在这里加
        self.add_handler('util.crypto.getRSAPub', HandlerGetRSAPub)
        self.add_handler('user.login', HandlerLogin)
        # 连接后执行的方法
        await self.request(req='util.crypto.getRSAPub')

    async def login(self, username, password, *, deviceType='Browser', deviceName='Windows-Google Chrome',
                    stay=False):
        data = {
            "user": username,
            "password": password,
            "deviceType": deviceType,
            "deviceName": deviceName,
            "stay": stay,
            "si": self.si
        }
        response = await self.request('user.login', **data)
        return response

    async def user_info(self):
        response = await self.request('user.info')
        return response

    async def setting_port(self, force_https=False, redirect=True, http_port=5666, https_port=5667):
        "修改端口"
        data = {
            "data": {
                "force_https": force_https,  # 强制Https
                "redirect": redirect,  # 80和443跳转
                "schema": {
                    "http": {
                        "port": http_port
                    },
                    "https": {
                        "port": https_port
                    }
                }
            }
        }
        response = await self.request('appcgi.network.gw.setting', **data)
        return response

    async def get_user_storage(self):
        "获取磁盘信息"
        data = {
            "quotaInfo": True,
            "spaceInfo": True,
            "storInfo": True
        }
        response = await self.request("stor.getUserStorage", **data)
        return response


class FileClient(BaseClient):
    async def _init(self):
        await super()._init()
        self.add_handler('util.getSI', HandlerGetSI)
        self.add_handler('user.authToken', HandlerAuthToken)
        # self.add_handler('file.ls', HandlerFileList)
        self.file_update_queue = asyncio.Queue()

        # 创建更新文件的任务
        update_file_task = asyncio.create_task(self._update_file())

    async def getSI(self):
        await self.request(req='util.getSI')

    async def authToken(self):
        await self.getSI()
        data = {
            "si": self.si,
            "token": self.token,
        }
        await self.request(req='user.authToken', **data)

    async def fileList(self, path=None):
        data = {
            "path": path,
        }
        return await self.request(req='file.ls', **data)

    async def upload(self, local_path, nas_path, overwrite=2):
        """
        :param local_path: 本地文件路径（绝对或相对路径）
        :param nas_path:  NAS文件绝对路径
        :param overwrite: 0跳过 1上传并覆盖 2保留两者
        :return: dict(status_code, file_name, upload_name, url)
        """
        from pathlib import Path
        nas_path = Path(nas_path)
        folder = nas_path.parent.as_posix()
        file_name = nas_path.name
        # 获取修改时间
        mtim = str(get_mtime(local_path))
        # checkUpload
        res = await self._checkUpload(local_path, nas_path.as_posix(), overwrite)
        uploadName = res.get('uploadName')

        if not self.base_url:
            raise RuntimeError("尚未 connect，无法确定上传地址（base_url 为空）")
        url = f'{self.base_url}/upload'
        headers = {
            'Referer': f'{self.base_url}/p/assets/upload.worker.js',
            'Trim-Overwrite': str(overwrite),
            'Trim-Token': self.token,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Trim-Mtim': mtim,
            'Trim-Path': f'{folder}/{uploadName}',
        }
        headers['Trim-Sign'] = get_signature(headers['Trim-Path'], self.sign_key)
        import requests
        import mimetypes
        mime_type, encoding = mimetypes.guess_type(local_path)
        with open(local_path, 'rb') as fp:
            files = {"trim-upload-file": (file_name, fp, mime_type)}
            res = requests.post(url=url, headers=headers, files=files)
        self.logger.info(f"upload {file_name} -> {res.status_code}")
        return {
            'status_code': res.status_code,
            'file_name': file_name,
            'upload_name': uploadName,
            'url': url,
        }

    # async def download(self):
    #     # http://192.168.1.4:5666/multiple-download?token=0
    #     pass

    async def _checkUpload(self, local_path, nas_path, overwrite=2):
        size = os.path.getsize(local_path)
        data = {
            "size": size,
            "path": nas_path,
            "overwrite": overwrite,  # 重写规则   0跳过 1上传并覆盖 2保留两者
        }
        res = await self.request(req='file.checkUpload', **data)
        return res

    async def _update_file(self):
        "这是一个内部方法，用来更新文件，服务于start_observer"
        while True:
            # 这里要使用异步方法get，阻塞到get数据为止
            local_path, nas_path, action = await self.file_update_queue.get()
            print(local_path, nas_path, action)
            if action == 'u':
                await self.upload(local_path, nas_path, overwrite=1)
            elif action == 'd':
                await self.download()

    async def start_observer(self, nas_path=None, local_path=os.getcwd(), recursive=False, interval=5,
                             exclude: list = None):
        """
        启动文件变化监听， 原理是对比NAS和本地的修改时间谁更新
        :param nas_path: NAS路径 默认我的文件路径
        :param local_path: 本地路径 默认程序工作路径
        :param interval: 每次轮询间隔时间 5
        :param recursive: 是否递归 默认False
        :param exclude: 排除指定后缀
        :return: None
        """
        if exclude is None:
            exclude = []
        while True:
            res = await self.fileList(path=nas_path)
            nas_files = res.get('files', [])
            nas_dict = {file['name']: file['mtim'] for file in nas_files}
            local_files = {}
            local_path_dict = {}
            # 扫描本地文件 TODO: 使用文件变化监听可能是更好的实践，拥有更好的性能，如开源项目Watchdog，但会增加项目复杂度
            for name, file_path, mtime in list_files(local_path, recursive=recursive):
                # TODO 排除指定后缀
                if name in exclude:
                    continue
                local_files[name] = mtime
                local_path_dict[name] = file_path
            # 迭代NAS文件，检查新增、对比那端有更新
            # TODO: 实现文件实际更新 上传已实现
            # 思路： 创建一个异步队列，把需要更新的操作put到队列，写一个异步任务来执行实际的文件更新
            # 分析: 实际上就一个上传和一个下载， 上传已经实现
            #   操作1：下载到本地
            #   操作2：上传到NAS
            # TODO: 上传：递归文件路径不对 下载： NAS不能递归
            # 上传解决思路：替换路径，nas路径最终路径=本地目录去掉根目录部分
            # 问题1， NAS不能显示所有子目录
            # 解决思路1 如果是递归， 给self.fileList加递归参数，一次性返回所有路径, 考虑使用生成器返回
            for name, nas_mtim in nas_dict.items():
                if name in local_files:
                    local_mtim = local_files[name]
                    if nas_mtim > local_mtim:
                        # NAS文件较新，更新本地文件
                        print(f"文件 '{name}' 在NAS上较新，更新到本地。")
                        # 不知道用put还是put_nowait, AI说没区别，强迫症好难选
                        # 看了代码，put最后调用put_nowait，使用put_nowait
                        self.file_update_queue.put_nowait((local_path_dict[name], f'{nas_path}/{name}', 'd'))
                    elif nas_mtim < local_mtim:
                        # 本地文件较新，更新NAS文件
                        print(f"文件 '{name}' 在本地较新，更新到NAS。")
                        print(name, nas_mtim, local_mtim)
                        self.file_update_queue.put_nowait((local_path_dict[name], f'{nas_path}/{name}', 'u'))
                else:
                    # 本地不存在该文件，将其从NAS复制到本地
                    print(f"本地不存在文件 '{name}'，从NAS复制到本地。")
                    self.file_update_queue.put_nowait((f'{local_path}/{name}', f'{nas_path}/{name}', 'd'))

            for name in local_files.keys():
                if name not in nas_dict:
                    # NAS不存在该文件，将其从本地复制到NAS
                    print(f"NAS不存在文件 '{name}'，从本地复制到NAS。")
                    self.file_update_queue.put_nowait((local_path_dict[name], f'{nas_path}/{name}', 'u'))
            await asyncio.sleep(interval)

    async def file_search(self, key: str, path: list):
        data = {
            "key": key,
            "path": path,
        }
        res = await self.request("appcgi.finder.fileSearch", **data)
        return res

class DownloadClient(BaseClient):
    async def _init(self):
        await super()._init()

    async def download(self, url: Union[list[str], str], save_path: str = None) -> bool:
        """
        下载文件
        :param url: 下载链接
        :param save_path: 保存路径
        :return: bool
        """
        if isinstance(url, str):
            url = [url]
        data = {
            "select_files": False,
            "uris": url
        }
        if save_path is None:
            res = await self.request(req='appcgi.downloadcenter.task.addUris', **data)
        else:
            # 记录默认保存路径
            default_save_path = await self.get_default_save_dir()
            if not await self.is_dir(save_path):
                await self.mkdir(save_path)
            await self.set_save_dir(save_path)
            res = await self.request(req='appcgi.downloadcenter.task.addUris', **data)
            # 恢复默认保存路径
            await self.set_save_dir(default_save_path)
        return  res.get("result") == "succ"

    async def get_default_save_dir(self) -> str:
        """
        获取默认保存目录
        :return: str
        """
        res = await self.request(req='appcgi.downloadcenter.config.getDefaultSaveDir')
        return res["data"]["rsp"]

    async def set_save_dir(self, save_dir: str) -> bool:
        """
        设置默认保存目录
        :param save_dir: NAS路径
        :return: bool
        """
        res = await self.request(req='appcgi.downloadcenter.config.setDefaultSaveDir', default_save_dir=save_dir)
        return  res.get("result") == "succ"

    async def mkdir(self, nas_path: str) -> bool:
        """
        创建目录
        :param nas_path: NAS路径
        :return: bool
        """
        res = await self.request(req='file.mkdir', path=nas_path)
        return  res.get("result") == "succ"

    async def is_dir(self, nas_path: str) -> bool:
        """
        判断目录是否存在
        :param nas_path: NAS路径
        :return: bool
        """
        res = await self.request(req='file.ls', path=nas_path)
        if res.get("result") == "fail" and res.get("errno") == 4100:
            return False
        elif res.get("result") == "succ":
            return True
        elif res.get("files") is not None:
            return True
        else:
            raise Exception(res)

    async def file_list(self, nas_path: str=None) -> List[dict]:
        """
        获取文件列表
        :param nas_path: NAS上的绝对路径，当值为None时返回当前用户文件
        :return: 返回一个文件列表, 如果没有目录则返回None
        example:[{"name": "文件夹A", "v": 3, "uid": 1000, "dir": 1},{"name": "文件夹B", "v": 2, "uid": 1000, "dir": 1}]
        """
        if nas_path is None:
            res = await self.request(req='file.ls')
        else:
            res = await self.request(req='file.ls', path=nas_path)
        if res.get("result") == "succ":
            file_list = res.get("files")
        elif res.get("result") == "fail" and res.get("errno") == 4100: # 目录不存在
            print(f"目录 '{nas_path}' 不存在")
            file_list = None
        else:
            raise Exception(res)
        return  file_list

    async def file_tree(self, nas_path: str=None, max_depth: int=1) -> List[dict]:
        """
        使用迭代方式获取完整的文件树结构
        :param nas_path: NAS路径，None表示根目录
        :param max_depth: 最大递归深度，防止无限递归
        :return: 包含完整目录结构的文件树
        example:
        [
            {"name": "文件夹A", "v": 3, "uid": 1000, "dir": 1,
             "files": [{"name": "文件夹AA", "v": 2, "uid": 1000, "dir": 1, "files": [...]}]},
            {"name": "文件夹B", "v": 2, "uid": 1000, "dir": 1}
        ]
        """
        from collections import deque
        root_files = await self.file_list(nas_path)
        queue = deque()
        for item in root_files:
            if item.get("dir") == 1:
                if nas_path is None:
                    item_path = f"vol{item['v']}/{item['uid']}/{item['name']}"
                else:
                    item_path = f"{nas_path}/{item['name']}"
                queue.append((item, item_path, 1))
        while queue:
            dir_item, dir_path, depth = queue.popleft()

            if depth > max_depth:
                self.logger.warning(f"Reached max depth {max_depth}, skipping: {dir_path}")
                dir_item["files"] = []
                continue
            try:
                sub_files = await self.file_list(dir_path)
                dir_item["files"] = sub_files
                for sub_item in sub_files:
                    if sub_item.get("dir") == 1:
                        sub_path = f"{dir_path}/{sub_item['name']}"
                        queue.append((sub_item, sub_path, depth + 1))
            except Exception as e:
                self.logger.warning(f"Failed to list directory {dir_path}: {e}")
                dir_item["files"] = []
        return root_files

class EmptyClient(BaseClient):
    async def _init(self):
        pass


class FnOsClient(FileClient, MainClient, SystemApiMixin, StorageApiMixin, FileOpsApiMixin,
                 ShareApiMixin, EmptyClient, DownloadClient):
    """
    这里有个坑， 以后增加客户端， 请在EmptyClient前面继承
    如果在EmptyClient后面继承，就会调用BaseClient的_init
    导致抛出NotImplementedError异常，这不是我们想要的结果
    所以写了一个EmptyClient, 让它不调用BaseClient的_init
    此时的MRO是FnOsClient=>MainClient=>FileClient=>EmptyClient=>BaseClient ...
    由于EmptyClient没有调用super()._init() 所以不会调用到BaseClient的_init

    SystemApiMixin / StorageApiMixin / FileOpsApiMixin / ShareApiMixin 是只加方法的封装层
    （sdk/api/curated.py），放在 EmptyClient 前面，不影响 _init 链路。
    """

    async def _init(self):
        await super()._init()
