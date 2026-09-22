# 待办

**要做什么已经清楚，只是还没做。** 准入见 [../WHERE-THINGS-LIVE.md](../WHERE-THINGS-LIVE.md)：

> 每一条必须写明它是哪张已关的票产生的。写不出来的，写不进去。

做完且判据过了，**删掉那一行**，不要划掉留着。

| 待办 | 怎么算做完 | 来自哪张票 |
|---|---|---|
| 五个通信口做「异常可恢复」：上位机从帧里看出断了（`conn` 掉 0、`miss` 连增），自己计时到恢复 | 产测文档 3.10 的判定栏能填出「误码 / 恢复时间」，人只要动手拔线、不用回来汇报 | 同上（原 `ISS-D1`）。⚠️ 2026-09-16 起**等工装的使用反馈**再动 |
| 上位机面板左边按九个配置项分类分段 | 九类各自成段；**端口本身仍按板子分组**（Bridge / Upper / Lower / 整板），那条已定不要重开 | 同上（原 `ISS-D2`）。⚠️ 同样等反馈 |
| 每个端口逐个打通到真板子上过 | 每个端口在真板子上跑过一轮并记下结果 | 同上（原 PORT-BRINGUP-PLAN.md 整份，该文件已删） |
| 整轮收尾要还原被 `rotate_keys.sh` 改掉的仓库文件（路径 ③ 会重写 `$BOOT/IAPServer/keys/fw_pubkey.inc` 和 `fw_signing_key.TEST_ONLY.pem`） 。⚠️ **2026-09-21 核实：现在没有任何东西要还原** —— 仓库处在公开根状态（`check_public_root.py` 退出码 0，四仓工作树空）。**这是路径 ③ 跑过之后才成立的收尾步骤，不是现在欠着的账** | 跑 `rotate_keys.sh --restore <本轮快照>`，之后 `check_public_root.py` 退出码 0。⚠️ **还原必须在整轮结束之后，不是路径 ③ 之后** —— 路径 ④ 发叶证书要用那把轮换后的根私钥 | [路径三换根之后 `T2-06` 必然失败，算不算](../maps/five-paths-e2e-test/issues/E2E-05-is-t2-06-failing-after-rotate-expected.md) |
| ⚠️ **换根之后 `enter_bootloader.py` 会对预编译的 `iap_probe_*.bin` 失效**。**2026-09-21 复核：此刻五个镜像内置的都是当前公开根**（逐字节搜 `fw_pubkey.inc` 全部命中），所以现在是好用的 —— 当初记下的 `old-key present = True` 是在**换根窗口期**取的快照。这条描述的是**跑过路径 ③ 之后**的状态，板子未认领时用它们做重启握手会用**编译那一刻烧进去的根**去验证请求方证书，和 bootloader 当前信的根（可能已轮换）对不上，静默不响应。**这不是产品缺陷**——脚本自己的文档已经写着"另一条路是按 BOOT0，需要人在场"；只是说明"软件重启进 bootloader"这条路在换过根之后，对着旧镜像会失效，重新编译镜像或者按 BOOT0 是仅有的两条路 | 需要重编 `onboard/iap_probe/iap_probe.ino` 用当前 `fw_pubkey.inc`，或接受按 BOOT0 | [撤销叶证书 + bootloader 原地升级](../maps/owner-revoke-and-boot-upgrade/map.md) |

| **`flashboot`：bootloader 原地升级** —— ✅ **2026-09-22 代码写完**（`$BOOT/IAPServer/boot_selfupgrade.{c,h}`、`IAP_server.c` 的 `flashboot` 分支、`$TOOL` 的 `RunEtherFlashBoot()`）。链接通过：**104,964 字节，还剩 17,916**；selfcheck 23 项全绿。⚠️ **一行都没上过板** —— `T1-29`–`T1-32` 四条全 ⬜。⚠️ **写回时压缩仍没做** —— owner 区 8 KiB 原样搬。`'R'` 那批已于 2026-09-22 落地，这一半现在不挡了 | 真板子上原地换一次 bootloader，**所有权和已装的 app 都还在**；掉电后按 BOOT0 进 DFU 能救回来 | [`flashboot` 的线上协议长什么样](../maps/owner-revoke-and-boot-upgrade/issues/OWN-12-what-does-the-flashboot-wire-protocol-look-like.md)；设计定稿 [FLASHBOOT.md](../docs/modules/M1/FLASHBOOT.md) |
| ~~**压缩 `'R'` 记录格式**~~ ✅ **2026-09-22 代码写完**（I 节 13 项全部落地）—— owner 区切成 `'O'` 32 条 × 160 字节 + `'R'` 96 条 × 32 字节，`format_ver` 3 → 4 硬切；写入验签、读取只查结构。链接 **105,296 字节，剩 17,584**；selfcheck 24 项全绿，新增主机用例 `T2-22`/`T2-23`。⚠️ **没上过板**，v4 要重烧 bootloader + 重新认领 | 真板子重新认领后，连续作废 96 个叶都生效 | 决策 58 / 59 + `I-D1`–`I-D3` |
| **`IAPTool setowner --wipe`：按需清空 owner 区** | 带 `--wipe` 那一次清空重写，不带的仍然只追加一条；剩 8 条时启动日志出提示 | [换根的时候把 owner 区清空重写](../maps/owner-revoke-and-boot-upgrade/issues/OWN-07-should-setowner-wipe-the-owner-area.md)。⚠️ **实施必然排在 `flashboot` 之后** —— 它要的 `RAM_D1` 擦写例程属于那半边 |
| **`RELEASE-NOTES.md` 改写**（英文）—— ✅ **2026-09-22 已写 `flashboot` 那段**（含「不要断电」、ST-Link 仍会清所有权、升到本版本本身会丢所有权）—— 构图中那句「顺手压缩 owner 区」已删，因为压缩还没做 | 发版说明里的升级规则和板子实际行为一致 | CHANGE-LIST 的 **H 节** |


| ~~**`run_takeown.py` 把 owner 私钥丢在临时目录**~~ ✅ **已修**（commit `c3f43dc`）—— 现在落在 `$TOOL/Output/owner-keys/<时间戳>/`，并在输出里把路径和后果说清楚 | — | 2026-09-20 跑 `T2-09` 时撞上 |

## 优先级最低

| 待办 | 怎么算做完 | 来自哪 |
|---|---|---|
| **研究 MCUboot 可行性** | 能回答「换过去值不值」—— app 空间损失多少，以及证书链 / 撤销 / 认领 / 物理在场这四样 MCUboot 没有的能力怎么补 | 2026-09-21 用户定：**这个版本不考虑 MCUboot**。⚠️ 关键约束：**整机没有外部 flash**（Bridge 板只有一颗 64 MiB SDRAM），第二个 slot 只能挤内部 flash 或放 SDRAM |

## 版本闸门与校准值（2026-09-21 定，形状已定的部分）

**三张已关的票产生的实施项。** 还有三张票开着，未定的部分见
[烧录前比版本 + 校准值住进扇区 15](../maps/version-gate-and-calibration/map.md)。

| 待办 | 怎么算做完 | 来自哪张票 |
|---|---|---|
| ~~**core 侧版本号**~~ ✅ **2026-09-21 done，live 编译验过** —— `openplc_app_version.h`（含 `.openplc_version` section）、`Arduino.h` 挂上、`udp_server.c` 加 include 和 `extern`。⚠️ **只剩 `IAP_config.h` 删 fallback 没做**，它会打断 PlatformIO 那条构建路径，见下 | 不写版本号 ⇒ 编译失败且报错可读 ✅；写了 ⇒ 编过 ✅；越界 300 被 `static_assert` 挡 ✅ | [app 版本号怎么从 sketch 传到 core](../maps/version-gate-and-calibration/issues/VER-01-how-does-the-sketch-version-reach-the-core.md) |
| ~~**构建钩子**~~ ✅ **2026-09-21 done，live 编译验过** —— `prebuild.sh` 宽松粗查；`postbuild.sh` 用 `objcopy -j .openplc_version` 从 ELF 裁出来；`platform.txt` 多传 `{compiler.path}` 和 `{build.project_name}` | `.version` 实测产出 `1.2.3` / `1.0.0`，**就是 ELF 里那段** ✅ | 同上 |
| ~~**identity 加第 5 段**~~ ✅ **2026-09-21 两侧都 done** —— core 报 app 版本，bootloader 报 `-`；`P2` 跨仓镜像检查绿 | 两边格式一致；`BOOTLD` 状态下第 5 段是 `-` 不是版本号 | [identity 怎么同时报卡包版本和 app 版本](../maps/version-gate-and-calibration/issues/VER-04-how-does-identity-carry-both-versions.md) |
| ~~**上位机解析改造**~~ ✅ **2026-09-21 done** —— `boardInfo` 加 `AppVersion`，四段固件降级为空值 | 同上 |
| ~~**上位机比对**~~ ✅ **2026-09-21 done**（新增 `version_gate.go`：读 `.version`、三段数值比较、相等放行、按 role 判、发现不到则拒绝）。⚠️ **只在 ETH 路径真正生效**，见下 | 版本低时拒绝并说明；`CUSAPP` 才比对，`BOOTLD*` 放行 | [版本号的格式和比大小的规则](../maps/version-gate-and-calibration/issues/VER-05-version-format-and-comparison.md)。⚠️ **实施前先看一眼 `cdctransfer` / `ethtransfer` 今天在发现失败时怎么处理** —— 「超时就拒绝」可能改变现有行为 |
| ~~**强制烧录开关**~~ ✅ **2026-09-21 两侧都 done** —— `--force` 布尔标志（不吞下一个参数）、标记文件在 `os.UserConfigDir()/openplc/`、**只在烧成功后才写**、不带 `--force` 的上传会清掉它 | 勾「是」能强制烧一次；**不改回「否」再烧会被拒**；**烧失败不写标记**（重试不受影响）；不带 `--force` 的调用会清掉标记 | [强制烧录这个开关长什么样](../maps/version-gate-and-calibration/issues/VER-06-what-does-the-force-switch-look-like.md) |
| **扇区 15 改造**（`$BOOT`）—— ✅ **2026-09-21 代码已改完**（八种事件日志、`'L'` 记录、防篡改链、`journal_log()` 全删；校准值区 `0x081E0000`+8 KiB；metadata 起点挪到 `0x081E2000`，3840 格 = 548 条；reclaim 先查校准值区是否全 `0xFF`，非空则经 SDRAM 搬运）。语法检查 + selfcheck 23 项全绿。✅ **2026-09-21 晚上板验收通过**：`21/3840`→`28/3840`，一次上传 **7 格**（原 8 格），旧 journal 被正确判为不认识并在首次上传时 reclaim。⚠️ **仍未验**：reclaim 搬运校准值那条分支（校准值区是空的，走不到 `calib_area_is_blank()==false`） | 真板子升级多次后校准值仍在；制造一次 metadata 满，校准值不丢 | [校准值和 metadata 怎么共用扇区 15](../maps/version-gate-and-calibration/issues/VER-02-how-do-calibration-and-metadata-share-the-sector.md) + 决策 61 |
| ~~`check_version_sync.py` 会坏~~ ✅ **2026-09-21 核实：不会。** 它读的是 **`$BOOT/Core/Inc/IAP_config.h`**、`boards.txt`、`RELEASE-NOTES.md` 三处，**不读 core 的 `cores/arduino/stm32/IAP_config.h`** ⇒ 删那个 fallback 对它无影响。**app 版本也不该纳入它** —— 每个 sketch 不同，不是跨仓镜像 | — | 全集对账（2026-09-21） |
| ~~**两个 journal 测试脚本要跟着改**~~ ✅ **2026-09-22 done** —— 两个脚本的档位数和判据字串已改；`$BOOT` 里 `IAP_JOURNAL_*` / `journal_*()` 一并改成 `IAP_META_*` / `meta_*()`，`bootloader_state.h` 的头注释重写。语法检查 + selfcheck 23 项全绿。⚠️ **两个脚本本身要真板子才能跑，还没跑过** | 两个脚本在新布局下都能跑过 | 全集对账（2026-09-21）|

| ~~**`RunGetOwner()` 补两句换主说明**~~ ✅ **2026-09-21 done**（`$TOOL/owner.go`）—— 现在只说「Only firmware signed by that key will start」，读的人以为没路可走 | 输出里说清两条路：`setowner`（要当前主人的密钥）和恢复出厂后 `takeown`（按 BOOT0） | [恢复出厂之后 takeown 被工具拦下，因为线上没法表达「已清空」](../maps/owner-revoke-and-boot-upgrade/issues/OWN-11-getowner-cannot-say-cleared.md) |

| ~~**`iap_probe` 的 v1/v2 两个镜像 app 版本相同**~~ ✅ **2026-09-22 定：不改，两个镜像都留 `1.0.0`** —— 五条路径验的是每条上传通道通不通，不是闸门；而且重新烧回早一个镜像的路径会被闸门拦下。理由写在 `build_probe_image.py` 文件头 | — | 2026-09-21 实施时撞上 |
| ⚠️ **`system/extras/postbuild.sh` 带着 System 文件属性**，任何写入都被拒（`prebuild.sh` 没有）。已在 live 和 repo 两边清掉 | 属性是 `-a----`；下次板卡包重装后如果又出现，要查是哪一步带上的 | 2026-09-21 实施时撞上 |

| ~~**CDC Transfer 这条路的版本闸门不生效**~~ ✅ **2026-09-22 定：接受** —— app 在跑时 `cdcIdentify` 收不到应答（sketch 占着 CDC 数据管道），进 bootloader 后第 5 段已是 `-`；这条路上不存在能读到已装版本的时刻。`DECISIONS.md` 62、`M1`、`RELEASE-NOTES.md` 三处都已写明「只有 ETH 挡得住」 | — | 2026-09-21 实施时撞上 |

## 下次上板一起做

**攒着一次做，不要零散上板**（用户 2026-09-20：「一会上板后统一改和测试」）。
板子只有一块，每次上板都要重烧 / 重新认领，散着做等于把同一份代价付很多遍。

| 待验 | 怎么算做完 | 来自哪 |
|---|---|---|
| **`Flash_If_Write()` 的 I-cache**：上板回归（烧写本身没被这次改动弄坏） | `T1-23` / `T1-24` 在真板子上各跑一轮 | 代码 `886b0ad`。⚠️ **「每条出口都重开 I-cache」那条已由 `P16` 静态证明**，比制造一次失败写入强 —— 上板只剩回归这一半 |
| **`flashboot` 四条** —— `T1-29` 换掉 bootloader、`T1-31` 所有权还在、`T1-30` 叶证书签的被拒、`T1-32` 未认领要按 BOOT0 | 四条全绿。⚠️ **失败会变砖，只能 ST-Link 救** | 代码 2026-09-22，设计 [FLASHBOOT.md](../docs/modules/M1/FLASHBOOT.md) |
| **reclaim 搬运校准值那条分支** —— 要先往校准值区（`0x081E0000`，8 KiB）写点东西，否则 `calib_area_is_blank()` 恒真，走不到 | 制造一次 metadata 区满，校准值不丢 | 决策 61 |
| **两个 metadata 脚本在新布局下跑一遍** —— `run_journal_reclaim.py`（`T1-28`）、`run_journal_slot_accounting.py`（`T1-26`）**改过但没跑过** | 两个都能跑过 | 2026-09-22 |
