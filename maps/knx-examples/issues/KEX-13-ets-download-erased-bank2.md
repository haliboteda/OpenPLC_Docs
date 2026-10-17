# ETS 下载把 bank2 整个擦了

Type: task
Opened: 2026-10-13
Status: resolved
Blocked by: -

## Question

用户 2026-10-13：DI6 关联到 1/0/1 后 ETS 做部分下载，板子死了；重新上传后开机打印 `KNX: not configured`；再做完整下载，下载到一半板子重启。

ST-Link 读出：bank2 扇区 6（KNX 数据）和扇区 7（bootloader 状态：校准值、所有权根区、metadata）除 bootloader 在 `0x081FFFE0` 的 `S15L` 标记外全是 0xFF；bank1 的 app 完好。于是 app 签名无效、所有权为空。

## 怎么算答完

找到擦掉扇区 7 的代码，改掉，固件编过；上板复测记进 TODO。

## Answer

2026-10-13 查实并修好代码；同日上板复测通过：写个体地址、完整下载、多次部分下载共 9 次重启，每次 bootloader 日志都是所有权已认领、metadata 在（7 条不变），开机打印 `KNX: address 1.1.20, configured`。

**原因**：`$CORE_REPO/libraries/OpenPLC_KNX/src/knx_nvm.cpp:34` 的 `knx_nvm_sector_write()` 建 `FLASH_EraseInitTypeDef` 时没设 `VoltageRange`。HAL 把它原样或进 `FLASH->CR2`，和 `SER | START` 一起写（`$CORE_LIVE/system/Drivers/STM32H7xx_HAL_Driver/Src/stm32h7xx_hal_flash_ex.c:957`）；CR 的 bit3 是 `BER`（`stm32h743xx.h` `FLASH_CR_BER_Pos`），栈上残值带着它时，扇区擦除变成整个 bank2 擦除。

**修法**：结构体清零，`VoltageRange = FLASH_VOLTAGE_RANGE_3`，和 bootloader 的 `Flash_If_Erase`（`$BOOT/Core/Src/usbd_cdc_flash.c:55-59`）一致。板卡包里没有别的 `FLASH_EraseInitTypeDef` 用户。

**P19 加一条**：凡声明 `FLASH_EraseInitTypeDef` 的文件，每个变量都要有 `.VoltageRange =`，否则报红（`$CORE_REPO/tests/check_no_sector15_writes.py`）。原来那条只看「写 flash 且点名扇区 15」，这次代码点名的是扇区 6，抓不到。

这块板的校准值还没写过（[TODO-fixture.md](../../../work/TODO-fixture.md) #28 未做），扇区 7 里没丢校准值。

## 引出了什么新的未知

没有。
