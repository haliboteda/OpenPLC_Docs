# 图与票的约定

**这份是唯一出处。** 照着它能无歧义地做三件事：新建一张票、找出当前前沿、关掉一张票。
定于 2026-09-16，由 `maps/docs-migration/issues/MIG-01-tracker-convention.md` 这张票敲定。

## 目录长什么样

```
maps/
├── INDEX.md                          活图清单
├── MAP-AND-TICKET-CONVENTION.md      这份
└── <effort>/
    ├── map.md                        一张图
    └── issues/<前缀>-NN-<slug>.md    一张票一个文件
```

**不用 `.scratch/`。** 目录名要说出这份文件多久变一次，而 `.scratch` 的字面意思是「用完就扔」——
这些要长期留着。

## 一张票长什么样

头部**恰好四个字段**，顺序固定，一行一个：

| 字段 | 取值 | 说明 |
|---|---|---|
| `Type:` | `research` / `prototype` / `grilling` / `task` | 决定谁来答。`grilling` 和 `prototype` **必须有人在场**，AI 不能自问自答 |
| `Opened:` | `YYYY-MM-DD` | 日期要写全 —— 两年后读的人得能判断它还算不算数 |
| `Status:` | `open` / `claimed` / `resolved` | 开工前先改成 `claimed` 再动手 |
| `Blocked by:` | `MIG-02, MIG-07` 或 `-` | **只写单向**，见下 |

**不设负责人字段** —— 单人项目，`claimed` 已经够了。

正文两节，缺一不可：

- `## Question` —— 这张票要定的那个决定
- `## 怎么算答完` —— **动手之前就要写**，而且要写成能判真假的话。「跑一遍全过」算，「整理得更清楚」不算

## blocking 只写单向

被挡的那张写 `Blocked by:`，**挡人的那张什么都不写**。

理由：两头都写就是同一个事实写两处，正撞「一个事实只写在一个文件里」，而 P8 专抓这个。
想知道「这张票挡着谁」，让脚本算，别手写。

## 前沿怎么算

**前沿 = `Status: open` 且 `Blocked by:` 列的票全部 `resolved` 的那些。**
`claimed` 不在前沿里（已经有会话在做了）。

```
python tools/list_wayfinder_map_frontier.py
```

**它不进 `selfcheck`。** `selfcheck` 是发版门禁，前沿有几张票不是对错问题 ——
塞进去只会制造一条永远在变的「结果」。

## 关一张票

1. 正文追加 `## Answer`，**第一行写 `YYYY-MM-DD 定`**，然后写答案本身
2. 追加 `## 引出了什么新的未知`，**答「没有」也要明写，空着不算关掉**
3. `Status:` 改成 `resolved`。**票留在原地不要移走** —— 移了，图里指向它的链接全断，而 P9 专抓断链
4. 回到 `map.md` 的 `## Decisions so far`，加一行：票的标题（带链接）+ 一句话摘要。**不要把答案抄过去**
5. 如果这个答案让迷雾里某条变得说得清了，就把它升格成新票，并从 `## Not yet specified` 里删掉

## 编号和文件名

- 票号带图前缀（`MIG-` 是文档搬迁那张图的），全局唯一。**这个项目的编号撞过车** —— 见 `$PROD/docs/ID-MAP.md`，曾有 13 套编号混用，`A1` 同时是四样东西
- **编号只活在文件名里。** 图的正文、提交说明、对话里一律用票的**标题**
- 脚本文件名写长一点，说清它干什么 —— `list_wayfinder_map_frontier.py`，不是 `frontier.py`

## 一个会话只关一张票

`research` 票除外（那种可以并行跑）。
