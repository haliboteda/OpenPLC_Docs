# 给用户的接口统一成一种约定

Type: grilling
Opened: 2026-10-13
Status: resolved
Blocked by: -

## Question

用户 2026-10-13：「我希望给用户的接口和类是一致的，统一的，简约的。」KNX 已定为只留一个对象 `KNX`（[决策 109](../../../docs/tables/DECISIONS.md)）。其他库只读审查的结果（`$CORE` = `open_plc_arduino`）：

| 问题 | 例子 | 位置 |
|---|---|---|
| 同一件事两个入口 | `openplcResetCause()` 和 `openplc_reset_cause()` 都公开 | `libraries/OpenPLC_Ports/src/OpenPLC_Ports.h:31,38`、`openplc_reset.h:217,220` |
| 内部头文件漏给用户 | 以太网例程要 include 构建用的 `OpenPLC_Net_Autostart.h`，只有 snake_case C 函数，另带 14 个 `openplc_lwip_*` 统计函数 | `libraries/OpenPLC_Net/src/OpenPLC_Net_Autostart.h:237-256`、`Ethernet_IP.ino:12` |
| 串口四种叫法 | `Serial`（USB）、`Serial4`（扩展口）、`Serial_Test`（RS232，决策 100 定的主输出口）、RS485 要用户自己 `new HardwareSerial` 并手动翻方向脚 | `cores/arduino/main.cpp:54`、`RS485_Echo.ino:13-21` |
| 引脚常量两套风格 | `DIN_1` `DOUT_1` `REL_1` 对 `RS232_TX_Pin` `RS485_DIR_Pin` `SDMMC_CD_Pin`；端子印 RY1、常量叫 `REL_1`；系统 LED 没名字，例程写 `PE2` | `variants/STM32H7xx/H743/variant_PLC_H743.h:180-267,411` |
| 前缀风格不一 | `calib_status_t` / `CALIB_OK` 无前缀，`OPENPLC_RESET_*` 有；YMODEM 函数 camelCase、类型 snake_case | `openplc_calib.h:137-184`、`openplc_ymodem.h:244-269` |
| SD 检测脚要用户自己传 | `SD.begin(SDMMC_CD_Pin)`，默认是「不检测」 | `libraries/OpenPLC_SD/src/OpenPLC_SD.h:67` |

| 做法 | 约定 | 改动面（grep 实数） | 推荐 |
|---|---|---|---|
| A 每个端口一个对象 | `RS232` `RS485` `CAN` `SD` `SDRAM` `KNX` `Net` `AI` `AO` `Board`，一律 `begin()` | B 的全部，再加模拟量（`$CORE` 8、文档 4、PortTool 1 处注释）和复位原因（`$CORE` 5、`$TEST` 1、文档 1） | |
| B 有状态的用对象，无状态的用 `openplcXxx()` | 对象：`RS232`（取代 `Serial_Test`）、`RS485`（薄类，内管方向脚）、`CAN` `SD` `SDRAM` `KNX` `Net`；自由函数只留无状态的板级调用（AI/AO、复位原因、VREF、YMODEM），snake_case 从用户头文件里拿掉；引脚统一一种后缀 | `Serial_Test` 改名：`$CORE` 30、`$TEST` 8、文档 12；网络 `$CORE` 5、文档 2；RS485 `$CORE` 3、文档 1；`SD.begin` `$CORE` 6、文档 4 | ✅ SD、SDRAM、CAN 已是「对象 + `begin()`」；模拟量本来无状态，硬套对象多一层 |
| C 只修文档和漏出来的内部名 | 不改名 | 约 5 个文件 | 达不到「一致」 |

跨仓镜像（校准区格式、AI 换算常数、`udp_server.c` 等、`ethernetif.c`、`IAP_boot_handoff`）、FixtureDemo 的路径、两个 `*_Autostart.h` 文件名、`OPENPLC_APP_VERSION` 都不动（[ARCHITECTURE.md](../../../docs/repo/ARCHITECTURE.md) 镜像表，P2 检查）。

## 怎么算答完

用户选定一种；按它先改 [M3-app-runtime.md](../../../docs/modules/M3-app-runtime.md) 写下约定，再改代码、例程、README、测试；P5 全过、P3 一致。`Serial_Test` 改名排在 KNX 合并落地之后（两边改同一批 KNX 文件）。

## Answer

2026-10-13 定：B（用户：「按推荐来」）。有状态的外设一个对象、`begin()` 起：`RS232`（取代 `Serial_Test`）、`RS485`（内管方向脚）、`CAN` `SD` `SDRAM` `KNX` `Net`；无状态的板级调用用 `openplc` 前缀 camelCase 函数，snake_case 的 `openplc_*` 不进用户 include 的头文件；引脚常量统一不带 `_Pin` 后缀。约定先写进 M3，再改代码；排在 IAP 代码精炼之后。

## 引出了什么新的未知

没有。实施记在 [TODO.md](../../../work/TODO.md) #59。
