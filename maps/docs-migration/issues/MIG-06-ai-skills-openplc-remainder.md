# AI-Skills/OpenPLC 搬空后剩什么

Type: grilling
Opened: 2026-09-16
Status: resolved
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

## Answer

2026-09-16 定并已执行。**`AI-Skills/OpenPLC/` 整个目录已删除 —— 它一个文件都不剩了。**

⚠️ **题面里「搬完不是空的」那条预判错了。** 它的依据是「`STATUS.md` 要劈成两半、
结果那半留下」，但执行时那个劈法被推翻了（需求和结果是同一行的不同列，劈不开），
`STATUS.md` 整份搬走，于是这里真的空了。

| 问的 | 答 |
|---|---|
| `/openplc:overview` 指向哪 | **它不存在，早在 2026-08-25 拆 plugin 层时就退役了。** `AI-Skills/README.md` 那张表记的是「它被什么取代」，不是「它还在」 |
| `_shared/rules/` 和 `sync_rules.py` | **不受影响。** 它们是跨项目的，和这个产品无关 |
| `AISupervisor/` | 不受影响 |
| `AI-Skills/README.md` | 已改：去掉 `OpenPLC/docs` 那一行，说明它 2026-09-16 搬进了 `OpenPLC_Docs`；「事实往哪放」那张表的第二行改成「那个产品自己的文档仓」 |

### 验证

`AI-Skills` 下已无任何 OpenPLC 产品级文档（`OpenPLC/` 目录已删）。
`selfcheck --quick` 13 项全 PASS，其中 P9 的扫描仍包含 `AI-Skills` 的 `_shared` 和 `README.md`。

## 引出了什么新的未知

**我的会话记忆里有三处把「`/openplc:overview`」当成现存入口讲**，已一并改掉 ——
那个 skill 退役了三周，记忆一直在拿它当到达路径。
**记忆不在 git 里，P9 看不见它，所以它漂了三周没有任何东西报警** ——
这正是这张图要堵的那种漏法，只不过发生在检查够不到的地方。
