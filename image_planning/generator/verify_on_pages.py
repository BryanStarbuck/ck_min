#!/usr/bin/env python3
"""Verify Stage 8 (on_pages) coverage in images/images.yaml.

Walks every publishable page OUTSIDE the images Level 2 (site/docs excluding
Photos, plus site/src and site/blog), finds every embedded image, resolves it to
a corpus entry three ways — /img/evidence/<sha256>, IPFS CID, and sha256 of the
local static file it points at — and reports every (page, image) pair where the
image IS in the YAML but the page is NOT listed in that image's on_pages.

A clean run prints "MISSING (page,image): 0". Any MISSING line is a real gap:
a page hosts a corpus image that on_pages fails to record. Read-only; never
writes. Run from anywhere:  python3 verify_on_pages.py
"""
import os, re, yaml, hashlib
from collections import defaultdict

ROOT = os.path.expanduser("~/BGit/Bryan_git/charlie-kirk")
HOME = os.path.expanduser("~")
YAML = os.path.join(ROOT, "images", "images.yaml")
STATIC = [os.path.join(ROOT, "site", "internals", "static"),
          os.path.join(ROOT, "site", "static")]
SCAN_ROOTS = [os.path.join(ROOT, "site", "docs"),
              os.path.join(ROOT, "site", "src"),
              os.path.join(ROOT, "site", "blog")]
SKIP = {"node_modules", "build", ".git", ".docusaurus"}
PAGE_EXT = (".md", ".mdx", ".tsx", ".jsx", ".ts", ".js", ".html")
IMG_EXT = (".jpg", ".jpeg", ".png", ".webp", ".gif")

RE_EVID = re.compile(r"/img/evidence/([0-9a-f]{64})")
RE_IPFS = re.compile(r"(?:ipfs\.io/ipfs/|ipfs://|dweb\.link/ipfs/)([A-Za-z0-9]{40,})"
                     r"|([A-Za-z0-9]{46,})\.ipfs\.dweb\.link")
RE_IMG  = re.compile(r'<img\b[^>]*?\bsrc\s*=\s*["\']([^"\']+)["\']', re.I)
RE_MD   = re.compile(r"!\[[^\]]*\]\(([^)\s]+)")
RE_VID  = re.compile(r'<(?:iframe|video|source)\b[^>]*?\bsrc\s*=\s*["\']([^"\']+)["\']', re.I)


def load_inners():
    doc = yaml.safe_load(open(YAML, encoding="utf-8"))
    out = []

    def walk(node):
        if not isinstance(node, dict):
            return
        for kind in ("images", "videos"):
            for mm in (node.get(kind) or []):
                if isinstance(mm, dict):
                    inner = mm.get("image") or mm.get("video")
                    if isinstance(inner, dict):
                        out.append(inner)
        for k, v in node.items():
            if re.fullmatch(r"level_\d+", k) and isinstance(v, list):
                for c in v:
                    if isinstance(c, dict):
                        walk(c.get(k, c))
    for top in (doc.get("level_3") or []):
        if isinstance(top, dict):
            walk(top.get("level_3", top))
    return out


def curpages(inner):
    out = set()
    for x in (inner.get("on_pages") or []):
        p = x.get("page") if isinstance(x, dict) else x
        if p:
            out.add(p)
    return out


_scache = {}
def sha_local(url, page_full):
    if not url or url.startswith(("http://", "https://", "ipfs://", "//")) or "ipfs" in url:
        return None
    clean = url.split("?", 1)[0].split("#", 1)[0]
    if not clean.lower().endswith(IMG_EXT) or "/img/evidence/" in clean:
        return None
    cands = ([os.path.join(b, clean.lstrip("/")) for b in STATIC] if clean.startswith("/")
             else [os.path.normpath(os.path.join(os.path.dirname(page_full), clean))])
    for c in cands:
        if os.path.isfile(c):
            if c not in _scache:
                _scache[c] = hashlib.sha256(open(c, "rb").read()).hexdigest()
            return _scache[c]
    return None


def main():
    inners = load_inners()
    sha_map = defaultdict(list)
    cid_map = defaultdict(list)
    for i in inners:
        s = (i.get("sha256") or "").lower().strip()
        c = (i.get("cid") or "").strip()
        if s:
            sha_map[s].append(i)
        if c:
            cid_map[c].append(i)

    present = 0
    missing = []
    for sroot in SCAN_ROOTS:
        if not os.path.isdir(sroot):
            continue
        for dp, dns, fns in os.walk(sroot):
            dns[:] = [d for d in dns if d not in SKIP]
            if os.sep + "Photos" in dp:
                continue
            for fn in fns:
                if not fn.endswith(PAGE_EXT):
                    continue
                full = os.path.join(dp, fn)
                txt = open(full, errors="replace").read()
                tp = full.replace(HOME, "~")
                rel = os.path.relpath(full, ROOT)
                sha_form = {}
                for m in RE_EVID.finditer(txt):
                    h = m.group(1).lower()
                    if h in sha_map:
                        sha_form.setdefault(h, "evid")
                for m in RE_IPFS.finditer(txt):
                    cid = m.group(1) or m.group(2)
                    for i in cid_map.get(cid, []):
                        s = (i.get("sha256") or "").lower()
                        if s:
                            sha_form.setdefault(s, "cid")
                for rx in (RE_IMG, RE_MD, RE_VID):
                    for m in rx.finditer(txt):
                        h = sha_local(m.group(1), full)
                        if h and h in sha_map:
                            sha_form.setdefault(h, "local")
                for sha, form in sha_form.items():
                    if any(tp in curpages(i) for i in sha_map[sha]):
                        present += 1
                    else:
                        missing.append((rel, sha, form))

    print("=" * 28)
    print("VERIFY on_pages")
    print(f"Corpus image entries: {len(inners)}   unique sha: {len(sha_map)}")
    print(f"(page,image) bindings correctly present: {present}")
    print(f"MISSING (page,image): {len(missing)}")
    for rel, sha, form in sorted(missing):
        print(f"  MISSING [{form:5}] {rel}  sha={sha[:16]}")
    print("=" * 28)
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
