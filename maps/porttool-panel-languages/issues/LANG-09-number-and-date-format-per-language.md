# 数字、日期、单位的写法跟不跟着语言变

Type: grilling
Opened: 2026-09-30
Status: open
Blocked by: LANG-03

## Question

换到英文 / 德文界面后，页面上的数字、日期、单位写法要不要跟着变（德文小数逗号 `3,3`、千分位 `1.000`；日期顺序）。今天页面里 `toFixed` / `toLocaleString` 共 16 处（`$TOOL/internal/ptpanel/web/index.html`，如 :1954 的 `cycles.toLocaleString()`），`toLocaleString` 跟的是浏览器语言，不是面板选的语言。

| 选项 | 代价 | 风险 |
|---|---|---|
| A. 一律照现在的写法（小数点、无千分位），不随语言变 | 只需把 `toLocaleString` 改成固定写法 | 德文界面上小数点不合德文习惯 |
| B. 跟着面板选的语言变 | 16 处都改成按面板语言格式化 | 屏幕上的数和日志 / 协议里的数长得不一样，对照日志时要换算 |

## 怎么算答完

一句话写明选了哪条，并写明 `index.html` 里那 16 处各按什么写法。
