# `flashboot` 的线上协议长什么样

Type: grilling
Opened: 2026-09-22
Status: resolved
Blocked by: -

## Question

`flashboot`（bootloader 原地升级）的**形状已经定死**，只剩线上这一段没定：

**已经定了的**（不要重开）：
- 走路线 2 —— 镜像读进 SDRAM、在 RAM 里擦扇区 0、写回新 bootloader + 旧 owner 记录。**不允许断电**
- 用 **owner 根**验签，不用内置根（内置根私钥是公开的）
- 未认领的板子上做 `flashboot` 要**物理在场**（`s_boot0_held`），已认领的走签名
- 擦写例程放 `RAM_D1`，全程关中断，不调 HAL（`A12`/`A13`，`.RamFunc` 段已经在 `.data` 里，不用改链接脚本）

**没定的**：帧格式、分块方式、和现有 `flash` 命令共用多少。

### 现有 `flash` 是这样的（`$BOOT/IAPServer/IAP_server.c:356`）

```
flash <size> <crc32hex> <imgsig_hex> <cert_hex> <noncesig_hex>
```

- `imgsig` —— 叶密钥对整个镜像的 ECDSA r||s（128 hex）
- `cert` —— 128 字节证书，根签的，里面是那把叶公钥（256 hex）
- `noncesig` —— 同一把叶密钥对 `sha256(nonce || "flash <size> <crc32hex> <imgsig_hex>")` 的签名，
  nonce 来自上一条 `authchallenge`
- 板子回 `OK` 之后，镜像字节直接流进 SDRAM（`IAP_STAGE_BASE`），收齐才验、验过才擦 app 区

### 候选

| | 做法 | 代价 | 风险 |
|---|---|---|---|
| **A** | 完全照搬：`flashboot <size> <crc32> <imgsig> <cert> <noncesig>`，同一套接收与暂存，只改三处（尺寸上限 120 KiB、写目标是扇区 0、写之前先把 owner 记录搬进 SDRAM） | 最小 —— bootloader 侧多一个分支，`IAPTool` 侧几乎是 `RunEther` 的副本 | **叶证书就能换掉 bootloader。** 一把发给「只准烧 app」的叶，凭同一张证书也能刷 bootloader |
| **B** | 帧格式同 A，但 **`imgsig` 必须由 owner 根直签**（`cert`/`noncesig` 仍用来做会话认证，防重放不变） | 比 A 多一个验签分支；`IAPTool flashboot` 要 `--key=owner.pem`（根私钥），不能用叶 | 每次升 bootloader 都要动根私钥。**但这正是想要的** —— 换 bootloader 和换所有权是同一个量级的动作 |
| **C** | 另设一套分块协议（每块带序号、逐块 ACK） | 传输层两边重写 | 今天没有需求要它；`flash` 那条传输路径已经在真板子上跑过很多轮，另起一套等于把验过的东西重验一遍 |

## 怎么算答完

1. 定下命令字符串的确切形状，写进 `$PROD/docs/modules/M1-firmware-upgrade.md` 的 `flashboot` 通道一节
2. 说清**谁能授权** —— 根还是叶，以及未认领板子上的 BOOT0 分支
3. `CHANGE-LIST.md` 的 `A9`/`A10`/`B2` 三行从 ⏳ 转成可做


## Answer

2026-09-22 用户定：**B**。

帧格式照搬 `flash`，传输与 SDRAM 暂存完全复用：

```
flashboot <size> <crc32hex> <imgsig_hex> <cert_hex> <noncesig_hex>
```

和 `flash` 的区别只有四处：

1. **`imgsig` 用 owner 根公钥验**，不用 `cert` 里那把叶。叶证书换不掉 bootloader
2. `cert` / `noncesig` 仍然只管**会话认证和防重放**，走和 `flash` 同一条路
3. 尺寸上限 120 KiB（bootloader 区），不是 `IAP_APP_MAX_SIZE`
4. 落盘目标是扇区 0，写之前先把 owner 记录搬进 SDRAM，擦完**先写 owner 再写 bootloader**

未认领的板子没有根可验，走物理在场（`s_boot0_held`），和 `takeown` 同一条规则。

**否掉 C**（另设分块协议）—— `flash` 那条传输已在真板子上跑过很多轮，另起一套等于把验过的东西重验一遍。

## 引出了什么新的未知

没有。剩下的都是实施：`CHANGE-LIST.md` 的 `A10`（bootloader 侧命令）、
`A11`（未认领时查 BOOT0）、`A12`（RAM 里擦写扇区 0）、`B2`（`IAPTool flashboot`）。
