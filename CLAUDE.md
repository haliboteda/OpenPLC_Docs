# 开工入口 —— OpenPLC_Docs

**这份文件是给 AI 会话看的。** 这个仓库装 OpenPLC 产品的**全部文档和待决的问题**。

## 先读这三份

| 读什么 | 回答 |
|---|---|
| [README.md](README.md) | 这个仓怎么读，四层各是什么 |
| [WHERE-THINGS-LIVE.md](WHERE-THINGS-LIVE.md) | **产出来一个东西该往哪放** —— 六问按顺序 |
| [GLOSSARY.md](GLOSSARY.md) | 不查就不知道是什么的词（跨仓镜像、工装、图、票、迷雾……） |

## ⚠️ 用 wayfinder 之前必读这一条

**这个项目的地图和票落在 `maps/<effort>/`，不是 `.scratch/`。**

wayfinder 那个 skill 在没有拿到 issue tracker 时会**默认退回本地 markdown 追踪器，落点是 `.scratch/`**。
**本项目不用那个默认。** 约定在 [maps/MAP-AND-TICKET-CONVENTION.md](maps/MAP-AND-TICKET-CONVENTION.md)。

> **踩过一次**：2026-09-11 和 09-13 两个会话照默认把一整张图写进了工作区根的 `.scratch/`。
> **工作区根目录不是仓库**，所以那张图连同两张还开着的票，在版本控制外躺了五天，
> 直到 2026-09-16 才被翻出来搬进这里。搬进来的一瞬间检查抓出 15 个问题 ——
> **它在 `.scratch/` 里时，没有任何东西看得见。**

## 现在有哪几张活图

跑这个，别凭记忆：

```
python tools/list_wayfinder_map_frontier.py          # 现在能开工的票
python tools/list_wayfinder_map_frontier.py --all    # 连被挡的和已关的一起看
```

清单在 [maps/INDEX.md](maps/INDEX.md)。

## 手头没活了

看 [work/TODO.md](work/TODO.md) 和 [waiting/WAITING-ON.md](waiting/WAITING-ON.md)。

## 两道提交门禁

`core.hooksPath = .githooks`，提交时跑两条检查：票关得诚不诚实、占位符有没有人认领。
它们也在 `selfcheck` 里（用例 **P12**），因为 `--no-verify` 跳得过钩子。
