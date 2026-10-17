# KNX 协议栈存 ETS 数据的区域多大

Type: grilling
Opened: 2026-10-12
Status: resolved
Blocked by: -

## Question

用户 2026-10-12：「板子上的数据配置要跟正规协议协议里面的对应上，跟标准一致。」

现在实际用 1024 B：协议栈的编译单元看不到 `knx_config.h` 的 4096，取了 `knx/platform.h` 的默认值（编译时报 `KNX_FLASH_SIZE not defined, using 1024`）。[BOOTLOADER-PROJECT-LAYOUT.md](../../../docs/build/BOOTLOADER-PROJECT-LAYOUT.md) 写的 4 KiB 与实际不符。

| 出处 | 说了什么 |
|---|---|
| 上游 thelsing/knx `examples/knx-demo/platformio.ini` | `-DKNX_FLASH_SIZE=…` 作全局编译开关，大小由设备自选 |
| ETS 主数据 `knx_master.xml` 的 `MV-091A` | IP 路由器过滤表在 512 起、长 8192，至少要 8704 B；上游 `bau091A.cpp:18` 一致 |
| ETS 主数据 `MV-07B0` | 各表按实际链接数分配，标准不给固定大小 |

> 影响：`KNX_IPRouter`（0x091A）在 1024 B 下，ETS 一下载过滤表就写坏堆（还没上过真总线）；TP 设备约能放 110 条链接，超了停机。

| 做法 | 大小 | 0x091A | 0x07B0 约能放 | 推荐 |
|---|---|---|---|---|
| A | 统一 8704 | 刚好够 | 1390 条链接 | |
| B | 统一 16384 | 够，有余量 | 2700 条链接 | ✅ 一个值满足标准下限，扇区 6（128 KiB）和 RAM 都够 |
| C | 按角色：07B0 用 4096，091A 用 8704 | 够 | 620 条 | |
| D | 保持 1024 | 不够 | 110 条 | |

实现方式确定：`boards.txt` 的 `build.knx_flags` 加 `-DKNX_FLASH_SIZE=…`（和 `MASK_VERSION` 同处），`knx_config.h` 没定义就 `#error`。调大后已下载的数据仍有效（读代码）。2026-10-17 起 `build.knx_flags` 已删，两个值改由 `prebuild.sh` 按 sketch 里的角色生成的头文件定义（[M3](../../../docs/modules/M3-app-runtime.md) `R3-24`）。

连带：`OpenPLC_ETS_Prod/OpenPLC_TP.xml:72-73` 的 `MaxEntries="65000"` 向 ETS 承诺的容量远超板子能放的，要按选定大小改并重新生成 `.knxprod`。

## 怎么算答完

用户选定大小；先改 BOOTLOADER-PROJECT-LAYOUT.md 和 `knx_config.h` 注释，再改 `boards.txt`、`MaxEntries`；6 个 KNX 例程编过、`using 1024` 警告消失。

## Answer

2026-10-12 定：B，所有角色统一 16384 B。用户原话：「B 其他问题按推荐的来。」

| 定了什么 | 一句理由 |
|---|---|
| `boards.txt` 的 `build.knx_flags` 加 `-DKNX_FLASH_SIZE=16384`，`knx_config.h` 没定义就 `#error` | 协议栈每个编译单元都看到同一个值，和上游 `platformio.ini` 的做法一致 |
| 产品文件的 `AddressTable` / `AssociationTable` `MaxEntries` 改成 2600 | 按协议栈的实际布局算，16 KiB 能放 2705 条，留约 600 B 余量；公式在 `$ETSPROD/README.md` |
| 产品文件应用版本 4 → 5 | 内容变了；ETS 按应用号 + 版本认应用，同号同版本不许是两个产品（`$ETSPROD/README.md`「Regenerating the product」） |
| 协议栈调试输出默认关，`-DKNX_DEBUG` 才打开；删掉没人定义的 `USE_RF` 分支 | 开机不再往 RS232 倒 `readMemory` / `RESTORED` 十六进制；RF 文件早已删掉 |

## 引出了什么新的未知

没有。2026-10-13 上板确认：16 KiB 程序开机 `1.1.20, configured`、无调试行；ETS 把设备原地更新到版本 5 并下载成功。
