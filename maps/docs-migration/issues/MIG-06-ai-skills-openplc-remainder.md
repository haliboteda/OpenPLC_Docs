# AI-Skills/OpenPLC 搬空后剩什么

Type: grilling
Opened: 2026-09-16
Status: open
Blocked by: MIG-03

## Question

`AI-Skills/OpenPLC/` 现在既放产品级文档，又是 `openplc` plugin 的宿主（`/openplc:overview` 从那来）。

`docs/` 搬走之后：plugin 还留不留、`/openplc:overview` 指向哪、
`_shared/rules/` 和 `sync_rules.py` 受不受影响。

⚠️ **搬完不是空的**（2026-09-16 由 `逐份定去向` 那张票定的）：`STATUS.md` 劈开之后
「最近结果 / 证据日期」两列**原样留在 `AI-Skills`**，因为生成器还不存在。
所以这张票要回答的是「还剩这一处产品级内容，怎么办」，不是「怎么清空」。

## 怎么算答完

跑一次 `/openplc:overview`，它指到的每个位置都存在。`AI-Skills` 里不再有任何一份产品级文档。
