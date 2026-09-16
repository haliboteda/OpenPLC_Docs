# 05 · 这一轮联调测哪些端口、按什么顺序

Type: grilling
Opened: 2026-09-11
Status: open
Blocked by: PUI-02

## Question

真板子上这一轮能测到哪一步，先测哪个？

## 已知的起点（2026-09-09 收工）

- **真板子 station6**：19 过 / 4 失败 / 4 跳过（27 步）
- **模拟板 station6**：26/26 全过
- 四个失败**没有一个是代码问题**：`sd-card`（卡是 exFAT，正确的失败）、`eth-throughput`（环境：`tun0` 代理占默认路由 + 有线网口 Disconnected）、`digital-in`（缺激励）、`analog-in`（缺激励）

## 要定的

1. **哪些端口现在就能测**（不用额外接线、不用额外硬件）。
2. **哪些卡在人要动手的事上**，各自挡在什么上：
   - `din` / 编码器 —— 八芯线从 `dout` 接过来，判据是矩阵对角
   - `ain` —— 那两个引脚彻底悬空，等硬件焊 JP5/JP6/JP8/JP9（请求单 `$PROD/docs/outbound/AIN-JUMPER-REQUEST.md`）
   - `sd` 的 integrity/stress/speed —— 要一张 FAT32 卡
   - `eth-throughput` —— 要关掉 `tun0` 代理 + PC 有线网口插到板子同一交换机
   - SD 热插拔的 H5 断言 —— 要人拔卡插卡
   - `aout` 电流核对 —— 万用表，⚠️ 先确认 JP3/JP4 没焊
3. **顺序**：02 改了 `term=` 的端口要优先复测（标签改过，等于换了个东西）。
4. **模拟板要不要先跑一遍** —— 改了固件 stub 之后 `build.py --sim` 要单独重建，忘了就是拿旧的在测。

## 产出

一份联调清单：端口 / 现在能不能测 / 挡在什么上 / 谁能解。人要动手的那几条按 `~/.claude/rules/hands-on-steps.md` 的格式单独列出来。

---

## 2026-09-11 首轮实测的发现

烧入修正后的工装镜像（`term=C10,C11` 已在板上确认），跑 `station6-poweron`：**18 过 / 5 失败 / 1 错误 / 4 跳过**。

### ⚠️ 新发现：`indicator-seen` 这一步无法无人值守运行

它是 `UserConfirm` 类型，会在终端里问「Did the status indicator flash six times? pass? [y/N]」然后**读 stdin**。非交互运行时直接 EOF：

```
ERROR indicator-seen (UserConfirm) - could not read an answer: EOF
```

**后果**：整条产线序列没法脚本化跑完，而且这一步 ERROR 之后，`execute_condition` 的门会让后面依赖它的步骤跟着跳。

要定：这类"要人眼确认"的步骤在**无人值守**模式下怎么处理 —— 跳过并标记为"未判"？还是序列拆成两段？（面板里跑的时候是弹框，不是这个问题。）

### 环境事实（当天）

| | |
|---|---|
| COM12 | Prolific PL2303GT，控制口 ✅ |
| COM16 | CH340，RS485 对端 ✅ |
| COM14 | ST-Link VCP，能烧板 ✅ |
| CAN 适配器 | ❌ 不在（但 `can` 用 `extloop`，不需要对端，照样过） |
| 有线网卡 | Disconnected；`tun0` Up —— **但 eth 照样通过**，板子和 PC 都在 192.168.0.x |
| SD 卡槽 | **空的**（`detected=0`，不是 exFAT 的问题） |

### ⚠️ 新缺陷：开机后插入的 SD 卡初始化不了，必须复位

**2026-09-11 实测，连探 4 次稳定复现。**

| 时机 | `sd.probe` 结果 |
|---|---|
| 开机后热插入 | `detected=1 ready=0 blocks=0 fs=none **err=0x10000000**` |
| 复位后（卡在位） | `detected=1 ready=1 blocks=123596800 mib=60350 v2x=1 fs=exfat err=0x0` |

`0x10000000` = `SDMMC_ERROR_UNSUPPORTED_FEATURE`。这份 HAL 里只有四处返回它（`TestCase/common/stm32h7xx_hal_sd.c:3261` 的 1.8 V 电压切换，`:3821 :3937 :4065` 的高速模式切换），**都在速度/电压协商阶段**，还没走到文件系统。

**为什么值得记**：`6b0b718` 刚把 SD 做成会话，目的就是"让面板看得见热插拔"。现在的状态是 —— **面板看得见插入（`detected=1`），但卡不可用**，而且只给一个 `err=0x10000000`。这对面板前的人是最坏的一种：看起来插好了，用不了，错误码没人看得懂。

**要做什么**（待定）：
1. 插入事件触发 SD 外设重新初始化（`HAL_SD_DeInit` + `HAL_SD_Init`），让热插即可用；或
2. 至少把这个状态在面板上说成人话：「卡已插入但未初始化 —— 请复位板子」，并把 `err=` 翻译成原因

⚠️ 这条和还欠的 **H5 热插拔断言**是同一件事的两面：H5 要断言"拔卡→插卡"能被看见，而这里发现"被看见"之后卡还不能用。

### 当前成绩（2026-09-11，四轮）

| 轮次 | 结果 | 变化 |
|---|---|---|
| 1 | 18 过 / 5 失败 / 1 错 / 4 跳 | 基线（烧入修正后的镜像） |
| 2 | 19 过 / 4 失败 | 用户把 RS485 接到 C10/C11 → `rs485` 转绿 |
| 3 | 20 过 / 3 失败 | 插入 SD 卡 → `sd-detect` 转绿 |
| 4 | 20 过 / 3 失败 | 复位后 `sd-card` 变成**正确的失败**（`got exfat`，不再是 `ready=0`） |

剩余三条失败：`sd-card`（要 FAT32）、`digital-in`（要八芯线）、`analog-in`（要焊 JP5/JP6/JP8/JP9）。
外加 `indicator-seen` 的 UserConfirm 无法无人值守。

## 怎么算答完

⚠️ **这张票搬进来时没有这一节**（2026-09-16 之前的写法不要求）。开工前先补上再动手。

