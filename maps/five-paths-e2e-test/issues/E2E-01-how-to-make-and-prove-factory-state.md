# 出厂态怎么造，怎么证明它真的是出厂态

Type: task
Opened: 2026-09-20
Status: resolved
Blocked by: -

## Question

五条路径的起点都是「模拟出厂：清 flash + 烧 bootloader」。**今天没有工具做这件事。**

`tools/flash_bootloader.py` 只做构建 + 烧写 + 抓启动日志，**全程不擦 flash**
（`--reset-only` 明写着 never writes flash，整个文件没有任何 erase 路径）。
所以直接跑它得到的不是出厂态 —— owner 记录、journal、app 区都还是上一轮的残留。

要做两件事：

1. **走通一次真正的清除** —— `STM32_Programmer_CLI` 的整片擦除（工具路径由
   `config/machine.py` 的 `get_programmer_cli()` 给出），然后烧 bootloader
2. **定下「这确实是出厂态」的判据** —— 光看擦除命令返回 0 不够。候选：
   - owner 记录区（`0x0801E000` 起 8 KiB）读回来全是 `0xFF`
   - 启动日志出现 `Owner slot: empty, using the built-in root key`
   - 启动日志出现公开根告警 `** This board trusts the PUBLISHED root key`
   - journal 槽位数归零
   - app 区验签失败（`BOOTLD-INVALID` 或等价日志）

⚠️ **这张票是 `task` 不是 `grilling`** —— 它本身没什么可争的，但**五条路径全卡在它后面**：
造不出可信的起点，后面每一条路径的结果都没法解释。

## 怎么算答完

- 有一个能重跑的东西（脚本或写下来的命令序列），从任意状态把板子带回出厂态
- 判据写成**能判真假**的话，且**至少两条相互独立**（只看一条日志不够 —— 日志没抓到也是 0 行，
  和「没打印」分不开，这个坑 `T2-07` 踩过）
- 写明**这一步测不到什么**

## Answer

2026-09-20 定，**真板子上跑过一遍，PASS**。

### 怎么造

```
python tools/reset_board_to_factory_state.py              擦除 + 烧 bootloader + 验证
python tools/reset_board_to_factory_state.py --check-only 只验证，绝不写
```

脚本在 `$TOOL/TestCase/tools/reset_board_to_factory_state.py`。四步：
读出**清除前**的三个区域 → `STM32_Programmer_CLI -e all` 整片擦除 →
**擦完先单独验一次**（还没烧 bootloader 时）→ 烧 bootloader → 复位抓日志 → 判定。

⚠️ **「擦完先单独验一次」这一步不能省**：烧在一次失败的擦除上面的 bootloader
照样能启动、照样打出所有正确的行，**日志分不出这两种情况**。那是唯一看得见差别的时刻。

### 判据：两类证据，缺一不判 PASS

| 类别 | 判据 | 怎么来的 |
|---|---|---|
| **读 flash**（不经串口） | owner 区 `0x0801E000` 起 **8 KiB 全 `0xFFFFFFFF`** | SWD `-r32` 读回来逐字比 |
| **读 flash** | app 区 `0x08020000` 起 256 字节全 `0xFFFFFFFF` | 同上 |
| **启动日志** | `Owner slot: empty` | 串口 |
| **启动日志** | `trusts the PUBLISHED root key` | 串口 |
| **启动日志** | `0/4096 journal slots used` | 串口 |

**两类相互独立**：读 flash 完全不经过串口，串口完全不经过 SWD。

⚠️ **日志一个字都没抓到时报 INCONCLUSIVE，不报 PASS。** 没抓到的日志和「什么都没说」的日志
长得一模一样 —— 这正是 `T2-07`（换根后公开根告警不再出现）踩过的坑。捕获证明用
`Bootloader state:` 那一行，**不用 SDRAM 自检那行** —— 后者只在板子留在 bootloader 时才打，
在一块还装着 app 的板子上它的缺席意味着「没走到」，不是「没抓到」。

### 2026-09-20 实测

清除前：owner 区已空（未认领），**app 区有程序**（`0x24080000` 向量表），**journal 37/4096 已用**。
清除后：三个区域全空 → 烧 bootloader → 日志：

```
Bootloader state: 0/4096 journal slots used, metadata absent
Owner slot: empty, using the built-in root key
** This board trusts the PUBLISHED root key: anyone can sign firmware it will run. **
** App signature invalid or absent - staying in bootloader **
** UPLOAD Mod ... (no valid application)
```

退出码 0，判定 PASS。

### ⚠️ 这一步测不到什么 —— 有一条是实测才发现的

| 测不到 | 为什么 |
|---|---|
| **RTC 备份域没有被清** | 实测日志：`Backup domain retained, nonce counter = 20`。**nonce 计数器不在 flash 里**，整片擦除碰不到它。一块真正没上过电的出厂板这个值是 0。对五条路径无害（nonce 只要不重复就行），但**「清 flash」不等于「全新芯片」**，这条差别要知道 |
| option bytes 没有被碰 | `-e all` 只擦 flash 扇区。读保护、WRP、BOOT 地址等保持原样 |
| 硬件本身 | 这一步只证明**软件状态**是出厂态。板子焊得对不对、外设通不通，是 `CHK-C` 单板出厂那张单子的事 |

## 引出了什么新的未知

**有两条。**

1. **「出厂态」要不要把 RTC 备份域也算进去** —— 今天不算（擦不掉，也不影响五条路径）。
   但如果将来有哪条路径依赖「nonce 从 0 开始」，这条就得重新想。已并入本图迷雾。
2. **实测时日志里出现 `** Ethernet link is DOWN - this board will not answer discovery. **`，
   紧接着又打出 `[NET] IP 192.168.0.3 ... IAP server reachable`** —— 两行自相矛盾。
   和本票无关（不影响出厂态判定），但**是个发现，不是噪音**。已记进本图迷雾。
