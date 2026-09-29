# app 里怎么套用修正值

Type: grilling
Opened: 2026-09-28
Status: resolved
Blocked by: CAL-05

## Question

用户 sketch 读 AI / 写 AO 时修正在哪一层生效：Arduino core 的 `analogRead` / `analogWrite` 自动套用，还是 `OpenPLC_Ports` 里给一个带单位的 API（mV、mA）；没有校准值时怎么办；用户要不要能拿到未修正的原始值。

## 怎么算答完

定下 API 和生效层；写明没有校准值时的行为；`OpenPLC_Ports` 的 AI / AO 例程用上它。

## Answer

2026-09-28 定（用户按推荐定）。`OpenPLC_Ports` 给带单位的 API（mV、mA），修正在这里套用；`analogRead` / `analogWrite` 保持原始值不动；没有有效校准值时退回标称换算并打一行日志。AI / AO 例程改用这个 API。

## 引出了什么新的未知

没有。实施项见 [work/TODO.md](../../../work/TODO.md)。
