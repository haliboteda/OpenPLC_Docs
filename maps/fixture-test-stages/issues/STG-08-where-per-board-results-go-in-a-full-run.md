# 工装完整测试时逐板结果记在哪

Type: grilling
Opened: 2026-10-09
Status: resolved
Blocked by: STG-01

## Question

单独跑某一步时不记录（决策 89）。工装完整测试时，每块板的结果按什么键（UID？SN？）记、记在哪、记什么？中途停下的那次记成什么（决策 96）？接替原「产线测试补齐」图的 PTG-01「逐板验收记录存在哪」（那张图 2026-10-17 已删）。

## 怎么算答完

记录的键、位置、字段写定。

## Answer

2026-10-10 用户按推荐定：记录放 A，停下记 `STOPPED`，PTG-01 一起关。

**结论**：沿用 PortTool 现有的报告格式（`$PORTTOOL/src/ptreport/ptreport.go`），每次工装完整测试写一份 JSON；按芯片 UID 分目录，SN 有就记。

| 事 | 定案 | 理由 / 出处 |
|---|---|---|
| 键 | 芯片 UID（`pt.id` 的 `uid=`，24 位十六进制）；SN 是可选字段 | UID 每块板都读得到，SN 只有扫了码才有（决策 20：SN 从外部读入）；校准存档已按 UID 分目录（`src/calstore`） |
| 位置 | exe 旁边的 `records/<UID>/`，一次运行一个文件 `<YYYYMMDD-HHMMSS>[-<SN>].json`，从不覆盖 | 和 `calibration/<UID>/`、`runlogs/` 同样的放法；文件名带 SN，按 SN 找回时搜文件名即可 |
| 字段 | `ptreport.Report` 现有字段：方案名、`limit_version`、PortTool 版本、固件、`board_uid`、`sn`、起止时间；每一步一条 `StepResult`（`type` 填步号 2 / 4 / 5 / 6，含每次尝试的原始值和判定）；安规的问卷答案放这一步的 `extra`（[STG-09](STG-09-what-the-safety-test-stage-reserves.md)） | 格式已有、带原始值，限值改了能重判 |
| 已过的步 | `records/<UID>/progress.json`：已通过的步号和对应报告文件名；再接上同一块板时据此问「从第 N 步继续」（决策 96） | 进度和报告分开：报告只追加，进度会被改写 |
| 中途停下 | 照样写一份报告，停下的那一步记新结果 `STOPPED`，后面没跑的记 `SKIPPED`；第 6 步没能恢复出厂时在 `reason` 写「带着产线的根」 | `ptreport` 已把 `TIMEOUT` 和 `FAIL` 分开记，停下也不该混进 `FAIL` |
| 单独跑某一步 | 不写（决策 89） | — |
| 不做 | 上传 ERP / MES、按 SN 建库查重（决策 20） | 外部系统自己读 `records/` |

### 记在哪：两条路

| 路 | 代价 | 风险 | 推荐 |
|---|---|---|---|
| A · exe 旁边固定的 `records/<UID>/` | 新加一个目录约定 | 换电脑跑，记录分散在几台 PC 上 | ✅ 面板没有方案文件也能写；和校准存档同一套找法 |
| B · 方案文件里的报告输出目录（`ptseq` 现有的 `dir` 输出，文件名 `<SN 或 UID>-<时间>.json`） | 现成 | 面板的完整测试不经过 `ptseq`；没有按 UID 分目录，`progress.json` 无处放 | |

### 和 PTG-01 的关系

原 PTG-01「逐板验收记录存在哪」问的是同一件事（每块板出厂结果写成什么、写在哪、怎么按 SN 找回），已随本票一起关。它要的「拿一块板走一遍、按 SN 找回」留到上板时做。注：PTG-01 提到的 `ID-MAP.md`「结果记在哪」一栏现在已不存在。

## 引出了什么新的未知

- 实现：TODO-fixture 第 46 条
- 拿一块板走一遍、按 SN 找回：TODO-fixture 第 45 条
