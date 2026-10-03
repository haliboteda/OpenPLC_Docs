# 例程的网口在 Renode 里通不通（调研记录）

回答 [SIM-02](issues/SIM-02-does-ethernet-work-in-renode.md)。2026-10-03，Renode 1.17.0，板卡包 0.1.3，bootloader 为当天 `$BOOT/Debug/open_plc_cube_ide.bin`。
例程 `Ethernet_IP`，FQBN 与 `$TEST/tools/run_examples.py` 相同（`usb=CDCgen`，`--warnings all` 编过）。flash 布局直接调用 `$TEST/host/renode/run.py`（用例 `T3-05`：每个例程经真 bootloader 启动）的 `flash_banks()`。
原型全在会话 scratch（`sim02/`：`UdpFrameBridge.cs`、`netpeer.py`、`drive.py`、`noncesig/`），不进仓。

## 结论

| 问题 | 结论 | 核实了吗 |
|---|---|---|
| 补上 PHY 后能不能 link up、拿到地址 | **能**。照 `nucleo_h753zi.repl:19-29` 补 PHY 后，`last_link` = 1、`shown_ip` = 1，USART3 打出 `[NET] ip=10.77.0.50 mac=02:A5:C3:9E:17:00` | ✅ 实跑 |
| 不补 PHY 会怎样 | 一帧都不发，`last_link` = 0；app 照常跑，不挂 | ✅ 实跑（对照组） |
| Switch 后面谁来回 DHCP | **Renode 没有内置 DHCP 服务**，要自己接一个。推荐：一个 60 行的 C# 桥（`include` 现场编译）把 Switch 上的帧经 127.0.0.1 UDP 转给 Python，Python 回 ARP / DHCP | ✅ 实跑 |
| UDP 发现有没有应答 | **有**。广播 `openplc_server_where_r_y` 到 `10.77.0.255:56865`，app 回 `STM32H743_000…0_CUSAPP_0.1.3_1.0.0`（五段，IAPTool 能解析） | ✅ 实跑 |
| 经网口上传能不能走 | **板子这边能走到 TCP 握手**：认证重启 → bootloader 进 `UPLOAD Mod (ethernet upload requested)` → 重新 DHCP → 发现回 `BOOTLD` → 56865 回 SYN-ACK。**但除了 PHY 还要再补两处**（下表第 2、3 条），而且**PC 上的 IAPTool 进不来**（本机没有 TAP），文件传输本身没跑 | 握手 ✅ 实跑；传文件 ❌ 没跑 |

## 平台要补的三处

`run.py` 的 resc 只要加这几行；第 2、3 条只有走上传那条路时才需要。

| # | 是什么 | 不补会怎样 | 补法 | 证据 |
|---|---|---|---|---|
| 1 | LAN8742 PHY | 无 link，无 DHCP | `machine LoadPlatformDescriptionFromString` 加 `phy: Network.EthernetPhysicalLayer @ ethernet 0 { … }`，寄存器值照抄 `nucleo_h753zi.repl:19-29`（`Id1 0x0007`、`Id2 0xC130`、`VendorSpecific15 0x1058` = 100M 全双工）。驱动从地址 0 扫起，地址 0 即可 | 对照组 `last_link` 0 vs 1 |
| 2 | 复位后的向量表 | 软件复位后 `PC = 0x0, SP = 0x0`，跑飞到 `0xEFFFFFFE` | `cpu InitVectorTableOffset 0x08000000`（真片由选项字节 BOOT_ADD0 决定；`run.py` 里的 `cpu VectorTableOffset` 只管第一次） | 第一次重启实跑的 console |
| 3 | 复位原因 | Renode 的 RCC 在软件复位后仍报 `PORRSTF`，bootloader 当冷启动处理、丢掉 app 的上传请求，直接回 `APP Mod` | `sysbus SetHookAfterPeripheralRead sysbus.rcc "if offset == 0xD0 and machine.SystemBus.ReadDoubleWord(0x38000000) == 0x504C4321: value = (value & ~(1 << 23)) \| (1 << 24)"` —— SRAM4 里有交接记录时报 `SFTRSTF` | 不补：UART4 第二次启动打 `Reset cause: POR` + `APP Mod`；补了：`Reset cause: SOFT` + `UPLOAD Mod` |

第 3 条的依据：bootloader 只在非 POR 复位时读交接记录（`$BOOT/IAPServer/IAP_boot_handoff.c:201-210`）；SRAM4 的内容在 Renode 复位后还在（补了之后能进 `UPLOAD Mod` 就是证据）。

## DHCP 对端怎么选

| 做法 | 代价 | 风险 | 核实了吗 |
|---|---|---|---|
| **A. C# 帧桥 + Python 对端**（本次做法） | 一个 `.cs`（`IMACInterface` + `IExternal`，用 `include @x.cs` 现场编译，`emulation CreateUdpFrameBridge` 建出来接到 Switch）+ 一个手写 ARP / DHCP / UDP / TCP 帧的 Python 脚本 | 对端是手写的，TCP 只写到 SYN，完整上传要在 Python 里写一个 TCP 客户端 | ✅ |
| B. TAP 接主机网卡，主机上跑 DHCP 服务，IAPTool 直接用 | 要装 OpenVPN 的 TAP-Windows6 驱动和 `tapctl.exe`（管理员权限，要用户动手） | 和主机网络混在一起；本机没装，`emulation CreateTap` 只打 `tapctl.exe utility not found - running in the dummy mode!` | ❌ 只核实了「现在不可用」 |
| C. 再起一台模拟机跑 Zephyr 的 DHCP 服务 | Renode 自己的用例就这么做（`tests/platforms/nucleo_h753zi.robot:404-428`），ELF 要从 antmicro 下 | 只解决 DHCP，不解决发现和上传 | ❌ 没跑 |

**推荐 A**：不用装驱动、不碰主机网络、能并行，已经跑通到 TCP 握手。
B 是唯一能让**真 IAPTool** 跑完整个网口上传的路，需要时再装。

关于 56865 端口：A 里板子的 56865 只在 Renode 的虚拟 Switch 上，主机这边只占 `127.0.0.1` 上两个自选端口（本次 47300–47399），所以和本机 `airtcp` 占着的 56865 不冲突。

## 实跑记录

| 跑法 | 虚拟时间 | 墙钟 | 结果 |
|---|---|---|---|
| 补 PHY，不重启 | 40 s | 357 s | DHCP、`[NET] ip=`、`last_link` = 1、`shown_ip` = 1、发现应答 ×3 |
| 不补 PHY | 40 s | 354 s | 0 帧、`last_link` = 0、app 照常跑 |
| 补 PHY + 认证重启（补丁 2，不补 3） | 90 s | 779 s | 重启后回到 app（`Reset cause: POR`），发现一直回 `CUSAPP` |
| 补 PHY + 认证重启（补丁 2 + 3） | 90 s | 911 s | `UPLOAD Mod`，`[NET] IP 10.77.0.50 … port 56865`，发现回 `BOOTLD_0.1.3_-`，SYN → SYN-ACK |

认证重启用的是 IAPTool 自己的 `iapcert.NonceSig`（scratch 里引用 `$TOOL` 模块编的小程序），证书由 `IAPTool cert --key=root.pem` 签发，和真上传走同一套代码。

墙钟慢主要在 bootloader 那段（约 5 分钟）：就是 [SIM-01-findings.md](SIM-01-findings.md)「当天的 bootloader 在原样的 `stm32h743.repl` 上起不来」那条 PWR BRRDY 等待，这次没补那个，靠拉长虚拟时间过去的。

## 没核实的

- **完整的网口上传**（传文件、校验、写 flash、回 app）没跑：A 的 Python 对端没写 TCP 客户端，B 没有 TAP
- 加了 PHY 之后，其余 12 个例程在 `T3-05` 里的表现没重跑（它们启动时都会初始化网络）
- KNX 的 IP 那一半（地图「Not yet specified」第一条）：桥能转任何以太网帧，包括组播；但 xknx 走主机套接字，要用它就得走 B
