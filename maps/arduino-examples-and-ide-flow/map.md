# Arduino 例程与 IDE 烧录流程

## 怎么看进度（不用问任何人）

```
python tools/list_wayfinder_map_frontier.py --all
```

## Destination

1. **每个用户端口在 IDE 的「文件 → 示例 → OpenPLC_Ports」下有一个例程**，编得过；上传后串口监视器里说清它在干什么、该接什么线、该看到什么
2. **按客户的路走通烧录**：干净的 Arduino IDE → Board Manager 从网上装发布版 → Tools → Port 选中「名称 @ IP」→ Upload，未认领和已认领的板子都能烧进去

先在模拟台上走通，再上板逐条验证。

## Notes

- **这张图带执行**：票定完就写代码，终点是能用的例程和走通的流程，不只是设计
- **只做必要的代码和功能**；先文档再代码
- 板卡包改动方向单向：先改 `$CORE_LIVE`，验过再拷进 `$CORE_REPO`
- ⚠️ **发布是对外动作**（推 tag、发 release、改线上索引），每一次发布前单独问用户
- 只在 Windows 上验
- 开票 / 关票 / 算前沿照 [图与票的约定](../MAP-AND-TICKET-CONVENTION.md)

### 开图时已定（2026-09-24 用户定）

| 事 | 定案 |
|---|---|
| 「所有端口」 | DI、DO、继电器、AI、AO、板载温度、RS232、RS485、USB 串口、以太网、系统 LED，**加上 CAN 和 SD 卡**（这两个要先补一个最小的库）。KNX、SDRAM 已有例程。扩展口 JunctionLink 不算 |
| 一个例程做成什么样 | 最小用法，外加串口里说清怎么测；**不做自动判过不过**（那是工装的活） |
| 例程放在哪 | 新库 `OpenPLC_Ports`，CAN / SD 需要的库代码也放这里 |
| 烧录流程跑到什么程度 | **和用户一样**：真的发 release，从网上装 |
| 模拟做到哪 | 编译全部例程 + 假板子出现在 Tools → Port 并收下一次 arduino-cli 发起的 upload。**测不到例程在板子上的真实行为** |
| 板子状态 | 未认领、已认领都要能烧 |

## 全集

```
ls open_plc_cube_ide/TestCase/porttool/porttool_*.c          # 板子上有哪些用户端口
grep -nE 'upload\.|discovery|pluggable' open_plc_arduino/platform.txt open_plc_arduino/boards.txt
ls package_index_json/*.json                                  # Board Manager 装的是什么
```

## Decisions so far

## Not yet specified

- **KNX、SDRAM 现有的 7 个例程要不要改成统一格式** —— 要等「一个例程长什么样」定了才说得清
- **发布之后怎么上板逐条验** —— 顺序、哪些要人动手，等例程和发布流程都定了再排

## Out of scope

- **扩展口 JunctionLink（UART4 / SPI2 / SPI6）的例程** —— 给扩展板用的连接器，不是面板端子。2026-09-24 定
- **自动判过不过的自检** —— 工装已经在做。2026-09-24 定
