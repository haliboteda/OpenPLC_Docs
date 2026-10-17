# AO 带负载两路档位不同时，输出值怎么填

Type: grilling
Opened: 2026-10-16
Status: resolved
Blocked by: -

## Question

AO 带负载（`aout.load`，[PORTTOOL-FLOW.md](../../../docs/modules/M4/PORTTOOL-FLOW.md) C.3.6「AO 带负载」）只有一个输出值，两路共用、各按自己的档位解释（`$PORTTOOL/src/ptlib/aoload.go`）。默认档位 AO1 电压、AO2 电流（[决策 134](../../../docs/tables/DECISIONS.md)），填 10 就是 AO1 出 10 mV、AO2 出 10 mA，测不对。

| | 做法 | 代价 | 风险 |
|---|---|---|---|
| **A（推荐）** | 每路一个输出值，单位跟这一路档位 | 卡片和配置各多一格，旧配置的一个值迁成两格 | 无 |
| B | 一个值，填满量程百分比，每路按自己满量程换算 | 改动少 | 人要换算成表上读数；和其他卡直接填 mA / mV 不一致 |

## 怎么算答完

选定一种，改 PORTTOOL-FLOW 的「AO 带负载」，列进 TODO-fixture。

## Answer

2026-10-16 用户选 A：每路一个输出值，单位跟这一路档位。改动列进 TODO-fixture 第 86 条。

## 引出了什么新的未知

没有。
