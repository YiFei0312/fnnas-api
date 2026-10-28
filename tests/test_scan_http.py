# -*- coding: utf-8 -*-
"""
离线用例：`/p`（相册应用）HTTP 接口提取器。

对应工具 `tools/scan_http.py`。它把前端 RTK Query 的定义
（`{url, method, params, body}`）解析成接口清单，供
`docs/api/http.md` 和 `docs/api/interfaces.html` 的 HTTP 一节使用。
"""

import json
import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import scan_http                                                         # noqa: E402


SAMPLE = """
var s = something;
var A = r({reducerPath:`albumApi`,baseQuery:s,tagTypes:[`AlbumList`],endpoints:e=>({
  getList: e.query({query: e=>({url:`/api/v1/album/list`,params:{offset:e.offset,limit:1e3}}),providesTags:[`AlbumList`]}),
  create:  e.mutation({query: e=>({url:`/api/v1/album/create`,method:`post`,body:e})}),
})});
var B = r({reducerPath:`aiPersonApi`,baseQuery:s,endpoints:e=>({
  getPersons: e.query({query:e=>({url:`/api/v1/ai-person/list`,params:e})}),
  mergePeople: e.mutation({query:e=>({url:`/api/v1/ai-person/mergePeople`,body:e,method:`POST`})}),
})});
fetch("/api/v1/not-rtk/whatever");
"""

# 产物里的 XOR 混淆密钥（和真实产物同样的写法）
KEY_NUMS = [50, 54, 50, 52, 52, 49, 69, 66, 90, 79, 71, 54, 65, 90, 67, 65, 65, 65, 90,
            54, 64, 52, 69, 90, 54, 64, 65, 78, 71, 67, 54, 64, 67, 54, 53, 65]
KEY_JS = """
var _s=(()=>{let e=new Uint8Array([%s]),t=new Uint8Array(36);
for(let n=0;n<36;n++)t[n]=e[n]^119;return new TextDecoder(`utf-8`).decode(t)})(),
ws=e=>c(e,_s);
""" % ",".join(str(x) for x in KEY_NUMS)


class TestExtract(unittest.TestCase):
    def test_extract_rtk_endpoints(self):
        items = scan_http.extract_file(SAMPLE, "sample.js")
        by_url = {i["url"]: i for i in items}
        # 只认 /api/ 开头的 RTK 定义，普通 fetch("/api/...") 不算
        self.assertEqual(set(by_url), {
            "/api/v1/album/list", "/api/v1/album/create",
            "/api/v1/ai-person/list", "/api/v1/ai-person/mergePeople"})
        self.assertEqual(by_url["/api/v1/album/list"]["method"], "GET")
        self.assertEqual(by_url["/api/v1/album/list"]["name"], "getList")
        self.assertEqual(by_url["/api/v1/album/list"]["kind"], "query")
        self.assertIn("params", by_url["/api/v1/album/list"]["fields"])
        self.assertEqual(by_url["/api/v1/album/create"]["method"], "POST")
        self.assertEqual(by_url["/api/v1/album/create"]["kind"], "mutation")
        self.assertIn("body", by_url["/api/v1/album/create"]["fields"])
        self.assertEqual(by_url["/api/v1/album/create"]["api"], "albumApi")
        self.assertEqual(by_url["/api/v1/ai-person/mergePeople"]["method"], "POST")

    def test_dedup_keeps_one_per_url_method(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = os.path.join(tmp, "a.js")
            with open(p, "w", encoding="utf-8") as f:
                f.write(SAMPLE)
            found = scan_http.collect([p])
        self.assertEqual(len(found), 4)

    def test_group_and_purpose(self):
        self.assertEqual(scan_http.group_of("/api/v1/album/list"), "v1/album")
        self.assertEqual(scan_http.group_of("/api/v2/photo/upload/path"), "v2/photo")
        self.assertEqual(scan_http.purpose_of("/api/v1/album/list"), "相册列表（分页/排序）")
        self.assertIn("人物", scan_http.purpose_of("/api/v1/ai-person/list"))
        self.assertEqual(scan_http.group_of("/api/v1/album/detail"), "v1/album")
        self.assertIn("相册", scan_http.purpose_of("/api/v1/album/detail"))


class TestAuthKeyDecode(unittest.TestCase):
    def test_decode_xor_key(self):
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "x.js"), "w", encoding="utf-8") as f:
                f.write(KEY_JS)
            key, name = scan_http.decode_auth_key(tmp)
        self.assertIsNotNone(key, "应该能解出 XOR 混淆的密钥")
        self.assertEqual(len(key), 36)
        self.assertEqual(key.count("-"), 4)          # 是个 UUID 形态
        self.assertEqual(name, "x.js")


class TestWriteOutputs(unittest.TestCase):
    def test_writes_json_and_md(self):
        items = {i["url"]: i for i in scan_http.extract_file(SAMPLE, "s.js")}
        records = sorted(items.values(), key=lambda x: x["url"])
        records[0]["probe"] = "HTTP 401（路由存在，需要浏览器会话 cookie）"
        meta = {"source": "test", "base": "http://127.0.0.1:5666",
                "auth_header": "authx", "auth_key": "KEY-123"}
        with tempfile.TemporaryDirectory() as tmp:
            jp, mp = os.path.join(tmp, "h.json"), os.path.join(tmp, "h.md")
            scan_http.write_json(jp, records, meta)
            scan_http.write_md(mp, records, meta)
            data = json.load(open(jp, encoding="utf-8"))
            md = open(mp, encoding="utf-8").read()
        self.assertEqual(len(data["endpoints"]), 4)
        self.assertEqual(data["meta"]["auth_key"], "KEY-123")
        self.assertIn("authx", md)
        self.assertIn("/api/v1/album/list", md)
        self.assertIn("## v1/album", md)
        self.assertIn("401", md)


class TestAuthxSignature(unittest.TestCase):
    """authx 签名（实测跑通的算法，见 tools/scan_http.py:make_authx）"""

    def test_sign_format(self):
        import re
        value = scan_http.make_authx("GET", "/p/api/v1/album/list",
                                     params={"offset": 0, "limit": 10})
        self.assertRegex(value, r"^nonce=\d{6}&timestamp=\d{13}&sign=[0-9a-f]{32}$")

    def test_get_params_change_sign(self):
        """GET 参数参与签名（且与顺序无关，因为签名前会按 key 排序）；固定 nonce/时间戳比对"""
        def sign(**kw):
            return scan_http.make_authx(nonce=123456, stamp=1700000000000, **kw)

        a = sign(method="GET", url="/p/x", params={"limit": 10, "offset": 0})
        b = sign(method="GET", url="/p/x", params={"offset": 0, "limit": 10})
        c = sign(method="GET", url="/p/x", params={"limit": 20, "offset": 0})
        self.assertEqual(a.split("sign=")[1], b.split("sign=")[1])
        self.assertNotEqual(a.split("sign=")[1], c.split("sign=")[1])

    def test_post_body_participates(self):
        def sign(body):
            return scan_http.make_authx("POST", "/p/api/v1/album/create", body=body,
                                        nonce=123456, stamp=1700000000000)
        a, b = sign({"album_name": "x"}), sign({"album_name": "y"})
        self.assertNotEqual(a.split("sign=")[1], b.split("sign=")[1])

    def test_path_participates(self):
        def sign(url):
            return scan_http.make_authx("GET", url, nonce=123456, stamp=1700000000000)
        a, b = sign("/p/api/v1/album/list"), sign("/p/api/v1/gallery/timeline")
        self.assertNotEqual(a.split("sign=")[1], b.split("sign=")[1])

    def test_decode_auth_key_matches_live_value(self):
        """产物里解出来的应用密钥应该是个 UUID 形态；有缓存产物时校验一下"""
        key, name = scan_http.decode_auth_key()
        if not key:
            self.skipTest("没有缓存产物")
        self.assertEqual(len(key), 36)
        self.assertEqual(key.count("-"), 4)


class TestRecordProbe(unittest.TestCase):
    def test_records_success_and_learns_params(self):
        rec = {"url": "/api/v1/album/list", "method": "GET"}
        scan_http.record_probe(rec, {"http": 200, "payload": {
            "code": 0, "data": {"list": []}}}, sent_params={"offset": 0, "limit": 10})
        self.assertEqual(rec["probe"], "HTTP 200 / code 0")
        self.assertEqual(rec["probe_code"], 0)
        self.assertEqual(sorted(rec["params_keys"]), ["limit", "offset"])
        self.assertEqual(rec["probe_params"], {"offset": 0, "limit": 10})

    def test_failure_does_not_learn_params(self):
        rec = {"url": "/api/v1/gallery/getList", "method": "GET"}
        scan_http.record_probe(rec, {"http": 200, "payload": {
            "code": 400, "msg": "invalid params", "data": None}},
            sent_params={"offset": 0, "limit": 10})
        self.assertIn("400", rec["probe"])
        self.assertIn("invalid params", rec["probe"])
        self.assertNotIn("params_keys", rec)

    def test_error_without_payload(self):
        rec = {"url": "/api/v1/x", "method": "POST"}
        scan_http.record_probe(rec, {"http": 401, "payload": None})
        self.assertEqual(rec["probe"], "HTTP 401")


class TestGeneratedHtmlHasHttpSection(unittest.TestCase):
    def test_html_includes_http_panel(self):
        path = os.path.join(ROOT, "docs", "api", "interfaces.html")
        if not os.path.exists(path):
            self.skipTest("还没有生成 HTML 文档")
        html = open(path, encoding="utf-8", errors="replace").read()
        self.assertIn('id="http"', html)
        self.assertIn("/api/v1/", html)
        self.assertIn("authx", html)

    def test_html_includes_album_doc(self):
        """相册模块文档要嵌进单文件 HTML（docs/modules/album.md → #doc-album-md）"""
        path = os.path.join(ROOT, "docs", "api", "interfaces.html")
        if not os.path.exists(path):
            self.skipTest("还没有生成 HTML 文档")
        html = open(path, encoding="utf-8", errors="replace").read()
        self.assertIn('id="doc-album-md"', html)
        self.assertIn('href="#doc-album-md"', html)
        self.assertIn("PhotoHttpClient", html)
        self.assertIn("数据模型", html)
        self.assertIn("album/update/poster", html)

    def test_render_http_panel_empty(self):
        import gen_html
        panel, toc, count = gen_html.render_http_panel(None)
        self.assertEqual((panel, toc, count), ("", "", 0))

    def test_render_doc_panel_embeds_markdown(self):
        import gen_html
        path = os.path.join(ROOT, "docs", "modules", "album.md")
        if not os.path.exists(path):
            self.skipTest("没有相册文档")
        panel, toc, count = gen_html.render_doc_panel([path])
        self.assertEqual(count, 1)
        self.assertIn('id="doc-album-md"', panel)
        self.assertIn("<table class=\"kv\">", panel)      # 字段表渲染成表格
        self.assertIn("doc-embed", panel)
        self.assertIn('href="#doc-album-md"', toc)

    def test_render_doc_panel_ignores_missing(self):
        import gen_html
        panel, toc, count = gen_html.render_doc_panel(["no/such/file.md"])
        self.assertEqual((panel, toc, count), ("", "", 0))

    def test_param_text_prefers_extracted_keys(self):
        # 挖到字段名就显示字段；只有宽松匹配时加 ? 标记；都没有就回落到定义里的标记
        self.assertEqual(scan_http.param_text({"params_keys": ["ids", "album_id"]}),
                         "ids, album_id")
        self.assertEqual(scan_http.param_text({"params_keys": [], "params_keys_loose": ["a", "b"]}),
                         "a, b ?")
        self.assertEqual(scan_http.param_text({"fields": ["body"]}), "body")
        self.assertEqual(scan_http.param_text({}), "-")


class TestWriteParamExtraction(unittest.TestCase):
    """extract_write_params：从 hook 别名链挖请求体字段"""

    def setUp(self):
        sys.path.insert(0, os.path.join(ROOT, "tools"))
        import extract_write_params
        self.E = extract_write_params

    def test_object_span_and_keys(self):
        text = 'x({a:1,b:{c:2},d:"e,f",g})'
        start = text.index("{")
        end = self.E.object_span(text, start)
        self.assertEqual(text[end], "}")
        keys = self.E.top_level_keys(text[start:end + 1])
        self.assertEqual(keys, ["a", "b", "d", "g"])       # 嵌套和字符串里的逗号不干扰

    def test_framework_keys_filtered(self):
        self.assertIn("queryCacheKey", self.E.FRAMEWORK_KEYS)
        self.assertNotIn("ids", self.E.FRAMEWORK_KEYS)     # 真实字段不能被过滤

    def test_split_spec(self):
        self.assertEqual(self.E.split_spec("o as i, a as o, n"), [("o", "i"), ("a", "o"),
                                                                  ("n", "n")])

    def test_end_to_end_alias_chain(self):
        """定义 chunk 导出 hook 别名 → 使用 chunk 导入 → 解构出 trigger → 调用点带对象字面量"""
        with tempfile.TemporaryDirectory() as tmp:
            with open(os.path.join(tmp, "Def.js"), "w", encoding="utf-8") as f:
                f.write('var n={reducerPath:`albumApi`,baseQuery:s,endpoints:e=>({'
                        'createAlbum:e.mutation({query:e=>({url:`/api/v1/album/create`,'
                        'method:`post`,body:e})})})},'
                        '{useCreateAlbumMutation:Ue}=n;export{Ue as i};')
            with open(os.path.join(tmp, "Use.js"), "w", encoding="utf-8") as f:
                f.write('import{i as q}from"./Def.js";'
                        'function C(){let[w]=q();return w({album_name:e,ids:t})}')
            modules = self.E.load_modules(tmp)
            defs = self.E.parse_defs(modules)
            self.assertEqual(len(defs), 1)
            self.assertEqual(defs[0]["url"], "/api/v1/album/create")
            self.assertEqual(defs[0]["method"], "POST")
            # hook 别名链：Ue -> 导出 i -> 导入 q；解构出 w
            mod = modules["Def.js"]
            self.assertEqual(mod["exports"].get("Ue"), "i")
            self.assertEqual(modules["Use.js"]["imports"].get("i"), "q")
            triggers = self.E.trigger_calls(modules["Use.js"]["text"], "q")
            self.assertEqual([t[0] for t in triggers], ["w"])
            name, start, end = triggers[0]
            calls = self.E.calls_in_scope(modules["Use.js"]["text"], name, start, end)
            self.assertEqual(calls[0][1], ["album_name", "ids"])

    def test_scope_limits_false_positives(self):
        """同名短别名在别处被调用时，作用域外的调用不能算进来"""
        text = ("function A(){let[h]=hook();return h({real_field:1})}"
                "function B(){return h({other_field:2})}")
        triggers = self.E.trigger_calls(text, "hook")
        name, start, end = triggers[0]
        calls = self.E.calls_in_scope(text, name, start, end)
        keys = [k for _kind, ks, _s in calls for k in ks]
        self.assertIn("real_field", keys)
        self.assertNotIn("other_field", keys)


if __name__ == "__main__":
    unittest.main(verbosity=2)
