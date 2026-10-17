# 报告里安规那一步的 `type` 填什么：STG-08 和 STG-09 写法冲突

Type: grilling
Opened: 2026-10-11
Status: resolved
Blocked by: -

## Question

两张已关的票对同一个字段的写法不一样：

| 票 | 写法 |
|---|---|
| [STG-08 逐板结果记在哪](STG-08-where-per-board-results-go-in-a-full-run.md) | 每一步的 `type` 填步号 |
| [STG-09 安规测试预留什么](STG-09-what-the-safety-test-stage-reserves.md) | 安规那一步记成 `type: safety` |

现在的实现按 STG-08 做：安规那一步 `type` 填 `"5"`，`id` 填 `"safety"`，写在 `$PROD/docs/modules/M4/PORTTOOL-FLOW.md` C.3.3。

| 选项 | 做法 |
|---|---|
| A（推荐） | 保持现状，把 STG-09 那一句改成「`type` 填 5、`id` 填 `safety`」；按步号查记录的写法统一 |
| B | 改成 STG-09 的写法，`type` 填 `safety`；其他步跟着改用名字 |

## 怎么算答完

选定一种写法，两张票和 PORTTOOL-FLOW.md C.3.3 说的一致。

## Answer

2026-10-11 用户定：**「需要我的现在问，不需要的按推荐开始」**，本票按推荐：选 A：保持 `type` 填步号 5、`id` 填 `safety`，STG-09 那一句已改（决策 103）。

## 引出了什么新的未知

没有。
