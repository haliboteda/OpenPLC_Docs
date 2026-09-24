# 数字量例程：DI、DO、继电器、系统 LED

Type: task
Opened: 2026-09-24
Status: resolved
Blocked by: IDE-05

## Question

照定下的格式写四个例程。系统 LED（PE2）现在没有宏，需要时补。

## 怎么算答完

四个例程在 `P5` 里编过；各自的接线和预期在文件头和串口输出里写清。

## Answer

2026-09-25 定。写了 `DI_Inputs`、`DO_Outputs`、`Relays`、`SystemLED`，在 `$CORE_REPO/libraries/OpenPLC_Ports/examples/`。系统 LED 直接用 `PE2`，没有新增宏（只有这个例程用它）。DI 不开内部上拉，文件头写明没有 24 V 时八路恒读 1。

`P5` 全量 48 个例程 0 失败（2026-09-25）。**只编译过，没上过板**。上板逐个验落在 [TODO.md](../../../work/TODO.md)「端口例程逐个上板验」。

## 引出了什么新的未知

没有。
