# 0.1.3 怎么命名、按什么顺序发

Type: grilling
Opened: 2026-09-24
Status: resolved
Blocked by: -

## Question

发 `0.1.3` 要定的几件事（事实见 [IDE-01-findings.md](../IDE-01-findings.md)）：

- **tag 叫什么** —— `open_plc_arduino` 已经有一个叫 `v0.1.3` 的**分支**（远端也有），再打同名 tag 会让 `v0.1.3` 有两个意思；`v0.1.3-pre` 今天就已经是这样
- **工具包 STM32Tools 升不升版本号** —— 同版本号 IDE 不会重新下载，而网上 0.1.2 里的 IAPTool 不会签名
- **客户填哪个索引地址** —— 现在的地址按版本钉死，而且没有任何文档告诉客户该填哪个
- **12 个本地 commit 还没推上 GitHub** —— 打 tag 之前要先推
- **测试的 `CORE_LIVE` 路径**写死了 `0.1.3-pre`，装上 `0.1.3` 后要换；`init_machine.py` 两个目录都在时会选中旧的

## 怎么算答完

每一件有定案；得到一份发 `0.1.3` 的逐步清单，标出哪一步是对外动作。

## Answer

2026-09-25 定（用户按推荐）。

| 事 | 定案 |
|---|---|
| tag 名 | **`0.1.3`，不带 `v`**（`v0.1.3` 已是分支名，不撞名也不删分支） |
| 工具包 STM32Tools | **升到 `0.1.3`**，和板卡包同号 |
| 客户填的索引地址 | **一个固定地址**：`package_index_json` 仓主分支上的索引文件，列出所有版本；README 写明 |
| 本机装上 0.1.3 之后 | Board Manager 卸掉 `0.1.3-pre`，重跑 `init_machine.py` 更新 `CORE_LIVE` |
| SD 用的 STM32SD + FatFs | **用户从库管理器装**，例程文件头写明（来自 [CAN 和 SD 卡在 Arduino 下最少要补什么](IDE-03-what-can-and-sd-need-in-arduino.md)） |

推 12 个本地 commit、打 tag、发 release、改线上索引都在 [发一个版本，像用户一样从网上装](IDE-12-release-and-install-like-a-user.md) 里做，**动手前单独问用户**。

## 引出了什么新的未知

没有。
