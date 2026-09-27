# Renode 能不能走 bootloader → app 的启动链

Type: research
Opened: 2026-09-27
Status: resolved
Blocked by: -

## Question

在 Renode 里烧入当前 bootloader 和一个签好名的 app（和 IDE 上传后 flash 里的内容一样），复位后 bootloader 能不能校验通过、跳进 app？卡住的话卡在哪个外设、能不能补。

## 怎么算答完

给出一套能复现的做法：Renode 里 bootloader 启动日志走完、跳进 `DO_Outputs`，DO1–DO8 按例程顺序开关；或者指出挡住它的外设模型缺口，以及补它要多大代价。

## Answer

2026-09-27 定。能：Renode 1.17.0 里当前 bootloader 验签通过、跳进签好名的 `DO_Outputs`，DO1–DO8 按例程顺序开关，不需要替 bootloader 做任何事。

做法（出处都是 2026-09-27 实测）：

| 步骤 | 做法 | 为什么 |
|---|---|---|
| flash 底色 | 整片 2 MiB 先填 `0xFF` | Renode 的空内存是 `0x00`，bootloader 会把它当成坏记录（owner 区报 32 条损坏、metadata 区报已满） |
| bootloader | `open_plc_cube_ide.bin` 放在 `0x08000000` | — |
| app | IDE 编出的 `.bin` 放在 `0x08020000` | — |
| 签名和证书 | `IAPTool sign <app.bin> <key>` 出 64 字节签名；`IAPTool cert --key=<key>` 出 128 字节自签证书。未认领板用随包的公开根 | 和 IDE 上传时发给板子的相同 |
| metadata | `0x081E2000` 放一条 224 字节 `'M'` 记录，格式照 `$BOOT/IAPServer/bootloader_state.c` 的 `iap_meta_rec_t` | 正常情况下由 bootloader 在上传成功时写入 |
| 加载 | 只用 `sysbus LoadBinary`；ELF 只 `LoadSymbolsFrom` | `LoadELF` 会按 `.data`/`.bss` 的 MemSiz 在 flash 加载地址处填零，清掉 owner 区和 app 开头（ST-Link 只写 FileSiz） |
| 复位向量 | `cpu VectorTableOffset 0x08000000` | — |

## 引出了什么新的未知

- metadata 记录由脚本按 `iap_meta_rec_t` 拼出来，和 bootloader 的格式是两份；bootloader 改格式时没有东西会报警。让 bootloader 自己写，要走一次真的上传，需要以太网或 USB CDC 在 Renode 里能用
- 平台里的以太网 MAC 后面没有 PHY 模型，bootloader 报 `Ethernet link is DOWN`
