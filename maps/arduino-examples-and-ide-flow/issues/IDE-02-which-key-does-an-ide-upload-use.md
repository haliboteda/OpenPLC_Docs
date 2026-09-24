# IDE 上传时用哪把密钥，已认领的板子要用户准备什么

Type: research
Opened: 2026-09-24
Status: resolved
Blocked by: -

## Question

Arduino IDE 点 Upload 时，板卡包里的 IAPTool 用哪把私钥签名、到哪里找它和它的证书；未认领和已认领的板子，用户各要事先做什么。

## 怎么算答完

给出 IAPTool 找密钥的实际顺序（引代码行）；两种板子状态下用户要准备的文件和放置位置；以及今天这条路上已知跑不通的地方（没有就写没有）。

## Answer

2026-09-24 定。详细结论和代码出处见 [IDE-02-findings.md](../IDE-02-findings.md)。

- **IDE 不传任何密钥参数**（`platform.txt:239`、`:249`）。IAPTool 依次找：`--key` → exe 旁 `local_config.json` 的 `signing_key` → **exe 旁 `keys\fw_signing_key.pem`**；证书是同名加 `.cert`，没有就自签
- 三种情况要放的文件：未认领 → 公开根私钥；已认领、自己持 owner 私钥 → owner 私钥；同事 → 自己的私钥加管理员发的 `.cert`。**都放在板卡包的 `STM32Tools\<版本>\win\keys\` 下**
- app 在跑时的网口重启用同一把密钥和证书，和 bootloader 判定一致；USB 路径靠 1200 波特率触发，不签名

## 引出了什么新的未知

- **密钥住在哪、谁放进去** —— 今天没有任何东西把密钥放进 `keys\`，客户文档也没说位置；而且这个目录带工具包版本号，升级就丢。开成新票 [IDE 上传用的密钥放在哪、怎么放进去](IDE-13-where-does-the-ide-upload-key-live.md)
- **Board Manager 上的工具包 0.1.2 里的 IAPTool 不会签名**（2026-03-25 的旧版，这台机器是手工拷过去的）—— 归 [一个发布版今天是怎么到 Board Manager 的](IDE-01-how-does-a-release-reach-board-manager.md)
- 密钥不对时 app 拒绝重启，工具只报 `No bootloader with UID found` —— 并进新票一起定

