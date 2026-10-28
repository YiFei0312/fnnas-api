# appcgi.tfa

> 自动生成（`python tools/gen_api.py`），共 20 个接口。
> 调用示例：`await client.api.appcgi.tfa.security_v1_device_list(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `security_v1_device_list` | `appcgi.tfa.security.v1.device.list` | 已实测存在（业务错误码） | ✅ | - | data |
| `security_v1_device_trust` | `appcgi.tfa.security.v1.device.trust` | 未实测（写接口） | ⚠️ | - | - |
| `security_v1_device_untrust` | `appcgi.tfa.security.v1.device.untrust` | 未实测（写接口） | ⚠️ | - | - |
| `security_v1_email_bind` | `appcgi.tfa.security.v1.email.bind` | 未实测（写接口） | ⚠️ | - | - |
| `security_v1_email_bind_before_verify` | `appcgi.tfa.security.v1.email.bindBeforeVerify` | 未实测（写接口） | ⚠️ | - | - |
| `security_v1_email_send_bind_code` | `appcgi.tfa.security.v1.email.sendBindCode` | 未实测（写接口） | ⚠️ | - | - |
| `security_v1_login_reset_password_send_email` | `appcgi.tfa.security.v1.login.resetPasswordSendEmail` | 未实测（写接口） | ⚠️ | - | - |
| `security_v1_login_reset_password_verify` | `appcgi.tfa.security.v1.login.resetPasswordVerify` | 未实测（写接口） | ⚠️ | - | - |
| `security_v1_login_send_email_code` | `appcgi.tfa.security.v1.login.sendEmailCode` | 未实测（写接口） | ⚠️ | - | - |
| `security_v1_login_totp_verify` | `appcgi.tfa.security.v1.login.totpVerify` | 未实测（写接口） | ⚠️ | - | - |
| `security_v1_me_get_config` | `appcgi.tfa.security.v1.me.getConfig` | 已实测通过 | ✅ | - | data |
| `security_v1_me_twofa_bind` | `appcgi.tfa.security.v1.me.twofa.bind` | 未实测（写接口） | ⚠️ | - | - |
| `security_v1_me_twofa_bind_before_verify` | `appcgi.tfa.security.v1.me.twofa.bindBeforeVerify` | 未实测（写接口） | ⚠️ | - | - |
| `security_v1_me_twofa_disable` | `appcgi.tfa.security.v1.me.twofa.disable` | 未实测（写接口） | ⚠️ | - | - |
| `security_v1_me_twofa_totp_verify` | `appcgi.tfa.security.v1.me.twofa.totpVerify` | 未实测（写接口） | ⚠️ | - | - |
| `security_v1_twofa_disable` | `appcgi.tfa.security.v1.twofa.disable` | 未实测（写接口） | ⚠️ | - | - |
| `security_v1_twofa_enable` | `appcgi.tfa.security.v1.twofa.enable` | 未实测（写接口） | ⚠️ | - | - |
| `security_v1_twofa_get_config` | `appcgi.tfa.security.v1.twofa.getConfig` | 已实测通过 | ✅ | - | data |
| `security_v1_user_disable_twofa` | `appcgi.tfa.security.v1.user.disableTwofa` | 未实测（写接口） | ⚠️ | - | - |
| `security_v1_user_get_twofa_config` | `appcgi.tfa.security.v1.user.getTwofaConfig` | 已实测存在（业务错误码） | ✅ | - | data |

## 实测样例

### appcgi.tfa.security.v1.device.list

状态：已实测存在（业务错误码）（errno=102550007），耗时 20.2ms

```json
{
  "result": "fail",
  "errno": 102550007,
  "reqid": "6ad238516ad23836000002da0086",
  "data": null
}
```

### appcgi.tfa.security.v1.me.getConfig

状态：已实测通过，耗时 4.4ms

```json
{
  "result": "succ",
  "reqid": "6ad238516ad23836000002da0087",
  "data": {
    "isTwofaEnforced": false,
    "isBindTwofaSecret": false,
    "isBindSecureEmail": false,
    "secureEmail": "",
    "twofaActiveAt": ""
  }
}
```

### appcgi.tfa.security.v1.twofa.getConfig

状态：已实测通过，耗时 3.9ms

```json
{
  "result": "succ",
  "reqid": "6ad238516ad23836000002da0088",
  "data": {
    "enabled": 0,
    "bindType": "",
    "target": []
  }
}
```

### appcgi.tfa.security.v1.user.getTwofaConfig

状态：已实测存在（业务错误码）（errno=102550007），耗时 5.0ms

```json
{
  "result": "fail",
  "errno": 102550007,
  "reqid": "6ad238526ad23836000002da0089",
  "data": null
}
```
