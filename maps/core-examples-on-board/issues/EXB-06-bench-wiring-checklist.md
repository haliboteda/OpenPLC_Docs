# 台子接线核对

Type: task
Opened: 2026-09-29
Status: open
Blocked by: -

## Question

跑第一条真板用例之前，台子上每个对端接在哪个 PC 口上、有没有接：USB-C（板子的 CDC 口）、网线、RS232 C05 / C06 接的哪个 USB 串口、USB-RS485（COM16?）、CANable（COM15）和它的 120 Ω 终端、KNX 总线电源、SD 卡、日志口。2026-09-29 PC 上看不到板子（网络 ping 不通，COM5 / COM11 不在）。

## 怎么算答完

每个对端对应到一个确定的 COM 口或 IP，写进 `$TEST/config/machine.py` 能用的形式；板子能被 PC 发现。
