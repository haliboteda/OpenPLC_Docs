# KNX 库的 TP 收发怎么在本板上发出合法帧

Type: grilling
Opened: 2026-09-29
Status: open
Blocked by: -

## Question

`OpenPLC_KNX` 用 USART1（19200 8E1）驱动 STKNX，而 STKNX 是裸模拟收发器，位时序要 MCU 用定时器产生（TIM12_CH1 发、TIM1_CH3 收）；工装固件的 `porttool_knx.c` 用脉冲时序在真总线上收发过真帧。库的 TP 物理层是改成定时器驱动（照工装那套），还是先上板验证现有 UART 路径到底行不行；PB14 空闲为高会不会一直往总线上打脉冲。

## 怎么算答完

先在真板上用 ETS 看现有库发的帧（总线只接电源 + ETS），得出行 / 不行；不行就定下改法（移植哪部分、放在哪层），改完后 ETS 里能看到板子发的组报文、板子能打印 ETS 发来的报文。
