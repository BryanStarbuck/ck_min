#!/usr/bin/env python3
"""generate_overlap_timeline.py — build the Overlap_Timeline infographic as SVG.

Reads the overlap spine and emits an exact, plotted 16:9 chart. Nothing in this
file is hand-typed data: every bar comes out of overlaps.csv, so re-running it
after the CSV changes is the whole update procedure.

    OVERLAPS_CSV is file ~/BGit/Bryan_git/charlie-kirk/site/docs/Planes/following/overlaps.csv
    SVG_OUT      is file ~/BGit/Bryan_git/charlie-kirk/site/internals/static/img/infographics/Overlap_Timeline.svg

WHAT CHANGED, AND WHY IT MATTERS
--------------------------------
The first version of this chart filled its bars from `audit_verdict` — a hostile
line-by-line audit of the claim, done by reading FLIGHT-TRACKING WEBSITES. That
was the best evidence available on the day it was made, and the picture it drew
was "most of this collapses".

It is no longer the best evidence available, for a reason that is the whole
subject of this investigation: THE RECORDS THOSE WEBSITES SHOWED HAVE BEEN
SCRUBBED. Re-reading them today does not reproduce that audit and never will.

So the bars are now filled from `adsb_verified_verdict` — the result of going to
the raw ADS-B position traces, pulling them out of the free historical archives,
KEEPING THE BYTES IN THIS REPO, and measuring each claim point-by-point against
the field it names. Every fill on this chart is reproducible by anyone from
files in `site/docs/Planes/<TAIL>/data/recovered/`, whatever any tracking site
later decides to serve.

That flips what solid and hollow mean, and the flip is the finding:
    SOLID   a trace WE HOLD puts the jet within 15 km of the claimed field.
    HOLLOW  a trace WE HOLD puts it somewhere else. This is the only fill that
            refutes a row.
    DOTTED  no surviving archive can answer. NOT a refutation, and it is by far
            the largest class.

A DIAMOND is the strongest thing on the chart: the jet transmitting from ON THE
GROUND at the named field. A trace still proves presence, never purpose, and
never occupancy — it places nobody aboard.

Design spec: goals.mdx (same directory)  (audience, framing, sizing, percentages, on-image text)
"""

import csv, collections, os, sys, html

ROOT     = os.path.expanduser("~/BGit/Bryan_git/charlie-kirk")
CSV_IN   = os.path.join(ROOT, "site/docs/Planes/following/overlaps.csv")
SVG_OUT  = os.path.join(ROOT, "site/internals/static/img/infographics/Overlap_Timeline.svg")

# ── palette ──────────────────────────────────────────────────────────────────
BG      = "#1b1b1f"
INK     = "#f4f4f6"
GREY    = "#9b9ba3"
DIM     = "#6e6e77"
AMBER   = "#e0a33e"   # Charlie Kirk + TPUSA
BLUE    = "#6ea8d8"   # Erika Kirk
RULE    = "#3a3a42"

# ── geometry (viewBox 1920 x 1080 = 16:9) ────────────────────────────────────
W, H       = 1920, 1080
AX_Y       = 530          # the shared time axis
AX_X0      = 150
AX_X1      = 1566
N_MONTHS   = 46           # Jan 2022 .. Oct 2025
SLOT       = (AX_X1 - AX_X0) / N_MONTHS
BAR_W      = 17
UNIT       = 40           # px per claimed overlap (5 units max on both bands)

# ADS-B verdict -> fill class. C solid, M hatched, R hollow, U and N dotted.
# U and N draw the same because they look the same to a reader -- "this bar
# could not be tested" -- but they are counted apart, because an archive that
# does not reach back is a DIFFERENT failure from a claim that never named an
# aircraft, and rolling them into one number would overstate the archive gap.
FILL = {
    "AT_CLAIMED_AIRPORT":     "C",
    "SAME_METRO_WRONG_FIELD": "M",
    "ELSEWHERE":              "R",
    "NOT_HEARD":              "U",
    "NO_ARCHIVE_COVERAGE":    "U",
    "NOT_QUERIED":            "U",
    "NO_TAIL_CLAIMED":        "N",
}


def month_list():
    out, y, m = [], 2022, 1
    while (y, m) <= (2025, 10):
        out.append("%04d-%02d" % (y, m))
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def load():
    """(upper, lower, undated, ground) — 'YYYY-MM' -> Counter of fill classes."""
    upper = collections.defaultdict(collections.Counter)
    lower = collections.defaultdict(collections.Counter)
    undated = 0
    ground = {"upper": set(), "lower": set(), "dates": set()}
    with open(CSV_IN, newline="") as fh:
        for r in csv.DictReader(fh):
            date = r["date"].strip()
            if len(date) < 7 or date == "UNKNOWN":
                undated += 1
                continue
            mo = date[:7]
            # TPUSA and 'Both' ride with Charlie: the upper band is the
            # organisation-and-Charlie ledger, the lower band is Erika's.
            band = upper if r["subject"] in ("Charlie", "Both", "TPUSA") else lower
            band[mo][FILL.get(r["adsb_verified_verdict"], "U")] += 1
            if r.get("adsb_ground_position") == "yes":
                ground["upper" if band is upper else "lower"].add(mo)
                ground["dates"].add(date)
    return upper, lower, undated, ground


def esc(s):
    return html.escape(s, quote=False)


def bar(x, y_axis, counts, colour, up):
    """Stack C, M, R, U outward from the axis. Returns SVG fragment."""
    frag, off = [], 0
    for fill in ("C", "M", "R", "U", "N"):
        for _ in range(counts.get(fill, 0)):
            y = y_axis - off - UNIT if up else y_axis + off
            if fill == "C":
                frag.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{BAR_W}" height="{UNIT}" fill="{colour}"/>')
            elif fill == "M":
                frag.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{BAR_W}" height="{UNIT}" fill="url(#hatch{colour[1:]})" stroke="{colour}" stroke-width="1.6"/>')
            elif fill == "R":
                frag.append(f'<rect x="{x+0.8:.1f}" y="{y+0.8:.1f}" width="{BAR_W-1.6}" height="{UNIT-1.6}" fill="none" stroke="{colour}" stroke-width="1.6"/>')
            else:   # U and N
                frag.append(f'<rect x="{x+0.8:.1f}" y="{y+0.8:.1f}" width="{BAR_W-1.6}" height="{UNIT-1.6}" fill="none" stroke="{colour}" stroke-width="1.4" stroke-dasharray="3 3" opacity="0.55"/>')
            off += UNIT
    return "".join(frag), off


def main():
    months = month_list()
    upper, lower, undated, ground = load()
    tot_u = sum(sum(c.values()) for c in upper.values())
    tot_l = sum(sum(c.values()) for c in lower.values())
    verd = collections.Counter()
    for band in (upper, lower):
        for c in band.values():
            verd.update(c)

    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Helvetica Neue, Helvetica, Arial, sans-serif">')
    s.append('<defs>')
    for col, name in ((AMBER, AMBER[1:]), (BLUE, BLUE[1:])):
        s.append(f'<pattern id="hatch{name}" width="7" height="7" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">'
                 f'<rect width="7" height="7" fill="none"/><line x1="0" y1="0" x2="0" y2="7" stroke="{col}" stroke-width="3.4"/></pattern>')
    s.append('</defs>')
    s.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')

    # ── title + subline (upper left, ~12% of frame) ──────────────────────────
    s.append(f'<text x="60" y="100" fill="{INK}" font-size="46" font-weight="700" letter-spacing="0.5">THE OVERLAPS, RE-TESTED AGAINST RECOVERED DATA</text>')
    s.append(f'<text x="62" y="139" fill="{GREY}" font-size="20">Egyptian-registered jets and the Kirks, January 2022 &#8211; October 2025. Each bar is one month.</text>')
    s.append(f'<text x="62" y="167" fill="{GREY}" font-size="20">Records in this case go missing, so every claim was re-tested against raw ADS-B traces we pulled and kept &#8212; not a live tracking site.</text>')

    # ── stat card (upper right, ~10%) ────────────────────────────────────────
    cx, cy, cw, ch = 1386, 40, 474, 188
    s.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" fill="none" stroke="{RULE}" stroke-width="1.5" rx="4"/>')
    s.append(f'<text x="{cx+22}" y="{cy+56}" fill="{INK}" font-size="46" font-weight="700">{tot_u + tot_l}</text>')
    s.append(f'<text x="{cx+96}" y="{cy+42}" fill="{GREY}" font-size="17">dated claimed overlaps</text>')
    s.append(f'<text x="{cx+96}" y="{cy+64}" fill="{DIM}" font-size="17">tallies broadcast as &#8220;73&#8221;</text>')
    s.append(f'<line x1="{cx+22}" y1="{cy+80}" x2="{cx+cw-22}" y2="{cy+80}" stroke="{RULE}" stroke-width="1"/>')
    s.append(f'<text x="{cx+22}" y="{cy+102}" fill="{DIM}" font-size="13" letter-spacing="1.1">CHECKED AGAINST TRACES WE HOLD</text>')
    # 100% stacked bar — corroborated / wrong field / refuted / unanswerable
    bx, by, bw, bh = cx + 22, cy + 112, cw - 44, 16
    c_, m_, r_, u_, n_ = verd["C"], verd["M"], verd["R"], verd["U"], verd["N"]
    tt = max(c_ + m_ + r_ + u_ + n_, 1)
    wc, wm, wr, wu = (bw * c_ / tt, bw * m_ / tt, bw * r_ / tt, bw * (u_ + n_) / tt)
    s.append(f'<rect x="{bx}" y="{by}" width="{wc:.1f}" height="{bh}" fill="{INK}"/>')
    s.append(f'<rect x="{bx+wc:.1f}" y="{by}" width="{wm:.1f}" height="{bh}" fill="url(#hatch{AMBER[1:]})" stroke="{AMBER}" stroke-width="1.2"/>')
    s.append(f'<rect x="{bx+wc+wm+0.8:.1f}" y="{by+0.8}" width="{max(wr-1.6,0.6):.1f}" height="{bh-1.6}" fill="none" stroke="{GREY}" stroke-width="1.5"/>')
    s.append(f'<rect x="{bx+wc+wm+wr+0.8:.1f}" y="{by+0.8}" width="{max(wu-1.6,0.6):.1f}" height="{bh-1.6}" fill="none" stroke="{DIM}" stroke-width="1.4" stroke-dasharray="3 3"/>')
    s.append(f'<text x="{bx}" y="{by+38}" fill="{GREY}" font-size="16">'
             f'<tspan fill="{INK}" font-weight="600">{c_} corroborated</tspan>  &#183;  '
             f'<tspan>{r_} refuted</tspan>  &#183;  <tspan>{m_} wrong field</tspan></text>')
    s.append(f'<text x="{bx}" y="{by+60}" fill="{DIM}" font-size="16">{u_} the archives cannot answer  &#183;  {n_} name no aircraft</text>')

    # ── month gridlines + year separators ────────────────────────────────────
    for i, mo in enumerate(months):
        gx = AX_X0 + i * SLOT + SLOT / 2
        s.append(f'<line x1="{gx:.1f}" y1="{AX_Y-212}" x2="{gx:.1f}" y2="{AX_Y+218}" stroke="{RULE}" stroke-width="0.5" opacity="0.32"/>')
        if mo.endswith("-01"):
            lx = AX_X0 + i * SLOT
            s.append(f'<line x1="{lx:.1f}" y1="{AX_Y-252}" x2="{lx:.1f}" y2="{AX_Y+244}" stroke="{RULE}" stroke-width="1.2"/>')
            s.append(f'<text x="{lx+10:.1f}" y="{AX_Y-244}" fill="{GREY}" font-size="19" font-weight="600" letter-spacing="1">{mo[:4]}</text>')

    # ── the bars ─────────────────────────────────────────────────────────────
    marks = []
    for i, mo in enumerate(months):
        x = AX_X0 + i * SLOT + (SLOT - BAR_W) / 2
        f, off = bar(x, AX_Y, upper.get(mo, {}), AMBER, True)
        s.append(f)
        if mo in ground["upper"]:
            marks.append((x + BAR_W / 2, AX_Y - off - 20))
        f, off = bar(x, AX_Y, lower.get(mo, {}), BLUE, False)
        s.append(f)
        if mo in ground["lower"]:
            marks.append((x + BAR_W / 2, AX_Y + off + 20))

    # ── the axis, drawn over the bars ────────────────────────────────────────
    s.append(f'<line x1="{AX_X0-58}" y1="{AX_Y}" x2="{AX_X1+18}" y2="{AX_Y}" stroke="{INK}" stroke-width="1.8"/>')

    # ── diamonds: the jet transmitting from ON THE GROUND at the named field ─
    for mx, my in marks:
        s.append(f'<path d="M {mx:.1f} {my-8} L {mx+8:.1f} {my} L {mx:.1f} {my+8} L {mx-8:.1f} {my} Z" fill="{INK}"/>')
    kx, ky = AX_X0 + 15.5 * SLOT, AX_Y - 300
    s.append(f'<path d="M {kx} {ky-7} L {kx+7} {ky} L {kx} {ky+7} L {kx-7} {ky} Z" fill="{INK}"/>')
    s.append(f'<text x="{kx+18}" y="{ky-2}" fill="{GREY}" font-size="16">the jet transmitting from <tspan fill="{INK}" font-weight="600">on the ground</tspan></text>')
    s.append(f'<text x="{kx+18}" y="{ky+20}" fill="{GREY}" font-size="16">at the named field &#8212; <tspan fill="{INK}" font-weight="600">{len(ground["dates"])} dates</tspan></text>')

    # ── band labels, frame left, inside the empty 2022 months ────────────────
    s.append(f'<text x="60" y="{AX_Y-118}" fill="{AMBER}" font-size="21" font-weight="700" letter-spacing="0.6">CHARLIE KIRK + TPUSA <tspan fill="{GREY}" font-weight="400">&#8212; {tot_u} claimed</tspan></text>')
    s.append(f'<text x="60" y="{AX_Y+188}" fill="{BLUE}" font-size="21" font-weight="700" letter-spacing="0.6">ERIKA KIRK <tspan fill="{GREY}" font-weight="400">&#8212; {tot_l} claimed</tspan></text>')

    # ── ghosted never-published block, off the right end, outside time ───────
    gx0 = AX_X1 + 52
    for k in range(undated):
        s.append(f'<rect x="{gx0 + k*26:.1f}" y="{AX_Y-88}" width="17" height="88" fill="none" stroke="{DIM}" stroke-width="1.3" stroke-dasharray="3 4" opacity="0.72"/>')
    s.append(f'<text x="{gx0}" y="{AX_Y+30}" fill="{GREY}" font-size="17" font-weight="600">{undated} more claimed overlaps</text>')
    for j, ln in enumerate(["never published &#8212; no date, no city,",
                            "no airport, no tail. Cannot be placed",
                            "on this timeline."]):
        s.append(f'<text x="{gx0}" y="{AX_Y+54+j*21}" fill="{DIM}" font-size="15">{ln}</text>')

    # ── legend, lower left (~5%) ─────────────────────────────────────────────
    lx0, ly0 = 60, 830
    s.append(f'<rect x="{lx0}" y="{ly0}" width="596" height="150" fill="none" stroke="{RULE}" stroke-width="1.5" rx="4"/>')
    rows = [("C", "corroborated &#8212; a trace we hold puts the jet at the claimed field"),
            ("M", "right area, wrong field &#8212; within 50 miles, not at the airport named"),
            ("R", "refuted &#8212; a trace we hold puts the jet somewhere else"),
            ("U", "not testable &#8212; no archive reaches back, or no aircraft was named")]
    for j, (fill, txt) in enumerate(rows):
        sy = ly0 + 26 + j * 32
        if fill == "C":
            s.append(f'<rect x="{lx0+20}" y="{sy-11}" width="17" height="17" fill="{INK}"/>')
        elif fill == "M":
            s.append(f'<rect x="{lx0+20}" y="{sy-11}" width="17" height="17" fill="url(#hatch{AMBER[1:]})" stroke="{GREY}" stroke-width="1.4"/>')
        elif fill == "R":
            s.append(f'<rect x="{lx0+20.8}" y="{sy-10.2}" width="15.4" height="15.4" fill="none" stroke="{GREY}" stroke-width="1.6"/>')
        else:
            s.append(f'<rect x="{lx0+20.8}" y="{sy-10.2}" width="15.4" height="15.4" fill="none" stroke="{DIM}" stroke-width="1.4" stroke-dasharray="3 3"/>')
        s.append(f'<text x="{lx0+50}" y="{sy+3}" fill="{GREY}" font-size="15.5">{txt}</text>')

    # ── September call-out lens, lower right (~16%) ──────────────────────────
    px0, py0, pw, ph = 964, 772, 700, 222
    sep_i = months.index("2025-09")
    sep_x = AX_X0 + sep_i * SLOT + SLOT / 2
    s.append(f'<line x1="{sep_x:.1f}" y1="{AX_Y+222}" x2="{px0+pw:.1f}" y2="{py0}" stroke="{RULE}" stroke-width="1.1"/>')
    s.append(f'<line x1="{sep_x-14:.1f}" y1="{AX_Y+222}" x2="{px0+40:.1f}" y2="{py0}" stroke="{RULE}" stroke-width="1.1"/>')
    s.append(f'<rect x="{px0}" y="{py0}" width="{pw}" height="{ph}" fill="{BG}" stroke="{INK}" stroke-width="1.6" rx="4"/>')
    s.append(f'<text x="{px0+26}" y="{py0+34}" fill="{AMBER}" font-size="18" font-weight="700" letter-spacing="1.1">WHAT THE RECOVERED TRACES SHOW AT PROVO</text>')
    lens = [("4 SEP 2025", "SU-BTT lands Provo, 12:45 pm &#8212; inbound from 8,100 km out"),
            ("5&#8211;10 SEP", "SU-BND transmits from the ground at Provo every day"),
            ("10 SEP 2025", "SU-BTT departs Provo, 07:14 am"),
            ("10 SEP 2025", "SU-BND still on the ground at 2:29 pm &#8212; it never leaves")]
    for j, (d, t) in enumerate(lens):
        ly = py0 + 64 + j * 26
        s.append(f'<text x="{px0+26}" y="{ly}" fill="{INK}" font-size="16.5" font-weight="700">{d}<tspan fill="{GREY}" font-weight="400">&#160;&#160;&#8212; {t}</tspan></text>')
    s.append(f'<text x="{px0+26}" y="{py0+178}" fill="{INK}" font-size="16.5">Charlie Kirk is killed at UVU, Orem &#8212; 7 miles away &#8212; at 12:23 pm</text>')
    s.append(f'<line x1="{px0+26}" y1="{py0+191}" x2="{px0+pw-26}" y2="{py0+191}" stroke="{RULE}" stroke-width="1"/>')
    s.append(f'<text x="{px0+26}" y="{py0+212}" fill="{GREY}" font-size="15.5">Times are Mountain, read off the trace. A trace proves presence &#8212; never who was aboard.</text>')

    # ── source line, bottom edge (~3%) ───────────────────────────────────────
    # Three rows, not two. A single row long enough to hold the coverage caveat
    # runs off the right edge of the frame, and a source line that is cut in half
    # is worse than no source line: it reads as if something was hidden.
    s.append(f'<line x1="60" y1="1006" x2="{W-60}" y2="1006" stroke="{RULE}" stroke-width="1"/>')
    src = [
        "Claim counts are researcher tallies attributed to Candace Owens and others. Every fill is computed from raw ADS-B trace files recovered from adsb.lol and airplanes.live and kept in this repo,",
        "measured point-by-point: corroborated = within 15 km of the claimed field that day. Dotted bars could not be tested &#8212; either no free archive reaches that day, or an archive that was serving other",
        "aircraft did not hear this one. Control aircraft with no connection to this case were queried on the same dates to tell those apart, and neither is evidence of anything. Erika Kirk&#8217;s itinerary has never",
        "been published, so no trace can place her aboard. Nothing here is a finding of wrongdoing by any living person.",
    ]
    for j, ln in enumerate(src):
        s.append(f'<text x="60" y="{1024 + j*16}" fill="{DIM}" font-size="13">{ln}</text>')

    s.append('</svg>')

    os.makedirs(os.path.dirname(SVG_OUT), exist_ok=True)
    with open(SVG_OUT, "w") as fh:
        fh.write("\n".join(s))

    print(f"wrote {SVG_OUT}")
    print(f"  upper (Charlie/TPUSA): {tot_u}   lower (Erika): {tot_l}   undated: {undated}")
    print(f"  fill totals: {dict(verd)}")
    mu = max((sum(c.values()) for c in upper.values()), default=0)
    ml = max((sum(c.values()) for c in lower.values()), default=0)
    print(f"  max bar height: upper={mu} ({mu*UNIT}px)  lower={ml} ({ml*UNIT}px)")
    print(f"  on-ground dates: {len(ground['dates'])} {sorted(ground['dates'])}")
    print(f"  on-ground months: upper={sorted(ground['upper'])} lower={sorted(ground['lower'])}")


if __name__ == "__main__":
    main()
