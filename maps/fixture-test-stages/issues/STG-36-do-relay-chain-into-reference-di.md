# DO → 继电器 → 标准机 DI 这条链的两处细节

Type: grilling
Opened: 2026-10-15
Status: resolved
Blocked by: -

## Question

[决策 133](../../../docs/tables/DECISIONS.md) 定了工装完整测试里被测板 DO 经继电器触点接标准机 DI。两处还没定：

| 事 | 背景 | A（推荐） | B |
|---|---|---|---|
| DO7、DO8 | DO 8 路（[STG-02](STG-02-what-the-reference-board-is.md) 第 2 行），继电器只有 RY1–RY6（[HARDWARE-FACTS.md](../../../docs/hardware/HARDWARE-FACTS.md)「继电器 RY1–RY6」）；DO1–6 各串一个继电器 | DO7、DO8 直接接标准机 DI7、DI8 | DO7、DO8 在工装测试里不测 |
| 「标准机核定电压」 | 标准机 DI 只读高 / 低，读不出电压值；原来「DO 带负载」判压降 ≤ 1 V 要人拿表量 | 读到高就算 DO 输出正常，压降不判 | 另加读电压的通道（标准机 AI 只有两路且焊成电流档，STG-02 第 5 行，不够 8 路） |

## 怎么算答完

两行各选定一种，写进决策 133 和 PORTTOOL-FLOW；要改的列进 TODO-fixture。

## Answer

2026-10-15 两行都选 A：

- **「标准机核定电压」**：A。用户 2026-10-15：「不论加什么硬件，对应那边DO就是高就是高，低就是低，只要匹配就是正确的」
- **DO7、DO8**：A。用户 2026-10-15「按推荐」：直接接标准机 DI7、DI8

## 引出了什么新的未知

没有。代码改动记在 TODO-fixture 第 83 条。
