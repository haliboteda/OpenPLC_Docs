# 要人配合的步骤脚本怎么问

Type: grilling
Opened: 2026-09-29
Status: resolved
Blocked by: EXB-01

## Question

DI 加 0–24 V、量 AO 和 DO、在 ETS 里看 KNX、插拔 SD 卡 —— 这些步骤脚本怎么提示、怎么知道人做完了（能靠板子的输出自己看出来的就不让人按回车）、人量到的数值要不要录进结果、这些步骤能不能集中到一次跑完。

## 怎么算答完

逐个列出要人配合的步骤：提示文案、完成的判断方式、结果怎么记；定下它们在整轮里的顺序。

## Answer

2026-10-03 定（用户五条都按推荐）：

| 问题 | 定了什么 | 一句理由 |
|---|---|---|
| 提示长什么样 | 用 `$TEST/tools/common.py` 的 `banner()`（固定框 + 🍍），框里只写动作和脚本在等什么，再响一声；英文 | 普通一行会混在日志里被漏看 |
| 怎么知道做完了 | 板子输出看得出来的，脚本自己等，最多 120 s，超时判不过；只能人看的，按一个键答 `y` / `n`，不用回车，一直等 | 能自动判的不让人回来报 |
| 量到的数录不录 | 不录，只记过 / 不过；答 `n` 时补一句备注，列在结果里 | AO 准不准归 [每块板的校准](../../per-board-calibration/map.md)，这里只看会不会动 |
| DI 测到什么程度 | 8 路逐路：加 24 V 后位图必须恰好只有这一路是 1，撤掉后回到全 0；不测门限 | 接错线能看出来；门限要人报电压，属于硬件和产线测试 |
| 顺序 | 开跑前一个框列出要先接好的东西（SD 卡、网线、24 V、AO 的表），按 `y` 开始；然后先跑要人的，跑完人可以离开 | 人只在开头守着 |

逐个例程（KNX 等 [KNX 回显例程长什么样](EXB-02-what-does-the-knx-echo-example-look-like.md)；`AI_Inputs` 这一轮不测）：

| 顺序 | 例程 | 人做什么 | 怎么判 |
|---|---|---|---|
| 1 | `DI_Inputs` | 按提示逐路加、撤 24 V | 位图（自动） |
| 2 | `DO_Outputs` | 看 DO1..DO8 依次亮 | 串口出现 `DO8 on` + 人答 `y` |
| 3 | `Relays` | 听 RY1..RY6 依次吸合 | 串口出现 `RY6 closed` + 人答 `y` |
| 4 | `SystemLED` | 看系统灯一秒闪一次 | 串口出现 `on` / `off` + 人答 `y` |
| 5 | `AO_Outputs` | 看表跟着打印的电流走 | 串口走到 `20.0 mA` + 人答 `y` |
| 6–14 | `USB_Serial` `RS485_Echo` `RS232_Echo` `CAN_Counter` `Ethernet_IP` `SD_ReadWrite` `BoardTemperature` `SDRAM_Basic` `SDRAM_DataLogger` | 不用人 | 照 [测试脚本怎么判一个例程过没过](EXB-01-how-does-the-script-judge-an-example.md)，判据在 `$TEST/tools/run_examples.py` 的表里 |

## 引出了什么新的未知

- 台子上有没有 RS232 转接器：`RS232_Echo` 和两个 SDRAM 例程都要它，归 [台子接线核对](EXB-06-bench-wiring-checklist.md)
