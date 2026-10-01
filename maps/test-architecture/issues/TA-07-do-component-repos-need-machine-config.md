# 部件仓要不要本机配置

Type: grilling
Opened: 2026-10-02
Status: open
Blocked by: TA-04, TA-05

## Question

照决策 78，部件仓最好不要 `config/machine.py`，让 CMake、`go` 自己找工具链。PortTool 仓 2026-10-01 刚加了一套 Python 的 `init_machine.py` / `common.py` / `machine.py`（它的 T4-01 要编 `$BOOT` 的 C 源码、T4-02 要起浏览器）：要不要收缩，收缩到什么程度。

## 怎么算答完

每个部件仓写明：要不要本机配置，要的话记哪几项、为什么离不开；PortTool 仓那套是留、缩还是删。
