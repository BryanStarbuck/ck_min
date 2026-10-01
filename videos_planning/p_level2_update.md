ROOT_DIR dir is ~/BGit/Bryan_git/charlie-kirk

THIS_DIR dir is {ROOT_DIR}/videos_planning
VIDEOS_DIR dir is {ROOT_DIR}/videos
HIERARCHY_FILE is file {VIDEOS_DIR}/videos.yaml
  Created 2026-07-23 as a copy of {ROOT_DIR}/images/images.yaml with only the
  SCHEMA converted to videos. Its DATA is replaced with the real video corpus by
  {HIERARCHY_PROMPT}. This prompt reads the YAML and must not generate pages
  from unconverted data — see THE STALE-DATA PRECONDITION below.
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
POSTER_DIR dir is {SITE_DIR}/static/img/video_posters
HOME_PAGE is file {DOCS_DIR}/index.mdx
PAGES_CSV is file {ROOT_DIR}/pages.csv
CK_FILE is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt
  (Real file. Moved 2026-09-19. ~/BGit/Bryan_git/charlie-kirk/Charlie_Kirk.txt is now a symlink to it —
   use that only to verify the location; always read and write the real path.)
ASSESS_MANUAL is file {ROOT_DIR}/prompts/Assess_Manual.md

IMAGE_PLANNING_DIR dir is {ROOT_DIR}/image_planning

TOC_COLUMNS is ... = 2
MAX_AGENTS is ... = 12

============================
GOAL
============================

Update the NAVIGATION pages of the videos Level 2 section — the Level 2 landing
page ({VIDEOS_L2_PAGE}), every Level 3 page, and every Level 4 page under
{VIDEOS_L2_DIR} — so that each one leads with a table of contents that carries
the visitor to the next level down, and so that a visitor can walk from the left
bar all the way to an individual video page without ever dead-ending.

{HIERARCHY_FILE} is the source of truth for what is correct: what the clusters
are, what they are called, how they nest, and which videos belong to each. This
prompt READS that YAML and WRITES pages. It primarily — almost certainly always
— does not write back into the YAML.

The end of the walk is the individual video page: one video, one write-up. Those
leaf pages are spoken of as Level 5 — the last click. This prompt does not
author their bodies; {VIDEO_PAGE_PROMPT} owns the WORDS. This prompt guarantees
that every one of them is reachable, correctly named, exactly one click from the
cluster page that owns it, and correctly LAID OUT.

Level 5 layout is this prompt's job. {LAYOUT_GUIDELINES} states how a video must
sit on its page, and every Level 5 page must satisfy it. Layout is a templating
concern, not a per-page concern: it is fixed by changing the markup {GEN_SCRIPT}
emits and the CSS block {GEN_SCRIPT} writes into {CUSTOM_CSS}, then rerunning
over every page. Never fix layout by hand-editing video pages.

============================
THE STALE-DATA PRECONDITION
============================

{HIERARCHY_FILE} was created by copying images/images.yaml and converting the
KEYS to the video schema. Its DATA started out as the image corpus.
{HIERARCHY_PROMPT} Stage 0 is what replaces that with the real video corpus.

Before generating any page, run the same gate {VIDEO_PAGE_PROMPT} runs:

  * Count entries whose file_path ends in an image extension (.jpg .jpeg .png
    .gif .webp .heic). Above zero → STOP.
  * Count entries whose ai_description begins "This image". Above zero → STOP.
  * Count entries with a non-empty cid. Under half → STOP.

Report the counts and tell the operator to run {HIERARCHY_PROMPT} Stage 0 first.
This is a hard stop, not a warning.

============================
SCOPE — WHAT THIS PROMPT TOUCHES
============================

Writes:

  * {VIDEOS_L2_PAGE} — the marked TOC section only; its prose is left alone.
  * {VIDEOS_L2_DIR}/{L3_key}/overview.mdx — every Level 3 cluster page.
  * {VIDEOS_L2_DIR}/{L3_key}/{L4_key}/overview.mdx — every Level 4 cluster page.
  * Deeper cluster overview.mdx pages (Level 5 cluster nodes, where the YAML
    nests that far) — same treatment, same rules.
  * The LAYOUT of every Level 5 video page — the player element, its wrapper,
    the prose wrapper, and any inline style on them. The prose between those
    wrappers is not touched.
  * {CUSTOM_CSS} — the marked block between /* CK_VIDEO_LAYOUT_START */ and
    /* CK_VIDEO_LAYOUT_END */ only. Everything outside those markers in that
    file belongs to the rest of the site and is never touched. In particular
    the images pipeline's CK_EVIDENCE_LAYOUT block lives in the same file and
    writing into it would destroy the image layout across ~1,850 pages.
  * {PAGES_CSV} rows for the pages above.
  * {GEN_SCRIPT} — the generator is the implementation of the rules below.
    Structural and layout rules are changed by editing the generator and
    rerunning it, never by hand-editing pages one at a time.
  * {POSTER_DIR} — poster frames, when the generator extracts them.

Does NOT write:

  * {HIERARCHY_FILE} — read-only input. If the YAML is wrong, record it in
    {FINDINGS_FILE} and leave the YAML for {HIERARCHY_PROMPT} to fix.
  * Video page PROSE (the write-up inside the Vid_*.mdx leaf pages) — owned by
    {VIDEO_PAGE_PROMPT}. This prompt may create a missing leaf page as a stub
    so the TOC link resolves, and reports it, but does not rewrite an existing
    one's prose. Their LAYOUT is a different matter and is this prompt's job —
    see GOAL and the Level 5 spec below.
  * {SITE_DIR}/sidebars.ts — never, unless explicitly asked.
  * {VIDEOS_L2_DIR}/buckley-carlson-kash-patel-valhalla.mdx — the hand-written
    topic page that predates this pipeline. It is linked from the TOC and
    otherwise left alone. Never an orphan.
  * Anything under {IMAGE_PLANNING_DIR}, {ROOT_DIR}/images, {DOCS_DIR}/Photos,
    or {SITE_DIR}/static/img/evidence.
  * Anything outside {VIDEOS_L2_DIR} other than {PAGES_CSV} rows, the marked
    CSS block, and {POSTER_DIR}.

============================
KNOWLEDGE — READ FIRST, IN THIS ORDER
============================

At the very start of every run — before reading anything else, before touching
any file — read into the context window:

  1. {LAYOUT_GUIDELINES} — the standards file for video pages. THIS IS READ
     FIRST, EVERY RUN, WITHOUT EXCEPTION. It is short. It is also the most
     load-bearing file in this prompt, because everything in it was put there
     after a real, visible defect shipped to the live site — inherited from the
     images pipeline where the defect was first found, or found here since. Read
     it in full, restate each of its points before doing any work, and treat
     every point as a defect that must be verified fixed by the end of the run —
     not as advice. Its rules OVERRIDE any conflicting rule in this prompt;
     where this prompt and that file disagree, that file is right and this
     prompt is stale and should be corrected to match.

     Its points today concern Level 5 video pages. It carries the whole layout
     specification — how the player sits on the page, the bounding box and how
     the player's size is calculated inside it, the player attribute rules (no
     autoplay, no loop, preload metadata, poster, controls inside the height
     ceiling), what the CSS block must do, and the verification checklist to run
     against the built output. This prompt does not restate any of that; read it
     there and implement it exactly.

     Every point in it, and any point added to it later, gets the same
     treatment: implement it in {GEN_SCRIPT} and in the {CUSTOM_CSS} marked
     block, rerun over every page, and verify it on the built output.

  2. {CHARTER_FILE} — the videos_planning charter: the audience model, the level
     model, the YAML schema, the hard rules.
  3. {HOME_PAGE} — the site home page. Read it for the TOC pattern to imitate
     (see THE MODEL below). It is the reference for what a good landing page
     looks like on this site.
  4. {HIERARCHY_FILE} — parse fully. Index every node (_key, title, depth,
     parent, site_level_2, site_page, number_of_videos,
     number_of_videos_recursive) and every video (cid, ipfs_pinned, sha256,
     file_path).
  5. {PAGES_CSV} — the master page index, for resolving link targets and for
     keeping in sync afterward.
  6. {ASSESS_MANUAL} — the site-wide writing and layout guide.
  7. {CK_FILE} — the master investigation file, for the one or two sentences of
     concept prose each cluster page carries. Load the section headers plus the
     sections relevant to the clusters being processed. This prompt writes far
     less prose than {VIDEO_PAGE_PROMPT} does, so a full read is not required —
     but no cluster paragraph is written without the relevant section in
     context.

============================
KNOWLEDGE — THE MODEL: THE HOME PAGE TOC
============================

{HOME_PAGE} is the pattern to imitate. What makes it good:

  * The table of contents IS the page. It starts immediately under the H1. A
    visitor sees the whole map before they see any prose.
  * Links are grouped under a heading that is itself a link to the section
    overview, so the visitor can either dive into a child or open the section.
  * The links sit in balanced side-by-side columns, so a long list stays on one
    screen instead of becoming a scroll.
  * Labels are the human titles, short and readable.

Our videos pages copy that shape with one difference: {TOC_COLUMNS} columns
instead of the home page's three. Two columns read better at the narrower main
area these pages have, and they stay readable on a laptop.

Column markup follows the home page's own idiom:

  <div style={{ display: "flex", justifyContent: "space-between", gap: "2rem" }}>
  <div style={{ flex: 1 }}>
    * [Label](/Videos/.../overview)
  </div>
  <div style={{ flex: 1 }}>
    * [Label](/Videos/.../Vid_key)
  </div>
  </div>

Split the list across the columns in reading order, balanced by count, child
clusters before video pages.

VIDEO LABELS NEED MORE THAN A TITLE. A row that reads only "2067372027623715212"
tells a visitor nothing, and this corpus names its files by X status id. Every
video row in a TOC carries a human label — the speaker and the claim, from the
YAML title or the {VIDEO_MANIFEST} description — and, where the generator can
read it, the duration. "Candace Owens — exploding-mic explainer (4:12)" is a
row a visitor can choose from. Never emit a bare filename or status id as a
label.

============================
KNOWLEDGE — THE LEVEL MODEL AND THE YAML MAPPING
============================

Site levels:

  Level 1  {DOCS_DIR}/index.mdx — the site home.
  Level 2  {VIDEOS_L2_PAGE} — the videos landing page, url /Videos, left-bar
           label "Videos", _category_.json position 20. One page. This is where
           a cold visitor arrives.
  Level 3  one page per level_3 node in {HIERARCHY_FILE}.
  Level 4  one page per level_4 node.
  Level 5  the individual video pages — one video, one write-up. Where the YAML
           nests a level_5 CLUSTER node, that node also becomes a cluster page
           and follows the cluster rules; its videos are its leaves.

The YAML shape and what each field becomes on the page:

  level_3:
    - level_3:
        title: "The Exploding Microphone Thesis"  -> the H1 and the link label
        _key: Mic_Thesis                          -> the directory name and url
                                                     segment:
                                                     /Videos/Mic_Thesis/overview
        site_level_2: ["Mic"]                     -> the site docs dirs this
                                                     cluster covers; cross-link
                                                     targets
        site_page: "site/docs/Mic/overview.mdx"
                                                  -> the written page this
                                                     cluster mirrors; link it as
                                                     /Mic/overview
        number_of_videos: 6                       -> videos owned directly by
                                                     this page (its own leaf
                                                     pages)
        number_of_videos_recursive: 14            -> the count shown on the
                                                     PARENT's TOC line for this
                                                     node

A level_4 nested under a level_3 means exactly this: the Level 3 page carries a
bullet that hyperlinks to that Level 4 page, labeled with the level_4 node's
title.

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

A level_5 node nested under a level_4 works the same way one level further down,
and where it carries a site_page it also cross-links to the written page it
mirrors:

        level_5:
          - level_5:
              title: "Buckley Carlson on the Valhalla Comment"
              _key: Videos_Buckley_Kash
              site_page: "site/docs/Videos/buckley-carlson-kash-patel-valhalla.mdx"

A node may own videos with no child clusters at all. That is normal and correct:
some video pages hang directly off a Level 3, some off a Level 4, and a Level 4
is not invented where the concept does not split. The TOC simply lists whatever
the node actually has.

Naming: titles use spaces and full words and are used verbatim as link labels;
_key uses underscores and is used verbatim as the directory name, the url
segment, and the page_key in {PAGES_CSV}. Video page FILENAMES carry the Vid_
prefix so they are greppable and never collide with the images pipeline's Img_
pages.

============================
KNOWLEDGE — WHAT MAKES A GREAT CLUSTER PAGE
============================

The goal of a Level 2, Level 3, or Level 4 page is navigation. It exists to hand
the visitor the next click. Judge every one of these pages against this:

  * The table of contents is at the TOP, directly under the H1 and the back
    button. Nothing of substance sits above it. If a visitor has to scroll to
    find out what is below this page, the page has failed.
  * Every child in the YAML appears in the TOC. Nothing in the YAML is missing
    from the page, and nothing on the page is absent from the YAML.
  * Child clusters come first, bolded, each with its recursive video count. The
    node's own video pages follow. A visitor can tell at a glance which links
    go deeper and which end at a clip.
  * {TOC_COLUMNS} balanced columns.
  * Labels are the YAML titles — human, readable, no keys, no filenames, no
    bare X status ids. Video rows carry the speaker and the claim, and the
    duration where it is known.
  * A CLUSTER PAGE NEVER EMBEDS PLAYERS. It is a table of contents, and a page
    that autoloads six IPFS video players is slow, heavy, and unusable on a
    phone. Posters as small thumbnails beside the rows are fine; players are
    not. The player belongs on the Level 5 page and only there.
  * A short concept paragraph AFTER the TOC — one to three sentences saying what
    this cluster is about and why it matters in the investigation, grounded in
    {CK_FILE}. Not a wall of text. The prose supports the navigation; it does
    not replace it.
  * A cross-link out to the written section this cluster mirrors — the
    site_page / site_level_2 targets — so a visitor watching the footage can
    reach the argument, and vice versa.
  * Up-link to the parent page, and peer links to the other clusters at the same
    level under the same parent. No dead ends and no browser back button.
  * Every link resolves. Section overviews are linked as /X/overview, never a
    bare /X; every target is checked against {PAGES_CSV}.

The two arrival paths from the charter both have to work: the cold visitor
coming down from the left bar, and the visitor arriving from a topic page
elsewhere on the site who wants to WATCH the footage for that topic and lands in
the middle of the tree. The second one is why peer links and the up-link matter
as much as the child links.

============================
KNOWLEDGE — PER-LEVEL SPECIFICATION
============================

=== Level 2: {VIDEOS_L2_PAGE} ===

  * Keep the existing frontmatter and keep the existing prose. It is good prose
    about the role of video evidence — footage types (production/TPUSA,
    security, drone, eyewitness), uses for timeline and shooter-location
    analysis, claims about unreleased or deleted footage — and it stays.
  * The TOC section lives between the markers {/* VIDEOS_TOC_START */} and
    {/* VIDEOS_TOC_END */} and is fully regenerated every run. Everything
    outside the markers is untouched.
  * MOVE the markers if needed so the TOC sits directly under the H1, above the
    prose. The prose follows the map, not the other way around.
  * Contents: every level_3 node, in YAML order, as a link — title as label,
    /Videos/{L3_key}/overview as href, its number_of_videos_recursive shown.
    {TOC_COLUMNS} balanced columns.
  * The hand-written buckley-carlson-kash-patel-valhalla.mdx gets a row too, so
    it is not stranded, even though no YAML node generates it.
  * One line above the TOC saying how many clusters and how many videos the
    section holds in total, and how many of those are playable right now (a cid
    that the local node reports as pinned).

=== Level 3: {VIDEOS_L2_DIR}/{L3_key}/overview.mdx ===

  * Frontmatter: displayed_sidebar: docs, slug, title, sidebar_label,
    description, and ck_node_key set to the node's _key.
  * Back button to /Videos/overview.
  * H1 from the node title.
  * TOC immediately below: every level_4 child bolded with its recursive count,
    then every video page this node owns. {TOC_COLUMNS} columns.
  * Concept paragraph(s) after the TOC.
  * Cross-links to the mirrored written pages (site_page and each site_level_2).
  * Related Areas block: up-link to Videos, and every peer level_3.

=== Level 4: {VIDEOS_L2_DIR}/{L3_key}/{L4_key}/overview.mdx ===

  * Same shape one level down. Back button to the parent Level 3 page.
  * TOC: level_5 cluster children first if any, then this node's video pages.
  * Related Areas: up-link to the parent Level 3, peers being the other level_4
    nodes under the same parent.

=== Level 5: the video pages ===

Two halves, and the split is the whole point: the WORDS belong to
{VIDEO_PAGE_PROMPT}; the LAYOUT belongs here.

Reachability and naming:

  * Verify each one exists at {node dir}/Vid_{video_key}.mdx, that its title
    matches the label used in the parent's TOC, and that the link resolves.
  * If a video entry in the YAML has no page yet, create a minimal stub —
    frontmatter with ck_video_cid, ck_video_sha256 and ck_node_key, the player
    (or the media-pending note when there is no cid), a placeholder heading —
    and report it so {VIDEO_PAGE_PROMPT} can write it properly.
  * Never overwrite an existing video page's prose from this prompt.

Layout — every Level 5 page, every run, enforced from {GEN_SCRIPT}:

  * The page structure is fixed: frontmatter (hide_table_of_contents: true),
    back button, H1, then the player wrapper, then the prose wrapper holding the
    whole write-up.
  * Behaviour lives in the CSS block between the CK_VIDEO_LAYOUT markers in
    {CUSTOM_CSS}, which {GEN_SCRIPT} writes — not in per-page inline styles, so
    one edit moves every page. The class contract (ck-video-wrap,
    ck-video-media, ck-video-text), the source order, the bounding box and size
    calculation, the wrap behaviour, the player attributes, and everything else
    about how the video looks and lays out are specified in
    {LAYOUT_GUIDELINES}. Implement that file; do not invent layout here.
  * The player src is always a public IPFS gateway URL built from the entry's
    cid. Video bytes are NEVER copied into {SITE_DIR}/static. Posters are the
    only local media, under {POSTER_DIR}.
  * The generator needs the video's intrinsic dimensions to choose between the
    wrapped and full-width layouts. Read them with ffprobe from the local file
    under {VIDEOS_DIR} or the mirror. When there is no local file — a fresh
    clone, or a manifest-only entry — assume 16:9, note the assumption in a
    page comment, and report the entry so a later pass can correct it.
  * Verified on the BUILT output, not just the source: see Stage 5.

============================
KNOWLEDGE — RERUNS PRESERVE PROSE
============================

This prompt runs many times. Pages already exist and some of them carry writing
that cost far more to produce than the structure did, written against sources
this prompt never reads. A rerun refreshes structure and preserves prose.

  Regenerated every run: the frontmatter mechanical fields, the back button, the
  whole table of contents, the counts, the Related Areas block, the peer and
  child link lists, the column markup, and on Level 5 pages the player element
  with its src, poster, sources and attributes.

  Carried forward when present: the page title, sidebar_label, the frontmatter
  description, the authored paragraphs under "## About This Cluster", and on
  Level 5 pages everything under "## What This Video Shows" including any
  transcript quotes and timestamps placed by hand.

Baseline generator boilerplate IS replaced — the generator recognizes its own
output and refreshes it. Hand-written or enriched prose is not. A scrub applied
to a page for safe-writing reasons must survive every later regeneration.

Pages under {VIDEOS_L2_DIR} that the current YAML no longer accounts for are
orphans (a renamed key, a removed node). Remove them, count them, report them.
overview.mdx and buckley-carlson-kash-patel-valhalla.mdx are PROTECTED and are
never orphans.

============================
KNOWLEDGE — GATES THAT STILL APPLY
============================

  * THE BAN SET is the union of {BAN_VIDEOS_CSV} (the MASTER — one row per item:
    sha256, cid, file_path, banned, reason, date_added; match by sha256, then
    cid, then file_path; a row with banned=false is an explicit un-ban) and
    {EXCLUDE_FILE} (the older identifier-per-line list, still honoured). Read
    both before building any navigation.
    A banned video gets no Level 5 page, no TOC entry, no poster, no pin, and NO
    LINK INTO IT FROM ANYWHERE — no card, no poster thumbnail, no "see also", no
    bypass-target link. Any page or poster that exists is deleted. Counts on
    cluster pages reflect what is actually published, not the raw YAML count, and
    a node whose every video is banned publishes no page at all.
    The YAML carries a `banned:` boolean on every video entry, copied down from
    the CSV by {HIERARCHY_PROMPT} Stage 6B. Treat it as corroboration, never as
    the authority — re-check the two files here, every run, because the YAML is
    regenerated by a different prompt and a ban that survives only in
    regenerated data is not a ban. Report any disagreement; the files win.
    If a run finds material that should not be public — private personal
    documents, an unrelated third party's records, footage of bystanders with no
    connection to the investigation — add a row to {BAN_VIDEOS_CSV} with a
    reason and the date before the run ends, and note it in {FINDINGS_FILE}.
    IPFS publication is not reversible, so this gate is checked before a page is
    written, never after.
  * THE BYPASS RULE AND THE BAN INTERACT. A cluster node that resolves to
    exactly one video page is bypassed in navigation — parents and peers link
    straight to that video page. If that single video is banned, there IS no
    video page, so there is nothing to bypass to. Such a node is not published
    and does not appear in any TOC. Check the ban set BEFORE computing the
    bypass set, or the bypass computation mints links to pages that will never
    exist.
  * NOTHING IS EVER PINNED by this prompt. An entry with ipfs_pinned false
    publishes a page whose player no public gateway can serve. Render it, report
    it loudly, and leave the pinning decision to a separate approved job.
  * Safe writing, on every word this prompt emits: the word "defamation" never
    appears; never write that a person knew anything before the crime or did
    anything immoral or illegal; never state as fact that a living person
    committed a crime unless court-proven; use attribution language throughout.
    Where a cluster paragraph summarises what the footage in that cluster
    claims, attribute it to the speakers — "clips in which several witnesses
    describe ..." — never to the site. Within those limits, say as much as is
    useful; the rules constrain phrasing, not depth.
  * MDX comments must be {/* ... */}. An HTML <!-- --> comment fails the MDX
    compile and breaks the deploy.
  * A node flagged needs_split in the YAML exceeds the twelve-video ceiling.
    This prompt does not split it (the YAML is read-only here) — it renders what
    is there and reports the node so {HIERARCHY_PROMPT} can split it.
  * SHOULD_BE_ON_PAGES IS NOT THIS PROMPT'S PROPERTY. Every video entry carries
    should_be_on_pages: the list of topic pages OUTSIDE the videos hierarchy
    where that footage ought to appear. {HIERARCHY_PROMPT} Stage 13 reasons out
    those values; {VIDEO_PAGE_PROMPT} Stage 6 acts on them, placing a card for each
    video inside a marked CK_PLACED_VIDEOS block at the bottom of the topic
    page. This prompt does neither. It never reads should_be_on_pages to decide
    navigation, never places a video outside {VIDEOS_L2_DIR}, and never creates,
    edits, reorders, or removes a CK_PLACED_VIDEOS block — nor the images
    pipeline's CK_PLACED_IMAGES block, which lives on those same topic pages.
    If a run notices a stale or malformed placement block, REPORT it in
    {FINDINGS_FILE} for {VIDEO_PAGE_PROMPT} to regenerate; do not repair it here.
    The three properties, so nothing gets confused: video_page is which page IS
    the video, on_pages is where it IS shown today, should_be_on_pages is where
    it OUGHT to be shown. Navigation is built from the tree and from video_page
    alone.

============================
OUTPUT SANITIZATION — NO INVISIBLE UNICODE, EVER
============================

Every emitted file — every .mdx page and every {PAGES_CSV} row — must contain no
invisible Unicode: zero-width spaces, bidi controls, no-break spaces including
U+202F, word joiners, BOMs, control characters, variation selectors, tag
characters. They hide content from review and can smuggle instructions past a
human reading the file.

  * Prose: replace space-like invisibles with a regular space, delete
    zero-width / bidi / control characters, collapse whitespace. Visible
    non-ASCII (em dashes, accented letters) may stay.
  * Published pages reference media by CID and posters by sha256-derived names,
    so source filenames never reach a page.
  * Any label or duration string the generator lifts out of a transcription, an
    OCR sidecar, or {VIDEO_MANIFEST} is untrusted for this purpose — machine
    output over arbitrary audio routinely carries no-break spaces and stray
    control characters. Sanitize before emitting.

After every emit pass, rescan everything written and hard-fail if any code point
in the invisible set remains. The set is enumerated in {GEN_SCRIPT} and in
{HIERARCHY_PROMPT}.

============================
STAGE 1 — READ AND INDEX
============================

* Run the STALE-DATA PRECONDITION gate. Stop if it fails.
* Read the knowledge files in the order given above.
* Parse {HIERARCHY_FILE} into a node index: depth, parent, _key, title, site
  bindings, own and recursive video counts, video list.
* Inventory existing pages under {VIDEOS_L2_DIR}: for each, read ck_node_key /
  ck_video_cid / ck_video_sha256 from frontmatter and build the existing-page
  map. Mark the two protected pages.
* BUILD THE BAN SET. Read {BAN_VIDEOS_CSV} (python3 csv module — the reason
  column contains commas and quoted text; create it with the header row
  sha256,cid,file_path,banned,reason,date_added if missing) and {EXCLUDE_FILE}.
  The ban set is their union minus any CSV row explicitly marked banned=false.
  Index it by sha256, by cid, and by expanded file_path. Mark every banned video
  in the node index so Stage 2 computes the bypass set and every TOC against the
  publishable videos only. Cross-check against the YAML's `banned:` field and
  report any disagreement; the files win.
* Ask the local IPFS node which CIDs it pins, so the landing page can report
  how many videos are actually playable. Filter the ban set out of that question
  first — a banned video that is pinned is a finding for {FINDINGS_FILE} and a
  worklist item for an approved unpinning job, never a "playable" count.

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

* For every cluster node, compute what its TOC SHOULD be from the YAML, and
  compare it to what the page currently has: missing children, stale labels,
  wrong counts, broken links, wrong column count, TOC below the prose, bare
  status-id labels, players embedded on a cluster page.
* Resolve every intended link target against {PAGES_CSV} and the docs tree.
  Anything unresolvable is listed, not silently emitted.
* List the pages that need rewriting, the orphans to remove, the video stubs to
  create.

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

Prefer the generator. Structural rules live in {GEN_SCRIPT}; change the rule
there, rerun it, and every page moves together. Hand-editing individual pages is
for one-off fixes only.

If {GEN_SCRIPT} does not exist yet, write it. Start from
{IMAGE_PLANNING_DIR}/generator/gen_photos_pages.py as prior art — it solves the
same structural problem for stills — but write a NEW file under
{GENERATOR_DIR}. Never edit the images generator, and never let the video
generator write the CK_EVIDENCE_LAYOUT block, the Photos tree, or
static/img/evidence.

* Update {GEN_SCRIPT} for any rule this prompt changed — {TOC_COLUMNS} columns,
  TOC above the prose, counts, human labels with durations, cross-links, prose
  preservation, no players on cluster pages.
* Update {GEN_SCRIPT}'s video-page markup and its CK_VIDEO_LAYOUT CSS block
  for every point in {LAYOUT_GUIDELINES} that the current output does not
  already satisfy. Layout defects are fixed here, at the template, and nowhere
  else.
* Run it over the whole tree.
* Where prose-level judgment is needed on many clusters at once — writing the
  concept paragraph for a cluster that has none, or reconciling a label against
  {CK_FILE} — partition the level_3 subtrees across up to {MAX_AGENTS} parallel
  agents. A subtree never splits across two agents. Give each agent its own
  scratch subdirectory; agents independently invent the same helper filenames
  and in a parallel run those collide.
* Shared files ({PAGES_CSV}, {VIDEOS_L2_PAGE}) are written by the orchestrator
  only.

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

* Merge rows for every cluster page created, rewritten, retitled, or removed,
  per the CSV schema in {ROOT_DIR}/claude.md: page_key = the node's _key,
  parent_key = the parent node's _key, level = the node's level, url_path,
  file_path, title, sidebar_label, directory, extension, has_frontmatter,
  line_count.
* Never delete rows for pages that still exist; flag rows whose files vanished
  instead of removing them blindly.

Output to stdout:
============================
STAGE 4 COMPLETE
pages.csv: N rows added, N updated, N flagged
============================

============================
STAGE 5 — BUILD AND VERIFY
============================

* Run {VERIFY_SCRIPT} over the whole corpus.
* Build the site: cd {SITE_DIR} && npm run build. It must pass. Broken links and
  MDX compile errors surface here — fix and rebuild until green.
* Walk the tree by hand from {VIDEOS_L2_PAGE}: pick three level_3 nodes at
  random and click down to a video page at the bottom of each. Every step must
  present the next level's links at the top of the page.
* Spot-check five Level 3 and five Level 4 pages: TOC at the top, all YAML
  children present, {TOC_COLUMNS} columns, counts match the YAML, human labels
  with no bare status ids, no players embedded, up-link and peer links present
  and resolving, cross-link to the mirrored written page present.
* LAYOUT CHECK on the Level 5 pages: run the verification section of
  {LAYOUT_GUIDELINES} in full — the grep checks against the built CSS bundle and
  the generated pages, then the browser eyeball checks it lists, in a clean
  profile with no IPFS Companion extension. Every point must pass before the run
  is declared complete.
* PLAYBACK CHECK: press play on five video pages across different clusters, in
  that same clean profile. Each must load and play with audio. A page that plays
  for you with Companion running and is dead for visitors is the default failure
  of this pipeline, not an edge case.
* Confirm the CK_EVIDENCE_LAYOUT block in {CUSTOM_CSS} is byte-identical to
  what it was before the run, and that {DOCS_DIR}/Photos and
  {SITE_DIR}/static/img/evidence are untouched.
* Run the invisible-Unicode scan over everything written.
* Confirm nothing outside {VIDEOS_L2_DIR}, {POSTER_DIR}, {PAGES_CSV}, and the
  marked CSS block changed, and that {HIERARCHY_FILE} and
  {SITE_DIR}/sidebars.ts are untouched.

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

* The STALE-DATA PRECONDITION gate runs before anything else and is a hard
  stop. Never generate pages from unconverted image data.
* {LAYOUT_GUIDELINES} is read at the very start of every run, before anything
  else, and overrides this prompt where they conflict. Never edit it from this
  prompt. Every point in it is a shipped defect to be fixed, and the run is not
  complete until each one is verified fixed on the built output.
* Level 5 video page LAYOUT is this prompt's responsibility; Level 5 PROSE is
  {VIDEO_PAGE_PROMPT}'s. Layout is fixed in {GEN_SCRIPT} and the marked
  CK_VIDEO_LAYOUT block in {CUSTOM_CSS}, then regenerated across every page —
  never by hand-editing individual video pages.
* CK_VIDEO_LAYOUT is ours; CK_EVIDENCE_LAYOUT belongs to the images pipeline and
  is never touched. Nothing under {IMAGE_PLANNING_DIR}, {ROOT_DIR}/images,
  {DOCS_DIR}/Photos, or {SITE_DIR}/static/img/evidence is ever written.
* This prompt writes ONLY inside {VIDEOS_L2_DIR} (plus {PAGES_CSV}, {GEN_SCRIPT}
  and our marked CSS region). It never edits a topic page elsewhere in
  {DOCS_DIR}. The should_be_on_pages placements on those pages — the marked
  CK_PLACED_VIDEOS blocks — belong to {VIDEO_PAGE_PROMPT} Stage 6, and the
  CK_PLACED_IMAGES blocks beside them belong to the images pipeline. Report a
  broken block in {FINDINGS_FILE}; never repair one from here.
* NEVER copy video bytes into {SITE_DIR}/static. The player's src is a public
  IPFS gateway URL built from the entry's cid. Posters are the only local media.
* Nothing is ever PINNED by this prompt. Unpinned CIDs are rendered and
  reported, not fixed.
* Cluster pages carry no players. A table of contents that autoloads six video
  streams is not a table of contents.
* Every point in {LAYOUT_GUIDELINES} — placement, opacity, text wrap, the
  bounding box and its size calculation, square corners, no autoplay, no loop,
  preload metadata, reachable controls — is satisfied on the built output. That
  file specifies the layout; this prompt only enforces it.
* {HIERARCHY_FILE} is the source of truth and is READ-ONLY here. Discrepancies
  go in {FINDINGS_FILE}, never into the YAML from this prompt.
* Every Level 2, Level 3, and Level 4 page leads with its table of contents,
  directly under the H1. Prose comes after the map.
* Every child node in the YAML has a hyperlinked bullet on its parent's page,
  labeled with the child's title. Every video a node owns has a link on that
  node's page, labeled with a human label and never a bare status id. Nothing in
  the YAML is unreachable from the tree.
* {TOC_COLUMNS} balanced columns, modeled on {HOME_PAGE}.
* Every page carries an up-link, peer links, and — where the node has a
  site_page or site_level_2 — a cross-link to the written section it mirrors.
  Overviews are linked /X/overview, never bare /X.
* Reruns refresh structure and preserve authored prose. Orphans are removed,
  counted, and reported. overview.mdx and
  buckley-carlson-kash-patel-valhalla.mdx are protected and are never orphans.
* Video page bodies belong to {VIDEO_PAGE_PROMPT}. This prompt may create a stub
  so a link resolves; it never rewrites an existing video page's write-up.
* Nothing in {EXCLUDE_FILE} is ever linked or published.
* No claims of prior knowledge or of immoral or illegal conduct by any person;
  claims made in the footage are attributed to the speaker; attribution language
  throughout; the word "defamation" never appears.
* No invisible Unicode in any emitted file — scan after every emit, and treat
  transcription, OCR, and manifest text as untrusted input for that purpose.
* {SITE_DIR}/sidebars.ts is never modified.
* The build must pass, and the clean-profile playback check must pass, before
  the run is declared complete.

============================
BACKGROUND — ORIGINAL DIRECTIVE, KNOWLEDGE PRESERVED
============================

This section preserves the intent this prompt was narrowed to, so nothing is
lost even where a stage above already encodes it.

* Focus this on the levels. Right now we are in a Level 2 for videos.
* The home page is very good because it has a table of contents. Ours are okay
  to be only two columns instead of three, but the focus of the Level 2 page,
  the Level 3 page, and the Level 4 page is that at the top of it is a table of
  contents.
* {HIERARCHY_FILE} is the YAML file. It has sections such as, when there is a
  level_3 in it:

      # site_level_2 = site docs dirs this cluster covers;
      # site_page = the page a node mirrors.
      level_3:
        - level_3:
            title: "The Exploding Microphone Thesis"
            _key: Mic_Thesis
            site_level_2: ["Mic"]
            site_page: "site/docs/Mic/overview.mdx"
            number_of_videos: 6

* Our Level 2 page in this directory for videos, the Level 3 pages in this
  videos Level 2, and the Level 4 pages in this videos Level 2 — this prompt is
  about the shape of those pages, the criteria for those pages, what makes them
  great, and what their goal is. The goal of this prompt is to update those
  pages.
* The output is nearly exclusively the files in the videos Level 2 directory.
* The individual videos are the Level 5 pages in this directory. We update the
  Level 2, Level 3, and Level 4 pages to make sure their tables of contents go
  to the next level down. That is what lets people navigate through and get into
  the individual videos at the end, which are the Level 5 pages.
* The source of the data of what is correct is the YAML file, and that is also
  the hierarchy we want. Primarily we read from the YAML file and almost never —
  probably never — update the YAML file from this prompt.
* With the YAML above, that means we update the Level 2 page and make sure the
  table of contents goes off to the Mic-appropriate Level 3 page in the same
  directory.
* When we see a level_4 in the YAML file, that means we take that level_3 page,
  which is its parent, and make sure there is a bullet point that hyperlinks to
  that level_4 page by that name, using the title YAML property for the name in
  the user interface:

      level_4:
        - level_4:
            title: "Shaped Charge Counterarguments"
            _key: Mic_Shaped_Charge
            number_of_videos: 8
            number_of_videos_recursive: 8

* The level_5 should go to a page for the site that is dedicated to one video,
  and it will have the write-up around that video:

      level_5:
        - level_5:
            title: "Buckley Carlson on the Valhalla Comment"
            _key: Videos_Buckley_Kash
            site_page: "site/docs/Videos/buckley-carlson-kash-patel-valhalla.mdx"

* In some cases some video files get links into them straight from a Level 3
  page or straight from the Level 4, and they may not need a Level 4 in between.
* This prompt might have done other things before. It is now focused on
  improving these hierarchy pages: reading from the YAML file and updating the
  Level 2, Level 3, and Level 4 pages underneath the directory that is the
  videos Level 2.
* This file was converted from the images navigation prompt on 2026-07-23. The
  differences that matter and were NOT in the images version: the CSS block is
  CK_VIDEO_LAYOUT and must never collide with the images pipeline's
  CK_EVIDENCE_LAYOUT in the same file; cluster pages carry no players; TOC rows
  need human labels and durations because this corpus names its files by X
  status id; the player is fed from a public IPFS gateway and video bytes are
  never copied into the site; and the two hand-written pages already under
  {VIDEOS_L2_DIR} are protected.
