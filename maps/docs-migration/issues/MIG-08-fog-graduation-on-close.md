# 关票时怎么强制回答「引出什么新未知」

Type: grilling
Opened: 2026-09-16
Status: resolved
Blocked by: MIG-01

## Question

迷雾只是个空格子，格子不会自己填满。靠收尾时人工回想，就是现在漏东西的原因。

要定：关一张票时，「这个答案引出了什么新的未知」这一问怎么变成**关不掉就过不去**的一步。
答「没有」也要明写，空着不算。

## 怎么算答完

关掉这张图上的任意一张票，走一遍流程 —— 没写这一节就关不掉。拿一张真票验，不是拿假设验。

## Answer

2026-09-16 定。检查脚本 [../../../tools/check_wayfinder_ticket_hygiene.py](../../../tools/check_wayfinder_ticket_hygiene.py)，
挂成 git 的 pre-commit 钩子 [../../../.githooks/pre-commit](../../../.githooks/pre-commit)（`core.hooksPath = .githooks`）。

**做成「提交不过去」，不是「约定里写着」。** 光写进约定就是靠自觉 ——
2026-09-16 这一轮里已经差点漏过一次（`逐份定去向` 引出的断链风险，
差点只留在已关票的正文里）。

脚本一次查五样，不止这一节：

| 查什么 | 为什么 |
|---|---|
| 四个头部字段齐不齐、取值合不合法 | 少一个，前沿就算错 |
| `## Question` 和 `## 怎么算答完` 在不在 | 「怎么算答完」要在动手前写，不是事后补 |
| `resolved` 的票有没有 `## Answer` **和** `## 引出了什么新的未知` | **本票的正题**。写「没有」可以，不写不行 |
| `## Answer` 第一行是不是 `YYYY-MM-DD` | 两年后读的人要判断它还算不算数 |
| `resolved` 的票有没有被它那张图的 `Decisions so far` 收录 | 堵「关了但图上没索引」—— 关掉即失踪 |

### 验证

`怎么算答完` 要求「拿一张真票验，不是拿假设验」：

拿已关的 `已知问题和待立项模块在新框架里住哪` 那张票，删掉 `## 引出了什么新的未知` 一节，
然后 `git commit` ——

```
Ticket hygiene: 1 problem(s) across 9 ticket(s).
  maps/docs-migration/issues/MIG-09-...md: resolved without section: ## 引出了什么新的未知

Commit refused.
```

**退出码 1，HEAD 停在 `2613a8f` 没动。** 之后恢复该票，全 9 张 clean，退出码 0。

## 引出了什么新的未知

1. **这道门禁绕得过。** `git commit --no-verify` 能跳过，而且 `core.hooksPath`
   是本机 git 配置、不在版本控制里。要不要一道绕不过的（进 `selfcheck`），
   归 `P7/P8/P9 和 selfcheck 怎么跟着搬` 那张票 —— 已写进它的题面。
2. **`core.hooksPath` 不随仓库走这件事，现在影响为零** ——
   2026-08-25 已定不再迁移到其他电脑，本机已配好。不必为此做什么。
