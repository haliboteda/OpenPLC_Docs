# 选过的语言存在哪个文件、长什么样

Type: grilling
Opened: 2026-09-30
Status: resolved
Blocked by: -

## Question

用户已定「存在 exe 旁边的文件里，下次打开沿用」。还没定的是：

| 选项 | 代价 | 风险 |
|---|---|---|
| A. 加进现有的 `porttool_ports.json`（`$PORTTOOL/internal/portmap/portmap.go`），多一个 `lang` 字段 | 少一个文件 | 这个文件名说的是「哪个 COM 是哪个」；而且它刻意不和别的设置混（`remember.go:19–21` 的注释） |
| B. 新开一个 `porttool_settings.json`，只放面板偏好 | 多一个文件、多一份读写代码 | 以后别的偏好也往里放，要守住「只放面板偏好」 |
| C. 其他 | — | — |

连带要定：

- 文件里语言怎么写（`zh` / `en` / `de`，还是 `zh-CN` 这种）
- 文件不在、读不懂、值不认识时：一律回到中文，还是另有做法
- exe 所在目录写不进去时（`portmap.go` 的 `save` 今天对写失败是静默忽略）：沿用这个做法，还是面板上说一句
- 切换控件放在页面哪里

## 怎么算答完

一句话写明选了 A / B / C 哪条，另写出：文件名、一个完整的文件内容样例、三种异常（不在 / 读不懂 / 写不进）各自的行为、切换控件的位置。

## Answer

2026-10-03 定（用户：按推荐）：**新开 `porttool_settings.json`**（exe 旁边），只放面板偏好，写 `"lang": "zh"`，取值 `zh` / `en` / `de`；文件不在或内容不对按中文。理由：`porttool_ports.json` 只管「哪个 COM 是哪个」，刻意不和别的设置混（`remember.go:19-21`）。

## 引出了什么新的未知

无。
