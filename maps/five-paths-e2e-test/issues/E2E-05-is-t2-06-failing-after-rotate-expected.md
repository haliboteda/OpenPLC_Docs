# 路径三换根之后 `T2-06` 必然失败，算不算

Type: grilling
Opened: 2026-09-20
Status: resolved
Blocked by: -

## Question

用例 `T2-06`（**「信任公开根」的告警不能失灵**）查的是一个常量：bootloader 认出那把公开根，
靠的是编进 `owner_slot.c` 的一份 **SHA-256 指纹**。`tools/check_public_root.py` 比对它还对不对。

路径 ③（自己生成证书、重烧 bootloader）要跑 `rotate_keys.sh` 换掉编译进去的根。
**换完之后那份指纹常量必然指向旧 key** —— `rotate_keys.sh` 自己的注释写明了这个代价。

于是路径 ③ 跑完，`T2-06` 会失败。**今天没有任何文档说这个失败算什么。** 三种可能：

| | 结论 | 后果 |
|---|---|---|
| **算预期** | 客户自己编译就是会这样，`T2-06` 只对**厂商出货的那份 bootloader** 有意义 | 要写清 `T2-06` 的适用范围，并且路径 ③ 里显式跳过它 |
| **算失败** | 换根之后指纹应该跟着更新 | `rotate_keys.sh` 要顺手改那个常量，或者换一种认公开根的办法 |
| **两者都不对** | 认公开根的机制本身要改 | —— |

⚠️ **这条不解决，路径 ③ 跑出来的红色结果没人能判断是真问题还是设计如此** ——
而一个「本来就会红」的用例混在结果里，会训练人忽略红色。

## 怎么算答完

三选一有明确结论，并写进 `M2-ownership.md` 的 `T2-06` 那一行（或它的脚注）：
**`T2-06` 在什么前提下有意义、什么前提下必然失败且该被跳过。**

判据要能判真假 —— 比如「路径 ③ 跑完，`check_public_root.py` 退出码非零，
而路径脚本把它记为 SKIPPED 并打出理由」这种。

## Answer

2026-09-20 定。**算预期。路径 ③ 必须显式把它记成 SKIPPED 并打出理由，不能让它红着。**

### 依据不是推理，是工具自己写的

`check_public_root.py`（决策 72 取消公开根后已删） 的文件头注释原文：

> That fingerprint is a CONSTANT on purpose. Deriving it from fw_pubkey.inc at build time would
> make the comparison true for every build, so the warning would also fire on a customer board
> built with the customer's own key -- and a warning everyone learns to ignore protects nobody.
>
> **In a customer's fork the two are SUPPOSED to differ** -- that is what having their own root
> means. **This check belongs to this repository, where the default key is by definition the
> published one.**

所以 `T2-06` 的适用范围是**这个仓库 / 厂商出货的那份 bootloader**。路径 ③ 模拟的正是
「客户用自己的根编译」，两者本来就该不一样 —— **失败是这个检查在正确工作，不是发现了问题。**

### 判据

路径 ③ 跑完时：

- `check_public_root.py` 退出码**非零**
- 而路径脚本把它记成 **SKIPPED**，并打出理由（大意：this path rotates the root on purpose;
  P6 only applies to the vendor build）
- ⚠️ **不是静默跳过** —— 要点名说跳了哪条、为什么。一个被静默略过的检查和一个没跑的检查分不开

### 现状（2026-09-20 实测）

`python tools/check_public_root.py` 退出码 **0**：

```
computed a3cbcbf79fb665df35cd14e144da9bac156b84da869b2c9f109e39def8c38bde
compiled a3cbcbf79fb665df35cd14e144da9bac156b84da869b2c9f109e39def8c38bde
the warning recognises the published root, and the build carries it
```

**仓库现在处在「公开根」状态**，路径 ③ 会把它改掉。

## 引出了什么新的未知

**一条，比本票原来的问题更要紧，已落进 [work/TODO.md](../../../work/TODO.md)：**

⚠️ **路径 ③ 会改动仓库里的文件，不只是板子。** `rotate_keys.sh` 重写
`IAPServer/keys/fw_pubkey.inc` 和 `fw_signing_key.TEST_ONLY.pem`。

好消息：脚本自带快照备份（`keys/backup/<snapshot>` + 每个文件旁边的 `.bak`）和 `--restore`，
`--list-backups` 能列。所以是可回退的。

⚠️ **但还原的时机不能想当然**：**必须放在整轮结束之后，不是路径 ③ 结束之后** ——
因为**路径 ④ 发叶证书要用那把轮换后的根私钥**。③ 之后立刻还原，④ 就没有根可以签发了。

所以整轮的收尾要有一步：`rotate_keys.sh --restore <本轮开始时记下的快照>`，
并用 `check_public_root.py` 退出码 0 验证还原成功。
