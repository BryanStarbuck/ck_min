ROOT_DIR dir is ~/BGit/Bryan_git/charlie-kirk

SITE_DIR dir is {ROOT_DIR}/site
DOCS_DIR dir is {SITE_DIR}/docs
CSS_FILE is file {SITE_DIR}/internals/src/css/custom.css
EVIDENCE_DIR dir is {SITE_DIR}/internals/static/img/evidence
PAGES_CSV is file {ROOT_DIR}/pages.csv
IMAGES_YAML is file {ROOT_DIR}/images/images.yaml
VIDEOS_YAML is file {ROOT_DIR}/videos/videos.yaml
BAN_IMAGES_CSV is file {ROOT_DIR}/images/ban_images.csv
BAN_VIDEOS_CSV is file {ROOT_DIR}/videos/ban_videos.csv
ASSESS_MANUAL is file {ROOT_DIR}/prompts/Assess_Manual.md
PILOT_DIR dir is {DOCS_DIR}/Tyler_Robinson/discord

WORK_DIR dir is {ROOT_DIR}/prompts/four_squares
CARD_INDEX_CSV is file {WORK_DIR}/card_index.csv
LEDGER_CSV is file {WORK_DIR}/ledger.csv
ROUTES_TXT is file {WORK_DIR}/routes.txt
BUILD_INDEX_PY is file {WORK_DIR}/build_card_index.py
CHECK_PY is file {WORK_DIR}/verify_blocks.py

AGENT_COUNT is 12
EFFORT is high
BATCH_SIZE is 35        (was 20; agents used well under half their context at 20)

MAX_SENTENCE_WORDS is 17
SENTENCES_PER_INTERESTING_BLOCK is 4
CARDS_PER_FOUR_SQUARE is 4

Read {ASSESS_MANUAL} before editing any page, plus the "Pages CSV" and "Images Are Tracked In Git" sections of {ROOT_DIR}/claude.md.


============================
GOAL
============================

Walk EVERY page under {DOCS_DIR}, recursively (the whole site: ~1,755 editable pages across ~73 Level 2 areas), and give each four
new blocks that carry a reader sideways into the site instead of dead-ending at the bottom. Resumable across many waves; a wave
that stops early is fine as long as the ledger records exactly what is done.

The four blocks, in this order, at one anchor point:
  1. Interesting In This Area      four short, densely hyperlinked sentences; every link inside the page's own Level 2.
  2. Interesting In Other Areas    same shape; every link in some OTHER Level 2.
  3. Four squares - in this area   2x2 grid of four sister-page cards from the page's own Level 2.
  4. Four squares - other areas    2x2 grid of four cards, each from a DIFFERENT Level 2, none the page's own.

A square carries the sister page's hero image or video, two or three sentences on what is in it and why it matters, and a chevron
button to it. Solid background, white text, not large. {PILOT_DIR} is the working pilot (every page there carries block 3): open two
or three and copy the markup exactly.


============================
WHAT ALREADY EXISTS - DO NOT REBUILD IT
============================

* CSS is shipped in {CSS_FILE} between CK_FOUR_SQUARE_START and CK_FOUR_SQUARE_END:
    .ck-4sq          the 2x2 grid wrapper, collapses to one column below 996px
    .ck-4sq-card     one square. Solid #0d2b6b panel, white text
    .ck-4sq-side     card modifier: media left, text to its right
    .ck-4sq-stack    card modifier: media on top, text underneath
    .ck-4sq-thumb    the media anchor
    .ck-4sq-body     the text side
    .ck-4sq-title    sister page title, links to it
    .ck-4sq-text     the two or three sentences, may contain its own links
    .ck-4sq-btn      the white chevron button
  No new CSS; a genuinely new shape goes inside those markers and is noted in the report.
* {PILOT_DIR}'s 28 pages already carry CK_4SQ_SECTION; leave it; they still need blocks 1, 2, 4.
* {WORK_DIR} holds this run's machine inputs (throwaway, not site content); see BUILT TOOLING.


============================
HARD PROHIBITIONS
============================

* NEVER write to ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt (read only; see {ROOT_DIR}/claude.md).
* NEVER touch {SITE_DIR}/sidebars.ts.
* NEVER edit anything outside {DOCS_DIR} except {PAGES_CSV} and {WORK_DIR}.
* NEVER use an HTML comment in a .md or .mdx file (see BLOCK MARKERS).
* NEVER add a per-file image line to {ROOT_DIR}/.gitignore or use git add -f; if Large File Bridge re-appended such lines, delete them.
* Do not commit (an external auto-commit sweeper handles the working tree).


============================
BLOCK MARKERS
============================

Every block is fenced so a re-run replaces it in place:
  CK_INTERESTING_HERE_START   ... CK_INTERESTING_HERE_END
  CK_INTERESTING_OTHER_START  ... CK_INTERESTING_OTHER_END
  CK_4SQ_SECTION_START        ... CK_4SQ_SECTION_END
  CK_4SQ_SITEWIDE_START       ... CK_4SQ_SITEWIDE_END

In EVERY file, .mdx and .md alike, each marker is written
    {/* CK_4SQ_SECTION_START */}
NEVER <!-- -->: docusaurus.config.ts sets no markdown.format override, so .md compiles through MDX too, and a bare <!-- is a hard
parse error ("Unexpected character `!` (U+0021) before name"). One fails npm run build, fails the Pages workflow, and freezes the
ENTIRE live site on its last good commit (2026-08-19: <!-- markers in 43 .md files under site/docs/laws/ silently blocked every deploy).

* Every run strips any existing block with these markers FIRST (match both {/* */} and legacy <!-- --> so old files are repaired),
  then writes the new one. Never nest or append a second copy.
* Text outside the markers is never touched (prose, tables, existing "## Interesting" lists, "## Related Areas" grids, "## Images"
  galleries all survive).


============================
WHERE THE BLOCKS GO ON THE PAGE
============================

Insert all four together, in GOAL order, ABOVE the FIRST of these anchors present in the file (one blank line each side):
  1. {/* CK_AUTHOR_CREDIT */}          (present on most pages - the usual case)
  2. a line that is exactly   ## Interesting
  3. a line that is exactly   ## Related Areas
  4. {/* CK_PLACED_IMAGES_START
  5. a "## Sources" or "## Fix Laws" or "## The Laws" heading
  6. end of file

Finished page order: frontmatter, back button, H1, hero media, the page's prose, Interesting In This Area, Interesting In Other
Areas, Other Pages In This Section (4sq same Level 2), Elsewhere In The Investigation (4sq other Level 2s), author credit,
Interesting (old three-bullet block, if present), Related Areas, Images. Readers meet the blocks after the article, above the
laws, credits, related grid and gallery.


============================
STAGE 0 - BUILD THE MACHINE INPUTS ONCE
============================

Deterministic, done once before any agent launches (agents spend their context on judgement and prose).

* mkdir -p {WORK_DIR}
* {BUILD_INDEX_PY} walks {DOCS_DIR} and emits {CARD_INDEX_CSV}, one row per editable page:
    url_path        public route, overview pages as /Dir/overview
    file_path       repo-relative path
    extension       md or mdx
    level           from {PAGES_CSV} where known, else derived from depth
    level2          the immediate subdirectory of {DOCS_DIR} it lives under
    is_overview     yes if the basename is overview.md/.mdx or README.md
    title           frontmatter title, else the first H1
    sidebar_label   frontmatter sidebar_label, else title
    description     frontmatter description, one line, quoted
    media_kind      image | video | none
    media_src       first /img/evidence/<sha>.jpg in the body, or the video src
    media_cid       the data-cid sitting on that same tag, else empty
    media_alt       the alt text on that same tag, else empty
    media_shape     ck-4sq-side | ck-4sq-stack | none
    banned          yes if the media is in the ban set
    anchor          which of the six anchors this file will use
    teaser          empty at first - filled in by agents as they go
  Rules (getting these wrong breaks the live site):
  * Image media_src is ALWAYS the local /img/evidence/<sha256>.jpg, never an ipfs.io or dweb.link URL (most CIDs in {IMAGES_YAML}
    came from "ipfs add -n" and sit on no node: the gateway 504s for visitors while rendering fine locally). The CID stays in
    data-cid as provenance. Videos keep their gateway src, copied verbatim from the sister page.
  * media_shape from MEASURED pixels: sips -g pixelWidth -g pixelHeight {EVIDENCE_DIR}/<sha>.jpg; ratio = width/height;
    ratio < 1.0 portrait -> ck-4sq-side (media left, text RIGHT); ratio >= 1.0 landscape -> ck-4sq-stack (media on top). Measure each
    distinct sha once and cache it (~2,000 files).
  * banned = UNION of {BAN_IMAGES_CSV}, {BAN_VIDEOS_CSV}, image_planning/exclude_images.txt, videos_planning/exclude_videos.txt,
    matched on sha256, then cid, then file_path.
  * Media failing either check counts as none (untracked or ignored images render locally and 404 for visitors):
        git ls-files --error-unmatch <path>    must succeed
        git check-ignore -v <path>             must produce nothing
* {ROUTES_TXT} comes from {SITE_DIR}/build/**/*.html (what visitors actually receive) via build_routes.py, NEVER from source filenames
  (that shipped 76 dead links on 59 pages): a leading year is not a number prefix (/court/Days_in_Court/2026-03-10-seal-motion, not
  /03-10-seal-motion; likewise /Timeline/12-23-shooting-time and /Planes/99-0004-Vance), and frontmatter id:/slug: override filenames
  (court/mirandize/overview.md serves /court/mirandize/mirandize-overview). Docusaurus strips numeric prefixes from directory segments
  too (laws/2_US_Intel/... serves /laws/US_Intel/...) but not years: resolve against built routes, never reimplement the rule. Some
  routes contain spaces and parentheses ("/Topics3/Suspects (List)/overview"): read with splitlines(), never split(). Stale or missing
  build: keep the previous routes.txt. Do NOT run npm run build just to check links (twenty minutes).
  routes.txt is OWNED by build_routes.py; build_card_index.py writes routes_derived.txt only (it once overwrote routes.txt and
  reintroduced every error above).
  KNOWN UNROUTABLE: site/docs/TPUSA/TPUSA.mdx (no /TPUSA/TPUSA route; name collides with the dir). Link /TPUSA/overview instead; never
  card or link it; flagged for a human.
* {LEDGER_CSV}, one row per editable page: file_path,level2,status,blocks,agent,updated
  status starts TODO. blocks is HOSW, one letter per block written (H=interesting-here, O=interesting-other, S=section 4sq,
  W=sitewide 4sq), dash for not yet. DONE only at HOSW (or the reduced sets in Stage 3).
* {CHECK_PY}: the Stage 7 verifier, so all agents check identically.


============================
BUILT TOOLING - STAGE 0 OUTPUT
============================

Stage 0 has run; its output is in {WORK_DIR} (read {WORK_DIR}/RESUME.md for run state). Reuse it; rebuild only when the site changed materially.
  build_card_index.py   builds card_index.csv, routes.txt, ledger.csv, shape_cache.json. Idempotent: carries the teaser column and
                        ledger status/agent forward; that merge MUST happen before the first write (once it ran after, blanking all
                        892 teasers, and the next wave authored competing ones).
  verify_blocks.py      the Stage 7 verifier, run per file
  merge_wave.py         the Stage 8 merge: reads the SITE as ground truth (not agent reports), rewrites the ledger, refreshes pages.csv
                        line_count, deals the next wave into batches/agent_N.txt
  check_site.sh         runs the verifier across every page carrying a block
  AGENT_BRIEF.md        the operating summary handed to each agent
  GOLDEN_EXAMPLE.mdx    a verified four-block page to copy
  agent_buckets.json    the stable area-to-agent assignment
  batches/agent_N.txt   the current wave's pages for agent N
Index-builder lessons:
  * A video hero cannot be a card thumb (an .mp4 URL in an <img> is broken). Resolve to its poster under /img/video_posters/ (poster
    attribute, or cid -> sha256 in {VIDEOS_YAML}); no poster = no media, thumb-less card.
  * A page's hero is the first image ABOVE the generated blocks. Images inside CK_4SQ blocks belong to OTHER pages; never harvest them.
    Images in a CK_PLACED_IMAGES block are a legitimate fallback when there is no floated hero.
Shape of the work: 1,755 editable pages, 73 Level 2 areas, 812 with usable media, 943 without.

============================
STAGE 1 - LOAD THE MAP
============================

* Read {PAGES_CSV} (columns per {ROOT_DIR}/claude.md; used here: page_key, level, level2_parent, page_type, url_path, file_path, title,
  sidebar_label, description).
* Reconcile disk vs {PAGES_CSV}:
  * File with no row: add one (page_key four words max, underscores, unique; parent_key = its dir's overview; level, level2_parent,
    level2_section, page_type, url_path, file_path, title, sidebar_label, directory, extension, has_frontmatter, line_count, description).
  * Row whose file is gone: report, never delete (human decision). Never renumber or re-key rows.
  * Known duplicate rows from an external process: don't dedupe; report the count.
* A page's Level 2 = its level2_parent; a level-2 page is its own Level 2.
* Skip as edit targets (keep as link targets): page_type image or video (the generated /Photos and /Videos leaves, ~3,014 of 4,772
  files); the site root index; any CLAUDE.md; pages under a generator-owned directory ("generated by" comment at top) unless that
  generator's prompt says otherwise. laws/README.md IS a published page, in scope.
* THE SITE'S EXCLUDE LIST DEFINES WHAT IS A PAGE. The docs plugin in {SITE_DIR}/docusaurus.config.ts excludes:
      **/_*.{js,jsx,ts,tsx,md,mdx}     underscore-prefixed files
      **/_*/**                          anything under an underscore directory
      **/*.test.{js,jsx,ts,tsx}
      **/__tests__/**
      **/prompts/**
      **/CLAUDE.md
      **/p_*.{md,mdx}                   prompt files living inside docs
  A match is unpublished: never edit or card it (the first run edited nine unreachable files: After/house/p_research.md and eight
  Consciousness_Control/_research/*.md; reverted). The index builder mirrors this list.


============================
STAGE 2 - PARTITION THE WORK ACROSS {AGENT_COUNT} AGENTS
============================

* Count EDITABLE pages per Level 2 (Photos and Videos count zero), sort largest first, deal round-robin into {AGENT_COUNT} buckets.
* Never split a directory: an agent owns whole Level 2 areas, stably across waves (consistent teasers and rotation). Root-level loose
  pages go to the smallest bucket.
* Launch all {AGENT_COUNT} agents in ONE message, effort {EFFORT}. Each receives its owned dirs, its batch (first {BATCH_SIZE} TODO pages
  in its bucket), {CARD_INDEX_CSV}, {ROUTES_TXT}, {LEDGER_CSV}, and this prompt. It may edit ONLY files in its own dirs; it may READ anything.
* {PAGES_CSV}, {LEDGER_CSV} and {CARD_INDEX_CSV} are single-writer: agents return new/missing rows, completed ledger rows and teasers as
  data in their final report; the coordinator merges once (twelve concurrent CSV writers lose rows).


============================
STAGE 2B - WAVES
============================

A wave: {AGENT_COUNT} agents x {BATCH_SIZE} pages, all report, the coordinator merges ledger, teasers and pages.csv rows and prints:
    wave N complete - pages done X of Y (Z%) - failures F
* Repeat until every ledger row is DONE.
* An agent short of context stops cleanly on a page boundary, reporting what it finished; never a half-written block.
* Fix any MDX compile failure before the next wave (one broken page stops the whole site deploying).


============================
STAGE 3 - PICK THE SISTER PAGES
============================

Block 3 (in this area):
* Pool = every editable page with this page's level2_parent, minus itself, in a stable thematic order (the section overview's listing
  order if it lists them, else alphabetical by url_path).
* For index i in a pool of size N take (i+1), (i+7), (i+13), (i+19) mod N (spreads picks; equal inbound cards when N is coprime with the
  offsets). Collisions: dedupe, fill from the nearest unused index.
* N <= 5: use every other page in the section and stop (no repeats, never outside the section).
* Section of TWO editable pages (one sister): omit block 3 and carry that link in block 1. A one-page Level 2 has no in-area block.
  Expected block sets: 1 page "-O-W", 2 pages "HO-W", 3+ "HOSW".
* An offset landing on banned media or a CLAUDE.md steps to the next unused index.
* Overview/hub pages may skip the offsets: card the four most important pages in the section, on merit.
* Never card the page itself.

Block 4 (other areas):
* Four pages from four DIFFERENT Level 2s, none this page's own.
* On genuine relevance: the page a reader of THIS page would most want next from that area; read it before carding. Prefer substantial
  Level 3 pages with their own hero over stubs and Level 2 overviews.
* Rotate so a section doesn't point at the same four pages: page i starts its area sweep at position (i * 4) in the area list.
* Never card a /Photos or /Videos page (generated leaves; link targets from prose only).


============================
STAGE 4 - BUILD ONE CARD
============================

Media: reuse media_src, media_cid, media_alt, media_shape verbatim from the sister's {CARD_INDEX_CSV} row (never re-derive or invent a
src); add loading="lazy". media_kind none: .ck-4sq-stack, no thumb (normal; ~half the pages have no media); never a broken img. banned
yes: pick a different sister.

Markup - copy exactly, substituting values:

<div className="ck-4sq-card ck-4sq-side">
  <a className="ck-4sq-thumb" href="{url}"><img src="{src}" data-cid="{cid}" alt="{alt}" loading="lazy" /></a>
  <div className="ck-4sq-body">
    <p className="ck-4sq-title"><a href="{url}">{title}</a></p>
    <p className="ck-4sq-text">{two or three sentences, with links}</p>
    <a className="ck-4sq-btn" href="{url}">Read this <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6" /></svg></a>
  </div>
</div>

Thumb-less variant: drop the first <a> line. Four cards go inside one <div className="ck-4sq"> ... </div>.

Text: two or three sentences, what is in it and why it matters (the hook, not a summary), carrying its own links (more than one is good;
they need not point at the card target). ONE canonical teaser per page, reused wherever it is carded: check the teaser column first and
reuse; return every teaser you author in your final report.

MDX safety (.md and .mdx compile through MDX with the SAME rules):
* No bare { or } in card text (it is code inside JSX).
* camelCase attributes: className, strokeWidth, strokeLinecap, loading.
* Apostrophes as &apos;; use &mdash; &ndash; &rarr; rather than raw punctuation; quotes in alt as &quot;. But NEVER double-escape:
  {CARD_INDEX_CSV} values are already escaped (a blanket & -> &amp; yields &amp;quot; shown as literal text); copy them through unchanged.
* JSX comments and JSX card markup in both extensions. The verifier compiles through the real plugin chain ({SITE_DIR}/_ck_mdxcheck.mjs,
  remark-gfm only).


============================
STAGE 5 - BUILD THE TWO INTERESTING BLOCKS
============================

Interesting In This Area:
* Actually read the pages of this Level 2 first (in a large area: the overview plus {CARD_INDEX_CSV} descriptions, then in full the ones
  you will link).
* Exactly {SENTENCES_PER_INTERESTING_BLOCK} sentences as bullets, each {MAX_SENTENCE_WORDS} words or fewer (count them).
* Hyperlink as many phrases as a sentence carries; two or three links per sentence is the target.
* Every link's level2_parent equals this page's; never link the page itself.
* Each sentence reveals something new. "Learn more about X" is wasted; "A deputy detail appears only in the indictment, never in the
  affidavit" is a sentence.

Interesting In Other Areas: same rules, inverted (every link's level2_parent is NOT this page's), reaching at least three different Level 2s
across the four sentences. This block matters most: it carries readers between investigation threads.

Headings:
  ## Interesting In This Area
  ## Interesting In Other Areas
Never rename or absorb the existing lower "## Interesting" three-bullet block.


============================
STAGE 6 - SECTION HEADINGS FOR THE TWO GRIDS
============================

* Block 3: "## Other Pages In This Section". Keep an existing section-specific override (the Discord pilot uses "## Other Parts of the
  Discord Messages"); don't invent new ones casually.
* Block 4: "## Elsewhere In The Investigation"


============================
STAGE 7 - VERIFY BEFORE REPORTING DONE
============================

Every agent runs {CHECK_PY} on its edited files and reports counts. It checks:
* MDX compiles. From {SITE_DIR}, with @mdx-js/mdx resolvable:

    node -e "import('@mdx-js/mdx').then(async m=>{const fs=require('fs');
      for (const f of process.argv.slice(1)) {
        let s=fs.readFileSync(f,'utf8').replace(/^---\n[\s\S]*?\n---\n/,'');
        try { await m.compile(s) } catch(e){ console.log('FAIL',f,e.message) } }
    })" <files>

  One unescaped brace fails the GitHub Pages build and the live site silently keeps serving the old version. Never skip it.
* Every internal link in a new block resolves against {ROUTES_TXT}.
* Every embedded image is git-tracked and not ignored: python3 image_planning/generator/audit_image_publication.py (exit 0 clean).
  KNOWN PRE-EXISTING FAILURE (image pipeline's, not this pass's): Panguitch_Timeline_Infographic.jpg, sha 660c477be659. {IMAGES_YAML} has
  the 9 MB original under images/ and a 929 KB copy served from site/internals/static/img/Panguitch_Timeline_Infographic.jpg under another
  sha; the audit reports the original NOT SERVED though nothing references it. Report it, leave it, read the audit as clean if it is the
  only failure.
* Each START marker at most once per file with its matching END.
* PLACEMENT: the block run sits ABOVE every trailing-apparatus marker (author credit, the page's own "## Interesting", "## Related Areas",
  the placed-images gallery, "## Sources"). Resolve the anchor by POSITION using the anchor column of {CARD_INDEX_CSV}, never by reading the
  six-anchor list as a priority order (an earlier verifier accepted any position; 111 pages had to be relocated).
* No page cards itself; no four square repeats a target.
* No .mdx contains a raw <!-- and no .md contains a raw {/*.
* Interesting sentences within {MAX_SENTENCE_WORDS} words.
DONE only when a page passes everything. A failing page is rolled back to its pre-edit state and reported FAILED with the reason. No partial state.


============================
STAGE 8 - COORDINATOR MERGE AND REPORT
============================

After each wave:
* Merge agent ledger rows, teasers and new {PAGES_CSV} rows, one write each (keep the 15-column schema and existing quoting).
* Refresh line_count for every edited page.
* Re-run the link check site-wide (block 4 crosses agent boundaries).
* Print the wave progress line.

After the final wave, output to stdout:

    ============================================================
    FOUR SQUARES PASS COMPLETE
    ============================================================
    pages walked          : N
    pages edited          : N
    pages skipped         : N   (image/video leaves, generated, root index)
    rows added to CSV     : N
    rows orphaned         : N   (file_path no longer on disk - REVIEW THESE)
    cards emitted         : N
    banned media avoided  : N
    MDX compile failures  : N
    unresolved links      : N
    untracked images      : N
    ============================================================

* Any non-zero on the last three lines is a failure: fix it, don't report done.


============================
DEFAMATION AND ACCURACY
============================

All output is public and bound by the defamation rules in {ROOT_DIR}/claude.md.
* Never state as fact that a living person committed a crime unless convicted; attribute ("according to", "reportedly", "allegedly").
* A card teaser is the most quotable text on the site, where an unattributed accusation does the most damage.
* Never write "hand off" or wording implying a deliberate transfer; use "the table and Charlie" or "the security team reaching Charlie".
* The state's narrative is a rifle round; the majority citizen finding on X is an explosive device. Text may state the government narrative
  as the government's, never as dominant or settled. Never raise electrocution.


============================
CONVERGENCE PRIORITY
============================

If context runs short, complete in this order and stop cleanly:
  1. Block 3 (highest value, easiest to get right).  2. Block 2 (strongest cross-section linker).  3. Block 4.  4. Block 1.
A page has a complete, marker-fenced block or none of it. Stopping beats guessing: an agent that cannot verify a page leaves it untouched and says so.
