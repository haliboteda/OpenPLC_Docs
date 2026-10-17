# DO 方波这一项判的是什么

Type: grilling
Opened: 2026-10-11
Status: resolved
Blocked by: -

## Question

测试项 `dout.square` 跑的是 `mode=hold` 的 PWM 方波（频率、位数、占空比，决策 101），判据却接到方案里的 `dout-blink`（`mode=blink` 下标准机数翻转次数）——两者不是一回事（`$PORTTOOL/src/ptitems/ptitems.go`）。

| 选项 | 做法 | 代价 |
|---|---|---|
| A（推荐） | 拆开：`dout.blink`（标准机数翻转，判次数差 ≤ 1）和 `dout.square`（PWM，人工看示波器答是 / 否，只在研发测试） | 目录多一项 |
| B | `dout.square` 改成 `mode=blink`，只留翻转计数 | 研发测试里没有 PWM 这一项，决策 101 的分辨率没人测 |

## 怎么算答完

选定一种；要改的列进 TODO-fixture。

## Answer

2026-10-13 用户定「按推荐」：**A**。拆成 `dout.blink`（`mode=blink`，标准机数翻转，次数差 ≤ 1；对端人工时照[决策 108](../../../docs/tables/DECISIONS.md)并排显示板子翻转数和人填的数）和 `dout.square`（PWM，人看示波器答是 / 否，只在研发测试）。

## 引出了什么新的未知

没有。
