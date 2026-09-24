# IDE-03 结论 · CAN 和 SD 卡在 Arduino 下最少要补什么

票：[issues/IDE-03-what-can-and-sd-need-in-arduino.md](issues/IDE-03-what-can-and-sd-need-in-arduino.md)
调查日期：2026-09-25。只读代码 + 在临时目录里用 arduino-cli 编译试验草图，**没上板子，没改任何仓库文件**。

路径缩写：`$CORE_REPO` = [`open_plc_arduino`](../../../open_plc_arduino)，`$BOOT` = [`open_plc_cube_ide`](../../../open_plc_cube_ide)，
`VARIANT` = [`$CORE_REPO/variants/STM32H7xx/H743/`](../../../open_plc_arduino/variants/STM32H7xx/H743)，
`UP/` = 从 Arduino 官方库索引下载到临时目录的上游库（本机没装任何第三方库，见下文「本机现状」）。
本机安装的 `0.1.3-pre` 板卡包 `variants/STM32H7xx/H743/` 和 `stm32yyxx_hal_conf.h` 与 `$CORE_REPO` 逐字节相同（`diff -rq` 为空），所以编译结果对仓库成立。

## 结论

> ✅ **CAN：没有能用的上游库，照 `$BOOT/TestCase/common/port_can.c` 写一层薄封装。** 最少改 1 个核心文件（变体里打开 `HAL_FDCAN`），加 1 个库目录。

> ✅ **SD：用上游 `STM32duino STM32SD` + `FatFs`，但变体里的 `PinMap_SD[]` 必须先裁到 3 个脚。** 不裁的话，这个库在本核心版本上会把 27 个脚全切成 SDMMC 功能，包括 CAN_TX、RS232、RS485、KNX。

> ✅ **两条都不限制用户 app**：都是轮询、不占中断向量、不定义强符号的 `HAL_*_MspInit`，用户仍可 `-DHAL_xxx_MODULE_DISABLED` 或自己直接调 HAL。

## 本机现状（查过的地方）

| 位置 | 有什么 |
|---|---|
| `C:\Users\WhoamIamwhO\AppData\Local\Arduino15\libraries` | 不存在 |
| 用户库目录 `d:\Users\WhoamIamwhO\Documents\Arduino\libraries`（`arduino-cli.yaml` 的 `directories.user`） | 空（只有 `.vscode`）；`arduino-cli lib list` = `No libraries installed.` |
| 板卡包自带库 [`$CORE_REPO/libraries/`](../../../open_plc_arduino/libraries) | 没有 CAN、SD、FatFs 相关的库 |
| 本机缓存的 `Arduino15/library_index.json` 里的候选 | `STM32duino STM32SD 1.5.0`（依赖 `FatFs 4.0.4`）、`STM32_CAN 1.2.2`、`ACANFD_STM32 1.1.2-rc1`、`ACAN_STM32 1.0.1` —— 下载到临时目录试过，结果见下两节 |

## 两条共同的前提

| 事实 | 出处 | 影响 |
|---|---|---|
| 核心是 STM32duino **2.4.0** 的分叉 | [`$CORE_REPO/cores/arduino/stm32/stm32_def.h:8-10`](../../../open_plc_arduino/cores/arduino/stm32/stm32_def.h) | STM32SD 走老代码路径（见 SD 一节） |
| 编的是 `PeripheralPins_PLC_H743.c`，不是通用那份 | [`$CORE_REPO/boards.txt:58`](../../../open_plc_arduino/boards.txt)（`-DCUSTOM_PERIPHERAL_PINS`）；`VARIANT/PeripheralPins_PLC_H743.c:21` | 要改引脚表就改这份 |
| Arduino 下时钟是 **HSI**，HSE 被关掉 | [`VARIANT/generic_clock.c:38-48`](../../../open_plc_arduino/variants/STM32H7xx/H743/generic_clock.c)（HSI 64 MHz → PLL1，PLL1Q = 192 MHz）；`system/Drivers/CMSIS/Device/ST/STM32H7xx/Source/Templates/system_stm32h7xx.c:200-201` 复位时清 `HSEON` | TestCase 的时钟前提（HSE 常开，bootloader [`Core/Src/main.c:526-532`](../../../open_plc_cube_ide/Core/Src/main.c)）在 Arduino 下不成立，封装要自己开 HSE |
| 草图可以用 `build_opt.h` 给整个构建加宏 | [`$CORE_REPO/platform.txt:25,112-113`](../../../open_plc_arduino/platform.txt)；[`system/extras/prebuild.sh:38-44`](../../../open_plc_arduino/system/extras/prebuild.sh) | 不改核心也能临时打开 HAL 模块 |

## CAN（FDCAN1，PB9 / PI9）

### 现状

| 项 | 事实 | 出处 |
|---|---|---|
| HAL 模块 | **没开。** 变体只开了 DAC/ADC/ETH/QSPI/SD/SDRAM；核心把 `HAL_FDCAN` 列在「Unused」里 | [`VARIANT/variant_PLC_H743.h:487-510`](../../../open_plc_arduino/variants/STM32H7xx/H743/variant_PLC_H743.h)；[`cores/arduino/stm32/stm32yyxx_hal_conf.h:135,147`](../../../open_plc_arduino/cores/arduino/stm32/stm32yyxx_hal_conf.h) |
| HAL 源文件 | 已经在，只差宏 | [`libraries/SrcWrapper/src/HAL/stm32yyxx_hal_fdcan.c`](../../../open_plc_arduino/libraries/SrcWrapper/src/HAL/stm32yyxx_hal_fdcan.c) |
| 引脚表 | `PinMap_CAN_RD` 有 `PI_9`，`PinMap_CAN_TD` 有 `PB_9`，都 AF9；开了宏就生效 | `VARIANT/PeripheralPins_PLC_H743.c:440-461` |
| 引脚名 | `CAN_TX_Pin` / `CAN_RX_Pin` 已定义 | `VARIANT/variant_PLC_H743.h:252-255` |
| 收发器 | ISO1044BDR，没有 STB/EN 脚，软件不用管 | [HARDWARE-FACTS.md:293](../../docs/hardware/HARDWARE-FACTS.md) |
| 板上跑通过的代码 | 时序表按 HSE = 25 MHz 整除（125k/250k/500k/1M），轮询收发，不设过滤器 | [`$BOOT/TestCase/common/port_can.c:30-35`](../../../open_plc_cube_ide/TestCase/common/port_can.c)（时序表）、`:95-127`（时钟+GPIO）、`:129-192`（Init/Start） |

### 上游库逐个核对

| 库 | 能不能用 | 原因 | 出处 |
|---|---|---|---|
| `ACANFD_STM32 1.1.2-rc1` | ❌ | 只认 `ARDUINO_NUCLEO_H743ZI2` 等几块 Nucleo，本板编译直接 `#error "Unhandled Nucleo Board"`（**实测**）；H743 的 RX 脚表没有 `PI_9`；按「FDCAN 时钟 = PCLK1」算位时序，本板 PLL1Q 192 MHz ≠ PCLK1 120 MHz | `UP/ACANFD_STM32-1.1.2-rc1/src/ACANFD_STM32.h:7-21`；`…NUCLEO_H743ZI2-objects.h:25-28`；`…NUCLEO_H743ZI2-settings.h:24-26` |
| `STM32_CAN 1.2.2`（pazi88） | ❌ | 只支持 bxCAN（`HAL_CAN_MODULE_ENABLED`），源码里没有 FDCAN；H7 没有 bxCAN | `UP/STM32_CAN-1.2.2/STM32_CAN.h:15-16` |
| `ACAN_STM32 1.0.1` | ❌ | 只支持 NUCLEO-F303K8 / L432KC（索引描述） | `library_index.json` |

### 做法对比

| | C1 薄封装库 + 变体开 HAL（**推荐**） | C2 不改核心，例程自带 HAL 代码 | C3 分叉 ACANFD_STM32 |
|---|---|---|---|
| 改哪些文件 | `variant_PLC_H743.h` 加 3 行 `HAL_FDCAN_MODULE_ENABLED`（照 `:502-504` 的 SD 写法）；新增 `libraries/OpenPLC_CAN/`（`src/*.h/*.cpp` 移植 `port_can.c`、`library.properties`、一个例程），结构照 [`libraries/OpenPLC_SDRAM/`](../../../open_plc_arduino/libraries/OpenPLC_SDRAM) | 0 个核心文件；例程目录里放 `build_opt.h`（`-DHAL_FDCAN_MODULE_ENABLED`）+ 约 50 行 HAL 调用 | 加板子分支、加 PI9、改时钟计算，外加一份第三方代码要维护 |
| 编译验证 | 未做（要改仓库）；C2 编过即说明 HAL + 引脚表 + `enableClock(HSE_CLOCK)` 这条路在本核心上能链接 | ✅ **实测编过**：89 500 B flash，`HAL_FDCAN_Init`、`PinMap_CAN_TD/RD` 均已链入 | 未做 |
| 例程好不好读 | 好：`CAN.begin(500000)` / `write` / `read` | 差：用户第一眼看到的是 HAL 结构体 | 好 |
| 风险 | 低，代码来自板上跑通的 `port_can.c` | `build_opt.h` 在 IDE 里「文件 → 示例」打开后是否随例程一起复制，**没验证** | 高 |

**C1 的封装要守的三条**（否则就限制了用户 app）：

| 规矩 | 为什么 |
|---|---|
| 轮询，不定义 `FDCAN1_IT0/IT1_IRQHandler` | 链接结果里这两个是弱符号（实测 `nm`），留给用户 |
| 不定义 `HAL_FDCAN_MspInit`，时钟和 GPIO 在 `begin()` 里直接配（`port_can.c` 本来就这样） | 强符号会和用户自己的冲突 |
| `begin()` 里先 `enableClock(HSE_CLOCK)` 再选 `FDCANSEL = HSE`，并对外给出句柄（照 `PortCan_Handle()`） | Arduino 下 HSE 是关的（见「共同前提」）；[`libraries/SrcWrapper/src/stm32/clock.c:124-129`](../../../open_plc_arduino/libraries/SrcWrapper/src/stm32/clock.c)。给句柄让用户能用封装没包的功能（过滤器、FD） |

`FDCANSEL` 是 FDCAN1/2 共用的，改成 HSE 不影响别人：本板 FDCAN2 没有可用引脚（[HARDWARE-FACTS.md:292](../../docs/hardware/HARDWARE-FACTS.md)）。

## SD 卡（SDMMC1，1 位，PC12 / PD2 / PC8，检测 PE6）

### 现状

| 项 | 事实 | 出处 |
|---|---|---|
| HAL 模块 | **已开** | `VARIANT/variant_PLC_H743.h:502-504` |
| HAL 源文件 | `stm32yyxx_hal_sd.c`、`_sd_ex.c`、`ll_sdmmc.c`、`ll_delayblock.c` 都在 | [`libraries/SrcWrapper/src/HAL/`](../../../open_plc_arduino/libraries/SrcWrapper/src/HAL)、`…/src/LL/` |
| 引脚名 | `SDMMC_CLK/CMD/D0/CD_Pin` 已定义 | `VARIANT/variant_PLC_H743.h:262-266` |
| **引脚表** | `PinMap_SD[]` 是芯片全集，**27 条**，含 SDMMC1 的 D1–D7、CKIN、CDIR、DIR 脚和整个 SDMMC2 | `VARIANT/PeripheralPins_PLC_H743.c:610-641` |
| 内核时钟 | `SDMMCSEL = PLL1Q = 192 MHz`；HAL 在宽总线配置时把分频钳到 ≤ 25 MHz（`NSPEED_CLK_DIV = 4` → 24 MHz） | `VARIANT/generic_clock.c:89`；`system/Drivers/STM32H7xx_HAL_Driver/Src/stm32h7xx_hal_sd.c:2462-2520`；`Inc/stm32h7xx_ll_sdmmc.h:697` |
| 检测脚 | PE6，低 = 已插入 | [HARDWARE-FACTS.md:415](../../docs/hardware/HARDWARE-FACTS.md) |
| 板上跑通过的代码 | 1 位、`ClockDiv = 0`、PLL2 50 MHz 内核时钟，只配 3 个脚，轮询读写，FatFs R0.12c 开 exFAT | [`$BOOT/TestCase/SD/sd_test.c:42-72`](../../../open_plc_cube_ide/TestCase/SD/sd_test.c)（时钟+GPIO）、`:135-140`（Init）；[`TestCase/common/ffconf.h:214`](../../../open_plc_cube_ide/TestCase/common/ffconf.h) |

### 上游 STM32SD 在这块板上的问题

| 问题 | 出处 | 不修会怎样 |
|---|---|---|
| **核心 ≤ 2.5.0 时，`BSP_SD_MspInit` 把 `PinMap_SD[]` 里每一个脚都切成 SDMMC 复用功能**；`BSP_SD_MspDeInit` 同样全部复位 | `UP/STM32duino_STM32SD-1.5.0/src/bsp_sd.c:466-475`、`:532-540` | `SD.begin()` 一调，下列脚被抢走：`PB9` CAN_TX、`PC10/PC11` RS232（也是调试串口 USART3）、`PD6` RS485_RX、`PC6` DIN_1、`PB14` KNX_TX、`PD7` KNX_TP_OK、`PG11` KNX_PROG_LED、`PA0` TEMP_SCPROT、`PB4` SPI6_MISO（`variant_PLC_H743.h:206,228,232-235,241-249,254,271`）。**没上板验证，是读代码得出的** |
| 默认 4 位总线 | `bsp_sd.c:103-105`、`:326` | D1–D3 没接，宽总线配置后读写会出错。加 `SD_BUS_WIDE=SDMMC_BUS_WIDE_1B` 解决 |

### 做法对比

| | S1 上游 STM32SD + 变体裁引脚表（**推荐**） | S2 不改核心，例程里覆盖 `PinMap_SD` | S3 照 `sd_test.c` 自写封装 + 内置 FatFs |
|---|---|---|---|
| 改哪些文件 | `PeripheralPins_PLC_H743.c:610-641` 裁成 PC8/PC12/PD2 三条；`variant_PLC_H743.h` 加 `#define SD_BUS_WIDE SDMMC_BUS_WIDE_1B`；例程 `SD.begin(SDMMC_CD_Pin)` | 0 个核心文件；例程里写一个强符号 `const PinMap PinMap_SD[]`（3 条）+ `build_opt.h` 设 1 位 | 新库目录：`sd_test.c` 的初始化 + diskio 桥 + 一份 FatFs（约 7 个文件）+ Arduino 风格的 File API |
| 用户要装什么 | Library Manager 装 `STM32duino STM32SD`（自动带 `FatFs`） | 同左 | 不用装 |
| 编译验证 | S2 实测等价：✅ 编过，`PinMap_SD` 变成 4 条（`nm -S` = `0x30`，原来 `0x150`） | ✅ **实测编过**（106 572 B） | 未做 |
| 风险 | 低；以后核心升到 ≥ 2.6，要改成分信号的 `PinMap_SD_CK/CMD/DATA0`（`bsp_sd.c:135-267` 走新路径） | 每个用 SD 的用户草图都得抄这段，漏了就抢 27 个脚 —— **陷阱留给了用户** | 代码量最大，API 要自己设计 |

**S1 不限制用户 app**：库全程轮询（`bsp_sd.c:432-448`，无 IRQ、无 DMA，开 D-cache 也不受影响）；`HAL_SD_MspInit` 在链接结果里是弱符号（实测 `nm`）；`PinMap_SD` 在变体里是 `WEAK`，用户真要别的接法还能自己覆盖。裁掉的 24 条在本板上本来就没接到 SD 座。

## 没验证的

| 项 | 为什么没验 |
|---|---|
| 任何一条在真板子上的收发 / 读写 | 没有硬件 |
| Arduino 下 `enableClock(HSE_CLOCK)` 能起振、FDCAN 位时序准 | 需要上板；bootloader 下 HSE 25 MHz 能用是 `port_can.c` 已证明的 |
| SD 在 24 MHz（PLL1Q 分频）下稳定 | TestCase 跑的是 PLL2 50 MHz 内核、HAL 同样钳到 ≤ 25 MHz，频率接近但时钟源不同 |
| STM32SD 抢脚的实际后果（串口是否当场断） | 读代码推断，没跑 |
| STM32SD 的 FatFs 版本（R0.15，`ffconf_default_80286.h:234` 开 exFAT）对 TestCase 用过的卡的兼容性 | TestCase 用的是 R0.12c |
| `build_opt.h` 随 IDE 的「示例」菜单复制 | 只用 arduino-cli 编过 |
| SD 座是否有电平转换 / 收发器 | HARDWARE-FACTS 没有 SD 座一节；`sd_test.c` 没配任何收发器且上板跑通，所以按「直连 3.3 V」处理 |

## 下一步

实现归 [IDE-10（CAN 和 SD 卡：最小的库和例程）](issues/IDE-10-can-and-sd.md)，按上面 C1 + S1 做。
