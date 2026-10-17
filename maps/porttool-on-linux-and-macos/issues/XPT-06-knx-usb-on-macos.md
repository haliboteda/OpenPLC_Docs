# macOS 上 KNX USB 接口怎么接

Type: grilling
Opened: 2026-10-16
Status: resolved
Blocked by: -

## Question

PortTool 的 KNX USB 接口在 macOS 上不能用：读写 HID 要调 macOS 的 IOKit，而三个平台都关着 cgo 从 Windows 一次交叉编译（`R4-02`「一次生成」），所以 macOS 走的是 `ErrUnsupported`（`$PORTTOOL/src/knxusb/hid.go:8-11`、`hid_other.go`）。[决策 131](../../../docs/tables/DECISIONS.md)要求三个平台都能用。

| 方案 | 做法 | 代价 | 风险 |
|---|---|---|---|
| A. purego | 用 `github.com/ebitengine/purego` 在运行时加载 IOKit / CoreFoundation，不开 cgo；加一个 `hid_darwin.go` | 一个新依赖；要手写 IOHIDManager 那几个调用 | 没有 Mac，验不了 |
| B. macOS 版开 cgo | 用 hidapi 之类的库 | macOS 版只能在 Mac 上编 | 违反「一次生成」 |

## 怎么算答完

选定一条；macOS 上能列出并打开 KNX USB 接口（要 Mac 真机，归 [XPT-03](XPT-03-which-real-machines-and-what-the-test-case-is.md)）。

## Answer

2026-10-16 用户定：**选 A（purego）**。加只在 darwin 编译的 `hid_darwin.go`，经 purego 调 IOKit 的 IOHIDManager；不开 cgo，一次生成照旧。

## 引出了什么新的未知

- 实现时替用户选的细节，用户 2026-10-16「按推荐」：purego 留 v0.10.2（不升 Go）；写报告加 2 s 超时，用 `IOHIDDeviceSetReportWithCallback`，和 Windows 一致（代码 `$PORTTOOL/src/knxusb/hid_darwin.go`，只过了 darwin 的 build / vet）：
  | # | 现在 | 另一种 |
  |---|---|---|
  | 1 | purego 用 v0.10.2，因为本机和 `go.mod` 是 Go 1.23.1 | 升 Go 到 1.25 再用 v0.11.x |
  | 2 | 写报告同步调 `IOHIDDeviceSetReport`，没有超时（Windows 版有 2 s） | 加 2 s 超时，和 Windows 一致 |
- macOS 上真跑：没有 Mac，归 [在哪几台真机上验、用例怎么写](XPT-03-which-real-machines-and-what-the-test-case-is.md)
