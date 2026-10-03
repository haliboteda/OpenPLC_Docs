# 编程模式怎么进、怎么让人看到

Type: grilling
Opened: 2026-10-03
Status: open
Blocked by: -

## Question

ETS 编物理地址时要求设备进编程模式。本板的编程键 `KNX_Prog_KEY`（PG9）和 BOOT0 是同一条网，编程灯 `KNX_Prog_LED`（PG11）这根线上没有灯（[HARDWARE-FACTS.md](../../../docs/hardware/HARDWARE-FACTS.md)「KNX 接口」）。编程模式用什么进、用什么退、用什么显示，才能不和 bootloader 的开机窗口（按住 BOOT0 复位 = 进上传模式）以及系统灯现有的用法打架。

## 怎么算答完

定下进、退、显示的方式；写明它和 bootloader 开机窗口、`SystemLED` 例程各自怎么区分。
