# 恢复出厂之后 takeown 被工具拦下，因为线上没法表达「已清空」

Type: grilling
Opened: 2026-09-21
Status: open
Blocked by: -

## Question

**恢复出厂之后板子重新认领不了 —— 拦住它的是 `IAPTool`，不是板子。**

2026-09-21 真板子实测：按 BOOT0 十秒做完恢复出厂，`getowner` 回
「Claimed at generation 5」、信任密钥是随项目发布的公开根，然后 `takeown` 直接被拒：

```
[FATAL] This board is already claimed (generation 5, key 61836388e974ef4c...).
Use setowner with the current owner's key to hand it over.
```

**命令根本没发到板子上。**

### 板子那边是对的

`$BOOT/IAPServer/owner_slot.c` 的 `owner_slot_claim()` 明确允许这种情况：

> Claimable when nothing is in force, **or when the last thing in force is a factory reset**

### 病根是线上的契约

`$TOOL/owner.go:10` 写着：

> `getowner` — generation of the record in force, **0 = unclaimed**

`RunTakeOwn()`（`owner.go:201`）据此判断：`gen != 0` 就算已认领。而**恢复出厂写的是一条
带 `OWNER_FLAG_CLEARED` 的记录，generation 照常递增**（这次是 5），于是 `getowner` 回 5。

⇒ **`0 = unclaimed` 这个约定只对「从没被认领过」的板子成立**，对「清空过」的板子不成立，
而线上没有任何字段能说出这个区别。

⚠️ 同一个病根还让 `getowner` 的输出本身有误导：一块刚恢复出厂的板子会被报成
「Claimed at generation 5 ... Only firmware signed by that key will start」。

### 候选

| | 做法 | 要想清楚什么 |
|---|---|---|
| ① | `getowner` 多回一个字段（cleared 标志） | 线格式要改，两边都要动；`P2`（跨仓镜像）要不要纳入 |
| ② | 已清空时 `getowner` 就回 **0** | 工具不用改，但**丢掉了 generation**，而 `setowner` 要靠它算下一条 |
| ③ | 工具不做前置判断，直接发命令、由板子拒 | 最小改动，且判据回到板子那边（符合「结果问板子要，不问工具要」）。代价是错误文案由板子给，工具的提示会变弱 |

## 怎么算答完

1. 定下 `getowner` 的线上契约，写进 [M2 归属与信任](../../../docs/modules/M2-ownership.md)
2. **`T2-05`（恢复出厂，然后能重新认领）在真板子上从头走通一次** ——
   它今天标 ✅ 但实际过不去，见下
3. 说清 `getowner` 对一块已清空的板子该怎么措辞

⚠️ **`T2-05` 的 ✅ 是错的。** 这条用例的判据就是「再 `takeown` 能成功」，
而 2026-09-21 实测走不通。已就地改成 ❌。
