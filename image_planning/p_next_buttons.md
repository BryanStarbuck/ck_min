ROOT_DIR dir is ~/BGit/Bryan_git/charlie-kirk

THIS_DIR dir is {ROOT_DIR}/image_planning
IMAGES_DIR dir is {ROOT_DIR}/images
HIERARCHY_FILE is file {IMAGES_DIR}/images.yaml
  (Moved 2026-07-22 from {THIS_DIR}/hierarchy_images.yaml; that name and location are gone.)
LAYOUT_GUIDELINES is file {THIS_DIR}/layout_guidelines.txt
CHARTER_FILE is file {THIS_DIR}/CLAUDE.md
EXCLUDE_FILE is file {THIS_DIR}/exclude_images.txt
BAN_IMAGES_CSV is file {IMAGES_DIR}/ban_images.csv
FINDINGS_FILE is file {THIS_DIR}/findings_for_hierarchy.md

GENERATOR_DIR dir is {THIS_DIR}/generator
GEN_SCRIPT is file {GENERATOR_DIR}/gen_photos_pages.py
BIND_SCRIPT is file {GENERATOR_DIR}/bind_image_pages.py
VERIFY_SCRIPT is file {GENERATOR_DIR}/verify_photos.py

IMAGE_PAGE_PROMPT is file {THIS_DIR}/p_yaml_to_site.md
NAV_PROMPT is file {THIS_DIR}/p_level2_update.md
HIERARCHY_PROMPT is file {THIS_DIR}/p_update_image_hierarchy.md

SITE_DIR dir is {ROOT_DIR}/site
DOCS_DIR dir is {SITE_DIR}/docs
PHOTOS_DIR dir is {DOCS_DIR}/Photos
STATIC_IMG_DIR dir is {SITE_DIR}/static/img/evidence
CUSTOM_CSS is file {SITE_DIR}/internals/src/css/custom.css
IMAGES_L2_PAGE is file {PHOTOS_DIR}/overview.mdx
PAGES_CSV is file {ROOT_DIR}/pages.csv
CK_FILE is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt
  (Real file; {ROOT_DIR}/Charlie_Kirk.txt is a symlink to it. READ-ONLY.)
ASSESS_MANUAL is file {ROOT_DIR}/prompts/Assess_Manual.md

SIBLING VIDEO PIPELINE (read-only from here, never written):
VIDEO_PLANNING_DIR dir is {ROOT_DIR}/videos_planning
VIDEOS_DIR dir is {ROOT_DIR}/videos
VIDEO_HIERARCHY_FILE is file {VIDEOS_DIR}/videos.yaml
VIDEOS_L2_DIR dir is {DOCS_DIR}/Videos

BTN_LABEL is the string "Next Image"
BTN_FILL is the value ... = a dark blue button fill (navy, e.g. #0d2b6b),
  darker than the back button's #1a73e8 so the two read as different controls.
BTN_TEXT is the value ... = white text (#fff) and a white right chevron.

============================
GOAL
============================

Give every image page under {PHOTOS_DIR} a "Next Image" button directly beneath its image, so a visitor can walk the ENTIRE
image corpus one picture at a time. Dark blue ({BTN_FILL}) filled pill, white "Next Image" text, white right chevron. It loads
the NEXT image page in one global traversal of the hierarchy, and the traversal LOOPS (the last image returns to the first).

Re-produced every run (the YAML changes between runs):
  1. A per-image property next_image written INTO {HIERARCHY_FILE}: the image_page (full ~-rooted path) of the next image in the
     traversal.
  2. On every image page (the one-image Level 5 leaf the YAML binds as image_page): the button under the image, href = the
     site-relative URL of next_image; in the same pass the image embed's src and hyperlinks are refreshed (both can drift).

Deterministic and mechanical: no prose, no full {CK_FILE} read, no page created/moved/deleted (pages come from
{IMAGE_PAGE_PROMPT}; run it first if pages are missing). Idempotent.

============================
KNOWLEDGE — READ FIRST
============================

  1. {LAYOUT_GUIDELINES}: its rules OVERRIDE everything here, including the button's color, shape, placement. First, every run.
  2. {CHARTER_FILE}: levels, schema, hard rules (no sidebars.ts edits; {PAGES_CSV} in sync; defamation gate; ban gate).
  3. {HIERARCHY_FILE}: parse fully; source of truth for order and identity (sha256, cid, file_path, image_page).
  4. {PAGES_CSV}: confirms every next_image URL; it wins over a derived URL.
Know without re-reading: {IMAGE_PAGE_PROMPT} owns image pages (creation, prose, embed, layout) and the CK_EVIDENCE_LAYOUT block in
{CUSTOM_CSS}; {NAV_PROMPT} owns cluster/landing navigation and shared button styling. {GEN_SCRIPT} already emits image pages and a
PER-CLUSTER previous/next sequence; the global chain extends that threading.

============================
KNOWLEDGE — THE TRAVERSAL ORDER (WHAT "NEXT" MEANS)
============================

One global sequence S = [p0, p1, ... p(N-1)], built by walking {HIERARCHY_FILE} once in DOCUMENT ORDER, depth-first, pre-order:
  * level_3 nodes in file order.
  * At every cluster node: (a) emit its OWN image pages in the YAML order of its images list, THEN (b) descend into each child
    cluster in YAML order, same rule.
  * Concatenate everything into S.

    next_image(p_i)       = image_page(p_(i+1))     for 0 <= i < N-1
    next_image(p_(N-1))   = image_page(p_0)          the last wraps to the first

Example: level_3 FBI with level_4 groups A, B, C, D; FBI owns no images; A holds five:
    A#1 -> A#2 -> A#3 -> A#4 -> A#5 -> B#1 -> B#2 -> ... -> D#last
D#last's next is the FIRST image of the NEXT level_3 in the file. If FBI owns images (the real one owns 21), they come FIRST,
before Group A. The very last image wraps to the very first. Never a dead end.

What is in S: only existing, publishable image pages. BANNED or VIDEO / UNKNOWN entries have no image page and are skipped (the
chain steps over them). Cluster overview pages are NOT in S. A BYPASSED single-image node still contributes its image page in
document order (bypass is a navigation-link rule only).
{GEN_SCRIPT}'s per-cluster "More In This Cluster" prev/next stays; the "Next Image" button is the separate GLOBAL chain that keeps
going past the cluster end. Keep both; never conflate them.

============================
KNOWLEDGE — THE BUTTON
============================

Placement: directly UNDER the image, inside the image block (the ck-evidence-image region), regardless of prose length; below the
mobile breakpoint it stays under the full-width image. {LAYOUT_GUIDELINES} and {NAV_PROMPT} own the precise markup/CSS home; absent
a rule there, place it as above.
Appearance: filled pill, {BTN_FILL}, white text, ~4px radius, padding matching the back button (siblings, distinguished by color:
back is the lighter #1a73e8). Label "Next Image". A WHITE right chevron after it (prefer inline SVG with stroke:#fff; a plain
right-chevron glyph is an acceptable fallback). Hover/focus may darken or lift; accessible contrast, focus ring, aria-label "Next image".
Target: href = site-relative URL of next_image (strip the {DOCS_DIR} prefix, drop .mdx, leading "/", never /docs, never a domain),
confirmed against {PAGES_CSV} url_path ({PAGES_CSV} wins). If next_image points at a page missing on disk (stale after a rename),
never emit the broken button: recompute S, fix next_image, then render (a button failing the build is a failed run).
Generated markup, regenerated wholesale every run.

============================
KNOWLEDGE — RE-FIXING THE IMAGE EMBED ON EACH PAGE
============================

  * src: /img/evidence/{sha256}.{ext} served from {STATIC_IMG_DIR}. Missing static copy but file_path on disk: copy it (downscale
    over ~2MB) per {IMAGE_PAGE_PROMPT}'s HOSTING THE IMAGE FILE, then reference it. File-less pinned IPFS entry:
    https://ipfs.io/ipfs/{cid}. Nothing resolves: keep the "media pending" state and report; never point an <img> at a file that
    does not serve.
  * Hyperlinks (back/parent, "Related Areas", "More In This Cluster" prev/next) are refreshed from current YAML + {PAGES_CSV}
    exactly as a normal {GEN_SCRIPT} rerun does (reuse it). The "What This Image Shows" prose is preserved (see
    {IMAGE_PAGE_PROMPT}'s BOOKKEEPING FIELDS ON PAGES).
The only NEW page element is the button.

============================
KNOWLEDGE — THE TWO GATES STILL APPLY
============================

  * BAN GATE: ban set = union of {BAN_IMAGES_CSV} (master; match sha256, then cid, then file_path; banned=false is an un-ban) and
    {EXCLUDE_FILE}, re-read every run (never trust the YAML's downstream `banned:`). A banned image is not in S, no next_image points
    at it, no button. A banned image with a live page: report it (deletion is {IMAGE_PAGE_PROMPT}'s job); never link to it.
  * MEDIA-TYPE GATE: video (.mp4/.mov/.webm/.m4v/.mkv/.avi src, or a CID known as video in {VIDEOS_DIR}/manifest.yaml or
    {ROOT_DIR}/IPFS/ipfs.txt) or UNKNOWN entries have no image page, are not in S, are never targets. Never emit <video>, <source>,
    <audio>, or a media <iframe>. Published video pages under {PHOTOS_DIR} stay in place, listed in {FINDINGS_FILE}, not purged,
    not woven into S.
  * Never write under {VIDEOS_L2_DIR}, {VIDEOS_DIR}, {VIDEO_PLANNING_DIR}.

============================
KNOWLEDGE — SAFE PROGRAMMATIC EDIT OF images.yaml
============================

  * Reuse {BIND_SCRIPT}'s emit_node / recount round-trip (the path {IMAGE_PAGE_PROMPT} and {HIERARCHY_PROMPT} rely on) so the file
    is byte-identical except next_image. Never a naive yaml dump (it reorders keys, reflows strings, and loses the visible \uXXXX
    escapes the mirror paths carry).
  * next_image is a per-image string, present on every image in S, holding a real ~-rooted image_page path (never null or empty).
    Images not in S (banned, video, unknown, no image_page) get no next_image: absent, never invalid.
  * After writing: yaml.safe_load must parse it, and the invisible-Unicode scan must pass, or STOP.
  * Writes ONLY next_image. No node/image add, remove, reorder or re-cluster ({HIERARCHY_PROMPT}'s job). Structural problems found
    by the traversal (image without image_page, duplicate image_page, cycle shorter than N) go to {FINDINGS_FILE} and the report.

============================
STAGE 1 — SETUP, PARSE, BUILD THE GLOBAL SEQUENCE
============================

* Read {LAYOUT_GUIDELINES}, {CHARTER_FILE}, {HIERARCHY_FILE}, {PAGES_CSV}.
* Build the ban set (union minus banned=false rows), indexed by sha256, cid, expanded file_path.
* Walk the YAML (THE TRAVERSAL ORDER); type and gate each image (skip banned, video, unknown, no image_page). Survivors in walk order = S.
* Verify S: every image_page resolves to a real .mdx under {PHOTOS_DIR}; no duplicates; |S| equals publishable image pages on disk.
  Mismatch = drift: record in {FINDINGS_FILE}, report ({IMAGE_PAGE_PROMPT} should run first).
* Compute next_image for every image in S.

Output to stdout:
============================
STAGE 1 COMPLETE
YAML images: N total   publishable (in S): N   skipped: N banned / N video / N unknown / N no-page
S length: N   image pages on disk under /Photos: N   (must match)
Wrap-around: last "<title>" -> first "<title>"
Drift problems: N (listed; run {IMAGE_PAGE_PROMPT} first if non-zero)
============================

============================
STAGE 2 — WRITE next_image INTO images.yaml
============================

* Via {BIND_SCRIPT}'s helpers, set next_image on every image in S; leave it absent elsewhere.
* yaml.safe_load re-parse and invisible-Unicode scan must pass, or STOP with the file restored.
* Confirm the byte diff touches only next_image lines.

Output to stdout:
============================
STAGE 2 COMPLETE
next_image values written: N added, N changed, N unchanged
YAML re-parses: yes   invisible-Unicode scan: clean
Diff limited to next_image lines: yes
============================

============================
STAGE 3 — RENDER THE BUTTON + REFRESH THE EMBED ON EACH IMAGE PAGE
============================

Drive this through the image-page generator so the button ships as generated markup.
* Extend {GEN_SCRIPT} (or its shared helpers), for every image page in S, to refresh the embed src and structural links as a normal
  rerun does (prose preserved) and render the button under the image with href = next_image's site-relative URL, confirmed against
  {PAGES_CSV}. Add its style once to the marked shared-button region in {CUSTOM_CSS}, regenerated in place later, touching nothing
  else in that file.
* The button block is replaced wholesale every run; everything else on the page byte-identical.
* No page create/move/delete; nothing under {VIDEOS_L2_DIR}; no sidebars.ts; no new {PAGES_CSV} rows (only correct a row whose
  title or url changed underneath it).

Output to stdout:
============================
STAGE 3 COMPLETE
Image pages updated: N   buttons rendered: N   embeds re-fixed: N
Static copies written this run: N (N downscaled)   media pending: N
CSS button region: written / refreshed
============================

============================
OUTPUT SANITIZATION — NO INVISIBLE UNICODE, EVER (SECURITY RULE)
============================

{HIERARCHY_FILE} after the write, every .mdx touched, and the {CUSTOM_CSS} button region must contain no invisible Unicode
(zero-width, bidi controls, no-break spaces incl. U+202F, word joiners, BOMs, controls, variation selectors, tag chars). Mirror
paths in the YAML keep their visible \uXXXX escapes; never decode them into raw invisibles. Re-scan all written files after every
emit pass and hard-fail on any hit. The full set is enumerated in {HIERARCHY_PROMPT}'s OUTPUT SANITIZATION section.

============================
STAGE 4 — BUILD, VERIFY, REPORT
============================

* cd {SITE_DIR} && npm run build. Must pass (every button href is internal; fix the YAML and rebuild until green).
* Traversal integrity: from the first image page follow next_image N times: all N pages visited exactly once, back at the first
  (ONE cycle of length N). A shorter cycle is a bug: report the break and its neighbours.
* Spot-check 10 image pages across level_3 subtrees: button present directly under the image, dark blue, white text, white right
  chevron, href resolves on disk; image src resolves; prose unchanged.
* Cluster boundaries on at least 3 pages: last image of a level_4 group lands on the next group's first; last image of a level_3
  subtree lands on the next level_3's first.
* Wrap: the file's last image page links to its first.
* BAN + MEDIA AUDIT: no href resolves to a banned image's page; no <video>/<source>/<audio>/media <iframe> emitted under
  {PHOTOS_DIR}; pre-existing contamination count did not rise.
* Nothing modified outside {HIERARCHY_FILE} (next_image only), image pages under {PHOTOS_DIR}, the marked {CUSTOM_CSS} region,
  {STATIC_IMG_DIR}, and (only for a changed title/url) {PAGES_CSV}. sidebars.ts untouched; no new rows.
* Invisible-Unicode scan over everything written.

Output to stdout:
============================
STAGE 4 COMPLETE — FINAL REPORT
Build: PASS/FAIL
Global chain: N image pages, single cycle length N (required), wraps last->first
Buttons rendered: N of N image pages
Cluster-boundary checks: N/3 pass   wrap check: pass/fail
Spot-checks: N/10 buttons resolve, N/10 embeds resolve, prose preserved: yes
BANNED image pages linked to: 0 (required)   media players emitted: 0 (required)
YAML changed: next_image only   pages.csv rows added: 0   sidebars.ts untouched: yes
invisible-Unicode scan: clean
============================

============================
HARD RULES
============================

* {LAYOUT_GUIDELINES} is read first and overrides this prompt (incl. button color, shape, placement); never edited from here.
* THE TRAVERSAL ORDER: document-order depth-first pre-order; own images before child clusters; next_image is the successor in S;
  last wraps to first; exactly one cycle covering every publishable image page once.
* next_image only on images in S; banned, video, unknown and page-less entries are never targets; both gates re-read from source
  files every run, never trusted from the YAML.
* In {HIERARCHY_FILE} this prompt writes next_image and NOTHING else, round-tripped via {BIND_SCRIPT}, re-parsed and scanned.
* The button: {BTN_FILL}, white "Next Image", white right chevron, directly under the image, href = next_image's site-relative URL
  confirmed against {PAGES_CSV}; generated, regenerated wholesale; never a broken internal link.
* No page created, moved or deleted; only the button plus the established embed/link refresh, authored prose preserved; no new
  {PAGES_CSV} rows; sidebars.ts never touched.
* STILL IMAGES ONLY: no media player, nothing written in the video pipeline, no video page in S.
* No invisible Unicode in any emitted file. The build must pass and the chain must verify as one cycle of length N.
