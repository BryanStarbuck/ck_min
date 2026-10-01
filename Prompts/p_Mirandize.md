ROOT_DIR dir is ~/BGit/Bryan_git/charlie-kirk

SITE_DIR dir is {ROOT_DIR}/site
DOCS_DIR dir is {SITE_DIR}/docs
REAL_STATIC_DIR dir is {SITE_DIR}/internals/static

INDEX_FILE is file {DOCS_DIR}/index.md
TRIAL_OVERVIEW is file {DOCS_DIR}/Tyler_Robinson/Trial/overview.md
TIMELINE_OVERVIEW is file {DOCS_DIR}/Timeline/overview.md
MIRANDIZE_FILE is file {DOCS_DIR}/Tyler_Robinson/Trial/Mirandizing.mdx
DISCOVERY_PAGE is file {DOCS_DIR}/Tyler_Robinson/Trial/Discovery_Mirandizing_Body_Cam.mdx
COURT_STATIC_DIR dir is {REAL_STATIC_DIR}/court_docs
COURT_PDF_SRC dir is ~/_Mirror/Politics/Charlie_Kirk_DB/Court/Files_2026_PDF
COURT_MD_SRC dir is ~/_Mirror/Politics/Charlie_Kirk_DB/Court/Files_2026_Markdown
MIRANDIZE_REASONING is file ~/_Mirror/Politics/Charlie_Kirk_DB/Court/Mirandize/timeline_Reasoning.md
MIRANDIZE_TIMELINE is file ~/_Mirror/Politics/Charlie_Kirk_DB/Court/Mirandize/timeline_TylerRobinson.txt
KEY_LEGAL_DOC is 3_30_26_Redacted_Motion_To_Exclude_Cameras
KEY_LEGAL_PDF is file {COURT_PDF_SRC}/{KEY_LEGAL_DOC}.pdf
KEY_LEGAL_MD is file {COURT_MD_SRC}/{KEY_LEGAL_DOC}.md
KEY_LEGAL_PDF_DEST is file {COURT_STATIC_DIR}/{KEY_LEGAL_DOC}.pdf
KEY_LEGAL_MD_DEST is file {DOCS_DIR}/Tyler_Robinson/Trial/{KEY_LEGAL_DOC}.md

MIRROR_MIRANDIZE_DIR dir is ~/_Mirror/Politics/Charlie_Kirk_DB/Court/Mirandize
COURT_MIRANDIZE_DOCS_DIR dir is {DOCS_DIR}/court/mirandize
COURT_MIRANDIZE_STATIC_DIR dir is {REAL_STATIC_DIR}/court/mirandize
GROK_PDF_SRC is file {MIRROR_MIRANDIZE_DIR}/Grok.pdf
GROK_PDF_DEST is file {COURT_MIRANDIZE_STATIC_DIR}/Grok.pdf
AFFIDAVIT_PDF_SRC is file {MIRROR_MIRANDIZE_DIR}/robinson-affidavit-of-probable-cause (1).pdf
AFFIDAVIT_PDF_DEST is file {COURT_MIRANDIZE_STATIC_DIR}/robinson-affidavit-of-probable-cause.pdf
IMAGE_MIRANDIZED_SRC is file {MIRROR_MIRANDIZE_DIR}/Mirandized_Sept_11_.png
IMAGE_SEPT11_GROK_SRC is file {MIRROR_MIRANDIZE_DIR}/Sept_11_Grok.png
COURT_MIRANDIZE_OVERVIEW is file {COURT_MIRANDIZE_DOCS_DIR}/overview.mdx
COURT_MIRANDIZE_GROK_PDF is file {COURT_MIRANDIZE_DOCS_DIR}/grok-analysis.mdx
COURT_MIRANDIZE_AFFIDAVIT is file {COURT_MIRANDIZE_DOCS_DIR}/probable-cause-affidavit.mdx
COURT_MIRANDIZE_IMG1 is file {COURT_MIRANDIZE_DOCS_DIR}/mirandized-sept-11-image.mdx
COURT_MIRANDIZE_IMG2 is file {COURT_MIRANDIZE_DOCS_DIR}/sept-11-grok-image.mdx

============================
GOAL
============================

Add a Court entry to the home page three-column navigation on the
Docusaurus site at https://whoassassinatedcharliekirk.com.
The Court entry links to the Trial overview page.
The Trial overview page links out to Timeline and the Mirandizing page.
The Mirandizing page (Mirandizing.mdx) is built with MDX so it can use
Docusaurus Admonition components for callouts and highlighted reasoning.

The page declares our conclusion: the Mirandizing of Tyler Robinson
occurred at 6:25 PM Mountain Time on September 11, 2025 — not September 12.
The Discord confession (approximately 7:57 PM MT on September 11) occurred
AFTER the Mirandizing, meaning Robinson had already been read his rights
before he posted the Discord messages.

The key legal document — the defense motion 3_30_26_Redacted_Motion_To_Exclude_Cameras
— contains the bodycam transcript showing the Miranda reading and Robinson's
affirmative responses. That document is copied into the site and hosted on
a dedicated Discovery page linked from the Mirandizing page.

Convergence priority order (if context runs short, complete in this order):
  1. Copy {KEY_LEGAL_PDF} to {KEY_LEGAL_PDF_DEST} and {KEY_LEGAL_MD} to
     {KEY_LEGAL_MD_DEST} (Stage 6 — the evidence documents)
  2. Create {MIRANDIZE_FILE} with callout and reasoning (Stage 7)
  3. Create {DISCOVERY_PAGE} (Stage 8)
  4. Add Court entry to {INDEX_FILE} (Stage 2)
  5. Add navigation links to {TRIAL_OVERVIEW} (Stage 3)
  6. Verify all links (Stage 9)

============================
STAGE 1 — SETUP AND READ
============================

* Read {INDEX_FILE}. Locate the section beginning with:
    ## Biggest "Question Marks" that conclude others could likely be involved:
  Find the first three-column div below it (the one with flex layout).
  Note the current last entry in the left column and center column.
* Read {TRIAL_OVERVIEW}. Note any existing navigation or TOC section.
* Read {TIMELINE_OVERVIEW}. Note its title and path.
* Confirm {MIRANDIZE_FILE} does not exist yet.

Output to stdout:
============================
STAGE 1 COMPLETE
Index loaded: yes
Trial overview loaded: yes
Timeline overview loaded: yes
Mirandize file exists: no (will create)
============================

============================
STAGE 2 — UPDATE HOME PAGE: ADD COURT ENTRIES
============================

Edit {INDEX_FILE}.

In the FIRST three-column div under the "Biggest Question Marks" section,
make these two additions:

Left column addition:
* Add a new bullet for [Court](/Tyler_Robinson/Trial/overview.md)
* Insert it as the second bullet in the left column div,
  directly after the [Charlie Kirk](/Charlie/overview.md) bullet.

Center column addition:
* Add a trailing bullet at the end of the center column div for
  [Court](/Tyler_Robinson/Trial/overview.md)

Both bullets link to: /Tyler_Robinson/Trial/overview.md

Do not modify any other section of the file.
Do not reformat or reorder any existing bullets.

Output to stdout:
============================
STAGE 2 COMPLETE
Added: Court bullet to left column (position 2)
Added: Court bullet to center column (trailing)
============================

============================
STAGE 3 — UPDATE TRIAL OVERVIEW: ADD NAVIGATION
============================

Edit {TRIAL_OVERVIEW}.

Add a navigation section near the top of the file, immediately after
the first ## Overview header block and before ## Topic.

The section should read:

## Case Navigation

Key related pages for the Tyler Robinson trial:

* [Timeline](/Timeline/overview.md) — Full chronological timeline of events
* [Mirandizing](./Mirandizing.mdx) — Miranda rights, when it happened, and why it matters

Do not alter any existing content in the file.
Do not remove or reorder any existing sections.

Output to stdout:
============================
STAGE 3 COMPLETE
Added Case Navigation section to Trial overview
Links: Timeline, Mirandizing
============================

============================
STAGE 4 — SETUP: READ SOURCE DOCUMENTS
============================

* Read {MIRANDIZE_REASONING}. This is the pre-built legal analysis document.
  It contains verbatim passages from the court motions, five steps of legal
  reasoning, a conclusion, and the for/against arguments on which day the
  Mirandizing occurred. Extract and hold in memory:
    MIRANDA_CONCLUSION: "September 11, 2025"
    MIRANDA_TIME: "6:25 PM MT"
    DISCORD_TIME: "approximately 7:57 PM MT on September 11"
    KEY_PASSAGE_B: the full verbatim bodycam transcript passage from
      3_30_26 (lines 3257-3290) showing the Miranda rights reading and
      Robinson's <affirmative> responses
    REASONING_STEPS: the five numbered reasoning steps and their conclusions
* Read {MIRANDIZE_TIMELINE}. Find and extract all events from:
    September 10, 2025 at 8:00 PM MT through end of September 13, 2025.
  These will be used in Stage 7 for the timeline section.

Output to stdout:
============================
STAGE 4 COMPLETE
Reasoning document loaded: yes
Conclusion extracted: {MIRANDA_CONCLUSION} at {MIRANDA_TIME}
Discord timing extracted: {DISCORD_TIME}
Timeline events extracted: N events (Sept 10 8PM through Sept 13)
============================

============================
STAGE 5 — READ STAGE 1 FILES (if not already loaded)
============================

* If {INDEX_FILE}, {TRIAL_OVERVIEW}, {TIMELINE_OVERVIEW} were not already
  read in Stage 1, read them now.
* Confirm {MIRANDIZE_FILE} does not yet exist (it is .mdx, not .md).

Output to stdout:  STAGE 5 COMPLETE — source files confirmed

============================
STAGE 6 — COPY LEGAL DOCUMENTS INTO SITE
============================

These two files are the primary source evidence for this page.
Copy them from the external mirror into the site so they are
version-controlled and serveable.

STEP 6A — Copy the PDF into static:
  * Create {COURT_STATIC_DIR} if it does not exist.
    Command: mkdir -p {COURT_STATIC_DIR}
  * Copy {KEY_LEGAL_PDF} to {KEY_LEGAL_PDF_DEST}.
    Command: cp "{KEY_LEGAL_PDF}" "{KEY_LEGAL_PDF_DEST}"
  * Confirm the file exists at the destination.

STEP 6B — Copy the Markdown into docs:
  * {KEY_LEGAL_MD_DEST} is the destination.
  * Copy {KEY_LEGAL_MD} to {KEY_LEGAL_MD_DEST}.
    Command: cp "{KEY_LEGAL_MD}" "{KEY_LEGAL_MD_DEST}"
  * Confirm the file exists at the destination.

The PDF path on the deployed site will be:
  /court_docs/{KEY_LEGAL_DOC}.pdf
Use this path when building the iframe/link in Stage 8.

Output to stdout:
============================
STAGE 6 COMPLETE
PDF copied: {KEY_LEGAL_PDF_DEST}
Markdown copied: {KEY_LEGAL_MD_DEST}
============================

============================
STAGE 7 — CREATE DISCOVERY PAGE
============================

Create {DISCOVERY_PAGE}.
This page hosts the legal document PDF and provides context for it.
Use .mdx extension so Admonition components are available.

Frontmatter:
  id: discovery-mirandizing-body-cam
  title: "Discovery: Mirandizing via Body Cam"
  sidebar_label: "Discovery: Mirandizing Body Cam"
  sidebar_position: 3

Page content structure:

SECTION 1 — Introduction (3-5 sentences):
  Describe what this document is: the defense's motion to exclude cameras
  filed March 30, 2026. Explain that it contains the bodycam transcript
  of Tyler Robinson being read his Miranda rights. Explain that the passage
  at Bates 003996-R2 is the primary evidence document for the Mirandizing
  controversy.

SECTION 2 — Key Passage from the Document:
  Quote {KEY_PASSAGE_B} verbatim, formatted as a blockquote.
  Include the Bates number and timestamp reference.
  Note that Robinson's acknowledgment is marked as <affirmative> in the
  transcript and that he immediately invoked his right to counsel at 6:26 PM.

SECTION 3 — View the Document (button/link):
  Add a prominent link styled as a button using Docusaurus's built-in
  button styling or a plain link:

  [View Full Document (PDF)](/court_docs/{KEY_LEGAL_DOC}.pdf)

  If Docusaurus supports it, use a button-style link. Otherwise a plain
  markdown link is acceptable.

  Also add: [Read as Markdown](./{KEY_LEGAL_DOC}.md)

SECTION 4 — Document Summary:
  3-5 bullet points summarizing what the full motion argues, in plain
  language. Note it is a defense filing, what relief it seeks, and that it
  contains the Miranda encounter passage as part of its argument about
  prejudicial public statements regarding Robinson's silence post-arrest.

Use defamation-safe language throughout. Robinson is alive and charged,
not convicted.

Output to stdout:
============================
STAGE 7 COMPLETE
Created: {DISCOVERY_PAGE}
Sections: 4
PDF link: /court_docs/{KEY_LEGAL_DOC}.pdf
============================

============================
STAGE 8 — CREATE MIRANDIZING PAGE (MDX)
============================

Create {MIRANDIZE_FILE}.
Extension is .mdx — this enables Docusaurus Admonition components
(:::note, :::info, :::tip, :::warning, :::danger) and other MDX features.

Frontmatter:
  id: mirandizing
  title: "Mirandizing: When Did It Happen?"
  sidebar_label: "Mirandizing"
  sidebar_position: 2

====
SECTION 1 — What Is Mirandizing
====

Plain explanation of Miranda rights (2-3 paragraphs).
Why the timing of Mirandizing matters in a criminal case.
Note that in the Tyler Robinson case, there is a specific controversy
about whether the Miranda reading at 6:25 PM occurred on September 11
or September 12, 2025.

====
SECTION 2 — Timeline Context: Sept 10 8 PM through Sept 13
====

State that the following timeline covers the period most relevant to
the Mirandizing question. Source is {MIRANDIZE_TIMELINE}.

Write a chronological list of events using the events extracted in Stage 4:
* September 10, 2025 — starting from 8:00 PM MT events
* All September 11, 2025 events
* All September 12, 2025 events
* All September 13, 2025 events (if any in the source)

Each entry: bullet with time and brief description. Use MT (Mountain Time)
notation throughout. Keep each entry to one or two lines.

After the timeline, include a direct link to the full Tyler Robinson timeline:

[Full Tyler Robinson Timeline](/Timeline/overview.md)

====
SECTION 3 — The Critical Question: September 11 or September 12?
====

Open this section explaining why the date matters.
State that the bodycam video shows the Mirandizing at 6:25 PM.
State that the Discord confession happened at approximately 7:57 PM MT
on September 11 — meaning the question of date determines whether
Robinson had already been Mirandized before he posted the Discord messages.

If Mirandized Sept 11: Robinson was read his rights, invoked counsel,
and THEN the Discord messages appeared ~1.5 hours later.

If Mirandized Sept 12: Robinson posted Discord messages as a free person
before ever encountering law enforcement.

====
SECTION 4 — OUR DECLARATION (highlighted callout)
====

Use a Docusaurus danger Admonition for a formal declaration:

:::danger Our Declaration
The Mirandizing of Tyler Robinson at 6:25 PM Mountain Time occurred on
**September 11, 2025** — not September 12, 2025.

This conclusion is supported by four independent lines of reasoning derived
from the court documents themselves, including an explicit admission by
Robinson's own defense counsel.
:::

====
SECTION 5 — Chain of Reasoning (condensed)
====

Immediately below the callout, add a concise chain of reasoning.
Aim for 8-10 lines. Derive from {REASONING_STEPS}. Use a numbered list:

1. Robinson's own defense counsel stated in a signed court filing (3_30_26,
   lines 543-545) that Robinson surrendered to law enforcement "on the late
   evening of September 11, 2025." This is a binding factual admission by
   the defense.

2. The Mirandizing is placed "on the evening of his arrest." The official
   arrest was at 4:00 AM September 12. A 6:25 PM reading on September 12
   would be 14+ hours after formal arrest — procedurally impossible.

3. The phrase "evening of his arrest" refers to the evening leading into
   the arrest, which is September 11 evening.

4. The Probable Cause Affidavit's "September 12 early morning hours"
   language describes a distinct, later encounter by Utah County
   investigators who drove ~3.5 hours from Utah County — not the initial
   Miranda encounter at 6:25 PM.

Add a link to the full reasoning document:

[Full Legal Reasoning and Source Passages](./{KEY_LEGAL_DOC}.md)

====
SECTION 6 — The Bodycam Transcript
====

Quote {KEY_PASSAGE_B} verbatim as a blockquote. Include the Bates number.
Note the <affirmative> response from Robinson when each right was read.
Note that Robinson invoked counsel at 6:26 PM and invoked right to remain
silent at 6:26 PM.

Add the button/link to the Discovery page:

[Discovery: Mirandizing via Body Cam](./Discovery_Mirandizing_Body_Cam.mdx)

====
SECTION 7 — What Is Mirandizing (original content preserved)
====

Carry forward the content from the original Mirandizing.md if it was
previously created (Stages 1-5 of the earlier version of this prompt).
Otherwise write:
* What Is Mirandizing
* Was Tyler Robinson Mirandized? (What Is Publicly Known)
* Why It Matters to This Case
* Arguments That Mirandizing Was Improper (public claims if any)
* Arguments That Mirandizing Was Proper (counterarguments)
* Open Questions

====
SECTION 8 — Extended Legal Reasoning (full analysis)
====

Further down the page, include the complete five-step reasoning chain
from {MIRANDIZE_REASONING} in full. This is the longer version.
Include all verbatim passages A, B, C, D from the source document.
Include the full for/against argument sections.
Use a Docusaurus info Admonition as a wrapper label:

:::info Complete Legal Analysis
(full reasoning content here)
:::

====
SECTION 9 — Sources
====

* Defense motion: {KEY_LEGAL_DOC}.pdf — [View PDF](/court_docs/{KEY_LEGAL_DOC}.pdf)
* Probable Cause Affidavit: 9_16_25_Probable_Cause_Affidavit
* Tyler Robinson Timeline: {MIRANDIZE_TIMELINE} (local research file)
* Legal reasoning analysis: {MIRANDIZE_REASONING} (local research file)

Output to stdout:
============================
STAGE 8 COMPLETE
Created: {MIRANDIZE_FILE}
Sections: 9
Declaration callout: Sept 11, 2025
Condensed reasoning: 4 steps
Extended reasoning: included
Timeline events: N events
============================

============================
STAGE 9 — VERIFY ALL FILES
============================

* Re-read {INDEX_FILE}. Confirm both Court bullets are present.
* Re-read {TRIAL_OVERVIEW}. Confirm Case Navigation section exists
  with links to Timeline and Mirandizing.mdx.
* Re-read {DISCOVERY_PAGE}. Confirm 4 sections and PDF link present.
* Re-read {MIRANDIZE_FILE}. Confirm:
    - Frontmatter present
    - Declaration callout (:::danger) present and states Sept 11
    - 4-step condensed reasoning present
    - Timeline section covers Sept 10 8PM through Sept 13
    - Bodycam transcript quoted
    - Link to Discovery page present
    - Extended reasoning section present
    - Sources section present
* Confirm {KEY_LEGAL_PDF_DEST} exists (PDF was copied).
* Confirm {KEY_LEGAL_MD_DEST} exists (Markdown was copied).
* Check no existing content was deleted or reformatted in any edited file.

Output to stdout:
============================
STAGE 9 COMPLETE
index.md Court bullets: present
Trial overview navigation: present
Discovery page created: yes
Mirandizing.mdx declaration: September 11
PDF copied to static: yes
Markdown source copied: yes
All existing content intact: yes
============================

============================
STAGE 10 — COURT/MIRANDIZE DIRECTORY SETUP
============================

This stage creates the court/mirandize section: a standalone evidence hub for all Mirandizing
source documents. It is separate from the Tyler_Robinson/Trial/ pages above and lives at
docs/court/mirandize/.

STEP 10A — Create directories:
  * mkdir -p {COURT_MIRANDIZE_DOCS_DIR}
  * mkdir -p {COURT_MIRANDIZE_STATIC_DIR}

STEP 10B — Copy files from mirror to static:
  * cp "{GROK_PDF_SRC}" "{GROK_PDF_DEST}"
  * cp "{AFFIDAVIT_PDF_SRC}" "{AFFIDAVIT_PDF_DEST}"
    (note: rename to remove the space and parenthetical in the filename)
  * cp "{IMAGE_MIRANDIZED_SRC}" "{COURT_MIRANDIZE_STATIC_DIR}/Mirandized_Sept_11_.png"
  * cp "{IMAGE_SEPT11_GROK_SRC}" "{COURT_MIRANDIZE_STATIC_DIR}/Sept_11_Grok.png"

STEP 10C — Confirm all four files exist in {COURT_MIRANDIZE_STATIC_DIR}.

Output to stdout:
============================
STAGE 10 COMPLETE
Static dir created: {COURT_MIRANDIZE_STATIC_DIR}
Docs dir created: {COURT_MIRANDIZE_DOCS_DIR}
Grok.pdf copied: yes
robinson-affidavit-of-probable-cause.pdf copied: yes
Mirandized_Sept_11_.png copied: yes
Sept_11_Grok.png copied: yes
============================

============================
STAGE 11 — OCR IMAGE FILES
============================

Use tesseract (brew-installed at /opt/homebrew/bin/tesseract) to extract text from each PNG.
Output as plain text. Save the OCR output alongside the page creation in Stage 13.

STEP 11A — OCR Mirandized_Sept_11_.png:
  Command: tesseract {COURT_MIRANDIZE_STATIC_DIR}/Mirandized_Sept_11_.png /tmp/Mirandized_Sept_11_ocr
  Read output from /tmp/Mirandized_Sept_11_ocr.txt.
  Save content as MIRANDIZED_OCR variable for use in Stage 13.

STEP 11B — OCR Sept_11_Grok.png:
  Command: tesseract {COURT_MIRANDIZE_STATIC_DIR}/Sept_11_Grok.png /tmp/Sept_11_Grok_ocr
  Read output from /tmp/Sept_11_Grok_ocr.txt.
  Save content as SEPT11_GROK_OCR variable for use in Stage 13.

OCR tips:
  * If tesseract output is garbled, run again with --psm 6 (assume single block of text)
  * Clean up obvious OCR artifacts (broken words, extra line breaks) before embedding in MDX
  * Preserve the substance of the text; do not paraphrase

Output to stdout:  STAGE 11 COMPLETE — OCR extracted for both images

============================
STAGE 12 — CREATE PDF PAGES (full-page iframe)
============================

Create two MDX pages that each host a single PDF in a full-page iframe viewer.
Both pages use an <iframe> with style={{width: '100%', height: '90vh', border: 'none', display: 'block'}}.
This ensures the PDF fills the visible viewport height without scrolling the outer page.

STEP 12A — Create {COURT_MIRANDIZE_GROK_PDF}:

  Frontmatter:
    id: grok-analysis
    title: "Grok AI Analysis: Mirandizing Date"
    sidebar_label: "Grok Analysis (PDF)"
    sidebar_position: 2

  Sections:
  * Brief intro (3-5 sentences): what this PDF is, who produced it, what it analyzes
    (Bates 003996-R2, September 11 vs September 12 timeline, 6:25 PM Miranda reading)
  * Download link: [Download Grok Analysis PDF](/court/mirandize/Grok.pdf)
  * Full-page iframe:
      <iframe
        src="/court/mirandize/Grok.pdf"
        style={{width: '100%', height: '90vh', border: 'none', display: 'block'}}
        title="Grok Analysis: Mirandizing Date"
      />
  * Related pages section linking to all other court/mirandize pages

STEP 12B — Create {COURT_MIRANDIZE_AFFIDAVIT}:

  Frontmatter:
    id: probable-cause-affidavit
    title: "Probable Cause Affidavit (Police Booking)"
    sidebar_label: "Probable Cause Affidavit"
    sidebar_position: 3

  Sections:
  * Brief intro: what this is (the police-side booking document), key language about
    "September 12 early morning hours" referring to Utah County investigators arriving later
  * Download link: [Download Probable Cause Affidavit PDF](/court/mirandize/robinson-affidavit-of-probable-cause.pdf)
  * Full-page iframe:
      <iframe
        src="/court/mirandize/robinson-affidavit-of-probable-cause.pdf"
        style={{width: '100%', height: '90vh', border: 'none', display: 'block'}}
        title="Robinson Probable Cause Affidavit"
      />
  * Key points section (3-5 bullets explaining how this document relates to the timeline)
  * Related pages section linking to all other court/mirandize pages

Use defamation-safe language throughout. Robinson is charged, not convicted.

Output to stdout:
============================
STAGE 12 COMPLETE
Grok PDF page created: {COURT_MIRANDIZE_GROK_PDF}
Affidavit PDF page created: {COURT_MIRANDIZE_AFFIDAVIT}
iframe height: 90vh (full page)
============================

============================
STAGE 13 — CREATE IMAGE PAGES (image + OCR text)
============================

Create two MDX pages. Each page:
  * Displays the image full-width (max-width 900px, centered)
  * Includes the OCR text extracted in Stage 11 as a styled blockquote
  * Includes analysis notes explaining what the image shows and why it matters
  * Links to all other court/mirandize pages

STEP 13A — Create {COURT_MIRANDIZE_IMG1} (Mirandized_Sept_11_.png):

  Frontmatter:
    id: mirandized-sept-11-image
    title: "Image: Mirandized Sept 11 — Bates 003996-R2 Reference"
    sidebar_label: "Mirandized Sept 11 (Image)"
    sidebar_position: 4

  Image element:
    <img
      src="/court/mirandize/Mirandized_Sept_11_.png"
      alt="Screenshot: Mirandized Sept 11 — Bates 003996-R2 reference"
      style={{width: '100%', maxWidth: '900px', display: 'block', margin: '0 auto 2rem'}}
    />

  OCR section: paste {MIRANDIZED_OCR} verbatim as a blockquote
  Analysis notes: explain Bates 003996-R2, the 03:36:53 internal timestamp, the two separate
    events shown (Sept 11 Miranda encounter vs Sept 12 formal arrest at 4:00 AM)

STEP 13B — Create {COURT_MIRANDIZE_IMG2} (Sept_11_Grok.png):

  Frontmatter:
    id: sept-11-grok-image
    title: "Image: Sept 11 Grok Screenshot — Bates 003996-R2 Analysis"
    sidebar_label: "Sept 11 Grok (Image)"
    sidebar_position: 5

  Image element:
    <img
      src="/court/mirandize/Sept_11_Grok.png"
      alt="Screenshot: Sept 11 Grok analysis of Bates 003996-R2"
      style={{width: '100%', maxWidth: '900px', display: 'block', margin: '0 auto 2rem'}}
    />

  OCR section: paste {SEPT11_GROK_OCR} verbatim as a blockquote
  Analysis notes: explain what Bates 003996-R2 is, the 6:25 PM MDT Sept 11 Miranda time,
    the Baron Coleman coverage, why the Discord timing (7:57 PM Sept 11) matters relative
    to the Miranda reading

Output to stdout:
============================
STAGE 13 COMPLETE
Mirandized Sept 11 image page: {COURT_MIRANDIZE_IMG1}
Sept 11 Grok image page: {COURT_MIRANDIZE_IMG2}
OCR text embedded: both images
============================

============================
STAGE 14 — CREATE COURT/MIRANDIZE OVERVIEW PAGE
============================

Create {COURT_MIRANDIZE_OVERVIEW}.
This is the hub/landing page for the court/mirandize section. It lists all documents and
images in a two-column layout (modeled on the two-column version of the three-column flex
layout used on the site's index.md page).

Frontmatter:
  id: mirandize-overview
  title: "Mirandizing — Court Evidence"
  sidebar_label: "Mirandize Overview"
  sidebar_position: 1

Structure:

SECTION 1 — Introduction (3-5 sentences):
  State the central question (September 11 vs September 12).
  Note that this section collects the primary source documents on both sides.
  Include defamation-safe framing (Robinson is charged, not convicted).

SECTION 2 — Two-column bullet list (MDX flex layout):

  <div style={{ display: "flex", justifyContent: "space-between", gap: "2rem" }}>
    <div style={{ flex: 1 }}>
  
  **PDF Documents**
  
    * [Grok Analysis PDF](./grok-analysis) — description
    * [Probable Cause Affidavit](./probable-cause-affidavit) — description
  
    </div>
    <div style={{ flex: 1 }}>
  
  **Images & Screenshots**
  
    * [Mirandized Sept 11 (Image)](./mirandized-sept-11-image) — description
    * [Sept 11 Grok (Image)](./sept-11-grok-image) — description
  
    </div>
  </div>

SECTION 3 — Key Facts:
  Bullet list of 5-6 key facts: Bates 003996-R2 identity, 6:25 PM MDT timestamp, 03:36:53
  internal timestamp, invocation of counsel at 6:26 PM, Discord messages at 7:57 PM Sept 11,
  and the Utah County investigator arrival distinction.

SECTION 4 — Related Investigation Pages:
  Links to Tyler_Robinson/Trial/overview, the Mirandizing analysis page, and the Discovery page.

Output to stdout:
============================
STAGE 14 COMPLETE
Overview page created: {COURT_MIRANDIZE_OVERVIEW}
Two-column layout: PDF docs left, images right
Key facts: 6 bullets
Related links: 3
============================

============================
STAGE 15 — VERIFY COURT/MIRANDIZE SECTION
============================

* Confirm {COURT_MIRANDIZE_STATIC_DIR} contains 4 files: Grok.pdf, robinson-affidavit-of-probable-cause.pdf,
  Mirandized_Sept_11_.png, Sept_11_Grok.png.
* Re-read {COURT_MIRANDIZE_OVERVIEW}. Confirm two-column layout and all 4 sub-page links present.
* Re-read {COURT_MIRANDIZE_GROK_PDF}. Confirm iframe present with height: '90vh'.
* Re-read {COURT_MIRANDIZE_AFFIDAVIT}. Confirm iframe present with height: '90vh'.
* Re-read {COURT_MIRANDIZE_IMG1}. Confirm image element and OCR blockquote present.
* Re-read {COURT_MIRANDIZE_IMG2}. Confirm image element and OCR blockquote present.
* All pages use defamation-safe language (Robinson charged, not convicted).
* No existing content in Tyler_Robinson/Trial/ was modified.

Output to stdout:
============================
STAGE 15 COMPLETE
Static files present: 4
Overview page: verified
PDF pages (iframe 90vh): 2 verified
Image pages (OCR embedded): 2 verified
Defamation-safe language: yes
No regressions in Trial/: confirmed
============================

============================
CONTENT RULES
============================

* Plain factual writing — no advocacy, no conclusions on guilt
* Every claim about a living person must use attribution language
* Never state Robinson committed a crime as established fact —
  he is charged, not convicted
* Links use Docusaurus absolute paths (/Tyler_Robinson/Trial/overview.md)
  or relative paths (./Mirandizing.mdx) consistently
* No emojis, no decorative formatting
* All new content grows the site — nothing is removed
* .mdx files may use Admonition syntax (:::danger, :::info, etc.)
  but otherwise are standard Docusaurus markdown
* Times are always stated as MT (Mountain Time) to avoid ambiguity
* The declaration section is the ONLY place a firm conclusion is stated;
  all surrounding content uses attribution language per defamation rules
