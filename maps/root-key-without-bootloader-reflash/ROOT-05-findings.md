# ROOT-05 调研结论：备份 SRAM 能不能当回收暂存区、128 KiB 扇区擦多久

票：[ROOT-05 根区放在哪、写满怎么回收](issues/ROOT-05-where-the-built-in-root-lives-and-how-it-is-updated.md)。
出处只用 ST 原件：**RM0433 Rev 8**（2023-01）、**DS12110 Rev 11**（2026-01，STM32H742xI/G、H743xI/G）。

## 一、备份 SRAM（4 KiB，`0x38800000`）

| 问题 | 结论 | 出处 |
|---|---|---|
| 只有 VBAT、VDD 断开时内容还在不在 | **在，前提是 `PWR_CR2.BREN`=1**；BREN=0 时只在 Run / Stop 下可用，进 Standby 或 VBAT 模式内容丢失 | RM0433 §6.4.4「Backup RAM」、§6.8.3 PWR_CR2 bit 0 BREN；DS12110 §3.3.2、§3.19 |
| 固件要打开什么 | ① `RCC_AHB4ENR.BKPRAMEN`（bit 28）开时钟；② `PWR_CR1.DBP`（bit 8）置 1 解除备份域写保护 —— BREN 本身也受它保护；③ 置 `PWR_CR2.BREN`（bit 0）；④ 等 `PWR_CR2.BRRDY`（bit 16）=1 之后写入的数据才保证在 Standby / VBAT 下保持 | RM0433 §8.7.43、§6.8.1 PWR_CR1 bit 8、§6.8.3 |
| BREN 设一次能不能一直有效 | 能：`PWR_CR2` 不被系统复位、NRST、VDD POR、Standby 唤醒复位，只被 VSW POR 和 `VSWRST` 复位 | RM0433 §6.8.3 |
| RDP 1→0 回退 | **被擦**（和 RTC 备份寄存器一起） | RM0433 §4.5.3、§8.4.6 |
| tamper 事件 | 默认**被擦**；`RTC_TAMPCR.TAMPxNOERASE`=1 时不擦 | RM0433 §46.3.15、§46.6.16 |
| 软件备份域复位 `RCC_BDCR.BDRST` | 不影响备份 RAM | RM0433 §8.4.6 |
| VSW（VDD/VBAT 切换后的电源）掉出工作范围 | 内容不再有效 | RM0433 §8.4.6 |
| Standby 唤醒 | 保持（BREN=1 时） | RM0433 §6.4.4；DS12110 §3.3.2 |
| 系统复位（NRST、IWDG、软复位） | **没核实**：RM0433 §8.4.6 列出的备份 RAM 复位途径只有 RDP 回退和 tamper，没有系统复位，但 ST 文档里没有一句直接写「备份 SRAM 不被系统复位清除」（这句话只写给了 RTC 备份寄存器，§46.3.15、DS12110 §3.29） | — |
| 本板 VBAT 接法 | **没核实**（要查 `$HW` 原理图，不在本次 ST 文档范围） | — |

⚠️ **RM0433 自身两处对不上**：§6.4.4 写 tamper「不整体擦除备份 RAM，而是读保护，要先擦（对它写一个 0）才能重新访问」；§46.3.1、§46.3.15、§46.6.16 写 tamper 默认擦除备份 SRAM。对回收方案的影响相同：tamper 之后暂存内容不可用。

## 二、128 KiB 扇区擦除时间

DS12110 Rev 11 **表 43**（§6.3.11，rev Y 芯片）与**表 140**（§7.3.11，rev V 芯片）数值相同，条件 TJ = −40…125 °C，由特性测试保证：

| 并行度（`FLASH_CR1/2.PSIZE`） | tERASE128KB 典型 | 最大 | 允许的编程电压 Vprog |
|---|---|---|---|
| x8（`00`） | 2 s | 4 s | 1.62–3.6 V |
| x16（`01`） | 1.8 s | 3.6 s | 1.62–3.6 V |
| x32（`10`） | 1.1 s | 2.2 s | 1.62–3.6 V |
| x64（`11`） | 1 s | 2 s | 1.8–3.6 V |

PSIZE 编码见 RM0433 §4.3.9 表 18；并行度同样作用于扇区擦除。本板芯片是 rev Y 还是 rev V **没核实**，但两张表数值一致，不影响结论。

> ✅ **结论**：备份 SRAM 可以当回收暂存区，但只在 VBAT 真的有电、且固件按 BKPRAMEN → DBP → BREN → 等 BRRDY 的顺序打开时，内容才能扛过 VDD 掉电；RDP 1→0 回退和 tamper 都会擦掉它，系统复位下是否保持 ST 文档没有明说。擦一个 128 KiB 扇区在 x64 并行度下典型 1 s、最坏 2 s，x8 下最坏 4 s，这就是回收时掉电窗口的量级。
