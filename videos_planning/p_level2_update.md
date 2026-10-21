ROOT_DIR dir is ~/BGit/Bryan_git/charlie-kirk

THIS_DIR dir is {ROOT_DIR}/videos_planning
VIDEOS_DIR dir is {ROOT_DIR}/videos
HIERARCHY_FILE is file {VIDEOS_DIR}/videos.yaml
  (Created 2026-07-23 from images.yaml with only the SCHEMA converted; {HIERARCHY_PROMPT} replaces the data. Never generate
   pages from unconverted data: see THE STALE-DATA PRECONDITION.)
VIDEO_MANIFEST is file {VIDEOS_DIR}/manifest.yaml
LAYOUT_GUIDELINES is file {THIS_DIR}/layout_guidelines.txt
CHARTER_FILE is file {THIS_DIR}/CLAUDE.md
EXCLUDE_FILE is file {THIS_DIR}/exclude_videos.txt
BAN_VIDEOS_CSV is file {VIDEOS_DIR}/ban_videos.csv
FINDINGS_FILE is file {THIS_DIR}/findings_for_hierarchy.md
VIDEO_PAGE_PROMPT is file {THIS_DIR}/p_yaml_to_site.md
HIERARCHY_PROMPT is file {THIS_DIR}/p_update_video_hierarchy.md

GENERATOR_DIR dir is {THIS_DIR}/generator
GEN_SCRIPT is file {GENERATOR_DIR}/gen_videos_pages.py
VERIFY_SCRIPT is file {GENERATOR_DIR}/verify_videos.py

SITE_DIR dir is {ROOT_DIR}/site
DOCS_DIR dir is {SITE_DIR}/docs
VIDEOS_L2_DIR dir is {DOCS_DIR}/Videos
CUSTOM_CSS is file {SITE_DIR}/internals/src/css/custom.css
VIDEOS_L2_PAGE is file {VIDEOS_L2_DIR}/overview.mdx
POSTER_DIR dir is {SITE_DIR}/internals/static/img/video_posters
  (internals/static is the only served static dir; {SITE_DIR}/static is not served. Page URL: /img/video_posters/{sha256}.jpg.)
HOME_PAGE is file {DOCS_DIR}/index.mdx
PAGES_CSV is file {ROOT_DIR}/pages.csv
CK_FILE is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt
  (Real file; {ROOT_DIR}/Charlie_Kirk.txt is a symlink to it. Read the real path. READ-ONLY.)
ASSESS_MANUAL is file {ROOT_DIR}/prompts/Assess_Manual.md

IMAGE_PLANNING_DIR dir is {ROOT_DIR}/image_planning

TOC_COLUMNS is ... = 2
MAX_AGENTS is ... = 12

============================
GOAL
============================

Update the NAVIGATION pages of the videos Level 2 ({VIDEOS_L2_PAGE}, every Level 3 and Level 4 page under {VIDEOS_L2_DIR}, and
deeper cluster pages) so each LEADS with a TOC carrying the visitor to the next level down, letting a visitor walk from the left
bar to any individual video page without dead-ending.

{HIERARCHY_FILE} is the source of truth (clusters, names, nesting, videos). READ it, WRITE pages; (almost) never write the YAML.

The walk ends at the Level 5 video page (one video, one write-up). {VIDEO_PAGE_PROMPT} owns the WORDS; this prompt guarantees each is
reachable, correctly named, one click from its owning cluster page, and correctly LAID OUT. Layout is a templating concern: fix it by
changing {GEN_SCRIPT}'s markup and the CSS block it writes into {CUSTOM_CSS}, then rerun over every page. Never hand-edit video pages
for layout.

============================
THE STALE-DATA PRECONDITION
============================

Before generating any page, run the same HARD-STOP gate as {VIDEO_PAGE_PROMPT}:
  * Entries whose file_path ends .jpg .jpeg .png .gif .webp .heic: above zero = STOP.
  * Entries whose ai_description begins "This image": above zero = STOP.
  * Entries with a non-empty cid: under half = STOP.
Report the counts and tell the operator to run {HIERARCHY_PROMPT} (its Stage 6 rebuild) first.

============================
SCOPE — WHAT THIS PROMPT TOUCHES
============================

Writes:
  * {VIDEOS_L2_PAGE}: the marked TOC section only.
  * Every cluster overview.mdx under {VIDEOS_L2_DIR} (Level 3, Level 4, deeper cluster nodes).
  * The LAYOUT of every Level 5 video page (player element, its wrapper, the prose wrapper, inline styles on them); prose untouched.
  * {CUSTOM_CSS}: only between /* CK_VIDEO_LAYOUT_START */ and /* CK_VIDEO_LAYOUT_END */. The images pipeline's CK_EVIDENCE_LAYOUT
    block lives in the same file; writing into it would destroy the image layout across ~1,850 pages.
  * {PAGES_CSV} rows for these pages.
  * {GEN_SCRIPT}: the implementation of the rules (structural and layout changes go here and are rerun).
  * {POSTER_DIR}: poster frames the generator extracts.
Does NOT write:
  * {HIERARCHY_FILE} (read-only; record problems in {FINDINGS_FILE} for {HIERARCHY_PROMPT}).
  * Video page PROSE ({VIDEO_PAGE_PROMPT}'s). A missing leaf may be created as a stub so a TOC link resolves (reported).
  * {SITE_DIR}/sidebars.ts (never, unless explicitly asked).
  * {VIDEOS_L2_DIR}/buckley-carlson-kash-patel-valhalla.mdx (hand-written; linked from the TOC, otherwise left alone, never an orphan).
  * Anything under {IMAGE_PLANNING_DIR}, {ROOT_DIR}/images, {DOCS_DIR}/Photos, {SITE_DIR}/static/img/evidence.
  * Any topic page elsewhere in {DOCS_DIR}, or anything outside {VIDEOS_L2_DIR} other than {PAGES_CSV} rows, the marked CSS block,
    and {POSTER_DIR}.

============================
KNOWLEDGE — READ FIRST, IN THIS ORDER
============================

  1. {LAYOUT_GUIDELINES}: READ FIRST, EVERY RUN, IN FULL. Every point was added after a real defect shipped (inherited from images
     or found here). Restate each point before working; treat each as a defect to verify fixed by run end. It OVERRIDES this prompt
     (where they disagree, correct this prompt). It carries the whole Level 5 layout spec (placement, bounding box and size
     calculation, player attributes: no autoplay, no loop, preload metadata, poster, controls inside the height ceiling; the CSS
     block's job; the verification checklist on built output). Every point, including new ones, is implemented in {GEN_SCRIPT} and
     the {CUSTOM_CSS} block, rerun over every page, verified on the built output.
  2. {CHARTER_FILE} (audience, levels, schema, hard rules).
  3. {HOME_PAGE}: the TOC pattern to imitate.
  4. {HIERARCHY_FILE}: parse fully; index nodes (_key, title, depth, parent, site_level_2, site_page, number_of_videos,
     number_of_videos_recursive) and videos (cid, ipfs_pinned, sha256, file_path).
  5. {PAGES_CSV}: link targets; kept in sync.
  6. {ASSESS_MANUAL}.
  7. {CK_FILE}: headers plus sections for the clusters in play; no cluster paragraph without its section in context.

============================
KNOWLEDGE — THE MODEL: THE HOME PAGE TOC
============================

{HOME_PAGE} is good because: the TOC IS the page, starting right under the H1; links grouped under headings that themselves link to
the section overview; balanced side-by-side columns keep long lists on one screen; short human labels.
Ours use {TOC_COLUMNS} columns instead of three (better at our narrower main area). Markup, in the home page's idiom:

  <div style={{ display: "flex", justifyContent: "space-between", gap: "2rem" }}>
  <div style={{ flex: 1 }}>
    * [Label](/Videos/.../overview)
  </div>
  <div style={{ flex: 1 }}>
    * [Label](/Videos/.../Vid_key)
  </div>
  </div>

Split in reading order, balanced by count, child clusters before video pages.

VIDEO LABELS NEED MORE THAN A TITLE: files are named by X status id, and "2067372027623715212" tells a visitor nothing. Every video row
carries a human label (speaker and claim, from the YAML title or {VIDEO_MANIFEST} description) and the duration where readable, e.g.
"Candace Owens — exploding-mic explainer (4:12)". Never a bare filename or status id.

============================
KNOWLEDGE — THE LEVEL MODEL AND THE YAML MAPPING
============================

  Level 1  {DOCS_DIR}/index.mdx, the site home.
  Level 2  {VIDEOS_L2_PAGE}, url /Videos, left-bar "Videos", _category_.json position 20. Where a cold visitor arrives.
  Level 3  one page per level_3 node.   Level 4  one per level_4 node.
  Level 5  video pages. A level_5 CLUSTER node also becomes a cluster page; its videos are its leaves.

  level_3:
    - level_3:
        title: "The Exploding Microphone Thesis"  -> the H1 and the link label
        _key: Mic_Thesis                          -> dir name and url segment: /Videos/Mic_Thesis/overview
        site_level_2: ["Mic"]                     -> site docs dirs covered; cross-link targets
        site_page: "site/docs/Mic/overview.mdx"   -> the written page mirrored; link it as /Mic/overview
        number_of_videos: 6                       -> videos owned directly (its own leaf pages)
        number_of_videos_recursive: 14            -> the count shown on the PARENT's TOC line
        level_4:
          - level_4:
              title: "Shaped Charge Counterarguments"
              _key: Mic_Shaped_Charge
              number_of_videos: 8
              number_of_videos_recursive: 8
              videos:
                - video: ...
  -> on {VIDEOS_L2_DIR}/Mic_Thesis/overview.mdx:
       * **[Shaped Charge Counterarguments](/Videos/Mic_Thesis/Mic_Shaped_Charge/overview)** — 8 videos

A level_5 node works the same one level further down, cross-linking its site_page when present, e.g.
        level_5:
          - level_5:
              title: "Buckley Carlson on the Valhalla Comment"
              _key: Videos_Buckley_Kash
              site_page: "site/docs/Videos/buckley-carlson-kash-patel-valhalla.mdx"
A node may own videos with no child clusters; never invent a level. Titles verbatim as labels; _key verbatim as dir name, url segment
and page_key. Video page FILENAMES carry the Vid_ prefix (greppable, never collide with Img_ pages).

============================
KNOWLEDGE — WHAT MAKES A GREAT CLUSTER PAGE
============================

Navigation: hand the visitor the next click.
  * TOC at the TOP, directly under the H1 and back button; nothing of substance above it.
  * Every YAML child appears, nothing extra.
  * Child clusters first, bolded, with recursive counts; then the node's own video pages.
  * {TOC_COLUMNS} balanced columns; human labels (no keys, filenames or bare status ids; speaker, claim, duration on video rows).
  * A CLUSTER PAGE NEVER EMBEDS PLAYERS (six autoloading IPFS players is slow, heavy, unusable on a phone). Small poster thumbnails
    beside rows are fine. The player lives only on the Level 5 page.
  * A one-to-three sentence concept paragraph AFTER the TOC, grounded in {CK_FILE}.
  * A cross-link to the written section mirrored (site_page / site_level_2).
  * Up-link to the parent and peer links to siblings; no dead ends.
  * Every link resolves; overviews as /X/overview, never bare /X; checked against {PAGES_CSV}.
Both arrival paths must work (cold from the left bar; topic arrival mid-tree wanting to WATCH, which is why up and peer links matter).

============================
KNOWLEDGE — PER-LEVEL SPECIFICATION
============================

=== Level 2: {VIDEOS_L2_PAGE} ===
  * Keep the frontmatter and the existing prose (footage types: production/TPUSA, security, drone, eyewitness; uses for timeline and
    shooter-location analysis; claims about unreleased or deleted footage).
  * TOC between {/* VIDEOS_TOC_START */} and {/* VIDEOS_TOC_END */}, fully regenerated; outside untouched. MOVE the markers if needed
    so the TOC sits directly under the H1, above the prose.
  * Every level_3 in YAML order: title label, /Videos/{L3_key}/overview href, number_of_videos_recursive; {TOC_COLUMNS} columns.
  * A row for buckley-carlson-kash-patel-valhalla.mdx so it is not stranded.
  * One line above the TOC: total clusters, total videos, and how many are playable now (cid reported pinned by the local node).

=== Level 3: {VIDEOS_L2_DIR}/{L3_key}/overview.mdx ===
  * Frontmatter: displayed_sidebar: docs, slug, title, sidebar_label, description, ck_node_key (= _key).
  * Back button to /Videos/overview. H1 from the node title.
  * TOC right below: level_4 children bolded with recursive counts, then owned video pages.
  * Concept paragraph(s) after; cross-links to site_page and each site_level_2; Related Areas: up-link to Videos plus every peer level_3.

=== Level 4: {VIDEOS_L2_DIR}/{L3_key}/{L4_key}/overview.mdx ===
  * Same shape; back button to the parent Level 3; TOC: level_5 cluster children first, then video pages; Related Areas: up-link to
    the parent, peers = sibling level_4s.

=== Level 5: the video pages (WORDS: {VIDEO_PAGE_PROMPT}; LAYOUT: here) ===
  * Reachability: each exists at {node dir}/Vid_{video_key}.mdx, its title matches the parent TOC label, the link resolves. Missing
    page: create a minimal stub (frontmatter with ck_video_cid, ck_video_sha256, ck_node_key; the player, or the media-pending note
    when there is no pinned cid; a placeholder heading) and report it. Never overwrite an existing page's prose.
  * Layout, every page, every run, from {GEN_SCRIPT}: fixed structure (frontmatter with hide_table_of_contents: true, back button, H1,
    player wrapper, prose wrapper holding the whole write-up). Behaviour lives in the CK_VIDEO_LAYOUT block, not per-page inline
    styles. The class contract (ck-video-wrap, ck-video-media, ck-video-text), source order, bounding box and size calculation, wrap
    behaviour, player attributes and look are specified in {LAYOUT_GUIDELINES}: implement it, invent nothing.
  * The player src is always a public IPFS gateway URL built from the cid; video bytes are NEVER copied into the site; posters (in
    {POSTER_DIR}) are the only local media.
  * Intrinsic dimensions (to choose wrapped vs full-width): ffprobe the local file under {VIDEOS_DIR} or the mirror. No local file
    (fresh clone, manifest-only): assume 16:9, note it in a page comment, report the entry.
  * Verified on the BUILT output (Stage 5).

============================
KNOWLEDGE — RERUNS PRESERVE PROSE
============================

  Regenerated every run: mechanical frontmatter, back button, the whole TOC, counts, Related Areas, peer and child lists, column
  markup; on Level 5 pages the player element with its src, poster, sources and attributes.
  Carried forward when present: title, sidebar_label, frontmatter description, authored paragraphs under "## About This Cluster"; on
  Level 5 pages everything under "## What This Video Shows" including hand-placed transcript quotes and timestamps.
Generator boilerplate IS refreshed; hand-written, enriched or safe-writing-scrubbed prose survives every regeneration. Pages the YAML no
longer accounts for are orphans: remove, count, report. overview.mdx and buckley-carlson-kash-patel-valhalla.mdx are PROTECTED, never orphans.

============================
KNOWLEDGE — GATES THAT STILL APPLY
============================

  * BAN SET = union of {BAN_VIDEOS_CSV} (MASTER; rows sha256, cid, file_path, banned, reason, date_added; match sha256, then cid, then
    file_path; banned=false is an explicit un-ban) and {EXCLUDE_FILE} (older identifier list, honoured). Read both before building
    navigation. A banned video gets no Level 5 page, no TOC entry, no poster, no pin, NO LINK INTO IT from anywhere (card, poster
    thumbnail, "see also", bypass target); existing pages and posters are deleted; counts reflect what is published; a node whose every
    video is banned publishes no page. The YAML `banned:` (copied by {HIERARCHY_PROMPT} Stage 6B) only corroborates; re-check the two
    files every run; report disagreements (files win). Newly found non-public material (private documents, unrelated third-party
    records, bystanders with no connection): add a CSV row with reason and date before the run ends and note it in {FINDINGS_FILE}.
    IPFS publication is not reversible, so the gate is checked before a page is written.
  * BYPASS AND BAN INTERACT: a node resolving to one video page is bypassed (parents and peers link straight to the video page; see
    {VIDEO_PAGE_PROMPT}). If that one video is banned there is nothing to bypass to: the node is unpublished and in no TOC. Apply the ban
    set BEFORE computing the bypass set.
  * NOTHING IS EVER PINNED by this prompt. An unpinned entry gets the honest media-pending treatment (per {VIDEO_PAGE_PROMPT}); report
    it loudly; pinning is a separate approved job.
  * Safe writing on every word: never "defamation"; never that a person knew anything before the crime or did anything immoral or
    illegal; never a living person committing a crime as fact unless court-proven; attribution throughout. A cluster paragraph
    summarising what its footage claims attributes it to the speakers ("clips in which several witnesses describe ..."), never the site.
  * MDX comments must be {/* ... */}; HTML <!-- --> breaks the compile and deploy.
  * needs_split nodes (over twelve videos): render as is and report for {HIERARCHY_PROMPT}.
  * SHOULD_BE_ON_PAGES IS NOT THIS PROMPT'S PROPERTY: {HIERARCHY_PROMPT} Stage 13 reasons it; {VIDEO_PAGE_PROMPT} Stage 6 places cards in
    CK_PLACED_VIDEOS blocks on topic pages. This prompt never reads it for navigation, never places a video outside {VIDEOS_L2_DIR}, and
    never creates, edits, reorders or removes a CK_PLACED_VIDEOS block or the images pipeline's CK_PLACED_IMAGES block. A stale or
    malformed block is REPORTED in {FINDINGS_FILE}, never repaired here. (video_page = which page IS the video; on_pages = where it IS
    shown; should_be_on_pages = where it OUGHT to be. Navigation uses the tree and video_page only.)

============================
OUTPUT SANITIZATION — NO INVISIBLE UNICODE, EVER
============================

No emitted .mdx page or {PAGES_CSV} row may contain invisible Unicode (zero-width, bidi controls, no-break spaces incl. U+202F, word
joiners, BOMs, controls, variation selectors, tag chars).
  * Prose: replace space-like invisibles with a space, delete zero-width/bidi/control chars, collapse whitespace; visible non-ASCII may stay.
  * Pages reference media by CID and posters by sha256 names, so source filenames never reach a page.
  * Labels or durations lifted from transcriptions, OCR sidecars or {VIDEO_MANIFEST} are untrusted: sanitize before emitting.
After every emit pass, rescan everything written and hard-fail on any hit. The set is enumerated in {GEN_SCRIPT} and {HIERARCHY_PROMPT}.

============================
STAGE 1 — READ AND INDEX
============================

* Run the STALE-DATA PRECONDITION gate; stop on failure.
* Read the knowledge files in order. Parse the YAML into a node index (depth, parent, _key, title, site bindings, own and recursive
  counts, videos).
* Inventory existing {VIDEOS_L2_DIR} pages (ck_node_key / ck_video_cid / ck_video_sha256); mark the two protected pages.
* BUILD THE BAN SET: parse {BAN_VIDEOS_CSV} with the python3 csv module (create with header sha256,cid,file_path,banned,reason,date_added
  if missing) plus {EXCLUDE_FILE}; union minus un-bans; index by sha256, cid, expanded file_path; mark banned videos so Stage 2 computes
  bypasses and TOCs over publishable videos only. Cross-check the YAML `banned:`; report disagreements.
* Ask the local IPFS node which CIDs it pins (for the "playable now" count), with the ban set filtered out first: a banned video found
  pinned is a {FINDINGS_FILE} item and an unpinning worklist entry for an approved job, never "playable".

Output to stdout:
============================
STAGE 1 COMPLETE
Precondition gate: PASS (image file_paths 0, "This image" prose 0, cid coverage N%)
Layout guideline lines: N
YAML: N level_3 / N level_4 / N level_5 clusters, N unique videos
Playable now: N   unpinned: N   no cid: N
Existing pages: N cluster / N video / 2 protected
Ban set: N identities ({BAN_VIDEOS_CSV} N rows, {EXCLUDE_FILE} N lines, N un-bans)
YAML banned: disagreeing with the files: N (listed — the files win)
Banned videos found PINNED: N (findings + unpinning worklist, not "playable")
Nodes with no publishable video left after the ban: N (not published, no TOC entry)
============================

============================
STAGE 2 — DECIDE THE STRUCTURAL DIFF
============================

* For every cluster node, compute its correct TOC from the YAML and diff against the page: missing children, stale labels, wrong counts,
  broken links, wrong column count, TOC below the prose, bare status-id labels, players embedded on a cluster page.
* Resolve every intended link against {PAGES_CSV} and the docs tree; list the unresolvable.
* List pages to rewrite, orphans to remove, video stubs to create.

Output to stdout:
============================
STAGE 2 COMPLETE
Cluster pages needing rewrite: N   Orphans: N   Missing video pages: N
Bare-id labels found: N   Players on cluster pages: N
Unresolvable link targets: N (list)   needs_split nodes: N (list)
============================

============================
STAGE 3 — APPLY
============================

Prefer the generator: change the rule in {GEN_SCRIPT}, rerun, every page moves together. Hand edits only for one-offs.
If {GEN_SCRIPT} doesn't exist yet, write a NEW file under {GENERATOR_DIR}, using {IMAGE_PLANNING_DIR}/generator/gen_photos_pages.py as
prior art; never edit the images generator; never let the video generator write CK_EVIDENCE_LAYOUT, the Photos tree, or static/img/evidence.
* Update {GEN_SCRIPT} for every rule here ({TOC_COLUMNS} columns, TOC above prose, counts, human labels with durations, cross-links, prose
  preservation, no players on cluster pages).
* Update its video-page markup and CK_VIDEO_LAYOUT block for every {LAYOUT_GUIDELINES} point the output doesn't yet satisfy (layout is
  fixed here and nowhere else).
* Run it over the whole tree.
* Where prose judgment is needed on many clusters, partition level_3 subtrees across up to {MAX_AGENTS} agents (never split a subtree;
  each agent gets its own scratch subdirectory, since agents invent the same helper filenames and collide).
* {PAGES_CSV} and {VIDEOS_L2_PAGE} are written by the orchestrator only.

Output to stdout:
============================
STAGE 3 COMPLETE
Cluster pages rewritten: N (L2 1, L3 N, L4 N, L5-cluster N)
Video pages relaid out: N  Inline width caps removed: N
Posters written: N   Dimensions read by ffprobe: N   16:9 assumed: N
Video stubs created: N     Orphans removed: N
Layout guideline points implemented: N of N
Agents run: N
============================

============================
STAGE 4 — PAGES.CSV
============================

* Merge rows for every cluster page created, rewritten, retitled or removed, per the schema in {ROOT_DIR}/claude.md: page_key = node
  _key, parent_key = parent node _key, level = node level, url_path, file_path, title, sidebar_label, directory, extension,
  has_frontmatter, line_count.
* Never delete rows for pages that still exist; flag rows whose files vanished.

Output to stdout:
============================
STAGE 4 COMPLETE
pages.csv: N rows added, N updated, N flagged
============================

============================
STAGE 5 — BUILD AND VERIFY
============================

* Run {VERIFY_SCRIPT} over the whole corpus.
* cd {SITE_DIR} && npm run build. Must pass; fix and rebuild until green.
* Walk down by hand from {VIDEOS_L2_PAGE} through three random level_3 nodes to a video page: every step shows the next level's links at the top.
* Spot-check five Level 3 and five Level 4 pages: TOC at top, all YAML children, {TOC_COLUMNS} columns, counts match, human labels (no bare
  status ids), no players, up and peer links resolve, cross-link to the mirrored page present.
* LAYOUT CHECK: run {LAYOUT_GUIDELINES}' verification section in full (grep checks on the built CSS bundle and generated pages, then its
  browser eyeball checks) in a clean profile with NO IPFS Companion. Every point passes before completion.
* PLAYBACK CHECK: in that clean profile, press play on five video pages across clusters; each must load and play with audio (plays-for-you-
  with-Companion, dead-for-visitors is the default failure of this pipeline).
* CK_EVIDENCE_LAYOUT in {CUSTOM_CSS} byte-identical to before; {DOCS_DIR}/Photos and {SITE_DIR}/static/img/evidence untouched.
* Invisible-Unicode scan over everything written.
* Nothing outside {VIDEOS_L2_DIR}, {POSTER_DIR}, {PAGES_CSV}, the marked CSS block and {GEN_SCRIPT} changed; {HIERARCHY_FILE} and
  sidebars.ts untouched.

Output to stdout:
============================
STAGE 5 COMPLETE — FINAL REPORT
Build: PASS/FAIL
Cluster pages under /Videos: L2 1, L3 N, L4 N, L5-cluster N
Video pages reachable: N of N in YAML (N excluded, N stubs pending write-up)
Walk-down checks: N/3 pass   Spot-checks: L3 N/5, L4 N/5
Playback check: N/5 played in a clean profile
Layout: in-flow yes/no  opaque yes/no  text-wrap yes/no  controls reachable
        yes/no  autoplay 0  loop 0  stale width caps: N
pages.csv in sync: yes   videos/videos.yaml untouched: yes
CK_EVIDENCE_LAYOUT intact: yes   Photos untouched: yes
sidebars.ts untouched: yes   invisible scan: clean
============================

============================
HARD RULES
============================

* The STALE-DATA PRECONDITION is a hard stop before anything else.
* {LAYOUT_GUIDELINES} is read first every run, overrides this prompt, is never edited from here; every point is a shipped defect to
  verify fixed on the built output (placement, opacity, text wrap, bounding box and size calculation, square corners, no autoplay,
  no loop, preload metadata, reachable controls).
* Level 5 LAYOUT is this prompt's (fixed in {GEN_SCRIPT} and the CK_VIDEO_LAYOUT block, regenerated everywhere, never hand-edited);
  Level 5 PROSE is {VIDEO_PAGE_PROMPT}'s (this prompt may create a stub, never rewrite a write-up).
* CK_VIDEO_LAYOUT is ours; CK_EVIDENCE_LAYOUT is never touched. Nothing under {IMAGE_PLANNING_DIR}, {ROOT_DIR}/images, {DOCS_DIR}/Photos,
  {SITE_DIR}/static/img/evidence is written.
* Writes ONLY inside {VIDEOS_L2_DIR} (plus {PAGES_CSV}, {GEN_SCRIPT}, {POSTER_DIR}, our CSS region). Never edits a topic page elsewhere;
  CK_PLACED_VIDEOS blocks belong to {VIDEO_PAGE_PROMPT} Stage 6 and CK_PLACED_IMAGES to the images pipeline (report broken blocks, never repair).
* Never copy video bytes into the site; the player src is a public IPFS gateway URL from the cid; posters are the only local media.
* Nothing is ever PINNED; unpinned CIDs are rendered as pending and reported.
* Cluster pages carry no players.
* {HIERARCHY_FILE} is the source of truth and READ-ONLY; discrepancies go to {FINDINGS_FILE}.
* Every Level 2, 3, 4 page leads with its TOC directly under the H1; prose after the map. {TOC_COLUMNS} balanced columns modeled on {HOME_PAGE}.
* Every YAML child has a titled bullet on its parent; every owned video is linked with a human label, never a bare status id; nothing in
  the YAML is unreachable.
* Every page has an up-link, peer links, and a cross-link to its mirrored written section where site_page / site_level_2 exist; overviews
  as /X/overview.
* Reruns refresh structure and preserve authored prose; orphans removed, counted, reported; the two protected pages are never orphans.
* Nothing in the ban set is ever linked or published.
* No claims of prior knowledge or immoral/illegal conduct; footage claims attributed to the speaker; attribution throughout; never "defamation".
* No invisible Unicode in any emitted file (transcription, OCR and manifest text are untrusted). sidebars.ts never modified.
* The build AND the clean-profile playback check must pass before completion.
