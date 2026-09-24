# 0.1.3 怎么命名、按什么顺序发

Type: grilling
Opened: 2026-09-24
Status: open
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
