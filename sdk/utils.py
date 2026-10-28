import time
import random
import os
from urllib.parse import urlparse

from .exceptions import BadRequestError


def ws_is_open(ws) -> bool:
    """
    判断 websockets 连接是否还活着。
    websockets 15 及以前是 ws.closed，17 起换成了 ws.state（State.OPEN），
    这里做个兼容，避免 SDK 被库版本绑死。
    """
    if ws is None:
        return False
    closed = getattr(ws, "closed", None)
    if closed is not None:
        return not closed
    state = getattr(ws, "state", None)
    name = getattr(state, "name", None)
    if name:
        return name == "OPEN"
    return True


def http_base_from_ws(url: str) -> str:
    """
    由 websocket 地址推导 http 基地址：
        ws://192.168.1.4:5666/websocket?type=main -> http://192.168.1.4:5666
        wss://nas.example.com/websocket          -> https://nas.example.com
    """
    p = urlparse(url)
    scheme = {"ws": "http", "wss": "https", "http": "http", "https": "https"}.get(p.scheme, "http")
    path = p.path or ""
    for suffix in ("/websocket", "/ws"):
        if suffix in path:
            path = path.split(suffix)[0]
            break
    return f"{scheme}://{p.netloc}{path.rstrip('/')}"


def _get_reqid():
    index = 1

    def func(backId='0000000000000000'):
        nonlocal index
        t = format(int(time.time()), 'x').zfill(8)
        e = format(index, 'x').zfill(4)
        index += 1
        return f"{t}{backId}{e}"

    return func


get_reqid = _get_reqid()


# 生成随机字符串
def generate_random_string(t):
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return ''.join(random.choice(chars) for _ in range(t))


def check_response(response: dict):
    """检查响应，如果包含错误代码则抛出异常"""
    if "errno" in response:
        error_code = response["errno"]
        raise BadRequestError(error_code)


def get_mtime(path) -> int:
    # 也可以用Path(file_path).stat().st_mtime
    mod_time = int(os.path.getmtime(path))
    return mod_time


def list_files(path: str, recursive: bool = False):
    for root, dirs, files in os.walk(path):
        if recursive is not True and path != root:
            break
        for file in files:
            file_path = os.path.join(root, file)
            mtime = get_mtime(file_path)
            yield file, file_path, mtime