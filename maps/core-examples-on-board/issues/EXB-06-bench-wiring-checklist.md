# 台子接线核对

Type: task
Opened: 2026-09-29
Status: resolved
Blocked by: -

## Question

跑第一条真板用例之前，台子上每个对端接在哪个 PC 口上、有没有接：USB-C（板子的 CDC 口）、网线、RS232 C05 / C06 接的哪个 USB 串口、USB-RS485（COM16?）、CANable（COM15）和它的 120 Ω 终端、KNX 总线电源、SD 卡、日志口。2026-09-29 PC 上看不到板子（网络 ping 不通，COM5 / COM11 不在）。

## 怎么算答完

每个对端对应到一个确定的 COM 口或 IP，写进 `$TEST/config/machine.py` 能用的形式；板子能被 PC 发现。

## Answer

2026-10-12 定。各对端和 `$TEST/config/machine.py` 里认它的设置（由 `$TEST/tools/init_machine.py` 的 `SETTINGS` 生成）：

| 对端 | PC 侧 | 脚本从哪拿 | 怎么核实的 |
|---|---|---|---|
| 板子 USB（CDC） | COM17 | `CDC_PORT`；读系统日志的脚本按 `BOARD_UID` 自己找这个口（决策 147） | 2026-10-10 `T3-06` 经它上传 15 个例程 |
| RS232 C05 / C06 | COM12 | `RS232_PORT`（2026-10-17 由 `LOG_PORTS` 改名：日志和例程输出改走板子 USB，这里只剩测 RS232 本身和用 `RS232` 打印的板上 sketch） | 2026-10-10 例程输出都在这里 |
| USB-RS485（A10 / A11） | COM16 | `RS485_PORT`（2026-10-12 新加，`run_examples.py --rs485` 的默认值） | 2026-10-10 `RS485_Echo` 过 |
| CANable | COM15 | 不进配置：`$TEST/tools/can_send.py` 按 USB VID/PID 找 | 2026-10-10 `CAN_Counter` 过 |
| 网线 | 板子 192.168.0.32（2026-10-12；MAC `02:BB:F5:38:99:12`，UID `393939383432510300390029`） | `BOARD_UID`（脚本运行时按它广播发现取 IP，见 [HOW-TO-RUN-TESTS](../../../docs/engineering/HOW-TO-RUN-TESTS.md)「`$TEST` 的本机配置」） | UDP 发现回了这块板的 UID；**地址由 DHCP 给、会变**，所以不记 IP |
| KNX 总线电源 | — | — | 2026-10-12 `KNX_BusMonitor` 收发（[KEX-08](../../knx-examples/issues/KEX-08-board-sees-no-bus-pulses.md)） |
| DI 24 V | — | — | 2026-10-10 `DI_Inputs` 过 |
| AO1、AO2 | 各接 470 Ω，量两端电压折算电流 | — | 用户 2026-09-29 |
| AI | 没接 | — | 不算接线缺陷：`AI_Inputs` 本轮不测（见[地图](../map.md)「Out of scope」） |

## 引出了什么新的未知

板子 IP 每次 DHCP 变了，上板脚本记的 IP 就过期。用户 2026-10-13 定：脚本运行时按 UID 广播发现（已做，见上表「网线」一行）。
