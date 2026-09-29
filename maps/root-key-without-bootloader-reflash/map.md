# 用户换自己的根，不用重烧 bootloader

## 怎么看进度（不用问任何人）

```
python tools/list_wayfinder_map_frontier.py --all
```

## Destination

用户手上没有 ST-Link，生成自己的根之后，由 IAPTool 把它写进板子、不改也不重烧 bootloader；逐条定下这条路和「把根编进 bootloader」相比的差别补不补、怎么补。

## Notes

- **范围只有 bootloader 和 IAPTool**（用户 2026-09-30 定）：工装不在这张图里，工装那边只做多语言
- **这张图只做可行性和决定**，不带执行
- 现状：bootloader 已经优先用 owner 区里的根，owner 区为空才用编进去的那把；`takeown` 写入、`setowner` 更换都不重烧。见 [M2 归属与信任](../../docs/modules/M2-ownership.md)
- 把用户引向「重编 bootloader」的是 `rotate_keys.sh`，见 `$BOOT/IAPServer/keys/README.md`
- 开票 / 关票 / 算前沿照 [图与票的约定](../MAP-AND-TICKET-CONVENTION.md)

## 全集

```
grep -rln "fw_public_key\|fw_pubkey" open_plc_cube_ide/IAPServer IAPTranfer_Tool --include=*.c --include=*.h --include=*.go --include=*.sh --include=*.inc
```

每一处读或写根公钥的地方，关最后一张票前都要说得出它在新做法下变不变。

## Decisions so far

## Not yet specified

- **给用户的文档怎么改**：`keys/README.md` 现在写的是「自己的根要重编 bootloader」，要等前面几张票定了才知道改成什么

## Out of scope

- **工装、产线预置**：用户 2026-09-30 定，这张图不碰工装
