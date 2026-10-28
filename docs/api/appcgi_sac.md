# appcgi.sac

> 自动生成（`python tools/gen_api.py`），共 39 个接口。
> 调用示例：`await client.api.appcgi.sac.desktop_v1_get_config(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `desktop_v1_get_config` | `appcgi.sac.desktop.v1.getConfig` | 已实测通过 | ✅ | - | data |
| `desktop_v1_mark_wallpaper` | `appcgi.sac.desktop.v1.markWallpaper` | 未实测（写接口） | ⚠️ | - | - |
| `desktop_v1_remove_wallpaper` | `appcgi.sac.desktop.v1.removeWallpaper` | 未实测（写接口） | ⚠️ | - | - |
| `desktop_v1_set_bg_color` | `appcgi.sac.desktop.v1.setBgColor` | 未实测（写接口） | ⚠️ | - | - |
| `desktop_v1_set_color` | `appcgi.sac.desktop.v1.setColor` | 未实测（写接口） | ⚠️ | - | - |
| `desktop_v1_set_fill_mode` | `appcgi.sac.desktop.v1.setFillMode` | 未实测（写接口） | ⚠️ | - | - |
| `desktop_v1_set_theme` | `appcgi.sac.desktop.v1.setTheme` | 未实测（写接口） | ⚠️ | - | - |
| `desktop_v1_set_wallpaper` | `appcgi.sac.desktop.v1.setWallpaper` | 未实测（写接口） | ⚠️ | - | - |
| `desktop_v1_set_wallpaper_type` | `appcgi.sac.desktop.v1.setWallpaperType` | 未实测（写接口） | ⚠️ | - | - |
| `entry_v1_add_user_desktop_entry` | `appcgi.sac.entry.v1.addUserDesktopEntry` | 未实测（写接口） | ⚠️ | - | - |
| `entry_v1_app_store_list` | `appcgi.sac.entry.v1.appStoreList` | 已实测通过 | ✅ | - | data |
| `entry_v1_del_user_desktop_entry` | `appcgi.sac.entry.v1.delUserDesktopEntry` | 未实测（写接口） | ⚠️ | - | - |
| `entry_v1_docker_list` | `appcgi.sac.entry.v1.dockerList` | 已实测通过 | ✅ | - | data |
| `entry_v1_edit_user_desktop_entry` | `appcgi.sac.entry.v1.editUserDesktopEntry` | 未实测（写接口） | ⚠️ | - | - |
| `entry_v1_exchange_entry_token` | `appcgi.sac.entry.v1.exchangeEntryToken` | 未实测（写接口） | ⚠️ | - | - |
| `entry_v1_file_associations_all` | `appcgi.sac.entry.v1.fileAssociations.all` | 未实测（写接口） | ⚠️ | - | - |
| `entry_v1_file_associations_list` | `appcgi.sac.entry.v1.fileAssociations.list` | 已实测通过 | ✅ | - | data |
| `entry_v1_file_associations_set_default` | `appcgi.sac.entry.v1.fileAssociations.setDefault` | 未实测（写接口） | ⚠️ | - | - |
| `entry_v1_get_entry_list` | `appcgi.sac.entry.v1.getEntryList` | 已实测通过 | ✅ | - | data |
| `entry_v1_get_user_desktop` | `appcgi.sac.entry.v1.getUserDesktop` | 已实测通过 | ✅ | - | data |
| `entry_v1_record_desktop_sort` | `appcgi.sac.entry.v1.recordDesktopSort` | 未实测（写接口） | ⚠️ | - | - |
| `externalnotify_v1_email_build_o_auth_url` | `appcgi.sac.externalnotify.v1.email.buildOAuthURL` | 未实测（写接口） | ⚠️ | - | - |
| `externalnotify_v1_email_get_access_token` | `appcgi.sac.externalnotify.v1.email.getAccessToken` | 已实测存在（业务错误码） | ✅ | - | data |
| `externalnotify_v1_email_get_config` | `appcgi.sac.externalnotify.v1.email.getConfig` | 已实测通过 | ✅ | - | data |
| `externalnotify_v1_email_get_providers` | `appcgi.sac.externalnotify.v1.email.getProviders` | 已实测通过 | ✅ | - | data |
| `externalnotify_v1_email_revoke_o_auth` | `appcgi.sac.externalnotify.v1.email.revokeOAuth` | 未实测（写接口） | ⚠️ | - | - |
| `externalnotify_v1_email_send_test_email` | `appcgi.sac.externalnotify.v1.email.sendTestEmail` | 未实测（写接口） | ⚠️ | - | - |
| `externalnotify_v1_email_start_or_update_server_config` | `appcgi.sac.externalnotify.v1.email.startOrUpdateServerConfig` | 未实测（写接口） | ⚠️ | - | - |
| `externalnotify_v1_email_stop` | `appcgi.sac.externalnotify.v1.email.stop` | 未实测（写接口） | ⚠️ | - | - |
| `externalnotify_v1_email_update_config` | `appcgi.sac.externalnotify.v1.email.updateConfig` | 未实测（写接口） | ⚠️ | - | - |
| `i18n_v1_config_get` | `appcgi.sac.i18n.v1.config.get` | 已实测通过 | ✅ | - | data |
| `i18n_v1_config_set` | `appcgi.sac.i18n.v1.config.set` | 未实测（写接口） | ⚠️ | - | - |
| `license_v1_config_get` | `appcgi.sac.license.v1.config.get` | 已实测通过 | ✅ | - | data |
| `license_v1_config_set` | `appcgi.sac.license.v1.config.set` | 未实测（写接口） | ⚠️ | - | - |
| `ups_v1_bind_or_unbind` | `appcgi.sac.ups.v1.bindOrUnbind` | 未实测（写接口） | ⚠️ | - | - |
| `ups_v1_check` | `appcgi.sac.ups.v1.check` | 已实测存在（业务错误码） | ✅ | - | data, errmsg |
| `ups_v1_device_list` | `appcgi.sac.ups.v1.deviceList` | 未实测（写接口） | ⚠️ | - | - |
| `ups_v1_list` | `appcgi.sac.ups.v1.list` | 已实测通过 | ✅ | - | data |
| `ups_v1_status` | `appcgi.sac.ups.v1.status` | 已实测通过 | ✅ | - | data |

## 实测样例

### appcgi.sac.desktop.v1.getConfig

状态：已实测通过，耗时 120.0ms

```json
{
  "result": "succ",
  "reqid": "6ad238416ad23836000002da004b",
  "data": {
    "userPreference": {
      "theme": 10,
      "wallpaperType": 100,
      "singlePhotoWpId": 1,
      "singleColorWpId": 7,
      "dynamicWpId": 8,
      "fillModeType": 0,
      "bgFillColorCode": "#444444",
      "bgOpacity": 100
    },
    "singlePhotoWallpapers": [
      {
        "id": 1,
        "type": 100,
        "name": "Sys Photo1",
        "url": "/static/bg/wallpaper-1.webp",
        "thumbnailUrl": "/static/thumbnail_bg/wallpaper-1.webp",
        "createdAt": "2026-09-12 21:15:29",
        "updatedAt": "2026-09-12 21:15:29"
      },
      {
        "id": 2,
        "type": 100,
        "name": "Sys Photo2",
        "url": "/static/bg/wallpaper-2.webp",
        "thumbnailUrl": "/static/thumbnail_bg/wallpaper-2.webp",
        "createdAt": "2026-09-12 21:15:29",
        "updatedAt": "2026-09-12 21:15:29"
      },
      {
        "id": 3,
        "type": 100,
        "name": "Sys Photo3",
        "url": "/static/bg/wallpaper-3.webp",
        "thumbnailUrl": "/static/thumbnail_bg/wallpaper-3.webp",
        "createdAt": "2026-09-12 21:15:29",
        "updatedAt": "2026-09-12 21:15:29"
      },
 
... (截断)
```

### appcgi.sac.entry.v1.appStoreList

状态：已实测通过，耗时 32.0ms

```json
{
  "result": "succ",
  "reqid": "6ad238426ad23836000002da004c",
  "data": {
    "list": [
      {
        "entryKey": "",
        "source": "trim.app-center",
        "appName": "anime_nasapi",
        "appType": "installed",
        "appID": "58",
        "entryName": "anime_nasapi.Application",
        "title": "飞牛NAS_API",
        "icon": "/app-center-static/serviceicon/anime_nasapi/ui/images/icon_{0}.png",
        "type": "iframe",
        "uri": {
          "protocol": "http",
          "host": "",
          "port": "3212",
          "path": "/",
          "fnDomain": "anime-nasapi"
        },
        "microApp": false,
        "nativeApp": false,
        "fullUrl": "",
        "status": "running",
        "fileTypes": [],
        "isDisplay": true,
        "appSource": "thirdparty",
        "feature": {}
      },
      {
        "entryKey": "",
        "source": "trim.app-center",
        "appName": "dmhy_collector",
        "appType": "installed",
        "appID": "55",
        "entryName": "dmhy_collector.Application",
        "title": "动漫花园采集",
        "icon": "/app-center-static/serviceicon/dmhy_collector/ui/images/icon_{0}.png",
        "type": "iframe",
        "uri": 
... (截断)
```

### appcgi.sac.entry.v1.dockerList

状态：已实测通过，耗时 22.2ms

```json
{
  "result": "succ",
  "reqid": "6ad238426ad23836000002da004d",
  "data": {
    "list": [
      {
        "entryKey": "",
        "source": "docker",
        "appName": "19bb41dc6b8a",
        "appType": "built-in",
        "appID": "19bb41dc6b8a",
        "entryName": "19bb41dc6b8a_0",
        "title": "llbot8:3080",
        "icon": "",
        "type": "open",
        "uri": {
          "protocol": "http",
          "host": "127.0.0.1",
          "port": "3080",
          "path": "",
          "fnDomain": "19bb41dc6b8a-0"
        },
        "microApp": false,
        "nativeApp": false,
        "fullUrl": "",
        "status": "running",
        "fileTypes": null,
        "isDisplay": true,
        "feature": {}
      },
      {
        "entryKey": "",
        "source": "docker",
        "appName": "705c2a5dc100",
        "appType": "built-in",
        "appID": "705c2a5dc100",
        "entryName": "705c2a5dc100_0",
        "title": "langbot:2280",
        "icon": "",
        "type": "open",
        "uri": {
          "protocol": "http",
          "host": "127.0.0.1",
          "port": "2280",
          "path": "",
          "fnDomain": "705c2a5dc100-0"
        },
        "microAp
... (截断)
```

### appcgi.sac.entry.v1.fileAssociations.list

状态：已实测通过，耗时 19.9ms

```json
{
  "result": "succ",
  "reqid": "6ad238426ad23836000002da004e",
  "data": {
    "list": []
  }
}
```

### appcgi.sac.entry.v1.getEntryList

状态：已实测通过，耗时 32.0ms

```json
{
  "result": "succ",
  "reqid": "6ad238426ad23836000002da004f",
  "data": {
    "list": [
      {
        "entryKey": "entry:1",
        "source": "built-in",
        "appName": "trim.file-manager",
        "appType": "built-in",
        "appID": "trim.file-manager",
        "entryName": "trim.file-manager",
        "title": "文件管理",
        "icon": "/static/app/icons/trim.file-manager/icon.png",
        "type": "open",
        "uri": {
          "protocol": "",
          "host": "",
          "port": "",
          "path": "",
          "fnDomain": ""
        },
        "microApp": false,
        "nativeApp": false,
        "fullUrl": "",
        "status": "running",
        "fileTypes": [],
        "isDisplay": true,
        "feature": {}
      },
      {
        "entryKey": "entry:2",
        "source": "built-in",
        "appName": "trim.setting",
        "appType": "built-in",
        "appID": "trim.setting",
        "entryName": "trim.setting",
        "title": "系统设置",
        "icon": "/static/app/icons/trim.setting/icon.png",
        "type": "open",
        "uri": {
          "protocol": "",
          "host": "",
          "port": "",
          "path": "",
          "fnDomain
... (截断)
```

### appcgi.sac.entry.v1.getUserDesktop

状态：已实测通过，耗时 18.7ms

```json
{
  "result": "succ",
  "reqid": "6ad238426ad23836000002da0050",
  "data": {
    "list": [
      {
        "entryKey": "entry:1",
        "source": "built-in",
        "itemType": "entry",
        "name": "文件管理",
        "folderPath": "",
        "sort": 10,
        "entry": {
          "appType": "",
          "sourceName": "built-in",
          "appName": "trim.file-manager",
          "serviceName": "trim.file-manager",
          "appID": "",
          "title": "文件管理",
          "icon": "/static/app/icons/trim.file-manager/icon.png",
          "openType": "open",
          "gatewaySocket": "",
          "gatewayPrefix": "",
          "url": {},
          "fullURL": "",
          "fnConnectConfig": {
            "allowProxy": 0
          },
          "display": {
            "isAdmin": false,
            "show": true,
            "order": 0
          },
          "status": null,
          "feature": {},
          "fileTypes": null,
          "state": "",
          "microApp": false,
          "nativeApp": false,
          "installTime": "",
          "updateTime": ""
        }
      },
      {
        "entryKey": "entry:2",
        "source": "built-in",
        "itemType": "entry
... (截断)
```

### appcgi.sac.externalnotify.v1.email.getAccessToken

状态：已实测存在（业务错误码）（errno=102550007），耗时 20.4ms

```json
{
  "result": "fail",
  "errno": 102550007,
  "reqid": "6ad238426ad23836000002da0051",
  "data": null
}
```

### appcgi.sac.externalnotify.v1.email.getConfig

状态：已实测通过，耗时 20.4ms

```json
{
  "result": "succ",
  "reqid": "6ad238426ad23836000002da0052",
  "data": {
    "subjectPrefix": "demoNAS",
    "isSetSubjectPrefix": false,
    "status": 0
  }
}
```

### appcgi.sac.externalnotify.v1.email.getProviders

状态：已实测通过，耗时 4.0ms

```json
{
  "result": "succ",
  "reqid": "6ad238436ad23836000002da0053",
  "data": [
    {
      "id": 1,
      "name": "Gmail",
      "type": "oauth2"
    },
    {
      "id": 2,
      "name": "Outlook",
      "type": "oauth2"
    },
    {
      "id": 3,
      "name": "Gmail（授权码）",
      "type": "code",
      "port": 587
    },
    {
      "id": 4,
      "name": "QQ邮箱",
      "type": "code",
      "port": 587
    },
    {
      "id": 5,
      "name": "126邮箱",
      "type": "code",
      "port": 994
    },
    {
      "id": 6,
      "name": "163邮箱",
      "type": "code",
      "port": 994
    },
    {
      "id": 7,
      "name": "自定义",
      "type": "custom"
    }
  ]
}
```

### appcgi.sac.i18n.v1.config.get

状态：已实测通过，耗时 26.6ms

```json
{
  "result": "succ",
  "reqid": "6ad238436ad23836000002da0054",
  "data": {
    "systemLanguage": "zh-CN",
    "languageList": [
      {
        "code": "zh-CN",
        "name": "简体中文",
        "region": "中国大陆"
      }
    ]
  }
}
```

### appcgi.sac.license.v1.config.get

状态：已实测通过，耗时 104.1ms

```json
{
  "result": "succ",
  "reqid": "6ad238436ad23836000002da0055",
  "data": {
    "isCommercial": false,
    "isActivatedLicense": true
  }
}
```

### appcgi.sac.ups.v1.check

状态：已实测存在（业务错误码）（errno=10000001），耗时 4.4ms

```json
{
  "result": "fail",
  "errno": 10000001,
  "reqid": "6ad238436ad23836000002da0056",
  "errmsg": "unexpected end of JSON input",
  "data": null
}
```

### appcgi.sac.ups.v1.list

状态：已实测通过，耗时 70.1ms

```json
{
  "result": "succ",
  "reqid": "6ad238436ad23836000002da0057",
  "data": []
}
```

### appcgi.sac.ups.v1.status

状态：已实测通过，耗时 20.6ms

```json
{
  "result": "succ",
  "reqid": "6ad238436ad23836000002da0058",
  "data": {
    "upsEnabled": false,
    "upsType": "",
    "upsTypeName": "",
    "shutdownUpsEnabled": false,
    "currentUps": {
      "name": "",
      "vendor": "",
      "product": "",
      "vendorId": "",
      "productId": "",
      "status": false,
      "batteryCharge": "",
      "powerSupplyType": "",
      "runtime": "",
      "shutdownPolicyType": "",
      "shutdownPolicyOnBattValue": 0,
      "shutdownPolicyLowBattValue": 0,
      "shutdownPolicyUnit": "",
      "batteryCapacity": ""
    }
  }
}
```
