# appcgi.usersrv

> 自动生成（`python tools/gen_api.py`），共 2 个接口。
> 调用示例：`await client.api.appcgi.usersrv.auth_user(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `auth_user` | `appcgi.usersrv.authUser` | 未实测（写接口） | ⚠️ | - | - |
| `get_app_user_list` | `appcgi.usersrv.getAppUserList` | 已实测通过 | ✅ | - | data, req, rev |

## 实测样例

### appcgi.usersrv.getAppUserList

状态：已实测通过，耗时 3.5ms

```json
{
  "data": {
    "userList": [
      999,
      996,
      994,
      993,
      992,
      991,
      990,
      988,
      987,
      986,
      985,
      984,
      983,
      982,
      981,
      980,
      979,
      978,
      977,
      976,
      975,
      974
    ]
  },
  "reqid": "6ad238526ad23836000002da008a",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.usersrv.getAppUserList"
}
```
