# 撤销叶证书 + bootloader 原地升级

## 怎么看进度（不用问任何人）

两条，加起来就是全部状态：

```
python tools/list_wayfinder_map_frontier.py --all
```

> 打出每张票是 `TAKEABLE` / `claimed` / `resolved` / `paused`，以及谁挡着谁。**别凭记忆，跑它。**

## 还要你拍几次板（**提前列出来，免得被逐个突袭**）

| 还剩几次 | 要你定什么 | 什么时候会问 |
|---|---|---|
| **0** | **设计全部走完，眼下没有要你拍板的** —— 剩下的都是 🤖 实施 | —— |
| —— | 另有一张调查票：[有些叶证书驱动不了重启握手](issues/OWN-08-some-leaf-certs-cannot-drive-the-reboot-handshake.md)，**不阻塞作废那套** | 要先做一个能说话的探针 app |
| 1 | `flashboot` 的线上协议：帧格式、分块、和现有 `flash` 共用多少 | 形状定了之后 |
| 2 | 撤销之后，客户怎么知道「哪几块板上的固件需要重传」 | 同上 |
| 4 | 发布说明怎么改（草稿在 [CHANGE-LIST.md](CHANGE-LIST.md) 的 H 节，英文） | 代码落地前 |

**不用你定的**：[要改的东西，一条不落](CHANGE-LIST.md) 里标 🤖 的那些，形状已经由已关的票定死了。

然后看 [要改的东西，一条不落](CHANGE-LIST.md) —— 实施要碰的每一处都在那，
按 🍍 要你拍板 / 🤖 可直接做 / ⏳ 等某张票 分好了。**票关掉时同步更新那份清单的标记。**

## Destination

owner 区从「只能追加、换 bootloader 就丢所有权」变成「**能撤销单张叶证书**、**能原地升级 bootloader 并顺手压缩记录**」。

**这张图产出设计定稿** —— 每处要改的东西有形状、有判据，可以交给实施。**不写代码。**

## Notes

- 域：[M1 固件升级](../../docs/modules/M1-firmware-upgrade.md)、[M2 归属与信任](../../docs/modules/M2-ownership.md)
- **先文档再代码** —— 定稿先进 `M2-ownership.md`，再动 `$BOOT`
- 改 owner 记录格式会波及跨仓镜像 `core:libraries/OpenPLC_IAP/src/owner_root_ro.{c,h}`，由用例 `P2`（跨仓镜像没分叉）守着
- 开票 / 关票 / 算前沿照 [图与票的约定](../MAP-AND-TICKET-CONVENTION.md)
- **实施要碰哪些地方、每条该谁拍板**，在 [要改的东西，一条不落](CHANGE-LIST.md)。它不是待办表 —— `work/TODO.md` 的准入要求每条挂一张已关的票

## 全集

这张图会碰到的所有文件，由这条命令算出来（找的是「谁提到 owner 记录或证书」，不是「我们打算在哪找」）：

```
grep -rln --include=*.c --include=*.h --include=*.go --include=*.py --include=*.md \
  -e owner_slot -e OWNER_SLOT -e OWNER_RECORD -e iap_cert -e IAP_CERT -e certserial \
  /e/WorkSpace/Schaeffer-AG
```

### 2026-09-20 的对账结果

命令输出 **39 个文件**（不含本图自己的 `maps/` 产物）。和 [要改的东西，一条不落](CHANGE-LIST.md) 比对，
**抓出五处漏掉的，已补进那份清单的 `C3`/`C4` 和新增的 `C-附` 一节**：

| 漏的 | 为什么要紧 |
|---|---|
| **core 侧镜像的不只是 `owner_root_ro`** —— 还有 `iap_cert.{c,h}` 和 `iap_auth.{c,h}` | 证书 132 → 128 字节，**三份都要同步**。原先清单只写了一份 |
| **`inject_owner_record.py`** | `T2-04`（无签名高 generation 记录夺不走板子）靠它手工拼记录字节。**格式变了不改它，那条用例造出来的是无效记录、什么都测不到** |
| **`host/bootloader_unit/` 整套** | `T1-16` 拿真实 `owner_slot.c` 在 PC 上跑，桩和用例要跟着改 |
| `check_mirror_sync.py` 的镜像清单 | 不加 `iap_cert`/`iap_auth`，`P2` 看不见它们分叉 |
| `CHALLENGE-AUTH.md` 和 `SECURITY.md` | 两份都在讲证书怎么用 |

## Decisions so far

**以下八条 2026-09-19 在对话里定，开图之前就已成立**，所以没有对应的票：

- **离职换人是真实需求** —— `R2-04`（撤销叶证书）原来标 ⬜「等真实需求」，那个理由到期，重开
- **「更换叶证书」今天就能做，「作废」不能** —— `IAPTool cert` 随时能发新证书且全程不碰板子；老证书永远有效，因为板子从不查任何名单（`iap_cert.c` 只验 `root_sig`，`serial` 读出来不和任何东西比）
- **走路线 2：bootloader 原地升级** —— 读进 SDRAM、在 RAM 里擦扇区 0、写回新镜像 + 旧 owner 记录。类比 BIOS 升级：**不允许断电**
- **否掉路线 3（owner 区独占一个 128 KiB 扇区）** —— 太浪费，现有权限功能已够基本用，不过度设计
- **升级 bootloader 用 owner 根验签**，不用内置根 —— 内置根私钥是公开的，拿它当门等于没有门
- **压缩 = 保留完整有效链的 `'O'` 记录 + 扔掉历史 `'R'` 快照和垃圾**，不折叠成一条。折叠出来的记录必然无签名，而无签名记录谁都能伪造；折叠也只多省两个槽
- **「没有有效 owner 可以授权的操作，一律要物理在场」** —— 一条规则覆盖 `takeown`、恢复出厂、以及**未认领板子上的 `flashboot`**；已认领的板子走 owner 签名，不要 BOOT0
- **掉电不是砖** —— 按住 BOOT0 复位进 ST ROM DFU，一根 USB 线重烧（2026-09-18 实测 11 次，见 [HOW-TO-RUN-TESTS.md](../../docs/engineering/HOW-TO-RUN-TESTS.md) 的 `T1-27` 一节）
- **被新逻辑取代的字段一律删，不留**（用户 2026-09-19：现在是测试阶段，数据随便改）—— 落到三处：证书的 `serial`、`iap_fw_metadata_t.sha256`、`owner_record_t.slots`。删 `slots` 的代价是从此做不了变长记录，而变长的收益在 `'R'` 记录同样是 160 字节时为零

以下两条有自己的票：

- [撤销记录点名的是序号还是公钥](issues/OWN-01-revoke-by-serial-or-by-pubkey.md)：**按叶公钥，取前 16 字节，一条记录装 4 个**。`serial` 整个删掉；`R4` 改成「撤销项 == 当前生效的根 → 忽略该项」；撤销检查**给 `iap_cert_verify()` 加参数**，让编译器保证没有调用点漏掉
- [擦扇区 0 的时候，那段代码从哪执行](issues/OWN-02-where-does-the-erase-code-run.md)：**必须放 `RAM_D1`（`0x24000000`）里跑，全程关中断**。⚠️ RM0433 §4.3.7 的 RWW 只跨 bank 有效，而**擦完扇区 0 之后取到的指令是 `0xFF`，RWW 救不回来**。链接脚本和启动代码**不用改**（`.RamFunc` 段已经有了）
- [升级被打断之后，板子怎么让人知道](issues/OWN-04-how-does-an-interrupted-upgrade-announce-itself.md)：两条 journal 事件（开始 / 完成，住 Bank 2 不被擦）+ 两段定稿文案。**启动日志那行刻意不讲 DFU 怎么用** —— 那条写在发布说明里，两处不重复
- [加了 'R' 记录，format_ver 要不要升到 3](issues/OWN-03-does-format-ver-go-to-3.md)：**升到 3，硬切不做兼容** —— 删了 `slots`、证书变 128 字节，布局整个变了，而现场没有已认领的板子
- [工具怎么确认一次撤销真的进去了](issues/OWN-05-how-does-the-tool-confirm-a-revocation-landed.md)：**信板子回的 `OK`，不加 `getrevoked`** —— `OK` 已经是板子重扫 flash 确认后才发的。顺带核实出 `B4` 是个不存在的问题（累加由板子自动做），且 `D7` 的形状原本写错了
- **2026-09-20 在对话里定，没有对应的票**：`'R'` 记录压到**一个 flash word（32 字节）**，owner 区改成 **`'O'` 32 条 + `'R'` 96 条**两段定长；写入验签、**读取只查结构**。详见 `DECISIONS.md` 第 58 / 59 条，要改的东西在 [要改的东西，一条不落](CHANGE-LIST.md) 的 I 节
- [换根的时候把 owner 区清空重写](issues/OWN-07-should-setowner-wipe-the-owner-area.md)：**按需清空，必须显式请求**。平时换根仍是低风险追加；剩 8 条时日志提示；`--wipe` 那一次才擦扇区 0。**实施排在 `flashboot` 之后**
- [第二次撤销写得进去但不生效](issues/OWN-06-second-revocation-is-written-but-never-takes-effect.md)：**`'R'` 退出链的行走，改成独立一趟扫描**。真板子验收通过（`T2-19`/`T2-20`），槽位 50 → 42、八次作废零浪费

## Not yet specified

- **`flashboot` 的线上协议**：帧格式、分块、和现有 `flash` 命令共用多少
- **撤销之后客户怎么知道「哪几块板上的固件需要重传」** —— 撤掉某人，他签过的固件下次启动会被拒、停在 bootloader。
  ⚠️ **要的不是撤销名单** —— 板子启动时已经在算「当前 app 的签名者被撤了没有」（`IAP_server.c:621`），
  最小做法是把那个布尔值报出来。这条 2026-09-20 由 [工具怎么确认一次撤销真的进去了](issues/OWN-05-how-does-the-tool-confirm-a-revocation-landed.md) 改准
- **发布说明要怎么改** —— 现在写着「换 bootloader 要重传 app + 重新认领」，原地升级做出来之后这句话会过期

## Out of scope

- **五条用户路径的端到端测试方案** —— 2026-09-20 已单独开图：[出厂到五条用户路径的端到端测试方案](../five-paths-e2e-test/map.md)。它测的是板子**今天**的真实行为，不依赖本图的任何产出，**两张图并行**
- **owner 区独占 128 KiB 扇区**（路线 3）—— 用户 2026-09-19 否掉：太浪费，而且现有权限功能已够基本用
