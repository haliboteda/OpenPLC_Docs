# 面板跑第 6 步还缺哪几样输入

Type: grilling
Opened: 2026-10-11
Status: resolved
Blocked by: -

## Question

第 6 步的顺序已经有了，并且测过：烧 bootloader（擦扇区 0–14）→ 上传 demo → 测试 → 不论结果都恢复出厂（`$PORTTOOL/src/ptstages/`、`src/stlink/`，TODO-fixture 第 43 条）。面板上这一步仍然是灰的，因为下面几样还没定：

| 缺什么 | 要定的是 |
|---|---|
| bootloader 镜像 | 放在哪：随交付包放在 exe 旁边，还是每次由用户选 |
| IAPTool 上传和认领 | 调用哪个 IAPTool、用什么参数上传 demo、怎么认领产线的根（决策 93） |
| 产线根的密钥 | 放在哪台机器的什么位置、谁能拿到 |
| demo 和用户级测试的配置 | 等 TODO-fixture 第 47 条（demo 例程）和第 38 条（面板改版） |

## 怎么算答完

前三行各有一个定案，写进 STG-01 或决策表；面板能接上的部分列进 TODO-fixture。

## Answer

2026-10-11 用户定：**「需要我的现在问，不需要的按推荐开始」**，本票按推荐：bootloader 镜像随交付包放在 exe 旁边；上传和认领用交付包里的 IAPTool，按 Arduino IDE 上传的同一套参数；产线根用产线电脑上 IAPTool 的本机私钥（没有就生成，M2-ownership.md「用户第一次在 IDE 里上传」那条），板子出厂前恢复出厂，不带根；demo 和配置跟第 47、38 条走（决策 103）。

## 引出了什么新的未知

没有。
