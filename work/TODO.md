# 待办

**要做什么已经清楚，只是还没做。** 准入见 [../WHERE-THINGS-LIVE.md](../WHERE-THINGS-LIVE.md)：

> 每一条必须写明它是哪张已关的票产生的。写不出来的，写不进去。

做完且判据过了，**删掉那一行**，不要划掉留着。

| 待办 | 怎么算做完 | 来自哪张票 |
|---|---|---|
| 五个通信口做「异常可恢复」：上位机从帧里看出断了（`conn` 掉 0、`miss` 连增），自己计时到恢复 | 产测文档 3.10 的判定栏能填出「误码 / 恢复时间」，人只要动手拔线、不用回来汇报 | 同上（原 `ISS-D1`）。⚠️ 2026-09-16 起**等工装的使用反馈**再动 |
| 上位机面板左边按九个配置项分类分段 | 九类各自成段；**端口本身仍按板子分组**（Bridge / Upper / Lower / 整板），那条已定不要重开 | 同上（原 `ISS-D2`）。⚠️ 同样等反馈 |
| 每个端口逐个打通到真板子上过 | 每个端口在真板子上跑过一轮并记下结果 | 同上（原 PORT-BRINGUP-PLAN.md 整份，该文件已删） |
| 整轮收尾要还原被 `rotate_keys.sh` 改掉的仓库文件（路径 ③ 会重写 `$BOOT/IAPServer/keys/fw_pubkey.inc` 和 `fw_signing_key.TEST_ONLY.pem`） 。⚠️ **2026-09-21 核实：现在没有任何东西要还原** —— 仓库处在公开根状态（`check_public_root.py` 退出码 0，四仓工作树空）。**这是路径 ③ 跑过之后才成立的收尾步骤，不是现在欠着的账** | 跑 `rotate_keys.sh --restore <本轮快照>`，之后 `check_public_root.py` 退出码 0。⚠️ **还原必须在整轮结束之后，不是路径 ③ 之后** —— 路径 ④ 发叶证书要用那把轮换后的根私钥 | [路径三换根之后 `T2-06` 必然失败，算不算](../maps/five-paths-e2e-test/issues/E2E-05-is-t2-06-failing-after-rotate-expected.md) |
| ⚠️ **换根之后 `enter_bootloader.py` 会对预编译的 `iap_probe_*.bin` 失效**。**2026-09-21 复核：此刻五个镜像内置的都是当前公开根**（逐字节搜 `fw_pubkey.inc` 全部命中），所以现在是好用的 —— 当初记下的 `old-key present = True` 是在**换根窗口期**取的快照。这条描述的是**跑过路径 ③ 之后**的状态，板子未认领时用它们做重启握手会用**编译那一刻烧进去的根**去验证请求方证书，和 bootloader 当前信的根（可能已轮换）对不上，静默不响应。**这不是产品缺陷**——脚本自己的文档已经写着"另一条路是按 BOOT0，需要人在场"；只是说明"软件重启进 bootloader"这条路在换过根之后，对着旧镜像会失效，重新编译镜像或者按 BOOT0 是仅有的两条路 | 需要重编 `onboard/iap_probe/iap_probe.ino` 用当前 `fw_pubkey.inc`，或接受按 BOOT0 | [撤销叶证书 + bootloader 原地升级](../maps/owner-revoke-and-boot-upgrade/map.md) |

| **`flashboot`：bootloader 原地升级** —— 收镜像进 SDRAM、在 `RAM_D1` 里擦扇区 0、写回 bootloader + owner 记录，写回时压缩 | 真板子上原地换一次 bootloader，**所有权和已装的 app 都还在**；掉电后按 BOOT0 进 DFU 能救回来 | [擦扇区 0 的时候，那段代码从哪执行](../maps/owner-revoke-and-boot-upgrade/issues/OWN-02-where-does-the-erase-code-run.md)、[升级被打断之后，板子怎么让人知道](../maps/owner-revoke-and-boot-upgrade/issues/OWN-04-how-does-an-interrupted-upgrade-announce-itself.md)。实施清单在 [要改的东西，一条不落](../maps/owner-revoke-and-boot-upgrade/CHANGE-LIST.md) 的 A 节（bootloader：`flashboot` 命令、原地升级例程、journal 事件表）和 B 节（PC 工具：`flashboot` 子命令与 `RunFlashBoot()`） |
| **压缩 `'R'` 记录格式** —— 32 字节一条，owner 区切成 `'O'` 32 条 + `'R'` 96 条，`format_ver` **3 → 4** 硬切 | 真板子重新认领后，连续作废 96 个叶都生效；跨仓镜像（`P2`）和 `T1-16` 全绿 | 决策 58 / 59 + `I-D1`–`I-D3`。清单在 CHANGE-LIST 的 **I 节 13 项**，全部形状已定 |
| **`IAPTool setowner --wipe`：按需清空 owner 区** | 带 `--wipe` 那一次清空重写，不带的仍然只追加一条；剩 8 条时启动日志出提示 | [换根的时候把 owner 区清空重写](../maps/owner-revoke-and-boot-upgrade/issues/OWN-07-should-setowner-wipe-the-owner-area.md)。⚠️ **实施必然排在 `flashboot` 之后** —— 它要的 `RAM_D1` 擦写例程属于那半边 |
| **`RELEASE-NOTES.md` 改写**（英文） —— 现在写着「换 bootloader 要重传 app + 重新认领」，原地升级做出来之后那句过期 | 发版说明里的升级规则和板子实际行为一致；**v3 → v4 那一次会丢所有权，要单独说明** | 英文草稿已在 CHANGE-LIST 的 **H 节**，等 `flashboot` 和压缩落地后一并改 |


| ⚠️ **`run_takeown.py` 不带 `--key` 时，把新生成的 owner 私钥丢在系统临时目录**（`%TEMP%/takeown-<hex>/owner_key.pem`），而那是认领之后**这块板唯一能签固件的密钥** | 要么默认落到一个不会被清的位置，要么跑完在输出里把路径和后果说清楚（现在两样都没有） | 2026-09-20 跑 `T2-09` 时撞上：临时目录一清，板子就只能重烧 bootloader 才能再用 |

## 下次上板一起做

**攒着一次做，不要零散上板**（用户 2026-09-20：「一会上板后统一改和测试」）。
板子只有一块，每次上板都要重烧 / 重新认领，散着做等于把同一份代价付很多遍。

| 待验 | 怎么算做完 | 来自哪 |
|---|---|---|
| **`enter_bootloader.py` 对已认领的板子无效** —— 它调 `IAPTool ether` 时不传 `--key`，用默认公开根签的证书，板子正确拒绝并打印 `Rejected unauthenticated ...`，而脚本只报「board does not appear to be in the bootloader」 | 已认领的板子上跑它，要么能通（透传 `--key`），要么报错点名「这块板已认领，需要 --key」 | [有些叶证书驱动不了重启握手](../maps/owner-revoke-and-boot-upgrade/issues/OWN-08-some-leaf-certs-cannot-drive-the-reboot-handshake.md) 2026-09-21 第四轮 |
| **`Flash_If_Write()` 的 I-cache**：上板回归（烧写本身没被这次改动弄坏） | `T1-23` / `T1-24` 在真板子上各跑一轮 | 代码 `886b0ad`。⚠️ **「每条出口都重开 I-cache」那条已由 `P16` 静态证明**，比制造一次失败写入强 —— 上板只剩回归这一半 |
