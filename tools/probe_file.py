# -*- coding: utf-8 -*-
"""
文件管理接口实测工具：在 NAS 上一个临时目录里，把 `file.*` 的**可逆**操作都跑一遍。

和 `tools/probe.py` / `tools/probe_share.py` 的分工：
    probe.py        带空参数批量探测，只能判断「接口在不在」
    probe_share.py  分享链接的完整生命周期（创建 → … → 删除）
    probe_file.py   文件管理：属性/权限/复制/移动/改名/压缩/解压/回收站/收藏/最近访问，
                    以及上传（HTTP）和删除 —— 全部在**自己新建的临时目录**里做

⚠️ 写接口的返回值只是「任务受理」，真正成败要看同 reqid 的推送（本工具会等）：
    ack    {"sysNotify":"taskId","taskId":"<base64>","reqid":"..."}
    push   {"sysNotify":"taskInfo","taskInfo":{...原参数...,"taskId":...}}
    push   {"percent":100,"size":...,"reqid":"..."}                  # 进度
    push   {"result":"succ","reqid":"..."} | {"result":"fail","reqid":"...","failedFiles":[{file,errno}]}

安全性（重要）：
    1. 默认 dry-run，不加 --yes 什么都不做；
    2. 所有写操作只发生在 `<--path>/<SCRATCH_PREFIX><时间戳>/` 这个自己新建的目录里，
       不会改动 --path 里原有的任何文件（原文件只读：ls/prop/access/calc/getAcl/download）；
    3. 删除前会断言目标路径就是那个临时目录（前缀 + 位于 --path 之下），否则拒绝执行；
    4. 收尾把临时目录清掉，并复查 --path 的列表与开始时**逐项一致**，
       同时复查原文件的 size/mtim 没变（证明没碰用户数据）；
    5. `file.trash.clear` 这种会波及别人的接口**不测**（只读列表 + 还原自己的文件）。

用法：
    python tools/probe_file.py                 # dry-run：只打印计划
    python tools/probe_file.py --yes           # 真跑，跑完自动清理
    python tools/probe_file.py --yes --keep    # 保留临时目录（调试用）
    python tools/probe_file.py --yes --path /vol1/1000/tmp

产物：
    data/file_probe.json     完整调用日志（参数 + 原始响应 + 任务结果 + 期间推送）
    data/probe_status.json   --merge 时把结论并进去（供 gen_api.py 使用）
"""

import argparse
import asyncio
import json
import mimetypes
import os
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sdk import FnOsClient                                            # noqa: E402
from sdk.push import is_pong                                         # noqa: E402
from tools.probe import PARAM_ERROR_ERRNO                             # noqa: E402
from tools.probe_common import DEFAULT_URL, Prober                    # noqa: E402
from tools.probe_common import merge_probe_status                     # noqa: E402

SCRATCH_PREFIX = "fnapi_filetest_"


def join(base, *parts):
    return "/".join([base.rstrip("/")] + [str(p).strip("/") for p in parts])


class FileProber(Prober):
    source = "tools/probe_file.py"

    def __init__(self, client, base, sample_limit=4000):
        super().__init__(client, sample_limit=sample_limit)
        self.base = base.rstrip("/")
        self.scratch = join(self.base, SCRATCH_PREFIX + time.strftime("%Y%m%d_%H%M%S"))
        self.pushes = []
        self.task_results = {}          # reqid -> 任务的最终推送
        self.notes = []
        self.prop_before = None
        self.baseline = None
        self.fav_hit = None
        self.trash_hit = None
        self.last_task_id = None

    # ---------------------------------------------------------------- 基础工具
    def abs_path(self, relative):
        return relative if relative.startswith("/") else "/" + relative

    async def ls(self, path):
        """列目录（file.ls 的 path 用不带前导斜杠的形式）"""
        resp = await self.client.api.file.ls(path=self.abs_path(path).lstrip("/"))
        return (resp or {}).get("files") or []

    async def exists(self, path):
        resp = await self.client.call("file.prop", {"files": [path]})
        prop = (resp or {}).get("prop") or [{}]
        first = prop[0] if prop else {}
        return not first.get("errno")

    async def wait_path(self, path, expect=True, timeout=25.0):
        """等异步任务落地：轮询 file.prop 直到文件出现/消失"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            try:
                if await self.exists(path) == expect:
                    return True
            except Exception:                                      # pragma: no cover
                pass
            await asyncio.sleep(0.6)
        return False

    async def snapshot(self):
        entries = await self.ls(self.base)
        return {e["name"]: (e.get("dir", 0), e.get("size"), e.get("mtim"))
                for e in entries}

    def note(self, text):
        self.notes.append(text)
        print(f"  · {text}")

    # ------------------------------------------------------- 异步任务：等结果
    def on_push(self, payload):
        """收集推送；带 result 的推送按 reqid 存起来当任务结果"""
        if is_pong(payload):
            return
        self.pushes.append({"at": time.strftime("%H:%M:%S"), "payload": payload})
        rid = payload.get("reqid")
        if rid and "result" in payload:
            self.task_results[rid] = payload
        if payload.get("sysNotify") == "taskId" and payload.get("taskId"):
            self.last_task_id = payload["taskId"]

    async def wait_task(self, reqid, timeout=40.0):
        deadline = time.time() + timeout
        while time.time() < deadline:
            if reqid in self.task_results:
                return self.task_results[reqid]
            await asyncio.sleep(0.3)
        return None

    async def call_task(self, req, params, note, timeout=40.0):
        """发一个异步写接口，并等它同 reqid 的任务结果（成败以推送为准）"""
        resp = await self.call(req, params, note=note)
        rid = (resp or {}).get("reqid")
        record = self.calls[-1]
        if not rid:
            return resp, None
        record["task_reqid"] = rid
        final = await self.wait_task(rid, timeout)
        if final is None:
            record["task_status"] = "timeout"
            print("    … 任务超时未回结果")
            return resp, None
        ok = final.get("result") == "succ"
        record["task_status"] = "succ" if ok else "fail"
        record["task_sample"] = json.dumps(final, ensure_ascii=False)[:500]
        if not ok:
            errno = final.get("errno")
            record["status"] = "param_error" if errno in PARAM_ERROR_ERRNO else "error"
            record["errno"] = errno
        print(f"    任务结果 {'succ' if ok else 'fail'}："
              f"{json.dumps(final, ensure_ascii=False)[:170]}")
        return resp, final

    # ------------------------------------------------------------------- 主流程
    async def run(self, keep=False):
        base = self.base

        print("--- 0) 记录基线（照原样复原的对照）")
        self.baseline = await self.snapshot()
        print(f"  {base} 现有 {len(self.baseline)} 项："
              f"{', '.join(sorted(self.baseline))}")
        original = None
        for name, (is_dir, _size, _mtim) in sorted(self.baseline.items()):
            if not is_dir:
                original = join(base, name)
                break
        if original is None:
            raise RuntimeError(f"{base} 里没有可用于测试的文件")
        print(f"  只读测试对象（不会改动）：{original}")
        prop_before = await self.client.call("file.prop", {"files": [original]})
        self.prop_before = ((prop_before or {}).get("prop") or [{}])[0]
        print(f"  原始属性：{json.dumps(self.prop_before, ensure_ascii=False)}")

        await self._read_phase(original)

        # ------------------------------------------------- 2) 自己建临时目录
        print(f"\n--- 2) 在临时目录里做可逆写操作：{self.scratch}")
        scratch = self.scratch
        error = None
        try:
            await self._write_phase(scratch, original)
        except Exception as exc:
            # 中途失败也要继续往下走：清理 + 核对复原
            error = f"{type(exc).__name__}: {exc}"
            print(f"\n!! 中间步骤出错：{error}（继续清理并核对复原）")

        print("\n--- 11) 清理临时目录")
        if keep:
            self.note(f"--keep：保留 {scratch}（记得自己删）")
        else:
            self._assert_scratch_safe(scratch)
            await self.call_task("file.rm", {"files": [scratch], "moveToTrashbin": False,
                                             "details": {"name": scratch.rsplit("/", 1)[-1],
                                                         "dir": 1, "count": 1}},
                                 note="删除临时目录（自己建的，直接删）")
            gone = await self.wait_path(scratch, expect=False, timeout=20)
            self.note(f"临时目录已删除：{gone}")

        # ------------------------------------------------------ 12) 复原核对
        print("\n--- 12) 复原核对")
        after = await self.snapshot()
        same = after == self.baseline
        self.note(f"{base} 与开始时一致：{same}")
        if not same:
            self.note(f"  开始：{sorted(self.baseline)}")
            self.note(f"  结束：{sorted(after)}")
        prop_after = await self.client.call("file.prop", {"files": [original]})
        prop_now = ((prop_after or {}).get("prop") or [{}])[0]
        unchanged = all(prop_now.get(k) == self.prop_before.get(k)
                        for k in ("size", "mtim", "btim"))
        self.note(f"原文件 size/mtim/btim 未变：{unchanged}")
        if not keep and not self.trash_hit:
            self.note("注意：有 1 个 20 字节的测试文件进了回收站且没能还原回来"
                      "（file.trash.restore 语义未确认），可在 Web UI 里清掉")
        return {"scratch": scratch, "original": original, "baseline_restored": same,
                "original_unchanged": unchanged, "kept": bool(keep),
                "error": error, "fav_hit": self.fav_hit, "trash_hit": self.trash_hit}

    # ------------------------------------------------------------ 只读阶段
    async def _read_phase(self, original):
        base = self.base
        print(f"\n--- 1) 只读接口（对象：{base} / 原文件）")
        rel = await self.call("file.ls", {"path": base.lstrip("/")},
                              note="列目录（相对路径写法）")
        abs_resp = await self.call("file.ls", {"path": base},
                                   note="列目录（绝对路径写法，对比）")
        rel_names = [e["name"] for e in (rel or {}).get("files") or []]
        abs_names = [e["name"] for e in (abs_resp or {}).get("files") or []]
        self.note(f"两种 path 写法结果一致：{rel_names == abs_names}"
                  f"（{len(rel_names)} 项：{', '.join(rel_names)}）")
        await self.call("file.lsDir", {"path": base.lstrip("/")}, note="列目录（分页/精简版）")
        await self.call("file.prop", {"files": [original]}, note="多个路径的属性")
        await self.call("file.prop", {"files": [base]}, note="目录属性")
        missing = await self.call("file.prop", {"files": [join(base, "__not_exist__.bin")]},
                                  note="不存在的文件 → 看条目里的 errno")
        item = (((missing or {}).get("prop") or [{}]) or [{}])[0]
        self.note(f"不存在的路径：外层 succ，条目里 errno={item.get('errno')}"
                  f"（4100 = 路径不存在）")
        await self.call("file.access", {"files": [original]}, note="当前用户权限位")
        await self.call("file.calc", {"files": [original]}, note="统计（同步返回 totals）")
        await self.call("file.getAcl", {"path": original}, note="读 ACL")
        await self.call("file.getAcl", {"path": original, "getProp": True}, note="读 ACL + 属性")
        # file.size 的参数名在前端里没有调用点，逐个试常见写法（都失败就如实记录）
        for params in ({"path": original}, {"files": [original]}, {"file": original},
                       {"paths": [original]}, {"file": base}):
            await self.call("file.size", params, note="占用大小（参数名未确认，逐个试）")
        usage = await self.call("file.usage", {}, note="存储占用统计（异步任务）")
        self.note(f"file.usage 返回 taskId={json.dumps((usage or {}).get('taskId'))}，"
                  f"分类用量靠推送（sysNotify={json.dumps((usage or {}).get('sysNotify'))}）")
        download = await self.call("file.download", {"files": [original]}, note="取下载地址")
        await self._check_download(download, original)
        await self.call("file.fav.list", {}, note="收藏夹")
        await self.call("file.recent.list", {}, note="最近访问")
        trash = await self.call("file.trash.list", {}, note="回收站（当前用户）")
        await self.call("file.trash.list", {"uid": 1000}, note="回收站（指定 uid，管理员）")
        entries = (trash or {}).get("files") or []
        self.note(f"回收站现有 {len(entries)} 项（只读，不动它们）")
        if entries:
            self.note(f"回收站条目字段：{sorted(entries[0])}")
        await self.call("file.team.lsDir", {}, note="团队空间目录（本机可能没有）")
        for params in ({"taskId": 999999999}, {"taskId": "999999999"},
                       {"taskIds": [999999999]}, {"id": 999999999}):
            await self.call("file.cancel", params, note="取消任务（先试错误参数名）")

    # ------------------------------------------------------------ 写入阶段
    async def _write_phase(self, scratch, original):
        base_name = original.rsplit("/", 1)[-1]

        await self.call("file.mkdir", {"path": scratch}, note="新建临时目录")
        if not await self.exists(scratch):
            raise RuntimeError(f"临时目录创建失败：{scratch}")
        await self.call("file.mkdir", {"path": join(scratch, "sub")}, note="建子目录（给 mv 用）")

        print("\n--- 3) 上传（HTTP /upload，前置 file.checkUpload）")
        local = self._make_local_sample()
        await self._upload(local, join(scratch, "upload.txt"))

        print("\n--- 4) checkUpload 的 overwrite 语义（0 跳过 / 1 覆盖 / 2 保留两者）")
        size = os.path.getsize(local)
        await self.call("file.checkUpload", {"size": size, "path": join(scratch, "fresh.txt")},
                        note="新文件（overwrite 省略）")
        for overwrite in (0, 1, 2):
            await self.call("file.checkUpload",
                            {"size": size, "path": join(scratch, "upload.txt"),
                             "overwrite": overwrite},
                            note=f"已存在 + overwrite={overwrite}")

        print("\n--- 5) 收藏 / 最近访问（加完就删，完全可逆）")
        await self.call("file.fav.add", {"path": scratch}, note="加收藏")
        fav = await self.call("file.fav.list", {}, note="收藏夹里应出现临时目录")
        fav_names = [f.get("path") for f in ((fav or {}).get("fav") or [])]
        self.fav_hit = scratch in fav_names
        self.note(f"收藏夹命中：{self.fav_hit}")
        await self.call("file.fav.del", {"path": scratch}, note="取消收藏")
        await self.call("file.recent.add", {"path": join(scratch, "upload.txt")}, note="加最近访问")
        await self.call("file.recent.del", {"path": [join(scratch, "upload.txt")]},
                        note="删最近访问（注意 path 是数组）")

        print("\n--- 6) 复制 / 改名 / 移动")
        # pathTo 是「目标目录」，复制过去保持原文件名
        copy_to = join(scratch, base_name)
        await self.call_task("file.cp", {"files": [original], "pathTo": scratch, "overwrite": 1,
                                         "details": {"name": base_name, "count": 1}},
                             note="复制原文件到临时目录")
        self.note(f"复制件出现：{await self.wait_path(copy_to)}（{copy_to}）")
        renamed = join(scratch, "renamed.jpg")
        await self.call("file.rename", {"path": copy_to, "newName": "renamed.jpg"},
                        note="改名（同步接口，失败会直接回 errno）")
        self.note(f"改名后存在：{await self.exists(renamed)}（{renamed}）")
        moved = join(scratch, "sub", "renamed.jpg")
        await self.call_task("file.mv", {"files": [renamed], "pathTo": join(scratch, "sub"),
                                         "overwrite": 1,
                                         "details": {"name": "renamed.jpg", "count": 1}},
                             note="移动到子目录")
        self.note(f"移动后存在：{await self.wait_path(moved)}（{moved}）")

        print("\n--- 7) 压缩 / 解压")
        archive = join(scratch, "arch.zip")
        for files in ([moved], ["renamed.jpg"], ["sub/renamed.jpg"]):
            await self.call_task("file.compress",
                                 {"description": "fnapi 测试压缩", "path": archive,
                                  "files": files, "level": 0,
                                  "details": {"name": "arch.zip", "count": 1}},
                                 note=f"压缩（files 用 {files[0]} 这种写法）")
            if await self.wait_path(archive, timeout=20):
                break
        self.note(f"压缩包出现：{await self.exists(archive)}（{archive}）")
        outdir = join(scratch, "out")
        if await self.exists(archive):
            # 注意：fromCharset 传空串会让服务端报 “Too short switch: -fromcharset”，不传就行
            await self.call_task("file.extract",
                                 {"description": "fnapi 测试解压", "path": outdir,
                                  "file": archive, "overwrite": 1,
                                  "details": {"name": "arch.zip", "count": 1}},
                                 note="解压到 out/（不传 fromCharset）")
            await asyncio.sleep(1.0)
            out_entries = await self.ls(outdir) if await self.exists(outdir) else []
            self.note(f"解压结果：{[e['name'] for e in out_entries]}")

        print("\n--- 8) 权限 / 属主（原样写回，不产生净变化）")
        acl = await self.call("file.getAcl", {"path": scratch}, note="先读当前 ACL")
        permset = (acl or {}).get("permset") or []
        details = {"name": scratch.rsplit("/", 1)[-1], "dir": 1, "count": 1}
        await self.call_task("file.setAcl2", {"files": [scratch], "permset": permset,
                                              "details": details, "sub": 1},
                             note="写回同样的 ACL（setAcl2，UI 用的就是它）")
        await self.call("file.setAcl", {"files": [scratch], "permset": permset,
                                        "details": details}, note="旧接口 setAcl（对照）")
        await self.call("file.chown", {"path": scratch, "uid": 1000, "gid": 1000},
                        note="chown 的错误参数写法（path）")
        await self.call_task("file.chown", {"files": [scratch], "uid": 1000, "gid": 1000},
                             note="chown 成原所有者（1000→1000，无净变化）")
        for params in ({"path": scratch}, {"files": [scratch]}, {"taskId": "x"},
                       {"dir": scratch}):
            await self.call("file.trimacl.conv", params, note="权限转 ACL 模型（参数未确认）")
        for params in ({}, {"taskId": "x"}, {"path": scratch}):
            await self.call("file.trimacl.conv.report", params,
                            note="权限转换进度报告（参数未确认）")

        print("\n--- 9) 回收站：删自己建的小文件 → （还原试过了但没成功，见下）")
        # 用一个 20 字节的小文件做回收站实验：file.rm 到回收站后我们没法把它彻底清掉
        # （见 docs/modules/file.md 的说明），所以别拿大文件试。
        victim = join(scratch, "trash-victim.txt")
        victim_local = self._make_local_sample(name="trash-victim.txt", lines=1)
        await self._upload(victim_local, victim)
        await self.call_task("file.rm", {"files": [victim], "moveToTrashbin": True,
                                         "details": {"name": "trash-victim.txt", "count": 1}},
                             note="删除到回收站（可还原）")
        self.note(f"原位置已消失：{await self.wait_path(victim, expect=False)}")
        trash = await self.call("file.trash.list", {}, note="回收站顶层条目（只读）")
        entries = (trash or {}).get("files") or []
        self.note(f"顶层回收站 {len(entries)} 条，字段 {sorted(entries[0]) if entries else []}")
        listed = await self.call("file.trash.list", {"path": join(scratch, "sub")},
                                 note="trash.list 传 path → 行为等同列目录")
        self.note(f"path 模式返回 {len((listed or {}).get('files') or [])} 条"
                  f"（内容与 file.ls 一致，不是回收站条目）")
        # 还原：ack 和任务结果都回 succ，但文件没回来 —— 说明 files 要传回收站内部路径，
        # 而 file.trash.list 并不暴露它。这个结论不写进文档（会误导），只留日志。
        await self.call_task("file.trash.restore",
                             {"files": [victim], "overwrite": 1,
                              "details": {"name": "trash-victim.txt", "count": 1}},
                             note="尝试还原（原路径）")
        back = await self.wait_path(victim, timeout=12)
        self.note(f"还原是否真的回来了：{back}"
                  f"（回 succ 但文件没回来 → files 路径形态未确认）")
        self.calls[-1].update(skip_merge=True,
                              skip_reason="接口回 succ 但文件没真的还原，语义未确认")
        self.trash_hit = back

        print("\n--- 10) 取消任务（用真实 taskId 试参数名）")
        if self.last_task_id:
            for params in ({"taskId": self.last_task_id},
                           {"taskId": self.last_task_id, "type": 1},
                           {"taskIds": [self.last_task_id]}):
                await self.call("file.cancel", params, note="取消刚跑完的任务")

    # ------------------------------------------------------------------ 辅助
    def _assert_scratch_safe(self, path):
        """删除前的硬保险：只允许删自己建的、位于 --path 之下的临时目录"""
        name = path.rsplit("/", 1)[-1]
        if not name.startswith(SCRATCH_PREFIX):
            raise RuntimeError(f"拒绝删除：{path} 不是本工具创建的临时目录")
        if not path.startswith(self.base + "/"):
            raise RuntimeError(f"拒绝删除：{path} 不在 {self.base} 之下")

    def _make_local_sample(self, name=None, lines=20):
        path = os.path.join(os.environ.get("TEMP", "."), SCRATCH_PREFIX + (name or "upload.txt"))
        with open(path, "w", encoding="utf-8") as f:
            f.write("fnOS file api probe\n" * lines)
        return path

    async def _check_download(self, resp, original):
        """file.download 返回的是带签名的 HTTP 地址，顺手下载一次核对大小"""
        items = (resp or {}).get("download") or []
        uri = items[0].get("uri") if items else None
        if not uri:
            self.note("file.download 没给 uri，跳过下载核对")
            return
        url = uri if uri.startswith("http") else f"{self.client.base_url}{uri}"
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                got = r.read()
            want = await self.client.call("file.prop", {"files": [original]})
            size = (((want or {}).get("prop") or [{}])[0] or {}).get("size")
            same = size == len(got)
            self.note(f"下载核对：HTTP {r.status}，{len(got)} 字节，"
                      f"与原文件大小一致：{same}")
            self.calls.append({
                "req": "file.download(HTTP)", "params": {"url": url}, "nested": False,
                "note": "GET file.download 给的 uri", "status": "succ" if same else "error",
                "errno": None, "resp_keys": ["http"], "elapsed_ms": None,
                "sample": json.dumps({"http": r.status, "bytes": len(got)})})
        except Exception as exc:                                   # pragma: no cover
            self.note(f"下载核对失败：{type(exc).__name__}: {exc}")
            self.calls.append({"req": "file.download(HTTP)", "params": {"url": url},
                               "nested": False, "note": "GET uri", "status": "exception",
                               "error": str(exc)[:200]})

    async def _upload(self, local_path, nas_path):
        """走 SDK 记录的 HTTP 上传流程：checkUpload 拿 uploadName → POST /upload"""
        client = self.client
        size = os.path.getsize(local_path)
        check = await self.call("file.checkUpload", {"size": size, "path": nas_path,
                                                    "overwrite": 0},
                                note="上传前置检查（拿 uploadName）")
        upload_name = (check or {}).get("uploadName") or os.path.basename(nas_path)
        base_url = client.base_url
        if not base_url:
            raise RuntimeError("base_url 为空，无法拼上传地址")
        folder = nas_path.rsplit("/", 1)[0]
        from sdk.FnOsClient import get_mtime, get_signature
        headers = {
            "Referer": f"{base_url}/p/assets/upload.worker.js",
            "Trim-Overwrite": "0",
            "Trim-Token": client.token,
            "Trim-Mtim": str(get_mtime(local_path)),
            "Trim-Path": f"{folder}/{upload_name}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        }
        headers["Trim-Sign"] = get_signature(headers["Trim-Path"], client.sign_key)
        body, content_type = self._multipart(local_path)
        request = urllib.request.Request(f"{base_url}/upload", data=body, headers={
            **headers, "Content-Type": content_type})
        try:
            with urllib.request.urlopen(request, timeout=30) as resp:
                text = resp.read().decode("utf-8", "replace")
                status = resp.status
        except Exception as exc:                                   # pragma: no cover
            self.note(f"HTTP 上传失败：{type(exc).__name__}: {exc}")
            self.calls.append({"req": "file.upload(HTTP)", "status": "exception",
                               "error": str(exc)[:200], "params": {"path": nas_path},
                               "nested": False, "note": "POST /upload"})
            return None
        record = {"req": "file.upload(HTTP)", "params": {"path": nas_path, "size": size},
                  "nested": False, "note": "POST /upload（multipart）",
                  "status": "succ" if status in (200, 201) else "error",
                  "errno": None, "resp_keys": ["http"], "sample": text[:400],
                  "elapsed_ms": None}
        self.calls.append(record)
        print(f"  {'OK ' if record['status'] == 'succ' else '!! '}"
              f"file.upload(HTTP) POST /upload -> HTTP {status}")
        self.note(f"上传落地：{await self.wait_path(nas_path)}（{nas_path}，"
                  f"服务端文件名 uploadName={upload_name}）")
        return upload_name

    @staticmethod
    def _multipart(local_path):
        boundary = "----fnapitest" + str(int(time.time() * 1000))
        mime = mimetypes.guess_type(local_path)[0] or "application/octet-stream"
        with open(local_path, "rb") as f:
            data = f.read()
        name = os.path.basename(local_path)
        lines = [
            f"--{boundary}".encode(),
            f'Content-Disposition: form-data; name="trim-upload-file"; filename="{name}"'.encode(),
            f"Content-Type: {mime}".encode(),
            b"",
            data,
            f"--{boundary}--".encode(), b"",
        ]
        return b"\r\n".join(lines), f"multipart/form-data; boundary={boundary}"


async def main_async(args):
    client = FnOsClient(ping_interval=None)
    client.logger.setLevel(50)
    await client.connect(args.url)
    if not await client.login(args.username, args.password):
        print("登录失败，请检查用户名/密码")
        return 1

    prober = FileProber(client, args.path)
    # 服务端推送要收全：异步任务的最终结果、进度、收藏变更都在里面
    client.add_push_handler(None, lambda _c, payload: prober.on_push(payload))

    error = None
    try:
        result = await prober.run(keep=args.keep)
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        print(f"\n!! 中断：{error}")
        result = {}
    finally:
        await client.close()

    report = {
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "url": args.url, "username": args.username, "base": args.path,
        "result": result, "error": error, "notes": prober.notes,
        "pushes_count": len(prober.pushes),
        "pushes": prober.pushes[-60:],
        "calls": prober.calls,
    }
    out = os.path.join("data", "file_probe.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n完整调用日志 -> {out}（{len(prober.calls)} 次调用，"
          f"{len(prober.pushes)} 条推送）")

    if args.merge:
        note = ""
        if args.keep:
            note = f"⚠ 本次用 --keep 保留了临时目录 {result.get('scratch')}，请手工删除"
            print("\n" + note)
        merged, by_status = merge_probe_status(
            args.probe, prober.calls, source=FileProber.source,
            stamp_key="file_probe_at", note_key="file_probe_note", note=note)
        print(f"实测结论合并 -> {args.probe}（写入/更新 {merged} 条，按状态 {by_status}）")
        print("下一步：python tools/gen_api.py && python tools/gen_html.py "
              "&& python tools/verify_html.py")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="文件管理接口实测（只在自己的临时目录里做可逆操作）")
    parser.add_argument("--url", default=os.environ.get("FNNAS_WS", DEFAULT_URL))
    parser.add_argument("--username", default=os.environ.get("fn_username", "demo-user"))
    parser.add_argument("--password", default=os.environ.get("fn_password", ""))
    parser.add_argument("--path", default="/vol1/1000/tmp",
                        help="测试用的父目录，默认 /vol1/1000/tmp（只会新建/删除它下面的临时目录）")
    parser.add_argument("--probe", default="data/probe_status.json", help="实测结论文件")
    parser.add_argument("--no-merge", dest="merge", action="store_false", default=True)
    parser.add_argument("--keep", action="store_true", help="保留临时目录（默认测完删除）")
    parser.add_argument("--yes", action="store_true", help="确认执行（不加只打印计划）")
    args = parser.parse_args()

    if not args.path.startswith("/"):
        print("--path 必须是绝对路径，例如 /vol1/1000/tmp")
        return 2

    print("=" * 72)
    print("文件管理接口实测（file.*，全部在自己的临时目录里做可逆操作）")
    print(f"  NAS        : {args.url}")
    print(f"  父目录     : {args.path}（原文件只读，不会改动）")
    print(f"  临时目录   : {args.path.rstrip('/')}/{SCRATCH_PREFIX}<时间戳>/")
    print(f"  测完处理   : {'保留（--keep，需手工删除）' if args.keep else '删除并核对目录复原'}")
    print(f"  合并实测   : {args.probe if args.merge else '否'}")
    print("=" * 72)
    if not args.yes:
        print("这是 dry-run：上面就是将要执行的计划。确认无误后加 --yes 真正执行。")
        print("执行时会做：只读探测 → 建临时目录 → 上传 → 复制/改名/移动 →")
        print("            压缩/解压 → 权限原样写回 → 删到回收站（还原语义未确认）→ 清理并核对复原。")
        return 0
    print("开始执行 ...\n")
    return asyncio.run(main_async(args))


if __name__ == "__main__":
    sys.exit(main())
