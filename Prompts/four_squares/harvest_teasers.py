#!/usr/bin/env python3
"""Harvest canonical teasers from the site itself, not from agent reports.

Every emitted card carries its target url and its teaser. The site is therefore
the authoritative teaser store; agent TSV files are only a fallback for pages
that were carded before this existed. Writes the teaser column of card_index.csv.
"""
import csv, os, re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(os.path.expanduser("~/BGit/Bryan_git/charlie-kirk"))
WORK = ROOT / "prompts/four_squares"

CARD_RE = re.compile(
    r'<p className="ck-4sq-title"><a href="([^"]+)">.*?</a></p>\s*'
    r'<p className="ck-4sq-text">(.*?)</p>', re.S)

seen = defaultdict(Counter)
for p in (ROOT / "site/docs").rglob("*.md*"):
    t = p.read_text(encoding="utf-8", errors="replace")
    if "ck-4sq-title" not in t:
        continue
    for url, teaser in CARD_RE.findall(t):
        seen[url][" ".join(teaser.split())] += 1

# agent TSV files fill gaps only
for f in sorted((WORK / "teasers").glob("agent_*.tsv")):
    for line in f.read_text(encoding="utf-8").splitlines():
        if "\t" not in line:
            continue
        url, teaser = line.split("\t", 1)
        if url.startswith("/") and not seen[url]:
            seen[url][" ".join(teaser.split())] += 1

rows = list(csv.DictReader(open(WORK / "card_index.csv", newline="", encoding="utf-8")))
n_set, n_conflict = 0, 0
for r in rows:
    c = seen.get(r["url_path"])
    if not c:
        continue
    best, _ = c.most_common(1)[0]
    if len(c) > 1:
        n_conflict += 1
    if r["teaser"] != best:
        r["teaser"] = best
        n_set += 1

with open(WORK / "card_index.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), quoting=csv.QUOTE_MINIMAL)
    w.writeheader(); w.writerows(rows)

have = sum(1 for r in rows if r["teaser"])
print(f"teasers harvested from site : {len(seen)} urls")
print(f"card_index teaser column set: {n_set}  (now filled on {have} of {len(rows)} pages)")
print(f"urls with divergent teasers : {n_conflict}  (majority variant kept)")
