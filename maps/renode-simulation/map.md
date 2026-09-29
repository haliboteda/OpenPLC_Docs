# 没有板子时用 Renode 验证固件

## 怎么看进度（不用问任何人）

```
python tools/list_wayfinder_map_frontier.py --all
```

## Destination

1. **Renode 里走和真板子一样的启动链**：bootloader 先运行，校验通过后跳进 app
2. **`OpenPLC_Ports` 的 13 个例程在 Renode 里自动判过不过**；判不了的逐个说明原因，并给出替代方案

## Notes

- **这张图带执行**：票定完就写代码
- **只做必要的代码和测试**；先文档再代码
- Renode 1.17.0 Windows 免安装版，装在 `D:\Soft\renode`（2026-09-27）
- 开票 / 关票 / 算前沿照 [图与票的约定](../MAP-AND-TICKET-CONVENTION.md)

### 开图时已定（2026-09-27 用户定）

| 事 | 定案 |
|---|---|
| 启动方式 | 和真板子一样：先进 bootloader，再跳 app。不在脚本里代替 bootloader 做事 |
| 范围 | 13 个例程都要；做不到的说出是哪个、为什么、有没有替代方案 |
| 目标（2026-09-27 用户定，取代上一行） | 验证 Arduino core 和 13 个例程的**代码**是对的，能直接上真板测。**不要求每个端口都在 Renode 里测出来**，只做达到这个目标必要的 |
| 做法（2026-09-28 用户认可） | 两层：① 13 个都查启动链走完、`setup()` 走完、`loop()` 在转、没跑飞；② 每个例程只查它自己端口的寄存器读写对不对。**Renode 只需把寄存器访问接住、记下来，不要求外设模拟得像**；判失败时先分清是代码的错还是模型的错 |

### 开图前已知（2026-09-27 实测）

- `DO_Outputs` 直接从 app 起跑（跳过 bootloader）时，在 `HAL_RTC_MspInit` 等 LSE 超时后进死循环：LSE 平时由 bootloader 打开。启动前替它置 LSEON 后，DO1–DO8 按例程顺序开关
- 所有例程的 `Serial` 走 USB CDC，Renode 的 USB 模型下看不到文字；平台里没有 DAC

## 全集

```
ls open_plc_arduino/libraries/OpenPLC_Ports/examples
```

## Decisions so far

- [Renode 能不能走 bootloader → app 的启动链](issues/REN-01-can-renode-boot-through-the-bootloader.md)：能，flash 填 `0xFF` 后放 bootloader、签好名的 app 和一条 metadata 记录，只用 `LoadBinary` 加载
- [13 个例程里哪些 Renode 判得了](issues/REN-02-which-examples-can-renode-judge.md)：5 个能、1 个能但有未核实项、6 个部分、`AO_Outputs` 不能，表见 [REN-02-findings.md](REN-02-findings.md)
- [13 个例程在 Renode 里跑两层检查](issues/REN-03-run-both-layers-on-all-examples.md)：13 个两层都过；只把第 ① 层做成用例 `T3-05` 进仓库，第 ② 层结论留在票里

## Not yet specified

（无）

## Out of scope

- **`Serial` 从哪引出来**：两层检查都没用到 `Serial` 文字，第 ② 层又不进仓库，不需要了。2026-09-28 定
