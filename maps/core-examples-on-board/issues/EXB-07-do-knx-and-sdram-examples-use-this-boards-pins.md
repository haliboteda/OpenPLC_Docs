# KNX 和 SDRAM 例程写死的引脚和本板对得上吗

Type: research
Opened: 2026-09-29
Status: resolved
Blocked by: -

## Question

`OpenPLC_KNX` 5 个、`OpenPLC_SDRAM` 2 个例程里写死的引脚和串口（如 KNX_Basic 的继电器用 PE6 / PE5、`Serial_Test`、PG9 编程键、PD7 / PH12 状态脚），和本板原理图对不对得上；文件头里的名字、说明和文件本身对不对得上（如 KNX_TP_PingPong 头里写的是 KNX_TP_Sender）。

## 怎么算答完

一张表：例程、写死的每个引脚 / 串口、本板实际接法（带原理图出处）、对不对；以及文件头和实际不一致的每一处。

## Answer

2026-09-29 定（只读核实，未上板）。引脚号基本都对；错在 KNX 例程的头注释（继电器写成 PE6 / PE5，实为 PI8 / PI10；PG9 实为高有效；PG11 上没有 LED）、4 个 KNX 例程不拉高 RS232 使能 PB10 所以端子上无输出、以及 `OpenPLC_KNX` 用 USART1 驱动 STKNX 而 STKNX 要定时器产生位时序。头注释与代码不一致共 19 处，SDRAM 两个例程一致。逐条见 [EXB-07-findings.md](../EXB-07-findings.md)。

## 引出了什么新的未知

- `OpenPLC_KNX` 的 TP 物理层能不能在本板上发出合法帧 → 升格为票 [KNX 库的 TP 收发怎么在本板上发出合法帧](EXB-08-how-does-the-knx-library-drive-stknx.md)
- `HARDWARE-FACTS.md` 把 PG11 记成「心跳指示」，原理图上心跳灯是 LED3 / PE2 → 记进 [work/TODO.md](../../../work/TODO.md)，等用户定
- 19 处头注释的修正随 [KNX 回显例程长什么样](EXB-02-what-does-the-knx-echo-example-look-like.md) 定下各例程去留后一起做
