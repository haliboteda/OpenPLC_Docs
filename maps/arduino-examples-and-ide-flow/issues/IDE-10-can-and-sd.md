# CAN 和 SD 卡：最小的库和例程

Type: task
Opened: 2026-09-24
Status: resolved
Blocked by: IDE-03, IDE-05

## Question

按「CAN 和 SD 卡在 Arduino 下最少要补什么」的结论补库，各写一个例程。

## 怎么算答完

库和两个例程在 `P5` 里编过；不限制用户 app 自己用这两个外设。变体的 SD 引脚表只剩板子真实接的脚（**先对原理图核实**，结论记进硬件事实文档）。

## Answer

2026-09-25 定。CAN 照 `port_can.c` 写了薄封装 `OpenPLC_CAN`，变体打开 `HAL_FDCAN`；SD 用上游 STM32SD，变体的 SD 引脚表按原理图从 27 项砍到 PC8/PC12/PD2（核实写进硬件事实文档「microSD 卡座」）。例程 `CAN_Counter`、`SD_ReadWrite`。

`P5` 全量 48 个例程 0 失败（2026-09-25）。**只编译过，没上过板**。上板逐个验落在 [TODO.md](../../../work/TODO.md)「端口例程逐个上板验」。

## 引出了什么新的未知

没有。
