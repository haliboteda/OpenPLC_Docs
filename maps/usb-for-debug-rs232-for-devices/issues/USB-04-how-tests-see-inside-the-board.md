# 测试靠什么看板子内部

Type: grilling
Opened: 2026-10-17
Status: resolved
Blocked by: USB-01

## Question

30 个上板脚本（`$TEST/tools/`，如 `flash_bootloader.py` 判 `T3-01` 的 SDRAM 自检行）和 4 个 Renode 脚本靠 RS232 日志判过不过；bootloader 替身也读它的输出。RS232 不再有日志后，测试换什么通道：USB、ST-Link（SWO / RTT）、诊断记录，还是测试版固件保留 RS232。

讨论中已定（用户 2026-10-17）：

| 事 | 定了什么 |
|---|---|
| 上板脚本 | 读 USB 口 1、只认 `[sys]` 行，交权后按 VID / PID + UID 重新找口（按推荐） |
| Renode | 模拟编译时口 1 内容落到 UART（同 SIM-01 的做法），开机缓存用 `sysbus` 从 SRAM4 读（按推荐） |
| 判据 | 行的内容不变，只换通道（按推荐） |
| USB 坏了 | 人工改走网口（读缓存），网口也坏了再用 SWO；USB 和网口都能调试和升级（用户原话：「网口和usb都是可以用来调试和升级的，如果都坏了，就用swo」） |

## 怎么算答完

上板脚本、Renode、替身各自改从哪读板子的输出定下，写进 HOW-TO-RUN-TESTS；要改的脚本清单能据此列出。

## Answer

2026-10-17 定，逐条见上面「讨论中已定」那张表；写进 [HOW-TO-RUN-TESTS.md](../../../docs/engineering/HOW-TO-RUN-TESTS.md)「测试从哪读板子的输出」。

## 引出了什么新的未知

- 30 个上板脚本、4 个 Renode 脚本的逐个改法和一个「按身份重新找口」的公共函数
