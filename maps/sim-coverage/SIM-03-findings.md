# SD 卡在 Renode 里能不能读写（调研记录）

2026-10-04，回答 [SIM-03](issues/SIM-03-does-sd-work-in-renode.md)。Renode 1.17.0，平台 `platforms/cpus/stm32h743.repl`，
0.1.3 板卡包里的两个例程（FQBN 同 `$TEST/tools/run_examples.py`），STM32SD 1.5.0，**经真 bootloader 引导**（flash 布局复用 `$TEST/host/renode/run.py` 的 `flash_banks()`）。
原型在会话 scratch 里，没进任何仓库。

## 结论

| 问题 | 结论 | 核实 | 证据 |
|---|---|---|---|
| `SD_ReadWrite` 能不能跑通 | **能**：打出 `SD_ReadWrite: OK`，镜像里有 `TEST.TXT`，内容 `hello from OpenPLC\r\n` | ✅ 实测 | 见下「怎么看到的」①② |
| `SD_FileReceive` 收文件后镜像内容是否一致 | **一致**：5004 字节随机数据经 usart3 YMODEM 送入，镜像里 `RECV.BIN` 逐字节相同 | ✅ 实测 | 例程打 `SD: wrote RECV.BIN, … crc32=23445B74`；Python 读镜像比对 `equal: True` |
| 卡检测 PE6 能不能用 `OnGPIO` 模拟插拔 | **能（只到引脚这一层）**：`gpioPortE OnGPIO 6 true` → 例程打 `SD: card removed`、调 `SD.end()`、RS232 上不再发 `C`；改回 `false` → 再调 `SD.begin()`、打 `SD: card inserted`、`C` 恢复 | ✅ 实测 | 拔出后 90 s（实际时间）RS232 收到 0 字节；插回后 60 s 收到 59 个 `C` |
| 拔卡后卡本身是否「消失」 | **不会**：`OnGPIO` 只改检测脚，SDMMC 上的卡模型还挂着；「拔卡途中读写失败」这类行为模拟不出 | 读代码推断，没实测 | 卡由 `SdCardFromFile` 挂在 `sysbus.sdmmc` 上，脚本里没有摘卡的步骤 |
| HAL 轮询 + 1 线在 `STM32HSDMMC` 模型上能否走通（REN-02 的未核实项） | **能** | ✅ 实测 | 同上两条；模型对 DCTRL.DTEN 报 `Unhandled`，但不影响读写 |

## 要照做才跑得通的四件事

| 事 | 为什么 | 不这么做的后果 |
|---|---|---|
| 镜像要事先格式化成 FAT32，`SdCardFromFile` 第四个参数给 `true` | `true` 直接读写这个文件，跑完能在主机上检查；`false` 用临时副本，跑完看不到 | 空镜像 → `SD.begin()` 失败；`false` → 镜像里永远是空的 |
| `cpu PerformanceInMips 10` | 默认 100 时虚拟时间比实际时间慢约 15 倍（bootloader 里有按指令数计的等待），20 s 虚拟要跑约 5 分钟 | 慢到收发超时；改成 10 后两个例程结果不变，约等于实时 |
| 发送端把数据按 32 字节一段、段间隔 50 ms 发 | Renode 的串口不按波特率节流，一个 1029 字节的包瞬间灌进去，中断连续触发，`loop()` 来不及取，核心 64 字节的接收环形缓冲溢出 | 头包 CRC 错，例程只回 `C`，从不回 `ACK` |
| 串口经 `emulation CreateServerSocketTerminal <端口> "rs232" false` + `connector Connect sysbus.usart3 rs232` 引到 Python，`ymodem.send()` 原样可用 | `ymodem.py` 只要求对象有 `read(1)` / `write()` | — |

⚠️ 分段节流靠的是实际时间，机器很忙时虚拟时间会变慢，节流是否仍够没测；
更稳的做法（按虚拟时间喂字节）没做。

## 怎么看到的

`Serial` 走 USB CDC，Renode 里看不到（SIM-01 在查）。这里**不看 `Serial`**，用两种办法：

1. **函数钩子读参数**：在 `Print::println(const char*)`、`Print::print(const char*)`、`Print::println(const String&)` 上挂 `cpu AddHook`，钩子里用 `machine.SystemBus.ReadBytes(r1, 48)` 读出字符串打日志。例程打到 `Serial` 的每一行都能这样看到；`print(unsigned long)` 没挂，所以字节数那一段是空的。
2. **跑完读镜像**：用 `pyfatfs` 打开镜像，列文件、读内容比对。

另外在 `SDClass::begin`、`SDClass::end` 上挂钩，判断插拔是否真的触发了卡初始化 / 释放。

## 测不到什么

| 盲区 | 原因 |
|---|---|
| 真卡的时序、4 线 / 高速模式、写保护、坏卡 | 例程只用 1 线；模型不模拟物理层 |
| 拔卡中途的读写错误处理 | 卡模型拔不掉，见上 |
| 分区表（MBR）镜像 | 这次镜像是不带分区表的 FAT32（`pyfatfs.mkfs` 的格式）；真卡一般带 MBR，FatFs 两种都认，但没在 Renode 里试 |
| `SD_FileReceive` 打在 `Serial` 上的完整行 | `print(unsigned long)` 没挂钩；SIM-01 解决后可直接看 |
| 大文件 / 多文件批次 | 只送了一个 5004 字节（5 个 1 KB 包）的文件 |

## 和现有用例的关系

`$TEST/host/renode/run.py`（用例 `T3-05`，每个例程经真 bootloader 能启动并持续进 `loop()`）给 SD 挂的是**没格式化的空镜像**、参数 `false`，镜像里没有文件系统，挂载必然失败（读代码推断，没在 T3-05 里看日志），所以那条用例**没测到 SD 读写**，只测到 SD 例程能启动。要把这条覆盖进模拟用例，得另写，按上面四件事配置。
