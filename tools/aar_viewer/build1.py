# Stage 1: render page images (webp) + collect text boxes (native or OCR) -> pages.json
import pymupdf, io, json, subprocess, os, csv, sys
from PIL import Image
SRC='/Users/bryan/BGit/Bryan_git/charlie-kirk/site/docs/UVU/after-action-report.pdf'
OUT='/Users/bryan/BGit/Bryan_git/charlie-kirk/site/internals/static/reports/uvu-after-action-report'
TMP='/private/tmp/claude-501/-Users-bryan-BGit-Bryan-git-charlie-kirk-site-docs-UVU/9f888966-8da8-49d5-831e-d4c7c898c10b/scratchpad/ocr'
os.makedirs(TMP,exist_ok=True)
d=pymupdf.open(SRC)
pages=[]
for p in d:
    n=p.number+1
    W,H=p.rect.width,p.rect.height
    pix=p.get_pixmap(matrix=pymupdf.Matrix(2,2))
    im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples)
    im.save(f'{OUT}/pages/p{n:03d}.webp','WEBP',quality=70,method=6)
    lines=[]
    if p.get_text().strip():
        src='pdf'
        for b in p.get_text('dict')['blocks']:
            for l in b.get('lines',[]):
                spans=[s for s in l['spans'] if s['text'].strip()]
                if not spans: continue
                if abs(l['dir'][1])>0.1: continue  # skip rotated
                t=''.join(s['text'] for s in l['spans']).rstrip()
                x0,y0,x1,y1=l['bbox']
                size=max(s['size'] for s in spans)
                lines.append([round(x0/W*100,3),round(y0/H*100,3),round((x1-x0)/W*100,3),round((y1-y0)/H*100,3),round(size/W*100,3),t])
    else:
        src='ocr'
        pix3=p.get_pixmap(matrix=pymupdf.Matrix(300/72,300/72))
        png=f'{TMP}/p{n:03d}.png'; pix3.save(png)
        tsv=subprocess.run(['tesseract',png,'-','--psm','3','tsv'],capture_output=True,text=True).stdout
        rows=list(csv.DictReader(io.StringIO(tsv),delimiter='\t',quoting=csv.QUOTE_NONE))
        IW,IH=pix3.width,pix3.height
        groups={}
        for r in rows:
            if r['level']!='5' or not r['text'].strip() or float(r['conf'])<0: continue
            k=(r['block_num'],r['par_num'],r['line_num'])
            groups.setdefault(k,[]).append(r)
        for k,ws in groups.items():
            x0=min(int(w['left']) for w in ws); y0=min(int(w['top']) for w in ws)
            x1=max(int(w['left'])+int(w['width']) for w in ws); y1=max(int(w['top'])+int(w['height']) for w in ws)
            t=' '.join(w['text'] for w in ws)
            h=y1-y0
            lines.append([round(x0/IW*100,3),round(y0/IH*100,3),round((x1-x0)/IW*100,3),round(h/IH*100,3),round(h*0.95/IW*100,3),t])
        os.remove(png)
    links=[]
    for L in p.get_links():
        r=L['from']; box=[round(r.x0/W*100,3),round(r.y0/H*100,3),round(r.width/W*100,3),round(r.height/H*100,3)]
        if L['kind']==pymupdf.LINK_URI: links.append(box+[L['uri']])
        elif L['kind']==pymupdf.LINK_GOTO: links.append(box+['#p'+str(L['page']+1)])
    pages.append({'n':n,'src':src,'lines':lines,'links':links})
    print(n,src,len(lines),len(links),file=sys.stderr)
json.dump(pages,open(f'{TMP}/../pages.json','w'))
