# macOS 上串口没有描述和 VID 怎么办

Type: grilling
Opened: 2026-09-30
Status: open
Blocked by: -

## Question

macOS 版为了能从 Windows 一次交叉编译而不开 cgo，串口列表只有名字（`$TOOL/internal/serialx/enum_basic.go:1–13`；上游 `go.bug.st/serial@v1.6.2/enumerator/doc.go:13`）。后果：面板上认不出哪个口是哪个转接器；`porttool answer --usb` 按 ST 的 VID 找板子 USB 口（`$TOOL/cmd/porttool/answer.go:30,91`）在 macOS 上找不到。

| 选项 | 代价 | 风险 |
|---|---|---|
| A. 接受：macOS 上只列名字，`--usb` 在 macOS 上报错并提示改用 `--com` | 几行代码 + 一句说明 | Mac 用户靠 `/dev/cu.*` 名字认口 |
| B. 不开 cgo，在 macOS 上调系统自带的 `ioreg` 读 VID 和描述 | 多一个只在 darwin 编译的文件，要解析 `ioreg` 输出 | 没有 Mac 就验不了；`ioreg` 输出格式随系统版本变 |
| C. 开 cgo | — | 违反 `R4-02`「一次生成」，列出来只为对比 |

## 怎么算答完

一句话写明选了哪条；选 A 写明 `--usb` 在 macOS 上的报错原文（英文，照决策 11）；选 B 写明在哪台 Mac、哪个系统版本上验。
