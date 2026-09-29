# 上游例程哪些和本板有关

Type: research
Opened: 2026-09-29
Status: resolved
Blocked by: -

## Question

core 里 32 个上游例程（`Wire`、`EEPROM`、`Servo`、`SoftwareSerial`、`SPI`、`SubGhz`、`SrcWrapper`、`RGB_LED_TLC59731`、`Mouse`、`Keyboard`、`IWatchdog`、`CMSIS_DSP`、`CI/build`），每一个在本板上有没有意义：它要的外设 / 引脚本板有没有、引出到端子没有、要什么外接器件；删掉它会不会影响别的东西（P5、上游同步）。出处只认原理图、网表和芯片数据手册。

## 怎么算答完

一张表，32 行，每行：例程、要什么、本板有没有（带出处）、建议「测」「删」「留着不测」及一句理由。

## Answer

2026-09-29 定（查源码和硬件资料，未上板）。32 个里：**测 2 个**（`arm_sin_cos_example_f32`、`IWDG_Button`）；**留着不测 11 个**（`Wire` 9 个要外接 I2C 器件，`SrcWrapper/BareMinimum` 是 core 依赖的库，`CI/build/BareMinimum` 是上游 CI 输入）；**建议删 19 个**（`EEPROM` 8、`Servo` 3、`SoftwareSerial` 2、`SPI` 2、`Keyboard`、`Mouse`、`SubGhz`、`RGB_LED_TLC59731` —— 本板没有那个外设，或写死的脚落在板内功能脚上）。删除只影响 P5 少编几个，`EXCLUDED` 里三条会变成死条目。逐个见 [EXB-04-findings.md](../EXB-04-findings.md)。**真删之前逐个问用户。**

## 引出了什么新的未知

- `EEPROM` 库自动选中 `0x081E0000`（扇区 15），`OpenPLC_KNX` 的应用 NVM 也写死在这里，写一次就擦掉校准值和 metadata → 升格为票 [KNX 和 EEPROM 往 flash 存数据时不能擦扇区 15](EXB-09-knx-and-eeprom-must-not-erase-sector-15.md)
- 删除清单要用户逐个确认 → 记进 [work/TODO.md](../../../work/TODO.md)
