# 三平台：要定目标或要真机才能做的几件

Type: grilling
Opened: 2026-10-15
Status: open
Blocked by: -

## Question

[决策 131](../../../docs/tables/DECISIONS.md) 要求工具和代码在 Windows、Linux、macOS 上都能用；bootloader 替身只做 Windows（[决策 143](../../../docs/tables/DECISIONS.md)）。2026-10-15 只读核查后，能按代码判定的缺陷已直接修；下面几件要用户定目标，或者没有真机做不了。

| 事 | 现状 | 不修会怎样 | 可选做法 | 出处 |
|---|---|---|---|---|
| **IAPTool 只有 amd64** | 三个平台都只编 `GOARCH=amd64`，`macosx/IAPTool` 是 x86_64；discovery 已有 `darwin_arm64` | Apple Silicon 的 Mac 没装 Rosetta 时 IDE 上传全部失败 | 加编 darwin/arm64，照 discovery 的 `macos-launcher.sh` 按架构分发（推荐）；另定要不要 linux/arm64 | `$TOOL` `build.py` 的 `TARGETS`；发版连带 `Arduino_Tools` 和索引 |
| **discovery 在 Linux 只有 amd64** | `platform.txt` 直接指 `linux_amd64` | 树莓派、ARM 笔记本上 IDE 的网络端口列表起不来 | 同上，要不要把 linux/arm64 算目标平台 | `$CORE_REPO` `platform.txt:260`、`tools/discovery/build.py:22-25` |
| **CubeMX 生成后的钩子只有 `.bat`** | 改回链接脚本的钩子登记的是 `restore_ld_script.bat` | Linux / macOS 上重新生成代码后要手工补跑（P17 会抓到） | 改调 `restore_ld_script.py`；CubeMX 能不能直接调 `.py` 要真机确认 | `$BOOT` `open_plc_cube_ide.ioc:377` |

另：按[决策 144](../../../docs/tables/DECISIONS.md)，各仓不是 Python 的脚本这样处理（用户 2026-10-16 定，同日已改完）：

| 脚本 | 谁在什么时候跑 | 处理 | 理由 |
|---|---|---|---|
| `$CORE_REPO` `tools/discovery/build.sh` | 开发者编 discovery | 删，留同功能的 `build.py` | 两份一样；可执行位已在 git 里（`ec3d73e`） |
| `$TOOL` `compile_tool.sh`、`$PORTTOOL` `compile_tool.sh` | 开发者编 IAPTool / PortTool，由各自的 `build.py` 调 bash 跑它 | 并进各自的 `build.py` | 现在是 cmd → Python → bash 三种语言；Windows 上找不到 bash 就编不了 |
| `$CORE_REPO` `system/extras/prebuild.sh` `postbuild.sh` | 用户的 IDE 每次编译（Windows 上经板卡包带的 busybox） | 保留 | 用户机器上不能假定装了 Python |
| `$TOOL` `tools/macos-launcher.sh`、`$CORE_REPO` `tools/discovery/macos-launcher.sh` | 用户的 Mac 上 IDE 直接执行 | 保留 | 同上；macOS 不再自带 Python |
| `$TOOL` `build.cmd`、`$PORTTOOL` `build.cmd` `delivery.cmd` | 双击入口，只调 `build.py` | 保留 | 一两行，Windows 双击只认它 |
| `$BOOT` `tools/restore_ld_script.bat` | CubeMX 生成代码后的钩子 | 见上表那一行 | 能不能直接调 `.py` 要真机确认 |
| `$CORE_REPO` `CI/update/gen_wrapper.sh` | 上游 STM32duino 的维护脚本（随 `init` 提交带进来） | 不动 | 不是我们的代码 |

没有 Linux / macOS 真机验证不了的：CubeIDE 在两平台的真实目录结构和插件后缀；Linux 上 ModemManager 抢 `/dev/ttyACM*`、dialout 组权限、ST-Link 的 udev 规则；macOS 上 IDE 传 `/dev/cu.*` 还是 `/dev/tty.*`、USB 拔出后串口读是报错还是一直读到 0 字节；macOS `networksetup` 列网卡是否完整（决策 51）；Renode 在两平台的 stdin 管道行为（T3-05、T1-27、T1-37 依赖它）。

用户 2026-10-16 定：IAPTool 加 macOS arm64（discovery 已有），Linux arm64 不加；macOS 真机测试环境用户来搭。做法：STM32Tools 的 `macosx/IAPTool` 改成按 CPU 选 `IAPTool-amd64` / `IAPTool-arm64` 的启动脚本，`platform.txt` 和直接调 `macosx/IAPTool` 的脚本都不用改。

## 怎么算答完

（目标平台已定）有真机时逐条跑一遍上面那串验证不了的，结果记进本票。

## Answer

## 引出了什么新的未知
