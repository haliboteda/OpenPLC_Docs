# IDE-04 结论 · 假板子要像到什么程度，arduino-cli upload 才能走完

票：[issues/IDE-04-how-real-must-the-fake-board-be.md](issues/IDE-04-how-real-must-the-fake-board-be.md)
调查日期：2026-09-24。本机实验，没碰真板子（实验期间局域网上没有真板子应答）。

路径缩写：`$TOOL` = `IAPTranfer_Tool`，`$CORE_REPO` = `open_plc_arduino`，
`FB` = [`$TEST/host/fakeboard/fake_board.py`](../../../OpenPLC_Test/host/fakeboard/fake_board.py)。

## 结论

> ✅ **从板子在 bootloader 状态开始（`BOOTLD`），现有 `fake_board.py` 已经能让 `arduino-cli upload` 走完、返回 0。** 实测过，见下面的实验 1、2。

> ✅ **从板子在跑 app 开始（`CUSAPP`，这是 IDE 用户最常见的情况）要补大约 25 行**：身份串的角色和第五段、UDP 重启挑战、「重启」后切换角色，收完镜像后静默几秒再以 `CUSAPP` 回来。在 scratch 里做了一份原型，实测整条链走完 —— 见实验 3。

> ✅ **同一台 PC 上的假板子能被发现，但地址是本机网卡 IP（这台机器是 `192.168.1.4`），不是 `127.0.0.1`。** 原因：discovery 和 IAPTool 都只往物理网卡的子网广播地址发，Windows 会把这个广播回环给本机绑在 `0.0.0.0` 上的 socket，回包源地址就是网卡 IP。

> ✅ **`-p <ip> -l network` 要求 discovery 当场看见那个端口，否则 arduino-cli 直接报 `port not found`、不调 IAPTool；不带 `-l` 就不查，直接把地址交给 IAPTool。** 原因：ethMethod 下 `upload.tool.serial` 和 `upload.tool.network` 都指向 `ethtransfer`（[boards.txt:112-113](../../../open_plc_arduino/boards.txt)）。

> ✅ **现在的「板子重新上线」判据对假板子是空的**：假板子一直在应答，所以不管收到什么都判「接受了」。要让这一步有意义，假板子收完镜像后必须先沉默、再回来。

## 一次 upload 的线上往返

「IAPTool」指 [`$TOOL/IAP_Ether.go`](../../../IAPTranfer_Tool/IAP_Ether.go)，除非另注文件。

| # | 步骤 | 线上是什么 | 代码 | FB 现状 |
|---|---|---|---|---|
| 0 | arduino-cli 把端口地址交给 IAPTool | `IAPTool ether <build>/<name>.bin <serial.port> [--force]`，地址原样放进 `{serial.port}` | [platform.txt:249](../../../open_plc_arduino/platform.txt)；`--force` 来自 [boards.txt:97-99](../../../open_plc_arduino/boards.txt)；入口 [app.go:246-251](../../../IAPTranfer_Tool/app.go)（先写上传锁） | 不涉及 |
| 1 | IDE 端口菜单 / `-l network` 的端口查找 | discovery 从每块物理网卡的 IP 往子网广播地址发 `openplc_server_where_r_y`，按回包源 IP 列端口 | [network_discovery.go:187-223, 348-360, 228-275](../../../open_plc_arduino/tools/discovery/network_discovery.go) | ✅ 已有（[FB:53-69](../../../OpenPLC_Test/host/fakeboard/fake_board.py) 绑 `0.0.0.0`，对四个关键字都回） |
| 2 | 单播 identify，最多 3 次、间隔 2.5 s | UDP 发 `openplc_server_where_r_y` 到给定 IP，回包要以 `STM32H743` 开头 | IAPTool:74, 299-330；解析 241-271（≥4 段即可，第五段是 app 版本） | ✅ 已有，但只回四段 `…_BOOTLD_0.1.3`，没有第五段 `-` |
| 3 | 版本门 | 只在角色是 `CUSAPP` 且有第五段时比较：镜像版本（`<name>.version`，postbuild 生成）比板上老就拒 | IAPTool:95-97；[version_gate.go:123-178](../../../IAPTranfer_Tool/version_gate.go) | ⚠️ 要补：角色 `CUSAPP` + 第五段版本号 |
| 4 | 取身份（私钥 + 证书，自签或委托） | 纯本地；IDE 不传 `--key`，用 IAPTool 旁边 `keys/` 里的默认钥 | IAPTool:103；[auth.go:36-89](../../../IAPTranfer_Tool/auth.go)；[sign.go:45-59](../../../IAPTranfer_Tool/sign.go) | 不涉及 |
| 5 | 按角色分支 | `BOOTLD` / `BOOTLD-INVALID` 直接进 TCP；`CUSAPP` 先重启 | IAPTool:109-154 | ✅ `BOOTLD`；⚠️ `CUSAPP`、`BOOTLD-INVALID` 要补（后者只是换个字符串） |
| 6 | UDP 重启挑战 | 发 `openplc_server_reboot_challenge`，收 nonce | IAPTool:363-367 | ⚠️ 要补：回一个 nonce |
| 7 | 认证重启 | 发 `openplc_server_reboot <证书hex> <nonce签名hex>`，不等回答；最多问 3 次 | IAPTool:368-372, 125-143 | ⚠️ 要补：收到后切到 `BOOTLD`，并沉默一小段 |
| 8 | 等待 + 重新发现 bootloader | 睡 `reboot_wait_seconds`（默认 4 s），然后**广播**找角色 `BOOTLD`、UID 相同的设备，最多 3 轮 | IAPTool:132-137, 160-173, 175-239；[common.go:50](../../../IAPTranfer_Tool/common.go) | ⚠️ 要补：以 `BOOTLD` 应答（广播回环在本机成立，实验 3） |
| 9 | TCP 连接 + `ping` | 连 `<ip>:56865`，`ping\n` → `OK` | IAPTool:501-509, 539-557 | ✅ 已有 |
| 10 | 公钥核对 | `getpubkey\n` → 128 位 hex；不是 128 位就警告跳过 | IAPTool:511-515；[auth.go:122-157](../../../IAPTranfer_Tool/auth.go) | ✅ 已有（T1-18a–g 的全部七种结果都在测，见 [KEY-MATCH.md](../../../OpenPLC_Test/host/fakeboard/KEY-MATCH.md)） |
| 11 | TCP 挑战 | `authchallenge\n` → nonce | IAPTool:570-573 | ✅ 已有（固定 nonce） |
| 12 | `flash` 命令 | `flash <size> <crc32> <镜像签名> <证书> <nonce签名>\n` → `OK` | IAPTool:568, 574-583 | ✅ 已有（只读 size，其余不验） |
| 13 | 分块发数据 | 8 KiB 一块，裸字节，每块等 `OK` | IAPTool:588-595；[common.go:18](../../../IAPTranfer_Tool/common.go) | ✅ 已有（[FB:86-92](../../../OpenPLC_Test/host/fakeboard/fake_board.py)） |
| 14 | 最终判决 | 90 s 窗口内：每 2 s 先听 TCP，有字且不是 `OK` 就是拒绝；没字就广播找同 UID 设备（任意角色），找到即成功 | IAPTool:627-676 | ⚠️ 要补：收齐后沉默几秒再以 `CUSAPP` 回来；现在一直在应答，判据恒为真。可选：按参数回 `Signature Failed` 等拒绝串，测 IAPTool 的拒绝路径 |

判决失败的文案和成功时「无回答、复位后重新上线」的约定见 [IAP-PROTOCOL.md「一次 flash 的往返」](../../docs/modules/M1/IAP-PROTOCOL.md)。

## 实验

均在本机：`arduino-cli 1.5.1`（IDE 自带），已装板卡包 `OpenPLC_Alpha:stm32 0.1.3-pre`，板卡包里的 `IAPTool.exe`（和 `$TOOL/Output/windows/IAPTool.exe` 同一次构建，9-22 22:35）。

| # | 做了什么 | 结果 |
|---|---|---|
| 1 | FB（`BOOTLD`）+ `IAPTool ether app.bin 127.0.0.1` | rc=0，9 s。identify/TCP 走 `127.0.0.1`，最终判决的广播回包来自 `192.168.1.4`，UID 相同 → 判「接受」 |
| 2 | FB + `arduino-cli board list` | 列出 `192.168.1.4  network`，Board Name 为 Unknown |
| 2b | FB + `arduino-cli upload -b …:upload_method=ethMethod -p 192.168.1.4 -l network --input-dir …` | rc=0，12 s，末尾打印 `New upload port: 192.168.1.4 (network)` |
| 2c | 同上但 `-p 127.0.0.1 -l network` | `Error getting port metadata: port not found: 127.0.0.1 network`，IAPTool 没被调用 |
| 2d | `-p 127.0.0.2`，不带 `-l` | IAPTool 被调用，参数原样是 `127.0.0.2` |
| 3 | scratch 原型（FB 加 `CUSAPP`/重启/静默回来，约 25 行）+ 镜像版本 2.0.0，板上 1.2.3 | rc=0，26 s：identify → reboot challenge → reboot → 等 4 s → 广播找到 `BOOTLD` → TCP 全套 → 静默 → 以 `CUSAPP` 回来 → 判「接受」 |
| 3b | 同上，镜像版本 1.0.0 | 版本门拒绝，`this board already runs 1.2.3; … 1.0.0, which is older` |

## 做模拟台时要知道的三个坑

| 坑 | 现象 | 出处 | 模拟台怎么办 |
|---|---|---|---|
| `-l network` 的端口查找默认只等 1 s，discovery 在 Windows 上启动要约 1.3 s（先跑一次 PowerShell 给网卡分类） | 同样的命令时好时坏：`port not found` | [iface_windows.go:26-29](../../../open_plc_arduino/tools/discovery/iface_windows.go)；[network_discovery.go:193](../../../open_plc_arduino/tools/discovery/network_discovery.go)；`arduino-cli upload --help` 的 `--discovery-timeout (default 1s)` | 加 `--discovery-timeout 8s` 后稳定；或者不带 `-l` |
| 失败的上传会留下上传锁，之后 90 s 内 discovery 不广播 | 一个用例失败后，下一个 `-l network` 用例 `port not found` | [uploadlock.go:19-26](../../../IAPTranfer_Tool/uploadlock.go)（`logf(true)` 退出不跑 defer，这是写明了的取舍）；[network_discovery.go:336-351](../../../open_plc_arduino/tools/discovery/network_discovery.go) | 用例之间删掉 `%TEMP%/openplc-iap-upload.lock`，或串行等过 90 s |
| 假板子在最后一个 `OK` 后 100 ms 内关 TCP，IAPTool 报 `read ack error: EOF` | 原型第一版踩到 | IAPTool:685-712（`readWithIdleGap` 把非超时错误连同已读内容一起返回，`sendAndWaitOK` 当失败） | 假板子「复位」时不要立刻关连接，停几百毫秒或干脆不关 |

## 这条模拟测不到什么

| 测不到 | 为什么 |
|---|---|
| 板子这一侧的任何校验：镜像签名、证书链、nonce 签名、叶撤销、CRC、重启冷却 | FB 不验任何东西（[FB:9-11](../../../OpenPLC_Test/host/fakeboard/fake_board.py)）；这些在真板子上由 T1-11 / S1 覆盖 |
| 固件真的被写进去、新 sketch 真的跑起来 | FB 只数字节 |
| 真实的复位时序、MAC 掉线、发现限流（同一源 2 s 内只回一次）、UDP 丢包 | FB 没有限流、不丢包；IAPTool 的重试间隔（IAPTool:49-52）和上传锁要防的碰撞都靠这些才会被触发 |
| 真的局域网：板子在另一台机器上、多网卡、VPN 抢路由、源地址钉在物理网卡上（IAPTool:391-440） | 本机回环时「对端」就是本机网卡 IP，`LocalIPFor` 永远命中自己的网卡 |
| 没有物理网卡时 discovery 的 `255.255.255.255` 兜底（[network_discovery.go:373-384](../../../open_plc_arduino/tools/discovery/network_discovery.go)） | 本机有物理网卡，没走到 |
| IDE 图形界面里 Tools → Port 和 Upload 按钮 | 只测了 `arduino-cli`；IDE 用的是常驻的 arduino-cli 守护进程，discovery 常开，1 s 竞态可能不存在 —— **没验证** |
| Linux / macOS | 只在 Windows 上跑过；广播回环给本机 socket 在别的系统上是否成立 **没验证** |

## 没验证的

- IDE 2 图形界面里的端口菜单和 Upload（票 [IDE-11](issues/IDE-11-ide-upload-on-the-simulator.md) 的范围）。
- 板卡包 `keys/fw_signing_key.pem` 对应的公钥：实验里 FB 用 `unknown` 回 `getpubkey`，跳过了公钥核对。模拟台要测核对通过，得让 FB 回那把钥的公钥（归 [IDE-02](issues/IDE-02-which-key-does-an-ide-upload-use.md) / [IDE-13](issues/IDE-13-where-does-the-ide-upload-key-live.md)）。
- 顺带看到但不在本票范围：discovery 按 `_` 只切四段（[network_discovery.go:232](../../../open_plc_arduino/tools/discovery/network_discovery.go)），五段身份串的端口标签显示成 `STM32H743 (0.1.3_1.2.3) @ …`；当前影响只在标签文字上。
