#!/usr/bin/env python3
"""Join the following/ CSVs into one enriched record per claimed overlap, then
emit a JSON + a pre-rendered markdown evidence table for every SLICE that a
cell in site/docs/Planes/following/overview.mdx should link to.

The .mdx pages under following/cuts/ are written FROM these artefacts. The
tables in them are pasted verbatim so no page can drift from the register.

Usage:  python3 build_cuts_data.py [--out DIR]
"""
import csv, json, os, sys, re
from datetime import date, timedelta

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
FOL = os.path.join(ROOT, "site/docs/Planes/following")
OUT = os.path.join(ROOT, "tools/following_cuts/out")


def rd(p):
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


overlaps = rd(os.path.join(FOL, "overlaps.csv"))
flights = rd(os.path.join(FOL, "flights.csv"))
airports = rd(os.path.join(FOL, "airports.csv"))
events = rd(os.path.join(FOL, "tpusa_events.csv"))
fplanes = rd(os.path.join(FOL, "planes.csv"))
root_planes = rd(os.path.join(ROOT, "planes.csv"))

AP = {r["airport_code"]: r for r in airports}
PL = {r["tail_number"]: r for r in fplanes}
RPL = {r["plane_key"]: r for r in root_planes}


def d(s):
    s = (s or "").strip()
    if not s or s.upper() == "UNKNOWN":
        return None
    try:
        return date.fromisoformat(s)
    except Exception:
        return None


def url_from_page(p):
    """site/docs/X/overview.mdx -> /X/overview"""
    p = (p or "").strip()
    if not p.startswith("site/docs/"):
        return ""
    p = p[len("site/docs/"):]
    p = re.sub(r"\.mdx?$", "", p)
    return "/" + p


MONTH = ["", "January", "February", "March", "April", "May", "June", "July",
         "August", "September", "October", "November", "December"]


def pretty(ds):
    dt = d(ds)
    return f"{dt.day} {MONTH[dt.month]} {dt.year}" if dt else (ds or "—")


def tails_of(s):
    s = (s or "").strip()
    if not s or s == "UNKNOWN":
        return []
    if " or " in s:
        return [t.strip() for t in s.split(" or ")]
    return [t.strip() for t in re.split(r"[;,]", s) if t.strip()]


def tail_link(t):
    r = RPL.get(t) or {}
    u = r.get("url_path") or (f"/Planes/{t}/overview")
    return f"[{t}]({u})"


# ---------------------------------------------------------------- enrichment
def ground_stay(tail, ds, code):
    """The flights.csv ground presence whose date window contains this claim."""
    dt = d(ds)
    if not dt:
        return None
    best = None
    for f in flights:
        if f["plane_tail_number"] != tail:
            continue
        s, e = d(f["start_date"]), d(f["end_date"])
        if not s or not e:
            continue
        if s <= dt <= e:
            score = 2 if (code and f["airport_code"] == code) else 1
            if not best or score > best[0]:
                best = (score, f)
    return best[1] if best else None


def events_near(ds, state, days=3):
    """Sourced Kirk/TPUSA appearances within +/- N days, same state first."""
    dt = d(ds)
    if not dt:
        return []
    hits = []
    for ev in events:
        ed = d((ev["dates"] or "").split(" ")[0].split("/")[0])
        if not ed:
            continue
        gap = (ed - dt).days
        if abs(gap) <= days:
            same = bool(state) and ev["state"] in (state or "").split("/")
            hits.append((0 if same else 1, abs(gap), gap, ev))
    hits.sort(key=lambda x: (x[0], x[1]))
    return [(h[2], h[3]) for h in hits]


VERDICT_LABEL = {
    "AT_CLAIMED_AIRPORT": "At the claimed airport — corroborated",
    "ELSEWHERE": "Elsewhere — refuted",
    "SAME_METRO_WRONG_FIELD": "Right area, wrong field",
    "NOT_HEARD": "Not heard",
    "NO_ARCHIVE_COVERAGE": "No archive coverage",
    "NO_TAIL_CLAIMED": "No aircraft named",
    "NO_DATE_CLAIMED": "No date named",
}
AUDIT_LABEL = {
    "accurate": "Accurate", "inaccurate": "Inaccurate", "partial": "Partially accurate",
    "archive_gap": "Not assessable — archive gap", "unpublished": "Never published", "": "Not reached by the audit",
}
SUBJ_LABEL = {
    "ERIKA_ONLY": "Erika Kirk alone", "CHARLIE_ONLY": "Charlie Kirk alone",
    "CHARLIE_AND_ERIKA": "Both Kirks", "TPUSA_NO_KIRK": "TPUSA event, neither Kirk",
}

recs = []
for o in overlaps:
    ds, code, tail = o["date"], o["airport_code"], o["foreign_tail"]
    tl = tails_of(tail)
    ap = AP.get(code, {})
    stay = ground_stay(tl[0], ds, code) if tl else None
    near = events_near(ds, o["state"])
    r = {
        "overlap_id": o["overlap_id"],
        "owens_index": o["owens_index"],
        "date": ds if d(ds) else "",
        "date_raw": ds,
        "date_pretty": pretty(ds) if d(ds) else "no date was ever published",
        "airport_code": code,
        "airport_name": o["airport_name"] or ap.get("airport_name", ""),
        "airport_class": o["airport_class"] or ap.get("airport_class", ""),
        "airport_page": url_from_page(ap.get("site_page", "")),
        "mro_on_field": ap.get("mro_on_field", ""),
        "customs": ap.get("is_us_customs_port", ""),
        "military_colocation": ap.get("military_colocation", ""),
        "city": o["city"], "state": o["state"], "country": o["country"],
        "metro_area": o["metro_area"],
        "following_tails": tl,
        "following_tail_raw": tail,
        "following_type": o["foreign_type"] or (PL.get(tl[0], {}).get("aircraft_type", "") if tl else ""),
        "following_hex": "; ".join(filter(None, [PL.get(t, {}).get("hex_code", "") for t in tl])),
        "following_operator": "; ".join(filter(None, [RPL.get(t, {}).get("operator_owner", "") for t in tl])),
        "arrived_from": o["arrived_from"], "departed_to": o["departed_to"],
        "transponder": o["transponder"],
        "subject": o["subject"], "attendee_class": o["attendee_class"],
        "attendee_label": SUBJ_LABEL.get(o["attendee_class"], o["attendee_class"]),
        "charlie_present": o["charlie_present"], "erika_present": o["erika_present"],
        "tpusa_event_present": o["tpusa_event_present"],
        "claimed_erika_location": o["claimed_erika_location"],
        "event": o["event"], "venue": o["venue"],
        "kirk_tail": o["kirk_tail"],
        "sourced_kirk_event_same_day": o["sourced_kirk_event_same_day"],
        "nearest_sourced_kirk_event": o["nearest_sourced_kirk_event"],
        "nearest_event_gap_days": o["nearest_event_gap_days"],
        "audit_verdict": o["audit_verdict"],
        "audit_label": AUDIT_LABEL.get(o["audit_verdict"], o["audit_verdict"]),
        "confidence": o["confidence"], "survives_audit": o["survives_audit"],
        "adsb_verdict": o["adsb_verified_verdict"],
        "adsb_label": ("Elsewhere by ADS-B — refutation withdrawn"
                       if o["adsb_verified_verdict"] == "ELSEWHERE" and "WITHDRAWN" in o["adsb_verified_note"]
                       else VERDICT_LABEL.get(o["adsb_verified_verdict"], o["adsb_verified_verdict"])),
        "adsb_km": o["adsb_closest_approach_km"],
        "adsb_ground": o["adsb_ground_position"],
        "adsb_note": o["adsb_verified_note"],
        "days_before_sept10": o["days_before_sept10"],
        "source": o["source"], "source_url": o["source_url"],
        "counterargument": o["counterargument"], "notes": o["notes"],
        "overlap_page": url_from_page(o["overlap_page"]),
        "ground_stay": None,
        "nearby_events": [],
    }
    if stay:
        r["ground_stay"] = {
            "tail": stay["plane_tail_number"], "airport_code": stay["airport_code"],
            "city": stay["city"], "state": stay["state"],
            "arrived": stay["start_date"], "departed": stay["end_date"],
            "arrived_pretty": pretty(stay["start_date"]), "departed_pretty": pretty(stay["end_date"]),
            "days_on_ground": stay["days_on_ground"],
            "confidence": stay["confidence"], "notes": stay["notes"],
            "location_page": url_from_page(stay["mdx_page"]),
        }
    for gap, ev in near[:4]:
        r["nearby_events"].append({
            "date": ev["dates"], "who": ev["who"], "title": ev["title"],
            "city": ev["city"], "state": ev["state"],
            "venue": ev["university_or_venue"], "time": ev["time"],
            "gap_days": gap, "event_type": ev["event_type"],
            "nearest_airport_code": ev["nearest_airport_code"],
            "nearest_airport_name": ev["nearest_airport_name"],
            "airport_distance_mi": ev["airport_distance_mi"],
            "charlie_present": ev["charlie_present"], "erika_present": ev["erika_present"],
            "page": url_from_page(ev["mdx_page"]),
            "source_url": ev["source_url"],
        })
    recs.append(r)

BY_ID = {r["overlap_id"]: r for r in recs}


# ---------------------------------------------------------------- rendering
def esc(s):
    s = (s or "").strip().replace("|", "\\|").replace("\n", " ")
    return re.sub(r"\s+", " ", s)


def clip(s, n=210):
    s = esc(s)
    return s if len(s) <= n else s[: n - 1].rsplit(" ", 1)[0] + "…"


def row_link(r):
    return f"[{r['overlap_id']}]({r['overlap_page']})" if r["overlap_page"] else f"`{r['overlap_id']}`"


def table_aircraft(rs):
    """Table A — the FOLLOWING plane: which airframe, which field, landed when, left when."""
    h = ("| Row | Date claimed | Airport | City / State | Following aircraft | Type | ICAO hex | "
         "Arrived from | Departed to | Ground stay logged, arrived | Departed | Days | "
         "Transponder / ground flag | ADS-B verdict | Closest approach |")
    out = [h, "|" + "---|" * 15]
    for r in rs:
        g = r["ground_stay"] or {}
        apc = r["airport_code"] or "—"
        ap = f"**{apc}**" if apc != "—" else "— *none named*"
        if r["airport_page"] and apc != "—":
            ap = f"[**{apc}**]({r['airport_page']})"
        apn = esc(r["airport_name"])
        tails = ", ".join(tail_link(t) for t in r["following_tails"]) or "*no tail named*"
        if len(r["following_tails"]) > 1:
            tails += (" — *source could not tell which*" if " or " in r["following_tail_raw"] else " — *both named on the row*")
        km = f"{r['adsb_km']} km" if r["adsb_km"] else "—"
        if r["adsb_ground"] == "yes":
            km += " — **on the ground**"
        tp = esc(r["transponder"]) or ("on the ground, transmitting" if r["adsb_ground"] == "yes"
                                       else ("airborne position" if r["adsb_ground"] == "no" else "—"))
        out.append("| " + " | ".join([
            row_link(r), f"**{r['date_pretty']}**", f"{ap}<br/>{apn}" if apn else ap,
            esc(", ".join(x for x in (r["city"], r["state"]) if x.strip())) or "*none named*", tails, (esc(r["following_type"]) if r["following_type"].strip().upper() not in ("", "UNKNOWN") else "*not stated*"),
            f"`{r['following_hex']}`" if r["following_hex"] else "—",
            (esc(r["arrived_from"]) if r["arrived_from"] not in ("", "UNKNOWN") else "*not recorded*"),
            (esc(r["departed_to"]) if r["departed_to"] not in ("", "UNKNOWN") else "*not recorded*"),
            g.get("arrived_pretty", "*no logged stay covers this date*"), g.get("departed_pretty", "—"),
            str(g.get("days_on_ground", "") or "—"), clip(tp, 90),
            f"**{r['adsb_label']}**", km,
        ]) + " |")
    return "\n".join(out)


def table_people(rs):
    """Table B — WHO was being followed, and what the Kirk/TPUSA side of the pairing actually was."""
    h = ("| Row | Date claimed | Who the sheet claims was present | Erika location as the sheet gives it | "
         "Sourced Kirk / TPUSA appearance same day | Venue | Local time | Nearest airport to that venue | "
         "Kirk-side aircraft on record |")
    out = [h, "|" + "---|" * 9]
    for r in rs:
        same = ""
        for ev in r["nearby_events"]:
            if ev["gap_days"] == 0:
                same = ev
                break
        if same:
            t = esc(f"{same['who']} — {same['title']}, {same['city']}, {same['state']}")
            ev_cell = f"[{t}]({same['page']})" if same["page"] else t
            venue, tm = esc(same["venue"]) or "—", esc(same["time"]) or "—"
            apx = f"{same['nearest_airport_code']} — {esc(same['nearest_airport_name'])}" if same["nearest_airport_code"] else "—"
            if same["airport_distance_mi"]:
                apx += f", {same['airport_distance_mi']} mi"
        else:
            # the register keeps its OWN nearest-event columns, curated by hand; they do not
            # always agree with the date join against the speaking-events catalog. Show both
            # rather than letting either one print "none" over the top of the other.
            parts = []
            reg = esc(r["nearest_sourced_kirk_event"])
            if reg and reg.lower() not in ("none", "none sourced", "unknown"):
                g = r["nearest_event_gap_days"].strip()
                gs = f" (register: {g} day{'s' if g not in ('1',) else ''} away)" if g else " (register, gap not stated)"
                parts.append(f"**Register's nearest sourced appearance:** {reg}{gs}")
            nearest = r["nearby_events"][0] if r["nearby_events"] else None
            if nearest:
                t = esc(f"{nearest['who']} — {nearest['title']}, {nearest['city']}, {nearest['state']}")
                lbl = f"[{t}]({nearest['page']})" if nearest["page"] else t
                parts.append(f"**Nearest in the events catalog:** {lbl} ({nearest['gap_days']:+d} days)")
            if not parts:
                ev_cell = ("**None same-day.** Neither this register's own nearest-event column nor a "
                           "date join against the sourced speaking-events catalog finds a Kirk or TPUSA "
                           "appearance within three days.")
            else:
                ev_cell = "**None same-day.** " + " · ".join(parts)
            venue = tm = apx = "—"
        who = {"claimed": "claimed", "not_claimed": "not claimed", "unknown": "unknown"}
        pres = (f"Charlie: **{who.get(r['charlie_present'], r['charlie_present'])}** · "
                f"Erika: **{who.get(r['erika_present'], r['erika_present'])}**")
        el = esc(r["claimed_erika_location"])
        el = "*blank on the sheet*" if not el else ("*never stated*" if el.upper() == "UNKNOWN" else el)
        kt = esc(r["kirk_tail"]) or "*none recorded*"
        out.append("| " + " | ".join([
            row_link(r), f"**{r['date_pretty']}**", pres, el, ev_cell, venue, tm, apx, kt,
        ]) + " |")
    return "\n".join(out)


def table_sources(rs):
    """Table C — where each row came from and every verdict passed on it."""
    h = ("| Row | Sheet index | Audit verdict (tracking-site pass) | ADS-B verdict (position data) | "
         "What the position data says | Source of the claim | Source post | Full row page |")
    out = [h, "|" + "---|" * 8]
    for r in rs:
        su = f"[post]({r['source_url']})" if r["source_url"].startswith("http") else "—"
        pg = f"[open]({r['overlap_page']})" if r["overlap_page"] else "—"
        out.append("| " + " | ".join([
            f"`{r['overlap_id']}`", r["owens_index"] or "—", f"**{r['audit_label']}**",
            f"**{r['adsb_label']}**", clip(r["adsb_note"], 230), clip(r["source"], 190), su, pg,
        ]) + " |")
    return "\n".join(out)


def counts(rs):
    def c(key):
        m = {}
        for r in rs:
            m[r[key] or "—"] = m.get(r[key] or "—", 0) + 1
        return dict(sorted(m.items(), key=lambda kv: (-kv[1], kv[0])))
    years = {}
    for r in rs:
        y = (r["date"] or "")[:4] or "no date"
        years[y] = years.get(y, 0) + 1
    tails = {}
    for r in rs:
        tails[r["following_tail_raw"] or "no tail named"] = tails.get(r["following_tail_raw"] or "no tail named", 0) + 1
    return {"rows": len(rs), "distinct_dates": len({r["date"] for r in rs if r["date"]}),
            "by_airport": c("airport_code"), "by_state": c("state"), "by_tail": tails,
            "by_year": dict(sorted(years.items())), "by_adsb_verdict": c("adsb_label"),
            "by_audit_verdict": c("audit_label"), "by_attendee": c("attendee_label"),
            "ground_confirmed": sum(1 for r in rs if r["adsb_ground"] == "yes"),
            "with_same_day_event": sum(1 for r in rs if any(e["gap_days"] == 0 for e in r["nearby_events"]))}


# ---------------------------------------------------------------- the slices
def A(cls):
    return lambda r: r["attendee_class"] == cls


def V(v):
    return lambda r: r["adsb_verdict"] == v


def AU(v):
    return lambda r: r["audit_verdict"] == v


def has_tail(t):
    return lambda r: r["following_tails"] == [t]


CHARLIE_ANY = lambda r: r["attendee_class"] in ("CHARLIE_ONLY", "CHARLIE_AND_ERIKA")
ERIKA_ANY = lambda r: r["attendee_class"] in ("ERIKA_ONLY", "CHARLIE_AND_ERIKA")
CT_LEDGER = lambda r: r["attendee_class"] in ("CHARLIE_ONLY", "CHARLIE_AND_ERIKA", "TPUSA_NO_KIRK")
E_LEDGER = lambda r: r["attendee_class"] == "ERIKA_ONLY" and r["date"]
UNPUB = lambda r: not r["date"]

SLICES = [
    # ---- table 1: "The question people actually ask"
    ("all-85", "Every claimed overlap, all 85 rows",
     "Overlaps with an Egyptian-registered jet, all told", lambda r: True),
    ("dated-80", "The 80 rows that carry a date",
     "of which carry a date at all", lambda r: bool(r["date"])),
    ("never-published-5", "The five rows that were never published",
     "of which were never published — no date, city, airport or tail", UNPUB),
    ("charlie-only-9", "The nine rows claiming Charlie Kirk without Erika",
     "Overlaps with Charlie Kirk where Erika is not claimed with him", A("CHARLIE_ONLY")),
    ("charlie-and-erika-9", "The nine rows claiming both Kirks together",
     "Overlaps claiming Charlie and Erika together", A("CHARLIE_AND_ERIKA")),
    ("charlie-any-18", "Every row that involves Charlie Kirk at all",
     "Overlaps involving Charlie at all", CHARLIE_ANY),
    ("erika-any-70", "Every row that involves Erika Kirk at all",
     "Overlaps involving Erika at all", ERIKA_ANY),
    ("erika-only-61", "The 61 rows resting on Erika Kirk alone",
     "Overlaps where Erika is claimed and Charlie is not", A("ERIKA_ONLY")),
    ("tpusa-no-kirk-6", "The six rows matched to a Turning Point event with neither Kirk",
     "Overlaps at a Turning Point event where neither Kirk is claimed present", A("TPUSA_NO_KIRK")),
    ("tail-su-btt-57", "Every row naming SU-BTT, the yellow plane",
     "Overlaps where the aircraft was SU-BTT, the yellow plane", has_tail("SU-BTT")),
    ("tail-su-bnd-16", "Every row naming SU-BND, the blue plane",
     "Overlaps where the aircraft was SU-BND, the blue plane", has_tail("SU-BND")),
    ("tail-both-3", "The three rows naming both tails at once",
     "Overlaps naming both tails on the one row",
     lambda r: r["following_tail_raw"] == "SU-BTT; SU-BND"),
    ("tail-unresolved-9", "The nine rows that cannot name the aircraft",
     "Overlaps where even the tail number is unresolved",
     lambda r: r["following_tail_raw"] in ("SU-BTT or SU-BND", "", "UNKNOWN")),

    # ---- table 2: "Under that rule"
    ("erika-established-0", "The rows where Erika Kirk's presence is actually established",
     "Overlaps where Erika Kirk's presence is established", lambda r: False),
    ("no-kirk-placeable-61", "The 61 rows where no Kirk can be placed at all",
     "Rows where no Kirk can be placed at all", A("ERIKA_ONLY")),

    # ---- table 3: the ADS-B verdict table
    ("adsb-at-claimed-airport-25", "The 25 rows corroborated by recovered position data",
     "At the claimed airport", V("AT_CLAIMED_AIRPORT")),
    ("adsb-elsewhere-3", "The three rows refuted by recovered position data",
     "Elsewhere", V("ELSEWHERE")),
    ("adsb-same-metro-1", "The one row that is right area, wrong field",
     "Right area, wrong field", V("SAME_METRO_WRONG_FIELD")),
    ("adsb-not-heard-37", "The 37 rows the archives cover but do not hear",
     "Not heard", V("NOT_HEARD")),
    ("adsb-no-archive-coverage-10", "The ten rows no free archive reaches",
     "No archive coverage", V("NO_ARCHIVE_COVERAGE")),
    ("adsb-no-tail-4", "The four rows that name no aircraft",
     "No aircraft named", V("NO_TAIL_CLAIMED")),
    ("adsb-no-date-5", "The five rows that name no date",
     "No date named", V("NO_DATE_CLAIMED")),

    # ---- table 4: the two ledgers
    ("ledger-charlie-tpusa-24", "The Charlie Kirk and TPUSA ledger — all 24 rows",
     "Charlie Kirk + TPUSA — claimed", CT_LEDGER),
    ("ledger-charlie-corroborated-13", "The 13 Charlie/TPUSA rows position data corroborates",
     "Charlie Kirk + TPUSA — corroborated",
     lambda r: CT_LEDGER(r) and r["adsb_verdict"] == "AT_CLAIMED_AIRPORT"),
    ("ledger-charlie-refuted-0", "The Charlie/TPUSA rows position data refutes — there are none",
     "Charlie Kirk + TPUSA — refuted",
     lambda r: CT_LEDGER(r) and r["adsb_verdict"] == "ELSEWHERE"),
    ("ledger-charlie-undecided-11", "The Charlie/TPUSA rows the archives cannot decide",
     "Charlie Kirk + TPUSA — archives cannot answer",
     lambda r: CT_LEDGER(r) and r["adsb_verdict"] in ("NOT_HEARD", "NO_ARCHIVE_COVERAGE", "NO_TAIL_CLAIMED", "SAME_METRO_WRONG_FIELD")),
    ("ledger-erika-56", "The Erika Kirk ledger — all 56 dated rows",
     "Erika Kirk — claimed", E_LEDGER),
    ("ledger-erika-corroborated-12", "The 12 Erika rows position data corroborates",
     "Erika Kirk — corroborated",
     lambda r: E_LEDGER(r) and r["adsb_verdict"] == "AT_CLAIMED_AIRPORT"),
    ("ledger-erika-refuted-3", "The three Erika rows position data refutes",
     "Erika Kirk — refuted", lambda r: E_LEDGER(r) and r["adsb_verdict"] == "ELSEWHERE"),
    ("ledger-erika-undecided-41", "The Erika rows the archives cannot decide",
     "Erika Kirk — archives cannot answer",
     lambda r: E_LEDGER(r) and r["adsb_verdict"] in ("NOT_HEARD", "NO_ARCHIVE_COVERAGE", "NO_TAIL_CLAIMED", "SAME_METRO_WRONG_FIELD")),

    # ---- table 7: the tracking-site audit verdicts
    ("audit-accurate", "Rows the tracking-site audit called accurate",
     "Accurate — the jet really was there that day", AU("accurate")),
    ("audit-inaccurate", "Rows the tracking-site audit called inaccurate",
     "Inaccurate — the jet was somewhere else", AU("inaccurate")),
    ("audit-partial", "Rows the tracking-site audit called partially accurate",
     "Partially accurate — right aircraft and date, wrong route or duration", AU("partial")),
    ("audit-archive-gap", "Rows the audit could not assess",
     "Not assessable — the flight archive does not reach back that far", AU("archive_gap")),
    ("audit-not-reached", "Rows the audit never reached",
     "Not reached by the audit", AU("")),

    # ---- table 8: which Egyptian plane
    ("tail-either-btt-or-bnd-5", "The five rows logged as “SU-BTT or SU-BND”",
     "“SU-BTT or SU-BND” — the source could not tell which",
     lambda r: r["following_tail_raw"] == "SU-BTT or SU-BND"),
    ("tail-none-4", "The four rows with no tail number at all",
     "No tail number recorded at all",
     lambda r: r["following_tail_raw"] in ("", "UNKNOWN")),

    # ---- prose claims that carry a number
    ("ground-confirmed-10", "The ten ground-position confirmations",
     "the aircraft transmitting positions with the on-ground flag set",
     lambda r: r["adsb_ground"] == "yes"),
    ("same-day-sourced-event-10", "Rows that land on a day this site independently sources a Kirk or TPUSA appearance",
     "rows that survive a same-day test at a shared field",
     lambda r: bool(r["sourced_kirk_event_same_day"].strip())),
    ("within-three-days-17", "Rows within three days of a sourced Kirk or TPUSA appearance in the same state",
     "fall within three days of a Turning Point or Charlie Kirk appearance this site can independently source in the same state",
     lambda r: r["nearest_event_gap_days"].strip().isdigit() and int(r["nearest_event_gap_days"]) <= 3),
]

# state slices (table 9) — driven off the airports actually named
STATE_SLICES = [
    ("state-nebraska", "Nebraska", ["KOMA", "KLNK"]),
    ("state-kansas", "Kansas", ["KICT", "KTOP"]),
    ("state-delaware", "Delaware", ["KILG"]),
    ("state-missouri", "Missouri", ["KSTL", "KCPS", "KSUS", "KSTL/KCPS/KSUS"]),
    ("state-utah", "Utah", ["KPVU"]),
]


def flight_table(fs):
    """Every logged ground presence by a following aircraft — arrival and departure dates."""
    h = ("| Aircraft | Airport | City / State | Arrived | Departed | Days on ground | "
         "Confidence in the leg | Location page | What the record says |")
    out = [h, "|" + "---|" * 9]
    for f in fs:
        pg = url_from_page(f["mdx_page"])
        lp = f"[{f['airport_code']}]({pg})" if pg else (f["airport_code"] or "—")
        out.append("| " + " | ".join([
            tail_link(f["plane_tail_number"]), lp,
            esc(f"{f['city']}, {f['state']}".strip(", ")) or "—",
            pretty(f["start_date"]) if d(f["start_date"]) else esc(f["start_date"]),
            pretty(f["end_date"]) if d(f["end_date"]) else esc(f["end_date"]),
            f["days_on_ground"] or "—", esc(f["confidence"]),
            f"[open]({pg})" if pg else "—", clip(f["notes"], 260),
        ]) + " |")
    return "\n".join(out)


def event_table(evs):
    """The Kirk / TPUSA side — who was where, when, and how far from the field."""
    h = ("| Date | Who | Event | City / State | Venue | Local time | Nearest airport | Miles | "
         "Charlie present | Erika present | Event page |")
    out = [h, "|" + "---|" * 11]
    for ev in evs:
        pg = url_from_page(ev["mdx_page"])
        t = esc(ev["title"])
        out.append("| " + " | ".join([
            f"**{esc(ev['dates'])}**", esc(ev["who"]) or "—",
            f"[{t}]({pg})" if pg else t, esc(f"{ev['city']}, {ev['state']}"),
            clip(ev["university_or_venue"], 110) or "—", esc(ev["time"]) or "—",
            f"{ev['nearest_airport_code']} — {esc(ev['nearest_airport_name'])}" if ev["nearest_airport_code"] else "—",
            ev["airport_distance_mi"] or "—", esc(ev["charlie_present"]) or "—",
            esc(ev["erika_present"]) or "—", f"[open]({pg})" if pg else "—",
        ]) + " |")
    return "\n".join(out)


def emit(slug, title, cell, rs, extra=None):
    rs = sorted(rs, key=lambda r: (r["date"] or "9999", r["overlap_id"]))
    payload = {
        "slug": slug, "title": title, "cell_text": cell,
        "url": f"/Planes/following/cuts/{slug}",
        "summary": counts(rs),
        "rows": rs,
    }
    if extra:
        payload.update(extra)
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, f"{slug}.json"), "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=1, ensure_ascii=False)
    tbl = ["## TABLE A — the following aircraft", "", table_aircraft(rs), "",
           "## TABLE B — who they are claimed to have been following", "", table_people(rs), "",
           "## TABLE C — sourcing and both verdicts", "", table_sources(rs)]
    if extra and extra.get("flights"):
        tbl += ["", "## TABLE D — every logged ground presence in this state", "",
                flight_table(extra["flights"])]
    if extra and extra.get("events"):
        tbl += ["", "## TABLE E — the Kirk / TPUSA appearances in this state", "",
                event_table(extra["events"])]
    with open(os.path.join(OUT, f"{slug}.tables.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(tbl) + "\n")
    return payload


index = []
for slug, title, cell, pred in SLICES:
    rs = [r for r in recs if pred(r)]
    p = emit(slug, title, cell, rs)
    index.append({"slug": slug, "title": title, "cell_text": cell, "rows": len(rs),
                  "url": p["url"], "distinct_dates": p["summary"]["distinct_dates"]})

for slug, state, codes in STATE_SLICES:
    rs = [r for r in recs if r["airport_code"] in codes]
    fs = [f for f in flights if f["airport_code"] in codes]
    st = {f["state"] for f in fs if f["state"]}
    evs = [e for e in events if e["state"] in st]
    p = emit(slug, f"{state} — every overlap, every landing, every event", state, rs,
             {"state": state, "airport_codes": codes, "flights": fs, "events": evs,
              "flight_count": len(fs), "event_count": len(evs)})
    index.append({"slug": slug, "title": p["title"], "cell_text": state, "rows": len(rs),
                  "url": p["url"], "distinct_dates": p["summary"]["distinct_dates"],
                  "flights": len(fs), "events": len(evs)})

with open(os.path.join(OUT, "_index.json"), "w", encoding="utf-8") as f:
    json.dump(index, f, indent=1, ensure_ascii=False)

print(f"{len(recs)} overlap records enriched")
for i in index:
    print(f"  {i['rows']:>3} rows  {i['slug']}")
