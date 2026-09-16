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
| `IAPServer/IAP_boot_handoff.c` | 47 | ⏸ 未处理 |
| `IAPServer/bootloader_state.c` | 37 | ⏸ 未处理 |
| `IAPServer/udp_server.c` | 28 | ⏸ 未处理。⚠️ 含镜像第 2 条，且**两边注释已确认分叉** |
| `IAPServer/IAP_server.h` | 15 | ⏸ 未处理 |
| `IAPServer/tcp_server.c` | 13 | ⏸ 未处理 |
| `LWIP/Target/ethernetif.h` | 9 | ⏸ 未处理 |
| `IAPServer/udp_server.h` | 3 | ⏸ 未处理 |
| `IAPServer/tcp_server.h` | 2 | ⏸ 未处理 |

**本批 12 个文件，处理完 3 个（338 行），未处理 9 个（308 行）。批 1 没做完。**
