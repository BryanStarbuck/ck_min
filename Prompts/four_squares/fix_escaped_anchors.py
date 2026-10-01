#!/usr/bin/env python3
"""Un-escape anchor tags that were half-escaped inside generated blocks.

Symptom on the live page: the reader sees the literal text
    <a href="/intelligence/overview">foreign-intelligence threads</a>
because the "<" was written as &lt; while the ">" stayed raw. A teaser link is
supposed to be a real HTML anchor in JSX, so restore the tag.

  --apply   write changes (default is a dry run)
"""
import os, re, sys
from pathlib import Path

ROOT = Path(os.path.expanduser("~/BGit/Bryan_git/charlie-kirk"))
APPLY = "--apply" in sys.argv

BLOCK_RE = re.compile(
    r"(?:\{/\*|<!--)\s*CK_(?:INTERESTING_HERE|INTERESTING_OTHER|4SQ_SECTION|4SQ_SITEWIDE)_START"
    r".*?CK_(?:INTERESTING_HERE|INTERESTING_OTHER|4SQ_SECTION|4SQ_SITEWIDE)_END\s*(?:\*/\}|-->)", re.S)
OPEN_RE = re.compile(r'&lt;a href="([^"]+)"\s*&gt;|&lt;a href="([^"]+)"\s*>')
CLOSE_RE = re.compile(r"&lt;/a\s*&gt;|&lt;/a\s*>")

files, fixes = 0, 0
for p in sorted((ROOT / "site/docs").rglob("*.md*")):
    t = p.read_text(encoding="utf-8", errors="replace")
    if "&lt;a href" not in t:
        continue
    n = [0]

    def fix(m):
        seg = m.group(0)
        seg, a = OPEN_RE.subn(lambda mm: f'<a href="{mm.group(1) or mm.group(2)}">', seg)
        seg, b = CLOSE_RE.subn("</a>", seg)
        n[0] += a + b
        return seg

    new = BLOCK_RE.sub(fix, t)
    if n[0]:
        files += 1
        fixes += n[0]
        print(("FIX " if APPLY else "WOULD FIX ") + f"{p.relative_to(ROOT)}  ({n[0]})")
        if APPLY:
            p.write_text(new, encoding="utf-8")

print(f"\nfiles {files}, anchor tags restored {fixes}"
      f"{'' if APPLY else '  (dry run - pass --apply)'}")
