ROOT_DIR dir is ~/BGit/Bryan_git/charlie-kirk
SITE_DIR dir is {ROOT_DIR}/site
FOLLOWING_DIR dir is {SITE_DIR}/docs/Planes/following
SPEAKING_DIR dir is {FOLLOWING_DIR}/speaking
CODE_DIR dir is {FOLLOWING_DIR}/apis/public_open_source/code
DATA_DIR dir is {FOLLOWING_DIR}/apis/public_open_source/data
PLANES_DIR dir is {SITE_DIR}/docs/Planes
EVENTS_CSV is file {FOLLOWING_DIR}/tpusa_events.csv
FLIGHTS_CSV is file {FOLLOWING_DIR}/flights.csv
OVERLAPS_CSV is file {FOLLOWING_DIR}/overlaps.csv
PLANES_CSV is file {FOLLOWING_DIR}/planes.csv
AIRPORTS_CSV is file {FOLLOWING_DIR}/airports.csv
FOLLOWING_CHARTER is file {FOLLOWING_DIR}/CLAUDE.md
ROOT_CHARTER is file {ROOT_DIR}/CLAUDE.md
ASSESS_MANUAL is file {ROOT_DIR}/prompts/Assess_Manual.md
CK_FILE is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt
  (Real file; {ROOT_DIR}/Charlie_Kirk.txt is a symlink to it. Read the real path. READ-ONLY.)
FLEET_FILE is file {CODE_DIR}/lib/fleet.js
GEO_LIB is file {CODE_DIR}/lib/geo.py
TRACES_LIB is file {CODE_DIR}/lib/traces.py
BUILDER is file {CODE_DIR}/airports_near.py
FETCHER is file {CODE_DIR}/fetch_event_windows.py
TRACE_INDEX is file {DATA_DIR}/recovery/trace_visit_index.json
OURAIRPORTS_DIR dir is {DATA_DIR}/ourairports
GAZETTEER_DIR dir is {DATA_DIR}/gazetteer
VENV dir is ~/.venvs/ck_flight
PYTHON is file {VENV}/bin/python
RADIUS_MILES is the value = 40
WINDOW_DAYS is the value = 2
OUTER_RADIUS_MULTIPLIER is the value = 1.5


Goal of this prompt = For every place Charlie Kirk, Erika Kirk, or TPUSA spoke, build a .yaml beside the .mdx page naming the airport
they probably landed at, every airport within {RADIUS_MILES} miles of it a private jet could also have used, and every tracked aircraft
(especially the Egyptian SU- tails) at any of those fields within plus or minus {WINDOW_DAYS} days.

Re-runnable: run again whenever a speaking location is added to {EVENTS_CSV}, a tail is added to {FLEET_FILE}, or ADS-B data is
recovered. Every yaml is generated; nothing in one is hand-edited.


====================================================================
STAGE 0 — READ FIRST, BEFORE TOUCHING ANYTHING
====================================================================

* Read {CK_FILE}: the most important source; it takes precedence. NEVER write to it; new material goes to
  ~/BGit/all/politics/charlie_kirk/Charlie_Kirk_AI_Inbox.txt.
* Read {ROOT_CHARTER} and {FOLLOWING_CHARTER} in full (following/ governs {FOLLOWING_DIR}; root governs the repo). This prompt obeys
  their rules without repeating them.
* Read {ASSESS_MANUAL} if this run touches a page, not just yaml.
* Read the header comments of {BUILDER}, {GEO_LIB}, {TRACES_LIB}: what each does and what it must never be read as saying.

The three rules a future run will be tempted to break:
  * THE ARRIVAL AIRPORT IS AN INFERENCE, NOT A RECORD. No published Kirk-side flight record exists for most events. "Probably landed
    at" = nearest jet-capable field to the venue city, and every row's selection_basis says so. Never state it on a page as known.
  * A TRACE PROVES PRESENCE, NEVER PURPOSE, AND NEVER OCCUPANCY. Full movements still put no person aboard.
  * AN ABSENCE IS NOT A FINDING. An ADS-B archive 404 means a volunteer network heard nothing (transponder off, outside coverage, or
    a wrong claimed date look identical). NEVER call it a removal until a control aircraft fails the same way on the same dates and
    endpoint.


====================================================================
STAGE 1 — MAKE SURE THE REFERENCE DATA IS ON DISK
====================================================================

Three free, open-licensed datasets, cached under {DATA_DIR}. Refresh only if missing or you want them current.

* OurAirports airports.csv and runways.csv (CC0, ~85,000 fields; gives a single strip with a windsock a real runway length):

      cd {CODE_DIR}
      node ourairports.js

  If runways.csv is still missing:

      curl -sS -o {OURAIRPORTS_DIR}/runways.csv \
        https://davidmegginson.github.io/ourairports-data/runways.csv

* US Census 2024 Gazetteer places national file (the city geocoder, ~32,000 US places with internal-point lat/lon):

      mkdir -p {GAZETTEER_DIR}
      cd {GAZETTEER_DIR}
      curl -sSL -O https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2024_Gazetteer/2024_Gaz_place_national.zip
      unzip -o 2024_Gaz_place_national.zip

* Python env: {GEO_LIB} uses timezonefinder for a real IANA timezone (trustworthy local times across states straddling two zones).
  macOS python is PEP 668 managed (plain pip3 is refused). Build the venv once, OUTSIDE the repo (inside it, the auto-commit job
  would sweep it up):

      python3 -m venv {VENV}
      {VENV}/bin/pip install timezonefinder pyyaml

  Without timezonefinder the code falls back to a state-to-timezone table and STAMPS state_table_APPROXIMATE into every affected yaml
  (a weaker method that says so is fine; one that hides is not).


====================================================================
STAGE 2 — PULL THE AIRCRAFT-DAYS THE WINDOWS ACTUALLY NEED
====================================================================

{BUILDER} can only answer "was an Egyptian jet here" for aircraft-days the repo HOLDS A TRACE FOR. An empty answer from a never-queried
day is worthless; the yaml's coverage block keeps the two apart.

      cd {CODE_DIR}
      {PYTHON} fetch_event_windows.py --plan          (requests needed vs already on disk)
      {PYTHON} fetch_event_windows.py --run --sleep 0.35

* Default scope: the following fleet (Egyptian SU- tails plus T7-ELL). --side kirk adds Kirk-side tails, turning estimated
  arrival/departure into OBSERVED wherever a Kirk aircraft shows.
* --limit N and --from / --to split long runs (polite to the two volunteer archives; resumable, since nothing on disk is re-requested).
* --tail SU-BTT narrows to one aircraft.

Non-optional rules:
  * NOTHING IS EVER OVERWRITTEN. A day on disk is skipped; --repull writes the new copy ALONGSIDE with a timestamp suffix (the diff
    between two pulls of one URL is the evidence something vanished).
  * PAYLOADS ARE STORED GZIPPED as <TAIL>_<DATE>_<source>_trace_full.json.gz (~15% size; raw JSON for a fleet sweep would add most of
    a gigabyte to a repo pushed every few minutes). gzip is LOSSLESS: gunzip -c returns exactly what the server sent, .meta.json records
    stored_gzipped and both byte counts, {TRACES_LIB} reads .json and .json.gz transparently. Existing uncompressed files are LEFT AS
    THEY ARE (evidence is never rewritten to save space).
  * A MISS IS RECORDED: an HTTP 404 writes a .miss.json.meta.json so the next run won't re-ask and the builder can tell "asked, got
    nothing" from "never asked".
  * RUN THE CONTROL TEST BEFORE PUBLISHING ANY 4xx AS SUPPRESSION:

        {PYTHON} fetch_event_windows.py --run --control --from <date> --to <date>

    It queries aircraft with no connection to the case over the same dates; identical failures mean the ARCHIVE, not the airframe,
    and must never be published as suppression (this investigation already retracted one such public claim).

    THE CONTROL TEST HAS RUN ONCE: {DATA_DIR}/recovery/archive_control_probe.json. Both free archives hold ESSENTIALLY NOTHING FOR
    2022 (controls 0 of 56, case aircraft 1 to 2%): 2022 IS A RETENTION BOUNDARY, NOT A REMOVAL; no 2022 gap may be published as
    suppression. That is the year the following-planes claim is said to BEGIN, so these archives cannot test its earliest, most
    load-bearing part; the ADS-B Exchange monthly sample (one day per month) is the only free route in. From 2023 controls run 82 to
    94% per year, so an empty 2023-2025 result is a fact about the AIRCRAFT. The Egyptian fleet sits at 14 to 19%: the expected profile
    of a government VIP jet based in Egypt outside volunteer coverage, NOT evidence of hiding.

    {BUILDER} stamps each event year's verdict into tracked_plane_presence.coverage.archive_control_test (25 of 139 events fall inside
    the 2022 boundary and say so). RE-RUN THE CONTROL whenever the window range grows past the covered years, and rewrite that json:

        {PYTHON} fetch_event_windows.py --run --control --every 8 --sleep 0.3


====================================================================
STAGE 3 — BUILD THE YAML FILES
====================================================================

      cd {CODE_DIR}
      {PYTHON} airports_near.py --rebuild-traces --report

* --rebuild-traces re-reads every recovered trace under {PLANES_DIR}/<TAIL>/data/recovered/ and rewrites {TRACE_INDEX}; pass it
  whenever STAGE 2 pulled anything (else the cached index is reused: ~1 second vs ~1 minute).
* --report prints the cross-event summary: events with an SU- tail inside the radius, JUST OUTSIDE it, unresolved events, mean fields
  per event.
* --only <slug> rebuilds one page's yaml, e.g. --only 20250910_orem.
* --radius and --window override {RADIUS_MILES} and {WINDOW_DAYS}; changing either changes what the file claims, so say so wherever
  output is used.
* --dry-run computes everything, writes nothing.

One .yaml per {EVENTS_CSV} row whose mdx_page is under {SPEAKING_DIR}, named to match the .mdx:

      {SPEAKING_DIR}/20250910_orem.mdx
      {SPEAKING_DIR}/20250910_orem.yaml

Docusaurus does not serve .yaml from site/docs: research data beside the pages (like the six spine CSVs beside {FOLLOWING_DIR}). Nothing
in a yaml goes public until a human puts it on a page, after clearing {FOLLOWING_CHARTER}'s public-content rules.


====================================================================
STAGE 4 — THE YAML HIERARCHY, AND WHAT EACH LEVEL MEANS
====================================================================

Seven top-level blocks, in this order.

  page
    slug, mdx, yaml, url. The join keys back to the site.

  event
    title, who, attendee_class, charlie_present, erika_present, event_type.
    dates      — raw, first_day, last_day, granularity, certainty. CERTAINTY IS LOAD-BEARING: PODCAST_PROXY means a podcast RELEASE
                 date (the event normally 0 to 7 days earlier). NEVER publish a same-day claim off a PODCAST_PROXY row.
    local_time — raw cell, parsed HH:MM, how it was parsed, the IANA timezone and the method that resolved it.
    location   — city, state, country, venue, metro_area, geocode and method. Methods, strongest first: us_census_2024_gazetteer,
                 manual_table, ourairports_municipality_centroid, curated_nearest_airport_code_in_tpusa_events_csv. A city UNKNOWN or
                 AMBIGUOUS in {EVENTS_CSV} STAYS UNRESOLVED; never fill it from memory (why five events resolve to nothing).

  search
    radius, window, window dates, centre airport, every tail and every register searched: the audit trail of the question.

  arrival_airport
    chosen_airport             full field record: code, name, type, elevation, longest runway, surface, runway count, lighting,
                               scheduled service, jet_capability, lat/lon.
    selection_basis            HOW it was chosen (the only honest reading of "probably landed at"):
                                 CURATED_CSV_AND_COMPUTED_NEAREST_JET_FIELD_AGREE
                                 CURATED_..._KEPT_computed_nearest_jet_field_DIFFERS
                                 COMPUTED_NEAREST_JET_CAPABLE_FIELD_no_curated_value
                               When curated and computed DISAGREE both are kept; publish the disagreement, never pick one silently.
    estimated_arrival          date, local time, timezone, UTC, basis, confidence.
    estimated_departure        the same.
                               BOTH ARE ARITHMETIC: arrival = event start minus 3 hours; departure = event end plus 4. With no published
                               event time, 19:00 local is assumed FOR THE ARITHMETIC ONLY and confidence drops to low. Planning
                               assumptions, not observations; each basis string says which.
    observed_by_adsb           the exception and the only records here: a Kirk-side airframe on the ground within the radius in the
                               window, with real first/last contact (UTC and local), ground minutes, carrying archives. Non-empty:
                               USE IT AND SAY IT IS OBSERVED. Empty: the note says so and the estimates stay estimates.

  airports_within_radius
    Every field a private jet could physically use within {RADIUS_MILES} miles of the arrival airport, nearest first. Heliports, seaplane
    bases, balloonports and closed fields excluded. EVERYTHING ELSE KEPT, including every small strip with no scheduled service (the
    point of the sweep). Counts for jet_capable, light_jet_capable, no_scheduled_service.
    jet_capability (coarse, off runway length and surface): jet_capable 5,000 ft paved, light_jet_capable 4,000 ft paved, marginal
    3,000 ft paved, not_jet_capable below, unknown where OurAirports has no runway row. A PLANNING classification, not type performance data.
    Each field carries tracked_plane_presence_in_window, a one-line summary of anything found there.

  tracked_plane_presence
    The answer the file exists for. THREE REGISTERS, KEPT APART, STRONGEST FIRST. NEVER COLLAPSE THEM INTO ONE NUMBER.
      from_adsb_traces     PRIMARY EVIDENCE: real on-ground ADS-B positions merged across archives, each with field, median distance from
                           that runway in km, first/last contact UTC and local, ground minutes, carrying archives, trace files on disk,
                           and cross_source_agreement (the charter's cross-check: two independent archives on one aircraft-day should
                           agree; a DISAGREEMENT is published, not reconciled).
      from_flights_csv     the curated stay register, {FLIGHTS_CSV}.
      from_overlaps_csv    CLAIMS, not records: {OVERLAPS_CSV}, with each claim's overlap_id and this repo's audit_verdict.
      just_outside_the_radius
                           A hard radius is a cliff that hides evidence (KSLC to KPVU is 41.6 miles, so at a flat 40 the 23 April 2024
                           Salt Lake City pairing vanishes by 1.6 miles). The search runs to {OUTER_RADIUS_MULTIPLIER}x the radius and
                           reports the outer ring SEPARATELY. THESE ARE NOT HITS; never publish them as hits.
      coverage             THE HONESTY BLOCK; read it before believing any empty result. aircraft_days_needed = tails x window days;
                           aircraft_days_held = days with a trace; coverage_pct; tails_with_no_trace_in_window. AN EMPTY RESULT WITH LOW
                           COVERAGE IS NOT A NEGATIVE FINDING; it is an unasked question. Close it via STAGE 2.

  counterargument and what_we_do_not_know
    In every file, never trimmed. Maintenance is the strongest innocent explanation: Duncan Aviation at Provo and Lincoln and Yingling at
    Wichita are Part 145 Falcon and Gulfstream shops, and a Falcon 7X parked for weeks at one reads as a maintenance visit.
    Transatlantic customs and fuel stops explain recurring East Coast fields. ERIKA'S SIDE IS THE WEAK SIDE: her flight logs are reported
    erased, so any Erika pairing rests on the foreign aircraft's track plus a CLAIMED location for her.


====================================================================
STAGE 5 — READ THE RESULT HONESTLY
====================================================================

Output to stdout the --report summary, then reason about it out loud.

    ------------------------------------------------------------------
    EVENTS WITH AN EGYPTIAN SU- TAIL INSIDE THE RADIUS AND WINDOW
    ------------------------------------------------------------------

* Always state the count as a fraction of events tested ("1 of 139" is the finding; "1" alone is not).
* A LOW COUNT IS ABOUT WHAT WE CAN CURRENTLY PROVE, NOT WHAT HAPPENED. {EVENTS_CSV} holds every location the repo can source, nowhere
  near every place the Kirks were. Exactly one row places Erika Kirk at an event before 10 September 2025; the trackers' 73-overlap tally
  is measured against Erika locations this repo cannot reproduce. Say BOTH halves whenever a number from this pipeline is quoted.
* Report outer-ring near misses as near misses: never as hits, never silently.
* Report events that resolved to nothing, by slug, with the reason.
* PUBLISH THE RESULT THAT WEAKENS THE CLAIM AS PROMINENTLY AS THE ONE THAT SUPPORTS IT. A run that only confirms beliefs is a reason to
  distrust the run.


====================================================================
STAGE 6 — WHEN A NEW SPEAKING LOCATION IS ADDED
====================================================================

Same order {FOLLOWING_CHARTER} sets for the six spine files: research first, publication second.
  1. Source row in {FOLLOWING_DIR}/sources.csv first (role, stance, evidence_class); source_id is PERMANENT once assigned.
  2. Event row in {EVENTS_CSV}, mdx_page = the .mdx filename that will exist; date_certainty honestly (EVENT_DATE or PODCAST_PROXY);
     city UNKNOWN or AMBIGUOUS rather than a guess.
  3. A field new to the investigation: add its {AIRPORTS_CSV} row and research how_unusual_foreign_state_jet, mro_on_field and
     innocent_explanation BEFORE the airport is described anywhere.
  4. Write the .mdx page in {SPEAKING_DIR} to the existing shape.
  5. STAGE 2 for the new window, then STAGE 3; the .yaml appears automatically (no code change).
  6. Add the {ROOT_DIR}/pages.csv row; refresh line_count on edited pages.
  7. Build before declaring done:

         cd {SITE_DIR} && npm run build

     Every <div> and </div> at column 0 (only the real build catches an indented closing tag).


====================================================================
STAGE 7 — EXTENDING THE PIPELINE
====================================================================

* NEW AIRCRAFT: add to {FLEET_FILE} with ICAO hex, side (following, kirk, n1098l) and hexSource (a wrong hex must be traceable); every
  downstream script picks it up. Add the matching {PLANES_CSV} row for the narrative side.
* NEW DATA SOURCE: add a (source_key, url_template) pair to SOURCES in {FETCHER} and to the recovered-filename convention. The source key
  is PART OF THE FILENAME on purpose (a deletion is provable only if the file says which server it came from).
* DIFFERENT RADIUS OR WINDOW: pass --radius / --window; never hard-code a second default set (each file's search block records what it used).
* NEW GEOCODE FALLBACK: add to geocode_place in {GEO_LIB} with a METHOD NAME that admits its weakness; never a silent guess.

Never delete or hand-edit a yaml (the next run overwrites it). A wrong value is fixed in the CSV, the fleet file, or the code that produced it.
