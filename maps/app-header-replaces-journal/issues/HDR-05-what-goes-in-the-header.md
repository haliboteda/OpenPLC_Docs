# header 那一千多字节里放什么

Type: grilling
Opened: 2026-09-20
Status: open
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
3. **换主语义带来的额外字段** —— 取决于 [换主之后，旧根签的固件还能不能启动](HDR-01-does-setowner-still-invalidate-installed-firmware.md)：
   若换主改成「只管未来」，可能要存**安装时那把根**（多 64 B）
4. **哈希范围的两端** —— 建议 `[app_base + HEADER_SIZE, + app_size)`，即 header 整个在范围外
   （和今天 metadata 整个在范围外同构）。要确认这样 `app_size` 仍被**间接保护**：
   改它就改了哈希范围，哈希变了签名就对不上
5. **padding 填什么** —— `0xFF`（擦除态）还是 `0x00`？影响 magic 的判据写法
6. **`_Static_assert` 锁哪几个尺寸** —— 今天 `bootloader_state.c` 用两个断言锁死 on-flash 格式，
   理由是「多一个 padding 字节会让已写记录全部错位」。新结构要照搬这个保护

## 怎么算答完

产出一张**逐字段的偏移表**（像 `M1-firmware-upgrade.md` 第 3 节那三张一样：偏移 / 长度 / 字段），
并且：

1. 每个字段旁边写清**它为什么在这里** —— 没有理由的字段不要留
2. 写明**哈希范围的起止**，以及 `app_size` 靠什么保证完整性
3. 写明**上面 6 条待定里每一条的结论**，包括答「不要」的那些
4. 写出要加的 `_Static_assert`
5. 确认**上位机仍然零改动**（`flash <size> <crc> <sig> <cert> <noncesig>` 协议不变，header 由板子自己填）
