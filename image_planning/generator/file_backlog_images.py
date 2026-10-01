#!/usr/bin/env python3
# file_backlog_images.py — move named images out of the Unfiled_Backlog staging
# node and into the topic cluster they actually belong to, filling in the
# ai_description at the same time.
#
# Unfiled_Backlog is where add_orphan_images.py parks an image it found on disk
# but could not classify. Nothing generates a useful Level 5 page from there, so
# images sit in it invisibly. This script does the filing step a human has to
# judge: it takes an explicit sha256 -> (target node _key, title, description)
# table and relocates the entry.
#
# Relocating is NOT deleting. The entry survives intact with the same sha256; it
# just hangs off a different cluster. images.yaml's grow-only rule is preserved:
# no entry and no node is ever removed by this script.
#
# The emitter below is copied from bind_image_pages.py and MUST stay identical to
# it, so the file round-trips byte-for-byte apart from the entries that moved.
import os, sys, yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sanitize_common import q_prose, q_identity

ROOT = os.path.expanduser('~/BGit/Bryan_git/charlie-kirk')
YAML_PATH = os.path.join(ROOT, 'images/images.yaml')
SOURCE_KEY = 'Unfiled_Backlog'

MEDIA_ORDER = ['cid', 'ipfs_pinned', 'sha256', 'file_path', 'ai_description',
               'ai_description_file', 'ocr_file', 'transcription_file',
               'image_page', 'next_image', 'on_pages', 'should_be_on_pages',
               'ipfs_url', 'also_filed_in']

# sha256 -> (target cluster _key, ai_description)
# Descriptions are written the way the rest of images.yaml writes them: purely
# what is VISIBLE in the frame, no conclusion drawn, no accusation restated.
PLAN = {
    # Circled dark object in the air behind the tent at the UVU event
    '465c80d7dd6e0c90d35e9ad31f019e44d623a9947a4cc04c3526a0da6ac15b94': (
        'Suspicious_Anomalies',
        'A screenshot of a social media video player paused at 00:25 of a 39-second '
        'clip filmed at the UVU event. Charlie Kirk is seated beneath the dark "PROVE '
        'ME WRONG" banner with the crowd and a standing security figure behind him. A '
        'hand-drawn yellow circle has been added by the poster to mark a small dark '
        'object visible in the air above and behind the seated figures.'),
    # RIP Charlie Kirk quotation meme
    '28230a180178d2bc0cd5231016716b2cf3ac65f5ca7125032ccdfc9628d5e71e': (
        'MEMEs_2',
        'A memorial meme headed "R.I.P. CHARLIE KIRK" over a photograph of a lone '
        'figure standing on a rocky outcrop beneath an overcast sky. The quotation '
        'reads: "When you tear out a man\'s tongue, you are not proving him a liar, '
        'you\'re only telling the world that you fear what he might say."'),
    # NYT article screenshot — Erika Kirk interview, bulletproof vest
    '569670783c20e2fd36d4cdb195c2970dbc5abf683152ddd449579f36f3a28200': (
        'Media_Coverage',
        'A screenshot of a New York Times article headed "For Erika Kirk, a Husband\'s '
        'Life Cut Short by Violence He Seemed to Foresee". The standfirst states that '
        'in an interview the wife of the conservative activist Charlie Kirk said she '
        'had implored him to wear a bulletproof vest, but that she sees divine work in '
        'his death. A portrait photograph of Erika Kirk appears below the headline.'),
    # Zoom crop of the escort photograph
    '8f7eb7496ce5f10dd6ae347c216004cf76554fce91c4ef0f7deef2bbe8f0c3a9': (
        'Security_Team',
        'A tight zoom crop of an outdoor photograph showing two men walking on a paved '
        'campus path. The man on the left wears a black polo with a badge on the chest '
        'and carries a long camouflage-patterned object at his side in a low ready '
        'position. The man on the right wears a white robe with a coloured stole. Faces '
        'are low-resolution and indistinct.'),
    # Cartridge comparison photograph
    'fbd26b09defeeb29dfd2cb339b8ff1964d8fb9508d19bab42b2fc879435d035d': (
        'Ballistics_Gun',
        'A photograph of five cartridges of descending size laid out on a black '
        'notepad, each hand-labelled in white along the case: 30-06, 5.56, 5.7, 45 and '
        '9mm. The image is a scale comparison of the rounds.'),
    # Charlie Kirk portrait at SiriusXM
    '93177a5ebd2c28440cf6be8025984fe5c83247f10023774b0f53cd4f11872bad': (
        'Charlie_Kirk',
        'A portrait photograph of Charlie Kirk in a light blue shirt and patterned tie, '
        'photographed in a SiriusXM radio studio with the SiriusXM logo visible on the '
        'wall behind him.'),
    # SUV seating diagram
    'd9e9e54fc8bf00047b0a4d285026c26e7829857ed7f8df358400faeed7a3bdb8': (
        'Security_Team',
        'A cutaway diagram of the interior of a large SUV with the seating positions '
        'highlighted in green and labelled in yellow text: Justin Davis and Dan Flood '
        'in the front row, Rick Cutler and Brian Harpole in the middle row, and Frank '
        'Turek in the rear. A black silhouette of a reclining figure is overlaid across '
        'the middle of the cabin.'),
    # Forensic hypothesis comparison table, page 2 of 3
    'e07e4196d3bd6d56f1add5c4245f4ae8d34d8a578f20f449af578e027e70040b': (
        'Mic',
        'Page 2 of 3 of a forensic hypothesis comparison table scoring each finding '
        'against two competing hypotheses, "RIFLE (.30-06)" and "SHAPED CHARGE", on a '
        'five-point scale with a delta column. Rows cover subarachnoid haemorrhage in '
        'the cerebellar vermis and parietal regions, a 53 Hz cavity-mode dominant peak, '
        'a +14.1 dB cavity-to-structural energy ratio, low energy above 500 Hz, a 104 '
        'microsecond rise time, the Cooper acoustic coupling effect and the Courtney '
        'thoracic-to-brain TBI mechanism. Sources are cited per row.'),
    # References and methodology page
    '413b9f00bd37ecb9121502de3e3274459845950e9134f614a837ccc06b1ac103': (
        'Mic',
        'A "References & Methodology" page from followtheepicenter.com setting out the '
        'zero-to-five rating scale used in the accompanying hypothesis comparison and '
        'listing sixteen numbered citations grouped under Blast Injury Literature, '
        'Respiratory Physiology, Thoracic Resonance and Acoustic Data Sources. The '
        'footer reads "Forensic Hypothesis Comparison" and "State of Utah v. Tyler '
        'Robinson".'),
    # USU Police officer public bio page
    '93f8be4820dbdb956e2b473c1a0ce3c79b9e20b1a0e48e9fb406e4e6749fe6b2': (
        'People',
        'A phone screenshot of the Utah State University Veterans Resource Office web '
        'page showing the public staff profile of Alan Robertson. The photograph shows '
        'him in a black police uniform with a Utah State University badge and a '
        'shoulder radio. The caption below reads that Alan Robertson is a full-time '
        'police officer with USU Police and has been with the agency for a little under '
        'a year. A cookie-consent banner covers the lower portion of the page.'),
    # Apple Podcasts removal graphic
    '332e68531a71617430c74a2d019a976ef1fc93161c3727f55451b334237ed511': (
        'Censorship_Evidence',
        'A graphic on a wood-grain background. On the left is a portrait of Charlie '
        'Kirk in a navy suit and red tie with a red strip of tape reading "CENSORED" '
        'across his mouth. The text to the right reads "CHARLIE KIRK — 1,793 Podcasts '
        'Removed from Apple Podcast (of his podcasts of when he was alive)".'),
}


def child_list(node):
    for k, v in node.items():
        if k.startswith('level_') and isinstance(v, list):
            yield int(k.split('_')[1]), v


def main():
    doc = yaml.safe_load(open(YAML_PATH, encoding='utf-8'))

    nodes = {}

    def index(items, lvl):
        for it in items:
            node = it[f'level_{lvl}']
            nodes[node['_key']] = node
            for nl, arr in child_list(node):
                index(arr, nl)
    index(doc['level_3'], 3)

    missing = [k for _, (k, _d) in PLAN.items() if k not in nodes]
    if missing:
        print('ERROR: unknown target node keys:', sorted(set(missing)))
        return 1
    if SOURCE_KEY not in nodes:
        print(f'ERROR: no {SOURCE_KEY} node'); return 1

    src = nodes[SOURCE_KEY]
    src_images = src.get('images') or []
    moved, notfound = [], []

    for sha, (target_key, desc) in PLAN.items():
        hit = None
        for im in src_images:
            if (im.get('image') or {}).get('sha256') == sha:
                hit = im; break
        if hit is None:
            notfound.append(sha[:12]); continue
        src_images.remove(hit)
        inner = hit['image']
        inner['ai_description'] = desc
        # A fresh page will be generated for it, so clear any stale binding.
        inner['image_page'] = ''
        tgt = nodes[target_key]
        tgt.setdefault('images', [])
        tgt['images'].append(hit)
        moved.append((sha[:12], target_key))

    src['images'] = src_images

    # ---------- recount (identical to bind_image_pages.py Stage 9) ----------
    split = {'n': 0}

    def recount(items, lvl):
        total = 0
        for it in items:
            node = it[f'level_{lvl}']
            direct = len(node.get('images') or []) + len(node.get('videos') or [])
            sub = sum(recount(arr, nl) for nl, arr in child_list(node))
            node['number_of_images'] = direct
            node['number_of_images_recursive'] = direct + sub
            if direct > 12:
                node['needs_split'] = True; split['n'] += 1
            elif 'needs_split' in node:
                del node['needs_split']
            total += direct + sub
        return total
    grand = recount(doc['level_3'], 3)

    # ---------- emit (identical to bind_image_pages.py) ----------
    PROSE_FIELDS = {'title', 'ai_description'}
    q = q_identity
    out = []
    out.append('# images.yaml — master image list / image evidence hierarchy for the Charlie Kirk site.')
    out.append('# Moved 2026-07-22 from image_planning/hierarchy_images.yaml (old name + location dead).')
    out.append('# GENERATED first pass from ~/_Mirror/Politics/Charlie_Kirk_Mi; GROWN by')
    out.append('# p_create_image_hierarchy.md: site Level 2/3/4 pages mirrored in as level_3/4/5')
    out.append('# (level incremented by one), page-embedded images bound in, sidecar file paths')
    out.append('# (.ai_description / .ocr / .transcription) resolved via Large File Bridge mapping,')
    out.append('# and site IPFS embeds (ipfs.io/ipfs/<CID>) bound to entries by sha256 via local IPFS.')
    out.append('# image_page = full path from ~ to the published Level 5 page that hosts that one')
    out.append('# image under site/docs/Photos; "" means no page exists for it yet.')
    out.append('# cid empty = IPFS not assigned yet. sha256 is the identity; ipfs_url entries have no local file.')
    out.append('# Nodes marked needs_split exceed the 12-image ceiling and get split on a later pass.')
    out.append('# site_level_2 = site docs dirs this cluster covers; site_page = the page a node mirrors.')

    def emit_media(im, pad):
        kind = 'image' if 'image' in im else 'video'
        inner = im[kind]
        out.append(f'{pad}- {kind}:')
        p2 = pad + '    '
        keys = MEDIA_ORDER + [k for k in inner if k not in MEDIA_ORDER]
        for k in keys:
            if k not in inner: continue
            v = inner[k]
            if k == 'ipfs_pinned':
                out.append(f'{p2}ipfs_pinned: {"true" if v else "false"}')
            elif k in ('on_pages', 'should_be_on_pages'):
                if v:
                    out.append(f'{p2}{k}:')
                    for pg in v:
                        path = pg['page'] if isinstance(pg, dict) else pg
                        out.append(f'{p2}  - page: {q(path)}')
                else:
                    out.append(f'{p2}{k}: []')
            elif k == 'sha256':
                out.append(f'{p2}{k}: {v if v else chr(34) + chr(34)}')
            elif isinstance(v, list):
                if v: out.append(f'{p2}{k}: [{", ".join(q(x) for x in v)}]')
            elif k in PROSE_FIELDS:
                out.append(f'{p2}{k}: {q_prose(v)}')
            else:
                out.append(f'{p2}{k}: {q(v)}')

    def emit_node(it, lvl, indent):
        node = it[f'level_{lvl}']
        pad = ' ' * indent
        out.append(f'{pad}- level_{lvl}:')
        p2 = pad + '    '
        out.append(f'{p2}title: {q_prose(node["title"])}')
        out.append(f'{p2}_key: {node["_key"]}')
        if 'site_level_2' in node:
            out.append(f'{p2}site_level_2: [{", ".join(q(x) for x in node["site_level_2"])}]')
        if node.get('site_page'):
            out.append(f'{p2}site_page: {q(node["site_page"])}')
        out.append(f'{p2}number_of_images: {node["number_of_images"]}')
        out.append(f'{p2}number_of_images_recursive: {node["number_of_images_recursive"]}')
        if node.get('needs_split'):
            out.append(f'{p2}needs_split: true   # over the 12 ceiling — split on a later pass')
        for kind in ('images', 'videos'):
            arr = node.get(kind) or []
            if not arr:
                if kind == 'images': out.append(f'{p2}images: []')
                continue
            out.append(f'{p2}{kind}:')
            for im in arr: emit_media(im, p2 + '  ')
        for nl, arr in child_list(node):
            if arr:
                out.append(f'{p2}level_{nl}:')
                for c in arr: emit_node(c, nl, indent + 6)

    out.append('level_3:')
    for it in doc['level_3']:
        emit_node(it, 3, 2)

    text = '\n'.join(out) + '\n'
    yaml.safe_load(text)  # must parse before we write
    open(YAML_PATH, 'w', encoding='utf-8').write(text)

    print('=' * 50)
    print('FILE BACKLOG IMAGES COMPLETE')
    for sha, key in moved:
        print(f'  {sha} -> {key}')
    if notfound:
        print('  NOT FOUND in backlog:', notfound)
    print(f'  moved: {len(moved)}   still in {SOURCE_KEY}: {len(src_images)}')
    print(f'  grand total media entries: {grand}   needs_split nodes: {split["n"]}')
    print('  YAML re-parses: yes')
    print('=' * 50)
    return 0


if __name__ == '__main__':
    sys.exit(main())
