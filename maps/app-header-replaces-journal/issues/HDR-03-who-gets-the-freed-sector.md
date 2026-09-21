# 让出来的 128 KiB state 扇区给谁

Type: grilling
Opened: 2026-09-20
Status: resolved
Blocked by: HDR-02

## Question

metadata 搬走之后，`IAP_STATE_SECTOR_ADDR`（`0x081E0000`，Bank2 Sector7）这 128 KiB 空出来。**给谁？**

⚠️ **被 [八种事件日志留不留，留的话住哪](HDR-02-do-the-event-logs-survive.md) 挡着** —— 日志要是留在原地，这个扇区就没空出来。

三个候选：

| | 给谁 | 得到 | 要处理什么 |
|---|---|---|---|
| **F1** | **app 区**，`IAP_APP_MAX_SIZE` 从 1792 KiB 涨到 1920 KiB | app 多 128 KiB | `Erase_FLASH()` 里那道守卫（`flashAddress + Len > IAP_STATE_SECTOR_ADDR → HAL_ERROR`）**是全代码唯一挡在 app 上传和 bootloader 状态之间的东西**，边界挪了要重新论证它挡的是什么 |
| **F2** | **校准值** | `DECISIONS.md` 第 45 条的掉电冲突**自动消失** | 见下 |
| **F3** | 空着 | 零风险，留给以后 | 什么都没得到 |

### F2 值得单独看 —— 它解掉一个已存在的设计冲突

[`DECISIONS.md` 第 45 条](../../../docs/tables/DECISIONS.md)（用户 2026-09-14 定）把校准值放在 state 扇区**最后 8 个槽**，
由 `journal_reclaim()` 擦扇区之前读进 RAM、擦完写回。

⚠️ **那条搬运会打破 journal 设计的地基**：今天「reclaim 不引入任何新失败模式」这句话成立，
是因为擦的那一刻掉电最坏是「需要重刷固件」，而那个结论本来就已成立。**校准值不一样 ——
重刷固件不会恢复它**，要重新标定或重新用 JLINK 写。

**没有 journal 就没有 reclaim，校准值独占一个永不擦的扇区，这个冲突根本不存在。**

⚠️ 但 F2 有个前置动作：扇区里现在装着旧 journal 记录，**必须先擦一次**，否则旧记录会被当成校准值读。

⚠️ 这一条的代码用户 2026-09-14 说过 AI 不写（「校准码代码不用写，你就写个 todo 就行」），
2026-09-16 又说「暂时不动」（见 [`waiting/WAITING-ON.md`](../../../waiting/WAITING-ON.md)）。
**本票只定归属，不写实现。**

### ⚠️ 校准值在这块板上没有别的地方可去（2026-09-20 核实）

**业界做法是板载 EEPROM。** TI 的 PLC 模拟模块参考设计（`TIDU189` 16 位模拟输出、
`TIDU192` 12 位模拟输入）原文：「On-board EEPROM has been provided to store calibration
data and module configuration」，输入输出模块都是。芯片级还有两层：MAX22000 内部有每通道
校准系数寄存器，DAC8760 有 gain / zero error 校准寄存器；出厂微调用片上熔丝。

**但这块板上没有 EEPROM。** 出处 `$HW/Bridge_overview.txt`（从原理图 + BOM 提取）：
Bridge 是唯一装 MCU 的板，器件是 STM32H743IIK6、SDRAM、LAN8742A PHY、USB-C、
microSD 卡座、JTAG/SWD、VL1220 电池、晶振、电压监控 —— **没有 EEPROM**。
四个板的 BOM csv 搜 `eeprom` / `24C` / `24LC` / `AT24` / `M24` / `FRAM` **全部零命中**。

逐个排除剩下的候选：

| 候选 | 能不能放校准值 |
|---|---|
| 独立 EEPROM | ❌ **板上没有** |
| microSD 卡 | ❌ 可拔插 —— 校准值是**这块板的身份**，不能跟着卡走 |
| RTC 备份寄存器（有 VL1220 电池撑着） | ❌ 三条都不行：**① 会丢**（电池没电就清零，而 `R1-31` 和 DR3 的 VBAT witness 正是为检测这件事存在的；校准值丢了要回产线）**② 撞过车**（2026-08-17，witness 和 app 的 nonce 计数器撞在 DR2）**③ 装不下**（空的只有 DR0 + DR5–DR9 = 24 字节，而设计要 256 字节）。分配表在 `$PROD/docs/repo/ARCHITECTURE.md` |
| app 区 / header | ❌ 每次升级被擦重写；且校准值由**上位机经 JLINK** 写（第 45 条），要改它就得擦整扇区 ⇒ **连 app 一起擦掉** |
| MCU 的 OTP 区 | ⚠️ HAL 有地址定义（`0x08FFF000`–`0x08FFF3FF`，1 KiB），但被 `#if defined(FLASH_OPTCR_PG_OTP)` 包着而 H743 头文件里没这个宏。**可用性未核实**；且 OTP 一次性，与「重新校准必须能覆盖」冲突 |
| **扇区 15** | ✅ **唯一剩下的** |

> ✅ **那 127.7 KiB 闲置不是设计失误，是这块板没有为校准值留专门器件的后果。**
> flash 的擦除粒度决定了：要保护几百字节不被 app 擦掉，就得独占一个扇区。

⚠️ **顺带一条硬件侧观察（不在本票范围，选型和判据是硬件工程师的事）**：`I2C3` 和 `I2C4`
都已经引到 J2 连接器上了，下一版硬件若加一颗 I2C EEPROM，校准值就不必再占 flash 扇区。

## 怎么算答完

1. 选定 F1 / F2 / F3 之一，一句话定论
2. 选 F1 的话：**写出 `Erase_FLASH()` 那道守卫改成什么**，并回答「守卫挪走之后，还有什么挡在 app 上传和 bootloader 自身之间」
3. 选 F2 的话：**写明「先擦一次」这个动作由谁在什么时候做**（出厂烧录？第一次升级？），
   并去 `DECISIONS.md` 第 45 条**标注前提已变**（该条现在写着「靠 reclaim 搬运」）
4. 不管选哪个：说明**这次是否改动 `IAP_APP_MAX_SIZE`**，因为它是跨仓镜像项（`boards.txt` 的 `upload.maximum_size`）

## Answer

⚠️ **2026-09-21 用户重开这张票**：**「补偿值不一定非要存在 15 扇区」**，归属重新讨论。
同时本票的前提也变了 —— 新方向是**在现有结构上**加防回滚和补偿值存储，不预设 metadata 已搬走。
**下面是 2026-09-20 的原结论，保留备查，但已不作数。**

### ~~2026-09-20 定~~（已重开）

**选 F2：扇区 15（`IAP_STATE_SECTOR_ADDR`，`0x081E0000`）留给 bootloader 侧，归属写明给校准值。**

理由不是「放这儿方便」，是**排除法之后它是唯一去处** —— 见上面那张候选表：
板上没有 EEPROM（BOM + 器件清单双重确认）、microSD 可拔插、RTC 备份寄存器会随电池掉电丢失且撞过车且只剩 24 字节、
app 区和 header 每次升级都被擦重写、OTP 可用性未核实且一次性。

**附带解掉一个既存冲突**：[`DECISIONS.md` 第 45 条](../../../docs/tables/DECISIONS.md)
原设计让校准值寄生在 journal 扇区最后 8 槽、由 `journal_reclaim()` 搬运，
而**搬运期间掉电会丢校准值，重刷固件救不回来**。没有 journal 就没有 reclaim，
校准值独占一个永不擦的扇区，**这个冲突不再存在**。
append 余量也从 8 槽涨到 4096 槽。

### 判据逐条回答

**第 3 条「先擦一次由谁在什么时候做」**：由**写校准值的那段代码负责，在第一次写入之前擦**。

> ✅ **关键**：日志删掉之后，**没有任何代码会去读扇区 15** —— bootloader 不再扫它，
> 启动判定改看 app 头部的 header。所以旧 journal 残留是**惰性的**，
> 在有人真要用这个扇区之前，里面是什么都无所谓。
> 不需要在固件里安排一次「开机擦一下」，那属于为不存在的问题写代码。

⚠️ 这段代码用户 2026-09-14 定过 AI 不写、2026-09-16 说「暂时不动」，所以**本票只交出这个约束，不交实现**。

**第 4 条「改不改 `IAP_APP_MAX_SIZE`」**：**本票不改**。app 区边界不动，
`Erase_FLASH()` 那道守卫（`flashAddress + Len > IAP_STATE_SECTOR_ADDR → HAL_ERROR`）原样保留。

⚠️ **但 `IAP_APP_MAX_SIZE` 仍然会变，变的原因在另一张票**：header 占掉 app 区开头
约 1024 字节，所以上限要减去 header 大小。那是
[header 那一千多字节里放什么](HDR-05-what-goes-in-the-header.md) 的事，
**两处别重复改** —— 它是跨仓镜像项（`boards.txt` 的 `upload.maximum_size`）。

## 引出了什么新的未知

一条：**`DECISIONS.md` 第 45 条现在有一句过时了** ——「谁保它活着 | `journal_reclaim()`
擦整扇区之前读进 RAM，擦完写回」。没有 journal 之后不再需要任何搬运。

⚠️ **故意先不改那一条**：第 45 条整条的前提（「为什么不另切一个扇区」）都建立在
journal 存在之上，而 journal 要等这张图走完才真的删掉。**现在改会变成描述一个还不存在的状态。**
落点记在这里，**由这张图收尾时一并改**。

## Answer

2026-09-21 定

**本票作废，由 [校准值和 metadata 怎么共用扇区 15](../../version-gate-and-calibration/issues/VER-02-how-do-calibration-and-metadata-share-the-sector.md) 取代。**

前提不成立了：用户 2026-09-21 定**不搬 metadata**，它留在扇区 15。
所以这个扇区从来没有"空出来"，问题从「给谁」变成「两样东西怎么共处」。

新结论（决策 61）：**校准值钉在最前 8 KiB 固定地址，metadata 接在后面 append。**

## 引出了什么新的未知

没有。
