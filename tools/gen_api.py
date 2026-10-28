#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把「静态扫描 + 实测抓包」的结果，封装成 API：

    输入：data/reqs.json        前端产物里提取的接口清单（静态）
          data/probe_status.json 实测结果（每个接口真实响应）
    输出：sdk/api/spec.py        接口元数据（SPEC/ALIASES/SAMPLE_KEYS）
          data/api_spec.json    同一份数据的 JSON 版本，给别的工具用
          docs/api/*.md         每个分组的接口文档（含实测样例）

只有 tier=endpoint（来自前端接口映射表）的接口会被封装；
实测不存在（errno=10000002）的会被剔除并记进文档，
免得把 i18n 文案键当成接口。

用法：
    python tools/gen_api.py
    python tools/gen_api.py --reqs data/reqs.json --probe data/probe_status.json
"""

import argparse
import json
import keyword
import os
import re
import sys
import time
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sdk.safety import is_readonly                            # noqa: E402
try:
    from api_doc_meta import PARAM_HINTS                      # noqa: E402
except ImportError:                                           # pragma: no cover
    PARAM_HINTS = {}

# 动态命名空间里已被占用的名字，生成的方法名要避开
RESERVED_METHOD_NAMES = {
    "call", "find", "help", "methods", "groups", "readonly_methods",
    "client", "_client", "_path", "spec",
}
# 人工确认过参数名的接口（来自 docs/modules 与实测），只写有依据的。
# 注意：真正的参数名单一来源是 tools/api_doc_meta.py 的 PARAM_HINTS（那里还带类型与说明），
# 这里的 KNOWN_PARAMS 只是「PARAM_HINTS 里没有、但人工确认过」的补充。
KNOWN_PARAMS = {
    "user.info": "user（可选，默认查自己）",
    "user.checkNewUser": "user",
    "user.checkNewGroup": "group",
    "user.mod": "user, comment, newName, disableUser, allowSSH",
    "user.setAdmin": "user, setAdmin",
    "user.del": "user",
    "user.changePassword": "user, password, newPassword, removeToken",
    "user.groupAddUsers": "group, users",
    "user.groupDelUsers": "group, users",
    "stor.getUserStorage": "quotaInfo, spaceInfo, storInfo",
    "stor.setUserStorage": "set",
    "appcgi.finder.fileSearch": "key, path(list)",
    "appcgi.network.gw.setting": "data",
    "notify.list": "page, pageSize",
    "usrdat.get": "key(推测)",
    "appcgi.backup.task.list": "（实测缺参数，参数名待补）",
}
STATUS_TEXT = {
    "succ": "已实测通过",
    "param_error": "已实测存在（缺参数）",
    "error": "已实测存在（业务错误码）",
    "timeout": "实测超时",
    "other": "实测返回非标准结构",
    "unknown": "实测不存在",
    "unverified": "未实测（写接口）",
}
# 真机实测确认过的一级模块（其余一级名基本是枚举、日期格式串、App id 之类的噪音）。
# 依据：data/probe_status.json 里 succ/param_error/error 的接口一级名，
# 外加 power（关机/重启，属于写接口所以没自动实测，但前端接口表确凿）。
KNOWN_MODULE_PREFIXES = {
    "appcgi", "file", "stor", "user", "util", "usrdat", "notify", "taskState",
    "liveupdate", "power",
}


def snake(name: str) -> str:
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", s)
    s = re.sub(r"[^0-9A-Za-z_]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_").lower()
    if not s:
        s = "op"
    if keyword.iskeyword(s) or s in RESERVED_METHOD_NAMES:
        s += "_"
    return s


def safe_method(group: str, rest: str) -> str:
    """
    生成一个既能用、又能通过属性访问到的方法名。

    坑：像 user.2fa.loginVerify 这种（2 开头）不能以下划线开头——
    动态命名空间会把 `_xxx` 当作内部属性直接 AttributeError，方法就点不出来了。
    所以先用接口名转换，不行再带上分组前缀兜底。
    """
    for candidate_src in (rest, f"{group.replace('.', '_')}_{rest}"):
        m = snake(candidate_src)
        if m and not m[0].isdigit() and not m.startswith("_"):
            return m
    return "op_" + snake(rest)


def group_of(req: str) -> str:
    parts = req.split(".")
    if parts[0] == "appcgi" and len(parts) >= 2:
        return ".".join(parts[:2])
    return parts[0]


def params_text(name):
    """参数列：优先用 PARAM_HINTS（带类型说明的单一来源），否则回落到 KNOWN_PARAMS"""
    hints = PARAM_HINTS.get(name)
    if hints:
        return ", ".join(hints.keys())
    return KNOWN_PARAMS.get(name, "")


def build_spec(reqs_data, probe_data):
    """合并静态清单与实测结论，产出 SPEC"""
    spec, aliases, samples, unknown, events, suspects = {}, {}, {}, [], [], []
    used = set()                      # (group, method) 去重
    for name, info in reqs_data.get("reqs", {}).items():
        tier = info.get("tier")
        if tier == "event":
            events.append(name)
            continue
        probe = probe_data.get("results", {}).get(name, {}) if probe_data else {}
        status = probe.get("status") or "unverified"
        # tier 只认 endpoint；但**实测确认存在**的（succ/缺参数/业务错误）也算数 ——
        # 实测比静态扫描更权威（例：file.size 静态分档是 unverified，实测是 succ）
        probed_exists = status in ("succ", "param_error", "error", "other", "timeout")
        if tier != "endpoint" and not probed_exists:
            continue
        if status == "unknown":
            unknown.append(name)
            continue
        if name.split(".")[0] not in KNOWN_MODULE_PREFIXES:
            # 一级模块不认识的，基本是 App id / 日期格式串 / 枚举，不封装但记录备查
            suspects.append(name)
            continue
        group = group_of(name)
        rest = name[len(group) + 1:] if name.startswith(group + ".") else name
        method = safe_method(group, rest)
        if (group, method) in used:
            method = safe_method(group, f"{group.replace('.', '_')}_{rest}")
        if (group, method) in used:      # 极端情况再兜底
            method = f"{method}_{len([1 for g, m in used if g == group])}"
        used.add((group, method))
        flags = "r" if is_readonly(name) else "w"
        spec[name] = (group, method, status, flags, params_text(name))
        if info.get("aliases"):
            aliases[name] = sorted(info["aliases"])
        if probe.get("resp_keys"):
            samples[name] = sorted(probe["resp_keys"])
    return spec, aliases, samples, sorted(unknown), sorted(events), sorted(suspects)


def write_spec_py(path, spec, aliases, samples, meta):
    lines = [
        "# -*- coding: utf-8 -*-",
        '"""fnOS 接口元数据（自动生成，不要手工编辑）。',
        "",
        "生成命令：python tools/gen_api.py",
        f"生成时间：{meta['generated_at']}",
        f"接口数：{meta['count']}（只读 {meta['readonly']} / 写 {meta['write']}）",
        '"""',
        "",
        "# req -> (分组, 方法名, 实测状态, 标记(r=只读/w=写), 已知参数)",
        "SPEC = {",
    ]
    for req, (group, method, status, flags, params) in sorted(spec.items()):
        lines.append(f'    {req!r}: ({group!r}, {method!r}, {status!r}, {flags!r}, {params!r}),')
    lines += [
        "}",
        "",
        "# req -> 前端接口表里的别名（能反映官方命名意图）",
        "ALIASES = {",
    ]
    for req, al in sorted(aliases.items()):
        lines.append(f"    {req!r}: {al!r},")
    lines += [
        "}",
        "",
        "# req -> 实测响应里的字段名",
        "SAMPLE_KEYS = {",
    ]
    for req, keys in sorted(samples.items()):
        lines.append(f"    {req!r}: {keys!r},")
    lines += [
        "}",
        "",
        "# 动态命名空间里已被占用的方法名，生成时不能冲突",
        f"RESERVED_METHOD_NAMES = {sorted(RESERVED_METHOD_NAMES)!r}",
        "",
        "META = {",
    ]
    for k, v in meta.items():
        lines.append(f"    {k!r}: {v!r},")
    lines += ["}", ""]
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def safe_json(sample, limit=1200):
    try:
        obj = json.loads(sample)
    except Exception:
        return sample[:limit]
    txt = json.dumps(obj, ensure_ascii=False, indent=2)
    return txt if len(txt) <= limit else txt[:limit] + "\n... (截断)"


def write_docs(out_dir, spec, aliases, samples, probe_data, unknown, events, suspects,
               reqs_data, base):
    os.makedirs(out_dir, exist_ok=True)
    groups = defaultdict(list)
    for req, meta in spec.items():
        groups[meta[0]].append(req)
    results = (probe_data or {}).get("results", {})

    written = []
    for group in sorted(groups):
        reqs = sorted(groups[group])
        fname = group.replace(".", "_") + ".md"
        path = os.path.join(out_dir, fname)
        lines = [
            f"# {group}",
            "",
            f"> 自动生成（`python tools/gen_api.py`），共 {len(reqs)} 个接口。",
            f"> 调用示例：`await client.api.{group}.{spec[reqs[0]][1]}(...)`",
            "",
            "| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
        for req in reqs:
            g, method, status, flags, params = spec[req]
            keys = ", ".join(samples.get(req, [])[:6])
            lines.append(f"| `{method}` | `{req}` | {STATUS_TEXT.get(status, status)} | "
                         f"{'✅' if flags == 'r' else '⚠️'} | {params or '-'} | {keys or '-'} |")
        lines += ["", "## 实测样例", ""]
        shown = 0
        for req in reqs:
            rec = results.get(req)
            if not rec or not rec.get("sample"):
                continue
            if req in unknown:
                continue
            shown += 1
            lines += [f"### {req}", "", f"状态：{STATUS_TEXT.get(rec['status'], rec['status'])}"
                      + (f"（errno={rec['errno']}）" if rec.get("errno") else "")
                      + f"，耗时 {rec.get('elapsed_ms')}ms", "",
                      "```json", safe_json(rec["sample"]), "```", ""]
        if not shown:
            lines += ["_本组接口未实测（写接口，不自动调用）。_", ""]
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        written.append((group, fname, len(reqs)))
        print(f"  写入 {path}")

    # 索引
    counts = defaultdict(int)
    for meta in spec.values():
        counts[meta[2]] += 1
    index = [
        "# fnOS 接口封装总览",
        "",
        "> 自动生成，来源：前端产物静态扫描 + 真机只读实测。",
        f"> 生成时间：{time.strftime('%Y-%m-%d %H:%M:%S')}，目标 NAS：`{base}`",
        "",
        f"- 已封装接口：**{len(spec)}** 个（只读 {sum(1 for m in spec.values() if m[3] == 'r')}，"
        f"写 {sum(1 for m in spec.values() if m[3] == 'w')}）",
        f"- 实测状态：" + "，".join(f"{STATUS_TEXT.get(k, k)} {v}" for k, v in sorted(counts.items())),
        f"- 实测被证伪（静态误报，已剔除）：{len(unknown)} 个",
        f"- 一级模块存疑（App id / 日期格式串等，未封装）：{len(suspects)} 个",
        f"- 服务端推送事件名：{len(events)} 个（见 events.md）",
        "",
        "## 📖 交互式单文件文档",
        "",
        "**推荐先看 [interfaces.html](interfaces.html)**：一个文件装下全部接口，带搜索、分组筛选、",
        "状态筛选，以及每个接口的「用途 / 参数 / 返回字段与数据类型」表格和实测原始报文。",
        "（`python tools/gen_html.py` 生成，双击即可用浏览器打开，不依赖网络。）",
        "",
        "下面是按分组拆分的 Markdown 版本，适合在编辑器/仓库里检索。",
        "",
        "## 用法",
        "",
        "```python",
        "from sdk import FnOsClient",
        "",
        "client = FnOsClient()",
        "await client.connect('ws://<nas>:5666/websocket?type=main')",
        "await client.login(user, password)",
        "",
        "# 1. 命名空间调用（推荐，有 docstring 和参数提示）",
        "await client.api.file.ls(path='vol1/1000')",
        "await client.api.stor.list_disk()          # 磁盘列表",
        "await client.api.appcgi.network.net_list() # 网卡信息",
        "",
        "# 2. 通用调用（临时试验新接口）",
        "await client.api.call('file.prop', {'path': '/vol1/1000/a.jpg'})",
        "",
        "# 3. 查找接口",
        "client.api.find('disk')        # 关键字搜索",
        "client.api.groups()            # 全部分组",
        "client.api.readonly_methods()  # 只看只读接口",
        "print(client.api.help('stor.listDisk'))",
        "```",
        "",
        "## 响应结构提醒",
        "",
        "`reqid` 在响应里可能出现得很靠后；`file.*`/`stor.*` 这种平铺结构的",
        "成功响应**没有 `result` 字段**（只有业务字段 + `reqid`），失败才有 `result=fail` + `errno`。",
        "其它模块的外层是 `data` 或 `rsp`，详见 [protocol.md](../protocol.md)。",
        "",
        "## 服务端主动推送",
        "",
        "```python",
        "from sdk.push import extract_notify, event_of",
        "",
        "def on_notify(client, payload):",
        "    for item in extract_notify(payload):",
        "        print(item['title'], item.get('event'), item.get('data'))",
        "",
        "client.add_push_handler('notify', on_notify)          # 只收通知类推送",
        "client.add_push_handler(None, lambda c, p: print(event_of(p), p))  # 全都要",
        "```",
        "",
        "## 分组一览",
        "",
        "| 分组 | 接口数 | 文档 |",
        "| --- | --- | --- |",
    ]
    for group, fname, n in sorted(written, key=lambda x: -x[2]):
        index.append(f"| `{group}` | {n} | [{fname}]({fname}) |")
    index.append("")
    with open(os.path.join(out_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(index))
    print(f"  写入 {os.path.join(out_dir, 'README.md')}")

    if events:
        path = os.path.join(out_dir, "events.md")
        lines = [
            "# 服务端推送事件名（自动生成）",
            "",
            "> 这些名字来自前端常量/枚举，属于服务端主动推送（消息里没有 reqid）",
            "> 或状态枚举，不是请求接口。连接后可通过 `recorder` 抓到真实推送报文。",
            "",
        ]
        lines += [f"- `{e}`" for e in events]
        lines.append("")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"  写入 {path}")

    if unknown or suspects:
        path = os.path.join(out_dir, "excluded.md")
        lines = [
            "# 未封装的名字及原因（自动生成）",
            "",
            "## 实测证伪（服务端返回「接口不存在」）",
            "",
            "> 静态扫描把它们当候选抓出来了，但真机实测 errno=10000002，",
            "> 说明服务端没有这个接口，多为 i18n 文案键。",
            "",
        ]
        lines += [f"- `{u}`" for u in unknown] or ["- （无）"]
        lines += ["", "## 一级模块存疑（疑似 App id / 日期格式串，未实测不封装）", ""]
        lines += [f"- `{s}`" for s in suspects] or ["- （无）"]
        lines.append("")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"  写入 {path}")

    # docs/api 整个目录都是生成物：清掉上一轮生成、这一轮不再需要的文件，
    # 免得接口被剔除后旧文档还留在仓库里误导人
    keep = {fn for _, fn, _ in written} | {"README.md", "events.md", "excluded.md"}
    for fn in sorted(os.listdir(out_dir)):
        if fn.endswith(".md") and fn not in keep:
            os.remove(os.path.join(out_dir, fn))
            print(f"  清理过期文档 {os.path.join(out_dir, fn)}")
    return written


def main():
    parser = argparse.ArgumentParser(description="生成 fnOS API 封装与文档")
    parser.add_argument("--reqs", default="data/reqs.json")
    parser.add_argument("--probe", default="data/probe_status.json")
    parser.add_argument("--spec-py", default="sdk/api/spec.py")
    parser.add_argument("--spec-json", default="data/api_spec.json")
    parser.add_argument("--docs", default="docs/api")
    args = parser.parse_args()

    if not os.path.exists(args.reqs):
        print(f"缺少 {args.reqs}，先跑 python tools/scan_web.py")
        return 2
    with open(args.reqs, "r", encoding="utf-8") as f:
        reqs_data = json.load(f)
    probe_data = None
    if os.path.exists(args.probe):
        with open(args.probe, "r", encoding="utf-8") as f:
            probe_data = json.load(f)
    else:
        print(f"提示：没有 {args.probe}，只生成未实测的封装（先跑 tools/probe.py 更好）")

    spec, aliases, samples, unknown, events, suspects = build_spec(reqs_data, probe_data)
    meta = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "base": reqs_data.get("base"),
        "count": len(spec),
        "readonly": sum(1 for m in spec.values() if m[3] == "r"),
        "write": sum(1 for m in spec.values() if m[3] == "w"),
        "unknown_reqs": unknown,
        "suspect_reqs": suspects,
        "source": {"reqs": args.reqs, "probe": args.probe if probe_data else None},
    }

    print(f"[1/3] 生成 {args.spec_py} ...")
    write_spec_py(args.spec_py, spec, aliases, samples, meta)

    print(f"[2/3] 生成 {args.spec_json} ...")
    d = os.path.dirname(os.path.abspath(args.spec_json))
    if d:
        os.makedirs(d, exist_ok=True)
    with open(args.spec_json, "w", encoding="utf-8") as f:
        json.dump({
            "meta": meta,
            "spec": {k: {"group": v[0], "method": v[1], "status": v[2],
                         "readonly": v[3] == "r", "params": v[4]}
                     for k, v in sorted(spec.items())},
            "aliases": aliases,
            "sample_keys": samples,
            "events": events,
        }, f, ensure_ascii=False, indent=2)

    print(f"[3/3] 生成 {args.docs}/ ...")
    write_docs(args.docs, spec, aliases, samples, probe_data, unknown, events, suspects,
               reqs_data, reqs_data.get("base", ""))

    print(f"\n封装完成：{len(spec)} 个接口"
          f"（只读 {meta['readonly']} / 写 {meta['write']}），"
          f"剔除实测误报 {len(unknown)} 个，模块存疑 {len(suspects)} 个，"
          f"推送事件 {len(events)} 个")
    return 0


if __name__ == "__main__":
    sys.exit(main())
