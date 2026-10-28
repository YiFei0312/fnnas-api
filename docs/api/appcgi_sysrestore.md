# appcgi.sysrestore

> 自动生成（`python tools/gen_api.py`），共 12 个接口。
> 调用示例：`await client.api.appcgi.sysrestore.add_sys_backup_task(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `add_sys_backup_task` | `appcgi.sysrestore.addSysBackupTask` | 未实测（写接口） | ⚠️ | - | - |
| `delete_sys_backup_bin` | `appcgi.sysrestore.deleteSysBackupBin` | 未实测（写接口） | ⚠️ | - | - |
| `do_sys_backup` | `appcgi.sysrestore.doSysBackup` | 未实测（写接口） | ⚠️ | - | - |
| `export_sysconf` | `appcgi.sysrestore.exportSysconf` | 未实测（写接口） | ⚠️ | - | - |
| `get_info` | `appcgi.sysrestore.getInfo` | 已实测通过 | ✅ | - | data, req, rev |
| `get_sys_backup_info` | `appcgi.sysrestore.getSysBackupInfo` | 已实测通过 | ✅ | - | data, req, rev |
| `get_sys_backup_task` | `appcgi.sysrestore.getSysBackupTask` | 已实测存在（业务错误码） | ✅ | - | req, rev |
| `get_sysconf_upload_path` | `appcgi.sysrestore.getSysconfUploadPath` | 已实测通过 | ✅ | - | data, req, rev |
| `import_sysconf` | `appcgi.sysrestore.importSysconf` | 未实测（写接口） | ⚠️ | - | - |
| `modify_sys_backup_task` | `appcgi.sysrestore.modifySysBackupTask` | 未实测（写接口） | ⚠️ | - | - |
| `set_system_recovery` | `appcgi.sysrestore.setSystemRecovery` | 未实测（写接口） | ⚠️ | - | - |
| `sysconf_import_progress` | `appcgi.sysrestore.sysconfImportProgress` | 未实测（写接口） | ⚠️ | - | - |

## 实测样例

### appcgi.sysrestore.getInfo

状态：已实测通过，耗时 33.9ms

```json
{
  "data": {
    "resetToFactory": {
      "supported": false,
      "reason": 100160031
    },
    "restoreStorage": {
      "supported": false
    }
  },
  "reqid": "6ad238516ad23836000002da0082",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.sysrestore.getInfo"
}
```

### appcgi.sysrestore.getSysBackupInfo

状态：已实测通过，耗时 20.9ms

```json
{
  "data": {
    "status": 1
  },
  "reqid": "6ad238516ad23836000002da0083",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.sysrestore.getSysBackupInfo"
}
```

### appcgi.sysrestore.getSysBackupTask

状态：已实测存在（业务错误码）（errno=100160045），耗时 3.7ms

```json
{
  "errno": 100160045,
  "reqid": "6ad238516ad23836000002da0084",
  "result": "fail",
  "rev": "0.1",
  "req": "appcgi.sysrestore.getSysBackupTask"
}
```

### appcgi.sysrestore.getSysconfUploadPath

状态：已实测通过，耗时 0.0ms

```json
{
  "data": {
    "dirPath": "/vol5/.cache.trim-sysrestore/import"
  },
  "reqid": "6ad238516ad23836000002da0085",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.sysrestore.getSysconfUploadPath"
}
```
