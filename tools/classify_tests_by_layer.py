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

files = []
for r in ("IAPTranfer_Tool", "OpenPLC_PortsTestingTool", "open_plc_cube_ide", "open_plc_arduino", "OpenPLC_Docs"):
    out = subprocess.run(["git", "-C", str(WS / r), "ls-files"], capture_output=True, text=True).stdout
    files += ["%s/%s" % (r, f) for f in out.splitlines() if PAT.search(f)]

T, P, B, C, D = "IAPTranfer_Tool/", "OpenPLC_PortsTestingTool/", "open_plc_cube_ide/", "open_plc_arduino/", "OpenPLC_Docs/"
TC = T + "TestCase/"

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
TOOL_SHIP = "不是测试：`$TOOL` 的发版工具"
PT_INFRA = "`$PORTTOOL` 自己的测试基础设施（留不留交给「部件仓要不要本机配置」）"
UPSTREAM = "上游第三方代码自带的，不属于本产品，不动"
OPEN_TA02 = "待定：只用一个仓但要上真板子（交给「只需要一个仓、但必须上真板子的测试归哪」）"
OPEN_TA06 = "待定：部件测试和整机测试共用的替身（交给「IAPTool 测试用的假板子」）"
OPEN_TA08 = "待定：不测产品，查各仓的 `.claude` 权限文件（交给「文档检查搬进 OpenPLC_Docs 后长什么样」）"

# (prefix or regex, destination, why: which repos it needs)
RULES = [
    (C + "system/Middlewares/OpenAMP/", UPSTREAM, "OpenAMP 自带"),
    (B + "TestCase/", FIRMWARE, "只用 `$BOOT`；由 `KNX_TEST_ENABLE` / `PORTTOOL_ENABLE` 等编进固件"),
    (D + "tools/", DOCS, "已经在 `$PROD`"),
    # IAPTool repo: its own unit tests
    (T + "key_lookup_test.go", TOOL_U, "只用 `$TOOL`（T1-35）"),
    (T + "internal/", TOOL_U, "只用 `$TOOL`（T1-35）"),
    # TestCase.exe: one Go package, imports IAPTool packages and runs IAPTool.exe
    (TC + "main.go", SYSTEM, "`TestCase.exe` 的入口；它 import `$TOOL` 的 `iapcert` / `iapproto` 并调 IAPTool.exe，对着真板子跑"),
    (TC + "signature.go", SYSTEM, "T1-11/12/14：import `$TOOL` 的 `iapcert` 造签名镜像，发给真板子 bootloader"),
    (TC + "signature_wrongkey.go", SYSTEM, "T1-19/20 相关：调 IAPTool.exe，对着真板子"),
    (TC + "tcp_session.go", SYSTEM, "T1-06–T1-10：import `$TOOL` 的 `iapproto`、调 IAPTool.exe，对着真板子"),
    (TC + "udp_discovery.go", OPEN_TA02, "T1-01–T1-05：只测 bootloader 的发现协议，唯一的第二个仓是为拨号 import 的 `$TOOL/internal/iapproto`"),
    (TC + "nonce_replay.go", OPEN_TA02, "T1-17：只测 bootloader 的防重放，要真板子"),
    (TC + "signature_badcrc.go", OPEN_TA02, "T1-24：只测 bootloader 拒收坏 CRC，要真板子"),
    (TC + "watch.go", SYSTEM, "`TestCase.exe` 内部的串口观察，跟着它走"),
    (TC + "requirements.txt", INFRA, "Python 依赖清单"),
    (TC + "acceptance/", SYSTEM, "一轮整机上板验收的记录"),
    # host/
    (TC + "host/bootloader_unit/gen_vectors.py", CONTRACT, "调 `$TOOL` 出货的 IAPTool 生成 `$BOOT` 测试的黄金向量，两个仓（见「bootloader 的 C 单元测试用什么驱动」）"),
    (TC + "host/bootloader_unit/", BOOT_U, "T1-16：编 `$BOOT` 的真实源码，黄金向量已提交，跑时只用 `$BOOT`"),
    (TC + "host/owner_capacity/", BOOT_U, "T2-22–T2-33、T1-33、T2-27：只编 `$BOOT` 的源码"),
    (TC + "host/sector15_reclaim/", BOOT_U, "T2-34：只编 `$BOOT` 的源码"),
    (TC + "host/owner_revoke/", CORE_U, "T2-21：编的是板卡包 `libraries/OpenPLC_IAP/src/owner_root_ro.c`，不是 bootloader"),
    (TC + "host/iapcert/", TOOL_U, "T1-15：只测 `$TOOL` 的 `iapcert`"),
    (TC + "host/crypto_ref/", TOOL_U, "T1-19/T1-20：只拿 IAPTool 的签名对照独立实现"),
    (TC + "host/fakeboard/run_ide_upload.py", SYSTEM, "T1-34：`arduino-cli` + 板卡包的上传配方 + IAPTool，三样东西"),
    (TC + "host/fakeboard/run_cases.py", TOOL_U, "T1-18a–g：只用 IAPTool 和假板子"),
    (TC + "host/fakeboard/KEY-MATCH.md", TOOL_U, "T1-18 的判据说明，跟着 run_cases.py 走"),
    (TC + "host/fakeboard/", OPEN_TA06, "T1-18（`$TOOL` 部件）和 T1-34（整机）都用它"),
    (TC + "host/renode/", SYSTEM, "T3-05：`$BOOT` 的 bootloader + 板卡包例程 + IAPTool，在 Renode 里"),
    (TC + "host/examples_build/", CORE_U, "P5：只用板卡包和 `arduino-cli`"),
    (TC + "host/variant_check/", CORE_U, "P4：只用板卡包和 `arduino-cli`"),
    (TC + "host/vector_alignment/", CORE_U, "P15：只用板卡包和 `arduino-cli`"),
    # onboard sketches: only driven by system scripts
    (TC + "onboard/iap_probe/", SYSTEM, "五条路径用的探针 app，由 `build_probe_image.py` 编、IAPTool 传"),
    (TC + "onboard/rs232/", SYSTEM, "T3-03 / T3-04：由 `run_m5.py` 等用 `arduino-cli` 编、IAPTool 传"),
    (TC + "onboard/sdram/", SYSTEM, "T3-02：由 `run_sdram.py` 用 `arduino-cli` 编、IAPTool 传"),
    # tools: consistency checks
    (TC + "tools/check_mirror_sync.py", CONTRACT, "P2：比 `$BOOT`、板卡包、`$TOOL` 的镜像代码"),
    (TC + "tools/check_version_sync.py", CONTRACT, "P1：比 `$BOOT` 和板卡包的版本号"),
    (TC + "tools/check_tool_sync.py", CONTRACT, "P11：比 `$TOOL` 编出的 IAPTool 和板卡包里那份"),
    (TC + "tools/check_core_sync.py", CORE_U, "P3：板卡包的两份（`$CORE_LIVE` 和 `$CORE_REPO`）"),
    (TC + "tools/check_no_sector15_writes.py", CORE_U, "P19：只扫板卡包"),
    (TC + "tools/check_icache_is_restored.py", BOOT_U, "P16：只扫 `$BOOT`"),
    (TC + "tools/check_cproject_ld.py", BOOT_U, "P17：只扫 `$BOOT`"),
    (TC + "tools/check_status_sync.py", DOCS, "P7：查 `$PROD`"),
    (TC + "tools/check_doc_dupes.py", DOCS, "P8：查 `$PROD`"),
    (TC + "tools/check_doc_paths.py", DOCS, "P9：查 `$PROD`，再到各代码仓核对路径"),
    (TC + "tools/check_no_stale_ids.py", DOCS, "P13：查 `$PROD`，再扫各代码仓"),
    (TC + "tools/check_changelist_has_no_orphans.py", DOCS, "P14：查 `$PROD`"),
    (TC + "tools/check_allow_hygiene.py", OPEN_TA08, "P10：扫各仓的 `.claude/settings*.json`"),
    # tools: on-board case drivers
    (TC + "tools/run_au1.py", OPEN_TA02, "T1-17：只用 ST-Link 和真板子 bootloader，不调 IAPTool"),
    (TC + "tools/run_boot0_upload_mode.py", OPEN_TA02, "T1-27：只看真板子 bootloader 的串口，不调 IAPTool"),
    (TC + "tools/run_case.py", INFRA, "跑 `TestCase.exe` 的用例并判结果"),
    (re.compile(re.escape(TC) + r"tools/run_[^/]+\.py$"), SYSTEM, "调 IAPTool（多数还用 ST-Link / `arduino-cli`）对着真板子跑"),
    # tools: infrastructure
    (TC + "tools/install_tool.py", TOOL_SHIP, "把 IAPTool 拷进板卡包，属于 IAPTool 发版"),
    (TC + "tools/selfcheck.py", INFRA, "现在的总自检入口；拆完各仓各一个"),
    (re.compile(re.escape(TC) + r"tools/"), INFRA, "本机配置、平台层、烧录、抓串口、板子状态、端口小工具"),
    # PortTool repo
    (P + "TestCase/host/porttool_caps/build.py", PT_U, "T4-01：编工装固件 `$BOOT/TestCase/porttool/`，按决策 78 的例外算 PortTool 自己的"),
    (P + "TestCase/host/porttool_caps/harness/", PT_U, "T4-01 / 模拟板：编工装固件，决策 78 的例外"),
    (P + "TestCase/host/porttool_caps/PORTTOOL-CAPS-TEST.md", PT_U, "T4-01 的说明，跟着 harness 走"),
    (P + "TestCase/host/porttool_caps/caps_golden.txt", PT_U, "T4-01 产出并提交的能力表；跑 Go 测试时只读它"),
    (P + "TestCase/host/porttool_caps/", PT_U, "Go 测试只读已提交的 `caps_golden.txt`，只用 `$PORTTOOL`"),
    (P + "TestCase/host/porttool_plan/", PT_U, "T4-04：假板子 + 已提交的能力表，只用 `$PORTTOOL`"),
    (P + "TestCase/host/porttool_panel/", PT_U, "T4-02 / T4-03：面板 + 模拟板，决策 78 的例外"),
    (P + "TestCase/plans/", PT_SHIP, "随 PortTool 发出去的方案文件"),
    (P + "TestCase/tools/check_calarea.py", CONTRACT, "和 P2 的校准值区一项合成一道，一次比 `$BOOT`、板卡包、`$PORTTOOL` 三方"),
    (P + "TestCase/tools/check_doc_paths.py", DOCS, "查 `$PROD` 里的 `$PORTTOOL/...` 路径"),
    (P + "TestCase/tools/build_fixture.py", PT_SHIP, "编工装镜像，交付要用"),
    (P + "TestCase/tools/make_delivery.py", PT_SHIP, "打交付包"),
    (P + "TestCase/tools/md2html.py", PT_SHIP, "交付包里的说明页"),
    (P + "TestCase/tools/", PT_INFRA, "本仓的 `common` / `init_machine` / `selfcheck`"),
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

ORDER = [BOOT_U, TOOL_U, CORE_U, PT_U, CONTRACT, SYSTEM, INFRA, DOCS, OPEN_TA02, OPEN_TA06, OPEN_TA08,
         PT_INFRA, TOOL_SHIP, PT_SHIP, FIRMWARE, UPSTREAM]
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
