# Flight Data Recovery Runbook

Moved verbatim out of {ROOT_DIR}/CLAUDE.md on 2026-09-24 to keep that file small. ROOT_DIR = ~/BGit/Bryan_git/charlie-kirk.

=== Planes / Flight Data ===

DIR:
* site/docs/Planes/{TAIL}/: One directory per aircraft. overview.mdx plus a
  data/ subdir (e.g. N1098L/data/adsb/) holding the RAW downloads. Filenames
  must record WHICH SOURCE the data came from, so deletions can be proven.
* site/docs/Planes/following/: The public page-per-location follow log. Governed
  by its own CLAUDE.md.
* site/docs/Planes/following/speaking/: One .mdx per Charlie speaking event,
  named {YYYYMMDD}_{city}.mdx.
* site/docs/Planes/following/overlap/: One directory per plane/person overlap,
  named {YYYYMMDD}_{ST}_{city}_{person}_{NNN}.
* site/docs/Planes/following/apis/: Four data-source lanes — government/,
  proprietary/, public_open_source/, browser_capture/ — each with knowledge.mdx
  (what this source is and what it holds), p_get_data.mdx (the prompt that pulls
  from it), code/, data/, and where applicable requests/ or captures/.
* site/docs/Planes/Aircraft-Costs/, site/docs/Planes/LASAI-Fleet/,
  site/docs/Planes/TPUSA-Aircraft/: Cross-cutting Planes pages — cost analysis,
  the LASAI Aviation II fleet, and TPUSA's own aircraft.

FILE:
* site/docs/Planes/following/flights.csv: The flight records themselves.
* site/docs/Planes/following/overlaps.csv: Computed plane/person overlaps.
* site/docs/Planes/following/airports.csv: Airport reference table.
* site/docs/Planes/following/tpusa_events.csv: TPUSA event dates and locations —
  the ground truth the flights are matched against.
* site/docs/Planes/following/planes.csv: The following-specific plane list
  (distinct from the root planes.csv, which drives autolinking).
* site/docs/Planes/following/Overlap_Window_Definition.mdx: Defines exactly what
  counts as an "overlap". Read it before computing or disputing one.


=== Generated Plane Pages (added 2026-08-28) ===

Most of what a reader sees under `/Planes/` is now GENERATED from the recovered
ADS-B data rather than written by hand. Every generator writes ONLY between its
own markers, so all of them are idempotent and safe to re-run.

DIR:
* site/docs/Planes/Airports/: **NEW page type.** One page per airport (290) that
  a case aircraft was on the ground at, or flew a recovered leg into or out of.
  Each carries the field's identity, every recovered ground visit with times,
  every leg, and the sourced events near it. Control-airliner-only fields get NO
  page on purpose — the controls test the archives, they are not case record.
* site/docs/Planes/Incidents/: **NEW page type.** One page per (tail, UTC date,
  field) ground contact within 50 miles of a sourced event — 147 contacts across
  110 pages. Several ground segments on one day at one field are ONE page with
  both segments, never two pages colliding on a filename.

FILE (all under following/apis/public_open_source/code/):
* rebuild_plane_pages.sh: **run this, not the scripts individually.** Order
  matters — the airport and incident pages must exist before any table links to
  them, because links are gated on page existence.
* lib/pagefacts.py: shared fact resolution. Airport identity (case-curated
  airports.csv, then the 85,945-row OurAirports database this pipeline already
  downloaded), date maths, MDX-safe cells, and marker splicing. `ap_link()`
  links an airport ONLY if its page exists.
* build_interesting_dates.py: per-aircraft "interesting dates" table. Writes
  analysis/interesting_dates.json, which every other generator reads.
* build_airport_incident_pages.py: creates the two new page types above.
* build_flight_record.py: per-aircraft "where it actually went" — every
  recovered leg and every airport touched.
* build_following_tables.py: the Charlie-side and Erika-side following tables.
* build_event_aircraft.py: per speaking-event blind-sweep result.
* build_overlap_verdicts.py: the ADS-B verdict on each of the 85 claimed
  overlaps.
* link_new_evidence.py: adds inbound links on every visible page to the airport
  and contact pages that page actually mentions.

THREE TRAPS THESE GENERATORS EXIST TO AVOID. All three were live defects found
while building them, and any future work on this data must not reintroduce them:

* **THE TWO CSVs DISAGREE ON THE SIGN OF THEIR OFFSET COLUMN.**
  `master_proximity.csv` stores `event_date - visit_date`; `geo_ground_foreign.csv`
  stores `sweep_date - event_date`. Reading one as the other turns *the day
  before the assassination* into *the day after*. Never use either column —
  recompute from the dates, which is what `days_between()` is for.
* **`dbflag:LADD` IS NOT SUSPICIOUS.** 12,889 of the ~16,000 rows in
  geo_ground_foreign.csv carry only the FAA's Limiting Aircraft Data Displayed
  privacy flag; at Provo that is mostly flight-school Cessna 172s. Printing the
  raw "notable" count beside a Kirk event would claim ~50 suspicious aircraft
  where ~45 are trainers whose owner filed a routine form. LADD is always broken
  out, labelled ordinary, and excluded from any named table.
* **TWO GROUND SEGMENTS IN A DAY ARE A FLIGHT, NOT A WAIT.** Merging them hides
  it — N59906 on 10 September 2025 is exactly this case. Segments are listed
  separately and the page says what the gap between them means.


================================================================================
== Recovering Deleted / Unavailable Flight Data ==
================================================================================

Flight records in this investigation go missing. Sometimes a tracking site drops
an aircraft. Sometimes an archive's retention window rolls off. Sometimes an API
starts refusing a range of dates. From the outside ALL THREE LOOK IDENTICAL, and
the single most important rule in this section exists because of that:

  **NEVER call something a removal until a control aircraft has failed the same
  way.** Query an airframe with NO connection to this case — e.g. hex 4ca7b5
  (Ryanair) or 3c6444 (Lufthansa) — on the same dates and the same endpoint. If
  the control fails identically, it is the ARCHIVE, not the airframe, and it
  must never be published as suppression. Running this test is what separates a
  retention boundary from a cover-up, and skipping it is how an investigation
  destroys its own credibility on the day somebody checks.

Worked example of that rule paying off, from the 2026-08-24 run: adsb.lol
returns HTTP 403 for every date 2025-10-12 to ~2025-12-15, and HTTP 404 for ALL
of 2026. Both looked like the case aircraft being hidden. Both control aircraft
failed exactly the same way. Neither was suppression. Meanwhile a THIRD thing
that did look like ordinary blocking — the N102DZ FlightRadar24 page — turned
out to be the one real removal. The test does not only protect against false
positives; it tells you where to spend the effort.


=== The method: how to find a backup at all ===

The routine that worked, in order. Do not skip step 1 — the answer is usually
that somebody already mirrors the thing, and it takes one search to find out.

* WEB SEARCH FOR THE MIRROR. Search the archive's own name plus "historical",
  "download", "open data", "github", "samples", "dump". Community ADS-B networks
  publish their archives on purpose and say so in their docs. This is how both
  the GitHub backup and the ADSBX sample archive were found, in one search.
* PROBE SIBLING HOSTS WITH THE SAME URL SHAPE. Most community networks run
  tar1090/readsb, so ONE url shape works across all of them:
      https://<host>/globe_history/YYYY/MM/DD/traces/<last2ofhex>/trace_full_<hex>.json
  Swap the host and re-probe. That is how globe.airplanes.live was found.
* CHECK FOR AN OFF-SITE MIRROR OF THE SAME ORGANISATION. An operator whose live
  API refuses a date may still publish that exact day elsewhere under an open
  licence. adsb.lol does precisely this.
* GO UP A LAYER — FROM THE SENSOR DATA TO THE PAGE. When the numbers are gone,
  the WEB PAGE that displayed them may survive in the Internet Archive. This is
  the only route that recovers WHAT A SITE SAID, and therefore the only route
  that can document a removal at all.
* PROBE THE LIVE URL TOO — BUT IN A REAL BROWSER, AND AGAINST CONTROLS.
  What the public gets from that URL TODAY is half the evidence. **A 403 from a
  script is NOT that evidence.** See "The failure this section already produced"
  below — this is the step that has actually shipped a wrong finding.


=== The failure this section already produced — read this one ===

On 2026-08-24 this investigation published, on a public page, that N102DZ's
FlightRadar24 page "returns HTTP 403 to the public today" and called that
A DOCUMENTED REMOVAL. IT WAS WRONG, and it had to be retracted on the page.

What actually happened: flightradar24.com returns HTTP 403 to ANY scripted
client. Not to that aircraft — to everything, including FR24's OWN HOMEPAGE.
Opened in an ordinary browser the N102DZ page loads fine, HTTP 200, with the
aircraft record intact.

The empty flight table on it is not evidence either. FR24 shows a logged-out
visitor SEVEN DAYS ONLY and says so under the table. A control private jet with
no connection to this case shows the identical empty table on the same day.

Three rules come out of that, and they are the expensive kind:

* THE CONTROL TEST APPLIES TO WEBSITES, NOT JUST TO ARCHIVES. It is easy to
  remember it for adsb.lol and forget it for the tracking site. Same rule.
* NEVER READ AN HTTP STATUS FROM curl AS THE PUBLIC'S EXPERIENCE. Anti-bot
  filters, Cloudflare, and consent walls all return 403/503 to scripts and
  200 to browsers. Confirm in a real browser — that is PASS 4
  (browser_capture/) and it exists precisely for this.
* AN EMPTY TABLE IS A PAYWALL UNTIL PROVEN OTHERWISE. Check what the same
  page shows for a control aircraft before calling emptiness a deletion.

The recovery was still worth doing — the archived copy preserves a 7-day window
that has since rolled past, which no subscription can now reconstruct. But the
HEADLINE was false, and the control test is what caught it. Run it first, not
after publication.


=== Techniques tried, and which ones worked ===

Run 2026-08-24. WORKED, all four are free and need no account:

* globe.airplanes.live/globe_history/... — WORKED, and it is the single biggest
  win. Independent volunteer network, same trace format as adsb.lol, typically
  5-10x MORE data for the same aircraft-day, and it serves the whole 403 band
  plus all of 2026. Should be queried alongside adsb.lol on every future pull.
* github.com/adsblol/globe_history_2025 (and _2024) — WORKED. adsb.lol mirrors
  its ENTIRE archive to GitHub Releases, one release per UTC day, ~3 GB, ODbL.
  Every date the live API 403s is present in full. Assets are a plain `split` of
  a tar (`.tar.aa`, `.tar.ab`) so stream them and filter instead of storing 3 GB:
      curl -sL <base>/<TAG>.tar.aa <base>/<TAG>.tar.ab \
        | tar -xf - --include '*trace_full_<hex>.json'
  GOTCHA: files inside are GZIP-COMPRESSED despite the .json name — gunzip after
  extracting. There is also a small separate `-mlatonly-` release per day.
* samples.adsbexchange.com/traces/YYYY/MM/DD/<last2>/trace_full_<hex>.json —
  WORKED. ADSBX's historical API is paid and 403s, but its FREE SAMPLE is a
  whole day, the 1st of each month, back to July 2016. THE ONLY FREE ROUTE INTO
  2022, and 2022 is where the following-planes claim starts. One day in thirty,
  so it can never test a claim about a specific mid-month date.
* Internet Archive CDX + raw snapshot — WORKED, and it is how the one genuine
  removal was proven. List snapshots, then fetch the raw bytes with the `id_`
  modifier and DECOMPRESS (the raw endpoint returns gzip):
      https://web.archive.org/cdx/search/cdx?url=<URL>&output=json&fl=timestamp,original,statuscode,digest&collapse=digest
      curl --compressed "https://web.archive.org/web/<TIMESTAMP>id_/<URL>"
  FlightRadar24 renders its flight-history table server-side, so the rows parse
  straight out of the archived HTML. Note FR24's free page only ever showed
  SEVEN DAYS of history — no archived copy can hold a multi-year record.

DID NOT WORK, recorded so nobody re-tries them blind:

* globe.adsb.fi/globe_history/... — HTTP 403.
* globe.theairtraffic.com/globe_history/... — HTTP 404.
* samples.adsbexchange.com/readsb-hist/... — 301s to the index; the per-ICAO
  `/traces/` path is the one that works.
* globe.adsbexchange.com/globe_history/... — 403, paid.
* OpenSky /api/flights/aircraft — 403 anonymous since the 2026-03-18 move to
  OAuth2 client credentials. NOT ATTEMPTED with credentials. Cheapest remaining
  gap to close.
* archive.today / archive.ph — HTTP 429 rate-limited on both attempts.
  INCONCLUSIVE, not ruled out. Worth retrying later.

CROSS-CHECK BEFORE PUBLISHING. Two independent routes on the same aircraft-day
should agree. N102DZ on 2025-10-13 came back from the GitHub backup and from
airplanes.live matching to the SECOND on first contact and to four decimals on
position. If two routes DISAGREE, publish the disagreement — do not pick one.


=== The code that does it ===

DIR:
* site/docs/Planes/following/apis/public_open_source/code/: the runnable pass-1
  clients. No dependencies, Node 18+.

FILE:
* .../code/recover_erased.js: THE RECOVERY HARNESS. Pulls airplanes.live and
  adsb.lol side by side per aircraft-day and diffs them, then runs the Internet
  Archive CDX + live-URL probe over the tracking-site pages and parses FR24
  history tables out of archived HTML. Flags each day
  RECOVERED_ONLY_ON_BACKUP / BOTH_HAVE_IT / ONLY_ON_ADSB_LOL / NEITHER_HAS_IT.
      node recover_erased.js [--tail N102DZ] [--pages-only] [--adsb-only]
* .../code/recover_adsbx_samples.js: the ADSBX free monthly sample sweep, the
  2022 route.  node recover_adsbx_samples.js [--tail X] [--from 2022-01] [--to 2026-08]
* .../code/ingest_github_backup.js: ingests traces extracted from a GitHub
  backup tarball into the per-aircraft directories, handling the gzip.
      node ingest_github_backup.js <extract-dir> <YYYY-MM-DD>
* .../code/write_recovery_records.js: writes each aircraft's _RECOVERED_DATA.md.
* .../code/geo_sweep.py: **THE GEOGRAPHIC SWEEP — asks what was there, not who.**
  Every other client in this repo asks a PER-TAIL question and can therefore only
  ever find an aircraft somebody already named; that route holds ~9% of the
  aircraft-days the speaking-event windows need. This one streams a whole UTC day
  of adsb.lol's GitHub Release backup (~2-5 GB, ODbL, no account, ~74k-95k
  aircraft) and filters it by GEOGRAPHY: a 50-mile circle on the US Census
  centroid of every sourced US event city, +/-1 day. 187 event-days, 278 UTC
  dates. Writes a CSV row for EVERY aircraft that entered a circle (that is the
  coverage record) and keeps the full track only for aircraft ON THE GROUND in an
  event circle that were foreign / unregistered / military / PIA, plus any tracked
  tail anywhere. **The six control cities are swept on the same days in the same
  run** — that is built in, not bolted on, because this repo has already had to
  retract a finding for skipping a control.
      python3 geo_sweep.py --plan | --run --jobs 8 | --run --date YYYY-MM-DD | --report
  `--jobs` uses PROCESSES not threads (the JSON half serialises on the GIL). The
  GitHub API is never touched — 60 requests/hour cannot cover 278 dates, so the
  release URL is built (`v2025.09.10-planes-readsb-prod-0`, DOTS in the date) and
  probed on the CDN. **Files inside the tarballs are gzip despite the `.json`
  name.**
* .../code/lib/targets.py: builds that target set out of `tpusa_events.csv` —
  circles, date windows, multi-day conference ranges, and the control cities.
  Rows naming only a month, or no usable city, are returned SEPARATELY and named
  in `data/geo_sweep/targets.json` rather than dropped.
* .../code/geo_sweep_samples.py: the same sweep against ADS-B Exchange's free
  monthly sample — **the only free archive that reaches before 2023**. One day a
  month, so it covers **2 of this investigation's 38 US event-days in 2022** and
  the other 36 are covered by nothing free that exists. `--city Provo --state UT`
  runs a ramp baseline across a range of months instead of an event test; say
  which one was run.
* .../code/analyse_geo_sweep.py: turns the swept days into (1) the notable-aircraft
  rate in EVENT circles against CONTROL circles, (2) which aircraft recur on the
  ground near 2+ events in 2+ states — the question the following claim actually
  makes, and the one per-tail probing can never ask — and (3) what the controls do
  to that recurrence list. An aircraft recurring near events AND near Des Moines
  is a busy charter, not a shadow.
* .../code/lib/fleet.js: tail -> ICAO hex registry. THE join key for every
  ADS-B source. Add a tail here and every script above picks it up.


=== Where recovered data lands ===

Per aircraft, and THE SOURCE IS PART OF THE FILENAME on purpose:

    site/docs/Planes/<TAIL>/data/recovered/
      <TAIL>_<YYYY-MM-DD>_<source-key>_trace_full.json          (pulls before 24 Aug 2026)
      <TAIL>_<YYYY-MM-DD>_<source-key>_trace_full.json.gz       (pulls from 24 Aug 2026 on)
      <TAIL>_<YYYY-MM-DD>_<source-key>_trace_full.json[.gz].meta.json
      <TAIL>_<WAYBACKTIMESTAMP>_wayback_<site>.html
      <TAIL>_<WAYBACKTIMESTAMP>_wayback_<site>_flights.json
      _RECOVERED_DATA.md

Source keys: `airplanes-live`, `adsb-lol`, `adsbexchange-samples`,
`adsblol-github-backup`, `wayback/<site>`.

**`.json` AND `.json.gz` ARE THE SAME EVIDENCE IN TWO CONTAINERS.** A trace is
repetitive JSON and gzips to about 15% of its size; a full fleet sweep across all 139
speaking-event windows in raw JSON would add most of a gigabyte to a tree an automated
job pushes every few minutes. gzip is lossless — `gunzip -c` returns the exact bytes the
server sent, and the `.meta.json` records `stored_gzipped` plus both the wire and stored
byte counts. `lib/traces.py` reads either form transparently. **The uncompressed files
already on disk are LEFT AS THEY ARE** — nothing that is already evidence gets rewritten
to save space.

**A DAY THE ARCHIVE WAS ASKED ABOUT AND HAD NOTHING** gets a
`..._trace_full.miss.json.meta.json` and no payload. That record is what separates
**"asked, and the archive holds nothing"** from **"nobody has queried it yet"**. Those
two must never be merged: the first is a coverage fact, the second is an open question,
and only the first belongs anywhere near a published sentence. Neither is proof the
aircraft was elsewhere — a volunteer network heard nothing, and transponder-off,
out-of-coverage, and a wrong claimed date all look identical from here.

* EVERY payload gets a `.meta.json` beside it recording the exact URL, HTTP
  status, byte count, UTC retrieval time, and a summary of the trace.
* NOTHING OVERWRITES A PREVIOUS PULL. A re-pull lands beside the first with a
  timestamp suffix. THE DIFF BETWEEN TWO PULLS OF THE SAME URL ON TWO DATES IS
  THE EVIDENCE THAT SOMETHING VANISHED — that is the whole point of the layout.
* `_RECOVERED_DATA.md` leads with an underscore so Docusaurus does not publish
  it (`**/_*.{md,mdx}` is in the exclude list). It is the audit trail, not a
  page. NOTE: the older `MISSING_DATA.md` files under `<TAIL>/data/adsb/` do NOT
  have the underscore and therefore DO become public pages — that looks
  unintended; ask before renaming them.


=== Updating the pages after a recovery ===

A recovery is not finished when the JSON lands. The pages have to say WHAT was
removed, WHEN, FROM WHERE, and WHAT THE DATA WAS. The order that worked:

1. THE HUB PAGE. site/docs/Planes/Flight-Data-Recovery/overview.mdx is the Level
   3 page for this whole effort. It carries the three-way split (real removal vs
   retention vs coverage), the recovered content itself, the four routes, the
   control test, and what is still gone.
2. THE AIRCRAFT'S OWN PAGE. Put the recovered record on <TAIL>/overview.mdx —
   the actual table, with UTC as published and local times computed beside it,
   plus a plain statement of what it confirms, what it corrects, and what it
   cannot show.
3. THE PAGE THAT MADE THE ERASURE CLAIM. Erika-Flight-Logs-Erased.mdx said the
   record was unavailable to anyone outside. It is not any more. UPDATE THE
   CLAIM-STATUS TABLE IN PLACE and say plainly that the position changed rather
   than quietly editing around it.
4. THE KNOWLEDGE PAGES. following/apis/public_open_source/knowledge.mdx and
   following/apis/overview.mdx both published gaps that are now closed. A
   "What we did NOT get" section that is out of date is worse than no section —
   append a dated UPDATE block that retracts the specific sentences.
5. pages.csv — a row for any new page, and refresh `line_count` on every page
   edited.
6. `cd site && npm run build` before declaring done. Keep every <div> and
   </div> at column 0; only the build catches an indented closing tag.

WRITING RULES SPECIFIC TO RECOVERY PAGES, and they are not optional:

* SAY WHICH OF THE THREE IT IS. Removal, retention, or coverage gap. Never let a
  403 be described in a way a reader will take as a deletion.
* PUBLISH THE RESULT THAT WEAKENS THE CLAIM AS PROMINENTLY AS THE ONE THAT
  SUPPORTS IT. The 2026-08-24 run recovered T7-ELL's first-ever traces and they
  showed a Dubai/Van Nuys global charter pattern — evidence AGAINST grouping it
  with the Egyptian tails. It went on the page. A recovery that only ever
  confirms what we already believed is a reason to distrust the recovery.
* CORRECT THIS SITE WHEN THE DATA SAYS TO. The recovered FR24 table showed that
  N102DZ "arrived Scottsdale 1:13pm and departed immediately at 1:13pm" was
  FR24's flight-DURATION column read a second time as a clock time. Real ground
  time ~18 minutes. That correction is more valuable than the recovery.
* A TRACE PROVES PRESENCE, NEVER PURPOSE, AND NEVER OCCUPANCY. Recovering an
  aircraft's full movements still does not place any person aboard. Erika Kirk's
  itinerary is the missing document and NO BACKUP ANYWHERE PRODUCES IT — say so
  on every page that leans on her side of a pairing.
* AN ABSENCE IS STILL NOT A FINDING. A 404 means a volunteer network heard
  nothing. Parked and silent, outside receiver coverage, or a wrong claimed date
  come first, every time.
* NEVER ASSERT INTENT. We can show that a page was public and is not any more.
  We cannot see why. Owners lawfully request blocking; sites reorganise URLs.
* SCOPE A CLAIM TO WHAT WAS ACTUALLY CHECKED. If only the `prod` tarball was
  verified, say `prod` — do not generalise to "the backup".

