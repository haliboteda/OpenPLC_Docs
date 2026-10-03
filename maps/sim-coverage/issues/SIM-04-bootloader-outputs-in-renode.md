# bootloader 开机把输出置 0，在 Renode 里判

Type: task
Opened: 2026-10-03
Status: resolved
Blocked by: -

## Question

决策 81 和 PB14：从 bootloader 第一批语句到 sketch 第一次写之前，DO1–DO8、AO 的 PA4 / PA5、KNX_TX（PB14）都是推挽输出、电平为低；交权前 `HAL_DeInit()` 之后又置一次。主机用例 `T1-36` 只测了 `safe_outputs_init()` 本身（假寄存器）。在 Renode 里用真 bootloader + 一个不碰这些脚的 app，复位后、跳转后各读一次 GPIO。BOR 检查（读 `FLASH->OPTSR_CUR`）在 Renode 里有没有模型，有就一起判。

## 怎么算答完

- 一条进 `$TEST` 的用例：Renode 里复位后到 app 运行，这 11 个脚始终是低电平输出
- BOR 检查能判就判，不能就写明原因

## Answer

2026-10-04 定。用例 `T1-37`（`$TEST/host/renode/boot_outputs.py`，判据和测不到什么见 [M1 固件升级](../../../docs/modules/M1-firmware-upgrade.md)「测试怎么跑」）：当前 `$BOOT` 工作区编出的 bootloader 跳进 `SystemLED`，11 个脚在五个时刻都是推挽输出、`ODR` 为 0，通过；进 `$TEST` 的 selfcheck，`--quick` 跳过。

- **BOR 能判**：Renode 1.17 的 `STM32H7_FlashController` 建了 `OPTSR_CUR`（复位值 `0x0406AAF0`，`BOR_LEV` = 0）和选项字节编程序列。`BOR_LEV` 为 0 时串口有警告，编程成 3 后没有，两种都过
- **用例真能抓错**：拿 `$BOOT/Debug/` 里 PB14 那次提交之前编的镜像跑，五个时刻都只报 PB14 不是输出
- **平台补了一处**：Renode 的 `pwr` 桩不置 `PWR_CR2.BRRDY`，bootloader 每次启动多等约 1 s。补在 `$TEST/host/renode/plc_h743.repl`，`T3-05` 也改用它，见 [REN-02-findings.md](../../renode-simulation/REN-02-findings.md)

## 引出了什么新的未知

没有。
