# VTOR 对齐到底要多少字节

Type: task
Opened: 2026-09-20
Status: resolved
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

## 2026-09-21 桌面核实：三条支柱里两条坐实，一条仍是抄件

| 要查的 | 结果 | 出处 |
|---|---|---|
| 向量表多长 | **664 字节** —— 真实 map 实测 `.isr_vector = 0x298`，不是只靠算 | `Drivers/CMSIS/Device/ST/STM32H7xx/Include/stm32h743xx.h:199`（`WAKEUP_PIN_IRQn = 149`） |
| `TBLOFF` 是哪几位 | `_Pos=7`、`_Msk=0x1FFFFFF<<7` ⇒ bit[31:7]，本机三份 CMSIS 一致 | `open_plc_cube_ide/Drivers/CMSIS/Include/core_cm7.h:557-558`。⚠️ **这是抄件，不是硅片** |
| app 当前链在哪 | `build.flash_offset=0x20000` ⇒ `0x08020000`，已是 128K 对齐 | `open_plc_arduino/platform.txt:109` |
| 「架构要求对齐 ≥ 向量表长度」 | ⚠️ **没有查过 ARMv7-M 架构手册原文**，是转述。它是 1024 的支柱，却没有出处 | —— |

**票里第二个担忧（`VECT_TAB_BASE_ADDRESS | VECT_TAB_OFFSET` 的 OR）是假警报，可以划掉**：
那段被 `#if defined(USER_VECT_TAB_ADDRESS)` 包着，而那个宏在两份 core 里**只出现在注释里**
（`open_plc_arduino/system/.../system_stm32h7xx.c:88`）。app 的 VTOR 实际由 bootloader 跳转前
**一处纯赋值**设定：`SCB->VTOR = app_base;`（`open_plc_cube_ide/IAPServer/IAP_server.c:749`）。

⚠️ **顺带发现**：`open_plc_arduino/variants/STM32H7xx/H743/ldscript.ld:61-66` 对 `.isr_vector`
只有 `ALIGN(4)`，**1024 对齐没有任何构建期防线**，全靠 `flash_offset` 这一个数字碰巧是对的。

## 怎么算答完

**实验换成读回寄存器，不再链非对齐地址。** 原方案（链到 `0x08020200` 烧进去看跑不跑）测的是
一条 UNPREDICTABLE 行为 —— 跑通了也只证明这颗片子这次没炸，不构成「512 够用」的证据。

**驱动已经写好**：`$TOOL/TestCase/tools/run_vtor_alignment.py`，探针在 `$TOOL/TestCase/onboard/vtor_probe/`。
`--build-only` 那一半 2026-09-21 在桌面上跑过（向量表落在 `0x08020000`，664 字节），
判读逻辑拿三种合成输出验过（符合头文件 / 与头文件矛盾 / 板子不吭声）。**上板那一半没跑过。**

1. **在 app 里量 `SCB->VTOR` 实际实现了哪几位**：写 `0x08020080`（bit[6:0] 非零）→ 读回 →
   打印 → 写回原值。读回值的低位被丢掉多少，就是硬件强制的对齐。
   **这一步把 `TBLOFF` 从 CMSIS 抄件换成实测。** 代码放 `$TOOL/TestCase/onboard/vtor_probe/`
2. **确认 app 侧读到的 `SCB->VTOR` 就是 `0x08020000`** —— 「app 的 VTOR 只由 bootloader 一处设定」
   这个依赖现在成立且没人验过
3. 写下**最终采用的 header 大小**，以及它哪部分是实测、哪部分仍按架构规则推
   （第 1 步答不了「对齐 ≥ 向量表长度」那条，那条要么查 ARM 手册原文，要么接受按规则推）

> 对照参考：`ref/Hello_World_OpenPLC/Core/Src/system_stm32h7xx.c` 是「app 侧 VTOR 怎么设」的现成样例，
> **它是对照不是权威，不要改它**。


## Answer

2026-09-21 定。**header 取 1024 字节。** 硬件强制的是 **128 字节**（实测），
1024 来自架构规则「对齐 ≥ 向量表长度取整到 2 的幂」，664 → 1024。

真板子实测（`python tools/run_vtor_alignment.py --key <owner.pem>`）：

| 写进 `SCB->VTOR` 的位 | 读回 | 结论 |
|---|---|---|
| bit0 / bit4 / bit6 | 被硬件丢掉 | 不实现 |
| **bit7 / bit8 / bit9** | 原样保留 | 实现 |

⇒ **最低实现位是 bit7，`TBLOFF = bit[31:7]` 成立** —— 和 `core_cm7.h` 一致，
这条从此不再靠抄件。同一次跑还确认 **bootloader 交给 app 的 `SCB->VTOR` 就是 `0x08020000`**。

⚠️ **1024 这一半仍未实测**，而且做不到：违反架构约束的后果是 UNPREDICTABLE，
板子跑得起来也不算证据。要么查 ARMv7-M 架构手册原文，要么按规则取 1024 —— **本票按后者定案**。

⚠️ **没有任何构建期防线守着这个对齐**：`$CORE_REPO/variants/STM32H7xx/H743/ldscript.ld:61-66`
对 `.isr_vector` 只有 `ALIGN(4)`，全靠 `build.flash_offset` 这一个数字碰巧是对的。

## 引出了什么新的未知

**两条。**

1. **给 `build.flash_offset` 加链接期对齐断言** —— 见上，header 改成非 1024 的值时链接器
   一声不吭，而后果是跳转后跑飞。已在 `work/TODO.md`（计划编号 `P15`）。
2. **票里担心的 `VECT_TAB_BASE_ADDRESS | VECT_TAB_OFFSET` 是假警报** —— 那段被
   `#if defined(USER_VECT_TAB_ADDRESS)` 包着，而那个宏在两份 core 里只出现在注释里，
   app 的 VTOR 实际由 bootloader 一处纯赋值设定（`$BOOT/IAPServer/IAP_server.c:749`）。**不用再查。**
