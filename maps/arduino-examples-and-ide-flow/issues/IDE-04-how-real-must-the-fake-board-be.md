# 假板子要像到什么程度，arduino-cli 的 upload 才能走完

Type: research
Opened: 2026-09-24
Status: resolved
Blocked by: -

## Question

要在模拟台上走通「Tools → Port 里出现板子 → Upload」，假板子要回应哪些东西：网络发现、app 状态下的重启握手、bootloader 状态下的挑战和 `flash`、上传完成后的「重新上线」。现有 `$TOOL/TestCase/host/fakeboard/fake_board.py` 已经会哪些、缺哪些。

## 怎么算答完

列出 arduino-cli upload 一次在线上的完整往返（从 IAPTool 的代码里读出来，引代码行），逐条标出假板子已有 / 要补；并说明这条模拟**测不到**什么。

## Answer

2026-09-25 定。14 步的完整往返表（每步引代码行、标出假板子有没有）见 [IDE-04-findings.md](../IDE-04-findings.md)。

- **板子停在 bootloader 时，现有 `fake_board.py` 已经够**：`arduino-cli upload -l network` 实测退出码 0
- **板子在跑 app 时（IDE 的常见情况）要补约 25 行**：以 app 身份回应发现（带第五段版本号）、回应 UDP 重启挑战、重启后换成 bootloader 身份、收完镜像后静默几秒再以 app 身份回来。原型实测整条链路走通
- **同一台 PC 上发现得到假板子**，但地址是网卡自己的 IP，不是 `127.0.0.1`
- 测不到：板子侧的一切校验（签名、证书、nonce、撤销、CRC）、真的写 flash、复位时序、限流、丢包、多网卡、IDE 自己的界面

## 引出了什么新的未知

没有要定的。实现时要处理的三个坑写进 [模拟台上走通 IDE 烧录](IDE-11-ide-upload-on-the-simulator.md)：
arduino-cli 的发现超时默认 1 秒、而发现程序启动要 1.3 秒；失败的上传留下锁文件，之后发现沉默 90 秒；假板子在最后一个 `OK` 后 100 ms 内关连接会被判失败。
另外**假板子必须真的静默过一次**，否则「板子重新上线」这条成功判据什么都没证明。

