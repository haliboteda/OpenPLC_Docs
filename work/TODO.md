# 待办

**要做什么已经清楚，只是还没做。** 准入见 [../WHERE-THINGS-LIVE.md](../WHERE-THINGS-LIVE.md)：

> 每一条必须写明它是哪张已关的票产生的。写不出来的，写不进去。

做完且判据过了，**删掉那一行**，不要划掉留着。

| 待办 | 怎么算做完 | 来自哪张票 |
|---|---|---|
| **TRNG nonce 上板验收** —— 主机侧全绿、两边都编过，**一次都没上过板** | 真板子上：开机日志打 `Backup domain retained`（不再提计数器）；`authchallenge` 连发两次拿到两个不同 nonce；一次完整的 ether 上传通过认证；同一块板重启两次，DHCP 事务号不同；抓两次到板子的 TCP 连接，SYN-ACK 的序列号不同（bootloader 和 app 各验一次） | 决议 66（nonce 改用 TRNG）、决议 67（lwIP 随机数和 TCP 初始序列号也改用 RNG），都是 2026-09-24 |
| **开机日志自相矛盾**：先打 `Ethernet link is DOWN - this board will not answer discovery`，随后 DHCP 拿到 IP、服务可达（`$BOOT/IAPServer/IAP_server.c` 的 `IAP_servers_start()`）。疑为 PHY 自协商未完成就判了，**未核实** | 上板核实原因；之后 link 真断时才打这句，协商中不打 | [出厂态怎么造，怎么证明它真的是出厂态](../maps/five-paths-e2e-test/issues/E2E-01-how-to-make-and-prove-factory-state.md) |
| 五个通信口做「异常可恢复」：上位机从帧里看出断了（`conn` 掉 0、`miss` 连增），自己计时到恢复 | 产测文档 3.10 的判定栏能填出「误码 / 恢复时间」，人只要动手拔线、不用回来汇报 | [问题去哪住](../maps/docs-migration/issues/MIG-09-where-do-defects-and-modules-live.md)（原 `ISS-D1`）。⚠️ 2026-09-16 起**等工装的使用反馈**再动 |
| 上位机面板左边按九个配置项分类分段 | 九类各自成段；**端口本身仍按板子分组**（Bridge / Upper / Lower / 整板），那条已定不要重开 | [问题去哪住](../maps/docs-migration/issues/MIG-09-where-do-defects-and-modules-live.md)（原 `ISS-D2`）。⚠️ 同样等反馈 |
| 每个端口逐个打通到真板子上过 | 每个端口在真板子上跑过一轮并记下结果 | [问题去哪住](../maps/docs-migration/issues/MIG-09-where-do-defects-and-modules-live.md)（原 PORT-BRINGUP-PLAN.md 整份，该文件已删） |
| 整轮收尾要还原被 `rotate_keys.sh` 改掉的仓库文件（路径 ③ 会重写 `$BOOT/IAPServer/keys/fw_pubkey.inc` 和 `fw_signing_key.TEST_ONLY.pem`） 。⚠️ **2026-09-22 跑过一次并还原过：路径 ③ 换了根，整轮结束后 `rotate_keys.sh --restore` + 重编，`check_public_root.py` 回到 0。此刻没有任何东西要还原** —— 仓库处在公开根状态（`check_public_root.py` 退出码 0，四仓工作树空）。**这是路径 ③ 跑过之后才成立的收尾步骤，不是现在欠着的账** | 跑 `rotate_keys.sh --restore <本轮快照>`，之后 `check_public_root.py` 退出码 0。⚠️ **还原必须在整轮结束之后，不是路径 ③ 之后** —— 路径 ④ 发叶证书要用那把轮换后的根私钥 | [路径三换根之后 `T2-06` 必然失败，算不算](../maps/five-paths-e2e-test/issues/E2E-05-is-t2-06-failing-after-rotate-expected.md) |
| ⚠️ **换根之后 `enter_bootloader.py` 会对预编译的 `iap_probe_*.bin` 失效**。⚠️ **2026-09-22 发现还有第二个、更常见的原因**：`iap_probe_v1/v2.bin` 是**老 core 编的**，里面那份 `owner_root_ro.c` 读不懂 v4 的 owner 记录，于是回落到编译进去的公开根、拒绝 owner 签的重启请求 —— 和换不换根无关。两个镜像已用当前 core 重编。**换根这条原因本身仍然成立** —— 当初记下的 `old-key present = True` 是在**换根窗口期**取的快照。这条描述的是**跑过路径 ③ 之后**的状态，板子未认领时用它们做重启握手会用**编译那一刻烧进去的根**去验证请求方证书，和 bootloader 当前信的根（可能已轮换）对不上，静默不响应。**这不是产品缺陷**——脚本自己的文档已经写着"另一条路是按 BOOT0，需要人在场"；只是说明"软件重启进 bootloader"这条路在换过根之后，对着旧镜像会失效，重新编译镜像或者按 BOOT0 是仅有的两条路 | 需要重编 `onboard/iap_probe/iap_probe.ino` 用当前 `fw_pubkey.inc`，或接受按 BOOT0 | [撤销叶证书 + bootloader 原地升级](../maps/owner-revoke-and-boot-upgrade/map.md) |

| ~~**压缩 `'R'` 记录格式**~~ ✅ **2026-09-22 代码写完**（I 节 13 项全部落地）—— owner 区切成 `'O'` 32 条 × 160 字节 + `'R'` 96 条 × 32 字节，`format_ver` 3 → 4 硬切；写入验签、读取只查结构。链接 **105,296 字节，剩 17,584**；selfcheck 24 项全绿，新增主机用例 `T2-22`/`T2-23`。⚠️ **没上过板**，v4 要重烧 bootloader + 重新认领 | 真板子重新认领后，连续作废 96 个叶都生效 | 决策 58 / 59 + `I-D1`–`I-D3` |
| ~~**`IAPTool setowner --wipe`：按需清空 owner 区**~~ ✅ **2026-09-22 代码写完**（CHANGE-LIST 的 J 节 6 项）。主机用例 `T2-24` 全绿；验收单新增 `CHK-B8`。⚠️ **没上板**，`CHK-B8` 会擦扇区 0，做之前要 ST-Link 在手边 | 带 `--wipe` 那一次清空重写，不带的仍然只追加一条 | [换根的时候把 owner 区清空重写](../maps/owner-revoke-and-boot-upgrade/issues/OWN-07-should-setowner-wipe-the-owner-area.md) |


| ~~**`run_takeown.py` 把 owner 私钥丢在临时目录**~~ ✅ **已修**（commit `c3f43dc`）—— 现在落在 `$TOOL/Output/owner-keys/<时间戳>/`，并在输出里把路径和后果说清楚 | — | 2026-09-20 跑 `T2-09` 时撞上 |

## 优先级最低

| 待办 | 怎么算做完 | 来自哪 |
|---|---|---|
| **研究 MCUboot 可行性** | 能回答「换过去值不值」—— app 空间损失多少，以及证书链 / 撤销 / 认领 / 物理在场这四样 MCUboot 没有的能力怎么补 | 2026-09-21 用户定：**这个版本不考虑 MCUboot**。⚠️ 关键约束：**整机没有外部 flash**（Bridge 板只有一颗 64 MiB SDRAM），第二个 slot 只能挤内部 flash 或放 SDRAM |

## 版本闸门与校准值（2026-09-21 定，形状已定的部分）

**[烧录前比版本 + 校准值住进扇区 15](../maps/version-gate-and-calibration/map.md) 那张图产生的实施项。** 图上七张票已全部关闭。

| 待办 | 怎么算做完 | 来自哪张票 |
|---|---|---|
| ~~**core 侧版本号**~~ ✅ **2026-09-21 done，live 编译验过** —— `openplc_app_version.h`（含 `.openplc_version` section）、`Arduino.h` 挂上、`udp_server.c` 加 include 和 `extern`。`IAP_config.h` 的 fallback 也已删除（PlatformIO 构建路径不支持，缺了就编译报错，理由在该文件注释里） | 不写版本号 ⇒ 编译失败且报错可读 ✅；写了 ⇒ 编过 ✅；越界 300 被 `static_assert` 挡 ✅ | [app 版本号怎么从 sketch 传到 core](../maps/version-gate-and-calibration/issues/VER-01-how-does-the-sketch-version-reach-the-core.md) |
| ~~**构建钩子**~~ ✅ **2026-09-21 done，live 编译验过** —— `prebuild.sh` 宽松粗查；`postbuild.sh` 用 `objcopy -j .openplc_version` 从 ELF 裁出来；`platform.txt` 多传 `{compiler.path}` 和 `{build.project_name}` | `.version` 实测产出 `1.2.3` / `1.0.0`，**就是 ELF 里那段** ✅ | 同上 |
| ~~**identity 加第 5 段**~~ ✅ **2026-09-21 两侧都 done** —— core 报 app 版本，bootloader 报 `-`；`P2` 跨仓镜像检查绿 | 两边格式一致；`BOOTLD` 状态下第 5 段是 `-` 不是版本号 | [identity 怎么同时报卡包版本和 app 版本](../maps/version-gate-and-calibration/issues/VER-04-how-does-identity-carry-both-versions.md) |
| ~~**上位机解析改造**~~ ✅ **2026-09-21 done** —— `boardInfo` 加 `AppVersion`，四段固件降级为空值 | 同上 |
| ~~**上位机比对**~~ ✅ **2026-09-21 done**（新增 `version_gate.go`：读 `.version`、三段数值比较、相等放行、按 role 判、发现不到则拒绝）。⚠️ **只在 ETH 路径真正生效**，见下 | 版本低时拒绝并说明；`CUSAPP` 才比对，`BOOTLD*` 放行 | [版本号的格式和比大小的规则](../maps/version-gate-and-calibration/issues/VER-05-version-format-and-comparison.md)。⚠️ **实施前先看一眼 `cdctransfer` / `ethtransfer` 今天在发现失败时怎么处理** —— 「超时就拒绝」可能改变现有行为 |
| ~~**强制烧录开关**~~ ✅ **2026-09-21 两侧都 done** —— `--force` 布尔标志（不吞下一个参数）、标记文件在 `os.UserConfigDir()/openplc/`、**只在烧成功后才写**、不带 `--force` 的上传会清掉它 | 勾「是」能强制烧一次；**不改回「否」再烧会被拒**；**烧失败不写标记**（重试不受影响）；不带 `--force` 的调用会清掉标记 | [强制烧录这个开关长什么样](../maps/version-gate-and-calibration/issues/VER-06-what-does-the-force-switch-look-like.md) |
| **扇区 15 改造**（`$BOOT`）—— ✅ **2026-09-21 代码已改完**（八种事件日志、`'L'` 记录、防篡改链、`journal_log()` 全删；校准值区 `0x081E0000`+8 KiB；metadata 起点挪到 `0x081E2000`，3840 格 = 548 条；reclaim 先查校准值区是否全 `0xFF`，非空则经 SDRAM 搬运）。语法检查 + selfcheck 23 项全绿。✅ **2026-09-21 晚上板验收通过**：`21/3840`→`28/3840`，一次上传 **7 格**（原 8 格），旧 journal 被正确判为不认识并在首次上传时 reclaim。✅ **2026-09-22 补验**：往校准值区写入可辨认字节后灌满 metadata，reclaim 擦完扇区，那段字节逐字节还在。⚠️ 以前验不了是**测试脚本**先擦掉了校准值（`-w` 写扇区任一部分都会整扇区擦），不是固件的问题 | 真板子升级多次后校准值仍在；制造一次 metadata 满，校准值不丢 | [校准值和 metadata 怎么共用扇区 15](../maps/version-gate-and-calibration/issues/VER-02-how-do-calibration-and-metadata-share-the-sector.md) + 决策 61 |
| ~~`check_version_sync.py` 会坏~~ ✅ **2026-09-21 核实：不会。** 它读的是 **`$BOOT/Core/Inc/IAP_config.h`**、`boards.txt`、`RELEASE-NOTES.md` 三处，**不读 core 的 `cores/arduino/stm32/IAP_config.h`** ⇒ 删那个 fallback 对它无影响。**app 版本也不该纳入它** —— 每个 sketch 不同，不是跨仓镜像 | — | 全集对账（2026-09-21） |
| ~~**两个 journal 测试脚本要跟着改**~~ ✅ **2026-09-22 done** —— 两个脚本的档位数和判据字串已改；`$BOOT` 里 `IAP_JOURNAL_*` / `journal_*()` 一并改成 `IAP_META_*` / `meta_*()`，`bootloader_state.h` 的头注释重写。语法检查 + selfcheck 23 项全绿。⚠️ **两个脚本本身要真板子才能跑，还没跑过** | 两个脚本在新布局下都能跑过 | 全集对账（2026-09-21）|

| ~~**`RunGetOwner()` 补两句换主说明**~~ ✅ **2026-09-21 done**（`$TOOL/owner.go`）—— 现在只说「Only firmware signed by that key will start」，读的人以为没路可走 | 输出里说清两条路：`setowner`（要当前主人的密钥）和恢复出厂后 `takeown`（按 BOOT0） | [恢复出厂之后 takeown 被工具拦下，因为线上没法表达「已清空」](../maps/owner-revoke-and-boot-upgrade/issues/OWN-11-getowner-cannot-say-cleared.md) |

| ~~**`iap_probe` 的 v1/v2 两个镜像 app 版本相同**~~ ✅ **2026-09-22 定：不改，两个镜像都留 `1.0.0`** —— 五条路径验的是每条上传通道通不通，不是闸门；而且重新烧回早一个镜像的路径会被闸门拦下。理由写在 `build_probe_image.py` 文件头 | — | 2026-09-21 实施时撞上 |
| ⚠️ **`system/extras/postbuild.sh` 带着 System 文件属性**，任何写入都被拒（`prebuild.sh` 没有）。已在 live 和 repo 两边清掉 | 属性是 `-a----`；下次板卡包重装后如果又出现，要查是哪一步带上的 | 2026-09-21 实施时撞上 |

| ~~**CDC Transfer 这条路的版本闸门不生效**~~ ✅ **2026-09-22 定：接受** —— app 在跑时 `cdcIdentify` 收不到应答（sketch 占着 CDC 数据管道），进 bootloader 后第 5 段已是 `-`；这条路上不存在能读到已装版本的时刻。`DECISIONS.md` 62、`M1`、`RELEASE-NOTES.md` 三处都已写明「只有 ETH 挡得住」 | — | 2026-09-21 实施时撞上 |

## 上板那批：2026-09-22 全部跑完

**一轮跑完，没有留尾巴。** 判据和证据在
[M1 固件升级](../docs/modules/M1-firmware-upgrade.md) 和
[M2 归属与信任](../docs/modules/M2-ownership.md) 的用例表里，这里只记结论。

| 验了什么 | 结果 |
|---|---|
| **`flashboot` 四条**（`T1-29` `T1-30` `T1-31` `T1-32`） | ✅ 当天换了五次 bootloader，五次都成功，所有权和 app 每次都在 |
| **v4 owner 区**（`T2-01` 认领、`T2-15`–`T2-20` 作废整批） | ✅ 一次作废花一个 32 字节 word，重复作废不花槽位，`'O'` 段全程不动 |
| **`setowner --wipe`**（`CHK-B8` / `T2-25`） | ✅ 6 个作废名额全部回收成 `96/96` |
| **`T1-23` / `T1-24`** 烧写回归 | ✅ 坏 CRC 回 `Checksum Failed`，不是 `Signature Failed` |
| **`T1-26` / `T1-28`** 两个 metadata 脚本 | ✅ 一次上传 7 格；灌满 3840 触发 reclaim |
| **reclaim 搬运校准值** | ✅ **第一次真的跑到** —— 以前跑不出来是测试脚本先把校准值擦了，不是固件的问题 |

⚠️ **这一轮从板子上挖出两个缺陷，都已修：**

1. **`IAPTool` 把「板子拒绝了镜像」报成成功。** 镜像签名是整包传完才验的，而工具传完就
   不再读应答。`ether` 和 `flashboot` 两条路都有。修法见 `$TOOL` 的 `IAP_Ether.go` ——
   现在读裁决，并以「板子重新上线」作为成功的正面证据。
2. **四个驱动脚本从来没真跑过**，各自带着必然失败的缺陷（详见 commit `07d993e`）。

