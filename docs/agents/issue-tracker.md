# Issue tracker: 本仓的 markdown

**本项目的问题和地图都落在这个仓库里，不用 GitHub Issues，也不用 `.scratch/`。**

选这个的理由：这套东西全部价值在「开一个新会话能直接读到」。
GitHub Issues 会把内容挪出 git —— 方向正好相反。

## Wayfinding operations

`/wayfinder` 用的就是这一节。

| | 在哪 |
|---|---|
| **地图** | `maps/<effort>/map.md` |
| **票** | `maps/<effort>/issues/<前缀>-NN-<slug>.md`，一张票一个文件 |
| **活图清单** | `maps/INDEX.md` |
| **blocking** | 票头部的 `Blocked by:` 行，只写单向 |
| **前沿（现在能开工的票）** | `python tools/list_wayfinder_map_frontier.py` |
| **认领** | 开工前把 `Status:` 改成 `claimed` 并保存 |
| **关票** | 追加 `## Answer`（第一行写日期）和 `## 引出了什么新的未知`，`Status:` 改 `resolved`，**票留在原地不要移走**，再去 `map.md` 的 `Decisions so far` 加一行 |

**⛔ 不要用 `.scratch/`。** 那是 wayfinder 在没拿到本文件时的默认落点，
而这个工作区的根目录**不是仓库** —— 写进去等于写在版本控制外。
2026-09-11 踩过一次，经过记在本仓的 `CLAUDE.md`。

## 细则在别处，这里不抄

票的四个头部字段、编号前缀、关票的完整步骤、一个会话只关一张票 ——
全部在 [../../maps/MAP-AND-TICKET-CONVENTION.md](../../maps/MAP-AND-TICKET-CONVENTION.md)，**那是唯一出处**。

## 两道门禁

`core.hooksPath = .githooks`，提交时跑票的卫生检查和孤儿占位符检查。
它们也进了 `selfcheck`（用例 **P12**），因为 `git commit --no-verify` 跳得过钩子。

## 其他 skill 怎么用这里

`to-tickets` / `to-spec` 这类要「发布到 issue tracker」的，
在 `maps/<effort>/` 下新建文件，规矩同上。
