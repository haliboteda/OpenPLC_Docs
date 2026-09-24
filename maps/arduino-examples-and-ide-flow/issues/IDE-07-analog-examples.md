# 模拟量例程：AI、AO、板载温度

Type: task
Opened: 2026-09-24
Status: resolved
Blocked by: IDE-05

## Question

照定下的格式写三个例程。AI 需要 VREFBUF（板子没有外部参考），见硬件事实文档。

## 怎么算答完

三个例程在 `P5` 里编过；读数的单位和换算在输出里写清。

## Answer

2026-09-25 定。写了 `AI_Inputs`（AI1 按 mV、AI2 按 µA）、`AO_Outputs`（0–20 mA 五档，EF 线只报原始电平）、`BoardTemperature`（500 mV 偏置、10 mV/°C）。三者共用库里的 `openplcEnableVref()`，打开片内 2.5 V 基准。

`P5` 全量 48 个例程 0 失败（2026-09-25）。**只编译过，没上过板**。上板逐个验落在 [TODO.md](../../../work/TODO.md)「端口例程逐个上板验」。

## 引出了什么新的未知

没有。
