# 测试按部件、契约、整机三层重新分布

## 怎么看进度（不用问任何人）

```
python tools/list_wayfinder_map_frontier.py --all
```

## Destination

测试按思路 C 重新分布，每一项现有测试都有去处：部件仓（bootloader、IAPTool、板卡包、PortTool）只用各自语言自带的工具测自己；`OpenPLC_Test`（`$TEST`）独有 Python 基础设施，只装契约测试和整机测试；文档检查归 `$PROD`；每个仓都有一个不靠别的仓的自检入口。终点是一份能照着搬的迁移清单。

## Notes

- **2026-10-02 起带执行**：用户把剩下的票一次定完，照 [MIGRATION.md](MIGRATION.md) 搬
- 已定的前提：[决策 78](../../docs/tables/DECISIONS.md)（三层与判据）、[决策 76](../../docs/tables/DECISIONS.md)（仓与仓彻底分离）、[决策 77](../../docs/tables/DECISIONS.md)（同一功能只留一份）
- 术语：部件测试 / 契约测试 / 整机测试，见 [GLOSSARY.md](../../GLOSSARY.md)。不用 `CONTEXT.md` / `docs/adr/`
- grilling 票要用户在场，AI 不自问自答
- 开票 / 关票 / 算前沿照 [图与票的约定](../MAP-AND-TICKET-CONVENTION.md)

## 全集

要找的是「所有在测试或检查东西的文件」：

```
for r in IAPTranfer_Tool OpenPLC_PortsTestingTool open_plc_cube_ide open_plc_arduino OpenPLC_Docs; do
  git -C $r ls-files -co --exclude-standard | grep -iE '(^|/)(TestCase|tests?|host|onboard)/|_test\.(go|c|py)$|(^|/)(check_|run_|selfcheck)[^/]*\.py$' | sed "s#^#$r/#"
done
git -C OpenPLC_Test ls-files -co --exclude-standard | sed "s#^#OpenPLC_Test/#"   # 这个仓里全是测试
```

逐个文件的归属由 `python tools/classify_tests_by_layer.py` 重新生成进 [TA-01-inventory.md](TA-01-inventory.md)。

## Decisions so far

- [只需要一个仓、但必须上真板子的测试归哪](issues/TA-02-where-do-single-repo-on-board-tests-go.md)：要真硬件的一律归 `$TEST` 整机层，T4-03 例外留在 `$PORTTOOL`
- [板卡包仓的测试怎么跑](issues/TA-05-how-are-board-package-tests-run.md)：`open_plc_arduino/tests/`，薄 Python 脚本 + T2-21 用 CMake，不要本机配置
- [部件仓要不要本机配置](issues/TA-07-do-component-repos-need-machine-config.md)：只有 PortTool 和 `$TEST` 要
- [文档检查搬进 OpenPLC_Docs 后长什么样](issues/TA-08-what-do-doc-checks-look-like-in-prod.md)：原样搬进 `$PROD/tools/`，入口 `check_docs.py`，编号不改
- [发版之前要跑什么](issues/TA-09-what-runs-before-a-release.md)：自己仓的自检 + `$TEST` 全部契约 + 相关整机项 + 文档检查
- [两个仓都要用的测试桩怎么办](issues/TA-11-test-stubs-two-repos-need.md)：替本仓代码的桩归本仓，可以重复
- [黄金向量由谁更新](issues/TA-12-who-updates-the-golden-vectors.md)：`$TEST` 只比对、不写
- [真 bootloader 替身覆盖不到的几例怎么办](issues/TA-13-what-the-real-bootloader-stand-in-cannot-cover.md)：T1-18c 原定在替身外拦一句，2026-10-03 按决策 79 作废；app 侧握手把板卡包代码编进替身；`jump_to_app` 加主机开关
- [依赖固件源码的 PortTool 测试归哪](issues/TA-10-where-do-porttool-tests-that-build-firmware-go.md)：工装算一个部件、源码跨两个仓，T4-01 到 T4-03 和模拟板留在 `$PORTTOOL`；校准值区核对合进 `$TEST` 契约层，一次比三方
- [每一项现有测试归哪一层、哪个仓](issues/TA-01-which-layer-and-repo-does-each-test-belong-to.md)：330 个文件逐个归位，部件 91、`$TEST` 52、文档检查 8、待定 8，表在 [TA-01-inventory.md](TA-01-inventory.md)
- [bootloader 的 C 单元测试用什么驱动](issues/TA-04-how-are-bootloader-c-unit-tests-driven.md)：`$BOOT/tests/` 下独立的 CMake 工程，用 CTest 跑，不挂到顶层 `CMakeLists.txt`；三组测试已在临时目录跑通
- [IAPTool 测试用的假板子：换成真 bootloader 代码，还是留着手写](issues/TA-06-should-the-fake-board-become-real-bootloader-code.md)：推荐把 `$BOOT/IAPServer` 的真代码编成 PC 替身替掉假板子的 bootloader 那一半；读代码已发现假板子和真 bootloader 有 6 处不一致
- [整体测试项目叫什么、放在哪](issues/TA-03-where-does-the-integration-project-live.md)：新仓 `OpenPLC_Test`，路径变量 `$TEST`；`IAPTranfer_Tool` 不改名

## Not yet specified

没有了。搬的顺序和 git 历史写在 [MIGRATION.md](MIGRATION.md)。`$BOOT/TestCase/` 里编进固件的板上自测是固件本身，不动（见归属表）。

## Out of scope

- 改任何一条测试的判据或内容：这张图只管测试住在哪、由谁跑
- 自动化服务器、CI：现在没有这个需求
