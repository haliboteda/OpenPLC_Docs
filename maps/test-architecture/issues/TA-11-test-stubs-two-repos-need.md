# 两个仓都要用的测试桩怎么办

Type: grilling
Opened: 2026-10-02
Status: resolved
Blocked by: -

## Question

`host/owner_revoke/stubs/iap_keyderive_stub.c` 现在被三组主机 C 测试共用：`owner_revoke` 搬去板卡包仓，`owner_capacity` 和 `sector15_reclaim` 搬去 `$BOOT`，于是两个仓都要它。决策 76（仓与仓彻底分离）要求各管各的，决策 77（同一功能只留一份）要求不重复：这类测试桩是两边各放一份并接受重复、加一道比对，还是别的办法。

## 怎么算答完

给出规则，并按规则写出 `iap_keyderive_stub.c` 的去处；归属表里如果还有别的同类文件，一并落位。

## Answer

2026-10-02 定（用户按推荐定，九件一次定完）。两个仓各放一份 `iap_keyderive_stub.c`，不做比对。规则：测试桩替的是本仓的代码，就归本仓，可以重复；决策 77 管产品代码，不管这种桩。bootloader 和板卡包各有自己的 `iap_keyderive.c`，桩替的是各自那份。

## 引出了什么新的未知

没有。
