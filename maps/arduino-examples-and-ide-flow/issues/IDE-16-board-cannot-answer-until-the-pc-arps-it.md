# 板子进 bootloader 后要等 PC 先 ARP 它才回得了话

Type: grilling
Opened: 2026-10-13
Status: open
Blocked by: -

## Question

2026-10-13 真板实测（PC 走 WLAN）：app 签名重启进 bootloader 后，从 `[NET] IP … reachable` 到第一次回话要 1–19 s；IAPTool 三轮广播常全部落空，靠单播 identify 兜底。13:24 那次「wrong key」误报就源于此。

| 事实 | 依据 |
|---|---|
| bootloader 打出 reachable 时已能收包，卡在回包：要先 ARP 到 PC 的 MAC，板子自己的 ARP 请求在这个网络里得不到应答 | 标记包每个都立刻出现在 COM12 上，同期发现和 ping 不回；lwIP `ARP_QUEUEING`=0、待解析条目 5 s 过期（`Middlewares/Third_Party/LwIP/src/core/ipv4/etharp.c:76,212-218,1066-1072`） |
| 回包通道在 Windows 自己 ARP 板子时打开：app 和 bootloader 同一个 MAC，Windows 认为 `.32` 条目仍有效，要等它变 Stale 再探测（ReachableTime 15–45 s） | `Get-NetNeighbor` 时间线与首次回话吻合 |
| IAPTool 重启后等 4 s、每 5 s 只发一个广播 | `IAPTranfer_Tool/common.go:40,48`、`IAP_Ether.go:266-301` |
| app 冷启动也偶发（8 次里 2 次 >5 s） | 同一套探针 |
| 2026-10-15 改后的 IAPTool（每秒单播问原 IP，决策 124）真板经网口上传 3 次：发重启到 bootloader 首次回话 5.4 / 4.3 / 4.3 s，传完到 app 回话 8.3 / 9.3 / 3.9 s，全程没发广播 | TODO #81 的上板记录 |
| 未验证：板子 ARP 为什么得不到应答（没抓包）；有线 PC 上是否出现 | — |

| 做法 | 改什么 | 代价 / 风险 | 推荐 |
|---|---|---|---|
| T1 IAPTool 密集发现 | 重启后每 0.5–1 s 发「广播 + 单播到原 IP」，窗口约 50 s，见到目标 UID 即返回 | 约 20 行；板端限流 50 条/s，远够 | ✅ 已出货的 bootloader 也受益 |
| B1 bootloader 记下请求方 MAC | `udp_server_recv()` 从帧头取源 MAC，`etharp_add_static_entry()` 只保留最近一个请求方；`lwipopts.h` 开 `ETHARP_SUPPORT_STATIC_ENTRIES` | 约 15 行 + 上板验证；静态条目要限量防占满；core 侧 `udp_server.c` 是跨仓镜像第 2 条，要定是否同步 | ✅ 首次发现即回，TCP 也受益 |
| B2 发现回包改广播 | — | 板子广播能否到 WLAN 未验证，大概率无效 | |

用户 2026-10-16 定：先查板子的 ARP 请求为什么没人应答（抓包，再换一台有线 PC 对照），查完再定改不改（[TODO](../../../work/TODO.md) #85）。T1 的核心（每秒单播问原 IP）已随决策 124 做了。

## 怎么算答完

用户选定；先改 [M1](../../../docs/modules/M1-firmware-upgrade.md) 写下行为，再改代码；真板跑 3 次「app 重启进 bootloader」、3 次复位进 app，首次回话 ≤1 s after `[NET]`（B1）或 IAPTool 不再进单播兜底（T1）。

## Answer

## 引出了什么新的未知
