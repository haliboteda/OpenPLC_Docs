# 面板上的字从哪几条路到页面上

Type: research
Opened: 2026-09-30
Status: resolved
Blocked by: -

## Question

工装面板上人看得见的每一句字，是从哪条路到页面上的（页面自己写的、Go 服务端送的、板子报的、操作系统给的）？每条路有多少条、出处在哪一行？有没有哪条路今天就把中文写进了日志或文件。

## 怎么算答完

一张表：每条路一行，写明出处（`文件:行号`）、条数、今天是什么语言；另列今天已经和决策 11 对不上的地方。条数加起来要和 map.md「全集」那条命令的输出对得上。

## Answer

2026-09-30 定（读 `$TOOL` 在 `9187f59` 的源码，未跑面板）：七条路，页面自己 861 条、Go 送上来 74 条，合计 935 条，和全集命令对得上。

| # | 路 | 出处 | 条数 | 今天 |
|---|---|---|---|---|
| 1 | 页面的静态 HTML | `$PORTTOOL/internal/ptpanel/web/index.html` 1–387 行 | 55 行含中文 | 中文 |
| 2 | 页面脚本里的字面量和词表 | 同一文件，17 张词表：`CHAN_NAME` :749、`PORT_NAME` :753、`PORT_WIRING` :856、`CASE_TEXT` :887、`SESSION_WHAT` :1135、`PORT_LABEL` :1152、`PARAM_CN` :1170、`VALUE_CN` :1183、`FIELD_CN` :1202、`TARGET_CN` :1249、`VALUE_HELP` :1285、`PARAM_HELP` :1335、`STEPTYPE_CN` :1357、`PLANFIELD_CN` :1367、`EXECCOND_CN` :1385、`OP_CN` :1409、`BOARD_LABEL` :1456；判据句由 `checkCN` :1420 / `failCN` :1435 在页面拼 | 830 个含中文的字面量（1、2 合计 861） | 中文 |
| 3 | Go 回的 `error` 字段 | `writeErr`（`$PORTTOOL/internal/ptpanel/panel.go:141`）及直接写 `"error"` 的四处（`hold.go:86,90,237,255`）；页面用 `showMessage(j.error)` 显示（`index.html:657` 等） | 3、4、5 合计 70 | 中文 |
| 4 | Go 回的 `why` 字段 | `judge.go:294`，页面存进 `judgeWhy`（`index.html:1512`） | 同上 | 中文 |
| 5 | Go 推进日志窗的上位机自述 | `s.emit`（`link.go:374`）经 SSE 进 `addLog`（`index.html:670`）；`hold.go`、`runlog.go` 的 `[持续]` / `[故障]` 行 | 同上 | 中文 |
| 6 | 模拟板在串口列表里的名字 | `simboard.Label`（`$PORTTOOL/internal/simboard/simboard.go:32`），经 `panel.go:170,177` 送出；同文件另有 3 句启动失败的错误 | 4 | 中文 |
| 7 | 不含中文、但会上屏的字 | 拼进中文句子的 `err.Error()`（`internal/ptpanel` 非测试文件 17 处）；板子 `pt.caps` 报的端口 / 参数名（页面按路 2 的词表转）；Windows 给的串口描述（原样） | — | 英文或原样 |

**今天已经和决策 11「日志文件英文」对不上的两处**：

- 持续测试的日志文件头把中文写进文件：`runlog.go:84–91` 的 `# duration 一直跑`，`runlog.go:158` 的 `# stopped (…)` 带着 `hold.go:67,143,151` 的「你点了停止 / 时间到了 / 板子没有应答」
- 「导出」按钮存的 `.txt`（`index.html:518–531`）把整个日志缓冲写出去，缓冲里有路 5 的中文行

## 引出了什么新的未知

- 上面两处「日志文件里有中文」怎么处理，归 [日志窗和导出的日志用哪种语言](LANG-05-log-window-and-exported-log-language.md)
- 路 7 的 `err.Error()` 是英文拼在中文里，换语言后怎么拼，归 [Go 送上来的 74 句在哪一层翻](LANG-04-where-go-side-strings-get-translated.md)
