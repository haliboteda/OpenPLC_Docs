# 编程模式怎么进、怎么让人看到

Type: grilling
Opened: 2026-10-03
Status: resolved
Blocked by: -

## Question

ETS 编物理地址时要求设备进编程模式。本板的编程键 `KNX_Prog_KEY`（PG9）和 BOOT0 是同一条网，编程灯 `KNX_Prog_LED`（PG11）这根线上没有灯（[HARDWARE-FACTS.md](../../../docs/hardware/HARDWARE-FACTS.md)「KNX 接口」）。编程模式用什么进、用什么退、用什么显示，才能不和 bootloader 的开机窗口（按住 BOOT0 复位 = 进上传模式）以及系统灯现有的用法打架。

## 怎么算答完

定下进、退、显示的方式；写明它和 bootloader 开机窗口、`SystemLED` 例程各自怎么区分。

## Answer

2026-10-03 定（用户：按推荐）：

| 问题 | 定了什么 | 一句理由 |
|---|---|---|
| 怎么进、怎么退 | app 运行中短按 BOOT0 键切换；再按一次或 ETS 编完地址后退出。**不要按着它上电或复位** —— 那是 bootloader 的上传模式，按满 10 秒恢复出厂 | 板上只有这一个键；MCU 只在复位时采样 BOOT0，运行中按不会进 bootloader |
| 怎么显示 | 系统灯 PE2 常亮 = 编程模式；USB 串口打印 `KNX: programming mode on` / `off`。用了 KNX 库，系统灯归编程模式用 | 全板只有这一个灯（HARDWARE-FACTS「PE2」）；PG11 那根线上没有灯 |
| 脚本能不能替人按 | 不能。用例提示人按一次，脚本从那行串口输出自动判 | 只为测试服务的代码会被用户照抄进自己的程序 |

## 引出了什么新的未知

无。
