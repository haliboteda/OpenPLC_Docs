# 八种事件日志留不留，留的话住哪

Type: grilling
Opened: 2026-09-20
Status: open
Blocked by: -

## Question

metadata 搬进 app 头部之后，journal 扇区里只剩事件日志。**它留不留？**

已经核实过的事实（开图前定，见 map 的 `Decisions so far`）：

- 八种事件（`UPDATE_OK` / `CRC_FAIL` / `SIG_FAIL` / `AUTH_FAIL` / `OVERFLOW_ABORT` / `BOOT_VERIFY_FAIL` / `JOURNAL_RECLAIMED` / `FLASH_WRITE_FAIL`）**支撑 0 条需求**
- **零在线读出路径** —— 上位机 grep `journal` 零命中；`dropped_events()` / `journal_full()` /
  `auth_fail_log()` / `auth_fail_count()` 在 `bootloader_state.c` 之外零调用者
- 唯一被消费的是 `last_log_event()`，用来防止 `BOOT_VERIFY_FAIL` 每次启动重复写 —— **自指**
- ⚠️ `bootloader_state.h` 的注释说满状态会出现在 identity 字符串里，**实际没有**（`iap_identity_string()` 只看 `app_is_valid`）。这是一处待改的文档漂移
- 今天唯一的实际用途：事故后拿 ST-Link dump 扇区、人工解析

三条路，代价差很多：

| | 做法 | 得到 | 失去 |
|---|---|---|---|
| **L1** | **砍掉** | `bootloader_state.{c,h}` 501 行大部分消失；扇区完全空出来 | 离线取证能力 |
| **L2** | **原样留在那个扇区** | 取证能力保住，改动最小 | 扇区不能挪作他用；`reclaim` 逻辑还要留着（而它现在只由 `save_metadata` 触发，那条路没了之后**谁来触发回收**是个新问题） |
| **L3** | **留，并补上读出路径** | 前几轮发现的两个缺口（撤销无痕、`BOOT_VERIFY_FAIL` 三合一）才有意义解决 | 跨两个仓，工作量最大 |

⚠️ **L2 有一个非显而易见的坑**：`journal_reclaim()` 今天是从 `bootloader_state_save_metadata()`
里调的，而且注释写明那是**唯一安全的擦除时机**（新镜像已写进 app 区，旧证明已作废）。
metadata 不再走 journal 之后，**那个时机不存在了** —— 日志写满之后靠什么回收，要一并回答。

## 怎么算答完

1. 选定 L1 / L2 / L3 之一，一句话定论
2. 选 L2 或 L3 的话：**回答「日志写满之后靠什么触发回收」**，并说明新的擦除时机为什么安全
   （对照今天那条论证：擦的那一刻旧数据已经作废，掉电最坏结果本来就已成立）
3. 选 L1 的话：点名 `R1-28`（metadata 和事件记在 journal 里，一次成功升级 = 8 槽）和
   `R1-29`（journal 扇区满了能 reclaim 并恢复）**各自是删除还是重写**，以及
   `T1-26`、`T1-28` 两条用例怎么处置
