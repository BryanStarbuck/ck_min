#!/usr/bin/env python3
# set_next_video.py — STAGE 2 of videos_planning/p_next_buttons.md.
#
# Writes the next_video property into videos/videos.yaml. next_video is the
# ~-rooted video_page path of the clip that comes NEXT in one global document
# pre-order walk of the whole hierarchy — a node's own videos before its child
# clusters, children in YAML order. The chain LOOPS: the last video's next_video
# is the first video's page, so the walk never dead-ends.
#
# THE PAGE MAPPING IS THE GENERATOR'S, NOT video_page. gen_videos_pages.py mints
# each published Level 5 page path itself and records the whole S sequence, in
# document order, in generated_pages.json. That manifest is the authority here.
# (The YAML's own video_page field is a downstream copy that a bind/emit pass
# repopulates separately; it is currently unpopulated, so this prompt does not
# depend on it. The drift is reported in findings_for_hierarchy.md.)
#
# THE EDIT IS SURGICAL. Only next_video lines are added, changed, or removed;
# every other byte of videos.yaml is preserved. A full re-serialize would reflow
# the 357 shot_timeline block scalars, so instead each existing next_video line
# is dropped and a fresh one is emitted immediately after that entry's
# video_page line. Idempotent: an unchanged value round-trips byte-for-byte.
#
# Membership of S: a video is in S iff it has a published page in the manifest.
# A banned video, or one whose page was never written, is absent from the
# manifest, so it gets no next_video (its cross-filed duplicate blocks are
# stripped too — only the first document-order occurrence of a CID is an S node).
import os, re, sys, json, yaml
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sanitize_video import q_identity, validate_no_invisible

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.expanduser('~/BGit/Bryan_git/charlie-kirk')
YAML_PATH = os.path.join(ROOT, 'videos/videos.yaml')
MANIFEST = os.path.join(HERE, 'generated_pages.json')


def tilde(p):
    h = os.path.expanduser('~')
    return '~' + p[len(h):] if p and p.startswith(h) else (p or '')


def decode(tok):
    """Decode a YAML double-quoted identity token to its literal value."""
    tok = (tok or '').strip()
    if not tok:
        return ''
    try:
        v = yaml.safe_load(tok)
        return v if isinstance(v, str) else (tok.strip('"') if tok else '')
    except Exception:
        return tok.strip('"')


vids = json.load(open(MANIFEST, encoding='utf-8'))['videos']
N = len(vids)
if N == 0:
    print('set_next_video.py: manifest is empty — nothing to do.')
    raise SystemExit(1)

# successor map, keyed by identity (cid preferred, sha256, then file_path).
# file_path is a last resort used ONLY for the rare entry that carries neither a
# cid nor a sha256 (an audio-only extraction), so it can never mis-bind an entry
# that a stronger identity already matched.
def _rp(p):
    return os.path.realpath(os.path.expanduser(p)) if p else ''

next_by_cid, next_by_sha, next_by_path = {}, {}, {}
for i, v in enumerate(vids):
    nxt = tilde(vids[(i + 1) % N]['page'])
    cid = (v.get('cid') or '').strip()
    sha = (v.get('sha256') or '').strip().lower()
    fp = (v.get('file_path') or '').strip()
    if cid:
        next_by_cid[cid] = nxt
    elif sha:
        next_by_sha[sha] = nxt
    elif fp:
        next_by_path[_rp(fp)] = nxt

VID_RE = re.compile(r'^(\s*)-\s+video:\s*$')
CID_RE = re.compile(r'^\s*cid:\s*(.*)$')
SHA_RE = re.compile(r'^\s*sha256:\s*(.*)$')
FP_RE = re.compile(r'^\s*file_path:\s*(.*)$')
VP_RE = re.compile(r'^(\s*)video_page:\s*(.*)$')
NV_RE = re.compile(r'^\s*next_video:\s*(.*)$')

text = open(YAML_PATH, encoding='utf-8').read()
ends_nl = text.endswith('\n')
lines = text.split('\n')

out = []
in_video = False
cur_cid = cur_sha = cur_fp = ''
used = set()
added = removed = 0
old_values = {}   # (line index in original) not needed; track changed count
new_pages = set()

for ln in lines:
    m = VID_RE.match(ln)
    if m:
        in_video = True
        cur_cid = cur_sha = cur_fp = ''
        out.append(ln)
        continue
    if NV_RE.match(ln):
        removed += 1           # drop every existing next_video; re-emit fresh
        continue
    if in_video and cur_cid == '':
        mc = CID_RE.match(ln)
        if mc:
            cur_cid = decode(mc.group(1))
            out.append(ln)
            continue
    if in_video and cur_sha == '':
        ms = SHA_RE.match(ln)
        if ms:
            cur_sha = decode(ms.group(1))
            out.append(ln)
            continue
    if in_video and cur_fp == '':
        mf = FP_RE.match(ln)
        if mf:
            cur_fp = decode(mf.group(1))
            out.append(ln)
            continue
    mv = VP_RE.match(ln)
    if in_video and mv:
        out.append(ln)
        indent = mv.group(1)
        cid = (cur_cid or '').strip()
        sha = (cur_sha or '').strip().lower()
        fp = _rp(cur_fp) if cur_fp else ''
        nxt = None
        if cid and cid in next_by_cid and cid not in used:
            nxt = next_by_cid[cid]
            used.add(cid)
        elif not cid and sha and sha in next_by_sha and ('sha:' + sha) not in used:
            nxt = next_by_sha[sha]
            used.add('sha:' + sha)
        elif not cid and not sha and fp and fp in next_by_path and ('fp:' + fp) not in used:
            nxt = next_by_path[fp]
            used.add('fp:' + fp)
        if nxt:
            out.append(f'{indent}next_video: {q_identity(nxt)}')
            added += 1
            new_pages.add(nxt)
        in_video = False       # video_page is the last field we act on
        continue
    out.append(ln)

new_text = '\n'.join(out)
if ends_nl and not new_text.endswith('\n'):
    new_text += '\n'

open(YAML_PATH, 'w', encoding='utf-8').write(new_text)

# validate: still parses, no invisible unicode, diff confined to next_video
reparsed = yaml.safe_load(open(YAML_PATH, encoding='utf-8'))
validate_no_invisible(YAML_PATH)

old_lines = text.split('\n')
new_lines = new_text.split('\n')
# byte-diff confinement check: every differing line is a next_video line
import difflib
diff_nonnv = 0
for d in difflib.unified_diff(old_lines, new_lines, lineterm=''):
    if d[:2] in ('++', '--', '@@'):
        continue
    if d and d[0] in '+-' and 'next_video:' not in d:
        diff_nonnv += 1

# integrity: does the chain form a single cycle over the manifest pages?
first = tilde(vids[0]['page'])
by_page = {}
for i, v in enumerate(vids):
    by_page[tilde(v['page'])] = tilde(vids[(i + 1) % N]['page'])
seen, cur, steps = set(), first, 0
while cur and cur not in seen:
    seen.add(cur)
    cur = by_page.get(cur)
    steps += 1
cycle_ok = (steps == N and cur == first)

print('=' * 28)
print('set_next_video.py COMPLETE (Stage 2)')
print(f'Manifest S videos: {N}')
print(f'next_video written: {added}   old next_video lines removed: {removed}')
print(f'Non-next_video lines changed in diff: {diff_nonnv}  (must be 0)')
print(f'YAML re-parses: {"yes" if reparsed else "no"}   invisible-unicode: clean')
print(f'Single cycle length {steps} over {N} pages, wraps last->first: {cycle_ok}')
print(f'Wrap: {os.path.basename(tilde(vids[-1]["page"]))} -> {os.path.basename(first)}')
print('=' * 28)
