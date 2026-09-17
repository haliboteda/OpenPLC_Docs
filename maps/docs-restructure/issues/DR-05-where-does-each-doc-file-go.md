# docs 下 32 份文件逐份定去处

Type: grilling
Opened: 2026-09-17
Status: resolved
Blocked by: DR-01, DR-02

## Question

`docs/` 下 **32 份 `.md` 加 1 份 `.html`**，分在 9 个子目录：
`agents`(2) `boot`(2) `build`(4) `hardware`(1) `outbound`(3)
`production`(5) `repo`(4) `security`(3) `tables`(6)。

每一份都要定去处，**一份都不许悬着**。建图时已定的三类留在模块外：
`hardware/`（引脚事实跨所有模块）、`agents/`（给 AI 看的）、`outbound/`（交给产线的）。

剩下的要逐份问：

- **`docs/tables/` 那 6 份** —— `STATUS.md` 是核心争议：它同时是需求表和状态表，
  需求搬进模块文档之后它还剩什么？`TEST-CASES.md` `ID-MAP.md` 同理
- **`docs/security/` 那 3 份** —— 内容主要属于 M2 归属与信任，
  但 `CHALLENGE-AUTH.md` 讲的会话认证是 M1 升级流程的一步。**一份文档跨两个模块怎么办**
- **`docs/boot/` `docs/repo/` `docs/build/`** —— 跨模块或纯工程，
  按建图时的判据应该进工程约束，但没逐份验证过
- **`docs/production/` 那 5 份** —— 和 M4 产线工装什么关系，
  是并进 M4 还是留在 `outbound/` 那一类（地图迷雾里记着这条）
- **哪些该直接删** —— 重组之后内容全部进了模块文档的，原文件不该留着当第二份

⚠️ **拆一份文档跨两个模块时**，判据仍然是「一个事实只有一个家」：
把事实放进它主要服务的那个模块，另一边**写指针不写拷贝**。
P8（`check_doc_dupes.py`）会抓拷贝，指针不算。

## 怎么算答完

32 份文件每一份都写明了去处（进哪个模块 / 进工程约束 / 留在模块外 / 删除），
**没有一份悬着**，用户对有争议的那几类拍过板。
并且重跑地图 `## 全集` 的命令 2，输出的每个文件都在这份去处清单里 —— 数量对得上。

## Answer

2026-09-17 定。**32 份 `.md` 加 1 份 `.html`，共 33 份，全部定了去处，一份没悬着。**

分组：留在模块外 6 · 进模块 6 · 工程约束 8 · M4 产线工装 4 · 三张总表 3 · 原地不动 2 · 删掉 2 · 搬位置 1 · 转完就删 1（html）。**6+6+8+4+3+2+2+1+1 = 33。**

判据是这张图的总口径：**不要重复、不要把同一件事分多处记载。**
一份文档只有一个家；别处要用它，写指针不写拷贝。

### 留在模块外（6）

| 文件 | 为什么不进任何模块 |
|---|---|
| `hardware/HARDWARE-FACTS.md` | 引脚事实**跨所有模块**，塞进任何一个都会被另外三个抄一份 |
| `agents/domain.md` | 给 AI 会话看的，不是产品设计 |
| `agents/issue-tracker.md` | 同上 |
| `outbound/AIN-JUMPER-REQUEST.md` | **给别人看的**（给硬件工程师的请求） |
| `outbound/FIXTURE-INTERFACE.md` | 给产线的接口清单 |
| `outbound/PROD-DOC-REVIEW.md` | 对客户文件的评审意见 |

### 进模块（6）

| 文件 | 去哪 | 一句话理由 |
|---|---|---|
| `boot/BOOT-SEQUENCE.md` | **M1** | 讲的就是 `server_decide()` 决定跑谁然后交出去 |
| `boot/JOURNAL.md` | **M1** | journal 记的是升级的 metadata 和事件 |
| `security/KEYS.md` | **M2** | `IAPServer/keys/` 是信任根的实体 |
| `security/OWNERSHIP.md` | **M2** | DR-04 已确认它是 M2 的主体，图是它的摘要版 |
| `repo/CONSTRAINTS.md` | **M3** | 「设计不能限制用户的 app」约束的正是 app 能怎么用这颗芯片 |
| `security/CHALLENGE-AUTH.md` | **M1** | 讲的是「一次命令怎么被信任」，那是升级流程里的一步；验签用的根从哪来是 M2 的事，**M2 那边写指针不写拷贝** |

### 进工程约束（8）

`build/BOOTLOADER-PROJECT-LAYOUT.md`、`build/BUILD-AND-TEST.md`、`build/CUBEMX-RULES.md`、
`build/RTC-LSE-CHANGE.md`、`repo/ARCHITECTURE.md`、`repo/CONVENTIONS.md`、
`production/TEST-DESIGN.md`、`tables/ACCEPTANCE-CHECKLIST.md`

**共同点**：它们回答「我们怎么保证板子一直做得到」，不回答「板子能做什么」。
`production/TEST-DESIGN.md` 讲测试系统怎么搭，不讲某条用例判什么 —— 判据在模块文档里。

### 进 M4 产线工装（4）

`production/BOARD-BRINGUP-CASES.md`、`production/PORTTOOL-FLOW.md`、
`production/PROD-CONFIG-ITEMS.md`、`production/PRODUCTION-FRAMEWORK.md`

M4 只有一条需求（`R4-01`）但内容量大，这四份就是它的实体。
和 `outbound/` 的分界：**这四份是我们自己怎么做，`outbound/` 三份是交给别人的东西。**

### 三张总表（3）

| 文件 | 变成什么 | 理由 |
|---|---|---|
| `tables/STATUS.md` | **只留第一节「全局，一眼看完」那 12 行汇总**，明细搬进模块文档 | 「今天能干什么、什么在挡路」**跨所有模块**，单个模块文档答不了 |
| `tables/TEST-CASES.md` | **整份并进各模块的第 4 节，这份消失** | 判据和跑法已经是模块文档测试表的两列，留着就是第二处记载 |
| `tables/ID-MAP.md` | **改成只讲「现在有哪几套编号、各住哪」**，旧→新对照交给 `ID-MIGRATION.md` | 票号 `DR-`、验收单 `CHK-`、静态检查 `P1`–`P12` 仍是独立几套，仍需要一张登记表 |

### 原地不动（2）

| 文件 | 为什么不动 |
|---|---|
| `tables/DECISIONS.md` | 48 条编号被提交信息和聊天记录大量外部引用，**明令不可重排**（`docs/agents/domain.md`）。已在地图的 `## Out of scope` 里 |
| `tables/DEFERRED-DESIGNS.md` | 推迟掉的方案和否决理由，**不属于任何模块的功能表**。`C13`/`C14` 两条作废需求要往里加，位置不变 |

### 删掉（2）

| 文件 | 理由 |
|---|---|
| `FILE-DESTINATIONS.md` | 记的是 2026-09-16 那次搬迁的去向，**这次重组后整份作废**。本节就是它的替代 |
| `REFERENCE-LAYER-TAXONOMY.md` | 定的是「参考层按问题域分」，**这次改成按模块分，等于推翻它** |

⚠️ **两份都是 git 里取得回的**。留着讲旧分类法的文档，正是这张图要消灭的「说了两套」。

### 搬位置但不改内容（1）

`repo/WRAP-UP.md` → **搬进 `agents/`**。它开头是「用户说『今天结束』不是道别，是一条指令」，
**是给 AI 的工作流程，不是产品设计**，放在 `repo/` 是分类错了。

### 转完就删（1，html）

`security/security-design.html` —— 18 张图转成 Mermaid 拆进模块文档后删除。
⚠️ **先抢救那 10 条只活在它里面的事实**（清单在 `../DR-06-findings.md`），顺序不能反。

## 引出了什么新的未知

1. **`STATUS.md` 只留那 12 行汇总之后，数字谁来更新。** 现在「7 条 ✅、1 条 🟡」这类计数
   是人手数出来的，明细搬进四份模块文档之后，**它会立刻开始漂，而且没有任何检查看得见** ——
   P7 只比对用例名单，不数状态
2. **工程约束那一层的成员定了，但按什么分节没定。** 8 份文档 + `ENG-01`–`ENG-09` 九条需求
   已经确定属于它，内部结构仍在迷雾里
