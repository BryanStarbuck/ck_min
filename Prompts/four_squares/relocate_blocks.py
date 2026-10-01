#!/usr/bin/env python3
"""Move an already-written four-block run to the correct anchor.

The anchor is the EARLIEST trailing-apparatus marker in the file, not the first
entry of a priority list. Pages written before that fix put the blocks below the
page's own "## Interesting" / "## Related Areas" / "## Sources" instead of above.

  --apply   write changes (default is a dry run)
"""
import csv, os, re, sys
from pathlib import Path

ROOT = Path(os.path.expanduser("~/BGit/Bryan_git/charlie-kirk"))
WORK = ROOT / "prompts/four_squares"
APPLY = "--apply" in sys.argv

NAMES = ["CK_INTERESTING_HERE", "CK_INTERESTING_OTHER", "CK_4SQ_SECTION", "CK_4SQ_SITEWIDE"]
RUN_RE = re.compile(
    r"(?:\{/\*|<!--)\s*CK_INTERESTING_HERE_START.*?"
    r"CK_4SQ_SITEWIDE_END\s*(?:\*/\}|-->)", re.S)

ANCHOR_PATTERNS = [
    ("CK_AUTHOR_CREDIT", re.compile(r"(?:\{/\*|<!--)\s*CK_AUTHOR_CREDIT")),
    ("H2_INTERESTING", re.compile(r"^## Interesting\s*$", re.M)),
    ("H2_RELATED_AREAS", re.compile(r"^## Related Areas\s*$", re.M)),
    ("CK_PLACED_IMAGES", re.compile(r"(?:\{/\*|<!--)\s*CK_PLACED_IMAGES_START")),
    ("H2_SOURCES", re.compile(r"^## (?:Sources|Fix Laws|The Laws)\s*$", re.M)),
]

moved = 0
for p in sorted((ROOT / "site/docs").rglob("*.md*")):
    t = p.read_text(encoding="utf-8", errors="replace")
    m = RUN_RE.search(t)
    if not m:
        continue                      # no block run, or blocks not contiguous
    run = m.group(0)
    rest = t[:m.start()] + t[m.end():]
    rest = re.sub(r"\n{4,}", "\n\n\n", rest)
    hits = [(n, mm.start()) for n, pat in ANCHOR_PATTERNS for mm in [pat.search(rest)] if mm]
    if not hits:
        continue
    _, at = min(hits, key=lambda x: x[1])
    if at >= m.start():
        continue                      # already at or above the right place
    new = rest[:at] + run + "\n\n" + rest[at:]
    new = re.sub(r"\n{4,}", "\n\n\n", new)
    moved += 1
    print(("MOVE " if APPLY else "WOULD MOVE ") + str(p.relative_to(ROOT)))
    if APPLY:
        p.write_text(new, encoding="utf-8")

print(f"\nblock runs relocated: {moved}{'' if APPLY else '  (dry run - pass --apply)'}")
