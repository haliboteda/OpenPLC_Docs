# 02 · 固件 14 个 `term=` 声明逐条对硬件

Type: research
Opened: 2026-09-11
Status: resolved
Blocked by: -

⚠️ **原状态写的是「关闭：已出本图范围」** —— 那是**出了范围**，不是答完。按约定已在地图的「明确不做」里记一行。

## Question

固件在 `pt.caps` 里给每个端口声明了端子号。**哪几条和 01 建立的权威端子表对不上？**

面板的标签全部由这些声明推导（`$TOOL/internal/ptproto/caps.go:185` 的 `TerminalLabels()`），所以声明错了，面板就一定错，而且错得看起来很正常。

## 01 已经解掉的部分（2026-09-11）

01 结掉时顺手查出了三处对不上，**已复核**，这张 ticket 不必重查：

| 端口 | 固件写的 | 硬件的 | 出处 |
|---|---|---|---|
| `rs485` | `C09,C10` | **`C10,C11`** | `UpperDeck/netlist.ipc:245-256`。C09 是 CAN_GND —— 按固件接线，一根线会接到 CAN 地上 |
| `eth` | `J1` | **`J4`** | `Bridge/Pick Place for 1436_01_SCHAE-BR-PCB.txt:128` |
| `usb` | `J2` | **`J5`** | 同上 `:139` |

**剩下的 11 个端口还没逐条对。** 那是这张 ticket 现在的全部内容。

## 原始起因（已撤回）

`$BOOT/TestCase/porttool/porttool_dout.c:340-341`：

```c
.term     = "A03-A10",
.terms    = NULL,          /* a plain run: DO<n> is terminal A0<n+2> */
```

按这个，DO1=A03、DO3=**A05**、DO8=A10。

但 `$PROD/docs/hardware/HARDWARE-FACTS.md:283`（出处 `netlist.ipc:245-256` + 原理图，两者一致）写着 **A07/C07=CAN L、A08/C08=CAN H、A09=CAN_GND、A10=RS485 A**，而面板自己的连接提示（`$TOOL/internal/ptpanel/web/index.html:259`）写着**控制口是端子 C05/C06**（RS232）。

**这条怀疑不成立，已撤回。** 01 查明：`dout` 的 A 是 **Lower Deck Klemmblock A**，CAN 那些在 **Upper Deck Klemmblock C**，两排互不相干。`A03-A10` 是对的。

## 要做什么

1. 把 14 个端口的 `term=` / `terms=` 声明全列出来（`$BOOT/TestCase/porttool/` 下每个 porttool_ 开头的 .c 里各自的 `porttool_port_t`）。
2. 逐条对 01 的权威表，产出三列：**端口 / 固件说的 / 硬件说的 / 是否一致**。
3. 对不上的，判断是固件写错还是命名空间不同。
4. ⚠️ **改固件的 `term=` 会让 `$TOOL/TestCase/host/porttool_caps/` 的契约测试（H4）跟着变** —— 那套是把固件 `.c` 原样编成 PC 程序来跑的，改了要一起过。

## 产出

一张对照表 + 一份「要改哪几处、改成什么」的清单。**改动本身先不做**，等这张表给用户看过。

## 怎么算答完

⚠️ **这张票搬进来时没有这一节**（2026-09-16 之前的写法不要求）。开工前先补上再动手。


## Answer

2026-09-16 补节。**这张票在本仓的约定成型之前就已经关了**，当时不要求写 `## Answer`。
结论散在它自己的正文和同目录的 `01-findings.md` 里。

## 引出了什么新的未知

搬迁时补的空节，当时不要求。
