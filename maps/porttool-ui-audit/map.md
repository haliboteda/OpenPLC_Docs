# 工装面板的提示与功能核对 + 上板联调

⚠️ **2026-09-16 从工作区根的 `.scratch/` 搬进本仓。** 它在那里**不属于任何仓库、
完全不在版本控制下** —— 而它有两张还开着的票。票号加了 `PUI-` 前缀。

## Destination

**工装测试那套**（PortTool 固件 + 上位机面板）的每一处标签、提示、参数名、判据展示，都和真实硬件与固件对得上；工程师不查文档就知道「我要开 DO3 并设 PWM」该点哪里。终点是一份「改什么、为什么」的清单加上真板子逐端口联调验证过的记录。

## Notes

**域**：工装测试（PortTool）。固件在 `$BOOT/TestCase/porttool/`，上位机在 `$TOOL/internal/` 下 pt 开头的那几个包，判据在 `$PROD/docs/tables/TEST-CASES.md`。

**⛔ 不在域内**：bootloader / IAP 产品路径（`$BOOT/IAPServer/`、`IAPTool`）、Arduino 板卡包。

**权威链，不许倒过来用**（`~/.claude/rules/verify-dont-assume.md`）：

```
Hardware/ 的原理图 · netlist · Klemmblockzuordnung     ← 唯一出处
        ↓ 抄件
固件的 pt.caps（term= / terms=）
        ↓ 抄件
面板的标签
```

面板照实显示固件给的东西，**所以面板上的错不一定是面板的错**。

**每个会话先读**：`$PROD/docs/production/PORTTOOL-FLOW.md`（现状与取舍）、`$PROD/docs/tables/DECISIONS.md` 第 9–36 条、`$PROD/docs/hardware/HARDWARE-FACTS.md`、`$PROD/docs/tables/TEST-CASES.md`。

**这张图允许执行**：不只出决策，端子表和对照清单本身就是产出物。

## 全集

这张图的范围由这个决定，**关最后一张票之前重跑一遍对账**：

```
grep -l "term=" 在 $BOOT/TestCase/porttool/ 下每个 porttool_ 开头的 .c 里
```

⚠️ **补记于 2026-09-16 搬迁时。** 原图没有这一节 —— 它写在这条规矩成型之前。

## Decisions so far

⚠️ **这三行是 2026-09-16 搬迁时补的索引** —— 这几张票关在本仓约定成型之前，
当时没有「关票要在地图上留一行」这条规矩。摘要取自各票正文。

- [01 · 从硬件资料建立权威端子表](issues/PUI-01-terminal-map-from-hardware.md)：端子表以原理图 / netlist 为唯一出处建起来了，调查结果在 [01-findings.md](01-findings.md)
- [03 · 格子上到底印什么](issues/PUI-03-label-format.md)：标签格式已定

<!-- 一条闭合 ticket 一行 -->

- [从硬件资料建立权威端子表](issues/PUI-01-terminal-map-from-hardware.md)：四排 `Klemmblock A/B/C/D`（A、B 在 Lower Deck，C、D 在 Upper Deck）。**A 字母不全局唯一** —— 原理图里的字母是板内局部的，单写 `A08` 有歧义。`dout` 的 `A03-A10` 没撞号，是对的。顺带查出**硬件文档自身**（`Klemmblockzuordnung`、`Klemmenbezeichnungen-R` 都漏了 CAN_GND）和**固件三处** `term=` 抄错。
- [格子上印什么](issues/PUI-03-label-format.md)：**印功能名，不印端子号** —— `DO3` 而不是 `A05`。名字取自 `Klemmenbezeichnungen-R`，按用户习惯缩写（DO / DI / AI / AO / `Relay 1-6`），具名信号照抄（`RS485 A`、`CAN H`…）。连带：`term=` 不再是标签来源；RS485 端子号错误不再上屏。

- [面板全中文 + 改了参数就不给结论](issues/PUI-04-panel-wording-audit.md)：面板上人看的字一处英文不留（协议原文只留在日志窗和悬停里）；**参数一改，判据当场失效** —— 按钮改口成「按我改的参数跑（不出结论）」并说清差在哪，另给一键「恢复方案参数」。连带修掉「打字被下一帧抹掉」和「sd / rtc 说明是过期事实」。H5 加了两条断言守住。

- [按钮与模式的形状](issues/PUI-04-panel-wording-audit.md)：卡片头的「启动/停止」和「开始测试」**合并成「单发 / 连续」两个单选 + 一个「开始」**；枚举参数（≤4 个选项）改成一行一个的单选，**每项后面直接写它是干什么的**（出处是固件文件头的注释）。用户 2026-09-11 定：**「简洁」是指合并汇总，不是自动折叠** —— 同一件事只写一处，整块「怎么配」因此取消，四条分别并进按钮区 / 模式单选 / 参数框标题 / 「改了参数」那句。19 个端口的「接线 / 测什么 / 什么算对」已按这个标准全部重写。

## 权威（用户 2026-09-11 定）

- **MCU 管脚** → `Hardware/STM32H743IIK6_GPIO_ASSIGNMENT_Schaeffer_Bridge_20260822.xlsx`
- **对外端子** → `Hardware/Klemmenbezeichnungen-R.pdf`
- 发现硬件文档有错 → **报给用户，不自己改**（记在 `Hardware/CLAUDE.md`）
- ✅ 已定（用户 2026-09-11）：**C09=CAN_GND、C10=RS485 A、C11=RS485 B**。`Klemmenbezeichnungen-R` 从 09 号起错开一位，A08 的 "Digital Out 6" 也印错成 "Digital Out 3"。图纸不改，结论记在 `HARDWARE-FACTS.md`

## Not yet specified

- **各端口具体的 UI 问题清单** —— 要等 01 / 02 出来才分得清哪些是「标签指错了」、哪些是「用词看不懂」。现在写等于先把雾切成块。
- **`loop=ctrl` 端口那三个数怎么和读数分区展示** —— 原则已定（DECISIONS 9：它们不是该端口的判据），但面板上怎么排没定。
- **操作语义**：「重新启动」「停止」这些按钮在会话/一次性动作/交权三类端口上语义不一样，要不要统一措辞。
- **校准相关的 UI** —— 挡在 `ISS-C1`（校准值存板子哪里，等用户定）。
- **失败信息的可读性** —— 超时 vs 判定失败已经分开记（ptreport 的三条规矩），但面板上读起来够不够清楚没看过。

## Out of scope

- **DO 硬件 PWM（`src=hw`）改造** —— 那是固件能力问题（等示波器扫频结果），不是提示与交互问题。
- **缺激励导致测不了的端口本身**（din / ain / 编码器要接线，sd 要 FAT32 卡）—— 联调范围里会点名，但「怎么造激励」属于硬件准备，不是这张图要决定的。
- bootloader / IAP 产品路径的任何 UI。

- [02 · 固件 14 个 `term=` 声明逐条对硬件](issues/PUI-02-firmware-term-vs-hardware.md)：原状态写的是「关闭：已出本图范围」。**那是个范围判断，不是走过的一步**，所以记在这里而不是「Decisions so far」
