# PortTool 的测试（`$PORTTOOL`）

PortTool 仓的测试都在 `$PORTTOOL/TestCase/` 下，入口是本仓自己的自检：

```
cd TestCase
python tools/init_machine.py   # 第一次：生成 config/machine.py
python tools/selfcheck.py      # ENV / GO-TEST / GO-VET / T4-01 / CALAREA / DOCS / T4-02（接模拟板）；--quick 跳过 T4-02
```

用例定义在 [M4 产线工装](../modules/M4-production-fixture.md)。

## 主机侧测试（`TestCase/host/`，不需要板子）

| 目录 | 怎么跑 | 覆盖什么 |
|---|---|---|
| `host/porttool_caps/` | `python build.py`，需要 gcc/clang | **T4-01** 端口工装的协议契约，判据见 `$PORTTOOL:TestCase/host/porttool_caps/PORTTOOL-CAPS-TEST.md`（贴着代码放，没有搬过来） |
| `host/porttool_panel/` | `python run.py --port COMx`（**真板子**）或 `--port sim`（**模拟板，不用板子**，见下），都要 playwright + Chrome | **T4-02** 面板在真浏览器里点一遍。判据：①页面先过一遍语法（用 playwright 自带的 node `--check`，板子都不用）②页面抛的任何异常、控制台任何 error 直接判失败 ③串口列表、未连接时的门闸、按板子分组 ④**逐个端口按一次「开始测试」，每个端口的结论必须是这台工位应该出的那一个** —— 缺激励的端口要失败，并且失败原因里要点出是哪个读数 ⑤**方案文件里的参数真的发出去了** —— `on=1:1` / `mv=1:1000` / `duty=1:100` / `mode=extloop` 在日志里能查到 ⑥**持续测试**：「单次 / 持续」两个单选，持续下面才出现时长（1/2/3/4 小时 / 一直跑）；左边可以勾多个端口、一次启动；**看门狗在续期**（日志里 `OK hold=` 一直在涨，不是只武装了一次）；点停止要同时出 `OK stopped all` 和 `OK hold=off`。⚠️ **断言看的是板子的回复不是发出去的命令** —— 续期由服务端直接走串口发，不过 `/api/command`，页面日志里没有那一行 ⑦两个 tab、日志的暂停/清空/过滤、断开、记下的控制口 ⑧**改了参数就不给结论** —— 改一个参数再按「开始测试」，结论不能是「失败」，卡片要说清哪一项和方案不一样，点「恢复方案参数」之后又能判（2026-09-11 用户实测撞出来的：勾 DO3、占空比 50，1.4 秒出一个假失败）⑨**卡片上不许剩协议词** —— 逐个端口扫一遍，命中 `BANNED_ON_CARDS` 里任何一个（`duty`、`freq`、`miss`、`Klemmblock`…）就判失败 ⑩**四个一直没被点过的控件**（2026-09-11 补）：「单独跑」单个 `pt.run` 目标、「自动回环应答」勾选框、「绑上/解开」对端串口、**方案页的「运行」按钮**（用 `bench-smoke.json` 跑完整一轮，每一步都要回判据）。⚠️ **「绑上」在模拟板上只能证明控件通到服务端并且能解开** —— 「绑对了适配器才闭合链路」只有真工位能证明，因为模拟板自己演所有对端。⚠️ 覆盖不到的是**真外观** —— 颜色间距好不好看只能人看 |
| `host/porttool_plan/` | `go test ./TestCase/host/porttool_plan/` | **T4-04** 判据算子（缺字段一律判失败）；执行器（超时与判据失败分得开、重试保留被它替掉的那次失败、失败后的门闸看最后一个真跑过的步骤）；随包发布的 `plans/bench-smoke.json` 和 `plans/station6-poweron.json` 都能拿假板子跑通；方案里的 `pt.run` 目标对着 caps 的 `runs=` 离线校验（打错名字、写一个固件没报过的目标，两种都要报）；方案页四个接口 —— **写盘前先验、方案名出不了 plans 目录、跑方案期间面板自己的回环应答器停摆** |

## 模拟板：手上没板子时怎么联调

**它是什么**：`TestCase/porttool/` 那些 `.c` 原样编成的 PC 程序，只换掉外设 stub 和最外层 main。命令解析、`pt.caps`、会话逻辑、帧格式、版本号全是固件那份源码，所以固件改了它编不过 —— **不会漂移**。设计理由见 `$PROD/docs/tables/DECISIONS.md` 第 29 条。

```bash
cd TestCase/host/porttool_caps && python build.py --sim   # 编，产出 harness/porttool_simboard.exe
porttool                                                  # 面板的端口列表里选 "sim"
porttool run --port sim --yes TestCase/plans/station6-poweron.json
cd TestCase/host/porttool_panel && python run.py --port sim   # T4-02，不用板子
```

**T4-03 是同一个脚本跑 Linux 版**：`--wsl Debian` 让面板在 WSL 里起（用 `Output/linux/PortTool`），浏览器仍是 Windows 上的 Chrome。先 `usbipd attach --wsl` 把串口挂进去，`--port` 写 WSL 里的名字，如 `/dev/ttyUSB1`。

**模拟板静态链接，不依赖任何 DLL。** 系统 PATH 上 `stlink_server` 目录带着一份 32 位的 `libwinpthread-1.dll`，动态链接时双击启动的面板会加载到它，模拟板一启动就以 `0xC000007B` 退出，面板上表现为连上 sim 却没有端口列表（2026-09-29）。

**T4-02 旁边还有一个 `naive.py`，问的不是同一个问题。** `run.py` 知道每个控件在哪、
该点哪一个；`naive.py` 只认页面：进一个端口，把印在上面的按钮按印出来的顺序挨个
按一遍，读它自己那一段给出的结论，同时查这一段的排版（说明在不在、按钮是不是排在
配置后面结果前面、要人插的对端是不是排在所有用例之前）。三个 2026-09-14 的 bug
`run.py` 看不见，因为它按的是代码里的位置，不是屏幕上的位置。

```bash
cd TestCase/host/porttool_panel
python naive.py --port COM5 --peer rs485=COM16     # 真板子，17 个端口 27 个用例
python naive.py --port COM5 --only sd              # 只走一个口
python naive.py --port COM5 --long                 # 连全量的 SD 压力和 SDRAM 全片扫描一起跑
```

⚠️ **默认跳过 `sdram.sweep`（整片 64 MB）。** 那两项验的是
器件不是面板，而且占掉这个脚本大半的时间 —— 抽查就能回答「按下去给不给得出像样的
答复」。要给器件下结论，加 `--long`，或者自己在面板上点那两段。用户 2026-09-14 定。

⚠️ 它不点「持续」（那是几小时的老化），不走模拟输出那张多点测量卡（要人读万用表），
`--peer` 一次只说一个口，形如 `rs485=COM16` —— 面板分不出哪个适配器
插在哪个端子上，这个脚本也分不出。

**造故障看面板怎么显示**（手敲进它的 stdin，或在面板底部的命令框里）：

| 命令 | 干什么 |
|---|---|
| `sim.help` | 列全部 |
| `sim.din 0x00` | 数字输入全低，看 din 判失败 |
| `sim.vdda 1800` | 基准坏掉，落在方案的 2400–2600 之外 |
| `sim.ain <ch> <mv>` / `sim.temp <ch> <mv>` | 单路模拟量读数 |
| `sim.link 0` | 拔网线（PHY 的 BSR 和 netif 一起变） |
| `sim.walk 1` | 数字输入自己轮转，看面板动起来 |

⚠️ **`sim.` 开头的命令真板上一条都没有**，由 `sim_main.c` 自己拦下，不进固件的 `dispatch()`。

⚠️ **它证明不了任何硬件行为。** 读数全是 stub 造的一块理想板子，每根对端线都当接好的；UART 中断收发、`rx_errors`、真 ADC、真 PHY 都不在里面。**它验的是 PC 侧的线路和方案文件。**
