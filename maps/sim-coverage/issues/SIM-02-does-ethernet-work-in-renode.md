# 例程的网口在 Renode 里通不通

Type: research
Opened: 2026-10-03
Status: open
Blocked by: -

## Question

Renode 的 H743 平台有 ETH MAC，没接 PHY；`nucleo_h753zi.repl` 里有一个 ID 正是 LAN8742A 的 PHY。补上之后，例程（每个例程启动都会初始化网络）能不能拿到 DHCP 地址、应答 UDP 发现、让 IAPTool 经网口上传。Windows 上 Renode 的 `Switch` 后面谁来回 DHCP。

## 怎么算答完

- 平台补上 PHY 后，`Ethernet_IP` 在 Renode 里打出 `link up` 和一个地址
- PC 侧（或 Renode 里的脚本）发 UDP 发现得到应答
- 写明经网口上传能不能走
