# 没有板子时用 Renode 验证固件

## 怎么看进度（不用问任何人）

```
python tools/list_wayfinder_map_frontier.py --all
```

## Destination

1. **Renode 里走和真板子一样的启动链**：bootloader 先运行，校验通过后跳进 app
2. **`OpenPLC_Ports` 的 13 个例程在 Renode 里自动判过不过**；判不了的逐个说明原因，并给出替代方案

## Notes

- **这张图带执行**：票定完就写代码
- **只做必要的代码和测试**；先文档再代码
- Renode 1.17.0 Windows 免安装版，装在 `D:\Soft\renode`（2026-09-27）
- 开票 / 关票 / 算前沿照 [图与票的约定](../MAP-AND-TICKET-CONVENTION.md)

### 开图时已定（2026-09-27 用户定）

| 事 | 定案 |
|---|---|
| 启动方式 | 和真板子一样：先进 bootloader，再跳 app。不在脚本里代替 bootloader 做事 |
| 范围 | 13 个例程都要；做不到的说出是哪个、为什么、有没有替代方案 |

### 开图前已知（2026-09-27 实测）

- `DO_Outputs` 直接从 app 起跑（跳过 bootloader）时，在 `HAL_RTC_MspInit` 等 LSE 超时后进死循环：LSE 平时由 bootloader 打开。启动前替它置 LSEON 后，DO1–DO8 按例程顺序开关
- 所有例程的 `Serial` 走 USB CDC，Renode 的 USB 模型下看不到文字；平台里没有 DAC

## 全集

```
ls open_plc_arduino/libraries/OpenPLC_Ports/examples
```

## Decisions so far

- [Renode 能不能走 bootloader → app 的启动链](issues/REN-01-can-renode-boot-through-the-bootloader.md)：能，flash 填 `0xFF` 后放 bootloader、签好名的 app 和一条 metadata 记录，只用 `LoadBinary` 加载

## Not yet specified

- **metadata 记录由脚本拼出，和 bootloader 的格式是两份**：要么让 bootloader 自己写（需要 Renode 里的以太网或 USB CDC 能用），要么加一道检查盯住两边一致

## Out of scope
