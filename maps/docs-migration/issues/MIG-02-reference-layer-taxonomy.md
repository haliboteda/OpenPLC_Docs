# 参考层按什么分类

Type: grilling
Opened: 2026-09-16
Status: resolved
Blocked by: -

## Question

参考层收「已经定死的事实和决策」。现在三个仓的 `docs/` 按**产物类型**分：`design/` `work/` `test/`。

主读者是 AI，目的是「一次读完建起系统框架」—— 按产物类型分是不是最优？
另一条路是按**问题域**分（硬件事实 / 安全与所有权 / 通信 / 产测 / 构建发版）。

这个决定挡着后面所有搬迁动作，因为不知道分类就不知道每份文件搬到哪。

## 怎么算答完

有一张分类表，能把现有 30 多份文档**每一份唯一地**归进一类，没有「不知道放哪」的，也没有一份同时属于两类。

## Answer

2026-09-16 定。分类表写成 [../../../docs/modules/](../../../docs/modules/)。

| 问 | 定成 |
|---|---|
| 准入判据 | **不会因为工作推进而变的进参考层，还在动的一律是票或图** |
| 按什么分 | **问题域**，不按产物类型。AI 要答的是「我在改 RS485 该读哪几份」 |
| 状态表 | **拆两半**：需求定义进 `tables/`；跑出来的结果不进参考层 |
| 对外文档 | **单独一类 `outbound/`** —— 判据不同：自成一体、不引内部链接、改了要重发 |
| 横跨所有域的总表 | **不拆**，单独成 `tables/`。它们的组织原则本来就是编号，硬按域切会让 `DECISIONS 44` 这类外部引用全断 |

### 验证

`怎么算答完` 要求「每一份唯一地归进一类，没有不知道放哪的，也没有一份同时属于两类」。
三个仓全部 **43 份** `.md` 逐一归位：

| 归到 | 份数 | 是哪些 |
|---|---|---|
| `hardware/` | 1 | HARDWARE-FACTS |
| `boot/` | 1 | JOURNAL ⚠️ 偏薄，见空缺 |
| `security/` | 4 | OWNERSHIP、KEYS、CROSS-CHECK、KEY-MATCH |
| `production/` | 5 | PORTTOOL-FLOW、PRODUCTION-FRAMEWORK、PROD-CONFIG-ITEMS、BOARD-BRINGUP-CASES、PORTTOOL-CAPS-TEST |
| `build/` | 5 | CUBEMX-RULES、BUILD-AND-TEST、RTC-LSE-CHANGE、OpenPLC_Bootloader、HOST-C-TESTS |
| `repo/` | 6 | ARCHITECTURE、CONVENTIONS、CONSTRAINTS、WRAP-UP、OVERVIEW、docs/INDEX |
| `outbound/` | 5 | FIXTURE-INTERFACE、AIN-JUMPER-REQUEST、PROD-DOC-REVIEW、RELEASE-NOTES |
| `tables/` | 5 | DECISIONS、DEFERRED-DESIGNS、TEST-CASES、checklist、ID-MAP、STATUS 的需求那半 |
| **不进参考层 → 是票或图** | 6 | PRODUCTION-TEST-GAP、PORT-BRINGUP-PLAN、PORTTOOL-FIRST-BENCH、DO-PWM-SCOPE-STEPS、BACKLOG、ISSUES |
| **留在原仓当入口** | 5 | 四个仓的 `CLAUDE.md` 和 `README.md` |

没有一份归不进去，也没有一份落进两类。判据在 6 份「还在动的」上直接生效，
不用一份份争 —— 它们记的都是「还没完的事」。

⚠️ **给 `三十多份文件逐份定去向` 那张票的两条**（这张不越界，只记下）：
`WRAP-UP.md` 的归位表和新的关票流程有重叠，要逐条对；
`STATUS.md` 要真的劈成两个文件，不是标一下。

## 引出了什么新的未知

1. **IAP 协议在参考层没有独立文档。** `boot/` 只有一份 journal 设计 ——
   这个产品的核心协议一直只活在代码注释和决策条目里。**这是真空缺，不是分类没分好。**
2. **`STATUS.md` 的「最近结果」判定为「该由脚本生成」，但那个生成器不存在。**
   现在是手抄的，这就是它三个数字对不上的原因。
