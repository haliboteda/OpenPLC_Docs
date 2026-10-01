# bootloader 的 C 单元测试用什么驱动

Type: research
Opened: 2026-10-02
Status: open
Blocked by: -

## Question

现在四组主机 C 测试（`bootloader_unit`、`owner_revoke`、`owner_capacity`、`sector15_reclaim`）由 Python 的 `build.py` 驱动。`$BOOT` 已有 `CMakeLists.txt` 和 `CMakePresets.json`：用 CMake + CTest 在 PC 上编这些测试可不可行，会不会和 CubeIDE 的固件构建、CubeMX 重新生成冲突；不行时 Makefile 的代价是什么。还要查清 `gen_vectors.py`（调 IAPTool 生成黄金向量）和这些测试的关系。

## 怎么算答完

给出推荐做法和理由；写明在 Windows 和 Linux 上各要装什么；写明和 `docs/build/CUBEMX-RULES.md` 的规则冲不冲突；有一个最小的可行性证据（例如一组测试用 CMake 编过并跑过）。
