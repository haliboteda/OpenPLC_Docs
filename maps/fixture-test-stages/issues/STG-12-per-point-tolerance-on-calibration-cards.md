# 校准卡片上逐点的「过 / 不过」还留不留

Type: grilling
Opened: 2026-10-10
Status: resolved
Blocked by: -

## Question

决策 99 去掉了拟合残差的判据。校准卡片上还有一列判的是校准前每点相对标称的误差：AO 卡「合格判据（±% FS）」默认 2 %，AI 卡「逐点参考判据」默认 1 %，每点标过 / 不过并汇总「N 个点里 M 个超出」，不拦存档（`$PORTTOOL/src/ptpanel/web/index.html`）。这一列留着当参考，还是连同 `tolPct` 输入框一起删？

## 怎么算答完

定下留或删；删的话列进 TODO-fixture。

## Answer

2026-10-14 用户定。**留着当参考，AO 的默认值也是 1 %，和 AI 一样**（用户 2026-10-14：「AO也是1%」）。仍然只标过 / 不过、不拦存档。改代码见 [TODO-fixture.md](../../../work/TODO-fixture.md) 第 79 条。

## 引出了什么新的未知

无。
