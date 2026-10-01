#!/usr/bin/env python3
"""Stage 8 coordinator merge. Reads the site as ground truth, not agent claims.

  python3 merge_wave.py <wave-label>
"""
import csv, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(os.path.expanduser("~/BGit/Bryan_git/charlie-kirk"))
WORK = ROOT / "prompts/four_squares"
LABEL = next((a for a in sys.argv[1:] if not a.startswith("-")), "wave")
BATCH = int(os.environ.get("FSQ_BATCH", "20"))
BLOCKS = [("CK_INTERESTING_HERE", "H"), ("CK_INTERESTING_OTHER", "O"),
          ("CK_4SQ_SECTION", "S"), ("CK_4SQ_SITEWIDE", "W")]

led = list(csv.DictReader(open(WORK / "ledger.csv")))
from collections import Counter as _C
area_size = _C(r["level2"] for r in led)
edited, cards = [], 0
for r in led:
    p = ROOT / r["file_path"]
    if not p.exists():
        r["status"] = "MISSING"
        continue
    t = p.read_text(encoding="utf-8", errors="replace")
    got = "".join(letter if (name + "_START") in t and (name + "_END") in t else "-"
                  for name, letter in BLOCKS)
    if got != r["blocks"]:
        r["blocks"] = got
        r["updated"] = LABEL
        edited.append(r["file_path"])
    # What a page CAN carry depends on how many sisters its Level 2 has.
    #   1 page  : no in-area link and no in-area grid exist at all
    #   2 pages : one sister - enough for the bullets, not for a 2x2 grid
    #   3+      : the full set
    n_area = area_size.get(r["level2"], 0)
    target = "-O-W" if n_area <= 1 else ("HO-W" if n_area == 2 else "HOSW")
    r["status"] = "DONE" if got == target else ("PARTIAL" if got != "----" else "TODO")
    cards += len(re.findall(r'className="ck-4sq-title"', t))

with open(WORK / "ledger.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=["file_path", "level2", "status", "blocks", "agent", "updated"])
    w.writeheader(); w.writerows(led)

# refresh line_count in pages.csv for edited pages
if edited:
    rows = list(csv.DictReader(open(ROOT / "pages.csv")))
    fields = rows[0].keys()
    ed = set(edited)
    n = 0
    for r in rows:
        if r["file_path"] in ed and (ROOT / r["file_path"]).exists():
            new = str(sum(1 for _ in open(ROOT / r["file_path"], encoding="utf-8", errors="replace")))
            if r.get("line_count") != new:
                r["line_count"] = new; n += 1
    with open(ROOT / "pages.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(fields), quoting=csv.QUOTE_MINIMAL)
        w.writeheader(); w.writerows(rows)
    print(f"pages.csv line_count refreshed : {n}")

# pages on disk with no pages.csv row
csv_paths = {r["file_path"] for r in csv.DictReader(open(ROOT / "pages.csv"))}
idx = list(csv.DictReader(open(WORK / "card_index.csv")))
missing_rows = [r["file_path"] for r in idx if r["file_path"] not in csv_paths]
orphans = [p for p in csv_paths if not (ROOT / p).exists()]

done = sum(1 for r in led if r["status"] == "DONE")
part = sum(1 for r in led if r["status"] == "PARTIAL")
todo = sum(1 for r in led if r["status"] == "TODO")
print(f"{LABEL} complete - pages done {done} of {len(led)} ({100*done//len(led)}%) "
      f"- partial {part} - todo {todo}")
print(f"cards on site   : {cards}")
print(f"pages edited    : {len(edited)}")
print(f"csv rows missing: {len(missing_rows)}  (pages on disk with no pages.csv row)")
print(f"csv rows orphan : {len(orphans)}  (REVIEW - file_path no longer on disk)")
(WORK / "csv_missing_rows.txt").write_text("\n".join(sorted(missing_rows)) + "\n")
(WORK / "csv_orphan_rows.txt").write_text("\n".join(sorted(orphans)) + "\n")

# Next wave batches. ONLY when explicitly asked: agents read their batch file
# while they run, so re-dealing mid-wave silently changes the list under them.
# An agent that expands $(cat batches/agent_N.txt) after a re-deal verifies the
# wrong files. Deal only between waves, never during one.
if "--deal" not in sys.argv:
    print("\n(batches NOT re-dealt - pass --deal between waves)")
    raise SystemExit(0)

for a in range(1, 13):
    t = sorted([r for r in led if r["agent"] == str(a) and r["status"] != "DONE"],
               key=lambda r: (r["level2"], r["file_path"]))
    (WORK / f"batches/agent_{a}.txt").write_text("\n".join(x["file_path"] for x in t[:BATCH]) + "\n")
