# KNX 例程按正规用法重写

## 怎么看进度（不用问任何人）

```
python tools/list_wayfinder_map_frontier.py --all
```

## Destination

`OpenPLC_KNX` 的例程按 KNX 的正规用法重写：板子作为 TP 总线设备，由 ETS 经网络上的 KNX IP 网关编物理地址、下载应用、关联组地址，之后能收发组报文；每个例程一条真板用例并通过，旧的 5 个例程删掉。

## Notes

- **这张图带执行**：票定完就写文档、例程、用例；先文档再代码，只做必要的
- **用户 2026-10-03 定**：例程（给用户照抄的 sketch）和用例（PC 侧在真板上证明它能用）一一对应；只做 TP 设备；ETS 经网络上的 KNX IP 网关接到总线；新的上板通过后旧的 5 个全删
- **前提**：新的 STKNX 数据链路层（[KNX 库的 TP 收发怎么在本板上发出合法帧](../core-examples-on-board/issues/EXB-08-how-does-the-knx-library-drive-stknx.md)）上板验收之前，任何例程都上不了总线
- **产品文件、它的源 XML、KNX 模块的使用说明都放 `OpenPLC_ETS_Prod`**（用户 2026-10-03 定）
- 编程键、编程灯、总线状态脚各有坑，见 [HARDWARE-FACTS.md](../../docs/hardware/HARDWARE-FACTS.md)「KNX 接口」
- 开票 / 关票 / 算前沿照 [图与票的约定](../MAP-AND-TICKET-CONVENTION.md)

## 全集

```
(cd open_plc_arduino && find libraries/OpenPLC_KNX \( -name '*.ino' -o -name '*.knxprod' -o -name '*.md' \) && grep -rlE 'OpenPLC_KNX\.h|KNX\.' --include=*.ino --include=*.md . )
```

关最后一张票前重跑：每个 KNX 例程要么是新的且有用例，要么已删；每份产品文件和说明都对应新的例程。

## Decisions so far

- [ETS 能导入的产品文件怎么做出来](issues/KEX-01-how-to-make-an-ets-importable-product.md)：OpenKNXproducer 4.3.12 + 本机 ETS 5.7 签名；ETS5 导入成功；厂家显示为 KNX Association
- [所有例程共用一个产品，还是一个例程一个](issues/KEX-02-one-product-for-all-examples-or-one-each.md)：共用一个产品；继电器开关 + 状态占 1–12、DI 占 13–20，已有编号永不改
## Not yet specified

- **ETS 参数**：现有产品文件没有参数；要不要做一个演示「在 ETS 里改参数、sketch 读到」的例程，得等产品文件怎么生成定了才看得清代价
- **不是 1 位的数据类型**（比如 AO 收 DPT 9 浮点设定值、AI 发测量值）要不要单独一个例程
- **整块板当一个现成的 KNX IO 设备**：如果所有例程共用一个整板产品，它可能自然就是这个；否则另议
- **板卡包菜单 KNX Role 的默认值**现在是 IP+TP（0x5780），这张图只做 TP：默认值要不要跟着改
- **旧 5 个例程删掉时**要同步的地方：P5 编译清单、`run_examples.py` 的表、README；库里那份导不进 ETS 的 `OpenPLC_Bridge.knxprod` 怎么处理
- **厂商号**：产品现在用开源 KNX 项目共用的测试厂商号 `M-00FA`；正式以 Schaeffer 名义发布要换成自己登记的厂商号

## Out of scope

- **KNXnet/IP 设备（0x57B0）、IP+TP 双模（0x5780）、IP/TP 耦合器（0x091A）**：用户 2026-10-03 定这一轮只做 TP 总线设备
