#!/usr/bin/env python3
# fixup_hierarchy.py — follow-up pass after grow_hierarchy.py:
#  1. resolve the duplicate 'Other' _key (rename the run-created level_3 to Other_Topics)
#  2. collapse same-sha256 duplicates WITHIN one node (merge properties, keep first)
#  3. bind site IPFS embeds: pages referencing https://ipfs.io/ipfs/<CID> get the CID
#     stamped onto the matching image entry (matched by sha256 via local IPFS node);
#     unmatched CIDs become new image/video entries under the page's node (ipfs_url kept)
#  4. recount, integrity check, emit.
import os, re, json, yaml, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sanitize_common import sanitize_prose, q_prose, q_identity, validate_no_invisible

HOME = os.path.expanduser('~')
ROOT = os.path.join(HOME, 'BGit/Bryan_git/charlie-kirk')
YAML_PATH = os.path.join(ROOT, 'images/images.yaml')
SCRATCH = '/private/tmp/claude-501/-Users-bryan-BGit-Bryan-git-charlie-kirk-image-planning/6c121314-b0c0-4abf-baa6-de96ef3106bc/scratchpad'

doc = yaml.safe_load(open(YAML_PATH))
cid_pages = json.load(open(os.path.join(SCRATCH, 'cids.json')))
cid_sha = json.load(open(os.path.join(SCRATCH, 'cid_sha.json')))
cid_kind = json.load(open(os.path.join(SCRATCH, 'cid_kind.json')))

def child_list(node):
    for lv in (4, 5, 6, 7):
        if node.get(f'level_{lv}'):
            yield lv, node[f'level_{lv}']

# ---- collect ----
all_keys, sha_index, page_map = [], {}, {}
cid_index = set()
def walk(items, lvl, fn):
    for it in items:
        node = it[f'level_{lvl}']
        fn(node, lvl)
        for nl, arr in child_list(node):
            walk(arr, nl, fn)

def collect(node, lvl):
    all_keys.append(node['_key'])
    if node.get('site_page'):
        page_map.setdefault(node['site_page'], node)
    for kind in ('images', 'videos'):
        for im in (node.get(kind) or []):
            inner = im.get('image') or im.get('video')
            if inner.get('sha256'):
                sha_index.setdefault(inner['sha256'], []).append(inner)
            if inner.get('cid'):
                cid_index.add(inner['cid'])
walk(doc['level_3'], 3, collect)

# ---- 1. duplicate 'Other' key ----
renamed = None
if all_keys.count('Other') > 1:
    for it in doc['level_3']:
        n = it['level_3']
        if n['_key'] == 'Other' and 'Other' in n.get('site_level_2', []):
            assert 'Other_Topics' not in all_keys
            n['_key'] = 'Other_Topics'
            renamed = "level_3 'Other' (site catch-all) -> Other_Topics"
            break

# ---- 2. same-sha dupes within one node ----
collapsed = []
def dedupe(node, lvl):
    for kind in ('images', 'videos'):
        arr = node.get(kind) or []
        seen = {}
        keep = []
        for im in arr:
            inner = im.get('image') or im.get('video')
            sha = inner.get('sha256') or inner.get('cid')
            if sha and sha in seen:
                first = seen[sha]
                for prop in ('on_site_pages', 'also_filed_in'):
                    for v in inner.get(prop, []) or []:
                        first.setdefault(prop, [])
                        if v not in first[prop]: first[prop].append(v)
                if inner.get('cid') and not first.get('cid'): first['cid'] = inner['cid']
                if inner.get('ai_description') and not first.get('ai_description'):
                    first['ai_description'] = inner['ai_description']
                collapsed.append((node['_key'], (sha or '')[:12]))
                continue
            if sha: seen[sha] = inner
            keep.append(im)
        if arr: node[kind] = keep
walk(doc['level_3'], 3, dedupe)

# ---- 3. bind IPFS CIDs ----
other_node = next(it['level_3'] for it in doc['level_3'] if it['level_3']['_key'] == 'Other_Topics')
stats = {'cid_stamped': 0, 'new_img': 0, 'new_vid': 0, 'unknown_kept': 0}
for cid, pages in cid_pages.items():
    sha = cid_sha.get(cid, {}).get('sha256', '')
    kind = cid_kind.get(cid, 'unknown')
    if sha and sha in sha_index:
        for inner in sha_index[sha]:
            if not inner.get('cid'): inner['cid'] = cid
            osp = inner.setdefault('on_site_pages', [])
            for p in pages:
                if p not in osp: osp.append(p)
        stats['cid_stamped'] += 1
        continue
    if cid in cid_index:   # already present (rerun) — idempotent, no dupe
        stats['cid_stamped'] += 1
        continue
    # new entry under the first referencing page's node (fallback: Other_Topics)
    target = next((page_map[p] for p in pages if p in page_map), other_node)
    entry_kind = 'video' if kind == 'video' else 'image'
    if kind in ('unknown', 'other', 'pdf'):
        entry_kind = 'image'; stats['unknown_kept'] += 1
    inner = {'cid': cid, 'sha256': sha, 'file_path': '',
             'ipfs_url': f'https://ipfs.io/ipfs/{cid}',
             'ai_description': '', 'ai_description_file': '', 'ocr_file': '',
             'transcription_file': '', 'on_site_pages': list(pages)}
    arr_name = 'images' if entry_kind == 'image' else 'videos'
    target.setdefault(arr_name, [])
    if target[arr_name] is None: target[arr_name] = []
    target[arr_name].append({entry_kind: inner})
    if sha: sha_index.setdefault(sha, []).append(inner)
    stats['new_img' if entry_kind == 'image' else 'new_vid'] += 1

# ---- 4. recount + integrity ----
needs_split = [0]
def recount(items, lvl):
    total = 0
    for it in items:
        node = it[f'level_{lvl}']
        direct = len(node.get('images') or []) + len(node.get('videos') or [])
        sub = sum(recount(arr, nl) for nl, arr in child_list(node))
        node['number_of_images'] = direct
        node['number_of_images_recursive'] = direct + sub
        if direct > 12:
            node['needs_split'] = True; needs_split[0] += 1
        elif 'needs_split' in node:
            del node['needs_split']
        total += direct + sub
    return total
grand = recount(doc['level_3'], 3)

keys2, dups2, shadup2 = set(), [], []
def check(node, lvl):
    k = node['_key']
    if k in keys2: dups2.append(k)
    keys2.add(k)
    for kind in ('images', 'videos'):
        local = set()
        for im in (node.get(kind) or []):
            inner = im.get('image') or im.get('video')
            ident = inner.get('sha256') or inner.get('cid')
            if ident in local: shadup2.append((k, ident[:12]))
            local.add(ident)
walk(doc['level_3'], 3, check)

# ---- emit (same conventions as grow_hierarchy.py) ----
# Field policy (OUTPUT SANITIZATION rule): prose sanitized, identity fields
# emitted with visible \uXXXX escapes — the file bytes must contain nothing invisible.
PROSE_FIELDS = {'title', 'ai_description'}
def q(s): return q_identity(s)
MEDIA_ORDER = ['cid', 'sha256', 'file_path', 'ipfs_url', 'ai_description', 'ai_description_file',
               'ocr_file', 'transcription_file', 'on_site_pages', 'also_filed_in']
out = []
out.append('# images.yaml — image evidence hierarchy for the Charlie Kirk site.')
out.append('# GENERATED first pass from ~/_Mirror/Politics/Charlie_Kirk_Mi; GROWN by')
out.append('# p_create_image_hierarchy.md: site Level 2/3/4 pages mirrored in as level_3/4/5')
out.append('# (level incremented by one), page-embedded images bound in, sidecar file paths')
out.append('# (.ai_description / .ocr / .transcription) resolved via Large File Bridge mapping,')
out.append('# and site IPFS embeds (ipfs.io/ipfs/<CID>) bound to entries by sha256 via local IPFS.')
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
        if k == 'sha256': out.append(f'{p2}{k}: {v if v else chr(34)+chr(34)}')
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
        out.append(f'{p2}level_{nl}:')
        for c in arr: emit_node(c, nl, indent + 6)

out.append('level_3:')
for it in doc['level_3']:
    emit_node(it, 3, 2)
open(YAML_PATH, 'w').write('\n'.join(out) + '\n')
yaml.safe_load(open(YAML_PATH))
validate_no_invisible(YAML_PATH)

print('renamed:', renamed)
print('within-node dupes collapsed:', len(collapsed), collapsed)
print('cid binding:', stats)
print('needs_split nodes:', needs_split[0], '| media total:', grand)
print('dup keys now:', dups2, '| dup sha-in-node now:', shadup2)
print('YAML re-parses: yes')
