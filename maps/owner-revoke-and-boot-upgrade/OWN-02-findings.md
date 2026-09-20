# 擦扇区 0 的时候，那段代码从哪执行 —— 调查产出

**回答的是票 [擦扇区 0 的时候，那段代码从哪执行](issues/OWN-02-where-does-the-erase-code-run.md)。**
2026-09-20。**只读代码、读 map 文件、查 RM0433，没有改任何代码，没有碰板子。**

代码事实一律给 `文件:行号`，取自 `$BOOT` = `E:\WorkSpace\Schaeffer-AG\open_plc_cube_ide`。
链接结果取自已有的构建产物 `Debug/open_plc_cube_ide.map`（未重新编译）。

⚠️ **RM0433 的引文出处说明**：这台机器**直连 st.com 取不到 PDF**（curl 92/52，HTTP 抓取 60 秒超时），
实际读的是同一份文件的大学镜像，**打开后封面标的是 `January 2023 RM0433 Rev 8`，章节号和页码自洽**。
引文逐字抄自该 PDF 解出的文本。**要当作权威引用前，建议拿 ST 官网那份对一次。**

---

## 结论先说

> ✅ **擦扇区 0 这段代码必须放在 RAM（`RAM_D1`，`0x24000000`）里跑，而且整段窗口要关中断。**

理由一句话：扇区 0 被擦掉之后 flash 里**没有指令可取**，不论 read-while-write 怎么规定都救不回来。

⚠️ **顺带一个好消息：链接脚本和启动代码都不用改。** `.RamFunc` 段已经在 `.data` 里
（[STM32H743IIKX_FLASH.ld:166-167](../../../open_plc_cube_ide/STM32H743IIKX_FLASH.ld)），
启动代码的 `.data` 拷贝循环已经会把它搬进 `RAM_D1`
（[startup_stm32h743xx.s:66-81](../../../open_plc_cube_ide/startup_stm32h743xx.s)）。
**要改的只是新写的那个函数加 `__RAM_FUNC`，以及它不能再调 HAL。** 详见第三节。

这使 [CHANGE-LIST.md](CHANGE-LIST.md) 的 **A13（链接脚本 / 启动代码：加 `.RamFunc` 段 + 启动时拷贝）**
从「要改」降级成「已经有了，只要用」。

---

## 问题一 · 现有的擦写代码跑在哪

> ✅ **全部从 flash 取指，`$BOOT` 里没有一行 RAM 驻留代码。** 而且它们都住在 **Bank 1 扇区 0**，
> 也就是 bootloader 自己那 128 KiB 里。

### 源码侧：没有任何 `__RAM_FUNC` 标注

`__RAM_FUNC` 这个宏**定义了但全工程没人用**：

| 事实 | 出处 |
|---|---|
| 宏定义 `#define __RAM_FUNC __attribute__((section(".RamFunc")))` | `Drivers/STM32H7xx_HAL_Driver/Inc/stm32h7xx_hal_def.h:194` |
| `IAPServer/`、`Core/`、`LWIP/`、`USB_DEVICE/` 里 `__RAM_FUNC` 出现 **0 次** | `grep -rn "__RAM_FUNC" IAPServer Core LWIP USB_DEVICE` 无输出 |
| ST HAL 的 `Src/` 里 `__RAM_FUNC` 也出现 **0 次** | 同上，对 `Drivers/STM32H7xx_HAL_Driver/Src/` |
| 工程里仅有的 `__attribute__((section(...)))` 是以太网 DMA 描述符和 RX 池，都是**数据不是代码** | `LWIP/Target/ethernetif.c:110`、`:111`、`:120` |

### 链接结果侧：地址证明它们在 flash

从 `Debug/open_plc_cube_ide.map` 取的实际地址（都落在 `0x08000000`–`0x0801FFFF`，即 Bank 1 扇区 0）：

| 函数 | 源码位置 | 链接后的地址 | 段 |
|---|---|---|---|
| `Flash_If_Erase()` | `Core/Src/usbd_cdc_flash.c:37` | `0x08001590` | `.text.Flash_If_Erase` |
| `Flash_If_Write()` | `Core/Src/usbd_cdc_flash.c:90` | `0x0800164c` | `.text.Flash_If_Write` |
| `Erase_FLASH()` | `Core/Src/usbd_cdc_flash.c:222` | `0x080016f0` | `.text.Erase_FLASH` |
| `HAL_FLASHEx_Erase()` | ST HAL | `0x08002cc4` | `.text.HAL_FLASHEx_Erase` |
| `FLASH_Erase_Sector()` | ST HAL | `0x08002c7c` | `.text.FLASH_Erase_Sector` |
| `HAL_FLASH_Program()` | ST HAL | `0x08002b4c` | `.text.HAL_FLASH_Program` |
| `FLASH_WaitForLastOperation()` | ST HAL | `0x08002a8c` | `.text.FLASH_WaitForLastOperation` |
| `HAL_GetTick()` | ST HAL | `0x080019b0` | `.text.HAL_GetTick` |
| `journal_reclaim()` | `IAPServer/bootloader_state.c:312` | 被内联进 `bootloader_state_save_metadata` = `0x08007cb4` | `.text` |

`journal_reclaim()` 是 `static` 且只有一个调用点，编译器把它内联掉了，所以 map 里没有独立符号 ——
`arm-none-eabi-nm -n` 里也查不到它，能查到的是包住它的 `bootloader_state_save_metadata`。

### 谁擦哪个 bank —— 票里的猜测只对了一半

全工程只有**两个** `Flash_If_Erase()` 调用点：

| 调用点 | 擦哪 | 哪个 bank |
|---|---|---|
| `IAPServer/bootloader_state.c:318` —— `journal_reclaim()` | `IAP_JOURNAL_BASE` = `IAP_STATE_SECTOR_ADDR` = `ADDR_FLASH_SECTOR_7_BANK2` = `0x081E0000`，1 个扇区 | **Bank 2** |
| `Core/Src/usbd_cdc_flash.c:243` —— `Erase_FLASH()`，唯一调用者是 `IAPServer/IAP_server.c:95` | `app_base` = `IAP_APP_ADDRESS` = `0x08020000` 起，长度到 app 实际大小，上限 `IAP_APP_MAX_SIZE` = `0x081E0000 - 0x08020000` = **1,835,008 B** | **Bank 1 扇区 1–7 + Bank 2 扇区 0–6** |

常量出处：`Core/Inc/usbd_cdc_flash.h:21`（`0x08020000`）、`:30`（Bank 2 起点 `0x08100000`）、
`:37`（`0x081E0000`）、`:74-76`；`IAPServer/bootloader_state.c:18`；bank 判定在
`Core/Src/usbd_cdc_flash.c:199` 的 `GetBank()`（`< 0x08100000` 就是 Bank 1）。

> ⚠️ **票里写「journal 扇区在 Bank 2 …… 所以今天可能根本没碰到这个问题」—— 这一半是错的。**
> journal 那条确实只碰 Bank 2，但**升级 app 那条每次都擦 Bank 1 的 7 个扇区，
> 而 bootloader 正从 Bank 1 扇区 0 取指。** 所以「擦 Bank 1 的同时从 Bank 1 取指」
> 这件事，**这个产品每做一次固件升级就干一次**，只是擦的不是自己那个扇区。

还有一条同类的：owner 记录追加 **是往 Bank 1 扇区 0 自己身上写**（不是擦）。
`IAPServer/owner_slot.c:336` 和 `:340` 调 `Flash_If_Write()` 写 `OWNER_SLOT_BASE` =
`0x0801E000`（`IAPServer/owner_slot.h:32`）—— 那正是**当前正在执行的那个扇区**的尾部 8 KiB。

---

## 问题二 · STM32H743 双 bank 下的 read-while-write

> ✅ **RM0433 的规矩是「读和写必须落在不同的 bank」，这一条是明文。**
> 同 bank 会发生什么**没有明文** —— 按 §4.3.3 + §4.3.8 推出来是「被拖住（stall）」而不是报错，
> 而板子上的实证支持这个推论。**但这对擦扇区 0 没有任何帮助**，理由见本节最后一段。

出处：**RM0433 Rev 8（2023 年 1 月，3353 页）**，第 4 章 *Embedded flash memory (FLASH)*，
从第 148 页起。⚠️ **引用章节号必须带 Rev 号** —— 更早的版本里闪存是第 3 章。
ST 官方 URL：`https://www.st.com/resource/en/reference_manual/rm0433-stm32h742-stm32h743753-and-stm32h750-value-line-advanced-armbased-32bit-mcus-stmicroelectronics.pdf`

Bank 地址范围也在这份里核对过 —— **§2.3.2 *Memory map and register boundary addresses*
（Table 7，p.131）**：Bank 1 = `0x08000000`–`0x080FFFFF`，Bank 2 = `0x08100000`–`0x081FFFFF`，
和票里写的一致。

### 规矩本身 —— §4.3.7 *Overview of FLASH operations*（p.157）

> "The embedded flash memory supports read-while-write operations **provided the read and
> write operations target different banks**. Similarly read-while-read operations are supported
> when two read operations target different banks."

同一节 *Program/erase operations* 小标题下：

> "Thanks to its dual bank architecture, the embedded flash memory can perform any of the
> above write or erase operation on one bank while a read or another program/erase operation
> is executed on **the other bank**."

§4.3.11 *FLASH parallel operations (STM32H742/743/753 devices only)*（p.168）重申一次：

> "As the non-volatile memory is divided into two independent banks, the embedded flash
> memory interface can drive different operations at the same time on each bank. For example a
> read, write or erase operation can be executed on bank 1 while another read, write or erase
> operation is executed on bank 2."

§4.2 *FLASH main features*（p.148）的特性表里也列着：*"two read/program/erase operations
executed in parallel on both banks (**only available on STM32H742/743/753**)"*。

⚠️ **那个限定词是真的**：§4.2 和 §4.3.11 都写着 H742/743/753 才有。H750 单 bank 没这个能力。
我们用的是 H743，在范围内。

### 同 bank 会发生什么 —— ⚠️ 这一段是**推论**，不是 RM0433 的原话

**RM0433 没有一句话直接说「从正在被擦的那个 bank 取指会怎样」。** 它给的是两块拼图：

**§4.3.3 *FLASH architecture and integration in the system*（p.151）**：

> "The embedded flash memory is built in such a way that **only one read or write operation can
> be executed at a time on a given bank**."

**§4.3.8 *FLASH read operations*（p.158–159）**：

> "The embedded flash memory effectively executes the read operation from the read command
> queue buffer **as soon as the non-volatile memory is ready and the previously requested
> operations on this specific bank have been served**."

> "When the read command queue is full, **any new AXI read request stalls the bus read channel
> interface and consequently the master that issued that request**."

（写那边同理，§4.3.9，p.161：写队列满则 stall 写通道。）

每个 bank 一条读队列，深度 3（一条在执行、两条等待，见 §4.3.8 开头和 Figure 10）。

> ⚠️ **把这两条拼起来得到「擦 Bank 1 的同时从 Bank 1 取指 = CPU 被拖住到擦除结束」——
> 这是推论。** RM0433 闪存章节里 "stall" 只出现在上面那两处，讲的都是「队列满」。
> **RM 从没说同 bank 的读会报总线错误或返回无效数据，也没说它一定会 stall 多久。**
> 下一节的板级证据才是「确实只是 stall」的直接依据。

配套的状态位在 §4.3.9 的 *Monitoring ongoing write operations*（p.163），寄存器描述在
**§4.9.5 *FLASH status register for bank 1 (FLASH_SR1)***（p.207–209）和
**§4.9.26 *FLASH_SR2***（p.230）：**bit 2 `QW1`**（wait queue flag，「写/擦/选项字节操作还在
命令队列里」，原文 *"It supersedes the BSY1/2 status bit"*）和 **bit 0 `BSY1`**（busy flag，
「正在对存储阵列实际动手」）。所有官方擦/写序列**一律等 `QW` 清零，不等 `BSY`**；
HAL 轮询的也是 `QW`，见 `Drivers/STM32H7xx_HAL_Driver/Src/stm32h7xx_hal_flash.c` 的
`FLASH_WaitForLastOperation()`。

⛔ **但 RM0433 没有把 `QW`/`BSY` 和「读被 stall」关联起来** —— 这两个位的描述里一个字都没提
stall。「`QW=1` 时读同 bank 会 stall」**不是 RM0433 的说法**。

### 板子上已经在这么干了 —— 票里那句猜测只对一半

现有代码**每次升级 app 都在擦 Bank 1 的 7 个扇区，同时从 Bank 1 扇区 0 取指**（见问题一）。
而且那段擦除：

- **不关中断** —— `Flash_If_Erase()`（`Core/Src/usbd_cdc_flash.c:37-70`）里没有 `__disable_irq()`，
  SysTick 和以太网中断全程开着，中断向量和处理函数都在 Bank 1
- **把 I-cache 关掉了** —— 第 46 行 `SCB_DisableICache()`，所以**每一条指令都真的去打那个正忙的 bank**

这三条用例都在**真板子**上过了（全部 ✅），证据就是它：

| 用例 | 测什么 | 台子 | 出处 |
|---|---|---|---|
| **T1-23**（一次真实上传走完，且擦除在验证之后） | 走完整个 `Erasing application region` → 写回 | 真板子 | [M1-firmware-upgrade.md:359](../../docs/modules/M1-firmware-upgrade.md) |
| **T1-22**（掉电落在擦写窗口） | 擦写窗口真的存在且有约 20 秒宽 | **真板子 + 人工断电** | [M1-firmware-upgrade.md:358](../../docs/modules/M1-firmware-upgrade.md) |
| **T1-28**（journal 扇区满了能 reclaim 并恢复） | 擦 Bank 2 扇区 7（跨 bank 那条） | 真板子 + ST-Link | [M1-firmware-upgrade.md:364](../../docs/modules/M1-firmware-upgrade.md) |

⚠️ **这三条测的都是「擦别的扇区」，没有一条测过「擦自己所在的扇区」。** 原地升级要做的事，
今天没有任何一条用例覆盖。

> ✅ **票里「journal 扇区在 Bank 2 …… 所以现有代码很可能根本没碰到这个问题」——
> 核实结果是一半对**：journal 那条确实跨 bank，但升级 app 那条同 bank 已经跑了几十次。
> 同 bank 能跑通，正是因为 RM0433 定的是 stall 不是 fault。

### 但这一切对擦扇区 0 都不管用

RWW 在这里**不是决定性的那条**。就算同 bank 的读只是被拖住：

1. 擦除结束那一刻，扇区 0 的内容是全 `0xFF`；
2. CPU 解除 stall 之后去取下一条指令，取到的是 `0xFF`；
3. **没有任何一条 read-while-write 规则能把已经擦掉的指令变回来。**

所以「能不能同 bank 取指」这个问题，对**擦扇区 1–7**有意义（答案：能，靠 stall），
对**擦扇区 0** 没有意义 —— 唯一的出路是执行代码根本不在 flash 里。

### RM0433 没有说的

**RM0433 里找不到「擦自己所在的 bank 要把代码搬进 RAM」这句话。** 全文搜 `from RAM` / `SRAM`
在第 4 章里没有任何「擦写代码须在 RAM 中运行」的要求或建议。能找到的 ST 表述**都不是 RM0433**：

| 出处 | 性质 | 说了什么 |
|---|---|---|
| [ST 社区帖 *STM32H7: no execution from flash while erasing or programming*](https://community.st.com/t5/stm32-mcus-products/stm32h7-no-execution-from-flash-while-erasing-or-programming/td-p/663288) | **ST 官方版主**（Technical Moderator）答复，**不是文档** | 建议闪存操作期间把**向量表和代码都搬到 RAM** |
| ES0392（H742/743/750/753 勘误表） | ST 官方勘误 | ⛔ **没查** —— 这台机器直连 st.com 被挡 |
| AN4808 | ST 应用笔记 | ⛔ **没查** |

**RM0433 也完全没有提 `VTOR`**（全文 0 次命中）。相关的三处它都只说了一半：

- **§2.4 *Embedded SRAM*（p.136）** 和 **§2.3.2 Table 7（p.131）**：`0x00000000` 是 **ITCM**，
  64 KB。**表里没有「启动区别名到 `0x00000000`」这种条目。**
- **§2.6 *Boot configuration*（p.137–138）**：只讲从哪取第一条指令
  （*"the selection of the boot area is done **before releasing the processor reset**"*），
  **没把这一步和 `VTOR` 的复位值联系起来**。
- **§19.1 NVIC（p.749）**：把向量表和异常的编程细节推给 **PM0253**（Cortex-M7 编程手册）。

⚠️ **所以「本工程不写 `SCB->VTOR` 的情况下，中断向量表实际落在哪」这条没验证，
而且 RM0433 根本回答不了它 —— 要坐实得去查 PM0253 里 `VTOR` 的复位值，这次没查。**
它不影响结论 —— 见问题三的 R4（全程关中断），关了中断就不依赖向量表在哪。

---

## 问题三 · 要不要把擦写那段搬进 RAM，搬的话改什么

> ✅ **要搬，而且只有原地升级这条路要搬 —— 现有的两条擦除路径一行都不用动。**

### 为什么现有代码不用动

| 现有路径 | 擦谁 | 执行代码在哪 | 要不要搬 |
|---|---|---|---|
| `journal_reclaim()`（`bootloader_state.c:312`） | Bank 2 扇区 7 | Bank 1 扇区 0 | ❌ 不用，**跨 bank** |
| `Erase_FLASH()` 升级 app（`IAP_server.c:95`） | Bank 1 扇区 1–7 + Bank 2 | Bank 1 扇区 0 | ❌ 不用，**同 bank 但不是同扇区**，扇区 0 的指令一直在 |
| **新增**：原地升级擦扇区 0 | **Bank 1 扇区 0** | **就是扇区 0 自己** | ✅ **必须搬** |

### 要改什么 —— 四处，其中两处已经有了

| # | 改哪 | 改什么 | 状态 |
|---|---|---|---|
| 1 | `STM32H743IIKX_FLASH.ld` | `.RamFunc` 段收进 `.data`，`.data` 的 VMA 在 `RAM_D1`、LMA 在 FLASH | ✅ **已经是这样**，第 166-167 行和第 171 行（`} >RAM_D1 AT> FLASH`）。⚠️ 工装脚本 `STM32H743IIKX_FLASH_PORTTOOL.ld:172-173` 同款，两份要保持一致 |
| 2 | `startup_stm32h743xx.s` | 启动时把 `.data`（含 `.RamFunc`）从 LMA 拷到 VMA | ✅ **已经是这样**，第 66-81 行的 `CopyDataInit` 循环 |
| 3 | **新文件**（放 `IAPServer/`，不要动 `Drivers/`） | 一个 `__RAM_FUNC` 的自包含擦写例程 | ⬜ 要写，约束见下 |
| 4 | 调用点 | 进例程前 `__disable_irq()`，例程末尾直接 `NVIC_SystemReset()`，**不返回 flash** | ⬜ 要写 |

第 3 项之所以是「自己写」而不是「给 HAL 函数加 `__RAM_FUNC`」：
`$BOOT/CLAUDE.md` 第 28 行写着 `Drivers/` 是「CubeMX 拉进来的，不动」，
而整条 HAL 调用链有五个函数在 flash（见问题一的表）。**挨个标注等于把 CubeMX 生成区改花。**

### 那个 RAM 例程必须守的六条

| # | 约束 | 为什么 |
|---|---|---|
| R1 | **不调 HAL**，直接写 `FLASH->KEYR1/CR1/SR1` | `HAL_FLASHEx_Erase`（`0x08002cc4`）、`FLASH_Erase_Sector`（`0x08002c7c`）、`HAL_FLASH_Program`（`0x08002b4c`）、`FLASH_WaitForLastOperation`（`0x08002a8c`）全在扇区 0 里。寄存器序列很短，可照抄 `stm32h7xx_hal_flash_ex.c` 的 `FLASH_Erase_Sector()`（CR1 清 `SNB`，置 `SER \| SNB \| START`）和 `stm32h7xx_hal_flash.c:154` 的 `HAL_FLASH_Program()`（置 `CR1.PG`，`ISB`/`DSB`，连写 8 个 32-bit 字，`ISB`/`DSB`，等 `QW1` 落下） |
| R2 | **不调 `HAL_GetTick()`** | 它在 `0x080019b0`，而且它依赖 SysTick 中断 —— 中断关掉之后 `uwTick` 根本不走，超时判据会永远不成立。超时改用固定次数的软件计数或 DWT 周期计数器 |
| R3 | **不 `printf`，不碰任何 `const` / 字符串字面量** | `.rodata` 在 flash（map 里 `.rodata` 起 `0x08014aa0`）。GCC 会把函数自己的 literal pool 跟着 `.RamFunc` 一起搬，**但 `.rodata` 里的数组和字符串不会跟着走** |
| R4 | **全程 `__disable_irq()`** | 见下面「中断向量表」一段 |
| R5 | **源数据从 SDRAM（`0xC0000000`）读，不从 flash 读** | `IAP_STAGE_BASE`，`Core/Inc/IAP_config.h:35`。这本来就是既定设计（A12） |
| R6 | **写完不回 flash，直接软复位** | 回去也得先 invalidate I-cache，而且新旧镜像的函数地址不保证一致。复位最干净，并且和 [OWN-04（升级被打断怎么让人知道）](issues/OWN-04-how-does-an-interrupted-upgrade-announce-itself.md) 的「重启后自己报」对得上 |

### 落点为什么是 `RAM_D1`（`0x24000000`）而不是 SDRAM

| 区 | 地址 | 能不能取指 | 出处 |
|---|---|---|---|
| `RAM_D1`（AXI SRAM） | `0x24000000`，512 KiB | ✅ 能 | MPU 没覆盖它：`Core/Src/main.c:519-529` 的 region 0 是 4 GB、`SubRegionDisable = 0xC7`（二进制 `1100_0111`），**子区 1（`0x20000000`–`0x3FFFFFFF`）被关掉**，落回 ARMv7-M 默认内存映射的 SRAM 区，不是 XN |
| SDRAM | `0xC0000000` | ❌ 不能 | 同一条 SRD 关掉了子区 6（`0xC0000000`–`0xDFFFFFFF`），落回默认映射的 External device 区，**默认就是 XN** |

⚠️ **上面这两行是按 ARMv7-M 的默认内存映射推出来的，不是实测。** MPU 配置的数值是照抄
`Core/Src/main.c:519`、`:523`、`:524` 的，`0xC7` 的位含义是标准 MPU 语义。**没有在板子上验过。**

空间够：map 里 `.data` 只占 `0x180`、`.bss` 占 `0xC000`（48 KiB），堆栈另加 12 KiB，
`RAM_D1` 的 512 KiB 还剩约 450 KiB。一个寄存器级擦写例程量级在 1–2 KiB。

### 中断向量表这条要特别小心

`SCB->VTOR` **在这个 bootloader 里从来没被写过**：`Core/Src/system_stm32h7xx.c:88` 的
`USER_VECT_TAB_ADDRESS` 是注释掉的，所以 `:297` 那行 `SCB->VTOR = ...` 整段被 `#if` 排除。
唯一写 VTOR 的地方是跳去 app 之前的 `IAPServer/IAP_server.c:672`。

也就是说，**擦扇区 0 的时候，中断向量表要么在扇区 0 里、要么指向一个更早就被别名过去的副本** ——
两种情况下，擦完之后任何一个中断进来都会取到空 flash。
**所以 R4（全程关中断）不是保险，是必需。**

现成的关中断范式在 `IAPServer/IAP_server.c:647-660`（跳 app 之前）：
`__disable_irq()` → 停 SysTick → `NVIC->ICER[0..7]` / `ICPR[0..7]` 全清。

---

## 顺带看到的两条，不属于本票

都在 `Flash_If_Write()`（`Core/Src/usbd_cdc_flash.c:90`）里，**只是记下来，没有改，也没有开票**：

1. **写后校验只比了 8 字节**：第 100 行 `*(uint64_t *)(DataAddress + i) != *(uint64_t *)(FlashAddress + i)`，
   而一次写的是 32 字节。后 24 字节写错了不会被发现。
2. **两条错误返回路径漏了收尾**：第 102 行 `return 2;` 和第 108 行 `return HAL_ERROR;` 都没走
   `HAL_FLASH_Lock()` / `SCB_EnableICache()`，**一次失败会把 I-cache 永久留在关闭状态**。

---

## 哪几条没验证

| 没验证的 | 为什么 |
|---|---|
| **「擦 Bank 1 时从 Bank 1 取指会 stall」这句话本身** | **RM0433 没有明文**，是从 §4.3.3 + §4.3.8 推的。直接依据是板级实证（T1-22 / T1-23），不是手册 |
| **本工程的中断向量表实际落在哪**（`SCB->VTOR` 从不被写，保持复位值） | RM0433 全文不提 `VTOR`，§2.6 也没说 `BOOT_ADD0` 那块地址会被别名到 `0x00000000`，§19.1 把 `VTOR` 推给 **PM0253**（没查）。**不影响结论** —— R4 全程关中断就绕过了它 |
| **ES0392 勘误表 / AN4808** | 这台机器直连 st.com 被挡，**都没查**。如果其中有关于「擦所在 bank」的条目，我不知道 |
| `RAM_D1` 可取指、SDRAM 不可取指 | 按 MPU 配置（`Core/Src/main.c:519-529`）+ ARMv7-M 默认内存映射推的，**没在板子上跑过一段 RAM 里的代码** |
| 「擦自己所在的扇区」这件事本身 | **今天一条用例都没有**。T1-22 / T1-23 / T1-28 测的全是擦别的扇区 |
| 擦扇区 0 的真实耗时、整个升级窗口有多长 | 本票是纯调查，没上板 |
