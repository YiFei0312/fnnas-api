#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
极简 Markdown → HTML 渲染器：只支持 `docs/` 里实际用到的那部分语法，
用途是把 `docs/modules/*.md` 这样的模块文档**嵌进单文件 HTML 接口文档**里。

支持：
    # / ## / ### / #### 标题        （整体降一级，因为页面已有 h1）
    ```lang … ``` 围栏代码块          → <pre class="sample">
    | 表格 | … |（含 |---| 分隔行）    → <table class="kv">
    - / 1. 列表                      → <ul>/<ol>
    > 引用                           → <div class="note">
    `行内代码`、**加粗**、[链接](url)  → <code>/<b>/<a>（.md 链接降级成文字，单文件里点不过去）
    ---                              → <hr>

不追求通用：遇到不认识的语法就当普通段落输出，宁可朴素也不能把文档渲染坏。
"""

import html
import re

_FENCE = re.compile(r"^```(\w*)\s*$")
_TABLE_SEP = re.compile(r"^\|[\s:\-|]+\|\s*$")
_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_UL = re.compile(r"^\s*[-*]\s+(.*)$")
_OL = re.compile(r"^\s*\d+\.\s+(.*)$")


def _starts_block(line):
    """这一行是不是「块级语法」的开头（列表续行判断用）"""
    s = line.strip()
    return bool(_FENCE.match(s) or _HEADING.match(line) or s.startswith(("|", ">"))
                or s in ("---", "***") or _UL.match(line) or _OL.match(line))


def _inline(text):
    """行内语法：先转义，再处理代码/加粗/链接（用占位符避免互相干扰）"""
    text = html.escape(text)
    placeholders = []

    def stash(fragment):
        placeholders.append(fragment)
        return "\x00%d\x00" % (len(placeholders) - 1)

    # 行内代码优先（里面的 ** 不该被当加粗）
    text = re.sub(r"`([^`]+)`", lambda m: stash("<code>%s</code>" % m.group(1)), text)

    def link(match):
        label, url = match.group(1), match.group(2)
        if url.startswith(("http://", "https://")):
            return stash('<a href="%s" target="_blank" rel="noopener">%s</a>'
                         % (url, label))
        # 单文件 HTML 里 .md 链接点不过去：降级成等宽文字
        return stash("<code>%s</code>" % label)

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)

    for idx, fragment in enumerate(placeholders):       # 还原占位符
        text = text.replace("\x00%d\x00" % idx, fragment)
    return text


def _table(rows):
    """rows 是原始表格行（含表头），第一行是表头"""
    cells = [[c.strip() for c in row.strip().strip("|").split("|")] for row in rows]
    out = ['<table class="kv"><thead><tr>']
    out += ["<th>%s</th>" % _inline(c) for c in cells[0]]
    out.append("</tr></thead><tbody>")
    for row in cells[1:]:
        out.append("<tr>" + "".join("<td>%s</td>" % _inline(c) for c in row) + "</tr>")
    out.append("</tbody></table>")
    return "".join(out)


def render_markdown(text):
    """把文档渲染成 HTML 片段（不含外层 <section>）"""
    lines = text.replace("\r\n", "\n").split("\n")
    out = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]

        # 空行
        if not line.strip():
            i += 1
            continue

        # 围栏代码块
        m = _FENCE.match(line.strip())
        if m:
            lang = m.group(1)
            i += 1
            code = []
            while i < n and not _FENCE.match(lines[i].strip()):
                code.append(lines[i])
                i += 1
            i += 1
            cls = ' class="sample lang-%s"' % lang if lang else ' class="sample"'
            out.append("<pre%s>%s</pre>" % (cls, html.escape("\n".join(code))))
            continue

        # 标题（降一级：文档 h1 -> 页面 h2）
        m = _HEADING.match(line)
        if m:
            level = min(len(m.group(1)) + 1, 5)
            out.append("<h%d>%s</h%d>" % (level, _inline(m.group(2)), level))
            i += 1
            continue

        # 表格：当前行以 | 开头，且下一行是分隔行
        if line.lstrip().startswith("|") and i + 1 < n and _TABLE_SEP.match(lines[i + 1].strip()):
            rows = [line]
            i += 2
            while i < n and lines[i].lstrip().startswith("|"):
                rows.append(lines[i])
                i += 1
            out.append(_table(rows))
            continue

        # 引用块
        if line.lstrip().startswith(">"):
            quote = []
            while i < n and lines[i].lstrip().startswith(">"):
                quote.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            out.append('<div class="note">%s</div>'
                       % render_markdown("\n".join(quote)))
            continue

        # 分隔线
        if line.strip() in ("---", "***"):
            out.append("<hr>")
            i += 1
            continue

        # 有序 / 无序列表（支持多行列表项：续行不是块级语法开头就并进上一项）
        if _UL.match(line) or _OL.match(line):
            ordered = bool(_OL.match(line))
            items = []
            while i < n:
                m2 = _OL.match(lines[i]) or _UL.match(lines[i])
                if not m2:
                    break
                item = [m2.group(1)]
                i += 1
                while i < n and lines[i].strip() and not _starts_block(lines[i]):
                    item.append(lines[i].strip())
                    i += 1
                items.append("<li>%s</li>" % _inline(" ".join(item)))
            tag = "ol" if ordered else "ul"
            out.append("<%s>%s</%s>" % (tag, "".join(items), tag))
            continue

        # 普通段落：连续行合并
        para = []
        while i < n and lines[i].strip() and not _starts_block(lines[i]):
            para.append(lines[i].strip())
            i += 1
        out.append("<p>%s</p>" % _inline(" ".join(para)))

    return "\n".join(out)


def first_heading(text, default="文档"):
    """取第一个一级标题，用作面板标题"""
    for line in text.splitlines():
        m = _HEADING.match(line.strip())
        if m:
            return re.sub(r"`", "", m.group(2)).strip()
    return default
