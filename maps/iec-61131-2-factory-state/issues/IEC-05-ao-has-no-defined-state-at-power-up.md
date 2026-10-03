# AO 在上电和掉电时怎么落到确定值

Type: grilling
Opened: 2026-09-28
Status: resolved
Blocked by: -

## Question

XTR111 的 OD 脚硬接地、输出恒使能，VIN 经 10k 接 PA4 / PA5，MCU 脚高阻时悬空（[IEC-02-findings.md](../IEC-02-findings.md)）。固件能做的是 bootloader 一开始就把 PA4 / PA5 驱动为低、一直保持到 sketch 接管；复位到那一刻之间的几毫秒、以及掉电时，只有改硬件（OD 接 MCU 或上拉、VIN 加下拉）才能兜住。要定：固件先做哪一段，硬件要不要提给硬件工程师。

## 怎么算答完

定下固件做什么、要不要提硬件改动；固件那段在真板子上量到上电后 AO 输出为 0 mA 直到 sketch 写值。

## Answer

2026-10-03 定（用户定）。固件：按[决策 81](../../../docs/tables/DECISIONS.md)，bootloader 一开始就把 PA4 / PA5 拉低（AO 0 mA），保持到 sketch 第一次写 AO；DO 的引脚同样主动置 0。硬件：先不提改板，等有示波器时量 AO 在上电、复位、掉电那几毫秒的实际输出，量出来有问题再请硬件工程师在 VIN 加下拉（记在 `waiting/WAITING-ON.md` 示波器那一行）。手册如实写：那两个几毫秒的窗口 AO 输出不确定。理由：标准 2003 7.11.3 只要求写明行为；固件已管住最长的那一段，剩下的窗口没实测过，不拿推测去要求改板。

## 引出了什么新的未知

没有。
