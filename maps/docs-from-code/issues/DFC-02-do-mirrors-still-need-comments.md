# 跨仓镜像的约束现在到底靠什么

Type: grilling
Opened: 2026-09-16
Status: open
Blocked by: -

## Question

`$PROD/docs/repo/ARCHITECTURE.md` 第 67 行写着九条跨仓镜像代码
**「只能靠注释交叉引用约束，机制上无法强制同步」**。

**但 P2 `check_mirror_sync.py` 存在，而且在 `selfcheck` 里是绿的。**
那句话要么已经过期，要么 P2 覆盖的没有它说的那么全。

这条挡着整张图：如果注释真的是唯一的约束手段，那九条镜像的注释**一行都不能动**；
如果 P2 已经接管，那它们和别的注释一样可以搬。

## 怎么算答完


读 `check_mirror_sync.py`，对着 ARCHITECTURE 那张九行的表逐条核：
**哪几条 P2 真的在查、哪几条只靠注释**。结论写回 ARCHITECTURE 第 67 行 ——
它现在这句话如果是错的，本身就是个发现。