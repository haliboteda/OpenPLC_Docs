# IDE-02 结论：IDE 上传用哪把密钥

票：[IDE-02 IDE 上传时用哪把密钥，已认领的板子要用户准备什么](issues/IDE-02-which-key-does-an-ide-upload-use.md)
调查日期 2026-09-24，只读代码和本机已装的板卡包，没有碰真板子。

`<TOOLDIR>` 下文指 IDE 实际运行的那份 IAPTool 所在目录：
`%LOCALAPPDATA%\Arduino15\packages\OpenPLC_Alpha\tools\STM32Tools\<版本>\win\`。

## 1 · IDE 传给 IAPTool 什么

> ✅ **结论**：IDE 只传位置参数（模式、bin、端口/IP、可选 `--force`），**不传 `--key` / `--cert`**，所以密钥全靠约定位置找。

| 菜单 | 命令行 | 出处 |
|---|---|---|
| USB (CDC) | `IAPTool.exe cdc <bin> <COM口> [--force]` | [platform.txt:239](../../../open_plc_arduino/platform.txt) |
| 以太网 | `IAPTool.exe ether <bin> <IP> [--force]` | [platform.txt:249](../../../open_plc_arduino/platform.txt) |

## 2 · IAPTool 找密钥和证书的顺序

| 顺序 | 私钥来源 | 出处 |
|---|---|---|
| 1 | `--key=<path>`（IDE 不传，这一步 IDE 永远跳过） | [app.go:302-304](../../../IAPTranfer_Tool/app.go) |
| 2 | `<TOOLDIR>\local_config.json` 里的 `"signing_key"` | [app.go:112-114](../../../IAPTranfer_Tool/app.go)、[common.go:212-218](../../../IAPTranfer_Tool/common.go) |
| 3 | `<TOOLDIR>\keys\fw_signing_key.pem`（存在才用） | [sign.go:28-29](../../../IAPTranfer_Tool/sign.go)、[sign.go:45-58](../../../IAPTranfer_Tool/sign.go) |
| — | 三处都没有 → 报错退出，提示第 3 条路径 | [auth.go:39-44](../../../IAPTranfer_Tool/auth.go) |

| 顺序 | 证书来源 | 出处 |
|---|---|---|
| 1 | `--cert=<path>`（IDE 不传） | [sign.go:73-76](../../../IAPTranfer_Tool/sign.go) |
| 2 | `<私钥路径>.cert`，即默认情况下 `<TOOLDIR>\keys\fw_signing_key.pem.cert` | [sign.go:79-83](../../../IAPTranfer_Tool/sign.go) |
| 3 | 都没有 → 用私钥**给自己签一张证书**（自签，私钥即根） | [auth.go:51-57](../../../IAPTranfer_Tool/auth.go) |

- `local_config.json` 和 `keys\` 都按 **exe 所在目录**找，不是 sketch 目录、不是当前目录（[common.go:204-218](../../../IAPTranfer_Tool/common.go)）。
- ⚠️ 但 `"signing_key"` 的**值**原样交给 `os.ReadFile`，相对路径按进程当前目录解析，不按 exe 目录（[sign.go:46-47](../../../IAPTranfer_Tool/sign.go)、[iapcert LoadKey](../../../IAPTranfer_Tool/iapcert/)）—— 要用这条就写绝对路径。IDE 启动 IAPTool 时的当前目录**没验证**。
- 证书的叶公钥和本地私钥对不上，上传前就停（[auth.go:75-83](../../../IAPTranfer_Tool/auth.go)）；证书不是板子当前根签的，在 bootloader 里 `getpubkey` 后停（[auth.go:122-157](../../../IAPTranfer_Tool/auth.go)）。
- 一份身份在一次上传里只解析一次，重启和烧录共用（[IAP_Ether.go:98-107](../../../IAPTranfer_Tool/IAP_Ether.go)）。

## 3 · 两种板子，用户要准备什么

| 板子状态 | 板子信任的根 | 用户要放的文件 | 放在哪 |
|---|---|---|---|
| **未认领** | 编译进 bootloader 的公开根（私钥在仓里：`open_plc_cube_ide/IAPServer/keys/fw_signing_key.TEST_ONLY.pem`） | 公开根私钥，改名 | `<TOOLDIR>\keys\fw_signing_key.pem`，不要 `.cert` |
| **已认领，上传者自己持有 owner 根** | 客户的 owner 根 | owner 私钥，改名 | `<TOOLDIR>\keys\fw_signing_key.pem`，不要 `.cert` |
| **已认领，上传者是同事（叶子）** | 客户的 owner 根 | 自己的叶私钥 + 管理员用 `IAPTool cert <叶公钥> --key=owner.pem` 签的证书 | `<TOOLDIR>\keys\fw_signing_key.pem` 和 `<TOOLDIR>\keys\fw_signing_key.pem.cert` |

替代做法：把 `"signing_key"` 设成私钥的**绝对路径**，证书放在那把私钥旁边（`<那个路径>.cert`）。
客户文档 [RELEASE-NOTES.md:273-286](../../../open_plc_cube_ide/RELEASE-NOTES.md) 写了 `keys/fw_signing_key.pem.cert`，**但没说 `keys/` 相对哪个目录**，也没说未认领板要自己把公开根私钥拷进去（见第 5 节 B2）。

本机现状：`STM32Tools\0.1.2\win\keys\fw_signing_key.pem` 与 `fw_signing_key.TEST_ONLY.pem` 字节相同（md5 一致），即本机 IDE 签的是公开根；这份 `keys\` 和 IAPTool.exe 都是手工放进去的（日期 09-17 / 09-22），不是装包装出来的。

## 4 · 板子正在跑 app 时的重启

| 通道 | 怎么进 bootloader | 要不要证书 | 出处 |
|---|---|---|---|
| USB (CDC) | 以 1200 波特开一下串口 | **不要**，IAPTool 侧不签任何东西 | [IAP_CDC.go:57-69](../../../IAPTranfer_Tool/IAP_CDC.go)、[IAP_CDC.go:118-126](../../../IAPTranfer_Tool/IAP_CDC.go) |
| 以太网 | UDP `openplc_server_reboot_challenge` 取 nonce → 发 `openplc_server_reboot <cert> <nonce签名>`，最多 3 轮 | **要**，用的就是第 2 节解析出的同一把私钥和同一张证书 | [IAP_Ether.go:118-150](../../../IAPTranfer_Tool/IAP_Ether.go)、[IAP_Ether.go:363-373](../../../IAPTranfer_Tool/IAP_Ether.go) |

> ✅ **结论**：app 验这张证书用的根，就是 bootloader 那块 owner 记录区里当前生效的根；记录区空时退回编译进 app 的 `fw_public_key`。所以已认领板上叶子 + 证书能重启，未认领板上公开根能重启，与 bootloader 的判断一致。

出处：[iap_auth.c:56-85](../../../open_plc_arduino/libraries/OpenPLC_IAP/src/iap_auth.c)（取根 + 查吊销 + 验签），[owner_root_ro.h:36-39](../../../open_plc_arduino/libraries/OpenPLC_IAP/src/owner_root_ro.h)、[owner_root_ro.c:215](../../../open_plc_arduino/libraries/OpenPLC_IAP/src/owner_root_ro.c)（空时退回编译进去的公钥）。
板卡包里的 `keys/fw_pubkey.inc` 与 bootloader 的那份字节相同（md5 一致）。

## 5 · 今天这条路上跑不通 / 不好用的地方

| 编号 | 是什么 | 在哪 | 影响 | 解决方案 |
|---|---|---|---|---|
| **B1** | **Board Manager 装到的 IAPTool 不会签名。** 索引里 0.1.3-pre 依赖 STM32Tools 0.1.2；那个 tar 包（本机 staging 里那份，SHA-256 与索引一致）里的 IAPTool.exe 是 2026-03-25 构建的，二进制里没有 `fw_signing_key`、`getpubkey`、`authchallenge`、`reboot_challenge` 这些串，也没有 `keys\` 目录 | [package_openplc_alp_index.json:35](../../../package_index_json/package_openplc_alp_index.json)、[:283-290](../../../package_index_json/package_openplc_alp_index.json) | 从 Board Manager 装的用户，对要求签名的 bootloader **上传必失败**（以太网连重启都过不去）。本机能用只是因为 exe 被手工换过 | 发一版新的 STM32Tools（含新 IAPTool），索引改依赖 —— 归 [IDE-01 发布版怎么到 Board Manager](issues/IDE-01-how-does-a-release-reach-board-manager.md) |
| **B2** | **没有任何东西把私钥放进 `<TOOLDIR>\keys\`**，客户文档也没说那个目录在哪 | [RELEASE-NOTES.md:273-286](../../../open_plc_cube_ide/RELEASE-NOTES.md) | 即使 B1 修了，未认领板的用户也要自己找到公开根私钥、拷到一个藏在 `AppData` 里的版本目录下，否则报 "no signing key found" | 二选一待定：随 STM32Tools 打包公开根私钥（它本来就是公开的）；或在客户文档写明 `<TOOLDIR>` 的完整路径和拷贝步骤 |
| **B3** | **以太网重启被拒时报错不提密钥。** app 拒绝时只往串口打印，UDP 不回任何东西；IAPTool 三轮后报 "No bootloader with UID=… found"，密钥是否匹配的检查要进了 bootloader 才跑 | [udp_server.c:222-224](../../../open_plc_arduino/libraries/OpenPLC_IAP/src/udp_server.c)、[IAP_Ether.go:145-146](../../../IAPTranfer_Tool/IAP_Ether.go) | 已认领板上用错钥匙（例如还是公开根）的用户，看到的是"板子没回来"，不是"钥匙不对" | 在重启失败的报错里补一句"也可能是密钥/证书不被这块板信任"；或重启前先在 app 侧查 `getpubkey`（app 目前没有这条命令，**没核实**是否值得加） |
| **B4** | **`keys\` 在带版本号的工具目录里。** STM32Tools 升版本后 IDE 用新目录，旧目录里的私钥和证书不会跟过去 | [platform.txt:234](../../../open_plc_arduino/platform.txt)（`{runtime.tools.STM32Tools.path}`） | B1 一修（必然升 STM32Tools 版本），所有已放好密钥的用户升级后上传失败，要重新拷一次 | 同 B2 一起定；`"signing_key"` 写绝对路径可以绕开，但 `local_config.json` 本身也在版本目录里 |
| **B5** | `"signing_key"` 相对路径按当前目录解析，与 README 说的"相对 exe"不一致 | [sign.go:46-47](../../../IAPTranfer_Tool/sign.go)、[README.md:52-53](../../../IAPTranfer_Tool/README.md) | 目前没有已知用户写相对路径，**当前影响为零**；README 那句说的是文件本身的查找位置，读起来容易误会 | 文档里写明"写绝对路径"即可 |

## 6 · 没有验证的

- IDE 启动 IAPTool 时的当前工作目录（只影响 B5）。
- CDC 那条 1200 波特重启在 app 固件侧确实不校验任何东西 —— 只看了 IAPTool 侧，没读 core 的 USB CDC 代码。
- Arduino IDE 卸载/升级板卡包时会不会删掉旧版本工具目录（影响 B4 里私钥会不会被一起删）。
- 现在发给客户的 bootloader 版本是否已经要求会话认证（决定 B1 是"今天就坏"还是"下一版 bootloader 发出去才坏"）。
- 以上全部没有在真板子上跑。
