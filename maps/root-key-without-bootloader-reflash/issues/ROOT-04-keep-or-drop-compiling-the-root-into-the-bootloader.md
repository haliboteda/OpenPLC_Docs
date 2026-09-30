# 「把根编进 bootloader」这条路还留不留

Type: grilling
Opened: 2026-09-30
Status: open
Blocked by: ROOT-02, ROOT-03

## Question

根能不重烧就换之后，`rotate_keys.sh`（生成密钥并编进 bootloader）还留着给谁用；留的话两条路怎么让用户选，不留的话已经这么做过的板子怎么办。

**「不留」用户 2026-09-30 已定**（bootloader 代码里不再编任何根，见 [map.md](../map.md)）。剩下要定的只有：`rotate_keys.sh` 删掉还是改成只生成密钥；已经编进自己根的板子升级到新 bootloader 时根去哪。

**2026-09-30 [决策 72](../../../docs/tables/DECISIONS.md) 之后**：出厂不写任何根，公开根和内置根都取消。`rotate_keys.sh` 跟着公开根一起删；已编进自己根的板子升级后根去哪仍待定。

## 怎么算答完

定下留或不留；留的话写出它服务的那种用户，不留的话写出已编进自己根的板子的去向。
