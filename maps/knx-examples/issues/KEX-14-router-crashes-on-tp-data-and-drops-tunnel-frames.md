# 换成 IP 路由器后开机死机、隧道不回确认

Type: grilling
Opened: 2026-10-15
Status: open
Blocked by: -

## Question

2026-10-15 跑 `T3-19` 时在真板上发现两处缺陷：

| 现象 | 证据 | 出处 |
|---|---|---|
| **换角色后开机即 BusFault**：板上 KNX 数据区存着 TP 设备（0x07B0）经 ETS 写的数据时，`KNX_IPRouter`（0x091A）开机死在 BusFault，网络不起、IAP 上传也收不回来 | CFSR `0x8200`，BFAR `0x24080000`（AXI SRAM 末尾外一字节）；栈帧 PC 在 `popByteArray()`，调用链 `DataProperty::write()` → `DataProperty::restore()`；寄存器显示从 `0x2407B5E0` 起拷约 256 KiB。用 ST-Link 擦掉 KNX 数据区后正常启动 | `$CORE_REPO` `libraries/OpenPLC_KNX/src/knx/`；数据区布局见 [BOOTLOADER-PROJECT-LAYOUT](../../../docs/build/BOOTLOADER-PROJECT-LAYOUT.md) |
| **经路由器开隧道，PC 发的帧收不到 TUNNELLING_ACK**：未经 ETS 编程的路由器，xknx 能连上（分到 1.1.1），还能收到 TP 侧的温度帧（TP → IP 通）；PC 发 `w 1/0/1 1` / `0` 三次重试都没有确认，测试盒网关那边总线上也没出现（IP → TP 不通） | `knx_monitor.py --gateway 192.168.0.32` 报 `Did not receive a TUNNELLING_ACK within 1 second` | `$CORE_REPO` `libraries/OpenPLC_KNX/src/knx/` 的隧道 / cEMI 服务 |

第一处会让用户换个例程就把板子变砖（只能 ST-Link 擦或按 BOOT0 进上传模式）。第二处让 `T3-19` 判不过；是否和「路由器没经 ETS 编程」有关没核实。

2026-10-15 查到根因（主机上用真的 `knx/*.cpp` 复现）：

| 缺陷 | 根因 | 状态 |
|---|---|---|
| 隧道不回确认 | 平台返回 IP 时做了 `lwip_ntohl`，栈又 `htonl` 一次，CONNECT_RESPONSE 里的数据端点成了 32.0.168.192，PC 的请求发到了不存在的地址；和是否经 ETS 编程无关 | **已修**：`$CORE_REPO` `libraries/OpenPLC_KNX/src/stm32h743_openplc_platform.cpp` 改回返回网络序；真板上经板子隧道写 1/0/1 的 1、0，测试盒那边都收到 |
| 换角色开机死机 | 数据区头部只比 apiVersion / 厂商号 / hardwareType / version，四样在两种角色下相同（hardwareType 从没设、全 0；version 写死 0x0100，`OpenPLC_KNX.cpp:115`），于是按本角色的布局恢复别的角色的数据；`DataProperty::restore` 不查元素数上限（`knx/data_property.cpp:126-138`），读出 0xFFFF 就越界。反过来 TP 设备读路由器数据、或写到一半断电的数据，同样会坏（`knx/table_object.cpp:96-97`、`knx/memory.cpp:131`） | 方案 A、D 用户 2026-10-16 定，行为见 [M3](../../../docs/modules/M3-app-runtime.md) `R3-20`；B、C 不做（有 A 和 D 后没有需要它们的已知情况） |

| 修法（换角色死机） | 改什么 | 代价 / 风险 | 推荐 |
|---|---|---|---|
| A. 角色写进 hardwareType | `OpenPLC_KNX.cpp` 在读数据区前把 `MASK_VERSION` 放进 hardwareType；不匹配就走现成的「数据无效」，不恢复 | 只改板卡包 1 处；已经用 ETS 编过程的板子升级后失效一次，要重新下载 | ✅ |
| B. `DataProperty::restore` 查元素数上限 | 栈里加检查，失败往上传 | 改外来的栈；只挡属性长度，挡不住表地址错位 | 作 A 的补充 |
| C. 数据块加 CRC | `knx/memory.cpp` 读写 | 改外来的栈、存储格式变，所有板失效一次；只有它能盖住写到一半断电 | 要覆盖断电就和 A 一起上 |
| D. 最后写头部 | `knx_nvm.cpp` 擦完先写头部以外的数据，最后写含头部的 32 字节；中途断电头部仍是 `0xFF`，按无效处理 | 只改板卡包约 5 行，不碰协议栈、格式不变 | ✅ 用户 2026-10-16 定，代替 B、C |

用户 2026-10-15 定的方向（细节在讨论）：

| 事 | 定了什么 |
|---|---|
| 角色在哪定 | sketch 里写一行 `OPENPLC_KNX_ROLE(...)`，菜单不再有 KNX 角色；编译前由 `prebuild.sh` 读出、作为编译参数同时交给 sketch 和库（做法 A，库不动）。**2026-10-17 已实现**：写法 `OPENPLC_KNX_ROLE(TP_DEVICE);` / `OPENPLC_KNX_ROLE(IP_ROUTER);`，`knxrole` 菜单和 `build.knx_flags` 已删，6 个例程已改；行为见 [M3](../../../docs/modules/M3-app-runtime.md) `R3-24`。未编译验证 |
| 参数能否传给库（2026-10-15 在已装板卡包上做原型、已恢复） | **能**：`prebuild.sh` 读出角色，生成 `{build.path}/sketch/openplc_knx_role.h`，经现有的 `build.opt`（`platform.txt:25`）`-include` 给每个编译单元；`platform.txt` 不改。实测 TP / 路由器两种 ELF 里分别只有 `Bau07B0` / `Bau091A`，换角色全部重编、不换不重编；不用 KNX 的 sketch 照常编；没写角色报 `#error`。只在 Windows 上实测 |
| 角色和板上数据不一致 | 要用户在菜单选强制覆盖才能传，选了就擦掉 KNX 数据区再写新的；谁来比、菜单怎么设在讨论 |

2026-10-15 讨论到这里（用户在考虑）：

| 事 | 现在的方向 |
|---|---|
| 角色不一致的提醒放哪 | 用户要在 Arduino 这一侧（IAPTool / IDE 输出窗口）提醒，不放 bootloader 判断；板上角色从 KNX 数据区头（`0x081C0000`）读，app 和 bootloader 都只「报」不「判」 |
| 不等重启就拿到角色 | 依赖 [IDE-17](../../arduino-examples-and-ide-flow/issues/IDE-17-usb-and-ethernet-share-one-upload-flow.md) 的 USB 双口方案：sketch 运行时 USB 也有 IAP 口应答 |
| 强制覆盖 | 菜单选项，擦 KNX 数据区后写新程序；一次性还是常开、谁来擦，未定 |
| 开机头部检查（方案 A） | 用户 2026-10-16 定：做（M3 `R3-20`），兜住 ST-Link 直烧和旧板子；断电写坏由方案 D 兜住 |

## 怎么算答完

两处各查到根因、定修法；先改 [M3](../../../docs/modules/M3-app-runtime.md) 写下行为（换角色时数据区怎么处理），再改代码；`T3-19` 在真板上过。

## Answer

## 引出了什么新的未知
