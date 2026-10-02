# bootloader 替身：用真代码代替手写假板子

**是什么**：把 `$BOOT/IAPServer` 的真源码，加板卡包 `OpenPLC_IAP/src/udp_server.c`（app 一侧的重启握手），编成一个 PC 程序。IAPTool 的契约测试（T1-18a–g、T1-34）对着它跑，不再对着手写的 `fake_board.py`。

**为什么**：手写假板子是 bootloader 协议的第二份实现，已经和真 bootloader 有 6 处不一致（`flash` 不验认证、`getowner` 回值不同等）。用真代码，不一致就不存在了。决定见 [IAPTool 测试用的假板子](../../maps/test-architecture/issues/TA-06-should-the-fake-board-become-real-bootloader-code.md) 和 [真 bootloader 替身覆盖不到的几例怎么办](../../maps/test-architecture/issues/TA-13-what-the-real-bootloader-stand-in-cannot-cover.md)。

## 住哪、怎么编

| 项 | 定案 |
|---|---|
| 位置 | `$TEST/host/bootstand/`。要 `$BOOT`、`$CORE_REPO`、`$TOOL` 三个仓，按决策 78 归契约层 |
| 构建 | CMake，和 `$BOOT/tests` 同一套写法；源码只读引用 `$BOOT` 和 `$CORE_REPO`，不拷贝 |
| 驱动 | `$TEST/host/fakeboard/` 的 `run_cases.py`（T1-18）和 `run_ide_upload.py`（T1-34）改为启动替身 |
| 端口 | 和假板子一样：烧写和命令走 61865，发现另外在 56865/UDP 应答（见 HOW-TO-RUN-TESTS 的假板子端口说明） |

## 真的是什么，替掉的是什么

| 真代码（只读编进来） | 替身自己写的 |
|---|---|
| `$BOOT/IAPServer`：`IAP_server.c`、`tcp_server.c`、`udp_server.c`、`bootloader_state.c`、`bkp_stash.c`、`owner_slot.c`、`iap_auth.c`、`iap_cert.c`、`iap_keyderive.c`、`fw_verify.c`、`sha256.c`、`net_rand.c`、`uecc/uECC.c` | lwIP raw API（`udp_*`、`tcp_*`、`pbuf_*`）桥到 PC 的 socket |
| 板卡包 `OpenPLC_IAP/src/udp_server.c`：app 在跑时的重启挑战与重启 | HAL 桩（flash 擦写、CRC、RNG、复位等）；CRC 是标准 CRC-32 IEEE 再取反，和 `$BOOT/Core/Src/crc.c` 的配置一致 |
| | flash、SDRAM、备份 SRAM 放在源码里的原地址（`0x08000000`、`0xC0000000`、`0x38800000`），由 PC 在固定地址上分配；flash 内容存成文件，模拟复位后还在 |
| | 角色切换：没有有效 app 时跑 bootloader 那一半；收完镜像、模拟复位后，镜像有效就切到 app 那一半 |

## 两处特别处理

| 情况 | 怎么做 | 为什么 |
|---|---|---|
| T1-18c：老 bootloader 不认识 `getpubkey` | 替身带一个开关，开着时在进入真代码之前拦下 `getpubkey`，回 `Unknown command` | 打过标签的 v0.1.0–v0.1.2 bootloader 都没有这条命令，现行代码造不出这一例 |
| `jump_to_app` 是 ARM 汇编 | `$BOOT/IAPServer/IAP_server.c` 加主机测试开关，开关打开时不编那段汇编 | 照 `bootloader_state.c` 的 `BOOTLOADER_STATE_HOST_TEST` 先例；固件编出来不变 |

## 怎么跑

| 做什么 | 命令（在 `$TEST` 下） |
|---|---|
| T1-18a–g 和它里面的 T2-28–T2-30 | `python host/fakeboard/run_cases.py`，selfcheck 的 `T1-18a-T1-18g` 一步就是它 |
| T1-34 | `python host/fakeboard/run_ide_upload.py`，要 arduino-cli，几分钟，不进 selfcheck |
| 单独起一块替身 | `python host/bootstand/bootstand.py --state <目录> --fresh [--root <128 位十六进制公钥>] [--old-bootloader] [--discovery-port 56865] [--uid <24 位十六进制>]` |

两个驱动脚本每次都先编替身（`host/bootstand/build/`，gitignored），要 `HOST_CC` 和 CMake（在 PATH 上或 `HOST_CC` 旁边）。替身往 stdout 打 `[stand-in] root <公钥>`（根变了就打）、`[stand-in] reset`、`[stand-in] jump to app`、`[stand-in] ... serving on <端口>`，脚本读这几行和真代码自己的 `printf` 判结果。

落地时和上文写法不一样的两处（2026-10-02，待用户确认）：

| 上文 | 实际 | 为什么 |
|---|---|---|
| 编成一个 PC 程序 | 两个程序 `bootstand_boot`、`bootstand_app`，由 `bootstand.py` 按复位轮流启动 | bootloader 和板卡包各有一份同名函数（`iap_auth`、`iap_cert`、`sha256`、`uECC`），一次链接放不下两份；分成两个进程也正好对应复位后整块内存重来 |
| PC 在固定地址上分配内存 | 同上，另外整个进程（镜像、栈、堆）链接在 4 GiB 以下 | 固件是 32 位的，真的 flash 驱动把缓冲区地址当 `uint32_t` 传给 `HAL_FLASH_Program`；64 位地址会被截断 |

## 测不到什么

真 lwIP、MAC、PHY 和时序；复位时 MAC 一起被拉掉（所以真板子烧写成功收不到 `OK`）；`flashboot`（替身直接拒绝，T1-18 / T1-34 不发它）；USB CDC 通道；Linux 上固定地址分配没验证过。替身不跑 `MX_RTC_Init()`，所以每次启动都会打一行 `Backup domain was lost`，只是日志，不影响判定。

⚠️ 换成真代码后，原来在假板子上过的用例如果失败，**先当成 IAPTool 或用例判据的问题去查**，不改替身去迁就用例：那正是要找的不一致。
