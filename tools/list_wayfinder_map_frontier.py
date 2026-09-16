"""List the frontier of every wayfinder map in this repository.

The frontier is every ticket that is still open and whose blockers have all
been resolved -- the tickets a session may claim right now.

Usage:
    python tools/list_wayfinder_map_frontier.py [--all]

The convention this reads is maps/MAP-AND-TICKET-CONVENTION.md.
"""

import argparse
import glob
import io
import os
import re
import sys

FIELD = re.compile(r"^(Type|Opened|Status|Blocked by):\s*(.*)$")
REQUIRED = ("Type", "Opened", "Status", "Blocked by")


def use_utf8_stdout():
    """Print ticket titles readably on a Chinese Windows console."""
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleOutputCP(65001)
        except Exception:
            pass
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def read_ticket(path):
    """Parse one ticket file into a dict, or return None with a reason."""
    text = io.open(path, encoding="utf-8").read()
    lines = text.splitlines()
    if not lines or not lines[0].startswith("# "):
        return None, "no title on the first line"
    ticket = {
        "path": path,
        "id": os.path.basename(path).split("-")[0] + "-" + os.path.basename(path).split("-")[1],
        "title": lines[0][2:].strip(),
        "blockers": [],
    }
    for line in lines[1:]:
        if line.startswith("## "):
            break
        m = FIELD.match(line)
        if m:
            ticket[m.group(1)] = m.group(2).strip()
    missing = [f for f in REQUIRED if f not in ticket]
    if missing:
        return None, "missing header field(s): " + ", ".join(missing)
    raw = ticket["Blocked by"]
    if raw and raw != "-":
        ticket["blockers"] = [b.strip() for b in raw.split(",") if b.strip()]
    return ticket, None


def main():
    use_utf8_stdout()
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true",
                    help="also list blocked, claimed and resolved tickets")
    args = ap.parse_args()

    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)

    problems = []
    maps = {}
    for path in sorted(glob.glob("maps/*/issues/*.md")):
        effort = path.split(os.sep)[1] if os.sep in path else path.split("/")[1]
        ticket, why = read_ticket(path)
        if ticket is None:
            problems.append("%s: %s" % (path, why))
            continue
        maps.setdefault(effort, {})[ticket["id"]] = ticket

    if not maps:
        print("No maps found under maps/.")
        return 0

    for effort in sorted(maps):
        tickets = maps[effort]
        print("=== %s ===" % effort)
        blocks = {}
        for t in tickets.values():
            for b in t["blockers"]:
                blocks.setdefault(b, []).append(t["id"])
        for tid in sorted(tickets):
            t = tickets[tid]
            unknown = [b for b in t["blockers"] if b not in tickets]
            problems.extend("%s: blocked by unknown ticket %s" % (t["path"], b)
                            for b in unknown)
            # A blocker that does not exist counts as unresolved, so a typo
            # cannot make a blocked ticket look takeable.
            open_blockers = [b for b in t["blockers"]
                            if b not in tickets or tickets[b]["Status"] != "resolved"]
            if t["Status"] == "open" and not open_blockers:
                mark = "TAKEABLE"
            elif t["Status"] == "resolved":
                mark = "resolved"
            elif t["Status"] == "claimed":
                mark = "claimed "
            else:
                mark = "blocked "
            if not args.all and mark.strip() != "TAKEABLE":
                continue
            line = "  %s  %-8s  %s" % (mark, t["Type"], t["title"])
            if open_blockers:
                line += "  <- waits on " + ", ".join(open_blockers)
            elif blocks.get(tid):
                line += "  (holds up %d)" % len(blocks[tid])
            print(line)
        print("")

    if problems:
        print("PROBLEMS")
        for p in problems:
            print("  " + p)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
