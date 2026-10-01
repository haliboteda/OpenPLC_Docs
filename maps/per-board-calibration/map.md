# 每块板校准 AI/AO，修正值写进扇区 15 并在 app 里生效

## 怎么看进度（不用问任何人）

```
python tools/list_wayfinder_map_frontier.py --all
```

## Destination

每块板在工装测试时校准 AI/AO：工装算出修正值、写进扇区 15 的校准值区、出厂重烧后仍在；用户 sketch 读 AI / 写 AO 时自动套用。精度指标按 IEC 61131-2 定，放在方案文件里能改。

## Notes

- **这张图带执行**：票定完就写代码；先文档再代码，只做必要的
- 已定的前提：[决策 61](../../docs/tables/DECISIONS.md)（校准值区在扇区 15 最前 8 KiB）、[决策 70](../../docs/tables/DECISIONS.md)（每块板都校准、整条链路、指标可改）
- **「修正值」和文档里的「校准值」是同一个东西**，见 [GLOSSARY.md](../../GLOSSARY.md)
- 工装那边已有的：多点测量和直线拟合（`$PORTTOOL/internal/ptcal`），结果只显示、不写板子
- 开票 / 关票 / 算前沿照 [图与票的约定](../MAP-AND-TICKET-CONVENTION.md)

## 全集

```
grep -rnil "calib" open_plc_cube_ide/IAPServer open_plc_cube_ide/TestCase/porttool OpenPLC_PortsTestingTool/internal OpenPLC_PortsTestingTool/cmd open_plc_arduino/cores open_plc_arduino/libraries/OpenPLC_*
```

要校准的通道以 [HARDWARE-FACTS.md](../../docs/hardware/HARDWARE-FACTS.md) 里 AI / AO 那几节为准。

## Decisions so far

- [IEC 61131-2 对模拟量精度规定了什么，同类产品标多少](issues/CAL-01-what-does-iec-61131-2-say-about-analog-accuracy.md)：标准不给数值，只要求声明误差项；同类输入 25 °C ±0.1 %、输出 ±0.3 %
- [修正值怎么写进板子，出厂重烧之后还在不在](issues/CAL-04-how-do-values-get-onto-the-board-and-survive-the-reflash.md)：工站 10 重烧只擦扇区 0–14，之后 JLINK 写扇区 15；系数先由 PC 按 UID 存档
- [校准哪些通道、每个通道用什么修正模型](issues/CAL-03-which-channels-and-what-correction-model.md)：AI1、AI2、AO1、AO2 四路，每路 5 点，直线（增益 + 偏移），温度不校准
- [AI / AO 的精度指标定多少](issues/CAL-02-what-accuracy-do-we-promise.md)：校准后 25 °C：AI ±0.1 % FS、AO ±0.3 % FS；全温先不声明；写在方案文件里
- [校准值区那 8 KiB 里放什么格式](issues/CAL-05-what-is-the-layout-of-the-8-kib-area.md)：魔数 + 版本 + UID + 每通道增益偏移 + CRC32；格式归 `$BOOT`，`P2` 盯两边一致
- [app 里怎么套用修正值](issues/CAL-06-how-does-the-app-apply-the-correction.md)：`OpenPLC_Ports` 给带单位的 API 并在那里套用；`analogRead` 不动；没校准值退回标称换算

## Not yet specified

- **工装面板上校准那一步长什么样**：要等写入路径和通道清单定了；面板那张图（工装面板的提示与功能核对）在暂停中

## Out of scope
