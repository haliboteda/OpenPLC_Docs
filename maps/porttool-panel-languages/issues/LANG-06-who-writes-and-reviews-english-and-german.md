# 英文和德文谁写、谁审、术语照什么

Type: grilling
Opened: 2026-09-30
Status: open
Blocked by: -

## Question

面板有 935 条中文（map.md「全集」），其中大段的是每个端口的接线说明和测试说明（`PORT_WIRING`、`CASE_TEXT` 等）。英文和德文：

- **谁写初稿**：AI 按中文译，还是有人写
- **谁审**：有没有读德文的硬件工程师能看；没有人审的话，德文还发不发
- **术语照什么**：硬件资料本身是德文的 —— 端子名出自 `$HW/Klemmenbezeichnungen-R.pdf`（`Digital Out`、`SD Karte`…），排号出自 `$HW/Klemmblockzuordnung.pdf`（`Klemmblock`）。德文界面是不是直接用这些词；英文界面用什么
- **术语表放哪**：进 [GLOSSARY.md](../../../GLOSSARY.md)，还是和词典放在一起

⚠️ 已知的错：`Klemmenbezeichnungen-R` 从 09 号起错开一位、A08 印错（`$PROD/docs/hardware/HARDWARE-FACTS.md` 记着）。照它取德文词时只取名字，不取它的端子号。

## 怎么算答完

写明：初稿谁出、谁审、没人审时德文怎么办；一张起步术语表（至少覆盖面板上现在出现的端口名、`端子排`、`占空比`、`频率`、`保持`、`通过 / 失败 / 未测`）三种语言并排，并写明它放在哪个文件。
