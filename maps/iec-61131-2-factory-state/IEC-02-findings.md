# 每个输出在各时刻的状态（IEC-02 调研记录）

2026-09-28 读原理图、网表、代码得出，**没有一条是实测**。bootloader 按决策 71 改过之后的版本。

⚠️ **2026-10-03 按决策 81 改了代码（未上板验证）**：bootloader 一开机就把 DO1–DO8 置 0、AO 的 PA4 / PA5 拉低，交权时再做一遍，保持到 sketch 第一次写。下表 DO、AO 两行是改后的预期。

## 输出 × 时刻

| 输出 | 上电、代码未跑 | bootloader 在跑 | 交权 → `setup()` 前 | 掉电 |
|---|---|---|---|---|
| DO1–DO8（VNQ5160K-E） | 大概率断开：MCU 脚高阻，靠 VNQ 输入脚内部下拉（**未核实**），只到 bootloader 第一批语句为止 | 断开：`safe_outputs_init()` 置 0（`$BOOT/IAPServer/safe_outputs.c`，决策 81） | 断开：`HAL_DeInit()` 之后再置 0 一次，core 不碰，直到 sketch 写 | 断开（同上电） |
| RY1–RY6 | 断开：栅极 33k 下拉（LowerDeck 网表 R3–R8） | 断开：`MX_GPIO_Init` 先写低再切输出，开机不再动（决策 71） | 断开 | 断开：线圈接 5V0，单线圈低边驱动，无自锁 |
| AO1–AO2（XTR111） | **不确定**：OD 脚 10k 接地，输出恒使能；VIN 经 10k 接 PA4/PA5，脚高阻时悬空，只到 bootloader 第一批语句为止（几毫秒，待示波器实测） | 0 mA：`safe_outputs_init()` 把 PA4 / PA5 拉低（决策 81） | 0 mA：`HAL_DeInit()` 之后再拉低一次，直到 sketch 开 DAC | **不确定**：MCU 已复位而 24 V 还在时 VIN 悬空（待示波器实测） |
| 系统灯 PE2 | 灭 | 窗口快闪，恢复出厂就绪常亮，之后灭 | 灭（`HAL_DeInit`），变体未定义 `LED_BUILTIN` | 灭 |

## 看门狗与电源监视

| 问题 | 结论 | 出处 |
|---|---|---|
| app 开 IWDG 吗 | 没开，core 和变体都不调用 `IWatchdog` | `open_plc_arduino` grep |
| bootloader 交权时 IWDG 在跑吗 | 没有，HAL IWDG 模块注释掉 | `$BOOT/Core/Inc/stm32h7xx_hal_conf.h:64` |
| 欠压检测 | 两边都没配 PVD / BOR | grep |
| RUN / STOP 模式 | 标准不强制，「as applicable」 | IEC 61131-2:2003 2.5 |

## 对照 IEC 61131-2:2003

| 条款 | 判断 | 理由 |
|---|---|---|
| 6.3.1.3 断电时无异常 | 未知 | DO / RY 会落到断开；AO 在那段时间没定义 |
| 6.3.1.4 上电时无异常 | DO / RY 满足（决策 71 之后）；AO 不满足 | AO 从上电到 sketch 开 DAC 之前没有确定值 |
| 6.3.2 欠压进入预定状态 | 不满足 | 没有欠压检测，预定状态没写 |
| 7.9 / 7.11.3 厂商写明输出行为 | 不满足 | 手册里没有 |
| 5.8 看门狗、电源监视、报警输出 | 不满足 | 看门狗没开，电源没监视，没有报警输出 |

## 没核实的

- VNQ5160K-E 输入脚悬空时是否断开、欠压关断阈值（数据手册没下载到）—— DO 的结论挂在这条上
- AO 的锡桥 JP1–JP4 出厂桥没桥；TLC7703 复位阈值；5V0 和 3V3 的掉电先后
- 芯片选项字节 `IWDG1_SW`（硬件看门狗模式）

## 顺带发现：抄件和网表对不上（没改）

| 文件 | 写的 | 网表 |
|---|---|---|
| `Hardware/LowerDeck_overview.txt` 第五节 | R3–R8 是「33k 限流电阻」 | 栅极到地的下拉 |
| `open_plc_arduino/variants/STM32H7xx/H743/variant_PLC_H743.h:224-225` | `AOUT_x_EF` 是「fault/enable」 | 只是故障标志，OD 已硬接地 |
| 同文件 `:187-188` | `REL_OUTA/B` 是「coil-A/B polarity」 | 单线圈，无极性 |
| 同文件 `:234` | `KNX_PROG_KEY` 低有效 | [HARDWARE-FACTS.md](../../docs/hardware/HARDWARE-FACTS.md) 记为按下为高 |
