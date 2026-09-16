# 把文档收编进 OpenPLC_Docs，换成问题导向的框架

## Destination

`OpenPLC_Docs` 成为唯一的文档与问题入口：三个代码仓的 `docs/` 搬空、参考层按主题收编、问题走「图 + 票」。
并且**「还问不清楚的事」和「产出来却没有去处的东西」都有位置**，关票时强制回答。

## Notes

**为什么开这张图**（2026-09-16 定）：旧框架是**产物导向**的 —— `DECISIONS.md` 记已定的、`STATUS.md` 记已跑的、`ISSUES.md` 记已发现的。
**整套里没有一个位置放「我知道有件事要弄清楚，但现在还问不清楚」**，所以没做的事在系统里不存在，等它在工位上冒出来才补一条。
现成的样本：`$PROD/docs/ID-MAP.md` 里三张验收单的「结果记在哪」写着 ⬜「没有去处」，需求 F2 因此一直是 🟡。

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

## Decisions so far

<!-- 一张已关的票一行：一句话摘要 + 链接。详情在票里，这里不重复 -->

- [tracker 约定怎么写](issues/MIG-01-tracker-convention.md)：票的头部恰好四个字段，blocking 只写单向，前沿由脚本算且不进 `selfcheck`，关掉的票原地改状态不移走。约定落在 [MAP-AND-TICKET-CONVENTION.md](../MAP-AND-TICKET-CONVENTION.md)
- [参考层按什么分类](issues/MIG-02-reference-layer-taxonomy.md)：准入判据是「不会因为工作推进而变」，按**问题域**分成八类，总表不拆、状态表拆两半。分类表落在 [REFERENCE-LAYER-TAXONOMY.md](../../docs/REFERENCE-LAYER-TAXONOMY.md)
- [已知问题和待立项模块在新框架里住哪](issues/MIG-09-where-do-defects-and-modules-live.md)：「已知问题」不是一类东西，拆成五个去处（票 / 参考层 / `work/` / `waiting/` / 迷雾）。路由表落在 [WHERE-THINGS-LIVE.md](../../WHERE-THINGS-LIVE.md)
- [三十多份文件逐份定去向](issues/MIG-03-file-by-file-destination.md)：43 份逐一定死，零待定。表落在 [FILE-DESTINATIONS.md](../../docs/FILE-DESTINATIONS.md)
- [关票时怎么强制回答「引出什么新未知」](issues/MIG-08-fog-graduation-on-close.md)：做成 pre-commit 钩子，缺了那一节**提交就过不去**，不是约定里写着。脚本是 [check_wayfinder_ticket_hygiene.py](../../tools/check_wayfinder_ticket_hygiene.py)

## Not yet specified

- 现有 10 套编号在新框架下要不要合并，`$PROD/docs/ID-MAP.md` 本身往哪去（`MIG-` 是第 11 套，还没登记）
- 给人扫的那一面 —— 要不要一个索引页，长什么样
- 下一张图开什么（等工装的使用反馈 / 等校准那条线）
- **`ID-MAP.md` 该不该改成脚本扫出来** —— 手维护已经漂了：多列七条早删掉的，漏了一条真实存在的
- **IAP 协议在参考层没有独立文档** —— 产品核心协议只活在代码注释和决策条目里。要不要补一份、补成什么样
- **`STATUS.md` 的「最近结果」该由脚本生成，但生成器不存在** —— 现在手抄，这是三个数字对不上的原因
- **一张图走完之后怎么归档** —— `INDEX.md` 里标什么、`maps/<effort>/` 目录动不动。第二张图开起来之前要定

## Out of scope

- 工装的三条待办（异常可恢复、失败码、面板按九类分段）—— 2026-09-16 定为**等使用反馈**，不在这张图上
- 任何代码改动。这张图只动文档和记录方式
