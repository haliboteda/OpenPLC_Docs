# 13 个例程在 Renode 里跑两层检查

Type: task
Opened: 2026-09-28
Status: claimed
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
| `CAN_Counter` | 第一帧对：TXBC `0x08000200`，消息 RAM `0x048C0000`（ID 0x123）、`0x00040000`（DLC 4），TXBAR `0x1`。**但第一帧后约 75 ms `loop()` 不再被调用**，停在哪还没查到 | ⏳ 在查 |
| `Ethernet_IP` | 还没测。已写好带 LAN8742A PHY 的平台叠加文件 | ⏳ |
| `USB_Serial` | 还没测 | ⏳ |

①：13 个都通过（`SD_ReadWrite` 要挂卡）。⚠️ 但原型脚本在结束 PC 读不到时默认「没卡住」，`CAN_Counter` 就这样漏判了；已改成读不到即失败，**另外 12 个要用改后的脚本重跑一遍 ①**。

## 测法上踩过的坑（不是固件的错）

| 现象 | 原因 | 办法 |
|---|---|---|
| 结束时的 PC、`echo` 输出读不到；控制台报 `Adding the specified count to the semaphore...` | Renode 的标准输入被关闭或继承时，控制台读线程崩溃，之后的监视器命令全部丢失 | 启动 Renode 时给一根一直开着的 stdin 管道，直到它退出 |
| 暂停时 `usart3 WriteChar` 注入无回显 | 同上一条有关，未单独核实 | 运行中经 `CreateServerSocketTerminal` 从 TCP 端口收发 |
| `SD_ReadWrite` 卡在 CMD0 | 卡检测脚 PE6 低有效，Renode 输入默认读低 = 有卡；没挂卡时模型不回 CMDSENT | `machine SdCardFromFile` 挂镜像 |
| DAC 控制寄存器读回 0 | DAC1 在平台里只是 Tag，不存值 | 只看数据寄存器 DHR12R1/R2 |
| 日志里 `HIT loop (37)` | Renode 合并连续重复的日志行 | 计数要按括号里的次数加 |
| 全量记录 FDCAN / 消息 RAM 访问后 25 s 仿真跑了 5 小时 | `loop()` 每圈都轮询 FDCAN，日志拖垮仿真 | 改用函数入口钩子 |
| 每次启动 bootloader 要约 6.5 s 虚拟时间才跳进 app | 开机继电器窗口等 | 仿真时长按「6.5 s + 例程所需」给 |
