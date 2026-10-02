# 「把根编进 bootloader」这条路还留不留

Type: grilling
Opened: 2026-09-30
Status: resolved
Blocked by: ROOT-02, ROOT-03

## Question

根能不重烧就换之后，`rotate_keys.sh`（生成密钥并编进 bootloader）还留着给谁用；留的话两条路怎么让用户选，不留的话已经这么做过的板子怎么办。

**「不留」用户 2026-09-30 已定**（bootloader 代码里不再编任何根，见 [map.md](../map.md)）。剩下要定的只有：`rotate_keys.sh` 删掉还是改成只生成密钥；已经编进自己根的板子升级到新 bootloader 时根去哪。

**2026-09-30 [决策 72](../../../docs/tables/DECISIONS.md) 之后**：出厂不写任何根，公开根和内置根都取消。`rotate_keys.sh` 跟着公开根一起删；已编进自己根的板子升级后根去哪仍待定。

## 怎么算答完

定下留或不留；留的话写出它服务的那种用户，不留的话写出已编进自己根的板子的去向。

## Answer

2026-10-03 定（用户选 A）。「把根编进 bootloader」这条路不留，`rotate_keys.sh` 已随决策 72 删掉。已经把自己的根编进旧 bootloader 的板子不做迁移：发出去过的 v0.1.0–v0.1.2 都没有 `flashboot`，只能用 ST-Link 重烧，重烧后回到无根，第一次上传重新认领，和恢复出厂一样。理由：旧根编在代码里，重烧就没了，迁移读不到；而且测试阶段不做向后兼容（[决策 79](../../../docs/tables/DECISIONS.md)）。

## 引出了什么新的未知

没有。
