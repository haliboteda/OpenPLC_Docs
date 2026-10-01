# 整体测试项目叫什么、放在哪

Type: grilling
Opened: 2026-10-02
Status: resolved
Blocked by: -

## Question

整体测试（契约 + 整机）是新开一个仓，还是把 `IAPTranfer_Tool` 改成测试仓、IAPTool 另开仓；仓名；文档里的路径变量叫什么。

## 怎么算答完

仓名、位置、路径变量三样都定下来，并写进 `docs/repo/ARCHITECTURE.md` 的路径变量表。

## Answer

2026-10-02 定（用户新建了仓）。新仓 `OpenPLC_Test`（`git@github.com:haliboteda/OpenPLC_Test.git`），放在工作区里和其他仓并列；路径变量 `$TEST`，已写进 ARCHITECTURE.md。`IAPTranfer_Tool` 不改名，拆完只剩 IAPTool。

## 引出了什么新的未知

没有。
