# -*- coding: utf-8 -*-
"""
接口安全分级：区分「只读接口」和「会改动 NAS 的写接口」。

为什么单独一个模块：
    tools/probe.py（实测哪些接口能用）和 tools/gen_api.py（生成封装）
    都必须用**同一套**判定，否则容易出现「生成时不算写接口、探测时却真去调」
    这种危险偏差。所以判定逻辑只写一份，两边都 import 它。

判定规则（保守优先）：
    1. 命中 EXTRA_ALLOW 人工白名单 -> 只读
    2. 方法名（最后一段）以 DENY_PREFIX 里的动词开头 -> 写接口（先判 deny）
    3. 方法名以 ALLOW_PREFIX 里的动词开头 -> 只读
    4. 以 .opt 结尾（读配置）-> 只读
    5. 其余一律当写接口处理
"""

# 只读动词：接口最后一段以这些开头才认为安全
ALLOW_PREFIX = (
    "get", "list", "ls", "query", "check", "status", "state", "info", "search",
    "calc", "prop", "size", "usage", "access", "general", "detail", "summary",
    "count", "stat", "read", "fetch", "show", "view", "is", "has", "find_",
)
# 危险动词：命中即视为写接口
DENY_PREFIX = (
    "set", "add", "del", "remove", "rm", "create", "make", "update", "mod", "edit",
    "start", "stop", "restart", "reboot", "enable", "disable", "format", "mount",
    "umount", "unmount", "eject", "reset", "clear", "active", "switch", "open",
    "close", "connect", "disconnect", "run", "cancel", "copy", "cp", "mv", "move",
    "rename", "chown", "import", "export", "restore", "recover", "apply", "bind",
    "revoke", "kick", "freeze", "unfreeze", "install", "uninstall", "upgrade",
    "sync", "send", "change", "write", "upload", "download", "exec", "signal",
    "kill", "scrub", "do", "test", "trial", "verify", "login", "logout", "auth",
    "token", "init", "mute", "record", "save", "put", "post", "patch", "replace",
    "swap", "migrate", "backup", "detect", "disc", "arping", "trim", "z",
)
# 人工确认过的只读接口（不满足前缀规则，但确认只查不改）
EXTRA_ALLOW = {
    "stor.diskSmart", "stor.diskHealth", "stor.general", "stor.state", "stor.state2",
    "stor.calcSpace", "appcgi.resmon.cpu", "appcgi.resmon.mem", "appcgi.resmon.disk",
    "appcgi.resmon.net", "appcgi.resmon.gpu", "appcgi.resmon.npu", "appcgi.resmon.battery",
    "appcgi.resmon.sysFan", "appcgi.resmon.gen", "appcgi.resmon.proc.list",
    "appcgi.resmon.proc.srv", "appcgi.resmon.alert.getBeepEvents",
    "appcgi.resmon.alert.getBeepReasons", "appcgi.resmon.alert.getSupportedBeepEvents",
    "appcgi.mountmgr.mountInfo", "appcgi.mountmgr.shares", "appcgi.mountmgr.list",
    "appcgi.mountmgr.check", "icenter.gen", "icenter.net", "icenter.svc",
    "notify.unreadTotal", "log.graph", "log.list", "usrdat.get", "usrdat.getArray",
    "usrdat.getArrayUpdateTime", "usrdat.isArrayValueExists", "app.list", "app.info",
    "app.status", "app.listvolume", "app.getdefinstvolume", "app.geticon",
    "user.groupUsers", "user.isAdmin", "user.active", "liveupdate.status",
    "liveupdate.check", "file.usage", "file.size", "file.userShareFilesAugmented",
    "appcgi.screen.isSleeping", "appcgi.share.team.allowShare",
    "appcgi.sac.entry.v1.appStoreList", "appcgi.sac.entry.v1.dockerList",
    "appcgi.sac.entry.v1.getUserDesktop", "appcgi.sac.entry.v1.getEntryList",
    "appcgi.sac.desktop.v1.getConfig", "appcgi.sac.i18n.v1.config.get",
    "appcgi.netsvr.fnassistant.info", "appcgi.netsvr.network.list",
    "appcgi.license.soft.trial.applystatus", "appcgi.license.soft.get",
    "appcgi.license.soft.list", "appcgi.license.soft.ipc.get",
    "handlerFn.fileCollection.result.password",
}


def is_readonly(req: str) -> bool:
    """接口是否只读（可以安全自动调用）"""
    if req in EXTRA_ALLOW:
        return True
    last = req.split(".")[-1].lower()
    if any(last.startswith(p) for p in DENY_PREFIX):
        return False
    if any(last.startswith(p) for p in ALLOW_PREFIX):
        return True
    if req.endswith(".opt"):          # xxx.opt 都是读配置
        return True
    return False
