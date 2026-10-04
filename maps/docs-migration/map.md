# 把文档收编进 OpenPLC_Docs，换成问题导向的框架

## Destination

`OpenPLC_Docs` 成为唯一的文档与问题入口：三个代码仓的 `docs/` 搬空、参考层按主题收编、问题走「图 + 票」。
并且**「还问不清楚的事」和「产出来却没有去处的东西」都有位置**，关票时强制回答。

## Notes

**为什么开这张图**（2026-09-16 定）：旧框架是**产物导向**的 —— `DECISIONS.md` 记已定的、`STATUS.md` 记已跑的、ISSUES.md 记已发现的。
**整套里没有一个位置放「我知道有件事要弄清楚，但现在还问不清楚」**，所以没做的事在系统里不存在，等它在工位上冒出来才补一条。
现成的样本：`$PROD/docs/tables/ID-MAP.md` 里三张验收单的「结果记在哪」写着 ⬜「没有去处」，需求 F2 因此一直是 🟡。

**这张图上的规矩**：

- **主读者是 AI 会话**，目的是让它一次读完就建起系统框架。人读是为了帮 AI 读得准。
- **文档只写能判真假的话。** 判不了真假的句子就是将来会漂的那些。
- **每张票先写「怎么算答完」**，答完拿它对。
- **编号 `MIG-NN` 只活在文件名里**，正文和对话一律用票的标题。
- 文档中文；代码注释、工具 stdout/stderr、README 英文。
- 每张票开工时 consult `grilling` 和 `domain-modeling`。
- **这张图执行到底，不只是规划**（wayfinder 默认只做决策，这里按它的 Notes 机制覆盖）——
  终点里「三个代码仓的 `docs/` 搬空」是一个真的改动，不是一份交出去的方案。
- **用户 2026-09-16 定：需要他动手或授权的事提前一次说清，其余按推荐直接走，不要逐张票请示。**
  ⚠️ 这意味着 `grilling` 票由我按推荐拍板并记录，不再逐问等答复 —— 他随时可以推翻某一条。

## 全集

这张图的范围由这个决定，**关最后一张票之前重跑一遍对账**：

```
find . -maxdepth 3 -name .git -not -path '*/node_modules/*'
```

⚠️ **补记于 2026-09-16，这张图关掉之后。** 当时终点写的是「三个代码仓」，
重跑这条命令会得到 **12 个仓** —— 那两批漏掉的（另外四个仓、66 处源码注释）本来当场就能捞出来。

## Decisions so far

<!-- 一张已关的票一行：一句话摘要 + 链接。详情在票里，这里不重复 -->

- [tracker 约定怎么写](issues/MIG-01-tracker-convention.md)：票的头部恰好四个字段，blocking 只写单向，前沿由脚本算且不进 `selfcheck`，关掉的票原地改状态不移走。约定落在 [MAP-AND-TICKET-CONVENTION.md](../MAP-AND-TICKET-CONVENTION.md)
- [参考层按什么分类](issues/MIG-02-reference-layer-taxonomy.md)：准入判据是「不会因为工作推进而变」，按**问题域**分成八类，总表不拆、状态表拆两半。分类表落在 [REFERENCE-LAYER-TAXONOMY.md](../../docs/modules/)
- [已知问题和待立项模块在新框架里住哪](issues/MIG-09-where-do-defects-and-modules-live.md)：「已知问题」不是一类东西，拆成五个去处（票 / 参考层 / `work/` / `waiting/` / 迷雾）。路由表落在 [WHERE-THINGS-LIVE.md](../../WHERE-THINGS-LIVE.md)
- [三十多份文件逐份定去向](issues/MIG-03-file-by-file-destination.md)：43 份逐一定死，零待定。表落在 [FILE-DESTINATIONS.md](../../docs/modules/)
- [关票时怎么强制回答「引出什么新未知」](issues/MIG-08-fog-graduation-on-close.md)：做成 pre-commit 钩子，缺了那一节**提交就过不去**，不是约定里写着。脚本是 [check_wayfinder_ticket_hygiene.py](../../tools/check_wayfinder_ticket_hygiene.py)
- [「没有去处」怎么报错](issues/MIG-07-no-destination-must-fail.md)：路由表补第六问「跑出来的数据」，并规定**占位符同一行必须指出一张票**，由 [check_no_orphan_placeholders.py](../../tools/check_no_orphan_placeholders.py) 在 pre-commit 上拦住
- [P7/P8/P9 和 selfcheck 怎么跟着搬](issues/MIG-05-doc-checks-follow.md)：`$PROD` 改指向本仓（不新造变量），脚本各留各家，新增 **P12** 把本仓的检查搬进 `selfcheck`，搬迁顺序定为**加 → 搬 → 减**
- [各仓 CLAUDE.md 改成什么](issues/MIG-04-claude-md-entrypoints.md)：四个入口各留一句**短**指针，不复述内容 —— 写成同一句长话时 P8 当场报重复
- [AI-Skills/OpenPLC 搬空后剩什么](issues/MIG-06-ai-skills-openplc-remainder.md)：**什么都不剩，目录已删**。`/openplc:*` skill 早在 2026-08-25 就退役了

## Not yet specified

2026-09-24 清理：编号合并由 [按功能模块重做文档与编号](../docs-restructure/map.md) 做完；`STATUS.md` 已没有「最近结果」栏；之后又开了六张图；归档写进了 [图与票的约定](../MAP-AND-TICKET-CONVENTION.md)；`ID-MAP.md` 补登了 `P12`–`P17` 和全部票号前缀。`ID-MAP` 改脚本生成、IAP 协议文档两条转入 [TODO「等外部」](../../work/TODO.md)。

## Out of scope

- 工装的三条待办（异常可恢复、失败码、面板按九类分段）—— 2026-09-16 定为**等使用反馈**，不在这张图上
- 任何代码改动。这张图只动文档和记录方式
- **逐板验收记录（`CHK-*` 的结果）到底存在哪** —— 那是产测那条线的事（需求 F2），不是文档框架的事。见 [「没有去处」怎么报错](issues/MIG-07-no-destination-must-fail.md)。搬迁时检查会拦住它，逼着当时回答

- **给人扫的索引页** —— 没有具体读者和场景。2026-09-24 划出
