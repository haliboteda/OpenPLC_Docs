# identity 怎么同时报卡包版本和 app 版本

Type: grilling
Opened: 2026-09-21
Status: resolved
Blocked by: VER-01

## Question

用户 2026-09-21 定：**卡包版本和用户 app 版本是两个东西**。那板子怎么把两个都报出来？

今天的 identity 是**四段**，`_` 分隔（[IAP_server.c:162-172](../../../../open_plc_cube_ide/IAPServer/IAP_server.c) 和
[udp_server.c:174](../../../../open_plc_arduino/libraries/OpenPLC_IAP/src/udp_server.c) 两边各生成一份）：

```
OPEN-PLC _ <uid> _ <role> _ <version>
                     │         └─ 现在是 OPENPLC_FW_VERSION，即卡包版本 build.fw_version
                     └─ CUSAPP / BOOTLD / BOOTLD-INVALID
```

⚠️ **上位机那边**：`parseBoardInfoFromReply`（[IAP_Ether.go:177-198](../../../../IAPTranfer_Tool/IAP_Ether.go)）
用 `strings.Join(parts[3:], "_")` **把第 4 段之后全部合并成一个 Version 字符串**。
所以直接加第 5 段，工具会读成 `0.1.3_1.0.0` 一整串。

两条路：

| | 怎么做 | 代价 |
|---|---|---|
| **P1** | **加第 5 段**，第 4 段仍是卡包版本 | 协议变更；`parseBoardInfoFromReply` 必须同步改，否则读出来是拼接串 |
| **P2** | **第 4 段换成 app 版本**，卡包版本不再进 identity | 不加字段；但卡包版本从此报不出来，`BOOTLD` 状态下这一段是什么要另外定 |

**还要顺带定一件事**：`OPENPLC_FW_VERSION`（卡包版本）**还留不留**。
用户 2026-09-21 说过「core 现有的版本宏删掉」—— [app 版本号怎么从 sketch 传到 core](VER-01-how-does-the-sketch-version-reach-the-core.md)
把它理解成「删掉 `"0.0.0"` 那个 fallback」，卡包版本本身经 `boards.txt` 的 `-D` 仍然存在。**这个理解要确认。**

## 怎么算答完

1. 选定 P1 / P2，写出**新的 identity 字符串格式**，逐段说明
2. 写明 `OPENPLC_FW_VERSION` 留不留；留的话它出现在哪、谁还在读它
3. 写明 `parseBoardInfoFromReply` 要改成什么，以及**旧固件配新工具 / 新固件配旧工具**各会怎样
4. 写明 bootloader 那一份 identity（`IAP_server.c`）要不要跟着改 —— 它报不出 app 版本，那一段填什么

## Answer

2026-09-21 定

**选 P1：加第 5 段。卡包版本留在第 4 段不动，app 版本是新的第 5 段。**

```
OPEN-PLC _ <uid> _ <role> _ <卡包版本> _ <app 版本>
   1        2        3         4            5  ← 新增
```

⚠️ **任何字段都不能含 `_`** —— `iap_identity_string()` 的注释明写这条，版本号是点分数字，满足。

### 1 · `OPENPLC_FW_VERSION`（卡包版本）保留

用户 2026-09-21 说的「core 现有的版本宏删掉」指的是
`cores/arduino/stm32/IAP_config.h` 里那个 `"0.0.0"` **fallback**，
不是卡包版本本身。它仍由 `boards.txt` 的 `build.fw_version` 经 `-D` 注入，仍占第 4 段。

### 2 · bootloader 那一份第 5 段填 `-`

identity **两边各生成一份**，都要改成五段：

| 谁 | 在哪 | 第 5 段填什么 |
|---|---|---|
| bootloader | `IAP_server.c` 的 `iap_identity_string()` | **`-`** —— 它不知道 app 是哪一版 |
| app | `libraries/OpenPLC_IAP/src/udp_server.c` | `openplc_app_version` 的内容 |

填 `-` 不填 `0.0.0`：**`0.0.0` 看起来像个真版本号**，会被误当成「装了一个 0.0.0 的 app」。

⚠️ **这是一处新的跨仓镜像** —— 两份 identity 的格式必须一致，改一份不改另一份不会编译报错。

### 3 · 两个方向的兼容都要处理

| | 会发生什么 | 怎么办 |
|---|---|---|
| **新固件 + 旧工具** | 旧工具 `strings.Join(parts[3:], "_")` 把后两段合成 `"0.1.3_1.0.0"` | 旧工具本来就不比版本，**只是显示难看**，不会误判。可接受 |
| **旧固件 + 新工具** | 只收到 4 段 | 新工具必须**按段数降级**：`len(parts) == 4` ⇒ 这块板没有 app 版本 ⇒ **放行，不比对** |

`parseBoardInfoFromReply`（`IAP_Ether.go:177-198`）要改掉 `strings.Join(parts[3:], "_")`，
改成分别取 `parts[3]`（卡包版本）和 `parts[4]`（app 版本，缺就是空）。

## 引出了什么新的未知

一条，已记进 `work/TODO.md`：**`P2`（跨仓镜像没分叉）现在不守 identity 格式**。
两份 identity 的段数和顺序从此必须一致，该纳进那道检查。
