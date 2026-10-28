# -*- coding: utf-8 -*-
"""
服务端主动推送（消息）的处理工具。

飞牛会推两类「没有 reqid」的报文：

    1. 心跳回包        {"res": "pong"}
    2. 业务通知        {"notify": [{"title": ..., "content": "{...json...}", ...}]}
                       或者迟到的异步结果 {"result": "succ", "data": {...}}

用法：

    def on_notify(client, payload):
        for item in extract_notify(payload):
            print(item["title"], item.get("data"))

    client.add_push_handler("notify", on_notify)     # 只关心带 notify 的推送
    client.add_push_handler(None, lambda c, p: print("push:", p))   # 全都要

    # 也可以做条件过滤
    client.add_push_handler(lambda p: "entryChange" in json.dumps(p), cb)
"""

import json

# 常见的事件字段名，推送里可能是顶层字段，也可能在 data 里
EVENT_KEYS = ("event", "eventId", "type", "cmd", "action", "res")


def push_matches(matcher, payload):
    """
    判断一条推送是否命中 matcher：

        None / "*"        任意推送
        字符串             payload 顶层有这个键，或者事件字段的值等于它
        可调用对象         matcher(payload) 为真
    """
    if matcher is None or matcher == "*":
        return True
    if callable(matcher):
        try:
            return bool(matcher(payload))
        except Exception:
            return False
    if not isinstance(matcher, str):
        return False
    if not isinstance(payload, dict):
        return False
    if matcher in payload:
        return True
    for key in EVENT_KEYS:
        if payload.get(key) == matcher:
            return True
    data = payload.get("data")
    if isinstance(data, dict):
        for key in EVENT_KEYS:
            if data.get(key) == matcher:
                return True
        if matcher in data:
            return True
    return False


def extract_notify(payload):
    """
    把推送里的通知列表整理成统一结构：

        [{"title":..., "level":..., "time":..., "from":..., "event":..., "data": <解析后的 content>}]

    只处理形如 {"notify": [...]} 的推送，其它返回空列表。
    """
    if not isinstance(payload, dict):
        return []
    items = payload.get("notify")
    if isinstance(items, dict):
        items = [items]
    if not isinstance(items, list):
        return []
    out = []
    for item in items:
        if not isinstance(item, dict):
            continue
        info = dict(item)
        content = item.get("content")
        if isinstance(content, str) and content.strip().startswith("{"):
            try:
                data = json.loads(content)
                info["data"] = data
                if isinstance(data, dict):
                    info.setdefault("event", data.get("eventId") or data.get("event"))
                    if data.get("title") and not info.get("title"):
                        info["title"] = data["title"]
            except Exception:
                pass
        out.append(info)
    return out


def is_pong(payload):
    """是不是心跳回包"""
    return isinstance(payload, dict) and payload.get("res") == "pong"


def event_of(payload):
    """给一条推送起个可读的名字，方便日志/统计（tools/watch.py 也用这个）"""
    if not isinstance(payload, dict):
        return "non-json"
    if is_pong(payload):
        return "pong"
    if "notify" in payload:
        items = extract_notify(payload)
        if items:
            first = items[0]
            return f"notify:{first.get('from', '?')}:{first.get('event') or 'item'}"
        return "notify"
    for key in EVENT_KEYS:
        if key in payload:
            return f"{key}={payload[key]}"
    data = payload.get("data")
    if isinstance(data, dict):
        for key in EVENT_KEYS:
            if key in data:
                return f"data.{key}={data[key]}"
    return "push:" + ",".join(sorted(payload.keys())[:4])
