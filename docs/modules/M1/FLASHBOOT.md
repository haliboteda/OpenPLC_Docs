# `flashboot` · bootloader 原地升级

**一条命令把新的 bootloader 写进扇区 0，同时把 owner 记录压缩后搬过去。**
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
| 落盘之前 | 无 | 把 owner 区**压缩**进 SDRAM 的 8 KiB；擦完**先写 owner 再写 bootloader** |

`cert` / `noncesig` 的作用不变 —— 会话认证与防重放，和 `flash` 同一条路。

**叶证书换不掉 bootloader。** 一把发给「只准烧 app」的叶，凭同一张证书也能换掉 bootloader，
而换 bootloader 和换所有权是同一个量级的动作。

**未认领的板子没有根可验**，走物理在场（`s_boot0_held`），和 `takeown` 同一条规则 ——
「没有有效 owner 可以授权的操作，一律要物理在场」。

## 擦写为什么必须在 RAM 里跑

擦扇区 0 的时候，执行擦除的代码本身住在扇区 0。所以整个擦写例程标 `.RamFunc`
（链接脚本已经把这个段收进 `.data`、启动代码已经会拷贝，**不用改脚本**），
全程关中断 —— 向量表也在扇区 0 —— 且不调 HAL，直接写 FLASH 寄存器序列，因为 HAL 在 flash 里。

代码落在 `RAM_D1`（`0x24000000`），**那里可执行** —— MPU region 0 把子区 1
（`0x20000000`–`0x3FFFFFFF`）排除在外（`SubRegionDisable = 0xC7`，见 `Core/Src/main.c` 的 `MPU_Config()`），
落回默认内存图，SRAM 在那里不是 XN。

⚙️ **链接时会多一条 `LOAD segment with RWX permissions`** —— `.RamFunc` 进了 `.data`，
那个段就同时可写可执行。这是要的效果，已在 `$TOOL/TestCase/tools/build_image.py`
的 `KNOWN_WARNINGS` 里按原文匹配放行。

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

## 顺手压缩：擦扇区是回收槽位的唯一时机

owner 区只能追加，槽位用掉就回不来 —— **除非整个扇区被擦掉**，而这正是 `flashboot` 干的事。
所以压缩就挂在这里，`owner_slot_compact()`（`$BOOT/IAPServer/owner_slot.c`）。

| 段 | 留什么 | 丢什么 |
|---|---|---|
| `'O'` | **链真正走过的那几条**，按走过的顺序前移 | 坏格式、写了一半、以及**链没走到的** |
| `'R'` | 还生效的作废，前移 | 坏格式、别的板子的、以及点名当任根的（R4 本来就忽略） |

⚠️ **链没走到的 `'O'` 记录必须丢，不能前移。** 链遇到一条验不过的就地停住，
后面那些从来没被评判过。把坏的那条删掉、后面的留下，等于让压缩替攻击者
把验证器拒绝过的那一环扶正 —— 这是这个函数唯一真正危险的地方。

**压缩在关中断之前跑完**，用的是普通代码：那时 flash 还读得到、`printf` 还出得来。
`ram_burn()` 只负责把交给它的那 8 KiB 写下去，一个判断都不做。

**压缩拒绝时原样搬过去。** 板子已认领、压出来的链却是空的，那是这个函数自己出了问题；
这时候回收不了槽位无所谓，丢了所有权没有任何办法补救。

判据见 `T1-33`（[M1 固件升级](../M1-firmware-upgrade.md)）—— 主机上跑真实的
`owner_slot.c`，压完再把结果当新 flash 重扫一遍。

## 镜像尺寸

加完 `flashboot`、压缩和 `setowner --wipe` 后 bootloader **106,324 字节**，122,880 的预算还剩 16,556（2026-09-22 实测）。
