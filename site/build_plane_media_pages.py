#!/usr/bin/env python3
"""
build_plane_media_pages.py — the two plane media wall pages under /Planes/.

Writes, from the media pages that ALREADY exist on this site:

  site/docs/Planes/Plane-Photos.mdx   every photo page in the Photos/Aircraft
                                      cluster, two columns, real aspect ratio,
                                      two sentences under each, each tile
                                      linking to that photo's own page.
  site/docs/Planes/Plane-Videos.mdx   every video page in the two aircraft
                                      video clusters, two columns, real
                                      aspect ratio, a sentence or two under
                                      each, and after every FOURTH video a
                                      three-sentence interlude carrying at
                                      least three links into the most
                                      interesting pages of the Planes section.
                                      Every interlude points somewhere new.

NO NEW IMAGE OR VIDEO BYTES ARE CREATED. Each tile re-uses the exact
/img/evidence/<sha>.jpg, /img/video_posters/<sha>.jpg and IPFS <source> lines
the existing leaf page already serves, so the wall is a second route into the
same corpus rather than a second copy of it.

Aspect ratio is measured from the actual pixels (PIL) and written onto the tile
as an aspect-ratio style, so nothing is stretched wide and nothing is cropped.

Re-runnable: both files are rewritten whole every run.

    python3 site/build_plane_media_pages.py [--check]
"""

import os
import re
import sys

REPO = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DOCS = os.path.join(REPO, "site/docs")
STATIC = os.path.join(REPO, "site/internals/static")

from PIL import Image

PHOTO_ROOTS = ["Photos/Aircraft"]
VIDEO_ROOTS = [
    ("Videos/Vid_Aircraft_Flight_Evidence", "Aircraft and flight-record video"),
    ("Videos/Vid_Drones", "Drones over the venue"),
]

IMG_SRC_RE = re.compile(r'<img className="ck-evidence-image"[^>]*\ssrc="([^"]+)"')
POSTER_RE = re.compile(r'poster="(/img/video_posters/[^"]+)"')
SOURCE_RE = re.compile(r'<source\s+src="([^"]+)"\s+type="([^"]+)"\s*/?>')

# Sentence ends we must not split on.
ABBREV = re.compile(
    r"(?:\b(?:Mr|Mrs|Ms|Dr|St|Lt|Col|Gen|Sgt|Sen|Rep|Gov|Jr|Sr|vs|approx|Inc|Ltd"
    r"|Co|Corp|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sept|Sep|Oct|Nov|Dec|No|Fig|Est)\."
    r"|\b[A-Z]\.(?:[A-Z]\.)*"
    r"|\ba\.m\.|\bp\.m\.)$"
)

_dims = {}


def dims_for(src):
    if src in _dims:
        return _dims[src]
    wh = None
    if src.startswith("/"):
        fs = os.path.join(STATIC, src.lstrip("/"))
        if src.lower().endswith(".svg"):
            # PIL cannot open an SVG; the viewBox carries the ratio instead.
            try:
                head = open(fs, encoding="utf-8", errors="replace").read(4000)
                m = re.search(r'viewBox="\s*[-\d.]+[ ,]+[-\d.]+[ ,]+'
                              r'([\d.]+)[ ,]+([\d.]+)', head)
                if not m:
                    m = re.search(r'width="([\d.]+)(?:px)?"[^>]*?'
                                  r'height="([\d.]+)(?:px)?"', head)
                if m:
                    wh = (int(round(float(m.group(1)))),
                          int(round(float(m.group(2)))))
            except Exception:
                wh = None
        else:
            try:
                with Image.open(fs) as im:
                    wh = im.size
            except Exception:
                wh = None
    _dims[src] = wh
    return wh


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def fm(text, key):
    m = re.search(r'^%s:\s*"?(.*?)"?\s*$' % key, text, re.M)
    if not m:
        return None
    s = m.group(1)
    try:
        s = s.encode("latin-1", "backslashreplace").decode("unicode_escape")
    except Exception:
        pass
    return s.strip()


def route_from_path(path):
    rel = os.path.relpath(path, DOCS)
    rel = re.sub(r"\.mdx?$", "", rel)
    return "/" + rel


def plain(s):
    """Markdown/MDX inline syntax out, readable prose in."""
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)      # links -> their text
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)            # bold
    s = re.sub(r"(?<!\w)\*([^*]+)\*(?!\w)", r"\1", s)   # italics
    s = re.sub(r"`([^`]+)`", r"\1", s)                  # code
    s = re.sub(r"\{/\*.*?\*/\}", " ", s)                # mdx comments
    s = re.sub(r"<[^>]+>", " ", s)                      # stray tags
    s = s.replace("--", "—")
    return " ".join(s.split())


def first_paragraph(text, headings):
    """First real prose paragraph under any of `headings`."""
    for h in headings:
        m = re.search(r"^##+\s+" + re.escape(h) + r"\s*$", text, re.M)
        if not m:
            continue
        for para in re.split(r"\n\s*\n", text[m.end():]):
            p = para.strip()
            if not p:
                continue
            if p[0] in "#<*|-" or p.startswith("{/*") or p.startswith("!["):
                continue
            return plain(p)
    return None


def sentences(s, n):
    """First n sentences of s, abbreviation-aware."""
    if not s:
        return ""
    out, cur = [], ""
    for tok in re.split(r"(?<=[.!?])\s+", s):
        cur = (cur + " " + tok).strip() if cur else tok
        if ABBREV.search(cur):
            continue
        out.append(cur)
        cur = ""
        if len(out) >= n:
            break
    if cur and len(out) < n:
        out.append(cur)
    return " ".join(out).strip()


def esc(s):
    s = (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # { and } open a JSX expression in MDX and would break the build.
    return s.replace("{", "&#123;").replace("}", "&#125;")


def escq(s):
    return esc(s).replace('"', "&quot;")


def caption_for(text, want):
    """`want` sentences of description, drawn from the page's own prose first."""
    body = first_paragraph(text, ["What This Image Shows", "What This Video Is",
                                  "What This Shows", "What Is Said"])
    desc = plain(fm(text, "description") or "")
    if body:
        cap = sentences(body, want)
        if len(cap.split()) < 12 and desc:
            cap = (cap + " " + desc).strip()
        return cap
    return sentences(desc, want)


def collect(root, prefix, src_re):
    """Leaf media pages under root: direct leaves first, then each sub-cluster."""
    out = []
    entries = sorted(os.listdir(root))
    for f in [e for e in entries if e.startswith(prefix) and e.endswith(".mdx")]:
        path = os.path.join(root, f)
        text = read(path)
        m = src_re.search(text)
        if not m:
            continue
        src = m.group(1)
        wh = dims_for(src)
        out.append({
            "link": fm(text, "slug") or route_from_path(path),
            "src": src,
            "title": fm(text, "title") or "Untitled",
            "cap": caption_for(text, 2),
            "w": wh[0] if wh else None,
            "h": wh[1] if wh else None,
            "sources": SOURCE_RE.findall(text),
        })
    for d in [e for e in entries if os.path.isdir(os.path.join(root, e))]:
        out.extend(collect(os.path.join(root, d), prefix, src_re))
    return out


def ar_style(item):
    if item["w"] and item["h"]:
        return ' style={{aspectRatio: "%d / %d"}}' % (item["w"], item["h"])
    return ""


def photo_tile(it):
    return (
        '  <figure className="ck-media-cell">\n'
        '    <a className="ck-media-shot" href="%s">'
        '<img src="%s" alt="%s" loading="lazy"%s /></a>\n'
        '    <figcaption className="ck-media-cap">'
        '<a href="%s">%s</a> — %s</figcaption>\n'
        '  </figure>' % (it["link"], it["src"], escq(it["title"]), ar_style(it),
                         it["link"], esc(it["title"]), esc(it["cap"]))
    )


def video_tile(it):
    srcs = "\n".join(
        '        <source src="%s" type="%s" />' % (u, t) for u, t in it["sources"]
    )
    return (
        '  <figure className="ck-media-cell">\n'
        '    <div className="ck-media-shot">\n'
        '      <video controls preload="none" poster="%s"%s>\n'
        '%s\n'
        '        Your browser does not support the video tag.\n'
        '      </video>\n'
        '    </div>\n'
        '    <figcaption className="ck-media-cap">'
        '<a href="%s">%s</a> — %s</figcaption>\n'
        '  </figure>' % (it["src"], ar_style(it), srcs, it["link"],
                         esc(it["title"]), esc(it["cap"]))
    )


# ---------------------------------------------------------------------------
# The interludes. One is emitted after every FOURTH video. Each is three
# sentences, each carries at least three linked phrases, and no interlude
# points at a page an earlier interlude already used. They are about the
# aircraft investigation itself, not about the videos.
# ---------------------------------------------------------------------------

INTERLUDES = [
    'Two Egyptian-registered government jets are put on the ground at Provo on '
    'the day of the assassination by primary ADS-B position data rather than by a'
    ' reading of a tracking website: [SU-BTT](/Planes/SU-BTT/overview) at a '
    'closest fix of 1.23 km from the field, and [SU-BND](/Planes/SU-BND/overview)'
    ' at 1.29 km. SU-BTT had been parked on that ramp since 4 September, six days'
    ' before, and SU-BND did not move at all that day — its first and last fixes '
    'of 10 September are the same Provo position. Of the 85 claimed overlap rows '
    'reconstructed on this site, 29 are ones primary position data can decide '
    'either way, 25 of those put the aircraft at the field the claim names and '
    'three are refuted (one of them, OWENS-015, since withdrawn); the count and '
    'the case against reading it as shadowing are both on [Following Charlie or '
    'Erika](/Planes/Following-Charlie-Erika).',

    '[N1098L](/Planes/N1098L/overview) is a US Army-contracted Bombardier Global '
    '6500, and researchers time low, slow passes near the campus in the half hour'
    ' after the shot; the recovered track puts its two low passes over Provo '
    'Municipal Airport, 4 km from campus, at 9:16 a.m. and 12:48 p.m. It launched'
    ' that morning from [Biggs Army '
    'Airfield](/Planes/Airport-Biggs-Army-Airfield) at Fort Bliss, a military '
    'origin rather than a civilian one, and it is not the only airframe of its '
    'type in this case — [N2100L](/Planes/N2100L/overview) is a sister ship in '
    'the same contractor fleet. What that class of aircraft is actually built to '
    'collect, and why a purpose-built collection platform is not a passing '
    'business jet, is set out on [ISR Program Context](/Planes/ISR-Operations).',

    "[N102DZ](/Planes/N102DZ/overview), the aircraft reported as Charlie Kirk's, "
    'had its FAA registration certificate re-issued 36 days after the '
    'assassination to a Cheyenne, Wyoming holding company — an ordinary kind of '
    'event that is not evidence of anything by itself '
    '([N79SC](/Planes/N79SC/overview) has also changed owners since). Erika Kirk '
    'publicly invited people to check flight logs, and researchers say that '
    "tail's public history was afterwards removed. The record shows the tracking "
    "sites hiding it at the owner's request rather than deleting it, and 10 of "
    'the 11 flights they listed publicly that week are held independently; the '
    'dispute, with both sides and the copies taken beforehand, is on [Erika '
    'Flight Logs Erased](/Planes/Erika-Flight-Logs-Erased). Separating a genuine '
    'removal from an archive retention boundary and from an ordinary gap in '
    'volunteer receiver coverage is the whole job of [Which Flight Records Were '
    'Deleted](/Planes/Deleted-Flight-Records) and [What A 403 Actually '
    'Means](/Planes/Flight-Data-Recovery/What-A-403-Means), which is where this '
    'site retracted one of its own claims.',

    'The Egyptian tails are not one stray jet: [SU-BTU](/Planes/SU-BTU/overview),'
    ' [SU-BTV](/Planes/SU-BTV/overview) and [SU-BGM](/Planes/SU-BGM/overview) '
    'fill out the group trackers call an armada, five foreign state aircraft '
    'cycling through one small Utah municipal field in the year of the '
    'assassination. The innocent reading has to be put at the same size: Provo '
    'and Lincoln are Duncan Aviation fields and Wichita is a Falcon service '
    "centre, Duncan has held the Egyptian Air Force's maintenance account since "
    '1999, and a jet sitting on a maintenance ramp is exactly what a maintenance '
    'visit looks like. The competing claim — that some of these legs logged as '
    'Cairo-to-Cairo actually ended in Israel with the transponder off — is '
    'collected, unverified and labelled as such, on [Israel '
    'Planes](/Planes/Israel-Planes).',

    '[N888KG](/Planes/N888KG/overview) left Provo about an hour after the '
    'shooting and was not heard for 76 minutes from a point over south-central '
    'Utah before reappearing northbound and flying back; its owner says it went '
    'to Page, Arizona and back. A gap in reception is not proof of anything on '
    'its own — coverage over that terrain is thin and receivers are volunteer-run'
    " — which is why the same day's other private traffic into the same small "
    'field, [N560TW](/Planes/N560TW/overview) out of Scottsdale that morning and '
    '[N872RA](/Planes/N872RA/overview) from Santa Barbara that afternoon, is '
    'logged beside it rather than left out. Laid end to end against the hospital '
    'and campus timings, those windows are what produce the conflicts set out on '
    'the [September 10 Flight Timeline](/Planes/Sept10-Flight-Timeline).',

    'Government aircraft sit on both ends of this week. [SAM '
    '99-0404](/Planes/SAM-99-0404/overview) is reported, in a tipster email '
    "circulated by Candace Owens, as tracked into Fort Huachuca, the Army's "
    'intelligence centre in Arizona, on 8–9 September 2025 under the '
    '[SAM702](/Planes/SAM-702/overview) callsign, two days before the '
    'assassination; no recovered trace confirms it. The day after it, Air Force '
    'Two carried the casket from Salt Lake City to Phoenix, landing at a military'
    ' installation rather than a civilian terminal — the [Casket '
    'Flight](/Planes/Casket-Flight) page has the route and the aircraft. Both VIP'
    ' movements trace back to the same single base, [Joint Base '
    'Andrews](/Planes/Airport-Joint-Base-Andrews), and the same physical airframe'
    ' appears in public tracking under several rotating callsigns, which is how '
    'one jet can look like several flights.',

    'Not every aircraft in this case is a mystery, and saying so is part of the '
    'record. [N59906](/Planes/N59906/overview) is a Piper Navajo Chieftain that '
    'made five aerial-mapping passes over the Utah Valley at about 19,000 ft that'
    ' morning, the last ending around 11:35 — and what that class of aircraft '
    'routinely does, including its April 2026 re-registration, is laid out on '
    '[Contract Survey Aircraft](/Planes/Contract-Survey-Aircraft). '
    '[N55906](/Planes/N55906/overview) differs from it by a single digit, has no '
    'confirmed route, operator or track anywhere in the public record, and is '
    'most likely a misreading that has been repeated. Which records would '
    'actually settle each remaining aircraft question — survey logs, raw ADS-B '
    'feeds, tasking orders — is the entire content of the [Planes Investigation '
    'Index](/Planes/Planes_Investigation_Index).',

    'Everything above is checkable, which is the only reason to publish it. '
    '[Flight Data Recovery](/Planes/Flight-Data-Recovery/overview) records what '
    'came back out of four independent free archives — 4,954 aircraft-days across'
    ' 7,116 trace files — and [Per-Aircraft Recovery '
    'Status](/Planes/Flight-Data-Recovery/Per-Aircraft-Status) gives one row per '
    'tail naming every source that answered and every one that did not. [Provo '
    '(KPVU)](/Planes/Airports/KPVU) has its own page listing all 135 recorded '
    'ground visits at that field, and the follow log runs [location by '
    'location](/Planes/following/overview) rather than as one narrative. None of '
    'it places any person aboard any aircraft: no manifest for any leg has been '
    'published by anyone, and a trace proves presence, never purpose and never '
    'occupancy.',
]


PHOTO_HEADER = """---
displayed_sidebar: docs
title: "Every Plane Photo In One Place"
sidebar_label: "All Plane Photos"
description: "A single scrolling wall of every photograph in the aircraft investigation — {n} images, each at its true aspect ratio, each clicking through to its own evidence page."
hide_table_of_contents: true
---

{{/* Generated by site/build_plane_media_pages.py. Rewritten whole on every run — do not hand-edit. */}}

<a href="/Planes/overview" style={{{{display:'inline-block', marginBottom:'1rem', padding:'0.35rem 0.9rem', background:'#1a73e8', color:'#fff', borderRadius:'4px', textDecoration:'none', fontSize:'0.9rem'}}}}>← Planes</a>

# Every Plane Photo In One Place

If you are new to the aircraft side of this investigation, this page is the fastest
way in: **{n} photographs**, everything the site holds on planes, flight records,
tail numbers, registrations, transponder tracks and the drones reported over the
venue, laid out end to end so you can scan the whole corpus in one scroll instead
of opening {n} separate pages. Nothing here is new — every picture is the same file
its own evidence page already serves, shown at its true shape rather than stretched
to the width of the column, and every tile clicks through to that page for the full
resolution image, where it came from, and what it does and does not show.

Two sentences sit under each picture so you can tell a screenshot of a flight-tracking
playback from a registration document from a photograph of an aircraft without opening
anything. A screenshot of a claim is a record that the claim was made; it is not
itself proof that the claim is true, and the individual pages are where that
distinction is argued out. Start anywhere in the wall below, or begin instead with
the [Planes section](/Planes/overview), with the
[Planes Investigation Index](/Planes/Planes_Investigation_Index), which names the
records that would settle each open aircraft question, or with the
[photo cluster these come from](/Photos/Aircraft/overview), which keeps them in
their original sub-clusters.

"""

VIDEO_HEADER = """---
displayed_sidebar: docs
title: "Every Plane Video In One Place"
sidebar_label: "All Plane Videos"
description: "A single scrolling wall of every video in the aircraft investigation — {n} clips, playable in place at their true aspect ratio, each linking to its own page."
hide_table_of_contents: true
---

{{/* Generated by site/build_plane_media_pages.py. Rewritten whole on every run — do not hand-edit. */}}

<a href="/Planes/overview" style={{{{display:'inline-block', marginBottom:'1rem', padding:'0.35rem 0.9rem', background:'#1a73e8', color:'#fff', borderRadius:'4px', textDecoration:'none', fontSize:'0.9rem'}}}}>← Planes</a>

# Every Plane Video In One Place

**{n} videos**, every clip this site holds on aircraft, flight records and the drones
reported over Utah Valley University, on one page and playable where they sit. Nothing
downloads until you press play, each player keeps the clip's real shape rather than
being stretched to the column, and the title under each one opens that video's own
page, where the full transcript, the source post and the argument about what it
actually establishes all live.

These are other people's videos, and a video is a record of what someone said, not a
finding. Several of them contradict each other and at least one contradicts itself
between its first half and its second. **After every fourth clip the page stops for
three sentences on what the flight data itself shows** — each of those blocks points
somewhere new in the [Planes section](/Planes/overview), so reading straight down gets
you the whole aircraft argument as well as the whole video corpus.

"""


def emit_photos():
    items = []
    for root in PHOTO_ROOTS:
        items += collect(os.path.join(DOCS, root), "Img_", IMG_SRC_RE)
    out = [PHOTO_HEADER.format(n=len(items))]
    out.append('<div className="ck-media-wall">')
    out += [photo_tile(it) for it in items]
    out.append("</div>")
    out.append("")
    out.append("## Where these came from")
    out.append("")
    out.append(
        "Every image above is filed in the site's "
        "[Aircraft and Flight Records photo cluster](/Photos/Aircraft/overview), "
        "which keeps them grouped by subject — "
        "[trip histories](/Photos/Aircraft/Trip_History/overview), "
        "[N1098L](/Photos/Aircraft/Planes_N1098L/overview), "
        "[SU-BTT](/Photos/Aircraft/SU_BTT/overview), "
        "[N59906](/Photos/Aircraft/N59906/overview), "
        "[N888KG](/Photos/Aircraft/Planes_N888KG/overview), "
        "[planes following Charlie or Erika](/Photos/Aircraft/Planes_Following_Charlie_Erika/overview) "
        "and the rest. This page is a second route into that same set of files, "
        "not a second copy of them: no image was re-encoded, resized or written to "
        "disk to build it."
    )
    out.append("")
    out.append(
        "The moving-picture equivalent is "
        "[Every Plane Video In One Place](/Planes/Plane-Videos), and both are "
        "introduced together on "
        "[Plane Photos and Videos](/Planes/Plane-Media)."
    )
    out.append("")
    return "\n".join(out), len(items)


def emit_videos():
    items, used = [], 0
    blocks = []
    for root, _label in VIDEO_ROOTS:
        items += collect(os.path.join(DOCS, root), "Vid_", POSTER_RE)
    for i in range(0, len(items), 4):
        chunk = items[i:i + 4]
        blocks.append('<div className="ck-media-wall">\n'
                      + "\n".join(video_tile(it) for it in chunk)
                      + "\n</div>")
        if used < len(INTERLUDES):
            blocks.append('<div className="ck-media-note">\n\n'
                          + INTERLUDES[used] + "\n\n</div>")
            used += 1
    out = [VIDEO_HEADER.format(n=len(items))]
    out.append("\n\n".join(blocks))
    out.append("")
    out.append("## Where these came from")
    out.append("")
    out.append(
        "Every clip above is filed in the site's "
        "[aircraft and flight-record video cluster](/Videos/Vid_Aircraft_Flight_Evidence/overview) "
        "or its [drone video cluster](/Videos/Vid_Drones/overview), which keep "
        "them grouped by subject. This page is a second route into that same set "
        "of files, not a second copy: nothing was re-encoded and no new video "
        "bytes were written to build it, and each player streams from the same "
        "IPFS sources the clip's own page uses."
    )
    out.append("")
    out.append(
        "The still-image equivalent is "
        "[Every Plane Photo In One Place](/Planes/Plane-Photos), and both are "
        "introduced together on "
        "[Plane Photos and Videos](/Planes/Plane-Media)."
    )
    out.append("")
    return "\n".join(out), len(items)


def main():
    check = "--check" in sys.argv
    for name, fn in (("Plane-Photos.mdx", emit_photos),
                     ("Plane-Videos.mdx", emit_videos)):
        body, n = fn()
        path = os.path.join(DOCS, "Planes", name)
        if check:
            old = read(path) if os.path.exists(path) else ""
            print("%-18s %4d items  %s" % (name, n,
                  "unchanged" if old == body else "WOULD CHANGE"))
            continue
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(body)
        print("%-18s %4d items  %5d lines  ->  %s"
              % (name, n, body.count("\n") + 1, path))


if __name__ == "__main__":
    main()
