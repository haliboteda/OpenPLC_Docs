# eth 和 usb 的速率门限定多少

Type: grilling
Opened: 2026-09-16
Status: open
Blocked by: -

## Question

`$PROD/docs/tables/DECISIONS.md` 第 42 条定了「有吞吐概念的口保留速率判据 + 收发字节数」，
但**门限写的是 TBD**。没有门限，那条判据判不出任何东西。

按 DECISIONS 44，判据和限值由硬件工程师写进方案文件，我方只报数值 ——
所以这张票要定的是**问他什么、以及方案文件里这两项长什么样**。

⚠️ 同样是 2026-09-16 搬迁时被检查拦下来逼出来的。

## 怎么算答完

`DECISIONS.md` 第 42 条那一行不再写 TBD：要么填上门限，要么改成「由方案文件给出」
并指出方案文件里的字段名。`check_no_orphan_placeholders.py` 不再报它。
