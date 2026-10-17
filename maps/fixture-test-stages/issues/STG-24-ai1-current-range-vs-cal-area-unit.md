# 标准机 AI1 焊成电流档，校准值区格式里 AI1 的单位写死是 mV

Type: grilling
Opened: 2026-10-11
Status: resolved
Blocked by: -

## Question

第 48 条要把第一台标准机的 AI1 焊成电流档；校准值区格式里 AI1 的单位是 mV（`$PORTTOOL/src/calarea/calarea.go`、`$BOOT/IAPServer` 的 `calib_area.h`），`calstore` 单位不符就拒存。

| 选项 | 做法 | 代价 |
|---|---|---|
| A | 格式升 v2，每路带档位 / 单位 | 跨仓：`calib_area.h`、板卡包、P2 一致性检查、`SECTOR-15.md` |
| B（推荐） | 格式不动，系数按登记的档位解释：AI1 登记为电流时存的就是 mA 系数，档位记在 PC 存档里 | 板卡包仍按 mV 解释 AI1；标准机只跑工装固件（决策 97），对它无害；产品板 AI1 都是电压档 |

## 怎么算答完

选定一种，写进决策表；要改的列进 TODO-fixture 第 38 条。

## Answer

2026-10-11 用户定：**「A 并且按推荐来」**（STG-23 选 A，STG-24 到 STG-28 按推荐），见决策 102。选 B：格式不动，AI1 的系数按登记的档位解释，档位记在 PC 存档里。

## 引出了什么新的未知

没有。
