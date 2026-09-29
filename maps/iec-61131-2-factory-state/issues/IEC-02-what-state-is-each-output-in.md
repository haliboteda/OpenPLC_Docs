# 每个输出在上电、掉电、没有 app、app 刚起来时处于什么状态

Type: research
Opened: 2026-09-28
Status: resolved
Blocked by: -

## Question

DO1–DO8、RY1–RY6、AO1–AO2、系统指示灯，在这几个时刻各是什么状态、由什么决定（硬件默认、bootloader、core 初始化、sketch）：上电到 bootloader 跑起来之前；bootloader 在跑（包括应用区为空、停在 upload 模式）；交权给 app 的那一刻；掉电过程中。另查标准有没有要求 RUN / STOP 模式。

## 怎么算答完

一张表：输出 × 时刻 → 状态 → 出处（原理图、代码行号或实测）；和标准 2003 6.3.1.3、6.3.1.4、6.3.2、7.8、7.11.3 逐条对照，写明哪条已满足、哪条不满足。

## Answer

2026-09-28 定。DO 和继电器在各时刻都落在断开（DO 挂在 VNQ 输入内部下拉这一条未核实上）；**AO 从上电到 sketch 开 DAC 之前、以及掉电时没有确定值**（XTR111 的 OD 硬接地、VIN 悬空）；看门狗、欠压检测、报警输出都没有；标准不强制 RUN / STOP。表和出处见 [IEC-02-findings.md](../IEC-02-findings.md)。

## 引出了什么新的未知

- [AO 在上电和掉电时怎么落到确定值](IEC-05-ao-has-no-defined-state-at-power-up.md)
- [欠压和掉电时进入什么预定状态](IEC-06-what-happens-on-undervoltage.md)
