# appcgi.network

> 自动生成（`python tools/gen_api.py`），共 39 个接口。
> 调用示例：`await client.api.appcgi.network.gen_info(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `gen_info` | `appcgi.network.gen.info` | 已实测存在（业务错误码） | ✅ | - | req, rev |
| `gen_set` | `appcgi.network.gen.set` | 未实测（写接口） | ⚠️ | - | - |
| `gw_getting` | `appcgi.network.gw.getting` | 已实测通过 | ✅ | - | data, req, rev |
| `gw_setting` | `appcgi.network.gw.setting` | 未实测（写接口） | ⚠️ | data | - |
| `hostname` | `appcgi.network.hostname` | 未实测（写接口） | ⚠️ | - | - |
| `net_add` | `appcgi.network.net.add` | 未实测（写接口） | ⚠️ | - | - |
| `net_arping` | `appcgi.network.net.arping` | 未实测（写接口） | ⚠️ | - | - |
| `net_bridge` | `appcgi.network.net.bridge` | 未实测（写接口） | ⚠️ | - | - |
| `net_conn` | `appcgi.network.net.conn` | 未实测（写接口） | ⚠️ | - | - |
| `net_del` | `appcgi.network.net.del` | 未实测（写接口） | ⚠️ | - | - |
| `net_detect` | `appcgi.network.net.detect` | 未实测（写接口） | ⚠️ | - | - |
| `net_disc` | `appcgi.network.net.disc` | 未实测（写接口） | ⚠️ | - | - |
| `net_get_multi_gw_status` | `appcgi.network.net.getMultiGWStatus` | 已实测通过 | ✅ | - | data, req, rev |
| `net_get_nic_performance_mode` | `appcgi.network.net.getNicPerformanceMode` | 已实测通过 | ✅ | - | data, req, rev |
| `net_info` | `appcgi.network.net.info` | 已实测存在（缺参数） | ✅ | - | req, rev |
| `net_list` | `appcgi.network.net.list` | 已实测通过 | ✅ | - | data, req, rev |
| `net_reset` | `appcgi.network.net.reset` | 未实测（写接口） | ⚠️ | - | - |
| `net_set` | `appcgi.network.net.set` | 未实测（写接口） | ⚠️ | - | - |
| `net_set_multi_gw` | `appcgi.network.net.setMultiGW` | 未实测（写接口） | ⚠️ | - | - |
| `net_set_nic_performance_mode` | `appcgi.network.net.setNicPerformanceMode` | 未实测（写接口） | ⚠️ | - | - |
| `net_state` | `appcgi.network.net.state` | 已实测存在（缺参数） | ✅ | - | req, rev |
| `route_list` | `appcgi.network.route.list` | 已实测存在（业务错误码） | ✅ | - | req, rev |
| `ssh_set` | `appcgi.network.ssh.set` | 未实测（写接口） | ⚠️ | - | - |
| `ssh_status` | `appcgi.network.ssh.status` | 已实测通过 | ✅ | - | data, req, rev |
| `ssh_switch` | `appcgi.network.ssh.switch` | 未实测（写接口） | ⚠️ | - | - |
| `static_add` | `appcgi.network.static.add` | 未实测（写接口） | ⚠️ | - | - |
| `static_del` | `appcgi.network.static.del` | 未实测（写接口） | ⚠️ | - | - |
| `static_list` | `appcgi.network.static.list` | 已实测存在（业务错误码） | ✅ | - | req, rev |
| `static_set` | `appcgi.network.static.set` | 未实测（写接口） | ⚠️ | - | - |
| `wifi_ap_list` | `appcgi.network.wifi.apList` | 未实测（写接口） | ⚠️ | - | - |
| `wifi_close` | `appcgi.network.wifi.close` | 未实测（写接口） | ⚠️ | - | - |
| `wifi_connect_hidden_ap` | `appcgi.network.wifi.connectHiddenAP` | 未实测（写接口） | ⚠️ | - | - |
| `wifi_connect_known_ap` | `appcgi.network.wifi.connectKnownAP` | 未实测（写接口） | ⚠️ | - | - |
| `wifi_connect_unknown_ap` | `appcgi.network.wifi.connectUnknownAP` | 未实测（写接口） | ⚠️ | - | - |
| `wifi_connected_ap` | `appcgi.network.wifi.connectedAP` | 未实测（写接口） | ⚠️ | - | - |
| `wifi_get_known_ap_info` | `appcgi.network.wifi.getKnownAPInfo` | 已实测存在（缺参数） | ✅ | - | req, rev |
| `wifi_ignore_known_ap` | `appcgi.network.wifi.ignoreKnownAP` | 未实测（写接口） | ⚠️ | - | - |
| `wifi_open` | `appcgi.network.wifi.open` | 未实测（写接口） | ⚠️ | - | - |
| `wifi_set_known_ap_info` | `appcgi.network.wifi.setKnownAPInfo` | 未实测（写接口） | ⚠️ | - | - |

## 实测样例

### appcgi.network.gen.info

状态：已实测存在（业务错误码）（errno=100000004），耗时 0.6ms

```json
{
  "errno": 100000004,
  "reqid": "6ad2383e6ad23836000002da0033",
  "result": "fail",
  "rev": "0.1",
  "req": "appcgi.network.gen.info"
}
```

### appcgi.network.gw.getting

状态：已实测通过，耗时 4.5ms

```json
{
  "data": {
    "schema": {
      "http": {
        "port": 5666
      },
      "https": {
        "port": 5667
      }
    },
    "force_https": false,
    "redirect": true
  },
  "reqid": "6ad2383e6ad23836000002da0034",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.network.gw.getting"
}
```

### appcgi.network.net.getMultiGWStatus

状态：已实测通过，耗时 5.7ms

```json
{
  "data": {
    "multiGwStatus": false
  },
  "reqid": "6ad2383f6ad23836000002da0035",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.network.net.getMultiGWStatus"
}
```

### appcgi.network.net.getNicPerformanceMode

状态：已实测通过，耗时 23.6ms

```json
{
  "data": {
    "nicPerfModeEnable": true
  },
  "reqid": "6ad2383f6ad23836000002da0036",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.network.net.getNicPerformanceMode"
}
```

### appcgi.network.net.info

状态：已实测存在（缺参数）（errno=100000002），耗时 5.6ms

```json
{
  "errno": 100000002,
  "reqid": "6ad2383f6ad23836000002da0037",
  "result": "fail",
  "rev": "0.1",
  "req": "appcgi.network.net.info"
}
```

### appcgi.network.net.list

状态：已实测通过，耗时 3.4ms

```json
{
  "data": {
    "net": {
      "ifs": [
        {
          "name": "0e04c6800db-ovs",
          "index": 1,
          "ifType": 0,
          "enable": true,
          "running": true,
          "onlink": true,
          "state": 100,
          "duplex": true,
          "speed": 1000,
          "mtu": 1500,
          "hwAddr": "00:11:22:33:44:55",
          "isOvsPort": true,
          "wireless": false,
          "ipv4Dhcp": false,
          "ipv4Mode": "manual",
          "ipv4Broad": "192.168.1.255",
          "ipv4Mask": "255.255.255.0",
          "ipv4Gateway": "192.168.1.1",
          "ipv4Dns": "192.168.1.1",
          "ipv4": [
            "192.168.1.11"
          ],
          "ipv4Addr": "192.168.1.11",
          "ipv6Mode": "auto",
          "ipv6Gateway": "fe80::2e0:4cff:fe68:7255",
          "ipv6Dns": "fd05:92df:7941::1",
          "ipv6": [
            {
              "addr": "2001:db8::1",
              "prefixLen": 64,
              "scope": "global"
            },
            {
              "addr": "2001:db8::1",
              "prefixLen": 64,
              "scope": "global"
            },
            
... (截断)
```

### appcgi.network.net.state

状态：已实测存在（缺参数）（errno=100000002），耗时 16.8ms

```json
{
  "errno": 100000002,
  "reqid": "6ad2383f6ad23836000002da0039",
  "result": "fail",
  "rev": "0.1",
  "req": "appcgi.network.net.state"
}
```

### appcgi.network.route.list

状态：已实测存在（业务错误码）（errno=100000004），耗时 0.4ms

```json
{
  "errno": 100000004,
  "reqid": "6ad2383f6ad23836000002da003a",
  "result": "fail",
  "rev": "0.1",
  "req": "appcgi.network.route.list"
}
```

### appcgi.network.ssh.status

状态：已实测通过，耗时 36.5ms

```json
{
  "data": {
    "enable": true,
    "sftp": true,
    "port": 22
  },
  "reqid": "6ad2383f6ad23836000002da003b",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.network.ssh.status"
}
```

### appcgi.network.static.list

状态：已实测存在（业务错误码）（errno=100000004），耗时 20.9ms

```json
{
  "errno": 100000004,
  "reqid": "6ad2383f6ad23836000002da003c",
  "result": "fail",
  "rev": "0.1",
  "req": "appcgi.network.static.list"
}
```

### appcgi.network.wifi.getKnownAPInfo

状态：已实测存在（缺参数）（errno=100000002），耗时 0.4ms

```json
{
  "errno": 100000002,
  "reqid": "6ad238406ad23836000002da003d",
  "result": "fail",
  "rev": "0.1",
  "req": "appcgi.network.wifi.getKnownAPInfo"
}
```
