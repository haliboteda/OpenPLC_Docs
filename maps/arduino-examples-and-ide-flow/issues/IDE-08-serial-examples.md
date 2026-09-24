# 串口例程：RS232、RS485、USB 串口

Type: task
Opened: 2026-09-24
Status: resolved
Blocked by: IDE-05

## Question

照定下的格式写三个例程。RS485 要手动控方向脚；RS232 和 printf 共用 USART3。

## 怎么算答完

三个例程在 `P5` 里编过；接线（需要什么对端）写清。

## Answer

2026-09-25 定。写了 `RS232_Echo`（先拉高 `RS232_EN_Pin`，用 core 的 `Serial_Test`）、`RS485_Echo`（发送时拉高 `RS485_DIR_Pin`，发完 `flush()` 再拉低）、`USB_Serial`。

`P5` 全量 48 个例程 0 失败（2026-09-25）。**只编译过，没上过板**。上板逐个验落在 [TODO.md](../../../work/TODO.md)「端口例程逐个上板验」。

## 引出了什么新的未知

没有。
