# 假板子要像到什么程度，arduino-cli 的 upload 才能走完

Type: research
Opened: 2026-09-24
Status: open
Blocked by: -

## Question

要在模拟台上走通「Tools → Port 里出现板子 → Upload」，假板子要回应哪些东西：网络发现、app 状态下的重启握手、bootloader 状态下的挑战和 `flash`、上传完成后的「重新上线」。现有 `$TOOL/TestCase/host/fakeboard/fake_board.py` 已经会哪些、缺哪些。

## 怎么算答完

列出 arduino-cli upload 一次在线上的完整往返（从 IAPTool 的代码里读出来，引代码行），逐条标出假板子已有 / 要补；并说明这条模拟**测不到**什么。
