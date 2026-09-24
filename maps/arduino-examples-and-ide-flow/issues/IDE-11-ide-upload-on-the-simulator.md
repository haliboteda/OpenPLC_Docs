# 模拟台上走通 IDE 烧录

Type: task
Opened: 2026-09-24
Status: resolved
Blocked by: IDE-02, IDE-04, IDE-13

## Question

补齐假板子，写一个脚本从 arduino-cli 发起：列端口 → 选中假板子 → upload 一个例程，未认领和已认领各一遍。

## 怎么算答完

脚本对两种板子状态都退出码 0；故意让假板子拒一次（错的密钥），脚本报红。并写清这条模拟测不到什么。假板子在「重启」期间必须真的静默，否则成功判据是空的；三个已知的坑见 [IDE-04-findings.md](../IDE-04-findings.md)。

## Answer

2026-09-25 做完，用例 `T1-34`（IDE 那条上传命令在假板子上走通），判据、跑法、测不到什么见 [M1-firmware-upgrade.md](../../../docs/modules/M1-firmware-upgrade.md) 的「测试怎么跑」节。
三种情况（未认领走公开根兜底、已认领用用户目录的密钥、密钥不对被拒重启）全部按预期；一遍约 4.5 分钟，所以手工跑，不进 selfcheck。

## 引出了什么新的未知

没有。
