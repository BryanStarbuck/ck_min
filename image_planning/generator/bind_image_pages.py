#!/usr/bin/env python3
# bind_image_pages.py — Stage 8 of p_create_image_hierarchy.md.
# Binds every image/video entry in images/images.yaml to its published Level 5
# "image page" under site/docs/Photos, via the ck_image_sha256 + ck_node_key
# frontmatter the page generator stamps on each page. Sets the image_page
# property to the full path from ~ to that page ("" when no page exists yet).
# Also normalizes every media entry so it always carries the full property set.
# Reads site pages; never creates, renames, or edits them.
import os, re, sys, yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sanitize_common import q_prose, q_identity, validate_no_invisible

ROOT = os.path.expanduser('~/BGit/Bryan_git/charlie-kirk')
YAML_PATH = os.path.join(ROOT, 'images/images.yaml')
PHOTOS_DIR = os.path.join(ROOT, 'site/docs/Photos')
TILDE_PHOTOS = '~/BGit/Bryan_git/charlie-kirk/site/docs/Photos'

# ---------- index the published image pages ----------
# ---------- publish-time exclusion gate ----------
# An excluded sha256 has no published page BY DESIGN (gen_photos_pages.py skips
# it and deletes any page that existed). Its image_page must therefore be "",
# and the "never clear a recorded page silently" rule below must NOT resurrect
# a path to a page the gate just removed. Load the same gate the generator uses.
EXCLUDE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            '..', 'exclude_images.txt')
EXCLUDED = set()
if os.path.exists(EXCLUDE_FILE):
    for line in open(EXCLUDE_FILE, encoding='utf-8'):
        line = line.split('#', 1)[0].strip()
        if re.fullmatch(r'[0-9a-f]{64}', line):
            EXCLUDED.add(line)

# ---------- media-type gate: /Photos is still images only ----------
# Kept deliberately in step with gen_photos_pages.py's load_video_cids(). Both
# parse the video pipeline's records BY FILENAME rather than scraping CIDs
# wholesale: those records describe a mixed corpus and a blanket scrape types
# 70 image entries as video when only 9 are. videos/videos.yaml is not consulted
# — it is still a schema shell whose cids describe the inherited image corpus.
VIDEO_EXT = ('.mp4', '.mov', '.webm', '.m4v', '.mkv', '.avi')
DOCS_DIR = os.path.join(ROOT, 'site/docs')


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
    for dp, _d, fs in os.walk(DOCS_DIR):
        if dp.startswith(PHOTOS_DIR) or dp.startswith(os.path.join(DOCS_DIR, 'Videos')):
            continue
        for fn in fs:
            if not fn.endswith(('.mdx', '.md')):
                continue
            try:
                txt = open(os.path.join(dp, fn), encoding='utf-8').read()
            except OSError:
                continue
            for tag in re.findall(r'<(?:video|source)\b.*?>', txt, re.S | re.I):
                c = _cid(tag)
                if c:
                    cids.add(c)
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


pages_total = pages_with_sha = 0
pages_without = []
by_pair = {}      # (sha256, node_key) -> tilde path
by_sha = {}       # sha256 -> [(node_key, tilde path)]
page_node_parent = {}   # node_key of a page -> its directory (for nearest-match fallback)

for dirpath, dirnames, filenames in os.walk(PHOTOS_DIR):
    for fn in filenames:
        if not fn.endswith('.mdx') or fn == 'overview.mdx':
            continue
        full = os.path.join(dirpath, fn)
        head = open(full, encoding='utf-8', errors='replace').read(4000)
        if not head.startswith('---'):
            continue
        fm = head.split('---', 2)[1] if head.count('---') >= 2 else ''
        m = re.search(r'^ck_image_sha256:\s*([0-9a-fA-F]{64})\s*$', fm, re.M)
        pages_total += 1
        if not m:
            pages_without.append(os.path.relpath(full, ROOT))
            continue
        sha = m.group(1).lower()
        nk = re.search(r'^ck_node_key:\s*(\S+)\s*$', fm, re.M)
        nk = nk.group(1).strip('"\'') if nk else ''
        rel = os.path.relpath(full, PHOTOS_DIR)
        tilde = f'{TILDE_PHOTOS}/{rel}'
        pages_with_sha += 1
        by_pair.setdefault((sha, nk), tilde)
        by_sha.setdefault(sha, []).append((nk, tilde))
        page_node_parent[nk] = os.path.dirname(rel)

# ---------- load the YAML ----------
doc = yaml.safe_load(open(YAML_PATH, encoding='utf-8'))

def child_list(node):
    for k, v in node.items():
        if k.startswith('level_') and isinstance(v, list):
            yield int(k.split('_')[1]), v

MEDIA_ORDER = ['cid', 'ipfs_pinned', 'sha256', 'file_path', 'ai_description',
               'ai_description_file', 'ocr_file', 'transcription_file',
               'image_page', 'next_image', 'on_pages', 'should_be_on_pages',
               'ipfs_url', 'also_filed_in']
REQUIRED_SCALARS = ['cid', 'sha256', 'file_path', 'ai_description',
                    'ai_description_file', 'ocr_file', 'transcription_file', 'image_page']

st = {'entries': 0, 'by_pair': 0, 'by_sha': 0, 'empty': 0, 'vanished': [],
      'kept_existing': 0, 'filled_missing_keys': 0}

def node_chain_keys(chain):
    """ancestor _keys, nearest first"""
    return list(reversed(chain))

def bind(items, lvl, chain):
    for it in items:
        node = it[f'level_{lvl}']
        key = node['_key']
        for kind in ('images', 'videos'):
            for im in (node.get(kind) or []):
                inner = im.get('image') or im.get('video')
                st['entries'] += 1
                sha = (inner.get('sha256') or '').lower()
                prev = inner.get('image_page') or ''

                # Video entries have no image page by design. /Photos is the
                # still-image Level 2; a video's page belongs under
                # site/docs/Videos and is recorded in videos/videos.yaml's own
                # video_page property, never in image_page here. Force "" and
                # skip the keep-prior-value rule, exactly as for exclusions —
                # otherwise a stale binding to a /Photos video page survives
                # every run. Covers both `videos:` array items and `image:`
                # items whose CID is really an .mp4.
                if kind == 'videos' or entry_is_video(inner):
                    inner['image_page'] = ''
                    st['video'] = st.get('video', 0) + 1
                    st['empty'] += 1
                    for k in REQUIRED_SCALARS:
                        if k not in inner or inner[k] is None:
                            inner[k] = ''; st['filled_missing_keys'] += 1
                    continue

                # Excluded images have no page by design: force "" and skip the
                # keep-prior-value rule, which would otherwise cling to the page
                # the exclusion gate just deleted.
                if sha in EXCLUDED:
                    inner['image_page'] = ''
                    st['excluded'] = st.get('excluded', 0) + 1
                    st['empty'] += 1
                    for k in REQUIRED_SCALARS:
                        if k not in inner or inner[k] is None:
                            inner[k] = ''; st['filled_missing_keys'] += 1
                    continue

                val = ''
                if sha:
                    if (sha, key) in by_pair:
                        val = by_pair[(sha, key)]; st['by_pair'] += 1
                    else:
                        cands = by_sha.get(sha) or []
                        if len(cands) == 1:
                            val = cands[0][1]; st['by_sha'] += 1
                        elif cands:
                            # nearest in the tree: prefer a page whose node key is an
                            # ancestor of this node, nearest ancestor first
                            anc = node_chain_keys(chain)
                            pick = None
                            for a in anc:
                                for nk, tp in cands:
                                    if nk == a:
                                        pick = tp; break
                                if pick: break
                            if pick:
                                val = pick; st['by_sha'] += 1

                # never clear a previously recorded page in favour of ""
                if not val and prev:
                    if os.path.isfile(os.path.expanduser(prev)):
                        val = prev; st['kept_existing'] += 1
                    else:
                        st['vanished'].append(prev)
                        val = prev
                if not val:
                    st['empty'] += 1

                inner['image_page'] = val
                for k in REQUIRED_SCALARS:
                    if k not in inner or inner[k] is None:
                        inner[k] = ''
                        st['filled_missing_keys'] += 1
        for nl, arr in child_list(node):
            bind(arr, nl, chain + [key])

bind(doc['level_3'], 3, [])

# ---------- Stage 9: counts, needs_split, integrity ----------
s9 = {'needs_split': 0}
def recount(items, lvl):
    total = 0
    for it in items:
        node = it[f'level_{lvl}']
        direct = len(node.get('images') or []) + len(node.get('videos') or [])
        sub = sum(recount(arr, nl) for nl, arr in child_list(node))
        node['number_of_images'] = direct
        node['number_of_images_recursive'] = direct + sub
        if direct > 12:
            node['needs_split'] = True; s9['needs_split'] += 1
        elif 'needs_split' in node:
            del node['needs_split']
        total += direct + sub
    return total
grand = recount(doc['level_3'], 3)

key_seen, key_dups, sha_dup = set(), [], []
counts = {}
def check(items, lvl):
    for it in items:
        node = it[f'level_{lvl}']
        counts[lvl] = counts.get(lvl, 0) + 1
        k = node['_key']
        if k in key_seen: key_dups.append(k)
        key_seen.add(k)
        for kind in ('images', 'videos'):
            local = set()
            for im in (node.get(kind) or []):
                inner = im.get('image') or im.get('video')
                ident = inner.get('sha256') or inner.get('ipfs_url') or ''
                if ident and ident in local: sha_dup.append((k, ident[:12]))
                if ident: local.add(ident)
        for nl, arr in child_list(node):
            check(arr, nl)
check(doc['level_3'], 3)

# ---------- emit (same conventions as grow_hierarchy.py) ----------
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

def emit_media(im, pad):
    kind = 'image' if 'image' in im else 'video'
    inner = im[kind]
    out.append(f'{pad}- {kind}:')
    p2 = pad + '    '
    keys = MEDIA_ORDER + [k for k in inner if k not in MEDIA_ORDER]
    for k in keys:
        if k not in inner: continue
        v = inner[k]
        if k == 'ipfs_pinned':
            out.append(f'{p2}ipfs_pinned: {"true" if v else "false"}')
        elif k in ('on_pages', 'should_be_on_pages'):
            # Both are a LIST OF {page: ...} MAPPINGS — emit as block mappings,
            # never stringify the dicts (that was the old bug). Both are stored
            # with an explicit [] when empty, so [] must round-trip.
            if v:
                out.append(f'{p2}{k}:')
                for pg in v:
                    path = pg['page'] if isinstance(pg, dict) else pg
                    out.append(f'{p2}  - page: {q(path)}')
            else:
                out.append(f'{p2}{k}: []')
        elif k == 'sha256': out.append(f'{p2}{k}: {v if v else chr(34)+chr(34)}')
        elif isinstance(v, list):
            if v: out.append(f'{p2}{k}: [{", ".join(q(x) for x in v)}]')
        elif k in PROSE_FIELDS: out.append(f'{p2}{k}: {q_prose(v)}')
        else: out.append(f'{p2}{k}: {q(v)}')

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
            if kind == 'images': out.append(f'{p2}images: []')
            continue
        out.append(f'{p2}{kind}:')
        for im in arr: emit_media(im, p2 + '  ')
    for nl, arr in child_list(node):
        if arr:
            out.append(f'{p2}level_{nl}:')
            for c in arr: emit_node(c, nl, indent + 6)

out.append('level_3:')
for it in doc['level_3']:
    emit_node(it, 3, 2)
open(YAML_PATH, 'w', encoding='utf-8').write('\n'.join(out) + '\n')

# ---------- validate ----------
re_doc = yaml.safe_load(open(YAML_PATH, encoding='utf-8'))
validate_no_invisible(YAML_PATH)

bad_pages, bound, total_media, missing_keys = [], 0, 0, 0
def verify(items, lvl):
    global bound, total_media, missing_keys
    for it in items:
        node = it[f'level_{lvl}']
        for kind in ('images', 'videos'):
            for im in (node.get(kind) or []):
                inner = im.get('image') or im.get('video')
                total_media += 1
                for k in REQUIRED_SCALARS:
                    if k not in inner: missing_keys += 1
                ip = inner.get('image_page') or ''
                if ip:
                    bound += 1
                    p = os.path.expanduser(ip)
                    if not os.path.isfile(p) or not p.startswith(PHOTOS_DIR):
                        bad_pages.append(ip)
                    # A video must never end up bound to a /Photos page.
                    if kind == 'videos' or entry_is_video(inner):
                        bad_pages.append('VIDEO BOUND TO /Photos: ' + ip)
        for nl, arr in child_list(node):
            verify(arr, nl)
verify(re_doc['level_3'], 3)

print('=' * 28)
print('STAGE 8 COMPLETE')
print(f'Image pages indexed under Photos: {pages_total} '
      f'({pages_with_sha} with ck_image_sha256, {len(pages_without)} without)')
print(f'Entries with image_page set: {bound}   matched by (sha256,node): {st["by_pair"]}   '
      f'by sha256 only: {st["by_sha"]}   kept prior value: {st["kept_existing"]}')
print(f'Entries with image_page "": {st["empty"]} '
      f'(of which {st.get("excluded", 0)} are publish-excluded, '
      f'{st.get("video", 0)} are video and belong to site/docs/Videos, '
      f'rest have no page yet)')
print(f'Known video CIDs: {len(VIDEO_CIDS)}')
print(f'Recorded pages now missing from disk: {len(st["vanished"])}')
for v in st['vanished'][:10]: print('   MISSING:', v)
print('=' * 28)
print('STAGE 9 COMPLETE')
print(f'Counts recomputed: yes (grand total media {grand})')
print(f'needs_split nodes: {s9["needs_split"]}')
print(f'Duplicate _keys: {len(key_dups)}   Duplicate sha256 within a node: {len(sha_dup)}')
print('YAML parses: yes')
print('=' * 28)
print('STAGE 10 — image_page verification')
print(f'Nodes: ' + '  '.join(f'level_{k}: {v}' for k, v in sorted(counts.items())))
print(f'Total media entries: {total_media}')
print(f'Entries missing a required property key: {missing_keys}')
print(f'image_page values that do not resolve under site/docs/Photos: {len(bad_pages)}')
for b in bad_pages[:10]: print('   BAD:', b)
print(f'image_page coverage: {100.0*bound/max(total_media,1):.1f}% ({bound} of {total_media})')
print(f'Pages with no ck_image_sha256 (resolve on a later generator pass): {len(pages_without)}')
for p in pages_without[:5]: print('   NO-SHA:', p)
print('=' * 28)
