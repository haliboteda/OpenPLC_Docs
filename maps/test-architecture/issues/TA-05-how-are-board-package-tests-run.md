# 板卡包仓的测试怎么跑

Type: grilling
Opened: 2026-10-02
Status: resolved
Blocked by: -

## Question

变体头断言（P4）、全部例程能编过（P5）、app 起始地址对齐（P15）都离不开 `arduino-cli`。搬进 `open_plc_arduino` 后，那个很薄的驱动脚本用什么语言、放在仓的哪里、怎么找到本机的 `arduino-cli`；`$CORE_LIVE` 和 `$CORE_REPO` 两份里测哪一份。

## 怎么算答完

三项各有：住在哪个路径、用什么命令跑、在一台只 clone 了 `open_plc_arduino` 的机器上需要先装什么。

## Answer

2026-10-02 定（用户按推荐定，九件一次定完）。全部进 `open_plc_arduino/tests/`。P3、P4、P5、P15、P19 用很薄的 Python 脚本，`arduino-cli` 从 PATH 或环境变量 `ARDUINO_CLI` 找，不要本机配置文件；T2-21 照 bootloader 的做法用 CMake/CTest。测仓里那一份：让 `arduino-cli` 直接把仓库目录当板卡包来编；实测做不到就退回 `$CORE_LIVE`，并回报。

## 引出了什么新的未知

没有。
