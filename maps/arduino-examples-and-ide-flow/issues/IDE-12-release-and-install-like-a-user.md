# 发一个版本，像用户一样从网上装

Type: task
Opened: 2026-09-24
Status: resolved
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
| 1 | ✅ 包即 `Arduino_Tools` release `0.1.3` 的附件（SHA-256 `a50f4d07b83e85d12985ab2e75a062f4f78f664a3304b3bc3667d3b921c34c52`，13320192 字节）；丢了可用 `git -C Arduino_Tools archive --format=tar.gz --prefix=Arduino_Tools-0.1.3/ 0.1.3` 重打 |
| 2 | ✅ 2026-09-27 用户已推，本地与 `origin/v0.1.3-dev` 一致 |
| 3 | ✅ tag `0.1.3` → `1765861` 已推；GitHub zip SHA-256 `f5c60c9197d3e29974365a8bac7c6cce8b8eae6ff4a8a3667606ff3befe11ed4`，18986779 字节 |
| 4 | ✅ `Arduino_Tools` 的 `main` 和 tag `0.1.3`（→ `324b5724`）已推；release 附件下载回来与第 1 步逐字节一致 |
| 5 | ✅ `package_index_json` `f9fabee` 已推，线上固定地址列出 `0.1.3` |
| 6 | ✅ 空数据目录的 arduino-cli（IDE 自带那份，只填固定地址）从网上装上 `0.1.3` 及全部依赖，校验通过；`OpenPLC_Ports` 13 个例程都在；装上的 IAPTool 与 `Output/windows/IAPTool.exe` 逐字节一致；`T1-34` 对着这份安装三种情况全过。没点 IDE 图形界面 |
| 7 | ✅ 2026-09-27 本机 IDE 索引地址换成固定地址，装上 `0.1.3`（arduino-cli 顺带卸掉 `0.1.3-pre` 和 STM32Tools `0.1.2`），`CORE_LIVE` 已重新探测；`P3` 改为不计换行符差异后全绿 |

⚠️ `Arduino_Tools` 里 linux / macosx 的 `IAPTool` 在 git 里是 `100644`，发出去的包里这两个文件是 `-rw-rw-r--`，没有可执行位（2026-09-27 `tar tv` 核实）；本图只验 Windows，未修。

## Answer

2026-09-27 定。`0.1.3` 已发布，客户填 `package_index_json` README 里的固定地址即可从 Board Manager 装上；空数据目录装上的这一版例程齐全，`T1-34` 三种情况全过（假板子，未点 IDE 图形界面，未上真板）。

## 引出了什么新的未知

- `Arduino_Tools` 里 linux / macosx 的 `IAPTool` 没有可执行位（见上文 ⚠️），这两个平台装上后上传未验
- 填了旧的按版本钉死地址（`releases/download/v0.1.3-pre/...`）的人看不到 `0.1.3`，要改填固定地址。用户 2026-09-27 定：由他把固定地址发给用户
- 板卡包 `platform.txt` 仍写 `version=0.1.0rc0`；IDE 按索引版本号装，不影响安装
