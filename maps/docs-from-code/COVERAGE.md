# 逐文件覆盖记录（机器生成）

**这份不是手写的** —— 由脚本对着 [CORPUS.md](CORPUS.md) 逐文件跑一遍生成，
所以它不可能漏掉语料里的文件。生成于 2026-09-16。

`设计段` = 该文件里带设计理由信号的多行注释段数（信号词见 `8,611 行怎么读完而不是抽样` 那张票）。
**`0` 段不是「没处理」，是「查过，没有可搬的」** —— 两种都要有记录，否则分不出「查过」和「忘了」。

| 批 | 文件 | 注释行 | 设计段 | 去向 |
|---|---|---:|---:|---|
| 3–5 | `IAPTranfer_Tool/./IAP_CDC.go` | 22 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/./IAP_Ether.go` | 46 | 4 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/./app.go` | 22 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 2 | `IAPTranfer_Tool/./auth.go` | 28 | 2 | `docs/security/`，逐条见 BATCH-LEDGER |
| 3–5 | `IAPTranfer_Tool/./build.py` | 13 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/./cert.go` | 6 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `IAPTranfer_Tool/./common.go` | 22 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 2 | `IAPTranfer_Tool/./owner.go` | 30 | 1 | `docs/security/`，逐条见 BATCH-LEDGER |
| 3–5 | `IAPTranfer_Tool/./sign.go` | 47 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/./uploadlock.go` | 16 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/host/bootloader_unit/gen_vectors.py` | 3 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/host/bootloader_unit/golden_vectors.h` | 18 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `IAPTranfer_Tool/TestCase/host/bootloader_unit/stubs/bootloader_state_stub.c` | 6 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/host/bootloader_unit/stubs/hal_stub.h` | 11 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `IAPTranfer_Tool/TestCase/host/bootloader_unit/stubs/main.h` | 9 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 2 | `IAPTranfer_Tool/TestCase/host/bootloader_unit/stubs/owner_slot_stub.c` | 5 | 0 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `IAPTranfer_Tool/TestCase/host/bootloader_unit/stubs/owner_slot_stub.h` | 4 | 0 | `docs/security/`，逐条见 BATCH-LEDGER |
| 3–5 | `IAPTranfer_Tool/TestCase/host/bootloader_unit/stubs/rtc.h` | 14 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `IAPTranfer_Tool/TestCase/host/bootloader_unit/test_main.c` | 47 | 3 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 2 | `IAPTranfer_Tool/TestCase/host/crypto_ref/ecdsa_verify.py` | 3 | 0 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `IAPTranfer_Tool/TestCase/host/crypto_ref/run_checks.py` | 2 | 0 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `IAPTranfer_Tool/TestCase/host/crypto_ref/sha256_ref.py` | 5 | 0 | `docs/security/`，逐条见 BATCH-LEDGER |
| 3–5 | `IAPTranfer_Tool/TestCase/host/examples_build/build.py` | 13 | 3 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 2 | `IAPTranfer_Tool/TestCase/host/fakeboard/fake_board.py` | 3 | 0 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `IAPTranfer_Tool/TestCase/host/fakeboard/run_cases.py` | 16 | 3 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `IAPTranfer_Tool/TestCase/host/iapcert/iapcert_test.go` | 38 | 1 | `docs/security/`，逐条见 BATCH-LEDGER |
| 3–5 | `IAPTranfer_Tool/TestCase/host/porttool_caps/build.py` | 239 | 20 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/host/porttool_caps/harness/sim_main.c` | 85 | 8 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/host/porttool_caps/harness/stubs/analog_stub.c` | 33 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/host/porttool_caps/harness/stubs/can_stub.c` | 15 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `IAPTranfer_Tool/TestCase/host/porttool_caps/harness/stubs/dout_stub.c` | 20 | 3 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/host/porttool_caps/harness/stubs/entries_stub.c` | 59 | 12 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/host/porttool_caps/harness/stubs/hal_stub.c` | 30 | 3 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/host/porttool_caps/harness/stubs/knx_stub.c` | 15 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/host/porttool_caps/harness/stubs/lwip_fake.h` | 26 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/host/porttool_caps/harness/stubs/lwip_stub.c` | 19 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/host/porttool_caps/harness/stubs/rs485_stub.c` | 19 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/host/porttool_caps/harness/stubs/usb_device.h` | 4 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `IAPTranfer_Tool/TestCase/host/porttool_caps/harness/stubs/usb_stub.c` | 13 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/host/porttool_caps/harness/stubs/usbd_cdc_if.h` | 3 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `IAPTranfer_Tool/TestCase/host/porttool_caps/harness/stubs/usbd_def.h` | 11 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/host/porttool_caps/harness/test_main.c` | 240 | 25 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/host/porttool_caps/ptboard_test.go` | 22 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/host/porttool_caps/pthold_test.go` | 39 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/host/porttool_caps/ptpanel_test.go` | 57 | 6 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/host/porttool_caps/ptproto_test.go` | 49 | 6 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/host/porttool_panel/naive.py` | 72 | 8 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/host/porttool_panel/run.py` | 274 | 26 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/host/porttool_plan/fake_board_test.go` | 15 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/host/porttool_plan/panel_plan_test.go` | 35 | 5 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/host/porttool_plan/plan_test.go` | 124 | 13 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/host/variant_check/build.py` | 11 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/build_image.py` | 22 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/can_watch.py` | 1 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/check_allow_hygiene.py` | 4 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/check_core_sync.py` | 22 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/check_doc_dupes.py` | 22 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/check_doc_paths.py` | 32 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/check_mirror_sync.py` | 55 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/check_public_root.py` | 20 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/check_status_sync.py` | 18 | 3 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/check_version_sync.py` | 5 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/common.py` | 47 | 3 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/enter_bootloader.py` | 4 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/flash_bootloader.py` | 14 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/init_machine.py` | 76 | 3 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/inject_owner_record.py` | 22 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/install_tool.py` | 1 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/make_delivery.py` | 13 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/md2html.py` | 4 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/rs485_echo.py` | 4 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/run_au1.py` | 21 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/run_m5.py` | 8 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/run_s3.py` | 10 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/run_s4.py` | 21 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/run_sdram.py` | 3 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/run_setowner.py` | 5 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/run_takeown.py` | 5 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/selfcheck.py` | 25 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/serial_watch.py` | 2 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/test_init_machine.py` | 17 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/TestCase/tools/upload_and_watch.py` | 4 | 0 | **0 段，查过没有可搬的** |
| 2 | `IAPTranfer_Tool/iapcert/iapcert.go` | 66 | 3 | `docs/security/`，逐条见 BATCH-LEDGER |
| 3–5 | `IAPTranfer_Tool/internal/ptboard/board.go` | 75 | 5 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/internal/ptcal/ptcal.go` | 58 | 6 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/internal/ptcal/ptcal_test.go` | 24 | 6 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/internal/ptcheck/ptcheck.go` | 36 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/internal/ptecho/cdc.go` | 8 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/internal/ptecho/ptecho.go` | 46 | 5 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/internal/ptpanel/hold.go` | 52 | 5 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/internal/ptpanel/judge.go` | 95 | 11 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/internal/ptpanel/link.go` | 75 | 4 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/internal/ptpanel/link_test.go` | 30 | 3 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/internal/ptpanel/net.go` | 35 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/internal/ptpanel/net_test.go` | 16 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/internal/ptpanel/panel.go` | 128 | 13 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/internal/ptpanel/plan.go` | 52 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/internal/ptpanel/remember.go` | 29 | 4 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/internal/ptpanel/runlog.go` | 27 | 3 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/internal/ptplan/ptplan.go` | 106 | 7 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/internal/ptproto/caps.go` | 79 | 6 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/internal/ptproto/proto.go` | 50 | 3 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/internal/ptreport/ptreport.go` | 31 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/internal/ptseq/peer.go` | 68 | 3 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/internal/ptseq/ptseq.go` | 112 | 5 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/internal/serialx/enum_basic.go` | 7 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/internal/serialx/enum_detailed.go` | 5 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `IAPTranfer_Tool/internal/serialx/serialx.go` | 47 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/internal/serialx/steady_test.go` | 10 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/internal/simboard/simboard.go` | 36 | 3 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `IAPTranfer_Tool/internal/simboard/simboard_test.go` | 12 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_arduino/libraries/OpenPLC_IAP/src/OpenPLC_IAP_Autostart.h` | 11 | 0 | **0 段，查过没有可搬的** |
| 2 | `open_plc_arduino/libraries/OpenPLC_IAP/src/fw_pubkey.c` | 4 | 0 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `open_plc_arduino/libraries/OpenPLC_IAP/src/fw_pubkey.h` | 8 | 0 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `open_plc_arduino/libraries/OpenPLC_IAP/src/fw_verify.c` | 1 | 0 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `open_plc_arduino/libraries/OpenPLC_IAP/src/fw_verify.h` | 12 | 0 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `open_plc_arduino/libraries/OpenPLC_IAP/src/iap_auth.c` | 8 | 0 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `open_plc_arduino/libraries/OpenPLC_IAP/src/iap_auth.h` | 18 | 0 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `open_plc_arduino/libraries/OpenPLC_IAP/src/iap_cert.c` | 1 | 0 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `open_plc_arduino/libraries/OpenPLC_IAP/src/iap_cert.h` | 7 | 0 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `open_plc_arduino/libraries/OpenPLC_IAP/src/iap_keyderive.c` | 2 | 0 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `open_plc_arduino/libraries/OpenPLC_IAP/src/iap_keyderive.h` | 12 | 0 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `open_plc_arduino/libraries/OpenPLC_IAP/src/owner_root_ro.c` | 18 | 1 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `open_plc_arduino/libraries/OpenPLC_IAP/src/owner_root_ro.h` | 26 | 1 | `docs/security/`，逐条见 BATCH-LEDGER |
| 3–5 | `open_plc_arduino/libraries/OpenPLC_IAP/src/udp_server.c` | 48 | 5 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_arduino/libraries/OpenPLC_Net/src/OpenPLC_Net_Autostart.h` | 3 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_arduino/libraries/OpenPLC_Net/src/ethernetif.c` | 149 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_arduino/libraries/OpenPLC_Net/src/ethernetif.h` | 9 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_arduino/libraries/OpenPLC_Net/src/openplc_lwip_force_sources.c` | 38 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_arduino/libraries/OpenPLC_Net/src/openplc_net_port.c` | 21 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_arduino/tools/discovery/iface_darwin.go` | 6 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_arduino/tools/discovery/iface_linux.go` | 5 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_arduino/tools/discovery/iface_windows.go` | 10 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_arduino/tools/discovery/network_discovery.go` | 27 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 1 | `open_plc_cube_ide/IAPServer/IAP_boot_handoff.c` | 47 | 3 | `docs/boot/`，逐条见 BATCH-LEDGER |
| 1 | `open_plc_cube_ide/IAPServer/IAP_boot_handoff.h` | 59 | 4 | `docs/boot/`，逐条见 BATCH-LEDGER |
| 1 | `open_plc_cube_ide/IAPServer/IAP_server.c` | 196 | 10 | `docs/boot/`，逐条见 BATCH-LEDGER |
| 1 | `open_plc_cube_ide/IAPServer/IAP_server.h` | 15 | 0 | `docs/boot/`，逐条见 BATCH-LEDGER |
| 1 | `open_plc_cube_ide/IAPServer/bootloader_state.c` | 37 | 2 | `docs/boot/`，逐条见 BATCH-LEDGER |
| 1 | `open_plc_cube_ide/IAPServer/bootloader_state.h` | 83 | 3 | `docs/boot/`，逐条见 BATCH-LEDGER |
| 2 | `open_plc_cube_ide/IAPServer/fw_pubkey.c` | 2 | 0 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `open_plc_cube_ide/IAPServer/fw_pubkey.h` | 10 | 1 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `open_plc_cube_ide/IAPServer/fw_verify.c` | 12 | 0 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `open_plc_cube_ide/IAPServer/fw_verify.h` | 17 | 1 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `open_plc_cube_ide/IAPServer/iap_auth.c` | 41 | 3 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `open_plc_cube_ide/IAPServer/iap_auth.h` | 34 | 0 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `open_plc_cube_ide/IAPServer/iap_cert.c` | 1 | 0 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `open_plc_cube_ide/IAPServer/iap_cert.h` | 36 | 1 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `open_plc_cube_ide/IAPServer/iap_keyderive.c` | 1 | 0 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `open_plc_cube_ide/IAPServer/iap_keyderive.h` | 13 | 0 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `open_plc_cube_ide/IAPServer/owner_slot.c` | 141 | 11 | `docs/security/`，逐条见 BATCH-LEDGER |
| 2 | `open_plc_cube_ide/IAPServer/owner_slot.h` | 104 | 4 | `docs/security/`，逐条见 BATCH-LEDGER |
| 1 | `open_plc_cube_ide/IAPServer/tcp_server.c` | 13 | 2 | `docs/boot/`，逐条见 BATCH-LEDGER |
| 1 | `open_plc_cube_ide/IAPServer/tcp_server.h` | 2 | 0 | `docs/boot/`，逐条见 BATCH-LEDGER |
| 1 | `open_plc_cube_ide/IAPServer/udp_server.c` | 28 | 2 | `docs/boot/`，逐条见 BATCH-LEDGER |
| 1 | `open_plc_cube_ide/IAPServer/udp_server.h` | 3 | 0 | `docs/boot/`，逐条见 BATCH-LEDGER |
| 1 | `open_plc_cube_ide/LWIP/Target/ethernetif.c` | 153 | 1 | `docs/boot/`，逐条见 BATCH-LEDGER |
| 1 | `open_plc_cube_ide/LWIP/Target/ethernetif.h` | 9 | 0 | `docs/boot/`，逐条见 BATCH-LEDGER |
| 3–5 | `open_plc_cube_ide/TestCase/ADC/adc_test.c` | 16 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/ADC/adc_test.h` | 33 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/CAN/can_test.c` | 87 | 6 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/CAN/can_test.h` | 179 | 3 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/DAC/dac_test.c` | 7 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/DAC/dac_test.h` | 29 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/DIN/din_test.c` | 4 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/DIN/din_test.h` | 15 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/ETH/eth_test.c` | 42 | 6 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/ETH/eth_test.h` | 31 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/KNX/knx_test.c` | 301 | 9 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/KNX/knx_test.h` | 224 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/PWM/pwm_test.c` | 19 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/PWM/pwm_test.h` | 14 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/RELAY/relay_test.c` | 2 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/RELAY/relay_test.h` | 30 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/RS232/rs232_test.c` | 2 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/RS232/rs232_test.h` | 13 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/RS485/rs485_test.c` | 41 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/RS485/rs485_test.h` | 20 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/SD/sd_test.c` | 101 | 5 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/SD/sd_test.h` | 82 | 5 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/SDRAM/sdram_test.c` | 75 | 5 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/SDRAM/sdram_test.h` | 95 | 4 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/common/bringup_test.c` | 7 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/common/bringup_test.h` | 22 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/common/ccsbcs.c` | 9 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/common/ff_gen_drv.c` | 33 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/common/ff_gen_drv.h` | 19 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/common/integer.h` | 10 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/common/port_adc.c` | 23 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/common/port_adc.h` | 33 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/common/port_can.c` | 18 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/common/port_can.h` | 52 | 5 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/common/port_dac.c` | 15 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/common/port_dac.h` | 32 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/common/port_din.c` | 1 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/common/port_din.h` | 16 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/common/port_dout.c` | 44 | 3 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/common/port_dout.h` | 49 | 5 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/common/port_led.c` | 2 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/common/port_led.h` | 12 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/common/port_pwm.c` | 6 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/common/port_pwm.h` | 13 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/common/port_rs485.c` | 21 | 3 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/common/port_rs485.h` | 29 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/common/port_vref.c` | 9 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/common/port_vref.h` | 14 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/common/testcase_hal_guard.h` | 39 | 3 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/porttool/porttool.c` | 127 | 12 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/porttool/porttool.h` | 158 | 9 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/porttool/porttool_ain.c` | 26 | 3 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/porttool/porttool_aout.c` | 34 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/porttool/porttool_can.c` | 111 | 7 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/porttool/porttool_cmd.c` | 13 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/porttool/porttool_cmd.h` | 23 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/porttool/porttool_din.c` | 51 | 3 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/porttool/porttool_dout.c` | 58 | 4 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/porttool/porttool_eth.c` | 79 | 7 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/porttool/porttool_knx.c` | 88 | 4 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/porttool/porttool_relay.c` | 44 | 4 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/porttool/porttool_rs232.c` | 16 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/porttool/porttool_rs485.c` | 74 | 4 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/porttool/porttool_run.c` | 115 | 6 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/porttool/porttool_run.h` | 27 | 0 | **0 段，查过没有可搬的** |
| 3–5 | `open_plc_cube_ide/TestCase/porttool/porttool_sd.c` | 27 | 2 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/porttool/porttool_sdram.c` | 41 | 4 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/porttool/porttool_temp.c` | 16 | 1 | `docs/engineering/TEST-DESIGN.md`（汇总） |
| 3–5 | `open_plc_cube_ide/TestCase/porttool/porttool_usb.c` | 92 | 8 | `docs/engineering/TEST-DESIGN.md`（汇总） |

**合计 227 个文件**：批 1 共 12、批 2 共 35、批 3–5 共 180。
与 `CORPUS.md` 的 227 行**逐文件对得上，差 0**。
