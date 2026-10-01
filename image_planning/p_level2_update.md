ROOT_DIR dir is ~/BGit/Bryan_git/charlie-kirk

THIS_DIR dir is {ROOT_DIR}/image_planning
IMAGES_DIR dir is {ROOT_DIR}/images
HIERARCHY_FILE is file {IMAGES_DIR}/images.yaml
  Moved 2026-07-22. It used to be {THIS_DIR}/hierarchy_images.yaml. That old
  name and that old location are both gone — the file is now images.yaml and it
  lives in {IMAGES_DIR}, not in {THIS_DIR}.
LAYOUT_GUIDELINES is file {THIS_DIR}/layout_guidelines.txt
CHARTER_FILE is file {THIS_DIR}/CLAUDE.md
EXCLUDE_FILE is file {THIS_DIR}/exclude_images.txt
BAN_IMAGES_CSV is file {IMAGES_DIR}/ban_images.csv
FINDINGS_FILE is file {THIS_DIR}/findings_for_hierarchy.md
IMAGE_PAGE_PROMPT is file {THIS_DIR}/p_yaml_to_site.md
HIERARCHY_PROMPT is file {THIS_DIR}/p_update_image_hierarchy.md

GENERATOR_DIR dir is {THIS_DIR}/generator
GEN_SCRIPT is file {GENERATOR_DIR}/gen_photos_pages.py
VERIFY_SCRIPT is file {GENERATOR_DIR}/verify_photos.py

SITE_DIR dir is {ROOT_DIR}/site
DOCS_DIR dir is {SITE_DIR}/docs
PHOTOS_DIR dir is {DOCS_DIR}/Photos
CUSTOM_CSS is file {SITE_DIR}/internals/src/css/custom.css

The SIBLING VIDEO PIPELINE — read-only from here, never written by this prompt:
VIDEO_PLANNING_DIR dir is {ROOT_DIR}/videos_planning
VIDEOS_DIR dir is {ROOT_DIR}/videos
VIDEO_HIERARCHY_FILE is file {VIDEOS_DIR}/videos.yaml
VIDEOS_L2_DIR dir is {DOCS_DIR}/Videos

IMAGES_L2_PAGE is file {PHOTOS_DIR}/overview.mdx
HOME_PAGE is file {DOCS_DIR}/index.mdx
PAGES_CSV is file {ROOT_DIR}/pages.csv
CK_FILE is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt
  (Real file. Moved 2026-09-19. ~/BGit/Bryan_git/charlie-kirk/Charlie_Kirk.txt is now a symlink to it —
   use that only to verify the location; always read and write the real path.)
ASSESS_MANUAL is file {ROOT_DIR}/prompts/Assess_Manual.md

TOC_COLUMNS is ... = 2
MAX_AGENTS is ... = 12

============================
GOAL
============================

Update the NAVIGATION pages of the images Level 2 section — the Level 2 landing
page ({IMAGES_L2_PAGE}), every Level 3 page, and every Level 4 page under
{PHOTOS_DIR} — so that each one leads with a table of contents that carries the
visitor to the next level down, and so that a visitor can walk from the left bar
all the way to an individual image page without ever dead-ending.

{HIERARCHY_FILE} is the source of truth for what is correct: what the clusters
are, what they are called, how they nest, and which images belong to each. This
prompt READS that YAML and WRITES pages. It primarily — almost certainly always
— does not write back into the YAML.

The end of the walk is the individual image page: one image, one write-up. Those
leaf pages are spoken of as Level 5 — the last click. This prompt does not
author their bodies; {IMAGE_PAGE_PROMPT} owns the WORDS. This prompt guarantees
that every one of them is reachable, correctly named, exactly one click from the
cluster page that owns it, and correctly LAID OUT.

Level 5 layout is this prompt's job. {LAYOUT_GUIDELINES} states how an image
must sit on its page, and every Level 5 page must satisfy it. Layout is a
templating concern, not a per-page concern: it is fixed by changing the markup
{GEN_SCRIPT} emits and the CSS block {GEN_SCRIPT} writes into {CUSTOM_CSS}, then
rerunning over all ~1,850 pages. Never fix layout by hand-editing image pages.

============================
SCOPE — WHAT THIS PROMPT TOUCHES
============================

Writes:

  * {IMAGES_L2_PAGE} — the marked TOC section only; its prose is left alone.
  * {PHOTOS_DIR}/{L3_key}/overview.mdx — every Level 3 cluster page.
  * {PHOTOS_DIR}/{L3_key}/{L4_key}/overview.mdx — every Level 4 cluster page.
  * Deeper cluster overview.mdx pages (Level 5 cluster nodes, where the YAML
    nests that far) — same treatment, same rules.
  * The LAYOUT of every Level 5 image page — the image element, its wrapper,
    the prose wrapper, and any inline style on them. The prose between those
    wrappers is not touched.
  * {CUSTOM_CSS} — the marked block between /* CK_EVIDENCE_LAYOUT_START */ and
    /* CK_EVIDENCE_LAYOUT_END */ only. Everything outside those markers in that
    file belongs to the rest of the site and is never touched.
  * {PAGES_CSV} rows for the pages above.
  * {GEN_SCRIPT} — the generator is the implementation of the rules below. There
    are roughly 1,850 pages under {PHOTOS_DIR}; structural and layout rules are
    changed by editing the generator and rerunning it, never by hand-editing
    pages one at a time.

Does NOT write:

  * {HIERARCHY_FILE} — read-only input. If the YAML is wrong, record it in
    {FINDINGS_FILE} and leave the YAML for the hierarchy prompt to fix.
  * Image page PROSE (the write-up inside the Img_*.mdx leaf pages) — owned by
    {IMAGE_PAGE_PROMPT}. This prompt may create a missing leaf page as a stub
    so the TOC link resolves, and reports it, but does not rewrite an existing
    one's prose. Their LAYOUT is a different matter and is this prompt's job —
    see GOAL and the Level 5 spec below.
  * {SITE_DIR}/sidebars.ts — never, unless explicitly asked.
  * {VIDEOS_L2_DIR}, {VIDEOS_DIR}, {VIDEO_HIERARCHY_FILE}, or
    {VIDEO_PLANNING_DIR} — the sibling video pipeline owns all four. Read them
    freely; write none of them. The /Videos Level 2 has its own navigation
    prompt, its own generator, and its own TOC markers, and a run of this
    prompt that edits a page over there destroys that work.
  * Anything outside {PHOTOS_DIR} other than {PAGES_CSV} rows.

============================
KNOWLEDGE — MEDIA-TYPE SCOPE: THE LEVEL 5 LAYOUT IS AN IMAGE LAYOUT
============================

This is the images Level 2. Every page it navigates to hosts a STILL IMAGE.
Video has its own Level 2 with a parallel structure and a different layout,
because the two media need different markup:

  images                                videos
  ------                                ------
  {PHOTOS_DIR}                          {VIDEOS_L2_DIR}
  {HIERARCHY_FILE}                      {VIDEO_HIERARCHY_FILE}
  {GEN_SCRIPT}                          gen_videos_pages.py
  Img_*.mdx leaf pages                  Vid_*.mdx leaf pages
  CK_EVIDENCE_LAYOUT css block          CK_VIDEO_LAYOUT css block
  ck-evidence-* classes                 ck-video-* classes
  <img> served from static/img/evidence <video> off a public IPFS gateway

Both generators write into the same {CUSTOM_CSS}, so each owns its OWN marked
block and touches nothing outside it. {GEN_SCRIPT} owns CK_EVIDENCE_LAYOUT and
must never write CK_VIDEO_LAYOUT — doing so silently destroys the video layout,
and the next video run destroys the image layout back.

THE GENERATOR MUST NOT BE ABLE TO RENDER A VIDEO. {GEN_SCRIPT} today contains a
code path that does: a `classify_ipfs_cids()` helper that decides whether a CID
is a video, an `is_video_src()` test, and a branch that emits

    <div className="ck-evidence-image-wrap ck-evidence-wide">
      <video className="ck-evidence-image" controls preload="metadata">
        <source src="https://ipfs.io/ipfs/<CID>" type="video/mp4" />

into an `Img_*.mdx` page under {PHOTOS_DIR}. That branch is why nine video
pages are published in the image hierarchy today, all under
{PHOTOS_DIR}/Official_Narrative/Narrative_Shot_in_the_Heart/, each headed "What
This Image Shows" and each carrying `ck_image_cid: none` because a video entry
has no sha256 to stamp.

The fix is inversion, not deletion, of the type test. The classifier stays —
knowing which CIDs are videos is exactly what is needed — but its result is
used to SKIP the entry instead of to choose different markup:

  * An entry that types as video is skipped: no leaf page, no {PAGES_CSV} row,
    no TOC link on its parent cluster page, and it does not count toward the
    parent's recursive image count. It is counted and reported.
  * An entry whose type cannot be settled is UNKNOWN and is also skipped. All
    9 known bad entries are extensionless IPFS CIDs with an empty sha256;
    assuming that shape is an image is what published them.
  * {GEN_SCRIPT} retains no branch capable of emitting `<video>`, `<source>`,
    `<audio>`, or a media-player `<iframe>`. A generator that CAN render a
    video will render one the next time a mistyped entry reaches it.
  * {VIDEOS_DIR}/manifest.yaml and {ROOT_DIR}/IPFS/ipfs.txt are the best oracle
    for whether a CID is a video, but BOTH must be parsed by filename — they
    describe a mixed corpus, and scraping their CIDs wholesale types 70 image
    entries as video when only 9 are (measured 2026-07-23). Do not use
    {VIDEO_HIERARCHY_FILE} yet: it is still a schema shell whose cids describe
    the inherited image corpus. Fall back to how the CID is embedded elsewhere
    on the site.

THE NINE EXISTING PAGES ARE NOT ORPHANS. Once their entries are skipped, the
orphan sweep will see nine leaf pages under {PHOTOS_DIR} with no backing entry
and try to remove them. It must not. They are written, published pages with
inbound links and no replacement under {VIDEOS_L2_DIR} yet. Treat any page
under {PHOTOS_DIR} containing a `<video>` or `<source>` element as PROTECTED:
leave it byte-identical, exclude it from orphan removal, list its path in
{FINDINGS_FILE}, and report the count. Migrating them to {VIDEOS_L2_DIR} and
then withdrawing them from {PHOTOS_DIR} is a separate, explicitly-approved job,
sequenced so the /Videos pages exist before the /Photos ones go away.

============================
KNOWLEDGE — READ FIRST, IN THIS ORDER
============================

At the very start of every run — before reading anything else, before touching
any file — read into the context window:

  1. {LAYOUT_GUIDELINES} — the standards file for images pages. THIS IS READ
     FIRST, EVERY RUN, WITHOUT EXCEPTION. It is short. It is also the most
     load-bearing file in this prompt, because everything in it was put there
     after a real, visible defect shipped to the live site. Read it in full,
     restate each of its points before doing any work, and treat every point as
     a defect that must be verified fixed by the end of the run — not as advice.
     Its rules OVERRIDE any conflicting rule in this prompt; where this prompt
     and that file disagree, that file is right and this prompt is stale and
     should be corrected to match.

     Its points today concern Level 5 image pages. It carries the whole layout
     specification — how the image sits on the page, the bounding box and how
     the image's size is calculated inside it, what the CSS block must do, and
     the verification checklist to run against the built output. This prompt
     does not restate any of that; read it there and implement it exactly.

     Every point in it, and any point added to it later, gets the same
     treatment: implement it in {GEN_SCRIPT} and in the {CUSTOM_CSS} marked
     block, rerun over every page, and verify it on the built output.

  2. {CHARTER_FILE} — the image_planning charter: the audience model, the level
     model, the YAML schema, the hard rules.
  3. {HOME_PAGE} — the site home page. Read it for the TOC pattern to imitate
     (see THE MODEL below). It is the reference for what a good landing page
     looks like on this site.
  4. {HIERARCHY_FILE} — parse fully. Index every node (_key, title, depth,
     parent, site_level_2, site_page, number_of_images,
     number_of_images_recursive) and every image (sha256, file_path).
  5. {PAGES_CSV} — the master page index, for resolving link targets and for
     keeping in sync afterward.
  6. {ASSESS_MANUAL} — the site-wide writing and layout guide.
  7. {CK_FILE} — the master investigation file, for the one or two sentences of
     concept prose each cluster page carries. Load the section headers plus the
     sections relevant to the clusters being processed. This prompt writes far
     less prose than {IMAGE_PAGE_PROMPT} does, so a full read is not required —
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

Our images pages copy that shape with one difference: {TOC_COLUMNS} columns
instead of the home page's three. Two columns read better at the narrower main
area these pages have, and they stay readable on a laptop. Existing generated
pages use a three-column grid; move them to {TOC_COLUMNS}.

Column markup follows the home page's own idiom:

  <div style={{ display: "flex", justifyContent: "space-between", gap: "2rem" }}>
  <div style={{ flex: 1 }}>
    * [Label](/Photos/.../overview)
  </div>
  <div style={{ flex: 1 }}>
    * [Label](/Photos/.../Img_key)
  </div>
  </div>

Split the list across the columns in reading order, balanced by count, child
clusters before image pages.

============================
KNOWLEDGE — THE LEVEL MODEL AND THE YAML MAPPING
============================

Site levels:

  Level 1  {DOCS_DIR}/index.mdx — the site home.
  Level 2  {IMAGES_L2_PAGE} — the images landing page, url /Photos, left-bar
           label "Photos". One page. This is where a cold visitor arrives.
  Level 3  one page per level_3 node in {HIERARCHY_FILE}.
  Level 4  one page per level_4 node.
  Level 5  the individual image pages — one image, one write-up. Where the YAML
           nests a level_5 CLUSTER node, that node also becomes a cluster page
           and follows the cluster rules; its images are its leaves.

The YAML shape and what each field becomes on the page:

  level_3:
    - level_3:
        title: "FBI"                          -> the H1 and the link label
        _key: FBI                             -> the directory name and url
                                                 segment: /Photos/FBI/overview
        site_level_2: ["FBI"]                 -> the site docs dirs this cluster
                                                 covers; cross-link targets
        site_page: "site/docs/FBI/overview.mdx"
                                              -> the written page this cluster
                                                 mirrors; link it as /FBI/overview
        number_of_images: 14                  -> images owned directly by this
                                                 page (its own leaf pages)
        number_of_images_recursive: 24        -> the count shown on the PARENT's
                                                 TOC line for this node

A level_4 nested under a level_3 means exactly this: the Level 3 page carries a
bullet that hyperlinks to that Level 4 page, labeled with the level_4 node's
title.

        level_4:
          - level_4:
              title: "TallyHallAlbum"
              _key: TallyHallAlbum
              number_of_images: 1
              number_of_images_recursive: 1
              images:
                - image: ...

  -> on {PHOTOS_DIR}/FBI/overview.mdx:
       * **[TallyHallAlbum](/Photos/FBI/TallyHallAlbum/overview)** — 1 image

A level_5 node nested under a level_4 works the same way one level further down,
and where it carries a site_page it also cross-links to the written page it
mirrors:

        level_5:
          - level_5:
              title: "Baker Tilly — TPUSA's Auditor (Claims)"
              _key: TPUSA_CO_BakerTilly
              site_page: "site/docs/TPUSA/Companies/baker-tilly.mdx"

A node may own images with no child clusters at all. That is normal and correct:
some image pages hang directly off a Level 3, some off a Level 4, and a Level 4
is not invented where the concept does not split. The TOC simply lists whatever
the node actually has.

Naming: titles use spaces and full words and are used verbatim as link labels;
_key uses underscores and is used verbatim as the directory name, the url
segment, and the page_key in {PAGES_CSV}.

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
  * Child clusters come first, bolded, each with its recursive image count. The
    node's own image pages follow. A visitor can tell at a glance which links
    go deeper and which end at a picture.
  * {TOC_COLUMNS} balanced columns.
  * Labels are the YAML titles — human, readable, no keys, no filenames.
  * A short concept paragraph AFTER the TOC — one to three sentences saying what
    this cluster is about and why it matters in the investigation, grounded in
    {CK_FILE}. Not a wall of text. The prose supports the navigation; it does
    not replace it.
  * A cross-link out to the written section this cluster mirrors — the
    site_page / site_level_2 targets — so a visitor looking at the pictures can
    reach the argument, and vice versa.
  * Up-link to the parent page, and peer links to the other clusters at the same
    level under the same parent. No dead ends and no browser back button.
  * Every link resolves. Section overviews are linked as /X/overview, never a
    bare /X; every target is checked against {PAGES_CSV}.

The two arrival paths from the charter both have to work: the cold visitor
coming down from the left bar, and the visitor arriving from a topic page
elsewhere on the site who wants to SEE the evidence for that topic and lands in
the middle of the tree. The second one is why peer links and the up-link matter
as much as the child links.

============================
KNOWLEDGE — PER-LEVEL SPECIFICATION
============================

=== Level 2: {IMAGES_L2_PAGE} ===

  * Keep the existing frontmatter and keep the existing prose. It is good prose
    about the role of photographic evidence and it stays.
  * The TOC section lives between the markers {/* PHOTOS_TOC_START */} and
    {/* PHOTOS_TOC_END */} and is fully regenerated every run. Everything
    outside the markers is untouched.
  * MOVE the markers if needed so the TOC sits directly under the H1, above the
    prose. The prose follows the map, not the other way around.
  * Contents: every level_3 node, in YAML order, as a link — title as label,
    /Photos/{L3_key}/overview as href, its number_of_images_recursive shown.
    {TOC_COLUMNS} balanced columns.
  * One line above the TOC saying how many clusters and how many images the
    section holds in total.

=== Level 3: {PHOTOS_DIR}/{L3_key}/overview.mdx ===

  * Frontmatter: displayed_sidebar: docs, slug, title, sidebar_label,
    description, and ck_node_key set to the node's _key.
  * Back button to /Photos/overview.
  * H1 from the node title.
  * TOC immediately below: every level_4 child bolded with its recursive count,
    then every image page this node owns. {TOC_COLUMNS} columns.
  * Concept paragraph(s) after the TOC.
  * Cross-links to the mirrored written pages (site_page and each site_level_2).
  * Related Areas block: up-link to Photos, and every peer level_3.

=== Level 4: {PHOTOS_DIR}/{L3_key}/{L4_key}/overview.mdx ===

  * Same shape one level down. Back button to the parent Level 3 page.
  * TOC: level_5 cluster children first if any, then this node's image pages.
  * Related Areas: up-link to the parent Level 3, peers being the other level_4
    nodes under the same parent.

=== Level 5: the image pages ===

Two halves, and the split is the whole point: the WORDS belong to
{IMAGE_PAGE_PROMPT}; the LAYOUT belongs here.

Reachability and naming:

  * Verify each one exists at {node dir}/{Img_key}.mdx, that its title matches
    the label used in the parent's TOC, and that the link resolves.
  * If an image entry in the YAML has no page yet, create a minimal stub —
    frontmatter with ck_image_sha256 and ck_node_key, the image, a placeholder
    heading — and report it so {IMAGE_PAGE_PROMPT} can write it properly.
  * Never overwrite an existing image page's prose from this prompt.

Layout — every Level 5 page, every run, enforced from {GEN_SCRIPT}:

  * The page structure is fixed: frontmatter (hide_table_of_contents: true),
    back button, H1, then the image wrapper, then the prose wrapper holding the
    whole write-up.
  * Behaviour lives in the CSS block between the CK_EVIDENCE_LAYOUT markers in
    {CUSTOM_CSS}, which {GEN_SCRIPT} writes — not in per-page inline styles, so
    one edit moves all ~1,850 pages. The class contract, the source order, the
    bounding box and size calculation, the wrap behaviour, and everything else
    about how the image looks and lays out are specified in
    {LAYOUT_GUIDELINES}. Implement that file; do not invent layout here.
  * Verified on the BUILT output, not just the source: see Stage 5.

============================
KNOWLEDGE — RERUNS PRESERVE PROSE
============================

This prompt runs many times. Pages already exist and some of them carry writing
that cost far more to produce than the structure did, written against sources
this prompt never reads. A rerun refreshes structure and preserves prose.

  Regenerated every run: the frontmatter mechanical fields, the back button, the
  whole table of contents, the counts, the Related Areas block, the peer and
  child link lists, the column markup.

  Carried forward when present: the page title, sidebar_label, the frontmatter
  description, and the authored paragraphs under "## About This Cluster".

Baseline generator boilerplate IS replaced — the generator recognizes its own
output and refreshes it. Hand-written or enriched prose is not. A scrub applied
to a page for safe-writing reasons must survive every later regeneration.

Pages under {PHOTOS_DIR} that the current YAML no longer accounts for are
orphans (a renamed key, a removed node). Remove them, count them, report them.

============================
KNOWLEDGE — GATES THAT STILL APPLY
============================

  * THE BAN SET is the union of {BAN_IMAGES_CSV} (the MASTER — one row per item:
    sha256, cid, file_path, banned, reason, date_added; match by sha256, then
    cid, then file_path; a row with banned=false is an explicit un-ban) and
    {EXCLUDE_FILE} (the older sha256-per-line list, still honoured). Read both
    before building any navigation.
    A banned image gets no Level 5 page, no TOC entry, no static copy, and NO
    LINK INTO IT FROM ANYWHERE — no thumbnail, no card, no "see also", no
    bypass-target link. Any page or static copy that exists is deleted. Counts on
    cluster pages reflect what is actually published, not the raw YAML count, and
    a node whose every image is banned publishes no page at all.
    The YAML carries a `banned:` boolean on every image entry, copied down from
    the CSV by {HIERARCHY_PROMPT}. Treat it as corroboration, never as the
    authority — re-check the two files here, every run, because the YAML is
    regenerated by a different prompt and a ban that survives only in
    regenerated data is not a ban. Report any disagreement; the files win.
    If a run finds material that should not be public — private personal
    documents, an unrelated third party's records, an accusation burned into the
    image — add a row to {BAN_IMAGES_CSV} with a reason and the date before the
    run ends, and note it in {FINDINGS_FILE}.
  * THE BYPASS RULE AND THE BAN INTERACT. A cluster node that resolves to
    exactly one image page is bypassed in navigation — parents and peers link
    straight to that image page. If that single image is banned, there IS no
    image page, so there is nothing to bypass to. Such a node is not published
    and does not appear in any TOC. Check the ban set BEFORE computing the
    bypass set, or the bypass computation mints links to pages that will never
    exist.
  * Safe writing, on every word this prompt emits: the word "defamation" never
    appears; never write that a person knew anything before the crime or did
    anything immoral or illegal; never state as fact that a living person
    committed a crime unless court-proven; use attribution language throughout.
    Within those limits, say as much as is useful — the rules constrain
    phrasing, not depth.
  * MDX comments must be {/* ... */}. An HTML <!-- --> comment fails the MDX
    compile and breaks the deploy.
  * A node flagged needs_split in the YAML exceeds the twelve-image ceiling.
    This prompt does not split it (the YAML is read-only here) — it renders what
    is there and reports the node so the hierarchy pass can split it.

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
  * Published pages never contain mirror filenames — served copies are
    sha256-named — so the macOS screenshot U+202F problem never reaches a page.

After every emit pass, rescan everything written and hard-fail if any code point
in the invisible set remains. The set is enumerated in {GEN_SCRIPT} and in
{THIS_DIR}/p_create_image_hierarchy.md.

============================
STAGE 1 — READ AND INDEX
============================

* Read the knowledge files in the order given above.
* Parse {HIERARCHY_FILE} into a node index: depth, parent, _key, title, site
  bindings, own and recursive image counts, image list.
* Inventory existing pages under {PHOTOS_DIR}: for each, read ck_node_key /
  ck_image_sha256 from frontmatter and build the existing-page map.
* BUILD THE BAN SET. Read {BAN_IMAGES_CSV} (python3 csv module — the reason
  column contains commas and quoted text; create it with the header row
  sha256,cid,file_path,banned,reason,date_added if missing) and {EXCLUDE_FILE}.
  The ban set is their union minus any CSV row explicitly marked banned=false.
  Index it by sha256, by cid, and by expanded file_path. Mark every banned image
  in the node index so Stage 2 computes the bypass set and every TOC against the
  publishable images only. Cross-check against the YAML's `banned:` field and
  report any disagreement; the files win.

Output to stdout:
============================
STAGE 1 COMPLETE
Layout guideline lines: N
YAML: N level_3 / N level_4 / N level_5 clusters, N unique images
Existing pages: N cluster / N image
Ban set: N identities ({BAN_IMAGES_CSV} N rows, {EXCLUDE_FILE} N lines, N un-bans)
YAML banned: disagreeing with the files: N (listed — the files win)
Nodes with no publishable image left after the ban: N (not published, no TOC entry)
============================

============================
STAGE 2 — DECIDE THE STRUCTURAL DIFF
============================

* For every cluster node, compute what its TOC SHOULD be from the YAML, and
  compare it to what the page currently has: missing children, stale labels,
  wrong counts, broken links, wrong column count, TOC below the prose.
* Resolve every intended link target against {PAGES_CSV} and the docs tree.
  Anything unresolvable is listed, not silently emitted.
* List the pages that need rewriting, the orphans to remove, the image stubs to
  create.

Output to stdout:
============================
STAGE 2 COMPLETE
Cluster pages needing rewrite: N   Orphans: N   Missing image pages: N
Unresolvable link targets: N (list)   needs_split nodes: N (list)
============================

============================
STAGE 3 — APPLY
============================

Prefer the generator. Structural rules live in {GEN_SCRIPT}; change the rule
there, rerun it, and every page moves together. Hand-editing individual pages is
for one-off fixes only.

* Update {GEN_SCRIPT} for any rule this prompt changed — {TOC_COLUMNS} columns,
  TOC above the prose, counts, labels, cross-links, prose preservation.
* Update {GEN_SCRIPT}'s image-page markup and its CK_EVIDENCE_LAYOUT CSS block
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
* Shared files ({PAGES_CSV}, {IMAGES_L2_PAGE}) are written by the orchestrator
  only.

Output to stdout:
============================
STAGE 3 COMPLETE
Cluster pages rewritten: N (L2 1, L3 N, L4 N, L5-cluster N)
Image pages relaid out: N  Inline width caps removed: N
Image stubs created: N     Orphans removed: N
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
* Walk the tree by hand from {IMAGES_L2_PAGE}: pick three level_3 nodes at
  random and click down to an image page at the bottom of each. Every step must
  present the next level's links at the top of the page.
* Spot-check five Level 3 and five Level 4 pages: TOC at the top, all YAML
  children present, {TOC_COLUMNS} columns, counts match the YAML, up-link and
  peer links present and resolving, cross-link to the mirrored written page
  present.
* LAYOUT CHECK on the Level 5 pages: run the verification section of
  {LAYOUT_GUIDELINES} in full — the grep checks against the built CSS bundle and
  the generated pages, then the browser eyeball checks it lists. Every point
  must pass before the run is declared complete.
* MEDIA-TYPE AUDIT. Grep every page {GEN_SCRIPT} wrote this run for `<video`,
  `<source`, `<audio`, and media-player `<iframe`. Expected count is ZERO; any
  hit fails the run. Then grep {GEN_SCRIPT} itself for those same strings —
  expected ZERO, because a generator that cannot render a video cannot leak
  one. Then grep ALL of {PHOTOS_DIR} and report the count separately: that is
  the protected pre-existing set, it was 9 on 2026-07-23, and it must not rise.
  Confirm all 9 are still on disk, byte-identical, and listed in
  {FINDINGS_FILE} — a drop in that number means the orphan sweep deleted a
  published page instead of protecting it.
* Run the invisible-Unicode scan over everything written.
* Confirm nothing outside {PHOTOS_DIR} and {PAGES_CSV} changed, and that
  {HIERARCHY_FILE}, {VIDEO_HIERARCHY_FILE}, {VIDEOS_L2_DIR}, and
  {SITE_DIR}/sidebars.ts are untouched.

Output to stdout:
============================
STAGE 5 COMPLETE — FINAL REPORT
Build: PASS/FAIL
Cluster pages under /Photos: L2 1, L3 N, L4 N, L5-cluster N
Image pages reachable: N of N in YAML (N excluded, N stubs pending write-up)
Walk-down checks: N/3 pass   Spot-checks: L3 N/5, L4 N/5
Layout: in-flow yes/no  opaque yes/no  text-wrap yes/no  stale width caps: N
Video/UNKNOWN entries skipped: N   media players emitted this run: 0 (required)
Protected /Photos pages carrying a video player: N (was 9, must not rise or fall)
pages.csv in sync: yes   images/images.yaml untouched: yes
videos.yaml untouched: yes   /Videos untouched: yes
sidebars.ts untouched: yes   invisible scan: clean
============================

============================
HARD RULES
============================

* {LAYOUT_GUIDELINES} is read at the very start of every run, before anything
  else, and overrides this prompt where they conflict. Never edit it from this
  prompt. Every point in it is a shipped defect to be fixed, and the run is not
  complete until each one is verified fixed on the built output.
* Level 5 image page LAYOUT is this prompt's responsibility; Level 5 PROSE is
  {IMAGE_PAGE_PROMPT}'s. Layout is fixed in {GEN_SCRIPT} and the marked CSS
  block in {CUSTOM_CSS}, then regenerated across every page — never by
  hand-editing individual image pages.
* STILL IMAGES ONLY. {GEN_SCRIPT} contains no branch that can emit `<video>`,
  `<source>`, `<audio>`, or a media-player `<iframe>`; entries typing as video
  or UNKNOWN are skipped, uncounted, unlinked, and reported. {GEN_SCRIPT} owns
  the CK_EVIDENCE_LAYOUT block in {CUSTOM_CSS} and never writes CK_VIDEO_LAYOUT.
  Nothing is ever written under {VIDEOS_L2_DIR}, {VIDEOS_DIR},
  {VIDEO_HIERARCHY_FILE}, or {VIDEO_PLANNING_DIR}.
* Any page under {PHOTOS_DIR} that already contains a `<video>` or `<source>`
  element is PROTECTED: never regenerated, never counted as an orphan, never
  removed. It is listed in {FINDINGS_FILE} and reported. Nine exist today.
* Every point in {LAYOUT_GUIDELINES} — placement, opacity, text wrap, the
  bounding box and its size calculation, square corners — is satisfied on the
  built output. That file specifies the layout; this prompt only enforces it.
* {HIERARCHY_FILE} is the source of truth and is READ-ONLY here. Discrepancies
  go in {FINDINGS_FILE}, never into the YAML from this prompt.
* Every Level 2, Level 3, and Level 4 page leads with its table of contents,
  directly under the H1. Prose comes after the map.
* Every child node in the YAML has a hyperlinked bullet on its parent's page,
  labeled with the child's title. Every image a node owns has a link on that
  node's page. Nothing in the YAML is unreachable from the tree.
* {TOC_COLUMNS} balanced columns, modeled on {HOME_PAGE}.
* Every page carries an up-link, peer links, and — where the node has a
  site_page or site_level_2 — a cross-link to the written section it mirrors.
  Overviews are linked /X/overview, never bare /X.
* Reruns refresh structure and preserve authored prose. Orphans are removed,
  counted, and reported.
* Image page bodies belong to {IMAGE_PAGE_PROMPT}. This prompt may create a stub
  so a link resolves; it never rewrites an existing image page's write-up.
* Nothing in {EXCLUDE_FILE} is ever linked or published.
* No claims of prior knowledge or of immoral or illegal conduct by any person;
  attribution language throughout; the word "defamation" never appears.
* No invisible Unicode in any emitted file — scan after every emit.
* {SITE_DIR}/sidebars.ts is never modified.
* The build must pass before the run is declared complete.

============================
BACKGROUND — ORIGINAL DIRECTIVE, KNOWLEDGE PRESERVED
============================

This section preserves the intent this prompt was narrowed to, so nothing is
lost even where a stage above already encodes it.

* Focus this on the levels. Right now we are in a Level 2 for images.
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
            title: "FBI"
            _key: FBI
            site_level_2: ["FBI"]
            site_page: "site/docs/FBI/overview.mdx"
            number_of_images: 14

* Our Level 2 page in this directory for images, the Level 3 pages in this
  images Level 2, and the Level 4 pages in this images Level 2 — this prompt is
  about the shape of those pages, the criteria for those pages, what makes them
  great, and what their goal is. The goal of this prompt is to update those
  pages.
* The output is nearly exclusively the files in the images Level 2 directory.
* The individual images are the Level 5 pages in this directory. We update the
  Level 2, Level 3, and Level 4 pages to make sure their tables of contents go
  to the next level down. That is what lets people navigate through and get into
  the individual images at the end, which are the Level 5 pages.
* The source of the data of what is correct is the YAML file, and that is also
  the hierarchy we want. Primarily we read from the YAML file and almost never —
  probably never — update the YAML file from this prompt.
* With the YAML above, that means we update the Level 2 page and make sure the
  table of contents goes off to the FBI-appropriate Level 3 page in the same
  directory.
* When we see a level_4 in the YAML file, that means we take that level_3 page,
  which is its parent, and make sure there is a bullet point that hyperlinks to
  that level_4 page by that name, using the title YAML property for the name in
  the user interface:

      level_4:
        - level_4:
            title: "TallyHallAlbum"
            _key: TallyHallAlbum
            number_of_images: 1
            number_of_images_recursive: 1

* The level_5 should go to a page for the site that is dedicated to one image,
  and it will have the write-up around that image:

      level_5:
        - level_5:
            title: "Baker Tilly — TPUSA's Auditor (Claims)"
            _key: TPUSA_CO_BakerTilly
            site_page: "site/docs/TPUSA/Companies/baker-tilly.mdx"

* In some cases some image files get links into them straight from a Level 3
  page or straight from the Level 4, and they may not need a Level 4 in between.
* This prompt might have done other things before. It is now focused on
  improving these hierarchy pages: reading from the YAML file and updating the
  Level 2, Level 3, and Level 4 pages underneath the directory that is the
  images Level 2.
