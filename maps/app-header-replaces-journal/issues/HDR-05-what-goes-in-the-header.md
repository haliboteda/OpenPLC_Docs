# header 那一千多字节里放什么

Type: grilling
Opened: 2026-09-20
Status: resolved
Blocked by: HDR-01, HDR-04

## Question

header 的**大小**由 [VTOR 对齐到底要多少字节](HDR-04-what-is-the-real-vtor-alignment.md) 定（推导值 1024）。
本票定的是**里面放什么、什么布局**。

已知必须有的（合计 196 字节，其余是 padding）：

| 字段 | 字节 | 为什么必须 |
|---|---|---|
| `app_size` | 4 | 定哈希范围。不记它就必须每次全擦 app 区（已定，见 map 的 `Decisions so far`） |
| `signature` | 64 | 对 app 内容的背书。**公钥本身验证不了任何东西** |
| `cert` | 128 | 证明该用哪把公钥验，且那把公钥被根认可。**只缓存叶公钥不安全** |

待定的：

1. **要不要 magic** —— 用来区分「这个位置从没写过」和「写了一半」。
   ⚠️ 它直接决定 map 的 `Not yet specified` 里那条能不能消掉：
   今天「板子起不来怎么查」那张表能分开 `metadata absent`（出厂空板）和
   `App signature invalid`（装过但上次失败），**header 跟 app 一起被擦之后这两行会塌缩**，
   除非 magic 能把它们分开
2. **要不要 `format_ver`** —— `owner_record_t` 从第一版就带着它，理由写在 `owner_slot.h`：
   「so a later format change is an upgrade rather than a breaking migration」。header 要不要照办
3. ~~换主语义带来的额外字段~~ —— **2026-09-20 已答**：[换主之后，旧根签的固件还能不能启动](HDR-01-does-setowner-still-invalidate-installed-firmware.md)
   定成「仍然作废，停在 bootloader」，所以验的就是**当前**的根，**不需要存安装时那把根**。
   三个字段合计 196 字节不变
4. **哈希范围的两端** —— 建议 `[app_base + HEADER_SIZE, + app_size)`，即 header 整个在范围外
   （和今天 metadata 整个在范围外同构）。要确认这样 `app_size` 仍被**间接保护**：
   改它就改了哈希范围，哈希变了签名就对不上
5. **padding 填什么** —— `0xFF`（擦除态）还是 `0x00`？影响 magic 的判据写法
6. **`_Static_assert` 锁哪几个尺寸** —— 今天 `bootloader_state.c` 用两个断言锁死 on-flash 格式，
   理由是「多一个 padding 字节会让已写记录全部错位」。新结构要照搬这个保护

## ⚠️ 这张票要专门兜住的两件事（2026-09-20 对话中挖出）

### 边界算错的后果，比今天严重得多

今天 metadata 在另一个扇区，**物理上不可能出现「app 的一部分没被签名覆盖」**。
header 紧挨在 app 前面之后，这件事就可能了：

```
0x08020000 ┌─ header ─┐
0x08020400 ├──────────┤ ← 向量表：[0] = MSP，[1] = Reset_Handler
           哈希起点若算成 0x08020408（往后偏 8 字节）
           ⇒ Reset_Handler 落在签名覆盖范围之外
           ⇒ 攻击者改它就能劫持执行流，而签名照样验得过
```

**这不是安全模型变差**（唯一有差别的攻击路径上，门槛仍然是「造不出 `root_sig`」），
**是实现出错的代价变大**。所以本票必须产出一条能被编译器或测试抓住的约束，不能只写在文档里。

### `app_base` 这个变量今天扛两个含义，S-e 下会分叉

| 用处 | 今天 | S-e 下 |
|---|---|---|
| `IAP_server.c:587-588` 读 MSP / Reset | `app_base` | `IAP_APP_ADDRESS + HEADER_SIZE` ✅ 跟着变 |
| `IAP_server.c:614` 哈希起点 | `app_base` | 同上 ✅ |
| `IAP_server.c:749` `SCB->VTOR` | `app_base` | 同上 ✅ |
| **`IAP_server.c:95` `Erase_FLASH(app_base, size)`** | `app_base` | ⚠️ **必须是 `IAP_APP_ADDRESS`（含 header）** —— 否则 header 那一段不会被擦，而 flash word 写过一次不能再写，**新 header 写不进去** |
| **`IAP_server.c:101` 写入起点** | `app_base` | 镜像写 `app_base`，**header 单独写** |

**只改 `app_base` 一处是不够的。**

## 怎么算答完

产出一张**逐字段的偏移表**（像 `M1-firmware-upgrade.md` 第 3 节那三张一样：偏移 / 长度 / 字段），
并且：

1. 每个字段旁边写清**它为什么在这里** —— 没有理由的字段不要留
2. 写明**哈希范围的起止**，以及 `app_size` 靠什么保证完整性
3. 写明**上面 6 条待定里每一条的结论**，包括答「不要」的那些
4. 写出要加的 `_Static_assert`，**其中必须有一条锁死「哈希起点 == 向量表起点 == `IAP_APP_ADDRESS + HEADER_SIZE`」三者是同一个常量** —— 上面那条边界风险靠它兜住，写在文档里不算
5. 确认**上位机仍然零改动**（`flash <size> <crc> <sig> <cert> <noncesig>` 协议不变，header 由板子自己填）
6. **逐条写明 `app_base` 那五个用处各自该用哪个地址**，并指出哪几处不能跟着 `app_base` 走

## Answer

2026-09-21 定

**本票作废 —— 不做 header 了。**

用户 2026-09-21 定：metadata 留在扇区 15，journal 的事件日志删掉，
校准值放扇区最前面。**app 镜像开头不再有定长 header**，
所以「里面放什么、分几段、哈希范围从哪起」这些问题全部消失。

⚠️ 本票讨论过程中挖出的一条仍然有用，已记在决策 62：
**版本号必须落在签名覆盖范围内才谈得上防回滚** —— 而这一版决定
**不在板子侧做防回滚**，所以这条约束这一轮用不上。

## 引出了什么新的未知

没有。
