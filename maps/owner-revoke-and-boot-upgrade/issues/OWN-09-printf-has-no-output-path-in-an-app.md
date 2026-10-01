# app 里的 printf 没有输出通道

Type: grilling
Opened: 2026-09-20
Status: resolved
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

## Answer

2026-09-20 定。**选 ① 的修正版：`DEBUG_UART` 绑 `USART3`，不是 `UART4`。**

两行加在 `core:variants/STM32H7xx/H743/variant_PLC_H743.h`：

```c
#define DEBUG_UART            USART3
#define DEBUG_PINNAME_TX      PC_10_ALT1
```

**为什么不是 `UART4`**：RS232 端子（PC10/PC11）和扩展口（PH13/PH14）在 `PeripheralPins.c` 里
都是 UART4，而一个外设只有一个句柄槽位 —— 把 `printf` 放 UART4 就等于和扩展口抢。
`PC10/PC11` 上另有 AF7 = USART3，线一根不用动，那正是 `Serial_Test` 今天用的一组
（2026-09-20 实测 18 行，所以这条路径已经证明是通的）。

**为什么 `DEBUG_PINNAME_TX` 不能省**：不写它，core 会取 `PinMap_UART_TX` 里第一个 USART3 TX，
那是 **PB10 —— 本板的 RS232 使能脚**，`printf` 会把使能脚重配成串口输出。

**bootloader 不受影响**：它有自己的 `_write`，`printf` 一直走 UART4/PC10。

固定住的办法：用例 `P4`（变体断言）新增 sketch `$CORE_REPO/tests/variant_check/uart_routing/`，
对两条通道各断一次，改错编译就不过。路由表记在
[HARDWARE-FACTS.md](../../../docs/hardware/HARDWARE-FACTS.md) 的「UART4 与 USART3」一节。

## 引出了什么新的未知

**一条：`printf` 和 `Serial_Test` 现在共用 USART3 的同一个句柄，谁先 `begin()` 决定波特率。**

`uart_debug_write()` 找得到已有句柄就直接用，找不到才自己 `uart_debug_init()` ——
后者是 **9600、半双工**。所以 app 里 `printf` 出现在 `Serial_Test.begin(115200)` 之前的话，
USART3 会先被配成 9600 半双工，之后 `Serial_Test.begin()` 再把它重配回来。
`core:cores/arduino/main.cpp` 今天在启动早期就 `begin(115200)`，所以正常顺序下不成问题，
**但这条没有在板子上验证过** —— 本票的改动全部只做到编译期。

⚠️ **`PB10` 仍然要 sketch 自己拉高**，这条改动不碰它（见 HARDWARE-FACTS「默认是关的」）。


## 2026-09-21 复测：真板子 30 秒窗口，两个通道各 30 行

`COM5` 收到 2550 字节：`Serial_Test` 的 `alive` **30 行**，`printf` 的
`alive via printf` **30 行**，一比一。基线是 printf 0 行 / `Serial_Test` 18 行。

⚠️ **这证明的是 `DEBUG_UART` 改对了**（printf 从 `PH13` 挪到了 RS232 的 `PC10`）。
**收发器仍然要 app 自己开** —— 探针里那句 `digitalWrite(RS232_EN_Pin, HIGH)` 不能省，
客户的 app 不写它照样什么都看不到。
