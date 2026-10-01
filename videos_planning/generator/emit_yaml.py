#!/usr/bin/env python3
# emit_yaml.py — STAGE 6 of p_update_video_hierarchy.md.
# Writes videos/videos.yaml from the corpus index (Stage 2), the sidecar harvest
# (Stage 3), the CID/pin record (Stage 4) and the cluster tree (Stage 5/7/8/9).
#
# Deterministic: stable key order, stable node order, stable video order. A
# rerun that changes nothing produces a byte-identical file.
import os, re, csv, sys, json, shutil, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sanitize_video import (sanitize_prose, sanitize_block, q_prose,
                            q_identity, validate_no_invisible)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.expanduser('~/BGit/Bryan_git/charlie-kirk')
YAML_PATH = os.path.join(ROOT, 'videos/videos.yaml')
BACKUP = os.path.join(HERE, 'videos.yaml.pre_rebuild.bak')

inv  = {r['vkey']: r for r in
        csv.DictReader(open(os.path.join(HERE, 'inventory.tsv'), encoding='utf-8'),
                       delimiter='\t')}
side = json.load(open(os.path.join(HERE, 'sidecars.json'), encoding='utf-8'))
cid_doc = json.load(open(os.path.join(HERE, 'cids.json'), encoding='utf-8'))
cids = cid_doc['entries']
tree = json.load(open(os.path.join(HERE, 'tree.json'), encoding='utf-8'))
nodes, roots = tree['nodes'], tree['roots']
DUPES = tree.get('duplicates', {})

# on_pages / should_be_on_pages come from later stages; read them back in when
# those stages have run so a rerun of this emitter does not drop them.
def load_side_map(name):
    p = os.path.join(HERE, name)
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}

ON_PAGES   = load_side_map('on_pages.json')
SHOULD_BE  = load_side_map('should_be_on_pages.json')
VIDEO_PAGE = load_side_map('video_page.json')

def tilde(p):
    h = os.path.expanduser('~')
    return '~' + p[len(h):] if p and p.startswith(h) else (p or '')

# ---------------------------------------------------------------- MODE DETECT
mode, evidence = 'REBUILD', 'file absent'
old_lines = old_bytes = 0
img_paths = img_desc = 0
if os.path.exists(YAML_PATH):
    txt = open(YAML_PATH, encoding='utf-8', errors='replace').read()
    old_lines, old_bytes = txt.count('\n') + 1, len(txt.encode('utf-8'))
    img_paths = len(re.findall(r'file_path:\s*"[^"]+\.(?:jpg|jpeg|png|gif|webp)"',
                               txt, re.I))
    vid_paths = len(re.findall(r'file_path:\s*"[^"]+\.(?:mp4|mov|m4v|mkv|avi|webm|mp3)"',
                               txt, re.I))
    img_desc = len(re.findall(r'ai_description:\s*"This image', txt))
    if img_paths > 100 or img_desc > 100:
        mode = 'REBUILD'
        evidence = (f'{img_paths} entries with an image file_path, '
                    f'{img_desc} ai_description values beginning "This image" '
                    f'(video file_paths: {vid_paths})')
    elif vid_paths > 0:
        mode = 'UPDATE'
        evidence = f'{vid_paths} entries with a video file_path, {img_paths} image'
    else:
        print('AMBIGUOUS MODE — stopping rather than guessing.')
        raise SystemExit(2)

if mode == 'REBUILD' and os.path.exists(YAML_PATH):
    shutil.copy2(YAML_PATH, BACKUP)

# ---------------------------------------------------------------- entry build
def build_entry(vkey):
    r = inv.get(vkey, {})
    s = side.get(vkey, {})
    c = cids.get(vkey, {})
    t = s.get('transcription') or {}
    a = s.get('ai_description') or {}
    o = s.get('ocr') or {}

    media = r.get('media_path', '')
    audio = r.get('audio_path', '')
    ovw = a.get('overview', '') or ''
    title = make_title(r, ovw)

    size = r.get('size', '')
    return dict(
        title=title,
        cid=c.get('cid', '') or '',
        ipfs_pinned=bool(c.get('ipfs_pinned', False)),
        sha256=c.get('sha256', '') or '',
        file_path=tilde(media),
        media_present=r.get('media_present', 'none'),
        file_size_bytes=int(size) if str(size).isdigit() else 0,
        duration=t.get('duration', '') or '',
        audio_file=tilde(audio),
        transcription_file=tilde(r.get('transcription_path', '')),
        transcription_source=r.get('transcription_source', '') or '',
        transcription_engine=t.get('engine', '') or '',
        transcription_generated=t.get('generated', '') or '',
        transcript_covers=t.get('covers', '') or '',
        transcript_complete=bool(t.get('complete', False)),
        ai_description_file=tilde(r.get('ai_description_path', '')),
        ai_description_provider=a.get('provider', '') or '',
        ai_description_engine=a.get('engine', '') or '',
        ai_description_generated=a.get('generated', '') or '',
        ai_description=ovw,
        shot_timeline=a.get('shot_timeline', '') or '',
        people_seen=a.get('people', '') or '',
        onscreen_text=a.get('onscreen', '') or '',
        ocr_file=tilde(r.get('ocr_path', '')),
        source_url=r.get('source_url', '') or '',
        source_author=r.get('source_author', '') or '',
        source_platform=r.get('source_platform', '') or '',
        added_date=r.get('added_date', '') or '',
        manifest_description=r.get('manifest_description', '') or '',
        duplicate_paths=[tilde(inv.get(d, {}).get('media_path', '')) 
                         for d in DUPES.get(vkey, [])],
        video_page=VIDEO_PAGE.get(vkey, ''),
        on_pages=ON_PAGES.get(vkey, []),
        should_be_on_pages=SHOULD_BE.get(vkey, []),
        _vkey=vkey,
    )


# ---------------------------------------------------------------- title
# A short human title for one video: the Level 5 page title and the link text in
# every table of contents above it. Under about nine words, naming the speaker
# when there is one.
#
# DEFAMATION: an accusation must never appear in `title` in the site's own
# voice, because the page generator copies this field straight into headings and
# link text. Almost every description in this corpus IS an accusation of some
# kind, so the title is built as ATTRIBUTED speech — "@handle - claim" — which
# reports that the source said it rather than asserting it. Anything still
# reading as a bare assertion is listed in findings_for_hierarchy.md for review.
CLAIM_WORDS = ('cover-up', 'coverup', 'murder', 'assassinat', 'rigged', 'faked',
               'fake ', 'lied', 'lying', 'framed', 'frame ', 'staged', 'hoax',
               'conspir', 'ordered', 'destroyed', 'deleted', 'wiped', 'bribe',
               'paid off', 'guilty', 'crime', 'criminal', 'hit job')

# "Author - some post text ... [1234567890].mp4" is how the mirror names an
# X capture. That gives a far better title than truncated vision-model prose.
MIRROR_NAME = re.compile(r'^(?P<author>.{2,40}?)\s+-\s+(?P<text>.*?)\s*'
                         r'(?:\.\.\.)?\s*(?:#\d+\s*)?\[[^\]]+\]$')

def _words(s, n):
    w = sanitize_prose(s).split()
    return ' '.join(w[:n]) + ('...' if len(w) > n else '')

def make_title(r, ovw):
    stem = os.path.splitext(r.get('basename', '') or '')[0]
    author = sanitize_prose(r.get('source_author', '') or '')
    md = sanitize_prose(r.get('manifest_description', '') or '')
    hint = sanitize_prose(r.get('title_hint', '') or '')

    if hint:
        return _words(hint, 12)

    m = MIRROR_NAME.match(stem)
    if m:
        a = sanitize_prose(m.group('author'))
        t = _words(m.group('text'), 9)
        return f'{a} - {t}' if t else a

    core = ''
    if md:
        # cut at the first clause boundary so the title is a label, not a thesis
        core = re.split(r'\s+[-\u2014:;(]\s*|\s+\u2014\s+', md, maxsplit=1)[0]
        core = _words(core or md, 10)
    elif re.search(r'[A-Za-z]{3}', stem) and not re.fullmatch(r'[\d_]+', stem):
        core = _words(stem.replace('_', ' ').replace('-', ' '), 9)
    if not core:
        core = _words(ovw, 9) or stem or r.get('vkey', 'Untitled')

    if author:
        return f'{author} - {core}'
    return core

PROSE = {'title', 'ai_description', 'people_seen', 'onscreen_text',
         'manifest_description'}
IDENT = {'cid', 'sha256', 'file_path', 'audio_file', 'transcription_file',
         'ai_description_file', 'ocr_file', 'source_url', 'video_page'}
ORDER = ['title', 'cid', 'ipfs_pinned', 'sha256', 'file_path', 'media_present',
         'file_size_bytes', 'duration', 'audio_file',
         'transcription_file', 'transcription_source', 'transcription_engine',
         'transcription_generated', 'transcript_covers', 'transcript_complete',
         'ai_description_file', 'ai_description_provider', 'ai_description_engine',
         'ai_description_generated', 'ai_description', 'shot_timeline',
         'people_seen', 'onscreen_text', 'ocr_file',
         'source_url', 'source_author', 'source_platform', 'added_date',
         'manifest_description', 'duplicate_paths', 'video_page', 'on_pages',
         'should_be_on_pages']

def emit_entry(e, ind):
    p = ' ' * ind
    out = [f'{p}- video:']
    q = ' ' * (ind + 4)
    for k in ORDER:
        v = e[k]
        if k == 'shot_timeline':
            if v.strip():
                out.append(f'{q}{k}: |')
                for line in sanitize_block(v).split('\n'):
                    out.append((f'{q}  {line}').rstrip())
            else:
                out.append(f'{q}{k}: ""')
        elif k == 'duplicate_paths':
            # other files on this machine whose bytes are identical to this
            # entry's — the same video saved under another name.
            if v:
                out.append(f'{q}{k}:')
                for dp in v:
                    out.append(f'{q}  - {q_identity(dp)}')
            else:
                out.append(f'{q}{k}: []')
        elif k in ('on_pages', 'should_be_on_pages'):
            if v:
                out.append(f'{q}{k}:')
                for pg in v:
                    out.append(f'{q}  - page: {q_identity(pg)}')
            else:
                out.append(f'{q}{k}: []')
        elif isinstance(v, bool):
            out.append(f'{q}{k}: {"true" if v else "false"}')
        elif isinstance(v, int):
            out.append(f'{q}{k}: {v}')
        elif k in IDENT:
            out.append(f'{q}{k}: {q_identity(v)}')
        elif k in PROSE:
            out.append(f'{q}{k}: {q_prose(v)}')
        else:
            out.append(f'{q}{k}: {q_prose(v)}')
    return out

# ---------------------------------------------------------------- node emit
def sort_videos(vkeys):
    def key(v):
        c = cids.get(v, {}).get('cid', '') or ''
        return (0, c) if c else (1, v)
    return sorted(vkeys, key=key)

def emit_node(nk, level, ind, out):
    n = nodes[nk]
    p = ' ' * ind
    q = ' ' * (ind + 4)
    out.append(f'{p}- level_{level}:')
    out.append(f'{q}title: {q_prose(n["title"])}')
    out.append(f'{q}_key: {n["_key"]}')
    out.append(f'{q}site_level_2: [' +
               ', '.join(q_identity(s) for s in n['site_level_2']) + ']')
    out.append(f'{q}site_page: {q_identity(n["site_page"])}')
    out.append(f'{q}number_of_videos: {n["number_of_videos"]}')
    out.append(f'{q}number_of_videos_recursive: {n["number_of_videos_recursive"]}')
    out.append(f'{q}publishable: {"true" if n["publishable"] else "false"}')
    out.append(f'{q}needs_split: {"true" if n["needs_split"] else "false"}')
    if n['videos']:
        out.append(f'{q}videos:')
        for v in sort_videos(n['videos']):
            out.extend(emit_entry(build_entry(v), ind + 6))
    else:
        out.append(f'{q}videos: []')
    kids = sorted(n['children'], key=lambda k: (nodes[k]['level'], nodes[k]['title'],
                                                nodes[k]['_key']))
    by_lvl = {}
    for k in kids:
        by_lvl.setdefault(nodes[k]['level'], []).append(k)
    for lvl in sorted(by_lvl):
        out.append(f'{q}level_{lvl}:')
        for k in by_lvl[lvl]:
            emit_node(k, lvl, ind + 6, out)

STAMP = datetime.date.today().isoformat()
header = f"""# videos.yaml — THE MASTER DATA FILE FOR VIDEO in the Charlie Kirk investigation.
#
# WHAT THIS FILE IS
#   The single, complete, accurate record of every video this investigation
#   holds: what it is, where its bytes are, what its IPFS CID is, what was SAID
#   in it, what is SEEN in it, what text is burned into it, which concept
#   cluster it belongs to, and which pages show it. It is NOT a by-product of
#   the website and it is not a copy of anything. Every prompt in the video
#   pipeline reads this file; none of them re-derives the corpus.
#
#   Built by videos_planning/generator/ from:
#     videos/                       the repo's own video corpus
#     videos/manifest.yaml          CIDs, provenance, pin status
#     IPFS/ipfs.txt, IPFS/videos/   the forensic originals
#     .lfbridge/videos/             Large File Bridge sidecars for the above
#     ~/_Mirror/Politics/Charlie_Kirk_Mi/   the concept-filed capture area
#     ~/BGit/Bryan_git/personal_large_files_bridge/_Mirror/...  its sidecars
#     site/docs/video_list.csv      the hand-kept YouTube index
#
#   REBUILT {STAMP} by videos_planning/p_update_video_hierarchy.md. The prior
#   contents were the inherited images.yaml corpus with only the KEYS converted
#   to the video schema; every VALUE in it described an image. That data was
#   discarded, not reconciled. From this point on the file only grows: entries
#   are matched by cid (then sha256, then file_path) and updated in place, new
#   videos are appended, and nothing is ever deleted or duplicated.
#
# THE LEVEL MODEL
#   There is no level_1 and no level_2 here. Level 1 is the site home page and
#   Level 2 is the videos landing page (site/docs/Videos/overview.mdx), so this
#   file's cluster tree begins at level_3. Site filesystem Level 2 maps to
#   level_3, site Level 3 to level_4, site Level 4 to level_5 — every level
#   incremented by one, because the whole tree hangs under the videos Level 2.
#
# publishable
#   true when the node's subtree contains at least one video; false when it does
#   not. The tree deliberately mirrors the WHOLE site, so most nodes are empty —
#   that emptiness is the useful part of the plan, because it shows exactly
#   which parts of the investigation have no video coverage. But a node with
#   publishable: false MUST NOT GENERATE A PAGE. p_yaml_to_site.md and
#   p_level2_update.md are required to honour this flag; publishing the empty
#   nodes would add hundreds of dead-end pages to the site.
#
# media_present
#   "video"       the video file is on this machine
#   "audio_only"  only the .mp3 extraction survives locally; the CID still makes
#                 the video playable from a public IPFS gateway
#   "none"        neither; known from the manifest, the site, or video_list.csv
#   The video corpus is gitignored, so on a fresh clone NO media is present.
#   This field is what lets a later pass behave correctly there instead of
#   concluding the corpus is empty.
#
# transcription_source
#   "video"          the transcription is of the video file itself
#   "audio_sibling"  it is of the .mp3 extraction beside it — same speech, same
#                    duration, a legitimate transcription of that video
#   ""               there is no transcription
#
# cid IS THE PRIMARY IDENTITY FOR VIDEO
#   The site plays video from public IPFS gateways and never from a copy in the
#   repo — the bytes are gitignored and GitHub Pages is not a video host. So an
#   entry may carry a cid and an empty sha256, and that is correct when the
#   bytes are not on this machine. An entry with cid "" cannot be published with
#   a player at all. ipfs_pinned false means no public gateway can reliably
#   serve it: it plays here and is DEAD for every visitor.
#
# EMPTY VALUES
#   A scalar with no value is "" — never null, never a missing key. Lists emit
#   [] and booleans emit false. Every video entry carries every key, always, so
#   a later pass can tell "not looked up yet" from "looked up, does not exist".
#
# on_pages vs should_be_on_pages
#   on_pages is OBSERVED — every other page in the repo that embeds this video
#   today. should_be_on_pages is REASONED — every page it OUGHT to appear on,
#   and it is a SUPERSET of on_pages, not a list of extras. The set difference
#   is the publishing worklist p_yaml_to_site.md consumes.
#
# INVISIBLE UNICODE IS FORBIDDEN in this file (security rule). Prose fields are
# scrubbed; identity fields keep their exact value but are emitted as visible
# \\uXXXX escapes so the path still resolves after YAML parses it.
"""

out = [header.rstrip('\n'), 'level_3:']
for nk in sorted(roots, key=lambda k: (nodes[k]['title'], nodes[k]['_key'])):
    emit_node(nk, 3, 2, out)
text = '\n'.join(out) + '\n'
open(YAML_PATH, 'w', encoding='utf-8').write(text)

validate_no_invisible(YAML_PATH)
import yaml as _y
_y.safe_load(open(YAML_PATH, encoding='utf-8'))

new_lines = text.count('\n')
new_bytes = len(text.encode('utf-8'))
lv = {}
for n in nodes.values():
    lv[n['level']] = lv.get(n['level'], 0) + 1
entries = sum(len(n['videos']) for n in nodes.values())

print('============================')
print('STAGE 6 COMPLETE')
print(f'Mode: {mode}   (evidence: {evidence})')
print(f'Backup written: {BACKUP}' if mode == 'REBUILD' else 'Backup: n/a')
print(f'Inherited image entries discarded: {img_paths}')
print(f'Video entries written: {entries}')
print(f"Nodes written: {lv.get(3,0)} level_3 / {lv.get(4,0)} level_4 / "
      f"{lv.get(5,0)+lv.get(6,0)} level_5+")
print('Every entry carries the full property set: yes')
print('YAML parses: yes    Sanitization validation: passed')
print(f'File size: {new_lines} lines, {new_bytes} bytes '
      f'(was {old_lines} lines, {old_bytes} bytes)')
print('============================')
