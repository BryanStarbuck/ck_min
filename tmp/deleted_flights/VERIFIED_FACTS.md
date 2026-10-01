# VERIFIED FACTS — re-derived directly from the raw traces on 2026-08-28

Every number below was computed from the payload files, not from a page, not
from a summary, and not from an agent's report. Where two archives hold the same
aircraft-day, both were decoded and they agree. Cite the file path, not this
document.

TOOLS (all under .../apis/public_open_source/code/, all offline):
  build_master_proximity.py   build_recovery_ledger.py   build_geo_findings.py
  build_flight_legs.py        coverage_percent.py        normalise_event_control.py
  ingest_sweep_traces.py      union_su_presence.py       test_prefilter.py
DERIVED CSVs (all under .../apis/public_open_source/data/analysis/):
  master_proximity.csv  recovery_ledger.csv  flight_legs.csv  geo_ground_foreign.csv
  geo_rates.csv  geo_recurrence.csv  su_presence_union.csv  circle_day_counts.json

================================================================================
F1. COVERAGE, WITH THE DENOMINATOR NAMED EVERY TIME
================================================================================
Event window = the 363 UTC days that are a sourced Charlie/Erika/TPUSA event
date +/-1, inside 2022-01-01..2025-12-31.

  Foreign fleet (SU-BTT/BND/BTU/BTV/BGM + T7-ELL): 195 / 2,178 = 8.95%. NEVER
    ASKED: 0. Every day has been put to every free archive that exists.
  US / Kirk-associated fleet (10 tails):           805 / 3,630 = 22.18%
  Control airliners:                               149 /   726 = 20.52%
  By year, foreign fleet: 2022 0.43%, 2023 9.26%, 2024 11.06%, 2025 13.11%
  GEOGRAPHIC SWEEP coverage of the same window:    261 / 363   = 71.90%
    2022 0.00%, 2023 82.72%, 2024 98.02%, 2025 92.23%
  Total aircraft-days held: 2,346. Source split:
    airplanes-live 2,072 (371 unique) | adsb-lol 1,702 (10 unique)
    adsbexchange-samples 207 (153 unique) | adsblol-github-backup 113 (111 unique)
    OPEN SOURCE 100%. PROPRIETARY/PAID 0% — no credential is held.
  Page-archive lane, counted in PAGES not aircraft-days: 66 captures
    (28 wayback/flightaware, 22 wayback/flightradar24, 16 flightaware-activity-log)

================================================================================
F2. THE INGEST THAT RAISED THE NUMBER (data already on disk, no network)
================================================================================
The sweep filed tracked-tail traces under the DATE; the per-tail lane looks under
the TAIL. 111 aircraft-days were uncounted. ingest_sweep_traces.py copies them
across (never moves, never shadows a direct pull, writes the same .meta.json).
  N1098L event-window coverage 4.68% -> 19.28%   (+53 days)
  N2100L                       2.75% -> 15.15%   (+45 days)
  N59906                       3.31% ->  6.89%   (+13 days)
  US fleet total              19.12% -> 22.18%
  Foreign fleet: UNCHANGED — every sweep trace for an Egyptian tail had already
  been pulled directly, which is a useful cross-check that the lanes agree.

================================================================================
F3. THE UNION — EVERY FOREIGN-FLEET GROUND PRESENCE NEAR A SOURCED EVENT
================================================================================
50 miles, event date +/-1. su_presence_union.csv. FOUR ROWS, TWO DATES, ONE FIELD:
  2024-04-23  SU-BTT  FA7X  KPVU 0.36 mi   Salt Lake City UT  day 0   per-tail only
  2025-09-09  SU-BND  GLF4  KPVU 0.80 mi   Orem UT            day -1  BOTH ROUTES
  2025-09-10  SU-BND  GLF4  KPVU 0.80 mi   Orem UT            day  0  BOTH ROUTES
  2025-09-10  SU-BTT  FA7X  KPVU 0.80 mi   Orem UT            day  0  BOTH ROUTES
Both Charlie-only. This reproduces, from raw ADS-B, the same two dates this
repo's own strict and loose overlap tests already returned across 139 events.

================================================================================
F4. THE BLIND GEOGRAPHIC SWEEP — SU-REGISTERED AIRCRAFT ON THE GROUND
================================================================================
1,772,543 aircraft-circle rows, 348 event circle-days, 153,613 aircraft on the
ground in an event circle. SU-registered ON THE GROUND in an event circle: 5.
  2023-03-22 SU-GDN B77W KJFK New Brunswick NJ  <- EGYPTAIR SCHEDULED SERVICE
  2025-01-21 SU-GET B789 KIAD Washington DC     <- EGYPTAIR SCHEDULED SERVICE
  2025-09-09 SU-BND GLF4 KPVU Orem UT
  2025-09-10 SU-BND GLF4 KPVU Orem UT
  2025-09-10 SU-BTT FA7X KPVU Orem UT
In CONTROL circles: 0.
Strip the two airliners: three business-jet presences, all Provo, 9-10 Sep 2025.
THIS IS A FLOOR, NOT A TOTAL — see F8.

CONTROL-CIRCLE HITS BY THE SAME TAILS ARE OVERFLIGHTS, NOT PRESENCE:
  SU-BTU over Des Moines 2025-04-24 at 24,000 ft and 2025-04-30 at 39,000 ft
  SU-BTT over Des Moines 2025-08-23 at 41,000 ft and 2025-09-10 at 41,000 ft
A circle entry is not an airport visit. That distinction is the finding.

================================================================================
F5. NORMALISATION — THE NAIVE RATIO DOES NOT SURVIVE
================================================================================
Naive: event circles 49.61 notable aircraft per circle-day, control 8.54 = 5.81x.
WORTHLESS: event circles are Phoenix/Dallas/Las Vegas, controls are Des Moines/
Shreveport. That ratio measures airport size.
N1 per aircraft ON THE GROUND: event 17,266/153,613 = 11.24%; control
  6,727/51,006 = 13.19%. RATIO 0.85x — event circles are LOWER.
N2 size-matched buckets (aircraft on ground per circle-day): 0.79, 0.86, 1.15,
  1.37, 0.99. Flat in every bucket that has both.
NO aggregate excess of foreign/unregistered/military/blocked aircraft near
Charlie Kirk's events survives a size-matched control.

================================================================================
F6. THE RECOVERY LEDGER — 10,215 (tail, UTC day) rows
================================================================================
  BOTH_HAVE_IT 1,692 | ONLY_ON_AIRPLANES_LIVE 182 | ONLY_ON_ADSB_LOL 10
  NEITHER_HAS_IT 7,869 (asked, and the archive had nothing)
  HELD_BY_AIRPLANES-LIVE 191 (adsb.lol NEVER ASKED — not the same thing)
  HELD_BY_ADSBEXCHANGE-SAMPLES 153 | HELD_BY_ADSBLOL-GITHUB-BACKUP 111
adsb.lol has TWO SITE-WIDE HOLES, control-tested, both archive facts:
  403 for EVERY aircraft 2025-10-12 -> ~2025-12-30
  404 for EVERY aircraft ~2025-12-31 -> ~2026-08-01
318 aircraft-days were recovered from inside those holes (281 airplanes.live,
29 ADSBX samples, 7 both, 1 GitHub backup). 210 of them are 2026. 41 are the
Egyptian fleet + T7-ELL. REAL RECOVERY, and a RETENTION BOUNDARY, not suppression.

THE RESIDUE, and it is the decisive test:
  81 case aircraft-days survive as "adsb.lol was asked and empty, airplanes.live
  had it", outside both holes. 10 control-airliner days do the same.
  NOT ONE of the 81 puts an aircraft within 50 miles of a sourced event. ZERO.
  Median trace points on days BOTH archives hold: 1,388.
  Median on days ONLY airplanes.live holds: 83. Seventeen times thinner.
  A one-archive day is a BARELY-HEARD day. That is the signature of coverage.

CORRECTED per-tail AL-only rate (only days where BOTH were asked, outside holes):
  controls 2.5% / 2.5% | N560TW 1.2 | N40JD 1.3 | N582MM 1.4 | N888KG 2.6
  N872RA 6.6 | N102DZ 7.8 | N1098L/N2100L/N59906 0.0
  T7-ELL 6.9 | SU-BTU 6.2 | SU-BGM 7.3 | SU-BTT 12.7 | SU-BND 15.9 | SU-BTV 17.1
An earlier draft said 9.6-72.4% — that WRONGLY merged "never asked" with "asked
and empty". Publish the correction.

================================================================================
F7. PROXIMITY BASE RATES — event-proximate days / days observed
================================================================================
  N582MM  53/276 = 19.2%  <- TPUSA-associated Learjet. THE POSITIVE CONTROL.
                             This is what "travels with them" looks like.
  N560TW  15/184 = 8.2  | N40JD 4/78 = 5.1 | N872RA 9/215 = 4.2 | N888KG 3/75 = 4.0
  N2100L   2/59  = 3.4  | N102DZ 4/144 = 2.8 | N59906 1/40 = 2.5 | N1098L 1/62 = 1.6
  SU-BTT   2/19  = 10.5 | SU-BND 2/22 = 9.1   <- TWO EVENTS EACH on a tiny
                             denominator, and both aircraft's two events are the
                             SAME two dates at the SAME field. Not a rate.
  SU-BTU 0/15, SU-BTV 0/16, SU-BGM 0/9, T7-ELL 0/76 = ZERO. NEVER.
  Controls 0/169, 0/163 — a NULL control for any US question. They fly in Europe.

================================================================================
F8. TWO DEFECTS IN OUR OWN CODE, FOUND AND FIXED — PUBLISH THESE
================================================================================
D1 NEGATIVE-LONGITUDE PRE-FILTER BUG (geo_sweep.py, fixed 2026-08-28).
   math.floor(-111.73) = -112, but a trace file PRINTS "-111.73". Tokens built
   with floor() shifted every western-hemisphere band one degree west, so the
   EASTERN EDGE of every US circle was never examined: 28.7% of each event
   circle's area on average, 20.1% for controls, 50.9% for Salt Lake City.
   PROVEN MISS: SU-BTT on the ground at Provo 2024-04-23, 39.7 mi inside the SLC
   circle, 53 ground points at median 0.58 km — the per-tail route holds it in
   full, which is how the defect was caught rather than shipped.
   NOT A REMOVAL. adsb.lol served the day; the tarball downloaded whole.
   BIAS DIRECTION: event circles were MORE blind than controls. The defect
   suppressed the pattern-supporting side.
   FIXED via _printed_int_parts(); locked by test_prefilter.py (6,000 random
   circles x 12 interior points, plus the Provo point asserted directly).
   UNTIL THE SWEEP IS RE-RUN, EVERY SWEEP-ONLY COUNT IS A FLOOR.
D2 GOVERNMENT-OPERATOR FALSE POSITIVES. Substring matching flagged FEDERAL
   EXPRESS, EXECUTIVE JET MANAGEMENT and ROYAL AIR as government operators.
   Words removed; the flag is re-derived offline in build_geo_findings.py from
   the own_op column already in every hits row. Also: the airliner exclusion set
   was missing BCS1/BCS3, B712, E135/E145 and the regional Embraers.
D3 CONTROL-SET FLAW. Albuquerque NM is BOTH a control city AND a sourced Charlie
   Kirk event city (30 Nov 2022, University of New Mexico), and supplies 102 of
   186 control-city recurrence touches. It did NOT contaminate the measurements:
   the sweep's earliest successfully swept day is 2023-03-10, fifteen months
   after that event. Any future sweep reaching into 2022 must drop it.

================================================================================
F9. THE SEPTEMBER 2025 PROVO RECORD, FROM THE RAW TRACES
================================================================================
SU-BND sat at Provo CONTINUOUSLY 5 -> 12 September 2025. Every fix from 6 to 12
September is at the SAME distance from the field reference point, 1.29 km,
unchanged across eight days. It was parked before Charlie Kirk arrived and still
parked two days after he was killed.

CORRECTION — SU-BND DID NOT TAKE OFF ON 10 SEPTEMBER 2025. Derived metadata on
this site records a wheels-up. The raw trace says otherwise and BOTH archives
agree to the point: of 257 position points that day, 256 report ON GROUND. The
one that does not is the LAST fix of the day, 20:29:19 UTC, reporting 4,525 ft
at the same position it held all day. KPVU field elevation is 4,497 ft. That is
a barometric reading on the ramp, not a departure.

SU-BTT on 10 September: on the ground at Provo 13:07:53 -> 13:13:16 UTC, first
airborne fix 13:14:03.82 UTC = 07:14:03 MDT. Last tracked on approach to
Wilmington DE 16:50:37 UTC. It left roughly five hours BEFORE the shooting.

SU-BND RETURNED TO PROVO IN 2026: ground presences 2026-05-13, 05-14, 05-20,
06-02, 06-04. Those five days exist ONLY on airplanes.live, because adsb.lol
serves nothing for any 2026 date. Without the second archive this investigation
would not know the aircraft came back.

30 foreign-fleet ground visits at KPVU in total, 2024-04-19 through 2026-06-04.

================================================================================
F10. N59906 — THE SURVEY AIRCRAFT, SETTLED
================================================================================
Piper PA-31 Navajo, MARC Inc. Raw trace, identical in both archives:
  09:08:45 MDT  on the ground at Provo (KPVU), 0.3 km from the field
  09:28:53 MDT  airborne, climbing
  09:54-11:41   LEVEL AT 19,000 FT, flying long parallel lines across a block
                spanning the Utah Valley and out over Tooele County
  11:10/11:25/11:35  passes 3.8-4.5 km from UVU — AT 19,000 FEET, on a survey line
  11:46-12:01   descending
  12:07:46 MDT  ON THE GROUND at Provo again, 0.3 km from the field
  ~12:20 MDT    the shooting
It landed roughly TWELVE MINUTES BEFORE the shooting. Constant 19,000 ft, long
parallel legs, a wide rectangular block, return to the launch field = a standard
aerial-mapping grid. It passed near UVU because UVU sits INSIDE the survey block.
Publishing the near-UVU distances without the altitude, the grid and the landing
time would be a serious misrepresentation.

================================================================================
F11. N708JH — AN OPEN QUESTION ON THIS SITE, ANSWERED
================================================================================
The N708JH page asks "Did N708JH operate into Utah at any point in September
2025?" The sweep answers YES. 2019 Gulfstream G550, registered UNITED STATES
GOVERNMENT, DEPARTMENT OF JUSTICE. Hex a97316.
  2025-09-11  KPVU Provo      0.0 mi  565 ground fixes  15:21-17:37 UTC  day +1
  2025-09-21  KSDL Scottsdale 0.1 mi  304 fixes         18:58-19:09 UTC  day  0
  2025-09-22  KSDL Scottsdale 0.3 mi  240 fixes         00:16-00:29 UTC  day +1
  2023-10-03  KSJC San Jose   0.3 mi  146 fixes                          day +1
THE ORDINARY EXPLANATION FITS COMPLETELY: a federal aircraft at the scene of a
federal investigation the day after, and at a national memorial service. The SAME
2023-10-03 sweep row also puts it on the ground at ALBUQUERQUE, a control city,
the same day. This aircraft goes everywhere. That is the correct frame.

================================================================================
F12. N1098L / N2100L — THE THREE NEW PROXIMITY EVENTS AND THEIR BASE RATE
================================================================================
Bombardier Global 6500s, LASAI Aviation II LLC. In the recovered traces they
transmit ONLY the callsigns AXEL10 and AXEL21. Dominant ground field for both is
BIGGS ARMY AIRFIELD (KBIF), Fort Bliss — 28 and 25 days, more than any other.
Visible only because of the F2 ingest:
  2024-09-04  N2100L  KMSN Madison WI      5.4 mi   day +1
  2024-12-18  N1098L  KPHX Phoenix         10.8 mi  day +1
  2025-08-08  N2100L  KLGB Long Beach CA   13.7 mi  day -1
AND THE BASE RATE SAYS THIS IS NOT A PATTERN: 1.6% and 3.4% of their observed
ground-visit days, at or BELOW the ordinary Kirk-side jets (2.8-8.2%) and far
below the TPUSA Learjet's 19.2%. Record them. Do not build on them.

================================================================================
STANDING RULES — a page that breaks one of these does not ship
================================================================================
* Removal vs retention boundary vs coverage gap. Say which, every time.
* An absence is NOT a finding. A .miss record means a volunteer network heard
  nothing: transponder off, out of coverage, or a wrong claimed date.
* A trace proves PRESENCE, never purpose, never occupancy. Nothing here places
  any person aboard any aircraft. No archive produces Erika Kirk's itinerary.
* Publish what weakens the claim as prominently as what supports it.
* Scope a claim to what was actually checked, and carry the F8-D1 FLOOR caveat
  on every sweep-only number.
* Never assert intent or tasking. Attribute; never state a crime as fact.
* Tallies (65/68/70/72/73/77) are trackers' counts, never records. Show the
  conflict; never average it.
* Erika's side is the weak side — say so on every Erika pairing and link
  /Planes/Erika-Flight-Logs-Erased.
* Do not merge the threads: the 18-month following pattern, the Sept 10 day-of
  timeline, the N1098L/LASAI thread and the N888KG departure are four claims.
* MDX: every <div> and </div> at column 0.
