# Relays 例程不停地切继电器，怎么不白耗寿命

Type: grilling
Opened: 2026-10-10
Status: resolved
Blocked by: -

## Question

`$CORE_REPO/libraries/OpenPLC_Ports/examples/Relays/Relays.ino` 的 `loop()` 把 RY1–RY6 轮流吸合，约 7.2 秒一轮、永不停止。上板测试时，它会从人按 y 一直切到下一个例程烧进去为止；板子再上电还会接着切（用户 2026-10-10：「relay 一直在响」，因此断了电）。

| 做法 | 代价 | 风险 |
|---|---|---|
| 例程只走一轮就停，按复位再走一轮 | 改一个出货例程和它的头注释；`run_examples.py` 那条提问去掉「it repeats」 | 客户错过那一轮就要按复位 |
| 例程走固定几轮（如 3 轮）后停 | 同上 | 同上，只是窗口大一些 |
| 例程不动，测试脚本在人回答后立刻烧一个不动继电器的 sketch | 只改 `$TEST/tools/run_examples.py` | 客户自己跑这个例程时照样一直切 |

## 怎么算答完

用户选定一种；按它改例程或脚本，`T3-06` 里 `Relays` 那条重跑通过。

## Answer

2026-10-12 定（用户）：**「跑几轮，relay之间间隔多久都可以设置。超过了给提醒就行」**。例程开机走 1 轮、每路吸合 1000 ms 后停，继电器全断开；串口命令 `r <轮数>`、`i <毫秒>` 设轮数和每路吸合时长，`g` 再走一遍，走的时候打任意字符回车就停。轮数超过 100（决策 91 的提醒线）或时长短于 1000 ms（手册电寿命按 1 s 通标定，见 [HARDWARE-FACTS.md](../../../docs/hardware/HARDWARE-FACTS.md)「继电器 RY1–RY6」）打一行 `warning:`，照样设。`T3-06`（[M3-app-runtime.md](../../../docs/modules/M3-app-runtime.md)）的 Relays 那条 2026-10-13 上板重跑通过（经网口上传）；`T3-11` 在 Renode 里判。

## 引出了什么新的未知

查手册时发现「HF41F 机械寿命 3 万次」是误记（3 万是 Z 型常开触点的电寿命，机械寿命 1000 万次），已在决策 46、91 里改正并记进 HARDWARE-FACTS。PortTool 面板 `$PORTTOOL/src/ptpanel/web/js/library.js:148` 的 `RELAY_RATED_OPS = 30000` 仍把 3 万次当「额定」算百分比。用户 2026-10-12 定：按器件手册同步、不猜，由工装那边改，见 [TODO-fixture.md](../../../work/TODO-fixture.md) 第 56 条。
