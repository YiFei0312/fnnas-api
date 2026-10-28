# appcgi.resmon

> 自动生成（`python tools/gen_api.py`），共 16 个接口。
> 调用示例：`await client.api.appcgi.resmon.alert_get_beep_events(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `alert_get_beep_events` | `appcgi.resmon.alert.getBeepEvents` | 已实测通过 | ✅ | - | req, rev |
| `alert_get_beep_reasons` | `appcgi.resmon.alert.getBeepReasons` | 已实测通过 | ✅ | - | req, rev |
| `alert_get_supported_beep_events` | `appcgi.resmon.alert.getSupportedBeepEvents` | 已实测通过 | ✅ | - | req, rev |
| `alert_mute_beeper` | `appcgi.resmon.alert.muteBeeper` | 未实测（写接口） | ⚠️ | - | - |
| `alert_set_beep_events` | `appcgi.resmon.alert.setBeepEvents` | 未实测（写接口） | ⚠️ | - | - |
| `battery` | `appcgi.resmon.battery` | 已实测存在（业务错误码） | ✅ | - | req, rev |
| `cpu` | `appcgi.resmon.cpu` | 已实测通过 | ✅ | - | data, req, rev |
| `disk` | `appcgi.resmon.disk` | 已实测通过 | ✅ | - | data, req, rev |
| `gen` | `appcgi.resmon.gen` | 已实测存在（缺参数） | ✅ | - | req, rev |
| `gpu` | `appcgi.resmon.gpu` | 已实测通过 | ✅ | - | data, req, rev |
| `mem` | `appcgi.resmon.mem` | 已实测通过 | ✅ | - | data, req, rev |
| `npu` | `appcgi.resmon.npu` | 已实测通过 | ✅ | - | data, req, rev |
| `proc_list` | `appcgi.resmon.proc.list` | 已实测通过 | ✅ | - | data, req, rev |
| `proc_signal` | `appcgi.resmon.proc.signal` | 未实测（写接口） | ⚠️ | - | - |
| `proc_srv` | `appcgi.resmon.proc.srv` | 实测返回非标准结构 | ✅ | - | data, req, rev |
| `sys_fan` | `appcgi.resmon.sysFan` | 已实测通过 | ✅ | - | data, req, rev |

## 实测样例

### appcgi.resmon.alert.getBeepEvents

状态：已实测通过，耗时 38.2ms

```json
{
  "reqid": "6ad238406ad23836000002da003e",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.resmon.alert.getBeepEvents"
}
```

### appcgi.resmon.alert.getBeepReasons

状态：已实测通过，耗时 3.4ms

```json
{
  "reqid": "6ad238406ad23836000002da003f",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.resmon.alert.getBeepReasons"
}
```

### appcgi.resmon.alert.getSupportedBeepEvents

状态：已实测通过，耗时 81.9ms

```json
{
  "reqid": "6ad238406ad23836000002da0040",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.resmon.alert.getSupportedBeepEvents"
}
```

### appcgi.resmon.battery

状态：已实测存在（业务错误码）（errno=100030002），耗时 49.7ms

```json
{
  "errno": 100030002,
  "reqid": "6ad238406ad23836000002da0041",
  "result": "fail",
  "rev": "0.1",
  "req": "appcgi.resmon.battery"
}
```

### appcgi.resmon.cpu

状态：已实测通过，耗时 37.8ms

```json
{
  "data": {
    "cpu": {
      "name": "Genuine Intel(R) 0000",
      "num": 1,
      "core": 24,
      "thread": 32,
      "maxFreq": 6000,
      "temp": [
        33
      ],
      "busy": {
        "all": 0,
        "user": 0,
        "system": 0,
        "iowait": 0,
        "other": 0
      },
      "loadavg": {
        "avg1min": 1.9716796875,
        "avg5min": 2.2587890625,
        "avg15min": 2.1884765625
      }
    }
  },
  "reqid": "6ad238406ad23836000002da0042",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.resmon.cpu"
}
```

### appcgi.resmon.disk

状态：已实测通过，耗时 85.7ms

```json
{
  "data": {
    "num": 8,
    "disk": [
      {
        "name": "sda",
        "temp": 0,
        "standby": false,
        "busy": 0,
        "read": 0,
        "write": 0
      },
      {
        "name": "nvme2n1",
        "temp": 0,
        "standby": false,
        "busy": 0,
        "read": 0,
        "write": 0
      },
      {
        "name": "nvme1n1",
        "temp": 0,
        "standby": false,
        "busy": 0,
        "read": 23949312,
        "write": 13312
      },
      {
        "name": "sdb",
        "temp": 0,
        "standby": false,
        "busy": 0,
        "read": 0,
        "write": 0
      },
      {
        "name": "sdc",
        "temp": 0,
        "standby": false,
        "busy": 0,
        "read": 0,
        "write": 0
      },
      {
        "name": "nvme3n1",
        "temp": 0,
        "standby": false,
        "busy": 0,
        "read": 0,
        "write": 0
      },
      {
        "name": "sdd",
        "temp": 0,
        "standby": false,
        "busy": 23,
        "read": 5660672,
        "write": 335872
      },
      {
        "name": "nvme0n1",
        "temp": 0,
        "standby": false,
        "busy": 0,
        "read": 0,
        "wr
... (截断)
```

### appcgi.resmon.gen

状态：已实测存在（缺参数）（errno=100000002），耗时 31.5ms

```json
{
  "errno": 100000002,
  "reqid": "6ad238416ad23836000002da0044",
  "result": "fail",
  "rev": "0.1",
  "req": "appcgi.resmon.gen"
}
```

### appcgi.resmon.gpu

状态：已实测通过，耗时 16.3ms

```json
{
  "data": {
    "num": 2,
    "gpu": [
      {
        "index": 1,
        "vendor": "Intel Corporation",
        "vendorId": 32902,
        "device": "UHD Graphics",
        "deviceId": 42888,
        "subDeviceId": 0,
        "domain": 0,
        "xe2": 0,
        "rebar": 0,
        "bus": 0,
        "dev": 2,
        "func": 0,
        "busy": 0,
        "ram": {
          "total": 0,
          "used": 0,
          "free": 0
        },
        "temp": 38,
        "engine": {
          "video": 0,
          "render": 0
        }
      },
      {
        "index": 2,
        "vendor": "Intel Corporation",
        "vendorId": 32902,
        "device": "Arc(TM) A770 Graphics",
        "deviceId": 22176,
        "subDeviceId": 0,
        "domain": 0,
        "xe2": 0,
        "rebar": 1,
        "bus": 3,
        "dev": 0,
        "func": 0,
        "busy": 0,
        "ram": {
          "total": 0,
          "used": 0,
          "free": 0
        },
        "engine": {
          "video": 0,
          "render": 0
        }
      }
    ]
  },
  "reqid": "6ad238416ad23836000002da0045",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.resmon.gpu"
}
```

### appcgi.resmon.mem

状态：已实测通过，耗时 12.6ms

```json
{
  "data": {
    "mem": {
      "reserved": 1750241280,
      "total": 68719476736,
      "free": 592465920,
      "used": 66374586368,
      "available": 594649088,
      "cached": 553877504,
      "buffers": 2850816,
      "zfsArc": 2037536000
    },
    "swap": {
      "total": 7516188672,
      "free": 1386770432,
      "used": 6129418240
    }
  },
  "reqid": "6ad238416ad23836000002da0046",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.resmon.mem"
}
```

### appcgi.resmon.npu

状态：已实测通过，耗时 0.4ms

```json
{
  "data": {
    "num": 0
  },
  "reqid": "6ad238416ad23836000002da0047",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.resmon.npu"
}
```

### appcgi.resmon.proc.list

状态：已实测通过，耗时 84.8ms

```json
{"data": {"list": [{"name": "systemd-timedat", "pid": 944585, "status": "S", "cpu": 0.0, "cpuTime": 0, "memory": 7360512, "ioRead": 0, "ioWrite": 0, "uid": 0}, {"name": "postgres", "pid": 2869181, "status": "S", "cpu": 0.0, "cpuTime": 0, "memory": 4911104, "ioRead": 0, "ioWrite": 0, "uid": 107}, {"name": "postgres", "pid": 2869180, "status": "S", "cpu": 0.0, "cpuTime": 0, "memory": 4677632, "ioRead": 0, "ioWrite": 0, "uid": 107}, {"name": "postgres", "pid": 2869176, "status": "S", "cpu": 0.0, "cpuTime": 0, "memory": 5095424, "ioRead": 0, "ioWrite": 0, "uid": 107}, {"name": "postgres", "pid": 2869172, "status": "S", "cpu": 0.0, "cpuTime": 0, "memory": 5087232, "ioRead": 0, "ioWrite": 0, "uid": 107}, {"name": "smbd", "pid": 2868078, "status": "S", "cpu": 0.0, "cpuTime": 1, "memory": 4640768, "ioRead": 0, "ioWrite": 0, "uid": 0}, {"name": "hermes", "pid": 2137695, "status": "S", "cpu": 0.03086419776082039, "cpuTime": 1052, "memory": 33009664, "ioRead": 0, "ioWrite": 0, "uid": 983}, {"name": "postgres", "pid": 2137537, "status": "S", "cpu": 0.0, "cpuTime": 0, "memory": 4841472, "ioRead": 0, "ioWrite": 0, "uid": 107}, {"name": "python3", "pid": 1376377, "status": "S", "cpu": 0.0, "cpuTi
```

### appcgi.resmon.proc.srv

状态：实测返回非标准结构，耗时 4.7ms

```json
{
  "data": {
    "srv": [
      {
        "name": "trim_core",
        "displayName": "",
        "system": true,
        "proc": [
          {
            "name": "trim",
            "cpu": 0.03086419776082039,
            "cpuTime": 907,
            "memory": 67842048,
            "ioRead": 180224,
            "ioWrite": 0,
            "pid": 2983
          },
          {
            "name": "finder_service",
            "cpu": 0.0,
            "cpuTime": 24,
            "memory": 5210112,
            "ioRead": 0,
            "ioWrite": 0,
            "pid": 2988
          },
          {
            "name": "imagesrv",
            "cpu": 0.0,
            "cpuTime": 25,
            "memory": 4943872,
            "ioRead": 0,
            "ioWrite": 0,
            "pid": 2989
          },
          {
            "name": "mediasrv",
            "cpu": 0.0,
            "cpuTime": 112,
            "memory": 4222976,
            "ioRead": 0,
            "ioWrite": 0,
            "pid": 2990
          },
          {
            "name": "rpc_broker",
            "cpu": 0.0,
            "cpuTime": 16,
            "memory": 4096000,
            "ioRead": 0,
            "ioWrite": 0,
      
... (截断)
```

### appcgi.resmon.sysFan

状态：已实测通过，耗时 4.7ms

```json
{
  "data": {
    "isTrim": false
  },
  "reqid": "6ad238416ad23836000002da004a",
  "result": "succ",
  "rev": "0.1",
  "req": "appcgi.resmon.sysFan"
}
```
