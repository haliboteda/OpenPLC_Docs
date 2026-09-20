# 升级被打断之后，板子怎么让人知道

Type: grilling
Opened: 2026-09-19
Status: resolved
Blocked by: -

## Question

原地升级有一个几百毫秒的危险窗口（擦扇区 0 + 写回）。掉电之后：板子用 BOOT0 + USB DFU 能重烧回来，**但 owner 记录可能已经没了或者只写了一半** —— 而操作员从外面看不出区别。

现成的材料：**journal 扇区在 `0x081E0000`，属于 Bank 2，整个升级过程不会被擦**。所以可以在升级前后各写一条记录，让救回来的板子自己说出上次发生过什么。

要定三件事：

1. **写什么** —— 两条 journal 事件的名字和各自的触发点（开始擦之前 / 写回全部完成之后）
2. **怎么报** —— 新 bootloader 启动时发现「有开始、没完成」，日志那一行的**英文原文**
3. **报完让人做什么** —— 这一行是纯诊断，还是要引导操作员去跑某个命令确认所有权

⚠️ 这是**诊断，不是恢复**。掉电丢的东西找不回来，这张票只保证「人知道要去查」，不保证「板子自己修好」。

## 用户 2026-09-19 给的方向

原话：**「直接报升级失败，请用 stlink 和 ide 重新烧写 boot 和 app 并重新授权。」**

⚠️ 但**要分两种情况，它们能不能出声不一样**：

| | 什么时候 | 板子还能说话吗 |
|---|---|---|
| **情况一** | `flashboot` 被拒（验签不过 / 镜像超 120 KiB / 未认领又没按 BOOT0） | ✅ 能，**还没擦任何东西**，当场回拒绝原因 |
| **情况二** | 擦写中途掉电 | ❌ **不能，扇区 0 空了，一个字都打不出**。只有救回来之后才报得出 |

情况二的日志草稿（英文，按代码和日志的语言规矩），**等用户改**：

```
** Previous bootloader update did not finish. Ownership may be incomplete. **
** Re-flash the bootloader and the application, then claim the board again. **
```

⚠️ **用户原话说「用 ST-Link 和 IDE」，其实不用** —— 按住 BOOT0 复位进 ST 的 ROM DFU，
一根 USB 线就能重烧（2026-09-18 实测 11 次）。**要不要在文案里给出这条更省事的路，待用户定。**

## 怎么算答完

三件事各有明确答案，并且第 2 条写出可以直接 grep 的日志原文。

同时写明一句：**这两条 journal 事件各吃几个槽**，以及它对「一次成功升级消耗 8 个 journal 槽」（`R1-28` / `T1-26`）那条判据有没有影响。

## Answer

2026-09-20 定。用户看过草稿后说「就这样」，**两段文案按草稿采用**。

### 两种情况分开，只有第二种需要新文案

| | 什么时候 | 板子还能说话吗 | 怎么报 |
|---|---|---|---|
| **一** | `flashboot` 被拒（验签不过 / 镜像超 120 KiB / 未认领又没按 BOOT0） | ✅ 能，**还没擦任何东西** | 当场回拒绝原因，走现有的应答路径，**不需要新文案** |
| **二** | 擦写中途掉电 | ❌ 不能，扇区 0 空了 | 见下 |

### 两条 journal 事件

| 事件 | 什么时候写 | 吃几格 |
|---|---|---|
| bootloader 升级开始 | **擦扇区 0 之前** | 1 |
| bootloader 升级完成 | 写回全部完成之后 | 1 |

journal 扇区在 `0x081E0000`（Bank 2），**整个升级过程不会被擦**，所以这两条能活下来。

⚠️ **对 `R1-28` / `T1-26`（一次成功升级消耗的 journal 槽数）没有影响** ——
那条数的是**升级 app**，和升级 bootloader 是两条不同的路径。两者不共用计数。

### 救回来之后那一行（英文，按日志的语言规矩）

新 bootloader 启动时读 journal，发现「有开始、没完成」就打：

```
** Previous bootloader update did not finish. Ownership may be incomplete. **
** Re-flash the bootloader and the application, then claim the board again. **
```

⚠️ **刻意不在这一行里讲 DFU 怎么用。** 启动日志要短；那条「按住 BOOT0 复位进 ST ROM DFU、
一根 USB 线重烧、不需要 ST-Link」的省事路子写在**发布说明**里（见下），两处不重复。

### 发布说明那一段（`$BOOT/RELEASE-NOTES.md`，整份是英文）

现在写着「换 bootloader 要重传 app **和**重新认领」，原地升级做出来之后过期。换成：

```markdown
### Updating the bootloader

From this release the bootloader can be updated in place with `IAPTool flashboot`.
**Ownership and the installed application both survive the update** -- no ST-Link needed.

- The update requires a signature from the board's current owner. An **unclaimed**
  board additionally requires BOOT0 to be held through start-up.
- **Do not cut power during the update.** If power is lost the board will not start.
  Hold BOOT0 through a reset to enter the ST ROM DFU and re-flash the bootloader over
  USB; whether ownership survived depends on where it stopped, and the boot log says so.
- The update also discards superseded entries in the owner record area, reclaiming slots.

⚠️ Re-flashing the bootloader over **ST-Link still wipes ownership** -- the owner records
live in the bootloader's own flash sector. Use `flashboot` to keep it.
```

⚠️ **这段有一句现在还不成立**：「所有权会保住」**只在 `format_ver` 3 之后的版本之间为真**。
升到 v3 的那一次，v2 记录会被判无效，所有权照样丢 —— **那一次切换要单独说明，不能混进这一段**。
见[加了 'R' 记录，format_ver 要不要升到 3](OWN-03-does-format-ver-go-to-3.md)。

## 引出了什么新的未知

**没有。** 两段文案都已定稿，落地时照抄即可；两条 journal 事件的名字和触发点也定了。
`format_ver` 3 那次切换要单独说明这件事，已经在发布说明那条待办里。
