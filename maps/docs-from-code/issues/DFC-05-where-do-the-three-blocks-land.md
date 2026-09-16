# 设计、需求、测试三大块落进参考层的哪里

Type: grilling
Opened: 2026-09-16
Status: open
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