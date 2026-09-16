# tracker 约定怎么写

Type: grilling
Opened: 2026-09-16
Status: resolved
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

## Answer

2026-09-16 定。约定写成 [../../MAP-AND-TICKET-CONVENTION.md](../../MAP-AND-TICKET-CONVENTION.md)，
前沿脚本是 [../../../tools/list_wayfinder_map_frontier.py](../../../tools/list_wayfinder_map_frontier.py)。

四个问题的结论：

| 问 | 定成 |
|---|---|
| 头部字段 | **恰好四个**：`Type` / `Opened` / `Status` / `Blocked by`。不设负责人字段 |
| blocking | **只写单向**（被挡的写 `Blocked by`）。两头都写就是同一事实写两处，P8 会抓 |
| 前沿 | **脚本算**，`python tools/list_wayfinder_map_frontier.py`。**不进 `selfcheck`** —— 门禁管对错，前沿有几张票不是对错 |
| 关掉的票 | **原地改 `Status: resolved`，不移走**。移了，图里指过去的链接全断，P9 会抓 |

另外两条是做的过程中定的，不是原问题：**票必须有 `## 怎么算答完`，动手前就写**；
**脚本文件名写长**（用户 2026-09-16 提，和 `$PROD/docs/CONVENTIONS.md` 里「文件名要说出内容或用途」是同一条，没有另写规矩）。

### 验证

`怎么算答完` 要求「拿现有的八张票逐一对照，没有一张需要临场发挥」：

- 八张票补上 `Opened:` 后全部解析通过，前沿算出 `参考层按什么分类` 一张，与手算一致
- 塞一张缺 `Opened:` 的票 → 报 `missing header field(s): Opened`，退出码 1
- 塞一张 `Blocked by: MIG-77`（不存在）→ 报 `blocked by unknown ticket MIG-77`，退出码 1

⚠️ **过程中修掉一个真缺陷**：blocker 写错字时，脚本原先把那张票算成可开工 ——
打错一个编号就能让被挡的票看起来能动。现已改成「不存在的 blocker 一律算未解决」。

⚠️ **这里只写下了「关票要回答新未知」这条规矩，没有让它变成关不掉就过不去的机制。**
强制那一半是 `关票时怎么强制回答「引出什么新未知」` 那张票的事，这张不越界。

## 引出了什么新的未知

**一张图走完之后怎么归档。** 这份约定说清了票不移走，但整张图走到终点之后
`maps/INDEX.md` 里标什么、`maps/<effort>/` 目录动不动，还没说。
现在只有一张活图，问题没浮出来；第二张图开起来之前要定。已记进图的迷雾。
