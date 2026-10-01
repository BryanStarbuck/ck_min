#!/usr/bin/env python3
# gen_videos_pages.py — Stages 1-4 of p_yaml_to_site.md.
#
# Reads   {ROOT}/videos/videos.yaml            (the plan; READ ONLY)
# Writes  {ROOT}/site/docs/Videos/**           (cluster pages + Vid_*.mdx video pages)
#         {ROOT}/site/static/img/video_posters/*.jpg
#         the CK_VIDEO_LAYOUT + CK_PLACED_VIDEOS blocks of custom.css
#         the CK_VIDEOS_TOC block of site/docs/Videos/overview.mdx
#         {ROOT}/pages.csv rows for the pages it wrote
#
# VIDEOS ONLY, ADDITIVE ONLY. It never reads or writes {ROOT}/images,
# image_planning, site/docs/Photos, static/img/evidence, or any CK_PLACED_IMAGES
# / CK_EVIDENCE_LAYOUT marked block.
#
# NOTHING IS EVER PINNED. A player is emitted only for a CID that is actually
# pinned on this node (verified at run time); everything else gets its full page
# with a poster and an honest media-pending note.
import base64
import os, re, sys, csv, json, html, subprocess, unicodedata, shutil
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sanitize_video import sanitize_prose, sanitize_block, validate_no_invisible
import ipfs_gateways

HERE     = os.path.dirname(os.path.abspath(__file__))
ROOT     = os.path.expanduser('~/BGit/Bryan_git/charlie-kirk')
YAML     = os.path.join(ROOT, 'videos', 'videos.yaml')
SITE     = os.path.join(ROOT, 'site')
DOCS     = os.path.join(SITE, 'docs')
L2DIR    = os.path.join(DOCS, 'Videos')
L2PAGE   = os.path.join(L2DIR, 'overview.mdx')
POSTERS  = os.path.join(SITE, 'internals', 'static', 'img', 'video_posters')
CSSFILE  = os.path.join(SITE, 'internals', 'src', 'css', 'custom.css')
PAGESCSV = os.path.join(ROOT, 'pages.csv')
EXCLUDE  = os.path.join(ROOT, 'videos_planning', 'exclude_videos.txt')
BANCSV   = os.path.join(ROOT, 'videos', 'ban_videos.csv')
OUTJSON  = os.path.join(HERE, 'generated_pages.json')
IPFS     = '/opt/homebrew/bin/ipfs'
FFPROBE  = '/opt/homebrew/bin/ffprobe'
FFMPEG   = '/opt/homebrew/bin/ffmpeg'

PROTECTED = {'overview.mdx', 'buckley-carlson-kash-patel-valhalla.mdx', '_category_.json'}

# Two columns rather than the home page's three: the main area on these pages is
# narrower, and two columns stay readable on a laptop.
TOC_COLUMNS = 2

# ------------------------------------------------------------------ helpers
def run(args, timeout=180):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except Exception as e:
        return 1, '', str(e)

EMOJI_RE = re.compile(
    '[\U0001F000-\U0001FAFF\U00002190-\U000021FF\U00002300-\U000027BF'
    '\U00002B00-\U00002BFF\U0001F1E6-\U0001F1FF☀-⛿]')

def clean_title(s, limit=95):
    s = sanitize_prose(s or '')
    s = EMOJI_RE.sub('', s)
    s = re.sub(r'\s*\|\s*$', '', s)
    s = re.sub(r'\s{2,}', ' ', s).strip(' -—–·')
    # X-post titles arrive as "Author - post text ...". Keep the whole thing but
    # trim the trailing ellipsis noise.
    s = re.sub(r'\s*\.\.\.$', '', s)
    s = re.sub(r'\s*\[\d{6,}\]\s*$', '', s)
    if len(s) > limit:
        cut = s[:limit].rsplit(' ', 1)[0]
        s = cut.rstrip(' ,;:-') + '…'
    return mdx_safe(s) or 'Untitled clip'

def short_label(s, limit=42):
    s = clean_title(s, limit * 3)
    if len(s) > limit:
        s = s[:limit].rsplit(' ', 1)[0].rstrip(' ,;:-') + '…'
    return s

STOP = {'the','a','an','of','and','or','to','in','on','at','for','with','is','it',
        'this','that','was','were','by','from','as','be','not','i','you','he','she',
        'they','we','his','her','their','its','my','me','but','so','if','then','than'}

def mint_key(title, seed):
    t = EMOJI_RE.sub(' ', sanitize_prose(title or ''))
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode()
    words = [w for w in re.split(r'[^A-Za-z0-9]+', t) if w]
    picked, seen = [], set()
    for w in words:
        lw = w.lower()
        if lw in STOP or lw in seen:
            continue
        seen.add(lw)
        picked.append(w[:1].upper() + w[1:])
        if len(picked) == 4:
            break
    if not picked:
        picked = ['Clip']
    return 'Vid_' + '_'.join(picked) + '_' + str(seed)[:7]

def esc_yaml(s):
    s = sanitize_prose(s).replace('&lt;', '<').replace('&#123;', '{').replace('&#125;', '}')
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'

def _decode_yaml_scalar(v):
    """Decode a frontmatter YAML scalar back to its literal string value.

    This is the inverse of esc_yaml(). It MUST be used wherever a title is read
    back out of an existing page, because that title is later re-emitted through
    esc_yaml(). Without decoding, a double-quoted title keeps its \\" escapes,
    esc_yaml() escapes them again, and every regeneration doubles the backslash
    count — the runaway-backslash title bug. Decoding makes the round-trip
    idempotent. Unquoted values (true / CIDs / plain words) pass through
    unchanged."""
    v = v.strip()
    if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
        s = v[1:-1]
        out = []
        i = 0
        while i < len(s):
            c = s[i]
            if c == '\\' and i + 1 < len(s):
                nxt = s[i + 1]
                if nxt in '\\"':
                    out.append(nxt); i += 2; continue
                if nxt == 'n':
                    out.append('\n'); i += 2; continue
                if nxt == 't':
                    out.append('\t'); i += 2; continue
            out.append(c); i += 1
        return ''.join(out)
    if len(v) >= 2 and v[0] == "'" and v[-1] == "'":
        return v[1:-1].replace("''", "'")
    return v

def first_sentences(s, n=2, limit=300):
    s = sanitize_prose(s or '')
    parts = re.split(r'(?<=[.!?])\s+', s)
    out = mdx_safe(' '.join(parts[:n]).strip())
    if len(out) > limit:
        out = out[:limit].rsplit(' ', 1)[0].rstrip(' ,;:-') + '…'
    return out

def mdx_safe(s):
    """YAML-derived prose is plain text going into MDX. `<` starts a JSX tag and
    `{` starts an expression, so both must be escaped or the page will not
    compile. Everything the generator emits as markup is added AFTER this."""
    return (s or '').replace('<', '&lt;').replace('{', '&#123;').replace('}', '&#125;')

def rel_url(path):
    """Route for a page we generate ourselves under /Videos. Our own layout is
    path-derived, so this is exact for those."""
    return '/' + os.path.relpath(path, DOCS)[:-4].replace(os.sep, '/')

_ROUTES = {}
def _load_routes():
    try:
        for row in csv.DictReader(open(PAGESCSV, encoding='utf-8')):
            fp, up = row.get('file_path') or '', row.get('url_path') or ''
            if fp and up:
                _ROUTES[os.path.normpath(os.path.join(ROOT, fp))] = up
    except Exception:
        pass

def site_url(path):
    """Route for ANY page on the site, including ones this pipeline did not
    write. A file path is not a route: site/docs/index.md is served at "/", not
    "/index", and a directory hub may carry a slug that differs from its folder.
    pages.csv records the real url_path, so it wins; the path-derived form is
    only the fallback."""
    path = os.path.normpath(path)
    u = _ROUTES.get(path)
    if u:
        return u
    u = rel_url(path)
    if u in ('/index', '/README'):
        return '/'
    return re.sub(r'/index$', '', u) or '/'

def dur_human(d):
    if not d:
        return ''
    m = re.match(r'^(\d+):(\d+):(\d+)$', d.strip())
    if not m:
        return d.strip()
    h, mi, s = (int(x) for x in m.groups())
    return (f'{h}:{mi:02d}:{s:02d}' if h else f'{mi}:{s:02d}')

# ------------------------------------------------------------------ load YAML
import yaml as _yaml
print('loading videos.yaml ...', flush=True)
DATA = _yaml.safe_load(open(YAML, encoding='utf-8'))

# THE BAN SET is the UNION of two sources (see the repo charter, "Banned Media"):
#   videos/ban_videos.csv          — the newer master, carries reason + a
#                                    true/false switch, so a row can un-ban.
#   videos_planning/exclude_videos.txt — the older one-identifier-per-line list.
# An item banned in EITHER gets no page, and any page it already has is deleted.
excluded, unbanned = set(), set()
if os.path.exists(EXCLUDE):
    for line in open(EXCLUDE, encoding='utf-8'):
        line = line.split('#')[0].strip()
        if line:
            excluded.add(line)
ban_rows = 0
if os.path.exists(BANCSV):
    for row in csv.DictReader(open(BANCSV, encoding='utf-8')):
        ids = [str(row.get(k) or '').strip() for k in ('sha256', 'cid', 'file_path')]
        ids = [i for i in ids if i]
        if not ids:
            continue
        ban_rows += 1
        if str(row.get('banned') or '').strip().lower() == 'false':
            unbanned.update(ids)          # explicit un-ban: the row records the decision
        else:
            excluded.update(ids)
excluded -= unbanned

class Node:
    __slots__ = ('lvl','key','title','raw','parent','kids','vids','rec','dirpath','page','bypass','bypass_target')
    def __init__(self, lvl, raw, parent):
        self.lvl, self.raw, self.parent = lvl, raw, parent
        self.key   = raw.get('_key')
        self.title = mdx_safe(sanitize_prose(raw.get('title') or self.key))
        self.kids, self.vids = [], []
        self.rec = 0
        self.bypass = False
        self.bypass_target = None

nodes, roots = [], []
def build(items, lvl, parent):
    key = 'level_%d' % lvl
    out = []
    for it in items or []:
        raw = it.get(key) if isinstance(it, dict) and key in it else it
        n = Node(lvl, raw, parent)
        nodes.append(n)
        out.append(n)
        n.kids = build(raw.get('level_%d' % (lvl + 1)), lvl + 1, n)
    return out
roots = build(DATA['level_3'], 3, None)

# ------------------------------------------------- unique videos, owner nodes
seen_ident, videos = {}, []
dupes = 0
for n in nodes:
    for item in n.raw.get('videos') or []:
        v = item.get('video') if isinstance(item, dict) and 'video' in item else item
        ident = v.get('cid') or v.get('sha256') or v.get('file_path')
        if not ident:
            continue
        if ident in seen_ident:
            seen_ident[ident]['also_nodes'].append(n)
            dupes += 1
            continue
        rec = dict(v=v, owner=n, also_nodes=[], ident=ident)
        seen_ident[ident] = rec
        videos.append(rec)
        n.vids.append(rec)

# recursive counts recomputed from the tree, never trusted from the file
def recount(n):
    n.rec = len(n.vids) + sum(recount(k) for k in n.kids)
    return n.rec
for r in roots:
    recount(r)

# ------------------------------------------------------ exclusion + publishable
def is_banned(v):
    for k in ('cid', 'sha256', 'file_path'):
        val = (v.get(k) or '').strip()
        if val and val in excluded:
            return True
    return False
skipped_excluded = [r for r in videos if is_banned(r['v'])]
for r in skipped_excluded:
    r['owner'].vids.remove(r)
videos = [r for r in videos if r not in skipped_excluded]
banned_pages_deleted = 0
for r in skipped_excluded:
    sha = r['v'].get('sha256') or ''
    poster = os.path.join(POSTERS, sha + '.jpg') if sha else ''
    if poster and os.path.exists(poster):
        os.remove(poster); banned_pages_deleted += 1
for r in roots:
    recount(r)

pub_nodes = [n for n in nodes if n.rec > 0]
empty_nodes = [n for n in nodes if n.rec == 0]

# ------------------------------------------------------------- paths and keys
for n in pub_nodes:
    chain, c = [], n
    while c is not None:
        chain.append(c.key)
        c = c.parent
    n.dirpath = os.path.join(L2DIR, *reversed(chain))
    n.page = os.path.join(n.dirpath, 'overview.mdx')

# Page keys become public URL slugs, so a slug minted from a raw social-media
# title can carry wording the site will not say in its own voice. An override
# here retires that slug for good; the minting rule is otherwise unchanged.
KEY_OVERRIDES = {
    # "hand off" implies a deliberate transfer between people and is not what the
    # footage establishes. See the repo guidance on this phrasing.
    'Vid_Hand_Off_pANvLdZ': 'Vid_Guard_Hands_Split_pANvLdZ',
}

used_keys = set(n.key for n in pub_nodes)

# STABLE PAGE KEYS ACROSS RERUNS. A video that already has a published page keeps
# that page's exact key (its URL, and every word of prose carried forward from
# that path). The minted key depends on the file path / CID, so re-filing a video
# or swapping in a higher-resolution copy (new sha256, sometimes a new CID) used
# to mint a new key: the orphan sweep deleted the authored page and a generic one
# appeared under a new URL (2026-09-26: 12 authored pages lost this way). Match an
# existing page by sha256 first, then by CID; prefer the owner's dir, then an
# authored page. A page found in another dir is moved so its prose carries over.
def _head_fm(path):
    # existing_fm() is defined further down; this pre-pass needs only three keys.
    try:
        head = open(path, encoding='utf-8').read(3000)
    except OSError:
        return {}
    out = {}
    for key in ('ck_video_sha256', 'ck_video_cid', 'ck_authored'):
        m = re.search(r'^' + key + r':\s*"?([^"\n]*)"?\s*$', head, re.M)
        if m:
            out[key] = m.group(1).strip()
    return out


_existing_by = {}
for _dp, _dn, _fns in os.walk(L2DIR):
    for _fn in sorted(_fns):
        if not _fn.endswith('.mdx') or _fn in PROTECTED:
            continue
        _p = os.path.join(_dp, _fn)
        _fm = _head_fm(_p)
        for _id in (_fm.get('ck_video_sha256'), _fm.get('ck_video_cid')):
            if _id:
                _existing_by.setdefault(_id, []).append(_p)
_claimed_pages = set()


def _reuse_page(r):
    v = r['v']
    for _id in (v.get('sha256'), v.get('cid')):
        cands = [p for p in _existing_by.get(_id or '', [])
                 if p not in _claimed_pages and os.path.exists(p)
                 and os.path.splitext(os.path.basename(p))[0] not in used_keys]
        if not cands:
            continue
        cands.sort(key=lambda p: (os.path.dirname(p) != r['owner'].dirpath,
                                  _head_fm(p).get('ck_authored', '').lower() != 'true', p))
        return cands[0]
    return None


for r in videos:
    v = r['v']
    old_page = _reuse_page(r)
    if old_page:
        _claimed_pages.add(old_page)
        k = os.path.splitext(os.path.basename(old_page))[0]
        used_keys.add(k)
        r['key'] = k
        r['page'] = os.path.join(r['owner'].dirpath, k + '.mdx')
        if os.path.realpath(old_page) != os.path.realpath(r['page']) and not os.path.exists(r['page']):
            os.makedirs(os.path.dirname(r['page']), exist_ok=True)
            os.replace(old_page, r['page'])
        r['url'] = rel_url(r['page'])
        continue
    seed = ''
    m = re.search(r'\[(\d{8,})\]', v.get('file_path') or '')
    if m:
        seed = m.group(1)
    if not seed:
        m = re.search(r'/(\d{8,})(?:_\d+)?\.\w+$', v.get('file_path') or '')
        if m:
            seed = m.group(1)
    if not seed:
        seed = (v.get('cid') or v.get('sha256') or 'x')[-12:]
    k = mint_key(v.get('title'), seed)
    k = KEY_OVERRIDES.get(k, k)
    base, i = k, 2
    while k in used_keys:
        k = f'{base}_{i}'; i += 1
    used_keys.add(k)
    r['key'] = k
    r['page'] = os.path.join(r['owner'].dirpath, k + '.mdx')
    r['url'] = rel_url(r['page'])

# ---------------------------------------------- global "Next Video" chain (loop)
# One flat sequence S over the WHOLE hierarchy in document pre-order: `videos` is
# already in that order (a node's own videos before its children, children in
# YAML order, first-occurrence-wins dedup). next_url is the successor in S and
# the last video wraps to the first, so the walk never dead-ends. This is the
# authority for both the button href and the next_video value written back into
# videos.yaml (carries out videos_planning/p_next_buttons.md).
def _tilde(p):
    h = os.path.expanduser('~')
    return '~' + p[len(h):] if p and p.startswith(h) else (p or '')
NV = len(videos)
for i, r in enumerate(videos):
    nxt = videos[(i + 1) % NV] if NV else None
    r['next_url'] = nxt['url'] if nxt else ''
    r['next_page_tilde'] = _tilde(nxt['page']) if nxt else ''

# ------------------------------------------------------------- bypass set
def resolve_single(n):
    """Return the one video rec a node's subtree resolves to, or None."""
    if n.rec != 1:
        return None
    if n.vids:
        return n.vids[0]
    for k in n.kids:
        got = resolve_single(k)
        if got:
            return got
    return None
for n in pub_nodes:
    tgt = resolve_single(n)
    if tgt is not None:
        n.bypass, n.bypass_target = True, tgt

# ------------------------------------------------------- pin status (run time)
print('reading local pin set ...', flush=True)
rc, out, _ = run([IPFS, 'pin', 'ls', '--type=recursive'], timeout=300)
PINNED = set(l.split()[0] for l in out.splitlines() if l.strip()) if rc == 0 else set()
print(f'  {len(PINNED)} recursive pins on the node', flush=True)

B32 = {}
_B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base32(cid):
    """CIDv0/v1 -> CIDv1 base32, the form the subdomain gateways require.

    Pure Python on purpose. This used to shell out to `ipfs cid base32`, which
    returned '' whenever the daemon/CLI was missing - and an empty b32 silently
    dropped the only working <source>, shipping a dead player. No external
    dependency now, so it cannot degrade that way."""
    if cid in B32:
        return B32[cid]
    out = ''
    try:
        c = cid.strip()
        if c.startswith('Qm'):                      # CIDv0, base58btc multihash
            n = 0
            for ch in c:
                n = n * 58 + _B58.index(ch)
            mh = n.to_bytes((n.bit_length() + 7) // 8, 'big')
            mh = b'\x00' * (len(c) - len(c.lstrip('1'))) + mh
            out = 'b' + base64.b32encode(b'\x01\x70' + mh).decode().lower().rstrip('=')
        elif c.startswith('b'):                     # already CIDv1 base32
            out = c
    except Exception:
        out = ''
    B32[cid] = out
    return out

# -------------------------------------------------- probe + posters (parallel)
os.makedirs(POSTERS, exist_ok=True)

def probe_and_poster(r):
    v = r['v']
    fp = os.path.expanduser(v.get('file_path') or '')
    r['w'] = r['h'] = 0
    r['poster'] = ''
    r['assumed_ratio'] = False
    if not fp or not os.path.exists(fp) or v.get('media_present') != 'video':
        r['assumed_ratio'] = True
        return
    rc, o, _ = run([FFPROBE, '-v', 'error', '-select_streams', 'v:0',
                    '-show_entries', 'stream=width,height', '-of', 'csv=p=0:s=x', fp], 60)
    if rc == 0 and 'x' in o:
        try:
            w, h = o.split('\n')[0].split('x')[:2]
            r['w'], r['h'] = int(w), int(h)
        except Exception:
            pass
    if not r['w']:
        r['assumed_ratio'] = True
    sha = v.get('sha256') or ''
    if not sha:
        return
    dest = os.path.join(POSTERS, sha + '.jpg')
    if os.path.exists(dest):
        r['poster'] = '/img/video_posters/%s.jpg' % sha
        return
    rc, _, _ = run([FFMPEG, '-nostdin', '-y', '-ss', '3', '-i', fp, '-frames:v', '1',
                    '-vf', "scale='min(1600,iw)':-2", '-q:v', '4', dest], 180)
    if rc != 0 or not os.path.exists(dest):
        rc, _, _ = run([FFMPEG, '-nostdin', '-y', '-ss', '0', '-i', fp, '-frames:v', '1',
                        '-vf', "scale='min(1600,iw)':-2", '-q:v', '4', dest], 180)
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        r['poster'] = '/img/video_posters/%s.jpg' % sha
    elif os.path.exists(dest):
        os.remove(dest)

print(f'probing {len(videos)} videos and extracting posters ...', flush=True)
with ThreadPoolExecutor(max_workers=6) as ex:
    list(ex.map(probe_and_poster, videos))
print('  posters on disk:', len([r for r in videos if r['poster']]), flush=True)

# ------------------------------------------------- CID CONTENT-TYPE GATE
# A CID is an opaque identity; nothing about it says the bytes are video. This
# corpus contains at least one entry whose CID resolves to a JPEG, which had it
# gone unchecked would have wrapped a still image in a <video> player — a
# control bar under a photograph, on a page that says it is footage.
# Blocks for a pinned CID are local, so the first 32 bytes are cheap to read.
def cid_kind(cid):
    rc, _, _ = 0, '', ''
    try:
        p = subprocess.run([IPFS, 'cat', '--length', '32', cid],
                           capture_output=True, timeout=25)
        b = p.stdout
    except Exception:
        b = b''
    if b[4:8] == b'ftyp':
        return 'mp4'
    if b[:4] == b'\x1aE\xdf\xa3':
        return 'webm'
    if b[:3] == b'\xff\xd8\xff':
        return 'jpeg'
    if b[:8] == b'\x89PNG\r\n\x1a\n':
        return 'png'
    if b[:3] == b'ID3' or b[:2] == b'\xff\xfb':
        return 'mp3'
    return 'unknown' if b else 'unreadable'

# ---------------------------------------------------------- playback decision
for r in videos:
    v = r['v']
    cid = (v.get('cid') or '').strip()
    plat = (v.get('source_platform') or '').lower()
    url = (v.get('source_url') or '').strip()
    r['mode'] = 'pending'
    r['embed_url'] = ''
    if plat in ('youtube', 'rumble') and url:
        if 'playlist' in url:
            r['mode'] = 'link'
        else:
            r['mode'] = 'thirdparty'
        r['embed_url'] = url
    elif cid and cid in PINNED:
        r['mode'] = 'ipfs'
    r['pending_reason'] = ''
    if r['mode'] == 'pending':
        if not cid:
            r['pending_reason'] = 'no-cid'
        elif v.get('media_present') == 'audio_only':
            r['pending_reason'] = 'audio-only'
        elif v.get('media_present') == 'none':
            r['pending_reason'] = 'no-media'
        else:
            r['pending_reason'] = 'unpinned'

wrong_kind = []
print('verifying CID content type for pinned entries ...', flush=True)
with ThreadPoolExecutor(max_workers=6) as ex:
    kinds = dict(zip([r['ident'] for r in videos if r['mode'] == 'ipfs'],
                     ex.map(cid_kind, [r['v']['cid'] for r in videos if r['mode'] == 'ipfs'])))
for r in videos:
    if r['mode'] != 'ipfs':
        continue
    k = kinds.get(r['ident'], 'unknown')
    if k in ('mp4', 'webm'):
        continue
    wrong_kind.append((r['key'], r['v']['cid'], k))
    r['mode'] = 'pending'
    r['pending_reason'] = 'not-video'
print(f'  CIDs that are not video (player withheld): {len(wrong_kind)}', flush=True)

# ------------------------------------------------------------------ templates
GEN_NOTE = ('{/* Generated by videos_planning/generator/gen_videos_pages.py from '
            'videos/videos.yaml. Structure between the CK_NAV markers is rewritten '
            'on every run; prose between the CK_PROSE markers is preserved. */}')

def yt_id(u):
    m = re.search(r'[?&]v=([A-Za-z0-9_-]{6,})', u) or re.search(r'youtu\.be/([A-Za-z0-9_-]{6,})', u)
    return m.group(1) if m else ''

def player_block(r):
    v = r['v']
    cid = (v.get('cid') or '').strip()
    poster = r['poster']
    wrap_mod = 'ck-video-wrap--full'
    if r['w'] and r['h'] and (r['w'] / r['h']) < 1.0:
        wrap_mod = 'ck-video-wrap--wrapped'
    ratio_note = ''
    if r['assumed_ratio'] and r['mode'] == 'ipfs':
        ratio_note = '\n{/* aspect ratio assumed 16:9 - no local copy to measure */}'
    if r['mode'] == 'ipfs':
        # Gateway list and its measurements live in ipfs_gateways.py - the
        # same list rewrite_video_gateways.py applies to existing pages.
        # (dweb.link / ipfs.io / w3s.link retired 2026-09; see that module.)
        b32 = base32(cid)
        if b32:
            srcs = ipfs_gateways.video_sources(b32, '    ')
        else:
            srcs = f'    {{/* no base32 for CID {cid} - no playable source emitted */}}\n'
        return (f'{ratio_note}\n<div className="ck-video-wrap {wrap_mod}">\n'
                f'  <video className="ck-video-media" controls preload="metadata"'
                + (f' poster="{poster}"' if poster else '') + '>\n'
                + srcs +
                '    Your browser does not support the video tag.\n'
                '  </video>\n</div>\n')
    if r['mode'] == 'thirdparty':
        u = r['embed_url']
        if 'youtube' in u:
            vid = yt_id(u)
            src = f'https://www.youtube.com/embed/{vid}'
        else:
            src = u if '/embed/' in u else u
        return ('\n<div className="ck-video-wrap ck-video-wrap--full ck-video-wrap--embed">\n'
                f'  <iframe className="ck-video-media" src="{src}" title="Video" loading="lazy"\n'
                '          allow="accelerometer; clipboard-write; encrypted-media; picture-in-picture"\n'
                '          allowFullScreen></iframe>\n</div>\n')
    # pending
    lines = []
    if poster:
        lines.append('\n<div className="ck-video-wrap ck-video-wrap--full ck-video-wrap--pending">\n'
                     f'  <img className="ck-video-media" src="{poster}" alt="Frame from this video" loading="lazy" />\n'
                     '</div>\n')
    reason = r['pending_reason']
    if reason == 'unpinned':
        body = ('**Media pending.** This footage is held locally and has not yet been published '
                'to IPFS, so it cannot be played here yet. The write-up below is complete.  \n'
                f'CID (computed): `{v.get("cid")}`')
    elif reason == 'audio-only':
        body = ('**Media pending.** Only the audio of this item is held locally, and it has not '
                'yet been published, so there is nothing to play here yet. The write-up below is '
                'drawn from the transcript.')
    elif reason == 'not-video':
        body = ('**Media pending.** The content identifier recorded for this item does not '
                'resolve to a video file, so there is nothing to play here. The identifier '
                'is recorded below for correction and the write-up is complete.  \n'
                f'CID (does not resolve to video): `{v.get("cid")}`')
    elif reason == 'no-cid':
        body = ('**Media pending.** No content identifier has been recorded for this item yet, '
                'so it cannot be played here. The write-up below is complete.')
    else:
        body = ('**Media pending.** The media for this item is not held locally and has not been '
                'published, so it cannot be played here. The write-up below is drawn from the '
                'records that describe it.')
    lines.append('\n:::note\n\n' + body + '\n\n:::\n')
    return ''.join(lines)

_load_routes()

PAGE_TITLES = {}
def _load_page_titles():
    try:
        for row in csv.DictReader(open(PAGESCSV, encoding='utf-8')):
            fp = row.get('file_path') or ''
            if fp:
                PAGE_TITLES[os.path.join(ROOT, fp)] = row.get('title') or ''
    except Exception:
        pass
_load_page_titles()

def page_label(path):
    t = PAGE_TITLES.get(path, '')
    if not t:
        m = re.search(r'^title:\s*(.+)$', open(path, encoding='utf-8').read()[:2000], re.M)
        t = _decode_yaml_scalar(m.group(1)) if m else ''
    return mdx_safe(sanitize_prose(t)) or rel_url(path)

def existing_fm(path):
    """Frontmatter of an existing page, or {}."""
    if not os.path.exists(path):
        return {}
    txt = open(path, encoding='utf-8').read()
    m = re.match(r'^---\n(.*?)\n---\n', txt, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        km = re.match(r'^([A-Za-z0-9_]+):\s*(.*)$', line)
        if km:
            out[km.group(1)] = _decode_yaml_scalar(km.group(2))
    return out

def extract_prose(path, marker='CK_PROSE'):
    if not os.path.exists(path):
        return None
    txt = open(path, encoding='utf-8').read()
    m = re.search(r'\{/\* %s_START \*/\}(.*?)\{/\* %s_END \*/\}' % (marker, marker), txt, re.S)
    if not m:
        return None
    body = m.group(1)
    if 'CK_PROSE_BASELINE' in body:
        return None          # our own boilerplate — refresh it from current data
    return body.strip('\n')

# --------------------------------------------------------- video page write-up
def baseline_writeup(r):
    v = r['v']
    out = ['{/* CK_PROSE_BASELINE */}', '']
    out.append('## What This Video Shows')
    out.append('')
    desc = mdx_safe(sanitize_block(v.get('ai_description') or '').strip())
    if desc:
        out.append(desc)
    else:
        out.append('A visual account of this clip has not been recorded yet.')
    out.append('')

    src_bits = []
    d = dur_human(v.get('duration'))
    if d:
        src_bits.append(f'Running time {d}.')
    plat = (v.get('source_platform') or '').lower()
    auth = mdx_safe(sanitize_prose(v.get('source_author') or ''))
    url = (v.get('source_url') or '').strip()
    if plat == 'x' and auth:
        src_bits.append(f'Captured from a post by {auth} on X.')
    elif plat == 'youtube':
        src_bits.append('Hosted on YouTube by its publisher, who can remove it at any time.')
    elif plat == 'rumble':
        src_bits.append('Hosted on Rumble by its publisher, who can remove it at any time.')
    elif plat == 'local':
        src_bits.append('Held in the investigation’s own capture archive.')
    if url:
        src_bits.append(f'Source: [{url}]({url})')
    if src_bits:
        out.append('### Where It Came From')
        out.append('')
        out.append(' '.join(src_bits))
        out.append('')

    people = mdx_safe(sanitize_block(v.get('people_seen') or '').strip())
    if people and people.lower() not in ('no people appear.', 'none.', 'n/a'):
        out.append('### Who Appears')
        out.append('')
        out.append(people)
        out.append('')

    ost = mdx_safe(sanitize_block(v.get('onscreen_text') or '').strip())
    if ost and ost.lower() not in ('none.', 'n/a', 'no on-screen text.'):
        out.append('### On-Screen Text')
        out.append('')
        out.append(ost)
        out.append('')

    tl = mdx_safe(sanitize_block(v.get('shot_timeline') or '').strip())
    if tl:
        out.append('### Shot By Shot')
        out.append('')
        out.append(tl)
        out.append('')
    return '\n'.join(out).rstrip() + '\n'

def nav_block_video(r):
    n = r['owner']
    anc = n
    while anc is not None and anc.bypass:
        anc = anc.parent
    lines = ['{/* CK_NAV_START */}', '']

    appears = []
    for item in r['v'].get('on_pages') or []:
        p = item.get('page') if isinstance(item, dict) else str(item)
        p = os.path.expanduser(str(p).strip())
        if p.startswith(DOCS) and os.path.exists(p):
            appears.append(p)
    if appears:
        lines += ['## Where This Video Also Appears', '']
        for p in sorted(set(appears)):
            lines.append(f'* [{page_label(p)}]({site_url(p)})')
        lines.append('')

    also = sorted({m.key: m for m in r['also_nodes'] if m.rec > 0}.values(), key=lambda x: x.title)
    if also:
        lines += ['## Also Filed Under', '']
        for m in also:
            tgt = rel_url(m.bypass_target['page']) if m.bypass else rel_url(m.page)
            lines.append(f'* [{m.title}]({tgt})')
        lines.append('')

    peers = [p for p in n.vids if p is not r]
    if peers:
        lines += ['## Other Videos In This Section', '']
        for p in peers[:12]:
            lines.append(f'* [{_vt(p, 80)}]({p["url"]})')
        lines.append('')

    if anc is not None:
        lines += ['', f'[← Back to {anc.title}]({rel_url(anc.page)}) · '
                      f'[All video evidence](/Videos/overview)', '']
    else:
        lines += ['', '[← All video evidence](/Videos/overview)', '']
    lines += ['{/* CK_NAV_END */}']
    return '\n'.join(lines)

def fallback_description(r):
    """CK-05: a video with no recorded description gets a unique, informative
    one — its title, its set, its source and running time — never the bare title."""
    v = r['v']
    bits = [f"Video '{clean_title(v.get('title'), 90)}' from the {_cluster_tag(r['owner'])} "
            f"video set of the Charlie Kirk investigation"]
    auth = sanitize_prose(v.get('source_author') or '')
    if (v.get('source_platform') or '').lower() == 'x' and auth:
        bits.append(f', captured from a post by {auth} on X')
    d = dur_human(v.get('duration'))
    if d:
        bits.append(f', running {d}')
    return mdx_safe(''.join(bits) + '.')

def write_video_page(r):
    v = r['v']
    old = existing_fm(r['page'])
    authored = old.get('ck_authored') == 'true'
    title = r.get('title') or clean_title(v.get('title'))
    label = old.get('sidebar_label') if authored and old.get('sidebar_label') else short_label(v.get('title'))
    prose = extract_prose(r['page']) or baseline_writeup(r)
    desc = (old.get('description') if authored and old.get('description')
            else first_sentences(v.get('ai_description') or v.get('manifest_description') or '', 2, 260)
            or fallback_description(r))
    fm = ['---',
          'title: ' + esc_yaml(title),
          'sidebar_label: ' + esc_yaml(label),
          'hide_table_of_contents: true',
          'description: ' + esc_yaml(desc),
          *(['image: ' + r['share_image']] if r.get('share_image') else []),
          'ck_authored: ' + ('true' if authored else 'false'),
          'ck_video_cid: ' + esc_yaml(v.get('cid') or ''),
          'ck_video_sha256: ' + esc_yaml(v.get('sha256') or ''),
          'ck_node_key: ' + esc_yaml(r['owner'].key),
          '---', '']
    body = [GEN_NOTE, '', '# ' + title, '',
            player_block(r), '',
            next_video_button(r), '',
            '<div className="ck-video-text">', '',
            '{/* CK_PROSE_START */}', '', prose, '', '{/* CK_PROSE_END */}', '',
            nav_block_video(r), '',
            '</div>', '']
    txt = '\n'.join(fm + body)
    txt = re.sub(r'\n{4,}', '\n\n\n', txt)
    os.makedirs(os.path.dirname(r['page']), exist_ok=True)
    existed = os.path.exists(r['page'])
    open(r['page'], 'w', encoding='utf-8').write(txt)
    return existed

# ------------------------------------------------------------- cluster pages
def _vt(r, limit):
    """Link text for a video: the authored title when there is one, trimmed."""
    t = r.get('title') or clean_title(r['v'].get('title'), limit)
    if len(t) > limit:
        t = t[:limit].rsplit(' ', 1)[0].rstrip(' ,;:-') + '…'
    return t

def _dur_suffix(r):
    d = dur_human(r['v'].get('duration'))
    return f' ({d})' if d else ''

# The "Next Video" button (videos_planning/p_next_buttons.md). A dark-navy pill
# with a white label and a white right chevron, rendered directly under the
# player. Its href is the site-relative url of this video's next_video — the next
# clip in one global depth-first walk of the whole hierarchy, looping the last
# clip back to the first. Styling lives once in the CK_VIDEO_LAYOUT CSS block, so
# the pill inherits the player wrapper's float and drops beneath the clip.
NEXT_CHEVRON = ('<svg width="15" height="15" viewBox="0 0 24 24" fill="none" '
                'stroke="#ffffff" strokeWidth="3" strokeLinecap="round" '
                'strokeLinejoin="round" aria-hidden="true">'
                '<path d="M9 6l6 6-6 6" /></svg>')

def next_video_button(r):
    url = r.get('next_url') or ''
    if not url:
        return ''
    return (f'<a className="ck-video-next" href="{url}" '
            f'aria-label="Next video">Next Video {NEXT_CHEVRON}</a>')

def back_button(url, label):
    style = ("style={{display:'inline-block', marginBottom:'1rem', "
             "padding:'0.35rem 0.9rem', background:'#1a73e8', color:'#fff', "
             "borderRadius:'4px', textDecoration:'none', fontSize:'0.9rem'}}")
    return f'<a href="{url}" {style}>← {label}</a>'

def flex_columns(items, cols=TOC_COLUMNS):
    """Balanced side-by-side flex columns in the site home page / Photos idiom.
    `items` are bullet strings WITHOUT the leading '* '."""
    if not items:
        return ''
    k = len(items)
    per = (k + cols - 1) // cols
    chunks = [items[i:i + per] for i in range(0, k, per)] or [items]
    out = ['<div style={{ display: "flex", justifyContent: "space-between", gap: "2rem" }}>']
    for ch in chunks:
        out.append('<div style={{ flex: 1 }}>\n')
        for it in ch:
            out.append(f'* {it}')
        out.append('\n</div>')
    out.append('</div>\n')
    return '\n'.join(out)

def _plural_vid(n):
    return f'{n} video' if n == 1 else f'{n} videos'

def cluster_toc_items(n):
    """TOC bullet strings for a cluster node, in reading order: child clusters
    first (bolded, with their recursive count so a visitor sees which links go
    deeper), then this node's own video pages. A child cluster resolving to a
    single video is BYPASSED — link straight to that video page."""
    items = []
    for k in sorted([k for k in n.kids if k.rec > 0], key=lambda x: x.title):
        if k.bypass:
            t = k.bypass_target
            items.append(f'[{_vt(t, 70)}{_dur_suffix(t)}]({t["url"]})')
        else:
            items.append(f'**[{k.title}]({rel_url(k.page)})** — {_plural_vid(k.rec)}')
    for r in n.vids:
        items.append(f'[{_vt(r, 70)}{_dur_suffix(r)}]({r["url"]})')
    return items

def written_record_links(n):
    """(label, url) cross-links to the written pages this cluster mirrors:
    site_page first, then each site_level_2 section it covers."""
    out, seen = [], set()
    sp = (n.raw.get('site_page') or '').strip()
    if sp:
        p = os.path.expanduser(sp)
        p = p if os.path.isabs(p) else os.path.join(ROOT, sp)
        if os.path.exists(p) and p.startswith(DOCS):
            u = site_url(p)
            out.append((page_label(p), u)); seen.add(u)
    for s in (n.raw.get('site_level_2') or []):
        s = (s or '').strip()
        if not s:
            continue
        u = f'/{s}/overview'
        if u not in seen:
            out.append((s, u)); seen.add(u)
    return out

def baseline_cluster_prose(n):
    kids = [k for k in n.kids if k.rec > 0]
    rel = written_record_links(n)
    bits = ['{/* CK_PROSE_BASELINE */}', '']
    what = f'This section collects the video evidence the investigation has filed under **{n.title}**'
    if n.rec == 1:
        what += ' — a single clip.'
    else:
        what += f' — {n.rec} clips'
        if kids:
            what += f' across {len(kids)} sub-section' + ('s' if len(kids) != 1 else '')
        what += '.'
    bits.append(what + ' Every entry links to its own page, where the footage plays next '
                'to a write-up of what it shows, the source it came from, and what it does '
                'and does not establish.')
    bits.append('')
    bits.append('Clips are grouped here by concept rather than by date or by who posted them, '
                'so related footage sits together. Claims spoken inside the videos are the '
                'speakers’ claims, reported here with attribution rather than adopted as '
                'conclusions.')
    bits.append('')
    tail = ('Open any clip above to start.')
    if rel:
        tail += (' For the investigative context behind this footage, see '
                 + ', '.join(f'[{t}]({u})' for t, u in rel) + '.')
    bits.append(tail)
    return '\n'.join(bits) + '\n'

def related_block_cluster(n):
    lines = ['## Related Areas', '']
    for t, u in written_record_links(n):
        lines.append(f'* Written record: [{t}]({u})')
    up = rel_url(n.parent.page) if (n.parent and n.parent.rec > 0) else '/Videos/overview'
    upt = n.parent.title if (n.parent and n.parent.rec > 0) else 'Videos'
    lines.append(f'* Up: [{upt}]({up})')
    if up != '/Videos/overview':
        lines.append('* All videos: [Videos](/Videos/overview)')
    parent_kids = [k for k in (n.parent.kids if n.parent else roots) if k.rec > 0 and k is not n]
    peers = []
    for k in sorted(parent_kids, key=lambda x: x.title):
        if k.bypass:
            t = k.bypass_target
            peers.append(f'[{_vt(t, 60)}]({t["url"]})')
        else:
            peers.append(f'[{k.title}]({rel_url(k.page)})')
    if peers:
        lines += ['', '**Peer clusters:** ' + ' · '.join(peers)]
    return '\n'.join(lines)

def write_cluster_page(n):
    old = existing_fm(n.page)
    authored = old.get('ck_authored') == 'true'
    prose = extract_prose(n.page) or baseline_cluster_prose(n)
    kids = [k for k in n.kids if k.rec > 0]
    own = len(n.vids)
    _anc = _anc_titles(n)[:CL_UP[id(n)]]
    _for = n.title + (f" ({' — '.join(_anc)})" if _anc else '')
    desc = (old.get('description') if authored and old.get('description') else
            (f'Video evidence filed under {_for} in the Charlie Kirk investigation '
             f'— {n.rec} clip' + ('s' if n.rec != 1 else '')
             + (f' across {len(kids)} sub-section' + ('s' if len(kids) != 1 else '') if kids else '')
             + ' with write-ups and sources.'))
    label = old.get('sidebar_label') if authored and old.get('sidebar_label') else short_label(n.title)
    up = rel_url(n.parent.page) if (n.parent and n.parent.rec > 0) else '/Videos/overview'
    upt = n.parent.title if (n.parent and n.parent.rec > 0) else 'Videos'
    # count line, in the Photos idiom: "N on this page and M sub-sections (R in total)"
    count = f'Video evidence filed under **{n.title}** — {_plural_vid(own)} on this page'
    if kids:
        count += (f' and {len(kids)} sub-section' + ('s' if len(kids) != 1 else '')
                  + f' ({_plural_vid(n.rec)} in total)')
    count += '. Scan the list and open any clip for the footage and its write-up.'
    fm = ['---',
          'displayed_sidebar: docs',
          'slug: ' + rel_url(n.page),
          'title: ' + esc_yaml(SEO_TITLE[id(n)]),
          'sidebar_label: ' + esc_yaml(label),
          'description: ' + esc_yaml(desc),
          *(['image: ' + SHARE[id(n)]] if SHARE[id(n)] else []),
          'ck_authored: ' + ('true' if authored else 'false'),
          'ck_base_title: ' + esc_yaml(n.title),
          'ck_node_key: ' + esc_yaml(n.key),
          '---', '']
    body = [GEN_NOTE, '',
            back_button(up, upt), '',
            '# ' + n.title + ' — Videos', '',
            count, '',
            '{/* CK_TOC_START */}', '',
            flex_columns(cluster_toc_items(n)), '',
            '{/* CK_TOC_END */}', '',
            '## About This Cluster', '',
            '{/* CK_PROSE_START */}', '', prose, '', '{/* CK_PROSE_END */}', '',
            '{/* CK_NAV_START */}', '',
            related_block_cluster(n), '',
            '{/* CK_NAV_END */}', '']
    txt = re.sub(r'\n{4,}', '\n\n\n', '\n'.join(fm + body))
    os.makedirs(os.path.dirname(n.page), exist_ok=True)
    existed = os.path.exists(n.page)
    open(n.page, 'w', encoding='utf-8').write(txt)
    return existed

# ------------------------------------------------- authored titles (PRE-PASS)
# Every table of contents, peer list and pages.csv row is built from titles, so
# any title a previous run's enrichment pass authored has to be loaded BEFORE
# the first page is written. Doing it inside the emit loop would leave pages
# written earlier in the loop pointing at the old title.
authored_titles = 0
for n in pub_nodes:
    fm = existing_fm(n.page)
    if fm.get('ck_authored') == 'true' and fm.get('title'):
        # ck_base_title is the cluster's own name; `title` carries the SEO suffix.
        n.title = mdx_safe(sanitize_prose(fm.get('ck_base_title') or fm['title']))
        authored_titles += 1
for r in videos:
    fm = existing_fm(r['page'])
    if fm.get('ck_authored') == 'true' and fm.get('title'):
        r['title'] = mdx_safe(sanitize_prose(fm['title']))
        authored_titles += 1
    else:
        r['title'] = clean_title(r['v'].get('title'))
print(f'authored titles carried forward: {authored_titles}', flush=True)

# ------------------------------------------------- SEO pre-pass (CK-06, CK-07)
# Private SEO workspace patterns: CK-07 duplicate <title>s, CK-06 one og:image
# for every page, CK-05 thin descriptions. Decided before any page is written so
# every TOC, peer list and pages.csv row agrees.
from collections import Counter

def _tk(t):
    return re.sub(r'\s+', ' ', html.unescape(str(t or ''))).strip().casefold()

def _external_titles():
    """Titles of every published doc OUTSIDE this generator's pages (hand-written
    pages, the /Photos tree, and the two protected /Videos pages)."""
    out = set()
    for dp, _d, fs in os.walk(DOCS):
        inside = dp == L2DIR or dp.startswith(L2DIR + os.sep)
        for fn in fs:
            if not fn.endswith(('.md', '.mdx')):
                continue
            if inside and not (dp == L2DIR and fn in PROTECTED):
                continue
            full = os.path.join(dp, fn)
            rel = os.path.relpath(full, DOCS)
            if (any(seg.startswith('_') for seg in rel.split(os.sep)) or fn == 'CLAUDE.md'
                    or re.match(r'p_.*\.mdx?$', fn) or f'{os.sep}prompts{os.sep}' in os.sep + rel):
                continue
            t = existing_fm(full).get('title', '')
            if not t:
                m = re.search(r'^# (.+)$', open(full, encoding='utf-8', errors='replace').read(), re.M)
                t = m.group(1) if m else ''
            if t:
                out.add(_tk(t.strip("'")))
    return out

EXTERNAL_TITLES = _external_titles()

# Cluster pages: "{title} — Videos"; a generic or repeated cluster title also
# names its parent ("Other — Tyler Robinson Videos"), climbing further only
# while it still collides.
GENERIC_CLUSTER_TITLES = {'other', 'others', 'more', 'misc', 'miscellaneous', 'unfiled',
                          'general', 'various', 'additional', 'extra', 'extras'}
_ctc = Counter(_tk(n.title) for n in pub_nodes)

def _anc_titles(n):
    out, a = [], n.parent
    while a is not None:
        if a.rec > 0:
            out.append(a.title)
        a = a.parent
    return out

def _cluster_seo(n, up):
    anc = _anc_titles(n)[:up]
    if anc:
        return f"{n.title} — {' — '.join(anc)} Videos"
    return n.title if re.search(r'\bvideos$', n.title, re.I) else f'{n.title} — Videos'

CL_UP = {id(n): (1 if (_tk(n.title) in GENERIC_CLUSTER_TITLES or _ctc[_tk(n.title)] > 1) else 0)
         for n in pub_nodes}
for _round in range(12):
    _seo = {id(n): _cluster_seo(n, CL_UP[id(n)]) for n in pub_nodes}
    _cnt = Counter(_tk(x) for x in _seo.values())
    _bumped = False
    for n in pub_nodes:
        k = _tk(_seo[id(n)])
        if (_cnt[k] > 1 or k in EXTERNAL_TITLES) and CL_UP[id(n)] < len(_anc_titles(n)):
            CL_UP[id(n)] += 1
            _bumped = True
    if not _bumped:
        break
_cnt = Counter(_tk(x) for x in _seo.values())
SEO_TITLE = {}
for n in pub_nodes:
    x = _seo[id(n)]
    if _cnt[_tk(x)] > 1 or _tk(x) in EXTERNAL_TITLES:
        x = f"{x} ({n.key.replace('_', ' ')})"
    SEO_TITLE[id(n)] = x
_cluster_keys = {_tk(x) for x in SEO_TITLE.values()}

# Video pages: a title (authored or minted) that repeats another page's gets its
# cluster appended, then its position in that cluster, then its key.
def _cluster_tag(n):
    if _tk(n.title) in GENERIC_CLUSTER_TITLES:
        anc = _anc_titles(n)
        if anc:
            return f'{anc[0]} — {n.title}'
    return n.title

def _dup_video_titles():
    c = Counter(_tk(r['title']) for r in videos)
    return [r for r in videos if c[_tk(r['title'])] > 1 or _tk(r['title']) in _cluster_keys
            or _tk(r['title']) in EXTERNAL_TITLES]

retitled_videos = set()
for _step in ('cluster', 'position', 'key'):
    _dups = _dup_video_titles()
    if not _dups:
        break
    for r in _dups:
        if _step == 'cluster':
            tag = _cluster_tag(r['owner'])
            if _tk(r['title']).endswith(_tk(' — ' + tag)):
                continue
            r['title'] = f"{r['title']} — {tag}"
        elif _step == 'position':
            r['title'] = f"{r['title']} — Clip {r['owner'].vids.index(r) + 1}"
        else:
            r['title'] = f"{r['title']} ({r['key']})"
        retitled_videos.add(r['key'])

# CK-06: share image = the video's poster frame, only when that poster is
# git-tracked (the live site builds from the repo). Clusters use the first
# poster in their subtree. Banned videos never reach `videos`.
def _git_tracked_names(dirpath):
    rc, out, _ = run(['git', '-C', ROOT, 'ls-files', '--', os.path.relpath(dirpath, ROOT)], 60)
    return {os.path.basename(l) for l in out.splitlines() if l} if rc == 0 else set()

TRACKED_POSTERS = _git_tracked_names(POSTERS)
for r in videos:
    sha = r['v'].get('sha256') or ''
    r['share_image'] = (r['poster'] if r['poster'] and (sha + '.jpg') in TRACKED_POSTERS else '')

def _first_share(n):
    for r in n.vids:
        if r['share_image']:
            return r['share_image']
    for k in n.kids:
        if k.rec > 0:
            x = _first_share(k)
            if x:
                return x
    return ''
SHARE = {id(n): _first_share(n) for n in pub_nodes}

# ------------------------------------------------------------------ emit
print('writing cluster pages ...', flush=True)
c_new = c_old = 0
for n in pub_nodes:
    if write_cluster_page(n): c_old += 1
    else: c_new += 1
print('writing video pages ...', flush=True)
v_new = v_old = 0
for r in videos:
    if write_video_page(r): v_old += 1
    else: v_new += 1

# ------------------------------------------------------------- orphan sweep
keep = set(n.page for n in pub_nodes) | set(r['page'] for r in videos)
orphans = []
for dirpath, dirnames, filenames in os.walk(L2DIR):
    for f in filenames:
        p = os.path.join(dirpath, f)
        if dirpath == L2DIR and f in PROTECTED:
            continue
        if f == '_category_.json':
            continue
        if p not in keep:
            orphans.append(p)
for p in orphans:
    os.remove(p)
for dirpath, dirnames, filenames in os.walk(L2DIR, topdown=False):
    if dirpath != L2DIR and not os.listdir(dirpath):
        os.rmdir(dirpath)


# ------------------------------------------------------------------ CSS block
CSS_VIDEO = """/* CK_VIDEO_LAYOUT_START */
/* Owned by videos_planning/generator/gen_videos_pages.py. Implements
   videos_planning/layout_guidelines.txt. Do not hand-edit; do not write into
   the CK_EVIDENCE_LAYOUT or CK_PLACED_IMAGES blocks from the videos pipeline. */
.ck-video-wrap {
  position: static;
  display: block;
  margin: 0 0 1.25rem 0;
  padding: 0;
  border-radius: 0;
  background: var(--ifm-background-color);
  opacity: 1;
  z-index: 1;
  line-height: 0;
}
.ck-video-wrap .ck-video-media {
  display: block;
  border-radius: 0;
  background: #000;
  opacity: 1;
  max-width: 100%;
  max-height: calc(100vh - var(--ifm-navbar-height, 60px) - 6rem);
}
.ck-video-wrap--full {
  width: 85%;
  max-width: 85%;
  clear: both;
}
.ck-video-wrap--full .ck-video-media {
  width: 100%;
  height: auto;
}
.ck-video-wrap--wrapped {
  float: left;
  width: auto;
  max-width: 45%;
  margin: 0 1.75rem 1rem 0;
}
.ck-video-wrap--wrapped .ck-video-media {
  width: auto;
  height: calc(100vh - var(--ifm-navbar-height, 60px) - 6rem);
  max-width: 100%;
}
.ck-video-wrap--embed {
  aspect-ratio: 16 / 9;
}
.ck-video-wrap--embed .ck-video-media {
  width: 100%;
  height: 100%;
  border: 0;
}
.ck-video-wrap--pending .ck-video-media {
  width: 100%;
  height: auto;
}
.ck-video-text {
  max-width: none !important;
  width: auto !important;
  line-height: var(--ifm-line-height-base);
}
.ck-video-text::after {
  content: "";
  display: block;
  clear: both;
}
@media (max-width: 996px) {
  .ck-video-wrap--wrapped,
  .ck-video-wrap--full {
    float: none;
    width: 100%;
    max-width: 100%;
    margin: 0 0 1.25rem 0;
  }
  .ck-video-wrap--wrapped .ck-video-media {
    width: 100%;
    height: auto;
  }
}
/* The "Next Video" button (videos_planning/p_next_buttons.md) sits directly
   under the player and walks the whole corpus one clip at a time, looping the
   last video back to the first. Dark navy fill, white label, white right
   chevron. It is an immediate sibling of the player wrapper, so it inherits the
   wrapper's layout: it clears beneath a floated (vertical) player aligned to the
   clip's left edge, and drops full-width under a landscape / media-pending
   player. Its ~4px pill radius never inherits the player's border-radius:0. */
.ck-video-next {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  clear: both;
  margin: 0 0 1.25rem 0;
  padding: 0.45rem 1rem;
  background: #0d2b6b;
  color: #fff !important;
  border-radius: 4px;
  text-decoration: none;
  font-size: 0.95rem;
  font-weight: 600;
  line-height: 1.2;
}
.ck-video-next:hover,
.ck-video-next:focus {
  background: #08205a;
  color: #fff !important;
  text-decoration: none;
}
.ck-video-next:focus-visible {
  outline: 2px solid #fff;
  outline-offset: 2px;
}
.ck-video-next svg {
  display: inline-block;
  flex: none;
}
.ck-video-wrap--wrapped + .ck-video-next {
  float: left;
  clear: left;
  margin: 0 0 1.25rem 0;
}
@media (max-width: 996px) {
  .ck-video-wrap--wrapped + .ck-video-next {
    float: none;
    clear: both;
    margin: 1rem 0;
  }
}
/* CK_VIDEO_LAYOUT_END */"""

CSS_CARDS = """/* CK_PLACED_VIDEOS_START */
/* Cards placed on topic pages by the videos pipeline. Never a player: the
   player lives on the video's own page under /Videos and everything else
   links to it. */
.ck-placed-videos {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1.25rem;
  margin: 1rem 0 1.5rem 0;
}
.ck-placed-video {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--ifm-color-emphasis-300);
  background: var(--ifm-background-surface-color);
}
.ck-placed-video img {
  display: block;
  width: 100%;
  height: auto;
  border-radius: 0;
  background: #000;
}
.ck-placed-video-body {
  padding: 0.6rem 0.75rem 0.75rem 0.75rem;
  font-size: 0.9rem;
}
.ck-placed-video-title {
  font-weight: 600;
  display: block;
  margin-bottom: 0.3rem;
  line-height: 1.3;
}
.ck-placed-video-caption {
  color: var(--ifm-color-emphasis-800);
  line-height: 1.4;
}
.ck-placed-video-meta {
  margin-top: 0.4rem;
  font-size: 0.8rem;
  color: var(--ifm-color-emphasis-600);
}
/* CK_PLACED_VIDEOS_END */"""

def upsert_block(text, start, end, block):
    pat = re.compile(re.escape(start) + r'.*?' + re.escape(end), re.S)
    if pat.search(text):
        return pat.sub(lambda _: block, text, count=1)
    return text.rstrip() + '\n\n' + block + '\n'

css = open(CSSFILE, encoding='utf-8').read()
before_ev = re.search(r'/\* CK_EVIDENCE_LAYOUT_START \*/.*?/\* CK_EVIDENCE_LAYOUT_END \*/', css, re.S)
before_pi = re.search(r'/\* CK_PLACED_IMAGES_START \*/.*?/\* CK_PLACED_IMAGES_END \*/', css, re.S)
ev_snapshot = before_ev.group(0) if before_ev else None
pi_snapshot = before_pi.group(0) if before_pi else None
css = upsert_block(css, '/* CK_VIDEO_LAYOUT_START */', '/* CK_VIDEO_LAYOUT_END */', CSS_VIDEO)
css = upsert_block(css, '/* CK_PLACED_VIDEOS_START */', '/* CK_PLACED_VIDEOS_END */', CSS_CARDS)
after_ev = re.search(r'/\* CK_EVIDENCE_LAYOUT_START \*/.*?/\* CK_EVIDENCE_LAYOUT_END \*/', css, re.S)
after_pi = re.search(r'/\* CK_PLACED_IMAGES_START \*/.*?/\* CK_PLACED_IMAGES_END \*/', css, re.S)
assert (after_ev.group(0) if after_ev else None) == ev_snapshot, 'CK_EVIDENCE_LAYOUT was modified'
assert (after_pi.group(0) if after_pi else None) == pi_snapshot, 'CK_PLACED_IMAGES was modified'
open(CSSFILE, 'w', encoding='utf-8').write(css)

# ------------------------------------------------------- Level 2 landing TOC
l2 = open(L2PAGE, encoding='utf-8').read()
l2_roots = sorted([k for k in roots if k.rec > 0], key=lambda x: x.title)
l2_items = []
for k in l2_roots:
    if k.bypass:
        t = k.bypass_target
        l2_items.append(f'[{_vt(t, 70)}{_dur_suffix(t)}]({t["url"]})')
    else:
        l2_items.append(f'[{k.title}]({rel_url(k.page)}) — {_plural_vid(k.rec)}')
toc = ['{/* VIDEOS_TOC_START */}', '',
       '## Video Clusters', '',
       f'The video archive holds {len(videos)} clips filed into {len(l2_roots)} concept '
       'clusters. Open a cluster to see its clips and its sub-areas; every clip has its '
       'own page with the footage and a write-up.', '',
       flex_columns(l2_items), '',
       'Also in this section: '
       '[Buckley Carlson on the "Valhalla" comment](/Videos/buckley-carlson-kash-patel-valhalla).',
       '', '{/* VIDEOS_TOC_END */}']
toc_txt = '\n'.join(toc)
if 'VIDEOS_TOC_START' in l2:
    l2 = re.sub(r'\{/\* VIDEOS_TOC_START \*/\}.*?\{/\* VIDEOS_TOC_END \*/\}', lambda _: toc_txt, l2, flags=re.S)
else:
    m = re.search(r'^#\s+.*$', l2, re.M)
    if m:
        l2 = l2[:m.end()] + '\n\n' + toc_txt + '\n' + l2[m.end():]
    else:
        l2 = l2.rstrip() + '\n\n' + toc_txt + '\n'
open(L2PAGE, 'w', encoding='utf-8').write(l2)

# ------------------------------------------------------------------ pages.csv
rows = list(csv.DictReader(open(PAGESCSV, encoding='utf-8')))
fields = rows[0].keys() if rows else []
fields = list(csv.reader(open(PAGESCSV, encoding='utf-8')))[0]
by_key = {r['page_key']: r for r in rows}
mine = set()
added = updated = 0

def csv_row(page_key, parent_key, level, url, path, title, label, page_type, desc, lines):
    return {
        'page_key': page_key, 'parent_key': parent_key, 'level': str(level),
        'level2_parent': 'Videos', 'level2_section': 'Videos', 'page_type': page_type,
        'url_path': url, 'file_path': os.path.relpath(path, ROOT),
        'title': title, 'sidebar_label': label,
        'directory': os.path.relpath(os.path.dirname(path), DOCS),
        'extension': 'mdx', 'has_frontmatter': 'yes',
        'line_count': str(lines), 'description': desc,
    }

for n in pub_nodes:
    lines = sum(1 for _ in open(n.page, encoding='utf-8'))
    parent = n.parent.key if (n.parent and n.parent.rec > 0) else 'Videos'
    row = csv_row(n.key, parent, n.lvl, rel_url(n.page), n.page, SEO_TITLE[id(n)],
                  short_label(n.title), 'index',
                  f'Video evidence filed under {n.title}.', lines)
    mine.add(n.key)
    if n.key in by_key:
        by_key[n.key].update(row); updated += 1
    else:
        by_key[n.key] = row; rows.append(row); added += 1
for r in videos:
    lines = sum(1 for _ in open(r['page'], encoding='utf-8'))
    t = r.get('title') or clean_title(r['v'].get('title'))
    row = csv_row(r['key'], r['owner'].key, r['owner'].lvl + 1, r['url'], r['page'],
                  t, short_label(r['v'].get('title')), 'video',
                  first_sentences(r['v'].get('ai_description') or '', 1, 200)
                  or existing_fm(r['page']).get('description') or t, lines)
    mine.add(r['key'])
    if r['key'] in by_key:
        by_key[r['key']].update(row); updated += 1
    else:
        by_key[r['key']] = row; rows.append(row); added += 1

removed = 0
kept = []
for row in rows:
    fp = os.path.join(ROOT, row.get('file_path', ''))
    if row['page_key'] in mine or not fp.startswith(L2DIR + os.sep) or row['page_key'] in ('Videos', 'Videos_Buckley_Kash'):
        kept.append(row)
    else:
        removed += 1
rows = kept
with open(PAGESCSV, 'w', encoding='utf-8', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=fields, extrasaction='ignore')
    w.writeheader()
    for row in rows:
        w.writerow({k: sanitize_prose(str(row.get(k, ''))) for k in fields})

# ------------------------------------------------------------------ manifest
man = []
for r in videos:
    v = r['v']
    man.append(dict(
        key=r['key'], page=r['page'], url=r['url'], node=r['owner'].key,
        node_title=r['owner'].title, node_page=r['owner'].page,
        cid=v.get('cid') or '', sha256=v.get('sha256') or '', mode=r['mode'],
        pending_reason=r['pending_reason'], poster=r['poster'],
        title=r.get('title') or clean_title(v.get('title')),
        raw_title=v.get('title'),
        # The page's own description is the best one-line caption available: it
        # was authored against the transcript and scrubbed for safe writing,
        # whereas the raw title is whatever the poster headlined it with.
        caption=existing_fm(r['page']).get('description') or '',
        duration=v.get('duration'), file_path=v.get('file_path'),
        transcription_file=v.get('transcription_file') or '',
        ai_description_file=v.get('ai_description_file') or '',
        ocr_file=v.get('ocr_file') or '',
        source_url=v.get('source_url') or '', source_author=v.get('source_author') or '',
        source_platform=v.get('source_platform') or '',
        on_pages=[x.get('page') if isinstance(x, dict) else x for x in (v.get('on_pages') or [])],
        should_be_on_pages=[x.get('page') if isinstance(x, dict) else x
                            for x in (v.get('should_be_on_pages') or [])],
        also_nodes=[m.key for m in r['also_nodes']],
    ))
json.dump(dict(videos=man,
               nodes=[dict(key=n.key, title=n.title, level=n.lvl, page=n.page,
                           url=rel_url(n.page), rec=n.rec, bypass=n.bypass,
                           parent=(n.parent.key if n.parent else ''),
                           site_level_2=n.raw.get('site_level_2') or [],
                           site_page=n.raw.get('site_page') or '')
                      for n in pub_nodes]),
          open(OUTJSON, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

# ------------------------------------------------------------------ scan
bad = 0
for n in pub_nodes:
    validate_no_invisible(n.page)
for r in videos:
    validate_no_invisible(r['page'])
validate_no_invisible(L2PAGE)

modes = {}
for r in videos:
    modes[r['mode']] = modes.get(r['mode'], 0) + 1
pend = {}
for r in videos:
    if r['mode'] == 'pending':
        pend[r['pending_reason']] = pend.get(r['pending_reason'], 0) + 1

print('=' * 60)
print('STAGE 1-4 COMPLETE')
print(f'YAML nodes: {len(nodes)}   publishable: {len(pub_nodes)}   empty skipped: {len(empty_nodes)}')
print(f'Videos: {len(videos)} unique  (duplicate cross-filings folded: {dupes}, banned: {len(skipped_excluded)})')
print(f'Ban set: {len(excluded)} identifiers  (ban_videos.csv rows: {ban_rows}, un-banned rows honoured: {len(unbanned)})')
print(f'Cluster pages: {c_new} created, {c_old} rewritten   bypassed in nav: {len([n for n in pub_nodes if n.bypass])}')
print(f'Video pages:   {v_new} created, {v_old} rewritten')
print(f'Players: {modes.get("ipfs",0)} IPFS (pinned), {modes.get("thirdparty",0)} third-party embed, '
      f'{modes.get("link",0)} link-only, {modes.get("pending",0)} media pending {pend}')
print(f'Posters written/present: {len([r for r in videos if r["poster"]])}')
print(f'SEO: cluster titles naming a parent: {sum(1 for n in pub_nodes if CL_UP[id(n)])}; '
      f'video titles disambiguated: {len(retitled_videos)}; share images: '
      f'{sum(1 for r in videos if r["share_image"])} video pages, '
      f'{sum(1 for n in pub_nodes if SHARE[id(n)])} cluster pages')
print(f'CIDs that are not video (player withheld): {len(wrong_kind)} {wrong_kind}')
print(f'Orphans removed: {len(orphans)}')
print(f'pages.csv: {added} added, {updated} updated, {removed} stale Videos rows dropped')
print(f'Invisible-unicode findings: {bad}')
print('=' * 60)
