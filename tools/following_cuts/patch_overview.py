#!/usr/bin/env python3
"""Link every count cell in following/overview.mdx down to its drill-down page.

Each replacement is an EXACT substring that must appear EXACTLY ONCE. The script
refuses to write if any of them is missing or ambiguous, so it cannot silently
half-apply and cannot be run twice into a mess.
"""
import os, sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
P = os.path.join(ROOT, "site/docs/Planes/following/overview.mdx")
C = "./cuts/"

R = [
 # ---- table 1: "The question people actually ask"
 ("| **Overlaps with an Egyptian-registered jet, all told** | **85** |",
  f"| **[Overlaps with an Egyptian-registered jet, all told]({C}all-85)** | **[85]({C}all-85)** |"),
 ("| &nbsp;&nbsp;of which carry a date at all | 80 |",
  f"| &nbsp;&nbsp;[of which carry a date at all]({C}dated-80) | [80]({C}dated-80) |"),
 ("| &nbsp;&nbsp;of which were never published — no date, city, airport or tail | 5 |",
  f"| &nbsp;&nbsp;[of which were never published — no date, city, airport or tail]({C}never-published-5) | [5]({C}never-published-5) |"),
 ("| **Overlaps with Charlie Kirk where Erika is *not* claimed with him** | **9** |",
  f"| **[Overlaps with Charlie Kirk where Erika is *not* claimed with him]({C}charlie-only-9)** | **[9]({C}charlie-only-9)** |"),
 ("| **Overlaps claiming Charlie *and* Erika together** | **9** |",
  f"| **[Overlaps claiming Charlie *and* Erika together]({C}charlie-and-erika-9)** | **[9]({C}charlie-and-erika-9)** |"),
 ("| **Overlaps involving Charlie at all** (9 + 9) | **18** |",
  f"| **[Overlaps involving Charlie at all]({C}charlie-any-18)** (9 + 9) | **[18]({C}charlie-any-18)** |"),
 ("| **Overlaps involving Erika at all** (61 alone + the 9 shared) | **70** |",
  f"| **[Overlaps involving Erika at all]({C}erika-any-70)** (61 alone + the 9 shared) | **[70]({C}erika-any-70)** |"),
 ("| **Overlaps where Erika is claimed and Charlie is not** | **61** |",
  f"| **[Overlaps where Erika is claimed and Charlie is not]({C}erika-only-61)** | **[61]({C}erika-only-61)** |"),
 ("| **Overlaps at a Turning Point event where neither Kirk is claimed present** | **6** |",
  f"| **[Overlaps at a Turning Point event where neither Kirk is claimed present]({C}tpusa-no-kirk-6)** | **[6]({C}tpusa-no-kirk-6)** |"),
 ("| **Overlaps where the aircraft was [SU-BTT](/Planes/SU-BTT/overview), the yellow plane** | **57** |",
  f"| **Overlaps where the aircraft was [SU-BTT](/Planes/SU-BTT/overview), the yellow plane** | **[57]({C}tail-su-btt-57)** |"),
 ("| **Overlaps where the aircraft was [SU-BND](/Planes/SU-BND/overview), the blue plane** | **16** |",
  f"| **Overlaps where the aircraft was [SU-BND](/Planes/SU-BND/overview), the blue plane** | **[16]({C}tail-su-bnd-16)** |"),
 ("| **Overlaps naming both tails on the one row** | **3** |",
  f"| **[Overlaps naming both tails on the one row]({C}tail-both-3)** | **[3]({C}tail-both-3)** |"),
 ('| **Overlaps where even the tail number is unresolved** | **9** — 5 logged as "SU-BTT or SU-BND", 4 with no tail at all |',
  f'| **[Overlaps where even the tail number is unresolved]({C}tail-unresolved-9)** | **[9]({C}tail-unresolved-9)** — [5 logged as "SU-BTT or SU-BND"]({C}tail-either-btt-or-bnd-5), [4 with no tail at all]({C}tail-none-4) |'),

 # ---- table 2: "Under that rule"
 ("| **Overlaps where Erika Kirk's presence is established** | **0** |",
  f"| **[Overlaps where Erika Kirk's presence is established]({C}erika-established-0)** | **[0]({C}erika-established-0)** |"),
 ("plus the 9 claimed with Erika, where Charlie is the half that is documented | **18** |",
  f"plus the 9 claimed with Erika, where Charlie is the half that is documented | **[18]({C}charlie-any-18)** |"),
 ("| **Overlaps involving Charlie Kirk** — the 9 where he is claimed alone,",
  f"| **[Overlaps involving Charlie Kirk]({C}charlie-any-18)** — the 9 where he is claimed alone,"),
 ("| **Overlaps at a Turning Point event with neither Kirk present** | **6** |",
  f"| **[Overlaps at a Turning Point event with neither Kirk present]({C}tpusa-no-kirk-6)** | **[6]({C}tpusa-no-kirk-6)** |"),
 ("| **Rows where no Kirk can be placed at all** | **61** |",
  f"| **[Rows where no Kirk can be placed at all]({C}no-kirk-placeable-61)** | **[61]({C}no-kirk-placeable-61)** |"),
 ("| | **85** |\n",
  f"| | **[85]({C}all-85)** |\n"),

 # ---- table 3: the ADS-B verdicts
 ("| **At the claimed airport** | **25** |",
  f"| **[At the claimed airport]({C}adsb-at-claimed-airport-25)** | **[25]({C}adsb-at-claimed-airport-25)** |"),
 ("| **Elsewhere** | **3** |",
  f"| **[Elsewhere]({C}adsb-elsewhere-3)** | **[3]({C}adsb-elsewhere-3)** |"),
 ("| Right area, wrong field | 1 |",
  f"| [Right area, wrong field]({C}adsb-same-metro-1) | [1]({C}adsb-same-metro-1) |"),
 ("| Not heard | 37 |",
  f"| [Not heard]({C}adsb-not-heard-37) | [37]({C}adsb-not-heard-37) |"),
 ("| No archive coverage | 10 |",
  f"| [No archive coverage]({C}adsb-no-archive-coverage-10) | [10]({C}adsb-no-archive-coverage-10) |"),
 ("| No aircraft named | 4 |",
  f"| [No aircraft named]({C}adsb-no-tail-4) | [4]({C}adsb-no-tail-4) |"),
 ("| No date named | 5 |",
  f"| [No date named]({C}adsb-no-date-5) | [5]({C}adsb-no-date-5) |"),

 # ---- table 4: the two ledgers
 ("| **Charlie Kirk + TPUSA** | 24 | **13** | **0** | 8 (+3 name no aircraft) |",
  f"| **[Charlie Kirk + TPUSA]({C}ledger-charlie-tpusa-24)** | [24]({C}ledger-charlie-tpusa-24) | "
  f"**[13]({C}ledger-charlie-corroborated-13)** | **[0]({C}ledger-charlie-refuted-0)** | "
  f"[8 (+3 name no aircraft)]({C}ledger-charlie-undecided-11) |"),
 ("| **Erika Kirk** | 56 | 12 | 3 | 39 (+1 names no aircraft) |",
  f"| **[Erika Kirk]({C}ledger-erika-56)** | [56]({C}ledger-erika-56) | "
  f"[12]({C}ledger-erika-corroborated-12) | [3]({C}ledger-erika-refuted-3) | "
  f"[39 (+1 names no aircraft)]({C}ledger-erika-undecided-41) |"),

 # ---- table 6: who the sheet claims was there
 ("| **Erika Kirk alone** | **61** | **72%** |",
  f"| **[Erika Kirk alone]({C}erika-only-61)** | **[61]({C}erika-only-61)** | **72%** |"),
 ("| **Charlie Kirk alone** | **9** | 11% |",
  f"| **[Charlie Kirk alone]({C}charlie-only-9)** | **[9]({C}charlie-only-9)** | 11% |"),
 ("| **Both Kirks together** | **9** | 11% |",
  f"| **[Both Kirks together]({C}charlie-and-erika-9)** | **[9]({C}charlie-and-erika-9)** | 11% |"),
 ("| **A TPUSA event, neither Kirk present** | **6** | 7% |",
  f"| **[A TPUSA event, neither Kirk present]({C}tpusa-no-kirk-6)** | **[6]({C}tpusa-no-kirk-6)** | 7% |"),
 ("| **Total claimed overlaps** | **85** | |",
  f"| **[Total claimed overlaps]({C}all-85)** | **[85]({C}all-85)** | |"),

 # ---- table 7: the tracking-site audit
 ("| **Accurate** — the jet really was there that day | **18** |",
  f"| **[Accurate]({C}audit-accurate)** — the jet really was there that day | **[18]({C}audit-accurate)** |"),
 ("| **Inaccurate** — the jet was somewhere else, usually another continent | **44** |",
  f"| **[Inaccurate]({C}audit-inaccurate)** — the jet was somewhere else, usually another continent | **[44]({C}audit-inaccurate)** |"),
 ("| Partially accurate — right aircraft and date, wrong route or duration | 5 |",
  f"| [Partially accurate]({C}audit-partial) — right aircraft and date, wrong route or duration | [5]({C}audit-partial) |"),
 ("| Not assessable — the flight archive does not reach back that far | 2 |",
  f"| [Not assessable]({C}audit-archive-gap) — the flight archive does not reach back that far | [2]({C}audit-archive-gap) |"),
 ("| **Never published** — a number with no date, city, airport or tail attached | **5** |",
  f"| **[Never published]({C}never-published-5)** — a number with no date, city, airport or tail attached | **[5]({C}never-published-5)** |"),
 ("| Not reached by the audit | 4 |",
  f"| [Not reached by the audit]({C}audit-not-reached) | [4]({C}audit-not-reached) |"),

 # ---- table 8: which Egyptian plane
 ("| **[SU-BTT](/Planes/SU-BTT/overview)** — the \"yellow plane\", Dassault Falcon 7X, hex `0101D3` | **57** | **10** | 46 | 5 |",
  f"| **[SU-BTT](/Planes/SU-BTT/overview)** — the \"yellow plane\", Dassault Falcon 7X, hex `0101D3` | **[57]({C}tail-su-btt-57)** | **10** | 46 | 5 |"),
 ("| **[SU-BND](/Planes/SU-BND/overview)** — the \"blue plane\", Gulfstream 4SP, hex `01003E` | **16** | **3** | 16 | 0 |",
  f"| **[SU-BND](/Planes/SU-BND/overview)** — the \"blue plane\", Gulfstream 4SP, hex `01003E` | **[16]({C}tail-su-bnd-16)** | **3** | 16 | 0 |"),
 ("| **Both tails named on the one row** | **3** | **2** | 2 | 1 |",
  f"| **[Both tails named on the one row]({C}tail-both-3)** | **[3]({C}tail-both-3)** | **2** | 2 | 1 |"),
 ('| *"SU-BTT or SU-BND"* — the source could not tell which | 5 | 0 | 5 | 0 |',
  f'| [*"SU-BTT or SU-BND"* — the source could not tell which]({C}tail-either-btt-or-bnd-5) | [5]({C}tail-either-btt-or-bnd-5) | 0 | 5 | 0 |'),
 ("| No tail number recorded at all | 4 | 3 | 1 | 0 |",
  f"| [No tail number recorded at all]({C}tail-none-4) | [4]({C}tail-none-4) | 3 | 1 | 0 |"),
 ("| **Total** | **85** | **18** | **70** | **6** |",
  f"| **Total** | **[85]({C}all-85)** | **[18]({C}charlie-any-18)** | **[70]({C}erika-any-70)** | **[6]({C}tpusa-no-kirk-6)** |"),

 # ---- table 9: the geographic view
 ("| **Nebraska** | Omaha (KOMA), Lincoln (KLNK) |",
  f"| **[Nebraska]({C}state-nebraska)** | [Omaha (KOMA), Lincoln (KLNK)]({C}state-nebraska) |"),
 ("| **Kansas** | Wichita (KICT) |",
  f"| **[Kansas]({C}state-kansas)** | [Wichita (KICT)]({C}state-kansas) |"),
 ("| **Delaware** | Wilmington (KILG) |",
  f"| **[Delaware]({C}state-delaware)** | [Wilmington (KILG)]({C}state-delaware) |"),
 ("| **Missouri** | St. Louis (KSTL, KCPS, KSUS) |",
  f"| **[Missouri]({C}state-missouri)** | [St. Louis (KSTL, KCPS, KSUS)]({C}state-missouri) |"),
 ("| **Utah** | Provo (KPVU) |",
  f"| **[Utah]({C}state-utah)** | [Provo (KPVU)]({C}state-utah) |"),

 # ---- prose figures that now have a page behind them
 ("**Ten of the twenty-five corroborations are the strongest evidence class available**",
  f"**[Ten of the twenty-five corroborations]({C}ground-confirmed-10) are the strongest evidence class available**"),
 ("**17 — across 12 distinct dates** — fall within three days of a Turning Point or Charlie Kirk appearance this site can independently source in the same state",
  f"**[17 — across 12 distinct dates]({C}within-three-days-17)** — fall within three days of a Turning Point or Charlie Kirk appearance this site can independently source in the same state"),
 ("and 11 rows resolving to only **six dates** survive a same-day-or-adjacent test at a shared field",
  f"and [11 rows resolving to only **six dates**]({C}same-day-sourced-event-10) survive a same-day-or-adjacent test at a shared field"),
]

s = open(P, encoding="utf-8").read()
bad = []
for old, new in R:
    n = s.count(old)
    if n != 1:
        bad.append(f"{n} matches: {old[:110]}")
if bad:
    print("REFUSING TO WRITE — %d anchors not unique:" % len(bad))
    for b in bad:
        print("  " + b)
    sys.exit(1)
for old, new in R:
    s = s.replace(old, new, 1)

# a pointer to the hub, right under the first counts table
anchor = "**Two columns, because rows and events are not the same thing"
assert s.count(anchor) == 1
s = s.replace(anchor, (
    "**Every count in every table on this page now opens.** Click a row label or a number and it "
    f"lands on a page listing the specific rows behind it — which aircraft, which airport, what date "
    f"it arrived and what date it left, who it is claimed to have been following, and every verdict "
    f"passed on that row. The index of all of them is [Table drill-downs]({C}overview).\n\n" + anchor), 1)

open(P, "w", encoding="utf-8").write(s)
print(f"patched {len(R)} cells + 1 pointer paragraph into overview.mdx")
