# USB 管调试和升级，RS232 留给设备

## 怎么看进度（不用问任何人）

```
python tools/list_wayfinder_map_frontier.py --all
```

## Destination

出厂的板子上，bootloader 和 core 不往 RS232 端子写任何东西，RS232 完全归用户程序；用户只插一根 USB 就能上传、看 sketch 的打印、拿到开机和出错的信息；测试仍有看得见板子内部的办法。到这一步时，要做的每件事都已定好、写进文档，可以照着改。

## Notes

- 来源：[决策 147](../../docs/tables/DECISIONS.md)（取代决策 100）
- 相关：[USB 和网口共用一套上传流程](../arduino-examples-and-ide-flow/issues/IDE-17-usb-and-ethernet-share-one-upload-flow.md)（双 CDC 口，决定能不能边看打印边上传）
- RS232 的硬件事实（UART4 / USART3 同脚、MAX3221 使能）见 [HARDWARE-FACTS.md](../../docs/hardware/HARDWARE-FACTS.md)「RS232 路径」
- 开票 / 关票 / 算前沿照 [图与票的约定](../MAP-AND-TICKET-CONVENTION.md)

## 全集

```
grep -rlE 'RS232\.|RS232_EN|Enable_RX_RS232|DEBUG_UART|printf\(|LOG_PORTS|log_port' open_plc_cube_ide/IAPServer open_plc_cube_ide/Core/Src open_plc_arduino/cores open_plc_arduino/libraries OpenPLC_Test/tools OpenPLC_Test/host OpenPLC_Test/onboard ; grep -rlE 'RS232|诊断口|决策 100' OpenPLC_Docs/docs
```

关最后一张票前重跑：每个文件要么已定怎么改，要么写明为什么不用改。

## Decisions so far

- [从上电到 app 跑起来，RS232 端子上实际会出现什么](issues/USB-02-what-appears-on-rs232-at-power-up.md)：正常上电设备收到 bootloader 10 行 + app `[BOOT]` 1 行，`setup()` 后再 1 行 `[NET]`；收发器由 bootloader 开、交权前关、core 再开且不关，要安静只能去掉打印
- [开机、bootloader、死机的信息，出厂板子上给谁看、在哪看](issues/USB-01-who-reads-boot-and-crash-info.md)：RS232 一个字节都不写；日志走 USB 口 1（口 2 跑 IAP），SRAM4 开机缓存 4 KB，死机信息复位后吐出，不设 RS232 开关
- [sketch 的 `Serial` 和 core 自己的日志走哪](issues/USB-03-where-serial-and-core-log-go.md)：`RS232.begin()` 才开芯片；打印用 `Serial`（不改名）；系统日志 `[sys]` 前缀、宏可关、口 1 没开只进缓存；例程改回 `Serial`
- [测试靠什么看板子内部](issues/USB-04-how-tests-see-inside-the-board.md)：上板脚本读 USB 口 1 的 `[sys]` 行，Renode 照 SIM-01 落 UART 并读 SRAM4 缓存，判据只换通道；USB 坏了走网口，都坏了用 SWO

## Not yet specified

- 开机缓存和故障记录的格式、日志前缀格式；IAPTool 经 USB 口 2 读缓存（网口的 `IAPTool log <ip>` 已定，见 [IAP-PROTOCOL.md](../../docs/modules/M1/IAP-PROTOCOL.md)「`openplc_log`」）
- bootloader 双 CDC 口、开机就初始化 USB、bootloader 和 app 身份统一 —— 和 IDE-17 合流
- IAPTool 重启后按 bootloader 身份 + UID 找口
- 「USB 不可用不拖垮开机和网口上传」（`R1-43`）的用例：拔掉 USB、USB 不枚举两种
- bootloader 体积：2026-10-13 的 Debug 版 108,612 B，flash 区 128 KiB，余约 22 KB；加双 CDC 和缓存前后要再量

## Out of scope

- 工装固件（`$BOOT` `TestCase/`）和 PortTool：不发给客户，测的正是 RS232 端子本身
