# 板子 TP 不通时，IDE 里的总线监视要不要改走 IP 网关

Type: grilling
Opened: 2026-10-10
Status: resolved
Blocked by: -

## Question

用户要在 IDE 里演示总线监视（打印总线报文、发组写），但这块板的 TP 收发不通（[KEX-08](KEX-08-board-sees-no-bus-pulses.md)），`KNX_BusMonitor` 用不了。

| 做法 | 代价 | 这块板上能不能马上用 |
|---|---|---|
| 新例程 `KNX_IPMonitor`：板子经网口连 KNX IP 网关的隧道，命令同 `KNX_BusMonitor`（`w` / `b`），报文从 IDE 串口打印 | KNX 库新写 KNXnet/IP 隧道客户端（约几百行）+ Renode 用例；先文档再代码 | 能，不经过 STKNX |
| 演示时用电脑上的 `$TEST/tools/knx_monitor.py` | 不改代码 | 能，但不在 IDE 里 |
| 修板子 | 定位坏的器件 | 不能 |

两条都验证不了板子的 TP 收发，`T3-13`–`T3-20`（[M3](../../../docs/modules/M3-app-runtime.md)）照旧等修板。

2026-10-12：板子 TP 收发已通（[KEX-08](KEX-08-board-sees-no-bus-pulses.md)），`KNX_BusMonitor` 能直接用，这张票的前提不在了，留给用户定关不关。

## 怎么算答完

用户选定一种；选第一种就在 M3 加需求和用例再动库。

## Answer

2026-10-12 定：不做（用户：「其他的可以按推荐并行开始」）。板子 TP 收发已通，`KNX_BusMonitor` 直接可用。

## 引出了什么新的未知

无。
