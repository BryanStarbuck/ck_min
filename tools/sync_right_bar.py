#!/usr/bin/env python3
"""
sync_right_bar.py — copy the right-bar wording into the site.

The right bar (the notice rail on every page) gets its wording from ONE file
outside this repo:

    ~/BGit/all/politics/charlie_kirk/ck/docusaurus/right_bar.txt

That file is the source of truth, and this script only ever READS it. It writes
the site-side copy:

    site/internals/src/data/right_bar.json

which is committed, so the GitHub Pages build never needs the external file.
The rail component (site/internals/src/components/CitizenNotice/) renders only
what is in that JSON, so the whole update is: edit right_bar.txt, run this,
commit.

    python3 tools/sync_right_bar.py [path/to/right_bar.txt]

HOW THE TEXT FILE IS READ
  * Paragraphs are separated by blank lines. Line breaks inside a paragraph are
    joined with spaces.
  * A paragraph that is only an email address, or a line like "Email me at:"
    followed by an address, becomes the email link (a mailto: link on the
    site). Any label before the address ("Email me at:") is kept as the label.
  * The paragraph just before the email is the call to action (the corrections
    half of the rail). The first paragraph is the lead. Everything in between
    is body text.
  * TRANSCRIPTION_FIXES holds known voice-transcription errors. They are fixed
    on the way into the site only; the text file is never changed.
"""
import json
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = Path.home() / "BGit/all/politics/charlie_kirk/ck/docusaurus/right_bar.txt"
OUTPUT = ROOT_DIR / "site/internals/src/data/right_bar.json"

# Voice-transcription errors seen in right_bar.txt. Site copy only.
TRANSCRIPTION_FIXES = [
    # Utah's public-records law is GRAMA (Government Records Access and Management Act).
    (re.compile(r"\bGamma requests\b"), "GRAMA requests"),
    (re.compile(r"\s+period\.", re.IGNORECASE), "."),
]

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")


def clean(text: str) -> str:
    text = " ".join(text.split())
    for pattern, replacement in TRANSCRIPTION_FIXES:
        text = pattern.sub(replacement, text)
    return text


def parse(raw: str) -> dict:
    paragraphs = [clean(p) for p in re.split(r"\n\s*\n", raw) if p.strip()]

    email = email_label = None
    email_index = None
    for i, para in enumerate(paragraphs):
        match = EMAIL_RE.search(para)
        # Only a short paragraph that is essentially the address counts as the
        # contact line — an address quoted inside a sentence stays body text.
        if match and len(para) - len(match.group(0)) <= 40:
            email = match.group(0)
            email_label = para[: match.start()].strip() or None
            email_index = i
            break
    if email is None:
        sys.exit("ERROR: no email address found in the right bar text.")

    before = paragraphs[:email_index]
    if len(before) < 2:
        sys.exit("ERROR: expected a lead paragraph and a call to action before the email.")

    return {
        "_generated_by": "tools/sync_right_bar.py — do not hand-edit; edit right_bar.txt and re-run",
        "lead": before[0],
        "body": before[1:-1],
        "action": before[-1],
        "email_label": email_label,
        "email": email,
    }


def main() -> None:
    source = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else DEFAULT_SOURCE
    if not source.is_file():
        sys.exit(f"ERROR: {source} not found.")
    data = parse(source.read_text(encoding="utf-8"))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    new = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    old = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else None
    if new == old:
        print(f"unchanged: {OUTPUT.relative_to(ROOT_DIR)}")
        return
    OUTPUT.write_text(new, encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT_DIR)} from {source}")
    print(f"  lead + {len(data['body'])} body paragraphs + action + {data['email']}")


if __name__ == "__main__":
    main()
