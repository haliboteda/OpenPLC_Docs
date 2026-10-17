# 对着正在跑 app 的 IP 发 getowner 这类查询，IAPTool 怎么办

Type: grilling
Opened: 2026-10-12
Status: resolved
Blocked by: -

## Question

`getowner` `getapprevoked` 走 TCP 56865，只有 bootloader 答；运行中的 app 只答 UDP（[IAP-PROTOCOL.md](../../../docs/modules/M1/IAP-PROTOCOL.md)「UDP」），所以对着 app 的 IP 查会报连接被拒。2026-10-12 已在 `$TOOL/owner.go` 的报错里加了提示「板子在 bootloader 吗？运行中的 sketch 不答这条命令」。

| 做法 | 代价 | 推荐 |
|---|---|---|
| A 保持现状：只把报错说清楚 | 用户要自己先让板子进 bootloader | ✅ 查询命令不带重启的副作用 |
| B IAPTool 查询前先发网口重启，把板子送进 bootloader 再查 | 一条查询会让正在跑的 app 停下 | |

## 怎么算答完

用户选定一种。

## Answer

2026-10-12 定：A，只把报错说清楚（用户：「其他的可以按推荐并行开始」）。查询命令不带重启的副作用。

## 引出了什么新的未知

无。
