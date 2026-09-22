# 要改的东西，一条不落

**这份是 [撤销叶证书 + bootloader 原地升级](map.md) 这张图的配套清单。**
它不是待办表（`work/TODO.md` 的准入要求每条挂一张**已关**的票，这些还没有）。
它回答的是：**这张图走完之后，实施要碰哪些地方，以及每一条该谁拍板。**

## 还没做的那几块，已经搬去 [work/TODO.md](../../work/TODO.md)

⚠️ **这份清单是实施全貌（含已完成的），不是待办表。**
开图时那几张票还开着，实施项挂不上「已关的票」、进不了 TODO（准入见
[WHERE-THINGS-LIVE.md](../../WHERE-THINGS-LIVE.md)），所以另起了这份。**票关之后它们就合规了，
2026-09-20 已经搬回 TODO** —— 四块：`flashboot` 原地升级、压缩 `'R'` 格式、
`setowner --wipe`、`RELEASE-NOTES.md` 改写。

**要知道「还剩多少活」看 TODO，不看这里。**

⚠️ 下面表格里的 `🤖` / `✅ 已定 <日期>` 说的是**谁拍板、决定定没定**，
**不是代码写没写**。两者曾经被混为一谈，结果是这份清单自己说不清还剩多少。

## 两列的含义

| 标记 | 意思 |
|---|---|
| 🍍 **要问** | 设计取舍 / 影响客户 / 改了不好回头。**必须用户拍板** |
| 🤖 **可直接做** | 有唯一正确答案，或纯机械，或只是调查。**不用问** |
| ⏳ **等票** | 形状还没定，等某张票关掉才动得了 |

---

## A · bootloader（`$BOOT` = `open_plc_cube_ide`）

| # | 改哪 | 改什么 | 谁拍板 |
|---|---|---|---|
| A1 | `IAPServer/owner_slot.h` | 新增 `'R'` 记录类型常量；撤销载荷布局（几个 × 几字节）；`_Static_assert` 锁尺寸 | 🤖 **已定 2026-09-20**（票 1：C / 16 字节） |
| A2 | `IAPServer/owner_slot.c` · `record_is_structurally_valid()` | 认 `'R'` 类型 | 🤖 **已定 2026-09-20** |
| A3 | `IAPServer/owner_slot.c` · `resolve_chain()` | 走链时比对撤销项（**不在 RAM 里建集合**，验证时直接扫）；`'R'` 强制要签名（无 TOFU 例外） | 🤖 **已定 2026-09-20** |
| A4 | `IAPServer/owner_slot.c` | 新增 `owner_slot_is_revoked(leaf_pubkey)` —— 比对前 16 字节 | 🤖 **已定 2026-09-20** |
| A5 | `IAPServer/owner_slot.c` | 新增 `owner_slot_revoke()` —— 追加 `'R'` 记录，验当前根签名 | 🤖 **已定 2026-09-20** |
| A6 | `IAPServer/owner_slot.c` | **`R4` 落地**：撤销项 == 当前生效的根公钥前 16 字节 → **忽略该项**（不拒整条，一条装 4 个人），并在启动日志喊一声 | 🤖 **已定 2026-09-20** |
| A7 | `IAPServer/owner_slot.c` · `report_root_trust()` | 启动日志加「owner 槽还剩 N 条」+ 撤销集合大小 | 🤖 |
| A8 | `IAPServer/iap_cert.c/.h` | **给 `iap_cert_verify()` 加一个参数**，让编译器保证每个调用点都处理撤销 —— 今天两个调用点：`iap_auth.c:122`、`IAP_server.c:428` | 🤖 **已定 2026-09-20** |
| A9 | `IAPServer/IAP_server.c` | 新增命令 `revoke` | ✅ **已实现并真板子验过**（`T2-19`/`T2-20`）|
| A10 | `IAPServer/IAP_server.c` | 新增命令 `flashboot` | ✅ **2026-09-22 已实现**（和 `flash` 同一条分支，`verb` 区分）—— 未上板 |
| A11 | `IAPServer/IAP_server.c` | 未认领时 `flashboot` 检查 `s_boot0_held` | ✅ **2026-09-22 已实现**（`owner_slot_root_is_public()` 且 `!s_boot0_held` → `Refused`）|
| A12 | **新文件** · 原地升级 | ✅ **2026-09-22 已实现** `IAPServer/boot_selfupgrade.{c,h}`（`.RamFunc`、关中断、不调 HAL）。⚠️ **写回时压缩还没做** —— 等 I 节，owner 区 8 KiB 原样搬 |
| A13 | 链接脚本 / 启动代码 | ✅ **不用改** —— `.RamFunc` 段已经收在 `.data` 里（`STM32H743IIKX_FLASH.ld:166-167`）、启动代码已经会拷贝。**只要用** | 🤖 **已定 2026-09-20**，核实过 |
| A16 | `owner_record_t.slots` | **删掉这个字段** | 🤖 **已定 2026-09-19** —— 变长记录不做了，它是个永远不触发的校验 |
| A17 | 构建尺寸 | 新增代码会涨。当前 **103,144 B**，上限 **122,880 B**，余 **19,736 B**。`CHK-A4` 自动卡 | 🤖 自动 |
| A18 | `IAPServer/iap_cert.h` | **删 `iap_cert_t.serial`**：`IAP_CERT_SIZE` 132 → **128**，`IAP_CERT_SIGNED_LEN` 68 → **64**，`_Static_assert` 跟着改 | 🤖 **已定 2026-09-19** |
| A19 | `iap_fw_metadata_t` | **删 `sha256[32]`**（全代码没人读）。新布局 `app_size 4 + signature 64 + cert 128 = 196` | 🤖 **已定 2026-09-19** |
| A20 | `IAP_METADATA_SLOTS` | **8 → 7 格**（196 字节要 7 个 32 字节格）。⚠️ **一次成功升级从 9 格降到 8 格** | 🤖 跟 A19 |
| A21 | `IAPServer/owner_slot.h` · `OWNER_FORMAT_VER` | **2 → 3**，硬切不做兼容 | 🤖 **已定** —— 见票 [加了 'R' 记录，format_ver 要不要升到 3](issues/OWN-03-does-format-ver-go-to-3.md) |

## B · PC 工具（`$TOOL` = `IAPTranfer_Tool`）

| # | 改哪 | 改什么 | 谁拍板 |
|---|---|---|---|
| B1 | `app.go` | 新增 `IAPTool revoke <ip> --key=owner.pem --leaf=<公钥>` | 🤖 **已定 2026-09-20** |
| B2 | `app.go` | 新增 `IAPTool flashboot <boot.bin> <ip>` | ✅ **2026-09-22 已实现** `RunEtherFlashBoot()` |
| B3 | `app.go` | 帮助文本、`Invalid mode` 那行的命令列表 | ✅ **2026-09-22 已实现** |
| B4 | `owner.go` | `RunRevoke()` —— 读板子的 generation + uid，拼签名前缀，签，下发，**再读回来确认** | 🤖 形状已定；⏳ 「已经撤过谁」怎么查还在迷雾 |
| B5 | `owner.go` | `RunFlashBoot()` | ⏳ 迷雾 |
| B6 | `iapcert/iapcert.go` | **整套删掉**：`serial` 字段、`SelfSignedSerial`、`NextSerial()`、`CounterPath()`、`.certserial` 文件 | 🤖 **已定 2026-09-19**（层①：删字段） |
| B7 | `iapcert/iapcert.go` | `Cert` 结构和 `SignedLen` 跟着改成 128 / 64 | 🤖 跟 B6 |
| B8 | `cert.go` | `issueLeafCert()` 去掉发号和 warning 返回值 | 🤖 跟 B6 |
| B9 | `$BOOT/IAPServer/keys/` | 删掉 `*.pem.certserial` 文件本身，以及 `keys/README.md` 里讲发号的那段 | 🤖 跟 B6 |
| B10 | `README.md` | 新命令的说明 | ✅ **2026-09-22 已实现**（`$TOOL/README.md` 「Replacing the bootloader」一节）|

## C · Arduino 板卡包（`$CORE` = `open_plc_arduino`）

| # | 改哪 | 改什么 | 谁拍板 |
|---|---|---|---|
| C1 | `libraries/OpenPLC_IAP/src/owner_root_ro.{c,h}` | **常量必须和 `owner_slot.h` 完全一致** —— 新增的 `'R'` 类型和载荷布局要同步 | 🤖 **可以做了 2026-09-20** |
| C2 | 板卡包版本号 / `boards.txt` | 发版时才动 | 🤖 |
| **C3** | `libraries/OpenPLC_IAP/src/iap_cert.{c,h}` | ⚠️ **2026-09-20 全集对账补** —— core 侧镜像的**不只是 `owner_root_ro`**。证书 132 → 128 字节、`IAP_CERT_SIGNED_LEN` 68 → 64 要同步到这里 | 🤖 已定，⏳ 跟 A18 |
| **C4** | `libraries/OpenPLC_IAP/src/iap_auth.{c,h}` | 同上 —— 会话认证那条路也镜像在 core 侧，证书长度变了要跟 | 🤖 已定，⏳ 跟 A18 |

## C-附 · 2026-09-20 全集对账补进来的（测试资产侧）

| # | 改哪 | 改什么 | 谁拍板 |
|---|---|---|---|
| **X1** | `$TOOL/TestCase/tools/inject_owner_record.py` | ⚠️ **它手工拼 owner 记录字节**（`T2-04` 靠它造「无签名的高 generation 记录」）。删了 `slots`、`format_ver` 升 3 之后**必须跟着改，否则那条用例造出来的是无效记录、测不到东西** | 🤖 已定，⏳ 跟 A16/A21 |
| **X2** | `$TOOL/TestCase/host/bootloader_unit/`（`owner_slot_stub.{c,h}`、`test_main.c`、`build.py`、`HOST-C-TESTS.md`） | ⚠️ **`T1-16` 拿真实 bootloader 源码在 PC 上跑**，包含 `owner_slot.c`。记录格式变了，桩和用例全要跟 | 🤖 已定，⏳ 跟 A1–A6 |
| **X3** | `$TOOL/TestCase/tools/check_mirror_sync.py` | 跨仓镜像清单要加 `iap_cert` / `iap_auth`（见 C3/C4），否则 `P2` 看不见它们分叉 | ✅ **本来就在查**（`check_mirror_sync.py:280-287,316-317`），这条写清单时没核实 |
| **X6** | `$TOOL/TestCase/tools/run_delegated_cert_on_real_board.py`、`run_rotate_root_revokes_old_leaf.py` | ⚠️ **2026-09-20 写新脚本时发现**：两个驱动都在标准输出里找 **264 个** hex 字符的证书（132 字节）。证书现在是 128 字节 = **256** 字符，**`T2-11` 和 `T2-12`–`T2-14` 的驱动本来会全部失败** | ✅ **2026-09-20 改完** |
| **X4** | `$PROD/docs/modules/M1/CHALLENGE-AUTH.md` | 讲会话认证怎么用证书。证书结构变了要跟 | 🤖 |
| **X5** | `$BOOT/IAPServer/SECURITY.md` | 同上 | 🤖 |

## 删字段带来的连锁，一条都不能漏

> 决定索引不在这里 —— 在 [地图](map.md) 的 `Decisions so far`，答案在各自的票里。
> 下面这几条是**改一处会牵动哪几处**，不是待拍板的事。

| # | 影响 | 谁拍板 |
|---|---|---|
| D9 | **需求 `R1-28`（一次成功升级 = 9 个 journal 槽）改成 8** | ✅ **2026-09-20 做完** |
| D10 | **用例 `T1-26` 的判据「差值 = 9」改成 8**，`run_journal_slot_accounting.py` 的期望值跟着改 | ✅ **2026-09-20 做完** |
| D11 | journal 回收频率从约 455 次一次变成 **512 次一次**，`M1-firmware-upgrade.md` 里那个数要改 | ✅ **2026-09-20 做完** |
| D12 | ⚠️ **手上那块板如果已认领（v2 记录），升到 v3 固件时会丢所有权，要手工重新 `takeown` 一次** | 🍍 **知会你**，不是决定 |

## F · 文档（`$PROD` = `OpenPLC_Docs`）

| # | 改哪 | 改什么 |
|---|---|---|
| F1 | `docs/modules/M2-ownership.md` | 新增「撤销」一节（格式 + 判断顺序 + `R4` 怎么落地） |
| F2 | 同上 | ✅ **2026-09-20 已改** —— 那段「下限连坐」的推理删掉了，换成「按叶公钥点名」并指向票 1 |
| F3 | 同上 | ✅ **2026-09-20 已改** —— 「等真实需求」的理由已删（离职换人是真实场景）。⚠️ **状态仍是 ⬜**：设计定了，代码还没写 |
| F4 | 同上 · 边界一节 | ⚠️ **「ST-Link 重烧 bootloader = 所有权重置」这句要改** —— 原地升级之后不再成立 |
| F5 | 同上 · BOOT0 那节 | 写进「没有有效 owner 能授权的操作一律物理在场」 |
| F6 | 同上 · 「定下来的取舍」表 | ✅ **2026-09-20 已标** `serial` 要删。⏳ `IAPServer/keys/README.md` 里讲发号那段等代码改完再动 |
| F7 | `docs/modules/M1-firmware-upgrade.md` | 新增 `flashboot` 通道—— ✅ **2026-09-22 已写**：`R1-34`–`R1-37` 四条需求 + `T1-29`–`T1-32` 四条用例（全 ⬜ 未跑），细节在 [FLASHBOOT.md](../../docs/modules/M1/FLASHBOOT.md) |
| F8 | `docs/tables/STATUS.md` | M2 条数变了；场景表「**同事离职，或他的叶私钥泄露了**」那一行的去向要改 |
| F9 | `docs/tables/DECISIONS.md` | 追加这一轮拍板的几条 |
| F10 | `docs/tables/ACCEPTANCE-CHECKLIST.md` | `CHK-B` 加一条「原地升级走一遍」 |
| F11 | `docs/engineering/HOW-TO-RUN-TESTS.md` | 新用例的跑法 |
| F12 | `$BOOT/RELEASE-NOTES.md` | 见 D8。⚠️ **这份文件是英文的**，草稿见下 |
| F13 | `GLOSSARY.md` | ✅ **2026-09-20 已加**：根/叶、认领、`'O'`/`'R'` 记录、原地升级、压缩 —— 未实现的都标了 ⚠️ |

## G · 测试用例（`$TOOL/TestCase`）

| # | 测什么 | 台子 | 测不到什么 |
|---|---|---|---|
| G1 | 撤销生效：被撤的叶子上传被拒 | 真板子 | —— |
| G2 | **撤销不连坐**：没被撤的叶子照常上传 | 真板子 | **正向对照，不可省** —— 没有它分不清「撤销生效」和「板子死了」 |
| G3 | 无签名的撤销记录被拒 | 真板子 | 出货工具做不出坏签名，要手工拼记录 |
| G4 | 撤不掉当前生效的根（`R4`） | 主机侧 | ✅ 2026-09-20 落成 `T2-21`。测不到真板子的 flash 行为，也测不到 bootloader 那份镜像 |
| G5 | 原地升级之后**所有权还在** | 真板子 | —— |
| G6 | 原地升级**顺手压缩了历史记录** | 真板子 | 判据是槽位数，要 ST-Link 复位读两次 |
| G7 | 未认领板子 `flashboot` 没按 BOOT0 → 被拒 | **真板子 + 人按 BOOT0** | —— |
| G8 | 升级镜像超尺寸 → **擦除之前**就被拒 | 真板子 | —— |
| G9 | 升级中掉电 → DFU 救回 → 日志报「上次被打断」 | **真板子 + 人工断电** | —— |
| G10 | 撤销记录被拷到另一块板上无效（`uid` 检查） | 真板子 | **要第二块板** —— 见 `waiting/WAITING-ON.md` |

⚠️ **G10 卡在第二块板上**，和 `R1-14`（两块板 MAC 不同）是同一个条件。

## H · `RELEASE-NOTES.md` 的草稿（英文，等用户改）

`open_plc_cube_ide/RELEASE-NOTES.md` 现在的 Upgrade rules 写着「换 bootloader 要重传 app **和**
重新认领」。原地升级做出来之后那句过期，换成：

```markdown
### Updating the bootloader

From this release the bootloader can be updated in place with `IAPTool flashboot`.
**Ownership and the installed application both survive the update** -- no ST-Link needed.

- The update requires a signature from the board's current owner. An **unclaimed**
  board additionally requires BOOT0 to be held through start-up.
- **Do not cut power during the update.** If power is lost the board will not start.
  Hold BOOT0 through a reset to enter the ST ROM DFU and re-flash the bootloader over
  USB; whether ownership survived depends on where it stopped, and the boot log says so.

⚠️ Re-flashing the bootloader over **ST-Link still wipes ownership** -- the owner records
live in the bootloader's own flash sector. Use `flashboot` to keep it.
```

⚠️ **这段有一条前提还没成立**：升到 `format_ver` 3 的那一次，v2 记录会被判无效，
**所有权仍然会丢**。所以「所有权会保住」这句话**从 v3 之后的版本之间才为真** ——
发布说明要把这一次切换单独说明。见票 [加了 'R' 记录，format_ver 要不要升到 3](issues/OWN-03-does-format-ver-go-to-3.md)。

---

## I · `'R'` 记录压缩到一个 flash word（2026-09-20 定，见 `DECISIONS.md` 58 / 59）

✅ **整节 2026-09-22 实现完毕**，链接通过（**105,296 字节，还剩 17,584**），selfcheck 24 项全绿。
⚠️ **一行都没上过板** —— v4 是硬切，要重烧 bootloader 并重新认领。

新布局：owner 区 8192 字节切两段，**`'O'` 32 条（5120 字节）+ `'R'` 96 条（3072 字节）**。
`'R'` 记录 32 字节 = `type`(1) + `reserved0`(1) + `format_ver`(2) + `uid`(12) + 叶公钥前 16 字节。
⚠️ **实现时把 `reserved0` 也纳入签名** —— 记录里没有签名字段要排除，「签的就是板子要写的那几个字节」
在这里能做到一个不差，所以签的是整条 32 字节，不是决策 58 里算的 31 字节内容。

| # | 改哪 | 改什么 | 谁拍板 |
|---|---|---|---|
| I1 | `$BOOT/IAPServer/owner_slot.h` | 拆出 `owner_revoke_rec_t`（32 字节）；`'O'` 段和 `'R'` 段各自的基址与条数常量；`_Static_assert` 锁两个尺寸 | ✅ **2026-09-22 已实现** |
| I2 | 同上 · `owner_record_t` | **删掉 union 里的 `revoked[4][16]`** —— `'R'` 不再共用这个结构体，`'O'` 只剩 `root_pubkey` | ✅ **2026-09-22 已实现** |
| I3 | 同上 · `OWNER_FORMAT_VER` | **3 → 4**，硬切不做兼容（沿用 `OWN-03` 的先例） | ✅ **2026-09-22 已实现** |
| I4 | `owner_slot.c` · `resolve_chain()` | 只扫 `'O'` 段建链；`'R'` 段**独立扫一趟**，只查结构（type / format_ver / uid），不验签、不看 generation | ✅ **2026-09-22 已实现** |
| I5 | `owner_slot.c` · `owner_slot_revoke()` | 写 32 字节记录；去掉 generation 检查；签名验完即丢；**写之前查重复，已存在则不写并回 `OK already revoked`**（`I-D1`） | ✅ **2026-09-22 已实现**，签名覆盖整条 32 字节 |
| I6 | `owner_slot.c` · `append_record()` | 拆成两个：`'O'` 往 `'O'` 段追加，`'R'` 往 `'R'` 段追加 | ✅ **2026-09-22 已实现**。`'R'` 只有一个 flash word，没有先写体后写头那一步 |
| I7 | `$CORE_REPO/libraries/OpenPLC_IAP/src/owner_root_ro.{c,h}` | 跨仓镜像，常量和两段扫描要完全一致 | ✅ **2026-09-22 已实现**（live 编译验过再拷进仓） |
| I8 | `$TOOL/owner.go` · `RunRevoke()` | 不再算 generation、不再发送它；签名改成覆盖新的 32 字节（整条记录） | ✅ **2026-09-22 已实现** |
| I9 | 主机侧 C 用例 | ⚠️ **原描述有误**：`T1-16` 的 owner 槽一直是**桩**，不是真实 `owner_slot.c`。真正跑真实代码的是 `host/owner_revoke/`（core 镜像）—— 已按两段布局改完并跑过；写入路径的主机覆盖由新增的 `host/owner_capacity/` 补上（见 I13） | ✅ **2026-09-22 已实现** |
| I10 | `$TOOL/TestCase/tools/inject_owner_record.py` | `T2-04` 靠它手工拼记录字节，布局变了必须跟 | ✅ **2026-09-22 已实现**（`format_ver` 4、`'O'` 段寻址不变；脚本本来就没有 `'R'` 路径） |
| I11 | `$TOOL/TestCase/tools/check_mirror_sync.py` | 两段的基址与条数加进镜像锚点，否则 `P2` 看不见它们分叉 | ✅ **2026-09-22 已实现**，新增 5 个锚点，`P2` 全绿 |
| I12 | `$PROD/docs/modules/M2-ownership.md` | 新布局的字节表、两段的划分理由、`'R'` 读取不验签这条 | ✅ **2026-09-22 已实现**（顺带修好了那节停在 v2 的旧字节表） |
| I13 | 用例 | **新增两条**：① 剩 8 条时启动日志出现提醒；② 第 97 个被拒且一个字节未写 | ✅ **2026-09-22 已实现** `T2-22`/`T2-23`，新建 `host/owner_capacity/` 在主机上跑真实 `owner_slot.c` 的写入路径（上板会永久烧掉全部 96 个名额） |

### I · 要你拍板的

| # | 问题 | 状态 |
|---|---|---|
| **I-D1** | 同一个叶被重复提交作废时怎么办 | ✅ **2026-09-20 定：幂等** —— 写之前扫一遍 `'R'` 段，那 16 字节前缀已存在就**不写记录**，回 `OK already revoked`。工具用 `strings.Contains(reply, "OK")` 判成功，所以这个应答既算成功又能把“已存在”显示出来。**这同时就是防重放** —— 重放一百次也只占一个 word |
| **I-D2** | `'R'` 段 96 条用满之后 | ✅ **2026-09-20 定**：**满了就不让添加**（回 `Refused`，一个字节不写）；**剩 8 条时启动日志开始提醒**，重点引导去**换根 + 重新授权**（`setowner`）而不是继续逐个作废。⚠️ **换根不腾空名额** —— 它让旧根签发的叶全部失效（所以**不再需要**逐个撤），但那 96 条记录仍占着 flash（读取不验签，板子无从分辨哪条属于哪一任根）。**真正回收名额只有两条路**：`flashboot` 原地升级时压缩（那半边还没做），或重烧 bootloader。**文案不得暗示「换根就能继续作废」**。⚠️ **2026-09-20 补**：用户希望换根时**把 `'O'`/`'R'` 两段全清空重写** —— 那会让名额真的回收，但把 `setowner` 变成擦扇区 0 的高风险操作，已单独开票：[换根的时候把 owner 区清空重写](issues/OWN-07-should-setowner-wipe-the-owner-area.md) |
| **I-D3** | `revoke` 要不要支持一次提交多个叶 | ✅ **2026-09-20 定：不做**。今天没有具体场景，而代价是命令格式变复杂 + 要回答「写了 3 条第 4 条失败怎么办」。单条命令跑 N 次效果相同 |
