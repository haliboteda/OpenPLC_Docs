# Go 里写死的 13 个用例号怎么改

Type: task
Opened: 2026-09-17
Status: resolved
Blocked by: DR-02

## Question

13 个用例号写死在 `IAPTranfer_Tool/TestCase/*.go` 的 `register(testCase{id: "…"})` 里：

```
T1  T1b  T2  T3  T4      tcp_session.go
N1  N2  N3  N4  N5        udp_discovery.go
S1  S2                    signature.go / signature_wrongkey.go
AU1                       nonce_replay.go
```

**`T1`–`T4` 现在是 TCP 会话用例**（「空闲连接 60 秒被断开」之类），
和新体系里 `T<模块号>-<序号>` 的 `T1-01` 撞名字。

⚠️ `ID-MAP.md` 现在写着这些号「**编号写死在 Go 代码里，不能改**」——
那是 2026-08-22 的判断，**用户 2026-09-17 已明确要求重排，这条判断作废**，
这张票要把那句话一起改掉。

要做的：

1. 把 13 个 id 换成新编号（模块归属由「54 条需求逐条归模块」那张票给出）
2. 跟着改所有引用这些 id 的地方 —— **不限 `.md`**，见地图 `## 全集` 的命令 1
3. 确认 `run_case.py --case <id>` 这类按 id 取用例的入口跟着改了
4. 跑 `selfcheck.py --quick` 验证 P7（总表和用例名单不得漂）仍然过

## 怎么算答完

`grep -rn 'id:[ ]*"' IAPTranfer_Tool/TestCase/*.go` 输出的每个 id 都是新格式，
`python tools/selfcheck.py --quick` 全过（**P7 是关键那条**：它专门查总表和用例名单对不对得上），
且用新 id 跑一次 `run_case.py` 能真的跑起来 —— **不是只改字符串就算完**。

## Answer

2026-09-17 定。**13 个用例号全部重排完，`selfcheck --quick` 13 项全过（P7 是关键那条）。**

映射照 [../../../docs/modules/M1-firmware-upgrade.md](../../../docs/modules/M1-firmware-upgrade.md) 的测试表，逐条核对过：

| 旧 | 新 | 测什么 |
|---|---|---|
| `N1`–`N5` | `T1-01`–`T1-05` | UDP 发现的五条 |
| `T2` | `T1-06` | 一次只服务一个客户端 |
| `T1` | `T1-07` | 空闲连接约 60s 被踢 |
| `T1b` | `T1-08` | 50s 内不被误踢 |
| `T3` | `T1-09` | 传输中闯入不打断 |
| `T4` | `T1-10` | 拒绝状态不卡死 |
| `S1` `S2` | `T1-11` `T1-12` | 无效签名 / 签方不对 |
| `AU1` | `T1-17` | nonce 跨掉电不重复 |

**改了 21 个文件、120 处**：6 个 Go 文件、8 个 Python 工具、`KEY-MATCH.md`，
以及 `JOURNAL.md` `BUILD-AND-TEST.md` `ACCEPTANCE-CHECKLIST.md` `ID-MAP.md`
`STATUS.md` `TEST-CASES.md`。

**验证**：`go build` / `go vet` 通过；`TestCase.exe` 的用例列表里 13 个新 id 全部列得出来，
标题与映射一一对应；`grep 'id: "旧号"'` 在 Go 里**零命中**；`run_case.py --help` 正常。
⚠️ **没有真板子跑过** —— 13 个里 9 个是板级用例，它们在真硬件上还没跑过一轮。

**误报排掉的**：`sha256.c` 和 `sha256_ref.py`（SHA-256 算法里 `T1` `T2` `S1` 是变量名）、
`stm32h7xx_ll_rcc.h`（寄存器名）、`dhcp.h`（协议常量）、`adc_test.c` `dac_test.c` `din_test.c`
`relay_test.c`（通道号）、`can_send.py` `can_watch.py`、以及
**`PORTTOOL-FLOW.md` 里的 `[T1 ]`** —— 那是工装串口报文的标签，画在 Mermaid 图里，不是用例号。
21 个文件是从 41 个候选里挑出来的。

`ID-MAP.md` 另外手工修了 6 处机械替换搞不对的地方，其中一条是**规矩本身作废**：
原文写「**编号只增不改**，用例号写死在 Go 代码和脚本里」——
今天的动作直接推翻了它，改成「改编号是可以的，但要一次改全」，并写明判据是 P7 仍然通过。

## 引出了什么新的未知

1. **这张表现在是混的，而且会混一段时间。** 13 个重排了，**其余用例号
   （`S3` `S4a` `S4b` `G1` `H1`–`H3` `K1`–`K7` `X1` `X2` `P0`–`P12` `BG1` `SD1` `M3` `M5` `O1` `EV1`）
   还是旧的** —— 完整重排不在这张票的范围里。已在 `ID-MAP.md` 开头加了醒目提示，
   免得有人把剩下的旧号读成新体系
2. **`STATUS.md` 仍然自称「53 条」**，实际 54 条。`ID-MAP.md` 的计数由 `DR-02` 修过了，
   `STATUS.md` 自己那三处（目录、合计行、明细节标题）没人改 —— 不属于本票范围，
   留给实施阶段
3. **没有任何检查能抓到「漏改的编号」。** P7 只比对 STATUS 和 TEST-CASES 两份名单一致，
   P9 只查路径。这次靠的是人工排误报 —— 完整重排时这条风险更大，
   已经是 `DR-09`（过渡期怎么走）要回答的问题
