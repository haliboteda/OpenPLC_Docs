# metadata 从 journal 扇区搬进 app 头部

Status: paused
Paused because: **2026-09-21 用户改了方向，这张图的终点已作废** —— metadata **不搬**，
留在扇区 15；journal 只删事件日志；校准值放扇区最前 8 KiB。
新路线在 [烧录前比版本 + 校准值住进扇区 15](../version-gate-and-calibration/map.md)。

> ⛔ **这张图已归档，六张票全部关闭，不要再从这里开工。**
> 仍然成立的结论已经搬进新图的 `## 从这张图继承的结论`，**下面整份保留备查**。
> 作废的是三条：选 S-e（header 放 app 镜像开头）、S-e 的安全模型、业界对标（元数据跟镜像走）。


## 怎么看进度（不用问任何人）

```
python tools/list_wayfinder_map_frontier.py --all
```

> 打出每张票是 `TAKEABLE` / `claimed` / `resolved` / `paused`，以及谁挡着谁。**别凭记忆，跑它。**

## 还要你拍几次板（**提前列出来，免得被逐个突袭**）

| 还剩几次 | 要你定什么 | 哪张票 |
|---|---|---|
| 1 | **header 里放什么** —— magic、`format_ver`、padding、编译期断言。⚠️ **「分几段」（两段式 / 三段式）2026-09-21 用户划掉，不再讨论** | [header 那一千多字节里放什么](issues/HDR-05-what-goes-in-the-header.md) |
| 2 | 发布和现场迁移怎么走 | [这次变更怎么发布，现场的板子怎么迁移](issues/HDR-06-how-does-this-ship-and-migrate.md) |

**还要你动一次手**：[VTOR 对齐到底要多少字节](issues/HDR-04-what-is-the-real-vtor-alignment.md) 要在真板子上验一次跳转。

> 2026-09-20 已关掉三张：换主语义、日志去留、扇区归属。

## header 现在长什么样（低分辨率，详情在票里）

**已经定死的**：

| 字段 | 字节 | 为什么必须 |
|---|---|---|
| `app_size` | 4 | 定哈希范围。不记它就必须每次全擦 app 区 |
| `signature` | 64 | 对 app 内容的背书 —— **公钥本身验证不了任何东西** |
| `cert` | 128 | 证明该用哪把公钥验，且那把公钥被根认可 —— **只缓存叶公钥不安全** |
| **合计** | **196** | |

**header 的总大小由 VTOR 对齐决定，不由内容决定** —— 推导值 **1024 字节**（H743 最大中断号 149 ⇒ 向量表 664 B ⇒ 向上取整到 2 的幂）。也就是说**约 828 字节是 padding**，实测确认在 [VTOR 对齐到底要多少字节](issues/HDR-04-what-is-the-real-vtor-alignment.md)。

**还没定的**（都在 [header 那一千多字节里放什么](issues/HDR-05-what-goes-in-the-header.md)）：分几段、要不要 magic、要不要 `format_ver`、padding 填什么、哈希范围的两端、要加哪几条 `_Static_assert`。

⚠️ **那 828 字节 padding 能放什么，判据是一句话**：**这个数据和这份固件是不是同生共死？**
是 → 可以进 header（版本号、构建时间、SBOM 哈希）；不是 → 必须住扇区 15（校准值、防回滚计数器）。

## Destination

firmware metadata（`app_size` + `signature` + `cert`）**从独立的 128 KiB journal 扇区搬进 app 镜像开头的定长 header**，
`IAP_STATE_SECTOR_ADDR` 那个扇区从此不再被 bootloader 用于启动判定。

**这张图产出设计定稿** —— 每处要改的东西有形状、有判据，可以交给实施。**不写代码。**

## Notes

- 域：[M1 固件升级](../../docs/modules/M1-firmware-upgrade.md)、[M2 归属与信任](../../docs/modules/M2-ownership.md)、[Journal 设计说明](../../docs/modules/M1/SECTOR-15.md)
- **先文档再代码** —— 定稿先进 `M1-firmware-upgrade.md`，再动 `$BOOT`
- 这次变更**同时动三个仓**：`$BOOT`（判定与写入）、`$CORE_REPO`（`build.flash_offset`）、`$TOOL`（6 个测试脚本的硬编码基址）。
  ⚠️ **`upload.maximum_size` 本来就是跨仓镜像项**（`boards.txt:37` 的注释明写「must equal IAP_APP_MAX_SIZE」），这次是在已有耦合点上多改一个数，不是新开口子
- **IAPTool 本体零改动** —— `flash <size> <crc> <sig> <cert> <noncesig>` 协议不变，header 由板子自己填
- 开票 / 关票 / 算前沿照 [图与票的约定](../MAP-AND-TICKET-CONVENTION.md)

## 全集

这张图会碰到的所有文件，由这条命令算出来（找的是「谁提到 app 基址、journal、或者编译期的 flash 偏移」，不是「我们打算在哪找」）：

```
grep -rln --include=*.c --include=*.h --include=*.go --include=*.py --include=*.md --include=*.txt --include=*.ld \
  -e 0x08020000 -e 0x8020000 -e 1835008 -e IAP_APP_ADDRESS -e IAP_APP_MAX_SIZE \
  -e bootloader_state -e journal -e JOURNAL -e flash_offset -e VECT_TAB_OFFSET \
  /e/WorkSpace/Schaeffer-AG
```

### 2026-09-20 首次对账

去掉 `.metadata/`、`Middlewares/`、`Drivers/CMSIS/`、本图自己的 `maps/` 产物，以及三个不属于本产品的目录之后，命令输出 **52 个文件**。开图时的讨论只点到其中一部分，**这次对账抓出四处原先没想到的**：

| 漏的 | 为什么要紧 |
|---|---|
| **`$BOOT` 自己的两份链接脚本**（`STM32H743IIKX_FLASH.ld` 和 `STM32H743IIKX_FLASH_PORTTOOL.ld`） | bootloader 侧也有 flash 布局常量，改 app 起点时要一起核对 |
| **`$CORE_REPO/tools/platformio/platformio-build.py`** | PlatformIO 那条构建路径**不读 `platform.txt`**，`build.flash_offset` 改了它不会跟着变 |
| **`$BOOT/tests/bootloader_unit/stubs/bootloader_state_stub.c`** | `T1-16` 拿真实 bootloader 源码在 PC 上跑，删掉 journal 之后这个桩整个失效 |
| **`ref/Hello_World_OpenPLC/Core/Src/system_stm32h7xx.c`** | 是对照不是权威，**不改** —— 但它是「app 侧 VTOR 怎么设」的现成参照，验 `HDR-04` 时用得上 |

⚠️ 输出里有一处误命中：`$CORE_REPO/libraries/STM32duino_LwIP/src/netif/ppp/polarssl/des.c`，与本图无关。

## 开图过程中撞见的文档漂移（**都还没改**）

2026-09-20 讨论这张图时顺带核出五处「文档说的和代码不符」。**四处会被本图的实施吸收，一处不会**：

| 哪里 | 文档说 | 代码实际 | 谁来收 |
|---|---|---|---|
| [`SECTOR-15.md`](../../docs/modules/M1/SECTOR-15.md) 扫描流程图 | `'M'（8格）… i += 8` | `i += IAP_METADATA_SLOTS`（**7**） | 本图（该文件整份重写或废弃） |
| 同上，写入流程图 | `追加 M 记录（8格）` | `journal_write(&rec, 7)` | 同上 |
| 同上，写入流程图 | `剩余格子 < 8` | `journal_room() < 7` | 同上。⚠️ **这处有实际后果**：剩正好 7 格时代码直接追加，追加完剩 0 格，那条 `UPDATE_OK` 日志写不进去 |
| `$BOOT/IAPServer/bootloader_state.h` 头部注释 | journal 满状态 "reported at boot and **in the identity string**" | `iap_identity_string()` 只看 `app_is_valid`，**identity 里没有** | 本图（[八种事件日志留不留](issues/HDR-02-do-the-event-logs-survive.md) 会重写这段） |
| ~~[`M2-ownership.md`](../../docs/modules/M2-ownership.md) `R2-04` 旁注~~ | ~~「状态仍是 ⬜ —— 代码一行还没写」~~ | 撤销已实现（commit `294fb20`） | ✅ **另一个会话 2026-09-20 17:5x 正在改，已在工作区**（未提交）。不属于本图，**本图不要碰它** |

## Decisions so far

**以下八条 2026-09-20 在对话里定，开图之前就已成立**，所以没有对应的票：

- **metadata 砍不得** —— 它支撑四条需求：`R1-26`（app 的签名在每次启动时被重新校验）、`R1-27`（掉电中断升级后板子仍可恢复）、`R1-28`（metadata 和事件记在 journal 里）、以及**跨模块的 `R2-04`（撤销叶子证书，回溯作废已装固件）**。最后那条写在 M2、实现却整个寄生在 metadata 的 `cert` 字段上，**最容易漏**
- **「掉电恢复」不是 metadata 的独立功能** —— 它是启动校验在「app 被写坏」这个输入下的表现，**不占任何额外字节**。`T1-21`（掉电落在传输期）真正靠的是 SDRAM 暂存区设计，`T1-22`（掉电落在擦写窗口）靠的就是启动校验本身
- **append-only 是 metadata 自己逼出来的，不是为了日志** —— NOR flash 最小擦除单位是整扇区，原地改写 metadata 等于每次升级擦一次；**metadata 跟 app 一起写之后，这个理由消失，journal 就没有存在必要了**
- **事件日志支撑 0 条需求、零读出路径** —— `dropped_events()` / `journal_full()` / `auth_fail_log()` / `auth_fail_count()` 四个导出函数在 `bootloader_state.c` 之外**零调用者**；上位机 grep `journal` 零命中。唯一被消费的是 `last_log_event()`，用途是给日志**自己**去重
- **尾附「哈希」不安全，尾附「签名 + 证书」安全** —— 差别不在位置，在**锚**：哈希没有锚，改镜像的人一次写入就把它一起改了；证书的 `root_sig` 锚在 owner 区，改镜像的人够不着。**开源不影响这一条 —— 安全来自密钥，不来自格式保密**
- **只缓存叶公钥（不存整张 cert）是不安全的** —— 缓存的公钥没有任何东西约束它是否被认可，攻击者追加一条自带公钥 + 自带签名的记录就能通过。`bootloader_state.h` 里那句 `do not add one` 拦的是这个
- **`app_size` 必须记** —— 不记就必须每次全擦 app 区（否则分不清「这一版的最后一个字节」和「上一版残留的第一个字节」），还要每次启动算满 1792 KiB 的哈希，并让上位机新增一个跨仓常量。**「不记长度 + 不全擦」在原理上不成立**
- **业界对标：元数据跟镜像走是主流，独立 append-only 扇区没查到先例** —— ESP32 Secure Boot v2 的签名块紧跟镜像。⚠️ **PLC 厂商（Siemens / Beckhoff）只查得到「验不验签」这一层，查不到「元数据存哪」** —— 他们的 bootloader 是闭源的

**以下两条 2026-09-20 由用户拍板，同样没有票：**

- **选 S-e：header 放 app 镜像开头** —— 相比放尾部（S-a），它**不需要额外擦一个 128 KiB 扇区**，也没有「忘记擦」这个坑，代价是要改 `build.flash_offset`（一个数字）并因 VTOR 对齐浪费约 800 字节
- **S-e 的安全模型不比今天差** —— 锚没动（`cert.root_sig` 仍验 `owner_slot_root()`，那把根在 owner 区，既不在 app 区也不在 journal 扇区）。逐项比过：物理接触者两者都挡不住（一样的路）；走 IAP 上传两者同一段代码；**唯一有差别的「app 提权改 flash」路径上，门槛同样是「造不出 `root_sig`」**；降级攻击两者都不挡（`a92a8c7` 早已移除 anti-rollback）。**S-e 还消除了「认哪一条 metadata」的歧义**（位置唯一，不像 append-only 要认物理最后一条）。失去的是取证历史，而那个能力已核实零读出路径。⚠️ **唯一新增的是一类实现风险** —— 哈希起点算错会让向量表开头漏出签名覆盖，详见 [header 那一千多字节里放什么](issues/HDR-05-what-goes-in-the-header.md)，那张票要产出编译期约束来兜住
- **撤销只管未来** —— 叶 a 被撤销后，**已经装在板子上的、a 签的固件照常启动**；a 再上传仍然被拒。理由：`R2-04` 记录在案的需求是「员工离职换人」（持证几人到十几个，换人频率不定），离职一个同事不该让他经手过的板子集体停机。⚠️ **`T2-15`（撤销回溯作废已经装上的固件）判据要重写**，它 2026-09-20 刚在真板子上通过

**以下两条有自己的票：**

- [换主之后，旧根签的固件还能不能启动](issues/HDR-01-does-setowner-still-invalidate-installed-firmware.md)：**不能，停在 bootloader —— 维持今天的行为，不跟撤销走同一个语义**。两者问的不是同一个问题：撤销问「这个人还值不值得信」，换主问「这块板还是不是你的」。header 因此仍存整张 `cert`，196 字节不变
- [八种事件日志留不留，留的话住哪](issues/HDR-02-do-the-event-logs-survive.md)：**全删，连 `JOURNAL.md` 一起删**。「日志满了靠什么回收」这个问题随之消失；state 扇区**完全**空出来，不是部分
- [让出来的 128 KiB state 扇区给谁](issues/HDR-03-who-gets-the-freed-sector.md)：~~留给 bootloader 侧，归校准值~~ ⚠️ **2026-09-21 用户重开** —— 「补偿值不一定非要存在扇区 15」，归属待重议。原结论的理由是排除法之后的唯一去处 —— 板上**没有 EEPROM**、microSD 可拔插、RTC 备份寄存器会随电池丢失且撞过车、app 区和 header 每次升级被擦重写。附带解掉第 45 条那个「reclaim 搬运校准值、掉电就丢」的既存冲突。⚠️ **本票不改 `IAP_APP_MAX_SIZE`** —— 它会因 header 而变，那是另一张票的事，别重复改
- [VTOR 对齐到底要多少字节](issues/HDR-04-what-is-the-real-vtor-alignment.md)：**header 取 1024**。真板子实测硬件只强制 128（`TBLOFF = bit[31:7]` 坐实），1024 来自架构规则「对齐 ≥ 向量表长度取整到 2 的幂」，664 → 1024，**那一半测不了也不必测**

## Not yet specified

2026-09-24 清理：本图已归档（metadata 不搬）。`R1-32` 两行塌缩、`P2` 纳入 `build.flash_offset`、bootloader 带 header 三条都以「要搬」为前提，不再成立；`AUTH_FAIL` 环形缓冲那条转入 [TODO「等外部」](../../work/TODO.md)。

## Out of scope

- **`flashboot` bootloader 原地升级** —— 在 [撤销叶证书 + bootloader 原地升级](../owner-revoke-and-boot-upgrade/map.md) 那张图里，**两张图并行**。本图不碰 bootloader 自身的升级路径
- **给 flash 上写保护（WRP）** —— `M2-ownership.md` 已记载「太锋利，留给客户自己决定」，本图不重开
- **`sha256` 硬件加速** —— 现在是纯软件实现（`IAPServer/sha256.c`）。S-e 下哈希范围不变（仍是实际镜像大小），**这次变更不改变哈希成本**，所以不在本图范围
