# DATA BRIEF — recovered-flight-data investigation (built 2026-08-28)

REPO = /Users/bryanstarbuck/BGit/Bryan_git/charlie-kirk
PLANES = $REPO/site/docs/Planes
CODE = $PLANES/following/apis/public_open_source/code
ANALYSIS = $PLANES/following/apis/public_open_source/data/analysis

## Raw data already on disk (DO NOT fetch from the internet — mine what is here)

1. PER-TAIL RECOVERED TRACES — $PLANES/<TAIL>/data/recovered/
   20,437 `.meta.json` files. 4,478 have a payload beside them; the rest are
   `.miss.` records meaning "the archive was ASKED and had nothing".
   Payload files are `<TAIL>_<DATE>_<source>_trace_full.json[.gz]`.
   `.json` and `.json.gz` are the SAME evidence — gunzip -c reads either.
   Sources: airplanes-live (2308), adsb-lol (1895), adsbexchange-samples (207),
   wayback/flightaware (28), wayback/flightradar24 (22),
   flightaware-activity-log (16), adsblol-github-backup (2).

2. TRACE VISIT INDEX — .../data/recovery/trace_visit_index.json (17 MB)
   17 tails x 2,235 tail-days, 6,429 airport GROUND VISITS already extracted,
   each with airport code, median km from the field, ground point count, and
   first/last UTC. This is the master flight record. Read it, do not rebuild it.

3. GEOGRAPHIC SWEEP — .../data/geo_sweep/<YYYY-MM-DD>/hits.csv.gz + _sweep.meta.json
   278 UTC day-directories, 1,772,543 aircraft-circle rows. Asks WHAT WAS THERE,
   not where one named tail was. 233 SWEPT, 28 TRUNCATED, 9 NO_RELEASE, 8 PROBE_UNRESOLVED.
   Six CONTROL cities swept on the same days in the same run.

4. GEO SWEEP SAMPLES — .../data/geo_sweep_samples/ (2022-04-01, 2022-06-01, 2022-12-01)
   The only free archive reaching before 2023. One day per month.

## Derived files built for this run (READ THESE FIRST)

* $ANALYSIS/master_proximity.csv — 4,214 ground visits joined to sourced
  Charlie/Erika/TPUSA events. 137 are within 50 miles of an event city +/-1 day.
  Built by $CODE/build_master_proximity.py.
* $ANALYSIS/recovery_ledger.csv — 10,104 (tail, UTC day) rows. Verdicts:
  BOTH_HAVE_IT 1692, ONLY_ON_AIRPLANES_LIVE 182, ONLY_ON_ADSB_LOL 10,
  NEITHER_HAS_IT 7869, HELD_BY_AIRPLANES-LIVE 191,
  HELD_BY_ADSBEXCHANGE-SAMPLES 153. Built by $CODE/build_recovery_ledger.py.
* $ANALYSIS/geo_ground_foreign.csv — 17,266 rows: every non-US / unregistered /
  military / PIA / LADD aircraft ON THE GROUND inside an event circle.
* $ANALYSIS/geo_rates.csv — event vs control base rates.
* $ANALYSIS/geo_recurrence.csv — 857 aircraft on the ground near 2+ events in
  2+ states, with `control_contaminated` marking the ones that also turn up
  near a control city (a busy charter, not a shadow).
* Built by $CODE/build_geo_findings.py.

## HEADLINE FACTS ALREADY ESTABLISHED (verify before reusing; cite the file)

A. GEOGRAPHIC SWEEP, blind to tail numbers, across 187 sourced event-days and
   1.77 M aircraft-circle rows: Egyptian-registered aircraft on the ground
   inside a 50-mile event circle appear EXACTLY THREE TIMES —
     2025-09-09  SU-BND (GLF4)  Provo KPVU 0.8 mi   Orem UT, day-1
     2025-09-10  SU-BND (GLF4)  Provo KPVU 0.8 mi   Orem UT, day-0
     2025-09-10  SU-BTT (FA7X)  Provo KPVU 0.8 mi   Orem UT, day-0
   This CONFIRMS the single most important claim and does not reproduce a
   "73 times" pattern anywhere in the swept range.
B. The control cities catch SU-BTT and SU-BTU over Des Moines at 24,000–41,000 ft,
   NOT on the ground — transit, not presence. That distinction is the finding.
C. RECOVERY LEDGER: 182 aircraft-days exist on airplanes.live where adsb.lol
   returned nothing. 88 of those fall inside adsb.lol's known 403 band
   (2025-10-12 onward) — an ARCHIVE fact, never suppression. 81 fall outside
   the band on case aircraft, and 10 fall outside the band ON THE CONTROL
   AIRLINERS, which is the background rate.
D. Per-tail AL-only rate: controls 2.5% / 4.0%; case aircraft 9.6%–72.4%.
   CONFOUND THAT MUST BE STATED: both controls are scheduled airliners in dense
   European receiver coverage. An airliner is heard by everyone. This is a weak
   control for a private jet and the difference is at least partly coverage.

## THE RULES (from $REPO/CLAUDE.md — non-negotiable)

* NEVER call something a removal until a control failed the same way.
* Removal vs retention vs coverage gap — say which, every time.
* An absence is NOT a finding. 404 = a volunteer network heard nothing.
* A trace proves presence, never purpose, never occupancy. No backup anywhere
  produces Erika Kirk's itinerary.
* Publish the result that WEAKENS the claim as prominently as the one that supports it.
* Scope a claim to what was actually checked.
* Never assert intent.
* Living people: attribution, no crime stated as fact.
* Every `<div>` and `</div>` at column 0 or the Docusaurus build breaks.
