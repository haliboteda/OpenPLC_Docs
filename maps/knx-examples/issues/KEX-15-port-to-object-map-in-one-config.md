# 端口和 KNX 对象的映射放进一个配置文件，工具生成产品文件和代码

Type: grilling
Opened: 2026-10-15
Status: resolved
Blocked by: -

## Question

用户 2026-10-15 提：板上端口和 ETS 对象的对应关系（如继电器 1 → 对象 1、2，DI1 → 对象 13）现在写死在两处，`$ETSPROD` `OpenPLC_TP.xml` 和各例程代码。要改成一个配置文件，由一个工具同时生成产品文件（`.xml` / `.knxprod`）和代码用的映射文件，改映射只改配置。

端子接到 MCU 哪个引脚不在此列：那由板子走线决定，唯一出处是原理图。

| 问题 | 定了什么（用户 2026-10-15） |
|---|---|
| 改了已有对象（编号、DPT、读写标志、删除） | 工具打 warning 说明后果（用户 ETS 工程里的组地址关联会错位），照常生成、不挡流程；新增对象不提示 |
| 应用版本号 | 用户在配置里自己写，不写工具报错退出、不生成（同 `OPENPLC_APP_VERSION`）；对象有改动而版本号没变时再加一条 warning |
| 结构 | 映射单独成一个文件，代码不写死对象编号，从生成的映射文件取 |
| 工具放哪 | 工具和配置放 `$ETSPROD`，生成产品文件，并把映射头文件写进 `$CORE_REPO` `libraries/OpenPLC_KNX/src/`；头文件是生成的副本，由 P2 比对和配置一致（用户 2026-10-16） |
| 签名工具和路径 | OpenKNXproducer v4.3.12 的 Windows x64 exe（85 MB）和 GPL-3.0 许可证直接提交进 `$ETSPROD` `tools/OpenKNXproducer/`；工具里的路径都相对仓库，ETS 的候选安装位置单独放在 `tools/ets_paths.json`（[决策 145](../../../docs/tables/DECISIONS.md)，用户 2026-10-16 选 A） |
| 配置格式 | JSON：Python 自带、零依赖，和工装方案文件（`$PORTTOOL` `src/plans/*.json`）一致；说明写进 `note` 字段（用户 2026-10-16） |
| 平台 | 只做 Windows：ETS 官方只支持 Windows（用户 2026-10-16，[决策 143](../../../docs/tables/DECISIONS.md)） |
| ETS 版本 | 签名只支持 ETS 5.7（命名空间 20，KEX-01 实测过）：找到 ETS6 没找到 5.7 时报「暂只支持 ETS 5.7」；6.0–6.3 等有 ETS6 环境验证后再加（用户 2026-10-16）；高于 6.3 的提示暂不支持 |

已知：本机做法是 OpenKNXproducer 生成、调本机 ETS 5.7 的签名 DLL 签名（[KEX-01-findings.md](../KEX-01-findings.md)）。它找 ETS 的顺序：`%USERPROFILE%\bin\CV\` 的子目录 → `C:\Program Files (x86)\ETS6`、`C:\Program Files\ETS6` → 两处 ETS5；目录里要有 `Knx.Ets.Xml.ObjectModel.dll`，按它的版本配 XML 命名空间（5.7 → 20，6.0 → 22，6.1 → 23，6.2 / 6.3 → 24）（[SignHelper.cs](https://github.com/OpenKNX/OpenKNX.Toolbox.Sign/blob/main/SignHelper.cs) `FindEtsPath`）。未核实：我们的源 XML 是命名空间 20，只装 ETS6 的机器能否签它。

另：ETS 6.3.0 起未注册产品显示警告、不能复制粘贴（[KNX 支持文章](https://support.knx.org/hc/en-us/articles/26285336909330-Handling-unregistered-Products-in-ETS)）；`M-00FA` 在 ETS 6.3+ 的表现未核实。

## 怎么算答完

工具放哪个仓定下来；先写进文档再写工具。

## Answer

2026-10-16 全部定完，见上面「定了什么」那张表。2026-10-17 做完，ETS 5.7 导入成功；行为写在 [M3](../../../docs/modules/M3-app-runtime.md) `R3-21` / `T3-23` 和 `$ETSPROD` README「Object map」。

## 引出了什么新的未知
