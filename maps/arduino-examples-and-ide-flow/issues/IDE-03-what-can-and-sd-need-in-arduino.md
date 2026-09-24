# CAN 和 SD 卡在 Arduino 下最少要补什么

Type: research
Opened: 2026-09-24
Status: resolved
Blocked by: -

## Question

CAN（FDCAN1，PB9/PI9）和 SD 卡（SDMMC1，1 位）现在在 Arduino 里用不了。最少要补哪些东西才能各写出一个例程：打开哪个 HAL 模块、有没有能直接用的 STM32duino 上游库、还是照 `$BOOT/TestCase/` 里上板跑通的代码写一层薄封装。

## 怎么算答完

两条各给出一个推荐做法和它的代价（要改哪些文件、会不会限制用户 app 用这些外设），并引用板子上跑通过的那份测试代码。

## Answer

2026-09-25 定。选项对比、代价和代码出处见 [IDE-03-findings.md](../IDE-03-findings.md)。

- **CAN：照 `$BOOT/TestCase/common/port_can.c` 写一层薄封装**，放进 `OpenPLC_Ports`；在变体里打开 `HAL_FDCAN`。
  本机找到的三个上游库都用不了（不认这块板、不认 PI9、或者只支持 bxCAN）。
  ⚠️ 和 bootloader 那份不同：Arduino 下时钟跑在 HSI、HSE 被关掉，封装要先打开 HSE
- **SD：用上游 STM32SD + FatFs**，1 位总线。⚠️ **前提是先把变体的 SD 引脚表砍到板子真实接的那几个脚**：
  表里现在有 27 项，`SD.begin()` 会把其中每一个都切成 SDMMC，包括 CAN 发送、RS232 和日志口、RS485 接收、DIN_1、KNX 灯
- 两者都不限制用户 app：只用轮询，中断处理和 MspInit 都留成 weak

## 引出了什么新的未知

- **SD 引脚表今天就是一个隐患** —— 任何用户装上 STM32SD 调 `SD.begin()` 都会抢走上面那些脚。修法并进 [CAN 和 SD 卡：最小的库和例程](IDE-10-can-and-sd.md)。
  ⚠️ 调查推荐保留的 `PC8/PC12/PD2` 是从变体（抄件）读出来的，**改表之前要对 `$HW` 的原理图核实**，并把结论记进硬件事实文档
- **STM32SD 和 FatFs 由用户从库管理器装，还是随板卡包带** —— 等用户定

