# 一个发布版今天是怎么到 Board Manager 的

Type: research
Opened: 2026-09-24
Status: resolved
Blocked by: -

## Question

从改完板卡包代码，到客户在 Board Manager 里能装到新版本，中间每一步是什么：打哪个仓的 tag、哪个 release 放 IAPTool、索引 JSON 里的校验和和大小谁来算、网络发现程序怎么进包、哪些步骤今天是手工的。

## 怎么算答完

列出每一步：在哪个仓、用什么命令或手工动作、**哪一步是对外动作**；并指出现有索引里 0.1.3-pre 是否真的能装（下载地址、校验和对得上）。

## Answer

2026-09-24 定。每一步、各在哪个仓、哪一步对外，见 [IDE-01-findings.md](../IDE-01-findings.md)。

- **发版今天全靠手工**，没有脚本也没有文档；发版验收单 `CHK-B1`–`CHK-B9` 不查索引和 release
- 链路：板卡包 zip 由 GitHub 按 `open_plc_arduino` 的 tag 自动生成；IAPTool 手工提交进 `Arduino_Tools` 再打 tag、上传 `STM32Tools.tar.gz`；网络发现程序手工编好提交进 git，随 zip 出去；索引 JSON 的校验和与大小手算，作为 `package_index_json` 的 release 附件上传。**对外动作共 6 步**
- **现在网上那个 `0.1.3-pre` 能装，但装上的东西是旧的**：tag 指向 2026-04-23 的提交，比当前分支落后 33 个 commit，没有网络发现程序；工具包里的 IAPTool 是 2026-03-25 的，不会签名，也没有 `takeown` / `setowner`
- **本机测的不是客户拿到的那份**：本机的工具包已被 `install_tool.py` 换成新版，`P11` 比的也是本机这份

## 引出了什么新的未知

发 `0.1.3` 时要定的命名和顺序，合成新票 [0.1.3 怎么命名、按什么顺序发](IDE-14-how-is-0-1-3-named-and-released.md)：
同名的分支已经存在（打 tag 会撞名）、工具包要不要升版本号、客户该填哪个索引地址、12 个没推上去的 commit。

