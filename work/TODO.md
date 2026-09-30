# 待办

**要做什么已经清楚，只是还没做。** 准入见 [../WHERE-THINGS-LIVE.md](../WHERE-THINGS-LIVE.md)：

> 每一条必须写明它是哪张已关的票产生的。写不出来的，写不进去。

做完且判据过了，**删掉那一行**，不要划掉留着。

| 待办 | 怎么算做完 | 来自哪张票 |
|---|---|---|
| **TRNG 上板验收：剩要抓包的两项** —— 2026-09-28 第二块板上已过四项：开机打 `Backup domain retained`、6 个 nonce 互不相同、ether 上传通过认证、认证不过打 `Auth rejected (attempt 1 this boot, peer …)` | 同一块板重启两次，DHCP 事务号不同；抓两次到板子的 TCP 连接，SYN-ACK 的序列号不同（bootloader 和 app 各验一次）。⚠️ 本机有 Npcap、没有 Wireshark / scapy，会话不是管理员 | 决议 66（nonce 改用 TRNG）、决议 67（lwIP 随机数和 TCP 初始序列号也改用 RNG）、决议 69（认证失败只留日志），都是 2026-09-24 |
| **所有权回归：v4 格式和 TRNG 之后重跑 12 条** —— `T2-02` `T2-03` `T2-04` `T2-05` `T2-07` `T2-08` `T2-09` `T2-10` `T2-11` `T2-12`–`T2-14` 最后一次上板早于 2026-09-22 的 v4 硬切，今天的固件一次没上过板。**和上一行同一轮做，只按两次 BOOT0**：① `flashboot` 换上当前 bootloader（所有权保留），顺带做上一行；② 不用 BOOT0：`T2-04` → `T2-11` → `T2-03` + `T2-12`–`T2-14`；③ BOOT0 十秒恢复出厂（`T2-05` 前半）→ `T2-08` → `T2-02` → 传一个公开根签的 app → 按 BOOT0 认领（`T2-05` 后半 + `T2-09`）；④ 最后换编进去的根：`T2-07` → `T2-10`，跑完 `rotate_keys.sh --restore` | 12 条都在当前固件上达到 [M2 归属与信任](../docs/modules/M2-ownership.md) 第 4 节的判据。⚠️ **[决策 72](../docs/tables/DECISIONS.md)（2026-09-30）之后，其中依赖按 BOOT0 认领、公开根、`rotate_keys.sh` 的用例（③④ 两步）都会被改写**；这一轮是先跑还是等决策 72 实施后按新判据跑，等用户定 | 决策 58（owner 区 v4 硬切）、决议 66 / 67（TRNG） |
| **开机日志自相矛盾**：先打 `Ethernet link is DOWN - this board will not answer discovery`，随后 DHCP 拿到 IP、服务可达（`$BOOT/IAPServer/IAP_server.c` 的 `IAP_servers_start()`）。疑为 PHY 自协商未完成就判了，**未核实** | 上板核实原因；之后 link 真断时才打这句，协商中不打 | [出厂态怎么造，怎么证明它真的是出厂态](../maps/five-paths-e2e-test/issues/E2E-01-how-to-make-and-prove-factory-state.md) |
| **端口例程逐个上板验：剩 5 个半** —— 2026-09-28 第二块板上已过 7 个：DO、继电器、系统 LED、板载温度、RS232、USB 串口、以太网；AO 只过了 AO1（470 Ω 上 9.32 V = 19.83 mA，0 码残余约 0.17 mA）。剩 AO2、DI、AI、RS485、CAN、SD；另把 `T1-34`（IDE 那条上传命令）对着真板子走一遍 | 每个例程上传后，串口监视器里的输出和端子上看到的与它文件头写的一致；IDE 的 Tools → Port 里选中真板子能 Upload，未认领和已认领各一次。⚠️ CAN 要第二个节点，SD 要一张卡，AI 要先焊跳线 | [一个例程长什么样](../maps/arduino-examples-and-ide-flow/issues/IDE-05-what-does-one-example-look-like.md) |
| **`HARDWARE-FACTS.md` 的 PG11 那一格等用户定**：记的是「心跳指示」，原理图上心跳灯是 LED3 / PE2，PG11（`KNX_Prog_LED`）这根线上没有 LED | 用户认可后改那一格，并同步变体头 `variant_PLC_H743.h:233-234` | [KNX 和 SDRAM 例程写死的引脚和本板对得上吗](../maps/core-examples-on-board/issues/EXB-07-do-knx-and-sdram-examples-use-this-boards-pins.md)，证据见 [EXB-07-findings.md](../maps/core-examples-on-board/EXB-07-findings.md) 表 3 |
| **上游例程删除清单等用户逐个确认**：建议删 19 个。`EEPROM` 8 个已随整库删掉（2026-09-30，本板不提供模拟 EEPROM，见 EXB-09），剩 11 个：`Servo` 3、`SoftwareSerial` 2、`SPI` 2、`Keyboard`、`Mouse`、`SubGhz`、`RGB_LED_TLC59731`） | 用户逐个点头后删；P5 `EXCLUDED` 去掉死条目；P5 重跑全绿 | [上游例程哪些和本板有关](../maps/core-examples-on-board/issues/EXB-04-which-upstream-examples-relate-to-this-board.md) |
| **面板连 sim 失败时的提示说错了对象**：模拟板进程退出时仍提示「检查 PORTTOOL_ENABLE、波特率、接线」（`$TOOL/internal/ptpanel/panel.go:439`），应说模拟板退出了及退出码 | sim 进程起不来时，面板提示里出现「模拟板」和它的退出码 | 2026-09-29 模拟板加载到 32 位 DLL 那次，见 [HOW-TO-RUN-TESTS.md](../docs/engineering/HOW-TO-RUN-TESTS.md)「模拟板」 |
| 五个通信口做「异常可恢复」：上位机从帧里看出断了（`conn` 掉 0、`miss` 连增），自己计时到恢复 | 产测文档 3.10 的判定栏能填出「误码 / 恢复时间」，人只要动手拔线、不用回来汇报 | [问题去哪住](../maps/docs-migration/issues/MIG-09-where-do-defects-and-modules-live.md)（原 `ISS-D1`）。⚠️ 2026-09-16 起**等工装的使用反馈**再动 |
| 上位机面板左边按九个配置项分类分段 | 九类各自成段；**端口本身仍按板子分组**（Bridge / Upper / Lower / 整板），那条已定不要重开 | [问题去哪住](../maps/docs-migration/issues/MIG-09-where-do-defects-and-modules-live.md)（原 `ISS-D2`）。⚠️ 同样等反馈 |
| 每个端口逐个打通到真板子上过 | 每个端口在真板子上跑过一轮并记下结果 | [问题去哪住](../maps/docs-migration/issues/MIG-09-where-do-defects-and-modules-live.md)（原 PORT-BRINGUP-PLAN.md 整份，该文件已删） |
| 整轮收尾要还原被 `rotate_keys.sh` 改掉的仓库文件（路径 ③ 会重写 `$BOOT/IAPServer/keys/fw_pubkey.inc` 和 `fw_signing_key.TEST_ONLY.pem`） 。⚠️ **2026-09-22 跑过一次并还原过：路径 ③ 换了根，整轮结束后 `rotate_keys.sh --restore` + 重编，`check_public_root.py` 回到 0。此刻没有任何东西要还原** —— 仓库处在公开根状态（`check_public_root.py` 退出码 0，四仓工作树空）。**这是路径 ③ 跑过之后才成立的收尾步骤，不是现在欠着的账** | 跑 `rotate_keys.sh --restore <本轮快照>`，之后 `check_public_root.py` 退出码 0。⚠️ **还原必须在整轮结束之后，不是路径 ③ 之后** —— 路径 ④ 发叶证书要用那把轮换后的根私钥 | [路径三换根之后 `T2-06` 必然失败，算不算](../maps/five-paths-e2e-test/issues/E2E-05-is-t2-06-failing-after-rotate-expected.md) |
| ⚠️ **换根之后 `enter_bootloader.py` 会对预编译的 `iap_probe_*.bin` 失效**。⚠️ **2026-09-22 发现还有第二个、更常见的原因**：`iap_probe_v1/v2.bin` 是**老 core 编的**，里面那份 `owner_root_ro.c` 读不懂 v4 的 owner 记录，于是回落到编译进去的公开根、拒绝 owner 签的重启请求 —— 和换不换根无关。两个镜像已用当前 core 重编。**换根这条原因本身仍然成立** —— 当初记下的 `old-key present = True` 是在**换根窗口期**取的快照。这条描述的是**跑过路径 ③ 之后**的状态，板子未认领时用它们做重启握手会用**编译那一刻烧进去的根**去验证请求方证书，和 bootloader 当前信的根（可能已轮换）对不上，静默不响应。**这不是产品缺陷**——脚本自己的文档已经写着"另一条路是按 BOOT0，需要人在场"；只是说明"软件重启进 bootloader"这条路在换过根之后，对着旧镜像会失效，重新编译镜像或者按 BOOT0 是仅有的两条路 | 需要重编 `onboard/iap_probe/iap_probe.ino` 用当前 `fw_pubkey.inc`，或接受按 BOOT0 | [撤销叶证书 + bootloader 原地升级](../maps/owner-revoke-and-boot-upgrade/map.md) |

| ~~**压缩 `'R'` 记录格式**~~ ✅ **2026-09-22 代码写完**（I 节 13 项全部落地）—— owner 区切成 `'O'` 32 条 × 160 字节 + `'R'` 96 条 × 32 字节，`format_ver` 3 → 4 硬切；写入验签、读取只查结构。链接 **105,296 字节，剩 17,584**；selfcheck 24 项全绿，新增主机用例 `T2-22`/`T2-23`。⚠️ **没上过板**，v4 要重烧 bootloader + 重新认领 | 真板子重新认领后，连续作废 96 个叶都生效 | 决策 58 / 59 + `I-D1`–`I-D3` |
| ~~**`IAPTool setowner --wipe`：按需清空 owner 区**~~ ✅ **2026-09-22 代码写完**（CHANGE-LIST 的 J 节 6 项）。主机用例 `T2-24` 全绿；验收单新增 `CHK-B8`。⚠️ **没上板**，`CHK-B8` 会擦扇区 0，做之前要 ST-Link 在手边 | 带 `--wipe` 那一次清空重写，不带的仍然只追加一条 | [换根的时候把 owner 区清空重写](../maps/owner-revoke-and-boot-upgrade/issues/OWN-07-should-setowner-wipe-the-owner-area.md) |


| ~~**`run_takeown.py` 把 owner 私钥丢在临时目录**~~ ✅ **已修**（commit `c3f43dc`）—— 现在落在 `$TOOL/Output/owner-keys/<时间戳>/`，并在输出里把路径和后果说清楚 | — | 2026-09-20 跑 `T2-09` 时撞上 |

## 出厂无根、第一次上传自动认领（2026-09-30 定）

**[决策 72](../docs/tables/DECISIONS.md) 的实施项**，来自 [第一次把用户的根写进板子，要不要按住 BOOT0](../maps/root-key-without-bootloader-reflash/issues/ROOT-02-must-the-first-write-of-the-users-root-need-boot0.md) 和同图的方案 5（根区并进扇区 15）。**按阶段做，前一阶段完再进下一阶段；先文档再代码。**

| 待办 | 怎么算做完 | 来自哪张票 |
|---|---|---|
| **0.1 前置：KNX / EEPROM 不再擦扇区 15** —— 用户 2026-09-30 定：删 `EEPROM` 库和 8 个例程；KNX 两块数据并进扇区 14，保存时一起读擦写；用 KNX 的程序编译时限 1664 KiB；selfcheck 扫 core 里写扇区 15 的代码 | 见 [KNX 和 EEPROM 往 flash 存数据时不能擦扇区 15](../maps/core-examples-on-board/issues/EXB-09-knx-and-eeprom-must-not-erase-sector-15.md) 的判据 | EXB-09（未关，这一行等它关） |
| **0.2 前置：核实备份 SRAM 只靠 VBAT 时保持内容、扇区擦除时间** | 出处写进 `maps/root-key-without-bootloader-reflash/ROOT-05-findings.md`（RM0433 / DS12110 章节号）；备份 SRAM 另在真板上断主电后读回 | 决策 72 · 方案 5 |
| **1 文档**：M2（信任根的一生、四条规则、出厂默认根、告警、住在哪、keys 目录）、`M1/SECTOR-15.md`（新布局、三种回收、六步、开机判断、掉电后果）、`M1/FLASHBOOT.md`、`M1/IAP-PROTOCOL.md`（`takeown` 无门禁、`getpubkey` 无根时的回答）、`repo/ARCHITECTURE.md`（备份 SRAM 登记、镜像表）、`$BOOT/IAPServer/keys/README.md` 和发布说明 | 文档里不再有「公开根」「按 BOOT0 认领」「`rotate_keys.sh`」当现状讲；P8 / P9 绿 | 决策 72 |
| **2 bootloader**：删 `fw_pubkey.*` / `keys/`；owner 区搬到 `0x081E2000`；无根时只收 `takeown`；`takeown` 去 BOOT0 门禁；扇区 15 新布局 + 完整标记；三种回收；备份 SRAM 暂存与恢复；`flashboot` 不再保 S0 尾部；链接脚本可回 128K | 主机用例全绿；编过 | 决策 72 |
| **3 IAPTool**：上传前发现无根 → 默认位置取或生成私钥并打印路径 → `takeown` → 上传；owner 类命令补 CDC 通道；删公开私钥回落；上传被拒时提示拷私钥或要叶证书；`genkey` / `compile_tool.sh` 去掉公开根 | 假板子上 USB、网口两条首次认领都通 | 决策 72 |
| **4 core**：删 `OpenPLC_IAP/src/fw_pubkey.*`；`owner_root_ro.*` 读新地址、链空时拒绝；板卡包不带公开私钥 | P2 绿；live 编过 | 决策 72 |
| **5 测试**：改 `host/owner_revoke` `owner_capacity` `bootloader_unit` `fakeboard` `renode` `crypto_ref`；删改 `check_public_root.py` `run_old_root_image_is_refused.py` `run_five_paths.py` `signature_wrongkey.go` `reset_board_to_factory_state.py` `inject_owner_record.py`；`check_mirror_sync.py` 换常量；新增：USB / 网口自动认领、恢复出厂回到无根、`setowner` 超过 32 次触发回收、回收中途断电从暂存恢复 | selfcheck 全绿 | 决策 72 |
| **6 上板与发布**：实验室那块板 ST-Link 烧新 bootloader、擦扇区 15 写回校准值、走一遍自动认领；跑第 5 阶段全部用例含真断电；升版本、发板卡包 | 真板上全过 | 决策 72 |

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

## 每块板校准 AI/AO（2026-09-28 定）

**[每块板校准那张图](../maps/per-board-calibration/map.md) 产生的实施项。**

| 待办 | 怎么算做完 | 来自哪张票 |
|---|---|---|
| **工装：5 点测量 → 拟合 → 按 UID 存档 → 生成扇区 15 的镜像** | 四路各 5 点，残差进报告；同一 UID 重测覆盖前留旧档 | [校准哪些通道](../maps/per-board-calibration/issues/CAL-03-which-channels-and-what-correction-model.md)、[修正值怎么写进板子](../maps/per-board-calibration/issues/CAL-04-how-do-values-get-onto-the-board-and-survive-the-reflash.md) |
| **工站 10：JLINK 只擦扇区 0–14 重烧，再写扇区 15** | 真板子上走完后扇区 15 逐字节等于存档；bootloader 和 app 正常启动 | [修正值怎么写进板子](../maps/per-board-calibration/issues/CAL-04-how-do-values-get-onto-the-board-and-survive-the-reflash.md) |
| **方案文件加精度字段**：AI ±0.1 % FS、AO ±0.3 % FS（25 °C，校准后残差） | 换一份方案文件就能改指标；残差超了判失败 | [AI / AO 的精度指标定多少](../maps/per-board-calibration/issues/CAL-02-what-accuracy-do-we-promise.md) |
| **`OpenPLC_Ports` 带单位的 AI / AO API**，套用修正值；没有有效校准值时退回标称换算并打日志；AI / AO 例程改用它 | 写入已知系数后读数按系数变；擦掉校准值区后退回标称并打日志 | [app 里怎么套用修正值](../maps/per-board-calibration/issues/CAL-06-how-does-the-app-apply-the-correction.md) |

## 开机提示改用指示灯（2026-09-28 定）

| 待办 | 怎么算做完 | 来自哪张票 |
|---|---|---|
| **上板验收**：新 bootloader 开机不动任何继电器 / DO / AO | 真板子上开机全程听不到继电器响；窗口内灯快闪、按住 BOOT0 进 upload 模式（`T1-27`）；按满 10 秒灯常亮、松手后恢复出厂 | [开机窗口改用什么提示](../maps/iec-61131-2-factory-state/issues/IEC-01-what-replaces-the-relay-click.md) |
