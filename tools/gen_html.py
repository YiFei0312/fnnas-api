#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把抓到的接口整理成一份**单文件 HTML 文档**（含用途、参数、字段类型表格）。

    输入：data/api_spec.json      接口清单（分组/方法名/实测状态/只读标记）
          data/probe_status.json  实测响应样例（用来推导字段和类型）
          data/reqs.json          静态扫描原始数据（别名等）
    输出：docs/api/interfaces.html  双击即可打开，自带搜索与筛选，无外部依赖

用法：
    python tools/gen_html.py
    python tools/gen_html.py --out docs/api/interfaces.html --sample-limit 4000
"""

import argparse
import json
import os
import re
import sys
import time
from collections import Counter
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from api_doc_meta import (MODULE_CN, PURPOSE, VERB_CN, NOUN_CN,   # noqa: E402
                          FIELD_CN, PARAM_HINTS, NESTED_DATA_REQS,
                          NESTED_DATA_SUSPECT, FIELD_TYPE_OVERRIDE)

STATUS_CN = {
    "succ": ("已实测通过", "ok"),
    "param_error": ("接口存在（缺参数）", "warn"),
    "error": ("接口存在（业务返回错误）", "warn"),
    "other": ("返回结构非标准", "warn"),
    "timeout": ("实测超时", "warn"),
    "unknown": ("实测不存在", "bad"),
    "unverified": ("未实测（写接口）", "skip"),
}
STATUS_ORDER = ["succ", "param_error", "error", "other", "timeout", "unverified", "unknown"]

# 响应外壳里的元字段，不算业务数据
META_KEYS = {"reqid", "result", "errno", "errmsg", "req", "rev"}


# ---------------------------------------------------------------- 工具函数
def esc(value):
    return escape(str(value), quote=True)


def jtype(value):
    """把 JSON 值映射成可读类型名"""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array<%s>" % (jtype(value[0]) if value else "any")
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def short(value, limit=70):
    try:
        text = json.dumps(value, ensure_ascii=False)
    except Exception:
        text = repr(value)
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]
    return text if len(text) <= limit else text[:limit] + "…"


def close_brackets(chunk):
    """给被截断的 JSON 补上缺失的 } 和 ]（忽略字符串内的括号）"""
    stack, in_str, esc_next = [], False, False
    for ch in chunk:
        if esc_next:
            esc_next = False
            continue
        if ch == "\\":
            esc_next = True
            continue
        if ch == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if ch in "{[":
            stack.append("}" if ch == "{" else "]")
        elif ch in "}]" and stack:
            stack.pop()
    return chunk + "".join(reversed(stack))


def loads_lenient(text):
    """解析样例报文；被截断时尽量补全，实在不行返回 None"""
    if not text:
        return None
    s = text.strip()
    if s.endswith("..."):
        s = s[:-3].rstrip().rstrip(",")
    try:
        return json.loads(s)
    except Exception:
        pass
    # 从后往前找可以安全截断的位置，补全括号后再试
    cuts = [i for i, ch in enumerate(s) if ch in ",}]"]
    for cut in reversed(cuts[-400:]):
        try:
            return json.loads(close_brackets(s[:cut + 1].rstrip().rstrip(",")))
        except Exception:
            continue
    return None


def field_rows(obj, depth=0, max_depth=2):
    """把一层 JSON 对象展开成字段表：[{name, type, sample, desc, children, extra}]"""
    rows = []
    if not isinstance(obj, dict):
        return [{"name": "(根)", "type": jtype(obj), "sample": short(obj),
                 "desc": "", "children": [], "extra": ""}]
    for key, value in obj.items():
        row = {
            "name": key,
            "type": jtype(value),
            "sample": short(value),
            "desc": FIELD_CN.get(key, ""),
            "children": [],
            "extra": "",
        }
        if isinstance(value, list) and value:
            row["extra"] = f"共 {len(value)} 条"
            if isinstance(value[0], dict) and depth < max_depth:
                row["children"] = field_rows(value[0], depth + 1, max_depth)
            elif value and not isinstance(value[0], (dict, list)):
                kinds = sorted({jtype(v) for v in value[:30]})
                row["type"] = "array<%s>" % "/".join(kinds)
        elif isinstance(value, dict) and depth < max_depth:
            row["children"] = field_rows(value, depth + 1, max_depth)
        rows.append(row)
    return rows


def envelope_of(sample):
    """判断响应外壳：data / rsp / flat / error / empty"""
    if not isinstance(sample, dict):
        return "empty"
    if isinstance(sample.get("data"), dict):
        return "data"
    if isinstance(sample.get("rsp"), dict):
        return "rsp"
    if sample.get("result") == "fail":
        return "error"
    business = [k for k in sample if k not in META_KEYS]
    return "flat" if business else "error"


ENVELOPE_CN = {
    "data": "data",
    "rsp": "rsp",
    "flat": "平铺",
    "error": "错误响应",
    "empty": "无样例",
}


# ---------------------------------------------------------------- 用途推断
def infer_purpose(req, group, method):
    """写接口没有实测，按方法名里的动词+名词推断用途，并在文档里标注「推断」"""
    rest = req[len(group) + 1:] if req.startswith(group + ".") else req
    tokens = [t for t in re.split(r"[._]", re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", rest).lower()) if t]
    if not tokens:
        return "接口（用途未知）"
    # 动词可能在任意位置：nas.find、cert.apply、task.delete 都把动词放后面
    verb, verb_idx = None, -1
    for i, tok in enumerate(tokens):
        if tok in VERB_CN:
            verb, verb_idx = VERB_CN[tok], i
            break
    words, unknown = [], []
    for i, tok in enumerate(tokens):
        if i == verb_idx or tok.isdigit() or tok in ("v1", "v2", "v3", "v4"):
            continue
        name = NOUN_CN.get(tok)
        if name:
            if name not in words:
                words.append(name)
        else:
            unknown.append(tok)
    if verb and words:
        text = f"{verb}{''.join(words)}"
    elif verb and unknown:
        text = f"{verb}（{'、'.join(unknown)}）"
    elif verb:
        text = verb
    elif words:
        text = f"{'、'.join(words)}相关操作"
    else:
        text = f"{req}（{method}）"
    if unknown and words:
        text += f"（{', '.join(unknown)}）"
    return text


def params_of(req, spec_params):
    """参数列表：已知的带上类型和说明，未知的只给名字"""
    hints = PARAM_HINTS.get(req, {})
    names = [n.strip() for n in (spec_params or "").replace("（", "(").split(",") if n.strip()]
    out, seen = [], set()
    for name in names:
        clean = re.sub(r"\(.*?\)", "", name).strip()
        if not clean or clean in seen:
            continue
        seen.add(clean)
        type_name, desc = hints.get(clean, ("未知", "暂未确认（先用 client.api.call 传参试）"))
        out.append({"name": clean, "type": type_name, "desc": desc})
    for key, (type_name, desc) in hints.items():
        if key not in seen:
            out.append({"name": key, "type": type_name, "desc": desc})
    return out


# ---------------------------------------------------------------- 组装数据
def build_records(spec, probe, reqs_data, sample_limit=4000):
    results = (probe or {}).get("results", {})
    aliases = reqs_data.get("aliases", {})
    records = []
    for req, meta in sorted(spec.items()):
        group = meta["group"]
        pr = results.get(req, {})
        status = meta["status"]
        raw_sample = pr.get("sample") or ""
        parsed = loads_lenient(raw_sample)
        envelope = envelope_of(parsed) if parsed is not None else ("error" if raw_sample else "empty")
        purpose = PURPOSE.get(req)
        src = "doc"
        if not purpose:
            purpose = infer_purpose(req, group, meta["method"])
            src = "infer"
        # 业务字段（剥掉外壳和元字段）
        body = parsed
        if isinstance(parsed, dict):
            if envelope == "data":
                body = parsed["data"]
            elif envelope == "rsp":
                body = parsed["rsp"]
            else:
                body = {k: v for k, v in parsed.items() if k not in META_KEYS}
        fields = field_rows(body) if isinstance(body, (dict, list)) else []
        for row in fields:                       # 空样例导致的类型误判，人工纠正
            override = FIELD_TYPE_OVERRIDE.get(req, {}).get(row["name"])
            if override:
                row["type"] = override
        if req in NESTED_DATA_REQS:
            nested_data = "must"
        elif req in NESTED_DATA_SUSPECT:
            nested_data = "suspect"
        else:
            nested_data = ""
        records.append({
            "req": req,
            "group": group,
            "module": MODULE_CN.get(group, (group, ""))[0],
            "method": meta["method"],
            "status": status,
            "status_text": STATUS_CN.get(status, (status, "skip"))[0],
            "status_cls": STATUS_CN.get(status, (status, "skip"))[1],
            "readonly": bool(meta["readonly"]),
            "purpose": purpose,
            "purpose_src": src,
            "params": params_of(req, meta.get("params", "")),
            "envelope": envelope,
            "fields": fields,
            "nested_data": nested_data,
            "resp_keys": sorted(k for k in (pr.get("resp_keys") or []) if k not in META_KEYS),
            "errno": pr.get("errno"),
            "elapsed_ms": pr.get("elapsed_ms"),
            "alias": ", ".join(aliases.get(req, [])),
            "sample": pretty_sample(raw_sample, sample_limit),
            "sample_ok": parsed is not None,
        })
    return records


def pretty_sample(raw, limit=4000):
    if not raw:
        return ""
    parsed = loads_lenient(raw)
    if parsed is None:
        return raw[:limit]
    text = json.dumps(parsed, ensure_ascii=False, indent=2)
    return text if len(text) <= limit else text[:limit] + "\n…（样例已截断）"


# ---------------------------------------------------------------- HTML
def render_fields(fields, level=0):
    if not fields:
        return '<p class="muted">该接口没有业务数据字段（成功时只返回 <code>result</code>/<code>reqid</code>）。</p>'
    rows = []
    for f in fields:
        rows.append(
            "<tr>"
            f'<td class="fname" style="padding-left:{10 + level * 16}px"><code>{esc(f["name"])}</code></td>'
            f'<td class="ftype"><span class="t">{esc(f["type"])}</span></td>'
            f'<td class="fsample"><code>{esc(f["sample"])}</code>'
            + (f' <span class="muted">{esc(f["extra"])}</span>' if f.get("extra") else "")
            + "</td>"
            f'<td class="fdesc">{esc(f["desc"])}</td>'
            "</tr>"
        )
        if f.get("children"):
            # 子字段表必须包在 <td> 里：<table> 不能作为 <tbody> 的直接子节点，
            # 否则浏览器会提前闭合外层表格，后面的 <tr>/<td> 全被当文本丢掉。
            nested = render_fields(f["children"], level + 1).replace(
                '<table class="fields">', '<table class="fields nested">')
            rows.append('<tr class="sub"><td colspan="4">' + nested + "</td></tr>")
    return '<table class="fields"><tbody>' + "".join(rows) + "</tbody></table>"


def render_params(params, nested_data=""):
    wrap = ""
    if nested_data == "must":
        wrap = ('<p class="nested-tip">⚠ 这组参数必须包一层 <code>data</code> 再发：'
                '<code>{"req":"...","data":{参数}}</code>；平铺发会返回 '
                '<code>errno 3000001 Invalid Params</code>。'
                '用 SDK 时：<code>await client.call(req, {...}, nested=True)</code>。</p>')
    elif nested_data == "suspect":
        wrap = ('<p class="nested-tip">⚠ 疑似同样要包一层 <code>data</code>'
                '（平铺与包 data 返回的错误码不同），参数未完全确认。</p>')
    if not params:
        return wrap + '<p class="muted">无参数（或参数名未确认）。</p>'
    rows = "".join(
        f'<tr><td><code>{esc(p["name"])}</code></td><td><span class="t">{esc(p["type"])}</span></td>'
        f'<td>{esc(p["desc"])}</td></tr>' for p in params)
    return wrap + ('<table class="params"><thead><tr><th>参数</th><th>类型</th><th>说明</th></tr></thead>'
                   f"<tbody>{rows}</tbody></table>")


def render_row(rec):
    perm = ('<span class="badge r">只读</span>' if rec["readonly"]
            else '<span class="badge w">写</span>')
    src = ('<span class="badge infer" title="写接口未实测，用途按方法名推断">推断</span>'
           if rec["purpose_src"] == "infer" else "")
    keys = rec["resp_keys"][:6]
    key_text = " · ".join(
        f'{k}: {next((f["type"] for f in rec["fields"] if f["name"] == k), "?")}' for k in keys) \
        if rec["fields"] else ("—" if rec["status"] != "succ" else "无业务字段")
    if len(rec["resp_keys"]) > 6:
        key_text += " …"
    alias = f'<div class="alias">别名：{esc(rec["alias"])}</div>' if rec["alias"] else ""
    if rec["nested_data"] == "must":
        data_badge = ('<span class="badge data" title="参数必须包在 data 里">'
                      'data 封装</span>')
    elif rec["nested_data"] == "suspect":
        data_badge = '<span class="badge data suspect" title="疑似需要 data 封装">data?</span>'
    else:
        data_badge = ""
    py_call = f"await client.api.{rec['group']}.{rec['method']}(...)"
    row_id = f"req-{esc(rec['req']).replace('.', '-')}"
    detail = f"""
    <tr class="detail" hidden>
      <td colspan="6">
        <div class="detail-box">
          <div class="detail-head">
            <div class="detail-title-bar">
              <h4><code>{esc(rec['req'])}</code> 详情</h4>
              <div class="detail-actions">
                <button type="button" class="act-btn copy-btn" data-copy="{esc(rec['req'])}">复制 req</button>
                <button type="button" class="act-btn copy-btn" data-copy="{esc(py_call)}">复制 Python 调用</button>
                <a class="act-btn link-anchor" href="#{row_id}" title="定位到此接口"># 链接</a>
              </div>
            </div>
            <div class="meta">
              <span class="meta-item">状态：<b>{esc(rec['status_text'])}</b>{'（errno=' + esc(rec['errno']) + '）' if rec.get('errno') else ''}</span>
              {'<span class="meta-item">耗时：<b>' + esc(rec['elapsed_ms']) + ' ms</b></span>' if rec.get('elapsed_ms') else ''}
              <span class="meta-item">响应外壳：<span class="t">{esc(ENVELOPE_CN.get(rec['envelope'], rec['envelope']))}</span></span>
              <span class="meta-item">Python 调用：<code>{esc(py_call)}</code></span>
            </div>
          </div>
          <div class="cols">
            <div class="col-card">
              <h5>请求参数</h5>
              {render_params(rec['params'], rec['nested_data'])}
            </div>
            <div class="col-card">
              <h5>返回字段与数据类型</h5>
              {render_fields(rec['fields'])}
            </div>
          </div>
          <div class="sample-wrap">
            <div class="sample-head">
              <h5>实测原始响应</h5>
              {'<button type="button" class="act-btn copy-sample">复制 JSON</button>' if rec['sample'] else ''}
            </div>
            <pre class="sample">{esc(rec['sample']) if rec['sample'] else '（未实测，无样例）'}</pre>
          </div>
        </div>
      </td>
    </tr>"""
    return f"""    <tr class="row" id="{row_id}"
        data-req="{esc(rec['req'].lower())}" data-group="{esc(rec['group'])}"
        data-status="{esc(rec['status'])}" data-readonly="{1 if rec['readonly'] else 0}"
        data-text="{esc((rec['req'] + ' ' + rec['purpose'] + ' ' + rec['method'] + ' ' + rec['alias']).lower())}">
      <td class="c-method"><a class="toggle" href="#{row_id}"><span class="chev">▸</span><code>{esc(rec['method'])}</code></a></td>
      <td class="c-req"><div class="req-line"><code class="copyable" data-copy="{esc(rec['req'])}" title="点击复制接口名">{esc(rec['req'])}</code>{data_badge}</div>{alias}</td>
      <td class="c-purpose">{esc(rec['purpose'])} {src}</td>
      <td class="c-perm">{perm}</td>
      <td class="c-status"><span class="badge {esc(rec['status_cls'])}">{esc(rec['status_text'])}</span></td>
      <td class="c-keys"><span class="types">{esc(key_text)}</span></td>
    </tr>{detail}
"""


def render_group(group, records, module_desc):
    rows = "".join(render_row(r) for r in records)
    counts = Counter(r["status"] for r in records)
    summary_chips = "".join(
        f'<span class="stat-pill {STATUS_CN[s][1]}">{esc(STATUS_CN[s][0])} <b>{counts[s]}</b></span>'
        for s in STATUS_ORDER if counts.get(s)
    )
    return f"""  <section class="group" id="g-{esc(group).replace('.', '-')}">
    <div class="group-head">
      <div class="group-title-wrap">
        <h2>{esc(MODULE_CN.get(group, (group, ''))[0])} <code>{esc(group)}</code>
          <span class="count">{len(records)} 个接口</span></h2>
        <p class="group-desc">{esc(module_desc)}</p>
      </div>
      <div class="group-stats">{summary_chips}</div>
    </div>
    <div class="table-wrap">
      <table class="api">
        <thead><tr>
          <th>方法</th><th>接口 req</th><th>用途</th><th>权限</th><th>实测状态</th><th>返回字段（类型）</th>
        </tr></thead>
        <tbody>
{rows}        </tbody>
      </table>
    </div>
  </section>
"""


CSS = """
:root{
  --bg:#f4f6fb;
  --bg-grad:radial-gradient(1200px 500px at 15% -10%, rgba(37,99,235,.09), transparent 65%),
            radial-gradient(900px 400px at 90% 0%, rgba(14,165,233,.08), transparent 60%);
  --card:#ffffff;
  --card-alt:#f8fafc;
  --line:#e2e8f0;
  --line-soft:#eef2f7;
  --text:#0f172a;
  --text-sec:#334155;
  --muted:#64748b;
  --accent:#2563eb;
  --accent-hover:#1d4ed8;
  --accent-soft:rgba(37,99,235,.1);
  --code:#f1f5f9;
  --code-border:#e2e8f0;
  --code-text:#0f172a;
  --sample-bg:#0f172a;
  --sample-text:#e2e8f0;
  --thead-bg:#f8fafc;
  --row-hover:#f1f6ff;
  --row-open:#eff6ff;
  --detail-bg:#f8fafc;
  --shadow-sm:0 1px 3px rgba(15,23,42,.04), 0 1px 2px rgba(15,23,42,.03);
  --shadow-md:0 4px 16px -2px rgba(15,23,42,.06), 0 2px 6px -1px rgba(15,23,42,.04);
  --shadow-lg:0 12px 32px -4px rgba(15,23,42,.12);
  --ok:#10b981;
  --warn:#f59e0b;
  --bad:#ef4444;
  --skip:#64748b;
  --type-color:#7c3aed;
  --sample-val:#059669;
  --toolbar-bg:rgba(255,255,255,.88);
}
html[data-theme="dark"]{
  --bg:#0b1120;
  --bg-grad:radial-gradient(1200px 500px at 15% -10%, rgba(59,130,246,.15), transparent 65%),
            radial-gradient(900px 400px at 90% 0%, rgba(14,165,233,.12), transparent 60%);
  --card:#111827;
  --card-alt:#1e293b;
  --line:#1f2937;
  --line-soft:#1e293b;
  --text:#f1f5f9;
  --text-sec:#cbd5e1;
  --muted:#94a3b8;
  --accent:#3b82f6;
  --accent-hover:#60a5fa;
  --accent-soft:rgba(59,130,246,.18);
  --code:#1e293b;
  --code-border:#334155;
  --code-text:#e2e8f0;
  --sample-bg:#090d16;
  --sample-text:#e2e8f0;
  --thead-bg:#162032;
  --row-hover:#17253b;
  --row-open:#1e293b;
  --detail-bg:#0f172a;
  --shadow-sm:0 1px 3px rgba(0,0,0,.3);
  --shadow-md:0 4px 20px rgba(0,0,0,.4);
  --shadow-lg:0 12px 32px rgba(0,0,0,.5);
  --type-color:#a78bfa;
  --sample-val:#34d399;
  --toolbar-bg:rgba(17,24,39,.88);
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{
  margin:0;
  font:14px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
  background-color:var(--bg);
  background-image:var(--bg-grad);
  background-attachment:fixed;
  color:var(--text);
  -webkit-font-smoothing:antialiased;
}
::-webkit-scrollbar{width:8px;height:8px}
::-webkit-scrollbar-track{background:transparent}
::-webkit-scrollbar-thumb{background:rgba(148,163,184,.4);border-radius:999px}
::-webkit-scrollbar-thumb:hover{background:rgba(148,163,184,.65)}

code,pre,.t{font-family:"JetBrains Mono",ui-monospace,SFMono-Regular,Consolas,"Liberation Mono",monospace}
code{
  background:var(--code);
  color:var(--code-text);
  border:1px solid var(--code-border);
  padding:1px 6px;
  border-radius:5px;
  font-size:12.5px;
}
a{color:var(--accent);text-decoration:none;transition:color .15s ease,background-color .15s ease}
a:hover{color:var(--accent-hover)}

.wrap{
  display:grid;
  grid-template-columns:256px 1fr;
  gap:22px;
  max-width:1640px;
  margin:0 auto;
  padding:22px 24px 40px;
}

/* 顶部横幅 */
header.top{
  grid-column:1/-1;
  position:relative;
  overflow:hidden;
  background:linear-gradient(135deg,#0f172a 0%,#1e3a8a 55%,#1d4ed8 100%);
  color:#fff;
  border-radius:16px;
  padding:26px 30px;
  box-shadow:0 10px 30px -5px rgba(29,78,216,.28);
  border:1px solid rgba(255,255,255,.12);
}
header.top::before{
  content:"";
  position:absolute;
  top:-120px;right:-80px;
  width:380px;height:380px;
  background:radial-gradient(circle,rgba(56,189,248,.28) 0%,transparent 70%);
  pointer-events:none;
}
.top-bar{display:flex;justify-content:space-between;align-items:flex-start;gap:16px;flex-wrap:wrap;position:relative;z-index:1}
.top-title-group h1{margin:0 0 8px;font-size:26px;font-weight:700;letter-spacing:-.01em;display:flex;align-items:center;gap:10px}
.top-title-group h1 .ver-pill{
  font-size:12px;font-weight:600;padding:2px 10px;border-radius:999px;
  background:rgba(56,189,248,.22);border:1px solid rgba(56,189,248,.4);color:#e0f2fe;
}
header.top p{margin:4px 0;color:rgba(255,255,255,.9);font-size:14px}
header.top p.small{color:rgba(255,255,255,.78);font-size:12.5px;margin-top:6px}
header.top code{background:rgba(255,255,255,.15);border-color:rgba(255,255,255,.22);color:#fff}
.theme-btn{
  background:rgba(255,255,255,.12);
  color:#fff;
  border:1px solid rgba(255,255,255,.24);
  border-radius:10px;
  padding:7px 13px;
  font-size:13px;
  font-weight:500;
  cursor:pointer;
  display:inline-flex;
  align-items:center;
  gap:6px;
  backdrop-filter:blur(8px);
  transition:all .18s ease;
}
.theme-btn:hover{background:rgba(255,255,255,.22);transform:translateY(-1px)}

.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:12px;margin:20px 0 0;position:relative;z-index:1}
.card{
  background:rgba(255,255,255,.1);
  border:1px solid rgba(255,255,255,.18);
  border-radius:12px;
  padding:12px 16px;
  cursor:pointer;
  backdrop-filter:blur(6px);
  transition:all .18s ease;
  user-select:none;
}
.card:hover{background:rgba(255,255,255,.18);transform:translateY(-2px);border-color:rgba(255,255,255,.35)}
.card b{display:block;font-size:24px;font-weight:700;line-height:1.2;margin-bottom:2px;letter-spacing:-.02em}
.card span{font-size:12.5px;color:rgba(255,255,255,.85)}

/* 侧边目录导航 */
nav.toc{
  position:sticky;
  top:20px;
  align-self:start;
  max-height:calc(100vh - 40px);
  overflow-y:auto;
  background:var(--card);
  border:1px solid var(--line);
  border-radius:14px;
  padding:14px 12px;
  box-shadow:var(--shadow-sm);
}
nav.toc h3{
  margin:6px 8px 8px;
  font-size:11.5px;
  font-weight:700;
  color:var(--muted);
  text-transform:uppercase;
  letter-spacing:.06em;
}
nav.toc h3:not(:first-child){margin-top:14px;padding-top:12px;border-top:1px solid var(--line-soft)}
.toc-filter{
  width:calc(100% - 12px);
  margin:0 6px 8px;
  padding:6px 10px;
  font-size:12.5px;
  border:1px solid var(--line);
  border-radius:8px;
  background:var(--card-alt);
  color:var(--text);
  outline:none;
  transition:border-color .15s;
}
.toc-filter:focus{border-color:var(--accent);background:var(--card)}
nav.toc a{
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:6px 10px;
  margin:1px 0;
  border-radius:8px;
  color:var(--text-sec);
  font-size:13px;
  font-weight:500;
  transition:all .15s ease;
}
nav.toc a:hover{background:var(--code);color:var(--accent)}
nav.toc a.active{background:var(--accent-soft);color:var(--accent);font-weight:600}
nav.toc a .n{
  color:var(--muted);
  background:var(--code);
  padding:1px 7px;
  border-radius:999px;
  font-size:11.5px;
  font-weight:500;
  font-family:ui-monospace,Consolas,monospace;
}
nav.toc a.active .n{background:var(--accent);color:#fff}
nav.toc a.top-link{color:var(--text);font-weight:600}

main{min-width:0}

/* 面板与说明卡片 */
section.panel{
  background:var(--card);
  border:1px solid var(--line);
  border-radius:14px;
  padding:20px 24px;
  margin-bottom:20px;
  box-shadow:var(--shadow-sm);
}
section.panel h2{
  margin:0 0 14px;
  font-size:18px;
  font-weight:700;
  display:flex;
  align-items:center;
  gap:8px;
}
section.panel h2::before{
  content:"";
  display:inline-block;
  width:4px;height:18px;
  background:var(--accent);
  border-radius:4px;
}
section.panel h3{font-size:14.5px;font-weight:600;margin:20px 0 10px;color:var(--text)}

/* 顶部工具栏 */
.toolbar{
  position:sticky;
  top:12px;
  z-index:20;
  background:var(--toolbar-bg);
  backdrop-filter:blur(12px);
  -webkit-backdrop-filter:blur(12px);
  border:1px solid var(--line);
  border-radius:14px;
  padding:12px 16px;
  display:flex;
  flex-wrap:wrap;
  gap:10px;
  align-items:center;
  margin-bottom:20px;
  box-shadow:var(--shadow-md);
}
.search-wrap{position:relative;flex:1;min-width:260px;display:flex;align-items:center}
.search-wrap .search-icon{
  position:absolute;left:11px;color:var(--muted);pointer-events:none;font-size:14px;
}
.search-wrap input[type=search]{
  width:100%;
  padding:8px 64px 8px 34px;
  border:1px solid var(--line);
  border-radius:9px;
  background:var(--card);
  color:var(--text);
  font-size:13.5px;
  font-family:inherit;
  outline:none;
  transition:border-color .15s,box-shadow .15s;
}
.search-wrap input[type=search]:focus{
  border-color:var(--accent);
  box-shadow:0 0 0 3px var(--accent-soft);
}
.search-wrap .kbd-hint{
  position:absolute;right:10px;
  font-size:11px;color:var(--muted);
  background:var(--code);border:1px solid var(--line);
  padding:1px 6px;border-radius:5px;pointer-events:none;
  font-family:ui-monospace,Consolas,monospace;
}
.toolbar select{
  padding:8px 12px;
  border:1px solid var(--line);
  border-radius:9px;
  background:var(--card);
  color:var(--text);
  font-size:13px;
  font-family:inherit;
  outline:none;
  cursor:pointer;
  transition:border-color .15s;
}
.toolbar select:focus{border-color:var(--accent)}
.toolbar button{
  padding:8px 13px;
  border:1px solid var(--line);
  background:var(--card);
  color:var(--text-sec);
  border-radius:9px;
  cursor:pointer;
  font-size:13px;
  font-weight:500;
  transition:all .15s ease;
}
.toolbar button:hover{border-color:var(--accent);color:var(--accent);background:var(--accent-soft)}
.toolbar label.ro-toggle{
  display:inline-flex;
  align-items:center;
  gap:6px;
  font-size:13px;
  font-weight:500;
  color:var(--text-sec);
  padding:7px 12px;
  border:1px solid var(--line);
  border-radius:9px;
  background:var(--card);
  cursor:pointer;
  user-select:none;
  transition:all .15s;
}
.toolbar label.ro-toggle:hover{border-color:var(--accent)}
.toolbar label.ro-toggle input{accent-color:var(--accent);margin:0;cursor:pointer}
#count{font-size:13px;font-weight:600;color:var(--muted);margin-left:auto;white-space:nowrap}

/* 接口分组与表格 */
section.group{
  background:var(--card);
  border:1px solid var(--line);
  border-radius:14px;
  padding:18px 20px;
  margin-bottom:20px;
  scroll-margin-top:84px;
  box-shadow:var(--shadow-sm);
}
.group-head{
  display:flex;
  justify-content:space-between;
  align-items:flex-start;
  flex-wrap:wrap;
  gap:12px;
  margin-bottom:14px;
  padding-bottom:12px;
  border-bottom:1px solid var(--line-soft);
}
section.group h2{margin:0 0 4px;font-size:18px;font-weight:700;display:flex;align-items:center;gap:8px;flex-wrap:wrap}
section.group h2 code{font-size:13.5px;font-weight:600;color:var(--accent);background:var(--accent-soft);border-color:transparent}
section.group .count{
  font-size:12px;color:var(--muted);font-weight:500;
  background:var(--code);padding:2px 9px;border-radius:999px;
}
.group-desc{margin:2px 0 0;color:var(--muted);font-size:13px}
.group-stats{display:flex;flex-wrap:wrap;gap:6px;align-items:center}
.stat-pill{
  font-size:11.5px;padding:2px 9px;border-radius:999px;
  background:var(--code);color:var(--text-sec);border:1px solid var(--line);
}
.stat-pill.ok{background:rgba(16,185,129,.1);color:#059669;border-color:rgba(16,185,129,.25)}
.stat-pill.warn{background:rgba(245,158,11,.1);color:#d97706;border-color:rgba(245,158,11,.25)}
.stat-pill.skip{background:var(--code);color:var(--muted)}
html[data-theme="dark"] .stat-pill.ok{color:#34d399}
html[data-theme="dark"] .stat-pill.warn{color:#fbbf24}

.table-wrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px}
table{width:100%;border-collapse:collapse}
table.api{background:var(--card)}
table.api>thead th{
  background:var(--thead-bg);
  text-align:left;
  font-size:12px;
  font-weight:600;
  text-transform:uppercase;
  letter-spacing:.03em;
  color:var(--muted);
  padding:10px 12px;
  border-bottom:1px solid var(--line);
  white-space:nowrap;
}
table.api>tbody>tr.row>td{
  padding:10px 12px;
  border-bottom:1px solid var(--line-soft);
  vertical-align:middle;
  font-size:13px;
  transition:background-color .12s ease;
}
table.api>tbody>tr.row{cursor:pointer}
table.api>tbody>tr.row:hover>td{background:var(--row-hover)}
table.api>tbody>tr.row.is-open>td{background:var(--row-open);border-bottom-color:var(--line)}
table.api>tbody>tr.row:last-child>td{border-bottom:none}

td.c-method{white-space:nowrap}
td.c-method a.toggle{display:inline-flex;align-items:center;gap:6px;font-weight:600}
td.c-method a.toggle code{
  background:transparent;border:none;padding:0;color:var(--accent);font-weight:600;font-size:13px;
}
td.c-method a.toggle:hover code{text-decoration:underline}
.chev{
  display:inline-block;
  font-size:11px;
  color:var(--muted);
  transition:transform .18s ease,color .18s ease;
  width:12px;
}
tr.row.is-open .chev{transform:rotate(90deg);color:var(--accent)}

td.c-req{min-width:220px}
.req-line{display:flex;align-items:center;gap:6px;flex-wrap:wrap}
code.copyable{cursor:copy;transition:all .15s}
code.copyable:hover{border-color:var(--accent);color:var(--accent)}
td.c-purpose{min-width:230px;color:var(--text-sec)}
td.c-perm,td.c-status{white-space:nowrap}
td.c-keys{max-width:340px;color:var(--text-sec)}
.types{font-family:"JetBrains Mono",ui-monospace,Consolas,monospace;font-size:12px;color:var(--muted)}
.alias{font-size:11.5px;color:var(--muted);margin-top:3px}

/* 徽章设计 */
.badge{
  display:inline-flex;
  align-items:center;
  gap:4px;
  padding:2px 9px;
  border-radius:999px;
  font-size:12px;
  font-weight:500;
  white-space:nowrap;
  border:1px solid transparent;
  line-height:1.4;
}
.badge.r{background:rgba(16,185,129,.12);color:#047857;border-color:rgba(16,185,129,.28)}
.badge.w{background:rgba(245,158,11,.12);color:#b45309;border-color:rgba(245,158,11,.3)}
.badge.ok{background:rgba(16,185,129,.12);color:#047857;border-color:rgba(16,185,129,.28)}
.badge.warn{background:rgba(245,158,11,.12);color:#b45309;border-color:rgba(245,158,11,.3)}
.badge.bad{background:rgba(239,68,68,.12);color:#b91c1c;border-color:rgba(239,68,68,.28)}
.badge.skip{background:var(--code);color:var(--muted);border-color:var(--line)}
.badge.infer{background:rgba(99,102,241,.12);color:#4338ca;border-color:rgba(99,102,241,.26);font-size:11px;padding:1px 7px}
.badge.data{background:rgba(13,148,136,.12);color:#0f766e;border-color:rgba(13,148,136,.28);font-size:11px;padding:1px 7px}
.badge.data.suspect{background:var(--code);color:var(--muted);border-color:var(--line)}

html[data-theme="dark"] .badge.r,
html[data-theme="dark"] .badge.ok{background:rgba(16,185,129,.16);color:#34d399;border-color:rgba(16,185,129,.3)}
html[data-theme="dark"] .badge.w,
html[data-theme="dark"] .badge.warn{background:rgba(245,158,11,.16);color:#fbbf24;border-color:rgba(245,158,11,.3)}
html[data-theme="dark"] .badge.bad{background:rgba(239,68,68,.16);color:#f87171;border-color:rgba(239,68,68,.3)}
html[data-theme="dark"] .badge.infer{background:rgba(129,140,248,.16);color:#a5b4fc;border-color:rgba(129,140,248,.3)}
html[data-theme="dark"] .badge.data{background:rgba(20,184,166,.16);color:#2dd4bf;border-color:rgba(20,184,166,.3)}

.nested-tip{
  margin:0 0 10px;
  padding:9px 12px;
  border-radius:8px;
  background:rgba(13,148,136,.08);
  border:1px solid rgba(13,148,136,.25);
  color:var(--text-sec);
  font-size:12.5px;
  line-height:1.65;
}
.muted{color:var(--muted)}
.small{font-size:12.5px}
table.http{font-size:12.5px}
table.http td,table.http th{padding:6px 8px}
table.http td:first-child{font-family:ui-monospace,Consolas,monospace}
.http-name{color:var(--text-sec);font-size:12px}
.http-probe{color:var(--muted);font-size:12px;white-space:nowrap}
.q{display:inline-block;margin-left:2px;padding:0 4px;border-radius:4px;background:var(--code-bg);
 color:var(--muted);font-size:11px}

/* 展开详情面板 */
tr.detail>td{background:var(--detail-bg);padding:0;border-bottom:1px solid var(--line)}
.detail-box{
  padding:18px 20px;
  border-left:3px solid var(--accent);
}
.detail-title-bar{
  display:flex;
  justify-content:space-between;
  align-items:center;
  flex-wrap:wrap;
  gap:10px;
  margin-bottom:8px;
}
.detail-head h4{margin:0;font-size:15px;font-weight:700}
.detail-actions{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.act-btn{
  padding:4px 10px;
  font-size:12px;
  font-weight:500;
  border-radius:6px;
  border:1px solid var(--line);
  background:var(--card);
  color:var(--text-sec);
  cursor:pointer;
  transition:all .15s;
}
.act-btn:hover{border-color:var(--accent);color:var(--accent);background:var(--accent-soft)}
.detail-head .meta{
  display:flex;
  flex-wrap:wrap;
  gap:8px 18px;
  font-size:12.5px;
  color:var(--muted);
  margin-bottom:14px;
  padding:8px 12px;
  background:var(--card);
  border:1px solid var(--line-soft);
  border-radius:8px;
}
.cols{display:grid;grid-template-columns:minmax(260px,1fr) minmax(340px,1.4fr);gap:16px;margin-bottom:14px}
.col-card{
  background:var(--card);
  border:1px solid var(--line-soft);
  border-radius:10px;
  padding:12px 14px;
}
.cols h5,.sample-head h5{
  margin:0 0 8px;
  font-size:12.5px;
  font-weight:700;
  text-transform:uppercase;
  letter-spacing:.04em;
  color:var(--muted);
}
table.params th,table.fields th{
  text-align:left;
  font-size:12px;
  color:var(--muted);
  padding:6px 8px;
  border-bottom:1px solid var(--line);
}
table.params td,table.fields td{
  padding:6px 8px;
  border-bottom:1px solid var(--line-soft);
  font-size:12.5px;
  vertical-align:top;
}
table.params tr:last-child td,table.fields tr:last-child td{border-bottom:none}
table.fields .t,table.params .t,.meta .t{color:var(--type-color);font-size:11.5px;font-weight:600}
table.fields .fsample code{background:transparent;border:none;color:var(--sample-val);padding:0}
table.fields .fdesc,td.fdesc{color:var(--text-sec)}

.sample-wrap{
  background:var(--card);
  border:1px solid var(--line-soft);
  border-radius:10px;
  padding:12px 14px;
}
.sample-head{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}
.sample-head h5{margin:0}
pre.sample{
  background:var(--sample-bg);
  color:var(--sample-text);
  padding:14px 16px;
  border-radius:8px;
  overflow:auto;
  max-height:360px;
  font-size:12.5px;
  line-height:1.55;
  margin:0;
  border:1px solid rgba(255,255,255,.07);
}

.grid2{display:grid;grid-template-columns:1fr 1fr;gap:18px}
table.kv td{padding:8px 10px;border-bottom:1px solid var(--line-soft);font-size:13px;vertical-align:top}
table.kv tr:last-child td{border-bottom:none}
table.kv td:first-child{white-space:nowrap;width:160px;font-weight:500}

.note{
  background:var(--card-alt);
  border:1px solid var(--line);
  border-left:4px solid var(--accent);
  padding:12px 16px;
  border-radius:8px;
  margin:14px 0 0;
  color:var(--text-sec);
}

/* 嵌进单文件的模块文档（docs/modules/*.md 渲染结果） */
.doc-embed{font-size:13.5px;line-height:1.7}
.doc-embed h2{margin:22px 0 10px;padding-bottom:6px;border-bottom:1px solid var(--line-soft);font-size:17px}
.doc-embed h3{margin:20px 0 8px;font-size:15px}
.doc-embed h4{margin:16px 0 6px;font-size:13.5px;color:var(--text-sec)}
.doc-embed p{margin:8px 0;color:var(--text-sec)}
.doc-embed ul,.doc-embed ol{margin:8px 0 8px 20px;color:var(--text-sec)}
.doc-embed li{margin:3px 0}
.doc-embed hr{margin:20px 0;border:none;border-top:1px solid var(--line-soft)}
.doc-embed code{
  font-family:ui-monospace,Consolas,monospace;
  background:var(--code);
  padding:1px 5px;
  border-radius:4px;
  font-size:12px;
  white-space:nowrap;
}
.doc-embed pre.sample{max-height:none;margin:10px 0}
.doc-embed pre.sample code{background:none;padding:0;white-space:pre}
.doc-embed table.kv{margin:10px 0;font-size:12.5px}
.doc-embed table.kv th{
  text-align:left;
  padding:6px 10px;
  background:var(--card-alt);
  border-bottom:1px solid var(--line);
  font-weight:600;
  white-space:nowrap;
}
.doc-embed .note{margin:12px 0}
.doc-embed .note p:first-child{margin-top:0}
.doc-embed .note p:last-child{margin-bottom:0}
.doc-src{margin:0 0 6px}
.warnbox{
  background:rgba(245,158,11,.07);
  border:1px solid rgba(245,158,11,.25);
  border-left:4px solid var(--warn);
  padding:12px 16px;
  border-radius:8px;
  margin:14px 0;
  color:var(--text-sec);
}
.empty-state{
  text-align:center;
  padding:48px 20px;
  background:var(--card);
  border:1px dashed var(--line);
  border-radius:14px;
  color:var(--muted);
  margin-bottom:20px;
}
.empty-state b{display:block;font-size:16px;color:var(--text);margin-bottom:6px}

/* 浮动回到顶部与提示框 */
.back-top{
  position:fixed;
  right:26px;
  bottom:26px;
  width:42px;
  height:42px;
  border-radius:50%;
  background:var(--accent);
  color:#fff;
  border:none;
  box-shadow:var(--shadow-lg);
  cursor:pointer;
  font-size:18px;
  display:flex;
  align-items:center;
  justify-content:center;
  opacity:0;
  pointer-events:none;
  transform:translateY(10px);
  transition:all .2s ease;
  z-index:50;
}
.back-top.show{opacity:1;pointer-events:auto;transform:translateY(0)}
.back-top:hover{background:var(--accent-hover);transform:translateY(-2px)}

.toast{
  position:fixed;
  bottom:28px;
  left:50%;
  transform:translateX(-50%) translateY(16px);
  background:#0f172a;
  color:#fff;
  padding:8px 16px;
  border-radius:999px;
  font-size:13px;
  font-weight:500;
  box-shadow:var(--shadow-lg);
  opacity:0;
  pointer-events:none;
  transition:all .2s ease;
  z-index:100;
}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}

footer{grid-column:1/-1;color:var(--muted);font-size:12.5px;padding:12px 4px 20px;text-align:center}

@media (max-width:1120px){
  .wrap{grid-template-columns:1fr;padding:14px}
  nav.toc{position:static;max-height:none}
  .cols,.grid2{grid-template-columns:1fr}
}
@media print{
  body{background:#fff}
  .toolbar,nav.toc,.theme-btn,.back-top,.detail-actions{display:none!important}
  .wrap{display:block;max-width:none}
  section.group,section.panel{break-inside:avoid;border:none;padding:0;box-shadow:none}
  tr.detail{display:table-row!important}
  pre.sample{background:#f5f5f5;color:#111}
}
"""

JS = """
(function(){
  var rows = Array.prototype.slice.call(document.querySelectorAll('tr.row'));
  var groups = Array.prototype.slice.call(document.querySelectorAll('section.group'));
  var q = document.getElementById('q'), g = document.getElementById('g'), st = document.getElementById('st');
  var ro = document.getElementById('ro'), cnt = document.getElementById('count');
  var emptyBox = document.getElementById('emptyState');
  var expanded = new Set();

  function setRowOpen(r, open){
    var d = r.nextElementSibling;
    if(!d || !d.classList.contains('detail')) return;
    if(open){
      expanded.add(r);
      r.classList.add('is-open');
      d.hidden = r.hidden;
    } else {
      expanded.delete(r);
      r.classList.remove('is-open');
      d.hidden = true;
    }
  }

  function toggle(r){
    setRowOpen(r, !expanded.has(r));
  }

  function apply(){
    var text = (q.value||'').trim().toLowerCase();
    var group = g.value, status = st.value, onlyRo = ro.checked, shown = 0;
    rows.forEach(function(r){
      var ok = true;
      if(text && r.dataset.text.indexOf(text) === -1) ok = false;
      if(ok && group && r.dataset.group !== group) ok = false;
      if(ok && status){
        if(status === 'tested') ok = r.dataset.status !== 'unverified';
        else if(status === 'write') ok = r.dataset.readonly === '0';
        else ok = r.dataset.status === status;
      }
      if(ok && onlyRo && r.dataset.readonly !== '1') ok = false;
      r.hidden = !ok;
      var d = r.nextElementSibling;
      if(d && d.classList.contains('detail')){ d.hidden = !ok || !expanded.has(r); }
      if(ok) shown++;
    });
    var visibleGroups = 0;
    groups.forEach(function(s){
      var any = s.querySelectorAll('tr.row:not([hidden])').length > 0;
      s.hidden = !any;
      if(any) visibleGroups++;
    });
    if(emptyBox) emptyBox.hidden = shown > 0;
    cnt.textContent = (text || group || status || onlyRo)
      ? ('显示 ' + shown + ' / ' + rows.length + ' 个接口')
      : ('共 ' + rows.length + ' 个接口（未筛选）');
  }

  rows.forEach(function(r){
    r.addEventListener('click', function(e){
      if(e.target.closest('a:not(.toggle)') || e.target.closest('.copyable') || e.target.closest('button')) return;
      toggle(r);
    });
  });

  document.getElementById('expandAll').addEventListener('click', function(){
    rows.forEach(function(r){ if(!r.hidden) setRowOpen(r, true); });
  });
  document.getElementById('collapseAll').addEventListener('click', function(){
    rows.forEach(function(r){ setRowOpen(r, false); });
  });
  var resetBtn = document.getElementById('resetFilter');
  if(resetBtn){
    resetBtn.addEventListener('click', function(){
      q.value = ''; g.value = ''; st.value = ''; ro.checked = false;
      apply();
    });
  }

  q.addEventListener('input', apply);
  g.addEventListener('change', apply);
  st.addEventListener('change', apply);
  ro.addEventListener('change', apply);

  document.addEventListener('click', function(e){
    var t = e.target.closest('.toggle');
    if(t){
      e.preventDefault();
      toggle(t.closest('tr.row'));
      return;
    }
    var copyEl = e.target.closest('[data-copy]');
    if(copyEl){
      e.stopPropagation();
      copyText(copyEl.getAttribute('data-copy'), '已复制：' + copyEl.getAttribute('data-copy'));
      return;
    }
    var copySample = e.target.closest('.copy-sample');
    if(copySample){
      var pre = copySample.closest('.sample-wrap').querySelector('pre.sample');
      if(pre) copyText(pre.textContent, '已复制 JSON 响应样例');
      return;
    }
    var cardEl = e.target.closest('.card[data-filter]');
    if(cardEl){
      var f = cardEl.getAttribute('data-filter');
      q.value = ''; g.value = ''; st.value = ''; ro.checked = false;
      if(f === 'ro') ro.checked = true;
      else if(f === 'write') st.value = 'write';
      else if(f === 'tested') st.value = 'tested';
      else if(f === 'succ') st.value = 'succ';
      apply();
      var apisEl = document.getElementById('apis');
      if(apisEl) apisEl.scrollIntoView({behavior:'smooth', block:'start'});
    }
  });

  /* 复制与 Toast */
  var toast = document.getElementById('toast');
  var toastTimer = null;
  function showToast(msg){
    if(!toast) return;
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function(){ toast.classList.remove('show'); }, 1800);
  }
  function copyText(str, msg){
    if(navigator.clipboard && navigator.clipboard.writeText){
      navigator.clipboard.writeText(str).then(function(){ showToast(msg || '已复制'); });
    } else {
      var ta = document.createElement('textarea');
      ta.value = str; document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); showToast(msg || '已复制'); } catch(e){}
      document.body.removeChild(ta);
    }
  }

  /* 侧边栏模块过滤与高亮 */
  var tocFilter = document.getElementById('tocFilter');
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll('nav.toc a.mod-link'));
  if(tocFilter){
    tocFilter.addEventListener('input', function(){
      var kw = (tocFilter.value || '').trim().toLowerCase();
      tocLinks.forEach(function(a){
        a.hidden = kw && a.textContent.toLowerCase().indexOf(kw) === -1;
      });
    });
  }

  /* 快捷键 / 聚焦搜索 */
  document.addEventListener('keydown', function(e){
    if(e.key === '/' && document.activeElement !== q && document.activeElement !== tocFilter){
      e.preventDefault();
      q.focus();
      q.select();
    } else if(e.key === 'Escape' && document.activeElement === q){
      q.value = '';
      apply();
      q.blur();
    }
  });

  /* 主题切换 */
  var themeBtn = document.getElementById('themeToggle');
  function applyTheme(dark){
    if(dark){
      document.documentElement.setAttribute('data-theme', 'dark');
      if(themeBtn) themeBtn.textContent = '☀ 浅色模式';
    } else {
      document.documentElement.removeAttribute('data-theme');
      if(themeBtn) themeBtn.textContent = '🌙 深色模式';
    }
  }
  var savedTheme = localStorage.getItem('fnos_doc_theme');
  if(savedTheme === 'dark' || (!savedTheme && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches)){
    applyTheme(true);
  }
  if(themeBtn){
    themeBtn.addEventListener('click', function(){
      var isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      applyTheme(!isDark);
      try { localStorage.setItem('fnos_doc_theme', !isDark ? 'dark' : 'light'); } catch(e){}
    });
  }

  /* 回到顶部与目录滚动高亮 */
  var backTop = document.getElementById('backTop');
  window.addEventListener('scroll', function(){
    if(backTop){
      if(window.scrollY > 400) backTop.classList.add('show');
      else backTop.classList.remove('show');
    }
  }, {passive: true});
  if(backTop){
    backTop.addEventListener('click', function(){
      window.scrollTo({top: 0, behavior: 'smooth'});
    });
  }

  if('IntersectionObserver' in window){
    var map = {};
    tocLinks.forEach(function(a){ map[a.getAttribute('href').slice(1)] = a; });
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(en){
        if(en.isIntersecting && map[en.target.id]){
          tocLinks.forEach(function(a){ a.classList.remove('active'); });
          map[en.target.id].classList.add('active');
        }
      });
    }, {rootMargin: '-10% 0px -80% 0px'});
    groups.forEach(function(s){ io.observe(s); });
  }

  if(location.hash){
    var el = document.querySelector(location.hash);
    if(el && el.classList.contains('row')){
      setRowOpen(el, true);
    }
  }
  apply();
})();
"""


def render_http_panel(http_api):
    """`/p` 相册应用的 HTTP 接口面板（数据来自 tools/scan_http.py）"""
    if not http_api or not http_api.get("endpoints"):
        return "", "", 0
    eps = http_api["endpoints"]
    meta = http_api.get("meta") or {}
    groups = {}
    for e in eps:
        m = re.match(r"^/api/v(\d+)/([^/]+)", e["url"])
        key = ("v%s/%s" % (m.group(1), m.group(2))) if m else "其它"
        groups.setdefault(key, []).append(e)
    get_n = sum(1 for e in eps if e["method"] == "GET")
    rows = []
    for key in sorted(groups):
        rows.append(
            f'<tr class="sub"><td colspan="5"><b>{esc(key)}</b>'
            f'<span class="count"> · {len(groups[key])} 个</span></td></tr>')
        for e in sorted(groups[key], key=lambda x: x["url"]):
            cls = "r" if e["method"] == "GET" else "w"
            probe = e.get("probe") or "-"
            keys = e.get("params_keys") or []
            loose = e.get("params_keys_loose") or []
            if keys:
                fields = ", ".join(keys)
            elif loose:
                fields = ", ".join(loose[:8]) + ' <span class="q">?</span>'
            else:
                fields = ", ".join(e.get("fields") or []) or "-"
            rows.append(
                f'<tr><td><code>{esc(e["url"])}</code></td>'
                f'<td><span class="badge {cls}">{esc(e["method"])}</span></td>'
                f'<td>{fields}</td>'
                f'<td class="http-name">{esc(e.get("name") or "-")}</td>'
                f'<td class="http-probe">{esc(probe)}</td></tr>')
    auth_key = meta.get("auth_key") or "（未解出）"
    panel = f"""
    <section class="panel" id="http">
      <h2>`/p` 相册应用的 HTTP 接口 <span class="count">共 {len(eps)} 个</span></h2>
      <p><code>/p</code> 是飞牛的<b>相册 / AI 相册</b>应用（照片时间线、相册、人物、智能识别、
      地图、回收站、预览、上传…）。它<b>不用 WebSocket</b>，全部走 REST，所以不在上面的
      WebSocket 接口表里。由 <code>python tools/scan_http.py</code> 从
      <code>data/web-cache/p</code> 的产物里提取。</p>
      <div class="warnbox">
        <b>怎么发请求（真机实测跑通）：</b>地址 = <code>{esc(meta.get('base') or '')}/p</code> + 下表路径，
        响应外壳是 <code>{{code, data, msg}}</code>（<code>code == 0</code> 才算成功）。<br>
        鉴权要<b>两样都带</b>，和 WebSocket 那套完全不同：<br>
        ① 请求头 <code>Cookie: fnos-token=&lt;WebSocket 登录返回的 token&gt;</code>；<br>
        ② 请求头 <code>authx: nonce=&lt;6位&gt;&amp;timestamp=&lt;13位毫秒&gt;&amp;sign=&lt;md5&gt;</code>，
        其中 <code>sign = md5(APPKEY_路径_nonce_时间戳_md5(反编码后的参数串)_应用密钥)</code>
        （GET 参数要按 key 排序，POST 算 JSON body；应用密钥在产物里 XOR 混淆，
        <code>scan_http.py:decode_auth_key()</code> 能解出来）。<br>
        只缺 token → HTTP 401；只缺 authx → <code>code 5000 invalid sign</code>。<br>
        现成的客户端：<code>sdk/http_photo.py</code>（<code>PhotoHttpClient</code>），
        相册接口的功能与用法见 <code>docs/modules/album.md</code>。
      </div>
      <p class="muted small">GET {get_n} 个 / 写 {len(eps) - get_n} 个；
      写接口没有发请求（只读原则）。应用密钥：<code>{esc(auth_key)}</code><br>
      「参数/请求体」来自 <code>tools/extract_write_params.py</code>：顺着 hook 别名链找到前端
      实际传参对象，取顶层字段名（带 <span class="q">?</span> 的为宽松匹配，仅供参考）。</p>
      <table class="http">
        <thead><tr><th>路径</th><th>方法</th><th>参数/请求体（挖到的字段）</th><th>前端端点名</th><th>实测</th></tr></thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
    </section>"""
    return panel, f'<a class="top-link" href="#http"><span>HTTP 接口（/p 相册，{len(eps)}）</span></a>', len(eps)


def render_doc_panel(paths):
    """
    把 `docs/modules/*.md` 这类模块文档渲染成 HTML 面板嵌进单文件文档。

    返回 (面板 HTML, 导航 HTML, 面板数)。文件不存在就跳过（不报错）。
    """
    from md_subset import first_heading, render_markdown

    panels, tocs = [], []
    for path in paths or []:
        if not path or not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        title = first_heading(text, os.path.splitext(os.path.basename(path))[0])
        slug = re.sub(r"[^a-z0-9]+", "-", os.path.basename(path).lower()).strip("-")
        rel = os.path.relpath(path).replace("\\", "/")
        body = render_markdown(text)
        panels.append(
            f'<section class="panel" id="doc-{esc(slug)}">\n'
            f'  <p class="muted small doc-src">来源文档 <code>{esc(rel)}</code>'
            f' · 渲染自 Markdown（单文件里链接不可点）</p>\n'
            f'  <div class="doc-embed">\n{body}\n  </div>\n'
            f'</section>')
        tocs.append(f'<a class="top-link" href="#doc-{esc(slug)}"><span>{esc(title)}</span></a>')
    return "\n".join(panels), "".join(tocs), len(panels)


def build_html(records, meta, probe, reqs_data, http_api=None, docs=None):
    groups = {}
    for r in records:
        groups.setdefault(r["group"], []).append(r)
    order = sorted(groups, key=lambda gp: (-len(groups[gp]), gp))

    counts = Counter(r["status"] for r in records)
    readonly = sum(1 for r in records if r["readonly"])
    tested = sum(1 for r in records if r["status"] != "unverified")
    cards = [
        ("接口总数", len(records), "all", "点击显示全部接口"),
        ("只读", readonly, "ro", "点击筛选只读接口"),
        ("写", len(records) - readonly, "write", "点击筛选写接口"),
        ("已实测", tested, "tested", "点击筛选已实测接口"),
        ("分组", len(groups), "all", "共 30 个功能模块"),
        ("实测通过", counts.get("succ", 0), "succ", "点击筛选实测通过接口"),
    ]
    card_html = "".join(
        f'<div class="card" data-filter="{flt}" title="{ tip }"><b>{v}</b><span>{esc(k)}</span></div>'
        for k, v, flt, tip in cards
    )

    toc = "".join(
        f'<a class="mod-link" href="#g-{esc(gp).replace(".", "-")}"><span>{esc(MODULE_CN.get(gp, (gp, ""))[0])}</span>'
        f'<span class="n">{len(groups[gp])}</span></a>' for gp in order)

    options = "".join(f'<option value="{esc(gp)}">{esc(MODULE_CN.get(gp, (gp, ""))[0])} · {esc(gp)} ({len(groups[gp])})</option>'
                      for gp in order)
    status_options = "".join(
        f'<option value="{s}">{esc(STATUS_CN[s][0])}</option>' for s in STATUS_ORDER)

    sections = "".join(render_group(gp, groups[gp], MODULE_CN.get(gp, (gp, ""))[1]) for gp in order)
    http_panel, http_toc, http_count = render_http_panel(http_api)
    doc_panels, doc_toc, doc_count = render_doc_panel(docs)
    http_note = (f" + <b>{http_count}</b> 个 HTTP 接口（<code>/p</code> 相册应用）"
                 if http_count else "")

    events = reqs_data.get("events") or []
    unknown = (probe or {}).get("results") and [
        k for k, v in probe["results"].items() if v.get("status") == "unknown"]
    suspects = meta.get("suspect_reqs", [])

    type_rows = "".join(
        "<tr><td><span class=\"t\">%s</span></td><td>%s</td></tr>" % (t, d) for t, d in [
            ("string", "字符串"),
            ("integer", "整数；时间戳是 <b>秒级</b> Unix 时间（如 1762805820），容量是 <b>字节</b>"),
            ("number", "浮点数（占用率、速率等）"),
            ("boolean", "布尔值 true / false；部分字段用 0/1 表示（如 file.ls 的 <code>dir=1</code> 表示目录）"),
            ("object", "嵌套对象（文档里会展开子表格）"),
            ("array&lt;object&gt;", "对象数组，文档里展开了数组元素的字段"),
            ("array&lt;string&gt;", "字符串数组"),
            ("null", "空值，字段存在但没有数据"),
        ])

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>飞牛 NAS 接口文档（{len(records)} 个接口）</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
  <header class="top">
    <div class="top-bar">
      <div class="top-title-group">
        <h1>飞牛 fnOS 接口文档 <span class="ver-pill">WebSocket RPC</span></h1>
        <p>由前端产物静态扫描 + 真机只读实测自动生成，共 <b>{len(records)}</b> 个 WebSocket 接口{http_note}，含用途、参数与返回数据类型。</p>
        <p class="small">目标设备：<code>{esc(meta.get('base') or '')}</code>
          &nbsp;·&nbsp; 实测时间：<code>{esc((probe or {}).get('generated_at') or '-')}</code>
          &nbsp;·&nbsp; 文档生成：<code>{esc(time.strftime('%Y-%m-%d %H:%M:%S'))}</code>
          &nbsp;·&nbsp; 实测账号：<code>{esc((probe or {}).get('username') or '-')}</code></p>
      </div>
      <button type="button" class="theme-btn" id="themeToggle" title="切换浅色/深色主题">🌙 深色模式</button>
    </div>
    <div class="cards">{card_html}</div>
  </header>

  <nav class="toc">
    <h3>文档导航</h3>
    <a class="top-link" href="#usage"><span>快速上手</span></a>
    <a class="top-link" href="#types"><span>数据类型约定</span></a>
    <a class="top-link" href="#envelope"><span>响应结构</span></a>
    <a class="top-link" href="#apis"><span>接口总表</span></a>
    {http_toc}
    {doc_toc}
    <a class="top-link" href="#appendix"><span>附录与字段字典</span></a>
    <h3>功能模块 ({len(groups)})</h3>
    <input type="search" id="tocFilter" class="toc-filter" placeholder="筛选模块名称...">
    {toc}
  </nav>

  <main>
    <section class="panel" id="usage">
      <h2>快速上手</h2>
      <div class="sample-wrap">
        <div class="sample-head">
          <h5>Python SDK 调用示例</h5>
          <button type="button" class="act-btn copy-sample">复制代码</button>
        </div>
        <pre class="sample" style="max-height:none">from sdk import FnOsClient

client = FnOsClient(ping_interval=60)
await client.connect('ws://&lt;你的NAS&gt;:5666/websocket?type=main')
await client.login('用户名', '密码')

# 全量接口（本节所有接口都能这样调，方法名见「方法」列）
await client.api.file.ls(path='vol4/1000')            # 列出目录
await client.api.stor.list_disk()                     # 硬盘列表
await client.api.appcgi.sysinfo.get_uptime()          # 开机时长

# 参数不确定时用通用调用
await client.api.call('file.prop', {{'path': 'vol4/1000'}})

# 分享链接（appcgi.sharesvr.* 的参数要包 data，SDK 已封装好）
share = await client.share_link_create('/vol4/1000/tmp/a.jpg', passwd='1234')
print(client.share_url(share['id']))     # http://&lt;NAS&gt;:5666/s/&lt;id&gt;
await client.share_link_remove(share['id'])
# 直接调底层接口时用 nested=True：await client.call(req, params, nested=True)
# 也可以交给自动适配：await client.call_auto(req, params)

# 相册应用（/p，HTTP REST，鉴权是另一套：cookie fnos-token + authx 签名）
from sdk.http_photo import PhotoHttpClient
photo = await PhotoHttpClient.login('http://&lt;你的NAS&gt;:5666', '用户名', '密码')
print(await photo.albums())                      # 相册列表
print(await photo.album_create('旅行照片'))       # → {{'albumId': 8, …}}

# 探索
client.api.find('disk')          # 按关键字找接口
client.api.groups()              # 所有分组
client.api.readonly_methods()    # 只看只读接口（安全）
print(client.api.help('stor.listDisk'))</pre>
      </div>
      <div class="note">
        <b>怎么读下面的表：</b>「用途」是接口做什么；「权限」里 <span class="badge r">只读</span> 表示不会改动数据，
        <span class="badge w">写</span> 表示会改数据（写接口没有真机实测，用途带
        <span class="badge infer">推断</span> 标记）；「实测状态」是本次真机探测结果；
        「返回字段（类型）」是实测响应里的顶层字段及推导出的类型，<b>点击任意行</b>可展开查看参数表、完整字段类型表和原始报文。
        带 <span class="badge data">data 封装</span> 标记的接口，参数要包在 <code>data</code> 里发。
      </div>
    </section>

    <section class="panel" id="types">
      <h2>数据类型约定</h2>
      <table class="kv"><tbody>{type_rows}</tbody></table>
      <div class="warnbox">
        <b>两个容易踩的坑：</b>
        ① <code>file.*</code> / <code>stor.*</code> 这类平铺结构的接口，<b>成功响应里没有 <code>result</code> 字段</b>，
        只有业务字段 + <code>reqid</code>；失败时才出现 <code>"result":"fail"</code> 和 <code>errno</code>。
        ② 同一个连接里不同模块的响应外壳不一样（<code>data</code> / <code>rsp</code> / 平铺），详见下一节。
      </div>
      <h3>实测状态含义</h3>
      <table class="kv"><tbody>
        <tr><td><span class="badge ok">已实测通过</span></td><td>返回成功，可以直接用（字段类型取自本次真机响应）</td></tr>
        <tr><td><span class="badge warn">接口存在（缺参数）</span></td><td>服务端认得这个接口，只是没给参数（errno 8192 / 100000002 / 1001 / 1 / 3000001 / 102550007）</td></tr>
        <tr><td><span class="badge warn">接口存在（业务返回错误）</span></td><td>接口存在但业务上拒绝（如功能未安装、设备不支持），errno 见接口详情</td></tr>
        <tr><td><span class="badge skip">未实测（写接口）</span></td><td>会写数据，为避免影响 NAS <b>没有自动调用</b>，需要自己确认参数后试</td></tr>
      </tbody></table>
    </section>

    <section class="panel" id="envelope">
      <h2>响应结构（4 种外壳）</h2>
      <table class="kv"><tbody>
        <tr><td><code>data</code></td><td><code>{{"result":"succ","data":{{...}},"reqid":"..."}}</code> —
          appcgi.network / sysinfo / resmon / security 等</td></tr>
        <tr><td><code>rsp</code></td><td><code>{{"result":"succ","rsp":{{...}},"reqid":"..."}}</code> —
          appcgi.mountmgr 等</td></tr>
        <tr><td>平铺</td><td><code>{{"files":[...],"uver":123,"reqid":"..."}}</code> —
          file.* / stor.*（成功时无 result）</td></tr>
        <tr><td>错误响应</td><td><code>{{"result":"fail","errno":8192,"reqid":"..."}}</code>，
          部分模块另外带 <code>errmsg</code></td></tr>
      </tbody></table>
      <p class="muted small">Python SDK 里 <code>sdk/api/curated.py:unwrap()</code> 会自动剥掉
      <code>data</code>/<code>rsp</code>，<code>check()</code> 在 <code>result == "fail"</code> 时抛
      <code>BadRequestError</code>。</p>

      <h3>请求结构（参数放哪里，实测有讲究）</h3>
      <table class="kv"><tbody>
        <tr><td>平铺参数</td><td><code>{{"req":"file.ls","reqid":"...","path":"vol1/1000"}}</code> —
          <code>file.*</code> / <code>stor.*</code> / <code>user.*</code> 等都是这种</td></tr>
        <tr><td><code>data</code> 封装</td><td><code>{{"req":"appcgi.sharesvr.share.link.list","reqid":"...","data":{{...}}}}</code> —
          <b>appcgi.sharesvr.* 的带参接口必须这样发</b>，平铺会得到 <code>errno 3000001 Invalid Params</code></td></tr>
      </tbody></table>
      <p class="muted small">怎么判断用哪种：看到 <code>Invalid Params</code> 就换另一种。
      SDK 提供了 <code>await client.call(req, params, nested=True)</code>（强制包 data）和
      <code>await client.call_auto(req, params)</code>（先平铺，报参数非法再自动改包 data 重发，并记住这个接口的写法）。</p>
    </section>

    <div class="toolbar">
      <div class="search-wrap">
        <span class="search-icon">🔍</span>
        <input type="search" id="q" placeholder="搜索接口名 / 用途 / 方法名，例如：磁盘、用户、get">
        <span class="kbd-hint" title="按 / 键快速聚焦搜索">/</span>
      </div>
      <select id="g"><option value="">全部分组</option>{options}</select>
      <select id="st"><option value="">全部状态</option><option value="tested">只看已实测</option>
        <option value="write">只看写接口</option>{status_options}</select>
      <label class="ro-toggle"><input type="checkbox" id="ro">只看只读</label>
      <button type="button" id="expandAll">展开全部</button>
      <button type="button" id="collapseAll">折叠全部</button>
      <button type="button" id="resetFilter" title="清空所有筛选条件">重置</button>
      <span id="count">共 {len(records)} 个接口（未筛选）</span>
    </div>

    <div id="emptyState" class="empty-state" hidden>
      <b>未找到匹配的接口</b>
      <span>请尝试更换搜索关键词或点击「重置」清空筛选条件</span>
    </div>

    <div id="apis">
{sections}    </div>

{http_panel}

{doc_panels}

    <section class="panel" id="appendix">
      <h2>附录</h2>
      <div class="grid2">
        <div>
          <h3>服务端主动推送的事件名（{len(events)}）</h3>
          <p class="muted small">这些名字来自前端常量，属于服务端推送/事件枚举，不是请求接口。
            用 <code>client.add_push_handler(...)</code> 接收。</p>
          <p>{''.join('<code>' + esc(e) + '</code> ' for e in events[:60])}
            {f'<span class="muted">… 共 {len(events)} 个</span>' if len(events) > 60 else ''}</p>
        </div>
        <div>
          <h3>静态扫描到但未封装的候选（{len(unknown or []) + len(suspects)}）</h3>
          <p class="muted small"><b>实测不存在</b>（服务端 errno=10000002，多为 i18n 文案键）：</p>
          <p>{''.join('<code>' + esc(u) + '</code> ' for u in (unknown or [])) or '（无）'}</p>
          <p class="muted small"><b>一级模块存疑</b>（疑似 App id / 日期格式串，未实测）：</p>
          <p>{''.join('<code>' + esc(s) + '</code> ' for s in suspects) or '（无）'}</p>
        </div>
      </div>
      <h3>字段中文说明（通用字段）</h3>
      <table class="kv"><tbody>
      {''.join(f'<tr><td><code>{esc(k)}</code></td><td>{esc(v)}</td></tr>' for k, v in sorted(FIELD_CN.items()))}
      </tbody></table>
    </section>
  </main>

  <footer>
    飞牛 fnOS 接口文档 · 自动生成于 {esc(time.strftime('%Y-%m-%d %H:%M:%S'))} ·
    生成脚本 <code>tools/gen_html.py</code> · 抓包流程见 <code>docs/capture.md</code>
  </footer>
</div>
<button type="button" class="back-top" id="backTop" title="回到顶部">↑</button>
<div class="toast" id="toast"></div>
<script>{JS}</script>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="生成单文件 HTML 接口文档")
    parser.add_argument("--spec", default="data/api_spec.json")
    parser.add_argument("--probe", default="data/probe_status.json")
    parser.add_argument("--reqs", default="data/reqs.json")
    parser.add_argument("--http", default="data/http_api.json",
                        help="HTTP 接口清单（tools/scan_http.py 产出；没有就不渲染该节）")
    parser.add_argument("--out", default="docs/api/interfaces.html")
    parser.add_argument("--doc", action="append", default=None,
                        help="把模块文档（Markdown）渲染进 HTML，可重复；"
                             "默认 docs/modules/album.md")
    parser.add_argument("--sample-limit", type=int, default=4000,
                        help="详情里原始报文的最大字符数")
    args = parser.parse_args()

    with open(args.spec, encoding="utf-8") as f:
        spec_doc = json.load(f)
    probe = None
    if os.path.exists(args.probe):
        with open(args.probe, encoding="utf-8") as f:
            probe = json.load(f)
    reqs_data = {}
    if os.path.exists(args.reqs):
        with open(args.reqs, encoding="utf-8") as f:
            reqs_data = json.load(f)
    http_api = None
    if os.path.exists(args.http):
        with open(args.http, encoding="utf-8") as f:
            http_api = json.load(f)

    records = build_records(spec_doc["spec"], probe, reqs_data, args.sample_limit)
    docs = args.doc or [os.path.join("docs", "modules", "album.md")]
    html = build_html(records, spec_doc.get("meta", {}), probe, reqs_data, http_api,
                      docs=docs)

    out_dir = os.path.dirname(os.path.abspath(args.out))
    os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html)
    size = os.path.getsize(args.out) / 1024
    print(f"写入 {args.out}（{len(records)} 个接口"
          f"{f' + {sum(1 for d in docs if d and os.path.exists(d))} 篇模块文档' if docs else ''}"
          f"，{size:.0f} KB）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
