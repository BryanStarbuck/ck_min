# Grok Twitter Research — Grow Every Public Page

This is an **executable runbook prompt**. When this file is run, the agent
system must **do the work** — not merely describe it.

**Core loop (every public page in pages.csv):**

```
pages.csv row
    → understand Level 2 + Level 3 (or deeper) topic
    → Grok AI + X/Twitter research (raw, not summarized)
    → save ~/T/_ck/grok/{Level2}/{Level3}_research.txt
    → grow the matching Docusaurus page under site/docs/
    → defamation-safe rewrite + Assess_Manual layout preserved
    → next row
```

Twelve agents partition `pages.csv` with **no overlap and no gaps**. Together
they cover every data row.

Do **not** invent a different workflow. Follow this file end-to-end.


====================================================================
0. ONE-SENTENCE MISSION
====================================================================

Use Grok/X research to **greatly grow** every public page on
WhoAssassinatedCharlieKirk.com with extensive citizen-investigator claims and
facts — written so a defamation attorney would still allow the page to publish.


====================================================================
1. PURPOSE (WHY THIS RUN EXISTS)
====================================================================

The public site is the Docusaurus site at:

  https://whoassassinatedcharliekirk.com

Repo public root:

  {ROOT_DIR}/site/docs/

### Who the audience is

Readers come here because they see clues that **Tyler Robinson is not the one
who decided Charlie Kirk would die** that day or at that location, and is not
a complete explanation of the cause of death. They see **intelligence-service
level** involvement (one or more services) as a live question. They do **not**
buy the narrative that a lone actor with a 30-06 bullet fully explains what
happened at Utah Valley University on September 10, 2025.

They want:

  * Documented claims, not vibes
  * What citizen investigators on **X / Twitter** are finding and posting
  * Timelines, who went where, who said what, when
  * Ballistics disputes, security failures, flights, censorship, court process
  * **All sides** of disputed issues — not only the government narrative
  * Enough detail that a careful reader can learn beyond the official story

This site documents as much of that as possible in a hierarchy (Level 2
sections → Level 3 topics → sometimes Level 4+).

### What this run does

For **every** public page row in pages.csv (Level 1 home, Level 2 overviews,
Level 3 topics/people, Level 4+ children — unless the runner filters):

  1. Run a **dedicated** Grok AI / X research query focused on that page's
     Level 2 area and especially its Level 3 (or deeper) topic.
  2. Save the **full raw** results to a temporary research text file.
  3. Integrate that research into the public MD/MDX page so the page **grows
     substantially** in information density.
  4. Write every new sentence under **defamation-safe** rules (attribute,
     allegedly/reportedly, quote the X speaker — never convert rumor into the
     site's own finding of criminal guilt against a living person).


====================================================================
2. VARIABLES AND PATHS
====================================================================

ROOT_DIR dir is ~/BGit/Bryan_git/charlie-kirk
  Git repo. Private research + public site live here.

SITE_DIR dir is {ROOT_DIR}/site
SITE_DOCS_DIR dir is {ROOT_DIR}/site/docs
  **Only** this tree is published. Only this tree is edited by default.

CK_FILE is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt
  (Real file. Moved 2026-09-19. ~/BGit/Bryan_git/charlie-kirk/Charlie_Kirk.txt is now a symlink to it —
   use that only to verify the location; always read and write the real path.)
  Master investigation file. Grows only — never delete or rewrite existing
  content. Section headers look like:

      =============== Section Title ==================

  Use it to ground queries and to pull additional facts/claims into pages
  when Grok returns thin results. It is private context, not a public page.

PAGES_CSV is file {ROOT_DIR}/pages.csv
  **Master read input.** One row = one public page. Current columns:

    page_key, parent_key, level, level2_parent, level2_section, page_type,
    url_path, file_path, title, sidebar_label, directory, extension,
    has_frontmatter, line_count, description

  Column meanings:

    page_key         Unique id (underscores, no special chars). Primary key.
    parent_key       Parent page_key (empty only for Home).
    level            1=Home, 2=section overview, 3=child/sub-overview, 4+=deeper.
    level2_parent    Owning Level 2 key when applicable.
    level2_section   Level 2 directory / section name (e.g. FBI, After, Planes).
    page_type        home | overview | topic | person | index | organization
    url_path         Public URL path (trailingSlash: false on this site).
    file_path        Path from repo root to .md / .mdx (authoritative location).
    title            Page title.
    sidebar_label    Sidebar label.
    directory        Parent dir under site/docs/.
    extension        md or mdx.
    has_frontmatter  yes/no.
    line_count       Lines in file (update after growth if practical).
    description      Short summary — **use heavily** when building Grok phrases.

ASSESS_MANUAL is file {ROOT_DIR}/prompts/Assess_Manual.md
  Layout and writing quality bar for every public page. **Read before editing.**

DEFAMATION_SKILL is file {ROOT_DIR}/skills_storage/ck_defemation_prevention.md
  Also: ~/.claude/commands/ck_defemation_prevention.md
  Defense-side media-attorney rules. **Read before editing.**

CLAUDE_MD is file {ROOT_DIR}/Claude.md
  (CLAUDE.md may also exist — same family of repo rules.)
  Public/private split, pages.csv maintenance, defamation, hierarchy.

RELATED_GROWTH_PROMPT is file {ROOT_DIR}/prompts/grok_write.mdx
  Sibling prompt for Level-2-focused growth with a 10-query Grok fan-out.
  This Twitter-research prompt is **page-row-driven** (pages.csv partitions)
  instead. Steal good linking/writing habits from grok_write.mdx; do not
  replace this runbook with it.

GROK_RESEARCH_ROOT dir is ~/T/_ck/grok
  Temporary research capture tree. Not published. Not committed unless asked.

  Per-page path:

    {GROK_RESEARCH_ROOT}/{LEVEL2_TOKEN}/{LEVEL3_TOKEN}_research.txt

  Examples:

    ~/T/_ck/grok/FBI/FBI_Investigation_research.txt
    ~/T/_ck/grok/After/Institutional_Resignations_research.txt
    ~/T/_ck/grok/Planes/N1098L_research.txt
    ~/T/_ck/grok/Home/index_research.txt
    ~/T/_ck/grok/After/overview_research.txt

NUM_AGENTS is integer **12**
  Exactly twelve parallel workers. Full coverage, zero overlap.

AGENT_ID is integer 1..12
  This worker's identity. Agent 1 = first partition; Agent 12 = last.

START_ROW / END_ROW
  Inclusive **1-based data-row** numbers (header excluded). Either computed
  from AGENT_ID (default) or passed by the human/orchestrator.

THE_DATE_TIME_STRING
  "{YYYYMMDD}_{HHMMSS}" style; only alphanumerics and underscores. Generate
  once per agent at start.

CHANGES_FILE is file {ROOT_DIR}/changes_grok_twitter_research.txt
  Run log. **Prepend** new blocks at the top (older history slides down).

AGENT_LOG is file {GROK_RESEARCH_ROOT}/_agent_{AGENT_ID}_log.txt
  Required per-agent TSV progress log (one line per row).

LOCK_DIR dir is {GROK_RESEARCH_ROOT}/_locks
  Optional mutex files when writing shared CHANGES_FILE (see PARALLELISM).

INPUT_TEXT (optional)
  Free-text instructions from the human when launching, e.g.:

    "Agent 3 of 12"
    "Only section FBI"
    "Rows 100-150"
    "Skip laws/ and Fix/disabled"
    "Re-research even if research file exists"
    "Dry-run research only (no page edits)"

  Honor INPUT_TEXT overrides when present.


====================================================================
3. READ FIRST (MANDATORY BEFORE ANY WORK)
====================================================================

Before partitioning, before any Grok call, before editing any page:

  1. Read **this entire prompt file**.
  2. Read **CK_FILE** — at minimum:
       * Scan all `=============== ... ==================` section titles
       * Deep-read sections relevant to your partition's Level 2 areas
         (Strange events, Timeline, Day of Shooting, Ballistics, FBI Cover up,
         Israel, N1098L, SAM Flight, Tyler Robinson, Court Case, Quotes, etc.)
  3. Read **ASSESS_MANUAL** fully enough to enforce Level 2 / Level 3 layout.
  4. Read **DEFAMATION_SKILL** fully enough to apply Interventions A–D and the
     attorney checklist.
  5. Read **CLAUDE_MD** public-layer + defamation + pages.csv rules.
  6. Load **PAGES_CSV** with a real CSV parser (quoted commas). Never split on
     commas with naive string split.

Private trees (`Details/`, `Research/`, `knowledge/`, `IPFS/`) may inform
judgment. **Default edit surface is only** `{SITE_DOCS_DIR}/**`.


====================================================================
4. SITE HIERARCHY (HOW PAGES RELATE)
====================================================================

* **Level 1 — Home** (`site/docs/index.mdx`)
  Landing + navigation hub. Grow carefully; do not destroy panel navigation.

* **Level 2 — Section overview** (usually `{Section}/overview.mdx`)
  Main section of the site. Reader orientation + **three-column TOC** of
  Level 3 children + three body paragraphs + Related Areas.
  Research: whole section. Integration: deepen the three paragraphs and
  Related Areas; **never replace** the TOC with a research dump.

* **Level 3 — Topic / person / index page** under a Level 2
  Focused investigation page. **Primary growth target.**
  Straight to substance; absolute back button; sub-headings; Related Areas.

* **Level 4+ — Nested children** (clusters, law subpages, hospital subtrees)
  Same writing rules as Level 3. Back button points to **immediate parent
  overview**, not always the top Level 2 if nesting is deeper — but if the
  page already has a working absolute back button, preserve its intent and
  only fix relative `href="../..."` bugs.

Mental model the audience uses:

  Level 2 = "which room of the investigation am I in?"
  Level 3 = "what specific claim-set am I reading?"


====================================================================
5. HOW TO LAUNCH (ORCHESTRATOR)
====================================================================

### 5.1 Preflight

  [ ] `test -f {PAGES_CSV} && test -f {CK_FILE} && test -d {SITE_DOCS_DIR}`
  [ ] Count data rows N with a CSV parser (exclude header)
  [ ] `mkdir -p {GROK_RESEARCH_ROOT} {LOCK_DIR}`
  [ ] Print N and the twelve partition ranges to stdout
  [ ] Confirm sum of partition sizes == N

### 5.2 Partition math (authoritative)

Let N = number of data rows (exclude header).
Let k = AGENT_ID - 1   # 0..11

```
start_index = floor(k * N / 12)          # 0-based inclusive
end_index   = floor((k + 1) * N / 12)    # 0-based exclusive

# 1-based inclusive data-row numbers for humans/logs:
START_ROW = start_index + 1
END_ROW   = end_index                    # last included 1-based row
# Process 0-based indices i in [start_index, end_index)
# Equivalent 1-based inclusive: START_ROW .. END_ROW
```

Header is never assigned.

**Invariant:** every data row belongs to exactly one agent.

Example only (recompute live — N changes when pages.csv grows):

  If N=944:
    Agent 1  → rows 1–78
    Agent 2  → rows 79–157
    ...
    Agent 12 → rows 866–944

### 5.3 Spawn twelve workers

Spawn exactly 12 agents **in parallel**. Each receives:

  * Path to this prompt file
  * AGENT_ID
  * START_ROW, END_ROW (precomputed — do not make workers re-fight over math)
  * ROOT_DIR, PAGES_CSV, CK_FILE, GROK_RESEARCH_ROOT
  * Any INPUT_TEXT filters

Workers must not share the same START_ROW/END_ROW range.

### 5.4 Orchestrator wait + aggregate

When all workers exit:

  1. Read each `{GROK_RESEARCH_ROOT}/_agent_{ID}_log.txt`
  2. Sum OK / PARTIAL / SKIP / FAIL
  3. Prepend orchestrator summary to CHANGES_FILE
  4. List pages needing human review (defamation edge cases, FAIL rows)
  5. Optionally recommend running `/ck_defemation_prevention` across site/docs

### 5.5 Single-agent mode

If the runner is told "You are Agent K of 12" (or only one agent is available):

  * Do **not** spawn children
  * Compute or accept START_ROW/END_ROW for K only
  * Execute the WORKER section for that partition only


====================================================================
6. WORKER BOOTSTRAP (EVERY AGENT, ONCE)
====================================================================

At agent start:

  1. Parse INPUT_TEXT for overrides (section filter, dry-run, force re-research).
  2. Set AGENT_ID, START_ROW, END_ROW.
  3. Generate THE_DATE_TIME_STRING.
  4. `mkdir -p {GROK_RESEARCH_ROOT} {LOCK_DIR}`
  5. Create/clear or append AGENT_LOG with a header line:

       # agent={AGENT_ID} start={START_ROW} end={END_ROW} at={THE_DATE_TIME_STRING}

  6. Load all CSV rows with a proper parser. Build list `rows[0..N-1]`.
  7. Select `rows[START_ROW-1 : END_ROW]` (Python slice end exclusive:
     `rows[START_ROW-1:END_ROW]`).
  8. **Resume support:** if AGENT_LOG already has OK lines for page_keys,
     skip those page_keys unless INPUT_TEXT says force re-run.
  9. Print to stdout: agent id, row count, first/last page_key in partition.

### Bootstrap helper (agents may run this)

```python
import csv, math, os
from pathlib import Path

ROOT = Path.home() / "BGit/Bryan_git/charlie-kirk"
PAGES = ROOT / "pages.csv"
AGENT_ID = int(os.environ.get("AGENT_ID", "1"))  # 1..12
NUM = 12

with PAGES.open(newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
N = len(rows)
k = AGENT_ID - 1
start = (k * N) // NUM
end = ((k + 1) * N) // NUM
partition = rows[start:end]
print(f"Agent {AGENT_ID}: data rows {start+1}-{end} count={len(partition)}")
for r in partition:
    print(r["page_key"], r["file_path"])
```


====================================================================
7. WHICH ROWS TO PROCESS / SKIP
====================================================================

### Default: process every assigned row with a real public file

For each row in the partition:

  * Resolve `{ROOT_DIR}/{file_path}`
  * Missing file → status SKIP, note "missing file", continue
  * Empty file_path → SKIP

### Default process by level

  * Level 1 home — yes (careful growth; keep navigation)
  * Level 2 overview — yes (grow body + Related Areas; protect TOC)
  * Level 3 — yes (**main target**)
  * Level 4+ — yes

### Default process by page_type

  * topic, person, overview, index, organization, home — all yes

### Recommended auto-skips (unless INPUT_TEXT says otherwise)

Skip or light-touch these (log SKIP with reason) to avoid wasting research
budget on non-investigative scaffolding:

  * Paths containing `/disabled/`
  * Paths containing `/trash/` (if present under docs — still public; if
    INPUT_TEXT says include trash, process them)
  * Paths under `laws/other/old/` or clearly "old draft" law trees
  * Pure asset-spec pages (e.g. `*_svg/needs`, pure SVG/PowerPoint specs)
    → still allowed to process if runner wants full coverage; default SKIP
    with reason `non_investigative_scaffold`

When in doubt and no filter is set: **process the row**.

### Optional INPUT_TEXT filters

  * `only levels 2,3`
  * `only page_types topic,person`
  * `only section FBI`  (level2_section match)
  * `exclude section laws`
  * `research only` / `dry-run` — write research files, do not edit MDX
  * `force` — re-query even if research file exists
  * `integrate only` — skip Grok if research file already exists; only grow page


====================================================================
8. PER-ROW LOOP (THE WORK)
====================================================================

For each assigned row, execute steps A → F **in order**. Never integrate
before the research file for that row is written (unless `integrate only`).


--------------------------------------------------------------------
STEP A — Understand the page (Level 2 + Level 3)
--------------------------------------------------------------------

  1. Parse fields:
       page_key, parent_key, level, level2_parent, level2_section,
       page_type, url_path, file_path, title, sidebar_label, directory,
       description, line_count

  2. Read the full existing page at `{ROOT_DIR}/{file_path}`.

  3. Note structure already present:
       * frontmatter keys
       * back button present?
       * H2/H3 outline
       * Related Areas present?
       * disclaimer present?
       * approximate line_count / substance density

  4. Build **LEVEL2_TOKEN** and **LEVEL3_TOKEN** for the research path.

     sanitize(s):
       * str(s)
       * replace spaces and hyphens with `_`
       * remove every character not in [A-Za-z0-9_]
       * collapse repeated `_`
       * strip leading/trailing `_`
       * if empty → `unknown`

     LEVEL2_TOKEN:
       * If level2_section non-empty → sanitize(level2_section)
       * Else if directory non-empty → sanitize(first path segment of directory)
       * Else if level == 1 → `Home`
       * Else → `root`

     LEVEL3_TOKEN:
       * Let base = filename without extension
       * If base in {overview, index} and page_key:
           prefer sanitize(page_key) if level>=2 and base==overview and
           multiple overviews could collide; else use `overview` / `index`
           for true Level 2 overviews and Home
       * For nested paths (Level 4+): prefer sanitize(page_key) OR
         sanitize( relative path under level2 with `/` → `_` )
         Example: Medical/Hospital/Wound.mdx → `Hospital_Wound` or page_key
       * Default: sanitize(base)
       * On collision with an existing different page_key's file, use
         sanitize(page_key)

  5. Build human phrases for the Grok query (natural English, not raw tokens):

     LEVEL2_DESCRIPTION:
       * Prefer a short phrase naming the investigation section.
       * Sources: level2_section name + parent overview title/description if
         known + this row's description when level==2.
       * Examples:
           "FBI involvement and cover-up claims after the UVU shooting"
           "aircraft and flight activity around the Charlie Kirk assassination"
           "events after the Charlie Kirk shooting at UVU"

     LEVEL3_DESCRIPTION:
       * Prefer title + description compressed into one clear focus phrase.
       * Must be specific to **this page**, not the whole site.
       * For person pages: "{Name} and their reported connection to the case"
         — no guilt asserted.
       * For Level 2 overview rows: restate the section breadth
         ("the full {section} investigation area and its major sub-topics").
       * For Home: "the overall Charlie Kirk assassination investigation and
         why many citizens reject the lone-gunman narrative"

  6. Optional CK_FILE touch:
       Grep CK_FILE for 3–10 distinctive keywords from title/description.
       Keep hits for integration later (still private until rewritten safely
       onto the public page).


--------------------------------------------------------------------
STEP B — Grok AI / X research (dedicated to this row only)
--------------------------------------------------------------------

Focus on **this one row only**. Do not research the whole site in one call.

### B.1 Primary query (REQUIRED — use this wording)

Fill braces only; keep the rest of the sentence structure:

```
Find all information Charlie Kirk citizen investigators discuss about
anything with his assassination or anything related (UVU, TPUSA, FBI,
Trial, Tyler Robinson, Erika Kirk) that is anything related to
{LEVEL2_DESCRIPTION} and especially anything in the area of
{LEVEL3_DESCRIPTION}. Search what people are saying on twitter about
this. Do not summarize. Give all the information you can. We want
extensive information and as many facts or claims as possible. Our
audience must learn beyond the government narrative to all sides of
the issue and all claims or discussions.
```

### B.2 How to actually retrieve (use every tool you have)

Depending on runtime, call as many of these as available:

  * **Grok AI chat / deep search** with the primary query
  * **x_semantic_search** — semantic query paraphrasing LEVEL3_DESCRIPTION
    + "Charlie Kirk" + "UVU"
  * **x_keyword_search** — operators for exact entities, e.g.:
      `"Charlie Kirk" (UVU OR TPUSA) {key entity} filter:has_engagement`
      mode Latest for recent; Top for high-signal
  * **web_search** — for named people, flights, court filings, news
  * **web_fetch / open_page** — for important linked threads or articles

Prefer **primary sources** (X posts, filings, FOIA/GRAMA, video metadata)
over recycled blog summaries.

### B.3 Demand raw breadth (anti-summary)

Instruct every tool call:

  * Do **not** summarize
  * Return handles, dates, URLs, and claim text when possible
  * Include disputed claims, conspiracy theories, **and** debunkings
  * Include "who went where / who said what / when" whenever available
  * Include counter-narrative and official-narrative statements

### B.4 Follow-up queries (if primary is thin)

If the first capture is short, generic, or off-topic, run **1–3** follow-ups:

  Follow-up template:

```
Find all X/Twitter posts and citizen investigator threads about the Charlie
Kirk assassination and {SPECIFIC_ENTITY_OR_KEYWORDS}. Include handles,
dates, URLs, and full claim text. Do not summarize. Include disputed and
conspiracy claims and any rebuttals.
```

Pick SPECIFIC_ENTITY_OR_KEYWORDS from:

  * Named people on the page
  * Locations (UVU, Losee Center, courtyard, Provo airport, Fort Huachuca)
  * Objects (N1098L, Mauser 98, 30-06, mic, tent paving, Discord)
  * Institutions (FBI, TPUSA, UVU PD, Orem PD)
  * Unique phrases from the page description

### B.5 Keyword bank (use when relevant — not every query)

  UVU, TPUSA, Tyler Robinson, Erika Kirk, shaped charge, 30-06, Mauser 98,
  N1098L, HADES, SAM flight, Fort Huachuca, Mossad, Israel, Candace Owens,
  Ian Carroll, gag order, Judge Graf, GRAMA, tent paving, mic explosion,
  ballistics, CBLA, Discord, Lance Twiggs, security team, sound crew,
  Brooksby, Kash Patel, Bill Ackman, donor meeting, Hamptons, autopsy,
  medical examiner, Air Force Two, visa revocation, deboosting

### B.6 Idempotency

  * If `{research_path}` already exists and INPUT_TEXT does **not** say
    `force`, and mode is not `integrate only`:
      - Default: **re-run research and overwrite** the research file only if
        the file is empty/stub/failed; otherwise **keep existing research**
        and proceed to integrate (faster restarts).
      - If INPUT_TEXT says `force`: always re-query and overwrite research.
  * If mode is `integrate only`: require research file to exist; if missing,
    run primary query once.


--------------------------------------------------------------------
STEP C — Write temporary research file (REQUIRED before integrate)
--------------------------------------------------------------------

Path:

```
{GROK_RESEARCH_ROOT}/{LEVEL2_TOKEN}/{LEVEL3_TOKEN}_research.txt
```

  * `mkdir -p` the Level 2 directory
  * Write **complete** capture — never a short abstract in place of raw data

### Required header

```
====================================================================
GROK TWITTER RESEARCH CAPTURE
====================================================================
page_key:        {page_key}
level:           {level}
page_type:       {page_type}
level2_section:  {level2_section}
level2_parent:   {level2_parent}
title:           {title}
url_path:        {url_path}
file_path:       {file_path}
agent_id:        {AGENT_ID}
partition_rows:  {START_ROW}-{END_ROW}
captured_at:     {THE_DATE_TIME_STRING}
level2_token:    {LEVEL2_TOKEN}
level3_token:    {LEVEL3_TOKEN}
level2_phrase:   {LEVEL2_DESCRIPTION}
level3_phrase:   {LEVEL3_DESCRIPTION}
tools_used:      {comma-separated tools}
primary_query:
{full primary query text}
====================================================================
PRIMARY RESULTS
====================================================================
{full raw output — posts, claims, links, dates, handles}

---------------- FOLLOW-UP QUERY 2 ----------------
{query}
---------------- RESULTS ----------------
{results}

---------------- FOLLOW-UP QUERY 3 ----------------
...
====================================================================
CK_FILE HITS (optional)
====================================================================
{relevant excerpts or section names from Charlie_Kirk.txt}
====================================================================
AGENT NOTES
====================================================================
{thin_result? yes/no; defamation_hotspots; entities_to_attribute}
====================================================================
```

Research files are temporary working product. They may contain raw
allegations. **Public pages must not paste them raw.**


--------------------------------------------------------------------
STEP D — Grow the public Docusaurus page
--------------------------------------------------------------------

Goal: **greatly grow** the page using the research file + CK_FILE hits,
while preserving Assess_Manual structure and defamation safety.

### D.0 PRESERVE EXISTING VALUE (HARD RULE — USER REQUIREMENT)

Pages already contain valuable investigation content. Growing a page is
**additive integration**, not a wipe-and-rewrite.

  1. **Never delete** existing valuable facts, sections, timelines, quotes,
     tables, attributed claims, or analysis already on the page.
  2. **Integrate** by expanding existing sections and/or inserting new H2/H3
     sections with new research. You may rewrite for clarity and flow, but
     every pre-existing substantive claim must still appear (same or clearer).
  3. **Keep the bottom of the page** — Related Areas blocks, bottom link
     grids, and footer-style cross-links to other pages must remain. Do not
     strip or replace the bottom link section. You may fix broken hrefs or
     improve link labels, but the bottom navigation content stays.
  4. Preserve frontmatter, back buttons, and Level 2 three-column TOCs.
  5. If you restructure, migrate old substance into the new structure first;
     only then add research. Diff yourself mentally: no net loss of prior
     investigative content.

If INPUT_TEXT is `research only` / `dry-run`: skip Step D (status OK_RESEARCH).

### D.1 Growth quality bar (definition of done for a normal topic page)

A page counts as successfully grown only if **at least one** of these is true:

  * Added **≥ 3** new distinct attributed claims/facts not already on the page,
    OR
  * Added **≥ 1** substantial new H2 section (≥ ~150 words) of sourced content,
    OR
  * Research was truly empty after follow-ups — then status PARTIAL and a
    short "Research gap" note is added (or only log PARTIAL without fake content)

**Do not** invent posts, handles, dates, or quotes. If Grok is vague, keep
vague attribution ("citizen investigators on X have discussed…") or skip.

**Do not** "grow" by padding, repeating the same claim, or restating the
site mission paragraph on every Level 3 page.

### D.2 Integration algorithm (surgical, not blind replace)

  1. Re-read page + research file.
  2. Extract candidate claims from research (bullet list in agent scratchpad).
  3. Drop candidates already present (same fact/claim already attributed).
  4. Drop candidates off-topic for this Level 3 (park them only if they
     strongly belong — better as a cross-link note than a digression).
  5. Cluster remaining candidates under 2–6 clear H2/H3 headings.
  6. Rewrite clusters into clean investigative prose:
       * who said what
       * when (if known)
       * where / what medium (X post, video, filing)
       * what claim exactly
       * counter-claim if research has one
  7. Place **highest-signal** material high on Level 3 pages:
       * challenges to lone-actor / 30-06 narrative
       * intel-service discussions
       * timeline contradictions
       * primary-source OSINT
     Place routine chronology and secondary color lower.
  8. Preserve:
       * YAML frontmatter
       * existing correct facts
       * Level 2 three-column TOC (may add missing child links)
       * back buttons (fix relative raw HTML)
       * Related Areas (add if missing)
       * existing media blocks (do not exceed 3 media items total)
  9. Apply defamation rewrite pass (Section 10) to every new sentence.
 10. Apply page-type playbook (Section 9).
 11. Update line_count in pages.csv if easy; else note in log.
 12. Do not create new pages unless research proves a critical orphan topic
     that cannot fit — default is grow existing rows only.

### D.3 Recommended new section titles (pick what fits)

Use only when content exists; do not add empty shells:

  * Citizen Investigator Claims on X
  * Timeline Claims (As Reported)
  * Who Said What (Attributed)
  * Official Narrative vs Competing Claims
  * Open Questions Raised by Investigators
  * Documents, Video, and Primary Sources Cited
  * Counter-Claims and Debunk Attempts
  * Related Movements / Locations / People (as reported)

### D.4 Quoting X users

Preferred form:

  > According to @{handle} on X ({date if known}), {paraphrase or short quote}.
  > Claim: {one-sentence claim}. This is an attributed public claim, not a
  > court finding.

If a URL exists, add a markdown or absolute link. Never fabricate a URL.

### D.5 Cross-linking

  * Markdown links to other docs: `[Label](./PeerPage)` or path Docusaurus accepts
  * Raw HTML anchors: **absolute** paths only (`/FBI/overview`)
  * When research mentions a topic that has its own page_key in pages.csv,
    link it
  * Related Areas: 6 links, two columns of three, **other sections**, mix of
    Level 2 and Level 3


--------------------------------------------------------------------
STEP E — Per-row verification checklist
--------------------------------------------------------------------

Before next row:

  [ ] Research file exists and is more than a header/stub (or PARTIAL logged)
  [ ] Page still parses as MD/MDX (no broken fences, no unclosed JSX tags)
  [ ] No new `href="../` raw HTML in touched file
  [ ] No new stated-fact criminal guilt for living persons
  [ ] Person pages: disclaimer + Status field when applicable
  [ ] Level 2: three-column TOC still present; columns still roughly balanced
  [ ] Level 3+: back button still present at top
  [ ] Related Areas present (Level 2 and 3)
  [ ] New claims attributed
  [ ] Did not paste entire research file into the page
  [ ] Did not delete true documented facts that were already on the page
  [ ] Growth bar met OR honest PARTIAL

### MDX footguns to avoid

  * Unescaped `{` `}` in prose inside MDX — escape or wrap as code/text carefully
  * Broken `style={{...}}` objects
  * Nested `:::` admonitions left open
  * Smart quotes breaking frontmatter YAML


--------------------------------------------------------------------
STEP F — Log and continue
--------------------------------------------------------------------

Append one TSV line to AGENT_LOG:

```
{status}\t{page_key}\t{file_path}\t{research_path}\t{lines_before}\t{lines_after}\t{note}
```

status ∈:

  * OK           — research + growth done, quality bar met
  * OK_RESEARCH  — research only mode
  * PARTIAL      — thin research and/or limited growth
  * SKIP         — filtered / missing / scaffold
  * FAIL         — exception; include error in note

On non-fatal errors: write stub research with error banner if needed, log
FAIL or PARTIAL, **continue** the partition. Do not abort the whole agent
for one bad row.


====================================================================
9. PAGE-TYPE PLAYBOOKS
====================================================================

### 9.1 Level 3 topic (default)

  * Grow body with clustered H2 sections
  * High-signal claims near top
  * Heavy attribution
  * Cross-links + Related Areas

### 9.2 Level 3 / 4 person page

  * Ensure Legal Disclaimer (Intervention A) after H1
  * Status: Alive / Deceased (YYYY) / Unknown — web-check if Unknown
  * Frame connection as "named in public commentary / reported connection"
  * **Highest** defamation care for private figures
  * Never title sections "Role in the Assassination" as fact

### 9.3 Level 2 overview

  * Protect three-column TOC structure (Assess_Manual grid)
  * Grow the **three paragraphs after TOC** with richer substance from research
  * May add missing TOC bullets for existing children found on disk
  * Do not dump X threads into the overview; keep overview scannable
  * Refresh Related Areas if weak

### 9.4 Index pages (page_type index)

  * Keep routing/hub purpose
  * Add short attributed "what investigators are watching" notes only if they
    help navigation
  * Prefer linking out over essay growth

### 9.5 Organization pages

  * True org facts stay as facts (e.g. TPUSA organized UVU event)
  * Criminal org-conduct claims → attributed only + Intervention B
  * TPUSA is litigious — extra care (trade libel)

### 9.6 Home (Level 1)

  * Preserve navigation panels / entry paths
  * Limited growth: strengthen the investigative thesis with attributed
    high-level points; do not turn Home into a 10,000-word dump
  * Still run research into `Home/index_research.txt` for use by other pages
    if needed

### 9.7 Fix / laws pages

  * These are policy/law text pages — do not overwrite statutory draft language
    with conspiracy essays
  * Growth allowed only in clearly narrative/supporting sections
  * If page is pure law text, status SKIP or minimal PARTIAL with note
    `law_text_preserve`


====================================================================
10. DEFAMATION RULES (PUBLIC PAGES — NON-NEGOTIABLE)
====================================================================

Think like a **defense-side defamation attorney** who still wants maximum
investigative information on the page.

Authoritative detail: DEFAMATION_SKILL. Summary for this run:

### 10.1 Five elements (shape writing to break "statement of fact of guilt")

  1. Statement of FACT
  2. FALSE or unverified
  3. PUBLISHED (this site is)
  4. Of and concerning an identifiable person/org
  5. Harm to reputation

Prefer: questions, attributed claims, opinion clearly labeled, "some
investigators allege," "public commentary claims."

### 10.2 User's hard line (from run requirements)

Never write as the site's own fact that a living person:

  * Knew Charlie Kirk would be killed ahead of time, OR
  * Took actions to cause his death (directly or indirectly), OR
  * Ordered / planned / carried out the assassination

**Unless** established in court.

If an X user said that about someone: **quote/attribute the X user**, then
add that the site does not adopt that as a finding, and no court has found it.

### 10.3 Never state as fact (unless court-proven)

  * Living person guilt for the killing or cover-up crimes
  * Erika Kirk refused autopsy "to hide the truth"
  * TPUSA planned or participated in the assassination
  * Named security / sound-crew **intentional** enabling of the killing
  * Site conclusions: "true assassins," "the real killer," "we proved X guilty"

### 10.4 Good patterns

  * "According to @handle on X…"
  * "Citizen investigators have claimed…"
  * "Reportedly…" / "Allegedly…"
  * "Some commentators ask whether…"
  * "Unverified allegation; no court has made such a finding."
  * "If true, this would raise questions about…"

### 10.5 Interventions A–D

  **A — Disclaimer** on person / high-risk org pages (after H1):

```mdx
:::caution Legal Disclaimer
Nothing on this page constitutes a finding of wrongdoing, criminal conduct,
ethical violation, or participation in any crime by [Name/Organization] or
any other living person. This site documents questions and claims that have
circulated in public commentary — not findings of fact. All persons and
organizations named on this site are presumed innocent. Allegations
referenced here are unproven and have not been established in any court.
:::
```

  **B — Fact → framed allegation**

    BEFORE: "X participated in the cover-up"
    AFTER:  "Some commentators have alleged X participated in a cover-up —
             this is an unverified allegation; no court has made such a finding"

  **C — Section caveat** for accusation lists:

    "(the following are unverified claims from public commentary, not findings
     of fact)"

  **D — Heading rewrite**

    BEFORE: "## Bill Ackman: His Role in the Assassination"
    AFTER:  "## Bill Ackman: Public Commentary and Context"

### 10.6 Risk tiers

  **HIGH**
    Erika Kirk (also IIED / false-light sensitivity — widow)
    Private figures: sound crew, security officers, UVU staff, vendors,
    Tyler Robinson's partner/family, ordinary named citizens

  **MODERATE**
    TPUSA (corporate / trade libel; litigious)
    High-profile living public figures in donor / Israel / politics threads

  **LOW — do not soften**
    Charlie Kirk (deceased)
    Other confirmed deceased
    True org facts ("TPUSA organized the UVU event")
    Charging facts about Tyler Robinson stated as **charges**, not guilt
    Institutional critique of FBI/CIA as agencies (named individual agents
    are higher risk than the institution)

### 10.7 What NOT to strip

  * True documented facts
  * Already attributed claims
  * Clearly labeled theories
  * Agency institutional critique
  * Investigative substance — only unattributed "site asserts living person
    is guilty" framing

### 10.8 Who said what / where / when (user priority)

The audience cares about **speakers and movements**:

  * Prefer "Candace Owens stated on X that…" over "It is known that…"
  * Prefer "Ian Carroll posted video analysis claiming…" over "Video proves…"
  * Prefer "Witnesses reported…" over "Security intentionally…"

### 10.9 Per-page attorney checklist

  [ ] No living person accused of a crime as site fact
  [ ] No Erika-autopsy-to-hide-evidence as fact
  [ ] No TPUSA-planned-assassination as fact
  [ ] No named private security/sound intentional wrongdoing as fact
  [ ] Person pages: disclaimer present
  [ ] H1/H2 do not imply guilt
  [ ] X claims attributed to speakers
  [ ] False-light captions avoided (photos/titles that imply guilt without saying it)


====================================================================
11. ASSESS_MANUAL LAYOUT (SUMMARY — FULL FILE GOVERNS)
====================================================================

### Level 2 overview

  * 1–2 sentence orientation
  * Three-column bullet TOC immediately after (MDX grid)
  * Exactly three explanatory paragraphs after TOC
  * Related Areas: 6 links, 2×3, other sections
  * Columns balanced (±1 row)

Three-column skeleton:

```mdx
<div style={{display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem'}}>
<div>

* [Topic A](./topic-a)

</div>
<div>

* [Topic B](./topic-b)

</div>
<div>

* [Topic C](./topic-c)

</div>
</div>
```

### Level 3 / deeper

  * Absolute back button at very top
  * Straight into substance
  * Sub-headings
  * Attributed claims
  * Status on person pages
  * Max 3 float-right media items @ 48% width; clearfix after
  * Related Areas at bottom

Back button pattern (absolute href — required):

```mdx
<a href="/{Level2Section}/overview" style={{display:'inline-block',
marginBottom:'1rem', padding:'0.35rem 0.9rem', background:'#1a73e8',
color:'#fff', borderRadius:'4px', textDecoration:'none',
fontSize:'0.9rem'}}>← {Level2 Label}</a>
```

### Related Areas

```mdx
## Related Areas

<div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:'0.5rem 2rem',
marginTop:'0.5rem'}}>
<div>

* [Phrase for Link 1](/OtherSection/Page)
* [Phrase for Link 2](/OtherSection/Page)
* [Phrase for Link 3](/OtherSection/Page)

</div>
<div>

* [Phrase for Link 4](/OtherSection/Page)
* [Phrase for Link 5](/OtherSection/Page)
* [Phrase for Link 6](/OtherSection/Page)

</div>
</div>
```

Rules: mix Level 2 + Level 3; jump outside current section; 4–8 word labels;
prefer under-linked pages.


====================================================================
12. LINKING RULES (CRITICAL)
====================================================================

This site uses `trailingSlash: false`. Relative raw HTML hrefs break.

  * NEVER `href="../overview"` in raw HTML `<a>`
  * ALWAYS absolute paths in raw HTML: `href="/FBI/overview"`
  * Level 2 overview back button: `href="/"` label `← Home`
  * Markdown doc links `[x](./Page)` are OK (build-time resolution)
  * Self-check: `rg 'href="\.\./' {touched files}` → zero matches


====================================================================
13. WRITING STYLE
====================================================================

  * Investigative documentation, not rant
  * Dense with claims, sources, contradictions
  * Wikipedia-like: lead with what matters; details below
  * Hyperlink concepts that have homes elsewhere on the site
  * When research conflicts, present **both** sides
  * Expand substantially when research is rich
  * Rewrite research into clean sections — never dump the raw file
  * Preserve names, numbers, dates, handles when rewriting
  * Charged ≠ convicted; alleged ≠ proven
  * Audience already knows the site thesis — Level 3 pages should not
    re-preach the entire home-page essay


====================================================================
14. PAGES.CSV MAINTENANCE
====================================================================

  * Primary mode: **read** CSV, **write** page files
  * Update CSV when: title, sidebar_label, path, level, or parent changes
  * New pages (rare): add full row with unique page_key ≤ 4 words-ish,
    underscores, parent_key set, level correct, file_path correct
  * Never delete a row because research failed
  * Prefer incremental edits over full regeneration mid-run
  * If multiple agents must edit pages.csv (rare), use LOCK_DIR mutex:


```bash
# naive lock
while ! mkdir "{LOCK_DIR}/pages_csv.lock" 2>/dev/null; do sleep 0.2; done
# ... edit pages.csv ...
rmdir "{LOCK_DIR}/pages_csv.lock"
```


====================================================================
15. PARALLELISM, SAFETY, RESUME
====================================================================

  * Partitions guarantee different rows; file_path collisions should not happen
  * If two rows share file_path: lower AGENT_ID writes; other SKIP `duplicate_path`
  * Research path collision: use sanitize(page_key) as LEVEL3_TOKEN
  * CHANGES_FILE concurrent prepend: use LOCK_DIR/changes.lock similarly
  * **No git commit/push** unless human explicitly asks after the run
  * **No** `git reset --hard`, force-push, or destructive clean
  * Do not edit unrelated repos or DEFEMATION_CleanUp targets
  * Optional backup before large rewrite:

      `cp "{file}" "{file}.bak_{THE_DATE_TIME_STRING}"`

  * Resume: skip page_keys already OK in AGENT_LOG unless `force`
  * Agent crash mid-run: restart same AGENT_ID; resume does the rest


====================================================================
16. REPORTING
====================================================================

### Per-row AGENT_LOG (required)

```
{status}\t{page_key}\t{file_path}\t{research_path}\t{lines_before}\t{lines_after}\t{note}
```

### End-of-agent CHANGES_FILE block (prepend, with lock)

```
====================================================================
{THE_DATE_TIME_STRING}  Agent {AGENT_ID}  rows {START_ROW}-{END_ROW}
====================================================================
processed: N
ok: N
ok_research: N
partial: N
skip: N
fail: N
research_root: {GROK_RESEARCH_ROOT}
pages_grown:
  - page_key (file_path) — one-line what was added
needs_human_review:
  - page_key — reason
fail_details:
  - page_key — error
====================================================================
```

### Orchestrator final block

Totals across agents, top failure reasons, recommendation for defamation scan.


====================================================================
17. STAGE CHECKLIST (FULL RUN)
====================================================================

  [ ] STAGE 0 — Read this prompt, CK_FILE, ASSESS_MANUAL, DEFAMATION_SKILL,
                CLAUDE_MD; preflight paths; count N
  [ ] STAGE 1 — Compute 12 partitions; print ranges; sum == N
  [ ] STAGE 2 — Spawn 12 workers (or run single-agent mode)
  [ ] STAGE 3 — Each worker: bootstrap → for each row A–F
  [ ] STAGE 4 — Workers prepend CHANGES_FILE summaries
  [ ] STAGE 5 — Orchestrator aggregate + human-review list
  [ ] STAGE 6 — Optional `/ck_defemation_prevention` site-wide pass


====================================================================
18. WORKER SYSTEM MESSAGE (COPY WHEN SPAWNING)
====================================================================

```
You are Worker Agent {AGENT_ID} of 12 for WhoAssassinatedCharlieKirk.com.

ROOT_DIR=~/BGit/Bryan_git/charlie-kirk
PAGES_CSV={ROOT_DIR}/pages.csv
CK_FILE=~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt
PROMPT={ROOT_DIR}/prompts/grok_twitter_research.md
GROK_RESEARCH_ROOT=~/T/_ck/grok
START_ROW={START_ROW}
END_ROW={END_ROW}

Obey PROMPT exactly. Read CK_FILE, Assess_Manual, and the defamation skill
before editing any public page.

Your job: process every pages.csv data row from START_ROW through END_ROW
inclusive (header excluded). For each row:

  1) Understand Level 2 + Level 3 from the CSV + existing page file
  2) Run the exact Grok/X primary query template in PROMPT (fill descriptions)
  3) Save full raw results to
     ~/T/_ck/grok/{LEVEL2_TOKEN}/{LEVEL3_TOKEN}_research.txt
  4) Greatly grow the public site/docs page with attributed, defamation-safe
     writing that preserves Assess_Manual layout
  5) Verify, log to _agent_{AGENT_ID}_log.txt, continue

Audience: people who reject the Tyler Robinson / 30-06 complete narrative and
want intelligence-service-level possibilities and citizen X investigation
claims documented carefully.

Hard rule: never state as fact that a living person knew of or caused Charlie
Kirk's death. Quote X users; use allegedly/reportedly; who-said-what matters.
Think like a defamation attorney who still wants the information published.

When finished, prepend your summary to changes_grok_twitter_research.txt.
Do the work — do not only plan it.
```


====================================================================
19. WORKED EXAMPLES
====================================================================

### Example A — Level 3 topic

Row:

  page_key: After_Crime_Scene_Handling
  level: 3
  level2_section: After
  file_path: site/docs/After/Site_Changes_And_Crime_Scene_Handling.mdx
  title: Site Changes and Crime-Scene Handling After the UVU Event (Claims)

Tokens:

  LEVEL2_TOKEN = After
  LEVEL3_TOKEN = Site_Changes_And_Crime_Scene_Handling
  research = ~/T/_ck/grok/After/Site_Changes_And_Crime_Scene_Handling_research.txt

LEVEL2_DESCRIPTION:
  "events after the Charlie Kirk shooting at UVU"

LEVEL3_DESCRIPTION:
  "rapid courtyard paving, crime-scene site changes, and Hardscape/Merrell
   contractor claims after the UVU event"

Primary query: (template with those phrases filled)

Integrate as attributed sections; never assert a named contractor "covered up
a murder" as site fact.

### Example B — Level 2 overview

  page_key: FBI
  level: 2
  file_path: site/docs/FBI/overview.mdx
  LEVEL2_TOKEN=FBI
  LEVEL3_TOKEN=overview
  research=~/T/_ck/grok/FBI/overview_research.txt
  Grow the three post-TOC paragraphs + Related Areas; keep three-column TOC.

### Example C — Person page

  page_key: FBI_Zachariah_Qureshi
  page_type: person
  file_path: site/docs/FBI/Zachariah_Qureshi.mdx
  LEVEL3_DESCRIPTION includes name + "reported arrest and release near UVU"
  without asserting guilt.
  Add/keep Legal Disclaimer; attribute all X claims.

### Example D — Home

  page_key: Home
  level: 1
  file_path: site/docs/index.mdx
  LEVEL2_TOKEN=Home
  LEVEL3_TOKEN=index
  Careful growth only; preserve navigation hub.


====================================================================
20. KEY REFERENCE FILES
====================================================================

  ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt
  {ROOT_DIR}/pages.csv
  {ROOT_DIR}/Claude.md
  {ROOT_DIR}/prompts/Assess_Manual.md
  {ROOT_DIR}/prompts/grok_write.mdx
  {ROOT_DIR}/prompts/grok_twitter_research.md   ← this file
  {ROOT_DIR}/skills_storage/ck_defemation_prevention.md
  ~/.claude/commands/ck_defemation_prevention.md
  {ROOT_DIR}/site/docs/

Context only (not default edit targets):

  ~/BGit/Bryan_git/DEFEMATION_CleanUp/p_Defemation.md


====================================================================
21. ANTI-PATTERNS (DO NOT DO THESE)
====================================================================

  * Summarizing Grok output into three vague bullets and calling it done
  * Pasting the entire research .txt into the MDX page
  * Replacing a Level 2 TOC with a research essay
  * Stating living-person guilt as fact "because Twitter said so"
  * Inventing handles, dates, URLs, or quotes
  * Re-preaching the full site thesis on every Level 3 page
  * Editing private Details/Research as if they were public pages
  * Using raw HTML relative hrefs (`../`)
  * Aborting the whole partition after one FAIL row
  * Two agents claiming the same row range
  * Softening true documented facts (TPUSA hosted the event, etc.)
  * Growing law-draft pages by overwriting statutory text
  * Skipping the research file and writing from memory only
  * Claiming "we proved" intelligence services did it as courtroom fact


====================================================================
22. SUCCESS CRITERIA
====================================================================

A successful full run means:

  [ ] All N data rows assigned to exactly one of 12 agents
  [ ] Sum of partition sizes == N
  [ ] Each processable page has a research file under ~/T/_ck/grok/...
  [ ] Each processable page is substantially richer in attributed
      citizen-investigator / X-sourced material (growth bar met or honest PARTIAL)
  [ ] Assess_Manual structure still holds (TOC, back buttons, Related Areas)
  [ ] Defamation-safe language on all new content
  [ ] AGENT_LOGs + CHANGES_FILE document the run
  [ ] No cross-agent file overwrites
  [ ] No fabricated sources

When this prompt is run: **execute the work**.


====================================================================
END OF PROMPT — GROK TWITTER RESEARCH
====================================================================
