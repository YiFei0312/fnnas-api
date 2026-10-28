#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
在压缩过的前端产物里查某个接口名的**上下文**——用来反推真实参数名。

打包后的 JS 基本是「一整行」，普通 grep 只能看到一大坨，所以这里按正则找到
每个命中点，打印前后 N 个字符。

用法：
    python tools/js_context.py "file\\.mkdir"
    python tools/js_context.py "file\\.rm" --window 500 --max 5
    python tools/js_context.py "file\\.(cp|mv|rename)" --files data/web-cache/assets
    python tools/js_context.py "file\\.prop" --json          # 只输出 JSON（给脚本用）
"""

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_DIR = os.path.join(ROOT, "data", "web-cache")


def iter_files(paths):
    for path in paths:
        if os.path.isfile(path):
            yield path
            continue
        for base, _dirs, files in os.walk(path):
            for name in files:
                if name.endswith((".js", ".mjs", ".html", ".json")):
                    yield os.path.join(base, name)


def main():
    ap = argparse.ArgumentParser(description="在打包后的 JS 里查接口名的上下文")
    ap.add_argument("pattern", help="正则，如 'file\\.mkdir'")
    ap.add_argument("--files", nargs="*", default=[DEFAULT_DIR],
                    help="文件或目录，默认 data/web-cache")
    ap.add_argument("--window", type=int, default=350, help="命中点前后各留多少字符")
    ap.add_argument("--max", type=int, default=12, help="每个动作最多打印几处")
    ap.add_argument("--json", action="store_true", help="输出 JSON 而不是人看的格式")
    args = ap.parse_args()

    rx = re.compile(args.pattern)
    hits = []
    for path in iter_files(args.files):
        try:
            with open(path, encoding="utf-8", errors="replace") as f:
                text = f.read()
        except OSError:
            continue
        for m in rx.finditer(text):
            start, end = max(0, m.start() - args.window), min(len(text), m.end() + args.window)
            hits.append({
                "file": os.path.relpath(path, ROOT),
                "offset": m.start(),
                "match": m.group(0),
                "context": text[start:end],
            })

    if args.json:
        print(json.dumps(hits, ensure_ascii=False, indent=1))
        return 0

    if not hits:
        print("没有命中：" + args.pattern)
        return 1
    print(f"命中 {len(hits)} 处（{args.pattern}）")
    shown = 0
    for h in hits:
        if shown >= args.max:
            print(f"…… 还有 {len(hits) - shown} 处，用 --max 调整")
            break
        shown += 1
        print(f"\n=== {h['file']} @ {h['offset']}")
        ctx = h["context"].replace("\n", " ")
        print("   " + ctx.replace(h["match"], f"【{h['match']}】"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
