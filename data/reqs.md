# fnOS 接口清单（自动生成）

> 来源：`http://192.168.1.10:5666` 前端产物静态提取  
> 生成时间：2026-10-16 21:56:25，耗时 1.2s  
> js 产物 128 个 / 入口页 4 个，共提取 `3849` 个候选名称  
> **本文件自动生成，不要手工编辑**，重新运行 `python tools/scan_web.py` 即可。

## 分档说明

来源标记：`direct`=前端真实调用点，`alias`=接口映射表（键名就是官方别名），
`assign`=事件枚举常量，`alias_key`/`loose`=长得像接口的其它字符串。

| 分档 | 含义 | 数量 |
| --- | --- | --- |
| `endpoint` | 来自前端接口映射表或真实调用点，**基本可确认是服务端接口** | 514 |
| `event` | 常量/枚举里的推送事件名 | 56 |
| `unverified` | 其它同形字符串，多数是 i18n 文案键，需实测确认 | 3279 |

## 分组统计

| 分组 | 接口数 |
| --- | --- |
| `handlerFn` | 243 |
| `settingAI` | 132 |
| `domains` | 126 |
| `fileSharingProtocol` | 90 |
| `file` | 86 |
| `taskbar` | 86 |
| `taskPanel` | 82 |
| `storageManagement` | 73 |
| `stor` | 66 |
| `taskCreatorDialog` | 64 |
| `shareLink` | 63 |
| `fileDetails` | 62 |
| `errors` | 59 |
| `search` | 59 |
| `remoteDeviceConnector` | 55 |
| `album` | 53 |
| `app` | 50 |
| `process` | 50 |
| `systemUpdate` | 50 |
| `action` | 49 |
| `team` | 49 |
| `folderView` | 48 |
| `preference` | 47 |
| `remoteConnection` | 47 |
| `authorizedDevices` | 45 |
| `beginnerGuide` | 44 |
| `appcgi.network` | 39 |
| `appcgi.sac` | 39 |
| `conditionalAlbum` | 39 |
| `upload` | 39 |
| `statusBar` | 38 |
| `components` | 37 |
| `tabs` | 35 |
| `user` | 35 |
| `application` | 34 |
| `tfaErrors` | 34 |
| `common` | 33 |
| `appcgi.netsvr` | 32 |
| `trim` | 31 |
| `backupLogDialog` | 30 |
| `person` | 30 |
| `archive` | 28 |
| `appcgi.sysinfo` | 27 |
| `userManagement` | 27 |
| `desktop` | 26 |
| `folderManage` | 26 |
| `settings` | 26 |
| `hooks` | 25 |
| `toolbar` | 25 |
| `appcgi.share` | 23 |
| `initialization` | 23 |
| `namesake` | 23 |
| `preview` | 23 |
| `shared` | 23 |
| `tagStatusLabel` | 23 |
| `nasConnecterDialog` | 22 |
| `appcgi.backup` | 21 |
| `persons` | 21 |
| `share` | 21 |
| `appcgi.tfa` | 20 |
| `backupTaskPlan` | 18 |
| `confirm` | 18 |
| `account` | 17 |
| `field` | 17 |
| `shareAlbum` | 17 |
| `appcgi.resmon` | 16 |
| `cryptDialog` | 16 |
| `manualInstall` | 16 |
| `photoWall` | 16 |
| `appDetail` | 15 |
| `appcgi.mountmgr` | 15 |
| `exportAssistanceTask` | 15 |
| `globalSettings` | 15 |
| `sidebar` | 15 |
| `ui` | 15 |
| `actions` | 14 |
| `externalStorage` | 14 |
| `handler` | 14 |
| `taskCard` | 14 |
| `appcgi.sharesvr` | 13 |
| `dragError` | 13 |
| `fileHandler` | 13 |
| `react` | 13 |
| `reconnect` | 13 |
| `appcgi.sysrestore` | 12 |
| `backupIconLabel` | 12 |
| `deviceDefaultName` | 12 |
| `modals` | 12 |
| `pathFormatter` | 12 |
| `totp` | 12 |
| `photoHandler` | 11 |
| `ups` | 11 |
| `utils` | 11 |
| `appcgi.license` | 10 |
| `equipmentManagement` | 10 |
| `fixTool` | 10 |
| `appcgi.ipblocker` | 9 |
| `appcgi.screen` | 9 |
| `backupOperationsDialog` | 9 |
| `compExtensionsSettings` | 9 |
| `exportAssistanceForm` | 9 |
| `hardDiskManagement` | 9 |
| `menus` | 9 |
| `taskEditorDialog` | 9 |
| `appcgi.security` | 8 |
| `bin` | 8 |
| `date` | 8 |
| `mediaCategory` | 8 |
| `messages` | 8 |
| `modal` | 8 |
| `openFileGuard` | 8 |
| `usrdat` | 8 |
| `appcgi.eventlogger` | 7 |
| `auth` | 7 |
| `error` | 7 |
| `externalAuth` | 7 |
| `props` | 7 |
| `validation` | 7 |
| `volume` | 7 |
| `backupSourceDialog` | 6 |
| `notify` | 6 |
| `remoteMount` | 6 |
| `storageList` | 6 |
| `wizard` | 6 |
| `appAccess` | 5 |
| `authorizeFile` | 5 |
| `device` | 5 |
| `fileProtocolConnecterDialog` | 5 |
| `hardware` | 5 |
| `languageAndTime` | 5 |
| `menu` | 5 |
| `module` | 5 |
| `remoteDir` | 5 |
| `style` | 5 |
| `table` | 5 |
| `tour` | 5 |
| `util` | 5 |
| `about` | 4 |
| `appcgi.filestor` | 4 |
| `appcgi.finder` | 4 |
| `arrowProps` | 4 |
| `com` | 4 |
| `compFormWidgets` | 4 |
| `emptyFolder` | 4 |
| `ignoreExtensionsSettings` | 4 |
| `install` | 4 |
| `installSettings` | 4 |
| `level` | 4 |
| `liveupdate` | 4 |
| `offline` | 4 |
| `trustDevice` | 4 |
| `uploadConfig` | 4 |
| `validator` | 4 |
| `appApiErrors` | 3 |
| `appcgi.accountsrv` | 3 |
| `body` | 3 |
| `browser` | 3 |
| `download` | 3 |
| `features` | 3 |
| `header` | 3 |
| `installed` | 3 |
| `license` | 3 |
| `log` | 3 |
| `nativeEvent` | 3 |
| `pagination` | 3 |
| `target` | 3 |
| `tempFileSettings` | 3 |
| `tfaDisable` | 3 |
| `theme` | 3 |
| `userSettings` | 3 |
| `additional` | 2 |
| `admin` | 2 |
| `appcgi.usersrv` | 2 |
| `av01` | 2 |
| `avc1` | 2 |
| `colgroup` | 2 |
| `column` | 2 |
| `compMiniDeviceCard` | 2 |
| `dd` | 2 |
| `deviceCardDescription` | 2 |
| `disconnectModal` | 2 |
| `event` | 2 |
| `exconn` | 2 |
| `filePicker` | 2 |
| `footer` | 2 |
| `format` | 2 |
| `icenter` | 2 |
| `index` | 2 |
| `map` | 2 |
| `monthLeft` | 2 |
| `monthRight` | 2 |
| `mp4a` | 2 |
| `net` | 2 |
| `page` | 2 |
| `power` | 2 |
| `recentRecord` | 2 |
| `storage` | 2 |
| `tar` | 2 |
| `task` | 2 |
| `trash` | 2 |
| `apis` | 1 |
| `appShareFiles` | 1 |
| `appStore` | 1 |
| `appcgi.iscsimgr` | 1 |
| `appcgi.updatemgr` | 1 |
| `attributes` | 1 |
| `backupSourcePathFormatter` | 1 |
| `cell` | 1 |
| `compConnectedDeviceCard` | 1 |
| `compDeviceIcon` | 1 |
| `config` | 1 |
| `data` | 1 |
| `dependentApps` | 1 |
| `env` | 1 |
| `hvc1` | 1 |
| `i18next` | 1 |
| `ignoreDotPrefixSettings` | 1 |
| `initialFocusRef` | 1 |
| `inputRef` | 1 |
| `keepFilesSettings` | 1 |
| `monthGrid` | 1 |
| `mp4v` | 1 |
| `myShare` | 1 |
| `navigator` | 1 |
| `org` | 1 |
| `photo` | 1 |
| `pickFolder` | 1 |
| `player` | 1 |
| `rangeInputEndRef` | 1 |
| `rangeInputStartRef` | 1 |
| `remote` | 1 |
| `rowSelection` | 1 |
| `scroll` | 1 |
| `semi` | 1 |
| `stpp` | 1 |
| `taskActionTips` | 1 |
| `taskState` | 1 |
| `tfaVerify` | 1 |
| `type` | 1 |
| `vp09` | 1 |
| `y` | 1 |

# endpoint（514）


## apis

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `apis.tfa.getMineConfig` | `cacheKey` | alias,loose | 5 |  |

## app

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `app.getdefinstvolume` | `getdefinstvolume` | alias,loose | 5 |  |
| `app.geticon` | `geticon` | alias,loose | 5 |  |
| `app.info` | `info` | alias,loose | 5 |  |
| `app.install` | `install` | alias,loose | 5 |  |
| `app.list` | `list` | alias,loose | 5 |  |
| `app.listvolume` | `listVolume` | alias,loose | 5 |  |
| `app.restart` | `restart` | alias,loose | 5 |  |
| `app.setdefinstvolume` | `setdefinstvolume` | alias,loose | 5 |  |
| `app.start` | `start` | alias,loose | 5 |  |
| `app.stop` | `stop` | alias,loose | 5 |  |
| `app.uninstall` | `uninstall` | alias,loose | 5 |  |

## appcgi.accountsrv

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appcgi.accountsrv.v1.token.edit` | `updateAuthorizedDeviceScopes` | alias,loose | 5 |  |
| `appcgi.accountsrv.v1.token.list` | `listAuthorizedDevice` | alias,loose | 5 |  |
| `appcgi.accountsrv.v1.token.revoke` | `delAuthorizedDevice` | alias,loose | 5 |  |

## appcgi.backup

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appcgi.backup.logger.list` | `logList` | alias,loose | 5 |  |
| `appcgi.backup.nas.find` | `findNas` | alias,loose | 5 |  |
| `appcgi.backup.storage.add` | `addStorage` | alias,loose | 5 |  |
| `appcgi.backup.storage.checkConnection` | `checkConnection` | alias,loose | 5 |  |
| `appcgi.backup.storage.createDir` | `createDir` | alias,loose | 5 |  |
| `appcgi.backup.storage.delete` | `deleteStorage` | alias,loose | 5 |  |
| `appcgi.backup.storage.getAuthUrl` | `getAuthUrl` | alias,loose | 5 |  |
| `appcgi.backup.storage.getQuota` | `getQuota` | alias,loose | 5 |  |
| `appcgi.backup.storage.list` | `storageList` | alias,loose | 5 |  |
| `appcgi.backup.storage.listDir` | `listDir` | alias,loose | 5 |  |
| `appcgi.backup.storage.update` | `updateStorage` | alias,loose | 5 |  |
| `appcgi.backup.task.add` | `addTask` | alias,loose | 5 |  |
| `appcgi.backup.task.delete` | `deleteTask` | alias,loose | 5 |  |
| `appcgi.backup.task.detail` | `taskDetails` | alias,loose | 5 |  |
| `appcgi.backup.task.disable` | `disableTask` | alias,loose | 5 |  |
| `appcgi.backup.task.enable` | `enableTask` | alias,loose | 5 |  |
| `appcgi.backup.task.list` | `taskList` | alias,loose | 5 |  |
| `appcgi.backup.task.operations` | `operationList` | alias,loose | 5 |  |
| `appcgi.backup.task.run` | `runTask` | alias,loose | 5 |  |
| `appcgi.backup.task.stop` | `stopTask` | alias,loose | 5 |  |
| `appcgi.backup.task.update` | `updateTask` | alias,loose | 5 |  |

## appcgi.eventlogger

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appcgi.eventlogger.common.archive` | `archiveLoggerSet` | alias,loose | 5 |  |
| `appcgi.eventlogger.common.archive.get` | `archiveLoggerSetQuery` | alias,loose | 5 |  |
| `appcgi.eventlogger.common.clear` | `clearLogger` | alias,loose | 5 |  |
| `appcgi.eventlogger.common.export` | `exportLogger` | alias,loose | 5 |  |
| `appcgi.eventlogger.common.list` | `getLogger` | alias,loose | 5 |  |
| `appcgi.eventlogger.debuglog.copyStart` | `debuglogCopy` | alias,loose | 5 |  |
| `appcgi.eventlogger.debuglog.copyStop` | `debuglogCopyStop` | alias,loose | 5 |  |

## appcgi.filestor

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appcgi.filestor.getAppDirList` | `getAppDirList` | alias,loose | 5 |  |
| `appcgi.filestor.getSysPartInfo` | `getSysPartInfo` | alias,loose | 5 |  |
| `appcgi.filestor.getTeamDirList` | `getTeamDirList` | alias,loose | 5 |  |
| `appcgi.filestor.isMountPoint` | `isMountPoint` | alias,loose | 5 |  |

## appcgi.finder

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appcgi.finder.cancelSearch` | `cancelSearch` | alias,loose | 5 |  |
| `appcgi.finder.fileSearch` | `search` | alias,loose | 5 |  |
| `appcgi.finder.searchOtherSharing` | `shareSearchOthers` | alias,loose | 5 |  |
| `appcgi.finder.trashSearch` | `trashSearch` | alias,loose | 5 |  |

## appcgi.ipblocker

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appcgi.ipblocker.addAllowList` | `addAllowList` | alias,loose | 5 |  |
| `appcgi.ipblocker.addDenyList` | `addDenyList` | alias,loose | 5 |  |
| `appcgi.ipblocker.autoBlock` | `autoBlock` | alias,loose | 5 |  |
| `appcgi.ipblocker.autoBlockRule` | `autoBlockRule` | alias,loose | 5 |  |
| `appcgi.ipblocker.deleteAllowList` | `deleteAllowList` | alias,loose | 5 |  |
| `appcgi.ipblocker.deleteDenyList` | `deleteDenyList` | alias,loose | 5 |  |
| `appcgi.ipblocker.queryAllowList` | `queryAllowList` | alias,loose | 5 |  |
| `appcgi.ipblocker.queryAutoBlockRule` | `queryAutoBlockRule` | alias,loose | 5 |  |
| `appcgi.ipblocker.queryDenyList` | `queryDenyList` | alias,loose | 5 |  |

## appcgi.iscsimgr

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appcgi.iscsimgr.iscsi.lun.list` | `lunList` | alias,loose | 5 |  |

## appcgi.license

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appcgi.license.soft.code.active` | `active` | alias,loose | 5 |  |
| `appcgi.license.soft.code.license` | `info` | alias,loose | 5 |  |
| `appcgi.license.soft.get` | `get` | alias,loose | 5 |  |
| `appcgi.license.soft.ipc.get` | `ipcGet` | alias,loose | 5 |  |
| `appcgi.license.soft.list` | `list` | alias,loose | 5 |  |
| `appcgi.license.soft.recover` | `recover` | alias,loose | 5 |  |
| `appcgi.license.soft.remove` | `remove` | alias,loose | 5 |  |
| `appcgi.license.soft.test.sendnotify` | `sendnotify` | alias,loose | 5 |  |
| `appcgi.license.soft.trial` | `trial` | alias,loose | 5 |  |
| `appcgi.license.soft.trial.applystatus` | `trialApplyStatus` | alias,loose | 5 |  |

## appcgi.mountmgr

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appcgi.mountmgr.cache.refresh` | `refreshCache` | alias,loose | 5 |  |
| `appcgi.mountmgr.check` | `check` | alias,loose | 5 |  |
| `appcgi.mountmgr.dfs.acquireUploadCacheDir` | `acquireUploadCacheDir` | alias,loose | 5 |  |
| `appcgi.mountmgr.dfs.cleanUploadCacheDir` | `cleanUploadCacheDir` | alias,loose | 5 |  |
| `appcgi.mountmgr.dfs.startUpload` | `startUpload` | alias,loose | 5 |  |
| `appcgi.mountmgr.list` | `list` | alias,loose | 5 |  |
| `appcgi.mountmgr.mount` | `mount` | alias,loose | 5 |  |
| `appcgi.mountmgr.mountInfo` | `mountInfo` | alias,loose | 5 |  |
| `appcgi.mountmgr.setting.detail` | `getSelectedVolForRemoteMountUpload` | alias,loose | 5 |  |
| `appcgi.mountmgr.setting.update` | `setSelectedVolForRemoteMountUpload` | alias,loose | 5 |  |
| `appcgi.mountmgr.shares` | `shares` | alias,loose | 5 |  |
| `appcgi.mountmgr.task.cancel` | `taskCancel` | alias,loose | 5 |  |
| `appcgi.mountmgr.task.detail` | `taskDetail` | alias,loose | 5 |  |
| `appcgi.mountmgr.task.list` | `taskList` | alias,loose | 5 |  |
| `appcgi.mountmgr.umount` | `umount` | alias,loose | 5 |  |

## appcgi.netsvr

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appcgi.netsvr.cert.apply` | `applyCert` | alias,loose | 5 |  |
| `appcgi.netsvr.cert.applystatus` | `getCertTaskStatus` | alias,loose | 5 |  |
| `appcgi.netsvr.cert.export` | `exportCert` | alias,loose | 5 |  |
| `appcgi.netsvr.cert.getuse` | `getUseCert` | alias,loose | 5 |  |
| `appcgi.netsvr.cert.list` | `getCertList` | alias,loose | 5 |  |
| `appcgi.netsvr.cert.remove` | `deleteCert` | alias,loose | 5 |  |
| `appcgi.netsvr.cert.renew` | `renewCert` | alias,loose | 5 |  |
| `appcgi.netsvr.cert.replace` | `replaceCert` | alias,loose | 5 |  |
| `appcgi.netsvr.cert.setuse` | `setUsedCert` | alias,loose | 5 |  |
| `appcgi.netsvr.cert.sysreset` | `updateSystemCert` | alias,loose | 5 |  |
| `appcgi.netsvr.cert.upload` | `uploadCert` | alias,loose | 5 |  |
| `appcgi.netsvr.conn.change` | `updateFnConnectInfo` | alias,loose | 5 |  |
| `appcgi.netsvr.conn.create` | `createFnConnectInfo` | alias,loose | 5 |  |
| `appcgi.netsvr.conn.getconfig` | `getFnConnectConfig` | alias,loose | 5 |  |
| `appcgi.netsvr.conn.open` | `openFnContentStatus` | alias,loose | 5 |  |
| `appcgi.netsvr.conn.quit` | `updateFnConnectStatus` | alias,loose | 5 |  |
| `appcgi.netsvr.conn.setconfig` | `setFnConnectConfig` | alias,loose | 5 |  |
| `appcgi.netsvr.conn.status` | `getFnConnectInfo` | alias,loose | 5 |  |
| `appcgi.netsvr.ddns.provider.list` | `getDDNSProviderList` | alias,loose | 5 |  |
| `appcgi.netsvr.ddns.record.create` | `createDDNS` | alias,loose | 5 |  |
| `appcgi.netsvr.ddns.record.detail` | `getDDNSInfo` | alias,loose | 5 |  |
| `appcgi.netsvr.ddns.record.list` | `getDDNSList` | alias,loose | 5 |  |
| `appcgi.netsvr.ddns.record.refresh` | `refreshDdns` | alias,loose | 5 |  |
| `appcgi.netsvr.ddns.record.remove` | `deleteDdns` | alias,loose | 5 |  |
| `appcgi.netsvr.ddns.record.test` | `testDDNSRecord` | alias,loose | 5 |  |
| `appcgi.netsvr.ddns.record.update` | `updateDDNS` | alias,loose | 5 |  |
| `appcgi.netsvr.domain.list` | `getTrimDomainList` | alias,loose | 5 |  |
| `appcgi.netsvr.domain.sharecheck` | `checkFnShareLink` | alias,loose | 5 |  |
| `appcgi.netsvr.fnassistant.close` | `closeAssistance` | alias,loose | 5 |  |
| `appcgi.netsvr.fnassistant.info` | `getAssistanceInfo` | alias,loose | 5 |  |
| `appcgi.netsvr.fnassistant.open` | `openAssistance` | alias,loose | 5 |  |
| `appcgi.netsvr.network.list` | `getNetworkInfo` | alias,loose | 5 |  |

## appcgi.network

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appcgi.network.gen.info` | `genInfo` | alias,loose | 5 |  |
| `appcgi.network.gen.set` | `genSet` | alias,loose | 5 |  |
| `appcgi.network.gw.getting` | `getting` | alias,loose | 5 |  |
| `appcgi.network.gw.setting` | `setting` | alias,loose | 5 |  |
| `appcgi.network.hostname` | `hostname` | alias,loose | 5 |  |
| `appcgi.network.net.add` | `networkAdd` | alias,loose | 5 |  |
| `appcgi.network.net.arping` | `netArPing` | alias,loose | 5 |  |
| `appcgi.network.net.bridge` | `createBridge` | alias,loose | 5 |  |
| `appcgi.network.net.conn` | `networkConnect` | alias,loose | 5 |  |
| `appcgi.network.net.del` | `networkDelete` | alias,loose | 5 |  |
| `appcgi.network.net.detect` | `networkDetect` | alias,loose | 5 |  |
| `appcgi.network.net.disc` | `networkDisconnect` | alias,loose | 5 |  |
| `appcgi.network.net.getMultiGWStatus` | `getMultiGWStatus` | alias,loose | 5 |  |
| `appcgi.network.net.getNicPerformanceMode` | `getNicPerformanceMode` | alias,loose | 5 |  |
| `appcgi.network.net.info` | `netInfo` | alias,loose | 5 |  |
| `appcgi.network.net.list` | `netList` | alias,loose | 5 |  |
| `appcgi.network.net.reset` | `resetNetwork` | alias,loose | 5 |  |
| `appcgi.network.net.set` | `netSet` | alias,loose | 5 |  |
| `appcgi.network.net.setMultiGW` | `setMultiGW` | alias,loose | 5 |  |
| `appcgi.network.net.setNicPerformanceMode` | `setNicPerformanceMode` | alias,loose | 5 |  |
| `appcgi.network.net.state` | `networkState` | alias,loose | 5 |  |
| `appcgi.network.route.list` | `routeList` | alias,loose | 5 |  |
| `appcgi.network.ssh.set` | `setSSH` | alias,loose | 5 |  |
| `appcgi.network.ssh.status` | `sshStatus` | alias,loose | 5 |  |
| `appcgi.network.ssh.switch` | `switchSSH` | alias,loose | 5 |  |
| `appcgi.network.static.add` | `staticAdd` | alias,loose | 5 |  |
| `appcgi.network.static.del` | `staticDel` | alias,loose | 5 |  |
| `appcgi.network.static.list` | `staticList` | alias,loose | 5 |  |
| `appcgi.network.static.set` | `staticSet` | alias,loose | 5 |  |
| `appcgi.network.wifi.apList` | `getWifiList` | alias,loose | 5 |  |
| `appcgi.network.wifi.close` | `closeWifi` | alias,loose | 5 |  |
| `appcgi.network.wifi.connectHiddenAP` | `connectHiddenAP` | alias,loose | 5 |  |
| `appcgi.network.wifi.connectKnownAP` | `connectKnownAP` | alias,loose | 5 |  |
| `appcgi.network.wifi.connectUnknownAP` | `connectUnknownAP` | alias,loose | 5 |  |
| `appcgi.network.wifi.connectedAP` | `connectedAP` | alias,loose | 5 |  |
| `appcgi.network.wifi.getKnownAPInfo` | `getKnownAPInfo` | alias,loose | 5 |  |
| `appcgi.network.wifi.ignoreKnownAP` | `ignoreKnownAP` | alias,loose | 5 |  |
| `appcgi.network.wifi.open` | `openWifi` | alias,loose | 5 |  |
| `appcgi.network.wifi.setKnownAPInfo` | `setKnownAPInfo` | alias,loose | 5 |  |

## appcgi.resmon

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appcgi.resmon.alert.getBeepEvents` | `getBeepEvents` | alias,loose | 5 |  |
| `appcgi.resmon.alert.getBeepReasons` | `getBeepReasons` | alias,loose | 5 |  |
| `appcgi.resmon.alert.getSupportedBeepEvents` | `getSupportedBeepEvents` | alias,loose | 5 |  |
| `appcgi.resmon.alert.muteBeeper` | `muteBeeper` | alias,loose | 5 |  |
| `appcgi.resmon.alert.setBeepEvents` | `setBeepEvents` | alias,loose | 5 |  |
| `appcgi.resmon.battery` | `battery` | alias,loose | 5 |  |
| `appcgi.resmon.cpu` | `cpu` | alias,loose | 5 |  |
| `appcgi.resmon.disk` | `disk` | alias,loose | 5 |  |
| `appcgi.resmon.gen` | `gen` | alias,loose | 5 |  |
| `appcgi.resmon.gpu` | `gpu` | alias,loose | 5 |  |
| `appcgi.resmon.mem` | `mem` | alias,loose | 5 |  |
| `appcgi.resmon.npu` | `npu` | alias,loose | 5 |  |
| `appcgi.resmon.proc.list` | `getProcList` | alias,loose | 5 |  |
| `appcgi.resmon.proc.signal` | `procSignal` | alias,loose | 5 |  |
| `appcgi.resmon.proc.srv` | `getProcSrv` | alias,loose | 5 |  |
| `appcgi.resmon.sysFan` | `sysFan` | alias,loose | 5 |  |

## appcgi.sac

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appcgi.sac.desktop.v1.getConfig` | `desktopConfig` | alias,loose | 5 |  |
| `appcgi.sac.desktop.v1.markWallpaper` | `desktopMarkWallpaper` | alias,loose | 5 |  |
| `appcgi.sac.desktop.v1.removeWallpaper` | `desktopRemoveWallpaper` | alias,loose | 5 |  |
| `appcgi.sac.desktop.v1.setBgColor` | `desktopSetBgColor` | alias,loose | 5 |  |
| `appcgi.sac.desktop.v1.setColor` | `desktopSetColor` | alias,loose | 5 |  |
| `appcgi.sac.desktop.v1.setFillMode` | `desktopSetFillMode` | alias,loose | 5 |  |
| `appcgi.sac.desktop.v1.setTheme` | `desktopSetTheme` | alias,loose | 5 |  |
| `appcgi.sac.desktop.v1.setWallpaper` | `desktopSetWallpaper` | alias,loose | 5 |  |
| `appcgi.sac.desktop.v1.setWallpaperType` | `desktopSetWallpaperType` | alias,loose | 5 |  |
| `appcgi.sac.entry.v1.addUserDesktopEntry` | `addUserDesktopEntry` | alias,loose | 5 |  |
| `appcgi.sac.entry.v1.appStoreList` | `appStoreList` | alias,loose | 10 |  |
| `appcgi.sac.entry.v1.delUserDesktopEntry` | `delUserDesktopEntry` | alias,loose | 5 |  |
| `appcgi.sac.entry.v1.dockerList` | `dockerList` | alias,loose | 5 |  |
| `appcgi.sac.entry.v1.editUserDesktopEntry` | `editUserDesktopEntry` | alias,loose | 5 |  |
| `appcgi.sac.entry.v1.exchangeEntryToken` | `exchangeEntryToken` | alias,loose | 5 |  |
| `appcgi.sac.entry.v1.fileAssociations.all` | `all` | alias,loose | 5 |  |
| `appcgi.sac.entry.v1.fileAssociations.list` | `list` | alias,loose | 5 |  |
| `appcgi.sac.entry.v1.fileAssociations.setDefault` | `setDefault` | alias,loose | 5 |  |
| `appcgi.sac.entry.v1.getEntryList` | `getEntryList` | alias,loose | 5 |  |
| `appcgi.sac.entry.v1.getUserDesktop` | `getUserDesktop` | alias,loose | 5 |  |
| `appcgi.sac.entry.v1.recordDesktopSort` | `recordDesktopSort` | alias,loose | 5 |  |
| `appcgi.sac.externalnotify.v1.email.buildOAuthURL` | `buildOAuthURL` | alias,loose | 5 |  |
| `appcgi.sac.externalnotify.v1.email.getAccessToken` | `getAccessToken` | alias,loose | 5 |  |
| `appcgi.sac.externalnotify.v1.email.getConfig` | `getEmailConfig` | alias,loose | 5 |  |
| `appcgi.sac.externalnotify.v1.email.getProviders` | `getEmailProviders` | alias,loose | 5 |  |
| `appcgi.sac.externalnotify.v1.email.revokeOAuth` | `revokeOAuth` | alias,loose | 5 |  |
| `appcgi.sac.externalnotify.v1.email.sendTestEmail` | `sendTestEmail` | alias,loose | 5 |  |
| `appcgi.sac.externalnotify.v1.email.startOrUpdateServerConfig` | `startOrUpdateEmailConfig` | alias,loose | 5 |  |
| `appcgi.sac.externalnotify.v1.email.stop` | `stopEmailServer` | alias,loose | 5 |  |
| `appcgi.sac.externalnotify.v1.email.updateConfig` | `updateSubjectPrefix` | alias,loose | 5 |  |
| `appcgi.sac.i18n.v1.config.get` | `getI18nConfig` | alias,loose | 5 |  |
| `appcgi.sac.i18n.v1.config.set` | `setI18nConfig` | alias,loose | 5 |  |
| `appcgi.sac.license.v1.config.get` | `licenseConfig` | alias,loose | 5 |  |
| `appcgi.sac.license.v1.config.set` | `setLicenseConfig` | alias,loose | 5 |  |
| `appcgi.sac.ups.v1.bindOrUnbind` | `upsBindOrUnbind` | alias,loose | 5 |  |
| `appcgi.sac.ups.v1.check` | `upsCheck` | alias,loose | 5 |  |
| `appcgi.sac.ups.v1.deviceList` | `upsDeviceList` | alias,loose | 5 |  |
| `appcgi.sac.ups.v1.list` | `upsList` | alias,loose | 5 |  |
| `appcgi.sac.ups.v1.status` | `upsStatus` | alias,loose | 5 |  |

## appcgi.screen

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appcgi.screen.getImageUploadPath` | `getImageUploadPath` | alias,loose | 5 |  |
| `appcgi.screen.getOptions` | `getOptions` | alias,loose | 5 |  |
| `appcgi.screen.getScreenImage` | `getScreenImage` | alias,loose | 5 |  |
| `appcgi.screen.getScreenSize` | `getScreenSize` | alias,loose | 5 |  |
| `appcgi.screen.getScreenVideo` | `getScreenVideo` | alias,loose | 5 |  |
| `appcgi.screen.isSleeping` | `isSleeping` | alias,loose | 5 |  |
| `appcgi.screen.setOptions` | `setOptions` | alias,loose | 5 |  |
| `appcgi.screen.setScreenImage` | `setScreenImage` | alias,loose | 5 |  |
| `appcgi.screen.setScreenVideo` | `setScreenVideo` | alias,loose | 5 |  |

## appcgi.security

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appcgi.security.firewall.getting` | `getConfig` | alias,loose | 5 |  |
| `appcgi.security.firewall.iflist` | `getIflist` | alias,loose | 5 |  |
| `appcgi.security.firewall.ifstat` | `getIfstat` | alias,loose | 5 |  |
| `appcgi.security.firewall.servlist` | `getServlist` | alias,loose | 5 |  |
| `appcgi.security.firewall.setting` | `setConfig` | alias,loose | 5 |  |
| `appcgi.security.flowaudit.traffic` | `getFlowauditTraffic` | alias,loose | 5 |  |
| `appcgi.security.safeCode.getting` | `safeCodeGetting` | alias,loose | 5 |  |
| `appcgi.security.safeCode.setting` | `safeCodeSetting` | alias,loose | 5 |  |

## appcgi.share

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appcgi.share.check.port` | `checkPort` | alias,loose | 5 |  |
| `appcgi.share.dlna.opt` | `dlnaOpt` | alias,loose | 5 |  |
| `appcgi.share.dlna.set` | `dlnaSet` | alias,loose | 5 |  |
| `appcgi.share.dlna.share.opt` | `dlnaShareOpt` | alias,loose | 5 |  |
| `appcgi.share.dlna.share.set` | `dlnaShareSet` | alias,loose | 5 |  |
| `appcgi.share.ftp.opt` | `ftpOpt` | alias,loose | 5 |  |
| `appcgi.share.ftp.set` | `ftpSet` | alias,loose | 5 |  |
| `appcgi.share.ftp.share.opt` | `ftpShareOpt` | alias,loose | 5 |  |
| `appcgi.share.ftp.share.set` | `ftpShareSet` | alias,loose | 5 |  |
| `appcgi.share.nfs.opt` | `nfsOpt` | alias,loose | 5 |  |
| `appcgi.share.nfs.set` | `nfsSet` | alias,loose | 5 |  |
| `appcgi.share.nfs.share.opt` | `nfsShareOpt` | alias,loose | 5 |  |
| `appcgi.share.nfs.share.set` | `nfsShareSet` | alias,loose | 5 |  |
| `appcgi.share.smb.opt` | `smbOpt` | alias,loose | 5 |  |
| `appcgi.share.smb.set` | `smbSet` | alias,loose | 5 |  |
| `appcgi.share.smb.share.opt` | `smbShareOpt` | alias,loose | 5 |  |
| `appcgi.share.smb.share.set` | `smbShareSet` | alias,loose | 5 |  |
| `appcgi.share.smb.tm.set` | `smbTimeMachineSet` | alias,loose | 5 |  |
| `appcgi.share.team.allowShare` | `teamAllowShare` | alias,loose | 5 |  |
| `appcgi.share.webdav.opt` | `webdavOpt` | alias,loose | 5 |  |
| `appcgi.share.webdav.set` | `webdavSet` | alias,loose | 5 |  |
| `appcgi.share.webdav.share.opt` | `webdavShareOpt` | alias,loose | 5 |  |
| `appcgi.share.webdav.share.set` | `webdavShareSet` | alias,loose | 5 |  |

## appcgi.sharesvr

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appcgi.sharesvr.share.link.clear` | `shareLinkClear` | alias,loose | 5 |  |
| `appcgi.sharesvr.share.link.create` | `shareLinkCreate` | alias,loose | 5 |  |
| `appcgi.sharesvr.share.link.default` | `shareLinkDefault` | alias,loose | 5 |  |
| `appcgi.sharesvr.share.link.default.get` | `shareLinkDefaultInfo` | alias,loose | 5 |  |
| `appcgi.sharesvr.share.link.default.set` | `shareLinkDefaultInfoSet` | alias,loose | 5 |  |
| `appcgi.sharesvr.share.link.get` | `shareLinkInfo` | alias,loose | 5 |  |
| `appcgi.sharesvr.share.link.list` | `shareLinkList` | alias,loose | 5 |  |
| `appcgi.sharesvr.share.link.remove` | `shareLinkRemove` | alias,loose | 5 |  |
| `appcgi.sharesvr.share.link.update` | `shareLinkUpdate` | alias,loose | 5 |  |
| `appcgi.sharesvr.share.permission.get` | `sharePermission` | alias,loose | 5 |  |
| `appcgi.sharesvr.share.permission.set` | `sharePermissionSet` | alias,loose | 5 |  |
| `appcgi.sharesvr.share.uploadpermission.get` | `shareUploadPermission` | alias,loose | 5 |  |
| `appcgi.sharesvr.share.uploadpermission.set` | `shareUploadPermissionSet` | alias,loose | 5 |  |

## appcgi.sysinfo

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appcgi.sysinfo.addPowerPlan` | `addPowerPlan` | alias,loose | 5 |  |
| `appcgi.sysinfo.deletePowerPlan` | `deletePowerPlan` | alias,loose | 5 |  |
| `appcgi.sysinfo.getBootOnPowerFlag` | `getBootOnPowerFlag` | alias,loose | 5 |  |
| `appcgi.sysinfo.getFanMode` | `getFanMode` | alias,loose | 5 |  |
| `appcgi.sysinfo.getHardwareInfo` | `getHardwareInfo` | alias,loose | 5 |  |
| `appcgi.sysinfo.getHostName` | `getHostName` | alias,loose | 5 |  |
| `appcgi.sysinfo.getMachineId` | `getMachineId` | alias,loose | 5 |  |
| `appcgi.sysinfo.getNetInfo` | `getNetInfo` | alias,loose | 5 |  |
| `appcgi.sysinfo.getPowerPlanStatus` | `getPowerPlanStatus` | alias,loose | 5 |  |
| `appcgi.sysinfo.getReservedPartition` | `getReservedPartition` | alias,loose | 5 |  |
| `appcgi.sysinfo.getTimeSetting` | `getTimeSetting` | alias,loose | 5 |  |
| `appcgi.sysinfo.getTimezoneList` | `getTimezoneList` | alias,loose | 5 |  |
| `appcgi.sysinfo.getTrimDisk` | `getTrimDisk` | alias,loose | 5 |  |
| `appcgi.sysinfo.getTrimMachineFeature` | `getTrimMachineFeature` | alias,loose | 5 |  |
| `appcgi.sysinfo.getTrimMachineType` | `getTrimMachineType` | alias,loose | 5 |  |
| `appcgi.sysinfo.getTrimVersion` | `getTrimVersion` | alias,loose | 5 |  |
| `appcgi.sysinfo.getUptime` | `getUptime` | alias,loose | 5 |  |
| `appcgi.sysinfo.initHostName` | `initHostName` | alias,loose | 5 |  |
| `appcgi.sysinfo.isTrimMachine` | `isTrimMachine` | alias,loose | 5 |  |
| `appcgi.sysinfo.listPowerPlan` | `listPowerPlan` | alias,loose | 5 |  |
| `appcgi.sysinfo.modifyPowerPlan` | `modifyPowerPlan` | alias,loose | 5 |  |
| `appcgi.sysinfo.nextPowerOffTime` | `getNextPowerOffTime` | alias,loose | 5 |  |
| `appcgi.sysinfo.setBootOnPowerFlag` | `setBootOnPowerFlag` | alias,loose | 5 |  |
| `appcgi.sysinfo.setFanMode` | `setFanMode` | alias,loose | 5 |  |
| `appcgi.sysinfo.setHostName` | `updateHostName` | alias,loose | 5 |  |
| `appcgi.sysinfo.setPowerPlanStatus` | `setPowerPlanStatus` | alias,loose | 5 |  |
| `appcgi.sysinfo.setTimeSetting` | `setTimeSetting` | alias,loose | 5 |  |

## appcgi.sysrestore

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appcgi.sysrestore.addSysBackupTask` | `addSysBackupTask` | alias,loose | 5 |  |
| `appcgi.sysrestore.deleteSysBackupBin` | `deleteSysBackupBin` | alias,loose | 5 |  |
| `appcgi.sysrestore.doSysBackup` | `doSysBackup` | alias,loose | 5 |  |
| `appcgi.sysrestore.exportSysconf` | `exportSysconf` | alias,loose | 5 |  |
| `appcgi.sysrestore.getInfo` | `getInfo` | alias,loose | 5 |  |
| `appcgi.sysrestore.getSysBackupInfo` | `getSysBackupInfo` | alias,loose | 5 |  |
| `appcgi.sysrestore.getSysBackupTask` | `getSysBackupTask` | alias,loose | 5 |  |
| `appcgi.sysrestore.getSysconfUploadPath` | `getSysconfUploadPath` | alias,loose | 5 |  |
| `appcgi.sysrestore.importSysconf` | `importSysconf` | alias,loose | 5 |  |
| `appcgi.sysrestore.modifySysBackupTask` | `modifySysBackupTask` | alias,loose | 5 |  |
| `appcgi.sysrestore.setSystemRecovery` | `setSystemRecovery` | alias,loose | 5 |  |
| `appcgi.sysrestore.sysconfImportProgress` | `sysconfImportProgress` | alias,loose | 5 |  |

## appcgi.tfa

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appcgi.tfa.security.v1.device.list` | `getTrustDeviceList` | alias,loose | 5 |  |
| `appcgi.tfa.security.v1.device.trust` | `trustDevice` | alias,loose | 5 |  |
| `appcgi.tfa.security.v1.device.untrust` | `untrustDevice` | alias,loose | 5 |  |
| `appcgi.tfa.security.v1.email.bind` | `bindEmail` | alias,loose | 5 |  |
| `appcgi.tfa.security.v1.email.bindBeforeVerify` | `bindBeforeVerify` | alias,loose | 5 |  |
| `appcgi.tfa.security.v1.email.sendBindCode` | `sendBindCode` | alias,loose | 5 |  |
| `appcgi.tfa.security.v1.login.resetPasswordSendEmail` | `sendResetPasswordEmail` | alias,loose | 5 |  |
| `appcgi.tfa.security.v1.login.resetPasswordVerify` | `resetPasswordVerify` | alias,loose | 5 |  |
| `appcgi.tfa.security.v1.login.sendEmailCode` | `sendEmailBindCode` | alias,loose | 5 |  |
| `appcgi.tfa.security.v1.login.totpVerify` | `loginTotpVerify` | alias,loose | 5 |  |
| `appcgi.tfa.security.v1.me.getConfig` | `getMineConfig` | alias,loose | 5 |  |
| `appcgi.tfa.security.v1.me.twofa.bind` | `bindTfaMine` | alias,loose | 5 |  |
| `appcgi.tfa.security.v1.me.twofa.bindBeforeVerify` | `bindBeforeVerifyTotp` | alias,loose | 5 |  |
| `appcgi.tfa.security.v1.me.twofa.disable` | `disableTfaMine` | alias,loose | 5 |  |
| `appcgi.tfa.security.v1.me.twofa.totpVerify` | `totpVerify` | alias,loose | 5 |  |
| `appcgi.tfa.security.v1.twofa.disable` | `disableTfa` | alias,loose | 5 |  |
| `appcgi.tfa.security.v1.twofa.enable` | `enableTfa` | alias,loose | 5 |  |
| `appcgi.tfa.security.v1.twofa.getConfig` | `getConfig` | alias,loose | 5 |  |
| `appcgi.tfa.security.v1.user.disableTwofa` | `disableUserTfa` | alias,loose | 5 |  |
| `appcgi.tfa.security.v1.user.getTwofaConfig` | `getUserTfaInfo` | alias,loose | 5 |  |

## appcgi.usersrv

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appcgi.usersrv.authUser` | `authUser` | alias,loose | 5 |  |
| `appcgi.usersrv.getAppUserList` | `getAppDirList` | alias,loose | 5 |  |

## data

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `data.dirList` | `itemsPath` | alias,loose | 5 |  |

## dd

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `dd.MM.y` | `short` | alias,loose | 20 |  |
| `dd.MM.yyyy` | `FORMAT_SWITCH_DATE` | alias,loose | 20 |  |

## exconn

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `exconn.getDomain` | `getDomain` | alias,loose | 5 |  |
| `exconn.setDomain` | `setDomain` | alias,loose | 5 |  |

## file

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `file.access` | `access` | alias,loose | 5 |  |
| `file.calc` | `calc` | alias,loose | 5 |  |
| `file.cancel` | `cancel` | alias,loose | 5 |  |
| `file.checkUpload` | `checkUpload` | alias,loose | 5 |  |
| `file.chown` | `chown` | alias,loose | 5 |  |
| `file.compress` | `compress` | alias,loose,assign | 11 |  |
| `file.cp` | `cp` | alias,loose,assign | 11 |  |
| `file.download` | `download` | alias,loose | 5 |  |
| `file.extract` | `extract` | alias,loose,assign | 11 |  |
| `file.fav.add` | `favAdd` | alias,loose | 5 |  |
| `file.fav.del` | `favDel` | alias,loose | 5 |  |
| `file.fav.list` | `favList` | alias,loose | 5 |  |
| `file.getAcl` | `getAcl` | alias,loose | 5 |  |
| `file.ls` | `ls` | alias,loose | 6 |  |
| `file.lsDir` | `lsDir` | alias,loose | 5 |  |
| `file.mkdir` | `mkdir` | alias,loose | 5 |  |
| `file.mv` | `mv` | alias,loose,assign | 11 |  |
| `file.prop` | `prop` | alias,loose | 5 |  |
| `file.recent.add` | `recentAdd` | alias,loose | 5 |  |
| `file.recent.clear` | `recentClear` | alias,loose | 5 |  |
| `file.recent.del` | `recentDel` | alias,loose | 5 |  |
| `file.recent.list` | `recentList` | alias,loose | 5 |  |
| `file.rename` | `rename` | alias,loose | 5 |  |
| `file.rm` | `rm` | alias,loose,assign | 9 |  |
| `file.setAcl` | `setAcl` | alias,loose | 5 |  |
| `file.setAcl2` | `setAcl2` | alias,loose,assign | 9 |  |
| `file.share.add` | `shareAdd` | alias,loose | 5 |  |
| `file.share.add2` | `shareAdd2` | alias,loose,assign | 9 |  |
| `file.share.del2` | `shareDel`, `shareDel2` | alias,loose,assign | 14 |  |
| `file.share.info` | `shareInfo` | alias,loose | 5 |  |
| `file.share.list` | `shareList` | alias,loose | 5 |  |
| `file.share.listOthers` | `shareListOthers` | alias,loose | 5 |  |
| `file.team.lsDir` | `teamLsDir` | alias,loose | 5 |  |
| `file.team.trash.clear` | `teamTrashClear` | alias,loose,assign | 9 |  |
| `file.team.trash.list` | `teamTrashList` | alias,loose | 5 |  |
| `file.team.trash.listTrashbin` | `teamTrashListTrashbin` | alias,loose | 5 |  |
| `file.team.trash.restore` | `teamTrashRestore` | alias,loose,assign | 9 |  |
| `file.trash.clear` | `trashClear` | alias,loose,assign | 9 |  |
| `file.trash.list` | `trashList` | alias,loose | 5 |  |
| `file.trash.restore` | `trashRestore` | alias,loose,assign | 9 |  |
| `file.trimacl.conv` | `trimaclConv` | alias,loose,assign | 9 |  |
| `file.trimacl.conv.report` | `trimaclConvReport` | alias,loose,assign | 9 |  |
| `file.usage` | `usage` | alias,loose | 5 |  |

## icenter

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `icenter.gen` | `gen` | alias,loose | 5 |  |
| `icenter.svc` | `svc` | alias,loose | 5 |  |

## liveupdate

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `liveupdate.check` | `checkUpdate` | alias,loose | 5 |  |
| `liveupdate.fixapt` | `aptUpdate` | alias,loose | 5 |  |
| `liveupdate.status` | `updateStatus` | alias,loose | 5 |  |
| `liveupdate.update` | `update` | alias,loose | 5 |  |

## log

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `log.clear` | `clear` | alias,loose | 5 |  |
| `log.graph` | `graph` | alias,loose | 5 |  |
| `log.list` | `list` | alias,loose | 5 |  |

## monthLeft

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `monthLeft.dateInput` | `valuePath` | alias,loose | 12 |  |
| `monthLeft.timeInput` | `valuePath` | alias,loose | 10 |  |

## monthRight

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `monthRight.dateInput` | `valuePath` | alias,loose | 12 |  |
| `monthRight.timeInput` | `valuePath` | alias,loose | 10 |  |

## notify

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `notify.del` | `del` | alias,loose | 5 |  |
| `notify.delAll` | `delAll` | alias,loose | 5 |  |
| `notify.list` | `list` | alias,loose | 5 |  |
| `notify.setRead` | `setRead` | alias,loose | 5 |  |
| `notify.setReadAll` | `setReadAll` | alias,loose | 5 |  |
| `notify.unreadTotal` | `unreadTotal` | alias,loose | 5 |  |

## power

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `power.poweroff` | `poweroff` | alias,loose | 5 |  |
| `power.reboot` | `reboot` | alias,loose | 5 |  |

## remoteDir

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `remoteDir.add` | `add` | alias,loose | 5 |  |
| `remoteDir.del` | `del` | alias,loose | 5 |  |
| `remoteDir.list` | `list` | alias,loose | 5 |  |
| `remoteDir.mount` | `mount` | alias,loose | 5 |  |
| `remoteDir.umount` | `umount` | alias,loose | 5 |  |

## stor

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `stor.abortSmartTest` | `abortSmartTest` | alias,loose | 5 |  |
| `stor.addDisk` | `addDisk` | alias,loose | 5 |  |
| `stor.addSpareDisk` | `addSpareDisk` | alias,loose | 5 |  |
| `stor.attachCache` | `attachCache` | alias,loose | 5 |  |
| `stor.btrfs.scrub` | `btrfsScrub` | alias,loose | 5 |  |
| `stor.cachedevState` | `cachedevState` | alias,loose | 5 |  |
| `stor.calcSpace` | `calcSpace` | alias,loose | 5 |  |
| `stor.create` | `create` | alias,loose | 5 |  |
| `stor.createCache` | `createCache` | alias,loose | 5 |  |
| `stor.delRec` | `delRec` | alias,loose | 5 |  |
| `stor.detachCache` | `detachCache` | alias,loose | 5 |  |
| `stor.detachCacheAndActive` | `detachCacheAndActive` | alias,loose | 5 |  |
| `stor.diskHealth` | `diskHealth` | alias,loose | 5 |  |
| `stor.diskMount` | `diskMount` | alias,loose | 5 |  |
| `stor.diskSmart` | `diskSmart` | alias,loose | 5 |  |
| `stor.eject` | `eject` | alias,loose | 5 |  |
| `stor.enableSmart` | `enableSmart` | alias,loose | 5 |  |
| `stor.extend` | `extend` | alias,loose | 5 |  |
| `stor.general` | `getStorGeneral` | alias,loose | 5 |  |
| `stor.getConf` | `getConf` | alias,loose | 5 |  |
| `stor.getDiskIdleTime` | `getDiskIdleTime` | alias,loose | 5 |  |
| `stor.getDiskWakeup` | `getDiskWakeup` | alias,loose | 5 |  |
| `stor.getGlobal` | `getGlobal` | alias,loose | 5 |  |
| `stor.getRemovableConf` | `getRemovableConf` | alias,loose | 5 |  |
| `stor.getSysPartInfo` | `getSysPartInfo` | alias,loose | 5 |  |
| `stor.getTeamStorage` | `getTeamStorage` | alias,loose | 5 |  |
| `stor.getUserStorage` | `getUserStorage` | alias,loose | 5 |  |
| `stor.listCachedev` | `listCachedev` | alias,loose | 5 |  |
| `stor.listDisk` | `listDisk` | alias,loose | 5 |  |
| `stor.listFreeDisk` | `listFreeDisk` | alias,loose | 5 |  |
| `stor.listRemovable` | `listRemovable` | alias,loose | 5 |  |
| `stor.listStor` | `listStor` | alias,loose | 5 |  |
| `stor.llbitmap.proactiveSync` | `llBitmapProactiveSync` | alias,loose | 5 |  |
| `stor.lvActive` | `lvActive` | alias,loose | 5 |  |
| `stor.makeTeamStorage` | `makeTeamStorage` | alias,loose | 5 |  |
| `stor.mount` | `mount` | alias,loose | 5 |  |
| `stor.readdDisk` | `readdDisk` | alias,loose | 5 |  |
| `stor.readdDiskToCache` | `readdDiskToCache` | alias,loose | 5 |  |
| `stor.recoverCache` | `recoverCache` | alias,loose | 5 |  |
| `stor.removeDisk` | `removeDisk` | alias,loose | 5 |  |
| `stor.removeDiskCheck` | `removeDiskCheck` | alias,loose | 5 |  |
| `stor.removeWarn` | `removeWarn` | alias,loose | 5 |  |
| `stor.replaceDisk` | `replaceDisk` | alias,loose | 5 |  |
| `stor.resize` | `resize` | alias,loose | 5 |  |
| `stor.runSmartTest` | `runSmartTest` | alias,loose | 5 |  |
| `stor.setConf` | `setConf` | alias,loose | 5 |  |
| `stor.setDiskIdleTime` | `setDiskIdleTime` | alias,loose | 5 |  |
| `stor.setDiskWakeup` | `setDiskWakeup` | alias,loose | 5 |  |
| `stor.setGlobal` | `setGlobal` | alias,loose | 5 |  |
| `stor.setRemovableConf` | `setRemovableConf` | alias,loose | 5 |  |
| `stor.setTeamStorage` | `setTeamStorage` | alias,loose | 5 |  |
| `stor.setTrashbin` | `setTrashbin` | alias,loose | 5 |  |
| `stor.setUserStorage` | `setUserStorage` | alias,loose | 5 |  |
| `stor.state2` | `getStorBasic` | alias,loose | 5 |  |
| `stor.stop` | `stop` | alias,loose | 5 |  |
| `stor.storAddDiskInfo` | `storAddDiskInfo` | alias,loose | 5 |  |
| `stor.umount` | `umount` | alias,loose | 5 |  |
| `stor.zClear` | `zClear` | alias,loose | 5 |  |
| `stor.zExport` | `zExport` | alias,loose | 5 |  |
| `stor.zImport` | `zImport` | alias,loose | 5 |  |
| `stor.zImportList` | `zImportList` | alias,loose | 5 |  |
| `stor.zOnline` | `zOnline` | alias,loose | 5 |  |
| `stor.zRecover` | `zRecover` | alias,loose | 5 |  |
| `stor.zScrub` | `zScrub` | alias,loose | 5 |  |

## target

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `target.checked` | `valuePath` | alias,loose | 20 |  |
| `target.value` | `valuePath` | alias,loose | 10 |  |

## taskState

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `taskState.list` | `list` | alias,loose | 5 |  |

## trim

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `trim.media` | `media` | alias,assign,loose | 9 |  |
| `trim.photos` | `photos` | alias,assign,loose | 9 |  |

## user

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `user.2fa.loginVerify` | `loginVerify` | alias,loose | 6 |  |
| `user.2fa.resetPassword` | `resetPassword` | alias,loose | 6 |  |
| `user.active` | `active`, `req` | alias,loose | 10 |  |
| `user.add` | `add` | alias,loose | 8 |  |
| `user.add1000` | `add1000` | alias,loose | 5 |  |
| `user.auth` | `auth` | alias,loose | 5 |  |
| `user.authToken` | `authToken` | alias,loose | 5 |  |
| `user.changePassword` | `changePassword` | alias,loose | 5 |  |
| `user.checkNewGroup` | `checkNewGroup` | alias,loose | 5 |  |
| `user.checkNewUser` | `checkNewUser` | alias,loose | 5 |  |
| `user.del` | `del` | alias,loose | 5 |  |
| `user.groupAdd` | `groupAdd` | alias,loose | 5 |  |
| `user.groupAddUsers` | `groupAddUsers` | alias,loose | 5 |  |
| `user.groupDel` | `groupDel` | alias,loose | 5 |  |
| `user.groupDelUsers` | `groupDelUsers` | alias,loose | 5 |  |
| `user.groupInfo` | `groupInfo` | alias,loose | 5 |  |
| `user.groupList` | `groupList` | alias,loose | 5 |  |
| `user.groupMod` | `groupMod` | alias,loose | 5 |  |
| `user.groupSetUsers` | `groupSetUsers` | alias,loose | 5 |  |
| `user.groupUsers` | `groupUsers` | alias,loose | 5 |  |
| `user.info` | `info` | alias,loose | 5 |  |
| `user.isAdmin` | `isAdmin` | alias,loose | 5 |  |
| `user.kickLoginDevice` | `kickLoginDevice` | alias,loose | 5 |  |
| `user.list` | `list` | alias,loose | 5 |  |
| `user.listLoginDevice` | `listLoginDevice` | alias,loose | 5 |  |
| `user.listUG` | `listUG` | alias,loose | 5 |  |
| `user.login` | `login` | alias,loose | 5 |  |
| `user.loginIntl` | `loginIntl` | alias,loose | 5 |  |
| `user.logout` | `logout` | alias,loose | 5 |  |
| `user.mod` | `mod` | alias,loose | 5 |  |
| `user.setAdmin` | `setAdmin` | alias,loose | 5 |  |
| `user.tokenLogin` | `tokenLogin` | alias,loose | 5 |  |
| `user.unfreeze` | `unfreeze` | alias,loose | 5 |  |

## usrdat

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `usrdat.del` | `del` | alias,loose | 5 |  |
| `usrdat.delArray` | `delArray` | alias,loose | 5 |  |
| `usrdat.get` | `get` | alias,loose | 5 |  |
| `usrdat.getArray` | `getArray` | alias,loose | 5 |  |
| `usrdat.getArrayUpdateTime` | `getArrayUpdateTime` | alias,loose | 5 |  |
| `usrdat.isArrayValueExists` | `isArrayValueExists` | alias,loose | 5 |  |
| `usrdat.set` | `set` | alias,loose | 5 |  |
| `usrdat.setArray` | `setArray` | alias,loose | 5 |  |

## util

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `util.crypto.getRSAPub` | `getRSAPub` | alias,loose | 5 |  |
| `util.getSI` | `getSI` | alias,loose | 5 |  |
| `util.trimaclNotify` | `trimaclNotify` | alias,loose | 5 |  |

## y

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `y.MM.dd` | `medium`, `short` | alias,loose | 20 |  |

# event（56）


## app

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `app.activated` | - | assign,loose | 4 |  |
| `app.appMeta` | - | assign,loose | 4 |  |
| `app.config.updated` | - | assign,loose | 4 |  |
| `app.hideservice` | - | assign,loose | 4 |  |
| `app.install.failed` | - | assign,loose | 4 |  |
| `app.installed` | - | assign,loose | 9 |  |
| `app.installing` | - | assign,loose | 5 |  |
| `app.showservice` | - | assign,loose | 4 |  |
| `app.start.failed` | - | assign,loose | 4 |  |
| `app.started` | - | assign,loose | 8 |  |
| `app.starting` | - | assign,loose | 4 |  |
| `app.stop.failed` | - | assign,loose | 4 |  |
| `app.stopped` | - | assign,loose | 8 |  |
| `app.stopping` | - | assign,loose | 4 |  |
| `app.uninstall.failed` | - | assign,loose | 4 |  |
| `app.uninstalled` | - | assign,loose | 9 |  |
| `app.uninstalling` | - | assign,loose | 5 |  |
| `app.update.failed` | - | assign,loose | 4 |  |
| `app.updated` | - | assign,loose | 8 |  |
| `app.updating` | - | assign,loose | 4 |  |
| `app.visibilitychange` | - | assign,loose | 4 |  |

## appStore

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appStore.updated` | - | assign,loose | 4 |  |

## av01

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `av01.0.04M.08` | - | assign,loose | 4 |  |

## avc1

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `avc1.42e01e` | - | assign,loose | 5 | 是 |

## com

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `com.apple.quicktime.HLS` | - | assign,loose | 4 |  |

## dragError

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `dragError.cannotMoveDirectoryIntoItself` | - | assign,loose | 5 | 是 |
| `dragError.cannotMoveInCurrentDirectory` | - | assign,loose | 5 | 是 |
| `dragError.noFileSelectionToMove` | - | assign,loose | 5 | 是 |
| `dragError.notAllowMoveFileIntoRootDirectory` | - | assign,loose | 5 | 是 |
| `dragError.notAllowUploadFileAndDirectoriesIntoRootDirectory` | - | assign,loose | 5 | 是 |
| `dragError.notAllowUploadFileIntoRootDirectory` | - | assign,loose | 5 | 是 |
| `dragError.selectedIncludeTargetItself` | - | assign,loose | 5 | 是 |
| `dragError.targetPathError` | - | assign,loose | 5 | 是 |

## file

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `file.upload` | - | loose,assign | 6 |  |
| `file.uploadFiles` | - | loose,assign | 6 |  |

## format

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `format.date` | - | assign,loose | 4 |  |

## hvc1

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `hvc1.1.6.L120.90` | - | assign,loose | 4 |  |

## net

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `net.ovs` | - | assign,loose | 4 |  |
| `net.set` | - | assign,loose | 4 |  |

## org

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `org.id3` | - | assign,loose | 4 |  |

## player

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `player.txt` | - | assign,loose | 4 |  |

## remote

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `remote.upload` | - | assign,loose | 4 |  |

## storage

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `storage.change` | - | assign,loose | 4 |  |

## team

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `team.other` | - | assign,loose | 4 |  |
| `team.quota` | - | assign,loose | 4 |  |
| `team.trashbin` | - | assign,loose | 4 |  |

## trim

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `trim.account` | - | assign,loose | 5 |  |
| `trim.ai` | - | assign,loose | 4 |  |
| `trim.assistance` | - | assign,loose | 4 |  |
| `trim.docker` | - | assign,loose | 4 |  |
| `trim.preview` | - | assign,loose | 5 |  |
| `trim.setting` | - | assign,loose | 4 |  |
| `trim.snapshots` | - | assign,loose | 5 |  |
| `trim.vm` | - | assign,loose | 4 |  |

## user

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `user.quota` | - | assign,loose | 4 |  |
| `user.trashbin` | - | assign,loose | 4 |  |

# unverified（3279）


## about

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `about.appName` | - | loose | 2 | 是 |
| `about.companyName` | - | loose | 1 | 是 |
| `about.copyright` | - | loose | 1 | 是 |
| `about.currentVersion` | - | loose | 1 | 是 |

## account

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `account.changePassword` | - | loose | 1 | 是 |
| `account.disable` | - | loose | 1 | 是 |
| `account.edit` | - | loose | 1 | 是 |
| `account.enableNow` | - | loose | 1 | 是 |
| `account.logoutSuccess` | - | loose | 1 | 是 |
| `account.modify` | - | loose | 2 | 是 |
| `account.modifyEmail` | - | loose | 1 | 是 |
| `account.password` | - | loose | 1 | 是 |
| `account.secureEmail` | - | loose | 1 | 是 |
| `account.secureEmailDescription` | - | loose | 1 | 是 |
| `account.setupNow` | - | loose | 1 | 是 |
| `account.trustDeviceManagement` | - | loose | 1 | 是 |
| `account.twoFactorAuth` | - | loose | 1 | 是 |
| `account.twoFactorAuthActiveTime` | - | loose | 1 | 是 |
| `account.twoFactorAuthDescription` | - | loose | 1 | 是 |
| `account.updateTime` | - | loose | 1 | 是 |
| `account.userDescription` | - | loose | 1 | 是 |

## action

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `action.addShortcutToDesktop` | - | loose | 1 | 是 |
| `action.cancelFavorite` | - | loose | 2 | 是 |
| `action.completelyDelete` | - | loose | 2 | 是 |
| `action.compress` | - | loose | 1 | 是 |
| `action.copy` | - | loose | 1 | 是 |
| `action.copyTo` | - | loose | 3 | 是 |
| `action.copyToAndMoveTo` | - | loose | 1 | 是 |
| `action.cut` | - | loose | 1 | 是 |
| `action.delete` | - | loose | 1 | 是 |
| `action.diskInfo` | - | loose | 1 | 是 |
| `action.download` | - | loose | 1 | 是 |
| `action.empty` | - | loose | 3 | 是 |
| `action.emptyRecentRecord` | - | loose | 1 | 是 |
| `action.extract` | - | loose | 1 | 是 |
| `action.favorite` | - | loose | 1 | 是 |
| `action.fileCollection` | - | loose | 1 | 是 |
| `action.info` | - | loose | 1 | 是 |
| `action.linkCopy` | - | loose | 2 | 是 |
| `action.linkDel` | - | loose | 1 | 是 |
| `action.linkEdit` | - | loose | 1 | 是 |
| `action.linkFileView` | - | loose | 1 | 是 |
| `action.manageDefaultOpenWith` | - | loose | 2 | 是 |
| `action.move` | - | loose | 1 | 是 |
| `action.moveTo` | - | loose | 3 | 是 |
| `action.newFolder` | - | loose | 2 | 是 |
| `action.newWindow` | - | loose | 1 | 是 |
| `action.open` | - | loose | 1 | 是 |
| `action.openFolder` | - | loose | 1 | 是 |
| `action.openWith` | - | loose | 2 | 是 |
| `action.paste` | - | loose | 1 | 是 |
| `action.refresh` | - | loose | 1 | 是 |
| `action.remoteConnect` | - | loose | 1 | 是 |
| `action.remoteDisconnect` | - | loose | 1 | 是 |
| `action.remoteEdit` | - | loose | 1 | 是 |
| `action.remoteRemove` | - | loose | 1 | 是 |
| `action.removeRecentRecord` | - | loose | 1 | 是 |
| `action.rename` | - | loose | 1 | 是 |
| `action.restore` | - | loose | 2 | 是 |
| `action.searchAppForExt` | - | loose | 2 | 是 |
| `action.share` | - | loose | 1 | 是 |
| `action.shareLink` | - | loose | 1 | 是 |
| `action.shareSettings` | - | loose | 1 | 是 |
| `action.storageInfo` | - | loose | 1 | 是 |
| `action.teamSettings` | - | loose | 1 | 是 |
| `action.teamSettingsPerm` | - | loose | 1 | 是 |
| `action.trash` | - | loose | 1 | 是 |
| `action.umount` | - | loose | 1 | 是 |
| `action.uploadFile` | - | loose | 2 | 是 |
| `action.uploadFolder` | - | loose | 2 | 是 |

## actions

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `actions.confirmStop` | - | loose | 1 | 是 |
| `actions.confirmUninstall` | - | loose | 1 | 是 |
| `actions.createBackupTask` | - | loose | 1 | 是 |
| `actions.install` | - | loose | 1 | 是 |
| `actions.installing` | - | loose | 1 | 是 |
| `actions.open` | - | loose | 1 | 是 |
| `actions.start` | - | loose | 1 | 是 |
| `actions.starting` | - | loose | 1 | 是 |
| `actions.stop` | - | loose | 1 | 是 |
| `actions.stopping` | - | loose | 1 | 是 |
| `actions.uninstall` | - | loose | 1 | 是 |
| `actions.uninstalling` | - | loose | 1 | 是 |
| `actions.upgrade` | - | loose | 1 | 是 |
| `actions.upgrading` | - | loose | 1 | 是 |

## additional

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `additional.thumbnail.sUrl` | - | loose | 1 |  |
| `additional.thumbnail.xxsUrl` | - | loose | 1 |  |

## admin

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `admin.adminView` | - | loose | 2 | 是 |
| `admin.setting` | - | loose | 1 | 是 |

## album

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `album.addPhotos` | - | loose | 1 | 是 |
| `album.addedTime` | - | loose | 2 | 是 |
| `album.albumEmpty` | - | loose | 1 | 是 |
| `album.albumNotFound` | - | loose | 1 | 是 |
| `album.albumSettings` | - | loose | 3 | 是 |
| `album.babyAge.birthday` | - | loose | 1 | 是 |
| `album.babyAge.birthdayWithYears` | - | loose | 1 | 是 |
| `album.babyAge.born` | - | loose | 1 | 是 |
| `album.babyAge.dayNumber` | - | loose | 1 | 是 |
| `album.babyAge.days` | - | loose | 1 | 是 |
| `album.babyAge.hundredDays` | - | loose | 1 | 是 |
| `album.babyAge.months` | - | loose | 1 | 是 |
| `album.babyAge.oneMonth` | - | loose | 1 | 是 |
| `album.babyAge.underOneYear` | - | loose | 2 | 是 |
| `album.babyAge.years` | - | loose | 3 | 是 |
| `album.babyAlbum` | - | loose | 1 | 是 |
| `album.birthday` | - | loose | 1 | 是 |
| `album.canAdd` | - | loose | 1 | 是 |
| `album.canView` | - | loose | 1 | 是 |
| `album.changeCover` | - | loose | 2 | 是 |
| `album.clickToEditName` | - | loose | 1 | 是 |
| `album.contentNotExist` | - | loose | 1 | 是 |
| `album.coverSetSuccess` | - | loose | 2 | 是 |
| `album.createFailed` | - | loose | 1 | 是 |
| `album.createSuccess` | - | loose | 1 | 是 |
| `album.deleteAlbum` | - | loose | 4 | 是 |
| `album.deleteAlbumConfirm` | - | loose | 2 | 是 |
| `album.deleteSuccess` | - | loose | 2 | 是 |
| `album.downloadAll` | - | loose | 2 | 是 |
| `album.editShareSettings` | - | loose | 1 | 是 |
| `album.enterAlbumName` | - | loose | 1 | 是 |
| `album.enterBabyName` | - | loose | 1 | 是 |
| `album.externalLinkManagement` | - | loose | 1 | 是 |
| `album.fillBabyBirthday` | - | loose | 2 | 是 |
| `album.itemCount` | - | loose | 1 | 是 |
| `album.itemsAdded` | - | loose | 1 | 是 |
| `album.noContent` | - | loose | 2 | 是 |
| `album.noPermission` | - | loose | 2 | 是 |
| `album.operationFailed` | - | loose | 2 | 是 |
| `album.owner` | - | loose | 1 | 是 |
| `album.photosCount` | - | loose | 1 | 是 |
| `album.public` | - | loose | 1 |  |
| `album.saveFailed` | - | loose | 1 | 是 |
| `album.selectAlbumView` | - | loose | 1 | 是 |
| `album.selectBabyBirthday` | - | loose | 1 | 是 |
| `album.share` | - | loose | 1 | 是 |
| `album.shared` | - | loose | 1 | 是 |
| `album.shootingTime` | - | loose | 3 | 是 |
| `album.specified` | - | loose | 1 |  |
| `album.unnamedAlbum` | - | loose | 3 | 是 |
| `album.unnamedBaby` | - | loose | 2 | 是 |
| `album.userGroup` | - | loose | 1 | 是 |
| `album.videosCount` | - | loose | 1 | 是 |

## app

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `app.account` | - | loose | 1 | 是 |
| `app.ai` | - | loose | 1 | 是 |
| `app.allFileManager` | - | loose | 1 | 是 |
| `app.appStore` | - | loose | 1 | 是 |
| `app.assistance` | - | loose | 1 | 是 |
| `app.backupAndSync` | - | loose | 1 | 是 |
| `app.docker` | - | loose | 1 | 是 |
| `app.downloadCenter` | - | loose | 1 | 是 |
| `app.fileManager` | - | loose | 1 | 是 |
| `app.fileManagerSetting` | - | loose | 1 | 是 |
| `app.logCenter` | - | loose | 1 | 是 |
| `app.mediaCenter` | - | loose | 1 | 是 |
| `app.photos` | - | loose | 1 | 是 |
| `app.recycleBin` | - | loose | 1 | 是 |
| `app.resourceManager` | - | loose | 1 | 是 |
| `app.setting` | - | loose | 1 | 是 |
| `app.status` | `status` | alias_key,loose | 2 |  |
| `app.system` | - | loose | 1 | 是 |

## appAccess

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appAccess.mySettingsTitle` | - | loose | 1 | 是 |
| `appAccess.noData` | - | loose | 1 |  |
| `appAccess.noSearchResult` | - | loose | 1 |  |
| `appAccess.searchPlaceholder` | - | loose | 1 | 是 |
| `appAccess.title` | - | loose | 1 | 是 |

## appApiErrors

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appApiErrors.LoginExpired` | - | loose | 1 | 是 |
| `appApiErrors.Unknown` | - | loose | 2 | 是 |
| `appApiErrors.UnknownNetworkError` | - | loose | 1 | 是 |

## appDetail

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appDetail.appSettings` | - | loose | 1 | 是 |
| `appDetail.currentVersion` | - | loose | 1 | 是 |
| `appDetail.developer` | - | loose | 1 | 是 |
| `appDetail.downloads` | - | loose | 1 | 是 |
| `appDetail.installLocation` | - | loose | 1 | 是 |
| `appDetail.introduction` | - | loose | 1 | 是 |
| `appDetail.latestVersion` | - | loose | 1 | 是 |
| `appDetail.learnMore` | - | loose | 1 | 是 |
| `appDetail.manualInstall` | - | loose | 1 | 是 |
| `appDetail.publisher` | - | loose | 1 | 是 |
| `appDetail.securityAlert` | - | loose | 1 | 是 |
| `appDetail.size` | - | loose | 1 | 是 |
| `appDetail.source` | - | loose | 1 | 是 |
| `appDetail.storageSpace` | - | loose | 1 | 是 |
| `appDetail.systemPartition` | - | loose | 1 | 是 |

## appShareFiles

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appShareFiles.searchPlaceholder` | - | loose | 1 | 是 |

## appcgi.updatemgr

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `appcgi.updatemgr.v1` | - | loose | 1 |  |

## application

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `application.appAccount` | - | loose | 1 | 是 |
| `application.authorizationPath.add` | - | loose | 1 | 是 |
| `application.authorizationPath.deleteConfirmContent` | - | loose | 1 | 是 |
| `application.authorizationPath.deleteConfirmTitle` | - | loose | 1 | 是 |
| `application.authorizationPath.empty` | - | loose | 1 | 是 |
| `application.authorizationPath.externalStoragePermissionError` | - | loose | 1 | 是 |
| `application.authorizationPath.folder` | - | loose | 1 | 是 |
| `application.authorizationPath.getPermissionFailed` | - | loose | 1 | 是 |
| `application.authorizationPath.mountPointNotConnected` | - | loose | 1 | 是 |
| `application.authorizationPath.noAccess` | - | loose | 1 | 是 |
| `application.authorizationPath.owner` | - | loose | 1 | 是 |
| `application.authorizationPath.readOnly` | - | loose | 2 | 是 |
| `application.authorizationPath.readWrite` | - | loose | 1 | 是 |
| `application.authorizationPath.status.appPermissionDeleted` | - | loose | 1 | 是 |
| `application.authorizationPath.status.appPermissionError` | - | loose | 1 | 是 |
| `application.authorizationPath.status.pathInaccessible` | - | loose | 1 | 是 |
| `application.authorizationPath.status.pathNotFound` | - | loose | 1 | 是 |
| `application.authorizationPath.status.pathNotSupported` | - | loose | 1 | 是 |
| `application.authorizationPath.title` | - | loose | 2 | 是 |
| `application.authorizationPath.writeOnly` | - | loose | 1 | 是 |
| `application.errors.deviceBoundToOtherAccount` | - | loose | 1 | 是 |
| `application.errors.deviceNotBound` | - | loose | 1 | 是 |
| `application.errors.deviceRegisterFailed` | - | loose | 1 | 是 |
| `application.errors.getDeviceIdFailed` | - | loose | 1 | 是 |
| `application.errors.invalidRequest` | - | loose | 1 | 是 |
| `application.errors.loginExpired` | - | loose | 1 | 是 |
| `application.errors.loginStatusExpired` | - | loose | 1 | 是 |
| `application.errors.networkError` | - | loose | 2 | 是 |
| `application.errors.noPermission` | - | loose | 1 | 是 |
| `application.errors.serviceError` | - | loose | 1 | 是 |
| `application.errors.verificationCodeError` | - | loose | 1 | 是 |
| `application.errors.verificationCodeTooFrequent` | - | loose | 1 | 是 |
| `application.modifyFailed` | - | loose | 2 | 是 |
| `application.pickFolder.title` | - | loose | 1 | 是 |

## archive

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `archive.button.cancel` | - | loose | 1 | 是 |
| `archive.button.save` | - | loose | 1 | 是 |
| `archive.condition.description` | - | loose | 1 | 是 |
| `archive.condition.logSizeGreaterThan` | - | loose | 1 | 是 |
| `archive.condition.logTimeBefore` | - | loose | 1 | 是 |
| `archive.condition.selectSize` | - | loose | 1 | 是 |
| `archive.condition.selectTime` | - | loose | 1 | 是 |
| `archive.condition.title` | - | loose | 1 | 是 |
| `archive.error.archiveFolderNotAvailable` | - | loose | 1 | 是 |
| `archive.error.archiveFolderNotExisting` | - | loose | 1 | 是 |
| `archive.error.archiveFolderNotWritable` | - | loose | 1 | 是 |
| `archive.error.exportFileOpenFailed` | - | loose | 1 | 是 |
| `archive.error.failed` | - | loose | 2 | 是 |
| `archive.error.noSpace` | - | loose | 1 | 是 |
| `archive.error.noStoragePool` | - | loose | 1 | 是 |
| `archive.error.pathNotExist` | - | loose | 1 | 是 |
| `archive.error.pathRequired` | - | loose | 2 | 是 |
| `archive.error.serviceError` | - | loose | 2 | 是 |
| `archive.error.success` | - | loose | 1 | 是 |
| `archive.loading.loading` | - | loose | 1 |  |
| `archive.loading.submitting` | - | loose | 1 |  |
| `archive.saveLocation.placeholder` | - | loose | 2 | 是 |
| `archive.saveLocation.title` | - | loose | 1 | 是 |
| `archive.time.oneMonthAgo` | - | loose | 2 | 是 |
| `archive.time.oneYearAgo` | - | loose | 2 | 是 |
| `archive.time.sixMonthsAgo` | - | loose | 2 | 是 |
| `archive.time.threeMonthsAgo` | - | loose | 2 | 是 |
| `archive.title` | - | loose | 1 | 是 |

## arrowProps

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `arrowProps.leftArrow.children` | - | loose | 2 |  |
| `arrowProps.leftArrow.props` | - | loose | 1 |  |
| `arrowProps.rightArrow.children` | - | loose | 2 |  |
| `arrowProps.rightArrow.props` | - | loose | 1 |  |

## attributes

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `attributes.role.value` | - | loose | 2 |  |

## auth

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `auth.authFailed` | - | loose | 1 | 是 |
| `auth.authFeedBackFailed` | - | loose | 1 | 是 |
| `auth.authFeedBackSuccess` | - | loose | 1 | 是 |
| `auth.authReAuth` | - | loose | 2 | 是 |
| `auth.authUpdating` | - | loose | 1 | 是 |
| `auth.errors.failed` | - | loose | 2 | 是 |
| `auth.errors.reAuthFailed` | - | loose | 1 | 是 |

## authorizeFile

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `authorizeFile.errors.folderPathRequired` | - | loose | 1 | 是 |
| `authorizeFile.errors.pathInvalid` | - | loose | 1 | 是 |
| `authorizeFile.errors.pathRequired` | - | loose | 1 | 是 |
| `authorizeFile.location` | - | loose | 1 | 是 |
| `authorizeFile.requestFileAccess` | - | loose | 1 | 是 |

## authorizedDevices

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `authorizedDevices.authorizedAt` | - | loose | 1 | 是 |
| `authorizedDevices.close` | - | loose | 2 | 是 |
| `authorizedDevices.deviceTypes.agent` | - | loose | 1 |  |
| `authorizedDevices.deviceTypes.browser` | - | loose | 1 |  |
| `authorizedDevices.deviceTypes.mobile` | - | loose | 1 |  |
| `authorizedDevices.deviceTypes.pc` | - | loose | 1 |  |
| `authorizedDevices.edit` | - | loose | 1 | 是 |
| `authorizedDevices.editFailure` | - | loose | 1 | 是 |
| `authorizedDevices.editSuccess` | - | loose | 1 | 是 |
| `authorizedDevices.editTitle` | - | loose | 1 | 是 |
| `authorizedDevices.empty` | - | loose | 1 | 是 |
| `authorizedDevices.howToAuthorize` | - | loose | 1 | 是 |
| `authorizedDevices.moreActions` | - | loose | 1 | 是 |
| `authorizedDevices.revoke` | - | loose | 1 | 是 |
| `authorizedDevices.revokeConfirm.content` | - | loose | 1 | 是 |
| `authorizedDevices.revokeConfirm.title` | - | loose | 1 | 是 |
| `authorizedDevices.revokeFailure` | - | loose | 1 | 是 |
| `authorizedDevices.revokeSuccess` | - | loose | 1 | 是 |
| `authorizedDevices.scope` | - | loose | 1 | 是 |
| `authorizedDevices.scopeLabel` | - | loose | 1 | 是 |
| `authorizedDevices.scopeLabels.eventSubscribe` | - | loose | 1 | 是 |
| `authorizedDevices.scopeLabels.fileRead` | - | loose | 1 | 是 |
| `authorizedDevices.scopeLabels.fileWrite` | - | loose | 1 | 是 |
| `authorizedDevices.scopeLabels.photoRead` | - | loose | 1 | 是 |
| `authorizedDevices.scopeLabels.trimAppCenterAll` | - | loose | 1 | 是 |
| `authorizedDevices.scopeLabels.trimBaiduNetdiskAll` | - | loose | 1 | 是 |
| `authorizedDevices.scopeLabels.trimBasic` | - | loose | 1 | 是 |
| `authorizedDevices.scopeLabels.trimDockerAll` | - | loose | 1 | 是 |
| `authorizedDevices.scopeLabels.trimDownloadAll` | - | loose | 1 | 是 |
| `authorizedDevices.scopeLabels.trimFilePath` | - | loose | 1 | 是 |
| `authorizedDevices.scopeLabels.trimFileRead` | - | loose | 1 | 是 |
| `authorizedDevices.scopeLabels.trimFileSharedAccess` | - | loose | 1 | 是 |
| `authorizedDevices.scopeLabels.trimFileUserAccess` | - | loose | 1 | 是 |
| `authorizedDevices.scopeLabels.trimFileUserAcl` | - | loose | 1 | 是 |
| `authorizedDevices.scopeLabels.trimFileWrite` | - | loose | 1 | 是 |
| `authorizedDevices.scopeLabels.trimLogAll` | - | loose | 1 | 是 |
| `authorizedDevices.scopeLabels.trimPhotoAll` | - | loose | 1 | 是 |
| `authorizedDevices.scopeLabels.trimStorageAll` | - | loose | 1 | 是 |
| `authorizedDevices.scopeLabels.trimSystemAll` | - | loose | 1 | 是 |
| `authorizedDevices.scopeLabels.trimSystemPlatformConfig` | - | loose | 1 | 是 |
| `authorizedDevices.scopeLabels.trimUserAll` | - | loose | 1 | 是 |
| `authorizedDevices.scopeSummaryMore` | - | loose | 1 | 是 |
| `authorizedDevices.scopeTooltip` | - | loose | 1 | 是 |
| `authorizedDevices.scopeUnknown` | - | loose | 1 | 是 |
| `authorizedDevices.title` | - | loose | 1 | 是 |

## av01

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `av01.0.01M.08` | - | loose | 1 |  |

## avc1

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `avc1.42E01E` | - | loose | 1 |  |

## backupIconLabel

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `backupIconLabel.aliPan` | - | loose | 1 | 是 |
| `backupIconLabel.anotherNas` | - | loose | 1 | 是 |
| `backupIconLabel.baiduPan` | - | loose | 1 | 是 |
| `backupIconLabel.dropbox` | - | loose | 1 | 是 |
| `backupIconLabel.external` | - | loose | 1 | 是 |
| `backupIconLabel.ftp` | - | loose | 1 | 是 |
| `backupIconLabel.googleDrive` | - | loose | 1 | 是 |
| `backupIconLabel.myNas` | - | loose | 1 | 是 |
| `backupIconLabel.oneDrive` | - | loose | 1 | 是 |
| `backupIconLabel.sftp` | - | loose | 1 | 是 |
| `backupIconLabel.smb` | - | loose | 1 | 是 |
| `backupIconLabel.webdav` | - | loose | 1 | 是 |

## backupLogDialog

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `backupLogDialog.actionType.cleanup` | - | loose | 1 | 是 |
| `backupLogDialog.actionType.download` | - | loose | 1 | 是 |
| `backupLogDialog.actionType.upload` | - | loose | 1 | 是 |
| `backupLogDialog.errorCode.fileCancelled` | - | loose | 1 | 是 |
| `backupLogDialog.errorCode.fileCloudError` | - | loose | 1 | 是 |
| `backupLogDialog.errorCode.fileCreateDirFailed` | - | loose | 1 | 是 |
| `backupLogDialog.errorCode.fileDecryptFailed` | - | loose | 1 | 是 |
| `backupLogDialog.errorCode.fileDuplicatedEntry` | - | loose | 1 | 是 |
| `backupLogDialog.errorCode.fileEncryptFailed` | - | loose | 1 | 是 |
| `backupLogDialog.errorCode.fileIgnored` | - | loose | 1 | 是 |
| `backupLogDialog.errorCode.fileInsufficientSpace` | - | loose | 1 | 是 |
| `backupLogDialog.errorCode.fileInvalidPath` | - | loose | 1 | 是 |
| `backupLogDialog.errorCode.fileListFailed` | - | loose | 1 | 是 |
| `backupLogDialog.errorCode.fileNoDirectory` | - | loose | 1 | 是 |
| `backupLogDialog.errorCode.fileNoSpace` | - | loose | 1 | 是 |
| `backupLogDialog.errorCode.fileOpenFailed` | - | loose | 1 | 是 |
| `backupLogDialog.errorCode.fileOpenTargetFailed` | - | loose | 1 | 是 |
| `backupLogDialog.errorCode.filePasswordError` | - | loose | 1 | 是 |
| `backupLogDialog.errorCode.fileReadFailed` | - | loose | 1 | 是 |
| `backupLogDialog.errorCode.fileRemoteDisconnected` | - | loose | 1 | 是 |
| `backupLogDialog.errorCode.fileRemoveSourceFailed` | - | loose | 1 | 是 |
| `backupLogDialog.errorCode.fileSizeExceed` | - | loose | 1 | 是 |
| `backupLogDialog.errorCode.fileVerifyingError` | - | loose | 1 | 是 |
| `backupLogDialog.errorCode.fileWriteTargetFailed` | - | loose | 1 | 是 |
| `backupLogDialog.errorCode.unknownError` | - | loose | 3 | 是 |
| `backupLogDialog.table.actionType` | - | loose | 1 | 是 |
| `backupLogDialog.table.errorMessage` | - | loose | 1 | 是 |
| `backupLogDialog.table.file` | - | loose | 1 | 是 |
| `backupLogDialog.table.startTime` | - | loose | 1 | 是 |
| `backupLogDialog.title` | - | loose | 1 | 是 |

## backupOperationsDialog

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `backupOperationsDialog.table.endTime` | - | loose | 1 | 是 |
| `backupOperationsDialog.table.excludedFiles` | - | loose | 1 | 是 |
| `backupOperationsDialog.table.startTime` | - | loose | 1 | 是 |
| `backupOperationsDialog.table.status` | - | loose | 1 | 是 |
| `backupOperationsDialog.table.totalFiles` | - | loose | 1 | 是 |
| `backupOperationsDialog.table.transferredFiles` | - | loose | 1 | 是 |
| `backupOperationsDialog.table.transferredSize` | - | loose | 1 | 是 |
| `backupOperationsDialog.title` | - | loose | 1 | 是 |
| `backupOperationsDialog.viewDetails` | - | loose | 1 | 是 |

## backupSourceDialog

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `backupSourceDialog.noPermission` | - | loose | 1 | 是 |
| `backupSourceDialog.table.actions` | - | loose | 1 | 是 |
| `backupSourceDialog.table.index` | - | loose | 1 | 是 |
| `backupSourceDialog.table.source` | - | loose | 2 | 是 |
| `backupSourceDialog.title` | - | loose | 1 | 是 |
| `backupSourceDialog.viewInStorage` | - | loose | 1 | 是 |

## backupSourcePathFormatter

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `backupSourcePathFormatter.myFiles` | - | loose | 1 | 是 |

## backupTaskPlan

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `backupTaskPlan.manual` | - | loose | 1 | 是 |
| `backupTaskPlan.monthOptionsLastDay` | - | loose | 2 | 是 |
| `backupTaskPlan.monthOptionsSuffix` | - | loose | 2 | 是 |
| `backupTaskPlan.optionsPlaceholder` | - | loose | 2 | 是 |
| `backupTaskPlan.periodOptions.0` | - | loose | 3 | 是 |
| `backupTaskPlan.periodOptions.1` | - | loose | 1 | 是 |
| `backupTaskPlan.periodOptions.2` | - | loose | 2 | 是 |
| `backupTaskPlan.periodPrefix` | - | loose | 1 | 是 |
| `backupTaskPlan.planLabels.backupEndTime` | - | loose | 1 | 是 |
| `backupTaskPlan.planLabels.executeDay` | - | loose | 1 | 是 |
| `backupTaskPlan.planLabels.firstBackupTime` | - | loose | 1 | 是 |
| `backupTaskPlan.planLabels.repeatFrequency` | - | loose | 1 | 是 |
| `backupTaskPlan.planLabels.timeError` | - | loose | 1 | 是 |
| `backupTaskPlan.planType.manual` | - | loose | 1 | 是 |
| `backupTaskPlan.planType.regular` | - | loose | 1 | 是 |
| `backupTaskPlan.regular` | - | loose | 1 | 是 |
| `backupTaskPlan.repeatHoursOnly` | - | loose | 1 | 是 |
| `backupTaskPlan.repeatMinutes` | - | loose | 1 | 是 |

## beginnerGuide

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `beginnerGuide.completeTips` | - | loose | 1 | 是 |
| `beginnerGuide.dynamicInstallation.downloadFailedTips` | - | loose | 1 | 是 |
| `beginnerGuide.dynamicInstallation.install` | - | loose | 1 |  |
| `beginnerGuide.dynamicInstallation.installFailedTips` | - | loose | 1 | 是 |
| `beginnerGuide.dynamicInstallation.installSuccessTips` | - | loose | 1 | 是 |
| `beginnerGuide.dynamicInstallation.installed` | - | loose | 1 |  |
| `beginnerGuide.dynamicInstallation.insufficientCapacityTips` | - | loose | 1 | 是 |
| `beginnerGuide.dynamicInstallation.noStorageTips` | - | loose | 1 | 是 |
| `beginnerGuide.dynamicInstallation.placeholder` | - | loose | 1 | 是 |
| `beginnerGuide.dynamicInstallation.selectStorageTips` | - | loose | 1 | 是 |
| `beginnerGuide.itemConfig.account.buttonProps.doneLabel` | - | loose | 1 | 是 |
| `beginnerGuide.itemConfig.account.buttonProps.label` | - | loose | 1 | 是 |
| `beginnerGuide.itemConfig.account.description` | - | loose | 1 | 是 |
| `beginnerGuide.itemConfig.account.title` | - | loose | 1 | 是 |
| `beginnerGuide.itemConfig.account.trimMachineDescription` | - | loose | 1 | 是 |
| `beginnerGuide.itemConfig.email.buttonProps.doneLabel` | - | loose | 1 | 是 |
| `beginnerGuide.itemConfig.email.buttonProps.label` | - | loose | 1 | 是 |
| `beginnerGuide.itemConfig.email.description` | - | loose | 1 | 是 |
| `beginnerGuide.itemConfig.email.title` | - | loose | 1 | 是 |
| `beginnerGuide.itemConfig.fnConnect.buttonProps.doneLabel` | - | loose | 1 | 是 |
| `beginnerGuide.itemConfig.fnConnect.buttonProps.label` | - | loose | 1 | 是 |
| `beginnerGuide.itemConfig.fnConnect.buttonProps.trimMachineLabel` | - | loose | 1 | 是 |
| `beginnerGuide.itemConfig.fnConnect.description` | - | loose | 1 | 是 |
| `beginnerGuide.itemConfig.fnConnect.title` | - | loose | 1 | 是 |
| `beginnerGuide.itemConfig.fnConnect.trimMachineDescription` | - | loose | 1 | 是 |
| `beginnerGuide.itemConfig.media.buttonProps.doneLabel` | - | loose | 1 | 是 |
| `beginnerGuide.itemConfig.media.description` | - | loose | 1 | 是 |
| `beginnerGuide.itemConfig.media.title` | - | loose | 1 | 是 |
| `beginnerGuide.itemConfig.photos.buttonProps.doneLabel` | - | loose | 1 | 是 |
| `beginnerGuide.itemConfig.photos.description` | - | loose | 1 | 是 |
| `beginnerGuide.itemConfig.photos.title` | - | loose | 1 | 是 |
| `beginnerGuide.itemConfig.storage.buttonProps.doneLabel` | - | loose | 1 | 是 |
| `beginnerGuide.itemConfig.storage.buttonProps.label` | - | loose | 1 | 是 |
| `beginnerGuide.itemConfig.storage.description` | - | loose | 1 | 是 |
| `beginnerGuide.itemConfig.storage.title` | - | loose | 1 | 是 |
| `beginnerGuide.skipGuide.label` | - | loose | 1 | 是 |
| `beginnerGuide.skipGuide.leaveTips` | - | loose | 1 | 是 |
| `beginnerGuide.storage.sizeLabel` | - | loose | 1 | 是 |
| `beginnerGuide.storage.state.broken` | - | loose | 1 | 是 |
| `beginnerGuide.storage.state.readOnly` | - | loose | 1 | 是 |
| `beginnerGuide.storage.state.removed` | - | loose | 1 | 是 |
| `beginnerGuide.storage.state.unready` | - | loose | 1 | 是 |
| `beginnerGuide.storage.unknown` | - | loose | 1 | 是 |
| `beginnerGuide.title` | - | loose | 1 | 是 |

## bin

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `bin.details.bytes` | - | loose | 1 | 是 |
| `bin.details.calculatingSimple` | - | loose | 2 | 是 |
| `bin.details.fileCount` | - | loose | 1 | 是 |
| `bin.info` | - | loose | 1 | 是 |
| `bin.owner` | - | loose | 1 | 是 |
| `bin.queryDetailsFailed` | - | loose | 1 | 是 |
| `bin.size` | - | loose | 1 | 是 |
| `bin.totalContains` | - | loose | 1 | 是 |

## body

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `body.cell` | - | loose | 2 |  |
| `body.outer` | - | loose | 1 |  |
| `body.wrapper` | - | loose | 1 |  |

## browser

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `browser.desktopWidget` | `name` | alias_key,loose | 4 |  |
| `browser.desktopWidgetWinOpen` | `name` | alias_key,loose | 4 |  |
| `browser.namesakeConf` | - | loose | 1 |  |

## cell

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `cell.getContext` | - | loose | 1 |  |

## colgroup

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `colgroup.col` | - | loose | 1 |  |
| `colgroup.wrapper` | - | loose | 1 |  |

## column

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `column.getFlatColumns` | - | loose | 1 |  |
| `column.getLeafColumns` | - | loose | 1 |  |

## com

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `com.apple.hls.interstitial` | - | loose | 1 |  |
| `com.apple.streaming.transportStreamTimestamp` | - | loose | 1 |  |
| `com.douban.frodo` | - | loose | 1 | 是 |

## common

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `common.admin` | - | loose | 2 | 是 |
| `common.adminOnlyOperation` | - | loose | 2 | 是 |
| `common.allow` | - | loose | 1 | 是 |
| `common.backToHome` | - | loose | 2 | 是 |
| `common.cancel` | - | loose | 23 | 是 |
| `common.checkDetail` | - | loose | 2 | 是 |
| `common.close` | - | loose | 1 | 是 |
| `common.comingSoon` | - | loose | 3 | 是 |
| `common.confirm` | - | loose | 7 | 是 |
| `common.decrypt` | - | loose | 1 |  |
| `common.disabled` | - | loose | 2 | 是 |
| `common.enabled` | - | loose | 1 |  |
| `common.encrypt` | - | loose | 1 |  |
| `common.errorOccurred` | - | loose | 1 | 是 |
| `common.fileOrFolderNotExist` | - | loose | 1 | 是 |
| `common.goToSettings` | - | loose | 1 | 是 |
| `common.insufficientPermission` | - | loose | 1 | 是 |
| `common.know` | - | loose | 11 | 是 |
| `common.loading` | - | loose | 3 | 是 |
| `common.loadingFiles` | - | loose | 1 | 是 |
| `common.more` | - | loose | 1 | 是 |
| `common.noData` | - | loose | 1 |  |
| `common.noSearchResult` | - | loose | 1 |  |
| `common.ok` | - | loose | 7 | 是 |
| `common.owner` | - | loose | 1 | 是 |
| `common.pageNotFound` | - | loose | 1 | 是 |
| `common.refresh` | - | loose | 1 | 是 |
| `common.reset` | - | loose | 1 | 是 |
| `common.retry` | - | loose | 1 | 是 |
| `common.search` | - | loose | 3 | 是 |
| `common.sessionExpired` | - | loose | 1 | 是 |
| `common.switchingLanguageOrTimezone` | - | loose | 1 | 是 |
| `common.unknown` | - | loose | 3 | 是 |

## compConnectedDeviceCard

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `compConnectedDeviceCard.deleteStorageLocationBtnTitle` | - | loose | 1 | 是 |

## compDeviceIcon

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `compDeviceIcon.addOther` | - | loose | 1 | 是 |

## compExtensionsSettings

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `compExtensionsSettings.errors.duplicateExtension` | - | loose | 1 | 是 |
| `compExtensionsSettings.errors.emptyExtension` | - | loose | 1 | 是 |
| `compExtensionsSettings.errors.emptyExtensionList` | - | loose | 1 | 是 |
| `compExtensionsSettings.errors.invalidExtension` | - | loose | 1 | 是 |
| `compExtensionsSettings.form.addBtnTitle` | - | loose | 1 | 是 |
| `compExtensionsSettings.form.extension.placeholder` | - | loose | 1 | 是 |
| `compExtensionsSettings.list.custom` | - | loose | 1 | 是 |
| `compExtensionsSettings.list.temp` | - | loose | 1 | 是 |
| `compExtensionsSettings.removeBtnTitle` | - | loose | 1 | 是 |

## compFormWidgets

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `compFormWidgets.sizeRangeInput.maxPrefix` | - | loose | 1 | 是 |
| `compFormWidgets.sizeRangeInput.minPrefix` | - | loose | 1 | 是 |
| `compFormWidgets.sizeRangeInput.placeholder` | - | loose | 1 | 是 |
| `compFormWidgets.sizeRangeInput.suffix` | - | loose | 1 | 是 |

## compMiniDeviceCard

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `compMiniDeviceCard.itemsSuffix` | - | loose | 1 | 是 |
| `compMiniDeviceCard.localSuffix` | - | loose | 1 | 是 |

## components

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `components.appErrorRender.networkError` | - | loose | 2 | 是 |
| `components.appErrorRender.networkErrorRetry` | - | loose | 1 | 是 |
| `components.appErrorRender.reload` | - | loose | 1 | 是 |
| `components.appPlaceHolder.developing` | - | loose | 1 | 是 |
| `components.dataContainer.empty` | - | loose | 1 | 是 |
| `components.dataContainer.loadFailed` | - | loose | 1 | 是 |
| `components.dataContainer.refresh` | - | loose | 1 | 是 |
| `components.detailsWidgets.copyOriginalPath` | - | loose | 1 | 是 |
| `components.detailsWidgets.copyOriginalPathSuccess` | - | loose | 1 | 是 |
| `components.errorBoundary.errorMessage` | - | loose | 1 | 是 |
| `components.errorBoundary.retry` | - | loose | 1 | 是 |
| `components.fileSharingProtocol.needModifyRegistry` | - | loose | 1 | 是 |
| `components.footer.item` | - | loose | 7 | 是 |
| `components.footer.selectedTotalText` | - | loose | 8 | 是 |
| `components.footer.sharedToDeviceAccount` | - | loose | 1 | 是 |
| `components.footer.totalText` | - | loose | 9 | 是 |
| `components.header.clearHistory` | - | loose | 1 | 是 |
| `components.header.deleteHistory` | - | loose | 1 | 是 |
| `components.header.navigation` | - | loose | 1 | 是 |
| `components.header.searchHistory` | - | loose | 1 | 是 |
| `components.header.searchIn` | `i18nKey` | alias_key,loose | 2 |  |
| `components.i18n.itemCountLabel.label` | `i18nKey` | alias_key,loose | 2 |  |
| `components.i18n.itemCountLabel.title` | - | loose | 1 | 是 |
| `components.pageStatus.empty` | - | loose | 1 | 是 |
| `components.pageStatus.loadFailed` | `i18nKey` | alias_key,loose | 2 |  |
| `components.pathInput.cannotAccessPath` | - | loose | 1 | 是 |
| `components.pathInput.pathNotExist` | - | loose | 1 | 是 |
| `components.selectAll` | - | loose | 1 | 是 |
| `components.selectStorage.available` | - | loose | 2 | 是 |
| `components.selectStorage.placeholder` | - | loose | 1 | 是 |
| `components.selectStorage.systemPartition` | - | loose | 1 | 是 |
| `components.showMore.showMore` | - | loose | 1 | 是 |
| `components.textClipboard.copy` | - | loose | 1 | 是 |
| `components.toastMessage.copySuccess` | - | loose | 1 | 是 |
| `components.updatableAppCard.latestVersion` | - | loose | 1 | 是 |
| `components.updatableAppCard.publishTime` | - | loose | 1 | 是 |
| `components.updatableAppCard.update` | - | loose | 1 | 是 |

## conditionalAlbum

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `conditionalAlbum.addFailedFileNotFound` | - | loose | 1 | 是 |
| `conditionalAlbum.addFolder` | - | loose | 2 | 是 |
| `conditionalAlbum.addPerson` | - | loose | 4 | 是 |
| `conditionalAlbum.addPhotos` | - | loose | 1 | 是 |
| `conditionalAlbum.addTag` | - | loose | 2 | 是 |
| `conditionalAlbum.albumCreateFailed` | - | loose | 1 | 是 |
| `conditionalAlbum.albumName` | - | loose | 1 | 是 |
| `conditionalAlbum.albumSettings` | - | loose | 3 | 是 |
| `conditionalAlbum.albumType` | - | loose | 1 | 是 |
| `conditionalAlbum.albumView` | - | loose | 1 | 是 |
| `conditionalAlbum.autoAddPhotos` | - | loose | 1 | 是 |
| `conditionalAlbum.babyAlbum` | - | loose | 1 | 是 |
| `conditionalAlbum.babyBirthday` | - | loose | 1 | 是 |
| `conditionalAlbum.babyName` | - | loose | 1 | 是 |
| `conditionalAlbum.conditionDescription` | - | loose | 2 | 是 |
| `conditionalAlbum.createSuccess` | - | loose | 1 | 是 |
| `conditionalAlbum.deleteFolder` | - | loose | 1 | 是 |
| `conditionalAlbum.deletePerson` | - | loose | 1 | 是 |
| `conditionalAlbum.folder` | - | loose | 2 | 是 |
| `conditionalAlbum.hideHiddenPersons` | - | loose | 1 |  |
| `conditionalAlbum.itemCount` | - | loose | 2 | 是 |
| `conditionalAlbum.keep` | - | loose | 1 | 是 |
| `conditionalAlbum.noData` | - | loose | 1 | 是 |
| `conditionalAlbum.normalAlbum` | - | loose | 1 | 是 |
| `conditionalAlbum.person` | - | loose | 2 | 是 |
| `conditionalAlbum.personNotFound` | - | loose | 1 | 是 |
| `conditionalAlbum.pleaseEnterBabyBirthday` | - | loose | 1 | 是 |
| `conditionalAlbum.remove` | - | loose | 1 | 是 |
| `conditionalAlbum.removePhotosConfirmContent` | - | loose | 1 | 是 |
| `conditionalAlbum.removePhotosConfirmTitle` | - | loose | 1 | 是 |
| `conditionalAlbum.saveFailed` | - | loose | 3 | 是 |
| `conditionalAlbum.saveSuccess` | - | loose | 3 | 是 |
| `conditionalAlbum.search` | - | loose | 1 | 是 |
| `conditionalAlbum.setConditions` | - | loose | 1 | 是 |
| `conditionalAlbum.setConditionsDescription` | - | loose | 1 | 是 |
| `conditionalAlbum.showHiddenPersons` | - | loose | 1 |  |
| `conditionalAlbum.tag` | - | loose | 2 | 是 |
| `conditionalAlbum.tiled` | - | loose | 2 | 是 |
| `conditionalAlbum.timeline` | - | loose | 2 | 是 |

## config

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `config.overrideDefaultProps.Spin.indicator` | - | loose | 1 |  |

## confirm

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `confirm.confirm` | - | loose | 2 | 是 |
| `confirm.dataVolumeUnavailable` | - | loose | 2 | 是 |
| `confirm.developer` | - | loose | 1 | 是 |
| `confirm.enableAfterInstall` | - | loose | 1 |  |
| `confirm.enableAfterUpdate` | - | loose | 1 |  |
| `confirm.features` | - | loose | 1 | 是 |
| `confirm.install` | - | loose | 1 |  |
| `confirm.installFailed` | - | loose | 4 | 是 |
| `confirm.introduction` | - | loose | 1 | 是 |
| `confirm.location` | - | loose | 1 | 是 |
| `confirm.publishTime` | - | loose | 1 | 是 |
| `confirm.publisher` | - | loose | 1 | 是 |
| `confirm.storageSpace` | - | loose | 1 | 是 |
| `confirm.systemPartition` | - | loose | 1 | 是 |
| `confirm.title` | - | loose | 1 | 是 |
| `confirm.update` | - | loose | 1 |  |
| `confirm.version` | - | loose | 1 | 是 |
| `confirm.volumeUnavailable` | - | loose | 2 | 是 |

## cryptDialog

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `cryptDialog.decrypt.label` | - | loose | 1 | 是 |
| `cryptDialog.decrypt.title` | - | loose | 1 | 是 |
| `cryptDialog.decrypt.tooltip` | - | loose | 1 | 是 |
| `cryptDialog.encrypt.label` | - | loose | 1 | 是 |
| `cryptDialog.encrypt.title` | - | loose | 1 | 是 |
| `cryptDialog.encrypt.tooltip` | - | loose | 1 | 是 |
| `cryptDialog.encryptionTipsTitle` | - | loose | 1 | 是 |
| `cryptDialog.error.fieldErrors.passwordError` | - | loose | 3 | 是 |
| `cryptDialog.error.fieldErrors.passwordNotMatch` | - | loose | 1 | 是 |
| `cryptDialog.form.common.enterPassword` | - | loose | 2 | 是 |
| `cryptDialog.form.common.passwordLengthError` | - | loose | 2 | 是 |
| `cryptDialog.form.common.specialCharacters` | - | loose | 1 | 是 |
| `cryptDialog.form.confirmPassword.label` | - | loose | 1 | 是 |
| `cryptDialog.form.confirmPassword.placeholder` | - | loose | 1 | 是 |
| `cryptDialog.form.password.label` | - | loose | 1 | 是 |
| `cryptDialog.form.password.placeholder` | - | loose | 1 | 是 |

## date

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `date.day` | - | loose | 2 | 是 |
| `date.format.daysHours` | - | loose | 1 | 是 |
| `date.format.hoursMinutes` | - | loose | 1 | 是 |
| `date.format.minutes` | - | loose | 1 | 是 |
| `date.format.seconds` | - | loose | 1 | 是 |
| `date.hour` | - | loose | 2 | 是 |
| `date.minute` | - | loose | 2 | 是 |
| `date.second` | - | loose | 2 | 是 |

## dependentApps

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `dependentApps.title` | - | loose | 1 | 是 |

## desktop

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `desktop.addFailed` | - | loose | 1 | 是 |
| `desktop.addSuccess` | - | loose | 1 | 是 |
| `desktop.addToGroupFailed` | - | loose | 1 | 是 |
| `desktop.appEntryNotFound` | - | loose | 1 | 是 |
| `desktop.changeThemeWallpaper` | - | loose | 1 | 是 |
| `desktop.createFolderFailed` | - | loose | 1 | 是 |
| `desktop.createGroupFailed` | - | loose | 2 | 是 |
| `desktop.hideAppIcon` | - | loose | 4 | 是 |
| `desktop.licenseWatermark.activate` | - | loose | 1 | 是 |
| `desktop.licenseWatermark.path` | - | loose | 1 | 是 |
| `desktop.manageApp` | - | loose | 1 | 是 |
| `desktop.moveIconFailed` | - | loose | 1 | 是 |
| `desktop.newFolder` | - | loose | 1 | 是 |
| `desktop.newGroup` | - | loose | 5 | 是 |
| `desktop.removeFailed` | - | loose | 1 | 是 |
| `desktop.removeFromDesktopFailed` | - | loose | 1 | 是 |
| `desktop.removeFromGroupFailed` | - | loose | 2 | 是 |
| `desktop.removeSuccess` | - | loose | 4 | 是 |
| `desktop.rename` | - | loose | 4 | 是 |
| `desktop.renameFailed` | - | loose | 1 | 是 |
| `desktop.renameModal.nameRequired` | - | loose | 1 | 是 |
| `desktop.renameModal.placeholder` | - | loose | 1 | 是 |
| `desktop.renameSuccess` | - | loose | 3 | 是 |
| `desktop.showAppIcon` | - | loose | 1 |  |
| `desktop.sortFailed` | - | loose | 1 | 是 |
| `desktop.sortGroupFailed` | - | loose | 1 | 是 |

## device

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `device.added` | - | loose | 1 | 是 |
| `device.pcSync` | - | loose | 1 | 是 |
| `device.removed` | - | loose | 1 | 是 |
| `device.unknown` | - | loose | 1 | 是 |
| `device.unknownDevice` | - | loose | 2 | 是 |

## deviceCardDescription

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `deviceCardDescription.local` | - | loose | 1 | 是 |
| `deviceCardDescription.storageSize` | - | loose | 1 | 是 |

## deviceDefaultName

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `deviceDefaultName.aliPan` | - | loose | 1 | 是 |
| `deviceDefaultName.anotherNas` | - | loose | 1 | 是 |
| `deviceDefaultName.baiduPan` | - | loose | 1 | 是 |
| `deviceDefaultName.dropbox` | - | loose | 1 | 是 |
| `deviceDefaultName.external` | - | loose | 1 | 是 |
| `deviceDefaultName.ftp` | - | loose | 1 | 是 |
| `deviceDefaultName.googleDrive` | - | loose | 1 | 是 |
| `deviceDefaultName.myNas` | - | loose | 1 | 是 |
| `deviceDefaultName.oneDrive` | - | loose | 1 | 是 |
| `deviceDefaultName.sftp` | - | loose | 1 | 是 |
| `deviceDefaultName.smb` | - | loose | 1 | 是 |
| `deviceDefaultName.webdav` | - | loose | 1 | 是 |

## disconnectModal

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `disconnectModal.disconnected` | - | loose | 1 | 是 |
| `disconnectModal.refresh` | - | loose | 2 | 是 |

## domains

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `domains.acl.actions.add` | - | loose | 1 | 是 |
| `domains.acl.actions.addPermission` | - | loose | 1 |  |
| `domains.acl.actions.delete` | - | loose | 1 | 是 |
| `domains.acl.actions.edit` | - | loose | 1 | 是 |
| `domains.acl.actions.editPermission` | - | loose | 2 | 是 |
| `domains.acl.actions.remove` | - | loose | 2 | 是 |
| `domains.acl.actions.view` | - | loose | 2 | 是 |
| `domains.acl.actions.viewPermission` | - | loose | 1 |  |
| `domains.acl.advanced.advanced` | - | loose | 1 | 是 |
| `domains.acl.advanced.convertInheritToExplicit` | - | loose | 1 | 是 |
| `domains.acl.advanced.disableParentInherit` | - | loose | 1 | 是 |
| `domains.acl.advanced.enableParentInherit` | - | loose | 1 | 是 |
| `domains.acl.advanced.removeAllInherit` | - | loose | 1 | 是 |
| `domains.acl.advanced.resetSubPermission` | - | loose | 2 | 是 |
| `domains.acl.advanced.resetSubPermissionDesc` | - | loose | 1 | 是 |
| `domains.acl.advanced.resetSubPermissionEditedNote` | - | loose | 1 | 是 |
| `domains.acl.common.allow` | - | loose | 3 | 是 |
| `domains.acl.common.cancel` | - | loose | 1 | 是 |
| `domains.acl.common.confirm` | - | loose | 1 | 是 |
| `domains.acl.common.custom` | - | loose | 8 | 是 |
| `domains.acl.common.deny` | - | loose | 3 | 是 |
| `domains.acl.common.denyAccess` | - | loose | 6 | 是 |
| `domains.acl.common.fullControl` | - | loose | 3 | 是 |
| `domains.acl.common.gotIt` | - | loose | 1 | 是 |
| `domains.acl.common.inheritFrom` | - | loose | 1 | 是 |
| `domains.acl.common.noPermission` | - | loose | 1 | 是 |
| `domains.acl.common.none` | - | loose | 1 | 是 |
| `domains.acl.common.read` | - | loose | 1 |  |
| `domains.acl.common.readOnly` | - | loose | 6 | 是 |
| `domains.acl.common.readWrite` | - | loose | 6 | 是 |
| `domains.acl.form.applyTo` | - | loose | 2 | 是 |
| `domains.acl.form.permissionScope` | - | loose | 1 | 是 |
| `domains.acl.inherit.allSubFiles` | - | loose | 2 | 是 |
| `domains.acl.inherit.allSubFolders` | - | loose | 2 | 是 |
| `domains.acl.inherit.allSubFoldersAndFiles` | - | loose | 2 | 是 |
| `domains.acl.inherit.firstLevelSubFiles` | - | loose | 2 | 是 |
| `domains.acl.inherit.firstLevelSubFolders` | - | loose | 2 | 是 |
| `domains.acl.inherit.firstLevelSubFoldersAndFiles` | - | loose | 2 | 是 |
| `domains.acl.inherit.propagateToAllSubLevels` | - | loose | 1 | 是 |
| `domains.acl.inherit.propagateToFirstLevelOnly` | - | loose | 1 | 是 |
| `domains.acl.inherit.subFiles` | - | loose | 1 | 是 |
| `domains.acl.inherit.subFolders` | - | loose | 1 | 是 |
| `domains.acl.inherit.subScope` | - | loose | 1 | 是 |
| `domains.acl.inherit.thisFolder` | - | loose | 5 | 是 |
| `domains.acl.inherit.thisFolderAndAllSubFiles` | - | loose | 2 | 是 |
| `domains.acl.inherit.thisFolderAndAllSubFolders` | - | loose | 2 | 是 |
| `domains.acl.inherit.thisFolderAndAllSubFoldersAndFiles` | - | loose | 2 | 是 |
| `domains.acl.inherit.thisFolderAndFirstLevelSubFiles` | - | loose | 2 | 是 |
| `domains.acl.inherit.thisFolderAndFirstLevelSubFolders` | - | loose | 2 | 是 |
| `domains.acl.inherit.thisFolderAndFirstLevelSubFoldersAndFiles` | - | loose | 2 | 是 |
| `domains.acl.messages.insufficientPermission` | - | loose | 1 |  |
| `domains.acl.messages.itemsFailed` | - | loose | 1 | 是 |
| `domains.acl.messages.modifyFailed` | - | loose | 2 | 是 |
| `domains.acl.messages.modifyPermissionLabel` | - | loose | 3 | 是 |
| `domains.acl.messages.modifyPermissionPartialFailed` | - | loose | 1 | 是 |
| `domains.acl.messages.noPermission` | - | loose | 1 |  |
| `domains.acl.messages.noSearchResult` | - | loose | 1 | 是 |
| `domains.acl.messages.resetSubPermissionSuccess` | - | loose | 1 | 是 |
| `domains.acl.messages.updateSuccess` | - | loose | 1 | 是 |
| `domains.acl.notify.bullets.exportBeforeConvert` | - | loose | 1 | 是 |
| `domains.acl.notify.bullets.safeConversion` | - | loose | 1 | 是 |
| `domains.acl.notify.cancelText` | - | loose | 1 | 是 |
| `domains.acl.notify.description` | - | loose | 1 | 是 |
| `domains.acl.notify.helpText` | - | loose | 1 | 是 |
| `domains.acl.notify.intro` | - | loose | 1 | 是 |
| `domains.acl.notify.okText` | - | loose | 1 | 是 |
| `domains.acl.notify.postpone.followUp` | - | loose | 1 | 是 |
| `domains.acl.notify.postpone.intro` | - | loose | 1 | 是 |
| `domains.acl.notify.postpone.okText` | - | loose | 1 | 是 |
| `domains.acl.notify.postpone.risks.newPermissionLost` | - | loose | 1 | 是 |
| `domains.acl.notify.postpone.risks.permissionInvalid` | - | loose | 1 | 是 |
| `domains.acl.notify.postpone.risks.restoreSnapshotPermissionAbnormal` | - | loose | 1 | 是 |
| `domains.acl.notify.postpone.title` | - | loose | 1 | 是 |
| `domains.acl.notify.postpone.toast` | - | loose | 1 | 是 |
| `domains.acl.notify.title` | - | loose | 1 | 是 |
| `domains.acl.permTree.admin` | - | loose | 2 | 是 |
| `domains.acl.permTree.changePermission` | - | loose | 2 | 是 |
| `domains.acl.permTree.createFileWriteData` | - | loose | 2 | 是 |
| `domains.acl.permTree.createFolderAppendData` | - | loose | 2 | 是 |
| `domains.acl.permTree.deleteSelf` | - | loose | 2 | 是 |
| `domains.acl.permTree.deleteSubFoldersAndFiles` | - | loose | 2 | 是 |
| `domains.acl.permTree.listFolderReadData` | - | loose | 2 | 是 |
| `domains.acl.permTree.read` | - | loose | 2 | 是 |
| `domains.acl.permTree.readAttributes` | - | loose | 2 | 是 |
| `domains.acl.permTree.readExtendedAttributes` | - | loose | 2 | 是 |
| `domains.acl.permTree.readPermissions` | - | loose | 2 | 是 |
| `domains.acl.permTree.takeOwnership` | - | loose | 2 | 是 |
| `domains.acl.permTree.traverseFolderExecuteFile` | - | loose | 2 | 是 |
| `domains.acl.permTree.write` | - | loose | 2 | 是 |
| `domains.acl.permTree.writeAttributes` | - | loose | 2 | 是 |
| `domains.acl.permTree.writeExtendedAttributes` | - | loose | 2 | 是 |
| `domains.acl.quickPerm.readOnlyComment` | - | loose | 1 | 是 |
| `domains.acl.quickPerm.readWriteComment` | - | loose | 1 | 是 |
| `domains.acl.subject.advanced` | - | loose | 1 | 是 |
| `domains.acl.subject.app` | - | loose | 1 | 是 |
| `domains.acl.subject.everyoneDescription` | - | loose | 2 | 是 |
| `domains.acl.subject.group` | - | loose | 1 | 是 |
| `domains.acl.subject.label` | - | loose | 2 | 是 |
| `domains.acl.subject.noApp` | - | loose | 1 | 是 |
| `domains.acl.subject.ownerDescription` | - | loose | 2 | 是 |
| `domains.acl.subject.user` | - | loose | 1 | 是 |
| `domains.acl.subject.userGroupApp` | - | loose | 2 | 是 |
| `domains.acl.table.action` | - | loose | 1 | 是 |
| `domains.acl.table.inheritFromParent` | - | loose | 3 | 是 |
| `domains.acl.table.notSet` | - | loose | 1 | 是 |
| `domains.acl.table.permission` | - | loose | 3 | 是 |
| `domains.acl.table.permissionPreview` | - | loose | 1 | 是 |
| `domains.acl.table.type` | - | loose | 1 | 是 |
| `domains.acl.validation.selectPermissionApplyScope` | - | loose | 1 | 是 |
| `domains.acl.validation.selectPermissionScope` | - | loose | 1 | 是 |
| `domains.acl.validation.selectUserGroupApp` | - | loose | 1 | 是 |
| `domains.license.limit.appCenter.content` | - | loose | 1 | 是 |
| `domains.license.limit.appCenter.okText` | - | loose | 1 | 是 |
| `domains.license.limit.appCenter.title` | - | loose | 1 | 是 |
| `domains.license.limit.disk.addDisk` | - | loose | 1 | 是 |
| `domains.license.limit.disk.contentWithLicense` | - | loose | 1 | 是 |
| `domains.license.limit.disk.contentWithoutLicense` | - | loose | 1 | 是 |
| `domains.license.limit.disk.createStorage` | - | loose | 1 | 是 |
| `domains.license.limit.disk.modifyStorageMode` | - | loose | 1 | 是 |
| `domains.license.limit.disk.mountStorage` | - | loose | 1 | 是 |
| `domains.license.limit.modal.cancelText` | - | loose | 1 | 是 |
| `domains.license.limit.modal.okText` | - | loose | 1 | 是 |
| `domains.license.limit.user.contentWithLicense` | - | loose | 1 | 是 |
| `domains.license.limit.user.contentWithoutLicense` | - | loose | 1 | 是 |
| `domains.license.limit.user.createUser` | - | loose | 1 | 是 |
| `domains.license.limit.user.enableUser` | - | loose | 1 | 是 |

## download

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `download.manualInstall` | - | loose | 1 |  |
| `download.title` | - | loose | 1 |  |
| `download.uploading` | - | loose | 2 | 是 |

## dragError

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `dragError.continue` | - | loose | 1 | 是 |
| `dragError.folderAlreadyExists` | - | loose | 1 | 是 |
| `dragError.tipsTitle` | - | loose | 2 | 是 |
| `dragError.uploadFailed` | - | loose | 1 | 是 |
| `dragError.uploadSuccess` | - | loose | 1 | 是 |

## emptyFolder

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `emptyFolder.dragFileHere` | - | loose | 1 |  |
| `emptyFolder.dragFolderHere` | - | loose | 1 |  |
| `emptyFolder.or` | - | loose | 1 | 是 |
| `emptyFolder.teamEmpty` | - | loose | 1 | 是 |

## env

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `env.NODE_ENV` | - | loose | 5 |  |

## equipmentManagement

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `equipmentManagement.connectedDevices` | - | loose | 1 | 是 |
| `equipmentManagement.currentDevice` | - | loose | 1 | 是 |
| `equipmentManagement.loggedInDevices` | - | loose | 1 | 是 |
| `equipmentManagement.loginAt` | - | loose | 1 | 是 |
| `equipmentManagement.logout` | - | loose | 1 | 是 |
| `equipmentManagement.logoutConfirm.content` | - | loose | 1 | 是 |
| `equipmentManagement.logoutConfirm.title` | - | loose | 1 | 是 |
| `equipmentManagement.logoutFailure` | - | loose | 1 | 是 |
| `equipmentManagement.logoutSuccess` | - | loose | 1 | 是 |
| `equipmentManagement.unknownDevice` | - | loose | 1 | 是 |

## error

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `error.E_LOG_OPEN_DIR_FAILED` | - | loose | 1 | 是 |
| `error.clearFailed` | - | loose | 1 | 是 |
| `error.clearSuccess` | - | loose | 1 | 是 |
| `error.default` | - | loose | 3 | 是 |
| `error.exportFailed` | - | loose | 1 | 是 |
| `error.fetchFailed` | - | loose | 1 | 是 |
| `error.loginExpired` | - | loose | 1 | 是 |

## errors

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `errors.assistanceAccountCreated` | - | loose | 1 | 是 |
| `errors.assistanceGroupCreated` | - | loose | 1 | 是 |
| `errors.cannotInstallOrStart` | - | loose | 1 | 是 |
| `errors.cannotInstallVersion` | - | loose | 1 | 是 |
| `errors.cannotStop` | - | loose | 1 | 是 |
| `errors.cannotUpdateVersion` | - | loose | 1 | 是 |
| `errors.closeAssistanceFailed` | - | loose | 1 | 是 |
| `errors.currentOsVersionNotSupported` | - | loose | 2 | 是 |
| `errors.dockerNotInitialized` | - | loose | 1 | 是 |
| `errors.downloadFailed` | - | loose | 3 | 是 |
| `errors.enableSSH` | - | loose | 2 | 是 |
| `errors.getInstallInfoFailed` | - | loose | 1 | 是 |
| `errors.getUninstallInfoFailed` | - | loose | 2 | 是 |
| `errors.install.beforeInstall` | - | loose | 2 | 是 |
| `errors.install.beforeInstallErrorTitle` | - | loose | 1 |  |
| `errors.install.dependencyVersionNotMatch` | - | loose | 2 | 是 |
| `errors.install.dependencyVersionNotMatch2` | - | loose | 2 | 是 |
| `errors.install.osVersionAbove` | - | loose | 2 | 是 |
| `errors.install.osVersionBelow` | - | loose | 2 | 是 |
| `errors.install.osVersionNotMatch` | - | loose | 2 | 是 |
| `errors.install.willInstall` | - | loose | 2 |  |
| `errors.install.willInstallApps` | - | loose | 1 |  |
| `errors.install.willStartApps` | - | loose | 1 |  |
| `errors.installFailed` | - | loose | 2 | 是 |
| `errors.missingDependencies` | - | loose | 2 | 是 |
| `errors.needUpgradeOs` | - | loose | 1 | 是 |
| `errors.openAssistanceFailed` | - | loose | 2 | 是 |
| `errors.outputText.install` | - | loose | 1 | 是 |
| `errors.outputText.start` | - | loose | 1 | 是 |
| `errors.outputText.stop` | - | loose | 1 | 是 |
| `errors.outputText.uninstall` | - | loose | 1 | 是 |
| `errors.outputText.upgrade` | - | loose | 1 | 是 |
| `errors.packageExceptionContent` | - | loose | 1 | 是 |
| `errors.start.beforeStartErrorTitle` | - | loose | 1 | 是 |
| `errors.start.packageExceptionTitle` | - | loose | 1 | 是 |
| `errors.start.riskControl.confirm` | - | loose | 1 | 是 |
| `errors.start.riskControl.content` | - | loose | 1 | 是 |
| `errors.start.riskControl.learnMore` | - | loose | 1 | 是 |
| `errors.start.riskControl.title` | - | loose | 1 | 是 |
| `errors.start.willInstallApps` | - | loose | 1 | 是 |
| `errors.start.willStart` | - | loose | 2 | 是 |
| `errors.start.willStartApps` | - | loose | 1 | 是 |
| `errors.startFailed` | - | loose | 3 | 是 |
| `errors.stop.packageExceptionTitle` | - | loose | 1 | 是 |
| `errors.stop.willStop` | - | loose | 1 | 是 |
| `errors.stop.willStopAppsTip` | - | loose | 1 | 是 |
| `errors.stopFailed` | - | loose | 5 | 是 |
| `errors.taskFailed` | - | loose | 3 | 是 |
| `errors.uninstall.willUninstall` | - | loose | 1 | 是 |
| `errors.uninstall.willUninstallApps` | - | loose | 1 | 是 |
| `errors.uninstallFailed` | - | loose | 1 | 是 |
| `errors.upgrade.beforeUpgrade` | - | loose | 1 |  |
| `errors.upgrade.beforeUpgradeErrorTitle` | - | loose | 1 |  |
| `errors.upgrade.willStartApps` | - | loose | 1 |  |
| `errors.upgrade.willUpgrade` | - | loose | 3 | 是 |
| `errors.upgrade.willUpgradeApps` | - | loose | 1 |  |
| `errors.upgrade.willUpgradeCanUseTip` | - | loose | 1 | 是 |
| `errors.upgrade.willUpgradeNoMatchAppTip` | - | loose | 1 | 是 |
| `errors.upgrade.willUpgradeNoMatchTip` | - | loose | 1 | 是 |

## event

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `event.subscribe` | - | loose | 1 |  |
| `event.target` | - | loose | 1 | 是 |

## exportAssistanceForm

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `exportAssistanceForm.outputDirField.label` | - | loose | 1 | 是 |
| `exportAssistanceForm.outputDirField.placeholder` | - | loose | 1 | 是 |
| `exportAssistanceForm.outputDirField.required` | - | loose | 2 | 是 |
| `exportAssistanceForm.srvType.app` | - | loose | 1 | 是 |
| `exportAssistanceForm.srvType.service` | - | loose | 1 | 是 |
| `exportAssistanceForm.srvType.system` | - | loose | 1 | 是 |
| `exportAssistanceForm.srvTypeField.label` | - | loose | 1 | 是 |
| `exportAssistanceForm.srvTypeField.placeholder` | - | loose | 1 | 是 |
| `exportAssistanceForm.srvTypeField.required` | - | loose | 1 | 是 |

## exportAssistanceTask

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `exportAssistanceTask.doing.cancelText` | - | loose | 1 | 是 |
| `exportAssistanceTask.doing.content` | - | loose | 1 | 是 |
| `exportAssistanceTask.doing.okText` | - | loose | 1 | 是 |
| `exportAssistanceTask.doing.title` | - | loose | 1 | 是 |
| `exportAssistanceTask.failed.content` | - | loose | 1 | 是 |
| `exportAssistanceTask.failed.okText` | - | loose | 1 | 是 |
| `exportAssistanceTask.failed.title` | - | loose | 1 | 是 |
| `exportAssistanceTask.start.cancelText` | - | loose | 1 | 是 |
| `exportAssistanceTask.start.content` | - | loose | 1 | 是 |
| `exportAssistanceTask.start.okText` | - | loose | 1 | 是 |
| `exportAssistanceTask.start.title` | - | loose | 1 | 是 |
| `exportAssistanceTask.success.cancelText` | - | loose | 1 | 是 |
| `exportAssistanceTask.success.content` | - | loose | 1 | 是 |
| `exportAssistanceTask.success.okText` | - | loose | 1 | 是 |
| `exportAssistanceTask.success.title` | - | loose | 1 | 是 |

## externalAuth

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `externalAuth.adminOnlyTip` | - | loose | 1 | 是 |
| `externalAuth.allUser` | - | loose | 1 | 是 |
| `externalAuth.onlyAdmin` | - | loose | 1 | 是 |
| `externalAuth.onlyUserVisible` | - | loose | 1 | 是 |
| `externalAuth.setFailed` | - | loose | 2 | 是 |
| `externalAuth.setSuccess` | - | loose | 1 | 是 |
| `externalAuth.title` | - | loose | 1 | 是 |

## externalStorage

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `externalStorage.action.hardDiskManage` | - | loose | 1 | 是 |
| `externalStorage.device.builtIn` | - | loose | 1 | 是 |
| `externalStorage.eject.cancel` | - | loose | 1 | 是 |
| `externalStorage.eject.confirm` | - | loose | 1 | 是 |
| `externalStorage.eject.confirmContent` | - | loose | 1 |  |
| `externalStorage.eject.confirmContentPartition` | - | loose | 1 |  |
| `externalStorage.eject.confirmTitle` | - | loose | 1 | 是 |
| `externalStorage.eject.failed` | - | loose | 1 | 是 |
| `externalStorage.eject.success` | - | loose | 1 | 是 |
| `externalStorage.noData.default` | - | loose | 1 |  |
| `externalStorage.noData.removed` | - | loose | 1 | 是 |
| `externalStorage.noData.search` | - | loose | 1 |  |
| `externalStorage.searchDevicePlaceholder` | - | loose | 1 | 是 |
| `externalStorage.searchPlaceholder` | - | loose | 1 | 是 |

## features

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `features.publishTime` | - | loose | 1 | 是 |
| `features.title` | - | loose | 1 | 是 |
| `features.version` | - | loose | 1 | 是 |

## field

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `field.btim` | - | loose | 12 | 是 |
| `field.datetime` | - | loose | 3 | 是 |
| `field.linkName` | - | loose | 3 | 是 |
| `field.location` | - | loose | 8 | 是 |
| `field.moreFields` | - | loose | 3 | 是 |
| `field.mtim` | - | loose | 17 | 是 |
| `field.name` | - | loose | 25 | 是 |
| `field.oriName` | - | loose | 1 | 是 |
| `field.oriPath` | - | loose | 4 | 是 |
| `field.owner` | - | loose | 16 | 是 |
| `field.path` | - | loose | 4 | 是 |
| `field.pathName` | - | loose | 2 | 是 |
| `field.rmTime` | - | loose | 4 | 是 |
| `field.size` | - | loose | 20 | 是 |
| `field.type` | - | loose | 23 | 是 |
| `field.username` | - | loose | 5 | 是 |
| `field.v` | - | loose | 6 | 是 |

## file

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `file.download.failed` | - | loose | 1 | 是 |
| `file.download.filesCount` | - | loose | 1 | 是 |
| `file.download.noPermission` | - | loose | 1 | 是 |
| `file.download.noPermissionWithPath` | - | loose | 1 | 是 |
| `file.extension.title` | - | loose | 2 | 是 |
| `file.extension.torrent` | - | loose | 1 | 是 |
| `file.external` | - | loose | 2 | 是 |
| `file.favorites` | - | loose | 2 | 是 |
| `file.fileNameTooLong` | - | loose | 2 | 是 |
| `file.fileSpecialCharacters` | - | loose | 2 | 是 |
| `file.folder` | - | loose | 1 | 是 |
| `file.folderNameTooLong` | - | loose | 2 | 是 |
| `file.folderSpecialCharacters` | - | loose | 2 | 是 |
| `file.invalidFileName` | - | loose | 2 | 是 |
| `file.invalidFolderName` | - | loose | 2 | 是 |
| `file.myFile` | - | loose | 3 | 是 |
| `file.otherShare` | - | loose | 2 | 是 |
| `file.pleaseEnterFileName` | - | loose | 2 | 是 |
| `file.pleaseEnterFolderName` | - | loose | 2 | 是 |
| `file.read` | - | loose | 1 |  |
| `file.remote` | - | loose | 2 | 是 |
| `file.search` | - | loose | 1 |  |
| `file.size` | `size` | alias_key,loose | 2 |  |
| `file.storageName` | - | loose | 4 | 是 |
| `file.team` | - | loose | 3 | 是 |
| `file.upload.cancel` | - | loose | 4 | 是 |
| `file.upload.failed` | - | loose | 5 | 是 |
| `file.upload.failedFileNameConflictWithDirectory` | - | loose | 1 | 是 |
| `file.upload.failedInvalidUploadPath` | - | loose | 1 | 是 |
| `file.upload.failedPathLengthExceeded` | - | loose | 1 | 是 |
| `file.upload.failedPermissionDenied` | - | loose | 1 | 是 |
| `file.upload.failedQuotaExceeded` | - | loose | 1 | 是 |
| `file.upload.failedServerIOError` | - | loose | 1 | 是 |
| `file.upload.failedServerInternalError` | - | loose | 1 | 是 |
| `file.upload.failedStorageSpaceNotEnough` | - | loose | 1 | 是 |
| `file.upload.failedTokenServerError` | - | loose | 1 | 是 |
| `file.upload.requestTimeout` | - | loose | 1 | 是 |
| `file.userFiles` | - | loose | 3 | 是 |
| `file.userShareFiles` | - | loose | 6 | 是 |
| `file.userShareFilesAugmented` | `i18nKey` | alias_key,loose | 2 |  |
| `file.write` | - | loose | 1 |  |

## fileDetails

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `fileDetails.allTypes` | - | loose | 1 | 是 |
| `fileDetails.calculatingCount` | - | loose | 2 | 是 |
| `fileDetails.calculatingSize` | - | loose | 3 | 是 |
| `fileDetails.copyOriginalPath` | - | loose | 1 | 是 |
| `fileDetails.copyOriginalPathSuccess` | - | loose | 1 | 是 |
| `fileDetails.createTime` | - | loose | 1 | 是 |
| `fileDetails.details` | - | loose | 1 | 是 |
| `fileDetails.duration` | - | loose | 1 | 是 |
| `fileDetails.exif` | - | loose | 1 |  |
| `fileDetails.exifMetadata.exposureProgram` | - | loose | 1 | 是 |
| `fileDetails.exifMetadata.exposureTime` | - | loose | 1 | 是 |
| `fileDetails.exifMetadata.fNumber` | - | loose | 1 | 是 |
| `fileDetails.exifMetadata.flash` | - | loose | 1 | 是 |
| `fileDetails.exifMetadata.focalLength` | - | loose | 1 | 是 |
| `fileDetails.exifMetadata.isoSpeedRatings` | - | loose | 1 | 是 |
| `fileDetails.exifMetadata.labels.exposureProgram.Manual` | - | loose | 1 | 是 |
| `fileDetails.exifMetadata.labels.flash.off` | - | loose | 1 | 是 |
| `fileDetails.exifMetadata.labels.flash.on` | - | loose | 1 | 是 |
| `fileDetails.exifMetadata.labels.meteringMode.Average` | - | loose | 1 | 是 |
| `fileDetails.exifMetadata.labels.meteringMode.Evaluative` | - | loose | 1 | 是 |
| `fileDetails.exifMetadata.labels.meteringMode.Other` | - | loose | 1 | 是 |
| `fileDetails.exifMetadata.labels.meteringMode.Partial` | - | loose | 1 | 是 |
| `fileDetails.exifMetadata.labels.meteringMode.Pattern` | - | loose | 1 | 是 |
| `fileDetails.exifMetadata.labels.meteringMode.Spot` | - | loose | 1 | 是 |
| `fileDetails.exifMetadata.labels.meteringMode.Unknown` | - | loose | 1 | 是 |
| `fileDetails.exifMetadata.make` | - | loose | 1 | 是 |
| `fileDetails.exifMetadata.meteringMode` | - | loose | 1 | 是 |
| `fileDetails.exifMetadata.model` | - | loose | 1 | 是 |
| `fileDetails.exifMetadata.title` | - | loose | 1 |  |
| `fileDetails.exifMetadata.unknown` | - | loose | 1 | 是 |
| `fileDetails.fileCountCalculationFailed` | - | loose | 2 | 是 |
| `fileDetails.fileSizeCalculationFailed` | - | loose | 3 | 是 |
| `fileDetails.fileType` | - | loose | 1 | 是 |
| `fileDetails.files` | - | loose | 2 | 是 |
| `fileDetails.filmingLocation` | - | loose | 1 | 是 |
| `fileDetails.filmingTime` | - | loose | 1 | 是 |
| `fileDetails.folder` | - | loose | 1 | 是 |
| `fileDetails.gettingInfo` | - | loose | 1 | 是 |
| `fileDetails.modifyTime` | - | loose | 1 | 是 |
| `fileDetails.moreInfo` | - | loose | 1 | 是 |
| `fileDetails.multipleTypes` | - | loose | 2 | 是 |
| `fileDetails.owner` | - | loose | 2 | 是 |
| `fileDetails.position` | - | loose | 1 | 是 |
| `fileDetails.resolution` | - | loose | 1 | 是 |
| `fileDetails.size` | - | loose | 2 | 是 |
| `fileDetails.spaceUsed` | - | loose | 2 | 是 |
| `fileDetails.teamSpace` | - | loose | 1 | 是 |
| `fileDetails.totalContains` | - | loose | 2 | 是 |
| `fileDetails.type` | - | loose | 2 | 是 |
| `fileDetails.unknown` | - | loose | 7 | 是 |
| `fileDetails.videoInfo` | - | loose | 1 |  |
| `fileDetails.videoMetadata.bitRate` | - | loose | 1 | 是 |
| `fileDetails.videoMetadata.channelLayout` | - | loose | 1 | 是 |
| `fileDetails.videoMetadata.channels` | - | loose | 1 | 是 |
| `fileDetails.videoMetadata.codecName` | - | loose | 1 | 是 |
| `fileDetails.videoMetadata.colorSpace` | - | loose | 1 | 是 |
| `fileDetails.videoMetadata.frameRate` | - | loose | 1 | 是 |
| `fileDetails.videoMetadata.labels.channelLayout.Mono` | - | loose | 1 | 是 |
| `fileDetails.videoMetadata.labels.channelLayout.Stereo` | - | loose | 1 | 是 |
| `fileDetails.videoMetadata.pixFmt` | - | loose | 1 | 是 |
| `fileDetails.videoMetadata.sampleRate` | - | loose | 1 | 是 |
| `fileDetails.videoMetadata.title` | - | loose | 1 |  |

## fileHandler

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `fileHandler.fileDetails.multipleItems` | - | loose | 1 | 是 |
| `fileHandler.fileDetails.title` | - | loose | 1 | 是 |
| `fileHandler.fileDetails.userFiles` | - | loose | 1 | 是 |
| `fileHandler.filePicker.pickFile.title` | - | loose | 1 |  |
| `fileHandler.filePicker.pickFolder.title` | - | loose | 1 |  |
| `fileHandler.newFolder.folder` | - | loose | 1 | 是 |
| `fileHandler.newFolder.title` | - | loose | 1 | 是 |
| `fileHandler.openFile.download` | - | loose | 1 | 是 |
| `fileHandler.openFile.noPermission` | - | loose | 4 | 是 |
| `fileHandler.openFile.notSupportedTip` | - | loose | 1 | 是 |
| `fileHandler.openFile.searchApp` | - | loose | 1 | 是 |
| `fileHandler.selectStorage.label` | - | loose | 1 | 是 |
| `fileHandler.selectStorage.title` | - | loose | 1 | 是 |

## filePicker

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `filePicker.selectFile` | - | loose | 1 |  |
| `filePicker.selectFolder` | - | loose | 1 |  |

## fileProtocolConnecterDialog

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `fileProtocolConnecterDialog.connectFailedMsg` | - | loose | 1 | 是 |
| `fileProtocolConnecterDialog.connectSuccessMsg` | - | loose | 1 | 是 |
| `fileProtocolConnecterDialog.emptyCancelTips` | - | loose | 1 | 是 |
| `fileProtocolConnecterDialog.title.disabled` | - | loose | 1 | 是 |
| `fileProtocolConnecterDialog.title.submitting` | - | loose | 1 | 是 |

## fileSharingProtocol

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `fileSharingProtocol.connectMode.hostname` | - | loose | 1 | 是 |
| `fileSharingProtocol.connectMode.ipAddress` | - | loose | 1 | 是 |
| `fileSharingProtocol.connectMode.macSteps.1` | - | loose | 1 | 是 |
| `fileSharingProtocol.connectMode.macSteps.2` | - | loose | 1 | 是 |
| `fileSharingProtocol.connectMode.macSteps.3` | - | loose | 1 | 是 |
| `fileSharingProtocol.connectMode.otherConnectionMethods` | - | loose | 2 | 是 |
| `fileSharingProtocol.connectMode.port` | - | loose | 1 | 是 |
| `fileSharingProtocol.connectMode.title` | - | loose | 1 | 是 |
| `fileSharingProtocol.connectMode.windowsFileSteps.1` | - | loose | 1 | 是 |
| `fileSharingProtocol.connectMode.windowsFileSteps.2` | - | loose | 1 | 是 |
| `fileSharingProtocol.connectMode.windowsNfsSteps.1` | - | loose | 1 | 是 |
| `fileSharingProtocol.connectMode.windowsNfsSteps.2` | - | loose | 1 | 是 |
| `fileSharingProtocol.connectMode.windowsNfsSteps.3` | - | loose | 1 | 是 |
| `fileSharingProtocol.connectMode.windowsNfsSteps.4` | - | loose | 1 | 是 |
| `fileSharingProtocol.connectMode.windowsWebdavSteps.1` | - | loose | 1 | 是 |
| `fileSharingProtocol.connectMode.windowsWebdavSteps.2` | - | loose | 1 | 是 |
| `fileSharingProtocol.connectMode.windowsWebdavSteps.3` | - | loose | 1 | 是 |
| `fileSharingProtocol.descriptions.dlna` | - | loose | 1 | 是 |
| `fileSharingProtocol.descriptions.ftp` | - | loose | 1 | 是 |
| `fileSharingProtocol.descriptions.nfs` | - | loose | 1 | 是 |
| `fileSharingProtocol.descriptions.smb` | - | loose | 1 | 是 |
| `fileSharingProtocol.descriptions.webdav` | - | loose | 1 | 是 |
| `fileSharingProtocol.directoryErrors.nameContainsSpecialChars` | - | loose | 1 | 是 |
| `fileSharingProtocol.directoryErrors.nameTooLong` | - | loose | 1 | 是 |
| `fileSharingProtocol.directoryErrors.noStorageSpace` | - | loose | 1 | 是 |
| `fileSharingProtocol.errors.unsupportedProtocol` | - | loose | 3 | 是 |
| `fileSharingProtocol.fileDel.appFile` | - | loose | 1 | 是 |
| `fileSharingProtocol.fileDel.appFileDesc` | - | loose | 1 | 是 |
| `fileSharingProtocol.fileDel.deletePermanently` | - | loose | 1 | 是 |
| `fileSharingProtocol.fileDel.description` | - | loose | 1 | 是 |
| `fileSharingProtocol.fileDel.externalStorageFile` | - | loose | 1 | 是 |
| `fileSharingProtocol.fileDel.externalStorageFileDesc` | - | loose | 1 | 是 |
| `fileSharingProtocol.fileDel.moveToTrash` | - | loose | 1 | 是 |
| `fileSharingProtocol.fileDel.remoteMountFile` | - | loose | 1 | 是 |
| `fileSharingProtocol.fileDel.remoteMountFileDesc` | - | loose | 1 | 是 |
| `fileSharingProtocol.fileDel.storageFile` | - | loose | 1 | 是 |
| `fileSharingProtocol.fileDel.storageInsufficientError` | - | loose | 1 | 是 |
| `fileSharingProtocol.fileDel.teamFile` | - | loose | 1 | 是 |
| `fileSharingProtocol.fileDel.teamFileDesc` | - | loose | 1 | 是 |
| `fileSharingProtocol.fileDel.updateFailed` | - | loose | 1 | 是 |
| `fileSharingProtocol.ftp.passiveType.custom` | - | loose | 1 | 是 |
| `fileSharingProtocol.ftp.passiveType.default` | - | loose | 1 | 是 |
| `fileSharingProtocol.nfs.securityWarning` | - | loose | 1 | 是 |
| `fileSharingProtocol.nfs.securityWarningContent` | - | loose | 1 | 是 |
| `fileSharingProtocol.noDirectories.appFile` | - | loose | 1 | 是 |
| `fileSharingProtocol.noDirectories.externalStorage` | - | loose | 1 | 是 |
| `fileSharingProtocol.noDirectories.personalFolder` | - | loose | 1 | 是 |
| `fileSharingProtocol.noDirectories.remoteMount` | - | loose | 1 | 是 |
| `fileSharingProtocol.noDirectories.team` | - | loose | 1 | 是 |
| `fileSharingProtocol.permit.contactAdmin` | - | loose | 1 | 是 |
| `fileSharingProtocol.permit.goEnable` | - | loose | 1 | 是 |
| `fileSharingProtocol.permit.serviceNotEnabled` | - | loose | 1 | 是 |
| `fileSharingProtocol.selectVisibleFolder.cancel` | - | loose | 1 | 是 |
| `fileSharingProtocol.selectVisibleFolder.personalFolder` | - | loose | 1 | 是 |
| `fileSharingProtocol.selectVisibleFolder.remoteMountTip` | - | loose | 1 | 是 |
| `fileSharingProtocol.selectVisibleFolder.save` | - | loose | 1 | 是 |
| `fileSharingProtocol.selectVisibleFolder.saveFailed` | - | loose | 1 | 是 |
| `fileSharingProtocol.selectVisibleFolder.saveSuccess` | - | loose | 1 | 是 |
| `fileSharingProtocol.selectVisibleFolder.selectAll` | - | loose | 1 | 是 |
| `fileSharingProtocol.selectVisibleFolder.selectVisibleTitle` | - | loose | 1 | 是 |
| `fileSharingProtocol.selectVisibleFolder.selected` | - | loose | 1 | 是 |
| `fileSharingProtocol.selectVisibleFolder.setupFailed` | - | loose | 1 | 是 |
| `fileSharingProtocol.selectVisibleFolder.setupSuccess` | - | loose | 1 | 是 |
| `fileSharingProtocol.selectVisibleFolder.unsupportedProtocol` | - | loose | 1 | 是 |
| `fileSharingProtocol.serviceSwitcher.disable` | - | loose | 1 |  |
| `fileSharingProtocol.serviceSwitcher.enable` | - | loose | 1 |  |
| `fileSharingProtocol.serviceSwitcher.enableFailed` | - | loose | 1 | 是 |
| `fileSharingProtocol.serviceSwitcher.enableSuccess` | - | loose | 1 | 是 |
| `fileSharingProtocol.tabs.fileDel` | - | loose | 1 | 是 |
| `fileSharingProtocol.tipsPanel.cannotAccess` | - | loose | 1 | 是 |
| `fileSharingProtocol.tipsPanel.specialCharsFolder` | - | loose | 1 | 是 |
| `fileSharingProtocol.visibleFolderRange.allAccessForbidden` | - | loose | 1 | 是 |
| `fileSharingProtocol.visibleFolderRange.allFolders` | - | loose | 1 | 是 |
| `fileSharingProtocol.visibleFolderRange.allFoldersAccessible` | - | loose | 1 | 是 |
| `fileSharingProtocol.visibleFolderRange.appFile` | - | loose | 1 | 是 |
| `fileSharingProtocol.visibleFolderRange.cannotAccessFolders` | - | loose | 1 | 是 |
| `fileSharingProtocol.visibleFolderRange.customFolders` | - | loose | 1 | 是 |
| `fileSharingProtocol.visibleFolderRange.externalStorage` | - | loose | 1 | 是 |
| `fileSharingProtocol.visibleFolderRange.items` | - | loose | 1 | 是 |
| `fileSharingProtocol.visibleFolderRange.nfsSecurityTip` | - | loose | 1 | 是 |
| `fileSharingProtocol.visibleFolderRange.noItems` | - | loose | 1 | 是 |
| `fileSharingProtocol.visibleFolderRange.personalFolder` | - | loose | 1 | 是 |
| `fileSharingProtocol.visibleFolderRange.personalFolderNfs` | - | loose | 1 | 是 |
| `fileSharingProtocol.visibleFolderRange.remoteMount` | - | loose | 1 | 是 |
| `fileSharingProtocol.visibleFolderRange.team` | - | loose | 1 | 是 |
| `fileSharingProtocol.visibleFolderRange.title` | - | loose | 1 | 是 |
| `fileSharingProtocol.visibleFolderRange.tooltip` | - | loose | 1 | 是 |
| `fileSharingProtocol.visibleFolderType.allowed` | - | loose | 1 | 是 |
| `fileSharingProtocol.visibleFolderType.disabled` | - | loose | 1 | 是 |
| `fileSharingProtocol.visibleFolderType.partial` | - | loose | 1 | 是 |

## fixTool

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `fixTool.executeTask` | - | loose | 1 |  |
| `fixTool.maintenanceTool` | - | loose | 1 | 是 |
| `fixTool.maintenanceToolDesc` | - | loose | 1 | 是 |
| `fixTool.pleaseSelectTask` | - | loose | 1 | 是 |
| `fixTool.taskExecuting` | - | loose | 1 |  |
| `fixTool.taskName` | - | loose | 2 | 是 |
| `fixTool.taskTypes.cleanThumb` | - | loose | 1 | 是 |
| `fixTool.taskTypes.recheckExif` | - | loose | 1 | 是 |
| `fixTool.taskTypes.regenerateThumb` | - | loose | 1 | 是 |
| `fixTool.taskTypes.reloadIndex` | - | loose | 1 | 是 |

## folderManage

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `folderManage.addFailed` | - | loose | 1 | 是 |
| `folderManage.addFolder` | - | loose | 1 | 是 |
| `folderManage.available` | - | loose | 1 | 是 |
| `folderManage.backupLocation` | - | loose | 1 | 是 |
| `folderManage.description` | - | loose | 1 | 是 |
| `folderManage.externalFolderTip` | - | loose | 1 | 是 |
| `folderManage.folderNotFound` | - | loose | 2 | 是 |
| `folderManage.mergeAs` | - | loose | 1 | 是 |
| `folderManage.mergeDesc` | - | loose | 1 | 是 |
| `folderManage.mergeTitle` | - | loose | 1 | 是 |
| `folderManage.modifyBackupLocation` | - | loose | 2 |  |
| `folderManage.noWritePermission` | - | loose | 1 | 是 |
| `folderManage.noWritePermissionError` | - | loose | 2 | 是 |
| `folderManage.photosCount` | - | loose | 1 | 是 |
| `folderManage.reconnectFolder` | - | loose | 1 | 是 |
| `folderManage.remove` | - | loose | 2 |  |
| `folderManage.removeFolderContent` | - | loose | 1 | 是 |
| `folderManage.removeFolderTitle` | - | loose | 1 | 是 |
| `folderManage.scan` | - | loose | 2 | 是 |
| `folderManage.scanAll` | - | loose | 1 | 是 |
| `folderManage.scanning` | - | loose | 1 | 是 |
| `folderManage.selectFolder` | - | loose | 2 | 是 |
| `folderManage.sharedFolderTip` | - | loose | 1 | 是 |
| `folderManage.subFolders` | - | loose | 1 | 是 |
| `folderManage.understood` | - | loose | 1 | 是 |
| `folderManage.videosCount` | - | loose | 1 | 是 |

## folderView

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `folderView.addTo` | - | loose | 2 | 是 |
| `folderView.captureTime` | - | loose | 1 | 是 |
| `folderView.changeFolderCover` | - | loose | 2 | 是 |
| `folderView.collect` | - | loose | 1 | 是 |
| `folderView.compressedJpeg` | - | loose | 1 | 是 |
| `folderView.copy` | - | loose | 1 | 是 |
| `folderView.copyFailed` | - | loose | 1 | 是 |
| `folderView.copyTo` | - | loose | 3 | 是 |
| `folderView.coverSetFailed` | - | loose | 1 | 是 |
| `folderView.coverSetSuccess` | - | loose | 1 | 是 |
| `folderView.delete` | - | loose | 3 | 是 |
| `folderView.deleteContent` | - | loose | 1 | 是 |
| `folderView.deleteCount` | - | loose | 1 | 是 |
| `folderView.deleteFailed` | - | loose | 1 | 是 |
| `folderView.deleteFileConfirm` | - | loose | 1 | 是 |
| `folderView.deleteFolderConfirm` | - | loose | 1 | 是 |
| `folderView.deleteSuccess` | - | loose | 1 | 是 |
| `folderView.download` | - | loose | 2 | 是 |
| `folderView.duplicateFileHandling` | - | loose | 1 | 是 |
| `folderView.duplicateFileQuestion` | - | loose | 1 | 是 |
| `folderView.editGeo` | - | loose | 1 | 是 |
| `folderView.editTag` | - | loose | 2 | 是 |
| `folderView.editTime` | - | loose | 2 | 是 |
| `folderView.fileName` | - | loose | 1 | 是 |
| `folderView.fileNameSpecialCharError` | - | loose | 1 | 是 |
| `folderView.fileSize` | - | loose | 1 | 是 |
| `folderView.fileType` | - | loose | 1 | 是 |
| `folderView.folderIsEmpty` | - | loose | 1 | 是 |
| `folderView.folderNameStartError` | - | loose | 1 | 是 |
| `folderView.folderNotFoundOrNoPermission` | - | loose | 2 | 是 |
| `folderView.getFolderCoverFailed` | - | loose | 1 | 是 |
| `folderView.maxFourCoverImages` | - | loose | 1 | 是 |
| `folderView.more` | - | loose | 1 | 是 |
| `folderView.move` | - | loose | 1 | 是 |
| `folderView.moveFailed` | - | loose | 1 | 是 |
| `folderView.moveTo` | - | loose | 3 | 是 |
| `folderView.original` | - | loose | 1 | 是 |
| `folderView.overwrite` | - | loose | 1 | 是 |
| `folderView.rememberChoice` | - | loose | 1 | 是 |
| `folderView.rename` | - | loose | 1 | 是 |
| `folderView.rotate` | - | loose | 1 | 是 |
| `folderView.selectedCount` | - | loose | 1 | 是 |
| `folderView.share` | - | loose | 2 | 是 |
| `folderView.shareExternalLink` | - | loose | 1 | 是 |
| `folderView.shareToDeviceUsers` | - | loose | 1 | 是 |
| `folderView.skip` | - | loose | 1 | 是 |
| `folderView.targetIsSubdirectory` | - | loose | 3 | 是 |
| `folderView.upFolderPoster` | - | loose | 1 | 是 |

## footer

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `footer.cancel` | - | loose | 2 |  |
| `footer.confirm` | - | loose | 2 |  |

## format

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `format.folder` | - | loose | 3 | 是 |

## globalSettings

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `globalSettings.adminOnly` | - | loose | 1 | 是 |
| `globalSettings.adminOnly2` | - | loose | 1 | 是 |
| `globalSettings.allUsers` | - | loose | 1 | 是 |
| `globalSettings.autoSwitchCPU` | - | loose | 1 | 是 |
| `globalSettings.autoSwitchCPUDesc` | - | loose | 1 | 是 |
| `globalSettings.enableGPU` | - | loose | 1 | 是 |
| `globalSettings.externalLinkPermission` | - | loose | 2 | 是 |
| `globalSettings.externalLinkPermissionDesc` | - | loose | 1 | 是 |
| `globalSettings.externalLinkSettings` | - | loose | 1 | 是 |
| `globalSettings.externalLinkSettingsDesc` | - | loose | 1 | 是 |
| `globalSettings.gpuStartFailed` | - | loose | 1 | 是 |
| `globalSettings.modifyFailed` | - | loose | 1 | 是 |
| `globalSettings.noAvailableGPU` | - | loose | 1 | 是 |
| `globalSettings.operationFailed` | - | loose | 2 | 是 |
| `globalSettings.selectGPU` | - | loose | 1 | 是 |

## handler

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `handler.delete` | - | loose | 1 | 是 |
| `handler.download` | - | loose | 1 | 是 |
| `handler.more` | - | loose | 1 | 是 |
| `handler.newFolder` | - | loose | 1 | 是 |
| `handler.refresh` | - | loose | 2 | 是 |
| `handler.sort` | - | loose | 2 | 是 |
| `handler.sortType.asc` | - | loose | 10 | 是 |
| `handler.sortType.desc` | - | loose | 10 | 是 |
| `handler.switchToColumnView` | - | loose | 1 | 是 |
| `handler.switchToIconView` | - | loose | 2 | 是 |
| `handler.switchToListView` | - | loose | 2 | 是 |
| `handler.upload` | - | loose | 1 | 是 |
| `handler.uploadFile` | - | loose | 1 | 是 |
| `handler.uploadFolder` | - | loose | 2 | 是 |

## handlerFn

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `handlerFn.compress.errors.namesakeError` | - | loose | 3 | 是 |
| `handlerFn.compress.failed` | - | loose | 2 | 是 |
| `handlerFn.compress.form.advancedSettings` | - | loose | 1 | 是 |
| `handlerFn.compress.form.cancel` | - | loose | 1 | 是 |
| `handlerFn.compress.form.checkCompressOptions` | - | loose | 1 |  |
| `handlerFn.compress.form.compressFile` | - | loose | 1 |  |
| `handlerFn.compress.form.compressionLevel` | - | loose | 1 | 是 |
| `handlerFn.compress.form.confirm` | - | loose | 1 | 是 |
| `handlerFn.compress.form.encryptCompress` | - | loose | 1 | 是 |
| `handlerFn.compress.form.fileName` | - | loose | 1 | 是 |
| `handlerFn.compress.form.fileNamePlaceholder` | - | loose | 1 | 是 |
| `handlerFn.compress.form.format` | - | loose | 1 | 是 |
| `handlerFn.compress.form.passwordPlaceholder` | - | loose | 1 | 是 |
| `handlerFn.compress.form.passwordRequired` | - | loose | 1 | 是 |
| `handlerFn.compress.levels.common` | - | loose | 1 | 是 |
| `handlerFn.compress.levels.fastest` | - | loose | 1 | 是 |
| `handlerFn.compress.levels.packOnly` | - | loose | 1 | 是 |
| `handlerFn.compress.levels.smallest` | - | loose | 1 | 是 |
| `handlerFn.compress.success` | - | loose | 1 | 是 |
| `handlerFn.compress.title` | - | loose | 1 | 是 |
| `handlerFn.copy.copySuccess` | - | loose | 1 | 是 |
| `handlerFn.cut.cutSuccess` | - | loose | 1 | 是 |
| `handlerFn.delete.cancel` | - | loose | 1 | 是 |
| `handlerFn.delete.cannotDelete` | - | loose | 1 | 是 |
| `handlerFn.delete.completelyDelete` | - | loose | 1 |  |
| `handlerFn.delete.confirmPassword` | `i18nKey` | alias_key,loose | 2 |  |
| `handlerFn.delete.confirmPasswordError` | - | loose | 1 | 是 |
| `handlerFn.delete.delete` | - | loose | 2 |  |
| `handlerFn.delete.deleteDescription` | - | loose | 1 | 是 |
| `handlerFn.delete.deleteFailed` | - | loose | 1 | 是 |
| `handlerFn.delete.deleteSuccess` | - | loose | 1 | 是 |
| `handlerFn.delete.directlyDeleteTip` | - | loose | 1 |  |
| `handlerFn.delete.mountDirError` | - | loose | 1 | 是 |
| `handlerFn.delete.moveToRecycleBin` | - | loose | 1 |  |
| `handlerFn.delete.recycleTip` | - | loose | 1 |  |
| `handlerFn.delete.remoteFilesTip` | - | loose | 1 |  |
| `handlerFn.delete.teamSpaceRecycleAdminTip` | - | loose | 1 |  |
| `handlerFn.delete.teamSpaceRecycleTip` | - | loose | 1 |  |
| `handlerFn.delete.teamSpaceTip` | - | loose | 2 | 是 |
| `handlerFn.empty.cancelText` | - | loose | 1 | 是 |
| `handlerFn.empty.clearFailed` | - | loose | 2 | 是 |
| `handlerFn.empty.clearSuccess` | - | loose | 1 | 是 |
| `handlerFn.empty.content` | - | loose | 1 | 是 |
| `handlerFn.empty.okText` | - | loose | 1 | 是 |
| `handlerFn.empty.title` | - | loose | 1 | 是 |
| `handlerFn.favorite.addFailed` | - | loose | 1 | 是 |
| `handlerFn.favorite.addSuccess` | - | loose | 1 | 是 |
| `handlerFn.favorite.removeFailed` | - | loose | 1 | 是 |
| `handlerFn.favorite.removeSuccess` | - | loose | 1 | 是 |
| `handlerFn.favorite.zipTips.cancel` | - | loose | 1 | 是 |
| `handlerFn.favorite.zipTips.content` | - | loose | 1 | 是 |
| `handlerFn.favorite.zipTips.ok` | - | loose | 1 | 是 |
| `handlerFn.favorite.zipTips.title` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.defaultName` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.defaultUser` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.errors.createFailed` | - | loose | 1 |  |
| `handlerFn.fileCollection.errors.editFailed` | - | loose | 1 |  |
| `handlerFn.fileCollection.fallbackName` | - | loose | 3 | 是 |
| `handlerFn.fileCollection.form.advancedSettings` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.form.attachment.addFile` | - | loose | 2 | 是 |
| `handlerFn.fileCollection.form.attachment.help` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.form.attachment.label` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.form.attachment.pickerTitle` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.form.attachment.placeholder` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.form.attachment.required` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.form.description.label` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.form.description.maxLength` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.form.description.placeholder` | - | loose | 2 | 是 |
| `handlerFn.fileCollection.form.fileTypes.any` | - | loose | 2 | 是 |
| `handlerFn.fileCollection.form.fileTypes.anyHelp` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.form.fileTypes.audio` | - | loose | 2 | 是 |
| `handlerFn.fileCollection.form.fileTypes.categoryHelp` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.form.fileTypes.document` | - | loose | 2 | 是 |
| `handlerFn.fileCollection.form.fileTypes.image` | - | loose | 2 | 是 |
| `handlerFn.fileCollection.form.fileTypes.label` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.form.fileTypes.video` | - | loose | 2 | 是 |
| `handlerFn.fileCollection.form.maxAccess.help` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.form.maxAccess.label` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.form.maxAccess.min` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.form.maxAccess.placeholder` | - | loose | 2 | 是 |
| `handlerFn.fileCollection.form.maxFileSize.label` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.form.name.label` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.form.name.placeholder` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.form.name.required` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.form.passwd.generate` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.form.passwd.help` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.form.passwd.label` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.form.passwd.minLength` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.form.passwd.pattern` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.form.passwd.placeholder` | - | loose | 2 | 是 |
| `handlerFn.fileCollection.form.uploadPath.label` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.form.uploadPath.placeholder` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.form.validTo.label` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.form.validTo.required` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.helper` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.result.attachment` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.result.copiedSuccess` | - | loose | 2 | 是 |
| `handlerFn.fileCollection.result.copyMessage` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.result.createSuccess` | - | loose | 1 |  |
| `handlerFn.fileCollection.result.downloadQrCode` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.result.downloadQrCodeFailed` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.result.editSuccess` | - | loose | 1 |  |
| `handlerFn.fileCollection.result.fileTypeSeparator` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.result.linkExpiresAtWithMaxAccess` | `i18nKey` | alias_key,loose | 2 |  |
| `handlerFn.fileCollection.result.linkExpiresAtWithUnlimitedAccess` | `i18nKey` | alias_key,loose | 2 |  |
| `handlerFn.fileCollection.result.linkPermanentWithMaxAccess` | `i18nKey` | alias_key,loose | 2 |  |
| `handlerFn.fileCollection.result.linkPermanentWithUnlimitedAccess` | `i18nKey` | alias_key,loose | 2 |  |
| `handlerFn.fileCollection.result.password` | `i18nKey` | alias_key,loose | 2 |  |
| `handlerFn.fileCollection.result.qrCodePosterHint` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.result.scanQRCode` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.result.shareMessage` | - | loose | 1 |  |
| `handlerFn.fileCollection.result.shareMessageDeadline` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.result.shareMessageDescription` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.result.shareMessageWithPassword` | - | loose | 1 |  |
| `handlerFn.fileCollection.result.title` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.result.uploadLinkHint` | - | loose | 1 | 是 |
| `handlerFn.fileCollection.title.create` | - | loose | 1 |  |
| `handlerFn.fileCollection.title.edit` | - | loose | 1 |  |
| `handlerFn.mkdir.createFailed` | - | loose | 2 | 是 |
| `handlerFn.mkdir.createSuccess` | - | loose | 1 | 是 |
| `handlerFn.move.cannotMove` | - | loose | 1 | 是 |
| `handlerFn.move.copyFailed` | - | loose | 1 |  |
| `handlerFn.move.copyHere` | - | loose | 1 | 是 |
| `handlerFn.move.copySuccess` | - | loose | 1 |  |
| `handlerFn.move.mountDirError` | - | loose | 1 | 是 |
| `handlerFn.move.moveFailed` | - | loose | 1 |  |
| `handlerFn.move.moveHere` | - | loose | 1 | 是 |
| `handlerFn.move.moveSuccess` | - | loose | 1 |  |
| `handlerFn.namesake.description.copy` | - | loose | 1 | 是 |
| `handlerFn.namesake.description.extract` | - | loose | 1 | 是 |
| `handlerFn.namesake.description.move` | - | loose | 1 | 是 |
| `handlerFn.namesake.description.restore` | - | loose | 1 | 是 |
| `handlerFn.namesake.description.upload` | - | loose | 1 | 是 |
| `handlerFn.namesake.keepBoth` | - | loose | 6 | 是 |
| `handlerFn.namesake.replaceAndOverwrite.copy` | - | loose | 1 | 是 |
| `handlerFn.namesake.replaceAndOverwrite.extract` | - | loose | 1 | 是 |
| `handlerFn.namesake.replaceAndOverwrite.move` | - | loose | 1 | 是 |
| `handlerFn.namesake.replaceAndOverwrite.restore` | - | loose | 1 | 是 |
| `handlerFn.namesake.replaceAndOverwrite.upload` | - | loose | 1 | 是 |
| `handlerFn.namesake.settingTips.copy` | - | loose | 1 | 是 |
| `handlerFn.namesake.settingTips.extract` | - | loose | 1 | 是 |
| `handlerFn.namesake.settingTips.move` | - | loose | 1 | 是 |
| `handlerFn.namesake.settingTips.restore` | - | loose | 1 | 是 |
| `handlerFn.namesake.settingTips.upload` | - | loose | 1 | 是 |
| `handlerFn.namesake.skip.copy` | - | loose | 1 | 是 |
| `handlerFn.namesake.skip.extract` | - | loose | 1 | 是 |
| `handlerFn.namesake.skip.move` | - | loose | 1 | 是 |
| `handlerFn.namesake.skip.restore` | - | loose | 1 | 是 |
| `handlerFn.namesake.skip.upload` | - | loose | 1 | 是 |
| `handlerFn.namesake.title` | - | loose | 2 | 是 |
| `handlerFn.newTeamSpace.title` | - | loose | 2 | 是 |
| `handlerFn.paste.cancel` | - | loose | 1 | 是 |
| `handlerFn.paste.confirm` | - | loose | 1 | 是 |
| `handlerFn.paste.continue` | - | loose | 1 | 是 |
| `handlerFn.paste.onlyDir` | - | loose | 1 | 是 |
| `handlerFn.paste.onlyDirContinue` | - | loose | 1 | 是 |
| `handlerFn.paste.tipsTitle` | - | loose | 2 | 是 |
| `handlerFn.recentRecord.cancel` | - | loose | 2 | 是 |
| `handlerFn.recentRecord.clearContent` | - | loose | 2 | 是 |
| `handlerFn.recentRecord.clearFailed` | - | loose | 2 | 是 |
| `handlerFn.recentRecord.clearSuccess` | - | loose | 1 | 是 |
| `handlerFn.recentRecord.clearTitle` | - | loose | 2 | 是 |
| `handlerFn.recentRecord.confirmClear` | - | loose | 2 | 是 |
| `handlerFn.rename.cancel` | - | loose | 1 | 是 |
| `handlerFn.rename.confirm` | - | loose | 1 | 是 |
| `handlerFn.rename.failed` | - | loose | 1 | 是 |
| `handlerFn.rename.fileName` | - | loose | 1 | 是 |
| `handlerFn.rename.folderName` | - | loose | 1 | 是 |
| `handlerFn.rename.success` | - | loose | 1 | 是 |
| `handlerFn.rename.title` | - | loose | 1 | 是 |
| `handlerFn.restore.restoreFailed` | - | loose | 1 | 是 |
| `handlerFn.restore.restoreSuccess` | - | loose | 1 | 是 |
| `handlerFn.shareLink.clipboard.copySuccess` | - | loose | 1 | 是 |
| `handlerFn.shareLink.clipboard.text` | - | loose | 1 |  |
| `handlerFn.shareLink.clipboard.textWithPassword` | - | loose | 1 |  |
| `handlerFn.shareLink.errors.createFailed` | - | loose | 1 | 是 |
| `handlerFn.shareLink.errors.editFailed` | - | loose | 1 | 是 |
| `handlerFn.shareLink.form.cancel` | - | loose | 1 | 是 |
| `handlerFn.shareLink.form.confirm` | - | loose | 1 | 是 |
| `handlerFn.shareLink.form.enterMaxAccess` | - | loose | 2 | 是 |
| `handlerFn.shareLink.form.enterPassword` | - | loose | 2 | 是 |
| `handlerFn.shareLink.form.expiredError` | - | loose | 1 | 是 |
| `handlerFn.shareLink.form.expiryTime` | - | loose | 1 | 是 |
| `handlerFn.shareLink.form.generatePassword` | - | loose | 1 | 是 |
| `handlerFn.shareLink.form.longTermEffective` | - | loose | 1 | 是 |
| `handlerFn.shareLink.form.maxAccess` | - | loose | 1 | 是 |
| `handlerFn.shareLink.form.password` | - | loose | 1 | 是 |
| `handlerFn.shareLink.form.passwordMaxLength` | - | loose | 1 | 是 |
| `handlerFn.shareLink.form.passwordMinLength` | - | loose | 1 | 是 |
| `handlerFn.shareLink.form.passwordPattern` | - | loose | 1 | 是 |
| `handlerFn.shareLink.form.selectDate` | - | loose | 3 | 是 |
| `handlerFn.shareLink.multipleFiles` | - | loose | 1 | 是 |
| `handlerFn.shareLink.presets.15days` | - | loose | 1 | 是 |
| `handlerFn.shareLink.presets.1day` | - | loose | 1 | 是 |
| `handlerFn.shareLink.presets.30days` | - | loose | 1 | 是 |
| `handlerFn.shareLink.presets.3days` | - | loose | 1 | 是 |
| `handlerFn.shareLink.presets.7days` | - | loose | 1 | 是 |
| `handlerFn.shareLink.result.accessCount` | `i18nKey` | alias_key,loose | 2 |  |
| `handlerFn.shareLink.result.copyLink` | - | loose | 1 | 是 |
| `handlerFn.shareLink.result.copyLinkAndPassword` | - | loose | 1 | 是 |
| `handlerFn.shareLink.result.copyShareLink` | - | loose | 2 | 是 |
| `handlerFn.shareLink.result.createSuccess` | - | loose | 2 | 是 |
| `handlerFn.shareLink.result.editSuccess` | - | loose | 1 | 是 |
| `handlerFn.shareLink.result.externalLink` | - | loose | 1 | 是 |
| `handlerFn.shareLink.result.linkExpiresAt` | `i18nKey` | alias_key,loose | 2 |  |
| `handlerFn.shareLink.result.linkPermanent` | - | loose | 1 | 是 |
| `handlerFn.shareLink.result.password` | - | loose | 1 | 是 |
| `handlerFn.shareLink.result.qrCodeTip` | - | loose | 1 | 是 |
| `handlerFn.shareLink.result.scanQRCode` | - | loose | 2 | 是 |
| `handlerFn.shareLink.result.unlimitedAccess` | - | loose | 1 | 是 |
| `handlerFn.shareLink.shareFailedTip` | - | loose | 1 | 是 |
| `handlerFn.shareLink.title.create` | - | loose | 1 |  |
| `handlerFn.shareLink.title.edit` | - | loose | 1 |  |
| `handlerFn.unzip.charsets.big5` | - | loose | 2 | 是 |
| `handlerFn.unzip.charsets.eucKr` | - | loose | 2 | 是 |
| `handlerFn.unzip.charsets.gbk` | - | loose | 2 | 是 |
| `handlerFn.unzip.charsets.iso88591` | - | loose | 2 | 是 |
| `handlerFn.unzip.charsets.latin` | - | loose | 2 | 是 |
| `handlerFn.unzip.charsets.shiftJis` | - | loose | 2 | 是 |
| `handlerFn.unzip.enterPassword.description` | - | loose | 1 | 是 |
| `handlerFn.unzip.enterPassword.placeholder` | - | loose | 1 | 是 |
| `handlerFn.unzip.messages.extractFailed` | - | loose | 2 | 是 |
| `handlerFn.unzip.messages.extractSuccess` | - | loose | 1 | 是 |
| `handlerFn.unzip.selectMode.charset.description` | - | loose | 1 | 是 |
| `handlerFn.unzip.selectMode.charset.placeholder` | - | loose | 1 | 是 |
| `handlerFn.unzip.selectMode.charset.title` | - | loose | 1 | 是 |
| `handlerFn.unzip.selectMode.description` | - | loose | 1 | 是 |
| `handlerFn.unzip.selectMode.options.rename` | - | loose | 1 | 是 |
| `handlerFn.unzip.selectMode.options.replace` | - | loose | 1 | 是 |
| `handlerFn.unzip.selectMode.options.skip` | - | loose | 1 | 是 |
| `handlerFn.unzip.selectMode.overwrite.description` | - | loose | 1 | 是 |
| `handlerFn.unzip.selectMode.overwrite.title` | - | loose | 1 | 是 |
| `handlerFn.unzip.title` | - | loose | 1 | 是 |
| `handlerFn.upload.addedToQueue` | - | loose | 2 | 是 |
| `handlerFn.upload.continue` | - | loose | 2 | 是 |
| `handlerFn.upload.failed` | - | loose | 2 | 是 |
| `handlerFn.upload.namesakeTip` | - | loose | 2 | 是 |
| `handlerFn.upload.partialFailed` | - | loose | 2 | 是 |
| `handlerFn.upload.remoteMountCacheFailed` | - | loose | 1 | 是 |
| `handlerFn.upload.remoteMountStage1Success` | - | loose | 1 | 是 |
| `handlerFn.upload.success` | - | loose | 1 | 是 |
| `handlerFn.upload.tooManyFilesContent` | - | loose | 2 | 是 |
| `handlerFn.upload.tooManyFilesTitle` | - | loose | 2 | 是 |

## hardDiskManagement

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `hardDiskManagement.diskType.notUsb` | - | loose | 1 | 是 |
| `hardDiskManagement.diskUsage.cache` | - | loose | 1 | 是 |
| `hardDiskManagement.diskUsage.mountAsExternalStorage` | - | loose | 1 | 是 |
| `hardDiskManagement.diskUsage.spareEnabled` | - | loose | 1 | 是 |
| `hardDiskManagement.diskUsage.spareSuffix` | - | loose | 1 | 是 |
| `hardDiskManagement.diskUsage.systemInstall` | - | loose | 1 | 是 |
| `hardDiskManagement.modals.killProcess.title` | - | loose | 1 | 是 |
| `hardDiskManagement.toast.mountSuccess` | - | loose | 1 | 是 |
| `hardDiskManagement.toastMessage.killProcessFailed` | - | loose | 1 | 是 |

## hardware

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `hardware.trimDisk.bayType.m2Expansion` | - | loose | 1 | 是 |
| `hardware.trimDisk.bayType.m2Primary` | - | loose | 1 | 是 |
| `hardware.trimDisk.bayType.sata` | - | loose | 1 | 是 |
| `hardware.trimDisk.slotPrefix.m2` | - | loose | 1 | 是 |
| `hardware.trimDisk.slotPrefix.sata` | - | loose | 1 | 是 |

## header

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `header.cell` | - | loose | 1 |  |
| `header.outer` | - | loose | 1 |  |
| `header.row` | - | loose | 1 |  |

## hooks

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `hooks.actionHooks.delete` | - | loose | 5 | 是 |
| `hooks.actionHooks.deleteBackupStorage.content` | - | loose | 1 | 是 |
| `hooks.actionHooks.deleteBackupStorage.failedMsg` | - | loose | 1 | 是 |
| `hooks.actionHooks.deleteBackupStorage.runningTaskMsg` | - | loose | 1 | 是 |
| `hooks.actionHooks.deleteBackupStorage.successMsg` | - | loose | 1 | 是 |
| `hooks.actionHooks.deleteBackupStorage.title` | - | loose | 1 | 是 |
| `hooks.actionHooks.deleteBackupTask.content` | - | loose | 1 | 是 |
| `hooks.actionHooks.deleteBackupTask.deleteSuccess` | - | loose | 1 | 是 |
| `hooks.actionHooks.deleteBackupTask.deleting` | - | loose | 2 | 是 |
| `hooks.actionHooks.deleteBackupTask.title` | - | loose | 1 | 是 |
| `hooks.actionHooks.disable` | - | loose | 3 | 是 |
| `hooks.actionHooks.disableBackupTask.content` | - | loose | 1 | 是 |
| `hooks.actionHooks.disableBackupTask.disableSuccess` | - | loose | 1 | 是 |
| `hooks.actionHooks.disableBackupTask.disabling` | - | loose | 1 | 是 |
| `hooks.actionHooks.disableBackupTask.title` | - | loose | 1 | 是 |
| `hooks.actionHooks.enable` | - | loose | 1 | 是 |
| `hooks.actionHooks.enableBackupTask.enableSuccess` | - | loose | 1 | 是 |
| `hooks.actionHooks.run` | - | loose | 1 | 是 |
| `hooks.actionHooks.stop` | - | loose | 3 | 是 |
| `hooks.actionHooks.stopBackupTask.content` | - | loose | 1 | 是 |
| `hooks.actionHooks.stopBackupTask.stopSuccess` | - | loose | 1 | 是 |
| `hooks.actionHooks.stopBackupTask.stopping` | - | loose | 1 | 是 |
| `hooks.actionHooks.stopBackupTask.title` | - | loose | 1 | 是 |
| `hooks.format.file.connectionTypeLabel` | - | loose | 2 | 是 |
| `hooks.format.file.multiple` | - | loose | 1 | 是 |

## i18next

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `i18next.translate.boo` | - | loose | 4 |  |

## ignoreDotPrefixSettings

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `ignoreDotPrefixSettings.label` | - | loose | 1 | 是 |

## ignoreExtensionsSettings

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `ignoreExtensionsSettings.dialogTitle` | - | loose | 1 | 是 |
| `ignoreExtensionsSettings.editBtnDisabledLabel` | - | loose | 1 |  |
| `ignoreExtensionsSettings.editBtnLabel` | - | loose | 1 |  |
| `ignoreExtensionsSettings.label` | - | loose | 1 | 是 |

## index

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `index.title` | - | loose | 1 | 是 |
| `index.upload` | - | loose | 1 | 是 |

## initialFocusRef

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `initialFocusRef.current` | - | loose | 2 |  |

## initialization

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `initialization.available` | - | loose | 1 | 是 |
| `initialization.backupDesc` | - | loose | 1 | 是 |
| `initialization.backupTitle` | - | loose | 1 | 是 |
| `initialization.defaultBackupLocation` | - | loose | 1 | 是 |
| `initialization.enableAI` | - | loose | 1 | 是 |
| `initialization.enableFailed` | - | loose | 1 | 是 |
| `initialization.enterPhotos` | - | loose | 1 | 是 |
| `initialization.insufficientStorage` | - | loose | 2 | 是 |
| `initialization.invalidStorage` | - | loose | 1 | 是 |
| `initialization.localAIDesc` | - | loose | 1 | 是 |
| `initialization.localAITitle` | - | loose | 1 | 是 |
| `initialization.modelInstallLocation` | - | loose | 1 | 是 |
| `initialization.modelStorageUnavailable` | - | loose | 1 | 是 |
| `initialization.nextStep` | - | loose | 2 | 是 |
| `initialization.noAvailableStorage` | - | loose | 1 | 是 |
| `initialization.noWritePermission` | - | loose | 1 | 是 |
| `initialization.prevStep` | - | loose | 1 | 是 |
| `initialization.restoreDefaultPath` | - | loose | 1 | 是 |
| `initialization.scanToDownloadApp` | - | loose | 1 | 是 |
| `initialization.selectFolder` | - | loose | 1 | 是 |
| `initialization.selectStorage` | - | loose | 1 | 是 |
| `initialization.welcomeDesc` | - | loose | 1 | 是 |
| `initialization.welcomeTitle` | - | loose | 1 | 是 |

## inputRef

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `inputRef.current` | - | loose | 4 |  |

## install

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `install.failed` | - | loose | 1 | 是 |
| `install.failedOrNotExist` | - | loose | 1 | 是 |
| `install.installing` | - | loose | 1 |  |
| `install.upgrading` | - | loose | 1 |  |

## installSettings

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `installSettings.allowUserAuthorizationPaths` | - | loose | 1 | 是 |
| `installSettings.allowUserAuthorizationPathsTooltip` | - | loose | 1 | 是 |
| `installSettings.title` | - | loose | 1 | 是 |
| `installSettings.userFileAuthorization` | - | loose | 1 | 是 |

## installed

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `installed.autoUpdatable` | - | loose | 1 | 是 |
| `installed.installed` | - | loose | 1 | 是 |
| `installed.updatable` | - | loose | 1 | 是 |

## keepFilesSettings

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `keepFilesSettings.label` | - | loose | 1 | 是 |

## languageAndTime

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `languageAndTime.dateFormat` | - | loose | 1 | 是 |
| `languageAndTime.personalInterfaceLanguage` | - | loose | 1 | 是 |
| `languageAndTime.timeFormat` | - | loose | 1 | 是 |
| `languageAndTime.twelveHourFormat` | - | loose | 1 | 是 |
| `languageAndTime.twentyFourHourFormat` | - | loose | 1 | 是 |

## level

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `level.all` | - | loose | 2 | 是 |
| `level.error` | - | loose | 2 | 是 |
| `level.normal` | - | loose | 1 | 是 |
| `level.warn` | - | loose | 1 | 是 |

## license

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `license.acceptTerms` | - | loose | 1 | 是 |
| `license.readFirst` | - | loose | 1 | 是 |
| `license.title` | - | loose | 1 | 是 |

## manualInstall

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `manualInstall.agree` | - | loose | 1 | 是 |
| `manualInstall.cannotInstallContent` | - | loose | 1 | 是 |
| `manualInstall.cannotInstallContent2` | - | loose | 1 | 是 |
| `manualInstall.cannotInstallTitle` | - | loose | 1 | 是 |
| `manualInstall.fileSizeLimit` | - | loose | 2 | 是 |
| `manualInstall.packageExceptionContent` | - | loose | 1 | 是 |
| `manualInstall.packageExceptionTitle` | - | loose | 1 | 是 |
| `manualInstall.selectFpkFile` | - | loose | 1 | 是 |
| `manualInstall.selectStorageSpace` | - | loose | 1 | 是 |
| `manualInstall.storageLowSpaceWarning` | - | loose | 1 | 是 |
| `manualInstall.title` | - | loose | 1 | 是 |
| `manualInstall.unverifiedAppContent` | - | loose | 1 | 是 |
| `manualInstall.unverifiedAppTitle` | - | loose | 1 | 是 |
| `manualInstall.uploadFpkFile` | - | loose | 1 | 是 |
| `manualInstall.uploadFromComputer` | - | loose | 1 | 是 |
| `manualInstall.uploadFromNAS` | - | loose | 1 | 是 |

## map

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `map.empty` | - | loose | 1 | 是 |
| `map.location` | - | loose | 1 | 是 |

## mediaCategory

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `mediaCategory.360` | - | loose | 1 | 是 |
| `mediaCategory.gif` | - | loose | 1 | 是 |
| `mediaCategory.livePhoto` | - | loose | 1 | 是 |
| `mediaCategory.panorama` | - | loose | 1 | 是 |
| `mediaCategory.photo` | - | loose | 1 | 是 |
| `mediaCategory.raw` | - | loose | 1 | 是 |
| `mediaCategory.screenshot` | - | loose | 1 | 是 |
| `mediaCategory.video` | - | loose | 1 | 是 |

## menu

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `menu.autoArchive` | - | loose | 1 | 是 |
| `menu.clear` | - | loose | 1 | 是 |
| `menu.export` | - | loose | 1 | 是 |
| `menu.exportAssistance` | - | loose | 1 | 是 |
| `menu.more` | - | loose | 1 | 是 |

## menus

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `menus.backupDeleteTask` | `label` | alias_key,loose | 2 |  |
| `menus.backupDisableTask` | `label` | alias_key,loose | 2 |  |
| `menus.backupEnableTask` | `label` | alias_key,loose | 2 |  |
| `menus.backupLocalData` | `label` | alias_key,loose | 2 |  |
| `menus.backupRemoteData` | `label` | alias_key,loose | 2 |  |
| `menus.backupTaskRecords` | `label` | alias_key,loose | 2 |  |
| `menus.backupTaskSettings` | `label` | alias_key,loose | 2 |  |
| `menus.description.backupLocalData` | - | loose | 1 |  |
| `menus.description.backupRemoteData` | - | loose | 1 |  |

## messages

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `messages.bindSuccess` | - | loose | 1 | 是 |
| `messages.copySuccess` | - | loose | 3 | 是 |
| `messages.modifySuccess` | - | loose | 2 | 是 |
| `messages.tfaDisabled` | - | loose | 1 | 是 |
| `messages.trustDeviceFailed` | - | loose | 1 | 是 |
| `messages.trustDeviceSuccess` | - | loose | 1 | 是 |
| `messages.untrustFailed` | - | loose | 1 | 是 |
| `messages.untrustSuccess` | - | loose | 1 | 是 |

## modal

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `modal.archive.title` | - | loose | 1 | 是 |
| `modal.clearLog.confirm` | - | loose | 1 | 是 |
| `modal.clearLog.content` | - | loose | 1 | 是 |
| `modal.clearLog.title` | - | loose | 1 | 是 |
| `modal.exportAssistance.title` | - | loose | 1 | 是 |
| `modal.exportLog.confirm` | - | loose | 1 | 是 |
| `modal.exportLog.content` | - | loose | 1 | 是 |
| `modal.exportLog.title` | - | loose | 1 | 是 |

## modals

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `modals.changeMoment.characterCount` | - | loose | 1 | 是 |
| `modals.changeMoment.characterLimitError` | - | loose | 1 | 是 |
| `modals.changeMoment.placeholder` | - | loose | 1 | 是 |
| `modals.changeMoment.title` | - | loose | 1 | 是 |
| `modals.secureEmail.modifySubTitle` | - | loose | 1 | 是 |
| `modals.secureEmail.modifyTitle` | - | loose | 1 | 是 |
| `modals.secureEmail.setupSubTitle` | - | loose | 1 | 是 |
| `modals.secureEmail.setupTitle` | - | loose | 2 | 是 |
| `modals.twoFactorAuth.enableSubTitle` | - | loose | 1 | 是 |
| `modals.twoFactorAuth.enableTitle` | - | loose | 2 | 是 |
| `modals.twoFactorAuth.modifySubTitle` | - | loose | 1 | 是 |
| `modals.twoFactorAuth.modifyTitle` | - | loose | 1 | 是 |

## module

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `module.all` | - | loose | 1 | 是 |
| `module.fileTransfer` | - | loose | 1 | 是 |
| `module.hardDiskStorage` | - | loose | 1 | 是 |
| `module.login` | - | loose | 1 | 是 |
| `module.system` | - | loose | 1 | 是 |

## monthGrid

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `monthGrid.current.foundation` | - | loose | 4 |  |

## mp4a

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `mp4a.40.2` | - | loose | 7 | 是 |
| `mp4a.40.5` | - | loose | 8 | 是 |

## mp4v

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `mp4v.20.8` | - | loose | 1 |  |

## myShare

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `myShare.searchPlaceholder` | - | loose | 1 | 是 |

## namesake

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `namesake.alwaysAsk` | - | loose | 1 | 是 |
| `namesake.copy.alwaysAskExtra` | - | loose | 1 | 是 |
| `namesake.copy.cover` | - | loose | 1 | 是 |
| `namesake.copy.coverExtra` | `i18nKey` | alias_key,loose | 2 |  |
| `namesake.copy.skipExtra` | - | loose | 1 | 是 |
| `namesake.copyFile` | - | loose | 1 | 是 |
| `namesake.copyFileDescription` | - | loose | 1 | 是 |
| `namesake.keepBoth` | - | loose | 1 | 是 |
| `namesake.keepBothExtra` | `i18nKey` | alias_key,loose | 2 |  |
| `namesake.move.alwaysAskExtra` | - | loose | 1 | 是 |
| `namesake.move.cover` | - | loose | 1 | 是 |
| `namesake.move.coverExtra` | `i18nKey` | alias_key,loose | 2 |  |
| `namesake.move.skipExtra` | - | loose | 1 | 是 |
| `namesake.moveFile` | - | loose | 1 | 是 |
| `namesake.moveFileDescription` | - | loose | 1 | 是 |
| `namesake.skip` | - | loose | 1 | 是 |
| `namesake.updateFailed` | - | loose | 2 | 是 |
| `namesake.upload.alwaysAskExtra` | - | loose | 1 | 是 |
| `namesake.upload.cover` | - | loose | 1 | 是 |
| `namesake.upload.coverExtra` | `i18nKey` | alias_key,loose | 2 |  |
| `namesake.upload.skipExtra` | - | loose | 1 | 是 |
| `namesake.uploadFile` | - | loose | 1 | 是 |
| `namesake.uploadFileDescription` | - | loose | 1 | 是 |

## nasConnecterDialog

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `nasConnecterDialog.backToListTips` | - | loose | 2 | 是 |
| `nasConnecterDialog.button.label` | - | loose | 1 | 是 |
| `nasConnecterDialog.button.title` | - | loose | 1 | 是 |
| `nasConnecterDialog.connectNasWithWebdav` | - | loose | 1 | 是 |
| `nasConnecterDialog.guidePanel.emptyTitle` | - | loose | 1 | 是 |
| `nasConnecterDialog.guidePanel.title` | - | loose | 1 | 是 |
| `nasConnecterDialog.loginForm.cancelTips` | - | loose | 1 | 是 |
| `nasConnecterDialog.loginForm.confirmTips` | - | loose | 1 | 是 |
| `nasConnecterDialog.loginForm.connectFailedMsg` | - | loose | 1 | 是 |
| `nasConnecterDialog.loginForm.connectSuccessMsg` | - | loose | 1 | 是 |
| `nasConnecterDialog.loginForm.emptyHostName` | - | loose | 1 | 是 |
| `nasConnecterDialog.loginForm.passwordEmpty` | - | loose | 1 | 是 |
| `nasConnecterDialog.loginForm.passwordLabel` | - | loose | 2 | 是 |
| `nasConnecterDialog.loginForm.portLabel` | - | loose | 2 | 是 |
| `nasConnecterDialog.loginForm.portalEmpty` | - | loose | 1 | 是 |
| `nasConnecterDialog.loginForm.portalInvalid` | - | loose | 1 | 是 |
| `nasConnecterDialog.loginForm.switchDevice` | - | loose | 1 | 是 |
| `nasConnecterDialog.loginForm.userNameEmpty` | - | loose | 1 | 是 |
| `nasConnecterDialog.loginForm.usernameLabel` | - | loose | 2 | 是 |
| `nasConnecterDialog.nasList.clickToConnect` | - | loose | 1 |  |
| `nasConnecterDialog.nasList.clickToSelect` | - | loose | 1 |  |
| `nasConnecterDialog.nasList.emptyHostName` | - | loose | 1 | 是 |

## nativeEvent

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `nativeEvent.target.scrollLeft` | - | loose | 1 |  |
| `nativeEvent.target.scrollTop` | - | loose | 1 |  |
| `nativeEvent.target.value` | - | loose | 2 |  |

## navigator

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `navigator.language` | - | loose | 1 | 是 |

## offline

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `offline.apiError.btnLabel` | - | loose | 1 | 是 |
| `offline.apiError.tipsLabel` | - | loose | 1 | 是 |
| `offline.networkError.btnLabel` | - | loose | 1 | 是 |
| `offline.networkError.tipsLabel` | - | loose | 1 | 是 |

## openFileGuard

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `openFileGuard.cancel` | - | loose | 1 | 是 |
| `openFileGuard.download` | - | loose | 1 | 是 |
| `openFileGuard.gotIt` | - | loose | 1 | 是 |
| `openFileGuard.noPermission` | - | loose | 1 | 是 |
| `openFileGuard.pathLabel` | - | loose | 1 | 是 |
| `openFileGuard.pathNotFound` | - | loose | 1 | 是 |
| `openFileGuard.searchApp` | - | loose | 1 | 是 |
| `openFileGuard.unsupportedPreview` | - | loose | 1 | 是 |

## page

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `page.leaveConfirmation` | - | loose | 1 | 是 |
| `page.search` | - | loose | 1 | 是 |

## pagination

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `pagination.currentPage` | - | loose | 1 |  |
| `pagination.pageSize` | - | loose | 1 |  |
| `pagination.total` | - | loose | 1 | 是 |

## pathFormatter

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `pathFormatter.appShare` | - | loose | 2 | 是 |
| `pathFormatter.externalStorage` | - | loose | 1 | 是 |
| `pathFormatter.linkShare` | - | loose | 1 | 是 |
| `pathFormatter.myFiles` | - | loose | 1 | 是 |
| `pathFormatter.myShare` | - | loose | 1 | 是 |
| `pathFormatter.noUsername` | - | loose | 1 | 是 |
| `pathFormatter.otherShare` | - | loose | 1 | 是 |
| `pathFormatter.otherShareFiles` | - | loose | 1 | 是 |
| `pathFormatter.remoteMount` | - | loose | 1 | 是 |
| `pathFormatter.storage` | - | loose | 4 | 是 |
| `pathFormatter.teamFiles` | - | loose | 2 | 是 |
| `pathFormatter.userFiles` | - | loose | 1 | 是 |

## person

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `person.addFailed` | - | loose | 2 | 是 |
| `person.addFailedFileNotFound` | - | loose | 1 | 是 |
| `person.addedSuccess` | - | loose | 1 | 是 |
| `person.clickToAddNamePlaceholder` | - | loose | 1 | 是 |
| `person.clickToEditName` | - | loose | 1 | 是 |
| `person.clickToEditNamePlaceholder` | - | loose | 1 | 是 |
| `person.coverSetSuccess` | - | loose | 2 | 是 |
| `person.createAlbumAndShare` | - | loose | 1 | 是 |
| `person.createAlbumFailed` | - | loose | 1 | 是 |
| `person.createNewPerson` | - | loose | 1 | 是 |
| `person.createPersonSuccess` | - | loose | 1 | 是 |
| `person.done` | - | loose | 2 | 是 |
| `person.editCover` | - | loose | 1 | 是 |
| `person.editName` | - | loose | 1 | 是 |
| `person.getInfoFailed` | - | loose | 1 | 是 |
| `person.hidePerson` | - | loose | 1 | 是 |
| `person.more` | - | loose | 1 | 是 |
| `person.noContent` | - | loose | 1 | 是 |
| `person.notExist` | - | loose | 2 | 是 |
| `person.operationFailed` | - | loose | 4 | 是 |
| `person.photosCount` | - | loose | 1 | 是 |
| `person.removePerson` | - | loose | 1 | 是 |
| `person.saveFailed` | - | loose | 1 | 是 |
| `person.shareExternalLink` | - | loose | 1 | 是 |
| `person.shareToDeviceUsers` | - | loose | 1 | 是 |
| `person.showPerson` | - | loose | 1 | 是 |
| `person.transferPhotoDescription` | - | loose | 1 | 是 |
| `person.unnamedPersonAlbum` | - | loose | 1 | 是 |
| `person.updateSuccess` | - | loose | 1 | 是 |
| `person.videosCount` | - | loose | 1 | 是 |

## persons

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `persons.addName` | - | loose | 1 | 是 |
| `persons.cancel` | - | loose | 1 | 是 |
| `persons.confirm` | - | loose | 1 | 是 |
| `persons.confirmHide` | - | loose | 1 | 是 |
| `persons.confirmRemove` | - | loose | 1 | 是 |
| `persons.editNameTitle` | - | loose | 1 | 是 |
| `persons.hidePersonContent` | - | loose | 1 | 是 |
| `persons.hidePersonTitle` | - | loose | 1 | 是 |
| `persons.hideSuccess` | - | loose | 1 | 是 |
| `persons.itemCount` | - | loose | 1 | 是 |
| `persons.mergeDuplicateNames` | - | loose | 1 | 是 |
| `persons.mergePeople` | - | loose | 2 | 是 |
| `persons.mergeTip` | - | loose | 1 | 是 |
| `persons.nameMaxLength` | - | loose | 1 | 是 |
| `persons.pleaseEnter` | - | loose | 1 | 是 |
| `persons.removeFailed` | - | loose | 1 | 是 |
| `persons.removePersonContent` | - | loose | 1 | 是 |
| `persons.removePersonTitle` | - | loose | 1 | 是 |
| `persons.removeSuccess` | - | loose | 1 | 是 |
| `persons.selectOneForCover` | - | loose | 1 | 是 |
| `persons.showSuccess` | - | loose | 1 | 是 |

## photo

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `photo.read` | - | loose | 1 |  |

## photoHandler

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `photoHandler.deleteConfirm` | - | loose | 1 | 是 |
| `photoHandler.deleteContent` | - | loose | 1 | 是 |
| `photoHandler.deleteCount` | - | loose | 1 | 是 |
| `photoHandler.deleteFailed` | - | loose | 1 | 是 |
| `photoHandler.moveToRecycleBin` | - | loose | 1 | 是 |
| `photoHandler.moveToRecycleBinFailed` | - | loose | 1 | 是 |
| `photoHandler.moveToRecycleBinSuccess` | - | loose | 1 | 是 |
| `photoHandler.photoNotExists` | - | loose | 1 | 是 |
| `photoHandler.remove` | - | loose | 1 | 是 |
| `photoHandler.removeFromAlbumContent` | - | loose | 1 | 是 |
| `photoHandler.removeFromAlbumTitle` | - | loose | 1 | 是 |

## photoWall

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `photoWall.addFolder` | - | loose | 1 | 是 |
| `photoWall.addPhotos.chooseFromComputer` | - | loose | 1 | 是 |
| `photoWall.addPhotos.filterAddedInSearch` | - | loose | 1 | 是 |
| `photoWall.emptySearch.goToSettingsToComplete` | `i18nKey` | alias_key,loose | 2 |  |
| `photoWall.emptySearch.modelNotInstalled` | `i18nKey` | alias_key,loose | 2 |  |
| `photoWall.emptySearch.modelNotInstalledContactAdmin` | - | loose | 1 | 是 |
| `photoWall.emptySearch.noResults` | - | loose | 1 | 是 |
| `photoWall.emptySearch.noResultsAi` | - | loose | 1 | 是 |
| `photoWall.emptySearch.notFoundSimilar` | - | loose | 1 | 是 |
| `photoWall.emptySearch.pleaseCompleteRecognition` | - | loose | 1 | 是 |
| `photoWall.emptySearch.searchFailedContactAdmin` | - | loose | 1 | 是 |
| `photoWall.emptySearch.searchFailedResetModel` | `i18nKey` | alias_key,loose | 2 |  |
| `photoWall.emptySearch.tryTextSearchFull` | `i18nKey` | alias_key,loose | 2 |  |
| `photoWall.saveMemoriesStartUpload` | - | loose | 1 | 是 |
| `photoWall.selectOneAsAlbumCover` | - | loose | 1 | 是 |
| `photoWall.selectedCountShort` | - | loose | 1 | 是 |

## pickFolder

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `pickFolder.title` | - | loose | 2 | 是 |

## preference

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `preference.alwaysPrompt` | - | loose | 1 | 是 |
| `preference.arrangement` | - | loose | 2 | 是 |
| `preference.autoLoadOriginal` | - | loose | 1 | 是 |
| `preference.autoLoadOriginalDesc` | - | loose | 1 | 是 |
| `preference.autoPlayLiveVideo` | - | loose | 1 | 是 |
| `preference.autoPlayLiveVideoDesc` | - | loose | 1 | 是 |
| `preference.backgroundColor` | - | loose | 2 | 是 |
| `preference.darkLightMode` | - | loose | 1 | 是 |
| `preference.fillModes.adaptive` | - | loose | 1 | 是 |
| `preference.fillModes.fill` | - | loose | 1 | 是 |
| `preference.fillModes.stretch` | - | loose | 1 | 是 |
| `preference.keepDuplicate` | - | loose | 1 | 是 |
| `preference.liveWallpaper.description` | - | loose | 1 | 是 |
| `preference.liveWallpaper.title` | - | loose | 1 | 是 |
| `preference.overwrite` | - | loose | 1 | 是 |
| `preference.sameNameHandling` | - | loose | 2 | 是 |
| `preference.sameNameHandlingDesc` | - | loose | 1 | 是 |
| `preference.skip` | - | loose | 1 | 是 |
| `preference.skipDuplicate` | - | loose | 1 | 是 |
| `preference.staticWallpaper.addComputerImage` | - | loose | 1 | 是 |
| `preference.staticWallpaper.addImage` | - | loose | 1 | 是 |
| `preference.staticWallpaper.addNasImage` | - | loose | 1 | 是 |
| `preference.staticWallpaper.deleteFailed` | - | loose | 1 | 是 |
| `preference.staticWallpaper.errorMessages.createDirectoryFailed` | - | loose | 2 | 是 |
| `preference.staticWallpaper.errorMessages.formatError` | - | loose | 2 | 是 |
| `preference.staticWallpaper.errorMessages.insufficientSpace` | - | loose | 2 | 是 |
| `preference.staticWallpaper.errorMessages.paramError` | - | loose | 2 | 是 |
| `preference.staticWallpaper.errorMessages.saveFailed` | - | loose | 2 | 是 |
| `preference.staticWallpaper.errorMessages.sizeLimit` | - | loose | 2 | 是 |
| `preference.staticWallpaper.errorMessages.thumbnailFailed` | - | loose | 2 | 是 |
| `preference.staticWallpaper.fileSizeError` | - | loose | 1 | 是 |
| `preference.staticWallpaper.formatHint` | - | loose | 1 | 是 |
| `preference.staticWallpaper.maxWallpapersError` | - | loose | 4 | 是 |
| `preference.staticWallpaper.selectImage` | - | loose | 1 | 是 |
| `preference.staticWallpaper.title` | - | loose | 1 | 是 |
| `preference.staticWallpaper.uploadSuccess` | - | loose | 1 | 是 |
| `preference.theme` | - | loose | 1 | 是 |
| `preference.themeModes.dark` | - | loose | 1 | 是 |
| `preference.themeModes.light` | - | loose | 1 | 是 |
| `preference.themeModes.system` | - | loose | 1 | 是 |
| `preference.uploadDuplicate` | - | loose | 2 | 是 |
| `preference.uploadDuplicateDesc` | - | loose | 1 | 是 |
| `preference.wallpaper` | - | loose | 1 | 是 |
| `preference.wallpaperTypes.dynamic` | - | loose | 1 | 是 |
| `preference.wallpaperTypes.solidColor` | - | loose | 1 | 是 |
| `preference.wallpaperTypes.static` | - | loose | 1 | 是 |
| `preference.wallpaperTypes.type` | - | loose | 2 | 是 |

## preview

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `preview.addToAlbum` | - | loose | 1 | 是 |
| `preview.modal.editShootingTime` | - | loose | 1 | 是 |
| `preview.modal.selectShootingDateTime` | - | loose | 2 | 是 |
| `preview.modal.selectTimezone` | - | loose | 2 | 是 |
| `preview.modal.shootingDateTime` | - | loose | 1 | 是 |
| `preview.modal.shootingTimeUpdated` | - | loose | 1 | 是 |
| `preview.modal.timezone` | - | loose | 1 | 是 |
| `preview.playSlideshow` | - | loose | 4 | 是 |
| `preview.refreshThumbnailFailed` | - | loose | 1 | 是 |
| `preview.removeAndAddToOtherPerson` | - | loose | 3 | 是 |
| `preview.removeFailed` | - | loose | 1 | 是 |
| `preview.removeFromAlbum` | - | loose | 1 | 是 |
| `preview.removeFromPerson` | - | loose | 2 | 是 |
| `preview.removeFromPersonContent` | - | loose | 1 | 是 |
| `preview.removeOnly` | - | loose | 1 | 是 |
| `preview.removeSuccess` | - | loose | 1 | 是 |
| `preview.setAsPersonCover` | - | loose | 1 | 是 |
| `preview.setPersonCoverFailed` | - | loose | 1 | 是 |
| `preview.sidebar.dateRangeTo` | - | loose | 1 | 是 |
| `preview.sidebar.editLocation` | - | loose | 1 | 是 |
| `preview.sidebar.expand` | - | loose | 2 |  |
| `preview.unfavorite` | - | loose | 2 |  |
| `preview.view` | - | loose | 2 | 是 |

## process

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `process.action.compress` | - | loose | 1 | 是 |
| `process.action.copy` | - | loose | 1 | 是 |
| `process.action.extract` | - | loose | 1 | 是 |
| `process.action.move` | - | loose | 1 | 是 |
| `process.action.remoteUpload` | - | loose | 1 | 是 |
| `process.action.restore` | - | loose | 1 | 是 |
| `process.action.rm` | - | loose | 1 | 是 |
| `process.action.setAcl` | - | loose | 1 | 是 |
| `process.action.shareAdd` | - | loose | 1 | 是 |
| `process.action.shareDel` | - | loose | 1 | 是 |
| `process.action.teamTrashClear` | - | loose | 1 | 是 |
| `process.action.teamTrashRestore` | - | loose | 1 | 是 |
| `process.action.trashClear` | - | loose | 1 | 是 |
| `process.action.trimAclConv` | - | loose | 2 | 是 |
| `process.action.trimAclConvReport` | - | loose | 2 | 是 |
| `process.action.upload` | - | loose | 2 | 是 |
| `process.background` | - | loose | 1 |  |
| `process.calculating` | - | loose | 1 | 是 |
| `process.calculatingWithCount` | - | loose | 1 | 是 |
| `process.calculatingWithTotal` | - | loose | 1 | 是 |
| `process.cancel` | - | loose | 1 | 是 |
| `process.compress` | - | loose | 1 | 是 |
| `process.confirm` | - | loose | 1 |  |
| `process.copy` | - | loose | 1 | 是 |
| `process.delete` | - | loose | 1 | 是 |
| `process.empty` | - | loose | 1 | 是 |
| `process.extract` | - | loose | 1 | 是 |
| `process.failedCount` | - | loose | 1 | 是 |
| `process.failedItems` | - | loose | 1 | 是 |
| `process.failedPart` | - | loose | 1 | 是 |
| `process.failedTip` | - | loose | 2 | 是 |
| `process.handle` | - | loose | 3 | 是 |
| `process.move` | - | loose | 1 | 是 |
| `process.perm` | - | loose | 1 | 是 |
| `process.processing` | - | loose | 1 | 是 |
| `process.processingTitle.compress` | - | loose | 1 | 是 |
| `process.processingTitle.copy` | - | loose | 1 | 是 |
| `process.processingTitle.delete` | - | loose | 1 | 是 |
| `process.processingTitle.empty` | - | loose | 1 | 是 |
| `process.processingTitle.extract` | - | loose | 1 | 是 |
| `process.processingTitle.move` | - | loose | 1 | 是 |
| `process.processingTitle.perm` | - | loose | 1 | 是 |
| `process.processingTitle.restore` | - | loose | 1 | 是 |
| `process.processingTitle.trimAclConv` | - | loose | 1 | 是 |
| `process.processingTitle.trimAclConvReport` | - | loose | 1 | 是 |
| `process.progressWithCount` | - | loose | 1 | 是 |
| `process.progressWithSize` | - | loose | 1 | 是 |
| `process.remaining` | - | loose | 1 | 是 |
| `process.restore` | - | loose | 1 | 是 |
| `process.view` | - | loose | 1 | 是 |

## props

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `props.block` | - | loose | 2 |  |
| `props.className` | - | loose | 4 |  |
| `props.disabled` | - | loose | 2 |  |
| `props.loading` | - | loose | 2 |  |
| `props.onKeyDown` | - | loose | 2 |  |
| `props.style` | - | loose | 4 |  |
| `props.style.display` | - | loose | 2 |  |

## rangeInputEndRef

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `rangeInputEndRef.current` | - | loose | 6 |  |

## rangeInputStartRef

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `rangeInputStartRef.current` | - | loose | 6 |  |

## react

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `react.context` | - | loose | 4 | 是 |
| `react.element` | - | loose | 8 | 是 |
| `react.forward_ref` | - | loose | 7 | 是 |
| `react.fragment` | - | loose | 6 | 是 |
| `react.lazy` | - | loose | 4 | 是 |
| `react.memo` | - | loose | 10 | 是 |
| `react.offscreen` | - | loose | 2 | 是 |
| `react.portal` | - | loose | 4 | 是 |
| `react.profiler` | - | loose | 4 | 是 |
| `react.provider` | - | loose | 4 | 是 |
| `react.strict_mode` | - | loose | 4 | 是 |
| `react.suspense` | - | loose | 4 | 是 |
| `react.suspense_list` | - | loose | 2 | 是 |

## recentRecord

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `recentRecord.clearAllRecord` | - | loose | 1 | 是 |
| `recentRecord.clearRecord` | - | loose | 1 | 是 |

## reconnect

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `reconnect.accessExceptionDesc` | - | loose | 1 | 是 |
| `reconnect.accessExceptionTitle` | - | loose | 1 | 是 |
| `reconnect.checkHardwareConnection` | - | loose | 1 | 是 |
| `reconnect.confirmReconnect` | - | loose | 1 | 是 |
| `reconnect.matchFailedContent` | - | loose | 1 | 是 |
| `reconnect.matchFailedTitle` | - | loose | 1 | 是 |
| `reconnect.reconnectFailed` | - | loose | 2 | 是 |
| `reconnect.reconnectFolder` | - | loose | 1 | 是 |
| `reconnect.reconnectManually` | - | loose | 1 | 是 |
| `reconnect.reconnectSuccess` | - | loose | 2 | 是 |
| `reconnect.scan` | - | loose | 1 | 是 |
| `reconnect.selectFolder` | - | loose | 1 | 是 |
| `reconnect.unmatchedDataWarning` | - | loose | 1 | 是 |

## remoteConnection

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `remoteConnection.action.mountCloud` | - | loose | 1 | 是 |
| `remoteConnection.action.mountFolder` | - | loose | 1 | 是 |
| `remoteConnection.action.setting` | - | loose | 1 | 是 |
| `remoteConnection.details.assignedPath` | - | loose | 1 | 是 |
| `remoteConnection.details.bytes` | - | loose | 2 | 是 |
| `remoteConnection.details.calcFailed` | - | loose | 1 | 是 |
| `remoteConnection.details.calculating` | - | loose | 1 | 是 |
| `remoteConnection.details.count` | - | loose | 2 |  |
| `remoteConnection.details.fileCount` | - | loose | 1 | 是 |
| `remoteConnection.details.host` | - | loose | 1 | 是 |
| `remoteConnection.details.location` | - | loose | 1 | 是 |
| `remoteConnection.details.originalPath` | - | loose | 1 | 是 |
| `remoteConnection.details.port` | - | loose | 1 | 是 |
| `remoteConnection.details.security` | - | loose | 1 | 是 |
| `remoteConnection.details.size` | - | loose | 3 | 是 |
| `remoteConnection.details.space` | - | loose | 1 | 是 |
| `remoteConnection.details.totalContains` | - | loose | 1 | 是 |
| `remoteConnection.details.type` | - | loose | 1 | 是 |
| `remoteConnection.details.username` | - | loose | 1 | 是 |
| `remoteConnection.detailsApp.title` | - | loose | 1 | 是 |
| `remoteConnection.disconnectModal.cancel` | - | loose | 1 | 是 |
| `remoteConnection.disconnectModal.content` | `i18nKey` | alias_key,loose | 2 |  |
| `remoteConnection.disconnectModal.ok` | - | loose | 1 |  |
| `remoteConnection.disconnectModal.okLoading` | - | loose | 1 |  |
| `remoteConnection.disconnectModal.title` | - | loose | 1 | 是 |
| `remoteConnection.error.default.connectionFailed` | - | loose | 1 | 是 |
| `remoteConnection.error.default.fileFailed` | - | loose | 1 | 是 |
| `remoteConnection.error.reAuth.button` | - | loose | 1 | 是 |
| `remoteConnection.error.reAuth.title` | - | loose | 1 | 是 |
| `remoteConnection.noData.default` | - | loose | 1 | 是 |
| `remoteConnection.noData.search` | - | loose | 1 | 是 |
| `remoteConnection.removeModal.cancel` | - | loose | 1 | 是 |
| `remoteConnection.removeModal.content` | `i18nKey` | alias_key,loose | 2 |  |
| `remoteConnection.removeModal.failed` | - | loose | 1 | 是 |
| `remoteConnection.removeModal.ok` | - | loose | 1 |  |
| `remoteConnection.removeModal.okLoading` | - | loose | 1 |  |
| `remoteConnection.removeModal.success` | - | loose | 1 | 是 |
| `remoteConnection.removeModal.title` | - | loose | 1 | 是 |
| `remoteConnection.searchPlaceholder` | - | loose | 1 | 是 |
| `remoteConnection.searchPlaceholderMountName` | - | loose | 1 | 是 |
| `remoteConnection.service.actionFailed` | - | loose | 1 | 是 |
| `remoteConnection.service.actionSuccess` | - | loose | 1 | 是 |
| `remoteConnection.service.connect` | - | loose | 1 |  |
| `remoteConnection.service.disconnect` | - | loose | 1 |  |
| `remoteConnection.status.connecting` | - | loose | 2 | 是 |
| `remoteConnection.status.disconnected` | - | loose | 1 | 是 |
| `remoteConnection.status.disconnecting` | - | loose | 1 |  |

## remoteDeviceConnector

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `remoteDeviceConnector.authExpired` | - | loose | 1 | 是 |
| `remoteDeviceConnector.authFailed` | - | loose | 1 | 是 |
| `remoteDeviceConnector.cloudServiceIntro` | - | loose | 1 |  |
| `remoteDeviceConnector.cloudServiceTips.general` | - | loose | 10 | 是 |
| `remoteDeviceConnector.cloudServiceTips.membershipStatus` | - | loose | 3 | 是 |
| `remoteDeviceConnector.cloudServiceTips.oneTwoThreeLimit` | - | loose | 1 | 是 |
| `remoteDeviceConnector.cloudServiceTips.policy` | - | loose | 10 | 是 |
| `remoteDeviceConnector.comingSoon` | - | loose | 1 | 是 |
| `remoteDeviceConnector.commentTooLong` | - | loose | 1 | 是 |
| `remoteDeviceConnector.confirm` | - | loose | 1 |  |
| `remoteDeviceConnector.connect` | - | loose | 1 |  |
| `remoteDeviceConnector.connecting` | - | loose | 2 | 是 |
| `remoteDeviceConnector.connecting2` | - | loose | 1 | 是 |
| `remoteDeviceConnector.connectionFailed` | - | loose | 1 | 是 |
| `remoteDeviceConnector.defaultDialogTitle` | - | loose | 2 | 是 |
| `remoteDeviceConnector.defaultIntro` | - | loose | 1 |  |
| `remoteDeviceConnector.domainOrIP` | - | loose | 1 | 是 |
| `remoteDeviceConnector.fileSharingIntro` | - | loose | 1 |  |
| `remoteDeviceConnector.fileSharingProtocol` | - | loose | 1 | 是 |
| `remoteDeviceConnector.invalidRange` | - | loose | 1 | 是 |
| `remoteDeviceConnector.membershipLinks.oneTwoThree` | - | loose | 1 | 是 |
| `remoteDeviceConnector.modify` | - | loose | 1 |  |
| `remoteDeviceConnector.mountCloudStorage` | - | loose | 1 |  |
| `remoteDeviceConnector.mountDirectory` | - | loose | 1 | 是 |
| `remoteDeviceConnector.mountName` | - | loose | 1 | 是 |
| `remoteDeviceConnector.mountPoint` | - | loose | 1 | 是 |
| `remoteDeviceConnector.mountRemoteFolder` | - | loose | 1 |  |
| `remoteDeviceConnector.mountSuccess` | - | loose | 1 | 是 |
| `remoteDeviceConnector.nextStep` | - | loose | 1 |  |
| `remoteDeviceConnector.notice` | - | loose | 10 | 是 |
| `remoteDeviceConnector.operationAbnormal` | - | loose | 1 | 是 |
| `remoteDeviceConnector.password` | - | loose | 1 | 是 |
| `remoteDeviceConnector.pathMustStartWithSlash` | - | loose | 1 | 是 |
| `remoteDeviceConnector.placeholder.comment` | - | loose | 1 | 是 |
| `remoteDeviceConnector.placeholder.domainOrIP` | - | loose | 1 | 是 |
| `remoteDeviceConnector.placeholder.passwordOptional` | - | loose | 1 |  |
| `remoteDeviceConnector.placeholder.passwordRequired` | - | loose | 1 |  |
| `remoteDeviceConnector.placeholder.port` | - | loose | 1 | 是 |
| `remoteDeviceConnector.placeholder.rootPath` | - | loose | 1 | 是 |
| `remoteDeviceConnector.placeholder.usernameOptional` | - | loose | 1 |  |
| `remoteDeviceConnector.placeholder.usernameRequired` | - | loose | 1 |  |
| `remoteDeviceConnector.pleaseCheckForm` | - | loose | 1 | 是 |
| `remoteDeviceConnector.pleaseSelectConnectionType` | - | loose | 1 | 是 |
| `remoteDeviceConnector.port` | - | loose | 1 | 是 |
| `remoteDeviceConnector.queryListFailed` | - | loose | 1 | 是 |
| `remoteDeviceConnector.reAuth` | - | loose | 1 | 是 |
| `remoteDeviceConnector.search` | - | loose | 1 | 是 |
| `remoteDeviceConnector.security` | - | loose | 1 | 是 |
| `remoteDeviceConnector.selectMountPoint` | - | loose | 1 | 是 |
| `remoteDeviceConnector.sftpRootWarning` | - | loose | 1 | 是 |
| `remoteDeviceConnector.specifiedPath` | - | loose | 1 | 是 |
| `remoteDeviceConnector.specifyMountPath` | - | loose | 1 | 是 |
| `remoteDeviceConnector.submitting` | - | loose | 2 | 是 |
| `remoteDeviceConnector.thirdPartyCloudService` | - | loose | 1 | 是 |
| `remoteDeviceConnector.username` | - | loose | 1 | 是 |

## remoteMount

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `remoteMount.cacheStorage.description` | - | loose | 1 | 是 |
| `remoteMount.cacheStorage.noStorage` | - | loose | 1 | 是 |
| `remoteMount.cacheStorage.setFailed` | - | loose | 1 | 是 |
| `remoteMount.cacheStorage.setSuccess` | - | loose | 1 | 是 |
| `remoteMount.cacheStorage.storageLabel` | - | loose | 1 | 是 |
| `remoteMount.cacheStorage.title` | - | loose | 1 | 是 |

## rowSelection

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `rowSelection.width` | - | loose | 1 |  |

## scroll

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `scroll.y` | - | loose | 1 |  |

## search

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `search.aiPromptWithExample` | - | loose | 2 | 是 |
| `search.aiSearch` | - | loose | 2 |  |
| `search.aiSearching` | - | loose | 1 | 是 |
| `search.conditionalSearch` | - | loose | 2 |  |
| `search.dateFormat.dayOnly` | - | loose | 2 | 是 |
| `search.dateFormat.monthOnly` | - | loose | 2 | 是 |
| `search.dateFormat.yearMonth` | - | loose | 1 | 是 |
| `search.dateFormat.yearOnly` | - | loose | 3 | 是 |
| `search.dateSuffix.month` | - | loose | 1 | 是 |
| `search.dateSuffix.year` | - | loose | 1 | 是 |
| `search.disableAISearchMotion` | - | loose | 1 |  |
| `search.enableAISearchMotion` | - | loose | 1 |  |
| `search.favorited` | - | loose | 5 | 是 |
| `search.fetchResultsFailedRebuildIndex` | - | loose | 1 | 是 |
| `search.filters.album` | - | loose | 2 | 是 |
| `search.filters.aperture` | - | loose | 2 | 是 |
| `search.filters.cameraMake` | - | loose | 2 | 是 |
| `search.filters.exposureTime` | - | loose | 2 | 是 |
| `search.filters.focalLength` | - | loose | 2 | 是 |
| `search.filters.folder` | - | loose | 2 | 是 |
| `search.filters.folderTip` | - | loose | 2 | 是 |
| `search.filters.iso` | - | loose | 2 | 是 |
| `search.filters.location` | - | loose | 2 | 是 |
| `search.filters.organize` | - | loose | 2 | 是 |
| `search.filters.person` | - | loose | 2 | 是 |
| `search.filters.searchOptions` | - | loose | 1 | 是 |
| `search.filters.selectAlbum` | - | loose | 2 | 是 |
| `search.filters.selectAperture` | - | loose | 2 | 是 |
| `search.filters.selectCameraMake` | - | loose | 2 | 是 |
| `search.filters.selectExposureTime` | - | loose | 2 | 是 |
| `search.filters.selectFocalLength` | - | loose | 2 | 是 |
| `search.filters.selectFolder` | - | loose | 2 | 是 |
| `search.filters.selectISO` | - | loose | 2 | 是 |
| `search.filters.selectLocation` | - | loose | 2 | 是 |
| `search.filters.selectPerson` | - | loose | 2 | 是 |
| `search.filters.selectShootingTime` | - | loose | 2 | 是 |
| `search.filters.selectType` | - | loose | 2 | 是 |
| `search.filters.shootingInfo` | - | loose | 1 | 是 |
| `search.filters.shootingTime` | - | loose | 2 | 是 |
| `search.filters.tag` | - | loose | 2 | 是 |
| `search.filters.type` | - | loose | 2 | 是 |
| `search.installed` | - | loose | 1 | 是 |
| `search.loadingAIModel` | - | loose | 1 | 是 |
| `search.noLocation` | - | loose | 3 | 是 |
| `search.noSearchResult` | - | loose | 1 | 是 |
| `search.noTags` | - | loose | 3 | 是 |
| `search.notInAlbum` | - | loose | 3 | 是 |
| `search.notInstalled` | - | loose | 1 | 是 |
| `search.openInFolderView` | - | loose | 1 | 是 |
| `search.placeholder` | - | loose | 1 | 是 |
| `search.resultCount` | - | loose | 1 | 是 |
| `search.searchFailed` | - | loose | 1 | 是 |
| `search.searchPlaceholder` | - | loose | 2 | 是 |
| `search.searchResult` | - | loose | 1 | 是 |
| `search.searchSimilarPhotos` | - | loose | 1 | 是 |
| `search.supportFileType` | - | loose | 1 | 是 |
| `search.supportFileTypePrefix` | - | loose | 1 | 是 |
| `search.switchToAISearch` | - | loose | 1 |  |
| `search.switchToConditionalSearch` | - | loose | 1 |  |

## semi

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `semi.form.required` | - | loose | 1 | 是 |

## settingAI

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `settingAI.advancedSettings` | - | loose | 2 | 是 |
| `settingAI.available` | - | loose | 1 | 是 |
| `settingAI.callSuccess` | - | loose | 1 | 是 |
| `settingAI.cancelDownload` | - | loose | 1 | 是 |
| `settingAI.canceling` | - | loose | 1 | 是 |
| `settingAI.checking` | - | loose | 2 | 是 |
| `settingAI.copyMagnetLink` | - | loose | 2 | 是 |
| `settingAI.copySuccess` | - | loose | 2 | 是 |
| `settingAI.cpu` | - | loose | 2 | 是 |
| `settingAI.description` | `i18nKey` | alias_key,loose | 2 |  |
| `settingAI.deviceBuiltIn` | - | loose | 2 | 是 |
| `settingAI.deviceCheck` | - | loose | 2 | 是 |
| `settingAI.disabledAIMessage` | - | loose | 1 | 是 |
| `settingAI.downloadInstallFailed` | - | loose | 2 | 是 |
| `settingAI.downloadSlowWarning` | - | loose | 2 | 是 |
| `settingAI.downloading` | - | loose | 1 | 是 |
| `settingAI.enableGPU` | - | loose | 1 | 是 |
| `settingAI.enableGPUDesc` | - | loose | 1 | 是 |
| `settingAI.extracting` | - | loose | 1 | 是 |
| `settingAI.faceRecognition` | - | loose | 2 | 是 |
| `settingAI.faceRecognitionDesc` | - | loose | 1 | 是 |
| `settingAI.faceRecognitionDescInstalled` | - | loose | 1 | 是 |
| `settingAI.faceRecognitionTaskAdded` | - | loose | 1 | 是 |
| `settingAI.gpu` | - | loose | 3 | 是 |
| `settingAI.hardwareCheckFailedMessage` | - | loose | 1 | 是 |
| `settingAI.hooks.cancelInstallFailed` | - | loose | 2 | 是 |
| `settingAI.hooks.cancelInstallSuccess` | - | loose | 2 | 是 |
| `settingAI.hooks.confirmResetFaceRecognition` | - | loose | 1 | 是 |
| `settingAI.hooks.confirmResetSmartRecognition` | - | loose | 1 | 是 |
| `settingAI.hooks.confirmUninstallFaceRecognitionModel` | - | loose | 1 | 是 |
| `settingAI.hooks.confirmUninstallSmartRecognitionModel` | - | loose | 1 | 是 |
| `settingAI.hooks.confirmUpdateSmartCategory` | - | loose | 1 | 是 |
| `settingAI.hooks.enableFailedNoGPU` | - | loose | 1 | 是 |
| `settingAI.hooks.faceRecognitionTaskAdded` | - | loose | 2 | 是 |
| `settingAI.hooks.gpuCallFailed` | - | loose | 1 | 是 |
| `settingAI.hooks.gpuCallFailedCheckDriver` | - | loose | 1 | 是 |
| `settingAI.hooks.gpuCallFailedInstallAmdMIGraphXAndROCm` | - | loose | 1 | 是 |
| `settingAI.hooks.gpuCloseFailed` | - | loose | 1 | 是 |
| `settingAI.hooks.gpuCloseSuccess` | - | loose | 1 | 是 |
| `settingAI.hooks.gpuSetSuccess` | - | loose | 1 | 是 |
| `settingAI.hooks.installFailed` | - | loose | 4 | 是 |
| `settingAI.hooks.insufficientStorage` | - | loose | 1 | 是 |
| `settingAI.hooks.modelInstallCompleteFaceRecognition` | - | loose | 1 | 是 |
| `settingAI.hooks.modelInstallCompleteSmartRecognition` | - | loose | 1 | 是 |
| `settingAI.hooks.noUnrecognizedVideos` | - | loose | 1 | 是 |
| `settingAI.hooks.resetFaceRecognition` | - | loose | 1 | 是 |
| `settingAI.hooks.resetSmartRecognition` | - | loose | 1 | 是 |
| `settingAI.hooks.selectModelFile` | - | loose | 2 | 是 |
| `settingAI.hooks.selectModelFileFirst` | - | loose | 2 | 是 |
| `settingAI.hooks.selectModelFirst` | - | loose | 2 | 是 |
| `settingAI.hooks.setFailed` | - | loose | 13 | 是 |
| `settingAI.hooks.setStorageFailed` | - | loose | 1 | 是 |
| `settingAI.hooks.smartRecognitionTaskAdded` | - | loose | 2 | 是 |
| `settingAI.hooks.uninstallFaceRecognitionModel` | - | loose | 1 | 是 |
| `settingAI.hooks.uninstallFailed` | - | loose | 2 | 是 |
| `settingAI.hooks.uninstallSmartRecognitionModel` | - | loose | 1 | 是 |
| `settingAI.hooks.uninstallSuccess` | - | loose | 2 | 是 |
| `settingAI.hooks.updateSmartCategory` | - | loose | 1 | 是 |
| `settingAI.hooks.updateSmartCategoryFailed` | - | loose | 1 | 是 |
| `settingAI.hooks.updateSmartCategoryTaskAdded` | - | loose | 1 | 是 |
| `settingAI.hooks.videoEnhancedRecognitionTaskAdded` | - | loose | 1 | 是 |
| `settingAI.importFromNAS` | - | loose | 2 | 是 |
| `settingAI.importFromNASDesc` | - | loose | 2 | 是 |
| `settingAI.installModel` | - | loose | 2 | 是 |
| `settingAI.installedIn` | - | loose | 2 | 是 |
| `settingAI.installing` | - | loose | 1 | 是 |
| `settingAI.memory` | - | loose | 2 | 是 |
| `settingAI.modal.confirmReAggregatePerson` | - | loose | 1 |  |
| `settingAI.modal.confirmReRunFaceRecognition` | - | loose | 1 |  |
| `settingAI.modal.custom` | - | loose | 1 | 是 |
| `settingAI.modal.detConfidenceDesc` | - | loose | 1 | 是 |
| `settingAI.modal.detConfidenceRange` | - | loose | 1 | 是 |
| `settingAI.modal.detConfidenceThreshold` | - | loose | 1 | 是 |
| `settingAI.modal.epsDesc` | `i18nKey` | alias_key,loose | 2 |  |
| `settingAI.modal.epsRange` | - | loose | 1 | 是 |
| `settingAI.modal.epsThreshold` | - | loose | 1 | 是 |
| `settingAI.modal.faceRecognitionSettings` | - | loose | 1 | 是 |
| `settingAI.modal.minSamples` | - | loose | 1 | 是 |
| `settingAI.modal.minSamplesDesc` | - | loose | 1 | 是 |
| `settingAI.modal.minSamplesRange` | - | loose | 1 | 是 |
| `settingAI.modal.pleaseInput` | - | loose | 4 | 是 |
| `settingAI.modal.reAggregatePerson` | - | loose | 1 |  |
| `settingAI.modal.reRunFaceRecognition` | - | loose | 1 |  |
| `settingAI.modal.restoreDefault` | - | loose | 4 | 是 |
| `settingAI.modal.setFailed` | - | loose | 3 | 是 |
| `settingAI.modal.setSuccess` | - | loose | 2 | 是 |
| `settingAI.modal.setSuccessFaceRecognition` | - | loose | 1 |  |
| `settingAI.modal.setSuccessPersonAggregation` | - | loose | 1 |  |
| `settingAI.modal.similarityThreshold` | - | loose | 1 | 是 |
| `settingAI.modal.similarityThresholdDesc` | - | loose | 1 | 是 |
| `settingAI.modal.similarityThresholdRange` | - | loose | 1 | 是 |
| `settingAI.modal.smartRecognitionSettings` | - | loose | 1 | 是 |
| `settingAI.model` | - | loose | 2 | 是 |
| `settingAI.modelInstallLocation` | - | loose | 1 | 是 |
| `settingAI.moreDownloadMethods` | - | loose | 2 | 是 |
| `settingAI.onlineDownload` | - | loose | 2 | 是 |
| `settingAI.personSimilarityPreference` | - | loose | 1 | 是 |
| `settingAI.pleaseSelect` | - | loose | 2 | 是 |
| `settingAI.preparingDownload` | - | loose | 1 | 是 |
| `settingAI.resetFaceRecognition` | - | loose | 1 | 是 |
| `settingAI.resetSmartRecognition` | - | loose | 1 | 是 |
| `settingAI.retryHardwareCheck` | - | loose | 1 | 是 |
| `settingAI.runUnrecognizedPhotos` | - | loose | 2 | 是 |
| `settingAI.runUnrecognizedVideos` | - | loose | 1 | 是 |
| `settingAI.selectModelFile` | - | loose | 2 | 是 |
| `settingAI.selectModelInstall` | - | loose | 2 | 是 |
| `settingAI.selectStorage` | - | loose | 1 | 是 |
| `settingAI.selectStorageFirst` | - | loose | 4 | 是 |
| `settingAI.smartRecTaskAdded` | - | loose | 1 | 是 |
| `settingAI.smartRecognition` | - | loose | 2 | 是 |
| `settingAI.smartRecognitionDesc` | - | loose | 1 | 是 |
| `settingAI.smartRecognitionDescInstalled` | - | loose | 1 | 是 |
| `settingAI.storageRequirement` | - | loose | 1 | 是 |
| `settingAI.storageSpace` | - | loose | 4 | 是 |
| `settingAI.testing` | - | loose | 1 | 是 |
| `settingAI.thunderDownloadBasic` | - | loose | 1 |  |
| `settingAI.thunderDownloadEnhanced` | - | loose | 1 |  |
| `settingAI.thunderDownloadFaceModel` | - | loose | 1 | 是 |
| `settingAI.uninstallModel` | - | loose | 2 | 是 |
| `settingAI.updateSmartCategory` | - | loose | 1 | 是 |
| `settingAI.utils.epsCustom` | - | loose | 1 | 是 |
| `settingAI.utils.epsDefault` | - | loose | 1 | 是 |
| `settingAI.utils.epsDefaultDesc` | - | loose | 1 | 是 |
| `settingAI.utils.epsLoose` | - | loose | 1 | 是 |
| `settingAI.utils.epsLooseDesc` | - | loose | 1 | 是 |
| `settingAI.utils.modelNotInstalled` | - | loose | 1 | 是 |
| `settingAI.utils.noUnrecognizedPhotos` | - | loose | 1 | 是 |
| `settingAI.utils.taskInProgress` | - | loose | 1 | 是 |
| `settingAI.validating` | - | loose | 1 | 是 |
| `settingAI.videoEnhancedRecognition` | - | loose | 2 | 是 |
| `settingAI.videoEnhancedRecognitionDesc` | - | loose | 1 | 是 |
| `settingAI.viewInstructions` | - | loose | 1 | 是 |

## settings

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `settings.askBeforeInstall` | - | loose | 1 | 是 |
| `settings.autoRunNewApp` | - | loose | 1 | 是 |
| `settings.autoUpdateDescriptionNextDay` | - | loose | 1 |  |
| `settings.autoUpdateDescriptionSameDay` | - | loose | 1 |  |
| `settings.balancedMode` | - | loose | 1 | 是 |
| `settings.balancedModeDescription` | - | loose | 1 | 是 |
| `settings.checkTime` | - | loose | 1 | 是 |
| `settings.checkTimeRequired` | - | loose | 1 | 是 |
| `settings.cloudSecurityStrategy` | - | loose | 1 | 是 |
| `settings.cloudSecurityStrategyRequired` | - | loose | 1 | 是 |
| `settings.cloudSecuritySync` | - | loose | 1 | 是 |
| `settings.downloadAndInstallVolume` | - | loose | 1 | 是 |
| `settings.enableAutoUpdate` | - | loose | 1 | 是 |
| `settings.folderManager` | - | loose | 1 | 是 |
| `settings.global` | - | loose | 1 | 是 |
| `settings.lenientMode` | - | loose | 1 | 是 |
| `settings.lenientModeDescription` | - | loose | 1 | 是 |
| `settings.minimumWindow` | - | loose | 1 | 是 |
| `settings.preference` | - | loose | 1 | 是 |
| `settings.saveSuccess` | - | loose | 1 | 是 |
| `settings.settingAI` | - | loose | 1 | 是 |
| `settings.storageSpace` | - | loose | 2 | 是 |
| `settings.storageUnavailable` | - | loose | 2 | 是 |
| `settings.strategyPlaceholder` | - | loose | 1 | 是 |
| `settings.strictMode` | - | loose | 1 | 是 |
| `settings.strictModeDescription` | - | loose | 1 | 是 |

## share

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `share.add` | - | loose | 1 | 是 |
| `share.addAccount` | - | loose | 1 | 是 |
| `share.cancel` | - | loose | 1 | 是 |
| `share.cancelShare` | - | loose | 1 | 是 |
| `share.cancelShareFailed` | - | loose | 1 | 是 |
| `share.cancelShareSuccess` | - | loose | 1 | 是 |
| `share.confirm` | - | loose | 2 | 是 |
| `share.noSearchResult` | - | loose | 1 | 是 |
| `share.noShareAccount` | - | loose | 1 | 是 |
| `share.openShare` | - | loose | 1 |  |
| `share.preview.permissionText` | - | loose | 1 | 是 |
| `share.searchPlaceholder` | - | loose | 1 | 是 |
| `share.selectShareAccount` | - | loose | 1 | 是 |
| `share.shareFailed` | - | loose | 1 | 是 |
| `share.shareName` | - | loose | 1 | 是 |
| `share.shareScope` | - | loose | 1 | 是 |
| `share.shareSettings` | - | loose | 1 |  |
| `share.shareSuccess` | - | loose | 1 | 是 |
| `share.title` | - | loose | 1 |  |
| `share.user` | - | loose | 1 | 是 |
| `share.userGroup` | - | loose | 1 | 是 |

## shareAlbum

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `shareAlbum.babyAlbum` | - | loose | 1 | 是 |
| `shareAlbum.cancel` | - | loose | 1 | 是 |
| `shareAlbum.closeSharing` | - | loose | 1 | 是 |
| `shareAlbum.copyLink` | - | loose | 2 | 是 |
| `shareAlbum.copyLinkWithPassword` | - | loose | 2 | 是 |
| `shareAlbum.createExternalLink` | - | loose | 1 | 是 |
| `shareAlbum.delete` | - | loose | 2 | 是 |
| `shareAlbum.edit` | - | loose | 2 | 是 |
| `shareAlbum.expiresAt` | - | loose | 2 | 是 |
| `shareAlbum.externalLink` | - | loose | 1 | 是 |
| `shareAlbum.itemCount` | - | loose | 2 | 是 |
| `shareAlbum.linkExpired` | - | loose | 2 | 是 |
| `shareAlbum.linkInvalid` | - | loose | 2 | 是 |
| `shareAlbum.longTerm` | - | loose | 2 | 是 |
| `shareAlbum.noShareLinks` | - | loose | 2 | 是 |
| `shareAlbum.noSharedAlbums` | - | loose | 2 | 是 |
| `shareAlbum.viewAllExternalLinks` | - | loose | 1 | 是 |

## shareLink

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `shareLink.action.clearRecord` | - | loose | 1 | 是 |
| `shareLink.action.delLink` | - | loose | 1 | 是 |
| `shareLink.action.editLink` | - | loose | 1 | 是 |
| `shareLink.action.setting` | - | loose | 1 | 是 |
| `shareLink.adminOnlyTip` | - | loose | 1 | 是 |
| `shareLink.field.access` | - | loose | 3 | 是 |
| `shareLink.field.createdTime` | - | loose | 3 | 是 |
| `shareLink.field.name` | - | loose | 3 | 是 |
| `shareLink.field.remainingAccess` | - | loose | 3 | 是 |
| `shareLink.field.status` | - | loose | 2 | 是 |
| `shareLink.field.type` | - | loose | 3 | 是 |
| `shareLink.field.username` | - | loose | 3 | 是 |
| `shareLink.field.validTo` | - | loose | 3 | 是 |
| `shareLink.fileCollectionPermissionMode.adminOnly` | - | loose | 1 | 是 |
| `shareLink.fileCollectionPermissionMode.allUsers` | - | loose | 1 | 是 |
| `shareLink.fileCollectionPermissionMode.setFailed` | - | loose | 1 | 是 |
| `shareLink.fileCollectionPermissionMode.title` | - | loose | 2 | 是 |
| `shareLink.handler.clear.cancel` | - | loose | 1 | 是 |
| `shareLink.handler.clear.confirm` | - | loose | 1 | 是 |
| `shareLink.handler.clear.content` | - | loose | 1 | 是 |
| `shareLink.handler.clear.error` | - | loose | 1 | 是 |
| `shareLink.handler.clear.noData` | - | loose | 1 | 是 |
| `shareLink.handler.clear.success` | - | loose | 1 | 是 |
| `shareLink.handler.clear.title` | - | loose | 1 | 是 |
| `shareLink.handler.delete.cancel` | - | loose | 1 | 是 |
| `shareLink.handler.delete.confirm` | - | loose | 1 | 是 |
| `shareLink.handler.delete.content` | `i18nKey` | alias_key,loose | 2 |  |
| `shareLink.handler.delete.contentMultiple` | - | loose | 1 | 是 |
| `shareLink.handler.delete.error` | - | loose | 1 | 是 |
| `shareLink.handler.delete.success` | - | loose | 1 | 是 |
| `shareLink.handler.delete.title` | - | loose | 1 | 是 |
| `shareLink.handler.delete.warning` | - | loose | 1 | 是 |
| `shareLink.noSearchResult` | - | loose | 1 |  |
| `shareLink.noShareLink` | - | loose | 1 | 是 |
| `shareLink.noShareLinkEmpty` | - | loose | 1 |  |
| `shareLink.noSharePermission` | - | loose | 1 | 是 |
| `shareLink.permissionMode.adminOnly` | - | loose | 1 | 是 |
| `shareLink.permissionMode.allUsers` | - | loose | 1 | 是 |
| `shareLink.permissionMode.setFailed` | - | loose | 1 | 是 |
| `shareLink.permissionMode.title` | - | loose | 2 | 是 |
| `shareLink.searchPlaceholder` | - | loose | 1 | 是 |
| `shareLink.selectedTotalText` | - | loose | 1 | 是 |
| `shareLink.settingTip.description` | - | loose | 1 | 是 |
| `shareLink.settingTip.remoteAccess` | - | loose | 1 | 是 |
| `shareLink.settingTip.shareLink` | - | loose | 1 | 是 |
| `shareLink.settingTip.suffix` | - | loose | 1 | 是 |
| `shareLink.settingTip.systemSetting` | - | loose | 1 | 是 |
| `shareLink.settingTip.title` | - | loose | 1 | 是 |
| `shareLink.status.exceeded` | - | loose | 1 | 是 |
| `shareLink.status.expired` | - | loose | 1 | 是 |
| `shareLink.status.invalid` | - | loose | 1 | 是 |
| `shareLink.status.noAccess` | - | loose | 1 | 是 |
| `shareLink.status.noFiles` | - | loose | 1 | 是 |
| `shareLink.status.noPermission` | - | loose | 1 | 是 |
| `shareLink.status.permanent` | - | loose | 1 | 是 |
| `shareLink.status.times` | - | loose | 2 | 是 |
| `shareLink.status.unlimited` | - | loose | 1 | 是 |
| `shareLink.status.userException` | - | loose | 1 | 是 |
| `shareLink.status.valid` | - | loose | 3 | 是 |
| `shareLink.title` | - | loose | 1 | 是 |
| `shareLink.totalText` | - | loose | 1 | 是 |
| `shareLink.type.collection` | - | loose | 1 | 是 |
| `shareLink.type.share` | - | loose | 1 | 是 |

## shared

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `shared.action.default.cancel` | - | loose | 2 | 是 |
| `shared.action.default.default` | - | loose | 2 | 是 |
| `shared.action.default.doing` | - | loose | 3 | 是 |
| `shared.action.default.failed` | - | loose | 2 | 是 |
| `shared.action.default.success` | - | loose | 1 | 是 |
| `shared.action.delete.default` | - | loose | 1 | 是 |
| `shared.action.delete.doing` | - | loose | 1 | 是 |
| `shared.action.delete.failed` | - | loose | 1 | 是 |
| `shared.action.delete.success` | - | loose | 1 | 是 |
| `shared.action.export.default` | - | loose | 1 | 是 |
| `shared.action.export.doing` | - | loose | 1 | 是 |
| `shared.action.export.failed` | - | loose | 1 | 是 |
| `shared.action.export.success` | - | loose | 1 | 是 |
| `shared.action.stop.default` | - | loose | 2 |  |
| `shared.action.umount.default` | - | loose | 1 | 是 |
| `shared.action.umount.doing` | - | loose | 1 | 是 |
| `shared.action.umount.failed` | - | loose | 1 | 是 |
| `shared.action.umount.success` | - | loose | 1 | 是 |
| `shared.action.umountAndExport.default` | - | loose | 1 | 是 |
| `shared.action.umountAndExport.doing` | - | loose | 1 | 是 |
| `shared.action.umountAndExport.failed` | - | loose | 1 | 是 |
| `shared.action.umountAndExport.success` | - | loose | 1 | 是 |
| `shared.passwordError` | - | loose | 1 | 是 |

## sidebar

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `sidebar.albums` | - | loose | 1 | 是 |
| `sidebar.collapse` | - | loose | 4 | 是 |
| `sidebar.duplicates` | - | loose | 1 | 是 |
| `sidebar.favorites` | - | loose | 1 | 是 |
| `sidebar.folders` | - | loose | 1 | 是 |
| `sidebar.library` | - | loose | 1 | 是 |
| `sidebar.map` | - | loose | 1 | 是 |
| `sidebar.mediaTypes` | - | loose | 1 | 是 |
| `sidebar.people` | - | loose | 1 | 是 |
| `sidebar.places` | - | loose | 1 | 是 |
| `sidebar.recentlyAdded` | - | loose | 1 | 是 |
| `sidebar.recycleBin` | - | loose | 1 | 是 |
| `sidebar.shared` | - | loose | 1 | 是 |
| `sidebar.smartCategories` | - | loose | 1 | 是 |
| `sidebar.tags` | - | loose | 1 | 是 |

## statusBar

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `statusBar.network.network` | - | loose | 2 | 是 |
| `statusBar.storage.diskPerformance` | - | loose | 2 | 是 |
| `statusBar.storage.getStorageFailed` | - | loose | 1 |  |
| `statusBar.storage.loading` | - | loose | 1 |  |
| `statusBar.storage.noStorageSpace` | - | loose | 1 |  |
| `statusBar.storage.states.broken` | - | loose | 1 | 是 |
| `statusBar.storage.states.cacheBroken` | - | loose | 1 | 是 |
| `statusBar.storage.states.cacheDegraded` | - | loose | 1 | 是 |
| `statusBar.storage.states.downgrade` | - | loose | 1 | 是 |
| `statusBar.storage.states.inactive` | - | loose | 1 | 是 |
| `statusBar.storage.states.mountpoint` | - | loose | 1 | 是 |
| `statusBar.storage.states.normal` | - | loose | 1 | 是 |
| `statusBar.storage.states.removed` | - | loose | 1 | 是 |
| `statusBar.storage.storageSpace` | - | loose | 1 | 是 |
| `statusBar.storage.storageSpaceWithId` | - | loose | 1 | 是 |
| `statusBar.system.memory` | - | loose | 1 | 是 |
| `statusBar.system.planToShutdown` | `i18nKey` | alias_key,loose | 2 |  |
| `statusBar.system.planToShutdownTitle` | - | loose | 1 | 是 |
| `statusBar.system.systemStatus` | - | loose | 1 | 是 |
| `statusBar.system.thisRuntime` | - | loose | 1 | 是 |
| `statusBar.system.timeUnits.days` | - | loose | 1 | 是 |
| `statusBar.system.timeUnits.hour` | - | loose | 2 | 是 |
| `statusBar.system.timeUnits.hours` | - | loose | 1 | 是 |
| `statusBar.system.timeUnits.minute` | - | loose | 2 | 是 |
| `statusBar.system.timeUnits.minutes` | - | loose | 1 | 是 |
| `statusBar.system.timeUnits.second` | - | loose | 1 | 是 |
| `statusBar.system.timeUnits.seconds` | - | loose | 1 | 是 |
| `statusBar.ups.connectUpsFirst` | - | loose | 1 | 是 |
| `statusBar.ups.currentPowerType` | - | loose | 1 | 是 |
| `statusBar.ups.remainingBattery` | - | loose | 1 | 是 |
| `statusBar.ups.shutdownAfterMinutes` | - | loose | 1 | 是 |
| `statusBar.ups.shutdownWaitingRule` | - | loose | 1 | 是 |
| `statusBar.ups.untilBatteryLow` | - | loose | 1 | 是 |
| `statusBar.widgets.diskPerformance` | - | loose | 1 | 是 |
| `statusBar.widgets.network` | - | loose | 1 | 是 |
| `statusBar.widgets.storageSpace` | - | loose | 1 | 是 |
| `statusBar.widgets.systemStatus` | - | loose | 1 | 是 |
| `statusBar.widgets.ups` | - | loose | 1 | 是 |

## stor

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `stor.format` | `format` | alias_key,loose | 2 |  |
| `stor.state` | `state` | alias_key,loose | 2 |  |

## storage

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `storage.storage` | - | loose | 2 | 是 |

## storageList

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `storageList.altText` | - | loose | 1 | 是 |
| `storageList.noStorage` | - | loose | 2 | 是 |
| `storageList.noStorageTip` | - | loose | 1 | 是 |
| `storageList.storageSpace` | - | loose | 5 | 是 |
| `storageList.storageSpaceManagement` | - | loose | 1 | 是 |
| `storageList.userFiles` | - | loose | 2 | 是 |

## storageManagement

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `storageManagement.common.confirmWordWithExternalDisk` | - | loose | 1 | 是 |
| `storageManagement.common.killProcess.closeNfsService` | - | loose | 1 | 是 |
| `storageManagement.common.killProcess.deleteLun` | - | loose | 1 | 是 |
| `storageManagement.common.killProcess.failedTips.cache` | - | loose | 1 |  |
| `storageManagement.common.killProcess.failedTips.storage` | - | loose | 2 | 是 |
| `storageManagement.common.killProcess.listProcess.externalDisk` | - | loose | 1 |  |
| `storageManagement.common.killProcess.listProcess.lossDataTips` | - | loose | 1 | 是 |
| `storageManagement.common.killProcess.listProcess.process` | - | loose | 1 | 是 |
| `storageManagement.common.killProcess.listProcess.storageSpace` | - | loose | 1 |  |
| `storageManagement.common.killProcess.restartMachine` | - | loose | 1 | 是 |
| `storageManagement.common.killProcess.specialProcessTips.docker` | - | loose | 1 | 是 |
| `storageManagement.common.killProcess.specialProcessTips.smb` | - | loose | 1 | 是 |
| `storageManagement.common.killProcess.ssdAbnormal` | - | loose | 1 | 是 |
| `storageManagement.common.killProcess.unknownProcess` | - | loose | 1 | 是 |
| `storageManagement.common.stepPrefix` | - | loose | 1 | 是 |
| `storageManagement.common.tagContent.checkDisk` | - | loose | 1 | 是 |
| `storageManagement.common.tagContent.degraded` | - | loose | 2 | 是 |
| `storageManagement.common.tagContent.fault` | - | loose | 1 |  |
| `storageManagement.common.tagContent.loss` | - | loose | 2 | 是 |
| `storageManagement.common.tagContent.scrub` | - | loose | 1 | 是 |
| `storageManagement.common.tagLabel.broken` | - | loose | 2 | 是 |
| `storageManagement.common.tagLabel.cacheBrokenConfirmed` | - | loose | 2 | 是 |
| `storageManagement.common.tagLabel.inactive` | - | loose | 2 | 是 |
| `storageManagement.common.tagLabel.normal` | - | loose | 2 | 是 |
| `storageManagement.common.tagLabel.notImported` | - | loose | 3 | 是 |
| `storageManagement.common.tagLabel.removedConfirmed` | - | loose | 3 | 是 |
| `storageManagement.common.tagLabel.unmounted` | - | loose | 1 | 是 |
| `storageManagement.common.vdevState.cantOpen` | - | loose | 1 | 是 |
| `storageManagement.common.vdevState.closed` | - | loose | 1 | 是 |
| `storageManagement.common.vdevState.degraded` | - | loose | 1 | 是 |
| `storageManagement.common.vdevState.faulted` | - | loose | 1 | 是 |
| `storageManagement.common.vdevState.offline` | - | loose | 1 | 是 |
| `storageManagement.common.vdevState.online` | - | loose | 1 | 是 |
| `storageManagement.common.vdevState.removed` | - | loose | 1 | 是 |
| `storageManagement.common.vdevState.unavail` | - | loose | 1 | 是 |
| `storageManagement.common.vdevState.unknown` | - | loose | 1 | 是 |
| `storageManagement.ssdCache.brand` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.brand` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menu.capacityDetails` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menu.changeMode` | - | loose | 2 | 是 |
| `storageManagement.storageSpace.menu.createStorage` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menu.delete` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menu.deleteAndUmount` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menu.detachCacheAndActive` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menu.export` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menu.removeCache` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menu.repairStorage` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menu.replaceDisk` | - | loose | 2 | 是 |
| `storageManagement.storageSpace.menu.resize` | - | loose | 2 | 是 |
| `storageManagement.storageSpace.menu.scrub` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menu.settings` | - | loose | 2 | 是 |
| `storageManagement.storageSpace.menu.spare` | - | loose | 3 | 是 |
| `storageManagement.storageSpace.menu.umount` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menu.umountAndExport` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menuDesc.delete` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menuDesc.export` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menuDesc.umount` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menuDesc.umountAndExport` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menuDisabledReason.broken` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menuDisabledReason.cacheBroken` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menuDisabledReason.cacheDegraded` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menuDisabledReason.containSystemDisk` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menuDisabledReason.degraded` | - | loose | 2 | 是 |
| `storageManagement.storageSpace.menuDisabledReason.inactive` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menuDisabledReason.notOperableSyncAction` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menuDisabledReason.notSupported` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menuDisabledReason.removed` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menuDisabledReason.scrubForbidden` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menuDisabledReason.unmounted` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menuDisabledReason.zfsForbidden` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.menuDisabledReason.zfsStateForbidden` | - | loose | 1 | 是 |
| `storageManagement.storageSpace.performance` | - | loose | 1 |  |
| `storageManagement.storageSpace.storageMode` | - | loose | 1 |  |

## stpp

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `stpp.ttml.im1t` | - | loose | 1 |  |

## style

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `style.display` | - | loose | 1 |  |
| `style.height` | - | loose | 2 |  |
| `style.left` | - | loose | 2 |  |
| `style.right` | - | loose | 2 |  |
| `style.width` | - | loose | 2 |  |

## systemUpdate

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `systemUpdate.aboutToRestart` | - | loose | 1 |  |
| `systemUpdate.cancel` | - | loose | 1 | 是 |
| `systemUpdate.checkUpdateError` | - | loose | 1 | 是 |
| `systemUpdate.checkingUpdate` | - | loose | 1 | 是 |
| `systemUpdate.closeUpdate` | - | loose | 1 | 是 |
| `systemUpdate.confirm` | - | loose | 1 | 是 |
| `systemUpdate.currentVersion` | - | loose | 2 | 是 |
| `systemUpdate.getUpdateStatusError` | - | loose | 1 | 是 |
| `systemUpdate.later` | - | loose | 1 | 是 |
| `systemUpdate.latestVersion` | - | loose | 2 | 是 |
| `systemUpdate.notification.goToUpdate` | - | loose | 2 | 是 |
| `systemUpdate.notification.importantVersionAvailable` | - | loose | 1 | 是 |
| `systemUpdate.notification.newVersionAvailable` | - | loose | 1 | 是 |
| `systemUpdate.notification.securityRebootRequired` | - | loose | 2 | 是 |
| `systemUpdate.notification.securityUpdateAvailable` | - | loose | 1 | 是 |
| `systemUpdate.notification.viewDetails` | - | loose | 3 | 是 |
| `systemUpdate.rebootTips.auto` | - | loose | 1 | 是 |
| `systemUpdate.rebootTips.manual` | - | loose | 1 | 是 |
| `systemUpdate.repairComplete` | - | loose | 1 |  |
| `systemUpdate.repairFailed` | - | loose | 1 |  |
| `systemUpdate.repairProcessMayTakeFewMinutes` | - | loose | 1 | 是 |
| `systemUpdate.repairing` | - | loose | 1 | 是 |
| `systemUpdate.repairingDuplicate` | - | loose | 1 | 是 |
| `systemUpdate.restartNow` | - | loose | 1 | 是 |
| `systemUpdate.restarting` | - | loose | 1 |  |
| `systemUpdate.retryUpdate` | - | loose | 1 | 是 |
| `systemUpdate.size` | - | loose | 1 | 是 |
| `systemUpdate.systemFileRepair` | - | loose | 1 | 是 |
| `systemUpdate.systemFileRepairInProgress.content` | - | loose | 1 | 是 |
| `systemUpdate.systemFileRepairInProgress.ignore` | - | loose | 1 | 是 |
| `systemUpdate.systemFileRepairInProgress.view` | - | loose | 1 | 是 |
| `systemUpdate.title` | - | loose | 1 | 是 |
| `systemUpdate.updateFailed` | - | loose | 2 | 是 |
| `systemUpdate.updateFailedWithError` | - | loose | 1 | 是 |
| `systemUpdate.updateNow` | - | loose | 1 | 是 |
| `systemUpdate.updateProgress.step` | - | loose | 1 | 是 |
| `systemUpdate.updateProgress.update` | - | loose | 2 | 是 |
| `systemUpdate.updateSteps.almostDone` | - | loose | 1 | 是 |
| `systemUpdate.updateSteps.completed` | - | loose | 1 | 是 |
| `systemUpdate.updateSteps.downloading` | - | loose | 1 | 是 |
| `systemUpdate.updateSteps.preparing` | - | loose | 1 | 是 |
| `systemUpdate.updateSteps.success` | - | loose | 1 | 是 |
| `systemUpdate.updateSteps.updating` | - | loose | 1 | 是 |
| `systemUpdate.updateSteps.verifying` | - | loose | 1 | 是 |
| `systemUpdate.updateSteps.waiting` | - | loose | 1 | 是 |
| `systemUpdate.updateSuccess` | - | loose | 1 |  |
| `systemUpdate.updateSystem` | - | loose | 1 | 是 |
| `systemUpdate.updateSystemConfirm` | - | loose | 1 | 是 |
| `systemUpdate.updating` | - | loose | 1 | 是 |
| `systemUpdate.version` | - | loose | 1 | 是 |

## table

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `table.event` | - | loose | 1 | 是 |
| `table.level` | - | loose | 2 | 是 |
| `table.module` | - | loose | 2 | 是 |
| `table.time` | - | loose | 1 | 是 |
| `table.user` | - | loose | 1 | 是 |

## tabs

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `tabs.account` | - | loose | 1 | 是 |
| `tabs.allApp` | - | loose | 1 | 是 |
| `tabs.allFiles` | - | loose | 1 | 是 |
| `tabs.appAccess` | - | loose | 1 | 是 |
| `tabs.appSearch` | - | loose | 1 | 是 |
| `tabs.appShareFiles` | - | loose | 1 | 是 |
| `tabs.authorizedDevices` | - | loose | 1 | 是 |
| `tabs.classification` | - | loose | 1 | 是 |
| `tabs.equipmentManagement` | - | loose | 1 | 是 |
| `tabs.externalAuth` | - | loose | 1 | 是 |
| `tabs.externalStorage` | - | loose | 2 | 是 |
| `tabs.favorite` | - | loose | 1 | 是 |
| `tabs.fileSharingProtocol` | - | loose | 1 | 是 |
| `tabs.installed` | - | loose | 2 | 是 |
| `tabs.languageAndTime` | - | loose | 2 | 是 |
| `tabs.latestRelease` | - | loose | 2 | 是 |
| `tabs.linkShare` | - | loose | 1 | 是 |
| `tabs.linkShareManage` | - | loose | 1 | 是 |
| `tabs.manualInstall` | - | loose | 1 | 是 |
| `tabs.myFiles` | - | loose | 2 | 是 |
| `tabs.myShare` | - | loose | 1 | 是 |
| `tabs.namesake` | - | loose | 1 | 是 |
| `tabs.otherShare` | - | loose | 1 | 是 |
| `tabs.personalTrashManage` | - | loose | 2 | 是 |
| `tabs.preference` | - | loose | 1 | 是 |
| `tabs.recentRecord` | - | loose | 1 | 是 |
| `tabs.recycleBin` | - | loose | 1 | 是 |
| `tabs.recycleBinManage` | - | loose | 1 | 是 |
| `tabs.remoteConnection` | - | loose | 1 | 是 |
| `tabs.remoteMount` | - | loose | 1 | 是 |
| `tabs.settings` | - | loose | 2 | 是 |
| `tabs.shareFiles` | - | loose | 1 | 是 |
| `tabs.shareLink` | - | loose | 1 | 是 |
| `tabs.teamSpace` | - | loose | 2 | 是 |
| `tabs.teamTrashManage` | - | loose | 2 | 是 |

## tagStatusLabel

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `tagStatusLabel.disabled` | - | loose | 2 | 是 |
| `tagStatusLabel.error` | - | loose | 1 | 是 |
| `tagStatusLabel.errorLabel.reason` | - | loose | 1 | 是 |
| `tagStatusLabel.errorLabel.title` | - | loose | 1 | 是 |
| `tagStatusLabel.matchedFilesLabel.title` | - | loose | 1 | 是 |
| `tagStatusLabel.notStarted` | - | loose | 2 | 是 |
| `tagStatusLabel.partialFailure` | - | loose | 1 | 是 |
| `tagStatusLabel.partialFailureLabel.decryptInfo` | - | loose | 1 | 是 |
| `tagStatusLabel.partialFailureLabel.failInfo` | - | loose | 1 | 是 |
| `tagStatusLabel.partialFailureLabel.title` | - | loose | 1 | 是 |
| `tagStatusLabel.running` | - | loose | 1 | 是 |
| `tagStatusLabel.runningPhaseLabel.actualFiles` | - | loose | 1 | 是 |
| `tagStatusLabel.runningPhaseLabel.backingUp` | - | loose | 1 | 是 |
| `tagStatusLabel.runningPhaseLabel.connecting` | - | loose | 1 | 是 |
| `tagStatusLabel.runningPhaseLabel.copying` | - | loose | 1 | 是 |
| `tagStatusLabel.runningPhaseLabel.scanning` | - | loose | 1 | 是 |
| `tagStatusLabel.runningPhaseLabel.totalFiles` | - | loose | 1 | 是 |
| `tagStatusLabel.stopped` | - | loose | 1 | 是 |
| `tagStatusLabel.stoppedLabel.actualFiles` | - | loose | 1 | 是 |
| `tagStatusLabel.stoppedLabel.title` | - | loose | 1 | 是 |
| `tagStatusLabel.successful` | - | loose | 1 | 是 |
| `tagStatusLabel.successfulLabel.actualFiles` | - | loose | 1 | 是 |
| `tagStatusLabel.successfulLabel.title` | - | loose | 1 | 是 |

## tar

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `tar.bz2` | - | loose | 2 |  |
| `tar.gz` | - | loose | 2 |  |

## target

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `target.dataset.scrollkey` | - | loose | 2 |  |

## task

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `task.upload.done` | - | loose | 1 |  |
| `task.upload.update` | - | loose | 1 |  |

## taskActionTips

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `taskActionTips.failMsg` | - | loose | 1 | 是 |

## taskCard

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `taskCard.controlButton.connecting` | - | loose | 1 |  |
| `taskCard.controlButton.disabled` | - | loose | 1 |  |
| `taskCard.controlButton.run` | - | loose | 1 |  |
| `taskCard.controlButton.running` | - | loose | 1 |  |
| `taskCard.controlButton.stop` | - | loose | 1 |  |
| `taskCard.controlButton.stopping` | - | loose | 1 |  |
| `taskCard.header.createBackupTask` | - | loose | 1 | 是 |
| `taskCard.header.localData` | - | loose | 2 |  |
| `taskCard.header.remoteData` | - | loose | 2 |  |
| `taskCard.header.title` | - | loose | 1 | 是 |
| `taskCard.header.updatedCreateBackupTask` | - | loose | 1 | 是 |
| `taskCard.timeInfo.next` | - | loose | 1 |  |
| `taskCard.timeInfo.plan` | - | loose | 1 | 是 |
| `taskCard.timeInfo.prev` | - | loose | 1 |  |

## taskCreatorDialog

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `taskCreatorDialog.assistHook.deviceAssist.title` | - | loose | 1 | 是 |
| `taskCreatorDialog.assistHook.ignoreExtensionsAssist.extLabel.disabled` | - | loose | 1 | 是 |
| `taskCreatorDialog.assistHook.ignoreExtensionsAssist.extLabel.empty` | - | loose | 1 | 是 |
| `taskCreatorDialog.assistHook.ignoreExtensionsAssist.title` | - | loose | 1 | 是 |
| `taskCreatorDialog.assistHook.planAssist.title` | - | loose | 1 | 是 |
| `taskCreatorDialog.assistHook.sourceAssist.notSelected` | - | loose | 1 | 是 |
| `taskCreatorDialog.assistHook.sourceAssist.title` | - | loose | 1 | 是 |
| `taskCreatorDialog.assistHook.targetAssist.title` | - | loose | 1 | 是 |
| `taskCreatorDialog.connectFileProtocol` | - | loose | 1 | 是 |
| `taskCreatorDialog.connectNas` | - | loose | 1 | 是 |
| `taskCreatorDialog.deviceSelector.connectedDeviceCard.title.selected` | - | loose | 1 |  |
| `taskCreatorDialog.deviceSelector.connectedDeviceCard.title.unselected` | - | loose | 1 |  |
| `taskCreatorDialog.deviceSelector.title.localData` | - | loose | 1 |  |
| `taskCreatorDialog.deviceSelector.title.remoteData` | - | loose | 1 |  |
| `taskCreatorDialog.pickSource` | - | loose | 1 | 是 |
| `taskCreatorDialog.pickTarget` | - | loose | 1 | 是 |
| `taskCreatorDialog.sourceManager.listTitle` | - | loose | 1 | 是 |
| `taskCreatorDialog.sourceManager.sourceTotalSize` | - | loose | 1 | 是 |
| `taskCreatorDialog.sourceManager.stepTitle.localData` | - | loose | 1 |  |
| `taskCreatorDialog.sourceManager.stepTitle.remoteData` | - | loose | 1 |  |
| `taskCreatorDialog.step4.nextStepDisabledTitle` | - | loose | 1 | 是 |
| `taskCreatorDialog.step4.title` | - | loose | 1 | 是 |
| `taskCreatorDialog.step5.title` | - | loose | 1 | 是 |
| `taskCreatorDialog.step6.confirmBtnTitle` | - | loose | 1 | 是 |
| `taskCreatorDialog.step6.createFailedMsg` | - | loose | 1 | 是 |
| `taskCreatorDialog.step6.createSuccessMsg` | - | loose | 1 | 是 |
| `taskCreatorDialog.step6.creatingTips` | - | loose | 1 | 是 |
| `taskCreatorDialog.step6.encryptionPreviewTitle` | - | loose | 1 | 是 |
| `taskCreatorDialog.step6.inputPlaceholder` | - | loose | 1 | 是 |
| `taskCreatorDialog.step6.planPreviewTitle` | - | loose | 1 | 是 |
| `taskCreatorDialog.step6.settingsPreviewTitle` | - | loose | 1 | 是 |
| `taskCreatorDialog.step6.stepTitle` | - | loose | 1 | 是 |
| `taskCreatorDialog.step6.taskNameExists` | - | loose | 1 | 是 |
| `taskCreatorDialog.step6.title` | - | loose | 1 | 是 |
| `taskCreatorDialog.targetCard.additional.addIconLabel` | - | loose | 1 | 是 |
| `taskCreatorDialog.targetCard.additional.clickToAdd` | - | loose | 1 | 是 |
| `taskCreatorDialog.targetCard.additional.destination.localData` | - | loose | 2 |  |
| `taskCreatorDialog.targetCard.additional.destination.remoteData` | - | loose | 2 |  |
| `taskCreatorDialog.targetCard.additional.selectDestination` | - | loose | 1 | 是 |
| `taskCreatorDialog.targetCard.normal.title.default` | - | loose | 2 | 是 |
| `taskCreatorDialog.targetCard.normal.title.selected` | - | loose | 1 |  |
| `taskCreatorDialog.targetCard.normal.title.unselected` | - | loose | 1 |  |
| `taskCreatorDialog.targetGroupConfig.fileProtocol` | - | loose | 1 | 是 |
| `taskCreatorDialog.targetGroupConfig.thirdParty` | - | loose | 1 | 是 |
| `taskCreatorDialog.targetManager.listTitle` | - | loose | 1 | 是 |
| `taskCreatorDialog.targetManager.pathTitle` | - | loose | 1 | 是 |
| `taskCreatorDialog.targetManager.stepTitle` | - | loose | 1 | 是 |
| `taskCreatorDialog.taskRuleForm.advancedSettings` | - | loose | 1 | 是 |
| `taskCreatorDialog.taskSettingsPreview.moreSourceTitle` | - | loose | 1 | 是 |
| `taskCreatorDialog.taskSettingsPreview.showAll` | - | loose | 1 | 是 |
| `taskCreatorDialog.taskSettingsPreview.sourceTotalCount` | - | loose | 1 | 是 |
| `taskCreatorDialog.validatorHook.errorTips.allEmpty` | - | loose | 1 | 是 |
| `taskCreatorDialog.validatorHook.errorTips.maxEmpty` | - | loose | 1 | 是 |
| `taskCreatorDialog.validatorHook.errorTips.maxEmptyAndMinTooSmall` | - | loose | 1 | 是 |
| `taskCreatorDialog.validatorHook.errorTips.maxExceedWithLimitTips` | - | loose | 2 | 是 |
| `taskCreatorDialog.validatorHook.errorTips.minAndMaxExceedWithLimitTips` | - | loose | 1 | 是 |
| `taskCreatorDialog.validatorHook.errorTips.minBiggerThanMax` | - | loose | 1 | 是 |
| `taskCreatorDialog.validatorHook.errorTips.minEmpty` | - | loose | 1 | 是 |
| `taskCreatorDialog.validatorHook.errorTips.minEmptyAndMaxTooSmall` | - | loose | 1 | 是 |
| `taskCreatorDialog.validatorHook.errorTips.minExceedWithLimitTips` | - | loose | 2 | 是 |
| `taskCreatorDialog.validatorHook.limitTips.exceed` | - | loose | 1 | 是 |
| `taskCreatorDialog.validatorHook.limitTips.exceedEmpty` | - | loose | 1 | 是 |
| `taskCreatorDialog.validatorHook.limitTips.exceedUnits` | - | loose | 1 | 是 |
| `taskCreatorDialog.validatorHook.limitTips.inputRange` | - | loose | 1 | 是 |

## taskEditorDialog

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `taskEditorDialog.confirmTips` | - | loose | 1 | 是 |
| `taskEditorDialog.contentTabItems.location` | - | loose | 1 | 是 |
| `taskEditorDialog.contentTabItems.plan` | - | loose | 1 | 是 |
| `taskEditorDialog.contentTabItems.rule` | - | loose | 1 | 是 |
| `taskEditorDialog.editFailedMsg` | - | loose | 1 | 是 |
| `taskEditorDialog.editSuccessMsg` | - | loose | 1 | 是 |
| `taskEditorDialog.errorTips.selectCacheStor` | - | loose | 1 | 是 |
| `taskEditorDialog.errorTips.selectCacheStorUnavailable` | - | loose | 1 | 是 |
| `taskEditorDialog.title` | - | loose | 1 | 是 |

## taskPanel

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `taskPanel.addToAlbum` | - | loose | 1 | 是 |
| `taskPanel.aiTaskStates.canceling` | - | loose | 1 | 是 |
| `taskPanel.aiTaskStates.clustering` | - | loose | 1 | 是 |
| `taskPanel.aiTaskStates.converting` | - | loose | 1 | 是 |
| `taskPanel.aiTaskStates.detecting` | - | loose | 2 | 是 |
| `taskPanel.aiTaskStates.preparing` | - | loose | 1 | 是 |
| `taskPanel.aiTaskStates.scanning` | - | loose | 1 | 是 |
| `taskPanel.aiTaskStates.updating` | - | loose | 1 | 是 |
| `taskPanel.cancel` | - | loose | 3 | 是 |
| `taskPanel.cancelTaskFailed` | - | loose | 1 | 是 |
| `taskPanel.canceled` | - | loose | 1 | 是 |
| `taskPanel.canceledTask` | - | loose | 3 | 是 |
| `taskPanel.check` | - | loose | 1 | 是 |
| `taskPanel.checkRepeat` | - | loose | 1 |  |
| `taskPanel.checkSimilar` | - | loose | 1 |  |
| `taskPanel.checking` | - | loose | 1 | 是 |
| `taskPanel.cleaning` | - | loose | 1 | 是 |
| `taskPanel.cleanupRecycleBin` | - | loose | 1 |  |
| `taskPanel.clearTaskList` | - | loose | 1 | 是 |
| `taskPanel.completedTask` | - | loose | 3 | 是 |
| `taskPanel.delete` | - | loose | 1 | 是 |
| `taskPanel.deleteFiles` | - | loose | 1 |  |
| `taskPanel.deleteRecord` | - | loose | 6 | 是 |
| `taskPanel.deleteRecordFailed` | - | loose | 1 | 是 |
| `taskPanel.deleting` | - | loose | 1 | 是 |
| `taskPanel.empty` | - | loose | 2 | 是 |
| `taskPanel.estimatedTime` | - | loose | 1 | 是 |
| `taskPanel.failedTask` | - | loose | 3 | 是 |
| `taskPanel.failureDetails` | - | loose | 2 | 是 |
| `taskPanel.fileNotExists` | - | loose | 1 | 是 |
| `taskPanel.finished` | - | loose | 3 | 是 |
| `taskPanel.folderNotExists` | - | loose | 1 | 是 |
| `taskPanel.folderScanning` | - | loose | 8 | 是 |
| `taskPanel.generating` | - | loose | 2 | 是 |
| `taskPanel.identifying` | - | loose | 1 | 是 |
| `taskPanel.ignore` | - | loose | 1 | 是 |
| `taskPanel.ignoreFailed` | - | loose | 1 | 是 |
| `taskPanel.ignoredSuccess` | - | loose | 1 | 是 |
| `taskPanel.inProgressWithCount` | - | loose | 2 | 是 |
| `taskPanel.itemsCanceled` | - | loose | 3 | 是 |
| `taskPanel.itemsCompleted` | - | loose | 2 | 是 |
| `taskPanel.itemsFailed` | - | loose | 1 | 是 |
| `taskPanel.itemsReadOriginalFileFailed` | - | loose | 2 | 是 |
| `taskPanel.noContent` | - | loose | 1 | 是 |
| `taskPanel.noUnrecognizedPhotos` | - | loose | 1 | 是 |
| `taskPanel.openFolder` | - | loose | 1 | 是 |
| `taskPanel.parsing` | - | loose | 1 | 是 |
| `taskPanel.parsingInProgress` | - | loose | 1 | 是 |
| `taskPanel.rebuilding` | - | loose | 1 | 是 |
| `taskPanel.recognize` | - | loose | 1 | 是 |
| `taskPanel.retry` | - | loose | 2 | 是 |
| `taskPanel.retryFailed` | - | loose | 2 | 是 |
| `taskPanel.scan` | - | loose | 1 | 是 |
| `taskPanel.stateWithCount` | - | loose | 1 | 是 |
| `taskPanel.taskFailed` | - | loose | 1 | 是 |
| `taskPanel.taskNotFound` | - | loose | 1 | 是 |
| `taskPanel.taskTypes.cleanThumb` | - | loose | 2 | 是 |
| `taskPanel.taskTypes.copy` | - | loose | 1 | 是 |
| `taskPanel.taskTypes.faceRec` | - | loose | 1 | 是 |
| `taskPanel.taskTypes.fixData` | - | loose | 1 | 是 |
| `taskPanel.taskTypes.folderScan` | - | loose | 1 | 是 |
| `taskPanel.taskTypes.googleTakeoutImport` | - | loose | 1 | 是 |
| `taskPanel.taskTypes.move` | - | loose | 1 | 是 |
| `taskPanel.taskTypes.recategorizeSmartCategory` | - | loose | 2 | 是 |
| `taskPanel.taskTypes.recheckExif` | - | loose | 2 | 是 |
| `taskPanel.taskTypes.recycleBin` | - | loose | 1 | 是 |
| `taskPanel.taskTypes.regenerateThumb` | - | loose | 2 | 是 |
| `taskPanel.taskTypes.reloadIndex` | - | loose | 2 | 是 |
| `taskPanel.taskTypes.repeatPhoto` | - | loose | 2 | 是 |
| `taskPanel.taskTypes.rotate` | - | loose | 1 | 是 |
| `taskPanel.taskTypes.smartRec` | - | loose | 1 | 是 |
| `taskPanel.taskTypes.smartRecVideo` | - | loose | 1 | 是 |
| `taskPanel.taskTypes.thumbnail` | - | loose | 2 | 是 |
| `taskPanel.taskTypes.updateSmartCategory` | - | loose | 2 | 是 |
| `taskPanel.taskTypes.upload` | - | loose | 1 | 是 |
| `taskPanel.title` | - | loose | 1 | 是 |
| `taskPanel.units.days` | - | loose | 1 | 是 |
| `taskPanel.units.hours` | - | loose | 1 | 是 |
| `taskPanel.units.minutes` | - | loose | 1 | 是 |
| `taskPanel.units.seconds` | - | loose | 1 | 是 |
| `taskPanel.upgrade` | - | loose | 1 | 是 |
| `taskPanel.upgrading` | - | loose | 1 | 是 |

## taskbar

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `taskbar.about.contactUs` | - | loose | 1 | 是 |
| `taskbar.about.copyright` | - | loose | 1 | 是 |
| `taskbar.about.currentVersion` | - | loose | 2 | 是 |
| `taskbar.about.howToBuy` | - | loose | 1 | 是 |
| `taskbar.about.remoteAssistance` | - | loose | 1 | 是 |
| `taskbar.aboutOS` | - | loose | 2 | 是 |
| `taskbar.admin` | - | loose | 1 | 是 |
| `taskbar.allApps` | - | loose | 1 | 是 |
| `taskbar.cancel` | - | loose | 2 | 是 |
| `taskbar.clearAll` | - | loose | 1 | 是 |
| `taskbar.clearAllConfirm` | - | loose | 1 | 是 |
| `taskbar.desktop` | - | loose | 1 | 是 |
| `taskbar.fileTaskInfo.title` | - | loose | 1 | 是 |
| `taskbar.fileTasks` | - | loose | 2 | 是 |
| `taskbar.helpCenter` | - | loose | 1 | 是 |
| `taskbar.loadingTaskList` | - | loose | 1 | 是 |
| `taskbar.logout` | - | loose | 2 | 是 |
| `taskbar.logoutConfirm` | - | loose | 1 | 是 |
| `taskbar.myAccount` | - | loose | 1 | 是 |
| `taskbar.noFileTasks` | - | loose | 1 | 是 |
| `taskbar.notice.detail` | - | loose | 2 | 是 |
| `taskbar.notice.group.system` | - | loose | 4 | 是 |
| `taskbar.notice.group.title` | - | loose | 1 | 是 |
| `taskbar.notice.loadFailed` | - | loose | 1 | 是 |
| `taskbar.notice.loading` | - | loose | 1 | 是 |
| `taskbar.notice.noNotifications` | - | loose | 1 | 是 |
| `taskbar.notice.retry` | - | loose | 1 | 是 |
| `taskbar.notifications` | - | loose | 1 | 是 |
| `taskbar.openFolder` | - | loose | 2 | 是 |
| `taskbar.pause` | - | loose | 2 | 是 |
| `taskbar.personalSettings` | - | loose | 1 | 是 |
| `taskbar.power.confirmRestartContent` | - | loose | 1 | 是 |
| `taskbar.power.confirmRestartOk` | - | loose | 1 | 是 |
| `taskbar.power.confirmRestartTitle` | - | loose | 1 | 是 |
| `taskbar.power.confirmShutdownContent` | - | loose | 1 | 是 |
| `taskbar.power.confirmShutdownOk` | - | loose | 1 | 是 |
| `taskbar.power.confirmShutdownTitle` | - | loose | 1 | 是 |
| `taskbar.power.dontClose` | - | loose | 1 | 是 |
| `taskbar.power.restartFail` | - | loose | 1 | 是 |
| `taskbar.power.restarting` | - | loose | 1 | 是 |
| `taskbar.power.shutdownDoneContent` | - | loose | 1 | 是 |
| `taskbar.power.shutdownDoneTitle` | - | loose | 1 | 是 |
| `taskbar.power.shutdownFail` | - | loose | 1 | 是 |
| `taskbar.power.shuttingDown` | - | loose | 1 | 是 |
| `taskbar.restart` | - | loose | 1 | 是 |
| `taskbar.settings` | - | loose | 1 | 是 |
| `taskbar.shutdown` | - | loose | 1 | 是 |
| `taskbar.start` | - | loose | 2 | 是 |
| `taskbar.systemNotifications` | - | loose | 1 | 是 |
| `taskbar.systemSettings` | - | loose | 1 | 是 |
| `taskbar.taskCompleted` | - | loose | 1 | 是 |
| `taskbar.taskRemaining` | - | loose | 1 | 是 |
| `taskbar.taskState.aboutToComplete` | - | loose | 2 | 是 |
| `taskbar.taskState.andMore` | - | loose | 1 | 是 |
| `taskbar.taskState.andMoreItems` | - | loose | 1 | 是 |
| `taskbar.taskState.calculatingSize` | - | loose | 2 | 是 |
| `taskbar.taskState.calculatingSizeWithCount` | - | loose | 1 | 是 |
| `taskbar.taskState.calculatingSizeWithSize` | - | loose | 1 | 是 |
| `taskbar.taskState.cancelled` | - | loose | 2 | 是 |
| `taskbar.taskState.completed` | - | loose | 3 | 是 |
| `taskbar.taskState.completedTo.compress` | - | loose | 1 | 是 |
| `taskbar.taskState.completedTo.copy` | - | loose | 1 | 是 |
| `taskbar.taskState.completedTo.extract` | - | loose | 1 | 是 |
| `taskbar.taskState.completedTo.move` | - | loose | 1 | 是 |
| `taskbar.taskState.completedTo.upload` | - | loose | 1 | 是 |
| `taskbar.taskState.failed` | - | loose | 1 | 是 |
| `taskbar.taskState.failedItems` | - | loose | 2 | 是 |
| `taskbar.taskState.partialCompletedTo.compress` | - | loose | 1 | 是 |
| `taskbar.taskState.partialCompletedTo.copy` | - | loose | 1 | 是 |
| `taskbar.taskState.partialCompletedTo.extract` | - | loose | 1 | 是 |
| `taskbar.taskState.partialCompletedTo.move` | - | loose | 1 | 是 |
| `taskbar.taskState.partialCompletedTo.upload` | - | loose | 1 | 是 |
| `taskbar.taskState.remainingTime` | - | loose | 2 | 是 |
| `taskbar.taskState.remoteMount` | - | loose | 1 | 是 |
| `taskbar.taskState.remoteMountStage1Completed` | - | loose | 1 | 是 |
| `taskbar.taskState.remoteMountUploadTo` | - | loose | 2 | 是 |
| `taskbar.taskState.savedTo` | - | loose | 1 | 是 |
| `taskbar.taskState.taskCancelledFailed` | - | loose | 1 | 是 |
| `taskbar.taskState.taskCancelledSuccess` | - | loose | 1 | 是 |
| `taskbar.taskState.uploadFailed` | - | loose | 1 | 是 |
| `taskbar.taskState.uploadToRemoteMount` | - | loose | 1 | 是 |
| `taskbar.taskState.uploadToRemoteMountColon` | - | loose | 1 | 是 |
| `taskbar.taskState.userCancelled` | - | loose | 1 | 是 |
| `taskbar.taskState.view` | - | loose | 2 | 是 |
| `taskbar.taskState.waiting` | - | loose | 1 | 是 |
| `taskbar.waiting` | - | loose | 2 | 是 |

## team

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `team.field.name` | - | loose | 1 | 是 |
| `team.noSearchResult` | - | loose | 1 |  |
| `team.noTeam` | - | loose | 1 |  |
| `team.searchPlaceholder` | - | loose | 1 | 是 |
| `team.searchTeamPlaceholder` | - | loose | 1 | 是 |
| `team.settings.buttons.cancel` | - | loose | 1 | 是 |
| `team.settings.buttons.confirm` | - | loose | 1 |  |
| `team.settings.buttons.create` | - | loose | 1 |  |
| `team.settings.buttons.next` | - | loose | 1 |  |
| `team.settings.buttons.previous` | - | loose | 1 | 是 |
| `team.settings.buttons.resetSubPermission` | - | loose | 1 | 是 |
| `team.settings.form.allMembers` | - | loose | 1 | 是 |
| `team.settings.form.fileShareProtocol` | - | loose | 1 | 是 |
| `team.settings.form.fileShareProtocolTooltip` | - | loose | 1 | 是 |
| `team.settings.form.limitQuota` | - | loose | 1 | 是 |
| `team.settings.form.name` | - | loose | 1 | 是 |
| `team.settings.form.namePlaceholder` | - | loose | 1 | 是 |
| `team.settings.form.nameRequired` | - | loose | 1 | 是 |
| `team.settings.form.onlyAdmin` | - | loose | 1 | 是 |
| `team.settings.form.quotaDisabledPlaceholder` | - | loose | 1 |  |
| `team.settings.form.quotaPlaceholder` | - | loose | 1 |  |
| `team.settings.form.storageLocation` | - | loose | 1 | 是 |
| `team.settings.form.storageLocationPlaceholder` | - | loose | 2 | 是 |
| `team.settings.form.trashbinAccess` | - | loose | 1 | 是 |
| `team.settings.form.trashbinAccessTooltip` | - | loose | 1 | 是 |
| `team.settings.form.used` | - | loose | 1 | 是 |
| `team.settings.form.viewTrashbin` | - | loose | 1 | 是 |
| `team.settings.messages.createSuccess` | - | loose | 1 | 是 |
| `team.settings.messages.enterInteger` | - | loose | 1 | 是 |
| `team.settings.messages.enterQuota` | - | loose | 1 | 是 |
| `team.settings.messages.nameAlreadyUsed` | - | loose | 1 | 是 |
| `team.settings.messages.quotaExceedsMax` | - | loose | 2 | 是 |
| `team.settings.messages.setFailed` | - | loose | 1 | 是 |
| `team.settings.messages.setPermissionFailed` | - | loose | 1 | 是 |
| `team.settings.messages.setSuccess` | - | loose | 1 | 是 |
| `team.settings.modal.createTitle` | - | loose | 1 | 是 |
| `team.settings.modal.editTitle` | - | loose | 1 | 是 |
| `team.settings.modal.permissionSuffix` | - | loose | 1 | 是 |
| `team.settings.permissions.advanced` | - | loose | 1 | 是 |
| `team.settings.permissions.app` | - | loose | 2 | 是 |
| `team.settings.permissions.everyoneDescription` | - | loose | 1 | 是 |
| `team.settings.permissions.object` | - | loose | 1 | 是 |
| `team.settings.permissions.ownerDescription` | - | loose | 1 | 是 |
| `team.settings.permissions.search` | - | loose | 1 | 是 |
| `team.settings.permissions.user` | - | loose | 2 | 是 |
| `team.settings.permissions.userGroup` | - | loose | 2 | 是 |

## tempFileSettings

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `tempFileSettings.label` | - | loose | 1 | 是 |
| `tempFileSettings.noAvailableStorage` | - | loose | 1 | 是 |
| `tempFileSettings.tooltip` | - | loose | 1 | 是 |

## tfaDisable

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `tfaDisable.description` | - | loose | 1 | 是 |
| `tfaDisable.failureMessage` | - | loose | 1 | 是 |
| `tfaDisable.title` | - | loose | 1 | 是 |

## tfaErrors

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `tfaErrors.badRequest` | - | loose | 1 | 是 |
| `tfaErrors.databaseError` | - | loose | 1 | 是 |
| `tfaErrors.deviceNotFound` | - | loose | 1 | 是 |
| `tfaErrors.duplicate2faBinding` | - | loose | 1 | 是 |
| `tfaErrors.emailModifiedResend` | - | loose | 1 | 是 |
| `tfaErrors.emailNotificationNotEnabled` | - | loose | 1 | 是 |
| `tfaErrors.emailSendFailed` | - | loose | 1 | 是 |
| `tfaErrors.emailVerificationCodeError` | - | loose | 1 | 是 |
| `tfaErrors.forbidden` | - | loose | 1 | 是 |
| `tfaErrors.generate2faKeyFailed` | - | loose | 1 | 是 |
| `tfaErrors.incorrectPassword` | - | loose | 1 | 是 |
| `tfaErrors.internalServerError` | - | loose | 1 | 是 |
| `tfaErrors.login2faCredentialExpired` | - | loose | 1 | 是 |
| `tfaErrors.networkError` | - | loose | 1 | 是 |
| `tfaErrors.notImplemented` | - | loose | 1 | 是 |
| `tfaErrors.operationFailed` | - | loose | 1 | 是 |
| `tfaErrors.parseFailed` | - | loose | 1 | 是 |
| `tfaErrors.requestTimeout` | - | loose | 1 | 是 |
| `tfaErrors.resetPasswordInvalidCredential` | - | loose | 1 | 是 |
| `tfaErrors.resourceConflict` | - | loose | 1 | 是 |
| `tfaErrors.resourceNotFound` | - | loose | 1 | 是 |
| `tfaErrors.secureEmailNotBound` | - | loose | 1 | 是 |
| `tfaErrors.sendEmailCodeTooFrequent` | - | loose | 1 | 是 |
| `tfaErrors.sendEmailFailed` | - | loose | 1 | 是 |
| `tfaErrors.serviceUnavailable` | - | loose | 1 | 是 |
| `tfaErrors.tooManyRequests` | - | loose | 1 | 是 |
| `tfaErrors.twoFaNotBound` | - | loose | 1 | 是 |
| `tfaErrors.twoFaStatusAbnormal` | - | loose | 1 | 是 |
| `tfaErrors.unauthorized` | - | loose | 1 | 是 |
| `tfaErrors.unknownError` | - | loose | 1 | 是 |
| `tfaErrors.validationFailed` | - | loose | 1 | 是 |
| `tfaErrors.verificationCodeError` | - | loose | 1 | 是 |
| `tfaErrors.verificationCodeExpired` | - | loose | 1 | 是 |
| `tfaErrors.verifyTotpAbnormal` | - | loose | 1 | 是 |

## tfaVerify

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `tfaVerify.step2.copiedToClipboard` | - | loose | 1 | 是 |

## theme

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `theme.dark` | - | loose | 1 | 是 |
| `theme.light` | - | loose | 1 | 是 |
| `theme.system` | - | loose | 1 | 是 |

## toolbar

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `toolbar.addTo` | - | loose | 2 | 是 |
| `toolbar.alreadyAddedRefreshThumbnailTask` | - | loose | 1 | 是 |
| `toolbar.ascending` | - | loose | 1 | 是 |
| `toolbar.compressedJPEG` | - | loose | 4 | 是 |
| `toolbar.copyTo` | - | loose | 2 | 是 |
| `toolbar.createAlbum` | - | loose | 1 | 是 |
| `toolbar.delete` | - | loose | 2 | 是 |
| `toolbar.descending` | - | loose | 1 | 是 |
| `toolbar.download` | - | loose | 2 | 是 |
| `toolbar.editLocation` | - | loose | 1 | 是 |
| `toolbar.editShootingTime` | - | loose | 2 | 是 |
| `toolbar.editTags` | - | loose | 2 | 是 |
| `toolbar.favorite` | - | loose | 2 |  |
| `toolbar.more` | - | loose | 3 | 是 |
| `toolbar.moveTo` | - | loose | 2 | 是 |
| `toolbar.original` | - | loose | 4 | 是 |
| `toolbar.refreshThumbnail` | - | loose | 4 | 是 |
| `toolbar.rename` | - | loose | 2 | 是 |
| `toolbar.rotateCounterclockwise` | - | loose | 2 | 是 |
| `toolbar.selectedCount` | - | loose | 3 | 是 |
| `toolbar.share` | - | loose | 2 | 是 |
| `toolbar.shareExternalLink` | - | loose | 3 | 是 |
| `toolbar.shareToDevice` | - | loose | 3 | 是 |
| `toolbar.sortBy` | - | loose | 1 | 是 |
| `toolbar.uploadFolder` | - | loose | 2 | 是 |

## totp

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `totp.account` | - | loose | 1 | 是 |
| `totp.manualAddTitle` | - | loose | 1 | 是 |
| `totp.secretKey` | - | loose | 1 | 是 |
| `totp.setupSecureEmailDescription` | - | loose | 1 | 是 |
| `totp.setupSecureEmailTitle` | - | loose | 1 | 是 |
| `totp.skipSecureEmailTitle` | - | loose | 1 | 是 |
| `totp.skipSecureEmailWarning` | - | loose | 1 | 是 |
| `totp.step1Description` | - | loose | 1 | 是 |
| `totp.step1Subtitle` | - | loose | 1 | 是 |
| `totp.step1Title` | - | loose | 1 | 是 |
| `totp.step2Title` | - | loose | 1 | 是 |
| `totp.token` | - | loose | 1 | 是 |

## tour

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `tour.aiSearchDesc` | - | loose | 1 | 是 |
| `tour.aiSearchTitle` | - | loose | 1 | 是 |
| `tour.gotIt` | - | loose | 2 | 是 |
| `tour.searchFilterDesc` | - | loose | 1 | 是 |
| `tour.searchFilterTitle` | - | loose | 1 | 是 |

## trash

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `trash.teamTrash` | - | loose | 1 | 是 |
| `trash.userTrash` | - | loose | 4 | 是 |

## trim

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `trim.appcenter.all` | - | loose | 1 |  |
| `trim.baidu_netdisk.all` | - | loose | 1 |  |
| `trim.basic` | - | loose | 1 |  |
| `trim.com.trim.updatemgr` | - | loose | 1 |  |
| `trim.docker.all` | - | loose | 1 |  |
| `trim.download.all` | - | loose | 1 |  |
| `trim.fallback` | - | loose | 1 |  |
| `trim.file.path` | - | loose | 1 |  |
| `trim.file.read` | - | loose | 1 |  |
| `trim.file.sharedAccess` | - | loose | 1 |  |
| `trim.file.userAccess` | - | loose | 5 | 是 |
| `trim.file.userAcl` | - | loose | 1 |  |
| `trim.file.write` | - | loose | 1 |  |
| `trim.log.all` | - | loose | 1 |  |
| `trim.photo.all` | - | loose | 1 |  |
| `trim.sac` | - | loose | 1 |  |
| `trim.storage.all` | - | loose | 1 |  |
| `trim.system.all` | - | loose | 1 |  |
| `trim.system.platformConfig` | - | loose | 1 |  |
| `trim.trim_license` | - | loose | 2 |  |
| `trim.user.all` | - | loose | 1 |  |

## trustDevice

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `trustDevice.description` | - | loose | 1 | 是 |
| `trustDevice.title` | - | loose | 1 | 是 |
| `trustDevice.verifyDescription` | - | loose | 1 | 是 |
| `trustDevice.verifyTitle` | - | loose | 1 | 是 |

## type

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `type.elementType` | - | loose | 5 |  |

## ui

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `ui.cancel` | - | loose | 5 | 是 |
| `ui.cannotScanQR` | - | loose | 1 | 是 |
| `ui.confirm` | - | loose | 3 | 是 |
| `ui.currentDevice` | - | loose | 1 | 是 |
| `ui.emailAddress` | - | loose | 1 | 是 |
| `ui.getVerificationCode` | - | loose | 1 |  |
| `ui.iKnow` | - | loose | 1 | 是 |
| `ui.loginAt` | - | loose | 1 | 是 |
| `ui.resendCode` | - | loose | 1 |  |
| `ui.resendInSeconds` | - | loose | 1 | 是 |
| `ui.save` | - | loose | 2 | 是 |
| `ui.skip` | - | loose | 2 | 是 |
| `ui.trustDevice` | - | loose | 1 | 是 |
| `ui.untrustDevice` | - | loose | 1 | 是 |
| `ui.verificationCode` | - | loose | 1 | 是 |

## upload

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `upload.addFolder` | - | loose | 1 | 是 |
| `upload.clickOrDragFolder` | - | loose | 1 | 是 |
| `upload.createFolderFailed` | - | loose | 1 | 是 |
| `upload.dragToUpload` | - | loose | 1 | 是 |
| `upload.dropToAdd` | - | loose | 1 | 是 |
| `upload.errors.fileNameConflictWithDirectory` | - | loose | 1 | 是 |
| `upload.errors.filePathTooLong` | - | loose | 1 | 是 |
| `upload.errors.insufficientStorage` | - | loose | 1 | 是 |
| `upload.errors.invalidUploadPath` | - | loose | 1 | 是 |
| `upload.errors.permissionDenied` | - | loose | 1 | 是 |
| `upload.errors.quotaExceeded` | - | loose | 1 | 是 |
| `upload.errors.serverIOError` | - | loose | 1 | 是 |
| `upload.errors.serverInternalError` | - | loose | 1 | 是 |
| `upload.errors.tokenServerError` | - | loose | 1 | 是 |
| `upload.errors.unsupportedFileFormat` | - | loose | 1 | 是 |
| `upload.folderContainsSpecialChar` | - | loose | 1 | 是 |
| `upload.folderCount` | - | loose | 1 | 是 |
| `upload.folderUploadFailed` | - | loose | 3 | 是 |
| `upload.folderUploadFailedDetail` | - | loose | 3 | 是 |
| `upload.getUploadPathFailed` | - | loose | 2 | 是 |
| `upload.importGoogleTakeout` | - | loose | 3 | 是 |
| `upload.importGoogleTakeoutDesc` | `i18nKey` | alias_key,loose | 2 |  |
| `upload.importGoogleTakeoutInstruction` | - | loose | 1 | 是 |
| `upload.importGoogleTakeoutTip` | `i18nKey` | alias_key,loose | 4 |  |
| `upload.modifyBackupLocation` | - | loose | 2 | 是 |
| `upload.noStoragePermission` | - | loose | 3 | 是 |
| `upload.noStoragePermissionContent` | - | loose | 2 | 是 |
| `upload.noStoragePermissionTitle` | - | loose | 2 | 是 |
| `upload.pleaseAddFolder` | - | loose | 1 | 是 |
| `upload.rotateComplete` | - | loose | 1 | 是 |
| `upload.rotateCompleteWithFailed` | - | loose | 1 | 是 |
| `upload.rotateFailed` | - | loose | 1 | 是 |
| `upload.startImport` | - | loose | 1 |  |
| `upload.uploadComplete` | - | loose | 4 | 是 |
| `upload.uploadCompleteWithFailed` | - | loose | 4 | 是 |
| `upload.uploadFailed` | - | loose | 4 | 是 |
| `upload.uploadFromComputer` | - | loose | 1 | 是 |
| `upload.uploadPhotos` | - | loose | 2 | 是 |
| `upload.workerInitFailed` | - | loose | 5 | 是 |

## uploadConfig

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `uploadConfig.desc` | `field` | alias_key,loose | 2 |  |
| `uploadConfig.fileSizeLimit` | `field` | alias_key,loose | 2 |  |
| `uploadConfig.fileType` | `field` | alias_key,loose | 2 |  |
| `uploadConfig.path` | `field` | alias_key,loose | 2 |  |

## ups

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `ups.batteryRemoved` | - | loose | 1 | 是 |
| `ups.builtinBattery` | - | loose | 1 | 是 |
| `ups.builtinUps` | - | loose | 1 | 是 |
| `ups.connectionLost` | - | loose | 1 | 是 |
| `ups.laptopBattery` | - | loose | 1 | 是 |
| `ups.mainsPower` | - | loose | 1 | 是 |
| `ups.minutes` | - | loose | 1 | 是 |
| `ups.noEstimatedTime` | - | loose | 1 | 是 |
| `ups.normalConnection` | - | loose | 1 | 是 |
| `ups.remainingBattery` | - | loose | 1 | 是 |
| `ups.upsBatteryPower` | - | loose | 1 | 是 |

## userManagement

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `userManagement.common.textTooLong` | - | loose | 1 | 是 |
| `userManagement.group.groupNameAllNumber` | - | loose | 1 | 是 |
| `userManagement.group.groupNameInvalid` | - | loose | 1 | 是 |
| `userManagement.group.groupNameRequired` | - | loose | 1 | 是 |
| `userManagement.group.groupNameTooLong` | - | loose | 1 | 是 |
| `userManagement.password.adminChangePasswordNotice` | - | loose | 1 | 是 |
| `userManagement.password.changePassword` | - | loose | 1 | 是 |
| `userManagement.password.confirmPassword` | - | loose | 1 | 是 |
| `userManagement.password.inputPassword` | - | loose | 3 | 是 |
| `userManagement.password.inputPasswordAgain` | - | loose | 2 | 是 |
| `userManagement.password.logoutOtherDevices` | - | loose | 1 | 是 |
| `userManagement.password.newPassword` | - | loose | 1 |  |
| `userManagement.password.oldPassword` | - | loose | 1 | 是 |
| `userManagement.password.password` | - | loose | 1 |  |
| `userManagement.password.passwordCopied` | - | loose | 1 | 是 |
| `userManagement.password.passwordError` | - | loose | 1 | 是 |
| `userManagement.password.passwordInvalid` | - | loose | 1 | 是 |
| `userManagement.password.passwordNotMatch` | - | loose | 1 | 是 |
| `userManagement.password.passwordNotMatchSame` | - | loose | 1 | 是 |
| `userManagement.password.passwordRequired` | - | loose | 1 | 是 |
| `userManagement.password.passwordStrength` | - | loose | 1 | 是 |
| `userManagement.password.passwordTooLong` | - | loose | 1 | 是 |
| `userManagement.password.passwordWeak` | - | loose | 3 | 是 |
| `userManagement.password.randomPassword` | - | loose | 2 | 是 |
| `userManagement.user.usernameInvalid` | - | loose | 1 | 是 |
| `userManagement.user.usernameRequired` | - | loose | 1 | 是 |
| `userManagement.user.usernameTooLong` | - | loose | 1 | 是 |

## userSettings

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `userSettings.about` | - | loose | 1 | 是 |
| `userSettings.feedback` | - | loose | 1 | 是 |
| `userSettings.helpCenter` | - | loose | 1 | 是 |

## util

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `util.createDomFromHtml` | - | loose | 1 | 是 |
| `util.findDom` | - | loose | 1 | 是 |

## utils

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `utils.externalDeviceName.default` | - | loose | 1 | 是 |
| `utils.externalDeviceName.hdd` | - | loose | 1 | 是 |
| `utils.externalDeviceName.ssd` | - | loose | 1 | 是 |
| `utils.externalDeviceName.usb` | - | loose | 1 | 是 |
| `utils.taskNameValidator.forbiddenSymbols` | - | loose | 1 | 是 |
| `utils.taskNameValidator.invalidChars` | - | loose | 1 | 是 |
| `utils.taskNameValidator.required` | - | loose | 1 | 是 |
| `utils.taskNameValidator.startsWithDot` | - | loose | 1 | 是 |
| `utils.taskNameValidator.tooLong` | - | loose | 1 | 是 |
| `utils.tooManySelectedTips` | - | loose | 1 | 是 |
| `utils.userRootDirName` | - | loose | 1 | 是 |

## validation

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `validation.emailFormatError` | - | loose | 1 | 是 |
| `validation.passwordVerificationError` | - | loose | 1 | 是 |
| `validation.pleaseEnterEmail` | - | loose | 2 | 是 |
| `validation.pleaseEnterPassword` | - | loose | 2 | 是 |
| `validation.pleaseEnterSixDigitCode` | - | loose | 1 | 是 |
| `validation.pleaseEnterVerificationCode` | - | loose | 2 | 是 |
| `validation.verificationCodeFormatError` | - | loose | 1 | 是 |

## validator

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `validator.fileName.nameCannotBe` | - | loose | 1 | 是 |
| `validator.fileName.nameContainsSpecialChars` | - | loose | 1 | 是 |
| `validator.fileName.nameExceedsLimit` | - | loose | 1 | 是 |
| `validator.fileName.pleaseEnterName` | - | loose | 1 | 是 |

## volume

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `volume.alwaysInstallNewAppsHere` | - | loose | 2 | 是 |
| `volume.folderLocation` | - | loose | 1 | 是 |
| `volume.install` | - | loose | 3 | 是 |
| `volume.insufficientSpace` | - | loose | 2 | 是 |
| `volume.location` | - | loose | 1 | 是 |
| `volume.selectStorageSpace` | - | loose | 1 | 是 |
| `volume.title` | - | loose | 1 | 是 |

## vp09

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `vp09.00.50.08` | - | loose | 1 |  |

## wizard

| req | 别名 | 来源 | 分数 | i18n? |
| --- | --- | --- | --- | --- |
| `wizard.cancel` | - | loose | 6 | 是 |
| `wizard.install` | - | loose | 3 | 是 |
| `wizard.next` | - | loose | 5 | 是 |
| `wizard.prev` | - | loose | 4 | 是 |
| `wizard.uninstall` | - | loose | 1 |  |
| `wizard.uninstallConfirm` | - | loose | 1 |  |

# HTTP 接口（启发式提取）

- `/api/v1/ai-base/check-requirement`
- `/api/v1/ai-base/data-vol`
- `/api/v1/ai-base/gpu`
- `/api/v1/ai-base/gpus`
- `/api/v1/ai-base/init`
- `/api/v1/ai-base/setting`
- `/api/v1/ai-base/validate-gpu`
- `/api/v1/ai-face/cancel-install`
- `/api/v1/ai-face/default-run-params`
- `/api/v1/ai-face/enabled`
- `/api/v1/ai-face/install`
- `/api/v1/ai-face/install-options`
- `/api/v1/ai-face/run`
- `/api/v1/ai-face/run-params`
- `/api/v1/ai-face/status`
- `/api/v1/ai-face/uninstall`
- `/api/v1/ai-person/addFacesToPerson`
- `/api/v1/ai-person/create`
- `/api/v1/ai-person/detail`
- `/api/v1/ai-person/list`
- `/api/v1/ai-person/mergePeople`
- `/api/v1/ai-person/personByName`
- `/api/v1/ai-person/photoLibrary/timeLine`
- `/api/v1/ai-person/posterFromPhoto`
- `/api/v1/ai-person/remove`
- `/api/v1/ai-person/removeFacesFromPerson`
- `/api/v1/ai-person/removePhotosFromPerson`
- `/api/v1/ai-person/rename`
- `/api/v1/ai-person/separatePhotoFromPerson`
- `/api/v1/ai-person/setVisibility`
- `/api/v1/ai-person/transferPhotosFromPerson`
- `/api/v1/ai-smart-rec/cancel-install`
- `/api/v1/ai-smart-rec/categories`
- `/api/v1/ai-smart-rec/category-enabled`
- `/api/v1/ai-smart-rec/default-run-params`
- `/api/v1/ai-smart-rec/enabled`
- `/api/v1/ai-smart-rec/install`
- `/api/v1/ai-smart-rec/install-options`
- `/api/v1/ai-smart-rec/run`
- `/api/v1/ai-smart-rec/run-params`
- `/api/v1/ai-smart-rec/similarity-enabled`
- `/api/v1/ai-smart-rec/status`
- `/api/v1/ai-smart-rec/uninstall`
- `/api/v1/ai-smart-rec/update-smart-category`
- `/api/v1/ai-smart-rec/video-enabled`
- `/api/v1/album/baby/timeline`
- `/api/v1/album/condition/add`
- `/api/v1/album/condition/list`
- `/api/v1/album/condition/remove`
- `/api/v1/album/create`
- `/api/v1/album/delete`
- `/api/v1/album/download/all`
- `/api/v1/album/item`
- `/api/v1/album/list`
- `/api/v1/album/normal/timeline`
- `/api/v1/album/photo/belong`
- `/api/v1/album/photo/remove`
- `/api/v1/album/remove`
- `/api/v1/album/update/name`
- `/api/v1/album/update/poster`
- `/api/v1/album/update/setting`
- `/api/v1/album_grant/cancel`
- `/api/v1/album_grant/create`
- `/api/v1/album_grant/list_mine`
- `/api/v1/album_grant/list_to_me`
- `/api/v1/album_grant/update`
- `/api/v1/app/version`
- `/api/v1/config/detail`
- `/api/v1/config/update`
- `/api/v1/explore/geos`
- `/api/v1/explore/recent_timeline`
- `/api/v1/explore/tags`
- `/api/v1/file/copy`
- `/api/v1/file/delete`
- `/api/v1/file/download`
- `/api/v1/file/move`
- `/api/v1/file/rename`
- `/api/v1/file/task/cancel`
- `/api/v1/file/task/delete`
- `/api/v1/file/task/list`
- `/api/v1/fixer/photoType`
- `/api/v1/fixer/photoType/status`
- `/api/v1/folder_view/cover`
- `/api/v1/folder_view/cover/setting`
- `/api/v1/folder_view/getFileList`
- `/api/v1/folder_view/getFolderList`
- `/api/v1/gallery/addTo/album`
- `/api/v1/gallery/getList`
- `/api/v1/gallery/getOne`
- `/api/v1/gallery/timeline`
- `/api/v1/google_takeout/heartbeat`
- `/api/v1/google_takeout/notice`
- `/api/v1/google_takeout/prepare`
- `/api/v1/magic-search/category-prompt`
- `/api/v1/magic-search/do`
- `/api/v1/magic-search/prompt`
- `/api/v1/magic-search/ready`
- `/api/v1/magic-search/similar`
- `/api/v1/map/preview/initCenter`
- `/api/v1/map/preview/mapBoundary`
- `/api/v1/map/timeLine`
- `/api/v1/media_category/list`
- `/api/v1/photo/folder/add`
- `/api/v1/photo/folder/defaultInit`
- `/api/v1/photo/folder/list`
- `/api/v1/photo/folder/new`
- `/api/v1/photo/folder/reconnect`
- `/api/v1/photo/folder/remove`
- `/api/v1/photo/folder/scan`
- `/api/v1/photo/folder/scan/all`
- `/api/v1/photo/folder/view`
- `/api/v1/photo/support/list`
- `/api/v1/photo/upload/path`
- `/api/v1/preview/download`
- `/api/v1/preview/tag/add`
- `/api/v1/preview/tag/addForPhoto`
- `/api/v1/preview/tag/delForPhoto`
- `/api/v1/preview/tag/list`
- `/api/v1/preview/update/dateTime`
- `/api/v1/preview/update/geo`
- `/api/v1/recycle-bin/add`
- `/api/v1/recycle-bin/clean-all`
- `/api/v1/recycle-bin/delete`
- `/api/v1/recycle-bin/restore`
- `/api/v1/recycle-bin/timeline`
- `/api/v1/repeat-photo/check`
- `/api/v1/repeat-photo/exclude`
- `/api/v1/repeat-photo/keep`
- `/api/v1/repeat-photo/merge`
- `/api/v1/search/filterlist`
- `/api/v1/search/index`
- `/api/v1/search/index/status`
- `/api/v1/search/suggest/filter`
- `/api/v1/server/architecture`
- `/api/v1/server/file_list`
- `/api/v1/server/folder_manage`
- `/api/v1/server/sys_info`
- `/api/v1/server/user_group_all`
- `/api/v1/server/users_all`
- `/api/v1/share_link/cleanupInvalid`
- `/api/v1/share_link/delete`
- `/api/v1/share_link/detail`
- `/api/v1/share_link/list`
- `/api/v1/share_link/new`
- `/api/v1/share_link/update`
- `/api/v1/sys_config/list`
- `/api/v1/sys_config/setting`
- `/api/v1/sys_config/time_zone/support`
- `/api/v1/sys_config/video_decode`
- `/api/v1/sys_config/video_decode/list_gpu`
- `/api/v1/task-panel/cancel`
- `/api/v1/task-panel/clear-done`
- `/api/v1/task-panel/delete`
- `/api/v1/task-panel/fail`
- `/api/v1/task-panel/list`
- `/api/v1/task-panel/retry`
- `/api/v1/task-panel/retry-one`
- `/api/v1/task-panel/skip-one`
- `/api/v1/thumbnail/refresh`
- `/api/v1/thumbnail/status`
- `/api/v1/user/info`
- `/api/v1/user_photo/stat`
- `/api/v1/video/decode/info`
- `/api/v1/video/decode/play`
- `/api/v1/video/decode/quality`
- `/api/v2/photo/upload/path`
- `/api/v2/search/results`
- `/api/v2/server/pools`
- `/multiple-download`
- `/upload`
