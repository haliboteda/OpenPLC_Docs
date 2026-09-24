# 一个例程长什么样

Type: prototype
Opened: 2026-09-24
Status: resolved
Blocked by: -

## Question

定下所有端口例程共用的格式：文件头写什么（接线、要准备什么）、用哪个串口输出、输出写什么、代码写到多短。先拿 DO 写一个原型给用户看。

## 怎么算答完

用户看过 DO 原型并确认格式；格式写进 `OpenPLC_Ports` 的 README，后面的例程照它写。

## Answer

2026-09-25 定（用户按推荐）。

**照 [DO 原型](../IDE-05-prototype/DO_Outputs/DO_Outputs.ino)：**

- 文件头四段：做什么 / 接什么线 / 该看到什么 / 串口监视器（板子的 USB 口，115200）
- 第一行代码是 `OPENPLC_APP_VERSION(1, 0, 0);`，其余越短越好
- 串口输出用英文（程序输出一律英文）
- 需要额外装库的，文件头第一行写明先装什么

格式写进 `OpenPLC_Ports` 的 README，后面的例程照它写。

## 引出了什么新的未知

没有。
