# sketch 的 `Serial` 和 core 自己的日志走哪

Type: grilling
Opened: 2026-10-17
Status: resolved
Blocked by: USB-01

## Question

Arduino 用户习惯 `Serial` 就是 USB 串口；现在例程按决策 100 用 `RS232` 对象打印。要定：`Serial` 指向 USB CDC、`RS232` 对象只给用户程序接设备；core 的 `[BOOT]` `[NET]` 去哪；USB 没人读时打印会不会拖慢 sketch（决策 124 的 20 ms 发送超时）；core 还要不要在开机时把 `RS232_EN` 拉高。

讨论中已定（用户 2026-10-17 按推荐）：

| 事 | 定了什么 |
|---|---|
| RS232 芯片 | `RS232.begin()` 先配串口引脚、再拉高 `RS232_EN`；`RS232.end()` 拉低；core 开机不再碰它 |
| 系统日志前缀 | `[sys]` 加原来的标签，如 `[sys][NET] ip=…` |
| 关掉系统日志 | sketch 里一行宏 `OPENPLC_SYSTEM_LOG(OFF);`（同 `OPENPLC_APP_VERSION` 的做法）；关了缓存照记、IAPTool 照读，只是不往口 1 吐 |
| 口 1 没打开时 | 系统日志只写缓存，口 1 打开（DTR 置位）后一次吐出，之后直接写；用户自己的 `Serial.print` 照 STM32duino 原行为 |
| `Serial` 的名字 | 不改：Arduino 惯例里 `Serial` 就是 USB 串口；`SerialUSB` 是同一个对象（`$CORE_REPO` `cores/arduino/WSerial.h:13`），例程和 README 统一写 `Serial`，首次出现注明「即 USB 口 1，也可写 `SerialUSB`」，端口对照表写清 `Serial` / `RS232` / `RS485` 各是哪个口（用户 2026-10-17） |
| 例程 | 打印一律改回 `Serial`；`RS232_Echo`、`RS485_Echo` 端子照旧收发数据，提示和结果打到 `Serial` |

## 怎么算答完

`Serial`、`RS232`、core 日志各自的去向和开机时 `RS232_EN` 的状态定下并写进 M3；例程改法能据此写出。

## Answer

2026-10-17 定，逐条见上面「讨论中已定」那张表；要求写成 [M3](../../../docs/modules/M3-app-runtime.md) `R3-23`（日志去向在 `R3-22`）。

## 引出了什么新的未知

- `R3-05`（core 的诊断串口不会被用户 sketch 掐掉）和 `T3-03` 的前提是 core 占着 RS232，改完后要改写成「用户的 `RS232` 不会被别的 UART 抢」
- `OPENPLC_SYSTEM_LOG` 宏怎么在编译前读出（照 `OPENPLC_APP_VERSION` / `OPENPLC_KNX_ROLE` 的 prebuild 做法）
