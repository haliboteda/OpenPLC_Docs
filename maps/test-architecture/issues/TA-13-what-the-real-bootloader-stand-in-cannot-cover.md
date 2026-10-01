# 真 bootloader 替身覆盖不到的几例怎么办

Type: grilling
Opened: 2026-10-02
Status: resolved
Blocked by: -

## Question

假板子换成真 bootloader 代码编的替身之后（见「IAPTool 测试用的假板子：换成真 bootloader 代码，还是留着手写」），有三件事真代码给不了：T1-18c（老 bootloader 答 `Unknown command`，IAPTool 照走）现行代码造不出来；T1-34 ②③（IDE 上传给正在跑 app 的板子）的重启握手在板卡包的 `OpenPLC_IAP/src/udp_server.c`，不在 bootloader 里；`$BOOT/IAPServer/IAP_server.c` 的 `jump_to_app` 是 ARM 汇编，PC 上编不过，要在 `$BOOT` 改一处。三件各怎么处理。

## 怎么算答完

T1-18c 留或删；T1-34 ②③ 的 app 一侧用什么替身、住哪个仓；`jump_to_app` 用什么办法让主机编得过（先例是 `bootloader_state.c` 的 `BOOTLOADER_STATE_HOST_TEST`）。

## Answer

2026-10-02 定（用户按推荐定，九件一次定完）。T1-18c 留：在真代码替身外面拦下 `getpubkey` 回 `Unknown command`；打过标签的 v0.1.0–v0.1.2 bootloader 都没有 `getpubkey`（它 2026-08-15 才加），外面可能还有这种板子。T1-34 ②③：把板卡包 `OpenPLC_IAP/src/udp_server.c`（app 一侧的重启握手）也编进同一个替身，T1-34 本来就在 `$TEST`。`jump_to_app`：在 `$BOOT` 加主机测试开关，照 `bootloader_state.c` 的 `BOOTLOADER_STATE_HOST_TEST`。

## 引出了什么新的未知

没有。
