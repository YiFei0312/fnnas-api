# appcgi.finder

> 自动生成（`python tools/gen_api.py`），共 4 个接口。
> 调用示例：`await client.api.appcgi.finder.cancel_search(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `cancel_search` | `appcgi.finder.cancelSearch` | 未实测（写接口） | ⚠️ | - | - |
| `file_search` | `appcgi.finder.fileSearch` | 未实测（写接口） | ⚠️ | key, path | - |
| `search_other_sharing` | `appcgi.finder.searchOtherSharing` | 已实测存在（缺参数） | ✅ | - | req, rev |
| `trash_search` | `appcgi.finder.trashSearch` | 未实测（写接口） | ⚠️ | - | - |

## 实测样例

### appcgi.finder.searchOtherSharing

状态：已实测存在（缺参数）（errno=100000002），耗时 30.9ms

```json
{
  "errno": 100000002,
  "reqid": "6ad238396ad23836000002da0019",
  "result": "fail",
  "rev": "0.1",
  "req": "appcgi.finder.searchOtherSharing"
}
```
