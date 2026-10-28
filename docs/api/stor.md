# stor

> 自动生成（`python tools/gen_api.py`），共 64 个接口。
> 调用示例：`await client.api.stor.abort_smart_test(...)`

| 方法 | req | 状态 | 只读 | 已知参数 | 响应字段 |
| --- | --- | --- | --- | --- | --- |
| `abort_smart_test` | `stor.abortSmartTest` | 未实测（写接口） | ⚠️ | - | - |
| `add_disk` | `stor.addDisk` | 未实测（写接口） | ⚠️ | - | - |
| `add_spare_disk` | `stor.addSpareDisk` | 未实测（写接口） | ⚠️ | - | - |
| `attach_cache` | `stor.attachCache` | 未实测（写接口） | ⚠️ | - | - |
| `btrfs_scrub` | `stor.btrfs.scrub` | 未实测（写接口） | ⚠️ | - | - |
| `cachedev_state` | `stor.cachedevState` | 未实测（写接口） | ⚠️ | - | - |
| `calc_space` | `stor.calcSpace` | 已实测通过 | ✅ | - | HDD, SSD, USB, frsizeStor, frsizeSys, fssizeStor |
| `create` | `stor.create` | 未实测（写接口） | ⚠️ | - | - |
| `create_cache` | `stor.createCache` | 未实测（写接口） | ⚠️ | - | - |
| `del_rec` | `stor.delRec` | 未实测（写接口） | ⚠️ | - | - |
| `detach_cache` | `stor.detachCache` | 未实测（写接口） | ⚠️ | - | - |
| `detach_cache_and_active` | `stor.detachCacheAndActive` | 未实测（写接口） | ⚠️ | - | - |
| `disk_health` | `stor.diskHealth` | 已实测存在（缺参数） | ✅ | - | - |
| `disk_mount` | `stor.diskMount` | 未实测（写接口） | ⚠️ | - | - |
| `disk_smart` | `stor.diskSmart` | 已实测存在（缺参数） | ✅ | - | - |
| `eject` | `stor.eject` | 未实测（写接口） | ⚠️ | - | - |
| `enable_smart` | `stor.enableSmart` | 未实测（写接口） | ⚠️ | - | - |
| `extend` | `stor.extend` | 未实测（写接口） | ⚠️ | - | - |
| `general` | `stor.general` | 已实测通过 | ✅ | - | array, block |
| `get_conf` | `stor.getConf` | 已实测存在（缺参数） | ✅ | - | - |
| `get_disk_idle_time` | `stor.getDiskIdleTime` | 已实测通过 | ✅ | - | idleTime, idleTimeRemovable |
| `get_disk_wakeup` | `stor.getDiskWakeup` | 已实测通过 | ✅ | - | wakeup |
| `get_global` | `stor.getGlobal` | 已实测通过 | ✅ | - | zfs_arc_max, zfs_vdev_async_write_max_active |
| `get_removable_conf` | `stor.getRemovableConf` | 已实测通过 | ✅ | - | permit |
| `get_sys_part_info` | `stor.getSysPartInfo` | 已实测通过 | ✅ | - | frsize, fssize |
| `get_team_storage` | `stor.getTeamStorage` | 已实测存在（缺参数） | ✅ | - | - |
| `get_user_storage` | `stor.getUserStorage` | 已实测通过 | ✅ | quotaInfo, spaceInfo, storInfo | stor, uid |
| `list_cachedev` | `stor.listCachedev` | 已实测通过 | ✅ | - | disk |
| `list_disk` | `stor.listDisk` | 已实测通过 | ✅ | - | disk |
| `list_free_disk` | `stor.listFreeDisk` | 已实测通过 | ✅ | - | disk |
| `list_removable` | `stor.listRemovable` | 已实测通过 | ✅ | - | removable |
| `list_stor` | `stor.listStor` | 已实测通过 | ✅ | - | array |
| `llbitmap_proactive_sync` | `stor.llbitmap.proactiveSync` | 未实测（写接口） | ⚠️ | - | - |
| `lv_active` | `stor.lvActive` | 未实测（写接口） | ⚠️ | - | - |
| `make_team_storage` | `stor.makeTeamStorage` | 未实测（写接口） | ⚠️ | - | - |
| `mount` | `stor.mount` | 未实测（写接口） | ⚠️ | - | - |
| `readd_disk` | `stor.readdDisk` | 已实测存在（缺参数） | ✅ | - | - |
| `readd_disk_to_cache` | `stor.readdDiskToCache` | 已实测存在（缺参数） | ✅ | - | - |
| `recover_cache` | `stor.recoverCache` | 未实测（写接口） | ⚠️ | - | - |
| `remove_disk` | `stor.removeDisk` | 未实测（写接口） | ⚠️ | - | - |
| `remove_disk_check` | `stor.removeDiskCheck` | 未实测（写接口） | ⚠️ | - | - |
| `remove_warn` | `stor.removeWarn` | 未实测（写接口） | ⚠️ | - | - |
| `replace_disk` | `stor.replaceDisk` | 未实测（写接口） | ⚠️ | - | - |
| `resize` | `stor.resize` | 未实测（写接口） | ⚠️ | - | - |
| `run_smart_test` | `stor.runSmartTest` | 未实测（写接口） | ⚠️ | - | - |
| `set_conf` | `stor.setConf` | 未实测（写接口） | ⚠️ | - | - |
| `set_disk_idle_time` | `stor.setDiskIdleTime` | 未实测（写接口） | ⚠️ | - | - |
| `set_disk_wakeup` | `stor.setDiskWakeup` | 未实测（写接口） | ⚠️ | - | - |
| `set_global` | `stor.setGlobal` | 未实测（写接口） | ⚠️ | - | - |
| `set_removable_conf` | `stor.setRemovableConf` | 未实测（写接口） | ⚠️ | - | - |
| `set_team_storage` | `stor.setTeamStorage` | 未实测（写接口） | ⚠️ | - | - |
| `set_trashbin` | `stor.setTrashbin` | 未实测（写接口） | ⚠️ | - | - |
| `set_user_storage` | `stor.setUserStorage` | 未实测（写接口） | ⚠️ | set | - |
| `state2` | `stor.state2` | 已实测通过 | ✅ | - | state |
| `stop` | `stor.stop` | 未实测（写接口） | ⚠️ | - | - |
| `stor_add_disk_info` | `stor.storAddDiskInfo` | 未实测（写接口） | ⚠️ | - | - |
| `umount` | `stor.umount` | 未实测（写接口） | ⚠️ | - | - |
| `z_clear` | `stor.zClear` | 未实测（写接口） | ⚠️ | - | - |
| `z_export` | `stor.zExport` | 未实测（写接口） | ⚠️ | - | - |
| `z_import` | `stor.zImport` | 未实测（写接口） | ⚠️ | - | - |
| `z_import_list` | `stor.zImportList` | 未实测（写接口） | ⚠️ | - | - |
| `z_online` | `stor.zOnline` | 未实测（写接口） | ⚠️ | - | - |
| `z_recover` | `stor.zRecover` | 未实测（写接口） | ⚠️ | - | - |
| `z_scrub` | `stor.zScrub` | 未实测（写接口） | ⚠️ | - | - |

## 实测样例

### stor.calcSpace

状态：已实测通过，耗时 14.7ms

```json
{
  "fssizeSys": 63677190144,
  "frsizeSys": 44970573824,
  "sysDiskType": "SSD",
  "storTotal": 6,
  "fssizeStor": 16688454434816,
  "frsizeStor": 12985099231232,
  "HDD": 1,
  "SSD": 5,
  "USB": 0,
  "result": "succ",
  "reqid": "6ad238566ad23836000002da00a6"
}
```

### stor.diskHealth

状态：已实测存在（缺参数）（errno=8192），耗时 4.4ms

```json
{
  "errno": 8192,
  "result": "fail",
  "reqid": "6ad238566ad23836000002da00a7"
}
```

### stor.diskSmart

状态：已实测存在（缺参数）（errno=8192），耗时 0.5ms

```json
{
  "errno": 8192,
  "result": "fail",
  "reqid": "6ad238566ad23836000002da00a8"
}
```

### stor.general

状态：已实测通过，耗时 37.4ms

```json
{
  "array": [
    {
      "name": "dm-1",
      "uuid": "trim_44b2de15_8a34_4f43_af2f_0a3982d43b0b-0",
      "mountpoint": "/vol4",
      "frsize": 300135895040,
      "fssize": 390192791552,
      "md": [
        {
          "name": "md1",
          "uuid": "aa4ffa9e-d25d-0c01-4ce2-a510327c7127",
          "raidDisks": 1,
          "level": "basic",
          "bitmapType": "bitmap",
          "arrayState": "clean",
          "syncAction": "idle",
          "syncCompleted": "none"
        }
      ],
      "level": "basic",
      "storId": 4,
      "comment": ""
    },
    {
      "name": "dm-2",
      "uuid": "trim_9d764261_1c92_4240_a7e5_4b8a6a57488b-0",
      "mountpoint": "/vol2",
      "frsize": 458681745408,
      "fssize": 509963567104,
      "md": [
        {
          "name": "md2",
          "uuid": "9c2ea91b-f84b-7c4f-4c38-63534be4bb83",
          "raidDisks": 1,
          "level": "basic",
          "bitmapType": "bitmap",
          "arrayState": "clean",
          "syncAction": "idle",
          "syncCompleted": "none"
        }
      ],
      "level": "basic",
      "storId": 2,
      "comment": ""
    },
    {
      "name": "dm-0",
      "uuid": "trim_54fcd6a9_734c_4
... (截断)
```

### stor.getConf

状态：已实测存在（缺参数）（errno=8192），耗时 0.6ms

```json
{
  "errno": 8192,
  "result": "fail",
  "reqid": "6ad238566ad23836000002da00aa"
}
```

### stor.getDiskIdleTime

状态：已实测通过，耗时 3.3ms

```json
{
  "idleTime": 30,
  "idleTimeRemovable": 30,
  "result": "succ",
  "reqid": "6ad238566ad23836000002da00ab"
}
```

### stor.getDiskWakeup

状态：已实测通过，耗时 3.5ms

```json
{
  "wakeup": 1,
  "result": "succ",
  "reqid": "6ad238566ad23836000002da00ac"
}
```

### stor.getGlobal

状态：已实测通过，耗时 3.7ms

```json
{
  "zfs_vdev_async_write_max_active": 10,
  "zfs_arc_max": 0,
  "result": "succ",
  "reqid": "6ad238566ad23836000002da00ad"
}
```

### stor.getRemovableConf

状态：已实测通过，耗时 0.5ms

```json
{
  "permit": 1,
  "result": "succ",
  "reqid": "6ad238566ad23836000002da00ae"
}
```

### stor.getSysPartInfo

状态：已实测通过，耗时 5.4ms

```json
{
  "frsize": 44970573824,
  "fssize": 63677190144,
  "result": "succ",
  "reqid": "6ad238576ad23836000002da00af"
}
```

### stor.getTeamStorage

状态：已实测存在（缺参数）（errno=8192），耗时 3.9ms

```json
{
  "errno": 8192,
  "result": "fail",
  "reqid": "6ad238576ad23836000002da00b0"
}
```

### stor.getUserStorage

状态：已实测通过，耗时 79.6ms

```json
{
  "stor": [
    {
      "id": 4,
      "comment": ""
    },
    {
      "id": 1,
      "comment": "P4800X"
    },
    {
      "id": 2,
      "comment": ""
    },
    {
      "id": 3,
      "comment": ""
    },
    {
      "id": 5,
      "comment": "SN570"
    },
    {
      "id": 6,
      "comment": ""
    }
  ],
  "uid": 1000,
  "result": "succ",
  "reqid": "6ad238576ad23836000002da00b1"
}
```

### stor.listCachedev

状态：已实测通过，耗时 650.3ms

```json
{
  "disk": [
    {
      "name": "sdd",
      "size": 240057409536,
      "sys": 1,
      "frsizeSys": 44970569728,
      "fssizeSys": 63677190144,
      "part": "sdd3",
      "partSize": 171337318400,
      "modelName": "TOSHIBA-TR200",
      "serialNumber": "79UB815TKEKN",
      "type": "SSD",
      "protocol": "SATA",
      "firmwareVersion": "SBFA15.2",
      "logicalBlockSize": 512,
      "physicalBlockSize": 512,
      "sataVersion": "SATA 3.2",
      "diskGroup": "sysSSD",
      "diskGroupEx": "sysSSD",
      "partitions": [
        {
          "no": 1,
          "name": "sdd1",
          "size": 199229440,
          "mountName": "efi",
          "fstype": "vfat",
          "fssize": 196131840,
          "frsize": 187728896,
          "efi": 1
        },
        {
          "no": 2,
          "name": "sdd2",
          "size": 68519198720,
          "mountName": "/",
          "fstype": "ext4",
          "fssize": 63677190144,
          "frsize": 44970569728,
          "sys": 1
        },
        {
          "no": 3,
          "name": "sdd3",
          "size": 171337318400
        }
      ]
    },
    {
      "name": "sdc",
      "size": 14000519643136,
      "modelName": "H
... (截断)
```

### stor.listDisk

状态：已实测通过，耗时 0.0ms

```json
{
  "disk": [
    {
      "name": "nvme0n1",
      "size": 1000204886016,
      "modelName": "WD Blue SN570 1TB SSD",
      "serialNumber": "2226B4443505",
      "type": "SSD",
      "protocol": "NVMe",
      "firmwareVersion": "234110WD",
      "logicalBlockSize": 512,
      "nvmeVersion": "1.4",
      "diskGroup": "SSD",
      "diskGroupEx": "SSD",
      "storage": [
        {
          "vdName": "164171d7-18e7-450e-8cbe-74f84b6075d4",
          "arrState": "ONLINE",
          "storUuid": "trim_ccd75486-c354-49c3-ac4c-7cf5dfb662de",
          "storId": 5,
          "storName": "",
          "level": "stripe"
        }
      ]
    },
    {
      "name": "sdd",
      "size": 240057409536,
      "sys": 1,
      "frsizeSys": 44970569728,
      "fssizeSys": 63677190144,
      "part": "sdd3",
      "partSize": 171337318400,
      "modelName": "TOSHIBA-TR200",
      "serialNumber": "79UB815TKEKN",
      "type": "SSD",
      "protocol": "SATA",
      "firmwareVersion": "SBFA15.2",
      "logicalBlockSize": 512,
      "physicalBlockSize": 512,
      "sataVersion": "SATA 3.2",
      "diskGroup": "sysSSD",
      "diskGroupEx": "sysSSD",
      "partitions": [
        {
          "no": 1,
   
... (截断)
```

### stor.listFreeDisk

状态：已实测通过，耗时 16.2ms

```json
{
  "disk": [
    {
      "name": "sdd",
      "size": 240057409536,
      "sys": 1,
      "frsizeSys": 44970569728,
      "fssizeSys": 63677190144,
      "part": "sdd3",
      "partSize": 171337318400,
      "modelName": "TOSHIBA-TR200",
      "serialNumber": "79UB815TKEKN",
      "type": "SSD",
      "protocol": "SATA",
      "firmwareVersion": "SBFA15.2",
      "logicalBlockSize": 512,
      "physicalBlockSize": 512,
      "sataVersion": "SATA 3.2",
      "diskGroup": "sysSSD",
      "diskGroupEx": "sysSSD",
      "partitions": [
        {
          "no": 1,
          "name": "sdd1",
          "size": 199229440,
          "mountName": "efi",
          "fstype": "vfat",
          "fssize": 196131840,
          "frsize": 187728896,
          "efi": 1
        },
        {
          "no": 2,
          "name": "sdd2",
          "size": 68519198720,
          "mountName": "/",
          "fstype": "ext4",
          "fssize": 63677190144,
          "frsize": 44970569728,
          "sys": 1
        },
        {
          "no": 3,
          "name": "sdd3",
          "size": 171337318400
        }
      ]
    },
    {
      "name": "sdc",
      "size": 14000519643136,
      "modelName": "H
... (截断)
```

### stor.listRemovable

状态：已实测通过，耗时 29.0ms

```json
{
  "removable": [
    {
      "mountName": "HSH721414ALN6M0",
      "path": "vol00/HSH721414ALN6M0",
      "name": "sdc",
      "diskName": "sdc",
      "modelName": "HSH721414ALN6M0",
      "serialNumber": "VFG3242D",
      "type": "HDD",
      "protocol": "SATA",
      "firmwareVersion": "T108",
      "logicalBlockSize": 4096,
      "physicalBlockSize": 4096,
      "sataVersion": "SATA 3.2",
      "rotationRate": 7200,
      "fssize": 13964505415680,
      "frsize": 6987613007872
    }
  ],
  "result": "succ",
  "reqid": "6ad238586ad23836000002da00b5"
}
```

### stor.listStor

状态：已实测通过，耗时 34.9ms

```json
{
  "array": [
    {
      "name": "dm-1",
      "size": 399947857920,
      "uuid": "trim_44b2de15_8a34_4f43_af2f_0a3982d43b0b-0",
      "mountpoint": "/vol4",
      "fstype": "btrfs",
      "frsize": 300135895040,
      "fssize": 390192791552,
      "md": [
        {
          "name": "md1",
          "size": 399952052224,
          "uuid": "aa4ffa9e-d25d-0c01-4ce2-a510327c7127",
          "raidDisks": 1,
          "level": "basic",
          "bitmapType": "bitmap",
          "arrayState": "clean",
          "syncAction": "idle",
          "syncCompleted": "none",
          "disk": [
            {
              "name": "nvme2n1",
              "size": 400088457216,
              "partitions": [
                {
                  "no": 1,
                  "name": "nvme2n1p1",
                  "size": 400087318528
                }
              ],
              "arrSlot": "0",
              "arrState": "in_sync",
              "modelName": "INTEL SSDPFR1Q400GBF",
              "serialNumber": "PHAK2205008C400AGN",
              "type": "SSD",
              "protocol": "NVMe",
              "firmwareVersion": "L031FP01",
              "logicalBlockSize": 512,
              "nvme
... (截断)
```

### stor.readdDisk

状态：已实测存在（缺参数）（errno=8192），耗时 0.4ms

```json
{
  "errno": 8192,
  "result": "fail",
  "reqid": "6ad238586ad23836000002da00b7"
}
```

### stor.readdDiskToCache

状态：已实测存在（缺参数）（errno=8192），耗时 3.5ms

```json
{
  "errno": 8192,
  "result": "fail",
  "reqid": "6ad238586ad23836000002da00b8"
}
```

### stor.state2

状态：已实测通过，耗时 4.3ms

```json
{
  "state": [
    {
      "name": "dm-1",
      "uuid": "trim_44b2de15_8a34_4f43_af2f_0a3982d43b0b-0",
      "frsize": 300135895040,
      "fssize": 390192791552
    },
    {
      "name": "dm-2",
      "uuid": "trim_9d764261_1c92_4240_a7e5_4b8a6a57488b-0",
      "frsize": 458681745408,
      "fssize": 509963567104
    },
    {
      "name": "dm-0",
      "uuid": "trim_54fcd6a9_734c_4051_af62_839fda2dcca7-0",
      "frsize": 235024965632,
      "fssize": 374415097856
    },
    {
      "name": "dm-3",
      "uuid": "trim_389dc2e3_b7f0_436f_9b70_66cff7ca6508-0",
      "frsize": 10658534342656,
      "fssize": 13965601341440
    },
    {
      "uuid": "trim_ccd75486-c354-49c3-ac4c-7cf5dfb662de",
      "frsize": 965560238080,
      "fssize": 965561286656
    },
    {
      "uuid": "trim_dee999bd-f629-42b9-9fe4-95956033faa9",
      "frsize": 367162032128,
      "fssize": 482720350208
    }
  ],
  "result": "succ",
  "reqid": "6ad238586ad23836000002da00b9"
}
```
