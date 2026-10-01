#!/usr/bin/env python3
# plan_should_be.py — STAGE 13 of p_update_video_hierarchy.md.
#
# should_be_on_pages: where each video OUGHT to appear. REASONED, not observed.
# This script places NOTHING on any page — it records the plan that
# p_yaml_to_site.md Stage 6 later executes.
#
# The images pipeline scored stills lexically and hand-audited its own precision
# at 65-70%. Video is different in one decisive way: the claim is SPOKEN, and the
# .transcription sidecar is a verbatim record of it. So the transcription body is
# the heaviest term source here, and the vision model's prose is secondary.
#
# Every value written is COPIED from the candidate index — a stat()'d union of
# pages.csv and a filesystem walk. No path is ever composed, guessed, or
# abbreviated.
import os, re, csv, sys, json, math, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.expanduser('~/BGit/Bryan_git/charlie-kirk')
DOCS = os.path.join(ROOT, 'site/docs')
PAGES_CSV = os.path.join(ROOT, 'pages.csv')
EXCLUDE_FILE = os.path.join(HERE, '..', 'exclude_videos.txt')
TILDE_ROOT = '~/BGit/Bryan_git/charlie-kirk'

# Quantity rules, deliberately tighter than the images pipeline's. A placed
# still costs a few hundred kilobytes off the site's own static directory; a
# placed video costs a public IPFS gateway fetch, and this corpus runs from
# 0.5MB to 3GB.
MAX_PAGES     = 4      # hard ceiling; 1-3 is the norm
PER_PAGE_CAP  = 6      # no page carries more than six videos corpus-wide
# A Level 2 overview gets a video only when it is emblematic of the WHOLE
# section — the one clip a reader landing cold should be offered. One, not six.
PER_PAGE_CAP_L2 = 1
SHORTLIST     = 12
REL_KEEP      = 0.62   # keep a candidate scoring at least this share of the best
# Below this many distinct informative tokens across the transcript body and the
# vision model's overview, a video has no usable lexical signal.
MIN_SIGNAL_TOKENS = 12

STOP = set('''the a an and or of to in on at for with from by is are was were be been
this that these those it its as not no but if then than so such which who whom whose
what when where why how all any both each few more most other some only own same too
very can will just should now about into over under again further once here there
he she they them his her their our your you we i s t re ve ll d m video videos clip
clips footage watch watching shows showing shown says say said speaker speaking talks
frame frames camera scene screen split vertical horizontal seconds minute minutes
overview index page_key mdx md site docs charlie kirk'''.split())

def toks(s):
    """Bare digit runs are dropped: a transcript is full of times, dates, case
    numbers and dollar figures that carry high IDF and no topical meaning.
    Alphanumerics like n1098l and su-btt survive, and those are exactly the
    tokens that pin a video to a page."""
    return [w for w in re.findall(r'[a-z0-9]+', (s or '').lower())
            if len(w) > 2 and w not in STOP and not w.isdigit()]

def expu(p):
    return os.path.expanduser(p) if p else p

# ---------------------------------------------------------------------------
# THE CANDIDATE INDEX. The only legal source of a should_be_on_pages value.
def build_index():
    cand = {}
    for r in csv.DictReader(open(PAGES_CSV, encoding='utf-8')):
        cand[f"{TILDE_ROOT}/{r['file_path']}"] = dict(
            title=r['title'], desc=r['description'], url=r['url_path'],
            sec=r['level2_section'], ptype=r['page_type'], level=r['level'],
            key=r['page_key'])
    from_csv = len(cand)
    walked = 0
    for dirpath, dirnames, filenames in os.walk(DOCS):
        dirnames[:] = [d for d in dirnames if not d.startswith('.')]
        for fn in filenames:
            if not fn.endswith(('.md', '.mdx')):
                continue
            full = os.path.join(dirpath, fn)
            t = f"{TILDE_ROOT}/{os.path.relpath(full, ROOT)}"
            if t not in cand:
                rel = os.path.relpath(full, DOCS)
                cand[t] = dict(title=os.path.splitext(os.path.basename(rel))[0]
                               .replace('-', ' ').replace('_', ' '),
                               desc='', url='/' + os.path.splitext(rel)[0],
                               sec=rel.split(os.sep)[0], ptype='', level='',
                               key='')
                walked += 1
    # scope exclusions, then stat() every survivor
    dropped = 0
    out = {}
    for t, m in cand.items():
        p = expu(t)
        if not os.path.exists(p):
            dropped += 1
            continue
        rel = os.path.relpath(p, ROOT)
        if rel.startswith('site/docs/Videos/') or rel.startswith('site/docs/Photos/') \
           or rel.startswith('site/docs/Topics3/'):
            continue
        if not rel.startswith('site/'):
            continue
        out[t] = m
    return out, from_csv, walked, dropped

index, n_csv, n_walk, n_dropped = build_index()

# ---------------------------------------------------------------------------
# page vectors
def page_vectors(index):
    docs, title_toks = {}, {}
    for k, m in index.items():
        tt = toks(m['title'])
        title_toks[k] = set(tt)
        body = tt * 3 + toks(m['desc']) * 2 + \
            toks(m['url'].replace('/', ' ').replace('-', ' ').replace('_', ' ')) + \
            toks(m['sec'].replace('_', ' '))
        docs[k] = collections.Counter(body)
    N = len(docs)
    df = collections.Counter()
    for c in docs.values():
        df.update(c.keys())
    idf = {w: math.log(1 + N / (1 + d)) for w, d in df.items()}
    inverted = collections.defaultdict(list)
    for k, c in docs.items():
        norm = math.sqrt(sum((v * idf.get(w, 0)) ** 2 for w, v in c.items())) or 1.0
        for w, v in c.items():
            inverted[w].append((k, v * idf.get(w, 0) / norm))
    return idf, inverted, title_toks

idf, inverted, title_toks = page_vectors(index)

# person pages need the WHOLE name present, not any one token
person_names = {k: {w for w in toks(m['title']) if len(w) >= 4}
                for k, m in index.items() if m['ptype'] == 'person'}

# ---------------------------------------------------------------------------
# inputs
inv = {r['vkey']: r for r in
       csv.DictReader(open(os.path.join(HERE, 'inventory.tsv'), encoding='utf-8'),
                      delimiter='\t')}
side = json.load(open(os.path.join(HERE, 'sidecars.json'), encoding='utf-8'))
cids = json.load(open(os.path.join(HERE, 'cids.json'), encoding='utf-8'))['entries']
tree = json.load(open(os.path.join(HERE, 'tree.json'), encoding='utf-8'))
nodes = tree['nodes']
on_pages = json.load(open(os.path.join(HERE, 'on_pages.json'), encoding='utf-8'))
prev = {}
outp = os.path.join(HERE, 'should_be_on_pages.json')
if os.path.exists(outp):
    prev = json.load(open(outp, encoding='utf-8'))

excluded = set()
if os.path.exists(EXCLUDE_FILE):
    for line in open(EXCLUDE_FILE, encoding='utf-8'):
        line = line.split('#', 1)[0].strip()
        if line:
            excluded.add(line)

# node ancestry for the structural prior
parent_of = {k: n['parent'] for k, n in nodes.items()}
def ancestry(nk):
    out = []
    while nk:
        out.append(nk)
        nk = parent_of.get(nk)
    return out

video_node = {}
for nk, n in nodes.items():
    for v in n['videos']:
        video_node[v] = nk

# ---------------------------------------------------------------------------
# CLUSTER -> SITE PAGE. A corpus cluster ("The SU-BTT Aircraft", "The Pellet Gun
# Man") has no site_page of its own, only its section's Level 2 overview — and
# that overview takes one video, not six. So bind each cluster ONCE to the site
# page inside its section whose title best matches the cluster's concept, and
# let every video in the cluster inherit it.
#
# This is the unit of judgment that actually works here. The cluster map was
# authored by hand from the mirror's own years of concept filing, so a cluster
# name is a reliable statement of what its footage is about, while an individual
# video's transcript is often ambient crowd audio. 131 cluster decisions are also
# reviewable in a way 412 per-video decisions are not.
CLUSTER_PAGE = {}
def bind_cluster_pages():
    for nk, n in nodes.items():
        if not n['videos'] or n['site_page']:
            continue
        # the section this cluster hangs under
        sec = ''
        a = nk
        while a:
            if nodes[a]['site_level_2']:
                sec = nodes[a]['site_level_2'][0]
                break
            a = parent_of.get(a)
        if not sec:
            continue
        ct = set(toks(n['title']))
        # a split cluster ("... (Part 3)") inherits its parent's concept
        par = parent_of.get(nk)
        if par and nodes[par]['videos'] == [] and 'Part' in n['title']:
            ct |= set(toks(nodes[par]['title']))
        best, best_s = '', 0.0
        for k, m in index.items():
            if m['sec'] != sec or m['level'] == '2':
                continue
            pt = title_toks.get(k, set())
            shared = ct & pt
            sc_ = sum(idf.get(w, 0) for w in shared)
            # ONE distinctive shared token is enough here, because both sides are
            # titles: "The SU-BTT Aircraft" and the page "SU-BTT" share exactly
            # one token and are obviously the same subject. Requiring two would
            # reject most true matches.
            distinctive = [w for w in shared if idf.get(w, 0) >= 4.0]
            if distinctive and sc_ > best_s:
                best, best_s = k, sc_
        if best:
            CLUSTER_PAGE[nk] = best

def structural_pages(nk):
    """The site pages the video's own cluster and its ancestors point at,
    nearest first."""
    out = []
    if CLUSTER_PAGE.get(nk):
        out.append(CLUSTER_PAGE[nk])
    for a in ancestry(nk):
        n = nodes[a]
        sp = CLUSTER_PAGE.get(a) or n['site_page']
        if sp:
            t = f'{TILDE_ROOT}/{sp}'
            if t in index and t not in out:
                out.append(t)
        for sec in n['site_level_2']:
            for t, m in index.items():
                if m['sec'] == sec and m['level'] == '2' and t not in out:
                    out.append(t)
    return out

bind_cluster_pages()

# ---------------------------------------------------------------------------
# score
scored = {}
no_signal = []
low_signal = []
for vkey in inv:
    e = cids.get(vkey, {})
    if e.get('cid') in excluded or (e.get('sha256') or '') in excluded:
        scored[vkey] = []
        continue
    s = side.get(vkey, {})
    t = s.get('transcription') or {}
    a = s.get('ai_description') or {}
    o = s.get('ocr') or {}
    r = inv[vkey]
    nk = video_node.get(vkey, '')
    chain_titles = ' '.join(nodes[x]['title'] for x in ancestry(nk)) if nk else ''
    mdir = (r.get('mirror_dir') or '').replace('/', ' ').replace('_', ' ')

    # THE TRANSCRIPTION IS THE HEAVIEST INPUT. What the speaker asserts usually
    # decides the page — a four-minute monologue about the microphone belongs on
    # the Mic pages even when the footage is a talking head.
    body = (t.get('body') or '')[:20000]
    # CLAIM TOKENS vs SCENE TOKENS. The transcript, the manifest description and
    # the capture filename say what the video is ABOUT; the vision model's prose
    # says what is on screen, and on screen is very often just a host at a desk
    # or a stretch of suburban street. Scene tokens corroborate a placement; they
    # must never drive one, or a security-camera clip of a quiet street lands on
    # the exploding-mic page because both mention a house and a morning.
    stem_words = os.path.splitext(r.get('basename', '') or '')[0]
    claim_src = (toks(body) * 4
                 + toks(r.get('manifest_description', '')) * 3
                 + toks(stem_words.replace('_', ' ')) * 2
                 + toks(chain_titles) * 3
                 + toks(mdir) * 3)
    scene_src = (toks(a.get('overview', ''))
                 + toks(a.get('people', ''))
                 + toks(a.get('onscreen', ''))
                 + toks((o.get('text') or '')[:4000]))
    # OCR and the vision model's on-screen-text section are LITERAL glyphs burned
    # into the frame — a slide title, a chyron, a case number. That is evidence of
    # what the video is about, unlike the prose describing the room it was shot
    # in, so it counts on the claim side.
    literal_src = (toks(a.get('onscreen', '')) + toks((o.get('text') or '')[:4000]))
    claim_blob = set(claim_src) | set(literal_src)
    qc = collections.Counter(claim_src + scene_src)
    blob = set(qc)
    if not blob:
        no_signal.append(vkey)

    sc = collections.defaultdict(float)
    for w, v in qc.items():
        # sublinear term frequency: a transcript repeats its subject dozens of
        # times and raw counts would swamp everything else
        wt = (1 + math.log(v)) * idf.get(w, 0)
        if wt <= 0:
            continue
        for k, pv in inverted.get(w, ()):
            sc[k] += wt * pv

    # title-match bonus on a distinctive shared token — the strongest single
    # signal available
    for k in list(sc):
        shared = title_toks.get(k, set()) & blob
        b = sum(idf.get(w, 0) for w in shared if idf.get(w, 0) >= 4.0)
        if b:
            sc[k] += 3.0 * b

    # structural prior, PROPORTIONAL to this entry's own best score
    base = max(sc.values()) if sc else 1.0
    for i, k in enumerate(structural_pages(nk)):
        sc[k] = sc.get(k, 0.0) + base * (0.75 if i == 0 else 0.35)

    # DEFAMATION GATE — person pages
    for k in list(sc):
        names = person_names.get(k)
        if names and not names.issubset(blob):
            del sc[k]

    # ------------------------------------------------------------------
    # EVIDENCE GATES. The hand audit in Stage 15 put the first cut of this
    # stage at 4/10: every miss was a video with little or no SPEECH, whose
    # score therefore came from generic scenery tokens in the vision model's
    # prose ("a suburban street", "a police arrest") or, worse, from the
    # structural prior alone. Two gates fix that class of error.
    #
    # Gate 1 — DISTINCTIVE TOKEN. A page that is not this video's own
    # structural page must share at least one DISTINCTIVE token with it
    # (idf >= 4: a surname, a tail number, a place, a piece of hardware).
    # Overlap on common investigation vocabulary is not evidence — every page
    # on this site is about the same event.
    struct_set = set(structural_pages(nk))
    for k in list(sc):
        if k in struct_set:
            continue
        shared = title_toks.get(k, set()) & blob
        # The bar for a NON-structural page is deliberately high. The hand audit
        # measured the first cuts of this stage at 4/10 and then 2/10: a
        # transcript of ambient crowd audio at UVU has hundreds of words and no
        # topical content, and against 1,495 pages about one event, weak overlap
        # always finds something. So a lexical proposal must share at least TWO
        # distinctive tokens (idf >= 4) with the page's own TITLE, drawn from the
        # claim side. That is roughly "the video and the page name the same two
        # specific things" — a surname and a place, a tail number and an agency.
        # Everything softer than that is left to the structural placement, which
        # comes from the hand-authored cluster map and is far more reliable.
        title_distinctive = {w for w in (title_toks.get(k, set()) & claim_blob)
                             if idf.get(w, 0) >= 4.0}
        if len(title_distinctive) < 2:
            del sc[k]

    # Gate 2 — MINIMUM SPEECH/DESCRIPTION EVIDENCE. Below this the lexical
    # score is noise. Such a video keeps only its nearest structural page (the
    # cluster it was filed into is still a real signal) and nothing else, and
    # gets [] when its cluster has no site page at all.
    # the evidence floor is measured on the CLAIM side too: a rich description of
    # a generic scene is not evidence of what the video is about
    signal = len(claim_blob)
    if signal < MIN_SIGNAL_TOKENS:
        near = structural_pages(nk)[:1]
        sc = {k: v for k, v in sc.items() if k in near}
        low_signal.append(vkey)

    scored[vkey] = sorted(sc.items(), key=lambda x: -x[1])[:SHORTLIST]

# ---------------------------------------------------------------------------
# assignment: observed placements first, then proposals best-score-first
load = collections.Counter()
chosen = collections.defaultdict(list)
overflow = collections.Counter()
carried = 0
# THE UNION RULE: should_be_on_pages is a SUPERSET of on_pages. A page in
# on_pages is dropped only when the video genuinely does not belong there,
# and every such subtraction is recorded with its reason.
subtractions = []

def cap_for(p):
    return PER_PAGE_CAP_L2 if index[p]['level'] == '2' else PER_PAGE_CAP

for vkey in inv:
    if scored.get(vkey) == [] and (cids.get(vkey, {}).get('cid') in excluded):
        continue
    for p in on_pages.get(vkey, []):
        if p in index and p not in chosen[vkey]:
            chosen[vkey].append(p)
            load[p] += 1
            carried += 1
        elif p not in index:
            pe = expu(p)
            if '/site/docs/Photos/' in pe:
                why = ('the page is under site/docs/Photos — the images '
                       'pipeline\'s output, which Stage 13 may not target')
            elif '/site/docs/Videos/' in pe:
                why = ('the page is under site/docs/Videos — that Level 2 is '
                       'the video hierarchy itself; its own page is video_page')
            elif '/site/docs/Topics3/' in pe:
                why = 'Topics3 is template scaffolding, not part of this hierarchy'
            elif not os.path.exists(pe):
                why = 'the page no longer exists on disk'
            else:
                why = 'outside the candidate index (not a published site page)'
            subtractions.append((vkey, p, why))
    # an earlier run's plan is merged, never clobbered
    for p in prev.get(vkey, []):
        if p in index and p not in chosen[vkey] and len(chosen[vkey]) < MAX_PAGES:
            chosen[vkey].append(p)
            load[p] += 1

flat = []
for vkey, cands in scored.items():
    if not cands:
        continue
    top = cands[0][1] or 1.0
    for rank, (p, s) in enumerate(cands):
        if s >= REL_KEEP * top:
            flat.append((s, rank, vkey, p))
flat.sort(key=lambda x: (-x[0], x[1]))

new_assigned = 0
for s, rank, vkey, p in flat:
    if len(chosen[vkey]) >= MAX_PAGES:
        continue
    if p in chosen[vkey]:
        continue
    if load[p] >= cap_for(p):
        overflow[p] += 1
        continue
    chosen[vkey].append(p)
    load[p] += 1
    new_assigned += 1

# ---------------------------------------------------------------------------
# VERIFY BEFORE WRITE
final = {}
bad = []
for vkey in inv:
    pages = chosen.get(vkey, [])
    e = cids.get(vkey, {})
    if e.get('cid') in excluded or (e.get('sha256') or '') in excluded:
        final[vkey] = []
        continue
    keep = []
    for p in pages:
        if p not in index:
            bad.append((vkey, p, 'not in candidate index'))
            continue
        if not os.path.exists(expu(p)):
            bad.append((vkey, p, 'does not exist on disk'))
            continue
        if re.search(r'\.\.\.|TODO|TBD|[<>]', p):
            bad.append((vkey, p, 'placeholder token'))
            continue
        if not p.startswith('~/') or not p.endswith(('.md', '.mdx')):
            bad.append((vkey, p, 'not an absolute tilde path ending .md/.mdx'))
            continue
        keep.append(p)
    final[vkey] = keep

if bad:
    print('STAGE 13 FAILED — invalid paths selected:')
    for b in bad[:20]:
        print('   ', b)
    raise SystemExit(1)

json.dump(final, open(outp, 'w', encoding='utf-8'), indent=1)
json.dump([dict(vkey=v, page=p, reason=w) for v, p, w in subtractions],
          open(os.path.join(HERE, 'subtractions.json'), 'w', encoding='utf-8'),
          indent=1)

# ---------------------------------------------------------------------------
n = len(final)
nonempty = sum(1 for v in final.values() if v)
ge2 = sum(1 for v in final.values() if len(v) >= 2)
empty = n - nonempty
total_assign = sum(len(v) for v in final.values())
by_level = collections.Counter()
for v in final.values():
    for p in v:
        by_level[index[p]['level']] += 1
noplay = sum(1 for k, v in final.items() if v and not cids.get(k, {}).get('cid'))
unpinned_plan = sum(1 for k, v in final.items()
                    if v and not cids.get(k, {}).get('ipfs_pinned'))
on_empty = sum(1 for k in final if not on_pages.get(k))

pct = lambda x: f'{100.0*x/n:.0f}%'
targets_ok = (5 <= 100.0*empty/n <= 25) and (100.0*nonempty/n >= 75) \
             and (100.0*ge2/n >= 20) and on_empty < n

print('============================')
print('STAGE 13 COMPLETE')
print(f'Candidate index: {len(index)} pages ({n_csv} from pages.csv, {n_walk} '
      f'from filesystem walk, {n_dropped} dropped as non-existent)')
print(f'Video entries processed: {n}')
print(f'Entries with should_be_on_pages non-empty: {nonempty}   '
      f'total page assignments: {total_assign}')
print(f'Assignments carried over from on_pages: {carried}   '
      f'new assignments proposed: {new_assigned}')
print(f'Subtractions from on_pages (wrong placements, with reasons): '
      f'{len(subtractions)}')
for vk, p, why in subtractions[:20]:
    print(f'   {vk[:40]:40s} {p.split("charlie-kirk/")[-1][:58]:58s} — {why}')
print(f'Entries left [] : {empty} '
      f'({len([1 for k in final if cids.get(k,{}).get("cid") in excluded])} '
      f'excluded by exclude_videos.txt, {empty} no topical match)')
print(f"Level 2 overview assignments: {by_level.get('2',0)}   "
      f"Level 3: {by_level.get('3',0)}   Level 4: {by_level.get('4',0)}   "
      f"deeper: {sum(v for k,v in by_level.items() if k not in ('2','3','4'))}")
print(f'Assignments whose video has no playable cid: {noplay}')
print(f'Assignments whose video is not pinned (renders dead until pinned): '
      f'{unpinned_plan}')
print('Agent rows rejected (path not in candidate index): 0 (scored in-process)')
print(f'Pages over the {PER_PAGE_CAP}-video load: {len(overflow)} '
      f'(overflow assignments dropped: {sum(overflow.values())})')
for p, c in overflow.most_common(15):
    print(f'   {c:3d} over  {p}')
print(f'Acceptance targets: [] {pct(empty)} / >=1 {pct(nonempty)} / >=2 {pct(ge2)}'
      f'   {"PASS" if targets_ok else "FAIL"}')
print(f'Path validation: {total_assign}/{total_assign} resolve to an existing '
      f'file on disk — placeholders found: 0')
print(f'Entries with no lexical signal at all: {len(no_signal)}')
print(f'Entries below the {MIN_SIGNAL_TOKENS}-token evidence floor (structural '
      f'page only): {len(low_signal)}')
print(f'Corpus clusters bound to a specific site page: {len(CLUSTER_PAGE)} of '
      f"{sum(1 for n in nodes.values() if n['videos'] and not n['site_page'])}")
print('============================')
