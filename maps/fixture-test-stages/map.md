# 工装六步测试

## Destination

工装各步（研发、功能、老化、安规、用户级功能；校准已并进研发测试，[决策 89](../../docs/tables/DECISIONS.md)、[决策 97](../../docs/tables/DECISIONS.md)）设计定稿：每个端口有哪些测试项、在哪些测试类型里出现、判据和标准值从哪来，每一步的进出条件。这张图只出设计，不写代码。

## Notes

- 前提见决策 89–99：六步和标准值来源（89）、校准精度 ±1 % FS（90）、继电器老化人工配次数（91）、总线判据（92）、第 6 步认领后恢复出厂（93、94）、中途停下整步重跑（96）、面板分测试库 / 配置 / 入口（97）、要改固件的四件事（98）
- 原先暂停的两张图「产线测试补齐」「工装面板的提示与功能核对」2026-10-17 已删：票已在这里答完或被面板改版取代，留下的未知并进下面「Not yet specified」
- 开票、关票、算前沿照 [图与票的约定](../MAP-AND-TICKET-CONVENTION.md)，票号前缀 `STG-`

## 全集

```
grep -o "^OK port=[a-z0-9]*" OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/caps_golden.txt | sort -u
```

这条命令列出的每个端口，在 [每个端口有哪些测试项](issues/STG-03-what-each-port-tests-at-each-level.md) 里要么有测试项，要么写明不测（RTC 不是测试项）。

## Decisions so far

- [第 6 步通过后怎么不按键恢复出厂](issues/STG-06-factory-reset-without-the-button.md)：ST-Link 擦掉 bootloader 和校准值区以外的全部 flash（决策 94）
- [第 2–6 步里每个端口跑哪些项、跑多久](issues/STG-04-which-level-and-how-long-in-stages-2-to-6.md)：不出固定表，用户在面板上配，记住上一次（决策 97）
- [面板怎么选测试类型、测试项和时长](issues/STG-10-how-the-panel-picks-stages-levels-and-durations.md)：五块布局，左边都是菜单，右上角「开始」才启动（决策 97；界面后由[决策 125](../../docs/tables/DECISIONS.md)改成研发测试和工装完整测试两块）
- [标准机和被测板之间接哪些线](issues/STG-02-what-the-reference-board-is.md)：DO↔DI 双向各 8 路、标准机 AO→AI2、标准机两路 AI 焊成电流档读 AO1/AO2、CAN 对 CAN、共地；AI1 的标准值由人工或仪器给。接法改由人在「标准机设置」里登记（决策 134、135）
- [每个端口有哪些测试项、判据和标准值从哪来](issues/STG-03-what-each-port-tests-at-each-level.md)：丢包率判 0、延时只记；速率下限等满速率回送做完实测取最低 × 0.8；DI 走位 8 拍只比 0 / 1；温度 0–60 °C
- [六步各自的进出条件](issues/STG-01-what-each-stage-needs-to-start-and-end.md)：一键跑某步失败后面不跑；ST-Link 用 `STM32_Programmer_CLI`；恢复出厂读出校准值、擦扇区 1–15、写回；第 6 步 demo 走 IAPTool
- [安规测试预留什么](issues/STG-09-what-the-safety-test-stage-reserves.md)：一张卡片，扫码录 SN、方案文件里的问卷（`safety.questions`）、人工合格 / 不合格；不对接 ERP
- [工装完整测试时逐板结果记在哪](issues/STG-08-where-per-board-results-go-in-a-full-run.md)：exe 旁边 `records/<UID>/`，一次一份 `ptreport` JSON，`progress.json` 记已过的步；停下记 `STOPPED`
- [Arduino demo 怎么讲工装协议](issues/STG-07-how-the-arduino-demo-speaks-the-fixture-protocol.md)：板卡包新例程 `FixtureDemo`，用板卡包 API 实现 `pt.id` / `pt.caps` / `pt.start` / `pt.stop` / `pt.echo`，含满速率回送；登记为跨仓镜像
- [第一台标准机怎么做出来](issues/STG-11-how-the-first-reference-board-gets-made.md)：DI、DO、AO 用本板自回环（自回环已由决策 135 取消），出错时人工逐个量定位；两路 AI 焊成电流档；CAN 板子不桥终端，USB-CAN 转换器自带 120 Ω
- [校准卡片上逐点的「过 / 不过」还留不留](issues/STG-12-per-point-tolerance-on-calibration-cards.md)：留着当参考，AI、AO 都按 ±1 % FS 标过 / 不过，不拦存档
- [校准除了残差，要不要再拦 k、b 本身](issues/STG-05-reject-a-board-on-k-and-b-themselves.md)：都不拦，只取最小二乘的 k、b，面板显示回归（决策 99）
- [面板改版之前，完整测试的第 2、4 步跑什么](issues/STG-13-what-stages-2-and-4-run-before-the-panel-redesign.md)：不做过渡方案，跟着面板改版（TODO-fixture 第 38 条）一起做
- [PC 怎么知道板子上烧了哪几路校准值、k 和 b 各是多少](issues/STG-23-how-the-pc-reads-the-calibration-on-the-board.md)：选 A：固件加只读的 `pt.cal`，原样报出校准值区，PC 用 `calarea.Decode` 解
- [标准机 AI1 焊成电流档，校准值区格式里 AI1 的单位写死是 mV](issues/STG-24-ai1-current-range-vs-cal-area-unit.md)：选 B：格式不动，AI1 的系数按登记的档位解释，档位记在 PC 存档里
- [AI / AO 档位登记跟着哪块板走](issues/STG-25-where-the-range-registration-is-kept.md)：选 A：按 UID 存，没登记过的板用产品默认（AI1 电压、AI2 电流、AO 0–20 mA）；默认档位已由决策 134 改为 AI1、AO1 电压，AI2、AO2 电流
- [选了时长时，各端口的测试项同时跑还是挨个跑](issues/STG-26-how-a-timed-stage-runs-its-items.md)：选 A：只测一次和要人回答的项先挨个跑，再让勾选端口的会话同时跑满时长，第一次不过就停；同一端口互斥的项只能选一个
- [制作标准机里「跑一遍功能测试」用哪套配置](issues/STG-27-what-config-make-reference-board-runs.md)：选 C：用功能测试配置；「标准机」选「不用」时，依赖标准机的项按 STG-11 换成自回环或人工，卡片上写明（自回环已由决策 135 取消）
- [改版后面板上的「方案」tab 怎么处理](issues/STG-28-what-happens-to-the-plan-tab.md)：选 A：页头保留「判据来自哪份方案」选择框；去掉面板里的方案编辑和运行，`porttool run` 命令行照旧
- [面板跑第 6 步还缺哪几样输入](issues/STG-14-what-the-panel-needs-to-run-stage-6.md)：bootloader 镜像随交付包放在 exe 旁边；上传和认领用交付包里的 IAPTool，按 Arduino IDE 上传的同一套参数；产线根用产线电脑上 IAPTool 的本机私钥（没有就生成，M2-ownership.md「用户第一次在 IDE 里上传」那条），板子出厂前恢复出厂，不带根；demo 和配置跟第 47、38 条走
- [报告里安规那一步的 `type` 填什么：STG-08 和 STG-09 写法冲突](issues/STG-15-report-step-type-for-the-safety-stage.md)：选 A：保持 `type` 填步号 5、`id` 填 `safety`，STG-09 那一句已改
- [完整测试时 SN 必须填吗](issues/STG-16-is-the-sn-required-in-a-full-run.md)：选 A：SN 可空，没扫码的板子按 UID 找记录
- [方案怎么同时驱动标准机（或上位机的 USB-CAN）当对端](issues/STG-18-how-a-plan-drives-the-reference-board.md)：面板接第二块板（标准机）作为第二条板子连接，测试项目录里标明哪一步在标准机上跑什么，方案文件的步骤加 `on: ref`；对端会话由执行器在被测板那一步之前启动、之后停止，沿用 deadman 续期；上位机做 CAN 对端用台子上现有的 CANable 2.0（SLCAN），Go 里实现驱动
- [方案里要人工填一个读数，用什么步骤](issues/STG-19-manual-reading-step-in-a-plan.md)：选 A：加人工填数的步骤，填的数走 `ptcheck` 判限值，报告留原始值
- [KNX 三项诊断没有判据，要不要算进 KNX 端口的结论](issues/STG-20-knx-diagnostics-in-the-port-verdict.md)：选 A：只记录的诊断不参与端口结论
- [KNX 直方图的格界抄进了面板文案](issues/STG-21-knx-histogram-bin-edges-in-panel-text.md)：选 B：面板文案去掉格界数字
- [`can_send.py` 的交互模式已经没有板端对象](issues/STG-22-can-send-interactive-mode-left-empty.md)：选 A：删掉 `can_send.py` 的交互模式，只保留 `Analyser`
- [RS232 就是控制口，「和上位机收发、加波特率」怎么做](issues/STG-17-rs232-is-the-control-port.md)：选 B：测 RS232 时控制口一起切波特率，测完切回，失联自动切回
- [DI 正交计数这一项，正交脉冲由谁送](issues/STG-29-who-feeds-quadrature-pulses-to-di.md)：选 A：标准机固件的 `dout` 加两路正交输出
- [demo 和工装固件的契约测试 T4-05 住哪个仓](issues/STG-30-where-the-demo-contract-test-lives.md)：选 A：T4-05 留在 `$PORTTOOL`，决策 78 的例外扩到 demo
- [AI2 读数、AO 输出选标准机当对端时怎么判](issues/STG-31-ai-ao-items-with-the-reference-board-as-peer.md)：选 A：标准机一侧按它自己的 k、b 自动给标准值（已做，PORTTOOL-FLOW C.3.2）；AI1 也能测，看登记里有没有接到它的标准机 AO（决策 134）
- [DO 带负载选人工时，问压降的时候输出已经关了](issues/STG-32-dout-load-manual-reading-while-output-is-on.md)：选 A：逐路开着输出等人填压降，并入决策 108 的 DO 手动输出卡片
- [DO 方波这一项判的是什么](issues/STG-33-what-the-dout-square-item-judges.md)：选 A：拆成 `dout.blink`（只在研发、人数翻转，决策 133）和 `dout.square`（PWM 人看示波器）
- [DO → 继电器 → 标准机 DI 这条链的两处细节](issues/STG-36-do-relay-chain-into-reference-di.md)：只比高 / 低；DO7、DO8 直接接标准机 DI7、DI8（决策 133）
- [工装测试里 AI1 读数怎么测；研发里一路不过、一路没填记什么](issues/STG-35-ai1-in-automated-tests-and-fail-plus-blank.md)：AI1 按决策 134 由同档的标准机 AO 测；多路每一路有自己的状态，没有整项结果
- [决策 137 实现时替用户选的几处细节](issues/STG-39-decision-137-details-picked-during-build.md)：照现在做；只有测试记录改成按板子 UID 分开存
- [决策 150 实现时替用户选的细节](issues/STG-43-decision-150-details-picked-during-build.md)：18 行都照现在做
- [`$PORTTOOL` 的命令允许列表要不要跟着新结构改](issues/STG-42-porttool-allow-list-after-the-move.md)：只删指向已删脚本的 4 条
- [决策 151、139 实现时替用户选的细节](issues/STG-40-decisions-138-139-details-picked-during-build.md)：按推荐；DI 逐路电平全没选也记「停下」、校准档位不一致不让开始、CAN 窗口删两边的「停止连发」，其余照现在
- [AO 带负载两路档位不同时，输出值怎么填](issues/STG-38-ao-load-one-value-two-ranges.md)：每路一个输出值
- [「多路每路一个结果」还覆盖哪几项](issues/STG-37-which-items-count-as-multi-channel.md)：按推荐，实时卡片、温度也每路一个状态
- [工装自动化测试里还剩的两处人答步骤怎么办](issues/STG-34-human-steps-left-in-the-automated-tests.md)：继电器按负载反馈判（决策 130、133）；安规留着，人工照现状
- 中途停下后从停下的那一步整步重跑，按 UID 记住已过的步骤（[决策 96](../../docs/tables/DECISIONS.md)）

## Not yet specified

- **安规测试的细节**：用户 2026-10-15「留着后期需求确定了再细化」，等需求
- **专业设备的对接接口**：用户 2026-10-09 说先预留，型号和接口都还不知道
- **标准机多久复核一次精度**：它自己也会漂，要等标准机怎么接定下来才问得清楚
- **「异常可恢复」怎么判**：做法已想好（上位机从帧里看出断了、自己计时到恢复），判据等测试项的判据定下来
- **失败码怎么生成**：倾向从「步骤 id + 字段 + 算子」自动生成，不维护码表、不带工站号；等硬件工程师反馈
- **对着《OPENPLC 生产测试指导文件》逐条核一遍差距**（`$HW/OPENPLC生产测试指导文件_V0.1_20260904.docx`，3.1–3.10 等）：硬件工程师反馈回来后做，只能人工对

## Out of scope

- ERP、SN、过站（决策 20）。安规那一步只答「预留什么」
