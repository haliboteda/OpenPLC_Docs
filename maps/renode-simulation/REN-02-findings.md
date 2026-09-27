# 13 个例程在 Renode 里判得了哪些（调研记录）

2026-09-27，读代码和 Renode 1.17.0 的平台文件得出，**Renode 一次都没对这些例程跑过**（`DO_Outputs` 除外，见 [REN-01](issues/REN-01-can-renode-boot-through-the-bootloader.md)）。
`REPL` = `D:\Soft\renode\platforms\cpus\stm32h7.repl`；`boards\nucleo_h753zi.repl`、`tests\platforms\nucleo_h753zi.robot` 在 Renode 安装目录下。

判定：**能** = 用到的外设都有模型，不看 `Serial` 文字也能判；**部分** = 要先把 `Serial` 引出来，或者缺对端；**不能** = 有外设没有模型。

| 例程 | 用到的外设 | Renode 模型 | 怎么判 | 判定 | 判不了时的替代方案 |
|---|---|---|---|---|---|
| `DO_Outputs` | GPIO 输出 ×8 | GPIO（REPL 116–184） | 同一时刻只有一个为高，按 1→8 轮，约 1 s | **能**（已实测） | — |
| `Relays` | GPIO 输出 ×6 | GPIO | 同上，高 1 s、低 200 ms | 能 | — |
| `SystemLED` | GPIO PE2 | GPIO | 挂 `Miscellaneous.LED`，判闪烁（nucleo_h753zi.robot:147–152 有同样写法） | 能 | — |
| `RS232_Echo` | USART3 | `usart3 @ 0x40004800`（REPL:376） | 往 usart3 写一个字节，等它原样回来 | 能 | — |
| `RS485_Echo` | USART2 + 方向脚 PD4 | `usart2 @ 0x40004400`（REPL:383） | 写一行等它回来；发送期间 PD4 为高 | 能 | `flush()` 等的 TC 标志模型会不会置，没核实 |
| `SD_ReadWrite` | SDMMC1 1 线 | `sdmmc @ 0x52007000`（REPL:725）+ `SdCardFromFile` | 挂一个 FAT32 镜像，跑完检查 `TEST.TXT` 的内容 | 能（有未核实项） | HAL 轮询 + 1 线在这个模型上能否走通没核实（官方用例是 Zephyr 驱动）；走不通就上真板 |
| `DI_Inputs` | GPIO 输入 ×8 | GPIO，`OnGPIO` 可驱动输入 | 驱动输入脚，结果只在 `Serial` 上 | 部分 | 读全局变量 `last`；或把 `Serial` 引出来 |
| `AI_Inputs` | ADC3 / ADC1 + VREFBUF | ADC 有；**VREF 只是 Tag**（REPL:777） | `SetVoltage` 给电压，结果只在 `Serial` 上 | 部分 | 引出 `Serial`；repl 的 `referenceVoltage` 3.3 改 2.5（固件按 2500 mV 算） |
| `BoardTemperature` | ADC1 通道 15 / 16 | 同上 | 同上 | 部分 | 同上 |
| `CAN_Counter` | FDCAN1 | `fdcan1: CAN.MCAN`（REPL:462） | 接 `CANHub`，看发出的 ID 0x123 和计数 | 部分 | Windows 上没有 SocketCAN 桥，对端要用 Python 往 hub 注帧；HAL 的 FDCAN 初始化能否走通没核实 |
| `Ethernet_IP` | ETH + LAN8742 PHY | MAC 有（REPL:566），**PHY 没接**；`nucleo_h753zi.repl:19–29` 有一个 ID 正是 LAN8742A 的 PHY | 接 `Switch`，抓 DHCP 请求；拿到地址后 USART3 打 `[NET] ip=` | 部分 | Renode 没有内置 DHCP 服务：再起一台跑 DHCP 的模拟机，或经 TAP 接主机（本机有没有 TAP 驱动没核实） |
| `USB_Serial` | USB OTG FS | `usb2 @ 0x40080000`（REPL:769）+ `USB.USB_UART` | nucleo_h753zi.robot:481–489 的 CDC 用法 | 部分 | 那个用例跑的是 Zephyr 的协议栈，STM32 USB 协议栈能否枚举没核实 |
| `AO_Outputs` | DAC1 ×2 | **只有 Tag**（REPL:806），Renode 里没有 STM32 DAC 模型 | — | **不能** | 在 `0x40007400` 放一个 `Python.PythonPeripheral` 桩，记录 DHR12R1/R2 的写入值，期望码 0 / 838 / 1677 / 2515 / 3354；电流准不准只能上真板 |

## 几个例程共有的缺口

| 缺口 | 影响 | 办法 |
|---|---|---|
| `Serial` 走 USB CDC，看不到文字 | 8 个「部分」 | ① `USB.USB_UART` 接 usb2（没核实）；② IDE 的 USB 菜单选 "CDC (no generic 'Serial')"，`Serial` 就变成 UART4（`boards.txt:82-83`、`WSerial.h:77-81`），要专门编一版 |
| 平台没有 PHY | 每个例程启动都会初始化网络（`main.cpp:181-198`） | 照 `nucleo_h753zi.repl:19-29` 补一个 LAN8742 |
| VREF、DAC1 只是 Tag | AI、温度、AO | 写 Python 桩 |
| 没有 DHCP 对端、没有 Windows 上的 CAN 桥 | 以太网、CAN | 第二台模拟机，或 Python 注帧 |
