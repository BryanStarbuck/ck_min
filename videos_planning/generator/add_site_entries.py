#!/usr/bin/env python3
# add_site_entries.py — the second half of STAGE 10.
# Every video the SITE shows must be represented in videos.yaml. scan_pages.py
# reports the embed identities the corpus does not already hold; this script
# appends a row for each to inventory.tsv so the rest of the pipeline picks them
# up on the next pass. Third-party hosted video (YouTube, Rumble) is recorded
# with cid "" and its watch URL in source_url: it is real evidence and belongs
# in the hierarchy, but it cannot be served from IPFS and its page carries an
# external embed rather than our player.
import os, csv, json, collections

HERE = os.path.dirname(os.path.abspath(__file__))
INV = os.path.join(HERE, 'inventory.tsv')
REP = os.path.join(HERE, 'stage10_report.json')

# Titles and clusters for the identities the sweep found. Each was resolved by
# opening the page it sits on; nothing here is guessed from the id.
KNOWN = {
    'yt|1RbDMiEReys':  ('Who Assassinated Charlie Kirk (site film)', 'Videos_Home_Film'),
    'yt|0ykbt_WGOZE':  ('Dave Smith podcast episode', 'Influencer_Podcast'),
    'yt|1xTpQ9RHkvk':  ('Tucker Carlson podcast episode', 'Influencer_Podcast'),
    'yt|2exo7iJ-qdc':  ('Project Constitution podcast episode', 'Influencer_Podcast'),
    'yt|J2DKRfwSt94':  ('Hodgetwins podcast episode', 'Influencer_Podcast'),
    'yt|X8UKjN5cjvw':  ('Ian Carroll podcast episode', 'Influencer_Podcast'),
    'yt|wcD2khO3rOA':  ('Candace Owens podcast episode', 'Influencer_Podcast'),
    'rumble|v6yrnyo':  ('Steve Bannon podcast episode', 'Influencer_Podcast'),
    'rumble|v705uyi':  ('Jimmy Dore podcast episode', 'Influencer_Podcast'),
    'ipfs|QmedrrPge7Bj8vUN6xxq1Zfz1CgwuY6xGAtWFFbU4tmg4R':
        ('Microphone footage embedded on the Mic overview', 'Site_Embed'),
}
WATCH = {'yt': 'https://www.youtube.com/watch?v={}',
         'rumble': 'https://rumble.com/embed/{}'}

rows = list(csv.DictReader(open(INV, encoding='utf-8'), delimiter='\t'))
cols = list(rows[0].keys())
have = {r['vkey'] for r in rows}
rep = json.load(open(REP, encoding='utf-8'))

added = []
for ident, pages in sorted(rep['new_entries'].items()):
    kind, ref = ident.split('|', 1)
    # a filename that IS a YouTube id is already in the corpus as a local file
    if ref in have:
        continue
    vkey = ('yt/' if kind in ('yt', 'rumble', 'odysee') else 'site/') + ref
    if vkey in have:
        continue
    title, _cluster = KNOWN.get(ident, ('', ''))
    r = {c: '' for c in cols}
    r.update(vkey=vkey, basename=ref, media_present='none', size='0',
             origin='site_embed', source_platform=
                 {'yt': 'youtube', 'rumble': 'rumble', 'odysee': 'odysee',
                  'ipfs': 'ipfs'}[kind],
             source_url=WATCH.get(kind, '').format(ref) if kind in WATCH else '',
             manifest_cid=ref if kind == 'ipfs' else '',
             manifest_pinned='', title_hint=title,
             manifest_description=f'Embedded on {len(pages)} site page(s)')
    rows.append(r)
    added.append(vkey)

with open(INV, 'w', encoding='utf-8', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=cols, delimiter='\t',
                       quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    w.writeheader()
    for r in sorted(rows, key=lambda x: x['vkey']):
        w.writerow(r)

print(f'STAGE 10 (append): {len(added)} site-embed entries added to the corpus')
for a in added:
    print('   ' + a)
