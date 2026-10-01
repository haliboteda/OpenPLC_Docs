# 板卡包仓的测试怎么跑

Type: grilling
Opened: 2026-10-02
Status: open
Blocked by: -

## Question

变体头断言（P4）、全部例程能编过（P5）、app 起始地址对齐（P15）都离不开 `arduino-cli`。搬进 `open_plc_arduino` 后，那个很薄的驱动脚本用什么语言、放在仓的哪里、怎么找到本机的 `arduino-cli`；`$CORE_LIVE` 和 `$CORE_REPO` 两份里测哪一份。

## 怎么算答完

三项各有：住在哪个路径、用什么命令跑、在一台只 clone 了 `open_plc_arduino` 的机器上需要先装什么。
