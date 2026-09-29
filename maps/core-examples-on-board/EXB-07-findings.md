# EXB-07 调研结论：KNX / SDRAM 例程的引脚和本板对不对得上

回答 [EXB-07](issues/EXB-07-do-knx-and-sdram-examples-use-this-boards-pins.md)。2026-09-29，只读核实，未上板。

路径简写：`$HW` = `Hardware/`，`$CORE` = `open_plc_arduino/`，`FACTS` = `OpenPLC_Docs/docs/hardware/HARDWARE-FACTS.md`，
`xlsx` = `$HW/STM32H743IIK6_GPIO_ASSIGNMENT_Schaeffer_Bridge_20260822.xlsx`（管脚分配的权威），`KNXLIB` = `$CORE/libraries/OpenPLC_KNX/src/`。

## 结论

> ✅ 引脚号本身基本都对（PB14 / PA10 / PD7 / PH12 / PG9 / PG11，代码里的继电器 PI8 / PI10，RS232 的 PC10 / PC11 / PB10，AIN_1 = PC3_C）。
> 问题出在**例程头注释里的引脚写错**（继电器写成 PE6 / PE5）、**极性和外设写错**（PG9 实际高有效；STKNX 不是 UART 器件），
> 以及**用了引脚但板子上根本没接东西**（PG11 这根线上没有 LED，AIN_1 出厂跳线开路）。

最影响可用性的三条：

| # | 是什么 | 影响 | 出处 |
|---|---|---|---|
| 1 | `OpenPLC_KNX` 用 USART1 19200 8E1 驱动 STKNX；STKNX 是裸模拟 TP1 收发器，位时序要 MCU 用定时器产生 | 三个走 TP 的例程（KNX_Basic 的 TP 侧、KNX_TP_PingPong、KNX_TP_TxTest）在这块板上发不出合法 TP 帧；UART 空闲电平为高，按 FACTS 即 PB14 高 = 持续有源脉冲（未上板核实） | `KNXLIB/stm32h743_openplc_platform.cpp:118-139`；FACTS「KNX 接口」:342-357 |
| 2 | 4 个 KNX 例程用 `Serial_Test` 输出，但不拉高 `RS232_EN_Pin`（PB10） | RS232 收发器默认关断，端子上一个字节都没有（启动后几毫秒的电荷泵余电除外） | FACTS「PB10 拉低 = 整片关断」「默认是关的」:19-36 |
| 3 | SDRAM_DataLogger 用 `analogRead(AIN_1)` | JP5 出厂开路 → PC3_C 悬空；core 也不使能 VREFBUF / PC3SO → 录下来的不是端子信号 | FACTS「模拟输入前端」:242-259、「VREFBUF」:216-240；`grep VREFBUF` 在 `$CORE/cores`、`variants` 下无结果 |

## 表 1：逐引脚 / 串口对照

| 例程 | 引脚/串口 | 例程里写的 | 本板实际（出处） | 对不对 |
|---|---|---|---|---|
| KNX_Basic、KNX_IP_Test（头注释） | 继电器 0 | PE6（REL_1） | 代码实际用 PI8（`KNXLIB/knx_config.h:64-68`）；本板 PE6 = `SDIO1_CD`（SD 卡检测），继电器 1 = `RELAIS_1_PI8`（xlsx 行 128；`$HW/Production/LowerDeck/netlist.ipc` T7 栅极） | ❌ 头注释错，代码对 |
| KNX_Basic、KNX_IP_Test（头注释） | 继电器 1 | PE5（REL_2） | 代码实际用 PI10；本板 PE5 = `HSFET_8`（Digital Out 8），继电器 2 = `RELAIS_2_PI10`（xlsx 行 126、129；LowerDeck netlist T6） | ❌ 头注释错，代码对 |
| KNX_Basic（头注释） | 继电器所在板 | "Bridge MPU schematic" | 继电器 RY1–RY6 在 Lower Deck，端子 B01–B04（`$HW/LowerDeck_overview.txt:45-82`） | ❌ |
| KNX_Basic、KNX_SelfTest（代码） | 继电器极性 | SET = 线圈通电 | PI8 → T7（SI2356DS N-MOS 低边）栅极，R8 33k 下拉 → 高 = 吸合（LowerDeck netlist + `bom.csv`） | ✅ |
| KNX_Basic（头注释）+ 库 | 编程键 PG9 | pull-up，active-low，EXTI 下降沿 | PG9 = `KNX_Prog_KEY` = BOOT0 网；SW2 按下接 3V3，R58 10k 下拉 → **高有效**（Bridge 原理图 `1436_01_SCHAE-BR.pdf` p5；FACTS「PG9 就是 BOOT0 网」:104-116） | ❌ 极性反。库配内部上拉 + 下降沿 → 松手时才触发（按 FACTS 实测 PULLUP 下常态读 0 推断，未上板） |
| KNX_Basic / IP_Test / TxTest / PingPong | 编程 LED PG11 | "LED on PG11 lights" | PG11 = `KNX_Prog_LED`，经 Bridge 板间连接器到 Upper Deck J8-10 后**不接任何器件**；Bridge 上仅有的 LED 是 LED1/LED2（以太网）和 LED3 `HBEAT`（在 PE2）（Bridge p5 + Pick Place；`$HW/Production/UpperDeck/netlist.ipc` `/KNX_PROG_LED` 只有 J8-10） | ❌ 引脚号对，但板上没有这颗 LED |
| KNX_Basic（头注释）+ 库 | KNX TX PB14 | USART1 TX AF4 | PB14 = `KNX_TX`（xlsx 行 142）✅；但 STKNX 需要的是 TIM12_CH1 产生位时序，不是 UART（FACTS:342-346） | 引脚 ✅ / 外设 ❌ |
| KNX_Basic（头注释）+ 库 | KNX RX PA10 | USART1 RX AF7 | PA10 = `KNX_RX`（xlsx 行 143）✅；实为 TIM1_CH3 捕获、低有效、需内部上拉（FACTS:347, 358, 373）；库 `PA_10_ALT1` 未配上拉（未核实 `uart_init` 是否自带） | 引脚 ✅ / 外设 ❌ |
| KNX_SelfTest、KNX_TP_TxTest | TP bus-OK PD7 | HIGH = bus detected | PD7 = `KNX_OK`（xlsx 行 144），经 U11 光耦 + U15 反相器（UpperDeck netlist）；本板实测恒 LOW、不跟总线走，原因未查清（FACTS:348, 391） | 引脚 ✅ / 判据 未核实 |
| KNX_SelfTest、KNX_TP_TxTest、IP_Test | TP VCC-OK PH12 | HIGH = bus powered | PH12 = `KNX_VCC_OK`（xlsx 行 145），经 U10 + U14；实测拔插总线跟着变（FACTS:349, 389） | ✅ |
| KNX_IP_Test、PingPong、TxTest | `Serial_Test` | 输出口（IP_Test 头注释另写"USB CDC for Serial output"） | `Serial_Test` = USART3 AF7，PC10 / PC11 → MAX3221 → 端子 C05 / C06（`$CORE/cores/arduino/main.cpp:54`；xlsx 行 92-93；FACTS:57-63） | 引脚 ✅；未拉高 PB10 → ❌ 无输出 |
| KNX_SelfTest | `Serial` | "UART4 at 115200, routed to the debug connector" | 默认 USB 菜单 `CDCgen`（`$CORE/boards.txt:80`，`none` 已注释），`Serial` = USB CDC，不是 UART4（FACTS:86-90） | ❌ 头注释错 |
| SDRAM_Basic、SDRAM_DataLogger | `Serial_Test` + `RS232_EN_Pin` | C05 / C06，115200，先拉高 RS232_EN | 同上；`RS232_EN_Pin` = PB10 高有效（variant `:243`；xlsx 行 94；FACTS:19-30） | ✅ |
| SDRAM_Basic、SDRAM_DataLogger | SDRAM | 64 MB 外部 SDRAM | U6 AS4C32M16SB，512 Mbit = 64 MB（`$HW/Bridge_overview.txt:15,90`；FACTS:138） | ✅ |
| SDRAM_DataLogger | `AIN_1` | 一路模拟输入 | `AIN_1` = PC3_C（variant `:217`；xlsx 行 108 `AIN1_PC3_C`），端子 D12（`$HW/UpperDeck_overview.txt:108`）；JP5 出厂开路 → 引脚悬空；需 VREFBUF + PC3SO（FACTS:216-259） | 引脚 ✅ / 能不能读到信号 ❌ |

## 表 2：文件头 / 注释 / 输出文字与代码本身不一致

| 例程 | 位置 | 写的 | 代码实际 |
|---|---|---|---|
| KNX_TP_PingPong | `:2` 文件名 | `KNX_TP_Sender` | 文件是 `KNX_TP_PingPong.ino` |
| KNX_TP_PingPong | `:7-8` | 与 `ping_pong.py` mode 2（ping-pong）兼容 | 只发不收，没有 pong 逻辑；本工作区找不到 `ping_pong.py`（未核实是否在别处） |
| KNX_TP_PingPong | `:15` + `:21` | MASK 0x07B0（TP-only） | 板卡包构建参数已带 `-DMASK_VERSION=0x5780`（`$CORE/boards.txt:34`）；sketch 里的 `#define` 管不到库的 `.cpp` —— 实际生效的 MASK 未核实（未编译） |
| KNX_TP_PingPong | `:156-158` | "LED ON / LED OFF" | PG11 上没有 LED（见表 1） |
| KNX_TP_TxTest | `:4-6` vs `:23-27` | 头两段先说 0x5780、IP+TP 都开，再说改成 0x07B0 | `:33` 定义 0x07B0（生效情况同上，未核实） |
| KNX_TP_TxTest | `:48` 启动横幅 | "MASK 0x5780 - IP+TP dual" | `:33` 是 0x07B0 |
| KNX_TP_TxTest | `:6`、`:95` | "ETS can also observe on IP side" / "on BOTH TP bus and IP multicast" | 按 0x07B0 的意图不起 IP 栈，也没调 `openplc_net_init()` |
| KNX_TP_TxTest | `:25` | "0x57B0/0x5780 IP stack" | 默认是 0x5780，0x57B0 只是菜单选项 |
| KNX_IP_Test | `:14` | USB CDC "for Serial output" | 输出全走 `Serial_Test`（RS232），且不拉高 PB10 |
| KNX_IP_Test | `:34` 期望输出 | `[KNX] Stack started (MASK 0x57B0)` | `:198` 打的是 `MASK 0x5780 - IP+TP dual device` |
| KNX_IP_Test | `:35` 期望输出 | `[KNX] Not yet configured by ETS - waiting...` | `:203-204` 是 `Not yet configured - use ETS to assign address.` + PG9 提示；且 `:182` 的 `selfProgram2CH()` 先写了表，这条分支基本走不到 |
| KNX_IP_Test | `:37` 期望输出 | `[KNX] Configured! Individual address: 1.1.1` | `:200-201` / `:224-225` 是 `[KNX] Already configured by ETS:` / `Configured by ETS:` + `[KNX] Individual address: ...` |
| KNX_IP_Test | `:43-44` 期望输出 | `Relay 0 ON` / `Relay 0 OFF` | `:63-64` 是 `[KNX] Relay 0 ON` |
| KNX_IP_Test | `:43-45` vs `:175` | 继电器在 PE6 / PE5 | 同一文件 `:175` 写 PI8 / PI10，和库一致 |
| KNX_IP_Test | `:171-172` | "MASK_VERSION 0x57B0 = IP device" 由板卡变体设定 | 默认是 0x5780（IP+TP），`:198` 自己也这么打 |
| KNX_Basic | `:19-20, 25-26, 64-65` | 继电器 PE6 / PE5 | 库用 PI8 / PI10 |
| KNX_Basic | `:17` | PG9 pull-up，active-low | 硬件高有效（见表 1） |
| KNX_Basic | `:10`、`:18` | PG11 LED 会亮 | 板上无此 LED |
| KNX_SelfTest | `:5` | `Serial` = UART4，接 debug 口 | USB CDC |

SDRAM_Basic、SDRAM_DataLogger 的头注释与代码一致（DataLogger 头写 16 MB，代码按 MiB 打印为 15 MB，属于十进制 / 二进制写法差异，不算错）。

## 表 3：抄件与 Hardware 不一致（按 `$HW/CLAUDE.md`，报给用户，不自行改）

| 抄件 | 位置 | 写的 | Hardware 实际 |
|---|---|---|---|
| 变体头 | `$CORE/variants/STM32H7xx/H743/variant_PLC_H743.h:233` | `KNX_PROG_KEY` active-low | 高有效（Bridge p5：SW2 接 3V3，R58 下拉） |
| 变体头 | 同上 `:234` | `KNX_PROG_LED` 是编程 LED | 该网络上无 LED |
| 变体头 | 同上 `:231-232` | 编程接口在 Upper Deck；"KNX TP UART (USART1)" | SW2 在 Bridge；STKNX 非 UART |
| 库注释 | `KNXLIB/knx_profiles.cpp:8-9` | 通道 0 / 1 → PE6 / PE5 | 同文件代码用 PI8 / PI10，与 xlsx 一致 |
| 库配置 | `KNXLIB/knx_config.h:16-38, 50-58` | STKNX 走 USART1；编程键 active-low | STKNX 为裸收发器；编程键高有效 |
| FACTS | `OpenPLC_Docs/docs/hardware/HARDWARE-FACTS.md:350` | `KNX_Prog_LED` PG11 "心跳指示" | 板上 HBEAT 灯是 LED3，接 PE2；PG11 这根线无 LED。**FACTS 这一格需更正** |
| xlsx（权威文件本身的描述文字） | 行 142-143 | KNX_TX / KNX_RX = "UART 转 KNX 数据收发" | 引脚对；但 STKNX 数据手册与 FACTS 均说明它不是 TP-UART。描述文字与器件不符，报给用户 |

## 未核实

- PB14 AF4 / PA10 AF7 = USART1 的 AF 编号只对照了 xlsx 的复用功能列，未逐条对照 STM32H743 数据手册的 AF 表。
- 库 UART 驱动 STKNX 时 PB14 空闲为高的后果（持续从总线抽流）是按 FACTS 电路推断，未上板。
- PD7 为什么恒 LOW（FACTS 已记为未查清）。
- sketch 内 `#define MASK_VERSION 0x07B0u` 与构建参数 `0x5780` 冲突时实际生效的是哪个（未编译）。
