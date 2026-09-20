# 有些叶证书驱动不了重启握手

Type: task
Opened: 2026-09-20
Status: open
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
（这条本身记在 `waiting/WAITING-ON.md` 的「交接时那两个坏字节」一节，2026-09-19 实测过
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
