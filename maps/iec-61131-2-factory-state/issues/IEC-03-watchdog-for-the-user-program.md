# 用户程序卡死时谁发现、输出怎么办

Type: grilling
Opened: 2026-09-28
Status: open
Blocked by: IEC-02

## Question

标准 2003 5.8 要求有监视用户程序的手段（看门狗）。要定：app 这边开不开 IWDG、由谁喂（core 在两次 `loop()` 之间喂，还是交给 sketch）、超时之后是复位还是先把输出置到规定状态、和 bootloader 交权时的看门狗状态怎么衔接（`$BOOT/IAPServer/IAP_boot_handoff.c`）。

## 怎么算答完

定下开不开、谁喂、超时行为；一个故意卡死的 sketch 在真板子上被发现，输出落到规定状态。
