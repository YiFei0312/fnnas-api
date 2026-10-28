# liveupdate

> 自动生成（`python tools/gen_api.py`），共 4 个接口。
> 调用示例：`await client.api.liveupdate.check(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `check` | `liveupdate.check` | 已实测通过 | ✅ | - | branchId |
| `fixapt` | `liveupdate.fixapt` | 未实测（写接口） | ⚠️ | - | - |
| `status` | `liveupdate.status` | 已实测通过 | ✅ | - | - |
| `update` | `liveupdate.update` | 未实测（写接口） | ⚠️ | - | - |

## 实测样例

### liveupdate.check

状态：已实测通过，耗时 296.1ms

```json
{
  "branchId": 2,
  "reqid": "6ad238546ad23836000002da009f",
  "result": "succ"
}
```

### liveupdate.status

状态：已实测通过，耗时 0.6ms

```json
{
  "result": "succ",
  "reqid": "6ad238556ad23836000002da00a0"
}
```
