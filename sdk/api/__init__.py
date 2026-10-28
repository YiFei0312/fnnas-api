# -*- coding: utf-8 -*-
"""
fnOS API 封装层。

    client.api.file.ls(path='vol1/1000')      # 命名空间调用
    client.api.call('file.prop', {'path': ...})  # 通用调用
    client.api.find('disk')                    # 搜索接口
"""

from .base import ApiNamespace, ApiMethod, build_api, SPEC, META, STATUS_TEXT

__all__ = ["ApiNamespace", "ApiMethod", "build_api", "SPEC", "META", "STATUS_TEXT"]
