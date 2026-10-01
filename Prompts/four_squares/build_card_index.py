#!/usr/bin/env python3
"""Stage 0 of p_4_squares.md — build card_index.csv, routes.txt, ledger.csv.

Deterministic extraction only. No judgement, no prose. Agents read the output.
"""
import csv, os, re, subprocess, sys, json
from pathlib import Path

ROOT = Path(os.path.expanduser("~/BGit/Bryan_git/charlie-kirk"))
DOCS = ROOT / "site/docs"
EVID = ROOT / "site/internals/static/img/evidence"
WORK = ROOT / "prompts/four_squares"
WORK.mkdir(parents=True, exist_ok=True)

SKIP_TOP = {"Photos", "Videos"}
SKIP_BASENAMES = {"CLAUDE.md"}

# The docs plugin's own exclude list in site/docusaurus.config.ts is the
# authority on what is a published page. Editing a file it excludes is wasted
# work: the page does not exist for any visitor. Mirrored here.
#   "**/_*.{js,jsx,ts,tsx,md,mdx}"   underscore-prefixed files
#   "**/_*/**"                        anything under an underscore directory
#   "**/prompts/**", "**/CLAUDE.md", "**/p_*.{md,mdx}"
import fnmatch


def excluded_by_site(rel_from_docs: str) -> bool:
    parts = rel_from_docs.split("/")
    base = parts[-1]
    if any(seg.startswith("_") for seg in parts[:-1]):
        return True
    if base.startswith("_") or base.startswith("p_"):
        return True
    if base == "CLAUDE.md" or "prompts" in parts[:-1]:
        return True
    return False

# ---------- ban set ----------
def load_ban():
    banned_sha, banned_cid = set(), set()
    for csvp in [ROOT / "images/ban_images.csv", ROOT / "videos/ban_videos.csv"]:
        if not csvp.exists():
            continue
        with open(csvp, newline="", encoding="utf-8") as fh:
            for row in csv.DictReader(fh):
                if (row.get("banned") or "").strip().lower() != "true":
                    continue
                if row.get("sha256"):
                    banned_sha.add(row["sha256"].strip())
                if row.get("cid"):
                    banned_cid.add(row["cid"].strip())
    for txtp in [ROOT / "image_planning/exclude_images.txt",
                 ROOT / "videos_planning/exclude_videos.txt"]:
        if not txtp.exists():
            continue
        for line in txtp.read_text(encoding="utf-8").splitlines():
            tok = line.strip().split()[0] if line.strip() and not line.strip().startswith("#") else ""
            if re.fullmatch(r"[0-9a-f]{64}", tok):
                banned_sha.add(tok)
            elif tok.startswith("Qm"):
                banned_cid.add(tok)
    return banned_sha, banned_cid

BAN_SHA, BAN_CID = load_ban()

# ---------- git tracked set for evidence dir ----------
def tracked_evidence():
    out = subprocess.run(["git", "ls-files", "site/internals/static/img/evidence"],
                         cwd=ROOT, capture_output=True, text=True).stdout
    return {Path(l).name for l in out.splitlines() if l.strip()}

TRACKED = tracked_evidence()

# ---------- image shape cache ----------
SHAPE_CACHE = WORK / "shape_cache.json"
shapes = json.loads(SHAPE_CACHE.read_text()) if SHAPE_CACHE.exists() else {}

def shape_for(fname):
    if fname in shapes:
        return shapes[fname]
    p = EVID / fname
    if not p.exists():
        shapes[fname] = "none"
        return "none"
    r = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(p)],
                       capture_output=True, text=True).stdout
    w = re.search(r"pixelWidth:\s*(\d+)", r)
    h = re.search(r"pixelHeight:\s*(\d+)", r)
    if not (w and h) or int(h.group(1)) == 0:
        shapes[fname] = "none"
    else:
        ratio = int(w.group(1)) / int(h.group(1))
        shapes[fname] = "ck-4sq-side" if ratio < 1.0 else "ck-4sq-stack"
    return shapes[fname]

# ---------- frontmatter ----------
FM_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)

def parse_fm(text):
    m = FM_RE.match(text)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).splitlines():
        mm = re.match(r'^([A-Za-z_]+):\s*(.*)$', line)
        if mm:
            v = mm.group(2).strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                v = v[1:-1]
            fm[mm.group(1)] = v
    return fm, text[m.end():]

IMG_TAG_RE = re.compile(r"<img\b[^>]*>", re.S)
SRC_RE = re.compile(r'src=\{?["\']([^"\']+)["\']')
CID_RE = re.compile(r'data-cid=\{?["\']([^"\']+)["\']')
ALT_RE = re.compile(r'alt=\{?(["\'])(.*?)\1', re.S)
VIDEO_RE = re.compile(r'<(?:video|source)\b[^>]*src=\{?["\'](https?://[^"\']+)["\']', re.S)
POSTER_RE = re.compile(r'poster=\{?["\']([^"\']+)["\']')
VIDPOSTER_RE = re.compile(r'src=\{?["\'](/img/video_posters/[0-9a-f]{64}\.jpg)["\']')

# cid -> sha256, so a video hero can borrow its own poster frame
CID2SHA = {}
try:
    import yaml
    _y = yaml.safe_load(open(ROOT / "videos/videos.yaml"))

    def _walk(n):
        if isinstance(n, dict):
            if n.get("cid") and n.get("sha256"):
                CID2SHA[n["cid"]] = n["sha256"]
            for v in n.values():
                _walk(v)
        elif isinstance(n, list):
            for v in n:
                _walk(v)
    _walk(_y)
except Exception:
    pass

PDIR = ROOT / "site/internals/static/img/video_posters"
TRACKED_POSTERS = {
    Path(l).name for l in subprocess.run(
        ["git", "ls-files", "site/internals/static/img/video_posters"],
        cwd=ROOT, capture_output=True, text=True).stdout.splitlines() if l.strip()}


def poster_shape(fname):
    """A card thumb is an <img>. Never put an .mp4 gateway URL in one."""
    key = "vp/" + fname
    if key in shapes:
        return shapes[key]
    p = PDIR / fname
    if not p.exists():
        shapes[key] = "none"
        return "none"
    r = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(p)],
                       capture_output=True, text=True).stdout
    w = re.search(r"pixelWidth:\s*(\d+)", r)
    h = re.search(r"pixelHeight:\s*(\d+)", r)
    shapes[key] = "none" if not (w and h) or int(h.group(1)) == 0 else (
        "ck-4sq-side" if int(w.group(1)) / int(h.group(1)) < 1.0 else "ck-4sq-stack")
    return shapes[key]


def video_poster(cut, v_match):
    """Resolve a video hero to a still image, or give up and return None."""
    tail = cut[max(0, v_match.start() - 400): v_match.end() + 400]
    for cand in (POSTER_RE.search(tail), VIDPOSTER_RE.search(tail)):
        if cand and "/img/video_posters/" in cand.group(1):
            fn = cand.group(1).rsplit("/", 1)[-1]
            if fn in TRACKED_POSTERS:
                return cand.group(1), fn
    m = re.search(r"(Qm[1-9A-HJ-NP-Za-km-z]{44})", v_match.group(1))
    if m:
        sha = CID2SHA.get(m.group(1))
        if sha and (sha + ".jpg") in TRACKED_POSTERS:
            return f"/img/video_posters/{sha}.jpg", sha + ".jpg"
    return None

def strip_blocks(body, markers):
    cut = body
    for marker in markers:
        i = cut.find(marker)
        if i != -1:
            cut = cut[:i]
    return cut


def _scan(cut):
    for tag in IMG_TAG_RE.finditer(cut):
        t = tag.group(0)
        s = SRC_RE.search(t)
        if not s or "/img/evidence/" not in s.group(1):
            continue
        src = s.group(1)
        fname = src.rsplit("/", 1)[-1]
        sha = fname.split(".")[0]
        cid = (CID_RE.search(t).group(1) if CID_RE.search(t) else "")
        _a = ALT_RE.search(t)
        alt = " ".join(_a.group(2).split()) if _a else ""
        banned = "yes" if (sha in BAN_SHA or (cid and cid in BAN_CID)) else "no"
        if fname not in TRACKED:
            continue  # untracked -> 404s for real visitors
        return "image", src, cid, alt, shape_for(fname), banned
    v = VIDEO_RE.search(cut)
    if v:
        got = video_poster(cut, v)
        if got:
            src, fn = got
            cid = re.search(r"(Qm[1-9A-HJ-NP-Za-km-z]{44})", v.group(1))
            cid = cid.group(1) if cid else ""
            banned = "yes" if (cid and cid in BAN_CID) else "no"
            return "video", src, cid, "", poster_shape(fn), banned
    return None


def find_media(body):
    """Hero media first; fall back to any image the page carries lower down.

    Never looks inside our own four-square blocks - those hold OTHER pages' media.
    """
    own_blocks = ("CK_4SQ_SECTION_START", "CK_4SQ_SITEWIDE_START", "CK_INTERESTING_HERE_START")
    hero = _scan(strip_blocks(body, own_blocks + ("CK_PLACED_IMAGES_START",)))
    if hero:
        return hero
    rest = re.split(r"CK_4SQ_(?:SECTION|SITEWIDE)_START.*?CK_4SQ_(?:SECTION|SITEWIDE)_END", body, flags=re.S)
    for chunk in rest:
        got = _scan(chunk)
        if got:
            return got
    return "none", "", "", "", "none", "no"

# The anchor is the EARLIEST of these in the file, by character position - not
# the first entry of a priority list. On 116 pages the author credit sits BELOW
# the page's own "## Interesting" or "## Related Areas", and priority order put
# the new blocks underneath those sections instead of above them, which is the
# opposite of the intended reading order.
ANCHOR_FINDERS = [
    ("CK_AUTHOR_CREDIT", lambda t: t.find("CK_AUTHOR_CREDIT")),
    ("H2_INTERESTING", lambda t: (lambda m: m.start() if m else -1)(
        re.search(r"^## Interesting\s*$", t, re.M))),
    ("H2_RELATED_AREAS", lambda t: (lambda m: m.start() if m else -1)(
        re.search(r"^## Related Areas\s*$", t, re.M))),
    ("CK_PLACED_IMAGES", lambda t: t.find("CK_PLACED_IMAGES_START")),
    ("H2_SOURCES", lambda t: (lambda m: m.start() if m else -1)(
        re.search(r"^## (Sources|Fix Laws|The Laws)\s*$", t, re.M))),
]


def pick_anchor(t):
    """Strip our own blocks first, so a previous run's output is not an anchor."""
    clean = re.sub(r"(?:\{/\*|<!--)\s*CK_(?:INTERESTING_HERE|INTERESTING_OTHER|4SQ_SECTION|4SQ_SITEWIDE)_START"
                   r".*?CK_(?:INTERESTING_HERE|INTERESTING_OTHER|4SQ_SECTION|4SQ_SITEWIDE)_END\s*(?:\*/\}|-->)",
                   "", t, flags=re.S)
    found = [(name, fn(clean)) for name, fn in ANCHOR_FINDERS]
    found = [(n, i) for n, i in found if i != -1]
    return min(found, key=lambda x: x[1])[0] if found else "EOF"

# ---------- pages.csv lookup ----------
pages_meta = {}
with open(ROOT / "pages.csv", newline="", encoding="utf-8") as fh:
    for row in csv.DictReader(fh):
        pages_meta.setdefault(row["file_path"], row)

# Real built routes are the authority. Filename-derived routes were wrong twice:
# a leading year/number is not always a Docusaurus number prefix (99-0004-Vance,
# 2026-03-10-seal-motion keep theirs), and frontmatter id:/slug: overrides the
# filename outright (court/mirandize/overview.md -> /court/mirandize/mirandize-overview).
_ROUTES_FILE = WORK / "routes.txt"
BUILT = set()
if _ROUTES_FILE.exists():
    BUILT = {l for l in _ROUTES_FILE.read_text().splitlines() if l}
BY_PARENT = {}
for _r in BUILT:
    BY_PARENT.setdefault(_r.rpartition("/")[0], []).append(_r)


def url_for(rel, fm=None):
    """rel is like site/docs/Foo/bar.mdx; fm is its parsed frontmatter."""
    p = rel[len("site/docs/"):]
    p = re.sub(r"\.mdx?$", "", p)
    parts = p.split("/")
    stem = parts[-1]
    parent = "/" + "/".join(parts[:-1]) if len(parts) > 1 else ""

    # 1. explicit slug/id wins, exactly as Docusaurus applies it
    if fm:
        slug = fm.get("slug")
        if slug:
            return slug if slug.startswith("/") else f"{parent}/{slug}"
        ident = fm.get("id")
        if ident:
            cand = f"{parent}/{ident}"
            if not BUILT or cand in BUILT:
                return cand

    # 2. the filename as-is, if the build serves it
    cand = f"{parent}/{stem}" if parent else f"/{stem}"
    if stem in ("README",):
        cand = parent or "/"
    if not BUILT or cand in BUILT:
        return cand

    # 3a. Docusaurus strips numeric prefixes from DIRECTORY segments too
    #     (laws/2_US_Intel/... serves /laws/US_Intel/...), so try the whole path
    #     with every segment de-prefixed.
    if BUILT:
        deprefixed = "/" + "/".join(re.sub(r"^\d+[-_.]", "", x) for x in parts)
        if deprefixed in BUILT:
            return deprefixed
        dp_parent = "/" + "/".join(re.sub(r"^\d+[-_.]", "", x) for x in parts[:-1])
        for want in (stem, re.sub(r"^\d+[-_.]", "", stem)):
            cand2 = f"{dp_parent}/{want}"
            if cand2 in BUILT:
                return cand2

    # 3b. otherwise the one built route in this directory that matches the stem
    #     with or without a stripped numeric prefix
    sibs = BY_PARENT.get(parent, [])
    stripped = re.sub(r"^\d+[-_.]", "", stem)
    for want in (stem, stripped):
        hits = [r for r in sibs
                if r.rpartition("/")[2] == want
                or re.fullmatch(r"[\d._-]*" + re.escape(want), r.rpartition("/")[2])]
        if len(hits) == 1:
            return hits[0]
    return cand

rows, routes, ledger = [], set(), []
for dirpath, dirnames, filenames in os.walk(DOCS):
    rel_dir = os.path.relpath(dirpath, DOCS)
    top = rel_dir.split(os.sep)[0]
    if top in SKIP_TOP:
        dirnames[:] = []
        continue
    dirnames[:] = [d for d in dirnames if not (rel_dir == "." and d in SKIP_TOP)]
    for fn in sorted(filenames):
        if not fn.endswith((".md", ".mdx")):
            continue
        if fn in SKIP_BASENAMES:
            continue
        rel_from_docs = os.path.relpath(os.path.join(dirpath, fn), DOCS).replace(os.sep, "/")
        if excluded_by_site(rel_from_docs):
            continue
        full = Path(dirpath) / fn
        rel = str(full.relative_to(ROOT))
        text = full.read_text(encoding="utf-8", errors="replace")
        fm, body = parse_fm(text)
        url = url_for(rel, fm)
        routes.add(url)
        base = fn.rsplit(".", 1)[0]
        is_overview = base in ("overview", "README")
        if is_overview:
            routes.add(url.rsplit("/overview", 1)[0] if url.endswith("/overview") else url)
        if rel_dir == ".":
            if base == "index":
                continue  # site root index: link target only
            level2 = base
        else:
            level2 = rel_dir.split(os.sep)[0]
        meta = pages_meta.get(rel, {})
        csv_level2 = meta.get("level2_parent") or ""
        title = fm.get("title") or meta.get("title") or ""
        if not title:
            m = re.search(r"^#\s+(.+)$", body, re.M)
            title = m.group(1).strip() if m else base.replace("-", " ").replace("_", " ")
        kind, src, cid, alt, shape, banned = find_media(body)
        # A video hero borrows a poster frame, which carries no alt of its own.
        # An empty alt on a card thumb is an accessibility hole, so name the page.
        if kind == "video" and not alt.strip():
            alt = "Video still from " + re.sub(r"\s+", " ", title).strip()
        anchor = pick_anchor(text)
        rows.append({
            "url_path": url,
            "file_path": rel,
            "extension": fn.rsplit(".", 1)[1],
            "level": meta.get("level", "3" if rel_dir != "." else "2"),
            "level2": level2,
            "csv_level2": csv_level2,
            "is_overview": "yes" if is_overview else "no",
            "title": title,
            "sidebar_label": fm.get("sidebar_label") or meta.get("sidebar_label") or title,
            "description": (fm.get("description") or meta.get("description") or "").replace("\n", " "),
            "media_kind": kind,
            "media_src": src,
            "media_cid": cid,
            "media_alt": alt,
            "media_shape": shape,
            "banned": banned,
            "anchor": anchor,
            "teaser": "",
        })
        ledger.append({"file_path": rel, "level2": rows[-1]["level2"],
                       "status": "TODO", "blocks": "----", "agent": "", "updated": ""})

SHAPE_CACHE.write_text(json.dumps(shapes))

# routes: also every /Photos + /Videos leaf, as link targets
for top in SKIP_TOP:
    d = DOCS / top
    if d.exists():
        for p in d.rglob("*.md*"):
            routes.add(url_for(str(p.relative_to(ROOT))))

prev_led, prev_teaser = {}, {}
_lp, _cp = WORK / "ledger.csv", WORK / "card_index.csv"
if _lp.exists():
    with open(_lp, newline="", encoding="utf-8") as fh:
        prev_led = {r["file_path"]: r for r in csv.DictReader(fh)}
if _cp.exists():
    with open(_cp, newline="", encoding="utf-8") as fh:
        prev_teaser = {r["url_path"]: r.get("teaser", "") for r in csv.DictReader(fh)}
for r in rows:
    if prev_teaser.get(r["url_path"]):
        r["teaser"] = prev_teaser[r["url_path"]]
for r in ledger:
    old = prev_led.get(r["file_path"])
    if old:
        r.update({k: old[k] for k in ("status", "blocks", "agent", "updated") if old.get(k)})

with open(WORK / "card_index.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), quoting=csv.QUOTE_MINIMAL)
    w.writeheader(); w.writerows(rows)

# routes.txt is OWNED BY build_routes.py, which reads the real build output.
# This script used to overwrite it with filename-derived routes, which silently
# reintroduced every prefix/slug error the build-derived file had just fixed.
# Write a side file instead so the two can be diffed when something looks off.
(WORK / "routes_derived.txt").write_text("\n".join(sorted(routes)) + "\n")

with open(WORK / "ledger.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=["file_path", "level2", "status", "blocks", "agent", "updated"])
    w.writeheader(); w.writerows(ledger)

from collections import Counter
c = Counter(r["level2"] for r in rows)
print(f"pages indexed : {len(rows)}")
print(f"routes        : {len(routes)}")
print(f"with media    : {sum(1 for r in rows if r['media_kind'] != 'none')}")
print(f"banned media  : {sum(1 for r in rows if r['banned'] == 'yes')}")
print(f"level2 areas  : {len(c)}")
print("anchors       :", dict(Counter(r["anchor"] for r in rows)))
