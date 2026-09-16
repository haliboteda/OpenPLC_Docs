# 01 · 从硬件资料建立权威端子表 —— 调查结果

调查日期：2026-09-11
调查范围：只读 `Hardware/`。固件 / 面板 / Arduino core / `.ioc` 只用于交叉验证，不当出处。
本次**没有修改任何项目文件**。

出处路径全部相对 `E:\WorkSpace\Schaeffer-AG\`。

---

## 0. 三句话结论

1. **对外螺钉端子一共四排**，全部命名为 `Klemmblock A / B / C / D`。A、B 在 **Lower Deck**，C、D 在 **Upper Deck**。Bridge 和 Junction Link **没有任何螺钉端子**。
2. **`A01–A12` 和 `C01–C12` 不是同一批端子。** 字母含义取决于你看的是哪一份文件：产品级文档（`Klemmblockzuordnung` / `Klemmenbezeichnungen`）里 A = Lower Deck 数字量输出排；KiCad 原理图里字母是**板内局部**的，Upper Deck 自己把 C 排叫 "UD Klemmblock A"。所以**光写 `A08` 是有歧义的**，必须带板名或 Klemmblock 全局字母。
3. **`Klemmblockzuordnung` 的 C09–C11 是错的**，漏掉了 `CAN_GND` 这个端子。以网表为准：**C09 = CAN_GND、C10 = RS485 A、C11 = RS485 B、C12 = GND**。固件 `porttool_rs485.c` 抄的是错的那一版。

---

## 1. 对外端子一共几排、在哪块板、哪个连接器

| Klemmblock | 板 | 端子数 | 物理连接器（位号） | 连接器型号 | 间距 | 功能 | 出处 |
|---|---|---|---|---|---|---|---|
| **A** | Lower Deck | 16（01–16） | `X4`(01–04) `X3`(05–08) `X2`(09–12) + `X1`(13–16) | `5TS350S-381N04ELB-01` ×3；`5TS508S-129N04ELB-01` ×1 | 3.50 mm / 5.08 mm | Digital Out 1–8 + GND + 12/24 V 电源输入 | [`Hardware/Production/LowerDeck/bom.csv:23-24`](../../../Hardware/Production/LowerDeck/bom.csv)、[`netlist.ipc:75-90`](../../../Hardware/Production/LowerDeck/netlist.ipc)、[`positions.csv`](../../../Hardware/Production/LowerDeck/positions.csv) `X1..X4` |
| **B** | Lower Deck | 12（01–12） | `X8`(01–03) `X7`(04–06) `X6`(07–09) `X5`(10–12) | `5TS508S-129N03ELB-01` ×4 | 5.08 mm | Relais Out 1–6 触点 | 同上 `bom.csv:25`、`netlist.ipc:63-74` |
| **C** | Upper Deck | 12（01–12） | `J9`(01–04) `J10`(05–08) `J11`(09–12) | `5TS350S-381N04ELB-01` ×3 | 3.50 mm | +5V / GND / KNX / RS232 / CAN / RS485 | [`Hardware/Production/UpperDeck/bom.csv:15`](../../../Hardware/Production/UpperDeck/bom.csv)、[`netlist.ipc:245-256`](../../../Hardware/Production/UpperDeck/netlist.ipc) |
| **D** | Upper Deck | 17（01–17） | `J1`(01–04) `J2`(05–08) `J3`(09–12) `J4`(13–17) | `5TS350S-381N04ELB-01` ×3 + `5TS350S-381N05ELB-01` ×1 | 3.50 mm | Digital IN 1–8 + Analog IN/OUT + GND | 同上 `bom.csv:15-16`、`netlist.ipc:208-212, 215-218, 235-238, 439-442` |

**不是螺钉端子、但也对外的接口**：

| 接口 | 板 | 位号 | 出处 |
|---|---|---|---|
| RJ45 10/100M | Bridge | **`J4`** | [`Hardware/Production/Bridge/1436_01_SCHAE-BR.xlsx`](../../../Hardware/Production/Bridge/1436_01_SCHAE-BR.xlsx) 第 21 行；`1436_01_SCHAE-BR.pdf` 第 3 页 |
| USB-C（仅 Device） | Bridge | **`J5`** | 同 xlsx 第 22 行；`1436_01_SCHAE-BR.pdf` 第 4 页 |
| microSD | Bridge | **`J6`** | 同 xlsx 第 23 行；`1436_01_SCHAE-BR.pdf` 第 4 页 |
| JTAG/SWD 10pin | Bridge | **`J7`**（Samtec FTSH-105） | 同 xlsx 第 24 行；`1436_01_SCHAE-BR.pdf` 第 5 页 |
| DIN 导轨扩展口（Hutschienenverbinder）20pin | Junction Link | **`J4`**（Samtec ERF8-010-01-L-D-EM2-TR） | [`Hardware/Production/JunctionLink/bom.csv:11`](../../../Hardware/Production/JunctionLink/bom.csv)、[`netlist.ipc:79-102`](../../../Hardware/Production/JunctionLink/netlist.ipc) |

**板间连接器（不对外，别当端子用）**：Bridge `J1`(2×16)/`J2`(2×15)/`J3`(2×15) ↔ Upper Deck `J7`/`J6`/`J8`；Upper Deck `J5`(2×22) ↔ Junction Link `J3`；Junction Link `J1`(2×8)/`J2`(2×3) ↔ Lower Deck `J1`/`J2`。出处：[`Hardware/Hardware_overview.txt:48-61`](../../../Hardware/Hardware_overview.txt)，与各板 BOM 位号一致。

> ⚠️ **Lower Deck 的螺钉端子位号是 `X1–X8`，不是 `J*`。** Lower Deck 的 `J1`/`J2` 是通到 Junction Link 的板间连接器。

---

## 2. 端子总表

### 排号怎么定出来的

网表 `netlist.ipc` 的每条 `317`/`327` 记录带焊盘的 X/Y 坐标。同一排端子 X 相同、Y 等间距，按 Y 排序就得到物理顺序。方向用 **Klemmblock D 定标**：按 Y 排出来的 17 个位置与 `Klemmblockzuordnung.pdf` 第 4 页的 D01–D17 **逐条一致（17/17）**，所以方向是对的；A、B、C 三排用同一个方向读。

### Klemmblock A —— Lower Deck，数字量输出 + 电源输入

| 端子 | 功能 | MCU 引脚 | 连接器-脚 | 网络名 | 出处 |
|---|---|---|---|---|---|
| A01 | GND | — | X4-4 | `GNDD` | `LowerDeck/netlist.ipc:78` |
| A02 | GND | — | X4-3 | `GNDD` | `:77` |
| A03 | **Digital Out 1** | PB13 (tim1-ch1n) | X4-2 | `DIG_OUT_1` | `:76`；引脚见 `Klemmblockzuordnung.pdf` p3 |
| A04 | **Digital Out 2** | PB0 (tim1-ch2n) | X4-1 | `DIG_OUT_2` | `:75` |
| A05 | **Digital Out 3** | PH15 (tim8-ch3n) | X3-4 | `DIG_OUT_3` | `:82` |
| A06 | **Digital Out 4** | PE4 (tim15-ch1n) | X3-3 | `DIG_OUT_4` | `:81` |
| A07 | **Digital Out 5** | PA8 (tim1-ch1) | X3-2 | `DIG_OUT_5` | `:80` |
| A08 | **Digital Out 6** | PA9 (tim1-ch2) | X3-1 | `DIG_OUT_6` | `:79` |
| A09 | **Digital Out 7** | PI7 (tim8-ch3) | X2-4 | `DIG_OUT_7` | `:86` |
| A10 | **Digital Out 8** | PE5 (tim15-ch1) | X2-3 | `DIG_OUT_8` | `:85` |
| A11 | GND | — | X2-2 | `GNDD` | `:84` |
| A12 | GND | — | X2-1 | `GNDD` | `:83` |
| A13 | GND（电源） | — | X1-4 | `GNDD` | `:90` |
| A14 | GND（电源） | — | X1-3 | `GNDD` | `:89` |
| A15 | +12/+24 V（电源输入） | — | X1-2 | `/24VIN` | `:88` |
| A16 | +12/+24 V（电源输入） | — | X1-1 | `/24VIN` | `:87` |

**三份硬件文件一致**：`LowerDeck/netlist.ipc`、`Klemmblockzuordnung.pdf` 第 3 页 / `.ods` sheet "Lower Deck" R3–R18、`OpenPLC_LowerDeck_R3.pdf` 第 1 页（图上标 "LD Klemmblock A"，A01–A16）。

**DO*n* ↔ HSFET*n* 是一一对应的，已核实**（不是靠名字猜的）：
- 高侧开关是 `U4`(DO1–4) / `U3`(DO5–8)，型号 `VNQ5160K-E`（`LowerDeck/bom.csv:21`）。
- 输入侧 `HIGHSIDE_FET1..8` 经 EMI 滤波 `U6`/`U5`（`EMI7204MUTAG`）变成 `HSIDE_FETn_EMI` 进 `U3`/`U4` 的 INPUT 脚。
- 在封装上按焊盘 X 坐标比对：`U4-9`(INPUT4)=`HSIDE_FET1_EMI` 的 X≈038108，和 `DIG_OUT_1` 的输出焊盘 X（038423–039053）同一列；逐列比下来 FET1↔OUT1 … FET8↔OUT8 全部对齐。
- 出处：`LowerDeck/netlist.ipc` 中 `U3`/`U4`/`U5`/`U6` 的 `327` 记录。
- 旁证：Upper Deck 顶层图的网络名直接写成 `HIGHSIDE_FET1_PB13`、`HIGHSIDE_FET2_PB0` …（`OpenPLC_UpperDeck_R3.pdf` 第 1 页），与上表 MCU 引脚栏完全吻合。

### Klemmblock B —— Lower Deck，继电器触点

| 端子 | 功能 | 驱动引脚 | 连接器-脚 | 网络名 | 出处 |
|---|---|---|---|---|---|
| B01 / B02 | **Relais Out 1** A / B | PI8 | X8-1 / X8-2 | `RYOUT-1A` / `RYOUT-1B` | `LowerDeck/netlist.ipc:63-64` |
| B03 / B04 | **Relais Out 2** A / B | PI10 | X8-3 / X7-1 | `RYOUT-2A` / `RYOUT-2B` | `:65-66` |
| B05 / B06 | **Relais Out 3** A / B | PI11 | X7-2 / X7-3 | `RYOUT-3A` / `RYOUT-3B` | `:67-68` |
| B07 / B08 | **Relais Out 4** A / B | PG7 | X6-1 / X6-2 | `RYOUT-4A` / `RYOUT-4B` | `:69-70` |
| B09 / B10 | **Relais Out 5** A / B | PG3 | X6-3 / X5-1 | `RYOUT-5A` / `RYOUT-5B` | `:71-72` |
| B11 / B12 | **Relais Out 6** A / B | PD3 | X5-2 / X5-3 | `RYOUT-6A` / `RYOUT-6B` | `:73-74` |

### Klemmblock C —— Upper Deck，现场总线 ⚠️ 这排有文档冲突

**以网表和 KiCad 原理图为准**（两者一致）：

| 端子 | 功能 | MCU 引脚 | 连接器-脚 | 网络名 | 出处 |
|---|---|---|---|---|---|
| C01 | **+5 V** | — | J9-4 | `+5V` | `UpperDeck/netlist.ipc:256` |
| C02 | **GND** | — | J9-3 | `GNDD` | `:255` |
| C03 | **KNX +** | 不是 GPIO，接 STKNX `U9` 的 `KNX_A`(11 脚) | J9-2 | `KNX+` | `:254` |
| C04 | **KNX −** | 不是 GPIO，接 `U9` 的 `KNX_B`(12 脚) | J9-1 | `KNX-` | `:253` |
| C05 | **RS232 TxD** | PB10 (usart3-tx) | J10-4 | `RS232_TXD` | `:248` |
| C06 | **RS232 RxD** | PC11 (usart3-rx) | J10-3 | `RS232_RXD` | `:247` |
| C07 | **CAN L** | PB9 (fdcan1-tx) | J10-2 | `CAN_L` | `:246` |
| C08 | **CAN H** | PI9 (fdcan1-rx) | J10-1 | `CAN_H` | `:245` |
| **C09** | **CAN_GND**（CAN 隔离侧地，与 `GNDD` 分开） | — | **J11-4** | `CAN_GND` | **`:252`** |
| **C10** | **RS485 A** | PD6 (usart2-rx) / PD5 (usart2-tx) | **J11-3** | `RS485_A` | **`:251`** |
| **C11** | **RS485 B** | 同上 | **J11-2** | `RS485_B` | **`:250`** |
| C12 | **GND** | — | J11-1 | `GNDD` | `:249` |

其余不占端子的控制信号：`Enable RS232` = PC10、`Richtung RS485`(方向) = PD4、`KNXVCC_OK` = PH12、`KNX_OK` = PD7、`KNX_Prog_KEY` = PG9、`KNX_Prog_LED` = PG11。出处：`Klemmblockzuordnung.pdf` 第 4 页右栏、`OpenPLC_UpperDeck_R3.pdf` 第 1 页网络名。

### Klemmblock D —— Upper Deck，数字量输入 + 模拟量

| 端子 | 功能 | MCU 引脚 | 连接器-脚 | 网络名 | 出处 |
|---|---|---|---|---|---|
| D01 | GND | — | J1-1 | `GNDD` | `UpperDeck/netlist.ipc:235` |
| D02 | **Digital IN 1** | PC6 — Enc1a (tim3-ch1) | J1-2 | `DIG_IN_1` | `:236` |
| D03 | **Digital IN 2** | PB5 — Enc1b (tim3-ch2) | J1-3 | `DIG_IN_2` | `:237` |
| D04 | **Digital IN 3** | PB6 — Enc2a (tim4-ch1) | J1-4 | `DIG_IN_3` | `:238` |
| D05 | **Digital IN 4** | PB7 — Enc2b (tim4-ch2) | J2-1 | `DIG_IN_4` | `:439` |
| D06 | **Digital IN 5** | PH10 — Enc3a (tim5-ch1) | J2-2 | `DIG_IN_5` | `:440` |
| D07 | **Digital IN 6** | PH11 — Enc3b (tim5-ch2) | J2-3 | `DIG_IN_6` | `:441` |
| D08 | **Digital IN 7** | PI5 | J2-4 | `DIG_IN_7` | `:442` |
| D09 | **Digital IN 8** | **PI6**（不是 PC6，见第 5 节） | J3-1 | `DIG_IN_8` | `:215`；网络名 `DIG_IN_8_PI6` 见 `:115-116, 428` |
| D10 | GND | — | J3-2 | `GNDD` | `:216` |
| D11 | GND | — | J3-3 | `GNDD` | `:217` |
| D12 | **Analog IN 1** | PC3 (adc3-inp1) | J3-4 | `AIN_1` | `:218` |
| D13 | **Analog IN 2** | PA6 (adc1-inp3) | J4-1 | `AIN_2` | `:208` |
| D14 | **Analog OUT 1** | PA4 (dac1-out1) | J4-2 | `AOUT_1` | `:209` |
| D15 | **Analog OUT 2** | PA5 (dac1-out2) | J4-3 | `AOUT_2` | `:210` |
| D16 | GND | — | J4-4 | `GNDD` | `:211` |
| D17 | GND | — | J4-5 | `GNDD` | `:212` |

不占端子的：`VREF`、AOUT1 故障反馈 `/EF` = PI4、AOUT2 故障反馈 `/EF` = PE3。出处：`Klemmblockzuordnung.pdf` 第 4 页右栏。

> 注：D14/D15 的 MCU 引脚在 `Klemmblockzuordnung` 里写成 `PA4 (adc1-in18)` / `PA5 (adc2-in18)`。那是 ADC 的复用名；这两个脚在这里当 **模拟输出** 用（DAC1_OUT1/OUT2）。**PA4/PA5 这个引脚号本身是核实过的**，只是括号里的外设注记指向了 ADC 那一侧。

---

## 3. 「A 与 C 两套编号」到底是什么关系

### 答案：**两个层级的命名，不是一套编号的两个别名。**

| 命名层 | 文件 | Lower Deck 的两排叫 | Upper Deck 的两排叫 |
|---|---|---|---|
| **产品级**（机箱面板上、给用户看的） | `Klemmblockzuordnung.pdf/.ods`、`Klemmenbezeichnungen-R.pdf` | **Klemmblock A**、**Klemmblock B** | **Klemmblock C**、**Klemmblock D** |
| **板内局部**（KiCad 原理图里） | `OpenPLC_LowerDeck_R3.pdf` p1、`OpenPLC_UpperDeck_R3.pdf` p1 | **"LD Klemmblock A"**、**"LD Klemmblock B"** | **"UD Klemmblock A"**、**"UD Klemmblock B"** |

### 证据

**证据 1 —— Upper Deck 原理图第 1 页的文字**（`Hardware/Production/UpperDeck/Schematics/OpenPLC_UpperDeck_R3.pdf` p1）。图上有两个标题块 **"UD Klemmblock A"** 和 **"UD Klemmblock B"**，下面逐条列：

```
UD Klemmblock A:  A01 +5V   A02 GND   A03 KNX+   A04 KNX-   A05 TXD RS232
                  A06 RXD RS232   A07 CAN L   A08 CAN H   A09 GND / CAN_GND
                  A10 RS485 A   A11 RS485 B   A12 GND
UD Klemmblock B:  B01 GND   B02..B09 Digital IN 1..8   B10 GND   B11 GND
                  B12 Analog IN 1   B13 Analog IN 2   B14 Analog OUT 1
                  B15 Analog OUT 2   B16 GND   B17 GND
```

这两组就是产品级的 **Klemmblock C** 和 **Klemmblock D**。

**证据 2 —— Lower Deck 原理图第 1 页**（`OpenPLC_LowerDeck_R3.pdf` p1）同样有 **"LD Klemmblock A"**（A01–A16，Digital Out）和 **"LD Klemmblock B"**（B01–B12，Relais Out）。这里的 "A" 和 Upper Deck 的 "A" 指的是**完全不同的两排端子**。

**证据 3 —— 机械图上两排是上下叠在一起的两个实体**（`Hardware/Klemmenbezeichnungen-R.pdf` p1，左下角那张装配爆炸图）。Upper Deck 的 Klemmblock C（01–12）和它正下方 Lower Deck 的 Klemmblock A（01–12 + 13–16）是**两排各自独立编号的螺钉端子**，图上分别拉线标注 "Klemmblock C" 和 "Klemblock A"。

### 对 `HARDWARE-FACTS.md:281` 那句话的核实结论

原话（[`open_plc_cube_ide/docs/design/HARDWARE-FACTS.md:281`]($PROD/docs/hardware/HARDWARE-FACTS.md)）：

> 端子字母 **C / A 两套并存**，指同一批端子：`Klemmblockzuordnung.pdf` 叫 C01–C12，KiCad 原理图 p1 叫 A01–A12。

| 判定 | 说明 |
|---|---|
| ✅ 就 Upper Deck 现场总线那一排而言，**说的是对的** | 那一排在 `Klemmblockzuordnung` 里叫 C01–C12，在 Upper Deck KiCad 原理图里叫 A01–A12，确实是同一批端子 |
| ❌ 但**不能由此推出「A 字母全局唯一」** | Lower Deck 也有一套 A01–A16（Digital Out 1–8 + 电源），而且那才是产品级文档和机箱面板上的 "A"。**`A08` 单独写出来是有歧义的**：产品级 = Digital Out 6，Upper Deck 原理图局部 = CAN H |
| ⚠️ 缺一句限定 | 那句话应当补上「**这是 Upper Deck 板内的局部命名**」，否则读者会把 A 当全局编号用 |

`HARDWARE-FACTS.md:283`（`A09=CAN_GND、A10=RS485 A、A11=RS485 B`）**是对的**，和本次网表核实完全一致。

### 建议的写法

| 写法 | 评价 |
|---|---|
| `Klemmblock C 的 C08` / `C08（Upper Deck）` | ✅ 唯一，推荐 |
| `UD Klemmblock A 的 A08` | ✅ 唯一，但只在对着 KiCad 原理图时用 |
| `A08` | ❌ 有歧义，别用 |

---

## 4. 「一个通道占多个端子」怎么排

### 继电器：`Relais Out n` → `B(2n-1)` 和 `B(2n)`，A 在前 B 在后

| 通道 | 端子对 |
|---|---|
| Relais Out 1 | B01 + B02 |
| Relais Out 2 | B03 + B04 |
| Relais Out 3 | B05 + B06 |
| Relais Out 4 | B07 + B08 |
| Relais Out 5 | B09 + B10 |
| Relais Out 6 | B11 + B12 |

规律是 **`A` 在奇数端子、`B` 在偶数端子**，从 B01 开始连排。出处：`LowerDeck/netlist.ipc:63-74`。

**⚠️ 通道配对和物理连接器的边界不重合。** 这排是 **4 个 3 脚连接器**（X8/X7/X6/X5，每个 3 脚），而通道是 2 脚一组，所以 **Relais 2 和 Relais 5 各自被切在两个连接器上**：

```
X8: B01 B02 B03      ← Relais1(B01+B02) + Relais2 的 A
X7: B04 B05 B06      ← Relais2 的 B + Relais3(B05+B06)
X6: B07 B08 B09      ← Relais4(B07+B08) + Relais5 的 A
X5: B10 B11 B12      ← Relais5 的 B + Relais6(B11+B12)
```

出处：`LowerDeck/bom.csv:25`（`X5..X8` = `5TS508S-129N03ELB-01`，3 脚）+ `netlist.ipc:63-74`（每个 X 的 -1/-2/-3 各接哪个 `RYOUT-`）。

**触点是「单刀，两端都引出来」，不是「常开 + 常闭」。** 继电器 `RY1..RY6` = `HF41F/005-HST`（`LowerDeck/bom.csv:17`），网表里每颗只有 4 个脚：`-1` = `5V0`、`-2` = 驱动 MOSFET 漏极（线圈两端），`-3`/`-4` = `RYOUT-nA`/`RYOUT-nB`（触点两端）。**只有 2 个触点脚，物理上不可能同时引出常开和常闭。** 出处：`LowerDeck/netlist.ipc:101-104`（RY1）、`:132-135`（RY2）、`:226-229`、`:265-268`、`:273-276`、`:304-307`。

### 其他「一个功能占多端子」的情况

| 功能 | 端子 | 关系 |
|---|---|---|
| KNX | C03 + C04 | 一对总线线（+ / −），一个通道 |
| RS232 | C05 + C06 | TxD / RxD，一个通道两根线 |
| CAN | C07 + C08 (+ **C09 = CAN_GND**) | H/L 差分对；**C09 是隔离侧参考地，长线场合要接** |
| RS485 | **C10 + C11** | A/B 差分对，一个通道 |
| Digital Out *n* | A(*n*+2)，单端子 | 回流走 A01/A02/A11/A12 任一 GND |
| Digital IN *n* | D(*n*+1)，单端子 | 回流走 D01/D10/D11 任一 GND |
| 正交编码器 Enc1/2/3 | D02+D03 / D04+D05 / D06+D07 | 复用 Digital IN 1–6，A/B 两相 |
| Analog IN/OUT | D12/D13/D14/D15，各单端子 | 回流走 D10/D11/D16/D17 |
| 电源输入 | A15+A16(+) / A13+A14(−) | 两两并联，为了载流（3 oz 厚铜、15 A 设计） |

---

## 5. 硬件文档**内部**对不上的地方

> 这一节说的是 `Hardware/` 里几份文件互相打架。按 `Hardware/CLAUDE.md` 的规矩，**以 KiCad 原理图 / netlist 为准**。

### 5.1 ⚠️ 最重要的一条：`Klemmblockzuordnung` 的 C09–C11 漏了 `CAN_GND`

| 端子 | `Klemmblockzuordnung.pdf` p3–4 / `.ods` | `Klemmenbezeichnungen-R.pdf` p1 | **`UpperDeck/netlist.ipc` + `OpenPLC_UpperDeck_R3.pdf` p1** |
|---|---|---|---|
| C09 | RS485 A | RS485 A | **CAN_GND** |
| C10 | RS485 B | RS485 B | **RS485 A** |
| C11 | GND | （无标注） | **RS485 B** |
| C12 | GND | （无标注） | GND（一致） |

C01–C08 三方完全一致，冲突只在最后四个。

**怎么判定的**：
- 网表 `UpperDeck/netlist.ipc:249-252` 给出 `J11` 四个脚的焊盘坐标与网络：`J11-1 GNDD (Y=-030669)`、`J11-2 RS485_B (-032047)`、`J11-3 RS485_A (-033425)`、`J11-4 CAN_GND (-034803)`。整排 12 个焊盘 Y 间距恒为 1378（0.1378 inch = 3.5 mm），跨 J9/J10/J11 三个连接器也连续，所以**是一条连排，顺序唯一**。
- 排序方向用 Klemmblock D 定标：同一块板另一侧的 17 个焊盘按同样方式排出来，和 `Klemmblockzuordnung` 的 D01–D17 **17/17 全对**。方向没错。
- Upper Deck 的 KiCad 原理图第 1 页独立地把这排标成 `A01 +5V … A09 GND / CAN_GND, A10 RS485 A, A11 RS485 B, A12 GND` —— **两份设计源文件互相印证**。
- `Klemmenbezeichnungen-R.pdf` 的机械图我把 PDF 里的引线矢量提取出来量过：10 条引线的端点沿端子排等间距排列（排内间距 7.02 pt，跨连接器间距 8.90 pt，两个 8.90 正好落在两处连接器边界），把 10 个标注定位到端子 01–10，**11 和 12 没有标注**。也就是说机械图跟的是 `Klemmblockzuordnung` 那一版。

**为什么可能错**：`Klemmblockzuordnung.ods` 的文件时间是 2023-05-26、`Klemmenbezeichnungen-R.pdf` 图签日期 23.05.23，而 Upper Deck 原理图是 **Rev R3 / 2024-07-11**。看起来像是后来加了 `CAN_GND` 端子、两份说明性文档没跟着改。**这一条是推测，没有变更记录可查，未验证。**

**影响**：接 RS485 时按 `Klemmblockzuordnung` 接线会**整体错一位**，A 接到 CAN_GND 上、B 接到 RS485 A 上，RS485 完全不通。这是会直接咬人的。

### 5.2 `Klemmblockzuordnung` 把 D09 的 MCU 引脚写成 PC6

`Klemmblockzuordnung.pdf` p4 / `.ods` sheet "Upper Deck" R26：`D09 Digital IN 8 → PC6 - Enc1a (tim3-ch1)` —— 和 D02（Digital IN 1）一模一样，是复制粘贴错误。

网表里的网络名是 **`DIG_IN_8_PI6`**（`UpperDeck/netlist.ipc:115-116, 428`），原理图顶层图也写 `DIG_IN_8_PI6`（`OpenPLC_UpperDeck_R3.pdf` p1）。**实际是 PI6。**

（这条 `Hardware/UpperDeck_overview.txt:132-135` 已经记过了，本次复核确认。）

### 5.3 `Klemmblockzuordnung` 给 C03(KNX+) 填了 `PE1/PE0 (uart8)`

`.ods` sheet "Upper Deck" R5 那一格确实写着 `PE1 (uart8-rx); PE0 (uart8-tx)`，C04 那格是空的。但 KNX± 接的是 STKNX 收发器 `U9` 的专用总线脚 `KNX_A`/`KNX_B`，**不是 STM32 GPIO，也不是 UART8**。

（这条 `Hardware/UpperDeck_overview.txt:136-143` 已经记过，本次复核确认。）

### 5.4 `Klemmenbezeichnungen-R.pdf` 上 "Digital Out 6" 印成了 "Digital Out 3"

机械图左下角 Klemmblock A 的引线标注，从左到右是：
`Digital Out 8 / Digital Out 7 / `**`Digital Out 3`**` / Digital Out 5 / Digital Out 4 / Digital Out 3 / Digital Out 2 / Digital Out 1`

第 3 个标注（对应 **A08**）应该是 "Digital Out 6"，图上印成了 "3"，和第 6 个标注重复。按位置和网表，**A08 = Digital Out 6**（`LowerDeck/netlist.ipc:79`）。

出处：`Hardware/Klemmenbezeichnungen-R.pdf` p1，图纸区 B7 附近。纯印刷错误，不影响接线（端子号本身没错）。

### 5.5 `Klemmenbezeichnungen-R.pdf` 里 Klemmblock B 的 3D 模型分组不对

机械图把 Klemmblock B 画成 **3 个 4 脚连接器**（`01|02|03|04` / `05|06|07|08` / `09|10|11|12`）。实际是 **4 个 3 脚连接器**（`X5..X8` = `5TS508S-129N03ELB-01`，`LowerDeck/bom.csv:25`；`positions.csv` 里 X5–X8 的 Y 坐标间隔 15.24 mm = 3 × 5.08 mm）。

端子编号和「Relais Out *n* 占哪两个端子」的括号标注都是对的，只是 3D 模型的壳体分组画错了。**不影响接线。**

### 5.6 `Hardware/` 自己的 overview 摘要里跟着抄错的两处

这两份 `*_overview.txt` 在任务给定的「算数」清单里，但它们是**从上面那些文件摘出来的二次整理**，本次发现两处跟着源文档一起错了：

| 位置 | 写的 | 实际 |
|---|---|---|
| [`Hardware/UpperDeck_overview.txt:87-90`](../../../Hardware/UpperDeck_overview.txt) | `C09 RS485 A / C10 RS485 B / C11 GND / C12 GND` | C09=CAN_GND、C10=RS485 A、C11=RS485 B、C12=GND（见 5.1）。这一节自称「已与本板KiCad原理图核对」，但这四行没核到 |
| [`Hardware/LowerDeck_overview.txt:49-50`](../../../Hardware/LowerDeck_overview.txt) | 「X5/X6/X7/X8 四个3pin端子，**每个对应一路继电器的A/B两触点**」 | 每个 3 脚连接器装不下一路的 2 个触点还多 1 个；实际是连排切分，Relais 2 / Relais 5 跨连接器（见第 4 节） |
| [`Hardware/Hardware_overview.txt:39`](../../../Hardware/Hardware_overview.txt) | 「Relais Out 1~6 (**常开/常闭触点对**)」 | 每颗继电器只有 2 个触点脚，引出的是**一对触点的两端**，不是 NO+NC（见第 4 节） |

---

## 6. 抄件和硬件对不上的地方

对比对象：固件 `open_plc_cube_ide/TestCase/porttool/*.c` 里各端口的 `.blk` / `.term` / `.terms` 声明。

| 端口（文件） | 固件声明 | 硬件事实 | 判定 |
|---|---|---|---|
| `porttool_dout.c:339-341` | `blk="A"`, `term="A03-A10"` | Klemmblock A（Lower Deck）A03–A10 = Digital Out 1–8 | ✅ 对 |
| `porttool_relay.c:274-278` | `blk="B"`, `term="B01-B12"`, `terms="B01+B02,…,B11+B12"` | 完全一致，连配对都对 | ✅ 对 |
| `porttool_din.c:270-272` | `blk="D"`, `term="D02-D09"` | D02–D09 = Digital IN 1–8 | ✅ 对 |
| `porttool_ain.c:170-174` | `blk="D"`, `term="D12,D13"` | D12=AIN1、D13=AIN2 | ✅ 对 |
| `porttool_aout.c:221-223` | `blk="D"`, `term="D14,D15"` | D14=AOUT1、D15=AOUT2 | ✅ 对 |
| `porttool_knx.c:559-561` | `blk="C"`, `term="C03,C04"` | C03=KNX+、C04=KNX− | ✅ 对 |
| `porttool_rs232.c:113-115` | `blk="C"`, `term="C05,C06"` | C05=TxD、C06=RxD | ✅ 对 |
| `porttool_can.c:334-336` | `blk="C"`, `term="C07,C08"` | C07=CAN L、C08=CAN H | ✅ 对（但没提 **C09 = CAN_GND**，长线接线时工程师会漏） |
| **`porttool_rs485.c:277-279`** | `blk="C"`, **`term="C09,C10"`** | **C10 = RS485 A、C11 = RS485 B**；C09 是 CAN_GND | ❌ **错一位**。抄的是 `Klemmblockzuordnung` 的错版 |
| **`porttool_eth.c:497-499`** | **`term="J1"`** | Bridge 的 RJ45 是 **`J4`**；Bridge `J1` 是通到 Upper Deck 的 2×16 板间排针 | ❌ **错** |
| **`porttool_usb.c:370-372`** | **`term="J2"`**（注释写 "the Type-C connector"） | Bridge 的 USB-C 是 **`J5`**；Bridge `J2` 是 2×15 板间排针 | ❌ **错** |
| `porttool_sd.c:141-143` | `term="J6"` | Bridge `J6` = microSD | ✅ 对 |
| `porttool_temp.c`、~~`porttool_soak.c`~~ | `blk="-"`, `term="-"` | 板载传感器 / 跨多块 | ✅ 合理。⚠️ **`porttool_soak.c` 已于 2026-09-12 删除**，持久测试改成上位机计时（见 [06](issues/PUI-06-port-list-structure.md)） |

Bridge 连接器出处：`Hardware/Production/Bridge/1436_01_SCHAE-BR.xlsx` 第 19–24 行（`J1` 2×16 排母、`J2`/`J3` 2×15 排母、`J4` RJ45 `74990111211`、`J5` USB-C `DX07S024WJ3`、`J6` microSD `104031-0811`、`J7` JTAG `FTSH-105-01-H-DV-K-P-TR`），与 `1436_01_SCHAE-BR.pdf` 第 3–5 页的图纸位号一致。

**上位机面板不是独立抄件。** `IAPTranfer_Tool/internal/ptproto/caps.go:61-62` 只是把固件给的 `blk`/`term` 字符串原样带出来，Go 侧没有自己的端子表。所以**面板上显示的 `C09,C10`、`J1`、`J2` 全部来自固件**，要改就改固件那三处。

---

## 7. 查不到的 / 未验证的

| 问题 | 状态 |
|---|---|
| **继电器触点是常开还是常闭** | **未验证。** 从 `Hardware/` 只能确定「每颗只有 2 个触点脚，引出的是一对触点的两端」（`LowerDeck/netlist.ipc` 的 RY1–RY6 记录）。NO / NC 要查 Hongfa `HF41F/005-HST` 数据手册，`Hardware/` 里没有这份手册。 |
| **`Klemmblockzuordnung` C09–C11 到底是笔误还是改版没跟上** | **未验证。** 只有文件日期（.ods 2023-05-26、机械图图签 23.05.23）早于 Upper Deck 原理图（R3 / 2024-07-11）这一条间接线索，仓库里没有 R1/R2 版本的原理图或改版记录可比。**建议向 Schaeffer AG 确认。** |
| **机箱面板上实际丝印的是什么** | **查不到。** `Hardware/` 里没有面板丝印图 / 外壳图 / 铭牌文件。本文档的 A/B/C/D 全局编号出自 `Klemmblockzuordnung` 和 `Klemmenbezeichnungen-R`，**没有实物照片或面板图佐证**。 |
| **`Klemmenbezeichnungen-R.pdf` 的 Klemmblock A / B 引线标注逐端子核对** | **只做了目视 + 局部放大，没做矢量提取。** C 排做了矢量提取（第 5.1 节）；A 排只核到 "Digital Out 6 印成 3"（第 5.4 节）；B 排只核到 Relais 的括号配对正确。A、B 两排的端子号-功能对照另有网表 + `Klemmblockzuordnung` + LD 原理图三方一致，所以不影响结论。 |
| **D14/D15 走的是 DAC1_OUT1/OUT2 还是别的** | **引脚号 PA4/PA5 已核实**（`Klemmblockzuordnung.pdf` p4 + `OpenPLC_UpperDeck_R3.pdf` p1 的 `ANA_OUT_1_PA4` / `ANA_OUT_2_PA5`）。但源文档括号里写的是 `adc1-in18` / `adc2-in18`，**「这两个脚在这里配成 DAC 输出」这件事本身没在 `Hardware/` 里找到明文**，是按功能名 `Analog OUT` 推的。要坐实得看 4–20 mA 驱动电路那一页的原理图。 |
| **Junction Link DIN 导轨扩展口的 20 个脚算不算「对外端子」** | 算对外接口，但**不是螺钉端子**（Samtec ERF8 0.8 mm 板对板）。管脚定义见 `Klemmblockzuordnung.pdf` 第 2 页 / `JunctionLink/netlist.ipc:79-98`，本文档没有展开成端子表。 |
| **`existed connector.xlsx`、`STM32H743IIK6_GPIO_ASSIGNMENT_..._20260822.xlsx`** | **本次没有打开。** 板间连接器对照用的是 `Hardware_overview.txt:48-61` 加各板 BOM 位号交叉验证；MCU 引脚用的是 `Klemmblockzuordnung` + 原理图网络名。这两份 xlsx 可以作为第三方印证，本次未取。 |

---

## 8. 要改的地方（本次未动手，等定）

| # | 改哪 | 改什么 | 理由 |
|---|---|---|---|
| 1 | [`open_plc_cube_ide/TestCase/porttool/porttool_rs485.c:277-279`](../../../open_plc_cube_ide/TestCase/porttool/porttool_rs485.c) | `term="C09,C10"` → `"C10,C11"`；`terms="C09+C10"` → `"C10+C11"` | 接线会整体错一位，RS485 直接不通 |
| 2 | [`open_plc_cube_ide/TestCase/porttool/porttool_eth.c:498`](../../../open_plc_cube_ide/TestCase/porttool/porttool_eth.c) | `term="J1"` → `"J4"` | Bridge J1 是板间排针，不是 RJ45 |
| 3 | [`open_plc_cube_ide/TestCase/porttool/porttool_usb.c:371`](../../../open_plc_cube_ide/TestCase/porttool/porttool_usb.c) | `term="J2"` → `"J5"` | Bridge J2 是板间排针，不是 USB-C |
| 4 | [`open_plc_cube_ide/TestCase/porttool/porttool_can.c:334-336`](../../../open_plc_cube_ide/TestCase/porttool/porttool_can.c) | 考虑把 `C09 = CAN_GND` 也报出来 | 长线场合不接隔离地会出问题，面板上现在看不到这个端子 |
| 5 | [`open_plc_cube_ide/docs/design/HARDWARE-FACTS.md:281`]($PROD/docs/hardware/HARDWARE-FACTS.md) | 补一句「这是 Upper Deck **板内局部**命名；Lower Deck 另有一套 A01–A16」 | 现在的写法会让人以为 A 是全局唯一的 |
| 6 | `open_plc_cube_ide/docs/design/HARDWARE-FACTS.md` | 把本文档第 2 节四张端子表收进去，每条带出处和核实日期 | `Hardware/CLAUDE.md` 要求「查出来的结论写进 HARDWARE-FACTS.md」 |
| 7 | [`Hardware/UpperDeck_overview.txt:87-90`](../../../Hardware/UpperDeck_overview.txt)、[`LowerDeck_overview.txt:49-50`](../../../Hardware/LowerDeck_overview.txt)、[`Hardware_overview.txt:39`](../../../Hardware/Hardware_overview.txt) | 见第 5.6 节 | 这三处是 `Hardware/` 里的二次整理，跟着源文档错了 |
| 8 | 向 Schaeffer AG 提 | `Klemmblockzuordnung` 的 C09–C11（5.1）、D09 引脚（5.2）、C03 引脚（5.3）、`Klemmenbezeichnungen-R` 的 "Digital Out 3"（5.4）和 Klemmblock B 3D 分组（5.5） | 5.1 是会咬人的那条 |

---

# 主会话的复核（2026-09-11）

下面每一条都由主会话**独立重查过一遍**，不是照抄上面的调查结果。

| 结论 | 复核方式 | 结果 |
|---|---|---|
| C 排顺序：C05/C06=RS232、C07/C08=CAN L/H、C09=CAN_GND、C10/C11=RS485 A/B | 读 `Hardware/Production/UpperDeck/netlist.ipc:245-256` 的焊盘 Y 坐标（等间距 1378 单位），推出沿端子条的物理顺序，再用面板自己的提示「控制口是端子 C05/C06」定方向 | ✅ 成立 |
| 固件 `rs485` 写 `C09,C10` | `open_plc_cube_ide/TestCase/porttool/porttool_rs485.c:277-278` | ✅ 确实这么写的，**且与上一条矛盾** |
| 以太网 RJ45 是 Bridge **J4**，不是 J1 | `Hardware/Production/Bridge/Pick Place for 1436_01_SCHAE-BR-PCB.txt:128` —— `J4  74990111211 ... "1 Port RJ45..."` | ✅ 成立 |
| USB-C 是 Bridge **J5**，不是 J2 | 同上 `:139` —— `J5  DX07S024WJ3 ... "USB Type C, 24Pin"` | ✅ 成立 |
| `Hardware/Bridge_overview.txt:91` 把 RJ45 写成 `J1` | 同一份文件 `:34` 又说 `J1` 是 32 针板间排针 —— **它自相矛盾**，且与贴装坐标表不符 | ✅ 该 overview 抄错了 |
| 上位机面板不是独立抄件 | `IAPTranfer_Tool/internal/ptproto/caps.go:61-62`，`Term` 就是个透传字符串字段 | ✅ 成立 |

## ⚠️ 主会话推翻的一条

调查报告说 `HARDWARE-FACTS.md:283` 「只对了一半」。**它讲的那几个数字其实全对**：该行写 A09=CAN_GND、A10=RS485 A、A11=RS485 B，在 Upper Deck 局部 A=C 的语境下，正是 C09/C10/C11，和网表一致。

问题不在数字，在于**那句话没有限定「仅 Upper Deck 局部编号」**，读的人会以为 A 字母全局唯一。真正的修法是给它补一个限定语，不是改数字。

## ⚠️ 主会话在派这张 ticket 时提出的怀疑，现已撤回

原怀疑：固件 `dout` 声明 `term="A03-A10"` 与 CAN / RS232 / RS485 的端子撞号。
**不成立。** `dout` 的 A 是 **Lower Deck Klemmblock A**（数字量输出排），CAN 那些在 **Upper Deck Klemmblock C**。两排互不相干，`A03-A10` 是对的。
