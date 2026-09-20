# 让出来的 128 KiB state 扇区给谁

Type: grilling
Opened: 2026-09-20
Status: open
Blocked by: HDR-02

## Question

metadata 搬走之后，`IAP_STATE_SECTOR_ADDR`（`0x081E0000`，Bank2 Sector7）这 128 KiB 空出来。**给谁？**

⚠️ **被 [八种事件日志留不留，留的话住哪](HDR-02-do-the-event-logs-survive.md) 挡着** —— 日志要是留在原地，这个扇区就没空出来。

三个候选：

| | 给谁 | 得到 | 要处理什么 |
|---|---|---|---|
| **F1** | **app 区**，`IAP_APP_MAX_SIZE` 从 1792 KiB 涨到 1920 KiB | app 多 128 KiB | `Erase_FLASH()` 里那道守卫（`flashAddress + Len > IAP_STATE_SECTOR_ADDR → HAL_ERROR`）**是全代码唯一挡在 app 上传和 bootloader 状态之间的东西**，边界挪了要重新论证它挡的是什么 |
| **F2** | **校准值** | `DECISIONS.md` 第 45 条的掉电冲突**自动消失** | 见下 |
| **F3** | 空着 | 零风险，留给以后 | 什么都没得到 |

### F2 值得单独看 —— 它解掉一个已存在的设计冲突

[`DECISIONS.md` 第 45 条](../../../docs/tables/DECISIONS.md)（用户 2026-09-14 定）把校准值放在 state 扇区**最后 8 个槽**，
由 `journal_reclaim()` 擦扇区之前读进 RAM、擦完写回。

⚠️ **那条搬运会打破 journal 设计的地基**：今天「reclaim 不引入任何新失败模式」这句话成立，
是因为擦的那一刻掉电最坏是「需要重刷固件」，而那个结论本来就已成立。**校准值不一样 ——
重刷固件不会恢复它**，要重新标定或重新用 JLINK 写。

**没有 journal 就没有 reclaim，校准值独占一个永不擦的扇区，这个冲突根本不存在。**

⚠️ 但 F2 有个前置动作：扇区里现在装着旧 journal 记录，**必须先擦一次**，否则旧记录会被当成校准值读。

⚠️ 这一条的代码用户 2026-09-14 说过 AI 不写（「校准码代码不用写，你就写个 todo 就行」），
2026-09-16 又说「暂时不动」（见 [`waiting/WAITING-ON.md`](../../../waiting/WAITING-ON.md)）。
**本票只定归属，不写实现。**

## 怎么算答完

1. 选定 F1 / F2 / F3 之一，一句话定论
2. 选 F1 的话：**写出 `Erase_FLASH()` 那道守卫改成什么**，并回答「守卫挪走之后，还有什么挡在 app 上传和 bootloader 自身之间」
3. 选 F2 的话：**写明「先擦一次」这个动作由谁在什么时候做**（出厂烧录？第一次升级？），
   并去 `DECISIONS.md` 第 45 条**标注前提已变**（该条现在写着「靠 reclaim 搬运」）
4. 不管选哪个：说明**这次是否改动 `IAP_APP_MAX_SIZE`**，因为它是跨仓镜像项（`boards.txt` 的 `upload.maximum_size`）
