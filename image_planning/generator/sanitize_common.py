# sanitize_common.py — shared output-sanitization for images/images.yaml emitters.
# SECURITY RULE (p_create_image_hierarchy.md, OUTPUT SANITIZATION): the emitted YAML
# must never contain invisible Unicode characters. Prose is cleaned; identity fields
# (paths/URLs) keep their exact value but are emitted as visible \uXXXX escapes.
import re

INV_RANGES = [(0x00,0x08),(0x0B,0x1F),(0x7F,0x9F),(0xA0,0xA0),(0xAD,0xAD),
    (0x34F,0x34F),(0x61C,0x61C),(0x115F,0x1160),(0x17B4,0x17B5),(0x180B,0x180E),
    (0x2000,0x200F),(0x2028,0x202F),(0x205F,0x206F),(0x3000,0x3000),(0x3164,0x3164),
    (0xFE00,0xFE0F),(0xFEFF,0xFEFF),(0xFFA0,0xFFA0),(0xFFF9,0xFFFB),(0xE0000,0xE007F)]
SPACE_LIKE = {0xA0,0x202F,0x205F,0x3000} | set(range(0x2000,0x200B))

def is_invisible(o):
    return any(lo <= o <= hi for lo, hi in INV_RANGES)

def sanitize_prose(s):
    out = []
    for ch in str(s):
        o = ord(ch)
        if o in SPACE_LIKE: out.append(' ')
        elif is_invisible(o): continue
        else: out.append(ch)
    return re.sub(r'\s+', ' ', ''.join(out)).strip()

def q_prose(s):
    s = sanitize_prose(s)
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'

def q_identity(s):
    out = []
    for ch in str(s):
        o = ord(ch)
        if ch == '\\': out.append('\\\\')
        elif ch == '"': out.append('\\"')
        elif o > 126 or is_invisible(o) or o < 32:
            out.append(f'\\u{o:04X}' if o <= 0xFFFF else f'\\U{o:08X}')
        else: out.append(ch)
    return '"' + ''.join(out) + '"'

def validate_no_invisible(path):
    txt = open(path, encoding='utf-8').read()
    bad = []
    for i, ch in enumerate(txt):
        if ch in ('\n', '\t'): continue
        if is_invisible(ord(ch)):
            bad.append((txt.count('\n', 0, i) + 1, f'U+{ord(ch):04X}'))
            if len(bad) > 5: break
    if bad:
        raise SystemExit(f'SANITIZATION FAILURE: invisible chars in {path}: {bad}')
    return True
