# appcgi.security

> 自动生成（`python tools/gen_api.py`），共 8 个接口。
> 调用示例：`await client.api.appcgi.security.firewall_getting(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `firewall_getting` | `appcgi.security.firewall.getting` | 已实测通过 | ✅ | - | data, req, rev |
| `firewall_iflist` | `appcgi.security.firewall.iflist` | 未实测（写接口） | ⚠️ | - | - |
| `firewall_ifstat` | `appcgi.security.firewall.ifstat` | 未实测（写接口） | ⚠️ | - | - |
| `firewall_servlist` | `appcgi.security.firewall.servlist` | 未实测（写接口） | ⚠️ | - | - |
| `firewall_setting` | `appcgi.security.firewall.setting` | 未实测（写接口） | ⚠️ | - | - |
| `flowaudit_traffic` | `appcgi.security.flowaudit.traffic` | 未实测（写接口） | ⚠️ | - | - |
| `safe_code_getting` | `appcgi.security.safeCode.getting` | 已实测通过 | ✅ | - | data, req, rev |
| `safe_code_setting` | `appcgi.security.safeCode.setting` | 未实测（写接口） | ⚠️ | - | - |

## 实测样例

### appcgi.security.firewall.getting

状态：已实测通过，耗时 32.7ms

```json
{
  "data": [
    {
      "profile": "default",
      "enable": false,
      "txfallback": true,
      "rxfallback": true,
      "workmode": "auto",
      "allowlan": true,
      "rules": [
        {
          "ifname": "ALL",
          "flowdir": 1,
          "ports": {
            "type": 0,
            "ranges": {
              "ports": [
                21,
                53,
                67,
                68,
                111,
                123,
                137,
                138,
                139,
                445,
                546,
                547,
                1900,
                2049,
                3478,
                3702,
                5005,
                5006,
                5353,
                5355,
                5666,
                5667,
                7200,
                7201,
                7202,
                7203,
                7204,
                7205,
                7206,
                7207,
                7208,
                7209,
                7210,
                9024,
                41750,
                42423
              ],
              "range": {
                "from": 0,
          
... (截断)
```

### appcgi.security.safeCode.getting

状态：已实测通过，耗时 3.9ms

```json
{
  "data": {
    "enable": false,
    "configured": false
  },
  "reqid": "6ad238446ad23836000002da0060",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.security.safeCode.getting"
}
```
