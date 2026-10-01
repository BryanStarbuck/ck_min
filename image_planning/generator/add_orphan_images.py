#!/usr/bin/env python3
# add_orphan_images.py — file down every image file on disk that images/images.yaml
# does not know about yet.
#
# grow_hierarchy.py only ingests images that are EMBEDDED ON A SITE PAGE (its Stage 6
# is a page sweep). An image that was downloaded but never placed on a page is
# therefore invisible to it and never gets an entry. This script closes that gap:
# it walks the image directories, hashes every file, and appends any sha256 that is
# not already in the hierarchy to the 'Unfiled_Backlog' level_3 node — the bucket
# that exists precisely for images not yet filed under a topic.
#
# Grow-only, exactly like grow_hierarchy.py: never deletes or reorders an entry, and
# never touches an entry that already exists.
#
# Run order:  grow_hierarchy.py  ->  add_orphan_images.py  ->  bind_image_pages.py
#
# The emitter below is a copy of the one in bind_image_pages.py and MUST stay
# identical to it. In particular on_pages / should_be_on_pages are lists of
# {page: ...} MAPPINGS and an empty one round-trips as []. Emitting them through a
# generic list branch stringifies the dicts and drops the empty ones; that bug in
# grow_hierarchy.py mangled 1,693 entries on 2026-08-12.
import os, re, sys, hashlib, yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sanitize_common import q_prose, q_identity

ROOT = os.path.expanduser('~/BGit/Bryan_git/charlie-kirk')
HOME = os.path.expanduser('~')
YAML_PATH = os.path.join(ROOT, 'images/images.yaml')
BACKLOG_KEY = 'Unfiled_Backlog'

# Directories that hold real images. video_posters/ is deliberately NOT swept: a
# poster is a frame derived from a video, it belongs to the videos side, and a
# poster only earns an entry here if a page actually embeds it (grow_hierarchy's
# page sweep handles that case).
SCAN_DIRS = ['images', 'site/internals/static/img/evidence']
IMG_EXT = ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif')

# ---------- exclusion gates ----------
# 1. Anything git ignores. images/.gitignore is a hand-curated privacy list; those
#    files are deliberately not in the repo and must not be catalogued either.
# 2. The publish-time ban set (ban_images.csv + exclude_images.txt).
def git_ignored(paths):
    import subprocess
    if not paths: return set()
    p = subprocess.run(['git', '-C', ROOT, 'check-ignore', '--stdin'],
                       input='\n'.join(paths), capture_output=True, text=True)
    return {l.strip() for l in p.stdout.splitlines() if l.strip()}

BANNED = set()
exc = os.path.join(ROOT, 'image_planning/exclude_images.txt')
if os.path.exists(exc):
    for line in open(exc, encoding='utf-8'):
        line = line.split('#', 1)[0].strip()
        if re.fullmatch(r'[0-9a-f]{64}', line): BANNED.add(line)
ban_csv = os.path.join(ROOT, 'images/ban_images.csv')
if os.path.exists(ban_csv):
    import csv
    with open(ban_csv, encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if (row.get('banned') or '').strip().lower() == 'true':
                s = (row.get('sha256') or '').strip()
                if re.fullmatch(r'[0-9a-f]{64}', s): BANNED.add(s)

# ---------- load ----------
doc = yaml.safe_load(open(YAML_PATH, encoding='utf-8'))

def child_list(node):
    for lv in (4, 5, 6, 7):
        if node.get(f'level_{lv}'): yield lv, node[f'level_{lv}']

known = set()
def index(items, lvl):
    for it in items:
        n = it[f'level_{lvl}']
        for kind in ('images', 'videos'):
            for m in (n.get(kind) or []):
                inner = m.get('image') or m.get('video')
                if inner.get('sha256'): known.add(inner['sha256'])
        for nl, arr in child_list(n): index(arr, nl)
index(doc['level_3'], 3)

backlog = None
for it in doc['level_3']:
    if it['level_3']['_key'] == BACKLOG_KEY: backlog = it['level_3']; break
if backlog is None:
    raise SystemExit(f"add_orphan_images: level_3 node '{BACKLOG_KEY}' not found.")

# ---------- scan ----------
candidates = []
for d in SCAN_DIRS:
    for root_, _, files in os.walk(os.path.join(ROOT, d)):
        for f in files:
            if os.path.splitext(f)[1].lower() in IMG_EXT:
                candidates.append(os.path.join(root_, f))
candidates.sort()
ignored = git_ignored([os.path.relpath(p, ROOT) for p in candidates])

def sha256_of(p):
    h = hashlib.sha256()
    with open(p, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''): h.update(chunk)
    return h.hexdigest()

stats = {'scanned': 0, 'already': 0, 'git_ignored': 0, 'banned': 0, 'added': 0}
seen_new = {}
for p in candidates:
    stats['scanned'] += 1
    if os.path.relpath(p, ROOT) in ignored: stats['git_ignored'] += 1; continue
    s = sha256_of(p)
    if s in known: stats['already'] += 1; continue
    if s in BANNED: stats['banned'] += 1; continue
    if s in seen_new: continue          # same bytes in two dirs — one entry only
    seen_new[s] = p
    backlog.setdefault('images', [])
    if backlog['images'] is None: backlog['images'] = []
    backlog['images'].append({'image': {
        'cid': '', 'ipfs_pinned': False, 'sha256': s,
        'file_path': p.replace(HOME, '~'),
        'ai_description': '', 'ai_description_file': '', 'ocr_file': '',
        'transcription_file': '', 'image_page': '',
        'on_pages': [], 'should_be_on_pages': [],
    }})
    known.add(s); stats['added'] += 1

# ---------- recount ----------
split = [0]
def recount(items, lvl):
    total = 0
    for it in items:
        n = it[f'level_{lvl}']
        direct = len(n.get('images') or []) + len(n.get('videos') or [])
        sub = sum(recount(arr, nl) for nl, arr in child_list(n))
        n['number_of_images'] = direct
        n['number_of_images_recursive'] = direct + sub
        if direct > 12: n['needs_split'] = True; split[0] += 1
        elif 'needs_split' in n: del n['needs_split']
        total += direct + sub
    return total
grand = recount(doc['level_3'], 3)

# ---------- emit (keep identical to bind_image_pages.py) ----------
PROSE_FIELDS = {'title', 'ai_description'}
def q(s): return q_identity(s)
MEDIA_ORDER = ['cid', 'ipfs_pinned', 'sha256', 'file_path', 'ai_description',
               'ai_description_file', 'ocr_file', 'transcription_file',
               'image_page', 'next_image', 'on_pages', 'should_be_on_pages',
               'ipfs_url', 'also_filed_in']
out = []
out.append('# images.yaml — master image list / image evidence hierarchy for the Charlie Kirk site.')
out.append('# Moved 2026-07-22 from image_planning/hierarchy_images.yaml (old name + location dead).')
out.append('# GENERATED first pass from ~/_Mirror/Politics/Charlie_Kirk_Mi; GROWN by')
out.append('# p_create_image_hierarchy.md: site Level 2/3/4 pages mirrored in as level_3/4/5')
out.append('# (level incremented by one), page-embedded images bound in, sidecar file paths')
out.append('# (.ai_description / .ocr / .transcription) resolved via Large File Bridge mapping,')
out.append('# and site IPFS embeds (ipfs.io/ipfs/<CID>) bound to entries by sha256 via local IPFS.')
out.append('# image_page = full path from ~ to the published Level 5 page that hosts that one')
out.append('# image under site/docs/Photos; "" means no page exists for it yet.')
out.append('# cid empty = IPFS not assigned yet. sha256 is the identity; ipfs_url entries have no local file.')
out.append('# Nodes marked needs_split exceed the 12-image ceiling and get split on a later pass.')
out.append('# site_level_2 = site docs dirs this cluster covers; site_page = the page a node mirrors.')

def emit_media(im, pad):
    kind = 'image' if 'image' in im else 'video'
    inner = im[kind]
    out.append(f'{pad}- {kind}:')
    p2 = pad + '    '
    for k in MEDIA_ORDER + [k for k in inner if k not in MEDIA_ORDER]:
        if k not in inner: continue
        v = inner[k]
        if k == 'ipfs_pinned':
            out.append(f'{p2}ipfs_pinned: {"true" if v else "false"}')
        elif k in ('on_pages', 'should_be_on_pages'):
            if v:
                out.append(f'{p2}{k}:')
                for pg in v:
                    out.append(f'{p2}  - page: {q(pg["page"] if isinstance(pg, dict) else pg)}')
            else:
                out.append(f'{p2}{k}: []')
        elif k == 'sha256': out.append(f'{p2}{k}: {v if v else chr(34)+chr(34)}')
        elif isinstance(v, list):
            if v: out.append(f'{p2}{k}: [{", ".join(q(x) for x in v)}]')
        elif k in PROSE_FIELDS: out.append(f'{p2}{k}: {q_prose(v)}')
        else: out.append(f'{p2}{k}: {q(v)}')

def emit_node(it, lvl, indent):
    n = it[f'level_{lvl}']
    pad = ' ' * indent
    out.append(f'{pad}- level_{lvl}:')
    p2 = pad + '    '
    out.append(f'{p2}title: {q_prose(n["title"])}')
    out.append(f'{p2}_key: {n["_key"]}')
    if 'site_level_2' in n:
        out.append(f'{p2}site_level_2: [{", ".join(q(x) for x in n["site_level_2"])}]')
    if n.get('site_page'): out.append(f'{p2}site_page: {q(n["site_page"])}')
    out.append(f'{p2}number_of_images: {n["number_of_images"]}')
    out.append(f'{p2}number_of_images_recursive: {n["number_of_images_recursive"]}')
    if n.get('needs_split'):
        out.append(f'{p2}needs_split: true   # over the 12 ceiling — split on a later pass')
    for kind in ('images', 'videos'):
        arr = n.get(kind) or []
        if not arr:
            if kind == 'images': out.append(f'{p2}images: []')
            continue
        out.append(f'{p2}{kind}:')
        for im in arr: emit_media(im, p2 + '  ')
    for nl, arr in child_list(n):
        if arr:
            out.append(f'{p2}level_{nl}:')
            for c in arr: emit_node(c, nl, indent + 6)

out.append('level_3:')
for it in doc['level_3']: emit_node(it, 3, 2)
open(YAML_PATH, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
yaml.safe_load(open(YAML_PATH, encoding='utf-8'))

print('=' * 28)
print('ADD ORPHAN IMAGES COMPLETE')
print(f'Files scanned: {stats["scanned"]}')
print(f'  already in hierarchy : {stats["already"]}')
print(f'  skipped, git-ignored : {stats["git_ignored"]}  (privacy list)')
print(f'  skipped, banned      : {stats["banned"]}')
print(f'  ADDED to {BACKLOG_KEY} : {stats["added"]}')
print(f'Grand total media entries: {grand}   needs_split nodes: {split[0]}')
print('YAML re-parses: yes')
print('=' * 28)
