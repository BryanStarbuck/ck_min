FOUR SQUARES - AGENT BRIEF
==========================

You are one of 12 agents executing ~/BGit/Bryan_git/charlie-kirk/prompts/p_4_squares.md.
Work at high effort. Read that prompt first; this brief is the operational summary.

ROOT is ~/BGit/Bryan_git/charlie-kirk. All paths below are relative to it.

READ THESE FIRST, IN THIS ORDER
  1. prompts/p_4_squares.md              the full spec
  2. prompts/four_squares/GOLDEN_EXAMPLE.mdx   the verified output shape - copy it
  3. prompts/Assess_Manual.md            writing and layout guide (skim; it is long)
  4. claude.md sections "Pages CSV" and "Images Are Tracked In Git"

YOUR INPUTS (already built - never rebuild them)
  prompts/four_squares/card_index.csv    one row per editable page: url_path, file_path,
                                         extension, level, level2, is_overview, title,
                                         sidebar_label, description, media_kind, media_src,
                                         media_cid, media_alt, media_shape, banned, anchor, teaser
  prompts/four_squares/routes.txt        every valid public route, one per line
  prompts/four_squares/ledger.csv        file_path, level2, status, blocks, agent, updated
  prompts/four_squares/verify_blocks.py  the Stage 7 verifier

media_src, media_cid, media_alt and media_shape are ALREADY CORRECT. Use them verbatim.
They have been measured with sips, checked against the ban lists, and checked for git
tracking. Do NOT re-derive them, do NOT invent a src, do NOT use an ipfs.io or dweb.link
URL for a card image. media_kind "none" means emit a thumb-less card.

WHAT YOU DO, PER PAGE
  1. Read the page.
  2. Pick 4 sister pages in its own level2 by the index offsets (i+1, i+7, i+13, i+19) mod N
     over that level2 sorted by url_path. Overview/hub pages instead get the 4 best pages
     in their section, chosen on merit. Never card the page itself. Never card a duplicate.
  3. Pick 4 pages from 4 DIFFERENT other level2 areas, on genuine relevance. Read each
     candidate before carding it. Never card anything under /Photos or /Videos.
  4. Write the four blocks and insert them together, immediately ABOVE the anchor named in
     the anchor column of card_index.csv, one blank line each side.
  5. Run the verifier on the file. If it fails, fix it or revert the page. Never leave a
     half-written block.

BLOCK ORDER ON THE PAGE
  Interesting In This Area  ->  Interesting In Other Areas  ->  Other Pages In This Section
  ->  Elsewhere In The Investigation  ->  the anchor line

NOT EVERY FILE UNDER site/docs IS A PAGE. The docs plugin excludes **/_*/**,
**/_*.md, **/p_*.md, **/prompts/**, **/CLAUDE.md. Those files are unreachable for
visitors - never edit them, never card them. card_index.csv already omits them, so
if a path is not in card_index.csv it is not a page. A previous wave wasted work on
nine such files.

MARKERS - ALWAYS {/* NAME */}, in .md as well as .mdx. An HTML comment <!-- -->
is a hard MDX compile error in BOTH and takes the whole site's deploy down with it. Getting this wrong breaks the
whole site deploy. Strip any existing block with the same marker before writing a new one.
28 pages under site/docs/Tyler_Robinson/discord already have a CK_4SQ_SECTION block; keep it
and add the other three.

WRITING RULES
  * Interesting bullets: exactly 4, each 17 words or fewer after stripping link markup,
    2-3 markdown links per bullet where the sentence can carry them. Each bullet reveals a
    fact, never "learn more about X". In-area block links only inside this level2; other-area
    block links only outside it, reaching 3+ distinct areas.
  * Card teaser: 2-3 sentences, the hook not a summary. Links inside a teaser must be raw
    HTML anchors <a href="/x">y</a>, never markdown. One canonical teaser per page, reused
    everywhere that page is carded. Check the teaser column of card_index.csv FIRST and reuse
    what is there. Append every teaser you author to your own file
        prompts/four_squares/teasers/agent_N.tsv        (url_path <TAB> teaser, one per line)
    That file is yours alone - it is the one file outside your areas you may write. The
    coordinator merges it into card_index.csv. Do not print the teaser list in your report.

SCRATCH FILES - all 12 agents share one scratchpad directory and WILL overwrite each other.
Namespace every scratch file you create with your agent number, e.g. scratchpad/agent_N/...,
or work under /tmp/fsq_agent_N/. A sibling agent clobbering your working file mid-run has
already happened once.
  * JSX safety: no bare { or }, camelCase attributes, &apos; &mdash; &ndash; &rarr;, &quot;
    inside alt text.
  * DO NOT re-escape card_index.csv values. media_alt, title and teaser already
    contain HTML entities. A blanket & -> &amp; pass turns &quot; into &amp;quot;,
    which renders as a literal "&quot;" on the page. 117 of those shipped before
    this was caught. Escape only bare ampersands, or simply copy the CSV value
    through unchanged - which is what it is there for.

DEFAMATION - this is public content.
  * Never state as fact that a living person committed a crime. Attribute: reportedly,
    allegedly, according to.
  * Never write "hand off" - use "the table and Charlie" or "the security team reaching Charlie".
  * The rifle account is the government's narrative and must be labelled as such; the majority
    citizen finding on X is an explosive device. Do not present the rifle account as settled.
    Do not raise electrocution.

HARD LIMITS
  * Edit ONLY files inside your assigned directories. Read anything.
  * Never write Charlie_Kirk.txt, site/sidebars.ts, pages.csv, ledger.csv or card_index.csv.
    The coordinator is the single writer for those. Return your data instead.
  * Never touch .gitignore. Never git add -f. Never commit.

BATCH FILE - read prompts/four_squares/batches/agent_N.txt ONCE, at the start, and
work from that list. Never re-expand it later in the run (no $(cat ...) in your
verifier command); the coordinator may re-deal batch files between waves and you
would then verify the wrong files. Pass your own explicit file list to the verifier.

VERIFY, THEN REPORT
  python3 prompts/four_squares/verify_blocks.py <every file you edited>
  Must print "0 failing". Then report back, compactly:
    pages done      : list of file_path
    pages skipped   : file_path + one-line reason
    cards emitted   : N
    teasers authored: url_path <TAB> teaser text   (one per line, for pages you carded)
    verifier         : the final line of its output
  Do not paste page content back. Do not paste the blocks you wrote.
