# bootloader 的 C 单元测试用什么驱动

Type: research
Opened: 2026-10-02
Status: resolved
Blocked by: -

## Question

现在四组主机 C 测试（`bootloader_unit`、`owner_revoke`、`owner_capacity`、`sector15_reclaim`）由 Python 的 `build.py` 驱动。`$BOOT` 已有 `CMakeLists.txt` 和 `CMakePresets.json`：用 CMake + CTest 在 PC 上编这些测试可不可行，会不会和 CubeIDE 的固件构建、CubeMX 重新生成冲突；不行时 Makefile 的代价是什么。还要查清 `gen_vectors.py`（调 IAPTool 生成黄金向量）和这些测试的关系。

## 怎么算答完

给出推荐做法和理由；写明在 Windows 和 Linux 上各要装什么；写明和 `docs/build/CUBEMX-RULES.md` 的规则冲不冲突；有一个最小的可行性证据（例如一组测试用 CMake 编过并跑过）。

## Answer

2026-10-02 定（research，待用户确认推荐）

**推荐：`$BOOT/tests/` 下放一个独立的 CMake 工程（`cmake -S tests`），用 CTest 跑；不碰顶层 `CMakeLists.txt`。**

| 结论 | 理由 |
|---|---|
| CMake + CTest 可行 | 三组 `$BOOT` 测试在本机用 CMake 编过、32 条 CTest 全过（证据见下） |
| 必须是独立工程，不能被顶层 `add_subdirectory` | 顶层 `CMakeLists.txt` 在 `project()` 前写死 `arm-none-eabi-gcc`，挂进去就成了交叉编译 |
| 不和 CubeIDE 固件构建冲突 | `.cproject` 的 `sourceEntries` 只列 `IAPServer Core TestCase Middlewares LWIP Drivers USB_DEVICE` 七个目录，新的 `tests/` 不进 `Debug/makefile`。⚠️ 所以**不能放进 `TestCase/`**，那个目录会被编进固件 |
| 不和 CubeMX 重新生成冲突 | `.ioc` 是 `TargetToolchain=STM32CubeIDE`，CubeMX 不写 CMake 文件，也不会碰它没生成过的 `tests/`；没在真实重新生成里验过 |
| 不和 [CUBEMX-RULES.md](../../../docs/build/CUBEMX-RULES.md) 冲突 | 那份管的是生成区、`.cproject` 链接脚本选项、`.settings/` 那个文件，这套测试一样都不碰 |
| `$BOOT` 现有的 CMake 文件是没人用的残留 | 顶层 `CMakeLists.txt` 由 `CMakeLists_template.txt` 填出来（`${templateWarning}` 是 CLion 模板的占位符，没查官方文档核实），`cmake/stm32cubemx/` + `CMakePresets.json` 是 CubeMX CMake 工具链的产物，两者互不引用，都是 2025-07-23 那次提交进来的 |
| Makefile 也行，但不如 CMake | 单编 3 个可执行文件很简单；但 `sector15_reclaim` 的 24 个多进程场景、按名字筛选（`-R`）、并行时各用各的工作目录，在 Makefile 里都得写 shell，而 Windows 上 `mingw32-make` 和 Linux 的 shell 不一样 |
| 要装什么 | Windows：MinGW-w64 的 `gcc` + `cmake`（本机 `D:\Soft\mingw64\bin` 里都有：gcc 16.1.0、cmake 4.4.1、ninja 1.13.2、mingw32-make 4.4.1）；Linux：`gcc` + `cmake`（Debian 上 `apt install gcc cmake`，**没在 Linux 上跑过**） |
| `golden_vectors.h` 留在 `$BOOT`，`gen_vectors.py` 不留 | 头文件只是 T1-16 编译要的数据，只用一个仓；生成它要调 `$TOOL` 出货的 `IAPTool`，按[决策 78](../../../docs/tables/DECISIONS.md) 的判据（要两个仓）归契约层 |
| `owner_revoke` 不该进 `$BOOT` | 它的 `build.py` 编的是 `$CORE_REPO/libraries/OpenPLC_IAP/src/owner_root_ro.c`（T2-21：在用的根不能吊销自己），不是 bootloader 源码，按决策 78 回板卡包仓 |

**证据**（Windows，本机 MinGW-w64 gcc 16.1.0，只读引用真实的 `$BOOT/IAPServer/*.c`）：

- 位置：[E:\tmp\ta04-cmake-poc](file:///E:/tmp/ta04-cmake-poc)，`tests/CMakeLists.txt` + `tests/run_steps.cmake`，测试源和 stubs 从 `IAPTranfer_Tool/TestCase/host/` 复制，编译参数照抄各 `build.py`
- 覆盖：`bootloader_unit`（T1-16：证书/认证核心）、`owner_capacity`（T2-22/23 段满告警与拒写、T1-33 compact、T2-24 wipe、T2-31/32/33，7 个阶段组）、`sector15_reclaim`（T2-34：七步回收每步断电 × 三种下次启动，24 个场景）；用例定义见 [HOW-TO-RUN-TESTS.md](../../../docs/engineering/HOW-TO-RUN-TESTS.md)、[M1-firmware-upgrade.md](../../../docs/modules/M1-firmware-upgrade.md)、[M2-ownership.md](../../../docs/modules/M2-ownership.md)
- `cmake -S tests -B build -G Ninja -DBOOT_ROOT=E:/WorkSpace/Schaeffer-AG/open_plc_cube_ide && cmake --build build && ctest --test-dir build -j8` → `100% tests passed out of 32`，5.3 秒；换 `-G "MinGW Makefiles"` 同样 32/32
- 反例：手工跑一个预期错的场景（`cut 3 | battery-dead | boot 1 1`）→ 测试程序打 `[FAIL]`，`run_steps.cmake` 退出码 1，CTest 会判失败

**测不到什么**：Linux 没跑（本机 WSL Debian 里没有 gcc 和 cmake，没装）；没做真实的 CubeMX 重新生成；没把这些输出和 `build.py` 的输出逐字节比对，只保证文件列表和编译参数相同。

## 引出了什么新的未知

- **共用的 `iap_keyderive_stub.c` 怎么分**：它现在住在 `owner_revoke/stubs/`，被 `owner_capacity`、`sector15_reclaim` 共用；`owner_revoke` 回板卡包仓之后，`$BOOT` 和板卡包仓各要一份，和[决策 77](../../../docs/tables/DECISIONS.md)（同一功能只留一份）、[决策 76](../../../docs/tables/DECISIONS.md)（仓与仓彻底分离）怎么取舍要定
- **`gen_vectors.py` 搬去 `$TEST` 之后怎么更新 `$BOOT` 里的 `golden_vectors.h`**：是跨仓写文件，还是只比对、不一致就报错，要定
- **本机编译器路径从哪来**：`build.py` 读 `config/machine.py` 的 `HOST_CC`（刻意不在 PATH 上）；换成 CMake 后是用 gitignored 的 `CMakeUserPresets.json` 还是命令行传 `-DCMAKE_C_COMPILER`，要定。顺带：`$BOOT/.gitignore` 没忽略 `build/`，搬的时候要加
- **`selfcheck.py` 现在按阶段组调 `build.py`**（`IAPTranfer_Tool/TestCase/tools/selfcheck.py:254-304`），搬完后谁来调 `ctest`、用什么名字，要和[每一项现有测试归哪一层、哪个仓](TA-01-which-layer-and-repo-does-each-test-belong-to.md)的结果对齐
