#!/usr/bin/env python3
"""Re-sync every aiatty_* row in pages.csv against what is on disk.
Preserves existing page_key values; adds rows for new pages; refreshes line_count,
title, sidebar_label and description. Never touches any non-aiatty row."""
import csv, io, os, re, sys

ROOT = '/Users/bryan/BGit/Bryan_git/charlie-kirk'
AIATT = os.path.join(ROOT, 'site/docs/court/ai_attorney')
CSV = os.path.join(ROOT, 'pages.csv')

def fm(text, field):
    m = re.search(r'^%s:\s*(.*)$' % field, text, re.M)
    if not m: return ''
    v = m.group(1).strip()
    if v.startswith('"') and v.endswith('"'): v = v[1:-1]
    return v.replace('\\"', '"')

rows = list(csv.reader(io.open(CSV, encoding='utf-8')))
header, body = rows[0], rows[1:]
idx = {c: i for i, c in enumerate(header)}

existing = {r[idx['file_path']]: r for r in body if r[idx['page_key']].startswith('aiatty_')}
kept = [r for r in body if not r[idx['page_key']].startswith('aiatty_')]

SPINE = {'overview','method','trial-cursor','case-stage-map','the-day-one-track','two-tracks-compared'}
out = []
for f in sorted(os.listdir(AIATT)):
    if not f.endswith('.mdx'): continue
    slug = f[:-4]
    path = 'site/docs/court/ai_attorney/' + f
    text = io.open(os.path.join(AIATT, f), encoding='utf-8').read()
    n = text.count('\n') + 1
    row = existing.get(path)
    if row is None:
        row = [''] * len(header)
        row[idx['page_key']] = 'aiatty_' + slug.replace('-', '_')
        row[idx['parent_key']] = 'court_ai_attorney'
        row[idx['level']] = '3' if slug == 'overview' else '4'
        row[idx['level2_parent']] = 'Court'
        row[idx['level2_section']] = 'court'
        row[idx['page_type']] = 'topic'
        row[idx['url_path']] = '/court/ai_attorney/' + slug
        row[idx['file_path']] = path
        row[idx['directory']] = 'court/ai_attorney'
        row[idx['extension']] = 'mdx'
        row[idx['has_frontmatter']] = 'yes'
    row[idx['title']] = fm(text, 'title') or row[idx['title']]
    row[idx['sidebar_label']] = fm(text, 'sidebar_label') or row[idx['sidebar_label']]
    row[idx['description']] = fm(text, 'description') or row[idx['description']]
    row[idx['line_count']] = str(n)
    out.append(row)

w = csv.writer(io.open(CSV, 'w', encoding='utf-8', newline=''))
w.writerow(header)
w.writerows(kept + out)
print('aiatty rows: %d (was %d) | total rows: %d' % (len(out), len(existing), len(kept) + len(out)))
