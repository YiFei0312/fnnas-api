# appcgi.iscsimgr

> 自动生成（`python tools/gen_api.py`），共 1 个接口。
> 调用示例：`await client.api.appcgi.iscsimgr.iscsi_lun_list(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `iscsi_lun_list` | `appcgi.iscsimgr.iscsi.lun.list` | 已实测存在（业务错误码） | ✅ | - | - |

## 实测样例

### appcgi.iscsimgr.iscsi.lun.list

状态：已实测存在（业务错误码）（errno=266240），耗时 4.1ms

```json
{
  "errno": 266240,
  "result": "fail",
  "reqid": "6ad238396ad23836000002da001d"
}
```
