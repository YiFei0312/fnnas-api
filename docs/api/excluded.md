# 未封装的名字及原因（自动生成）

## 实测证伪（服务端返回「接口不存在」）

> 静态扫描把它们当候选抓出来了，但真机实测 errno=10000002，
> 说明服务端没有这个接口，多为 i18n 文案键。

- `apis.tfa.getMineConfig`
- `app.getdefinstvolume`
- `app.geticon`
- `app.info`
- `app.list`
- `app.listvolume`
- `exconn.getDomain`
- `icenter.gen`
- `icenter.svc`
- `log.graph`
- `log.list`
- `remoteDir.list`
- `target.checked`
- `usrdat.getArray`
- `usrdat.getArrayUpdateTime`
- `usrdat.isArrayValueExists`

## 一级模块存疑（疑似 App id / 日期格式串，未实测不封装）

- `app.install`
- `app.restart`
- `app.setdefinstvolume`
- `app.start`
- `app.stop`
- `app.uninstall`
- `data.dirList`
- `dd.MM.y`
- `dd.MM.yyyy`
- `exconn.setDomain`
- `log.clear`
- `monthLeft.dateInput`
- `monthLeft.timeInput`
- `monthRight.dateInput`
- `monthRight.timeInput`
- `remoteDir.add`
- `remoteDir.del`
- `remoteDir.mount`
- `remoteDir.umount`
- `target.value`
- `trim.media`
- `trim.photos`
- `y.MM.dd`
