# 模拟台上走通 IDE 烧录

Type: task
Opened: 2026-09-24
Status: open
Blocked by: IDE-02, IDE-04

## Question

补齐假板子，写一个脚本从 arduino-cli 发起：列端口 → 选中假板子 → upload 一个例程，未认领和已认领各一遍。

## 怎么算答完

脚本对两种板子状态都退出码 0；故意让假板子拒一次（错的密钥），脚本报红。并写清这条模拟测不到什么。
