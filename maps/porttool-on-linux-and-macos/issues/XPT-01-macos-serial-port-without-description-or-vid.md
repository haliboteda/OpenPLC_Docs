# macOS 上串口没有描述和 VID 怎么办

Type: grilling
Opened: 2026-09-30
Status: resolved
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

## Answer

2026-09-30 定：**选 B** —— macOS 上调系统自带的 `ioreg` 读 VID / PID / 产品名 / 序列号，按口名并进 `serialx.List` 的结果；不开 cgo，一次生成照旧。理由：板子的 USB 口靠 `0483:5740` 认（`$TOOL/internal/ptecho/cdc.go:10–26`），而且不只 `porttool answer --usb`，方案里的 USB 那一路也靠它（`$TOOL/internal/ptseq/peer.go:132`）；只有口名的话 Mac 上 USB 那一路测不了，达不到本图终点。

- 解析 `ioreg -r -c IOUSBHostDevice -l -w 0` 的文本输出：每个 USB 设备节点取 `idVendor` / `idProduct`（十进制，转成四位大写十六进制，与 Windows / Linux 一致）、`USB Product Name`、`USB Serial Number`，挂到它子树里的 `IOCalloutDevice` / `IODialinDevice` 上
- `ioreg` 跑不了或解析不出东西时退回只有口名，不报错 —— 列口不能因为描述拿不到而失败
- 解析函数不带平台标签，单元测试在 Windows 上跑；样本是按 `ioreg` 的已知格式手写的，**不是从真 Mac 录下来的**
- 在真 Mac 上验归 [在哪几台真机上验、用例怎么写](XPT-03-which-real-machines-and-what-the-test-case-is.md)

## 引出了什么新的未知

- 手写样本和真 `ioreg` 输出是否一致：在真 Mac 上录一份替换样本，归 [在哪几台真机上验、用例怎么写](XPT-03-which-real-machines-and-what-the-test-case-is.md)
