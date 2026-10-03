# SD 卡在 Renode 里能不能读写

Type: research
Opened: 2026-10-03
Status: resolved
Blocked by: -

## Question

`SD_ReadWrite`、`SD_FileReceive` 用 STM32SD（SDMMC1，1 线，HAL 轮询）。Renode 有 `sdmmc` 模型和 `SdCardFromFile`，这条组合能不能走通没核实（REN-02 记的未核实项）。能的话，挂一个 FAT32 镜像，`SD_FileReceive` 经 RS232（usart3）收一个 YMODEM 文件后，镜像里的文件和发出去的一样。卡检测脚 PE6 能不能用 `OnGPIO` 驱动来模拟插拔。

## 怎么算答完

- `SD_ReadWrite` 在 Renode 里打出 `SD_ReadWrite: OK`，镜像里有 `TEST.TXT`
- `SD_FileReceive` 收一个文件后镜像里的内容逐字节相同
- 插拔能不能模拟，给出结论

## Answer

2026-10-03：**三条判据全部实测通过**：`SD_ReadWrite` 写出 `TEST.TXT`；`SD_FileReceive` 经 usart3 收 5004 字节 YMODEM 文件，镜像里逐字节相同；PE6 用 `OnGPIO` 模拟插拔，例程打出插、拔两行。要照做的四件：镜像先格式化成 FAT32 且直接读写、`PerformanceInMips 10`、发送端分段节流（Renode 串口不按波特率限速）、usart3 引成 socket。见 [SIM-03-findings.md](../SIM-03-findings.md)。

## 引出了什么新的未知

- `T3-05` 给 SD 挂的是没格式化的空镜像，所以它只测到 SD 例程能启动，没测到读写（读代码推断）
