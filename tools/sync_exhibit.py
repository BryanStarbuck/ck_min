#!/usr/bin/env python3
"""
sync_exhibit.py — copy the Exhibit 11 area (analysis page + 3D Body Tour) from the
charlie-kirk repo into this repo, and point its links at pages this site has.

charlie-kirk is the source of truth. This script only ever READS it. It copies:

    charlie-kirk/site/docs/scorecard/exhibit/*            -> site/docs/scorecard/exhibit/
    charlie-kirk/site/internals/static/scorecard/exhibit/ -> site/internals/static/scorecard/exhibit/

(the static half is served at /scorecard/exhibit/: body_tour.html, one page per body
part, overview.html = the State's Exhibit 11 page, and body_tour_assets/). Every
file is overwritten on each run except the directory's CLAUDE.md, which is
human-owned: it is copied only if this repo has none.

WHY THE LINKS ARE REWRITTEN
  The Exhibit 11 pages cite ~20 pages that live in charlie-kirk but were removed
  from this site in the 2026-10-01 trim (all of Medical/, and scorecard/ apart
  from exhibit/). Copied as-is, every one of those links 404s on the live site.
  So, on the copies only:
    * a dead link is pointed at the page here that covers the SAME subject, and
      its link text is changed to name that page;
    * where this site has no such page, the link is removed (a footer list item
      goes; in a "Sources:" line the item goes, the step text still names the
      person or document it relies on).
  Never point a citation at a page that does not hold the fact it backs.

    python3 tools/sync_exhibit.py            copy, rewrite, then audit every link
    python3 tools/sync_exhibit.py --check    audit only (no copy)

The audit exits 1 if any link in the copied files still points at a page or file
this site does not have. When charlie-kirk adds a new link to a removed page, add a
rule below (EXACT, SRC_MAP, LI_MAP, OTHER_MAP or MDX_EXACT) and re-run.
"""
import re
import shutil
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
SRC_ROOT = Path.home() / "BGit/Bryan_git/charlie-kirk"
REL_DOCS = Path("site/docs/scorecard/exhibit")
REL_STATIC = Path("site/internals/static/scorecard/exhibit")
DOCS_DIR = ROOT_DIR / "site/docs"
STATIC_DIR = ROOT_DIR / "site/internals/static"

ANALYSIS = "/scorecard/exhibit/analysis"
Q7 = ANALYSIS + "#question-7-do-these-injuries-point-more-to-a-blasts-pressure-wave-than-to-a-bullet"
EACH_INJURY = ANALYSIS + "#each-injury-in-plain-english"
EXHIBIT = "/scorecard/exhibit/overview.html"
TOUR = "/scorecard/exhibit/body_tour.html"
DAY_4 = "/court/Preliminary_Hearing/Day_4"

NAR = "/scorecard/Not_A_Rifle_Wound/"
CAM = "/scorecard/Charge_At_The_Mic/"
DROP = None

# ---------------------------------------------------------------- HTML pages
# 1. Exact replacements, applied first, for links whose right target depends on
#    the sentence around them. (old, new)
EXACT = [
    ('<a class="back" href="/scorecard/overview">← Scorecard</a>',
     '<a class="back" href="/">← Home</a>'),
    # neck: the entrance-wound step
    (f'Sources: <a href="{NAR}Details/Wound_Record">The Wound on the Record</a> · '
     '<a href="/Medical/missing_spinal_cord_question">the witness statement</a>',
     f'Source: <a href="{EXHIBIT}#entrance">State\'s Exhibit 11, as quoted</a>'),
    # neck: the "front to back ... downward" step
    (f'Sources: <a href="{NAR}Details/Wound_Record">The Wound on the Record</a> · '
     f'<a href="{ANALYSIS}">',
     f'Sources: <a href="{EXHIBIT}#trajectory">The State\'s brief: its one-line direction</a> · '
     f'<a href="{ANALYSIS}">'),
    # spine: what the report says happened here
    (f'<p class="bt-src">Source: <a href="{NAR}Details/Wound_Record">The Wound on the Record</a></p>',
     f'<p class="bt-src">Source: <a href="{EXHIBIT}#cord-absent">State\'s Exhibit 11, as quoted</a></p>'),
    # spine: the security head relaying a doctor (not on the Exhibit 11 page)
    (f'Source: <a href="{NAR}Details/Wound_Record">The Wound on the Record</a> '
     '(Brian Harpole, Shawn Ryan Show, Nov. 17, 2025, relaying a doctor)',
     'Source: Brian Harpole, Shawn Ryan Show, Nov. 17, 2025, relaying a doctor'),
    # lungs: Jon Bray's 53 Hz sound work. No page here holds it; the step text
    # already names him and says no lab has tested it.
    (f'\n            <p class="bt-src">Source: <a href="{CAM}Expert_Found_Transmitter">Expert Found Transmitter</a></p>',
     ''),
]

# 2. Links inside <p class="bt-src"> "Source(s):" lines: target -> (href, label) | DROP
SRC_MAP = {
    NAR + "Details/Wound_Record": (EXHIBIT, "State's Exhibit 11, as quoted"),
    NAR + "Side_To_Side": (EXHIBIT + "#perforated", "State's Exhibit 11: the ordered list"),
    NAR + "Wrong_Angle": (DAY_4, "preliminary hearing, Day 4"),
    NAR + "Too_Little_Damage": ("/court/ai_attorney/mechanism-of-death-explosive",
                                "The mechanism of death: an explosive, not a rifle round"),
    NAR + "No_Ballistic_Match": ("/court/ballistics-atf-cbla", "Ballistics: the ATF's inconclusive comparison"),
    CAM + "Transmitter_Under_Shirt": ("/Mic/rode-wireless-mic", "The RØDE Wireless PRO on his shirt"),
    CAM + "Expert_Found_Transmitter": ("/Mic/mic-explosion-video-analysis", "Jon Bray's video frame analysis"),
    CAM + "Shirt_Moves_First": ("/Mic/six-forensic-physics-phenomena", "Ali Zreik's six forensic physics phenomena"),
    "/Medical/shape_charge_vs_bullet": (Q7, "Exhibit 11 Analysis: bullet versus blast"),
    "/Medical/missing_spinal_cord_question": (EACH_INJURY, "Exhibit 11 Analysis: the spinal cord"),
    "/Medical/state_brief_trajectory_contradiction": (EACH_INJURY, "Exhibit 11 Analysis: the neck bones"),
    "/Medical/charlie_trip_to_hospital": ("/Timeline/medical-death-timeline",
                                          "Shot to pronouncement: the medical timeline"),
    "/Medical/doctors_question_me_report": DROP,
}

# 3. Footer list items (<li> holding one link). Every footer already lists the
#    Exhibit 11 page and the analysis, so most dead items simply go.
LI_MAP = {
    NAR + "Details/Wound_Record": DROP,
    NAR + "Side_To_Side": DROP,
    NAR + "Injuries_Dont_Fit": DROP,
    NAR + "Wrong_Angle": (DAY_4, "Preliminary hearing, Day 4: the sworn distance and height of the roof"),
    "/Medical/shape_charge_vs_bullet": DROP,
    "/Medical/charlies_injuries": DROP,
    "/Medical/missing_spinal_cord_question": DROP,
    "/Medical/doctors_question_me_report": DROP,
    "/Medical/charlie_trip_to_hospital": ("/Timeline/medical-death-timeline",
                                          "Shot to pronouncement: the medical timeline and the CPR accounts"),
    "/Medical/charlie_kirk_medical_examiner_report": ("/Timeline/autopsy-forensic-timeline",
                                                      "Autopsy and medical examiner timeline"),
}

# 4. Anywhere else (body_tour.html's "Where these words come from" line).
OTHER_MAP = {
    NAR + "Side_To_Side": DROP,
    NAR + "overview": ("/Cause_of_Death/overview", "Cause of Death"),
}

# ---------------------------------------------------------------- analysis.mdx
ATF = "[the ATF ballistics record](/court/ballistics-atf-cbla)"
BT = lambda page, name: f'<a href="/scorecard/exhibit/{page}.html">the {name} page of the Body Tour</a>'
MDX_EXACT = [
    # top button: the trimmed Side to Side page -> the Body Tour
    ('<a href="/scorecard/Not_A_Rifle_Wound/Side_To_Side" style=', f'<a href="{TOUR}" style='),
    ("← Side to Side, Not Front to Back</a>", "Body Tour (3D) →</a>"),
    (f"([the wound on the record]({NAR}Details/Wound_Record))", f"({ATF})"),
    (f"Line by line, with the testimony: [The Wound on the Record]({NAR}Details/Wound_Record).",
     f'Every quoted line, highlighted: <a href="{EXHIBIT}">the Exhibit 11 page</a>.'),
    ('in 2009 ([shape charge versus bullet](/Medical/shape_charge_vs_bullet))', f'in 2009 ({BT("brain", "Brain")})'),
    (f"([The Angle Is Wrong]({NAR}Wrong_Angle))", f'({BT("spine", "Spine")})'),
    ("([the missing spinal cord](/Medical/missing_spinal_cord_question))", f'({BT("spine", "Spine")})'),
    ("the edge ([shape charge versus bullet](/Medical/shape_charge_vs_bullet))", f'the edge ({BT("neck", "Neck")})'),
    (f"([Side to Side]({NAR}Side_To_Side))", f'({BT("neck", "Neck")})'),
    ("([the trip to the hospital](/Medical/charlie_trip_to_hospital))",
     "([shot to pronouncement: the medical timeline](/Timeline/medical-death-timeline))"),
    # "Where the evidence lives"
    (f"* [The Wound on the Record]({NAR}Details/Wound_Record) — every quoted line of Exhibit 11 and the sworn testimony, word for word",
     f'* <a href="{TOUR}">Body Tour (3D)</a> — each injured body part drawn in 3D and tested two ways: as a bullet, and as a shaped charge'),
    (f"* [Side to Side, Not Front to Back]({NAR}Side_To_Side) — the order of the damage, read against the State's one-line direction",
     "* [Ballistics: the ATF's inconclusive comparison](/court/ballistics-atf-cbla) — the recovered fragments against the rifle"),
    ("* [Charlie's injuries, term by term](/Medical/charlies_injuries) and [shape charge versus bullet](/Medical/shape_charge_vs_bullet) — the same findings, scored finding by finding",
     "* [Autopsy, forensic and medical examiner timeline](/Timeline/autopsy-forensic-timeline) — the autopsy, the examiner, and the conflicting wound descriptions, in order"),
    # "Related Areas"
    (f"* [Not a Rifle Wound]({NAR}overview)", f'* <a href="{TOUR}">Body Tour (3D)</a>'),
    ("* [The medical examiner's report](/Medical/charlie_kirk_medical_examiner_report)",
     "* [Autopsy and medical examiner timeline](/Timeline/autopsy-forensic-timeline)"),
    ("* [Why the autopsy report is not public](/Medical/autopsy_report_not_public)",
     "* [Gag orders and sealing](/court/gag-orders-sealing)"),
    ("* [Doctors question the report](/Medical/doctors_question_me_report)", "* [The Microphone](/Mic/overview)"),
    ("* [The Scorecard](/scorecard/overview)", "* [Court & Trial](/court/overview)"),
]

ANCHOR_RE = re.compile(r'<a href="([^"#]*)(#[^"]*)?">([^<]*)</a>')
LI_RE = re.compile(r'^(\s*)<li><a href="([^"#]*)(?:#[^"]*)?">[^<]*</a></li>$')
SRC_LINE_RE = re.compile(r'^(\s*<p class="bt-src">)Sources?: (.*?)</p>$')

used = set()


def apply_exact(text, rules):
    for old, new in rules:
        if old in text:
            text = text.replace(old, new)
            used.add(old)
    return text


def remap(line, table):
    """Rewrite every anchor in line whose target is in table; DROP removes it."""
    def sub(m):
        target = m.group(1)
        if target not in table:
            return m.group(0)
        rule = table[target]
        return "\x00" if rule is DROP else f'<a href="{rule[0]}">{rule[1]}</a>'
    line = ANCHOR_RE.sub(sub, line)
    # a dropped link takes one " · " separator with it
    line = re.sub(r"( · )?\x00( · )?", lambda m: " · " if m.group(1) and m.group(2) else "", line)
    return line


def fix_src_line(line):
    """Rewrite a Sources line, drop repeated targets, fix Source/Sources."""
    m = SRC_LINE_RE.match(line)
    if not m:
        return remap(line, SRC_MAP)
    items, seen = [], set()
    for item in remap(m.group(2), SRC_MAP).split(" · "):
        href = re.search(r'href="([^"]*)"', item)
        key = href.group(1) if href else item.strip()
        if item.strip() and key not in seen:
            seen.add(key)
            items.append(item)
    if not items:
        return None
    return f'{m.group(1)}{"Sources" if len(items) > 1 else "Source"}: {" · ".join(items)}</p>'


def rewrite_html(text):
    text = apply_exact(text, EXACT)
    out, seen_li = [], set()
    for line in text.split("\n"):
        if "<ul" in line:
            seen_li = set()
        li = LI_RE.match(line)
        if 'class="bt-src"' in line:
            line = fix_src_line(line)
        elif li:
            rule = LI_MAP.get(li.group(2), "keep")
            if rule is DROP:
                continue
            if rule != "keep":
                line = f'{li.group(1)}<li><a href="{rule[0]}">{rule[1]}</a></li>'
            key = LI_RE.match(line).group(2).replace(EXHIBIT, "overview.html")
            if key in seen_li:
                continue
            seen_li.add(key)
        else:
            line = remap(line, OTHER_MAP)
        if line is not None:
            out.append(line)
    return "\n".join(out)


def copy_and_rewrite():
    if not SRC_ROOT.is_dir():
        sys.exit(f"source repo not found: {SRC_ROOT}")
    dst_docs, dst_static = ROOT_DIR / REL_DOCS, ROOT_DIR / REL_STATIC
    dst_docs.mkdir(parents=True, exist_ok=True)
    for f in sorted((SRC_ROOT / REL_DOCS).iterdir()):
        if not f.is_file():
            continue
        dst = dst_docs / f.name
        # CLAUDE.md files are human-owned: copy it the first time, never overwrite.
        if f.name == "CLAUDE.md" and dst.exists():
            if dst.read_bytes() != f.read_bytes():
                print(f"note: {dst.relative_to(ROOT_DIR)} differs from charlie-kirk's; left as is")
            continue
        shutil.copy2(f, dst)
    shutil.copytree(SRC_ROOT / REL_STATIC, dst_static, dirs_exist_ok=True)

    for f in sorted(dst_static.glob("*.html")):
        f.write_text(rewrite_html(f.read_text(encoding="utf-8")), encoding="utf-8")
    analysis = dst_docs / "analysis.mdx"
    analysis.write_text(apply_exact(analysis.read_text(encoding="utf-8"), MDX_EXACT), encoding="utf-8")
    for old, _ in EXACT + MDX_EXACT:
        if old not in used:
            print(f"note: rule matched nothing (source changed?): {old.strip()[:100]}")


def route_exists(path):
    path = path.split("#")[0].split("?")[0].rstrip("/") or "/"
    if path == "/" or (STATIC_DIR / path.lstrip("/")).is_file():
        return True
    base = DOCS_DIR / path.lstrip("/")
    return any(Path(str(base) + ext).is_file() for ext in (".md", ".mdx")) or \
        any((base / f"index{ext}").is_file() for ext in (".md", ".mdx"))


def audit():
    dst_static = ROOT_DIR / REL_STATIC
    bad = []
    files = sorted(dst_static.glob("*.html")) + [ROOT_DIR / REL_DOCS / "analysis.mdx"]
    for f in files:
        text = f.read_text(encoding="utf-8")
        links = re.findall(r'(?:href|src)="([^"]+)"', text) + re.findall(r"\]\((/[^)\s]+)\)", text)
        for link in links:
            if link.startswith(("http", "#", "mailto:", "${")):
                continue
            ok = route_exists(link) if link.startswith("/") else \
                (dst_static / link.split("#")[0]).is_file()
            if not ok:
                bad.append(f"{f.relative_to(ROOT_DIR)}: {link}")
    for b in sorted(set(bad)):
        print("DEAD LINK", b)
    print(f"audit: {len(files)} files, {len(set(bad))} dead links")
    return not bad


if __name__ == "__main__":
    if "--check" not in sys.argv:
        copy_and_rewrite()
    sys.exit(0 if audit() else 1)
