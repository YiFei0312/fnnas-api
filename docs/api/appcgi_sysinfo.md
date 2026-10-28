# appcgi.sysinfo

> 自动生成（`python tools/gen_api.py`），共 27 个接口。
> 调用示例：`await client.api.appcgi.sysinfo.add_power_plan(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `add_power_plan` | `appcgi.sysinfo.addPowerPlan` | 未实测（写接口） | ⚠️ | - | - |
| `delete_power_plan` | `appcgi.sysinfo.deletePowerPlan` | 未实测（写接口） | ⚠️ | - | - |
| `get_boot_on_power_flag` | `appcgi.sysinfo.getBootOnPowerFlag` | 已实测存在（业务错误码） | ✅ | - | req, rev |
| `get_fan_mode` | `appcgi.sysinfo.getFanMode` | 已实测通过 | ✅ | - | data, req, rev |
| `get_hardware_info` | `appcgi.sysinfo.getHardwareInfo` | 已实测通过 | ✅ | - | data, req, rev |
| `get_host_name` | `appcgi.sysinfo.getHostName` | 已实测通过 | ✅ | - | data, req, rev |
| `get_machine_id` | `appcgi.sysinfo.getMachineId` | 已实测通过 | ✅ | - | data, req, rev |
| `get_net_info` | `appcgi.sysinfo.getNetInfo` | 已实测存在（业务错误码） | ✅ | - | req, rev |
| `get_power_plan_status` | `appcgi.sysinfo.getPowerPlanStatus` | 已实测通过 | ✅ | - | data, req, rev |
| `get_reserved_partition` | `appcgi.sysinfo.getReservedPartition` | 已实测存在（业务错误码） | ✅ | - | req, rev |
| `get_time_setting` | `appcgi.sysinfo.getTimeSetting` | 已实测通过 | ✅ | - | data, req, rev |
| `get_timezone_list` | `appcgi.sysinfo.getTimezoneList` | 已实测通过 | ✅ | - | data, req, rev |
| `get_trim_disk` | `appcgi.sysinfo.getTrimDisk` | 已实测存在（业务错误码） | ✅ | - | req, rev |
| `get_trim_machine_feature` | `appcgi.sysinfo.getTrimMachineFeature` | 实测超时 | ✅ | - | - |
| `get_trim_machine_type` | `appcgi.sysinfo.getTrimMachineType` | 已实测通过 | ✅ | - | data, req, rev |
| `get_trim_version` | `appcgi.sysinfo.getTrimVersion` | 已实测通过 | ✅ | - | data, req, rev |
| `get_uptime` | `appcgi.sysinfo.getUptime` | 已实测通过 | ✅ | - | data, req, rev |
| `init_host_name` | `appcgi.sysinfo.initHostName` | 未实测（写接口） | ⚠️ | - | - |
| `is_trim_machine` | `appcgi.sysinfo.isTrimMachine` | 已实测通过 | ✅ | - | data, req, rev |
| `list_power_plan` | `appcgi.sysinfo.listPowerPlan` | 已实测通过 | ✅ | - | req, rev |
| `modify_power_plan` | `appcgi.sysinfo.modifyPowerPlan` | 未实测（写接口） | ⚠️ | - | - |
| `next_power_off_time` | `appcgi.sysinfo.nextPowerOffTime` | 未实测（写接口） | ⚠️ | - | - |
| `set_boot_on_power_flag` | `appcgi.sysinfo.setBootOnPowerFlag` | 未实测（写接口） | ⚠️ | - | - |
| `set_fan_mode` | `appcgi.sysinfo.setFanMode` | 未实测（写接口） | ⚠️ | - | - |
| `set_host_name` | `appcgi.sysinfo.setHostName` | 未实测（写接口） | ⚠️ | - | - |
| `set_power_plan_status` | `appcgi.sysinfo.setPowerPlanStatus` | 未实测（写接口） | ⚠️ | - | - |
| `set_time_setting` | `appcgi.sysinfo.setTimeSetting` | 未实测（写接口） | ⚠️ | - | - |

## 实测样例

### appcgi.sysinfo.getBootOnPowerFlag

状态：已实测存在（业务错误码）（errno=100060031），耗时 30.6ms

```json
{
  "errno": 100060031,
  "reqid": "6ad238466ad23836000002da0071",
  "result": "fail",
  "rev": "0.1",
  "req": "appcgi.sysinfo.getBootOnPowerFlag"
}
```

### appcgi.sysinfo.getFanMode

状态：已实测通过，耗时 0.3ms

```json
{
  "data": {
    "mode": 2
  },
  "reqid": "6ad238476ad23836000002da0072",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.sysinfo.getFanMode"
}
```

### appcgi.sysinfo.getHardwareInfo

状态：已实测通过，耗时 0.5ms

```json
{
  "data": {
    "cpu": {
      "name": "Genuine Intel(R) 0000",
      "num": 1,
      "core": 24,
      "thread": 32
    },
    "mem": {
      "num": 2,
      "total": 68719476736,
      "frequency": 3200,
      "type": "DDR4",
      "vendor": "Asgard"
    },
    "gpu": [
      {
        "vendor": "Intel Corporation",
        "vendorId": 32902,
        "device": "UHD Graphics"
      },
      {
        "vendor": "Intel Corporation",
        "vendorId": 32902,
        "device": "Arc(TM) A770 Graphics"
      }
    ],
    "vm": {
      "available": 0,
      "iommu": 0,
      "sriov": 0
    },
    "bios": {
      "vendor": "American Megatrends International, LLC.",
      "version": "Leo-Patch 1.4",
      "baseboard": {
        "vendor": "Intel",
        "productName": "Z790M GAMING WIFI D4",
        "version": "Leo-Patch 1.4",
        "serialNumber": "Default string"
      },
      "system": {
        "vendor": "Intel",
        "productName": "i9-13950HX(ES)",
        "version": "Leo-Patch 1.4",
        "serialNumber": "Default string",
        "sku": "Default string",
        "uuid": "03000200-0400-0500-0006-000700080009",
        "family": "Default string"
      }
    },
    "sysdis
... (截断)
```

### appcgi.sysinfo.getHostName

状态：已实测通过，耗时 3.3ms

```json
{
  "data": {
    "hostName": "demoNAS",
    "hasUsers": true,
    "trimVersion": "1.2.0800"
  },
  "reqid": "6ad238476ad23836000002da0074",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.sysinfo.getHostName"
}
```

### appcgi.sysinfo.getMachineId

状态：已实测通过，耗时 0.4ms

```json
{
  "data": {
    "machineId": "3a398d1a2e664ace8179d7a13e3184d5ff45dded"
  },
  "reqid": "6ad238476ad23836000002da0075",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.sysinfo.getMachineId"
}
```

### appcgi.sysinfo.getNetInfo

状态：已实测存在（业务错误码）（errno=100000004），耗时 0.4ms

```json
{
  "errno": 100000004,
  "reqid": "6ad238476ad23836000002da0076",
  "result": "fail",
  "rev": "0.1",
  "req": "appcgi.sysinfo.getNetInfo"
}
```

### appcgi.sysinfo.getPowerPlanStatus

状态：已实测通过，耗时 3.1ms

```json
{
  "data": {
    "enable": true
  },
  "reqid": "6ad238476ad23836000002da0077",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.sysinfo.getPowerPlanStatus"
}
```

### appcgi.sysinfo.getReservedPartition

状态：已实测存在（业务错误码）（errno=100060001），耗时 0.3ms

```json
{
  "errno": 100060001,
  "reqid": "6ad238476ad23836000002da0078",
  "result": "fail",
  "rev": "0.1",
  "req": "appcgi.sysinfo.getReservedPartition"
}
```

### appcgi.sysinfo.getTimeSetting

状态：已实测通过，耗时 317.1ms

```json
{
  "data": {
    "timezone": {
      "offset": "+08:00",
      "zone": "Asia/Shanghai",
      "zone_name": "Asia/Shanghai"
    },
    "ntpEnable": true,
    "time": 1792161864,
    "ntpPool": [
      "ntp.tencent.com"
    ],
    "sysNtpPool": [
      "ntp.tencent.com",
      "ntp.aliyun.com",
      "pool.ntp.org",
      "time.google.com",
      "time.cloudflare.com",
      "time.apple.com",
      "time.windows.com",
      "time.nist.gov"
    ]
  },
  "reqid": "6ad238476ad23836000002da0079",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.sysinfo.getTimeSetting"
}
```

### appcgi.sysinfo.getTimezoneList

状态：已实测通过，耗时 13.1ms

```json
{
  "data": {
    "zonelist": [
      {
        "offset": "-12:00",
        "zone_name": "Etc/GMT+12",
        "zone": "Etc/GMT+12"
      },
      {
        "offset": "-11:00",
        "zone_name": "Etc/GMT+11",
        "zone": "Etc/GMT+11"
      },
      {
        "offset": "-10:00",
        "zone_name": "America/Adak",
        "zone": "America/Adak"
      },
      {
        "offset": "-10:00",
        "zone_name": "Pacific/Honolulu",
        "zone": "Pacific/Honolulu"
      },
      {
        "offset": "-09:30",
        "zone_name": "Pacific/Marquesas",
        "zone": "Pacific/Marquesas"
      },
      {
        "offset": "-09:00",
        "zone_name": "America/Anchorage",
        "zone": "America/Anchorage"
      },
      {
        "offset": "-09:00",
        "zone_name": "Etc/GMT+9",
        "zone": "Etc/GMT+9"
      },
      {
        "offset": "-08:00",
        "zone_name": "America/Los_Angeles",
        "zone": "America/Los_Angeles"
      },
      {
        "offset": "-08:00",
        "zone_name": "America/Tijuana",
        "zone": "America/Tijuana"
      },
      {
        "offset": "-08:00",
        "zone_name": "Etc/GMT+8",
        "zone": "Etc/GMT+8"
      },
      {
  
... (截断)
```

### appcgi.sysinfo.getTrimDisk

状态：已实测存在（业务错误码）（errno=100060031），耗时 4.4ms

```json
{
  "errno": 100060031,
  "reqid": "6ad238486ad23836000002da007b",
  "result": "fail",
  "rev": "0.1",
  "req": "appcgi.sysinfo.getTrimDisk"
}
```

### appcgi.sysinfo.getTrimMachineType

状态：已实测通过，耗时 0.6ms

```json
{
  "data": {
    "type": "",
    "model": [
      10,
      152,
      128
    ]
  },
  "reqid": "6ad238506ad23836000002da007d",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.sysinfo.getTrimMachineType"
}
```

### appcgi.sysinfo.getTrimVersion

状态：已实测通过，耗时 4.9ms

```json
{
  "data": {
    "trimVersion": "1.2.0800",
    "edition": "Mainland-PE",
    "platform": "x86"
  },
  "reqid": "6ad238506ad23836000002da007e",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.sysinfo.getTrimVersion"
}
```

### appcgi.sysinfo.getUptime

状态：已实测通过，耗时 3.6ms

```json
{
  "data": {
    "uptime": 219462
  },
  "reqid": "6ad238506ad23836000002da007f",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.sysinfo.getUptime"
}
```

### appcgi.sysinfo.isTrimMachine

状态：已实测通过，耗时 4.1ms

```json
{
  "data": {
    "isTrim": false
  },
  "reqid": "6ad238506ad23836000002da0080",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.sysinfo.isTrimMachine"
}
```

### appcgi.sysinfo.listPowerPlan

状态：已实测通过，耗时 0.6ms

```json
{
  "reqid": "6ad238516ad23836000002da0081",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.sysinfo.listPowerPlan"
}
```
