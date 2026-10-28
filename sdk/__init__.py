# -*- coding: utf-8 -*-
"""
fnOS SDK。

这里用 PEP 562 的模块级 __getattr__ 做懒加载：`sdk.safety`、`sdk.api.spec`
这类离线工具链不需要 websockets / pycryptodome / watchdog 也能 import，
只有真正用到 FnOsClient 时才去加载重依赖。

坑：`from sdk import FnOsClient` 时，Python 的 import 机制会先把同名子模块
`sdk.FnOsClient` 塞进包里当属性，从而盖住 __getattr__ 的返回值（拿到的是模块
而不是类）。所以这里 import 完子模块后，显式把类写回模块全局变量。
"""

__all__ = ["FnOsClient", "AsyncFileEventHandler", "wait_file_task", "is_task_ok",
           "task_error", "call_file_task"]


def __getattr__(name):
    if name == "FnOsClient":
        from .FnOsClient import FnOsClient as _cls
        globals()["FnOsClient"] = _cls          # 覆盖 import 机制塞进来的同名子模块
        return _cls
    if name == "AsyncFileEventHandler":
        from .handlers import AsyncFileEventHandler as _cls
        globals()["AsyncFileEventHandler"] = _cls
        return _cls
    if name in ("wait_file_task", "is_task_ok", "task_error", "call_file_task"):
        from . import filetasks
        value = getattr(filetasks, name)
        globals()[name] = value
        return value
    raise AttributeError(f"module 'sdk' has no attribute {name!r}")
