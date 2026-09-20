# 第二次撤销写得进去但不生效

Type: grilling
Opened: 2026-09-20
Status: resolved
Blocked by: -

## Question

**一块板今天只能撤销一次。** 第二次及以后的每一次都会写进一条记录、**烧掉一个不可回收的槽**，
然后不生效 —— 板子自己的回读确认会发现并回 `Refused`，所以不会静默出错，但那个槽回不来了。

2026-09-20 真板子实测（generation 1，已撤一个叶，再撤第二个）：

```
** revoke wrote a record but it did not take effect - see the boot log **
```

复位后的启动日志：

```
Owner slot: 4 record(s), latest generation 2      ← 1 条 'O' + 3 条 'R'，三条 R 都是 generation 2
Owner slot: claimed at generation 1               ← 生效记录不动，这是设计
Owner slot: 47/51 slot(s) free, 1 leaf(s) revoked ← 只有第一条 R 生效；两次失败各烧一个槽
```

**根因是两个条件互相矛盾**，都在 `$BOOT/IAPServer/owner_slot.c`：

| 在哪 | 要求 |
|---|---|
| `owner_slot_revoke()` 开头 | `generation == s_effective->generation + 1`。而 `s_effective` 是 **`'O'` 记录**，撤销永不改它 —— 所以每次撤销算出来的都是同一个数 |
| `resolve_chain()`（第 205 行 `if (!first && (r->generation <= last_gen)) continue;`） | 链上 generation **严格递增**，`'R'` 记录也走这条路 |

第一次撤销用掉了 generation 2，第二次算出来还是 2，于是**写得进 flash、却在行走时被跳过**。

⚠️ **这不是工具的问题。** `$TOOL/owner.go` 的 `RunRevoke()` 按板子的规则算 `next = gen + 1`，
板子的规则本身自相矛盾。

### 候选

| | 做法 | 要想清楚什么 |
|---|---|---|
| ① | `owner_slot_revoke()` 改成要求「比链上**最大** generation 大 1」，不是「比生效记录大 1」 | generation 递增是防重放的机制 —— 改判据之前要确认它还挡得住重放 |
| ② | `'R'` 记录不参与 generation 递增检查（`resolve_chain()` 对 R 记录跳过那一条） | 那 `'R'` 记录靠什么防重放？签名覆盖 `uid`，但同一块板上重放同一条 R 记录仍然成立 —— 不过重放一条**撤销**记录的收益是什么，值得单独想 |
| ③ | 一条 `'R'` 记录装满 4 个名字再写（批量） | **治标** —— 第 5 个叶照样撞上同一堵墙 |

## 怎么算答完

1. 定下 `'R'` 记录的 generation 语义，写进 [M2 归属与信任](../../../docs/modules/M2-ownership.md)
2. **有一条用例证明能连续撤销两个不同的叶，且两个都生效** —— 今天没有任何用例覆盖第二次撤销，
   所以这个缺陷躲过了 `T2-15`–`T2-18` 全绿
3. 说清**已经写进去的废记录**怎么办：留着（占槽但无害），还是压缩时清掉
   （压缩在 [撤销叶证书 + bootloader 原地升级](../map.md) 的原地升级那半边）


## Answer

2026-09-20 定。**`'R'` 记录退出链的行走，改成独立一趟扫描** —— 修法由决策 59 定下，
不是三个候选里的任何一个：病根是 `'R'` 借了为 `'O'` 设计的 generation，而它压根不需要一个链上位置。

具体：`resolve_chain()` 选记录时跳过 `'R'`；链走完之后单独扫一遍 `'R'`，只查结构和 `uid`，
不验签、不看 generation；`owner_slot_revoke()` 去掉 generation 规则，记录里那 4 字节固定写 0；
线上命令变成 `revoke <prefix> <sig>`。**跨仓镜像 `owner_root_ro.c` 同步改了** ——
不改的话 app 和 bootloader 会对「哪些叶还有效」给出不同答案。

**真板子验收通过**（用例 `T2-19` / `T2-20`）：作废计数 **7 → 8**，第二个叶生效；
重复作废同一个叶回 `OK already revoked` 且 **`no slot was spent (42 free, unchanged)`**。
最硬的旁证是累积账：槽位 50 → 42，**八次作废各消耗一个槽，一次浪费都没有** ——
修复前每次失败的尝试都会白烧一个不可回收的槽，这个账根本对不上。

## 引出了什么新的未知

**一条**：验证过程中发现**有些叶证书驱动不了重启握手** —— 同一把根签发、同一次启动周期内，
一张能把板子请回 bootloader、另一张不能。**不是本次改动引入的**（第一次观察在改 core 之前）。
已单独开票：[有些叶证书驱动不了重启握手](OWN-08-some-leaf-certs-cannot-drive-the-reboot-handshake.md)。
作废那套用例已改用**根密钥自签**把板子请回 bootloader，不受它阻塞。
