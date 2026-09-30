# core 里那份内置根怎么跟着改

Type: grilling
Opened: 2026-09-30
Status: open
Blocked by: ROOT-05

## Question

Arduino core 也编了一份 `fw_public_key`（`OpenPLC_IAP/src/fw_pubkey.c`，2026-09-30 已删），app 在运行时用 `owner_root_ro.c` 读 owner 链，链为空时回落到它。内置根搬到 flash、能被用户更新之后，core 那份编死的拷贝会和板子上的不一致。core 是改成从新位置读（范围扩到 core，板卡包要重发），还是有别的办法；这张图原定只碰 bootloader 和 IAPTool。

**2026-09-30 [决策 72](../../../docs/tables/DECISIONS.md) 之后**：出厂不写任何根，公开根和内置根都取消。照这条 core 那份 `fw_public_key` 直接删；剩下的是 `owner_root_ro.c` 改读新位置、链为空时 app 侧怎么处理。

## 怎么算答完

定下 core 那份怎么改；要改 core 的话把 `$CORE_REPO` 加进这张图的范围和 `## 全集` 命令。
