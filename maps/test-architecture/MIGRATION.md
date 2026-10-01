# 迁移清单

照 [map.md](map.md) 的决定把测试搬到位。归属以 [TA-01-inventory.md](TA-01-inventory.md) 为准，动手前重跑 `python tools/classify_tests_by_layer.py`。git 历史不带：直接拷贝，提交说明写明从哪个 commit 拷来，旧历史留在原仓。

| 步 | 做什么 | 怎么算做完 |
|---|---|---|
| 1 | 文档检查 P7、P8、P9、P12、P13、P14、P18 搬进 `$PROD/tools/`，入口 `check_docs.py` | 在 `$PROD` 里 `python tools/check_docs.py` 全绿；旁边的代码仓不在时跳过并说明 |
| 2a | bootloader 的部件测试进 `$BOOT/tests/`（CMake/CTest）：T1-16、`owner_capacity`、T2-34、P16、P17 | `cmake -S tests` + `ctest` 全过；`$BOOT/.gitignore` 忽略构建目录 |
| 2b | 板卡包的部件测试进 `open_plc_arduino/tests/`：P3、P4、P5、P15、P19、T2-21 | 每项一条命令跑通；写明是测仓里那份还是 `$CORE_LIVE` |
| 2c | IAPTool 只留自己的单元测试（T1-15、T1-35）和 T1-19/T1-20；`internal/iapproto`、`internal/netiface` 改成公开包供 `$TEST` 引用 | `go test ./...` 全过；仓里不再有 `TestCase/` |
| 3 | 其余进 `$TEST`：`TestCase.exe`、上板脚本、假板子与 T1-18 / T1-34、Renode、板上 sketch、契约检查 P1 / P2 / P11 与三方校准值区核对、黄金向量比对、P10、本机配置与基础设施、`Output/` 里的密钥和探针镜像 | `$TEST` 的自检全绿；`Output/five-paths-keys/` 在新位置能签名后才删旧的 |
| 4 | 清空 `$TOOL/TestCase/`；改所有文档里的路径；`ACCEPTANCE-CHECKLIST.md` 每项写明哪个仓的哪条命令 | 五个仓的自检和 `check_docs.py` 全绿；P9 不报断路径 |
| 5 | 真代码替身替掉假板子的 bootloader 那一半，含 T1-18c 拦截、板卡包 app 侧握手、`$BOOT` 的 `jump_to_app` 主机开关 | T1-18a–g、T1-34 在替身上全过 |
