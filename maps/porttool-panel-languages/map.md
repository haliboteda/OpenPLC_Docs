# 工装面板可选中文 / English / Deutsch

## 怎么看进度（不用问任何人）

```
python tools/list_wayfinder_map_frontier.py --all
```

## Destination

工装面板（`PortTool` 的浏览器页面）上可选中文 / English / Deutsch，默认中文；选过之后存在 exe 旁边的文件里，下次打开沿用。只翻面板上给人看的字；控制台输出、日志、报告文件照 [决策 11](../../docs/tables/DECISIONS.md) 保持英文。

## Notes

- **终点是用户 2026-09-30 定的**，原意照录在 Destination。范围只有工装面板，工装的其他部分（固件、方案文件、CLI、报告）不变
- **这张图先做规划**：票定完之后执不执行、什么时候执行，由用户另定。票里只出决定，不写代码
- **这张图重开了决策 11**：那条的「什么情况下重开」写的就是「补一个语言开关，不是把中文换掉」。票定完后在 [DECISIONS.md](../../docs/tables/DECISIONS.md) 追加一条新决策，不改第 11 条原文
- **执行时要同步改的规矩**：`$TOOL/CLAUDE.md`「面板上的字一律说大白话」写的是「而且是中文」，多语言落地后要改成「默认中文，另两种同样说大白话」
- **大白话规矩对三种语言一样成立**：不抄协议字面量、不露内部名 —— 见 `$TOOL/CLAUDE.md` 同一节
- 现状：页面是一个 `go:embed` 的文件 `$TOOL/internal/ptpanel/web/index.html`（`<html lang="zh-CN">`，4145 行）；面板监听 `127.0.0.1:0` 随机端口（`$TOOL/internal/ptpanel/panel.go:772`），所以浏览器的 `localStorage` 换一次端口就是另一个源、存不住；exe 旁边已有一个面板自己的记忆文件 `porttool_ports.json`（`$TOOL/internal/ptpanel/remember.go:38`）
- 和暂停的 [工装面板的提示与功能核对 + 上板联调](../porttool-ui-audit/map.md) 有交叠：那边「面板逐卡片过一遍提示与参数」还开着，会改中文原文 —— 先后见本图的票
- **要用到的 skill**：`grilling`（本图的 grilling 票）、`codebase-design`（字串放哪一层、Go 和页面之间的缝）、`prototype`（如果要先拿一张卡片试切换）；术语进 [GLOSSARY.md](../../GLOSSARY.md)
- 开票 / 关票 / 算前沿照 [图与票的约定](../MAP-AND-TICKET-CONVENTION.md)

## 全集

在工作区根目录跑（bash）。按「面板上人看得见的中文字串」找：页面里的字面量和 HTML 文本，加上面板服务端和模拟板会送到页面上的 Go 字串（去掉整行注释和测试文件）：

```
python -c 'import re,glob; fs=[f for f in glob.glob("IAPTranfer_Tool/internal/ptpanel/**/*.*",recursive=True)+["IAPTranfer_Tool/internal/simboard/simboard.go"] if f.endswith((".go",".html")) and not f.endswith("_test.go")]; pat=re.compile(r"\"[^\"\n]*[一-鿿][^\"\n]*\"|\x27[^\x27\n]*[一-鿿][^\x27\n]*\x27|\x60[^\x60\n]*[一-鿿][^\x60\n]*\x60|>[^<>\n]*[一-鿿][^<>\n]*<"); [print(f,i,m,sep="\t") for f in fs for i,l in enumerate(open(f,encoding="utf-8"),1) if not l.lstrip().startswith("//") for m in pat.findall(l)]'
```

2026-09-30 是 935 条：`index.html` 861，`internal/ptpanel/*.go` 70，`simboard.go` 4。关最后一张票前重跑，每一条都要落在「三种语言都有」「明确不译」两类之一。

⚠️ 这条命令抓不到**不含中文、却会上屏的字**：Go 拼进中文句子里的 `err.Error()`、板子报上来的名字、Windows 给的串口描述。它们归 [面板上的字从哪几条路到页面上](issues/LANG-01-which-paths-bring-text-to-the-panel.md) 那张表管。

## Decisions so far

- [面板上的字从哪几条路到页面上](issues/LANG-01-which-paths-bring-text-to-the-panel.md)：七条路，页面自己 861 条、Go 送上来 74 条；另有两处已经违反决策 11（持续测试日志文件头、导出的日志里夹着中文）

## Not yet specified

- **数字、日期、单位的写法要不要跟着语言变**（德文的小数逗号、`toLocaleString` 的千分位）：要等 [页面上的字怎么组织、切换怎么生效](issues/LANG-03-how-page-strings-are-organized.md) 定了才知道有没有地方放
- **悬停里的协议原值**（`title` 里的 `duty` / `mode=extloop`）：现在是「中文 + 悬停英文原文」，换到英文界面后两者可能长得一样，是否还要悬停没想清楚
- **暂停中的「端口列表怎么组织」**（`porttool-ui-audit` 那张图）一旦重排列表，会整批改分组名和说明 —— 和本图的先后要等那张图恢复时再看

## Out of scope

- **控制台输出、日志文件、报告文件**：照决策 11 保持英文（用户 2026-09-30 定）
- **日志窗里的协议原文**（`pt.*` 命令回显、帧、`ERR` 行）：原样显示，不译 —— 决策 11 与 `PORTTOOL-FLOW.md` A.6 铁律 1
- **`IAPTool`、固件 printf、方案文件内容、`porttool run` 的 CLI**：用户 2026-09-30 定只动工装面板
