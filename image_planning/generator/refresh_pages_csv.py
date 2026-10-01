#!/usr/bin/env python3
"""Refresh pages.csv rows for generated /Photos pages from the files on disk.

Used after enrichment agents edit page bodies/titles: updates title,
sidebar_label, description, and line_count for every row whose file_path is
under site/docs/Photos/ (except the landing page). Does NOT touch any page
file and does NOT add or remove rows.
"""
import csv, os, re

ROOT = os.path.expanduser("~/BGit/Bryan_git/charlie-kirk")
PAGES_CSV = os.path.join(ROOT, "pages.csv")
PREFIX = "site/docs/Photos/"
LANDING = "site/docs/Photos/overview.mdx"

FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)


def fm_field(fm, name):
    m = re.search(rf"^{name}:\s*(.*)$", fm, re.M)
    if not m:
        return None
    v = m.group(1).strip()
    if v.startswith('"') and v.endswith('"'):
        import json
        try:
            v = json.loads(v)
        except Exception:
            v = v[1:-1]
    return v


with open(PAGES_CSV, newline="") as f:
    rdr = csv.DictReader(f)
    fields = rdr.fieldnames
    rows = list(rdr)
for r in rows:
    r.pop(None, None)

updated = missing = 0
for r in rows:
    fp = r["file_path"]
    if not fp.startswith(PREFIX) or fp == LANDING:
        continue
    path = os.path.join(ROOT, fp)
    if not os.path.exists(path):
        missing += 1
        continue
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = FM_RE.match(text)
    if m:
        fm = m.group(1)
        for col, name in (("title", "title"), ("sidebar_label", "sidebar_label"),
                          ("description", "description")):
            v = fm_field(fm, name)
            if v:
                r[col] = v
    r["line_count"] = str(text.count("\n") + 1)
    updated += 1

with open(PAGES_CSV, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore", restval="")
    w.writeheader()
    w.writerows(rows)
print(f"refreshed {updated} rows; {missing} rows point at missing files")
