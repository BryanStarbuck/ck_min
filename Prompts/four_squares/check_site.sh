#!/bin/bash
# Site-wide Stage 7 check. Enumeration is done in Python: some doc paths contain
# spaces ("/Topics3/South Stairs/"), and shell word-splitting drops or mangles
# them. BSD grep -Z did not reliably NUL-delimit here either.
cd ~/BGit/Bryan_git/charlie-kirk || exit 1
python3 - "$@" <<'PY'
import subprocess, sys
from pathlib import Path
MARKS = ("CK_4SQ_SITEWIDE_START", "CK_INTERESTING_HERE_START",
         "CK_INTERESTING_OTHER_START", "CK_4SQ_SECTION_START")
files = [str(p) for p in Path("site/docs").rglob("*.md*")
         if any(m in p.read_text(encoding="utf-8", errors="replace") for m in MARKS)]
print(f"pages carrying blocks: {len(files)}")
if not files:
    sys.exit(0)
rc = 0
for i in range(0, len(files), 200):          # keep argv well under the limit
    rc |= subprocess.run([sys.executable, "prompts/four_squares/verify_blocks.py",
                          *files[i:i+200]]).returncode
sys.exit(rc)
PY
