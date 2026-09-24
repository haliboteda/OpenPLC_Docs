# 以太网例程

Type: task
Opened: 2026-09-24
Status: resolved
Blocked by: IDE-05

## Question

照定下的格式写一个例程，用 `OpenPLC_Net` 已经起来的网络。

## 怎么算答完

例程在 `P5` 里编过；输出里打出板子的 IP，并给出从 PC 上验证它的方法。

## Answer

2026-09-25 定。写了 `Ethernet_IP`：用 `OpenPLC_Net` 已起来的网络，打出 link 状态和 DHCP 地址，文件头给出从 PC ping 或在 Tools → Port 里找它。

`P5` 全量 48 个例程 0 失败（2026-09-25）。**只编译过，没上过板**。上板逐个验落在 [TODO.md](../../../work/TODO.md)「端口例程逐个上板验」。

## 引出了什么新的未知

没有。
