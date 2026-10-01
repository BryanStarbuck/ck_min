#!/usr/bin/env python3
"""audit_video_registration.py — whole-repo check that every downloaded video
actually entered the master hierarchy (videos/videos.yaml).

Why this exists: videos/manifest.yaml is only the ck_add_text skill's download
log and drives nothing. videos/videos.yaml is the master record that drives
/Videos Level 5 page generation, the nav galleries on Level 2 overviews, the
should_be_on_pages placement pass, and the next_video chain. A video that is
downloaded, pinned, embedded and committed but NOT in videos.yaml is invisible
to all of it — it silently exists on exactly one page and nowhere else.

An audit on 2026-08-19 found 41 such videos dating back to 2026-07-24, none of
which had ever been deleted; they had simply never been registered.

Note the identifier mismatch this script handles for you: videos.yaml stores
CIDv0 (Qm...), pages embed CIDv1 base32 (bafybei...). Comparing them without
converting silently reports zero.

Exit 0 = every downloaded video is registered. Exit 1 = at least one is not.
"""
import os, re, subprocess, sys, yaml

ROOT = os.path.expanduser('~/BGit/Bryan_git/charlie-kirk')
MANIFEST = os.path.join(ROOT, 'videos/manifest.yaml')
MASTER = os.path.join(ROOT, 'videos/videos.yaml')
DOCS = os.path.join(ROOT, 'site/docs')
IPFS = '/opt/homebrew/bin/ipfs'


def base32(cid):
    if not cid.startswith('Qm'):
        return ''
    try:
        return subprocess.run([IPFS, 'cid', 'base32', cid],
                              capture_output=True, text=True, timeout=10).stdout.strip()
    except Exception:
        return ''


def main():
    manifest = yaml.safe_load(open(MANIFEST, encoding='utf-8')) or []
    master = open(MASTER, encoding='utf-8').read()

    # every CID embedded anywhere on the site, in either encoding
    embedded = set()
    for dp, _, fs in os.walk(DOCS):
        for fn in fs:
            if fn.endswith(('.md', '.mdx')):
                t = open(os.path.join(dp, fn), encoding='utf-8', errors='replace').read()
                embedded |= set(re.findall(r'bafybei[a-z2-7]{52}', t))
                embedded |= set(re.findall(r'Qm[1-9A-HJ-NP-Za-km-z]{44}', t))

    unregistered = []
    for e in manifest:
        cid = str(e.get('ipfs_cid') or '').strip()
        fn = str(e.get('filename') or '').strip()
        if not cid and not fn:
            continue
        b32 = base32(cid)
        registered = (cid and cid in master) or (b32 and b32 in master) or (fn and fn in master)
        if registered:
            continue
        on_site = bool((cid and cid in embedded) or (b32 and b32 in embedded))
        unregistered.append((e.get('added_date'), fn, cid, on_site))

    print('videos in manifest.yaml : %d' % len(manifest))
    print('NOT in videos.yaml      : %d' % len(unregistered))
    if unregistered:
        on = sum(1 for u in unregistered if u[3])
        print('  of those, embedded on a site page already : %d' % on)
        print('  of those, on no page at all               : %d' % (len(unregistered) - on))
        print('\n%-12s %-34s %-8s %s' % ('ADDED', 'FILE', 'ON-SITE', 'CID'))
        for d, fn, cid, on_site in sorted(unregistered, key=lambda x: str(x[0])):
            print('%-12s %-34s %-8s %s' % (d, fn[:34], 'yes' if on_site else 'NO', cid))
        print('\nFix: queue them, then rebuild the hierarchy:')
        print('  python3 videos_planning/generator/scan_pages.py')
        print('  python3 videos_planning/generator/add_site_entries.py')
        print('  then run videos_planning/p_update_video_hierarchy.md')
    return 1 if unregistered else 0


if __name__ == '__main__':
    sys.exit(main())
