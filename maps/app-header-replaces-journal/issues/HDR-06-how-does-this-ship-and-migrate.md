# 这次变更怎么发布，现场的板子怎么迁移

Type: grilling
Opened: 2026-09-20
Status: open
Blocked by: HDR-03, HDR-05

## Question

这次变更**同时动三个仓**，而且改了 app 的编译地址 —— 发布顺序错了，现场的板子会以
「装不进去」或「装进去起不来」的方式失败。

已知的迁移事实：

- 现有 app 链接在 `0x08020000`，新 bootloader 去 `0x08020000 + HEADER_SIZE` 找向量表
- 新 bootloader 读 header 位置，拿到的是**旧 app 的向量表字节** → 判定无效 → **停在 bootloader** ✅ 安全，但**必须重传 app**
- 旧 app 是用旧板卡包编译的，**必须换新板卡包重编译**才能装进新 bootloader
- ⚠️ 这是「bootloader 与 app 必须捆绑升级」那条已知风险的又一次实例，
  而且**这次连 Arduino 板卡包版本也要一起发**

要定的：

1. **三个仓的发布顺序**：`$BOOT`、`$CORE_REPO`（含 `$PKGIDX` 的版本号）、`$TOOL` 谁先谁后，
   以及中间状态下（用户升了一半）会看到什么
2. **旧 journal 扇区里的残留数据怎么处理** —— 取决于
   [让出来的 128 KiB state 扇区给谁](HDR-03-who-gets-the-freed-sector.md)。给校准值的话必须先擦一次
3. **发布说明怎么写**（英文，`$BOOT/RELEASE-NOTES.md`）—— 现在那份写着「换 bootloader 要重传 app + 重新认领」，
   这次要加上「**还要换板卡包重新编译**」
4. **现场的人怎么知道自己撞上了这件事** —— 板子停在 bootloader 时串口打什么，
   能不能一眼看出是「地址变了」而不是「app 坏了」
5. ⚠️ **`$CORE_REPO/tools/platformio/platformio-build.py` 那条路径** —— 它不读 `platform.txt`，
   `build.flash_offset` 改了它不会跟着变。走 PlatformIO 编译的用户会编出一个链接到旧地址的 app，
   **装得进去但起不来**。这条要么修、要么在发布说明里明写

## 怎么算答完

1. 写出**三个仓的发布顺序**，以及每种「升了一半」的组合下板子的表现（至少覆盖：只升 bootloader、只升板卡包）
2. 写出发布说明要加的段落（**英文**），放进 `$BOOT/RELEASE-NOTES.md` 的草稿位置
3. 第 5 条 PlatformIO 那条路径：**给出结论是修还是记** —— 不能留空
4. 回答第 4 条：现场看到的那行串口输出**原文**是什么
5. 核对 [`docs/modules/M1-firmware-upgrade.md`](../../../docs/modules/M1-firmware-upgrade.md) 第 7 节
   「板子起不来怎么查」那张八行索引表**要加哪一行**
