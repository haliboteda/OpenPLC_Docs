# 部件仓要不要本机配置

Type: grilling
Opened: 2026-10-02
Status: resolved
Blocked by: TA-04, TA-05

## Question

照决策 78，部件仓最好不要 `config/machine.py`，让 CMake、`go` 自己找工具链。PortTool 仓 2026-10-01 刚加了一套 Python 的 `init_machine.py` / `common.py` / `machine.py`（它的 T4-01 要编 `$BOOT` 的 C 源码、T4-02 要起浏览器）：要不要收缩，收缩到什么程度。

## 怎么算答完

每个部件仓写明：要不要本机配置，要的话记哪几项、为什么离不开；PortTool 仓那套是留、缩还是删。

## Answer

2026-10-02 定（用户按推荐定，九件一次定完）。bootloader 不要（本机 gcc 用 gitignored 的 `CMakeUserPresets.json` 告诉 CMake）；IAPTool 不要（只用 `go`；拷进板卡包时按平台默认位置找 Arduino15）；板卡包不要（见「板卡包仓的测试怎么跑」）；PortTool 保留现有的小配置（`$BOOT`、CubeIDE、gcc、Git Bash 离不开）；`$TEST` 用完整的本机配置，从 `$TOOL` 那套搬过去。

## 引出了什么新的未知

没有。
