# 第一次把用户的根写进板子，要不要按住 BOOT0

Type: grilling
Opened: 2026-09-30
Status: resolved
Blocked by: -

## Question

现在 `takeown` 要求按住 BOOT0（物理在场）才能把第一把根写进 owner 区；编进 bootloader 的那条路不用按。用户没有 ST-Link 时，第一次写入保留这道门、换一道别的门、还是不设门；每种各挡住了谁、放过了谁。

## 怎么算答完

定下第一次写入的门禁，并写出它挡不住的那种攻击者。

## Answer

2026-09-30 定（用户定）。**不设门**：出厂板子没有任何根，第一次经 USB 或网口上传时由 IAPTool 自动认领，不按 BOOT0（[决策 72](../../../docs/tables/DECISIONS.md)）。挡不住的是在用户之前连上这块板子的人：同一网络里的人，或者接着 USB 那台电脑上的恶意程序。用户发现认领失败后长按 BOOT0 10 秒恢复出厂再来。

## 引出了什么新的未知

- IAPTool 自动生成的私钥放在哪、换电脑时怎么提示：已记进 [map.md](../map.md) 的 `## Not yet specified`
