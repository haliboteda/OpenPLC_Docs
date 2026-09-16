# 检查只读 .md 是个盲区

Type: grilling
Opened: 2026-09-16
Status: resolved
Blocked by: -

## Question

P8 和 P9 只扫 `.md`。这次发现文档路径同时写在 **43 个源文件**的注释里
（固件、core、Go、Python、`index.html`、连 `plans/*.json` 都有），**66 处，一条都没被任何检查看见**。

要定：P9 要不要连源码注释里的文档路径一起扫。

⚠️ 代价不是零：源码里出现 `docs/...` 的形态比 markdown 杂得多，
误报会让人学会忽略这条检查 —— 而 `check_doc_dupes.py` 自己的注释里就写着
「一条看起来在保护、其实没有的例外，比没有例外更糟」。

## 怎么算答完

改完之后，**把这次那 66 处退回去**（挑一份源文件改回旧路径），检查必须报它。
同时对现在这套干净的代码跑一遍，**零误报**。两条都过才算。

## Answer

2026-09-16 定。**P9 扩到源码注释**，但收得很窄。

`$TOOL/TestCase/tools/check_doc_paths.py` 加了两样：

| | |
|---|---|
| `sources()` | 收集四个仓里可能在注释里提到文档的源文件（`.c/.h/.cpp/.go/.py/.json/.html/.js/.txt/.cmd/.ps1`） |
| `SRC_PATH` | **只认带 `docs/` 且有扩展名的 token**。`$VAR/...` 那种另有规则管，所以 lookbehind 里排掉 `$` |

**为什么收这么窄**：票里自己写了代价 —— 源码里 `docs/...` 的形态比 markdown 杂得多，
**误报会让人学会忽略这条检查**。这句话本身就是 `check_doc_dupes.py` 注释里的原话：
「一条看起来在保护、其实没有的例外，比没有例外更糟。」

### 顺带抓出 4 处真断链

调这条规则时它立刻报了 8 个，其中 **4 个是今天搬迁漏掉的真错**
（我当时只修了 design / test / work 那三个子目录下的形态，没管直接挂在 docs/ 下的 STATUS.md 这种）：

| 在哪 | 错在哪 |
|---|---|
| `$TOOL/TestCase/tools/common.py` | 写的是 PROD/docs/STATUS.md —— 少了 tables/ 这一层 |
| `$TOOL/TestCase/tools/selfcheck.py` | `STATUS_DOC` 还指着 open_plc_cube_ide/docs/STATUS.md（已删的位置） |
| `$TOOL/TestCase/tools/run_s4.py` | 打印里写着 docs/STATUS.md（已删的位置） |
| `$BOOT/IAPServer/owner_slot.c` | 指着 `check-public-root.ps1` —— **`.ps1` 那批 2026-09-01 就归档了**，现在是 `check_public_root.py` |

另外 4 个是示意写法，改用了本来就有的 `path/to/` 约定（检查器认这个），不是给检查开后门。

### 验证

票的判据是两条，都要过：

**零误报** —— 对现在这套干净的代码：**99 份文档 + 1,220 个源文件、513 条引用，全部存在。**

**退回去必须报** —— 把 `$BOOT/IAPServer/owner_slot.h` 里一处改回搬迁前那个已经不存在的
design 目录下的 OWNERSHIP.md：

```
  open_plc_cube_ide\IAPServer\owner_slot.h:4  ->  <搬迁前那个旧路径>
  1 reference(s) name a file that does not exist     exit=1
```

**抓到了。** 恢复后重跑，513 条全部存在。

## 引出了什么新的未知

⚠️ **这条新检查自己就违反了刚刚定下的那条规矩。**

`sources()` 里那张「扫哪些子目录」的清单（`IAPServer` / `LWIP` / `Core/Src` / `TestCase` / `internal` / …）
**是我手写列出来的** —— 正是 [一张图怎么算「全做完」](FG-01-what-makes-a-map-done.md)
点名不许的那种做法：**手写清单会窄在写它的人的印象上**。

不在那几个子目录里的源文件，这条检查一个都看不见。**全集应该由命令算出来**，
而不是列出来。留作下一张票。
