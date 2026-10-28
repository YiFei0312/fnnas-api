#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扫描 fnOS Web 前端产物，静态提取全部 websocket 接口名（req）。

原理：
    飞牛网页把接口名硬编码在前端 JS bundle 里，形如

        {ls:`file.ls`, lsDir:`file.lsDir`, mkdir:`file.mkdir`, ...}

    所以拿到 Web 产物就能穷举服务端支持的接口清单，不需要一个页面一个页面
    手工抓包。脚本会从各个前端入口（/、/p/、/v/、/s/ ...）递归爬取所有
    js 产物，提取三类信息：

      1. direct  直接调用点        req:"file.ls"
      2. alias   接口映射表        ls:`file.ls`      （带可读别名，最有用）
      3. loose   其它模板字符串    `app.started`     （含服务端推送事件名）

用法：
    python tools/scan_web.py                                   # 默认地址
    python tools/scan_web.py --base http://192.168.1.14:5666
    python tools/scan_web.py --entry / --entry /p/ --entry /v/
    python tools/scan_web.py --force                           # 忽略缓存重下

产出：
    data/reqs.json    全部候选接口（来源、别名、出现次数、所属 bundle）
    data/reqs.md      便于阅读的分组清单
    data/web-cache/   前端产物缓存，重复运行不需再下载

只依赖标准库。
"""

import argparse
import json
import os
import re
import sys
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

DEFAULT_BASE = os.environ.get("FNNAS_BASE", "http://192.168.1.10:5666")
DEFAULT_ENTRIES = ["/", "/p/", "/v/", "/s/"]

NAME = r"[A-Za-z0-9_.\-]{2,80}"
# 合法接口名：至少两段，小写开头，如 file.ls / appcgi.network.gw.setting
REQ_NAME_RE = re.compile(r"^[a-z][A-Za-z0-9_]*(?:\.[A-Za-z0-9_]+)+$")

PATTERNS = {
    # 直接调用点：req:"file.ls"  /  "req":"file.ls"  /  req:'file.ls'
    "direct": re.compile(r"""req\s*:\s*["'](""" + NAME + r""")["']"""),
    # 接口映射表：ls:`file.ls`（键名可读，正好当方法名用）
    "alias": re.compile(r"""([A-Za-z0-9_$]{1,40})\s*:\s*`(""" + NAME + r""")`"""),
    # 常量/枚举赋值：e.Started=`app.started`（服务端推送事件名）
    "assign": re.compile(r"""[A-Za-z0-9_$]+\.[A-Za-z0-9_$]+\s*=\s*`(""" + NAME + r""")`"""),
    # 其它模板字符串：`taskbar.power.restarting`（大量是 i18n 文案键，需过滤）
    "loose": re.compile(r"""`(""" + NAME + r""")`"""),
}
# i18n 文案：形如 e(`taskbar.power.restarting`)，用来把文案键挑出来打标记
I18N_CALL_PATTERN = re.compile(r"""[A-Za-z0-9_$]{1,4}\(\s*`(""" + NAME + r""")`""")
# 对象里这些键名装的是 i18n 文案 / 配置项 / 域名，不是接口映射表，
# 例如 {field:`uploadConfig.desc`}、{i18nKey:`photoWall.xxx`}、{address:`pan.baidu.com`}
KEY_DENY = {
    "desc", "description", "field", "fieldclassname", "label", "placeholder", "i18nkey",
    "name", "address", "value", "key", "icon", "title", "type", "id", "path", "mode",
    "children", "text", "content", "message", "tip", "tooltip", "color", "classname",
    "url", "href", "size", "count", "index", "page", "data", "params", "options",
    "config", "version", "code", "errmsg", "result", "reqid", "namespace", "category",
    "state", "status", "props", "ref", "default", "format", "unit", "tag", "to",
    "from", "source", "target", "event", "eventid", "appname", "alias", "displayname",
}
# 域名 / DRM 常量，长得像 req 但不是
TLD_LAST_SEGMENT = {
    "com", "org", "net", "cn", "io", "wiki", "fps", "clearkey", "alpha", "playready",
    "streamingkeydelivery", "w3", "baidu", "aliyun",
}
# 前端产物引用（html/js 里都可能是相对或绝对路径）
ASSET_PATTERN = re.compile(r"""["'\(]([^"'\(\)\s]{0,140}?assets/[A-Za-z0-9_.\-]+\.(?:js|mjs))""")
# 走 http 的接口（上传 / 下载这类）
HTTP_PATH_PATTERN = re.compile(
    r"""["'`](/(?:api|upload|download|multiple-download|websocket)[A-Za-z0-9_\-/.]{0,80})["'`]"""
)
# 明显的噪音（模块系统 / 打包器生成的字段）
REQ_DENY = {"module.exports", "process.env", "this.req", "e.req", "t.req", "n.req"}

# 打分：direct 是真实调用点，alias 是官方接口表，assign 是事件枚举，
# alias_key 是「长得像接口但键名说明只是普通字段」，loose 只是候选
SCORE = {"direct": 6, "alias": 4, "assign": 3, "alias_key": 1, "loose": 1}


def log(msg):
    print(msg, flush=True)


class Fetcher:
    """带磁盘缓存的下载器"""

    def __init__(self, base, cache_dir, timeout=30, retries=2, force=False):
        self.base = base.rstrip("/")
        self.cache_dir = cache_dir
        self.timeout = timeout
        self.retries = retries
        self.force = force
        self.fetched = 0
        self.cached = 0
        self.failed = []
        os.makedirs(cache_dir, exist_ok=True)

    def _cache_path(self, url):
        rel = urlparse(url).path.lstrip("/")
        if not rel or rel.endswith("/"):
            rel += "index.html"
        rel = re.sub(r"[^A-Za-z0-9_.\-/]", "_", rel)
        return os.path.join(self.cache_dir, rel.replace("/", os.sep))

    def get(self, url):
        """返回 (最终 url, bytes)，失败返回 (url, None)"""
        url = urljoin(self.base + "/", url)
        path = self._cache_path(url)
        if os.path.exists(path) and not self.force:
            self.cached += 1
            with open(path, "rb") as f:
                return url, f.read()
        last_err = None
        for attempt in range(self.retries + 1):
            try:
                req = Request(url, headers={"User-Agent": "fnnas-api-scan/1.0"})
                with urlopen(req, timeout=self.timeout) as resp:
                    data = resp.read()
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "wb") as f:
                    f.write(data)
                self.fetched += 1
                return url, data
            except (HTTPError, URLError, OSError) as e:
                last_err = e
                if attempt < self.retries:
                    time.sleep(0.4 * (attempt + 1))
        self.failed.append((url, str(last_err)))
        return url, None

    def get_many(self, urls, workers=8):
        with ThreadPoolExecutor(max_workers=workers) as ex:
            return list(ex.map(self.get, urls))


def app_root(base, url):
    """
    求某个产物所属应用的根路径：
        /assets/index.js        -> http://host:5666/
        /p/assets/index.js      -> http://host:5666/p/
        /p/                     -> http://host:5666/p/
    产物里的相对引用（assets/xxx.js）要相对这个根路径解析，
    直接相对产物本身会解析成 /assets/assets/xxx.js 这种错误地址。
    """
    path = urlparse(url).path
    idx = path.find("/assets/")
    if idx >= 0:
        return urljoin(base + "/", path[:idx + 1])
    if not path.endswith("/"):
        path = path.rsplit("/", 1)[0] + "/"
    return urljoin(base + "/", path)


def crawl(fetcher, entries, max_assets, workers=8):
    """从入口页面出发，递归收集所有 js 产物"""
    contents = {}      # url -> bytes（含 html 与 js）
    seen = set()
    frontier = list(entries)
    while frontier and len(contents) < max_assets:
        batch = [u for u in frontier if u not in seen][:64]
        if not batch:
            break
        seen.update(batch)
        results = fetcher.get_many(batch, workers=workers)
        new_refs = []
        for url, blob in results:
            if blob is None:
                continue
            contents[url] = blob
            text = blob.decode("utf-8", "replace")
            root = app_root(fetcher.base, url)
            for m in ASSET_PATTERN.finditer(text):
                ref = m.group(1)
                full = urljoin(fetcher.base + "/", ref) if ref.startswith("/") else urljoin(root, ref)
                if full not in seen and full not in new_refs:
                    new_refs.append(full)
        log(f"  已抓取 {len(contents)} 个产物，新发现 {len(new_refs)} 个引用")
        frontier = new_refs
    return contents


def extract(contents):
    """从所有产物中提取接口候选，同时收集 http 接口"""
    reqs = {}
    http_paths = set()
    i18n_args = set()
    for url, blob in contents.items():
        if not url.endswith((".js", ".mjs")):
            continue
        text = blob.decode("utf-8", "replace")
        asset = os.path.basename(urlparse(url).path)
        for m in HTTP_PATH_PATTERN.finditer(text):
            http_paths.add(m.group(1))
        for m in I18N_CALL_PATTERN.finditer(text):
            i18n_args.add(m.group(1))
        for source, pat in PATTERNS.items():
            for m in pat.finditer(text):
                alias, name = (m.group(1), m.group(2)) if source == "alias" else (None, m.group(1))
                if name in REQ_DENY or not REQ_NAME_RE.match(name):
                    continue
                if name.split(".")[-1].lower() in TLD_LAST_SEGMENT:
                    continue          # 域名 / DRM 常量
                src = source
                if source == "alias" and alias.lower() in KEY_DENY:
                    # 键名说明这是配置项/文案字段，不算接口表证据
                    src = "alias_key"
                item = reqs.setdefault(name, {
                    "score": 0, "count": 0, "sources": [], "aliases": [], "assets": set(),
                })
                item["score"] += SCORE[src]
                item["count"] += 1
                if src not in item["sources"]:
                    item["sources"].append(src)
                if alias and alias not in item["aliases"]:
                    item["aliases"].append(alias)
                item["assets"].add(asset)
    # 分档：endpoint=接口表/调用点，event=事件枚举，unverified=其它候选（多为 i18n 文案键）
    for name, item in reqs.items():
        if "direct" in item["sources"] or "alias" in item["sources"]:
            item["tier"] = "endpoint"
        elif "assign" in item["sources"]:
            item["tier"] = "event"
        else:
            item["tier"] = "unverified"
        item["i18n_suspect"] = name in i18n_args
    return reqs, http_paths


def group_of(name):
    """分组：appcgi.network.gw.setting -> appcgi.network；file.ls -> file"""
    parts = name.split(".")
    if parts[0] == "appcgi" and len(parts) >= 2:
        return ".".join(parts[:2])
    return parts[0]


def write_outputs(out_json, out_md, base, reqs, http_paths, fetcher, contents, started, entries):
    groups = defaultdict(list)
    for name in sorted(reqs):
        groups[group_of(name)].append(name)
    tiers = defaultdict(int)
    for v in reqs.values():
        tiers[v["tier"]] += 1
    result = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "base": base,
        "entries": entries,
        "elapsed_sec": round(time.time() - started, 1),
        "assets_count": sum(1 for u in contents if u.endswith((".js", ".mjs"))),
        "pages_count": sum(1 for u in contents if not u.endswith((".js", ".mjs"))),
        "reqs_count": len(reqs),
        "tiers": dict(tiers),
        "groups": {g: len(v) for g, v in sorted(groups.items())},
        "reqs": {
            name: {
                "tier": v["tier"],
                "score": v["score"],
                "count": v["count"],
                "sources": sorted(v["sources"]),
                "aliases": sorted(v["aliases"]),
                "i18n_suspect": v["i18n_suspect"],
                "assets": sorted(v["assets"]),
            }
            for name, v in sorted(reqs.items())
        },
        "http_paths": sorted(http_paths),
        "failed_urls": [{"url": u, "error": e} for u, e in fetcher.failed],
    }
    out_dir = os.path.dirname(os.path.abspath(out_json))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    lines = [
        "# fnOS 接口清单（自动生成）",
        "",
        f"> 来源：`{base}` 前端产物静态提取  ",
        f"> 生成时间：{result['generated_at']}，耗时 {result['elapsed_sec']}s  ",
        f"> js 产物 {result['assets_count']} 个 / 入口页 {result['pages_count']} 个，"
        f"共提取 `{len(reqs)}` 个候选名称  ",
        "> **本文件自动生成，不要手工编辑**，重新运行 `python tools/scan_web.py` 即可。",
        "",
        "## 分档说明",
        "",
        "来源标记：`direct`=前端真实调用点，`alias`=接口映射表（键名就是官方别名），",
        "`assign`=事件枚举常量，`alias_key`/`loose`=长得像接口的其它字符串。",
        "",
        "| 分档 | 含义 | 数量 |",
        "| --- | --- | --- |",
        f"| `endpoint` | 来自前端接口映射表或真实调用点，**基本可确认是服务端接口** | {tiers.get('endpoint', 0)} |",
        f"| `event` | 常量/枚举里的推送事件名 | {tiers.get('event', 0)} |",
        f"| `unverified` | 其它同形字符串，多数是 i18n 文案键，需实测确认 | {tiers.get('unverified', 0)} |",
        "",
        "## 分组统计",
        "",
        "| 分组 | 接口数 |",
        "| --- | --- |",
    ]
    for g in sorted(groups, key=lambda x: (-len(groups[x]), x)):
        lines.append(f"| `{g}` | {len(groups[g])} |")
    lines.append("")
    for tier in ("endpoint", "event", "unverified"):
        names = [n for n in sorted(reqs) if reqs[n]["tier"] == tier]
        if not names:
            continue
        lines += [f"# {tier}（{len(names)}）", ""]
        cur_group = None
        for name in names:
            g = group_of(name)
            if g != cur_group:
                cur_group = g
                lines += ["", f"## {g}", "", "| req | 别名 | 来源 | 分数 | i18n? |",
                          "| --- | --- | --- | --- | --- |"]
            v = reqs[name]
            alias = ", ".join(f"`{a}`" for a in v["aliases"][:4]) or "-"
            lines.append(f"| `{name}` | {alias} | {','.join(v['sources'])} | {v['score']} | "
                         f"{'是' if v['i18n_suspect'] else ''} |")
        lines.append("")
    if http_paths:
        lines += ["# HTTP 接口（启发式提取）", ""]
        lines += [f"- `{p}`" for p in sorted(http_paths)]
        lines.append("")
    with open(out_md, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    log(f"  写入 {out_json}")
    log(f"  写入 {out_md}")
    return result


def main():
    parser = argparse.ArgumentParser(description="静态扫描 fnOS 前端，提取全部 websocket 接口名")
    parser.add_argument("--base", default=DEFAULT_BASE, help=f"fnOS 地址，默认 {DEFAULT_BASE}")
    parser.add_argument("--entry", action="append", default=None,
                        help="前端入口路径，可重复指定，默认 / /p/ /v/ /s/")
    parser.add_argument("--cache-dir", default="data/web-cache", help="前端产物缓存目录")
    parser.add_argument("--out", default="data/reqs.json", help="req 清单输出路径")
    parser.add_argument("--md", default="data/reqs.md", help="markdown 清单输出路径")
    parser.add_argument("--max-assets", type=int, default=4000, help="最多抓取多少个产物")
    parser.add_argument("--workers", type=int, default=8, help="并发下载数")
    parser.add_argument("--force", action="store_true", help="忽略缓存重新下载")
    args = parser.parse_args()
    entries = args.entry or DEFAULT_ENTRIES

    started = time.time()
    log(f"[1/3] 从 {args.base} 递归抓取前端产物（入口：{' '.join(entries)}）...")
    fetcher = Fetcher(args.base, args.cache_dir, force=args.force)
    contents = crawl(fetcher, entries, args.max_assets, workers=args.workers)
    js_count = sum(1 for u in contents if u.endswith((".js", ".mjs")))
    log(f"  产物 {len(contents)} 个（js {js_count}），新下载 {fetcher.fetched}，"
        f"命中缓存 {fetcher.cached}，失败 {len(fetcher.failed)}")
    if js_count == 0:
        log("没有抓到任何 js 产物，请确认地址/协议是否正确")
        return 2

    log("[2/3] 提取接口候选 ...")
    reqs, http_paths = extract(contents)
    if not reqs:
        log("没有提取到任何 req，前端产物格式可能变化了")
        return 3

    log("[3/3] 写出清单 ...")
    result = write_outputs(args.out, args.md, args.base, reqs, http_paths, fetcher, contents,
                           started, entries)

    groups = defaultdict(int)
    for name in reqs:
        groups[group_of(name)] += 1
    log("")
    log(f"共 {len(reqs)} 个候选名称，分档：{result['tiers']}")
    log("Top 分组：")
    for g in sorted(groups, key=lambda x: -groups[x])[:20]:
        log(f"  {g:<38} {groups[g]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
