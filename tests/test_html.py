# -*- coding: utf-8 -*-
"""
离线测试 HTML 接口文档生成器（`tools/gen_html.py`）。

重点是防回归那条真的踩过的坑：
嵌套的字段表必须包在 <td> 里 —— `<table>` 一旦直接出现在 `<tbody>` 下，
浏览器会提前闭合外层表格，后面的 <tr>/<td> 会被当纯文本丢掉，
页面看着正常但少一大半接口（Python 的宽松 HTML 解析查不出来）。

    在仓库根目录运行：
        python -m unittest discover -s tests -v
"""

import json
import os
import re
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import gen_html as G                                                  # noqa: E402
from api_doc_meta import PURPOSE                                      # noqa: E402


def make_inputs():
    """一份最小的 spec + probe，覆盖：数组对象、嵌套对象、截断样例、无样例、写接口

    spec 的结构与 data/api_spec.json 里的 spec 字段一致（值是 dict）。
    """
    def item(group, method, status, readonly, params=""):
        return {"group": group, "method": method, "status": status,
                "readonly": readonly, "params": params}

    spec = {
        "file.ls": item("file", "ls", "succ", True, "path"),
        "stor.listDisk": item("stor", "list_disk", "succ", True),
        "user.del": item("user", "del", "unverified", False, "user"),
        "appcgi.backup.task.delete": item("appcgi.backup", "task_delete", "unverified", False),
        "appcgi.network.net.list": item("appcgi.network", "net_list", "succ", True),
    }
    results = {
        "file.ls": {
            "status": "succ",
            "sample": json.dumps({
                "files": [{"name": "a.jpg", "dir": 1, "size": 100, "mtim": 1762805820,
                           "ext": {"icon": "jpg"}}],
                "uver": 117436739026944,
                "reqid": "abc",
            }, ensure_ascii=False),
            "resp_keys": ["files", "uver", "reqid"], "elapsed_ms": 12.3,
        },
        "stor.listDisk": {
            "status": "succ",
            # 故意截断，检查容错
            "sample": '{"disk":[{"id":1,"diskType":"SSD","fssize":512110190592,"partitions":[{"no":1},',
            "resp_keys": ["disk"], "elapsed_ms": 8.0,
        },
        "appcgi.network.net.list": {
            "status": "succ",
            "sample": json.dumps({"data": {"ifs": [{"name": "eth0", "ipv4": "192.168.1.2"}]},
                                  "result": "succ"},
                                 ensure_ascii=False),
            "resp_keys": ["data", "result"], "elapsed_ms": 5.0,
        },
    }
    reqs = {"aliases": {"file.ls": ["file.lsDir"]}, "events": ["diskDegraded", "entryChange"]}
    meta = {"base": "http://nas:5666", "suspect_reqs": ["app.list"]}
    return spec, results, reqs, meta


class TestHelpers(unittest.TestCase):
    def test_loads_lenient_handles_truncated_json(self):
        obj = G.loads_lenient('{"a":1,"b":[{"c":2},{"c":3')
        self.assertIsInstance(obj, dict)
        self.assertEqual(obj["a"], 1)

    def test_loads_lenient_returns_none_on_garbage(self):
        self.assertIsNone(G.loads_lenient("not json at all"))
        self.assertIsNone(G.loads_lenient(""))

    def test_jtype_mapping(self):
        self.assertEqual(G.jtype(True), "boolean")       # bool 必须在 int 之前判断
        self.assertEqual(G.jtype(1), "integer")
        self.assertEqual(G.jtype(1.5), "number")
        self.assertEqual(G.jtype("x"), "string")
        self.assertEqual(G.jtype(None), "null")
        self.assertEqual(G.jtype([1, 2]), "array<integer>")
        self.assertEqual(G.jtype([]), "array<any>")

    def test_field_rows_expands_array_of_objects(self):
        rows = G.field_rows({"files": [{"name": "a", "size": 1}], "uver": 7})
        by_name = {r["name"]: r for r in rows}
        self.assertEqual(by_name["files"]["type"], "array<object>")
        self.assertIn("共 1 条", by_name["files"]["extra"])
        self.assertEqual([c["name"] for c in by_name["files"]["children"]], ["name", "size"])
        self.assertEqual(by_name["uver"]["type"], "integer")

    def test_field_rows_expands_nested_object(self):
        rows = G.field_rows({"cpu": {"core": 24, "busy": 3.5}})
        self.assertEqual(rows[0]["children"][0]["name"], "core")

    def test_envelope_detection(self):
        self.assertEqual(G.envelope_of({"result": "succ", "data": {}}), "data")
        self.assertEqual(G.envelope_of({"result": "succ", "rsp": {}}), "rsp")
        self.assertEqual(G.envelope_of({"files": [], "uver": 1}), "flat")
        self.assertEqual(G.envelope_of({"result": "fail", "errno": 8192}), "error")


class TestPurposeInference(unittest.TestCase):
    def test_documented_req_uses_curated_text(self):
        spec, results, reqs, meta = make_inputs()
        recs = G.build_records(spec, {"results": results}, reqs)
        ls = next(r for r in recs if r["req"] == "file.ls")
        self.assertEqual(ls["purpose"], PURPOSE["file.ls"])
        self.assertEqual(ls["purpose_src"], "doc")

    def test_write_req_gets_inferred_purpose_and_badge(self):
        spec, results, reqs, meta = make_inputs()
        recs = G.build_records(spec, {"results": results}, reqs)
        # 有人工写好的用途：直接用，标 doc
        dele = next(r for r in recs if r["req"] == "user.del")
        self.assertEqual(dele["purpose_src"], "doc")
        # 没人工写过的写接口：按方法名推断，标 infer
        task = next(r for r in recs if r["req"] == "appcgi.backup.task.delete")
        self.assertEqual(task["purpose_src"], "infer")
        self.assertEqual(task["purpose"], "删除任务")
        html = G.build_html(recs, meta, {"results": results}, reqs)
        self.assertIn("推断", html)

    def test_verb_after_noun_is_translated(self):
        # nas.find / cert.apply 这类动词在后面的写法，早期版本翻译不出来
        self.assertTrue(G.infer_purpose("appcgi.backup.nas.find", "appcgi.backup", "find").startswith("查找"))
        self.assertEqual(G.infer_purpose("appcgi.netsvr.cert.apply", "appcgi.netsvr", "cert_apply"),
                         "应用证书")

    def test_every_purpose_is_non_empty(self):
        spec, results, reqs, meta = make_inputs()
        recs = G.build_records(spec, {"results": results}, reqs)
        for r in recs:
            self.assertTrue(r["purpose"].strip(), r["req"])


class TestRender(unittest.TestCase):
    def build(self):
        spec, results, reqs, meta = make_inputs()
        recs = G.build_records(spec, {"results": results}, reqs)
        html = G.build_html(recs, meta, {"results": results, "generated_at": "now",
                                        "username": "u"}, reqs)
        return recs, html

    def test_row_and_detail_counts_match(self):
        recs, html = self.build()
        self.assertEqual(html.count('<tr class="row"'), len(recs))
        self.assertEqual(html.count('<tr class="detail"'), len(recs))

    def test_nested_table_is_wrapped_in_a_cell(self):
        """回归：<table> 不能是 <tbody> 的直接子节点，否则浏览器会吞掉后面的行"""
        recs, html = self.build()
        self.assertNotRegex(html, r"<tbody>\s*<table")
        self.assertIn('<tr class="sub"><td colspan="4"><table class="fields nested">', html)

    def test_fields_table_renders_types_and_examples(self):
        recs, html = self.build()
        self.assertIn("array&lt;object&gt;", html)      # 类型要转义显示
        self.assertIn("共 1 条", html)
        self.assertIn("修改时间（秒级 Unix 时间戳）", html)   # 字段中文说明

    def test_html_is_balanced_and_self_contained(self):
        from html.parser import HTMLParser
        recs, html = self.build()

        class Balance(HTMLParser):
            def __init__(self):
                super().__init__(convert_charrefs=True)
                self.stack, self.errors = [], []
                self.links = []

            def handle_starttag(self, tag, attrs):
                if tag == "link":
                    self.links.append(dict(attrs).get("href"))
                if tag not in {"area", "base", "br", "col", "embed", "hr", "img",
                               "input", "link", "meta", "param", "source", "track", "wbr"}:
                    self.stack.append(tag)

            def handle_endtag(self, tag):
                if tag in {"area", "base", "br", "col", "embed", "hr", "img", "input",
                           "link", "meta", "param", "source", "track", "wbr"}:
                    return
                if not self.stack:
                    self.errors.append(f"多余闭合 </{tag}>")
                    return
                while self.stack and self.stack[-1] != tag:
                    self.errors.append(f"未闭合 <{self.stack.pop()}>")
                if self.stack:
                    self.stack.pop()

        bal = Balance()
        bal.feed(html)
        self.assertFalse(bal.errors, bal.errors[:5])
        self.assertFalse(bal.stack, bal.stack[:5])
        self.assertFalse(bal.links, "文档必须自包含，不能引用外部资源")

    def test_filtering_metadata_present(self):
        recs, html = self.build()
        self.assertIn('id="q"', html)
        self.assertIn('data-readonly="1"', html)
        self.assertIn('data-text="file.ls ', html)
        self.assertIn("共 %d 个接口" % len(recs), html)      # 无 JS 时也有正确计数

    def test_detail_escapes_html_in_samples(self):
        spec = {"file.prop": {"group": "file", "method": "prop", "status": "succ",
                              "readonly": True, "params": "path"}}
        results = {"file.prop": {"status": "succ", "resp_keys": ["name"],
                                 "sample": json.dumps({"name": "<script>alert(1)</script>"})}}
        recs = G.build_records(spec, {"results": results}, {"aliases": {}})
        html = G.build_html(recs, {}, {"results": results}, {"aliases": {}})
        self.assertNotIn("<script>alert(1)</script>", html)
        self.assertIn("&lt;script&gt;", html)


class TestGeneratedFile(unittest.TestCase):
    """真仓库产物存在时，顺手检查一遍（生成物缺失就跳过）"""

    def test_committed_html_matches_spec(self):
        path = os.path.join(ROOT, "docs", "api", "interfaces.html")
        spec_path = os.path.join(ROOT, "data", "api_spec.json")
        if not (os.path.exists(path) and os.path.exists(spec_path)):
            self.skipTest("尚未生成 interfaces.html")
        with open(path, encoding="utf-8") as f:
            html = f.read()
        with open(spec_path, encoding="utf-8") as f:
            spec = json.load(f)["spec"]
        ids = re.findall(r'<tr class="row" id="req-([^"]+)"', html)
        self.assertEqual(len(ids), len(spec), "接口行数与 spec 不一致（重新跑 gen_html.py）")
        self.assertEqual(len(ids), len(set(ids)), "接口 id 有重复")
        self.assertNotRegex(html, r"<tbody>\s*<table")
        for req in spec:
            self.assertIn("req-" + req.replace(".", "-"), html)


if __name__ == "__main__":
    unittest.main(verbosity=2)
