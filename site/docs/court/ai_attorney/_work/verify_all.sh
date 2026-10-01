#!/bin/sh
# Full STAGE 9 verification for the ai_attorney section.
cd /Users/bryan/BGit/Bryan_git/charlie-kirk/site/docs/court/ai_attorney || exit 1
R=/Users/bryan/BGit/Bryan_git/charlie-kirk
fail=0

echo "== 1. DISCLAIMERS =="
for f in *.mdx; do
  grep -q 'Theoretical Exercise Only' "$f" || { echo "  MISSING BOTTOM: $f"; fail=1; }
  grep -q 'Legal Disclaimer'         "$f" || { echo "  MISSING TOP: $f";    fail=1; }
  grep -q 'CK_AUTHOR_CREDIT'         "$f" || { echo "  MISSING CREDIT: $f"; fail=1; }
done
echo "  ok"

echo "== 2. HTML COMMENTS (blocking) =="
grep -ln '<!--' *.mdx && fail=1 || echo "  none"

echo "== 3. INDENTED CLOSING DIV (blocking) =="
grep -ln '^[[:space:]]\+</div>' *.mdx && fail=1 || echo "  none"

echo "== 4. BANNED LANGUAGE =="
grep -niE "defense failed to|counsel neglected|they should have|an obvious miss|incompetent|ineffective assistance|malpractice|sandbagging|throwing the case|compromised counsel|handed off" *.mdx \
  | grep -v '^method.mdx' || echo "  none"

echo "== 5. 'was never asked' / 'was not asked' outside T1 context =="
grep -niE "was never asked|were never asked" *.mdx || echo "  none"

echo "== 6. H2 STRUCTURE =="
for f in *.mdx; do
  n=$(grep -c '^## ' "$f")
  case "$f" in
    overview.mdx|method.mdx|trial-cursor.mdx|case-stage-map.mdx|the-day-one-track.mdx|two-tracks-compared.mdx) ;;
    *) [ "$n" -eq 8 ] || { echo "  H2=$n (expected 8): $f"; fail=1; } ;;
  esac
done
echo "  ok"

echo "== 7. THESIS PAGES CARRY THE TABLE =="
for f in mechanism-of-death-explosive federal-handling-and-nondisclosure foreign-decision-and-notification \
         direction-of-us-military-intelligence the-diverted-pursuit aircraft-and-ground-vehicles \
         foreign-registered-handsets-on-campus the-university-owned-house withheld-exculpatory-material; do
  [ -f "$f.mdx" ] || { echo "  MISSING PAGE: $f"; fail=1; continue; }
  grep -q '## The Gap Analysis' "$f.mdx" || { echo "  NO GAP ANALYSIS: $f"; fail=1; }
  grep -q '### What would defeat this thesis' "$f.mdx" || { echo "  NO DEFEAT BLOCK: $f"; fail=1; }
  grep -q '## How This Reaches A Juror' "$f.mdx" || { echo "  NO JUROR BLOCK: $f"; fail=1; }
  rows=$(sed -n '/## The Gap Analysis/,/### Where this chain/p' "$f.mdx" | grep -c '^| [0-9]')
  [ "$rows" -ge 8 ] || { echo "  ONLY $rows TABLE ROWS: $f"; fail=1; }
  printf "  %-42s %2s rows\n" "$f" "$rows"
done

echo "== 8. MDX COMPILES =="
node "$R/site/_ck_mdxcheck.mjs" *.mdx || fail=1

echo "== 9. INTERNAL LINKS =="
python3 _work/check_links.py || fail=1

echo
[ "$fail" -eq 0 ] && echo "ALL CHECKS PASS" || echo "SOME CHECKS FAILED"
exit $fail
