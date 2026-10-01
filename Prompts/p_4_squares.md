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

Read {ASSESS_MANUAL} into the context window before editing any page.
Read the "Pages CSV" and "Images Are Tracked In Git" sections of {ROOT_DIR}/claude.md too.


============================
GOAL
============================

Walk EVERY page under EVERY directory under {DOCS_DIR}, recursively, and give
each one four new blocks that carry a reader sideways into the rest of the site
instead of dead-ending them at the bottom of an article.

Scope is the whole site, not a sample. At the time this prompt was last revised
that is roughly 1,758 editable pages spread across roughly 73 Level 2 areas.
Every one of them gets upgraded. The run is resumable: it is expected to take
many waves of agents, and a wave that stops early is not a failure so long as
the ledger records exactly what is done and what is not.

The four blocks, in this order, all placed at the same anchor point:

  1. Interesting In This Area      four short sentences, densely hyperlinked,
                                   every link inside the page's own Level 2.
  2. Interesting In Other Areas    four short sentences, densely hyperlinked,
                                   every link in some OTHER Level 2.
  3. Four squares - in this area   2x2 grid of four sister-page cards, all four
                                   sisters inside the page's own Level 2.
  4. Four squares - other areas    2x2 grid of four sister-page cards, each card
                                   in a DIFFERENT Level 2, none of them the
                                   page's own.

A "four square" is two rows by two columns. Each square carries the sister
page's own hero image or video, two or three sentences saying what is in it and
why it matters, and a chevron button through to that page. Solid background
colour, white text, not large.

The working pilot for all of this is {PILOT_DIR}. Every page there already
carries one four-square block. Open two or three of those files and copy the
markup exactly rather than inventing a new shape.


============================
WHAT ALREADY EXISTS - DO NOT REBUILD IT
============================

* The CSS is already written and shipped. It lives in {CSS_FILE} between the
  markers CK_FOUR_SQUARE_START and CK_FOUR_SQUARE_END. Class names:

    .ck-4sq          the 2x2 grid wrapper, collapses to one column below 996px
    .ck-4sq-card     one square. Solid #0d2b6b panel, white text
    .ck-4sq-side     card modifier: media left, text to its right
    .ck-4sq-stack    card modifier: media on top, text underneath
    .ck-4sq-thumb    the media anchor
    .ck-4sq-body     the text side
    .ck-4sq-title    sister page title, links to it
    .ck-4sq-text     the two or three sentences, may contain its own links
    .ck-4sq-btn      the white chevron button

  Do not add new CSS. If a genuinely new shape is needed, add it inside those
  same markers and say so in the run report.

* {PILOT_DIR} is the reference implementation of block 3. Its 28 pages already
  carry a CK_4SQ_SECTION block. Leave those in place; they still need blocks
  1, 2 and 4.

* {WORK_DIR} holds the machine-built inputs for this run - the card index, the
  ledger, the route set and the two helper scripts. Build them once in Stage 0
  and reuse them on every later wave. They are throwaway working files, not
  site content.


============================
HARD PROHIBITIONS
============================

* NEVER write to ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt. Read only. See {ROOT_DIR}/claude.md.
* NEVER touch {SITE_DIR}/sidebars.ts. Not to add a page, not to reorder one.
* NEVER edit anything outside {DOCS_DIR} except {PAGES_CSV} and {WORK_DIR}.
* NEVER use an HTML comment in a .mdx file. A raw <!-- --> compiles locally and
  fails the GitHub Pages MDX build, and the live site then silently keeps
  serving the previous version for days. Use the JSX comment form in .mdx and
  the HTML form only in .md.
* NEVER add a per-file image line to {ROOT_DIR}/.gitignore and never reach for
  git add -f. If Large File Bridge has re-appended those lines, delete them.
* Do not commit. The repo has an external auto-commit sweeper; leave the working
  tree for it.


============================
BLOCK MARKERS
============================

Every generated block is fenced by comment markers so a re-run replaces it in
place instead of stacking duplicates. Canonical names:

  CK_INTERESTING_HERE_START   ... CK_INTERESTING_HERE_END
  CK_INTERESTING_OTHER_START  ... CK_INTERESTING_OTHER_END
  CK_4SQ_SECTION_START        ... CK_4SQ_SECTION_END
  CK_4SQ_SITEWIDE_START       ... CK_4SQ_SITEWIDE_END

In EVERY file, .mdx and .md alike, each marker is written

    {/* CK_4SQ_SECTION_START */}

NEVER write an HTML comment. Do NOT write <!-- CK_4SQ_SECTION_START --> in a .md
file. This site's docusaurus.config.ts sets no markdown.format override, so
Docusaurus 3 compiles .md through the MDX loader exactly like .mdx, and a bare
<!-- is a hard MDX parse error: "Unexpected character `!` (U+0021) before name".
One such marker fails `npm run build`, which fails the Pages workflow, which
leaves the ENTIRE live site frozen on its last good commit. On 2026-08-19 this
put <!-- markers into 43 .md files under site/docs/laws/ and silently blocked
every deploy until they were converted back.

Rules:

* On every run, strip any existing block with these markers FIRST, then write
  the new one. Never nest, never append a second copy. When stripping, match
  BOTH the {/* */} and the legacy <!-- --> form, so old files get repaired.
* The marker form does not vary by extension. {/* */} everywhere.
* Text outside the markers is never touched. Existing prose, existing tables,
  existing "## Interesting" bullet lists, existing "## Related Areas" grids and
  existing "## Images" galleries all survive unchanged.


============================
WHERE THE BLOCKS GO ON THE PAGE
============================

Insert all four blocks together, in the order listed under GOAL, at the FIRST
of these anchors that appears in the file:

  1. {/* CK_AUTHOR_CREDIT */}          (present on most pages - the usual case)
  2. a line that is exactly   ## Interesting
  3. a line that is exactly   ## Related Areas
  4. {/* CK_PLACED_IMAGES_START
  5. a "## Sources" or "## Fix Laws" or "## The Laws" heading
  6. end of file

Insert ABOVE the anchor line, never below it, and leave one blank line on each
side of the inserted run.

So the running order down a finished page is:

  frontmatter
  back button
  H1
  hero media
  the page's own prose
  Interesting In This Area
  Interesting In Other Areas
  Other Pages In This Section          (four squares, same Level 2)
  Elsewhere In The Investigation       (four squares, other Level 2s)
  author credit
  Interesting                          (the old three-bullet block, if present)
  Related Areas
  Images

The blocks sit BELOW the page's own argument and ABOVE the laws, the credits,
the related-areas grid and the image gallery. A reader who has finished the
article meets them; a reader still reading the article does not.


============================
STAGE 0 - BUILD THE MACHINE INPUTS ONCE
============================

Do this once, before any agent is launched. It is deterministic work and no
agent should ever redo it by hand. Everything here is mechanical extraction;
the agents are then free to spend their whole context on judgement and prose.

* mkdir -p {WORK_DIR}

* Write {BUILD_INDEX_PY} and run it. It walks {DOCS_DIR} recursively and emits
  {CARD_INDEX_CSV}, one row per editable page, with these columns:

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

  Rules the script must follow, because getting these wrong is what produces a
  broken live site:

  * media_src is ALWAYS the local repo path /img/evidence/<sha256>.jpg. Never an
    ipfs.io or dweb.link URL for an image. Most CIDs in {IMAGES_YAML} were made
    with "ipfs add -n" and sit on no node, so the gateway 504s for real visitors
    while rendering perfectly on the machine that holds the file. The CID stays
    in data-cid as provenance only. Videos are the exception and keep their
    gateway src, copied verbatim from the sister page.
  * media_shape comes from the file's REAL pixel dimensions, measured, never
    guessed:  sips -g pixelWidth -g pixelHeight {EVIDENCE_DIR}/<sha>.jpg
      ratio = pixelWidth / pixelHeight
      ratio <  1.0   portrait   -> ck-4sq-side   media left, text to its RIGHT
      ratio >= 1.0   landscape  -> ck-4sq-stack  media on top, text UNDERNEATH
    Measure every distinct sha once and cache it; there are about 2,000 files
    and re-measuring per card is wasted time.
  * banned is the UNION of {BAN_IMAGES_CSV}, {BAN_VIDEOS_CSV},
    image_planning/exclude_images.txt and videos_planning/exclude_videos.txt,
    matched on sha256 first, then cid, then file_path.
  * A media file that fails either of these is treated as media_kind none:
        git ls-files --error-unmatch <path>    must succeed
        git check-ignore -v <path>             must produce nothing
    An image that exists on disk but is untracked or ignored renders in local
    dev and 404s for every real visitor.

* Emit {ROUTES_TXT} from {SITE_DIR}/build/**/*.html - the pages a visitor
  actually receives - using build_routes.py. Do NOT derive routes from source
  filenames. That was tried and it shipped 76 dead links across 59 pages,
  because filename-derived routes get two things wrong:
    * a leading year is not a Docusaurus number prefix. The built route is
      /court/Days_in_Court/2026-03-10-seal-motion, not /...(/03-10-seal-motion).
      Same class of bug produced /Timeline/23-shooting-time for
      /Timeline/12-23-shooting-time and /Planes/0004-Vance for /Planes/99-0004-Vance.
    * frontmatter id: or slug: overrides the filename outright, so
      court/mirandize/overview.md serves /court/mirandize/mirandize-overview.
  Some routes contain spaces and parentheses ("/Topics3/Suspects (List)/overview"),
  so read the file with splitlines(), never split() - whitespace-splitting
  shreds those routes and makes every link to them look broken.
  If {SITE_DIR}/build is stale or missing, keep the previous routes.txt rather
  than regenerating from filenames. Do NOT run npm run build just to check
  links; it takes twenty minutes.

  routes.txt is OWNED by build_routes.py. build_card_index.py must never write
  it - it did once, silently replacing the build-derived file with a
  filename-derived one and reintroducing every error listed above. It now writes
  routes_derived.txt instead, purely so the two can be diffed.

  Docusaurus strips a numeric prefix from DIRECTORY segments as well as from
  file names (laws/2_US_Intel/... serves /laws/US_Intel/...), but leaves years
  and some numbers alone. Do not try to reimplement that rule - resolve every
  source file against the built route set instead.

  KNOWN UNROUTABLE SOURCE PAGE: site/docs/TPUSA/TPUSA.mdx. It exists in source
  but the build serves no /TPUSA/TPUSA route - the name collides with the TPUSA
  directory. Link to /TPUSA/overview instead. Flagged for a human decision;
  nothing in this pass should card or link it.

* Emit {LEDGER_CSV}: one row per editable page, columns

    file_path,level2,status,blocks,agent,updated

  status starts as TODO. blocks is the four-letter state HOSW, one letter per
  block written: H=interesting-here, O=interesting-other, S=section 4sq,
  W=sitewide 4sq, a dash for not yet. A page is DONE only at HOSW.

* Write {CHECK_PY}, the verifier used in Stage 7, so all twelve agents check
  their work the same way instead of each inventing a check.


============================
BUILT TOOLING - STAGE 0 OUTPUT
============================

Stage 0 has been run and its output is committed to {WORK_DIR}. Later runs reuse
it; rebuild it only when the site has changed materially.

  build_card_index.py   builds card_index.csv, routes.txt, ledger.csv, shape_cache.json
                        Rebuild is idempotent: it carries the teaser column and
                        the ledger status/agent columns forward. That merge MUST
                        happen before the first file is written - when it ran
                        after, a rebuild silently blanked all 892 teasers and the
                        next wave started authoring competing ones.
  verify_blocks.py      the Stage 7 verifier, run per file
  merge_wave.py         the Stage 8 coordinator merge - reads the SITE as ground
                        truth rather than trusting an agent's report, rewrites the
                        ledger, refreshes pages.csv line_count, and deals the next
                        wave's batches into batches/agent_N.txt
  check_site.sh         runs the verifier across every page carrying a block
  AGENT_BRIEF.md        the operating summary handed to each of the 12 agents
  GOLDEN_EXAMPLE.mdx    a verified four-block page, copied rather than reinvented
  agent_buckets.json    the stable area-to-agent assignment
  batches/agent_N.txt   the current wave's 20 pages for agent N

Two facts the index builder had to get right, both learned the hard way:

  * A video hero cannot be a card thumb. A card thumb is an <img>, and an .mp4
    gateway URL inside an <img> is a broken image. Video heroes are resolved to
    their poster still under /img/video_posters/, via the poster attribute or via
    cid -> sha256 in {VIDEOS_YAML}. If no poster exists the page counts as having
    no media and gets a thumb-less card.
  * A page's hero is the first image ABOVE the generated blocks. Images inside a
    CK_4SQ block belong to OTHER pages and must never be harvested as this page's
    hero. Images inside a CK_PLACED_IMAGES block are a legitimate fallback when
    the page has no floated hero.

Current shape of the work: 1,755 editable pages, 73 Level 2 areas, 812 pages with
usable media and 943 without.

============================
STAGE 1 - LOAD THE MAP
============================

* Read {PAGES_CSV}. Columns are defined in {ROOT_DIR}/claude.md. The ones this
  prompt uses: page_key, level, level2_parent, page_type, url_path, file_path,
  title, sidebar_label, description.

* Reconcile disk against {PAGES_CSV}:
  * A file on disk with no row in {PAGES_CSV} gets a row added. Derive
    page_key (four words maximum, underscores, no special characters, unique),
    parent_key (the overview page of its directory), level, level2_parent,
    level2_section, page_type, url_path, file_path, title, sidebar_label,
    directory, extension, has_frontmatter, line_count and description.
  * A row in {PAGES_CSV} whose file_path no longer exists is reported, not
    deleted. Deleting rows is a human decision.
  * Do not renumber or re-key existing rows.
  * The CSV is known to carry duplicate rows written by an external process.
    Do not dedupe it as a side effect of this run; report the count.

* Level 2 of a page = its level2_parent column. Every page has exactly one.
  A page whose own level is 2 is its own Level 2.

* Skip as edit targets, but keep as link targets:
  * page_type of image or video - the generated /Photos and /Videos leaf pages.
    That is about 3,014 of the 4,772 files on disk and is the single biggest
    reason the real workload is 1,758 pages and not 4,772.
  * The site root index page.
  * Any CLAUDE.md file. It is instructions to an AI, not a page.
  * Any page under a directory owned by a generator, unless the generator's own
    prompt says otherwise. Check for a "generated by" comment at the top.

  laws/README.md IS a published page and is in scope.

* THE SITE'S OWN EXCLUDE LIST IS THE AUTHORITY ON WHAT IS A PAGE. The docs
  plugin in {SITE_DIR}/docusaurus.config.ts excludes:

      **/_*.{js,jsx,ts,tsx,md,mdx}     underscore-prefixed files
      **/_*/**                          anything under an underscore directory
      **/*.test.{js,jsx,ts,tsx}
      **/__tests__/**
      **/prompts/**
      **/CLAUDE.md
      **/p_*.{md,mdx}                   prompt files living inside docs

  A file matching any of those is NOT published and must never be edited or
  carded. On the first run this was missed and nine files were edited that no
  visitor can reach - After/house/p_research.md and the eight
  Consciousness_Control/_research/*.md staging notes. They were reverted. The
  index builder now mirrors this list, which is why the editable count is 1,731
  rather than 1,762.


============================
STAGE 2 - PARTITION THE WORK ACROSS {AGENT_COUNT} AGENTS
============================

* Count pages per Level 2 area using EDITABLE pages only. Photos and Videos
  hold thousands of leaf pages and would otherwise swamp the partition; they
  are not edit targets and count as zero.
* Sort the areas by editable page count, largest first.
* Deal them round-robin into {AGENT_COUNT} buckets, so the biggest areas land in
  different buckets and total page counts come out roughly even.
* A directory is never split across two agents. An agent owns whole Level 2
  areas including everything nested inside them. Ownership is stable across
  waves: the same agent number always owns the same areas, so its teasers and
  its rotation stay consistent.
* Root-level loose pages (files directly in {DOCS_DIR}) go to the agent with the
  smallest bucket.
* Launch all {AGENT_COUNT} agents in ONE message so they run concurrently, each
  at effort {EFFORT}.

Each agent receives:
  * its list of owned directories
  * its batch: the first {BATCH_SIZE} pages in its bucket whose ledger status is
    still TODO
  * {CARD_INDEX_CSV}, {ROUTES_TXT} and {LEDGER_CSV} as its inputs
  * this prompt

Each agent may edit ONLY files inside its own directories. Every agent may READ
any page anywhere.

{PAGES_CSV} is written by ONE writer. Agents do not write to it. Each agent
returns its new-row and missing-row findings as data, and the coordinator merges
them into {PAGES_CSV} once, after all agents finish.

{LEDGER_CSV} and {CARD_INDEX_CSV} are also single-writer. An agent returns its
completed rows and its teasers as data in its final report; the coordinator
merges. Twelve concurrent writers to one CSV lose rows.


============================
STAGE 2B - WAVES
============================

One wave is: launch {AGENT_COUNT} agents, each takes {BATCH_SIZE} pages, all
report, the coordinator merges the ledger, the card index teasers and the
pages.csv rows, then prints a progress line.

* Run waves until every ledger row is DONE. At {AGENT_COUNT} x {BATCH_SIZE} that
  is 240 pages a wave and roughly eight waves for the whole site.
* An agent that runs short of context stops cleanly on a page boundary and
  reports which pages it finished. It never leaves a half-written block.
* Between waves the coordinator prints:

    wave N complete - pages done X of Y (Z%) - failures F

* A wave with a non-zero MDX compile failure count is fixed before the next wave
  is launched. A broken .mdx page stops the whole site from deploying, so the
  cost of carrying one forward is the entire run.


============================
STAGE 3 - PICK THE SISTER PAGES
============================

For the in-this-area four square (block 3):

* The candidate pool is every editable page sharing this page's level2_parent,
  minus the page itself.
* Order the pool in a stable thematic sequence - the order the section's own
  overview page lists them in, if it lists them. Otherwise alphabetical by
  url_path.
* For the page at index i in a pool of size N, take indexes
  (i+1), (i+7), (i+13), (i+19) modulo N.
  * This spreads the picks across the section and, when N is coprime with the
    offsets, gives every page in the section the same number of inbound cards.
  * If N is small the offsets collide. Deduplicate, then fill from the nearest
    unused index.
  * If N is 5 or fewer, use every other page in the section and stop. Do not
    pad the grid with repeats and do not reach outside the section.
  * If the section holds only TWO editable pages there is exactly one sister,
    and a single card in a two-column grid reads as broken. Omit block 3
    entirely on those pages and carry the one in-area link in the block 1
    bullets instead. A Level 2 of one page has no in-area block at all.
    Expected block sets by section size: 1 page "-O-W", 2 pages "HO-W",
    3 or more "HOSW".
  * If the offset lands on a page whose media is banned, or on a CLAUDE.md, step
    to the next unused index rather than dropping the card.
* An overview or hub page does not have to follow the offsets. Give it the four
  most important pages in its own section instead, chosen on merit.
* A page never cards itself.

For the other-areas four square (block 4):

* Pick four pages from four DIFFERENT Level 2 areas, none of them this page's
  own Level 2. Four cards, four distinct level2_parent values.
* Choose on genuine relevance, not proximity: the page that a reader of THIS
  page would most want next from that area. Read the candidate before carding it.
* Prefer Level 3 pages with real substance and their own hero media over thin
  stubs and over Level 2 overview pages.
* Vary the four areas across the pages within one section, so a whole section
  does not point at the same four outside pages. Rotate: page i in the section
  starts its area sweep at position (i * 4) in the area list.
* Never card a page in /Photos or /Videos. Those are generated image and video
  leaves; they are link targets from prose, not destinations for a card.


============================
STAGE 4 - BUILD ONE CARD
============================

Media:

* The card uses the sister page's own hero media, already extracted into
  {CARD_INDEX_CSV}. Reuse media_src, media_cid, media_alt and media_shape
  verbatim from that row. Do not re-derive them by hand and do not invent a src.
* Add loading="lazy".
* If media_kind is none, emit the card with the .ck-4sq-stack shape and no
  thumb. About 968 of the 1,758 pages have no media of their own, so a
  thumb-less card is normal, not an error. Never emit a broken img.
* If banned is yes, pick a different sister. Never card banned media.

Markup - copy this exactly, substituting the values:

<div className="ck-4sq-card ck-4sq-side">
  <a className="ck-4sq-thumb" href="{url}"><img src="{src}" data-cid="{cid}" alt="{alt}" loading="lazy" /></a>
  <div className="ck-4sq-body">
    <p className="ck-4sq-title"><a href="{url}">{title}</a></p>
    <p className="ck-4sq-text">{two or three sentences, with links}</p>
    <a className="ck-4sq-btn" href="{url}">Read this <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M9 6l6 6-6 6" /></svg></a>
  </div>
</div>

The thumb-less variant drops the whole first <a> line and keeps everything else.

Four of those go inside one <div className="ck-4sq"> ... </div>.

Text:

* Two or three sentences. What is in it, and why it matters. Not a summary of
  the whole page - the hook.
* The text may and should carry its own hyperlinks out to other pages. More than
  one is good. They do not have to point at the card's own target.
* Write ONE canonical teaser per page and reuse it everywhere that page is
  carded, so the same page reads the same way across the site. The teaser lives
  in the teaser column of {CARD_INDEX_CSV}. Before writing a new one, check
  whether the row already has one and reuse it. Return every teaser you author
  in your final report so the coordinator can write it back.

MDX safety:
* Inside JSX, a bare { or } is code. Never put one in card text.
* Write attributes camelCase: className, strokeWidth, strokeLinecap, loading.
* Escape a literal apostrophe in JSX text as &apos; and use &mdash; &ndash;
  &rarr; rather than raw punctuation.
* Quote marks inside an alt attribute become &quot;. But NEVER double-escape:
  values coming out of {CARD_INDEX_CSV} are already escaped, so a blanket
  & -> &amp; pass over them produces &amp;quot; and the page shows the entity as
  literal text. Copy those columns through unchanged.
* .md and .mdx BOTH compile through MDX here, with the SAME rules. A stray brace
  or an HTML comment breaks a .md page exactly as it breaks an .mdx page. Use
  JSX comments and JSX card markup in both. The verifier compiles both through
  the real build's plugin chain ({SITE_DIR}/_ck_mdxcheck.mjs, remark-gfm only).


============================
STAGE 5 - BUILD THE TWO INTERESTING BLOCKS
============================

Both blocks have the same shape. They differ only in where the links point.

Interesting In This Area:

* Read every page in this page's Level 2 first. Actually read them - the point
  is to know what is in that area, not to restate the sidebar. In a large area
  read the overview plus the descriptions in {CARD_INDEX_CSV}, then read in full
  the handful you are about to link.
* Write exactly {SENTENCES_PER_INTERESTING_BLOCK} sentences as a bullet list.
* Each sentence is {MAX_SENTENCE_WORDS} words or fewer. Count them.
* Hyperlink as many phrases as the sentence will carry. Two or three links in
  one sentence is the target, not the exception. The phrase carries the meaning
  and the link carries the reader.
* Every link points at a page whose level2_parent equals this page's.
* Never link to the page itself.
* Each sentence should reveal something a reader did not know from this page.
  "Learn more about X" is a wasted sentence. "A deputy detail appears only in
  the indictment, never in the affidavit" is a sentence.

Interesting In Other Areas:

* Same rules, one inversion: every link points at a page whose level2_parent is
  NOT this page's.
* Across the four sentences, reach at least three different Level 2 areas.
* This block matters most. It is how a reader crosses from one investigation
  thread to another.

Heading text:

  ## Interesting In This Area
  ## Interesting In Other Areas

Do not rename or absorb the existing "## Interesting" three-bullet block that
some pages already carry lower down. It stays where it is.


============================
STAGE 6 - SECTION HEADINGS FOR THE TWO GRIDS
============================

* Block 3 heading: "## Other Pages In This Section"
  * A section may override this with something truer to its own material. The
    Discord pilot uses "## Other Parts of the Discord Messages". Keep an
    override that already exists; do not invent new ones casually.
* Block 4 heading: "## Elsewhere In The Investigation"


============================
STAGE 7 - VERIFY BEFORE REPORTING DONE
============================

Every agent runs {CHECK_PY} on its own edited files and reports the counts. The
checker covers:

* MDX compiles. From {SITE_DIR}, with @mdx-js/mdx resolvable:

    node -e "import('@mdx-js/mdx').then(async m=>{const fs=require('fs');
      for (const f of process.argv.slice(1)) {
        let s=fs.readFileSync(f,'utf8').replace(/^---\n[\s\S]*?\n---\n/,'');
        try { await m.compile(s) } catch(e){ console.log('FAIL',f,e.message) } }
    })" <files>

  A single unescaped brace fails the whole GitHub Pages build and the live site
  silently keeps serving the previous version. Never skip this.

* Every internal link in a new block resolves against {ROUTES_TXT}.

* Every embedded image is git-tracked and not gitignored:

    python3 image_planning/generator/audit_image_publication.py

  Exit 0 is clean. If Large File Bridge has re-appended per-file image lines to
  {ROOT_DIR}/.gitignore, delete those lines. Never work around it with git add -f.

  KNOWN PRE-EXISTING FAILURE, not caused by this prompt and not to be "fixed" by
  it: Panguitch_Timeline_Infographic.jpg, sha 660c477be659. {IMAGES_YAML} carries
  TWO entries for this picture - the 9 MB original under images/ (sha 660c...) and
  a 929 KB compressed copy already served from
  site/internals/static/img/Panguitch_Timeline_Infographic.jpg under a different
  sha. The audit keys on sha, so it reports the original as NOT SERVED. The
  original is on no page and is referenced by nothing. This belongs to the image
  pipeline, not to the four-squares pass. Report it, leave it alone, and read the
  audit as clean when it is the only failure.

* No page carries a duplicate block. Each of the four START markers appears at
  most once per file, and each has its matching END.

* PLACEMENT is checked, not just validity. The block run must sit ABOVE every
  trailing-apparatus marker in the file - the author credit, the page's own
  "## Interesting" list, "## Related Areas", the placed-images gallery and
  "## Sources". For a long time the verifier accepted a run anywhere in the
  file, so blocks written below one of those passed silently; two agents hit it
  and self-corrected, and 111 pages had to be relocated afterwards. Resolve the
  anchor by POSITION using the anchor column of {CARD_INDEX_CSV}, never by
  reading the six-anchor list as a priority order.

* No page cards itself, and no four square contains the same target twice.

* No .mdx file contains a raw <!-- and no .md file contains a raw {/*.

* Sentence lengths in the Interesting blocks are within {MAX_SENTENCE_WORDS}.

An agent reports DONE for a page only when that page passes every check. A page
that fails is rolled back to its pre-edit state and reported as FAILED with the
reason. There is no partial state on a page.


============================
STAGE 8 - COORDINATOR MERGE AND REPORT
============================

After each wave:

* Merge every agent's ledger rows, teasers and new {PAGES_CSV} rows in one write
  each. Keep the 15-column schema and the existing quoting style.
* Refresh line_count for every page that was edited.
* Re-run the link check across the whole site, not just per agent, because
  block 4 crosses agent boundaries.
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

* Any non-zero on the last three lines is a failure. Fix it, do not report done.


============================
DEFAMATION AND ACCURACY
============================

Everything written by this prompt is public site content and is bound by the
defamation rules in {ROOT_DIR}/claude.md.

* Never state as fact that a living person committed a crime unless a court
  convicted them. Attribute: "according to", "reportedly", "allegedly".
* A card teaser is 25 words of the most quotable text on the site. It is
  exactly where an unattributed accusation does the most damage. Write it
  accordingly.
* Do not write "hand off" or similar wording implying a deliberate transfer.
  Use "the table and Charlie" or "the security team reaching Charlie".
* The state's narrative is that Charlie Kirk was killed by a rifle round. The
  majority citizen finding on X is that he died by an explosive device. Card
  text may state the government narrative as the government's narrative. It
  must not present it as the dominant or settled conclusion. Do not raise
  electrocution.


============================
CONVERGENCE PRIORITY
============================

If context runs short, complete in this order and stop cleanly rather than
leaving a half-written block on a page:

  1. Block 3, the in-this-area four square. It is the highest value and the
     easiest to get right.
  2. Block 2, Interesting In Other Areas. It is the strongest cross-section
     link generator on the site.
  3. Block 4, the other-areas four square.
  4. Block 1, Interesting In This Area.

A page either has a complete, marker-fenced block or none of that block. There
is no partial state.

Stopping is always better than guessing. An agent that cannot verify a page
leaves the page untouched and says so.
