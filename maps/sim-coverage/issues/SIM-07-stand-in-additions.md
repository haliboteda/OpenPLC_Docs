# 替身补齐：驱动、手势、故障注入、撤销、比版本

Type: task
Opened: 2026-10-03
Status: resolved
Blocked by: -

## Question

[SIM-05-findings.md](../SIM-05-findings.md) 列出替身（`$TEST/host/bootstand/`）补几样东西就能跑的用例。要补：

- `host/fakeboard/` 下一个驱动：摆好 `flash.bin` / `sram4.bin`、不清状态重启替身、读替身日志、调现成的 Go 用例
- 替身加 `--gesture none/upload/factory` 开关，照 `$BOOT/Core/Src/main.c:400-421`，用于 `T2-05`、`T2-09`、`T2-36`
- 替身的假 flash 加故障注入（第 N 次擦 / 写后退出），用于 `T1-22`
- 撤销的 `T2-19`、`T2-20` 在替身上跑，补 M2 脚注 ⁷ 说的 bootloader 侧 `resolve_chain()` 主机零覆盖
- 烧录前比版本（拒旧版、`--force` 只放行一次）给一个用例编号，写进 M1 用例表，在替身上跑

## 怎么算答完

- 以上每一项在 `$TEST` 里有可跑的入口，`python tools/selfcheck.py` 或 `host/fakeboard/run_cases.py` 能跑到并通过
- M1 / M2 用例表里对应各条的「条件」列写明「替身」，测不到的写在同一行
- 比版本有编号和 M1 表里的一行

## Answer

2026-10-04 做完：新驱动 `$TEST/host/fakeboard/run_lifecycle.py`（selfcheck 的 `T1-22` `T1-38` `T2-05` `T2-19` 四步）在替身上跑 `T1-22` `T1-38` `T2-05` `T2-09` `T2-19` `T2-20` `T2-36`，七条全过；`run_cases.py` 原有 9 条照旧全过。替身加了 `--gesture none|upload|factory`（照 `$BOOT/Core/Src/main.c` 开机窗口那段）和 `--fail-after-erase/-program N`（第 N 次擦 / 写后掉电，下一次冷启动）；比版本新编号 `T1-38`、需求 `R1-40`。替身证明的是真 bootloader 代码的决定；按键本身、真 flash 的擦写窗口、CDC 那支仍要真板子，各条的「条件」列写明了。

## 引出了什么新的未知

无。
