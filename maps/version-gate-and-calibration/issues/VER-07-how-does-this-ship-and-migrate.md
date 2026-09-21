# 这次变更怎么发布，现场的板子怎么迁移

Type: grilling
Opened: 2026-09-21
Status: resolved
Blocked by: VER-04

## Question

从 [metadata 从 journal 扇区搬进 app 头部](../../app-header-replaces-journal/map.md) 那张图
继承过来的问题（原 `HDR-06`），**范围小了但没消失**。

不搬 header 之后，`build.flash_offset` 和 `upload.maximum_size` 都不用动了。
但仍然有两处会打断现场板子：

| 变更 | 后果 |
|---|---|
| **扇区 15 布局改了** —— 前面让出 8 KiB 给校准值，metadata 起点从 `0x081E0000` 挪到 `0x081E2000` | 装了新 bootloader 的板子**读不到旧 metadata**，会报 app 无效 ⇒ **要重传一次固件**。和 `a92a8c7` 同一类 |
| **事件日志删了** | 旧 journal 里的 `'L'` 记录成了不认识的记录。今天 `bootloader_state_init()` 遇到不认识的记录会**停下并把 journal 转为只读**（`s_format_unknown`），要确认新代码怎么处理这片旧数据 |

还有一处**只影响用户**、不影响板子的：

- **sketch 不写 `OPENPLC_APP_VERSION` 就编译不过** —— 所有现存的用户 sketch **第一次用新板卡包时都会编译失败**。这是故意的，但要有迁移说明

## 怎么算答完

1. 写明**装了新 bootloader 的板子开机时看到旧 journal 会怎样** —— 是自动擦、报错停下、还是当空处理
2. 写明**现场迁移的步骤**：先换 bootloader 还是先换板卡包，中间那一步板子处于什么状态
3. 写明**校准值怎么办** —— 现场板子的扇区 15 里现在没有校准值，新布局下那 8 KiB 是空的，要不要做什么
4. 写出**给用户的迁移说明**要讲哪几句（尤其「你的 sketch 现在编译不过了，加这一行」）
5. 确认 `RELEASE-NOTES.md` 要改哪几句

## Answer

2026-09-21 定

**选 M1：新 bootloader 第一次启动发现扇区 15 不是新格式，整个擦掉。不做迁移，不保旧数据。**

### 1 · 旧 journal 怎么处理

**擦掉，全新建。** 理由：**现在做这件事是免费的** —— 校准值功能还没实现，
现场板子的扇区 15 里根本没有校准值，擦掉零损失。

⚠️ **今天的代码本来就会擦**：`bootloader_state_init()` 扫描时遇到不认识的记录会置
`s_format_unknown`，下一次 `bootloader_state_save_metadata()` 就 `journal_reclaim()` 擦整扇区。
新布局只需要确认判据对得上，**不需要新写一段迁移代码**。

### 2 · 后果：现场板子要重传一次 app

扇区 15 一擦，metadata 就没了 ⇒ 板子报 app 无效 ⇒ 重传一次固件。
和 `a92a8c7`（删防回滚那次改 metadata 布局）同一类，发版说明要照那次的口径写。

### 3 · 迁移顺序：先换板卡包，再换 bootloader

**中间状态必须是可用的**，这个顺序满足：

| 状态 | 能用吗 |
|---|---|
| 新板卡包 + 旧 bootloader | ✅ **能用** —— metadata 格式没变；app 报 5 段 identity，旧工具只是显示难看，不影响烧录 |
| 旧板卡包 + 新 bootloader | ⚠️ 板子先瘫一阵（metadata 被擦，要等重传） |

### 4 · 用户那边会遇到什么

⚠️ **所有现存 sketch 换上新板卡包后第一次编译都会失败** —— 没写 `OPENPLC_APP_VERSION`。
这是故意的，迁移说明里要写清楚加哪一行、加在哪。

### 5 · `RELEASE-NOTES.md` 要写的

1. sketch 现在必须声明版本号，**旧 sketch 编译不过**，加 `OPENPLC_APP_VERSION(1, 0, 0);`
2. 烧录时会比版本，低了拒绝；要强制走 工具 ▸ 低版本强制烧录，**一次性**
3. 换 bootloader 会擦掉状态扇区，**已装的 app 要重传一次**
4. 升级顺序：**先换板卡包，再换 bootloader**
5. SWD / Serial 直连不受版本检查约束（决策 62）

## 引出了什么新的未知

一条，记进图的 `## Not yet specified`：**将来有了校准值之后，「遇到不认识的记录就擦整扇区」这条逻辑会变危险** ——
那时 metadata 区损坏不该连累校准值区。本次免费，下次不免费。
