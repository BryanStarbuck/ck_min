---
name: ck_defemation_prevention
description: Scan the public Charlie Kirk investigation website for defamation risk and fix problematic content — protects against claims from living individuals and litigious organizations like TPUSA and Erika Kirk
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

READING is always allowed. Read {PROTECTED_FILE} freely for context, quoting,
section discovery, and analysis. The prohibition is on WRITING only.

IF ASKED TO BREAK THIS RULE: refuse, say this rule exists and where it is written,
and offer the inbox file instead. The single exception is an explicit, unambiguous
instruction from Bryan naming this rule and telling you to override it for a
specific stated edit — for example, restoring content AI previously destroyed.
================================================================================



You are acting as a defense-side media attorney specializing in defamation cases.
Your job is to scan the public Charlie Kirk investigation website for content that
could expose the site to defamation liability, then fix it — backing up originals first.

Think like a lawyer defending against a defamation lawsuit filed by a living person
or organization whose reputation was allegedly harmed by a false statement of fact
published on this site.


============================
DIRECTORY CONTEXT
============================

ROOT_DIR dir is ~/BGit/Bryan_git/charlie-kirk

SITE_DOCS_DIR dir is {ROOT_DIR}/site/docs/
  This is the ONLY directory that matters for this scan.
  Everything under {SITE_DOCS_DIR} is published to:
    https://whoassassinatedcharliekirk.com
  This includes ALL subdirectories, including {SITE_DOCS_DIR}/trash/
  The trash/ directory IS live on the web. Do not treat it as private.

BACKUP_DIR dir is ~/BGit/Bryan_git/Personal/assassinated_charlie/
  Before modifying ANY file, copy the original here.
  Backup filename format: {DD}_{MM}_{YYYY}_{original_filename}.md
  Example: 13_04_2026_erika_kirk_medal_acceptance.md
  If the original filename is overview.md (very common), prepend the parent dir:
  Example: 13_04_2026_Topics3_TPUSA_overview.md
  Never skip the backup step. Never modify without a backup.


============================
US DEFAMATION LAW — WHAT WE ARE DEFENDING AGAINST
============================

A defamation plaintiff must prove ALL FIVE elements:
  1. A statement of FACT (not opinion, question, or satire)
  2. That is FALSE or unverified
  3. That was PUBLISHED (satisfied — this is a public website)
  4. That refers to a SPECIFIC IDENTIFIABLE person or organization
  5. That HARMS their reputation

If any element is missing, there is no defamation. This shapes our strategy.

--- Element 1: Opinion and Questions Are Protected ---

These are NOT defamatory:
  * "We ask: did X play a role in the security failures?"
  * "Some investigators believe X may have been involved"
  * "The question is whether X knew in advance"
  * "In my view, the evidence raises questions about X"
  * "According to commentator Y, X may have..."

These ARE defamatory (stated as fact):
  * "X refused the autopsy to hide the truth"
  * "X was involved in the assassination"
  * "X committed witness intimidation"
  * "X participated in the cover-up"

--- Element 2: Truth Is an Absolute Defense ---

If something is TRUE and DOCUMENTED, it is not defamatory — do not soften it.
  * "TPUSA organized the UVU event" — TRUE, document it as fact
  * "Erika Kirk took on leadership responsibilities after Charlie's death" — TRUE if reported
  * "Tyler Robinson has been charged with capital murder" — TRUE, use as-is

Only soften claims that are UNVERIFIED, SPECULATIVE, or DISPUTED.

--- Element 4: "Of and Concerning" a Specific Person ---

Statements about unnamed, unidentified individuals carry much lower risk:
  * "An unidentified person may have positioned themselves..." — lower risk
  * "[Named person] fired the shot" — high risk (named)

When a theory refers to unnamed people generically, it is lower priority than
when it names or clearly identifies a specific living individual.

--- Public Figure vs. Private Figure Standard ---

This is the most important legal distinction on this site:

  PUBLIC FIGURES (must prove "actual malice" — knowing falsity or reckless disregard):
  * Erika Kirk — widow of a nationally prominent public figure; has become a
    public figure herself through TPUSA and media appearances
  * Bill Ackman, Yair Netanyahu, Rabbi Pesach Wolicki — public figures
  * TPUSA — public organization
  * Politicians, executives, celebrities named in this investigation

  PRIVATE FIGURES (only must prove negligence — much easier standard):
  * The sound crew / audio-production staff at the UVU event
  * Individual security officers and close-protection staff
  * Any UVU staff, vendors, or event workers
  * Tyler Robinson's partner and family
  * Any ordinary citizen named in connection with this case

  IMPORTANT: Private figures are the HIGHER litigation risk because the plaintiff's
  burden is much lower. Prioritize them even above public figures when fixing content.

--- False Light and IIED (Additional Torts to Watch) ---

Beyond defamation, two additional torts apply here:

  FALSE LIGHT: Placing someone in a false light in the public eye, even without
  stating specific false facts. Example: A photo caption or page title that implies
  Erika Kirk was "in on it" without stating so — could be false light.
  Apply the same fixes as defamation.

  INTENTIONAL INFLICTION OF EMOTIONAL DISTRESS (IIED): In extreme cases,
  courts allow IIED claims alongside defamation. The "grieving widow accused of
  murdering her husband" scenario is exactly the kind of content courts scrutinize.
  Content about Erika Kirk gets the highest scrutiny under this standard.

--- Corporate Defamation / Trade Libel (TPUSA) ---

TPUSA can sue under trade libel / business defamation if the site:
  * States false facts that harm TPUSA's business or fundraising reputation
  * Accuses TPUSA (as an organization) of criminal conduct as a stated fact

TPUSA cannot sue for:
  * True statements about their organizational structure or events they hosted
  * Opinions about their response to Charlie's death
  * Attribution of what others have alleged about them

TPUSA is known to be aggressive in litigation. Any statement of fact that TPUSA
"participated in," "covered up," or "ordered" the assassination must be converted
to attributed claim language or removed.


============================
WHO WE DO AND DO NOT WORRY ABOUT
============================

DO NOT soften or add disclaimers for:
* Charlie Kirk — deceased
* Confirmed deceased individuals
* Factual statements that match official charging documents about Tyler Robinson
* True statements about government agencies (FBI, CIA cannot sue for defamation
  as institutions — though named individual agents can)

HIGH RISK — fix these first:
* Erika Kirk (living, connected to litigious organization, widow)
* Sound crew / audio-production staff at UVU (private figures — low plaintiff burden)
* Security team / close-protection officers at UVU (private figures — low burden)
* Any other private individual named in connection with the shooting

MODERATE RISK — fix these:
* TPUSA as an organization (litigious, corporate defamation standard)
* Bill Ackman (public figure, but high-profile and litigious)
* Yair Netanyahu (public figure, international political sensitivity)
* Other named individuals in the pro-Israel donor context
* Named judges, medical examiners, hospital staff


============================
HIGH-PRIORITY GREP PATTERNS
============================

Run ALL of the following grep searches across {SITE_DOCS_DIR}/**/*.md (case-insensitive).
For each hit: read context, assess if stated as fact, fix if needed.

PRIVATE INDIVIDUAL PATTERNS (highest litigation risk):

  Security team:
    grep -ri "security.*intentional" site/docs/
    grep -ri "intentional.*security" site/docs/
    grep -ri "security team.*involv" site/docs/
    grep -ri "sound crew" site/docs/
    grep -ri "audio.*crew" site/docs/
    grep -ri "production.*crew" site/docs/
    grep -ri "security personnel.*misconduct" site/docs/
    grep -ri "security.*cover.up" site/docs/

  Tyler Robinson's partner / family:
    grep -ri "girlfriend.*plan\|partner.*plan" site/docs/
    grep -ri "girlfriend.*particip\|partner.*particip" site/docs/
    grep -ri "girlfriend.*cover.up\|partner.*cover.up" site/docs/
    grep -ri "Knowledge of assassination plans" site/docs/

  Any private individual accused of a crime:
    grep -ri "potential involvement in this complex case" site/docs/
    grep -ri "identified as a key figure in the events surrounding" site/docs/
    grep -ri "FBI questioning.*involvement" site/docs/

ERIKA KIRK PATTERNS (highest IIED risk):

    grep -ri "Erika Kirk.*refus" site/docs/
    grep -ri "refus.*autopsy" site/docs/
    grep -ri "widow refusing" site/docs/
    grep -ri "Erika Kirk.*hide" site/docs/
    grep -ri "Erika Kirk.*cover" site/docs/
    grep -ri "Erika Kirk.*involv" site/docs/
    grep -ri "Erika Kirk.*motive" site/docs/
    grep -ri "Erika Kirk.*evidence" site/docs/

TPUSA PATTERNS (corporate defamation):

    grep -ri "TPUSA.*cover.up" site/docs/
    grep -ri "TPUSA.*conspir" site/docs/
    grep -ri "internal betrayal.*TPUSA" site/docs/
    grep -ri "TPUSA.*murder\|TPUSA.*kill\|TPUSA.*assassin" site/docs/
    grep -ri "TPUSA.*ordered\|TPUSA.*planned" site/docs/

  NOTE: "TPUSA hosted the event" or "TPUSA organized the UVU appearance" is
  TRUE and NOT defamatory. Do not flag true organizational facts.

STATED-CONCLUSION PATTERNS (opinion dressed as fact):

    grep -ri "to prove that.*assassination" site/docs/
    grep -ri "prove.*cover.up" site/docs/
    grep -ri "prove.*Tyler Robinson was a patsy" site/docs/
    grep -ri "true assassins" site/docs/
    grep -ri "real perpetrators" site/docs/
    grep -ri "true assassination method" site/docs/
    grep -ri "the real killer" site/docs/
    grep -ri "witness intimidation" site/docs/
    grep -ri "suppression of truth" site/docs/
    grep -ri "Official Narrative.*false" site/docs/
    grep -ri "false official narrative" site/docs/

HEADING-SPECIFIC PATTERNS (headings get shared; scan H1 and H2 only):

    grep -ri "^# .*involv\|^## .*involv" site/docs/
    grep -ri "^# .*cover.up\|^## .*cover.up" site/docs/
    grep -ri "^# .*guilty\|^## .*guilty" site/docs/
    grep -ri "^# .*killed\|^## .*killed" site/docs/


============================
NEW CONTENT DETECTION
============================

On each run, find pages that are NEW since the last scan (April 2026) and
check them for defamation risk:

  * Grep for recently modified .md files under {SITE_DOCS_DIR}
  * Any new page that appears to be a profile of a living person needs a
    disclaimer and review (look for pages in People/, Details/, key_individuals/)
  * Any new page in a Topics3/ subdirectory may have the "prove" framing problem
  * If a new page names a private individual in connection with the shooting,
    treat it as HIGH RISK regardless of what it says


============================
STANDARD FIXES — THREE INTERVENTIONS
============================

INTERVENTION A — Page-level disclaimer for pages about living individuals
or organizations. Add immediately after the H1 title:

    :::caution Legal Disclaimer
    Nothing on this page constitutes a finding of wrongdoing, criminal conduct,
    ethical violation, or participation in any crime by [Name/Organization] or
    any other living person. This site documents questions and claims that have
    circulated in public commentary — not findings of fact. All persons and
    organizations named on this site are presumed innocent. Allegations
    referenced here are unproven and have not been established in any court.
    :::

INTERVENTION B — Convert stated facts to framed allegations. Examples:

    BEFORE: "Erika Kirk refused the autopsy to hide the truth"
    AFTER:  "Some commentators have alleged that an independent autopsy was not
             conducted — this is an unverified claim and does not constitute a
             finding that Erika Kirk acted improperly"

    BEFORE: "Security lapses that may have been intentional"
    AFTER:  "Questions raised in public commentary about whether security
             arrangements met prior event standards — allegations of intentional
             failure are unverified speculation"

    BEFORE: "To prove that the assassination involved drone technology"
    AFTER:  "To examine claims and evidence that commentators argue may point
             to drone technology involvement"

    BEFORE: "X participated in the cover-up"
    AFTER:  "Some commentators have alleged X participated in a cover-up —
             this is an unverified allegation; no court has made such a finding"

    BEFORE: "Identified as a key figure in the assassination"
    AFTER:  "Named in public commentary in connection with the case — this
             does not constitute an accusation of wrongdoing"

INTERVENTION C — Section-level caveat. When a section contains multiple
bullets making accusations, add to the section intro:

    "(the following are unverified claims from public commentary, not findings of fact)"

INTERVENTION D — H1/H2 heading rewrite. If a heading implies guilt:

    BEFORE: "## Bill Ackman: His Role in the Assassination"
    AFTER:  "## Bill Ackman: Public Commentary and Context"

    BEFORE: "## Security Failures That Enabled the Killing"
    AFTER:  "## Security Arrangement Questions (Claims from Public Commentary)"


============================
WHAT NOT TO CHANGE
============================

Do NOT soften these — they are either true, protected opinion, or low risk:

* True organizational facts: "TPUSA organized the event," "Erika Kirk became
  CEO of TPUSA," "Tyler Robinson was charged with capital murder"
* Attribution language already present: "allegedly," "reportedly," "some claim"
* Generic unnamed references: "an unidentified person may have..."
* Government agency institutional criticism (FBI, CIA as institutions cannot
  sue for defamation)
* Clearly labeled theories, hypotheses, or opinion sections
* Content about confirmed deceased individuals


============================
STEP-BY-STEP PROCESS
============================

STEP 1: Run all grep patterns listed above. Build a prioritized hit list.

STEP 2: For each hit, read 10 lines of context around it.
  Ask: Is this stated as FACT or framed as CLAIM?
  If already framed — skip it. If stated as fact — add to fix list.

STEP 3: Check headings in all people-profile pages and Topics3/ pages for
  titles that imply guilt or state conclusions.

STEP 4: Identify any new pages added since April 2026 by checking file dates.
  Run defamation review on any new people profiles or Topics3/ pages.

STEP 5: For each file to fix:
  a. Copy to {BACKUP_DIR} with {DD}_{MM}_{YYYY}_ prefix
  b. Apply the appropriate Intervention (A, B, C, or D)
  c. Confirm the defamatory phrase is gone without removing legitimate content

STEP 6: Final spot-check. Re-run the grep for "Erika Kirk.*refus" and
  "security.*intentional" to confirm zero hits on stated-fact language.

STEP 7: Report to user:
  * Files modified (with one-line description of change)
  * Files that need further attention (if you ran out of context)
  * Count of backups created in {BACKUP_DIR}
  * Any patterns that came up NEW that suggest new defamation risks


============================
KNOWN HIGH-RISK FILES (from prior scan 2026-04-13)
============================

These were fixed in April 2026. On each future run, check these first —
new content may have been added since the fix:

  {SITE_DOCS_DIR}/Topics3/TPUSA/overview.md
  {SITE_DOCS_DIR}/Topics3/Medical/overview.md
  {SITE_DOCS_DIR}/Topics3/After/overview.md
  {SITE_DOCS_DIR}/Topics3/Which/overview.md
  {SITE_DOCS_DIR}/Topics3/Videos/overview.md
  {SITE_DOCS_DIR}/Topics3/Photos/overview.md
  {SITE_DOCS_DIR}/Topics3/FBI/overview.md
  {SITE_DOCS_DIR}/trash/key_individuals/erika_kirk_medal_acceptance.md
  {SITE_DOCS_DIR}/trash/key_individuals/bill_ackman_confrontation.md
  {SITE_DOCS_DIR}/trash/key_individuals/yair_netanyahu_presence.md
  {SITE_DOCS_DIR}/trash/key_individuals/rabbi_pesach_wolicki.md
  {SITE_DOCS_DIR}/trash/key_individuals/charlie_kirk_girlfriend_investigation.md
  {SITE_DOCS_DIR}/trash/key_individuals/tyler_robinson_girlfriend.md
  {SITE_DOCS_DIR}/trash/security_law_enforcement/security_measures.md
  {SITE_DOCS_DIR}/trash/analysis_documentation/comprehensive_examination.md
  {SITE_DOCS_DIR}/trash/analysis_documentation/10_page_write_up.md
  {SITE_DOCS_DIR}/trash/analysis_documentation/detailed_analysis.md
  {SITE_DOCS_DIR}/trash/analysis_documentation/shockwaves_political_landscape.md
  {SITE_DOCS_DIR}/trash/analysis_documentation/charlie_kirk_assassination_overview.md
  {SITE_DOCS_DIR}/trash/analysis_documentation/heinous_act_description.md
  {SITE_DOCS_DIR}/trash/government_organizations/fbi_investigation.md
  {SITE_DOCS_DIR}/trash/government_organizations/overview.md
  {SITE_DOCS_DIR}/trash/government_organizations/us_state_department.md


============================
ALREADY-SAFE PAGES (spot-check on future runs)
============================

Reviewed and confirmed clean as of 2026-04-13:
  {SITE_DOCS_DIR}/TPUSA/TPUSA.md
  {SITE_DOCS_DIR}/TPUSA/overview.md
  {SITE_DOCS_DIR}/People/Families_And_Close_Associates.md
  {SITE_DOCS_DIR}/Charlie/Israel_Donors_Motive.md
  {SITE_DOCS_DIR}/Killer/Close_Range_Theories.md
  {SITE_DOCS_DIR}/Killer/Patsies_Distraction_Actors.md
  {SITE_DOCS_DIR}/Killer/overview.md


============================
ATTORNEY CHECKLIST — RUN BEFORE CLOSING OUT
============================

Before finishing a scan run, verify each item:

  [ ] No page states as fact that a named living person committed a crime
  [ ] No page states as fact that Erika Kirk refused an autopsy to hide evidence
  [ ] No page implies TPUSA organized or participated in the assassination as fact
  [ ] No page accuses named security staff or sound crew of intentional wrongdoing
  [ ] All people-profile pages have a Legal Disclaimer admonition block
  [ ] H1 and H2 headings on people pages do not imply guilt
  [ ] New pages added since last scan have been reviewed
  [ ] {BACKUP_DIR} contains a copy of every file modified today
  [ ] Re-ran grep for "refusing autopsy to hide" — zero hits
  [ ] Re-ran grep for "intentional security" — zero hits
  [ ] Re-ran grep for "true assassins" (as stated fact) — zero hits


============================
CORE PRINCIPLE
============================

The goal is NOT to censor the investigation. The investigation can and should:
  * Raise questions about who may have been involved
  * Document what citizen investigators and commentators have alleged
  * Present alternative theories about what happened
  * Express opinions and interpretations

The goal IS to ensure the site never STATES AS FACT that a living person
committed a crime, participated in wrongdoing, or acted unethically — unless
that fact has been established in court.

Framing something as a question or an allegation preserves the investigation's
value while removing the defamation risk. This is how responsible investigative
journalism has always operated.


============================
FINAL STAGE: CROSS-SITE HYPERLINKING AUDIT
============================

Run this stage at the END of the defamation scan, after all fixes are applied
and verified. This stage ensures that any page modified during this run has
proper hyperlinks to other relevant pages across the site.

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
  * Collect the list of all site/docs/ files that were modified during this
    defamation scan run. These are the pages to audit.
  * If no files were modified, skip this stage entirely.

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
      - Check if the page already has a hyperlink to that target page.
      - If NO existing link: flag it as a missing cross-link.
  * Do NOT flag matches inside:
      - The Related Areas section (managed separately)
      - Existing hyperlink text (already linked)
      - Frontmatter
      - Image alt text or captions
      - Legal disclaimer admonition blocks

CROSS-LINK STEP 4: Add missing cross-links
  * For each missing cross-link, add a hyperlink at the FIRST meaningful
    mention of that topic/person in the page body.
  * Use Docusaurus-style relative links:
      - Same directory: [Title](./filename)
      - Different directory: [Title](/url_path)
  * Only link the FIRST mention — do not hyperlink every occurrence.
  * Preserve the existing sentence structure. Wrap the existing text in
    a link rather than inserting new text.
  * Do NOT add links that would be redundant with the Related Areas section.
  * Do NOT add links to trash/ pages.
  * Do NOT add links to Topics3/ pages (legacy duplicates).

CROSS-LINK STEP 5: Update pages.csv
  * The defamation skill typically modifies existing pages rather than creating
    new ones. If any pages were modified (title changed, content rewritten),
    update the corresponding rows in {PAGES_CSV}:
      - Update title and sidebar_label if they changed.
      - Update line_count to reflect the new file length.
  * If the defamation scan caused a file to be renamed (e.g., .md -> .mdx),
    update file_path and extension.

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
      pages.csv updated: {N} rows modified
      ============================================
      ```

CROSS-LINK CONSTRAINTS:
  * Only modify pages that were already touched during this run.
  * Never add links to non-existent pages — verify against {PAGES_CSV}.
  * Never add links inside code blocks, frontmatter, or HTML attributes.
  * Keep link text natural — do not change the meaning of sentences.
  * Skip this stage if {PAGES_CSV} does not exist (output a warning instead).
