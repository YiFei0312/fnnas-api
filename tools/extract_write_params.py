#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 `/p`（相册应用）的前端产物里，把接口的**请求参数字段**挖出来。

为什么需要单独的脚本：
    `tools/scan_http.py` 只能看到 RTK Query 的定义，参数在那里通常是这样透传的：

        create: e.mutation({query: e => ({url: `/api/v1/album/create`,
                                          method: `post`, body: e})})
        getList: e.query({query: e => ({url: `/api/v1/album/list`, params: e})})

    `body: e` / `params: e` 说明「请求参数就是调用时传进来的对象」，字段名在**调用点**。
    而调用点隔着两层别名（hook 变量 → 导出名 → 导入别名），压缩后的产物里全是
    `o` / `Ue` / `h` 这种单字母，所以这里做一个迷你「模块图 + 别名链」解析：

        定义 chunk：{useCreateShareLinkMutation: o} ... export{... o as i ...}
        使用 chunk：import{i as h}from"./B8RasvHeFEYlBmIA2.js"
        调用点：    const [h] = _(); await h({name: …, validTo: …, password: …})

用法：
    python tools/scan_http.py                    # 先有接口清单
    python tools/extract_write_params.py         # 再补参数（就地更新 data/http_api.json）
    python tools/extract_write_params.py --show album/create
    python tools/extract_write_params.py --dry-run

产出（写回 data/http_api.json 的每个 endpoint）：
    params_keys / body_keys   顶层字段名（用逗号分隔的字符串也保留原样）
    param_source              inline | call_site | call_site_var | 未解析
    param_evidence            1~3 条证据片段（反编译出来的原始代码）
"""

import argparse
import json
import os
import re
import sys
import time
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))

ASSET_DIR = os.path.join(ROOT, "data", "web-cache", "p", "assets")
HTTP_JSON = os.path.join(ROOT, "data", "http_api.json")

IMPORT_RE = re.compile(r'import\{([^}]*)\}from"\./([A-Za-z0-9_\-]+\.js)"')
EXPORT_RE = re.compile(r"export\{([^}]*)\}")
REDUCER_RE = re.compile(r"reducerPath\s*:\s*[`'\"]([A-Za-z0-9_$]+)[`'\"]")
ENDPOINT_RE = re.compile(r"([A-Za-z_$][\w$]*)\s*:\s*e\.(query|mutation)\s*\(\s*\{\s*query\s*:")
URL_RE = re.compile(r"url\s*:\s*[`'\"]([^`'\"]+)[`'\"]")
METHOD_RE = re.compile(r"method\s*:\s*[`'\"]([A-Za-z]+)[`'\"]")
INLINE_BODY_RE = re.compile(r"\bbody\s*:\s*\{")
INLINE_PARAMS_RE = re.compile(r"\bparams\s*:\s*\{")


# ------------------------------------------------------------------ 模块图
def split_spec(spec):
    out = []
    for item in spec.split(","):
        item = item.strip()
        if not item:
            continue
        if " as " in item:
            a, b = item.split(" as ")
            out.append((a.strip(), b.strip()))
        else:
            out.append((item, item))
    return out


def load_modules(asset_dir=ASSET_DIR):
    modules = {}
    for name in sorted(os.listdir(asset_dir)):
        if not name.endswith(".js"):
            continue
        with open(os.path.join(asset_dir, name), encoding="utf-8", errors="replace") as f:
            text = f.read()
        imports = {}
        for m in IMPORT_RE.finditer(text):
            for exported, local in split_spec(m.group(1)):
                imports[exported] = local
        exports = {}
        for m in EXPORT_RE.finditer(text):
            for local, exported in split_spec(m.group(1)):
                exports.setdefault(local, exported)
        modules[name] = {"text": text, "imports": imports, "exports": exports}
    return modules


# --------------------------------------------------------------- 端点定义
def object_span(text, start):
    """从 text[start] == '{' 开始，返回匹配的 '}' 下标"""
    depth, i, quote = 0, start, None
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in "`'\"":
            quote = ch
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def top_level_keys(obj_text):
    body = obj_text.strip()
    if body.startswith("{"):
        body = body[1:]
    if body.endswith("}"):
        body = body[:-1]
    keys, depth, quote, cur = [], 0, None, ""
    i = 0
    while i < len(body):
        ch = body[i]
        if quote:
            cur += ch
            if ch == "\\":
                cur += body[i + 1] if i + 1 < len(body) else ""
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in "`'\"":
            quote = ch
            cur += ch
        elif ch in "{[(":
            depth += 1
            cur += ch
        elif ch in "}])":
            depth -= 1
            cur += ch
        elif ch == "," and depth == 0:
            _add_key(keys, cur)
            cur = ""
        else:
            cur += ch
        i += 1
    _add_key(keys, cur)
    return keys


def _add_key(keys, chunk):
    chunk = chunk.strip()
    if not chunk or chunk.startswith("..."):
        return
    m = re.match(r"^([A-Za-z_$][\w$]*)\s*:", chunk)
    if m:
        keys.append(m.group(1))
        return
    m = re.match(r"^([A-Za-z_$][\w$]*)$", chunk)
    if m and m.group(1) not in ("true", "false", "null", "undefined"):
        keys.append(m.group(1))


def parse_defs(modules):
    """解析出所有 (api, key, kind, url, method, chunk, inline_keys)"""
    defs = []
    for name, mod in modules.items():
        text = mod["text"]
        reducers = [(m.start(), m.group(1)) for m in REDUCER_RE.finditer(text)]
        if not reducers:
            continue
        endpoints = [(m.start(), m.group(1), m.group(2))
                     for m in ENDPOINT_RE.finditer(text)]
        if not endpoints:
            continue
        # 每个端点对象从它自己的位置到下一个端点/文件尾
        for idx, (pos, key, kind) in enumerate(endpoints):
            end = endpoints[idx + 1][0] if idx + 1 < len(endpoints) else len(text)
            window = text[pos:end]
            api = None
            for rpos, rname in reducers:
                if rpos < pos:
                    api = rname
            url_m = URL_RE.search(window)
            if not url_m or not url_m.group(1).startswith("/api/"):
                continue
            method_m = METHOD_RE.search(window)
            method = method_m.group(1).upper() if method_m else "GET"
            inline = []
            for rx in ((INLINE_BODY_RE, INLINE_PARAMS_RE) if method != "GET"
                       else (INLINE_PARAMS_RE,)):
                for bm in rx.finditer(window):
                    end_b = object_span(window, bm.end() - 1)
                    if end_b > 0:
                        inline.extend(top_level_keys(window[bm.end() - 1:end_b + 1]))
            defs.append({"api": api or "", "key": key, "kind": kind, "url": url_m.group(1),
                         "method": method, "chunk": name, "inline": inline, "pos": pos})
    return defs


# ------------------------------------------------------------- 参数对象解析
# 明显不是接口字段的键（RTK / React 框架内部字段），压缩后容易混进来
FRAMEWORK_KEYS = {
    "queryCacheKey", "endpointName", "requestId", "refetchCachedPages", "fixedCacheKey",
    "apiUid", "extractRehydrationInfo", "hasRehydrationInfo", "endpointDefinitions",
    "forceUpdate", "refetch", "unsubscribe", "abort", "reset", "lastPromiseInfo",
    "isLoading", "isError", "isSuccess", "isUninitialized", "originalArgs",
    "startedTimeStamp", "fulfilledTimeStamp", "isFetching", "currentData", "isPending",
    "setOptions", "update", "destroy", "children", "className", "style", "onClick",
    "onChange", "onClose", "onOk", "placeholder", "disabled", "loading",
}


def enclosing_body(text, pos):
    """
    找 pos 所在的最近一层 `{...}`（函数体）范围，用来把「调用点」限定在
    `const [trigger] = useXxx()` 所在的那个组件函数里，避免单字母别名满文件乱撞。
    """
    depth = 0
    i = pos
    while i > 0:
        ch = text[i]
        if ch == "}":
            depth += 1
        elif ch == "{":
            if depth == 0:
                end = object_span(text, i)
                return (i, end) if end > 0 else None
            depth -= 1
        i -= 1
    return None


def trigger_calls(text, hook_alias, scan_body=True):
    """
    找 hook 解构出来的 trigger 及其调用点：
        const [h] = useXxxMutation();  ->  h
        const [h, {isLoading}] = useXxxMutation({...});  ->  h
    返回 [(trigger, scope_start, scope_end)] 与直接调用 [(literal_keys, snippet)]
    """
    triggers, literals = [], []
    for m in re.finditer(r"\[([^\[\]]{1,120})\]\s*=\s*" + re.escape(hook_alias) + r"\(",
                         text):
        parts = [p.strip() for p in m.group(1).split(",")]
        name = parts[0] if parts else ""
        if not re.match(r"^[A-Za-z_$][\w$]*$", name):
            continue
        scope = enclosing_body(text, m.start()) if scan_body else (0, len(text))
        if scope:
            triggers.append((name, scope[0], scope[1]))
    return triggers


def calls_in_scope(text, alias, start, end):
    """在 scope 里找 alias( 的实参，返回 [(kind, keys, snippet)]"""
    out = []
    seg = text[start:end if end else len(text)]
    for m in re.finditer(r"(?<![\w$.])" + re.escape(alias) + r"\(", seg):
        i = m.end() - 1
        j = i + 1
        while j < len(seg) and seg[j] in " \n\t":
            j += 1
        if j >= len(seg) or seg[j] == ")":
            continue
        if seg[j] == "{":
            end_b = object_span(seg, j)
            if end_b > 0:
                out.append(("literal", top_level_keys(seg[j:end_b + 1]),
                            seg[j:end_b + 1]))
        else:
            head = seg[j:j + 60]
            vm = re.match(r"^[A-Za-z_$][\w$]*$", head.split(")")[0].split(",")[0].strip())
            if vm:
                out.append(("identifier", [], vm.group(0)))
    return out


def resolve_identifier(text, var):
    """传变量时，回文件里找最近的 `var={...}` 赋值"""
    best = None
    for m in re.finditer(r"[{,;(]\s*(?:let|const|var)?\s*" + re.escape(var) + r"\s*=\s*\{",
                         text):
        end = object_span(text, m.end() - 1)
        if end < 0:
            continue
        if best is None or m.start() > best[0]:
            best = (m.start(), text[m.end() - 1:end + 1])
    return top_level_keys(best[1]) if best else []


def resolve_identifier(text, var):
    """传变量时，回文件里找最近的 `var={...}` 赋值"""
    best = None
    for m in re.finditer(r"[{,;(]\s*(?:let|const|var)?\s*" + re.escape(var) + r"\s*=\s*\{",
                         text):
        end = object_span(text, m.end() - 1)
        if end < 0:
            continue
        if best is None or m.start() > best[0]:
            best = (m.start(), text[m.end() - 1:end + 1])
    return top_level_keys(best[1]) if best else []


# --------------------------------------------------------------- 主流程
def main():
    ap = argparse.ArgumentParser(description="挖 /p 接口的请求参数字段")
    ap.add_argument("--http", default=HTTP_JSON)
    ap.add_argument("--asset-dir", default=ASSET_DIR)
    ap.add_argument("--show", default=None, help="只显示某个接口（url 片段）")
    ap.add_argument("--dry-run", action="store_true", help="不写回 http_api.json")
    args = ap.parse_args()

    with open(args.http, encoding="utf-8") as f:
        doc = json.load(f)
    records = doc["endpoints"]

    modules = load_modules(args.asset_dir)
    defs = parse_defs(modules)
    print("产物 %d 个，解析出 %d 个端点定义" % (len(modules), len(defs)))

    # url+method -> 定义
    by_url = {}
    for d in defs:
        by_url.setdefault((d["url"], d["method"]), d)

    # 解析 hook 别名链
    resolved = 0
    for d in defs:
        mod = modules[d["chunk"]]
        suffix = "Query" if d["kind"] == "query" else "Mutation"
        hook = "use%s%s%s" % (d["key"][0].upper(), d["key"][1:], suffix)
        m = re.search(re.escape(hook) + r"\s*:\s*([A-Za-z_$][\w$]*)", mod["text"])
        if not m:
            d["users"] = []
            continue
        local = m.group(1)
        exported = mod["exports"].get(local) or local
        users = []
        for name, other in modules.items():
            if exported in other["imports"]:
                users.append((name, other["imports"][exported]))
        d["users"] = users
        if users:
            resolved += 1
    print("能追到调用点的端点：%d / %d" % (resolved, len(defs)))

    filled = matched = 0
    for rec in records:
        d = by_url.get((rec["url"], rec["method"]))
        if not d:
            rec["params_keys"] = []
            rec["param_source"] = "未追到定义"
            continue
        matched += 1
        keys, evidence, sources = list(d["inline"]), [], set()
        if d["inline"]:
            sources.add("inline")
        field = "body_keys" if rec["method"] != "GET" else "params_keys"
        loose_keys, loose_evidence = [], []
        for chunk, alias in d.get("users") or []:
            text = modules[chunk]["text"]
            triggers = trigger_calls(text, alias)
            # 1) 高置信：hook 解构所在作用域内的调用点
            for trigger, start, end in triggers:
                for kind, arg_keys, snippet in calls_in_scope(text, trigger, start, end):
                    if kind == "literal":
                        if arg_keys:
                            keys.extend(arg_keys)
                            evidence.append(snippet.replace("\n", " ")[:200])
                            sources.add("call_site")
                    else:
                        var_keys = resolve_identifier(text, snippet)
                        if var_keys:
                            keys.extend(var_keys)
                            evidence.append("%s = {%s}" % (snippet, ", ".join(var_keys)))
                            sources.add("call_site_var")
            # 2) 低置信：整个 chunk 里「传对象字面量」的调用（可能撞到同名函数，单独列）
            for trigger, _s, _e in triggers:
                for m in re.finditer(r"(?<![\w$.])" + re.escape(trigger) + r"\(\{", text):
                    end_b = object_span(text, m.end() - 1)
                    if end_b > 0:
                        lit = text[m.end() - 1:end_b + 1]
                        lit_keys = [k for k in top_level_keys(lit) if k not in FRAMEWORK_KEYS]
                        if lit_keys:
                            loose_keys.extend(lit_keys)
                            loose_evidence.append(lit.replace("\n", " ")[:180])
                            sources.add("call_site_loose")
        high = list(dict.fromkeys(
            k for k in keys if k and k != "undefined" and k not in FRAMEWORK_KEYS))
        loose = [k for k in dict.fromkeys(loose_keys) if k not in high]
        rec["params_keys"] = high
        rec["params_keys_loose"] = loose[:20]
        rec["param_source"] = "+".join(sorted(sources)) if sources else "未解析（参数由变量传入）"
        rec["param_evidence"] = evidence[:3] or [e for e in loose_evidence[:2]]
        if high or loose:
            filled += 1
        if args.show and args.show in rec["url"]:
            print("\n=== %s %s   [%s]" % (rec["method"], rec["url"], rec["param_source"]))
            print("  字段(高置信):", high)
            if loose:
                print("  字段(宽松，可能是同名函数噪声):", loose[:12])
            for e in rec["param_evidence"][:3]:
                print("  证据:", e.replace("\n", " ")[:190])
            print("  调用点别名:", d.get("users"))

    total = len(records)
    print("\n接口 %d 个：匹配到定义的 %d 个，挖到参数字段的 %d 个" % (total, matched, filled))
    for k, v in Counter(r.get("param_source") for r in records).most_common():
        print("   %-30s %d" % (k, v))
    write_n = sum(1 for r in records if r["method"] != "GET" and r.get("params_keys"))
    print("   其中写接口：%d / %d 挖到了请求体字段"
          % (write_n, sum(1 for r in records if r["method"] != "GET")))

    if not args.dry_run:
        doc["meta"]["param_extracted_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(args.http, "w", encoding="utf-8") as f:
            json.dump(doc, f, ensure_ascii=False, indent=2)
        print("已更新 %s" % os.path.relpath(args.http, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
