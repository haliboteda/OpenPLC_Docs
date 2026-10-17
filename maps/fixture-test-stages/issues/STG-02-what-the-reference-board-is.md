# 标准机和被测板之间接哪些线

Type: grilling
Opened: 2026-10-09
Status: resolved
Blocked by: -

## Question

标准机和被测板之间接哪些线：AO↔AI、DO↔DI，还有哪些？

已定的：标准机跑工装固件，讲工装协议，在面板连接区有自己的口（决策 97）；RS232、RS485 的对端是上位机，CAN 对发的对端可选标准机或上位机（决策 98）；KNX 只在研发测试，产线不需要对端。

## 怎么算答完

一张接线表：标准机端子 ↔ 被测板端子 ↔ 用在哪个测试项。

## Answer

2026-10-10 用户定。

| # | 标准机 | 被测板 | 用在哪个测试项 |
|---|---|---|---|
| 1 | DO1–8 | DI1–8 | DI 逐路读电平 |
| 2 | DI1–8 | DO1–8 | DO 带负载输出，对端选标准机时 |
| 3 | AO（电流） | AI2（电流档） | AI2 读数 |
| 4 | — | AI1（电压档） | AI1 读数：标准值由人工或仪器给，标准机 AO 只出电流（XTR111，`$HW/UpperDeck_overview.txt`） |
| 5 | AI1、AI2（都焊成电流档） | AO1、AO2 | AO 输出，对端选标准机时；两路同时读 |
| 6 | CAN | CAN | CAN 对发，对端选标准机时 |
| 7 | GND | GND | 共用 |

标准机的两路 AI 都焊成电流档：AI 每路都能焊成电压或电流档（用户 2026-10-10；[HARDWARE-FACTS.md](../../../docs/hardware/HARDWARE-FACTS.md)「档位决定」）。

## 引出了什么新的未知

- CAN 两头的终端电阻接不接（出厂断开，[HARDWARE-FACTS.md](../../../docs/hardware/HARDWARE-FACTS.md)「终端电阻出厂是断开的」），并进 [第一台标准机怎么做](STG-11-how-the-first-reference-board-gets-made.md)
