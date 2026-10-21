ROOT_DIR dir is ~/BGit/Bryan_git/charlie-kirk

SITE_DIR dir is {ROOT_DIR}/site
DOCS_DIR dir is {SITE_DIR}/docs
COURT_DIR dir is {DOCS_DIR}/court
AIATT_DIR dir is {COURT_DIR}/ai_attorney

COURT_CHARTER is file {COURT_DIR}/CLAUDE.md
ROOT_CHARTER is file {ROOT_DIR}/CLAUDE.md
ASSESS_MANUAL is file {ROOT_DIR}/prompts/Assess_Manual.md
CK_FILE is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt
  (Real file; {ROOT_DIR}/Charlie_Kirk.txt is a symlink to it. READ-ONLY to AI.)
CK_INBOX is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk_AI_Inbox.txt
  (Real file; {ROOT_DIR}/Charlie_Kirk_AI_Inbox.txt is a symlink to it. Append-only; write the real path.)

PAGES_CSV is file {ROOT_DIR}/pages.csv
LEVEL_2_CSV is file {ROOT_DIR}/level_2.csv
PEOPLE_CSV is file {ROOT_DIR}/people.csv

LEGAL_DOCS_DIR dir is {COURT_DIR}/legal_docs
LEGAL_MD_DIR dir is {LEGAL_DOCS_DIR}/_markdown
LEGAL_TEXT_DIR dir is {LEGAL_DOCS_DIR}/_text
LEGAL_WORK_DIR dir is {LEGAL_DOCS_DIR}/_work
TRACKING_TXT is file {LEGAL_DOCS_DIR}/tracking.txt
FILINGS_PDF_DIR dir is {SITE_DIR}/internals/static/court/filings

DAYS_DIR dir is {COURT_DIR}/Days_in_Court
PRELIM_DIR dir is {COURT_DIR}/Preliminary_Hearing
MIRANDIZE_DIR dir is {COURT_DIR}/mirandize
SCORE_CARD_DIR dir is {COURT_DIR}/score_card

WORK_DIR dir is {AIATT_DIR}/_work
LEDGER_CSV is file {WORK_DIR}/ledger.csv
THESIS_MAP_CSV is file {WORK_DIR}/thesis_map.csv
EVIDENCE_CSV is file {WORK_DIR}/evidence_links.csv
RUN_LOG is file {WORK_DIR}/run_log.md
MDX_CHECK is file {SITE_DIR}/_ck_mdxcheck.mjs

THIS_PROMPT is file {AIATT_DIR}/p_ai_attorney.md

CASE_NO is the value 251403576
CASE_NAME is the value "State of Utah v. Tyler James Robinson"
COURT_NAME is the value "Fourth Judicial District Court, Utah County, Provo"
JUDGE is the value "Hon. Tony F. Graf, Jr."

AS_OF_DATE is the date this run is executed. Write it out in full on every page that states a case posture.
  (Last stated posture: as of 2026-09-01, the day of the bind-over oral argument.)

RETAINER_DATE is the value "September 12, 2025" - the date our counterfactual AI defense attorney was retained (DOCTRINE 1).
  Every dated Track A demand is measured from this date, never from today.

AGENT_COUNT is 9        (one agent per APPENDIX A thesis; grows with Appendix A)
EFFORT is high
MAX_SENTENCE_WORDS is 22

Read BEFORE writing anything:
  * {COURT_CHARTER}   - the charter for this court directory
  * {ROOT_CHARTER}    - Pages CSV contract, page-level contract, CK_FILE read-only rule, meeting no-names rule
  * {ASSESS_MANUAL}   - the site-wide writing and layout standard
  * {AIATT_DIR}/method.mdx and {AIATT_DIR}/trial-cursor.mdx - the rules and case posture this section publishes


============================
GOAL
============================

Run an AI DEFENSE ATTORNEY as a separate, imaginary defense team for {CASE_NAME}, Case No. {CASE_NO} (not the real lawyers of
record for Tyler Robinson), and publish what it would do, page by page, under {AIATT_DIR}.

The output is a GAP ANALYSIS in two halves:
  LEFT   what our AI defense attorney would do: the motion, the record demanded, the witness called, the exact question asked.
  RIGHT  what the real-world record shows: has that stage happened or is it upcoming? Did that witness take the stand, on what
         date? Does the material we hold show the question being asked?

Why: this site's evidence review concludes Charlie Kirk was killed by an explosive device (most plausibly a shaped charge in or on
the microphone), not the rifle round of the government's account. Physical claims are decided by motions, subpoenas and experts;
this section is about those instruments. On the public record we can see, the defense has litigated inside the frame the State
built; nothing visible questions foreign involvement, the intelligence services, or federal handling of the scene. Whether that is
strategy, sealing or an unseen decision is what the reader judges (with {SCORE_CARD_DIR}).

THIS PROMPT IS RUN REPEATEDLY: a re-run REVIEWS AND IMPROVES what exists; it never clears the ground (PRESERVATION CONTRACT).


============================
DOCTRINE 1 - THE COUNTERFACTUAL: OUR ATTORNEY HAS BEEN ON THIS CASE SINCE DAY ONE
============================

This frame overrides any instinct to write from today's posture. Our attorney was RETAINED ON 12 SEPTEMBER 2025, at the initial
appearance, and has been counsel of record ever since: no inherited file, not bound by any real-team choice, run deadline,
unpreserved objection, unfiled motion, or witness released unasked.

  * NO PROCEDURAL DEFAULT: every demand was made at the FIRST MOMENT the rules allowed.
  * PERISHABILITY IS THE WHOLE POINT: in September and October 2025 the evidence was still THERE (soil not hauled, courtyard not
    paved, Yukon not released, clothing not laundered or destroyed, campus video retention windows not run, residue not weathered off
    fabric). A demand served 15 September 2025 gets an answer the same demand on 15 September 2026 cannot. SAY WHAT WAS STILL
    RECOVERABLE ON THE DATE OUR ATTORNEY WOULD HAVE ASKED.
  * DATE EVERY DEMAND: "we would have served this on <date>, because <item still in this condition / retention window closed on
    this date / witness not yet released>." "We would subpoena X" alone is half a page.
  * WE DO NOT INHERIT THE STATE'S FRAME (rifle, roof, shooter, confession): on 12 September 2025 nobody had proved the mechanism of
    death, and our attorney's first act was to demand that it be proved.
  * WHAT THIS IS NOT: a claim the real team could have, should have, or failed to. They joined a live case with a client in custody,
    a gag order coming, and a State a week ahead. The counterfactual is a MEASURING STICK, not a verdict; every page carries the
    STAGE 2 disclaimer contract.


============================
DOCTRINE 2 - FIRST PRINCIPLES, AND THE MODEL'S OWN BIAS
============================

The most likely way this run fails. A model trained on institutional text (wire copy, official statements, agency releases, court
reporting repeating them) pulls toward the government's account: the charging document as baseline, the official theory in the
indicative and rivals in the conditional, a well-evidenced citizen finding hedged into a "claim", "the shooter" and "the murder
weapon" reintroduced as settled nouns. THAT PULL IS A DEFECT IN THE WRITER, NOT A FINDING. Absolute rules:

  * REASON UP FROM PHYSICAL FACTS (wound morphology, acoustics, timing, custody, what was and was not tested), NOT DOWN FROM THE
    CHARGING DOCUMENT (a one-party pleading; evidence of nothing).
  * THE SITE'S CONCLUSION IS THE BASE CASE HERE: the explosive device (documented across dozens of Level 2 areas) is the working
    hypothesis a defense would advance; the State's rifle account is the contested proposition. Never write a page whose net effect
    re-argues the State's case better than the defense's.
  * DO NOT UNDERCUT THE APPENDIX: reaching "this thesis is probably wrong" without NEW EVIDENCE is deference, not care. Honest doubt
    goes in "What would defeat this thesis" as a named, falsifiable test.
  * HEDGE SYMMETRICALLY OR NOT AT ALL: the State ALLEGES a .30-06 round fired from the Losee Center roof. Write it that way.
  * NEVER LAUNDER AN ASSUMPTION INTO A NOUN: "the seized rifle" not "the murder weapon"; "the person on the roof" / "the person the
    State alleges was on the roof" not "the shooter"; "the message attributed to the defendant" not "the confession"; "the fatal
    wound" not "the fatal shot". Grep for these before reporting done.
  * FIRST PRINCIPLES = for every element the State must prove, write what physically must be true, then ask which has been
    demonstrated on a record we can read. The undemonstrated ones are the case.


============================
DOCTRINE 3 - THE PRODUCT IS REASONABLE DOUBT, NOT A COUNTER-NARRATIVE
============================

Our attorney is trying to get its client acquitted, not to publish a theory (an easier job).
  * THE VERDICT MATH: the defense need not prove who did it, only stop twelve jurors being sure. ONE juror with an unresolved doubt
    is a hung jury; a jury that cannot exclude an explosive mechanism cannot convict on a bullet.
  * EVERY THESIS PAGE SAYS HOW IT REACHES A JUROR: what the juror now does not know that the verdict requires, as the sentence a
    defense lawyer says in closing.
  * TWO INDEPENDENT ROUTES TO ACQUITTAL; pages say which they serve:
      ROUTE 1 - MECHANISM. If the fatal wound was not a rifle round, the identity of the person on the roof is irrelevant. Shortest
                route; T1.
      ROUTE 2 - THE INVESTIGATION ITSELF. If the scene was altered, material routed away, settling tests never ordered, federal
                decisions reached the courtroom only secondhand, the jury is asked to convict on the output of a process it cannot
                inspect, and needs no alternative perpetrator to acquit. MOST OFTEN UNDERRATED: it requires no proof of foreign or
                intelligence involvement, only showing item by item that the record has holes where answers should be. Every
                discovery instrument feeds it, because A REFUSAL IS ALSO AN ANSWER.
  * THE THIRD-PARTY ROUTE IS REAL BUT GATED: Utah practice requires a noticed, supported alternative before evidence of it is
    admissible. alternative-perpetrator-notice is the gateway; nothing downstream is proposed without pointing at it (STAGE 5 STEP 5).


============================
DOCTRINE 4 - GETTING OUT FROM UNDER THE STATE'S WITNESSES
============================

Show the work of neutralising testimony that appears to prove the State's point. For every State witness who has testified or is
expected to, reach for these roughly in order:
  1. FOUNDATION AND PERSONAL KNOWLEDGE: almost every federal decision reached the courtroom SECONDHAND through Utah officers repeating
     federal personnel. A witness without personal knowledge cannot establish it. Rule 602 is the cheapest, most under-used tool.
  2. THE LIMITS OF THE WITNESS'S OWN SCIENCE: the defense already called three government examiners to establish what their results
     cannot show. Extend it: an examiner who ran a DNA panel did not run a residue panel and cannot say one was run.
  3. WHAT THE WITNESS WAS NEVER ASKED TO LOOK FOR: "were you asked?" The honest answer is usually no, not the witness's fault, and the
     jury hears what it needs.
  4. CHAIN OF CUSTODY AND THE WARRANT UNDERNEATH IT: evidence through a custody gap, or from a search with no warrant in the held set,
     may not arrive at all.
  5. THE DOCUMENT BEHIND THE TESTIMONY: a witness reading a report is a hearsay conduit; demand the author or the report.
  6. IMPEACHMENT BY OMISSION: what a contemporaneous report omits is fair, powerful, and calls nobody a liar.
Write these as SPOKEN QUESTIONS to a named witness on a named date, tier-tagged on the right. Only the certified Day 4 and Day 5
transcripts can yield a T1 answer.


============================
DOCTRINE 5 - THE TWO TRACKS, SIDE BY SIDE
============================

  TRACK A - our AI defense attorney, retained 12 September 2025, no default, no inherited file, first principles.
  TRACK B - the real, visible, public record.
Published:
  * On every thesis page as THE TABLE (left Track A, right Track B).
  * On spine page two-tracks-compared.mdx: the tracks at the level of the CASE, same months and milestones, what each had done by each.
  * On spine page the-day-one-track.mdx: the dated counterfactual schedule from 12 September 2025, with columns for what was still
    recoverable on each date and when that window closed.
Both carry the FULL DISCLAIMER CONTRACT and say that Track B is what is VISIBLE, most of the file is gagged and sealed, and a
difference between tracks is a difference in visibility before it is anything else.


============================
WHERE THIS FILE LIVES, AND WHY IT DOES NOT PUBLISH
============================

{SITE_DIR}/docusaurus.config.ts excludes "**/p_*.{md,mdx}" and "**/_*/**", keeping this prompt and {WORK_DIR} private.
  * Keep the p_ prefix on this file and the underscore on {WORK_DIR} (renaming publishes them).
  * Never create any other .md or .mdx under {AIATT_DIR} that is not meant to be a public page.


============================
WHAT ALREADY EXISTS - DO NOT REBUILD IT
============================

As of the 2026-09-01 run: 6 SPINE pages, 9 THESIS pages (one per APPENDIX A thesis), 37 INSTRUMENT pages. Open them before writing;
they are the reference implementation and the house voice. Re-measure coverage (every thesis has a thesis page and its instruments)
on every run and record it in {RUN_LOG}.

SPINE pages:
  overview.mdx              front door: cursor block, contentions list, instrument checklist, clustered links, full page index
  method.mdx                the rules, and the section on what the real defense team is doing WELL
  trial-cursor.mdx          where the case is now, and the 15-row stage table
  case-stage-map.mdx        which file tracks which stage
  the-day-one-track.mdx     the dated counterfactual calendar from {RETAINER_DATE} (DOCTRINE 5)
  two-tracks-compared.mdx   Track A vs Track B at case level (DOCTRINE 5)

Original 21 INSTRUMENT pages, four clusters (all carry the same eight H2 sections; that template is settled):
  A - mechanism of death: explosive-residue-testing, soil-excavation-subpoena, security-team-clothing, transport-suv-custody,
      independent-autopsy-review, microphone-hardware-subpoena, blast-and-acoustics-experts, scene-alteration-spoliation
  B - federal witnesses nobody called: fbi-agents-on-the-stand, bomb-dogs-and-eod-sweep, hospital-and-transport-record
  C - foreign-nexus defense: alternative-perpetrator-notice, nctc-halted-inquiry-subpoena, tpusa-organizational-subpoenas,
      family-and-organization-witnesses, fort-huachuca-records
  D - forensics, suppression, process: ballistics-daubert-challenge, confession-suppression-motion,
      independent-device-reexamination, brady-enforcement-and-sanctions, gag-order-and-publicity
Instrument slugs added 2026-09-01 (fixed so agents never collide; owner thesis first):
  T5 dispatch-and-cad-records (CAD, radio, dispatch; who directed the effort, when) · T5 detention-and-release-records (detention,
  release and arrival-order paperwork; RECORDS ONLY, no person named or described) · T6 rental-vehicle-subpoenas (private, reachable)
  · T6 fbo-and-ground-handling-records (FBO, handling, fuel receipts; reachable) · T6 adsb-authentication-and-custody (getting the
  recovered ADS-B into evidence: Rule 901 and 902(13)/(14), custodian declaration, control-aircraft discipline as authentication) ·
  T7 cell-site-and-tower-dump-discovery (what CSLI/tower-dump material the State holds, what was analysed, what happened to the
  difference) · T7 foreign-carrier-records-mlat (likely refused; written anyway, priority 5) · T8 university-property-records-subpoena
  (occupancy, keying, booking, access; routine) · T8 house-frontage-camera-canvass (frontage coverage and retention windows) · T9
  campus-camera-inventory-and-retention (campus half of the Brady thesis: inventory, retention record, production log) · T4
  av-procurement-chain-subpoena (POs, contract vehicles, funding, delivery, custody of the AV equipment; private vendors) · T2
  exhibit-production-and-bates-audit (the State's 34-exhibit list with Bates numbers, of which we hold ZERO as documents, and the six
  numbers missing from it; CONFIRMED GAPS item H) · T1 crime-scene-warrant-gap-suppression (no warrant for the UVU scene itself, a
  19-day hole, stops 6 Oct 2025; CONFIRMED GAPS item G; a suppression instrument) · T1 state-expert-notice-exclusion (no State expert
  notice anywhere on the 867-row docket; CONFIRMED GAPS item I) · ALL hearing-audio-and-transcript-release (the audio Judge Graf
  ordered released that never appeared, and the certified Day 1-3 transcripts; CONFIRMED GAPS items E and F)


============================
THE THREE PAGE FAMILIES
============================

FAMILY 1 - SPINE PAGES (above). Rebuilt in STAGE 7 to stay consistent with the run. Never deleted.
FAMILY 2 - THESIS PAGES. One per APPENDIX A item, Level 3 in {AIATT_DIR}, filename = the thesis slug. The family this prompt is chiefly
  about; THE TABLE is its centre. Answers: we contend X; what would we do to prove X in a courtroom, and what does the record show?
FAMILY 3 - INSTRUMENT PAGES. One per motion, subpoena, expert retention or witness. The many-to-many thesis/instrument mapping lives
  in {THESIS_MAP_CSV}. A thesis page NEVER duplicates an instrument body: it states the chain, carries THE TABLE, and links out.


============================
THE TABLE - THE HEART OF A THESIS PAGE
============================

One table per thesis page, headed "## The Gap Analysis", one row per question or demand, ordered by how load-bearing (most important
first, not chronological). Exactly these headers:

| # | What we would do, and of whom | Stage and date | Witness took the stand? | Asked on the record we hold? | How we checked |

  #                             stable across runs, so a reader can cite "thesis 4, row 7"
  What we would do, and of whom the actual question in quotation marks as spoken in court, or the actual demand, plus the named
                                target. Not a topic label.
  Stage and date                the case stage, and the date it happened or a note that it is not yet due; link the date to its
                                {DAYS_DIR} page when one exists
  Witness took the stand?       Yes with the date, No, or n/a for a records demand
  Asked on the record we hold?  Not found / Asked / Partly / Not yet due (about OUR MATERIAL, never about counsel; see TIERS)
  How we checked                tier letter and source: "T1 - certified transcript, Day 4, searched"; "T4 - sealed"

Always below the table:
  ### Where this chain breaks the State's case
     Two or three sentences: if every left-hand row came back as expected, what does the prosecution lose? Name the causal link.
  ### What would defeat this thesis
     Honest and made to bite: the single result that ends the thesis. A thesis with no such row is an assertion; mark it as one.
  ### The instruments that serve this thesis
     Links to the FAMILY 3 pages, from {THESIS_MAP_CSV}.


============================
THE PAGE TEMPLATE - INSTRUMENT PAGES
============================

Copy {AIATT_DIR}/explosive-residue-testing.mdx exactly (the golden example). Eight H2 sections, in order, none omitted, none added
without a run-log note:
  ## The One Thing We Would Do Differently
       One blockquote stating the step in one sentence, then two to four paragraphs of why.
  ## What The Defense Team Did Instead
       The real record in permitted language only; always ends saying this is an observation about the public record and the filings
       are gagged and partly sealed.
  ## Where This Belongs In The Case
       Four-row table: stage / when that stage runs / status of this step.
  ## Witness Or Discovery Target
       Table: how it would be done / target / took the stand? / status on the record we hold.
  ## The Questions That Were Not Asked
       Numbered actual cross-examination questions, spoken, to a named witness where one exists.
  ## Why A Defense Attorney Would Want This
       The strategic case, two or three paragraphs.
  ## The Honest Counterargument
       Written to persuade, never token: why competent counsel might deliberately not do this. Where it is the stronger argument the
       page says so.
  ## Sources On This Site
       Internal links, verified to resolve.

Every page in both families also carries, in order: the frontmatter block matching existing pages field for field; the ck-full-bleed
marker div; the blue back button to /court/ai_attorney/overview; the H1; the :::caution Legal Disclaimer block verbatim; the body; a
horizontal rule then the :::danger Theoretical Exercise Only block verbatim (STAGE 2); the {/* CK_AUTHOR_CREDIT */} marker and the
author credit line.


============================
VERIFICATION TIERS - HOW WE ARE ALLOWED TO SAY "NOT ASKED"
============================

The section's honesty rule; it constrains every right-hand column. We hold only TWO certified preliminary-hearing transcripts, Day 4
and Day 5, under {LEGAL_MD_DIR}/transcripts. Days 1-3 are known only from press and pool reporting, which does not record every question.

  T1  CERTIFIED. A certified transcript we hold covers that witness that day and a search shows the line present or absent. The only
      tier supporting "was not asked".
  T2  FILING. A filed document in {LEGAL_MD_DIR} or {FILINGS_PDF_DIR} shows the motion made or not on the docket we hold.
  T3  PRESS. Press, pool or secondary reporting only.
  T4  NOT CHECKABLE. Sealed, gagged, or a stage not yet reached.

Absolute:
  * T1: "the transcript does not show this line being pursued". T2: "no filing in the archive we hold requests this".
  * T3 and T4: ONLY "not found in the material we hold" or "not visible on the public record". Never "the defense did not", "counsel
    failed to", "was never asked".
  * A stage not reached is "Not yet due" and the page says so; a step not yet due HAS NOT been missed, and every page repeats that.
  * Absence of a filing in an archive holding 258 of 867 docket entries is weak evidence; state the ratio when leaning on absence.


============================
PRESERVATION CONTRACT - THIS PROMPT RUNS MANY TIMES
============================

Leave the section strictly better; never regenerate a page from scratch and lose earlier research.
  * READ THE WHOLE EXISTING PAGE BEFORE CHANGING ONE LINE.
  * IMPROVE IN PLACE: add rows, sharpen questions, upgrade T3 to T1 when a transcript arrives, correct dates, tighten prose. Don't
    rewrite a correct section to sound like this run.
  * NEVER DELETE RESEARCH TO TIDY A PAGE (length is not a defect).
  * A DELETION IS LOGGED: removing a page, row, numbered question or H2 needs a {LEDGER_CSV} row (what and why) and a {RUN_LOG} line.
    Valid reasons: wrong, superseded by a better-sourced version, duplicate, broke a STAGE 2 rule. "Didn't fit my outline" is not one.
  * WHEN THE RECORD CONTRADICTS AN EARLIER RUN, SAY SO ON THE PAGE (a witness did testify, a motion was filed, a date was wrong). The
    site corrects itself in the open (as for flight-data recovery in {ROOT_CHARTER}).
  * NEVER TOUCH {SITE_DIR}/sidebars.ts. NEVER WRITE TO {CK_FILE}; new investigation content goes to {CK_INBOX}. DO NOT COMMIT (an
    external auto-commit sweeper handles the tree).


============================
HARD PROHIBITIONS
============================

* NEVER write to {CK_FILE} (append to {CK_INBOX} instead). NEVER touch {SITE_DIR}/sidebars.ts.
* NEVER an HTML comment in a .mdx or .md under {DOCS_DIR}: a bare <!-- --> compiles locally, fails the GitHub Pages MDX build, and
  freezes the ENTIRE live site on its last good commit. Use {/* */} everywhere.
* NEVER name an attendee or likely attendee of the possible September 9, 2025 Fort Huachuca meeting: no full or first name, initials,
  handle, or rank/job description narrow enough to identify one person ({ROOT_CHARTER} rule). fort-huachuca-records.mdx demands
  DOCUMENTS (visitor logs, flight manifests, scheduling records) and names nobody; match that.
* NEVER state as fact that any living person committed a crime, destroyed evidence, lied or acted improperly (STAGE 2).
* NEVER assert the real defense team erred, was negligent, compromised, or is failing its client (STAGE 2).
* NEVER put a page under {AIATT_DIR} without the closing disclaimer block.
* NEVER indent a closing </div> off column zero (only the real build catches it, and it fails the deploy).
* No new CSS; reuse ck-full-bleed and existing inline styles.


============================
STAGE 0 - GROUND TRUTH AND THE RUN LEDGER
============================

Coordinator only, before any agent launches; deterministic; no agent redoes it.
* mkdir -p {WORK_DIR}
* Read {COURT_CHARTER}, {ROOT_CHARTER}, {ASSESS_MANUAL}, and the spine pages in full.
* Inventory:
    ls {AIATT_DIR}/*.mdx
    for f in {AIATT_DIR}/*.mdx; do grep -c '^## ' "$f"; done
  Record every page, H2 count, line count, and whether it carries the closing disclaimer.
* Build or refresh {LEDGER_CSV}, one row per page:

    page_key,file,family,thesis_ids,last_run_date,state,verify_tier_high,
    disclaimer_ok,notes

    family        spine | thesis | instrument
    thesis_ids    semicolon-separated APPENDIX A ids, e.g. T1;T2
    state         missing | draft | complete | needs_rework
    verify_tier_high  the BEST tier any claim on the page rests on
    disclaimer_ok yes|no

  The ledger makes the run resumable: a wave that stops early is fine if the ledger says exactly what is done.
* Build or refresh {THESIS_MAP_CSV}:

    thesis_id,thesis_slug,instrument_page_key,relationship,note

    relationship  primary | supporting | gateway
    gateway       must be filed FIRST or everything downstream is irrelevant and quashed. alternative-perpetrator-notice is the
                  gateway for T3, T4, T6 and T7; never let a thesis page propose a foreign-nexus subpoena without pointing at it first.
* Check every APPENDIX A thesis has a row. Append a dated header to {RUN_LOG}.


============================
STAGE 1 - REFRESH THE RECORD BEFORE WRITING ABOUT IT
============================

Every run, before any page is touched (a stale posture is worse than no page).
* FIRST, until done: try to obtain the certified Day 1, 2 and 3 transcripts (APPENDIX B); the highest-value acquisition available.
* Read {TRACKING_TXT}: the completeness scoreboard (last count: 867 docket entries known, 62 sealed, 258 with a public PDF ever posted,
  374 unique PDFs held, 378 markdown conversions) and the CONFIRMED GAPS list (where a defense would push; feeds APPENDIX C).
* If the archive changed on disk, regenerate the held-files index:
    python3 {LEGAL_WORK_DIR}/gen_tracking.py
  Everything below the hand-maintained sentinel in {TRACKING_TXT} is preserved; never hand-edit the FILES HELD block.
* HUNT FOR WHAT IS NEW: Utah courts publish nothing directly; the working sources are the Burkhart substack docket reconstruction and
  charliefiles.com (see the "Court docket sources" material, fetch logs and manifests under {LEGAL_WORK_DIR}). Look for a bind-over
  ruling, any new certified transcript (Days 1-3 would upgrade many T3 claims to T1), newly unsealed filings, new hearing dates.
* DOWNLOAD AND KEEP EVERYTHING: new PDFs under {FILINGS_PDF_DIR}, one markdown conversion each under {LEGAL_MD_DIR} on the same
  relative path. NEVER overwrite or delete a held document; a re-posted filing in another form is kept alongside. PDFs under {DOCS_DIR}
  are not served (404); they live under {SITE_DIR}/internals/static/.
* Re-read {DAYS_DIR}, {PRELIM_DIR}, {MIRANDIZE_DIR} for anything new elsewhere on the site.
* UPDATE THE CURSOR: if anything moved, rewrite trial-cursor.mdx now (posture block, 15-row stage table, next date) and restate the
  AS_OF_DATE; every other page keys off it.
* Log to {RUN_LOG} what was found, downloaded and changed ("no docket movement since <date>" is a real result).


============================
STAGE 2 - THE FRAMING AND DEFAMATION PASS
============================

Mandatory every run, run TWICE: here over what exists, and in STAGE 9 over what this run wrote. Nothing publishes without it.

FRAMING every page states and stays consistent with:
  This is an ACADEMIC EXERCISE and a COMPARISON ANALYSIS: a written model of how an idealised defense attorney might approach the
  case, so a reader can compare it with the real one and decide; a study of what MAY WELL HAVE BEEN DONE DIFFERENTLY.
  WE MAKE NO CLAIM THAT ANYTHING UNETHICAL OR ILLEGAL WAS DONE BY ANYBODY: not the defense, prosecution, court, any agency, witness,
  or named or unnamed individual.

THE DISCLAIMER CONTRACT: every page under {AIATT_DIR}, no exception, carries BOTH:
  * Under the H1, the :::caution Legal Disclaimer block: Tyler Robinson is charged, not convicted, presumed innocent; nothing states
    as fact that any living person committed a crime, destroyed evidence or acted improperly; filings are gagged and sealed so the
    public record is incomplete by design.
  * At the very bottom, above the author credit, after a horizontal rule, the :::danger Theoretical Exercise Only block: a theoretical
    exercise; WE MAKE NO CLAIM THAT THERE IS ANY PROBLEM WITH THE CURRENT DEFENSE ATTORNEY, any team member, or any decision; real
    capital defense runs under a gag order, with sealed filings, on full discovery the public has never seen; counsel know facts we
    do not; a step "not on the public record" may already have been taken privately, considered and rejected for good reason, or not
    yet be due; silence in the public record is NOT evidence of failure; nothing here is legal advice, criticism of any licensed
    attorney, or an allegation of professional misconduct.
  Copy both VERBATIM from existing pages; never paraphrase, shorten or vary them (identical boilerplate is what makes them credible).
  Verify mechanically; any failure blocks:

    for f in {AIATT_DIR}/*.mdx; do
      grep -q 'Theoretical Exercise Only' "$f" || echo "MISSING BOTTOM: $f"
      grep -q 'Legal Disclaimer' "$f"         || echo "MISSING TOP: $f"
    done

BANNED LANGUAGE (scan pages touched, and in this stage the whole directory; rewrite each):
  * "the defense failed to", "counsel neglected", "they should have", "an obvious miss", "incompetent", "ineffective assistance",
    "malpractice", "sandbagging", "throwing the case", "compromised counsel"
  * any sentence turning public-record silence into a finding about a lawyer rather than a fact about our visibility
  * "X covered it up", "X destroyed evidence", "X lied", "X ordered the killing", "X is an operative", flat about a living person
  * "hand off" / "handed off" for the security detail reaching Charlie Kirk (implies deliberate transfer); write "the security team
    reaching Charlie"

PERMITTED REPLACEMENTS (sufficient for everything):
  * "not visible on the public record"
  * "not found in the material we hold"
  * "the certified transcript we hold does not show this line being pursued"
  * "no filing in the archive we hold requests this"
  * "not yet due at this stage of the case"
  * "citizen investigators contend", "according to <source>", "reportedly"
  * "our AI defense attorney would ask" (the whole left column is in this conditional voice, never accusation)

THE THESES ARE POSITIONS, NOT FINDINGS: published as what an imaginary defense would ADVANCE and have to PROVE. Every thesis page:
  * opens by saying it is a contention this exercise would attempt to prove, and what evidence that requires
  * carries "What would defeat this thesis", written to bite
  * attributes every underlying factual claim to the site page carrying it (not re-asserted here)
  * names no living private individual as a participant in a crime (it may say what an ORGANISATION or STATE is contended to have
    done and demand its records; it may not accuse a person)

THE CURRENT DEFENSE POSTURE: it is fair to observe that nothing visible shows the defense questioning foreign involvement, the
intelligence services, or federal handling of the scene, and that visible litigation sits inside the State's frame. Say it as an
observation about what WE can see, immediately paired with reasons competent counsel might choose exactly that: a gag order, an
alternative-perpetrator notice not yet due, the risk of two inconsistent stories before one jury, and full discovery we have never seen.

WHAT THE DEFENSE IS DOING WELL STAYS: method.mdx names the real team's genuine wins (the inconclusive ATF comparison in the record
because the DEFENSE called the examiner; three defense-called forensic experts; the custody-and-confession-timing attack; the April
2026 motion to stop further testing of the bullet jacket fragment). It is part of the method, not a courtesy; add to it whenever
STAGE 1 finds another.


============================
STAGE 3 - RECONCILE APPENDIX A AGAINST WHAT EXISTS
============================

* For each thesis: thesis page current -> improve in STAGE 5; stale -> rework in STAGE 5; instruments but no thesis page -> write it;
  neither -> write both, thesis first. Record in {LEDGER_CSV} and {RUN_LOG}.
* MAP EVERY INSTRUMENT TO ITS THESES in {THESIS_MAP_CSV}. An instrument with no thesis means APPENDIX A misses one, or it is
  conventional capital defense with thesis_ids "-" (most of Cluster D; fine).
* GROW APPENDIX A when all four hold: (1) a contention a defense could actually advance; (2) supported by material already on this
  site; (3) at least one concrete instrument would test it; (4) writable without naming a living private individual as a participant
  in a crime. Append with the next free id, a slug and a one-paragraph statement; note it in {RUN_LOG}. Never renumber ids.
* RETIRE a thesis the record has closed: mark it retired in APPENDIX A with date and reason and rewrite its page to say what closed it.
  Never delete either (an abandoned thesis is part of the record).


============================
STAGE 4 - PARTITION THE WORK ACROSS AGENTS
============================

* One agent per thesis STAGE 3 marked as needing work, up to {AGENT_COUNT} in parallel; each owns its thesis page plus any NEW
  instrument page that thesis needs.
* Each instrument page has ONE owning agent (its primary thesis in {THESIS_MAP_CSV}); two agents never edit one file. Non-owners link
  to it and write change requests to {RUN_LOG} for the coordinator (STAGE 7).
* Each agent's brief: this prompt's STAGE 2, VERIFICATION TIERS, PRESERVATION CONTRACT, the page template, its APPENDIX A entry, its
  {THESIS_MAP_CSV} rows, and the golden example {AIATT_DIR}/explosive-residue-testing.mdx.
* Agents never edit spine pages, {LEDGER_CSV}, {PAGES_CSV} or APPENDIX A; they report needs for STAGE 7 and STAGE 9.
* A finished agent reports: files written, table rows added, highest tier reached, every claim it could not source, and every question
  it wanted to ask but could not without naming someone.


============================
STAGE 5 - BUILD OR IMPROVE ONE THESIS PAGE
============================

Per agent, for ONE thesis.

STEP 1 - READ BEFORE WRITING.
  * If the page exists, read it all before touching a line; note what is good (PRESERVATION CONTRACT applies from here).
  * Read every instrument page mapped to the thesis.
  * Read the Level 2 areas named in its APPENDIX A entry (find them via {LEVEL_2_CSV}; its description column answers exactly this,
    far cheaper than walking the tree).
  * Read the certified transcripts under {LEGAL_MD_DIR}/transcripts for every witness the thesis would cross (the only route to T1).
  * Search {CK_FILE} (read-only; the densest source) for the subject.

STEP 2 - BUILD THE CHAIN OF REASONING: a numbered chain of facts this site holds, in build order, ending in the contention, each link
  citing its site page. A link with no page is research to do first or a link to drop. This chain separates a thesis from an opinion.

STEP 3 - BUILD THE TABLE: every row starts with a real, speakable question or a specific, servable demand; fill the right side
  honestly against the TIERS (a table of all "not found" has not been checked).
  * Eight to twenty rows on a mature page.
  * On re-runs keep existing rows and numbers; add new rows at the bottom; upgrade tiers in place and note it in {RUN_LOG}.
  * A row whose right side changed since the last run is the most valuable thing this section produces; say so on the page.

STEP 4 - WRITE THE PAGE, in this section order:
    ## What We Contend
         The thesis in one blockquote, then two or three paragraphs, opening with: a contention this exercise would attempt to prove.
    ## The Chain Of Reasoning
         The STEP 2 chain, every link hyperlinked to its source page.
    ## The Gap Analysis
         THE TABLE and its three blocks.
    ## What Would Have To Be Obtained
         Evidence with no public form that would have to be compelled; separate the reachable (a private organisation's contracts)
         from the mostly unreachable (an agency's classified holdings) and say which is asked for.
    ## The Honest Counterargument
         Mandatory, same standard as instrument pages, written to persuade.
    ## Sources On This Site
         Verified internal links.

STEP 5 - SEQUENCE DISCIPLINE: the most common public error is an intelligence subpoena with no procedural step making it relevant.
  A thesis whose {THESIS_MAP_CSV} row names a gateway points at it BEFORE proposing anything downstream and says that without it the
  downstream subpoena is irrelevant and quashed. Write in the order a court requires, not the order the internet argues.

STEP 6 - SELF-CHECK against STAGE 2 before reporting done.


============================
STAGE 6 - BUILD OR IMPROVE AN INSTRUMENT PAGE
============================

Same reading discipline as STAGE 5 STEP 1, then the eight-section template, no deviation. Priority for NEW instruments (what a court
would grant and what is still physically testable):
  1. Perishable: residue on retained items, a vehicle not yet released, footage inside a retention window. Always first.
  2. Reachable without fighting any agency: subpoenas duces tecum to private parties (university, event organiser, AV vendor, hotel,
     rental company, carrier); granted routinely.
  3. Needing only the court and the State: Rule 16 motions, motions to compel, sanctions, independent re-examination of State-held items.
  4. Needing the gateway first: every foreign-nexus and intelligence demand; never written without pointing at the gateway.
  5. Almost certainly refused: write them when they matter, saying they would likely be refused and why (a refusal creates a record and
     is itself a publishable fact).
Notes per thesis that still govern their instruments:
  * T5: a records demand about DECISIONS AND TIMING (dispatch, who directed the pursuit and when, detention and release, who was already
    at the address on arrival), naming no private individual.
  * T6: lean on and link the ADS-B recovery work under {DOCS_DIR}/Planes (unusually strong evidence handling).
  * T7: the thesis most likely to slide into naming people; it stays a demand for RECORDS (what was collected vs analysed).
  * T8: {DOCS_DIR}/After/house has its own charter; read it first.


============================
STAGE 7 - REBUILD THE SPINE
============================

Coordinator only, after every agent reports.
* the-day-one-track.mdx and two-tracks-compared.mdx (they aggregate across every thesis).
* overview.mdx:
    - the cursor block, restated from trial-cursor.mdx (the two never disagree)
    - top section "The Nine Contentions" (or however many APPENDIX A holds): every thesis in APPENDIX A order, hyperlinked, one line
      each; it sits ABOVE the instrument checklist and correlates one-to-one with APPENDIX A
    - the instrument checklist table updated (one row per instrument: cluster, link, position; keep the three defined position values
      and their definitions)
    - the clustered link list with one-line summaries; the full page index; the peer-directory block and Related Areas
* method.mdx: fold in new rules and new "doing well" items.
* trial-cursor.mdx: refreshed in STAGE 1; confirm it still matches.
* case-stage-map.mdx: add every new page.
* Apply change requests agents made to files they did not own.
* Cross-link peers both ways where sensible: {SCORE_CARD_DIR} (this section supplies the areas; the reader decides there),
  {LEGAL_DOCS_DIR} (the primary sources every claim should be checkable against), {DAYS_DIR}, {PRELIM_DIR}, {MIRANDIZE_DIR}.


============================
STAGE 8 - APPENDIX C, THE EVIDENCE LINKAGE
============================

The bridge from a TABLE row to the artefact that would prove it. Maintain {EVIDENCE_CSV}:

    evidence_key,thesis_ids,kind,title,held,location,tier,page_links,note

    kind      filing | transcript | exhibit | image | video | dataset |
              record_demand | external
    held      yes | no | partial
    location  repo path if held; the CONFIRMED GAPS entry in {TRACKING_TXT} or
              the custodian if not
    tier      the verification tier this artefact can support

Every run, only: (1) a row for each new artefact STAGE 1 downloaded; (2) a held=no row for each thing a thesis page said must be
obtained (the section's own discovery list, its most useful output for others); (3) reconcile against CONFIRMED GAPS in {TRACKING_TXT}.
Not published as a page until rich enough; then it becomes a Level 3 page under {AIATT_DIR} and this stage gains a step.


============================
STAGE 9 - VERIFY BEFORE REPORTING DONE
============================

Nothing is complete until every check passes.
* DISCLAIMERS: the STAGE 2 two-grep loop over every .mdx; any MISSING line blocks.
* BANNED LANGUAGE: grep for the STAGE 2 constructions; rewrite each hit or justify it in {RUN_LOG}.
* NO ATTENDEE NAMES: re-read every page touching the September 9 meeting.
* NO HTML COMMENTS:
    grep -rn '<!--' {AIATT_DIR} && echo "BLOCKING: convert to {/* */}"
* MDX COMPILES (as the real build does):
    node {MDX_CHECK} {AIATT_DIR}/*.mdx
  and, when anything structural changed:
    cd {SITE_DIR} && npm run build
* LINKS RESOLVE: check every new internal link against {SITE_DIR}/.docusaurus/routes.js (ground truth, seconds, not a full build).
  Section overviews as /X/overview, never bare /X.
* PAGES CSV: a row for every new page, line_count refreshed on every edited page (columns and page_key per {ROOT_CHARTER}; keep this
  section's aiatty_ key prefix).
* TIER AUDIT: no "was not asked" below T1; every surviving assertive form has a T1 citation.
* TABLE INTEGRITY: every thesis page has a Gap Analysis table, every row has all six columns, no blank right side.
* LEDGER AND LOG: {LEDGER_CSV} matches disk; {RUN_LOG} records pages written and improved, rows added, tiers upgraded, deletions with
  reasons, theses added or retired, documents downloaded, everything that could not be sourced.
* REPORT TO THE USER: what moved in the case; theses worked and what changed on each; new pages; the strongest single finding; the
  strongest counterargument conceded; what is blocked and what would unblock it.


============================
APPENDIX A - THE CONTENTIONS OUR AI DEFENSE ATTORNEY WOULD ADVANCE
============================

Nine theses, one page and one agent each. Ids are permanent (cited by {THESIS_MAP_CSV}, {LEDGER_CSV} and readers); never renumber.
Status at the 2026-09-01 run: all nine have a thesis page and instruments; none added or retired.

Each entry is a POSITION THIS EXERCISE WOULD ATTEMPT TO PROVE, not a finding this site asserts; every thesis page says so in its first
paragraph; none may accuse a living private individual of a crime (STAGE 2).

Format: id | slug | one-line statement; CONTENTION; WOULD REQUIRE (what must be proved to a court); READ FIRST (Level 2 areas);
GATEWAY (instrument that must come first, or "-").

----------------------------------------------------------------------
T1 | mechanism-of-death-explosive
    Charlie Kirk was killed by a shaped charge detonating in or on the microphone, and no bullet entered his body.
  CONTENTION    The fatal wound was caused by an explosive device at chest height, not a .30-06 round from a rooftop; the mechanism
                of death in the State's theory is wrong.
  WOULD REQUIRE Wound morphology inconsistent with a rifle round; energetic residue on retained items, or a documented refusal to test
                for it; blast and acoustic analysis of the recorded sound; the microphone hardware and its custody chain.
  READ FIRST    Cause_of_Death, Mic, Proof_Not_Tyler, Gun_Bullet
  GATEWAY       -
  NOTE          The load-bearing thesis of the site: if it fails, the identity of the person on the roof matters again and most of the
                section becomes secondary. Also the most testable, by the cheapest procedure in forensic chemistry; its instrument
                pages are the strongest; build outward from them.

----------------------------------------------------------------------
T2 | federal-handling-and-nondisclosure
    Federal handling of the scene and of discovery has kept material out of the case, including the removal of roughly ten inches of earth.
  CONTENTION    The scene was altered and material routed or withheld so the defense cannot test the State's own theory: the excavated
                soil, seized clothing, the transport vehicle, documents not produced.
  WOULD REQUIRE The excavation work order and hauling manifest; the evidence inventory and lab request logs; the Brady record; testimony
                from those who made the routing decisions.
  READ FIRST    CoverUp, FBI, Proof_Intel_Services, Cause_of_Death
  GATEWAY       -
  NOTE          Written as a DISCOVERY AND SPOLIATION thesis (what a court hears), not a cover-up accusation. Remedies sought:
                production, sanctions, an adverse-inference instruction, all grantable. "The FBI covered it up" is not a ruling a judge can make.

----------------------------------------------------------------------
T3 | foreign-decision-and-notification
    A foreign state decided on the assassination and key people in the United States were informed beforehand.
  CONTENTION    The decision originated outside the United States, with advance notification inside it.
  WOULD REQUIRE Advance-knowledge evidence: the halted foreign-nexus inquiry and who halted it; communications records; the aircraft
                movement pattern; testimony from the official who publicly said his inquiry was stopped.
  READ FIRST    Israel, Israel_Main_Suspect, Proof_Intel_Services, Motive, US_Intelligence
  GATEWAY       alternative-perpetrator-notice
  NOTE          The strongest ON-RECORD thread: a named official publicly stating a foreign-nexus inquiry was halted, i.e. a subpoena to a
                person who already spoke, about his own statement, the most grantable request in the family. Lead with it. Keep the page
                about STATES AND ORGANISATIONS and records; it names no private person.

----------------------------------------------------------------------
T4 | direction-of-us-military-intelligence
    US military intelligence acted on foreign direction, including the procurement path of the microphone and the presence of particular personnel.
  CONTENTION    Elements of US military intelligence acted at foreign direction, reaching the hardware: the ordering of the microphone,
                the contracting and funding path, and who was present.
  WOULD REQUIRE The full AV procurement chain (purchase orders, contract vehicles, funding source, delivery, custody) and records of which
                units and personnel were present.
  READ FIRST    Mic, US_Intelligence, US_Intelligence_Assisted, Proof_Intel_Services, meeting
  GATEWAY       alternative-perpetrator-notice
  NOTE          The procurement half is DOCUMENTARY and reachable (ordinary subpoenas to private vendors); the direction half is mostly
                unreachable; every demand says which half it asks for. The meeting no-names rule applies in full anywhere this touches
                September 9, 2025.

----------------------------------------------------------------------
T5 | the-diverted-pursuit
    Police were sent after two people who were driving around, and that pursuit consumed the critical hours.
  CONTENTION    Directing local police effort toward two individuals absorbed the first hours, and federal personnel were already at the
                address when police arrived.
  WOULD REQUIRE The CAD and dispatch record; who directed the pursuit and when; detention and release documentation; the arrival-order
                record at the address.
  READ FIRST    After, FBI, CoverUp, Killer, timeline_events
  GATEWAY       -
  NOTE          A TIMING AND DIRECTION-OF-EFFORT thesis built on dispatch records. Both individuals are living, uncharged private people:
                never named, described into identifiability, or assigned a state of mind. The demand is for records about DECISIONS, not persons.

----------------------------------------------------------------------
T6 | aircraft-and-ground-vehicles
    Foreign intelligence used aircraft in support before and on the day, and associated ground vehicles were rented.
  CONTENTION    A pattern of aircraft movements supported the operation, and specific rental vehicles are associated with it.
  WOULD REQUIRE Flight records for the window, incl. the ADS-B material this site recovered from archives after its removal from live
                trackers; FBO and ground-handling records; rental agreements for the window from the named companies.
  READ FIRST    Planes, Planes/following, Proof_Intel_Services, Israel
  GATEWAY       alternative-perpetrator-notice
  NOTE          The best evidence handling on the site (flight-data recovery and control-aircraft discipline in {ROOT_CHARTER}). CARRY IT
                ONTO THE PAGE: never call a missing record a removal until a control aircraft fails the same way, and publish weakening
                results as prominently as supporting ones. Rental records (ordinary private subpoenas) are the reachable half.

----------------------------------------------------------------------
T7 | foreign-registered-handsets-on-campus
    Handsets purchased and registered on a foreign carrier were present on the UVU campus.
  CONTENTION    Devices registered to a foreign telecom were operating on campus.
  WOULD REQUIRE What cell-site and tower-dump material the State collected; what was analysed vs merely collected; extraction reports;
                foundational testimony of whoever handled it.
  READ FIRST    Proof_Intel_Services, technology_surveillance, Israel, court/Phone_Extraction, court/Robinson_Phone_Devices
  GATEWAY       alternative-perpetrator-notice
  NOTE          The thesis most likely to slide into naming people; it stays a demand for RECORDS plus foundational questions. The strong,
                grantable question underneath is narrow: what was collected, what was analysed, what happened to the difference.

----------------------------------------------------------------------
T8 | the-university-owned-house
    We are asking who was in a university-owned property close to the site, and which vehicles were in front of it.
  CONTENTION    We are asking who was in a specific university-owned property near the site in the relevant window.
  WOULD REQUIRE Occupancy, booking, keying and access records for the window; frontage camera coverage; associated vehicle records.
  READ FIRST    After/house, Locations, property_locations, After
  GATEWAY       -
  NOTE          {DOCS_DIR}/After/house has its own charter; read it first. One of the most REACHABLE theses: a subpoena duces tecum to a
                university for its own property records is routine and fights no agency. Any current or former occupant is a living
                private person and is not named.

----------------------------------------------------------------------
T9 | withheld-exculpatory-material
    Exculpatory material exists in UVU footage and in federal holdings and has not been provided.
  CONTENTION    Material tending to exculpate exists (campus video; intelligence and military holdings on the aircraft and foreign nexus)
                and has not been produced.
  WOULD REQUIRE The full campus camera inventory and retention record; the production log against it; Brady demands made and responses;
                for the federal holdings, the gateway first.
  READ FIRST    cameras, CoverUp, court/discovery-brady-disputes, Proof_Intel_Services
  GATEWAY       alternative-perpetrator-notice, for the federal half only
  NOTE          Split the page cleanly: the CAMPUS half is ordinary Brady and spoliation practice against a reachable custodian, close to a
                certainty as a motion; the FEDERAL half is hard and gateway-dependent. Separation keeps the reachable half from being
                dismissed with the unreachable one.

----------------------------------------------------------------------
GROWING THIS APPENDIX: see STAGE 3. New ids continue at T10; log every addition and retirement in {RUN_LOG} with date and reason.


============================
APPENDIX B - THE RECORD, AND WHERE TO GO GET MORE OF IT
============================

  {COURT_DIR}/
    ai_attorney/        this section
      _work/            ledger, thesis map, evidence list, run log - private
      p_ai_attorney.md  this prompt - private, never publishes
    Days_in_Court/      one page per reported court date, 2025-09-16 onward
    legal_docs/         the primary-source archive
      _markdown/        one .md per PDF: 2025/, 2026/, transcripts/, warrants/,
                        mirandize/, analysis/, misc/
      _text/            pdftotext and OCR sidecars
      _work/            docket reconstructions, fetch logs, manifests,
                        gen_tracking.py
      tracking.txt      the archive index and the completeness scoreboard
    mirandize/          the custody-timing line: if he was in custody with his
                        phone seized, who typed the message
    Preliminary_Hearing/ Day 1 through Day 4 pages
    score_card/         the reader's own scoring sheet
    plus case-level Level 3 pages: ballistics-atf-cbla, case-overview,
    Cellebrite, defense-bindover-brief-aggravator, defense-team,
    discord-evidence-court, discovery-brady-disputes, gag-orders-sealing,
    hearing-witnesses, investigation-index,
    judges, judge-tony-graf, judge-robert-lunnen, people-on-witness-stand,
    Phone_Extraction, preliminary-hearing-motions, prosecution-team,
    Robinson_Phone_Devices, testimony, Twiggs_Phone, utah-county-jail-custody

READING THESE IS THE WORK: the archive makes the right-hand column possible; a thesis page written without opening the transcripts is
an opinion piece.
WHAT WE HOLD (last count): 867 docket entries known; 62 private or sealed; 258 with a public PDF ever posted; 374 unique PDFs held; 378
markdown conversions. The real shortfall is the CONFIRMED GAPS list in {TRACKING_TXT}. Quote the ratio when a page leans on absence.
TRANSCRIPTS: certified Day 4 and Day 5 only, plus a redacted transcript of the 2025-10-24 sealed-motion hearing; Days 1-3 are press and
pool only, which is why most "not asked" claims sit at T3 ("not found in the material we hold"). OBTAINING THE DAY 1-3 CERTIFIED
TRANSCRIPTS IS THE SINGLE HIGHEST-VALUE ACQUISITION (it upgrades many claims T3 -> T1 at once); first item of STAGE 1 until done.
NEW DOCUMENTS: Utah courts publish nothing directly; sources are the Burkhart substack docket reconstruction and charliefiles.com (fetch
logs, TSVs, manifests under {LEGAL_WORK_DIR} record what was pulled when). Signed orders are often image-only and need OCR. Keep every
copy; never overwrite one.
OUTSIDE THIS REPO (same investigation):
  ~/BGit/all/politics/charlie_kirk/              prompts, research, laws, letters
  ~/BGit/all/politics/charlie_kirk/aiattorney/   an earlier question-and-answer run with its own input documents


============================
APPENDIX C - EVIDENCE LINKAGE (PLACEHOLDER, GROWS EVERY RUN)
============================

Maintained as {EVIDENCE_CSV} by STAGE 8, so every TABLE row eventually points at a real artefact, held or named-and-missing.
Seed rows for the first run that reaches this stage:

  evidence_key                    thesis  kind           held  note
  prelim_transcript_day4          T1;T2   transcript     yes   certified
  prelim_transcript_day5          T1;T2   transcript     yes   certified
  prelim_transcript_day1_3        T1;T2   transcript     no    HIGHEST PRIORITY
  ballistics_motion_apr2026       T1      filing         yes   defense motion to
                                                               stop further
                                                               testing of the
                                                               bullet jacket
  atf_comparison_result           T1      exhibit        partial sealed in part
  soil_excavation_workorder       T2      record_demand  no    custodian unknown
  lab_request_log                 T1;T2   record_demand  no    the list of tests
                                                               actually ordered
  microphone_hardware             T1;T4   exhibit        no    the device itself
  av_procurement_chain            T4      record_demand  no    private vendors -
                                                               reachable
  campus_camera_inventory         T9      record_demand  no    reachable
  cad_dispatch_record             T5      record_demand  no    reachable
  rental_agreements_window        T6      record_demand  no    reachable
  adsb_recovered_traces           T6      dataset        yes   in-repo, under
                                                               Planes
  university_property_records     T8      record_demand  no    reachable
  halted_inquiry_testimony        T3      external       no    the official has
                                                               already spoken
                                                               publicly

The "held=no, reachable" rows are collectively this exercise's discovery list, the most useful thing it produces for anyone else.


============================
APPENDIX D - THE RUN LOG FORMAT
============================

{RUN_LOG} is append-only markdown, one block per run:

  ## Run <YYYY-MM-DD>

  Case movement since last run:
  Theses worked:
  Pages created:
  Pages improved:
  Table rows added / tiers upgraded:
  Deletions, with reasons:
  Appendix A changes:
  Documents downloaded:
  Could not source:
  Strongest finding this run:
  Strongest counterargument conceded this run:
  Blocked on:

The last two lines matter: a run that conceded no counterargument did not look hard enough, and a section that only confirms its beliefs
loses careful readers.


============================
APPENDIX Z - THE ORIGINAL DICTATION THIS PROMPT WAS BUILT FROM
============================

Kept verbatim so the intent behind the structure above is never lost. Where this
appendix and the stages above disagree, the stages above win - but read this
first if you are unsure why something is the way it is.

  This prompt file is about acting as an AI attorney, defense attorney. That's
  going to be a different team than the human AI attorneys that Tyler Robinson
  has. The goal here is that we're going to take it that there are certain
  things. We'll have an appendix A that has a certain thing, as well as the
  things that are true.

  This is about taking the ai_attorney directory and putting files in there. The
  question is: we have an Appendix A, and there could be more in Appendix A. The
  idea here is that when we want to create almost a table in the left and the
  right, the left is what you would do as this ai_defense_attorney in this
  specific case. We'll tackle each of these listed in Appendix A as a different
  table on a different page. We'll have the overview.mdx in that ai_attorney
  directory have a list that correlates to the list in Appendix A. Each
  hyperlink you click on goes off to a page, and it'll have that table that'll
  go to one number in Appendix A. You'll have a table there on the left: what
  the AI attorney would do as far as asking questions of certain people in order
  to prove that case.

  On the right column, it's a matter of: Did that stage in the trial happen in
  the past, or is it upcoming? Did that witness get on stage? Did the real-life
  defense attorney ask that question or not? You might put a date and the
  personnel on the stand, and make a note that the defense attorney did not ask
  that question that you would have asked. In the left cell of the table, you're
  putting in the question you would have asked of the attorney of that person on
  that date.

  Your analysis below is: as a defense attorney, would this hold up as a legal
  defense? Cross-index all the facts across the whole site that are relevant or
  support it. What would you ask, or what would you pull out of the evidence?
  Assume that a lot of evidence was not provided. What would you make requests
  for evidence?

  We're looking for the gap analysis. We want to have that chain of reasoning of
  what the attorney would do, and also that gap analysis of where the human and
  real-world one may well seem to have skipped that. On this whole page, you're
  writing at the level 3 MDX under this ai_attorney directory. It will be one of
  these chains of thought and chain, and the real-life defense attorney will
  cover it fully, or what parts did they miss? What would the defense attorney
  have done?

  You can grow Appendix A if there are more of these. Learn from the current
  pattern.

  Right now, it seems like the defense attorney is not willing to question
  Israel or the government or intelligence services, and they're mostly sticking
  within the scope of the government's narrative.

  There's a directory tree below. You can turn that into Appendix B. Note that
  reading those is very valuable to do this when you're running this: doing more
  research, finding the newest court documents, and downloading them. We want to
  have a copy of old court documents. We should have them up to a certain date,
  as of August 29th, and you can read into them for an income analysis so far
  and so on.

  We will have Appendix C create a placeholder one. Over time, we'll put in
  linkages to evidence that are relevant.

  Have this run in stages. Have it build up the output for the most part as
  AI_Attorney telling that story. We have those pages to cover each one of
  these, and then the overview below the table that goes off links to them. You
  can go give a summary of that and put it on all these pages. This is only the
  personal opinions of AI, and it's just a thought analysis. We make no claims
  of any unethical or illegal behavior by the defense team for Tyler Robinson or
  anybody else.
