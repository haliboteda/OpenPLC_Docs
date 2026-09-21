# ST-Link 直连的版本回退防不防

Type: grilling
Opened: 2026-09-21
Status: resolved
Blocked by: -

## Question

上位机侧的版本比对只盖住 CDC / ETH 两条烧录路径（[boards.txt](../../../../open_plc_arduino/boards.txt) 的 `menu.upload_method`）。
**STM32CubeProgrammer 的 SWD 和 Serial 两条路直接烧 flash，天然绕过任何检查。**

要不要防？市面 PLC 怎么做？

## 怎么算答完

1. 列出技术上能防的手段，以及每个手段的代价
2. 给出结论：防还是不防
3. 不防的话，**写明要在文档里交代哪几句**

## Answer

2026-09-21 定

**不防。把说明写清楚，留给客户自己决定。**

### 手段和代价

| | 效果 | 代价 |
|---|---|---|
| **RDP Level 1** | 调试口能连，但一连就**触发全片擦除** | 防得住「读出固件」，**防不住「擦掉重烧旧版本」** |
| **RDP Level 2** | **永久禁用调试口**，ST-Link 根本连不上 | ⚠️ **不可逆**，且同时废掉「BOOT0 恢复出厂」和「ST-Link 救砖」两条现有能力 |
| **WRP** | 写保护指定扇区 | 项目已定「厂商不上，留给客户自己决定」——见 [M2-ownership.md](../../../docs/modules/M2-ownership.md) 第 6 节 |

**市面 PLC 通常是三层叠加**：RDP Level 2 + 调试口不引出到外壳 + 防拆。
⚠️ 但 [防回滚](../../anti-rollback/map.md) 里已核实过一条：**Siemens / Beckhoff 只查得到「验不验签」这一层**，
再往下 bootloader 闭源，用没用 RDP2 查不到。

### 要写进说明的三句话

1. **不防的是什么**：物理接触 + SWD/Serial 直连烧写可以装任意版本，版本检查完全绕过
2. **为什么不防**：唯一有效的手段是 RDP Level 2，它不可逆，会同时废掉恢复出厂和救砖
3. **客户要防怎么做**：自己设 RDP Level 2 / WRP，并承担不能再调试和救砖的后果 ——
   和 `M2-ownership.md` 里 WRP 那条同一个口径

## 引出了什么新的未知

没有。
