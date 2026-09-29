# 第一次把用户的根写进板子，要不要按住 BOOT0

Type: grilling
Opened: 2026-09-30
Status: open
Blocked by: -

## Question

现在 `takeown` 要求按住 BOOT0（物理在场）才能把第一把根写进 owner 区；编进 bootloader 的那条路不用按。用户没有 ST-Link 时，第一次写入保留这道门、换一道别的门、还是不设门；每种各挡住了谁、放过了谁。

## 怎么算答完

定下第一次写入的门禁，并写出它挡不住的那种攻击者。
