#!/usr/bin/env python3
"""Repair links inside generated blocks that point at non-existent routes.

Cause: routes.txt used to be derived from filenames, which stripped leading
number-like segments (2026-, 12-, 99-) that Docusaurus actually keeps, and
ignored frontmatter id:/slug:. Cards and bullets were validated against that
wrong whitelist, so they shipped 404s.

Resolution is by unambiguous suffix match against the real built routes.

  --apply   write changes (default is a dry run)
"""
import os, re, sys
from pathlib import Path
from collections import Counter

ROOT = Path(os.path.expanduser("~/BGit/Bryan_git/charlie-kirk"))
WORK = ROOT / "prompts/four_squares"
APPLY = "--apply" in sys.argv
# splitlines, never split: routes like "/Topics3/Suspects (List)/overview"
# contain spaces, and whitespace-splitting turns them into false negatives.
routes = [r for r in (WORK / "routes.txt").read_text().splitlines() if r]
routeset = set(routes)

MANUAL = {
    # /TPUSA/TPUSA was never built; the section hub is the overview page.
    "/TPUSA/TPUSA": "/TPUSA/overview",
}


def resolve(bad):
    if bad in MANUAL:
        return MANUAL[bad]
    parent, _, leaf = bad.rpartition("/")
    # the real route keeps a numeric prefix the deriver removed
    cands = [r for r in routes
             if r.rpartition("/")[0] == parent
             and re.fullmatch(r"[\d._-]*" + re.escape(leaf), r.rpartition("/")[2])]
    if len(cands) == 1:
        return cands[0]
    cands = [r for r in routes if r.rpartition("/")[0] == parent
             and r.rpartition("/")[2].endswith(leaf)]
    return cands[0] if len(cands) == 1 else None


BLOCK_RE = re.compile(
    r"(?:\{/\*|<!--)\s*CK_(?:INTERESTING_HERE|INTERESTING_OTHER|4SQ_SECTION|4SQ_SITEWIDE)_START"
    r".*?CK_(?:INTERESTING_HERE|INTERESTING_OTHER|4SQ_SECTION|4SQ_SITEWIDE)_END\s*(?:\*/\}|-->)", re.S)

unresolved, fixed, files = Counter(), Counter(), 0
for p in sorted((ROOT / "site/docs").rglob("*.md*")):
    t = p.read_text(encoding="utf-8", errors="replace")
    if "CK_4SQ" not in t and "CK_INTERESTING" not in t:
        continue
    n = [0]

    def fix_block(m):
        seg = m.group(0)
        for bad in set(re.findall(r'href="(/[^"#?]*)"', seg) + re.findall(r"\]\((/[^)\s#?]*)\)", seg)):
            if bad.rstrip("/") in routeset or bad in routeset:
                continue
            good = resolve(bad)
            if not good:
                unresolved[bad] += 1
                continue
            seg = seg.replace(f'href="{bad}"', f'href="{good}"').replace(f"]({bad})", f"]({good})")
            fixed[f"{bad} -> {good}"] += 1
            n[0] += 1
        return seg

    new = BLOCK_RE.sub(fix_block, t)
    if n[0]:
        files += 1
        if APPLY:
            p.write_text(new, encoding="utf-8")

for k, v in fixed.most_common():
    print(f"  {v:>3}  {k}")
if unresolved:
    print("\nUNRESOLVED (need a human decision):")
    for k, v in unresolved.most_common():
        print(f"  {v:>3}  {k}")
print(f"\nfiles {files}, links repaired {sum(fixed.values())}, unresolved {sum(unresolved.values())}"
      f"{'' if APPLY else '  (dry run - pass --apply)'}")
