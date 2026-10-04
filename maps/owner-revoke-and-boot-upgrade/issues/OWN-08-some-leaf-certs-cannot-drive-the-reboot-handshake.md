# 有些叶证书驱动不了重启握手

Type: task
Opened: 2026-09-20
Status: resolved
Blocked by: OWN-09

## Question

**同一把根签发的两张叶证书，一张能把板子从 app 请回 bootloader，另一张不能。**
app 收到 `openplc_server_reboot` 之后不重启，继续以 `CUSAPP` 应答 UDP 发现。

2026-09-20 两次独立观察，**同一次启动周期内**（同一个 app、同一把 owner 根、相隔 36 秒）：

| 时间 | 证书 | 结果 |
|---|---|---|
| 15:58:15 | `spared_leaf` | ✅ 重启成功，板子进 bootloader |
| 15:58:51 | `third_leaf` | ❌ app 不理会，三次发现全部超时 |

更早一次（15:34 / 15:38）是同样的形状：一张旧证书能用、一张新证书不能。
**当时记成「未查清的偶发」，现在可复现，所以不是偶发。**

⚠️ **不是 2026-09-20 那批改动引入的** —— 第一次观察发生在改 `owner_root_ro.c` 之前，
用的是当时板上那个 app。

### 为什么要紧

重启握手是**委托证书持有者**把板子弄进上传模式的唯一软件手段
（`$TOOL/IAP_Ether.go` 的 `authenticatedUDPReboot`）。它不工作，那个人就只能到现场按 BOOT0 ——
而「认领之后的操作全部走签名、不需要人到板子跟前」是 M2 明确写下的性质。

### 诊断卡在哪

**app 跑起来之后 RS232 收发器是关断的**，`printf` 出不来，所以看不到 app 侧的判断过程
（这条本身记在 `work/TODO.md` 的「交接时那两个坏字节」一节，2026-09-19 实测过
`PB10` 为低）。要看见 app 说什么，得先有一个**主动 `digitalWrite(RS232_EN_Pin, HIGH)`** 的 sketch。

`T1-16` 覆盖不到这条：重启握手在 core 侧的 `udp_server.c` / `iap_auth.c`，
不在那个主机台子上。

⚠️ **2026-09-20 调查受阻**：做了能说话的探针之后发现，
**app 里的 `printf` 压根没有输出通道**（实测 `printf` 0 行 / `Serial_Test` 18 行）——
而要区分的三种结局恰恰只差在那几行 `printf` 上。
**这张票被 [app 里的 printf 没有输出通道](OWN-09-printf-has-no-output-path-in-an-app.md) 挡着**，
先把那条修了才查得下去。

## 怎么算答完

1. **做一个能说话的探针 app**（开 RS232 收发器），复现一次成功、一次失败，把 app 侧拒绝的那一行抓出来
2. 说清**判据是什么** —— 哪一类叶证书会被拒、为什么，以及它和 `owner_root_ro_is_revoked()`、
   nonce TTL、证书验签三者中的哪一个有关
3. 如果是缺陷，登记需求/用例号；如果是设计（例如某种刻意的限制），写进 [M2 归属与信任](../../../docs/modules/M2-ownership.md)

⚠️ **暂时的绕行办法已经在用**：`run_revoke_leaf.py` 里把板子请回 bootloader 改用
**根密钥自签**（`move_to_bootloader_selfsigned()`），那条路可靠。所以这张票不阻塞作废那套用例。

## 2026-09-20 上板调查：现象复现，范围大幅缩小

`printf` 通了之后（见 [app 里的 printf 没有输出通道](OWN-09-printf-has-no-output-path-in-an-app.md)），
拿同一张证书反复试：**有时成功、有时失败** —— 所以这**不是「某些证书天生不行」，是间歇性的**。
票的标题据此已经不准确，但先不改，等根因定了一起改。

**失败那一次的决定性观察**：app 在跑（心跳不断，`printf` 和 `Serial_Test` 两个通道都在输出），
但收到重启请求时**一个字都没打印**。

### 已经排除的（都是实测或查实，不是推测）

| 假设 | 怎么排除的 |
|---|---|
| 冷却期（`REBOOT_COOLDOWN_MS` 10 秒） | 那条路径**会打印** `Reboot request ignored: still within cooldown`，实测时一行没有 |
| 证书或签名验不过 | 同理，那条路径会打印 `Rejected unauthenticated openplc_server_reboot request` |
| UDP 包跨 pbuf 段、`p->len` 只拿到前半截 | `PBUF_POOL_BUFSIZE = 1524`（`OpenPLC_Net/src/lwipopts_default.h:73`），远大于命令的 ~407 字节，**不会跨段** |

### 还剩的两条，下一轮从这里开始

按 `udp_server.c` 的代码，静默只剩两种可能：

1. **`sscanf(recv_buf, "openplc_server_reboot %256s %128s", ...)` 返回 ≠ 2** —— 那个分支整个被跳过，不打印任何东西
2. **包根本没到 app** —— `CM_Reboot` 用 `sendUDPNoResponseOnPort` 发出，不等应答，所以 PC 那边无从分辨

**怎么分开这两条**：`udp_server.c` 里已经有 `udp_server_recv_counter`、
`udp_server_last_rx_len_value`、`udp_server_last_rx_tick_ms` 三个全局计数。
**让探针 sketch 把它们打出来**，失败那一次看计数有没有涨、收到的长度是多少 ——
涨了且长度是 407 就是第 1 条，没涨就是第 2 条。

⚠️ **顺带发现的一个隐患（不是本票的根因，但该记）**：那段接收码用 `p->len` 而不是
`p->tot_len` 取长度。今天因为 `PBUF_POOL_BUFSIZE` 够大而碰不到，但包一旦跨段就会静默截断。


## 2026-09-20 第二轮：问题在 IAPTool 侧，app 已证明是好的

给探针加上 `udp_server.c` 自带的收包计数（`openplc_udp_server_recv_count()` 等，
getter 本来就声明在 `OpenPLC_IAP_Autostart.h`，**没改产品代码**）之后，得到一组对照：

### 手工直接发 UDP（python socket → 192.168.0.3:56865）

| 发什么 | app 收到 | 回复 |
|---|---|---|
| `openplc_server_where_r_y`（24 字节） | ✅ `rx len=24` | 47 字节身份串 |
| `openplc_server_reboot_challenge`（31 字节） | ✅ `rx len=31` | **32 字节 nonce** |
| **407 字节的 `openplc_server_reboot ...`** | ✅ **`rx len=407`** | ——（内容是垃圾，预期不重启） |

**app 全程活着，心跳不断，收到了完整的 407 字节。**
这同时再次证实包不跨 pbuf 段（`p->len` 拿到了全长）。

### 同一时刻，IAPTool 跑同样的握手

| 观察 | 值 |
|---|---|
| app 收到的包 | **只有 1 个，`len=24`**（发现命令）—— challenge 和 reboot 都没到 |
| IAPTool 拿到 nonce 了吗 | **拿到了**（拿不到会报 `reboot challenge request failed`） |
| app 重启了吗 | **没有** —— 心跳 36 次不间断，没有任何启动横幅 |
| app 崩了吗 | **没有** —— 同上 |

**这两组观察无法用 app 侧解释。** 同一个地址、同一个端口（`getPort()` 默认 56865，已查）、
同样的字节，手工发得到、IAPTool 发不到，而 IAPTool 又确实收到了来自某处的 nonce。

### 下一轮从哪开始

问题在 **PC 侧**，不在固件侧。两个具体方向：

1. **IAPTool 到底把包发去了哪里** —— 在 `sendUDPWithResponseOnPort` / `dialUDPBoard` 里把
   `conn.LocalAddr()` 和 `conn.RemoteAddr()` 打出来。这台机器可能有多个网卡，
   广播（发现）和单播（challenge）可能走不同接口
2. **那个 nonce 到底是谁回的** —— 抓包（Wireshark）最直接；或者把收到的字节打印出来，
   看它是真 nonce 还是发现应答的残留

⚠️ **票的标题已经不准** —— 和叶证书无关，也不是板子的毛病。根因定了一起改。


## 2026-09-20 第三轮：主路径实测正常，严重性大幅下降

给 `dialUDPBoard` / `sendUDPWithResponseOnPort` 临时加了诊断打印（**已撤销**，问题不在那），
拿**存在的证书 + 正常调用**跑一次完整握手：

| 步骤 | 结果 |
|---|---|
| dial（发现） | `local=192.168.0.2:xxxxx -> remote=192.168.0.3:56865` ✅ |
| 发现应答 | 47 字节身份串 ✅ |
| dial（challenge）+ 应答 | **32 字节 nonce** ✅ |
| dial（reboot） | ✅ |
| 板子 | `** Checking Starting Mod ...` → **`** UPLOAD Mod ... (ethernet upload requested)`** ✅ |
| IAPTool | `reached bootloader: True` ✅ |

**接口选择没有问题**（单播和广播都走 192.168.0.2），**整条路径在正常情况下是好的**。

### ⚠️ 之前的部分「失败」是调查方自己造成的

前几轮用**绝对路径**传 `--key` 时，IAPTool 直接
`FATAL Cannot authenticate to this board: failed to read signing key ...`，
**challenge 压根没发出去** —— 这正好解释了那几次 `app 只收到 1 个包（len=24）`。
同一个文件改用**相对路径**调用则一切正常。

⚠️ **追加更正**：后来单独验了——`IAPTool pubkey` 用相对路径、绝对路径（反斜杠）、绝对路径（正斜杠）**三种写法都能读到同一把密钥**。所以「绝对路径读不到」也不成立，那次 `FATAL` 几乎肯定是调查脚本自己的转义问题把路径写坏了。

### 还剩什么

最早那两次失败（2026-09-20 15:34 用 `keys2/doomed_leaf`、15:58 用 `keys8/third_leaf`）
的证书**确实都存在**（已逐个核对目录），而且当时 IAPTool 的日志显示它读到了证书。
**那两次仍然没有解释，也再没复现过。**

所以这张票**不关，但降级**：不再是「每次上传都可能挂」的阻塞问题，
而是「见过两次、无法复现」的待观察项。**下次它再出现时，app 现在能说话了**
（`printf` 通了，探针会打印收包计数），当场就能分辨是哪一种。


## 停手声明（2026-09-20）

**今天为这个现象提过五个假设，全部被实测推翻：**
UDP 包跨 pbuf 段、app 处理长包时崩溃、app 重启但没进 bootloader、
证书文件不存在、绝对路径读不到密钥。

**主路径已经反复实测正常**，最早那两次再没复现过。
继续猜是浪费——这张票等它**自己再出现**，到时候探针会当场告诉我们是哪一种。


## 2026-09-21 第四轮：今天这次完全解释清楚了，但票先不关

**今天的失败是拿错钥匙，不是缺陷。** 板子昨天被 `Output/revoke-run/owner_r3.pem` 认领
（`getowner` 回「Claimed at generation 4」，公钥逐字节相同），而 `tools/enter_bootloader.py`
调的是 `IAPTool ether <big> <ip>`，**不传 `--key`** —— 用默认那把公开根签的证书，板子正确拒绝。
换成 `--key=owner_r3.pem` 之后一次就进了 bootloader。

**证据链**（探针带 `udp_server.c` 自带计数，`printf` 已通）：

| 观察 | 值 |
|---|---|
| 收包计数 | `len=31`（challenge）→ **`len=407`（重启命令，完整）** |
| 407 的构成 | `21 + 1 + 256 + 1 + 128`，和 `IAP_Ether.go:301` 拼的串一致 |
| app 打的那行 | **`Rejected unauthenticated openplc_server_reboot request`** |

⚠️ **上一轮记的「一个字都没打印」是错的** —— 那是抓日志时只 grep 了 `udp rx=`，
把这行滤掉了。板子一直在说原因。据此，`sscanf` 返回的是 2，**分支进去了，是验签没过**，
主机上拿同样的 407 字节跑同一个 `sscanf` 也返回 2。

**为什么不关**：本票最早的观察是「**同一把根签发的两张叶**，一张行一张不行」。
今天解释的是「根本就不是那把根」。两者不是同一个现象，**旧观察仍未复现、也仍未解释**。

### 该改的东西

`enter_bootloader.py` 对**已认领的板子**无效，而它自己的文档没说这件事。
要么加 `--key` 透传，要么在板子已认领时给出可操作的报错，而不是「board does not appear
to be in the bootloader」。已记进 `work/TODO.md`。

## 2026-09-21 晚：那个已查清的病根修掉了，票仍然开着

`enter_bootloader.py` 调 `IAPTool ether` 时不传 `--key` —— 这条在真板子上复现并修了：

- 复现条件是**板子已认领**。当天早些时候板子处于未认领状态，脚本能用；重新认领（generation 1）之后再跑，板子打印
  `Rejected unauthenticated openplc_server_reboot request`，而脚本只说「board does not appear to be in the bootloader」
- **修了两处**：加 `--key` 并透传给 `IAPTool`；失败时读它**本来就已经抓到**的板子日志，
  看到 `Rejected unauthenticated` 就点名「这块板已认领，这次请求是公开根签的」
- 两条路都验过：不带 `--key` 退出码 1 且点名原因，带 `--key` 退出码 0 且进了 bootloader

⚠️ **本票不关**：它记的是最早那个观察 —— **同一把根签发的两张叶，一张能驱动重启握手、另一张不能**。
那个还没复现过，和「拿错钥匙」不是一回事。**等它自己再出现。**

## 2026-09-22：复现了两次，但把「叶证书」这个说法推翻了

上板那一轮里，用叶证书驱动的重启握手**失败了两次**，都在 `run_revoke_leaf.py` 的
前置步骤和 `run_flashboot.py` 的 `--sign-with-leaf` 上。板子当时活得好好的（照常应答
`CUSAPP` 发现请求），只是不理会那条重启请求。

⚠️ **但拿同一把失败的叶证书单独重试，3 次全部成功。** 所以变量不是证书 ——
票名里「有些叶证书」这个说法站不住。

两次失败有一个共同点，成功的那些没有：**都紧跟在 app 刚启动之后**（一次在
`reset_and_capture` 之后立刻发，一次在一次成功上传之后约一分钟）。成功的几次
板子都已经稳定运行了一阵。**像是 app 侧的就绪时序**，不是密钥材料。

**还没定位到根因**，所以这张票不关。下一步该看的是 app 启动到它开始受理
`openplc_server_reboot_challenge` 之间那段窗口有多长、期间请求被丢在哪一层。

## Answer

2026-09-22 定案：**和叶证书无关。丢包 + 重试次数不对称。**

请一个跑着 app 的板子回 bootloader，是三个 UDP 报文、全程没有任何确认：
challenge 出去 → nonce 回来 → 签好的 reboot 出去。**这一整串原来只试一次**，
而紧挨着它的 identify 步骤试 **三次**。

于是同样的丢包率，在 identify 上几乎看不见，全部砸在这一串上 ——
这就是「同一把根的两张叶，一张行一张不行」的真正来源：**不是叶，是运气**。

### 证据

| | |
|---|---|
| 2026-09-22 复现 **两次** | 两次都在 `run_revoke_leaf.py` / `run_flashboot.py` 的前置步骤 |
| **同一把失败的叶单独重试 3 次，全部成功** | 所以变量不是证书材料 |
| 两次失败时板子都在正常应答发现请求（`CUSAPP`） | 所以也不是「板子还没准备好」—— 我一度这么猜，错了 |
| 源码核实 | identify 重试 3 次（`IAP_Ether.go`），challenge 0 次，reboot 0 次且无确认 |

### 修了什么

`IAP_Ether.go` 的 `rebootAttempts = 3`：请求 → 等 → 看板子回没回来，没回来就再请一次。
重复请求是安全的 —— 已经重启的板子在 bootloader 里，那里没有 reboot 命令，报文被忽略。

**改完实测**：连续五轮完整的「app → bootloader → 上传」，**五轮全过**，
其中 **两轮触发了重试** —— 那两轮在改之前就是彻底失败。

## 引出了什么新的未知

**一个**：`openplc_server_reboot` 这条命令**本身没有任何应答**，所以工具永远无法直接确认
它到没到，只能靠「板子是不是回来了」间接推断。现在的重试把这件事从「一次机会」
变成「三次机会」，但**没有改变它是不可确认的**这个性质。

真要根治是给它加一条应答，那会动线上协议，**不在这一版的范围内**。
⚠️ 记在这里而不是开新票：今天没有任何东西被它挡住，重试已经把现象压到看不见了。
