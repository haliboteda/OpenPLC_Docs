# 01 · 从硬件资料建立权威端子表

Type: research
Opened: 2026-09-11
Status: resolved
Blocked by: -

## Question

这块板对外的接线端子，**权威的编号和功能对照表是什么**？只准从 `Hardware/` 来。

要回答的具体几点：

1. **一共有几排端子？** Upper Deck、Lower Deck、Bridge、JunctionLink 各自对外的端子是哪些连接器（`J*`）。
2. **`A01–A12` 和 `C01–C12` 是什么关系？** `$PROD/docs/hardware/HARDWARE-FACTS.md:283` 附近写「端子字母 C / A 两套并存，指同一批端子：`Klemmblockzuordnung.pdf` 叫 C01–C12，KiCad 原理图 p1 叫 A01–A12」。**如果只有一批，那 A 字母就是全局唯一的**；如果每排各有一套 A01–A12，那就不是。这一条决定后面所有对照怎么做。
3. **DO1–DO8（`HSFET1~8`）落在哪几个端子？** 已知线索：`Hardware/Bridge_overview.txt:47` 说 `J3` 上有 `RELAIS_1~6` 和 `HSFET1~8` 的驱动信号 —— 但那是板间连接器，不是对外端子。要找的是**对外接线端子**。
4. 同样查清：DI、AI、AO、继电器触点、CAN H/L/GND、RS232、RS485 A/B、KNX ± 各自的端子号。
5. **一块硬件占多个端子的情况**（继电器是触点对，6 通道 12 端子）按什么规律排。

## 出处限制

**只有这些算数**：`Hardware/Production/*/netlist.ipc`、`Hardware/Production/UpperDeck/Schematics/OpenPLC_UpperDeck_R3.pdf`、`Hardware/Klemmblockzuordnung.pdf` / `.ods`、`Klemmenbezeichnungen-R.pdf`、各 `*_overview.txt`、BOM / positions。

**不算数**：固件的 `pt.caps`、面板代码、Arduino 板卡包的变体头、`.ioc` —— 全是抄件。抄件可以用来交叉验证，对不上时**先说这件事本身**。

## 产出

查出来的每一条写进 `$PROD/docs/hardware/HARDWARE-FACTS.md`，**每条带出处（文件:行号）和核实日期**。那里是软件侧唯一会去读的地方。

## Answer

2026-09-09 定（日期是 2026-09-16 搬迁时按票的内容补的，旧写法不要求）。

完整结果与逐条出处在 [01-findings.md](../01-findings.md)（含主会话的独立复核一节）。

**1. 几排端子**：四排螺钉端子，全叫 `Klemmblock A/B/C/D`。A（DO + 电源）、B（继电器）在 **Lower Deck**；C（现场总线）、D（DI/AI/AO）在 **Upper Deck**。Bridge 和 JunctionLink 没有螺钉端子，只有 RJ45 / USB-C / microSD / JTAG。

**2. `A01–A12` 与 `C01–C12` 的关系**：**不是同一批端子，A 字母不全局唯一。** 产品级文档里 A = Lower Deck 的数字量输出排；KiCad 原理图里字母是板内局部的，Upper Deck 把自己的 C 排叫 "UD Klemmblock A"。**单写 `A08` 有歧义**（产品级 = Digital Out 6，UD 原理图 = CAN H）。

**3. 功能落点**（已复核）：DO1–8 = A03–A10（Lower Deck）；继电器 1–6 = B01+B02 … B11+B12；KNX± = C03/C04；RS232 TxD/RxD = C05/C06；CAN L/H = C07/C08；**CAN_GND = C09**；**RS485 A/B = C10/C11**；DI1–8 = D02–D09；AI1/AI2 = D12/D13；AO1/AO2 = D14/D15。以太网 = Bridge **J4**；USB-C = Bridge **J5**。

**4. 撤回**：派这张 ticket 时怀疑「`dout` 的 A03–A10 与 CAN/RS232/RS485 撞号」—— **不成立**，两者分属不同 Klemmblock。

**5. 顺带查出的抄件错误**（这是本张 ticket 最值钱的产出）：
- `Klemmblockzuordnung.pdf/.ods` 第 4 页漏了 `CAN_GND`，把 RS485 A/B 整体上移一位 —— **硬件文档本身错了**
- 固件三处：`porttool_rs485.c` 的 `C09,C10` 应为 `C10,C11`；`porttool_eth.c` 的 `J1` 应为 `J4`；`porttool_usb.c` 的 `J2` 应为 `J5`
- `Hardware/Bridge_overview.txt:91` 把 RJ45 写成 J1，且与同文件 :34 自相矛盾
- `HARDWARE-FACTS.md:283` 数字全对，但缺「仅 Upper Deck 局部编号」的限定语

## 怎么算答完

⚠️ **这张票搬进来时没有这一节**（2026-09-16 之前的写法不要求）。开工前先补上再动手。



## 引出了什么新的未知

⚠️ 2026-09-16 搬迁时补的空节 —— 这张票关在这条规矩成型之前。
