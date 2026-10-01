#!/usr/bin/env python3
"""Generate routes.txt from the REAL build output, not from filenames.

Deriving routes from disk paths is wrong in at least two ways Docusaurus cares
about, both found in production:
  * a leading year like 2026- is NOT a number prefix, so it stays in the route
  * frontmatter id:/slug: overrides the filename entirely
    (court/mirandize/overview.md -> /court/mirandize/mirandize-overview)
site/build/**/*.html is what visitors actually get, so that is the authority.
"""
import os, sys
from pathlib import Path

ROOT = Path(os.path.expanduser("~/BGit/Bryan_git/charlie-kirk"))
BUILD = ROOT / "site/build"
WORK = ROOT / "prompts/four_squares"

if not BUILD.exists():
    sys.exit("site/build missing - run a build, or keep the previous routes.txt")

routes = set()
for p in BUILD.rglob("*.html"):
    rel = p.relative_to(BUILD)
    parts = list(rel.parts)
    if parts[-1] == "index.html":
        parts = parts[:-1]
    else:
        parts[-1] = parts[-1][:-len(".html")]
    routes.add("/" + "/".join(parts) if parts else "/")

(WORK / "routes.txt").write_text("\n".join(sorted(routes)) + "\n")
print(f"routes from build: {len(routes)}")
