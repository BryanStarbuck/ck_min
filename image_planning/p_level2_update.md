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
IMAGE_PAGE_PROMPT is file {THIS_DIR}/p_yaml_to_site.md
HIERARCHY_PROMPT is file {THIS_DIR}/p_update_image_hierarchy.md

GENERATOR_DIR dir is {THIS_DIR}/generator
GEN_SCRIPT is file {GENERATOR_DIR}/gen_photos_pages.py
VERIFY_SCRIPT is file {GENERATOR_DIR}/verify_photos.py

SITE_DIR dir is {ROOT_DIR}/site
DOCS_DIR dir is {SITE_DIR}/docs
PHOTOS_DIR dir is {DOCS_DIR}/Photos
CUSTOM_CSS is file {SITE_DIR}/internals/src/css/custom.css

SIBLING VIDEO PIPELINE (read-only from here, never written):
VIDEO_PLANNING_DIR dir is {ROOT_DIR}/videos_planning
VIDEOS_DIR dir is {ROOT_DIR}/videos
VIDEO_HIERARCHY_FILE is file {VIDEOS_DIR}/videos.yaml
VIDEOS_L2_DIR dir is {DOCS_DIR}/Videos

IMAGES_L2_PAGE is file {PHOTOS_DIR}/overview.mdx
HOME_PAGE is file {DOCS_DIR}/index.mdx
PAGES_CSV is file {ROOT_DIR}/pages.csv
CK_FILE is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt
  (Real file; {ROOT_DIR}/Charlie_Kirk.txt is a symlink to it. Read the real path. READ-ONLY.)
ASSESS_MANUAL is file {ROOT_DIR}/prompts/Assess_Manual.md

TOC_COLUMNS is ... = 2
MAX_AGENTS is ... = 12

============================
GOAL
============================

Update the NAVIGATION pages of the images Level 2 ({IMAGES_L2_PAGE}, every Level 3 and Level 4 page under {PHOTOS_DIR}, and
deeper cluster pages) so each LEADS with a TOC carrying the visitor to the next level down, letting a visitor walk from the
left bar to any individual image page without dead-ending.

{HIERARCHY_FILE} is the source of truth (clusters, names, nesting, images). READ it, WRITE pages; (almost) never write the YAML.

The walk ends at the Level 5 image page (one image, one write-up). {IMAGE_PAGE_PROMPT} owns the WORDS; this prompt guarantees
each is reachable, correctly named, one click from its owning cluster page, and correctly LAID OUT. Layout is a templating
concern: fix it by changing {GEN_SCRIPT}'s markup and the CSS block it writes into {CUSTOM_CSS}, then rerun over all ~1,850
pages. Never hand-edit image pages for layout.

============================
SCOPE — WHAT THIS PROMPT TOUCHES
============================

Writes:
  * {IMAGES_L2_PAGE}: the marked TOC section only.
  * Every cluster overview.mdx under {PHOTOS_DIR} (Level 3, Level 4, deeper cluster nodes).
  * The LAYOUT of every Level 5 image page (image element, its wrapper, the prose wrapper, inline styles on them); the prose
    between wrappers is untouched.
  * {CUSTOM_CSS}: only between /* CK_EVIDENCE_LAYOUT_START */ and /* CK_EVIDENCE_LAYOUT_END */.
  * {PAGES_CSV} rows for these pages.
  * {GEN_SCRIPT}: the implementation of the rules below (structural and layout changes go here and are rerun, never page by page).
Does NOT write:
  * {HIERARCHY_FILE} (read-only; record problems in {FINDINGS_FILE}).
  * Image page PROSE ({IMAGE_PAGE_PROMPT}'s). A missing leaf may be created as a stub so a TOC link resolves (reported).
  * {SITE_DIR}/sidebars.ts (never, unless explicitly asked).
  * {VIDEOS_L2_DIR}, {VIDEOS_DIR}, {VIDEO_HIERARCHY_FILE}, {VIDEO_PLANNING_DIR} (the video pipeline has its own nav prompt,
    generator and TOC markers; editing there destroys that work).
  * Anything outside {PHOTOS_DIR} other than {PAGES_CSV} rows and the marked CSS block.

============================
KNOWLEDGE — MEDIA-TYPE SCOPE: THE LEVEL 5 LAYOUT IS AN IMAGE LAYOUT
============================

  images                                videos
  {PHOTOS_DIR}                          {VIDEOS_L2_DIR}
  {HIERARCHY_FILE}                      {VIDEO_HIERARCHY_FILE}
  {GEN_SCRIPT}                          gen_videos_pages.py
  Img_*.mdx leaf pages                  Vid_*.mdx leaf pages
  CK_EVIDENCE_LAYOUT css block          CK_VIDEO_LAYOUT css block
  ck-evidence-* classes                 ck-video-* classes
  <img> served from static/img/evidence <video> off a public IPFS gateway

Both generators write {CUSTOM_CSS}; each owns only its marked block. {GEN_SCRIPT} owns CK_EVIDENCE_LAYOUT and never writes
CK_VIDEO_LAYOUT (each would destroy the other's layout on alternate runs).

THE GENERATOR MUST NOT BE ABLE TO RENDER A VIDEO. {GEN_SCRIPT} has a classify_ipfs_cids() helper, an is_video_src() test, and
a branch emitting
    <div className="ck-evidence-image-wrap ck-evidence-wide">
      <video className="ck-evidence-image" controls preload="metadata">
        <source src="https://ipfs.io/ipfs/<CID>" type="video/mp4" />
into Img_*.mdx pages. That branch published nine video pages under {PHOTOS_DIR}/Official_Narrative/Narrative_Shot_in_the_Heart/
("What This Image Shows", ck_image_cid: none).
The fix INVERTS the type test (keep the classifier, use it to SKIP):
  * Video-typed entry: no leaf page, no {PAGES_CSV} row, no TOC link, not counted in the parent's recursive count. Counted and reported.
  * Unsettled type = UNKNOWN = skipped (all 9 bad entries are extensionless IPFS CIDs with empty sha256).
  * {GEN_SCRIPT} keeps no branch able to emit <video>, <source>, <audio> or a media-player <iframe>.
  * Oracle: {VIDEOS_DIR}/manifest.yaml and {ROOT_DIR}/IPFS/ipfs.txt, both parsed BY FILENAME (wholesale CID scraping typed 70
    entries as video when only 9 are). Not {VIDEO_HIERARCHY_FILE} yet (schema shell of image data). Fallback: how the CID is
    embedded elsewhere on the site.
THE NINE EXISTING PAGES ARE PROTECTED, NOT ORPHANS: any {PHOTOS_DIR} page containing <video> or <source> is left byte-identical,
excluded from orphan removal, listed in {FINDINGS_FILE}, and counted. Migration to {VIDEOS_L2_DIR} then withdrawal is a separate,
explicitly-approved job.

============================
KNOWLEDGE — READ FIRST, IN THIS ORDER
============================

  1. {LAYOUT_GUIDELINES}: READ FIRST, EVERY RUN, IN FULL. Every point in it was added after a real defect shipped; restate each
     point before working and treat each as a defect to verify fixed by run end. It OVERRIDES this prompt (where they disagree,
     correct this prompt). It carries the whole Level 5 layout spec (placement, bounding box and size calculation, the CSS block's
     job, the verification checklist on built output); this prompt does not restate it. Every point, including new ones, is
     implemented in {GEN_SCRIPT} and the {CUSTOM_CSS} block, rerun over every page, verified on the built output.
  2. {CHARTER_FILE} (audience, levels, schema, hard rules).
  3. {HOME_PAGE}: the TOC pattern to imitate.
  4. {HIERARCHY_FILE}: parse fully; index nodes (_key, title, depth, parent, site_level_2, site_page, number_of_images,
     number_of_images_recursive) and images (sha256, file_path).
  5. {PAGES_CSV}: link targets; kept in sync.
  6. {ASSESS_MANUAL}.
  7. {CK_FILE}: headers plus sections for the clusters in play; no cluster paragraph is written without its section in context.

============================
KNOWLEDGE — THE MODEL: THE HOME PAGE TOC
============================

{HOME_PAGE} is good because: the TOC IS the page, starting right under the H1 (the whole map before any prose); links are grouped
under headings that themselves link to the section overview; balanced side-by-side columns keep long lists on one screen; labels
are short human titles.
Our pages copy it with {TOC_COLUMNS} columns instead of three (better at our narrower main area; existing three-column pages move
to {TOC_COLUMNS}). Markup, in the home page's idiom:

  <div style={{ display: "flex", justifyContent: "space-between", gap: "2rem" }}>
  <div style={{ flex: 1 }}>
    * [Label](/Photos/.../overview)
  </div>
  <div style={{ flex: 1 }}>
    * [Label](/Photos/.../Img_key)
  </div>
  </div>

Split in reading order, balanced by count, child clusters before image pages.

============================
KNOWLEDGE — THE LEVEL MODEL AND THE YAML MAPPING
============================

  Level 1  {DOCS_DIR}/index.mdx, the site home.
  Level 2  {IMAGES_L2_PAGE}, url /Photos, left-bar "Photos". Where a cold visitor arrives.
  Level 3  one page per level_3 node.   Level 4  one per level_4 node.
  Level 5  image pages. A level_5 CLUSTER node also becomes a cluster page; its images are its leaves.

  level_3:
    - level_3:
        title: "FBI"                          -> the H1 and the link label
        _key: FBI                             -> dir name and url segment: /Photos/FBI/overview
        site_level_2: ["FBI"]                 -> site docs dirs covered; cross-link targets
        site_page: "site/docs/FBI/overview.mdx"
                                              -> the written page mirrored; link it as /FBI/overview
        number_of_images: 14                  -> images owned directly (its own leaf pages)
        number_of_images_recursive: 24        -> the count shown on the PARENT's TOC line
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

A level_5 node works the same one level further down, cross-linking its site_page when present, e.g.
        level_5:
          - level_5:
              title: "Baker Tilly — TPUSA's Auditor (Claims)"
              _key: TPUSA_CO_BakerTilly
              site_page: "site/docs/TPUSA/Companies/baker-tilly.mdx"
A node may own images with no child clusters (images may hang off a Level 3 or a Level 4); never invent a level. Titles are used
verbatim as labels; _key verbatim as dir name, url segment and page_key.

============================
KNOWLEDGE — WHAT MAKES A GREAT CLUSTER PAGE
============================

Navigation: hand the visitor the next click.
  * TOC at the TOP, directly under the H1 and back button; nothing of substance above it.
  * Every YAML child appears, nothing extra.
  * Child clusters first, bolded, with recursive counts; then the node's own image pages.
  * {TOC_COLUMNS} balanced columns; labels are YAML titles (no keys, no filenames).
  * A one-to-three sentence concept paragraph AFTER the TOC, grounded in {CK_FILE}.
  * A cross-link to the written section mirrored (site_page / site_level_2).
  * Up-link to the parent and peer links to siblings; no dead ends.
  * Every link resolves; overviews as /X/overview, never bare /X; checked against {PAGES_CSV}.
Both arrival paths must work (cold from the left bar; topic arrival mid-tree, which is why up and peer links matter).

============================
KNOWLEDGE — PER-LEVEL SPECIFICATION
============================

=== Level 2: {IMAGES_L2_PAGE} ===
  * Keep the frontmatter and the existing prose (good prose on photographic evidence).
  * TOC between {/* PHOTOS_TOC_START */} and {/* PHOTOS_TOC_END */}, fully regenerated; outside untouched. MOVE the markers if
    needed so the TOC sits directly under the H1, above the prose.
  * Every level_3 in YAML order: title label, /Photos/{L3_key}/overview href, number_of_images_recursive; {TOC_COLUMNS} columns.
  * One line above the TOC: total clusters and images.

=== Level 3: {PHOTOS_DIR}/{L3_key}/overview.mdx ===
  * Frontmatter: displayed_sidebar: docs, slug, title, sidebar_label, description, ck_node_key (= _key).
  * Back button to /Photos/overview. H1 from the node title.
  * TOC right below: level_4 children bolded with recursive counts, then owned image pages.
  * Concept paragraph(s) after; cross-links to site_page and each site_level_2; Related Areas: up-link to Photos plus every peer level_3.

=== Level 4: {PHOTOS_DIR}/{L3_key}/{L4_key}/overview.mdx ===
  * Same shape; back button to the parent Level 3; TOC: level_5 cluster children first, then image pages; Related Areas: up-link
    to the parent, peers = sibling level_4s.

=== Level 5: the image pages (WORDS: {IMAGE_PAGE_PROMPT}; LAYOUT: here) ===
  * Reachability: each exists at {node dir}/{Img_key}.mdx, its title matches the parent TOC label, the link resolves. Missing page:
    create a minimal stub (frontmatter with ck_image_sha256 and ck_node_key, the image, a placeholder heading) and report it.
    Never overwrite an existing page's prose.
  * Layout, every page, every run, from {GEN_SCRIPT}: fixed structure (frontmatter with hide_table_of_contents: true, back button,
    H1, image wrapper, prose wrapper holding the whole write-up). Behaviour lives in the CK_EVIDENCE_LAYOUT block, not per-page
    inline styles. The class contract, source order, bounding box and size calculation, wrap behaviour and look are specified in
    {LAYOUT_GUIDELINES}: implement it, invent nothing. Verified on the BUILT output (Stage 5).

============================
KNOWLEDGE — RERUNS PRESERVE PROSE
============================

  Regenerated every run: mechanical frontmatter, back button, the whole TOC, counts, Related Areas, peer and child lists, column markup.
  Carried forward when present: title, sidebar_label, frontmatter description, authored paragraphs under "## About This Cluster".
Generator boilerplate IS refreshed (it recognizes its own); hand-written, enriched or safe-writing-scrubbed prose survives every
regeneration. Pages the YAML no longer accounts for are orphans (renamed key, removed node): remove, count, report (never the
protected video pages).

============================
KNOWLEDGE — GATES THAT STILL APPLY
============================

  * BAN SET = union of {BAN_IMAGES_CSV} (MASTER; rows sha256, cid, file_path, banned, reason, date_added; match sha256, then cid,
    then file_path; banned=false is an explicit un-ban) and {EXCLUDE_FILE} (older sha256 list, honoured). Read both before building
    navigation. A banned image gets no Level 5 page, no TOC entry, no static copy, NO LINK INTO IT from anywhere (thumbnail, card,
    "see also", bypass target); existing pages and copies are deleted; counts reflect what is published; a node whose every image
    is banned publishes no page. The YAML `banned:` (copied by {HIERARCHY_PROMPT}) only corroborates; re-check the two files every
    run; report disagreements (files win). Newly found non-public material (private documents, unrelated third-party records, an
    accusation burned into the image): add a CSV row with reason and date before the run ends and note it in {FINDINGS_FILE}.
  * BYPASS AND BAN INTERACT: a node resolving to one image page is bypassed (parents and peers link straight to the image page; see
    {IMAGE_PAGE_PROMPT}). If that one image is banned there is no page to bypass to: the node is unpublished and in no TOC. Apply
    the ban set BEFORE computing the bypass set.
  * Safe writing on every word: never "defamation"; never that a person knew anything before the crime or did anything immoral or
    illegal; never a living person committing a crime as fact unless court-proven; attribution throughout; say as much as useful.
  * MDX comments must be {/* ... */}; HTML <!-- --> breaks the compile and deploy.
  * needs_split nodes (over twelve images): render as is and report them for the hierarchy pass.

============================
OUTPUT SANITIZATION — NO INVISIBLE UNICODE, EVER
============================

No emitted .mdx page or {PAGES_CSV} row may contain invisible Unicode (zero-width, bidi controls, no-break spaces incl. U+202F,
word joiners, BOMs, controls, variation selectors, tag chars).
  * Prose: replace space-like invisibles with a space, delete zero-width/bidi/control chars, collapse whitespace; visible non-ASCII may stay.
  * Pages never contain mirror filenames (copies are sha256-named), so the macOS U+202F problem never reaches a page.
After every emit pass, rescan everything written and hard-fail on any hit. The set is enumerated in {GEN_SCRIPT} and in
{HIERARCHY_PROMPT}'s OUTPUT SANITIZATION section.

============================
STAGE 1 — READ AND INDEX
============================

* Read the knowledge files in order. Parse the YAML into a node index (depth, parent, _key, title, site bindings, own and
  recursive counts, images).
* Inventory existing {PHOTOS_DIR} pages (ck_node_key / ck_image_sha256) into the existing-page map.
* BUILD THE BAN SET: parse {BAN_IMAGES_CSV} with the python3 csv module (create it with header
  sha256,cid,file_path,banned,reason,date_added if missing) plus {EXCLUDE_FILE}; union minus un-bans; index by sha256, cid,
  expanded file_path; mark banned images in the node index so Stage 2 computes bypasses and TOCs over publishable images only.
  Cross-check the YAML `banned:`; report disagreements.

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

* For every cluster node, compute its correct TOC from the YAML and diff against the page: missing children, stale labels, wrong
  counts, broken links, wrong column count, TOC below the prose.
* Resolve every intended link against {PAGES_CSV} and the docs tree; list the unresolvable (never emit them silently).
* List pages to rewrite, orphans to remove, image stubs to create.

Output to stdout:
============================
STAGE 2 COMPLETE
Cluster pages needing rewrite: N   Orphans: N   Missing image pages: N
Unresolvable link targets: N (list)   needs_split nodes: N (list)
============================

============================
STAGE 3 — APPLY
============================

Prefer the generator: change the rule in {GEN_SCRIPT}, rerun, every page moves together. Hand edits only for one-offs.
* Update {GEN_SCRIPT} for every rule here ({TOC_COLUMNS} columns, TOC above prose, counts, labels, cross-links, prose
  preservation, the media-type skip).
* Update its image-page markup and CK_EVIDENCE_LAYOUT block for every {LAYOUT_GUIDELINES} point the output doesn't yet satisfy
  (layout is fixed here and nowhere else).
* Run it over the whole tree.
* Where prose judgment is needed on many clusters (a missing concept paragraph, reconciling a label against {CK_FILE}), partition
  level_3 subtrees across up to {MAX_AGENTS} agents (never split a subtree; each agent gets its own scratch subdirectory, since
  agents invent the same helper filenames and collide).
* {PAGES_CSV} and {IMAGES_L2_PAGE} are written by the orchestrator only.

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

* Merge rows for every cluster page created, rewritten, retitled or removed, per the schema in {ROOT_DIR}/claude.md: page_key =
  node _key, parent_key = parent node _key, level = node level, url_path, file_path, title, sidebar_label, directory, extension,
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
* Walk down by hand from {IMAGES_L2_PAGE} through three random level_3 nodes to an image page: every step shows the next level's
  links at the top.
* Spot-check five Level 3 and five Level 4 pages: TOC at top, all YAML children, {TOC_COLUMNS} columns, counts match, up and peer
  links resolve, cross-link to the mirrored page present.
* LAYOUT CHECK: run {LAYOUT_GUIDELINES}' verification section in full (grep checks on the built CSS bundle and generated pages,
  then its browser eyeball checks). Every point passes before completion.
* MEDIA-TYPE AUDIT: grep pages {GEN_SCRIPT} wrote this run for `<video`, `<source`, `<audio`, media `<iframe`: ZERO required. Grep
  {GEN_SCRIPT} itself for the same: ZERO required. Grep ALL of {PHOTOS_DIR} and report separately (the protected set; 9 on
  2026-07-23; must not rise or fall). Confirm all 9 are on disk, byte-identical, listed in {FINDINGS_FILE} (a drop means the
  orphan sweep deleted a published page).
* Invisible-Unicode scan over everything written.
* Nothing outside {PHOTOS_DIR}, {PAGES_CSV}, the marked CSS block and {GEN_SCRIPT} changed; {HIERARCHY_FILE},
  {VIDEO_HIERARCHY_FILE}, {VIDEOS_L2_DIR}, {SITE_DIR}/sidebars.ts untouched.

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

* {LAYOUT_GUIDELINES} is read first every run, overrides this prompt, is never edited from here; every point is a shipped defect
  to verify fixed on the built output (placement, opacity, text wrap, bounding box and size calculation, square corners).
* Level 5 LAYOUT is this prompt's (fixed in {GEN_SCRIPT} and the marked {CUSTOM_CSS} block, regenerated everywhere, never
  hand-edited); Level 5 PROSE is {IMAGE_PAGE_PROMPT}'s (this prompt may create a stub, never rewrite a write-up).
* STILL IMAGES ONLY: {GEN_SCRIPT} has no branch able to emit <video>, <source>, <audio>, media <iframe>; video/UNKNOWN entries are
  skipped, uncounted, unlinked, reported; {GEN_SCRIPT} never writes CK_VIDEO_LAYOUT; nothing written under {VIDEOS_L2_DIR},
  {VIDEOS_DIR}, {VIDEO_HIERARCHY_FILE}, {VIDEO_PLANNING_DIR}.
* {PHOTOS_DIR} pages containing <video> or <source> are PROTECTED: never regenerated, never orphans, never removed; listed in
  {FINDINGS_FILE}. Nine exist today.
* {HIERARCHY_FILE} is the source of truth and READ-ONLY; discrepancies go to {FINDINGS_FILE}.
* Every Level 2, 3, 4 page leads with its TOC directly under the H1; prose after the map. {TOC_COLUMNS} balanced columns modeled on
  {HOME_PAGE}.
* Every YAML child has a titled bullet on its parent; every owned image is linked; nothing in the YAML is unreachable.
* Every page has an up-link, peer links, and a cross-link to its mirrored written section where site_page / site_level_2 exist;
  overviews as /X/overview.
* Reruns refresh structure and preserve authored prose; orphans removed, counted, reported.
* Nothing in the ban set is ever linked or published.
* No claims of prior knowledge or immoral/illegal conduct; attribution throughout; never "defamation".
* No invisible Unicode in any emitted file. sidebars.ts never modified. The build must pass before completion.
