# SIM-05 结论：标「真板子」的用例里，哪些替身或 Renode 能跑

票：[SIM-05](issues/SIM-05-which-real-board-cases-the-stand-in-can-run.md)。2026-10-03 读代码 + 对着替身实跑得出。

## 出处缩写

| 缩写 | 指什么 |
|---|---|
| M1 / M2 / M3 | [M1-firmware-upgrade.md](../../docs/modules/M1-firmware-upgrade.md) §5、[M2-ownership.md](../../docs/modules/M2-ownership.md) §4、[M3-app-runtime.md](../../docs/modules/M3-app-runtime.md) §3 的用例表 |
| bs | `$TEST/host/bootstand/`（bootloader 替身，设计见 [BOOTLOADER-STAND-IN.md](../../docs/engineering/BOOTLOADER-STAND-IN.md)） |
| fb | `$TEST/host/fakeboard/`（替身的驱动：`run_cases.py` 跑 `T1-18a`–`g` 和 `T2-28`–`T2-30`，`run_ide_upload.py` 跑 `T1-34`） |
| TC | `$TEST` 根目录的 Go 用例程序（`main.go` + `udp_discovery.go` `tcp_session.go` `signature*.go`），接受 `--ip` `--port` |
| IAP | `$BOOT/IAPServer/` |
| repl | Renode 1.17 的 `platforms/cpus/stm32h7.repl` |
| REN-02 | [REN-02-findings.md](../renode-simulation/REN-02-findings.md)（Renode 每个外设有没有模型） |

## 判定口径

| 判定 | 含义 |
|---|---|
| **替身·已跑通** | 本次把现有脚本或出货工具原样对着替身跑，判据成立；**还没有自动判定接到 selfcheck** |
| **替身·可补** | 判据要看的东西替身给得出，缺驱动脚本或替身一个小开关（「要补什么」列写明） |
| **Renode·可补** | 要真 bootloader / app 二进制或真外设寄存器，替身没有、Renode 有模型 |
| **只能上板** | 判据看的是替身换掉的那一层（真 lwIP/PHY 时序、USB、TRNG、`.RamFunc` 擦扇区 0、引脚复用、物理端子），或 Renode 没有模型 |

替身能给什么、给不了什么，一句话：**IAP 的命令、认证、验签、扇区 15 全是真代码**（`bs/CMakeLists.txt:51-58`），**flash 是映射在原地址的文件、复位后还在**（`bs/host/hostmem.c:119-131`），**换掉的是 lwIP（PC socket）、HAL（`bs/host/hal_host.c`）、BOOT0 恒为「没按」（`bs/boot/main_boot.c:75`、`hal_host.c:70`）、SDRAM 自检恒过（`bs/boot/boot_glue.c:106`）、`flashboot` 落盘一律拒绝（`boot_glue.c:109-117`）、没有 USB CDC**。

## 一张总表（53 条）

### M1（27 条）

| # | 测什么 | 判定 | 理由和出处 | 已有替身用例 | 要补什么 |
|---|---|---|---|---|---|
| `T1-01` | 四个发现关键词都应答 | 替身·已跑通 | TC `T1-01 --ip=127.0.0.1 --port=61865` 通过；发现应答是真 `IAP/udp_server.c` | 无 | 驱动里起替身后调 TC（见文末「要补的驱动」） |
| `T1-02` | 连续多轮发现 | 替身·已跑通 | 同上，6 轮全答 | 无 | 同上 |
| `T1-03` | 发现回复在 2 s 内 | **只能上板** | 替身上 **FAIL**：20 次里 1 次超 2 s（均值 294 ms、最大 2.6 s）。时延来自 PC socket 桥（`bs/host/lwip_bridge.c` 的 `bridge_poll`），不代表板子 | 无 | — |
| `T1-04` | 10 分钟发现浸泡 | **只能上板** | 浸泡要抓的是 pbuf / 内存 / PHY 长跑问题，替身把 lwIP 换成了 `malloc` + socket（`lwip_bridge.c:103-123`） | 无 | — |
| `T1-05` | 泛洪限流且正常发现仍答 | 替身·已跑通 | TC 通过：807 包换来 150 个应答（50/s）；限流是真代码 `IAP/udp_server.c:37` | 无 | 驱动调 TC |
| `T1-06` | 一次只服务一个客户端 | 替身·已跑通 | TC 通过；拒绝由真 `IAP/tcp_server.c:113-116` 决定，桥按 lwIP 语义回 RST（`lwip_bridge.c:359-363`） | 无 | 驱动调 TC |
| `T1-07` | 空闲约 60 s 被踢 | 替身·已跑通 | TC 通过，`dropped after 1m1s`；计时是真 `tcp_server.c:22,97-102` | 无 | 驱动调 TC（单条 1 分钟，不进 selfcheck） |
| `T1-08` | 50 s 不被误踢 | 替身·已跑通 | TC 通过 | 无 | 同上 |
| `T1-09` | 传输中闯入不打断 | 替身·已跑通（证据弱） | TC 通过，但闯入方拿到的是「连接被拒」而不是被固件拒（日志里没有 `Refused second connection`）—— 本机传 87 KB 太快，敲门时替身可能已在复位 | 无 | 用更大的镜像，或判据加「替身日志在敲门时仍处于 `FLASH_RECEIVE`」 |
| `T1-10` | 第一条关闭后能再连 | 替身·已跑通 | TC 通过 | 无 | 驱动调 TC |
| `T1-11` | 无效签名被拒 | 替身·已跑通 | TC 通过，替身回 `Signature Failed`；验签是真 `IAP_server.c:560-575` | 无 | 驱动调 TC |
| `T1-12` | 签方不对被拒 | 替身·已跑通 | 同上 | 无 | 同上 |
| `T1-13` | 启动时重新验签 | 替身·可补 | 启动判定是真 `IAP_server.c:702-720,754`；替身每次「复位」重跑它，app 区就在 `state/flash.bin` 里 | 无 | 改 `flash.bin` 里 app 区一个字节 → 重启替身 → 判 `App signature invalid or absent`。Renode 也能跑，但替身更便宜 |
| `T1-14` | 失败上传不伤 app | 替身·可补 | app 区在 `flash.bin`，比对前后字节即可，不用 ST-Link | 无 | `T1-11` 前后各算一次 app 区（`0x08020000` 起）的 SHA-256 |
| `T1-17` | nonce 跨掉电不重复 | **只能上板** | 替身的随机数是 `BCryptGenRandom`（`hal_host.c:82-98`），测的是 PC。⚠️ **判据本身已过期**：写的是「计数器不归零」，决策 66 起 nonce 直接取 TRNG、计数器已删（`IAP/iap_auth.c:4-7`）；`$TEST/nonce_replay.go` 头注释仍按计数器格式解析 | 无 | 先按决策 66 重写判据（另开票） |
| `T1-21` | 掉电落在传输期，旧 app 照起 | 替身·可补 | 传输期 app 区不动（先暂存 SDRAM，`IAP_server.c:482-490`）；杀掉替身进程就是断电，`flash.bin` 是文件映射，杀进程不丢 | 无 | 传输中途杀替身 → 不带 `--fresh` 重启 → 判 `APP Mod`。真断电的电气过程只能上板 |
| `T1-22` | 掉电落在擦写窗口，重传能救 | 替身·可补 | 擦写窗口在 PC 上是微秒级，靠时机杀不中 | 无 | `hal_host.c` 加一个故障注入开关：第 N 次 `HAL_FLASHEx_Erase` / `HAL_FLASH_Program` 后直接退出（`hal_host.c:107-134`） |
| `T1-23` | 真实上传走完，擦除在验证之后 | 替身·可补（网口那支） | 本次替身日志里 `Transfer complete, verifying` 在前、`Erasing application region` 在后（`IAP_server.c:95`）。**CDC 那支只能上板**：替身没有 USB | `T1-34` ① 走完了一次网口上传，但只判 `Checksum and signature OK`，不判顺序 | 在驱动里判两行日志的先后 |
| `T1-24` | 坏 CRC 先于验签被拒 | 替身·已跑通 | TC 通过，回 `Checksum Failed` | 无 | 驱动调 TC |
| `T1-25` | CDC 模式不起以太网 | 替身·可补（决策那半） | 起不起网口由真 `IAP_servers_start()` 按模式决定（`IAP_server.c:846-860`），交接记录在 `sram4.bin` 里 | 无 | 往 `sram4.bin` 写一条 `BOOT_REQ_CDC` 交接记录（格式 `IAP/IAP_boot_handoff.c:177-260`）→ 判发现不应答，同轮正向对照写 `BOOT_REQ_ETH`。真 USB 枚举只能上板 |
| `T1-26` | 一次成功升级 = 7 槽 | 替身·可补 | 本次替身启动行 `0/3583` → `7/3583` → `14/3583`（`IAP/bootloader_state.c:282`），复位不用 ST-Link | 无 | 驱动读两次启动行求差。⚠️ 见文末「顺带发现」第 3 条：总数是 3583 不是 3840 |
| `T1-27` | 按住 BOOT0 复位进上传模式 | Renode·可补 | 手势在 `$BOOT/Core/Src/main.c:400-421`，替身没编它（`main_boot.c` 自己调 `server_decide(0U)`）。Renode 跑真 bootloader，`gpioPortG` 有模型（repl:131），可在启动窗口内拉高 PG9 | 无 | Renode 脚本拉 PG9。⚠️ `Reset cause: PIN` 要靠 `STM32H7_RCC`（repl:513）的 `RSR` 模型，**没核实** |
| `T1-28` | metadata 满了 reclaim，校准值原样搬 | 替身·可补 | reclaim 是真 `bootloader_state.c:200`；本次 `setowner --wipe` 已触发一次 `Reclaiming sector 15 (28 metadata slots, root area compacted)`。灌满只要直接写 `flash.bin`，不受 ST-Link「写一部分先擦整扇区」的限制 | 无 | 往 `flash.bin` 扇区 15 写满 metadata + 一段可辨认的校准值 → 上传一次 → 判 reclaim 行和校准值逐字节还在。⚠️ 判据原文过期，见「顺带发现」第 2 条 |
| `T1-29` | `flashboot` 换掉 bootloader | **只能上板** | 替身落盘一律拒（`boot_glue.c:109-117`）；判据要看新 bootloader 报的版本，而替身的 bootloader 是 PC 程序，换不掉。Renode 跑得了真二进制和 flash 控制器（repl:66），但要网口 —— 等 [SIM-02](issues/SIM-02-does-ethernet-work-in-renode.md) | 无 | — |
| `T1-30` | 叶证书签的 bootloader 镜像被拒 | 替身·已跑通 | 本次 `IAPTool flashboot --key=<叶>`：替身回 `Signature Failed`，日志 `Bootloader untouched`（`IAP_server.c:560-575`）。替身扇区 0 本来就是空的，「扇区 0 一字节没动」只有上板才有分量 | 无 | 驱动里跑一次 |
| `T1-31` | 换完 bootloader 所有权还在 | **只能上板** | 依赖 `T1-29` 真的落盘（`IAP/boot_selfupgrade.c` 的 `.RamFunc`），替身不编它 | 无 | — |
| `T1-32` | 未认领板 `flashboot` 要按 BOOT0 | 替身·可补（拒绝那半） | 无根时真代码一律回 `Refused`（`IAP_server.c:467`）。本次 IAPTool 在发命令前就自己拦了，要验板子侧得发原始命令。⚠️ **判据后半「按住再来 → 成功」和代码对不上**，见「顺带发现」第 1 条 | 无 | 用 TC 的原始上传路径（`signature.go` 的 `uploadImage`）发 `flashboot`，判 `Refused` |

### M2（21 条）

| # | 测什么 | 判定 | 理由和出处 | 已有替身用例 | 要补什么 |
|---|---|---|---|---|---|
| `T2-01` | `takeown` 把无根板绑到新钥 | 替身·已跑通 | 本次全新替身上 `IAPTool takeown` → `Board claimed`，随后 `getowner` 认得 | `T2-28` 走的是「上传时自动认领」，不是 `takeown` 命令 | 驱动里加「重启后仍认得」和 `.pem` 不在临时目录两条判定 |
| `T2-02` | 已认领板拒绝第二次认领 | 替身·可补 | 本次第二次 `takeown` 被 IAPTool 的前置检查拦下，板子侧没跑到；板子侧拒绝是真 `IAP_server.c:234-266`，主机用例 `T2-31` 已盖其逻辑 | 无 | 发原始 `takeown`，判 `Refused` 且 `getpubkey` 不变 |
| `T2-03` | 换 owner 要现任签名 | 替身·可补 | 本次正向 `setowner` 通过、generation +1；负向要 `run_setowner.py --bad-signature` 拼的坏签名 | 无 | 把 `run_setowner.py` 的坏签名拼法搬进驱动 |
| `T2-04` | 无签名高 generation 夺不走 | 替身·可补 | 原脚本用 ST-Link 写记录；替身直接写 `flash.bin` 根区（`0x081E2000`，同 `$TEST/host/renode/run.py:40`） | 无 | 写记录 → 重启 → 判 `getpubkey` 仍是原主人 |
| `T2-05` | 恢复出厂回到无根 | 替身·可补 或 Renode·可补 | 恢复出厂由 `main.c:407-417` 在手势后调真 `owner_slot_factory_reset(true)`。替身缺手势，Renode 有真手势代码 | 无 | 替身：`main_boot.c` 加 `--gesture none/upload/factory`，照抄 `main.c:400-421` 的分支；Renode：PG9 拉高 > 10 s 虚拟时间再放开 |
| `T2-09` | 恢复出厂让原 app 失效 | 同 `T2-05` | 失效由真启动判定给出（`IAP_server.c:702-720`） | 无 | 同 `T2-05`，再判 `App signature invalid or absent` |
| `T2-10` | 换根后旧根镜像装不进 | 替身·可补 | 本次换根后旧叶上传被 IAPTool 前置检查拦下；板子侧要原始上传，app 区比对用 `flash.bin` | 无 | 原始上传 + app 区前后 SHA-256 |
| `T2-11` | 真板子收下委托证书并执行 | 替身·已跑通 | 本次根签发叶证书，叶钥上传 → 替身 `Checksum and signature OK` → 复位进 app；验链是真 `IAP/iap_cert.c` | `T1-18d` 只测工具的判断，不走到板子执行 | 驱动里跑一次 |
| `T2-12` | 换根后旧叶 app 下次启动被拒 | 替身·已跑通 | 本次 `setowner` 后重启替身 → `App signature invalid or absent` | 无 | 驱动里跑一次 |
| `T2-13` | 换根后旧叶再上传被拒 | 替身·可补 | 本次被 IAPTool 前置检查拦（`was not issued by this board's root`），板子侧没跑到 | 无 | 原始上传 + app 区比对 |
| `T2-14` | 换根后新叶能传能起 | 替身·已跑通 | 本次新根签的叶上传 → 复位 → `APP Mod` | 无 | 驱动里跑一次 |
| `T2-15` | 撤销不碰已装固件 | 替身·可补 | 启动判定刻意不看撤销（`IAP_server.c:710-716`）；本次撤销后没单独重启验 | 无 | 撤销 → 重启 → 判 `APP Mod` |
| `T2-16` | 被撤的叶再上传被拒 | 替身·已跑通 | 本次撤销后叶上传在会话认证就被拒（`Auth rejected: ... the leaf has been revoked`） | 无 | 加 app 区比对 |
| `T2-17` | 撤销不连坐 | 替身·已跑通 | 本次同根另一张叶照常上传并起来 | 无 | 驱动里跑一次 |
| `T2-18` | 坏签名撤销记不进去 | 替身·可补 | 撤销验签是真 `IAP_server.c:348` 起那段 | 无 | 照 `run_revoke_leaf.py --bad-signature` 拼 |
| `T2-19` | 连续撤两个都生效 | 替身·可补 | 替身编的是真 `owner_slot.c` + `iap_cert.c`（`bs/CMakeLists.txt:55-56`），**正好补上 M2 脚注 ⁷ 说的「bootloader 侧 `resolve_chain()` 主机零覆盖」** | 无 | 撤两张 → 重启 → 判 `2 leaf(s) revoked`，两张都传不进、第三张能传 |
| `T2-20` | 重复撤销幂等 | 替身·可补 | 同上 | 无 | 判 `OK already revoked` 且 `N/96` 不变 |
| `T2-25` | `setowner --wipe` 回收名额 | 替身·已跑通 | 本次：generation 3、`96/96 revoke slot(s) free, 0 leaf(s) revoked`，扇区 0–14 逐字节未变。替身扇区 0 是空的，「不碰扇区 0」只有上板才有分量 | 无 | 驱动里跑一次 |
| `T2-26` | 板子报得出签名者被撤 | 替身·已跑通（两支）+ 可补（第三支） | 本次 `getapprevoked`：撤销后答被撤，换成没撤的叶后答 `still trusted`。第三支「板上没固件」在全新替身上天然成立，省掉 M2 脚注 ¹⁶ 那次手工 | 无 | 全新替身先认领不上传，判答「没有」 |
| `T2-35` | 出厂板经 USB 第一次上传被认领 | **只能上板** | 替身没有 USB CDC（BOOTLOADER-STAND-IN.md「测不到什么」）；Renode 的 USB2 OTG FS 只是 Tag（repl:792） | `T2-28` 盖了认领逻辑（经网口） | — |
| `T2-36` | 恢复出厂后经网口再次认领 | 替身·可补 | 认领那半 `T2-28` 已盖；恢复出厂那半同 `T2-05` | `T2-28` | `--gesture factory` 之后接 `T2-28` 的 `claim-new-key`，判两把私钥不同 |

### M3（5 条）

| # | 测什么 | 判定 | 理由和出处 | 已有替身用例 | 要补什么 |
|---|---|---|---|---|---|
| `T3-01` | 启动 SDRAM 自检 | Renode·可补（通过那支） | 替身把自检桩成恒过（`boot_glue.c:106`）。Renode 在 `0xC0000000` 有内存（repl:63）、FMC 是 Python 桩（repl:748），能跑出 `SDRAM staging buffer OK`；**坏 SDRAM 那支（`$BOOT/Core/Src/fmc.c:129`）只能上板** | 无 | Renode 让 bootloader 停在上传模式（不放 app），判 UART4 上那一行 |
| `T3-02` | `OpenPLC_SDRAM` 封装 19 条断言 | Renode·可补（断言部分） | 断言只读写内存，Renode 有；但结果经 `Serial`（USB CDC）输出，要等 [SIM-01](issues/SIM-01-how-to-see-serial-in-renode.md)。**清零速率只能上板** | 无 | SIM-01 定了之后加进 Renode 用例 |
| `T3-03` | `Serial4.begin()` 不掐掉诊断口 | **只能上板** | 原故障是引脚复用冲突把 app 挂死（M3 脚注 ³），Renode 的 GPIO 不建模复用功能对 UART 的影响 | 无 | — |
| `T3-04` | RS232 端子收发 | **只能上板** | 判据是端子 C05/C06 上的电平；例程回显逻辑 Renode 能测（REN-02 `RS232_Echo` 行），那归 `T3-05` / SIM-06 | 无 | — |
| `T3-06` | 自有库例程逐个在真板测通 | 部分 Renode·可补 | 哪些例程 Renode 判得了见 REN-02 表；放进哪条用例由 [SIM-06](issues/SIM-06-which-case-holds-the-example-behaviour-checks.md) 定。端子电平、AO 电流、真 USB 只能上板 | 无 | 等 SIM-06 |

## 小结

| 判定 | 条数 | 哪些 |
|---|---|---|
| 替身·已跑通 | **19** | `T1-01` `T1-02` `T1-05`–`T1-12` `T1-24` `T1-30` `T2-01` `T2-11` `T2-12` `T2-14` `T2-16` `T2-17` `T2-25`（`T2-26` 两支也跑通，计入下一行） |
| 替身·可补 | **20** | `T1-13` `T1-14` `T1-21`–`T1-23` `T1-25` `T1-26` `T1-28` `T1-32` `T2-02`–`T2-04` `T2-10` `T2-13` `T2-15` `T2-18`–`T2-20` `T2-26` `T2-36` |
| 替身或 Renode·可补 | **2** | `T2-05` `T2-09` |
| Renode·可补 | **4** | `T1-27` `T3-01` `T3-02` `T3-06`（后三条只覆盖一部分） |
| 只能上板 | **8** | `T1-03` `T1-04` `T1-17` `T1-29` `T1-31` `T2-35` `T3-03` `T3-04` |

**「可补」的不替代上板。** 替身跑通说明 IAP 的决策逻辑对；同一条在真板子上还要验 lwIP / PHY、USB、真 flash 擦写和掉电。所以用例表的「条件」列应写成「替身 + 真板子」两档，不是把「真板子」换掉。

## 要补的驱动（一个脚本 + 替身三个开关）

| 补什么 | 放哪 | 服务哪些用例 |
|---|---|---|
| 一个驱动：起替身、按用例摆状态（写 `flash.bin` / `sram4.bin`）、不带 `--fresh` 重启、读替身日志、调 TC 的现成用例、调暂存的 IAPTool。复用 `fb/_common.py` 的 `build_stand_in` `start_stand_in` `stage_iap_tool` | `fb/` 下新脚本；`_common.py` 加 `read_flash` / `write_flash` / `restart` 三个函数 | 上表所有「替身」行 |
| `--gesture none/upload/factory`：照 `$BOOT/Core/Src/main.c:400-421` 在 `server_decide` 前调 `owner_slot_factory_reset`、传 `boot0Pressed` | `bs/boot/main_boot.c` + `bs/host/hostctl.c` | `T2-05` `T2-09` `T2-36` |
| 故障注入：第 N 次擦 / 写 flash 后退出进程 | `bs/host/hal_host.c` | `T1-22` |
| 版本号用构建参数 `-DAPP_VERSION=…` 另编一份（已有，`bs/CMakeLists.txt:13-18`），不用改代码 | 驱动里另配一个构建目录 | 烧录前比版本（M1 §1「比什么」，没有 `T1` 编号） |

本次已用第四行验过：app 一半报 `9.9.9` 时上传 `1.0.0`（`.version` 旁置文件）被 IAPTool 拒；`--force` 放行并打 `FORCE FLASH`；紧接着再 `--force` 报 `force flash has already been used once`。**烧录前比版本整条在替身上跑得通**，它目前在 M1 里没有用例编号。

## 本次实跑了什么、测不到什么

> ✅ **结论**：全部在**替身（真 IAP 代码跑在 PC 上，Windows）**上跑，没有真板子、没有 Renode。

| 跑了什么 | 结果 |
|---|---|
| `python host/fakeboard/run_cases.py`（现有 `T1-18a`–`g`、`T2-28`–`T2-30`） | 9 条全过 |
| TC 的 `T1-01` `T1-02` `T1-03` `T1-05`–`T1-12` `T1-24`，`--ip=127.0.0.1 --port=61865` | 除 `T1-03` 外全过；`T1-03` 失败原因见上表 |
| 出货 IAPTool 手工走：叶证书上传、撤销、`getapprevoked`、换根、`--wipe`、`flashboot`（叶 / 根）、`takeown`、比版本 | 见上表各行 |

**测不到**：真 lwIP / MAC / PHY 和时序（`T1-03` 就栽在这）；USB CDC；`flashboot` 落盘；TRNG；BOOT0 手势；Renode 那几行一条都没跑，只读了平台文件。所有临时文件都在会话 scratchpad，没写任何仓库。

## 顺带发现（文档和代码对不上）

| # | 是什么 | 在哪 | 影响 |
|---|---|---|---|
| 1 | `T1-32` / `R1-37` 写「未认领板按住 BOOT0 再发 `flashboot` → 成功」；决策 72 后代码对无根板一律 `Refused`，不看 BOOT0 | M1 表 `T1-32` 行、M1 `R1-37`；代码 `IAP_server.c:467`；[FLASHBOOT.md](../../docs/modules/M1/FLASHBOOT.md):30 已是新说法 | 照旧判据上板会判失败 |
| 2 | `T1-28` 判据里的日志原文已变：代码打 `... reclaims sector 15.` 和 `Reclaiming sector 15 (<n> metadata slots, root area compacted)`，判据写的是 `... reclaims it.` 和 `Reclaiming metadata area (<n> slots discarded)` | M1 表 `T1-28` 行；`bootloader_state.c:200,286` | 按原文匹配的脚本会漏判 |
| 3 | metadata 区总槽数：代码跑出 `/3583`（[SECTOR-15.md](../../docs/modules/M1/SECTOR-15.md):36 也写 3583 ÷ 7 = 511），另几处仍写 3840 / 548 次 | M1-firmware-upgrade.md:224、:443；SECTOR-15.md:6、:228；[HOW-TO-RUN-TESTS.md](../../docs/engineering/HOW-TO-RUN-TESTS.md):421-422 | 灌满 reclaim 的脚本若按 3840 算，会多灌 |
| 4 | `T1-17` 判据「计数器不归零」和 `$TEST/nonce_replay.go` 头注释仍是计数器 nonce；决策 66 已改 TRNG | M1 表 `T1-17` 行；`IAP/iap_auth.c:4-7` | 这条用例现在判的东西不存在了 |

✅ **上表四处 2026-10-03 已改**：M1 的 `R1-37` / `T1-32`（标为要按新判据重跑）、`T1-28` 判据原文、3583 格 / 511 次（M1、SECTOR-15、HOW-TO-RUN-TESTS、决策 61 加注）、`T1-17` 判据；`$TEST` 的 `nonce_replay.go` 改按 TRNG 判、`run_au1.py` 去掉计数器对照、`run_journal_reclaim.py` 按决策 72 的扇区 15 布局读写（原来写回时会抹掉根区）。
