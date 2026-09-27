# 13 个例程里哪些 Renode 判得了

Type: research
Opened: 2026-09-27
Status: resolved
Blocked by: -

## Question

`OpenPLC_Ports` 的每个例程用到哪些外设、Renode 的 `stm32h743.repl` 有没有对应模型、能从哪里观察到例程的行为（GPIO、UART、CAN、以太网、SD……）。判不了的，有什么替代方案。

## 怎么算答完

13 行的表：例程、用到的外设、Renode 能不能判、判据从哪观察、判不了时的替代方案。每一行的「能」都有出处（平台文件里的模型名，或实测）。

## Answer

2026-09-27 定。5 个现在就能判（`DO_Outputs`、`Relays`、`SystemLED`、`RS232_Echo`、`RS485_Echo`），`SD_ReadWrite` 能判但有未核实项，6 个只能判一部分，`AO_Outputs` 判不了（没有 DAC 模型）。逐个表格和替代方案见 [REN-02-findings.md](../REN-02-findings.md)，除 `DO_Outputs` 外都是读代码得出，没跑过。

## 引出了什么新的未知

- `Serial` 从哪引出来：`USB.USB_UART` 还是改编译选项走 UART4
- 板载温度：变体头标 NTC（`variant_PLC_H743.h:228-229`），`BoardTemperature` 按线性传感器算（`BoardTemperature.ino:27`），哪个对要查原理图，没核实
