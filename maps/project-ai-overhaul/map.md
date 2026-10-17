# 项目 AI 改造

Status: paused
Paused because: 方案已记下，等用户看完再定怎么做（用户 2026-10-14）

## 怎么看进度（不用问任何人）

```
python tools/list_wayfinder_map_frontier.py --all
```

## Destination

交给用户的产品仓里没有任何 Claude 相关文件，也不在 `.gitignore` 里留痕迹；这些文件全部进一个私有仓，换电脑后 clone 再跑一条命令就能恢复原样。

## Notes

- **用户 2026-10-14**：产品仓要提供给用户，不给用户 Claude 的东西；不想放进 `.gitignore`；换电脑时 Claude 的东西要能同步过去
- **用户 2026-10-14**：继续用自己维护的 board 包，不改成 library 方式；core 留在 STM32duino 2.4.0，需要的上游修复单条摘（与本图无关，只是同一次讨论）

## 方案

### 结构

```
E:\WorkSpace\Schaeffer-AG\
├── OpenPLC_AI\                       ← 新建私有仓（暂名）
│   ├── .gitignore                    ← */settings.local.json*（本机专属，不进 git）
│   ├── link.py                       ← 换电脑后跑一次
│   ├── workspace\                    ← 工作区根目录的 CLAUDE.md、settings.json、rules\
│   ├── memory\                       ← Claude 的记忆文件
│   └── <产品仓名>\                    ← 每个产品仓一个目录：CLAUDE.md、settings.json
│
├── .claude\  ══junction══▶  OpenPLC_AI\workspace\
├── <产品仓>\
│   ├── .claude\  ══junction══▶  ..\OpenPLC_AI\<产品仓名>\
│   └── .git\info\exclude             ← 一行 .claude/，只在本机，不进提交
└── …
```

### 为什么是这几样

| 选择 | 一句话理由 |
|---|---|
| `CLAUDE.md` 挪进 `.claude/` | 每个仓只链一个目录，不用给单个文件建链接 |
| 用 junction，不用符号链接 | 不需要开发者模式、不需要管理员权限 |
| 用 `.git/info/exclude`，不用 `.gitignore` | 效果相同，但不进提交，用户看不见 |
| 不用硬链接 | 编辑器「写临时文件再改名」式保存会让链接悄悄断开 |

### 每个产品仓改造一次

| 步 | 做什么 |
|---|---|
| 1 | `CLAUDE.md`、`.claude/settings.json` 搬进 `OpenPLC_AI/<仓名>/` |
| 2 | `git rm --cached CLAUDE.md .claude/settings.json` 后提交 —— 已跟踪的文件忽略规则管不到，必须先取消跟踪 |
| 3 | `.git/info/exclude` 加 `.claude/` |
| 4 | `.claude` 换成指向私有仓的 junction |

`git rm --cached` 只影响之后的提交，**历史里仍有这些文件**；要清历史得用 `git filter-repo` 改写并强推，所有提交号都会变、所有旧克隆作废。

### 新电脑恢复

| 步 | 做什么 |
|---|---|
| 1 | 按原目录结构 clone 各产品仓 |
| 2 | clone `OpenPLC_AI` |
| 3 | `python OpenPLC_AI/link.py`：建全部 junction、写各仓的 `exclude`（已有则跳过） |
| 4 | `OpenPLC_Test/tools/init_machine.py` 生成本机的 `settings.local.json` |
| 5 | 每个仓用交互模式开一次 Claude，接受信任 —— 不接受的话 settings 里的 allow 规则不生效 |

`~/.claude/rules/` 仍按原有方式：clone `AI-Skills`，跑 `_shared/sync_rules.py`。

### 已验证（2026-10-14，在 `Hardware` 仓临时试装后已恢复原样）

| 项 | 结果 |
|---|---|
| 开发者模式关闭时建 junction | ✅ 成功，不要管理员权限 |
| Claude 经 junction 读 `.claude/CLAUDE.md` | ✅ 新会话报告的加载路径是 `Hardware\.claude\CLAUDE.md` |
| Claude 经 junction 读 `settings.json` / `settings.local.json` | ✅ |
| 工作区根目录 `CLAUDE.md` 照常加载 | ✅ |
| git 穿过 junction 看到已跟踪文件 | ⚠️ 是，所以要先做改造步骤 2 |
| `CLAUDE.md` 里的 HTML 注释 | Claude 看不到，写给 AI 的内容不能放在注释里 |

### 要跟着改的

| 位置 | 原因 |
|---|---|
| `OpenPLC_Test/tools/` 的 `init_machine.py`、`check_allow_hygiene.py`、`common.py`、`test_init_machine.py` | 读写各仓的 `.claude/` 或 `CLAUDE.md` |
| `OpenPLC_Docs/tools/` 的 `check_doc_paths.py`、`check_doc_dupes.py` | 同上 |
| 文档里指向各仓 `CLAUDE.md` 的链接 | 文件移走后 P9 会报断链 |
| 根目录 `settings.json` / `settings.local.json` 里的 `cd IAPTranfer_Tool/TestCase && …` | 脚本已按决策 78 搬到 `OpenPLC_Test`，这些规则已匹配不到任何命令 |

## 全集

在工作区根目录跑（bash）。按「Claude 相关文件，以及读写它们的工具」找：

```
for r in */; do r=${r%/}; [ -d "$r/.git" ] || continue; git -C "$r" ls-files | grep -E '(^|/)(CLAUDE\.md|\.claude/)' | sed "s#^#$r/#"; done
ls -d CLAUDE.md .claude/* .claude/rules/* 2>/dev/null
grep -rlE '\.claude|CLAUDE\.md' --include=*.py */tools 2>/dev/null
```

2026-10-14：已跟踪的 14 个（7 个仓各有 `CLAUDE.md` + `.claude/settings.json`，`OpenPLC_Docs`、`package_index_json` 只有 `CLAUDE.md`），工作区根目录 4 个（不在任何 git 里），读写它们的工具 6 个。

⚠️ 这条命令抓不到 `OpenPLC_Docs/docs/agents/` 这类写给 AI 的文档，见下面「Not yet specified」。

## Decisions so far

（还没有）

## Not yet specified

- **用户拿到的是 git 仓库还是打包文件**：决定要不要用 `git filter-repo` 清历史
- **私有仓叫什么、放在哪**：`OpenPLC_AI` 是暂名；也可以并进已有的 `AI-Skills`
- **`settings.local.json` 怎么拆**：本机路径（`additionalDirectories`）留本机；`git commit` / `git push` / 上板脚本这类与机器无关的 allow 规则要不要挪进 `settings.json`
- **记忆目录用 junction 还是改 `autoMemoryDirectory`**：后者能省一个链接，但是否支持相对路径没验证
- **`OpenPLC_Docs` 和 `package_index_json` 是否交给用户**：不交的话这两个仓的 `CLAUDE.md`、`docs/agents/` 可以不动

## Out of scope

- `~/.claude/rules/`：已由 `AI-Skills/_shared/sync_rules.py` 同步
- 历史对话记录（`~/.claude/projects/E--WorkSpace-…`）：只属于本机
- 不属于本产品的目录（`Arduino_Examples`、`arduino_test`、`KNX_Project_China`、`KNX_USB_Tool`、`ref/`）
