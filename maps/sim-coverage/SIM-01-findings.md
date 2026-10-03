# 例程的 `Serial` 在 Renode 里怎么看得到（调研记录）

回答 [SIM-01](issues/SIM-01-how-to-see-serial-in-renode.md)。2026-10-03，Renode 1.17.0，板卡包 0.1.3，bootloader 为当天 `$BOOT/Debug/open_plc_cube_ide.bin`。
实验脚本和全部输出在会话 scratch（`sim01/exp.py`），不进仓；做法与 `$TEST/host/renode/run.py`（用例 `T3-05`：每个例程经真 bootloader 启动）相同，只多了下文说的 `pwr` 补丁。

## 结论

| 问题 | 结论 | 核实了吗 |
|---|---|---|
| 走哪条路 | **USB 菜单选「CDC (no generic 'Serial')」（`usb=CDC`）**，`Serial` 落到 UART4，Renode 里 `uart4 CreateFileBackend` 就能读 | ✅ 实跑 |
| `USB.USB_UART` 接 `usb2` 那条 | **走不通**：ST 的 USB 协议栈在 Renode 的 `STM_USB` 模型上枚举卡在读配置描述符，PC 侧一个字节都收不到 | ✅ 实跑；卡住的根因没定位 |
| 例程要不要改 | **不改**，只改编译的 FQBN（`usb=CDCgen` → `usb=CDC`） | ✅ |
| USB 上传（IAPTool `cdc`）能不能在 Renode 里走 | **不能**，归「只能上板」 | 部分实跑，见下 |

## 证据

**UART4 这条通了。** `DI_Inputs` 用 `usb=CDC` 编（`--warnings all` 零警告），经真 bootloader 启动，`uart4.txt` 在 bootloader 的 `** APP Mod ...` 之后接着出现：

```
** APP Mod ...
DI_Inputs: prints DI1..DI8 on every change.
DI1..DI8: 0 0 0 0 0 0 0 0
```

UART4 的依据：`boards.txt:82-83`（`usb=CDC` 加 `-DDISABLE_GENERIC_SERIALUSB`）、`WSerial.h` 的 `SERIAL_UART_INSTANCE == 4` 分支、`variant_PLC_H743.h:464-472`（`SERIAL_UART_INSTANCE 4`）。

**USB 这条不通。** `usb=CDCgen`（与真板相同）+ `usb_uart: USB.USB_UART` 接 `usb2`：

| 现象 | 依据 |
|---|---|
| 一开机就插（`nucleo_h753zi.robot:481-489` 的写法）：什么都不发生 | `STM_USB` 只在插入那一刻置一次总线复位标志（`STM_USB.cs` 的 `USBConnection` 构造 → `HostReset`），之后 app 初始化 USB 时写 `GINTSTS` 把它清了 |
| 等 app 起来后（虚拟时间 7 s）再插：SetAddress、SetConfiguration 都过了，第二次读配置描述符（67 字节，超过 EP0 的 64 字节一包）时设备端只交出 3 字节，主机一直等，之后再无动静 | 控制台 `logLevel -1 usb2`：`taking 3`；前一次控制读的状态阶段被丢：`Out endpoint #0 - host tried to write out when endpoint is inactive` |
| `usb_uart.txt` 始终为空 | 实跑 |

`STM_USB` 只有设备模式（`STM_USB.cs`：`IUSBDevice`，置 FHMOD 时打 `Host direction unsupported`）；`USB_UART` 是一个只认 CDC 的模拟主机（`USB_UART.cs`：`class USB_UART : USBHost, IUART`）。官方用例跑通的是 Zephyr 的驱动，不是 ST 的。源码：github.com/renode/renode-infrastructure `src/Emulator/Peripherals/Peripherals/USB/`。

## 选的那条和真板二进制差在哪

| | 真板（`usb=CDCgen`） | Renode 用（`usb=CDC`） |
|---|---|---|
| `Serial` 是谁 | `SerialUSB`（`USBSerial`） | UART4 上的 `HardwareSerial`（PH13/PH14） |
| USB 协议栈 | 有 | **仍然有**：`USBD_USE_CDC` 照样定义，CDC 接口和 1200 波特「重启进 bootloader」处理照样编进去；只是 `SerialUSB` 没被引用，链接时丢掉 |
| `while (!Serial && millis() < 3000)` | 等 PC 打开端口，最多 3 s | 立即通过（硬件串口恒为真） —— 开机时序比真板早最多 3 s |
| 体积（`DI_Inputs`） | 88368 B | 87056 B |

符号差异只有 `USBSerial::*`、`SerialUSB`、`CDC_ReceiveQueue_*`/`CDC_TransmitQueue_*`、`CDC_connected`。所以这条路测得到「例程逻辑打出了什么」，**测不到 USB CDC 那一段**（枚举、DTR 等待、USB 收发），那段只能上板。

## USB 上传为什么不能在 Renode 里走

| 环节 | 情况 | 核实了吗 |
|---|---|---|
| 枚举 | 上面那个卡点；bootloader 也用 ST 的 USB 栈（`$BOOT/USB_DEVICE/`） | app 侧实跑；bootloader 侧没单独跑 |
| IAPTool 要一个真 COM 口 | `IAP_CDC.go` 按端口名打开串口，靠「以 1200 波特打开」触发重启；`USB_UART` 只把数据管道变成 Renode 的 UART，不发 SET_LINE_CODING（`USB_UART.cs` 里 `BaudRate` 只是个属性），1200 波特这一下送不到设备 | 读源码 |
| 走 USB/IP 让 Windows 看到模拟设备 | Renode 有 `USBIPServer`，能导出任何 `IUSBDevice`（含 `STM_USB`）；但 Windows 要装 USB/IP **客户端**驱动，本机装的 `usbipd-win` 是服务端（把本机 USB 共享给 WSL） | 读源码 + 看本机安装；没试 |

前两条任一条就挡住了。上传在模拟里要测，走网口那条（IAPTool `eth`），看「例程的网口在 Renode 里通不通」那张票。

## 顺带发现

| 发现 | 影响 | 办法 |
|---|---|---|
| **当天的 bootloader 在原样的 `stm32h743.repl` 上起不来**：`bkp_stash_enable()` 等 PWR_CR2 的 BRRDY，Renode 的 `pwr` 桩没回这一位（`stm32h7.repl:728-746` 只处理 0x0/0x4/0xC/0x18），每次等满 1 s 超时并刷屏警告；两次实跑 15 s 虚拟时间都没走到 `APP Mod` | `T3-05` 照现状跑大概会全挂（`run.py` 本身没跑，只跑了同样写法的副本） | 平台里覆盖 `pwr`，CR2（偏移 0x8）读回 `0x10001`；加上后 app 的 `setup()` 在约 6.6 s 进入 |
| Renode 里 DI 全读 0 | 真板不接 24 V 时全读 1，判 DI 的用例要自己驱动输入脚 | — |

## 推荐

1. 要看 `Serial` 的模拟用例，**另编一版 `usb=CDC`**，`uart4 CreateFileBackend` 读输出；判据只看例程打出的文字，USB CDC 那段在用例里写明「只能上板」。
2. `T3-05` 的平台补上 `pwr` 的 BRRDY（上表），否则当天的 bootloader 过不去。
3. `USB.USB_UART` 不追：要追就得改 Renode 的 `STM_USB` 模型（C#），这个项目不值得。
