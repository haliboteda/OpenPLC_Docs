# DI 正交计数这一项，正交脉冲由谁送

Type: grilling
Opened: 2026-10-11
Status: resolved
Blocked by: -

## Question

[STG-03](STG-03-what-each-port-tests-at-each-level.md) 的研发测试里 DI 有「正交计数」，但没写脉冲从哪来。测试项目录里这一项现在标着待定（`$PORTTOOL/src/ptitems/ptitems.go` 的 `din.quad`）。标准机的 DO 只能逐路开关或出 PWM，没有两路相差 90° 的输出（`$BOOT/TestCase/common/port_dout.c`）。

| 选项 | 做法 | 代价 |
|---|---|---|
| A（推荐） | 标准机固件的 `dout` 加一种两路正交输出（固定频率、相差 1/4 周期），面板按送出的脉冲数判计数 | 改固件；标准机定下来才能上板验 |
| B | 研发自己接编码器或信号发生器，人工填期望计数 | 不改固件；结果靠人 |
| C | 研发测试里先不放这一项 | 正交计数没人测 |

## 怎么算答完

选定一种；要改的列进 TODO-fixture。

## Answer

2026-10-11 用户定：**「B 其他推荐」**，本票按推荐：选 A：标准机固件的 `dout` 加两路正交输出，面板按送出的脉冲数判计数（决策 104）。

## 引出了什么新的未知

没有。
