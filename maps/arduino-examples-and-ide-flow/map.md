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
- **这一版统一叫 `0.1.3`**，发布就发 `0.1.3`（用户 2026-09-24 定）。板卡包 = `$CORE_REPO`（`open_plc_arduino`）；
  `package_index_json` 是 IDE 加载这个插件用的索引；IDE 装出来的位置 `$CORE_LIVE` 和 `$CORE_REPO` 内容相同。
  固件和 `boards.txt` 已是 `0.1.3`，**带 `-pre` 的只剩索引里那一项和它装出来的目录名**
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

- [IDE 上传时用哪把密钥，已认领的板子要用户准备什么](issues/IDE-02-which-key-does-an-ide-upload-use.md)：IDE 不传密钥参数，IAPTool 用工具包里 `keys\fw_signing_key.pem`（加同名 `.cert`）；三种板子状态各放什么已列出
- [一个发布版今天是怎么到 Board Manager 的](issues/IDE-01-how-does-a-release-reach-board-manager.md)：全手工、对外 6 步；网上的 `0.1.3-pre` 能装但内容是 4 月的，工具包里的 IAPTool 不会签名
- [假板子要像到什么程度，arduino-cli 的 upload 才能走完](issues/IDE-04-how-real-must-the-fake-board-be.md)：停在 bootloader 时现有假板子已够；跑 app 时补约 25 行，原型已走通
- [CAN 和 SD 卡在 Arduino 下最少要补什么](issues/IDE-03-what-can-and-sd-need-in-arduino.md)：CAN 照板上跑通的代码写薄封装；SD 用上游 STM32SD，但先把变体里 27 项的 SD 引脚表砍到真实接的脚
- [一个例程长什么样](issues/IDE-05-what-does-one-example-look-like.md)：照 DO 原型，文件头四段、USB 串口 115200、英文输出
- [IDE 上传用的密钥放在哪、怎么放进去](issues/IDE-13-where-does-the-ide-upload-key-live.md)：`%AppData%\openplc\keys\`，公开根私钥随包兜底，找不到或不对时报出路径
- [模拟台上走通 IDE 烧录](issues/IDE-11-ide-upload-on-the-simulator.md)：用例 `T1-34`，arduino-cli 对跑 app 的假板子上传，未认领 / 已认领 / 密钥不对三种都按预期，手工跑
- [0.1.3 怎么命名、按什么顺序发](issues/IDE-14-how-is-0-1-3-named-and-released.md)：tag `0.1.3`、工具包也升 0.1.3、客户用一个固定索引地址
- 端口例程（[数字量](issues/IDE-06-digital-io-examples.md)、[模拟量](issues/IDE-07-analog-examples.md)、[串口](issues/IDE-08-serial-examples.md)、[以太网](issues/IDE-09-ethernet-example.md)、[CAN 和 SD](issues/IDE-10-can-and-sd.md)）：13 个例程在 `OpenPLC_Ports`，`P5` 全绿，未上板
- [发一个版本，像用户一样从网上装](issues/IDE-12-release-and-install-like-a-user.md)：`0.1.3` 已发布，从固定索引地址装上后例程齐全、`T1-34` 全过

## Not yet specified

- **KNX、SDRAM 现有的 7 个例程要不要改成统一格式** —— 要等「一个例程长什么样」定了才说得清
- **linux / macosx 上装的 `IAPTool` 没有可执行位**（发出去的包里是 `-rw-rw-r--`），那两个平台的 IDE 上传未验 —— 本图只验 Windows

## Out of scope

- **扩展口 JunctionLink（UART4 / SPI2 / SPI6）的例程** —— 给扩展板用的连接器，不是面板端子。2026-09-24 定
- **自动判过不过的自检** —— 工装已经在做。2026-09-24 定
