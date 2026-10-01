# 13 个例程在 Renode 里跑两层检查

Type: task
Opened: 2026-09-28
Status: resolved
Blocked by: REN-01, REN-02

## Question

按图里定的两层做法，13 个例程逐个跑：① 启动链走完、`setup()` 走完、`loop()` 在转、没跑飞；② 各自端口的寄存器读写对不对。判失败时分清是代码的错还是模型或测法的错。

## 怎么算答完

13 个例程两层都有结论；判失败的每一个说出是代码、模型还是测法的问题。之后再定写进仓库的方案。

## 进度（2026-09-28，全部在 Renode 里实测）

| 例程 | ② 看到了什么 | 结论 |
|---|---|---|
| `DO_Outputs` | 先全拉低，再 DO1→DO8 依次开关 | ✅ |
| `Relays` | 先全关，再 R1→R6 依次开关 | ✅ |
| `SystemLED` | PE2 交替开关 | ✅ |
| `DI_Inputs` | 拉高 DIN1/3/8 后全局变量 `last` = `0x85` | ✅ |
| `RS232_Echo` | USART3 发 `HI!` 原样收回 | ✅ |
| `RS485_Echo` | USART2 整行原样收回；PD4 发前拉高、发完拉低 | ✅ |
| `SD_ReadWrite` | 挂 FAT32 镜像后，卡里 `TEST.TXT` = `hello from OpenPLC` | ✅ |
| `AI_Inputs` | ADC3 通道 1、ADC1 通道 3 | ✅ |
| `BoardTemperature` | ADC1 通道 15、16 | ✅ |
| `AO_Outputs` | 两路 DAC 依次写 0 / 838 / 1677 / 2515 / 3354，循环 | ✅ |
| `CAN_Counter` | 第一帧：TXBC `0x08000200`，消息 RAM `0x048C0000`（ID 0x123）、`0x00040000`（DLC 4），TXBAR `0x1`；14 s 内发出 5 帧 | ✅ 曾以为第一帧后 `loop()` 停住，是测法的错，见下表 |
| `Ethernet_IP` | 经 MDIO 读到 PHY link up（`last_link` = 1）；MAC 发出 DHCP DISCOVER 及 3 次重发 | ✅ 拿地址测不到：Renode 的 NetworkServer 没有 DHCP |
| `USB_Serial` | OTG_FS 初始化正确（FDMOD、DCFG 全速、软连接）。**发现 core 的 bug**：USB 初始化把 PA8/PA9/PA10（DO5、DO6、KNX_RX）也配成了 USB 功能，见 [HARDWARE-FACTS.md](../../../docs/hardware/HARDWARE-FACTS.md)「USB FS 只接了 PA11 / PA12」。已修，2026-09-28 真板子上确认 | ✅ 枚举和收发测不到，真板子上回显正常 |

①：13 个都通过（`SD_ReadWrite` 要挂卡），改后的脚本上跑过两轮：USB 修复前一轮、修复后一轮。

## 测法上踩过的坑（不是固件的错）

| 现象 | 原因 | 办法 |
|---|---|---|
| 结束时的 PC、`echo` 输出读不到；控制台报 `Adding the specified count to the semaphore...` | Renode 的标准输入被关闭或继承时，控制台读线程崩溃，之后的监视器命令全部丢失 | 启动 Renode 时给一根一直开着的 stdin 管道，直到它退出 |
| 暂停时 `usart3 WriteChar` 注入无回显 | 同上一条有关，未单独核实 | 运行中经 `CreateServerSocketTerminal` 从 TCP 端口收发 |
| `SD_ReadWrite` 卡在 CMD0 | 卡检测脚 PE6 低有效，Renode 输入默认读低 = 有卡；没挂卡时模型不回 CMDSENT | `machine SdCardFromFile` 挂镜像 |
| DAC 控制寄存器读回 0 | DAC1 在平台里只是 Tag，不存值 | 只看数据寄存器 DHR12R1/R2 |
| 日志里 `HIT loop (37)` | Renode 合并连续重复的日志行 | 计数要按括号里的次数加 |
| 全量记录 FDCAN / 消息 RAM 访问后 25 s 仿真跑了 5 小时 | `loop()` 每圈都轮询 FDCAN，日志拖垮仿真 | 改用函数入口钩子 |
| 不带 `delay()` 的例程第一圈后 `loop()` 像是停了、仿真极慢 | `loop()` 上常驻的 Python 钩子每圈都执行 | 钩子打一次就摘；结束后再挂一次、多跑 10 s，确认 `loop()` 还在转 |
| `fdcan1: FrameSent is not initialized` | FDCAN 没接总线 | 无害，不用接 CAN hub |
| 每次启动 bootloader 要约 6.5 s 虚拟时间才跳进 app | 开机窗口等 | 仿真时长按「6.5 s + 例程所需」给 |

## Answer

2026-09-28 定。13 个例程两层都过，判失败的都是测法的错（见上表）。进仓库只做第 ① 层：用例 `T3-05`，脚本在 `$TEST/host/renode/`，判据见 [M3 应用运行环境](../../../docs/modules/M3-app-runtime.md) 的「测试怎么跑」节；第 ② 层的结论就是上面的进度表，不自动复查。

脚本拼的 metadata 记录不另加一致性检查：bootloader 每次启动都校验它，格式不对 `T3-05` 就判「没跳进 app」。

## 引出了什么新的未知

没有。
