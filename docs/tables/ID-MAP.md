# 编号登记表：哪个编号住在哪

**说到任何编号，在同一句话里给出这里的路径。** 2026-08-22 建。

**为什么需要这份文件**：清点时发现全项目有 **13 套编号**在混用，其中 `A1` 同时是四样东西 ——「USB CDC 能烧写」（需求）、「go test」（selfcheck 第 1 步）、「主机侧 Go 测试」（验收单第 1 项）、「已修的版本号问题」（待办）。**说"A7 过了"字面上有四个意思。**

2026-08-22 消掉了三套：**selfcheck 的步骤号整套删除**（每一步本来就只是某个用例的别名）、待办加 `ISS-` 前缀、验收单加 `CHK-` 前缀。**还剩 10 套，两两不撞。** 2026-09-16 加了第 11 套：wayfinder 的票号（见下表首行）。

---

## 现在有效的编号

⚠️ **2026-09-17 起这张表是混的。** 13 个写死在 Go 里的用例号已经重排成 `T1-xx`
（票：`$PROD/maps/docs-restructure/issues/DR-03-renumber-hardcoded-go-case-ids.md`），
**静态检查号（`P1`–`P13`）不参与重排** —— 它们属于工程约束层。其余用例号（
`M3` `EV1` `H3`）保持原样：前两个 ⛔ 不做，`H3`（`go vet`）是卫生检查不是需求证据。**其余全部重排完毕**，对照见 `$PROD/maps/docs-restructure/DR-02-test-id-mapping.md`。


| 编号形态 | 是什么 | 定义在哪 | 谁实现 | 结果记在哪 |
|---|---|---|---|---|
| `A1`–`A7` `B1`–`B11` `C1`–`C14` `D1`–`D9` `E1`–`E8` `F1`–`F6` | **产品需求**（54 条，每条一句可判定的话。⚠️ **`C6` 不存在**，`C` 组实际 13 条） | [STATUS.md](STATUS.md) 第三节 | — 它们是主张，不是可执行的东西 | 同一张表的「状态」列 |
| `T1-06`–`T1-10` | **TCP 会话用例** | `$PROD/docs/engineering/HOW-TO-RUN-TESTS.md` | `$TOOL:TestCase/tcp_session.go`（`register(testCase{id:"T1-07"…})` —— 编号写死在 Go 代码里，**改它就要同时改代码、脚本和文档**） | [STATUS.md](STATUS.md) 的「最近结果」列 |
| `T1-01`–`T1-05` | **UDP 发现用例** | `$PROD/docs/engineering/HOW-TO-RUN-TESTS.md` | `$TOOL:TestCase/udp_discovery.go` | [STATUS.md](STATUS.md) 的「最近结果」列 |
| `T1-11` `T1-12` `T1-13` `T1-21` `T1-22` `T1-14` | **签名 / 掉电 / staging 用例** | `$PROD/docs/engineering/HOW-TO-RUN-TESTS.md` | T1-11/T1-12 → `signature.go` + `signature_wrongkey.go`；T1-13 → `python tools/run_s3.py`；**T1-21/T1-22 → `tools/run_s4.py`**；T1-14 → `python tools/run_case.py --case T1-11 --then-reset` | [STATUS.md](STATUS.md) 的「最近结果」列 |
| `T2-01` `T2-02` `T2-03` `T2-04` `T2-05` | **所有权用例** | `$PROD/docs/engineering/HOW-TO-RUN-TESTS.md` | `python tools/run_takeown.py`、`run_setowner.py`、`inject_owner_record.py` | [STATUS.md](STATUS.md) 的「最近结果」列 |
| `T1-17` | **nonce 跨掉电不重复** | `$PROD/docs/engineering/HOW-TO-RUN-TESTS.md` | `$TOOL:TestCase/nonce_replay.go`，由 `python tools/run_au1.py` 编排 | [STATUS.md](STATUS.md) 的「最近结果」列 |
| `T1-15` `T1-16` `H3` `T1-18a`–`T1-18g` `T1-19` `T1-20` | **主机侧用例**（不需要板子） | `$PROD/docs/engineering/HOW-TO-RUN-TESTS.md` | T1-15 → `go test ./TestCase/...`；**H3（不重排，卫生检查）→ `go vet ./...`（2026-08-22 新建）**；T1-16 → `host/bootloader_unit/build.py`；T1-18a–T1-18g → `host/fakeboard/run_cases.py`；T1-19/T1-20 → `host/crypto_ref/run_checks.py` | [STATUS.md](STATUS.md) 的「最近结果」列 |
| `MIG-NN` `PTG-NN` | **wayfinder 的票**，一张票一个待决的问题。前缀就是它所属那张图 | `$PROD/maps/<图>/issues/` 一张票一个文件 | — 它们是问题，不是测试 | 票自己的 `## Answer`，图的 `Decisions so far` 只放一行摘要 |
| `P1`–`P11` | **静态检查**（P1–P6 看代码，P7–P9 看文档，**P10 看本机 `.claude/` 权限配置，纯建议性、不进 selfcheck**——那份文件本机专属不进 git，不能当发版门禁）| `$PROD/docs/engineering/HOW-TO-RUN-TESTS.md` | `tools/check_version_sync.py`(P1)、`check_mirror_sync.py`(P2)、`check_core_sync.py`(P3)、`host/variant_check/build.py`(P4)、`host/examples_build/build.py`(P5)、`check_public_root.py`(P6)、`check_status_sync.py`(P7)、`check_doc_dupes.py`(P8)、`check_doc_paths.py`(P9)、`check_allow_hygiene.py`(P10)、`$PROD/tools/check_wayfinder_ticket_hygiene.py` 与 `check_no_orphan_placeholders.py`(P12) | [STATUS.md](STATUS.md) 的「最近结果」列 |
| `T3-01` | **启动门禁**（SDRAM 自检 + 日志口通不通） | `$PROD/docs/tables/ACCEPTANCE-CHECKLIST.md` 的「T3-01 · 启动门禁」节 | `tools/flash_bootloader.py` 判读；日志文案在 `Core/Src/fmc.c` | [STATUS.md](STATUS.md) 的「最近结果」列 |
| `T3-02` `M3` `T3-03` `T3-04` `EV1` | **零散的板级用例** | `$PROD/docs/engineering/HOW-TO-RUN-TESTS.md` | T3-02 → `onboard/sdram/`，由 `tools/run_sdram.py` 跑；M3 要第二块板；T3-03 → `onboard/`；T3-04 → `onboard/rs232/SerialPort`；EV1 ⛔ 难以构造 | [STATUS.md](STATUS.md) 的「最近结果」列 |
| `CHK-A1`–`A7` `CHK-B1`–`B7` `CHK-C1`–`C7` | **三张验收单**（改动后自检 / 发版 / 单板出厂） | `$PROD/docs/tables/ACCEPTANCE-CHECKLIST.md` | 大部分是"跑某条命令"或人工 | ⬜ **还没有去处**，由 `PTG-01` 回答（`$PROD/maps/production-test-gap/issues/PTG-01-where-do-per-board-records-go.md`）。F2 因此一直是 🟡 |
| ~~`ISS-*`~~ | **2026-09-16 整套废除。** 「已知问题」不是一类东西 —— 拆进了票 / `$PROD/work/TODO.md` / `$PROD/waiting/WAITING-ON.md`，各有各的关闭条件 | — | — | — |
| ~~`M1`–`M8`~~ | **2026-09-16 整套废除。** 八个模块全部完成；待立项而没有真实需求的进图的迷雾 | — | — | — |

---

## 2026-08-22 删掉了什么

### selfcheck 的 `A0`–`A14`（整套删除）

12 步每一步都只是某个用例的别名。改成用例号本身之后，**一整套编号消失，`A1`/`A2`/`A3`/`A7` 的四义歧义少掉一个来源**。

| 旧步骤号 | 现在叫 | 跑的是什么 |
|---|---|---|
| `A0` | `ENV` | 这台机器有哪些工具链（不是用例，是探测） |
| `A1` | **`T1-15`** | `go test ./TestCase/...` |
| `A2` | **`T1-16`** | 主机侧 C 单测（真实 `sha256.c` / `iap_keyderive.c` / `iap_auth.c`） |
| `A3` | **`H3`** ← **新建的编号** | `go vet ./...` |
| `A7` | **`P1`** | 版本号三处一致 |
| `A8` | **`P2`** | 跨仓镜像没分叉 |
| `A9` | **`P3`** | core live 与 git 一致 |
| `A10` | **`T1-18a`–`T1-18g`** | IAPTool 传输前的密钥匹配决策 |
| `A11` | **`T1-19` `T1-20`** | 加密交叉验证 |
| `A13` | **`P4`** | Arduino 变体的 FMC 保留脚断言 |
| `A14` | **`P6`** | 公开根指纹 |
| `A4` `A5` `A6` | — | **从来不存在。** 对话里说的 "A4/A5" 一般指验收单的 `CHK-A4`（构建）/ `CHK-A5`（烧写） |
| `A15` | — | **不是步骤号。** 那是配置变量 `$A15` / `A15_DIR`（Arduino15 数据目录），在 `tools/common.py` / `tools/common.py` 里 |

★ **顺带补掉一个真实缺口**：`A1`（go test）和 `A3`（go vet）此前**映射不到任何用例号，所以它们的结果从来没有被写进任何文件**。给 `go vet` 建了 `H3` 之后，每一步在 [STATUS.md](STATUS.md) 里都有行。

同日又新增三步：**`P7`**（总表和用例不得漂移）、**`P8`**（一个事实只能写在一个文件里）、**`P9`**（文档里提到的路径必须存在）。**它们看的是文档，不是固件** —— 因为 2026-08-22 证明了这两类漂移靠眼睛找不出来。

### `T0` → `BG1`（该编号 2026-09-17 再次改名为 `T3-01`）

`T0` 不属于 `T1-06`–`T1-10` 那一系列：它在另一个仓库、另一个文件、另一种性质（启动门禁不是设备行为用例），`TEST-CASES.md` 里根本没有 `T0` 这一条。

改名之后，提交信息里"T0 fails"这种话不再和 T 系列混淆。**`Core/Src/fmc.c` 的日志文案没动** —— 那是日志不是编号。

### 待办和验收单加前缀

- 原来 docs/TODO.md 里的裸 `A1`/`B4`/`C2` → 曾改成 `ISS-A3`/`ISS-B4`/…，**2026-09-16 连 `ISS-` 一起废除**。旧提交信息里的这些编号只能当历史读。
- 验收单（现 `ACCEPTANCE-CHECKLIST.md`）的三张表 → `CHK-A*`/`CHK-B*`/`CHK-C*`。

---

## 还剩的三处会看错的地方

**这三处不是 bug，是同一个字母数字在不同层次上的合理重用。列在这里，看到时不用重新推。**

| 看到 | 可能是 | 怎么分辨 |
|---|---|---|
| **`M3`** | ① **用例**：两块板的 MAC 不同<br>② **设计模块**：app 侧 SDRAM 库 | 上下文提"MAC"或"第二块板"→ 用例；提"SDRAM 库"或"链接脚本"→ 模块。两者不相关 |
| **`T3-03`** | ① **用例**：`Serial_Test` 抗 `Serial4.begin()`<br>② **设计模块**：串口冲突 | **两者是同一个主题**，不会导致误解 |
| **`D1`** | ① **需求**：journal metadata 一次升级 5 槽<br>② **原已知问题** `ISS-D1`（编号已废除）：限流是固定窗口<br>③ **硬件网络名**：SDRAM 的第 1 根数据线（`PD15`） | ③ 是最常出现的那个。提"线""`PD15`""SDRAM"→ 硬件网络。⚠️ `D0`–`D15` 整套都是网络名 |

`CHK-B1`/`CHK-B2`/`CHK-B3` 和 `P1`/`P2`/`P3` **是同一批检查的两个名字**（`TEST-CASES.md` 明说了"前三个对应发版检查单的 B1/B2/B3"）。**没有合并** —— 按 `$PROD/docs/repo/CONVENTIONS.md` 的「不要擅自 dedup 或删除」，这个要单独问过再动。

---

## 加新编号的规矩

1. **先看这张表有没有撞。** 撞了就换一个前缀，不要"反正上下文能分清"。
2. **改编号是可以的，但要一次改全。** 用例号写死在 Go 代码和脚本里，需求号被用例引用 —— 2026-09-17 重排 13 个用例号时，代码、脚本、三张表一起改，判据是 `selfcheck` 的 P7 仍然通过。
3. **新起一套编号之前先问：它能不能就用现有某一套？** selfcheck 原来那套步骤号就是没问这句话的后果 —— 一整套编号，零信息量，一个四义歧义。
4. **加完回来更新这张表。**

## 提编号就给路径

**通用那一条规则不在这里**，在 `AI-Skills/_shared/rules/cite-the-path.md`，它会作为用户级 rule 在每个项目里加载。这里只答本项目的那一半：**哪类编号在哪个文件。**

> ⚠️ **完整的登记表在 `$PROD/docs/tables/ID-MAP.md`** —— 10 套编号，每套定义在哪、谁实现、结果记在哪。下面这张只是最常用的四类，**不要在这里加第二份清单**。

| 编号 | 去哪查 |
|---|---|
| 需求 A1–A7 B1–B11 C1–C14 D1–D9 E1–E8 F1–F5 | `$PROD/docs/tables/STATUS.md` —— 连同用例、状态、最近结果 |
| 用例的判据和怎么跑 | `$PROD/docs/engineering/HOW-TO-RUN-TESTS.md`（跨仓，贴着代码走） |
| 待办、在等什么 | `$PROD/work/TODO.md`、`$PROD/waiting/WAITING-ON.md` |
| 待决的问题 | `$PROD/maps/<图>/issues/` |

实现在哪：`T1-01`–`T1-17`（M1 的用例）→ `TestCase/*.go`；K → `TestCase/host/fakeboard/`；H2 → `TestCase/host/bootloader_unit/`；X → `TestCase/host/crypto_ref/`；P → `TestCase/tools/check_*`。
