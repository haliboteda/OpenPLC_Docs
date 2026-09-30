# 在哪几台真机上验、用例怎么写

Type: grilling
Opened: 2026-09-30
Status: open
Blocked by: XPT-01, XPT-02

## Question

`T4-01` / `T4-02`（[M4-production-fixture.md](../../../docs/modules/M4-production-fixture.md)）只在 Windows 上跑过。终点要每个平台一条跑过的用例。要定：

- 有没有 Linux 实机、Mac 实机（WSL 默认接不到 USB 串口）；没有的话怎么办
- 每个平台的用例测什么：只打开面板连上模拟板，还是接真板子逐路测
- Linux 串口权限（`dialout` 组）由谁、在哪一步处理
- macOS 上 `ioreg` 补 VID 的解析，样本是手写的：在真 Mac 上录一份真输出替换 `$TOOL/internal/serialx` 里的测试样本

## 怎么算答完

写明每个平台用哪台机器（型号 / 系统版本）、用例编号和判据，以及这条用例测不到什么。
