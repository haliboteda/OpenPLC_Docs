# 八种事件日志留不留，留的话住哪

Type: grilling
Opened: 2026-09-20
Status: resolved
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

## Answer

2026-09-20 定

**选 L1：八种事件日志全删，连同它的文档一起删。**

用户原话：**「我目前不想留日志。日志全删掉，文档也删」**

理由已经在开图前核实过（见 map 的 `Decisions so far`）：**支撑 0 条需求、零在线读出路径、
唯一被消费的 `last_log_event()` 是给日志自己去重**。删掉不损失任何被证明过的能力。

**「日志写满之后靠什么回收」这个问题一并消失** —— 没有日志就没有 `journal_reclaim()`，
连带 `s_format_unknown`、`s_dropped_events`、`prev_hash` 链、`IAP_EVT_*` 八个枚举全部退场。

### 要删的

| 在哪 | 删什么 |
|---|---|
| `$BOOT/IAPServer/bootloader_state.{c,h}` | `journal_log()` / `journal_reclaim()` / `journal_write()` / `iap_log_rec_t` / `bootloader_event_type_t` 八个枚举 / 四个零调用者的导出函数（`dropped_events` `journal_full` `auth_fail_log` `auth_fail_count`）/ `last_log_event()` |
| `$BOOT/IAPServer/IAP_server.c` | 九处 `bootloader_state_log_event()` 调用；`IAP_server.c:662` 那段 `BOOT_VERIFY_FAIL` 去重 |
| `$PROD/docs/modules/M1/SECTOR-15.md` | **整份删除** |
| `$PROD/docs/modules/M1-firmware-upgrade.md` | 「日志的四条规则」一节、八种事件那一段、`R1-28` 重写、`R1-29` 删除 |
| `$TEST/tools/run_journal_reclaim.py` | 删（`T1-28` 的驱动） |
| `$TEST/tools/run_journal_slot_accounting.py` | 删（`T1-26` 的驱动） |
| `$PROD/docs/tables/` 各表 | `T1-26`、`T1-28` 两条用例删除；`R1-29` 删除 |

### 附带效果

`IAP_STATE_SECTOR_ADDR` 那个扇区**会完全空出来**（不是部分空出来），
所以 [让出来的 128 KiB state 扇区给谁](HDR-03-who-gets-the-freed-sector.md) 的三个候选都成立，没有被日志占掉的那部分。

## 引出了什么新的未知

一条：**`AUTH_FAIL` 的 RAM 环形缓冲（`iap_auth_fail_entry_t s_auth_fail[32]`，`bootloader_state_note_auth_fail()`）算不算「日志」？**

它**不占 flash**（刻意设计成 RAM-only，防止未认证调用者磨损扇区），但它的两个读取函数
`auth_fail_log()` / `auth_fail_count()` 同样是零调用者 —— 写进去从来没人读。

按本票的口径它该一起删，但它和 flash 日志不是同一个东西，**删它属于清理死代码，要单独确认**。
已记进 map 的 `Not yet specified`。
