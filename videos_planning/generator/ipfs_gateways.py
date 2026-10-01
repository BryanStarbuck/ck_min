"""The ONE list of public IPFS gateways that site video players are built from.

Every <source> a video page carries comes from GATEWAYS, in this order. Both
gen_videos_pages.py (new pages) and rewrite_video_gateways.py (existing pages,
including hand-authored ones) import it, so changing a gateway is a one-line
edit here followed by re-running the rewrite.

WHY dweb.link / ipfs.io / w3s.link ARE GONE (measured 2026-09-15):
  * dweb.link and ipfs.io are being retired. Since 2026-09-01 they "step aside"
    for part of every hour and answer HTTP 429 with the body "This IPFS gateway
    is switching to a service worker gateway only"; full retirement is
    2026-09-21 UTC. A <video> tag cannot run a service worker, so the
    inbrowser.link redirect does nothing for embedded video.
  * w3s.link (Storacha) now 301-redirects to dweb.link, so it was never a
    second route - both old <source>s landed on the same dead host.
  * The path form (ipfs.io/ipfs/<cid>, dweb.link/ipfs/<cid>) was already 403
    behind a Cloudflare challenge for browser requests.

HOW THIS ORDER WAS CHOSEN - 40 random site CIDs, browser UA + site Referer,
1 KB range request, plus the same four confirmed 206 video/mp4 via fetch() from
the live page's own origin in Chrome:
  ipfs.orbitor.dev       39/40   median first byte ~1s
  gateway.pinata.cloud   40/40   median first byte ~7s
  ipfs.filebase.io       26/40   median first byte ~2s
  gw.ipfs-lens.dev       35/40   median first byte ~10s
Every one of the 40 was served by at least one. All four send
Access-Control-Allow-Origin: * and honour Range (seeking works).

These are still free, best-effort public gateways with no SLA. A <source> list
only falls through on an HTTP/network ERROR, never on a stall, so the site also
ships site/internals/src/clientModules/ipfsVideoFallback.js, which drops a
source that has not produced metadata within a few seconds and moves on.
Re-measure periodically; gateways die.
"""

import base64

GATEWAYS = [
    'https://ipfs.orbitor.dev/ipfs/{cid}',
    'https://gateway.pinata.cloud/ipfs/{cid}',
    'https://ipfs.filebase.io/ipfs/{cid}',
    'https://gw.ipfs-lens.dev/ipfs/{cid}',
]

_B58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def base32(cid):
    """CIDv0/v1 -> CIDv1 base32. Pure Python, no daemon dependency. '' if unparseable."""
    c = (cid or '').strip()
    try:
        if c.startswith('Qm'):
            n = 0
            for ch in c:
                n = n * 58 + _B58.index(ch)
            mh = n.to_bytes((n.bit_length() + 7) // 8, 'big')
            mh = b'\x00' * (len(c) - len(c.lstrip('1'))) + mh
            return 'b' + base64.b32encode(b'\x01\x70' + mh).decode().lower().rstrip('=')
        if c.startswith('bafy'):
            return c.lower()
    except Exception:
        pass
    return ''


def urls(cid):
    b32 = base32(cid)
    return [g.format(cid=b32) for g in GATEWAYS] if b32 else []


def primary_url(cid):
    u = urls(cid)
    return u[0] if u else ''


def video_sources(cid, indent='    '):
    """The <source> lines for one video, one per line, each prefixed with indent,
    newline-terminated. '' if the CID cannot be converted."""
    return ''.join(f'{indent}<source src="{u}" type="video/mp4" />\n' for u in urls(cid))
