# 迁移清单

照 [map.md](map.md) 的决定把测试搬到位。归属以 [TA-01-inventory.md](TA-01-inventory.md) 为准，动手前重跑 `python tools/classify_tests_by_layer.py`。git 历史不带：直接拷贝，提交说明写明从哪个 commit 拷来，旧历史留在原仓。

| 步 | 做什么 | 怎么算做完 |
|---|---|---|
| 1 | 文档检查 P7、P8、P9、P12、P13、P14、P18 搬进 `$PROD/tools/`，入口 `check_docs.py` | 在 `$PROD` 里 `python tools/check_docs.py` 全绿；旁边的代码仓不在时跳过并说明 |
| 2a | bootloader 的部件测试进 `$BOOT/tests/`（CMake/CTest）：T1-16、`owner_capacity`、T2-34、P16、P17 | `cmake -S tests` + `ctest` 全过；`$BOOT/.gitignore` 忽略构建目录 |
| 2b | 板卡包的部件测试进 `open_plc_arduino/tests/`：P3、P4、P5、P15、P19、T2-21 | 每项一条命令跑通；写明是测仓里那份还是 `$CORE_LIVE` |
| 2c | IAPTool 只留自己的单元测试（T1-15、T1-35）和 T1-19/T1-20，放进本仓 `tests/`，入口 `tests/selfcheck.py`；发版工具 `install_tool.py` 放 `tools/`，按平台默认位置找 Arduino15；`internal/iapproto`、`internal/netiface` 改成公开包供 `$TEST` 引用 | `go test ./...` 全过；仓里不再有 `TestCase/` |
| 3 | 其余进 `$TEST`：`TestCase.exe`、上板脚本、假板子与 T1-18 / T1-34、Renode、板上 sketch、契约检查 P1 / P2 / P11 与三方校准值区核对、黄金向量比对、P10、本机配置与基础设施、`Output/` 里的密钥和探针镜像 | `$TEST` 的自检全绿；`Output/five-paths-keys/` 在新位置能签名后才删旧的 |
| 4 | 清空 `$TEST`；改所有文档里的路径；`ACCEPTANCE-CHECKLIST.md` 每项写明哪个仓的哪条命令 | 五个仓的自检和 `check_docs.py` 全绿；P9 不报断路径 |
| 5 | 真代码替身替掉假板子的 bootloader 那一半，含 T1-18c 拦截（2026-10-03 按决策 79 删掉）、板卡包 app 侧握手、`$BOOT` 的 `jump_to_app` 主机开关 | T1-18a–g、T1-34 在替身上全过 |

## 进度

| 步 | 状态 |
|---|---|
| 1 | ✅ 2026-10-02：`$PROD/tools/check_docs.py` 8 项全过，和原 selfcheck 的 P7–P18 逐项一致 |
| 2a | ✅ 2026-10-02：`$BOOT/tests` 的 CTest 34 项全过，场景数和原 `build.py` 一致 |
| 2b | ✅ 2026-10-02：`open_plc_arduino/tests` 快速项全过。⚠️ P4、P5、P15 测的是 `$CORE_LIVE`：`platform.txt` 的版本号 `0.1.0rc0` arduino-cli 不认，仓库目录当不了板卡包 |
| 2c | ✅ 2026-10-02：公开包 `iapproto/`、`netiface/`；T1-15、T1-19/T1-20 进 `tests/`，入口 `tests/selfcheck.py`；`install_tool.py` 进 `tools/`，按平台默认位置找 Arduino15 |
| 3 | ✅ 2026-10-02：`$TEST` 自检 7 过 1 跳（T3-05：`$BOOT/Debug/` 现在是工装镜像）。`Output/` 90 个文件 sha256 一致，那把密钥在新位置签名成功，旧的未删 |
| 4 | ✅ 2026-10-02：`$TOOL/TestCase/` 已删（105 个文件逐个在新位置核过；`gen_vectors.py` 改写成 `$TEST` 的 P20）；`Output/` 里 90 个测试资产再核 sha256 后删除，那把密钥在新位置签名通过；文档路径全部改到新位置，`ACCEPTANCE-CHECKLIST.md` 每项写明哪个仓的哪条命令；PortTool 的 CALAREA、DOCS 两步删掉（已被 `$TEST` 的 P2、`$PROD` 的 P9 取代） |
| 5 | ✅ 2026-10-02：替身在 `$TEST/host/bootstand`，T1-18a–g（含 T2-28–T2-30）10 例、T1-34 3 例在替身上全过，`fake_board.py` 已删；`$BOOT` 的 `jump_to_app` 加了主机开关，固件字节不变。落地和设计的两处差异待用户确认，见 [BOOTLOADER-STAND-IN.md](../../docs/engineering/BOOTLOADER-STAND-IN.md)「怎么跑」 |
