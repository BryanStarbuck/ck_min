#!/usr/bin/env python3
"""Repair card alt text truncated by the pre-fix index builder.

The old ALT_RE excluded both quote characters, so an apostrophe inside a
double-quoted alt cut it short ("Page 2 of the State" from "the State's brief").
Cards emitted from that index carry the truncated string. This rewrites the alt
on every generated card to the corrected value keyed by media src.

  --apply   write changes (default is a dry run)
"""
import csv, os, re, sys
from pathlib import Path

ROOT = Path(os.path.expanduser("~/BGit/Bryan_git/charlie-kirk"))
WORK = ROOT / "prompts/four_squares"
APPLY = "--apply" in sys.argv

good = {}
with open(WORK / "card_index.csv", newline="", encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        if r["media_src"] and r["media_alt"]:
            good.setdefault(r["media_src"], r["media_alt"])


def plain(s):
    """Normalise for comparison: entities back to characters, whitespace collapsed."""
    for a, b in (("&amp;", "&"), ("&quot;", '"'), ("&apos;", "'"), ("&mdash;", "-"),
                 ("&ndash;", "-"), ("&rarr;", "->"), ("&lt;", "<"), ("&gt;", ">")):
        s = s.replace(a, b)
    return " ".join(s.split())


def jsx_escape(s):
    return (s.replace("&", "&amp;").replace('"', "&quot;")
             .replace("<", "&lt;").replace(">", "&gt;")
             .replace("'", "&apos;").replace("{", "").replace("}", ""))


BLOCK_RE = re.compile(
    r"(\{/\*|<!--)\s*CK_(?:4SQ_SECTION|4SQ_SITEWIDE|INTERESTING_HERE|INTERESTING_OTHER)_START.*?"
    r"CK_(?:4SQ_SECTION|4SQ_SITEWIDE|INTERESTING_HERE|INTERESTING_OTHER)_END\s*(?:\*/\}|-->)", re.S)
IMG_RE = re.compile(r'<img\s+src="([^"]+)"([^>]*?)alt="([^"]*)"')

files = [p for p in (ROOT / "site/docs").rglob("*.md*")
         if "CK_4SQ_SITEWIDE_START" in p.read_text(encoding="utf-8", errors="replace")
         or "CK_4SQ_SECTION_START" in p.read_text(encoding="utf-8", errors="replace")]

fixed_files, fixed_alts = 0, 0
for p in files:
    t = p.read_text(encoding="utf-8", errors="replace")
    n = [0]

    def fix_block(bm):
        def fix_img(im):
            src, mid, alt = im.group(1), im.group(2), im.group(3)
            want = good.get(src)
            if not want:
                return im.group(0)
            cur_p, want_p = plain(alt), plain(want)
            # Only repair a genuine truncation: the emitted alt is a strict
            # prefix of the real one. Escaping differences are left alone.
            if not (len(cur_p) < len(want_p) and want_p.startswith(cur_p)):
                return im.group(0)
            want_esc = jsx_escape(want)
            n[0] += 1
            return f'<img src="{src}"{mid}alt="{want_esc}"'
        return IMG_RE.sub(fix_img, bm.group(0))

    new = BLOCK_RE.sub(fix_block, t)
    if n[0]:
        fixed_files += 1
        fixed_alts += n[0]
        print(f"{'FIX ' if APPLY else 'WOULD FIX '}{p.relative_to(ROOT)}  ({n[0]} alt)")
        if APPLY:
            p.write_text(new, encoding="utf-8")

print(f"\nfiles touched {fixed_files}, alt attributes repaired {fixed_alts}"
      f"{'' if APPLY else '  (dry run - pass --apply)'}")
