# demo 和工装固件的契约测试 T4-05 住哪个仓

Type: grilling
Opened: 2026-10-11
Status: resolved
Blocked by: -

## Question

T4-05 用同一份 Go 测试对板卡包例程 `FixtureDemo` 和工装固件的模拟板各跑一遍（`$PORTTOOL/TestCase/host/porttool_demo/`）。它用到三个仓（`$CORE_REPO`、`$BOOT`、`$PORTTOOL`），按决策 78 的判据该归 `$TEST` 的契约层；可它要 import `$PORTTOOL/src/ptproto`，在 `$TEST` 里 import 不到。决策 78 的例外只说了「一个部件的源码分在两个仓」，没覆盖 demo。

| 选项 | 做法 | 代价 |
|---|---|---|
| A（推荐） | 留在 `$PORTTOOL`，把决策 78 的例外扩成「工装协议的镜像（demo）也跟着 PortTool」 | 改一条决策的例外 |
| B | 搬到 `$TEST`，解析改用 Python 重写一份 | 协议解析多一份实现，会和面板用的那份分叉（决策 77） |

## 怎么算答完

选定一种；选 A 就在决策 78 的例外里补一句，`tools/classify_tests_by_layer.py` 去掉「等用户定」。

## Answer

2026-10-11 用户定：**「B 其他推荐」**，本票按推荐：选 A：T4-05 留在 `$PORTTOOL`，决策 78 的例外扩到工装协议的镜像（决策 104）。

## 引出了什么新的未知

没有。
