# 测试按部件、契约、整机三层重新分布

## 怎么看进度（不用问任何人）

```
python tools/list_wayfinder_map_frontier.py --all
```

## Destination

测试按思路 C 重新分布，每一项现有测试都有去处：部件仓（bootloader、IAPTool、板卡包、PortTool）只用各自语言自带的工具测自己；`OpenPLC_Test`（`$TEST`）独有 Python 基础设施，只装契约测试和整机测试；文档检查归 `$PROD`；每个仓都有一个不靠别的仓的自检入口。终点是一份能照着搬的迁移清单。

## Notes

- **这张图只做决定，不带执行**：票全关之后照迁移清单搬。四个仓一起动，前面的决定会改后面怎么搬
- 已定的前提：[决策 78](../../docs/tables/DECISIONS.md)（三层与判据）、[决策 76](../../docs/tables/DECISIONS.md)（仓与仓彻底分离）、[决策 77](../../docs/tables/DECISIONS.md)（同一功能只留一份）
- 术语：部件测试 / 契约测试 / 整机测试，见 [GLOSSARY.md](../../GLOSSARY.md)。不用 `CONTEXT.md` / `docs/adr/`
- grilling 票要用户在场，AI 不自问自答
- 开票 / 关票 / 算前沿照 [图与票的约定](../MAP-AND-TICKET-CONVENTION.md)

## 全集

要找的是「所有在测试或检查东西的文件」：

```
for r in IAPTranfer_Tool OpenPLC_PortsTestingTool open_plc_cube_ide open_plc_arduino OpenPLC_Docs; do
  git -C $r ls-files | grep -iE '(^|/)(TestCase|tests?|host|onboard)/|_test\.(go|c|py)$|(^|/)(check_|run_|selfcheck)[^/]*\.py$' | sed "s#^#$r/#"
done
```

## Decisions so far

- [整体测试项目叫什么、放在哪](issues/TA-03-where-does-the-integration-project-live.md)：新仓 `OpenPLC_Test`，路径变量 `$TEST`；`IAPTranfer_Tool` 不改名

## Not yet specified

- **搬迁的顺序和 git 历史怎么带**：要等归属表和各仓的跑法定了才说得清
- **`$BOOT/TestCase/` 里编进固件的板上测试**（ADC、CAN、RS485……）算哪层：它们是固件的一部分，可能不用动

## Out of scope

- 改任何一条测试的判据或内容：这张图只管测试住在哪、由谁跑
- 自动化服务器、CI：现在没有这个需求
