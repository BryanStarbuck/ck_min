#!/bin/bash
MIRROR="$HOME/_Mirror/Politics/Charlie_Kirk_Mi"
SIDE="$HOME/BGit/Bryan_git/personal_large_files_bridge/_Mirror/Politics/Charlie_Kirk_Mi"
OUT="inventory.tsv"
printf 'sha256\tdir\tfilename\torig_path\thas_desc\n' > "$OUT"
find "$MIRROR" -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.webp' -o -iname '*.gif' -o -iname '*.heic' \) -print0 2>/dev/null \
| while IFS= read -r -d '' f; do
    rel="${f#$MIRROR/}"
    d=$(dirname "$rel"); b=$(basename "$rel")
    h=$(shasum -a 256 "$f" 2>/dev/null | awk '{print $1}')
    desc="no"; [ -f "$SIDE/$rel.ai_description" ] && desc="yes"
    printf '%s\t%s\t%s\t~/_Mirror/Politics/Charlie_Kirk_Mi/%s\t%s\n' "$h" "$d" "$b" "$rel" "$desc"
  done >> "$OUT"
echo "DONE rows: $(( $(wc -l < "$OUT") - 1 ))"
echo "unique sha256: $(tail -n +2 "$OUT" | cut -f1 | sort -u | wc -l)"
echo "with descriptions: $(tail -n +2 "$OUT" | awk -F'\t' '$5=="yes"' | wc -l)"
