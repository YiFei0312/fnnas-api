# -*- coding: utf-8 -*-
"""
离线用例：文件管理接口的封装（参数形态按真机实测）+ 异步任务等待器。

对应实测工具 `tools/probe_file.py`（真机跑过：
`python tools/probe_file.py --yes`），这里只测「发出去的参数对不对」，
不连 NAS。
"""

import asyncio
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from sdk.api.curated import FileOpsApiMixin                              # noqa: E402
from sdk.filetasks import call_file_task, install_sniffer, is_task_ok    # noqa: E402
from sdk.filetasks import task_error, wait_file_task                     # noqa: E402
from tools.probe_common import classify                                  # noqa: E402


def run(coro):
    return asyncio.new_event_loop().run_until_complete(coro)


class FakeFileClient(FileOpsApiMixin):
    """只记录请求，不真的发"""

    def __init__(self, response=None):
        self.seen = []
        self.response = response if response is not None else {"result": "succ"}

    async def request(self, req=None, **params):
        self.seen.append((req, params))
        return dict(self.response, reqid="rid-1") if isinstance(self.response, dict) \
            else self.response

    async def call(self, req, params=None, timeout=None, nested=False):
        self.seen.append((req, params or {}))
        return dict(self.response, reqid="rid-1")


class TestFileOpsParams(unittest.TestCase):
    def setUp(self):
        self.c = FakeFileClient()
        self.req = lambda: self.c.seen[-1]

    def test_prop_uses_files_array(self):
        run(self.c.file_prop("/vol1/1000/tmp/a.jpg", "/vol1/1000/tmp/b.jpg"))
        self.assertEqual(self.req()[0], "file.prop")
        self.assertEqual(self.req()[1]["files"],
                         ["/vol1/1000/tmp/a.jpg", "/vol1/1000/tmp/b.jpg"])

    def test_size_uses_single_file(self):
        run(self.c.file_size("/vol1/1000/tmp"))
        self.assertEqual(self.req(), ("file.size", {"file": "/vol1/1000/tmp"}))

    def test_calc_access_use_files(self):
        run(self.c.file_calc("/vol1/1000/tmp"))
        self.assertEqual(self.req(), ("file.calc", {"files": ["/vol1/1000/tmp"],
                                                    "timeout": -1}))
        run(self.c.file_access("/vol1/1000/tmp"))
        self.assertEqual(self.req(), ("file.access", {"files": ["/vol1/1000/tmp"]}))

    def test_acl_get_prop_flag(self):
        run(self.c.file_acl("/vol1/1000/tmp", get_prop=True))
        self.assertEqual(self.req(), ("file.getAcl", {"path": "/vol1/1000/tmp",
                                                      "getProp": True}))

    def test_cp_mv_use_path_to(self):
        run(self.c.file_cp("/a.jpg", "/vol1/1000/tmp/dst"))
        req, params = self.req()
        self.assertEqual(req, "file.cp")
        self.assertEqual(params["files"], ["/a.jpg"])
        self.assertEqual(params["pathTo"], "/vol1/1000/tmp/dst")
        self.assertEqual(params["overwrite"], 1)
        self.assertNotIn("src", params)          # 老封装用的 src/dst 是错的
        run(self.c.file_mv(["a", "b"], "/dst"))
        self.assertEqual(self.req()[1]["files"], ["a", "b"])

    def test_extract_never_sends_empty_fromcharset(self):
        run(self.c.file_extract("/tmp/a.zip", "/tmp/out"))
        params = self.req()[1]
        self.assertEqual(params["file"], "/tmp/a.zip")
        self.assertEqual(params["path"], "/tmp/out")
        self.assertNotIn("fromCharset", params)   # 传空串服务端会报 Too short switch

    def test_compress_level_and_optional_passwd(self):
        run(self.c.file_compress("/tmp/a.jpg", "/tmp/a.zip", description="d"))
        params = self.req()[1]
        self.assertEqual(params["files"], ["/tmp/a.jpg"])
        self.assertEqual(params["path"], "/tmp/a.zip")
        self.assertNotIn("passwd", params)
        run(self.c.file_compress("/tmp/a.jpg", "/tmp/a.zip", passwd="1234"))
        self.assertEqual(self.req()[1]["passwd"], "1234")

    def test_chown_setacl_recent(self):
        run(self.c.file_chown("/tmp/x", 1000, 1000))
        self.assertEqual(self.req(), ("file.chown", {"files": ["/tmp/x"],
                                                     "uid": 1000, "gid": 1000}))
        run(self.c.file_set_acl("/tmp/x", [{"owner": 6}], sub=True))
        params = self.req()[1]
        self.assertEqual(self.req()[0], "file.setAcl2")     # setAcl 不存在，走 setAcl2
        self.assertEqual(params["sub"], 1)
        run(self.c.file_recent_del("/a", "/b"))
        self.assertEqual(self.req()[1]["path"], ["/a", "/b"])   # 数组，不是单值
        run(self.c.file_fav_del("/a"))
        self.assertEqual(self.req()[1]["path"], "/a")            # fav 是单值

    def test_check_upload_overwrite_optional(self):
        run(self.c.file_check_upload(420, "/tmp/a.txt"))
        self.assertNotIn("overwrite", self.req()[1])
        run(self.c.file_check_upload(420, "/tmp/a.txt", overwrite=2))
        self.assertEqual(self.req()[1]["overwrite"], 2)

    def test_readonly_getters_unwrap(self):
        c = FakeFileClient({"result": "succ", "prop": [{"size": 1}], "access": [6],
                            "fav": [{"path": "/a"}], "files": [{"name": "x"}],
                            "recent": [{"name": "y"}],
                            "download": [{"uri": "/download/x"}]})
        self.assertEqual(run(c.file_prop("/a")), [{"size": 1}])
        self.assertEqual(run(c.file_access("/a")), [6])
        self.assertEqual(run(c.file_favorites()), [{"path": "/a"}])
        # file.recent.list 的响应键是 recent（不是 files）
        self.assertEqual(run(c.file_recent()), [{"name": "y"}])
        self.assertEqual(run(c.file_trash()), [{"name": "x"}])
        self.assertEqual(run(c.file_download("/a")), [{"uri": "/download/x"}])


class TestTaskWaiter(unittest.TestCase):
    class Stub:
        def __init__(self):
            self.handlers = []
            self.script = []
            install_sniffer(self)          # 真客户端在 __init__ 里就装了

        def add_push_handler(self, matcher, callback=None):
            if callback is None:
                self.handlers.append((matcher, matcher))
                return matcher
            self.handlers.append((matcher, callback))
            return callback

        async def call(self, req, params=None, timeout=None, nested=False):
            return {"sysNotify": "taskId", "taskId": "tid", "reqid": "rid-1"}

        def push(self, payload):
            for _matcher, cb in self.handlers:
                cb(self, payload)

    def test_result_already_arrived(self):
        c = self.Stub()
        c.push({"result": "succ", "reqid": "rid-1"})      # 先到
        self.assertTrue(is_task_ok(run(wait_file_task(c, "rid-1", timeout=1))))

    def test_result_arrives_later(self):
        c = self.Stub()
        task = asyncio.ensure_future(wait_file_task(c, "rid-1", timeout=5))

        async def fire():
            await asyncio.sleep(0.05)
            c.push({"result": "fail", "reqid": "rid-1",
                    "failedFiles": [{"file": "/a", "errno": 4100}]})
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(task, fire()))
        result = task.result()
        self.assertFalse(is_task_ok(result))
        self.assertIn("errno=4100", task_error(result))

    def test_timeout_returns_none(self):
        c = self.Stub()
        self.assertIsNone(run(wait_file_task(c, "nope", timeout=0.1)))
        self.assertFalse(is_task_ok(None))
        self.assertIn("超时", task_error(None))

    def test_call_file_task_waits(self):
        c = self.Stub()

        async def main():
            task = asyncio.ensure_future(call_file_task(c, "file.rm", {"files": ["/a"]},
                                                        timeout=5))
            await asyncio.sleep(0.05)
            c.push({"result": "succ", "reqid": "rid-1"})
            return await task
        _resp, result = run(main())
        self.assertTrue(is_task_ok(result))


class TestClassifyFlatEnvelope(unittest.TestCase):
    """平铺外壳（file.*）成功时没有 result 字段，不能算 other"""

    def test_flat_success_is_succ(self):
        self.assertEqual(classify({"files": [], "uver": 1})[0], "succ")
        self.assertEqual(classify({"size": 1, "reqid": "x"})[0], "succ")

    def test_explicit_results(self):
        self.assertEqual(classify({"result": "succ"})[0], "succ")
        self.assertEqual(classify({"result": "fail"})[0], "other")
        self.assertEqual(classify({"result": "fail", "errno": 8192})[0], "param_error")
        self.assertEqual(classify({"result": "fail", "errno": 10000002})[0], "unknown")
        self.assertEqual(classify({"result": "fail", "errno": 4100})[0], "error")


class TestDocMetaCoversFileFamily(unittest.TestCase):
    def test_every_file_req_has_purpose(self):
        from tools.api_doc_meta import PARAM_HINTS, PURPOSE
        import json
        spec = json.load(open(os.path.join(ROOT, "data", "api_spec.json"),
                              encoding="utf-8"))["spec"]
        file_reqs = [r for r in spec if r.startswith("file.")]
        self.assertGreater(len(file_reqs), 30)
        missing = [r for r in file_reqs if r not in PURPOSE]
        self.assertEqual(missing, [], f"这些 file.* 接口缺用途说明：{missing}")

    def test_confirmed_params_documented(self):
        from tools.api_doc_meta import PARAM_HINTS
        # 实测确认过的参数名必须在文档里（防止以后又写回 path/src/dst）
        self.assertIn("files", PARAM_HINTS["file.prop"])
        self.assertIn("file", PARAM_HINTS["file.size"])
        self.assertIn("pathTo", PARAM_HINTS["file.cp"])
        self.assertIn("pathTo", PARAM_HINTS["file.mv"])
        self.assertIn("fromCharset", PARAM_HINTS["file.extract"])
        self.assertIn("sub", PARAM_HINTS["file.setAcl2"])
        for bad in ("src", "dst"):
            self.assertNotIn(bad, PARAM_HINTS["file.cp"])
            self.assertNotIn(bad, PARAM_HINTS["file.mv"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
