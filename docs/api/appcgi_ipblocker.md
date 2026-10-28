# appcgi.ipblocker

> 自动生成（`python tools/gen_api.py`），共 9 个接口。
> 调用示例：`await client.api.appcgi.ipblocker.add_allow_list(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `add_allow_list` | `appcgi.ipblocker.addAllowList` | 未实测（写接口） | ⚠️ | - | - |
| `add_deny_list` | `appcgi.ipblocker.addDenyList` | 未实测（写接口） | ⚠️ | - | - |
| `auto_block` | `appcgi.ipblocker.autoBlock` | 未实测（写接口） | ⚠️ | - | - |
| `auto_block_rule` | `appcgi.ipblocker.autoBlockRule` | 未实测（写接口） | ⚠️ | - | - |
| `delete_allow_list` | `appcgi.ipblocker.deleteAllowList` | 未实测（写接口） | ⚠️ | - | - |
| `delete_deny_list` | `appcgi.ipblocker.deleteDenyList` | 未实测（写接口） | ⚠️ | - | - |
| `query_allow_list` | `appcgi.ipblocker.queryAllowList` | 已实测通过 | ✅ | - | req, rev |
| `query_auto_block_rule` | `appcgi.ipblocker.queryAutoBlockRule` | 已实测通过 | ✅ | - | data, req, rev |
| `query_deny_list` | `appcgi.ipblocker.queryDenyList` | 已实测通过 | ✅ | - | data, req, rev |

## 实测样例

### appcgi.ipblocker.queryAllowList

状态：已实测通过，耗时 117.4ms

```json
{
  "reqid": "6ad238396ad23836000002da001a",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.ipblocker.queryAllowList"
}
```

### appcgi.ipblocker.queryAutoBlockRule

状态：已实测通过，耗时 18.8ms

```json
{
  "data": {
    "enable": false,
    "time": 5,
    "failedCount": 10,
    "banPeriod": 1
  },
  "reqid": "6ad238396ad23836000002da001b",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.ipblocker.queryAutoBlockRule"
}
```

### appcgi.ipblocker.queryDenyList

状态：已实测通过，耗时 0.4ms

```json
{
  "data": {},
  "reqid": "6ad238396ad23836000002da001c",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.ipblocker.queryDenyList"
}
```
