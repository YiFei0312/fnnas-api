# user

> 自动生成（`python tools/gen_api.py`），共 33 个接口。
> 调用示例：`await client.api.user.user_2fa_login_verify(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `user_2fa_login_verify` | `user.2fa.loginVerify` | 未实测（写接口） | ⚠️ | - | - |
| `user_2fa_reset_password` | `user.2fa.resetPassword` | 未实测（写接口） | ⚠️ | - | - |
| `active` | `user.active` | 已实测通过 | ✅ | - | - |
| `add` | `user.add` | 未实测（写接口） | ⚠️ | - | - |
| `add1000` | `user.add1000` | 未实测（写接口） | ⚠️ | - | - |
| `auth` | `user.auth` | 未实测（写接口） | ⚠️ | - | - |
| `auth_token` | `user.authToken` | 未实测（写接口） | ⚠️ | - | - |
| `change_password` | `user.changePassword` | 未实测（写接口） | ⚠️ | user, password, newPassword, removeToken | - |
| `check_new_group` | `user.checkNewGroup` | 已实测存在（缺参数） | ✅ | group | - |
| `check_new_user` | `user.checkNewUser` | 已实测存在（缺参数） | ✅ | user | - |
| `del_` | `user.del` | 未实测（写接口） | ⚠️ | user | - |
| `group_add` | `user.groupAdd` | 未实测（写接口） | ⚠️ | - | - |
| `group_add_users` | `user.groupAddUsers` | 未实测（写接口） | ⚠️ | group, users | - |
| `group_del` | `user.groupDel` | 未实测（写接口） | ⚠️ | - | - |
| `group_del_users` | `user.groupDelUsers` | 未实测（写接口） | ⚠️ | group, users | - |
| `group_info` | `user.groupInfo` | 未实测（写接口） | ⚠️ | - | - |
| `group_list` | `user.groupList` | 未实测（写接口） | ⚠️ | - | - |
| `group_mod` | `user.groupMod` | 未实测（写接口） | ⚠️ | - | - |
| `group_set_users` | `user.groupSetUsers` | 未实测（写接口） | ⚠️ | - | - |
| `group_users` | `user.groupUsers` | 已实测通过 | ✅ | - | groups, uver |
| `info` | `user.info` | 已实测通过 | ✅ | user | userInfo |
| `is_admin` | `user.isAdmin` | 已实测通过 | ✅ | - | admin |
| `kick_login_device` | `user.kickLoginDevice` | 未实测（写接口） | ⚠️ | - | - |
| `list` | `user.list` | 已实测通过 | ✅ | - | users, uver |
| `list_login_device` | `user.listLoginDevice` | 已实测通过 | ✅ | - | loginDevice |
| `list_ug` | `user.listUG` | 已实测通过 | ✅ | - | uver |
| `login` | `user.login` | 未实测（写接口） | ⚠️ | - | - |
| `login_intl` | `user.loginIntl` | 未实测（写接口） | ⚠️ | - | - |
| `logout` | `user.logout` | 未实测（写接口） | ⚠️ | - | - |
| `mod` | `user.mod` | 未实测（写接口） | ⚠️ | user, comment, newName, disableUser, allowSSH | - |
| `set_admin` | `user.setAdmin` | 未实测（写接口） | ⚠️ | user, setAdmin | - |
| `token_login` | `user.tokenLogin` | 未实测（写接口） | ⚠️ | - | - |
| `unfreeze` | `user.unfreeze` | 未实测（写接口） | ⚠️ | - | - |

## 实测样例

### user.active

状态：已实测通过，耗时 1.5ms

```json
{
  "result": "succ",
  "reqid": "6ad238596ad23836000002da00bc"
}
```

### user.checkNewGroup

状态：已实测存在（缺参数）（errno=8192），耗时 3.8ms

```json
{
  "errno": 8192,
  "result": "fail",
  "reqid": "6ad238596ad23836000002da00bd"
}
```

### user.checkNewUser

状态：已实测存在（缺参数）（errno=8192），耗时 0.4ms

```json
{
  "errno": 8192,
  "result": "fail",
  "reqid": "6ad238596ad23836000002da00be"
}
```

### user.groupUsers

状态：已实测通过，耗时 4.6ms

```json
{
  "uver": 117436739026944,
  "groups": [
    {
      "group": "Administrators",
      "gid": 1000,
      "users": [
        1000
      ]
    },
    {
      "group": "Users",
      "gid": 1001
    }
  ],
  "result": "succ",
  "reqid": "6ad238596ad23836000002da00bf"
}
```

### user.info

状态：已实测通过，耗时 4.5ms

```json
{
  "userInfo": {
    "user": "demo-user",
    "uid": 1000,
    "comment": "",
    "email": "",
    "mobile": "",
    "disableChangePassword": false,
    "lastChange": 20708,
    "disableUser": 0,
    "admin": true,
    "allowSSH": true,
    "groups": [
      "Administrators",
      "Users"
    ]
  },
  "result": "succ",
  "reqid": "6ad238596ad23836000002da00c0"
}
```

### user.isAdmin

状态：已实测通过，耗时 3.4ms

```json
{
  "admin": true,
  "result": "succ",
  "reqid": "6ad238596ad23836000002da00c1"
}
```

### user.list

状态：已实测通过，耗时 0.4ms

```json
{
  "uver": 117436739026944,
  "users": [
    {
      "user": "demo-user",
      "uid": 1000,
      "admin": true,
      "allowSSH": true
    }
  ],
  "result": "succ",
  "reqid": "6ad238596ad23836000002da00c2"
}
```

### user.listLoginDevice

状态：已实测通过，耗时 19.8ms

```json
{
  "loginDevice": [
    {
      "tid": "IRCL4509rIfjUcTIjsaZO3vHMeDVYVEz1x3UiFgvnNI=",
      "deviceName": "Windows-Google Chrome",
      "deviceType": "Browser",
      "loginTime": 1792159492
    },
    {
      "tid": "A5BkDa+Tt512qSsFhsaZO/bhx2eSG3/glwoCR/eRTdY=",
      "deviceName": "Windows-Google Chrome",
      "deviceType": "Browser",
      "loginTime": 1792160735
    },
    {
      "tid": "AdlPbCsVEvw8DPtgkcaZO0u2KGRz8/lx0hiAPErH2Ss=",
      "deviceName": "Windows-Google Chrome",
      "deviceType": "Browser",
      "loginTime": 1792159376
    },
    {
      "tid": "HXP4RJSBomjGWeTAi8aZO+pGO/ek4RD/GwaS0U0usWk=",
      "deviceName": "Windows-Google Chrome",
      "deviceType": "Browser",
      "loginTime": 1792159934
    },
    {
      "tid": "ERIjSQDKe77UyxkpgsaZO+X+W49zJbfANRvZAF4PTGA=",
      "deviceName": "Windows-Google Chrome",
      "deviceType": "Browser",
      "loginTime": 1792161846,
      "activeTime": 1792161881,
      "currentDevice": true
    },
    {
      "tid": "fGCW+CoLDRdgShzEisaZO3axTZ0i6AVv5lY77b59UQk=",
      "deviceName": "Windows-Google Chrome",
      "deviceType": "Browser",
      "loginTime": 1792160080
    },
    {
      "tid": "fRU061e4v4K51eEtls
... (截断)
```

### user.listUG

状态：已实测通过，耗时 0.4ms

```json
{
  "uver": 117436739026944,
  "result": "succ",
  "reqid": "6ad2385a6ad23836000002da00c4"
}
```
