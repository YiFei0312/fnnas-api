# appcgi.share

> 自动生成（`python tools/gen_api.py`），共 23 个接口。
> 调用示例：`await client.api.appcgi.share.check_port(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `check_port` | `appcgi.share.check.port` | 未实测（写接口） | ⚠️ | - | - |
| `dlna_opt` | `appcgi.share.dlna.opt` | 已实测通过 | ✅ | - | data, req, rev |
| `dlna_set` | `appcgi.share.dlna.set` | 未实测（写接口） | ⚠️ | - | - |
| `dlna_share_opt` | `appcgi.share.dlna.share.opt` | 已实测通过 | ✅ | - | data, req, rev |
| `dlna_share_set` | `appcgi.share.dlna.share.set` | 未实测（写接口） | ⚠️ | - | - |
| `ftp_opt` | `appcgi.share.ftp.opt` | 已实测通过 | ✅ | - | data, req, rev |
| `ftp_set` | `appcgi.share.ftp.set` | 未实测（写接口） | ⚠️ | - | - |
| `ftp_share_opt` | `appcgi.share.ftp.share.opt` | 已实测通过 | ✅ | - | data, req, rev |
| `ftp_share_set` | `appcgi.share.ftp.share.set` | 未实测（写接口） | ⚠️ | - | - |
| `nfs_opt` | `appcgi.share.nfs.opt` | 已实测通过 | ✅ | - | data, req, rev |
| `nfs_set` | `appcgi.share.nfs.set` | 未实测（写接口） | ⚠️ | - | - |
| `nfs_share_opt` | `appcgi.share.nfs.share.opt` | 已实测通过 | ✅ | - | data, req, rev |
| `nfs_share_set` | `appcgi.share.nfs.share.set` | 未实测（写接口） | ⚠️ | - | - |
| `smb_opt` | `appcgi.share.smb.opt` | 已实测通过 | ✅ | - | data, req, rev |
| `smb_set` | `appcgi.share.smb.set` | 未实测（写接口） | ⚠️ | - | - |
| `smb_share_opt` | `appcgi.share.smb.share.opt` | 已实测通过 | ✅ | - | data, req, rev |
| `smb_share_set` | `appcgi.share.smb.share.set` | 未实测（写接口） | ⚠️ | - | - |
| `smb_tm_set` | `appcgi.share.smb.tm.set` | 未实测（写接口） | ⚠️ | - | - |
| `team_allow_share` | `appcgi.share.team.allowShare` | 已实测存在（业务错误码） | ✅ | - | req, rev |
| `webdav_opt` | `appcgi.share.webdav.opt` | 已实测通过 | ✅ | - | data, req, rev |
| `webdav_set` | `appcgi.share.webdav.set` | 未实测（写接口） | ⚠️ | - | - |
| `webdav_share_opt` | `appcgi.share.webdav.share.opt` | 已实测通过 | ✅ | - | data, req, rev |
| `webdav_share_set` | `appcgi.share.webdav.share.set` | 未实测（写接口） | ⚠️ | - | - |

## 实测样例

### appcgi.share.dlna.opt

状态：已实测通过，耗时 33.0ms

```json
{
  "data": {
    "dlnaEnable": true,
    "port": 8200
  },
  "reqid": "6ad238446ad23836000002da0061",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.share.dlna.opt"
}
```

### appcgi.share.dlna.share.opt

状态：已实测通过，耗时 0.4ms

```json
{
  "data": {
    "path": [],
    "count": 0,
    "sharesCount": {
      "user": 0,
      "others": 0,
      "mounted": 0,
      "external": 0,
      "appshare": 0,
      "team": 0
    },
    "extended": {
      "mounted": [],
      "external": [],
      "appShare": [],
      "team": []
    }
  },
  "reqid": "6ad238456ad23836000002da0062",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.share.dlna.share.opt"
}
```

### appcgi.share.ftp.opt

状态：已实测通过，耗时 3.8ms

```json
{
  "data": {
    "ftpEnable": true,
    "mode": 2,
    "ipv4Addr": "192.168.1.10",
    "option": {
      "port": 21,
      "timeout": 900,
      "passiveLow": 55536,
      "passiveHigh": 55899,
      "securityPolicy": 3,
      "ftp": true,
      "ssl": 3,
      "passiveIp": ""
    }
  },
  "reqid": "6ad238456ad23836000002da0063",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.share.ftp.opt"
}
```

### appcgi.share.ftp.share.opt

状态：已实测通过，耗时 4.6ms

```json
{
  "data": {
    "mode": 2,
    "extended": {
      "teamShareMode": 2,
      "mounted": [],
      "external": [],
      "appShare": [],
      "team": []
    },
    "path": [],
    "count": 0,
    "sharesCount": {
      "user": 0,
      "others": 0,
      "mounted": 0,
      "external": 0,
      "appshare": 0,
      "team": 0
    }
  },
  "reqid": "6ad238456ad23836000002da0064",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.share.ftp.share.opt"
}
```

### appcgi.share.nfs.opt

状态：已实测通过，耗时 3.5ms

```json
{
  "data": {
    "nfsEnable": true,
    "mode": 1,
    "ipv4Addr": "192.168.1.10",
    "path": "/fs/1000/nfs"
  },
  "reqid": "6ad238456ad23836000002da0065",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.share.nfs.opt"
}
```

### appcgi.share.nfs.share.opt

状态：已实测通过，耗时 67.2ms

```json
{
  "data": {
    "mode": 1,
    "extended": {
      "teamShareMode": 1,
      "mounted": [],
      "external": [],
      "appShare": [],
      "team": []
    },
    "path": [],
    "count": 0,
    "sharesCount": {
      "user": 0,
      "others": 0,
      "mounted": 0,
      "external": 0,
      "appshare": 0,
      "team": 0
    }
  },
  "reqid": "6ad238456ad23836000002da0066",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.share.nfs.share.opt"
}
```

### appcgi.share.smb.opt

状态：已实测通过，耗时 4.1ms

```json
{
  "data": {
    "smbEnable": true,
    "wsddEnable": true,
    "mode": 2,
    "ipv4Addr": "192.168.1.10",
    "svcPort": 445,
    "mount": "demoNAS",
    "option": {
      "workGroup": "",
      "oplocks": true,
      "ntlmv1": false,
      "serverSigning": 1,
      "transportEncryption": 1,
      "supportSmb1": false,
      "enableFruit": false,
      "enableDirSort": false,
      "enableVoteFile": true,
      "voteFiles": "/._*/.DS_Store/",
      "deleteVoteFiles": false,
      "wildcardSearchCache": false,
      "winsIP": "",
      "disableMultiConn": false,
      "enableMultiChannel": true,
      "aioWrite": 2
    },
    "timeMachine": {
      "enable": false,
      "vol": 0,
      "quota": 10737418240,
      "folder": "",
      "status": -1
    }
  },
  "reqid": "6ad238456ad23836000002da0067",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.share.smb.opt"
}
```

### appcgi.share.smb.share.opt

状态：已实测通过，耗时 13.3ms

```json
{
  "data": {
    "mode": 2,
    "extended": {
      "teamShareMode": 2,
      "mounted": [],
      "external": [],
      "appShare": [],
      "team": []
    },
    "path": [],
    "count": 0,
    "sharesCount": {
      "user": 0,
      "others": 0,
      "mounted": 0,
      "external": 0,
      "appshare": 0,
      "team": 0
    }
  },
  "reqid": "6ad238456ad23836000002da0068",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.share.smb.share.opt"
}
```

### appcgi.share.team.allowShare

状态：已实测存在（业务错误码）（errno=100000004），耗时 4.4ms

```json
{
  "errno": 100000004,
  "reqid": "6ad238456ad23836000002da0069",
  "result": "fail",
  "rev": "0.1",
  "req": "appcgi.share.team.allowShare"
}
```

### appcgi.share.webdav.opt

状态：已实测通过，耗时 7.2ms

```json
{
  "data": {
    "webdavEnable": false,
    "mode": 2,
    "httpAddr": "http://192.168.1.10:5005",
    "httpsAddr": "https://192.168.1.10:5006",
    "ipv4Addr": "192.168.1.10",
    "option": {
      "http": true,
      "https": true,
      "httpPort": 5005,
      "httpsPort": 5006,
      "infinity": true
    }
  },
  "reqid": "6ad238466ad23836000002da006a",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.share.webdav.opt"
}
```

### appcgi.share.webdav.share.opt

状态：已实测通过，耗时 3.9ms

```json
{
  "data": {
    "mode": 2,
    "extended": {
      "teamShareMode": 2,
      "mounted": [],
      "external": [],
      "appShare": [],
      "team": []
    },
    "path": [],
    "count": 0,
    "sharesCount": {
      "user": 0,
      "others": 0,
      "mounted": 0,
      "external": 0,
      "appshare": 0,
      "team": 0
    }
  },
  "reqid": "6ad238466ad23836000002da006b",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.share.webdav.share.opt"
}
```
