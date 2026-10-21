ROOT_DIR dir is ~/BGit/Bryan_git/charlie-kirk

THIS_DIR dir is {ROOT_DIR}/image_planning
IMAGES_DIR dir is {ROOT_DIR}/images
HIERARCHY_FILE is file {IMAGES_DIR}/images.yaml
  (Moved 2026-07-22 from {THIS_DIR}/hierarchy_images.yaml; that name and location are gone.)
GENERATOR_DIR dir is {THIS_DIR}/generator
INVENTORY_TSV is file {GENERATOR_DIR}/inventory.tsv

SITE_DIR dir is {ROOT_DIR}/site
DOCS_DIR dir is {SITE_DIR}/docs
HOME_PAGE is file {DOCS_DIR}/index.mdx
IMAGES_L2_PAGE is file {DOCS_DIR}/Photos/overview.mdx
PAGES_CSV is file {ROOT_DIR}/pages.csv
CK_FILE is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt
  (Real file; {ROOT_DIR}/Charlie_Kirk.txt is a symlink to it. Read the real path. READ-ONLY.)
CHARTER_FILE is file {THIS_DIR}/CLAUDE.md
EXCLUDE_FILE is file {THIS_DIR}/exclude_images.txt
BAN_IMAGES_CSV is file {IMAGES_DIR}/ban_images.csv

MIRROR_DIR dir is ~/_Mirror/Politics/Charlie_Kirk_Mi
MIRROR_SIDECAR_DIR dir is ~/BGit/Bryan_git/personal_large_files_bridge/_Mirror/Politics/Charlie_Kirk_Mi
REPO_SIDECAR_DIR dir is {ROOT_DIR}/.lfbridge

SIBLING VIDEO PIPELINE (read-only from here, never written):
VIDEO_PLANNING_DIR dir is {ROOT_DIR}/videos_planning
VIDEOS_DIR dir is {ROOT_DIR}/videos
VIDEO_HIERARCHY_FILE is file {VIDEOS_DIR}/videos.yaml
VIDEOS_L2_DIR dir is {DOCS_DIR}/Videos
FINDINGS_FILE is file {THIS_DIR}/findings_for_hierarchy.md

LFB_DIR dir is ~/BGit/Bryan_git/LargeFileBridge
LFB_PM_DIR dir is {LFB_DIR}/pm
COMPANY_BRIDGE_DIR dir is ~/BGit/act3/act3_large_files_bridge
PERSONAL_BRIDGE_DIR dir is ~/BGit/Bryan_git/personal_large_files_bridge

============================
GOAL
============================

Grow and improve {HIERARCHY_FILE}, the image evidence hierarchy YAML, into the most complete
hierarchy possible over the investigation's STILL IMAGE corpus (video is out of scope: read
MEDIA-TYPE SCOPE first). Each stage adds or enriches. Nothing is deleted (two carve-outs below).
No duplicates: an existing item gets its properties updated in place.

End state: one Level 5 page per image under the images Level 2 (today the Photos section,
{IMAGES_L2_PAGE}); the images landing page becomes mostly a TOC into Level 3 pages that come from
the YAML's level_3 nodes. This prompt builds the YAML ONLY: it creates/edits no Docusaurus page,
never touches sidebars.ts or {PAGES_CSV}. Stage 11 only RECORDS placements.

SCRIPTS (all under {GENERATOR_DIR}):
  update_hierarchy.py       Stages 3, 8, 9, 10 and the counts/integrity pass; emits via the shared emitter.
  plan_should_be.py plan    Stage 11: scores and selects should_be_on_pages.
  plan_should_be.py build   Stage 11: writes agent shortlist slices (optional judgment pass).
  plan_should_be.py write   Stage 11: merges agent rows back in.
  verify_stage_12_13.py     Stages 12 and 13, read-only, exit 1 on failure. Has its own INDEPENDENT
                            extractor (HTML tag parser, not the writer's regex).
  verify_on_pages.py        Third opinion on Stage 8 alone.

Run order: update_hierarchy.py -> plan_should_be.py plan -> verify_stage_12_13.py.
Back up the YAML first; each rewrites it in place.

Convergence priority (if context runs short, complete in this order):
  1. Stage 3 (CID + pin status; Stage 8 depends on it)  1b. Stage 3B (banned sync; cheap, gates 10 and 11, never skip)
  2. Stage 4  3. Stage 6  4. Stage 7  5. Stage 8  6. Stage 9  7. Stage 10  8. Stage 11
  9. Stage 5  10. Stage 12  11. Stage 13

============================
KNOWLEDGE — MEDIA-TYPE SCOPE: THIS PIPELINE IS IMAGES ONLY
============================

Earlier revisions told this pipeline to harvest video; that defect put playable video pages
under {DOCS_DIR}/Photos. Video belongs to the sibling pipeline, a full mirror of this one:

  images                                videos
  {THIS_DIR}                            {VIDEO_PLANNING_DIR}
  {HIERARCHY_FILE}                      {VIDEO_HIERARCHY_FILE}
  {DOCS_DIR}/Photos                     {VIDEOS_L2_DIR}
  Img_*.mdx leaf pages                  Vid_*.mdx leaf pages
  ck_image_sha256 frontmatter           ck_video_cid + ck_video_sha256
  gen_photos_pages.py                   gen_videos_pages.py
  served from static/img/evidence       played from a public IPFS gateway

THE RULE: a video never becomes an entry here (no `image:` or `video:` item at any level), never
gets an image_page, never gets a should_be_on_pages placement. This prompt never writes to
{VIDEO_HIERARCHY_FILE}, {VIDEOS_DIR}, {VIDEO_PLANNING_DIR} or {VIDEOS_L2_DIR} (reads freely).

TYPING (the YAML does not record media type, so decide at HARVEST time, Stage 7, never later):
  1. Extension on resolved src or file_path: .mp4 .mov .webm .m4v .mkv .avi = video; still-image ext = image.
  2. Extensionless src (IPFS case): CID inside <video>, <source>, or a markdown link ending in a video
     extension = video; CID inside <img> or ![]() = image.
  3. The video pipeline's records, PARSED BY FILENAME (never scrape CIDs wholesale; these are mixed):
       {VIDEOS_DIR}/manifest.yaml: take ipfs_cid only where the record's filename has a video extension.
       {ROOT_DIR}/IPFS/ipfs.txt: three-line blocks; use a block only when `ipfs add "<filename>"` names a video.
       {VIDEO_HIERARCHY_FILE}: NOT an oracle yet (still a schema shell of image entries) until populated.
     (Scraping all CIDs from these typed 70 entries as video when only 9 are.)
  4. Still undecided = UNKNOWN, not image. Report it, create nothing.

HAND-OFF: record each distinct video found (CID or path, page, enclosing tag), one line each, under
this heading in {FINDINGS_FILE}:
    == VIDEO REFERENCES — HAND-OFF TO videos_planning ==
Never write into {VIDEO_PLANNING_DIR}.

LEGACY CONTAMINATION (second carve-out from only-grows; on_pages is the first). As of 2026-07-23 the
file holds 53 `video:` items plus 9 `image:` items whose CID is an .mp4, all under level_4 _key
Narrative_Shot_in_the_Heart (they produced nine <video> players under
{DOCS_DIR}/Photos/Official_Narrative/Narrative_Shot_in_the_Heart/). Never add one, never enrich one
(Stages 3, 8, 9, 10, 11 skip them), never silently delete them: count, list, hand off, report in
every stage that touches entries. Removing them and un-publishing their pages is a separate,
explicitly-approved job, after the content lands under {VIDEOS_L2_DIR}.

============================
KNOWLEDGE — THE LEVEL MODEL (READ THIS FIRST)
============================

SITE levels: Level 1 = {HOME_PAGE}. Level 2 = directories directly under {DOCS_DIR} (TPUSA, FBI,
UVU, Israel, Mic, Planes, Timeline; Photos and Videos too). Level 3 = pages inside a Level 2
(overview plus analysis pages and first-level subdir overviews). Level 4 = one directory deeper.

YAML levels: no level_1 or level_2; the tree hangs under the images Level 2 and begins at level_3.

CORE MAPPING RULE, increment by one: site Level 2 -> YAML level_3; site Level 3 -> level_4; site
Level 4 -> level_5. The level_3 list is a SUPERSET of the site's Level 2s (minus the exclusions in
Stage 4). Each image on a site Level 3 page becomes an entry parented on the level_4 that correlates
to that page. Mirror-derived clusters already in the YAML stay; site-derived nodes merge INTO them.

============================
KNOWLEDGE — THE YAML FILE TODAY
============================

{HIERARCHY_FILE} is ~9,000 lines (~500KB). Read and learn from it before changing anything.
  * Root `level_3:` is an array; each item keyed `level_3:`; may hold a `level_4:` array, which may
    hold `level_5:`. Same shape at every depth.
  * Cluster node fields: title (spaces allowed), _key (underscores, four words or less, unique across
    the WHOLE file; the future page_key in {PAGES_CSV}), number_of_images (direct),
    number_of_images_recursive (subtree), optional needs_split: true (over 12), images (array).
    Plus site_level_2 (Stage 4) and site_page (Stage 6).
  * Image item fields: cid (IPFS CID, spoken "SID"), ipfs_pinned, sha256 (the identity; LFB
    fingerprint deferred), file_path (usually under {MIRROR_DIR}), ai_description (inline prose),
    ai_description_file / ocr_file / transcription_file (Stage 9), banned (Stage 3B), image_page
    (Stage 10), on_pages (Stage 8; supersedes old on_site_pages), should_be_on_pages (Stage 11),
    optional ipfs_url (IPFS-embed-only entries), optional also_filed_in (other mirror dirs holding the
    same sha256; deliberate cross-filing, kept).
  * Full property set, in emission order:

      images:
        - image:
            cid: "bafkreiabc...(CIDv1; "" only when the file is gone)"
            ipfs_pinned: false
            sha256: c51ef651e0e2fd9187ac8fa0b5d25908baba279b0c03f1ea93f6522fa3cedbb4
            file_path: "~/_Mirror/Politics/Charlie_Kirk_Mi/Censorship/G3o-JSJWUAA6XUC.jpeg"
            ai_description: "This image shows a wide-angle, daytime view of a crowded outdoor courtyard ..."
            ai_description_file: "~/BGit/Bryan_git/personal_large_files_bridge/_Mirror/Politics/Charlie_Kirk_Mi/Censorship/G3o-JSJWUAA6XUC.jpeg.ai_description"
            ocr_file: "~/BGit/Bryan_git/personal_large_files_bridge/_Mirror/Politics/Charlie_Kirk_Mi/Censorship/G3o-JSJWUAA6XUC.jpeg.ocr"
            transcription_file: ""
            banned: false
            image_page: "~/BGit/Bryan_git/charlie-kirk/site/docs/Photos/FBI/Img_Photo_c51ef6.mdx"
            on_pages:
              - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/FBI/overview.mdx"
              - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/Killer/israel-mossad.mdx"
            should_be_on_pages:
              - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/FBI/overview.mdx"
              - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/Killer/israel-mossad.mdx"
              - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/CoverUp/evidence-destruction.mdx"

    Every entry carries every property. Empty scalar = "" (never omitted, never null), so later passes
    can tell "not looked up" from "does not exist". Typed exceptions: on_pages / should_be_on_pages
    emit [] when empty; ipfs_pinned and banned emit false.
  * ~21 mirror-derived level_3 clusters exist (FBI, The Shot and the Shooter Position, Unfiled Backlog,
    Patsy Candidates, Security Team, TPUSA, Court and Legal Proceedings, Aircraft and Flight Evidence,
    Tyler Robinson, Memes and Commentary, Ballistics and the Gun, The UVU Venue, Charlie Kirk Himself,
    People of the Investigation, The Microphone, CIA and US Intelligence, Google Search Evidence, The
    Table Hand Off, Maps and Site Geometry, Israel and Mossad, The Truck and Back of Tent).
  * Prior art: {GENERATOR_DIR}/gen_hierarchy.js built the first pass from {INVENTORY_TSV} (sha256, dir,
    filename, orig_path, has_desc) plus clusters.json. Reuse its conventions: same sha256 in the SAME
    dir collapses; same sha256 in DIFFERENT concept dirs is deliberate (also_filed_in); its _key minting.

Cluster sizing ({CHARTER_FILE}): six images per page target, twelve ceiling; over twelve = not one
concept, mark needs_split: true and split one level deeper later. Concept clusters ("what is this
evidence about"), never by date or poster.

============================
KNOWLEDGE — THE BANNED PROPERTY (COPIED DOWN FROM {BAN_IMAGES_CSV})
============================

Every entry carries `banned:` as a real boolean (default false; true only because a ban row matches).

Banned is a PUBLISH-TIME GATE, not a delete. A banned image gets: no Level 5 page under
{DOCS_DIR}/Photos (an existing one is deleted by {THIS_DIR}/p_yaml_to_site.md, never by this prompt);
no served copy under the static evidence dir (STATIC_IMG_DIR in p_yaml_to_site.md; the image itself
is the payload); no placement or link anywhere on the site (no topic page, cluster page, TOC,
thumbnail, card); never pinned to IPFS (pinning is irreversible, so the gate holds BEFORE any pin).
Its entry stays in {HIERARCHY_FILE} forever: banning changes what is published, not what is known.

{BAN_IMAGES_CSV} is the MASTER; the repo charter ({ROOT_DIR}/claude.md, "Banned Media") owns the
contract; the YAML value is a downstream copy:
    ban_images.csv  ──▶  images.yaml (banned:)  ──▶  site/docs/Photos/ pages
Edit only the CSV; never hand-edit `banned:` (the next run overwrites it).

CSV FORMAT (header row, then one row per item):
  sha256        hex digest; PRIMARY identity (survives renames, moves, cross-filed copies)
  cid           IPFS CID if assigned, else empty. Secondary.
  file_path     full path from ~; last-resort match key, not authoritative
  banned        true or false. A false row is an explicit UN-BAN (kept as the record).
  reason        short plain-text reason. Required.
  date_added    YYYY-MM-DD

MATCH ORDER: sha256, then cid, then file_path. Any match sets banned to that row's value; no match =
false. sha256 matching bans EVERY cross-filed copy (file_path would ban one and publish the rest).

{EXCLUDE_FILE} (older one-sha256-per-line list) still counts. BAN SET = UNION of the two, minus any
CSV row marked banned=false. New bans go in the CSV; never delete lines from {EXCLUDE_FILE}.

Why: the mirror swept in private material (bank/health dashboards, booking confirmations, billing
portals, video calls with named faces; eleven were found published in the first full run) and
defamatory composites that burn an unproven accusation about a living person into the pixels.
When a run finds such material (private documents, unrelated third-party records, no connection to
the investigation, accusation burned in), add a CSV row with reason and date BEFORE the run ends and
note it in {FINDINGS_FILE}, or Stage 11 may plan it onto many pages.

============================
KNOWLEDGE — SIDECAR FILES (OCR, TRANSCRIPTION, AI DESCRIPTION) AND THE PATH MAPPING
============================

Large File Bridge ({LFB_DIR}; specs in {LFB_PM_DIR}) writes three sidecars per media file:
  .transcription = what was SAID; .ai_description = what is SEEN; .ocr = the literal on-screen text.
Naming: full filename kept, second extension appended: photo.jpg -> photo.jpg.ai_description,
photo.jpg.ocr; Blue_Side.mp4 -> Blue_Side.mp4.transcription.

Placement (authoritative: {LFB_PM_DIR}/artifact_placement_policy.mdx section 0, plus ai_description.mdx,
ocr.mdx, Transcribe.mdx, repo_tracking_scheme.mdx):
  * Original INSIDE a git repo: path-mirrored under that repo's .lfbridge/:
      {ROOT_DIR}/videos/X.mp4 -> {REPO_SIDECAR_DIR}/videos/X.mp4.transcription
    ({REPO_SIDECAR_DIR} holds videos/ and IPFS/videos/ sidecars.)
  * Original OUTSIDE any repo (the mirror): NO .lfbridge/ segment; the bridge repo (SDL) is the
    tracking area: {MIRROR_DIR}/Autopsy/X.jpg -> {MIRROR_SIDECAR_DIR}/Autopsy/X.jpg.ai_description
    Personal SDL: {PERSONAL_BRIDGE_DIR}   Company SDL: {COMPANY_BRIDGE_DIR}
  * Older files may still be under a .lfbridge/_Mirror/ path. Check both before calling it missing.
Coverage is high now (~1,978 .ai_description, ~1,795 .ocr, ~331 .transcription at writing; recount).

Every IMAGE entry gets ai_description_file / ocr_file / transcription_file = sidecar path or "".
The inline ai_description stays as short prose. Legacy video entries get no sidecar properties.

============================
KNOWLEDGE — THE SITE'S LEVEL 2 SECTIONS
============================

Enumerate live (ls {DOCS_DIR}); ~70 dirs (After, Before, FBI, Gun_Bullet, Israel, Mic, Photos,
Planes, Topics3, TPUSA, UVU, Videos, ...). {PAGES_CSV} is the master page index (page_key,
parent_key, level, url_path, file_path, title, ...); use it with the filesystem walk. When they
disagree, the filesystem is what exists.

============================
STAGE 1 — SETUP AND READ
============================

* Read {CHARTER_FILE} (authority on audience, levels, schema, hard rules).
* Read {HIERARCHY_FILE} fully; index every _key, node path, sha256 and the node(s) it lives under.
* Read {GENERATOR_DIR}/gen_hierarchy.js, clusters.json, and the header of {INVENTORY_TSV}.
* Read {PAGES_CSV}.
* Read {BAN_IMAGES_CSV} (create it with header sha256,cid,file_path,banned,reason,date_added and no
  rows if missing) and {EXCLUDE_FILE}. Report both counts.
* Enumerate {DOCS_DIR} top-level dirs.
* Consult {CK_FILE} by section when a clustering or parenting decision needs arbitration (do not read
  all 400K+ lines up front). The hierarchy mirrors the investigation's real concepts.

Output to stdout:
============================
STAGE 1 COMPLETE
YAML nodes indexed: N level_3 / N level_4 / N level_5
Images indexed: N unique sha256
Site Level 2 dirs found: N
ban_images.csv ready: yes    rows: N (N banned=true, N un-bans)
exclude_images.txt: N sha256 values
pages.csv rows: N
============================

============================
STAGE 2 — LEARN THE SIDECAR MAPPING (VERIFY, DON'T ASSUME)
============================

* Read the five LFB specs above (frontmatter description plus placement sections are enough).
* Verify the mapping on disk: 5 sample images under {MIRROR_DIR} against {MIRROR_SIDECAR_DIR}, and one
  repo file under {VIDEOS_DIR} against {REPO_SIDECAR_DIR} (verification only; never add it to the YAML).
  Check the legacy .lfbridge/_Mirror/ location before concluding a sample is missing.
* Count .ai_description, .ocr, .transcription files under {MIRROR_SIDECAR_DIR}.

Output to stdout:
============================
STAGE 2 COMPLETE
Mapping verified: N/5 mirror samples, repo sample yes/no
Sidecar counts: ai_description N, ocr N, transcription N
============================

============================
STAGE 3 — CID: EVERY IMAGE GETS ITS IPFS CID AND PIN STATUS
============================

Runs before the page sweeps because pages embed images by IPFS gateway URL as well as by static file,
and Stage 8 must recognise a CID-only reference.

A CID is computed from the bytes; no network or daemon needed:
    ipfs add -n -Q "<file>"          # -n only-hash, -Q print just the CID
USE THE DEFAULT CIDv0 ("Qm...") — what the site embeds and the local pin set holds. --cid-version=1
gives a different string (codec changes too) and Stage 8 would resolve nothing. If v1 is needed for a
dweb.link URL, convert at use time with `ipfs cid base32 <cid>`; never store it. Always the same flags
(-n -Q, default chunker, CIDv0) or CIDs won't match gateway URLs.

Pinned = this node holds and serves the blocks; separate from having a CID:
    ipfs pin ls --type=all <cid>       # exit 0 and prints the cid = pinned
    ipfs block stat <cid>              # blocks present locally

* For every IMAGE entry whose file_path exists on disk (skip legacy video): compute the CID and write
  `cid` (unconditional; a readable file never keeps cid ""); record ipfs_pinned true/false.
* NEVER pin in this stage (irreversible publication). Pinning the publishable set is a separate,
  explicitly-approved job that first filters out the whole ban set.
* ipfs_url-only entries: parse the CID from the URL; ipfs_pinned from the local node (false if absent).
* file_path missing on disk: leave cid "", report it, never invent one.
* Build a CID -> sha256 index for Stage 8.
* Never overwrite a non-empty cid with "". A mismatch with the recomputed CID means the bytes changed:
  report it, keep the recomputed value, note the old one.
* Script it (~1,700 entries); batch `ipfs add -n`, cache by sha256 (cross-filed copies share one CID).

Output to stdout:
============================
STAGE 3 COMPLETE
Entries with local file: N   CID computed: N   CID already present + matching: N
CID mismatches (bytes changed): N (listed)
Pinned on local node: N   Not pinned: N
ipfs_url-only entries with CID parsed from URL: N
Entries left cid "" (file missing on disk): N (listed)
Nothing pinned by this stage: confirmed
============================

============================
STAGE 3B — BANNED: SYNC THE BAN SET ONTO EVERY ENTRY
============================

The ONLY stage that writes `banned:`. It copies a decision already made; it reasons about nothing.
Run every run right after Stage 3, and again whenever the CSV changes (cheap, idempotent).

STEP 1 — READ THE BAN SET.
  * Parse {BAN_IMAGES_CSV} with the python3 csv module (reason contains commas and quotes). Expected
    header: sha256,cid,file_path,banned,reason,date_added. Missing file: create it with the header
    (missing means "nothing banned", not "skip the gate").
  * banned column strictly: "true"/"false" any case. Anything else = malformed: STOP and report
    (guessing false publishes banned material).
  * Build lookups by sha256, cid, and expanded file_path (expand ~ on both sides).
  * Every sha256 in {EXCLUDE_FILE} joins as banned=true unless a CSV row for it says false (CSV un-ban wins).

STEP 2 — SET banned ON EVERY ENTRY, at every depth: sha256, then cid, then file_path; first match
  wins; no match = false. Write the key on EVERY entry (never omit, never null). A banned sha256 bans
  every cross-filed copy: print entries banned and distinct sha256 banned; equal counts on a
  cross-filing corpus means the walk missed duplicates. Never delete a banned entry.

STEP 3 — REPORT CSV ROWS MATCHING NOTHING, with reason text (usually: stale identity because the file
  was re-encoded; a video filed in the wrong CSV, so check {VIDEOS_DIR}/ban_videos.csv; or a
  legitimate pre-emptive row). Never delete them.

STEP 4 — RE-EMIT through the shared emitter (emit_node/recount from {GENERATOR_DIR}/bind_image_pages.py,
  byte-for-byte round-trip): no banned change = byte-identical file. Verify it parses. Apply OUTPUT
  SANITIZATION (treat the human-typed reason column as untrusted).

DO NOT here: delete/edit any page or served static copy (p_yaml_to_site.md's job); clear image_page,
on_pages or should_be_on_pages (on_pages is the observation telling the page prompt what to remove;
Stages 10 and 11 handle the rest); touch IPFS.

Output to stdout:
============================
STAGE 3B COMPLETE
{BAN_IMAGES_CSV}: N rows (N banned=true, N banned=false un-bans)
{EXCLUDE_FILE}: N sha256 values
Entries marked banned: true : N   across N distinct sha256 (cross-filed copies caught)
  (by sha256: N, by cid: N, by file_path: N)
Entries marked banned: false: N
Every entry carries the banned key: yes
CSV rows matching no entry: N   (listed with reason)
YAML parses: yes    Byte-identical when nothing changed: yes/no
============================

============================
STAGE 4 — SITE LEVEL 2 SWEEP → YAML LEVEL_3 SUPERSET
============================

The level_3 list must include ALL site Level 2 sections except: Photos and Videos (media Level 2s),
Topics3 (template scaffolding; /Topics3/Photos is unrelated), unfiltered/queue/catch-all categories
(but include ONE "Other" level_3 and fold other_topics-style catch-alls into it), and non-page files
at the docs root (index.mdx, Topics.mdx, image_list.csv, video_list.csv, index.html).

For each remaining site Level 2:
* Match an existing level_3 by _key, title and MEANING (TPUSA covers TPUSA; "The UVU Venue" covers UVU;
  "Ballistics and the Gun" covers Gun_Bullet; "Aircraft and Flight Evidence" covers Planes; "CIA and
  US Intelligence" covers intelligence / US_Intelligence; "Court and Legal Proceedings" covers court /
  Legal / legal_investigation). Never a second name for the same concept.
* Record the mapping as site_level_2 on EVERY level_3 (list; [] for mirror-only nodes).
* Uncovered: append a level_3 (title from the section name, unique _key, number_of_images: 0,
  number_of_images_recursive: 0, images: [], site_level_2: [<dirname>]).
* Never remove or rename a level_3; update in place.

Output to stdout:
============================
STAGE 4 COMPLETE
Site Level 2s swept: N
Matched to existing level_3: N
New level_3 nodes added: N (list their _keys)
Excluded: Photos, Videos, Topics3, non-page files
Other node present: yes
============================

============================
STAGE 5 — HOME PAGE TABLES OF CONTENTS → MORE LEVEL_3S
============================

{HOME_PAGE} carries several TOCs: the three-column flex divs under "Biggest Question Marks",
"## Table of Contents", "## Areas of Investigation", "Related Areas"/"Related", and per-thesis link
clusters (Tyler Robinson Not Assassin, Cause of Death, Mossad / Israel Top Suspect, US Intelligence
Assisted, ...). They surface concepts the directory sweep misses; this stage is expected to ADD nodes.
* Read it fully; extract EVERY TOC and link cluster; resolve each target to its site section.
* Add a level_3 (Stage 4 rules) for each concept not covered. Covered ones are skipped, though you may
  append to site_level_2 or refine the title if the TOC gives a better name.

Output to stdout:
============================
STAGE 5 COMPLETE
TOC sections parsed on home page: N
Concepts found: N
Already covered: N
New level_3 nodes added: N (list their _keys)
============================

============================
STAGE 6 — FILESYSTEM LEVEL 3/4 PAGES → YAML LEVEL_4/LEVEL_5 NODES
============================

For every site Level 2 mapped to a level_3 (via site_level_2):
* Enumerate its Level 3 pages (overview plus every page file in the dir plus first-level subdir
  overviews; {PAGES_CSV} levels guide, filesystem checks).
* Each site Level 3 page -> a level_4 under the right level_3: title (frontmatter title or first H1),
  _key (unique, four words max; prefer the page_key from {PAGES_CSV} when free), site_page: <repo-relative
  path>, number_of_images, number_of_images_recursive, images: [].
* Each site Level 4 page -> a level_5 under the right level_4, same fields.
* Skip pure-navigation pages only when they would create an empty duplicate of their parent; when in
  doubt, include.
* A site page that is the same concept as an existing mirror node: MERGE (keep the node, add site_page).
* Grow and update only.

Output to stdout:
============================
STAGE 6 COMPLETE
Site Level 3 pages processed: N → level_4 nodes (N new, N merged)
Site Level 4 pages processed: N → level_5 nodes (N new, N merged)
============================

============================
STAGE 7 — PAGE IMAGE SWEEP → IMAGE ENTRIES IN THE YAML
============================

Every page with images gets those images represented in the YAML.
* Scan every page under {DOCS_DIR} for markdown images, <img>, <iframe>/<video>/<source>, and
  static-asset links, using the SAME multi-line-aware extractor as Stage 8. Served /img/... maps to
  {SITE_DIR}/internals/static/img/... ({SITE_DIR}/static/ does not exist).
* TYPE EVERY REFERENCE FIRST (MEDIA-TYPE SCOPE). Video and UNKNOWN: no entry; count and hand off to
  {FINDINGS_FILE}. Video tags are matched so the type test can see them, not to harvest them.
* Out of scope: {DOCS_DIR}/Photos, {VIDEOS_L2_DIR}, {DOCS_DIR}/Topics3. {DOCS_DIR}/video_list.csv is the
  video pipeline's index, not a source here.
* SITE-ONLY ASSETS (no mirror original; e.g. All_Laws.jpeg, Timeline_Israel.jpeg, Iran_Timeline.jpeg,
  court/mirandize/*.png under {SITE_DIR}/internals/static/) are real evidence: create an entry (sha256
  the static file, file_path = its tilde path, cid per Stage 3) under the node matching the page.
* For each still image: sha256 it; match to a mirror original by sha256 (against {INVENTORY_TSV} and
  existing entries), then by filename. Mirror original is the preferred file_path, else the static path.
    * sha256 already in the YAML: no duplicate; update properties and add the page to on_pages
      (shape per Stage 8).
    * New: add under the level_4 (or level_5) correlating to the page: cid, ipfs_pinned, sha256,
      file_path, ai_description: "", on_pages: [{page: <tilde path>}], should_be_on_pages: [], sidecar
      fields (Stage 9) and image_page: "" (Stage 10).
* Inline embeds on topic pages stay where they are; this hierarchy is an index, not a relocation.

Output to stdout:
============================
STAGE 7 COMPLETE
Pages scanned: N
Images found on pages: N (N matched to mirror originals)
New image entries added: N
Existing entries updated (on_pages): N
Video references found: N (0 entries created — handed off to findings)
Unknown-type references: N (0 entries created — handed off to findings)
============================

============================
STAGE 8 — ON_PAGES: WHERE ELSE IN THE REPO EACH IMAGE IS SHOWN
============================

Three properties, never confused:
  image_page          which page IS this image: its one Level 5 page under {DOCS_DIR}/Photos (Stage 10).
  on_pages            where ELSE it is shown TODAY: every other page in the repo embedding it, OBSERVED
                      from file contents (here). Covers any page outside the images Level 2.
  should_be_on_pages  where it SHOULD be shown: REASONED plan (Stage 11); superset of on_pages; the
                      difference is the publishing work still to do.

SHAPE: a list of mappings with one `page:` key holding the tilde-rooted path (not flat strings, not
repo-relative, not URLs); [] when none:
    on_pages:
      - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/FBI/overview.mdx"

ON_PAGES IS OBSERVED, NEVER INFERRED. The only way to earn a binding: read page P and find a
reference that resolves to the image. Never from shared topic, the image's cluster site_level_2 /
site_page, a person in the image being the page subject, carrying a value forward unread, or any
judgment. Deciding whether an image belongs on a page is Stage 11.

LESSONS (measured 2026-07-23; reproduce as the regression test):
  * Ground truth then: 123 refs on 41 non-Photos pages; 102 resolve (76 by CID, 40 by evidence filename);
    34 pages legitimately show a corpus image; 7 site-only assets. The file held 1,056 bindings on 99
    pages, 946 (89%) on pages with no image reference: imported from the old topically-guessed
    on_site_pages. Most [] lists are CORRECT. The job is rebuild from observation and delete every
    unsupported binding, not "fill the empties".
  * The fabrication survived in update_hierarchy.py as a union (recover_on_pages()):
        merged = set(existing_pages.get(id(inner), set()))   # prior values
        merged |= sweep_pages.get(sha, set())                # observed values
    That re-adopts every fabricated binding forever. Correct shape is assignment:
        observed = sweep_pages.get(sha, set())
        for p in sorted(prior - observed):
            report_removal(p, sha, reason)
        inner['on_pages'] = [{'page': p} for p in sorted(observed)]
  * on_site_pages (old flat list) values are HINTS only: one earns on_pages only by re-reading the page.
    After this stage on_site_pages must not appear anywhere in the file.

THE ONE PLACE THIS PROMPT DELETES DATA: rebuild on_pages from ground truth every run (a false binding
misleads Stage 11, which unions on_pages into should_be_on_pages). Report every removed binding (page,
sha256, reason: no such reference / page missing). Only on_pages; nothing else. If fewer than 80
resolvable references are found site-wide, the extractor is broken: do NOT write, fail, fix it.

HOW TO FIND REFERENCES — one linear pass (reverse index), each file read once:
* Every text file under {ROOT_DIR} (.md .mdx .html .tsx .jsx .ts .js .json .csv .yaml; include blog and
  React components), skipping node_modules/, build/, .git/, and {SITE_DIR}/internals/static/ binaries.
* MULTI-LINE AWARE. The dominant form splits the tag across lines inside an anchor:
      <a href="/Photos/People/People_tyler_bowyer/Img_Photo_3caf21"><img
        src="https://ipfs.io/ipfs/QmVA7WhYwAvFXe7rjdrgrRwdCJpprLG39vrS3Xp8PK2otq"
        alt="Screenshot of a February 2022 exchange ..."
        style={{width: '100%', height: 'auto', aspectRatio: '1320/1297'}}
      /></a>
  A line pattern like `<img[^>]*src="[^"]+` misses 72%. Use:
      tags = re.findall(r'<img\b.*?>', text, re.S)
      src  = re.search(r'src=["\']([^"\']+)["\']', tag)
  Test any regex against a known multi-line page first. No grep-based extraction.
* Forms seen (share of 123): 76 ipfs.io/ipfs/<CID> (62%); 40 /img/evidence/<sha256>.jpg (33%); 7 site-only
  /img/<name>.jpeg and /court/mirandize/<name>.png (5%). Also handle: markdown ![alt](src), require()/import
  src, background-image / style url(), https://<CID>.ipfs.dweb.link/, ipfs://<CID>, <video>/<source>/<iframe>
  src and poster. Video refs are typed and skipped; a <video> poster is a still image and IS eligible.
  Count every form; an unknown form is a reported unresolved reference, never silently dropped (hard-fail).
* PATH FACTS: /img/... = {SITE_DIR}/internals/static/img/... . {SITE_DIR}/internals/static/img/evidence/
  holds ~1,453 files named <full lowercase 64-hex sha256>.<ext> (verified), so resolve by exact name
  match on all 64 chars, no hashing.
* Resolve to an entry, in order:
    1. CID -> Stage 3 cid index (62% of refs). If that index is empty, STOP. Normalise both sides with
       `ipfs cid base32` (a page may carry v1 of a stored v0).
    2. Evidence filename -> 64-hex basename = sha256. Exact.
    3. Other local static file -> sha256 it. Exact.
    4. Basename vs file_path basenames: AMBIGUOUS; accept only a unique match, else residual + report.
* Append the page's tilde path; dedupe; sort each list. stat() every page path before writing; remove and
  report vanished pages.

UNRESOLVED REFERENCES ARE A FINDING. The 7 site-only refs known (Fix/overview.mdx and
laws/explain/all/overview.mdx -> /img/All_Laws.jpeg; Iran/overview.mdx -> /img/Iran_Timeline.jpeg;
Timeline/overview.mdx and Israel/overview.mdx -> /img/Timeline_Israel.jpeg;
court/mirandize/mirandized-sept-11-image.mdx -> /court/mirandize/Mirandized_Sept_11_.png;
court/mirandize/sept-11-grok-image.mdx -> /court/mirandize/Sept_11_Grok.png) get entries via Stage 7's
site-only rule, then bind here.

SCOPE — never in on_pages: pages under {DOCS_DIR}/Photos (~1,600 of their own <img>; thousands of
bindings means the filter leaks; check whether paths carry a leading ./ and assert zero recorded paths
contain /docs/Photos/); files in {THIS_DIR}, {GENERATOR_DIR}, {HIERARCHY_FILE}, {PAGES_CSV}; anything
outside {ROOT_DIR}.

SANITY GATES (all before writing; fail on any breach):
  1. Calibration: count non-Photos refs and record it. History: 6, 75, 83, 123, then 318 refs on 120 pages
     (2026-07-23 evening, the multi-line extractor plus markdown forms), giving 176 bindings on 148 entries.
     Nothing is ever removed from the site, so substantially FEWER than last time = broken extractor.
  2. `grep -l '<img'` over non-Photos docs: the extractor must find a ref on EVERY listed page.
  3. Re-verify every binding by reopening the page (drop and count failures). This alone catches fabrication.
  4. Zero paths under /docs/Photos/, zero non-existent paths, zero duplicates within an entry.
  5. Bindings within the same order of magnitude as resolvable refs.

PARALLELISM: one script does the mechanical sweep in seconds (~1,500 non-Photos pages). Agents only for
the RESIDUAL (ambiguous basenames, relative paths, component indirection, hand-written embeds):
partition whole directories across 12 agents (never split a dir; balance by file count). Each returns
(page_path, resolved_sha256_or_cid, verbatim_matched_text) rows; the verbatim text is mandatory and is
re-checked against the page (rows without it are rejected and counted). Agents never edit the YAML; one
writer merges script plus agent output in a single write.

Output to stdout:
============================
STAGE 8 COMPLETE
Files read: N   Image references found: N (multi-line aware)
Pages with at least one <img> (naive grep): N   pages the extractor found refs on: N   (must be equal)
Reference forms seen: ipfs-CID N, evidence-filename N, other-static N, markdown N, other N
Resolved by CID: N   by evidence filename: N   by sha256: N   by basename: N
Unresolved references: N (listed with page + reference; each is a Stage 7 site-only-asset candidate)
Entries with on_pages non-empty: N   total page bindings: N
Bindings verified by reopening the page: N/N
Bindings REMOVED as unsupported: N (listed: page + sha256 + reason)
Recorded pages that no longer exist on disk: N (listed, removed)
Photos-scope leaks blocked: N   paths under /docs/Photos in output: 0
on_site_pages remaining in file: 0
Extractor calibration: N refs this run vs N last run (site only grows — a drop is a bug)
============================

============================
STAGE 9 — SIDECAR FILE-PATH PROPERTIES ON EVERY IMAGE
============================

For EVERY image entry (skip and count legacy video):
* Expected paths per Stage 2: mirror original -> {MIRROR_SIDECAR_DIR}/<same rel path>/<name.ext>.<sidecar>;
  original inside {ROOT_DIR} -> {REPO_SIDECAR_DIR}/<repo rel path>/<name.ext>.<sidecar>; legacy
  .lfbridge/_Mirror/ as fallback.
* Set ai_description_file, ocr_file, transcription_file = path if the file exists, else "".
* Empty inline ai_description + existing .ai_description sidecar: fill it with the sidecar's Overview
  paragraph collapsed to one paragraph (readDesc() in gen_hierarchy.js). Never overwrite a non-empty one.

Output to stdout:
============================
STAGE 9 COMPLETE
Entries processed: N
ai_description_file set: N   ocr_file set: N   transcription_file set: N
Inline descriptions filled from sidecars: N
Entries with no sidecars at all: N
Legacy video entries skipped: N
============================

============================
STAGE 10 — IMAGE_PAGE: BIND EVERY IMAGE TO ITS LEVEL 5 PAGE
============================

The IMAGE PAGE (Level 5) hosts one image with title and descriptive prose:
  Photos (Level 2) > Maps (Level 3 cluster overview) > Img_Photo_cf0c99.mdx (image page)
~1,100+ exist, generated by {GENERATOR_DIR}/gen_photos_pages.py. This stage only READS them.

image_page = tilde-rooted path to that page, e.g.
    image_page: "~/BGit/Bryan_git/charlie-kirk/site/docs/Photos/Maps/Img_Photo_cf0c99.mdx"
or "" when no page exists (key always present).

MATCHING via frontmatter:
    ck_image_sha256: cf0c994cfd5c6ba50dd08f272f073ceddb0471dcfa7130bf511e874cfa2a5bac
    ck_node_key: Maps
  * Index every .mdx under {DOCS_DIR}/Photos declaring ck_image_sha256 by (ck_image_sha256, ck_node_key).
  * Look up (entry sha256, enclosing node _key): exact match (makes cross-filed copies each bind their own page).
  * Else sha256 alone: one page = use it; several = nearest ck_node_key in the tree (same parent, then same
    level_3 subtree). None = "".
  * Pages without ck_image_sha256: never guess by filename; count and report.

RULES:
  * Set on EVERY image entry.
  * Legacy video entry: "", counted, reported (its page belongs in {VIDEO_HIERARCHY_FILE}'s video_page).
  * A Photos page containing <video>/<source> is a video page in the wrong hierarchy: bind nothing, list it
    under the hand-off heading in {FINDINGS_FILE}, report the count (nine today, all under
    {DOCS_DIR}/Photos/Official_Narrative/Narrative_Shot_in_the_Heart/).
  * Never invent a path; verify existence at write time, else "". Never a path outside {DOCS_DIR}/Photos
    (topic-page embeds are on_pages).
  * image_page is an IDENTITY field (OUTPUT SANITIZATION): non-ASCII emitted as visible \uXXXX escapes.
  * Never clear a non-empty image_page to ""; if the page vanished, report it.
  * BANNED ENTRY: image_page "" always (clearing is correct here). If a page carrying its sha256 exists, do
    not bind or delete it: write "", REPORT loudly with page path, served-copy path and ban reason, so
    p_yaml_to_site.md removes both. Count separately; non-zero means banned material is live.

Output to stdout:
============================
STAGE 10 COMPLETE
Image pages indexed under Photos: N (N with ck_image_sha256, N without)
Entries with image_page set: N   matched by (sha256,node): N   by sha256 only: N
Entries with image_page "": N (no page exists yet)
Banned entries skipped: N   of those, LIVE PAGES FOUND NEEDING DELETION: N
  (each listed with page path, served-copy path, and ban reason)
Recorded pages now missing from disk: N (listed)
============================

============================
STAGE 11 — SHOULD_BE_ON_PAGES: WHERE EACH IMAGE OUGHT TO APPEAR
============================

The one REASONED property. Most images appear only on their own Level 5 page; a reader in the
Ballistics or Spy Plane section should see that topic's evidence on the page they are reading. This is
the worklist a later publishing prompt consumes.

should_be_on_pages ⊇ on_pages: it is the complete desired state (repeat every on_pages page unless it was
a wrong placement). Stage 8 must run first and be clean (unioning fabricated bindings creates fabricated
publishing instructions): confirm Stage 8 reported zero unverified bindings, or, if it did not run this
session, re-verify each on_pages entry by reopening the page.

ELIGIBLE: still images only. Legacy video entries get no new placement; existing placements on them
(the 9 mistyped .mp4 `image:` entries each carry one) are reported, not acted on.

SHAPE: identical to on_pages (list of `- page:` tilde paths; [] when none).

EVERY PATH MUST BE REAL, FULL, AND VERIFIED — NO PLACEHOLDERS.
  * Hard failures if they reach the file:
      - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/....mdx"
      - page: ".../site/docs/FBI/overview.mdx"
      - page: "site/docs/FBI/overview.mdx"            (repo-relative)
      - page: "/FBI/overview"                          (a URL path)
      - page: "~/.../charlie-kirk/site/docs/FBI/coverup.mdx"  (invented file)
    Any value with "...", "TODO", "TBD", "<", ">" or another placeholder, or not an absolute tilde path
    ending .md/.mdx, is invalid.
  * THE ONLY LEGAL WAY TO PRODUCE A VALUE — build a candidate index once and select from it:
      1. {PAGES_CSV} file_path (repo-relative) expanded to {ROOT_DIR}/<file_path> in tilde form.
      2. Union a walk of every .md/.mdx under {DOCS_DIR} (the CSV can lag).
      3. stat() every candidate; drop non-existent. That set, keyed by tilde path, is THE index.
      4. Every value written is an index key byte for byte; no code path constructs a string.
  * VERIFY BEFORE AND AFTER WRITE: re-stat every path before emitting; after emitting, re-parse, expanduser,
    stat again. Any miss FAILS the stage (no partial file, no degrading to ""). Fix and re-emit.
  * Right page does not exist: record under "Wanted pages that do not exist" (sha256 + suggested title);
    write only real pages.

DECISION INPUTS, by weight:
  1. The .ai_description (SEEN) and .ocr (SAYS) sidecar files, not just the inline prose; OCR names people,
     dates, tail numbers, case numbers, headlines.
  2. The node the image sits under (_key, title, site_level_2 / site_page): usually the strongest and
     cheapest signal (an image under the level_4 whose site_page is site/docs/Planes/N1098L.mdx almost
     certainly belongs there).
  3. The mirror directory of the original.
  4. {PAGES_CSV} title, description (best cheap matcher), page_type (person pages need the image to DEPICT
     the person), level, level2_section, url_path.
  5. {CK_FILE} arbitrates description vs cluster.

TARGETING: Level 3 pages mainly (Level 4 equally good when the concept lives there). Level 2 overviews only
for an emblematic headline image (at most one or two per overview). NEVER under {DOCS_DIR}/Photos, nor
{THIS_DIR}, {GENERATOR_DIR}, {HIERARCHY_FILE}, {PAGES_CSV}, outside {ROOT_DIR}, or Topics3 scaffolding.

QUANTITY: one to three pages per image normal, five ceiling (a "fits ten pages" image is generic: give
the one or two where it is evidence). [] is common and correct; never pad. Per-page load max 12 across
the corpus: keep the strongest 12, report overflow under "Wanted pages that do not exist".

DEFAMATION GATE:
  * banned: true -> should_be_on_pages: [] unconditionally; filter before scoring; clear any prior pages
    and report each. Do NOT union its on_pages (those are pages it must be REMOVED from): report a banned
    entry with non-empty on_pages as a REMOVAL WORKLIST (page + ban reason), leave on_pages untouched.
    Nothing links into a banned image anywhere.
  * Same for any sha256 in {EXCLUDE_FILE} (ban set = CSV union EXCLUDE minus CSV un-bans).
  * An image of a named living person goes only where that person's presence is the point. Never assign an
    image whose content (incl. OCR) accuses a living person; those stay private until cropped.
  * Unsure: leave it out and note it.

ACCEPTANCE TARGETS (measure over ALL entries after the write; print the table; retune, don't ship, on a miss):
    should_be_on_pages empty []              >= 5%   and <= 15%
    should_be_on_pages with >= 1 page        >= 85%
    should_be_on_pages with >= 2 pages       >= 20%
    should_be_on_pages with >= 3 pages       >= 20%
    on_pages empty []                        < 100%  (all-empty means broken)
  The empty floor matters: assigning everything means it stopped discriminating. on_pages is observed
  (~90% empty legitimately) and is only a liveness check; never tune it. Run of 2026-07-23 landed at
  11.6% / 88.4% / 58.0% / 36.5%, on_pages 91.5% empty.

HOW TO RUN:
  * Candidate index and mechanical filters (ban set, Photos exclusion, per-page load) are scripted.
  * Selection is scripted: {GENERATOR_DIR}/plan_should_be.py plan scores every image against every
    candidate (sidecar description + OCR + cluster + mirror dir vs page title, description, url path,
    section). Reproducible and auditable.
  * Scoring rules learned the hard way (do not drop):
      - drop bare digit runs from tokens (OCR'd flight lists / trends charts are mostly numbers that win on IDF).
      - sublinear tf (1 + log tf) on the image side (a repeated airport code outranked the real subject).
      - title-match bonus: a distinctive token (idf >= 4) shared with the page TITLE is the strongest signal.
      - structural prior PROPORTIONAL to the entry's best score (0.75x nearest ancestor's site_page, 0.35x
        further ancestors); a flat bonus is noise next to cosine scores of 20-40.
      - person gate: page_type=person needs the WHOLE name present (Blake_Harruff otherwise admits blake-neff).
      - selection cutoff: keep candidates >= 0.74 of the entry's best (CK_REL_KEEP overrides). Tune this knob,
        and only this knob, to land the targets.
  * Measured precision ~65-70% (hand audit of 20). Exact on named people, tail numbers, case numbers,
    documents; weak on generic geography (a map described only as "Orem, Utah, Utah Lake").
  * OPTIONAL JUDGMENT PASS: `plan_should_be.py build` writes 12 shortlist slices to /tmp/ck_stage11 (each
    entry with description, OCR, ~12 scored candidates). 12 parallel agents return (sha256, node_key,
    selected_index_key, confidence, one-line reason) choosing EXISTING index keys; a path not in the index
    is REJECTED and counted. Agents never edit the YAML; `plan_should_be.py write` is the single writer.
    ASK FIRST: twelve agents over ~1,700 entries costs real money.
  * The writer applies quantity and defamation rules, unions on_pages, dedupes, sorts, re-stats, writes once.

RULES: key on EVERY entry ([] when empty, never "" or missing). Grow, do not clobber: merge an existing
non-empty list with this run's selections; remove a page only when it no longer exists, and report it.
Page values are IDENTITY fields (\uXXXX escapes).

Output to stdout:
============================
STAGE 11 COMPLETE
Candidate index: N pages (N from pages.csv, N from filesystem walk, N dropped as non-existent)
Image entries processed: N
Entries with should_be_on_pages non-empty: N   total page assignments: N
Assignments carried over from on_pages: N   new assignments proposed: N
Entries left [] : N (N banned, N excluded by {EXCLUDE_FILE}, N no topical match)
Banned entries with a non-empty on_pages — REMOVAL WORKLIST: N (listed with page + reason)
Banned entries whose should_be_on_pages was cleared this run: N (listed)
Level 2 overview assignments: N   Level 3: N   Level 4: N
Agent rows rejected (path not in candidate index): N
Pages over the 12-image load: N (listed with overflow counts)
Wanted pages that do not exist: N (listed: suggested title + image sha256)
Path validation: N/N resolve to an existing file on disk — placeholders found: 0
============================

============================
OUTPUT SANITIZATION — NO INVISIBLE UNICODE, EVER (SECURITY RULE)
============================

The emitted {HIERARCHY_FILE} must contain no invisible Unicode (they hide content, spoof strings, smuggle
instructions). The invisible set includes at minimum: U+0000-U+0008, U+000B-U+001F, U+007F-U+009F, U+00A0,
U+00AD, U+034F, U+061C, U+115F, U+1160, U+17B4, U+17B5, U+180B-U+180E, U+2000-U+200F, U+2028-U+202F
(U+202F NARROW NO-BREAK SPACE is what macOS puts before "AM/PM" in screenshot filenames; it WILL appear),
U+205F-U+206F, U+3000, U+3164, U+FE00-U+FE0F, U+FEFF, U+FFA0, U+FFF9-U+FFFB, U+E0000-U+E007F.

  * PROSE fields (title, ai_description): replace space-like invisibles (U+00A0, U+2000-U+200A, U+202F,
    U+205F, U+3000) with a space, DELETE zero-width/bidi/control/joiner chars, collapse whitespace. Visible
    non-ASCII (em dashes, accents) may stay.
  * IDENTITY fields (file_path, ai_description_file, ocr_file, transcription_file, image_page, ipfs_url,
    on_pages and should_be_on_pages page values, cid, also_filed_in, site_page, site_level_2): must still
    match the real file, so emit ALL non-ASCII as visible escapes in YAML double-quoted scalars (U+202F
    becomes the six characters " "). Parsed value unchanged.

MANDATORY after every emit: re-scan the file and hard-fail on any invisible code point; re-parse and
spot-check that an escaped file_path still resolves on disk.

============================
STAGE 12 — COUNTS, NEEDS_SPLIT, INTEGRITY
============================

* Recompute number_of_images and number_of_images_recursive on every node.
* needs_split: true when over 12 direct images; remove the flag at 12 or under.
* Every _key unique file-wide. No sha256 twice within one node (across nodes is cross-filing; keep
  also_filed_in accurate).
* YAML parses: python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" {HIERARCHY_FILE}
* Every image entry has the full property set (cid, ipfs_pinned, sha256, file_path, ai_description,
  ai_description_file, ocr_file, transcription_file, banned, image_page, on_pages, should_be_on_pages)
  with "" / [] / false for empties. No missing key.
* banned is a real boolean everywhere (not null, not the string "true"); hard fail otherwise.
* Re-read {BAN_IMAGES_CSV} now (it may have changed mid-run) and confirm banned values agree.
* Banned entries with non-empty should_be_on_pages: 0. With non-empty image_page: 0.
* Every non-empty image_page exists and lives under {DOCS_DIR}/Photos.
* Every should_be_on_pages value: absolute tilde path, .md/.mdx, exists, under {DOCS_DIR}, NOT under
  {DOCS_DIR}/Photos. Grep page values for "...", "TODO", "TBD", "<", ">" and hard-fail on a hit. Zero tolerance.
* on_pages ⊆ should_be_on_pages per entry, or reported as a deliberate de-placement.
* Verify EVERY on_pages binding against the page's bytes; hard-fail on any unsubstantiated one; none under
  {DOCS_DIR}/Photos; all exist.
* Binding total vs reference total: above ~2x means fabrication crept back.
* Run the OUTPUT SANITIZATION scan; confirm one escaped file_path round-trips.

Output to stdout:
============================
STAGE 12 COMPLETE
Counts recomputed: yes
needs_split nodes: N
Duplicate _keys: 0   Duplicate sha256 within a node: 0
Entries banned: N   banned values disagreeing with {BAN_IMAGES_CSV}: 0
Banned entries with a non-empty should_be_on_pages: 0   with an image_page: 0
should_be_on_pages paths validated: N/N exist on disk   placeholders: 0
YAML parses: yes
============================

============================
STAGE 13 — VERIFY AND REPORT
============================

* Every non-excluded site Level 2 maps to exactly one level_3 (site_level_2 present); Other exists; every
  home-page TOC concept resolves to a level_3.
* Spot-check 10 Stage 7 pages: their images are reachable in the YAML.
* Spot-check 10 should_be_on_pages assignments by opening page and description; each path opens. Padding
  means the pass was too loose; report it.
* Nothing pre-existing removed: diff node and image counts vs Stage 1 (account for every on_pages removal).
* Independent re-derivation of on_pages: a SECOND extractor with a different approach (HTML/JSX parse, not
  regex) over non-Photos docs; diff against the YAML; they must agree. Every past failure was systematic.
* MEDIA-TYPE AUDIT (fail on any): zero `video:` items added (count <= Stage 1); zero `image:` entries added
  that type as video; no video-typed entry gained image_page, on_pages, sidecar path or should_be_on_pages;
  no path written under {VIDEOS_L2_DIR}, {VIDEOS_DIR}, {VIDEO_PLANNING_DIR}. Re-type from the reference, not
  the array (the 9 contaminated entries sit in `images:` arrays).
* Print the tree summary: each level_3 _key with recursive image count and child count.

Output to stdout:
============================
STAGE 13 COMPLETE — FINAL REPORT
level_3 nodes: N (was N)   level_4: N (was N)   level_5: N (was N)
Total image entries: N (was N)
Media-type audit: video added this run 0 (confirmed)
Legacy video contamination: N `video:` items + N mistyped `image:` items
  (was 53 + 9 on 2026-07-23; handed off to findings, none enriched, none removed)
Published /Photos pages carrying a <video> element: N (was 9)
Sidecar coverage: ai_description N%, ocr N%, transcription N%
image_page coverage: N% (N of N entries bound to a Level 5 page)
BANNED: N entries banned (no Level 5 page, no served copy, no placement, no pin)
  {BAN_IMAGES_CSV} rows: N   {EXCLUDE_FILE} sha256 values: N
  banned entries still live on the site (removal worklist): N (listed)
on_pages coverage: N entries bound, N total bindings, all N verified against page bytes
should_be_on_pages coverage: N% (N of N entries planned onto at least one page)
Publishing worklist (should_be_on_pages minus on_pages): N placements pending
Every should_be_on_pages path exists on disk: confirmed
Nothing removed except unsupported on_pages bindings: N removed (confirmed)
============================

============================
HARD RULES
============================

* IMAGES ONLY (MEDIA-TYPE SCOPE). Type at harvest; non-images are counted, handed off, dropped; UNKNOWN is
  not an image. Never write under {VIDEOS_L2_DIR}, {VIDEOS_DIR}, {VIDEO_PLANNING_DIR}.
* {HIERARCHY_FILE} only grows; no duplicates; update in place. Carve-outs: (1) on_pages is rebuilt from
  observation and unsupported bindings are deleted and reported, never blanked wholesale (fail instead);
  (2) legacy video entries are never added to or enriched, never silently deleted.
* on_pages is OBSERVED, should_be_on_pages is REASONED (the confusion that corrupted 89% of on_pages). A
  banned entry gets should_be_on_pages: [] and its on_pages is a removal worklist.
* banned is COPIED DOWN from {BAN_IMAGES_CSV} by Stage 3B only; real boolean, default false. Banned = no
  Level 5 page, no served copy, no placement, no link, no pin; entry never deleted. Add CSV rows for newly
  found non-public material before the run ends.
* No page create/move/edit under {SITE_DIR}, no sidebars.ts, no {PAGES_CSV} edits. No pages in {THIS_DIR},
  no planning notes in {SITE_DIR}/docs/Photos/.
* _keys are future page_keys: unique file-wide, ASCII-only, treated like primary keys.
* No invisible Unicode (OUTPUT SANITIZATION); scan after every emit.
* Every page path (image_page, on_pages, should_be_on_pages) is an absolute tilde path to a file that EXISTS
  when written, from a stat()-verified index, verified before and after write. Placeholders are hard failures.
* Clusters are concept clusters: the folder proposes, the description decides, {CK_FILE} arbitrates.
* Later publishing follows the repo defamation rules (attribution, no stating a living person committed a
  crime, accusations cropped out of images). Raw claims stay private here or in {CK_FILE}.
* The original directive's "each image or video entry" for sidecars is SUPERSEDED (2026-07-23): video
  sidecars belong to the sibling pipeline against {VIDEO_HIERARCHY_FILE}.
