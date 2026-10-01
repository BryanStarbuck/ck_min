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
  (Real file. Moved 2026-09-19. ~/BGit/Bryan_git/charlie-kirk/Charlie_Kirk.txt is now a symlink to it —
   use that only to verify the location; always read and write the real path.)

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


Goal of this prompt = For every place Charlie Kirk, Erika Kirk, or TPUSA spoke, build a
.yaml file beside the .mdx page that names the airport they probably landed at, every
airport within {RADIUS_MILES} miles of it that a private jet could also have used, and
every tracked aircraft — especially the Egyptian SU- tails — that was at any of those
fields within plus or minus {WINDOW_DAYS} days.

This prompt is re-runnable. Run it again whenever a new speaking location is added to
{EVENTS_CSV}, whenever a new tail is added to {FLEET_FILE}, or whenever new ADS-B data
is recovered. It builds up the yaml files rather than replacing a hand-written analysis,
because every one of them is generated and nothing in them is hand-edited.


====================================================================
STAGE 0 — READ FIRST, BEFORE TOUCHING ANYTHING
====================================================================

* Read {CK_FILE}. It is the most important source there is and it takes precedence over
  everything else. NEVER write to it. New material goes to ~/BGit/all/politics/charlie_kirk/Charlie_Kirk_AI_Inbox.txt.
* Read {ROOT_CHARTER} and {FOLLOWING_CHARTER} in full. The following/ charter governs
  everything in {FOLLOWING_DIR} and the root charter governs the repo. This prompt does
  not repeat their rules; it obeys them.
* Read {ASSESS_MANUAL} if this run will also touch a page and not only a yaml file.
* Read the header comment at the top of {BUILDER}, {GEO_LIB} and {TRACES_LIB}. Each one
  opens with what it does and — more importantly — what it must never be read as saying.

The three rules from those files that this prompt exists to enforce, restated because
they are the ones a future run will be tempted to break:

  * THE ARRIVAL AIRPORT IS AN INFERENCE, NOT A RECORD. No published Kirk-side flight
    record exists for the overwhelming majority of these events. "Probably landed at"
    means "nearest jet-capable field to the venue city" and the yaml says so on every
    single row in selection_basis. Never restate it on a page as a known airport.
  * A TRACE PROVES PRESENCE, NEVER PURPOSE, AND NEVER OCCUPANCY. Recovering an
    aircraft's full movements still does not put any person aboard it.
  * AN ABSENCE IS NOT A FINDING. A 404 from an ADS-B archive means a volunteer receiver
    network heard nothing. Parked with the transponder off, outside coverage, or a wrong
    claimed date all look identical from outside. NEVER call one a removal until a
    control aircraft has failed the same way on the same dates and the same endpoint.


====================================================================
STAGE 1 — MAKE SURE THE REFERENCE DATA IS ON DISK
====================================================================

Three public datasets do the geometry. All three are free, open-licensed, and cached
under {DATA_DIR}. Check each and refresh only if it is missing or you want it current.

* OurAirports airports.csv and runways.csv — CC0, about 85,000 fields worldwide. This is
  where "a single strip with a windsock" gets a runway length behind it instead of an
  adjective. Refresh both with:

      cd {CODE_DIR}
      node ourairports.js

  If runways.csv is missing after that, pull it directly:

      curl -sS -o {OURAIRPORTS_DIR}/runways.csv \
        https://davidmegginson.github.io/ourairports-data/runways.csv

* US Census 2024 Gazetteer, places national file — the city geocoder. About 32,000 US
  places with an internal point latitude and longitude. Pull it with:

      mkdir -p {GAZETTEER_DIR}
      cd {GAZETTEER_DIR}
      curl -sSL -O https://www2.census.gov/geo/docs/maps-data/data/gazetteer/2024_Gazetteer/2024_Gaz_place_national.zip
      unzip -o 2024_Gaz_place_national.zip

* The python environment. {GEO_LIB} uses timezonefinder to turn a latitude and longitude
  into a real IANA timezone, which is what makes the local landing and departure times
  trustworthy across a state that straddles two zones. macOS python is PEP 668 managed,
  so a plain pip3 install is refused. Build the venv once, OUTSIDE this repo — a venv
  inside {ROOT_DIR} would be swept up by the auto-commit job:

      python3 -m venv {VENV}
      {VENV}/bin/pip install timezonefinder pyyaml

  If timezonefinder is not importable the code still runs. It falls back to a state-to-
  timezone table and STAMPS state_table_APPROXIMATE into every affected yaml, because a
  weaker method that says so is fine and a weaker method that hides is not.


====================================================================
STAGE 2 — PULL THE AIRCRAFT-DAYS THE WINDOWS ACTUALLY NEED
====================================================================

This is the stage that decides whether the answer means anything. {BUILDER} can only
answer "was an Egyptian jet here" for aircraft-days this repo HOLDS A TRACE FOR. An
empty answer from a day nobody ever queried is worth exactly nothing, and the yaml's
coverage block exists to keep those two apart.

Work out the plan first:

      cd {CODE_DIR}
      {PYTHON} fetch_event_windows.py --plan

That prints how many requests are needed and how many are already on disk. Then run it:

      {PYTHON} fetch_event_windows.py --run --sleep 0.35

* Default scope is the following fleet — the Egyptian SU- tails plus T7-ELL. Add
  --side kirk to pull the Kirk-side tails as well, which is what turns the estimated
  arrival and departure into an OBSERVED one wherever a Kirk aircraft actually shows.
* --limit N and --from / --to split a long run into pieces. It is polite to the two
  volunteer archives and it makes a partial run resumable, because nothing is ever
  re-requested once it is on disk.
* --tail SU-BTT narrows to one aircraft.

Rules this stage keeps, and they are not optional:

  * NOTHING IS EVER OVERWRITTEN. A day already on disk is skipped. --repull writes the
    new copy ALONGSIDE the old with a timestamp suffix, because the diff between two
    pulls of one URL on two dates is the evidence that something vanished.
  * PAYLOADS ARE STORED GZIPPED as <TAIL>_<DATE>_<source>_trace_full.json.gz. A trace
    gzips to about 15% of its size and a full fleet sweep in raw JSON would add most of
    a gigabyte to a repo an automated job pushes every few minutes. gzip is LOSSLESS —
    gunzip -c returns exactly what the server sent, the .meta.json records
    stored_gzipped and both byte counts, and {TRACES_LIB} reads .json and .json.gz
    transparently. The uncompressed files already on disk are LEFT AS THEY ARE; nothing
    that is already evidence is rewritten to save space.
  * A MISS IS RECORDED, NOT DISCARDED. An HTTP 404 writes a .miss.json.meta.json so the
    next run does not re-ask and so the builder can tell "asked and got nothing" apart
    from "never asked".
  * RUN THE CONTROL TEST BEFORE PUBLISHING ANY 4xx AS SUPPRESSION:

        {PYTHON} fetch_event_windows.py --run --control --from <date> --to <date>

    That asks the same archives about aircraft with no connection to this case over the
    same dates. If the controls fail identically it is the ARCHIVE, not the airframe,
    and it must never be published as suppression. This investigation has already had to
    retract one such claim on a public page. Do not make it two.

    THE CONTROL TEST HAS ALREADY BEEN RUN ONCE AND IT FOUND SOMETHING. The record is
    {DATA_DIR}/recovery/archive_control_probe.json. Both free archives hold ESSENTIALLY
    NOTHING FOR 2022 - the control aircraft return 0 of 56, the case aircraft 1 to 2%.
    2022 IS A RETENTION BOUNDARY, NOT A REMOVAL, and no 2022 gap may be published as
    suppression. That is the year the following-planes claim is said to BEGIN, so these
    two archives cannot test the earliest and most load-bearing part of it at all; the
    ADS-B Exchange monthly sample, one day per month, is the only free route in. From
    2023 the control runs 82 to 94% per year, so an empty 2023-2025 result is a fact
    about the AIRCRAFT and not about the archive. The Egyptian fleet sits at 14 to 19%
    against that control, which is the expected profile of a government VIP jet based in
    Egypt and outside volunteer receiver coverage - IT IS NOT EVIDENCE OF HIDING.

    {BUILDER} reads that json and stamps the verdict for each event's own year into
    tracked_plane_presence.coverage.archive_control_test. 25 of the 139 events fall
    inside the 2022 boundary and say so in their own file. RE-RUN THE CONTROL whenever
    the window range grows past the years it covers, and rewrite that json when you do:

        {PYTHON} fetch_event_windows.py --run --control --every 8 --sleep 0.3


====================================================================
STAGE 3 — BUILD THE YAML FILES
====================================================================

      cd {CODE_DIR}
      {PYTHON} airports_near.py --rebuild-traces --report

* --rebuild-traces re-reads every recovered trace under {PLANES_DIR}/<TAIL>/data/recovered/
  and rewrites {TRACE_INDEX}. Pass it whenever STAGE 2 pulled anything. Leave it off and
  the cached index is reused, which takes about a second instead of about a minute.
* --report prints the cross-event summary: which events have an Egyptian SU- tail inside
  the radius, which have one JUST OUTSIDE it, which events could not be resolved at all,
  and the mean number of fields per event.
* --only <slug> rebuilds one page's yaml, e.g. --only 20250910_orem.
* --radius and --window override {RADIUS_MILES} and {WINDOW_DAYS}. Changing either
  changes what the file claims, so say so wherever the output is used.
* --dry-run computes everything and writes nothing.

One .yaml is written per row of {EVENTS_CSV} whose mdx_page is under {SPEAKING_DIR},
named to match the .mdx exactly:

      {SPEAKING_DIR}/20250910_orem.mdx
      {SPEAKING_DIR}/20250910_orem.yaml

Docusaurus does not serve .yaml out of site/docs, so these files are research data
sitting beside the pages, the same way the six spine CSVs sit beside {FOLLOWING_DIR}.
Nothing in a yaml reaches the public web until a human puts it on a page, and it must
clear the public-content rules in {FOLLOWING_CHARTER} before it does.


====================================================================
STAGE 4 — THE YAML HIERARCHY, AND WHAT EACH LEVEL MEANS
====================================================================

Every file carries the same seven top-level blocks, in this order.

  page
    slug, mdx, yaml, url. The join keys back to the site.

  event
    title, who, attendee_class, charlie_present, erika_present, event_type.
    dates      — raw, first_day, last_day, granularity, certainty.
                 CERTAINTY IS LOAD-BEARING. PODCAST_PROXY means the date is a podcast
                 RELEASE date and the event was normally 0 to 7 days earlier. NEVER
                 publish a same-day claim off a PODCAST_PROXY row.
    local_time — the raw time cell, the parsed HH:MM, how it was parsed, the IANA
                 timezone and which method resolved it.
    location   — city, state, country, venue, metro_area, and the geocode with its
                 method. Methods, strongest first: us_census_2024_gazetteer,
                 manual_table, ourairports_municipality_centroid,
                 curated_nearest_airport_code_in_tpusa_events_csv. A city recorded as
                 UNKNOWN or AMBIGUOUS in {EVENTS_CSV} STAYS UNRESOLVED. Do not fill one
                 in from memory — that is why five events resolve to nothing.

  search
    radius, window, the window dates, the centre airport, every tail searched, and every
    register searched. This is the audit trail of what the question actually was.

  arrival_airport
    chosen_airport             the full field record — code, name, type, elevation,
                               longest runway, surface, runway count, lighting,
                               scheduled service, jet_capability, lat/lon.
    selection_basis            HOW the field was chosen, and the only honest reading of
                               "probably landed at":
                                 CURATED_CSV_AND_COMPUTED_NEAREST_JET_FIELD_AGREE
                                 CURATED_..._KEPT_computed_nearest_jet_field_DIFFERS
                                 COMPUTED_NEAREST_JET_CAPABLE_FIELD_no_curated_value
                               When the curated and computed values DISAGREE, both are
                               kept in the file. Publish the disagreement; never resolve
                               it by picking one silently.
    estimated_arrival          date, local time, timezone, UTC, basis, confidence.
    estimated_departure        the same.
                               BOTH ARE ARITHMETIC ON THE EVENT TIME. Arrival is event
                               start minus 3 hours; departure is event end plus 4. Where
                               no event time is published, 19:00 local is assumed FOR THE
                               ARITHMETIC ONLY and confidence drops to low. These are
                               planning assumptions, not observations, and the basis
                               string on each says which.
    observed_by_adsb           the exception, and the only rows here that are records.
                               A Kirk-side airframe actually on the ground within the
                               radius in this window, with real first and last contact
                               times in UTC and local, ground minutes, and which archives
                               carry it. Where this list is non-empty, USE IT AND SAY IT
                               IS OBSERVED. Where it is empty, the note says so and the
                               estimates above stay estimates.

  airports_within_radius
    Every field a private jet could physically use within {RADIUS_MILES} miles of the
    arrival airport, nearest first. Heliports, seaplane bases, balloonports and closed
    fields are excluded — a business jet cannot use any of them. EVERYTHING ELSE IS KEPT,
    including every small strip with no scheduled service, because those are the point of
    the sweep. Counts are given for jet_capable, light_jet_capable and
    no_scheduled_service.

    jet_capability is a deliberately coarse four-way classification off runway length and
    surface: jet_capable at 5,000 ft paved, light_jet_capable at 4,000 ft paved, marginal
    at 3,000 ft paved, not_jet_capable below that, and unknown where OurAirports publishes
    no runway row. It is a PLANNING classification, not performance data for any type.

    Each field also carries tracked_plane_presence_in_window — the one-line summary of
    anything found there.

  tracked_plane_presence
    The answer to the question the whole file exists for. THREE REGISTERS, KEPT APART,
    STRONGEST FIRST. NEVER COLLAPSE THEM INTO ONE NUMBER.

      from_adsb_traces     PRIMARY EVIDENCE. Real on-ground ADS-B positions, merged
                           across archives, each carrying: the field, the median distance
                           from that runway in km, first and last contact in UTC and
                           local, ground minutes, which archives carry it, the trace files
                           on disk, and cross_source_agreement. That last field is the
                           cross-check the charter requires — two independent free
                           archives on one aircraft-day should agree, and where they do
                           not the DISAGREEMENT is published rather than reconciled.
      from_flights_csv     the curated stay register, {FLIGHTS_CSV}.
      from_overlaps_csv    CLAIMS, not records — {OVERLAPS_CSV}, with each claim's
                           overlap_id and this repo's own audit_verdict on it.

      just_outside_the_radius
                           A hard radius creates a cliff and a cliff hides evidence.
                           KSLC to KPVU is 41.6 miles, so at a flat 40 the 23 April 2024
                           Salt Lake City pairing vanishes by 1.6 miles. The search
                           therefore runs to {OUTER_RADIUS_MULTIPLIER} times the radius
                           and reports the outer ring SEPARATELY. THESE ARE NOT HITS and
                           must never be published as ones.

      coverage             THE HONESTY BLOCK, and the one to read before believing any
                           empty result above it. aircraft_days_needed is tails times
                           window days; aircraft_days_held is how many this repo actually
                           has a trace for; coverage_pct is the ratio; and
                           tails_with_no_trace_in_window names the aircraft that were
                           never heard from at all. AN EMPTY RESULT WITH LOW COVERAGE IS
                           NOT A NEGATIVE FINDING. It is an unasked question. Close it by
                           going back to STAGE 2.

  counterargument and what_we_do_not_know
    Carried in every file, never trimmed. Maintenance is the strongest innocent
    explanation in this record — Duncan Aviation at Provo and Lincoln and Yingling at
    Wichita are Part 145 Falcon and Gulfstream shops, and a Falcon 7X parked for weeks at
    one reads as a maintenance visit. Transatlantic customs and fuel stops explain the
    recurring East Coast fields. And ERIKA'S SIDE IS THE WEAK SIDE: her flight logs are
    reported erased, so any Erika pairing rests on the foreign aircraft's track plus a
    CLAIMED location for her.


====================================================================
STAGE 5 — READ THE RESULT HONESTLY
====================================================================

Output to stdout the --report summary and then reason about it out loud.

    ------------------------------------------------------------------
    EVENTS WITH AN EGYPTIAN SU- TAIL INSIDE THE RADIUS AND WINDOW
    ------------------------------------------------------------------

* State the count as a fraction of the events tested, always. "1 of 139" is the finding.
  "1" on its own is not.
* A LOW COUNT IS A STATEMENT ABOUT WHAT WE CAN CURRENTLY PROVE, NOT ABOUT WHAT HAPPENED.
  {EVENTS_CSV} holds every Kirk and TPUSA location this repo can source and it is nowhere
  near every location the Kirks were at. Exactly one row in it places Erika Kirk at an
  event before 10 September 2025. The trackers' 73-overlap tally is measured against a
  set of Erika locations this repo cannot reproduce. Say BOTH halves of that whenever a
  number from this pipeline is quoted.
* Report the near misses in the outer ring as near misses. Never as hits, never silently.
* Report the events that resolved to nothing, by slug, with the reason.
* PUBLISH THE RESULT THAT WEAKENS THE CLAIM AS PROMINENTLY AS THE ONE THAT SUPPORTS IT.
  A run that only ever confirms what we already believed is a reason to distrust the run.


====================================================================
STAGE 6 — WHEN A NEW SPEAKING LOCATION IS ADDED
====================================================================

The order matters, and it is the same order {FOLLOWING_CHARTER} sets out for the six
spine files. Research first, publication second.

  1. Add the source row to {FOLLOWING_DIR}/sources.csv first, with its role, stance and
     evidence_class. source_id is PERMANENT once assigned.
  2. Add the event row to {EVENTS_CSV}, with mdx_page pointing at the .mdx filename that
     will exist. Fill date_certainty honestly — EVENT_DATE or PODCAST_PROXY. Fill city as
     UNKNOWN or AMBIGUOUS rather than guessing it.
  3. If the event's field is new to this investigation, add its {AIRPORTS_CSV} row and
     research how_unusual_foreign_state_jet, mro_on_field and innocent_explanation BEFORE
     the airport is described anywhere.
  4. Write the .mdx page in {SPEAKING_DIR} to the existing shape.
  5. Run STAGE 2 for the new window, then STAGE 3. The new .yaml appears automatically —
     no code change is needed for a new location.
  6. Add the {ROOT_DIR}/pages.csv row for the new page and refresh line_count on any page
     edited.
  7. Build before declaring done:

         cd {SITE_DIR} && npm run build

     Keep every <div> and </div> at column 0. Only the real build catches an indented
     closing tag.


====================================================================
STAGE 7 — EXTENDING THE PIPELINE
====================================================================

* A NEW AIRCRAFT. Add it to {FLEET_FILE} with its ICAO hex, its side (following, kirk,
  n1098l) and where the hex came from. Every script downstream picks it up — the fetcher,
  the trace index, the builder. Record the hexSource: a wrong hex must be traceable.
  Add the matching {PLANES_CSV} row for the narrative side.
* A NEW DATA SOURCE. Add it to SOURCES in {FETCHER} as a (source_key, url_template) pair
  and to the recovered-filename convention. The source key is PART OF THE FILENAME on
  purpose — a deletion can only be proven if the file says which server it came from.
* A DIFFERENT RADIUS OR WINDOW. Pass --radius and --window. Do not hard-code a second
  set of defaults; a file built at a different radius must say so in its own search block,
  and it does.
* A NEW GEOCODE FALLBACK. Add it to geocode_place in {GEO_LIB} and give it a METHOD NAME
  that admits how weak it is. Never add a fallback that guesses silently.

Never delete a yaml. Never hand-edit one — the header says so and the next run overwrites
it. If a value in a yaml is wrong, the fix goes into the CSV, the fleet file, or the code
that produced it.
