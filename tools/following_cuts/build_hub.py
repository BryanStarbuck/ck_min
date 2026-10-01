#!/usr/bin/env python3
"""Write following/cuts/overview.mdx — the hub that indexes every drill-down page."""
import json, os

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "tools/following_cuts/out")
CUTS = os.path.join(ROOT, "site/docs/Planes/following/cuts")
idx = {i["slug"]: i for i in json.load(open(os.path.join(OUT, "_index.json")))}

GROUPS = [
    ("The count, broken open", "The first table on the overview — *“The question people actually ask.”* "
     "Every row of it is a filter over the same 85-row register.",
     ["all-85", "dated-80", "never-published-5", "charlie-only-9", "charlie-and-erika-9",
      "charlie-any-18", "erika-any-70", "erika-only-61", "tpusa-no-kirk-6"]),
    ("Which aircraft was named", "The tail-number rows of the same table, and the aircraft table further down. "
     "Two airframes carry 76 of the 85 rows.",
     ["tail-su-btt-57", "tail-su-bnd-16", "tail-both-3", "tail-unresolved-9",
      "tail-either-btt-or-bnd-5", "tail-none-4"]),
    ("Applying the presence rule", "The second table — what is left when a person is treated as absent "
     "unless their presence can be established.",
     ["erika-established-0", "no-kirk-placeable-61"]),
    ("What the recovered position data says", "The verdict table. Each verdict is a measurement against raw "
     "ADS-B traces this investigation pulled from free archives and stored in the repository.",
     ["adsb-at-claimed-airport-25", "adsb-elsewhere-3", "adsb-same-metro-1", "adsb-not-heard-37",
      "adsb-no-archive-coverage-10", "adsb-no-tail-4", "adsb-no-date-5", "ground-confirmed-10"]),
    ("The two ledgers, side by side", "The Charlie/TPUSA ledger and the Erika ledger do not behave the same "
     "way. These are the cells of that comparison.",
     ["ledger-charlie-tpusa-24", "ledger-charlie-corroborated-13", "ledger-charlie-refuted-0",
      "ledger-charlie-undecided-11", "ledger-erika-56", "ledger-erika-corroborated-12",
      "ledger-erika-refuted-3", "ledger-erika-undecided-41"]),
    ("The tracking-site audit", "The independent line-by-line audit of the source sheet, which reached a very "
     "different result from the position data. Both are published; neither is reconciled into the other.",
     ["audit-accurate", "audit-inaccurate", "audit-partial", "audit-archive-gap", "audit-not-reached"]),
    ("Where the pairings actually land", "The rows where the aircraft side and the Kirk/TPUSA side fall close "
     "enough together to be worth testing.",
     ["same-day-sourced-event-10", "within-three-days-17"]),
    ("The five clustering states", "Each state page carries the overlap rows, every logged ground presence by "
     "every following aircraft, and every sourced Kirk or TPUSA appearance in that state.",
     ["state-utah", "state-nebraska", "state-kansas", "state-delaware", "state-missouri"]),
]

all_slugs = [s for _, _, ss in GROUPS for s in ss]
missing = [s for s in idx if s not in all_slugs]
assert not missing, f"ungrouped slices: {missing}"

def bullet(s):
    i = idx[s]
    n = i["rows"]
    cnt = f"{n} row{'s' if n != 1 else ''}" if n else "empty by construction"
    return f"* [{i['title']}](./{s}) — **{cnt}**"

cols = [[], [], []]
flat = []
for title, blurb, slugs in GROUPS:
    flat.extend(slugs)
for n, s in enumerate(flat):
    cols[n % 3].append(bullet(s))

body = []
body.append("""---
id: cuts-overview
slug: /Planes/following/cuts/overview
displayed_sidebar: docs
title: "Table drill-downs — every number on the Following page, opened up"
sidebar_label: "Table drill-downs"
description: "Every count in every table on the Planes That Followed Them overview, opened into a page listing the specific rows behind it — which aircraft, which airport, which date, who is claimed present, and every verdict."
keywords:
  - Charlie Kirk
  - Erika Kirk
  - SU-BTT
  - SU-BND
  - overlap register
  - flight tracking
  - TPUSA
image: "/img/docusaurus-social-card.jpg"
hide_table_of_contents: true
---

{/* Full-bleed marker: activates the site-wide full-width + text-wrap
    layout in custom.css (full width + overflow-safe side videos). Scoped
    via CSS :has(). */}
<div className="ck-full-bleed" />

<a href="/Planes/following/overview" style={{display:'inline-block', marginBottom:'1rem',
padding:'0.35rem 0.9rem', background:'#1a73e8', color:'#fff',
borderRadius:'4px', textDecoration:'none', fontSize:'0.9rem'}}>&larr; Planes That Followed Them</a>

# Table drill-downs — every number, opened up

**[The Following overview](/Planes/following/overview) is a page of counts.** *85. 61. 25. 37.
"At the claimed airport." "No archive coverage." An investigator reading it wants to click the
number and see the rows &mdash; **which aircraft, which airport, what date it landed and what
date it left, who it is claimed to have been following, and what every verdict on that row
actually was.** Each page below is one of those cells, opened.

""")

body.append("<div style={{display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem'}}>\n")
for c in cols:
    body.append("<div>\n\n" + "\n".join(c) + "\n\n</div>\n")
body.append("</div>\n")

total_rows = idx["all-85"]["rows"]
body.append(f"""
## What is on every one of these pages

Each drill-down carries the same three tables, generated straight out of this directory's
register rather than retyped, so a page cannot drift from the data behind it.

**Table A &mdash; the following aircraft.** The row ID, the claimed date, the airport with its
code and full name, the city and state, the tail number linked to that aircraft's own page, the
airframe type, the ICAO hex the ADS-B network actually broadcasts, where the leg arrived from and
departed to, the arrival and departure dates of any logged ground stay covering that date, how
many days it sat, the transponder or on-ground flag, the ADS-B verdict, and the measured closest
approach in kilometres.

**Table B &mdash; who they are claimed to have been following.** Whether Charlie Kirk and Erika
Kirk are each claimed present, the Erika-location cell exactly as the source sheet gives it, the
sourced Turning Point or Kirk appearance on that same day where one exists, that event's venue and
local start time, the nearest airport to the venue with its distance in miles, and any Kirk-side
aircraft on record. Where there is no same-day appearance the table names the nearest sourced one
and how many days off it is, rather than leaving the cell blank.

**Table C &mdash; sourcing and both verdicts.** The index the row carries on the original sheet,
the tracking-site audit verdict, the ADS-B position verdict, what the position data actually says,
who published the claim, a link to the source post, and a link to that row's own full page.

The five state pages carry two more: **Table D**, every logged ground presence by every following
aircraft at that state's fields with arrival and departure dates, and **Table E**, every sourced
Kirk or TPUSA appearance in that state with venue, time and nearest airport.

## Three things every one of these pages says, because they are true of all of them

**A trace locates an aircraft. It never places a person aboard.** A verdict of *at the claimed
airport* confirms the aircraft half of a pairing and nothing else. It does not put Charlie Kirk or
Erika Kirk anywhere.

**Erika Kirk's presence is established on none of the {total_rows} rows.** Her flight logs are
[reported as erased](/Planes/Erika-Flight-Logs-Erased) and no dated itinerary has ever been
published by anyone. What the source sheet has instead is a column that usually names a whole
state, sometimes two states at once, and sometimes nothing.

**An empty archive is not a deletion.** *Not heard* means a volunteer network holds no trace for
that airframe on that date. Parked with the transponder off, outside receiver coverage, and a wrong
claimed date all look identical from the outside. Before any absence here was written down,
unrelated control aircraft with no connection to this case were queried on the same dates and the
same endpoints.

## Related

* [Planes That Followed Them](/Planes/following/overview) &mdash; the overview these pages open up
* [The overlap index](/Planes/following/overlap/overview) &mdash; one page per claimed overlap
* [The 73 overlaps](/Planes/following/73_overlaps) &mdash; the reconstructed source list
* [Speaking events](/Planes/following/speaking/overview) &mdash; the Kirk and TPUSA side of every pairing
* [What "overlap" meant](/Planes/following/Overlap_Window_Definition) &mdash; the window definition
* [Flight Data Recovery](/Planes/Flight-Data-Recovery/overview) &mdash; the archives the position data came from
* [Erika's erased flight logs](/Planes/Erika-Flight-Logs-Erased) &mdash; why her side cannot be checked
""")

os.makedirs(CUTS, exist_ok=True)
with open(os.path.join(CUTS, "overview.mdx"), "w", encoding="utf-8") as f:
    f.write("".join(body))

with open(os.path.join(CUTS, "_category_.json"), "w", encoding="utf-8") as f:
    json.dump({"label": "Table drill-downs", "position": 5, "collapsed": True,
               "link": {"type": "doc", "id": "Planes/following/cuts/overview"}}, f, indent=2)
print("hub written,", len(flat), "slices indexed")
