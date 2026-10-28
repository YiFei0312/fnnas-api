# notify

> 自动生成（`python tools/gen_api.py`），共 6 个接口。
> 调用示例：`await client.api.notify.del_(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `del_` | `notify.del` | 未实测（写接口） | ⚠️ | - | - |
| `del_all` | `notify.delAll` | 未实测（写接口） | ⚠️ | - | - |
| `list` | `notify.list` | 已实测通过 | ✅ | page, pageSize | page, pageTotal, total |
| `set_read` | `notify.setRead` | 未实测（写接口） | ⚠️ | - | - |
| `set_read_all` | `notify.setReadAll` | 未实测（写接口） | ⚠️ | - | - |
| `unread_total` | `notify.unreadTotal` | 已实测通过 | ✅ | - | unreadTotal |

## 实测样例

### notify.list

状态：已实测通过，耗时 47.6ms

```json
{
  "total": 0,
  "page": 1,
  "pageTotal": 0,
  "result": "succ",
  "reqid": "6ad238556ad23836000002da00a3"
}
```

### notify.unreadTotal

状态：已实测通过，耗时 17.1ms

```json
{
  "unreadTotal": 0,
  "result": "succ",
  "reqid": "6ad238556ad23836000002da00a4"
}
```
