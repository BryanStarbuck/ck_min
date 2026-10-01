#!/usr/bin/env python3
"""Convert every archived court PDF to Markdown.

Uses pymupdf4llm, which reads the PDF's own text and layout objects and emits
Markdown with real pipe tables where it detects a table. That matters here
because the exhibit lists, witness lists and restitution notices are column
data - a naive text dump collapses those columns into unreadable runs.

Pandoc is NOT usable for this: pandoc has no PDF *reader*, it can only write
PDF. For a scanned, image-only filing there is no text layer at all, so those
fall back to the OCR sidecar text already produced by ocrmypdf.

Output mirrors the filings tree:
  site/internals/static/court/filings/2026/foo.pdf
  -> site/docs/court/legal_docs/_markdown/2026/foo.md

Re-runnable: skips a .md that is newer than its .pdf unless --force.
"""
import os, sys, re, datetime, subprocess

ROOT = "/Users/bryan/BGit/Bryan_git/charlie-kirk"
FIL  = ROOT + "/site/internals/static/court/filings"
OUT  = ROOT + "/site/docs/court/legal_docs/_markdown"
OCR  = ROOT + "/site/docs/court/legal_docs/_text"
FORCE = "--force" in sys.argv

import pymupdf4llm, pymupdf

def ocr_fallback(rel):
    """Find OCR/pdftotext sidecar text already extracted for this PDF."""
    base = os.path.basename(rel)[:-4] + ".txt"
    sub = rel.split("/")[0]
    for cand in (os.path.join(OCR, sub, base), os.path.join(OCR, "other", base)):
        if os.path.exists(cand):
            t = open(cand, errors="ignore").read().strip()
            if t:
                return t
    return ""

def convert(rel):
    src = os.path.join(FIL, rel)
    dst = os.path.join(OUT, rel[:-4] + ".md")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if not FORCE and os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
        return "skip", 0

    try:
        doc = pymupdf.open(src)
        pages = doc.page_count
        doc.close()
    except Exception as e:
        return f"open-error:{e}", 0

    md, how = "", "pymupdf4llm"
    try:
        md = pymupdf4llm.to_markdown(src, show_progress=False, table_strategy="lines_strict")
    except Exception:
        try:
            md = pymupdf4llm.to_markdown(src, show_progress=False)
        except Exception as e:
            md, how = "", f"convert-error:{e}"

    stripped = re.sub(r"[\s\-\|_]+", "", md or "")
    if len(stripped) < 40:
        alt = ocr_fallback(rel)
        if alt:
            md = alt
            how = "ocr-sidecar (no text layer in the PDF - this is a scanned/signed image filing)"
        else:
            how = "NO TEXT RECOVERED"

    hdr = (
        f"<!-- Converted from {rel} -->\n"
        f"# {os.path.basename(rel)[:-4].replace('_',' ')}\n\n"
        f"> **Source PDF:** `court/filings/{rel}` — served at `/court/filings/{rel}`  \n"
        f"> **Pages:** {pages}  \n"
        f"> **Converted:** {datetime.date.today().isoformat()} by `_work/pdf_to_markdown.py` ({how})  \n"
        f"> This Markdown is a machine conversion for searching and quoting. "
        f"The PDF is the record; where they differ, the PDF governs.\n\n"
        f"---\n\n"
    )
    open(dst, "w").write(hdr + (md or "").strip() + "\n")
    return how, len(md or "")

def main():
    rels = []
    for root, _, fns in os.walk(FIL):
        for fn in sorted(fns):
            if fn.lower().endswith(".pdf"):
                rels.append(os.path.relpath(os.path.join(root, fn), FIL))
    rels.sort()
    counts = {}
    empty = []
    for i, rel in enumerate(rels, 1):
        how, n = convert(rel)
        key = how.split(":")[0].split(" ")[0]
        counts[key] = counts.get(key, 0) + 1
        if how == "NO TEXT RECOVERED":
            empty.append(rel)
        if i % 50 == 0:
            print(f"  {i}/{len(rels)}", flush=True)
    print(f"\nconverted {len(rels)} PDFs -> {OUT}")
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {v:>4}  {k}")
    if empty:
        print(f"\n{len(empty)} with NO text recovered (need OCR):")
        for e in empty:
            print("   ", e)

if __name__ == "__main__":
    main()
