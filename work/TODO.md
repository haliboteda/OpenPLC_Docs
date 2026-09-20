# 待办

**要做什么已经清楚，只是还没做。** 准入见 [../WHERE-THINGS-LIVE.md](../WHERE-THINGS-LIVE.md)：

> 每一条必须写明它是哪张已关的票产生的。写不出来的，写不进去。

做完且判据过了，**删掉那一行**，不要划掉留着。

| 待办 | 怎么算做完 | 来自哪张票 |
|---|---|---|
| 五个通信口做「异常可恢复」：上位机从帧里看出断了（`conn` 掉 0、`miss` 连增），自己计时到恢复 | 产测文档 3.10 的判定栏能填出「误码 / 恢复时间」，人只要动手拔线、不用回来汇报 | 同上（原 `ISS-D1`）。⚠️ 2026-09-16 起**等工装的使用反馈**再动 |
| 上位机面板左边按九个配置项分类分段 | 九类各自成段；**端口本身仍按板子分组**（Bridge / Upper / Lower / 整板），那条已定不要重开 | 同上（原 `ISS-D2`）。⚠️ 同样等反馈 |
| 每个端口逐个打通到真板子上过 | 每个端口在真板子上跑过一轮并记下结果 | 同上（原 PORT-BRINGUP-PLAN.md 整份，该文件已删） |
| **`T2-08`** 公开根告警是常驻的，不是一次性提示 | 连续复位 3 次，每次启动日志都有 `trusts the PUBLISHED root key`；脚本退出码反映结果 | [五条路径里「测安全性」各指什么](../maps/five-paths-e2e-test/issues/E2E-02-what-does-security-mean-per-path.md) |
| **`T2-09`** 认领会让板上原有的 app 失效 | 认领后复位，日志出现 `App signature invalid or absent`、停在 bootloader | [五条路径里「测安全性」各指什么](../maps/five-paths-e2e-test/issues/E2E-02-what-does-security-mean-per-path.md) |
| **`T2-10`** 换根后旧根签的固件装不进去 | 用公开根签的镜像上传被拒，且 app 区一字节未动 | [五条路径里「测安全性」各指什么](../maps/five-paths-e2e-test/issues/E2E-02-what-does-security-mean-per-path.md) |
| **`T2-11`** 真板子收下委托证书并据此执行固件 ⚠️ **今天是盲区** | 同事用叶私钥 + 根签发的证书上传成功，复位后正常启动。**退出码接上**，不留手工步骤 | [五条路径里「测安全性」各指什么](../maps/five-paths-e2e-test/issues/E2E-02-what-does-security-mean-per-path.md) |
| **`T2-12`** 换根后旧叶签的 app 下次启动被拒 ⚠️ **今天真板子零覆盖** | `setowner` 换根 → 复位 → `App signature invalid or absent` → 停在 bootloader | [五条路径里「测安全性」各指什么](../maps/five-paths-e2e-test/issues/E2E-02-what-does-security-mean-per-path.md) |
| **`T2-13`** 换根后旧叶再上传被拒 | 旧叶私钥 + 旧证书上传失败，且 app 区一字节未动 | [五条路径里「测安全性」各指什么](../maps/five-paths-e2e-test/issues/E2E-02-what-does-security-mean-per-path.md) |
| **`T2-14`** 新根签发的新叶能传能起 | 新叶上传成功 + 复位后正常启动。**这是 `T2-12`/`T2-13` 的正向对照，不可省** | [五条路径里「测安全性」各指什么](../maps/five-paths-e2e-test/issues/E2E-02-what-does-security-mean-per-path.md) |
| 把 `T2-08`–`T2-14` 登记进 [ID-MAP.md](../docs/tables/ID-MAP.md)，并写进 M2 的「测试怎么跑」表 | `check_status_sync.py`（`P7`）通过：每条被引用的用例都有定义，每条定义都被引用 | [五条路径里「测安全性」各指什么](../maps/five-paths-e2e-test/issues/E2E-02-what-does-security-mean-per-path.md) |
| ⚠️ **`Flash_If_Write()` 的两条错误返回路径漏了 `HAL_FLASH_Lock()` / `SCB_EnableICache()`**（`$BOOT/Core/Src/usbd_cdc_flash.c` 第 104、110 行；成功路径 116-117 行两个都调了） | 两条错误路径都恢复锁和 I-cache；**一次失败的写入之后 I-cache 仍是开的**（可用寄存器读回判真假） | [擦扇区 0 的时候，那段代码从哪执行](../maps/owner-revoke-and-boot-upgrade/issues/OWN-02-where-does-the-erase-code-run.md) |
| `Flash_If_Write()` 写后校验只比了 8 字节，而一次写的是 32 字节的 flash word（同文件第 104 行比 `uint64_t`） | 校验覆盖整个 32 字节 flash word | [擦扇区 0 的时候，那段代码从哪执行](../maps/owner-revoke-and-boot-upgrade/issues/OWN-02-where-does-the-erase-code-run.md) |
| 准备**两个可区分的镜像**当升级的 v1 / v2（五条路径每条都要「针对自己程序进行升级」） | 启动日志里的版本串从 A 变成 B，脚本能判真假。先确认 `Output/` 下现有的 `iap_probe_app.bin` / `iap_probe_altmac.bin` 能不能直接当 v1/v2，不能就各做一个 | [五条路径共用一块板，顺序怎么排](../maps/five-paths-e2e-test/issues/E2E-03-what-order-do-the-five-paths-run-in.md) |
| 整轮收尾要还原被 `rotate_keys.sh` 改掉的仓库文件（路径 ③ 会重写 `$BOOT/IAPServer/keys/fw_pubkey.inc` 和 `fw_signing_key.TEST_ONLY.pem`） | 跑 `rotate_keys.sh --restore <本轮快照>`，之后 `check_public_root.py` 退出码 0。⚠️ **还原必须在整轮结束之后，不是路径 ③ 之后** —— 路径 ④ 发叶证书要用那把轮换后的根私钥 | [路径三换根之后 `T2-06` 必然失败，算不算](../maps/five-paths-e2e-test/issues/E2E-05-is-t2-06-failing-after-rotate-expected.md) |
| ⚠️ **`enter_bootloader.py` 对预编译的 `iap_probe_*.bin` 无效**：核实过，这两个镜像编译时内置的是**轮换前的旧根**（`old-key present = True`，`today-key present = False`），板子未认领时用它们做重启握手会用**编译那一刻烧进去的根**去验证请求方证书，和 bootloader 当前信的根（可能已轮换）对不上，静默不响应。**这不是产品缺陷**——脚本自己的文档已经写着"另一条路是按 BOOT0，需要人在场"；只是说明"软件重启进 bootloader"这条路在换过根之后，对着旧镜像会失效，重新编译镜像或者按 BOOT0 是仅有的两条路 | 需要重编 `onboard/iap_probe/iap_probe.ino` 用当前 `fw_pubkey.inc`，或接受按 BOOT0 | [撤销叶证书 + bootloader 原地升级](../maps/owner-revoke-and-boot-upgrade/map.md) |
| ⚠️ **`R4`（当前生效的根永远撤不掉自己）实现了但零测试** | 一个能喂假 flash 记录区、跑**真实** `owner_root_ro.c` 的主机台子，喂一条点名当任根的撤销记录，判它被忽略而不是拒掉整条 | [撤销叶证书 + bootloader 原地升级](../maps/owner-revoke-and-boot-upgrade/CHANGE-LIST.md) 的 `G4`。⚠️ `T1-16` 的 owner 槽是桩，测不到这条 |
| ⚠️ **`IAPTool revoke` 把成功的撤销报成失败**（退出码 1）：`RunRevoke()` 回读 `getowner` 要求 generation 前进，但撤销记录**永不成为生效 owner 记录**，所以它不会变（`owner.go` `RunRevoke` 末段） | 撤销成功时退出码 0。⚠️ **回读凭据today 不存在** —— 板子没有任何 TCP 命令能报「撤过谁 / 撤了几个」，修法要先定（见 CHANGE-LIST 的 `D13`） | [撤销叶证书 + bootloader 原地升级](../maps/owner-revoke-and-boot-upgrade/CHANGE-LIST.md)，2026-09-20 真板子实测发现 |
| ⚠️ **一块板今天只能撤销一次** —— 第二次写得进去但不生效，且**每次失败烧掉一个不可回收的 owner 槽** | 能连续撤两个不同的叶且两个都生效，并有用例盯住它 | [第二次撤销写得进去但不生效](../maps/owner-revoke-and-boot-upgrade/issues/OWN-06-second-revocation-is-written-but-never-takes-effect.md)，2026-09-20 真板子实测发现 |
