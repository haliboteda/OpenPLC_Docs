"""Refuse a ticket that is closed without saying what it opened up.

A resolved ticket must carry both its answer and the new unknowns that answer
produced -- writing "none" is fine, leaving the section out is not. This also
checks that every resolved ticket is indexed on its own map.

Usage:
    python tools/check_wayfinder_ticket_hygiene.py

Exits non-zero if anything is wrong. The convention it enforces is
maps/MAP-AND-TICKET-CONVENTION.md.
"""

import glob
import io
import os
import re
import sys

REQUIRED_HEADER = ("Type", "Opened", "Status", "Blocked by")
REQUIRED_ALWAYS = ("## Question", "## 怎么算答完")
REQUIRED_WHEN_RESOLVED = ("## Answer", "## 引出了什么新的未知")
TYPES = ("research", "prototype", "grilling", "task")
STATUSES = ("open", "claimed", "resolved")
HEADER_LINE = re.compile(r"^(Type|Opened|Status|Blocked by):\s*(.*)$")
ANSWER_DATE = re.compile(r"## Answer\s*\n+(\d{4}-\d{2}-\d{2})")


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


def main():
    use_utf8_stdout()
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)

    problems = []
    checked = 0
    for path in sorted(glob.glob("maps/*/issues/*.md")):
        rel = path.replace("\\", "/")
        effort = rel.split("/")[1]
        text = io.open(path, encoding="utf-8").read()
        checked += 1

        def bad(msg):
            problems.append("%s: %s" % (rel, msg))

        header = {}
        for line in text.splitlines()[1:]:
            if line.startswith("## "):
                break
            m = HEADER_LINE.match(line)
            if m:
                header[m.group(1)] = m.group(2).strip()

        for field in REQUIRED_HEADER:
            if field not in header:
                bad("missing header field: " + field)
        if header.get("Type") and header["Type"] not in TYPES:
            bad("unknown Type: " + header["Type"])
        if header.get("Status") and header["Status"] not in STATUSES:
            bad("unknown Status: " + header["Status"])
        for section in REQUIRED_ALWAYS:
            if section not in text:
                bad("missing section: " + section)

        if header.get("Status") == "resolved":
            for section in REQUIRED_WHEN_RESOLVED:
                if section not in text:
                    bad("resolved without section: " + section)
            if "## Answer" in text and not ANSWER_DATE.search(text):
                bad("## Answer does not start with a YYYY-MM-DD date")
            map_path = os.path.join("maps", effort, "map.md")
            if os.path.isfile(map_path):
                index = io.open(map_path, encoding="utf-8").read()
                if os.path.basename(path) not in index:
                    bad("resolved but not indexed in %s" % map_path)

    if problems:
        print("Ticket hygiene: %d problem(s) across %d ticket(s)." % (len(problems), checked))
        for p in problems:
            print("  " + p)
        return 1
    print("Ticket hygiene: %d ticket(s), all clean." % checked)
    return 0


if __name__ == "__main__":
    sys.exit(main())
