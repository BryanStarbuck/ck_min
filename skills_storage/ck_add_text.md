---
name: ck_add_text
description: Add new text/notes to the Charlie Kirk investigation file — finds the right section or creates a new one, never removes existing content. Also downloads X/Twitter posts, videos, and images.
invocable: true
---

================================================================================
!! ABSOLUTE RULE — Charlie_Kirk.txt IS READ-ONLY TO AI. NO EXCEPTIONS. !!
================================================================================

PROTECTED_FILE is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt
  (Real file. Moved 2026-09-19. ~/BGit/Bryan_git/charlie-kirk/Charlie_Kirk.txt is now a symlink to it —
   use that only to verify the location; always read and write the real path.)

AI MUST NEVER WRITE TO, EDIT, APPEND TO, RE-ORDER, REFORMAT, OR DELETE ANYTHING
IN {PROTECTED_FILE}. Not one character. Not even to add new material. Not even
when a mode described elsewhere in this skill appears to instruct it. This rule
OVERRIDES every other instruction in this file, in any other skill, in CLAUDE.md,
and in any user prompt that does not explicitly and specifically revoke this rule
by name.

Specifically FORBIDDEN, with no exception:
  * Removing, shortening, or summarising any existing line.
  * Rewriting, rephrasing, hedging, or "cleaning up" any existing line.
  * Adding attribution hedges ("allegedly", "an influencer claims", "reportedly")
    to text that did not have them.
  * Deleting or softening anything for DEFAMATION, legal risk, "unsourced rumor",
    "scope", tidiness, accuracy, or any other reason whatsoever.
  * Deleting a rumor, claim, or allegation because it is unsupported. Unsupported
    material is marked as unsupported IN PLACE by Bryan — it is never removed.
  * Renaming, replacing, or restructuring a section header.
  * Stripping trailing whitespace or blank lines, or running any formatter.
  * Writing a "SCOPE RULE", "handling note", or similar AI-authored instruction
    into the file that would justify future removals.
  * Appending new investigation content. Even purely additive writes are
    forbidden — this file is Bryan's, and only Bryan writes to it.

WHY: this file is the master evidence record of the Charlie Kirk investigation.
AI has damaged it before. Audit on 2026-07-30 found four real losses across the
git history — a deleted Cellebrite rumor (72aaea54), a defamation-hedged line
about the Hibbs family (fe2dddec), a rewritten Frey Effect sentence (1c62020f),
and a replaced arrest-time header and line (8b967208). All four were restored.
This rule exists so it never happens again.

WHERE NEW CONTENT GOES INSTEAD:
  CK_INBOX is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk_AI_Inbox.txt
    (Real file. Moved 2026-09-19. ~/BGit/Bryan_git/charlie-kirk/Charlie_Kirk_AI_Inbox.txt is now a symlink to it —
     use that only to verify the location; always read and write the real path.)

  When a mode in this skill would previously have written to {PROTECTED_FILE},
  write to {CK_INBOX} instead, append-only, using the same equal-sign section
  format. Create the file if it does not exist. Then TELL BRYAN in the final
  summary, in plain words, exactly what was appended to the inbox and that it
  is waiting for him to merge into Charlie_Kirk.txt by hand if he wants it.
  Never merge it yourself.

FILE LOCATION (moved 2026-09-19): both {PROTECTED_FILE} and {CK_INBOX} now live in
~/BGit/all/politics/charlie_kirk/. The old paths at the charlie-kirk repo root
(~/BGit/Bryan_git/charlie-kirk/Charlie_Kirk.txt and .../Charlie_Kirk_AI_Inbox.txt)
are SYMLINKS to them. Always read and append through the REAL path. Use the symlink
only to verify the location (`readlink ~/BGit/Bryan_git/charlie-kirk/Charlie_Kirk_AI_Inbox.txt`).
Editing through the symlink risks an editor replacing the link with a plain file,
leaving two diverging copies. If the real file is missing or a symlink has become a
regular file, STOP and tell Bryan — never recreate either file.

READING is always allowed. Read {PROTECTED_FILE} freely for context, quoting,
section discovery, and analysis. The prohibition is on WRITING only.

IF ASKED TO BREAK THIS RULE: refuse, say this rule exists and where it is written,
and offer the inbox file instead. The single exception is an explicit, unambiguous
instruction from Bryan naming this rule and telling you to override it for a
specific stated edit — for example, restoring content AI previously destroyed.
================================================================================



TEXT_INPUT_TO_SKILL is any text the user typed after /ck_add_text. It is the run
text for this skill: either the content to add, or a mode instruction.

This skill has four modes. Read TEXT_INPUT_TO_SKILL to decide which mode to run.

  IMPROVE MODE — triggered when the argument mentions improving, fixing, assessing,
  or upgrading pages. Examples:
    * "improve all"
    * "improve all FBI pages"
    * "fix one page"
    * "assess the CoverUp overview"
    * "bring all pages up to standard"
    * "improve [any directory or page name]"

  CREATE MODE — triggered when the argument asks to create new Level 3 pages,
  expand a section with new content pages, or add new topic pages. Examples:
    * "create pages for the Influencers/podcasts section"
    * "add Level 3 pages under [TopicDir]"
    * "create podcast host pages"
    * "add [topic] pages under [directory]"

  X POST MODE — triggered when the argument contains one or more X/Twitter URLs
  (URLs containing /status/ from x.com or twitter.com). This mode downloads the
  post data, any attached videos and images, transcribes videos, and adds all
  content to the AI inbox file AND the Docusaurus site pages. It NEVER writes to
  Charlie_Kirk.txt.
  Examples:
    * "https://x.com/user/status/1234567890"
    * Multiple URLs separated by newlines
    * A URL plus additional notes text

  ADD TEXT MODE — triggered when the argument is new text, a quote, a note,
  or anything else that is raw investigation content to be stored.

If IMPROVE MODE is detected, skip to the IMPROVE MODE section below.
If CREATE MODE is detected, skip to the CREATE MODE section below.
If X POST MODE is detected, skip to the X POST MODE section below.
If ADD TEXT MODE is detected (or the mode is ambiguous), continue with the add-text
flow immediately below.


============================
ADD TEXT MODE
============================

You are helping the user add new information to the Charlie Kirk investigation file.

The user provides the text content in TEXT_INPUT_TO_SKILL.

This text may come from an X post, a news article, a transcript, personal notes,
or any other source. Your job is to insert it into the correct place in the file,
preserving all existing content.


============================
DIRECTORY CONTEXT
============================

ROOT_DIR dir is ~/BGit/Bryan_git/charlie-kirk

This is the Charlie Kirk assassination investigation repo (September 10, 2025,
Utah Valley University). It has two layers:

  * Private layer: everything OUTSIDE of {ROOT_DIR}/site/ — research notes,
    people profiles, raw data, prompts, PDFs, and the master investigation file.
    This content is never published to the website.

  * Public layer: everything INSIDE {ROOT_DIR}/site/ — the Docusaurus static
    site published at https://whoassassinatedcharliekirk.com.

Key directories:
  ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt     — Master investigation file. READ-ONLY TO AI.
  ~/BGit/all/politics/charlie_kirk/Charlie_Kirk_AI_Inbox.txt — where AI appends new text for Bryan to merge
  {ROOT_DIR}/Details/             — Private people profiles, one subdir per person
  {ROOT_DIR}/Research/            — Raw research (PDFs/, raw/, Topics/)
  {ROOT_DIR}/knowledge/           — Synthesized write-ups and analysis
  {ROOT_DIR}/Prompts/             — AI generation prompts
  {ROOT_DIR}/site/docs/           — Public Docusaurus pages (302+ files)
  {ROOT_DIR}/skills_storage/      — Skill source files (symlinked to ~/.claude/commands/)
  {ROOT_DIR}/videos/              — Central video storage (gitignored)
  {ROOT_DIR}/images/              — Central image storage
  {ROOT_DIR}/videos_transcription/ — Transcription files for downloaded videos
  {ROOT_DIR}/IPFS/                — IPFS evidence files and pin scripts
  {ROOT_DIR}/tmp/                 — Batch progress files for multi-URL processing

CK_FILE is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt   ← READ-ONLY TO AI. NEVER WRITE.
  (Real file. Moved 2026-09-19. ~/BGit/Bryan_git/charlie-kirk/Charlie_Kirk.txt is now a symlink to it —
   use that only to verify the location; always read and write the real path.)
CK_INBOX is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk_AI_Inbox.txt   ← AI writes new text HERE
  (Real file. Moved 2026-09-19. ~/BGit/Bryan_git/charlie-kirk/Charlie_Kirk_AI_Inbox.txt is now a symlink to it —
   use that only to verify the location; always read and write the real path.)
SITE_DOCS_DIR is dir {ROOT_DIR}/site/docs/
TRANSCRIBE_JS is file ~/BGit/all/tools/Transcription/Transcribe.js
TRANSCRIBE_CONFIG is file {ROOT_DIR}/tmp/transcribe_config.yaml

HISTORY_DIR is dir ~/T/_ck_skill/history/
RUN_LOG is file {HISTORY_DIR}{YYYY-MM-DD}_{HH-MM-SS}.md


============================
RUN LOG (MANDATORY, BOTH MODES)
============================

Every single invocation of this skill writes exactly one run-log file. This is in
ADDITION to all the work the skill already does — it never replaces or shortcuts a
step. Its purpose is post-hoc debugging: months later Bryan must be able to read
one file and know what was passed in, what the skill decided, what commands it
ran, what came back, and what it wrote.

* FIRST ACTION OF EVERY RUN, before parsing input, before any fetch:

  ```bash
  mkdir -p ~/T/_ck_skill/history
  ```

  Compute the run stamp from the real clock (`date "+%Y-%m-%d_%H-%M-%S"`) and set
  RUN_LOG to {HISTORY_DIR}{stamp}.md. Do not invent a timestamp. Immediately write
  the header block (verbatim input, mode, cwd) so a run that dies mid-way still
  leaves a log naming its input.

* APPEND AS YOU GO — do not buffer the whole log to the end. After each step
  completes or fails, append its entry. A crashed or context-exhausted run must
  still leave a partial log showing the last step reached. If a step fails, the log
  entry says FAILED and records the exact stderr, not a summary.

* Log format:

  ```markdown
  # ck_add_text run {stamp}

  ## Input
  Mode: {X POST MODE | ADD TEXT MODE}
  Raw TEXT_INPUT_TO_SKILL (verbatim, including any line breaks or URL wrapping):
  ```
  {exact raw input}
  ```
  Parsed URLs: {list, one per line, after un-wrapping}
  Flags: skip_video={y/n} transcribe={y/n} target_section={... or none}

  ## Steps
  | # | Step | Result | Detail |
  |---|------|--------|--------|
  | 1 | Fetch post | OK | {post_id} @{user}, has_video={y/n} has_images={n}, quoted={id or none} |
  | 6 | Video download | OK/FAILED/SKIPPED | {filename}, {bytes}, yt-dlp exit {code} |
  | 6b | IPFS pin | OK/FAILED | CID {cid} |
  | 6b2 | Public gateway verify | OK/FAILED | http {code}, content-type {type}, {ms} |
  | 9H-1 | Media in source file | PASS/FAIL | grep -c {cid} {page} = {n} |
  | 9H-2 | Gateway at publish time | PASS/FAIL | http {code}, content-type {type} |
  | 9H-3 | Pushed to origin/main | PASS/PENDING/FAIL | ahead/behind {a}/{b}, cid in remote = {n} |
  | 9H-4 | Pages deploy | PASS/FAIL/SKIPPED | run {id}, {conclusion} |
  | 9H-5 | Live page | PASS/FAIL/SKIPPED | curl {url} → cid count {n} |
  | ... | | | |

  ## Commands run
  Each media/IPFS/transcription command, verbatim, with its exit code and the
  first + last 10 lines of output. yt-dlp failures get their FULL stderr.

  ## Media outcome
  Video file: {path or NONE — why}
  Video CID: {cid or NONE}
  Publicly retrievable: {yes | NO — reason}
  Remote pin: {service + result, or NONE CONFIGURED}
  Player emitted on page: {yes | no — why not}
  Images: {paths + CIDs, or none}

  ## Files written
  {one line per file created or modified, with created/modified and line delta}

  ## Warnings and unfinished business
  {every gap, skipped step, unverified CID, or manual follow-up Bryan must do.
   If there are none, write "none".}
  ```

* The log is written for BOTH modes. In ADD TEXT MODE the media sections read
  "n/a (add text mode)".

* In MULTI-POST MODE there is ONE log file for the whole batch, with a `## Steps`
  table and `## Media outcome` block per post under a `### {post_id}` heading.

* The log lives outside the repo (~/T/) on purpose — it is a debug artifact, never
  committed, never published.

* Tell the user the log path in the Step 10 summary.


============================
RULES
============================

* {CK_FILE} (Charlie_Kirk.txt) IS READ-ONLY TO AI. See the ABSOLUTE RULE at the
  top of this skill. Do NOT write to it, not even additively. All new investigation
  text goes to {CK_INBOX} = ~/BGit/all/politics/charlie_kirk/Charlie_Kirk_AI_Inbox.txt
  instead, append-only, and Bryan merges it by hand.

* NEVER remove, delete, or reduce any existing text in {CK_FILE} or {CK_INBOX}.
  Every character that existed before must still exist after.

* NEVER rewrite, rephrase, or "clean up" existing content. Existing text stays
  exactly as-is, typos and all.

* The new text you insert should be lightly formatted to match the style of the
  file (plain text, no markdown headers, asterisk bullets if needed) but preserve
  the user's words and meaning.

* If the user provides a source URL, include it on its own line near the top of
  the inserted block.


============================
SECTION FORMAT
============================

The file uses equal-sign section headers. The pattern is:

    (blank line)
    =============== Section Title ==================
    (content lines)
    (blank line before next section)

The number of equal signs varies slightly but aim for roughly this pattern:
  * At least 12 equal signs before the title
  * At least 12 equal signs after the title
  * A space between the equal signs and the title text
  * One blank line before the header line
  * Content starts on the next line after the header
  * One or more blank lines before the next section header


============================
STEPS (ADD TEXT MODE)
============================

STEP 1: Read the file
* Read {CK_FILE} fully. Note every section header and its line number.
* Build a mental list of sections and their topics.

STEP 2: Analyze the new text
* Determine the topic(s) of the text the user wants to add.
* Identify which existing section is the best match.
* If no existing section is a reasonable match, decide on a new section title.

STEP 3: Decide placement
* If an existing section matches:
  - Insert the new text at the END of that section (before the blank lines
    that precede the next section header).
  - Do NOT insert in the middle of existing content.
* If creating a new section:
  - Place it immediately AFTER the most related existing section.
  - MANDATORY: Before writing any content, FIRST insert a section header line
    using the equal-sign format. Example:
      =============== Your Section Title ==================
    The header MUST appear before any new content. Never add content without
    its own section header when creating a new section.
  - Choose a short, descriptive title matching the style of existing headers.

STEP 4: Insert the text
* Use the Edit tool to insert text. The edit must be purely additive.
* After editing, verify that:
  - No existing text was removed or changed.
  - The new text appears in the correct location.
  - Section header formatting is consistent with the rest of the file.

STEP 5: Confirm to the user
* Tell the user:
  - Which section the text was added to (existing or new).
  - The line number range of the insertion.
  - A one-line summary of what was added.


============================
X POST MODE
============================

This mode processes one or more X/Twitter post URLs. For each URL it:
  1. Fetches the post data via the X API
  2. Downloads any video attachments
  3. Downloads any image attachments
  4. Pins media to IPFS for permanent hosting
  5. Transcribes videos automatically (unless toggled off)
  6. Adds the post text and transcription to {CK_INBOX} (never to {CK_FILE})
  7. Creates or updates Docusaurus site pages with embedded media
  8. Converts .md pages to .mdx when embedding media
  9. Updates IPFS pin scripts and video indexes
  10. Adds X post links to every modified page


============================
X POST STEP 0: PARSE INPUT AND DETECT MULTI-URL MODE
============================

Parse TEXT_INPUT_TO_SKILL to identify all components:

**Component 1: One or more X/Twitter URLs**
* URLs containing /status/ from x.com or twitter.com
* Examples:
    https://x.com/redpillb0t/status/2039976250429640891
    https://twitter.com/someuser/status/1234567890

**Component 2: Video URL**
* A direct video URL (not an X post URL)
* If the X post already has a video attachment, this is redundant

**Component 2b: Image URL**
* A direct image URL (.jpg/.png/.webp/.gif)
* If the X post already has image attachments, those are handled automatically

**Component 3: Site Section**
* An optional hint about which site/docs/ directory this content belongs in
* E.g., "FBI", "CoverUp", "Israel", "Ballistics"
* If provided, skip auto-detection and use this section for ALL posts
* If NOT provided, auto-detect per post from post content (Step 3)

**Component 4: Text Block**
* Additional text/notes to add alongside the X post content
* Applied after the X post content is processed

**Component 5: Video Flags**
* Video transcription is AUTOMATIC by default for any post that has a video.
  TRANSCRIBE_REQUESTED = true unless overridden.
* If the input contains the phrase "skip transcription" or "transcription off"
  or "no transcription" (case-insensitive), set TRANSCRIBE_REQUESTED = false.
* If the input contains "transcription on" (case-insensitive), set
  TRANSCRIBE_REQUESTED = true (this is the default, but useful to re-enable).
* If the input contains "don't transfer video" or "don't download video" or
  "no video" (case-insensitive), set SKIP_VIDEO = true. This skips video
  download (Step 6), transcription (Step 7), and transcription processing
  (Step 8) entirely. Images are still downloaded unless separately skipped.
* If SKIP_VIDEO = true, set TRANSCRIBE_REQUESTED = false.

**Transcription Toggle Persistence:**
* Check {TRANSCRIBE_CONFIG} for a saved default:
  ```yaml
  transcribe_default: true   # or false
  ```
  If the file exists, use its value as the default instead of true.
  If the file does not exist, the default is true (transcription ON).
* If the user says "transcription off" or "transcription on" WITHOUT any URLs,
  update {TRANSCRIBE_CONFIG} and confirm:
    "Transcription default set to {on/off}. Future videos will {be/not be}
     transcribed automatically."
  Then stop — do not proceed to Step 1.
* If the user provides URLs AND a transcription flag, the flag applies to THIS
  run only and does NOT change the persisted default.

Parse rules for URL pairing (same as holon skill):

  0. UN-WRAP LINE-BROKEN URLS FIRST, BEFORE TOKENISING. Input is often pasted from
     a terminal, phone, or transcription that hard-wrapped a URL mid-way, e.g.:

       https://x.com/TarynEllez7/status/2086589506
       967265670?s=20

     Treated naively this yields the status id 2086589506 — a valid-looking but
     wrong id, and the X API returns "not found" or the wrong post, so no video is
     ever downloaded. This has silently broken real runs.

     Repair rule: if a line ends inside an X status URL (it matches
     `/status/\d+$` with no trailing punctuation) and the NEXT line begins with
     digits, join the two lines with no separator. Repeat until no more joins
     apply. Do the same for any line ending in `/` or `status` with digits on the
     next line.

     After un-wrapping, VALIDATE every X status id: it must be 15–20 digits. If an
     id is shorter, do not proceed with it — stop and ask the user to re-paste that
     URL, and log the rejected id in {RUN_LOG}. A truncated id must never be sent
     to the X API and quietly turned into a "post has no video" conclusion.

     Also strip tracking suffixes (`?s=20`, `?t=...`) before use, and record both
     the raw and the repaired URL in {RUN_LOG} under "## Input".

  1. Split the (un-wrapped) input into non-empty tokens by line. Blank lines are
     separators.

  2. Identify each token as one of:
     - X_URL: a URL containing "/status/" (X.com or Twitter.com post)
     - DIRECT_VIDEO_URL: a video URL not containing "/status/"
     - DIRECT_IMAGE_URL: a direct image URL (.jpg/.png/.webp/.gif)
     - SITE_SECTION: a non-URL token matching a directory name under {SITE_DOCS_DIR},
       OR any token that looks like a directory-style name that appears immediately
       before an X_URL with no intervening blank line
     - TEXT_BLOCK: a token that doesn't fit any above category
     - SKIP_VIDEO_FLAG: "don't transfer video", "don't download video", "no video"
     - TRANSCRIBE_FLAG: "skip transcription", "transcription off", "no transcription",
       or "transcription on"

  3. Build a PAIRS list. Walk through the token list and pair each X_URL with the
     SITE_SECTION that immediately precedes it (no blank line between them):
     - If a SITE_SECTION token appears and the very next non-blank token is an
       X_URL → they form a named pair:
         { url: X_URL, section: SITE_SECTION }
     - If an X_URL has no preceding SITE_SECTION → unnamed pair:
         { url: X_URL, section: null }

  4. Handle the "one name, many URLs" pattern:
     If a single SITE_SECTION directly precedes a run of multiple consecutive
     X_URLs (no blank lines between), assign that section to all URLs in the run.

  5. If a single SITE_SECTION appears in the input but no URL-pairing could be
     established, treat it as a global default section for ALL unnamed pairs.

  6. Any token that is not an X_URL, SITE_SECTION, DIRECT_VIDEO_URL,
     DIRECT_IMAGE_URL, SKIP_VIDEO_FLAG, or TRANSCRIBE_FLAG is part of a
     TEXT_BLOCK and applies to all posts.

* After parsing, output the resolved PAIRS list:
  ```
  ============================================
  Input Parsed
  ============================================
  Pairs to process:
    1. URL: {url}
       Section: {section or "auto-detect"}
    2. URL: {url}
       Section: {section or "auto-detect"}
    ... (one entry per pair)
  Direct video URL: {url or "none"}
  Direct image URL: {url or "none"}
  Text block: {yes/no — brief summary}
  Skip video: {yes/no}
  Transcribe video: {yes (default) / no}
  Mode: {SINGLE POST | MULTI-POST — {count} posts}
  ============================================
  ```

* **MULTI-POST MODE**: If 2 or more X post URLs are present, process them using
  the checkpoint system described in Step 0B below. Any global text block or
  transcribe flag applies to ALL posts.


============================
X POST STEP 0B: CHECKPOINT & BATCHING (multi-post mode only)
============================

SKIP IF: Only 1 X post URL was parsed in Step 0 (single-post mode).

PROGRESS_FILE is file {ROOT_DIR}/tmp/batch_progress.yaml

The checkpoint system ensures that if processing is interrupted (context exhaustion,
error, user abort), completed work is preserved and processing can resume from where
it left off.

* 0B-1. Check for an existing progress file at {PROGRESS_FILE}:

  If the file exists, read it. It contains:
  ```yaml
  batch_id: '{timestamp}'
  started: '{YYYY-MM-DD HH:MM}'
  total_urls: {n}
  completed:
    - url: '{url}'
      post_id: '{id}'
      section: '{section_dir}'
      status: 'done'
  failed:
    - url: '{url}'
      error: '{reason}'
  remaining:
    - url: '{url}'
      section: '{paired section or null}'
  sections_modified: ['FBI', 'CoverUp']
  pages_created: ['site/docs/FBI/some-page.mdx']
  pages_modified: ['site/docs/CoverUp/overview.md']
  ```

  Compare the URLs in the progress file against the current PAIRS list:
  - URLs listed under `completed:` → SKIP these entirely. They are done.
  - URLs listed under `failed:` → retry them (user is re-running to fix failures).
  - URLs listed under `remaining:` → process these.
  - Any URLs in the current PAIRS list that are NOT in the progress file → add them
    to the processing queue (new URLs added since last run).

  Output:
  ```
  ============================================
  Resuming from Checkpoint
  ============================================
  Progress file: {PROGRESS_FILE}
  Previously completed: {n} posts
  Previously failed: {n} posts (will retry)
  Remaining to process: {n} posts
  New URLs not in checkpoint: {n} posts
  Total to process this run: {n}
  ============================================
  ```

* 0B-2. If NO progress file exists, create one:
  ```bash
  mkdir -p {ROOT_DIR}/tmp
  ```
  Write the initial progress file with all URLs under `remaining:` and empty
  `completed:` and `failed:` lists. Set batch_id to the current timestamp
  (YYYYMMDD_HHMMSS format). Set sections_modified, pages_created, and
  pages_modified to empty lists.

  Output:
  ```
  ============================================
  New Batch Started
  ============================================
  Batch ID: {batch_id}
  Progress file: {PROGRESS_FILE}
  Total posts to process: {n}
  ============================================
  ```

* 0B-3. Build the PROCESSING_QUEUE from the progress file: all URLs that need
  processing (remaining + failed retries + new URLs). Preserve section pairings
  from Step 0.

* 0B-4. Process each URL in PROCESSING_QUEUE one at a time. For each URL:

  a. Output a divider:
    ```
    ############################################
    Processing Post {n} of {total}: {url}
    Section: {paired section or "auto-detect"}
    Batch progress: {completed_count}/{total_count}
    ############################################
    ```

  b. Run Steps 1 through 9 for this URL. Step 10 (final summary) runs ONCE
     at the end after all URLs are done.

  c. After this URL completes (success or failure), IMMEDIATELY update the
     progress file:
     - Move the URL from `remaining:` to `completed:` (if success) or `failed:`
       (if error), with status details.
     - If a section was modified, add its name to `sections_modified:` (if not
       already listed).
     - Add any created/modified page paths to `pages_created:` / `pages_modified:`.
     - Write the file to disk. This is the checkpoint — if the conversation dies
       after this write, the next run picks up from here.

  d. **CONTEXT COMPACTION**: After updating the progress file, mentally release
     all intermediate data from this URL's processing. Do NOT retain in working
     memory:
     - The full xurl API response JSON
     - The full text of files read during section detection
     - The full text of site/docs/ files read during Step 9
     - OCR output text (already saved to YAML)
     - Transcription text (already saved to evidence file)

     DO retain (needed for deduplication and final summary):
     - The post_id, author, section, and status (1 line per URL)
     - List of files created or modified (filenames only, not contents)
     - Video/image CIDs (needed if a later URL references the same media)
     - The sections_modified list (needed for final summary)

     This compaction keeps the context window lean. The progress file on disk is
     the authoritative record — the context window only needs enough to process
     the current URL and know what was already done.

* 0B-5. **DEDUPLICATION ACROSS BATCH**: Before creating a new Level 3 page in
  Step 9, check whether a PREVIOUS URL in this batch already created that page.
  The retained list of files created (from 0B-4d) and the pages_created list in
  the progress file serve as the check. If the page already exists, update it
  instead of creating a duplicate.


============================
X POST STEP 1: FETCH THE POST
============================

SKIP IF: No X/Twitter URL for this post.

* Extract the post ID from the URL. X URLs look like:
  - https://x.com/{username}/status/{post_id}
  - https://twitter.com/{username}/status/{post_id}
  - The post_id is the numeric string after /status/

* Fetch the full post data using xurl with expanded fields. The expansions below also
  pull in any QUOTED tweet and its media — this is essential because media (video or
  images) is frequently attached to a quoted tweet, not to the post you were given:
  ```bash
  xurl "/2/tweets/{post_id}?tweet.fields=created_at,author_id,public_metrics,text,entities,conversation_id,lang,note_tweet,attachments,referenced_tweets&expansions=author_id,attachments.media_keys,referenced_tweets.id,referenced_tweets.id.attachments.media_keys,referenced_tweets.id.author_id&user.fields=name,username,description,public_metrics&media.fields=url,preview_image_url,type,width,height,duration_ms,variants" --auth app
  ```
  With these expansions, a quoted tweet's media appears in `includes.media`, the quoted
  tweet object in `includes.tweets`, and its author in `includes.users`.

* If xurl fails or returns an error, inform the user and stop processing this post.
  (If in multi-post mode, mark as failed and move to the next post.)

* **RESOLVE THE MEDIA SOURCE (quoted / linked status) — do this BEFORE printing the
  Has Video / Has Images line, so media is never silently dropped.** Media often does
  NOT live on the post you were given — it lives in a QUOTED tweet, or in a status URL
  pasted into the post's text:

  - Set MEDIA_SOURCE_URL = the original post URL and QUOTED_ORIGIN = none by default.
  - PARENT_HAS_MEDIA = true if `includes.media` contains an entry whose media_key is in
    THIS post's own `attachments.media_keys`. If true, keep MEDIA_SOURCE_URL = original
    post URL and skip the rest of this resolution.
  - If PARENT_HAS_MEDIA is false, find a quoted or linked status, in order:
      1. QUOTED TWEET: `referenced_tweets` entry with type == "quoted" → QUOTED_ID = its
         `id`; its media is already in `includes.media` (via the expansions).
      2. LINKED STATUS: else scan `entities.urls` for the FIRST `expanded_url` matching
         https://(x|twitter).com/{anyuser}/status/{digits} (ignore ?query) → QUOTED_ID =
         the digits after /status/.
      3. If QUOTED_ID came from the linked-status path and its media is not already in
         `includes.media`, fetch that status with the SAME xurl command (post_id =
         QUOTED_ID) and read its media, author, and text.
  - If media was found on the quoted/linked status:
      * MEDIA_SOURCE_URL = https://x.com/{quoted_username}/status/{QUOTED_ID} — the URL
        yt-dlp (Step 6) and curl (Step 6B) MUST download from, NOT the parent post.
      * QUOTED_ORIGIN = @{quoted_username}. Treat the quoted status's video/image
        attachments as this post's media for Steps 6 and 6B, and merge them into the
        temp YAML attachments block below.
  - If no media is found anywhere, the post genuinely has no media.

* Output to stdout — print the FULL POST TEXT so the user can immediately see what
  was downloaded:
  ```
  ============================================
  X Post Fetched: {post_id}
  ============================================
  Author: @{username} ({display_name})
  Date: {created_at}
  Likes: {like_count} | Retweets: {retweet_count} | Views: {impression_count}
  Has Video: {yes/no — if from a quote/link, write "yes (from quoted {QUOTED_ORIGIN})"}
  Has Images: {yes/no — count if yes; note "(from quoted {QUOTED_ORIGIN})" if applicable}
  Media source: {MEDIA_SOURCE_URL — only show if different from the original post URL}
  -------- POST TEXT --------
  {full text of post — print every word, no truncation}
  ---------------------------
  ============================================
  ```

* Save a TEMP YAML file immediately to /tmp/ck_xpost_{post_id}.yaml with the raw
  post data. This is a first-pass save before section detection — capture everything
  including all attachment URLs so nothing is lost if later steps fail.

  TEMP YAML format:
  ```yaml
  id: '{post_id}'
  url: '{original_url}'
  author:
    username: '{username}'
    name: '{display_name}'
    id: '{author_id}'
  text: |
    {full text of the post}
  created_at: '{created_at}'
  lang: '{lang}'
  public_metrics:
    retweet_count: {n}
    reply_count: {n}
    like_count: {n}
    quote_count: {n}
    bookmark_count: {n}
    impression_count: {n}
  attachments:
    videos:
      - type: video
        media_key: '{media_key}'
        duration_ms: {n}
        preview_image_url: '{url}'
        variants:
          - url: '{variant_url}'
            content_type: '{type}'
            bit_rate: {n}
    images:
      - type: photo
        media_key: '{media_key}'
        url: '{url}'
        width: {n}
        height: {n}
  investigation: 'charlie_kirk'
  added_date: '{today YYYY-MM-DD}'
  temp_file: true
  # If media came from a quoted/linked status (Step 1 media resolution), fill the
  # attachments block above with the QUOTED status's media, and record its origin:
  media_from_quoted_status:
    quoted_status_id: '{QUOTED_ID or ""}'
    quoted_status_url: '{MEDIA_SOURCE_URL if from a quote/link, else ""}'
    quoted_author: '{QUOTED_ORIGIN or ""}'
  ```

  Output: "Temp YAML saved: /tmp/ck_xpost_{post_id}.yaml"


============================
X POST STEP 2: OCR IMAGES IF POST TEXT IS SPARSE
============================

SKIP IF: No X post was fetched in Step 1.
SKIP IF: Post text has 20 or more meaningful words.
SKIP IF: Post has no image attachments.

* Many high-value posts are memes or screenshots — the real content is IN the image.

* Count meaningful words in the post text (words longer than 2 characters, excluding
  URLs, @handles, and #hashtags). If fewer than 20, attempt OCR.

* For each image attachment:

  2a. Download to temp:
    ```bash
    TMPIMG=$(mktemp /tmp/ck_ocr_XXXXXX.jpg)
    curl -L -o "$TMPIMG" "{image_url}?format=jpg&name=4096x4096"
    ```

  2b. Run OCR:
    ```bash
    tesseract "$TMPIMG" stdout --psm 3 2>/dev/null
    ```
    If tesseract not installed: "tesseract not found. Install with: brew install tesseract"
    Skip OCR for this image but continue.

  2c. Capture OCR output as OCR_TEXT. If it has more than 5 words:
    - Output the extracted text to stdout:
      ```
      ============================================
      OCR Text Extracted from Image
      ============================================
      {OCR_TEXT}
      ============================================
      ```
    - Append to the analysis pool for topic matching
    - Update the temp YAML to add an ocr_text field

  2d. Clean up: rm -f "$TMPIMG"

* Combine OCR text from all images into one analysis pool.


============================
X POST STEP 3: ANALYZE POST IN CK INVESTIGATION CONTEXT AND DETERMINE PLACEMENT
============================

* ANALYSIS POOL = post text + OCR text (if any) + text block (if provided)

* IMPORTANT: Read the analysis pool carefully in the context of the Charlie Kirk
  investigation. Understand what specific aspect of the investigation this post
  relates to — a specific incident, person, evidence category, timeline event,
  or theory. This understanding drives every placement decision below.

* If SITE_SECTION was provided in the input (from Step 0 pairing), use it directly.
  Resolve to a directory under {SITE_DOCS_DIR}.

* Otherwise, analyze the ANALYSIS POOL to determine which CK investigation topic
  this post relates to. Match against these topic directories:

  FBI/          — FBI involvement, cover-up, FBI blocking investigations
  CIA/          — CIA involvement theories
  Israel/       — Israel connections, Mossad
  CoverUp/      — Cover-up evidence, destroyed evidence
  Killer/       — Suspect analysis, Tyler Robinson
  Gun_Bullet/   — Ballistics, gun, bullet analysis
  Planes/       — N1098L, SAM flights, SU-BTT
  Drones/       — Drone sightings
  cameras/      — Surveillance camera analysis
  security/     — Security failures at UVU
  Before/       — Timeline events before the assassination
  After/        — Timeline events after the assassination
  People/       — Key individuals
  Censorship/   — Censorship of the investigation
  Motive/       — Motive analysis
  Proof_Intel_Services/ — Intelligence services involvement proof
  Proof_Not_Tyler/      — Evidence Tyler is not the shooter
  Fix/          — Legal reform proposals
  Influencers/  — Influencer coverage
  Media/        — Media analysis and response

* Store as TARGET_SECTION_DIR.

* LEVEL 2 / LEVEL 3 PAGE DETERMINATION (mandatory for X Post Mode):

  3a. Identify the Level 2 parent page:
    * The Level 2 page is the overview.md (or equivalent parent nav page)
      inside {SITE_DOCS_DIR}/{TARGET_SECTION_DIR}/.
    * Read that Level 2 page. Confirm it exists.
    * NEVER auto-create a new Level 2 page. If no existing Level 2 page is
      a reasonable fit, ASK the user:
        "No existing Level 2 page fits this content well. The closest is
         {TopicDir}/overview.md. Should I use that, or do you want a new
         Level 2 page created? (new Level 2 pages are rare)"
      Wait for the user's response before proceeding.

  3b. Identify or plan the Level 3 page:
    * List all existing .md and .mdx files in {SITE_DOCS_DIR}/{TARGET_SECTION_DIR}/.
    * Determine if an existing Level 3 page covers this specific sub-topic.
      - If YES: plan to add the new content to that existing Level 3 page.
      - If NO: plan to create a new Level 3 page. Choose a succinct, descriptive
        filename that captures the distinct sub-topic. Use lowercase-with-hyphens.
        Examples: uvu-public-contacts.md, fbi-evidence-request-denied.md,
        drone-sighting-sept-9.md
    * Store the decision as TARGET_L3_PAGE (existing path or new filename).

  3c. For roughly 95% of X posts, the right placement is: find the best Level 2
    parent, then create or update a Level 3 page under it. Only in rare cases
    does content belong directly on a Level 2 page.

* Also determine the best matching section in {CK_FILE} for the add-text step.
  Store as CK_SECTION_NAME.


============================
X POST STEP 4: SAVE POST DATA AS YAML
============================

SKIP IF: No X post was fetched in Step 1.

* Create directory if needed: {ROOT_DIR}/Research/x_posts/

* Save the post as a final YAML file: {ROOT_DIR}/Research/x_posts/{post_id}.yaml
  Include all fields from the temp YAML plus ocr_text if OCR was performed.
  Set temp_file: false.

* Delete the temp file:
  ```bash
  rm -f /tmp/ck_xpost_{post_id}.yaml
  ```


============================
X POST STEP 5: ADD POST TEXT TO MASTER INVESTIGATION FILE
============================

* Follow the same logic as ADD TEXT MODE Steps 1-5, using the post text + OCR text
  as the content to add.

* Format the insertion block as:

  Source: {original_url}
  Author: @{username} ({display_name})
  Date: {created_at}
  Likes: {like_count} | Retweets: {retweet_count} | Views: {impression_count}

  {full text of post}

  {OCR text if any, prefixed with "[Image text]: "}

* Insert into {CK_INBOX} under a heading naming the matching {CK_FILE} section
  (determined in Step 3 as CK_SECTION_NAME) so Bryan knows where it belongs.
  NEVER write to {CK_FILE} itself. Purely additive, never remove existing content.


============================
X POST STEP 5B: BUILD THE MEDIA INVENTORY (MANDATORY — DO NOT SKIP)
============================

Before downloading anything, write down an explicit, numbered inventory of every
media item attached to this post (and to any quoted/linked status resolved in
Step 1). Every later step iterates over THIS list. Steps 6, 6B, 9d, 9e and 9H are
each responsible for the WHOLE list, not for "the video" and "the image".

WHY THIS EXISTS: on 2026-07-21 a post with TWO videos
(https://x.com/hurtfeelingzday/status/2079661605332062718) produced ZERO media on
the site. Two separate assumptions caused it, and both are banned from here on:

  * The skill assumed "a post has at most one video". The download step writes
    `{post_id}.%(ext)s` — a single filename — so even a successful multi-video post
    can only ever leave one file behind.
  * The user's own wording said "get the two IMAGES on there". Both attachments were
    in fact VIDEOS. The run trusted the wording, looked for photos, found none, and
    stopped.

* 5B-1. Enumerate from `includes.media` — never from the user's wording, never from
  a guess. The user routinely calls a video "an image", "a pic", "the screenshot" or
  "the clip". Their wording tells you WHAT THEY WANT DONE WITH IT. It never tells you
  WHAT TYPE IT IS. Only `media.type` decides that, and it is authoritative:
    - type == "video" or "animated_gif" → a VIDEO item (Step 6)
    - type == "photo"                   → an IMAGE item (Step 6B)

* 5B-2. Build the list with a stable index, in the order the media_keys appear:

  ```
  MEDIA INVENTORY for {post_id}   (source: {original post | quoted @user})
    [1] video  828x476  20.1s  media_key 13_2079661564873875456
    [2] video  438x854  41.7s  media_key 13_2079661564869701632
  Videos: 2   Images: 0
  ```

  Print this block to stdout and copy it verbatim into {RUN_LOG} under "## Input".

* 5B-3. FILENAME RULE. When the inventory holds MORE THAN ONE video, every video
  filename is suffixed with its index: `{post_id}_1.mp4`, `{post_id}_2.mp4`. Never
  overwrite `{post_id}.mp4` twice. A single-video post keeps the plain
  `{post_id}.mp4` name so existing manifest rows continue to match.

* 5B-4. COMPLETION CONTRACT. At the end of the run, every row of this inventory must
  have reached one of exactly two terminal states, recorded per row in {RUN_LOG}:
    - PLACED  — downloaded, pinned, publicly verified, and embedded on a named page.
    - BLOCKED — deliberately not published, with a stated reason (banned in
      {BAN_IMAGES_CSV}/{BAN_VIDEOS_CSV}, copyright, user said skip, download failed).
  There is no third state. "I processed the post" is not a terminal state for a row.
  If any row is neither PLACED nor BLOCKED, the run is INCOMPLETE — say so in Step 10.


============================
X POST STEP 6: DOWNLOAD VIDEO(S) AND PIN TO IPFS
============================

SKIP IF: SKIP_VIDEO = true — user requested no video transfer.

LOOP: run this entire step ONCE PER VIDEO ROW in the Step 5B inventory. A post with
three videos runs Step 6 three times and ends with three CIDs and three players.

**DO NOT skip this step because Step 1 reported "Has Video: no".** The X API's
`includes.media` block is NOT a reliable signal for quote/repost videos — a true quote
tweet leaves the media_key on the quoted tweet, so the API returns no media even though a
video exists. yt-dlp walks quoted AND reposted media itself via GraphQL, straight from the
post URL. Therefore, whenever SKIP_VIDEO is false, ALWAYS attempt the yt-dlp download below
against the original post URL — regardless of what Step 1's detection found. Only conclude
the post has no video if yt-dlp itself finds nothing to download.

* All videos go to the central directory: {ROOT_DIR}/videos/
  Never store videos inside site/ or individual topic directories.

* First time setup: create directory and .gitignore if they don't exist:
  ```bash
  mkdir -p {ROOT_DIR}/videos
  ```
  Create {ROOT_DIR}/videos/.gitignore with:
  ```
  *.mp4
  *.mp3
  *.mkv
  *.avi
  *.mov
  *.wav
  *.webm
  ```
  Also ensure {ROOT_DIR}/.gitignore has a line for videos/:
  ```
  videos/
  ```

* 6-pre. CHECK FOR DUPLICATE before downloading:

  Read {ROOT_DIR}/videos/manifest.yaml and check whether this video already exists
  by matching ANY of these against every entry in the manifest:
    - source_url matches the X post URL or video URL
    - the post URL appears in the entry's `also_posted_as:` list
    - filename starts with the post_id

  IDENTITY IS THE BYTES, NOT THE POST ID. The same video is constantly re-posted,
  quoted, and re-uploaded under different status ids. Matching only on post_id makes
  the skill re-download and re-pin a file it already has. Real case: run
  https://x.com/juliandorey/status/2079257528513499568 and run
  https://x.com/ArtifexMemor/status/2079560806690324910 are byte-identical (sha256
  1e83d2d7…, CID QmTPZV4tV5…, 79 MB) — the second download was pure waste, and it
  briefly created two copies of the same 79 MB file on disk.

  Therefore, after ANY download completes (step 6a2), compute:
  ```bash
  shasum -a 256 {ROOT_DIR}/videos/{filename}
  ```
  and search the manifest for that sha256 BEFORE pinning. If it matches an existing
  entry:
    - DELETE the file you just downloaded — the repo keeps ONE copy per distinct video.
    - Reuse the existing entry's CID for embedding.
    - Append this post's URL to that entry's `also_posted_as:` list so the next run
      dedups before downloading instead of after.
    - Say so in the summary: "duplicate of {existing filename} — reused CID {cid}".

  Every NEW manifest entry must carry a `sha256:` field. Backfill it whenever you
  touch an entry that lacks one.

  Also scan {ROOT_DIR}/IPFS/ipfs.txt for the post_id as a secondary check.

  **Case A — Already in manifest AND file exists locally:**
    SKIP steps 6a through 6e entirely. Use the existing CID and filename for step 6f
    onward (embedding in site pages). Output:
    ```
    ============================================
    Video Already Exists — Skipping Download
    ============================================
    File: {ROOT_DIR}/videos/{manifest_entry.filename}
    IPFS CID: {manifest_entry.ipfs_cid}
    Gateway: {manifest_entry.ipfs_gateway_url}
    Source: {manifest_entry.source_url}
    ============================================
    ```

  **Case B — In manifest but file is MISSING locally:**
    Recover from IPFS:
    ```bash
    mkdir -p {ROOT_DIR}/videos
    ipfs get --output={ROOT_DIR}/videos/{manifest_entry.filename} {manifest_entry.ipfs_cid}
    ipfs pin add {manifest_entry.ipfs_cid}
    ```
    If IPFS retrieval succeeds, SKIP steps 6a through 6e. Use existing CID for 6f onward.
    If IPFS retrieval fails, fall through to step 6a and download fresh.

  **Case C — NOT in manifest:**
    Proceed to step 6a.

* 6a. Download using yt-dlp. Try the ORIGINAL post URL FIRST — yt-dlp resolves quoted and
  reposted media on its own, so the post URL alone downloads the video in the vast majority
  of cases. Only if that downloads nothing and a quoted status was resolved in Step 1, retry
  against MEDIA_SOURCE_URL:
  ```bash
  mkdir -p {ROOT_DIR}/videos
  yt-dlp "{original_post_url}" -o "{ROOT_DIR}/videos/{post_id}.%(ext)s" \
    || yt-dlp "{MEDIA_SOURCE_URL}" -o "{ROOT_DIR}/videos/{post_id}.%(ext)s"
  ```
  Never gate this on Step 1 detection — attempting the post URL directly is exactly what
  prevents quote/repost videos from being silently dropped.

  ALWAYS USE yt-dlp TO FETCH VIDEO. Do NOT download video with curl. The `variants[]`
  URLs that the X API hands back (video.twimg.com/…) are NOT a dependable download path —
  treat them as metadata for choosing quality, never as a fetch target. yt-dlp is the
  only supported downloader in this skill.

* 6a-multi. MULTI-VIDEO POSTS — still yt-dlp, driven as a PLAYLIST.

  A post with two or more videos is a playlist to yt-dlp, and a bare `-o {post_id}.%(ext)s`
  makes every entry collide on one filename. Give the output template a playlist index so
  each entry lands in its own file:
  ```bash
  yt-dlp --yes-playlist "{original_post_url}" \
    -S "res,tbr" \
    -o "{ROOT_DIR}/videos/{post_id}_%(playlist_index)s.%(ext)s"
  ```
  This yields {post_id}_1.mp4, {post_id}_2.mp4, … one per video row in the Step 5B
  inventory. Verified working on 2026-08-11 against the two-video post
  https://x.com/hurtfeelingzday/status/2079661605332062718, whose original run left the
  site with nothing at all.

  `-S "res,tbr"` is not optional. On HLS-only tweets yt-dlp's default pick can be a very
  low-bitrate rendition — on that same post it defaulted to the ~314 kbps variants when
  ~832 kbps was available. Sorting by resolution then total bitrate takes the best.

  For a SINGLE-video post keep the plain 6a command and the plain `{post_id}.mp4` name so
  existing manifest rows keep matching.

* 6a-fallback. If 6a produced FEWER files than the Step 5B inventory expects, retry
  against MEDIA_SOURCE_URL with the same playlist form, then try cookies:
  ```bash
  yt-dlp --cookies-from-browser chrome --yes-playlist "{original_post_url}" \
    -S "res,tbr" -o "{ROOT_DIR}/videos/{post_id}_%(playlist_index)s.%(ext)s"
  ```
  Never conclude "the post has no video" while the Step 5B inventory lists one. The
  inventory outranks a failed download: that combination is a FAILED DOWNLOAD, reported
  loudly, not an absent video.

* 6a2. VERIFY THE DOWNLOAD ACTUALLY PRODUCED A PLAYABLE FILE. yt-dlp can exit 0
  having written nothing, or having written a tiny fragment or an HLS manifest.
  Never trust the exit code alone:

  ```bash
  ls -la {ROOT_DIR}/videos/{post_id}.* 2>/dev/null
  ```

  Set VIDEO_DOWNLOAD_OK = true only if a file exists AND is larger than 100 KB AND
  `file` reports it as a media container. If VIDEO_DOWNLOAD_OK is false:
    - Set VIDEO_CID = none and VIDEO_PUBLIC_OK = false.
    - Log the FULL yt-dlp stderr to {RUN_LOG} under "## Commands run".
    - Do NOT proceed to 6b/6c/6c2/6c3 — there is nothing to pin, and writing a
      manifest/ipfs.txt row for a nonexistent file poisons the duplicate check on
      every future run.
    - Continue to the remaining steps (the page is still created from the post text
      and any images), but the page gets NO video player — see 9e.
    - Report it loudly in Step 10 as "VIDEO FAILED", not silently.

* 6b. Pin to IPFS:
  - Ensure the IPFS daemon is running:
    ```bash
    ipfs id > /dev/null 2>&1 || brew services start kubo
    ```
    Wait for the daemon to answer before adding. If the daemon cannot be started,
    set VIDEO_CID = none, VIDEO_PUBLIC_OK = false, log it, and skip to 6d.
  - Add and pin the video:
    ```bash
    ipfs add --pin {ROOT_DIR}/videos/{filename}
    ```
  - Capture the CID from the output (e.g. QmWepcax...)
  - Verify the pin:
    ```bash
    ipfs pin ls {CID}
    ```

* 6b2. PUBLISH THE CID TO THE NETWORK AND VERIFY A REAL VISITOR CAN FETCH IT.

  THIS IS THE STEP WHOSE ABSENCE CAUSED THE RECURRING "the video is not on the
  page" BUG. `ipfs add --pin` only makes the bytes available FROM THIS MACHINE.
  A page can therefore ship a perfectly correct-looking <video> tag whose CID has
  exactly one provider — Bryan's laptop — so the player is broken for every visitor
  whenever that machine is asleep, offline, or the daemon is stopped. Local
  `ipfs pin ls` succeeding proves NOTHING about the public site.

  - Announce the CID to the DHT so public gateways can find a provider:
    ```bash
    ipfs routing provide {CID}
    ```

  - Request a remote pin so the file survives this machine being off. Check for a
    configured service:
    ```bash
    ipfs pin remote service ls
    ```
    If a service is configured:
    ```bash
    ipfs pin remote add --service={service} --name="{post_id}.mp4" {CID}
    ```
    If NO remote service is configured, do not fail the run — but record
    REMOTE_PIN = "NONE CONFIGURED" in {RUN_LOG} and say so in the Step 10 summary,
    because it means this video's availability depends on one machine staying up.
    Recommend to the user once per run:
      "No IPFS remote pinning service is configured. Videos are served only from
       this machine, so players break when it sleeps. Configure one with:
         ipfs pin remote service add pinata https://api.pinata.cloud/psa {JWT}
       or route the file through Large File Bridge (~/BGit/Bryan_git/LargeFileBridge/)."

  - Verify retrievability THROUGH A PUBLIC GATEWAY, which is what a visitor's
    browser actually does. Do not skip this and do not substitute a localhost
    gateway check:
    ```bash
    curl -s -o /dev/null -w "http=%{http_code} type=%{content_type} t=%{time_total}\n" \
      --max-time 60 -r 0-1000 "https://ipfs.orbitor.dev/ipfs/{CID}"
    ```
    Set VIDEO_PUBLIC_OK = true ONLY if http is 200 or 206 AND content_type is a
    video type (video/mp4, application/octet-stream is acceptable for mp4 bytes).
    An HTML content-type means the gateway returned an error page — that is a
    FAILURE, not a success, even with http 200.

    If the first attempt fails, wait 20 seconds and retry once (DHT propagation of
    a fresh CID is not instant). Also test the second gateway in
    videos_planning/generator/ipfs_gateways.py:
    ```bash
    curl -s -o /dev/null -w "http=%{http_code} type=%{content_type}\n" \
      --max-time 60 -r 0-1000 "https://gateway.pinata.cloud/ipfs/{CID}"
    ```
    Do not test ipfs.io or dweb.link — both were retired in September 2026 and
    return 429/403 for every CID, so a failure there says nothing about ours.

  - Record in {RUN_LOG}: the CID, both gateway results verbatim, REMOTE_PIN, and
    the final VIDEO_PUBLIC_OK value.

  - If VIDEO_PUBLIC_OK is false, the video is downloaded and pinned locally but is
    NOT publicly servable yet. Still write the manifest, ipfs.txt, and videos.md
    rows (the bytes and CID are real). Set the manifest field:
    ```yaml
    public_verified: false
    ```
    and see 9e for what the page gets instead of a broken player.
    If VIDEO_PUBLIC_OK is true, write `public_verified: true`.

* 6c. Update manifest — append to {ROOT_DIR}/videos/manifest.yaml:
  ```yaml
  - filename: {filename}
    ipfs_cid: {CID}
    ipfs_gateway_url: https://ipfs.orbitor.dev/ipfs/{CID}
    source_url: {source_url}
    source_author: '@{username}'
    description: '{brief description from content}'
    added_date: '{today YYYY-MM-DD}'
    pinned: true
    public_verified: {true|false}   # from 6b2 — was it fetchable via a public gateway?
    remote_pin: '{service name | none}'
  ```

* 6c2. Update {ROOT_DIR}/IPFS/ipfs.txt — append the IPFS commands for this video:
  ```
  # {post_id}.mp4 — @{username} · {today YYYY-MM-DD}
  # {description up to 80 chars}
  ipfs get {CID}
  ipfs add "{filename}"
  ipfs pin add {CID}
  ```
  This file is the master IPFS pin script. Anyone who runs these commands on any
  IPFS node will download and rebroadcast the evidence file.

* 6c3. Create or update {ROOT_DIR}/videos/videos.md — a human-readable index:
  If the file does not exist, create it with this header:
  ```markdown
  # Video Evidence Index

  All videos downloaded from X/Twitter posts related to the Charlie Kirk investigation.
  Videos are pinned to IPFS for permanent, censorship-resistant hosting.

  ## How to access

  ```sh
  # Install IPFS: brew install kubo
  # Start daemon: ipfs daemon
  # Then run the commands from IPFS/ipfs.txt
  ```

  ## Video Index

  | File | IPFS CID | Description | Source | Date |
  |------|----------|-------------|--------|------|
  ```

  Append a new row to the Video Index table:
  ```
  | {filename} | `{CID}` | {description} | [@{username}]({source_url}) | {today} |
  ```

* 6c4. REGISTER THE VIDEO IN videos.yaml (MANDATORY — DO NOT SKIP):

  VIDEOS_YAML is file {ROOT_DIR}/videos/videos.yaml

  {ROOT_DIR}/videos/manifest.yaml is only this skill's own download log. It drives
  NOTHING. The MASTER video record for the whole site is {VIDEOS_YAML} — the video
  evidence hierarchy. It is what drives /Videos Level 5 page generation, the nav
  galleries on every Level 2 overview, the should_be_on_pages placement pass that
  puts a video onto ADDITIONAL Level 2 pages, the next_video chain, and the
  banned-media gate.

  A video that exists on disk, is pinned, and is embedded on the page this run
  wrote, but has NO entry in {VIDEOS_YAML}, is invisible to every one of those
  passes. It gets no Level 5 page, never appears in a gallery, and is never
  placed on any other page. From the reader's point of view the video "was never
  added" to every page except the single one this run touched.

  THIS IS THE SINGLE LARGEST FAILURE OF THIS SKILL. An audit on 2026-08-19 found
  41 videos downloaded between 2026-07-24 and 2026-08-19 that were pinned,
  verified, embedded, and committed — and none of them were ever registered. Five
  of them sit under Tyler_Robinson/ alone. Zero had been deleted; they had simply
  never entered the hierarchy. The image side of this skill got its registration
  step (6B-c4) on 2026-08-12 and its backlog stopped growing that day. The video
  side had no equivalent step at all until this one.

  NO BINDER WILL DO THIS FOR YOU — ON EITHER SIDE. `bind_video_pages.py` only
  records which existing Level 5 page hosts an ALREADY-REGISTERED video; it never
  creates an entry. Its image counterpart `bind_image_pages.py` is the same: binds
  only, never creates (the claim that it creates entries was wrong and was removed
  from step 6B-c4 on 2026-09-03). On the IMAGE side the creating script is
  `grow_hierarchy.py`'s Stage 6 page sweep; on the VIDEO side there is no page-sweep
  equivalent at all, which is why this step is manual. Nothing will notice this
  video unless you act here.

  BEWARE THE IDENTIFIER MISMATCH. {VIDEOS_YAML} stores CIDv0 (`Qm...`). Pages embed
  CIDv1 base32 (`bafybei...`) in the gateway URL. Grepping a page's `bafybei...`
  against {VIDEOS_YAML} therefore returns 0 even when the video IS registered, and
  grepping the `Qm` form against the page returns 0 even when it IS embedded.
  Convert before you compare:
  ```bash
  ipfs cid base32 {CID}     # Qm... -> bafybei...
  ```

  DO NOT hand-append a node to {VIDEOS_YAML}. It is a ~36,000-line nested hierarchy
  with per-node counters and it is rewritten by the pipeline. Instead queue it and
  run the intake stage:

  1. Register the embed identity so the pipeline can see it:
     ```bash
     cd {ROOT_DIR}
     python3 videos_planning/generator/scan_pages.py
     python3 videos_planning/generator/add_site_entries.py
     ```
     scan_pages.py walks the site and reports every embed identity the corpus does
     not already hold; add_site_entries.py appends a row for each to
     `videos_planning/generator/inventory.tsv`.

  2. Verify THIS video's CID is now queued, not just that the scripts exited 0:
     ```bash
     python3 -c "import json;d=json.load(open('videos_planning/generator/stage10_report.json'));print([k for k in d['new_entries'] if '{CID}' in k] or 'NOT QUEUED')"
     grep -c "{CID}" videos_planning/generator/inventory.tsv
     ```
     `NOT QUEUED` or a count of 0 means the embed on the page is not in a form the
     scanner recognises — fix the embed (Step 9e markup) and re-run. Do not
     proceed and do not report success.

  3. If {VIDEOS_YAML} itself must be updated in this run (the user asked for the
     video on more than the one page this run wrote, or asked for a Level 5 page),
     run the hierarchy pipeline: {ROOT_DIR}/videos_planning/p_update_video_hierarchy.md.
     It is a multi-stage run that rewrites {VIDEOS_YAML} and regenerates pages —
     say so before starting it, and commit first.

  4. Confirm and report honestly:
     ```bash
     python3 -c "import yaml;yaml.safe_load(open('videos/videos.yaml'));print('parses OK')"
     ```
     If the video is queued but the hierarchy has not been rebuilt yet, the run log
     and the Step 10 summary MUST say so in "Warnings and unfinished business":
     "videos.yaml does NOT yet carry this video — queued as a new_entry; no Level 5
     page and no gallery thumbnail until the hierarchy pipeline runs." Never report
     a video as fully added while it is only queued.

  5. COMMIT the queue change together with the page and the poster. An uncommitted
     inventory.tsv edit is the one the auto-commit sweeper's revert eats.

* 6d. Output:
  ```
  ============================================
  Video Downloaded & Pinned to IPFS
  ============================================
  File: {ROOT_DIR}/videos/{filename}
  Size: {file size}
  IPFS CID: {CID}
  Gateway: https://ipfs.orbitor.dev/ipfs/{CID}
  Publicly retrievable: {YES (http {code}, {type}) | NO — {reason}}
  Remote pin: {service + result | NONE CONFIGURED — served only from this machine}
  IPFS commands added to: IPFS/ipfs.txt
  Video index updated: videos/videos.md
  Registered in videos.yaml: {PASS — in hierarchy | QUEUED — new_entry only, no Level 5 page or gallery thumbnail yet | FAIL — not queued}
  ============================================
  ```

  If VIDEO_DOWNLOAD_OK is false, output this instead — never stay silent:
  ```
  ============================================
  VIDEO DOWNLOAD FAILED — page will have NO player
  ============================================
  Post: {post_url}
  yt-dlp exit: {code}
  Error: {last line of stderr}
  Tried: {original_post_url}{, then MEDIA_SOURCE_URL if applicable}
  Suggested fix: yt-dlp --cookies-from-browser chrome "{post_url}" \
    -o "{ROOT_DIR}/videos/{post_id}.%(ext)s"
  Logged to: {RUN_LOG}
  ============================================
  ```


============================
X POST STEP 6B: DOWNLOAD IMAGES AND PIN TO IPFS
============================

SKIP IF: No images available from the post or from a separate image URL.
NOTE: If Step 2 already downloaded images for OCR from temp paths, those were temp
  files — images still need to be downloaded fresh to {ROOT_DIR}/images/ here.

* All images go to: {ROOT_DIR}/images/
  Never store images inside site/ or individual topic directories.

* First time setup:
  ```bash
  mkdir -p {ROOT_DIR}/images
  ```

* Image URL extraction from X API response:
  - Images appear in "includes.media" array with type "photo"
  - For highest quality, append "?format=jpg&name=4096x4096" to the base URL
  - Record width and height from the API for aspect ratio in embeds

* 6B-pre. CHECK FOR DUPLICATE IMAGES before downloading:

  If {ROOT_DIR}/images/manifest.yaml exists, check each image against it:
    - source_url matches the X post URL or image URL
    - filename starts with the post_id

  MANDATORY sha256 CHECK — the filename check alone is NOT enough. When a post
  QUOTES another post, the same image bytes arrive under TWO different post_ids
  and both pass the filename check, producing two manifest entries, two ipfs.txt
  blocks, and two CIDs for one file. Real case: run 2026-08-12 added
  2087393163778347089_1.jpg twice because 2087396047064625425 quoted it.

  So after downloading (6B-a) and BEFORE pinning (6B-b), always:
  ```bash
  shasum -a 256 "{ROOT_DIR}/images/{filename}" | cut -d' ' -f1
  ```
  Search {ROOT_DIR}/images/manifest.yaml for that sha256. If it already appears
  under a DIFFERENT filename, this is the same image arriving through a quoted
  post. Delete the just-downloaded duplicate file, reuse the existing entry's CID
  for embedding, and write NO new manifest row and NO new ipfs.txt block.
  Output: "Duplicate image bytes: {new} == {existing} (CID: {cid}) — reusing"

  For each image:

  **Case A — In manifest AND file exists locally:**
    SKIP download and IPFS pin for this image. Use the existing CID for embedding.
    Output: "Image already exists: {filename} (CID: {cid})"

  **Case B — In manifest but file MISSING locally:**
    Recover from IPFS:
    ```bash
    mkdir -p {ROOT_DIR}/images
    ipfs get --output={ROOT_DIR}/images/{manifest_entry.filename} {manifest_entry.ipfs_cid}
    ipfs pin add {manifest_entry.ipfs_cid}
    ```
    If retrieval succeeds, use existing CID. If fails, fall through to 6B-a.

  **Case C — NOT in manifest:**
    Proceed to 6B-a.

* 6B-a. Download each image:
  ```bash
  curl -L -o "{ROOT_DIR}/images/{post_id}_{index}.jpg" "{image_url}?format=jpg&name=4096x4096"
  ```
  Where {index} is 1, 2, 3... for multiple images from the same post.

* 6B-b. Pin each image to IPFS:
  ```bash
  ipfs id > /dev/null 2>&1 || brew services start kubo
  ipfs add --pin {ROOT_DIR}/images/{filename}
  ```
  Capture the CID. Verify: ipfs pin ls {CID}

  NEVER use `ipfs add -n`. That is a DRY RUN: it prints a real-looking CID while
  storing no blocks, so the CID lands in the manifest and on the site and every
  public gateway then 504s forever. Only `ipfs add --pin` actually stores bytes.

* 6B-b2. Announce and PUBLICLY VERIFY each image:
  `ipfs pin ls` succeeding proves only that THIS machine has the bytes. It proves
  nothing about what a visitor to the live site will see.
  ```bash
  ipfs routing provide {CID}
  curl -s -o /dev/null -w "%{http_code} %{content_type} %{size_download}\n" \
    --max-time 60 "https://ipfs.orbitor.dev/ipfs/{CID}"
  ```
  Expect 200, an image/* content type, and a size matching the local file. If it
  is not 200, retry once against https://gateway.pinata.cloud/ipfs/{CID}. Record both results
  verbatim in {RUN_LOG}. Set IMAGE_PUBLIC_OK accordingly and set public_verified
  in the manifest row from it — never write `public_verified: true` unhecked.

  Also request a remote pin so the image survives this machine being off:
  ```bash
  ipfs pin remote service ls
  ipfs pin remote add --service={service} --name="{filename}" {CID}
  ```
  If no service is configured, set remote_pin: 'none' and say so in the Step 10
  summary rather than failing the run.

* 6B-c. Update image manifest — append to {ROOT_DIR}/images/manifest.yaml:
  ```yaml
  - filename: {filename}
    ipfs_cid: {CID}
    ipfs_gateway_url: https://ipfs.orbitor.dev/ipfs/{CID}
    source_url: {source_url}
    source_author: '@{username}'
    description: '{brief description}'
    width: {width_px}
    height: {height_px}
    sha256: {sha256 from 6B-pre}
    ocr_text_extracted: {true/false}
    added_date: '{today YYYY-MM-DD}'
    pinned: true
    public_verified: {true|false}   # from 6B-b2 — was it fetchable via a public gateway?
    remote_pin: '{service name | none}'
  ```

  Always write sha256 — it is what makes the 6B-pre duplicate check work on the
  next run, and it is the identity key used by images/ban_images.csv.

  After appending, verify the file still parses and gained exactly one entry:
  ```bash
  python3 -c "import yaml;d=yaml.safe_load(open('{ROOT_DIR}/images/manifest.yaml'));print(len(d))"
  python3 -c "
import yaml,collections
d=yaml.safe_load(open('{ROOT_DIR}/images/manifest.yaml'))
c=collections.Counter(e.get('filename') for e in d)
print('DUPLICATES:',{k:v for k,v in c.items() if v>1} or 'none')"
  ```
  If a duplicate filename is reported, remove the block you just added.

* 6B-c2. Update {ROOT_DIR}/IPFS/ipfs.txt — append IPFS commands for each image:
  ```
  # {filename} — @{username} · {today YYYY-MM-DD}
  # {one-line description}
  ipfs get {CID}
  ipfs add "{filename}"
  ipfs pin add {CID}
  ```
  First grep ipfs.txt for {CID}. If it is already present, do NOT append a second
  block — ipfs.txt is a run-once script and a repeated block re-downloads the same
  file. Verify afterwards that no CID appears twice:
  ```bash
  grep -o '^ipfs pin add .*' {ROOT_DIR}/IPFS/ipfs.txt | sort | uniq -d
  ```

* 6B-c3. GIT TRACKING GUARD (MANDATORY — DO NOT SKIP):

  Images must be COMMITTED to the repo, not merely present on disk. The live site
  serves them out of the repo via GitHub Pages, so an untracked or ignored image
  is a BROKEN IMAGE in production even though it looks perfect locally.

  Real case: on 2026-08-12 Large File Bridge appended per-file lines for the new
  images to {ROOT_DIR}/.gitignore, the images were never committed, and the new
  page shipped with two broken embeds. ~1,950 such lines were removed and the
  policy is now recorded in a banner at the bottom of .gitignore.

  For EVERY image file written this run — both the source copy in
  {ROOT_DIR}/images/ and the served copy under
  {ROOT_DIR}/site/internals/static/img/evidence/ — run:
  ```bash
  git -C {ROOT_DIR} check-ignore -v "{path}"
  ```
  - Exit code 1 (no output) means NOT ignored. Good. Continue.
  - Any output means the file IS ignored. Read which file and line matched:
      * Matched in {ROOT_DIR}/.gitignore  → this is the Large File Bridge bug.
        DELETE that line from .gitignore. Never work around it with `git add -f`,
        because the line stays and silently eats the next image too.
      * Matched in {ROOT_DIR}/images/.gitignore → this is a DELIBERATE privacy
        exclusion (hand-curated, currently 2 files). STOP. Do not un-ignore it,
        do not add it, and do not embed it on any page. Report it to Bryan.
      * Matched in {ROOT_DIR}/videos/.gitignore → correct and expected for video
        files. Videos are pulled from IPFS and never committed. Leave it.

  Then stage the image files:
  ```bash
  git -C {ROOT_DIR} add "{path}" ...
  git -C {ROOT_DIR} status --short -- images site/internals/static/img/evidence
  ```
  Every image from this run must show as `A ` (added) or already be tracked.
  If any still shows `??`, the run has FAILED — stop and report, do not proceed
  to Step 9 and publish a page that embeds a file git does not have.

  Never add a per-file image line to {ROOT_DIR}/.gitignore for any reason. To keep
  an image out of the repo use {ROOT_DIR}/images/.gitignore; to keep it off the
  public site use {ROOT_DIR}/images/ban_images.csv.

* 6B-c4. REGISTER THE IMAGE IN images.yaml (MANDATORY — DO NOT SKIP):

  IMAGES_YAML is file {ROOT_DIR}/images/images.yaml

  {ROOT_DIR}/images/manifest.yaml is only this skill's own download log. The
  MASTER image record for the whole site is {IMAGES_YAML} — the image evidence
  hierarchy. It is what drives /Photos Level 5 page generation, the nav
  galleries, the should_be_on_pages placement pass, the next_image chain, and the
  banned-media gate. An image that exists on disk and on a page but has no entry
  in {IMAGES_YAML} is invisible to every one of those passes: it never gets its
  own /Photos page, never appears in a gallery, and is never re-checked. Runs on
  2026-08-10 and 2026-08-12 all skipped this and left their images unregistered.

  KNOW WHICH SCRIPT DOES WHAT. Three generators touch {IMAGES_YAML} and they are
  NOT interchangeable. Naming the wrong one is how a run reports an image
  "registered" when nothing registered it:

    grow_hierarchy.py     THE PAGE SWEEP, and the one this step needs. Its Stage 6
                          walks every page under site/docs/, resolves each local
                          <img src> to a file, hashes it, and CREATES an entry for
                          any sha256 the corpus does not hold — filing it under the
                          node that MIRRORS THE PAGE IT FOUND IT ON. That last part
                          is why this script and not another: the page tells it the
                          topic, so a Mic page embed lands in the Mic cluster.
    add_orphan_images.py  Disk sweep, a BACKSTOP only. Walks images/ and the served
                          evidence dir and files anything unknown into
                          `Unfiled_Backlog`. It has no page context, so everything
                          it creates is UNFILED — no topic cluster, and no /Photos
                          page until something files it. Use it for an image that is
                          deliberately on no page, never as the primary path.
    bind_image_pages.py   BINDS ONLY. It scans site/docs/Photos/ for Level 5 pages
                          carrying a `ck_image_sha256:` frontmatter key and records
                          which page hosts which already-registered image. It walks
                          the rest of site/docs/ ONLY to collect video CIDs so it can
                          skip video entries. **It never creates an image entry.**
                          Running it on a brand-new image does nothing at all.

  This skill said for months that `bind_image_pages.py` "CREATES entries from any
  sha256 it finds embedded on a page". IT DOES NOT, and never did. On 2026-09-03 a
  run followed that instruction to the letter, ran the binder, and found no entry;
  it would have reported the image registered had it not checked. Verified against
  the source: bind_image_pages.py only ever walks PHOTOS_DIR for frontmatter.

  Placement still depends on embedding the image the durable way:

      <img src="/img/evidence/{sha256}.jpg" data-cid="{CID}" />

  An image embedded by IPFS gateway URL alone (`src="https://ipfs.io/ipfs/{CID}"`)
  carries no sha256, so the page sweep cannot resolve it to a file and the image
  never enters {IMAGES_YAML} at all. That is what happened to the 2026-08-10
  engraved-bullets image. Always use the `/img/evidence/{sha256}.jpg` src (Step 9d)
  and keep the CID in `data-cid`.

  What NO generator can know, and what this skill MUST supply, is exactly two
  fields — every one of them leaves both empty:

      cid:              the IPFS CID from 6B-b
      ai_description:   a one-paragraph description of what the image actually
                        depicts, written like the sibling entries in the file

  DO NOT hand-append whole nodes to {IMAGES_YAML}. It is a ~36,000-line nested
  hierarchy with per-node `number_of_images` / `number_of_images_recursive`
  counters, and it is REWRITTEN UNDER YOU by these generators and the auto-commit
  process — a working-tree edit made at the wrong moment gets reverted silently
  (observed 2026-08-12). Instead:

  1. Embed the image on the page first (Step 9d), with the sha256 src.
  2. Run the PAGE SWEEP so the entry is created in the RIGHT cluster:
     ```bash
     cd {ROOT_DIR}
     python3 image_planning/generator/grow_hierarchy.py
     ```
     Then CONFIRM it landed — never assume the script did it:
     ```bash
     grep -c "sha256: {sha256}" images/images.yaml     # must be 1, not 0
     ```
     A 0 means the embed is not in a form the sweep can resolve (wrong src, or the
     file is missing from site/internals/static/img/evidence/). Fix the embed and
     re-run. Only for an image deliberately on no page, fall back to
     `python3 image_planning/generator/add_orphan_images.py`, and then say plainly
     in the summary that it sits in Unfiled_Backlog with no topic cluster.
  3. Then patch ONLY the two empty fields, matched **by sha256** so the edit
     survives lines moving:
     ```bash
     cd {ROOT_DIR} && python3 - <<'PY'
     import re
     p='images/images.yaml'; src=open(p,encoding='utf8').read()
     sha='{sha256}'; cid='{CID}'; desc='{one-paragraph description}'
     src=re.sub(r'( *)cid: ""\n( *sha256: %s\n)'%sha,
                lambda m:'%scid: "%s"\n%s'%(m.group(1),cid,m.group(2)),src)
     src=re.sub(r'(sha256: %s\n *file_path: "[^"]*"\n)( *)ai_description: ""'%sha,
                lambda m:'%s%sai_description: "%s"'%(m.group(1),m.group(2),desc),src)
     open(p,'w',encoding='utf8').write(src)
     PY
     python3 -c "import yaml;yaml.safe_load(open('images/images.yaml'));print('parses OK')"
     ```
  4. Confirm the entry exists and both fields are non-empty:
     ```bash
     grep -B2 -A7 "sha256: {sha256}" images/images.yaml
     ```
  5. COMMIT the change in the same commit as the page and the image binary. An
     uncommitted {IMAGES_YAML} edit is the one the revert eats.

  A parse failure means the edit corrupted the file — restore it with
  `git checkout -- images/images.yaml` and redo it.

  DO NOT RUN THE PLACEMENT STAGE TO GET YOUR IMAGE ONTO A PAGE. This step's job
  is finished when the image is embedded on the page YOU wrote (Step 9d) and
  registered. It is tempting to reach for
  `image_planning/generator/place_should_be_images.py --apply` to spread it
  further. Do not, without Bryan asking:

    * It is WHOLE-CORPUS — there is no --page or --only flag. It rewrites the
      CK_PLACED_IMAGES block on every host page in one go.
    * It regenerates each block from {IMAGES_YAML}'s should_be_on_pages, and that
      field has drifted far behind what is actually on the pages. Measured
      2026-09-03: a dry run reported 662 pages edited and applying it produced
      5,090 deletions against 359 insertions — a net removal of roughly five
      thousand existing image placements. Reconciling that drift is its own job.
    * `plan_should_be.py plan`, which repopulates the field, is a SCRIPTED scorer
      working off each entry's ai_description. Where a description is wrong the
      assignment is wrong, and several were: on 2026-09-03 it put a muzzle-energy
      chart on `surrendering-vs-turning-himself-in` because the manifest
      description for that image was wrong (it is a portrait of Charlie Kirk).

  For ONE image on ONE topic page, hand-place it as Step 9d already describes and
  let grow_hierarchy.py record the page in on_site_pages. That is the whole job.

  Note the schema differs by node depth: mirrored level_4/level_5 page nodes use
  `on_site_pages: [...]`, while top-level level_3 cluster entries use `on_pages`,
  `should_be_on_pages`, `image_page`, `next_image`, and `banned`. Never invent
  keys — copy the exact key set already present on the sibling entries around the
  insertion point.

* 6B-d. Output:
  ```
  ============================================
  Image(s) Downloaded & Pinned to IPFS
  ============================================
  Files: {list of filenames}
  IPFS CIDs: {list of CIDs}
  Public gateway verified: {yes/no per CID — from 6B-b2}
  Remote pin: {service | NONE CONFIGURED}
  Duplicates skipped: {list, or none}
  Git: {n} file(s) staged, 0 ignored
  images.yaml: {n} entr(ies) added under {node key} — parses OK
  OCR performed: {yes/no — from Step 2}
  IPFS commands added to: IPFS/ipfs.txt
  ============================================
  ```


============================
X POST STEP 7: TRANSCRIBE VIDEO
============================

SKIP IF: TRANSCRIBE_REQUESTED is false.
SKIP IF: No video was downloaded in Step 6 — inform the user:
  "Transcription skipped — no video was downloaded."
NOTE: Transcription is ON BY DEFAULT. The user does NOT need to say "transcribe."

* Create output directory if needed:
  ```bash
  mkdir -p {ROOT_DIR}/videos_transcription
  ```

* Create a temp directory for transcription:
  ```bash
  TRANSC_TMPDIR=$(mktemp -d /tmp/ck_transcribe_XXXXXX)
  ```

* Run the transcription:
  ```bash
  cd "$TRANSC_TMPDIR" && node ~/BGit/all/tools/Transcription/Transcribe.js "{ROOT_DIR}/videos/{video_filename}" transcription.txt
  ```

* Wait for completion. This may take several minutes for long videos.

* Verify output:
  ```bash
  ls -la "$TRANSC_TMPDIR/transcription.txt"
  ```

* If transcription fails, inform the user and continue. Do not block on failure.

* Copy the transcription to the permanent location:
  ```bash
  cp "$TRANSC_TMPDIR/transcription.txt" {ROOT_DIR}/videos_transcription/{post_id}.md
  ```

* Read the transcription into memory.

* Clean up:
  ```bash
  rm -rf "$TRANSC_TMPDIR"
  ```

* Output:
  ```
  ============================================
  Video Transcribed (automatic)
  ============================================
  Video: {video_filename}
  Transcription: {ROOT_DIR}/videos_transcription/{post_id}.md
  Word count: {approximate word count}
  ============================================
  ```


============================
X POST STEP 8: PROCESS TRANSCRIPTION INTO INVESTIGATION FILE
============================

SKIP IF: Step 7 was skipped or transcription failed.

* Read the full transcription from {ROOT_DIR}/videos_transcription/{post_id}.md.

* Add the transcription content to {CK_INBOX} (NEVER {CK_FILE}), noting the same section as the post text
  (determined in Step 3). Format the insertion as:

  [Transcription of video from @{username}, {date}]
  Source: {original_url}

  {transcription text}

* Follow all ADD TEXT MODE rules — purely additive, never remove existing content.

* Analyze the transcription for additional people, facts, quotes, and claims
  that were not in the post text. Note any new people or topics discovered.
  These will be used to enrich the site page in Step 9.

* Also save a copy in the evidence directory:
  ```bash
  mkdir -p {ROOT_DIR}/Research/evidence
  cp {ROOT_DIR}/videos_transcription/{post_id}.md {ROOT_DIR}/Research/evidence/{post_id}_transcription.md
  ```


============================
X POST STEP 9: CREATE/UPDATE LEVEL 3 SITE PAGE WITH EMBEDDED MEDIA
============================

SKIP IF: No TARGET_SECTION_DIR was determined in Step 3.

This step uses the Level 2 / Level 3 decisions made in Step 3.

* 9a. RESOLVE THE TARGET LEVEL 3 PAGE

  Use TARGET_L3_PAGE from Step 3:

  **Case A — Existing Level 3 page:** Read it. Plan to append the new content
  at an appropriate location (usually at the end, before Related Areas if present).

  **Case B — New Level 3 page:** Create it. Choose a succinct, descriptive
  filename that captures the distinct sub-topic of this post. Use
  lowercase-with-hyphens. The filename should make the topic immediately clear.
  Good examples:
    * uvu-public-contacts.md
    * fbi-evidence-request-denied.md
    * drone-sighting-sept-9.md
    * erika-kirk-ceo-announcement.md

  **DEDUPLICATION CHECK (multi-post mode):** Before creating a new page, check
  the pages_created list from the batch progress file and the retained file list.
  If the same page was already created by a previous URL in this batch, update
  it instead.

* 9b. MDX CONVERSION (if media is involved)

  If creating a new page or updating an existing page that needs embedded media
  (video or images), use .mdx format:

  - If the target file is .md, convert it to .mdx:
    1. Rename the file from .md to .mdx
    2. Search all files under {SITE_DOCS_DIR} for links pointing to the old .md
       filename and update them to .mdx
    3. Do NOT modify sidebars.ts — the sidebar is managed separately

  - If creating a new page, create it as .mdx from the start

* 9c. PAGE CONTENT — NEAR-VERBATIM FROM THE POST

  IMPORTANT: When the X post or blog post contains substantive text, copy
  it nearly word for word onto the Level 3 page. Do not summarize,
  paraphrase, or condense. The goal is to preserve the full informational
  value of the original post on this page. Only light formatting adjustments
  are allowed (fixing line breaks, adding attribution, etc.).

  Page structure for a NEW Level 3 page:
    - Back button at the very top linking to the parent Level 2 page
    - Page title (H1) — descriptive of the specific sub-topic
    - Source attribution block: author, date, link to original post
    - Full post text (nearly verbatim, attributed: "According to @{username}...")
    - OCR text if extracted (attributed, nearly verbatim)
    - Transcription content if available (key quotes and full relevant passages)
    - Embedded images and/or video (see media embedding rules below)
    - Follow all defamation rules for living persons
    - Related Areas section at the bottom

  Page structure when APPENDING to an existing Level 3 page:
    - Add a ## sub-heading for the new content (e.g., "## @{username} Report, {date}")
    - Source attribution block
    - Full post text (nearly verbatim)
    - Embedded images/video
    - Keep all existing content intact

* 9d. IMAGE HANDLING

  Images from the post MUST be saved to {ROOT_DIR}/images/ (done in Step 6B)
  and embedded on the Level 3 page. Do not skip images — they often contain
  critical evidence (screenshots, documents, photos).

  IMAGE SRC IS THE sha256 PATH, NEVER THE CID. Images are served OUT OF THE REPO at
  /img/evidence/{sha256}.jpg (the copy Step 6B wrote to
  {ROOT_DIR}/site/internals/static/img/evidence/). Videos use IPFS gateway URLs;
  images do not. Two separate failures come from getting this backwards:
    * A CID-only `src` depends on a gateway finding a provider. With no remote pin
      configured, that provider is only this machine.
    * A CID-only `src` carries NO sha256, so grow_hierarchy.py's page sweep cannot
      resolve it to a file and the image never enters {IMAGES_YAML} — no /Photos
      page, no gallery, no placement, no verification. This is exactly how the
      2026-08-10 engraved-bullets image went unregistered for two days.
  Keep the CID in `data-cid` so the IPFS copy stays recorded and greppable.

  IMAGE EMBEDDING — use half-width, floated right, text flows around it:
  Single image:
  ```
  <div style={{float: 'right', width: '48%', maxWidth: '480px', marginLeft: '1.5rem', marginBottom: '1rem'}}>
    <img
      src="/img/evidence/{sha256}.jpg"
      data-cid="{CID}"
      alt="{description}"
      style={{width: '100%', height: 'auto', aspectRatio: '{width}/{height}', borderRadius: '4px'}}
      loading="lazy"
    />
    <p style={{fontSize: '0.85rem', color: '#666', marginTop: '0.5rem'}}>
      <em>{Description}. Source: <a href="{original_url}">@{username} on X</a>, {date}.</em>
    </p>
  </div>
  ```

  Multiple images from the same post (up to 4 attachments):
  ```
  <div style={{float: 'right', width: '48%', maxWidth: '480px', marginLeft: '1.5rem', marginBottom: '1rem'}}>
    <div style={{display: 'flex', flexWrap: 'wrap', gap: '0.5rem'}}>
      <img
        src="/img/evidence/{sha256_1}.jpg"
        data-cid="{CID_1}"
        alt="{description_1}"
        style={{width: 'calc(50% - 0.25rem)', height: 'auto', aspectRatio: '{w1}/{h1}', borderRadius: '4px'}}
        loading="lazy"
      />
      <img
        src="/img/evidence/{sha256_2}.jpg"
        data-cid="{CID_2}"
        alt="{description_2}"
        style={{width: 'calc(50% - 0.25rem)', height: 'auto', aspectRatio: '{w2}/{h2}', borderRadius: '4px'}}
        loading="lazy"
      />
    </div>
    <p style={{fontSize: '0.85rem', color: '#666', marginTop: '0.5rem'}}>
      <em>{Description}. Source: <a href="{original_url}">@{username} on X</a>, {date}.</em>
    </p>
  </div>
  ```

  These pages go PUBLIC — never a localhost / 127.0.0.1 URL (a visitor's browser would
  try a gateway on their own machine and fail).
  For VIDEO emit one <source> per gateway in videos_planning/generator/ipfs_gateways.py
  (orbitor, pinata, filebase, ipfs-lens, in that order) as shown in 9e. dweb.link,
  ipfs.io and w3s.link were retired in September 2026 — never emit them. For IMAGES the src is
  /img/evidence/{sha256}.jpg as shown above; note the
  CID in data-cid. The local daemon is only for pinning, not embeds.

* 9e. VIDEO EMBEDDING — use half-width, floated right, with text flowing around it.

  MANDATORY GATE — a post that had a video MUST end with either a working player on
  the page or an explicit, logged reason why not. Silently producing a page with no
  video for a video post is the single most common failure of this skill and is
  never acceptable.

  Decide from the flags set in Step 6:

  - VIDEO_DOWNLOAD_OK true AND VIDEO_PUBLIC_OK true → emit the full player below.
    This is the required outcome. Every other branch is a degraded fallback that
    must be reported.

  - VIDEO_DOWNLOAD_OK true, VIDEO_PUBLIC_OK false → the bytes exist locally but no
    public gateway can serve them yet. Emit the player anyway (the CID becomes
    valid the moment the file is remote-pinned or the daemon is reachable) AND add
    an MDX comment directly above it so the unverified state is visible in the
    source, plus a caption line pointing at the source post as the working fallback:
    ```
    {/* CK_VIDEO_UNVERIFIED {CID} — not retrievable via a public gateway as of {date}.
        Remote-pin this CID, then re-verify:
        curl -sI -r 0-100 https://ipfs.orbitor.dev/ipfs/{CID} */}
    ```
    Caption gains: `If the player does not load, watch the original on <a href="{post_url}">X</a>.`
    Record it in {RUN_LOG} under "## Warnings and unfinished business".

  - VIDEO_DOWNLOAD_OK false → there is no CID. Do NOT write a <video> tag with an
    empty, guessed, or other post's CID. Instead put a linked reference where the
    player would go:
    ```
    <p><em>Video: <a href="{post_url}">@{username} on X</a> ({duration}) — not yet
    mirrored to IPFS.</em></p>
    ```
    and log it as an outstanding item.

  - The post genuinely had no video (yt-dlp found nothing to download and Step 1
    reported no media) → no video section at all, and the run log says
    "no video present" rather than "video failed".

  Player markup:
  ```
  <div style={{float: 'right', width: '48%', maxWidth: '480px', marginLeft: '1.5rem', marginBottom: '1rem'}}>
    <video controls style={{width: '100%', height: 'auto', display: 'block', borderRadius: '4px'}}>
      <source src="https://ipfs.orbitor.dev/ipfs/{CID}" type="video/mp4" />
      <source src="https://gateway.pinata.cloud/ipfs/{CID}" type="video/mp4" />
      <source src="https://ipfs.filebase.io/ipfs/{CID}" type="video/mp4" />
      <source src="https://gw.ipfs-lens.dev/ipfs/{CID}" type="video/mp4" />
      Your browser does not support the video tag.
    </video>
    <p style={{fontSize: '0.85rem', color: '#666', marginTop: '0.5rem'}}>
      <em>{Description}. Source: <a href="{original_url}">@{username} on X</a>, {date}.</em>
    </p>
  </div>
  ```
  NEVER use cloudflare-ipfs.com — that gateway was shut down in 2024.
  NEVER use ipfs.io, dweb.link or w3s.link — retired September 2026 (429 / redirect to dweb.link).
  NEVER use `width="100%"` as an HTML attribute — use style={{width: '100%'}} only.

  If the video or images came from a quoted/linked status (QUOTED_ORIGIN is set), credit
  the original media poster in the caption, e.g. "Video by {QUOTED_ORIGIN}, quoted by
  @{username} on X" — link the caption to the original post URL the user gave.

  Always add clearfix div after the last floated element on the page:
  ```
  <div style={{clear: 'both'}} />
  ```

* 9e2. TRANSCRIPTION ON PAGE

  If transcription was performed in Step 7, add a "## Transcript Summary" or
  "## Key Statements" section below the video embed:
  - Include the most important quotes and claims from the transcription
  - If the transcription is short (under 500 words), include the full text
  - Always attribute: "From video testimony by {speaker}, {date}."
  - Look for NEW people, facts, and topics mentioned only in the video (not in
    the post text) and include those on the page

* 9f. UPDATE THE LEVEL 2 PAGE TOC — MANDATORY FOR NEW LEVEL 3 PAGES

  If a new Level 3 page was created, immediately update the parent Level 2
  page's TOC to include a link to the new page:

  * Read the Level 2 page (overview.md or equivalent).
  * Add a bullet entry for the new Level 3 page in the three-column TOC.
  * Re-balance columns so heights are equal or off by at most one row.
  * If the Level 2 page has no TOC yet, create one from scratch including
    all existing Level 3 pages in that directory plus the new one.
  * Verify: every .md and .mdx file in the directory (except the Level 2 page)
    must be linked from the TOC. If any are missing, add them now.

  This step is NOT optional. A Level 3 page without a link from its parent
  Level 2 page is an orphan and will never be found by readers.

* 9g. ADD X POST LINK TO EVERY MODIFIED/CREATED PAGE

  For EACH site page (.md or .mdx) that was modified or created in this step:

  9g-a. Check if the page already has a section titled "## X.com posts:"
    (case-insensitive match on the heading text).

  9g-b. If the section does NOT exist, add it at the very bottom of the page
    (but ABOVE the Related Areas section if one exists):
    ```
    ## X.com posts:
    ```

  9g-c. Under the "X.com posts:" heading, append a bullet with a hyperlinked
    summary of the post. The summary must be 10 words or fewer and describe what
    the post is about. The link text IS the summary; the URL is the original X
    post URL. Format:
    ```
    * [{10-word-or-less summary of the post}]({original_x_post_url})
    ```
    Example:
    ```
    * [Whistleblower reveals FBI destroyed CK evidence in 2025](https://x.com/someuser/status/123456)
    ```

  9g-d. If the section already exists, append the new bullet at the end of the
    existing bullet list. Do NOT duplicate — if the same URL is already listed,
    skip it.

  9g-e. Track whether at least one page received the X post link. Set
    X_LINK_PLACED = true if any page was updated with the link.

* 9g-f. FALLBACK: If X_LINK_PLACED = false (no page received the link):
  Check if {ROOT_DIR}/Research/collected_links.md exists. If not, create it:
  ```markdown
  # Collected Links

  X post links that were processed but not yet assigned to a specific site page.
  Review these periodically and move them to the appropriate page.

  ## X.com posts:
  ```
  Append the bullet to the "X.com posts:" section.

* If the content mentions people who have Details/ profiles, cross-link to them.


============================
X POST STEP 9H: VERIFY THE READER CAN ACTUALLY SEE IT
============================

SKIP IF: No site/docs/ page was created or modified in Step 9.

Everything up to here proves the work happened on THIS machine. It does not prove a
visitor to whoassassinatedcharliekirk.com can see it. Those are different claims, and
reporting the first as if it were the second is the single most common way this skill
has misled. This step closes that gap with four checks. Each one is a hard PASS or FAIL
that goes in the summary — never "probably fine", never inferred from the fact that an
earlier step succeeded.

WHY THIS EXISTS: on 2026-08-10 a video was correctly downloaded, pinned, transcribed,
and embedded, and the run reported complete. The reader saw no video, because the
GitHub Pages deploy was still in_progress. Nothing was broken; the skill simply stopped
reporting one link short of the reader. Separately, the older and more dangerous failure
is a CID hashed with `ipfs add -n` that lives on no node — the page renders a dead
player and the run still says "complete".

* 9H-1. SOURCE CHECK — is the media actually in the file on disk?

  THIS SITE HAS TWO EMBEDDING CONVENTIONS AND THEY USE DIFFERENT IDENTIFIERS. Grepping
  for the wrong one reports a perfectly good page as broken (and, worse, sends you off
  "fixing" it):

    - VIDEO  → embedded as an IPFS gateway URL. Grep for the **CID**.
        <source src="https://ipfs.orbitor.dev/ipfs/{CID}" type="video/mp4" />   (one per gateway)
    - IMAGE  → embedded as a locally-served evidence file. Grep for the **sha256**.
        <img src="/img/evidence/{sha256}.jpg" data-cid="{CID}" />
      The CID may appear in `data-cid`, but the src that a reader's browser actually
      loads is the sha256 path. An image audit that greps only for CIDs will report
      false failures on correctly-placed images — this happened during the 2026-08-11
      re-audit of 40 past runs and briefly flagged two healthy runs as broken.

  So, for each page modified or created, iterate the Step 5B inventory and grep for the
  identifier that matches that row's TYPE:
  ```bash
  grep -c "{CID}"     {page_path}    # video rows
  grep -c "{sha256}"  {page_path}    # image rows
  ```
  For image rows also confirm the served file really exists, because a missing file
  404s silently behind a page that looks fine:
  ```bash
  ls -la {ROOT_DIR}/site/internals/static/img/evidence/{sha256}.jpg
  ```
  Zero (or a missing static file) means the edit did not land. Do not proceed to the
  remaining checks for that page; report FAIL and say the edit was lost.

  EXISTING ON DISK IS NOT ENOUGH — the file must also be IN GIT. GitHub Pages builds
  from the repo, not from this machine, so an ignored or untracked evidence file
  renders locally and 404s for every real visitor:
  ```bash
  git -C {ROOT_DIR} ls-files --error-unmatch \
    "site/internals/static/img/evidence/{sha256}.jpg" \
    || echo "FAIL: NOT TRACKED IN GIT"
  git -C {ROOT_DIR} check-ignore -v \
    "site/internals/static/img/evidence/{sha256}.jpg"
  ```
  The first command must succeed; the second must produce no output. If either fails,
  this is the Step 6B-c3 failure reaching production — go back to 6B-c3, remove the
  offending .gitignore line, stage the file, and re-run this check. Report FAIL until
  both pass. This exact defect shipped two broken images on 2026-08-12.

* 9H-1b. INVENTORY RECONCILIATION — the check that would have caught the worst bug.

  Walk the Step 5B inventory row by row and assert every row is PLACED or BLOCKED
  (the 5B-4 contract). Print the table:
  ```
  [1] video  QmR3ycmF8…  PLACED   site/docs/Planes/Erika-Flight-Logs-Erased.mdx
  [2] video  Qmbwcn BJi…  PLACED   site/docs/Planes/Erika-Flight-Logs-Erased.mdx
  ```
  A row with no page and no stated reason is a FAILED RUN even when the page itself
  built, deployed, and looks complete. Report the count plainly:
  "Media inventory: {n} rows — {p} placed, {b} blocked, {u} UNACCOUNTED FOR."
  Any value of u above zero forbids printing "Complete".

* 9H-2. GATEWAY CHECK — re-confirm at publish time, not just at pin time.

  Step 6b2 already verified the CID when it was pinned. Re-run it here anyway, because
  a pin can be lost between steps and because this is the check whose result the reader
  actually experiences:
  ```bash
  curl -sI -m 45 -r 0-100 "https://ipfs.orbitor.dev/ipfs/{CID}" | head -5
  ```
  PASS requires **HTTP 200 AND a content-type of video/* or image/*.**
  A `content-type: text/html` is a gateway error page, not the file — that is a FAIL
  even though the status line may read 200. A 504 is a FAIL and almost always means the
  CID is on no reachable node (the `ipfs add -n` trap).
  On FAIL: say so plainly in the summary, name the CID, and state that the page will
  render a dead player until the file is pinned to a reachable node or a remote pinning
  service.

* 9H-3. COMMIT AND PUSH CHECK — did the edit leave this machine?

  This repo is auto-committed by an external process ("Bryan 26 Tower" / "Bryan 27
  Laptop"), so an edit may be committed by something other than this run. Do not assume
  either way — check:
  ```bash
  cd {ROOT_DIR}
  git status --short -- {page_path}
  git rev-list --left-right --count origin/main...HEAD
  git show origin/main:{page_path} | grep -c "{CID}"
  ```
  PASS requires the CID present in the **origin/main** copy — that is the only version
  the site builds from. A clean `git status` alone is NOT proof; neither is a local
  commit. If the change is uncommitted or unpushed, report it as PENDING and tell Bryan
  the auto-commit process has not picked it up yet. Do not commit or push to force it
  unless Bryan asks — the repo has its own commit process and the global rules forbid
  pushing without an explicit request.

  THE PAGE REACHING origin/main DOES NOT MEAN THE IMAGE DID. These are two separate
  files and they routinely travel in different commits. On 2026-08-12 the page commit
  (761084d1) went to origin/main and deployed, while the image binaries sat in a
  LATER, UNPUSHED commit (1ed73654) — so the live HTML referenced
  /img/evidence/<sha>.jpg for files origin/main did not contain, and every visitor
  got a 404 behind a page that verified green on every other check. Checking only the
  page is what let that ship.

  So for EVERY media row in the Step 5B inventory, check the BINARY separately:
  ```bash
  cd {ROOT_DIR}
  # the served copy the browser actually requests
  git cat-file -e origin/main:site/internals/static/img/evidence/{sha256}.jpg \
    && echo "IMAGE IN origin/main" || echo "FAIL: IMAGE NOT IN origin/main"
  # the source copy
  git cat-file -e origin/main:images/{filename} \
    && echo "SOURCE IN origin/main" || echo "FAIL: SOURCE NOT IN origin/main"
  ```
  Videos are exempt — `videos/*` is deliberately gitignored and served from IPFS.
  Images are NOT exempt: they are served out of the repo.

  Report each image as its own PASS/PENDING/FAIL line. If the page is in origin/main
  but an image is not, that is the WORST state, not a partial success — the page is
  live and visibly broken. Say exactly that, and say it will stay broken until the
  image commit is pushed.

* 9H-4. DEPLOY CHECK — did GitHub Pages rebuild?

  A push does not publish. The Pages workflow takes roughly 3–4 minutes.
  ```bash
  gh run list --limit 3
  ```
  Find the run triggered by the push containing this edit.
  - `completed / success` → proceed to 9H-5.
  - `in_progress` or `queued` → wait for it rather than reporting a false negative:
    ```bash
    gh run watch {run_id} --exit-status
    ```
  - `completed / failure` → FAIL. The most common cause in this repo is an MDX compile
    error, and the most common cause of THAT is an HTML comment `<!-- -->` in a .mdx
    file (must be `{/* */}`). Read the run log, name the real error in the summary, and
    fix it if it is in a file this run touched.

* 9H-5. LIVE PAGE CHECK — the only check that speaks for the reader.

  ```bash
  curl -s -m 60 "https://whoassassinatedcharliekirk.com{url_path}" | grep -c "{CID}"
  ```
  A count of 1 or more is PASS: the deployed HTML really contains the player.
  Zero is FAIL even if 9H-1 through 9H-4 all passed — that combination means the build
  dropped the content, and it is worth investigating rather than explaining away.

  THE HTML CONTAINING THE IDENTIFIER IS NOT THE SAME CLAIM AS THE READER SEEING THE
  MEDIA. Grepping the page proves the <img>/<video> TAG shipped. It says nothing about
  whether the thing the tag POINTS AT actually loads. For images the two come apart
  completely, because the grep target and the browser's request target are different
  strings:

      <img src="/img/evidence/{sha256}.jpg" data-cid="{CID}" />
                ^ what the browser fetches    ^ what a CID grep matches

  A CID-only grep therefore returns 1 on a page whose every image is a broken icon.
  That is exactly how the 2026-08-12 Rifle_Site_Kia_Soul_Turnaround failure passed:
  both sha256 strings were present in the deployed HTML, every earlier check was
  green, and both images returned **404** to every visitor because Large File Bridge
  had gitignored the served files.

  So for EVERY image row in the Step 5B inventory, FETCH THE IMAGE ITSELF:
  ```bash
  curl -s -o /dev/null -m 45 -w "img http=%{http_code} type=%{content_type} bytes=%{size_download}\n" \
    -L "https://whoassassinatedcharliekirk.com/img/evidence/{sha256}.jpg"
  ```
  PASS requires **http 200 AND a content-type of image/\*** AND a byte count close to
  the local file. A 404 is a FAIL. An `text/html` content-type is the site's 404 page
  dressed as a success and is also a FAIL. Do the same for any video poster:
  `/img/video_posters/{sha256}.jpg`.

  This is the one check that is causally downstream of everything — build, commit,
  push, deploy, ignore rules, file naming, extension mismatch, CDN. Whatever the cause,
  a broken image fails here. Never report an image as published without it.

* 9H-6. RECORD THE RESULTS.

  Write all five results into {RUN_LOG} as a table with the literal command output
  (status codes, counts, run ids) — not a summarised verdict. Then carry them into the
  Step 10 summary using the "Publication verification" block defined there.

  If any check FAILED or is PENDING, the run is NOT complete. Say which check failed,
  what the reader currently sees, and what would fix it. Never print "Complete" over a
  failed check.

* 9H-6b. REPO-WIDE PUBLICATION AUDIT (MANDATORY, FAST, LOCAL).

  Every check above is scoped to THIS run's media. That is not enough. A four-month
  audit on 2026-08-12 found damage that no single run would ever have noticed,
  because each run only ever looked at itself:

    * 85 downloaded images had never been copied to
      site/internals/static/img/evidence/ — nothing served them.
    * 265 page embeds used src="https://ipfs.io/ipfs/{CID}" instead of the local
      /img/evidence/{sha256}.jpg path. Most CIDs were produced with `ipfs add -n`
      and live on no node, so 11 of them returned 504 from the public gateway.
      Every one of those rendered perfectly on this machine and was broken for
      every real visitor.
    * 15 images were downloaded and pinned but never embedded on any page.

  So end every run with the whole-repo check, not just your own:

    python3 {ROOT_DIR}/image_planning/generator/audit_image_publication.py

  It exits 0 when clean and 1 when any image in {ROOT_DIR}/images/ is unserved,
  served-but-on-no-page, or banned-but-still-served. Banned and privacy-listed
  images are reported as WITHHELD and are never failures.

  Add `--gateway` (slow, needs network) to also probe every remaining ipfs.io
  <img> embed against the public gateway. Run that form whenever this run added
  or repointed an IPFS embed.

  Report the audit's RESULT line in the Step 10 summary. If it says FAIL, list the
  offending files. Images this run added must never appear in the failing lists —
  if they do, fix them before reporting the run complete. Pre-existing failures
  from older runs are NOT a reason to block this run: report them so Bryan can see
  the backlog, and say plainly that they predate this run.

* 9H-6c. REPO-WIDE VIDEO REGISTRATION AUDIT (MANDATORY whenever this run
  touched a video).

  The image audit above says nothing about video. Run:

    python3 {ROOT_DIR}/videos_planning/generator/audit_video_registration.py

  It exits 0 when every video in videos/manifest.yaml is present in the master
  {ROOT_DIR}/videos/videos.yaml, and 1 when any is not. It handles the
  CIDv0/CIDv1 conversion for you, and it reports separately the videos that are
  already embedded on a page (visible on exactly one page, invisible to every
  gallery and placement pass) from those on no page at all.

  A video THIS run added must never appear in that list. If it does, go back to
  Step 6c4 — it is queued at best, and saying "added" would be false.

  Pre-existing entries are a backlog, not a reason to block this run. Report the
  count in the Step 10 summary and say plainly that they predate this run. As of
  2026-08-19 that backlog is 41 videos dating to 2026-07-24, and clearing it
  requires the hierarchy pipeline (videos_planning/p_update_video_hierarchy.md),
  not this skill.

* 9H-7. TIME BUDGET.

  These checks add roughly 4–5 minutes, nearly all of it waiting on the Pages deploy.
  That is the correct trade — the alternative is telling Bryan something is published
  when it is not. If Bryan's input contains "skip verify" or "no verify"
  (case-insensitive), skip 9H-4 and 9H-5 only, and say plainly in the summary that
  deploy and live-page verification were skipped at his request and the live site is
  therefore unconfirmed. Never skip 9H-1, 9H-2, or 9H-3 — those are fast and local.


============================
X POST STEP 10: FINAL SUMMARY
============================

* **SINGLE-POST MODE** — output the post summary:
  ```
  ============================================
  ck_add_text X Post Complete
  ============================================
  Post: {post_id} by @{username} on {date}
  URL: {original_url}
  Post text (first 100 chars): {preview...}
  OCR performed: {yes — {word count} words | no}
  YAML saved: {path}
  Appended to CK_INBOX (Charlie_Kirk.txt NOT touched): {section name it belongs under}
  Video: {downloaded filename or "none" or "FAILED — see log"}
  Video IPFS CID: {CID or "none"}
  Video publicly retrievable: {YES | NO — {reason}}
  Remote pin: {service | NONE CONFIGURED}
  Player on page: {yes | no — {reason}}
  Images: {downloaded filenames or "none"}
  Image IPFS CIDs: {CIDs or "none"}
  Video skipped: {yes — user said no video | no}
  Transcription: {yes — saved to {path} | no — not requested | failed}
  Site pages updated: {list of files modified/created}
  X post link placed on: {list of pages}
  IPFS commands added: {yes/no}
  Local build: {SUCCESS | FAILED}            (Step 11a)
  Committed & pushed: {yes — {sha} | NO}     (Step 11c)
  Pages deploy: {success — run {id} | FAILED | not run}   (Step 11d)
  Live page: {http 200, video present | NOT LIVE — {reason}}  (Step 11e)
  Video durable: {yes — remote-pinned | NO — single provider, this machine}
  Run log: {RUN_LOG}
  -------- Media inventory reconciliation (Step 9H-1b) --------
  Inventory rows: {n}   Placed: {p}   Blocked: {b}   UNACCOUNTED: {u}
  {one line per row: [i] {type} {cid|sha256} {PLACED → page | BLOCKED → reason}}
  -------- Publication verification (Step 9H) --------
  Media in source file:   {PASS | FAIL — edit did not land}
  Public IPFS gateway:    {PASS — http 200, {content-type} | FAIL — {code}/{type}}
  Page in origin/main:    {PASS | PENDING — awaiting auto-commit | FAIL}
  Image binaries in remote: {PASS — {n}/{n} in origin/main | FAIL — {list sha256}}
  Registered in images.yaml: {PASS — {n} entr(ies) | FAIL — not registered}
  Registered in videos.yaml: {PASS — in hierarchy | QUEUED — new_entry only | FAIL — not queued | n/a — no video}
  Repo-wide image audit:  {CLEAN | FAIL — {n} unserved, {n} on no page (Step 9H-6b)}
  Pages deploy:           {PASS — run {id} success | FAIL — run {id}, {error} | SKIPPED}
  Live page contains it:  {PASS | FAIL | SKIPPED}
  Live media files load:  {PASS — {n}/{n} images+posters http 200 image/* | FAIL — {list sha256 + code} | SKIPPED}
  READER CAN SEE IT:      {YES | NO — {which check failed and what fixes it}}
  ============================================
  ```

* The final line is the one that matters. Print **YES** only when every non-skipped
  check passed AND the inventory shows zero UNACCOUNTED rows. If any check failed or is
  pending, print **NO** followed by the specific cause — and do not describe the run as
  complete anywhere in the reply.

* DURABILITY IS A STANDING GAP, NOT A PER-RUN SURPRISE. As of 2026-08-11 this machine
  has NO IPFS remote pinning service configured (`ipfs pin remote service ls` returns
  nothing), so every video on the site has exactly one provider: this machine. A 2026-08-11
  audit of 40 past runs found all 27 checked CIDs returning http 206 video/mp4 from
  ipfs.io — which proves they work WHILE this machine is up, and proves nothing beyond
  that. Say this plainly whenever REMOTE_PIN is "NONE CONFIGURED"; do not let a green
  gateway check stand in for durability.

* Before printing the summary, FINALISE {RUN_LOG}: make sure the Steps table has a
  row for every step attempted, the "## Files written" list matches what was
  actually written, and "## Warnings and unfinished business" names every gap
  (failed download, unverified CID, missing remote pin, page without a player).
  A run log that says "none" while the summary reports a failure is a bug.

* **MULTI-POST MODE** — after ALL posts and Step 0B loop finishes:

  Read the final state of {PROGRESS_FILE} to build this report:
  ```
  ============================================
  ALL POSTS PROCESSED — BATCH COMPLETE
  ============================================
  Batch ID: {batch_id}
  Total posts: {n}
  Successful: {n}
  Failed: {n} — {list URLs with error reasons}
  Sections modified: {list}
  Pages created: {list}
  Pages modified: {list}
  Videos downloaded: {n}
  Images downloaded: {n}
  Transcriptions completed: {n}
  IPFS pins added: {n}
  Videos NOT publicly retrievable: {n} — {list CIDs}
  Video posts that got no player: {n} — {list post ids + reason}
  Run log: {RUN_LOG}
  -------- Publication verification (Step 9H) --------
  Pages verified live: {n} of {n}
  Pages NOT yet live: {n} — {list page + which check failed}
  Pages deploy: {PASS — run {id} | FAIL — run {id}, {error} | SKIPPED}
  READER CAN SEE IT: {YES — all pages live | NO — {n} pages not visible}
  ============================================
  ```

  In multi-post mode, run 9H-1 through 9H-3 per page as each post finishes, but run the
  deploy check (9H-4) and live checks (9H-5) ONCE at the end of the batch — one push
  usually covers every page, so watching the deploy per post would waste minutes per
  post for the same answer.

* **BATCH CLEANUP**: After a successful batch (all posts processed, no remaining):
  - Rename the progress file to mark it complete:
    ```bash
    mv {ROOT_DIR}/tmp/batch_progress.yaml {ROOT_DIR}/tmp/batch_{batch_id}_done.yaml
    ```
  - This clears the way for the next batch. Old done files can be deleted manually
    or kept as a log of past batches.

* **INCOMPLETE BATCH**: If some posts remain unprocessed (context exhaustion,
  user abort), the progress file stays at {PROGRESS_FILE} with the remaining
  URLs still listed. Output:
  ```
  ============================================
  BATCH INCOMPLETE — RESUME AVAILABLE
  ============================================
  Completed this run: {n}
  Still remaining: {n}
  Progress file: {PROGRESS_FILE}

  To resume, run the same command again:
    /ck_add_text {paste the same URL list}
  Or just the remaining URLs — completed ones will be auto-skipped.
  ============================================
  ```


============================
X POST STEP 11: VERIFY THE READER ACTUALLY GETS IT (MANDATORY)
============================

SKIP IF: no files under {SITE_DOCS_DIR} were created or modified this run.

Steps 1-10 prove the skill did its work on THIS MACHINE. They prove nothing about
what a visitor sees. Two things decide that, and both must be checked before the
run is allowed to call itself complete:

  * the page reached the live site (the GitHub Pages deploy went green), and
  * the video the page points at is fetchable from a public gateway.

A run that stops at "site pages updated" has historically reported success while
the live site had no such page — or had the page with a player nobody could load.
Do not stop there.

* 11a. LOCAL BUILD FIRST. Never push a page that has not compiled:
  ```bash
  cd {ROOT_DIR}/site && npm run build 2>&1 | tail -20
  ```
  Require "[SUCCESS] Generated static files". An MDX compile error here is the
  cheapest place to catch it — a broken .mdx fails the Pages workflow and silently
  leaves the WHOLE site stale at its previous commit, not just this page.

* 11b. CONFIRM THE BUILT PAGE CONTAINS WHAT YOU THINK IT DOES. Pages build as
  `{name}.html` files, not directories — check the file, not a folder:
  ```bash
  F={ROOT_DIR}/site/build/{url_path}.html
  ls -la "$F"
  grep -c "{CID}" "$F"
  ```
  The build minifier STRIPS ATTRIBUTE QUOTES, so `grep '<source src="'` returns
  nothing on a perfectly good page. Match on the CID or the bare tag name, never
  on a quoted-attribute pattern, or you will diagnose a working page as broken.

* 11c. CONFIRM IT WAS COMMITTED AND PUSHED. This repo has an external auto-commit
  process ("Bryan 26 Tower" / "Bryan 27 Laptop") that may have already committed
  and pushed the files:
  ```bash
  git status --porcelain | head -30
  git status -sb | head -2
  ```
  If the new/changed site files are still listed as modified or untracked, they
  are NOT live no matter how green anything else is. Never create or switch
  branches; never push unless Bryan asked. If the files are uncommitted and Bryan
  did not ask for a commit, say so plainly in the Step 10 summary and record it in
  {RUN_LOG} as unfinished business — do not claim the page is live.

* 11d. WATCH THE PAGES DEPLOY TO COMPLETION:
  ```bash
  gh run list --limit 5
  gh run watch {run_id} --exit-status
  ```
  Green is the only acceptable outcome. If it failed, read the log
  (`gh run view {run_id} --log-failed`) and fix the cause — the most common is an
  HTML comment `<!-- -->` inside an .mdx file, which must be `{/* */}`. A red
  deploy means every page on the site is stale, so this is never "just this page's
  problem". Set DEPLOY_OK accordingly.

* 11e. FETCH THE LIVE PAGE AND ASSERT THE MEDIA IS IN IT:
  ```bash
  curl -s -o /tmp/ck_live.html -w "http=%{http_code}\n" -L "https://whoassassinatedcharliekirk.com{url_path}"
  grep -c "{CID}" /tmp/ck_live.html
  grep -c "<video" /tmp/ck_live.html
  ```
  Require http 200 AND the CID present AND a <video> tag (for a video post).

  THEN FETCH EVERY STATIC MEDIA FILE THE PAGE POINTS AT. Anything served out of
  site/internals/static/ 404s silently behind a page that looks perfect — the HTML
  is fine, the file is missing. Loop over the Step 5B inventory:
  ```bash
  # every image row
  curl -s -o /dev/null -w "img %{http_code} %{content_type} %{size_download}\n" \
    -L "https://whoassassinatedcharliekirk.com/img/evidence/{sha256}.jpg"
  # every video row's poster
  curl -s -o /dev/null -w "poster %{http_code} %{content_type}\n" \
    -L "https://whoassassinatedcharliekirk.com/img/video_posters/{sha256}.jpg"
  ```
  Each must return **200 with an image/\* content type**. A 404, or a 200 carrying
  `text/html` (the site's 404 page), is a FAILED RUN — say so and do not describe the
  images as published. See 9H-5 for why grepping the HTML does not substitute for this.

* 11f. RE-RUN THE PUBLIC GATEWAY CHECK FROM 6b2 one final time, after the deploy.
  This catches the case where the CID resolved during the run only because the
  bytes were still warm in a gateway cache.

* 11g. STATE THE DURABILITY CAVEAT HONESTLY. If REMOTE_PIN was "NONE CONFIGURED",
  the gateway check passing means "it works right now", NOT "it will keep working".
  The CID has a single provider — this machine. Say exactly that in the summary
  rather than reporting an unqualified success.

* Append an 11-row block to the {RUN_LOG} Steps table: local build, built-page
  contains CID, commit/push state, deploy conclusion + run id, live page http +
  CID present, poster http, post-deploy gateway result, remote-pin state.

* Add to the Step 10 summary:
  ```
  Local build: {SUCCESS | FAILED}
  Committed & pushed: {yes — {sha} | NO — files still uncommitted}
  Pages deploy: {success — run {id} | FAILED — run {id} | not run}
  Live page: {http 200, video present | NOT LIVE — {reason}}
  Video durable: {yes — remote-pinned to {service} | NO — single provider, this machine}
  ```


============================
IMPROVE MODE
============================

ASSESSMENT MANUAL — READ THIS FIRST
-------------------------------------
ASSESS_MANUAL is file /Users/bryan/BGit/Bryan_git/charlie-kirk/prompts/Assess_Manual.md

MANDATORY: Read this file FULLY into context before touching any page. The manual
defines all Level 2 and Level 3 page requirements. Every structural decision you
make must be validated against it. The manual is the authority — the summary below
is a quick reference only.

Absolute path: /Users/bryan/BGit/Bryan_git/charlie-kirk/prompts/Assess_Manual.md

SITE_DOCS_DIR is dir /Users/bryan/BGit/Bryan_git/charlie-kirk/site/docs/

Pages are organized as:
  * Level 2: {SITE_DOCS_DIR}/{TopicDir}/overview.md
             OR {SITE_DOCS_DIR}/{TopicDir}/{topic}.md when that file acts as the
             parent navigation page for a group of Level 3 pages.
  * Level 3: {SITE_DOCS_DIR}/{TopicDir}/{specific-page}.md — individual topic pages
             that are linked from a Level 2 TOC.

SCOPE PARSING — decide which pages to process based on TEXT_INPUT_TO_SKILL:

  * "improve all" or "all pages" or "every page"
      → collect every overview.md (Level 2) and every other .md (Level 3)
        under {SITE_DOCS_DIR}, excluding index.md at root.
  * "improve all {TopicDir} pages" or "fix {TopicDir}"
      → collect all .md files inside {SITE_DOCS_DIR}/{TopicDir}/.
  * "improve [one page]" or a specific file name / path
      → process that single page only.
  * "improve overview pages" or "all level 2"
      → collect every overview.md across all topic directories.
  * "improve level 3" or "all detail pages"
      → collect every non-overview .md under each topic directory.

When the scope is large (more than 10 pages), tell the user the count and ask:
  "Found {N} pages to improve. Process all at once, or start with {TopicDir} first?"
Proceed when they confirm.

IMPROVE STEPS FOR EACH PAGE
----------------------------

For every page in scope, run these steps in order:

IMPROVE STEP 1: Read the page
  * Read the full file. Identify whether it is Level 2 (overview.md or acting
    as a parent nav page) or Level 3 (a specific topic page linked from a L2 TOC).

IMPROVE STEP 2: If Level 2 — audit the TOC against actual files on disk
  * List all .md and .mdx files in the same directory.
  * Check: is every existing Level 3 page linked from the TOC?
  * If any are missing from the TOC → add them (fix the TOC in STEP 3).
  * Check: does the TOC link to any files that do not exist? → remove those links.

IMPROVE STEP 3: Run the checklist from the assessment manual for the page's level.
  * List every failing item. If all items pass, output "PASS — no changes needed"
    for this page and skip to the next.

IMPROVE STEP 4: Fix each failing item — do not skip any
  Level 2 fixes (apply all that are needed):
    [ ] Missing or bad orientation paragraph → add one or two sentence intro.
    [ ] Missing three-column TOC → build it from the Level 3 pages that exist
        in this directory. Link to actual existing files only.
    [ ] TOC missing links to existing Level 3 pages → add missing links.
    [ ] TOC columns unbalanced → redistribute bullets left-to-right.
    [ ] Prose before the TOC → move it to after the TOC.
    [ ] Missing three explanatory paragraphs after TOC → write them (what /
        substance / next steps). Do not duplicate TOC bullet text.
    [ ] Missing or wrong Related Areas section → add or fix it (6 links,
        2 columns of 3, pointing outside this section).

  Level 3 fixes (apply all that are needed):
    [ ] Missing back button → add it at the very top using the MDX button pattern.
    [ ] Back button links to wrong page → correct the href.
    [ ] No sub-headings → add ## sub-headings to break up the content.
    [ ] Unsourced factual claims → add inline "(source needed)" flags or known
        source links.
    [ ] Living person, defamation violations → rewrite to use attribution language
        ("reportedly", "according to", "allegedly"). Never state as fact that a
        living person committed a crime unless court-proven.
    [ ] Missing Status field on a person profile page → add Status: Alive /
        Deceased (YYYY) / Unknown.
    [ ] Media items wider than 48% or not floated right → fix inline styles.
    [ ] Missing clearfix after last media item → add the clearfix div.
    [ ] Missing or wrong Related Areas section → add or fix it.
    [ ] Page is a .md that contains embedded media → convert to .mdx and update
        all links pointing to it.

  Both levels:
    [ ] Broken internal links → fix the path to match the actual file location.
    [ ] Unclosed MDX tags or rendering issues → close/fix them.

IMPROVE STEP 5: Write the updated file
  * Use the Edit tool (preferred) or Write tool for larger rewrites.
  * Never remove existing body content. Only add missing structure (TOC, back
    button, paragraphs, Related Areas) or rewrite violating sentences in place.
  * Keep the existing page title (H1) exactly as-is.

IMPROVE STEP 6: Report for this page
  * Output a one-line summary:
      FIXED {file_path} — {comma-separated list of items fixed}
    or
      PASS {file_path} — no issues found

IMPROVE STEP 7: Move to next page, repeat until all pages in scope are done.

FINAL IMPROVE REPORT
--------------------
After processing all pages, output a summary table:

  Pages assessed:  {N}
  Pages fixed:     {N}
  Pages passed:    {N}
  Items fixed:     {list each fix type and how many times it was applied}

If any pages could not be fully fixed (e.g., a .typ extension, a linked page that
does not exist), list them separately under "Needs Manual Attention".

IMPROVE MODE CONSTRAINTS
------------------------
  * Never delete body content that conveys factual information.
  * Adding structure (TOC, back button, paragraphs, Related Areas) is always safe.
  * Rewriting a sentence for defamation safety is required for living persons —
    rewrite the minimum needed; do not paraphrase the whole page.
  * When IMPROVE MODE identifies sub-topics that are missing Level 3 pages, note
    them under "Needs Manual Attention" — do not create them during IMPROVE MODE.
    Use CREATE MODE to build new pages.
  * Do not change the Docusaurus front matter (title, sidebar_label, etc.) unless
    it is clearly wrong or missing.
  * Only write to files under {SITE_DOCS_DIR}. Do not touch private files, the
    master Charlie_Kirk.txt (READ-ONLY TO AI), or anything outside the site/docs/ tree.


============================
CREATE MODE
============================

ASSESSMENT MANUAL — READ THIS FIRST
-------------------------------------
ASSESS_MANUAL is file /Users/bryan/BGit/Bryan_git/charlie-kirk/prompts/Assess_Manual.md

MANDATORY: Read this file FULLY before creating any pages. Every new page you
create must comply with the requirements in the manual for its level.

Absolute path: /Users/bryan/BGit/Bryan_git/charlie-kirk/prompts/Assess_Manual.md

WHAT CREATE MODE DOES
---------------------
Create Mode builds new Level 3 pages under an existing Level 2 topic and
immediately updates the Level 2 page's TOC to link to them. It never leaves
orphan pages — every new page must be reachable from a Level 2 TOC entry.

When creating pages that will contain embedded media (videos, images), create
them as .mdx files from the start. Otherwise create as .md.

CREATE STEPS
------------

CREATE STEP 1: Identify scope
  * From TEXT_INPUT_TO_SKILL, determine:
    - Which Level 2 page is the parent (the .md file whose TOC will be updated).
    - What Level 3 pages need to be created (titles, content, file names).
  * Read the parent Level 2 page fully.
  * List all .md and .mdx files already in the directory to avoid duplicates.

CREATE STEP 2: Create each Level 3 page
  * For each new page, write a fully compliant Level 3 file (see assessment manual):
    - Back button at the very top linking to the parent Level 2 page.
    - Page title (H1) matching the topic.
    - Content organized under ## sub-headings.
    - All factual claims attributed to a source.
    - Defamation-safe language for all living persons.
    - Status field if this is a person profile page.
    - Clearfix div after the last media item (if any).
    - Related Areas section at the bottom: 6 links, 2 columns of 3,
      pointing outside the current section.
  * File naming: use lowercase-with-hyphens, prefixed with the parent topic
    name when pages are siblings in the same directory (e.g., podcasts-tucker-carlson.md).
  * If the page will contain embedded video or images, use .mdx extension.

CREATE STEP 3: Update the parent Level 2 page TOC — MANDATORY
  After creating all Level 3 pages, immediately update the parent Level 2 page:
  * Add a bullet for each new Level 3 page in the three-column TOC.
  * Re-balance columns so heights are equal or off by at most one row.
    Column balance rules:
      - Distribute entries left-to-right (fill column 1 bullet 1, then col 2 bullet 1,
        then col 3 bullet 1, then col 1 bullet 2, etc.)
      - Extra items go to column 1 first, then column 2.
  * If the Level 2 page has no TOC yet, create one from scratch including all
    existing Level 3 pages in that directory plus the new ones.
  * If the Level 2 page is missing other required elements (orientation paragraph,
    three explanatory paragraphs, Related Areas), fix them now.

CREATE STEP 4: Verify no orphans
  * Confirm every .md and .mdx file in the directory (except the Level 2 page itself)
    is linked from the Level 2 TOC. If any are missing, add them.

CREATE STEP 5: Report
  * List every file created and the Level 2 file updated.
  * Note any TOC rebalancing performed.
  * Flag any pages that could not be created due to missing information.

CREATE MODE CONSTRAINTS
-----------------------
  * Never create a Level 3 page without also updating the parent Level 2 TOC.
  * Never link to a file in the TOC that does not exist on disk.
  * Defamation rules apply to all content written — see assessment manual and
    the CLAUDE.md files in the project for full defamation rules.
  * Only write to files under {SITE_DOCS_DIR}.
  * NEVER modify sidebars.ts — the sidebar is managed separately.


============================
EXISTING SECTIONS (reference)
============================

These are the major sections currently in the file (for quick reference during
topic matching). Always re-read the file for the current list since it grows
over time.

* SUPER Strange events
* Strange events
* Accoustics shows direction of bullet
* Timeline
* Court Case
* WhiteHouse
* Israel
* Day of Shooting
* Mossad Quotes World Stage Puppet Master
* Mic Explode pulls shirt
* Gun Mauser Model 98
* Tylers Backpack
* Tylers Timeline that day and clothes
* Tylers Clothing
* Coincidences or NOT (Right after death)
* Quotes OTHER
* Quotes Charlies / Verified
* They were going to kill him TOMORROW
* Quotes from Charlie
* Quotes from NON-CHARLIE
* FBI Cover up
* Ballistics: FBI CBLA Test
* Shawn Sipes / Blake
* SUV Destroyed
* Tyler Robinson did not turn himself in
* MiniVan / SUV: Back Hatch : Tyler M Sipes
* Judges
* 3419 S River Road
* N1098L
* FBI Blocking Investigations
* Phil Lyman
* Other Suspect. Roof top? construction site?
* Charlie Quotes
* Landscaping cement under Tent / UVU
* Monopod Camera / Truck
* Terryl (Fonsworth?) / Michael Olbert
* Tyler Clothing changes
* SAM Flight
* SU-BTT Plane
* N1098
* Stairs Guy and Backpack prove not him
* Tyler trip after assassination


============================
IMPORTANT
============================

* If the symlink ~/.claude/commands/ck_add_text.md does not exist, ask the user:
  "The ck_add_text skill symlink is not installed. Create it? (y/n)"
  If yes, run:
    ln -s ~/BGit/Bryan_git/charlie-kirk/skills_storage/ck_add_text.md ~/.claude/commands/ck_add_text.md

* In ADD TEXT MODE: this skill writes only to {CK_INBOX}. {CK_FILE} and all other
  files are read-only.

* In IMPROVE MODE: this skill writes only to files under {SITE_DOCS_DIR}
  (~/BGit/Bryan_git/charlie-kirk/site/docs/). {CK_FILE} and all private files
  outside site/ are read-only.

* In CREATE MODE: this skill writes new .md/.mdx files under {SITE_DOCS_DIR} and
  updates the parent Level 2 page. {CK_FILE} and all private files are read-only.

* In X POST MODE: this skill writes to:
  - {CK_INBOX} (adding post text and transcriptions — {CK_FILE} is NEVER written)
  - {ROOT_DIR}/Research/x_posts/ (YAML post data)
  - {ROOT_DIR}/Research/evidence/ (transcription copies)
  - {ROOT_DIR}/Research/collected_links.md (fallback link collection)
  - {ROOT_DIR}/videos/ (downloaded videos, gitignored)
  - {ROOT_DIR}/videos_transcription/ (transcription files)
  - {ROOT_DIR}/images/ (downloaded images)
  - {ROOT_DIR}/videos/manifest.yaml (video manifest)
  - {ROOT_DIR}/images/manifest.yaml (image manifest)
  - {ROOT_DIR}/videos/videos.md (human-readable video index)
  - ~/T/_ck_skill/history/{date}_{time}.md (per-run debug log — outside the repo,
    never committed, written on EVERY run)
  - {ROOT_DIR}/IPFS/ipfs.txt (master IPFS pin script)
  - {ROOT_DIR}/tmp/batch_progress.yaml (multi-post checkpoint)
  - {ROOT_DIR}/tmp/transcribe_config.yaml (transcription toggle)
  - {SITE_DOCS_DIR}/ (creating/updating .mdx pages with embedded media)

* NEVER modify sidebars.ts (site/sidebars.ts) in ANY mode unless the user's
  input text explicitly asks to update the sidebar/left bar. The sidebar
  structure is managed separately and this skill must not touch it.


============================
IMPORTANT RULES
============================

* Always follow the investigation's defamation prevention rules.
* For ANY living person: never accuse them of crimes or unethical actions.
  Use attribution language ("according to...", "allegedly", "reportedly").
  Include denials and counterarguments. Note legitimate roles first.
* Always use attribution language for claims from social media posts.
* Never remove existing content — only add to it.
* Keep the investigation's writing tone: investigative, not conspiratorial.
* Include counterarguments and denials where relevant.
* Video embeds: always use CSS style attributes, never HTML width= attribute.
  Always include height: 'auto' and display: 'block'. Local IPFS gateway first.
  Never use cloudflare-ipfs.com — shut down in 2024.


============================
FINAL STAGE: CROSS-SITE HYPERLINKING AUDIT
============================

Run this stage at the END of every mode (ADD TEXT, IMPROVE, CREATE, X POST)
after all other steps are complete. This stage ensures that any page created
or updated during this run has proper hyperlinks to other relevant pages
across the site.

PAGES_CSV is file {ROOT_DIR}/pages.csv

This CSV contains every publicly visible page on the site with columns:
  page_key, parent_key, level, url_path, file_path, title, sidebar_label,
  directory, extension, has_frontmatter, line_count

See the == Pages CSV == section in {ROOT_DIR}/CLAUDE.md for full column
definitions. Key columns:
  * page_key:   unique identifier (4 words max, underscores, no special chars)
  * parent_key: page_key of parent page (empty only for Home)
  * level:      numeric hierarchy level (1=Home, 2=section, 3=child, 4+=deeper)

CROSS-LINK STEP 1: Identify affected pages
  * Collect the list of all site/docs/ files that were created or modified
    during this run (in any mode). These are the pages to audit.
  * If no site/docs/ files were touched (e.g., ADD TEXT MODE only wrote to
    {CK_FILE}), skip this stage entirely.

CROSS-LINK STEP 2: Load the page index
  * Read {PAGES_CSV} into memory. Build a lookup of url_path -> title for
    all pages.
  * Group pages by directory/topic for quick matching.

CROSS-LINK STEP 3: Audit each affected page for missing cross-links
  * For each affected page, read its full content.
  * Scan the page text for mentions of topics, people, events, or concepts
    that match OTHER pages in {PAGES_CSV}. Look for:
      - People names that have their own page (e.g., "Tyler Robinson",
        "Erika Kirk", "Candace Owens", "Ian Carroll", "Rick Cutler")
      - Topic keywords that match a page title or directory name (e.g.,
        "FBI", "drones", "ballistics", "TPUSA", "N1098L", "cover-up",
        "autopsy", "Israel")
      - Timeline references that match timeline pages
      - Location references that match location pages
      - References to laws (Law 1, Law 2, etc.) that match Fix/ pages
  * For each match found:
      - Check if the page already has a hyperlink to that target page
        (look for existing markdown links or HTML links pointing to
        the matching url_path).
      - If NO existing link: flag it as a missing cross-link.
  * Do NOT flag matches inside:
      - The Related Areas section (those are managed separately)
      - Existing hyperlink text (already linked)
      - Frontmatter
      - Image alt text or captions

CROSS-LINK STEP 4: Add missing cross-links
  * For each missing cross-link, add a hyperlink at the FIRST meaningful
    mention of that topic/person in the page body.
  * Use Docusaurus-style relative links:
      - Same directory: [Title](./filename)
      - Different directory: [Title](/url_path)
  * Only link the FIRST mention — do not hyperlink every occurrence.
  * Preserve the existing sentence structure. Wrap the existing text in
    a link rather than inserting new text. Example:
      BEFORE: "The FBI has been blocking independent investigations"
      AFTER:  "The [FBI](/FBI) has been blocking independent investigations"
  * If a person is mentioned and has a People/ page:
      BEFORE: "Candace Owens covered this extensively"
      AFTER:  "[Candace Owens](/People/candace-owens) covered this extensively"
  * Do NOT add links that would be redundant with the Related Areas section.
  * Do NOT add links to trash/ pages.
  * Do NOT add links to Topics3/ pages (those are legacy duplicates).

CROSS-LINK STEP 5: Update pages.csv
  * If any NEW pages were created during this run (IMPROVE MODE rarely does
    this, but CREATE MODE and X POST MODE do):
      - For each new page, add a row to {PAGES_CSV} with all columns filled in.
      - Generate a unique page_key: 4 words or less, underscores, no special
        characters, descriptive enough to distinguish from sibling pages.
        Check existing page_keys in the CSV to avoid duplicates.
      - Set parent_key to the page_key of the parent overview page
        (the overview.md in the same directory, or the nearest ancestor
        directory that has an overview.md).
      - Set level based on depth: overview at depth N = level N+1,
        non-overview at depth N = level N+2.
  * If any existing pages were MODIFIED (title change, file rename, move):
      - Update the corresponding row in {PAGES_CSV}.
      - If a page was moved, update its file_path, url_path, directory,
        parent_key, and level. Also update any other rows that reference
        it as their parent_key.
  * If any pages were DELETED:
      - Remove the row from {PAGES_CSV}.
      - Update any orphaned children to point to the nearest valid parent.

CROSS-LINK STEP 6: Report
  * Output a summary:
      ```
      ============================================
      Cross-Site Hyperlinking Audit
      ============================================
      Pages audited: {N}
      Cross-links added: {N}
        {page} -> {target} ({reason})
        ...
      Pages already well-linked: {N}
      pages.csv updated: {N} rows added, {N} rows modified, {N} rows removed
      ============================================
      ```

CROSS-LINK CONSTRAINTS:
  * Only modify pages that were already touched during this run.
  * Never add links to non-existent pages — verify against {PAGES_CSV}.
  * Never add links inside code blocks, frontmatter, or HTML attributes.
  * Keep link text natural — do not change the meaning of sentences.
  * Skip this stage if {PAGES_CSV} does not exist (output a warning instead).
