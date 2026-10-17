# RS232 就是控制口，「和上位机收发、加波特率」怎么做

Type: grilling
Opened: 2026-10-11
Status: resolved
Blocked by: -

## Question

[决策 98](../../../docs/tables/DECISIONS.md) 要求 RS232 改成和上位机收发并能选波特率（TODO-fixture 第 36 条），前提写的是「现在是 C05 / C06 短接自回环」。实际上工装的控制口就是这组 RS232（UART4，`$BOOT/TestCase/porttool/porttool_rs232.c` 是 `loop=self`），[HARDWARE-FACTS.md](../../../docs/hardware/HARDWARE-FACTS.md)「RS232 路径」写明这是板上唯一一组 RS232 脚。改它的波特率就是改控制口的波特率。

| 选项 | 做法 | 代价 |
|---|---|---|
| A | 控制口搬到 USB，RS232 空出来单独测 | 控制链路整个换；USB 自身的测试和控制挤在一个口上 |
| B | 测 RS232 时控制口和测试一起切到选定的波特率，测完切回 | 切换中途断了要能自己恢复，否则板子失联 |
| C | 维持现状（控制口通信本身就证明 RS232 收发正常），改决策 98 的描述 | 只在一个波特率下验过 |

## 怎么算答完

选定一种；改决策 98 的那一行，要做的列进 TODO-fixture。

## Answer

2026-10-11 用户定：**「B 其他推荐」**。选 B：测 RS232 时板子和电脑一起切到选定的波特率，测完切回；超时没收到命令板子自动切回（决策 104）。

## 引出了什么新的未知

没有。
