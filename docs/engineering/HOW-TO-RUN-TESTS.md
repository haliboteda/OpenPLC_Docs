# 测试怎么跑

**每条用例的判据、前置条件、怎么跑都在这里。** 需求和最近结果在 [STATUS.md](../tables/STATUS.md)。

测试按部件、契约、整机三层分在各仓（[决策 78](../tables/DECISIONS.md)）。每个仓有自己的自检入口，不靠别的仓：

| 仓 | 测什么 | 入口（在那个仓的根目录跑） |
|---|---|---|
| `$BOOT` | bootloader 的主机 C 测试（T1-16、T1-33、T2-22–T2-34 中归 bootloader 的）、P16、P17 | `cd tests && cmake --preset local && cmake --build --preset local && ctest --preset local` |
| `$CORE_REPO` | P3、P4、P5、P15、P19、T2-21 | `python tests/selfcheck.py`（`--full` 加上约 45 分钟的 P5） |
| `$TOOL` | T1-15、T1-35、T1-19 / T1-20 | `python tests/selfcheck.py` |
| `$PORTTOOL` | T4-01 到 T4-04 | `cd TestCase && python tools/selfcheck.py`（`--quick` 跳过浏览器那步） |
| `$TEST` | 契约（P1、P2、P11、P20、T1-18）、整机（`TestCase.exe`、上板脚本、T1-34、T1-37、T3-05）、P10 | `python tools/selfcheck.py`（`--quick` 跳过慢的；上板脚本不进自检） |
| `$PROD` | 文档检查 P7、P8、P9、P12、P13、P14、P18 | `python tools/check_docs.py` |

**下文的 `tools/...`、`host/...`、`onboard/...` 不加前缀时都在 `$TEST` 根目录跑。** 其他仓的命令写明仓名。

需要「传输进行中」的用例不会自己实现传输，而是**把 IAPTool 当子进程拉起来**跑真实烧写 —— 被测的始终是出货代码路径，不是测试代码里的仿制品。

## `$TEST` 的本机配置

⚠️ **机器相关的路径只允许出现在 `$TEST/config/machine.py`**（PortTool 另有自己的一份）。它是 `tools/init_machine.py` 生成的，不要手写、也没有模板可抄；需要新的本机路径时，把它连同探测方式加进那个脚本的 `SETTINGS` 表。

⚠️ **`init_machine.py` 有单元测试**：`python tools/test_init_machine.py`（**32 个用例**，四组）。

| 组 | 测什么 | 为什么只能这么测 |
|---|---|---|
| tables | `SETTINGS` / `PREREQS` / `EXAMPLES` 的列是否齐 | 三张手写表，最常见的编辑错误是加了一行漏一列；不测的话报错发生在你不在场的那台机器上 |
| ports | `detect_log_ports()` 的 **macOS 分支** | 本项目没有 mac，所以文件系统是假的，只测排序与去重逻辑 |
| claude dirs | `--write-claude-dirs` 的合并、`ignored_by_own_rules()` 的护栏 | 它改的那个文件装着几百条手工批准的权限规则，**"没弄丢东西"就是被测的性质** |
| ask_for | 引号剥离、`~` 展开、安装根目录校验 | 提问按定义在自动化里跑不到（只在"stdin 是终端且环境无自动化标记"时发生），只能替换 `input()` |

退出码：0 全过，1 有失败，2 全过但 ask_for 那组因这台机器没有真 CubeIDE / Arduino IDE 而跳过 —— **不假装通过**。

```
python tools/init_machine.py      # 一次性：探测本机路径，生成 config/machine.py（Linux 上是 python3）
python tools/selfcheck.py         # 不需要板子的检查；--list 先看它跑哪几步
python tools/flash_bootloader.py  # 命令行编 bootloader、ST-Link 烧写、抓启动日志（CubeIDE 必须关闭）
python tools/serial_watch.py      # 只看串口，不碰板子
```

⚠️ **测试脚本一律用 Python**（2026-09-01 定）。缺什么会报 `SKIP` 并说清缺什么，**不会静默跳过**。

## 编译 `TestCase.exe`

```sh
# 在 $TEST 下
go build -o Output/windows/TestCase.exe .
```

`go.mod` 用 `replace IAPTool => ../IAPTranfer_Tool` 引用 IAPTool 的公开包（`iapcert`、`iapproto`、`netiface`），所以 IAPTranfer_Tool 要放在旁边。

## 运行

```sh
TestCase <case-id|all> --ip=<addr> [--port=56865] [--bin=<file.bin>] [--iaptool=<path>]
         [--key=<owner.pem>]
```

- `--ip` 必填。设备 IP 从串口日志的 `[NET]` 行读，或用 `IAPTool ether` 的广播发现看。
- `--bin` T1-09 / T1-11 / T1-12 需要；`--key` T1-11 / T1-12 需要，是板子当前信任的那把私钥。
- `--iaptool` 默认找 `Output/windows/IAPTool.exe`。
- 退出码：全过 0，有失败 1，参数错 2。

## 用例

### TCP 会话规则（`tcp_session.go`）

设备一次只服务一个客户端，且空闲客户端不能永久占住端口。

| ID | 验证什么 | 前置条件 | 判据 |
|---|---|---|---|
| **T1-07** | 空闲连接 60s 后被踢 | 设备停在 bootloader | 连上后保持沉默，在 ~60s（容差 +15s）内被对端关闭 |
| **T1-08** | 空闲连接 50s 内**不**被踢 | 设备停在 bootloader | 沉默 50s 后连接仍在，且 `ping` 仍答 `OK` |
| **T1-06** | 已有连接时第二个连接被拒 | 设备停在 bootloader | 第二个连接被拒（或虽接上但不被服务），**且第一个连接不受影响** |
| **T1-09** | 传输进行中的第二个连接不打断传输 | 设备停在 bootloader，需 `--bin` | IAPTool 报告传输完成且退出码 0，闯入的连接未被服务 |
| **T1-10** | 第一个连接正常关闭后能再连 | 设备停在 bootloader | 关闭后重连成功并被服务 |

### UDP 发现（`udp_discovery.go`）

每一次以太网升级都从一条发现回复开始，所以发现一旦不稳，现场看到的是"板子不见了"。

| ID | 验证什么 | 前置条件 | 判据 |
|---|---|---|---|
| **T1-01** | 四个关键词都应答 | 设备在线 | `openplc_server_where_r_y` / `DISCOVER` / `openplc_discover` / `ping` 全部有回复 |
| **T1-02** | 多轮间隔查询都应答 | 设备在线 | 6 轮全部有回复 |
| **T1-03** | 回复落在工具的超时之内 | 设备在线 | 20 轮全部在 2s（IAPTool 的 `CommandTimeout`）内返回 |
| **T1-04** | 长时间浸泡下发现依然可靠 | 设备在线，`--minutes=N`（默认 10） | 整段时间内零次无应答 |
| **T1-05** | 泛洪被封顶，且封顶不会把发现打死 | 设备在线 | 以约 500 次/秒猛打 3 秒，回复速率不超过 50/s 的上限；**且随后正常查询仍能应答** |

### 签名校验（`signature.go`）

| ID | 验证什么 | 前置条件 | 判据 |
|---|---|---|---|
| **T1-11** | 签名无效的镜像被拒绝 | 设备停在 bootloader，需 `--bin` 和 `--key`（板子信任的那把，用来签挑战） | 传完后设备回 `Signature Failed`（或 `No Signature`） |
| **T1-12** | 被**别的密钥**签过的镜像被拒绝 | 同 T1-11，另需 `--iaptool`（用它生成临时密钥并签名） | 同上。**外加**上传前 `getpubkey` 必须和临时密钥不同 |
| **T1-13** | **已装好的** app 被改坏 → 启动期拒绝 | 板上有能启动的 app、ST-Link、**一个已签名的恢复镜像** | `metadata present` + `App signature invalid or absent`，且**没有** `** APP Mod` |
| **T1-14** | 被拒绝的上传**不破坏已装好的 app** | 紧接 T1-11 之后复位 | 下次启动出现 `** APP Mod ...`，**不是** `no valid application`。用 `python tools/run_case.py --case T1-11 --then-reset` 跑 |

```
python tools/run_s3.py --bin <app.bin>       # 破坏 + 判定 + 自动恢复
```

### 所有权（`python tools/run_takeown.py`，需求 R2-02）

T2-01 / T2-03 的动作走出货工具（`IAPTool takeown` / `setowner`），判据向板子要（原始 TCP `getowner` / `getpubkey`）。`--bad-signature` 是例外：出货工具做不出坏签名，那条验的是板子的行为，所以在用例里手工拼记录。

| ID | 验证什么 | 前置条件 | 判据 |
|---|---|---|---|
| **T2-01** | 认领把板子绑到一把新密钥上 | 板子停在 bootloader，**且这次启动按住过 BOOT0** | 判据见模块文档的测试表 |
| **T2-02** | BOOT0 没按时认领被拒 | 停在 bootloader，**没按 BOOT0**（用 `enter_bootloader.py` 进） | 回 `Refused`，`getpubkey` **一字节不变** |

| **T2-03** | 换 owner：现任签名才算数 | 板子已被一把**你持有私钥**的密钥认领 | 判据见模块文档的测试表 |
| **T2-04** | 无签名的高 generation 记录**夺不走**板子 | 同上 | 扫描器看得见那条记录，但 `getpubkey` 仍返回原主人 |
| **T2-05** | 恢复出厂回到没有根 | 板子已被认领，**有人在板子旁**按住 BOOT0 十秒 | 判据见模块文档的测试表 |

```
python tools/run_takeown.py --key b.pem --expect-refused  # 已有根时认领被拒，不需要人
python tools/run_takeown.py --key a.pem                # 无根板子认领，不需要人
python tools/run_setowner.py --current-key a.pem      # 换 owner，不需要人
python tools/run_setowner.py --current-key a.pem --bad-signature
python tools/inject_owner_record.py --key <hex> --also-unsigned 9   # 夺取攻击
```

### 认证与重放（`nonce_replay.go`）

| ID | 验证什么 | 前置条件 | 判据 |
|---|---|---|---|
| **T1-17** | nonce 不重复，且**掉电后不从头开始** | 设备停在 bootloader；**要人工断电一次**；VBAT 电池在位 | 两阶段所有 nonce 互不相同；阶段内计数器恰好 +1；断电后的第一个计数器**严格大于**断电前最后一个 |

```
python tools/run_au1.py                 # 编排两个阶段，中间提示你拔电
python tools/run_au1.py --resume         # 阶段 1 已经跑过了，直接等断电
```

### 委托证书怎么在真板子上复现

判据见对应模块文档的测试表。

```
# 管理员：用板子当前信任的那把根，给"同事"的公钥发一张证书
IAPTool pubkey <同事>/keys/fw_signing_key.pem          # 128 hex
IAPTool cert <那 128 hex> --key=<owner.pem> > <同事>/keys/fw_signing_key.pem.cert

# 同事：什么参数都不用加
IAPTool ether app.bin <ip>
```

判据三条，缺一不可：

1. 工具打出 `Certificate was issued by this board's root (<根前16位>...)` —— 不是 `Signing key matches this board`，那是自签路径
2. 上传成功，串口出现 `Checksum and signature OK`
3. **复位后进 `** APP Mod`** —— 证明启动期拿存下来的那张证书重验也过了，不只是上传时过了

反向：把证书换成另一把根签的，工具必须**在传输开始前**就拒，且报的是"这张证书不是这块板的根签的"。

## ⚠️ 上板之前先看测试资产的日期

**`Output/` 下的探针镜像不会自动跟着仓库走**，
过期的那一份会给出一个看起来像产品故障的失败。

| 踩过的 | 症状 |
|---|---|
| `Output/iap_probe_app.bin`（2026-09-18 编） | 早于证书 132→128 字节那次变更，app 侧验不了新证书，**重启握手九次全拒**。当前镜像在 `Output/probe-images/` |

**判断标准**：失败的那一步是「够到板子了吗」还是「板子答错了」。够不到就先查日期。

## 怎么让设备停在 bootloader

T1-07–T1-10 和 T1-11 都要求设备处于 bootloader 且以太网已起。三种办法：

1. **`python tools/enter_bootloader.py`** —— 全自动，不需要碰板子。**推荐**
2. **按住 BOOT0 复位** —— 日志出现 `** UPLOAD Mod ... (BOOT0 held)`
3. 让 app 收到认证过的 UDP reboot（`IAPTool ether` 的第一步就是这个），但它随后会真的上传

## 主机侧测试（不需要板子）

跑得快、随时能跑，**改完代码先过这一层再上板**。

| 目录 | 怎么跑 | 覆盖什么 |
|---|---|---|
| `$TOOL/tests/iapcert/` | 在 `$TOOL` 下 `go test ./tests/...` | 证书布局与根签名覆盖的字节范围（换个范围就验错东西）；serial 计数器从 1 开始、递增、落文件；serial 小端落在偏移 64；挑战签名覆盖 `sha256(nonce\|\|msg)` 且顺序不可换 |
| `$TOOL` 根目录、`internal/`、`iapproto/`、`netiface/` | 在 `$TOOL` 下 `go test . ./internal/... ./iapproto/... ./netiface/...` | **T1-35** IAPTool 自己的单元测试：密钥查找顺序（`--key` → `local_config.json` → 用户配置目录 → exe 旁边）、串口层、`internal/iapproto` 的协议常量与绑物理网卡拨号。进 selfcheck |
| `$BOOT/tests/bootloader_unit/` | `$BOOT/tests` 下 `ctest --preset local -R T1-16`，需要 gcc/clang 和 CMake | 用 stub 在主机上编译**真实的** `sha256.c` / `iap_cert.c` / `fw_verify.c` / `iap_auth.c` 并跑断言。金标证书由出货工具生成，所以过了就等于 C 和 Go 对同一套线格式达成一致。细节见 `$BOOT/tests/bootloader_unit/HOST-C-TESTS.md`（贴着代码放） |
| `$CORE_REPO/tests/owner_revoke/` | `$CORE_REPO/tests` 下 `ctest --preset local`，需要 gcc/clang 和 CMake | **T2-21** 当前生效的根撤不掉自己（`R4`）。喂一块 RAM 里的假 owner 记录区（按 `owner_slot.h` 的字节布局手搓），在主机上编译并跑**真实的** `owner_root_ro.c`。判据见 [M2 归属与信任](../modules/M2-ownership.md) 的「测试怎么跑」节 |
| `$BOOT/tests/owner_capacity/` | `$BOOT/tests` 下 `ctest --preset local -R "T2-2|T2-3|T1-33"`，需要 gcc/clang 和 CMake | owner 区容量、压缩、`--wipe`、自撤、出厂无根、恢复出厂、连续 40 次换主（T2-22–T2-33、T1-33、T2-27）。判据见 [M2 归属与信任](../modules/M2-ownership.md) |
| `$BOOT/tests/sector15_reclaim/` | `$BOOT/tests` 下 `ctest --preset local -R T2-34`，需要 gcc/clang 和 CMake | **T2-34** 扇区 15 回收中途断电。在主机上编译**真实的** `bootloader_state.c` / `bkp_stash.c` / `owner_slot.c`，flash 和备份 SRAM 用 RAM 代替，在每次 flash 操作之前逐个断电。判据见 [M2 归属与信任](../modules/M2-ownership.md) |
| `host/fakeboard/` | `python host/fakeboard/run_cases.py` | **T1-18a–T1-18g** IAPTool 在传输开始前的密钥/证书匹配决策，六种情况：自签的两种 + 委托证书的三种 + 一把密钥都没有（`T1-18c` 老 bootloader 那种按决策 79 作废）。对着 bootloader 替身跑（`$TEST/host/bootstand`：真 bootloader 代码编成的 PC 程序，见 [BOOTLOADER-STAND-IN.md](BOOTLOADER-STAND-IN.md)），过了工具这一关的几例会真的上传、被替身验签。七种情况的判据见 `$TEST/host/fakeboard/KEY-MATCH.md`（贴着代码放） |
| `host/fakeboard/` | `python host/fakeboard/run_ide_upload.py [--keep]`，需要 arduino-cli | **T1-34** 从 `arduino-cli upload`（IDE 那条命令）烧 bootloader 替身（真 bootloader 代码 + 板卡包 app 一侧的重启握手）：未认领 / 已认领 / 密钥不对。判据和测不到什么见 [M1 固件升级](../modules/M1-firmware-upgrade.md) 的「测试怎么跑」节。⚠️ **几分钟，不进 selfcheck** |
| `host/fakeboard/` | `python host/fakeboard/run_lifecycle.py [--only ID] [--keep]`，selfcheck 的 `T1-22` `T1-38` `T2-05` `T2-19` 四步就是它 | **T1-22 T1-38 T2-05 T2-09 T2-19 T2-20 T2-36** 在 bootloader 替身上：掉电落在擦写窗口、比版本、恢复出厂（`--gesture factory`）及其后果、连续撤销和重复撤销。判的是真 bootloader 代码的决定；按键、真 flash 擦写窗口、CDC 那支仍要真板子 |
| `$TOOL/tests/crypto_ref/` | 在 `$TOOL` 下 `python tests/crypto_ref/run_checks.py [--rounds N]` | SHA-256 构造对 hashlib（309 向量）；IAPTool 真实签名交给一份独立的纯算术 P-256 验证器。对照方法见 `$TOOL/tests/crypto_ref/CROSS-CHECK.md`（贴着代码放） |
| `$CORE_REPO/tests/variant_check/` | `python tests/variant_check/build.py`，需要 arduino-cli（环境变量 `ARDUINO_CLI` / `ARDUINO_CLI_CONFIG`） | **P4** Arduino 变体头的编译期断言。目前两个：`m4_fmc_pins`（FMC 保留脚表 39 个自洽）、`uart_routing`（printf 控制台在 USART3/PC10，扩展口留着 UART4/PH13-14）。**编不过就是变体头坏了，不是 sketch 坏了** |
| `$CORE_REPO/tests/examples_build/` | `python tests/examples_build/build.py [--only LIB]`，需要 arduino-cli | **P5** 编译板卡包里**每一个能在这块板上编的 example**（自有库 + 上游库）。⚠️ **约 45 分钟，故意不进 selfcheck** —— 见下 |
| `host/renode/` | `python host/renode/run.py [--only NAME]`，需要 arduino-cli 和 Renode（`$RENODE`）。⚠️ `$BOOT/Debug/` 里必须是 bootloader，是工装镜像时跳过 | **T3-05** `OpenPLC_Ports` 的 13 个例程在 Renode 里经真 bootloader 启动，判启动链、`setup()`、`loop()`、没跑飞。判据和测不到什么见 [M3 应用运行环境](../modules/M3-app-runtime.md) 的「测试怎么跑」节。⚠️ **约 25 分钟（每个例程先编译），进 selfcheck，`--quick` 跳过** |
| `host/renode/` | `python host/renode/boot_outputs.py`，需要 arduino-cli、Renode 和 CubeIDE（把 `$BOOT` 工作区拷进临时目录编，不碰 `$BOOT/Debug/`） | **T1-37** 开机输出置 0：真 bootloader 跳进 `SystemLED`，DO1–DO8、PA4、PA5、PB14 在五个时刻都是推挽输出、电平为低；BOR 档位不是 3 时串口警告、是 3 时不警告。判据和测不到什么见 [M1 固件升级](../modules/M1-firmware-upgrade.md) 的「测试怎么跑」节。⚠️ **约 11 分钟（编 bootloader 和例程占大头）**，进 selfcheck，`--quick` 跳过 |

⚠️ **bootloader 替身的上传通道用 61865，不用产品端口 56865**（`$TEST/host/fakeboard/_common.py` 的 `TEST_PORT`）：本机的 56865/TCP 可能被别的程序占着。复制到临时目录的 IAPTool 也写上这个端口，所以两边对得上；板子和出货的 IAPTool 仍是 56865。T1-34 的发现走的是板卡包写死的 56865/UDP，替身在那里也应答。替身每次跑都会先编一遍，要 `HOST_CC` 和 CMake。

### P5 · example 不能腐烂

**范围**：自有库（`OpenPLC_*`）和上游库的例程都编。上游例程里本来就不面向 H743 的（别的芯片的外设、这块板没有的 USB 功能）列在 `build.py` 的排除表里，每条带一句理由（决议 68）。

**什么时候跑**：改了 `open_plc_arduino` 的任何库之后，以及发版前。**不在 `selfcheck` 里** —— selfcheck 是"改完代码就跑"的东西，往里加 45 分钟只会让人不跑它。

```
python tests/examples_build/build.py              # 在 $CORE_REPO 下；全部
python tests/examples_build/build.py --only SDRAM  # 只挑一个库
```

### 静态检查一览（`P` 系列）

**不碰任何代码执行，看的是源码和文档本身。** `P1`/`P2`/`P3` 对应发版检查单的
`CHK-B1` / `CHK-B2` / `CHK-B3`，以前是人工核对。

| 编号 | 跑什么 | 查什么 | 在哪个自检里 |
|---|---|---|---|
| `P1` | `$TEST/tools/check_version_sync.py` | 固件版本号三处一致 | ✅ `$TEST` |
| `P2` | `$TEST/tools/check_mirror_sync.py` | 跨仓镜像（清单见 ARCHITECTURE.md「跨仓镜像的代码」） + RTC 备份寄存器占用 | ✅ `$TEST` |
| `P3` | `$CORE_REPO/tests/check_core_sync.py` | `$CORE_LIVE` 与 git 仓库一致 | ✅ `$CORE_REPO` |
| `P4` | `$CORE_REPO/tests/variant_check/build.py` | Arduino 变体头的编译期断言 | ✅ `$CORE_REPO` |
| `P5` | `$CORE_REPO/tests/examples_build/build.py` | 板卡包里每个能在这块板上编的 example 都编得过 | ⛔ 约 45 分钟，故意不进 |
| `P7` | `$PROD/tools/check_status_sync.py` | **三头对账**：需求表 ↔ 用例表 ↔ `selfcheck.py` 的 `CATALOG`。第三头 2026-09-21 才加 —— 在那之前，一个步骤可以每次都在跑却没有任何文档 | ✅ `$PROD` |
| `P8` | `$PROD/tools/check_doc_dupes.py` | 同一条主张没有写在两份文档里 | ✅ `$PROD` |
| `P9` | `$PROD/tools/check_doc_paths.py` | 文档里点名的每条路径都存在，链接的锚点和路径型链接文字也对得上 | ✅ `$PROD` |
| `P10` | `$TEST/tools/check_allow_hygiene.py` | 本机 `.claude/` 权限配置 | ⛔ 纯建议性，本机专属不进 git |
| `P11` | `$TEST/tools/check_tool_sync.py` | 板卡包里的 `IAPTool` 不落后于仓库 | ✅ `$TEST` |
| `P12` | `$PROD/tools/check_wayfinder_ticket_hygiene.py` + `check_no_orphan_placeholders.py` | 票关得诚不诚实、占位符有没有人认领 | ✅ `$PROD` |
| `P13` | `$PROD/tools/check_no_stale_ids.py` | 改过名的编号没有残留引用 | ✅ `$PROD` |
| `P14` | `$PROD/tools/check_changelist_has_no_orphans.py` | **没做完的活不许只活在某张图的 `CHANGE-LIST` 里** —— 每份 `CHANGE-LIST` 要有横幅说明未完成的块搬去了哪，且 `work/TODO.md` 里找得到 | ✅ `$PROD` |
| `P15` | `$CORE_REPO/tests/vector_alignment/build.py` | **app 的起始地址必须是 1024 的倍数**。正：当前 `build.flash_offset` 编得过；**反：传 `0x20200` 必须链接失败**，且错误里点名对齐。需要 arduino-cli | ✅ `$CORE_REPO` |
| `P16` | `$BOOT/tests/checks/check_icache_is_restored.py`（`ctest -R P16`） | **关掉 I-cache 之后，每条出口都要重新打开** —— `SCB_DisableICache()` 与 `SCB_EnableICache()` 之间不许有 `return`，且 `HAL_FLASH_Lock()` 要排在重开之前。跳转到 app 那一处显式豁免（跳走不回来） | ✅ `$BOOT` |
| `P17` | `$BOOT/tests/checks/check_cproject_ld.py`（`ctest -R P17`） | **`.cproject` 的链接脚本必须是 `${PLC_LD_SCRIPT}` 变量，不是写死的文件名** —— CubeMX 每次生成都会写死它，写死之后工装镜像编不出来。生成后的自动修在 `$BOOT/tools/restore_ld_script.bat`，这道检查兜它失效的情况。见 [../build/CUBEMX-RULES.md](../build/CUBEMX-RULES.md) | ✅ `$BOOT` |
| `P18` | `$PROD/tools/gen_id_map.py --check` | **`ID-MAP.md` 的现行编号表和各文档里真正定义的编号一致** —— 那张表由这个脚本扫出来写进去（决议 69），手改或者新增编号忘了重新生成，都会报红。修法：`python tools/gen_id_map.py --write` | ✅ `$PROD` |
| `P19` | `$CORE_REPO/tests/check_no_sector15_writes.py` | **core 里没有代码写扇区 15** —— 扫 `$CORE_REPO` 的 `cores/`、`libraries/`、`variants/`，见到 `0x081E0000`、`FLASH_SECTOR_7` 与 `FLASH_BANK_2` 同文件、或 `FLASH_SECTOR_TOTAL - 1` 就报红。扇区 15 只有 bootloader 能写，见 [BOOTLOADER-PROJECT-LAYOUT.md](../build/BOOTLOADER-PROJECT-LAYOUT.md)「Flash 分区」 | ✅ `$CORE_REPO` |
| `P20` | `$TEST/tools/check_golden_vectors.py` | `$BOOT` 提交的 `golden_vectors.h` 和出货 IAPTool 现在生成的同一结构 | ✅ `$TEST` |

⚠️ **这张表和 `$TOOL`、`$TEST` 两个 `selfcheck.py` 的 `CATALOG` 由 `P7` 对账**（2026-09-21 补的第三头）。
`P14` 曾经从这个缝里漏过去：它进了 `CATALOG`、每次都在跑，文档里却一个字都没有。
**新加一个步骤要同时动三处** —— `CATALOG`、这张表、以及模块文档里引用它的那条需求；
少一处 `P7` 就红。

### T2-06 · 已作废

决策 72 取消了公开根，这条告警和它的指纹常量一起删除，见 [M2 归属与信任](../modules/M2-ownership.md) 的用例表。

### P1 · 版本号三处一致

```
python tools/check_version_sync.py       # 在 $TEST 下
```

比对 bootloader（`Core/Inc/IAP_config.h` 的 `OPENPLC_FW_VERSION`）、Arduino core（`boards.txt` 的 `build.fw_version`）、`RELEASE-NOTES.md` 最新的版本标题——三处本来毫无关联，各改各的。对应发版检查单 **CHK-B1**。退出码：0 三处一致，1 有分叉，2 缺文件。

### P2 · 跨仓镜像没分叉

```
python tools/check_mirror_sync.py        # 在 $TEST 下
```

`$PROD/docs/repo/ARCHITECTURE.md` 列出的跨仓镜像代码，三个仓库没有共享构建系统，一侧改了另一侧不会报错，只会在运行时表现成不相关的症状。比的不是整份文件（C++ 侧有 `extern "C"`，两边 API 也不一样），是**每一项一个语义锚点**——只要求锚点一致。**没被检查覆盖的锚点会在输出末尾点名列出**，全绿不代表全覆盖。对应 **CHK-B2**。退出码：0 全部锚点一致，1 至少一处分叉，2 缺文件。

### P3 · core live 与 git 仓库一致

```
python tests/check_core_sync.py          # 在 $CORE_REPO 下
```

比对 Arduino IDE **真正加载**的那份（`$CORE_LIVE`）和板卡包的 git 版（`$CORE_REPO`）。方向天生单向：改动在 `$CORE_LIVE` 里做、验证、再拷回仓库提交——`$CORE_LIVE` 不进版本控制，验证过忘了拷回来，那段代码就只活在这台机器上，重装一次 IDE 就没了。六类刻意排除在比对之外：IDE 自己的安装元数据、Go 构建产物、编辑器备份、`.claude/`、`.vscode/`。**CRLF 与 LF 视为相同**：从网上装的包是 LF，仓库在 `core.autocrlf=true` 下检出是 CRLF，只差换行符不算差异。对应 **CHK-B3**。退出码：0 一致，1 有差异，2 仓库路径不对。

### P7 · 总表和用例名单不得漂

```
python tools/check_status_sync.py        # 在 $PROD 下；加 --list 只打印解析结果
```

`$PROD/docs/tables/STATUS.md` 和 `TEST-CASES.md` 里的用例编号必须是同一个集合。抓三类漏洞：STATUS.md 拿某条用例当证据、但 TEST-CASES.md 没定义它（需求指着一条谁都跑不了的用例）；TEST-CASES.md 定义了某条用例、但没有需求在引用它（一条跑出来的结果没人记录，烂了也没人发现）；某条用例引用的需求号 STATUS.md 里不存在。退出码：0 两边一致，1 有漂移，2 缺文件。

### P8 · 一个事实只能写在一个文件里

```
python tools/check_doc_dupes.py          # 在 $PROD 下；加 --min 40 只看更长的断言；--code 连代码块也列
```

把每份文档切成句子，去掉 markdown 加粗之类的强调符号（这样加粗过的一份能跟没加粗的一份对上），任何长到能算"断言"的句子出现在两个以上文件里就判失败。**指针（"见 X"）不算**——指针短且泛化，这正是修复重复的手段本身。**代码块单独报告、不计入失败**：抓下来的日志、命令这类东西合理地要在多处原样出现（发布说明要给客户看到他会看到的确切字符串，验收记录要写板子实际打了什么）——它们引的是那份 `.c` 文件，不是互相抄。退出码：0 没有断言重复，1 至少一处，2 环境问题。

#### P8 扫哪些文件

| 扫 | |
|---|---|
| 六个仓的 `CLAUDE.md` | bootloader / core / 工具 / 硬件 / 参考工程 / AI-Skills |
| `$BOOT/RELEASE-NOTES.md` | |
| `$PROD` 根的四份 | `CLAUDE.md` `README.md` `GLOSSARY.md` `WHERE-THINGS-LIVE.md` |
| `$PROD/docs/` 全部 | 递归 |
| `AI-Skills/OpenPLC` 和 `AI-Skills/_shared` | 站着的规矩 |

**`$PROD/maps/` 不扫。** 一张票的 `## Answer` 按设计就会摘述别处的结论，
两张图的 `Paused because:` 按约定就是同一句话 —— 纳进来这些全变成永久红灯。
实测数据：纳入会多 47 份文件、报 11 处重复，其中只有 2 处是真的。

⚠️ **一个 named 路径找不到文件时，这条检查现在直接失败**（退出码 2），不再静默跳过。
静默跳过让它从 2026-09-16 到 09-17 只扫 21 个文件、一份 `$PROD` 的文档都没扫，**却一直报 PASS**。

### P9 · 文档里提到的路径必须存在

```
python tools/check_doc_paths.py          # 在 $PROD 下；加 --list 打印它 resolve 出的每条路径
```

只检查三种能明确判断"相对谁"的写法：markdown 链接（相对当前文档）、`$BOOT`/`$TOOL`/`$CORE` 这类仓库变量路径、反引号包住的 `docs/`开头的路径（相对某个仓库根）。**故意不检查其余所有反引号路径**——一条不带仓库变量的裸路径意思是"相对这段话在讲哪个仓库"，检查脚本猜不出来。想让某条裸路径也被查到，就给它加上仓库变量前缀。路径里的行号（如 `fmc.c` 后面跟的行号范围）在检查前会被去掉——文件必须存在，行号只是提示，本来就会漂。另外两条（2026-09-24 起）：**链接带 `#锚点` 的，锚点必须是目标文件里某个标题按 GitHub 规则生成的锚点**；**链接文字本身写成一个路径的，文字里的文件名必须和链接目标一致**（防止目标改对了、文字还是旧路径）。链接文字是一句话的不查。

退出码：0 每条路径都能 resolve，1 至少一条断链，2 环境问题。

### P11 · 包里的 IAPTool 不能落后于仓库

```
python tools/check_tool_sync.py           # 在 $TEST 下；加 --list 连两份 usage 一起打
```

修法一条命令：在 `$TOOL` 下 `python tools/install_tool.py`（`compile_tool.sh` 末尾会自动跑它，所以正常情况下不用手动敲）。

**IDE 的 Upload 按钮跑的不是我们构建的那份 IAPTool**，而是板卡包里的副本（`$A15/packages/OpenPLC_Alpha/tools/STM32Tools/<版本>/<平台>/IAPTool`，`keys/` 也在它旁边）。所以客户手上那个二进制可以比这里所有用例测的那个落后几周，而没有任何东西会说话。比的不是哈希（同一份源码两次构建逐字节都不同，一个哭喊的检查等于没有检查），是**两个二进制自己报出来的子命令集合**：仓库有、包里没有的动词就是缺陷 —— 菜单到不了那个功能。退出码：0 包里能做到仓库能做的全部，1 落后了，2 有一份二进制不存在。

### P20 · 黄金向量和出货的 IAPTool 对得上

```
python tools/check_golden_vectors.py      # 在 $TEST 下
```

用出货的 IAPTool 在临时目录重新生成一份黄金向量，和 `$BOOT/tests/bootloader_unit/golden_vectors.h` 比；不一样就失败，并打出去 `$BOOT` 更新的命令，**不写 `$BOOT`**（「黄金向量由谁更新」那张票）。**只比结构**（12 个数组的长度和 5 个固定输入）：每次生成的密钥和签名都是随机的，没法逐字节比，所以证书长度变了抓得到、长度不变的格式变化抓不到。

### P10 · allow 列表不许攒字面命令

```
python tools/check_allow_hygiene.py                  # 每个仓库一行汇报
python tools/check_allow_hygiene.py --list            # 连被点名的条目也打出来
python tools/check_allow_hygiene.py --fail-over 400   # 超过这个数才算失败
```

`.claude/settings.local.json` 每次人批准一条"以后别再问"，就原样追加一行——没有任何东西会删。攒到某个点，`allow` 数组里全是再也不会命中第二次的一次性记录，而真正该有通用模式的仓库反而一条没有，每条命令都弹窗。

**这条不是发版门禁**——`settings.local.json` 本机专属、不进 git，不同机器天然不同，没法当"必须全绿"的检查。默认只打印、退出码 0；只有 `--fail-over` 指定阈值且真的超了才返回 1。**判据只看"像不像一次性"**（是否带绝对路径、是否带 `-First N` 这种烤进去的输出切片），会把一些合理的本机安装路径也点出来。

## 板上测试（`$TEST/onboard/`）

| 目录 | 是什么 | 怎么用 |
|---|---|---|
| `rs232/SerialPort/` | UART + USB-CDC 回显 sketch | 用 Arduino IDE/CLI 编译上传，往端子 C05/C06 发字符看回显 |
| `rs232/M5_SerialConflict/` | **T3-03**：`Serial4.begin()` 之后 `Serial_Test` 还能不能收 | 判据见模块文档的测试表 |
| `sdram/SDRAM_Acceptance/` | **T3-02**：`OpenPLC_SDRAM` 封装的 19 条断言 + 清零速率测量 | `python tools/run_sdram.py` |

### T3-02 · SDRAM 封装（需求 R3-03）

sketch 打 `RESULT <名字> PASS|FAIL` 和 `MEASURE <名字> <数>`，脚本按行判。**任何 FAIL、缺 `DONE`（说明跑一半挂了）、或一条 RESULT 都没有，都算失败。**

2026-08-17 实测：`begin()` 1.4 ms，清零 **91 MB/s**（清满 64MB ≈ 701 ms），`allocUninitialized()` 0 µs。

### T3-03 · 诊断串口不被用户 sketch 掐掉（需求 R3-05）

| 判据 | 前置条件 |
|---|---|
| sketch 调过 `Serial4.begin()` 之后，往端子发 5 个字节，`Serial_Test` **全部回显** | 板子在线、COM5 接在端子上、`$ARDUINO_CLI` 已配 |

## 板级端口 · RS485（`$BOOT/TestCase/RS485/rs485_test.c`）

跑在 **bootloader** 里，不是 app：`Core/Src/main.c` 的 `RS485_TEST_ENABLE` 置 1，`python tools/flash_bootloader.py` 编译烧写，然后 `python tools/rs485_echo.py --port <适配器口> --listen 8`。USART2 经 SP3485EN 出到端子。

**前置条件**：USB-RS485 适配器 A 接端子 A10（J11-3）、B 接 A11（J11-2）；日志看端子 C05/C06（UART4）。**必须有第二台设备在 A/B 上**：PD4 同时驱动 `/RE` 和 `DE`，板子听不见自己。

⚠️ **必须有第二台设备在 A/B 上。** PD4 同时驱动 `/RE` 和 `DE`（同一条网），发的时候收就是关的，**板子听不见自己** —— 没有适配器时 R2/R4 一条都判不了。

| 编号 | 判据 | 不接线能不能判 |
|---|---|---|
| R1 | PD4 / PD5 当普通 GPIO 推 0 和 1，读回来一致 | ✅ 能，专门用来分开"没接线"和"这个脚是死的" |
| R2 | 适配器上每 **3 s** 收到一帧 `RS485 HELLO <n>` | ❌ 要适配器 |
| R4 | 主机发一串探针，板子原样发回；同时在日志口打出 **ASCII + hex** 两列 | ❌ 要适配器 |

## T1-21 / T1-22 · 掉电中断，怎么跑

```bash
python3 tools/run_s4.py --case a --bin <app.bin> --pad-to 1835008 --retry 3
python3 tools/run_s4.py --case b --bin <app.bin> --pad-to 1835008 --retry 3
```

⚠️ **`--pad-to` 两条都要，而且要补到 app 区上限 1835008。** 不补零时窗口只有几秒，
人抓不住；补满之后传输窗口约 34 秒、擦写窗口约 20 秒。**旧写法给 `T1-21` 写 1200000、
给 `T1-22` 完全不写，两个都不够** —— 脚本自己的文件头就写着 1200000 对擦写窗口太短。
2026-09-18 实测：补到 1835008，`T1-21` 一次命中，`T1-22` 第三次命中。

| | |
|---|---|
| **判据 T1-21** | 传输窗口内断电 → 重新上电后**旧 app 照常启动**（日志出现 `APP Mod`，且**没有** `App signature invalid or absent`）|
| **判据 T1-22** | 擦写窗口内断电 → 上电报 `App signature invalid or absent`，**且重传一次能恢复** |
| **窗口锚点** | `Staging in SDRAM` 之后 / `Erasing application region` 之前 = T1-21；`Erasing application region` 之后 = T1-22。字符串对齐 `open_plc_cube_ide/IAPServer/IAP_server.c` |

## T1-27 · 按住 BOOT0 强制进上传模式，怎么跑

```bash
python3 tools/run_boot0_upload_mode.py --ports COM5
```

脚本只捕获日志并判定，**一次复位都不发**。整个手势由人做：

1. 按一下复位键并松开
2. **一看到系统指示灯快闪就按住 BOOT0**
3. 灯停了再按约两秒，然后松开

| | |
|---|---|
| **判据** | 日志同时出现 `** UPLOAD Mod ... (BOOT0 held)` 和 `** Reset cause: PIN` |
| **为什么复位不能由 ST-Link 驱动** | BOOT0 是**启动模式引脚**。按住它的时候复位，芯片去启动 ST 自带的 DFU，我们的 bootloader 根本不执行 —— 串口全程静默，USB 上出现 `DFU in FS Mode`，要等下一次「BOOT0 为低」的复位才退出。2026-09-18 这么试了 11 次，每次都报「没按」，而板子其实在 DFU 里 |
| **为什么用指示灯当信号** | `Core/Src/main.c` 的 `boot_window()` 让系统指示灯快闪 2 秒，**灯闪的那 2 秒就是窗口本身**；开机不动任何继电器（决策 71）。PC 这边看不见它。⚠️ **期间根本不看 BOOT0**，只在 2 秒那一刻读一次 |
| ⛔ **破坏性** | 长按超过 10 秒会**武装恢复出厂，松手就执行**。而这条用例需要长按，两者分不开。**在已认领的板子上跑会抹掉 owner 密钥** |

## T1-28 · metadata 区满了能回收，怎么跑

```bash
python3 tools/run_journal_reclaim.py --bin <app.bin>
python3 tools/run_journal_reclaim.py --inspect     # 只读，报告当前槽数
```

| | |
|---|---|
| **判据** | 灌满后板子报 `** Metadata area full - the next successful update reclaims sector 15. **`；一次上传后日志出现 `Reclaiming sector 15 (<n> metadata slots, root area compacted)`；**且板子照常启动 app**。⚠️ **校准值区那 8 KiB 必须原样还在** —— reclaim 擦的是整个扇区 |
| **为什么不能靠反复上传灌满** | 一次上传只占 7 槽，3583 槽要 511 次上传、大半天 |
| **为什么必须整片读回来再整片写回去** | 扇区里存着当前 app 的 metadata（签名和证书**伪造不了**）**以及校准值**，而 `STM32_Programmer_CLI` 写之前会擦整个扇区 |
| **留的空槽必须少于 7** | 回收只发生在写 metadata 的那一刻，而一条 metadata 占 7 槽 |

## 五条用户路径 · 从出厂态跑一整轮

**这一节是整轮的剧本**，按[决策 72](../tables/DECISIONS.md)（出厂无根、第一次上传自动认领）写。
单条用例各自能跑，但客户是沿着一条路径走下来的，**顺序本身就是被测对象**：
② 的恢复出厂只有在 ① 真的认领过之后才有意义，⑤ 的证书由 ④ 换上的那把根签发。

| | 路径 |
|---|---|
| ① | 出厂板经 USB 第一次上传，自动认领 |
| ② | 恢复出厂回到没有根，下一次经网口上传再自动认领 |
| ③ | 已认领的板子经网口继续上传，并升级 |
| ④ | `setowner` 换根：旧根被拒，新根能传 |
| ⑤ | 根持有者给同事签叶证书，同事用自己的私钥上传 |

> ⚠️ **整轮只要人到板子跟前 1 次**：路径 ② 复位后按住 BOOT0 超过 10 秒。放在 ② 是为了把唯一的动手步骤提到最前面，之后全部无人值守。
> 回到出厂态走 ST-Link，不用人按；路径 ① 要一根接到板子 USB 口的线。

⚠️ **2026-09-22 那一轮整轮通过记的是决策 72 之前的规则**（公开根、按 BOOT0 认领、`rotate_keys.sh`）。**这份新剧本还没上板跑过。**

### 怎么跑

```bash
python3 tools/run_five_paths.py --elf <boot.elf> --cdc <COM口>   # 整轮
python3 tools/run_five_paths.py --dry-run                         # 只打印计划，什么都不碰
python3 tools/run_five_paths.py --from 3 --owner-key <owner.pem>  # 从路径 ③ 续跑
python3 tools/run_five_paths.py --only 1 2                        # 只跑这几条
```

⚠️ **破坏性**：整片擦除（校准值先读出再写回）、前后认领两次。
⚠️ **`$BOOT/Debug/` 可能是工装镜像**（`PORTTOOL_ENABLE=1`），所以用 `--elf` 指定 bootloader；脚本见到工装镜像会拒绝烧。
⚠️ **上板前先用当前 core 重编 `Output/probe-images/` 里的两个探针镜像** —— 旧镜像里的 `owner_root_ro.c` 读的是旧地址。

自动认领时脚本把 IAPTool 的用户配置目录挪进 `--keydir`，生成的私钥落在那里，**本机真正的私钥不会被读到或覆盖**。

**某一步没过就停**，不往下跑：后面每一步都建立在前一步留下的状态上。

### 步骤与判据

| 步 | 做什么 | 判据 | 用例 | 要人吗 |
|---|---|---|---|---|
| 0 | 造出厂态 | 见下「出厂态怎么造、怎么证明」 | — | — |
| **①** | 经 USB 上传 v1，本机没有私钥 | IAPTool 打出 `This board has no root yet` 和 `Claimed.`，私钥生成在它打印的路径下且文件存在；v1 起来 | `T2-35` | — |
| **②-a** | 复位后按住 BOOT0 超过 10 秒 | 板子打 `FACTORY RESET DONE` | `T2-05` | ✋ **唯一一次** |
| ②-b | 普通复位 | ① 装的 app 不再启动（`App signature invalid or absent`，没有 `APP Mod`），`getpubkey` 回 `none` | `T2-09` | — |
| ②-c | 经网口上传 v1，换一个空的配置目录 | 同 ①，经以太网；认领的私钥和 ① 那把不同 | `T2-36` | — |
| ③-a | 拿另一把密钥 `takeown` | `Refused`，`getpubkey` 一字节不变 | `T2-02` | — |
| ③-b | 用 owner 私钥经网口上传 v2 | 版本串 v1 → v2 | — | — |
| ④-a | 坏签名 `setowner` | 被拒，什么都没变 | `T2-03` 负向 | — |
| ④-b | 正确签名 `setowner` 换到新根 | `OK`，generation +1 | `T2-03` 正向 | — |
| ④-c | 用旧根签的镜像上传 | 被拒，app 区一字节未动 | `T2-10` | — |
| ④-d | 用新根签的镜像上传 | 装上并启动 | — | — |
| **⑤** | 新根给同事签叶证书，同事用自己的私钥上传 | 上传成功并启动 | `T2-11` | — |

**三条贯穿全表的原则**：反向用例必须配正向对照；判据不能只看「某行日志没出现」；结果问板子要，不问工具要。

⚠️ **按叶点名作废不在这一轮**，归 `T2-15`–`T2-20`；④ 测的是「换根让旧根失效」。

### 出厂态怎么造、怎么证明

```bash
python3 tools/reset_board_to_factory_state.py --elf <boot.elf>  # 擦除 + 烧 bootloader + 写回校准值 + 验证
python3 tools/reset_board_to_factory_state.py --check-only      # 只验证，绝不写
```

**判据要两类证据，缺一不判 PASS** —— 一类读 flash（走 SWD），一类读串口，互不经过对方：

| 类别 | 判据 |
|---|---|
| 读 flash | 根区 `0x081E2000` 起 8 KiB 全 `0xFF` |
| 读 flash | app 区 `0x08020000` 起 256 字节全 `0xFF`；metadata 区 `0x081E4000` 起 256 字节全 `0xFF` |
| 读 flash | 校准值区和擦除前逐字节相同；`0x081FFFE0` 有 bootloader 第一次启动写的布局标记 |
| 启动日志 | `Owner slot: empty - no root` |
| 启动日志 | `Bootloader state: 0/… metadata slots used, metadata absent` |

⚠️ **「擦完先单独验一次」不能省** —— 烧在一次失败的擦除上面的 bootloader 照样能启动、照样打出所有正确的行。
⚠️ **日志一个字都没抓到时报 INCONCLUSIVE，不报 PASS。**

### 升级要怎么观察

「升级」要看见的是「装上去的东西真的换了」，所以要两个可区分的镜像：`Output/probe-images/iap_probe_v1.bin` 和 `iap_probe_v2.bin`，
启动时打不同的版本串，判据是日志里那个串从 v1 变成 v2。

### 这一轮测不到什么

| 测不到 | 为什么 |
|---|---|
| 两块板的 MAC 是否真的不同 | 手上只有一块板 |
| 掉电中断 | 归 `T1-21`/`T1-22`；扇区 15 回收中途断电归 `T2-34`（主机）和上板断电那一项 |
| 精确作废单张叶证书 | 归 `T2-15`–`T2-20` |

## 未覆盖

## R1-31 · 备份域失效能被发现：已实地验证，没有脚本

**没有专门的脚本，也不打算写** —— 2026-09-19 排查 `T1-17` 时正负两个方向都真实触发过，
证据比脚本更硬。判据在 `$BOOT/IAPServer/iap_auth.c` 的 `iap_auth_report_backup_domain()`。

| 方向 | 怎么出现的 | bootloader 打的 |
|---|---|---|
| 域丢了 | witness 写进去之后被 app 清掉（当时两边 RTC 时钟源不一致） | `** Backup domain was lost ... **` + `The RTC has restarted from a fixed time.` |
| 域还在 | 时钟源统一之后 | `Backup domain retained` |

⚠️ **这两行 2026-09-24 起不再提重放保护**（决议 66：nonce 改由 TRNG 出，不再住备份域）。
丢了域影响的是 RTC 走时，**不影响上传能不能通过认证**。

⚠️ **要再现得自己制造一次备份域丢失。** core 自带 `resetBackupDomain()`
（`$CORE_REPO/cores/arduino/stm32/backup.h`）能清整个域，不必拆电池。

**完整的覆盖矩阵和每条待补用例的设计骨架在 [docs/STATUS.md](../tables/STATUS.md)**，这里只留摘要：

| ID | 内容 | 为什么还没做 |
|---|---|---|
