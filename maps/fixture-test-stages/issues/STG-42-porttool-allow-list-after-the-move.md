# `$PORTTOOL` 的命令允许列表要不要跟着新结构改

Type: grilling
Opened: 2026-10-17
Status: resolved
Blocked by: -

## Question

`$PORTTOOL/.claude/settings.json`（进 git、团队共用）的允许列表里有 4 条指向已删的东西：`./compile_tool.sh`、`bash compile_tool.sh`、两条旧路径的 `TestCase/host/porttool_caps/build.py`（[决策 149](../../../docs/tables/DECISIONS.md) 重组后已不在）。

| 选项 | 做法 | 风险 |
|---|---|---|
| A. 只删这 4 条 | 允许列表只剩 git、go 那几条 | 无：删条目只会少放行 |
| B. 删 4 条，再加 `tools/build.sh` 和 `TestCase/test.sh` | 两个菜单入口免确认 | `tools/build.sh flash` 会烧板子；按 `$TEST/CLAUDE.md` 的规矩，碰硬件的命令不进团队共用的那份 |

## 怎么算答完

选定一条，改 `settings.json`。

## Answer

2026-10-17 用户选 **A**：只删这 4 条，已删；两个菜单入口不进团队共用的允许列表。

## 引出了什么新的未知
