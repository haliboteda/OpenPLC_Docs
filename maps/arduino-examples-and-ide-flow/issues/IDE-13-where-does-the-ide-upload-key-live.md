# IDE 上传用的密钥放在哪、怎么放进去

Type: grilling
Opened: 2026-09-24
Status: open
Blocked by: IDE-01

## Question

IDE 上传时 IAPTool 到板卡包的 `STM32Tools\<版本>\win\keys\` 找密钥（见 [IDE-02-findings.md](../IDE-02-findings.md)）。
这个位置有三个问题：没有任何东西把密钥放进去；客户文档没说；工具包一升级目录就换、密钥就丢。
要定的是：**用户的密钥放在哪、用什么方式交给 IDE 上传用、密钥不对时用户看到什么**。

## 怎么算答完

定下密钥的位置和放置方式，写清它在工具包升级后是否还在；定下密钥不对时的报错文案。
