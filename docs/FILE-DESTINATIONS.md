# 逐份文件的去向

**三个仓的全部 43 份 `.md`，一份一行。** 定于 2026-09-16，由
`maps/docs-migration/issues/MIG-03-file-by-file-destination.md` 这张票敲定。

分类依据见 [REFERENCE-LAYER-TAXONOMY.md](REFERENCE-LAYER-TAXONOMY.md)。
**43 行全部定死，没有 ⏸。** 去处的定义见 [../WHERE-THINGS-LIVE.md](../WHERE-THINGS-LIVE.md)。

| 现在在哪 | 去哪 | 备注 |
|---|---|---|
| `open_plc_cube_ide/docs/design/HARDWARE-FACTS.md` | docs/hardware/HARDWARE-FACTS.md |  |
| `open_plc_cube_ide/docs/design/JOURNAL.md` | docs/boot/JOURNAL.md |  |
| `open_plc_cube_ide/docs/design/OWNERSHIP.md` | docs/security/OWNERSHIP.md | 同目录的 security-design.html 一起搬 |
| `open_plc_cube_ide/docs/design/KEYS.md` | docs/security/KEYS.md |  |
| `open_plc_cube_ide/docs/design/PORTTOOL-FLOW.md` | docs/production/PORTTOOL-FLOW.md |  |
| `open_plc_cube_ide/docs/design/PRODUCTION-FRAMEWORK.md` | docs/production/PRODUCTION-FRAMEWORK.md |  |
| `open_plc_cube_ide/docs/test/PROD-CONFIG-ITEMS.md` | docs/production/PROD-CONFIG-ITEMS.md |  |
| `open_plc_cube_ide/docs/test/BOARD-BRINGUP-CASES.md` | docs/production/BOARD-BRINGUP-CASES.md |  |
| `open_plc_cube_ide/docs/design/CUBEMX-RULES.md` | docs/build/CUBEMX-RULES.md |  |
| `open_plc_cube_ide/docs/design/RTC-LSE-CHANGE.md` | docs/build/RTC-LSE-CHANGE.md |  |
| `open_plc_cube_ide/OpenPLC_Bootloader.md` | docs/build/BOOTLOADER-PROJECT-LAYOUT.md | 改名已批准：文件名要说出内容 |
| `AI-Skills/OpenPLC/docs/test/BUILD-AND-TEST.md` | docs/build/BUILD-AND-TEST.md |  |
| `AI-Skills/OpenPLC/docs/design/ARCHITECTURE.md` | docs/repo/ARCHITECTURE.md |  |
| `AI-Skills/OpenPLC/docs/CONVENTIONS.md` | docs/repo/CONVENTIONS.md |  |
| `AI-Skills/OpenPLC/docs/design/CONSTRAINTS.md` | docs/repo/CONSTRAINTS.md |  |
| `open_plc_cube_ide/docs/design/FIXTURE-INTERFACE.md` | docs/outbound/FIXTURE-INTERFACE.md |  |
| `open_plc_cube_ide/docs/test/AIN-JUMPER-REQUEST.md` | docs/outbound/AIN-JUMPER-REQUEST.md |  |
| `open_plc_cube_ide/docs/test/PROD-DOC-REVIEW.md` | docs/outbound/PROD-DOC-REVIEW.md |  |
| `open_plc_cube_ide/docs/design/DECISIONS.md` | docs/tables/DECISIONS.md | 48 条编号一个不动 |
| `open_plc_cube_ide/docs/design/DEFERRED-DESIGNS.md` | docs/tables/DEFERRED-DESIGNS.md |  |
| `IAPTranfer_Tool/TestCase/TEST-CASES.md` | docs/tables/TEST-CASES.md | 编号写死在 Go 代码里，不能改 |
| `IAPTranfer_Tool/TestCase/acceptance/checklist.md` | docs/tables/ACCEPTANCE-CHECKLIST.md | 改名已批准 |
| `AI-Skills/OpenPLC/docs/ID-MAP.md` | docs/tables/ID-MAP.md | 要加一行登记 MIG- 前缀 |
| `AI-Skills/OpenPLC/docs/STATUS.md` | docs/tables/REQUIREMENTS.md（需求那 53 条） | 「最近结果 / 证据日期」两列**原样留在原仓不动** —— 生成器还不存在，现在删掉等于丢掉已有记录 |
| `open_plc_cube_ide/RELEASE-NOTES.md` | 留在原仓 | 对外、英文、自成一体，跟着版本走 |
| `open_plc_cube_ide/CLAUDE.md` | 留在原仓（入口） | 内容改写是另一张票 |
| `open_plc_arduino/CLAUDE.md` | 留在原仓（入口） | 同上 |
| `IAPTranfer_Tool/CLAUDE.md` | 留在原仓（入口） | 同上 |
| `open_plc_cube_ide/README.md` | 留在原仓（门面） |  |
| `IAPTranfer_Tool/README.md` | 留在原仓（门面） |  |
| `open_plc_cube_ide/docs/design/PRODUCTION-TEST-GAP.md` | 转成票 | 「要什么/有什么」的差距 → 一张图 |
| `open_plc_cube_ide/docs/test/PORT-BRINGUP-PLAN.md` | 进 `work/` | 每个端口卡在哪 = 工作项 |
| `open_plc_cube_ide/docs/test/PORTTOOL-FIRST-BENCH.md` | 进 `waiting/` | 「只有真硬件能回答的问题」= 等外部条件 |
| `open_plc_cube_ide/docs/test/DO-PWM-SCOPE-STEPS.md` | 进 `waiting/` | 等示波器实测；VNQ5160K-E 的 PWM 上限无数据手册可查 |
| `open_plc_cube_ide/docs/work/ISSUES.md` | **拆开分流** | 6 条逐条分流：B1/C1 转票、B2 进 `waiting/`、A3/D1/D2 进 `work/`。文件删掉 |
| `open_plc_cube_ide/docs/work/BACKLOG.md` | **删** | 唯一一条（C12 等真实需求）进迷雾。见 `WHERE-THINGS-LIVE.md` |
| `IAPTranfer_Tool/TestCase/host/bootloader_unit/HOST-C-TESTS.md` | 留在原地 | 它描述的就是所在目录，`docs/build/` 放指针 |
| `IAPTranfer_Tool/TestCase/host/crypto_ref/CROSS-CHECK.md` | 留在原地 | 同上，`docs/security/` 放指针 |
| `IAPTranfer_Tool/TestCase/host/fakeboard/KEY-MATCH.md` | 留在原地 | 同上，`docs/security/` 放指针 |
| `IAPTranfer_Tool/TestCase/host/porttool_caps/PORTTOOL-CAPS-TEST.md` | 留在原地 | 同上，`docs/production/` 放指针 |
| `open_plc_cube_ide/docs/INDEX.md` | **删** | 搬完目录结构就回答了「去哪查」，留着是第二份会漂的地图。git 里取得回来 |
| `AI-Skills/OpenPLC/docs/OVERVIEW.md` | **删** | 同上，由本仓 `README.md` 取代 |
| `AI-Skills/OpenPLC/docs/process/WRAP-UP.md` | docs/repo/WRAP-UP.md（逐条对后的剩余） | 被新关票流程接管的条目删掉并指过去；「不要假设用户要推送」这类新框架里没有位置的**必须保留** |

**合计 43 行。** 覆盖三个仓全部 `.md`，没有一份没被提到。
