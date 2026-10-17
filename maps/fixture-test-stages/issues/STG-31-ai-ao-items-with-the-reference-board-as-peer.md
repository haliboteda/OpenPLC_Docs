# AI2 读数、AO 输出选标准机当对端时怎么判

Type: grilling
Opened: 2026-10-11
Status: resolved
Blocked by: -

## Question

测试项目录里 AI2 读数、AO 输出的默认对端是标准机（`$PORTTOOL/src/ptitems/ptitems.go`），但执行器现在遇到这种组合记 ERROR（原因 `analog_peer`，`$PORTTOOL/src/ptlib/analog.go`），所以功能测试用默认配置时这几项会出错。要判，得用标准机自己的校准值和档位换算它那一侧的输出 / 读数。

| 选项 | 做法 | 代价 |
|---|---|---|
| A（推荐） | 执行器也读标准机的 `pt.cal`、UID 和档位登记，标准机那一侧按它自己的 k、b 换算，再和被测板比 | 标准机必须先校准过（决策 97 的制作标准机已要求） |
| B | 默认对端改成人工，标准机这条先不支持 | 产线要人逐点读表，慢 |

## 怎么算答完

选定一种；要改的列进 TODO-fixture。

## Answer

2026-10-13 用户定「按推荐」：**A**。执行器也读标准机的 `pt.cal`、UID 和档位登记，标准机那一侧按它自己的 k、b 换算成标准值，卡片照[决策 108](../../../docs/tables/DECISIONS.md)显示，标准值一栏自动填。2026-10-13 已做（`$PORTTOOL/src/ptlib/analog.go`，PORTTOOL-FLOW C.3.2「读数 / 输出项」）。

## 引出了什么新的未知

没有。
