# 交付包怎么带上 Linux 版

Type: grilling
Opened: 2026-10-16
Status: resolved
Blocked by: -

## Question

[TODO-fixture.md](../../../work/TODO-fixture.md) 第 91 条：`$PORTTOOL/Output/delivery/` 只有 Windows 版（`PortTool.exe`、`start.cmd`）。[决策 131](../../../docs/tables/DECISIONS.md)（三个平台都要能用）要求补 Linux 版。要定下面四件：

| # | 要定的事 | 背景 |
|---|---|---|
| 1 | ~~交付包发 Linux 可执行文件和 XPT-04 冲突~~ | 已答（用户 2026-10-16）：源码和可执行文件都提供，可执行文件单独处理；XPT-04 已同步改 |
| 2 | ~~Linux（和 macOS）模拟板用什么编~~ 已答（用户 2026-10-16）：**zig cc**，装在 `D:\Soft\zig`，路径由 `init_machine.py` 的 `ZIG` 写进本机配置；`build.py --sim --target <平台>` 交叉编 | [决策 112](../../../docs/tables/DECISIONS.md)要求交付包带模拟板。模拟板是工装固件的 C 代码在电脑上编成的程序（`$PORTTOOL/src/simboard/c/sim_main.c` 包含 `porttool.c`），要一个能出 Linux 程序的 C 编译器。本机只有 MinGW（`x86_64-w64-mingw32`，只出 Windows 程序），WSL Debian 里没有 gcc。候选：zig cc（MIT 许可，Windows 上一个压缩包）；WSL 里 `apt install gcc`（只出 Linux）。**2026-10-16 实测 zig 0.17.0**：在 Windows 上编出 `x86_64-linux-musl`（静态）、`x86_64-macos`、`aarch64-macos` 三个模拟板，Linux 版在 WSL 里回 `pt.caps` 正常，macOS 版没机器跑。顺带修了 `sim_main.c` 在 Linux 上编不过（`-std=c11` 下 `clock_gettime` 不可见，换 gcc 也一样） |
| 3 | 包怎么组织 | 见下面的方案表 |
| 4 | ~~macOS 要不要这次一起补~~ | 已答（用户 2026-10-16「我希望代码是兼容多平台的」）：要。KNX 那部分见 [macOS 上 KNX USB 接口怎么接](XPT-06-knx-usb-on-macos.md)；没有 Mac 真机，验证归 XPT-03 |

| 方案 | 做法 | 代价 | 风险 | 推荐 |
|---|---|---|---|---|
| **A** | 同一个文件夹放两个平台的文件：加 `PortTool`、`start.sh`、`stage6/IAPTool`。`start.sh` 一开头先 `chmod +x` | 最小，包大约多 20 MB | 双击 `start.sh` 可能只当文本打开，所以说明里只写 `bash start.sh` | ✅ 推荐。代码已经按平台挑文件名；固件、方案、`stage6` 只有一份；U 盘或 zip 丢了可执行位也不影响 |
| B | 分成 `delivery/windows/` 和 `delivery/linux/` 两套 | 共用的文件存两份；`delivery.cmd`、`build.py`、文档里的路径都要改 | 两份可能不一致 | 不推荐 |
| C | A 之外再出一个 `delivery-linux.tar.gz`（打包时写上 0755） | 多一步打包 | 小 | 需要单个文件发出去时再加 |
| D | Windows 出 zip、Linux 出 tar.gz，不再交文件夹 | 改掉现在的交付方式 | 同 B | 不推荐 |

## 已有的事实

| 事实 | 出处 |
|---|---|
| 固件 `.hex`、`plans/`、`stage6/bootloader.hex`、`stage6/FixtureDemo.ino.bin` 和平台无关，两个平台共用 | `$PORTTOOL/tools/ptbuild/deliver.go`（原 `make_delivery.py`，决策 149 后改写成 Go） |
| `Output/linux/PortTool` 已经编出；`$TOOL/Output/linux/IAPTool` 已有；PortTool 在 Linux 上找的就是 `IAPTool` 和 `porttool_simboard` | `$PORTTOOL/src/ptstages/userlevel.go:32-37`、`src/simboard/simboard.go:73-78` |
| Linux 上找 `STM32_Programmer_CLI` 只查 PATH，没有默认安装路径；第 6 步和 ST-Link 探测都靠它 | `$PORTTOOL/src/stlink/stlink.go:56-71` |
| `Output/delivery/` 现在那份是 10-13 打的（0.13.0），比脚本旧 | `make_delivery.py:518` 已经会拷模拟板 |
| 没验证过：Linux 上用 `IAPTool cdc` 真上传；CubeProgrammer 在 Linux 上的默认安装路径；ST-Link 和 `/dev/hidraw` 的 udev 权限 | 只能在 WSL + usbipd 上验 |

## 怎么算答完

四件各定一种。照定的改 `make_delivery.py`、`stlink.go`（补 Linux 默认路径）、中英 README、[PORTTOOL-FLOW.md](../../../docs/modules/M4/PORTTOOL-FLOW.md) C.4「交付包」、`$PORTTOOL/CLAUDE.md` 构建表、`delivery.cmd` 的提示。

## Answer

2026-10-16 用户定：**A**，Windows 和 Linux 放在同一个文件夹；其余照推荐（macOS 暂不进包；命令行帮助的例子同时写 `COM7` 和 `/dev/ttyUSB0`）。包里有什么见 [PORTTOOL-FLOW.md](../../../docs/modules/M4/PORTTOOL-FLOW.md) C.4「交付包」。

## 引出了什么新的未知
