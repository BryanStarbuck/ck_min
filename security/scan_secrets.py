#!/usr/bin/env python3
"""Scan tracked files for credentials that should never be in this repo.

Credentials for this investigation live OUTSIDE every git repo, in
~/.credentials/charlie_kirk.json (mode 600), and are read at run time by
site/docs/Planes/following/apis/public_open_source/code/lib/credentials.js.

Run it by hand, or let the pre-commit hook run it:

    python3 security/scan_secrets.py            # scan every tracked file
    python3 security/scan_secrets.py --staged   # scan what is about to be committed

Exit 0 = clean. Exit 1 = at least one finding. Findings print the file, the line
number and the pattern that matched -- NEVER the secret itself.

ARCHIVED CAPTURES ARE SCANNED TOO -- and this is the part that changed.

Archived copies of flight-tracking pages under site/docs/Planes/*/data/recovered/
carry the VENDOR'S own client-side keys, baked into the HTML those sites served
to the public: Flightradar24's Firebase web key, FlightAware's Mapbox token,
Stadia Maps key and Vicinity token. Those keys are theirs and were already public
on their own sites, so this script used to skip those paths entirely and said so.

That was wrong in one practical respect: GitHub push protection does not care
whose key it is. On 2026-08-24 it rejected the push of the entire investigation
over FlightAware's Mapbox token in
site/docs/Planes/N102DZ/data/recovered/N102DZ_20260114192750_wayback_flightaware.html.
A scanner that passes a commit the remote will refuse is not protecting anything.

So captures are now scanned, and the fix is redaction rather than deletion:
security/scrub_vendor_tokens.py replaces just the VALUE with
__REDACTED_VENDOR_CREDENTIAL_sha256_<16 hex>__, leaving the key name, the markup
and every byte of flight data untouched. The fingerprint is one-way but stable,
so "this page served the same key as that page" is still provable. The evidence
survives; the credential does not.

Captures are scanned with the SHAPE patterns only -- the same unmistakable
formats GitHub itself blocks on. The looser "a name containing key/token is
being assigned something random" heuristic is not applied to them, because raw
ADS-B traces are full of random-looking values that are position data, not
secrets, and 1,000 false positives train people to ignore the scanner.
"""
import argparse
import re
import subprocess
import sys

# (name, compiled pattern). Anchored on shapes that are unambiguous credentials.
PATTERNS = [
    ("google-api-key",      re.compile(rb"AIza[0-9A-Za-z_\-]{35}")),
    ("aws-access-key-id",   re.compile(rb"AKIA[0-9A-Z]{16}")),
    ("github-token",        re.compile(rb"gh[pousr]_[A-Za-z0-9]{36,}")),
    ("slack-token",         re.compile(rb"xox[abposr]-[A-Za-z0-9-]{10,}")),
    # Real OpenAI keys are base62 with no hyphens in the body. Requiring that
    # is what keeps podcast slugs like "sk-us-anything-254-charlie-and-aliens"
    # out of the report -- 490 of them matched before this was tightened.
    ("openai-key",          re.compile(rb"sk-(?:proj-|svcacct-)?[A-Za-z0-9]{32,}")),
    ("anthropic-key",       re.compile(rb"sk-ant-[A-Za-z0-9_\-]{32,}")),
    ("google-oauth-secret", re.compile(rb"GOCSPX-[A-Za-z0-9_\-]{20,}")),
    ("rapidapi-key",        re.compile(rb"[0-9a-f]{32}msh[0-9a-f]{16}")),
    ("private-key-block",   re.compile(rb"-----BEGIN (?:RSA |EC |OPENSSH |PGP )?PRIVATE KEY")),
    ("jwt",                 re.compile(rb"eyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}")),
]

# A named-looking credential being ASSIGNED a value. Handled apart from the
# shape patterns above because the shape of the VALUE is what decides it: the
# name may be anything containing key/token/secret/password, with or without a
# vendor prefix (FR24_API_TOKEN, OPENSKY_CLIENT_SECRET, apiKey, db_password),
# and group 1 is the value we then test for randomness.
ASSIGNED = re.compile(
    rb"""(?i)[A-Za-z0-9_.\[\]"']{0,40}"""
    rb"""(?:api[_-]?key|apikey|[_-]?token|secret|password|passwd|passphrase|client[_-]?id)"""
    rb"""[A-Za-z0-9_]{0,20}["']?\s*[:=]\s*["']?([A-Za-z0-9/+_.\-]{16,})["']?""")


def looks_random(value: bytes) -> bool:
    """A credential value, as opposed to a sentence, a path or a placeholder."""
    if len(value) < 16:
        return False
    if PLACEHOLDER.search(value):
        return False
    has_digit = any(c in b"0123456789" for c in value)
    has_alpha = any(chr(c).isalpha() for c in value)
    # Hyphen-and-word slugs ("us-anything-254-charlie-and-aliens") are prose,
    # not keys. Real credentials do not read as words separated by hyphens.
    wordy = len([w for w in re.split(rb"[-_.]", value) if w.isalpha() and len(w) > 2]) >= 3
    return has_digit and has_alpha and not wordy

# Paths not scanned at all: this script (it contains the patterns themselves),
# its redacting twin, and vendored dependencies we do not author.
SKIP = (
    re.compile(r"^security/scan_secrets\.py$"),
    re.compile(r"^security/scrub_vendor_tokens\.py$"),
    re.compile(r"(^|/)node_modules/"),
)

# Verbatim third-party captures. Scanned, but with the shape patterns only --
# see the module docstring for why the assigned-secret heuristic is held back.
CAPTURE = (
    re.compile(r"/data/recovered/"),
    re.compile(r"/data/adsb/"),
    re.compile(r"/captures/"),
)

# The marker scrub_vendor_tokens.py leaves behind. Never a finding.
REDACTED = re.compile(rb"__REDACTED_VENDOR_CREDENTIAL_sha256_[0-9a-f]{16}__")

# Placeholder values that look like assignments but carry nothing.
PLACEHOLDER = re.compile(rb"(?i)(your[_-]?|example|placeholder|xxxx|<[a-z_]+>|redacted|changeme|\.{3})")


def tracked(staged: bool) -> list[str]:
    cmd = ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"] if staged \
        else ["git", "ls-files"]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    return [p for p in out.splitlines() if p]


def scan(path: str) -> list[tuple[int, str]]:
    if any(rx.search(path) for rx in SKIP):
        return []
    is_capture = any(rx.search(path) for rx in CAPTURE)
    try:
        with open(path, "rb") as fh:
            data = fh.read()
    except (OSError, IsADirectoryError):
        return []
    if b"\0" in data[:8192]:          # binary
        return []
    hits = []
    for lineno, line in enumerate(data.splitlines(), 1):
        if len(line) > 20000:
            continue
        matched = False
        for name, rx in PATTERNS:
            m = rx.search(line)
            if m and not PLACEHOLDER.search(m.group(0)) and not REDACTED.search(line):
                hits.append((lineno, name))
                matched = True
                break
        if matched:
            continue
        if is_capture:
            continue
        m = ASSIGNED.search(line)
        if m and looks_random(m.group(1)):
            hits.append((lineno, "assigned-secret"))
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--staged", action="store_true",
                    help="scan only files staged for commit")
    args = ap.parse_args()

    findings = 0
    for path in tracked(args.staged):
        for lineno, name in scan(path):
            print(f"{path}:{lineno}: possible {name}")
            findings += 1

    if findings:
        print()
        print(f"{findings} possible credential(s) found. NOTHING IS PRINTED ABOVE EXCEPT THE LOCATION.")
        print("Move the value to ~/.credentials/charlie_kirk.json (chmod 600) and read it through")
        print("site/docs/Planes/following/apis/public_open_source/code/lib/credentials.js.")
        print("If it is a THIRD-PARTY key inside an archived capture, do not skip it and do not")
        print("delete the file -- run:  python3 security/scrub_vendor_tokens.py")
        print("which redacts the value in place and leaves the capture otherwise intact.")
        return 1
    print("clean: no credentials found in "
          + ("staged files" if args.staged else "tracked files"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
