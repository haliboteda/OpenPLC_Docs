# 测试脚本怎么判一个例程过没过

Type: grilling
Opened: 2026-09-29
Status: resolved
Blocked by: -

## Question

PC 侧脚本判例程时：例程的串口输出要不要加机器能读的行；判据写在哪（沿用工装方案文件和 `ptcheck`，还是写在 Python 脚本里）；上传走哪条路（网口 / USB CDC）；用例编进哪个编号段、住在哪份文档。

## 怎么算答完

定下输出格式、判据位置、上传路径、用例编号和文档位置；拿一个已人工验过的例程（如 RS485_Echo）写出第一条用例的样子。

## Answer

2026-09-30 定（用户四条都选第一种）：

| 问题 | 定了什么 | 一句理由 |
|---|---|---|
| 输出格式 | 例程不加机器行，脚本用正则认例程现有的人读输出 | 例程是给用户看的；文案一改用例就断，正好逼文件头和实际输出一致 |
| 判据位置 | 写在 Python 脚本里的一张表，一个例程一行（发什么、等哪行、正则、要人做什么） | `ptcheck` 为的是面板和产线不分歧，这里没有面板；自动化一律用 Python |
| 上传路径 | USB CDC（`cdcMethod`，`IAPTool cdc`），例程的 `Serial` 输出也在这个口 | 一根线同时管上传和判定 |
| 编号和文档 | 需求 `R3-09`、用例 `T3-06`（一个编号管全部例程，`--only NAME` 跑单个），写在 [M3 应用运行环境](../../../docs/modules/M3-app-runtime.md)；脚本 `$TEST/tools/run_examples.py` | 与 `T3-05` 一个编号管 13 个例程同一个做法 |

第一条用例（`RS485_Echo`）：编译 → 经 CDC 上传 → 开 CDC 口和 RS485 转接器 → 等到 `RS485_Echo: send a line over RS485.` → 从转接器发 `EXB-PING-1\n` → 2 s 内转接器收回同样的字节，**且** CDC 口出现 `RS485 echoed: EXB-PING-1`，判过。

## 引出了什么新的未知

- 经 CDC 给**正在跑 app** 的板子上传（1200 bps magic touch，见 [M1](../../../docs/modules/M1-firmware-upgrade.md)）没在这台板子上验过 —— 在 `T3-06` 的第一次上板里验，不另开票
