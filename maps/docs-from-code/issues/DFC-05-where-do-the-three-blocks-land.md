# 设计、需求、测试三大块落进参考层的哪里

Type: grilling
Opened: 2026-09-16
Status: resolved
Blocked by: DFC-01

## Question

用户要的是「按这几大块整理好」，但参考层现在是**按问题域**分的八类
（hardware / boot / security / production / build / repo / outbound / tables）。

「需求」已经有 `tables/STATUS.md`，「测试」已经有 `tables/TEST-CASES.md`，
「设计」散在 `tables/DECISIONS.md` 和各个域里。**三大块和八类不是一一对应。**

要定：是给三大块新开位置，还是把提取出来的东西并进现有的八类。

## 怎么算答完


拿 `DFC-01` 判定要搬走的那些注释，每一条都能指出唯一一个落点，
没有「既像设计又像测试」的悬空项。
## Answer

2026-09-16 定。**不给三大块新开位置，并进现有八类。** 这是做完两批之后得出的，不是先想好的。

| 用户说的「块」 | 实际落点 |
|---|---|
| **设计** | 按**问题域**进八类：启动那套 → `docs/modules/M1/BOOT-SEQUENCE.md`，安全那套 → `docs/modules/M1/CHALLENGE-AUTH.md`，各自补进该域已有的文档 |
| **需求** | `docs/tables/STATUS.md`，**已经在那儿**，不动 |
| **测试** | 判据继续在 `docs/engineering/HOW-TO-RUN-TESTS.md`；**测试系统本身怎么搭的** → 新建 `docs/engineering/TEST-DESIGN.md`（用户当天定批 3–5 汇总进一份测试设计文档） |

**为什么不新开**：八类是按「我在改 RS485，该读哪几份」分的；
「设计 / 需求 / 测试」是按**产物类型**分的 —— 那正是 `参考层按什么分类` 那张票否掉的分法。
两套并存会让每份文档同时属于两个位置。

### 验证

判据是「`DFC-01` 判定要搬走的那些注释，每一条都能指出唯一一个落点，没有悬空项」。
两批实做下来：

| 批 | 文件 | 落点 | 悬空 |
|---|---|---|---|
| boot | 12 / 12 | `docs/boot/`（+ 一条进 `JOURNAL.md`） | 0 |
| security | 35 / 35 | `docs/security/`（+ 7 条进 `OWNERSHIP.md`） | 0 |
| 3–5 汇总 | 125 个文件的 482 段 | `docs/engineering/TEST-DESIGN.md` | 0 |

**没有一条同时像两个落点。** 逐文件记录在 `../BATCH-LEDGER.md`。

## 引出了什么新的未知

没有。这一票的答案是被前两批的实做逼出来的，不是设计出来的。
