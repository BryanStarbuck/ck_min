#!/usr/bin/env python3
"""Check every internal link in the ai_attorney section against the real route set."""
import os, re, io, sys
ROOT='/Users/bryan/BGit/Bryan_git/charlie-kirk'
AIATT=os.path.join(ROOT,'site/docs/court/ai_attorney')
routes=set()
r=io.open(os.path.join(ROOT,'site/.docusaurus/routes.js'),encoding='utf-8').read()
for m in re.finditer(r"path: '([^']+)'", r):
    routes.add(m.group(1).rstrip('/') or '/')
# every .mdx now on disk under ai_attorney is a live route
for f in os.listdir(AIATT):
    if f.endswith('.mdx'):
        routes.add('/court/ai_attorney/'+f[:-4])
bad={}
for f in sorted(os.listdir(AIATT)):
    if not f.endswith('.mdx'): continue
    t=io.open(os.path.join(AIATT,f),encoding='utf-8').read()
    for m in re.finditer(r'\]\((/[^)#?\s]*)', t):
        u=m.group(1).rstrip('/') or '/'
        if u.startswith('/img/') or u.startswith('/court/filings/'): continue
        if u not in routes:
            bad.setdefault(f,set()).add(u)
    for m in re.finditer(r'href="(/[^"#?]*)"', t):
        u=m.group(1).rstrip('/') or '/'
        if u.startswith('/img/') or u.startswith('/court/filings/'): continue
        if u not in routes:
            bad.setdefault(f,set()).add(u)
n=0
for f,us in sorted(bad.items()):
    print(f)
    for u in sorted(us): print('   BROKEN', u); n+=1
print('---', n, 'broken links across', len(bad), 'files')
sys.exit(1 if n else 0)
