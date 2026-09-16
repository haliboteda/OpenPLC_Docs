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
| `LWIP/Target/ethernetif.c` | 153 | ⏸ **未处理**。大部分是 ST 的 `@brief` 模板；我们自己的是 USER CODE MACADDRESS 块，**那是九条跨仓镜像之一**，按规矩改动要问用户。留到专门一轮 |
| `IAPServer/IAP_boot_handoff.c` | 47 | ✅ 取出：**冷启动首次访问必须是写**（SRAM4 与 ECC 校验位上电随机、对不上，先读会 BusFault）、cache 维护为何无条件正确、读回校验是旧方案缺的那条、四种认不出来的分支 → `BOOT-SEQUENCE.md` |
| `IAPServer/bootloader_state.c` | 37 | ✅ **什么都没搬** —— 逐条比对后 `JOURNAL.md` 已经全有（0xFF 空格、一个 flash 字、`prev_hash` 12 字节、`_Static_assert`、唯一会擦的地方、认不出记录的三种情况）。**这是「文档已经最全」的一个实例** |
| `IAPServer/udp_server.c` | 28 | ⏸ 未处理。⚠️ 含镜像第 2 条，且**两边注释已确认分叉** |
| `IAPServer/IAP_server.h` | 15 | ✅ 取出：两阶段接在 CubeMX 的哪两个 USER CODE 点上 → `BOOT-SEQUENCE.md`。⚠️ 文件里有一行中文注释「添加全局同步对象」提到 FreeRTOS 的 `xDataMutex` / `xCommandTaskHandle`，**本工程没有 FreeRTOS，疑似死代码**，没动，记在这里 |
| `IAPServer/tcp_server.c` | 13 | ✅ 取出：单会话、60 秒静默超时（lwIP 500 ms 粗 tick）、接收状态的所有权 → `BOOT-SEQUENCE.md` 新增一节 |
| `LWIP/Target/ethernetif.h` | 9 | ✅ **什么都没搬** —— 全是 ST 的版权与许可头，生成的 |
| `IAPServer/udp_server.h` | 3 | ✅ **什么都没搬** —— 只有文件名、创建日期、作者 |
| `IAPServer/tcp_server.h` | 2 | ✅ **什么都没搬** —— 同上 |

**本批 12 个文件：处理完 10 个（451 行）。**

**剩 2 个，都含跨仓镜像，按 `ARCHITECTURE.md` 的规矩要先问用户：**

| 文件 | 注释行 | 为什么要问 |
|---|---|---|
| `LWIP/Target/ethernetif.c` | 153 | 我们自己的那块是 USER CODE MACADDRESS —— **镜像第 1 条** |
| `IAPServer/udp_server.c` | 28 | **镜像第 2 条**，且两边注释已确认分叉（core 那份丢了「at 115200 baud」） |

⚠️ **这一批「什么都没搬」的有 4 个文件** —— 那不是没做，是**比对后确认文档已经全了**。
两种记录都要写，否则分不出「查过」和「忘了」。
