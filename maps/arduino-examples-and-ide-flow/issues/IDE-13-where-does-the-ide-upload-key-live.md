# IDE 上传用的密钥放在哪、怎么放进去

Type: grilling
Opened: 2026-09-24
Status: resolved
Blocked by: IDE-01

## Question

IDE 上传时 IAPTool 到板卡包的 `STM32Tools\<版本>\win\keys\` 找密钥（见 [IDE-02-findings.md](../IDE-02-findings.md)）。
这个位置有三个问题：没有任何东西把密钥放进去；客户文档没说；工具包一升级目录就换、密钥就丢。
要定的是：**用户的密钥放在哪、用什么方式交给 IDE 上传用、密钥不对时用户看到什么**。

## 怎么算答完

定下密钥的位置和放置方式，写清它在工具包升级后是否还在；定下密钥不对时的报错文案。

## Answer

2026-09-25 定（用户按推荐）。

- **位置**：`%AppData%\openplc\keys\`（`os.UserConfigDir()/openplc/keys/`，和强制烧录的标记文件同一个父目录），不带版本号，工具包升级后还在。
  IAPTool 找密钥的顺序：`--key` → `local_config.json` 的 `signing_key` → **用户目录** → 工具包里的 `keys\`（今天已经这样放的机器照样能用）→ **随包带的公开根私钥**（兜底，每次用到都打一行警告）
- **怎么放进去**：找不到密钥时 IAPTool 报出应放的完整路径；客户文档写清
- **密钥不对时**：报「板子拒绝了重启请求，多半是 `<路径>` 这把密钥不是它信的那把，用 `IAPTool getowner <ip>` 查」，代替现在的 `No bootloader with UID found`

## 引出了什么新的未知

没有。
