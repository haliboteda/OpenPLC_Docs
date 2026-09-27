# 发一个版本，像用户一样从网上装

Type: task
Opened: 2026-09-24
Status: claimed
Blocked by: IDE-01, IDE-14, IDE-06, IDE-07, IDE-08, IDE-09, IDE-10, IDE-11

## Question

按发布流程发一个版本，在干净的 Arduino IDE 里从 Board Manager 装上，打开例程、在 Tools → Port 里选中假板子、Upload。**发布是对外动作，动手前单独问用户。**

## 怎么算答完

从网上装上的那一版里能看到全部例程，并能烧进模拟台上的假板子。

## 执行清单（2026-09-25 按 IDE-01 调查和 IDE-14 定案排好）

命名和地址以 [0.1.3 怎么命名、按什么顺序发](IDE-14-how-is-0-1-3-named-and-released.md) 为准；每一步的出处见 [IDE-01-findings.md](../IDE-01-findings.md) 第 5 节。

| # | 做什么 | 对外？ |
|---|---|---|
| 1 | 编好三平台 IAPTool（`compile_tool.sh`），打成 STM32Tools `0.1.3` 的包，带上 `keys/published_root.TEST_ONLY.pem`；算校验和与大小 | 否 |
| 2 | `open_plc_arduino` 的 `v0.1.3-dev` 推上 GitHub（本地领先的 commit 不推，zip 里就没有） | **是** |
| 3 | `open_plc_arduino` 打 tag `0.1.3` 并推送；下载 GitHub 生成的 zip，算校验和与大小 | **是** |
| 4 | `Arduino_Tools` 提交新二进制、打 tag `0.1.3`、发 release，附件是第 1 步的包 | **是** |
| 5 | 索引 JSON 新增 `0.1.3` 条目（板卡包地址、STM32Tools `0.1.3`），推到 `package_index_json` **主分支**；README 写明客户填的固定地址 | **是** |
| 6 | 干净的 IDE 里填固定地址 → Board Manager 装 `0.1.3` → 例程在 → Tools → Port 选中假板子 → Upload（`T1-34` 对着网上装的这一版再跑一遍） | 否 |
| 7 | 卸掉 `0.1.3-pre`，重跑 `init_machine.py` 更新 `CORE_LIVE` | 否 |

⚠️ 第 3 步的校验和取自 GitHub 自动生成的 zip；GitHub 不保证这个 zip 永远逐字节不变，若日后装不上先查这一条。

## 进度（2026-09-27）

| # | 状态 |
|---|---|
| 1 | ✅ 包在 `E:\tmp\rel013\STM32Tools.tar.gz`（SHA-256 `a50f4d07b83e85d12985ab2e75a062f4f78f664a3304b3bc3667d3b921c34c52`，13320192 字节）；丢了可用 `git -C Arduino_Tools archive --format=tar.gz --prefix=Arduino_Tools-0.1.3/ 0.1.3` 重打 |
| 2 | ✅ 2026-09-27 用户已推，本地与 `origin/v0.1.3-dev` 一致 |
| 3 | ✅ tag `0.1.3` → `1765861` 已推；GitHub zip SHA-256 `f5c60c9197d3e29974365a8bac7c6cce8b8eae6ff4a8a3667606ff3befe11ed4`，18986779 字节 |
| 4 | ✅ `Arduino_Tools` 的 `main` 和 tag `0.1.3`（→ `324b5724`）已推；release 附件下载回来与第 1 步逐字节一致 |
| 5 | 索引条目本地写好，等推送 |
| 6、7 | 未开始 |

⚠️ `Arduino_Tools` 里 linux / macosx 的 `IAPTool` 在 git 里是 `100644`，`git archive` 打出的包在这两个平台上可能没有可执行位；本图只验 Windows，未修。
