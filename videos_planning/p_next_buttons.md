ROOT_DIR dir is ~/BGit/Bryan_git/charlie-kirk

THIS_DIR dir is {ROOT_DIR}/videos_planning
VIDEOS_DIR dir is {ROOT_DIR}/videos
HIERARCHY_FILE is file {VIDEOS_DIR}/videos.yaml
  (Created 2026-07-23 from images.yaml with only the SCHEMA converted; {HIERARCHY_PROMPT} replaces the data. See THE STALE-DATA PRECONDITION.)
VIDEO_MANIFEST is file {VIDEOS_DIR}/manifest.yaml
LAYOUT_GUIDELINES is file {THIS_DIR}/layout_guidelines.txt
CHARTER_FILE is file {THIS_DIR}/CLAUDE.md
EXCLUDE_FILE is file {THIS_DIR}/exclude_videos.txt
BAN_VIDEOS_CSV is file {VIDEOS_DIR}/ban_videos.csv
FINDINGS_FILE is file {THIS_DIR}/findings_for_hierarchy.md

GENERATOR_DIR dir is {THIS_DIR}/generator
GEN_SCRIPT is file {GENERATOR_DIR}/gen_videos_pages.py
BIND_SCRIPT is file {GENERATOR_DIR}/bind_video_pages.py
EMIT_SCRIPT is file {GENERATOR_DIR}/emit_yaml.py
VERIFY_SCRIPT is file {GENERATOR_DIR}/verify.py

VIDEO_PAGE_PROMPT is file {THIS_DIR}/p_yaml_to_site.md
NAV_PROMPT is file {THIS_DIR}/p_level2_update.md
HIERARCHY_PROMPT is file {THIS_DIR}/p_update_video_hierarchy.md

SITE_DIR dir is {ROOT_DIR}/site
DOCS_DIR dir is {SITE_DIR}/docs
VIDEOS_L2_DIR dir is {DOCS_DIR}/Videos
CUSTOM_CSS is file {SITE_DIR}/internals/src/css/custom.css
VIDEOS_L2_PAGE is file {VIDEOS_L2_DIR}/overview.mdx
POSTER_DIR dir is {SITE_DIR}/internals/static/img/video_posters
PAGES_CSV is file {ROOT_DIR}/pages.csv
CK_FILE is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt
  (Real file; {ROOT_DIR}/Charlie_Kirk.txt is a symlink to it. READ-ONLY.)
ASSESS_MANUAL is file {ROOT_DIR}/prompts/Assess_Manual.md

SIBLING IMAGE PIPELINE (never read for data, never written):
IMAGE_PLANNING_DIR dir is {ROOT_DIR}/image_planning
IMAGES_DIR dir is {ROOT_DIR}/images
IMAGE_HIERARCHY_FILE is file {IMAGES_DIR}/images.yaml
PHOTOS_DIR dir is {DOCS_DIR}/Photos
IMAGE_NEXT_PROMPT is file {IMAGE_PLANNING_DIR}/p_next_buttons.md

BTN_LABEL is the string "Next Video"
BTN_FILL is the value ... = a dark blue button fill (navy, e.g. #0d2b6b),
  darker than the back button's #1a73e8 so the two read as different controls.
BTN_TEXT is the value ... = white text (#fff) and a white right chevron.

============================
GOAL
============================

Give every video page under {VIDEOS_L2_DIR} a "Next Video" button directly beneath its player, so a visitor can walk the ENTIRE video
corpus one clip at a time. Dark blue ({BTN_FILL}) filled pill, white "Next Video" text, white right chevron. It loads the NEXT video
page in one global traversal of the hierarchy, and the traversal LOOPS (the last video returns to the first).

Re-produced every run (the YAML changes between runs):
  1. A per-video property next_video written INTO {HIERARCHY_FILE}: the video_page (full ~-rooted path) of the next video.
  2. On every video page (the one-video Level 5 leaf the YAML binds as video_page): the button under the player, href = next_video's
     site-relative URL; in the same pass the player is re-emitted correctly (gateway src, poster, fallback sources, attributes all drift).

Deterministic and mechanical: no write-up prose, no full {CK_FILE} read, no page created/moved/deleted (pages come from
{VIDEO_PAGE_PROMPT} and {NAV_PROMPT}; run them first if pages are missing). Idempotent.

============================
THE STALE-DATA PRECONDITION (CHECK THIS BEFORE WRITING A SINGLE BYTE)
============================

HARD STOP gate before Stage 1 (same as the sibling prompts):
  * Entries whose file_path ends .jpg .jpeg .png .gif .webp .heic: above zero = STOP; tell the operator to run {HIERARCHY_PROMPT}
    (its Stage 6 rebuild) first.
  * Entries whose ai_description begins "This image": above zero = STOP.
  * Entries with a non-empty cid: under half = STOP.
Status 2026-07-23: PASSES (400 videos, 0 image paths, 0 "This image", 372 of 400 with a CID, every one with a video_page). Still run it.

============================
SCOPE — VIDEOS ONLY, ADDITIVE, ONE CONTROL
============================

  * THE ONLY INPUT IS THE VIDEO CORPUS: read/write {HIERARCHY_FILE} (next_video only) and video pages under {VIDEOS_L2_DIR}. DO NOT READ
    OR WRITE {IMAGE_HIERARCHY_FILE}, {IMAGE_PLANNING_DIR}, {PHOTOS_DIR}, {SITE_DIR}/static/img/evidence. {IMAGE_NEXT_PROMPT} was the
    prior art; never copy a file from it (that reverts this directory's conversion).
  * ONE CONTROL: add the button to each Level 5 video page and refresh the player embed already there. Never delete, move, resize,
    retarget or reword anything else; never touch an image, <img>, CK_PLACED_IMAGES block, or the CK_EVIDENCE_LAYOUT block. Every image
    and prose paragraph on an edited page is byte-identical after the run.
Our stylesheet territory: the CK_VIDEO_LAYOUT block and ck-video-* classes. The images generator owns CK_EVIDENCE_LAYOUT and
ck-evidence-* in the same file (writing theirs destroys the image layout, and their next run destroys ours).

============================
KNOWLEDGE — READ FIRST
============================

  1. {LAYOUT_GUIDELINES}: OVERRIDES everything here, incl. button color, shape, placement. First, every run. The player stays IN THE
     PAGE (no position:fixed / sticky), square corners, opaque, controls always reachable; the button must break none of that.
  2. {CHARTER_FILE}: levels, schema, hard rules (no sidebars.ts edits; {PAGES_CSV} in sync; defamation gate; ban gate; never copy
     video bytes into static; never pin as a side effect).
  3. {HIERARCHY_FILE}: parse fully; source of truth for order and identity (cid, ipfs_pinned, sha256, file_path, video_page).
  4. {PAGES_CSV}: confirms every next_video URL; it wins over a derived URL.
Know without re-reading: {VIDEO_PAGE_PROMPT} owns page WORDS; {NAV_PROMPT} owns LAYOUT and navigation (player markup, TOCs,
CK_VIDEO_LAYOUT). {GEN_SCRIPT} already emits the pages and a per-cluster "Other Videos In This Section" list; reuse its machinery.

============================
KNOWLEDGE — THE TRAVERSAL ORDER (WHAT "NEXT" MEANS)
============================

One global sequence S = [p0, p1, ... p(N-1)], built by walking {HIERARCHY_FILE} once in DOCUMENT ORDER, depth-first, pre-order:
  * level_3 nodes in file order.
  * At every cluster node (any depth): (a) emit its OWN video pages in the YAML order of its videos list, THEN (b) descend into each
    child cluster in YAML order, same rule.
  * Concatenate everything into S.

    next_video(p_i)       = video_page(p_(i+1))     for 0 <= i < N-1
    next_video(p_(N-1))   = video_page(p_0)          the last wraps to the first

Example: level_3 FBI with level_4 groups A, B, C, D; FBI owns no videos; A holds five:
    A#1 -> A#2 -> A#3 -> A#4 -> A#5 -> B#1 -> B#2 -> ... -> D#last
D#last's next is the FIRST video of the NEXT level_3 in the file. FBI's own videos, if any, come FIRST. The very last wraps to the
very first. Never a dead end.

What is in S:
  * Only video pages that ACTUALLY EXIST under {VIDEOS_L2_DIR} and are publishable. video_page "" (not written yet): NOT in S, the
    chain steps over it, reported for {VIDEO_PAGE_PROMPT}. BANNED: no page, not in S.
  * MEDIA-PENDING pages ARE in S (cid "" or unpinned still have a full page: title, write-up, sources, honest pending note). Real
    destinations; buttons into and out of them work.
  * Cluster overview pages are NOT in S.
  * A BYPASSED single-video node still contributes its video page in document order (bypass is a navigation-link rule only).
  * PROTECTED pages: overview.mdx is a cluster page, never in S. The hand-written buckley-carlson-kash-patel-valhalla.mdx (no ck_
    frontmatter) is NOT in S and gets NO button (body untouched). If its video also has a generated page in the YAML, that generated
    page is the S node; record the collision in {FINDINGS_FILE} for a human.
{GEN_SCRIPT}'s per-cluster "Other Videos In This Section" list (inside the CK_NAV block) stays; the button is the separate GLOBAL chain
that continues past the cluster end. Keep both; never conflate them.

============================
KNOWLEDGE — THE BUTTON
============================

Placement: directly UNDER the player, between the ck-video-wrap block (from {GEN_SCRIPT}'s player_block) and the ck-video-text prose
wrapper, regardless of prose length. Below the 996px mobile breakpoint it stays under the full-width player. On a MEDIA-PENDING page
(no <video>, only the poster/pending block in ck-video-wrap) it goes directly beneath that block. {LAYOUT_GUIDELINES} and {NAV_PROMPT}
own the precise markup/CSS home; absent a rule there, place it as above.
Appearance: filled pill, {BTN_FILL}, white text, ~4px radius, padding matching back_button in {GEN_SCRIPT} (#1a73e8; siblings
distinguished by color). Label "Next Video". WHITE right chevron after it (prefer inline SVG with stroke:#fff; plain glyph is an
acceptable fallback). Hover/focus may darken or lift; accessible contrast, focus ring, aria-label "Next video". The button keeps its
pill radius; it never inherits the player's border-radius:0.
Target: href = next_video's site-relative URL (strip {DOCS_DIR}, drop .mdx, leading "/", no /docs, no domain), confirmed against
{PAGES_CSV} url_path ({PAGES_CSV} wins). If next_video points at a page missing on disk, never emit the broken button: recompute S,
fix next_video, then render.
Generated markup, regenerated wholesale every run. Its style lives ONCE as a ck-video-next rule in the CK_VIDEO_LAYOUT block, written
by {GEN_SCRIPT}, regenerated in place, touching nothing else (never CK_EVIDENCE_LAYOUT).

============================
KNOWLEDGE — RE-FIXING THE PLAYER EMBED ON EACH PAGE
============================

Drive through {GEN_SCRIPT}'s established refresh; do not re-implement it.
  * src: PUBLIC IPFS GATEWAY URLs built from the cid, one <source> per gateway in the order of the single list in
    {GENERATOR_DIR}/ipfs_gateways.py (v1 base32 form computed at generation time; the YAML keeps CIDv0). Retired gateways (dweb.link,
    ipfs.io, w3s.link) are never emitted. VIDEO BYTES ARE NEVER COPIED INTO {SITE_DIR}/static; a src at /static/, a relative path or
    localhost is a defect.
  * cid "" OR ipfs_pinned false (confirmed at run time with `ipfs pin ls --type=recursive`, not the YAML field): NO player; keep the
    honest "media pending" note and poster if any. Report the count and CIDs; never pin as a side effect (irreversible; separate approved job).
  * poster: /img/video_posters/{sha256}.jpg when present under {POSTER_DIR} (the only video media served locally). Generate new
    posters here only if trivially extractable from a local file as the sibling prompts do; a missing poster never withholds the button.
  * hyperlinks: back button, "Where This Video Also Appears", "Also Filed Under", and "Other Videos In This Section" are refreshed
    from current YAML + {PAGES_CSV} as a normal rerun does. "What This Video Shows" prose (between the CK_PROSE markers, and any page
    with ck_authored: true) is preserved.
The only NEW page element is the button.

============================
KNOWLEDGE — THE GATES STILL APPLY
============================

  * BAN GATE: ban set = union of {BAN_VIDEOS_CSV} (master; match sha256, then cid, then file_path; banned=false is an un-ban) and
    {EXCLUDE_FILE}, re-read every run (never trust the YAML's `banned:`). A banned video is not in S, no next_video points at it, no
    button. A banned video with a live page: report in {FINDINGS_FILE} (deletion is {VIDEO_PAGE_PROMPT}'s job); never link to it.
    Newly found non-public material: add a CSV row with reason and date and record it in {FINDINGS_FILE} before the run ends. IPFS is
    irreversible, so the gate is checked before a button is minted.
  * MEDIA-TYPE GATE: a still-image file_path or "This image" prose is a stale-data leak that already STOPPED the run at the
    precondition; never weave such an entry into S.
  * Never write under {IMAGE_PLANNING_DIR}, {IMAGES_DIR}, {PHOTOS_DIR}, {SITE_DIR}/static/img/evidence; never emit an <img> gallery
    or image-evidence block.

============================
KNOWLEDGE — SAFE PROGRAMMATIC EDIT OF videos.yaml
============================

  * Reuse {BIND_SCRIPT} (emit_node / recount) and {EMIT_SCRIPT} so the file is byte-identical except next_video. Never a naive yaml
    dump (reorders keys, reflows strings, loses the escapes mirror paths carry).
  * next_video is a per-video string on every video in S, holding a real ~-rooted video_page path (never null or empty). Videos not in
    S (banned, empty video_page) get none: absent, never invalid.
  * After writing: yaml.safe_load must parse it and the invisible-Unicode scan must pass, or STOP with the file restored.
  * Writes ONLY next_video. No node/video add, remove, reorder or re-cluster ({HIERARCHY_PROMPT}'s job). Structural problems (video
    without video_page, duplicate video_page, cycle shorter than N) go to {FINDINGS_FILE} and the report.

============================
STAGE 1 — SETUP, PARSE, BUILD THE GLOBAL SEQUENCE
============================

* Run the STALE-DATA PRECONDITION gate; stop on failure.
* Read {LAYOUT_GUIDELINES}, {CHARTER_FILE}, {HIERARCHY_FILE}, {PAGES_CSV}.
* Build the ban set (union minus banned=false rows), indexed by sha256, cid, expanded file_path.
* Ask the local node which CIDs it pins (`ipfs pin ls --type=recursive`) for Stage 3. Pin status decides only whether a PLAYER is
  emitted; it never removes a media-pending page from S.
* Walk the YAML (THE TRAVERSAL ORDER); skip banned, no video_page, or a video_page that is not a real .mdx under {VIDEOS_L2_DIR}.
  Survivors in walk order = S.
* Verify S: every video_page resolves; no duplicates; |S| equals publishable video pages on disk (excluding the two protected pages
  and cluster overviews). Mismatch = drift: record in {FINDINGS_FILE}, report ({VIDEO_PAGE_PROMPT} / {NAV_PROMPT} should run first).
* Compute next_video for every video in S.

Output to stdout:
============================
STAGE 1 COMPLETE
Precondition gate: PASS (image file_paths 0, "This image" prose 0, cid coverage N%)
YAML videos: N total   publishable (in S): N   skipped: N banned / N no-page / N no-file
S length: N   video pages on disk under /Videos: N   (must match)
Playable now: N (cid + pinned)   media-pending in S: N (unpinned/no-cid, still walked)
Wrap-around: last "<title>" -> first "<title>"
Drift problems: N (listed; run {VIDEO_PAGE_PROMPT}/{NAV_PROMPT} first if non-zero)
============================

============================
STAGE 2 — WRITE next_video INTO videos.yaml
============================

* Via {BIND_SCRIPT} / {EMIT_SCRIPT}, set next_video on every video in S; leave it absent elsewhere.
* yaml.safe_load re-parse and invisible-Unicode scan must pass, or STOP with the file restored.
* Confirm the byte diff touches only next_video lines.

Output to stdout:
============================
STAGE 2 COMPLETE
next_video values written: N added, N changed, N unchanged
YAML re-parses: yes   invisible-Unicode scan: clean
Diff limited to next_video lines: yes
============================

============================
STAGE 3 — RENDER THE BUTTON + REFRESH THE EMBED ON EACH VIDEO PAGE
============================

* Extend {GEN_SCRIPT} (or its shared helpers), for every video page in S, to refresh the player src / poster / fallback sources and
  structural links as a normal rerun does (media-pending entries keep their block; prose between CK_PROSE markers preserved), and
  render the button after the ck-video-wrap block and before ck-video-text, href = next_video's URL confirmed against {PAGES_CSV}.
  Add the ck-video-next rule once to the CK_VIDEO_LAYOUT region in {CUSTOM_CSS}, regenerated in place later, touching nothing else.
* The button block is replaced wholesale every run; everything else on the page byte-identical.
* No page create/move/delete; nothing under {PHOTOS_DIR}; no sidebars.ts; no new {PAGES_CSV} rows (only correct a row whose title or
  url changed underneath it). Never touch the buckley-carlson body, CK_EVIDENCE_LAYOUT, or any CK_PLACED_IMAGES block.

Output to stdout:
============================
STAGE 3 COMPLETE
Video pages updated: N   buttons rendered: N   embeds re-fixed: N
Players emitted: N   media-pending (no player, button present): N
CSS button region (ck-video-next in CK_VIDEO_LAYOUT): written / refreshed
============================

============================
OUTPUT SANITIZATION — NO INVISIBLE UNICODE, EVER (SECURITY RULE)
============================

{HIERARCHY_FILE} after the write, every .mdx touched, and the {CUSTOM_CSS} button region must contain no invisible Unicode (zero-width,
bidi controls, no-break spaces incl. U+202F, word joiners, BOMs, controls, variation selectors, tag chars). Mirror paths keep their
visible escapes; never decode them into raw invisibles. Labels lifted from transcriptions, OCR or {VIDEO_MANIFEST} are untrusted:
sanitize first. Re-scan all written files after every emit pass and hard-fail on any hit. The full set is in {GEN_SCRIPT} and
{HIERARCHY_PROMPT}.

============================
STAGE 4 — BUILD, VERIFY, REPORT
============================

* cd {SITE_DIR} && npm run build. Must pass (hrefs are internal; fix the YAML and rebuild until green).
* Traversal integrity: from the first video page follow next_video N times: all N visited once, back at the first (ONE cycle of
  length N). A shorter cycle is a bug: report the break and its neighbours.
* Spot-check 10 video pages across level_3 subtrees: button directly under the player (or pending block), dark blue, white text,
  white right chevron, href resolves on disk; player src is a public gateway URL (never /static/, relative, localhost); prose unchanged.
* Cluster boundaries on at least 3 pages (last of a level_4 group -> next group's first; last of a level_3 subtree -> next level_3's first).
* Wrap: the file's last video page links to its first.
* MEDIA-PENDING on at least 2 pages: pending note (no dead player), working button, reachable from the previous video.
* BAN + IMAGE AUDIT: no href to a banned video's page; no button on the buckley-carlson page; no <img> gallery or CK_EVIDENCE /
  CK_PLACED_IMAGES block written; CK_EVIDENCE_LAYOUT byte-identical; {PHOTOS_DIR} and {SITE_DIR}/static/img/evidence untouched.
* Nothing modified outside {HIERARCHY_FILE} (next_video only), video pages under {VIDEOS_L2_DIR}, the CK_VIDEO_LAYOUT button region,
  and (only for a changed title/url) {PAGES_CSV}. sidebars.ts untouched; no new rows. Invisible-Unicode scan clean. Nothing pinned.

Output to stdout:
============================
STAGE 4 COMPLETE — FINAL REPORT
Build: PASS/FAIL
Global chain: N video pages, single cycle length N (required), wraps last->first
Buttons rendered: N of N video pages
Cluster-boundary checks: N/3 pass   wrap check: pass/fail
Media-pending checks: N/2 (pending note + working button)
Spot-checks: N/10 buttons resolve, N/10 players are IPFS-gateway, prose preserved: yes
BANNED video pages linked to: 0 (required)   buckley-carlson button: 0 (required)
CK_EVIDENCE_LAYOUT intact: yes   Photos untouched: yes   nothing pinned: yes
YAML changed: next_video only   pages.csv rows added: 0   sidebars.ts untouched: yes
invisible-Unicode scan: clean
============================

============================
HARD RULES
============================

* {LAYOUT_GUIDELINES} is read first and overrides this prompt (incl. button color, shape, placement); never edited from here.
* The STALE-DATA PRECONDITION is a hard stop; never write next_video or a button from unconverted image data.
* THE TRAVERSAL ORDER: document-order depth-first pre-order; own videos before child clusters; successor in S; last wraps to first;
  exactly one cycle over every publishable video page. Media-pending pages ARE in S; banned and page-less videos are NOT.
* next_video only on videos in S; the ban gate is re-read from {BAN_VIDEOS_CSV}/{EXCLUDE_FILE} every run, never trusted from the YAML.
* In {HIERARCHY_FILE} this prompt writes next_video and NOTHING else, round-tripped via {BIND_SCRIPT} / {EMIT_SCRIPT}, re-parsed and scanned.
* The button: {BTN_FILL}, white "Next Video", white right chevron, directly under the player, href = next_video's site-relative URL
  confirmed against {PAGES_CSV}; generated, regenerated wholesale; never a broken link; style once in CK_VIDEO_LAYOUT, never CK_EVIDENCE_LAYOUT.
* No page created, moved or deleted; only the button plus the established player/link refresh; authored prose preserved; no new
  {PAGES_CSV} rows; sidebars.ts never touched.
* VIDEO ONLY: never copy video bytes into {SITE_DIR}/static; player src is a public gateway URL; no <img> gallery, image-evidence block,
  or write in the images pipeline; no still in S.
* Nothing is ever PINNED; unpinned / CID-less entries keep their pending note and still get a button; report their count and CIDs.
* overview.mdx and buckley-carlson-kash-patel-valhalla.mdx are never orphans, never in S; the buckley-carlson body is never edited.
* No invisible Unicode in any emitted file. The build must pass and the chain must verify as one cycle of length N.
