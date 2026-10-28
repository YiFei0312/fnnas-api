#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
把 `.fpk` 安装到飞牛 NAS（走 App Center 的 HTTP API，等价于在应用中心里「手动安装」）。

流程（反编译 AppStore 前端 + 实测确认）：
    1. 上传 fpk 到 NAS 某个目录（HTTP /upload，带 Trim-* 签名头）
    2. POST /app-center/v1/download/task   {packageSourceType: "file", path: <NAS 路径>}
    3. POST /app-center/v1/download/status {downloadTaskId}        → 轮询到 Success
    4. GET/POST /app-center/v1/install/info {appName, version, packageType}
    5. POST /app-center/v1/install/task   {appName, version, packageType,
                                          systemParameters, customParameters}
    6. POST /app-center/v1/install/status {taskId}                → 轮询到成功
    7. POST /app-center/v1/start/start    {appName, ignoreDependencies: true}

鉴权：这些接口只认 cookie `fnos-token`（WebSocket 登录返回的 token），不需要 authx。

用法：
    python tools/install_nas_app.py --dump             # 只探测：上传 + 取包信息，不安装
    python tools/install_nas_app.py                    # 安装并启动
    python tools/install_nas_app.py --uninstall        # 卸载
    python tools/install_nas_app.py --status           # 查看是否已安装/运行
    python tools/install_nas_app.py --fpk dist/x.fpk --nas-path /vol1/1000/tmp/sample.fpk
"""

import argparse
import asyncio
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)


def log(msg):
    print("[install] %s" % msg, flush=True)


class AppCenter:
    def __init__(self, base_url, token):
        self.base = base_url.rstrip("/")
        self.token = token

    # ------------------------------------------------------------- HTTP
    def _request(self, method, path, body=None, params=None, timeout=60, raw=False):
        url = self.base + path
        if params:
            url += "?" + urllib.parse.urlencode(params)
        headers = {"Cookie": "fnos-token=" + self.token,
                   "User-Agent": "fnnas-mcp-installer/1.0"}
        data = None
        if body is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(body).encode()
        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as resp:
                payload = resp.read()
                status = resp.status
        except urllib.error.HTTPError as exc:
            payload = exc.read()
            status = exc.code
        text = payload.decode("utf-8", "replace")
        if raw:
            return status, text
        try:
            return status, json.loads(text)
        except Exception:
            raise RuntimeError("HTTP %s %s 返回非 JSON：%r" % (status, path, text[:200]))

    def get(self, path, params=None, timeout=60):
        return self._request("GET", path, params=params, timeout=timeout)[1]

    def post(self, path, body=None, timeout=60):
        return self._request("POST", path, body=body or {}, timeout=timeout)[1]

    def check(self, resp, what):
        if not isinstance(resp, dict):
            raise RuntimeError("%s 返回异常：%r" % (what, resp))
        # 有些接口（download/status）直接回数据、没有 {code,msg,data} 外壳
        if "code" not in resp:
            return resp
        if resp.get("code") != 0:
            raise RuntimeError("%s 失败：code=%s msg=%s"
                               % (what, resp.get("code"), resp.get("msg")))
        return resp.get("data")

    # ------------------------------------------------------------- 状态
    def installed_list(self):
        return self.check(self.get("/app-center/v1/app/installed"), "读取已安装列表")

    def find_installed(self, appname):
        data = self.installed_list() or {}
        for app in data.get("list") or []:
            if app.get("appName") == appname:
                return app
        return None

    def app_detail(self, appname):
        return self.check(self.get("/app-center/v1/app/detail",
                                   {"appName": appname}), "读取应用详情")


def read_manifest(fpk_path):
    """从 .fpk（tar）里读 manifest，拿到 appname / version / platform"""
    import tarfile
    data = {}
    with tarfile.open(fpk_path) as tar:
        for member in tar.getmembers():
            if member.name == "manifest":
                text = tar.extractfile(member).read().decode("utf-8", "replace")
                for line in text.splitlines():
                    if "=" in line:
                        key, _, value = line.partition("=")
                        data[key.strip()] = value.strip()
                break
    return data


# ---------------------------------------------------------------- 上传
def upload_file(client, local_path, nas_path):
    """checkUpload 拿 uploadName → multipart POST /upload（Trim-* 签名）

    注意：multipart 的字段名必须是 `trim-upload-file`（前端 upload.worker.js 就是这么发的），
    写成 `file` 服务端会直接 400。
    """
    from sdk.FnOsClient import get_mtime, get_signature

    size = os.path.getsize(local_path)
    # checkUpload 对「已存在」的文件只会返回一个带 .~#N 后缀的新名字，
    # 所以先把旧文件删掉，保证上传出来的就是我们想要的文件名
    def exists(path):
        prop = client.call_sync("file.prop", {"files": [path]})
        return (prop.get("prop") or [{}])[0].get("errno") is None

    if exists(nas_path):
        log("NAS 上已有同名文件，先删除：%s" % nas_path)
        client.call_sync("file.rm", {"files": [nas_path], "moveToTrashbin": False,
                                     "details": {"name": os.path.basename(nas_path),
                                                 "count": 1}})
        # file.rm 是异步任务：等它真的删掉，否则 checkUpload 会返回带 .~#N 的新名字
        for _ in range(20):
            if not exists(nas_path):
                break
            time.sleep(0.5)
        if exists(nas_path):
            log("!! 旧文件还在，上传可能落到 .~#N 名字上")
    client.call_sync("file.checkUpload", {"size": size, "path": nas_path, "overwrite": 1})
    # 关键：Trim-Path 用「目标文件名」。checkUpload 返回的 uploadName 在文件已存在时会带
    # .~#N 后缀，按它传反而会落成奇怪的名字、应用中心解析失败；实测直接用目标名可以覆盖。
    folder = nas_path.rsplit("/", 1)[0]
    target = nas_path
    base_url = client.base_url
    headers = {
        "Referer": base_url + "/p/assets/upload.worker.js",
        "Trim-Overwrite": "0",
        "Trim-Token": client.token,
        "Trim-Mtim": str(get_mtime(local_path)),
        "Trim-Path": target,
        "User-Agent": "Mozilla/5.0",
    }
    headers["Trim-Sign"] = get_signature(target, client.sign_key)

    boundary = "----fnnasmcp" + uuid.uuid4().hex
    with open(local_path, "rb") as f:
        content = f.read()
    body = b"\r\n".join([
        ("--%s" % boundary).encode(),
        ('Content-Disposition: form-data; name="trim-upload-file"; filename="%s"'
         % os.path.basename(target)).encode(),
        b"Content-Type: application/octet-stream",
        b"",
        content,
        ("--%s--" % boundary).encode(),
        b"",
    ])
    request = urllib.request.Request(
        base_url + "/upload", data=body,
        headers=dict(headers, **{"Content-Type":
                                 "multipart/form-data; boundary=%s" % boundary}))
    try:
        with urllib.request.urlopen(request, timeout=300) as resp:
            text = resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        raise RuntimeError("上传失败 HTTP %s：%s"
                           % (exc.code, exc.read()[:300].decode("utf-8", "replace")))
    log("上传完成：%s -> %s（响应 %s）" % (local_path, target, text[:120]))
    # 校验：按大小找实际落盘的文件（正常情况下就是 target；极端情况下服务端会给 .~#N）
    prop = client.call_sync("file.prop", {"files": [target]})
    remote_size = (prop.get("prop") or [{}])[0].get("size")
    if remote_size != size:
        folder = nas_path.rsplit("/", 1)[0]
        listing = client.call_sync("file.ls", {"path": folder}) or {}
        candidates = [e for e in (listing.get("files") or [])
                      if str(e.get("name", "")).startswith(os.path.basename(target))
                      and e.get("size") == size]
        if not candidates:
            raise RuntimeError("上传后找不到大小一致的文件：本地 %s 字节" % size)
        target = "%s/%s" % (folder, candidates[-1]["name"])
        log("上传落点校正为：%s" % target)
    log("大小校验通过：%s 字节" % size)
    return target



def provision_app_config(host, port, username, password, timeout=90):
    """装完后把 NAS 账号密码写进应用配置（调用应用自己的 /api/config）"""
    if not (username and password):
        return False
    base = "http://%s:%s" % (host, port)
    payload = json.dumps({"nas": {"host": "127.0.0.1", "port": 5666,
                                  "username": username, "password": password}}).encode()
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            request = urllib.request.Request(
                base + "/api/config", data=payload,
                headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(request, timeout=15) as resp:
                doc = json.loads(resp.read().decode("utf-8", "replace"))
            if doc.get("ok"):
                log("已把账号 %s 写入应用配置（应用会自动重连）" % username)
                # 等它连上
                for _ in range(30):
                    time.sleep(2)
                    with urllib.request.urlopen(base + "/api/status", timeout=10) as resp:
                        st = json.loads(resp.read().decode("utf-8", "replace"))
                    if st.get("connection", {}).get("connected"):
                        log("应用已连接飞牛：%s" % st["connection"].get("ws_url"))
                        return True
                log("账号已写入，但应用暂时还没连上（可稍后在界面点「测试连接」）")
                return True
        except Exception:
            time.sleep(3)
    log("!! 应用还没起来，账号密码没写入（稍后可在界面里填）")
    return False


# ---------------------------------------------------------------- 主流程
def run(args):
    from sdk import FnOsClient

    async def login():
        client = FnOsClient(ping_interval=60)
        client.logger.setLevel(50)
        await client.connect(args.ws)
        ok = await client.login(args.username, args.password)
        if not ok:
            raise RuntimeError("WebSocket 登录失败")
        return client

    if not (args.username and args.password):
        log("缺少登录 NAS 的账号密码：用 --username/--password 或环境变量 "
            "fn_username/fn_password 提供（安装应用需要管理员权限）")
        return 2

    log("登录 %s ..." % args.ws)
    # 全程只用一个事件循环：SDK 的 websocket 绑定在这个 loop 上，
    # 用 asyncio.run() 会把 loop 关掉，后续调用直接报 "Event loop is closed"
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def login():
        client = FnOsClient(ping_interval=60)
        client.logger.setLevel(50)
        await client.connect(args.ws)
        ok = await client.login(args.username, args.password)
        if not ok:
            raise RuntimeError("WebSocket 登录失败")
        return client

    client = loop.run_until_complete(login())

    def call_sync(req, params=None):
        return loop.run_until_complete(client.call(req, params or {}))

    client.call_sync = call_sync
    token = client.token
    base = "http://%s:%s" % (args.host, args.port)
    ac = AppCenter(base, token)

    # ---- 状态
    if args.status:
        app = ac.find_installed(args.appname)
        print(json.dumps(app, ensure_ascii=False, indent=2) if app else "未安装")
        return 0

    # ---- 只写配置（应用已装好，只是补账号密码）
    if args.provision_only:
        app = ac.find_installed(args.appname)
        if not app:
            log("还没安装 %s，先跑一次安装" % args.appname)
            return 1
        app_user = args.app_username or args.username
        app_pass = args.app_password or args.password
        if not (app_user and app_pass):
            log("请用 --app-username/--app-password 指定要写入应用的账号密码")
            return 1
        ok = provision_app_config(args.host, args.app_port or 8686, app_user, app_pass)
        return 0 if ok else 1

    # ---- 卸载
    if args.uninstall:
        app = ac.find_installed(args.appname)
        if not app:
            log("没有安装 %s" % args.appname)
            return 0
        info = ac.check(ac.get("/app-center/v1/uninstall/info",
                               {"appName": args.appname}), "读取卸载信息")
        print("卸载信息：", json.dumps(info, ensure_ascii=False)[:300])
        ac.post("/app-center/v1/stop/start", {"appName": args.appname})
        time.sleep(1)
        resp = ac.post("/app-center/v1/uninstall/start", {"appName": args.appname})
        log("卸载请求：%s" % json.dumps(resp, ensure_ascii=False)[:200])
        for _ in range(60):
            time.sleep(2)
            left = ac.find_installed(args.appname)
            if not left:
                log("已卸载")
                return 0
        log("警告：卸载后仍能在列表里看到")
        return 1

    # ---- 1) 上传 fpk
    fpk = os.path.abspath(args.fpk)
    if not os.path.exists(fpk):
        raise SystemExit("找不到 %s，先跑 python tools/build_nas_app.py" % fpk)
    if args.nas_path:
        nas_path = args.nas_path
    else:
        # 用唯一文件名：应用中心对「已存在」的文件会返回 xxx.~#N 这种新名字，
        # 上传完的文件名和预期不一致会让后面的解析/安装对不上，干脆每次换名
        stem, ext = os.path.splitext(os.path.basename(fpk))
        nas_path = "/vol1/1000/tmp/%s-%d%s" % (stem, int(time.time()), ext or ".fpk")
    log("fpk：%s（%.1f MB）" % (fpk, os.path.getsize(fpk) / 1024 / 1024))
    nas_path = upload_file(client, fpk, nas_path)

    # ---- 2/3) 让应用中心解析这个包，然后等 install/info 就绪
    #
    # 实测：download/status 对「新包」不可靠（任务 id 很快就查不到，偶尔报 status=3，
    # 但解析其实会成功）；真正能反映「包解析好了、可以装」的是 install/info 返回 code=0。
    # 所以这里以 install/info 为准，download 任务失败就重建，最多重试几次。
    local_manifest = read_manifest(fpk)
    app_name = args.appname or local_manifest.get("appname") or "fnnas-mcp"
    version = local_manifest.get("version") or "1.0.0"
    package_type = "path"
    log("本地 manifest：appname=%s version=%s" % (app_name, version))

    info_resp = {}
    for attempt in range(args.tries):
        resp = ac.post("/app-center/v1/download/task",
                       {"packageSourceType": "file", "path": nas_path})
        download_id = ((resp.get("data") or {}) or {}).get("downloadTaskId")
        log("download/task -> %s（第 %d 次）" % (download_id, attempt + 1))
        deadline = time.time() + args.wait_parse
        while time.time() < deadline:
            info_resp = ac.get("/app-center/v1/install/info",
                               {"appName": app_name, "version": version,
                                "packageType": package_type})
            if info_resp.get("code") == 0:
                break
            st = ac.get("/app-center/v1/download/status",
                        {"downloadTaskId": download_id})
            data = st.get("data") if isinstance(st, dict) else None
            state = (data or {}).get("status")
            if state == 3:
                log("   解析失败（status=3），重建下载任务重试")
                break
            time.sleep(2)
        if info_resp.get("code") == 0:
            break
        time.sleep(1)
    if info_resp.get("code") != 0:
        raise RuntimeError(
            "解析没成功（install/info code=%s）。如果 NAS 上有旧缓存，删掉 "
            "/vol1/appcenter-downloads/%s-*-tpk 再试；或者构建时升版本号。"
            % (info_resp.get("code"), app_name))

    # ---- 4) install/info（解析是异步的，这里轮询等它准备好）
    resp = {}
    for attempt in range(args.wait_parse):
        resp = ac.get("/app-center/v1/install/info",
                      {"appName": app_name, "version": version,
                       "packageType": package_type})
        if resp.get("code") == 0:
            break
        if attempt == 0 or attempt % 10 == 0:
            log("install/info 还没就绪（code=%s），等解析完成…" % resp.get("code"))
        time.sleep(1)
    log("install/info -> code=%s msg=%s" % (resp.get("code"), resp.get("msg")))
    if resp.get("code") != 0:
        raise RuntimeError(
            "install/info 拿不到包信息（code=%s）。应用中心按 appName 缓存解析结果，"
            "如果版本号没变但内容变了，缓存里还是旧内容；删掉 NAS 上的 "
            "/vol1/appcenter-downloads/%s-*-tpk 后再试，或者构建时升版本号。"
            % (resp.get("code"), app_name))
    install_info = resp.get("data") or {}
    if args.verbose or args.dump:
        print(json.dumps(install_info, ensure_ascii=False)[:1500])
    if install_info.get("taskId"):
        log("已有安装任务在进行：%s" % install_info["taskId"])
        task_id = install_info["taskId"]
    else:
        # ---- 5) install/task
        # 前端实际传的字段（AppStore 里 install.start 调用点）：
        #   {agreedToProtocol, installVolumeID, dataVolumeId, immediateStart, apiScope}
        wizard = install_info.get("wizardInfo") or {}
        root_install = wizard.get("installType") == "root"
        volume_id = args.volume_id
        if volume_id is None:
            syscfg = ac.check(ac.get("/app-center/v1/sysconfig"), "读取应用中心设置") or {}
            volume_id = syscfg.get("downloadAndInstallVolumeID") or syscfg.get("volumeID") or 1
        # 实测：systemParameters 必须同时给 installVolumeID 和 dataVolumeId，
        # 只给 installVolumeID 会失败（异步任务报 code 10208 ErrCodeVolumeIDException）；
        # 加 agreedToProtocol / apiScope / immediateStart 反而会让接口 500，别乱加。
        system_params = {
            "installVolumeID": 0 if root_install else int(volume_id),
            "dataVolumeId": int(volume_id),
        }
        resp = ac.post("/app-center/v1/install/task", {
            "appName": app_name,
            "version": version,
            "packageType": package_type,
            "systemParameters": system_params,
            # 不要传 customParameters：实测传了（哪怕是 {}）会让接口 HTTP 500 / code 10000
        })
        log("install/task -> %s" % json.dumps(resp, ensure_ascii=False)[:300])
        data = ac.check(resp, "创建安装任务")
        task_id = data.get("taskId")
    log("安装 taskId = %s" % task_id)

    # ---- 6) 轮询 install/status
    ok = False
    for i in range(300):
        doc = ac.post("/app-center/v1/install/status", {"taskId": task_id})
        if isinstance(doc, dict) and "status" not in doc and doc.get("code") not in (0, None):
            time.sleep(2)
            continue
        st = ac.check(doc, "安装状态")
        state = st.get("status")
        progress = st.get("progress")
        if args.verbose or i % 5 == 0:
            print("   安装中 status=%s progress=%s %s"
                  % (state, progress, (st.get("outputText") or "")[:80]))
        if state == 2:
            ok = True
            break
        if state in (3, 4):
            raise RuntimeError("安装失败：%s" % json.dumps(st, ensure_ascii=False)[:800])
        time.sleep(2)
    if not ok:
        raise RuntimeError("等安装完成超时")

    # ---- 7) 启动
    if args.start:
        resp = ac.post("/app-center/v1/start/start",
                       {"appName": app_name, "ignoreDependencies": True})
        log("start/start -> %s" % json.dumps(resp, ensure_ascii=False)[:300])
        time.sleep(3)

    # 可选：把账号密码写进应用配置（这样安装完就能直接用）
    if args.provision and not args.no_provision:
        app_port = args.app_port or int(local_manifest.get("service_port") or 8686)
        provision_app_config(args.host, app_port,
                            args.app_username or args.username,
                            args.app_password or args.password)

    app = ac.find_installed(app_name)
    log("安装完成：%s" % json.dumps(
        {k: (app or {}).get(k) for k in ("appName", "name", "version", "status")},
        ensure_ascii=False))
    print(json.dumps(app, ensure_ascii=False, indent=2)[:2000])
    return 0


def main():
    parser = argparse.ArgumentParser(description="安装 fpk 到飞牛 NAS")
    parser.add_argument("--fpk", default=os.path.join(ROOT, "dist", "fnnas-mcp-1.0.0.fpk"))
    parser.add_argument("--nas-path", default=None,
                        help="上传到 NAS 的路径，默认 /vol1/1000/tmp/<文件名>")
    parser.add_argument("--host", default="192.168.1.10")
    parser.add_argument("--port", default=5666)
    parser.add_argument("--ws", default="ws://192.168.1.10:5666/websocket?type=main")
    parser.add_argument("--username", default=os.environ.get("fn_username", ""),
                        help="登录 NAS 用的管理员账号（装应用需要，默认读 fn_username）")
    parser.add_argument("--password", default=os.environ.get("fn_password", ""),
                        help="登录 NAS 用的管理员密码（默认读 fn_password）")
    parser.add_argument("--provision", action="store_true",
                        help="安装后把账号密码写进应用配置（让应用装完即用）")
    parser.add_argument("--app-username", default="",
                        help="写进应用的账号（默认同 --username）")
    parser.add_argument("--app-password", default="",
                        help="写进应用的密码（默认同 --password）")
    parser.add_argument("--appname", default="fnnas-mcp")
    parser.add_argument("--tries", type=int, default=3, help="解析失败时重试次数")
    parser.add_argument("--wait-parse", type=int, default=60,
                        help="等应用中心解析完包的秒数")
    parser.add_argument("--volume-id", type=int, default=None,
                        help="装到哪个存储卷（默认用应用中心的默认卷）")
    parser.add_argument("--dump", action="store_true", help="只探测包信息，不安装")
    parser.add_argument("--status", action="store_true", help="查看安装状态")
    parser.add_argument("--uninstall", action="store_true", help="卸载")
    parser.add_argument("--no-start", dest="start", action="store_false", default=True,
                        help="安装后不自动启动")
    parser.add_argument("--app-port", type=int, default=None,
                        help="应用服务端口（默认读 manifest 的 service_port，没有则 8686）")
    parser.add_argument("--provision-only", action="store_true",
                        help="不安装，只把 --username/--password 写进已装应用的配置")
    parser.add_argument("--no-provision", action="store_true",
                        help="安装后不自动把账号密码写入应用配置")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
