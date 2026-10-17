# 从上电到 app 跑起来，RS232 端子上实际会出现什么

Type: task
Opened: 2026-10-17
Status: resolved
Blocked by: -

## Question

读 bootloader、交权、core 的代码，列出上电到 `setup()` 之间所有碰 RS232 的动作：`RS232_EN`（PB10）何时拉高拉低、UART4 / USART3 何时初始化、谁打了什么、交接时那两个固定的坏字节（TODO 优先级最低一节）。接在 RS232 上的设备会收到这些。

## 怎么算答完

一张按时间排的表：动作、出处（文件:行号）、设备那头看到什么；写进本票 Answer，作为 USB-01 和 USB-03 的依据。

## Answer

2026-10-17 定

硬件前提（PB10 低 = MAX3221 整片关断、PC10 → DIN、端子 C05/C06）见 [HARDWARE-FACTS.md](../../../docs/hardware/HARDWARE-FACTS.md)「RS232 路径」，下表不重述。行号按 2026-10-17 的工作区。

**A. 正常上电**（有合法 app、BOOT0 没按、board 已认领、BOR = 3、sector 15 无需修复）

| # | 时刻 / 动作 | 出处 | 接在 RS232 上的设备看到 |
|---|---|---|---|
| 1 | 上电到 `main()` 前：PB10 未配置，R68 下拉 → 收发器关断 | HARDWARE-FACTS「PB10 拉低 = 整片关断」 | 静默：TxD 无驱动（关断时发送器输出高阻，取自 MAX3221 数据手册，本仓无副本、未量） |
| 2 | 锁存复位原因；`safe_outputs_init()` 只动 DO/AO/KNX_TX，不碰 PB10、PC10 | `$BOOT` `Core/Src/main.c:242`、`:247`；`IAPServer/safe_outputs.c:18` | 无 |
| 3 | 打开三个故障异常；UART4 起来之前的故障报告只走 SWO/ITM | `$BOOT` `Core/Src/main.c:257` | 无 |
| 4 | `MX_GPIO_Init()`：PB10 配推挽、先写低 | `$BOOT` `Core/Src/main.c:294`；`Core/Src/gpio.c:67`、`:97` | 无（仍关断） |
| 5 | `Enable_RX_RS232()`：PB10 拉高，收发器上电 | `$BOOT` `Core/Src/main.c:295`；`Core/Src/usart.c:148` | 线进入空闲；此刻 PC10 还没接 UART4，DIN 悬空到 #6 为止（是否出毛刺未量） |
| 6 | `MX_UART4_Init()`：115200 8N1，PC10/PC11 AF8；RX 打开但没人读 | `$BOOT` `Core/Src/main.c:296`；`Core/Src/usart.c:48`、`:112` | 空闲；设备发来的字节被丢弃 |
| 7 | `bor_level_report()`：BOR ≠ 3 才打 1 行 | `$BOOT` `IAPServer/bor_check.c:19` | 正常板无 |
| 8 | 开机提示 2 行 + `** Reset cause: POR/PIN/SOFT…` | `$BOOT` `Core/Src/main.c:307`、`:310` | 3 行 |
| 9 | `Startup window: system LED blinking for 2 s`，随后 2 s 闪灯 | `$BOOT` `Core/Src/main.c:183`–`:191` | 1 行，然后 2 s 静默 |
| 10 | `bootloader_state_init()`：`Bootloader state: N/M metadata slots used…` | `$BOOT` `Core/Src/main.c:317`；`IAPServer/bootloader_state.c:282` | 1 行 |
| 11 | `owner_slot_report()`：记录数、`claimed at generation`、空闲槽数 | `$BOOT` `IAPServer/IAP_server.c:630`；`IAPServer/owner_slot.c:755`、`:769`、`:808` | 3 行（空板只有 `:750` 1 行） |
| 12 | `BOOT0 button is not pressed.` | `$BOOT` `IAPServer/IAP_server.c:648` | 1 行 |
| 13 | `** APP Mod ...` | `$BOOT` `IAPServer/IAP_server.c:727` | 1 行 |
| 14 | `Disable_RX_RS232()`：PB10 拉低，收发器关断 | `$BOOT` `IAPServer/IAP_server.c:755` | 回到静默；电荷泵余电衰减期间驱动器仍能出合规电平（HARDWARE-FACTS「电荷泵余电」） |
| 15 | `HAL_UART_DeInit(&huart4)`：关断之后才释放 PC10/PC11 | `$BOOT` `IAPServer/IAP_server.c:756` | 无 |
| 16 | `HAL_DeInit()` 复位全部 GPIO（PB10 回复位态，R68 继续拉低）、`safe_outputs_init()`、跳 app | `$BOOT` `IAPServer/IAP_server.c:766`、`:788`、`:798` | 无 |
| 17 | app `premain()`：`init()`（USB CDC 在这里初始化）、`MX_RTC_Init()`；随后 `initVariant()` | `$CORE_REPO` `cores/arduino/main.cpp:117`、`:145`；`libraries/SrcWrapper/src/stm32/hw_config.c:74` | 无 |
| 18 | PB10 推挽拉高，收发器上电，此后不再拉低 | `$CORE_REPO` `cores/arduino/main.cpp:149`–`:150` | 线进入空闲；PC10 仍是复位态，DIN 悬空到 #19 为止（是否出毛刺未量） |
| 19 | `RS232.begin(115200)`：USART3 AF7 on PC10/PC11 | `$CORE_REPO` `cores/arduino/main.cpp:153`、`:46`、`:36` | 空闲 |
| 20 | `[BOOT] millis=N` | `$CORE_REPO` `cores/arduino/main.cpp:56`–`:57` | 1 行 |
| 21 | 网口初始化、UDP 服务启动，不打印 | `$CORE_REPO` `cores/arduino/main.cpp:154`–`:155` | 无 |
| 22 | `setup()`：PB10 高、USART3 开着交给 sketch | `$CORE_REPO` `cores/arduino/main.cpp:159` | — |
| 23 | `setup()` 之后，拿到 IP 时在 `loop()` 间隙打一次 `[NET] ip=… mac=…` | `$CORE_REPO` `cores/arduino/main.cpp:168`、`:89`、`:68`–`:83` | 1 行，时刻取决于 DHCP，插在 sketch 自己的 RS232 输出中间 |

打印总量：bootloader 129 处 `printf`（`IAP_server.c` 33、`owner_slot.c` 38、`bootloader_state.c` 13、`stm32h7xx_it.c` 11、`iap_auth.c` 10、`main.c` 7、`udp_server.c` 7、`IAP_boot_handoff.c` 4、`boot_selfupgrade.c` 3、`fmc.c` 2、`bor_check.c` 1），全部经 `__io_putchar` 同时写 ITM 和 UART4（`$BOOT` `Core/Src/main.c:105`–`:109`）；app 侧开机只有 `main.cpp` 的 `[BOOT]` / `[NET]`，另有 9 处 `printf`（`IAP_boot_handoff.c` 4、`OpenPLC_IAP` 5）只在出错时打，经 `_write` 走 USART3（`$CORE_REPO` `cores/arduino/Print.cpp:249`，`DEBUG_UART` 见 `variants/STM32H7xx/H743/variant_PLC_H743.h:478`）。

**B. 其他路径**（只列和 A 的差别）

| 路径 | 差别 | 出处 | 设备看到 |
|---|---|---|---|
| BOOT0 上传（2 s 时按着，10 s 前松） | 多一行提示；`BOOT0 button is pressed!`；`** UPLOAD Mod ... (BOOT0 held)` + `Please input your command:`；第二次 `MX_GPIO_Init()` 把 PB10 拉低再拉高（收发器关一瞬）；`Backup domain retained`、`SDRAM staging buffer OK`；之后才开 USB CDC 和网口；5 s 没网线再 2 行；整个上传会话的日志都上 RS232；成功后 `Checksum and signature OK. Rebooting...` → 软复位 → 再走一遍 A（`Reset cause: SOFT`） | `$BOOT` `Core/Src/main.c:200`、`:342`、`:348`、`:353`、`:355`、`:359`、`:362`；`IAPServer/iap_auth.c:151`；`Core/Src/fmc.c:123`；`IAPServer/IAP_server.c:724`、`:821`、`:562` | A 的 #1–#12 + 约 7 行 + 会话日志，然后整段 A 再来一遍 |
| 恢复出厂（按住超过 10 s 再松） | 再多 `Factory reset ARMED` 和 `FACTORY RESET DONE…`（无 root 时为 `nothing to do`）；owner 报告变成 `last record is a factory reset`；其余同上传 | `$BOOT` `Core/Src/main.c:210`、`:328`；`IAPServer/owner_slot.c:591`、`:561`、`:773` | 同上传，多 2 行 |
| BOOT0 卡住 30 s | 1 行 `treating it as stuck`，按上传处理 | `$BOOT` `Core/Src/main.c:215` | 同上传，多 1 行 |
| 没有合法 app（含空板） | `App signature invalid or absent` + `UPLOAD Mod ... (no valid application)`，其余同上传 | `$BOOT` `IAPServer/IAP_server.c:708` | 同上传 |
| app → bootloader：1200 波特 touch | app 收到 1200 波特就写交接记录并 `NVIC_SystemReset()`，成功不打印（写失败才经 USART3 打 1 行）；复位后 PB10 由 R68 拉低，走 A 的 #1–#12（`Reset cause: SOFT`），然后 `UPLOAD Mod ... (CDC upload requested)`，只开 USB CDC，其余同上传 | `$CORE_REPO` `cores/arduino/stm32/usb/cdc/usbd_cdc_if.c:184`；`cores/arduino/stm32/IAP_boot_handoff.c:157`、`:161`；`$BOOT` `IAPServer/IAP_server.c:694` | 复位那一刻 app 正开着收发器，是否出毛刺未量；之后同上传 |
| app → bootloader：签名重启 `openplc_server_reboot` | 验签通过就同上；拒绝或冷却期内经 USART3 打 1 行；原因为 `ethernet upload requested`，只开网口 | `$CORE_REPO` `libraries/OpenPLC_IAP/src/udp_server.c:177`、`:189`、`:195`、`:88`；`$BOOT` `IAPServer/IAP_server.c:698` | 同 1200 波特 touch |

**交接时那两个坏字节**（[TODO.md](../../../work/TODO.md) 第 4 节）：`[`、`0xC2` 固定出现在 `[BOOT] millis=` 之前。现行代码里没有任何一处有意发它们；那组实测早于决策 100，当时 app 里 PB10 为低。#18 → #19（以及 bootloader 的 #5 → #6）都是「收发器先上电、DIN 后接 UART」，是候选来源，未验证。

**结论**

- 每次正常上电，设备在约 2 s 内收到 bootloader 10 行 + app 1 行 `[BOOT] millis=`（115200 8N1），`setup()` 之后再收到 1 行 `[NET]`；上传、恢复出厂、从 app 重启进 bootloader 的路径还要多出十余行乃至整段会话日志，最后再走一遍正常上电。
- 收发器的开关只有三处：bootloader `main.c:295` 开、`IAP_server.c:755` 关、core `main.cpp:150` 开且不再关。要让 RS232 在开机时完全安静，得去掉这些打印，单靠 PB10 做不到 —— app 一进来就把它打开了。
- 另找出口的事实：bootloader 的 `printf` 只走 ITM + UART4；它的 USB CDC 只在留在 bootloader 时、所有开机打印之后才起（`main.c:358`–`:359`），正常启动根本不开 USB。app 的 USB CDC 在 `premain()` 里就起来了，比 `[BOOT]` 早，但那时主机多半还没打开端口。SWO/ITM 只有调试器打开 ITM 才有输出（`main.c:92`），引脚在 JTAG 座（`$HW` `Hardware_overview.txt:114`），app 不走 ITM —— 只能给开发和测试用。

## 引出了什么新的未知

- [HARDWARE-FACTS.md](../../../docs/hardware/HARDWARE-FACTS.md)「电荷泵余电」和 [TODO.md](../../../work/TODO.md) 第 4 节仍按决策 100 之前（app 里 PB10 为低、`[BOOT]` 靠余电出来）描述；现行 `main.cpp:150` 在打印前已拉高 PB10，那两处要改
- 两个坏字节在决策 100 之后是否还在、是否来自「收发器先上电、DIN 后接 UART」那一瞬 —— 要上板量，量之前先问板子是否空闲
- 复位瞬间（app 收发器开着时 `NVIC_SystemReset()`）线上是否出毛刺 —— 同上，要上板量
