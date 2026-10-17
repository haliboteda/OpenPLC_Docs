# 方案怎么同时驱动标准机（或上位机的 USB-CAN）当对端

Type: grilling
Opened: 2026-10-11
Status: resolved
Blocked by: -

## Question

下面这几条都要「被测板以外的另一端」配合，而方案执行器（`$PORTTOOL/src/ptplan` 的 `Step` / `Peer`）只认一块板子：

| TODO-fixture | 要另一端做什么 |
|---|---|
| 37 产线 CAN 对发 | 标准机跑 `can mode=echo`，或上位机的 USB-CAN 转换器回送 |
| 40 DI 走位 8 拍 | 标准机的 DO 逐路走位 |
| 40 DO 带负载、标准机读 | 标准机的 DI 读被测板的 DO |
| 40 方波 blink 翻转次数 | 标准机的 DI 数翻转 |

只把 CAN 步改成 `mode=normal` 而没有对端，这一步在每个台子上都会失败，所以第 37、40 条的这几项还没改。

要定的：

1. 方案文件里怎么写对端（第二个串口、哪一步在哪块板上跑）
2. 谁去启动标准机上的会话、什么时候停
3. 上位机做 CAN 对端时用哪款转换器。台子上现在是 CANable 2.0，走 SLCAN（驱动在 `$TEST/tools/can_send.py` 的 `Analyser`）

## 怎么算答完

三点各有定案，写进 STG-03 或决策表；实现列进 TODO-fixture。

## Answer

2026-10-11 用户定：**「需要我的现在问，不需要的按推荐开始」**，本票按推荐：面板接第二块板（标准机）作为第二条板子连接，测试项目录里标明哪一步在标准机上跑什么，方案文件的步骤加 `on: ref`；对端会话由执行器在被测板那一步之前启动、之后停止，沿用 deadman 续期；上位机做 CAN 对端用台子上现有的 CANable 2.0（SLCAN），Go 里实现驱动（决策 103）。

## 引出了什么新的未知

没有。
