# appcgi.mountmgr

> 自动生成（`python tools/gen_api.py`），共 15 个接口。
> 调用示例：`await client.api.appcgi.mountmgr.cache_refresh(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `cache_refresh` | `appcgi.mountmgr.cache.refresh` | 未实测（写接口） | ⚠️ | - | - |
| `check` | `appcgi.mountmgr.check` | 已实测存在（业务错误码） | ✅ | - | errmsg |
| `dfs_acquire_upload_cache_dir` | `appcgi.mountmgr.dfs.acquireUploadCacheDir` | 未实测（写接口） | ⚠️ | - | - |
| `dfs_clean_upload_cache_dir` | `appcgi.mountmgr.dfs.cleanUploadCacheDir` | 未实测（写接口） | ⚠️ | - | - |
| `dfs_start_upload` | `appcgi.mountmgr.dfs.startUpload` | 未实测（写接口） | ⚠️ | - | - |
| `list` | `appcgi.mountmgr.list` | 已实测通过 | ✅ | - | rsp |
| `mount` | `appcgi.mountmgr.mount` | 未实测（写接口） | ⚠️ | - | - |
| `mount_info` | `appcgi.mountmgr.mountInfo` | 已实测存在（业务错误码） | ✅ | - | errmsg |
| `setting_detail` | `appcgi.mountmgr.setting.detail` | 已实测通过 | ✅ | - | rsp |
| `setting_update` | `appcgi.mountmgr.setting.update` | 未实测（写接口） | ⚠️ | - | - |
| `shares` | `appcgi.mountmgr.shares` | 已实测存在（业务错误码） | ✅ | - | errmsg |
| `task_cancel` | `appcgi.mountmgr.task.cancel` | 未实测（写接口） | ⚠️ | - | - |
| `task_detail` | `appcgi.mountmgr.task.detail` | 已实测存在（业务错误码） | ✅ | - | errmsg |
| `task_list` | `appcgi.mountmgr.task.list` | 已实测通过 | ✅ | - | rsp |
| `umount` | `appcgi.mountmgr.umount` | 未实测（写接口） | ⚠️ | - | - |

## 实测样例

### appcgi.mountmgr.check

状态：已实测存在（业务错误码）（errno=51380225），耗时 125.8ms

```json
{
  "result": "fail",
  "errno": 51380225,
  "reqid": "6ad2383a6ad23836000002da0022",
  "errmsg": "Name is required"
}
```

### appcgi.mountmgr.list

状态：已实测通过，耗时 53.5ms

```json
{
  "result": "succ",
  "reqid": "6ad2383a6ad23836000002da0023",
  "rsp": null
}
```

### appcgi.mountmgr.mountInfo

状态：已实测存在（业务错误码）（errno=51380225），耗时 13.2ms

```json
{
  "result": "fail",
  "errno": 51380225,
  "reqid": "6ad2383a6ad23836000002da0024",
  "errmsg": "Path parameter is required"
}
```

### appcgi.mountmgr.setting.detail

状态：已实测通过，耗时 284.8ms

```json
{
  "result": "succ",
  "reqid": "6ad2383a6ad23836000002da0025",
  "rsp": {
    "cacheVol": 1,
    "vols": [
      1,
      2,
      3,
      4,
      5,
      6
    ]
  }
}
```

### appcgi.mountmgr.shares

状态：已实测存在（业务错误码）（errno=51380227），耗时 63.6ms

```json
{
  "result": "fail",
  "errno": 51380227,
  "reqid": "6ad2383b6ad23836000002da0026",
  "errmsg": "Address is required"
}
```

### appcgi.mountmgr.task.detail

状态：已实测存在（业务错误码）（errno=1001），耗时 37.1ms

```json
{
  "result": "fail",
  "errno": 1001,
  "reqid": "6ad2383b6ad23836000002da0027",
  "errmsg": "unexpected end of JSON input"
}
```

### appcgi.mountmgr.task.list

状态：已实测通过，耗时 12.7ms

```json
{
  "result": "succ",
  "reqid": "6ad2383b6ad23836000002da0028",
  "rsp": {
    "list": []
  }
}
```
