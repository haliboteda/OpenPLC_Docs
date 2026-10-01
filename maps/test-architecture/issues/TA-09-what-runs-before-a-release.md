# 发版之前要跑什么

Type: grilling
Opened: 2026-10-02
Status: resolved
Blocked by: TA-01, TA-03

## Question

现在发版前跑的是 `IAPTranfer_Tool` 的一个 `selfcheck`，加 `ACCEPTANCE-CHECKLIST.md`。拆成各仓自检加 `$TEST` 之后，发一版板卡包、发一版 IAPTool、发一版 bootloader，各要跑哪几个仓的哪几项。

## 怎么算答完

三种发版各一张清单，每项写到「哪个仓的哪条命令」；`ACCEPTANCE-CHECKLIST.md` 要改的地方列出来。

## Answer

2026-10-02 定（用户按推荐定，九件一次定完）。每次发版跑四样：被发的那个仓自己的自检、`$TEST` 的全部契约测试、`$TEST` 里和它有关的整机项、`$PROD` 的文档检查。整机项：板卡包 = 例程逐个上板 + T1-34；IAPTool = T1-34 + 五条用户路径；bootloader = 五条用户路径 + 掉电（T1-21/T1-22）+ 按住 BOOT0（T1-27）；PortTool 只跑自己的自检。`ACCEPTANCE-CHECKLIST.md` 每项写明「哪个仓的哪条命令」。`build_image.py`（命令行编 bootloader）和 `flash_bootloader.py` 进 `$TEST`：bootloader 发版照常用 CubeIDE 编。

## 引出了什么新的未知

没有。
