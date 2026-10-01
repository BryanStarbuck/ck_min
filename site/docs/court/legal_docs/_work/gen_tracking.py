#!/usr/bin/env python3
"""Regenerate tracking.txt for the State v. Robinson legal-document archive.

Walks the filings tree, takes each document's description from its Markdown
conversion, and writes tracking.txt. The hand-written sections at the bottom
(CONFIRMED GAPS onward) are preserved across runs.

    python3 site/docs/court/legal_docs/_work/gen_tracking.py
"""
import hashlib, json, os, re, subprocess, collections, datetime

ROOT = "/Users/bryan/BGit/Bryan_git/charlie-kirk"
FIL  = ROOT + "/site/internals/static/court/filings"
LD   = ROOT + "/site/docs/court/legal_docs"
MD   = LD + "/_markdown"
WORK = LD + "/_work"
OUT  = LD + "/tracking.txt"
HAND_MARKER = "<<<HAND-MAINTAINED SECTIONS BELOW - PRESERVED ACROSS RUNS>>>"

LABEL = {
    "2025":        "Docket filings, Sept-Dec 2025",
    "2026":        "Docket filings, Jan 2026 onward",
    "warrants":    "Search warrants, affidavits and returns",
    "transcripts": "Hearing transcripts (PDF)",
    "mirandize":   "Arrest / Miranda / probable-cause material",
    "analysis":    "NOT PRIMARY SOURCE - commentary and AI analysis, kept apart on purpose",
    "misc":        "Other primary-source material",
    "misc/docket_indexes":        "Docket printouts and index documents",
    "misc/uvu_grama_records":     "Utah Valley University GRAMA record productions",
    "misc/foia_gro":              "FOIA / GRAMA responses",
    "misc/court_press_and_rules": "Court press notices and standing rules",
    "misc/hearing_coverage":      "Hearing coverage material",
    "misc/case_files_undated":    "Case files with no date on the face of the document",
    ".":           "Top level",
}

CAP = re.compile(r"(Case\s*No\.?\s*:?\s*251403576|Case Number\s*:?\s*251403576|"
                 r"Hon\.\s*Tony\s+F\.?\s+Graf|Judge\s+Tony\s+F\.?\s+Graf|Defendant\.?\s*\))", re.I)
NOISE = re.compile(r"(pro hac vice|Telephone:|Facsimile:|Email:|Attorney for|"
                   r"Deputy Utah County Attorneys|#\s?\d{4,5}\b)", re.I)

def describe(rel):
    p = os.path.join(MD, rel[:-4] + ".md")
    if not os.path.exists(p):
        return ""
    raw = open(p, errors="ignore").read()
    raw = raw.split("---\n", 2)[-1]                      # drop our header block
    raw = re.sub(r"<!--.*?-->", " ", raw, flags=re.S)    # drop html comments
    raw = re.sub(r"^\s*\|.*$", " ", raw, flags=re.M)     # drop table rows
    ms = list(CAP.finditer(raw[:6000]))
    body = raw[ms[-1].end():] if ms else raw
    # If we are still sitting in the attorney caption block, jump to the first
    # real sentence of the document instead.
    OPENER = re.compile(
        r"(COMES NOW|Before the court|The State of Utah|Defendant,? by and through|"
        r"Pursuant to|The parties|Plaintiff,? the State|The court|IT IS HEREBY|"
        r"The Deseret News|Defendant Tyler|Attorney [A-Z]|The undersigned|"
        r"NOTICE IS HEREBY|This matter|Now that I have been served|"
        r"I request that the court|The Order of the Court)", re.I)
    m = OPENER.search(body[:6000])
    if m and m.start() > 120:
        body = body[m.start():]
    out, total = [], 0
    for ln in body.split("\n"):
        s = ln.strip().lstrip("#*> ").strip()
        if len(s) < 3: continue
        if NOISE.search(s) and len(s) < 90: continue
        if re.fullmatch(r"[_\-=*/\\.:;,|\s]+", s): continue
        if len(s) < 25 and re.fullmatch(r"[A-Z\s,\.\)\(v]*", s): continue
        out.append(s); total += len(s)
        if total > 700: break
    return re.sub(r"\s+", " ", " ".join(out)).strip()[:480]

def filedate(fn):
    for pat, g in ((r"^\d{3}_(\d{4})-(\d{2})-(\d{2})_", (1,2,3)),
                   (r"^(\d{4})-(\d{2})-(\d{2})", (1,2,3))):
        m = re.match(pat, fn)
        if m: return f"{m.group(g[0])}-{m.group(g[1])}-{m.group(g[2])}"
    m = re.match(r"^(\d{1,2})_(\d{1,2})_(\d{2})_", fn)
    if m:
        try: return f"20{m.group(3)}-{int(m.group(1)):02d}-{int(m.group(2)):02d}"
        except ValueError: return ""
    m = re.match(r"^(\d{4})-(\d{2})", fn)
    return m.group(0) if m else ""

def pagecount(p):
    try:
        info = subprocess.run(["pdfinfo", p], capture_output=True, text=True, timeout=60).stdout
        m = re.search(r"^Pages:\s+(\d+)", info, re.M)
        return int(m.group(1)) if m else None
    except Exception:
        return None

def collect():
    groups = collections.OrderedDict()
    for root, dirs, fns in os.walk(FIL):
        dirs.sort()
        pdfs = sorted(f for f in fns if f.lower().endswith(".pdf"))
        if not pdfs: continue
        sub = os.path.relpath(root, FIL)
        rows = []
        for fn in pdfs:
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, FIL)
            rows.append(dict(fn=fn, rel=rel, bytes=os.path.getsize(p), pages=pagecount(p),
                             date=filedate(fn), desc=describe(rel),
                             sha=hashlib.sha256(open(p, "rb").read()).hexdigest()[:12]))
        rows.sort(key=lambda r: (r["date"] or "9999", r["fn"]))
        groups[sub] = rows
    return groups

def main():
    groups = collect()
    total = sum(len(v) for v in groups.values())
    analysis = sum(len(v) for k, v in groups.items() if k.startswith("analysis"))
    prim = total - analysis
    nmd = sum(1 for _, _, fs in os.walk(MD) for f in fs if f.endswith(".md"))

    docket = []
    dj = os.path.join(WORK, "docket_867.json")
    if os.path.exists(dj):
        docket = json.load(open(dj))

    L = []; w = L.append
    w("=" * 78)
    w("TRACKING - COURT DOCUMENT ARCHIVE")
    w("State of Utah v. Tyler James Robinson, Case No. 251403576")
    w("Fourth Judicial District Court, Utah County, Provo Department")
    w("Hon. Tony F. Graf, Jr.")
    w(f"Generated {datetime.date.today().isoformat()}")
    w("=" * 78)
    w("")
    w("Working index of every court document held in this repository.")
    w("Regenerate the FILES HELD section from the archive on disk with:")
    w("    python3 site/docs/court/legal_docs/_work/gen_tracking.py")
    w("Everything below the hand-maintained sentinel is preserved across runs -")
    w("edit that by hand, and do not hand-edit FILES HELD.")
    w("")
    w("WHERE THINGS LIVE")
    w("  PDFs        site/internals/static/court/filings/<subdir>/")
    w("              served publicly at /court/filings/<subdir>/<name>.pdf")
    w("  Markdown    site/docs/court/legal_docs/_markdown/<same path>.md")
    w("              one .md per PDF, produced by _work/pdf_to_markdown.py")
    w("  Plain text  site/docs/court/legal_docs/_text/")
    w("              pdftotext / OCR sidecars, plus the hearing transcripts")
    w("  Work files  site/docs/court/legal_docs/_work/")
    w("              docket data, fetch logs, per-lane discovery notes")
    w("")
    w("A PDF placed under site/docs/ is NOT served and 404s for every real")
    w("visitor. That is why the PDFs live under site/internals/static/ and only")
    w("the text lives under docs/. The _markdown/, _text/ and _work/ directories")
    w("begin with an underscore, so Docusaurus excludes them from the built site.")
    w("")

    w("-" * 78)
    w("COMPLETENESS SCOREBOARD")
    w("-" * 78)
    if docket:
        dtot = len(docket); dpdf = sum(1 for r in docket if r["has_pdf"])
        dpriv = sum(1 for r in docket if r.get("private"))
        w(f"* Docket entries known to exist ..................... {dtot}")
        w(f"* Of those, marked PRIVATE / sealed on the docket ... {dpriv}")
        w(f"* Entries for which a public PDF was ever posted .... {dpdf}")
        w("")
    w(f"* Unique PDFs held (primary source) ................. {prim}")
    w(f"* Commentary / AI analysis PDFs (NOT source) ........ {analysis}")
    w(f"* Markdown conversions ............................. {nmd}")
    w("")
    w("Read the scoreboard carefully. A large share of the docket entries with no")
    w("public copy are clerical - Returns of Electronic Notification, Requests to")
    w("Submit. The substantive shortfall is the number in CONFIRMED GAPS, not the")
    w("raw arithmetic above.")
    w("")

    w("-" * 78)
    w("FILES HELD")
    w("-" * 78)
    w("Format:")
    w("  * <filename>")
    w("      <date> | <pages> | <bytes> | sha256:<first 12>")
    w("      <what the document says>")
    w("")
    for sub, rows in groups.items():
        w("")
        w(f"### {sub}/  -  {LABEL.get(sub, sub)}   ({len(rows)} files)")
        w("")
        for r in rows:
            w(f"* {r['fn']}")
            pp = f"{r['pages']} pp" if r["pages"] else "? pp"
            w(f"    {r['date'] or 'no date':<10} | {pp:>7} | {r['bytes']:>10,} B | sha256:{r['sha']}")
            w(f"    {r['desc'] or '(no extractable text - open the PDF)'}")
        w("")

    # ---- non-PDF assets: transcripts and exhibit images ----
    TR  = LD + "/_text/transcripts"
    EXH = ROOT + "/site/internals/static/court/exhibits"
    w("-" * 78)
    w("OTHER HELD ASSETS (not PDFs)")
    w("-" * 78)
    w("")
    if os.path.isdir(TR):
        tfs = sorted(f for f in os.listdir(TR) if not f.startswith("."))
        w(f"### Hearing transcripts, text form  ({len(tfs)} files)")
        w("    site/docs/court/legal_docs/_text/transcripts/")
        w("")
        w("    CERTIFIED transcripts are the PDFs in filings/transcripts/ above.")
        w("    Everything in this directory is a TEXT capture - a commercial or")
        w("    community transcription of the pool feed. Useful for searching and")
        w("    for locating a passage. NOT the record and NOT citable as one.")
        w("")
        for f in tfs:
            n = os.path.getsize(os.path.join(TR, f))
            words = 0
            try:
                words = len(open(os.path.join(TR, f), errors="ignore").read().split())
            except Exception:
                pass
            w(f"* {f}")
            w(f"    {n:>10,} B | ~{words:,} words")
        w("")
    if os.path.isdir(EXH):
        w("### Preliminary hearing and case exhibit images")
        w("    site/internals/static/court/exhibits/  ->  served at /court/exhibits/")
        w("")
        w("    These are SCREENSHOTS of exhibits as displayed on the courtroom pool")
        w("    feed. A screenshot of a projected exhibit is not the exhibit - the")
        w("    State's 34 numbered exhibits are still unheld as documents (gap H).")
        w("")
        w("    NOT CURRENTLY EMBEDDED ON ANY PUBLIC PAGE. Several show or name")
        w("    living people. Before any of these is placed on a page, apply the")
        w("    site's defamation rules: presence only, no accusation, crop where")
        w("    needed, and carry the charged-not-convicted disclaimer.")
        w("")
        for d in sorted(os.listdir(EXH)):
            dp = os.path.join(EXH, d)
            if not os.path.isdir(dp): continue
            fs = sorted(os.listdir(dp))
            tot = sum(os.path.getsize(os.path.join(dp, f)) for f in fs)
            w(f"* {d}/  -  {len(fs)} images, {tot:,} B")
            for f in fs:
                w(f"    - {f}")
        w("")

    keep = ""
    if os.path.exists(OUT):
        old = open(OUT, errors="ignore").read()
        i = old.find(HAND_MARKER)
        if i >= 0:
            keep = old[i + len(HAND_MARKER):].lstrip("\n")
    w(HAND_MARKER)
    w("")
    if keep:
        w(keep.rstrip())
    else:
        w("-" * 78)
        w("CONFIRMED GAPS")
        w("-" * 78)
        w("(hand-maintained)")

    open(OUT, "w").write("\n".join(L) + "\n")
    print(f"wrote {OUT}")
    print(f"  {total} PDFs in {len(groups)} directories, {nmd} markdown conversions")

if __name__ == "__main__":
    main()
