# app 里的 printf 没有输出通道

Type: grilling
Opened: 2026-09-20
Status: open
Blocked by: -

## Question

**`libraries/OpenPLC_IAP/` 里所有 `printf` 诊断，在 app 跑起来之后一行都出不来。**
不是被 RS232 收发器挡住，是**根本没有输出路径**。

2026-09-20 实测对照，同一个函数、同一时刻、同一个串口：

| 写法 | 收到的行数 |
|---|---|
| `printf("...")` | **0** |
| `Serial_Test.println("...")` | **18** |

前置都已排除：`PB10`（RS232_EN）实测为高（`GPIOB_ODR = 0x00000400`），
stdout 也已 `setvbuf(..., _IONBF, 0)`。

**根因**：`printf` → `_write()` → `uart_debug_write()` → `DEBUG_UART`，
而 `DEBUG_UART` 在没有显式定义时解析自 `PIN_SERIAL_TX`
（`libraries/SrcWrapper/src/stm32/uart.c:25-27`）。本板的
`variant_PLC_H743.h:470` 把 `PIN_SERIAL_TX` 定成 **`PH13`**（UART4 在 JunctionLink 扩展口那一组），
而 RS232 控制台走的是 **`PC10`/`PC11`**（`Serial_Test` 用的那一组）。

### 为什么要紧

这些话**客户也看不到**，它们恰恰是出问题时最需要的那几句：

- `Rejected unauthenticated openplc_server_reboot request`
- `Reboot request ignored: still within cooldown`

⚠️ 它还**挡住了另一张票的诊断**：[有些叶证书驱动不了重启握手](OWN-08-some-leaf-certs-cannot-drive-the-reboot-handshake.md)
要区分「验证失败」「冷却期内」「`sscanf` 解析失败」三种结局，唯一的区别就在这几行 `printf` 上。

### 候选

| | 做法 | 代价 | 取舍 |
|---|---|---|---|
| ① | variant 里显式 `#define DEBUG_UART UART4` | 一行 | `printf` 和 `Serial_Test` 共用一个外设句柄，**谁后 `begin()` 谁赢**（`$PROD/docs/hardware/HARDWARE-FACTS.md` 已记这条），要确认不会互相踩 |
| ② | 把 `PIN_SERIAL_TX`/`RX` 改成 `PC10`/`PC11` | 一行 | 改的是**默认 `Serial` 的含义**，会影响所有用 `Serial1` 之类的客户 sketch |
| ③ | 库里那几处 `printf` 改成走 `Serial_Test` | 动 core 库多处 | 不碰 variant，但 C 文件要拿到 C++ 的 `HardwareSerial` |

## 怎么算答完

1. 选定一条，让 `udp_server.c` 的两句拒绝日志在真板子上**看得见**
2. 说清它对 **bootloader 侧**有没有影响（bootloader 有自己的 `_write`，`printf` 一直是通的 —— 不要把两边搞混）
3. 如果选 ① 或 ②，`变体断言`（用例 `P4`）要跟着加一条，防止它再漂回去
