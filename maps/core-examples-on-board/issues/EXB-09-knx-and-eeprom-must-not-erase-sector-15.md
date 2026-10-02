# KNX 和 EEPROM 往 flash 存数据时不能擦扇区 15

Type: grilling
Opened: 2026-09-29
Status: resolved
Blocked by: -

## Question

`OpenPLC_KNX` 的应用 NVM 写死在 `0x081E0000`（`knx_config.h:94-97`，`KNX_SelfTest.ino:76` 就会写），上游 `EEPROM` 库也自动选中这个扇区（`stm32_eeprom.c:40-43`）；而扇区 15 装着校准值和固件 metadata（[SECTOR-15.md](../../../docs/modules/M1/SECTOR-15.md)），擦了之后下次上电 bootloader 停在等重传、校准值要回工装重写。KNX 应用 NVM 挪到哪、`EEPROM` 库是删掉、禁用还是挪扇区，由谁来防止以后再有代码写进扇区 15。

**用户 2026-09-30 已定一半：本板不提供模拟 EEPROM**（板上没有 EEPROM 芯片，`$HW/Production/Bridge/1436_01_SCHAE-BR.xlsx` 里存储器件只有 SDRAM 和 microSD 卡座），`EEPROM` 库连同 8 个例程删掉。**KNX 两块数据用户同日定方案 B+**：应用配置（约 80 字节）和协议栈数据（4 KiB）都放扇区 14（`0x081C0000`，仍属 app 区），保存时两块一起读出、擦、写回；只有链接了 `OpenPLC_KNX` 的程序在编译时检查不超过 1664 KiB，不用 KNX 的程序仍是 1792 KiB；selfcheck 加一道扫描，core 里有代码写扇区 15 就报错。本票按「一个会话只关一张」留到下个会话写 `## Answer` 关掉。

⚠️ **实施时发现（2026-09-30）**：板卡包链接脚本实际只给 app 1,703,936 B（`LD_MAX_SIZE` 已是 app 上限，`ldscript.ld:54` 又减一次 `LD_FLASH_OFFSET`），所以今天任何程序都到不了扇区 14。用户同日定改回 1,835,008 B，改了之后 B+ 的构建检查才真正起作用；事实写在 [BOOTLOADER-PROJECT-LAYOUT.md](../../../docs/build/BOOTLOADER-PROJECT-LAYOUT.md)「Flash 分区」。

## 怎么算答完

定下 KNX 应用 NVM 和 `EEPROM` 各自的去处，以及一道能自动发现「有代码往扇区 15 写」的检查；改完后在真板上跑 `KNX_SelfTest`，扇区 15 逐字节不变。

## Answer

2026-09-30 定（用户；2026-10-03 补记关票）。本板不提供模拟 EEPROM：板上没有 EEPROM 芯片，`EEPROM` 库连同 8 个例程删掉。KNX 两块数据按方案 B+ 放扇区 14（`0x081C0000`，仍属 app 区），保存时两块一起读改写；板卡包给 app 的上限改回 1,835,008 B，构建检查才真正起作用（见 [BOOTLOADER-PROJECT-LAYOUT.md](../../../docs/build/BOOTLOADER-PROJECT-LAYOUT.md)）。P19 盯住板卡包里没有代码写扇区 15。

## 引出了什么新的未知

没有。
