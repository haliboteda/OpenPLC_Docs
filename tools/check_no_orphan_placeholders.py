"""Refuse a placeholder that admits something has nowhere to go.

Writing "no destination yet" in a table is how a whole category goes quiet:
the words, not a status symbol -- an empty checkbox means not started, which is
a legitimate thing for a status column to say.
the marker stays, nobody is on the hook, and the gap surfaces months later at
the bench. A placeholder is allowed only when the same row names the ticket that owns it.
Only table rows are checked: a cell is where a destination gets declared, and
prose that quotes a marker is not itself a missing destination.

Usage:
    python tools/check_no_orphan_placeholders.py [extra_path ...]

Extra paths let this run against documents that have not been migrated yet.
Exits non-zero if any placeholder has no ticket beside it.
"""

import glob
import io
import os
import re
import sys

MARKERS = ("没有去处", "TBD", "暂无去处")
TICKET_REF = re.compile(r"[A-Z]{2,5}-\d{2}")


def use_utf8_stdout():
    """Print document lines readably on a Chinese Windows console."""
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


def scan(path, problems):
    try:
        text = io.open(path, encoding="utf-8").read()
    except (IOError, UnicodeDecodeError):
        return 0
    for n, line in enumerate(text.splitlines(), 1):
        # Only table rows: declaring a destination happens in a cell, and prose
        # that merely quotes a marker is not itself a missing destination.
        if not line.lstrip().startswith("|"):
            continue
        if any(m in line for m in MARKERS) and not TICKET_REF.search(line):
            problems.append("%s:%d: placeholder with no ticket beside it\n      %s"
                            % (path.replace("\\", "/"), n, line.strip()[:140]))
    return 1


def main():
    use_utf8_stdout()
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)

    problems = []
    checked = 0
    for path in sorted(glob.glob("docs/**/*.md", recursive=True)) + ["WHERE-THINGS-LIVE.md"]:
        checked += scan(path, problems)
    for extra in sys.argv[1:]:
        checked += scan(extra, problems)

    if problems:
        print("Orphan placeholders: %d in %d document(s)." % (len(problems), checked))
        for p in problems:
            print("  " + p)
        print("")
        print("Every one of these says something has nowhere to go. Give it a real")
        print("destination, or open a ticket and name it on the same line.")
        return 1
    print("Orphan placeholders: none in %d document(s)." % checked)
    return 0


if __name__ == "__main__":
    sys.exit(main())
