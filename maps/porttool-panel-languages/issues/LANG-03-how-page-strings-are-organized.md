# 页面上的字怎么组织、切换怎么生效

Type: grilling
Opened: 2026-09-30
Status: resolved
Blocked by: LANG-01

## Question

页面自己的 861 条字（静态 HTML + 17 张词表 + 散在各函数里的句子，见 [面板上的字从哪几条路到页面上](LANG-01-which-paths-bring-text-to-the-panel.md)）换成三种语言，按什么组织：

| 选项 | 代价 | 风险 |
|---|---|---|
| A. 一张总词典，每句一个键，三种语言并排；代码里只写键 | 861 处全部改成查键，一次改动最大 | 键名要起得看得懂，否则读代码的人对不上屏幕 |
| B. 保留现有的词表形状，每张表多一层语言（`PARAM_CN` → 按语言取）；散句另收进一张表 | 改动按表走，词表以外的散句仍要逐句收 | 两套机制并存，漏收的散句不报错、只是切了语言还显示中文 |
| C. 三种语言各一份 `index.html` | 不用改查找方式 | 同一改动要做三遍，必然分叉 |

连带要定：

- 词典放在 `index.html` 里，还是 `web/` 下单独的文件（仍然 `go:embed`）
- 切换后是当场重画，还是刷新页面
- 一句话缺了某种语言的译文时，显示中文，还是显示键名让人一眼看出来
- `<html lang>` 跟着变不变

## 怎么算答完

一句话写明选了哪条，并写出：词典在哪个文件、一条词条的样子、缺译文时显示什么、切换是重画还是刷新。

## Answer

2026-09-30 定：

- **选 A**：一张总词典，键按原词表名分段（`param.duty`、`value.extloop`），每条三种语言并排；代码里只写键。理由：「每个键三种语言齐全」只需查一张表
- 板子报上来的日志照旧是英文原文，不进词典（与本图 Out of scope 一致）
- **词典放 `internal/ptpanel/web/strings.json`（`$TOOL` 里，待建），嵌进 exe**（`panel.go:22` 的 `go:embed web` 自动带上）。不放 exe 旁边：没有人需要不重新编译就改译文，放旁边会有漏拷、版本对不上的问题
- **切换 = 刷新页面**；有通过 / 失败结果、未下发的参数或未保存的方案时先弹窗说明会丢，确认才刷新。理由：只在页面里的状态（`index.html` 的 `verdicts`、`edited`、`plan`）刷新就没了，而当场重画漏掉的地方会静默留在旧语言
- `<html lang>` 跟着语言变（`zh-CN` / `en` / `de`）
- **缺某种语言的译文时显示中文原文**。真正防漏译的是「每个键三种语言齐全」那条检查（归 [面板的浏览器用例在三种语言下怎么保持有效](LANG-07-how-the-panel-browser-tests-stay-valid.md)），页面只需不坏

一条词条的样子（英文、德文的措辞归 [英文和德文谁写、谁审、术语照什么](LANG-06-who-writes-and-reviews-english-and-german.md)，这里只示意形状）；句中要填的值写成 `{名字}`，各语言自己决定放在句子哪里：

```json
{
  "param.duty":  { "zh": "占空比（%）", "en": "Duty cycle (%)", "de": "Tastverhältnis (%)" },
  "conn.picked": { "zh": "已选 <b>{port}</b> —— 点「连接」继续。",
                   "en": "<b>{port}</b> selected — click Connect to continue.",
                   "de": "<b>{port}</b> ausgewählt — auf Verbinden klicken." }
}
```

## 引出了什么新的未知

- 数字、日期、单位的写法要不要跟着语言变：词典定下来之后有地方放了，从迷雾升格成 [数字、日期、单位的写法跟不跟着语言变](LANG-09-number-and-date-format-per-language.md)
