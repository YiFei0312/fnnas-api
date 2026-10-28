# appcgi.filestor

> 自动生成（`python tools/gen_api.py`），共 4 个接口。
> 调用示例：`await client.api.appcgi.filestor.get_app_dir_list(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `get_app_dir_list` | `appcgi.filestor.getAppDirList` | 已实测通过 | ✅ | - | data, req, rev |
| `get_sys_part_info` | `appcgi.filestor.getSysPartInfo` | 已实测通过 | ✅ | - | data, req, rev |
| `get_team_dir_list` | `appcgi.filestor.getTeamDirList` | 已实测通过 | ✅ | - | req, rev |
| `is_mount_point` | `appcgi.filestor.isMountPoint` | 已实测存在（缺参数） | ✅ | - | req, rev |

## 实测样例

### appcgi.filestor.getAppDirList

状态：已实测通过，耗时 66.6ms

```json
{
  "data": {
    "dirList": [
      {
        "name": "mcsmanager",
        "v": 4,
        "uid": 0,
        "gid": 0,
        "size": 76,
        "mtim": 1782832053,
        "btim": 1786452833,
        "atim": 1791383893,
        "dir": 1,
        "path": "vol4/@appshare/mcsmanager"
      },
      {
        "name": "fnnas.anime_subscription",
        "v": 1,
        "uid": 981,
        "gid": 976,
        "size": 8,
        "mtim": 1789735105,
        "btim": 1789735105,
        "atim": 1791383892,
        "dir": 1,
        "path": "vol1/@appshare/fnnas.anime_subscription"
      },
      {
        "name": "fnosBrowser",
        "v": 1,
        "uid": 980,
        "gid": 975,
        "size": 18,
        "mtim": 1789920243,
        "btim": 1789920243,
        "atim": 1791383892,
        "dir": 1,
        "path": "vol1/@appshare/fnosBrowser"
      },
      {
        "name": "zerotier",
        "v": 1,
        "uid": 979,
        "gid": 974,
        "size": 8,
        "mtim": 1790017609,
        "btim": 1790017609,
        "atim": 1791383892,
        "dir": 1,
        "path": "vol1/@appshare/zerotier"
      },
      {
        "name": "metube",
        "v": 1,
        "uid": 978,
   
... (截断)
```

### appcgi.filestor.getSysPartInfo

状态：已实测通过，耗时 49.8ms

```json
{
  "data": {
    "fssize": 67119927296,
    "frsize": 48413335552,
    "type": "SSD"
  },
  "reqid": "6ad238386ad23836000002da0016",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.filestor.getSysPartInfo"
}
```

### appcgi.filestor.getTeamDirList

状态：已实测通过，耗时 19.0ms

```json
{
  "reqid": "6ad238386ad23836000002da0017",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.filestor.getTeamDirList"
}
```

### appcgi.filestor.isMountPoint

状态：已实测存在（缺参数）（errno=100000002），耗时 12.7ms

```json
{
  "errno": 100000002,
  "reqid": "6ad238396ad23836000002da0018",
  "result": "fail",
  "rev": "0.1",
  "req": "appcgi.filestor.isMountPoint"
}
```
