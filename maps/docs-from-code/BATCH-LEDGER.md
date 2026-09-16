# 逐文件台账

**[CORPUS.md](CORPUS.md) 里每一个文件都要在这里有一行** —— 搬了什么 / 什么都没搬，两种都要写。
对不上的文件数必须是 0，那是「全做完」的判据。

## 批 1 · boot（2026-09-16）

⚠️ **`docs/boot/` 原来只有 `JOURNAL.md` 一份**，所以这一批不是「比对补充」，
是**从注释里把 boot 的设计文档写出来**。产物：[../../docs/boot/BOOT-SEQUENCE.md](../../docs/boot/BOOT-SEQUENCE.md)。

⚠️ **域分错了要纠正**：语料按目录归的 `boot`，其中 **411 行其实属于 `security`**
（`owner_slot`、`iap_auth`、`iap_cert`、`fw_verify`、`fw_pubkey`、`iap_keyderive`）——
它们归批 2，不在本批。

| 文件 | 注释行 | 处理 |
|---|---|---|
| `IAPServer/IAP_server.c` | 196 | ✅ 取出：两阶段启动、Phase 1 为何先于外设、BOOT0 一票否决、跳转顺序、`naked` 的理由、命令分帧、写 flash 的暴露窗口 → `BOOT-SEQUENCE.md` |
| `IAPServer/IAP_boot_handoff.h` | 59 | ✅ 取出：交接记录为何在 SRAM4 的四条理由、地址是链接脚本保证、枚举值只许追加 → `BOOT-SEQUENCE.md` |
| `IAPServer/bootloader_state.h` | 83 | 🟡 大部分 `JOURNAL.md` 已有（flash word、防篡改链、M 记录 8 格）。**补了一条只活在注释里的**：被拒绝的认证只记 RAM 不落 flash，理由是磨损与拒绝服务 |
| `LWIP/Target/ethernetif.c` | 153 | ✅ 取出：MAC 从 UID 派生的算法与理由（生成的 MAC 是编译期常量，两块板同网段会撞）→ `BOOT-SEQUENCE.md`。**用户 2026-09-16 批准后**给两边注释补了引用位置。⚠️ **发现 core 侧 `openplc_make_mac_from_uid()` 原本一句解释都没有** —— 同一个设计只有 bootloader 一侧写了。其余 `@brief` 是 ST 模板，没动 |
| `IAPServer/IAP_boot_handoff.c` | 47 | ✅ 取出：**冷启动首次访问必须是写**（SRAM4 与 ECC 校验位上电随机、对不上，先读会 BusFault）、cache 维护为何无条件正确、读回校验是旧方案缺的那条、四种认不出来的分支 → `BOOT-SEQUENCE.md` |
| `IAPServer/bootloader_state.c` | 37 | ✅ **什么都没搬** —— 逐条比对后 `JOURNAL.md` 已经全有（0xFF 空格、一个 flash 字、`prev_hash` 12 字节、`_Static_assert`、唯一会擦的地方、认不出记录的三种情况）。**这是「文档已经最全」的一个实例** |
| `IAPServer/udp_server.c` | 28 | ✅ 取出：发现限流的完整四步论证 → `BOOT-SEQUENCE.md`。**用户 2026-09-16 批准后**把两边分叉的注释统一成「结论 + 一句话 + 引用位置」，三份拷贝（boot / core 仓 / `$CORE_LIVE`）一起改 |
| `IAPServer/IAP_server.h` | 15 | ✅ 取出：两阶段接在 CubeMX 的哪两个 USER CODE 点上 → `BOOT-SEQUENCE.md`。⚠️ 文件里有一行中文注释「添加全局同步对象」提到 FreeRTOS 的 `xDataMutex` / `xCommandTaskHandle`，**本工程没有 FreeRTOS，疑似死代码**，没动，记在这里 |
| `IAPServer/tcp_server.c` | 13 | ✅ 取出：单会话、60 秒静默超时（lwIP 500 ms 粗 tick）、接收状态的所有权 → `BOOT-SEQUENCE.md` 新增一节 |
| `LWIP/Target/ethernetif.h` | 9 | ✅ **什么都没搬** —— 全是 ST 的版权与许可头，生成的 |
| `IAPServer/udp_server.h` | 3 | ✅ **什么都没搬** —— 只有文件名、创建日期、作者 |
| `IAPServer/tcp_server.h` | 2 | ✅ **什么都没搬** —— 同上 |

## 批 1 结果：12 / 12，全部处理完

⚠️ **「什么都没搬」的有 4 个文件** —— 那不是没做，是**比对后确认文档已经全了**。
两种记录都要写，否则分不出「查过」和「忘了」。

**改了代码注释的只有 2 处**，都经用户当场批准（跨仓镜像第 1、2 条）：
统一了分叉的措辞，并按「写理由要带引用位置」补上指向文档的那一句。
三份拷贝（bootloader / core 仓 / `$CORE_LIVE`）同步改。

### 验证

- `selfcheck --quick` 13 项全 PASS，**含 P2（镜像一致）和 P3（live == repo）**
- **bootloader 固件编过：0 errors / 0 warnings，102,904 字节**
- 完整 `selfcheck` **18 项全 PASS**（含 H2/H4/K1-K7/X1-X2/P4）
- ⚠️ **core 没有被编译过。** `P5`（Arduino 示例构建）根本没出现在这次 `selfcheck` 里 ——
  改的是 `.c` 文件里的注释，风险接近零，**但这是推测，不是实测**。
  要证明得单独跑 `TestCase/host/examples_build/build.py`

## 批 2 · security（2026-09-16）

35 个文件、729 行。⚠️ **和批 1 不一样：这个域本来就有像样的文档**
（`OWNERSHIP.md` 264 行 + `KEYS.md` + 配图 html），所以这批是真的**比对补全**。

| 文件 | 注释行 | 处理 |
|---|---|---|
| `IAPServer/iap_auth.{c,h}` | 75 | ✅ **整套挑战应答机制文档里几乎不存在** —— `nonce` 全文只出现过 1 次、`RNG` **0 次**。新建 [../../docs/security/CHALLENGE-AUTH.md](../../docs/security/CHALLENGE-AUTH.md) |
| `IAPServer/iap_cert.h` | 36 | ✅ 取出：一个镜像要过的两道检查、为什么两条缺一不可、为什么拆成两个函数 → `CHALLENGE-AUTH.md` |
| `IAPServer/owner_slot.h` | 104 | 🟡 绝大部分 `OWNERSHIP.md` 已有（签名前缀 88、uid 绑板、format_ver、告警判据）。**补了三条**：记录必须是整数个 flash 字（H7 一次编程 256 位）、签 `generation` 是为了挡重放进后面的槽、`format_ver` 从第一版就在是刻意的 |
| `iapcert/iapcert.go`、`owner.go`、`auth.go` | 124 | 🟡 大部分已有。**补了两条**：签名必须覆盖板子最终写入的确切字节（`uid` 是板子自己填的）、流水号写失败只报警告不当错误 |
| `IAPServer/owner_slot.c` | 141 | ✅ **什么都没搬** —— 逐段比对后 `OWNERSHIP.md` 的状态机 / 三个操作 / 记录格式 / 诚实的上限四节已经覆盖 |
| 其余 24 个小文件 | 216 | ✅ 逐个扫过。绝大多数是「Mirrors X」式的镜像指针，已足够。**补了两条**：验签必须用 `owner_slot_root()` 不能用内置的 `fw_public_key`（否则认领是摆设）、core 侧 `owner_root_ro` 只读镜像的存在与约束 |

**批 2 结果：35 / 35 全部过完。** 新增 `CHALLENGE-AUTH.md`，`OWNERSHIP.md` 补了 7 条。
其中 5 个测试侧文件（`iapcert_test.go` / `run_cases.py` / `sha256_ref.py` / `fake_board.py` / `ecdsa_verify.py`）
的内容**归到测试设计文档**，见批 3–5。

⚠️ **留给「测试设计文档」的一条**（用户 2026-09-16 定批 3–5 汇总进那份）：
`iapcert` 做成 package 而不是 main 的一部分，是为了让用例能 `import` 它 ——
**一个自己重新实现了密码学的用例，只能证明那个重新实现和它自己一致。** 这是测试设计原则，不是安全设计。
