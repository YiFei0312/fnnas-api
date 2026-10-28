# appcgi.backup

> 自动生成（`python tools/gen_api.py`），共 21 个接口。
> 调用示例：`await client.api.appcgi.backup.logger_list(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `logger_list` | `appcgi.backup.logger.list` | 已实测存在（缺参数） | ✅ | - | req, rev |
| `nas_find` | `appcgi.backup.nas.find` | 未实测（写接口） | ⚠️ | - | - |
| `storage_add` | `appcgi.backup.storage.add` | 未实测（写接口） | ⚠️ | - | - |
| `storage_check_connection` | `appcgi.backup.storage.checkConnection` | 已实测存在（缺参数） | ✅ | - | req, rev |
| `storage_create_dir` | `appcgi.backup.storage.createDir` | 未实测（写接口） | ⚠️ | - | - |
| `storage_delete` | `appcgi.backup.storage.delete` | 未实测（写接口） | ⚠️ | - | - |
| `storage_get_auth_url` | `appcgi.backup.storage.getAuthUrl` | 已实测存在（缺参数） | ✅ | - | req, rev |
| `storage_get_quota` | `appcgi.backup.storage.getQuota` | 已实测存在（缺参数） | ✅ | - | req, rev |
| `storage_list` | `appcgi.backup.storage.list` | 已实测通过 | ✅ | - | req, rev |
| `storage_list_dir` | `appcgi.backup.storage.listDir` | 已实测存在（缺参数） | ✅ | - | req, rev |
| `storage_update` | `appcgi.backup.storage.update` | 未实测（写接口） | ⚠️ | - | - |
| `task_add` | `appcgi.backup.task.add` | 未实测（写接口） | ⚠️ | - | - |
| `task_delete` | `appcgi.backup.task.delete` | 未实测（写接口） | ⚠️ | - | - |
| `task_detail` | `appcgi.backup.task.detail` | 已实测存在（缺参数） | ✅ | - | req, rev |
| `task_disable` | `appcgi.backup.task.disable` | 未实测（写接口） | ⚠️ | - | - |
| `task_enable` | `appcgi.backup.task.enable` | 未实测（写接口） | ⚠️ | - | - |
| `task_list` | `appcgi.backup.task.list` | 已实测存在（缺参数） | ✅ | （实测缺参数，参数名待补） | req, rev |
| `task_operations` | `appcgi.backup.task.operations` | 未实测（写接口） | ⚠️ | - | - |
| `task_run` | `appcgi.backup.task.run` | 未实测（写接口） | ⚠️ | - | - |
| `task_stop` | `appcgi.backup.task.stop` | 未实测（写接口） | ⚠️ | - | - |
| `task_update` | `appcgi.backup.task.update` | 未实测（写接口） | ⚠️ | - | - |

## 实测样例

### appcgi.backup.logger.list

状态：已实测存在（缺参数）（errno=100000002），耗时 18.2ms

```json
{
  "errno": 100000002,
  "reqid": "6ad238376ad23836000002da000b",
  "result": "fail",
  "rev": "0.1",
  "req": "appcgi.backup.logger.list"
}
```

### appcgi.backup.storage.checkConnection

状态：已实测存在（缺参数）（errno=100000002），耗时 50.9ms

```json
{
  "errno": 100000002,
  "reqid": "6ad238376ad23836000002da000c",
  "result": "fail",
  "rev": "0.1",
  "req": "appcgi.backup.storage.checkConnection"
}
```

### appcgi.backup.storage.getAuthUrl

状态：已实测存在（缺参数）（errno=100000002），耗时 83.4ms

```json
{
  "errno": 100000002,
  "reqid": "6ad238376ad23836000002da000d",
  "result": "fail",
  "rev": "0.1",
  "req": "appcgi.backup.storage.getAuthUrl"
}
```

### appcgi.backup.storage.getQuota

状态：已实测存在（缺参数）（errno=100000002），耗时 20.2ms

```json
{
  "errno": 100000002,
  "reqid": "6ad238376ad23836000002da000e",
  "result": "fail",
  "rev": "0.1",
  "req": "appcgi.backup.storage.getQuota"
}
```

### appcgi.backup.storage.list

状态：已实测通过，耗时 3.3ms

```json
{
  "reqid": "6ad238376ad23836000002da000f",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.backup.storage.list"
}
```

### appcgi.backup.storage.listDir

状态：已实测存在（缺参数）（errno=100000002），耗时 0.0ms

```json
{
  "errno": 100000002,
  "reqid": "6ad238376ad23836000002da0010",
  "result": "fail",
  "rev": "0.1",
  "req": "appcgi.backup.storage.listDir"
}
```

### appcgi.backup.task.detail

状态：已实测存在（缺参数）（errno=100000002），耗时 31.7ms

```json
{
  "errno": 100000002,
  "reqid": "6ad238376ad23836000002da0011",
  "result": "fail",
  "rev": "0.1",
  "req": "appcgi.backup.task.detail"
}
```

### appcgi.backup.task.list

状态：已实测存在（缺参数）（errno=100000002），耗时 70.9ms

```json
{
  "errno": 100000002,
  "reqid": "6ad238386ad23836000002da0012",
  "result": "fail",
  "rev": "0.1",
  "req": "appcgi.backup.task.list"
}
```
