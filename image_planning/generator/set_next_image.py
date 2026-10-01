#!/usr/bin/env python3
# set_next_image.py — carries out image_planning/p_next_buttons.md, Stages 1-2.
#
# Writes the next_image property onto every publishable image in
# images/images.yaml. next_image is the image_page (full ~-rooted path) of the
# image that comes NEXT in one global depth-first, pre-order walk of the whole
# hierarchy — a node's OWN images before its child clusters, children in YAML
# order. The chain LOOPS: the last image's next_image is the first image's page.
#
# Membership of the walk S: an image is in S iff its image_page is set AND
# resolves to a real .mdx on disk under site/docs/Photos, AND it is not banned
# (ban_images.csv / exclude_images.txt) and not a video. Everything else gets no
# next_image (the key is left absent). Banned/video entries already carry
# image_page "" from bind_image_pages.py; the CSV ban (which bind does not zero)
# is re-checked here.
#
# Serialization reuses bind_image_pages.py's emit conventions VERBATIM, extended
# only to (a) place next_image right after image_page and (b) emit
# should_be_on_pages as a block-mapping list (same shape as on_pages) rather
# than stringifying the dicts. Nothing else in the file moves: a dry-run diff
# must show only next_image lines changing.
import os, re, sys, csv, argparse, yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sanitize_common import q_prose, q_identity, validate_no_invisible

ROOT = os.path.expanduser('~/BGit/Bryan_git/charlie-kirk')
YAML_PATH = os.path.join(ROOT, 'images/images.yaml')
PHOTOS_DIR = os.path.join(ROOT, 'site/docs/Photos')
DOCS_DIR = os.path.join(ROOT, 'site/docs')
EXCLUDE_FILE = os.path.join(ROOT, 'image_planning/exclude_images.txt')
BAN_CSV = os.path.join(ROOT, 'images/ban_images.csv')

# ---------- ban set: exclude_images.txt + ban_images.csv ----------
BANNED_SHA, BANNED_CID, BANNED_PATH = set(), set(), set()
if os.path.exists(EXCLUDE_FILE):
    for line in open(EXCLUDE_FILE, encoding='utf-8'):
        line = line.split('#', 1)[0].strip()
        if re.fullmatch(r'[0-9a-f]{64}', line):
            BANNED_SHA.add(line)
if os.path.exists(BAN_CSV):
    with open(BAN_CSV, encoding='utf-8', newline='') as f:
        for row in csv.DictReader(f):
            if (row.get('banned') or '').strip().lower() == 'false':
                continue  # explicit un-ban
            sha = (row.get('sha256') or '').strip().lower()
            cid = (row.get('cid') or '').strip()
            fp = (row.get('file_path') or '').strip()
            if re.fullmatch(r'[0-9a-f]{64}', sha):
                BANNED_SHA.add(sha)
            if cid:
                BANNED_CID.add(cid)
            if fp:
                BANNED_PATH.add(os.path.realpath(os.path.expanduser(fp)))

# ---------- media-type gate (kept in step with bind_image_pages.py) ----------
VIDEO_EXT = ('.mp4', '.mov', '.webm', '.m4v', '.mkv', '.avi')


def _cid(s):
    m = re.search(r'/ipfs/(\w+)', s or '') or re.search(r'^(Qm\w{44})$', (s or '').strip())
    return m.group(1) if m else ''


def _load_video_cids():
    cids = set()
    try:
        for rec in yaml.safe_load(open(os.path.join(ROOT, 'videos/manifest.yaml'),
                                       encoding='utf-8')) or []:
            if (rec.get('filename') or '').lower().endswith(VIDEO_EXT) and rec.get('ipfs_cid'):
                cids.add(rec['ipfs_cid'])
    except (OSError, yaml.YAMLError):
        pass
    try:
        txt = open(os.path.join(ROOT, 'IPFS/ipfs.txt'), encoding='utf-8').read()
        for block in re.split(r'\n\s*\n', txt):
            m = re.search(r'ipfs\s+add\s+"([^"]+)"', block)
            if m and m.group(1).lower().endswith(VIDEO_EXT):
                cids.update(re.findall(r'\b(Qm[1-9A-HJ-NP-Za-km-z]{44})\b', block))
    except OSError:
        pass
    return cids


VIDEO_CIDS = _load_video_cids()


def entry_is_video(inner):
    for field in ('file_path', 'ipfs_url', 'cid'):
        v = (inner.get(field) or '').strip()
        if v.lower().endswith(VIDEO_EXT):
            return True
        c = _cid(v)
        if c and c in VIDEO_CIDS:
            return True
    return False


def is_banned(inner):
    sha = (inner.get('sha256') or '').strip().lower()
    cid = (inner.get('cid') or '').strip()
    fp = (inner.get('file_path') or '').strip()
    if sha and sha in BANNED_SHA:
        return True
    if cid and cid in BANNED_CID:
        return True
    if fp and os.path.realpath(os.path.expanduser(fp)) in BANNED_PATH:
        return True
    return False


def is_publishable(inner):
    ip = (inner.get('image_page') or '').strip()
    if not ip:
        return False
    p = os.path.expanduser(ip)
    if not os.path.isfile(p) or not os.path.realpath(p).startswith(os.path.realpath(PHOTOS_DIR)):
        return False
    if is_banned(inner):
        return False
    if entry_is_video(inner):
        return False
    return True


# ---------- load YAML ----------
doc = yaml.safe_load(open(YAML_PATH, encoding='utf-8'))


def child_list(node):
    for k, v in node.items():
        if k.startswith('level_') and isinstance(v, list):
            yield int(k.split('_')[1]), v


# ---------- build the global sequence S (document pre-order) ----------
S = []          # inner image dicts, in walk order
all_imgs = []   # every inner image dict (to strip stale next_image off non-S)


def walk(items, lvl):
    for it in items:
        node = it[f'level_{lvl}']
        for im in (node.get('images') or []):
            inner = im.get('image')
            if inner is None:
                continue
            all_imgs.append(inner)
            if is_publishable(inner):
                S.append(inner)
        # videos are not part of the still-image walk
        for vm in (node.get('videos') or []):
            inner = vm.get('video')
            if inner is not None:
                all_imgs.append(inner)
        for nl, arr in child_list(node):
            walk(arr, nl)


walk(doc['level_3'], 3)

# ---------- assign next_image (successor in S, last wraps to first) ----------
N = len(S)
in_S = {id(x) for x in S}
added = changed = unchanged = cleared = 0
for idx, inner in enumerate(S):
    nxt = S[(idx + 1) % N]['image_page']
    prev = inner.get('next_image')
    if 'next_image' not in inner:
        added += 1
    elif prev != nxt:
        changed += 1
    else:
        unchanged += 1
    inner['next_image'] = nxt
# strip any stale next_image off entries no longer in S
for inner in all_imgs:
    if id(inner) not in in_S and 'next_image' in inner:
        del inner['next_image']
        cleared += 1

# ---------- emit (bind_image_pages.py conventions, verbatim + 2 additions) ----
MEDIA_ORDER = ['cid', 'ipfs_pinned', 'sha256', 'file_path', 'ai_description',
               'ai_description_file', 'ocr_file', 'transcription_file',
               'image_page', 'next_image', 'on_pages', 'should_be_on_pages',
               'ipfs_url', 'also_filed_in']
PROSE_FIELDS = {'title', 'ai_description'}
q = q_identity
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


def _emit_page_list(p2, key, v):
    # on_pages and should_be_on_pages are both lists of {page: ...} mappings.
    # Emit populated ones as block mappings; emit [] when empty (both are stored
    # with an explicit [] today, so [] must round-trip).
    if v:
        out.append(f'{p2}{key}:')
        for pg in v:
            path = pg['page'] if isinstance(pg, dict) else pg
            out.append(f'{p2}  - page: {q(path)}')
    else:
        out.append(f'{p2}{key}: []')


def emit_media(im, pad):
    kind = 'image' if 'image' in im else 'video'
    inner = im[kind]
    out.append(f'{pad}- {kind}:')
    p2 = pad + '    '
    keys = MEDIA_ORDER + [k for k in inner if k not in MEDIA_ORDER]
    for k in keys:
        if k not in inner:
            continue
        v = inner[k]
        if k == 'ipfs_pinned':
            out.append(f'{p2}ipfs_pinned: {"true" if v else "false"}')
        elif k in ('on_pages', 'should_be_on_pages'):
            _emit_page_list(p2, k, v)
        elif k == 'sha256':
            out.append(f'{p2}{k}: {v if v else chr(34) + chr(34)}')
        elif isinstance(v, list):
            if v:
                out.append(f'{p2}{k}: [{", ".join(q(x) for x in v)}]')
        elif k in PROSE_FIELDS:
            out.append(f'{p2}{k}: {q_prose(v)}')
        else:
            out.append(f'{p2}{k}: {q(v)}')


def emit_node(it, lvl, indent):
    node = it[f'level_{lvl}']
    pad = ' ' * indent
    out.append(f'{pad}- level_{lvl}:')
    p2 = pad + '    '
    out.append(f'{p2}title: {q_prose(node["title"])}')
    out.append(f'{p2}_key: {node["_key"]}')
    if 'site_level_2' in node:
        out.append(f'{p2}site_level_2: [{", ".join(q(x) for x in node["site_level_2"])}]')
    if node.get('site_page'):
        out.append(f'{p2}site_page: {q(node["site_page"])}')
    out.append(f'{p2}number_of_images: {node["number_of_images"]}')
    out.append(f'{p2}number_of_images_recursive: {node["number_of_images_recursive"]}')
    if node.get('needs_split'):
        out.append(f'{p2}needs_split: true   # over the 12 ceiling — split on a later pass')
    for kind in ('images', 'videos'):
        arr = node.get(kind) or []
        if not arr:
            if kind == 'images':
                out.append(f'{p2}images: []')
            continue
        out.append(f'{p2}{kind}:')
        for im in arr:
            emit_media(im, p2 + '  ')
    for nl, arr in child_list(node):
        if arr:
            out.append(f'{p2}level_{nl}:')
            for c in arr:
                emit_node(c, nl, indent + 6)


out.append('level_3:')
for it in doc['level_3']:
    emit_node(it, 3, 2)

ap = argparse.ArgumentParser()
ap.add_argument('--out', default=YAML_PATH)
args = ap.parse_args()
open(args.out, 'w', encoding='utf-8').write('\n'.join(out) + '\n')

# ---------- validate ----------
re_doc = yaml.safe_load(open(args.out, encoding='utf-8'))
validate_no_invisible(args.out)

# integrity: single cycle of length N over the on-disk image pages
first = S[0]['image_page'] if S else ''
seen, cur, steps = set(), first, 0
by_page = {x['image_page']: x for x in S}
cycle_ok = bool(S)
while cur and cur not in seen:
    seen.add(cur)
    steps += 1
    nx = by_page.get(cur)
    cur = nx['next_image'] if nx else ''
cycle_ok = (steps == N and cur == first)

print('=' * 28)
print('set_next_image.py COMPLETE')
print(f'Images in YAML (image entries): {len([1 for _ in all_imgs])}')
print(f'Publishable images in walk S: {N}')
print(f'next_image: {added} added, {changed} changed, {unchanged} unchanged, {cleared} cleared off non-S')
print(f'Single cycle over all {N} pages, wraps last->first: {cycle_ok} (steps={steps})')
if S:
    print(f'Wrap: last image_page {S[-1]["image_page"].split("/")[-1]} -> '
          f'first {S[0]["image_page"].split("/")[-1]}')
print(f'Wrote: {args.out}')
print('=' * 28)
