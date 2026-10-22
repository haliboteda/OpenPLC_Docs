# 待办 · 工装

**这一份记工装（`$PORTTOOL`、`$BOOT/TestCase/`）的待办；IAP 的在 [TODO.md](TODO.md)。** 只有这两份（[决策 85](../docs/tables/DECISIONS.md)）。准入、分节、做完删行的规矩和 TODO.md 相同，见 [../WHERE-THINGS-LIVE.md](../WHERE-THINGS-LIVE.md)。

> 每一条必须写明它是哪张已关的票（或哪条决策）产生的。写不出来的，写不进去。

- 编号沿用拆分前 TODO.md 里的号，不重排
- 台子接线核对（TODO.md 第 1 条）两边共用，只记在 TODO.md
- **目标是改版后的面板**（第 38 条）：只做它用得上的，不做改版前的过渡方案（用户 2026-10-11，[STG-13](../maps/fixture-test-stages/issues/STG-13-what-stages-2-and-4-run-before-the-panel-redesign.md)）
- **制作标准机不再是单独的测试类型**（[决策 128](../docs/tables/DECISIONS.md)，用户 2026-10-14：「实际上研发测试就是手动制造一个标准机」）：研发测试里校准、烧校准值、逐个端口手动测
- 只有一块板时，工装上板排在 IAP 释放板子之后；不上板的部分用模拟板（面板端口选 `sim`）

---

## 1 · 上板那天，按顺序做

演示那天照 [PORTTOOL-DEMO-ON-BOARD.md](../docs/engineering/PORTTOOL-DEMO-ON-BOARD.md) 做，它标了每步顺带做完这一节的哪几行。

### 1.1 动手准备

| # | 做什么 | 怎么算做完 | 来自哪 |
|---|---|---|---|
| 2 | **SD 卡要有能认的文件系统**（要求见 [PORTTOOL-DEMO-ON-BOARD.md](../docs/engineering/PORTTOOL-DEMO-ON-BOARD.md) 准备第 2 步）：上板时看 `sd.probe` 的 `fs` 确认 | 工装 `sd.probe` 的 `fs` 不是 `none`，`sd.integrity` 报 `identical=1` | [XPT-03](../maps/porttool-on-linux-and-macos/issues/XPT-03-which-real-machines-and-what-the-test-case-is.md) 的实测 |
| 48 | **第一台标准机焊 AI 电流档**：AIN1 桥 JP9 脚 1–2 + JP5 脚 2–3（由结构图推出，**焊前对原理图核实**，不可逆）；AIN2 同产品板默认 | 两路 AI 都能读电流；在「标准机设置」页登记成「AI1 电流、AI2 电流」（决策 135） | [第一台标准机怎么做出来](../maps/fixture-test-stages/issues/STG-11-how-the-first-reference-board-gets-made.md) |

### 1.2 工装固件上板

| # | 做什么 | 怎么算做完 | 来自哪 |
|---|---|---|---|
| 66 | **SD 文件传递上板**（[决策 120](../docs/tables/DECISIONS.md)，PORTTOOL-FLOW B.11）：烧当前工装固件（≥ 0.15.0），exFAT 卡；研发 SD 端口经网口、再经 USB 各写一个几百 KB 的文件 → 两行都过 → 列出、查看、存到电脑、删除 → 安全拔卡后插电脑能打开刚写的文件 | 两条线都写读通过；拔卡在电脑上看到的文件和原文件一样 | 决策 120 |
| 24 | **面板浏览器测试 `T4-02` 对真板子**（拆仓后主机侧和模拟板都过了） | `$PORTTOOL`：`go run ./TestCase/host/porttool_panel --port <控制口>` 全部检查通过 | [决策 76](../docs/tables/DECISIONS.md) |
| 25 | **KNX `frames` 模式重试一次**：09-30 那次发出后板子不应答、同时断了电，分不清是断电还是卡死 | 研发测试 KNX 的「收发整帧」卡片（一次开 60 秒，决策 105）：不卡死，`crc_raw` 涨、`crc_bad=0` | [HARDWARE-FACTS.md](../docs/hardware/HARDWARE-FACTS.md)「KNX 接口」 |
| 26 | **KNX `loopback` 的 `bad` 一直涨**：总线有电（`bus=ok vcc=1`），每秒约 30 个 `bad`，`chars` 几乎不涨。线索（未核实）：工装 `porttool_knx.c` 捕获 RX 上升沿，而 RX 低有效，上升沿是脉冲结尾，见 [KNX-TP-DATA-LINK.md](../docs/modules/M3/KNX-TP-DATA-LINK.md) | 查清原因，方案 `station6-poweron*.json` 的 knx 步判过；或改判据并写明理由 | 2026-09-30 实测 |
| 88 | **KNX 高级窗口上板 + 接 KNX USB 接口实测**（PORTTOOL-FLOW B.12、C.3.6「KNX 分析」、C.3.7）：烧工装固件 ≥ 0.17.0（KNX 分析窗口要的 `pt.set knx tx=` 从这版起有，[决策 120](../docs/tables/DECISIONS.md)；`$PORTTOOL/Output/fixture/`，交付包里叫 `openplc_fixture_<版本>.hex`）；KNX USB 接口和板子接同一条有电的 KNX 总线；连接区「KNX USB 接口」选上它；研发 KNX 端口勾「KNX 分析」点开始 → 板子发一条、电脑发一条 → 两边各连发 10 条再点「停止发包」→ 关窗再打开 → 结束这一项。Windows、Linux 各做一次（Linux 先给 `/dev/hidraw*` 加读写权限）；第 25 条一起看 | 两边发的都标「对上了」；电脑那栏写出接口名和用的 EMI，电脑发的确认是「成」；接口型号和 EMI 记进 [HARDWARE-FACTS.md](../docs/hardware/HARDWARE-FACTS.md)「KNX 接口」 | [决策 151](../docs/tables/DECISIONS.md) 第 8 条 |
| 27 | **每个端口逐个在真板子上跑过一轮**并记下结果 | 每个端口有一轮结果 | [问题去哪住](../maps/docs-migration/issues/MIG-09-where-do-defects-and-modules-live.md)（原 PORT-BRINGUP-PLAN） |
| 28 | **校准上板：四路各 3–6 点（决策 117） → 面板拟合出 k、b 存本地 → 点「烧进板子」写进扇区 15**（烧当前工装固件（≥ 0.18.0），经控制口 `pt.calw`，不要 ST-Link，[决策 142](../docs/tables/DECISIONS.md)）；之后只擦扇区 0–14 重烧 bootloader | 四路的回归和 k、b 在面板上显示并进报告；「烧进板子」回报读回一致、k、b 和存档一样，扇区 15 的根区和 metadata 烧前烧后一致（ST-Link 读回比）；重烧后扇区 15 的 k、b 不变，bootloader 和 app 正常启动 | [校准哪些通道](../maps/per-board-calibration/issues/CAL-03-which-channels-and-what-correction-model.md)、[修正值怎么写进板子](../maps/per-board-calibration/issues/CAL-04-how-do-values-get-onto-the-board-and-survive-the-reflash.md)、[决策 90](../docs/tables/DECISIONS.md)、[决策 97](../docs/tables/DECISIONS.md) |
| 41 | **ETH / USB 速率下限实测**（第 35 条做完后）：几块良品各跑一次满速率回送 | 实测最低值 × 0.8 写进方案文件 | [每个端口有哪些测试项](../maps/fixture-test-stages/issues/STG-03-what-each-port-tests-at-each-level.md) |
| 42 | **核实 `STM32_Programmer_CLI -d` 烧工装固件不碰扇区 15**：先在面板「烧进板子」写校准值（[决策 142](../docs/tables/DECISIONS.md)），再用 ST-Link 重烧工装固件 | 扇区 15 读回和烧之前一致 | [六步各自的进出条件](../maps/fixture-test-stages/issues/STG-01-what-each-stage-needs-to-start-and-end.md) |
| 50 | **核实 ST-Link 擦写的两处参数**：`-e` 擦扇区时 H743 第二个 bank 是不是按 8–15 编号；`-rst` 之后工装固件会不会重新跑起来（一次读 128 KiB 的 `-u` 只有烧校准值用，[决策 142](../docs/tables/DECISIONS.md) 后不用了） | 两项在真板上各看到一次，结果写进 `$PROD/docs/modules/M4/PORTTOOL-FLOW.md` C.3.5 | 第 43 条（主机上只用替身测过） |
| 54 | **FixtureDemo 在真板子上跑一遍**：用户级测试经 RS232 讲工装协议 | 面板对 demo 跑完第 6 步的测试；`fixture_board.cpp` 里的板卡包调用（引脚、裸 TCP、USB CDC、FDCAN 计数，以及决策 127 补的 PHY 读寄存器、固定 IP、SD 识别和读写、SDRAM 扫描、校准值区、AI 16 位读、控制口切波特率）各看到一次；第 6 步测 USB 时口 1 上没有 `[sys]` 日志行（demo 已 `OPENPLC_SYSTEM_LOG(OFF)`，PORTTOOL-FLOW A.9） | [Arduino demo 怎么讲工装协议](../maps/fixture-test-stages/issues/STG-07-how-the-arduino-demo-speaks-the-fixture-protocol.md)（T4-05 只在主机上比过） |
| 63 | **人代替标准机的卡片在真板子上点一遍**（决策 108、137）：研发测试 AI / AO / DI / DO 四张卡（研发全人工，决策 133）各块勾几路，手加信号、手量输出、填标准值 | DI 灯跟着手加的 24 V 变；AO 设 10 mA 表量到的和卡片偏差一致；DO「输出」时勾了的路端子有 24 V、「停止输出」后全没有；标准值的对错和偏差算得对 | [决策 108](../docs/tables/DECISIONS.md)、[STG-32](../maps/fixture-test-stages/issues/STG-32-dout-load-manual-reading-while-output-is-on.md) |
| 65 | **CAN 分析窗口在真板子上用 CANable 走一遍**（[决策 111](../docs/tables/DECISIONS.md)）：先烧当前工装镜像（≥ 0.14.0）（加了 `can mode=bus`），研发测试 CAN 勾「CAN 分析（高级窗口）」开始；让板子发、分析器发各一帧，再换一次波特率 | 两个方向都标「对上了」、换波特率后照样对上；拔掉 CAN 线时标「没收到」、板子最近一次错误写「没有节点应答」 | 决策 111；模拟板只验过面板这头的假线（PORTTOOL-FLOW C.3.7） |
| 68 | **继电器开合上板**（第 67 条做完后）：烧当前工装固件（≥ 0.17.0），照 [PORTTOOL-DEMO-ON-BOARD.md](../docs/engineering/PORTTOOL-DEMO-ON-BOARD.md) 第 5 步走：并行、串行各一次，吸合 / 断开时长不同 | 触点上接负载（[决策 130](../docs/tables/DECISIONS.md)），研发人工时人数负载实际开合次数填入、和设定次数一致；跑满自己停在断开；串行时一路跑满下一路才开始 | [决策 123](../docs/tables/DECISIONS.md)、决策 130 |
| 45 | **逐板记录走一遍**（第 46 条做完后）：一块板跑完整测试，扫 SN | `records/<UID>/` 里有这次的报告，按 SN 搜文件名能找回 | [逐板结果记在哪](../maps/fixture-test-stages/issues/STG-08-where-per-board-results-go-in-a-full-run.md)、PTG-01 |
| 76 | **#76 工装一侧：同板同输入用工装固件读 AI1**（IAP 窗口请求，用户 2026-10-15 定由工装窗口读）：板子 UID 393939383432510300390029，AI1 接 10 V；先用 ST-Link 读出扇区 0–1、15 留底 → 烧工装固件 → 读 AI1 原始值、按 `aiNominal` 换算 mV → 写回扇区 0–1（工装镜像会盖掉 bootloader）、比对扇区 15 | 数补进 [TODO.md](TODO.md) 第 76 条或回给 IAP 窗口；板子恢复原样 | [TODO.md](TODO.md) 第 76 条 |
| 83 | 进度：2026-10-15 全部做完，等上板（DO7、DO8 按 [STG-36](../maps/fixture-test-stages/issues/STG-36-do-relay-chain-into-reference-di.md) 直接接标准机 DI7、DI8）：DO 逐路走、继电器由标准机 DI 数次数（上位机数，去抖两帧），selfcheck 在模拟板上过、T4-05 指 `$CORE_LIVE` 过。**按决策 133 改**：先改 PORTTOOL-FLOW，再改面板：研发测试去掉标准机 / 专业设备（含 AI / AO 标准机校准 `/api/analog/calref`）；工装完整测试 DO、继电器走「DO → 继电器 → 标准机 DI」一条链，先测 DO（继电器吸合）再测继电器（DO 持续高），失败提示单独检查 DO、继电器；T4-02 跟着改 | T4-02 在模拟板上过 | [决策 133](../docs/tables/DECISIONS.md)、[STG-36](../maps/fixture-test-stages/issues/STG-36-do-relay-chain-into-reference-di.md) |
| 43 | **面板接上第 6 步**：**剩接真板子时在面板上点一次第 6 步**。已有并在替身上测过：ST-Link 三种操作（烧 bootloader 擦扇区 0–14、恢复出厂、烧校准值）和第 6 步的顺序（`src/stlink`、`src/ptstages`）；输入按[决策 103](../docs/tables/DECISIONS.md)（`ptstages.Stage6`，成功、上传失败、测试失败、恢复出厂失败四种）：交付包 `stage6/` 带 bootloader 镜像和 IAPTool，上传用 IDE 的 `IAPTool cdc <demo.bin> <口>`，产线根是本机私钥（[PORTTOOL-FLOW.md](../docs/modules/M4/PORTTOOL-FLOW.md) C.3.5）；demo 例程 `FixtureDemo`（A.9，T4-05），`.bin` 已进交付包；面板（`src/ptpanel/full.go`，L5）：exe 旁 `stage6/` 里 bootloader、IAPTool、`FixtureDemo.ino.bin` 齐且控制口不是模拟板时第 6 步可勾，缺了灰掉并列出缺的文件 | 面板上能点第 6 步；`T4-02` 过 | [六步各自的进出条件](../maps/fixture-test-stages/issues/STG-01-what-each-stage-needs-to-start-and-end.md)、决策 94、96 |
| 89 | **AO 设 0 关缓冲上板**（[决策 152](../docs/tables/DECISIONS.md)）：烧当前工装固件，AO1 电流档端子接 470 Ω；设 0 → 设 10 mA → 再设 0；板卡包 `openplcWriteAO_mA` 同样走一遍；之后删掉 STG-41 列的临时诊断代码，板子写回 `E:/tmp/flash-backup/full_flash_uid0029_before_aodiag_20261016.bin`（整片 2 MB，烧诊断固件前读的）还给 IAP | 两次设 0 时电阻两端都约 0.5 mV，10 mA 时约 4.7 V；板卡包同样 | [STG-41](../maps/fixture-test-stages/issues/STG-41-where-does-the-ao-noise-come-from.md)、决策 152 |

---

## 2 · 不用板子、现在能做的

| # | 做什么 | 怎么算做完 | 来自哪 |
|---|---|---|---|
| 86 | **用暗号自动选端口**（[决策 146](../docs/tables/DECISIONS.md)）：先写进 PORTTOOL-FLOW，再给工装固件加「报告各端子收到了什么」、PortTool 加「自动识别」；收不到的端子退回手选，手选时可拔插识别 | 模拟板上自动识别把 RS232、RS485、CAN 都对上；拔掉一个转接头时该端子退回手选 | [决策 146](../docs/tables/DECISIONS.md)、[IDE-19](../maps/arduino-examples-and-ide-flow/issues/IDE-19-tell-serial-ports-apart.md) |

---

## 3 · 等外部

**一行两样：等什么 → 到了之后立刻做什么。**

| 在等 | 到了之后立刻做 | 来自哪 |
|---|---|---|
| **德文审稿人**（审前也上线，决策 82） | 把 `strings.json` 的德文交给他审，审过后把 `de_reviewed` 改成 `true`，菜单里的「（未审）」随之去掉 | [英文和德文谁写、谁审、术语照什么](../maps/porttool-panel-languages/issues/LANG-06-who-writes-and-reviews-english-and-german.md) |
| **能接板子的 Linux / macOS 机器** | 定 [在哪几台真机上验、用例怎么写](../maps/porttool-on-linux-and-macos/issues/XPT-03-which-real-machines-and-what-the-test-case-is.md) | [工装在 Linux / macOS 上运行](../maps/porttool-on-linux-and-macos/map.md) |
| **台子上 AI 的接法定下来**（AI 硬件已正常：用户 2026-09-30 看过，AI2 输入 2 mA 读到 2.02–2.06 mA） | `$PORTTOOL/TestCase/host/porttool_panel/sweep.go` 里真板子上 `ain` 的预期从 `either` 改回真实预期 | 用户 2026-09-30 |
| **硬件工程师用过工装之后的反馈** | 交给他之前先把上位机版本升到 0.18.2（0.18.1 打包后又加了失败码和断开恢复，决策 120：源码变了版本不变会被拒），再 `$PORTTOOL/tools/build.sh all` 重打 `Output/delivery/`（现在那包的 `stage6/FixtureDemo.ino.bin` 也早于 demo 协议版本升到 0.18.1）。反馈到了：定五个通信口做不做「异常可恢复」（上位机从帧里看出断了、自己计时到恢复）；原先暂停的两张图（已删）的问题已并进 [工装六步测试](../maps/fixture-test-stages/map.md)；顺带确认交付包 `start.cmd` 选 1 能在标准安装位置找到 STM32CubeProgrammer（2026-10-20 修过那三条路径，本机没装在标准位置、没实测） | 用户 2026-09-16 定；[问题去哪住](../maps/docs-migration/issues/MIG-09-where-do-defects-and-modules-live.md)（原 `ISS-D1`、`ISS-D2`） |
| **AO 电压档电路调到 0–10 V**（现在约 0–2.5 V，[HARDWARE-FACTS.md](../docs/hardware/HARDWARE-FACTS.md)「模拟输出 AOUT1 / AOUT2」） | 按新电路改 AO 电压档的标称公式（现在是端子电压 = DAC 脚电压，`$PORTTOOL/src/ptlib/analog.go` 的 `aoMV`），改 HARDWARE-FACTS 那一节 | [决策 134](../docs/tables/DECISIONS.md)「量程目标」 |
| **硬件工程师回答 `ef1=` / `ef2=` 哪个电平算故障** | 把判据写进方案文件（判据和限值由他写，我方只报电平，决策 44）。2026-09-28 数据点：AO1 设 20 mA，端子开路和接 470 Ω（实出 19.83 mA）两种情况 EF1 都读 1 | 同上 |
| **用户定板卡包剩下的编译 warning 动不动**（2026-10-20 `--warnings all` 编 FixtureDemo / AO_Outputs 时看到） | `OpenPLC_IAP/src/uecc/curve-specific.inc:544` 未用参数：micro-ecc 是拷进来的第三方库，`$BOOT/IAPServer/uecc/` 有镜像，要两边一起改；`OpenPLC_KNX.cpp:73、87`、`knx_nvm.cpp:36` 的结构体 `= {0}`：改 `= {}` 即可，KNX 例程没编过确认 | 2026-10-20 编译输出 |

---

## 4 · 优先级最低

（无）
