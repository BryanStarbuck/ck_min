ROOT_DIR dir is ~/BGit/Bryan_git/charlie-kirk

THIS_DIR dir is {ROOT_DIR}/image_planning
IMAGES_DIR dir is {ROOT_DIR}/images
HIERARCHY_FILE is file {IMAGES_DIR}/images.yaml
  Moved 2026-07-22. It used to be {THIS_DIR}/hierarchy_images.yaml. That old
  name and that old location are both gone — the file is now images.yaml and it
  lives in {IMAGES_DIR}, not in {THIS_DIR}.
GENERATOR_DIR dir is {THIS_DIR}/generator
INVENTORY_TSV is file {GENERATOR_DIR}/inventory.tsv

SITE_DIR dir is {ROOT_DIR}/site
DOCS_DIR dir is {SITE_DIR}/docs
HOME_PAGE is file {DOCS_DIR}/index.mdx
IMAGES_L2_PAGE is file {DOCS_DIR}/Photos/overview.mdx
PAGES_CSV is file {ROOT_DIR}/pages.csv
CK_FILE is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt
  (Real file. Moved 2026-09-19. ~/BGit/Bryan_git/charlie-kirk/Charlie_Kirk.txt is now a symlink to it —
   use that only to verify the location; always read and write the real path.)
CHARTER_FILE is file {THIS_DIR}/CLAUDE.md
EXCLUDE_FILE is file {THIS_DIR}/exclude_images.txt
BAN_IMAGES_CSV is file {IMAGES_DIR}/ban_images.csv

MIRROR_DIR dir is ~/_Mirror/Politics/Charlie_Kirk_Mi
MIRROR_SIDECAR_DIR dir is ~/BGit/Bryan_git/personal_large_files_bridge/_Mirror/Politics/Charlie_Kirk_Mi
REPO_SIDECAR_DIR dir is {ROOT_DIR}/.lfbridge

The SIBLING VIDEO PIPELINE — read-only from here, never written by this prompt:
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

Grow and improve {HIERARCHY_FILE} — the image evidence hierarchy YAML — so it
becomes the most full and complete hierarchy possible over the investigation's
STILL IMAGE corpus. Video is out of scope — see MEDIA-TYPE SCOPE below, and
read it before any stage runs. This prompt runs in multiple stages. Each adds to
the YAML or enriches it. Nothing is ever deleted from it. No duplicates are
ever created — when an item already exists, its YAML properties are updated in
place instead.

The end state this YAML is building toward: the site will eventually host an
image page for every image, all living under one Level 2 directory called
images (today that Level 2 is the Photos section, {IMAGES_L2_PAGE}). When we
later create the list-of-images page — the top level of the images area — that
page will be mostly a table of contents: a table with links into the images
directory's Level 3 pages, and those Level 3 pages come directly from the
level_3 nodes of this YAML. This prompt builds the YAML only. It does NOT
create or modify any Docusaurus page, and it does NOT touch sidebars.ts or
{PAGES_CSV}. Page generation is a later, separate prompt. Stage 11 plans image
placements onto topic pages, but it only RECORDS the plan in the YAML — it
places nothing and edits no page.

THE SCRIPTS THAT CARRY THIS OUT (all under {GENERATOR_DIR}):

  update_hierarchy.py       Stages 3, 8, 9, 10 and the counts/integrity pass,
                            then emits the YAML through the shared emitter.
  plan_should_be.py plan    Stage 11 — scores and selects should_be_on_pages.
  plan_should_be.py build   Stage 11 — writes agent shortlist slices instead
                            (the optional judgment pass; see Stage 11).
  plan_should_be.py write   Stage 11 — merges agent rows back in.
  verify_stage_12_13.py     Stages 12 and 13, read-only, exit 1 on failure.
                            Carries its own INDEPENDENT extractor (an HTML tag
                            parser, not the writer's regex) so a systematic
                            extraction bug cannot pass by agreeing with itself.
  verify_on_pages.py        Third opinion on Stage 8 alone.

Run order: update_hierarchy.py -> plan_should_be.py plan -> verify_stage_12_13.py.
Back up the YAML first; every one of these rewrites it in place.

Convergence priority order (if context runs short, complete in this order):
  1. Stage 3 — CID and pin status on every image (Stage 8 depends on it)
  1b. Stage 3B — banned: sync the ban set from {BAN_IMAGES_CSV} onto every entry
      (cheap, and Stages 10 and 11 are gated on it — never skip it)
  2. Stage 4 — site Level 2 sweep into YAML level_3 superset
  3. Stage 6 — filesystem Level 3/4 pages into YAML level_4/level_5 nodes
  4. Stage 7 — page image sweep into YAML image entries
  5. Stage 8 — on_pages: every other repo page that shows each image
  6. Stage 9 — sidecar file-path properties on every image entry
  7. Stage 10 — image_page path on every image entry
  8. Stage 11 — should_be_on_pages: where each image OUGHT to appear
  9. Stage 5 — home page tables of contents into more level_3s
 10. Stage 12 — counts and needs_split
 11. Stage 13 — verify

============================
KNOWLEDGE — MEDIA-TYPE SCOPE: THIS PIPELINE IS IMAGES ONLY
============================

This pipeline owns STILL IMAGES. It does not own video, and it never has —
earlier revisions of this prompt told it to harvest video anyway, and that
instruction is what put playable video pages under {DOCS_DIR}/Photos. That was
a defect. The rules below replace it.

Video belongs to the SIBLING pipeline, which is a complete mirror of this one:

  images                                videos
  ------                                ------
  {THIS_DIR}                            {VIDEO_PLANNING_DIR}
  {HIERARCHY_FILE}                      {VIDEO_HIERARCHY_FILE}
  {DOCS_DIR}/Photos                     {VIDEOS_L2_DIR}
  Img_*.mdx leaf pages                  Vid_*.mdx leaf pages
  ck_image_sha256 frontmatter           ck_video_cid + ck_video_sha256
  gen_photos_pages.py                   gen_videos_pages.py
  served from static/img/evidence       played from a public IPFS gateway

THE RULE, stated four ways so no stage can miss it:

  * A video NEVER becomes an entry in {HIERARCHY_FILE} — not as an `image:`
    item, not as a `video:` item, not under any node at any level.
  * A video NEVER gets an image_page. There is no such thing as a video page
    under {DOCS_DIR}/Photos. Its page belongs under {VIDEOS_L2_DIR} and is
    written by the video pipeline.
  * A video NEVER gets a should_be_on_pages placement from this prompt. The
    placement stage plans still images onto topic pages and nothing else.
  * This prompt NEVER writes to {VIDEO_HIERARCHY_FILE}, {VIDEOS_DIR},
    {VIDEO_PLANNING_DIR}, or {VIDEOS_L2_DIR}. It reads them freely.

HOW TO TELL A VIDEO FROM AN IMAGE. The YAML does not record media type, so it
is decided at harvest time from the reference itself, in this order:

  1. Extension on the resolved src or file_path: .mp4, .mov, .webm, .m4v,
     .mkv, .avi → video. Any still-image extension → image.
  2. Enclosing tag when the src is extensionless (the IPFS gateway case):
     a CID inside <video>, <source>, or a markdown link ending in a video
     extension is a video; a CID inside <img> or ![]() is an image.
  3. The video pipeline's own records, PARSED BY FILENAME — never scraped for
     CIDs wholesale, because these files describe a mixed corpus:
       - {VIDEOS_DIR}/manifest.yaml — take ipfs_cid only where that record's
         filename carries a video extension.
       - {ROOT_DIR}/IPFS/ipfs.txt — three-line blocks; a block contributes only
         when its `ipfs add "<filename>"` names a video. It also lists .jpg,
         .txt and .pdf.
       - {VIDEO_HIERARCHY_FILE} is NOT usable as an oracle yet. Per
         {VIDEO_PLANNING_DIR}/CLAUDE.md it is still a schema shell carrying the
         inherited IMAGE corpus, so every cid in it currently describes an
         image. Start consulting it once the video pipeline has populated it.
     Measured 2026-07-23: scraping every CID out of these three files types 70
     image entries as video when only 9 are. Parse by filename.
  4. Still undecided → treat it as UNKNOWN, not as an image. Report it and
     create nothing. Guessing "image" is how videos got in here.

Note that rule 2 means an extensionless IPFS CID cannot be typed from the YAML
alone once it has been harvested. That is exactly why the typing must happen at
harvest time, in Stage 7, and never be deferred to the page generator.

THE HAND-OFF. Finding a video is useful information, so it is recorded rather
than dropped. Append it to a section of {FINDINGS_FILE} headed:

    == VIDEO REFERENCES — HAND-OFF TO videos_planning ==

one line per distinct video, carrying the CID (or file path), the page it was
found on, and the enclosing tag. The video pipeline reads {THIS_DIR} as prior
art and picks these up. Do not write into {VIDEO_PLANNING_DIR} yourself.

LEGACY CONTAMINATION ALREADY IN THE FILE. As of 2026-07-23 {HIERARCHY_FILE}
already carries video that a previous run harvested, and every run must report
it:

  * 53 `video:` items across the tree.
  * 9 `image:` items whose CID is in fact an .mp4 — all of them under the
    level_4 node _key Narrative_Shot_in_the_Heart. These are the entries that
    produced the nine `<video>` players now published under
    {DOCS_DIR}/Photos/Official_Narrative/Narrative_Shot_in_the_Heart/.

This is the SECOND carve-out from the only-grows rule (the first is on_pages).
Video entries are contamination, not data, and the rule for them is:

  * Never add another one.
  * Never enrich one. A video entry is skipped by Stages 3, 8, 9, 10 and 11 —
    it gets no cid refresh, no on_pages, no sidecar paths, no image_page, no
    should_be_on_pages.
  * Do not delete them silently either. Count them, list them, hand them off
    to {FINDINGS_FILE}, and report the totals in every stage that touches
    entries. Removing them from the YAML and un-publishing the pages they
    produced is a separate, explicitly-approved job, because the same content
    has to land under {VIDEOS_L2_DIR} before it leaves {DOCS_DIR}/Photos.

============================
KNOWLEDGE — THE LEVEL MODEL (READ THIS FIRST)
============================

Two different level systems are in play. Do not confuse them.

The SITE (filesystem) levels:
  * Level 1 — the site home page ({HOME_PAGE}).
  * Level 2 — the top-level sections: the directories directly under
    {DOCS_DIR}. Examples: TPUSA, FBI, UVU, Israel, Mic, Planes, Timeline.
    Photos (images) and Videos are also Level 2s.
  * Level 3 — the pages inside a Level 2 directory (overview.md plus the
    individual analysis pages, and first-level subdirectory overviews).
  * Level 4 — pages one directory deeper.

The YAML ({HIERARCHY_FILE}) levels:
  * There is no level_1 and no level_2 inside the YAML. Level 1 is the site
    home and Level 2 is the images landing page itself, so the YAML's cluster
    tree begins at level_3.
  * "Level two refers to the images directory" — the entire YAML tree hangs
    under the future images Level 2 page. Every YAML level_3 becomes a child
    page of that images Level 2.

THE CORE MAPPING RULE — increment by one:
  We are effectively taking all the Level 2s, Level 3s, and Level 4s that exist
  in the site filesystem outside this YAML and reproducing that same hierarchy
  inside the YAML, but with every level number incremented by one:

    site filesystem Level 2  →  YAML level_3
    site filesystem Level 3  →  YAML level_4
    site filesystem Level 4  →  YAML level_5

  So the YAML's level_3 list is a SUPERSET that includes the site's list of
  Level 2s (except images, videos, and unfiltered/queue categories — see
  Stage 4), the YAML's level_4 nodes correlate to the site's Level 3 pages
  parented hierarchically under their appropriate level_3 parent, and each
  image found on a site Level 3 page becomes a level_5 entry parented on the
  level_4 node that correlates to that filesystem Level 3 page.

  Additionally, image clusters that came from the mirror
  ({MIRROR_DIR}) already exist in the YAML and stay — the site-derived nodes
  merge INTO this tree, they do not replace it.

============================
KNOWLEDGE — THE YAML FILE TODAY
============================

{HIERARCHY_FILE} exists (about 9,000 lines, ~500KB). Read it and learn from it
before changing anything. Its current shape:

  * Root key `level_3:` is an array. Each item is itself keyed `level_3:`.
    A level_3 node may contain a `level_4:` array; a level_4 may contain a
    `level_5:` array. Same shape at every depth.
  * Cluster node fields: title (human readable, spaces allowed), _key
    (underscores, four words or less, unique across the WHOLE file — this is
    the future page_key in {PAGES_CSV}), number_of_images (direct count),
    number_of_images_recursive (subtree count), optional
    needs_split: true (node is over the 12-image ceiling; split on a later
    pass), images (array of image items).
  * Image item fields today: cid (the IPFS CID — spoken as "SID", it means the
    CID; historically left empty, now filled for every entry with a local file
    by Stage 3), ipfs_pinned (true/false — whether the local IPFS node pins
    those blocks; a CID exists whether or not it is pinned), sha256 (the identity —
    fingerprint from Large File Bridge is deferred, sha256 stands in),
    file_path (path to the original file, usually under {MIRROR_DIR}),
    ai_description (inline prose text, mostly empty today),
    ai_description_file / ocr_file / transcription_file (paths to the Large
    File Bridge sidecars, "" when the sidecar does not exist — see Stage 9),
    image_page (path to the published Level 5 page that hosts this one image,
    "" when no page exists yet — see Stage 10), on_pages (list of every OTHER
    page in the repo that shows this image TODAY — see Stage 8; supersedes the
    old flat on_site_pages property, which is migrated and removed),
    should_be_on_pages (list of every page in the repo this image SHOULD appear
    on — the planned end state, computed in Stage 11), optional
    ipfs_url (for entries that exist only as an IPFS embed with no local
    file), optional also_filed_in (list of other mirror dirs the same sha256
    legitimately lives in — cross-filing is deliberate and kept).

  * The full property set on an image item, in emission order:

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

    Every image entry carries every one of these properties. A property that
    has no value is emitted as the empty string "" — never omitted, never
    null. Absence of the key would make later passes unable to tell "not
    looked up yet" from "looked up, does not exist." The exceptions to the
    ""-for-empty rule are the typed properties: on_pages and
    should_be_on_pages are lists and emit [] when empty, and ipfs_pinned and
    banned are booleans and emit false — ipfs_pinned when the local node does
    not pin the CID, banned when no row in {BAN_IMAGES_CSV} matches the image.
  * banned is the publish gate. It is a real boolean, always present, default
    false, and its value is COPIED DOWN from {BAN_IMAGES_CSV} by Stage 3B —
    the only stage allowed to write it. banned: true means no Level 5 page, no
    served copy, no placement on any page, and no link into it from anywhere.
    See the BANNED knowledge section below.
  * About 21 level_3 clusters exist today (FBI, The Shot and the Shooter
    Position, Unfiled Backlog, Patsy Candidates, Security Team, TPUSA, Court
    and Legal Proceedings, Aircraft and Flight Evidence, Tyler Robinson,
    Memes and Commentary, Ballistics and the Gun, The UVU Venue, Charlie Kirk
    Himself, People of the Investigation, The Microphone, CIA and US
    Intelligence, Google Search Evidence, The Table Hand Off, Maps and Site
    Geometry, Israel and Mossad, The Truck and Back of Tent). They were
    generated by a first pass from the mirror's own concept filing.
  * Prior art: {GENERATOR_DIR}/gen_hierarchy.js built that first pass from
    {INVENTORY_TSV} (sha256, dir, filename, orig_path, has_desc per image)
    plus a clusters.json merge map. Read both to understand how dedupe was
    done (same sha256 in the SAME dir collapses; same sha256 in DIFFERENT
    concept dirs is deliberate and recorded as also_filed_in) and how unique
    _keys were minted. Reuse those conventions.

Cluster sizing rules (from the charter, {CHARTER_FILE}):
  * Six images per page is the target. Twelve is the ceiling. Over twelve
    means the node is not one concept — mark needs_split: true and split one
    level deeper on a later pass.
  * Clusters are concept clusters. The question is always "what is this
    evidence about," never "when was it downloaded" or "who posted it."
  * Titles may use spaces and full words. Keys use underscores, four words or
    less, unique file-wide.

============================
KNOWLEDGE — THE BANNED PROPERTY (COPIED DOWN FROM {BAN_IMAGES_CSV})
============================

Every image entry carries `banned:`. It is a real boolean, always present, never
null, never a missing key — same rule as every other field. The default is
false. An entry is banned: true only because a row for it exists in the ban CSV.

WHAT BANNED MEANS. Banned is a PUBLISH-TIME GATE, not a delete. A banned image:

  * Gets NO Level 5 page under {DOCS_DIR}/Photos. If one exists it is deleted
    by {THIS_DIR}/p_yaml_to_site.md — not by this prompt, which never touches a
    page.
  * Gets NO served copy under the site's static evidence directory
    (STATIC_IMG_DIR in {THIS_DIR}/p_yaml_to_site.md). A page that omits the
    accusation in its prose is not enough; the file itself must stop being
    served, because the image is the payload.
  * Is NEVER placed on any other page anywhere on the site. No topic page, no
    cluster page, no table of contents, no thumbnail, no card, no link. Nothing
    links INTO it, because there is nothing to link into.
  * Is NEVER pinned to IPFS. Any pinning job filters banned entries out before
    it runs. IPFS publication is not reversible in practice — a CID that has
    been announced and fetched can be served by anyone who cached it — so the
    gate has to hold BEFORE the pin, not after.
  * Keeps its entry in {HIERARCHY_FILE} forever. This file only grows. Banning
    changes what is published; it never changes what is known.

WHERE THE DECISION LIVES. {BAN_IMAGES_CSV} is the MASTER. The repo charter
({ROOT_DIR}/claude.md, "Banned Media") owns the contract. The YAML property is
DOWNSTREAM — it exists so the rest of the pipeline can read the decision out of
the data it already has, but it is a copy and never the source:

    ban_images.csv  ──▶  images.yaml (banned:)  ──▶  site/docs/Photos/ pages

Edits go in the CSV. Never hand-edit `banned:` in the YAML — the next run of
this prompt overwrites it. Never treat the YAML as the place where the ban was
decided.

CSV FORMAT. Header row, then one row per item:

  sha256        sha256 hex digest of the image file. PRIMARY identity here —
                survives renames, moves, and the duplicate copies cross-filing
                creates. Nearly every image in this corpus has one.
  cid           The IPFS CID when one is assigned, else empty. Secondary.
  file_path     Full path from ~. For humans reading the CSV and as a
                last-resort match key. Not authoritative — files move.
  banned        true or false. Normally true. A row set to false is an explicit
                UN-BAN: the row stays as the record of the decision and its
                reason, and the item publishes normally.
  reason        Short plain-text reason. Required.
  date_added    YYYY-MM-DD the row was added.

MATCH ORDER: sha256 first, then cid, then file_path. Any match sets the entry's
banned to that row's banned value. An entry matched by no row gets banned: false.

CROSS-FILING MAKES sha256 THE RIGHT KEY. The same image legitimately appears
under several concept nodes (that is what also_filed_in records), so one CSV row
must ban EVERY copy of it. Matching on sha256 does that automatically; matching
on file_path would ban one copy and publish the rest.

THE OLDER LIST. {EXCLUDE_FILE} is the previous one-sha256-per-line never-publish
list and it still counts. The BAN SET is the UNION of the two, minus any CSV row
explicitly marked banned=false. New bans go in the CSV; do not empty
{EXCLUDE_FILE} to "move" entries into the CSV, and do not delete lines from it —
leave them and add the row.

WHY THIS GATE EXISTS. The mirror is a years-long personal filing area and
private material was swept into it by accident — bank and health-account
dashboards, booking confirmations, billing portals, video calls showing named
participants' faces. Eleven such entries were found published during the first
full run. The second category is defamation: composite screenshots that stamp an
unproven criminal accusation about a named living person into the pixels, where
prose cannot soften it and cropping cannot remove it.

WHEN A RUN FINDS SOMETHING THAT SHOULD NOT BE PUBLIC — private personal
documents, an unrelated third party's records, anything whose subject has no
connection to the investigation, an accusation burned into the image — add a row
to {BAN_IMAGES_CSV} with a reason and the date BEFORE the run ends, and note it
in {FINDINGS_FILE}. Do not wait for a later pass; Stage 11 of this same run may
otherwise plan it onto a dozen topic pages.

============================
KNOWLEDGE — SIDECAR FILES (OCR, TRANSCRIPTION, AI DESCRIPTION) AND THE PATH MAPPING
============================

Large File Bridge (the web app at {LFB_DIR}; understand it by reading the
product management specification files in {LFB_PM_DIR} and the code) produces
three sidecar text files per media file. They answer three different questions:

  * .transcription   — "what was SAID" (audio/video speech, verbatim)
  * .ai_description  — "what is SEEN" (a vision model's hyper-detailed prose
                       about the image or video frame)
  * .ocr             — "what does it SAY on screen" (the literal text visible
                       in the pixels, verbatim — screenshots, slides, signs,
                       chyrons, documents)

Naming rule: the sidecar keeps the media file's FULL filename (original
extension kept) and APPENDS the second-level extension:
  Blue_Side.mp4  →  Blue_Side.mp4.transcription
  Blue_Side.mp4  →  Blue_Side.mp4.ai_description
  Blue_Side.mp4  →  Blue_Side.mp4.ocr
  photo.jpg      →  photo.jpg.ai_description  (and photo.jpg.ocr)

Placement rule — where the sidecar lives depends on whether the original is
inside a working git repo (this is the mapping pattern; the authoritative spec
is {LFB_PM_DIR}/artifact_placement_policy.mdx section 0, with
ai_description.mdx, ocr.mdx, Transcribe.mdx, and repo_tracking_scheme.mdx):

  * Original INSIDE a working git repo — the sidecar is path-mirrored under
    that repo's committed .lfbridge/ tracking directory:
      {ROOT_DIR}/videos/X.mp4
        →  {REPO_SIDECAR_DIR}/videos/X.mp4.transcription
      {REPO_SIDECAR_DIR} currently holds videos/ and IPFS/videos/ sidecars.

  * Original OUTSIDE any git repo (the mirror) — there is NO .lfbridge/
    segment. The dedicated bridge repo (an "SDL": a personal or company file
    repo that exists only to hold these files) IS the tracking area, and the
    mirror hangs directly off its root:
      {MIRROR_DIR}/Autopsy/X.jpg
        →  {MIRROR_SIDECAR_DIR}/Autopsy/X.jpg.ai_description
      Personal SDL: {PERSONAL_BRIDGE_DIR}
      Company SDL:  {COMPANY_BRIDGE_DIR}

  * Older files may still sit under a .lfbridge/_Mirror/ path until Large File
    Bridge migrates them. Check both locations before concluding a sidecar is
    missing.

Coverage snapshot at the time this prompt was written (re-count at run time —
these grow constantly): under {MIRROR_SIDECAR_DIR} there were ~1,978
.ai_description files, ~1,795 .ocr files, and ~331 .transcription files.
Coverage is no longer thin — most images now have descriptions and OCR.

WHAT THIS MEANS FOR THE YAML: every IMAGE entry in {HIERARCHY_FILE} gets YAML
properties holding the FILE PATH to each sidecar that exists for it. This is
required — the sidecars are how later passes search, cluster, caption, and
publish. The properties are:

  ai_description_file   path to the .ai_description sidecar, or "" if none
  ocr_file              path to the .ocr sidecar, or "" if none
  transcription_file    path to the .transcription sidecar, or "" if none
                        (an image rarely has one; it is kept on the schema so
                        entries stay uniform)

Legacy video entries get NO sidecar properties from this prompt — see
MEDIA-TYPE SCOPE. Video sidecars, which is where .transcription actually earns
its keep, are the video pipeline's job against {VIDEO_HIERARCHY_FILE}.

The existing inline ai_description field stays as the short prose text; the
new *_file fields point at the full sidecar files on disk.

============================
KNOWLEDGE — THE SITE'S LEVEL 2 SECTIONS (SNAPSHOT)
============================

Enumerate live at run time (ls {DOCS_DIR}) — the list below is a snapshot so
you know what to expect. Directories directly under {DOCS_DIR}:

  After, analysis_documentation, Before, cameras, campus_university,
  Cause_of_Death, Censorship, Charlie, Companies_Organizations, court,
  CoverUp, Defamation, distraction_people, Drones, Electrocution, FBI, Fix,
  GoogleSearches, gov, Gov_Mind_Control, government_organizations, Gun_Bullet,
  Influencers, intelligence, Iran, Israel, Israel_Main_Suspect,
  key_individuals, Killer, Law_Enforcement, laws, Legal, legal_investigation,
  Locations, maps, Media, Medical, Mic, Motive, Narrative,
  organizations_groups, Other, other_topics, People, Photos, Planes,
  political_context, Proof_Intel_Services, Proof_Not_Tyler,
  security_law_enforcement, Security_Team, social_media_analysis, Suspects,
  Suspicious, technology_surveillance, Tent, Theories, Timeline,
  Topic-Analyses, Topics3, TPUSA, Tyler_Robinson, Tyler_Robinson_Not_Assassin,
  US_Intelligence, US_Intelligence_Assisted, UVU, Videos, Vote, Witnesses,
  Your_Actions_Fix_It

{PAGES_CSV} is the master page index (page_key, parent_key, level, url_path,
file_path, title, ...). Use it alongside the filesystem walk — the CSV gives
you each page's level and parentage directly; the filesystem walk catches any
drift. When they disagree, the filesystem is what actually exists.

============================
STAGE 1 — SETUP AND READ
============================

* Read {CHARTER_FILE} — the image_planning charter. It is the authority on
  the audience model, the level model, the YAML schema, and the hard rules.
* Read {HIERARCHY_FILE} fully. Build an in-memory index of: every _key, every
  node path, every sha256 and the node(s) it lives under.
* Read {GENERATOR_DIR}/gen_hierarchy.js, {GENERATOR_DIR}/clusters.json, and
  the header of {INVENTORY_TSV} — the prior-art conventions.
* Read {PAGES_CSV}.
* Read {BAN_IMAGES_CSV} — the MASTER record of what must never be published.
  Create it with the header row sha256,cid,file_path,banned,reason,date_added
  and no data rows if it does not exist. Stage 3B copies it down onto every
  entry as `banned:`. Read {EXCLUDE_FILE} alongside it; the ban set is the union
  of the two. Report both counts here, so a run that is about to plan thousands
  of placements knows up front what is off limits.
* Enumerate {DOCS_DIR} top-level directories (the site Level 2s).
* Reference {CK_FILE} as needed throughout — it is the source of truth for
  what the investigation's concepts actually are. The hierarchy must mirror
  the investigation's real concept structure, not an arbitrary photo-album
  structure. Do not read all 400K+ lines up front; consult sections when a
  clustering or parenting decision needs arbitration.

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

* Read these product management specs in {LFB_PM_DIR} (frontmatter
  description paragraph plus the placement sections are enough):
    ai_description.mdx, ocr.mdx, Transcribe.mdx,
    artifact_placement_policy.mdx, repo_tracking_scheme.mdx
* Confirm the mapping rules from the KNOWLEDGE section above against the
  actual disk: pick 5 sample images under {MIRROR_DIR}, compute their
  expected sidecar paths under {MIRROR_SIDECAR_DIR}, and verify existence.
  Do the same for one repo-internal file under {VIDEOS_DIR} against
  {REPO_SIDECAR_DIR}. That sample verifies the inside-a-git-repo mapping rule
  and nothing more — it does NOT add that file to {HIERARCHY_FILE}.
* Count current sidecar coverage: number of .ai_description, .ocr, and
  .transcription files under {MIRROR_SIDECAR_DIR}.
* If a sample is missing, check the legacy .lfbridge/_Mirror/ location
  before concluding it does not exist.

Output to stdout:
============================
STAGE 2 COMPLETE
Mapping verified: N/5 mirror samples, repo sample yes/no
Sidecar counts: ai_description N, ocr N, transcription N
============================

============================
STAGE 3 — CID: EVERY IMAGE GETS ITS IPFS CID AND PIN STATUS
============================

This stage runs BEFORE the page sweeps on purpose. Site pages embed evidence
images two ways — as a local static file, and as an IPFS gateway URL
(https://ipfs.io/ipfs/<CID>/..., https://<CID>.ipfs.dweb.link/...). The later
on_pages sweep (Stage 8) has to recognise an image by its CID when the page
references it only by CID. So the CID column has to be populated first, or
every IPFS-embedded reference on the site is unmatchable.

KNOWLEDGE — how a CID is obtained.

A CID is a content address. It is COMPUTED from the file's bytes — it does not
require the network, a daemon, or the file ever having been published. So
every image with a local file on disk can always get a CID, whether or not it
is pinned anywhere:

    ipfs add -n -Q "<file>"          # compute only, no add, default settings

  -n / --only-hash  computes the CID without writing the block to the node
  -Q / --quiet      prints just the CID

USE THE DEFAULT CID VERSION — CIDv0, the base58 "Qm..." form. That is what the
site already embeds (https://ipfs.io/ipfs/Qm... appears on the Photos image
pages and on topic pages such as site/docs/Israel/Mossad.mdx) and what the
local node's pin set holds. Passing --cid-version=1 produces a DIFFERENT
string (bafkrei.../bafybei...) for the same bytes, because v1 also switches
the leaf codec — it would not match a single URL on the site and Stage 8 would
resolve nothing. If a v1 form is ever needed for a dweb.link subdomain URL,
convert at use time with `ipfs cid base32 <cid>`; do not store it.

Pinning is a SEPARATE question from having a CID. Pinned means "this node
holds the blocks and rebroadcasts them so a public gateway can serve it."
Check it against the local node:

    ipfs pin ls --type=all <cid>       # exit 0 and prints the cid = pinned
    ipfs block stat <cid>              # blocks present locally

Chunking settings change the CID, so ALWAYS use the same flags on every run
(-n -Q, default chunker, default CIDv0). A CID computed with different flags
will not match the one in a gateway URL.

WHAT TO DO.

* For every IMAGE entry in {HIERARCHY_FILE} that has a file_path pointing at a
  file that exists on disk (legacy video entries are skipped — MEDIA-TYPE
  SCOPE):
    * Compute the CID with the flags above. Write it to the entry's `cid`
      property. This is unconditional — a CID is always obtainable for a local
      file, so an entry with a readable file_path must never be left with
      cid: "".
    * Check pin status against the local IPFS node and record it:
        ipfs_pinned: true      the local node pins it (it is being served)
        ipfs_pinned: false     CID computed, but the node does not pin it
    * Do NOT pin anything in this stage. Pinning publishes content to the
      public IPFS network and it is irreversible in practice — a CID, once
      announced, can be fetched and cached by anyone. Some images in this
      corpus must never be published (see {BAN_IMAGES_CSV} and {EXCLUDE_FILE} —
      the private/personal material pulled 2026-07-22 and everything banned
      since). This stage RECORDS state; it does not change what is public. If a
      run wants to pin the publishable set, that is a separate,
      explicitly-approved job that must first filter out the whole ban set —
      every banned: true entry, which is to say every identity in
      {BAN_IMAGES_CSV} and every sha256 in {EXCLUDE_FILE}.
* For entries with NO local file (ipfs_url-only entries harvested from site
  embeds), the CID is already known from the URL — parse it out of the URL and
  set `cid` from it. Set ipfs_pinned by asking the local node; if the node
  does not have it, false.
* For entries whose file_path points at a file that no longer exists on disk:
  leave cid: "" and report the entry. Never invent a CID.
* Also mirror the finding the other way: build a CID -> sha256 index in memory
  and hold it for Stage 8, which needs to resolve an IPFS URL on a page back
  to the image entry it belongs to.
* Never overwrite a non-empty cid with "". If a recorded CID no longer matches
  the recomputed one, that means the file's bytes changed — report the
  mismatch, keep the recomputed value, and note the old one.

Do this with a script, not by hand — there are ~1,700 entries. Batch the
`ipfs add -n` calls and cache by sha256, since the same sha256 appearing under
several nodes (deliberate cross-filing) has exactly one CID.

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

Read the BANNED knowledge section before running this. This stage is the ONLY
place in the whole pipeline that writes `banned:`. It reasons about nothing. It
copies a decision that was already made in {BAN_IMAGES_CSV} down onto the data,
so every later stage and every later prompt can see it.

Run it on every run, immediately after Stage 3, and re-run it any time the CSV
changes. It is cheap and it is idempotent.

STEP 1 — READ THE BAN SET.

  * Read {BAN_IMAGES_CSV}. Parse it as a real CSV (python3 csv module — the
    reason column contains commas, semicolons and quoted text). Expected header:
    sha256,cid,file_path,banned,reason,date_added
  * If the file does not exist, CREATE it with that header row and zero data
    rows, then continue. A missing CSV means "nothing is banned", not "skip the
    gate" — and the file needs to exist so the next person can add a row.
  * Parse the banned column strictly: "true" (any case) is true, "false" (any
    case) is false. Anything else is a malformed row — STOP and report it rather
    than guessing. Guessing "false" on a malformed row publishes banned material.
  * Build three lookup dicts from the rows: by sha256, by cid, by expanded
    file_path (expand ~ on both sides before comparing).
  * Read {EXCLUDE_FILE} too. Every sha256 in it joins the ban set with
    banned=true, unless a CSV row for that same identity says banned=false — an
    explicit CSV un-ban wins, because it is the newer and more deliberate record.

STEP 2 — SET banned ON EVERY ENTRY.

  * Walk every image entry in {HIERARCHY_FILE}, at every depth.
  * Look the entry up in the ban set: sha256 first, then cid, then file_path.
    First match wins and supplies the value.
  * No match → banned: false.
  * Write the key on EVERY entry, including the false ones. Never omit it,
    never emit null. A missing key is indistinguishable from "not checked yet"
    and this is exactly the field where that ambiguity is dangerous.
  * A banned sha256 bans EVERY copy of that image, in every node it is
    cross-filed into. Verify that: count the entries banned and the distinct
    sha256s banned, and print both. If they are equal on a corpus that
    cross-files, the walk missed the duplicates.
  * Never delete an entry because it is banned. The file only grows.

STEP 3 — REPORT THE ROWS THAT MATCHED NOTHING.

  A CSV row that matches no entry is a real finding, not noise. It usually means
  one of three things and each needs a different fix:

    * The identity is stale (the file was re-saved or re-encoded, so its sha256
      moved).
    * The item is a video, filed in the wrong CSV — check {VIDEOS_DIR}/
      ban_videos.csv and say so.
    * The item is genuinely not in this corpus yet, and the row is pre-emptive.
      That is legitimate. Keep the row.

  List every unmatched row with its reason text. Do not delete unmatched rows.

STEP 4 — RE-EMIT AND VALIDATE.

  Emit through the shared emitter — reuse emit_node/recount from
  {GENERATOR_DIR}/bind_image_pages.py, which round-trips this file byte-for-byte
  — so a run that changes no banned value produces a byte-identical file. Verify
  the YAML parses. Apply OUTPUT SANITIZATION: the reason column is human-typed
  text and a plausible carrier of invisible Unicode, so treat it as untrusted
  even though this stage does not copy the reason into the YAML.

DO NOT, IN THIS STAGE:

  * Do not delete, move, or edit any page, and do not delete any served copy
    under the static evidence directory. This prompt never touches either.
    Removing the page and the served file for a newly banned image is
    {THIS_DIR}/p_yaml_to_site.md's job.
  * Do not clear image_page, on_pages, or should_be_on_pages here. on_pages is
    an OBSERVATION — "this image is on that page today" stays true and is
    exactly what tells the page prompt what to go remove. Stages 10 and 11
    handle the forward-looking fields.
  * Do not pin, unpin, or touch IPFS in any way.

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

The YAML's list of level_3 nodes must include ALL of the website's Level 2
sections, except:

  * Photos (the images Level 2 itself — the YAML hierarchy IS its content)
  * Videos (same reasoning — a media Level 2, not a concept)
  * Topics3 (template scaffolding, not a real section — the /Topics3/Photos
    page is unrelated to this hierarchy; do not confuse the two)
  * Any unfiltered / queue / catch-all category EXCEPT Other: we DO include
    one "Other" level_3 in the YAML as the catch-all. Fold other_topics-style
    catch-alls into that single Other node rather than creating several.
  * Non-page files at the docs root (index.mdx, Topics.mdx, image_list.csv,
    video_list.csv, index.html) — these are not sections.

For every remaining site Level 2 (TPUSA, FBI, UVU, Israel, Mic, Timeline,
etc.):

* Check whether a YAML level_3 already covers that concept. Match by _key,
  by title, and by meaning — e.g. existing "TPUSA" covers site TPUSA;
  "The UVU Venue" covers site UVU; "Ballistics and the Gun" covers site
  Gun_Bullet; "Aircraft and Flight Evidence" covers site Planes;
  "CIA and US Intelligence" covers site intelligence / US_Intelligence;
  "Court and Legal Proceedings" covers site court / Legal /
  legal_investigation. Do NOT create a duplicate concept under a second name.
  Record the site-dir-to-level_3 mapping you decide in a comment on the node:
    site_level_2: <dirname>   (add this property to every level_3 node,
    a list if several site dirs map to one node, empty list if the node is
    mirror-only)
* If no existing level_3 covers it, append a new level_3 node: title from the
  section's human-readable name, unique _key (four words max, underscores),
  number_of_images: 0, number_of_images_recursive: 0, images: [],
  site_level_2: [<dirname>].
* Never remove or rename an existing level_3. Grow only. Update properties in
  place when the node already exists.

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

The home page {HOME_PAGE} is the site's Level 1 and it carries MORE than one
table of contents — the three-column flex divs under "Biggest Question Marks",
the "## Table of Contents" section, "## Areas of Investigation", the
"Related Areas" and "Related" sections, and the per-thesis link clusters
(Tyler Robinson Not Assassin, Cause of Death, Mossad / Israel Top Suspect,
US Intelligence Assisted, and others). These reflect how the investigation
actually organizes its concepts, and they are likely to surface areas that the
Level 2 directory sweep alone did not.

* Read {HOME_PAGE} fully. Extract every table of contents and every link
  cluster — all of them, not just the first.
* For each linked area/topic in those TOCs, resolve the link target to its
  site section, and check whether a YAML level_3 covers that concept.
* Add a new level_3 for each one not yet covered, using the same rules and
  fields as Stage 4. No dupes — an area already covered by an existing
  level_3 (under any name) is skipped, though you may update that node's
  properties (e.g. append to site_level_2, refine title) if the TOC reveals a
  better human-readable name.
* This stage is expected to ADD items beyond the previous stages — that is
  its purpose. The YAML must end up the most full and complete hierarchy
  possible.

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

Apply the increment-by-one mapping rule to the pages inside each site Level 2.

For every site Level 2 that maps to a YAML level_3 (from Stage 4's
site_level_2 property):

* Enumerate its Level 3 pages: overview.md/.mdx plus every other page file
  directly in the directory, plus first-level subdirectory overviews. Use
  {PAGES_CSV} levels as the guide and the filesystem as the check.
* For each site Level 3 page, ensure a YAML level_4 node exists under the
  correct level_3 parent:
    title            the page's title (frontmatter title or first H1)
    _key             unique file-wide, four words max, underscores; prefer
                     the page's page_key from {PAGES_CSV} when it is free
    site_page: <repo-relative file path of the page>
    number_of_images / number_of_images_recursive / images: []
* For each site Level 4 page (one directory deeper), ensure a YAML level_5
  node under the correct level_4 parent, same fields.
* Skip pages that are pure navigation with no evidentiary concept of their
  own only if adding them would create an empty duplicate of their parent;
  when in doubt, include the page.
* Existing mirror-derived level_4/level_5 nodes stay where they are. If a
  site page and an existing mirror node are the same concept, MERGE: keep the
  existing node, add the site_page property to it. No dupes.
* Never remove existing nodes or images. Grow and update only.

Output to stdout:
============================
STAGE 6 COMPLETE
Site Level 3 pages processed: N → level_4 nodes (N new, N merged)
Site Level 4 pages processed: N → level_5 nodes (N new, N merged)
============================

============================
STAGE 7 — PAGE IMAGE SWEEP → IMAGE ENTRIES IN THE YAML
============================

Go through ALL the site's pages and make sure every page that has one or more
images gets those images represented in the YAML hierarchy.

* Scan every page under {DOCS_DIR} for embedded media: markdown image syntax,
  <img> tags, <iframe>/<video>/<source> embeds, and static-asset links.
  Use the SAME multi-line-aware extractor Stage 8 specifies — the site's
  dominant embed form splits `<img` and `src=` across lines, and a
  line-oriented pattern misses 72% of them. Resolve each src to the actual
  file: the served path /img/... maps to {SITE_DIR}/internals/static/img/...
  ({SITE_DIR}/static/ does not exist on this repo).

* TYPE EVERY REFERENCE BEFORE DOING ANYTHING WITH IT, using the four-step test
  in MEDIA-TYPE SCOPE. Video and UNKNOWN references get no entry — they are
  counted and appended to the hand-off section of {FINDINGS_FILE}, and the
  sweep moves on. Only references typed as still images continue below. The
  <video>/<source>/<iframe> forms are matched precisely so that the type test
  can see them, NOT so that they can be harvested; an extractor that ignores
  video tags would type an extensionless IPFS CID as an image and reintroduce
  exactly the bug this rule exists to prevent.

* Directories that are OUT OF SCOPE for the sweep: {DOCS_DIR}/Photos (this
  hierarchy IS its content), {VIDEOS_L2_DIR} (the video pipeline's published
  output — every reference on those pages is a video by construction), and
  {DOCS_DIR}/Topics3 (template scaffolding).

* SITE-ONLY ASSETS. Some published images have no mirror original at all —
  hand-made diagrams and timeline graphics living only under
  {SITE_DIR}/internals/static/ (All_Laws.jpeg, Timeline_Israel.jpeg,
  Iran_Timeline.jpeg, court/mirandize/*.png and others found at run time).
  They are real published evidence images and they belong in the corpus.
  Create an entry for each: sha256 the static file, file_path = the static
  file's tilde-rooted path, cid computed as in Stage 3, and park it under the
  level_3/level_4 node matching the page it appears on. Never skip a published
  image just because it did not come from the mirror.
* For each image found on a page:
    * Compute its sha256. Try to match it back to an original under
      {MIRROR_DIR} — first by sha256 against {INVENTORY_TSV} and the YAML's
      existing entries, then by filename. The mirror original is the
      preferred file_path; if there is no mirror original, use the site
      static file's path.
    * If that sha256 already exists anywhere in the YAML: do NOT add a
      duplicate. Update the existing entry's properties instead — and record
      the page reference by appending the page's repo-relative path to an
      on_pages list property on that image entry (see Stage 8 for its
      shape: a list of `- page:` mappings holding tilde-rooted page paths).
    * If it does not exist yet: add a new image entry under the level_4 (or
      level_5) node that correlates to the page it was found on — per the
      level model, "where those level_5 image entries are parented is on the
      level_4 in the YAML which correlates to the Level 3 page in the file
      system." Fields: cid (Stage 3 fills it), ipfs_pinned, sha256,
      file_path, ai_description: "", on_pages: [{page: <tilde-rooted page
      path>}], should_be_on_pages: [] (Stage 11 fills it), plus the sidecar
      path fields (Stage 9 fills them) and image_page: "" (Stage 10 fills it).
* Videos found on pages get NO entry — not a `video:` item and not an
  `image:` item. This is the exact instruction that shipped the defect: a
  previous revision of this line said "Videos found on pages get entries too,
  as `video:` items with the same fields," and the harvest that followed put
  53 `video:` items and 9 mistyped `image:` items into {HIERARCHY_FILE}, nine
  of which the page generator then published as playable `<video>` pages under
  {DOCS_DIR}/Photos. Hand them off to {FINDINGS_FILE} instead.
  {DOCS_DIR}/video_list.csv is the video pipeline's starting index, not this
  one's — do not read it as a source of entries.
* Images already embedded ad hoc inside topic pages across the site stay
  where they are on those pages — this hierarchy is the browsable index over
  the corpus, not a relocation of every inline image.

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

KNOWLEDGE — what on_pages answers.

Two properties record two different relationships, and they must not be
confused:

  image_page  "which page IS this image" — the one Level 5 page under
              {DOCS_DIR}/Photos that exists to host this single image. Set in
              Stage 10. Exactly one, or "".
  on_pages    "where ELSE is this image shown TODAY" — every OTHER page
              anywhere in the repo that embeds it right now, observed from the
              actual file contents. Zero to many. Set here.
  should_be_on_pages
              "where SHOULD this image be shown" — the planned end state,
              reasoned out rather than observed. Zero to many. Set in Stage 11.
              It is a superset of on_pages; the difference between the two is
              the publishing work still to do.

on_pages covers any page hosted on any site Level 2, Level 3, or Level 4 —
that is, anywhere OUTSIDE the images Level 2 directory. A page under some
other Level 2 hierarchy (FBI, Planes, Tyler_Robinson, People, Timeline, the
blog, anything) that wants to show that image gets its file path recorded on
the image entry.

THE PROPERTY SHAPE.

on_pages is a LIST OF MAPPINGS, each with a single `page:` key holding the
full path from ~ to the page file — the same tilde-rooted convention
file_path, image_page, and the sidecar path properties already use:

    on_pages:
      - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/FBI/overview.mdx"
      - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/Killer/israel-mossad.mdx"

Not a flat list of strings. Not repo-relative. Not URLs.

Every image entry carries the key. An image shown on no other page emits an
empty list:

    on_pages: []

ON_PAGES IS OBSERVED, NEVER INFERRED — THIS IS THE RULE THE LAST RUN BROKE.

on_pages is a statement of fact about bytes on disk: "the text of page P
contains a reference that resolves to this image." It is established by
reading P and finding the reference. There is exactly one way to earn a
binding, and it is that.

A binding may NEVER be produced by any of these:
  * the image and the page being about the same topic
  * the image sitting in a YAML cluster whose site_level_2 / site_page points
    at that page
  * a person named in the image also being the subject of the page
  * carrying a value forward from an earlier run without re-reading the page
  * an agent's judgment, recollection, or reasonable inference

If you find yourself deciding whether an image belongs on a page, you are
writing should_be_on_pages (Stage 11), not on_pages. Topical reasoning is
that stage's whole job and this stage's cardinal sin.

WHAT THE LAST RUN ACTUALLY PRODUCED — MEASURED 2026-07-23.

This stage has run before and its output is wrong in a specific, measurable
way. Reproduce these measurements at the start of the run; they are the
regression test.

  Ground truth, by a multi-line-aware sweep of every .md/.mdx under
  {DOCS_DIR} excluding Photos/:
      123 image references on 41 pages
      102 of them resolve to an image entry (76 by IPFS CID, 40 by evidence
          filename; some images appear on more than one page)
       34 distinct pages legitimately show a corpus image
        7 references are site-only assets with no YAML entry (listed below)

  What {HIERARCHY_FILE} contains:
      1,056 page bindings across 99 distinct pages
        946 of those bindings (89%) point at a page that contains no image
            reference at all
         68 of the 99 recorded pages are not in ground truth
          1 recorded page no longer exists on disk
          3 real pages are missing entirely: People/skylar-baird.mdx,
            US_Intelligence/Fort_Huachuca/Cabot_alibi.mdx,
            US_Intelligence/US_Army_HADES.mdx
      1,608 of 1,687 image entries have on_pages: []

  Read that carefully, because the obvious diagnosis is the wrong one. The
  problem is NOT that the empty lists are empty. Most of them are CORRECT —
  only 34 pages outside Photos show a corpus image, so the overwhelming
  majority of the 1,687 images genuinely appear nowhere but their own Photos
  page, and [] is the true answer for them. The problem is that 89% of the
  bindings that DO exist are fabricated: they came from the old
  `on_site_pages` property, which an earlier pass populated by topical
  guessing, and which the migration step then imported as though it were
  observation. Pages like Israel/overview.mdx, index.mdx and
  Suspects/Black_Clothing_Suspect.mdx each carry 33 image bindings while
  containing no image at all.

  So this stage's job is not "fill in the empties." It is: rebuild the whole
  property from observation, and delete every binding that observation does
  not support.

THE FAILURE THIS STAGE KEEPS REPRODUCING — READ BEFORE TOUCHING THE SCRIPT.

Run of 2026-07-23 found the fabrication had survived a rewrite, in a single line
of {GENERATOR_DIR}/update_hierarchy.py:

    merged = set(existing_pages.get(id(inner), set()))   # prior values
    merged |= sweep_pages.get(sha, set())                # observed values
    inner['on_pages'] = [{'page': p} for p in sorted(merged)]

That union is the bug. It reads the prior file, reads the observed sweep, and
keeps BOTH — so a fabricated binding written by any earlier run is re-adopted
every single run and can never be dislodged. It survived because the function
was named recover_on_pages() and reads like data recovery; recovering a value
that was never observed is fabrication with a friendlier name. Measured effect:
1,057 prior values, of which the sweep reproduced 123 — 934 (88%) were false and
had to be deleted.

The correct shape is assignment, not union:

    observed = sweep_pages.get(sha, set())
    for p in sorted(prior - observed):
        report_removal(p, sha, reason)
    inner['on_pages'] = [{'page': p} for p in sorted(observed)]

Whatever the sweep did not see is removed and reported. There is no merge step.
Guard it with the <80-references abort so a broken extractor fails loudly rather
than blanking the property.

MIGRATION — on_site_pages is the old name, and its values are UNTRUSTED.

Earlier passes wrote `on_site_pages`, a flat list of repo-relative page paths.
That property is now gone from the file; its values survive inside on_pages,
and 89% of them are wrong. Should it reappear in a future input:

  * Treat every on_site_pages value as a HINT, never as a binding. A hint
    earns a place in on_pages only by re-reading the page and finding the
    reference. A hint that fails verification is discarded and counted.
  * Do not "merge and keep both." That is precisely how the fabricated
    bindings became permanent.
  * After this stage, `on_site_pages` must not appear anywhere in the file.

THE ONE PLACE THIS PROMPT DELETES DATA — AND WHY IT MUST.

The hard rule elsewhere in this prompt is that {HIERARCHY_FILE} only grows.
on_pages is the single carve-out, because a false binding is not data, it is a
factual error about the contents of a file, and it actively misleads Stage 11
(which unions on_pages into should_be_on_pages, so every fabricated binding
becomes a fabricated publishing instruction).

  * Rebuild on_pages from ground truth on every run: compute the observed set,
    then set each entry's on_pages to exactly that set.
  * Every removed binding is REPORTED — page path, image sha256, and the
    reason (page has no such reference / page does not exist on disk).
  * Removal applies to on_pages ONLY. No node, no image entry, and no other
    property is ever removed by this stage.
  * If the observed set for the whole run comes out implausibly small (fewer
    than 80 resolvable references site-wide), the extractor is broken — do NOT
    write the file. Fail, report, and fix the extractor. Never let a broken
    extractor blank out on_pages across the corpus.

HOW TO FIND THE REFERENCES — one linear pass, multi-line aware.

The work is a reverse index: for every page file in the repo, what images does
it show. Read each file exactly once. This is O(n) over the repo's text, not
O(images x pages).

* Enumerate every text file in the repo recursively — every .md, .mdx, .html,
  .tsx/.jsx/.ts/.js, .json, .csv, .yaml under {ROOT_DIR}, skipping
  node_modules/, build/, .git/, and {SITE_DIR}/internals/static/ binaries.
  Include the blog and any React components that embed evidence images.

* THE EXTRACTOR MUST BE MULTI-LINE AWARE. This is the second bug that broke
  the last run. The site's dominant embed form puts the tag open and the src
  on DIFFERENT LINES, wrapped in an anchor:

      <a href="/Photos/People/People_tyler_bowyer/Img_Photo_3caf21"><img
        src="https://ipfs.io/ipfs/QmVA7WhYwAvFXe7rjdrgrRwdCJpprLG39vrS3Xp8PK2otq"
        alt="Screenshot of a February 2022 exchange ..."
        style={{width: '100%', height: 'auto', aspectRatio: '1320/1297'}}
      /></a>

  A line-oriented pattern such as `<img[^>]*src="[^"]+` finds NOTHING here. On
  this corpus it recovers 35 of 123 references — it silently misses 72% of
  them, and 34 of the 41 pages with images look image-free. Match the whole
  tag across newlines and then pull src out of it:

      tags = re.findall(r'<img\b.*?>', text, re.S)
      src  = re.search(r'src=["\']([^"\']+)["\']', tag)

  Any regex used here is tested against a known multi-line page before the
  sweep runs. `grep`-based extraction is not acceptable for this stage.

* Reference forms that actually occur, with their measured share of the 123:

      76  <img src="https://ipfs.io/ipfs/<CID>">     IPFS gateway, 62%
      40  <img src="/img/evidence/<sha256>.jpg">     published evidence, 33%
       7  <img src="/img/<name>.jpeg"> and
           <img src="/court/mirandize/<name>.png">   site-only assets, 5%

  Also handle, even though they are currently rare or absent here — the site
  changes and the extractor must not silently miss a new form: markdown
  `![alt](src)`, `<img>` with a `require()`/import src, background-image /
  style url(), `https://<CID>.ipfs.dweb.link/`, `ipfs://<CID>`, and
  `<video>`/`<source>`/`<iframe>` src and poster attributes. Video tags are
  matched so the extractor can TYPE what it found and prove it missed nothing;
  a reference typed as video per MEDIA-TYPE SCOPE is then counted and skipped,
  never bound to an entry. A `<video>` poster frame is a still image and IS
  eligible — it is a separate asset from the video it fronts.
  Count every form found, and hard-fail the run if a
  reference form appears that the extractor has no rule for — an unknown form
  must surface as a reported unresolved reference, never be dropped silently.

* PATH FACTS the resolver depends on (verified 2026-07-23):
    - The served path /img/... maps to {SITE_DIR}/internals/static/img/...
      NOT to {SITE_DIR}/static/ — that directory does not exist. A resolver
      that looks only under {SITE_DIR}/static/ resolves zero static refs.
    - {SITE_DIR}/internals/static/img/evidence/ holds 1,453 files and the
      filename IS the full lowercase 64-hex sha256 plus extension
      (0025bec0...280f.jpg). Verified: shasum of the file equals its name.
      So an evidence reference resolves by string match on the name — no
      hashing needed, and no prefix matching either. Use all 64 characters.

* Resolve each reference back to an image ENTRY in {HIERARCHY_FILE}, in this
  precedence order:
    1. IPFS CID in the reference -> the cid index built in Stage 3. Exact.
       This is the majority path — 62% of references — so Stage 3 MUST have
       completed. If the cid index is empty, stop; do not proceed with an
       unpopulated index and then report that nothing resolved.
       Normalise both sides before comparing (a page may carry the v1 base32
       form of a CID stored as v0): `ipfs cid base32` on each.
    2. Evidence filename -> the 64-hex basename IS the sha256 -> match the
       entry's sha256. Exact.
    3. Any other local static file -> sha256 the file on disk -> match the
       entry's sha256. Exact.
    4. Filename match against file_path basenames. AMBIGUOUS — a basename can
       collide. Only accept when it resolves to exactly one entry; otherwise
       leave it for the judgment pass below and report it.
* Append the referencing page's tilde-rooted path to that entry's on_pages.
  Deduplicate: a page that embeds the same image five times is recorded once.
  Sort each list so reruns produce a stable file.
* Every page path written must exist on disk — stat it before writing, the
  same discipline Stage 11 uses. A recorded page that has vanished is removed
  and reported, not carried.

UNRESOLVED REFERENCES ARE A FINDING, NOT A DROP.

Seven references currently resolve to nothing because the asset is a site-only
illustration with no mirror original and no sha-encoded name:

    site/docs/Fix/overview.mdx                        /img/All_Laws.jpeg
    site/docs/laws/explain/all/overview.mdx           /img/All_Laws.jpeg
    site/docs/Iran/overview.mdx                       /img/Iran_Timeline.jpeg
    site/docs/Timeline/overview.mdx                   /img/Timeline_Israel.jpeg
    site/docs/Israel/overview.mdx                     /img/Timeline_Israel.jpeg
    site/docs/court/mirandize/mirandized-sept-11-image.mdx
                                       /court/mirandize/Mirandized_Sept_11_.png
    site/docs/court/mirandize/sept-11-grok-image.mdx
                                       /court/mirandize/Sept_11_Grok.png

These are real published images and belong in the corpus. Hand them to Stage 7's
rule for site-only assets: sha256 the file on disk, create an image entry whose
file_path is the static file, park it under the level_3/level_4 matching the
page it appears on, and then bind on_pages here. Do not leave a published image
absent from the YAML just because it never came from the mirror.

SCOPE RULE — what does NOT go in on_pages.

  * Pages under {DOCS_DIR}/Photos. Those are the images Level 2 itself. The
    image's own Level 5 page belongs in image_page, and a Photos cluster
    overview page listing its children is structure, not an outside reference.
    Note the Photos pages carry ~1,600 of their own <img> references — if a
    sweep reports thousands of bindings, the Photos exclusion filter is
    leaking. Verify the filter on the actual path strings: a list produced by
    `grep -rl ... .` may or may not carry a leading `./`, and a filter written
    for the wrong one silently passes every Photos page through. Assert that
    zero recorded paths contain /docs/Photos/ before writing.
  * Files in {THIS_DIR} (planning layer), {GENERATOR_DIR} scripts,
    {HIERARCHY_FILE} itself, and {PAGES_CSV}. Those reference images as data,
    not as a page showing them.
  * Anything outside {ROOT_DIR}.

SANITY GATES — run all of these before writing, and fail on any breach.

  1. Extractor calibration. Sweep non-Photos docs and count references. History,
     newest last: 6 refs at HEAD~150, 75 at HEAD~60, 83 at HEAD~20, 123 on
     2026-07-23 morning, and 318 refs across 120 pages on 2026-07-23 evening
     (the jump is the multi-line-aware extractor plus markdown ![](...) forms
     the earlier count did not see, not a sudden site change). Nothing has ever
     been removed. So a run that finds substantially FEWER than the last
     recorded count has a broken extractor, not a shrunken site. Record the
     count each run so the next run can compare.
     Of those 318 refs the corpus-resolvable ones produce 176 bindings on 148
     entries — that ratio (roughly one binding per two references, since a page
     often shows the same image twice and many refs are external http) is itself
     a calibration signal.
  2. Cross-check against a naive page-level count: `grep -l '<img'` over
     non-Photos docs gives the number of pages that contain at least one tag.
     The multi-line extractor must find a reference on EVERY one of those
     pages. A page in the grep list with zero extracted references is an
     extractor failure — list it and fix the pattern.
  3. Every binding is re-verified by reopening the page and confirming the
     reference is present in its text. Bindings that fail are dropped and
     counted. This gate alone would have caught all 946 fabricated bindings.
  4. Zero recorded paths under /docs/Photos/. Zero recorded paths that do not
     exist on disk. Zero duplicate paths within one entry's list.
  5. Total bindings must be within the same order of magnitude as resolvable
     references. 102 resolvable references cannot yield 1,056 bindings.

PARALLELISM — dividing the repo across agents.

The mechanical extraction above should be scripted; a script reads each file
once and is exact, and this stage is small enough (about 1,500 non-Photos
pages) that one script does the whole sweep in seconds. Use parallel agents
only for the RESIDUAL — references the script could not resolve mechanically
(ambiguous basenames, relative paths needing page-context resolution, images
behind a component indirection, hand-written embeds with no recognisable asset
path).

* Partition the repo's directories recursively across 12 agents. Map whole
  directories to agents — never split a directory across two agents, so no
  file is read twice and no file is missed. Balance by total file count, not
  directory count.
* Each agent walks only its assigned directories, opens each unresolved file
  once, and returns a flat list of (page_path, resolved_sha256_or_cid,
  verbatim_matched_text) rows. The verbatim matched text is mandatory — it is
  the evidence, and the writer re-checks it against the page before accepting
  the row. An agent row without a verbatim match is rejected and counted.
  Agents do NOT edit {HIERARCHY_FILE} — they report, and a single writer
  merges. Concurrent writers to one YAML file would corrupt it.
* Merge all agent output plus the scripted output into the YAML in one write.

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

For EVERY IMAGE entry in {HIERARCHY_FILE} (old and new). Legacy video entries
are skipped and counted — MEDIA-TYPE SCOPE:

* Compute the expected sidecar paths using the mapping learned in Stage 2:
    original under {MIRROR_DIR}       →  {MIRROR_SIDECAR_DIR}/<same relative
                                          path>/<name.ext>.<sidecar>
    original inside {ROOT_DIR}        →  {REPO_SIDECAR_DIR}/<repo-relative
                                          path>/<name.ext>.<sidecar>
    check the legacy .lfbridge/_Mirror/ location as fallback
* Set on each entry:
    ai_description_file   path if the file exists, else ""
    ocr_file              path if the file exists, else ""
    transcription_file    path if the file exists, else ""
* Where the inline ai_description text is empty and an .ai_description
  sidecar exists, fill the inline field with the sidecar's Overview
  paragraph, collapsed to a single paragraph (the readDesc() convention in
  gen_hierarchy.js shows exactly how).
* Do not overwrite a non-empty inline ai_description.

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

KNOWLEDGE — what an image page is.

Under the images Level 2 ({DOCS_DIR}/Photos) the site publishes one page per
image. That page hosts a single image and nothing else: the image itself, a
title, and prose describing what the image shows and why it matters to the
investigation. We call it the IMAGE PAGE, or the Level 5 page. It is the leaf
of the published hierarchy, the same way an image entry is the leaf of this
YAML.

  Photos                       ← site Level 2 (the images landing page)
    Maps                       ← site Level 3  (a cluster overview page)
      Img_Photo_cf0c99.mdx     ← the IMAGE PAGE — one image, its description

These pages already exist on disk — about 1,100+ of them, generated by
{GENERATOR_DIR}/gen_photos_pages.py from this YAML. This stage does NOT create
them, rename them, or edit them. It READS them and records where each one is,
so the YAML can find its published page later. Reading site pages is allowed;
the no-page-modification hard rule still holds.

THE PROPERTY.

Every image entry gets an `image_page` property whose value is the FULL PATH
FROM ~ to that image's Level 5 page under the images directory:

    image_page: "~/BGit/Bryan_git/charlie-kirk/site/docs/Photos/Maps/Img_Photo_cf0c99.mdx"

Not the URL, not a repo-relative path — the tilde-rooted filesystem path, the
same convention file_path and the sidecar path properties already use. An
entry whose image has no page yet gets image_page: "" (empty string, key still
present).

HOW TO MATCH AN ENTRY TO ITS PAGE.

Each generated image page carries the binding in its frontmatter:

    ck_image_sha256: cf0c994cfd5c6ba50dd08f272f073ceddb0471dcfa7130bf511e874cfa2a5bac
    ck_node_key: Maps

  * Walk every .mdx under {DOCS_DIR}/Photos and index the ones that declare
    ck_image_sha256 — key the index by (ck_image_sha256, ck_node_key).
  * For each image entry in {HIERARCHY_FILE}, look up (its sha256, the _key of
    the node it sits under). That pair is the exact match: it is what makes
    cross-filed images work, since the SAME sha256 legitimately appears under
    several nodes and each of those nodes publishes its own page for it.
  * If the exact pair is not found, fall back to sha256 alone. If that yields
    exactly one page, use it. If it yields several, choose the page whose
    ck_node_key is nearest in the tree (same parent first, then same level_3
    subtree), and leave the others alone.
  * If no page carries that sha256 at all, set image_page: "".
  * Some pages are hand-written or predate the sha256 frontmatter and carry no
    ck_image_sha256. Do not try to guess them by filename. Count them and
    report them; they resolve on a later pass once the page generator restamps
    them.

RULES.

  * image_page is set on EVERY image entry — the existing ones and any added
    by earlier stages. No entry is left without the key.
  * A legacy VIDEO entry never receives an image_page. Leave it "", count it,
    and report it. There is no video page under {DOCS_DIR}/Photos to bind to;
    a video's page lives under {VIDEOS_L2_DIR} and is recorded in
    {VIDEO_HIERARCHY_FILE}'s own video_page property, not here.
  * If a page under {DOCS_DIR}/Photos is found to contain a `<video>` or
    `<source>` element, it is a published video page in the wrong hierarchy.
    Do not bind anything to it. List it under the hand-off heading in
    {FINDINGS_FILE} and report the count. Nine such pages exist today, all
    under {DOCS_DIR}/Photos/Official_Narrative/Narrative_Shot_in_the_Heart/.
  * Never invent a path. The file must exist on disk at the moment you write
    the value; verify existence before writing, and write "" if it does not.
  * Never write a page path that lives outside {DOCS_DIR}/Photos. Ad-hoc
    embeds on topic pages elsewhere in the site belong in on_pages, not
    here. The two properties answer different questions: on_pages is
    "where else does this image appear," image_page is "which page IS this
    image."
  * image_page is an IDENTITY field for sanitization purposes — see the
    OUTPUT SANITIZATION section. It must keep resolving to the real file, so
    any non-ASCII in it is emitted as a visible \uXXXX escape, never replaced.
  * Never delete an existing non-empty image_page in favour of "". If a
    previously recorded page has vanished from disk, report it rather than
    silently clearing it.
  * A BANNED ENTRY GETS NO image_page. banned: true means there is no Level 5
    page for that image and there never will be while the ban stands, so the
    field is "". Two cases, handled differently:
      - No page exists → write "" and move on. Normal.
      - A page DOES exist on disk carrying that sha256 → it is a page that
        should not be there. Do NOT bind it, do NOT delete it (this prompt never
        touches a page). Write "" and REPORT it loudly, listing the page path,
        the served copy's path if one exists, and the ban reason, so
        {THIS_DIR}/p_yaml_to_site.md removes both on its next run. Count these
        separately — a non-zero number means banned material is live right now.
    The "never clear a non-empty image_page" rule above does not apply to a
    banned entry: clearing it is the correct action, not a regression.

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

KNOWLEDGE — what should_be_on_pages answers.

Stage 8 recorded where an image IS shown today. This stage records where it
SHOULD be shown — the plan. It is the one property in the file that is
reasoned rather than observed: nothing on disk tells you the answer, you work
it out from what the image depicts and what each page is about.

Why it exists: most evidence images in this corpus are published nowhere but
their own Level 5 image page. A reader deep in the Ballistics section or the
Spy Plane section should SEE the evidence for that topic on the page they are
reading, not have to go find it under Photos. This property is the worklist a
later publishing prompt consumes to place images onto topic pages.

Relationship to the other two properties:

  should_be_on_pages ⊇ on_pages

  Every page already in on_pages is repeated in should_be_on_pages unless the
  image genuinely does not belong there (a wrong placement made by an earlier
  pass). The set difference — should_be_on_pages minus on_pages — is exactly
  the work still to do. Never treat should_be_on_pages as "additional pages
  beyond on_pages"; it is the complete desired state.

  THIS UNION IS WHY STAGE 8 MUST RUN FIRST AND MUST BE CLEAN. Stage 8's last
  output carried 946 fabricated bindings (89% of its total). Unioning those
  into should_be_on_pages would convert every fabricated observation into a
  fabricated publishing instruction, and the next prompt would act on it.
  Before unioning, confirm Stage 8 reported zero unverified bindings. If
  Stage 8 did not run in this session, re-verify each on_pages entry by
  reopening the page rather than trusting the file.

WHAT IS ELIGIBLE. Still images only. A legacy video entry is skipped: it gets
no new should_be_on_pages placement, and any placement a previous run put on
one is reported rather than acted on. Planning a video onto a topic page from
here would have the publishing prompt embed a video off a /Photos-scoped
identity, which is the same defect one layer further downstream. Nine of the
`image:` entries in the file today are in fact .mp4s and already carry a
should_be_on_pages row each — see MEDIA-TYPE SCOPE.

THE PROPERTY SHAPE.

Identical in shape to on_pages: a LIST OF MAPPINGS, each with a single `page:`
key holding the full path from ~ to the page file.

    should_be_on_pages:
      - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/Gun_Bullet/overview.mdx"
      - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/Gun_Bullet/trajectory-analysis.mdx"

Not a flat list of strings. Not repo-relative. Not URLs. Every image entry
carries the key; an image that belongs on no topic page emits:

    should_be_on_pages: []

EVERY PATH MUST BE REAL, FULL, AND VERIFIED — NO PLACEHOLDERS.

This is the rule that matters most in this stage, because the value is
reasoned rather than read off disk, which makes it the one place a plausible
but fictional path can slip in. A path here is only ever COPIED from a real
row of {PAGES_CSV} or from a real filesystem walk of {DOCS_DIR}. It is never
composed, guessed, abbreviated, or typed from memory of what a page is
probably called.

  * FORBIDDEN, and a hard failure if any of these reach the file:
      - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/....mdx"
      - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/FBI/....mdx"
      - page: ".../site/docs/FBI/overview.mdx"
      - page: "site/docs/FBI/overview.mdx"            (repo-relative)
      - page: "/FBI/overview"                          (a URL path)
      - page: "~/.../charlie-kirk/site/docs/FBI/coverup.mdx"  (invented file)
    Any value containing an ellipsis, "...", "TODO", "TBD", "<", ">", or any
    other placeholder token is invalid. Any value that is not an absolute
    tilde-rooted path ending in .md or .mdx is invalid.

  * THE ONLY LEGAL WAY TO PRODUCE A VALUE. Build a candidate index once, up
    front, and select from it. Nothing outside the index may ever be written:
      1. Read {PAGES_CSV}. Its file_path column is repo-relative
         (site/docs/FBI/overview.mdx). Expand each to
         {ROOT_DIR}/<file_path> in tilde-rooted form.
      2. Walk {DOCS_DIR} for every .md/.mdx on disk. Union it with the CSV set
         — the CSV can lag, the filesystem is what actually exists.
      3. stat() every candidate. Drop any that does not exist. Keep the
         surviving set as THE candidate index, keyed by its tilde-rooted path.
      4. Every value written to should_be_on_pages must be a key of that
         index, byte for byte. Selecting a page means selecting an index key —
         there is no code path that constructs a string.

  * VERIFY BEFORE WRITE, then VERIFY AFTER WRITE. Before emitting, re-stat
    every path in every should_be_on_pages list. After emitting, re-parse the
    YAML, expanduser every should_be_on_pages page value, and stat it again.
    If any single path does not resolve to an existing file, the stage FAILS —
    do not write a partial file with bad paths, do not "best effort" it, and
    do not degrade a bad path to "". Fix the selection and re-emit.

  * Never invent a page because the image obviously deserves one. If the right
    page does not exist yet, that is a finding, not a path: record it in the
    stage's stdout report under "Wanted pages that do not exist" with the
    image's sha256 and a suggested title, and leave the image's
    should_be_on_pages holding only the real pages that do exist. Page
    creation is a later prompt's job.

HOW TO DECIDE WHICH PAGES AN IMAGE BELONGS ON.

Inputs to the decision, in order of weight:

  1. The image's ai_description (what is SEEN) and its .ocr text (what it SAYS
     on screen). Read the sidecar files, not just the truncated inline prose —
     the OCR in particular names people, dates, tail numbers, case numbers,
     and headlines that pin an image to a specific page.
  2. The YAML node the image already sits under — its _key and title are the
     concept cluster it was filed into, and that cluster's site_level_2 /
     site_page properties (set in Stages 4 and 6) already point at the site
     pages for that concept. This is usually the strongest single signal and
     the cheapest: an image under the level_4 whose site_page is
     site/docs/Planes/N1098L.mdx almost certainly should_be_on that page.
  3. The mirror directory the original file sits in ({MIRROR_DIR}/<dir>) —
     years of manual filing by concept.
  4. {PAGES_CSV} columns: title, description, page_type, level, level2_section
     and url_path. The description column is a one-sentence summary of what
     the page covers — it is the best cheap matcher against an image
     description. page_type (person / organization / topic / index / …) tells
     you whether a page is about a PERSON, in which case the image should
     depict that person, not merely mention them.
  5. {CK_FILE} arbitrates when the description and the cluster disagree about
     which investigative thread an image really belongs to.

Targeting rules:

  * Aim at Level 3 pages — the specific analysis pages inside a section. That
    is where evidence images do their work. Level 4 pages are equally good
    when the concept lives that deep.
  * Level 2 overview pages get an image only when it is emblematic of the
    whole section — a headline image a reader landing cold should see. Expect
    this to be rare: at most one or two images per Level 2 overview.
  * NEVER target a page under {DOCS_DIR}/Photos. That whole Level 2 is the
    image hierarchy itself; an image's own page there is image_page, and
    cluster overviews there are structure. Same exclusions as Stage 8's scope
    rule: nothing in {THIS_DIR}, nothing in {GENERATOR_DIR}, not
    {HIERARCHY_FILE}, not {PAGES_CSV}, nothing outside {ROOT_DIR}.
  * Do not target Topics3 scaffolding pages.

Quantity rules:

  * One to three pages per image is the norm. Five is the ceiling. An image
    that seems to belong on ten pages is a generic image (a logo, a stock
    portrait, a map with no annotation) — give it the one or two pages where
    it is actually evidence, not every page it could decorate.
  * Many images belong on zero topic pages. [] is a correct and common answer.
    Do not pad. A weak topical match is worse than none: it puts an
    unexplained image on a page and makes the page look padded.
  * Per-page load: no page should be assigned more than 12 images across the
    whole corpus. After the full pass, count assignments per page; for any
    page over 12, keep the strongest 12 by match quality and report the rest
    as overflow (they are candidates for a new child page — report them under
    "Wanted pages that do not exist").

DEFAMATION GATE — applies before any page is added.

should_be_on_pages is a publishing instruction, so the repo's defamation rules
bind here even though this stage writes no page:

  * AN ENTRY WITH banned: true IS SKIPPED ENTIRELY. Emit should_be_on_pages: []
    for it, unconditionally, regardless of how good the topical match is, and do
    not spend scoring on it — filter banned entries out before the scorer runs.
    If it previously held pages, CLEAR them and report each cleared page; this
    is the one property where clearing is the correct action.
    The union-with-on_pages rule is deliberately broken for banned entries: an
    on_pages value on a banned image is a list of pages the image must be
    REMOVED from, not pages it should stay on. Unioning them would convert a ban
    into an instruction to publish it more widely. Report every banned entry
    with a non-empty on_pages as a REMOVAL WORKLIST, page by page with the ban
    reason, and leave on_pages itself untouched — it is the observation that
    drives the removal.
    Nothing links into a banned image from anywhere: no card, no thumbnail, no
    table-of-contents row, no "see also". There is no Level 5 page to link to,
    so any link that exists is broken as well as unwanted.
  * An image whose sha256 appears in {EXCLUDE_FILE} is never assigned to any
    page. Same treatment: should_be_on_pages: [], unconditionally. The ban set
    is the UNION of {BAN_IMAGES_CSV} and {EXCLUDE_FILE}, minus any CSV row
    explicitly marked banned=false.
  * An image showing a named living person is assigned only to pages where
    that person's presence is the point. Do not assign an image whose visible
    content (including its OCR text) makes an accusation against a living
    person — those stay private until cropped.
  * When unsure, leave it out and note it.

ACCEPTANCE TARGETS — the run is not done until these hold.

Measure them over ALL image entries (not just the planned ones) after the write,
and print the table. A run that misses any of them is retuned, not shipped:

    should_be_on_pages empty []              >= 5%   and <= 15%
    should_be_on_pages with >= 1 page        >= 85%
    should_be_on_pages with >= 2 pages       >= 20%
    should_be_on_pages with >= 3 pages       >= 20%
    on_pages empty []                        < 100%  (all-empty means broken)

The empty floor matters as much as the ceiling: [] is the correct answer for an
image that genuinely belongs on no topic page, and a run that assigns everything
has stopped discriminating. The on_pages check is only a liveness test — that
property is observed, so it is legitimately ~90% empty and must never be tuned
toward these numbers.

Run of 2026-07-23 landed at 11.6% / 88.4% / 58.0% / 36.5%, on_pages 91.5% empty.

HOW TO RUN IT.

  * The candidate index (pages.csv + filesystem walk + stat) and the mechanical
    filters (the ban set — {BAN_IMAGES_CSV} plus {EXCLUDE_FILE} — Photos-scope
    exclusion, per-page load counts)
    are scripted — they are exact and cheap.
  * The selection itself runs scripted too, via
    {GENERATOR_DIR}/plan_should_be.py plan. It scores every image against every
    candidate page over the same evidence a human would read — the
    .ai_description (what is SEEN), the .ocr text (what it SAYS on screen), the
    concept cluster the image was filed into, and the mirror directory — against
    each page's title, description, url path and section. Scripted selection is
    reproducible and auditable: every assignment traces to a score and the whole
    pass re-runs identically, which judgment does not.
  * Scoring rules that were learned the hard way and must not be dropped:
      - drop bare digit runs from the token stream. An OCR'd Flightradar24 list
        or Google Trends chart is mostly dates, times and altitudes; those score
        high on IDF, mean nothing, and against a short page vector one shared
        number decides the match.
      - sublinear term frequency (1 + log tf) on the image side. Raw tf let an
        airport code repeated eleven times in a flight list outrank everything
        the image was actually about.
      - title-match bonus. A distinctive token (idf >= 4) shared between the
        image and the page TITLE is the strongest signal available — without it
        a tail-number screenshot ranked an @-handle page above the eight pages
        literally named after that tail number.
      - structural prior PROPORTIONAL to the entry's own best score (0.75x for
        the nearest ancestor node's site_page, 0.35x for further ancestors). A
        flat bonus is noise next to cosine scores of 20-40.
      - person gate: a page_type=person page needs the WHOLE name present, not
        any one token. A folder named Blake_Harruff otherwise admits blake-neff
        and blake-bednarz alongside the right page.
      - selection cutoff: keep candidates scoring >= 0.74 of the entry's best
        (CK_REL_KEEP overrides). Tune this knob, and only this knob, to land the
        acceptance targets — it is the one parameter the distribution turns on.
  * MEASURED PRECISION, so nobody over-trusts the numbers: hand-auditing 20
    random assignments across two passes put topical precision near 65-70%. The
    strong cases are exact — a named person, a tail number, a case number, a
    document. The weak cases are generic geography: a Flightradar or Google Maps
    screenshot whose description is just "Orem, Utah, Utah Lake" matches any page
    that names the same ground. Lexical matching cannot fix that; it has no idea
    which investigative thread the map belongs to.
  * OPTIONAL JUDGMENT PASS, for when that precision is not good enough. The
    script's `build` subcommand writes 12 shortlist slices to /tmp/ck_stage11,
    each entry carrying its description, OCR and its ~12 scored candidates.
    Partition those slices across 12 parallel agents; each returns rows of
    (sha256, node_key, selected_index_key, confidence, one-line reason) and
    selects an EXISTING index key. An agent returning a path not in the
    candidate index has its row REJECTED and counted — it does not reach the
    file. Agents do NOT edit {HIERARCHY_FILE}; `plan_should_be.py write` is the
    single writer that merges. Concurrent writers corrupt it. Do not launch this
    pass without asking first — it is twelve agents over ~1,700 entries and it
    costs real money.
  * The writer applies the quantity and defamation rules, unions in every page
    already present in on_pages, dedupes, sorts each list, re-stats every path,
    and writes once.

RULES.

  * should_be_on_pages is set on EVERY image entry — no entry is left without
    the key. Empty is [], never "" and never a missing key.
  * Grow, do not clobber. An existing non-empty should_be_on_pages from an
    earlier run is merged with this run's selections, not replaced. Remove an
    existing entry only when the page no longer exists on disk, and report
    every such removal.
  * Page values are IDENTITY fields for sanitization — see the OUTPUT
    SANITIZATION section. Non-ASCII is emitted as a visible \uXXXX escape,
    never replaced, so the path keeps resolving.

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

The emitted {HIERARCHY_FILE} must NEVER contain invisible Unicode characters.
Invisible characters (zero-width spaces, bidi controls, no-break spaces,
word joiners, BOMs, control characters, variation selectors, tag characters)
are a security problem: they can hide content from review, spoof strings,
and smuggle instructions past a human reading the file. Every byte of the
emitted YAML must be visible in a text editor.

The invisible set includes at minimum: U+0000-U+0008, U+000B-U+001F, U+007F-
U+009F, U+00A0, U+00AD, U+034F, U+061C, U+115F, U+1160, U+17B4, U+17B5,
U+180B-U+180E, U+2000-U+200F, U+2028-U+202F (U+202F NARROW NO-BREAK SPACE is
the one macOS puts in screenshot filenames before "AM/PM" — it WILL appear in
the inputs), U+205F-U+206F, U+3000, U+3164, U+FE00-U+FE0F, U+FEFF, U+FFA0,
U+FFF9-U+FFFB, and U+E0000-U+E007F.

Two different treatments, chosen by field kind:

  * PROSE fields (title, ai_description) — sanitize the CONTENT: replace
    space-like invisibles (U+00A0, U+2000-U+200A, U+202F, U+205F, U+3000)
    with a regular space, DELETE zero-width/bidi/control/joiner characters
    outright, then collapse runs of whitespace. Visible non-ASCII (em dashes,
    accented letters) may stay — they are visible and harmless.

  * IDENTITY fields (file_path, ai_description_file, ocr_file,
    transcription_file, image_page, ipfs_url, on_pages page values,
    should_be_on_pages page values, cid, also_filed_in,
    site_page, site_level_2) — the value
    must keep matching the real file on disk, so the characters cannot be
    replaced. Instead emit them as visible ASCII escapes inside YAML
    double-quoted scalars (U+202F becomes the six visible characters backslash-u-2-0-2-F, i.e. "\u202F"). The parsed value is unchanged and still resolves the file; the
    file bytes contain nothing invisible. Escape ALL non-ASCII in identity
    fields this way.

MANDATORY validation after every emit: re-scan the written file and hard-fail
if any code point from the invisible set remains anywhere in it. Also
re-parse the YAML and spot-check that an escaped file_path still resolves to
an existing file on disk.

============================
STAGE 12 — COUNTS, NEEDS_SPLIT, INTEGRITY
============================

* Recompute number_of_images (direct) and number_of_images_recursive
  (subtree) on every node. They must be accurate.
* Re-evaluate needs_split on every node: over 12 direct images → true (six
  is the target, twelve the ceiling; over twelve means the node is not one
  concept and gets split one level deeper on a later pass). At or under 12 →
  remove the flag.
* Verify every _key is unique across the whole file.
* Verify no node contains the same sha256 twice. Same sha256 under DIFFERENT
  nodes is legitimate cross-filing — keep it, and keep also_filed_in
  accurate.
* Verify the YAML parses (e.g. python3 -c "import yaml,sys;
  yaml.safe_load(open(sys.argv[1]))" {HIERARCHY_FILE} — or any equivalent).
* Verify every image entry carries the full property set — cid, ipfs_pinned,
  sha256,
  file_path, ai_description, ai_description_file, ocr_file,
  transcription_file, banned, image_page, on_pages, should_be_on_pages — with
  "" standing in for any scalar that has no value, [] for the empty lists, and
  false for the booleans. No key is ever missing.
* Verify banned holds a real boolean on every entry — not null, not the string
  "true", not missing. Any failure is a hard fail.
* Verify the banned values still agree with {BAN_IMAGES_CSV} as it stands right
  now. Re-read the CSV here rather than trusting that Stage 3B ran; the CSV may
  have been edited mid-run, and this is the last cheap chance to catch it.
* Verify no banned entry has a non-empty should_be_on_pages and none has a
  non-empty image_page. Both counts must be 0. A banned image with a planned
  placement or a bound Level 5 page is the exact failure this gate exists to
  prevent.
* Verify every non-empty image_page resolves to a file that exists on disk
  and lives under {DOCS_DIR}/Photos.
* Verify every should_be_on_pages page value: it is an absolute tilde-rooted
  path, it ends in .md or .mdx, it resolves to a file that EXISTS on disk, it
  lives under {DOCS_DIR}, and it does NOT live under {DOCS_DIR}/Photos. Grep
  the emitted file for placeholder tokens — "...", "TODO", "TBD", "<", ">" —
  inside any page value and hard-fail on a hit. There is no tolerance here: a
  single unresolvable or placeholder path fails the stage.
* Verify on_pages ⊆ should_be_on_pages on every entry, or the entry is
  reported as a deliberate de-placement.
* Verify EVERY on_pages binding against the page's actual bytes: open the
  page, confirm a reference resolving to that image is present. Report the
  count verified and hard-fail if any binding cannot be substantiated — this
  is the check that catches the fabricated-binding failure mode. Also confirm
  no on_pages path lies under {DOCS_DIR}/Photos and every one exists on disk.
* Sanity-check the binding total against the reference total: bindings can
  exceed resolvable references only by the amount of legitimate multi-page
  reuse. A ratio above ~2x means fabrication has crept back in.
* Run the OUTPUT SANITIZATION validation: scan the emitted file for every
  code point in the invisible set and fail hard if any is found. Confirm at
  least one escaped file_path round-trips: parse the YAML, expanduser the
  path, and check the file exists.

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

* Confirm every non-excluded site Level 2 maps to exactly one level_3
  (site_level_2 property present).
* Confirm the Other level_3 exists.
* Confirm every home-page TOC concept resolves to a level_3.
* Confirm every page found with images in Stage 7 has its images reachable in
  the YAML (spot-check 10 pages).
* Spot-check 10 should_be_on_pages assignments by hand: open the page and read
  the image's description, and confirm the image genuinely belongs there.
  Confirm each of those 10 paths opens a real file. A placement that reads as
  padding is a signal the whole pass was too loose — report it.
* Confirm no pre-existing node or image entry was removed: the file only
  grows. Diff the node count and image count against Stage 1's index.
  on_pages bindings are the one exception; account for every removal.
* Independent re-derivation of on_pages. Do not re-run Stage 8's script.
  Write a SECOND, independent extractor (different author, different
  approach — e.g. an HTML/JSX parse rather than a regex) over the non-Photos
  docs, and diff its page-to-image set against what the YAML now holds. They
  must agree. Two implementations agreeing is the only real defence against a
  systematic extraction bug, and every failure this stage has had so far was
  systematic: one regex that could not see multi-line tags, one migration
  that imported guesses as facts.
* MEDIA-TYPE AUDIT — this run added no video. Assert all four and fail the
  run on any of them:
    - Zero `video:` items were added this run. The count of `video:` items in
      the file is <= the count Stage 1 indexed.
    - Zero `image:` entries were added this run whose src, file_path, or CID
      types as video under the four-step test in MEDIA-TYPE SCOPE.
    - No entry of either kind gained an image_page, on_pages, sidecar path,
      or should_be_on_pages this run if it types as video.
    - No path written anywhere in the file this run points under
      {VIDEOS_L2_DIR}, {VIDEOS_DIR}, or {VIDEO_PLANNING_DIR}.
  Re-type from the reference, not from which YAML array the entry sits in —
  the 9 known contaminated entries are in `images:` arrays, so an audit that
  only counts `video:` items reports a clean run on a dirty file.
* Print a final tree summary: each level_3 _key with its recursive image
  count and child count.

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

* IMAGES ONLY. This pipeline never harvests, enriches, binds, or plans a
  video, and never writes a path under {VIDEOS_L2_DIR}, {VIDEOS_DIR}, or
  {VIDEO_PLANNING_DIR}. Every media reference is typed at harvest time by the
  four-step test in MEDIA-TYPE SCOPE, and anything that is not a still image
  is counted, handed off to {FINDINGS_FILE}, and dropped. UNKNOWN is not
  treated as image. Video belongs to {VIDEO_HIERARCHY_FILE} and publishes to
  {VIDEOS_L2_DIR}.
* {HIERARCHY_FILE} only grows. Never delete a node or an image entry. No
  duplicates — existing items get their properties updated in place.
* SECOND CARVE-OUT: legacy video entries. They are contamination from an
  earlier revision of this prompt, they are never added to and never enriched,
  and they are never silently deleted either — they are counted, listed, and
  handed off. Removing them and un-publishing the /Photos pages they produced
  is a separate, explicitly-approved job, sequenced after the same content
  lands under {VIDEOS_L2_DIR}.
* ONE CARVE-OUT: on_pages. It is rebuilt from observation on every run and
  bindings that observation does not support are deleted and reported (see
  Stage 8). A false binding is a factual error about a file's contents, not
  data, and it propagates into should_be_on_pages and then into published
  pages. Nothing else in the file is ever deleted, and on_pages is never
  blanked wholesale — a run that resolves implausibly few references must
  fail instead of writing.
* on_pages is OBSERVED, should_be_on_pages is REASONED. Never let topical
  judgment write a binding into on_pages. That single confusion is what
  corrupted 89% of the property's contents. The ONE exception to the
  superset rule is a banned entry: it gets should_be_on_pages: [] and its
  on_pages is a removal worklist, never a source of placements.
* banned IS COPIED DOWN, NEVER DECIDED HERE. {BAN_IMAGES_CSV} is the master and
  the repo charter ({ROOT_DIR}/claude.md, "Banned Media") owns the contract.
  Stage 3B is the only stage that writes the key; every other stage reads it.
  Every entry carries it as a real boolean and the default is false. A banned
  image gets no Level 5 page, no served copy under the static evidence
  directory, no placement on any page, no link into it from anywhere, and is
  never pinned — and its entry is never deleted from {HIERARCHY_FILE}, because
  banning is a publish-time gate over a file that only grows. When a run finds
  material that should not be public, add the row to {BAN_IMAGES_CSV} with a
  reason before the run ends.
* This prompt does not create, move, or edit any page under {SITE_DIR}, does
  not touch {SITE_DIR}/sidebars.ts, and does not modify {PAGES_CSV}. The
  YAML is the plan; publishing is a later prompt.
* Do not put Docusaurus pages in {THIS_DIR} and do not put planning notes in
  {SITE_DIR}/docs/Photos/.
* _key uniqueness is file-wide and _keys are the future page_keys — treat
  them like database primary keys. Keys are ASCII-only by construction.
* {HIERARCHY_FILE} must never contain invisible Unicode characters — see the
  OUTPUT SANITIZATION section. Prose is cleaned; identity fields (paths,
  URLs) are emitted with visible \uXXXX escapes; every emit is followed by
  the invisible-character validation scan. This is a security rule, not a
  style rule.
* Every page path written anywhere in {HIERARCHY_FILE} — image_page, on_pages,
  should_be_on_pages — is an absolute tilde-rooted path to a file that EXISTS
  on disk at the moment it is written, selected from a stat()-verified
  candidate index, never composed or guessed. Placeholders ("...", "TODO",
  "<page>") are a hard failure, not a draft state. Paths are verified before
  the write and re-verified after it.
* Clusters are concept clusters, arbitrated by {CK_FILE}. The folder
  proposes, the description decides, {CK_FILE} arbitrates.
* When later prompts publish from this YAML, all public output follows the
  repo defamation rules (attribution language, no stating a living person
  committed a crime, accusations cropped out of images). Raw claims stay
  private in this planning layer or in {CK_FILE}.

============================
BACKGROUND — ORIGINAL DIRECTIVE, KNOWLEDGE PRESERVED
============================

This section preserves the full intent of the directive this prompt was built
from, so no knowledge is lost even where a stage above already encodes it.

* Growing and improving the output YAML file ({HIERARCHY_FILE}) is the goal.
  The prompt has multiple stages and is created to run later.
* "Level 2" refers to the fact that we will eventually put an image-hosted
  page for every image under a Level 2 directory called images. The Level 2
  IS that images directory. Today that is the Photos section.
* We create Level 3s under that images Level 2, and the YAML's level_3 list
  will definitely be a superset that includes the list of the website's
  Level 2s — except images and videos and any unfiltered or catch-all
  category — plus an "Other" entry included as a level_3. The website's
  Level 2s include TPUSA, FBI, UVU, and many more; one stage reads those
  Level 2s and makes sure they are all present as level_3s in the YAML.
* We then take every other Level 2 (outside the images Level 2) and its
  Level 3 pages, and make a level_4 in the YAML for each one, parented
  hierarchically under the appropriate parent.
* We create a level_5 per image: if some Level 3 content page has an image —
  one or more images on the page — we create level_5 YAML for each of those
  images. Where those level_5s are parented is on the level_4 in the YAML
  which correlates to the Level 3 page in the file system.
* We are effectively taking all the Level 2s, Level 3s, and Level 4s in the
  file system outside this YAML and reproducing the hierarchy in the YAML
  with the levels incremented by one: filesystem Level 2 → YAML level_3,
  filesystem Level 3 → YAML level_4, filesystem Level 4 → YAML level_5.
* A further stage goes through all the pages and makes sure that every page
  that has one or more images gets those added to the YAML hierarchy. No
  duplicates — it does not add them if they already exist, but it DOES
  update their YAML properties.
* Learn from the existing YAML file — its structure and conventions carry
  forward.
* These directories often hold the OCR text files, the transcription text
  files, and the AI-description text files:
    ~/BGit/act3/act3_large_files_bridge/
    ~/BGit/Bryan_git/personal_large_files_bridge/
  We want YAML properties for all of those: each image entry gets a property
  that is a file path to the sidecar file that correlates to it.
  [SUPERSEDED 2026-07-23: the original directive said "each image or video
  entry". Video is no longer in this pipeline's scope at all — see MEDIA-TYPE
  SCOPE. Video sidecars are filled in against {VIDEO_HIERARCHY_FILE} by the
  sibling pipeline. The historical wording is corrected here rather than left
  standing, because it is the sentence the video harvest was justified by.]
* By reading the product management specification files and the code in
  ~/BGit/Bryan_git/LargeFileBridge/ you learn how we map between the original
  file paths and the mirroring file system in the other place where the
  sidecars are stored. Learn that pattern and fill in those YAML properties.
* The YAML must be built into the most full and complete hierarchy possible.
  Look at the home page and its table of contents — there might be more than
  one table of contents there — and make sure all of those become level_3s
  in the YAML hierarchy too. That is likely to add more items than are found
  in the earlier stages. Never create dupes, but always look for more that
  can be added.
* The end goal: when we create our list-of-images page (the top level), it
  will be mostly a table of contents — a table with links into the images
  directory's Level 3 pages, which come from this YAML file's level_3s.
* There is a property called should_be_on_pages, a sub-hierarchy under each
  image alongside on_pages. It records which pages that image SHOULD go on —
  we go calculate that, it is not read off disk. Late in the run we look
  through the pages and, for every image, map that image to the several pages
  it should appear on: mostly Level 3s, sometimes Level 2s, always outside the
  Photos Level 2. {PAGES_CSV} is useful for deciding which pages an image
  should appear on. The values must be real, full, verified file paths — the
  four-dot form seen in the original sketch
  ("~/BGit/Bryan_git/charlie-kirk/site/docs/....mdx") was a PLACEHOLDER
  standing in for a real page path, never a value to emit.
* There is a property called image_page. These are the pages under the images
  Level 2 directory — the Level 5 pages that each host one image and carry the
  description of it. We add the full path from ~ to that Level 5 page as the
  image_page property on the image entry, so the YAML can find the published
  page for any image later. All YAML properties are kept updated on every
  image entry so everything is findable later — a property with no value is
  written as "" rather than dropped.
