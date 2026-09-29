# ROOT-01 调研结论：H743 有没有能存根公钥的 OTP / 保护存储

票：[ROOT-01 H743 的 OTP 区能不能存根公钥](issues/ROOT-01-can-the-h743-otp-area-hold-the-root.md)。
芯片型号 **STM32H743IIK6**：`$HW/Hardware_overview.txt` 与 `$BOOT/open_plc_cube_ide.ioc`（`Mcu.CPN=STM32H743IIK6`）一致。

出处只用 ST 原件：**RM0433 Rev 8**（2023-01，适用 STM32H742/743/753/750）、**DS12110 Rev 11**（2026-01，STM32H742xI/G、H743xI/G）。
RM0433 全文检索 "OTP" / "one-time" 在 flash 章节零命中（唯一的 "one-time programmable" 是 USB OTG 的一个寄存器位，无关）。

| 候选 | 有没有 | 容量 | 写入方式（bootloader 运行时能否自写，不用 ST-Link） | 可否更换 / 作废 | RDP 下行为 | 出处 |
|---|---|---|---|---|---|---|
| **用户 OTP 区** | **没有** | — | — | — | — | RM0433 §4.3.4 表 15（H743xI 的 flash 只有 user main / system memory / option bytes 三类）；DS12110 §3.3.1 同 |
| Option bytes | 有，但**没有可放用户数据的字段** | 表 21 所有字段都是配置位（RDP、BOR、WRP、PCROP、secure 区边界、BOOT_ADD…） | 能：解锁 `FLASH_OPTCR` 后软件改 | 可反复改（RDP 2 下除 SWAP 外全冻结） | — | RM0433 §4.4.1、§4.4.4 表 21、§4.5.3 |
| Secure access mode（secure-only 区 / RSS） | **H743 没有**，只有 H750xB、H753xI 有 | — | — | — | — | RM0433 §5.1、§5.3 |
| 扇区写保护 WRP | 有 | 粒度 **128 KiB 整扇区** | 能：软件改 `FLASH_WPSN_PRG1R` 的 WRPSn 位 | **RDP 0/1 下软件可随时清除**；RDP 2 下永久冻结 | L2 下不可改 | RM0433 §4.5.2、§4.9.16 |
| PCROP（只执行区） | 有 | 256 B 粒度 | 能：软件改 `FLASH_PRAR_PRG1` | 只能在 RDP 1→0 回退或带保护移除的 bank erase 时撤销 | — | RM0433 §4.5.4 |
| 备份 SRAM / RTC 备份寄存器 | 有 | 4 KiB | 能，运行时直接写 | 随时可改 | RDP 1→0 回退时被擦 | DS12110 §3.3.2、§3.29；RM0433 §4.5.3 |
| RDP Level 2 | 有 | 不是存储 | 能：软件写 RDP=0xCC | **不可逆**（永久关调试、option bytes 冻结） | — | RM0433 §4.5.3 表 23、表 25 |

各行不适用的原因（各一句）：

- **Option bytes**：没有空闲的数据字段，64 字节公钥放不进去。
- **PCROP**：只执行区里的数据连 CPU 自己都不能读，验签需要读公钥，所以不能用。
- **WRP**：粒度是 128 KiB 整扇区。锁 sector 0 就连同 bootloader 和 owner 区一起锁死，之后 `takeown`、`setowner`、factory reset 都写不进去；而且软件能自己解锁，不是一次性的。
- **备份 SRAM**：易失（靠 VBAT 保持），随时可改，不能当「一次写入」的根。本板 VBAT 接法**未核实**。
- **RDP 2**：能冻结 option bytes，但冻结不了 user flash 本身，还会永久封死调试口，与「一次写入的根」无关。

## 和现有 owner 区比

现有做法是 [M2 归属与信任](../../docs/modules/M2-ownership.md)、`$BOOT/IAPServer/owner_slot.h`：`0x0801E000` 起 8 KiB，放在 sector 0 尾部，只追加。

| | owner 区（现状） | H743 上可得的「一次性」存储 |
|---|---|---|
| bootloader 运行时自写、不用 ST-Link | 能 | OTP 不存在；其余候选要么放不下数据，要么不是一次性的 |
| 写入后能否防篡改 | 不能，能跑起来的 app 理论上可以写 sector 0 | 同样做不到：WRP 软件可解锁，锁上还会把 owner 区一起锁死 |
| 让 factory reset 回落到用户根 | 可在 owner 区里定义（在 [ROOT-03 恢复出厂回到哪把根](issues/ROOT-03-which-root-does-a-factory-reset-return-to.md) 定） | 没有独立的硬件位置可用 |

> ✅ **结论**：STM32H743 **没有用户 OTP 区**（RM0433 §4.3.4 表 15）。芯片上也没有别的一次性存储既能放下 64 字节公钥、又能由 bootloader 在运行时自己写入。secure-only 区只在 H753/H750 上有，WRP 软件可解锁，PCROP 读不出来。所以「用户根」和「恢复出厂时回落的根」只能继续放在 owner 区这类普通 flash 里。OTP 这条路对本板不成立。

⚠️ **抄件与源头对不上**：[M2 归属与信任](../../docs/modules/M2-ownership.md) 第 728 行说 WRP「设置之后清除需要 ST-Link/J-Link 物理访问」。RM0433 §4.5.2 写的是 RDP 0/1 下 WRP 位可以由软件无限制修改，只有 RDP 2 下才冻结。
