#!/usr/bin/env python3
# sanitize_video.py — output sanitization for the VIDEO pipeline's emitters.
#
# SECURITY RULE (p_update_video_hierarchy.md, OUTPUT SANITIZATION): the emitted
# videos/videos.yaml must never contain invisible Unicode. Invisible characters
# hide content from review, spoof strings, and smuggle instructions past a human
# reading the file. Every byte of the emitted YAML must be visible in an editor.
#
# Two treatments, chosen by field kind:
#   PROSE fields    — sanitize the CONTENT. Space-like invisibles become a plain
#                     space, zero-width / bidi / control / joiner characters are
#                     deleted, whitespace runs collapse. Visible non-ASCII stays:
#                     the sidecars legitimately carry em dashes, curly quotes,
#                     U+00B7 MIDDLE DOT and U+2713 CHECK MARK, and those are fine.
#   IDENTITY fields — the value must keep resolving the real file on disk, so no
#                     character may be replaced. Every non-ASCII code point is
#                     emitted as a visible \uXXXX escape inside a YAML
#                     double-quoted scalar; YAML decodes it on parse, so the
#                     parsed value is unchanged while the file's own bytes hold
#                     nothing invisible. This matters here: the mirror's
#                     filenames carry full-width punctuation and emoji.
#
# This is the video pipeline's own module. The images pipeline has an equivalent
# at image_planning/generator/sanitize_common.py; that file is PRIOR ART, read
# only, and is never copied into this directory.
import re

INVISIBLE_RANGES = [
    (0x0000, 0x0008), (0x000B, 0x001F), (0x007F, 0x009F),
    (0x00A0, 0x00A0), (0x00AD, 0x00AD), (0x034F, 0x034F), (0x061C, 0x061C),
    (0x115F, 0x1160), (0x17B4, 0x17B5), (0x180B, 0x180E),
    (0x2000, 0x200F), (0x2028, 0x202F), (0x205F, 0x206F),
    (0x3000, 0x3000), (0x3164, 0x3164), (0xFE00, 0xFE0F), (0xFEFF, 0xFEFF),
    (0xFFA0, 0xFFA0), (0xFFF9, 0xFFFB), (0xE0000, 0xE007F),
]
# The space-like subset gets replaced by a plain space rather than deleted.
# U+202F NARROW NO-BREAK SPACE is the one macOS puts in screenshot filenames
# before AM/PM, and it does appear in these inputs.
SPACE_LIKE = {0x00A0, 0x202F, 0x205F, 0x3000} | set(range(0x2000, 0x200B))


def is_invisible(o):
    return any(lo <= o <= hi for lo, hi in INVISIBLE_RANGES)


def sanitize_prose(s):
    """Clean a prose value and collapse it to a single line."""
    out = []
    for ch in str(s or ''):
        o = ord(ch)
        if o in SPACE_LIKE:
            out.append(' ')
        elif is_invisible(o):
            continue
        else:
            out.append(ch)
    return re.sub(r'\s+', ' ', ''.join(out)).strip()


def sanitize_block(s):
    """Clean a prose value that must KEEP its line breaks (shot_timeline)."""
    out = []
    for ch in str(s or ''):
        o = ord(ch)
        if ch == '\n':
            out.append(ch)
        elif o in SPACE_LIKE:
            out.append(' ')
        elif is_invisible(o):
            continue
        else:
            out.append(ch)
    lines = [re.sub(r'[ \t]+', ' ', l).rstrip() for l in ''.join(out).split('\n')]
    return '\n'.join(lines).strip('\n')


def q_prose(s):
    """A YAML double-quoted scalar for a PROSE field."""
    s = sanitize_prose(s)
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def q_identity(s):
    """A YAML double-quoted scalar for an IDENTITY field: every non-ASCII code
    point becomes a visible \\uXXXX escape so the emitted bytes are all visible
    while the parsed value still resolves the real file."""
    out = []
    for ch in str(s or ''):
        o = ord(ch)
        if ch == '\\':
            out.append('\\\\')
        elif ch == '"':
            out.append('\\"')
        elif o < 32 or o > 126 or is_invisible(o):
            out.append(f'\\u{o:04X}' if o <= 0xFFFF else f'\\U{o:08X}')
        else:
            out.append(ch)
    return '"' + ''.join(out) + '"'


def validate_no_invisible(path):
    """HARD FAIL if any invisible code point survived into the written file."""
    txt = open(path, encoding='utf-8').read()
    bad = []
    for i, ch in enumerate(txt):
        if ch in ('\n', '\t'):
            continue
        if is_invisible(ord(ch)):
            bad.append((txt.count('\n', 0, i) + 1, f'U+{ord(ch):04X}'))
            if len(bad) > 5:
                break
    if bad:
        raise SystemExit(f'SANITIZATION FAILURE: invisible characters in {path}: {bad}')
    return True
