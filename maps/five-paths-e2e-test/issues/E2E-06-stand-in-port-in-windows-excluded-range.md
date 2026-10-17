# 替身的 UDP 端口落进 Windows 排除段时，用例怎么报

Type: grilling
Opened: 2026-10-12
Status: resolved
Blocked by: -

## Question

2026-10-12 本机 `netsh int ipv4 show excludedportrange protocol=udp` 有 61780–61879，替身固定用的 61865（`$TEST/host/fakeboard/_common.py` 的 `TEST_PORT`）绑不上。替身日志报 `UDP bind 61865 failed`，用例却报「app 没启动」：`T1-38`（版本门）、`T2-05` `T2-09` `T2-36`（恢复出厂及之后）、`T2-19`（先后吊销两个叶证书）、`T1-22`（擦除窗口里掉电后恢复）。端口换成 60517 后这几条全过，所以和 IAP 改动无关。排除段由 winnat 动态保留，会变。

| 做法 | 代价 | 推荐 |
|---|---|---|
| A 换一个固定端口 | 改一行；排除段会变，哪天又撞上 | |
| B `resolve_port()` 先试绑 UDP / TCP，绑不上直接报端口被排除，并提示 `netsh` 命令 | 十来行；端口不变 | ✅ 失败时一眼看出是环境问题 |
| C B 之上绑不上就自动换空闲端口 | 要先核实 IAPTool 和替身的端口都只从 `resolve_port()` 取 | |

临时绕过：管理员 `net stop winnat` 再 `net start winnat`。

## 怎么算答完

用户选定一种并改完；`python tools/selfcheck.py` 上这几条过，或报出端口被排除。

## Answer

2026-10-12 定：B（用户：「其他问题和工作单开子窗口继续」，按推荐）。`resolve_port()` 先按替身的绑法（`0.0.0.0`，UDP 和 TCP）试绑 61865，绑不上就退出码 2 并点名端口和 `netsh` 命令，不再让用例误报「app 没启动」。

2026-10-12 改：C（用户：「如果替身端口被占用，那就选一些冷门端口」）。61865 绑不上时 `resolve_port()` 依次试几个 Windows 动态段（49152 起）以外的冷门端口，取第一个 UDP 和 TCP 都绑得上的，本次运行的替身和 IAPTool 都用它；全绑不上才退出码 2。

## 引出了什么新的未知

没有。
