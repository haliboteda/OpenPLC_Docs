# 开机窗口改用什么提示

Type: grilling
Opened: 2026-09-28
Status: resolved
Blocked by: -

## Question

bootloader 开机那 2 秒的 BOOT0 窗口，和按满 10 秒的「恢复出厂已就绪」，现在都靠继电器响来提示（`$BOOT/Core/Src/main.c` 的 `BOOT0_WINDOW_*`、`boot0_armed_signal()`）。改成什么：系统指示灯 PE2（[HARDWARE-FACTS.md](../../../docs/hardware/HARDWARE-FACTS.md)「PE2」）按不同节奏闪、再加串口日志一行，还是别的办法。

⚠️ `boot0_armed_signal()` 的注释写着「This board has no general-purpose LED」，和硬件事实里的 PE2 系统指示灯对不上。

## 怎么算答完

两个提示（窗口开着、恢复出厂已就绪）各定一种形式；开机过程中没有任何继电器、DO、AO 被动作；真板子上照新提示能进 upload 模式、能恢复出厂。

## Answer

2026-09-28 定（用户按推荐定）。改用系统指示灯 PE2 加串口日志：窗口那 2 秒灯快闪，按满 10 秒「恢复出厂已就绪」时灯常亮；**开机不动任何继电器、DO、AO**。见 [决策 71](../../../docs/tables/DECISIONS.md)。

## 引出了什么新的未知

没有。实施项见 [work/TODO.md](../../../work/TODO.md)。
