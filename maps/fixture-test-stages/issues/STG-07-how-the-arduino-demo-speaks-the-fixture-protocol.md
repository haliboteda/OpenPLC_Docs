# Arduino demo 怎么讲工装协议

Type: grilling
Opened: 2026-10-09
Status: resolved
Blocked by: STG-03

## Question

demo 和工装固件用同一套协议（决策 93）。它放在板卡包的哪个库、哪个例程？覆盖哪些测试项？

## 怎么算答完

写清 demo 的位置和覆盖的测试项。

## Answer

2026-10-10 用户按推荐定：放在 A；ETH / USB 满速率回送在 demo 里也做。

### 放在哪

| 做法 | 代价 | 风险 | 推荐 |
|---|---|---|---|
| A · 新例程 `OpenPLC_Ports/examples/FixtureDemo`，用板卡包已有的 API（`OpenPLC_Ports`、`OpenPLC_CAN`、`openplc_analog`、`OpenPLC_SD` 等）在 sketch 里重写协议的子集 | 协议多一份实现，成为一条跨仓镜像（[GLOSSARY.md](../../../GLOSSARY.md)「跨仓镜像」），要进镜像清单并有契约测试 | 两边协议漂移；靠同一份主机测试对两边各跑一遍兜住 | ⭐ 第 6 步要测的是用户 app 走的路径（板卡包 API、校准公式），只有用板卡包 API 写才测得到 |
| B · 把 `$BOOT/TestCase/porttool/` 的 C 源码搬进板卡包 | 约 5800 行；直接碰 HAL 和裸寄存器（如 `porttool.c` 自己接管 `UART4_IRQHandler`），和 Arduino core 抢外设 | 测的是工装固件的驱动，不是用户 app 的路径 | |
| C · 新建独立库 `OpenPLC_Fixture` 放协议解析，例程只做端口调用 | 多一个库要发版 | 用户能看到并依赖一个产线专用库 | |

### 协议子集

实现完整测试要用的命令：`pt.id`、`pt.caps`、`pt.cal`、`pt.list`、`pt.start` / `pt.set` / `pt.stop`、`pt.echo`、`pt.hold`、`pt.led`、`pt.run`，应答和采样帧照 [PORTTOOL-FLOW.md](../../../docs/modules/M4/PORTTOOL-FLOW.md)「A.4」「A.5」。控制口仍是 RS232 115200 8N1：demo 用 `RS232`（USART3），物理上就是工装控制口的 C05 / C06 端子；`printf` 进系统日志走 USB 口 1（`R3-22`）（[HARDWARE-FACTS.md](../../../docs/hardware/HARDWARE-FACTS.md)「app 侧三条通道各走哪个外设」）。`pt.caps` 表头和 `pt.id` 带 `demo=<例程版本>`，面板凭它分清 demo 和工装固件。和工装固件逐条的差别见 PORTTOOL-FLOW.md「A.9」。

### 覆盖的测试项

2026-10-14 按 [决策 127](../../../docs/tables/DECISIONS.md) 改：用户级和功能测试测同样的项，demo 每一项都要跑得了。原来「RS232 不单独测（它就是控制口）」「SDRAM 不覆盖（前几步已测）」两行作废。

| 端口 | demo 怎么做 |
|---|---|
| DI、DO、继电器 | 逐路读电平、带负载输出、逐路吸合 |
| AI、AO | 读数 / 输出走带校准的 API（[CALIBRATED-ANALOG.md](../../../docs/modules/M3/CALIBRATED-ANALOG.md)）；`pt.cal` 报扇区 15 的校准值，面板照工装固件一样判 |
| 温度 | 两路读数 |
| RS485、CAN | 与上位机收发、对发 |
| ETH、USB | 链路检查（`pt.run eth.link`）/ 枚举信息（`mode=info`）；数据收发满速率回送 |
| SD | 识别卡、读写（`pt.run sd.*`，经 `OpenPLC_SD`） |
| SDRAM | 总线检查、全片扫描（`pt.run sdram.*`，经 `OpenPLC_SDRAM`） |
| RS232 | `rs232` 会话，切控制口波特率，同工装固件（决策 104） |
| KNX、复位键、LED | 不覆盖：只在研发测试 |

## 引出了什么新的未知

- **已定** · `pt.caps` 里怎么标出固件是 demo 还是工装固件：`demo=<例程版本>`（PORTTOOL-FLOW.md「A.9」）
- **已定 B**（用户 2026-10-15：「那你就按内容都自动做了把，注意只做必要的」，按推荐；不分叉 STM32duino，见决策 124）· RS485 帧的 `overrun`：板卡包的串口中断自己清掉溢出标志（core `SrcWrapper/src/stm32/uart.c` 的 `HAL_UART_ErrorCallback`），sketch 数不到，demo 的帧里没有这个字段。**已做（2026-10-15）**：判据 `rs485` 的「无溢出」带 `if_present`，只在帧里有 `overrun` 时判；工装固件照报照判

  | 做法 | 代价 | 风险 | 推荐 |
  |---|---|---|---|
  | A · 板卡包串口加溢出计数（`HAL_UART_ErrorCallback` 里数，`HardwareSerial` 给一个读它的函数），demo 报 `overrun` | 改板卡包、随下一版发；用户 app 多一个函数 | 和上游 STM32duino 多一处分叉；**与用户「不想跟 stm32duino 分叉」相悖**（[决策 124](../../../docs/tables/DECISIONS.md)「USB 打印卡住」那一行） | 判据和工装固件完全一样，测的仍是用户 app 的串口 |
  | B · 判据「无溢出」只在帧里有这个字段时判 | 改 `ptcheck` 或方案 | 工装固件哪天丢了这个字段也没人报 | ⭐ 不分叉 STM32duino |
  | C · 不改，用户级 RS485 判不过 | 无 | 用户级永远不过 | |
