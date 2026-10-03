# 0.1.3 在模拟环境里能测的都测掉

## 怎么看进度（不用问任何人）

```
python tools/list_wayfinder_map_frontier.py --all
```

## Destination

0.1.3（决策 83：三个开发分支上的全部代码）里，模拟环境看得见的行为都有自动跑的用例并通过；模拟看不见的逐条列出，留给上板。

## Notes

- **带执行**（用户 2026-10-03：「按你推荐做必要的事」）：票定完就写文档、用例和必要的模拟件；先文档再代码，只做必要的
- 模拟手段三套：Renode（真 bootloader + 真 app 二进制，`$TEST/host/renode/`，用例 `T3-05`）、bootloader 替身（`$TEST/host/bootstand/`）、工装模拟板（`sim`）
- Renode 每个外设有没有模型，2026-09-27 查过：[REN-02-findings.md](../renode-simulation/REN-02-findings.md)。**模拟做不到的不硬做**，归到「只能上板」
- 用到的 skill：`research`（research 票）、`grilling`（grilling 票）
- 开票 / 关票 / 算前沿照 [图与票的约定](../MAP-AND-TICKET-CONVENTION.md)

## 全集

```
grep -ohE "\*\*R[1-3]-[0-9]+\*\*" OpenPLC_Docs/docs/modules/M[1-3]-*.md | sort -u
```

2026-10-03 是 M1–M3 的全部需求。关最后一张票前重跑：每一条落在「有模拟用例」「只有主机用例」「只能上板」三类之一，第三类写明为什么。

## Decisions so far

- [替身补齐：驱动、手势、故障注入、撤销、比版本](issues/SIM-07-stand-in-additions.md)：`run_lifecycle.py` 在替身上跑掉电、比版本（`T1-38`）、恢复出厂、撤销，七条全过
- [例程行为检查放进哪条用例、每个例程判什么](issues/SIM-06-which-case-holds-the-example-behaviour-checks.md)：新用例 `T3-11`，`usb=CDC` 读 UART4；有模型的例程都判；不装 TAP
- [SD 卡在 Renode 里能不能读写](issues/SIM-03-does-sd-work-in-renode.md)：SD 读写和 YMODEM 收文件在 Renode 里都通；插拔只模拟到检测脚
- [例程的网口在 Renode 里通不通](issues/SIM-02-does-ethernet-work-in-renode.md)：补 PHY 后网口、DHCP、发现都通；完整上传要 TAP 驱动
- [例程的 `Serial` 在 Renode 里怎么看得到](issues/SIM-01-how-to-see-serial-in-renode.md)：`usb=CDC` 另编一版，`Serial` 走 UART4；USB 上传只能上板
- [标着「真板子」的用例里，哪些替身或 Renode 能跑](issues/SIM-05-which-real-board-cases-the-stand-in-can-run.md)：53 条里替身已跑通 19、补驱动能跑 20、替身或 Renode 2、Renode 4、只能上板 8
- [bootloader 开机把输出置 0，在 Renode 里判](issues/SIM-04-bootloader-outputs-in-renode.md)：用例 `T1-37` 通过，BOR 检查在 Renode 里也能判
## Not yet specified

- **KNX 的 IP 那一半**：网口在 Renode 里通了之后（看「例程的网口在 Renode 里通不通」），能不能用 xknx 对着模拟板收发 KNXnet/IP 组报文
- **USB 上传在模拟里走不走得通**：看「例程的 `Serial` 在 Renode 里怎么看得到」查出的 USB 结论

## Out of scope

- **物理量**：AO 实际电流、继电器真吸合、DI 门限电压、BOR 掉电复位、真断电、TRNG 抓包、示波器要量的 —— 模拟没有模拟电路
- **KNX TP 真总线和 ETS 互通**：Renode 的定时器做不出 104 µs 位时序和输入捕获；链路逻辑已由主机用例 `T3-09` 覆盖
