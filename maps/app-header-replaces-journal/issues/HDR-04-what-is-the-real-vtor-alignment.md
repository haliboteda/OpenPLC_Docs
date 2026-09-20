# VTOR 对齐到底要多少字节

Type: task
Opened: 2026-09-20
Status: open
Blocked by: -

## Question

header 的大小由 app 向量表的对齐要求决定 —— header 有多大，app 的起点就往后挪多少，
而**那个起点必须满足 `SCB->VTOR` 的对齐约束**。

**推导出来的是 1024 字节，但没有在板子上验过。**

推导过程：

```
ARMv7-M 的 VTOR 寄存器 TBLOFF 域 = bit[31:7]   ⇒ 硬件强制至少 128 字节对齐
架构还要求对齐边界不小于向量表本身长度（向上取整到 2 的幂）

H743 最大中断号 WAKEUP_PIN_IRQn = 149          （Drivers/CMSIS/.../stm32h743xx.h:199）
(16 系统异常 + 150 外设中断) × 4 = 664 字节
664 向上取整到 2 的幂 = 1024 字节
```

⚠️ **这条错了整个方案要重来** —— 如果实际要 2048，header 的浪费翻倍；如果 512 就够，
能省一半。而且对齐不满足时的表现是**跳转后跑飞**，不是干净报错，现场很难查。

⚠️ 顺带要确认的第二件事：`$CORE_REPO/platform.txt:59,62` 把
`-DVECT_TAB_OFFSET={build.flash_offset}` 传给 app 编译，而 `system_stm32h7xx.c` 里是
`SCB->VTOR = VECT_TAB_BASE_ADDRESS | VECT_TAB_OFFSET`（**或运算，不是加法**）。
`0x08000000 | 0x20400 = 0x08020400` 恰好是对的，但**这依赖两个数不重叠位**，
换个 offset 值可能就不成立了。这条要在同一次实验里一并看。

## 怎么算答完

在**真板子**上做完这两件，并把观察到的原话记进 `## Answer`：

1. **把 app 链接到一个非 1024 对齐的地址**（例如 `0x08020200`），烧进去，复位 —— 记录板子的实际表现
   （跳转成功？HardFault？跑飞？串口打了什么？）
2. **链接到 `0x08020400`**，烧进去，复位 —— 确认能正常跑起来，且 app 侧读到的 `SCB->VTOR` 就是 `0x08020400`
3. 写下**最终采用的 header 大小**，以及它是实测确认的还是仍按架构规则推的

> 对照参考：`ref/Hello_World_OpenPLC/Core/Src/system_stm32h7xx.c` 是「app 侧 VTOR 怎么设」的现成样例，
> **它是对照不是权威，不要改它**。
