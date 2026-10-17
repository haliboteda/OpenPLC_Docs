# 要不要出 arm64 版

Type: grilling
Opened: 2026-09-30
Status: resolved
Blocked by: -

## Question

当时 `$TOOL` 的 `compile_tool.sh:35`（2026-10-16 并进 `build.py`，决策 144）写死 `GOARCH=amd64`。Apple Silicon 的 Mac 靠 Rosetta 转译跑 amd64 版；ARM 的 Linux（如树莓派）跑不了。linux/arm64、darwin/arm64 2026-09-30 已确认编得过。

| 选项 | 代价 | 风险 |
|---|---|---|
| A. 只出 amd64 | 不改 | Mac 上依赖 Rosetta；ARM Linux 不支持 |
| B. macOS 加 arm64（或合成一个通用二进制） | 改构建脚本；通用二进制要 `lipo`，Windows 上没有 | 目录要多分一层架构 |
| C. macOS 和 Linux 都加 arm64 | 同 B，多一份 Linux | 同 B |

## 怎么算答完

一句话写明选了哪条，并写出 `Output/` 下的目录结构（每个平台 / 架构一个路径）。

## Answer

2026-09-30 定：**选 B** —— 只给 `PortTool` 另出一份 macOS arm64，Linux 不出 arm64。理由：在售的 Mac 都是 Apple Silicon；ARM Linux 没有人提过。

`Output/bin/` 下的结构（`$PORTTOOL/tools/build.sh tool` 一次生成；本机的模拟板也编在对应平台目录里）：

| 路径 | 内容 |
|---|---|
| `Output/bin/windows/` | `PortTool.exe`、`plans/` |
| `Output/bin/linux/` | `PortTool`、`plans/`（amd64） |
| `Output/bin/darwin/` | `PortTool`、`plans/`（amd64，Intel Mac 与 Rosetta） |
| `Output/bin/darwin-arm64/` | `PortTool`、`plans/`（Apple Silicon） |

`Output/` 指 `$PORTTOOL/Output/`（决策 76 拆仓后 IAPTool 不在这里；它的 macOS arm64 见 IDE-18）。不做通用二进制：要 `lipo`，Windows 上没有，违反「一次生成」。

## 引出了什么新的未知

没有。
