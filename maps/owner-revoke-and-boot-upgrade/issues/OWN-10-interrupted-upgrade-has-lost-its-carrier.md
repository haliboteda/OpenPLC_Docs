# 升级被打断怎么报，原方案的载体已经没了

Type: grilling
Opened: 2026-09-21
Status: claimed
Blocked by: -

## Question

[升级被打断之后，板子怎么让人知道](OWN-04-how-does-an-interrupted-upgrade-announce-itself.md) 定的办法是
**写两条 journal 事件**（擦扇区 0 之前一条「升级开始」、写回完成之后一条「升级完成」），
理由是「journal 扇区在 `0x081E0000`（Bank 2），整个升级过程不会被擦，所以这两条能活下来」。

**那个载体已经被另一张图删掉了。**

| 哪张票 | 定了什么 |
|---|---|
| [八种事件日志留不留，留的话住哪](../../app-header-replaces-journal/issues/HDR-02-do-the-event-logs-survive.md) | **全删** —— 八种事件、`journal_log()`、`M1/JOURNAL.md` 一起删 |
| [让出来的 128 KiB state 扇区给谁](../../app-header-replaces-journal/issues/HDR-03-who-gets-the-freed-sector.md) | 整个扇区划给**校准值** |

两张图各自都写明「本图不碰对方那半边」，于是这处对撞正好落在两张图的缝里，**谁都没发现**。

### 为什么要紧

`flashboot` 擦扇区 0 的中途掉电，板子起不来，而扇区 0 是空的 ——
**这时候没有任何软件还在跑**，只能按 BOOT0 进 DFU 重刷。要让人知道
「上次是升级没升完，不是板子坏了」，得有个**掉电能活下来、且不在扇区 0 里**的地方。

这条挡着 [要改的东西，一条不落](../CHANGE-LIST.md) 的 **A14**（journal 事件表加两条）
和 **F7**（`M1-firmware-upgrade.md` 的事件表加两条）—— 两行现在都指着不存在的东西。

### 候选

| | 载体 | 要想清楚什么 |
|---|---|---|
| ① | **RTC 备份寄存器**一个标志位 | 会随 VBAT 没电丢失（`R1-31` 就是查这个），而且**备份寄存器撞过车** —— 认领之前要看占用表（`$PROD/docs/repo/ARCHITECTURE.md`） |
| ② | **校准值扇区里留一个定长小区** | HDR-03 把整个扇区给了校准值，要回头改那条的边界；好处是掉电和 VBAT 都不怕 |
| ③ | **owner 记录区**（`0x0801E000`） | ⛔ **不行** —— 它和 bootloader 同在扇区 0，升级时正在被擦 |
| ④ | **不报** | 新 bootloader 起不来本身就是信号，靠 DFU 那套流程的文档说清。代价是现场分不出「升级没升完」和「板子坏了」 |

## 怎么算答完

1. 定下载体，写进 [M1 固件升级](../../../docs/modules/M1-firmware-upgrade.md)
2. 把 [要改的东西，一条不落](../CHANGE-LIST.md) 的 **A14** 和 **F7** 两行按新答案改掉
3. 说清**这条新机制自己怎么验** —— 掉电中断 `flashboot` 是个破坏性用例，
   判据要写成能判真假的话（参照 `T1-21`/`T1-22` 怎么验「掉电中断升级后仍可恢复」）
4. 若选 ②，回头说明 HDR-03 的「整个扇区归校准值」要不要改口


## 2026-09-21 查证：候选的可行性不是等价的

**这个场景要的载体必须同时扛住两件事：掉电，以及随后用 SWD 重刷扇区 0 的救砖动作。**
（扇区 0 空了板子什么都跑不了，所以「报出来」的一定是**救回来之后的新 bootloader**去读。）

| 载体 | 扛掉电 | 扛救砖 | 依据 |
|---|---|---|---|
| **RTC 备份寄存器** | ✅ **但依赖 VBAT** | ✅ 救砖不碰 RTC | `T1-17` 2026-09-19 真断电验收过（ST-Link 量到 0.00V，计数器不归零）。⚠️ 而 `R1-31` 的存在就是因为 VBAT 会没电 —— **VBAT 一空，恰好在最需要它的时候丢** |
| **扇区 15（校准值那块）** | ✅ flash | ✅ **救砖用 `STM32_Programmer_CLI -w <elf>`，只写 ELF 占的扇区，不是整片擦** | `tools/flash_bootloader.py:131-132` |
| SRAM4 no-init | ❌ **掉电就丢** | — | `docs/hardware/HARDWARE-FACTS.md`「SRAM4 的 no-init 机制」明写「掉电仍然丢」 |
| owner 记录区 | ❌ 和 bootloader 同在扇区 0，正在被擦 | — | `owner_slot.h` |

⇒ **只有扇区 15 是无条件成立的**；RTC 备份寄存器成立但有 VBAT 这个前提。

**空闲的备份寄存器**（真要用的话）：`DR0`、`DR5`–`DR9`，共 6 个。分配表在
`docs/repo/ARCHITECTURE.md`，⚠️ 认领前必看 —— 2026-08-17 撞过一次车。
