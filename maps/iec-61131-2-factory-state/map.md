# 出厂状态符合 IEC 61131-2

## 怎么看进度（不用问任何人）

```
python tools/list_wayfinder_map_frontier.py --all
```

## Destination

IEC 61131-2 对「没有程序在跑、上电、掉电、欠压、程序卡死」时的要求，这块板逐条做到，并写进给用户的手册：每个输出在这些时刻处于什么状态、看门狗和报警输出怎么工作。

## Notes

- **这张图带执行**：票定完就写代码；先文档再代码，只做必要的
- 标准原文和出处：[IEC-61131-2.md](../../docs/standards/IEC-61131-2.md)。**标准不要求出厂预装 app**（那份文件第 1 节），所以本图不做出厂 app
- 条款以 2003 版全文为准，2017 版正文没核实
- 开票 / 关票 / 算前沿照 [图与票的约定](../MAP-AND-TICKET-CONVENTION.md)

### 开图时已定（2026-09-28 用户定）

| 事 | 定案 |
|---|---|
| 开机窗口 | **不能再让继电器响**：继电器上接了负载时，每次上电都会被动作一次（标准 2003 6.3.1.4：上电过程中不许有 unintended condition）。改用系统指示灯，见 [决策 71](../../docs/tables/DECISIONS.md) |

## 全集

```
grep -rnE "Relay_On|Relay_Off|HAL_GPIO_WritePin|IWDG|HAL_DAC" open_plc_cube_ide/Core/Src open_plc_cube_ide/IAPServer open_plc_arduino/cores/arduino
```

上面找的是 bootloader 和 core 里所有会动输出、会碰看门狗的地方；输出清单以 [HARDWARE-FACTS.md](../../docs/hardware/HARDWARE-FACTS.md) 为准。

## Decisions so far

- [AO 在上电和掉电时怎么落到确定值](issues/IEC-05-ao-has-no-defined-state-at-power-up.md)：bootloader 一开始把 AO 和 DO 主动置 0（决策 81）；硬件下拉等示波器实测再说
- [报警输出用哪个、正常时是什么状态](issues/IEC-04-alarm-output.md)：板卡包不提供，用户在程序里自己定义；手册建议正常时吸合
- [用户程序卡死时谁发现、输出怎么办](issues/IEC-03-watchdog-for-the-user-program.md)：板卡包只提供看门狗能力，由 sketch 自己开、自己喂；bootloader 不计数、不停 app（决策 80 取代同日先定的默认开启）
- [开机窗口改用什么提示](issues/IEC-01-what-replaces-the-relay-click.md)：系统指示灯 PE2 + 串口日志：窗口快闪、恢复出厂就绪常亮；开机不动任何输出
- [每个输出在上电、掉电、没有 app、app 刚起来时处于什么状态](issues/IEC-02-what-state-is-each-output-in.md)：DO / 继电器都落在断开；AO 上电和掉电时没定义；无看门狗、欠压检测、报警输出；RUN / STOP 不强制

## Not yet specified

- **手册写在哪、写成什么样**：要等各输出的状态和看门狗行为定了才知道要写哪些
- **型式试验要的测试程序（PFVP）**：标准要求做型式试验时厂商提供跑遍所有 I/O 的程序，工装固件接近这个角色；要不要、何时做型式试验还没说

## Out of scope

- **出厂预装 app**：标准不要求（[IEC-61131-2.md](../../docs/standards/IEC-61131-2.md) 第 1 节）。2026-09-28 定
- **EMC、耐压、环境这类型式试验本身**：是硬件和实验室的事，不是固件能做到的
