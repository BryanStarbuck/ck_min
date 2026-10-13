Build and update the Body Tour: 3D medical diagrams of the State's Exhibit 11 injuries, made easy
for a jury to understand. One contents page lists the body parts, and one page per body part has
two tabs: "If Bullet" and "Shaped Charge Explosion".
This file is a prompt. It is excluded from the Docusaurus build by the "**/p_*.{md,mdx}" rule in
docusaurus.config.ts, so it never publishes even though it sits in site/docs/scorecard/exhibit/.


ROOT_DIR dir is ~/BGit/Bryan_git/charlie-kirk

SITE_DIR dir is {ROOT_DIR}/site
EXHIBIT_DIR dir is {SITE_DIR}/docs/scorecard/exhibit
TOUR_DIR dir is {SITE_DIR}/internals/static/scorecard/exhibit          (served at /scorecard/exhibit/)
ASSETS_DIR dir is {TOUR_DIR}/body_tour_assets
CONTENTS_PAGE is file {TOUR_DIR}/body_tour.html                       (the table of contents)
PART_PAGE is file {TOUR_DIR}/{body_part}.html                           (one per body part)
PARTS_JS is file {ASSETS_DIR}/parts.js                                  (the one list of parts; feeds every menu)
ANATOMY_JS is file {ASSETS_DIR}/anatomy.js                              (the 3D body, anchors, findings, camera shots)
EXHIBIT_PAGE is file {TOUR_DIR}/overview.html                           (State's Exhibit 11 page; GENERATED, never edit)
EXHIBIT_BUILDER dir is {ROOT_DIR}/Prompts/exhibit_build                 (edit its template + build_exhibit_11.py instead)
ANALYSIS_PAGE is file {EXHIBIT_DIR}/analysis.mdx
DIR_CLAUDE is file {EXHIBIT_DIR}/CLAUDE.md                              (READ it; never write it)
TOOLS_DIR dir is {ROOT_DIR}/Prompts/body_tour_build
TOUR_REFERENCE is file {TOOLS_DIR}/README.md                            (scene vocabulary, coordinates, how to add a part)
CHECK_SCENES is file {TOOLS_DIR}/check_scenes.mjs
SHOOT is file {TOOLS_DIR}/shoot.mjs
WOUND_RECORD is file {SITE_DIR}/docs/scorecard/Not_A_Rifle_Wound/Details/Wound_Record.mdx
LOCATIONS_FILE is file {EXHIBIT_DIR}/locations.md                     (where the transmitter sat, the angles, the video research; draft: true, never published)
SCORECARD_OVERVIEW is file {SITE_DIR}/docs/scorecard/overview.mdx
SIDE_TO_SIDE is file {SITE_DIR}/docs/scorecard/Not_A_Rifle_Wound/Side_To_Side.mdx
STAGING_DIR dir is {ROOT_DIR}/Prompts/scorecard_build/staging/scorecard  (staging twins of the two scorecard pages)
MEMO_PDF is file {SITE_DIR}/internals/static/court/filings/2026/246_2026-07-28_Memorandum_in_Support_of_Preliminary_Hearing_Bindover.pdf
ASSESS_MANUAL is file {ROOT_DIR}/prompts/Assess_Manual.md
CK_FILE is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt     (READ-ONLY, always)
SHOTS_DIR dir is ~/T/_body_tour_shots
THE_DATE_TIME_STRING is the string "{Date}_{Time}_" where it uses "_" instead of any special characters, so it is purely alphanumeric or underscores.
REPORT_FILE is file ~/to/CK_Body_Tour_Update.md

BODY_PARTS are, in this order (the order of the top-bar menu): neck, brain, heart, lungs, spine
NEW_BODY_PART is ... = (none)
  * If the run text names a body part that is not in BODY_PARTS ("add the liver", "do the eardrums"),
    that is NEW_BODY_PART. Add it (STAGE 3), then append it to BODY_PARTS.
TABS are: "If Bullet" (data-tab bullet) and "Shaped Charge Explosion" (data-tab charge)
STEPS_PER_TAB is 4 to 8           (the last step of each tab is always the verdict)

Read {ROOT_DIR}/CLAUDE.md, DIR_CLAUDE, TOUR_REFERENCE, LOCATIONS_FILE and ASSESS_MANUAL into the context
window before anything else.


====================================================================
  WHAT WE ARE BUILDING
====================================================================

Think like a cinematographer and a medical illustrator. Think of motion graphics in the spirit of
Claude Motion (code that animates text, lines and shapes), but built straight into the page:
three.js for the body, scroll-driven steps for the story. Claude Motion itself cannot be driven
from Claude Code.

* CONTENTS_PAGE is almost a menu: a list of body parts and a 3D figure. Click a part and you go to
  its page.
* Every PART_PAGE gets its own page, illustrated as if we are giving it to a jury to make it easy to
  understand.
  * The top bar: a back button at top left (to CONTENTS_PAGE), the body part name at top left, the
    two tabs, and the menu of every body part.
  * The body is drawn in 3D. The outer body is a see-through mesh. Inside it, the organs that matter
    for this part are solid: a chest, a head or a neck; the heart; the two lungs; the spine.
  * It reads like a marketing page. As you scroll, text cards rise on the right, lines reach over to
    point at what each card is talking about, and things appear, light up, fade or break apart.
    Tell the story so a jury understands it, and stay technically accurate.
* Tab "If Bullet": go through that hypothesis. If it was a bullet, where did it go in, where did it
  probably go, where is the damage, and which damage is disconnected from that path? Show where the
  path probably was, and the indicators that it was not a bullet. Speak like a medical examiner
  talking to a jury in their own terms. Tour through why the case does or does not hold.
* Tab "Shaped Charge Explosion": a very small amount of explosive, a shaped charge, powerful
  enough, in the microphone transmitter he wore on his chest under his shirt, on the right side.
  It blasts into his chest. The jet goes up and across his body, across the torso, to the front-left
  of the neck, and a pressure (concussion) wave passes through the chest. Go through that
  hypothesis in the same 3D body, with the insides see-through so the organ is the focus. Show the
  concussion wave. Point out which connections are probable and which are not.

The stance. The only public words of Exhibit 11 come from a document written by the prosecution: the
State's July 28, 2026 bindover brief, MEMO_PDF, pages 2 and 3. It is very heavily one-sided. Do not
take it as the truth. Our thesis is that the State's story does not hold. The site's investigation
concludes, close to conclusively, that it was a shaped charge explosion at the microphone. Do not
discount that and do not underweight it. Keep it honest: every claim is sourced, attributed, and
true to standard anatomy and blast and gunshot medicine.


====================================================================
  HARD RULES
====================================================================

* Quote Exhibit 11 exactly as the brief prints it, square brackets and "…" included. Check every
  quote word for word against WOUND_RECORD. Never invent a finding, a measurement, or a location the
  quoted lines do not give. When the drawing needs a place the report does not give (where in the
  cord the missing length was), draw an example and say in the text that it is an example.
* Say whose words are whose. "Bullet", ".30 caliber", "fragmented" and "front to back, slightly left
  to right, and downward" are the prosecutors' words, written outside the quotation marks.
* The .30-06 is "the government's narrative"; the shaped charge at the microphone is the
  investigators' conclusion. Never let the site's own narration argue against the charge. Never
  bring up electrocution.
* Defamation: never state or imply that a prosecutor, the medical examiner or any living person
  lied, misquoted or acted wrongly. The point is that the public cannot check the report. Tyler
  Robinson is "charged, not convicted, and presumed innocent". Never imply the security team, the AV
  crew or TPUSA staff knew of, placed or touched any device. Never write "hand off". No suspicion
  scores or "suspicious" labels.
* Attribute every analyst claim by name (Jon Bray's motion maps and sound work, Ali Zreik's frame
  review). Anonymous commenters stay anonymous, and the text says they never examined the body.
* Every PART_PAGE keeps the "About the drawing" note and the legal note in its footer.
* The transmitter's position and every angle follow LOCATIONS_FILE (DEVICE_XY, DEVICE_ZONE, BULLET_ANGLE in
  ANATOMY_JS). Change them only with new evidence, and record that evidence, the measurement and the date in
  LOCATIONS_FILE first. Measured from the front camera (2026-10-13): the clip sat about 2 in below the
  T-shirt neckline and 2 to 3 in right of center, just under the right collarbone; the State's path is drawn
  at the sworn 9 degrees with the published 4 to 10 degree range shaded.
* Never edit EXHIBIT_PAGE by hand (change EXHIBIT_BUILDER and rebuild). Never edit site/sidebars.ts.
  Never write to CK_FILE.
* CLAUDE.md files are human-owned. Never create, edit or append to any CLAUDE.md, DIR_CLAUDE
  included. If one goes stale, put the exact proposed text under "CLAUDE.md suggestions" at the end
  of REPORT_FILE. Pass this rule on to any agent you start.
* HTML pages live in TOUR_DIR, never in site/docs/ (docs serves only md/mdx). three.js stays
  vendored in ASSETS_DIR; never load a script from a CDN.


====================================================================
  STAGE 0: READ
====================================================================

* Read, in full: ANALYSIS_PAGE, WOUND_RECORD, SIDE_TO_SIDE, and the text of pages 2 and 3 of
  EXHIBIT_PAGE.
* Read these site pages for the evidence each tab draws on:
  * {SITE_DIR}/docs/scorecard/Not_A_Rifle_Wound/ : Wrong_Angle.mdx, Too_Little_Damage.mdx,
    Injuries_Dont_Fit.mdx, No_Ballistic_Match.mdx
  * {SITE_DIR}/docs/scorecard/Charge_At_The_Mic/ : overview.mdx, Transmitter_Under_Shirt.mdx,
    Shirt_Moves_First.mdx, Expert_Found_Transmitter.mdx
  * {SITE_DIR}/docs/Medical/ : shape_charge_vs_bullet.mdx, charlies_injuries.mdx,
    missing_spinal_cord_question.mdx, doctors_question_me_report.mdx
* Read PARTS_JS, ANATOMY_JS (ORGANS, GROUPS, ANCHORS, FINDINGS, SHOTS, DEVICE_XY, DEVICE_ZONE, BULLET_ANGLE),
  CONTENTS_PAGE and every existing PART_PAGE.
* Grep CK_FILE (read only) for anything newer than the pages: a release of the full report, new
  filings, new testimony, new analysis of the wound.

Output to stdout:
"
=====================================================
  STAGE 0 done: evidence read; {N} body parts on file
=====================================================
"


====================================================================
  STAGE 1: DECIDE THE WORK
====================================================================

* If NEW_BODY_PART is set: do STAGE 3 for it, then STAGE 2 and STAGE 4 for it only, then STAGE 5
  for every page (the menus and footers changed everywhere).
* Otherwise, for each part in BODY_PARTS: compare its page with what STAGE 0 found. Note every
  quote, fact, source link or argument that is new, changed or wrong. Those parts get STAGE 2 and 4.
* If the full Exhibit 11 report has been made public: stop and tell Bryan before changing anything.
  Every page would then be rebuilt from the report itself, not from the brief's quotes.


====================================================================
  STAGE 2: REASON THROUGH EACH BODY PART
====================================================================

For each body part being worked on, write the reasoning down in a scratch file in TOOLS_DIR named
{THE_DATE_TIME_STRING}{body_part}_reasoning.md before writing any HTML.

* List that part's Exhibit 11 findings: the exact quote, the exhibit page, and the plain-English
  meaning.
* If Bullet: draw the State's account faithfully (entry low on the front-left of the neck; the sworn
  9-degree drop; a slight drift toward his right; no exit wound; the stretch zone of a high-speed
  round, drawn generously). For each finding, is it reached, strained, or not reached without a
  second cause? Give the bullet its best case (bone shattering, fragments, blood draining from the
  neck, resuscitation) and say where even that falls short. Use distances only as "about", from the
  model.
* Shaped Charge Explosion: the transmitter on the upper right chest, where the front camera shows its
  clip (LOCATIONS_FILE); the dashed zone reaches down to the nipple-level written accounts. The jet goes
  up and across to the front-left of the neck, about 45 degrees upward; damage radiates from that point; the pressure wave
  hits both sides of the chest at once (blast lung, chest-wall bruising, blood in both cavities,
  cardiac contusion); a pressure surge rides the arteries to the brain (Courtney and Courtney 2009).
  For each finding, does it fit?
* For each finding, a verdict for each tab: Fits, Either, Strains it, or Not reached.
* What would settle it: the tests or records that would decide each finding.


====================================================================
  STAGE 3: ADD A NEW BODY PART (only when NEW_BODY_PART is set)
====================================================================

Follow "Adding a body part" in TOUR_REFERENCE:
* New organs, anchors, findings and camera shots go in ANATOMY_JS, in the patient's own coordinates
  (+x = the patient's LEFT), baked into the geometry.
* Add the part to PARTS_JS. Every page's top-bar menu then includes it automatically.
* Create its PART_PAGE by copying neck.html's structure.
* Add it to CONTENTS_PAGE (the part list with data-part, and the "at a glance" table), and to "The
  other body parts" list in every other PART_PAGE's footer.


====================================================================
  STAGE 4: WRITE THE PAGES
====================================================================

* Each tab: an intro (eyebrow, title, two sentences), then STEPS_PER_TAB steps. Each step is one idea:
  a kicker, a title of 4 to 9 words, 2 to 4 short paragraphs or a list, an Exhibit 11 quote box when
  the step is about a finding, and a source line linking the site page the fact comes from.
* The last step of each tab: a verdict table (finding, explanation, chip), a "What would settle it"
  list on the Shaped Charge tab, and buttons to the other tab and the next part.
* Each step's scene (vocabulary in TOUR_REFERENCE): move the camera like a film. Open with a wide
  establishing shot, push in to the organ, cut to a cross-section when order or depth matters, pull
  back for the verdict. Use 2 to 4 labels of 7 words or fewer, and set "point" to what the card is
  about. Use red for reached, amber for not reached, blue for the State's path and orange for the
  blast.
* Plain words first, the medical term second. Short sentences. No hedging the investigators'
  conclusion in the site's own voice. Attribute everything that is a person's reading.
* Keep the head (title, description, og tags), the top bar, the footer sources, the "About the
  drawing" note and the legal note on every page.


====================================================================
  STAGE 5: VERIFY
====================================================================

* Run: node --no-warnings {CHECK_SCENES}   (from ROOT_DIR). Fix every problem it lists.
* Make sure the dev server is up (just localhost, http://localhost:3377/). Then run SHOOT into
  SHOTS_DIR, for the changed parts or all of them:
  PW_CORE=~/T/_pw/node_modules/playwright-core/index.mjs node --no-warnings {SHOOT} {parts} {SHOTS_DIR}
  (If playwright-core is missing: mkdir -p ~/T/_pw && cd ~/T/_pw && npm i playwright-core)
* Look at the screenshots, desktop and phone. Every step: the camera frames what the card talks
  about, labels do not cover each other or the key organ, the card's leader line lands on its label,
  and the text is readable. Fix and re-shoot until each one is right.
* Every link on the pages resolves: site routes against {SITE_DIR}/.docusaurus/routes.js, files
  under {SITE_DIR}/internals/static/.
* If any MDX changed: node {SITE_DIR}/_ck_mdxcheck.mjs {files}, then cd {SITE_DIR} && npm run build.


====================================================================
  STAGE 6: KEEP THE WAYS IN
====================================================================

* SCORECARD_OVERVIEW and SIDE_TO_SIDE each show three buttons in their ck-sc-cta block: Exhibit 11,
  Who Wrote Page 2? Analysis, Body Tour (3D) (href /scorecard/exhibit/body_tour.html, a plain <a>).
  Their twins in STAGING_DIR must match.
* The Exhibit 11 "More" menu (EXHIBIT_BUILDER template) and ANALYSIS_PAGE link to CONTENTS_PAGE and
  to each body page. Add a link for a new part there too.


====================================================================
  STAGE 7: REPORT
====================================================================

* Write REPORT_FILE: a summary on top (which parts changed and why, in a few lines), then each
  part's changes, the screenshot folder, anything held back with the reason, and open questions for
  Bryan. End with "CLAUDE.md suggestions" (file, line, exact proposed text) if DIR_CLAUDE or any
  other CLAUDE.md is now stale.

Output to stdout:
"
=====================================================
  Body Tour updated: {list of parts}
  Contents page: http://localhost:3377/scorecard/exhibit/body_tour.html
  Report: ~/to/CK_Body_Tour_Update.md
=====================================================
"
