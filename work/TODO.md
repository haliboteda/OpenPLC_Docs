# 待办

**要做的事和在等的事只写在这一份文件里**（[决策 85](../docs/tables/DECISIONS.md)），每天的工作就是同步它。准入和分节见 [../WHERE-THINGS-LIVE.md](../WHERE-THINGS-LIVE.md)：

> 每一条必须写明它是哪张已关的票（或哪条决策）产生的。写不出来的，写不进去。

做完且判据过了，**删掉那一行**，不打勾、不划掉（git 有历史）。

- 用例的判据和跑法在 [HOW-TO-RUN-TESTS.md](../docs/engineering/HOW-TO-RUN-TESTS.md) 和各模块文档的用例表里，这里只写跑哪条、看什么
- 反复走的流程（每次改完、每次发版、每块板出厂）是 [验收单 CHK-A / B / C](../docs/tables/ACCEPTANCE-CHECKLIST.md)，不是待办
- 模拟里已经测过、只差上板的需求，逐条在 [RECONCILE.md](../maps/sim-coverage/RECONCILE.md)

---

## 1 · 上板那天，按顺序做

**要人动手的全排在 1.1，一次做完；之后的步骤多数能自己跑。** 0.1.3 只有一条发布线：这一节全过，才重建 0.1.3 的 release 和 tag（[决策 83](../docs/tables/DECISIONS.md)）。

### 1.1 动手准备

| # | 做什么 | 怎么算做完 | 来自哪 |
|---|---|---|---|
| 1 | **台子接线核对**：USB-C（板子 CDC）、网线到有 DHCP 的网、RS232 真电平转接器（C05/C06）、USB-RS485、CANable（开 120 Ω 终端）、KNX 总线电源 + 网上的 KNX IP 网关、24 V 供电、一根能逐路点 DI1–DI8 的 24 V 线、AO1/AO2 各串一块电流表、ST-Link。COM 口以 `PortTool ports` 为准（09-30 记过 COM12 = PL2303 控制口、COM16 = CH340 RS485、COM15 = CANable、COM17 = 板子 USB，换过 USB 口就会变） | 每个对端对到一个确定的 COM 口或 IP，写进 `$TEST/config/machine.py` 能用的形式；板子能被 PC 发现 | [台子接线核对](../maps/core-examples-on-board/issues/EXB-06-bench-wiring-checklist.md) |
| 2 | **SD 卡换一张 FAT32 的**（现在那张 60 GB 读出 `fs=none`，大概率 exFAT），插进卡座 | 工装 `sd-card` 步 `fs` 不是 `none` | [XPT-03](../maps/porttool-on-linux-and-macos/issues/XPT-03-which-real-machines-and-what-the-test-case-is.md) 的实测 |
| 3 | **板子上电恢复**：09-30 收工时 ST-Link 量到目标电压 0.00 V | 上电后 ST-Link 读得到目标电压，`PortTool ports` 能看到控制口 | 2026-09-30 工装调试 |
| 4 | **按当前源码重编 bootloader 和工装固件**：`$BOOT/Debug/` 里那份是 10-03 12:48 编的，早于输出置 0 和 PB14 两次提交；工装固件 `$PORTTOOL/build.py --fixture` 重编；`$TEST/Output/probe-images/` 两个探针镜像用当前 core 重编（旧镜像读旧根区地址） | `$TEST`：`python tools/build_image.py` 0 errors、`.bin` ≤ 131,072 B；工装镜像只剩那条刻意的 `#warning` | [决策 72](../docs/tables/DECISIONS.md)、[决策 81](../docs/tables/DECISIONS.md) |

### 1.2 bootloader 和所有权

| # | 做什么 | 怎么算做完 | 来自哪 |
|---|---|---|---|
| 5 | **ST-Link 烧当前 bootloader**；擦扇区 15 后写回这块板的校准值；过启动门禁 `T3-01`（R3-01） | `$TEST`：`python tools/flash_bootloader.py`；日志有 `SDRAM staging buffer OK`；校准值区逐字节等于烧之前读出的 | [决策 72](../docs/tables/DECISIONS.md) 第 6 阶段、[验收单 T3-01](../docs/tables/ACCEPTANCE-CHECKLIST.md#t3-01--启动门禁) |
| 6 | **开机输出置 0**：从上电到 sketch 第一次写之前，AO 0 mA、DO 和继电器全断开、PB14 为低；开机全程不响继电器，窗口内系统灯快闪 | 万用表 / 电流表实测；用一个不碰这些脚的 sketch 看 PB14 一直为低（模拟里 `T1-37` 已过） | [决策 81](../docs/tables/DECISIONS.md)、[开机窗口改用什么提示](../maps/iec-61131-2-factory-state/issues/IEC-01-what-replaces-the-relay-click.md) |
| 7 | **第一次上传自动认领**：出厂态板子经 USB 上传（`T2-35`）、恢复出厂后经网口上传（`T2-36`） | IAPTool 打印生成的私钥路径和 `Claimed.`，app 起来；两把私钥不同 | [决策 72](../docs/tables/DECISIONS.md)；[验收单 CHK-B4](../docs/tables/ACCEPTANCE-CHECKLIST.md#chk-b--发版验收) |
| 8 | **所有权回归**：整轮 `run_five_paths.py`（CHK-B9）盖住 `T2-02` `T2-03` `T2-05` `T2-09` `T2-10` `T2-11`；另外单跑 `T2-04`（`inject_owner_record.py --also-unsigned 9`）、`T2-12`–`T2-14`（`run_rotate_root_revokes_old_leaf.py`）、`T2-25`（`setowner --wipe`） | 每条达到 [M2](../docs/modules/M2-ownership.md) 用例表的判据 | 决策 58、决议 66 / 67、[决策 72](../docs/tables/DECISIONS.md) |
| 9 | **按 BOOT0**：按住复位进上传模式（`T1-27`，R1-04）；按满 10 秒灯常亮、松手恢复出厂 | 进上传模式、不跳 app；10 秒后恢复出厂、根区为空 | [开机窗口改用什么提示](../maps/iec-61131-2-factory-state/issues/IEC-01-what-replaces-the-relay-click.md) |
| 10 | **`flashboot` 真写扇区 0**：`T1-29`、`T1-31`；`T1-32` 按决策 72 后的新判据重跑（无根板一律 `Refused`） | `$TEST`：`python tools/run_flashboot.py`；见 [M1](../docs/modules/M1-firmware-upgrade.md) 用例表 | [M1](../docs/modules/M1-firmware-upgrade.md) 脚注 ¹¹ |
| 11 | **真断电**：擦写窗口掉电再上传（`T1-21` / `T1-22`）；nonce 跨掉电不重复（`T1-17`，`$TEST`：`python tools/run_au1.py`）；备份 SRAM 只靠 VBAT 时保持内容（断主电后读回）；拿掉 VBAT 电池后的行为（R1-31） | 各条按 M1 用例表的判据；备份 SRAM 断电前后逐字节相同 | [决策 72](../docs/tables/DECISIONS.md) 方案 5（出处已写进 `maps/root-key-without-bootloader-reflash/ROOT-05-findings.md`）、决议 66 |
| 12 | **发现**：回复在 2 秒内（`T1-03`，R1-10）、10 分钟浸泡（`T1-04`，R1-11）；**开机日志自相矛盾**：先打 `Ethernet link is DOWN …`，随后 DHCP 拿到 IP（`$BOOT/IAPServer/IAP_server.c` 的 `IAP_servers_start()`，疑为自协商没完成就判了，未核实） | `T1-03` / `T1-04` 按 M1 判据；日志：只有 link 真断时才打那句 | [M1](../docs/modules/M1-firmware-upgrade.md)、[出厂态怎么造](../maps/five-paths-e2e-test/issues/E2E-01-how-to-make-and-prove-factory-state.md) |
| 13 | **TRNG 抓包剩两项**：同一块板重启两次，DHCP 事务号不同；两次到板子的 TCP 连接，SYN-ACK 序列号不同（bootloader 和 app 各验一次）。⚠️ 本机有 Npcap、没有 Wireshark / scapy，会话不是管理员 | 两项都不同 | 决议 66 / 67 / 69（2026-09-24） |
| 14 | **复位原因**：按复位键、断电、软件复位各一次看启动日志（R1-30）；开看门狗故意卡死，sketch 用 `openplcResetCause()` 读出「看门狗」；`IWatchdog` 库开、喂、超时复位走一遍（上游 `IWatchdog::isReset()` 在本板多半永远是 false，未核实） | 日志里的复位原因和动作一致；sketch 读得出看门狗复位 | [决策 80](../docs/tables/DECISIONS.md) |
| 15 | **BOR 约 2.7 V**：实验室的板子用 ST-Link 写选项字节 `BOR_LEV=3`；把 24 V 慢慢调低 | 低于阈值时复位、输出全 0，回升后正常重启；开机检查不再报警（模拟里 `T1-37` 已判过检查本身）。另从原理图核实 3.3 V 那级在 24 V 掉到多少时才跟着掉 | [欠压和掉电时进入什么预定状态](../maps/iec-61131-2-factory-state/issues/IEC-06-what-happens-on-undervoltage.md) |
| 16 | **交权时外设冷不冷**（R3-02）：逐个外设看寄存器是不是复位值 | 和 [M3](../docs/modules/M3-app-runtime.md) R3-02 的说法一致 | [RECONCILE.md](../maps/sim-coverage/RECONCILE.md) |

### 1.3 app 和例程

| # | 做什么 | 怎么算做完 | 来自哪 |
|---|---|---|---|
| 17 | **15 个例程逐个上板**（`T3-06`，R3-09）：DI 逐路加 24 V、看 DO / 继电器 / 系统灯、量 AO（要人的先跑），之后自动；`SD_FileReceive` 经 RS232 发文件写卡 | `$TEST`：`python tools/run_examples.py --cdc … --rs485 … --rs232 …` 全过 | [测试脚本怎么判一个例程过没过](../maps/core-examples-on-board/issues/EXB-01-how-does-the-script-judge-an-example.md)、[要人配合的步骤脚本怎么问](../maps/core-examples-on-board/issues/EXB-05-how-does-the-script-ask-for-a-human-step.md) |
| 18 | **IDE 那条上传命令对真板子**（`T1-34`）：Tools → Port 选中真板子 Upload，未认领和已认领各一次 | 两次都上传成功、app 起来 | [一个例程长什么样](../maps/arduino-examples-and-ide-flow/issues/IDE-05-what-does-one-example-look-like.md) |
| 19 | **串口**：`Serial4.begin()` 不掐掉诊断口（`T3-03`，R3-05）；RS232 端子收发（`T3-04`）；sketch 在 `delay()` 里时照样应答网络、能经网口上传（R3-07） | 按 M3 用例表；`delay()` 期间发现有应答、`ether` 上传成功 | [RECONCILE.md](../maps/sim-coverage/RECONCILE.md) |
| 20 | **校准值生效**：写入已知系数后 AI / AO 读数按系数变；擦掉校准值区后退回标称并打一行日志 | 两种情况都和 [CALIBRATED-ANALOG.md](../docs/modules/M3/CALIBRATED-ANALOG.md) 一致 | [app 里怎么套用修正值](../maps/per-board-calibration/issues/CAL-06-how-does-the-app-apply-the-correction.md) |
| 21 | **两块板同时在台上时**：按 UID 定位（R1-13）；两块板的 MAC 不同（R1-14） | 定位到对的那块；MAC 不重复 | [RECONCILE.md](../maps/sim-coverage/RECONCILE.md) |

### 1.4 KNX（总线电源 + 网上的 KNX IP 网关 + ETS）

| # | 做什么 | 怎么算做完 | 来自哪 |
|---|---|---|---|
| 22 | **新的 STKNX 数据链路层上真总线**：ETS 导入 `$ETSPROD/OpenPLC_TP.knxprod`，按 BOOT0 进编程模式编物理地址、下载；`KNX_Switch`、`KNX_Inputs` 收发；用 ETS 总线监视器核对应答和空闲时序（「NAK、BUSY 共用重发计数」那条没有出处，看实际） | ETS 里看得到板子发的组报文，板子打印 ETS 发来的报文；空闲时不占总线；对方认我们的应答、我们也认对方的 | [KNX 库的 TP 收发怎么在本板上发出合法帧](../maps/core-examples-on-board/issues/EXB-08-how-does-the-knx-library-drive-stknx.md)、[KNX 例程按正规用法重写](../maps/knx-examples/map.md) |
| 23 | **新例程过了之后删旧的 5 个 KNX 例程**和库里两路继电器配置要不要留（地图迷雾里那条） | 旧例程删掉，P5 重跑全绿 | [KNX 例程按正规用法重写](../maps/knx-examples/map.md) |

### 1.5 工装固件上板

| # | 做什么 | 怎么算做完 | 来自哪 |
|---|---|---|---|
| 24 | **面板浏览器测试 `T4-02` 对真板子**（拆仓后主机侧和模拟板都过了） | `$PORTTOOL/TestCase/host/porttool_panel`：`python run.py --port <控制口>` 全部检查通过 | [决策 76](../docs/tables/DECISIONS.md) |
| 25 | **KNX `frames` 模式重试一次**：09-30 发出后板子不再应答，随即发现断电，分不清是断电还是卡死 | 面板里跑 `frames` 60 秒：不卡死，`crc_raw` 涨、`crc_bad=0` | [HARDWARE-FACTS.md](../docs/hardware/HARDWARE-FACTS.md)「KNX 接口」 |
| 26 | **KNX `loopback` 的 `bad` 一直涨**：总线有电（`bus=ok vcc=1`），每秒约 30 个 `bad`，`chars` 几乎不涨。线索（未核实）：工装 `porttool_knx.c` 捕获 RX 上升沿，而 RX 低有效，上升沿是脉冲结尾，见 [KNX-TP-DATA-LINK.md](../docs/modules/M3/KNX-TP-DATA-LINK.md) | 查清原因，方案 `station6-poweron*.json` 的 knx 步判过；或改判据并写明理由 | 2026-09-30 实测 |
| 27 | **每个端口逐个在真板子上跑过一轮**并记下结果 | 每个端口有一轮结果 | [问题去哪住](../maps/docs-migration/issues/MIG-09-where-do-defects-and-modules-live.md)（原 PORT-BRINGUP-PLAN） |
| 28 | **校准：工装 5 点测量 → 拟合 → 按 UID 存档 → 生成扇区 15 镜像**，确认生成 `calarea.bin`；**工站 10**：J-Link 只擦扇区 0–14 重烧，再写扇区 15 | 四路各 5 点、残差进报告；工站 10 走完后扇区 15 逐字节等于存档，bootloader 和 app 正常启动 | [校准哪些通道](../maps/per-board-calibration/issues/CAL-03-which-channels-and-what-correction-model.md)、[修正值怎么写进板子](../maps/per-board-calibration/issues/CAL-04-how-do-values-get-onto-the-board-and-survive-the-reflash.md) |

### 1.6 重发 0.1.3（上面全过之后）

| # | 做什么 | 怎么算做完 | 来自哪 |
|---|---|---|---|
| 29 | **实验室所有板子用 ST-Link 烧最新 bootloader**，发布说明写明「旧板子先用 ST-Link 烧新 bootloader」 | 每块板烧完走一遍第一次上传自动认领 | [决策 83](../docs/tables/DECISIONS.md) |
| 30 | **跑一遍 [CHK-B 发版验收](../docs/tables/ACCEPTANCE-CHECKLIST.md#chk-b--发版验收)**，然后重做产物：板卡包 tar.gz（`v0.1.3-dev`）；STM32Tools 里三个平台的 IAPTool 用 `$TOOL` `v0.1.3` 重编；索引里两处校验值和大小；照 IDE-15 的做法原地替换并重建 0.1.3 的 release 和 tag | CHK-B 全过；WSL 和 Windows 各从网上装一遍、编译、上传 | [决策 83](../docs/tables/DECISIONS.md)、[Linux / macOS 用户怎么拿到能运行的 IAPTool](../maps/arduino-examples-and-ide-flow/issues/IDE-15-how-do-linux-and-macos-users-get-an-executable-iaptool.md) |

---

## 2 · 不用板子、现在能做的

（无）

---

## 3 · 等外部

**一行两样：等什么 → 到了之后立刻做什么。**

| 在等 | 到了之后立刻做 | 来自哪 |
|---|---|---|
| **这台电脑的有线网口接回 10.32.2.x 网段**（KNX IP 网关 10.32.2.129 在那边） | 跑 [测试脚本能不能经 IP 网关直接收发组报文](../maps/knx-examples/issues/KEX-04-can-the-script-talk-through-the-ip-gateway.md)（探测脚本见 [KEX-04-findings.md](../maps/knx-examples/KEX-04-findings.md)），然后定 [用例怎么判、人做哪几步](../maps/knx-examples/issues/KEX-06-how-does-each-test-case-judge.md) | [KNX 例程按正规用法重写](../maps/knx-examples/map.md) |
| **德文审稿人**（用户 2026-10-03 定「德文审过才上线」） | 把 `strings.json` 的德文交给他审，审过后把 `de_reviewed` 改成 `true` | [英文和德文谁写、谁审、术语照什么](../maps/porttool-panel-languages/issues/LANG-06-who-writes-and-reviews-english-and-german.md) |
| **能接板子的 Linux / macOS 机器** | 定 [在哪几台真机上验、用例怎么写](../maps/porttool-on-linux-and-macos/issues/XPT-03-which-real-machines-and-what-the-test-case-is.md) | [工装在 Linux / macOS 上运行](../maps/porttool-on-linux-and-macos/map.md) |
| **一次示波器** | 量 DO 那颗 VNQ5160K-E 的 PWM 上限（到多少赫兹出不来，极窄 / 极宽占空比还出不出得来，数据手册查不到）；量 AO 在上电、复位、掉电那几毫秒的输出电流，有问题再请硬件工程师在 VIN 加下拉 | [问题去哪住](../maps/docs-migration/issues/MIG-09-where-do-defects-and-modules-live.md)、[AO 在上电和掉电时怎么落到确定值](../maps/iec-61131-2-factory-state/issues/IEC-05-ao-has-no-defined-state-at-power-up.md) |
| **台子上 AI 的接法定下来**（AI 硬件已正常：用户 2026-09-30 看过，AI2 输入 2 mA 读到 2.02–2.06 mA） | `$PORTTOOL/TestCase/host/porttool_panel/run.py` 里 `EXPECT["ain"]` 从 `either` 改回真实预期 | 用户 2026-09-30 |
| **DI 的硬件改好**（用户 2026-09-30：不接线读 `0xFF`，正常应是 `0x00`） | 接 24 V 激励测数字输入；`DI_Inputs` 文件头「不接 24 V 时全读 1 是板子正常」那句跟着改 | 用户 2026-09-30 |
| **硬件工程师用过工装之后的反馈** | 交给他之前先按当前源码重编工装固件、重打 `$PORTTOOL/Output/delivery/`（10-01 那包早于三种语言）。反馈到了：定五个通信口做不做「异常可恢复」（上位机从帧里看出断了、自己计时到恢复）、面板左边要不要按九个配置项分段（端口仍按板子分组）；恢复暂停的两张图 [工装面板的提示与功能核对](../maps/porttool-ui-audit/map.md)、[产线测试补齐](../maps/production-test-gap/map.md) | 用户 2026-09-16 定；[问题去哪住](../maps/docs-migration/issues/MIG-09-where-do-defects-and-modules-live.md)（原 `ISS-D1`、`ISS-D2`） |
| **硬件工程师回答 `ef1=` / `ef2=` 哪个电平算故障** | 把判据写进方案文件（判据和限值由他写，我方只报电平，决策 44）。2026-09-28 数据点：AO1 设 20 mA，端子开路和接 470 Ω（实出 19.83 mA）两种情况 EF1 都读 1 | 同上 |

---

## 4 · 优先级最低

| 待办 | 怎么算做完 | 来自哪 |
|---|---|---|
| **研究 MCUboot 可行性** | 能回答「换过去值不值」：app 空间损失多少，证书链 / 撤销 / 认领 / 物理在场这四样怎么补。⚠️ 整机没有外部 flash，第二个 slot 只能挤内部 flash 或放 SDRAM | 用户 2026-09-21 定：**这个版本不考虑** |
| **交接时那两个坏字节**：`[BOOT] millis=` 前固定多 `[` `0xC2`，在启动日志偏移 502（bootloader → app 交接处），11 次零偏差，功能无影响。已排除：收发器被关着、电荷泵没塌完、冷启动。2026-09-19 实测 app 运行时 PB10 为低，收发器确实关着，`[BOOT]` / `[NET]` 是电荷泵余电 | 用一个主动 `digitalWrite(RS232_EN_Pin, HIGH)` 的 sketch，看 `alive` 是否随之出现，区分「sketch 在跑但输出被挡」和「sketch 没跑」 | 原 WAITING-ON 最低优先级一节 |
| **`system/extras/postbuild.sh` 曾带 System 文件属性**，任何写入都被拒；2026-09-21 已在 live 和 repo 两边清掉 | 板卡包重装后如果又出现，查是哪一步带上的 | 2026-09-21 实施时撞上 |
