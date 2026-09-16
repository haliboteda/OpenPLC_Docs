# 各仓 CLAUDE.md 改成什么

Type: grilling
Status: open
Blocked by: MIG-03

## Question

`docs/` 搬空之后，各仓根目录的 `CLAUDE.md` 是 AI 会话唯一的入口。写错等于会话找不到东西。

要定：它还留多少内容、指向 `OpenPLC_Docs` 的哪几个位置、工作区根的 `CLAUDE.md` 怎么改。

## 怎么算答完

从零开一个新会话，只读某个仓的 `CLAUDE.md`，能找到这个仓要用的全部文档，不需要猜路径。
四个仓（bootloader / core / tool / 工作区根）各验一次。
