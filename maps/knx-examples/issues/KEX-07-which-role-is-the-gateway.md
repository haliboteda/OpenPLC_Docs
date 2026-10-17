# 「网关」指哪个角色

Type: grilling
Opened: 2026-10-09
Status: resolved
Blocked by: -

## Question

[决策 95](../../../docs/tables/DECISIONS.md) 定了「只做 IP+TP，板子当网关」。库里带两个网络的角色有两个，行为不同：

| 角色 | 现在的代码做什么 | 在哪 |
|---|---|---|
| IP+TP 双模（0x5780，板卡包菜单默认） | 板子自己是一个设备，IP、TP 两边都能收发；自己发的报文两边各发一份。**不在 IP 和 TP 之间转发别人的报文** | `bau5780.h`（2026-10-09 已删） |
| IP/TP 耦合器（0x091A） | 按过滤表在 IP 和 TP 之间转发报文，ETS 可经它访问 TP 上的设备 | `$CORE_REPO/libraries/OpenPLC_KNX/src/knx/bau091A.h` |

用户 2026-10-09：**「网关的意思是同时具备 tp 和 ip」** —— 上表两个角色都满足。还差一件：ETS 或别的 IP 设备要不要**经板子**访问 TP 总线上的其他设备（要就是 0x091A，不要就是 0x5780）。

**2026-10-09 查到的两条事实**（影响能不能用 ETS 配置板子）：

| 事实 | 出处 |
|---|---|
| ETS 认识的 mask 里没有 0x5780（有 `MV-07B0` System B、`MV-57B0` System B IP、`MV-091A` Coupler），0x5780 是本库自己加的；板子在 0x5780 下向 ETS 报的就是 0x5780，所以**这个角色做不出 ETS 产品文件，ETS 也下载不进去** | 本机 ETS 5 的 `KnxMaster/14/knx_master.xml`；`bau5780.cpp`（2026-10-09 已删） 里 `maskVersion(0x5780)` |
| 0x091A 没有组对象，板子不能作为一个设备被 ETS 关联组地址 | `$CORE_REPO/libraries/OpenPLC_KNX/src/knx_facade.h` `getGroupObject` 的条件编译 |

「网关」是哪一个，另一个以及只接 TP（0x07B0）、只接 IP（0x57B0）的角色从板卡包菜单和库里删掉。

用户 2026-10-09 又定：**只用 ETS 认识、能编程的模式，不要自己创造**（0x5780 出局），并要求 **PLC 像普通 KNX 设备一样被 ETS 编程**。ETS 里能当「普通设备」（有组对象）的是 0x07B0 / 0x57B0；0x091A 是耦合器，没有组对象。和同日「openplc 就是做网关用的」冲突，待用户定。

## 怎么算答完

定下保留的那一个角色；菜单默认值随之定。

## Answer

2026-10-09 定（用户：「knx的demo例子改成 tp， IP网关，busmonitor」）：

| 问题 | 定了什么 | 一句理由 |
|---|---|---|
| 保留哪些角色 | TP 设备 0x07B0（默认）、IP 网关 0x091A | ETS 都认识；前者是能被 ETS 关联组地址的普通设备，后者转发 IP 和 TP |
| 删哪些 | 0x5780（本库自造，ETS 不认识）、0x57B0（只走 IP 的设备，不要） | [决策 95](../../../docs/tables/DECISIONS.md) |
| 和测试盒互相控制用哪个 | 0x07B0 | 0x091A 没有组对象 |

## 引出了什么新的未知

- 0x091A 的 ETS 产品文件怎么做（OpenKNXproducer 能不能生成耦合器产品没核实）—— 进迷雾
