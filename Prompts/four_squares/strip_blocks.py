#!/usr/bin/env python3
"""Remove all four generated blocks from a page, restoring it to pre-run state.

Used when a file turns out not to be a published page after all.
"""
import re, sys
from pathlib import Path

NAMES = ["CK_INTERESTING_HERE", "CK_INTERESTING_OTHER", "CK_4SQ_SECTION", "CK_4SQ_SITEWIDE"]
n_files = 0
for f in sys.argv[1:]:
    p = Path(f)
    t = orig = p.read_text(encoding="utf-8")
    for name in NAMES:
        t = re.sub(r"\n*(?:\{/\*|<!--)\s*" + name + r"_START\s*(?:\*/\}|-->).*?"
                   r"(?:\{/\*|<!--)\s*" + name + r"_END\s*(?:\*/\}|-->)\n*", "\n\n", t, flags=re.S)
    t = re.sub(r"\n{4,}", "\n\n\n", t)
    if t != orig:
        p.write_text(t, encoding="utf-8")
        n_files += 1
        print("stripped", f)
print(f"{n_files} files stripped")
