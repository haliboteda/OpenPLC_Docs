# Go 送上来的 74 句在哪一层翻

Type: grilling
Opened: 2026-09-30
Status: open
Blocked by: LANG-01, LANG-03

## Question

面板服务端 70 句、模拟板 4 句中文（`error` / `why` 字段、日志窗里的 `[持续]` 行、模拟板的名字，出处见 [面板上的字从哪几条路到页面上](LANG-01-which-paths-bring-text-to-the-panel.md)）换语言时谁来翻：

| 选项 | 代价 | 风险 |
|---|---|---|
| A. Go 只回一个代号加参数（如 `{"code":"hold.bad_hours"}`），页面按词典拼句 | 74 处都改成回代号，页面多一批词条；和判据句今天的做法一样（Go 回结构化的 `check`，页面 `checkCN` 拼） | 代号和词典两边要对上，对不上时页面要有兜底 |
| B. Go 知道当前语言，自己按语言回句子 | 页面不用改 | Go 里多一份词典，和页面那份是两处出处 |
| C. Go 改回英文，页面照 A 翻；英文句子本身当代号 | 服务端和决策 11 的「英文」对齐 | 英文句子一改，页面那边就对不上 |

连带要定：

- 拼在句子里的 `err.Error()`（17 处，是英文）换到德文 / 英文界面时怎么放
- 模拟板那 3 句启动失败的错误（`simboard.go:109–111,155`）同时也是 CLI 会看到的吗 —— 是的话它归控制台，照决策 11 该是英文

## 已有的事实（2026-09-30，读 `$TOOL` 在 `9187f59` 的源码）

| 事实 | 出处 |
|---|---|
| `error` 通道：panel.go 15 条、hold.go 7、judge.go 5、net.go 1；带参数的只有端口名、地址、`err` 三类 | `panel.go:148–645`、`hold.go:62–255`、`judge.go:181–393`、`net.go:135` |
| `capsError` 走 state JSON，页面同样用 `showMessage` 显示，归入 `error` 一类 | `panel.go:234,439`；`index.html:725` |
| `why`：只有 1 处，参数是方案名和端口名 | `judge.go:294–296` |
| 日志窗行：panel.go 3、hold.go 6、link.go 7（都带 `[link …]` 前缀）、runlog.go 4 | `link.go:374` 汇总 |
| 拼进中文句子的 `err`：**12 处**（不是 [LANG-01](LANG-01-which-paths-bring-text-to-the-panel.md) 写的 17 处；`internal/ptpanel` 里 `err.Error()` 共 31 处，其余不进句子）。来源：串口库 / `net` 5、`os` 3、自家代码 3、`os/exec` 1 | `panel.go:148,337,420,439`、`hold.go:255`、`judge.go:364`、`link.go:147,163,240`、`runlog.go:69,77`、`simboard.go:155` |
| **模拟板的中文报错今天会打到 CLI 的 stderr**：`porttool run --port sim` 失败时 `run.go:152` 用 `%v` 把它拼进英文句子 —— 已违反决策 11「控制台英文」 | `simboard.go:109–111,155`；`$PORTTOOL/cmd/porttool/run.go:147,152` |
| `simboard.Label` 只进面板的端口列表，CLI 不打印 | `panel.go:170,177`；`porttool ports` 打的是 `serialx` 自己的 Label（`main.go:80–92`） |
| 先例：判据句由 Go 回结构化的 `check`（`field` / `op` / `min` / `max` / `value` / `unit`），`what` / `why` 保持英文给 CLI 和 CSV，页面 `checkCN` / `failCN` 自己拼中文 | `judge.go:311–323`；`index.html:1420,1435` |

## 怎么算答完

一句话写明选了哪条；逐条说清 `error`、`why`、`[持续]` 行、`simboard.Label`、`err.Error()` 五种各怎么处理；并说明模拟板那 3 句是面板专用还是 CLI 也会打印（查源码回答）。
