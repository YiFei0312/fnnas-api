# -*- coding: utf-8 -*-
"""
离线用例：`/p` 相册应用 HTTP 客户端（`sdk/http_photo.py`）。

覆盖签名算法、请求拼装（路径/参数/body）、响应解包与错误抛出、相册方法;
不连 NAS。
"""

import asyncio
import json
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from sdk.http_photo import (APP_KEY, APP_SECRET, PhotoHttpClient,        # noqa: E402
                            PhotoHttpError, make_authx)


def run(coro):
    return asyncio.new_event_loop().run_until_complete(coro)


class TestAuthx(unittest.TestCase):
    def test_format(self):
        value = make_authx("GET", "/p/api/v1/album/list")
        self.assertRegex(value, r"^nonce=\d{6}&timestamp=\d{13}&sign=[0-9a-f]{32}$")

    def test_params_sorted_so_order_does_not_matter(self):
        def sign(params):
            return make_authx("GET", "/p/x", params=params,
                              nonce=123456, stamp=1700000000000)
        self.assertEqual(sign({"limit": 10, "offset": 0}),
                         sign({"offset": 0, "limit": 10}))
        self.assertNotEqual(sign({"limit": 10, "offset": 0}),
                            sign({"limit": 20, "offset": 0}))

    def test_body_and_path_participate(self):
        def sign(path, body):
            return make_authx("POST", path, body=body,
                              nonce=123456, stamp=1700000000000)
        self.assertNotEqual(sign("/p/a", {"x": 1}), sign("/p/a", {"x": 2}))
        self.assertNotEqual(sign("/p/a", {"x": 1}), sign("/p/b", {"x": 1}))

    def test_secret_changes_sign(self):
        a = make_authx("GET", "/p/x", nonce=1, stamp=2)
        b = make_authx("GET", "/p/x", secret="other-secret", nonce=1, stamp=2)
        self.assertNotEqual(a, b)


class FakeClient(PhotoHttpClient):
    """把底层 HTTP 换掉，只验证方法拼出来的请求"""

    def __init__(self, response=None, error=None):
        super().__init__("http://fake:5666", token="tok")
        self.calls = []
        self.response = response if response is not None else {"ok": True}
        self.error = error

    def _request_sync(self, method, path, params=None, body=None):
        self.calls.append({"method": method, "path": path,
                           "params": params, "body": body})
        if self.error:
            raise self.error
        return self.response

    def last_call(self):
        return self.calls[-1]


class TestAlbumMethods(unittest.TestCase):
    def test_albums_params(self):
        c = FakeClient()
        run(c.albums())
        call = c.last_call()
        self.assertEqual(call["method"], "GET")
        self.assertEqual(call["path"], "/api/v1/album/list")
        self.assertEqual(call["params"]["offset"], 0)
        self.assertIn("sort_by", call["params"])

    def test_album_detail_uses_snake_case(self):
        c = FakeClient()
        run(c.album(8))
        self.assertEqual(c.last_call()["params"], {"album_id": 8})

    def test_album_create_body(self):
        c = FakeClient()
        run(c.album_create("旅行", [6958]))
        call = c.last_call()
        self.assertEqual(call["method"], "POST")
        self.assertEqual(call["body"], {"album_name": "旅行", "ids": [6958]})

    def test_album_timeline_uses_camel_case(self):
        c = FakeClient()
        run(c.album_timeline(8))
        params = c.last_call()["params"]
        self.assertEqual(params["albumId"], 8)
        self.assertIn("startTime", params)
        self.assertIn("endTime", params)

    def test_album_delete_and_photos(self):
        c = FakeClient()
        run(c.album_delete(8))
        self.assertEqual(c.last_call()["body"], {"album_id": 8})
        run(c.album_add_photos(8, [1, 2]))
        self.assertEqual(c.last_call()["body"], {"ids": [1, 2], "album_id": 8})
        run(c.album_remove_photos(8, [1]))
        self.assertEqual(c.last_call()["body"], {"ids": [1], "album_id": 8})

    def test_photos_requires_colon_date(self):
        c = FakeClient()
        run(c.photos("2026:10:04 00:00:00", "2026:10:04 23:59:59"))
        params = c.last_call()["params"]
        self.assertEqual(params["start_time"], "2026:10:04 00:00:00")
        self.assertEqual(params["mode"], "datetime")

    def test_error_raises_with_code(self):
        c = FakeClient(error=PhotoHttpError(400, "invalid params",
                                            "/api/v1/album/item"))
        with self.assertRaises(PhotoHttpError) as ctx:
            run(c.album(1))
        self.assertEqual(ctx.exception.code, 400)

    def test_no_token_rejected(self):
        c = PhotoHttpClient("http://fake:5666")
        with self.assertRaises(PhotoHttpError):
            c._request_sync("GET", "/api/v1/album/list")


class TestResponseUnwrap(unittest.TestCase):
    def test_request_returns_data(self):
        class C(PhotoHttpClient):
            def _request_sync(self, method, path, params=None, body=None):
                return {"list": []}
        c = C("http://fake:5666", token="t")
        self.assertEqual(run(c.request("GET", "/x")), {"list": []})

    def test_constants_are_the_live_ones(self):
        self.assertEqual(len(APP_KEY), 30)          # 前端硬编码的 appkey
        self.assertEqual(len(APP_SECRET), 36)       # XOR 解出来的应用密钥是 UUID 形态
        self.assertEqual(APP_SECRET.count("-"), 4)


if __name__ == "__main__":
    unittest.main(verbosity=2)
