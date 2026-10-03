# 文件怎么经 RS232 传到板子上写进 SD 卡

Type: grilling
Opened: 2026-09-29
Status: resolved
Blocked by: EXB-01

## Question

用户要的 SD 例程：PC 经 RS232 把一个文件传给板子，板子写进 SD 卡；拔卡、插卡都打日志。传输用什么格式（现成协议如 XMODEM，还是长度 + CRC 的自定格式）；PC 侧用什么发；是替换 SD_ReadWrite 还是新增；怎么判文件写对了（读回比对）；插拔靠什么检测。

## 怎么算答完

定下传输格式、PC 侧工具、例程去留、写对的判据、插拔检测方式和日志文案。

## Answer

2026-10-03 定（用户：都按推荐）：

| 问题 | 定了什么 | 一句理由 |
|---|---|---|
| 传输格式 | **YMODEM**（首包带文件名和精确长度，1 KB 包，CRC16，丢包重传）；接收端是 `OpenPLC_Ports` 里的一个模块，主机单元测试 `T3-10` | XMODEM 不带名字、末包补 `0x1A` 保不住长度；自定格式用户没有现成工具发 |
| PC 侧 | 用户用 Tera Term（文件 → 传输 → YMODEM → 发送）或 lrzsz 的 `sb`；测试脚本在 `$TEST` 里自带 Python 发送端 | 用户不必装 Python |
| 例程 | **新增** `SD_FileReceive`，`SD_ReadWrite` 保留 | 最简单的读写示范还要在 |
| 写对的判据 | 写完关文件，从卡上读回算 CRC32，USB 串口打 `SD: wrote NAME, N bytes, crc32=XXXXXXXX`；PC 拿原文件算一遍比对 | YMODEM 每包校验证明不了卡上的内容 |
| 插拔和日志 | 每 50 ms 读卡检测脚 PE6（低 = 插着），连续两次一样才算数；插入时重新 `SD.begin()`；打 `SD: card inserted` / `SD: card removed`。**日志全走 USB 串口，RS232 只走 YMODEM**；文件头写明传文件时不接网线最稳 | 板卡包拿到 IP 时会在 RS232 上打一行 `[NET]`（`cores/arduino/main.cpp`），YMODEM 发送端当噪声重传 |

## 引出了什么新的未知

无。
