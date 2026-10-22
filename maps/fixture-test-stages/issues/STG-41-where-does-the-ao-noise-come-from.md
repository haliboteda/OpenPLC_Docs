# AO 端子上的噪声从哪来

Type: task
Opened: 2026-10-16
Status: open
Blocked by: -

## Question

MCU 驱动 AO（DAC → XTR111）时端子上有噪声；直接给 XTR111 输入加信号时没有（用户 2026-10-16 实测）。噪声来自 MCU 侧的哪一项：数字活动、DAC 输出缓冲、VREFBUF，还是 DAC 关掉后仍在的板上耦合？

已知前提：板上没有外部基准，VREF+ 只有退耦，VREFBUF 必须开（[HARDWARE-FACTS.md](../../../docs/hardware/HARDWARE-FACTS.md)「模拟量：没有外部基准，必须使能片内 VREFBUF」）；DAC 缓冲开（R17 / R18 1 kΩ 对地）、不用触发、只在 start / set 时写（`$BOOT/TestCase/common/port_dac.c`）。

## 实验

实验方案用户 2026-10-16 定。每个实验由一条临时命令 `pt.aodiag` 做，`$PORTTOOL/TestCase/tools/aodiag.py` 逐个带着跑。

| 实验 | 板子做什么 | 和 E0 比只差 |
|---|---|---|
| E0 | AO 设定值，固件照常跑（中断开着，CPU 忙等） | 基线 |
| E1 | 设好 DAC 后进安静窗口：屏蔽全部中断、停 HAL 时基（TIM6）和 SysTick、以太网起来过就停 ETH DMA；WFI 睡 N 秒，由 TIM2 单次定时唤醒；窗口里串口不发一个字节 | 没有数字活动 |
| E2 | E1 + DAC 输出缓冲关 | 缓冲 |
| E3 | E1 + VREFBUF 换档 2.5 / 2.048 / 1.8 / 1.5 V（一次一档） | 基准电压。DAC 码不变，所以 PA4 电压按比例变 |
| E4 | AI1 每 1 ms 转换一次 | ADC 活动 |
| E5 | 控制串口每 10 ms 发一行固定字符串 | UART 活动 |
| E6 | DAC 通道关掉，PA4 只剩 1 kΩ 下拉 | 没有 DAC 输出 |

每个实验开始前停掉所有会话；结束后 VREFBUF 回 2.5 V、AO 回 0 mV（0 时缓冲关，决策 152）。

## 测哪里

示波器 AC 耦合，量每处的 Vpp 和主频率：

| 测点 | 是什么 |
|---|---|
| PA4（AO2 是 PA5） | DAC 输出脚，XTR111 的输入 |
| TP3 | VREF+ |
| AO 端子（AO1 D14，AO2 D15） | 用户看到噪声的地方 |

## 怎么判读

| 看到 | 说明 |
|---|---|
| E1 没有、E0 有 | 来自 MCU 数字活动；再看 E4、E5 哪个把它带回来 |
| E1 仍有，E2 没有或明显变小 | 来自 DAC 输出缓冲 |
| E1 仍有，TP3 上同样有，E3 随档位变 | 来自 VREFBUF |
| E6 仍有 | 不是 DAC 产生的，是耦合进 PA4 / XTR111 输入的 |
| 全和 E0 一样 | 不是这几项，回到这张票补实验 |

**测不到的**：安静窗口里仍在跑的有 TIM2 自己、HSE / PLL、SDRAM 自刷新、以太网 PHY 和 USB PHY 自己的时钟。E2 时 DAC 无缓冲直接带 1 kΩ，PA4 直流电平会大幅下降（具体值没算过）。E6 时 PA4 是否真的高阻，看它是否落到约 0 V。

## 临时代码

找到原因后全部删掉，`PORTTOOL_VERSION` 不为它升号：

- `$BOOT/TestCase/porttool/porttool_aodiag.c` / `.h`：命令解析与实验流程
- `$BOOT/TestCase/common/port_aodiag.c` / `.h`：安静窗口、DAC 缓冲与开关、VREFBUF 换档
- `$BOOT/TestCase/porttool/porttool.c` 的 `pt.aodiag` 一行分派、`porttool.h` 命令表一行
- `$PORTTOOL/src/simboard/c/stubs/aodiag_stub.c` 和 `build.py` 里的两行
- `$PORTTOOL/TestCase/tools/aodiag.py` 和只给它用的 `common.py`（删完 `$PORTTOOL` 里就没有 Python 了，决策 149）

`pt.aodiag` 不进 `pt.caps`，面板不用它。

## 实测结果（2026-10-16，真板 UID …0029，AO1 电流档，端子接 470 Ω，用户用万用表量电阻两端）

| 状态 | 读数 |
|---|---|
| DAC 缓冲开，输出 0（复位后、或任何非零值回到 0） | 76–78 mV（0.16 mA） |
| DAC 缓冲关，输出 0 | 0.5 mV |
| DAC 通道关 | 0.5 mV |
| 缓冲开，1000 mV / 512 mV | 4.54 V / 2.34 V，读数不跳 |
| 缓冲关，512 mV | 0.166 V：带不动 R17 的 1 kΩ |

**结论**：用户说的「噪声」是 0 mA 时 0.16 mA 的偏移，来自 DAC 输出缓冲开着时到不了 0 V（推算 DAC 脚约 16 mV）；不是数字活动，也不是 XTR111 之后的电路。缓冲必须开，否则带不动 1 kΩ 负载。万用表上看不到读数跳动，示波器没量。改法：设 0 时关缓冲、非 0 时开（[决策 152](../../../docs/tables/DECISIONS.md)）。

⚠️ 诊断代码自己的问题：E2 关掉缓冲后，恢复时在通道开着的情况下改缓冲位，没生效，缓冲一直关到复位；实验中途几次 0.5 mV 是这个原因。

## 怎么算答完

E0–E6（E3 四档）在真板子上各跑一次，读数在 `$PORTTOOL/Output/aodiag/` 的 CSV 里；按上面的判读表写出噪声来自哪一项（或都不是）；上面列的临时代码删掉。
