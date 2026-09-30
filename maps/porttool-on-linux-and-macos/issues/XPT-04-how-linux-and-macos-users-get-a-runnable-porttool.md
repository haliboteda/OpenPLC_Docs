# Linux / macOS 用户怎么拿到能运行的 PortTool

Type: grilling
Opened: 2026-09-30
Status: open
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
| 用户用 git 把 PortTool 发给用户，所以可执行位要记在 git 里（文件模式 `100755`），和 IDE-15 的修法相同 | 用户 2026-09-30 |

## 怎么算答完

一句话写明选了哪条；写出发布包的文件名和里面的目录；在 Linux 上实测「下载 → 解压 → 双击」能打开面板。
