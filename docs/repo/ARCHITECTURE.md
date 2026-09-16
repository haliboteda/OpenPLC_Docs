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
| `$PROD` | `AI-Skills` checkout 里的 `OpenPLC/` —— 产品级文档在它的 `docs/` 下 |

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

核对两边是否已同步：`$TOOL/TestCase/tools/check_core_sync.py`（用例 **P3**，发版检查单 B3）。

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

因为没有共享构建，下面这些东西在多个仓库里各有一份拷贝，**只能靠注释交叉引用约束，机制上无法强制同步**。改一处必须改另一处，否则会静默分叉 —— 不会编译报错，只会在运行时表现成别的症状。

下表的 "core" 指 `$CORE_LIVE` 和 `$CORE_REPO` 两份（先改前者，验证过再同步到后者）。

| 内容 | 在哪几份 |
|---|---|
| MAC 从 UID 派生的算法 | bootloader `LWIP/Target/ethernetif.c`（USER CODE MACADDRESS 块）、core `libraries/OpenPLC_Net/src/ethernetif.c` |
| 发现回复限流 `discovery_reply_allowed()` | bootloader `IAPServer/udp_server.c`、core `libraries/OpenPLC_IAP/src/udp_server.c` |
| 身份字符串格式 `name_uid_role_version` | bootloader `IAPServer/IAP_server.c` 的 `iap_identity_string()`、core `libraries/OpenPLC_IAP/src/udp_server.c`、Go 侧解析 |
| SRAM4 交接记录 `boot_handoff_t` | bootloader `IAPServer/IAP_boot_handoff.{c,h}`、core `cores/arduino/stm32/IAP_boot_handoff.{c,h}` |
| 上传锁的文件名和过期时间 | `$TOOL/uploadlock.go`、core `tools/discovery/network_discovery.go` |
| 机器 ID（UID）的字节序与十六进制格式 | bootloader `IAPServer/iap_keyderive.c`、core `libraries/OpenPLC_IAP/src/iap_keyderive.c` |
| 证书线格式（132 字节，签名覆盖前 68） | bootloader `IAPServer/iap_cert.h`、core `libraries/OpenPLC_IAP/src/iap_cert.h`、`$TOOL/iapcert/iapcert.go` |
| owner 记录格式（v2，签名前缀 88） | bootloader `IAPServer/owner_slot.h`、core `libraries/OpenPLC_IAP/src/owner_root_ro.c`、`$TOOL/owner.go` |
| **RTC 备份寄存器的分配** | 见下表 —— **认领任何一个之前先看这里** |

### RTC 备份寄存器分配表

备份寄存器是**跨 bootloader / app 持久存在**的共享资源，而两个镜像分别编译、没有任何机制阻止它们抢同一个。

| 寄存器 | bootloader | app / core | |
|---|---|---|---|
| DR0 | — | — | 空 |
| DR1 | **nonce 计数器**（`IAPServer/iap_auth.c`） | `RTC_BKP_INDEX`（`cores/arduino/stm32/backup.h:34` 定义，**当前无人写**） | ⚠️ 潜在冲突：谁引入 STM32RTC 库谁就会踩 |
| DR2 | — | **nonce 计数器**（`libraries/OpenPLC_IAP/src/iap_auth.c:21`） | |
| DR3 | **VBAT witness** | — | |
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

## 密钥

签名密钥和固定口令在 bootloader 仓库里，连同它们的注意事项：`$PROD/docs/security/KEYS.md`。
