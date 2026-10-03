# bootloader 开机把输出置 0，在 Renode 里判

Type: task
Opened: 2026-10-03
Status: open
Blocked by: -

## Question

决策 81 和 PB14：从 bootloader 第一批语句到 sketch 第一次写之前，DO1–DO8、AO 的 PA4 / PA5、KNX_TX（PB14）都是推挽输出、电平为低；交权前 `HAL_DeInit()` 之后又置一次。主机用例 `T1-36` 只测了 `safe_outputs_init()` 本身（假寄存器）。在 Renode 里用真 bootloader + 一个不碰这些脚的 app，复位后、跳转后各读一次 GPIO。BOR 检查（读 `FLASH->OPTSR_CUR`）在 Renode 里有没有模型，有就一起判。

## 怎么算答完

- 一条进 `$TEST` 的用例：Renode 里复位后到 app 运行，这 11 个脚始终是低电平输出
- BOR 检查能判就判，不能就写明原因
