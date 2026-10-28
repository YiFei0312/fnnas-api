# appcgi.sharesvr

> 自动生成（`python tools/gen_api.py`），共 13 个接口。
> 调用示例：`await client.api.appcgi.sharesvr.share_link_clear(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `share_link_clear` | `appcgi.sharesvr.share.link.clear` | 未实测（写接口） | ⚠️ | isAdmin | - |
| `share_link_create` | `appcgi.sharesvr.share.link.create` | 已实测通过 | ⚠️ | name, files, maxAccess, passwd, validTo, type, uploadConfig | data |
| `share_link_default` | `appcgi.sharesvr.share.link.default` | 未实测（写接口） | ⚠️ | - | - |
| `share_link_default_get` | `appcgi.sharesvr.share.link.default.get` | 已实测通过 | ✅ | - | data |
| `share_link_default_set` | `appcgi.sharesvr.share.link.default.set` | 未实测（写接口） | ⚠️ | mode, customize, rateLimit | - |
| `share_link_get` | `appcgi.sharesvr.share.link.get` | 已实测通过 | ✅ | id | data |
| `share_link_list` | `appcgi.sharesvr.share.link.list` | 已实测通过 | ✅ | page, pageSize, keyword, isAdmin, type, sortColumn, sortType | data |
| `share_link_remove` | `appcgi.sharesvr.share.link.remove` | 已实测通过 | ⚠️ | idList | data |
| `share_link_update` | `appcgi.sharesvr.share.link.update` | 已实测通过 | ⚠️ | id, name, maxAccess, passwd, validTo | data |
| `share_permission_get` | `appcgi.sharesvr.share.permission.get` | 已实测通过 | ✅ | - | data |
| `share_permission_set` | `appcgi.sharesvr.share.permission.set` | 未实测（写接口） | ⚠️ | mode | - |
| `share_uploadpermission_get` | `appcgi.sharesvr.share.uploadpermission.get` | 已实测通过 | ✅ | - | data |
| `share_uploadpermission_set` | `appcgi.sharesvr.share.uploadpermission.set` | 未实测（写接口） | ⚠️ | mode | - |

## 实测样例

### appcgi.sharesvr.share.link.create

状态：已实测通过，耗时 285.3ms

```json
{
  "result": "succ",
  "reqid": "6ad255766ad2557600000305000d",
  "data": {
    "id": "a5f36f3e809d4b998f",
    "name": "probe-share-1792169334",
    "maxAccess": 3,
    "access": 0,
    "validTo": 1792172934,
    "passwd": "probe1234",
    "uid": 1000,
    "type": 1,
    "status": "valid",
    "accessStatus": "valid",
    "createdTime": 1792169335631,
    "uploadConfig": {
      "path": "",
      "desc": "",
      "fileSizeLimit": 0,
      "fileType": ""
    }
  }
}
```

### appcgi.sharesvr.share.link.default.get

状态：已实测通过，耗时 178.0ms

```json
{
  "result": "succ",
  "reqid": "6ad255766ad25576000003050003",
  "data": {
    "mode": "default",
    "ddns": "",
    "customize": {
      "protocol": "",
      "domain": "",
      "port": "",
      "host": ""
    },
    "fnDefault": "http://192.168.1.11:5666",
    "rateLimit": {
      "upload": 0,
      "download": 0
    }
  }
}
```

### appcgi.sharesvr.share.link.get

状态：已实测通过，耗时 43.2ms

```json
{
  "result": "succ",
  "reqid": "6ad255776ad25576000003050011",
  "data": {
    "id": "a5f36f3e809d4b998f",
    "name": "probe-share-1792169334-edit",
    "maxAccess": 0,
    "access": 0,
    "validTo": 0,
    "passwd": "",
    "uid": 1000,
    "type": 1,
    "status": "valid",
    "accessStatus": "valid",
    "createdTime": 1792169335631,
    "files": [
      {
        "path": "/vol1/1000/tmp",
        "file": "20260127_195353.jpg",
        "isDir": 0
      }
    ],
    "uploadConfig": {
      "path": "",
      "desc": "",
      "fileSizeLimit": 0,
      "fileType": ""
    }
  }
}
```

### appcgi.sharesvr.share.link.list

状态：已实测通过，耗时 42.0ms

```json
{
  "result": "succ",
  "reqid": "6ad255776ad25576000003050013",
  "data": {
    "total": 0,
    "list": null
  }
}
```

### appcgi.sharesvr.share.link.remove

状态：已实测通过，耗时 43.1ms

```json
{
  "result": "succ",
  "reqid": "6ad255776ad25576000003050012",
  "data": {
    "failedCount": 0,
    "failedIdList": []
  }
}
```

### appcgi.sharesvr.share.link.update

状态：已实测通过，耗时 42.3ms

```json
{
  "result": "succ",
  "reqid": "6ad255776ad25576000003050010",
  "data": {
    "id": "a5f36f3e809d4b998f",
    "name": "probe-share-1792169334-edit",
    "maxAccess": 0,
    "access": 0,
    "validTo": 0,
    "passwd": "",
    "uid": 1000,
    "type": 1,
    "status": "valid",
    "accessStatus": "valid",
    "createdTime": 1792169335631,
    "uploadConfig": {
      "path": "",
      "desc": "",
      "fileSizeLimit": 0,
      "fileType": ""
    }
  }
}
```

### appcgi.sharesvr.share.permission.get

状态：已实测通过，耗时 42.8ms

```json
{
  "result": "succ",
  "reqid": "6ad255766ad25576000003050004",
  "data": {
    "mode": "all"
  }
}
```

### appcgi.sharesvr.share.uploadpermission.get

状态：已实测通过，耗时 47.9ms

```json
{
  "result": "succ",
  "reqid": "6ad255766ad25576000003050005",
  "data": {
    "mode": "admin"
  }
}
```
