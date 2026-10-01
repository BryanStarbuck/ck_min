#!/usr/bin/env python3
"""Rewrite every IPFS video embed under site/docs to the gateway list in ipfs_gateways.py.

Run after changing ipfs_gateways.GATEWAYS. Idempotent: the current gateways are
recognised too, so a second run changes nothing.

  python3 videos_planning/generator/rewrite_video_gateways.py            # dry run, report only
  python3 videos_planning/generator/rewrite_video_gateways.py --write    # apply

What it touches, and nothing else:
  * Every RUN of consecutive <source src="GATEWAY" type="video/mp4" /> tags for
    one CID (on one line or across lines) becomes one <source> per gateway, one
    per line, at the indent of the first tag. Anything after the run on the same
    line (a caption <p>, a link) is kept exactly.
  * href="GATEWAY" and markdown ](GATEWAY) links become the primary gateway.
  * MDX comments that merely mention an old gateway are left alone - they are
    history, not something a visitor's browser loads.
A run mixing two different CIDs is left untouched and reported.
"""
import os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ipfs_gateways import base32, video_sources, primary_url

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
DOCS = os.path.join(ROOT, 'site', 'docs')

CID = r'(?:Qm[1-9A-HJ-NP-Za-km-z]{44}|bafy[a-z2-7]{50,})'
PATH_HOSTS = r'(?:ipfs\.io|dweb\.link|gateway\.ipfs\.io|gateway\.pinata\.cloud|ipfs\.orbitor\.dev|ipfs\.filebase\.io|gw\.ipfs-lens\.dev)'
SUB_HOSTS = r'(?:dweb\.link|w3s\.link|nftstorage\.link)'
GW_URL = (rf'https://(?:(?P<sub>{CID})\.ipfs\.{SUB_HOSTS}/?'
          rf'|{PATH_HOSTS}/ipfs/(?P<path>{CID})/?)')
GW_URL_NOGROUP = GW_URL.replace('?P<sub>', '?:').replace('?P<path>', '?:')

SRC = rf'<source src="{GW_URL_NOGROUP}" type="video/mp4" />'
RUN = re.compile(rf'{SRC}(?:[ \t]*\n?[ \t]*{SRC})*')
ONE_URL = re.compile(GW_URL)
HREF = re.compile(rf'(href="|\]\()({GW_URL_NOGROUP})(?=["\)])')


def cid_of(url):
    m = ONE_URL.fullmatch(url) or ONE_URL.match(url)
    return base32(m.group('sub') or m.group('path')) if m else ''


def rewrite(text, stats):
    out, pos = [], 0
    for m in RUN.finditer(text):
        cids = {cid_of(u) for u in re.findall(r'src="([^"]+)"', m.group(0))}
        if len(cids) != 1 or '' in cids:
            stats['mixed'] += 1
            continue
        line_start = text.rfind('\n', 0, m.start()) + 1
        lead = text[line_start:m.start()]
        indent = lead if lead.strip() == '' else ''
        new = video_sources(cids.pop(), indent)[len(indent):].rstrip('\n')
        out.append(text[pos:m.start()])
        out.append(new)
        pos = m.end()
        stats['runs'] += 1
    text = ''.join(out) + text[pos:]

    def href_sub(m):
        new = primary_url(cid_of(m.group(2)))
        if not new:
            return m.group(0)
        stats['links'] += 1
        return m.group(1) + new
    return HREF.sub(href_sub, text)


def main():
    write = '--write' in sys.argv
    changed, stats = [], {'runs': 0, 'links': 0, 'mixed': 0}
    for d, _, files in os.walk(DOCS):
        for f in files:
            if not f.endswith(('.md', '.mdx')):
                continue
            p = os.path.join(d, f)
            with open(p, encoding='utf-8') as fh:
                old = fh.read()
            new = rewrite(old, stats)
            if new != old:
                changed.append(os.path.relpath(p, ROOT))
                if write:
                    with open(p, 'w', encoding='utf-8') as fh:
                        fh.write(new)
    print(f"{'WROTE' if write else 'DRY RUN'}: {len(changed)} files; "
          f"{stats['runs']} <source> runs rebuilt; {stats['links']} links repointed; "
          f"{stats['mixed']} mixed-CID runs skipped")
    if '--list' in sys.argv:
        print('\n'.join(changed))


if __name__ == '__main__':
    main()
