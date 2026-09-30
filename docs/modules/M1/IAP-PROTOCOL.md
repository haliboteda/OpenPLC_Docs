# IAP 协议 · bootloader 和 app 在线上认哪些命令

> ⚠️ **`takeown` / `getpubkey` / `flashboot` 三行按[决策 72](../../tables/DECISIONS.md) 写的是目标设计，代码尚未实施**，见 [work/TODO.md](../../../work/TODO.md)「出厂无根、第一次上传自动认领」。其余各行以代码为准。

**这份是命令一览。** 每条命令的格式、要不要认证、会回什么。
为什么是这个形状，各自的专门文档里写着，这里只给指针。

实现：bootloader 在 [`IAP_server.c`](../../../../open_plc_cube_ide/IAPServer/IAP_server.c) 的 `process_command()`
和 [`udp_server.c`](../../../../open_plc_cube_ide/IAPServer/udp_server.c)；
app 在 core 的 [`udp_server.c`](../../../../open_plc_arduino/libraries/OpenPLC_IAP/src/udp_server.c)。
**命令表以代码为准**，两边对不上时是这份文档过期了。

## 传输

| 通道 | 谁在听 | 端口 / 形式 |
|---|---|---|
| TCP | bootloader | `OPENPLC_SERVER_PORT`（56865），定义在 `$BOOT/Core/Inc/IAP_config.h` |
| UDP | bootloader 和 app | 同一个端口。只收发现和（app 的）重启请求 |
| USB CDC | bootloader | 和 TCP 同一个命令解析器 |

**TCP 和 CDC 上一条命令以 `\n` 或 `\r` 结尾。** 没有结尾的残片 500 ms 后丢弃。
一条命令可以跨多个 TCP 段 / USB 包到达。

## bootloader 的命令（TCP / CDC）

| 命令 | 认证 | 回答 |
|---|---|---|
| `openplc_server_where_r_y` | 无 | 身份串，五段 `名称_UID_角色_卡包版本_-`，角色是 `BOOTLD` 或 `BOOTLD-INVALID`（没有可启动的 app） |
| `ping` | 无 | `OK` |
| `info` | 无 | bootloader 版本串 |
| `getuid` | 无 | 机器 ID（十六进制） |
| `getpubkey` | 无 | 板子**当前信任的根**公钥，128 个十六进制字符；**没有根时回 `none`**（实施时定具体字样）。IAPTool 靠它判断要不要自动认领 |
| `getowner` | 无 | 当前 owner 记录的 generation，未认领为 `0` |
| `getapprevoked` | 无 | `yes` / `no` / `none` —— 签装着那个 app 的叶有没有被撤销；`none` 是没有可启动的 app |
| `authchallenge` | 无 | 一个 nonce（32 个十六进制字符）；RNG 失败回 `ERR`。见 [CHALLENGE-AUTH.md](CHALLENGE-AUTH.md) |
| `takeown <公钥hex>` | **不设门**（决策 72），USB 或网口都行；**只在板子没有根时接受** | `OK` / `Refused` / `Bad key`。只用于第一次认领，IDE 上传时由 IAPTool 自动发 |
| `setowner <gen> <新公钥hex> <签名hex>` | 当前主人的签名 | `OK` / `Refused` / `Bad args` / `Bad length` / `Bad hex` |
| `setownerwipe <gen> <新公钥hex> <签名hex>` | 同上 | 成功时板子复位、**不回话**；回 `Refused` 说明什么都没擦 |
| `revoke <叶公钥前 16 字节hex> <签名hex>` | 当前主人的签名 | `OK` / `OK already revoked` / `Refused` / `Bad …` |
| `flash <size> <crc32hex> <镜像签名hex> <证书hex> <nonce签名hex>` | 叶证书 + 挑战应答 | 见下一节 |
| `flashboot …` | 同 `flash` 的字段；镜像签名用 **owner 根**验，**没有根时拒绝** | 见 [FLASHBOOT.md](FLASHBOOT.md) |
| 其他 | — | `Unknown command` |

签名覆盖哪些字节、证书格式：见 [M2 归属与信任](../M2-ownership.md) 和 [CHALLENGE-AUTH.md](CHALLENGE-AUTH.md)。

## 一次 `flash` 的往返

1. 发 `authchallenge`，拿到 nonce
2. 发 `flash …`。nonce 签名覆盖 `sha256(nonce ‖ "flash <size> <crc32hex> <镜像签名hex>")`。
   通过回 `OK`，进入接收；不通过回 `ERR`，**不擦任何东西**
3. 发镜像字节，每收一块回 `OK`，先落进 SDRAM
4. 收齐之后校验，回答是下面之一：

| 回答 | 意思 |
|---|---|
| **（不回话，板子复位后重新上线）** | 成功。复位会把 MAC 一起带走，所以成功在线上是沉默的，只能靠「板子重新上线」确认 |
| `Checksum Failed` | CRC 不对；带后缀 `- SDRAM staging buffer failed its self-test` 时是暂存区坏了 |
| `No Signature` | 没带有效签名 |
| `Signature Failed` | 签名不对、叶被撤销，或开机时的密码学自检失败 |
| `Flash Failed` | 镜像是好的，写 flash 失败，重传即可 |
| `Failed` | 发送的字节超过暂存区 |

## UDP

| 发 | 谁回 | 回答 |
|---|---|---|
| `DISCOVER` / `openplc_discover` / `openplc_server_where_r_y` / `ping` | bootloader 和 app | 身份串。app 的第五段是 sketch 的版本号，bootloader 是 `-`。整台设备有发现限流 |
| `openplc_server_reboot_challenge` | app | nonce；RNG 失败时**不回** |
| `openplc_server_reboot <证书hex> <nonce签名hex>` | app | 不回。通过就复位进 bootloader。签名覆盖 `sha256(nonce ‖ "openplc_server_reboot")`；有冷却时间，窗口内重复的请求被忽略 |

app 不认 TCP 上的任何命令；要烧写，先用上面这条把它送进 bootloader。
