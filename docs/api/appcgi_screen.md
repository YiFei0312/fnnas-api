# appcgi.screen

> 自动生成（`python tools/gen_api.py`），共 9 个接口。
> 调用示例：`await client.api.appcgi.screen.get_image_upload_path(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `get_image_upload_path` | `appcgi.screen.getImageUploadPath` | 已实测存在（业务错误码） | ✅ | - | - |
| `get_options` | `appcgi.screen.getOptions` | 已实测存在（业务错误码） | ✅ | - | - |
| `get_screen_image` | `appcgi.screen.getScreenImage` | 已实测存在（业务错误码） | ✅ | - | - |
| `get_screen_size` | `appcgi.screen.getScreenSize` | 已实测存在（业务错误码） | ✅ | - | - |
| `get_screen_video` | `appcgi.screen.getScreenVideo` | 已实测存在（业务错误码） | ✅ | - | - |
| `is_sleeping` | `appcgi.screen.isSleeping` | 已实测存在（业务错误码） | ✅ | - | - |
| `set_options` | `appcgi.screen.setOptions` | 未实测（写接口） | ⚠️ | - | - |
| `set_screen_image` | `appcgi.screen.setScreenImage` | 未实测（写接口） | ⚠️ | - | - |
| `set_screen_video` | `appcgi.screen.setScreenVideo` | 未实测（写接口） | ⚠️ | - | - |

## 实测样例

### appcgi.screen.getImageUploadPath

状态：已实测存在（业务错误码）（errno=266240），耗时 2.7ms

```json
{
  "errno": 266240,
  "result": "fail",
  "reqid": "6ad238446ad23836000002da0059"
}
```

### appcgi.screen.getOptions

状态：已实测存在（业务错误码）（errno=266240），耗时 4.0ms

```json
{
  "errno": 266240,
  "result": "fail",
  "reqid": "6ad238446ad23836000002da005a"
}
```

### appcgi.screen.getScreenImage

状态：已实测存在（业务错误码）（errno=266240），耗时 0.5ms

```json
{
  "errno": 266240,
  "result": "fail",
  "reqid": "6ad238446ad23836000002da005b"
}
```

### appcgi.screen.getScreenSize

状态：已实测存在（业务错误码）（errno=266240），耗时 3.8ms

```json
{
  "errno": 266240,
  "result": "fail",
  "reqid": "6ad238446ad23836000002da005c"
}
```

### appcgi.screen.getScreenVideo

状态：已实测存在（业务错误码）（errno=266240），耗时 4.1ms

```json
{
  "errno": 266240,
  "result": "fail",
  "reqid": "6ad238446ad23836000002da005d"
}
```

### appcgi.screen.isSleeping

状态：已实测存在（业务错误码）（errno=266240），耗时 0.4ms

```json
{
  "errno": 266240,
  "result": "fail",
  "reqid": "6ad238446ad23836000002da005e"
}
```
