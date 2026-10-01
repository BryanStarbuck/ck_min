#!/usr/bin/env python3
# harvest_sidecars.py — STAGE 3 of p_update_video_hierarchy.md.
# For every row in inventory.tsv, resolve and PARSE all three Large File Bridge
# sidecars (.transcription / .ai_description / .ocr) and write the parsed result
# to generator/sidecars.json keyed by vkey. This is the core of the run: the
# sidecars are the data.
import os, re, csv, sys, json, yaml

HERE = os.path.dirname(os.path.abspath(__file__))
INV  = os.path.join(HERE, 'inventory.tsv')
OUT  = os.path.join(HERE, 'sidecars.json')
REP  = os.path.join(HERE, 'stage3_report.json')

def collapse(s):
    return re.sub(r'\s+', ' ', (s or '')).strip()

# ------------------------------------------------------------ .transcription
def parse_transcription(path):
    """Five-line header, a 60-'=' divider, then the body as one long line."""
    out = dict(engine='', generated='', duration='', covers='', complete=False,
               body='', header_source='', parse_ok=False)
    try:
        txt = open(path, encoding='utf-8', errors='replace').read()
    except OSError:
        return out
    lines = txt.split('\n')
    div = -1
    for i, l in enumerate(lines[:12]):
        if re.match(r'^={10,}\s*$', l):
            div = i
            break
    head = lines[:div] if div >= 0 else lines[:5]
    for l in head:
        m = re.match(r'^Transcription of:\s*(.+?)\s*$', l)
        if m:
            out['header_source'] = m.group(1); continue
        m = re.match(r'^Generated on:\s*(.+?)\s*$', l)
        if m:
            out['generated'] = m.group(1); continue
        m = re.match(r'^Engine:\s*(.+?)\s*$', l)
        if m:
            out['engine'] = m.group(1); continue
        if 'Source duration:' in l or 'Transcript covers:' in l:
            m = re.search(r'Source duration:\s*([0-9:]+)', l)
            if m:
                out['duration'] = m.group(1)
            m = re.search(r'Transcript covers:\s*([0-9:]+)', l)
            if m:
                out['covers'] = m.group(1)
            # the completeness marker: U+2713 CHECK MARK followed by "full"
            out['complete'] = bool(re.search(r'✓\s*full', l))
    if div >= 0:
        out['body'] = '\n'.join(lines[div + 1:]).strip()
        out['parse_ok'] = True
    else:
        out['body'] = txt.strip()
    return out

# ----------------------------------------------------------- .ai_description
AI_KEYS = ('source', 'status', 'engine', 'provider', 'generated', 'kind')

def split_md_sections(md):
    secs, cur, buf = {}, None, []
    for line in (md or '').split('\n'):
        m = re.match(r'^\s*##\s+(.+?)\s*$', line)
        if m:
            if cur is not None:
                secs[cur] = '\n'.join(buf).strip()
            cur, buf = m.group(1).strip(), []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        secs[cur] = '\n'.join(buf).strip()
    return secs

def pick(secs, *names):
    low = {k.lower(): v for k, v in secs.items()}
    for n in names:
        if n.lower() in low:
            return low[n.lower()]
    for k, v in low.items():
        for n in names:
            if n.lower() in k:
                return v
    return ''

def parse_ai_description(path):
    out = dict(source='', status='', engine='', provider='', generated='', kind='',
               overview='', shot_timeline='', people='', onscreen='', hyper='',
               location='', parse_ok=False)
    try:
        doc = yaml.safe_load(open(path, encoding='utf-8', errors='replace'))
    except Exception:
        return out
    if not isinstance(doc, dict):
        return out
    for k in AI_KEYS:
        out[k] = str(doc.get(k, '') or '')
    # PyYAML parses an ISO 8601 scalar into a datetime and str() then renders it
    # in Python's form, not the sidecar's. Take `generated` off the raw text so
    # the YAML records exactly what the sidecar recorded.
    try:
        raw = open(path, encoding='utf-8', errors='replace').read(4000)
        m = re.search(r'^generated:\s*(\S+)\s*$', raw, re.M)
        if m:
            out['generated'] = m.group(1)
    except OSError:
        pass
    out['parse_ok'] = True
    if out['status'] != 'done':
        return out
    secs = split_md_sections(doc.get('description', '') or '')
    out['overview']       = collapse(pick(secs, 'Overview'))
    out['shot_timeline']  = pick(secs, 'Shot-by-shot / Timeline', 'Shot-by-shot',
                                 'Timeline').strip()
    out['people']         = collapse(pick(secs, 'People'))
    out['onscreen']       = collapse(pick(secs, 'Objects, Text & Brands',
                                          'Objects, Text and Brands', 'Objects'))
    out['hyper']          = collapse(pick(secs, 'Hyper-Detail'))
    out['location']       = collapse(pick(secs, 'Location'))
    return out

# ---------------------------------------------------------------------- .ocr
def parse_ocr(path):
    """Observed format (Stage 1): a YAML doc with source/status/engine/level/
    generated/kind/language/stride_seconds/frames_sampled/truncated/text/blocks."""
    out = dict(source='', status='', engine='', generated='', language='',
               stride_seconds='', frames_sampled='', truncated='', text='',
               n_blocks=0, parse_ok=False)
    try:
        doc = yaml.safe_load(open(path, encoding='utf-8', errors='replace'))
    except Exception:
        return out
    if not isinstance(doc, dict):
        return out
    out['parse_ok'] = True
    for k in ('source', 'status', 'engine', 'generated', 'language'):
        out[k] = str(doc.get(k, '') or '')
    out['stride_seconds'] = str(doc.get('stride_seconds', '') or '')
    out['frames_sampled'] = str(doc.get('frames_sampled', '') or '')
    out['truncated'] = str(doc.get('truncated', '') or '')
    out['text'] = (doc.get('text', '') or '').strip()
    b = doc.get('blocks')
    out['n_blocks'] = len(b) if isinstance(b, list) else 0
    return out

# ---------------------------------------------------------------------- main
rows = list(csv.DictReader(open(INV, encoding='utf-8'), delimiter='\t'))
data, rep = {}, dict(
    no_transcription=[], audio_sibling=[], partial=[], no_ai_description=[],
    ai_not_done=[], pairing_mismatch=[], ocr_set=[], no_duration=[])

for r in rows:
    vkey = r['vkey']
    e = dict(vkey=vkey, basename=r['basename'])
    tp, ap, op = r['transcription_path'], r['ai_description_path'], r['ocr_path']

    if tp and os.path.exists(tp):
        t = parse_transcription(tp)
        e['transcription'] = t
        if not t['duration']:
            rep['no_duration'].append(vkey)
        if not t['complete']:
            rep['partial'].append(vkey)
        # pairing check: header filename vs the sidecar's own base name
        expect = os.path.basename(tp)
        for suf in ('.transcription',):
            if expect.endswith(suf):
                expect = expect[:-len(suf)]
        if t['header_source'] and t['header_source'] != expect:
            rep['pairing_mismatch'].append(
                dict(vkey=vkey, sidecar=tp, header=t['header_source'], expect=expect))
        if r['transcription_source'] == 'audio_sibling':
            rep['audio_sibling'].append(vkey)
    else:
        e['transcription'] = None
        rep['no_transcription'].append(vkey)

    if ap and os.path.exists(ap):
        a = parse_ai_description(ap)
        e['ai_description'] = a
        if a['status'] != 'done':
            rep['ai_not_done'].append(dict(vkey=vkey, status=a['status']))
        exp = os.path.basename(ap)[:-len('.ai_description')]
        if a['source'] and os.path.basename(a['source']) != exp:
            rep['pairing_mismatch'].append(
                dict(vkey=vkey, sidecar=ap, header=a['source'], expect=exp))
    else:
        e['ai_description'] = None
        rep['no_ai_description'].append(vkey)

    if op and os.path.exists(op):
        e['ocr'] = parse_ocr(op)
        rep['ocr_set'].append(vkey)
    else:
        e['ocr'] = None

    data[vkey] = e

json.dump(data, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
json.dump(rep, open(REP, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

n = len(rows)
own = sum(1 for r in rows if r['transcription_source'] == 'video')
sib = sum(1 for r in rows if r['transcription_source'] == 'audio_sibling')
ov  = sum(1 for v in data.values() if (v['ai_description'] or {}).get('overview'))
sh  = sum(1 for v in data.values() if (v['ai_description'] or {}).get('shot_timeline'))
pe  = sum(1 for v in data.values() if (v['ai_description'] or {}).get('people'))
ot  = sum(1 for v in data.values() if (v['ai_description'] or {}).get('onscreen'))
du  = sum(1 for v in data.values() if (v['transcription'] or {}).get('duration'))

print('============================')
print('STAGE 3 COMPLETE')
print(f'Rows processed: {n}')
print(f"transcription_file set: {n-len(rep['no_transcription'])} "
      f"(own video {own} / audio sibling {sib})   missing: {len(rep['no_transcription'])}")
print(f"  transcript_complete false: {len(rep['partial'])}  (PARTIAL TRANSCRIPTS)")
print(f"ai_description_file set: {n-len(rep['no_ai_description'])}   "
      f"missing: {len(rep['no_ai_description'])}")
print(f'  ## Overview extracted: {ov}   ## Shot-by-shot extracted: {sh}')
print(f'  ## People extracted: {pe}     ## Objects/Text extracted: {ot}')
print(f"ocr_file set: {len(rep['ocr_set'])}")
print(f'Duration harvested for: {du} of {n} rows')
print(f"Sidecar/media pairing mismatches: {len(rep['pairing_mismatch'])}")
print(f'Sidecar index written: {OUT}')
print('============================')
print('MISSING TRANSCRIPTION:', ', '.join(rep['no_transcription'][:20]) or 'none')
print('PARTIAL:', ', '.join(rep['partial'][:20]) or 'none')
print('MISSING AI DESCRIPTION:', ', '.join(rep['no_ai_description'][:20]) or 'none')
print('AI NOT DONE:', rep['ai_not_done'][:10])
print('PAIRING MISMATCH:', rep['pairing_mismatch'][:5])
