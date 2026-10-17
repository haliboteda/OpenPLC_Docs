# PC 怎么知道板子上烧了哪几路校准值、k 和 b 各是多少

Type: grilling
Opened: 2026-10-11
Status: resolved
Blocked by: -

## Question

工装完整测试的门槛（没烧校准值不让开始）、AI / AO「读数 / 输出」项按板上公式换算、制作标准机先查校准值，都要读到板子上的 k、b（决策 97）。工装固件现在不读扇区 15，`pt.id` 只报 uid（`$BOOT/TestCase/porttool/porttool.c`）。

| 选项 | 做法 | 代价 |
|---|---|---|
| A（推荐） | 固件加只读的 `pt.cal`，原样报出校准值区前 56 字节，PC 用 `calarea.Decode` 解 | 改固件、模拟板桩和 T4-01 的 golden；固件仍不写 flash |
| B | 每次用 ST-Link 读扇区 15 | 第 2、4 步也得插着 ST-Link，读一次几秒 |
| C | 信 PC 本地的烧录记录 | 板子重烧或换板后不准，门槛形同虚设 |

## 怎么算答完

选定一种，写进决策表；要改的列进 TODO-fixture 第 38 条。

## Answer

2026-10-11 用户定：**「A 并且按推荐来」**（STG-23 选 A，STG-24 到 STG-28 按推荐），见决策 102。选 A：固件加只读的 `pt.cal`，原样报出校准值区，PC 用 `calarea.Decode` 解。

## 引出了什么新的未知

没有。
