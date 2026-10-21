ROOT_DIR dir is ~/BGit/Bryan_git/charlie-kirk

THIS_DIR dir is {ROOT_DIR}/image_planning
IMAGES_DIR dir is {ROOT_DIR}/images
HIERARCHY_FILE is file {IMAGES_DIR}/images.yaml
  (Moved 2026-07-22 from {THIS_DIR}/hierarchy_images.yaml; that name and location are gone.)
LAYOUT_GUIDELINES is file {THIS_DIR}/layout_guidelines.txt
CHARTER_FILE is file {THIS_DIR}/CLAUDE.md
EXCLUDE_FILE is file {THIS_DIR}/exclude_images.txt
BAN_IMAGES_CSV is file {IMAGES_DIR}/ban_images.csv
HIERARCHY_PROMPT is file {THIS_DIR}/p_update_image_hierarchy.md
FINDINGS_FILE is file {THIS_DIR}/findings_for_hierarchy.md

SITE_DIR dir is {ROOT_DIR}/site
DOCS_DIR dir is {SITE_DIR}/docs
PHOTOS_DIR dir is {DOCS_DIR}/Photos
IMAGES_L2_PAGE is file {PHOTOS_DIR}/overview.mdx
STATIC_IMG_DIR dir is {SITE_DIR}/static/img/evidence
PAGES_CSV is file {ROOT_DIR}/pages.csv
CK_FILE is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt
  (Real file; {ROOT_DIR}/Charlie_Kirk.txt is a symlink to it. Read the real path. READ-ONLY.)
ASSESS_MANUAL is file {ROOT_DIR}/prompts/Assess_Manual.md

MIRROR_DIR dir is ~/_Mirror/Politics/Charlie_Kirk_Mi
MIRROR_SIDECAR_DIR dir is ~/BGit/Bryan_git/personal_large_files_bridge/_Mirror/Politics/Charlie_Kirk_Mi
REPO_SIDECAR_DIR dir is {ROOT_DIR}/.lfbridge

SIBLING VIDEO PIPELINE (read-only from here, never written):
VIDEO_PLANNING_DIR dir is {ROOT_DIR}/videos_planning
VIDEOS_DIR dir is {ROOT_DIR}/videos
VIDEO_HIERARCHY_FILE is file {VIDEOS_DIR}/videos.yaml
VIDEOS_L2_DIR dir is {DOCS_DIR}/Videos

MAX_AGENTS is ... = 12

============================
GOAL
============================

Generate, and keep regenerating, the published pages of the images Level 2 (today Photos, rooted at
{IMAGES_L2_PAGE}) from {HIERARCHY_FILE}. The YAML is already built (cluster tree; per image sha256,
file_path, ai_description, sidecar paths, on_pages (formerly on_site_pages), should_be_on_pages,
image_page, also_filed_in, node site_level_2 / site_page). This prompt READS the YAML and WRITES pages;
it never edits the YAML's data.

Under {PHOTOS_DIR}:
  * Cluster pages: one .mdx per YAML node (level_3/4/5), mostly navigation (TOC of peers, children, images).
  * Image pages: one .mdx per image entry, one image plus a written description linking into the site.
Every page hosts a STILL IMAGE, never a media player (MEDIA-TYPE SCOPE is a hard rule).

Outside {PHOTOS_DIR}, both read-only against the YAML:
  * Stage 5: inline copies on host topic pages (on_pages) become clickable to their image page
    (wrapping anchor only).
  * Stage 6: images in should_be_on_pages not yet on a topic page are PLACED in a generated gallery block
    at the page bottom, each clickable to its image page.

Runs MANY times: read each existing page, rewrite it against current YAML and {LAYOUT_GUIDELINES}.
Idempotent: same inputs, same pages, same anchors.

============================
KNOWLEDGE — MEDIA-TYPE SCOPE: NEVER PUBLISH A VIDEO UNDER /Photos
============================

Video has its own Level 2, plan, generator and layout:
  images                                videos
  {THIS_DIR}                            {VIDEO_PLANNING_DIR}
  {HIERARCHY_FILE}                      {VIDEO_HIERARCHY_FILE}
  {PHOTOS_DIR}                          {VIDEOS_L2_DIR}
  Img_*.mdx leaf pages                  Vid_*.mdx leaf pages
  ck_image_sha256 frontmatter           ck_video_cid + ck_video_sha256
  served from {STATIC_IMG_DIR}          played from a public IPFS gateway

This already went wrong: nine Img_Photo_*.mdx pages under {PHOTOS_DIR}/Official_Narrative/
Narrative_Shot_in_the_Heart/ carry ck_image_cid: none, render a <video> off an IPFS gateway, under "What
This Image Shows". The YAML carries 53 `video:` items and 9 `image:` items whose CID is an .mp4 (fixed
upstream in {HIERARCHY_PROMPT}); this prompt must refuse to publish them anyway.

THE RULE:
  * Type every entry before writing its page. Video when file_path or resolved src ends .mp4 / .mov / .webm /
    .m4v / .mkv / .avi; when its CID belongs to a VIDEO-FILENAMED record in {VIDEOS_DIR}/manifest.yaml or a
    video-filenamed block in {ROOT_DIR}/IPFS/ipfs.txt (parse by filename; scraping CIDs wholesale typed 70
    entries as video when only 9 are); or when the CID is embedded elsewhere inside <video>/<source>. Do not
    use {VIDEO_HIERARCHY_FILE} as an oracle yet (still a schema shell of image data).
  * A video entry gets NO page, static copy, {PAGES_CSV} row, TOC entry, or Stage 5/6 placement. Skip, count.
  * NEVER emit <video>, <source>, <audio>, or a media-player <iframe> into any file under {PHOTOS_DIR}. A
    generator code path that can render video is the defect: remove it.
  * Not confidently typed = UNKNOWN = skipped (an extensionless IPFS CID with empty sha256 is the exact shape of
    all 9 bad entries).
  * Never write under {VIDEOS_L2_DIR}, {VIDEOS_DIR}, {VIDEO_PLANNING_DIR} (read freely).

ALREADY-PUBLISHED VIDEO PAGES under {PHOTOS_DIR} (containing <video> or <source>) are NOT orphans and NOT
purged (their {VIDEOS_L2_DIR} replacements don't exist; inbound links would die). Leave them, count them, list
each path in {FINDINGS_FILE} under
    == VIDEO PAGES PUBLISHED UNDER /Photos — HAND-OFF TO videos_planning ==
and report the count. Migration is a separate, explicitly-approved job (video pages first, then withdrawal).

============================
KNOWLEDGE — READ FIRST, IN THIS ORDER
============================

  1. {LAYOUT_GUIDELINES}: the images-page standards; grows over time; its rules OVERRIDE this prompt. Read first.
  2. {CK_FILE}: source of truth for every concept and what descriptions are grounded in. 400K+ lines: the
     orchestrator loads section headers plus sections relevant to the clusters being processed; each agent
     loads the sections for ITS clusters before writing.
  3. {CHARTER_FILE} (audience, levels, schema, hard rules).
  4. {ASSESS_MANUAL} (site-wide writing and layout; all pages must meet it).
  5. {HIERARCHY_FILE}: parse fully; index every node (_key, title, depth, parent) and image.
  6. {PAGES_CSV}: resolve link targets; kept in sync afterward.

============================
KNOWLEDGE — THE PAGE MODEL
============================

Level 1 = site home; Level 2 = {IMAGES_L2_PAGE} (url /Photos, left-bar "Photos"); YAML level_3 nodes are the
pages under it, then level_4, level_5. Image pages hang off the node that owns the image.

  {PHOTOS_DIR}/overview.mdx                       the Level 2 landing page
  {PHOTOS_DIR}/{L3_key}/overview.mdx              level_3 cluster page
  {PHOTOS_DIR}/{L3_key}/{L4_key}/overview.mdx     level_4 cluster page
  {PHOTOS_DIR}/{L3_key}/{L4_key}/{L5_key}/overview.mdx   level_5 cluster page
  {node dir}/{image_key}.mdx                      image page, in its node's dir

  * Node keys are the YAML _key verbatim.
  * image_key: from the filename stem, sanitized to [A-Za-z0-9_], four words or less, made site-unique by
    appending the first 8 hex of sha256 when the stem collides or is meaningless. Never changes once minted
    (on rerun reuse the existing page's key, matched by recorded sha256).

Navigation (a visitor never dead-ends):
  * Every cluster page has a TOC to its PEERS, PARENT, CHILD clusters, and its image pages.
  * Every image page links to its parent cluster page and previous/next peer images.
  * {IMAGES_L2_PAGE} keeps its prose; only the TOC between {/* PHOTOS_TOC_START */} and {/* PHOTOS_TOC_END */}
    is regenerated (table of every level_3: title link, recursive image count).
  * Single-image nodes are bypassed in every TOC (next section).
Both arrival paths must work: cold browse from the left bar, and topic arrival wanting the evidence one click away.

============================
KNOWLEDGE — SINGLE-IMAGE NODES ARE BYPASSED IN NAVIGATION
============================

A node is BYPASSED when number_of_images_recursive is 1 and it has no child clusters surviving the same test,
i.e. its whole subtree resolves to exactly one image page. This removes a pointless middle click.

LINKS change only:
  * The parent's TOC lists the single IMAGE PAGE instead (its title; count shows 1 image). Peer lists do the same.
  * The image page's back/parent link points to the NEAREST NON-BYPASSED ANCESTOR.
  * Its previous/next links come from the set the parent linked.
The page is still built: the bypassed cluster page is generated at its normal path with its frontmatter
(ck_node_key), concept paragraph and own TOC; it keeps its {PAGES_CSV} row at its true level; it is NEVER an
orphan. The image page keeps its real path under the bypassed node's dir and ck_node_key = that node's _key.
Multi-image nodes are linked normally. Applies at every depth (a one-image level_3 is linked straight to its
image page from the Level 2 TOC).

Example: level_3 "Table And Charlie" > level_4 "1776 Man" (_key Table_1776_Man, one image,
.../Photos/Table_And_Charlie/Table_1776_Man/Img_Photo_24288a.mdx). Table_And_Charlie links straight to
Img_Photo_24288a.mdx titled "1776 Man"; Table_1776_Man/overview.mdx is written, in {PAGES_CSV}, builds, but is in
no TOC; the image's back link goes to Table_And_Charlie.

============================
KNOWLEDGE — IMAGE PAGE LAYOUT SPEC
============================

This prompt writes the WORDS. The LAYOUT is owned by {THIS_DIR}/p_level2_update.md (generator markup plus the
marked CK_EVIDENCE_LAYOUT block in {SITE_DIR}/internals/src/css/custom.css); {LAYOUT_GUIDELINES} wins on conflict.
Recorded so prose suits the shape:
  * No right bar: hide_table_of_contents: true.
  * True aspect ratio; never stretch or crop. Opaque (transparent sources get an opaque backing).
  * The image sits IN THE PAGE, floated right of the prose, scrolling with the text (the earlier viewport-fixed
    bottom-right spec shipped, was wrong, and is superseded). Prose WRAPS around it and resumes full width below;
    no hand-capped prose width.
  * Bounding box sized by the viewport: a share of main-area width (at most 70%) and max height under one screen.
  * Below the mobile breakpoint: full-width block above the prose.
  * Write ordinary paragraphs.
  * After any layout change, test one wide and one tall image visually.

============================
KNOWLEDGE — THE EXCLUSION GATE (NOT EVERYTHING IN THE YAML MAY BE PUBLISHED)
============================

BAN SET = UNION of:
  {BAN_IMAGES_CSV}: the MASTER; rows sha256, cid, file_path, banned, reason, date_added. Match sha256, then cid,
    then file_path. banned=false is an explicit UN-BAN (row kept). New bans go here.
  {EXCLUDE_FILE}: older one-sha256-per-line list; still honoured; never emptied.
minus CSV rows marked false.

The repo charter ({ROOT_DIR}/claude.md, "Banned Media") owns the contract; {HIERARCHY_PROMPT} Stage 3B copies a
`banned:` boolean onto every YAML entry. This prompt does NOT trust or write that field: it re-checks every identity
against the two files every run (a ban living only in regenerated data is not a ban). The YAML value corroborates:
if it and the files disagree, STOP and report.

A banned image gets nothing:
  * NO page under {PHOTOS_DIR} (DELETE an existing one and its {PAGES_CSV} row).
  * NO served copy under {STATIC_IMG_DIR} (delete it; the image is the payload, prose care is not protection).
  * NO placement anywhere (dropped from Stage 6; existing placements, in or outside CK_PLACED_IMAGES, removed).
  * NO LINK INTO IT (no thumbnail, card, TOC row, "see also", Stage 5 wrapper). Cluster counts reflect what is published.
  * NO PIN (any pinning job filters the ban set first; IPFS is irreversible).
The YAML entry is never deleted (complete private record; banning is a publish-time gate that survives regeneration).

Why: the mirror swept in private material (bank/health dashboards, bookings, billing portals, video calls with named
faces; eleven were published in the first full run), plus composites burning an unproven accusation about a living
person into the pixels. When a run finds such material, add a CSV row with reason and date BEFORE the run ends,
record it in {FINDINGS_FILE}, and delete the page and served copy in the same run.

============================
KNOWLEDGE — HOSTING THE IMAGE FILE
============================

* Copy the original to {STATIC_IMG_DIR}/{sha256}.{ext} (lowercase original extension): ASCII-safe, dedupes
  cross-filed images, avoids the mirror's invisible-Unicode filenames (U+202F in macOS screenshot names).
* Reference it as /img/evidence/{sha256}.{ext}. Skip the copy when the target exists.
* No local file but an ipfs_url: embed the IPFS URL (ipfs.io primary; see existing site embeds). Neither: still
  generate the page with the description and a "media pending" note.
* Static assets go only under {STATIC_IMG_DIR}, never {DOCS_DIR}. Over ~2MB: write a downscaled copy (longest side
  2000px, quality ~85); the mirror keeps the original.

============================
KNOWLEDGE — WRITING THE DESCRIPTION
============================

Sources, all used:
  * The inline ai_description (starting point).
  * Sidecars (ai_description_file, ocr_file, transcription_file) whenever they improve the write-up; OCR is often the
    richest (literal on-screen text); quote it where it helps.
  * The hosting pages (on_pages, plus the node's site_page / site_level_2): read each, and explain how the image relates
    to every page it was hosted on.
  * {CK_FILE}: the investigation area the image belongs to, described accurately.
Hyperlink to related Level 2s and Level 3s; link section overviews as /X/overview (not bare /X); resolve every target
against {PAGES_CSV}; prefer routes known to build.

Safe-writing rules (mandatory):
  * The word "defamation" never appears in article text.
  * Never write that any person KNEW anything before the crime, or DID anything immoral or illegal. Check for exactly
    these two failure modes.
  * Never state as fact that a living person committed a crime unless court-proven; use attribution ("according to",
    "allegedly", "reportedly", "researchers have questioned"); frame suspicions as questions or reported claims.
  * Include as MUCH information as possible within those limits (they constrain phrasing, not depth).
  * Raw claims stay private in {CK_FILE} and the planning layer.
  * The YAML is an input, not an authority: ai_description has been wrong about people, places, events, and clustering
    sometimes files an image under a thesis its contents contradict. Write what the evidence shows, say so on the page
    when it differs from the filing, record it in {FINDINGS_FILE}.
Style per {ASSESS_MANUAL}. MDX comments must be {/* ... */}; HTML <!-- --> breaks the compile and deploy.

============================
KNOWLEDGE — BOOKKEEPING FIELDS ON PAGES
============================

Frontmatter:
  * Cluster page: title, ck_node_key: <_key>
  * Image page: title, hide_table_of_contents: true, ck_image_sha256: <sha256>, ck_node_key: <owning node _key>
Reruns match existing pages by ck_image_sha256 / ck_node_key first, filename second, and REFRESH STRUCTURE BUT
PRESERVE PROSE:
  * Regenerated every run: slug and mechanical frontmatter, back button, image src and href, layout classNames and text
    column maxWidth, "Where This Image Appears", "Related Areas", peer/child TOCs, previous/next.
  * Carried forward when present: page title, sidebar_label, frontmatter description, img alt, prose under
    "## What This Image Shows" (image pages), the three paragraphs under "## About This Cluster" (cluster pages).
The writing pass is far more expensive than generation and uses sources the generator never reads; regeneration must
never discard it or resurrect raw YAML text over deliberately scrubbed prose. Baseline boilerplate prose IS refreshed
(the generator recognizes its own). Pages the YAML no longer accounts for are removed as orphans (renamed key or removed
node), counted and reported every run (never the bypassed cluster pages or the video pages above).

============================
KNOWLEDGE — CLICKABLE IMAGES ON HOST PAGES (LINK BACK TO THE IMAGE PAGE)
============================

An image usually appears on its own image page (image_page) AND inline on topic pages (on_pages). Make the inline copy
CLICKABLE to land on its image page (topic arrival at image level). Link-only: nothing else on the host page changes;
the YAML is not written.

URL: image_page is a file path under {SITE_DIR}/docs, e.g.
  ~/BGit/Bryan_git/charlie-kirk/site/docs/Photos/FBI/Img_FBI_Shuts_down_b7009f.mdx
routeBasePath is "/", so strip the {SITE_DIR}/docs prefix and drop .mdx:
  /Photos/FBI/Img_FBI_Shuts_down_b7009f
Site-relative, leading "/", no domain, no /docs. Confirm against {PAGES_CSV} url_path; {PAGES_CSV} wins.

on_pages entries may be stringified dicts, e.g. "{'page': '~/BGit/Bryan_git/charlie-kirk/site/docs/Mic/AES.mdx'}":
extract the path, dedupe, skip and record paths that don't exist.

MATCH the right <img> (only this image, never a neighbor), in order:
  1. IPFS CID in an <img src> or markdown image URL (https://ipfs.io/ipfs/{cid}, https://{cid}.ipfs.dweb.link/..., bare
     /ipfs/{cid}): strongest, host pages key on it.
  2. Served static path /img/evidence/{sha256}.{ext}.
  3. Original filename stem or distinctive alt substring, only when unambiguous on that page.
No match on a claimed host: record "claimed host, not embedded" and move on; never invent an embed or a bare text link.

WRAP, do not replace:
  * Markdown:  ![alt](src)  becomes  [![alt](src)](URL)
  * MDX <img .../>:  <a href="URL"><img ... /></a>, every attribute and style verbatim; only the matched tag (siblings in
    the same grid untouched). Never alter src, alt, sizing, caption.
IDEMPOTENT AND SAFE:
  * Already wrapped to exactly this URL: leave it; never double-wrap.
  * Wrapped by a human to somewhere else (e.g. the original X post): do NOT clobber; record and report for review.
  * Never point an image at a different image's page.
  * A BANNED image is never wrapped: remove the embed and the served copy, report each with the ban reason.
  * N host pages = N edits, one matched <img> each.

============================
KNOWLEDGE — SHOULD_BE_ON_PAGES: PLACING IMAGES ONTO TOPIC PAGES
============================

Per image:
  on_pages            where it IS shown today (observed; ~91% empty).
  should_be_on_pages  where it OUGHT to be shown (reasoned by {HIERARCHY_PROMPT} Stage 11); the COMPLETE desired state,
                      a superset of on_pages, never "extras".
  image_page          its own Level 5 page under {PHOTOS_DIR}.
The work is: should_be_on_pages minus what is already embedded on that page. Most images appear only on their own page;
this brings the evidence to the reader, one click from the full write-up.

SHAPE: list of `page:` tilde paths, e.g.
    should_be_on_pages:
      - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/Suspicious/Cause_of_Death/entrance-or-exit.mdx"
Stage 11 stat()-verified them; re-stat anyway (pages get renamed). Report a non-resolving path; never guess or invent a neighbour.

SRC, in order per image (record the branch):
  1. Served static copy /img/evidence/{sha256}.{ext} when present under {STATIC_IMG_DIR} (the site convention).
  2. Static copy missing but file_path on disk: copy per HOSTING (downscale over ~2MB), then branch 1.
  3. No local file: https://ipfs.io/ipfs/{cid} (IPFS-native entries).
  4. Nothing resolves: skip and report; never emit an <img> that cannot serve.
  CID CAVEAT (measured 2026-07-23): a pinned CID returned 200 from ipfs.io, an unpinned one 504; few entries are pinned. So
  CID is valid as src only for pinned, file-less entries (branch 3). Every emitted <img> carries data-cid so a later
  pinning pass can switch src by rewriting one attribute pair; once fully pinned, branch 3 may move ahead of branch 1.

LINK TARGET: image_page converted as in Stage 5, confirmed against {PAGES_CSV}. No image_page: skip and report (no dead ends).

BLOCK at the BOTTOM of the page, between MDX markers:
    {/* CK_PLACED_IMAGES_START — generated, do not hand-edit */}
    ## Images
    ... gallery ...
    {/* CK_PLACED_IMAGES_END */}
  * Bottom placement: prose above is never reflowed or interrupted; appending is safe to repeat.
  * Regenerated wholesale each run (inside replaced, outside byte-identical). Markers absent: append at EOF; present:
    replace in place (it stays where a human moved it). Empty list: REMOVE the block.
  * Never in a page under {PHOTOS_DIR}, {THIS_DIR}, or any planning file. MDX comments only.

NO DUPLICATES: drop any image whose sha256 OR cid already appears anywhere in the page text with the marked block
stripped out (covers inline /img/evidence embeds, IPFS embeds, older out-of-block placements).

PER-PAGE LOAD: cap 12 (count already-embedded images), keep YAML order (best first), report overflow so the hierarchy
pass can split or prune.

BAN GATE applies (checked against the two files, not the YAML): never placed; existing placements removed, including
ones OUTSIDE a CK_PLACED_IMAGES block, which must be found and cut explicitly. Nothing links into a banned image.

CAPTION: one line per image from the ai_description's first sentence, ending with the link to the full write-up. All
safe-writing rules apply; a failing ai_description is rewritten for the caption and the discrepancy recorded in
{FINDINGS_FILE}. Captions regenerate with the block, so human commentary belongs above the markers or on the image page.

============================
STAGE 1 — SETUP AND READ
============================

* Read in order: {LAYOUT_GUIDELINES}, {CK_FILE} (as in READ FIRST), {CHARTER_FILE}, {ASSESS_MANUAL}, {HIERARCHY_FILE},
  {PAGES_CSV}. Index nodes and images.
* Inventory existing pages under {PHOTOS_DIR}; map by ck_node_key / ck_image_sha256.
* Ensure {STATIC_IMG_DIR} exists.
* BUILD THE BAN SET FIRST: parse {BAN_IMAGES_CSV} with the python3 csv module (reason has commas and quotes) plus
  {EXCLUDE_FILE}; union minus CSV un-bans; index by sha256, cid, expanded file_path; hand it to every agent. A malformed
  banned column is a STOP. Cross-check against the YAML `banned:` and REPORT disagreements (files win; usually
  {HIERARCHY_PROMPT} hasn't re-run since the CSV changed).
* DELETION WORKLIST: existing {PHOTOS_DIR} pages whose ck_image_sha256 is banned, and {STATIC_IMG_DIR} files named for
  a banned sha256. Deleted in Stage 3 before any new page; {PAGES_CSV} rows in Stage 4. Non-empty = banned material is
  live now: say so at the TOP of the report.

Output to stdout:
============================
STAGE 1 COMPLETE
Layout guidelines lines: N
YAML nodes: N level_3 / N level_4 / N level_5   images: N unique sha256
Existing pages found: N cluster / N image
Ban set: N identities ({BAN_IMAGES_CSV} N rows, {EXCLUDE_FILE} N lines, N un-bans)
YAML banned: disagreeing with the files: N (listed — the files win)
DELETION WORKLIST: N live pages + N served copies for banned images
============================

============================
STAGE 2 — PARTITION THE WORK
============================

* Partition level_3 nodes (whole subtrees) into up to {MAX_AGENTS} partitions balanced by number_of_images_recursive
  (fewer for a small corpus; 12 expected on full runs). A subtree never splits across agents (consistent peer links).
* Give each agent its OWN scratch subdirectory, never the shared scratchpad root (agents invent the same helper names,
  apply.py, dump.py, out.json, and overwrite each other mid-run; this has happened).
* Every agent gets the YAML index and {PAGES_CSV} for cross-partition links.

Output to stdout:
============================
STAGE 2 COMPLETE
Partitions: N   (list: partition -> level_3 _keys -> recursive image count)
============================

============================
STAGE 3 — PARALLEL PAGE GENERATION (UP TO {MAX_AGENTS} AGENTS)
============================

Launch all partitions in one burst. Each agent receives its subtree(s), the full node index, the layout spec,
{LAYOUT_GUIDELINES} contents, the writing rules, the ban set, its existing-page map, and pointers to {CK_FILE},
{PAGES_CSV}, {ASSESS_MANUAL}. Each agent, top-down:

* Read the {CK_FILE} sections for its clusters.
* Compute its bypass set first (node -> the one image page it resolves to); build every TOC against it.
* Every cluster node: create or rewrite overview.mdx (title, short concept paragraph grounded in {CK_FILE} under the
  safe-writing rules, full TOC of parent, peers, children, image pages, with bypassed nodes replaced by their image
  pages). Bypassed nodes get their own page the same way.
* Every image entry:
    * FIRST the ban check. Banned: delete any existing page in this node dir and the served copy, hand the {PAGES_CSV}
      row to the orchestrator, report with ban reason; write no page, copy no file, mint no key, omit from every TOC.
      Check before copying so a banned image never lands in {STATIC_IMG_DIR} even momentarily.
    * Type check (MEDIA-TYPE SCOPE); video/UNKNOWN skipped and counted.
    * Ensure the static copy (HOSTING).
    * Existing page for this sha256 in this node dir: read it, then rewrite (BOOKKEEPING). Else mint the key and create.
    * Apply the LAYOUT SPEC; write the description (WRITING THE DESCRIPTION).
    * Safe-writing check on the finished text.
* Return to the orchestrator (never write {PAGES_CSV} or {IMAGES_L2_PAGE} directly): pages created / rewritten /
  unchanged with page_key (node _key or image_key), parent_key, level, url_path, file_path, title, sidebar_label,
  directory, extension, line_count; plus orphans, missing originals, missing sidecars, unresolvable links.

Output to stdout (after all agents return):
============================
STAGE 3 COMPLETE
Agents run: N
Cluster pages: N created, N rewritten (N bypassed in navigation)
Image pages: N created, N rewritten
Banned images skipped (no page written): N
Banned images UN-PUBLISHED this run: N pages deleted, N served copies deleted
  (each listed with sha256, page path, and ban reason)
Static copies written: N (N downscaled)   IPFS embeds: N   media pending: N
Problems reported: N (list)
============================

============================
STAGE 4 — SHARED FILES: LANDING PAGE AND PAGES.CSV
============================

Orchestrator only, single-threaded:
* Regenerate {IMAGES_L2_PAGE}'s TOC between PHOTOS_TOC_START / PHOTOS_TOC_END (first run: insert the markers before the
  final paragraph): every level_3 title linked to its page with recursive count; a bypassed level_3 links straight to its
  image page. Prose outside untouched.
* Merge agent rows into {PAGES_CSV} per the schema in {ROOT_DIR}/claude.md (page_key = node _key or image_key;
  parent_key = parent node _key, image pages parent to their owning node; level = node depth, image pages depth + 1).
  Add new, update retitled/moved, remove rows of banned/orphaned pages deleted this run; report rows whose files vanished
  otherwise rather than deleting blindly.

Output to stdout:
============================
STAGE 4 COMPLETE
Landing page TOC rows: N
pages.csv: N rows added, N updated, N flagged
============================

============================
STAGE 5 — MAKE HOST-PAGE IMAGES CLICKABLE (LINK TO THE IMAGE PAGE)
============================

Image pages now exist, so link targets are real. Follow CLICKABLE IMAGES ON HOST PAGES exactly. Work by host PAGE so each
file is opened and rewritten once:
* Walk every image; banned ones are skipped and their host embeds REMOVED (not merely left unlinked). Derive each URL
  from image_page (confirm against {PAGES_CSV}). Parse on_pages into deduped host paths.
* Invert: host page -> [(cid, sha256, filename, image-page URL), ...].
* Per host page (partitioned across up to {MAX_AGENTS} agents; never split a page): read it; locate each image's one
  matching embed (CID, then static path, then filename/alt); none = "claimed host, not embedded"; wrap in an anchor per the
  idempotency rules; byte-identical elsewhere.
* Never modify pages under {PHOTOS_DIR} here, nor {HIERARCHY_FILE}. Creates, deletes and moves nothing beyond the ban removals.

Output to stdout:
============================
STAGE 5 COMPLETE
Host pages scanned: N   host pages edited: N
Image embeds linked: N   already linked (skipped): N
Claimed hosts with no matching embed: N (list)
Pre-existing anchors left intact: N (list)
============================

============================
STAGE 6 — PLACE THE SHOULD_BE_ON_PAGES IMAGES ONTO THEIR TOPIC PAGES
============================

Makes the YAML's plan real. Follow SHOULD_BE_ON_PAGES exactly. Image pages exist (Stage 3) and {PAGES_CSV} is current (Stage 4).

Plan first:
* Walk every image. Skip and report video/UNKNOWN (this block emits <img> only; a video would become an <img> pointed at an
  .mp4). Skip and count banned. Skip empty should_be_on_pages. Skip and report missing image_page.
* Resolve src (four branches); perform the {STATIC_IMG_DIR} copies NOW, before any page edit.
* Derive and confirm the image-page URL.
* Re-stat every should_be_on_pages path; drop and report missing ones and any under {PHOTOS_DIR}.
* Invert: host page -> ordered (sha256, cid, src, image-page URL, alt, caption), YAML order kept.

Per host page (up to {MAX_AGENTS} agents; never split a page):
* Read it; strip the existing block from the test text; drop images whose sha256 or cid already appear (Stage 5 owns them).
* Cap 12 counting existing embeds, YAML order; report overflow.
* Emit "## Images" with one figure per image: <img> wrapped in an anchor to its Photos URL, data-cid, alt from the
  description, loading="lazy", plus the caption and its "full write-up" link.
* Replace between markers / append at EOF / remove when empty. Byte-identical outside the markers.
* Never modify {PHOTOS_DIR} pages or {HIERARCHY_FILE}.
Styles: one marked CK_PLACED_IMAGES region in {SITE_DIR}/internals/src/css/custom.css beside CK_EVIDENCE_LAYOUT; write once,
regenerate in place, touch nothing else in that file.

Output to stdout:
============================
STAGE 6 COMPLETE
Images with should_be_on_pages: N   placements planned: N over N pages
Src resolution: N static / N copied-then-static / N IPFS gateway / N unresolvable
Pages edited: N   blocks created: N   blocks replaced: N   blocks removed: N
Images placed: N   skipped as already embedded: N
Over the 12-per-page cap: N (list of page -> overflow count)
Missing image_page: N   should_be_on_pages paths that no longer exist: N (list)
============================

============================
OUTPUT SANITIZATION — NO INVISIBLE UNICODE, EVER (SECURITY RULE)
============================

No emitted file (.mdx pages, {PAGES_CSV} rows, components, CSS) may contain invisible Unicode (zero-width, bidi
controls, no-break spaces incl. U+202F, word joiners, BOMs, controls, variation selectors, tag chars).
  * Prose: replace space-like invisibles with a space, delete zero-width/bidi/control chars, collapse whitespace;
    visible non-ASCII may stay.
  * Paths/URLs: sha256-named static copies keep mirror filenames out of pages; if a mirror path must appear, emit
    non-ASCII as visible escapes.
After every emit pass, re-scan all written files and hard-fail on any hit. The full invisible set is enumerated in
{HIERARCHY_PROMPT}'s OUTPUT SANITIZATION section.

============================
STAGE 7 — BUILD, VERIFY, REPORT
============================

* cd {SITE_DIR} && npm run build. Must pass; fix broken links and MDX errors (e.g. a stray <!-- -->) and rebuild until
  green. Stage 5/6 links are internal, so bad targets fail here.
* Spot-check 10 image pages across partitions: frontmatter present, hide_table_of_contents true, src resolves (static file
  or IPFS URL), layout applied, at least one link to another Level 2/3, safe-writing passes, no "defamation".
* Spot-check 5 cluster pages: TOC lists all peers, children, image pages; every link resolves.
* Bypass check on every bypassed node: parent TOC links the image page and NOT the cluster page; the cluster page exists,
  has its {PAGES_CSV} row and builds; the image's back link is the nearest non-bypassed ancestor.
* Spot-check 10 Stage 5 image/host pairs: matched <img> wrapped with the derived URL, no sibling wrapped, URL resolves.
* Spot-check 10 Stage 6 pages: block between its markers at the bottom, every src resolves (static file or a pinned CID),
  every href is a real image page, no image twice, page above the markers unchanged.
* MEDIA-TYPE AUDIT: grep files written this run under {PHOTOS_DIR} for `<video`, `<source`, `<audio`, media `<iframe`:
  must be ZERO. Grep ALL of {PHOTOS_DIR} and report separately (pre-existing contamination; was 9 on 2026-07-23 under
  Official_Narrative/Narrative_Shot_in_the_Heart/; must not rise). Confirm those 9 are still listed in {FINDINGS_FILE}
  and were not purged.
* BAN AUDIT: re-read {BAN_IMAGES_CSV} and {EXCLUDE_FILE} now (rows may have been added mid-run). Fail on any:
    - a {PHOTOS_DIR} page with a banned ck_image_sha256
    - a {STATIC_IMG_DIR} file named for a banned sha256 or cid
    - any {DOCS_DIR} page referencing a banned image (grep sha256, cid, original basename; inside and outside blocks)
    - any page linking to a /Photos URL of a banned image's page
  Grep for identity, not page path (a stale link with no page is still a link into banned material).
* Nothing written under {VIDEOS_L2_DIR}, {VIDEOS_DIR}, {VIDEO_PLANNING_DIR}; no new {PAGES_CSV} row under /Videos.
* {PAGES_CSV} row change matches pages created. Invisible-Unicode scan over everything written (incl. host pages).
* Nothing modified outside {PHOTOS_DIR}, {STATIC_IMG_DIR}, {PAGES_CSV}, Stage 5 host pages (anchors and ban removals),
  Stage 6 host pages (block and ban removals), the marked CSS region, and {IMAGES_L2_PAGE}'s marker section. sidebars.ts untouched.

Output to stdout:
============================
STAGE 7 COMPLETE — FINAL REPORT
Build: PASS/FAIL
Pages now under /Photos: N cluster + N image = N total
Images published: N of N in YAML (N pending media)
BANNED: N images in the ban set — 0 have a page, 0 have a served copy,
  0 are placed on any page, 0 are linked to from anywhere (all four required)
  Un-published this run: N pages + N served copies + N placements removed
Video/UNKNOWN entries skipped, not published: N (handed off to findings)
Media players emitted into /Photos this run: 0 (required)
Pre-existing /Photos pages carrying a video player: N (was 9, must not rise)
Host pages linked: N   image embeds made clickable: N
Topic pages carrying placed images: N   images placed: N
Spot-checks: image pages N/10 pass, cluster pages N/5 pass, host links N/10 pass,
             placement blocks N/10 pass
pages.csv in sync: yes   sidebars.ts untouched: yes   invisible scan: clean
============================

============================
HARD RULES
============================

* Read {LAYOUT_GUIDELINES} first every run; it overrides this prompt; never edit it from here.
* {CK_FILE} is loaded at the start (relevant sections); every description is grounded in it.
* STILL IMAGES ONLY (MEDIA-TYPE SCOPE). No <video>, <source>, <audio> or media <iframe> in any {PHOTOS_DIR} file.
  Existing video pages there are left, listed in {FINDINGS_FILE}, never orphan-purged. Never write the video pipeline's paths.
* WRITES ONLY: pages under {PHOTOS_DIR}; copies under {STATIC_IMG_DIR}; {IMAGES_L2_PAGE}'s marked TOC; marked regions of
  shared layout component/CSS under {SITE_DIR}/internals/src/; {PAGES_CSV} rows; on host topic pages, Stage 5 wrapping anchors
  and Stage 6 marked blocks (plus ban removals). Never {HIERARCHY_FILE}'s data, never {SITE_DIR}/sidebars.ts, no planning notes
  in the site, no pages in {THIS_DIR}.
* Stage 5 only wraps the one matched <img> per host page in an anchor to that image's own page; never double-wraps, never
  clobbers a human anchor.
* Stage 6 places should_be_on_pages images not already on the page, in the regenerated CK_PLACED_IMAGES block at the BOTTOM;
  byte-identical outside; static src (IPFS only for pinned, file-less), data-cid, anchor to its image page; no duplicates, max
  12, nothing banned, nothing without an image_page.
* Single-image nodes are bypassed in navigation but still generated, still in {PAGES_CSV}, never orphans.
* Reruns refresh structure and PRESERVE authored and scrubbed prose; orphan removals counted and reported.
* Image pages: one image, no right bar, true aspect ratio, in-page right float within the viewport-sized bounding box
  (max 70% of main-area width) per the LAYOUT SPEC and {LAYOUT_GUIDELINES}.
* Descriptions: maximum information within safe-writing; never "defamation"; no prior-knowledge or immoral/illegal-conduct
  claims; attribution; /X/overview links verified against {PAGES_CSV}.
* Nothing in the ban set is ever published, placed, linked to, or pinned; whatever exists for it is DELETED (page, served copy,
  placements, {PAGES_CSV} row). The set is re-read from the two files every run, never inherited from the YAML. Newly found
  non-public material gets a CSV row before the run ends. Prose care does not substitute for withholding the image.
* Up to {MAX_AGENTS} agents partitioned by subtree (or by host page in Stages 5-6); shared files written only by the orchestrator.
* No invisible Unicode in any emitted file. The build must pass before the run is complete.
