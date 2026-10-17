# 方案里要人工填一个读数，用什么步骤

Type: grilling
Opened: 2026-10-11
Status: resolved
Blocked by: -

## Question

[STG-03](STG-03-what-each-port-tests-at-each-level.md) 定了 DO 带负载时人工判「端子电压 ≥ 供电 − 1 V」（TODO-fixture 第 40 条）。方案执行器里人工的步骤只有 `UserConfirm`，只能答是 / 否，填不了数。

| 选项 | 做法 | 代价 |
|---|---|---|
| A（推荐） | 加一种人工填数的步骤，填进去的数照常走 `ptcheck` 判限值，报告里留原始值 | 多一种步骤类型，面板和方案页都要能显示 |
| B | 用 `UserConfirm`，把判据写进提示：「量到的电压 ≥ 供电 − 1 V 吗？」 | 报告里没有量到的数，事后不能按新限值重判（违背 `ptreport`「原始值都留」） |

## 怎么算答完

选定 A 或 B；列进 TODO-fixture。

## Answer

2026-10-11 用户定：**「需要我的现在问，不需要的按推荐开始」**，本票按推荐：选 A：加人工填数的步骤，填的数走 `ptcheck` 判限值，报告留原始值（决策 103）。

## 引出了什么新的未知

没有。
