#!/usr/bin/env python3
# build_inventory.py — STAGE 2 of p_update_video_hierarchy.md.
# Builds one flat index of every video this investigation holds, from every
# source, and writes it to generator/inventory.tsv. Ground truth for Stages 3-6.
# Reads only; writes nothing but the TSV.
import os, re, csv, sys, yaml, json

ROOT        = os.path.expanduser('~/BGit/Bryan_git/charlie-kirk')
VIDEOS_DIR  = os.path.join(ROOT, 'videos')
IPFS_DIR    = os.path.join(ROOT, 'IPFS')
IPFS_VIDEOS = os.path.join(IPFS_DIR, 'videos')
MANIFEST    = os.path.join(VIDEOS_DIR, 'manifest.yaml')
IPFS_TXT    = os.path.join(IPFS_DIR, 'ipfs.txt')
LFB         = os.path.join(ROOT, '.lfbridge')
LFB_VIDEOS  = os.path.join(LFB, 'videos')
LFB_IPFS    = os.path.join(LFB, 'IPFS', 'videos')
MIRROR      = os.path.expanduser('~/_Mirror/Politics/Charlie_Kirk_Mi')
MIRROR_SC   = os.path.expanduser('~/BGit/Bryan_git/personal_large_files_bridge/_Mirror/Politics/Charlie_Kirk_Mi')
MIRROR_LEG  = os.path.expanduser('~/BGit/Bryan_git/personal_large_files_bridge/.lfbridge/_Mirror/Politics/Charlie_Kirk_Mi')
VIDEO_CSV   = os.path.join(ROOT, 'site/docs/video_list.csv')
OUT         = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inventory.tsv')

VIDEO_EXT = {'.mp4', '.mov', '.m4v', '.mkv', '.avi', '.webm'}
AUDIO_EXT = {'.mp3', '.wav', '.m4a', '.aac', '.flac', '.ogg'}

def tilde(p):
    h = os.path.expanduser('~')
    return '~' + p[len(h):] if p.startswith(h) else p

def sidecar_for(media_abs, kind, sc_root, media_root):
    """Resolve a sidecar path per the LFB placement rule. Returns abs path or ''."""
    rel = os.path.relpath(media_abs, media_root)
    cand = os.path.join(sc_root, rel) + '.' + kind
    if os.path.exists(cand):
        return cand
    return ''

rows = {}   # vkey -> dict

def blank(vkey):
    return dict(vkey=vkey, basename='', media_path='', media_present='none', size='',
                mtime='', audio_path='', transcription_path='', transcription_source='',
                ai_description_path='', ocr_path='', manifest_cid='', manifest_pinned='',
                source_url='', source_author='', added_date='', manifest_description='',
                source_platform='', origin='', mirror_dir='', title_hint='')

# ---------------------------------------------------------------- 1. videos/
disk_video, disk_audio = {}, {}
for n in sorted(os.listdir(VIDEOS_DIR)):
    p = os.path.join(VIDEOS_DIR, n)
    if not os.path.isfile(p):
        continue
    stem, ext = os.path.splitext(n)
    if ext.lower() in VIDEO_EXT:
        disk_video[stem] = p
    elif ext.lower() in AUDIO_EXT:
        disk_audio[stem] = p

for stem, p in disk_video.items():
    r = blank(stem)
    st = os.stat(p)
    r.update(basename=os.path.basename(p), media_path=p, media_present='video',
             size=str(st.st_size), mtime=str(int(st.st_mtime)), origin='videos_dir',
             source_platform='x')
    if stem in disk_audio:
        r['audio_path'] = disk_audio[stem]
    rows[stem] = r

# ---------------------------------------------------------------- 2. manifest
manifest = yaml.safe_load(open(MANIFEST, encoding='utf-8')) or []
manifest_only, manifest_names = [], set()
for rec in manifest:
    fn = rec.get('filename', '')
    stem, ext = os.path.splitext(fn)
    if ext.lower() not in VIDEO_EXT:
        continue
    manifest_names.add(fn)
    r = rows.get(stem)
    if r is None:
        r = blank(stem)
        r.update(basename=fn, origin='manifest_only', source_platform='x')
        # the .mp4 is gone; is there an .mp3 survivor?
        if stem in disk_audio:
            r.update(media_present='audio_only', audio_path=disk_audio[stem],
                     media_path=disk_audio[stem])
            st = os.stat(disk_audio[stem]); r['size'] = str(st.st_size)
        else:
            r['media_present'] = 'none'
        rows[stem] = r
        manifest_only.append(fn)
    r.update(manifest_cid=rec.get('ipfs_cid', '') or '',
             manifest_pinned=str(bool(rec.get('pinned', False))).lower(),
             source_url=rec.get('source_url', '') or '',
             source_author=rec.get('source_author', '') or '',
             added_date=str(rec.get('added_date', '') or ''),
             manifest_description=(rec.get('description', '') or '').replace('\t', ' '))

# ---------------------------------------------------------------- 3. IPFS/
ipfs_txt_cid = {}    # filename -> (cid, comment)
if os.path.exists(IPFS_TXT):
    txt = open(IPFS_TXT, encoding='utf-8').read().split('\n')
    cur_cid, cur_comment = '', ''
    for i, line in enumerate(txt):
        m = re.match(r'^ipfs get (\S+)\s*$', line)
        if m:
            cur_cid = m.group(1)
            cur_comment = ''
            for j in range(i - 1, max(-1, i - 4), -1):
                if txt[j].startswith('#'):
                    cur_comment = txt[j].lstrip('# ').strip()
            continue
        m = re.match(r'^ipfs add "(.+)"\s*$', line)
        if m and cur_cid:
            ipfs_txt_cid[m.group(1)] = (cur_cid, cur_comment)

if os.path.isdir(IPFS_VIDEOS):
    for n in sorted(os.listdir(IPFS_VIDEOS)):
        p = os.path.join(IPFS_VIDEOS, n)
        if not os.path.isfile(p) or os.path.splitext(n)[1].lower() not in VIDEO_EXT:
            continue
        vkey = 'IPFS/' + os.path.splitext(n)[0]
        r = blank(vkey)
        st = os.stat(p)
        r.update(basename=n, media_path=p, media_present='video', size=str(st.st_size),
                 mtime=str(int(st.st_mtime)), origin='ipfs_dir', source_platform='ipfs')
        cid, comment = ipfs_txt_cid.get(n, ('', ''))
        # ipfs.txt may name it with a different path form
        if not cid:
            for k, v in ipfs_txt_cid.items():
                if os.path.basename(k) == n:
                    cid, comment = v
                    break
        r.update(manifest_cid=cid, manifest_description=comment.replace('\t', ' '))
        rows[vkey] = r

# ---------------------------------------------------------------- 4. sidecars
# A sidecar proves a video existed even when the media file is gone.
def scan_sidecar_dir(sc_dir, media_root, origin, key_prefix=''):
    found = {}
    if not os.path.isdir(sc_dir):
        return found
    for dirpath, _, filenames in os.walk(sc_dir):
        for fn in filenames:
            for kind in ('transcription', 'ai_description', 'ocr'):
                suf = '.' + kind
                if not fn.endswith(suf):
                    continue
                media_name = fn[:-len(suf)]
                stem, ext = os.path.splitext(media_name)
                if ext.lower() not in VIDEO_EXT | AUDIO_EXT:
                    continue
                rel_dir = os.path.relpath(dirpath, sc_dir)
                relkey = stem if rel_dir == '.' else os.path.join(rel_dir, stem)
                vkey = key_prefix + relkey
                found.setdefault(vkey, {})[(kind, ext.lower())] = os.path.join(dirpath, fn)
    return found

repo_sc  = scan_sidecar_dir(LFB_VIDEOS, VIDEOS_DIR, 'videos_dir')
ipfs_sc  = scan_sidecar_dir(LFB_IPFS,   IPFS_VIDEOS, 'ipfs_dir', 'IPFS/')

def attach_sidecars(sc_map, default_origin, media_root, audio_lookup):
    for vkey, kinds in sc_map.items():
        r = rows.get(vkey)
        if r is None:
            r = blank(vkey)
            stem = vkey.split('/')[-1]
            r.update(basename=stem, origin='sidecar_only', source_platform='x')
            # audio-only survivor?
            if stem in audio_lookup:
                r.update(media_present='audio_only', audio_path=audio_lookup[stem],
                         media_path=audio_lookup[stem])
                r['size'] = str(os.stat(audio_lookup[stem]).st_size)
            rows[vkey] = r
        # video's own sidecars first, audio sibling as fallback for transcription
        for kind in ('transcription', 'ai_description', 'ocr'):
            vid = next((p for (k, e), p in kinds.items()
                        if k == kind and e in VIDEO_EXT), '')
            aud = next((p for (k, e), p in kinds.items()
                        if k == kind and e in AUDIO_EXT), '')
            col = kind + ('_path' if kind != 'ai_description' else '_path')
            col = {'transcription': 'transcription_path',
                   'ai_description': 'ai_description_path',
                   'ocr': 'ocr_path'}[kind]
            if vid:
                r[col] = vid
                if kind == 'transcription':
                    r['transcription_source'] = 'video'
            elif aud and kind == 'transcription':
                r[col] = aud
                r['transcription_source'] = 'audio_sibling'
            elif aud and kind != 'transcription':
                # audio has no ai_description/ocr in practice; ignore
                pass

attach_sidecars(repo_sc, 'videos_dir', VIDEOS_DIR, disk_audio)
attach_sidecars(ipfs_sc, 'ipfs_dir', IPFS_VIDEOS, {})

# ---------------------------------------------------------------- 5. mirror
mirror_videos = []
for dirpath, dirnames, filenames in os.walk(MIRROR):
    dirnames[:] = [d for d in dirnames if not d.startswith('.')]
    for fn in filenames:
        if os.path.splitext(fn)[1].lower() in VIDEO_EXT:
            mirror_videos.append(os.path.join(dirpath, fn))

for p in sorted(mirror_videos):
    rel = os.path.relpath(p, MIRROR)
    vkey = 'mirror/' + os.path.splitext(rel)[0]
    r = blank(vkey)
    st = os.stat(p)
    r.update(basename=os.path.basename(p), media_path=p, media_present='video',
             size=str(st.st_size), mtime=str(int(st.st_mtime)), origin='mirror',
             mirror_dir=os.path.dirname(rel) or '.', source_platform='local')
    for kind, col in (('transcription', 'transcription_path'),
                      ('ai_description', 'ai_description_path'),
                      ('ocr', 'ocr_path')):
        sc = sidecar_for(p, kind, MIRROR_SC, MIRROR)
        if not sc and os.path.isdir(MIRROR_LEG):
            sc = sidecar_for(p, kind, MIRROR_LEG, MIRROR)
        r[col] = sc
        if kind == 'transcription' and sc:
            r['transcription_source'] = 'video'
    # audio sibling in the mirror
    base_noext = os.path.splitext(p)[0]
    for ae in AUDIO_EXT:
        if os.path.exists(base_noext + ae):
            r['audio_path'] = base_noext + ae
            break
    if not r['transcription_path'] and r['audio_path']:
        sc = sidecar_for(r['audio_path'], 'transcription', MIRROR_SC, MIRROR)
        if sc:
            r['transcription_path'] = sc
            r['transcription_source'] = 'audio_sibling'
    rows[vkey] = r

# ---------------------------------------------------------------- 6. video_list.csv
yt_rows = 0
if os.path.exists(VIDEO_CSV):
    with open(VIDEO_CSV, encoding='utf-8') as fh:
        for rec in csv.reader(fh):
            if len(rec) < 3:
                continue
            title, yt, cid = rec[0].strip(), rec[1].strip(), rec[2].strip()
            if not yt.startswith('http'):
                continue
            m = re.search(r'(?:watch\?v=|playlist\?list=)([A-Za-z0-9_-]+)', yt)
            ident = m.group(1) if m else re.sub(r'\W+', '_', yt)[-24:]
            vkey = 'yt/' + ident
            if vkey in rows:
                continue
            r = blank(vkey)
            desc = rec[3].strip() if len(rec) > 3 else ''
            date = rec[8].strip() if len(rec) > 8 else ''
            r.update(basename=ident, media_present='none', origin='video_list_csv',
                     source_platform='youtube', source_url=yt, manifest_cid=cid,
                     manifest_description=desc.replace('\t', ' '), added_date=date,
                     title_hint=title.replace('\t', ' '))
            rows[vkey] = r
            yt_rows += 1

# ---------------------------------------------------------------- write
COLS = ['vkey', 'basename', 'media_path', 'media_present', 'size', 'mtime',
        'audio_path', 'transcription_path', 'transcription_source',
        'ai_description_path', 'ocr_path', 'manifest_cid', 'manifest_pinned',
        'source_url', 'source_author', 'added_date', 'manifest_description',
        'source_platform', 'origin', 'mirror_dir', 'title_hint']

with open(OUT, 'w', encoding='utf-8', newline='') as fh:
    w = csv.writer(fh, delimiter='\t', quoting=csv.QUOTE_MINIMAL,
                   lineterminator='\n')
    w.writerow(COLS)
    for vkey in sorted(rows):
        w.writerow([str(rows[vkey].get(c, '')).replace('\t', ' ').replace('\n', ' ')
                    for c in COLS])

# ---------------------------------------------------------------- report
by_origin, by_present = {}, {}
for r in rows.values():
    by_origin[r['origin']] = by_origin.get(r['origin'], 0) + 1
    by_present[r['media_present']] = by_present.get(r['media_present'], 0) + 1

disk_no_manifest = [n for stem, n in
                    ((s, os.path.basename(p)) for s, p in disk_video.items())
                    if n not in manifest_names]

print('============================')
print('STAGE 2 COMPLETE')
print(f'Rows in corpus index: {len(rows)}')
print(f"  from videos/ on disk: {by_origin.get('videos_dir',0)}"
      f"          from IPFS/videos: {by_origin.get('ipfs_dir',0)}")
print(f"  from manifest only (no local file): {by_origin.get('manifest_only',0)}"
      f" from mirror: {by_origin.get('mirror',0)}")
print(f"  from sidecar-only evidence: {by_origin.get('sidecar_only',0)}"
      f"         from video_list.csv: {by_origin.get('video_list_csv',0)}")
print(f"media_present: video {by_present.get('video',0)} / "
      f"audio_only {by_present.get('audio_only',0)} / none {by_present.get('none',0)}")
print(f'Manifest records with no disk file: {len(manifest_only)} (expected ~18)')
print(f'Disk files with no manifest record: {len(disk_no_manifest)} '
      f'({", ".join(sorted(disk_no_manifest))})')
print(f'Inventory written: {OUT}')
print('============================')

json.dump({'manifest_only': manifest_only, 'disk_no_manifest': disk_no_manifest,
           'by_origin': by_origin, 'by_present': by_present},
          open(os.path.join(os.path.dirname(OUT), 'stage2_report.json'), 'w'), indent=1)
