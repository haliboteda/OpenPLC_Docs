# 要不要出 arm64 版

Type: grilling
Opened: 2026-09-30
Status: open
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
