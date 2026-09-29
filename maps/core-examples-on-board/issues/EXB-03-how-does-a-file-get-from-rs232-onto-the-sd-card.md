# 文件怎么经 RS232 传到板子上写进 SD 卡

Type: grilling
Opened: 2026-09-29
Status: open
Blocked by: EXB-01

## Question

用户要的 SD 例程：PC 经 RS232 把一个文件传给板子，板子写进 SD 卡；拔卡、插卡都打日志。传输用什么格式（现成协议如 XMODEM，还是长度 + CRC 的自定格式）；PC 侧用什么发；是替换 SD_ReadWrite 还是新增；怎么判文件写对了（读回比对）；插拔靠什么检测。

## 怎么算答完

定下传输格式、PC 侧工具、例程去留、写对的判据、插拔检测方式和日志文案。
