# appcgi.license

> 自动生成（`python tools/gen_api.py`），共 10 个接口。
> 调用示例：`await client.api.appcgi.license.soft_code_active(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `soft_code_active` | `appcgi.license.soft.code.active` | 未实测（写接口） | ⚠️ | - | - |
| `soft_code_license` | `appcgi.license.soft.code.license` | 未实测（写接口） | ⚠️ | - | - |
| `soft_get` | `appcgi.license.soft.get` | 已实测存在（业务错误码） | ✅ | - | data, errmsg |
| `soft_ipc_get` | `appcgi.license.soft.ipc.get` | 已实测存在（业务错误码） | ✅ | - | data, errmsg |
| `soft_list` | `appcgi.license.soft.list` | 已实测存在（业务错误码） | ✅ | - | data, errmsg |
| `soft_recover` | `appcgi.license.soft.recover` | 未实测（写接口） | ⚠️ | - | - |
| `soft_remove` | `appcgi.license.soft.remove` | 未实测（写接口） | ⚠️ | - | - |
| `soft_test_sendnotify` | `appcgi.license.soft.test.sendnotify` | 未实测（写接口） | ⚠️ | - | - |
| `soft_trial` | `appcgi.license.soft.trial` | 未实测（写接口） | ⚠️ | - | - |
| `soft_trial_applystatus` | `appcgi.license.soft.trial.applystatus` | 已实测通过 | ✅ | - | data |

## 实测样例

### appcgi.license.soft.get

状态：已实测存在（业务错误码）（errno=102550007），耗时 37.0ms

```json
{
  "result": "fail",
  "errno": 102550007,
  "reqid": "6ad238396ad23836000002da001e",
  "errmsg": "Bad Request",
  "data": null
}
```

### appcgi.license.soft.ipc.get

状态：已实测存在（业务错误码）（errno=102550007），耗时 3.6ms

```json
{
  "result": "fail",
  "errno": 102550007,
  "reqid": "6ad238396ad23836000002da001f",
  "errmsg": "Bad Request",
  "data": null
}
```

### appcgi.license.soft.list

状态：已实测存在（业务错误码）（errno=102550007），耗时 0.5ms

```json
{
  "result": "fail",
  "errno": 102550007,
  "reqid": "6ad2383a6ad23836000002da0020",
  "errmsg": "Bad Request",
  "data": null
}
```

### appcgi.license.soft.trial.applystatus

状态：已实测通过，耗时 82.9ms

```json
{
  "result": "succ",
  "reqid": "6ad2383a6ad23836000002da0021",
  "data": false
}
```
