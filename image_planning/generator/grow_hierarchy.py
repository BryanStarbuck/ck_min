#!/usr/bin/env python3
# grow_hierarchy.py — Stages 3-8 of p_create_image_hierarchy.md.
# Grows images/images.yaml (formerly image_planning/hierarchy_images.yaml): site
# Level 2s -> level_3 superset, site pages ->
# level_4/level_5 nodes (level incremented by one), page images -> image entries,
# sidecar file-path properties, counts + needs_split. Grow-only: never deletes.
import os, re, csv, sys, hashlib, yaml, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sanitize_common import sanitize_prose, q_prose, q_identity, validate_no_invisible

HOME = os.path.expanduser('~')
ROOT = os.path.join(HOME, 'BGit/Bryan_git/charlie-kirk')
THIS = os.path.join(ROOT, 'image_planning')
YAML_PATH = os.path.join(ROOT, 'images/images.yaml')
DOCS = os.path.join(ROOT, 'site/docs')
STATIC_DIRS = [os.path.join(ROOT, 'site/static'), os.path.join(ROOT, 'site/internals/static')]
MIRROR = os.path.join(HOME, '_Mirror/Politics/Charlie_Kirk_Mi')
MIRROR_TILDE = '~/_Mirror/Politics/Charlie_Kirk_Mi'
SIDE = os.path.join(HOME, 'BGit/Bryan_git/personal_large_files_bridge/_Mirror/Politics/Charlie_Kirk_Mi')
SIDE_TILDE = '~/BGit/Bryan_git/personal_large_files_bridge/_Mirror/Politics/Charlie_Kirk_Mi'
SIDE_LEGACY = os.path.join(HOME, 'BGit/Bryan_git/personal_large_files_bridge/.lfbridge/_Mirror/Politics/Charlie_Kirk_Mi')
SIDE_LEGACY_TILDE = '~/BGit/Bryan_git/personal_large_files_bridge/.lfbridge/_Mirror/Politics/Charlie_Kirk_Mi'
REPO_SIDE = os.path.join(ROOT, '.lfbridge')
REPO_SIDE_TILDE = '~/BGit/Bryan_git/charlie-kirk/.lfbridge'
ROOT_TILDE = '~/BGit/Bryan_git/charlie-kirk'
INVENTORY = os.path.join(THIS, 'generator/inventory.tsv')
PAGES_CSV = os.path.join(ROOT, 'pages.csv')

IMG_EXT = ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.heic', '.avif', '.svg')
VID_EXT = ('.mp4', '.mov', '.webm', '.m4v')

# ---------- Stage 3 mapping: site Level 2 dir -> level_3 _key ----------
# Order matters: the FIRST dir listed for a key is the PRIMARY dir (its overview
# becomes the node's site_page and its pages become level_4 children directly).
# Additional dirs for the same key become a level_4 node under it.
SITE_MAP = [
    ('FBI', 'FBI'), ('TPUSA', 'TPUSA'), ('Tyler_Robinson', 'Tyler_Robinson'),
    ('Mic', 'Mic'), ('Israel', 'Israel'), ('Israel_Main_Suspect', 'Israel'),
    ('maps', 'Maps'), ('Security_Team', 'Security_Team'),
    ('Charlie', 'Charlie_Kirk'), ('People', 'People'), ('key_individuals', 'People'),
    ('court', 'Court_Legal'), ('Legal', 'Court_Legal'), ('legal_investigation', 'Court_Legal'),
    ('Planes', 'Aircraft'),
    ('Gun_Bullet', 'Ballistics_Gun'),
    ('UVU', 'UVU_Venue'), ('campus_university', 'UVU_Venue'),
    ('intelligence', 'CIA_Intelligence'), ('US_Intelligence', 'CIA_Intelligence'),
    ('US_Intelligence_Assisted', 'CIA_Intelligence'), ('Proof_Intel_Services', 'CIA_Intelligence'),
    ('GoogleSearches', 'Google_Search'),
    ('Tent', 'Truck_Tent'),
    ('Killer', 'Shot_Position'),
    ('distraction_people', 'Patsy'),
    # New level_3 nodes
    ('After', 'After_Shooting'), ('Before', 'Before_Shooting'),
    ('analysis_documentation', 'Analysis_Documentation'), ('Topic-Analyses', 'Analysis_Documentation'),
    ('cameras', 'Security_Cameras'), ('Cause_of_Death', 'Cause_of_Death'),
    ('Censorship', 'Censorship_Evidence'),
    ('Companies_Organizations', 'Companies_Orgs'), ('organizations_groups', 'Companies_Orgs'),
    ('CoverUp', 'Cover_Up_Evidence'), ('Defamation', 'Defamation_Cases'),
    ('Drones', 'Drones_Evidence'), ('Electrocution', 'Electrocution'),
    ('Fix', 'Fix_Laws'), ('laws', 'Fix_Laws'),
    ('gov', 'Government'), ('government_organizations', 'Government'),
    ('Gov_Mind_Control', 'Gov_Mind_Control'),
    ('Influencers', 'Influencers_Coverage'), ('Iran', 'Iran'),
    ('Law_Enforcement', 'Law_Enforcement'), ('security_law_enforcement', 'Law_Enforcement'),
    ('Locations', 'Locations'), ('Media', 'Media_Coverage'), ('Medical', 'Medical'),
    ('Motive', 'Motive'), ('Narrative', 'Official_Narrative'),
    ('Other', 'Other_Topics'), ('other_topics', 'Other_Topics'),
    ('political_context', 'Political_Context'),
    ('Tyler_Robinson_Not_Assassin', 'Tyler_Not_Assassin'), ('Proof_Not_Tyler', 'Tyler_Not_Assassin'),
    ('social_media_analysis', 'Social_Media'),
    ('Suspects', 'Suspects'), ('Suspicious', 'Suspicious_Anomalies'),
    ('technology_surveillance', 'Tech_Surveillance'),
    ('Theories', 'Theories'), ('Timeline', 'Timeline'),
    ('Vote', 'Vote'), ('Witnesses', 'Witnesses'),
    ('Your_Actions_Fix_It', 'Your_Actions'),
]
NEW_L3_TITLES = {
    'After_Shooting': 'After the Shooting', 'Before_Shooting': 'Before the Shooting',
    'Analysis_Documentation': 'Analysis and Documentation', 'Security_Cameras': 'Security Cameras',
    'Cause_of_Death': 'Cause of Death', 'Censorship_Evidence': 'Censorship',
    'Companies_Orgs': 'Companies and Organizations', 'Cover_Up_Evidence': 'Cover Up',
    'Defamation_Cases': 'Defamation Cases', 'Drones_Evidence': 'Drones',
    'Electrocution': 'Electrocution', 'Fix_Laws': 'Fix Laws',
    'Government': 'Government Organizations', 'Gov_Mind_Control': 'Government Mind Control',
    'Influencers_Coverage': 'Influencers', 'Iran': 'Iran',
    'Law_Enforcement': 'Law Enforcement', 'Locations': 'Locations',
    'Media_Coverage': 'Media Coverage', 'Medical': 'Medical', 'Motive': 'Motive',
    'Official_Narrative': 'The Official Narrative', 'Other_Topics': 'Other',
    'Political_Context': 'Political Context', 'Tyler_Not_Assassin': 'Tyler Robinson Not Assassin',
    'Social_Media': 'Social Media Analysis', 'Suspects': 'Suspects',
    'Suspicious_Anomalies': 'Suspicious Anomalies', 'Tech_Surveillance': 'Technology and Surveillance',
    'Theories': 'Theories', 'Timeline': 'Timeline', 'Vote': 'Vote',
    'Witnesses': 'Witnesses', 'Your_Actions': 'Your Actions Fix It',
}
EXCLUDED_DIRS = {'Photos', 'Videos', 'Topics3'}

# ---------- load ----------
doc = yaml.safe_load(open(YAML_PATH))
report = {}

used_keys = set()
sha_index = {}   # sha256 -> list of image-dicts (inner dict)
node_count_before = {'l3': 0, 'l4': 0, 'l5': 0, 'l6': 0}
img_count_before = 0

def child_list(node):
    for lv in (4, 5, 6, 7):
        if f'level_{lv}' in node and node[f'level_{lv}'] is not None:
            yield lv, node[f'level_{lv}']

def walk_index(items, lvl):
    global img_count_before
    for it in items:
        node = it[f'level_{lvl}']
        used_keys.add(node['_key'])
        node_count_before[f'l{lvl}'] = node_count_before.get(f'l{lvl}', 0) + 1
        for kind in ('images', 'videos'):
            for im in (node.get(kind) or []):
                inner = im.get('image') or im.get('video')
                img_count_before += 1
                sha_index.setdefault(inner['sha256'], []).append(inner)
        for nl, arr in child_list(node):
            walk_index(arr, nl)

walk_index(doc['level_3'], 3)

inventory = {}   # sha256 -> mirror orig_path (tilde)
with open(INVENTORY) as f:
    next(f)
    for line in f:
        p = line.rstrip('\n').split('\t')
        if len(p) >= 4:
            inventory.setdefault(p[0], p[3])

pages_meta = {}  # repo-rel file_path -> (page_key, title)
with open(PAGES_CSV) as f:
    for row in csv.DictReader(f):
        pages_meta[row['file_path']] = (row['page_key'], row['title'])

def norm(s):
    # A _key or title of a date-named directory (e.g. 20230207) round-trips out of
    # images.yaml as an int, not a str, and .lower() then raises. Coerce before
    # normalising rather than rewriting hundreds of YAML keys.
    return re.sub(r'[^a-z0-9]', '', str(s if s is not None else '').lower())

def mk_key(seg, parent_key=None):
    base = re.sub(r'[^A-Za-z0-9_]+', '_', seg).strip('_')
    base = '_'.join([w for w in base.split('_') if w][:4]) or 'Node'
    k = base
    if k in used_keys and parent_key:
        k = '_'.join(((parent_key.split('_')[0] + '_' + base).split('_'))[:4])
    n = 2; stem = k
    while k in used_keys:
        k = f'{stem}_{n}'; n += 1
    used_keys.add(k)
    return k

def page_title(abs_path, fallback):
    try:
        txt = open(abs_path, encoding='utf-8', errors='replace').read()
    except OSError:
        return fallback
    m = re.search(r'^---\n.*?^title:\s*["\']?(.+?)["\']?\s*$.*?^---', txt, re.S | re.M)
    if m: return m.group(1).strip()
    m = re.search(r'^#\s+(.+)$', txt, re.M)
    if m: return re.sub(r'[*_`\[\]]', '', m.group(1)).strip()
    return fallback

def l3_by_key(key):
    for it in doc['level_3']:
        if it['level_3']['_key'] == key:
            return it['level_3']
    return None

# ---------- Stage 3: site Level 2 sweep -> level_3 superset ----------
new_l3, matched_l3 = [], []
for d, key in SITE_MAP:
    node = l3_by_key(key)
    if node is None:
        node = {'title': NEW_L3_TITLES[key], '_key': key, 'site_level_2': [],
                'number_of_images': 0, 'number_of_images_recursive': 0, 'images': []}
        used_keys.add(key)
        doc['level_3'].append({'level_3': node})
        new_l3.append(key)
    elif key not in [x for x in new_l3] and key not in matched_l3:
        matched_l3.append(key)
    sl2 = node.setdefault('site_level_2', [])
    if d not in sl2:
        sl2.append(d)
for it in doc['level_3']:
    it['level_3'].setdefault('site_level_2', [])
report['stage3'] = f"site dirs swept: {len(SITE_MAP)} | matched existing level_3: {len(set(matched_l3))} | new level_3: {len(new_l3)}"
report['stage3_new'] = new_l3

# ---------- Stage 5: filesystem pages -> level_4/level_5 nodes ----------
page_node = {}   # repo-rel page path -> node dict that owns its images
def is_page(f): return f.endswith(('.md', '.mdx')) and f != '_category_.json'

def find_child(node, name_candidates, child_lvl):
    arr = node.get(f'level_{child_lvl}')
    if not arr: return None
    cands = {norm(c) for c in name_candidates if c}
    for it in arr:
        ch = it[f'level_{child_lvl}']
        if norm(ch['_key']) in cands or norm(ch['title']) in cands:
            return ch
    return None

def ensure_child(node, child_lvl, title, seg, site_page):
    ch = find_child(node, [title, seg, os.path.splitext(os.path.basename(site_page))[0]], child_lvl)
    created = False
    if ch is None:
        pk = pages_meta.get(site_page, (None, None))[0]
        key = pk if (pk and pk not in used_keys) else None
        if key: used_keys.add(key)
        else: key = mk_key(seg, node['_key'])
        ch = {'title': title, '_key': key, 'number_of_images': 0,
              'number_of_images_recursive': 0, 'images': []}
        node.setdefault(f'level_{child_lvl}', []).append({f'level_{child_lvl}': ch})
        created = True
    if site_page and not ch.get('site_page'):
        ch['site_page'] = site_page
    return ch, created

stats5 = {'l4_new': 0, 'l4_merged': 0, 'deep_new': 0, 'deep_merged': 0}

def attach_dir(parent_node, abs_dir, rel_dir, child_lvl):
    """Attach every page and subdir of abs_dir under parent_node at child_lvl."""
    try: entries = sorted(os.listdir(abs_dir))
    except OSError: return
    for f in entries:
        p = os.path.join(abs_dir, f)
        rel = os.path.join(rel_dir, f)
        if os.path.isfile(p) and is_page(f):
            stem = os.path.splitext(f)[0]
            if stem.lower() in ('overview', 'index'):
                if not parent_node.get('site_page'):
                    parent_node['site_page'] = rel
                page_node[rel] = parent_node
                continue
            title = pages_meta.get(rel, (None, None))[1] or page_title(p, stem.replace('_', ' ').replace('-', ' '))
            ch, created = ensure_child(parent_node, child_lvl, title, stem, rel)
            k = 'l4' if child_lvl == 4 else 'deep'
            stats5[f'{k}_new' if created else f'{k}_merged'] += 1
            page_node[rel] = ch
        elif os.path.isdir(p):
            ov = None
            for cand in ('overview.mdx', 'overview.md', 'index.mdx', 'index.md'):
                if os.path.isfile(os.path.join(p, cand)):
                    ov = os.path.join(rel, cand); break
            title = (pages_meta.get(ov, (None, None))[1] if ov else None) or f.replace('_', ' ').replace('-', ' ')
            ch, created = ensure_child(parent_node, child_lvl, title, f, ov or '')
            k = 'l4' if child_lvl == 4 else 'deep'
            stats5[f'{k}_new' if created else f'{k}_merged'] += 1
            attach_dir(ch, p, rel, min(child_lvl + 1, 7))

seen_primary = set()
for d, key in SITE_MAP:
    abs_dir = os.path.join(DOCS, d)
    if not os.path.isdir(abs_dir): continue
    node = l3_by_key(key)
    rel_dir = os.path.join('site/docs', d)
    if key not in seen_primary:
        seen_primary.add(key)
        attach_dir(node, abs_dir, rel_dir, 4)
    else:
        ov = None
        for cand in ('overview.mdx', 'overview.md'):
            if os.path.isfile(os.path.join(abs_dir, cand)):
                ov = os.path.join(rel_dir, cand); break
        title = (pages_meta.get(ov, (None, None))[1] if ov else None) or d.replace('_', ' ').replace('-', ' ')
        ch, created = ensure_child(node, 4, title, d, ov or '')
        stats5['l4_new' if created else 'l4_merged'] += 1
        attach_dir(ch, abs_dir, rel_dir, 5)
report['stage5'] = stats5

# ---------- Stage 6: page image sweep -> image entries ----------
# Fallback bucket for images on pages that map to no node. Look up by the level_3
# _KEY ('Other_Topics'), not by the site DIRECTORY name ('Other') — SITE_MAP maps
# the dir 'Other' to the key 'Other_Topics'. Using the dir name returned None and
# crashed Stage 6 with "'NoneType' object has no attribute 'setdefault'".
other_node = l3_by_key('Other_Topics')
if other_node is None:
    raise SystemExit("grow_hierarchy: level_3 node 'Other_Topics' is missing from "
                     "images/images.yaml; Stage 6 has no fallback bucket.")
IMG_RE = [
    re.compile(r'!\[[^\]]*\]\(\s*([^)\s]+)'),
    re.compile(r'<img[^>]*?src=["\']([^"\']+)["\']', re.I),
    re.compile(r'\]\(\s*([^)\s]+?\.(?:png|jpe?g|webp|gif|avif))\s*\)', re.I),
]
VID_RE = [
    re.compile(r'<(?:video|source)[^>]*?src=["\']([^"\']+)["\']', re.I),
    re.compile(r'\]\(\s*([^)\s]+?\.(?:mp4|mov|webm|m4v))\s*\)', re.I),
    re.compile(r'<iframe[^>]*?src=["\']([^"\']+\.(?:mp4|mov|webm|m4v))["\']', re.I),
]

def resolve_asset(src, page_abs_dir):
    src = src.strip().strip('"\'')
    if src.startswith(('http://', 'https://', 'data:', 'ipfs://')): return None
    src = src.split('#')[0].split('?')[0]
    src = urllib.parse.unquote(src)
    if src.startswith('pathname://'): src = src[len('pathname://'):]
    cands = []
    if src.startswith('/'):
        for sd in STATIC_DIRS: cands.append(os.path.join(sd, src.lstrip('/')))
    else:
        cands.append(os.path.normpath(os.path.join(page_abs_dir, src)))
    for c in cands:
        if os.path.isfile(c): return c
    return None

def sha256_of(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

stats6 = {'pages': 0, 'found': 0, 'mirror_matched': 0, 'new_img': 0, 'updated': 0,
          'new_vid': 0, 'unresolved': 0, 'external': 0}
static_sha_cache = {}
all_pages = []
for root_, dirs, files in os.walk(DOCS):
    for f in files:
        if is_page(f): all_pages.append(os.path.join(root_, f))

for abs_page in sorted(all_pages):
    rel_page = os.path.relpath(abs_page, ROOT)
    stats6['pages'] += 1
    try: txt = open(abs_page, encoding='utf-8', errors='replace').read()
    except OSError: continue
    found_img, found_vid = set(), set()
    for rx in IMG_RE:
        for m in rx.findall(txt):
            if m.lower().endswith(IMG_EXT) or rx is IMG_RE[1]: found_img.add(m)
    for rx in VID_RE:
        for m in rx.findall(txt): found_vid.add(m)
    if not found_img and not found_vid: continue
    target = page_node.get(rel_page) or other_node
    for kind, found in (('image', found_img), ('video', found_vid)):
        for src in sorted(found):
            if src.startswith(('http://', 'https://')):
                stats6['external'] += 1; continue
            abs_asset = resolve_asset(src, os.path.dirname(abs_page))
            if not abs_asset:
                stats6['unresolved'] += 1; continue
            if kind == 'image' and not abs_asset.lower().endswith(IMG_EXT): continue
            stats6['found'] += 1
            if abs_asset not in static_sha_cache:
                static_sha_cache[abs_asset] = sha256_of(abs_asset)
            sha = static_sha_cache[abs_asset]
            if sha in sha_index:
                for inner in sha_index[sha]:
                    osp = inner.setdefault('on_site_pages', [])
                    if rel_page not in osp: osp.append(rel_page)
                stats6['updated'] += 1
                continue
            if sha in inventory:
                fp = inventory[sha]; stats6['mirror_matched'] += 1
            else:
                fp = abs_asset.replace(HOME, '~')
            inner = {'cid': '', 'sha256': sha, 'file_path': fp,
                     'ai_description': '', 'on_site_pages': [rel_page]}
            arr_name = 'images' if kind == 'image' else 'videos'
            target.setdefault(arr_name, [])
            if target[arr_name] is None: target[arr_name] = []
            target[arr_name].append({kind: inner})
            sha_index.setdefault(sha, []).append(inner)
            stats6['new_img' if kind == 'image' else 'new_vid'] += 1
report['stage6'] = stats6

# ---------- Stage 7: sidecar file-path properties ----------
def sidecar_base(fp_tilde):
    """Return (tilde_base_candidates) for a media file_path."""
    if fp_tilde.startswith(MIRROR_TILDE + '/'):
        rel = fp_tilde[len(MIRROR_TILDE) + 1:]
        return [(SIDE, SIDE_TILDE, rel), (SIDE_LEGACY, SIDE_LEGACY_TILDE, rel)]
    if fp_tilde.startswith(ROOT_TILDE + '/'):
        rel = fp_tilde[len(ROOT_TILDE) + 1:]
        return [(REPO_SIDE, REPO_SIDE_TILDE, rel)]
    return []

def read_desc_overview(abs_side):
    try: raw = open(abs_side, encoding='utf-8', errors='replace').read()
    except OSError: return ''
    i = raw.find('description:')
    if i == -1: return ''
    body = re.sub(r'^description:\s*[>|][-+]?\s*\n?', '', raw[i:])
    body = '\n'.join(s[2:] if s.startswith('  ') else s for s in body.split('\n')).strip()
    body = re.sub(r'^##\s*Overview\s*\n', '', body, flags=re.I)
    overview = re.split(r'\n##\s', body)[0].strip()
    return re.sub(r'\s+', ' ', overview).strip()

stats7 = {'entries': 0, 'desc': 0, 'ocr': 0, 'trans': 0, 'inline_filled': 0, 'no_sidecars': 0}
def fill_sidecars(items):
    for it in items:
        for lvl, arr in [(k, v) for k, v in it.items() if k.startswith('level_')]:
            pass
def walk_fill(items, lvl):
    for it in items:
        node = it[f'level_{lvl}']
        for kind in ('images', 'videos'):
            for im in (node.get(kind) or []):
                inner = im.get('image') or im.get('video')
                stats7['entries'] += 1
                fp = inner.get('file_path', '')
                bases = sidecar_base(fp)
                got_any = False
                for prop, ext, cnt in (('ai_description_file', '.ai_description', 'desc'),
                                       ('ocr_file', '.ocr', 'ocr'),
                                       ('transcription_file', '.transcription', 'trans')):
                    val = ''
                    for absb, tilb, rel in bases:
                        cand = os.path.join(absb, rel + ext)
                        if os.path.isfile(cand):
                            val = f'{tilb}/{rel}{ext}'; break
                    inner[prop] = val
                    if val: stats7[cnt] += 1; got_any = True
                if not got_any: stats7['no_sidecars'] += 1
                if not inner.get('ai_description') and inner.get('ai_description_file'):
                    d = read_desc_overview(os.path.expanduser(inner['ai_description_file']))
                    if d:
                        inner['ai_description'] = d; stats7['inline_filled'] += 1
        for nl, arr in child_list(node):
            walk_fill(arr, nl)
walk_fill(doc['level_3'], 3)
report['stage7'] = stats7

# ---------- Stage 8: counts, needs_split, integrity ----------
stats8 = {'needs_split': 0}
def recount(items, lvl):
    total = 0
    for it in items:
        node = it[f'level_{lvl}']
        direct = len(node.get('images') or []) + len(node.get('videos') or [])
        sub = 0
        for nl, arr in child_list(node):
            sub += recount(arr, nl)
        node['number_of_images'] = direct
        node['number_of_images_recursive'] = direct + sub
        if direct > 12:
            node['needs_split'] = True; stats8['needs_split'] += 1
        elif 'needs_split' in node:
            del node['needs_split']
        total += direct + sub
    return total
grand_total = recount(doc['level_3'], 3)

# integrity: unique keys, no dup sha within one node
key_seen, key_dups, sha_dup_in_node = set(), [], []
def walk_check(items, lvl):
    for it in items:
        node = it[f'level_{lvl}']
        k = node['_key']
        if k in key_seen: key_dups.append(k)
        key_seen.add(k)
        for kind in ('images', 'videos'):
            local = set()
            for im in (node.get(kind) or []):
                inner = im.get('image') or im.get('video')
                ident = inner.get('sha256') or inner.get('cid') or ''
                if ident and ident in local: sha_dup_in_node.append((k, ident[:12]))
                if ident: local.add(ident)
        for nl, arr in child_list(node):
            walk_check(arr, nl)
walk_check(doc['level_3'], 3)
stats8.update({'dup_keys': key_dups, 'dup_sha_in_node': sha_dup_in_node, 'grand_total': grand_total})
report['stage8'] = stats8

# ---------- emit ----------
# Field policy (OUTPUT SANITIZATION rule): prose fields get content-sanitized
# (invisible unicode removed); identity fields keep their exact value but any
# non-ASCII is emitted as a visible \uXXXX escape. The file bytes stay visible.
PROSE_FIELDS = {'title', 'ai_description'}
def q(s):
    return q_identity(s)

out = []
# Keep this header identical to the one bind_image_pages.py emits — bind runs after
# grow, so a divergent header here just churns the first 12 lines of a 3 MB file.
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

MEDIA_ORDER = ['cid', 'sha256', 'file_path', 'ai_description', 'ai_description_file',
               'ocr_file', 'transcription_file', 'on_site_pages', 'also_filed_in']
NODE_SCALARS = ['title', '_key']

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
            # LIST OF {page: ...} MAPPINGS — emit as block mappings. The generic
            # list branch below would stringify the dicts ("- page': ...") and an
            # empty list would be dropped entirely; both are stored with an
            # explicit [] when empty, so [] must round-trip. Keep this identical
            # to emit_media in bind_image_pages.py. Getting this wrong silently
            # mangled 1,693 entries on 2026-08-12.
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
open(YAML_PATH, 'w').write('\n'.join(out) + '\n')

# re-parse to prove validity, then the mandatory invisible-character scan
yaml.safe_load(open(YAML_PATH))
validate_no_invisible(YAML_PATH)

# ---------- report ----------
print('BEFORE:', node_count_before, '| media entries:', img_count_before)
for k in ('stage3', 'stage3_new', 'stage5', 'stage6', 'stage7', 'stage8'):
    print(k.upper() + ':', report[k])
nc = {'l3': 0, 'l4': 0, 'l5': 0, 'l6': 0, 'l7': 0}
me = [0]
def wc(items, lvl):
    for it in items:
        n = it[f'level_{lvl}']
        nc[f'l{lvl}'] = nc.get(f'l{lvl}', 0) + 1
        me[0] += len(n.get('images') or []) + len(n.get('videos') or [])
        for nl, arr in child_list(n): wc(arr, nl)
wc(doc['level_3'], 3)
print('AFTER:', nc, '| media entries:', me[0])
print('YAML re-parses: yes')
