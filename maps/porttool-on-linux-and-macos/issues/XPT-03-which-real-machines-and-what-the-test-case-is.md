# 在哪几台真机上验、用例怎么写

Type: grilling
Opened: 2026-09-30
Status: open
Blocked by: XPT-01, XPT-02

## Question

`T4-01` / `T4-02`（[M4-production-fixture.md](../../../docs/modules/M4-production-fixture.md)）只在 Windows 上跑过。终点要每个平台一条跑过的用例。要定：

- 有没有 Linux 实机、Mac 实机（WSL 默认接不到 USB 串口）；没有的话怎么办
- 每个平台的用例测什么：只打开面板连上模拟板，还是接真板子逐路测
- Linux 串口权限（`dialout` 组）由谁、在哪一步处理
- macOS 上 `ioreg` 补 VID 的解析，样本是手写的：在真 Mac 上录一份真输出替换 `$TOOL/internal/serialx` 里的测试样本

## 已有的事实

| 事实 | 出处 |
|---|---|
| **目前没有 Linux 实机，也没有 Mac 实机**；手头只有 Windows 机器上的 WSL（Debian 13），默认接不到 USB 串口 | 用户 2026-09-30 |
| **先做 Linux**：在 WSL 里用 `usbipd-win` 把板子的 USB 串口转进去，接真板子逐路测；Linux 没问题后再定 macOS | 用户 2026-09-30 |

## Linux 实测（2026-09-30，WSL Debian 13 + `usbipd-win` 4.3.0，真板子跑工装固件 0.10.0，`$TOOL` 在 `e5b7fdb`）

| 事实 | 怎么得到的 |
|---|---|
| WSL 空闲时虚拟机会停，挂进去的 USB 设备随之掉线；要让 WSL 里常驻一个进程再 `usbipd attach` | `ports` 两次突然列空，WSL `uptime` 只有几秒 |
| 串口权限不用处理：WSL 默认用户已在 `dialout` 组 | `id` |
| Linux 版 `ports` 列出全部四个口，VID/PID/序列号和 Windows 一致 | `PortTool ports` |
| 面板在 Linux 上能起、能列口、能连板子读出 15 张端口卡、能列方案 | `--no-browser` 起面板后用 `curl` 调 `/api/ports`、`/api/connect`、`/api/plans` |
| `bench-smoke.json`：Linux 7/7 过，和 Windows 相同 | `PortTool run`，控制口 PL2303 |
| `station6-poweron-relaxed.json`：**方案里写死 `"com": "COM16"` 当 RS485 对端，Linux 上打不开，RS485 一定失败** | Windows 17 过；Linux 原样跑 16 过，只多了 RS485 `miss=5` |
| 把对端改成 `/dev/ttyUSB0` 后 Linux 17 过，失败项和 Windows 完全相同（无 SD 卡、网口对端、DI 没接激励、KNX、人工确认读到 EOF） | 连跑 4 次；其中 1 次 RS485 报 `junk=1`，单跑 RS485 5 次全过；Windows 只跑了 1 次，不知道那边会不会也出 |
| 按 [DECISIONS.md](../../../docs/tables/DECISIONS.md) 第 73 条改完（`$TOOL` 未提交的改动）：Linux `ports` 显示芯片，如 `/dev/ttyUSB0 - USB Serial (ch341-uart)`；没选对端时 RS485 直接报「bind one once in the panel」；在面板里绑上后 Linux 连跑 3 次、Windows 1 次，都是 17 过，和改前 Windows 相同 | `PortTool ports` / `run`；绑定走面板的 `/api/link` |
| `T4-03`（面板在浏览器里点一遍，Linux 版跑在 WSL）：216 过 3 不过；同一脚本在 Windows 上跑 `T4-02`，结果完全相同。3 条都是台子今天的状态和 `run.py` 里写的预期不符：没插 SD 卡；电脑不在板子的网段（板子 `192.168.0.32`）；AI 判成「过」（`!ain … ch1=3265/124 ch2=6375/243`，即 MCU 引脚上 124 mV / 243 mV），脚本预期 D12/D13 没接信号源、应判不过 | `run.py --wsl Debian --port /dev/ttyUSB0` 与 `run.py --port COM12` |
| 插上 SD 卡、电脑和板子放进同一网段后重跑：`T4-03`（Linux）和 `T4-02`（Windows）都只剩 AI 一条不过，其余全过 | 同上 |
| AI 口硬件正在改，本图先不考虑 AI：`run.py` 对 ain 不判过也不判不过 | 用户 2026-09-30，见 [WAITING-ON.md](../../../waiting/WAITING-ON.md) |
| 不判 AI 之后：`T4-03`（Linux）和 `T4-02`（Windows）全部检查通过 | `run.py --wsl Debian --port /dev/ttyUSB0`；`run.py --port COM12` |
| `usbipd attach` 的先后决定 `ttyUSB` 编号：换一次顺序，PL2303 就从 `ttyUSB1` 变成了 `ttyUSB0` | `PortTool ports` |
| 没测到：桌面 Linux 上双击打开、`xdg-open` 开浏览器、udev 和串口权限（`T4-03` 的浏览器在 Windows 上） | — |

## 怎么算答完

写明每个平台用哪台机器（型号 / 系统版本）、用例编号和判据，以及这条用例测不到什么。
