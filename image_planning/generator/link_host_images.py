#!/usr/bin/env python3
"""Stage 5 of p_yaml_to_site.md — make each image's inline copies on its host
pages CLICKABLE, linking to that image's Photos image page.

Link-only: wraps the single matched <img>/markdown-image in an anchor to the
image's Photos page URL. Never changes prose, src, alt, sizing, siblings, or the
YAML. Idempotent: skips an <img> already wrapped to the same URL; never clobbers
a pre-existing human anchor to a different target; never double-wraps.

Run with --apply to write. Default is a dry run that only reports.
"""
import csv, os, re, sys
import yaml

ROOT = os.path.expanduser("~/BGit/Bryan_git/charlie-kirk")
YAML_PATH = os.path.join(ROOT, "images", "images.yaml")
DOCS = os.path.join(ROOT, "site", "docs")
PHOTOS = os.path.join(DOCS, "Photos")
PAGES_CSV = os.path.join(ROOT, "pages.csv")
EXCLUDE_FILE = os.path.join(ROOT, "image_planning", "exclude_images.txt")
TILDE_DOCS = "~/BGit/Bryan_git/charlie-kirk/site/docs"

APPLY = "--apply" in sys.argv

# ---------- exclusion gate ----------
EXCLUDED = set()
if os.path.exists(EXCLUDE_FILE):
    for line in open(EXCLUDE_FILE, encoding="utf-8"):
        line = line.split("#", 1)[0].strip()
        if re.fullmatch(r"[0-9a-f]{64}", line):
            EXCLUDED.add(line)

# ---------- pages.csv url lookup ----------
csv_url_by_file = {}
with open(PAGES_CSV, newline="") as f:
    for r in csv.DictReader(f):
        csv_url_by_file[r["file_path"]] = r["url_path"]


def image_page_url(image_page):
    """Tilde path under site/docs -> site-relative /path (drop .mdx), confirmed
    against pages.csv where possible."""
    p = os.path.expanduser(image_page)
    if not p.startswith(os.path.join(ROOT, "site", "docs")):
        return None
    rel = os.path.relpath(p, os.path.join(ROOT, "site", "docs"))
    url = "/" + re.sub(r"\.mdx?$", "", rel)
    csv_file = "site/docs/" + rel
    csv_url = csv_url_by_file.get(csv_file)
    if csv_url and csv_url != url:
        return csv_url
    return url


def host_rel(page):
    p = os.path.expanduser(str(page))
    if p.startswith(ROOT + os.sep):
        p = os.path.relpath(p, ROOT)
    return p


# ---------- collect media entries with a real image page + host pages ----------
with open(YAML_PATH) as f:
    data = yaml.safe_load(f)

# host page (repo-rel) -> list of {cid, sha, stem, url}
host_map = {}
n_entries = 0


def walk(node):
    global n_entries
    if not isinstance(node, dict):
        return
    for coll in ("images", "videos"):
        for it in node.get(coll) or []:
            i = it.get("image", it.get("video", it))
            if not isinstance(i, dict):
                continue
            sha = i.get("sha256") or ""
            if sha in EXCLUDED:
                continue
            # Video entries are filtered out here by the image_page gate below:
            # bind_image_pages.py forces image_page = "" on anything that types
            # as video, because /Photos is the still-image Level 2 and a video's
            # page lives under site/docs/Videos. Keep that invariant — if this
            # script ever stops requiring image_page, it needs its own media-type
            # check, or it will wrap an <img> anchor around an .mp4.
            ip = i.get("image_page") or ""
            ops = i.get("on_pages") or []
            if not ip or not ops:
                continue
            url = image_page_url(ip)
            if not url:
                continue
            cid = i.get("cid") or ""
            stem = os.path.splitext(os.path.basename(i.get("file_path") or ""))[0]
            n_entries += 1
            seen = set()
            for hp in ops:
                page = hp.get("page") if isinstance(hp, dict) else hp
                if not page:
                    continue
                rel = host_rel(page)
                if rel.startswith("site/docs/Photos/"):
                    continue  # never edit Photos pages here
                if rel in seen:
                    continue
                seen.add(rel)
                host_map.setdefault(rel, []).append(
                    {"cid": cid, "sha": sha, "stem": stem, "url": url})
    # recurse into level_N children
    for k, v in node.items():
        if re.fullmatch(r"level_\d+", k) and isinstance(v, list):
            for child in v:
                if isinstance(child, dict):
                    inner = child.get(k, child)
                    walk(inner)


for item in data.get("level_3") or []:
    walk(item.get("level_3", item))

# ---------- edit host pages ----------
IMG_TAG = re.compile(r"<img\b[^>]*?/?>", re.I)
MD_IMG = re.compile(r"!\[[^\]]*\]\(([^)\s]+)[^)]*\)")

linked = already = no_match = preexisting = 0
missing_pages = []
preexisting_list = []
no_match_list = []
edited_pages = 0


def src_of(tag):
    m = re.search(r'src\s*=\s*"([^"]*)"', tag) or re.search(r"src\s*=\s*'([^']*)'", tag)
    return m.group(1) if m else ""


for rel in sorted(host_map):
    fp = os.path.join(ROOT, rel)
    if not os.path.isfile(fp):
        missing_pages.append(rel)
        continue
    with open(fp, encoding="utf-8") as f:
        text = f.read()
    orig = text
    for ent in host_map[rel]:
        cid, sha, stem, url = ent["cid"], ent["sha"], ent["stem"], ent["url"]

        def identifies(s):
            s = s or ""
            if cid and cid in s:
                return True
            if sha and sha in s:
                return True
            return False

        # find matching <img> tag
        target = None
        for m in IMG_TAG.finditer(text):
            if identifies(m.group(0)):
                target = m
                break
        if target:
            start, end = target.start(), target.end()
            before = text[:start]
            # already wrapped to same url?
            am = re.search(r'<a\b[^>]*href\s*=\s*"([^"]*)"[^>]*>\s*$', before)
            if am:
                if am.group(1) == url:
                    already += 1
                    continue
                # human-placed anchor to a different target — do not clobber
                preexisting += 1
                preexisting_list.append(f"{rel} -> {am.group(1)} (wanted {url})")
                continue
            new = f'<a href="{url}">' + text[start:end] + "</a>"
            text = before + new + text[end:]
            linked += 1
            continue
        # markdown image fallback (CID/sha in URL)
        md_target = None
        for m in MD_IMG.finditer(text):
            if identifies(m.group(1)):
                md_target = m
                break
        if md_target:
            start, end = md_target.start(), md_target.end()
            before = text[:start]
            if before.rstrip().endswith("[") or re.search(r'\]\([^)]*\)\s*$', "") :
                pass
            # already wrapped? pattern [![..](..)](url)
            after = text[end:end+200]
            if before.endswith("[") and after.lstrip().startswith("]("):
                # extract existing url
                em = re.match(r"\s*\]\(([^)]+)\)", after)
                if em and em.group(1) == url:
                    already += 1
                    continue
                elif em:
                    preexisting += 1
                    preexisting_list.append(f"{rel} -> {em.group(1)} (md, wanted {url})")
                    continue
            new = "[" + text[start:end] + f"]({url})"
            text = before + new + text[end:]
            linked += 1
            continue
        no_match += 1
        no_match_list.append(f"{rel}: {cid or sha or stem}")
    if text != orig:
        edited_pages += 1
        if APPLY:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(text)

print("============================")
print("STAGE 5", "(APPLIED)" if APPLY else "(DRY RUN)")
print(f"Media entries with image_page + on_pages: {n_entries}")
print(f"Host pages in map: {len(host_map)}   host pages edited: {edited_pages}")
print(f"Image embeds linked: {linked}   already linked: {already}")
print(f"Claimed hosts with no matching embed: {no_match}")
print(f"Pre-existing anchors left intact: {preexisting}")
if missing_pages:
    print(f"Host pages not found on disk: {len(missing_pages)}")
    for m in missing_pages[:10]:
        print("   -", m)
if preexisting_list:
    print("Pre-existing anchors (review):")
    for m in preexisting_list[:20]:
        print("   -", m)
if no_match_list:
    print("No-match sample:")
    for m in no_match_list[:20]:
        print("   -", m)
print("============================")
