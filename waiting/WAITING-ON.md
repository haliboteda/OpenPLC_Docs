# 在等什么

**一行两样：等的是什么 → 到了之后立刻做什么。** 见 [../WHERE-THINGS-LIVE.md](../WHERE-THINGS-LIVE.md)。

这类东西的真实风险不是忘了记，**是条件到了没人想起来**。

| 在等 | 到了之后立刻做 | 来自哪张票 |
|---|---|---|
| **德文审稿人**：工装面板的德文译文由谁审（用户 2026-10-03 定「德文审过才上线」） | 把德文初稿交给他审，审过后在面板上打开 Deutsch | [英文和德文谁写、谁审、术语照什么](../maps/porttool-panel-languages/issues/LANG-06-who-writes-and-reviews-english-and-german.md) |
| **一次示波器** | 量 DO 那颗 VNQ5160K-E 的 PWM 上限：到多少赫兹出不来，极窄/极宽占空比还出不出得来。**数据手册查不到**；顺带量 AO 在上电、复位、掉电那几毫秒的输出电流（bootloader 把 PA4 / PA5 拉低之前、MCU 停了之后），量出来有问题再请硬件工程师在 VIN 加下拉（「AO 在上电和掉电时怎么落到确定值」，用户 2026-10-03 定先测再说） | [问题去哪住](../maps/docs-migration/issues/MIG-09-where-do-defects-and-modules-live.md)（原 DO-PWM-SCOPE-STEPS.md，该文件已删） |
| **台子上 AI 的接法定下来**（AI 硬件已正常：用户 2026-09-30 看过；AI2 输入 2 mA 读到 2.02–2.06 mA） | `$PORTTOOL/TestCase/host/porttool_panel/run.py` 里 `EXPECT["ain"]` 从 `either` 改回真实预期 | 用户 2026-09-30 |
| **DI 的硬件改好**（用户 2026-09-30：DI 要改硬件；不接线读 `0xFF`，正常应是 `0x00`。改好后 `DI_Inputs` 文件头「不接 24 V 时全读 1 是板子正常」那句要跟着改） | 再接 24 V 激励测数字输入 | 用户 2026-09-30 |
| **KNX 环回模式查清**（2026-09-30 总线已有电：`bus=ok vcc=1`；但 `mode=loopback` 每秒约 30 个 `bad`，`chars` 几乎不涨。线索（未核实）：工装 `porttool_knx.c` 捕获 RX 上升沿，而 RX 低有效，上升沿是脉冲结尾，见 [KNX-TP-DATA-LINK.md](../docs/modules/M3/KNX-TP-DATA-LINK.md)） | 方案里 knx 那一步才判得过 | 2026-09-30 实测 |
| **硬件工程师用过工装之后的反馈** | 决定「异常可恢复 / 失败码 / 面板分段」三条还做不做，**以及 `工装面板的提示与功能核对` 那张图剩的三张票**（面板逐卡片验收 / 这轮测哪些端口 / 端口列表怎么组织） | 用户 2026-09-16 定 |
| **硬件工程师回答 `ef1=`/`ef2=` 哪个电平算故障** | 把判据写进方案文件（判据和限值由他写，我方只报电平，见 DECISIONS 44）。2026-09-28 实测数据点：AO1 设 20 mA，端子开路和接 470 Ω（实出 19.83 mA）两种情况 EF1 都读 1 | 同上 |



## 最低优先级 · 交接时那两个坏字节，原因未知

`[BOOT] millis=` 前固定多两个字节 `[` `0xC2`，位置固定在启动日志偏移 502（bootloader→app 交接处）。
11 次测量零偏差。**功能无影响**，那行本身完整。

**已排除**（都是实测）：

| 假设 | 怎么测的 |
|---|---|
| 收发器被关着 | core 里先拉高 PB10 再打印 → 坏字节不变 |
| 电荷泵没塌完，DeInit 把 PC10 放浮空 | bootloader 里 `Disable_RX_RS232()` 后插 20 ms → 坏字节不变 |
| 冷启动会丢 | 真断电上电（POR）→ 照样出，逐字节相同 |

**2026-09-19 量过了，硬件事实文档没错。** app 跑起来时 `PB10` 实测为**低**
（`GPIOB_IDR` bit10 = 0，ST-Link 读的是引脚实际电平，不用万用表；同一读法在 bootloader 下读到高，
可作对照）。收发器确实是关断的 —— `[BOOT]` / `[NET]` 两行出得来是电荷泵余电，
而 sketch 自己每秒一次的 `IAP_PROBE_APP alive` **一行都没出来**。

⚠️ **还差一步才算坐实**：现在无法区分「sketch 在跑但输出被挡」和「sketch 根本没跑」。
要一个主动 `digitalWrite(RS232_EN_Pin, HIGH)` 的 sketch，看 `alive` 是否随之出现。
（ST-Link 直接写 `GPIOB_ODR` 更快，但写内存被权限策略拦下。）
