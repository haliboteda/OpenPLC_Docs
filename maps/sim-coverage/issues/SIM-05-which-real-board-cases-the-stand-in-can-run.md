# 标着「真板子」的用例里，哪些替身或 Renode 能跑

Type: research
Opened: 2026-10-03
Status: open
Blocked by: -

## Question

M1–M3 的用例表里不少标「真板子」，例如出厂无根第一次上传自动认领（`T2-35` USB、`T2-36` 网口）、`flashboot`、烧录前比版本、复位原因交到 app。逐条看：判据要观察的东西，bootloader 替身（`$TEST/host/bootstand/`）或 Renode 能不能给出来；已经有替身用例覆盖的标出来，能补的列出要补什么。

## 怎么算答完

- 一张表：每条标「真板子」的 `T1` / `T2` / `T3` 用例，替身能跑 / Renode 能跑 / 只能上板，各一句理由和出处
