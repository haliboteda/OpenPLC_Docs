# 例程的 `Serial` 在 Renode 里怎么看得到

Type: research
Opened: 2026-10-03
Status: open
Blocked by: -

## Question

8 个例程的结果只打在 `Serial`（USB CDC）上（[REN-02-findings.md](../../renode-simulation/REN-02-findings.md)「几个例程共有的缺口」）。两条路：Renode 的 `USB.USB_UART` 接 `usb2`，看 STM32 的 USB 协议栈能不能枚举；或者编译时 USB 菜单选「CDC (no generic 'Serial')」，`Serial` 落到 UART4，在 Renode 里接 UART4。哪条能走通、对例程有没有改动、和真板上跑的二进制差在哪。顺带回答：USB 上传（IAPTool `cdc`）能不能在 Renode 里走。

## 怎么算答完

- 在 Renode 里跑一个例程，PC 侧拿到它 `Serial` 打的头一行
- 写明选的那条路和真板二进制的差别
- USB 上传能不能走，给出结论和依据
