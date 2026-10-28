# -*- coding: utf-8 -*-
"""
常用接口的「手写」封装层。

和 `client.api.xxx`（自动生成、覆盖全部接口）的分工：

    client.api.*        全量接口，字段名原样返回，适合探索和临时调用
    本文件的 mixin 方法  高频只读接口，带参数名、自动解包、出错抛异常，适合业务里直接用

所有方法都遵循同一约定：
    - 成功：返回业务数据（自动剥掉 data / rsp 外层），失败：抛 BadRequestError
    - 需要登录：是（内部会带签名，登录由 client.login 完成）
    - 全部实测通过（见 docs/api/README.md 的状态列）

新增方法的判断标准：只加「一眼就能看懂参数」的接口，
参数含义不明的留给 client.api.*，避免瞎猜参数名。
"""

from ..exceptions import BadRequestError


def unwrap(resp):
    """剥掉 fnOS 响应外层：{data:{...}} / {rsp:{...}} / 平铺对象"""
    if not isinstance(resp, dict):
        return resp
    for key in ("data", "rsp"):
        if key in resp and isinstance(resp[key], dict):
            return resp[key]
    return resp


def check(resp):
    """失败时抛 BadRequestError，成功返回原响应"""
    if isinstance(resp, dict) and resp.get("result") == "fail":
        raise BadRequestError(resp.get("errno"), resp)
    return resp


def data_of(resp):
    """check + unwrap 的合体，最常用"""
    return unwrap(check(resp))


class SystemApiMixin:
    """系统信息 / 运行状态 / 网络 等只读接口"""

    # ---------- 系统信息 appcgi.sysinfo ----------
    async def sysinfo_hostname(self):
        """主机名（同时返回是否已建用户、系统版本）"""
        return data_of(await self.request("appcgi.sysinfo.getHostName"))

    async def sysinfo_version(self):
        """系统版本"""
        return data_of(await self.request("appcgi.sysinfo.getTrimVersion"))

    async def sysinfo_machine_id(self):
        """设备 ID"""
        return data_of(await self.request("appcgi.sysinfo.getMachineId"))

    async def sysinfo_hardware(self):
        """硬件信息（CPU / 内存 / 主板 / BIOS / 系统盘）"""
        return data_of(await self.request("appcgi.sysinfo.getHardwareInfo"))

    async def sysinfo_uptime(self):
        """开机时长"""
        return data_of(await self.request("appcgi.sysinfo.getUptime"))

    async def sysinfo_time(self):
        """时间设置（时区、NTP 等）"""
        return data_of(await self.request("appcgi.sysinfo.getTimeSetting"))

    async def sysinfo_timezones(self):
        """可选的时区列表"""
        return data_of(await self.request("appcgi.sysinfo.getTimezoneList"))

    async def sysinfo_fan_mode(self):
        """风扇模式"""
        return data_of(await self.request("appcgi.sysinfo.getFanMode"))

    async def sysinfo_is_trim_machine(self):
        """本机是否为飞牛整机"""
        return data_of(await self.request("appcgi.sysinfo.isTrimMachine"))

    async def sysinfo_machine_type(self):
        """整机型号"""
        return data_of(await self.request("appcgi.sysinfo.getTrimMachineType"))

    async def sysinfo_power_plans(self):
        """电源计划列表"""
        return data_of(await self.request("appcgi.sysinfo.listPowerPlan"))

    async def sysinfo_power_plan_status(self):
        """电源计划当前状态"""
        return data_of(await self.request("appcgi.sysinfo.getPowerPlanStatus"))

    # ---------- 资源监控 appcgi.resmon ----------
    async def resmon_cpu(self):
        """CPU 使用率 / 负载"""
        return data_of(await self.request("appcgi.resmon.cpu"))

    async def resmon_mem(self):
        """内存使用情况"""
        return data_of(await self.request("appcgi.resmon.mem"))

    async def resmon_disk(self):
        """磁盘 IO"""
        return data_of(await self.request("appcgi.resmon.disk"))

    async def resmon_net(self):
        """网络吞吐"""
        return data_of(await self.request("appcgi.resmon.net"))

    async def resmon_gpu(self):
        """GPU 状态（无 GPU 时返回空）"""
        return data_of(await self.request("appcgi.resmon.gpu"))

    async def resmon_npu(self):
        """NPU 状态（无 NPU 时返回空）"""
        return data_of(await self.request("appcgi.resmon.npu"))

    async def resmon_processes(self):
        """进程列表"""
        return data_of(await self.request("appcgi.resmon.proc.list"))

    async def resmon_fan(self):
        """风扇转速"""
        return data_of(await self.request("appcgi.resmon.sysFan"))

    # ---------- 网络 appcgi.network ----------
    async def network_interfaces(self):
        """网卡列表（含 IP / 速率 / 状态）"""
        return data_of(await self.request("appcgi.network.net.list"))

    async def network_gateway(self):
        """网关配置（端口 / 强制 https 等）"""
        return data_of(await self.request("appcgi.network.gw.getting"))

    async def network_ssh_status(self):
        """SSH 开关状态"""
        return data_of(await self.request("appcgi.network.ssh.status"))

    async def network_multi_gateway_status(self):
        """多网关状态"""
        return data_of(await self.request("appcgi.network.net.getMultiGWStatus"))

    async def network_nic_performance_mode(self):
        """网卡性能模式"""
        return data_of(await self.request("appcgi.network.net.getNicPerformanceMode"))

    # ---------- 通知 ----------
    async def notify_list(self, page=1, page_size=20):
        """通知列表（返回 page/pageTotal/total 与列表）"""
        return data_of(await self.request("notify.list", page=page, pageSize=page_size))

    async def notify_unread_total(self):
        """未读通知数"""
        return unwrap(check(await self.request("notify.unreadTotal")))

    # ---------- 用户 ----------
    async def user_list_all(self):
        """用户列表"""
        return data_of(await self.request("user.list"))

    async def user_login_devices(self):
        """当前账号的登录设备"""
        return data_of(await self.request("user.listLoginDevice"))

    async def user_is_admin(self):
        """当前账号是否管理员"""
        return unwrap(check(await self.request("user.isAdmin")))

    # ---------- 分享协议配置 ----------
    async def share_options(self, protocol="smb"):
        """
        读取共享协议配置（只读，.opt 结尾的接口）
        :param protocol: smb / nfs / ftp / webdav / dlna
        """
        req = f"appcgi.share.{protocol}.opt"
        return data_of(await self.request(req))


class StorageApiMixin:
    """存储相关只读接口（stor.*）"""

    async def storage_disks(self):
        """硬盘列表"""
        return unwrap(check(await self.request("stor.listDisk")))

    async def storage_volumes(self):
        """存储空间列表"""
        return unwrap(check(await self.request("stor.listStor")))

    async def storage_free_disks(self):
        """可用（未使用）硬盘"""
        return unwrap(check(await self.request("stor.listFreeDisk")))

    async def storage_calc_space(self):
        """容量汇总（系统/存储 总量与可用量、HDD/SSD/USB 数量）"""
        return unwrap(check(await self.request("stor.calcSpace")))

    async def storage_general(self):
        """存储总览（array / block）"""
        return unwrap(check(await self.request("stor.general")))

    async def storage_state(self):
        """存储状态"""
        return unwrap(check(await self.request("stor.state2")))

    async def storage_sys_partition(self):
        """系统分区使用情况"""
        return unwrap(check(await self.request("stor.getSysPartInfo")))

    async def storage_removable(self):
        """可移动设备列表"""
        return unwrap(check(await self.request("stor.listRemovable")))

    async def storage_cache_devs(self):
        """缓存设备列表"""
        return unwrap(check(await self.request("stor.listCachedev")))

    async def storage_user_quota(self, quota_info=True, space_info=True, stor_info=True):
        """用户存储与配额（等价于 get_user_storage）"""
        return unwrap(check(await self.request(
            "stor.getUserStorage", quotaInfo=quota_info, spaceInfo=space_info,
            storInfo=stor_info)))


class FileOpsApiMixin:
    """
    文件常用操作（`file.*`）。

    参数全部按**真机实测**修正过（复现脚本：`python tools/probe_file.py --yes`，
    结论见 `data/file_probe.json` 与 [docs/modules/file.md]）：

    - 批量查询类接口的参数是 **`files` 数组**（不是 `path`）：`file.prop` / `file.access`
      / `file.calc`；`file.size` 反而是单个 `file`；
    - 复制/移动的参数是 `{files, pathTo, overwrite}`，**`pathTo` 是目标目录**；
    - 写操作是**异步任务**：接口只回 `{sysNotify:"taskId", taskId}`，成败要看同 `reqid`
      的推送（`{"result":"succ"|"fail", failedFiles:[{file,errno}]}`）——
      这一层由 `sdk/filetasks.py` 的 `wait_file_task()` 负责等结果；
    - 常见业务错误：`4100` = 路径不存在（`file.prop` 里是条目级 errno，不是接口级）。
    """

    # ------------------------------------------------------------ 只读
    async def file_prop(self, *paths, path=None):
        """批量取属性（返回 prop 数组；不存在的路径元素里带 errno=4100）"""
        files = list(paths) or ([path] if path else [])
        return unwrap(check(await self.request("file.prop", files=files))).get("prop", [])

    async def file_size(self, path):
        """单个路径的占用大小（返回 {size, space}）"""
        return unwrap(check(await self.request("file.size", file=path)))

    async def file_calc(self, *paths, path=None, timeout=-1):
        """统计文件数/目录数/占用（返回 fileCount / dirCount / fileSizeTotal / space）"""
        files = list(paths) or ([path] if path else [])
        return unwrap(check(await self.request("file.calc", files=files, timeout=timeout)))

    async def file_acl(self, path, get_prop=False):
        """读取 ACL（返回 permset / defaultPermset）"""
        return unwrap(check(await self.request("file.getAcl", path=path, getProp=get_prop)))

    async def file_access(self, *paths, path=None):
        """权限位（返回 access 数组，access[0] & 6 非 0 即可读写）"""
        files = list(paths) or ([path] if path else [])
        return unwrap(check(await self.request("file.access", files=files))).get("access", [])

    async def file_download(self, *paths):
        """取下载地址（返回 download[].uri，是带签名的 HTTP 地址）"""
        return unwrap(check(await self.request("file.download",
                                               files=list(paths)))).get("download", [])

    async def file_favorites(self):
        """收藏夹列表"""
        return unwrap(check(await self.request("file.fav.list"))).get("fav", [])

    async def file_recent(self):
        """最近访问列表（响应键是 `recent`，不是 files）"""
        return unwrap(check(await self.request("file.recent.list"))).get("recent", [])

    async def file_trash(self, uid=None):
        """回收站顶层条目（字段 rmUid / rmTime）"""
        return unwrap(check(await self.request("file.trash.list", uid=uid))).get("files", [])

    async def file_shares(self):
        """已分享文件列表（旧接口 file.share.list）"""
        return unwrap(check(await self.request("file.share.list")))

    # ------------------------------------------------------------ 写操作
    async def file_mkdir(self, path):
        """新建文件夹（写操作；path 用绝对路径，含新目录名）"""
        return unwrap(check(await self.request("file.mkdir", path=path)))

    async def file_rm(self, files, move_to_trashbin=True, details=None):
        """
        删除文件/文件夹（写操作，异步任务）
        :param files: 绝对路径列表
        :param move_to_trashbin: True 进回收站，False 直接删
        """
        if isinstance(files, str):
            files = [files]
        return unwrap(check(await self.request(
            "file.rm", files=list(files), moveToTrashbin=move_to_trashbin,
            details=details or {})))

    async def file_cp(self, files, path_to, overwrite=1, details=None):
        """复制到目录 path_to（写操作，异步任务；同名保持原文件名）"""
        if isinstance(files, str):
            files = [files]
        return unwrap(check(await self.request(
            "file.cp", files=list(files), pathTo=path_to, overwrite=overwrite,
            details=details or {})))

    async def file_mv(self, files, path_to, overwrite=1, details=None):
        """移动到目录 path_to（写操作，异步任务）"""
        if isinstance(files, str):
            files = [files]
        return unwrap(check(await self.request(
            "file.mv", files=list(files), pathTo=path_to, overwrite=overwrite,
            details=details or {})))

    async def file_rename(self, path, new_name):
        """重命名（写操作，同步接口，失败直接返回 errno）"""
        return unwrap(check(await self.request("file.rename", path=path, newName=new_name)))

    async def file_fav_add(self, path):
        """添加收藏（写操作）"""
        return unwrap(check(await self.request("file.fav.add", path=path)))

    async def file_fav_del(self, path):
        """取消收藏（写操作，一次一个路径）"""
        return unwrap(check(await self.request("file.fav.del", path=path)))

    async def file_recent_add(self, path):
        """记入最近访问（写操作）"""
        return unwrap(check(await self.request("file.recent.add", path=path)))

    async def file_recent_del(self, *paths):
        """从最近访问里移除（写操作；注意参数是数组）"""
        return unwrap(check(await self.request("file.recent.del", path=list(paths))))

    async def file_recent_clear(self):
        """清空最近访问（写操作）"""
        return unwrap(check(await self.request("file.recent.clear")))

    async def file_compress(self, files, path, description="", level=0, passwd=None,
                            details=None):
        """
        压缩（写操作，异步任务）
        :param files: 要压缩的绝对路径列表
        :param path: 输出压缩包路径（含文件名）
        """
        if isinstance(files, str):
            files = [files]
        params = {"description": description, "path": path, "files": list(files),
                  "level": level, "details": details or {}}
        if passwd:
            params["passwd"] = passwd
        return unwrap(check(await self.request("file.compress", **params)))

    async def file_extract(self, file, path, description="", overwrite=1, details=None):
        """
        解压（写操作，异步任务）
        :param file: 压缩包路径
        :param path: 输出目录
        :param overwrite: 同名处理，1=覆盖
        注意：**不要传空的 fromCharset**，服务端会报 `Too short switch: -fromcharset`。
        """
        return unwrap(check(await self.request(
            "file.extract", description=description, path=path, file=file,
            overwrite=overwrite, details=details or {})))

    async def file_set_acl(self, files, permset, sub=False, details=None):
        """
        设置 ACL（写操作，异步任务；`file.setAcl` 接口不存在，走 setAcl2）
        :param permset: 先用 file_acl(path) 读出来，改完再写回
        """
        if isinstance(files, str):
            files = [files]
        return unwrap(check(await self.request(
            "file.setAcl2", files=list(files), permset=permset,
            details=details or {}, sub=1 if sub else 0)))

    async def file_chown(self, files, uid, gid):
        """改属主（写操作，异步任务；参数是 files 数组）"""
        if isinstance(files, str):
            files = [files]
        return unwrap(check(await self.request(
            "file.chown", files=list(files), uid=uid, gid=gid)))

    async def file_check_upload(self, size, path, overwrite=None):
        """上传前置检查（返回 uploadName 等；overwrite: 0 跳过 / 1 覆盖 / 2 保留两者）"""
        params = {"size": size, "path": path}
        if overwrite is not None:
            params["overwrite"] = overwrite
        return unwrap(check(await self.request("file.checkUpload", **params)))

    async def file_cancel(self, task_id):
        """取消进行中的任务（⚠ 参数形态未确认：实测 taskId/taskIds/id 都报 8192）"""
        return unwrap(check(await self.request("file.cancel", taskId=task_id)))

    async def file_restore_from_trash(self, paths, details=None, overwrite=1):
        """
        从回收站还原（写操作，异步任务）
        ⚠ 实测：接口和任务都回 `succ`，但传原路径**并没有真的还原**，
        `files` 应该传的路径形态没确认下来（`file.trash.list` 不暴露它），别依赖。
        """
        if isinstance(paths, str):
            paths = [paths]
        return unwrap(check(await self.request(
            "file.trash.restore", files=list(paths), overwrite=overwrite,
            details=details or {})))

    # 说明：搜索接口用已有的 FileClient.file_search(key, path)，这里不重复封装。


class ShareApiMixin:
    """
    分享链接（公开链接分享）—— `appcgi.sharesvr.share.link.*` 系列。

    和 `file.share.*` 的区别：`file.share.*` 是「分享给其它 NAS 用户」的旧接口，
    当前版本的 Web UI 已经改用本 mixin 封装的分享链接（生成一个 /s/<id> 网址给别人看）。

    实测踩坑（重要）：
        这一族接口的参数必须包在 `data` 里发，平铺会返回 errno 3000001 Invalid Params；
        而且 `id` 必须是字符串。本 mixin 已经处理好，直接用即可。

        d = await client.share_link_create('/vol1/1000/tmp/a.jpg', passwd='1234')
        print(client.share_url(d['id']))        # http://<nas>:5666/s/xxxx

    完整实测记录见 docs/modules/share.md。
    """

    #: 列表接口返回里 list 为 None 时代表「一条分享都没有」
    DEFAULT_SORT = ("createdTime", "DESC")

    async def share_link_default(self):
        """分享链接的默认配置（域名模式 / 自定义域名 / 限速 / fnDefault 前缀）"""
        return data_of(await self.call("appcgi.sharesvr.share.link.default.get"))

    async def share_permission(self):
        """谁能创建分享链接：{"mode": "all"} / {"mode": "admin"} 等"""
        return data_of(await self.call("appcgi.sharesvr.share.permission.get"))

    async def share_permission_set(self, mode):
        """设置谁能创建分享链接（写操作）；mode 取值同 share_permission() 返回"""
        return data_of(await self.call("appcgi.sharesvr.share.permission.set",
                                       {"mode": mode}, nested=True))

    async def share_upload_permission(self):
        """分享链接里谁可以上传：{"mode": "admin"} 等"""
        return data_of(await self.call("appcgi.sharesvr.share.uploadpermission.get"))

    async def share_upload_permission_set(self, mode):
        """设置分享上传权限（写操作）"""
        return data_of(await self.call("appcgi.sharesvr.share.uploadpermission.set",
                                       {"mode": mode}, nested=True))

    async def share_links(self, page=1, page_size=100, keyword="", is_admin=False,
                          share_type=0, sort_column=None, sort_type=None):
        """
        分享链接列表（实测通过）

        :param page_size: 每页条数
        :param keyword: 按名称搜索；支持直接粘贴分享地址（服务端会解析出 id）
        :param is_admin: True 看全部用户的分享（管理员）
        :param share_type: 0 = 全部；1 = 分享链接；4 = 文件收集（上传请求）
        :return: {"total": n, "list": [...]}；没有分享时 list 是 [] 而不是 None
        """
        sc, st = self.DEFAULT_SORT
        data = data_of(await self.call("appcgi.sharesvr.share.link.list", {
            "page": page, "pageSize": page_size, "keyword": keyword,
            "isAdmin": bool(is_admin), "type": share_type,
            "sortColumn": sort_column or sc, "sortType": sort_type or st}, nested=True))
        if isinstance(data, dict) and data.get("list") is None:
            data = dict(data, list=[])
        return data

    async def share_link(self, share_id):
        """
        单条分享详情（实测通过）—— 比列表多一个 files 字段：
            files: [{"path": "/vol1/1000/tmp", "file": "a.jpg", "isDir": 0}]
        path 是所在目录，file 是文件/目录名。
        """
        return data_of(await self.call("appcgi.sharesvr.share.link.get",
                                       {"id": str(share_id)}, nested=True))

    async def share_link_create(self, files, name=None, max_access=0, passwd=None,
                                valid_to=None, extra=None):
        """
        创建分享链接（写操作，实测通过）

        :param files: 路径或路径列表，如 '/vol1/1000/tmp/20260127_195353.jpg'
        :param name: 分享名称，默认取第一个文件的文件名
        :param max_access: 可访问次数，0 = 不限
        :param passwd: 提取码，None = 不设（响应里是明文返回的，注意别外泄日志）
        :param valid_to: 失效时间（秒级时间戳），None/0 = 永久有效
        :param extra: 额外字段（type / uploadConfig 等，做文件收集时用）
        :return: 分享详情 dict，含 id / name / type / status / createdTime(毫秒) / validTo(秒)
                 分享地址用 client.share_url(data['id']) 拼。
        """
        files = [files] if isinstance(files, str) else list(files)
        params = {
            "name": name or files[0].rstrip("/").split("/")[-1],
            "files": files,
            "maxAccess": max_access,
        }
        if passwd:
            params["passwd"] = passwd
        if valid_to:
            params["validTo"] = int(valid_to)
        if extra:
            params.update(extra)
        return data_of(await self.call("appcgi.sharesvr.share.link.create",
                                       params, nested=True))

    async def share_link_update(self, share_id, name=None, max_access=None,
                                passwd=None, valid_to=None, extra=None):
        """
        修改分享链接（写操作，实测通过）；只提交传进来的字段。

        :param valid_to: 秒级时间戳，0 = 改成永久有效
        """
        params = {"id": str(share_id)}
        if name is not None:
            params["name"] = name
        if max_access is not None:
            params["maxAccess"] = max_access
        if passwd is not None:
            params["passwd"] = passwd
        if valid_to is not None:
            params["validTo"] = int(valid_to)
        if extra:
            params.update(extra)
        return data_of(await self.call("appcgi.sharesvr.share.link.update",
                                       params, nested=True))

    async def share_link_remove(self, *share_ids):
        """
        删除一个或多个分享（写操作，实测通过）

        :return: {"failedCount": 0, "failedIdList": []}
        """
        return await self.share_link_remove_ids(share_ids)

    async def share_link_remove_ids(self, share_ids):
        """删除分享（写操作），参数是 id 的可迭代对象"""
        ids = [str(i) for i in share_ids]
        return data_of(await self.call("appcgi.sharesvr.share.link.remove",
                                       {"idList": ids}, nested=True))

    async def share_link_clear(self, is_admin=False):
        """清空分享链接（写操作）；:return: {"clear": 删除条数}"""
        return data_of(await self.call("appcgi.sharesvr.share.link.clear",
                                       {"isAdmin": bool(is_admin)}, nested=True))

    async def share_link_count(self, is_admin=False):
        """当前分享条数（列表 total 的快捷方式）"""
        return (await self.share_links(page=1, page_size=1, is_admin=is_admin))["total"]

    def share_url(self, share_id, base=None):
        """
        拼出分享地址：http://<nas>:5666/s/<id>（实测 HTTP 200，页面标题就是分享名称）

        :param base: 服务端返回的 fnDefault（share_link_default()['fnDefault']）或自定义域名
        """
        base = (base or getattr(self, "base_url", None) or "").rstrip("/")
        if not base:
            raise BadRequestError(None, {"errmsg": "还没 connect 或无 base_url，请显式传 base"})
        return f"{base}/s/{share_id}"
