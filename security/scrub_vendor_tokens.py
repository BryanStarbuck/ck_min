#!/usr/bin/env python3
"""Redact THIRD-PARTY vendor credentials out of archived flight-tracker captures.

WHY THIS EXISTS
---------------
Nothing here is ours. The captures under site/docs/Planes/*/data/recovered/ are
verbatim archives of what Flightradar24 / FlightAware served to the public on the
day we pulled them, and those pages ship their own client-side keys inside the
HTML: FlightAware's Mapbox token, its Stadia Maps key, its Vicinity token,
Flightradar24's Firebase web key. They were already public on the vendor's own
site. They are still credentials, and GitHub push protection rejects a push that
carries one -- which on 2026-08-24 blocked the whole investigation from being
published over FlightAware's Mapbox token in
N102DZ_20260114192750_wayback_flightaware.html.

So we redact the VALUE and keep everything else. The key NAME stays, the
surrounding markup stays byte-for-byte, and in place of the value we write

    __REDACTED_VENDOR_CREDENTIAL_sha256_<first 16 hex of sha256(value)>__

The fingerprint is one-way: it cannot be turned back into the token, but two
captures that carried the same vendor key still fingerprint identically, so the
evidentiary chain -- "this page served the same key as that page" -- survives
the redaction. That is the whole point. We lose the secret, not the proof.

USAGE
-----
    python3 security/scrub_vendor_tokens.py              # scrub every capture
    python3 security/scrub_vendor_tokens.py --check      # report only, change nothing
    python3 security/scrub_vendor_tokens.py path ...     # scrub named paths

Exit 0 = nothing left to redact. Exit 1 = --check found unredacted credentials.
Output names the file, the line and the pattern. It NEVER prints a value.
"""
import argparse
import hashlib
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directories holding verbatim third-party captures.
CAPTURE_DIRS = ("/data/recovered/", "/data/adsb/", "/captures/")
CAPTURE_EXTS = (".html", ".htm", ".json", ".txt", ".js")

MARK = "__REDACTED_VENDOR_CREDENTIAL_sha256_"
ALREADY = re.compile(re.escape(MARK) + r"[0-9a-f]{16}__")

# 1. Shape patterns -- unmistakable credential formats, redacted wherever they
#    appear, including inside a URL query string such as ?access_token=pk.eyJ...
SHAPES = [
    ("mapbox-token",      re.compile(r"\b(?:pk|sk)\.eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+")),
    ("mapbox-token",      re.compile(r"\b(?:pk|sk)\.eyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{10,}")),
    ("google-api-key",    re.compile(r"\bAIza[0-9A-Za-z_\-]{35}\b")),
    ("aws-access-key-id", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("github-token",      re.compile(r"\bgh[pousr]_[A-Za-z0-9]{36,}\b")),
    ("slack-token",       re.compile(r"\bxox[abposr]-[A-Za-z0-9-]{10,}")),
    ("jwt",               re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}")),
]

# 2. Named assignments -- the value shape alone is not conclusive (a UUID, a hex
#    blob), so the NAME is what marks it as a credential. Deliberately a curated
#    list: over-redaction would damage the capture, which is the thing we are
#    trying to preserve.
NAMED = re.compile(
    r"""(?ix)
    (["']?)                                   # 1 opening quote around the name
    ( MAPBOX_(?:API|ACCESS)_TOKEN
    | STADIA_MAPS_API_KEY
    | VICINITY_TOKEN
    | GOOGLE_MAPS_API_KEY
    | MAPTILER_KEY
    | api[_-]?key | apikey
    | access[_-]?token | auth[_-]?token | bearer[_-]?token
    | client[_-]?secret
    )
    \1                                        # matching closing quote
    (\s*[:=]\s*)                              # 3 the separator
    (["'])                                    # 4 opening quote around the value
    ([^"'\s]{16,})                            # 5 THE VALUE
    \4                                        # matching closing quote
    """)

# A value that carries nothing -- a placeholder, a path, a word. Redacting one
# of these would be noise in the diff and would not remove any secret.
PLACEHOLDER = re.compile(
    r"(?i)^(?:your|my|the|test|demo|sample|example|placeholder|dummy|fake|none|null|"
    r"undefined|changeme|xxx+|\.\.\.|<|\{|\$)")


def fingerprint(value: str) -> str:
    return MARK + hashlib.sha256(value.encode("utf-8", "replace")).hexdigest()[:16] + "__"


def is_credential_value(value: str) -> bool:
    """A real credential value, as opposed to a placeholder or a plain word."""
    if len(value) < 16 or PLACEHOLDER.match(value) or ALREADY.search(value):
        return False
    if "/" in value or value.startswith("http"):
        return False
    has_digit = any(c.isdigit() for c in value)
    has_alpha = any(c.isalpha() for c in value)
    # "us-anything-254-charlie-and-aliens" reads as words; a key does not.
    wordy = len([w for w in re.split(r"[-_.]", value) if w.isalpha() and len(w) > 2]) >= 3
    return has_digit and has_alpha and not wordy


def scrub_text(text: str):
    """Return (new_text, [(pattern_name, line_number), ...])."""
    findings = []

    def note(name, start):
        findings.append((name, text.count("\n", 0, start) + 1))

    for name, pattern in SHAPES:
        def repl(m, _name=name):
            note(_name, m.start())
            return fingerprint(m.group(0))
        text = pattern.sub(repl, text)

    def named_repl(m):
        value = m.group(5)
        if not is_credential_value(value):
            return m.group(0)
        note("named:" + m.group(2).lower(), m.start())
        return f"{m.group(1)}{m.group(2)}{m.group(1)}{m.group(3)}{m.group(4)}{fingerprint(value)}{m.group(4)}"

    text = NAMED.sub(named_repl, text)
    return text, findings


def capture_files(paths):
    if paths:
        for p in paths:
            yield os.path.abspath(p)
        return
    for root, dirs, files in os.walk(REPO):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "build")]
        path = root.replace(os.sep, "/") + "/"
        if not any(marker in path for marker in CAPTURE_DIRS):
            continue
        for name in files:
            if name.lower().endswith(CAPTURE_EXTS):
                yield os.path.join(root, name)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("paths", nargs="*", help="files to scrub (default: every capture)")
    ap.add_argument("--check", action="store_true", help="report only, write nothing")
    args = ap.parse_args()

    scanned = changed = total = 0
    for path in sorted(capture_files(args.paths)):
        try:
            original = open(path, encoding="utf-8", errors="surrogateescape").read()
        except (OSError, UnicodeError) as exc:
            print(f"skip  {path}: {exc}", file=sys.stderr)
            continue
        scanned += 1
        scrubbed, findings = scrub_text(original)
        if not findings:
            continue
        changed += 1
        total += len(findings)
        rel = os.path.relpath(path, REPO)
        for name, line in sorted(findings, key=lambda f: f[1]):
            print(f"{'FOUND' if args.check else 'REDACT'}  {rel}:{line}  {name}")
        if not args.check:
            with open(path, "w", encoding="utf-8", errors="surrogateescape") as fh:
                fh.write(scrubbed)

    verb = "unredacted credential" if args.check else "credential redacted"
    print(f"\n{scanned} capture files scanned, {changed} files, {total} {verb}(s)")
    return 1 if (args.check and total) else 0


if __name__ == "__main__":
    sys.exit(main())
