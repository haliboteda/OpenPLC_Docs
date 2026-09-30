# Linux / macOS 用户怎么拿到能运行的 PortTool

Type: grilling
Opened: 2026-09-30
Status: resolved
Blocked by: XPT-02

## Question

在 Windows 上生成的文件拷到 Linux / macOS 上没有可执行位；macOS 还会拦截没签名的程序。IAPTool 踩过同一个坑，见 [Linux / macOS 用户怎么拿到能运行的 IAPTool](../../arduino-examples-and-ide-flow/issues/IDE-15-how-do-linux-and-macos-users-get-an-executable-iaptool.md)（那边证实了 tar 里的权限会被保留）。要定：

| 选项 | 代价 | 风险 |
|---|---|---|
| A. 发 `.tar.gz`，打包时写上可执行位；macOS 在说明里写怎么放行 | 构建脚本里加打包 | Mac 用户第一次要手动放行 |
| B. 同 A，macOS 版另做签名和公证 | 要 Apple 开发者账号 | 账号和证书要有人管 |
| C. 发 `.zip`，说明里写 `chmod +x` | 最小 | 用户漏看就打不开 |

连带要定：和 IDE-15 那边一起解决，还是各走各的。

## 已有的事实

| 事实 | 出处 |
|---|---|
| 用户通过 git 拿到的是 `IAPTranfer_Tool` **源码仓库**，自己用 `go build` 编出本平台的 PortTool；仓库 README 补编译说明。自己编出来的文件本来就有可执行位，不用在 git 里记 | 用户 2026-09-30 |
| 全新 clone、清空模块缓存后，只装 Go 1.23 就编得出 Windows / Linux 版 PortTool 和 IAPTool；第一次要联网下三个依赖 | 2026-09-30 在 Windows 上实测 |

## 怎么算答完

一句话写明选了哪条；写出发布包的文件名和里面的目录；在 Linux 上实测「下载 → 解压 → 双击」能打开面板。

## Answer

2026-09-30 定：**不发可执行文件，用户 clone 源码仓库 `IAPTranfer_Tool` 后自己 `go build`** —— 上面 A / B / C 都不选。自己编出来的文件本来就有可执行位，Mac 上也不经过下载隔离。

- `$TOOL/README.md` 新增「Building from source」一节：本机编译、交叉编译、`plans/` 要拷到可执行文件旁边、Linux 要 `dialout` 组
- 实测（WSL Debian 13，Go 1.23.1）：全新 clone → `go build` → 两个文件都是 `-rwxr-xr-x`；面板能起并列出方案；接真板子 `bench-smoke.json` 7/7 过。WSL 里访问不了 HTTPS，依赖模块是从 Windows 那次全新下载的缓存拷进来的，「第一次联网下载依赖」只在 Windows 上验过

## 引出了什么新的未知

- Mac 上自己编译、运行：没有 Mac，归 [在哪几台真机上验、用例怎么写](XPT-03-which-real-machines-and-what-the-test-case-is.md)
