# Domain docs

**单上下文**（single-context）。这个产品只有一个领域，不是 monorepo。

| 要什么 | 在哪 |
|---|---|
| 术语表（不查就不知道是什么的词） | [../../GLOSSARY.md](../../GLOSSARY.md) |
| 已拍板、不要重开的决策 | `$PROD/docs/tables/DECISIONS.md`，48 条，**编号不要重排** |
| 推迟掉的方案和否决理由 | `$PROD/docs/tables/DEFERRED-DESIGNS.md` |

⚠️ **本仓不用 `CONTEXT.md`，也不用 `docs/adr/`。**
`domain-modeling` 这个 skill 默认往那两处写 —— **在本仓请写进上面那张表指的地方**：
术语进 `GLOSSARY.md`，够得上 ADR 分量的决策进 `DECISIONS.md`（追加一条，不改已有编号）。

理由：这个项目的决策编号被大量外部引用（提交信息、别的文档、聊天记录都在说
「`DECISIONS 44`」），另起一套 ADR 编号等于制造第二套会漂的编号。
