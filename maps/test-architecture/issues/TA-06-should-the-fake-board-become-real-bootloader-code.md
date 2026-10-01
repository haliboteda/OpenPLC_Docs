# IAPTool 测试用的假板子：换成真 bootloader 代码，还是留着手写

Type: research
Opened: 2026-10-02
Status: open
Blocked by: -

## Question

`host/fakeboard/fake_board.py` 是用 Python 手写的 bootloader 应答，是 bootloader 协议的第二份实现。查清 bootloader 的网口代码（`IAPServer/`、lwIP）能不能像 PortTool 的模拟板那样编成 PC 程序当替身：要替换哪些硬件桩，lwIP 有没有现成的主机端口，大概多少工作量；做不了的话，用一条契约测试核对假板子和真板子回的东西一致要怎么写。

## 怎么算答完

两条路各给出：要动的文件、替换的桩、预估工作量、能覆盖和覆盖不到的用例（T1-18、T1-34）；给出推荐。
