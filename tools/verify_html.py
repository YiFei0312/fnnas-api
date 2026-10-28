#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
校验 `docs/api/interfaces.html` 是否真的完整、能被浏览器正确解析。

为什么需要它：表格是手工拼字符串生成的，一旦 <table> 里出现不合法的子节点，
浏览器会**提前闭合外层表格**，后面的 <tr>/<td> 会被当成纯文本丢掉——
页面看着正常，但少了一大半接口，Python 的宽松 HTML 解析器查不出来。
所以这里用真实浏览器（Edge/Chrome 的 --dump-dom）再解析一遍，逐个比对接口 id。

用法：
    python tools/verify_html.py            # 找不到浏览器时只做静态检查
    python tools/verify_html.py --browser "C:\\path\\to\\msedge.exe"
"""

import argparse
import os
import re
import subprocess
import sys
import tempfile
from html.parser import HTMLParser

VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input",
             "link", "meta", "param", "source", "track", "wbr"}
BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]


class Balance(HTMLParser):
    """宽松的标签配平检查（抓生成器里的笔误，抓不到浏览器的表格规则）"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.errors = [], []

    def handle_starttag(self, tag, attrs):
        if tag not in VOID_TAGS:
            self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag in VOID_TAGS:
            return
        if tag not in self.stack:
            self.errors.append(f"多余闭合 </{tag}>（第 {self.getpos()[0]} 行）")
            return
        while self.stack and self.stack[-1] != tag:
            self.errors.append(f"未闭合 <{self.stack.pop()}>（第 {self.getpos()[0]} 行）")
        self.stack.pop()


def rows_of(html):
    return re.findall(r'<tr class="row" id="req-([^"]+)"', html)


def find_browser(explicit=None):
    for path in ([explicit] if explicit else []) + BROWSERS:
        if path and os.path.exists(path):
            return path
    return None


def dump_dom(browser, url):
    with tempfile.TemporaryDirectory() as tmp:
        cmd = [browser, "--headless=new", "--disable-gpu", "--no-sandbox",
               "--virtual-time-budget=15000", "--dump-dom", url]
        try:
            out = subprocess.run(cmd, capture_output=True, timeout=180)
        except Exception as exc:            # noqa: BLE001
            print(f"! 浏览器执行失败：{exc}")
            return None
        dom = out.stdout.decode("utf-8", "replace")
        return dom or None


def main():
    parser = argparse.ArgumentParser(description="校验生成的 HTML 接口文档")
    parser.add_argument("--file", default="docs/api/interfaces.html")
    parser.add_argument("--browser", default=None, help="浏览器可执行文件路径")
    parser.add_argument("--expect", type=int, default=None,
                        help="期望的接口数量（默认从接口行里推断）")
    args = parser.parse_args()

    path = os.path.abspath(args.file)
    if not os.path.exists(path):
        print(f"✗ 文件不存在：{path}（先跑 python tools/gen_html.py）")
        return 1
    html = open(path, encoding="utf-8").read()
    size_kb = len(html.encode("utf-8")) / 1024
    print(f"文件：{path}（{size_kb:.0f} KB）")

    ids = rows_of(html)
    groups = re.findall(r'<section class="group" id="g-([^"]+)"', html)
    details = html.count('<tr class="detail"')
    fails = []

    print(f"接口行：{len(ids)}   详情块：{details}   分组：{len(groups)}")
    if args.expect and len(ids) != args.expect:
        fails.append(f"接口数量 {len(ids)} != 期望 {args.expect}")
    if details != len(ids):
        fails.append(f"接口行({len(ids)}) 与详情块({details}) 数量不一致")
    if len(set(ids)) != len(ids):
        dupes = [i for i in set(ids) if ids.count(i) > 1]
        fails.append(f"接口 id 重复：{dupes[:5]}")
    if 'id="appendix"' not in html:
        fails.append("缺少附录")

    bal = Balance()
    bal.feed(html)
    print("标签配平：" + ("OK" if not bal.errors and not bal.stack
                        else f"✗ {bal.errors[:3]} 未闭合={bal.stack[:3]}"))
    if bal.errors or bal.stack:
        fails.append("标签配平失败")

    # 关键：嵌套 <table> 必须包在 <td> 里，否则浏览器会吞掉后面的行
    nested_bad = re.findall(r'<tbody>\s*<table', html)
    if nested_bad:
        fails.append(f"有 {len(nested_bad)} 处 <table> 直接放在 <tbody> 里")

    browser = find_browser(args.browser)
    if not browser:
        print("· 未找到 Edge/Chrome，跳过浏览器解析校验")
    else:
        print(f"用浏览器解析：{browser}")
        dom = dump_dom(browser, "file:///" + path.replace("\\", "/"))
        if dom is None:
            print("· --dump-dom 没有输出，跳过")
        else:
            dom_ids = rows_of(dom)
            missing = [i for i in ids if i not in set(dom_ids)]
            print(f"浏览器解析出的接口行：{len(dom_ids)} / {len(ids)}")
            if len(dom_ids) != len(ids) or missing:
                fails.append(f"浏览器丢掉了 {len(ids) - len(dom_ids)} 行"
                             f"（例如 {missing[:3]}）")
            elif dom_ids != ids:
                fails.append("浏览器解析出的顺序与文件不一致")

    if fails:
        print("\n✗ 校验失败：")
        for f in fails:
            print("  - " + f)
        return 1
    print("\n✓ 校验通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
