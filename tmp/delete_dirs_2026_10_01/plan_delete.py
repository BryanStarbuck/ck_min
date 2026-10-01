#!/usr/bin/env python3
"""Plan (and with --execute, perform) removal of site/docs Level 2 dirs.

Step 1: scan everything we KEEP and write keep_images.csv (every image/video it references).
Step 2: scan the dirs we DELETE, list the media only they use, and write delete_media.csv.
Step 3 (--execute): delete the dirs (minus carve-outs) and the delete-only media.
"""
import csv, os, re, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SITE = REPO / "site"
DOCS = SITE / "docs"
STATIC = SITE / "internals" / "static"
OUT = Path(__file__).resolve().parent

DELETE = """Locations Witnesses Videos Iran TPUSA Israel Tyler_Robinson Israel_Main_Suspect
Tyler_Robinson_Not_Assassin key_individuals US_Intelligence Killer US_Intelligence_Assisted
Law_Enforcement UVU gov Suspects Gov_Mind_Control Suspicious government_organizations
technology_surveillance Gun_Bullet Tent hypotheses Theories Topic-Analyses Influencers
intelligence Topics3 social_media_analysis Planes CoverUp political_context Defamation
Proof_Intel_Services distraction_people Proof_Not_Tyler Drones Roof Electrocution
security_law_enforcement FBI Security_Team Photos Other Censorship other_topics Charlie People
Companies_Organizations people_analysis Before Motive cameras Narrative campus_university
organizations_groups analysis_documentation About Medical After meeting""".split()
# Never delete, even though it was in the pasted list.
PROTECTED = {"Timeline"}
# Pages inside a deleted dir that are about the proposed Charlie Kirk disclosure laws.
CARVE_OUTS = [DOCS / "Photos" / "Fix_Laws"]

MEDIA_EXT = r"(?:jpe?g|png|gif|webp|avif|svg|bmp|tiff?|heic|mp4|webm|mov|m4v|mp3|m4a|wav)"
REF_RE = re.compile(r"""["'(=\s]((?:\.{0,2}/|@site/)?[^"'()\s<>{}|]*?\.""" + MEDIA_EXT + r""")(?=["')\s?#}]|$)""", re.I | re.M)
SHA_RE = re.compile(r"\b([0-9a-f]{64})\b")
TEXT_EXT = {".md", ".mdx", ".tsx", ".ts", ".js", ".jsx", ".css", ".json", ".yml", ".yaml", ".html", ".txt"}

assert not (set(DELETE) & PROTECTED) or True
delete_dirs = [DOCS / d for d in DELETE if d not in PROTECTED and (DOCS / d).is_dir()]
missing = [d for d in DELETE if not (DOCS / d).exists()]

def in_any(p, roots):
    return any(p == r or r in p.parents for r in roots)

def is_deleted(p):
    return in_any(p, delete_dirs) and not in_any(p, CARVE_OUTS)

# Index every media file under static + docs by sha256-in-name for frontmatter sha refs.
media_files = [p for base in (STATIC, DOCS) for p in base.rglob("*")
               if p.is_file() and re.search(r"\." + MEDIA_EXT + "$", p.name, re.I)]
by_sha = {}
for p in media_files:
    m = SHA_RE.search(p.name)
    if m:
        by_sha.setdefault(m.group(1), []).append(p)

def resolve(ref, src):
    ref = ref.split("?")[0].split("#")[0]
    if ref.startswith(("http://", "https://", "data:")):
        return []
    cands = []
    if ref.startswith("@site/"):
        cands.append(SITE / ref[6:])
    elif ref.startswith("/"):
        cands += [STATIC / ref[1:], SITE / "static" / ref[1:], DOCS / ref[1:]]
    else:
        cands += [src.parent / ref, STATIC / ref]
    return [c.resolve() for c in cands if c.is_file()]

def refs_of(path):
    try:
        text = path.read_text(errors="ignore")
    except Exception:
        return set()
    found = set()
    for m in REF_RE.finditer(text):
        for r in resolve(m.group(1), path):
            found.add(r)
    for sha in set(SHA_RE.findall(text)):
        for p in by_sha.get(sha, []):
            found.add(p.resolve())
    return found

def text_files(root):
    if root.is_file():
        return [root] if root.suffix in TEXT_EXT else []
    return [p for p in root.rglob("*") if p.is_file() and p.suffix in TEXT_EXT]

# ---- Step 1: KEEP sources -------------------------------------------------
keep_sources = []
for child in DOCS.iterdir():
    if (DOCS / child.name) not in delete_dirs:
        keep_sources += text_files(child)
for c in CARVE_OUTS:
    keep_sources += text_files(c)
for extra in ["src", "blog", "docusaurus.config.ts", "sidebars.ts"]:
    if (SITE / extra).exists():
        keep_sources += text_files(SITE / extra)
keep_sources += [p for p in STATIC.rglob("*") if p.is_file() and p.suffix in {".css", ".html", ".json", ".txt"}]

keep = {}
for src in keep_sources:
    for r in refs_of(src):
        keep.setdefault(r, set()).add(src)
# Media physically inside kept trees are kept too.
for p in media_files:
    rp = p.resolve()
    if DOCS in rp.parents and not is_deleted(rp):
        keep.setdefault(rp, set()).add(rp.parent)

with open(OUT / "keep_images.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["media_path", "referenced_by_count", "example_referrer"])
    for p in sorted(keep):
        srcs = sorted(keep[p])
        w.writerow([str(p.relative_to(REPO)), len(srcs), str(srcs[0].relative_to(REPO))])

# ---- Step 2: DELETE side ----------------------------------------------------
del_refs = {}
for d in delete_dirs:
    for src in text_files(d):
        if is_deleted(src):
            for r in refs_of(src):
                del_refs.setdefault(r, set()).add(src)
# Media referenced by deleted pages and living OUTSIDE deleted dirs, not kept.
delete_media = sorted(p for p in del_refs if p not in keep and not is_deleted(p))
# Media inside deleted dirs that a kept page still needs -> must be rescued.
rescue = sorted(p for p in keep if is_deleted(p))

with open(OUT / "delete_media.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["media_path", "bytes"])
    for p in delete_media:
        w.writerow([str(p.relative_to(REPO)), p.stat().st_size])

print(f"delete dirs: {len(delete_dirs)}  missing from disk: {missing}")
print(f"keep sources scanned: {len(keep_sources)}  keep media: {len(keep)}")
print(f"media referenced by deleted pages: {len(del_refs)}  of which delete-only (outside dirs): {len(delete_media)} "
      f"({sum(p.stat().st_size for p in delete_media)/1e6:.1f} MB)")
print(f"kept media living inside deleted dirs (rescue): {len(rescue)}")
for p in rescue[:20]:
    print("  RESCUE", p.relative_to(REPO))

if "--execute" in sys.argv:
    if rescue:
        sys.exit("refusing: rescue list not empty")
    carve_rel = [str(c.relative_to(REPO)) for c in CARVE_OUTS]
    for d in delete_dirs:
        rel = str(d.relative_to(REPO))
        keep_inside = [c for c in carve_rel if c.startswith(rel + "/")]
        if keep_inside:
            files = subprocess.run(["git", "ls-files", rel], cwd=REPO, capture_output=True, text=True).stdout.split("\n")
            files = [x for x in files if x and not any(x.startswith(k + "/") for k in keep_inside)]
            for i in range(0, len(files), 500):
                subprocess.run(["git", "rm", "-q", "--"] + files[i:i+500], cwd=REPO, check=True)
        else:
            subprocess.run(["git", "rm", "-r", "-q", "--", rel], cwd=REPO, check=True)
    files = [str(p.relative_to(REPO)) for p in delete_media]
    for i in range(0, len(files), 500):
        subprocess.run(["git", "rm", "-q", "--"] + files[i:i+500], cwd=REPO, check=True)
    print("EXECUTED")
