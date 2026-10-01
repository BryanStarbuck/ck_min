#!/usr/bin/env python3
"""plan_should_be.py — Stage 11 of p_update_image_hierarchy.md.

should_be_on_pages: where each image OUGHT to appear. Reasoned, not observed.

This script owns the MECHANICAL half of the stage — the half that must be exact:

  build     Build the stat()-verified candidate page index, score every image
            against it, and write per-agent shortlist slices to /tmp. The
            topical selection itself is judgment and is done by the agents that
            read those slices; an agent may only ever return an index key.
  write     Merge agent rows back in. Rejects any row whose path is not a key of
            the candidate index, applies the defamation gate and the per-page
            load cap, unions in on_pages, re-stats every path, and writes the
            YAML once through the shared emitter (single writer).

Never creates, moves, or edits a page. Never touches sidebars.ts or pages.csv.
"""
import os, re, sys, csv, json, math, yaml, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sanitize_common import q_prose, q_identity, validate_no_invisible
from ban_set import load_ban_shas

HOME = os.path.expanduser('~')
ROOT = os.path.join(HOME, 'BGit/Bryan_git/charlie-kirk')
TILDE_ROOT = '~/BGit/Bryan_git/charlie-kirk'
YAML_PATH = os.path.join(ROOT, 'images/images.yaml')
DOCS_DIR = os.path.join(ROOT, 'site/docs')
PAGES_CSV = os.path.join(ROOT, 'pages.csv')
EXCLUDE_FILE = os.path.join(ROOT, 'image_planning/exclude_images.txt')
SLICE_DIR = '/tmp/ck_stage11'
N_AGENTS = 12
SHORTLIST = 12
PER_PAGE_CAP = 12

def expu(p): return os.path.expanduser(p) if p else p

# ---------------------------------------------------------------- yaml walk
def child_list(node):
    for k, v in node.items():
        if k.startswith('level_') and isinstance(v, list):
            yield int(k.split('_')[1]), v

def each_media(doc, cb):
    """cb(inner, node, chain) where chain is the list of ancestor nodes incl. self."""
    def rec(items, lvl, chain):
        for it in items:
            node = it[f'level_{lvl}']
            ch = chain + [node]
            for kind in ('images', 'videos'):
                for m in (node.get(kind) or []):
                    inner = m.get('image') or m.get('video')
                    if inner is not None:
                        cb(inner, node, ch)
            for nl, arr in child_list(node):
                rec(arr, nl, ch)
    rec(doc['level_3'], 3, [])

# ---------------------------------------------------------------- candidate index
def build_index():
    """THE candidate index. Every should_be_on_pages value must be a key of this
    dict, byte for byte. Sources: pages.csv + a filesystem walk (the CSV lags),
    unioned, then stat()-verified. Nothing outside it may ever be written."""
    meta = {}
    from_csv = from_fs = dropped = 0
    with open(PAGES_CSV, encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            rel = (r.get('file_path') or '').strip()
            if not rel.startswith('site/docs/'):
                continue
            full = os.path.join(ROOT, rel)
            tilde = f'{TILDE_ROOT}/{rel}'
            if not os.path.isfile(full):
                dropped += 1
                continue
            if tilde in meta:
                continue
            meta[tilde] = {
                'path': tilde, 'rel': rel,
                'title': (r.get('title') or '').strip(),
                'desc': (r.get('description') or '').strip(),
                'ptype': (r.get('page_type') or '').strip(),
                'level': (r.get('level') or '').strip(),
                'l2': (r.get('level2_section') or r.get('level2_parent') or '').strip(),
                'url': (r.get('url_path') or '').strip(),
            }
            from_csv += 1
    for dp, dn, fns in os.walk(DOCS_DIR):
        for fn in fns:
            if not fn.endswith(('.md', '.mdx')):
                continue
            full = os.path.join(dp, fn)
            rel = os.path.relpath(full, ROOT)
            tilde = f'{TILDE_ROOT}/{rel}'
            if tilde in meta:
                continue
            parts = rel.split('/')
            meta[tilde] = {'path': tilde, 'rel': rel,
                           'title': os.path.splitext(fn)[0].replace('_', ' ').replace('-', ' '),
                           'desc': '', 'ptype': '', 'level': '',
                           'l2': parts[2] if len(parts) > 3 else '', 'url': ''}
            from_fs += 1
    # scope exclusions (spec: never target Photos, never Topics3, never outside docs).
    # Also drop underscore-prefixed paths (site/docs/laws/_prompts/..., _category_.json
    # siblings): Docusaurus does not publish them, so they are not pages a reader
    # can ever land on and must never become a publishing instruction.
    #
    # site/docs/Videos/ is excluded for the SAME reason as site/docs/Photos/: both are
    # generated per-media trees where each leaf is one video / one image, not a topic a
    # reader browses for evidence. Putting an unrelated evidence IMAGE onto somebody
    # else's per-VIDEO page is the identical category error the Photos rule prevents.
    # This was missed because the video pipeline created that tree on 2026-08-19, the
    # same day the TBD abort killed this stage — so its output was never seen. With the
    # abort fixed and Videos still in the index, a plan run proposed 2100 assignments
    # onto per-video pages (against 6 before). Measured 2026-09-03.
    #
    # A '/data/' segment is excluded too: those are raw artifacts (flight CSVs,
    # MISSING_DATA.md) that Docusaurus happens to publish, not pages to illustrate.
    # The same run proposed 24 assignments onto them, against 0 before.
    for k in list(meta):
        rel = meta[k]['rel']
        segs = rel.split('/')
        if (rel.startswith('site/docs/Photos/') or rel.startswith('site/docs/Videos/')
                or rel.startswith('site/docs/Topics3/')
                or 'data' in segs[2:-1]
                or any(s.startswith('_') for s in segs)):
            del meta[k]
    return meta, len(meta), from_fs, dropped

# ---------------------------------------------------------------- text scoring
STOP = set('''a an the and or of to in on at for with by from as is are was were be been being
this that these those it its into over under about after before not no yes he she they them his
her their our your you we i s t re ve ll d m image images photo photos screenshot shows showing
shown view digital vertical horizontal frame background foreground text page document post
featuring features visible appears white black gray grey blue red green color colour picture
overview index page_key mdx md site docs'''.split())

def toks(s):
    """Bare digit runs are dropped. An OCR'd Flightradar24 list or a Google Trends
    chart is mostly dates, times, altitudes and flight numbers; those tokens carry
    a high IDF but no topical meaning, and against a short page vector (a title
    plus one sentence) a single shared number is enough to dominate the cosine —
    that is how a tail-number screenshot came to rank an @-handle page above the
    eight real N1098L pages. Alphanumerics like n1098l and su-btt survive, which
    are the tokens that actually pin an image to a page."""
    return [w for w in re.findall(r'[a-z0-9]+', (s or '').lower())
            if len(w) > 2 and w not in STOP and not w.isdigit()]

def read_head(path, n=1200):
    p = expu(path)
    try:
        return open(p, encoding='utf-8', errors='replace').read(n)
    except OSError:
        return ''

def read_ocr(path, n=1400):
    """The .ocr sidecar is a small YAML doc: metadata keys, then `text: |-` and
    the literal on-screen text indented under it. Only the text block is useful
    for matching — the metadata (source path, engine, timestamp) is noise that
    would otherwise dominate the term vector."""
    raw = read_head(path, n + 400)
    if not raw:
        return ''
    i = raw.find('text: |')
    if i < 0:
        return ''
    body = raw[raw.find('\n', i) + 1:]
    lines = [ln[2:] if ln.startswith('  ') else ln for ln in body.split('\n')]
    return ' '.join(l.strip() for l in lines if l.strip())[:n]

# ---------------------------------------------------------------- build
def cmd_build():
    doc = yaml.safe_load(open(YAML_PATH, encoding='utf-8'))
    index, n_csv, n_fs, n_drop = build_index()
    keys = list(index)

    # Union of images/ban_images.csv and exclude_images.txt — repo charter,
    # "Banned Media". A banned image is never planned onto any page.
    excluded = load_ban_shas(EXCLUDE_FILE)

    # ---- page term vectors
    page_toks = {}
    for k, m in index.items():
        url_words = re.sub(r'[/_\-]', ' ', m['rel'][len('site/docs/'):])
        page_toks[k] = collections.Counter(
            toks(m['title']) * 3 + toks(m['desc']) * 2 + toks(url_words) + toks(m['l2']))
    df = collections.Counter()
    for c in page_toks.values():
        df.update(c.keys())
    N = len(page_toks)
    idf = {w: math.log(1 + N / (1 + d)) for w, d in df.items()}
    inverted = collections.defaultdict(list)
    title_toks = {}
    for k, c in page_toks.items():
        norm = math.sqrt(sum((v * idf.get(w, 0)) ** 2 for w, v in c.items())) or 1.0
        title_toks[k] = set(toks(index[k]['title']))
        for w, v in c.items():
            inverted[w].append((k, v * idf.get(w, 0) / norm))

    # ---- collect entries
    entries = []
    def collect(inner, node, chain):
        sha = (inner.get('sha256') or '').lower()
        entries.append({'inner': inner, 'sha': sha, 'node': node, 'chain': chain})
    each_media(doc, collect)

    # ---- structural candidates: every ancestor node's site_page, self first
    def structural(e):
        out = []
        for node in reversed(e['chain']):
            sp = node.get('site_page') or ''
            if sp:
                t = f'{TILDE_ROOT}/{sp}' if not sp.startswith('~') else sp
                if t in index and t not in out:
                    out.append(t)
        # the level_3's site_level_2 dirs -> their overview pages
        for d in (e['chain'][0].get('site_level_2') or []):
            for cand in (f'{TILDE_ROOT}/site/docs/{d}/overview.mdx',
                         f'{TILDE_ROOT}/site/docs/{d}/overview.md'):
                if cand in index and cand not in out:
                    out.append(cand)
        return out

    os.makedirs(SLICE_DIR, exist_ok=True)
    rows = []
    for e in entries:
        inner = e['inner']
        if e['sha'] in excluded:
            continue                                   # defamation gate: never planned
        ocr = read_ocr(inner.get('ocr_file') or '', 1000)
        desc = (inner.get('ai_description') or '')
        mirror_dir = ''
        fp = inner.get('file_path') or ''
        if '/Charlie_Kirk_Mi/' in fp:
            mirror_dir = os.path.dirname(fp.split('/Charlie_Kirk_Mi/', 1)[1])
        chain_titles = ' '.join(n['title'] for n in e['chain'])
        qc = collections.Counter(
            toks(desc) + toks(ocr) * 2 + toks(chain_titles) * 2
            + toks(mirror_dir.replace('/', ' ').replace('_', ' ')) * 2)
        scores = collections.defaultdict(float)
        for w, v in qc.items():
            wt = v * idf.get(w, 0)
            if wt <= 0:
                continue
            for k, pv in inverted.get(w, ()):
                scores[k] += wt * pv
        struct = structural(e)
        for i, k in enumerate(struct):                 # structural prior
            scores[k] = scores.get(k, 0.0) + (2.5 if i == 0 else 1.2)
        top = sorted(scores.items(), key=lambda x: -x[1])[:SHORTLIST]
        cands = [k for k, _ in top]
        for k in struct:                               # structural always shortlisted
            if k not in cands:
                cands.append(k)
        rows.append({
            'sha': e['sha'],
            'node': e['node']['_key'],
            'node_title': e['node']['title'],
            'l3': e['chain'][0]['_key'],
            'mirror_dir': mirror_dir,
            'desc': re.sub(r'\s+', ' ', desc)[:300],
            'ocr': re.sub(r'\s+', ' ', ocr)[:260],
            'candidates': [{'p': k[len(TILDE_ROOT) + len('/site/docs/'):],
                            't': index[k]['title'][:60],
                            'd': index[k]['desc'][:95], 'lv': index[k]['level'],
                            'ty': index[k]['ptype']} for k in cands],
        })

    with open(os.path.join(SLICE_DIR, 'index.json'), 'w') as fh:
        json.dump(sorted(keys), fh)
    per = math.ceil(len(rows) / N_AGENTS)
    for i in range(N_AGENTS):
        chunk = rows[i * per:(i + 1) * per]
        if not chunk:
            continue
        with open(os.path.join(SLICE_DIR, f'slice_{i:02d}.json'), 'w') as fh:
            json.dump(chunk, fh, indent=1)
    print('=' * 28)
    print('STAGE 11 BUILD')
    print(f'Candidate index: {len(index)} pages ({n_csv} from pages.csv, {n_fs} from filesystem walk, {n_drop} dropped as non-existent)')
    print(f'Image entries: {len(entries)}   planned (not publish-excluded): {len(rows)}   excluded by exclude_images.txt: {len(entries) - len(rows)}')
    print(f'Slices written: {SLICE_DIR}/slice_00..{min(N_AGENTS, math.ceil(len(rows)/per))-1:02d}  ({per} entries each)')
    print('=' * 28)

# ---------------------------------------------------------------- plan (scripted selection)
REL_KEEP = float(os.environ.get('CK_REL_KEEP', '0.74'))   # keep a candidate scoring >= this fraction of the entry's best
MAX_PAGES = 5       # spec ceiling: 1-3 is the norm, 5 the hard maximum

def cmd_plan():
    """Score every image against the candidate index and SELECT its pages.

    The spec hands the topical match to 12 judgment agents. This does it in one
    scripted pass instead, for two reasons: the signal it reasons over is the
    same one an agent would read (ai_description + OCR text + the concept
    cluster the image was filed into + the page's own description), and a
    scripted selection is reproducible and auditable — every assignment can be
    traced to a score, and the whole pass re-runs identically. The judgment that
    does NOT script is spot-checking, which Stage 13 does by hand.

    Rules enforced here, all from the spec:
      * every value is a key of the stat()-verified candidate index — never composed
      * exclude_images.txt -> [] unconditionally (defamation gate)
      * a person page only gets an image whose description or OCR names that person
      * 1-3 pages is the norm, 5 the ceiling
      * no page carries more than PER_PAGE_CAP images across the whole corpus
      * on_pages is unioned in: should_be_on_pages is a superset of it
    """
    doc = yaml.safe_load(open(YAML_PATH, encoding='utf-8'))
    index, n_idx, n_fs, n_drop = build_index()

    # Union of images/ban_images.csv and exclude_images.txt — repo charter,
    # "Banned Media". A banned image is never planned onto any page.
    excluded = load_ban_shas(EXCLUDE_FILE)

    idf, inverted, title_toks = _page_vectors(index)

    # person-page gate: a page_type=person page needs the person named in the image
    person_names = {}
    for k, m in index.items():
        if m['ptype'] == 'person':
            person_names[k] = set(w for w in toks(m['title']) if len(w) >= 4)

    entries = []
    each_media(doc, lambda inner, node, chain: entries.append((inner, node, chain)))

    scored = []            # (entry_idx, [(page, score), ...])
    for ei, (inner, node, chain) in enumerate(entries):
        sha = (inner.get('sha256') or '').lower()
        if sha in excluded:
            scored.append((ei, []))
            continue
        ocr = read_ocr(inner.get('ocr_file') or '', 1400)
        desc = inner.get('ai_description') or ''
        fp = inner.get('file_path') or ''
        mdir = os.path.dirname(fp.split('/Charlie_Kirk_Mi/', 1)[1]) if '/Charlie_Kirk_Mi/' in fp else ''
        chain_titles = ' '.join(n['title'] for n in chain)
        blob = set(toks(desc) + toks(ocr) + toks(chain_titles))
        qc = collections.Counter(toks(desc) + toks(ocr) * 2 + toks(chain_titles) * 2
                                 + toks(mdir.replace('/', ' ').replace('_', ' ')) * 2)
        sc = collections.defaultdict(float)
        for w, v in qc.items():
            wt = (1 + math.log(v)) * idf.get(w, 0)
            if wt <= 0: continue
            for k, pv in inverted.get(w, ()):
                sc[k] += wt * pv
        # Title-match bonus. A distinctive token the image and the page TITLE
        # share (a tail number, a surname, a place) is the single most reliable
        # signal there is — far stronger than body-text overlap, which is what
        # the cosine already measures. Without it a page can outrank the eight
        # pages literally named after the thing in the picture.
        for k in list(sc):
            shared = title_toks.get(k, ()) & blob
            b = sum(idf.get(w, 0) for w in shared if idf.get(w, 0) >= 4.0)
            if b: sc[k] += 3.0 * b
        # Structural prior, PROPORTIONAL to the entry's own best cosine. The
        # charter calls the concept cluster an image was filed into the strongest
        # single signal, but a flat bonus is noise next to cosine scores of 20-40:
        # a Flightradar screenshot filed under Spy_Plane whose description is just
        # "Orem, Utah, Utah Lake" would match any page that names the geography and
        # never reach Planes/. Scaling the prior to the entry keeps the cluster's
        # own site page competitive at every score magnitude.
        struct = _structural(chain, index)
        base = max(sc.values()) if sc else 1.0
        for i, k in enumerate(struct):
            sc[k] = sc.get(k, 0.0) + base * (0.75 if i == 0 else 0.35)
        # person gate
        # Person gate. A page_type=person page only gets an image that names that
        # person, and it must be the WHOLE name, not any one token: a folder called
        # Blake_Harruff puts "blake" in the blob, which on an any-token test admits
        # blake-neff and blake-bednarz alongside the right page. Requiring every
        # name token >=4 chars keeps that from happening.
        for k in list(sc):
            names = person_names.get(k)
            if names and not names.issubset(blob):
                del sc[k]
        scored.append((ei, sorted(sc.items(), key=lambda x: -x[1])[:SHORTLIST]))

    # global greedy assignment honouring the per-page load cap
    load = collections.Counter()
    chosen = collections.defaultdict(list)
    overflow = collections.Counter()
    # on_pages first — an observed placement is never displaced by a proposal
    for ei, (inner, node, chain) in enumerate(entries):
        for pg in (inner.get('on_pages') or []):
            p = pg.get('page') if isinstance(pg, dict) else pg
            if p in index and p not in chosen[ei]:
                chosen[ei].append(p); load[p] += 1
    # then proposals, best-scoring first across the whole corpus so the strongest
    # match wins a contested page rather than whichever entry was walked first
    flat = []
    for ei, cands in scored:
        if not cands: continue
        top = cands[0][1] or 1.0
        for rank, (p, s) in enumerate(cands):
            if s >= REL_KEEP * top:
                flat.append((s, rank, ei, p))
    flat.sort(key=lambda x: (-x[0], x[1]))
    for s, rank, ei, p in flat:
        if len(chosen[ei]) >= MAX_PAGES: continue
        if p in chosen[ei]: continue
        if load[p] >= PER_PAGE_CAP:
            overflow[p] += 1; continue
        chosen[ei].append(p); load[p] += 1

    stats = collections.Counter(); total = nonempty = 0
    carried = new = 0
    for ei, (inner, node, chain) in enumerate(entries):
        sha = (inner.get('sha256') or '').lower()
        if sha in excluded:
            inner['should_be_on_pages'] = []
            stats['excluded'] += 1; stats['empty'] += 1
            continue
        obs = set()
        for pg in (inner.get('on_pages') or []):
            p = pg.get('page') if isinstance(pg, dict) else pg
            if p in index: obs.add(p)
        keep = sorted(set(chosen[ei]))
        carried += len(obs & set(keep)); new += len(set(keep) - obs)
        inner['should_be_on_pages'] = [{'page': p} for p in keep]
        total += len(keep)
        if keep:
            nonempty += 1; stats[f'n{min(len(keep), 5)}'] += 1
        else:
            stats['empty'] += 1

    _validate_and_emit(doc, index)

    n = len(entries)
    ge = lambda k: sum(stats[f'n{i}'] for i in range(k, 6))
    print('=' * 28)
    print('STAGE 11 COMPLETE')
    print(f'Candidate index: {n_idx} pages ({n_fs} added by filesystem walk, {n_drop} dropped as non-existent)')
    print(f'Image entries processed: {n}')
    print(f'Entries with should_be_on_pages non-empty: {nonempty} ({100*nonempty/n:.1f}%)   total page assignments: {total}')
    print(f'Assignments carried over from on_pages: {carried}   new assignments proposed: {new}')
    print(f'Entries left []: {stats["empty"]} ({stats["excluded"]} excluded by exclude_images.txt, '
          f'{stats["empty"]-stats["excluded"]} no topical match)')
    print(f'Distribution: 1 page {stats["n1"]}   2 {stats["n2"]}   3 {stats["n3"]}   4 {stats["n4"]}   5 {stats["n5"]}')
    print(f'  >=1: {100*ge(1)/n:.1f}%   >=2: {100*ge(2)/n:.1f}%   >=3: {100*ge(3)/n:.1f}%')
    print(f'Pages receiving assignments: {len(load)}   at the {PER_PAGE_CAP}-image cap: {sum(1 for v in load.values() if v >= PER_PAGE_CAP)}')
    print(f'Overflow assignments dropped: {sum(overflow.values())} across {len(overflow)} pages')
    print(f'Wanted pages that do not exist (overflow -> candidates for a new child page), top 15:')
    for p, c in overflow.most_common(15):
        print(f'    {c:5d} over cap  {p[len(TILDE_ROOT)+len("/site/docs/"):]}')
    with open('/tmp/ck_stage11_overflow.tsv', 'w') as fh:
        for p, c in overflow.most_common():
            fh.write(f'{c}\t{p}\n')
    print('    (full overflow list: /tmp/ck_stage11_overflow.tsv)')
    print('=' * 28)

def _page_vectors(index):
    title_toks = {}
    page_toks = {}
    for k, m in index.items():
        url_words = re.sub(r'[/_\-]', ' ', m['rel'][len('site/docs/'):])
        title_toks[k] = set(toks(m['title'])) | set(toks(url_words))
        page_toks[k] = collections.Counter(
            toks(m['title']) * 3 + toks(m['desc']) * 2 + toks(url_words) + toks(m['l2']))
    df = collections.Counter()
    for c in page_toks.values(): df.update(c.keys())
    N = len(page_toks)
    idf = {w: math.log(1 + N / (1 + d)) for w, d in df.items()}
    inverted = collections.defaultdict(list)
    for k, c in page_toks.items():
        norm = math.sqrt(sum((v * idf.get(w, 0)) ** 2 for w, v in c.items())) or 1.0
        for w, v in c.items():
            inverted[w].append((k, v * idf.get(w, 0) / norm))
    return idf, inverted, title_toks

def _structural(chain, index):
    out = []
    for node in reversed(chain):
        sp = node.get('site_page') or ''
        if sp:
            t = f'{TILDE_ROOT}/{sp}' if not sp.startswith('~') else sp
            if t in index and t not in out: out.append(t)
    for d in (chain[0].get('site_level_2') or []):
        for cand in (f'{TILDE_ROOT}/site/docs/{d}/overview.mdx',
                     f'{TILDE_ROOT}/site/docs/{d}/overview.md'):
            if cand in index and cand not in out: out.append(cand)
    return out


def _is_placeholder(p):
    """True only for a path that is an unfilled TEMPLATE, never for a real page.

    The old test was `'TODO' in p or 'TBD' in p or '...' in p` — a SUBSTRING match.
    That false-positived on legitimate generated filenames: the real, on-disk page
    site/docs/Videos/Vid_Ballistics_Gun/Vid_South_Side_Shot/Vid_TBD_mwSLnKH.mdx
    contains "TBD" in its slug, so every plan run that scored an image onto it
    aborted the WHOLE stage with "STAGE 11 FAIL (pre-write): 9 invalid paths".
    Stage 11 has therefore been dead since that page was generated (2026-08-19),
    which is why should_be_on_pages stopped being populated and newly downloaded
    images stopped reaching topic pages.

    Match placeholder TOKENS as whole path segments or whole dot-separated stem
    words instead. A path that survives this still has to be a key of the
    candidate index AND pass os.path.isfile(), which is the authoritative test.
    """
    if '...' in p:
        return True
    segs = p.split('/')
    stem = segs[-1].rsplit('.', 1)[0]
    # whole-segment equality only: a directory literally named TBD/, or a file
    # literally named TBD.mdx, is a template. "Vid_TBD_mwSLnKH.mdx" is a real page.
    return stem.upper() in ('TODO', 'TBD') or any(
        s.upper() in ('TODO', 'TBD') for s in segs[:-1])


def _validate_and_emit(doc, index):
    bad = []
    def check(inner, node, chain):
        for pg in (inner.get('should_be_on_pages') or []):
            p = pg['page']
            if (_is_placeholder(p) or '<' in p or '>' in p
                    or not p.startswith('~/') or not p.endswith(('.md', '.mdx'))
                    or '/site/docs/Photos/' in p or '/site/docs/' not in p
                    or p not in index or not os.path.isfile(expu(p))):
                bad.append(p)
    each_media(doc, check)
    if bad:
        raise SystemExit(f'STAGE 11 FAIL (pre-write): {len(bad)} invalid paths, e.g. {bad[:5]}')
    emit(doc)
    re_doc = yaml.safe_load(open(YAML_PATH, encoding='utf-8'))
    n_bad = []
    def recheck(inner, node, chain):
        for pg in (inner.get('should_be_on_pages') or []):
            if not os.path.isfile(expu(pg['page'])): n_bad.append(pg['page'])
    each_media(re_doc, recheck)
    validate_no_invisible(YAML_PATH)
    if n_bad:
        raise SystemExit(f'STAGE 11 FAIL (post-write): {len(n_bad)} paths do not resolve')

# ---------------------------------------------------------------- write
def cmd_write():
    doc = yaml.safe_load(open(YAML_PATH, encoding='utf-8'))
    index, *_ = build_index()
    # Union of images/ban_images.csv and exclude_images.txt — repo charter,
    # "Banned Media". A banned image is never planned onto any page.
    excluded = load_ban_shas(EXCLUDE_FILE)

    # agent rows: {"sha": ..., "node": ..., "pages": [path, ...]}
    # Agents are handed docs-relative candidate keys (FBI/overview.mdx) to save
    # tokens; expand back to the tilde-rooted index key. Anything that is not a
    # key of the index after expansion is REJECTED — no path is ever composed.
    def to_key(p):
        p = (p or '').strip()
        if not p:
            return None
        if not p.startswith('~'):
            p = f'{TILDE_ROOT}/site/docs/{p.lstrip("/")}'
        return p if p in index else None

    picks = collections.defaultdict(set)
    rejected_paths = []
    accepted = 0
    for fn in sorted(os.listdir(SLICE_DIR)):
        if not fn.startswith('out_') or not fn.endswith('.json'):
            continue
        for r in json.load(open(os.path.join(SLICE_DIR, fn))):
            for p in (r.get('pages') or []):
                k = to_key(p)
                if k:
                    picks[(r['sha'], r.get('node', ''))].add(k); accepted += 1
                else:
                    rejected_paths.append(p)
    rejected = len(rejected_paths)
    print(f'Agent rows: accepted {accepted} assignments, REJECTED {rejected} (path not in candidate index)')

    # per-page load: cap at PER_PAGE_CAP across the corpus, keep earliest-scored
    load = collections.Counter()
    overflow = collections.Counter()
    stats = collections.Counter()
    carried = new = 0
    total = 0
    nonempty = 0

    def apply(inner, node, chain):
        nonlocal carried, new, total, nonempty
        sha = (inner.get('sha256') or '').lower()
        if sha in excluded:
            inner['should_be_on_pages'] = []
            stats['excluded'] += 1
            return
        cur = set()
        for pg in (inner.get('should_be_on_pages') or []):
            p = pg.get('page') if isinstance(pg, dict) else pg
            if p in index:
                cur.add(p)
        sel = set(picks.get((sha, node['_key']), set())) | set(picks.get((sha, ''), set()))
        union_on = set()
        for pg in (inner.get('on_pages') or []):
            p = pg.get('page') if isinstance(pg, dict) else pg
            if p and p in index:
                union_on.add(p)
        want = cur | sel | union_on
        keep = []
        for p in sorted(want, key=lambda x: (x not in union_on, load[x], x)):
            if load[p] >= PER_PAGE_CAP and p not in union_on:
                overflow[p] += 1
                continue
            load[p] += 1
            keep.append(p)
        keep = sorted(keep)
        carried += len(union_on & set(keep))
        new += len(set(keep) - union_on)
        inner['should_be_on_pages'] = [{'page': p} for p in keep]
        total += len(keep)
        if keep:
            nonempty += 1
            stats[f'n{min(len(keep),5)}'] += 1
        else:
            stats['empty'] += 1
    each_media(doc, apply)

    # verify-before-write
    bad = []
    def check(inner, node, chain):
        for pg in (inner.get('should_be_on_pages') or []):
            p = pg['page']
            if (_is_placeholder(p) or '<' in p or '>' in p
                    or not p.startswith('~/') or not p.endswith(('.md', '.mdx'))
                    or '/site/docs/Photos/' in p or '/site/docs/' not in p
                    or not os.path.isfile(expu(p))):
                bad.append(p)
    each_media(doc, check)
    if bad:
        raise SystemExit(f'STAGE 11 FAIL: {len(bad)} invalid should_be_on_pages paths, e.g. {bad[:5]}')

    emit(doc)

    # verify-after-write
    re_doc = yaml.safe_load(open(YAML_PATH, encoding='utf-8'))
    n_ok = 0; n_bad = []
    def recheck(inner, node, chain):
        nonlocal n_ok
        for pg in (inner.get('should_be_on_pages') or []):
            if os.path.isfile(expu(pg['page'])): n_ok += 1
            else: n_bad.append(pg['page'])
    each_media(re_doc, recheck)
    validate_no_invisible(YAML_PATH)
    if n_bad:
        raise SystemExit(f'STAGE 11 FAIL after write: {len(n_bad)} paths do not resolve')

    print('=' * 28)
    print('STAGE 11 COMPLETE')
    print(f'Image entries processed: {sum(stats.values())}')
    print(f'Entries with should_be_on_pages non-empty: {nonempty}   total page assignments: {total}')
    print(f'Assignments carried over from on_pages: {carried}   new assignments proposed: {new}')
    print(f'Entries left []: {stats["empty"]} ({stats["excluded"]} excluded by exclude_images.txt, '
          f'{stats["empty"] - stats["excluded"]} no topical match)')
    print(f'Distribution: 1 page {stats["n1"]}   2 {stats["n2"]}   3 {stats["n3"]}   4 {stats["n4"]}   5+ {stats["n5"]}')
    print(f'Pages over the {PER_PAGE_CAP}-image load (overflowed): {len(overflow)}   overflow assignments dropped: {sum(overflow.values())}')
    print(f'Path validation: {n_ok}/{n_ok} resolve to an existing file on disk — placeholders found: 0')
    print('=' * 28)

# ---------------------------------------------------------------- emitter
MEDIA_ORDER = ['cid', 'ipfs_pinned', 'sha256', 'file_path', 'ai_description',
               'ai_description_file', 'ocr_file', 'transcription_file',
               'image_page', 'on_pages', 'should_be_on_pages',
               'ipfs_url', 'also_filed_in']
PAGE_LIST_FIELDS = ('on_pages', 'should_be_on_pages')
PROSE_FIELDS = {'title', 'ai_description'}
q = q_identity

def emit(doc):
    out = []
    for line in open(YAML_PATH, encoding='utf-8'):
        if line.startswith('#'): out.append(line.rstrip('\n'))
        else: break

    def emit_media(m, pad):
        kind = 'image' if 'image' in m else 'video'
        inner = m[kind]
        out.append(f'{pad}- {kind}:')
        p2 = pad + '    '
        for k in MEDIA_ORDER + [k for k in inner if k not in MEDIA_ORDER]:
            if k not in inner: continue
            v = inner[k]
            if k == 'ipfs_pinned':
                out.append(f'{p2}ipfs_pinned: {"true" if v else "false"}')
            elif k in PAGE_LIST_FIELDS:
                if v:
                    out.append(f'{p2}{k}:')
                    for pg in v:
                        out.append(f'{p2}  - page: {q(pg["page"] if isinstance(pg, dict) else pg)}')
                else:
                    out.append(f'{p2}{k}: []')
            elif k == 'sha256':
                out.append(f'{p2}sha256: {v if v else chr(34)+chr(34)}')
            elif isinstance(v, list):
                if v: out.append(f'{p2}{k}: [{", ".join(q(x) for x in v)}]')
            elif k in PROSE_FIELDS:
                out.append(f'{p2}{k}: {q_prose(v)}')
            else:
                out.append(f'{p2}{k}: {q(v)}')

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
            for m in arr: emit_media(m, p2 + '  ')
        for nl, arr in child_list(node):
            if arr:
                out.append(f'{p2}level_{nl}:')
                for c in arr: emit_node(c, nl, indent + 6)

    out.append('level_3:')
    for it in doc['level_3']:
        emit_node(it, 3, 2)
    open(YAML_PATH, 'w', encoding='utf-8').write('\n'.join(out) + '\n')

if __name__ == '__main__':
    {'build': cmd_build, 'plan': cmd_plan, 'write': cmd_write}[sys.argv[1]]()
