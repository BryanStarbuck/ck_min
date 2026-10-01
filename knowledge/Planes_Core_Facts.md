# Planes Investigation — Core Facts

Everything measured so far in the aircraft investigation, in one place. Every figure here traces to a
file in this repo (paths at the end). Measured as of 29 September 2026 on branch
`bikash/feat/planes-proof-overlaps`. Public pages live under `site/docs/Planes/`
(served at https://whoassassinatedcharliekirk.com/Planes/overview).

Read the rules first. They decide what any of the numbers below may be used to say.

---

## 1. The rules every fact here obeys

- **A trace proves presence, never occupancy or purpose.** No record in this investigation places any
  person aboard any aircraft.
- **An absence is not a finding.** "Not heard" can mean parked with receivers out of range, transponder
  off, or a wrong claimed date.
- **"Heard" windows are minimums.** ADS-B gives the first and last time a volunteer receiver heard the
  aircraft, not its real arrival or departure.
- **FlightAware stays are inferred.** Arrival to next departure, with no flight recorded between; not watched.
- **Control test before "removal".** Nothing is called deleted until unrelated control aircraft
  (Ryanair 4ca7b5, Lufthansa 3c6444) fail the same way on the same dates.
- **Hidden is not deleted.** Owners can ask FlightAware and Flightradar24 to hide their flights (FAA LADD / PIA).
- **Never assert intent. Never name a possible Fort Huachuca meeting attendee.**

Source ranking: a primary record (trace, FAA registry, FlightAware record) outranks a relayed account
(an X post, a broadcast, a spreadsheet screenshot).

---

## 2. The claim, and what the record says about it

The public claim: Egyptian-registered government jets "followed" Charlie Kirk, Erika Kirk and TPUSA
events, usually quoted as **73 overlaps** (Candace Owens, 17 Nov 2025, up from 68).

| Question | Answer |
|---|---|
| Is 73 a record? | **No.** It is a tracker tally. 68 rows came from a researcher's sheet; 5 were added with no dates. No full dated list was ever published. |
| How big is the rebuilt register? | **85 rows** (`following/overlaps.csv`): 61 Erika alone, 9 Charlie alone, 9 both, 6 TPUSA event with neither. SU-BTT is named on 57, SU-BND on 16, both on 3, "either" on 5; 4 name no tail. |
| How many are proven? | **25**: the foreign jet heard at the named field by recovered ADS-B (5 Charlie-only, 6 both, 12 Erika-only, 2 TPUSA). |
| How many are contradicted? | **3** (OWENS-015, -036, -050). OWENS-015's refutation was **withdrawn 14 Sep 2026**: FlightAware records the Goose Bay landing. 1 more is right area, wrong field (OWENS-012). |
| How many can't be decided? | **56** (37 not heard, 10 no archive coverage, 5 no date, 4 no tail). |
| What does FlightAware say? | Jet at the named field on **23** rows, flying elsewhere on **14**, no flight on **25**. |
| Was a Kirk jet ever on the same ramp as SU-BTT or SU-BND before 10 Sep 2025? | **Zero times** for N582MM, N102DZ or N79SC. Only N888KG, which is Provo-based and a separate claim. |
| What does the claim rest on for Erika? | Social-media placements, not an aircraft. Her aircraft column is empty on 84 of 85 rows. |

**The history of the published number:** this site first published 24 confirmed / 12 refuted
(24–26 Aug 2026). A fix-by-fix re-read retracted 9 of the 12 refutations: 6 had been scored on the
wrong day, 2 off the shorter archive, and 1 (OWENS-012) off a single fix in Paris. The result became
25 / 1 / 3, and then OWENS-015 was withdrawn.

---

## 3. The Egyptian fleet

FlightAware, bought one week at a time for 2022–2025 (`flightaware_derived/us_flights.csv`):
**1,021 flights, 193 touching the US, 13 US airports, never Phoenix** (where TPUSA is based).

| Tail | What it is | Key facts |
|---|---|---|
| **SU-BTT** | Dassault Falcon 7X, "the yellow plane" | In the 73. In the US from March 2022. 4 Sep 2025: Paris → Minot (landed 16:04Z) → Provo (landed **18:46Z, 12:46 p.m. MDT**). 10 Sep: first fix on the ground 07:07:53, **wheels up 07:14:03 MDT**, about five hours before the shooting; landed Wilmington 12:51 p.m. EDT; left the US 11 Sep for Cairo. |
| **SU-BND** | **Gulfstream IV** (type GLF4 in FlightAware and ADS-B; *not* a G550), "the blue plane" | In the 73. At Provo **23 May – 13 Sep 2025** (113 days); FlightAware records one completed local loop (5 Sep). 10 Sep: heard twice from **one parked spot** (16:05–17:34Z and 19:40–20:29Z, 4 m apart), nothing between; the shooting falls in the gap. Left Provo **12:57 p.m. MDT 13 Sep** for Goose Bay. Earlier long stays at Cahokia (2022, 2023) and Provo (Apr–Jul 2024). |
| **SU-BGM** | Gulfstream IV | Not in the 73. At Provo **8 Jul 2024 – 16 Apr 2025** (276 days with no flight, then a loop on 10 Apr). N582MM was on the ground at Provo during that stay on 10 Aug 2024 (heard together for at least 17 min) and at Heber Valley (38 km) on 22 Aug 2024. |
| **SU-BTU** | Falcon 7X | Not in the 73. Wilmington stays in Aug and Nov 2024. No US leg after 1 May 2025. |
| **SU-BTV** | Falcon 7X | Not in the 73. **The 27 May – 2 Jun 2025 Provo stay was SU-BTV**, not SU-BTU as reported. |
| **T7-ELL** | San Marino-registered Global Express | A US and Gulf charter, not Egyptian government; never at a Kirk location. |

Fleet patterns:
- **They were often in the US together.** Two flew inside the US on the same day only once
  (14 Jul 2023), but two or three were in the country at once on **about 341 days**. Same field at
  once: Cahokia (SU-BND + SU-BGM, 2022 and 2023); Provo (SU-BND + SU-BTT 23–28 Apr 2024 and
  **4–10 Sep 2025**; SU-BND + SU-BGM Jul 2024; SU-BGM + SU-BTU Apr 2025; SU-BND + SU-BTV May–Jun 2025).
- **Ways in and out:** in via Paris Le Bourget or Goose Bay; out to Cairo from Wilmington (**45
  departures abroad, no arrival from abroad**). All four 2025 arrivals at Provo from abroad came
  through **Minot International** (a civil field, 13 miles from Minot AFB). 6 of 7 Utah entries were
  via North Dakota; SU-BND entered once via Salt Lake City (19 Apr 2024).
- **Omaha → Lincoln:** 52 min to 5 h 28 min on the ground at Omaha, then a 15–24 min hop.
- **Innocent reading, stated at the same size:** Provo and Lincoln are Duncan Aviation fields, Wichita
  is a Falcon service centre, and Duncan has held the Egyptian Air Force maintenance account since 1999.
- **Fleet value today:** about $265M (5 airframes).

---

## 4. 10 September 2025 at Provo (times MDT, UTC−6)

The site gives the shooting as about **12:10–12:23 p.m.** (two annotations: 18:10 UTC, and 12:23 p.m.).

| Time | Aircraft | What the record shows |
|---|---|---|
| 07:07:53 | SU-BTT | First fix, on the ground at Provo |
| **07:14:03** | SU-BTT | Wheels up for Wilmington (the "7:08" figure is its first fix) |
| 09:08 | N59906 | On the ground at Provo before its survey flight |
| **09:16** | N1098L | First low pass: bottomed at 4,700–4,750 ft, 2–3 km NW of Provo Municipal, **4.16 km from UVU** |
| 10:05 | SU-BND | First of two heard windows, same parked spot |
| 10:07–10:27 | N560TW | On the ground at Provo; then Santa Barbara; home at Scottsdale 1:43 p.m. MDT |
| 10:50 | SU-BTT | Last fix, on approach to Wilmington (landed 12:51 p.m. EDT) |
| 11:01–11:35 | N59906 | Five survey passes at about 19,000 ft |
| **12:06** | N59906 | Back on the ground at Provo, about 17 min before the shooting |
| **12:10–12:23** | — | **The shooting** |
| 12:23–12:24 | N1098L | **204–229 km north of UVU**, descending, not near the campus |
| **12:48** | N1098L | Second low pass, same track, again 4.16 km from UVU |
| 13:11:49 | N888KG | Airborne from Provo |
| 13:30:51 → 14:46:54 | N888KG | **76-minute silence**, starting over south-central Utah (~145 km north of the Arizona line); owner says Page, AZ and back |
| 13:40 | SU-BND | Second heard window, same spot |
| 14:29–15:12 | N40JD | At Provo, from Scottsdale |
| 15:04:16 | N888KG | Back on the ground at Provo |
| **~15:30** | N102DZ | Landed Provo (after SLC 9:23 a.m. and a Scottsdale round trip) |
| 16:36–17:16 | N872RA | At Provo, the **only tracked arrival from Santa Barbara**; who was aboard is not in the record |
| 18:57 | N582MM | Reached Provo from Denver, **after the shooting** |
| 20:23 | N79SC | At Provo |

On 10–11 Sep all seven tracked US jets were on the ground at Provo while SU-BND was there. SU-BTT had
left before six of them arrived; N888KG had been at Provo since the evening of 7 Sep.

---

## 5. The Kirk-side jets

Seven US jets are tracked as the comparison fleet. **Being tracked does not mean the jet belongs to the Kirks.**

| Tail | What the record supports |
|---|---|
| **N582MM** (2001 Learjet 60, Phoenix area) | **Charlie Kirk's usual jet.** On the ground within 50 mi of the event, on the event day, at **30 of 56** answerable events, Jan 2024 – 9 Sep 2025 (2024: 18 of 33; 2025: 12 of 23). Next best: N79SC 10 of 44; N102DZ 1 of 39. Before 13 Sep 2023 no tracked jet is at his events (owner changed 21–25 Jun 2023; FAA certificate to DOJA Contracting LLC, Mesa AZ, 25 Jan 2024). Away from its home fields it is still at 28 of 53. **4–5 Oct 2025 Fort Huachuca → Kalispell legs are in the traces**, with no on-ground fix at either field. |
| **N102DZ** (Gulfstream V) | **Reported as the Kirk family's.** 10 Sep: landed SLC 9:23 a.m., Scottsdale round trip, Provo ~3:30 p.m. Near a Kirk event only once before Sep 2025 (1 minute, Las Vegas, 30 Jan 2024). Hidden (not deleted) by FlightAware and Flightradar24; FAA registration re-issued 16 Oct 2025. 520 aircraft-days held. |
| **N79SC** (Learjet 60, Phoenix area) | Called "her probable plane"; **the record does not support it.** Within 50 mi of N582MM on 103 of 201 days (same airport on 69). At 11 of his 100 dated events before 10 Sep 2025 (N582MM also there at 8). San Clemente, 21–22 Mar 2025, is the only date that fits "her plane", and N560TW and N872RA were nearby too. At the claimed field on 1 of the 62 Erika register rows (Provo, 10 Sep, after the shooting). Owner changed three times in 2026. |
| **N888KG** (Challenger 300, Lehi UT, Provo-based) | **A separate claim; not tied to either Kirk.** The 76-minute silence (above); owner and FBI call it routine. The only Kirk-side jet ever on a ramp with SU-BTT or SU-BND before 10 Sep 2025. |
| **N560TW** (Citation XLS) | Flagged by Candace Owens; reported TPUSA-donor link; no record ties it to either Kirk. The removal-test control aircraft. |
| **N872RA** (Hawker, Santa Ana-based) | The Santa Barbara arrival at 4:36 p.m. that is **not** N40JD. |
| **N40JD** (Premier 1) | At Provo 2:29–3:12 p.m. on 10 Sep (not ~4:40 p.m.). |

**Erika Kirk's aircraft cannot be identified from the public record.** No dated itinerary of hers has
been published: of 139 sourced appearances, one places her at an event before 10 Sep 2025 with a firm
date. At the CBS town hall (taped 10 Dec, aired 13 Dec 2025) she invited people to check "my flight
log" and **named no tail**; X accounts attached it to N102DZ.

No aircraft is registered to Turning Point USA or Turning Point Action (FAA registry).

---

## 6. Other aircraft

| Tail | Fact |
|---|---|
| **N1098L** (Global 6500, LASAI Aviation II, callsign **AXEL10**, not AXLE10) | Two low passes over Provo Municipal (09:16, 12:48), 4.16 km from UVU; **not near UVU at 12:23**. Launched from Biggs Army Airfield. Not previously N911PV (that registration belonged to a different airframe, cancelled Feb 2023). |
| **N2100L** (Global 6500, sister ship, serial 60100 vs 60098) | AXEL21 track over SW Utah the night of 11 Sep 2025 is real; its role is debated. |
| **LASAI fleet** | **11 aircraft** under two Virginia LLCs (3 Globals, 2 Challenger 650s, 6 King Air 350s), about $290M. Corrected from "fifteen" on 29 Sep 2026. |
| **N59906** (Piper Navajo, MARC Inc. survey) | Five passes 11:01–11:35 at ~19,000 ft; on the ground 12:06. |
| **N55906** | Most likely a misreading of N59906; no track exists. |
| **N155TV** | KSL Chopper 5 (news helicopter); no trace held. |
| **N708JH** | Gulfstream G550 registered to the US Government (DOJ); in the case through a tracking-block claim. |
| **99-0404** (C-37A, SAM702) | "Tracked into Fort Huachuca 8–9 Sep" rests on a **tipster email**; no recovered trace. |
| **99-0004** (C-32A) | Air Force Two to Las Vegas, 27 May 2025. The casket flight (SLC → Phoenix, 11 Sep 2025) tail is not published. |
| **N885LS** | Las Vegas Sands 737; registration record only; no connection asserted. |
| **Pilatus PC-12** | Uncorroborated report; no tail, no track. |

---

## 7. Deleted, hidden and recovered

- **Nothing has been shown deleted.** Every Flightradar24 aircraft page still loads. Scripted 403s
  from Flightradar24 are bot protection (it blocks its own home page the same way).
- **13 flights listed publicly on 11 Sep 2025 are hidden now; 12 are recovered.** N102DZ 11 (10 held;
  the missing one is a 7 Sep Scottsdale → Los Angeles leg listed with no actual time), N888KG 2 (both held).
- **What is hidden:** N102DZ and N888KG on FlightAware and Flightradar24; N102DZ went on the FAA privacy
  list between Dec 2025 and Apr 2026. T7-ELL's Flightradar24 table is also hiding (it had flown).
  The Egyptian jets were never hidden.
- **adsb.lol HTTP 403 on 17 late-2025 dates** for all twelve subject tails: archive-wide (controls fail
  too). Recovered from airplanes.live and adsb.lol's own GitHub backup.
- **The one records change in the disputed window:** N102DZ's FAA registration, re-issued 16 Oct 2025.
- **Retracted by this site:** the claim that N102DZ was "removed from Flightradar24" (the page loads).
  Then its correction ("only the free seven-day window") was itself corrected on 15 Sep 2026: it had
  flown, so the empty table was hiding.

**What the investigation holds:** 4,954 aircraft-days of primary position data across **17 aircraft**,
7,116 trace files (467 MB) from four free archives (adsb.lol, airplanes.live, ADS-B Exchange monthly
samples, adsb.lol GitHub backup); 13,602 asked-and-empty aircraft-days. Coverage starts Feb 2023; 2022
exists only as ADS-B Exchange first-of-the-month samples.

---

## 8. Wrong claims this site used to make (do not repeat)

| Was published | The record |
|---|---|
| SU-BTT departed "around the time of the shooting" / at 7:08 | Wheels up 07:14:03 MDT, about five hours before |
| SU-BND's "transponder was on at the moment of the shooting" | Heard twice at one parked spot; the shooting falls in the gap |
| SU-BND "flew out the same day" / "two loops in 113 days" | Left 13 Sep; one completed loop (the 10 June loop is only in a Flightradar24 export) |
| SU-BND is a G550 | Gulfstream IV (GLF4) |
| Egyptian jets come "one at a time" / "together only once" | Together in the US on ~341 days |
| N1098L passes "over UVU at the time of the shooting" | 09:16 and 12:48; 200+ km away at 12:23 |
| N888KG lost signal "at the Arizona border" | Silence began over south-central Utah |
| N59906 passes "at the time of the shooting" | Back on the ground 12:06 |
| N560TW "home 20 minutes after the shot" | 1:43 p.m. MDT (a time-zone slip) |
| N872RA left Santa Barbara 2:19 p.m. MDT | 2:19 p.m. PDT |
| Kolvet's Santa Barbara plane was N40JD | N40JD came from Scottsdale; the Santa Barbara arrival is N872RA |
| The 27 May 2025 Provo arrival was SU-BTU | SU-BTV |
| Wilmington: 12 or 21 departures | 45 departures abroad |
| Omaha hop "within twenty minutes" | 52 min – 5 h 28 min on the ground, then a 15–24 min hop |
| "Every Utah rotation via North Dakota" | 6 of 7 |
| 78-row register, 60/13/1/4; 24/12/42 verdicts | 85 rows, 61/9/9/6; 25/3/1/56 |
| "Days in the US" per jet | Those counts are days with a US flight |
| LASAI fleet of fifteen | Eleven |
| N79SC is Erika's plane; N888KG is hers | Neither is supported; hers is unidentifiable |
| 99-0404 "tracked into Fort Huachuca" | A tipster's claim; no trace |
| SU-BND's Provo contact "4.9 km from the UVU event" | 4.9 **miles** from Orem, the event city |
| SU-BTT's "first-ever trip to America", 20 Jul 2025, "to an Army base in Nebraska" | In the US from March 2022; the 20 Jul 2025 leg was Paris → Omaha Eppley, a civil airport |
| Flight records "removed" / "disappeared" (Narrative and Timeline pages) | Hidden from public tracking sites |

---

## 9. Open questions and what would settle them

- **Records nobody has obtained:** the Provo airport badge access list (updated 11 Sep 2025), the
  Duncan Aviation FBO / rental-car logs, customs records at Minot, Erika Kirk's itinerary, a manifest
  for any flight. State public-records requests to the city-owned airports are the fastest route; none
  has been filed. An FAA request for LADD enrolment dates is drafted in the private `all` repo.
- **56 register rows** cannot be decided by any free archive; the Kirk-side jets were only queried from
  Feb 2023, so the 2022 stays are unanswered.
- **UVU distances** on pages use different reference points: an aircraft's closest approach to campus
  (N1098L 4.16 km), a contact's distance to Orem's city centre (≈5 mi), or the airport to campus
  (about 4 mi straight line). No UVU coordinate is stored in the repo.
- **Still stale, not yet fixed:** three generated photo pages (`Photos/Aircraft/Img_Photo_f2e5fa`, `_a7f60f`,
  `_528138`) describe N1098L "over UVU" and N888KG "over the Utah–Arizona border"; two page titles still
  say "N1098L HADES Over UVU".
- **Per-aircraft coverage tables** on the tail pages date from 24 Aug 2026 (`build_tail_provenance.js`
  not rerun); they carry correction notes.

**Decisions for Bryan:**
- Fort Huachuca names on the SAM, Andrews and Biggs pages (Hegseth, Hansell, Harpole, Snow). The repo's
  own rule forbids naming possible attendees.
- Named_People §4 applies "Person of Interest" and "Missing" labels to named living people; needs a
  defamation review.
- N102DZ's page title "Kirk's Plane" states ownership as fact.

---

## 10. Where the data lives and how to rebuild

| What | Path (under `site/docs/Planes/`) |
|---|---|
| Claim register (85 rows) | `following/overlaps.csv` |
| Kirk / TPUSA events | `following/tpusa_events.csv` |
| ADS-B ground contacts | `following/apis/public_open_source/data/analysis/master_proximity.csv` |
| Kirk-side stops and linkage | `…/analysis/kirk_side/` (`stops.csv`, `charlie_event_aircraft.csv`, `n79sc_n582mm_days.csv`, `plane_linkage_summary.json`) |
| FlightAware (Egyptian jets) | `following/apis/proprietary/data/flightaware_derived/us_flights.csv` |
| FlightAware restated answers | `following/apis/proprietary/data/flightaware_restated/` |
| Raw traces | `<TAIL>/data/recovered/` (source in the filename) |
| Overlap graphics | `site/internals/static/img/infographics/overlaps/` |
| Aircraft prices | `aircraft_costs.csv` (repo root) |
| Adelson jet material | private `all/politics/charlie_kirk/flights/adelson/` only |

Rebuild order after a data change: `analyse_kirk_side_record.py` → `build_kirk_plane_linkage.py` →
`rebuild_plane_pages.sh` → `build_plane_linkage_pages.py`; graphics: `measure_windows.py` →
`build_info_yaml.py` → `build_pair_yaml.py` → `node build_overlap_svg.ts --all` → `embed_overlap_svgs.py`;
cuts: `tools/following_cuts/build_cuts_data.py` → `resync_tables.py`. Check pages with
`node site/_ck_mdxcheck.mjs <files>`. **Never run `npm run build` on this machine** (it runs out of memory).
