# VREF+ 改由外部基准提供时固件怎么改

Type: grilling
Opened: 2026-10-20
Status: open
Blocked by: -

## Question

用户 2026-10-20 提出讨论：模拟部分的 VREF+ 从片内 VREFBUF（2.5 V）改成板上外部基准，固件怎么改。现在板上 VREF+ 只有退耦、没有基准芯片，固件必须开 VREFBUF（[HARDWARE-FACTS.md](../../../docs/hardware/HARDWARE-FACTS.md)「模拟量：没有外部基准，必须使能片内 VREFBUF」），所以前提是硬件先加基准。

要定两件事：新老板子怎么区分，满量程从哪来。

| 方案 | 做法 | 代价 / 风险 | 推荐 |
|---|---|---|---|
| A 两份固件 | 编译开关选片内 / 外部 | 工装、板卡包、交付包各两套；烧错时新板与外部基准抢 VREF+、老板 VREF+ 悬空 | |
| B 开机判断 | VREFBUF 保持高阻（`ENVR=0`、`HIZ=1`）读一次 VREFINT：满量程即 VREF+ 悬空，开 VREFBUF；读数正常即有外部基准，不开 | 工装 `port_vref.c`、板卡包 `openplcEnableVref` 各加一个判断函数；判断依据在老板上用过，新板没测 | ✅ |
| C 删掉开 VREFBUF | 一行 | 现有板子 ADC / DAC 全坏 | |

满量程：建议统一用开机时由 VREFINT 实测的 VREF+（工装 `port_dac.c` 已这样做），2500 mV 只作测不到时的后备。外部基准不是 2.5 V 时，下面这些写死 2500 的地方要改：板卡包 `openplc_analog.c` 的标称换算、`$PORTTOOL/src/calstore/spec.go` 的 `VrefMV`、判据方案 `station6-poweron.json` 的 `vdda` 区间；AO 4–20 mA 偏置（R11 / R14 + JP3 / JP4）接的是 VREF 网络，偏置跟着变；已烧的校准值要重校。

## 怎么算答完

用户给出外部基准的型号和电压（最好附新版原理图），并定老板子是否继续支持；据此在上表选定方案，写进 DECISIONS.md，硬件事实写进 HARDWARE-FACTS.md。
