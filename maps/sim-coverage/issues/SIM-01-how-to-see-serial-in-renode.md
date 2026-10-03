# 例程的 `Serial` 在 Renode 里怎么看得到

Type: research
Opened: 2026-10-03
Status: resolved
Blocked by: -

## Question

8 个例程的结果只打在 `Serial`（USB CDC）上（[REN-02-findings.md](../../renode-simulation/REN-02-findings.md)「几个例程共有的缺口」）。两条路：Renode 的 `USB.USB_UART` 接 `usb2`，看 STM32 的 USB 协议栈能不能枚举；或者编译时 USB 菜单选「CDC (no generic 'Serial')」，`Serial` 落到 UART4，在 Renode 里接 UART4。哪条能走通、对例程有没有改动、和真板上跑的二进制差在哪。顺带回答：USB 上传（IAPTool `cdc`）能不能在 Renode 里走。

## 怎么算答完

- 在 Renode 里跑一个例程，PC 侧拿到它 `Serial` 打的头一行
- 写明选的那条路和真板二进制的差别
- USB 上传能不能走，给出结论和依据

## Answer

2026-10-03：编译时 USB 菜单选「CDC (no generic 'Serial')」（`usb=CDC`），`Serial` 落到 UART4，Renode 里直接读；例程源码不改（`DI_Inputs` 经真 bootloader 实测）。Renode 的 `USB_UART` 和 ST 的 USB 协议栈枚举不通；**USB 上传归「只能上板」**，模拟里的上传走网口。见 [SIM-01-findings.md](../SIM-01-findings.md)。

## 引出了什么新的未知

- 当前 bootloader 在原样平台上等 `PWR_CR2.BRRDY` 卡住；平台补 `pwr` 读回就绪后 app 6.6 s 起来 —— 由「bootloader 开机把输出置 0，在 Renode 里判」那张票一并补进共用平台
- Renode 里 DI 默认全读 0，真板不接 24 V 时全读 1：判 DI 的用例要自己驱动输入脚
