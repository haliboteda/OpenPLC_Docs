# P7/P8/P9 和 selfcheck 怎么跟着搬

Type: task
Status: open
Blocked by: MIG-03

## Question

文档检查脚本住在 `$TOOL/TestCase/tools/`，扫描根**写死在代码里**
（`check_doc_paths.py` 的第 96–100 行列着 boot / tool / core / skills 四个仓）。

要定：`OpenPLC_Docs` 怎么加进扫描范围；脚本本身留在 `TestCase` 还是也搬；
搬完 `selfcheck` 的 16 项还剩哪些、跑不跑得过。

## 怎么算答完

`selfcheck` 在搬完之后全过，且 `OpenPLC_Docs` 里每一个链接都被 P9 真的扫到 ——
故意写一条坏链接进去，P9 要报错。
