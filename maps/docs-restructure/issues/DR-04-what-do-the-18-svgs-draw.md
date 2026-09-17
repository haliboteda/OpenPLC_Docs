# 那 18 张 SVG 图各画的是什么

Type: research
Opened: 2026-09-17
Status: resolved
Blocked by: -

## Question

`docs/modules/M2-ownership.md`（148 KB）里有 **18 张手写 SVG 图**，
结构是 5 条流程（A 一次上传 · B 认领 · C 发证书 · D 换根 · E 恢复出厂）、
12 份参考、1 份诊断表。

这些图要转成 Mermaid 拆进模块文档，但**转之前得先知道每张画的是什么**：

- 逐张列出：画的是什么、属于哪个模块（M1 还是 M2 为主）、
  Mermaid 的哪种图型放得下（flowchart / sequence / state / 表格）
- 哪几张**转不了** —— 手写 SVG 能做的排版 Mermaid 未必做得到，
  转不了的要当场说出来，不要硬转成一张读不懂的图
- 哪几张的内容**已经和 `OWNERSHIP.md` 的文字分叉了** ——
  那份文档自己写着「和本文打架时以本文为准」，等于预设了会打架，
  **但从来没有人核对过到底打没打架**。这是这张票最值钱的产出
- 转完之后 `docs/security/` 那三份 markdown（OWNERSHIP / CHALLENGE-AUTH / KEYS）
  还剩多少内容、够不够独立成文

⚠️ **只调查，不动手转。** 转图属于后面的执行，这张票只负责把 18 张摸清楚。

## 怎么算答完

产出一份清单：18 张图逐张写明「画什么 / 归哪个模块 / 用哪种 Mermaid 图型 / 能不能转」，
并且明确列出**和 markdown 文字对不上的地方**（一条都没有也要明写「没有」）。

## Answer

2026-09-17 定。完整清单在 [../DR-04-findings.md](../DR-04-findings.md)（21 KB），下面只记结论。

**先纠一个数：不是 18 张 SVG，是 17 张 SVG + 2 张 HTML 表，共 19 件。**
票里的「18」漏数了开头那张场景索引表（8 个用户处境 → 该看哪张图）。
那张表是唯一按「用户处境」组织的东西，**模块化之后没有任何模块文档会天然长出它**。

**五件转不了**，理由逐条写在 findings 里：参考 2 所有权生命周期（viewBox 高 3190，
是一篇带状态骨架的文章不是图）、参考 6 flash 布局（按比例的地址条，Mermaid 没有内存布局图型，
硬转会丢掉「bootloader 代码和 owner 区同属扇区 0」这个相邻关系 —— 那是选址的全部理由）、
参考 7 字节级格式、参考 9 nonce（SVG 里 0 条边，没有流程关系）、参考 10 BOOT0 时间轴。
最适合 Mermaid 的是参考 5 启动决策链（flowchart TD，几乎无损）和 5 条流程（sequenceDiagram + alt）。

**图和文字确实打架了，五处**，全部回 `$BOOT/IAPServer/` 源码核实，不是拿抄件对抄件：

| 分歧 | 谁对 |
|---|---|
| `OWNERSHIP.md` 的记录格式表写「**最大 generation 的那条有效记录获胜**」 | **图对，md 错。** `owner_slot.c:121` 原文 `never "highest generation wins". That shortcut would be a hole`。而且同一份 md 的状态机 ASCII 写的是「沿链取最后一条有效的」—— **文档内部自相矛盾** |
| `OWNERSHIP.md` 说自签证书「纯粹是 **160 字节** + 一次验签」 | **图对，md 错。** `iap_cert.h:34` `IAP_CERT_SIZE 132U` 带 `_Static_assert`；160 是 `OWNER_RECORD_SIZE`，抄串了相邻章节 |
| 参考 7 底部红字指责「`JOURNAL.md` 里 M 记录还写着 4 格」 | **图自己过期了。** 实测 `docs/modules/M1/JOURNAL.md` 五处全是 8 格。转图时这条要删，抄过去等于凭空造一条假缺陷 |
| 参考 8 写「链在**中途**断了 ⇒ 回落」 | **md 对，图错。** 代码只在 `s_effective == NULL` 或链尾 cleared 时回落 |
| 换 owner 的代数举例，md 用 G2→G3、图用 G1→G2→G3 | 都不错，并排读会误导。统一成 G(n+1) 被 G(n) 签 |

另有一条措辞层面的：md 说「64 字节的哈希比对」，实际是对 64 字节公钥算 SHA-256 再比 32 字节摘要。
**核对过、确认没有分歧的 13 项**也明写在 findings 里。

**比分歧更要紧的是缺口：10 条事实只活在这份 HTML 里**，逐条 grep 过三份 md（部分 grep 过整个 `docs/`）
确认别处没有 —— nonce TTL 30 秒、全局单 nonce 的并发冲突是可用性怪癖不是安全洞、
签名消息的确切字节、BOOT0 的 30 秒卡键上限、`owner_slot_factory_reset()` 必须排在 `server_decide()` 之前、
交接记录在 SRAM4 `0x38000000` 魔数 `"PLC!"` 及「为什么不用 RTC」、SDRAM 暂存区刻意不在链接脚本
MEMORY 块里、`meta.sha256` 写了没人读、启动验签失败只记一连串里的第一次、
0.1.2 工具刷 0.1.3 板「失败得很安静」。**HTML 一删这些就没了。**

**转完之后三份 markdown 的去向**：`OWNERSHIP.md`（292 行）几乎全留，**它就是 M2 归属与信任文档的主体**
—— 图是它的摘要版，不是反过来；`CHALLENGE-AUTH.md`（89 行）**现在不够**独立成文，
缺 TTL / 全局单 nonce / 签名消息三条，补完才够；`KEYS.md`（23 行）一行不动，
但太小撑不起独立文档，去处留给「docs 下 32 份文件逐份定去处」那张票。

**一句话**：转图的工作量大头**不是画 Mermaid，是去重** —— 真正只存在于图里的事实只有 10 条，
其余都是已有 markdown 的图形化重述。19 件合并后预计只剩 8–10 张 Mermaid + 6–7 张 markdown 表。

## 引出了什么新的未知

1. **那张「场景索引表」在新体系里住哪。** 它按用户处境组织（「我的板子起不来」→ 看哪张图），
   横跨 M1 和 M2，**任何一个模块文档都容不下它**。这是模块化这个划分标准的第一个真实反例 ——
   已记进地图的 `## Not yet specified`
2. **转图之前要先修 `OWNERSHIP.md` 的两处实际错误**，否则错会被复制进模块文档。
   已进 `work/TODO.md`
3. **10 条只活在 HTML 里的事实要先抢救再删 HTML。** 已进 `work/TODO.md`
