#!/usr/bin/env python3
"""verify_stage_12_13.py — Stages 12 and 13 of p_update_image_hierarchy.md.

Read-only. Re-derives every checkable claim about images/images.yaml from disk:

  Stage 12  counts / needs_split / _key uniqueness / duplicate sha within a node /
            full property set on every entry / image_page resolves and lives under
            Photos / every should_be_on_pages path is real, non-placeholder, under
            docs and not under Photos / on_pages subset of should_be_on_pages /
            EVERY on_pages binding re-verified against the referencing page's bytes.
  Stage 13  an INDEPENDENT second extractor (HTML-parser based, not the regex the
            writer used) re-derives the page->image set and diffs it against the
            YAML. Two implementations agreeing is the only real defence against a
            systematic extraction bug.

Exit code 1 on any hard failure.
"""
import os, re, sys, yaml, hashlib, collections
from html.parser import HTMLParser

ROOT = os.path.expanduser('~/BGit/Bryan_git/charlie-kirk')
TILDE_ROOT = '~/BGit/Bryan_git/charlie-kirk'
YAML_PATH = os.path.join(ROOT, 'images/images.yaml')
DOCS = os.path.join(ROOT, 'site/docs')
PHOTOS = os.path.join(DOCS, 'Photos')
STATIC = os.path.join(ROOT, 'site/internals/static')
REQUIRED = ['cid', 'ipfs_pinned', 'sha256', 'file_path', 'ai_description',
            'ai_description_file', 'ocr_file', 'transcription_file',
            'image_page', 'on_pages', 'should_be_on_pages']

def expu(p): return os.path.expanduser(p) if p else p
fail = []
def bad(msg): fail.append(msg); print('  FAIL: ' + msg)

doc = yaml.safe_load(open(YAML_PATH, encoding='utf-8'))

def child_list(node):
    for k, v in node.items():
        if k.startswith('level_') and isinstance(v, list):
            yield int(k.split('_')[1]), v

entries = []          # (inner, node_key, level)
node_count = collections.Counter()
keys_seen = collections.Counter()
def rec(items, lvl):
    for it in items:
        n = it[f'level_{lvl}']
        node_count[lvl] += 1
        keys_seen[n['_key']] += 1
        direct = len(n.get('images') or []) + len(n.get('videos') or [])
        if n.get('number_of_images') != direct:
            bad(f'{n["_key"]}: number_of_images {n.get("number_of_images")} != {direct}')
        if direct > 12 and not n.get('needs_split'):
            bad(f'{n["_key"]}: {direct} direct images but needs_split not set')
        if direct <= 12 and n.get('needs_split'):
            bad(f'{n["_key"]}: needs_split set but only {direct} direct images')
        for kind in ('images', 'videos'):
            local = collections.Counter()
            for m in (n.get(kind) or []):
                inner = m.get('image') or m.get('video')
                if inner is None: continue
                entries.append((inner, n['_key'], lvl))
                ident = inner.get('sha256') or inner.get('ipfs_url') or ''
                if ident: local[ident] += 1
            for ident, c in local.items():
                if c > 1: bad(f'{n["_key"]}: sha256 {ident[:12]} appears {c}x in one node')
        for nl, arr in child_list(n):
            rec(arr, nl)
rec(doc['level_3'], 3)

print('=' * 28); print('STAGE 12 — COUNTS, PROPERTIES, INTEGRITY')
print(f'Nodes: ' + '  '.join(f'level_{k}: {v}' for k, v in sorted(node_count.items())))
print(f'Image/video entries: {len(entries)}')
dupk = [k for k, c in keys_seen.items() if c > 1]
print(f'Duplicate _keys: {len(dupk)}' + (f' {dupk[:5]}' if dupk else ''))
if dupk: bad(f'{len(dupk)} duplicate _keys')

# ---- full property set, image_page, should_be_on_pages validity
miss = collections.Counter(); ip_ok = ip_empty = 0; ip_bad = []
sb_total = sb_ok = 0; sb_bad = []; on_total = 0; deplaced = 0
PLACEHOLDER = ('...', 'TODO', 'TBD', '<', '>')
for inner, nk, lvl in entries:
    for k in REQUIRED:
        if k not in inner: miss[k] += 1
    ipg = inner.get('image_page') or ''
    if ipg:
        if not os.path.isfile(expu(ipg)): ip_bad.append(('missing', ipg))
        elif '/site/docs/Photos/' not in ipg: ip_bad.append(('not-under-Photos', ipg))
        else: ip_ok += 1
    else:
        ip_empty += 1
    sb = set()
    for pg in (inner.get('should_be_on_pages') or []):
        p = pg.get('page') if isinstance(pg, dict) else pg
        sb_total += 1; sb.add(p)
        if (any(t in p for t in PLACEHOLDER) or not p.startswith('~/')
                or not p.endswith(('.md', '.mdx')) or '/site/docs/' not in p
                or '/site/docs/Photos/' in p or not os.path.isfile(expu(p))):
            sb_bad.append(p)
        else: sb_ok += 1
    for pg in (inner.get('on_pages') or []):
        p = pg.get('page') if isinstance(pg, dict) else pg
        on_total += 1
        if p not in sb:
            deplaced += 1   # legal only when the page is not a docs page (component/blog)
            if p.endswith(('.md', '.mdx')) and '/site/docs/' in p:
                bad(f'on_pages not in should_be_on_pages: {p}')
for k, c in miss.items(): bad(f'{c} entries missing required key {k}')
print(f'Entries missing a required property: {sum(miss.values())}')
print(f'image_page set + resolves under Photos: {ip_ok}   "": {ip_empty}   invalid: {len(ip_bad)}')
if ip_bad: bad(f'{len(ip_bad)} bad image_page values, e.g. {ip_bad[:3]}')
print(f'should_be_on_pages assignments: {sb_total}   valid on disk: {sb_ok}   placeholders/invalid: {len(sb_bad)}')
if sb_bad: bad(f'{len(sb_bad)} bad should_be_on_pages values, e.g. {sb_bad[:3]}')
print(f'on_pages bindings: {on_total}   not mirrored into should_be_on_pages: {deplaced} '
      f'(non-docs pages — components/blog — which should_be_on_pages does not target)')

# ---- every on_pages binding re-verified against the page's bytes
sha_of = {}
cid_of = {}
for inner, nk, lvl in entries:
    s = (inner.get('sha256') or '').lower()
    if s:
        sha_of.setdefault(s, set())
        if inner.get('cid'): cid_of.setdefault(s, set()).add(inner['cid'])
verified = unverified = 0
page_cache = {}
for inner, nk, lvl in entries:
    s = (inner.get('sha256') or '').lower()
    for pg in (inner.get('on_pages') or []):
        p = pg.get('page') if isinstance(pg, dict) else pg
        full = expu(p)
        if '/site/docs/Photos/' in p: bad(f'on_pages under Photos: {p}')
        if not os.path.isfile(full):
            bad(f'on_pages page missing on disk: {p}'); unverified += 1; continue
        if full not in page_cache:
            page_cache[full] = open(full, encoding='utf-8', errors='replace').read()
        txt = page_cache[full]
        hit = s and s in txt
        if not hit:
            for c in cid_of.get(s, ()):
                if c in txt: hit = True; break
        if not hit:   # local static file whose bytes hash to this sha
            for m in re.finditer(r'["\'](/[^"\']+\.(?:jpg|jpeg|png|webp|gif))["\']', txt, re.I):
                d = os.path.join(STATIC, m.group(1).lstrip('/'))
                if os.path.isfile(d) and hashlib.sha256(open(d, 'rb').read()).hexdigest() == s:
                    hit = True; break
        if hit: verified += 1
        else: unverified += 1; bad(f'on_pages binding unsubstantiated: {s[:12]} on {p}')
print(f'on_pages bindings verified against page bytes: {verified}/{verified+unverified}')

txt_all = open(YAML_PATH, encoding='utf-8').read()
print(f'on_site_pages remaining in file: {txt_all.count("on_site_pages")}')
print(f'YAML parses: yes')

# ---------------------------------------------------------------- Stage 13
print('=' * 28); print('STAGE 13 — INDEPENDENT RE-DERIVATION')

class Grab(HTMLParser):
    """Second extractor, deliberately NOT the writer's regex: a real HTML/JSX tag
    parser. If the two disagree the writer's pattern has a systematic bug."""
    def __init__(self):
        super().__init__(convert_charrefs=True); self.srcs = []
    def handle_starttag(self, tag, attrs):
        if tag in ('img', 'iframe', 'video', 'source'):
            for k, v in attrs:
                if k in ('src', 'poster') and v: self.srcs.append(v)

RE_CID = re.compile(r'(?:ipfs\.io/ipfs/|ipfs://|dweb\.link/ipfs/)([A-Za-z0-9]{40,})'
                    r'|([A-Za-z0-9]{46,})\.ipfs\.dweb\.link')
cid_to_sha = {}
for s, cs in cid_of.items():
    for c in cs: cid_to_sha[c] = s

indep = collections.defaultdict(set)     # sha -> {tilde page}
pages_seen = 0
for dp, dn, fns in os.walk(DOCS):
    dn[:] = [d for d in dn if d not in ('Photos',)]
    for fn in fns:
        if not fn.endswith(('.md', '.mdx')): continue
        full = os.path.join(dp, fn)
        rel = os.path.relpath(full, ROOT)
        if rel.startswith('site/docs/Photos/'): continue
        t = open(full, encoding='utf-8', errors='replace').read()
        pages_seen += 1
        g = Grab()
        try: g.feed(t)
        except Exception: pass
        srcs = list(g.srcs) + re.findall(r'!\[[^\]]*\]\(([^)\s]+)', t)
        tilde = f'{TILDE_ROOT}/{rel}'
        for s in srcs:
            m = RE_CID.search(s)
            if m:
                c = m.group(1) or m.group(2)
                if c in cid_to_sha: indep[cid_to_sha[c]].add(tilde)
                continue
            me = re.search(r'/img/evidence/([0-9a-f]{64})', s)
            if me:
                if me.group(1) in sha_of: indep[me.group(1)].add(tilde)
                continue
            if s.startswith('/') and s.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif')):
                d = os.path.join(STATIC, s.lstrip('/'))
                if os.path.isfile(d):
                    h = hashlib.sha256(open(d, 'rb').read()).hexdigest()
                    if h in sha_of: indep[h].add(tilde)

recorded = collections.defaultdict(set)
for inner, nk, lvl in entries:
    s = (inner.get('sha256') or '').lower()
    for pg in (inner.get('on_pages') or []):
        p = pg.get('page') if isinstance(pg, dict) else pg
        if p.endswith(('.md', '.mdx')) and '/site/docs/' in p:
            recorded[s].add(p)

ind_pairs = {(s, p) for s, ps in indep.items() for p in ps}
rec_pairs = {(s, p) for s, ps in recorded.items() for p in ps}
print(f'Docs pages scanned (non-Photos): {pages_seen}')
print(f'Independent extractor pairs: {len(ind_pairs)}   YAML-recorded docs pairs: {len(rec_pairs)}')
only_ind = ind_pairs - rec_pairs
only_rec = rec_pairs - ind_pairs
print(f'In independent but MISSING from YAML: {len(only_ind)}')
for s, p in sorted(only_ind)[:8]: print(f'    {s[:12]}  {p}')
print(f'In YAML but NOT found independently: {len(only_rec)}')
for s, p in sorted(only_rec)[:8]: print(f'    {s[:12]}  {p}')
if only_ind: bad(f'{len(only_ind)} bindings the independent extractor found that the YAML lacks')
if only_rec: bad(f'{len(only_rec)} YAML bindings the independent extractor cannot reproduce')

# ---- tree summary
print('=' * 28); print('TREE SUMMARY (level_3)')
for it in doc['level_3']:
    n = it['level_3']
    kids = sum(len(a) for _, a in child_list(n))
    print(f'  {n["number_of_images_recursive"]:5d} imgs  {kids:3d} children  {n["_key"]}')

print('=' * 28)
if fail:
    print(f'RESULT: {len(fail)} FAILURES'); sys.exit(1)
print('RESULT: all Stage 12 + Stage 13 checks pass')
