# -*- coding: utf-8 -*-
"""
文件异步任务的结果等待器。

**为什么要这个模块**：`file.cp` / `file.mv` / `file.rm` / `file.compress` / `file.extract`
/ `file.setAcl2` / `file.chown` / `file.usage` 这些接口是**异步任务**，WebSocket 上的返回
只是一个「收到任务」的 ack：

.. code-block:: json

    {"sysNotify": "taskId", "taskId": "OdkhlbCaRg+61xHFGLc29w==", "reqid": "..."}

真正的成败是**同 `reqid` 的推送**：

.. code-block:: json

    {"sysNotify": "taskInfo", "taskInfo": {"req": "file.cp", "reqid": "...", ...}}
    {"percent": 100, "size": 1880200, "sizeTotal": 1880200, "reqid": "..."}
    {"result": "succ", "reqid": "..."}
    {"result": "fail", "reqid": "...", "failedFilesCount": 1,
     "failedFiles": [{"file": "/vol1/...", "errno": 4100}]}

只看 ack 会以为「复制成功了」，其实任务可能失败（实测 `file.mv` 源文件不存在时
ack 是 succ、推送才是 fail）。所以正确姿势是：

.. code-block:: python

    resp = await client.file_cp([src], dst)
    result = await wait_file_task(client, resp["reqid"])     # None = 超时
    if not is_task_ok(result):
        raise RuntimeError(result)
"""

import asyncio

_STATE_ATTR = "_file_task_state"


def install_sniffer(client):
    """
    给 client 挂一个常驻的推送嗅探器，缓存「带 result 的推送」。

    `BaseClient.__init__` 里已经自动调用了，所以任务结果不会漏；
    自己造的假客户端（测试）想用 `wait_file_task` 就手动调一下。
    """
    state = getattr(client, _STATE_ATTR, None)
    if state is not None:
        return state
    state = {"events": {}, "results": {}}

    def on_push(_client, payload):
        reqid = payload.get("reqid")
        if not reqid or "result" not in payload:
            return
        state["results"][reqid] = payload
        event = state["events"].get(reqid)
        if event is not None and not event.is_set():
            event.set()

    on_push._internal = True          # remove_push_handler() 清空时不会误删它
    client.add_push_handler(None, on_push)
    setattr(client, _STATE_ATTR, state)
    return state


_sniffer = install_sniffer


async def wait_file_task(client, reqid, timeout=120):
    """
    等某个异步文件任务的结果。

    :param client: 已连接（且已开启推送分发）的客户端
    :param reqid: 发起请求时返回的 reqid（`resp["reqid"]`）
    :param timeout: 超时秒数
    :return: 结果推送 dict（`{"result": "succ"|"fail", ...}`），超时返回 None

    注意：嗅探器是**常驻**的（`BaseClient.__init__` 里就装好了），所以哪怕结果推送
    比 `wait_file_task` 调用更早到，也能拿到。
    """
    state = _sniffer(client)
    if reqid in state["results"]:
        return state["results"][reqid]
    event = state["events"].setdefault(reqid, asyncio.Event())
    try:
        await asyncio.wait_for(event.wait(), timeout)
    except asyncio.TimeoutError:
        return None
    return state["results"].get(reqid)


def is_task_ok(result):
    """任务结果是否成功（None / 缺 result 都算失败）"""
    return bool(isinstance(result, dict) and result.get("result") == "succ")


def task_error(result):
    """把失败的任务结果压成一句人能看的错误信息"""
    if not isinstance(result, dict):
        return "任务没有回结果（超时）"
    failed = result.get("failedFiles") or []
    if failed:
        detail = "; ".join(f"{f.get('file')}: errno={f.get('errno')}" for f in failed[:5])
    else:
        detail = result.get("errmsg") or f"errno={result.get('errno')}"
    return f"任务失败：{detail}"


async def call_file_task(client, req, params=None, timeout=120):
    """
    发一个异步文件任务并等结果：返回 `(resp, result)`。

    `resp` 是 ack（含 reqid），`result` 是最终推送（可能是 None = 超时）。
    """
    resp = await client.call(req, params or {})
    reqid = (resp or {}).get("reqid")
    if not reqid:
        return resp, None
    return resp, await wait_file_task(client, reqid, timeout=timeout)
