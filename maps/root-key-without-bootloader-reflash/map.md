# 用户换自己的根，不用重烧 bootloader

## 怎么看进度（不用问任何人）

```
python tools/list_wayfinder_map_frontier.py --all
```

## Destination

**出厂不写任何根；用户第一次经 USB 或网口上传时，IAPTool 自动生成密钥并认领板子**（[决策 72](../../docs/tables/DECISIONS.md)）。之后连续换根无论多少次，都不改、也不重写 bootloader。逐条定下根区放哪、写满怎么回收，以及 bootloader、IAPTool、core 各自怎么改。

## Notes

- **范围只有 bootloader 和 IAPTool**（用户 2026-09-30 定）：工装不在这张图里，工装那边只做多语言
- **这张图只做可行性和决定**，不带执行
- 现状：bootloader 已经优先用 owner 区里的根，owner 区为空才用编进去的那把；`takeown` 写入、`setowner` 更换都不重烧。见 [M2 归属与信任](../../docs/modules/M2-ownership.md)
- 把用户引向「重编 bootloader」的是 `rotate_keys.sh`；它和 bootloader 的 `keys/` 目录 2026-09-30 已随决策 72 删除
- 开票 / 关票 / 算前沿照 [图与票的约定](../MAP-AND-TICKET-CONVENTION.md)

## 全集

```
grep -rln "fw_public_key\|fw_pubkey" open_plc_cube_ide/IAPServer IAPTranfer_Tool --include=*.c --include=*.h --include=*.go --include=*.sh --include=*.inc
```

每一处读或写根公钥的地方，关最后一张票前都要说得出它在新做法下变不变。

## Decisions so far

- [core 里那份内置根怎么跟着改](issues/ROOT-06-the-cores-copy-of-the-built-in-root.md)：删掉；app 读扇区 15 的根区，链为空时拒绝
- [恢复出厂之后板子信任哪把根](issues/ROOT-03-which-root-does-a-factory-reset-return-to.md)：回到没有根，下次上传自动重新认领
- [根区放在哪、写满怎么回收](issues/ROOT-05-where-the-built-in-root-lives-and-how-it-is-updated.md)：扇区 15 `0x081E2000` 起 8 KiB，回收时暂存备份 SRAM（方案 5）
- **出厂不写任何根，第一次上传自动认领，USB 或网口都行，不按 BOOT0；恢复出厂仍长按 BOOT0 10 秒**（用户 2026-09-30 定，[决策 72](../../docs/tables/DECISIONS.md)）。取代同日早些时候的「内置根搬出代码、安全机制不变」
- **连续换根不限次数，任何一次都不改、不重写 bootloader**（用户 2026-09-30 定）
- **每个存放方案都要配 flash 分布图**（用户 2026-09-30 定）
- [第一次把用户的根写进板子，要不要按住 BOOT0](issues/ROOT-02-must-the-first-write-of-the-users-root-need-boot0.md)：不按，USB 或网口都能认领
- **私钥放本机固定的默认位置，生成和读取时提示路径；换电脑自己拷根私钥；多人合用发叶证书；工装走 ST-Link 不涉及证书**（用户 2026-09-30 定，写进决策 72）
- [H743 的 OTP 区能不能存根公钥](issues/ROOT-01-can-the-h743-otp-area-hold-the-root.md)：没有 OTP，根只能放 owner 区这类普通 flash

## Not yet specified

- **私钥默认位置的具体路径**：用户定了「板卡包目录之外的一个固定位置，生成和读取时都提示路径」，具体路径写进 M2 时定

- **给用户的文档怎么改**：`keys/README.md` 现在写的是「自己的根要重编 bootloader」，要等前面几张票定了才知道改成什么

## Out of scope

- **工装、产线预置**：用户 2026-09-30 定，这张图不碰工装
