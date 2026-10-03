# 例程的网口在 Renode 里通不通

Type: research
Opened: 2026-10-03
Status: resolved
Blocked by: -

## Question

Renode 的 H743 平台有 ETH MAC，没接 PHY；`nucleo_h753zi.repl` 里有一个 ID 正是 LAN8742A 的 PHY。补上之后，例程（每个例程启动都会初始化网络）能不能拿到 DHCP 地址、应答 UDP 发现、让 IAPTool 经网口上传。Windows 上 Renode 的 `Switch` 后面谁来回 DHCP。

## 怎么算答完

- 平台补上 PHY 后，`Ethernet_IP` 在 Renode 里打出 `link up` 和一个地址
- PC 侧（或 Renode 里的脚本）发 UDP 发现得到应答
- 写明经网口上传能不能走

## Answer

2026-10-03：**能通**。平台补 LAN8742A PHY 后 `Ethernet_IP` 打出 `link up` 和地址、UDP 发现有应答（DHCP 由一个帧桥 + Python 对端回）。经网口上传在板子这侧走到 `UPLOAD Mod` 和 TCP 握手，要再补软件复位后的向量表和复位原因两处；**PC 上的 IAPTool 进模拟网络要 TAP 驱动，本机没装，完整上传没跑**。见 [SIM-02-findings.md](../SIM-02-findings.md)。

## 引出了什么新的未知

- 要不要装 TAP 驱动、让模拟里跑完整的网口上传 —— 归「例程行为检查放进哪条用例、每个例程判什么」那一轮问
- 补了 PHY 之后其余例程在 `T3-05` 里的表现没重跑
