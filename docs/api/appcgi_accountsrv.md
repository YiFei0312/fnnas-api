# appcgi.accountsrv

> 自动生成（`python tools/gen_api.py`），共 3 个接口。
> 调用示例：`await client.api.appcgi.accountsrv.v1_token_edit(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `v1_token_edit` | `appcgi.accountsrv.v1.token.edit` | 未实测（写接口） | ⚠️ | - | - |
| `v1_token_list` | `appcgi.accountsrv.v1.token.list` | 已实测存在（业务错误码） | ✅ | - | data, errmsg |
| `v1_token_revoke` | `appcgi.accountsrv.v1.token.revoke` | 未实测（写接口） | ⚠️ | - | - |

## 实测样例

### appcgi.accountsrv.v1.token.list

状态：已实测存在（业务错误码）（errno=1），耗时 72.9ms

```json
{
  "result": "fail",
  "errno": 1,
  "reqid": "6ad238366ad23836000002da000a",
  "errmsg": "unexpected end of JSON input",
  "data": null
}
```
