# 第 6 步通过后怎么不按键恢复出厂

Type: grilling
Opened: 2026-10-09
Status: resolved
Blocked by: -

## Question

决策 93 要求第 6 步通过后自动恢复出厂。现在恢复出厂只有「按住 BOOT0 满 10 秒」这一种门控（[M2-ownership.md](../../../docs/modules/M2-ownership.md)），软件做不到。可选：现任 owner 签名的「释放」命令；ST-Link 只擦根区并保留校准值；保留按键，由面板提示人去按。

## 怎么算答完

选定一条，写明它会不会削弱决策 72 的所有权模型，以及对扇区 15 里校准值的影响。

## Answer

2026-10-09 定（用户）：第 6 步时 ST-Link 插着，通过后用 ST-Link 擦掉 bootloader 和校准值区以外的全部 flash，回到出厂状态，不用新增软件命令，所有权模型不动。见 [决策 94](../../../docs/tables/DECISIONS.md)。

## 引出了什么新的未知

面板怎么驱动 ST-Link（用哪个工具、擦写哪几段），并进 [六步各自的进出条件](STG-01-what-each-stage-needs-to-start-and-end.md)。
