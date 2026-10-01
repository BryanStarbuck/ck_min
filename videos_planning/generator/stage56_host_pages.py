#!/usr/bin/env python3
# stage56_host_pages.py — Stages 5 and 6 of p_yaml_to_site.md.
#
# STAGE 5  every video embed already sitting on a topic page gets a text link
#          beneath it pointing at that video's own page under /Videos. A <video>
#          or <iframe> is NEVER wrapped in an anchor (the click hits the
#          controls); a real <img> thumbnail standing in for a video is.
# STAGE 6  every video the YAML says BELONGS on a topic page and is not already
#          there gets a CARD in a regenerated CK_PLACED_VIDEOS block at the
#          bottom of that page. A card, never a player.
#
# ADDITIVE ONLY. Outside our own markers and the one added link line, every host
# page stays byte-identical — every image, caption and CK_PLACED_IMAGES block
# that was there before the run is there after it.
import os, re, sys, json, subprocess, csv

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sanitize_video import sanitize_prose, validate_no_invisible

HERE     = os.path.dirname(os.path.abspath(__file__))
ROOT     = os.path.expanduser('~/BGit/Bryan_git/charlie-kirk')
DOCS     = os.path.join(ROOT, 'site', 'docs')
L2DIR    = os.path.join(DOCS, 'Videos')
PHOTOS   = os.path.join(DOCS, 'Photos')
PAGESCSV = os.path.join(ROOT, 'pages.csv')
GEN      = os.path.join(HERE, 'generated_pages.json')
IPFS     = '/opt/homebrew/bin/ipfs'
CAP      = 6

# The ban set is re-checked here against the identity, never inherited on trust
# from whatever wrote generated_pages.json. Union of ban_videos.csv (master) and
# exclude_videos.txt (older list); a CSV row with banned=false is an un-ban.
BANCSV  = os.path.join(ROOT, 'videos', 'ban_videos.csv')
EXCLUDE = os.path.join(ROOT, 'videos_planning', 'exclude_videos.txt')
banned, unbanned = set(), set()
if os.path.exists(EXCLUDE):
    for line in open(EXCLUDE, encoding='utf-8'):
        line = line.split('#')[0].strip()
        if line:
            banned.add(line)
if os.path.exists(BANCSV):
    for row in csv.DictReader(open(BANCSV, encoding='utf-8')):
        ids = [str(row.get(k) or '').strip() for k in ('sha256', 'cid', 'file_path')]
        ids = [i for i in ids if i]
        if not ids:
            continue
        (unbanned if str(row.get('banned') or '').strip().lower() == 'false' else banned).update(ids)
banned -= unbanned

G = json.load(open(GEN, encoding='utf-8'))
VIDS = [v for v in G['videos']
        if not any((v.get(k) or '').strip() in banned for k in ('cid', 'sha256', 'file_path'))]
BANNED_N = len(G['videos']) - len(VIDS)

url_by_file = {}
for row in csv.DictReader(open(PAGESCSV, encoding='utf-8')):
    fp = row.get('file_path') or ''
    if fp:
        url_by_file[os.path.join(ROOT, fp)] = row.get('url_path') or ''

B32 = {}
def base32(cid):
    if not cid:
        return ''
    if cid not in B32:
        try:
            p = subprocess.run([IPFS, 'cid', 'base32', cid], capture_output=True, text=True, timeout=20)
            B32[cid] = p.stdout.strip() if p.returncode == 0 else ''
        except Exception:
            B32[cid] = ''
    return B32[cid]

def mdx_safe(s):
    return (s or '').replace('<', '&lt;').replace('{', '&#123;').replace('}', '&#125;')

def norm_page(p):
    p = os.path.expanduser(str(p or '').strip())
    if not p:
        return ''
    if not os.path.isabs(p):
        p = os.path.join(ROOT, p)
    return os.path.normpath(p)

def video_url(v):
    return url_by_file.get(v['page']) or v['url']

def dur_human(d):
    m = re.match(r'^(\d+):(\d+):(\d+)$', (d or '').strip())
    if not m:
        return ''
    h, mi, s = (int(x) for x in m.groups())
    return (f'{h}:{mi:02d}:{s:02d}' if h else f'{mi}:{s:02d}')

def first_sentence(s, limit=170):
    s = sanitize_prose(s or '')
    out = re.split(r'(?<=[.!?])\s+', s)[0].strip()
    if len(out) > limit:
        out = out[:limit].rsplit(' ', 1)[0].rstrip(' ,;:-') + '…'
    return mdx_safe(out)

# ----------------------------------------------------------------- STAGE 5
LINK_RE = re.compile(r'Full write-up and sources for this video')
stage5 = {}
for v in VIDS:
    for p in v.get('on_pages') or []:
        fp = norm_page(p)
        if not fp or not fp.startswith(DOCS) or not os.path.exists(fp):
            continue
        if fp.startswith(L2DIR + os.sep) or fp == L2DIR or fp.startswith(PHOTOS + os.sep):
            continue
        stage5.setdefault(fp, [])
        if v not in stage5[fp]:
            stage5[fp].append(v)

s5_pages = s5_links = s5_already = 0
s5_nomatch = []
for fp, vids in sorted(stage5.items()):
    txt = orig = open(fp, encoding='utf-8').read()
    for v in vids:
        cid, b32 = v['cid'], base32(v['cid'])
        url = video_url(v)
        needles = [n for n in (cid, b32) if n]
        stem = os.path.splitext(os.path.basename(os.path.expanduser(v['file_path'] or '')))[0]
        hit = None
        for nd in needles:
            for m in re.finditer(re.escape(nd), txt):
                hit = m
                break
            if hit:
                break
        if hit is None and stem and len(stem) > 8 and txt.count(stem) == 1:
            hit = re.search(re.escape(stem), txt)
        if hit is None:
            s5_nomatch.append((os.path.relpath(fp, ROOT), v['key']))
            continue
        # find the end of the element the match sits inside
        tail = txt[hit.end():]
        close = None
        for pat in (r'</video>', r'</iframe>', r'/>', r'\)\s*$'):
            m2 = re.search(pat, tail, re.M)
            if m2 and (close is None or m2.end() < close):
                close = m2.end()
        if close is None:
            s5_nomatch.append((os.path.relpath(fp, ROOT), v['key']))
            continue
        insert_at = hit.end() + close
        after = txt[insert_at:insert_at + 400]
        if LINK_RE.search(after) or url in after:
            s5_already += 1
            continue
        line = f'\n\n<p><a href="{url}">Full write-up and sources for this video →</a></p>\n'
        txt = txt[:insert_at] + line + txt[insert_at:]
        s5_links += 1
    if txt != orig:
        open(fp, 'w', encoding='utf-8').write(txt)
        validate_no_invisible(fp)
        s5_pages += 1

# ----------------------------------------------------------------- STAGE 6
START = '{/* CK_PLACED_VIDEOS_START — generated, do not hand-edit */}'
END   = '{/* CK_PLACED_VIDEOS_END */}'
BLOCK_RE = re.compile(re.escape('{/* CK_PLACED_VIDEOS_START') + r'.*?' + re.escape(END), re.S)
IMG_BLOCK_RE = re.compile(re.escape('{/* CK_PLACED_IMAGES_START') + r'.*?' +
                          re.escape('{/* CK_PLACED_IMAGES_END */}'), re.S)

plan = {}
no_page, gone = [], []
for v in VIDS:
    if not v.get('should_be_on_pages'):
        continue
    if not v.get('page') or not os.path.exists(v['page']):
        no_page.append(v['key'])
        continue
    for p in v['should_be_on_pages']:
        fp = norm_page(p)
        if not fp or not os.path.exists(fp):
            gone.append((v['key'], str(p)))
            continue
        if not fp.startswith(DOCS) or fp.startswith(L2DIR + os.sep) or fp == L2DIR \
           or fp.startswith(PHOTOS + os.sep):
            gone.append((v['key'], str(p)))
            continue
        plan.setdefault(fp, [])
        if v not in plan[fp]:
            plan[fp].append(v)

s6_created = s6_replaced = s6_removed = s6_cards = s6_dupe = 0
s6_overflow, s6_img_touched = [], []
pending_cards = 0
for fp, vids in sorted(plan.items()):
    orig = open(fp, encoding='utf-8').read()
    img_before = IMG_BLOCK_RE.search(orig)
    stripped = BLOCK_RE.sub('', orig)
    keep = []
    for v in vids:
        ids = [x for x in (v['cid'], base32(v['cid']), v['sha256']) if x]
        if any(i in stripped for i in ids):
            s6_dupe += 1
            continue
        keep.append(v)
    already = len(vids) - len(keep)
    room = max(0, CAP - already)
    if len(keep) > room:
        s6_overflow.append((os.path.relpath(fp, ROOT), len(keep) - room))
        keep = keep[:room]

    if not keep:
        if BLOCK_RE.search(orig):
            new = BLOCK_RE.sub('', orig).rstrip() + '\n'
            open(fp, 'w', encoding='utf-8').write(new)
            s6_removed += 1
        continue

    cards = [START, '', '## Videos', '',
             'Footage related to this page. Each card opens that clip\'s own page, '
             'with the video, the full write-up, and its source.', '',
             '<div className="ck-placed-videos">', '']
    for v in keep:
        url = video_url(v)
        title = mdx_safe(sanitize_prose(v['title']))
        cap = first_sentence(v.get('caption') or '')
        if not cap or cap.strip() == title.strip():
            cap = ''
        meta = []
        d = dur_human(v.get('duration'))
        if d:
            meta.append(d)
        if v.get('source_author'):
            meta.append(mdx_safe(sanitize_prose(v['source_author'])))
        elif v.get('source_platform') and v['source_platform'] != 'local':
            meta.append(v['source_platform'])
        if v['mode'] != 'ipfs':
            meta.append('media pending')
            pending_cards += 1
        alt = title.replace('"', "'")
        cards.append(f'<div className="ck-placed-video" data-cid="{v["cid"]}">')
        if v.get('poster'):
            cards.append(f'  <a href="{url}"><img src="{v["poster"]}" alt="{alt}" loading="lazy" /></a>')
        cards.append('  <div className="ck-placed-video-body">')
        cards.append(f'    <a className="ck-placed-video-title" href="{url}">{title}</a>')
        if cap:
            cards.append(f'    <span className="ck-placed-video-caption">{cap}</span>')
        if meta:
            cards.append(f'    <div className="ck-placed-video-meta">{" · ".join(meta)}</div>')
        cards.append('  </div>')
        cards.append('</div>')
        s6_cards += 1
    cards += ['', '</div>', '', END]
    block = '\n'.join(cards)
    if BLOCK_RE.search(orig):
        new = BLOCK_RE.sub(lambda _: block, orig, count=1)
        s6_replaced += 1
    else:
        new = orig.rstrip() + '\n\n' + block + '\n'
        s6_created += 1
    open(fp, 'w', encoding='utf-8').write(new)
    validate_no_invisible(fp)
    img_after = IMG_BLOCK_RE.search(open(fp, encoding='utf-8').read())
    a = img_before.group(0) if img_before else None
    b = img_after.group(0) if img_after else None
    if a != b:
        s6_img_touched.append(os.path.relpath(fp, ROOT))

print('=' * 60)
print(f'Ban set: {len(banned)} identifiers   videos withheld from both stages: {BANNED_N}')
print('STAGE 5 COMPLETE')
print(f'Host pages scanned: {len(stage5)}   host pages edited: {s5_pages}')
print(f'Video embeds linked: {s5_links}   already linked (skipped): {s5_already}')
print(f'Claimed hosts with no matching embed: {len(s5_nomatch)}')
for x in s5_nomatch[:15]:
    print('   ', x)
print('=' * 60)
print('STAGE 6 COMPLETE')
print(f'Videos with should_be_on_pages: {len([v for v in VIDS if v.get("should_be_on_pages")])}'
      f'   placements planned over {len(plan)} pages')
print(f'Pages edited: {s6_created + s6_replaced}   blocks created: {s6_created}   '
      f'blocks replaced: {s6_replaced}   blocks removed: {s6_removed}')
print(f'Videos placed: {s6_cards}   skipped as already embedded: {s6_dupe}')
print(f'Cards whose video has no playable cid (link works, media pending): {pending_cards}')
print(f'Over the {CAP}-per-page cap: {len(s6_overflow)}')
for x in s6_overflow[:15]:
    print('   ', x)
print(f'Missing video_page: {len(no_page)}   should_be paths that no longer resolve: {len(gone)}')
print(f'CK_PLACED_IMAGES blocks touched: {len(s6_img_touched)} {s6_img_touched[:5]}')
print('=' * 60)
