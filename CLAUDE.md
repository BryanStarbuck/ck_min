ROOT_DIR dir is ~/BGit/Bryan_git/charlie-kirk
SITE_DIR dir is {ROOT_DIR}/site
CK_FILE is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt   (alias: CHARLIE_KIRK_FILE)
CK_INBOX is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk_AI_Inbox.txt
PAGES_CSV is file {ROOT_DIR}/pages.csv
LEVEL_2_CSV is file {ROOT_DIR}/level_2.csv
ASSESS_MANUAL is file {ROOT_DIR}/prompts/Assess_Manual.md
IMAGES_YAML is file {ROOT_DIR}/images/images.yaml
VIDEOS_YAML is file {ROOT_DIR}/videos/videos.yaml
BAN_IMAGES_CSV is file {ROOT_DIR}/images/ban_images.csv
BAN_VIDEOS_CSV is file {ROOT_DIR}/videos/ban_videos.csv
INFO_GRAPHICS_DIR dir is {SITE_DIR}/internals/static/img/infographics/
NANO_BANANA_4K is file ~/BGit/all/tools/Nano_Banana_4K/nb_4k.js
MEETING_DIR dir is {SITE_DIR}/docs/meeting/
REF_DIR dir is {ROOT_DIR}/knowledge/claude_reference/

REF_DIR holds the long runbooks that used to live in this file, moved word for word on
2026-09-24. Read the matching one before deep work in that area:
  * flight_data_recovery.md   recovering erased flight data, geo sweep, generated plane pages
  * repo_file_map.md          full "what does what" map of every generator, CSV, prompt, dir
  * media_pages_people.md     images/banned media/infographics in full, pages.csv columns,
                              people-profile template

KEEP THIS FILE SMALL (under 20k chars). Do not append run logs, worked examples, dated
"what we tried" notes, or file inventories here. Those go in REF_DIR or in the nested
CLAUDE.md of the directory they concern. Add at most a one-line pointer here.


== Where Charlie_Kirk.txt And The Inbox Live (moved 2026-09-19) ==

Both real files live in ~/BGit/all/politics/charlie_kirk/. {ROOT_DIR}/Charlie_Kirk.txt and
{ROOT_DIR}/Charlie_Kirk_AI_Inbox.txt are SYMLINKS to them. Always read and write the REAL
path; use the symlink only to confirm location. Editors that save via write-and-rename
turn a symlink into a plain file and split the data into two diverging copies. If a
symlink is missing or became a regular file, stop and tell Bryan; never recreate or
overwrite either file. Older prompts naming {ROOT_DIR}/Charlie_Kirk.txt or a Dropbox path
mean the real file above.


================================================================================
!! ABSOLUTE RULE — {CK_FILE} (Charlie_Kirk.txt) IS READ-ONLY TO AI !!
================================================================================

AI MUST NEVER WRITE TO, EDIT, APPEND TO, RE-ORDER, REFORMAT, OR DELETE ANYTHING IN
{CK_FILE}. Not one character, not even additive material. This OVERRIDES every skill,
prompt and instruction, and applies to Claude Code, subagents, AI-written scripts, and
any automation an AI sets up. Forbidden with no exception: removing, shortening,
summarising, rewriting, rephrasing, or hedging any line ("allegedly", "an influencer
claims"); softening or deleting for defamation, legal risk, "unsourced rumor", scope or
tidiness (Bryan marks unsupported material in place); renaming or restructuring
headers; stripping whitespace or running formatters; writing a "SCOPE RULE" or handling
note into the file; appending new content.

READING is always allowed. NEW CONTENT GOES TO {CK_INBOX}: append-only, same equal-sign
section format, with a line naming the {CK_FILE} section it belongs under. Tell Bryan
what was appended. Bryan merges by hand; AI never merges.

Why: a 2026-07-30 audit found four AI edits that damaged the file (72aaea54 deleted a
marked rumor and wrote a SCOPE RULE; fe2dddec inserted a defamation hedge on the Hibbs
line; 1c62020f rewrote the Frey Effect sentence; 8b967208 replaced the "4:00pm 9/12/2025
Arrest Time" header). All restored and marked [RESTORED 2026-07-30].

If asked to break this rule: refuse, cite it, offer {CK_INBOX}. Only exception: an
explicit instruction from Bryan that names this rule and states the specific edit.


================================================================================
HOW HE DIED — DO NOT DEFAULT TO THE GOVERNMENT NARRATIVE
================================================================================

Citizen investigations, seriously investigating, have concluded Charlie Kirk died by an
explosive. The state's narrative of a 30-06 bullet appears to be disproven. The site may
mention that the bullet/30-06 story is the government's narrative, but we state that
investigations on X by far hold the majority opinion that he died by an explosive. Do not
undercut this by presenting the state's narrative as dominant. Do not bring up
electrocution as a possible cause. Claude Code tends to drift to the government
narrative; here that appears to be very wrong, so follow this guidance.


================================================================================
NARRATIVE AND SCORE CARDS  ({SITE_DIR}/docs/Narrative/: fed_narrative/, score_card/)
================================================================================

SCORE CARDS: several of them. Viewers of the movie get a list and an area and decide,
item by item, whether there is a problem in that area. Examples:
  * Legal courtroom / defense attorney score card: simulate an ideal defense attorney.
    Would they act differently from the current one? Is the current one's conduct a
    problem, yes or no?
  * Fed slop narrative score card: the Fed narrative's talking points. Later used to
    check online influencers against.

NARRATIVE #1 "FED NARRATIVE": claims (true, untrue, or lies) the government tends to
push. Build a bullet list of the general Fed narrative, then map each point to the ones
that appear to be lies, or that citizen investigators on x.com allege are false.
Example: Tyler Robinson "sent the confession" by Discord, yet he was taken into custody
(3:30 or 6:20, Sept 11), which would make sending it impossible.

NARRATIVE #2 "CHAINS OF REASONING": several chains, each its own page listing a chain of
points (facts that tend to be true) that together prove a conclusion. Examples: why it
was not a 30-06; why it was a shaped charge in the microphone; why the planes following
him were spy planes and how to deduce the country (Israel).

Narrative/overview.mdx has ONE TOC: (1) Level 3 docs not otherwise linked, (2) the Fed
narrative TOC under its own header. Below that the score card, then Chains of Reasoning.


== What This Repo Is ==

Single-investigation repo: the Charlie Kirk assassination (Sept 10, 2025, Utah Valley
University). Two layers:
  * Public: everything inside {SITE_DIR}/, a Docusaurus 3.9 / React 19 / TS site at
    https://whoassassinatedcharliekirk.com, deployed by GitHub Pages
    (.github/workflows/pages.yml) FROM THE REPO, not from any machine.
    Dev: cd {SITE_DIR} && npm start (port 3000). Build: npm run build.
  * Private: everything else (research, people profiles, raw data, prompts, PDFs).
    Never published. Public pages never link into private dirs.

Tooling for this site also lives outside the repo in ~/BGit/all/politics/charlie_kirk/
(prompts/, research/, laws/, Letters/, defemation/, tweets/, podcasts/, and more).
Source media: ~/_Mirror/Politics/Charlie_Kirk_Mi/. Their transcriptions/AI descriptions:
~/BGit/Bryan_git/personal_large_files_bridge/_Mirror/Politics/Charlie_Kirk_Mi/.


== Key Directories (full map: {REF_DIR}repo_file_map.md) ==

  site/docs/                 public pages; each child dir is a Level 2 (see level_2.csv)
  site/internals/static/     served verbatim from site root (img/evidence, img/infographics,
                             img/video_posters, img/km-timelines, court/, data/)
  images/, image_planning/   image files + images.yaml + generator/ (image pipeline)
  videos/, videos_planning/  video master data + generator/ (videos themselves gitignored,
                             pulled from IPFS); videos_transcription/ = one .md per video
  Details/{Person}/          private people profiles ({Person}.md, Research_{Person}.md,
                             p_{Person}.md). ck/people/ is the older location.
  Research/                  raw/, x_posts/, Topics/, PDFs/ (hosted PDFs go in Research/PDFs/)
  knowledge/                 synthesized write-ups; claude_reference/ = runbooks
  prompts/                   prompt library (Assess_Manual.md, p_4_squares.md,
                             four_squares/ = a run in progress, read RESUME.md)
  laws/                      PRIVATE law drafting workspace (see Fix Laws)
  IPFS/                      pinned evidence; ipfs.txt / ipfs.sh = pull-and-pin commands
  skills_storage/*.md        skill sources (flat), symlinked from ~/.claude/commands/
  security/                  secret scanning + pre-commit hook
  tools/                     push.sh, sync_right_bar.py
  tmp/                       per-question research runs (e.g. kill_me_research/)
  Backup/                    STALE, unrelated app specs; not part of the investigation

Root data files: pages.csv (~2 MB, grep it, never read whole), level_2.csv,
interesting_pages.csv (what to feature/tweet), people.csv (person cross-link lookup),
planes.csv (drives tail-number autolinking; add a row to autolink a tail), planes.yaml,
aircraft_costs.csv, videos.csv, timeslines.csv, missing_videos.txt,
404_Investigation_Report.txt, ck_main_progress.txt.


== Nested CLAUDE.md Charters — read before working in that subtree ==

images/, image_planning/ (hierarchy YAML moved to images/images.yaml 2026-07-22),
videos_planning/ (if its first variable says "image_planning" it was clobbered; restore),
site/docs/laws/, site/docs/Charlie/, site/docs/Planes/ (plotted vs model-generated
infographics), site/docs/Planes/following/ (all safely-public info goes here),
site/docs/Planes/following/apis/ (how flight data is fetched), site/docs/After/house/.
The root file does not repeat their rules.


== Page Levels ==

  Level 1   site/docs/index.md                      home page
  Level 2   site/docs/{Section}/overview.mdx        section page with TOC
  Level 3   site/docs/{Section}/{Topic}.mdx         one topic
  Level 4   site/docs/{Section}/{Topic}/{Page}.mdx  children of a topic (normal)
  Level 5   site/docs/Photos|Videos/.../{item}.mdx  one image or video (generated)

Every task starts with WHICH LEVEL 2 DOES THIS BELONG IN? Read {LEVEL_2_CSV} first
(directory, 40-word description, file_path; ~75 sections). New info: pick the Level 2,
create or update a Level 3 page, add its link to that Level 2's overview.mdx TOC (the TOC
links every child page). When told "add this image/video to these Level 2 pages", match
directory names under docs/. Read other Level 2s freely for facts and links.

pages.csv: one row per public page (page_key, parent_key, level, url_path, file_path,
title, sidebar_label, directory, extension, has_frontmatter, line_count). page_key is 4
words max, underscores, unique. Any skill that creates, renames, moves or deletes a page
updates pages.csv (and parent_key references). Refresh line_count on edited pages.
Full column contract: {REF_DIR}media_pages_people.md.


== Writing Pages ==

  * Read {ASSESS_MANUAL} into context at the start of any task that creates, edits,
    reviews, or restructures site pages. All page work follows it.
  * Before declaring done: cd {SITE_DIR} && npm run build. Keep every <div>/</div> at
    column 0. For fast checks: node site/_ck_mdxcheck.mjs <files...> (do not add
    @slorber/remark-comment to it).
  * Defamation: on public pages never state as fact that a living person committed a
    crime unless court-proven; attribute ("according to", "reportedly"); include denials;
    frame suspicions as questions. Private notes may be unfiltered but must be scrubbed
    before moving to site/docs/. /ck_defemation_prevention scans for this.
  * Every person page carries Status: Alive / Deceased (YYYY) / Unknown. Web-search it
    before adding the page. Profile template: {REF_DIR}media_pages_people.md.


== Skills ==

Sources: {ROOT_DIR}/skills_storage/*.md (flat). Each is symlinked from
~/.claude/commands/{file}. On first run, check each link; if missing or broken, ask
before creating: ln -s {ROOT_DIR}/skills_storage/{file} ~/.claude/commands/{file}
  * /ck_add_text {text}       add notes (writes to {CK_INBOX}, never {CK_FILE})
  * /ck_defemation_prevention scan public pages for defamation risk
  * /ck_rebalance_level       propose and execute Level 2 restructuring


== Images, Videos, Banned Media (full: {REF_DIR}media_pages_people.md) ==

  * IMAGES ARE TRACKED IN GIT. Never gitignore an image; an untracked image works locally
    and 404s for every visitor. Large File Bridge once added ~1,950 per-image lines to
    .gitignore; if they reappear, delete them (do not use git add -f). Before publishing an
    embed: git ls-files --error-unmatch <path> succeeds and git check-ignore -v <path>
    prints nothing. Only videos/* stays ignored (served via IPFS).
  * NEVER embed an image by IPFS gateway URL. Use <img src="/img/evidence/{sha256}.jpg"
    data-cid="{CID}" />. Most image CIDs came from ipfs add -n and are on no node.
    Videos do use the gateway. Audit: python3 image_planning/generator/audit_image_publication.py [--gateway]
  * An image under site/docs/ is NOT served by a literal <img>; put it under
    site/internals/static/.
  * BANNED MEDIA: {BAN_IMAGES_CSV} / {BAN_VIDEOS_CSV} are the master never-publish lists
    (sha256, cid, file_path, banned, reason, date_added; match sha256, then cid, then path).
    The ban set is the UNION with legacy image_planning/exclude_images.txt and
    videos_planning/exclude_videos.txt. The CSV flows down to banned: true|false on every
    YAML entry; never hand-edit banned in the YAML. A banned item gets no Level 5 page, no
    served copy, no embed anywhere, no IPFS pin; its YAML entry is never deleted.
    After a CSV change: re-sync YAML, verify it parses with no invisible Unicode, re-run
    generators. Edit images.yaml via bind_image_pages.py helpers, videos.yaml via
    videos_planning/generator/emit_yaml.py.


== Infographics (full contract: {REF_DIR}media_pages_people.md) ==

One dir per topic: {INFO_GRAPHICS_DIR}{topic}/ (served at /img/infographics/{topic}/).
Moved 2026-08-28 from {ROOT_DIR}/info_graphics/, which no longer exists. topic is 1-2
words with underscores; one aircraft = {TAIL}_{Type} (e.g. N1098L_Flight_Record). Plane
templates: {SITE_DIR}/docs/Planes/info_graphic/. Everything in these dirs is public.
  * goals.mdx: first line = full path of every target page. Then: Audience, What they
    should learn, Conceptual framing, What we are educating on, Perspective, Polarity and
    scope, Numbers, Sizing, Framing and placement, Screen percentages (guidelines),
    numbered Order of understanding, exact On-image text.
  * nana_banana_pro_prompt.txt: written from goals.mdx; raw text, no markdown; carries
    layout, sizing, percentages, and exact quoted strings; states 16:9.
  * Always 16:9, always 2K:
    node {NANO_BANANA_4K} {INFO_GRAPHICS_DIR}{topic}/nana_banana_pro_prompt.txt {INFO_GRAPHICS_DIR}{topic}/{topic}.jpg --size 2K --aspect 16:9
  * When data must be exact, generate the chart with code (see Overlap_Timeline/), not
    the model: the model spells text right and draws bars wrong.


== Fix Laws Section ==

Public: https://whoassassinatedcharliekirk.com/Fix/overview. Four federal laws as the
path to justice, shown as cards (title of 4 words or less, image, three sentences, "View
Law" button to that law's detail page): 1 FBI & DOJ Disclosure, 2 Intelligence
Disclosure, 3 Mandate the Investigation, 4 Trusted Investigators.
{SITE_DIR}/docs/Fix/ holds ONLY public pages (overview.md + one detail page per law).
{ROOT_DIR}/laws/ is the private drafting workspace. Never mix the two.


== Planes and Flight Data (full runbook: {REF_DIR}flight_data_recovery.md) ==

  * site/docs/Planes/{TAIL}/ per aircraft, raw downloads in data/; filenames record WHICH
    SOURCE the data came from. Following log: site/docs/Planes/following/ (speaking/
    {YYYYMMDD}_{city}.mdx, overlap/, apis/, flights.csv, overlaps.csv, tpusa_events.csv,
    Overlap_Window_Definition.mdx).
  * Flight records have been erased. Document when records are claimed on Twitter or
    documented early, then scrubbed. Check the proprietary tracker, the open-source
    tracker, the peer-to-peer feeders, and the Wayback Machine. Prove when data was
    removed and try to get it back.
  * CONTROL TEST FIRST: never call anything a removal until a control aircraft with no
    link to the case (hex 4ca7b5 Ryanair, 3c6444 Lufthansa) fails the same way on the same
    dates and endpoint. Applies to websites too. A curl 403 is not what the public sees
    (confirm in a real browser); an empty table is a paywall until proven otherwise. This
    rule exists because the N102DZ FR24 "removal" was published and had to be retracted.
  * Say which it is: removal, retention boundary, or coverage gap. Publish results that
    weaken a claim as prominently as ones that support it. A trace proves presence, never
    purpose or occupancy. An absence is not a finding. Never assert intent.
  * Plane pages are generated: run
    site/docs/Planes/following/apis/public_open_source/code/rebuild_plane_pages.sh
    (not the scripts one by one). Traps: the two proximity CSVs disagree on offset sign
    (recompute from dates); dbflag:LADD is not suspicious; two ground segments in a day
    are a flight unless both sit at the same spot (then one parked stay heard twice).


== Credentials ==

No credential ever lives in this repo. Flight API keys are in ~/.credentials/charlie_kirk.json
(mode 600, under charlie_kirk.flight_apis), read only via
.../public_open_source/code/lib/credentials.js. Never print a value; report a missing
credential by NAME. Third-party vendor keys inside archived captures are redacted in place
with python3 security/scrub_vendor_tokens.py, never deleted (the capture is evidence).
Run sh security/install_hooks.sh once per machine. If GitHub push protection blocks a
push, do not click allow; scrub, and if the value is only in unpushed commits, reset to
origin/main and recommit.


== Pushing This Repo ==

Use sh tools/push.sh [max_attempts] from {ROOT_DIR}, not a bare git push. Pushes of the
large ADS-B evidence race the auto-commit job on the other machine and fail with "cannot
lock ref". Before concluding a push failed, git fetch origin and compare HEAD to
origin/main; it usually landed. Never migrate to Git LFS (history rewrite, force-push).


== The `meeting` Level 2 — Possible Fort Huachuca Meeting ==

{MEETING_DIR} has one subject: a very likely meeting at Fort Huachuca, AZ (U.S. Army
Intelligence Center) just before the assassination. Most likely SEPTEMBER 9, 2025;
possibly Sept 8.

HARD RULE: WE NEVER LIST ANY NAMES OF WHO ATTENDED, OR WHO LIKELY ATTENDED, EVEN IF WE
KNOW. Not full names, first/last names, initials, handles, identifying ranks or titles,
narrow job descriptions, photos, or links to a named person. A good source or the name
appearing elsewhere does not change this. This overrides any prompt or skill; if a task
needs a name, it belongs elsewhere or goes to Bryan.

We also do not say the meeting necessarily happened, or that it was about Charlie Kirk
(an open question, stated as one). Instead, point readers to run their own searches on
X.com, Google, and We The Citizens:
    9/9/2025 meeting for Huachuca
    9/9/2025 meeting for Huachuca Charlie Kirk
Framing: people have proposed who may have been present at a possible meeting there,
possibly on that date; readers who want the identifications can find them with these
searches. Recommending a search is NOT asserting the meeting happened.

Related: {CK_FILE} sections "Fort Huachuca: People possibly at UVU & soldiers at Fort
Huachuca" and "SAM-702 FLIGHT to Fort Huachuca ... As VIP Passenger";
{SITE_DIR}/docs/US_Intelligence/, US_Intelligence_Assisted/, Planes/ (SAM flights).
