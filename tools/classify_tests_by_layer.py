"""Sorts every file in the test-architecture map's full set into a layer and a repo.

Rewrites maps/test-architecture/TA-01-inventory.md. Rerun it before moving
anything: the full set changes as files are added. The rules are decision 78's
(how many repos a file needs to run); see that map.

    python tools/classify_tests_by_layer.py

Exit 0 = every file matched a rule, 1 = some did not (they are listed).
"""
import os
import re
import subprocess
import sys
from collections import OrderedDict
from pathlib import Path

# The product repos sit beside this one.
WS = Path(__file__).resolve().parents[2]
OUT = WS / "OpenPLC_Docs" / "maps" / "test-architecture" / "TA-01-inventory.md"
PAT = re.compile(r"(^|/)(TestCase|tests?|host|onboard)/|_test\.(go|c|py)$|(^|/)(check_|run_|selfcheck)[^/]*\.py$", re.I)
REPOS = ("IAPTranfer_Tool", "OpenPLC_PortsTestingTool", "open_plc_cube_ide", "open_plc_arduino", "OpenPLC_Docs", "OpenPLC_Test")

files = []
for r in REPOS:
    if not (WS / r).is_dir():
        continue
    # Tracked plus not-yet-committed (but not ignored): a move is checked before
    # its commit, and OpenPLC_Test holds nothing but tests, so all of it counts.
    out = subprocess.run(["git", "-C", str(WS / r), "ls-files", "-co", "--exclude-standard"],
                         capture_output=True, text=True).stdout
    files += ["%s/%s" % (r, f) for f in out.splitlines() if r == "OpenPLC_Test" or PAT.search(f)]

T, P, B, C, D, X = ("IAPTranfer_Tool/", "OpenPLC_PortsTestingTool/", "open_plc_cube_ide/", "open_plc_arduino/",
                    "OpenPLC_Docs/", "OpenPLC_Test/")

# Destinations, in the order the summary prints them.
BOOT_U = "`$BOOT` 部件测试"
TOOL_U = "`$TOOL` 部件测试"
CORE_U = "`$CORE_REPO` 部件测试"
PT_U = "`$PORTTOOL` 部件测试"
CONTRACT = "`$TEST` 契约测试"
SYSTEM = "`$TEST` 整机测试"
INFRA = "`$TEST` 测试基础设施"
DOCS = "`$PROD` 文档检查"
FIRMWARE = "不是测试：留在 `$BOOT`（编进固件的板上自测 / 工装固件源码）"
PT_SHIP = "不是测试：`$PORTTOOL` 的产品数据或发版工具"
PT_INFRA = "`$PORTTOOL` 自己的测试基础设施（保留，见「部件仓要不要本机配置」）"
UPSTREAM = "上游第三方代码自带的，不属于本产品，不动"

# (prefix or regex, destination, why: which repos it needs)
RULES = [
    (C + "system/Middlewares/OpenAMP/", UPSTREAM, "OpenAMP 自带"),
    (B + "TestCase/", FIRMWARE, "只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件"),
    (B + "tests/", BOOT_U, "T1-16、owner 区各组、T2-34、P16、P17：只编或只扫 `$BOOT`"),
    (C + "tests/", CORE_U, "P3、P4、P5、P15、P19、T2-21：只用板卡包（和 `arduino-cli`）"),
    (D + "tools/", DOCS, "P7、P8、P9、P12、P13、P14、P18：查 `$PROD`"),
    # IAPTool repo: its own tests only
    (T + "tests/", TOOL_U, "T1-15、T1-19/T1-20：只用 `$TOOL`"),
    (T + "key_lookup_test.go", TOOL_U, "T1-35：只用 `$TOOL`"),
    (T + "internal/", TOOL_U, "T1-35：只用 `$TOOL`"),
    (T + "iapproto/", TOOL_U, "T1-35：只用 `$TOOL`"),
    (T + "netiface/", TOOL_U, "T1-35：只用 `$TOOL`"),
    # OpenPLC_Test
    (X + "tools/check_mirror_sync.py", CONTRACT, "P2：比 `$BOOT`、板卡包、`$TOOL`、`$PORTTOOL` 的镜像代码（校准值区一次比三方）"),
    (X + "tools/check_version_sync.py", CONTRACT, "P1：比 `$BOOT` 和板卡包的版本号"),
    (X + "tools/check_tool_sync.py", CONTRACT, "P11：比 `$TOOL` 编出的 IAPTool 和板卡包里那份"),
    (X + "tools/check_golden_vectors.py", CONTRACT, "P20：出货 IAPTool 生成的结构对 `$BOOT` 提交的黄金向量"),
    (X + "host/fakeboard/run_ide_upload.py", SYSTEM, "T1-34：`arduino-cli` + 板卡包的上传配方 + IAPTool"),
    (X + "host/fakeboard/", CONTRACT, "T1-18a–g：IAPTool 对 bootloader 协议；替身改用 `$BOOT` 真代码后要两个仓"),
    (X + "host/renode/", SYSTEM, "T3-05：`$BOOT` 的 bootloader + 板卡包例程 + IAPTool，在 Renode 里"),
    (X + "onboard/", SYSTEM, "上板用的 sketch，由上板脚本用 `arduino-cli` 编、IAPTool 传"),
    (X + "acceptance/", SYSTEM, "一轮整机上板验收的记录"),
    (re.compile(re.escape(X) + r"[^/]+\.go$"), SYSTEM, "`TestCase.exe`：import `$TOOL` 的公开包、调 IAPTool，对着真板子跑"),
    (re.compile(re.escape(X) + r"tools/run_[^/]+\.py$"), SYSTEM, "上板用例的驱动：调 IAPTool（多数还用 ST-Link / `arduino-cli`）对着真板子跑"),
    (X, INFRA, "本机配置、平台层、烧录、抓串口、板子状态、端口小工具、本仓说明"),
    # PortTool repo
    (P + "TestCase/host/porttool_caps/", PT_U, "T4-01 / 模拟板：编工装固件，决策 78 的例外"),
    (P + "TestCase/host/porttool_plan/", PT_U, "T4-04：假板子 + 已提交的能力表"),
    (P + "TestCase/host/porttool_panel/", PT_U, "T4-02 / T4-03：面板 + 模拟板，决策 78 的例外"),
    (P + "TestCase/plans/", PT_SHIP, "随 PortTool 发出去的方案文件"),
    (P + "TestCase/tools/build_fixture.py", PT_SHIP, "编工装镜像，交付要用"),
    (P + "TestCase/tools/make_delivery.py", PT_SHIP, "打交付包"),
    (P + "TestCase/tools/md2html.py", PT_SHIP, "交付包里的说明页"),
    (P + "TestCase/", PT_INFRA, "本仓的 `common` / `init_machine` / `selfcheck` 和本机配置"),
    (P + "internal/", PT_U, "只用 `$PORTTOOL`"),
]


def classify(f):
    for key, dest, why in RULES:
        if (key.search(f) if isinstance(key, re.Pattern) else f.startswith(key) or f == key):
            return dest, why
    return None, None


rows, unknown = [], []
for f in files:
    dest, why = classify(f)
    if dest is None:
        unknown.append(f)
    rows.append((f, dest or "**没有规则命中**", why or ""))

ORDER = [BOOT_U, TOOL_U, CORE_U, PT_U, CONTRACT, SYSTEM, INFRA, DOCS, PT_INFRA, PT_SHIP, FIRMWARE, UPSTREAM]
summary = OrderedDict((k, 0) for k in ORDER)
for _, dest, _ in rows:
    summary[dest] = summary.get(dest, 0) + 1
summary = OrderedDict((k, v) for k, v in summary.items() if v)

def link(text, target):
    """A markdown link, relative to the inventory file (built here so P9 does
    not read it as a path relative to this script)."""
    return "[%s](%s)" % (text, target)


lines = ["# 每一项现有测试归哪一层、哪个仓 —— 归属表", "",
         "「%s」那张票的产物。范围是 %s「全集」那条命令的输出，由 %s 生成，2026-10-02 跑出 **%d** 个文件，下表也是 %d 行。" % (
             link("每一项现有测试归哪一层、哪个仓", "issues/TA-01-which-layer-and-repo-does-each-test-belong-to.md"),
             link("map.md", "map.md"),
             link("`tools/classify_tests_by_layer.py`", "../../tools/classify_tests_by_layer.py"),
             len(files), len(rows)),
         "判据：%s，跑它需要几个仓。" % link("决策 78", os.path.relpath(WS / "OpenPLC_Docs" / "docs" / "tables" / "DECISIONS.md", OUT.parent).replace(os.sep, "/")), "",
         "## 汇总", "", "| 去处 | 文件数 |", "|---|---|"]
lines += ["| %s | %d |" % (k, v) for k, v in summary.items()]
lines += ["", "## 逐个文件", "", "| 文件 | 去处 | 依据 |", "|---|---|---|"]
lines += ["| `%s` | %s | %s |" % r for r in rows]
OUT.write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
print(len(files), "files,", len(unknown), "unmatched")
for u in unknown:
    print("  ", u)
for k, v in summary.items():
    print("%4d  %s" % (v, k))
sys.exit(1 if unknown else 0)
