# 带单位、套校准值的 AI / AO 读写

`OpenPLC_Ports` 给用户的模拟量 API：读 AI、写 AO 时直接用 mV、mA，并套用这块板在工装上测出的校准值。
定于 [app 里怎么套用修正值](../../../maps/per-board-calibration/issues/CAL-06-how-does-the-app-apply-the-correction.md)；
校准值区的格式和系数含义在 [SECTOR-15.md](../M1/SECTOR-15.md)「校准值区的格式」，这里不抄。

## API

| 函数 | 返回 / 参数 | 通道 |
|---|---|---|
| `float openplcReadAI1_mV()` | AI1 的电压，mV | AI1（0–10 V） |
| `float openplcReadAI2_mA()` | AI2 的电流，mA | AI2（0–20 mA） |
| `void openplcWriteAO_mA(uint8_t channel, float mA)` | `channel` 取 1 或 2；超出 0–20 mA 的值截到边界 | AO1、AO2（电流输出） |
| `calib_status_t openplcCalibrationStatus()` | 这块板的校准值是否有效（`CALIB_OK` / `CALIB_BLANK` / `CALIB_CORRUPT` / `CALIB_OTHER_BOARD`） | — |

AO 只有 mA：两路都是电流输出（XTR111），硬件上没有电压输出可写。

## 怎么换算

| 步 | 做什么 |
|---|---|
| 1 | 第一次调用时打开内部 2.5 V 基准、读一次扇区 15 的校准值区，之后不再读 |
| 2 | 标称换算：AI1 = 引脚电压 × 90.6k / 22.6k；AI2 = 引脚电压 / 124 Ω；AO 引脚电压 = 目标电流 × 1024 Ω / 10 |
| 3 | 套校准值：输入取 `gain × 标称值 + offset`；输出写给硬件的是 `(目标 − offset) / gain` |
| 4 | 校准值无效（没写过、写坏了、不是这块板的）时第 3 步用 `gain 1 / offset 0`，并在诊断串口打一行日志，**只打一次** |

函数内部把 ADC / DAC 分辨率设成 12 位并保持在 12 位；同一个 sketch 里再用 `analogRead()` 的人要知道这一点。
`analogRead()` / `analogWrite()` 本身不动，仍是原始值。

## 测试

主机侧用例 `T3-07`：把真的 `openplc_calib.c` 和换算代码在 PC 上编译，校准值区放在内存里，验证系数生效、三种无效情况退回标称且日志只打一次。真板子上的读数精度归工装的校准流程验证，不在这里。
