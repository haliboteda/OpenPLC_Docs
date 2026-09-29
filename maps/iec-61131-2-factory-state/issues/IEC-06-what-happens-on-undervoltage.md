# 欠压和掉电时进入什么预定状态

Type: grilling
Opened: 2026-09-28
Status: open
Blocked by: -

## Question

标准 2003 6.3.2 要求欠压或长时间中断时维持正常运行，或进入预定状态并写明。板子测不了 24 V（[DECISIONS.md](../../../docs/tables/DECISIONS.md) 里「板子测不了任何电压和电流」那条），MCU 只能用 PVD / BOR 看 3V3。要定：开不开 PVD / BOR、阈值多少、触发后做什么（例如把所有输出置断开、打日志），还是在手册里写明「靠硬件自然掉电断开」。

## 怎么算答完

定下做法；如果开 PVD，拉低供电时能看到输出按规定落下。
