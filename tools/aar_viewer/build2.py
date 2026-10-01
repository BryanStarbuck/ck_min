# Stage 2: pages.json + TOC -> index.html (PDF-look viewer)
import json, re, html
S='/private/tmp/claude-501/-Users-bryan-BGit-Bryan-git-charlie-kirk-site-docs-UVU/9f888966-8da8-49d5-831e-d4c7c898c10b/scratchpad'
OUT='/Users/bryan/BGit/Bryan_git/charlie-kirk/site/internals/static/reports/uvu-after-action-report'
pages=json.load(open(f'{S}/pages.json'))
N=len(pages)
# ---- outline from the printed TOC (printed page p == PDF page p+1)
toc=[]
for ln in open(f'{S}/aar.txt').read().split('\f')[0:4]:
    for l in ln.splitlines():
        m=re.match(r'^(\s*)(.+?)\s*\.{3,}\s*(\d+)\s*$',l)
        if not m: continue
        t=m.group(2).strip(); pg=int(m.group(3))+1
        if re.match(r'^\d+\.\d+|^[A-D]\.\d+|^D\.\d+|^Core |^Advisory|^Communications Lead|^Objectives|^Context|^The Project|^Cooperation|^Actions Taken|^Documents|^Professional|^Pre-Event|^Incident Day|^Post-Incident R',t):
            lvl=2
        else: lvl=1
        toc.append((lvl,t,pg))
def esc(s): return html.escape(s,quote=True)
out=[]
for p in pages:
    n=p['n']
    label='Cover' if n==1 else f'Page {n-1}'
    spans=[]
    for x,y,w,h,fs,t in p['lines']:
        spans.append(f'<span style="left:{x}%;top:{y}%;width:{w}%;height:{h}%;font-size:{fs}cqw" data-w="{w}">{esc(t)}</span>')
    links=[]
    for x,y,w,h,href in p['links']:
        ext=not href.startswith('#')
        links.append(f'<a class="lk" href="{esc(href)}" style="left:{x}%;top:{y}%;width:{w}%;height:{h}%"'+(' target="_blank" rel="noopener"' if ext else '')+' aria-label="link"></a>')
    load='eager' if n<=2 else 'lazy'
    out.append(f'<section class="page" id="p{n}" data-n="{n}" aria-label="{label}">'
               f'<img src="pages/p{n:03d}.webp" alt="{label} of the After-Action Report for Utah Valley University" loading="{load}" decoding="async" width="1224" height="1584">'
               f'<div class="tl{" ocr" if p["src"]=="ocr" else ""}">{"".join(spans)}</div>{"".join(links)}</section>')
tochtml=''.join(f'<a class="t{l}" href="#p{pg}" data-p="{pg}"><span>{esc(t)}</span><em>{pg-1}</em></a>' for l,t,pg in toc)
page=open(f'{S}/template.html').read()
page=page.replace('{{TOC}}',tochtml).replace('{{PAGES}}','\n'.join(out)).replace('{{N}}',str(N))
open(f'{OUT}/index.html','w').write(page)
print('toc',len(toc),'bytes',len(page))
