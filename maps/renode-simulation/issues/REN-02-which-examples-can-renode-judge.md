# 13 个例程里哪些 Renode 判得了

Type: research
Opened: 2026-09-27
Status: claimed
Blocked by: -

## Question

`OpenPLC_Ports` 的每个例程用到哪些外设、Renode 的 `stm32h743.repl` 有没有对应模型、能从哪里观察到例程的行为（GPIO、UART、CAN、以太网、SD……）。判不了的，有什么替代方案。

## 怎么算答完

13 行的表：例程、用到的外设、Renode 能不能判、判据从哪观察、判不了时的替代方案。每一行的「能」都有出处（平台文件里的模型名，或实测）。
