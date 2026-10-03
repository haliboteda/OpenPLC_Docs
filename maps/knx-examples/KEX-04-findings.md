# 测试脚本能不能经 IP 网关直接收发组报文 —— 现场发现

票：[测试脚本能不能经 IP 网关直接收发组报文](issues/KEX-04-can-the-script-talk-through-the-ip-gateway.md)。2026-10-03 第一轮，**票未答完**：这台 PC 当时没接在网关的网段上。

## 网关（出处：ETS 历史日志 `%LOCALAPPDATA%\KNX\ETS5\Log\ETS5.log`，不是现场探测）

| 字段 | 值 |
|---|---|
| 名称 | `HDL KNXnet/IP Device`（厂商号 0x0073 = HDL） |
| IP | 10.32.2.129:3671；ETS 当时用的本机地址 10.32.2.199 |
| 物理地址 | 1.1.4 |
| 隧道 | 用过：LinkLayer 和 Busmonitor 两种模式，最后一次 2026-07-06 |
| 服务族版本、隧道连接数 | **没拿到**，要现场发 DESCRIPTION_REQUEST |

## 2026-10-03 现场

| 做了什么 | 结果 |
|---|---|
| 4 个本机接口各发组播 SEARCH_REQUEST；单播 DESCRIPTION_REQUEST 到 10.32.2.129 | 都没有响应：PC 只有 WLAN 192.168.1.3/24 通，有线网卡断开 |
| 往总线发报文 | 一个没发 |

## 已定的

- 测试脚本用 **xknx**（本机 `pip install` 3.20.0 成功）：用例要读物理地址这类设备管理操作，xknx 已经带了，还管隧道的序号、重发和心跳

## 还要做

PC 有线口接回 10.32.2.x 后重跑：搜到网关、经隧道往 31/7/255 发一个 0 并收到确认、试第二条并行隧道。探测脚本在本会话的 scratchpad（`kex04/probe_xknx.py`），答票时搬进 `$TEST/tools/`。
