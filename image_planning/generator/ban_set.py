#!/usr/bin/env python3
"""The image ban set — shared by every generator that publishes images.

See the repo charter, "Banned Media". The ban set is the UNION of two sources:

  images/ban_images.csv             the newer master. Columns sha256, cid,
                                    file_path, banned, reason, date_added.
                                    banned=false is an explicit un-ban: the row
                                    stays as a record of the decision and the
                                    item publishes normally.
  image_planning/exclude_images.txt the older one-sha256-per-line list.

An item matched by EITHER gets no page, no served copy, and no placement on any
other page. Match by sha256 first, then cid, then file_path — any match bans it.
An item with no row and no line is not banned.
"""
import csv
import os
import re

ROOT = os.path.expanduser("~/BGit/Bryan_git/charlie-kirk")
EXCLUDE_FILE = os.path.join(ROOT, "image_planning", "exclude_images.txt")
BAN_CSV = os.path.join(ROOT, "images", "ban_images.csv")

SHA_RE = re.compile(r"[0-9a-f]{64}")


def load_ban_idents(exclude_file=EXCLUDE_FILE, ban_csv=BAN_CSV):
    """Return (banned, unbanned) sets of raw identifiers: sha256, cid, file_path."""
    banned, unbanned = set(), set()
    if os.path.exists(exclude_file):
        with open(exclude_file, encoding="utf-8") as f:
            for line in f:
                line = line.split("#", 1)[0].strip()
                if SHA_RE.fullmatch(line):
                    banned.add(line)
    if os.path.exists(ban_csv):
        with open(ban_csv, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                ids = [str(row.get(k) or "").strip()
                       for k in ("sha256", "cid", "file_path")]
                ids = [i for i in ids if i]
                if not ids:
                    continue
                if str(row.get("banned") or "").strip().lower() == "false":
                    unbanned.update(ids)
                else:
                    banned.update(ids)
    return banned - unbanned, unbanned


def load_ban_shas(exclude_file=EXCLUDE_FILE, ban_csv=BAN_CSV):
    """Just the sha256 identifiers — for the sha-keyed gates."""
    banned, _ = load_ban_idents(exclude_file, ban_csv)
    return {i for i in banned if SHA_RE.fullmatch(i)}


def is_banned(entry, banned=None):
    """True when a hierarchy image entry matches a ban by sha256, cid, or path."""
    if banned is None:
        banned, _ = load_ban_idents()
    for k in ("sha256", "cid", "file_path"):
        v = str(entry.get(k) or "").strip()
        if v and v in banned:
            return True
    return False


if __name__ == "__main__":
    b, u = load_ban_idents()
    print(f"banned identifiers: {len(b)}  (sha256: {len(load_ban_shas())})")
    print(f"explicit un-bans:   {len(u)}")
