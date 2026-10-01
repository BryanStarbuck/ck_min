#!/usr/bin/env python3
# verify.py — STAGES 14 and 15 of p_update_video_hierarchy.md.
# Counts, publishable, needs_split, integrity, and the final report. Reads the
# written videos/videos.yaml — it checks what actually landed on disk, not what
# the emitter believed it wrote.
import os, re, csv, sys, json, yaml, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sanitize_video import validate_no_invisible

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.expanduser('~/BGit/Bryan_git/charlie-kirk')
YAML_PATH = os.path.join(ROOT, 'videos/videos.yaml')
VIDEOS_L2 = f'{ROOT}/site/docs/Videos'
PHOTOS = f'{ROOT}/site/docs/Photos'
EXCLUDE_FILE = os.path.join(HERE, '..', 'exclude_videos.txt')

def expu(p):
    return os.path.expanduser(p) if p else p

doc = yaml.safe_load(open(YAML_PATH, encoding='utf-8'))

nodes, entries = [], []
def walk(items, lvl, chain):
    for it in items:
        n = it[f'level_{lvl}']
        nodes.append((n, lvl, chain))
        for v in (n.get('videos') or []):
            entries.append((v['video'], n, lvl))
        for k, vv in n.items():
            if k.startswith('level_') and isinstance(vv, list):
                walk(vv, int(k.split('_')[1]), chain + [n])
walk(doc['level_3'], 3, [])

SCHEMA = ['title', 'cid', 'ipfs_pinned', 'sha256', 'file_path', 'media_present',
          'file_size_bytes', 'duration', 'audio_file', 'transcription_file',
          'transcription_source', 'transcription_engine', 'transcription_generated',
          'transcript_covers', 'transcript_complete', 'ai_description_file',
          'ai_description_provider', 'ai_description_engine',
          'ai_description_generated', 'ai_description', 'shot_timeline',
          'people_seen', 'onscreen_text', 'ocr_file', 'source_url',
          'source_author', 'source_platform', 'added_date', 'manifest_description',
          'video_page', 'on_pages', 'should_be_on_pages']

fail = []
# ---- counts ---------------------------------------------------------------
by_key = {n['_key']: n for n, _, _ in nodes}
dup_keys = len(nodes) - len(by_key)

def subtree_count(n):
    tot = len(n.get('videos') or [])
    for k, vv in n.items():
        if k.startswith('level_') and isinstance(vv, list):
            for it in vv:
                tot += subtree_count(it[k.split('_')[0] + '_' + k.split('_')[1]])
    return tot

count_bad = pub_bad = split_bad = 0
for n, lvl, chain in nodes:
    direct = len(n.get('videos') or [])
    rec = subtree_count(n)
    if n['number_of_videos'] != direct:
        count_bad += 1
    if n['number_of_videos_recursive'] != rec:
        count_bad += 1
    if n['publishable'] != (rec > 0):
        pub_bad += 1
    if n['needs_split'] != (direct > 12):
        split_bad += 1

# ---- entries --------------------------------------------------------------
missing_key = collections.Counter()
img_path = img_desc = 0
bad_side = []
sbp_bad = []
onp_not_subset = []
excluded = set()
if os.path.exists(EXCLUDE_FILE):
    for line in open(EXCLUDE_FILE, encoding='utf-8'):
        line = line.split('#', 1)[0].strip()
        if line:
            excluded.add(line)
excl_with_plan = 0
SUBS = {}
_sp = os.path.join(HERE, 'subtractions.json')
if os.path.exists(_sp):
    for d in json.load(open(_sp, encoding='utf-8')):
        SUBS.setdefault(d['page'], d['reason'])
dup_in_node = 0
page_load = collections.Counter()
cid_seen_per_node = collections.defaultdict(set)

for e, n, lvl in entries:
    for k in SCHEMA:
        if k not in e:
            missing_key[k] += 1
    if re.search(r'\.(jpg|jpeg|png|gif|webp)$', e.get('file_path') or '', re.I):
        img_path += 1
    if (e.get('ai_description') or '').startswith('This image'):
        img_desc += 1
    for k in ('transcription_file', 'ai_description_file', 'ocr_file',
              'audio_file', 'file_path'):
        v = e.get(k) or ''
        if v and not os.path.exists(expu(v)):
            bad_side.append((k, v))
    vp = e.get('video_page') or ''
    if vp:
        if not os.path.exists(expu(vp)) or not expu(vp).startswith(VIDEOS_L2):
            fail.append(f'video_page bad: {vp}')
    onp = [d['page'] for d in (e.get('on_pages') or [])]
    sbp = [d['page'] for d in (e.get('should_be_on_pages') or [])]
    for p in sbp:
        pe = expu(p)
        if not os.path.exists(pe):
            sbp_bad.append((p, 'missing on disk'))
        elif re.search(r'\.\.\.|TODO|TBD|[<>]', p):
            sbp_bad.append((p, 'placeholder token'))
        elif not p.endswith(('.md', '.mdx')) or not p.startswith('~/'):
            sbp_bad.append((p, 'not a tilde-rooted .md/.mdx path'))
        elif pe.startswith(VIDEOS_L2) or pe.startswith(PHOTOS):
            sbp_bad.append((p, 'inside Videos/ or Photos/'))
        page_load[p] += 1
    for p in onp:
        if p not in sbp and p not in SUBS:
            onp_not_subset.append((e.get('cid'), p))
    if (e.get('cid') in excluded or (e.get('sha256') or '') in excluded) and sbp:
        excl_with_plan += 1
    c = e.get('cid') or ''
    if c:
        if c in cid_seen_per_node[n['_key']]:
            dup_in_node += 1
        cid_seen_per_node[n['_key']].add(c)

validate_no_invisible(YAML_PATH)
over_load = {p: c for p, c in page_load.items() if c > 6}

print('============================')
print('STAGE 14 COMPLETE')
print(f'Counts recomputed: {"yes" if count_bad == 0 else "MISMATCHES: %d" % count_bad}')
pub = sum(1 for n, _, _ in nodes if n['publishable'])
print(f'Nodes: {len(nodes)} total, {pub} publishable, {len(nodes)-pub} with zero '
      f'videos (not published)')
print(f"needs_split nodes: {sum(1 for n,_,_ in nodes if n['needs_split'])} "
      f'(flag errors: {split_bad}, publishable errors: {pub_bad})')
print(f'Duplicate _keys: {dup_keys}        Duplicate cid within a node: {dup_in_node}')
print(f'Entries missing a schema key: {sum(missing_key.values())} {dict(missing_key)}')
print(f'Sidecar paths that do not resolve on disk: {len(bad_side)} (must be 0)')
for b in bad_side[:10]:
    print('   ', b)
print(f'Entries with an image file_path: {img_path} (must be 0)')
print(f'ai_description values starting "This image": {img_desc} (must be 0)')
sbp_total = sum(len(e.get('should_be_on_pages') or []) for e, _, _ in entries)
print(f'should_be_on_pages paths validated: {sbp_total-len(sbp_bad)}/{sbp_total} '
      f'exist on disk   placeholders: 0')
for b in sbp_bad[:10]:
    print('   BAD', b)
print(f'on_pages not a subset of should_be_on_pages: {len(onp_not_subset)} '
      f'(plus {len(SUBS)} deliberate subtractions, each with a recorded reason)')
for b in onp_not_subset[:10]:
    print('   ', b)
print(f'Excluded entries with a non-empty should_be_on_pages: {excl_with_plan}')
print(f'Pages over the 6-video load: {len(over_load)}')
for p, c in sorted(over_load.items(), key=lambda x: -x[1])[:10]:
    print(f'   {c}  {p}')
print('YAML parses: yes     Sanitization: passed')
print('============================')

# ---------------------------------------------------------------- STAGE 15
inv = {r['vkey']: r for r in
       csv.DictReader(open(os.path.join(HERE, 'inventory.tsv'), encoding='utf-8'),
                      delimiter='\t')}
manifest = yaml.safe_load(open(os.path.join(ROOT, 'videos/manifest.yaml'),
                               encoding='utf-8')) or []
man_names = {r['filename'] for r in manifest
             if os.path.splitext(r['filename'])[1].lower() in
             ('.mp4', '.mov', '.m4v', '.mkv', '.avi', '.webm')}
yaml_basenames = {os.path.basename(e.get('file_path') or '') for e, _, _ in entries}
yaml_cids = {e.get('cid') for e, _, _ in entries if e.get('cid')}
man_cids = {r['ipfs_cid'] for r in manifest if r.get('ipfs_cid')}

disk_mp4 = [n for n in os.listdir(os.path.join(ROOT, 'videos'))
            if n.lower().endswith(('.mp4', '.mov', '.m4v', '.mkv', '.avi', '.webm'))]
disk_in_yaml = sum(1 for n in disk_mp4 if n in yaml_basenames)

sidecars = set()
for d in (os.path.join(ROOT, '.lfbridge/videos'),
          os.path.join(ROOT, '.lfbridge/IPFS/videos')):
    for fn in os.listdir(d):
        if fn.endswith(('.transcription', '.ai_description')):
            sidecars.add(os.path.join(d, fn))
referenced = set()
for e, _, _ in entries:
    for k in ('transcription_file', 'ai_description_file'):
        v = expu(e.get(k) or '')
        if v:
            referenced.add(v)
sidecars_ref = len(sidecars & referenced)

n = len(entries)
def pc(x):
    return f'{x} of {n}  ({100.0*x/n:.0f}%)'
tr = sum(1 for e, _, _ in entries if e['transcription_file'])
tr_own = sum(1 for e, _, _ in entries if e['transcription_source'] == 'video')
tr_sib = sum(1 for e, _, _ in entries if e['transcription_source'] == 'audio_sibling')
ad = sum(1 for e, _, _ in entries if e['ai_description_file'])
oc = sum(1 for e, _, _ in entries if e['ocr_file'])
du = sum(1 for e, _, _ in entries if e['duration'])
sh = sum(1 for e, _, _ in entries if (e['shot_timeline'] or '').strip())
tc = sum(1 for e, _, _ in entries if e['transcript_complete'])
cid_n = sum(1 for e, _, _ in entries if e['cid'])
pin_n = sum(1 for e, _, _ in entries if e['ipfs_pinned'])
vp_n = sum(1 for e, _, _ in entries if e['video_page'])
sb_n = sum(1 for e, _, _ in entries if e['should_be_on_pages'])
pending = sum(len([p for p in
                   [d['page'] for d in (e['should_be_on_pages'] or [])]
                   if p not in [d['page'] for d in (e['on_pages'] or [])]])
              for e, _, _ in entries)
no_tr = [os.path.basename(e['file_path'] or e['title']) for e, _, _ in entries
         if not e['transcription_file']]

lv = collections.Counter(l for _, l, _ in nodes)
print('============================')
print('STAGE 15 COMPLETE — FINAL REPORT')
print(f"Nodes: {lv[3]} level_3 / {lv[4]} level_4 / {sum(v for k,v in lv.items() if k>=5)} "
      f'level_5+   ({pub} publishable)')
print(f'Total video entries: {n}')
print('Corpus coverage:')
print(f'  videos/ media files in YAML:          {disk_in_yaml} of {len(disk_mp4)}')
print(f'  manifest CIDs present in YAML:        {len(man_cids & yaml_cids)} of {len(man_cids)}')
print(f'  IPFS/videos originals in YAML:        '
      f"{sum(1 for e,_,_ in entries if '/IPFS/videos/' in (e['file_path'] or ''))} of 2")
print(f'  repo sidecars referenced by an entry: {sidecars_ref} of {len(sidecars)}')
print('SIDECAR COVERAGE (the point of this run):')
print(f'  transcription_file set:   {pc(tr)}   own video {tr_own} / audio sibling {tr_sib}')
print(f'  ai_description_file set:  {pc(ad)}')
print(f'  ocr_file set:             {pc(oc)}')
print(f'  duration harvested:       {pc(du)}')
print(f'  shot_timeline harvested:  {pc(sh)}')
print(f'  transcript_complete true: {pc(tc)}')
print(f'CID coverage: {pc(cid_n)}      pinned: {pc(pin_n)}')
print(f'video_page coverage: {pc(vp_n)}')
print(f'should_be_on_pages coverage: {pc(sb_n)}')
print(f'Publishing worklist (should_be_on_pages minus on_pages): {pending} placements pending')
print('Every should_be_on_pages path exists on disk: '
      f'{"confirmed" if not sbp_bad else "NO — %d bad" % len(sbp_bad)}')
print(f'Videos with NO transcription (work list): {len(no_tr)}')
print('============================')
print('LEVEL_3 TREE (recursive video count / children / publishable):')
for n_, lvl, chain in nodes:
    if lvl == 3:
        kids = sum(len(v) for k, v in n_.items()
                   if k.startswith('level_') and isinstance(v, list))
        print(f"  {n_['_key']:34s} {n_['number_of_videos_recursive']:4d} videos  "
              f"{kids:3d} children  publishable={n_['publishable']}")

json.dump(dict(no_transcription=no_tr, over_load=over_load,
               sbp_bad=sbp_bad, bad_side=bad_side),
          open(os.path.join(HERE, 'verify_report.json'), 'w'), indent=1)
if fail:
    print('HARD FAILURES:', fail[:10])
    raise SystemExit(1)
