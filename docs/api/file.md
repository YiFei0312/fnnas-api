# file

> 自动生成（`python tools/gen_api.py`），共 44 个接口。
> 调用示例：`await client.api.file.access(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `access` | `file.access` | 已实测通过 | ✅ | files | access |
| `calc` | `file.calc` | 已实测通过 | ✅ | files | dirCount, fileCount, fileSizeTotal, space |
| `cancel` | `file.cancel` | 已实测存在（缺参数） | ⚠️ | taskId | - |
| `check_upload` | `file.checkUpload` | 已实测通过 | ✅ | size, path, overwrite | uploadName |
| `chown` | `file.chown` | 已实测通过 | ⚠️ | files, uid, gid | sysNotify, taskId |
| `compress` | `file.compress` | 已实测通过 | ⚠️ | description, path, files, level, passwd, details | sysNotify, taskId |
| `cp` | `file.cp` | 已实测通过 | ⚠️ | files, pathTo, overwrite, details | sysNotify, taskId |
| `download` | `file.download` | 已实测通过 | ⚠️ | files | download |
| `extract` | `file.extract` | 已实测通过 | ⚠️ | description, path, file, overwrite, fromCharset, details | sysNotify, taskId |
| `fav_add` | `file.fav.add` | 已实测通过 | ⚠️ | path | - |
| `fav_del` | `file.fav.del` | 已实测通过 | ⚠️ | path | - |
| `fav_list` | `file.fav.list` | 已实测通过 | ✅ | - | fav, uver |
| `get_acl` | `file.getAcl` | 已实测通过 | ✅ | path, getProp | aclType, uver |
| `ls` | `file.ls` | 已实测通过 | ✅ | path | files, uver |
| `ls_dir` | `file.lsDir` | 已实测通过 | ✅ | path | uver |
| `mkdir` | `file.mkdir` | 已实测通过 | ⚠️ | path | - |
| `mv` | `file.mv` | 已实测通过 | ⚠️ | files, pathTo, overwrite, details | sysNotify, taskId |
| `prop` | `file.prop` | 已实测通过 | ✅ | files | prop, uver |
| `recent_add` | `file.recent.add` | 已实测通过 | ⚠️ | path | - |
| `recent_clear` | `file.recent.clear` | 未实测（写接口） | ⚠️ | - | - |
| `recent_del` | `file.recent.del` | 已实测通过 | ⚠️ | path | - |
| `recent_list` | `file.recent.list` | 已实测通过 | ✅ | - | recent, uver |
| `rename` | `file.rename` | 已实测通过 | ⚠️ | path, newName | - |
| `rm` | `file.rm` | 已实测通过 | ⚠️ | files, moveToTrashbin, details | sysNotify, taskId |
| `set_acl` | `file.setAcl` | 未实测（写接口） | ⚠️ | - | - |
| `set_acl2` | `file.setAcl2` | 已实测通过 | ⚠️ | files, permset, details, sub | sysNotify, taskId |
| `share_add` | `file.share.add` | 未实测（写接口） | ⚠️ | - | - |
| `share_add2` | `file.share.add2` | 未实测（写接口） | ⚠️ | path, shareName | - |
| `share_del2` | `file.share.del2` | 未实测（写接口） | ⚠️ | path | - |
| `share_info` | `file.share.info` | 已实测通过 | ✅ | path | uver |
| `share_list` | `file.share.list` | 已实测通过 | ✅ | - | - |
| `share_list_others` | `file.share.listOthers` | 已实测通过 | ✅ | - | uver |
| `size` | `file.size` | 已实测通过 | ✅ | file | size |
| `team_ls_dir` | `file.team.lsDir` | 已实测通过 | ✅ | - | uver |
| `team_trash_clear` | `file.team.trash.clear` | 未实测（写接口） | ⚠️ | - | - |
| `team_trash_list` | `file.team.trash.list` | 已实测存在（缺参数） | ✅ | - | - |
| `team_trash_list_trashbin` | `file.team.trash.listTrashbin` | 已实测通过 | ✅ | - | uver |
| `team_trash_restore` | `file.team.trash.restore` | 未实测（写接口） | ⚠️ | - | - |
| `trash_clear` | `file.trash.clear` | 未实测（写接口） | ⚠️ | uid | - |
| `trash_list` | `file.trash.list` | 已实测通过 | ✅ | uid, path, key | files, uver |
| `trash_restore` | `file.trash.restore` | 未实测（写接口） | ⚠️ | files, details, overwrite | - |
| `trimacl_conv` | `file.trimacl.conv` | 已实测存在（缺参数） | ⚠️ | - | - |
| `trimacl_conv_report` | `file.trimacl.conv.report` | 已实测存在（缺参数） | ⚠️ | - | - |
| `usage` | `file.usage` | 已实测通过 | ✅ | - | sysNotify, taskId |

## 实测样例

### file.access

状态：已实测通过，耗时 37.6ms

```json
{
  "access": [
    32718
  ],
  "result": "succ",
  "reqid": "6ad274f76ad274f60000033e000b"
}
```

### file.calc

状态：已实测通过，耗时 42.4ms

```json
{
  "fileSizeTotal": 1880200,
  "space": 1884160,
  "fileCount": 1,
  "dirCount": 0,
  "result": "succ",
  "reqid": "6ad274f76ad274f60000033e000c"
}
```

### file.cancel

状态：已实测存在（缺参数）（errno=8192），耗时 15.7ms

```json
{
  "errno": 8192,
  "result": "fail",
  "reqid": "6ad274f76ad274f60000033e001f"
}
```

### file.checkUpload

状态：已实测通过，耗时 0.0ms

```json
{
  "uploadName": "trash-victim.txt.~#0",
  "result": "succ",
  "reqid": "6ad274fb6ad274f60000033e0048"
}
```

### file.chown

状态：已实测通过，耗时 30.4ms

```json
{
  "sysNotify": "taskId",
  "taskId": "nfjL9t6pQQCB7ORMBBoNNg==",
  "reqid": "6ad274fb6ad274f60000033e0040"
}
```

### file.compress

状态：已实测通过，耗时 31.9ms

```json
{
  "sysNotify": "taskId",
  "taskId": "/Rfw68QGRMGCyPqZQLp5LA==",
  "reqid": "6ad274f86ad274f60000033e0034"
}
```

### file.cp

状态：已实测通过，耗时 21.0ms

```json
{
  "sysNotify": "taskId",
  "taskId": "Sf7JaEkGTGa/Dt88zTlGqw==",
  "reqid": "6ad274f76ad274f60000033e002e"
}
```

### file.download

状态：已实测通过，耗时 18.4ms

```json
{
  "download": [
    {
      "uri": "/download//vol1/1000/tmp/20260127_195353.jpg?t=1792782198&sign=REDACTED"
    }
  ],
  "result": "succ",
  "reqid": "6ad274f76ad274f60000033e0015"
}
```

### file.extract

状态：已实测通过，耗时 21.3ms

```json
{
  "sysNotify": "taskId",
  "taskId": "Wy7XtlIARHKoo1PRf3eXnA==",
  "reqid": "6ad274f86ad274f60000033e0038"
}
```

### file.fav.add

状态：已实测通过，耗时 46.4ms

```json
{
  "result": "succ",
  "reqid": "6ad274f76ad274f60000033e0029"
}
```

### file.fav.del

状态：已实测通过，耗时 48.2ms

```json
{
  "result": "succ",
  "reqid": "6ad274f76ad274f60000033e002b"
}
```

### file.fav.list

状态：已实测通过，耗时 15.9ms

```json
{
  "fav": [
    {
      "id": 5,
      "datetime": 1792177399,
      "path": "/vol1/1000/tmp/fnapi_filetest_20261017_030318",
      "uid": 1000,
      "mtim": 1792177399,
      "btim": 1792177399,
      "dir": 1
    },
    {
      "id": 1,
      "datetime": 1790023187,
      "path": "/vol3/1000/video/sample",
      "uid": 1000,
      "mtim": 1780122656,
      "btim": 1743079625,
      "dir": 1
    }
  ],
  "uver": 117436739026944,
  "result": "succ",
  "reqid": "6ad274f76ad274f60000033e002a"
}
```

### file.getAcl

状态：已实测通过，耗时 20.1ms

```json
{
  "aclType": "trimacl",
  "uver": 117436739026944,
  "result": "succ",
  "reqid": "6ad274fa6ad274f60000033e003b"
}
```

### file.ls

状态：已实测通过，耗时 32.0ms

```json
{
  "files": [
    {
      "name": "20260127_195353.jpg",
      "uid": 1000,
      "size": 1880200,
      "mtim": 1769517306,
      "btim": 1792167850
    }
  ],
  "uver": 117436739026944,
  "reqid": "6ad274f66ad274f60000033e0006"
}
```

### file.lsDir

状态：已实测通过，耗时 16.1ms

```json
{
  "uver": 117436739026944,
  "reqid": "6ad274f66ad274f60000033e0007",
  "result": "succ"
}
```

### file.mkdir

状态：已实测通过，耗时 26.8ms

```json
{
  "result": "succ",
  "reqid": "6ad274f76ad274f60000033e0022"
}
```

### file.mv

状态：已实测通过，耗时 24.0ms

```json
{
  "sysNotify": "taskId",
  "taskId": "rPc1LntjQAuJjBb9V5HLtA==",
  "reqid": "6ad274f86ad274f60000033e0032"
}
```

### file.prop

状态：已实测通过，耗时 29.8ms

```json
{
  "prop": [
    {
      "errno": 4100
    }
  ],
  "uver": 117436739026944,
  "result": "succ",
  "reqid": "6ad274f76ad274f60000033e000a"
}
```

### file.recent.add

状态：已实测通过，耗时 15.3ms

```json
{
  "result": "succ",
  "reqid": "6ad274f76ad274f60000033e002c"
}
```

### file.recent.del

状态：已实测通过，耗时 16.1ms

```json
{
  "result": "succ",
  "reqid": "6ad274f76ad274f60000033e002d"
}
```

### file.recent.list

状态：已实测通过，耗时 48.4ms

```json
{
  "recent": [
    {
      "id": 59,
      "datetime": 1792164201,
      "path": "/vol4/1000/code/fnnas-api/interfaces.html",
      "uid": 1000,
      "size": 1314636,
      "mtim": 1792163509,
      "btim": 1792164181
    },
    {
      "id": 58,
      "datetime": 1791862849,
      "path": "/vol3/1000/document/sample/sample/sample.pdf",
      "uid": 1000,
      "size": 105106884,
      "mtim": 1791860269,
      "btim": 1791860269
    },
    {
      "id": 57,
      "datetime": 1791860956,
      "path": "/vol3/1000/document/sample/sample/sample.pdf",
      "uid": 1000,
      "size": 312766166,
      "mtim": 1791860404,
      "btim": 1791860400
    },
    {
      "id": 50,
      "datetime": 1791858346,
      "path": "/vol3/1000/document/sample/sample/sample.pdf",
      "uid": 1000,
      "size": 393805066,
      "mtim": 1767369206,
      "btim": 1771685316
    },
    {
      "id": 48,
      "datetime": 1791807578,
      "path": "/vol1/@appshare/xunlei/downloads/漫画后续/187.pdf",
      "uid": 975,
      "size": 6585459,
      "mtim": 1791806132,
      "btim": 1791806090
    },
    {
      "id": 47,
      "datetime": 1791807373
... (截断)
```

### file.rename

状态：已实测通过，耗时 32.0ms

```json
{
  "result": "succ",
  "reqid": "6ad274f86ad274f60000033e0030"
}
```

### file.rm

状态：已实测通过，耗时 23.4ms

```json
{
  "sysNotify": "taskId",
  "taskId": "BFq02xqcS6qymQtD51GIeg==",
  "reqid": "6ad275076ad274f60000033e0062"
}
```

### file.setAcl2

状态：已实测通过，耗时 27.7ms

```json
{
  "sysNotify": "taskId",
  "taskId": "s3j3uboXSqWoFTfA8doe1Q==",
  "reqid": "6ad274fa6ad274f60000033e003c"
}
```

### file.share.info

状态：已实测通过，耗时 71.1ms

```json
{
  "uver": 117436739026944,
  "result": "succ",
  "reqid": "6ad255766ad25576000003050009"
}
```

### file.share.list

状态：已实测通过，耗时 83.3ms

```json
{
  "result": "succ",
  "reqid": "6ad255766ad25576000003050006"
}
```

### file.share.listOthers

状态：已实测通过，耗时 63.1ms

```json
{
  "uver": 117436739026944,
  "result": "succ",
  "reqid": "6ad255766ad25576000003050007"
}
```

### file.size

状态：已实测通过，耗时 14.9ms

```json
{
  "size": 38,
  "result": "succ",
  "reqid": "6ad274f76ad274f60000033e0013"
}
```

### file.team.lsDir

状态：已实测通过，耗时 32.1ms

```json
{
  "uver": 117436739026944,
  "reqid": "6ad274f76ad274f60000033e001b",
  "result": "succ"
}
```

### file.team.trash.list

状态：已实测存在（缺参数）（errno=8192），耗时 20.6ms

```json
{
  "errno": 8192,
  "result": "fail",
  "reqid": "6ad238546ad23836000002da0099"
}
```

### file.team.trash.listTrashbin

状态：已实测通过，耗时 20.1ms

```json
{
  "uver": 117436739026944,
  "reqid": "6ad238546ad23836000002da009a",
  "result": "succ"
}
```

### file.trash.list

状态：已实测通过，耗时 32.2ms

```json
{
  "files": [
    {
      "name": "renamed.jpg",
      "uid": 1000,
      "size": 1880200,
      "mtim": 1769517306,
      "btim": 1792177399
    }
  ],
  "uver": 117436739026944,
  "reqid": "6ad274fb6ad274f60000033e004d"
}
```

### file.trimacl.conv

状态：已实测存在（缺参数）（errno=8192），耗时 16.1ms

```json
{
  "errno": 8192,
  "result": "fail",
  "reqid": "6ad274fb6ad274f60000033e0044"
}
```

### file.trimacl.conv.report

状态：已实测存在（缺参数）（errno=8192），耗时 19.1ms

```json
{
  "errno": 8192,
  "result": "fail",
  "reqid": "6ad274fb6ad274f60000033e0047"
}
```

### file.usage

状态：已实测通过，耗时 32.0ms

```json
{
  "sysNotify": "taskId",
  "taskId": "uKif6a+9TJij6dHwUCA6GQ==",
  "reqid": "6ad274f76ad274f60000033e0014"
}
```
