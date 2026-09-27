# Linux / macOS 用户怎么拿到能运行的 IAPTool

Type: grilling
Opened: 2026-09-27
Status: open
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
