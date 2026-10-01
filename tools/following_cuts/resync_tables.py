#!/usr/bin/env python3
"""Replace the TABLE A..E block inside every cuts/*.mdx with the freshly generated
tables, so no page can drift from the register and no dropped row can survive.

The span replaced runs from the '## TABLE A' heading to the last table line of the
last TABLE section. Prose above and below is left exactly as written.
"""
import os, re, sys, glob

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "tools/following_cuts/out")
CUTS = os.path.join(ROOT, "site/docs/Planes/following/cuts")

changed, clean, missing = [], [], []
for path in sorted(glob.glob(os.path.join(CUTS, "*.mdx"))):
    slug = os.path.basename(path)[:-4]
    if slug == "overview":
        continue
    tf = os.path.join(OUT, f"{slug}.tables.md")
    if not os.path.exists(tf):
        missing.append(slug)
        continue
    fresh = open(tf, encoding="utf-8").read().rstrip("\n")
    lines = open(path, encoding="utf-8").read().split("\n")

    starts = [i for i, l in enumerate(lines) if l.startswith("## TABLE ")]
    if not starts:
        missing.append(slug + " (no TABLE heading in page)")
        continue
    a = starts[0]
    # walk forward from the last TABLE heading to the end of its table body
    b = starts[-1]
    while b + 1 < len(lines) and (lines[b + 1].startswith("|") or not lines[b + 1].strip()):
        if lines[b + 1].strip() == "" and b + 2 < len(lines) and not lines[b + 2].startswith("|"):
            break
        b += 1
    new = lines[:a] + fresh.split("\n") + lines[b + 1:]
    out = "\n".join(new)
    if out != "\n".join(lines):
        open(path, "w", encoding="utf-8").write(out)
        changed.append(slug)
    else:
        clean.append(slug)

print(f"resynced {len(changed)} pages; {len(clean)} already byte-identical")
if missing:
    print("MISSING / UNPARSED:", ", ".join(missing))
    sys.exit(1)
