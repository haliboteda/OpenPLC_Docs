# 每一项现有测试归哪一层、哪个仓 —— 归属表

「[每一项现有测试归哪一层、哪个仓](issues/TA-01-which-layer-and-repo-does-each-test-belong-to.md)」那张票的产物。范围是 [map.md](map.md)「全集」那条命令的输出，由 [`tools/classify_tests_by_layer.py`](../../tools/classify_tests_by_layer.py) 生成，2026-10-02 跑出 **330** 个文件，下表也是 330 行。
判据：[决策 78](../../docs/tables/DECISIONS.md)，跑它需要几个仓。

## 汇总

| 去处 | 文件数 |
|---|---|
| `$BOOT` 部件测试 | 26 |
| `$TOOL` 部件测试 | 12 |
| `$CORE_REPO` 部件测试 | 12 |
| `$PORTTOOL` 部件测试 | 41 |
| `$TEST` 契约测试 | 5 |
| `$TEST` 整机测试 | 28 |
| `$TEST` 测试基础设施 | 19 |
| `$PROD` 文档检查 | 8 |
| 待定：只用一个仓但要上真板子（交给「只需要一个仓、但必须上真板子的测试归哪」） | 5 |
| 待定：部件测试和整机测试共用的替身（交给「IAPTool 测试用的假板子」） | 2 |
| 待定：不测产品，查各仓的 `.claude` 权限文件（交给「文档检查搬进 OpenPLC_Docs 后长什么样」） | 1 |
| `$PORTTOOL` 自己的测试基础设施（留不留交给「部件仓要不要本机配置」） | 3 |
| 不是测试：`$TOOL` 的发版工具 | 1 |
| 不是测试：`$PORTTOOL` 的产品数据或发版工具 | 6 |
| 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 93 |
| 上游第三方代码自带的，不属于本产品，不动 | 68 |

## 逐个文件

| 文件 | 去处 | 依据 |
|---|---|---|
| `IAPTranfer_Tool/TestCase/acceptance/2026-09-18-boot-iap-full-run.md` | `$TEST` 整机测试 | 一轮整机上板验收的记录 |
| `IAPTranfer_Tool/TestCase/host/bootloader_unit/HOST-C-TESTS.md` | `$BOOT` 部件测试 | T1-16：编 `$BOOT` 的真实源码，黄金向量已提交，跑时只用 `$BOOT` |
| `IAPTranfer_Tool/TestCase/host/bootloader_unit/build.py` | `$BOOT` 部件测试 | T1-16：编 `$BOOT` 的真实源码，黄金向量已提交，跑时只用 `$BOOT` |
| `IAPTranfer_Tool/TestCase/host/bootloader_unit/gen_vectors.py` | `$TEST` 契约测试 | 调 `$TOOL` 出货的 IAPTool 生成 `$BOOT` 测试的黄金向量，两个仓（见「bootloader 的 C 单元测试用什么驱动」） |
| `IAPTranfer_Tool/TestCase/host/bootloader_unit/golden_vectors.h` | `$BOOT` 部件测试 | T1-16：编 `$BOOT` 的真实源码，黄金向量已提交，跑时只用 `$BOOT` |
| `IAPTranfer_Tool/TestCase/host/bootloader_unit/stubs/bootloader_state_stub.c` | `$BOOT` 部件测试 | T1-16：编 `$BOOT` 的真实源码，黄金向量已提交，跑时只用 `$BOOT` |
| `IAPTranfer_Tool/TestCase/host/bootloader_unit/stubs/hal_stub.c` | `$BOOT` 部件测试 | T1-16：编 `$BOOT` 的真实源码，黄金向量已提交，跑时只用 `$BOOT` |
| `IAPTranfer_Tool/TestCase/host/bootloader_unit/stubs/hal_stub.h` | `$BOOT` 部件测试 | T1-16：编 `$BOOT` 的真实源码，黄金向量已提交，跑时只用 `$BOOT` |
| `IAPTranfer_Tool/TestCase/host/bootloader_unit/stubs/main.h` | `$BOOT` 部件测试 | T1-16：编 `$BOOT` 的真实源码，黄金向量已提交，跑时只用 `$BOOT` |
| `IAPTranfer_Tool/TestCase/host/bootloader_unit/stubs/owner_slot_stub.c` | `$BOOT` 部件测试 | T1-16：编 `$BOOT` 的真实源码，黄金向量已提交，跑时只用 `$BOOT` |
| `IAPTranfer_Tool/TestCase/host/bootloader_unit/stubs/owner_slot_stub.h` | `$BOOT` 部件测试 | T1-16：编 `$BOOT` 的真实源码，黄金向量已提交，跑时只用 `$BOOT` |
| `IAPTranfer_Tool/TestCase/host/bootloader_unit/stubs/rng.h` | `$BOOT` 部件测试 | T1-16：编 `$BOOT` 的真实源码，黄金向量已提交，跑时只用 `$BOOT` |
| `IAPTranfer_Tool/TestCase/host/bootloader_unit/stubs/rtc.h` | `$BOOT` 部件测试 | T1-16：编 `$BOOT` 的真实源码，黄金向量已提交，跑时只用 `$BOOT` |
| `IAPTranfer_Tool/TestCase/host/bootloader_unit/test_main.c` | `$BOOT` 部件测试 | T1-16：编 `$BOOT` 的真实源码，黄金向量已提交，跑时只用 `$BOOT` |
| `IAPTranfer_Tool/TestCase/host/crypto_ref/CROSS-CHECK.md` | `$TOOL` 部件测试 | T1-19/T1-20：只拿 IAPTool 的签名对照独立实现 |
| `IAPTranfer_Tool/TestCase/host/crypto_ref/ecdsa_verify.py` | `$TOOL` 部件测试 | T1-19/T1-20：只拿 IAPTool 的签名对照独立实现 |
| `IAPTranfer_Tool/TestCase/host/crypto_ref/run_checks.py` | `$TOOL` 部件测试 | T1-19/T1-20：只拿 IAPTool 的签名对照独立实现 |
| `IAPTranfer_Tool/TestCase/host/crypto_ref/sha256_ref.py` | `$TOOL` 部件测试 | T1-19/T1-20：只拿 IAPTool 的签名对照独立实现 |
| `IAPTranfer_Tool/TestCase/host/examples_build/build.py` | `$CORE_REPO` 部件测试 | P5：只用板卡包和 `arduino-cli` |
| `IAPTranfer_Tool/TestCase/host/fakeboard/KEY-MATCH.md` | `$TOOL` 部件测试 | T1-18 的判据说明，跟着 run_cases.py 走 |
| `IAPTranfer_Tool/TestCase/host/fakeboard/_common.py` | 待定：部件测试和整机测试共用的替身（交给「IAPTool 测试用的假板子」） | T1-18（`$TOOL` 部件）和 T1-34（整机）都用它 |
| `IAPTranfer_Tool/TestCase/host/fakeboard/fake_board.py` | 待定：部件测试和整机测试共用的替身（交给「IAPTool 测试用的假板子」） | T1-18（`$TOOL` 部件）和 T1-34（整机）都用它 |
| `IAPTranfer_Tool/TestCase/host/fakeboard/run_cases.py` | `$TOOL` 部件测试 | T1-18a–g：只用 IAPTool 和假板子 |
| `IAPTranfer_Tool/TestCase/host/fakeboard/run_ide_upload.py` | `$TEST` 整机测试 | T1-34：`arduino-cli` + 板卡包的上传配方 + IAPTool，三样东西 |
| `IAPTranfer_Tool/TestCase/host/iapcert/iapcert_test.go` | `$TOOL` 部件测试 | T1-15：只测 `$TOOL` 的 `iapcert` |
| `IAPTranfer_Tool/TestCase/host/owner_capacity/build.py` | `$BOOT` 部件测试 | T2-22–T2-33、T1-33、T2-27：只编 `$BOOT` 的源码 |
| `IAPTranfer_Tool/TestCase/host/owner_capacity/stubs/fake_owner_flash.c` | `$BOOT` 部件测试 | T2-22–T2-33、T1-33、T2-27：只编 `$BOOT` 的源码 |
| `IAPTranfer_Tool/TestCase/host/owner_capacity/stubs/fake_owner_flash.h` | `$BOOT` 部件测试 | T2-22–T2-33、T1-33、T2-27：只编 `$BOOT` 的源码 |
| `IAPTranfer_Tool/TestCase/host/owner_capacity/stubs/reclaim_stub.c` | `$BOOT` 部件测试 | T2-22–T2-33、T1-33、T2-27：只编 `$BOOT` 的源码 |
| `IAPTranfer_Tool/TestCase/host/owner_capacity/stubs/usbd_cdc_flash.h` | `$BOOT` 部件测试 | T2-22–T2-33、T1-33、T2-27：只编 `$BOOT` 的源码 |
| `IAPTranfer_Tool/TestCase/host/owner_capacity/test_main.c` | `$BOOT` 部件测试 | T2-22–T2-33、T1-33、T2-27：只编 `$BOOT` 的源码 |
| `IAPTranfer_Tool/TestCase/host/owner_revoke/build.py` | `$CORE_REPO` 部件测试 | T2-21：编的是板卡包 `libraries/OpenPLC_IAP/src/owner_root_ro.c`，不是 bootloader |
| `IAPTranfer_Tool/TestCase/host/owner_revoke/stubs/fake_owner_area.h` | `$CORE_REPO` 部件测试 | T2-21：编的是板卡包 `libraries/OpenPLC_IAP/src/owner_root_ro.c`，不是 bootloader |
| `IAPTranfer_Tool/TestCase/host/owner_revoke/stubs/iap_keyderive_stub.c` | `$CORE_REPO` 部件测试 | T2-21：编的是板卡包 `libraries/OpenPLC_IAP/src/owner_root_ro.c`，不是 bootloader |
| `IAPTranfer_Tool/TestCase/host/owner_revoke/stubs/iap_keyderive_stub.h` | `$CORE_REPO` 部件测试 | T2-21：编的是板卡包 `libraries/OpenPLC_IAP/src/owner_root_ro.c`，不是 bootloader |
| `IAPTranfer_Tool/TestCase/host/owner_revoke/test_main.c` | `$CORE_REPO` 部件测试 | T2-21：编的是板卡包 `libraries/OpenPLC_IAP/src/owner_root_ro.c`，不是 bootloader |
| `IAPTranfer_Tool/TestCase/host/renode/run.py` | `$TEST` 整机测试 | T3-05：`$BOOT` 的 bootloader + 板卡包例程 + IAPTool，在 Renode 里 |
| `IAPTranfer_Tool/TestCase/host/sector15_reclaim/build.py` | `$BOOT` 部件测试 | T2-34：只编 `$BOOT` 的源码 |
| `IAPTranfer_Tool/TestCase/host/sector15_reclaim/stubs/fake_flash.c` | `$BOOT` 部件测试 | T2-34：只编 `$BOOT` 的源码 |
| `IAPTranfer_Tool/TestCase/host/sector15_reclaim/stubs/host_s15.h` | `$BOOT` 部件测试 | T2-34：只编 `$BOOT` 的源码 |
| `IAPTranfer_Tool/TestCase/host/sector15_reclaim/stubs/stm32h7xx_hal.h` | `$BOOT` 部件测试 | T2-34：只编 `$BOOT` 的源码 |
| `IAPTranfer_Tool/TestCase/host/sector15_reclaim/stubs/usbd_cdc_flash.h` | `$BOOT` 部件测试 | T2-34：只编 `$BOOT` 的源码 |
| `IAPTranfer_Tool/TestCase/host/sector15_reclaim/test_main.c` | `$BOOT` 部件测试 | T2-34：只编 `$BOOT` 的源码 |
| `IAPTranfer_Tool/TestCase/host/variant_check/build.py` | `$CORE_REPO` 部件测试 | P4：只用板卡包和 `arduino-cli` |
| `IAPTranfer_Tool/TestCase/host/variant_check/m4_fmc_pins/m4_fmc_pins.ino` | `$CORE_REPO` 部件测试 | P4：只用板卡包和 `arduino-cli` |
| `IAPTranfer_Tool/TestCase/host/variant_check/uart_routing/uart_routing.ino` | `$CORE_REPO` 部件测试 | P4：只用板卡包和 `arduino-cli` |
| `IAPTranfer_Tool/TestCase/host/vector_alignment/build.py` | `$CORE_REPO` 部件测试 | P15：只用板卡包和 `arduino-cli` |
| `IAPTranfer_Tool/TestCase/main.go` | `$TEST` 整机测试 | `TestCase.exe` 的入口；它 import `$TOOL` 的 `iapcert` / `iapproto` 并调 IAPTool.exe，对着真板子跑 |
| `IAPTranfer_Tool/TestCase/nonce_replay.go` | 待定：只用一个仓但要上真板子（交给「只需要一个仓、但必须上真板子的测试归哪」） | T1-17：只测 bootloader 的防重放，要真板子 |
| `IAPTranfer_Tool/TestCase/onboard/iap_probe/iap_probe.ino` | `$TEST` 整机测试 | 五条路径用的探针 app，由 `build_probe_image.py` 编、IAPTool 传 |
| `IAPTranfer_Tool/TestCase/onboard/rs232/M5_SerialConflict/M5_SerialConflict.ino` | `$TEST` 整机测试 | T3-03 / T3-04：由 `run_m5.py` 等用 `arduino-cli` 编、IAPTool 传 |
| `IAPTranfer_Tool/TestCase/onboard/rs232/SerialPort/SerialPort.ino` | `$TEST` 整机测试 | T3-03 / T3-04：由 `run_m5.py` 等用 `arduino-cli` 编、IAPTool 传 |
| `IAPTranfer_Tool/TestCase/onboard/sdram/SDRAM_Acceptance/SDRAM_Acceptance.ino` | `$TEST` 整机测试 | T3-02：由 `run_sdram.py` 用 `arduino-cli` 编、IAPTool 传 |
| `IAPTranfer_Tool/TestCase/requirements.txt` | `$TEST` 测试基础设施 | Python 依赖清单 |
| `IAPTranfer_Tool/TestCase/signature.go` | `$TEST` 整机测试 | T1-11/12/14：import `$TOOL` 的 `iapcert` 造签名镜像，发给真板子 bootloader |
| `IAPTranfer_Tool/TestCase/signature_badcrc.go` | 待定：只用一个仓但要上真板子（交给「只需要一个仓、但必须上真板子的测试归哪」） | T1-24：只测 bootloader 拒收坏 CRC，要真板子 |
| `IAPTranfer_Tool/TestCase/signature_wrongkey.go` | `$TEST` 整机测试 | T1-19/20 相关：调 IAPTool.exe，对着真板子 |
| `IAPTranfer_Tool/TestCase/tcp_session.go` | `$TEST` 整机测试 | T1-06–T1-10：import `$TOOL` 的 `iapproto`、调 IAPTool.exe，对着真板子 |
| `IAPTranfer_Tool/TestCase/tools/build_image.py` | `$TEST` 测试基础设施 | 本机配置、平台层、烧录、抓串口、板子状态、端口小工具 |
| `IAPTranfer_Tool/TestCase/tools/build_probe_image.py` | `$TEST` 测试基础设施 | 本机配置、平台层、烧录、抓串口、板子状态、端口小工具 |
| `IAPTranfer_Tool/TestCase/tools/can_send.py` | `$TEST` 测试基础设施 | 本机配置、平台层、烧录、抓串口、板子状态、端口小工具 |
| `IAPTranfer_Tool/TestCase/tools/can_watch.py` | `$TEST` 测试基础设施 | 本机配置、平台层、烧录、抓串口、板子状态、端口小工具 |
| `IAPTranfer_Tool/TestCase/tools/check_allow_hygiene.py` | 待定：不测产品，查各仓的 `.claude` 权限文件（交给「文档检查搬进 OpenPLC_Docs 后长什么样」） | P10：扫各仓的 `.claude/settings*.json` |
| `IAPTranfer_Tool/TestCase/tools/check_changelist_has_no_orphans.py` | `$PROD` 文档检查 | P14：查 `$PROD` |
| `IAPTranfer_Tool/TestCase/tools/check_core_sync.py` | `$CORE_REPO` 部件测试 | P3：板卡包的两份（`$CORE_LIVE` 和 `$CORE_REPO`） |
| `IAPTranfer_Tool/TestCase/tools/check_cproject_ld.py` | `$BOOT` 部件测试 | P17：只扫 `$BOOT` |
| `IAPTranfer_Tool/TestCase/tools/check_doc_dupes.py` | `$PROD` 文档检查 | P8：查 `$PROD` |
| `IAPTranfer_Tool/TestCase/tools/check_doc_paths.py` | `$PROD` 文档检查 | P9：查 `$PROD`，再到各代码仓核对路径 |
| `IAPTranfer_Tool/TestCase/tools/check_icache_is_restored.py` | `$BOOT` 部件测试 | P16：只扫 `$BOOT` |
| `IAPTranfer_Tool/TestCase/tools/check_mirror_sync.py` | `$TEST` 契约测试 | P2：比 `$BOOT`、板卡包、`$TOOL` 的镜像代码 |
| `IAPTranfer_Tool/TestCase/tools/check_no_sector15_writes.py` | `$CORE_REPO` 部件测试 | P19：只扫板卡包 |
| `IAPTranfer_Tool/TestCase/tools/check_no_stale_ids.py` | `$PROD` 文档检查 | P13：查 `$PROD`，再扫各代码仓 |
| `IAPTranfer_Tool/TestCase/tools/check_status_sync.py` | `$PROD` 文档检查 | P7：查 `$PROD` |
| `IAPTranfer_Tool/TestCase/tools/check_tool_sync.py` | `$TEST` 契约测试 | P11：比 `$TOOL` 编出的 IAPTool 和板卡包里那份 |
| `IAPTranfer_Tool/TestCase/tools/check_version_sync.py` | `$TEST` 契约测试 | P1：比 `$BOOT` 和板卡包的版本号 |
| `IAPTranfer_Tool/TestCase/tools/common.py` | `$TEST` 测试基础设施 | 本机配置、平台层、烧录、抓串口、板子状态、端口小工具 |
| `IAPTranfer_Tool/TestCase/tools/enter_bootloader.py` | `$TEST` 测试基础设施 | 本机配置、平台层、烧录、抓串口、板子状态、端口小工具 |
| `IAPTranfer_Tool/TestCase/tools/flash_bootloader.py` | `$TEST` 测试基础设施 | 本机配置、平台层、烧录、抓串口、板子状态、端口小工具 |
| `IAPTranfer_Tool/TestCase/tools/init_machine.py` | `$TEST` 测试基础设施 | 本机配置、平台层、烧录、抓串口、板子状态、端口小工具 |
| `IAPTranfer_Tool/TestCase/tools/inject_owner_record.py` | `$TEST` 测试基础设施 | 本机配置、平台层、烧录、抓串口、板子状态、端口小工具 |
| `IAPTranfer_Tool/TestCase/tools/install_tool.py` | 不是测试：`$TOOL` 的发版工具 | 把 IAPTool 拷进板卡包，属于 IAPTool 发版 |
| `IAPTranfer_Tool/TestCase/tools/netifquery/main.go` | `$TEST` 测试基础设施 | 本机配置、平台层、烧录、抓串口、板子状态、端口小工具 |
| `IAPTranfer_Tool/TestCase/tools/platform_info.py` | `$TEST` 测试基础设施 | 本机配置、平台层、烧录、抓串口、板子状态、端口小工具 |
| `IAPTranfer_Tool/TestCase/tools/reset_board_to_factory_state.py` | `$TEST` 测试基础设施 | 本机配置、平台层、烧录、抓串口、板子状态、端口小工具 |
| `IAPTranfer_Tool/TestCase/tools/rs485_echo.py` | `$TEST` 测试基础设施 | 本机配置、平台层、烧录、抓串口、板子状态、端口小工具 |
| `IAPTranfer_Tool/TestCase/tools/run_au1.py` | 待定：只用一个仓但要上真板子（交给「只需要一个仓、但必须上真板子的测试归哪」） | T1-17：只用 ST-Link 和真板子 bootloader，不调 IAPTool |
| `IAPTranfer_Tool/TestCase/tools/run_boot0_upload_mode.py` | 待定：只用一个仓但要上真板子（交给「只需要一个仓、但必须上真板子的测试归哪」） | T1-27：只看真板子 bootloader 的串口，不调 IAPTool |
| `IAPTranfer_Tool/TestCase/tools/run_case.py` | `$TEST` 测试基础设施 | 跑 `TestCase.exe` 的用例并判结果 |
| `IAPTranfer_Tool/TestCase/tools/run_cdc_does_not_start_ethernet.py` | `$TEST` 整机测试 | 调 IAPTool（多数还用 ST-Link / `arduino-cli`）对着真板子跑 |
| `IAPTranfer_Tool/TestCase/tools/run_delegated_cert_on_real_board.py` | `$TEST` 整机测试 | 调 IAPTool（多数还用 ST-Link / `arduino-cli`）对着真板子跑 |
| `IAPTranfer_Tool/TestCase/tools/run_examples.py` | `$TEST` 整机测试 | 调 IAPTool（多数还用 ST-Link / `arduino-cli`）对着真板子跑 |
| `IAPTranfer_Tool/TestCase/tools/run_five_paths.py` | `$TEST` 整机测试 | 调 IAPTool（多数还用 ST-Link / `arduino-cli`）对着真板子跑 |
| `IAPTranfer_Tool/TestCase/tools/run_flashboot.py` | `$TEST` 整机测试 | 调 IAPTool（多数还用 ST-Link / `arduino-cli`）对着真板子跑 |
| `IAPTranfer_Tool/TestCase/tools/run_journal_reclaim.py` | `$TEST` 整机测试 | 调 IAPTool（多数还用 ST-Link / `arduino-cli`）对着真板子跑 |
| `IAPTranfer_Tool/TestCase/tools/run_journal_slot_accounting.py` | `$TEST` 整机测试 | 调 IAPTool（多数还用 ST-Link / `arduino-cli`）对着真板子跑 |
| `IAPTranfer_Tool/TestCase/tools/run_m5.py` | `$TEST` 整机测试 | 调 IAPTool（多数还用 ST-Link / `arduino-cli`）对着真板子跑 |
| `IAPTranfer_Tool/TestCase/tools/run_old_root_image_is_refused.py` | `$TEST` 整机测试 | 调 IAPTool（多数还用 ST-Link / `arduino-cli`）对着真板子跑 |
| `IAPTranfer_Tool/TestCase/tools/run_revoke_leaf.py` | `$TEST` 整机测试 | 调 IAPTool（多数还用 ST-Link / `arduino-cli`）对着真板子跑 |
| `IAPTranfer_Tool/TestCase/tools/run_rotate_root_revokes_old_leaf.py` | `$TEST` 整机测试 | 调 IAPTool（多数还用 ST-Link / `arduino-cli`）对着真板子跑 |
| `IAPTranfer_Tool/TestCase/tools/run_s3.py` | `$TEST` 整机测试 | 调 IAPTool（多数还用 ST-Link / `arduino-cli`）对着真板子跑 |
| `IAPTranfer_Tool/TestCase/tools/run_s4.py` | `$TEST` 整机测试 | 调 IAPTool（多数还用 ST-Link / `arduino-cli`）对着真板子跑 |
| `IAPTranfer_Tool/TestCase/tools/run_sdram.py` | `$TEST` 整机测试 | 调 IAPTool（多数还用 ST-Link / `arduino-cli`）对着真板子跑 |
| `IAPTranfer_Tool/TestCase/tools/run_setowner.py` | `$TEST` 整机测试 | 调 IAPTool（多数还用 ST-Link / `arduino-cli`）对着真板子跑 |
| `IAPTranfer_Tool/TestCase/tools/run_takeown.py` | `$TEST` 整机测试 | 调 IAPTool（多数还用 ST-Link / `arduino-cli`）对着真板子跑 |
| `IAPTranfer_Tool/TestCase/tools/selfcheck.py` | `$TEST` 测试基础设施 | 现在的总自检入口；拆完各仓各一个 |
| `IAPTranfer_Tool/TestCase/tools/serial_watch.py` | `$TEST` 测试基础设施 | 本机配置、平台层、烧录、抓串口、板子状态、端口小工具 |
| `IAPTranfer_Tool/TestCase/tools/test_init_machine.py` | `$TEST` 测试基础设施 | 本机配置、平台层、烧录、抓串口、板子状态、端口小工具 |
| `IAPTranfer_Tool/TestCase/tools/upload_and_watch.py` | `$TEST` 测试基础设施 | 本机配置、平台层、烧录、抓串口、板子状态、端口小工具 |
| `IAPTranfer_Tool/TestCase/udp_discovery.go` | 待定：只用一个仓但要上真板子（交给「只需要一个仓、但必须上真板子的测试归哪」） | T1-01–T1-05：只测 bootloader 的发现协议，唯一的第二个仓是为拨号 import 的 `$TOOL/internal/iapproto` |
| `IAPTranfer_Tool/TestCase/watch.go` | `$TEST` 整机测试 | `TestCase.exe` 内部的串口观察，跟着它走 |
| `IAPTranfer_Tool/internal/iapproto/iapproto_test.go` | `$TOOL` 部件测试 | 只用 `$TOOL`（T1-35） |
| `IAPTranfer_Tool/internal/serialx/ioreg_test.go` | `$TOOL` 部件测试 | 只用 `$TOOL`（T1-35） |
| `IAPTranfer_Tool/internal/serialx/steady_test.go` | `$TOOL` 部件测试 | 只用 `$TOOL`（T1-35） |
| `IAPTranfer_Tool/internal/serialx/sysfs_test.go` | `$TOOL` 部件测试 | 只用 `$TOOL`（T1-35） |
| `IAPTranfer_Tool/key_lookup_test.go` | `$TOOL` 部件测试 | 只用 `$TOOL`（T1-35） |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/PORTTOOL-CAPS-TEST.md` | `$PORTTOOL` 部件测试 | T4-01 的说明，跟着 harness 走 |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/build.py` | `$PORTTOOL` 部件测试 | T4-01：编工装固件 `$BOOT/TestCase/porttool/`，按决策 78 的例外算 PortTool 自己的 |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/caps_golden.txt` | `$PORTTOOL` 部件测试 | T4-01 产出并提交的能力表；跑 Go 测试时只读它 |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/harness/sim_main.c` | `$PORTTOOL` 部件测试 | T4-01 / 模拟板：编工装固件，决策 78 的例外 |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/harness/stubs/analog_stub.c` | `$PORTTOOL` 部件测试 | T4-01 / 模拟板：编工装固件，决策 78 的例外 |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/harness/stubs/can_stub.c` | `$PORTTOOL` 部件测试 | T4-01 / 模拟板：编工装固件，决策 78 的例外 |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/harness/stubs/dout_stub.c` | `$PORTTOOL` 部件测试 | T4-01 / 模拟板：编工装固件，决策 78 的例外 |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/harness/stubs/entries_stub.c` | `$PORTTOOL` 部件测试 | T4-01 / 模拟板：编工装固件，决策 78 的例外 |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/harness/stubs/hal_stub.c` | `$PORTTOOL` 部件测试 | T4-01 / 模拟板：编工装固件，决策 78 的例外 |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/harness/stubs/knx_stub.c` | `$PORTTOOL` 部件测试 | T4-01 / 模拟板：编工装固件，决策 78 的例外 |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/harness/stubs/lwip.h` | `$PORTTOOL` 部件测试 | T4-01 / 模拟板：编工装固件，决策 78 的例外 |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/harness/stubs/lwip/dhcp.h` | `$PORTTOOL` 部件测试 | T4-01 / 模拟板：编工装固件，决策 78 的例外 |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/harness/stubs/lwip/netif.h` | `$PORTTOOL` 部件测试 | T4-01 / 模拟板：编工装固件，决策 78 的例外 |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/harness/stubs/lwip/tcp.h` | `$PORTTOOL` 部件测试 | T4-01 / 模拟板：编工装固件，决策 78 的例外 |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/harness/stubs/lwip_fake.h` | `$PORTTOOL` 部件测试 | T4-01 / 模拟板：编工装固件，决策 78 的例外 |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/harness/stubs/lwip_stub.c` | `$PORTTOOL` 部件测试 | T4-01 / 模拟板：编工装固件，决策 78 的例外 |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/harness/stubs/rs485_stub.c` | `$PORTTOOL` 部件测试 | T4-01 / 模拟板：编工装固件，决策 78 的例外 |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/harness/stubs/stm32h7xx_hal.h` | `$PORTTOOL` 部件测试 | T4-01 / 模拟板：编工装固件，决策 78 的例外 |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/harness/stubs/usb_device.h` | `$PORTTOOL` 部件测试 | T4-01 / 模拟板：编工装固件，决策 78 的例外 |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/harness/stubs/usb_stub.c` | `$PORTTOOL` 部件测试 | T4-01 / 模拟板：编工装固件，决策 78 的例外 |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/harness/stubs/usbd_cdc_if.h` | `$PORTTOOL` 部件测试 | T4-01 / 模拟板：编工装固件，决策 78 的例外 |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/harness/stubs/usbd_def.h` | `$PORTTOOL` 部件测试 | T4-01 / 模拟板：编工装固件，决策 78 的例外 |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/harness/test_main.c` | `$PORTTOOL` 部件测试 | T4-01 / 模拟板：编工装固件，决策 78 的例外 |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/ptboard_test.go` | `$PORTTOOL` 部件测试 | Go 测试只读已提交的 `caps_golden.txt`，只用 `$PORTTOOL` |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/pthold_test.go` | `$PORTTOOL` 部件测试 | Go 测试只读已提交的 `caps_golden.txt`，只用 `$PORTTOOL` |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/ptpanel_test.go` | `$PORTTOOL` 部件测试 | Go 测试只读已提交的 `caps_golden.txt`，只用 `$PORTTOOL` |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_caps/ptproto_test.go` | `$PORTTOOL` 部件测试 | Go 测试只读已提交的 `caps_golden.txt`，只用 `$PORTTOOL` |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_panel/naive.py` | `$PORTTOOL` 部件测试 | T4-02 / T4-03：面板 + 模拟板，决策 78 的例外 |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_panel/run.py` | `$PORTTOOL` 部件测试 | T4-02 / T4-03：面板 + 模拟板，决策 78 的例外 |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_plan/fake_board_test.go` | `$PORTTOOL` 部件测试 | T4-04：假板子 + 已提交的能力表，只用 `$PORTTOOL` |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_plan/panel_plan_test.go` | `$PORTTOOL` 部件测试 | T4-04：假板子 + 已提交的能力表，只用 `$PORTTOOL` |
| `OpenPLC_PortsTestingTool/TestCase/host/porttool_plan/plan_test.go` | `$PORTTOOL` 部件测试 | T4-04：假板子 + 已提交的能力表，只用 `$PORTTOOL` |
| `OpenPLC_PortsTestingTool/TestCase/plans/bench-smoke.json` | 不是测试：`$PORTTOOL` 的产品数据或发版工具 | 随 PortTool 发出去的方案文件 |
| `OpenPLC_PortsTestingTool/TestCase/plans/station6-poweron-relaxed.json` | 不是测试：`$PORTTOOL` 的产品数据或发版工具 | 随 PortTool 发出去的方案文件 |
| `OpenPLC_PortsTestingTool/TestCase/plans/station6-poweron.json` | 不是测试：`$PORTTOOL` 的产品数据或发版工具 | 随 PortTool 发出去的方案文件 |
| `OpenPLC_PortsTestingTool/TestCase/tools/build_fixture.py` | 不是测试：`$PORTTOOL` 的产品数据或发版工具 | 编工装镜像，交付要用 |
| `OpenPLC_PortsTestingTool/TestCase/tools/check_calarea.py` | `$TEST` 契约测试 | 和 P2 的校准值区一项合成一道，一次比 `$BOOT`、板卡包、`$PORTTOOL` 三方 |
| `OpenPLC_PortsTestingTool/TestCase/tools/check_doc_paths.py` | `$PROD` 文档检查 | 查 `$PROD` 里的 `$PORTTOOL/...` 路径 |
| `OpenPLC_PortsTestingTool/TestCase/tools/common.py` | `$PORTTOOL` 自己的测试基础设施（留不留交给「部件仓要不要本机配置」） | 本仓的 `common` / `init_machine` / `selfcheck` |
| `OpenPLC_PortsTestingTool/TestCase/tools/init_machine.py` | `$PORTTOOL` 自己的测试基础设施（留不留交给「部件仓要不要本机配置」） | 本仓的 `common` / `init_machine` / `selfcheck` |
| `OpenPLC_PortsTestingTool/TestCase/tools/make_delivery.py` | 不是测试：`$PORTTOOL` 的产品数据或发版工具 | 打交付包 |
| `OpenPLC_PortsTestingTool/TestCase/tools/md2html.py` | 不是测试：`$PORTTOOL` 的产品数据或发版工具 | 交付包里的说明页 |
| `OpenPLC_PortsTestingTool/TestCase/tools/selfcheck.py` | `$PORTTOOL` 自己的测试基础设施（留不留交给「部件仓要不要本机配置」） | 本仓的 `common` / `init_machine` / `selfcheck` |
| `OpenPLC_PortsTestingTool/internal/calarea/calarea_test.go` | `$PORTTOOL` 部件测试 | 只用 `$PORTTOOL` |
| `OpenPLC_PortsTestingTool/internal/ptcal/ptcal_test.go` | `$PORTTOOL` 部件测试 | 只用 `$PORTTOOL` |
| `OpenPLC_PortsTestingTool/internal/ptecho/ptecho_test.go` | `$PORTTOOL` 部件测试 | 只用 `$PORTTOOL` |
| `OpenPLC_PortsTestingTool/internal/ptpanel/link_test.go` | `$PORTTOOL` 部件测试 | 只用 `$PORTTOOL` |
| `OpenPLC_PortsTestingTool/internal/ptpanel/net_test.go` | `$PORTTOOL` 部件测试 | 只用 `$PORTTOOL` |
| `OpenPLC_PortsTestingTool/internal/serialx/ioreg_test.go` | `$PORTTOOL` 部件测试 | 只用 `$PORTTOOL` |
| `OpenPLC_PortsTestingTool/internal/serialx/steady_test.go` | `$PORTTOOL` 部件测试 | 只用 `$PORTTOOL` |
| `OpenPLC_PortsTestingTool/internal/serialx/sysfs_test.go` | `$PORTTOOL` 部件测试 | 只用 `$PORTTOOL` |
| `OpenPLC_PortsTestingTool/internal/simboard/simboard_test.go` | `$PORTTOOL` 部件测试 | 只用 `$PORTTOOL` |
| `open_plc_cube_ide/TestCase/ADC/adc_test.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/ADC/adc_test.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/CAN/can_test.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/CAN/can_test.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/DAC/dac_test.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/DAC/dac_test.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/DIN/din_test.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/DIN/din_test.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/ETH/eth_test.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/ETH/eth_test.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/KNX/knx_test.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/KNX/knx_test.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/PWM/pwm_test.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/PWM/pwm_test.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/RELAY/relay_test.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/RELAY/relay_test.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/RS232/rs232_test.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/RS232/rs232_test.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/RS485/rs485_test.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/RS485/rs485_test.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/SD/sd_test.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/SD/sd_test.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/SDRAM/sdram_test.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/SDRAM/sdram_test.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/bringup_test.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/bringup_test.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/ccsbcs.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/diskio.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/diskio.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/ff.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/ff.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/ff_gen_drv.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/ff_gen_drv.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/ffconf.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/integer.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/port_adc.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/port_adc.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/port_can.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/port_can.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/port_dac.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/port_dac.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/port_din.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/port_din.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/port_dout.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/port_dout.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/port_led.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/port_led.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/port_pwm.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/port_pwm.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/port_rs485.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/port_rs485.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/port_vref.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/port_vref.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/stm32h7xx_hal_adc.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/stm32h7xx_hal_adc.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/stm32h7xx_hal_adc_ex.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/stm32h7xx_hal_adc_ex.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/stm32h7xx_hal_dac.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/stm32h7xx_hal_dac.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/stm32h7xx_hal_dac_ex.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/stm32h7xx_hal_dac_ex.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/stm32h7xx_hal_fdcan.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/stm32h7xx_hal_fdcan.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/stm32h7xx_hal_sd.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/stm32h7xx_hal_sd.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/stm32h7xx_hal_sd_ex.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/stm32h7xx_hal_sd_ex.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/stm32h7xx_ll_adc.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/stm32h7xx_ll_delayblock.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/stm32h7xx_ll_delayblock.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/stm32h7xx_ll_sdmmc.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/stm32h7xx_ll_sdmmc.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/common/testcase_hal_guard.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/porttool/porttool.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/porttool/porttool.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/porttool/porttool_ain.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/porttool/porttool_aout.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/porttool/porttool_can.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/porttool/porttool_cmd.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/porttool/porttool_cmd.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/porttool/porttool_din.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/porttool/porttool_dout.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/porttool/porttool_eth.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/porttool/porttool_knx.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/porttool/porttool_relay.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/porttool/porttool_rs232.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/porttool/porttool_rs485.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/porttool/porttool_run.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/porttool/porttool_run.h` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/porttool/porttool_sd.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/porttool/porttool_sdram.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/porttool/porttool_temp.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_cube_ide/TestCase/porttool/porttool_usb.c` | 不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码） | 只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/scripts/ci/check_compliance.py` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/CMakeLists.txt` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/metal-header-template.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/metal-test.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/metal-test.h` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/CMakeLists.txt` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/freertos/CMakeLists.txt` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/freertos/alloc.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/freertos/atomic.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/freertos/irq.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/freertos/main.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/freertos/mutex.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/freertos/sleep.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/freertos/threads.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/freertos/zynq7/CMakeLists.txt` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/freertos/zynq7/Xilinx.spec` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/freertos/zynq7/lscript.ld` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/freertos/zynqmp_a53/CMakeLists.txt` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/freertos/zynqmp_a53/lscript.ld` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/freertos/zynqmp_r5/CMakeLists.txt` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/freertos/zynqmp_r5/lscript.ld` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/generic/CMakeLists.txt` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/generic/alloc.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/generic/atomic.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/generic/irq.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/generic/main.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/generic/microblaze_generic/CMakeLists.txt` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/generic/microblaze_generic/helper.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/generic/microblaze_generic/lscript.ld` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/generic/microblaze_generic/platform.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/generic/microblaze_generic/platform.h` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/generic/mutex.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/generic/zynq7/CMakeLists.txt` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/generic/zynq7/Xilinx.spec` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/generic/zynq7/helper.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/generic/zynq7/lscript.ld` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/generic/zynqmp_a53/CMakeLists.txt` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/generic/zynqmp_a53/helper.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/generic/zynqmp_a53/lscript.ld` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/generic/zynqmp_r5/CMakeLists.txt` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/generic/zynqmp_r5/helper.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/generic/zynqmp_r5/lscript.ld` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/linux/CMakeLists.txt` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/linux/alloc.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/linux/atomic.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/linux/condition.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/linux/irq.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/linux/main.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/linux/mutex.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/linux/shmem.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/linux/spinlock.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/linux/threads.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/linux/zynq/CMakeLists.txt` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/linux/zynq/device.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/zephyr/CMakeLists.txt` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/zephyr/alloc.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/zephyr/atomic.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/zephyr/main.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/zephyr/metal-test-internal.h` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/system/zephyr/mutex.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/libmetal/test/version.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/open-amp/apps/tests/CMakeLists.txt` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/open-amp/apps/tests/msg/CMakeLists.txt` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/open-amp/apps/tests/msg/rpmsg-flood-ping.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/open-amp/apps/tests/msg/rpmsg-ping.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/open-amp/apps/tests/msg/rpmsg-ping.h` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/open-amp/apps/tests/msg/rpmsg-update.c` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `open_plc_arduino/system/Middlewares/OpenAMP/open-amp/scripts/ci/check_compliance.py` | 上游第三方代码自带的，不属于本产品，不动 | OpenAMP 自带 |
| `OpenPLC_Docs/tools/check_no_orphan_placeholders.py` | `$PROD` 文档检查 | 已经在 `$PROD` |
| `OpenPLC_Docs/tools/check_wayfinder_ticket_hygiene.py` | `$PROD` 文档检查 | 已经在 `$PROD` |
