#!/usr/bin/env python3
"""
inject_nav_gallery.py  —  Nav galleries on Photos/ and Videos/ overview pages.

For every NON-ROOT overview.mdx under site/docs/Photos and site/docs/Videos this
script inserts (idempotently, between CK_NAV_GALLERY markers) a two-column
gallery of every LEAF media page that lives in that overview's subtree.

  * A "leaf" page is an Img_*.mdx (photos) or Vid_*.mdx (videos) file.
  * The gallery is placed right ABOVE the "Related Areas" section (before the
    CK_NAV_START marker on video pages, before "## Related Areas" on photo pages)
    and BELOW the in-body table of contents, which is left untouched on top.
  * Each tile is the leaf's own image (photos) or its video poster (videos),
    sized to fill its column at full width with the real aspect ratio preserved
    (aspect-ratio computed here from the actual pixels), and it links to the
    leaf page. Images alternate left / right across the two columns and cascade
    down the page until every leaf in the subtree is shown.
  * The right table-of-contents sidebar is turned off on these pages
    (hide_table_of_contents: true) so the gallery fills the main column.

A Level-3 overview therefore shows every leaf beneath it across all of its
Level-4 sub-sections plus any leaves it holds directly; a Level-4 overview shows
its own direct leaves. Deeper overviews follow the same rule.

Re-runnable: an existing gallery block is replaced, so prose is never touched.
"""

import os
import re
import sys

REPO = os.path.expanduser("~/BGit/Bryan_git/charlie-kirk")
DOCS = os.path.join(REPO, "site/docs")
STATIC = os.path.join(REPO, "site/internals/static")

from PIL import Image

START = "{/* CK_NAV_GALLERY_START */}"
END = "{/* CK_NAV_GALLERY_END */}"

SECTIONS = {
    "Photos": {
        "leaf_prefix": "Img_",
        # The main evidence image. Usually a local /img/evidence/<sha>.<ext>,
        # but some leaves point straight at an IPFS gateway URL — accept both.
        "src_re": re.compile(r'<img className="ck-evidence-image"[^>]*\ssrc="([^"]+)"'),
    },
    "Videos": {
        "leaf_prefix": "Vid_",
        "src_re": re.compile(r'poster="(/img/video_posters/[^"]+)"'),
    },
}

_dim_cache = {}


def dims_for(src):
    """Return (w, h) for a /img/... web path, or None. Cached."""
    if src in _dim_cache:
        return _dim_cache[src]
    fs = os.path.join(STATIC, src.lstrip("/"))
    wh = None
    try:
        with Image.open(fs) as im:
            wh = im.size
    except Exception:
        wh = None
    _dim_cache[src] = wh
    return wh


def read(path):
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def frontmatter_title(text):
    m = re.search(r'^title:\s*"?(.*?)"?\s*$', text, re.MULTILINE)
    if not m:
        return "image"
    t = m.group(1)
    # Decode \uXXXX escapes that YAML double-quoting left in place.
    try:
        t = t.encode("latin-1", "backslashreplace").decode("unicode_escape")
    except Exception:
        pass
    return t


def frontmatter_slug(text):
    m = re.search(r'^slug:\s*"?(.*?)"?\s*$', text, re.MULTILINE)
    return m.group(1).strip() if m else None


def route_from_path(path):
    rel = os.path.relpath(path, DOCS)
    if rel.endswith(".mdx"):
        rel = rel[:-4]
    elif rel.endswith(".md"):
        rel = rel[:-3]
    return "/" + rel


def parse_leaf(path, src_re):
    """Return dict(link, src, alt, w, h) for a leaf media page, or None."""
    text = read(path)
    m = src_re.search(text)
    if not m:
        return None
    src = m.group(1)
    link = frontmatter_slug(text) or route_from_path(path)
    alt = frontmatter_title(text)
    wh = dims_for(src)
    return {
        "link": link,
        "src": src,
        "alt": alt,
        "w": wh[0] if wh else None,
        "h": wh[1] if wh else None,
    }


def collect_leaves(dir_path, leaf_prefix, src_re):
    """Leaves under dir_path, recursively: direct leaves first (sorted), then
    each sub-section's leaves (sub-sections sorted). Cascades down the page."""
    out = []
    entries = sorted(os.listdir(dir_path))
    files = [e for e in entries if e.endswith(".mdx") and e.startswith(leaf_prefix)]
    subdirs = [e for e in entries if os.path.isdir(os.path.join(dir_path, e))]
    for f in files:
        leaf = parse_leaf(os.path.join(dir_path, f), src_re)
        if leaf:
            out.append(leaf)
    for d in subdirs:
        out.extend(collect_leaves(os.path.join(dir_path, d), leaf_prefix, src_re))
    return out


def esc(s):
    s = s or ""
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def build_block(leaves):
    lines = [START, "", '<div className="ck-nav-gallery">']
    for lf in leaves:
        ar = ""
        if lf["w"] and lf["h"]:
            ar = f' style={{{{aspectRatio: "{lf["w"]} / {lf["h"]}"}}}}'
        lines.append(
            f'  <a className="ck-nav-tile" href="{lf["link"]}">'
            f'<img src="{lf["src"]}" alt="{esc(lf["alt"])}" loading="lazy"{ar} /></a>'
        )
    lines.append("</div>")
    lines.append("")
    lines.append(END)
    return "\n".join(lines)


def ensure_hide_toc(text):
    """Set hide_table_of_contents: true inside the leading frontmatter."""
    m = re.match(r'^---\n(.*?)\n---\n', text, re.DOTALL)
    if not m:
        return text
    fm = m.group(1)
    if re.search(r'^hide_table_of_contents:', fm, re.MULTILINE):
        fm2 = re.sub(r'^hide_table_of_contents:.*$',
                     'hide_table_of_contents: true', fm, flags=re.MULTILINE)
    else:
        fm2 = fm + "\nhide_table_of_contents: true"
    return text[:m.start(1)] + fm2 + text[m.end(1):]


def strip_existing(text):
    return re.sub(re.escape(START) + r'.*?' + re.escape(END) + r'\n?',
                  "", text, flags=re.DOTALL)


def insert_before_anchor(text, block):
    """Insert block right before the Related-Areas region."""
    for anchor in ("{/* CK_NAV_START */}", "## Related Areas"):
        idx = text.find(anchor)
        if idx != -1:
            # Back up over blank lines so spacing stays clean.
            j = idx
            while j > 0 and text[j - 1] == "\n":
                j -= 1
            return text[:j] + "\n\n" + block + "\n\n" + text[idx:]
    return None


def process(section, dry):
    cfg = SECTIONS[section]
    root = os.path.join(DOCS, section)
    root_overview = os.path.join(root, "overview.mdx")
    changed = 0
    skipped = 0
    for cur, _dirs, files in os.walk(root):
        if "overview.mdx" not in files:
            continue
        ov = os.path.join(cur, "overview.mdx")
        if os.path.abspath(ov) == os.path.abspath(root_overview):
            continue  # never the Level-2 root (would be the whole corpus)
        leaves = collect_leaves(cur, cfg["leaf_prefix"], cfg["src_re"])
        if not leaves:
            skipped += 1
            continue
        text = read(ov)
        text = strip_existing(text)
        block = build_block(leaves)
        new = insert_before_anchor(text, block)
        if new is None:
            print(f"  ! no anchor, skipped: {ov}")
            skipped += 1
            continue
        new = ensure_hide_toc(new)
        if not dry:
            with open(ov, "w", encoding="utf-8") as fh:
                fh.write(new)
        changed += 1
    print(f"{section}: {changed} overview pages updated, {skipped} skipped")


if __name__ == "__main__":
    dry = "--dry" in sys.argv
    which = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not which:
        which = ["Photos", "Videos"]
    for s in which:
        process(s, dry)
