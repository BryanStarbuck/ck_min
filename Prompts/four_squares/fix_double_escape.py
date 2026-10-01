#!/usr/bin/env python3
"""Repair double-escaped HTML entities inside generated blocks.

card_index.csv alt text already contains entities (&quot; etc). An escaping pass
that blindly rewrote & -> &amp; turned those into &amp;quot;, which renders to a
visible "&quot;" on the page instead of a quote mark. Only touches our own
blocks, and only sequences that are unambiguously a double-escape.

  --apply   write changes (default is a dry run)
"""
import os, re, sys
from pathlib import Path

ROOT = Path(os.path.expanduser("~/BGit/Bryan_git/charlie-kirk"))
APPLY = "--apply" in sys.argv

BLOCK_RE = re.compile(
    r"(?:\{/\*|<!--)\s*CK_(?:INTERESTING_HERE|INTERESTING_OTHER|4SQ_SECTION|4SQ_SITEWIDE)_START"
    r".*?CK_(?:INTERESTING_HERE|INTERESTING_OTHER|4SQ_SECTION|4SQ_SITEWIDE)_END\s*(?:\*/\}|-->)", re.S)
DBL_RE = re.compile(r"&amp;(quot|apos|amp|mdash|ndash|rarr|lt|gt);")

files, fixes = 0, 0
for p in sorted((ROOT / "site/docs").rglob("*.md*")):
    t = p.read_text(encoding="utf-8", errors="replace")
    if "CK_4SQ" not in t and "CK_INTERESTING" not in t:
        continue
    n = [0]

    def fix(m):
        seg, c = DBL_RE.subn(r"&\1;", m.group(0))
        n[0] += c
        return seg

    new = BLOCK_RE.sub(fix, t)
    if n[0]:
        files += 1
        fixes += n[0]
        print(("FIX " if APPLY else "WOULD FIX ") + f"{p.relative_to(ROOT)}  ({n[0]})")
        if APPLY:
            p.write_text(new, encoding="utf-8")

print(f"\nfiles {files}, entities repaired {fixes}"
      f"{'' if APPLY else '  (dry run - pass --apply)'}")
