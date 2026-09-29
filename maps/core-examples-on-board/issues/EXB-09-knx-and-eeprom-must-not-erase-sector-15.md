# KNX 和 EEPROM 往 flash 存数据时不能擦扇区 15

Type: grilling
Opened: 2026-09-29
Status: open
Blocked by: -

## Question

`OpenPLC_KNX` 的应用 NVM 写死在 `0x081E0000`（`knx_config.h:94-97`，`KNX_SelfTest.ino:76` 就会写），上游 `EEPROM` 库也自动选中这个扇区（`stm32_eeprom.c:40-43`）；而扇区 15 装着校准值和固件 metadata（[SECTOR-15.md](../../../docs/modules/M1/SECTOR-15.md)），擦了之后下次上电 bootloader 停在等重传、校准值要回工装重写。KNX 应用 NVM 挪到哪、`EEPROM` 库是删掉、禁用还是挪扇区，由谁来防止以后再有代码写进扇区 15。

## 怎么算答完

定下 KNX 应用 NVM 和 `EEPROM` 各自的去处，以及一道能自动发现「有代码往扇区 15 写」的检查；改完后在真板上跑 `KNX_SelfTest`，扇区 15 逐字节不变。
