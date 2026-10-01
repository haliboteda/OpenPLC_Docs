# IAPTool 测试用的假板子：换成真 bootloader 代码，还是留着手写

Type: research
Opened: 2026-10-02
Status: resolved
Blocked by: -

## Question

`host/fakeboard/fake_board.py` 是用 Python 手写的 bootloader 应答，是 bootloader 协议的第二份实现。查清 bootloader 的网口代码（`IAPServer/`、lwIP）能不能像 PortTool 的模拟板那样编成 PC 程序当替身：要替换哪些硬件桩，lwIP 有没有现成的主机端口，大概多少工作量；做不了的话，用一条契约测试核对假板子和真板子回的东西一致要怎么写。

## 怎么算答完

两条路各给出：要动的文件、替换的桩、预估工作量、能覆盖和覆盖不到的用例（T1-18、T1-34）；给出推荐。

## Answer

2026-10-02 定（research；用户同日认可推荐）

**推荐 A：把 `$BOOT/IAPServer` 的真代码编成主机替身，替掉假板子里 BOOTLD 那一半。** 理由：试编已证明整条网口路径（发现、烧写、认证、owner）能在 PC 上编过，缺的只是一层 lwIP→Winsock 的桥和一组 HAL 桩；而读代码已找到假板子和真 bootloader 的 6 处分歧（见下表），B 只能发现分歧，A 让分歧不再存在。

**两条路对比**

| | A 真代码替身 | B 留假板子 + 契约测试 |
|---|---|---|
| 编进来的真文件 | `IAP_server.c` `tcp_server.c` `udp_server.c` `bootloader_state.c` `bkp_stash.c` `owner_slot.c` `iap_auth.c` `iap_cert.c` `iap_keyderive.c` `fw_verify.c` `sha256.c` `net_rand.c` `uecc/uECC.c` | 无 |
| 要写的桩 | lwIP raw API 22 个（`udp_*` 6、`tcp_*` 14、`pbuf_alloc/free`）桥到真 socket；HAL 约 35 个；`boot_selfupgrade` / `boot_handoff` / `CDC_Transmit_FS` 各一两个空实现；flash 和 SDRAM 用固定地址 `VirtualAlloc` | B1 Renode：要给 MAC 配 PHY、接 TAP、给 DHCP；B2 静态比对：一个 Python 脚本 |
| 要动 `$BOOT` | **要一处**：`IAP_server.c` 的 `jump_to_app` 是 naked ARM 内联汇编，x86 汇编不过；需加一个主机测试开关或把它拆出去（已有先例 `BOOTLOADER_STATE_HOST_TEST` 之于 `bootloader_state.c`） | 不动 |
| 工作量 | 新写约 700–900 行 C（socket 桥约 300、HAL 和 flash 桩约 250、主循环和复位模拟约 200），2–4 天（**估计，未核实**） | B1 未知且风险高；B2 约 80 行、半天 |
| T1-18a/b/d/e/f/g（密钥 / 证书匹配） | ✅ 根用真 `takeown` 写进 RAM 里的 owner 区，每例换根不用重编 | B2 只能核对 `getpubkey` 的回法字符串 |
| T1-18c（老 bootloader 答 `Unknown command`） | ❌ 现行代码答得出 `getpubkey`，造不出这一例 | 照旧靠假板子 |
| T2-28–T2-30（出厂板认领、复用密钥、板子属于别人） | ✅ 走真 `owner_slot_claim` | 照旧 |
| T1-34 ①未认领 | ✅ 全程真代码，且真校验 nonce 签名和镜像签名 —— 假板子一项不验 | 照旧不验 |
| T1-34 ②已认领 ③密钥不对 | ❌ 重启握手（`openplc_server_reboot_challenge`）在 `$CORE` 的 `libraries/OpenPLC_IAP/src/udp_server.c`，不在 bootloader；要覆盖得把它也编进来 | 照旧 |
| 都覆盖不到 | 真 lwIP / MAC / PHY、复位把 MAC 一起拉掉（所以烧写成功没有 `OK`）、时序 | 同左，外加所有状态逻辑 |
| 按决策 78 住哪 | 跑它要 `$TOOL` + `$BOOT`，归契约层，住 `$TEST` | 同左 |

**读代码找到的分歧**（假板子 `$TOOL/TestCase/host/fakeboard/fake_board.py` vs 真 `$BOOT/IAPServer/IAP_server.c`）

| 命令 / 行为 | 假板子 | 真 bootloader |
|---|---|---|
| `getowner` | `0` / `1` | owner 记录的代数（`owner_slot_generation()`） |
| `flash` | 不验 nonce 签名，一律 `OK` | 认证不过答 `ERR` 并记一次失败 |
| `info` | `Unknown command` | `Boot Loader 0.1.3` |
| `takeown` 带坏十六进制 | 不区分 | `Bad key` |
| 发现回的角色 | 永远 `BOOTLD` | 没有有效 app 时是 `BOOTLD-INVALID` |
| 第二条 TCP 连接 | 照收 | 拒绝（`tcp_server.c` `_accept` 返回 `ERR_MEM`） |

**几条证据**

- 试编在 scratchpad 里做，没动任何仓库文件：MinGW gcc 16.1 编上面 13 个真文件，只用约 110 行桩头文件就全部编过（`IAP_server.c` 用的是删掉 `jump_to_app` 汇编的副本），链接时剩 61 个未定义符号，全是 lwIP raw API、HAL 和外设句柄。
- `IAP_STAGE_BASE` 写死为 `0xC0000000`，前面没有 `#ifndef`；在本机实测 `VirtualAlloc` 能拿到 `0x08000000`（flash）、`0xC0000000`（SDRAM）、`0x38800000`（BKPSRAM）三个固定地址，所以源码里的地址常量可以原样用。
- lwIP 没有现成的主机端口可用：`$BOOT` 里只有 lwIP 2.1.2 本体，没有 contrib；contrib 的 win32 端口走 pcap，要装 Npcap、给假板子单独一个 IP（**未核实**）。只桩 raw API 更省事。PortTool 的 `lwip_fake.h` / `lwip_stub.c` 是进程内队列，**不用真 socket**，桥接得新写；按决策 76 也不能跨仓去引用它。
- `HAL_CRC_Calculate` 的桩就是标准 CRC-32 IEEE 再取反（`$BOOT/Core/Src/crc.c` 配的是字节输入、输入输出都反转、默认多项式和初值）。
- B1 Renode：`stm32h7.repl` 里有 `SynopsysDWCEthernetQualityOfService` MAC 模型，但没有 PHY；bootloader 要从 MDIO 初始化 LAN8742，还要 `dhcp_start`。Renode 在 Windows 上能不能接 TAP **未核实**。`host/renode/run.py` 现在只接两个串口文件。

## 引出了什么新的未知

- **T1-18c（老 bootloader 答 `Unknown command`）怎么办**：真代码造不出这一例。留一个只答这一句的极小假板子，还是删掉这条用例 —— 等用户定。
- **T1-34 ②③ 的重启握手在 `$CORE`**：是把 `open_plc_arduino/libraries/OpenPLC_IAP/src/udp_server.c` 也编进同一个替身（变成三个仓的契约测试），还是 app 这一侧继续用假的 —— 等用户定。
- **A 需要改 `$BOOT` 一处**（给 `jump_to_app` 加主机测试开关，或把它拆出 `IAP_server.c`），要 bootloader 那边同意。
- 上面 6 处分歧现在有没有盖住 IAPTool 的真 bug：**未核实**。
