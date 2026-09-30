# 面板的浏览器用例在三种语言下怎么保持有效

Type: grilling
Opened: 2026-09-30
Status: open
Blocked by: LANG-03

## Question

用例 `T4-02`（面板在真浏览器里点一遍，见 [HOW-TO-RUN-TESTS.md](../../../docs/engineering/HOW-TO-RUN-TESTS.md)）的两个脚本靠中文找控件、判结果：`$TOOL/TestCase/host/porttool_panel/run.py` 有 74 个含中文的字面量，`naive.py` 有 70 个，而 `naive.py` 按设计就是「照页面上印的字点」。另外 `run.py:559` 的 `BANNED_ON_CARDS` 把 `Klemmblock`、`Digital Out`、`period`、`hold`、`temperature` 当成「漏出来的协议词」—— 在英文 / 德文界面里它们正是该显示的词。

| 选项 | 代价 | 测不到什么 |
|---|---|---|
| A. 两个脚本只在中文下跑，另加一条检查：词典里每个键三种语言都有、没有空的 | 最小 | 英文 / 德文界面上的排版、截断、漏收的散句 |
| B. A 之外，`run.py` 在三种语言下各跑一遍，断言改成按键查词典 | 断言要从中文字面量改成键 | 译文写得对不对 |
| C. `naive.py` 也三种语言各跑 | 最大；它按字点，要三套字 | 同 B |

连带要定：`BANNED_ON_CARDS` 改成按语言各一张表，还是只在中文下查。

## 怎么算答完

一句话写明选了哪条；写明 `BANNED_ON_CARDS` 怎么处理；并写出这个选择**测不到什么**，准备照原话写进 `T4-02` 的判据。
