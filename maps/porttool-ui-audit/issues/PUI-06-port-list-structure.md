# 06 · 端口列表怎么组织

Type: grilling
Opened: 2026-09-13
Status: open
Blocked by: -

⚠️ 原状态附注：2026-09-13 重写过，原文写于 09-11，三分之一是过期事实，已改准。

## Question

面板左边那张列表把 18 个东西列成「端口」，但它们**不是一类东西**，而用户的心理模型是「接口」。列表该怎么组织？

起因是用户 2026-09-11 的原话：**「pwm 应该是 do 里面的一项，soak 也是一个针对某个接口的测试项。」**

---

## 现状（2026-09-13 核实）

**不是平铺，已经按板子分组。** `renderTree()`（`$TOOL/internal/ptpanel/web/index.html:1342`）按固件报的 `board=` 分成四组，顺序写死在 `const order = ["bridge","upper","lower","junction","whole"]`。

`pt.caps` 报 `ports=18`（`$TOOL/TestCase/host/porttool_caps/caps_golden.txt`）：

| board | 端口 |
|---|---|
| `bridge` | `eth` `led` `rtc` `sd` `sdram` `usb` |
| `upper` | `ain` `aout` `can` `din` `knx` `rs232` `rs485` |
| `lower` | `dout` `pwm` `relay` `temp` |
| `whole` | `bringup` |

`kind=` 三类：`session` 12 个、`run` 3 个（`led` `rtc` `sdram`）、`handover` 2 个（`bringup` `pwm`）。

## 用户当初那句话，核实结果

| 用户的判断 | 代码实际 | 结论 |
|---|---|---|
| **pwm 是 do 里的一项** | ✅ **成立。** `pwm` 不是端口 —— 它是**交权目标**（`porttool_handover.c（已删）:68`），描述 `"breathing LED on Digital Out 6"`，端子 `A08`（= DO6），标 `HANDOVER_OWN_ROW` 所以在 caps 里单占一行 | **还没做** |
| **soak 是针对某个接口的测试项** | ✅ **成立，而且已经按这个改完了。** 见下 | ✅ **已解决** |

## ✅ 已解决：持久化测试（2026-09-12）

用户 2026-09-11 的原话：「如果是持久化测试的话，左侧菜单有个持久化的菜单，然后里面可以选对哪些端口进行持久化。」

**做出来的形状和当初设想的不一样，但解决的是同一件事**，用户已验收：

- **`soak` 端口整个删掉** —— `porttool_soak.c` 不再存在，固件 0.9.0 → 0.10.0
- **不另开菜单**，改成：端口行上每个 `kind=session` 带一个复选框（`picked2`），勾几个一起跑；卡片上「**单次 / 持续**」两个单选 + 时长（1/2/3/4 小时 / 一直）
- **计时和判定都在上位机**（`$TOOL/internal/ptpanel/hold.go`），板子只发数据；`pt.hold` 续期式看门狗到期 `stop_all()` + 点故障灯
- **判据不分叉** —— 持续跑不给结论（「不自动给结论 —— 老化、调波形、量电压用」），判据仍只有 `internal/ptcheck` 一份

⚠️ `soak` 这个词在固件里还剩三个**交权目标**（`can.soak`、`sd.integrity.soak`、`sdram.retention.soak`，都是 `HANDOVER_ON_PORT_ROW`，挂在各自端口行上）。**它们不是端口，不在这张 ticket 的范围里。**

---

## 还要定的三件

### 1. 分组维度 —— ✅ 已定（用户 2026-09-13）：**按板子，不改**

保持现状：按 `board=` 分成 Bridge / Upper Deck / Lower Deck / 整板四组。

**理由**：按接口类型分要新增一份「端口 → 接口类型」映射，固件不报这个字段 —— 要么写死在面板侧（抄件，会漂），要么改固件 caps 契约。代价不值。

下面两条是当时的备选，**不要重开**：乙 = 按接口类型；丙 = 接口类型为主、板子印行尾。

| | 主轴 | 好在哪 | 差在哪 |
|---|---|---|---|
| 甲 | **板子**（现状） | 和硬件堆叠一致；出处是固件的 `board=`，不用在面板侧编表 | 工程师找「我要开 DO3」时不知道 DO 在哪一层 |
| 乙 | **接口类型** | 和人要做的事一致 | 分类表**只能住在面板侧**，是抄件 —— 加端口的人得回来改它 |
| 丙 | 接口类型为主，板子印在行尾当副信息 | 两边都照顾到 | 行变长；仍有抄件问题 |

⚠️ **乙和丙都要新增一份「端口 → 接口类型」的映射**。固件现在不报这个。要么面板侧写死（抄件，会漂），要么固件 caps 加一个字段（改固件 + 改 caps 契约 + 改 `caps_golden.txt`）。**这是这条真正的代价，先定要不要付。**

### 2. `pwm` 收进 `dout` 卡片之后怎么说清

两者用途不同，收进同一张卡要能分辨：

- **`dout` 会话的逐路软件 PWM** —— 八路独立频率，每路一个 32 位相位累加器，可设 duty/freq，**跑完能回来**
- **`pwm` 交权目标** —— 单路呼吸灯，只驱动 DO6，**去不回来**

⚠️ `pt.handover pwm` 和 `dout` 端口**抢 PA9**（Digital Out 6）。交权前会先停所有会话，所以不打架。

### 3. 交权「去不回来」在 UI 上说清了没有

`pt.handover` 不返回（`porttool_handover.h（已删）:11`：“Handing over is one-way”；`DECISIONS.md` 第 13 条把面板上给它按钮叫做“放一个自杀键”），对面板前的人意味着「点了就得重启板子」。现在列表里这类端口显示「👁 人工判」（`portStatus()`，`index.html:1336` 附近），**但没有任何地方写「点了回不来」**。

---

## 已经定了、不要重开的

- **A08 就是 Digital Out 6**（用户 2026-09-11 确认 `Klemmenbezeichnungen-R` 从 09 号起印错一位）。固件描述是对的，图纸不改。结论在 `$PROD/docs/hardware/HARDWARE-FACTS.md`
- **一块硬件只占一行**：一次性动作和交权入口共用同一颗芯片时，交权那几个挂到该行的 `targets=` 上（`$PROD/docs/tables/DECISIONS.md` 第 17 条，详见 `PORTTOOL-FLOW.md:469`）
- **不要和 [03](PUI-03-label-format.md) 一起做** —— 03 改的是印什么字，这张改的是卡片怎么排

## 怎么算答完

⚠️ **这张票搬进来时没有这一节**（2026-09-16 之前的写法不要求）。开工前先补上再动手。

