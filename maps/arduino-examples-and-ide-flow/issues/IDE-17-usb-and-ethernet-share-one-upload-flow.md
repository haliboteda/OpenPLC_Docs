# USB 和网口共用一套上传流程，怎么拆

Type: grilling
Opened: 2026-10-15
Status: open
Blocked by: -

## Question

[决策 132](../../../docs/tables/DECISIONS.md)：两条路逻辑一样、只留传输层。2026-10-15 只读比对的结论：bootloader 里命令处理本来就是一份（`process_command()`），差在会话生命周期和身份串第 5 段写死 `-`；IAPTool 是两份独立流程，漂得最多；板卡包没有重复代码，差在 1200 bps 复位请求不认证。

用户 2026-10-15 补充：**不要等板子重启才拿到信息**（版本、KNX 角色）；USB 和网口只是 IAP 的两个端口，整个 IAP 逻辑不变。即 sketch 运行时 USB 上也要有和网口 UDP 服务同样的应答。

2026-10-15 真板原型（core 副本，没进仓）：**一根 USB 出两个 CDC 口可行**。sketch 跑着时口 1 是 `Serial`、口 2 由 core 应答 IAP，命令和网口 UDP 服务调同一个函数（DISCOVER 回带 app 版本、reboot challenge 回 nonce）；Win11 免驱（usbccgp + usbser），flash 多 848 B；端点用 0–5（上限 9），TX FIFO 336 words（上限 1024）。前提：IAPTool 改按「VID/PID + USB 序列号 + 接口号」找口（go.bug.st/serial 不给接口号，三平台各自读）；bootloader 仍是单口时 COM 号在 app / bootloader 间会变（已实测）。未验证：Linux、macOS、Win10、带签名的 USB 重启全流程、IDE 端口列表、装了 ST VCP 驱动的主机。

双口的影响（2026-10-15 讨论）：端点按接口拆分是 USB 2.0 第 9 章和 IAD 补充规范的正规用法；全速 12 Mbit/s 两口共用，IAP 平时只有查询，大量数据只在上传时（那时 sketch 已停），吞吐没实测；电脑上多一个 COM 口，用户可能在串口监视器里选错，口名在 Windows 上还没显示出来；装了 ST 虚拟串口驱动的主机可能冲突，未验证。待用户定：bootloader 保持单口（推荐，IAPTool 按序列号重新找口）还是也做成双口。

用户 2026-10-16 定：USB 只当设备（[决策 138](../../../docs/tables/DECISIONS.md)）；做双口的话，**Windows 和 Linux 上都要让用户分得清两个口、不会选错**（口名或 IDE 端口列表），macOS 在真机上验时同此要求。2026-10-16 读源码（未上板）：Arduino IDE 分不出两个口 —— serial-discovery 1.5.2 只报 vid / pid / serialNumber，两口相同；内置 discovery 总会加载，板卡包藏不掉也标不了第二个口。Linux 可靠 by-id 的 `-if00` / `-if02` 和 udev 规则区分；Windows 只能在 IAPTool 里按序列号 + `MI_xx` 找到 IAP 口，或让两个口对复位和 IAP 都一样能用。

| 两条路不一致的地方 | CDC | 网口 | 出处 |
|---|---|---|---|
| 版本闸门 | 板子在跑 app 时不比；进了 bootloader 第 5 段是 `-`，等于放行 | 复位前比 | `$TOOL` `IAP_CDC.go:22-35`、`IAP_Ether.go:97-99` |
| `--force` 一次性标记 | 烧成后不写 | 写 | `$TOOL` `common.go` `SendFile`、`IAP_Ether.go:673` |
| 等板子回来、认回同一块板 | 没有：COM 口消失就报成功 | 按 UID 找回、应答了才算成功 | `$TOOL` `common.go:292-333`、`IAP_Ether.go:578-582,706-726` |
| 密钥不对 | 进了 bootloader 才发现，app 已停、回不去 | app 不复位，直接报 | `$TOOL` `IAP_CDC.go:137-142`、`IAP_Ether.go:276-282` |
| 复位请求认证 | 1200 bps，不认证 | 挑战 + 签名 | `$CORE_REPO` `cores/arduino/stm32/usb/cdc/usbd_cdc_if.c:183-187`、`libraries/OpenPLC_IAP/src/udp_server.c:159-197` |
| 上传中途断开 | bootloader 不清状态，停在接收里直到复位 | TCP 断开、空闲 60 s 都清 | `$BOOT` `USB_DEVICE/App/usbd_cdc_if.c:242-256`、`IAPServer/tcp_server.c:38-41,82-98` |
| 等 OK 的判法、超时 | 含有 OK、10 s | 等于 OK、5 s | `$TOOL` `common.go:181`、`IAP_Ether.go:778` |

| 方案 | 改什么 | 代价 / 风险 | 推荐 |
|---|---|---|---|
| **G1** IAPTool 抽传输接口 | 一个 `boardLink`（认出、请复位、按 UID 找回、开会话），整条流程 `runUpload()` 一份，CDC / 网口各实现传输；`owner` 命令也走它 | 约 600 行；共用流程可接假 `boardLink` 做单元测试，两条路一起测；真 USB 仍要真板子 | ✅ |
| **B1** bootloader 会话生命周期不分通路 | 空闲超时挪进 `IAP_task()`；CDC 掉 DTR 也清状态 | 小；复跑 T1-07 / T1-08 | ✅ |
| **V1** 闸门两条路都在 bootloader 里比 | 板卡包把版本串放到 app 镜像固定偏移（K1）；bootloader 验签后从那里读出填第 5 段（B2）；加一条「回到 app」命令，CDC 被拒后板子能回去（B3） | 三仓都改；新增一条跨仓契约（偏移和魔数，进 P2）；按 BOOT0 进 bootloader 的板子也能比 | ✅ |
| V2 版本经 SRAM4 交接区转报 | app 复位前写进交接记录 | 按 BOOT0 进入时没有版本 | |
| K2 1200 bps 复位请求 | 保持不认证，在 M1 写成通路限制：这条请求带不了证书，要认证就得让 app 占 CDC 数据管道，违反 [CONSTRAINTS.md](../../../docs/modules/M3/CONSTRAINTS.md) | 无代码 | 等用户定 |

另：`$BOOT` `IAPServer/IAP_server.c` 里 `takeown`、`setowner`、`revoke` 各自手写十六进制解析，和 `hex_decode` 重复（`takeown` 不查长度）—— 和通路无关，合不合等用户定。

## 怎么算答完

用户在上表里选定；先改 [M1](../../../docs/modules/M1-firmware-upgrade.md) 写下行为，再改代码；T1-38（版本闸门）补 CDC 那支。

## Answer

## 引出了什么新的未知
