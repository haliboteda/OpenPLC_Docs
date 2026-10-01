# 依赖固件源码的 PortTool 测试归哪

Type: grilling
Opened: 2026-10-02
Status: open
Blocked by: -

## Question

PortTool 的 T4-01（协议契约）、T4-02 / T4-03（面板在浏览器里点一遍，对端是模拟板）、校准值区核对，都要编 `$BOOT` 里的工装固件源码 `TestCase/porttool/`。按决策 78 的判据它们要两个仓，归 `$TEST` 契约层；但工装固件和 PortTool 是同一个工装的两半，模拟板也是 PortTool 日常开发离不开的。是照判据搬去 `$TEST`，还是把「工装固件源码」算作 PortTool 的一部分、让这几项留在 `$PORTTOOL`，或者别的分法。

## 怎么算答完

T4-01、T4-02、T4-03、校准值区核对、模拟板各有唯一去处；如果不照判据走，把例外写进决策 78 并说明理由。
