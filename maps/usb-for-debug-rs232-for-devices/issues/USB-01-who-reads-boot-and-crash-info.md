# 开机、bootloader、死机的信息，出厂板子上给谁看、在哪看

Type: grilling
Opened: 2026-10-17
Status: resolved
Blocked by: -

## Question

现在这些信息只走 RS232：bootloader 的 135 处 `printf`（UART4）、core 开机的 `[BOOT]` `[NET]` 两行、SDRAM 自检结果。RS232 让给设备以后，它们去哪：

| 可能 | 代价 |
|---|---|
| 出厂版完全不打，开发 / 测试版用编译开关仍走 RS232 | 两种固件；客户板上出问题时看不到 |
| 改走 USB | bootloader 的 USB 口在跑 IAP 协议；开机最早那段 USB 还没连上 |
| 存成诊断记录，连上 USB / 网口时读出来 | 要定存哪、多大（见地图「Not yet specified」） |

讨论中已定：

| 事 | 定了什么 |
|---|---|
| 去向 | 原来打到 RS232 的日志（bootloader、core）全部改走 USB；为此 USB 要提前初始化，开机、交权、上传的流程跟着改（用户 2026-10-17 更正） |
| 死机信息 | 故障时写进复位后不丢的内存、下次开机收进诊断信息；SWO 照旧保留给开发（用户 2026-10-17） |
| USB 口数 | 做成两个 CDC 口，日志和 IAP 协议分开（用户 2026-10-17；和 [IDE-17](../../arduino-examples-and-ide-flow/issues/IDE-17-usb-and-ethernet-share-one-upload-flow.md) 合流） |
| 两个口的分工 | bootloader 和 app 一致：口 1 看日志（app 里也是用户的 `Serial`），口 2 跑 IAP 协议；系统日志放口 1，每行带前缀，和用户输出区分（用户 2026-10-17） |
| 开机缓存 | 环形缓冲区放 SRAM4 的不初始化区域，先定 4 KB，复位保留、断电清空；电脑打开口 1 时先吐缓存再接实时输出，sketch 里可关；IAPTool 另有命令随时读（用户 2026-10-17 按推荐） |
| 交权 | 交权时 USB 照常断开重连；bootloader 和 app 报给电脑的身份统一，COM 号不变（用户 2026-10-17 按推荐） |
| 死机 | 不打 RS232（用户 2026-10-17） |
| SRAM4 缓存不被用户占用 | 三份链接脚本的 `RAM_D3` 把缓存那 4 KB 挖掉（同交接记录的做法），挡住链接器放进来的变量；用户直接用指针写坏时，靠每条记录的魔数和校验发现、整块丢弃；不用 MPU（用户 2026-10-17） |
| 用户改 app 的 USB 身份 | 不拦；IAPTool 重启后按 bootloader 的身份 + 板子 UID 重新找口，上传不受影响，只是交权时 COM 号会变，文档写明（用户 2026-10-17） |

## 怎么算答完

出厂版 bootloader 和 core 各自在 RS232 上输出什么（可以是「什么都不输出」）、这些信息改去哪里，用户定下并写进 M1、M3。

## Answer

2026-10-17 定，逐条见上面「讨论中已定」那张表；要求写成 [M1](../../../docs/modules/M1-firmware-upgrade.md) `R1-43`、[M3](../../../docs/modules/M3-app-runtime.md) `R3-22`。

- 出厂板子上 bootloader 和 core 不往 RS232 写任何东西，RS232 完全归用户程序
- 日志走 USB 口 1（app 里即用户的 `Serial`，系统行带前缀），口 2 跑 IAP 协议；bootloader 和 app 分工一致、身份统一
- 电脑来不及打开口 1 的那段存进 SRAM4 的 4 KB 开机缓存；故障信息复位后经口 1 吐出，SWO 留给开发；不设 RS232 日志开关

## 引出了什么新的未知

- bootloader 也要做双 CDC 口，开机就初始化 USB —— 和 [IDE-17](../../arduino-examples-and-ide-flow/issues/IDE-17-usb-and-ethernet-share-one-upload-flow.md) 合流
- IAPTool 重启后按 bootloader 身份 + 板子 UID 找口
- 系统日志前缀的格式；开机缓存的记录格式
- 缓存地址和大小是新的跨仓镜像（bootloader / 板卡包），要进 ARCHITECTURE 和 P2
- 「USB 速度」菜单里的 High Speed 两项，板子只有全速口，选了可能没有 USB（未细查）
