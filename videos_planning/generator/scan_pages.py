#!/usr/bin/env python3
# scan_pages.py — STAGES 10 and 11 of p_update_video_hierarchy.md.
#
# Stage 10  every page on the site that SHOWS a video must have that video
#           represented in the YAML. Unmatched embeds become new entries.
# Stage 11  on_pages: for every video, every OTHER page in the repo that embeds
#           it. OBSERVED, never reasoned.
#
# One linear pass: each file is read exactly once and every video reference in
# it is extracted, so this is O(repo text), not O(videos x pages).
import os, re, csv, json, hashlib, subprocess, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.expanduser('~/BGit/Bryan_git/charlie-kirk')
DOCS = os.path.join(ROOT, 'site/docs')
VIDEOS_L2 = os.path.join(DOCS, 'Videos')
IPFS = '/opt/homebrew/bin/ipfs'

TEXT_EXT = {'.md', '.mdx', '.html', '.tsx', '.jsx', '.ts', '.js', '.json',
            '.csv', '.yaml', '.yml'}
SKIP_DIRS = {'node_modules', 'build', '.git', '.docusaurus', '.lfbridge',
             '__pycache__', 'videos_planning', 'image_planning', '.cache'}
# Files that reference videos AS DATA, not as a page showing them.
SKIP_FILES = {
    os.path.join(ROOT, 'videos/videos.yaml'),
    os.path.join(ROOT, 'videos/manifest.yaml'),
    os.path.join(ROOT, 'videos/videos.md'),
    os.path.join(ROOT, 'pages.csv'),
    os.path.join(ROOT, 'IPFS/ipfs.txt'),
    os.path.join(ROOT, 'IPFS/ipfs.sh'),
}

cid_doc = json.load(open(os.path.join(HERE, 'cids.json'), encoding='utf-8'))
cid_index = dict(cid_doc['cid_index'])          # v0 and base32 -> vkey
entries = cid_doc['entries']
inv = {r['vkey']: r for r in
       csv.DictReader(open(os.path.join(HERE, 'inventory.tsv'), encoding='utf-8'),
                      delimiter='\t')}
sha_index = {e['sha256']: v for v, e in entries.items() if e.get('sha256')}
base_index = collections.defaultdict(list)
for v, r in inv.items():
    if r['media_path']:
        base_index[os.path.basename(r['media_path'])].append(v)
yt_index = {}
for v, r in inv.items():
    m = re.search(r'(?:watch\?v=|playlist\?list=|youtu\.be/|/embed/)([A-Za-z0-9_-]{6,})',
                  r.get('source_url', '') or '')
    if m:
        yt_index[m.group(1)] = v

VIDEO_EXT_RE = r'(?:mp4|mov|m4v|mkv|avi|webm)'
PATTERNS = [
    ('ipfs',  re.compile(r'https?://(?:ipfs\.io|dweb\.link|gateway\.pinata\.cloud|ipfs\.orbitor\.dev'
                         r'|ipfs\.filebase\.io|gw\.ipfs-lens\.dev)'
                         r'/ipfs/([A-Za-z0-9]{40,})')),
    ('ipfs',  re.compile(r'https?://([A-Za-z0-9]{50,})\.ipfs\.(?:dweb\.link|w3s\.link)')),
    ('ipfs',  re.compile(r'ipfs://([A-Za-z0-9]{40,})')),
    # third-party video is only EMBEDDED when it is an iframe/embed URL. A plain
    # youtube.com/watch link in prose is a citation, not something the page shows.
    ('yt',    re.compile(r'https?://(?:www\.)?youtube(?:-nocookie)?\.com/embed/'
                         r'([A-Za-z0-9_-]{6,})')),
    ('rumble', re.compile(r'https?://rumble\.com/embed/([A-Za-z0-9]+)')),
    ('odysee', re.compile(r'https?://odysee\.com/\$/embed/([^\s"\'<>)]+)')),
    ('file',  re.compile(r'["\'(]([^"\'()<>\s]+\.' + VIDEO_EXT_RE + r')["\')]')),
]
# NOTE: an https://x.com/<user>/status/<id> link is deliberately NOT a pattern.
# The whole corpus is X-sourced, so those links are everywhere in prose as
# CITATIONS. on_pages records where a video is SHOWN, and a link is not an
# embed. A page that actually shows our copy of an X video embeds it by CID.

# The images pipeline places stills by CID on these same pages, so a bare IPFS
# URL is not proof of video. Accept one only when the surrounding markup says
# video, the URL names a video file, or the CID is already a known video CID.
VIDEO_CONTEXT = re.compile(r'<video|<source|type\s*=\s*["\']video/|\.(?:'
                           + VIDEO_EXT_RE + r')\b', re.I)

def is_video_context(txt, start, end, ref, known):
    if known:
        return True
    lo = max(0, start - 300)
    hi = min(len(txt), end + 200)
    return bool(VIDEO_CONTEXT.search(txt[lo:hi]))

def tilde(p):
    h = os.path.expanduser('~')
    return '~' + p[len(h):] if p.startswith(h) else p

def norm_cid(c):
    if c in cid_index:
        return cid_index[c]
    return None

# ---------------------------------------------------------------- the sweep
on_pages = collections.defaultdict(set)
found_total = resolved = 0
by_kind = collections.Counter()
resolved_by = collections.Counter()
unresolved = []
site_embeds = []            # Stage 10: what the SITE shows
new_entries = {}            # identity -> proposed new entry

files_read = 0
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
    for fn in filenames:
        if os.path.splitext(fn)[1].lower() not in TEXT_EXT:
            continue
        full = os.path.join(dirpath, fn)
        if full in SKIP_FILES:
            continue
        try:
            txt = open(full, encoding='utf-8', errors='replace').read()
        except OSError:
            continue
        files_read += 1
        is_doc_page = full.startswith(DOCS) or full.startswith(os.path.join(ROOT, 'site/blog'))
        under_videos_l2 = full.startswith(VIDEOS_L2)
        # SCOPE: on_pages records where a video is SHOWN, and only something
        # under site/ is a page. Research/x_posts/*.yaml, images/images.yaml and
        # videos.csv reference videos as DATA — same class as videos.yaml and
        # manifest.yaml, which the prompt's scope rule already excludes.
        is_page = full.startswith(os.path.join(ROOT, 'site') + os.sep)

        for kind, pat in PATTERNS:
            for m in pat.finditer(txt):
                ref = m.group(1)
                if kind == 'file':
                    # only media that actually lives in this repo/mirror
                    if ref.startswith('http'):
                        continue
                if kind == 'ipfs' and not is_video_context(
                        txt, m.start(), m.end(), ref, ref in cid_index):
                    by_kind['ipfs_image_skipped'] += 1
                    continue
                found_total += 1
                by_kind[kind] += 1
                vkey = None
                if kind == 'ipfs':
                    vkey = norm_cid(ref) or (f'site/{ref}' if f'site/{ref}' in inv
                                             else None)
                    if vkey:
                        resolved_by['cid'] += 1
                elif kind in ('yt', 'rumble', 'odysee'):
                    # a corpus file named by its YouTube id (_QwGo0LyZ3I.mp4) is
                    # the same video as the embed that names that id
                    vkey = yt_index.get(ref) or (ref if ref in inv else None) \
                        or (f'yt/{ref}' if f'yt/{ref}' in inv else None)
                    if vkey:
                        resolved_by['third_party_id'] += 1
                elif kind == 'file':
                    b = os.path.basename(ref)
                    cands = base_index.get(b, [])
                    if len(cands) == 1:
                        vkey = cands[0]
                        resolved_by['basename'] += 1

                if is_doc_page:
                    site_embeds.append(dict(page=tilde(full), kind=kind, ref=ref,
                                            vkey=vkey))
                if vkey:
                    resolved += 1
                    # SCOPE: the video's own Level 5 page is video_page, and a
                    # cluster overview listing its children is structure.
                    if is_page and not under_videos_l2:
                        on_pages[vkey].add(tilde(full))
                    elif not is_page:
                        by_kind['data_reference_skipped'] += 1
                else:
                    if is_doc_page and kind in ('ipfs', 'yt', 'rumble', 'odysee'):
                        new_entries.setdefault((kind, ref), []).append(tilde(full))
                    unresolved.append((tilde(full), kind, ref))

out = {k: sorted(v) for k, v in on_pages.items()}
json.dump(out, open(os.path.join(HERE, 'on_pages.json'), 'w', encoding='utf-8'),
          indent=1)
json.dump(dict(site_embeds=site_embeds, new_entries={f'{k[0]}|{k[1]}': v
                                                     for k, v in new_entries.items()},
               unresolved=unresolved[:400]),
          open(os.path.join(HERE, 'stage10_report.json'), 'w', encoding='utf-8'),
          indent=1)

print('============================')
print('STAGE 10 COMPLETE')
site_pages = len({e['page'] for e in site_embeds})
matched = sum(1 for e in site_embeds if e['vkey'])
print(f'Pages scanned: {files_read}     Videos found on pages: {len(site_embeds)} '
      f'({matched} matched to corpus)  across {site_pages} pages')
print(f"IPFS-hosted: {sum(1 for e in site_embeds if e['kind']=='ipfs')}    "
      f"third-party hosted (YouTube/Rumble/X): "
      f"{sum(1 for e in site_embeds if e['kind'] in ('yt','rumble','odysee'))}")
print(f'New video identities the site shows that the corpus lacks: {len(new_entries)}')
for (kind, ref), pgs in sorted(new_entries.items())[:40]:
    print(f'   {kind:7s} {ref[:60]:60s} on {len(pgs)} page(s)')
print('============================')
print('STAGE 11 COMPLETE')
print(f'Files read: {files_read}        Video references found: {found_total}')
print(f"Resolved by CID: {resolved_by['cid']}   by third-party id: "
      f"{resolved_by['third_party_id']}   by sha256: 0   by basename: "
      f"{resolved_by['basename']}")
print(f'Unresolved: {len(unresolved)}')
print(f"IPFS URLs skipped as non-video (image placements): "
      f"{by_kind['ipfs_image_skipped']}")
print(f"References in data files, not pages (scope rule, not bound): "
      f"{by_kind['data_reference_skipped']}")
print(f'Entries with on_pages non-empty: {len(out)}    '
      f'Total page bindings: {sum(len(v) for v in out.values())}')
print('============================')
