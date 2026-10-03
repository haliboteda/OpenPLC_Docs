# Linux / macOS 用户怎么拿到能运行的 IAPTool

Type: grilling
Opened: 2026-09-27
Status: resolved
Blocked by: -

## Question

已发布的 STM32Tools `0.1.3` 里 linux / macosx 的 `IAPTool` 没有可执行位，IDE 上传必然失败；有 Linux 和 macOS 用户（用户 2026-09-27）。要定：**用哪种发布方式让已装 0.1.3 的用户和新用户都拿到修好的包**。

git 里的修法已知：`Arduino_Tools` 里 `git update-index --chmod=+x linux/IAPTool macosx/IAPTool` 一次；`core.fileMode=false` 下以后换二进制会保留 `100755`。

## 已有的事实（2026-09-27，WSL Debian 13 + Linux 版 arduino-cli 1.5.1）

| 事实 | 怎么得到的 |
|---|---|
| 从网上装的 0.1.3：`IAPTool` 是 `-rw-r--r--`，运行报 `Permission denied`；同包的 `dfu-util` 是 `-rwxr-xr-x` | 空数据目录从固定索引地址安装 |
| arduino-cli 解压保留 tar 里的权限，所以 git 里记对即可 | 同上（`dfu-util` 在 git 里是 `100755`） |
| 在 0.1.3 板卡包的依赖里换成新工具包 `0.1.4`，或原地替换 0.1.3 的附件：**已装 0.1.3 的用户刷新索引后看不到更新**，`core upgrade` 答「已是最新」 | 本地镜像模拟索引，从一份已装 0.1.3 的数据目录出发 |
| 同时发板卡包 `0.1.4`（内容不变）+ STM32Tools `0.1.4`：已装用户看到 `0.1.3 → 0.1.4` 更新，`core upgrade` 装上 STM32Tools `0.1.4` 并卸掉 `0.1.3` | 同上 |

⚠️ 没验到的：升级后 `IAPTool` 能不能运行（那一步 WSL 的 HTTPS 断了没跑完）；新用户路径；macOS。

## 怎么算答完

选定发布方式；已装 0.1.3 的 Linux 用户按 IDE 的正常操作能拿到能运行的 `IAPTool`，在 Linux 上实测。

## Answer

2026-10-03 定（用户：只针对 0.1.3 修改，保证这个版本全部正常）。不发 0.1.4，原地替换 0.1.3：把 GitHub release `0.1.3` 上原来的 `STM32Tools.tar.gz` 下载下来，只把 `linux/IAPTool`、`macosx/IAPTool` 两个文件的权限从 `0664` 改成 `0775`（和同包 `dfu-util` 一样），其余 85 个文件逐个比对未变；新包 SHA-256 `B2F9D413…`、13,287,279 字节，已替换 release 附件，索引里四行校验值和大小同步更新（`package_index_json` `e58fae2`），`Arduino_Tools` 的 git 也记成 `100755`（`f0d8e547`）。公开根私钥不删：0.1.3 的板子和 IAPTool 要用它，删了 0.1.3 反而坏。

已经装了 0.1.3 的 Linux / macOS 用户，因为版本号没变，IDE 不会自己重新下载：在 IDE 里卸载再装一次板卡包，或者在本机对已装的 `IAPTool` 跑一次 `chmod +x`。新装的用户不用做任何事。

验过：WSL Debian 里解压新包，`IAPTool` 是 `-rwxr-xr-x`、直接运行打出用法；线上索引返回新的校验值。

## 引出了什么新的未知

没验到：macOS（没有机器）；在真的 Linux IDE 里从网上完整装一遍、点 Upload。

## 后来补的

2026-10-03 同日，在 WSL Debian 里删掉重装后编译，发现 0.1.3 在 Linux 上**连编译都不行**：板卡包的 `system/extras/prebuild.sh`、`postbuild.sh` 和网口发现 `network_discovery`（Linux、macOS 各一份）、`macos-launcher.sh` 也没有可执行权限；STM32Tools 的 `stm32CubeProg.sh` 同样。根因是板卡包用 GitHub 按 tag 自动生成的 zip 发布，它把每个文件标成 DOS 创建的，arduino-cli 解压时丢掉 Unix 权限。

用户定：只修 0.1.3，tag 可以删了重建，先保证程序没问题再建 tag。做法：
- 板卡包：在原 tag 提交上只改这 6 个文件权限（`d179678`），打成 tar.gz（和原 zip 比，2130 个文件内容一致、只有这 6 个权限不同），作为 `open_plc_arduino` release `0.1.3` 的附件；tag `0.1.3` 重建到 `d179678`
- STM32Tools：附件再换一次，加上 `stm32CubeProg.sh`；`Arduino_Tools` 的 tag `0.1.3` 重建到只差这 3 个权限的提交
- 索引 `package_index_json` `80ba4f1`：板卡包改指 release 附件；`CLAUDE.md` 写明以后都发 tar.gz（`0537c6f`）
- 开发分支 `v0.1.3-dev` 和 `Arduino_Tools` 的 git 也记成 `100755`

先用本地索引在 WSL 里装、测通，再发布；发布后从线上索引删掉重装再测一遍：权限全是 `-rwxr-xr-x`，`DO_Outputs` 编过，`IAPTool` 能运行，网口发现能运行。没测到：上传（要接板子）、macOS。WSL 里 IDE 的配置顺带改了：板卡包索引从 0.1.2 时期的旧地址换成固定地址，没在运行的代理 `127.0.0.1:5780` 清掉了。
