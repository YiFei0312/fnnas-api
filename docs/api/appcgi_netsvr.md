# appcgi.netsvr

> 自动生成（`python tools/gen_api.py`），共 32 个接口。
> 调用示例：`await client.api.appcgi.netsvr.cert_apply(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `cert_apply` | `appcgi.netsvr.cert.apply` | 未实测（写接口） | ⚠️ | - | - |
| `cert_applystatus` | `appcgi.netsvr.cert.applystatus` | 未实测（写接口） | ⚠️ | - | - |
| `cert_export` | `appcgi.netsvr.cert.export` | 未实测（写接口） | ⚠️ | - | - |
| `cert_getuse` | `appcgi.netsvr.cert.getuse` | 已实测通过 | ✅ | - | data |
| `cert_list` | `appcgi.netsvr.cert.list` | 已实测通过 | ✅ | - | data |
| `cert_remove` | `appcgi.netsvr.cert.remove` | 未实测（写接口） | ⚠️ | - | - |
| `cert_renew` | `appcgi.netsvr.cert.renew` | 未实测（写接口） | ⚠️ | - | - |
| `cert_replace` | `appcgi.netsvr.cert.replace` | 未实测（写接口） | ⚠️ | - | - |
| `cert_setuse` | `appcgi.netsvr.cert.setuse` | 未实测（写接口） | ⚠️ | - | - |
| `cert_sysreset` | `appcgi.netsvr.cert.sysreset` | 未实测（写接口） | ⚠️ | - | - |
| `cert_upload` | `appcgi.netsvr.cert.upload` | 未实测（写接口） | ⚠️ | - | - |
| `conn_change` | `appcgi.netsvr.conn.change` | 未实测（写接口） | ⚠️ | - | - |
| `conn_create` | `appcgi.netsvr.conn.create` | 未实测（写接口） | ⚠️ | - | - |
| `conn_getconfig` | `appcgi.netsvr.conn.getconfig` | 已实测通过 | ✅ | - | data |
| `conn_open` | `appcgi.netsvr.conn.open` | 未实测（写接口） | ⚠️ | - | - |
| `conn_quit` | `appcgi.netsvr.conn.quit` | 未实测（写接口） | ⚠️ | - | - |
| `conn_setconfig` | `appcgi.netsvr.conn.setconfig` | 未实测（写接口） | ⚠️ | - | - |
| `conn_status` | `appcgi.netsvr.conn.status` | 已实测通过 | ✅ | - | data |
| `ddns_provider_list` | `appcgi.netsvr.ddns.provider.list` | 已实测通过 | ✅ | - | data |
| `ddns_record_create` | `appcgi.netsvr.ddns.record.create` | 未实测（写接口） | ⚠️ | - | - |
| `ddns_record_detail` | `appcgi.netsvr.ddns.record.detail` | 已实测存在（缺参数） | ✅ | - | data, errmsg |
| `ddns_record_list` | `appcgi.netsvr.ddns.record.list` | 已实测通过 | ✅ | - | data |
| `ddns_record_refresh` | `appcgi.netsvr.ddns.record.refresh` | 未实测（写接口） | ⚠️ | - | - |
| `ddns_record_remove` | `appcgi.netsvr.ddns.record.remove` | 未实测（写接口） | ⚠️ | - | - |
| `ddns_record_test` | `appcgi.netsvr.ddns.record.test` | 未实测（写接口） | ⚠️ | - | - |
| `ddns_record_update` | `appcgi.netsvr.ddns.record.update` | 未实测（写接口） | ⚠️ | - | - |
| `domain_list` | `appcgi.netsvr.domain.list` | 已实测通过 | ✅ | - | data |
| `domain_sharecheck` | `appcgi.netsvr.domain.sharecheck` | 未实测（写接口） | ⚠️ | - | - |
| `fnassistant_close` | `appcgi.netsvr.fnassistant.close` | 未实测（写接口） | ⚠️ | - | - |
| `fnassistant_info` | `appcgi.netsvr.fnassistant.info` | 已实测通过 | ✅ | - | data |
| `fnassistant_open` | `appcgi.netsvr.fnassistant.open` | 未实测（写接口） | ⚠️ | - | - |
| `network_list` | `appcgi.netsvr.network.list` | 已实测通过 | ✅ | - | data |

## 实测样例

### appcgi.netsvr.cert.getuse

状态：已实测通过，耗时 113.9ms

```json
{
  "result": "succ",
  "reqid": "6ad2383b6ad23836000002da0029",
  "data": {
    "ftps": {
      "id": 1,
      "domain": "fnOS"
    },
    "gateway": {
      "id": 1,
      "domain": "fnOS"
    },
    "webdav": {
      "id": 1,
      "domain": "fnOS"
    }
  }
}
```

### appcgi.netsvr.cert.list

状态：已实测通过，耗时 32.7ms

```json
{
  "result": "succ",
  "reqid": "6ad2383b6ad23836000002da002a",
  "data": [
    {
      "id": 1,
      "domain": "fnOS",
      "encryptType": "ECDSA",
      "issuedBy": "fnOS",
      "SAN": "fnOS",
      "status": "suc",
      "validFrom": 1789218931000,
      "validTo": 1797081331000,
      "desc": "系统自签名证书",
      "isDefault": 0,
      "source": "system",
      "renewal": 0
    }
  ]
}
```

### appcgi.netsvr.conn.getconfig

状态：已实测通过，耗时 6.0ms

```json
{
  "result": "succ",
  "reqid": "6ad2383c6ad23836000002da002b",
  "data": {
    "webdav": 0,
    "connectUsingPublicIp": 1
  }
}
```

### appcgi.netsvr.conn.status

状态：已实测通过，耗时 3.8ms

```json
{
  "result": "succ",
  "reqid": "6ad2383c6ad23836000002da002c",
  "data": {
    "status": "closed"
  }
}
```

### appcgi.netsvr.ddns.provider.list

状态：已实测通过，耗时 10.0ms

```json
{
  "result": "succ",
  "reqid": "6ad2383c6ad23836000002da002d",
  "data": [
    {
      "name": "tencentcloud",
      "alias": "腾讯云",
      "type": "BuildIn",
      "accessKeyAlias": "SecretID",
      "accessSecretAlias": "SecretKey",
      "ipv6Support": 1,
      "txtSupport": 1,
      "accessKeyRequired": true
    },
    {
      "name": "aliyun",
      "alias": "阿里云",
      "type": "BuildIn",
      "accessKeyAlias": "AccessKey",
      "accessSecretAlias": "SecretKey",
      "ipv6Support": 1,
      "txtSupport": 1,
      "accessKeyRequired": true
    },
    {
      "name": "huawei",
      "alias": "华为云",
      "type": "BuildIn",
      "accessKeyAlias": "AccessKey",
      "accessSecretAlias": "SecretKey",
      "ipv6Support": 1,
      "txtSupport": 1,
      "accessKeyRequired": true
    },
    {
      "name": "oraydns",
      "alias": "花生壳",
      "type": "BuildIn",
      "accessKeyAlias": "用户名",
      "accessSecretAlias": "密码",
      "ipv6Support": 0,
      "accessKeyRequired": true
    },
    {
      "name": "changeip",
      "alias": "ChangeIP.com",
      "type": "BuildIn",
      "accessKeyAlias": "邮箱",
      "accessSecretAlias": "密码",
      "ipv6Support": 0,
      "accessKeyRe
... (截断)
```

### appcgi.netsvr.ddns.record.detail

状态：已实测存在（缺参数）（errno=3000001），耗时 3.3ms

```json
{
  "result": "fail",
  "errno": 3000001,
  "reqid": "6ad2383c6ad23836000002da002e",
  "errmsg": "Invalid Params",
  "data": null
}
```

### appcgi.netsvr.ddns.record.list

状态：已实测通过，耗时 17.1ms

```json
{
  "result": "succ",
  "reqid": "6ad2383c6ad23836000002da002f",
  "data": {
    "list": [
      {
        "id": 1,
        "provider": "aliyun",
        "providerAlias": "阿里云",
        "domain": "example.com",
        "ipv4": "disabled",
        "ipv6": "auto",
        "ipv4Addr": "-",
        "source": "",
        "ipv6Addr": "2001:db8::1::f36",
        "status": "failed",
        "lastUpdateTime": 1792161679129,
        "updateInterval": 5,
        "lastUpdateError": "SDKError:\n   StatusCode: 400\n   Code: SignatureDoesNotMatch\n   Message: code: 400, Specified signature does not match our calculation. server StringToSign is [ACS3-HMAC-SHA256\n1ae2ef290e365c7189e14dbe725f0795dfbaf05576cc4095902b9703c49129da], se",
        "providerSupportTxt": 1
      },
      {
        "id": 2,
        "provider": "aliyun",
        "providerAlias": "阿里云",
        "domain": "6.example.com",
        "ipv4": "disabled",
        "ipv6": "auto",
        "ipv4Addr": "-",
        "source": "",
        "ipv6Addr": "2001:db8::1::f36",
        "status": "suc",
        "lastUpdateTime": 1792161680013,
        "updateInterval": 5,
        "providerSupportTxt": 1
      }
    ],
    "total": 2
 
... (截断)
```

### appcgi.netsvr.domain.list

状态：已实测通过，耗时 336.9ms

```json
{
  "result": "succ",
  "reqid": "6ad2383c6ad23836000002da0030",
  "data": [
    "fnos.net",
    "5ddd.com"
  ]
}
```

### appcgi.netsvr.fnassistant.info

状态：已实测通过，耗时 21.0ms

```json
{
  "result": "succ",
  "reqid": "6ad2383d6ad23836000002da0031",
  "data": {
    "isOpen": false,
    "deviceId": "",
    "deviceCode": "",
    "expireAt": "",
    "connectFailed": false
  }
}
```

### appcgi.netsvr.network.list

状态：已实测通过，耗时 1513.1ms

```json
{
  "result": "succ",
  "reqid": "6ad2383d6ad23836000002da0032",
  "data": [
    {
      "name": "auto",
      "index": 0,
      "ifType": 0,
      "ipv4Addr": "203.0.113.10",
      "ipv6Addr": "2001:db8::1::f36"
    },
    {
      "name": "0e04c6800db-ovs",
      "index": 1,
      "ifType": 0,
      "ipv4Addr": "192.168.1.11",
      "ipv6Addr": "2001:db8::1"
    },
    {
      "name": "enp8s0",
      "index": 2,
      "ifType": 0,
      "ipv4Addr": "192.168.1.10",
      "ipv6Addr": "2001:db8::1"
    }
  ]
}
```
