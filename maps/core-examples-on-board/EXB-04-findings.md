# EXB-04 结论：上游例程哪些和本板有关

票：[EXB-04](issues/EXB-04-which-upstream-examples-relate-to-this-board.md)。2026-09-29 核实。

## 出处缩写

| 缩写 | 文件 |
|---|---|
| xlsx | `Hardware/STM32H743IIK6_GPIO_ASSIGNMENT_Schaeffer_Bridge_20260822.xlsx`，sheet `GPIO_ASSIGNMENT`，后跟行号 |
| JL | `Hardware/Production/JunctionLink/netlist.ipc` |
| BOM | `Hardware/Production/Bridge/1436_01_SCHAE-BR.xlsx` + `Hardware/Production/{UpperDeck,LowerDeck,JunctionLink}/bom.csv` |
| HF | [HARDWARE-FACTS.md](../../docs/hardware/HARDWARE-FACTS.md) |
| var | `open_plc_arduino/variants/STM32H7xx/H743/variant_PLC_H743.{h,cpp}`（抄件，只作交叉验证） |

**Arduino 数字脚号 N 就是 `PA_N`**（N = 0–15，`variant_PLC_H743.cpp:17-33`）。上游例程里写死的 `2`、`9`、`10`、`13` 等数字在本板上全落到 PA 口，下表按这个换算。

## 评判原则

| 建议 | 含义 |
|---|---|
| **测** | 现有台子（板子上电，接了 RS485 / CAN / KNX，AO 接 470 Ω）不加东西就能跑出可判的结果 |
| **留着不测** | 例程原样能对上本板引出的端子，但要台子上没有的外接器件；或者是库的基础设施 |
| **删** | 例程要的东西本板没有；或写死的引脚落在板内功能脚上，原样对不上任何端子 |

## 32 个例程

| # | 例程 | 需要什么 | 本板有没有（出处） | 建议 | 理由 |
|---|---|---|---|---|---|
| 1 | `CI/build/examples/BareMinimum` | 只做编译：include 7 个库，注释写明「can not be executed」 | 不相关：它是上游 CI 脚本 `CI/build/arduino-cli.py` 的输入，不在 IDE 例程菜单里，也不在 P5 范围内（`build.py:84-102` 只扫 `libraries/*/examples`） | 留着不测 | 属于上游 CI 工具，不是给用户的例程；要删就是连整个 `CI/build` 一起处理，另开一件事 |
| 2 | `CMSIS_DSP/arm_sin_cos_example_f32` | 纯计算，经 `Serial`（USB CDC）打印 `SUCCESS`/`FAILURE` | 有：USB FS 在 PA11/PA12（HF「USB FS 只接了 PA11 / PA12」） | **测** | 只要 USB 串口，打印结果能直接判 |
| 3 | `EEPROM/eeprom_clear` | 写满整个 EEPROM；`pinMode(13)` | ⛔ 每写一个字节就把扇区 15 整个擦一次（见下文「EEPROM」）；脚 13 = PA13 = SWDIO（xlsx 135） | 删 | 会擦掉校准值和 metadata，重启后 bootloader 停在 IAP 等重传；16384 次擦写还会压到扇区寿命上；另外会把 SWD 关掉 |
| 4 | `EEPROM/eeprom_crc` | 只读，打印 CRC | 读的是 `0x081FC000`–`0x081FFFFF`，也就是 metadata 区的尾巴（见下文） | 删 | 读本身无害，但读到的是 metadata，没有意义；整库跟 #3 一起处理 |
| 5 | `EEPROM/eeprom_get` | 只读 | 同 #4 | 删 | 同 #4 |
| 6 | `EEPROM/eeprom_iteration` | `EEPROM[i] += 1`，每一次都是写 | 同 #3 | 删 | 同 #3 |
| 7 | `EEPROM/eeprom_put` | 写 | 同 #3 | 删 | 同 #3 |
| 8 | `EEPROM/eeprom_read` | 只读 | 同 #4 | 删 | 同 #4 |
| 9 | `EEPROM/eeprom_update` | 写；`analogRead(0)` 当电位器 | 同 #3；A0 = PA0 = LM50 温度传感器 `TEMP_SCPROT`（HF「两路板载温度」），不是电位器 | 删 | 同 #3 |
| 10 | `EEPROM/eeprom_write` | 写；`analogRead(0)` | 同 #9 | 删 | 同 #3 |
| 11 | `IWatchdog/IWDG_Button` | IWDG；`USER_BTN`、`LED_BUILTIN` | IWDG 是片上外设，有。`USER_BTN` / `LED_BUILTIN` 在变体里都是 `PNUM_NOT_DEFINED`（var `.h:410-416`），所以「按键」永远读不到按下 → 永远不喂狗 | **测** | 原样跑的结果是**约 10 s 复位一次**，从 bootloader 启动日志或 USB 重新枚举就能判；这正好验证 IWDG 生效 |
| 12 | `Keyboard/KeyboardMessage` | USB HID | 无：板卡包 USB 菜单只有 CDC（`boards.txt:79-83`），`Keyboard.h:27-29` 直接 `#error`；P5 已排除 | 删 | 没有 HID 需求，编都编不过 |
| 13 | `Mouse/ButtonMouseControl` | USB HID + D2–D6 五个按键 | 无 HID（同 #12）；PA2–PA6 = ETH_MDIO / TEMP_HSSW / AOUT1 / AOUT2 / AIN2（xlsx 6、117、110、111、109） | 删 | 同 #12 |
| 14 | `RGB_LED_TLC59731/RGB_LED_TLC59731` | TLC59731 RGB LED 驱动芯片 | 无：四块板 BOM 里都没有 TLC59731；`LED_BUILTIN` 未定义，库头文件自己报 `#warning` | 删 | 这是 STM32WB5MM-DK 的板载器件（例程注释原话） |
| 15 | `SPI/BarometricPressureSensor` | SCP1000 传感器；SPI 总线；DRDY = 脚 6，CS = 脚 7 | SPI 总线有：SPI2 在扩展口 J4-3~6（JL:81-84，var `.h:419-439` 一致）。但脚 6 = PA6 = AIN2（xlsx 109），脚 7 = PA7 = `RMII_CRS_DV`（xlsx 7） | 删 | DRDY / CS 不在 J4 上；原样跑会把以太网的 `RMII_CRS_DV` 配成输出，网口断掉 |
| 16 | `SPI/DigitalPotControl` | AD5206 数字电位器；CS = 脚 10 | SPI2 有（同上）；脚 10 = PA10 = `KNX_RX`（xlsx 143），光耦 U13 开集输出在拉这根线（HF「KNX」） | 删 | CS 不在 J4 上；原样跑会把 MCU 推挽输出和光耦下拉顶在一起 |
| 17 | `Servo/Knob` | 舵机信号接脚 9；电位器接 A0 | 脚 9 = PA9 = `HSFET_6` = Digital Out 6（HF「USB FS…」表；`LowerDeck_overview.txt:36-40` 交叉验证：VNQ5160K-E 高边驱动）；A0 = LM50 温度 | 删 | 舵机脉冲会打到高边驱动的 DO6 上，那不是舵机信号电平；电位器位置是温度传感器 |
| 18 | `Servo/Sweep` | 舵机接脚 9 | 同 #17 | 删 | 同 #17 |
| 19 | `Servo/fs90r` | FS90R 连续旋转舵机接脚 9；A0 | 同 #17 | 删 | 同 #17 |
| 20 | `SoftwareSerial/SoftwareSerialExample` | RX = 脚 10，TX = 脚 11；`Serial` 当控制台 | 脚 10 = PA10 = `KNX_RX`；脚 11 = PA11 = USB D-（HF「USB FS 只接了 PA11 / PA12」） | 删 | TX 占 USB D- 会把 `Serial`（USB CDC）自己弄断；本板有 4 个硬件串口不需要软串口 |
| 21 | `SoftwareSerial/TwoPortReceive` | 两组软串口：(10,11)、(8,9) | 同 #20；脚 8/9 = PA8/PA9 = DO5/DO6（HF 同表） | 删 | 同 #20，外加 TX 会拨动 DO6 |
| 22 | `SrcWrapper/BareMinimum` | 空 sketch（已补 `OPENPLC_APP_VERSION`） | 不需要外设 | 留着不测 | `SrcWrapper` 是 core 基础设施不能删（`cores/arduino/Arduino.h:33`、`platform.txt:117`）；空 sketch 能上传这件事每个别的例程都已覆盖 |
| 23 | `SubGhz/ReadRegister` | SubGhz 射频 | 无：只有 STM32WL 有，`SubGhz.h:21-22` 直接 `#error`；P5 已排除 | 删 | 这颗芯片没有这个外设 |
| 24 | `Wire/SFRRanger_reader` | SRF08 超声测距模块，I2C 地址 0x70 | I2C 总线有：I2C2 在 J4-8 SDA / J4-9 SCL（JL:86-87；var `.h:442-447` PH5/PH4 一致）。器件四块板 BOM 里都没有，台子上 J4 也没接东西 | 留着不测 | 总线能对上端子，缺的只是外接模块 |
| 25 | `Wire/digital_potentiometer` | AD5171 数字电位器，地址 0x2C | 同 #24 | 留着不测 | 同 #24 |
| 26 | `Wire/i2c_scanner` | I2C 总线，任意从机 | 同 #24 | 留着不测 | 空总线只会报「没有设备」，判不出什么；J4 上接一个任意 I2C 模块后它是最省事的一个 |
| 27 | `Wire/master_reader` | 对端是跑 `slave_sender` 的另一块板 | 同 #24 | 留着不测 | 要第二块 I2C 板子 |
| 28 | `Wire/master_reader_writer` | 对端跑 `slave_sender_receiver` | 同 #24 | 留着不测 | 同 #27 |
| 29 | `Wire/master_writer` | 对端跑 `slave_receiver` | 同 #24 | 留着不测 | 同 #27 |
| 30 | `Wire/slave_receiver` | 对端跑 `master_writer` | 同 #24 | 留着不测 | 同 #27 |
| 31 | `Wire/slave_sender` | 对端跑 `master_reader` | 同 #24 | 留着不测 | 同 #27 |
| 32 | `Wire/slave_sender_receiver` | 对端跑 `master_reader_writer` | 同 #24 | 留着不测 | 同 #27 |

**合计**：测 2（#2、#11），留着不测 11（#1、#22、#24–#32），删 19。

**未核实**：I2C2 在板上有没有上拉电阻。UpperDeck、JunctionLink 网表里 I2C2 网上只有 EMI 滤波器（JL:`U5-1/8`、`U1-3/6`），没有电阻；Bridge 板只有 PDF/PNG 原理图没有网表，没逐脚查。外接 I2C 模块通常自带上拉，不影响上表建议。

## EEPROM：写一次就擦掉扇区 15

| | |
|---|---|
| 选哪个扇区 | H743 有两个 bank，`FLASH_BANK_NUMBER` 取 `FLASH_BANK_2`（`libraries/EEPROM/src/utility/stm32_eeprom.c:27-33`）；`FLASH_DATA_SECTOR` = `FLASH_SECTOR_TOTAL - 1` = 7（`:40-43`，`FLASH_SECTOR_TOTAL` = 8 见 CMSIS `stm32h743xx.h:10665`）→ **bank 2 sector 7 = `0x081E0000`，就是扇区 15** |
| 读写哪段 | `FLASH_END` = `0x081FFFFF`（CMSIS `stm32h743xx.h:2079`），`FLASH_PAGE_SIZE` 缺省 16 KiB（`stm32_eeprom.h:79-88`）→ 缓冲映射 `0x081FC000`–`0x081FFFFF`（`stm32_eeprom.c:84`） |
| 怎么写 | 每次 `EEPROM.write` / `put` / `update` / `[] +=` 都调 `eeprom_buffer_flush()`（`stm32_eeprom.c:121-133`），它**擦整个 sector 7**（`:248-255`）再写回 16 KiB |
| 那个扇区里是什么 | 前 8 KiB 校准值 + 后 120 KiB firmware metadata（[SECTOR-15.md](../../docs/modules/M1/SECTOR-15.md)「布局」；[BOOTLOADER-PROJECT-LAYOUT.md](../../docs/build/BOOTLOADER-PROJECT-LAYOUT.md):28、36） |
| 擦掉的后果 | metadata 没了 → 下次上电 bootloader 判「没有可跑的 app」，停在 `IAP_ALL` 等重传（[M1-firmware-upgrade.md](../../docs/modules/M1-firmware-upgrade.md):168、475）；校准值没了要回工装重写 |
| 有没有东西挡着 | 没有：变体和 `boards.txt` 都没覆盖 `FLASH_DATA_SECTOR` / `FLASH_BASE_ADDRESS`；flash 写保护没开（[M2-ownership.md](../../docs/modules/M2-ownership.md):723-724） |
| 和 app、bootloader 区重不重叠 | 不重叠：bootloader `0x08000000`–`0x0801FFFF`，app `0x08020000`–`0x081DFFFF`（BOOTLOADER-PROJECT-LAYOUT.md:34-35）。**问题只在扇区 15** |
| 能不能挪到别的扇区 | 现在没有空扇区：app 区一直到 `0x081E0000`，bank 2 sector 6（`0x081C0000`）已被 KNX 协议栈 NVM 占用（`libraries/OpenPLC_KNX/src/knx_nvm.cpp:13`） |

所以 EEPROM 库在本板上**没有安全的落点**。✅ **2026-09-30 用户定：整库删除**，见 [EXB-09](issues/EXB-09-knx-and-eeprom-must-not-erase-sector-15.md)。当时的可选做法：

| 做法 | 代价 | 风险 |
|---|---|---|
| 删整个 `EEPROM` 库 | 自有库和 core 都不用它；要同步改 `libraries/CMakeLists.txt:4` 和 `CI/build` 的 BareMinimum | 用户 `#include <EEPROM.h>` 直接找不到库 |
| 留库，在变体里让它 `#error` | 改一行变体 | 报错信息能说清原因，但上游同步时要保住这一行 |
| 挪扇区 | 要从 app 区切一个 128 KiB 扇区出来 | 改 flash 分区，影响 bootloader / 工装 / 链接脚本三边 |

## 删掉会影响什么

| 受影响的东西 | 影响 | 出处 |
|---|---|---|
| **P5**（编译板卡包里所有例程） | 例程是动态扫出来的，删掉就少编几个，不会报错。只有**一个例程都扫不到**时才失败。`EXCLUDED` 里 Keyboard / Mouse / SubGhz 三条删掉例程后变成死条目，应一起去掉。P5 扫的是**已安装的板卡包**（`CORE_LIVE`），所以要下次发版装上后才生效 | `$CORE_REPO/tests/examples_build/build.py:38-42、84-112` |
| P5 的说明文档 | 只描述范围（「别的芯片的外设、这块板没有的 USB 功能」），没有逐个列例程，删掉 EXCLUDED 后这句可以不改 | [HOW-TO-RUN-TESTS.md](../../docs/engineering/HOW-TO-RUN-TESTS.md):298-323 |
| 决议 68（上游例程要编得过、同步时保住版本号那一行） | 删了之后要多一条同步规则：**上游同步时不要把删掉的例程或库带回来**，需要记进 DECISIONS | [DECISIONS.md](../../docs/tables/DECISIONS.md):2602-2613 |
| 本图的全集计数 | map 写「上游 32」，但它给的 `find open_plc_arduino/libraries` 只扫出 31 个上游例程；第 32 个是 `CI/build` 下的 BareMinimum | [map.md](map.md)「全集」 |
| 自有库 / core | 12 个上游库里**只有 `SrcWrapper` 被 core 用到**（`cores/arduino/Arduino.h:33`、`platform.txt:117`），自有库 `OpenPLC_*` 一个都不 include；`OpenPLC_Net` 依赖的是 `STM32duino_LwIP`（不在本票范围，也没有例程） | 在 `libraries/OpenPLC_*`、`cores`、`variants` 下 grep `#include` 和 `library.properties` 的 `depends=` |
| 删整库时 | 要改 `libraries/CMakeLists.txt:3-13` 的 `add_subdirectory`；`CI/build/examples/BareMinimum` include 了 EEPROM / IWatchdog / Servo / SPI / SoftwareSerial / Wire / CMSIS_DSP，删其中任何一个库它就编不过（它本来就缺版本号那一行，现在也编不过） | 同左 |
| 其他测试 / 检查脚本 | 没有别的地方引用这些例程或库 | 在 `$TEST`、`OpenPLC_Docs/tools`、`OpenPLC_Docs/docs`、`package_index_json` 下 grep |

**按库归纳**（只有删例程和删整库两种做法）：

| 库 | 例程 | 建议 |
|---|---|---|
| `Keyboard`、`Mouse`、`SubGhz`、`RGB_LED_TLC59731` | 全删 | 删整库：本板用不了，也没人依赖 |
| `EEPROM` | 全删 | 见上面 EEPROM 那张表 |
| `Servo`、`SoftwareSerial` | 全删 | 只删例程或删整库都行；库本身对任何 GPIO 通用，但没有需求 |
| `SPI` | 两个都删 | **只删例程**，库留着（总线引到了 J4） |
| `Wire` | 全留 | 不动 |
| `IWatchdog`、`CMSIS_DSP` | 留，测 | 不动 |
| `SrcWrapper` | 留 | 不能删 |

## 顺带发现（不在本票范围）

| 发现 | 出处 | 影响 |
|---|---|---|
| **`OpenPLC_KNX` 的 `saveAppConfig()` 也擦扇区 15**：`KNX_APP_NVM_FLASH_ADDR` = `0x081E0000`，bank 2 sector 7 | `libraries/OpenPLC_KNX/src/knx_config.h:94-97`、`knx_nvm.cpp:93-107` | 已经有调用者：`OpenPLC_KNX/examples/KNX_SelfTest/KNX_SelfTest.ino:77`。跑一次就会擦掉校准值和 metadata，后果同上面 EEPROM |
| 板上有 LED 和按键，变体没映射：`LED_BUILTIN` / `USER_BTN` = `PNUM_NOT_DEFINED` | var `.h:410-416`；xlsx 156 `PE2 = LED_DRIVER`；BOM 有 LED1–3、SW1（复位）/ SW2（BOOT0，PG9） | 目前影响为零；#11 能测正是因为按键没映射。PE2 是不是 Bridge 上的 LED3「HBEAT」，**未核实**（Bridge 没有网表） |
