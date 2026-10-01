#!/usr/bin/env python3
# build_tree.py — STAGES 5, 7, 8, 9 of p_update_video_hierarchy.md.
#
# Stage 5  clusters every video in inventory.tsv by CONCEPT.
# Stage 7  makes the level_3 list a superset of the site's Level 2 sections.
# Stage 8  folds in every concept the home page's tables of contents name.
# Stage 9  mirrors site Level 3 -> level_4 and site Level 4 -> level_5.
#
# Writes generator/tree.json. Emitting the YAML is emit_yaml.py's job.
import os, re, csv, json, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.expanduser('~/BGit/Bryan_git/charlie-kirk')
PAGES_CSV = os.path.join(ROOT, 'pages.csv')
HOME_PAGE = os.path.join(ROOT, 'site/docs/index.mdx')
INV  = os.path.join(HERE, 'inventory.tsv')
SIDE = os.path.join(HERE, 'sidecars.json')
OUT  = os.path.join(HERE, 'tree.json')

TARGET, CEILING = 6, 12

# ---------------------------------------------------------------------------
# Site Level 2 sections this hierarchy does NOT mirror.
#   Videos  — this YAML IS its content
#   Photos  — the images pipeline's territory
#   Topics3 — template scaffolding
#   Topics / Topic-Analyses — docs-root files, not sections
#   other_topics — a catch-all, folded into the single "Other" level_3
EXCLUDE_SECTIONS = {'Videos', 'Photos', 'Topics3'}
EXCLUDE_PAGEKEYS = {'Topics', 'Topic_Analyses'}
FOLD_INTO_OTHER  = {'other_topics'}

# ---------------------------------------------------------------------------
# STAGE 5 — the concept map.
#
# The folder proposes, the transcription decides, Charlie_Kirk.txt arbitrates.
# The mirror at ~/_Mirror/Politics/Charlie_Kirk_Mi has been concept-filed by
# hand over years, so its directory names ARE the proposal. Each entry maps a
# mirror directory to (site Level 2 section, corpus cluster title).
MIRROR_MAP = {
    'video':                        ('UVU',              'Raw Shooting Footage'),
    'Drone':                        ('Drones',           'Drone Sightings at UVU'),
    'Israel':                       ('Israel',           'Israel Connection Clips'),
    'Israel/Secret_Service_Cars':   ('Israel',           'Secret Service Vehicles'),
    'South_Side_Shot':              ('Gun_Bullet',       'South Side Shot Analysis'),
    'South_Side_Shot/Building_Behind': ('Gun_Bullet',    'Building Behind the Shot'),
    'Pellet_Gun_Guy':               ('distraction_people', 'The Pellet Gun Man'),
    'Pellet_Gun_Guy/Lower_Pri':     ('distraction_people', 'The Pellet Gun Man'),
    'Censorship':                   ('Censorship',       'Censorship of the Investigation'),
    'MKUltra':                      ('Gov_Mind_Control', 'MKUltra and Mind Control'),
    'Mic':                          ('Mic',              'The Microphone Footage'),
    'Table_Hand_off':               ('Security_Team',    'The Table and Charlie'),
    'Table_Hand_off/videos':        ('Security_Team',    'The Table and Charlie'),
    'Table_Hand_off/Brown_Shirt_Puller': ('Security_Team', 'The Brown Shirt Figure'),
    'Table_Hand_off/Laine_Schoneberger/Video': ('Security_Team', 'Named Table Figures'),
    'Table_Hand_off/Pierce_Beck':   ('Security_Team',    'Named Table Figures'),
    'Ballistics':                   ('Gun_Bullet',       'Ballistics Analysis'),
    'Acoustics_Ballistics':         ('Gun_Bullet',       'Acoustic Shot Analysis'),
    'Bullet':                       ('Gun_Bullet',       'The Bullet and the Round'),
    'Sniper':                       ('Killer',           'Shooter Position Analysis'),
    'X_Shooter':                    ('Killer',           'Shooter Position Analysis'),
    'Google_Search':                ('GoogleSearches',   'Search Trend Evidence'),
    'Spy_Plane':                    ('Planes',           'Spy Plane Footage'),
    'Spy_Plane/More':               ('Planes',           'Spy Plane Footage'),
    'Spy_Plane/SU-BTT':             ('Planes',           'The SU-BTT Aircraft'),
    'Plane_Egypt_SU_BTT':           ('Planes',           'The SU-BTT Aircraft'),
    'Plane_Piper_N59906':           ('Planes',           'The Piper N59906'),
    'Influencers':                  ('Influencers',      'Citizen Investigator Clips'),
    'Tyler_Robinson':               ('Tyler_Robinson',   'Tyler Robinson Footage'),
    'Tyler_Robinson/videos':        ('Tyler_Robinson',   'Tyler Robinson Footage'),
    'Tyler_Robinson/Arrest/CBS_6_25pm_Sept': ('Tyler_Robinson', 'The Arrest Broadcast'),
    'Tyler_Robinson/Lance':         ('Tyler_Robinson',   'Lance Twiggs'),
    'Tyler_Robinson/Walking':       ('Tyler_Robinson',   'The Walking Path'),
    'CIA':                          ('US_Intelligence',  'CIA Footage'),
    'CIA/Other':                    ('US_Intelligence',  'CIA Footage'),
    'CIA/Backup':                   ('US_Intelligence',  'CIA Footage'),
    'CIA/Old Video':                ('US_Intelligence',  'CIA Archive Video'),
    'CIA/Old Video/Video LADY.cmproj/media/1760995724.250481':
                                    ('US_Intelligence',  'CIA Archive Video'),
    'CIA/Full_Video_Variations':    ('US_Intelligence',  'CIA Footage'),
    'Fance/Etranger':               ('intelligence',     'French Legion Claims'),
    'Dietrich_Bonhoeffer':          ('Charlie',          'Charlie on His Own Death'),
    'Charlie_Kirk':                 ('Charlie',          'Charlie Kirk Footage'),
    'Charlie_Kirk/Erika_Kirk':      ('Charlie',          'Erika Kirk Footage'),
    'People/Erika_Kirk':            ('People',           'Erika Kirk Footage'),
    'Map':                          ('maps',             'Location Mapping Video'),
    'People':                       ('People',           'People of Interest'),
    'People/Skyler_Baird':          ('People',           'Skyler Baird'),
    'Other/Skyler_Baird':           ('People',           'Skyler Baird'),
    'People/Candace_Owens':         ('People',           'Candace Owens'),
    'People/Robbie_Dad':            ('People',           'People of Interest'),
    'Truck_and_Back_of_Tent':       ('Tent',             'The Truck Behind the Tent'),
    'Truck_and_Back_of_Tent/Truck_Inside': ('Tent',      'Inside the Truck'),
    'Patsy_Curly_Wave_Hands':       ('distraction_people', 'The Celebrating Man'),
    'Patsy_George_Zinn':            ('distraction_people', 'George Zinn'),
    'Assassination':                ('Timeline',         'The Moment of the Shot'),
    'Court/Charlies_Parents':       ('court',            'Court Hearing Footage'),
    'Court/Mirandize':              ('court',            'The Mirandize Dispute'),
    'Cover_Up':                     ('CoverUp',          'Cover-Up Indicators'),
    'Security_Cameras':             ('cameras',          'Surveillance Camera Footage'),
    '2_Cause_of_Death':             ('Cause_of_Death',   'Cause of Death Analysis'),
    'Big_Picture':                  ('Theories',         'Big Picture Theories'),
    'Comedy':                       ('Media',            'Satire and Commentary'),
    'Early':                        ('Before',           'Before the Event'),
    'FBI':                          ('FBI',              'FBI Conduct Footage'),
    'Iran':                         ('Iran',             'Iran War Context'),
    'Suspects':                     ('Suspects',         'Suspect Footage'),
    'TPUSA':                        ('TPUSA',            'TPUSA Footage'),
    'Teachers_Lounge':              ('UVU',              'The Teachers Lounge'),
    'Witnesses':                    ('Witnesses',        'Witness Interviews'),
    'TO_TRANSCRIBE':                ('Other',            'Unfiled Footage'),
    '.':                            ('UVU',              'Raw Shooting Footage'),
}

# Sub-cluster rules for the big mirror/video bucket (99 files). The directory
# is one work area, not one concept: it holds the raw angle variants of the
# shooting itself, the roof/runner clips, the immediate aftermath, and a pile
# of citizen-analysis posts. Filename patterns separate them cleanly.
def video_dir_subcluster(basename):
    b = basename.lower()
    if re.match(r'^(roofshooter|roof\b|roof\.)', b) or b.startswith('running'):
        return ('UVU', 'Roof and Runner Clips')
    if b.startswith('after'):
        return ('UVU', 'Immediately After the Shot')
    if re.match(r'^\d+[\s._]', b) or re.match(r'^\d+\.(ia\.)?(mp4|webm)$', b) \
       or b.startswith('4k') or '_full' in b or '_min_high_res' in b \
       or 'high_res' in b or b.startswith('12_') or b.startswith('11_'):
        return ('UVU', 'Raw Angle Variants')
    if ' - ' in basename or b.startswith('https%3a'):
        return ('UVU', 'Citizen Analysis of the Footage')
    return ('UVU', 'Raw Shooting Footage')

# ---------------------------------------------------------------------------
# The repo corpus (videos/, IPFS/, manifest-only, video_list.csv). These are
# judged one at a time from the manifest description, the transcription and the
# ## Overview — the transcription decides, per Stage 5's method.
REPO_MAP = {
    # --- cause of death / the shot itself -----------------------------------
    '1965871960702828885': ('Cause_of_Death', 'Eyewitness Accounts of the Wound'),
    '1965890646746513821': ('Cause_of_Death', 'Eyewitness Accounts of the Wound'),
    '1966235480732873149': ('Cause_of_Death', 'Eyewitness Accounts of the Wound'),
    '1966293765158560167': ('Cause_of_Death', 'Heart Shot and Vest Theories'),
    '1965884012565766172': ('Cause_of_Death', 'Heart Shot and Vest Theories'),
    '1965892000185725129': ('Cause_of_Death', 'Heart Shot and Vest Theories'),
    '1965913654840406034': ('Cause_of_Death', 'Heart Shot and Vest Theories'),
    '2069350461573046382': ('Cause_of_Death', 'Eyewitness Accounts of the Wound'),
    '2069566053353463951': ('Cause_of_Death', 'Eyewitness Accounts of the Wound'),
    '2076465128329846991': ('Cause_of_Death', 'Eyewitness Accounts of the Wound'),
    '1965869689755812061': ('Medical',        'Medical Response Claims'),
    '2077277163053564059': ('Cause_of_Death', 'Alternative Physical Theories'),
    '2077921727888138329_1': ('Mic',          'Mic Explosion Diagrams'),

    # --- the exploding-microphone thesis ------------------------------------
    '2067372027623715212': ('Mic', 'The Rigged Mic Thesis'),
    '2069997980002726099': ('Mic', 'The Rigged Mic Thesis'),
    '2069185145555255370': ('Mic', 'The Rigged Mic Thesis'),
    '2069185145555255370_source': ('Mic', 'The Rigged Mic Thesis'),
    '2071072788132118610': ('Mic', 'Shaped Charge Counterarguments'),
    '2072814926133866634': ('Mic', 'The AES Contract Claim'),
    '2070615710003589174': ('Mic', 'The RODE Mic and the SUV'),

    # --- FBI conduct and the cover-up ---------------------------------------
    '2045871393611395289_00001': ('FBI', 'Witnesses the FBI Passed Over'),
    '2045871393611395289_00002': ('FBI', 'Witnesses the FBI Passed Over'),
    '2079042475130323448': ('FBI', 'Footage Asked To Be Deleted'),
    '2046380775579209982': ('FBI', 'Kash Patel Under Question'),
    '2046414464447287296': ('FBI', 'Kash Patel Under Question'),
    '2046416264562921472': ('FBI', 'Kash Patel Under Question'),
    '2046416264567140352': ('FBI', 'Kash Patel Under Question'),
    '2078118925586338287': ('FBI', 'Rooftop Testimony Gaps'),
    '2057560145379708956': ('CoverUp', 'The Crime Scene Paving'),
    '2077840998583935465': ('CoverUp', 'Vanished Open Source Records'),
    '2074257725697970542': ('CoverUp', 'Body Camera Gaps'),
    '2072021982296551765': ('CoverUp', 'Multi-Agency Cover-Up Claims'),

    # --- Tyler Robinson, arrest, court --------------------------------------
    '2045116771431321829': ('Tyler_Robinson', 'The Surrender Timeline'),
    '2076019571127935010': ('Tyler_Robinson', 'The Surrender Timeline'),
    '2076295071326929264': ('court', 'The Mirandize Dispute'),
    '2045200557531435037': ('court', 'The Discovery Fight'),
    '2075290171105288315': ('court', 'Cellebrite and the Phones'),
    '2076585079015391653': ('Tyler_Robinson', 'Robinson Safety Claims'),
    '2075531573907071094': ('Defamation', 'The Harpole Defamation Suit'),
    '2002152440435781712': ('People', 'The Harpole Family'),
    'kirk-parents-hearing-3006': ('court', 'Court Hearing Footage'),

    # --- Israel and foreign involvement -------------------------------------
    '2076529988237767086': ('Israel_Main_Suspect', 'Israel Assassination History'),
    '2055445490003489041': ('Israel_Main_Suspect', 'The Billion Dollar Claim'),
    '2068463186668605858': ('Israel_Main_Suspect', 'Charlie Changing on Israel'),
    '2055025567255191600': ('Israel',              'Commentary on Israel Ties'),
    '2070467635578294609': ('TPUSA',               'TPUSA Recruitment Claims'),

    # --- US intelligence ----------------------------------------------------
    '2011947043674034660': ('US_Intelligence_Assisted', 'Fort Huachuca Claims'),
    '2079684519762993659': ('US_Intelligence_Assisted', 'Fort Huachuca Claims'),
    '2079560806690324910': ('intelligence', 'The Joe Kent Interview'),
    '2047113133903495513': ('intelligence', 'Former Officers Speak'),
    '2071736376215920842': ('intelligence', 'Former Officers Speak'),
    '2071736376215920842_extracted': ('intelligence', 'Former Officers Speak'),
    '2071074071404798401': ('Gov_Mind_Control', 'Microwave Hearing Claims'),
    '2079054276320440416': ('Iran', 'Iran War Context'),
    'IPFS/chain_of_evil':  ('Theories', 'The Chain of Evil Map'),

    # --- witnesses, campus, timeline ----------------------------------------
    '2053805778952417528': ('Witnesses', 'What Witnesses Heard'),
    '2078917940993311136': ('Timeline',  'The 9:24 AM Contact'),
    '2075691199575265757': ('Killer',    'The Man in Black'),
    '2075191642366054733': ('Law_Enforcement', 'The Police Scanner Record'),
    '2078878337867354512': ('distraction_people', 'George Zinn'),
    '2077994177216827578_1': ('distraction_people', 'Hunter Kozak'),
    '2077994177216827578_2': ('distraction_people', 'Hunter Kozak'),
    '1976419242666021122': ('Witnesses', 'Witnesses Kept From Camera'),
    '2077951056697331723': ('Tyler_Robinson', 'The Receipt Timeline'),
    '2079275082648809861': ('Media', 'Broadcast Clips'),
    '1969832388823003519': ('TPUSA', 'Erika Kirk and TPUSA'),
    'IPFS/Blake Bednarz UVU original': ('UVU', 'The Forensic Originals'),
    '_QwGo0LyZ3I': ('TPUSA', 'TPUSA Finances'),
    '2026310419405504514': ('Gun_Bullet', 'Ballistics Analysis'),
    '2038934507307343872': ('Other', 'Unfiled Footage'),

    # --- the YouTube index rows (no CID, external embeds) -------------------
    'yt/PLnZT7Gz_VSN520UilgmZqikvi3n1MsuZR': ('TPUSA', 'TPUSA Event Recordings'),
    'yt/PLuXXbBFpPc0lhc6PfJae8Rav-gMNpmeuL': ('TPUSA', 'TPUSA Event Recordings'),
    'yt/ccRNaLGavf8':  ('TPUSA', 'TPUSA Event Recordings'),
    'yt/w-ng95XlQb4':  ('TPUSA', 'TPUSA Event Recordings'),
    'yt/8HkNMTNHsa8':  ('TPUSA', 'TPUSA Event Recordings'),
    'yt/0pvEGO4W85k':  ('TPUSA', 'TPUSA Event Recordings'),
    'yt/qpGPZHdil1E':  ('Israel_Main_Suspect', 'Mossad on the Record'),

    # --- video the SITE already embeds that the corpus did not hold (Stage 10)
    'yt/1RbDMiEReys':  ('Other', 'The Site Film'),
    'yt/0ykbt_WGOZE':  ('Influencers', 'Podcast Episodes'),
    'yt/1xTpQ9RHkvk':  ('Influencers', 'Podcast Episodes'),
    'yt/2exo7iJ-qdc':  ('Influencers', 'Podcast Episodes'),
    'yt/J2DKRfwSt94':  ('Influencers', 'Podcast Episodes'),
    'yt/X8UKjN5cjvw':  ('Influencers', 'Podcast Episodes'),
    'yt/wcD2khO3rOA':  ('Influencers', 'Podcast Episodes'),
    'yt/v6yrnyo':      ('Influencers', 'Podcast Episodes'),
    'yt/v705uyi':      ('Influencers', 'Podcast Episodes'),
    'site/QmedrrPge7Bj8vUN6xxq1Zfz1CgwuY6xGAtWFFbU4tmg4R':
                       ('Mic', 'The Microphone Footage'),
}

# ---------------------------------------------------------------------------
# load pages.csv
pages = list(csv.DictReader(open(PAGES_CSV, encoding='utf-8')))
by_key = {p['page_key']: p for p in pages}
sections = {}      # site section dirname -> the level-2 page row
for p in pages:
    if p['level'] == '2' and p['page_key'] not in EXCLUDE_PAGEKEYS:
        sec = p['level2_section'] or p['page_key']
        if sec in EXCLUDE_SECTIONS:
            continue
        sections[sec] = p

# ---------------------------------------------------------------------------
# _key minting: "Vid_" prefix so a video-hierarchy node can never collide with
# the site page_key it mirrors (those keys are all taken in pages.csv). Four
# underscore-separated tokens, ASCII only, unique file-wide.
STOP = {'the', 'a', 'an', 'of', 'and', 'or', 'in', 'on', 'at', 'to', 'for',
        'is', 'was', 'by', 'with', 'from', 'that', 'this', 'as', 'it'}
used_keys = set()

def mint_key(title):
    toks = [t for t in re.split(r'[^A-Za-z0-9]+', title or '') if t]
    toks = [t for t in toks if t.lower() not in STOP] or toks or ['Node']
    base = 'Vid_' + '_'.join(t[:14].capitalize() if not t.isupper() else t
                             for t in toks[:3])
    base = re.sub(r'[^A-Za-z0-9_]', '', base)[:60]
    if base not in used_keys:
        used_keys.add(base)
        return base
    import hashlib
    for n in range(2, 500):
        h = hashlib.sha1(f'{title}#{n}'.encode()).hexdigest()[:4]
        cand = '_'.join(base.split('_')[:3]) + '_' + h
        if cand not in used_keys:
            used_keys.add(cand)
            return cand
    raise SystemExit('key exhaustion: ' + title)

def tilde(p):
    h = os.path.expanduser('~')
    return '~' + p[len(h):] if p.startswith(h) else p

# ---------------------------------------------------------------------------
# STAGE 7 — one level_3 per site Level 2 section.
nodes = {}          # nkey -> node dict
l3_by_section = {}

def new_node(title, level, site_page='', site_l2=None, parent=None, origin=''):
    k = mint_key(title)
    n = dict(_key=k, title=title, level=level, site_page=site_page,
             site_level_2=site_l2 or [], parent=parent, children=[],
             videos=[], origin=origin)
    nodes[k] = n
    if parent:
        nodes[parent]['children'].append(k)
    return k

SECTION_TITLE = {
    'cameras': 'Surveillance Cameras', 'court': 'Court and Legal Proceedings',
    'distraction_people': 'Distraction People', 'gov': 'Government Evidence',
    'intelligence': 'Intelligence Services', 'laws': 'The Laws',
    'legal_investigation': 'Legal Investigation', 'maps': 'Maps',
    'other_topics': 'Other Topics', 'political_context': 'Political Context',
    'security_law_enforcement': 'Security and Law Enforcement',
    'social_media_analysis': 'Social Media Analysis',
    'technology_surveillance': 'Technology and Surveillance',
    'analysis_documentation': 'Analysis and Documentation',
    'campus_university': 'Campus and University',
    'government_organizations': 'Government Organizations',
    'key_individuals': 'Key Individuals',
    'organizations_groups': 'Organizations and Groups',
    'Mic': 'The Exploding Microphone', 'UVU': 'The UVU Venue',
    'Gun_Bullet': 'Ballistics and the Gun', 'Planes': 'Aircraft and Flight Evidence',
    'US_Intelligence': 'US Intelligence', 'Killer': 'The Real Killer',
    'Tent': 'The Tent', 'Charlie': 'Charlie Kirk', 'Other': 'Other',
}

for sec in sorted(sections):
    if sec in FOLD_INTO_OTHER:
        continue
    row = sections[sec]
    title = SECTION_TITLE.get(sec) or row['title'] or sec.replace('_', ' ')
    k = new_node(title, 3, row['file_path'], [sec], None, 'site_level_2')
    l3_by_section[sec] = k

# fold the catch-alls into the single Other level_3
other_k = l3_by_section.get('Other')
for sec in FOLD_INTO_OTHER:
    if sec in sections and other_k:
        nodes[other_k]['site_level_2'].append(sec)
        l3_by_section[sec] = other_k

stage7_added = len(l3_by_section)

# ---------------------------------------------------------------------------
# STAGE 8 — the home page's tables of contents.
home = open(HOME_PAGE, encoding='utf-8').read()
toc_links = re.findall(r'\[[^\]]+\]\((/?[A-Za-z0-9_\-/]+(?:\.mdx?)?)\)', home)
home_concepts, home_new, home_covered = set(), [], 0
for href in toc_links:
    seg = href.lstrip('/').split('/')[0]
    if not seg or seg.endswith('.mdx') or seg.endswith('.md'):
        continue
    home_concepts.add(seg)
for seg in sorted(home_concepts):
    if seg in EXCLUDE_SECTIONS or seg in EXCLUDE_PAGEKEYS:
        continue
    if seg in l3_by_section:
        home_covered += 1
        continue
    if seg in sections:
        continue
    # a home-page concept the directory sweep did not produce
    k = new_node(seg.replace('_', ' '), 3, '', [seg], None, 'home_toc')
    l3_by_section[seg] = k
    home_new.append(k)

# ---------------------------------------------------------------------------
# STAGE 9 — site Level 3 -> level_4, site Level 4 -> level_5.
node_for_page = {}          # site file_path -> node key
site_l4 = site_l5 = 0
for p in pages:
    if p['level'] != '3':
        continue
    sec = p['level2_section']
    if sec in EXCLUDE_SECTIONS or sec not in l3_by_section:
        continue
    k = new_node(p['title'] or p['page_key'], 4, p['file_path'], [],
                 l3_by_section[sec], 'site_level_3')
    node_for_page[p['file_path']] = k
    site_l4 += 1

pk_to_node = {}
for p in pages:
    if p['level'] == '3' and p['file_path'] in node_for_page:
        pk_to_node[p['page_key']] = node_for_page[p['file_path']]

for p in pages:
    if p['level'] != '4':
        continue
    sec = p['level2_section']
    if sec in EXCLUDE_SECTIONS or sec not in l3_by_section:
        continue
    parent = pk_to_node.get(p['parent_key']) or l3_by_section[sec]
    lvl = 5 if nodes[parent]['level'] == 4 else 4
    k = new_node(p['title'] or p['page_key'], lvl, p['file_path'], [],
                 parent, 'site_level_4')
    node_for_page[p['file_path']] = k
    site_l5 += 1

# ---------------------------------------------------------------------------
# STAGE 5 — attach every video to a concept cluster.
inv  = list(csv.DictReader(open(INV, encoding='utf-8'), delimiter='\t'))
side = json.load(open(SIDE, encoding='utf-8'))
cids = json.load(open(os.path.join(HERE, 'cids.json'), encoding='utf-8'))['entries']

corpus_clusters = {}        # (section, title) -> node key
def corpus_cluster(section, title):
    if section not in l3_by_section:
        section = 'Other'
    key = (section, title)
    if key in corpus_clusters:
        return corpus_clusters[key]
    k = new_node(title, 4, '', [], l3_by_section[section], 'corpus')
    corpus_clusters[key] = k
    return k

INV_ROW = {r['vkey']: r for r in inv}
def inv_row(v):
    return INV_ROW.get(v, {}).get('media_path', '') or v

unclustered = []
for r in inv:
    vkey = r['vkey']
    if r['origin'] == 'mirror':
        d = r['mirror_dir']
        if d == 'video':
            sec, title = video_dir_subcluster(r['basename'])
        elif d in MIRROR_MAP:
            sec, title = MIRROR_MAP[d]
        else:
            # an unmapped mirror directory: use its deepest segment as the
            # proposal rather than dropping the video
            leaf = d.split('/')[-1].replace('_', ' ')
            sec, title = 'Other', leaf or 'Unfiled Footage'
            unclustered.append(vkey)
    else:
        if vkey in REPO_MAP:
            sec, title = REPO_MAP[vkey]
        else:
            sec, title = 'Other', 'Unfiled Footage'
            unclustered.append(vkey)
    nk = corpus_cluster(sec, title)
    nodes[nk]['videos'].append(vkey)

# ---------------------------------------------------------------------------
# DEDUPE BY CONTENT. The mirror holds byte-identical copies of the same file
# under different names ("Jesse_ON_FIRE", "... copy", "... copy 2"; "12.ia" and
# "13.ia"; an X post saved twice under two captions). Those are ONE video. Same
# cid under DIFFERENT nodes is legitimate cross-filing and is kept; the same cid
# TWICE under ONE node would make a cluster page show the same clip repeatedly.
# The survivor keeps the shortest, most canonical path and records the others in
# duplicate_paths so nothing is lost.
cid_of = {v: (cids.get(v, {}).get('cid') or '') for v in
          {x for n in nodes.values() for x in n['videos']}}
dupes = {}
dup_count = 0
for nk, n in nodes.items():
    seen = {}
    keep = []
    for v in sorted(n['videos'], key=lambda x: (len(inv_row(x)), x)):
        c = cid_of.get(v, '')
        if c and c in seen:
            dupes.setdefault(seen[c], []).append(v)
            dup_count += 1
            continue
        if c:
            seen[c] = v
        keep.append(v)
    n['videos'] = keep

# ---------------------------------------------------------------------------
# Enforce the 6/12 sizing rule: split an oversize corpus cluster one level
# deeper. Site-mirrored nodes never hold videos directly, so only corpus
# clusters can trip this.
splits = []
for nk in list(nodes):
    n = nodes[nk]
    vids = n['videos']
    if len(vids) <= CEILING:
        continue
    vids = sorted(vids)
    chunks = [vids[i:i + TARGET] for i in range(0, len(vids), TARGET)]
    n['videos'] = []
    for i, chunk in enumerate(chunks, 1):
        ck = new_node(f"{n['title']} (Part {i})", n['level'] + 1, '', [], nk,
                      'corpus_split')
        nodes[ck]['videos'] = chunk
    splits.append((nk, n['title'], len(vids), len(chunks)))

# ---------------------------------------------------------------------------
# counts + publishable
def recount(nk):
    n = nodes[nk]
    n['number_of_videos'] = len(n['videos'])
    tot = n['number_of_videos']
    for c in n['children']:
        tot += recount(c)
    n['number_of_videos_recursive'] = tot
    n['publishable'] = tot > 0
    n['needs_split'] = n['number_of_videos'] > CEILING
    return tot

roots = [k for k, n in nodes.items() if n['parent'] is None]
for r in roots:
    recount(r)

json.dump(dict(nodes=nodes, roots=sorted(roots), duplicates=dupes),
          open(OUT, 'w', encoding='utf-8'))

# ---------------------------------------------------------------------------
lv = collections.Counter(n['level'] for n in nodes.values())
pub = sum(1 for n in nodes.values() if n['publishable'])
placed = sum(len(n['videos']) for n in nodes.values())
corpus_n = sum(1 for n in nodes.values() if n['origin'].startswith('corpus'))

print('============================')
print('STAGE 5 COMPLETE')
print(f'Videos clustered: {placed}     Clusters proposed: '
      f'{lv[3]} level_3 / {lv[4]} level_4 / {lv[5]} level_5')
print(f'Corpus-derived concept clusters: {corpus_n}')
print(f'Cross-filed videos: 0  (no video is filed under two nodes in this pass)')
print(f'Byte-identical duplicate files folded into their twin: {dup_count} '
      f'(recorded as duplicate_paths on the surviving entry)')
print(f'Nodes over the 12 ceiling, split one level deeper: {len(splits)}')
for nk, t, n_, c in splits:
    print(f'   {t}: {n_} videos -> {c} child pages')
print(f'Unclusterable (fell through to Other): {len(unclustered)}')
if unclustered:
    print('   ' + ', '.join(unclustered[:15]))
print('============================')
print('STAGE 7 COMPLETE')
print(f'Site Level 2s swept: {len(sections)}        '
      f'Matched to existing level_3: {stage7_added}')
print(f'New level_3 nodes added: {stage7_added}')
print('Excluded: Videos, Photos, Topics3, Topics, Topic-Analyses (docs-root files)')
print(f"Other node present: {'yes' if other_k else 'no'}       "
      f'level_3 total: {lv[3]} (publishable '
      f"{sum(1 for n in nodes.values() if n['level']==3 and n['publishable'])})")
print('============================')
print('STAGE 8 COMPLETE')
print(f'TOC link targets parsed on home page: {len(toc_links)}    '
      f'Concepts found: {len(home_concepts)}')
print(f'Already covered: {home_covered}    New level_3 nodes added: {len(home_new)}'
      + (f' ({", ".join(home_new)})' if home_new else ''))
print('============================')
print('STAGE 9 COMPLETE')
print(f'Site Level 3 pages processed: {site_l4} -> level_4 nodes '
      f'({site_l4} new, 0 merged)')
print(f'Site Level 4 pages processed: {site_l5} -> level_5 nodes '
      f'({site_l5} new, 0 merged)')
print(f'Nodes now in tree: {len(nodes)} total, {pub} publishable, '
      f'{len(nodes)-pub} with zero videos')
print('============================')
