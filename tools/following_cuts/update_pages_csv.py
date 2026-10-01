#!/usr/bin/env python3
"""Add / refresh a pages.csv row for the cuts hub and every drill-down page, and
refresh line_count on the one page this run edited (following/overview.mdx)."""
import csv, os, re, sys, glob

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CSV = os.path.join(ROOT, "pages.csv")
CUTS = os.path.join(ROOT, "site/docs/Planes/following/cuts")
PARENT = "Planes_Following_Index"


def fm(path):
    t = open(path, encoding="utf-8").read()
    lines = t.split("\n")
    block = {}
    if lines and lines[0].strip() == "---":
        for i, l in enumerate(lines[1:], 1):
            if l.strip() == "---":
                break
            m = re.match(r"^(\w+):\s*(.*)$", l)
            if m:
                block[m.group(1)] = m.group(2).strip().strip('"')
    return block, len(lines)


with open(CSV, newline="", encoding="utf-8") as f:
    rd = csv.DictReader(f)
    cols = rd.fieldnames
    rows = list(rd)

by_key = {r["page_key"]: r for r in rows}


def key_for(slug):
    return "Planes_Cut_" + re.sub(r"[^A-Za-z0-9]+", "_", slug).strip("_")


added = updated = 0
for path in sorted(glob.glob(os.path.join(CUTS, "*.mdx"))):
    slug = os.path.basename(path)[:-4]
    meta, n = fm(path)
    is_hub = slug == "overview"
    key = "Planes_Cuts_Index" if is_hub else key_for(slug)
    row = {
        "page_key": key,
        "parent_key": PARENT if is_hub else "Planes_Cuts_Index",
        "level": "4" if is_hub else "5",
        "level2_parent": "Planes", "level2_section": "Planes",
        "page_type": "overview" if is_hub else "topic",
        "url_path": f"/Planes/following/cuts/{slug}",
        "file_path": f"site/docs/Planes/following/cuts/{slug}.mdx",
        "title": meta.get("title", slug),
        "sidebar_label": meta.get("sidebar_label", meta.get("title", slug)),
        "directory": "Planes/following/cuts",
        "extension": "mdx", "has_frontmatter": "yes",
        "line_count": str(n),
        "description": meta.get("description", ""),
    }
    if key in by_key:
        by_key[key].update(row)
        updated += 1
    else:
        rows.append(row)
        by_key[key] = row
        added += 1

# refresh line_count on the overview page this run edited
ov = os.path.join(ROOT, "site/docs/Planes/following/overview.mdx")
for r in rows:
    if r["file_path"] == "site/docs/Planes/following/overview.mdx":
        r["line_count"] = str(len(open(ov, encoding="utf-8").read().split("\n")))

with open(CSV, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for r in rows:
        w.writerow({c: r.get(c, "") for c in cols})
print(f"pages.csv: {added} rows added, {updated} refreshed, {len(rows)} total")
