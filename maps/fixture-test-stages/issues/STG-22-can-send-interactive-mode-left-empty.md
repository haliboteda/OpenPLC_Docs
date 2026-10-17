# `can_send.py` 的交互模式已经没有板端对象

Type: grilling
Opened: 2026-10-11
Status: resolved
Blocked by: -

## Question

第 33 条删掉了旧的 CAN 板端 echo（决策 87）。`$TEST/tools/can_send.py` 的交互模式原来就是和它对发的，现在没有东西可以对；文件里的 `Analyser` 类还在被 `$TEST/tools/run_examples.py` 使用。

| 选项 | 做法 | 代价 |
|---|---|---|
| A（推荐） | 删掉交互模式，只保留 `Analyser` | STG-18 定下来之前，台子上没有现成的 CAN 手工收发脚本 |
| B | 保留不动 | 留着一段已经用不了的入口 |

## 怎么算答完

选定一种；要改的列进 TODO-fixture。

## Answer

2026-10-11 用户定：**「需要我的现在问，不需要的按推荐开始」**，本票按推荐：选 A：删掉 `can_send.py` 的交互模式，只保留 `Analyser`（决策 103）。

## 引出了什么新的未知

没有。
