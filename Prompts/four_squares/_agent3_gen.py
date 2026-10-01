#!/usr/bin/env python3
"""Agent 3 block generator. Reads a spec dict and rewrites the four blocks."""
import csv, json, re, sys, os
from pathlib import Path

ROOT = Path(os.path.expanduser("~/BGit/Bryan_git/charlie-kirk"))
IDX = {r['url_path']: r for r in csv.DictReader(open(ROOT/'prompts/four_squares/card_index.csv'))}
ROUTES = set((ROOT/'prompts/four_squares/routes.txt').read_text().split())

CHEV = ('<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        'strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">'
        '<path d="M9 6l6 6-6 6" /></svg>')

def esc_text(s):
    s = s.replace('\\', '')
    s = s.replace('&', '&amp;')
    s = s.replace('{', '').replace('}', '')
    s = s.replace("'", '&apos;').replace('’', '&apos;')
    s = s.replace('—', '&mdash;').replace('–', '&ndash;')
    return s

def esc_attr(s):
    s = s.replace('\\', '')
    s = s.replace('&', '&amp;')
    s = s.replace('"', '&quot;').replace("'", '&apos;').replace('’', '&apos;')
    s = s.replace('{', '').replace('}', '')
    return s

def card(url, teaser):
    r = IDX[url]
    title = esc_text(r['title'])
    kind, shape = r['media_kind'], r['media_shape']
    if kind == 'image' and r['media_src'].startswith('/img/'):
        shape = shape if shape in ('ck-4sq-side', 'ck-4sq-stack') else 'ck-4sq-stack'
        thumb = ('  <a className="ck-4sq-thumb" href="%s"><img src="%s" data-cid="%s" alt="%s" loading="lazy" /></a>\n'
                 % (url, r['media_src'], r['media_cid'], esc_attr(r['media_alt'])))
    else:
        shape = 'ck-4sq-stack'
        thumb = ''
    return ('<div className="ck-4sq-card %s">\n%s'
            '  <div className="ck-4sq-body">\n'
            '    <p className="ck-4sq-title"><a href="%s">%s</a></p>\n'
            '    <p className="ck-4sq-text">%s</p>\n'
            '    <a className="ck-4sq-btn" href="%s">Read this %s</a>\n'
            '  </div>\n</div>\n' % (shape, thumb, url, title, teaser, url, CHEV))

def grid(urls, teasers):
    return '<div className="ck-4sq">\n\n' + ''.join(card(u, teasers[u]) for u in urls) + '\n</div>'

def build(spec, teasers):
    out = []
    out.append('{/* CK_INTERESTING_HERE_START */}\n\n## Interesting In This Area\n\n'
               + '\n'.join('* ' + b for b in spec['here'])
               + '\n\n{/* CK_INTERESTING_HERE_END */}')
    out.append('{/* CK_INTERESTING_OTHER_START */}\n\n## Interesting In Other Areas\n\n'
               + '\n'.join('* ' + b for b in spec['other'])
               + '\n\n{/* CK_INTERESTING_OTHER_END */}')
    out.append('{/* CK_4SQ_SECTION_START */}\n\n## Other Pages In This Section\n\n'
               + grid(spec['section'], teasers) + '\n\n{/* CK_4SQ_SECTION_END */}')
    out.append('{/* CK_4SQ_SITEWIDE_START */}\n\n## Elsewhere In The Investigation\n\n'
               + grid(spec['sitewide'], teasers) + '\n\n{/* CK_4SQ_SITEWIDE_END */}')
    return '\n\n'.join(out)

def validate(spec, teasers, fp):
    errs = []
    me = None
    for u, r in IDX.items():
        if r['file_path'] == fp:
            me = u
    for grp in ('section', 'sitewide'):
        urls = spec[grp]
        if len(set(urls)) != len(urls):
            errs.append(f'{grp}: duplicate target')
        for u in urls:
            if u not in IDX: errs.append(f'{grp}: no index row {u}')
            elif IDX[u]['banned'] == 'yes': errs.append(f'{grp}: banned media {u}')
            if u == me: errs.append(f'{grp}: self card {u}')
            if u not in teasers: errs.append(f'{grp}: no teaser {u}')
    if len(set(IDX[u]['level2'] for u in spec['sitewide'] if u in IDX)) != 4:
        errs.append('sitewide: not 4 distinct level2')
    if any(IDX[u]['level2'] == 'Suspicious' for u in spec['sitewide'] if u in IDX):
        errs.append('sitewide: contains own level2')
    if any(IDX[u]['level2'] != 'Suspicious' for u in spec['section'] if u in IDX):
        errs.append('section: target outside own level2')
    for b in spec['here']:
        for u in re.findall(r'\]\((/[^)\s]*)\)', b):
            if not u.startswith('/Suspicious/'): errs.append(f'here: outside-area link {u}')
            if u == me: errs.append(f'here: self link {u}')
    areas = set()
    for b in spec['other']:
        for u in re.findall(r'\]\((/[^)\s]*)\)', b):
            if u.startswith('/Suspicious/'): errs.append(f'other: in-area link {u}')
            if u in IDX: areas.add(IDX[u]['level2'])
    if len(areas) < 3: errs.append(f'other: only {len(areas)} areas')
    for key in ('here', 'other'):
        if len(spec[key]) != 4: errs.append(f'{key}: {len(spec[key])} bullets')
        for b in spec[key]:
            plain = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', b)
            plain = re.sub(r'&[a-z]+;', ' ', plain)
            n = len(plain.split())
            if n > 17: errs.append(f'{key}: {n} words: {plain[:50]}')
    for u in set(re.findall(r'href="(/[^"#?]*)"', json.dumps(teasers))):
        if u.rstrip('/') not in ROUTES and u not in ROUTES:
            errs.append(f'teaser: unresolved {u}')
    for grp in ('section', 'sitewide'):
        for u in spec[grp]:
            if u.rstrip('/') not in ROUTES and u not in ROUTES:
                errs.append(f'{grp}: unresolved route {u}')
    for b in spec['here'] + spec['other']:
        for u in re.findall(r'\]\((/[^)\s]*)\)', b):
            if u.rstrip('/') not in ROUTES and u not in ROUTES:
                errs.append(f'bullet: unresolved route {u}')
    return errs

MARK = re.compile(r'\n*\{/\* CK_(?:INTERESTING_HERE|INTERESTING_OTHER|4SQ_SECTION|4SQ_SITEWIDE)_START \*/\}.*?'
                  r'\{/\* CK_(?:INTERESTING_HERE|INTERESTING_OTHER|4SQ_SECTION|4SQ_SITEWIDE)_END \*/\}\n*', re.S)

def apply(fp, spec, teasers):
    p = ROOT / fp
    text = p.read_text()
    text = MARK.sub('\n\n', text)
    anchor = '{/* CK_AUTHOR_CREDIT */}'
    if anchor not in text:
        raise SystemExit('no anchor in ' + fp)
    blocks = build(spec, teasers)
    text = text.replace(anchor, blocks + '\n\n' + anchor, 1)
    p.write_text(text)

if __name__ == '__main__':
    mod = sys.argv[1]
    ns = {}
    exec(open(mod).read(), ns)
    SPECS, TEASERS = ns['SPECS'], ns['TEASERS']
    only = sys.argv[2:] or list(SPECS)
    bad = 0
    for fp in only:
        errs = validate(SPECS[fp], TEASERS, fp)
        if errs:
            bad += 1
            print('SPEC-FAIL', fp)
            for e in errs: print('   -', e)
    if bad:
        raise SystemExit(1)
    for fp in only:
        apply(fp, SPECS[fp], TEASERS)
        print('wrote', fp)
