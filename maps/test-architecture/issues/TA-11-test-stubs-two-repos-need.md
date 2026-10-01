# 两个仓都要用的测试桩怎么办

Type: grilling
Opened: 2026-10-02
Status: open
Blocked by: -

## Question

`host/owner_revoke/stubs/iap_keyderive_stub.c` 现在被三组主机 C 测试共用：`owner_revoke` 搬去板卡包仓，`owner_capacity` 和 `sector15_reclaim` 搬去 `$BOOT`，于是两个仓都要它。决策 76（仓与仓彻底分离）要求各管各的，决策 77（同一功能只留一份）要求不重复：这类测试桩是两边各放一份并接受重复、加一道比对，还是别的办法。

## 怎么算答完

给出规则，并按规则写出 `iap_keyderive_stub.c` 的去处；归属表里如果还有别的同类文件，一并落位。
