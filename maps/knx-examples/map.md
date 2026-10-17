# KNX 例程按正规用法重写

## 怎么看进度（不用问任何人）

```
python tools/list_wayfinder_map_frontier.py --all
```

## Destination

`OpenPLC_KNX` 只做 IP+TP 一种形式，板子当网关用（[决策 95](../../docs/tables/DECISIONS.md)）。只用 ETS 认识的模式。ETS 给 PLC 编程后和测试盒上的三台设备（IP 网关、温度传感器、继电器开关执行器，保留已有配置、不重新编程）互相控制，每条用例有对应的 Arduino 例程并在真板上通过；另有一个通用例程能打印总线报文、能发报文让别的设备动作。

## Notes

- **这张图带执行**：票定完就写文档、例程、用例；先文档再代码，只做必要的
- **用户 2026-10-09 定（[决策 95](../../docs/tables/DECISIONS.md)）**：只做 IP+TP，板子当网关，不要别的模式；先做打印总线报文、往总线发报文。**推翻了 10-03 的「只做 TP 设备」**；按 TP 设备定的票照旧成立，TP 设备仍是默认角色（[KEX-05](issues/KEX-05-which-examples-and-what-each-shows.md)）
- **用户 2026-10-03 定、仍有效**：例程（给用户照抄的 sketch）和用例（PC 侧在真板上证明它能用）一一对应；新的上板通过后旧的 5 个全删
- **前提**：新的 STKNX 数据链路层（[KNX 库的 TP 收发怎么在本板上发出合法帧](../core-examples-on-board/issues/EXB-08-how-does-the-knx-library-drive-stknx.md)）—— 2026-10-12 在新板上收发都通（[KEX-08](issues/KEX-08-board-sees-no-bus-pulses.md)），完整验收是 [TODO](../../work/TODO.md) 的 #22
- **产品文件、它的源 XML、KNX 模块的使用说明都放 `OpenPLC_ETS_Prod`**（用户 2026-10-03 定）
- 编程键、编程灯、总线状态脚各有坑，见 [HARDWARE-FACTS.md](../../docs/hardware/HARDWARE-FACTS.md)「KNX 接口」
- 开票 / 关票 / 算前沿照 [图与票的约定](../MAP-AND-TICKET-CONVENTION.md)

## 全集

```
(cd open_plc_arduino && find libraries/OpenPLC_KNX \( -name '*.ino' -o -name '*.knxprod' -o -name '*.md' \) && grep -rlE 'OpenPLC_KNX\.h|KNX\.' --include=*.ino --include=*.md . )
```

关最后一张票前重跑：每个 KNX 例程要么是新的且有用例，要么已删；每份产品文件和说明都对应新的例程。

## Decisions so far

- [ETS 下载把 bank2 整个擦了](issues/KEX-13-ets-download-erased-bank2.md)：`knx_nvm.cpp` 擦扇区前没设 `VoltageRange`，残值置了 `BER`；清零并设 `FLASH_VOLTAGE_RANGE_3`，P19 加查这一项，2026-10-13 上板复测通过
- [KNX 协议栈存 ETS 数据的区域多大](issues/KEX-12-knx-nvm-size.md)：统一 16 KiB，`MaxEntries` 2600（产品文件应用版本 4 → 5），协议栈调试输出默认关
- [板子 TP 不通时，IDE 里的总线监视要不要改走 IP 网关](issues/KEX-09-ide-bus-monitor-through-the-ip-gateway.md)：不做，TP 已通

- [执行器被总线写时不回报状态，用例怎么判它动了](issues/KEX-11-actuator-does-not-report-status-on-bus-write.md)：改判据，人看 A1 的灯；温度用例不写假温度，按室温从 RS232 设阈值
- 2026-10-10 用户认可非 1 位例程 `KNX_Analog`：对象 23–26（AI1 / AI2 / AO1 / AO2，表在 `$ETSPROD/README.md`），产品文件应用版本 3 → 4，用例 `T3-20`
- 2026-10-10 用户「没有用的就要删掉」：旧 5 个例程、导不进 ETS 的 `OpenPLC_Bridge.knxprod`、两路继电器配置和不经 ETS 自编程（`initRelayProfile2CH`、`selfProgram2CH`、`knx_profiles.*`）、无人调用的 `loadAppConfig` / `saveAppConfig` / `tpBusOk` / `tpVccOk` 已删

- [温度过阈值时板子的 DO2 出 24 V，阈值从 RS232 设](issues/KEX-10-temperature-threshold-drives-do2.md)：改 `KNX_Temperature`，默认 27 °C
- [板子的 KNX_RX 上看不到总线脉冲：先查哪一边](issues/KEX-08-board-sees-no-bus-pulses.md)：是板子硬件；2026-10-12 修好后收发都通
- [测试脚本能不能经 IP 网关直接收发组报文](issues/KEX-04-can-the-script-talk-through-the-ip-gateway.md)：能，经测试盒的 732 secure 开 xknx 隧道；ETS 同时连着也行
- [用例怎么判、人做哪几步](issues/KEX-06-how-does-each-test-case-judge.md)：`$TEST/tools/run_knx_box.py`，`T3-13`–`T3-20`；人只做 ETS 编程、按键、加撤 24 V、听继电器、看执行器的灯

- [「网关」指哪个角色](issues/KEX-07-which-role-is-the-gateway.md)：保留 TP 设备 0x07B0（默认）和 IP 网关 0x091A；0x5780、0x57B0 删掉

- [例程清单：每个演示什么](issues/KEX-05-which-examples-and-what-each-shows.md)：`KNX_Switch`（继电器）、`KNX_Inputs`（DI）、`KNX_Temperature`（对象 21 温度输入、22 过阈值开关输出）；开机打印地址，收发各打一行；角色不是 TP 编译报错
- [编程模式怎么进、怎么让人看到](issues/KEX-03-how-to-enter-and-show-programming-mode.md)：运行中短按 BOOT0 键切换；系统灯常亮 + 串口一行；脚本不代按
- [ETS 能导入的产品文件怎么做出来](issues/KEX-01-how-to-make-an-ets-importable-product.md)：OpenKNXproducer 4.3.12 + 本机 ETS 5.7 签名；ETS5 导入成功；厂家显示为 KNX Association
- [所有例程共用一个产品，还是一个例程一个](issues/KEX-02-one-product-for-all-examples-or-one-each.md)：共用一个产品；继电器开关 + 状态占 1–12、DI 占 13–20，已有编号永不改
## Not yet specified

- [端口和 KNX 对象的映射放进一个配置文件，工具生成产品文件和代码](issues/KEX-15-port-to-object-map-in-one-config.md)：已关；工具和配置在 `$ETSPROD`，2026-10-17 做完（M3 `R3-21`）

- [换成 IP 路由器后开机死机、隧道不回确认](issues/KEX-14-router-crashes-on-tp-data-and-drops-tunnel-frames.md)：隧道字节序已修；换角色死机等用户在 A / B / C 里选

- **IP 网关（0x091A）的 ETS 产品文件**：现有产品文件是 TP 设备的。OpenKNX 项目有一个 0x091A 的 IP 路由器应用，用 knxprod 由 ETS 编程（[knx-user-forum「OpenKNX IP-Router」](https://knx-user-forum.de/forum/projektforen/openknx/1917749-openknx-ip-router)），可作参照；做不做待用户定

- **ETS 参数**：现有产品文件没有参数；要不要做一个演示「在 ETS 里改参数、sketch 读到」的例程，没定
- **整块板当一个现成的 KNX IO 设备**：例程已共用一个整板产品（[KEX-02](issues/KEX-02-one-product-for-all-examples-or-one-each.md)），但没有一个例程同时用上全部对象；要不要做这样一个，没定
- **厂商号**：用户 2026-10-10 定「厂商号先叫 OpenPLC」。厂商号是 KNX 协会分配的编号，ETS 按编号显示厂商名，没登记前仍用共用测试号 `M-00FA`（ETS 里显示 KNX Association）；产品名、硬件名已是 OpenPLC

## Out of scope

- **本库自造的 IP+TP 双模（0x5780）、只接 IP 的设备（0x57B0）**：[决策 95](../../docs/tables/DECISIONS.md) 不要
