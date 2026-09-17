# 工程约束那一层内部按什么分节

Type: grilling
Opened: 2026-09-17
Status: resolved
Blocked by: -

## Question

工程约束层的**成员已经定死**，要定的只剩它内部怎么分节。

**九条需求**（`ENG-01`–`ENG-09`，出自 [DR-02-id-mapping.md](../DR-02-id-mapping.md)）：
`E3` bootloader 镜像装得进保留的 flash、`D7` 版本三处一致、`D8` 跨仓镜像不静默分叉、
`D9` `$CORE_LIVE` 的改动确实进了 git、`F1` 一条命令跑完不用板子的检查、
`F5` 自动化全用 Python、`F3` 发版前有验收单、`F4` 捆绑升级风险写进发布说明、
`F2` 每块出厂板有逐板检查单。

**八份文档**（出自 [DR-05](DR-05-where-does-each-doc-file-go.md)）：
`build/` 四份（`BOOTLOADER-PROJECT-LAYOUT.md` `BUILD-AND-TEST.md` `CUBEMX-RULES.md`
`RTC-LSE-CHANGE.md`）、`repo/ARCHITECTURE.md`、`repo/CONVENTIONS.md`、
`production/TEST-DESIGN.md`、`tables/ACCEPTANCE-CHECKLIST.md`。

要定的是**分节的标准和节名** —— 而且标准要能套到将来新增的工程约束上，
不能是「这九条这八份恰好这么分」。

⚠️ **别复制模块层那套划分标准。** 模块层问「外面的人失去什么能力」，
工程约束按定义回答不了这个问题（不做到板子功能不变），所以它需要自己的一句判据。

## 怎么算答完

写下分节的**那一句标准**，以及按它分出来的节名；九条需求和八份文档逐一落进某一节，
**没有一条悬着**。并且拿一条不在上面清单里的工程约束试一下那句标准 ——
判得出去处才算这句话立得住。

## Answer

2026-09-17 定。**标准是「我现在处在开发流程的哪一步」**，分五节：

| 节 | 装什么 |
|---|---|
| **改代码时** | `CUBEMX-RULES.md`、`CONVENTIONS.md`、`RTC-LSE-CHANGE.md`、`ARCHITECTURE.md` |
| **构建时** | bootloader 镜像装得进保留的 flash、`BUILD-AND-TEST.md`、`BOOTLOADER-PROJECT-LAYOUT.md` |
| **提交前** | 版本三处一致 · 跨仓镜像不分叉 · `$CORE_LIVE` 的改动进了 git · 一条命令跑完不用板子的检查 · 自动化全用 Python、`TEST-DESIGN.md` |
| **发版时** | 发版前有验收单 · 捆绑升级风险写进发布说明、`ACCEPTANCE-CHECKLIST.md` |
| **出厂时** | 每块出厂板有逐板检查单 |

**为什么是这条标准**：它和模块层同构但不重复 —— 模块层按「外面的人要做什么」组织，
这层按「**我们自己要做什么**」组织，两层各答各的问题。
而且它判得出清单外的东西：拿「提交信息要写清楚」试，判得出是「提交前」；
换成「它在守什么不被破坏」那条标准就判不出来（提交信息没在守某个具体的东西）。

⚠️ **一个已知的勉强处，没有为它开例外**：`TEST-DESIGN.md`（测试系统怎么搭）
放在「提交前」不够贴切 —— 它是设计文档，不是某一刻要照着做的事。
**为一份文档破掉标准的代价更大**，所以留在「提交前」，并在这里写明它是勉强的。

## 引出了什么新的未知

没有。
