# 例程清单：每个演示什么

Type: grilling
Opened: 2026-10-03
Status: resolved
Blocked by: KEX-02, KEX-03

## Question

候选（2026-10-03 推荐）：`KNX_Programming`（进编程模式、ETS 编物理地址并下载应用、串口打印拿到的地址）、`KNX_Switch`（ETS 写开 / 关 → 继电器动作，另一个对象回报状态）、`KNX_Input`（DI 一变就发组报文，别人读时回答当前值）。每个用哪些组对象、串口打印什么、文件头写什么；要不要再加。

## 怎么算答完

每个例程定下：名字、演示的操作、用到的组对象、串口打印格式、文件头里写的接线和预期。

## Answer

2026-10-03 定（用户：可以）：

| 问题 | 定了什么 | 一句理由 |
|---|---|---|
| 几个例程 | `KNX_Switch`（继电器 1–6，对象 1–12）、`KNX_Inputs`（DI 1–8，对象 13–20）；编程不单独成例程，两个例程开机都打印地址和配没配置 | 编程键和系统灯由库统一处理，单独一个例程只剩打印地址 |
| 串口打印（USB） | 开机 `KNX: address 1.1.20, configured` 或 `KNX: not configured - program it with ETS`；收发各一行，如 `KNX RX relay 3 switch = 1`、`KNX TX relay 3 status = 1`、`KNX TX DI 2 = 1` | 不开 ETS 也看得到发生了什么，用例也靠它判 |
| 什么时候发 | 继电器状态在开关真正改变后发、被读时回答；DI 每 20 ms 采样、变了就发、被读时回答；开机不主动发、不周期发 | 只做必要的 |
| 写法 | 直接用板卡包脚名 `REL_1`…`REL_6`、`DIN_1`…`DIN_8`；不用库里只管两路的继电器配置；文件头写接线、所用对象、ETS 步骤（链到 `OpenPLC_ETS_Prod` 的 README）、预期打印；**KNX Role 不是 TP 时编译报错** | 产品是 `MV-07B0`，角色选错要到 ETS 下载时才暴露 |

## 引出了什么新的未知

- 库里那个只管两路的继电器配置（`initRelayProfile2CH`、`selfProgram2CH`）在旧例程删掉后还要不要留 —— 进迷雾
