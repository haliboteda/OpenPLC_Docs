# core 里的例程在真板上逐个测通

## 怎么看进度（不用问任何人）

```
python tools/list_wayfinder_map_frontier.py --all
```

## Destination

自有库的 20 个例程（`OpenPLC_Ports` 13、`OpenPLC_KNX` 5、`OpenPLC_SDRAM` 2）各有一条真板用例并全部通过：PC 侧脚本编译、上传、读串口、照工装的方式判过不过，要人配合的步骤由脚本提示。其次，上游例程里和本板有关的也测通；和本板无关的从 core 里删掉。

## Notes

- **这张图带执行**：票定完就写代码和用例；先文档再代码，只做必要的
- **优先级**（用户 2026-09-29 定）：自有库 20 个必须先全过；上游里有关的其次；无关的删掉
- **判定方式照工装**：板子只报原始值，上位机判（[决策 22](../../docs/tables/DECISIONS.md)）。例程本身不加自检，这和 [Arduino 例程与 IDE 烧录流程](../arduino-examples-and-ide-flow/map.md) 定的「例程不自己判过不过」不冲突
- **人工配合**（用户 2026-09-29 定）：AO、DO 用户自己量；DI 用户按脚本提示从 0 到 24 V 加电压；KNX 用户在 ETS 里看总线、手动往总线发数据
- **台子**（用户 2026-09-29 说）：板子通电，RS485、CAN、KNX 都接上了，KNX 只接了总线电源；AO1、AO2 各接 470 Ω
- 现有的相关用例：P5 只编译、仿真用例 `T3-05` 只看启动，见 [HOW-TO-RUN-TESTS.md](../../docs/engineering/HOW-TO-RUN-TESTS.md)、[M3-app-runtime.md](../../docs/modules/M3-app-runtime.md)；工装判据在 `$PORTTOOL/TestCase/plans/station6-poweron.json`
- 开票 / 关票 / 算前沿照 [图与票的约定](../MAP-AND-TICKET-CONVENTION.md)

## 全集

```
find open_plc_arduino -name "*.ino"
```

2026-09-29 是 52 个：自有库 20，上游 32（含 `CI/build` 下 1 个，其中 3 个 P5 已排除）。关最后一张票前重跑，每个都要落在「有用例且通过」「删掉」「明确不测」三类之一。

## Decisions so far

- [KNX 库的 TP 收发怎么在本板上发出合法帧](issues/EXB-08-how-does-the-knx-library-drive-stknx.md)：现有 USART 路径不可能对；新写 STKNX 数据链路层用定时器收发 TP1，位时序照搬工装固件
- [KNX 和 EEPROM 往 flash 存数据时不能擦扇区 15](issues/EXB-09-knx-and-eeprom-must-not-erase-sector-15.md)：不提供模拟 EEPROM；KNX 两块数据放扇区 14；P19 盯住
- [测试脚本怎么判一个例程过没过](issues/EXB-01-how-does-the-script-judge-an-example.md)：认例程现有输出、判据在 Python 表里、经 USB CDC 上传、用例 `T3-06`

- [上游例程哪些和本板有关](issues/EXB-04-which-upstream-examples-relate-to-this-board.md)：测 2、留着不测 11、建议删 19；删前逐个问用户；`EEPROM` 和 KNX 会擦扇区 15

- [KNX 和 SDRAM 例程写死的引脚和本板对得上吗](issues/EXB-07-do-knx-and-sdram-examples-use-this-boards-pins.md)：引脚号基本对；KNX 例程头注释 19 处错、不开 RS232 使能所以无输出、库用 UART 驱动 STKNX 可能发不出合法帧

## Not yet specified

- **KNX 和 SDRAM 例程要不要改成 `OpenPLC_Ports` 的统一格式**：原来挂在 [Arduino 例程与 IDE 烧录流程](../arduino-examples-and-ide-flow/map.md) 的迷雾里，判定方式定了之后可能会变得必须回答

## Out of scope

- **AI_Inputs 这一轮不测**：用户 2026-09-29 定（跳线没焊，读数悬空）
- **AO、DO 的自动回读**：板上没有回读通道，用户自己量（2026-09-29 定）
