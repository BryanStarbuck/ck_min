#!/usr/bin/env python3
# compute_cids.py — STAGE 4 of p_update_video_hierarchy.md.
# Seeds CIDs from manifest.yaml and IPFS/ipfs.txt, computes a CIDv0 for every row
# with a local file (`ipfs add -n -Q`, default chunker/cid-version so the value
# matches what the manifest records and the site embeds), records pin status, and
# builds the v0 + base32-v1 index Stage 11 resolves page embeds against.
#
# NOTHING IS EVER PINNED BY THIS SCRIPT. It records state; it does not change
# what is public.
import os, csv, json, subprocess, hashlib, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
INV  = os.path.join(HERE, 'inventory.tsv')
OUT  = os.path.join(HERE, 'cids.json')
IPFS = '/opt/homebrew/bin/ipfs'
WORKERS = int(os.environ.get('CID_WORKERS', '5'))

rows = list(csv.DictReader(open(INV, encoding='utf-8'), delimiter='\t'))

def run(args, timeout=1800):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout.strip(), p.stderr.strip()
    except Exception as e:
        return 1, '', str(e)

def compute_cid(path):
    rc, out, err = run([IPFS, 'add', '-n', '-Q', path])
    return out if rc == 0 and out.startswith('Qm') else ''

def sha256_of(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 22), b''):
            h.update(chunk)
    return h.hexdigest()

def to_base32(cid):
    rc, out, _ = run([IPFS, 'cid', 'base32', cid], timeout=30)
    return out if rc == 0 and out else ''

# ---------------------------------------------------------------- compute
result = {}
jobs = []
for r in rows:
    vkey, mp = r['vkey'], r['media_path']
    seeded = r['manifest_cid'].strip()
    ent = dict(vkey=vkey, cid=seeded, cid_source='manifest' if seeded else '',
               sha256='', ipfs_pinned=False, recomputed='', mismatch=False,
               file_size=int(r['size']) if r['size'].isdigit() else 0)
    result[vkey] = ent
    is_video = os.path.splitext(mp)[1].lower() in (
        '.mp4', '.mov', '.m4v', '.mkv', '.avi', '.webm')
    if mp and os.path.exists(mp) and is_video:
        jobs.append((vkey, mp))

print(f'{len(jobs)} local video files to hash '
      f'({sum(result[v]["file_size"] for v, _ in jobs)/2**30:.1f} GB), '
      f'{WORKERS} workers', flush=True)

# A hash cache keyed by (path, size, mtime) so a rerun costs seconds, not the
# ~10 minutes it takes to stream 25 GB through the hasher twice.
CACHE = os.path.join(HERE, 'hash_cache.json')
cache = {}
if os.path.exists(CACHE):
    try:
        cache = json.load(open(CACHE, encoding='utf-8'))
    except Exception:
        cache = {}

def cache_key(path):
    st = os.stat(path)
    return f'{path}|{st.st_size}|{int(st.st_mtime)}'

done = [0]
def work(job):
    vkey, mp = job
    ck = cache_key(mp)
    hit = cache.get(ck)
    if hit:
        cid, sha = hit['cid'], hit['sha256']
    else:
        cid = compute_cid(mp)
        sha = sha256_of(mp)
    done[0] += 1
    if done[0] % 25 == 0:
        print(f'  ... {done[0]}/{len(jobs)}', flush=True)
    return vkey, cid, sha, ck

with ThreadPoolExecutor(max_workers=WORKERS) as ex:
    for vkey, cid, sha, ck in ex.map(work, jobs):
        cache[ck] = dict(cid=cid, sha256=sha)
        ent = result[vkey]
        ent['sha256'] = sha
        ent['recomputed'] = cid
        if cid:
            if ent['cid'] and ent['cid'] != cid:
                ent['mismatch'] = True
                ent['prior_cid'] = ent['cid']
                ent['cid'] = cid
                ent['cid_source'] = 'recomputed(mismatch)'
            elif not ent['cid']:
                ent['cid'] = cid
                ent['cid_source'] = 'computed'
            else:
                ent['cid_source'] = 'manifest(confirmed)'

json.dump(cache, open(CACHE, 'w', encoding='utf-8'))

# ---------------------------------------------------------------- pin status
# Dump the node's whole pinset ONCE and test membership locally. Never query
# `ipfs pin ls <cid>` per CID: for a CID the node does not hold, that call goes
# to the network and blocks until it times out.
uniq = sorted({e['cid'] for e in result.values() if e['cid']})
print(f'checking pin status for {len(uniq)} distinct CIDs', flush=True)
pinned = set()
for t in ('recursive', 'direct', 'indirect'):
    rc, out, err = run([IPFS, 'pin', 'ls', '--type=' + t], timeout=600)
    if rc == 0:
        for line in out.split('\n'):
            c = line.split(' ', 1)[0].strip()
            if c:
                pinned.add(c)
    else:
        print(f'  WARNING: pin ls --type={t} failed: {err[:120]}', flush=True)
print(f'  local pinset holds {len(pinned)} CIDs', flush=True)
pinned &= set(uniq)
for e in result.values():
    e['ipfs_pinned'] = e['cid'] in pinned

# ---------------------------------------------------------------- cid index
print('building base32 index', flush=True)
b32 = {}
with ThreadPoolExecutor(max_workers=8) as ex:
    for cid, v1 in zip(uniq, ex.map(to_base32, uniq)):
        if v1:
            b32[cid] = v1

index = {}
for e in result.values():
    if e['cid']:
        index[e['cid']] = e['vkey']
        if e['cid'] in b32:
            index[b32[e['cid']]] = e['vkey']

json.dump(dict(entries=result, cid_index=index, base32=b32),
          open(OUT, 'w', encoding='utf-8'), indent=None)

seeded_manifest = sum(1 for e in result.values()
                      if e['cid_source'].startswith('manifest'))
computed = sum(1 for e in result.values() if e['cid_source'] == 'computed')
mismatches = [e for e in result.values() if e['mismatch']]
no_cid = [e['vkey'] for e in result.values() if not e['cid']]
unpinned = [e['vkey'] for e in result.values() if e['cid'] and not e['ipfs_pinned']]

print('============================')
print('STAGE 4 COMPLETE')
print(f'Seeded from manifest/ipfs.txt: {seeded_manifest}')
print(f'Rows with local file: {len(jobs)}    CID computed: {computed}    '
      f'already present and matching: {seeded_manifest}')
print(f'CID mismatches (bytes changed): {len(mismatches)}')
for m in mismatches[:10]:
    print(f"   {m['vkey']}: was {m.get('prior_cid')} now {m['cid']}")
print(f'Pinned on local node: {len(pinned)}    NOT pinned: {len(unpinned)} '
      f'(THESE PUBLISH AS DEAD PLAYERS)')
print(f'Rows left cid "": {len(no_cid)}')
print(f'   {", ".join(no_cid[:25])}')
print(f'CID index built: {len(uniq)} v0 + {len(b32)} base32 forms')
print('Nothing pinned by this stage: confirmed')
print('============================')
