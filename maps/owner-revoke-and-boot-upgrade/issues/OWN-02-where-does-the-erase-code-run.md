# 擦扇区 0 的时候，那段代码从哪执行

Type: research
Opened: 2026-09-19
Status: resolved
Blocked by: -

## Question

原地升级要擦**整个扇区 0**（128 KiB），而 bootloader 自己就住在那儿。这条路能不能走通，取决于三个还没核实的事实：

1. **现有的 flash 写入和擦除代码跑在哪** —— `Flash_If_Write()` 和 `journal_reclaim()`（唯一会擦扇区的地方）是从 flash 取指还是从 RAM？`IAPServer/` 下没有任何 `.RamFunc` / `__attribute__((section(".RamFunc")))` 的痕迹，**但 journal 扇区在 `0x081E0000`，属于 Bank 2，而 bootloader 在 Bank 1** —— 所以今天可能根本没碰到这个问题
2. **STM32H743 双 bank 下的 read-while-write**：擦 Bank 1 的扇区时，能不能继续从 Bank 1 取指执行？（`0x08000000`–`0x080FFFFF` 是 Bank 1）
3. **要不要把擦写那段搬进 RAM**，以及搬的话链接脚本和启动代码要改什么

⚠️ 项目文档和代码里**都没有记载**第 2 条。出处只能是 **RM0433**（STM32H743 参考手册）的 embedded flash memory 一章，或者在板子上实测。

## 怎么算答完

三个问题各自写下答案和**出处**（RM0433 的章节号 / 代码的 `文件:行号` / 实测的步骤和结果），并给出一句结论：

> **「擦扇区 0 这段代码必须放在 ___」**

以及：如果结论是「必须放 RAM」，写明要改哪几处（链接脚本的段、启动代码的拷贝、哪些函数要标）。

## Answer

2026-09-20 定。**全部依据在 [OWN-02-findings.md](../OWN-02-findings.md)**，这里只放结论。

> **擦扇区 0 这段代码必须放在 RAM（`RAM_D1`，`0x24000000`）里跑，而且整段窗口要关中断。**

### 1 · 现有擦写代码全部从 flash 取指，而且就住在要被擦的那个扇区里

`$BOOT` 里**一行 RAM 驻留代码都没有** —— `__RAM_FUNC` 宏有定义，但 `IAPServer/` `Core/` `LWIP/`
`USB_DEVICE/` 和 HAL 的 `Src/` 里出现 0 次。`Debug/open_plc_cube_ide.map` 坐实：
`Flash_If_Erase` `0x08001590`、`Flash_If_Write` `0x0800164c`、`Erase_FLASH` `0x080016f0`，
整条 HAL 链在 `0x080019b0`–`0x08002cc4` —— **全在 Bank 1 扇区 0**。

### 2 · 开票时那句猜测只对一半

⚠️ 票里写着「journal 扇区在 Bank 2 而 bootloader 在 Bank 1，所以现有代码很可能根本没碰到这个问题」。
**`journal_reclaim()` 确实擦 Bank 2，但升级 app 那条每次都擦 Bank 1 的扇区 1–7**
（`IAP_server.c:95` → `Erase_FLASH(0x08020000, …)`），而 bootloader 正从 Bank 1 扇区 0 取指。

**「擦 Bank 1 的同时从 Bank 1 取指」这个产品每升级一次固件就干一次**，而且 `Flash_If_Erase()`
全程不关中断、还把 I-cache 关掉 —— 每条指令都真的去打那个正忙的 bank。

### 3 · RM0433 怎么说：跨 bank 才叫 RWW。**同 bank 会怎样，手册没有直说**

**RM0433 Rev 8 第 4 章 Embedded flash memory**（⚠️ **引章节号必须带 Rev 号** —— 更早的版本里
闪存是第 3 章）：

- **§4.3.7（p.157）** — RWW *"provided the read and write operations target different banks"*
- **§4.3.3（p.151）** — *"only one read or write operation can be executed at a time on a given bank"*
- **§4.3.8（p.158）** — 读请求进队列，队列满了 *"any new AXI read request **stalls** the bus
  read channel interface"*
- **§4.2（p.148）** — 双 bank 并行 *"only available on STM32H742/743/753"*。我们这颗 H743 在范围内

⚠️ **「从正在被擦的 bank 取指会被拖住而不是出错」是推论，不是 RM0433 的原话。**
手册没有任何一句直接讲这件事；上面那两条是拼出来的，而 "stall" 在整章里只出现在「队列满」的语境。
**这条的直接依据是板级实证** —— `T1-22`（掉电落在擦写窗口）和 `T1-23`（一次真实上传走完，
擦除在验证之后）都在**真板子**上通过，而那条路径每次都在擦 Bank 1、同时从 Bank 1 取指。

⚠️ RM0433 也**没有**把 `QW`/`BSY` 状态位和「读被 stall」关联起来 —— 那两个位的描述里一个字都没提。

**但这一整段对擦扇区 0 都没用**：擦完之后扇区 0 全是 `0xFF`，CPU 解除 stall 去取下一条指令，
取到的是 `0xFF`。**结论不依赖 RWW 那条规矩。**

### 4 · 链接脚本和启动代码**不用改** —— 已经有了

`.RamFunc` 段已经收在 `.data` 里（`STM32H743IIKX_FLASH.ld:166-167`，第 171 行 `} >RAM_D1 AT> FLASH`），
启动代码的 `.data` 拷贝循环已经会把它搬进 `RAM_D1`。**核实过，属实。**

⚠️ **落点必须是 `RAM_D1`（`0x24000000`），不能是 SDRAM** —— MPU 配置下 SDRAM `0xC0000000`
落回默认映射的 External device 区，**默认 XN（不可执行）**。

### 5 · 要新写的那段例程，六条硬约束

1. **不调 HAL** —— 直接写 `FLASH->KEYR1/CR1/SR1`。给 HAL 函数加 `__RAM_FUNC` 不行：`Drivers/` 不动，而整条 HAL 链有五个函数在扇区 0 里
2. **不调 `HAL_GetTick()`** —— 关了中断 `uwTick` 不走，超时判据永不成立
3. **不 `printf`、不碰 `.rodata`**
4. **全程 `__disable_irq()`**（现成范式在 `IAP_server.c:647-660`）
5. **源数据从 SDRAM 读**
6. **写完直接 `NVIC_SystemReset()`**，不返回 flash

## 引出了什么新的未知

**两条，都不属于本票，已落进 [work/TODO.md](../../../work/TODO.md)：**

`Flash_If_Write()`（`Core/Src/usbd_cdc_flash.c:90`）有两个既存缺陷，**我逐行核实过**：

1. **写后校验只比了 8 字节** —— 第 104 行比 `uint64_t`，而一次写的是 32 字节的 flash word
2. ⚠️ **两条错误返回路径（第 104、110 行）漏了 `HAL_FLASH_Lock()` 和 `SCB_EnableICache()`** ——
   成功路径（第 116-117 行）两个都调了。**一次失败会把 I-cache 永久留在关闭状态、flash 留在解锁状态**，
   直到下次复位

另有三条**没能核实的**，都写在发现文档里：

- **RM0433 引文的出处本身** —— 这台机器直连 st.com 取不到 PDF，读的是同一份文件的大学镜像
  （封面标 January 2023 / RM0433 Rev 8，章节号页码自洽）。**正式引用前拿 ST 官网那份对一次**
- **ES0392 勘误表和 AN4808 都没查** —— 同样是被网络挡住
- 还有一条：`RAM_D1` 可取指、SDRAM 不可取指是按 MPU 配置
加 ARMv7-M 默认内存映射推出来的，**没在板子上真跑过一段 RAM 里的代码**。
写那段例程时第一件事就是验它。
