# AO 在上电和掉电时怎么落到确定值

Type: grilling
Opened: 2026-09-28
Status: open
Blocked by: -

## Question

XTR111 的 OD 脚硬接地、输出恒使能，VIN 经 10k 接 PA4 / PA5，MCU 脚高阻时悬空（[IEC-02-findings.md](../IEC-02-findings.md)）。固件能做的是 bootloader 一开始就把 PA4 / PA5 驱动为低、一直保持到 sketch 接管；复位到那一刻之间的几毫秒、以及掉电时，只有改硬件（OD 接 MCU 或上拉、VIN 加下拉）才能兜住。要定：固件先做哪一段，硬件要不要提给硬件工程师。

## 怎么算答完

定下固件做什么、要不要提硬件改动；固件那段在真板子上量到上电后 AO 输出为 0 mA 直到 sketch 写值。
