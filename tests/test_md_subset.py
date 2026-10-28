# -*- coding: utf-8 -*-
"""
离线用例：`tools/md_subset.py`（把模块文档渲染进单文件 HTML 用的 Markdown 子集渲染器）。
"""

import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import md_subset                                                      # noqa: E402


class TestHeadings(unittest.TestCase):
    def test_levels_shifted_down(self):
        html = md_subset.render_markdown("# 标题\n## 二级\n### 三级")
        self.assertIn("<h2>标题</h2>", html)
        self.assertIn("<h3>二级</h3>", html)
        self.assertIn("<h4>三级</h4>", html)

    def test_first_heading(self):
        self.assertEqual(md_subset.first_heading("# 相册（`/p`）\n## x"), "相册（/p）")
        self.assertEqual(md_subset.first_heading("没有标题", "默认"), "默认")


class TestBlocks(unittest.TestCase):
    def test_fenced_code_escaped(self):
        html = md_subset.render_markdown('```python\nx = "<a>"\n```')
        self.assertIn('<pre class="sample lang-python">', html)
        self.assertIn("&lt;a&gt;", html)
        self.assertNotIn("<a>", html)

    def test_table(self):
        html = md_subset.render_markdown("| 字段 | 说明 |\n|---|---|\n| `albumId` | 相册 ID |")
        self.assertIn('<table class="kv">', html)
        self.assertIn("<th>字段</th>", html)
        self.assertIn("<code>albumId</code>", html)

    def test_list_multiline_item(self):
        html = md_subset.render_markdown("- 第一行\n  第二行继续\n- 另一项")
        self.assertIn("<li>第一行 第二行继续</li>", html)
        self.assertIn("<li>另一项</li>", html)
        self.assertNotIn("<p>第二行", html)

    def test_ordered_list(self):
        html = md_subset.render_markdown("1. 一\n2. 二")
        self.assertIn("<ol><li>一</li><li>二</li></ol>", html)

    def test_blockquote(self):
        html = md_subset.render_markdown("> 注意 `code`")
        self.assertIn('<div class="note">', html)
        self.assertIn("<code>code</code>", html)

    def test_hr(self):
        self.assertIn("<hr>", md_subset.render_markdown("---"))

    def test_paragraph_joins_lines(self):
        html = md_subset.render_markdown("第一行\n第二行")
        self.assertIn("<p>第一行 第二行</p>", html)


class TestInline(unittest.TestCase):
    def test_bold_and_code(self):
        html = md_subset.render_markdown("这是 **重点** 和 `x=1`")
        self.assertIn("<b>重点</b>", html)
        self.assertIn("<code>x=1</code>", html)

    def test_html_escaped(self):
        html = md_subset.render_markdown("a < b & c > d")
        self.assertIn("a &lt; b &amp; c &gt; d", html)

    def test_external_link(self):
        html = md_subset.render_markdown("[飞牛](https://www.fnnas.com)")
        self.assertIn('<a href="https://www.fnnas.com"', html)
        self.assertIn("飞牛</a>", html)

    def test_md_link_degrades_to_code(self):
        html = md_subset.render_markdown("[相册](../modules/album.md)")
        self.assertIn("<code>相册</code>", html)
        self.assertNotIn("href", html)

    def test_code_span_protects_bold(self):
        html = md_subset.render_markdown("`a**b**c`")
        self.assertIn("<code>a**b**c</code>", html)


class TestRealDocs(unittest.TestCase):
    def test_album_doc_renders(self):
        path = os.path.join(ROOT, "docs", "modules", "album.md")
        if not os.path.exists(path):
            self.skipTest("没有相册文档")
        with open(path, encoding="utf-8") as f:
            text = f.read()
        html = md_subset.render_markdown(text)
        for needle in ("<h2>", 'table class="kv"', 'pre class="sample', "<li>"):
            self.assertIn(needle, html)
        # 不应有未渲染的表格行或残留加粗标记
        self.assertNotIn("<p>|", html)
        self.assertNotIn("**", html)


if __name__ == "__main__":
    unittest.main(verbosity=2)
