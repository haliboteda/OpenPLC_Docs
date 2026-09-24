# CAN 和 SD 卡在 Arduino 下最少要补什么

Type: research
Opened: 2026-09-24
Status: open
Blocked by: -

## Question

CAN（FDCAN1，PB9/PI9）和 SD 卡（SDMMC1，1 位）现在在 Arduino 里用不了。最少要补哪些东西才能各写出一个例程：打开哪个 HAL 模块、有没有能直接用的 STM32duino 上游库、还是照 `$BOOT/TestCase/` 里上板跑通的代码写一层薄封装。

## 怎么算答完

两条各给出一个推荐做法和它的代价（要改哪些文件、会不会限制用户 app 用这些外设），并引用板子上跑通过的那份测试代码。
