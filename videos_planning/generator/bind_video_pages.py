#!/usr/bin/env python3
# bind_video_pages.py — STAGE 12 of p_update_video_hierarchy.md.
# Records which published Level 5 page under site/docs/Videos hosts each video.
# READS site pages; never creates, renames, or edits one. On the first several
# runs this correctly sets every video_page to "" — the pages do not exist yet.
import os, re, csv, json

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.expanduser('~/BGit/Bryan_git/charlie-kirk')
VIDEOS_L2 = os.path.join(ROOT, 'site/docs/Videos')
TILDE_L2 = '~/BGit/Bryan_git/charlie-kirk/site/docs/Videos'

cids = json.load(open(os.path.join(HERE, 'cids.json'), encoding='utf-8'))['entries']
tree = json.load(open(os.path.join(HERE, 'tree.json'), encoding='utf-8'))
nodes = tree['nodes']
prev = {}
pj = os.path.join(HERE, 'video_page.json')
if os.path.exists(pj):
    prev = json.load(open(pj, encoding='utf-8'))

# ---------------------------------------------------------------- index pages
by_pair, by_ident, pages_total, pages_with, pages_without = {}, {}, 0, 0, []
for dirpath, _, filenames in os.walk(VIDEOS_L2):
    for fn in filenames:
        if not fn.endswith(('.mdx', '.md')):
            continue
        full = os.path.join(dirpath, fn)
        head = open(full, encoding='utf-8', errors='replace').read(4000)
        if not head.startswith('---'):
            continue
        fm = head.split('---', 2)[1] if head.count('---') >= 2 else ''
        pages_total += 1
        cid = re.search(r'^ck_video_cid:\s*"?([A-Za-z0-9]+)"?\s*$', fm, re.M)
        sha = re.search(r'^ck_video_sha256:\s*"?([0-9a-fA-F]{64})"?\s*$', fm, re.M)
        if not cid and not sha:
            pages_without.append(os.path.relpath(full, ROOT))
            continue
        nk = re.search(r'^ck_node_key:\s*"?(\S+?)"?\s*$', fm, re.M)
        nk = nk.group(1) if nk else ''
        tilde = f'{TILDE_L2}/{os.path.relpath(full, VIDEOS_L2)}'
        pages_with += 1
        for ident in filter(None, [cid.group(1) if cid else None,
                                   sha.group(1).lower() if sha else None]):
            by_pair.setdefault((ident, nk), tilde)
            by_ident.setdefault(ident, []).append((nk, tilde))

# ---------------------------------------------------------------- bind
video_node = {}
for nk, n in nodes.items():
    for v in n['videos']:
        video_node[v] = nk

out, st = {}, dict(pair=0, ident=0, empty=0, vanished=[])
for vkey, e in cids.items():
    nk = video_node.get(vkey, '')
    node_key = nodes[nk]['_key'] if nk else ''
    val = ''
    for ident in filter(None, [e.get('cid'), (e.get('sha256') or '').lower()]):
        if (ident, node_key) in by_pair:
            val = by_pair[(ident, node_key)]
            st['pair'] += 1
            break
    if not val:
        for ident in filter(None, [e.get('cid'), (e.get('sha256') or '').lower()]):
            c = by_ident.get(ident) or []
            if len(c) == 1:
                val = c[0][1]
                st['ident'] += 1
                break
    # never invent a path; never silently clear a recorded one
    if val and not os.path.exists(os.path.expanduser(val)):
        val = ''
    if not val and prev.get(vkey):
        p = os.path.expanduser(prev[vkey])
        if os.path.exists(p):
            val = prev[vkey]
        else:
            st['vanished'].append(prev[vkey])
    if not val:
        st['empty'] += 1
    assert '/Photos/' not in val, f'refusing a /Photos path for {vkey}'
    out[vkey] = val

json.dump(out, open(pj, 'w', encoding='utf-8'), indent=1)

print('============================')
print('STAGE 12 COMPLETE')
print(f'Video pages indexed under Videos: {pages_total} '
      f'({pages_with} with ck_ frontmatter, {len(pages_without)} without)')
print(f"Entries with video_page set: {st['pair']+st['ident']}   "
      f"by (identity,node): {st['pair']}   by identity only: {st['ident']}")
print(f"Entries with video_page \"\": {st['empty']} (no page exists yet)")
print(f"Recorded pages now missing from disk: {len(st['vanished'])} {st['vanished'][:5]}")
print('Paths under /Photos rejected: 0')
print('Hand-written pages carrying no ck_ frontmatter (not guessed by filename):')
for p in pages_without:
    print('   ' + p)
print('============================')
