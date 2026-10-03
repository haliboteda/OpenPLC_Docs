# 标着「真板子」的用例里，哪些替身或 Renode 能跑

Type: research
Opened: 2026-10-03
Status: resolved
Blocked by: -

## Question

M1–M3 的用例表里不少标「真板子」，例如出厂无根第一次上传自动认领（`T2-35` USB、`T2-36` 网口）、`flashboot`、烧录前比版本、复位原因交到 app。逐条看：判据要观察的东西，bootloader 替身（`$TEST/host/bootstand/`）或 Renode 能不能给出来；已经有替身用例覆盖的标出来，能补的列出要补什么。

## 怎么算答完

- 一张表：每条标「真板子」的 `T1` / `T2` / `T3` 用例，替身能跑 / Renode 能跑 / 只能上板，各一句理由和出处

## Answer

2026-10-03：M1–M3 标「真板子」的 53 条用例里，替身上已经跑通 19 条，补一个驱动或小开关就能跑 20 条，替身或 Renode 都能补 2 条，Renode 能补 4 条，只能上板 8 条。逐条判定、理由和要补什么见 [SIM-05-findings.md](../SIM-05-findings.md)。替身只证明 IAP 的决策逻辑，不替代上板。

## 引出了什么新的未知

- 替身要补的驱动、恢复出厂手势开关、假 flash 故障注入、撤销两条和比版本的用例 —— 开成 [替身补齐：驱动、手势、故障注入、撤销、比版本](SIM-07-stand-in-additions.md)
- 顺带查出四处文档和代码对不上，已于同日改正（见 findings 末尾）
