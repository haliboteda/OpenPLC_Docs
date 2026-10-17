# 完整测试时 SN 必须填吗

Type: grilling
Opened: 2026-10-11
Status: resolved
Blocked by: -

## Question

安规卡片扫码录 SN，写进报告的 `sn` 字段，也决定记录文件名 `records/<UID>/<时间>[-<SN>].json` 带不带 SN（[STG-08](STG-08-where-per-board-results-go-in-a-full-run.md)、[STG-09](STG-09-what-the-safety-test-stage-reserves.md)）。STG-09 没说必须填，所以现在可以空着。

| 选项 | 代价 |
|---|---|
| A 可空（现状） | 没扫码的板子记录里没有 SN，按 SN 搜文件名找不回来，只能按 UID 找 |
| B 必填 | 没扫码就不让给安规结论；没有扫码枪的工位要手敲 |

## 怎么算答完

选定 A 或 B；选 B 的话列进 TODO-fixture。

## Answer

2026-10-11 用户定：**「需要我的现在问，不需要的按推荐开始」**，本票按推荐：选 A：SN 可空，没扫码的板子按 UID 找记录（决策 103）。

## 引出了什么新的未知

没有。
