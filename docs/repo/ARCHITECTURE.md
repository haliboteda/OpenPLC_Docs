# 三仓布局

这个产品是**三个独立的代码库**，没有共享构建系统。一个功能通常要同时改动其中两到三个。

## 路径变量

全套文档用下面这些变量指代路径，**别的地方不写绝对路径**。

| 变量 | 指什么 |
|---|---|
| `$BOOT` | `open_plc_cube_ide` 的 clone —— bootloader 的 CubeIDE 工程 |
| `$CORE_REPO` | `open_plc_arduino` 的 clone —— 板卡包，在版本控制下 |
| `$CORE_LIVE` | Arduino IDE **真正加载**的那份板卡包（`$A15/packages/.../stm32/<版本>`），**不在版本控制下** |
| `$TOOL` | `IAPTranfer_Tool` 的 clone —— PC 工具和全部测试资产 |
| `$HW` | `Hardware` 的 clone —— 原理图、netlist、生产文件 |
| `$REF` | `Hello_World_OpenPLC` 的 clone —— 同一块板子的参考工程 |
| `$IDE` | Arduino IDE 2.x 的安装根目录 |
| `$A15` | Arduino 的数据目录（装着 `packages/` 那个） |
| `$PKGIDX` | `package_index_json` 的 clone —— 只在发板卡包时用 |
| `$PROD` | `OpenPLC_Docs` 仓库 —— 全部文档和待决的问题。2026-09-16 从 `AI-Skills` 搬出来独立成仓 |

⚠️ **这里刻意不写任何一条本机的实际路径。** 以前这张表带一列「本机当前值」，也就是把九条 `E:\...` / `C:\Users\...` 写进了一个会被 clone 到别处的仓库 —— 而它自己下一段就说脚本不读它。**这台机器上每一项解析成了什么，问 `$TOOL/TestCase` 里的 `python tools/common.py --probe`**，它是唯一会照实回答的。

脚本只认 `$TOOL/TestCase/config/machine.py`（gitignored，由 `$TOOL/TestCase/tools/init_machine.py` 探测生成）。selfcheck 的 **ENV** 一步会把脚本实际解析到的路径全部打出来。

`$CORE_LIVE` 末尾是板卡包版本号，**发版会变**，所以任何地方都不写死它；`$A15/packages/OpenPLC_Alpha/tools/STM32Tools/<版本>` 里那个是随包分发的 IAPTool 版本，两个号互相独立。

## 三个仓库

| | 路径 | 内容 |
|---|---|---|
| **App 侧** | `$CORE_LIVE`（干活的地方）<br>`$CORE_REPO`（git 仓库） | 定制板卡包。编译用户应用；同时拥有 `cores/arduino/main.cpp`、变体头文件 `variants/STM32H7xx/H743/variant_PLC_H743.h`、引脚与外设映射、`libraries/OpenPLC_IAP`、`libraries/OpenPLC_Net`、`tools/discovery/` |
| **Bootloader 侧** | `$BOOT` | STM32CubeIDE 工程（`IAPServer/`、`Core/`、`LWIP/`） |
| **PC 工具侧** | `$TOOL` | Go，产出 `IAPTool.exe` 和 `TestCase.exe` |

⚠️ **Arduino 板卡包是要分发给其他工程师的**，所以 core 层的改动是共享基础设施，不是本地小修小补。

### App 侧有两份，方向是单向的

`$CORE_LIVE` 是 **Arduino IDE 真正加载的那份**（插件安装目录）。改动先落在这里，在这里编译、烧板、验证。

**只有验证通过的代码才拷进 `$CORE_REPO` 提交。**

- 反过来做没有意义 —— IDE 根本不看 `$CORE_REPO`，改那边不生效。
- ⚠️ **`$CORE_LIVE` 不在版本控制下。** 验证通过后忘了同步，那段代码就只存在于这一台机器上，重装一次 IDE 就没了。
- 同步**继续手动做，不自动化**（2026-09-11 定）。兜底是 P3 `$TOOL/TestCase/tools/check_core_sync.py`，提交前跑它。

核对两边是否已同步：`$TOOL/TestCase/tools/check_core_sync.py`（用例 **P3**，发版检查单 `CHK-B3`）。

它**刻意排除六类**，每一类为什么排除写在脚本自己的 `SKIP` 注释里 —— 那是唯一出处，这里不抄。

> 2026-09-11 跑过：`live and repo are identical`。

## 其他位置

| | 路径 |
|---|---|
| **参考示例** | `$REF` —— 发明新写法之前先看这里是怎么做的 |
| **硬件文档** | `$HW` —— 概览 `.txt` + `Production/UpperDeck/Schematics/OpenPLC_UpperDeck_R3.pdf` |
| **测试与验收总入口** | `$TOOL\TestCase` —— 用例、主机侧单元测试、板上 sketch、自动化脚本、验收单全在这里。本机路径只写在 `TestCase\config\machine.py` |
| **板卡包索引** | `$PKGIDX` —— Arduino IDE 拉板卡包用的 package index json |

**文档打架时以 KiCad 原理图为准**（确实打过架，见 `$PROD/docs/hardware/HARDWARE-FACTS.md`）。

## 跨仓镜像的代码

因为没有共享构建，下面这些东西在多个仓库里各有一份拷贝。改一处必须改另一处，
否则会静默分叉 —— **不会编译报错**，只会在运行时表现成别的症状。

**同步的规矩（2026-09-16 定）**：

1. **bootloader 是源。** 先在 `$BOOT` 里调试清楚，再同步给其他仓。
2. **改动了下表任何一处，当场问用户要不要同步其余位置** —— 不要自行决定。
3. **不做共享文件**（submodule / 生成拷贝那类），2026-09-16 明确放弃。

**下表第 1–9 条的 22 个位置 2026-09-16 逐个核实过，第 10 条 2026-09-18 新增并核实。** "core" 指 `$CORE_LIVE` 和
`$CORE_REPO` 两份（先改前者，验证过再同步到后者）。

「谁在查」一栏是实测的，不是推测 —— 跑 `$TOOL/TestCase/tools/check_mirror_sync.py`（用例 **P2**），
它自己会在输出末尾列出没查的项。

| # | 内容 | 在哪几份（源在最前） | 谁在查 |
|---|---|---|---|
| 1 | MAC 从 UID 派生的算法 | bootloader `LWIP/Target/ethernetif.c`（USER CODE MACADDRESS 块）<br>core `libraries/OpenPLC_Net/src/ethernetif.c` | P2 |
| 2 | 发现回复限流 `discovery_reply_allowed()` | bootloader `IAPServer/udp_server.c`<br>core `libraries/OpenPLC_IAP/src/udp_server.c` | P2（上限 + 窗口两项）。⚠️ **只比数值，不比注释** —— 两边的解释 2026-09-16 已经分叉（core 那份丢了「at 115200 baud」） |
| 3 | 身份字符串格式 `name_uid_role_<卡包版本>_<app版本>`（五段，`_` 分隔，任何字段都不能含 `_`）。bootloader 那一份第 5 段固定填 `-`（它不知道装的是哪一版 sketch） | bootloader `IAPServer/IAP_server.c` 的 `iap_identity_string()`<br>core `libraries/OpenPLC_IAP/src/udp_server.c`<br>tool `IAP_Ether.go` 的 `parseBoardInfoFromReply`、`IAP_CDC.go` | P2 |
| 4 | SRAM4 交接记录 `boot_handoff_t` | bootloader `IAPServer/IAP_boot_handoff.{c,h}`<br>core `cores/arduino/stm32/IAP_boot_handoff.{c,h}` | P2 |
| 5 | 上传锁的文件名和过期时间 | tool `uploadlock.go`<br>core `tools/discovery/network_discovery.go` | P2（两项） |
| 6 | 机器 ID（UID）的字节序与十六进制格式 | bootloader `IAPServer/iap_keyderive.c`<br>core `libraries/OpenPLC_IAP/src/iap_keyderive.c` | P2 比两个函数的**规范化正文**（2026-09-22 补上，此前完全没查）。⚠️ 不比整个文件 —— `#include` 两边本来就不同（`main.h` / `Arduino.h`） |
| 7 | 证书线格式（128 字节，签名覆盖前 64） | bootloader `IAPServer/iap_cert.h`<br>core `libraries/OpenPLC_IAP/src/iap_cert.h`<br>tool `iapcert/iapcert.go` | P2（长度 + 签名前缀两项） |
| 8 | owner 记录格式（v3，签名前缀 88） | bootloader `IAPServer/owner_slot.h`<br>core `libraries/OpenPLC_IAP/src/owner_root_ro.c`<br>tool `owner.go` | P2（版本 + 签名前缀两项） |
| 9 | **RTC 备份寄存器的分配** | bootloader `IAPServer/iap_auth.c`<br>core `libraries/OpenPLC_IAP/src/iap_auth.c`<br>分配表见下 —— **认领任何一个之前先看这里** | 🟡 **只查一半**：P2 只扫两个 `iap_auth.c`，不扫 core 的 `backup.h` 和 HID indices |
| 11 | **`sha256.c` 和 `iap_cert.c` 整个文件** —— 两边本来就一模一样，原先只有头注释不同 | bootloader `IAPServer/`<br>core `libraries/OpenPLC_IAP/src/` | P2 **逐字节**。⚠️ 差一个字节就红，所以改完一边必须同步另一边。<br>**`sha256.h` 不在内** —— 两边的 include guard 名字是刻意不同的；API 真变了 `.c` 必然跟着变，一样抓得到 |
| 12 | **`iap_auth.c`**：`iap_auth_issue_challenge` 整个函数；外加 `iap_auth_verify_and_consume` 里**签名覆盖哪些字节**（`nonce || msg`，顺序和长度） | 同上 | P2 比**规范化正文**（去注释、去空白）。⚠️ **不比整个文件、不比 `verify_and_consume`、也不比 `rng_words`** —— core 那份是刻意的子集（没有 `iap_auth_report_backup_domain`），`verify_and_consume` 两边取当任根的 API 和诊断输出本来就不同，`rng_words` 两边够到的 RNG 句柄不同（core 那份转调 `OpenPLC_Net` 的 `openplc_rng_words()`，决议 67） |
| 13 | **校准值区格式**（魔数、版本、通道数、布局、CRC-32）。格式见 [SECTOR-15.md](../modules/M1/SECTOR-15.md)「校准值区的格式」 | bootloader `IAPServer/calib_area.h`<br>core `libraries/OpenPLC_Ports/src/openplc_calib.h`<br>tool `internal/calarea/calarea.go` | P2。**2026-09-28 新增** |
| 10 | **物理网卡判定** —— 排掉没 up 的、回环、点对点（VPN tun）、无 MAC 的，再按操作系统分类虚拟网卡 | core `tools/discovery/network_discovery.go` 的 `isPhysicalInterface()` + `iface_{windows,linux,darwin}.go`<br>tool `internal/netiface/` | P2。**2026-09-18 新增** —— 决定见 `$PROD/docs/tables/DECISIONS.md` 第 51 条 |

> ✅ **13 条里 12 条 P2 真的在查，第 9 条只查一半。**
> 所以「只能靠注释约束」这个旧说法已经不成立 —— **只剩第 9 条的另一半（core 的 `backup.h`
> 和 HID indices）仍然只靠人。**

> ⚠️ **第 11、12 条 2026-09-22 新增**，决定见 [DECISIONS.md 第 65 条](../tables/DECISIONS.md)。
> 它们**没有**推翻上面的规矩 3：两个仓各自仍是一个真实文件，没有 submodule、没有生成拷贝，
> 同步照旧按规矩 1、2 手工做 —— 变的只是忘了同步会当场报错。

### RTC 备份寄存器分配表

备份寄存器是**跨 bootloader / app 持久存在**的共享资源，而两个镜像分别编译、没有任何机制阻止它们抢同一个。

| 寄存器 | bootloader | app / core | |
|---|---|---|---|
| DR0 | — | — | 空 |
| DR1 | — | `RTC_BKP_INDEX`（`cores/arduino/stm32/backup.h:34` 定义，**当前无人写**） | 2026-09-24 起 bootloader 不再用它（决议 66），撞车随之消失 |
| DR2 | — | — | 空。2026-09-24 起 app 也不用（决议 66） |
| DR3 | **VBAT witness** | — | 只证明备份域活着（RTC 走时要它），**不再与重放保护有关** |
| DR4 | — | `HID_MAGIC_NUMBER_BKP_INDEX` | |
| DR5–DR9 | — | — | 空 |
| DR10 | — | `HID_OLD_MAGIC_NUMBER_BKP_INDEX` | |

> ⚠️ **踩过一次（2026-08-17 定位）**：bootloader 的 VBAT witness 曾经放在 DR2，和 app 的 nonce 计数器**撞车**。
>
> app 侧的注释当时写的理由是"两个镜像不同时运行，所以没有冲突风险" —— **这个推理是错的**。备份寄存器存在的意义就是跨这次交接保存状态，**先后访问同一份持久状态就是冲突**。
>
> 后果是双向的：app 的计数器覆盖 witness，导致 bootloader 每次启动都误报"备份域丢失"（表象）；而 witness 的写入把 app 的计数器重置成固定值，**导致 app 每次经过 bootloader 之后重复发放同一批 nonce 编号**（真正的缺陷 —— 重放保护只剩 tick 在撑）。
>
> 现已把 witness 挪到 DR3。**加新用途时更新这张表。**

> ⚠️ **这张表现在只剩三个占用格，但规矩不变。** 两个 nonce 计数器 2026-09-24 随
> [决议 66](../tables/DECISIONS.md)（改用 TRNG）一起删了 —— **不等于以后可以随便占**：
> 没有分配器这件事没变，加新用途仍然先改这张表。

## 密钥

签名密钥和固定口令在 bootloader 仓库里，连同它们的注意事项：`$PROD/docs/modules/M2-ownership.md`。
