# 要不要出 arm64 版

Type: grilling
Opened: 2026-09-30
Status: resolved
Blocked by: -

## Question

`$TOOL/compile_tool.sh:35` 写死 `GOARCH=amd64`。Apple Silicon 的 Mac 靠 Rosetta 转译跑 amd64 版；ARM 的 Linux（如树莓派）跑不了。linux/arm64、darwin/arm64 2026-09-30 已确认编得过。

| 选项 | 代价 | 风险 |
|---|---|---|
| A. 只出 amd64 | 不改 | Mac 上依赖 Rosetta；ARM Linux 不支持 |
| B. macOS 加 arm64（或合成一个通用二进制） | 改构建脚本；通用二进制要 `lipo`，Windows 上没有 | 目录要多分一层架构 |
| C. macOS 和 Linux 都加 arm64 | 同 B，多一份 Linux | 同 B |

## 怎么算答完

一句话写明选了哪条，并写出 `Output/` 下的目录结构（每个平台 / 架构一个路径）。

## Answer

2026-09-30 定：**选 B** —— 只给 `PortTool` 另出一份 macOS arm64，Linux 不出 arm64。理由：在售的 Mac 都是 Apple Silicon；ARM Linux 没有人提过。

`Output/` 下的结构（`compile_tool.sh` 一次生成）：

| 路径 | 内容 |
|---|---|
| `Output/windows/` | `IAPTool.exe`、`PortTool.exe`、`plans/`、`keys/` |
| `Output/linux/` | `IAPTool`、`PortTool`、`plans/`、`keys/`（amd64） |
| `Output/darwin/` | `IAPTool`、`PortTool`、`plans/`、`keys/`（amd64，Intel Mac 与 Rosetta） |
| `Output/darwin-arm64/` | `PortTool`、`plans/`（Apple Silicon） |

`Output/darwin` 不改成 arm64：`$TOOL/TestCase/tools/install_tool.py:27` 拿它的 IAPTool 装进板卡包的 `macosx/`。不做通用二进制：要 `lipo`，Windows 上没有，违反「一次生成」。

## 引出了什么新的未知

没有。
