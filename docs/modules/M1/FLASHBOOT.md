# `flashboot` · bootloader 原地升级

**一条命令把新的 bootloader 写进扇区 0，同时把 owner 记录原样搬过去。**
类比 BIOS 升级：**中途不允许断电**。

形状定于 2026-09-19（走原地升级、用 owner 根验签、没有有效 owner 就要物理在场），
线上协议定于 2026-09-22，见[`flashboot` 的线上协议长什么样](../../../maps/owner-revoke-and-boot-upgrade/issues/OWN-12-what-does-the-flashboot-wire-protocol-look-like.md)。

## 线上长什么样

```
flashboot <size> <crc32hex> <imgsig_hex> <cert_hex> <noncesig_hex>
```

**逐字段和 `flash` 相同**，传输与 SDRAM 暂存走同一条路。四处不同：

| | `flash` | `flashboot` |
|---|---|---|
| `imgsig` 用谁验 | `cert` 里那把叶公钥 | **owner 根公钥**（`owner_slot_root()`） |
| 尺寸上限 | `IAP_APP_MAX_SIZE`（1792 KiB） | **120 KiB**（`OWNER_SLOT_BASE - FLASH_BASE`） |
| 落盘目标 | `IAP_APP_ADDRESS` | **扇区 0**（`0x08000000`） |
| 落盘之前 | 无 | 把 owner 区 8 KiB 搬进 SDRAM；擦完**先写 owner 再写 bootloader** |

`cert` / `noncesig` 的作用不变 —— 会话认证与防重放，和 `flash` 同一条路。

**叶证书换不掉 bootloader。** 一把发给「只准烧 app」的叶，凭同一张证书也能换掉 bootloader，
而换 bootloader 和换所有权是同一个量级的动作。

**未认领的板子没有根可验**，走物理在场（`s_boot0_held`），和 `takeown` 同一条规则 ——
「没有有效 owner 可以授权的操作，一律要物理在场」。

## 擦写为什么必须在 RAM 里跑

擦扇区 0 的时候，执行擦除的代码本身住在扇区 0。所以整个擦写例程标 `.RamFunc`
（链接脚本已经把这个段收进 `.data`、启动代码已经会拷贝，**不用改脚本**），
全程关中断 —— 向量表也在扇区 0 —— 且不调 HAL，直接写 FLASH 寄存器序列，因为 HAL 在 flash 里。

## 顺序为什么是「先 owner 后 bootloader」

掉电落在两次写之间时，owner 记录已经在了、bootloader 还没有：板子起不来，但**所有权还在**。
反过来则是所有权没了、板子回落到出厂根，**谁按 BOOT0 谁就能占走它**。

## 断在哪会怎样

| 断点 | 板子的状态 | 怎么救 |
|---|---|---|
| 传输 / 校验 / 验签 | 一个字节没写，bootloader 照常 | 重发 |
| 擦完，写 owner 之前 | 起不来，所有权没了 | ST-Link 重烧 + 重新认领 |
| 写完 owner，写 bootloader 之前 | 起不来，**所有权还在** | ST-Link 重烧 |
| 写完 | 正常重启进新 bootloader | —— |

⚠️ **扇区 15 不受影响** —— `STM32_Programmer_CLI -w <elf>` 只擦 ELF 占的那些扇区，
所以 ST-Link 救砖不会带走 metadata 和校准值。

## 现在不做的

**压缩 owner 记录**（丢掉历史 `'R'` 快照、只留完整有效链）要等 `'R'` 记录压缩到一个 flash word
那批改完 —— 见 `maps/owner-revoke-and-boot-upgrade/CHANGE-LIST.md` 的 I 节。
在那之前 `flashboot` 把 owner 区 **8 KiB 原样搬过去**。
