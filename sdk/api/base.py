# -*- coding: utf-8 -*-
"""
fnOS 接口封装层：把抓取到的所有 req 暴露成可点出来的 API。

设计目标：
    1. 接口元数据集中在 `sdk/api/spec.py`（由 tools/gen_api.py 自动生成），
       不用手写几百个重复方法；
    2. 调用形态友好，支持逐级命名空间：

        await client.api.file.ls(path='vol1/1000')
        await client.api.appcgi.network.net_list()
        await client.api.stor.list_disk()
        await client.api.call('file.prop', {'path': '/vol1/1000/a.jpg'})

    3. 每个方法带 docstring：req 名、实测状态、是否只读、已知参数、响应字段；
    4. 未知接口不用记：`client.api.find('disk')`、`client.api.help('stor.listDisk')`、
       `dir(client.api.file)` 看全部方法。

安全提示：
    spec 里 `readonly=False` 的是写接口（删除/重启/格式化等），SDK 只封装，
    不会自动调用；`client.api.readonly_methods()` 可以只看安全的只读接口。
"""

from .spec import SPEC, META, ALIASES, SAMPLE_KEYS, RESERVED_METHOD_NAMES

STATUS_TEXT = {
    "succ": "已实测通过",
    "param_error": "已实测存在（缺参数）",
    "error": "已实测存在（返回业务错误码）",
    "timeout": "实测超时（可能是耗时接口）",
    "unverified": "未实测（写接口，静态扫描得到）",
    "unknown": "实测不存在（静态扫描误报）",
    "other": "实测返回非标准结构",
}


class ApiMethod:
    """一个接口的可调用封装（由 ApiNamespace 动态创建并缓存）"""

    def __init__(self, client, req, meta):
        self._client = client
        self.req = req
        self.group, self.method_name, self.status, self.flags, self.params = meta
        self.readonly = "r" in self.flags
        self.aliases = ALIASES.get(req, [])
        self.sample_keys = SAMPLE_KEYS.get(req, [])
        self.__name__ = self.method_name
        self.__qualname__ = f"{self.group}.{self.method_name}"
        self.__doc__ = self.build_doc()

    def build_doc(self):
        lines = [f"[{self.req}] {STATUS_TEXT.get(self.status, self.status)}"]
        line2 = "只读接口" if self.readonly else "⚠ 写接口，会修改 NAS 数据"
        if self.params:
            line2 += f"；已知参数: {self.params}"
        lines.append(line2)
        if self.sample_keys:
            lines.append(f"响应字段: {', '.join(self.sample_keys)}")
        if self.aliases:
            lines.append(f"前端别名: {', '.join(self.aliases)}")
        lines.append("")
        lines.append(f"调用: await client.api.{self.group}.{self.method_name}(...)")
        return "\n".join(lines)

    async def __call__(self, params=None, timeout=None, **kwargs):
        merged = dict(params) if params else {}
        merged.update(kwargs)
        return await self._client.call(self.req, merged, timeout=timeout)

    def __repr__(self):
        return f"<ApiMethod {self.req} ({self.status}{', readonly' if self.readonly else ', WRITE'})>"


class ApiNamespace:
    """接口命名空间，支持 .file / .appcgi.network 这种逐级访问"""

    def __init__(self, client, path=()):
        self._client = client
        object.__setattr__(self, "_path", tuple(path))

    # ---------- 内部 ----------
    def _children(self):
        depth = len(self._path)
        kids = set()
        for meta in SPEC.values():
            parts = meta[0].split(".")
            if parts[:depth] == list(self._path) and len(parts) > depth:
                kids.add(parts[depth])
        return kids

    def _methods(self):
        group = ".".join(self._path)
        return {meta[1]: req for req, meta in SPEC.items() if meta[0] == group}

    # ---------- 属性访问 ----------
    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)
        if name in self._children():
            ns = ApiNamespace(self._client, self._path + (name,))
            object.__setattr__(self, name, ns)
            return ns
        methods = self._methods()
        if name in methods:
            m = ApiMethod(self._client, methods[name], SPEC[methods[name]])
            object.__setattr__(self, name, m)
            return m
        similar = [n for n in list(self._children()) + list(methods)
                   if name.lower() in n.lower() or n.lower() in name.lower()]
        hint = f"，你是想找 {'/'.join(sorted(similar)[:5])} 吗？" if similar else \
            "，可以用 client.api.find('关键字') 搜索"
        raise AttributeError(
            f"接口命名空间 '{'.'.join(self._path) or 'api'}' 下没有 '{name}'{hint}")

    def __dir__(self):
        return sorted(set(self._children()) | set(self._methods())
                      | {"call", "find", "help", "methods", "groups", "readonly_methods"})

    # ---------- 通用入口 ----------
    async def call(self, req, params=None, timeout=None, **kwargs):
        """直接调用任意接口：await client.api.call('file.ls', {'path': ...})"""
        merged = dict(params) if params else {}
        merged.update(kwargs)
        return await self._client.call(req, merged, timeout=timeout)

    def methods(self, group=None):
        """列出一组接口：client.api.methods('file') -> {方法名: req}"""
        if group is None:
            group = ".".join(self._path)
        if not group:
            return {meta[1]: req for req, meta in SPEC.items()}
        return {meta[1]: req for req, meta in SPEC.items() if meta[0] == group}

    def groups(self):
        """列出所有分组及接口数量"""
        out = {}
        for meta in SPEC.values():
            out[meta[0]] = out.get(meta[0], 0) + 1
        return dict(sorted(out.items()))

    def readonly_methods(self):
        """只列只读接口（可以放心调用）"""
        return {meta[1]: req for req, meta in SPEC.items()
                if "r" in meta[3] and meta[2] != "unknown"}

    def find(self, keyword):
        """按关键字搜索接口，返回 {req: 状态}"""
        kw = keyword.lower()
        return {req: meta[2] for req, meta in SPEC.items() if kw in req.lower()}

    def help(self, req):
        """查看某个接口的封装说明"""
        if req not in SPEC:
            return (f"没有 {req}；可用 client.api.find('关键字') 搜索，"
                    f"共封装 {META.get('count', len(SPEC))} 个接口")
        return ApiMethod(None, req, SPEC[req]).build_doc()

    def __repr__(self):
        path = ".".join(self._path) or "api"
        return (f"<ApiNamespace {path} groups={len(self._children())} "
                f"methods={len(self._methods())} total={META.get('count', len(SPEC))}>")


def build_api(client):
    """给 client 造一个 api 根节点"""
    return ApiNamespace(client, ())


__all__ = ["ApiNamespace", "ApiMethod", "build_api", "SPEC", "META", "ALIASES",
           "SAMPLE_KEYS", "RESERVED_METHOD_NAMES", "STATUS_TEXT"]
