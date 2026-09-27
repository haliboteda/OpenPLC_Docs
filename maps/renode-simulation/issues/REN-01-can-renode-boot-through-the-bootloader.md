# Renode 能不能走 bootloader → app 的启动链

Type: research
Opened: 2026-09-27
Status: claimed
Blocked by: -

## Question

在 Renode 里烧入当前 bootloader 和一个签好名的 app（和 IDE 上传后 flash 里的内容一样），复位后 bootloader 能不能校验通过、跳进 app？卡住的话卡在哪个外设、能不能补。

## 怎么算答完

给出一套能复现的做法：Renode 里 bootloader 启动日志走完、跳进 `DO_Outputs`，DO1–DO8 按例程顺序开关；或者指出挡住它的外设模型缺口，以及补它要多大代价。
