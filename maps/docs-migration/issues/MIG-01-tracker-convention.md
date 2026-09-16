# tracker 约定怎么写

Type: grilling
Status: open
Blocked by: -

## Question

这个仓用哪套约定表达「图、票、blocking、前沿」？

现在的目录形态（`maps/<effort>/map.md` + `issues/MIG-NN-<slug>.md`）是照 wayfinder 的本地回退改的，
**还没正式写下来**，所以现在是惯例不是约定。

要定的：

- 票的头部有哪几个字段（`Type` / `Status` / `Blocked by` 之外还要不要别的）
- blocking 怎么表达，才能让「前沿」一眼看出来
- 前沿靠人扫还是靠脚本扫
- 票关掉之后放哪 —— 原地改状态，还是移进 `closed/`

## 怎么算答完

仓里有一份 tracker 约定文档，照着它能**无歧义地**做三件事：新建一张票、找出当前前沿、关掉一张票。
拿现有的八张票逐一对照，没有一张需要临场发挥。
