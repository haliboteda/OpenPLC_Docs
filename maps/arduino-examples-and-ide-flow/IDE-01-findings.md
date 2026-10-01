# IDE-01 调查结论：一个发布版今天是怎么到 Board Manager 的

票：[IDE-01（从改完代码到客户在 Board Manager 装到新版，每一步是什么）](issues/IDE-01-how-does-a-release-reach-board-manager.md)
调查日期：2026-09-24。只读调查，没有 push / tag / 建 release。

> ✅ **结论**：今天**没有任何发版脚本或发版文档**，整条链路全靠手工。
> 理由：四个仓里找不到 release / checksum 相关的脚本；`CHK-B1`–`CHK-B9` 只检查代码和板子，不碰索引 JSON 和 release（见 [ACCEPTANCE-CHECKLIST.md](../../docs/tables/ACCEPTANCE-CHECKLIST.md)）。

> ✅ **结论**：索引里现有的 0.1.3-pre 条目**能装**：下载地址 200、sha256 和 size 都对得上（实测见 §3）。
> 但它装上的是 **2026-04-23 的旧代码**，配的 IAPTool 更旧，是 2026-03-25 的（见 §4）。

---

## 1. 链路上的四个对外件

| 件 | 在哪 | 怎么产生 | 今天的状态 |
|---|---|---|---|
| 板卡包 zip | `https://github.com/haliboteda/open_plc_arduino/archive/refs/tags/v<版本>.zip` | **GitHub 按 tag 自动生成**，不是上传的 | tag `v0.1.3-pre` → `7b22679 add knx lib`（2026-04-23）；GitHub release `v0.1.3-pre` 没有任何附件 |
| STM32Tools（内含 IAPTool） | `https://github.com/haliboteda/Arduino_Tools/releases/download/v0.1.2/STM32Tools.tar.gz` | **手工**：把 IAPTool 二进制提交进 `Arduino_Tools` 仓（commit `4a833bf5 update iaptool`，2026-03-25），打 tag `v0.1.2`，把 `Arduino_Tools-0.1.2/` 打成 tarball 手工上传成 release 附件 | release 创建于 2026-03-25，附件 digest 和索引一致 |
| 网络发现程序 | `open_plc_arduino/tools/discovery/bin/*/network_discovery[.exe]` | **手工**跑 `tools/discovery/build.sh`，二进制**直接提交进 git**，随 tag zip 一起出去 | 首次加进来是 `d6552fc`（2026-08-11），**不在 `v0.1.3-pre` tag 里** |
| 索引 JSON | `package_index_json/package_openplc_alp_index.json`，**客户实际用的是 release 附件** `.../package_index_json/releases/download/v<版本>/package_openplc_alp_index.json` | **手工**改 JSON（checksum/size 手算），commit + 打 tag + 把 JSON 作为 release 附件上传 | 本机 IDE 配的地址就是 v0.1.3-pre 那个附件（`~/.arduinoIDE/arduino-cli.yaml`） |

⚠️ **IAPTool 不在 `IAPTranfer_Tool` 仓发 release**（`gh release list -R haliboteda/IAPTranfer_Tool` 为空）。
`compile_tool.sh:61-75` 调 `TestCase/tools/install_tool.py`，**只把二进制拷进本机** `$A15/.../STM32Tools/<ver>/`，不碰 `Arduino_Tools` 仓，也不碰任何 release。

## 2. 今天发一个版的每一步（按实物反推，无文档）

| # | 仓 | 动作 | 手工 / 脚本 | 对外？ |
|---|---|---|---|---|
| 1 | `IAPTranfer_Tool` | `compile_tool.sh` 编 IAPTool（win/darwin/linux amd64） | 脚本 | 否 |
| 2 | `Arduino_Tools` | 把 `Output/<os>/IAPTool*` 拷进 `win/` `macosx/` `linux/` 并提交 | **手工**（没有脚本做这一步） | 否 |
| 3 | `Arduino_Tools` | 打 tag `v<工具版本>`，push 到 GitHub `origin` | 手工 | **是：push + tag** |
| 4 | `Arduino_Tools` | 打出 `STM32Tools.tar.gz`（根目录 `Arduino_Tools-<版本>/`），建 GitHub release 并上传 | 手工 | **是：release** |
| 5 | `open_plc_arduino` | `tools/discovery/build.sh` 编四个 discovery 二进制并提交 | 手工触发脚本 | 否 |
| 6 | `open_plc_arduino` | 跑发版检查 `CHK-B1`（三处版本号一致）/ `CHK-B2`（跨仓镜像代码一致）/ `CHK-B3`（`$CORE_LIVE` 与仓库一致），见 [ACCEPTANCE-CHECKLIST.md](../../docs/tables/ACCEPTANCE-CHECKLIST.md) | 脚本 | 否 |
| 7 | `open_plc_arduino` | 打 tag `v<版本>`，push 到 GitHub `origin`（不是 `internal` —— 索引指向 GitHub） | 手工 | **是：push + tag** |
| 8 | `open_plc_arduino` | 建 GitHub release（历史上一直有，但**没有附件**，Board Manager 不读它） | 手工 | 是：release（可省） |
| 9 | 本机 | 下载 `archive/refs/tags/v<版本>.zip`，算 sha256 和字节数 | **手工** | 否 |
| 10 | `package_index_json` | 在 `platforms[]` 顶部加一条；`toolsDependencies` 里 `STM32Tools` 版本改成第 4 步的；需要的话在 `tools[]` 加新 STM32Tools 条目（checksum/size 同样手算） | **手工** | 否 |
| 11 | `package_index_json` | commit，打 tag `v<版本>`，push | 手工 | **是：push + tag** |
| 12 | `package_index_json` | 建 GitHub release `v<版本>`，上传 JSON 作为附件 | 手工 | **是：release** |
| 13 | 客户 | 在 IDE「其他开发板管理器地址」填第 12 步那个附件的 URL，Board Manager 安装 | 客户 | — |

⚠️ **第 12/13 步有个断点**：客户地址是**按版本号钉死**的 release 附件。
`v0.1.2` 那个附件里只有 `0.1.2 / 0.1.1 / 0.1.0`（实测），**填旧地址的客户永远看不到新版**。
`raw.githubusercontent.com/.../master/package_openplc_alp_index.json` 内容与 v0.1.3-pre 附件逐字相同，但**没有任何文档告诉客户该填哪个地址**（全仓 grep 不到）。

## 3. 现有 0.1.3-pre 条目能不能装（实测 2026-09-24）

| 项 | 索引里写的 | 实测 | 结果 |
|---|---|---|---|
| 板卡包 URL | `.../open_plc_arduino/archive/refs/tags/v0.1.3-pre.zip`（`package_openplc_alp_index.json:14`） | HTTP 200 | ✅ |
| 板卡包 checksum | `SHA-256:80F46A18…81BF4BE`（`:16`） | `80f46a18…81bf4be` | ✅ 一致 |
| 板卡包 size | `11276626`（`:17`） | 11276626 | ✅ |
| STM32Tools 0.1.2 URL | `.../Arduino_Tools/releases/download/v0.1.2/STM32Tools.tar.gz` | HTTP 200 | ✅ |
| STM32Tools checksum / size | `ECD0F752…C8EA586` / `9996281` | 一致；GitHub 附件 digest 也是这个值 | ✅ |
| 索引 JSON 本身 | 本地 = `origin/master` = v0.1.3-pre release 附件 | 去掉 CRLF 后逐字相同 | ✅ |

xpack gcc / openocd / CMSIS 是第三方 release，**没有逐个下载校验**。

## 4. 能装，但装上的东西不对

| 问题 | 证据 | 影响 |
|---|---|---|
| tag `v0.1.3-pre` 是旧代码 | 指向 `7b22679`（2026-04-23），落后当前 `v0.1.3-dev` 33 个 commit；里面没有 `tools/discovery`、没有 `pluggable_discovery`，`boards.txt` 里没有 `build.fw_version` | 客户装到的不是现在测过的这版 |
| 发出去的 IAPTool 比仓库旧半年 | release 里的 `win/IAPTool.exe` sha256 `046d3e89…` 等于 `Arduino_Tools` 的 `4a833bf5`；本机 `STM32Tools/0.1.2/win/IAPTool.exe` 是 `6bcd6fcb…`（= `IAPTranfer_Tool/Output/windows/IAPTool.exe`，2026-09-22）。旧版里没有 `--force`、`setowner`、`takeown` | 当前 `platform.txt:239,249` 会传 `{upload.force_flag}`，选了「强制烧写」菜单的客户会拿旧 IAPTool 失败 |
| 本机测的根本不是发出去的那份 | `install_tool.py` 把新 IAPTool 覆盖进 `STM32Tools/0.1.2/`，**版本号没变**；用例 **P11**（`TestCase/tools/check_tool_sync.py`：包里的 IAPTool 不能比仓库的旧）比的是本机这份，不是 release 附件 | P11 全绿也证明不了客户那份是新的 |
| release 里没有 `keys/` | tarball 里没有 `win/keys/`；IAPTool 找默认签名密钥的位置是 `<exe>/keys/fw_signing_key.pem`（`IAPTranfer_Tool/sign.go:28-29,54`） | **没验证**：客户从 IDE 上传时缺这把密钥会怎样 |

## 5. 发 0.1.3（不是 0.1.3-pre）要改的地方

版本统一叫 0.1.3。固件和 `boards.txt:28`（`build.fw_version=0.1.3`）已经是 0.1.3，带 `-pre` 的只有下面这些：

| 东西 | 现在 | 发 0.1.3 后 | 谁动 |
|---|---|---|---|
| 索引 `platforms[0]`（`package_openplc_alp_index.json:12-17`） | `version` `0.1.3-pre`，`url` `.../v0.1.3-pre.zip`，`archiveFileName` `open_plc_arduino-0.1.3-pre.zip`，checksum/size 对应旧 zip | 新增一条 `0.1.3`，url/文件名改成 `v0.1.3`，checksum/size 按新 zip 重算。**0.1.3-pre 条目留不留要定** | 手工 |
| 索引 `toolsDependencies.STM32Tools` | `0.1.2` | 新工具版本号（见下一行），因为 IDE 不会给同版本号的工具重新下载 | 手工 |
| `Arduino_Tools` tag / release | `v0.1.2` | 新 tag（例如 `v0.1.3`，号是独立的，见 `package_index_json/CLAUDE.md`），附件里放当前 IAPTool | 手工，对外 |
| `open_plc_arduino` tag | `v0.1.3-pre` | `v0.1.3`。⚠️ 仓里**已有一个叫 `v0.1.3` 的分支**（`origin/v0.1.3` → `5127758`，2026-04-07），再打同名 tag 会像现在 `v0.1.3-pre` 一样出现 `refname is ambiguous`。GitHub 的 `refs/tags/` URL 不受影响 | 手工，对外 |
| `package_index_json` tag / release 附件 | `v0.1.3-pre` | `v0.1.3`；客户地址随之变成 `.../releases/download/v0.1.3/...` | 手工，对外 |
| 已装目录 | `$A15/packages/OpenPLC_Alpha/hardware/stm32/0.1.3-pre` | Board Manager 升级后变成 `.../stm32/0.1.3` | IDE |
| `CORE_LIVE`（`$TEST/config/machine.py:52`） | 写死 `...\stm32\0.1.3-pre` | 改成 `...\stm32\0.1.3`，或重跑 `init_machine.py` | 手工 / 脚本 |
| `init_machine.py` 自动探测（`TestCase/tools/init_machine.py:103-106,152`） | 取 `stm32/*` 字符串排序的最后一个 | ⚠️ `0.1.3-pre` 排在 `0.1.3` **后面**。两个目录同时存在时它会选中旧的 `-pre` | 要么删掉旧目录，要么改排序 |
| `init_machine.py` 模板示例（`:483,502,524`） | `0.1.3-pre` | 只是示例文本，不影响探测 | 可顺手改 |
| `IAPTool` 查找（`TestCase/tools/common.py:281`） | `STM32Tools/*` 通配 | 不用改 | — |

`open_plc_arduino` 的 `v0.1.3-dev` 比 GitHub 上的领先 12 个 commit；`internal`（git.schaeffer-ag.de）今天连不上（`Connection reset`）。**打 tag 之前得先 push，否则 zip 里没有这 12 个 commit。**

## 6. 小问题（不影响安装）

| 问题 | 在哪 |
|---|---|
| `platform.txt:258` 注释写的是 `build.ps1`，实际文件是 `build.py` | `open_plc_arduino/platform.txt:258` |
| `tools/discovery/bin/windows_amd64/err.log` 被提交进了 git，会跟着 zip 发出去 | `git ls-files tools/discovery` |
| `package_index_json/CLAUDE.md` 的示意图写的是 `.tar.gz`，索引实际用的是 `.zip` | `package_index_json/CLAUDE.md` 链路图 |
| 维护者邮箱是个人 gmail | `package_openplc_alp_index.json:7` |

## 7. 没验证的

| 项 | 为什么没验证 |
|---|---|
| 在一台干净机器上从 Board Manager 走完一遍安装 | 只做了下载加校验，没有真的装 |
| `STM32Tools.tar.gz` 是不是 GitHub 自动生成的 tag 归档原样上传的 | 自动归档下载超时、下到一半，没比完 |
| GitHub 的 tag zip 以后还会不会逐字节不变 | 今天的 checksum 对得上；更早那次对不对不知道 |
| zip 解开后 `macos-launcher.sh`、linux/darwin 二进制还有没有可执行位 | 没在 macOS / Linux 上装过 |
| 缺 `keys/` 时从 IDE 上传会怎样 | 没在干净环境试过 |
| 三方工具（xpack gcc/openocd、CMSIS）的 checksum | 没下载（每个 200 MB 以上） |
| 客户今天实际填的是哪个索引地址 | 找不到任何面向客户的安装说明 |
