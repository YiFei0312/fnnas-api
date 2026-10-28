# appcgi.eventlogger

> 自动生成（`python tools/gen_api.py`），共 7 个接口。
> 调用示例：`await client.api.appcgi.eventlogger.common_archive(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `common_archive` | `appcgi.eventlogger.common.archive` | 未实测（写接口） | ⚠️ | - | - |
| `common_archive_get` | `appcgi.eventlogger.common.archive.get` | 已实测通过 | ✅ | - | data, req, rev |
| `common_clear` | `appcgi.eventlogger.common.clear` | 未实测（写接口） | ⚠️ | - | - |
| `common_export` | `appcgi.eventlogger.common.export` | 未实测（写接口） | ⚠️ | - | - |
| `common_list` | `appcgi.eventlogger.common.list` | 已实测存在（缺参数） | ✅ | - | req, rev |
| `debuglog_copy_start` | `appcgi.eventlogger.debuglog.copyStart` | 未实测（写接口） | ⚠️ | - | - |
| `debuglog_copy_stop` | `appcgi.eventlogger.debuglog.copyStop` | 未实测（写接口） | ⚠️ | - | - |

## 实测样例

### appcgi.eventlogger.common.archive.get

状态：已实测通过，耗时 47.7ms

```json
{
  "data": {
    "switch": 0,
    "filePath": "",
    "validPath": 1
  },
  "reqid": "6ad238386ad23836000002da0013",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.eventlogger.common.archive.get"
}
```

### appcgi.eventlogger.common.list

状态：已实测存在（缺参数）（errno=100000002），耗时 38.1ms

```json
{
  "errno": 100000002,
  "reqid": "6ad238386ad23836000002da0014",
  "result": "fail",
  "rev": "0.1",
  "req": "appcgi.eventlogger.common.list"
}
```
