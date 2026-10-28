# usrdat

> 自动生成（`python tools/gen_api.py`），共 5 个接口。
> 调用示例：`await client.api.usrdat.del_(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `del_` | `usrdat.del` | 未实测（写接口） | ⚠️ | - | - |
| `del_array` | `usrdat.delArray` | 未实测（写接口） | ⚠️ | - | - |
| `get` | `usrdat.get` | 已实测存在（缺参数） | ✅ | key(推测) | - |
| `set` | `usrdat.set` | 未实测（写接口） | ⚠️ | - | - |
| `set_array` | `usrdat.setArray` | 未实测（写接口） | ⚠️ | - | - |

## 实测样例

### usrdat.get

状态：已实测存在（缺参数）（errno=8192），耗时 9.6ms

```json
{
  "errno": 8192,
  "result": "fail",
  "reqid": "6ad2385a6ad23836000002da00c5"
}
```
