# 烧录前比版本 + 校准值住进扇区 15

## 怎么看进度（不用问任何人）

```
python tools/list_wayfinder_map_frontier.py --all
```

> 打出每张票是 `TAKEABLE` / `claimed` / `resolved` / `paused`，以及谁挡着谁。**别凭记忆，跑它。**

## 还要你拍几次板（**提前列出来，免得被逐个突袭**）

| 还剩几次 | 要你定什么 | 哪张票 |
|---|---|---|
| 1 | 发布和现场迁移怎么走 | [这次变更怎么发布，现场的板子怎么迁移](issues/VER-07-how-does-this-ship-and-migrate.md) |

## Destination

**两件事，共用一个扇区和一次设计**：

1. **sketch 必须带自己的版本号**，烧录时上位机比对板子上跑的那一版，低了拒绝、可强制覆盖
2. **校准值和 firmware metadata 共用扇区 15**，journal 的事件日志去掉

**这张图产出设计定稿** —— 每处要改的东西有形状、有判据，可以交给实施。**不写代码。**

## Notes

- 域：[M1 固件升级](../../docs/modules/M1-firmware-upgrade.md)、[M2 归属与信任](../../docs/modules/M2-ownership.md)
- **先文档再代码**
- 这次变更**同时动三个仓**：`$CORE_REPO`（版本宏、`Arduino.h`、`prebuild.sh`、`postbuild.sh`、`boards.txt`）、
  `$TOOL`（比对逻辑、`.version` 读取）、`$BOOT`（扇区 15 布局、删事件日志）
- ⚠️ **本图的三张已关票是 2026-09-21 用户在对话里逐条拍的板**，不是 AI 自答。
  一次记三张是补记，不是违反「一个会话只关一张票」
- 开票 / 关票 / 算前沿照 [图与票的约定](../MAP-AND-TICKET-CONVENTION.md)

## 全集

这张图会碰到的所有文件，由这条命令算出来（找的是「谁碰版本号、谁碰扇区 15、谁碰 identity、谁碰构建钩子」）：

```
grep -rln --include=*.c --include=*.h --include=*.cpp --include=*.go --include=*.py \
          --include=*.md --include=*.txt --include=*.sh --include=*.ino \
  -e OPENPLC_FW_VERSION -e openplc_app_version -e fw_version -e build_opt -e build.opt \
  -e IAP_STATE_SECTOR_ADDR -e IAP_JOURNAL -e journal -e iap_identity_string \
  -e parseBoardInfoFromReply -e prebuild -e postbuild -e 0x081E0000 \
  /e/WorkSpace/Schaeffer-AG
```

### 2026-09-21 对账（关最后一张票时做的）

去掉 `.metadata/`、`Middlewares/`、`Drivers/`、三个不属于本产品的目录和本图自己的产物之后，
命令输出 **53 个文件**。**抓出四处开图时没想到的**：

| 漏的 | 为什么要紧 |
|---|---|
| ~~**`check_version_sync.py`**~~ | ⚠️ **当时判断错了，2026-09-21 核实后撤回**：它读的是 `$BOOT/Core/Inc/IAP_config.h` 而非 core 的同名文件，**删 core 的 fallback 对它无影响** |
| **`run_journal_reclaim.py` / `run_journal_slot_accounting.py`** | 一个测 `R1-29`（依赖 `** Journal full ...` 的日志文案），一个数槽位（4096 → 3840） |
| ~~**`bootloader_unit/stubs/bootloader_state_stub.c`**~~ | ⚠️ **判断错了，2026-09-21 实施后撤回**：桩只实现 `crypto_selftest_passed()` 一个函数，不依赖日志 API。改完 `T1-16` 仍 PASS |
| **`docs/modules/M1/SECTOR-15.md`** | 整份在讲 journal，事件日志删掉后大半不存在了 |

⚠️ 误命中（与本图无关，不改）：`libraries/OpenPLC_KNX/*`、`libraries/EEPROM/*`、
`stm32yyxx_hal_conf.h`、VTOR 那两个探针、owner 相关的四个脚本和桩。

两条成立、两条撤回，都已进 `work/TODO.md`。

⚠️ **这次对账暴露了一个方法问题**：`check_version_sync.py` 和 `bootloader_state_stub.c` 两条都是
**只看 grep 命中就断言「它会坏」**，打开看才发现不依赖。
**全集命令回答的是「谁提到了这件事」，不是「谁依赖它」** —— 前者是对账的入口，后者要逐个打开看。

## Decisions so far

- [app 版本号怎么从 sketch 传到 core](issues/VER-01-how-does-the-sketch-version-reach-the-core.md)：**A+B**
  —— sketch 里一行 `OPENPLC_APP_VERSION(1, 0, 0);`，core 只声明不定义，
  漏写时 `prebuild.sh` 报错、链接器兜底；`.version` 从 ELF 提取
- [校准值和 metadata 怎么共用扇区 15](issues/VER-02-how-do-calibration-and-metadata-share-the-sector.md)：
  **前 8 KiB 校准值（固定地址），后 120 KiB metadata（append，548 条）**。
  满了只搬那 8 KiB，旧 metadata 直接丢；工装按 UID 留副本兜住唯一那个掉电窗口
- [ST-Link 直连的版本回退防不防](issues/VER-03-do-we-block-swd-downgrade.md)：**不防，写进说明**
  —— 唯一手段 RDP Level 2 不可逆，会同时废掉「BOOT0 恢复出厂」和「ST-Link 救砖」
- [identity 怎么同时报卡包版本和 app 版本](issues/VER-04-how-does-identity-carry-both-versions.md)：
  **加第 5 段**，卡包版本留在第 4 段。bootloader 那一份第 5 段填 `-`；
  新工具按段数降级（收到 4 段 = 旧固件 = 放行）
- [版本号的格式和比大小的规则](issues/VER-05-version-format-and-comparison.md)：
  **三段 0–255，逐段数值比，相等放行，不支持预发布后缀**；`CUSAPP` 才比对，两种 `BOOTLD` 放行；
  **发现超时则拒绝**（未知不等于没有）；比对必须在请板子进 bootloader 之前
- [强制烧录这个开关长什么样](issues/VER-06-what-does-the-force-switch-look-like.md)：**T** ——
  菜单和端口平级（默认「否」），IAPTool 用 `--force`；**一次性靠 IAPTool 自己的标记文件**，
  「把菜单拨回否」就是重置。**标记只在烧成功后才写**，所以失败重试不受影响

## 从这张图继承的结论

[metadata 从 journal 扇区搬进 app 头部](../app-header-replaces-journal/map.md) 2026-09-21 归档，
下面这些是**和 header 无关、因此仍然成立**的部分，搬过来免得随那张图一起被忽略：

- **metadata 砍不得** —— 它支撑 `R1-26`（每次启动重校验签名）、`R1-27`（掉电中断后可恢复）、
  `R1-28`（metadata 记在 journal 里）、以及跨模块的 `R2-04`（撤销叶证书）。
  最后那条写在 M2、实现却整个寄生在 `cert` 字段上，**最容易漏**
- **「掉电恢复」不是 metadata 的独立功能** —— 它是启动校验在「app 被写坏」这个输入下的表现，不占额外字节
- **事件日志支撑 0 条需求、零读出路径** —— 四个导出函数在 `bootloader_state.c` 之外零调用者，
  上位机 grep `journal` 零命中。⚠️ **这是「删日志」的依据**，见
  [八种事件日志留不留，留的话住哪](../app-header-replaces-journal/issues/HDR-02-do-the-event-logs-survive.md)
- **只缓存叶公钥（不存整张 cert）是不安全的** —— 缓存的公钥没有任何东西约束它是否被认可
- **`app_size` 必须记** —— 不记就必须每次全擦 app 区，还要每次启动算满 1792 KiB 的哈希
- **尾附「哈希」不安全，尾附「签名 + 证书」安全** —— 差别在**锚**：`cert.root_sig` 锚在 owner 区，改镜像的人够不着

⚠️ **有一条反过来了**：那张图记着「metadata 跟 app 一起写之后，append-only 的理由消失，
journal 就没必要了」。**本图不搬 metadata，所以 append 仍然需要** —— 删掉的只是事件日志。

## Not yet specified

- **校准值区那 8 KiB 内部怎么组织** —— magic / 长度 / CRC 要不要，放几条，怎么判「这里还没写过」
- **metadata 记录本身要不要瘦身** —— 事件日志删掉之后，记录头里的 `type` / `slots` 还有没有用
- **上位机比对不通过时给用户看什么** —— 文案、在 IDE 输出窗口怎么显示、怎么引导到强制选项
- **工装按 UID 存校准值副本的形态** —— 存哪、什么格式、谁来读。这条可能整个属于产测那条线，不在本图

## Out of scope

- **板子侧的单调计数器 / 真正的防回滚** —— 2026-09-21 论证过：它挡不住有物理接触的人，
  也挡不住拿到叶私钥还能自己造固件的人，而**撤销机制覆盖得更彻底**。
  本图做的是**上位机侧的防呆**，不是安全机制。见 [防回滚](../anti-rollback/map.md)
- **MCUboot** —— 2026-09-21 用户定「这个版本不考虑」，待办见 `work/TODO.md`
- **app header 的布局** —— 本图不搬 metadata，它留在扇区 15
