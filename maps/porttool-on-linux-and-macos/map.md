# 工装在 Linux / macOS 上运行

## 怎么看进度（不用问任何人）

```
python tools/list_wayfinder_map_frontier.py --all
```

## Destination

`PortTool` 在 Windows、Linux、macOS 上都能双击打开面板，并逐路测完板上每个端口；三个平台的可执行文件由一条命令一次生成；每个平台各有一条跑过的用例，并写明这条用例测不到什么。**带执行。**

## Notes

- **终点是用户 2026-09-30 定的**，需求落在 [M4-production-fixture.md](../../docs/modules/M4-production-fixture.md) 的 `R4-02`
- **用户 2026-09-30**：能并行的就开始做，只做必要的代码、功能和测试；同一会话可以做本图多张票
- **「一次生成」是硬约束**：排除给 macOS 开 cgo（开了 Mac 版只能在 Mac 上编）
- 现状（`$TOOL` 在 `9187f59`，2026-09-30 在 Windows 上交叉编译，未在 Linux / macOS 上运行）：
  - linux/amd64、linux/arm64、darwin/amd64、darwin/arm64 都编得过；`$TOOL/compile_tool.sh:14–35` 已一次出三个平台，但 `GOARCH=amd64` 写死
  - 浏览器、ping、模拟板文件名已按平台分开（`$TOOL/internal/ptpanel/panel.go:797`、`net.go:144`、`$TOOL/internal/simboard/simboard.go:40`）
- 和 [Linux / macOS 用户怎么拿到能运行的 IAPTool](../arduino-examples-and-ide-flow/issues/IDE-15-how-do-linux-and-macos-users-get-an-executable-iaptool.md) 是同一类发布问题（可执行位），先后见本图的票
- **要用到的 skill**：`grilling`（本图的票）
- 开票 / 关票 / 算前沿照 [图与票的约定](../MAP-AND-TICKET-CONVENTION.md)

## 全集

在工作区根目录跑（bash，要 `go`）。按「`PortTool` 自己的代码里行为随操作系统变的地方」找：`PortTool` 依赖的本仓各包里的平台构建标签、`runtime.GOOS` 分支、调外部程序、写死的 Windows 名字（`.exe`、`COMn`），加上发版脚本里的平台和架构：

```
(cd IAPTranfer_Tool && for d in $(go list -deps -f '{{if not .Standard}}{{.ImportPath}}{{end}}' ./cmd/porttool | grep '^IAPTool' | sed 's#^IAPTool#.#'); do grep -nE '//go:build|runtime\.GOOS|exec\.Command|\.exe"|COM[0-9]' $d/*.go | grep -v '_test\.go:'; done; grep -nE 'GOOS|GOARCH|PLATFORMS=' compile_tool.sh)
```

2026-09-30 是 28 行：Go 源码 24 行（12 个文件），`compile_tool.sh` 4 行。关最后一张票前重跑，每一行都要落在「三个平台都验过」「明确与平台无关」两类之一。

⚠️ 这条命令抓不到**第三方库里的平台差异**（如 `go.bug.st/serial` 在 darwin 上不给 VID）和**操作系统本身的差异**（Linux 串口要 `dialout` 组权限）。前者归 [macOS 上串口没有描述和 VID 怎么办](issues/XPT-01-macos-serial-port-without-description-or-vid.md)，后者归 [在哪几台真机上验、用例怎么写](issues/XPT-03-which-real-machines-and-what-the-test-case-is.md)。

## Decisions so far

- [macOS 上串口没有描述和 VID 怎么办](issues/XPT-01-macos-serial-port-without-description-or-vid.md)：调系统自带的 `ioreg` 补 VID / PID，不开 cgo
- [要不要出 arm64 版](issues/XPT-02-whether-to-ship-arm64.md)：只给 PortTool 加 `Output/darwin-arm64/`，Linux 不出 arm64

## Not yet specified

- **帮助文本和面板里写死的 `COM7` / `COM16` 示例**（`$TOOL/cmd/porttool/run.go`、`answer.go`）在 Linux / macOS 上要不要换成本平台的写法：等真机上看过面板和 CLI 才知道还有哪些类似的地方

## Out of scope

- **`IAPTool` 的多平台**：已在 [Arduino 例程与 IDE 烧录流程](../arduino-examples-and-ide-flow/map.md) 那张图里
- **固件**：板子那头不因上位机平台而变
