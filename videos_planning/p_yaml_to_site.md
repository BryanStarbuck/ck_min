ROOT_DIR dir is ~/BGit/Bryan_git/charlie-kirk

THIS_DIR dir is {ROOT_DIR}/videos_planning
VIDEOS_DIR dir is {ROOT_DIR}/videos
HIERARCHY_FILE is file {VIDEOS_DIR}/videos.yaml
  (Created 2026-07-23 from images.yaml with only the SCHEMA converted; {HIERARCHY_PROMPT} replaces the data.
   See THE STALE-DATA PRECONDITION.)
VIDEO_MANIFEST is file {VIDEOS_DIR}/manifest.yaml
LAYOUT_GUIDELINES is file {THIS_DIR}/layout_guidelines.txt
CHARTER_FILE is file {THIS_DIR}/CLAUDE.md
EXCLUDE_FILE is file {THIS_DIR}/exclude_videos.txt
BAN_VIDEOS_CSV is file {VIDEOS_DIR}/ban_videos.csv
FINDINGS_FILE is file {THIS_DIR}/findings_for_hierarchy.md
HIERARCHY_PROMPT is file {THIS_DIR}/p_update_video_hierarchy.md
NAV_PROMPT is file {THIS_DIR}/p_level2_update.md

SITE_DIR dir is {ROOT_DIR}/site
DOCS_DIR dir is {SITE_DIR}/docs
VIDEOS_L2_DIR dir is {DOCS_DIR}/Videos
VIDEOS_L2_PAGE is file {VIDEOS_L2_DIR}/overview.mdx
POSTER_DIR dir is {SITE_DIR}/internals/static/img/video_posters
  NOT {SITE_DIR}/static: docusaurus.config.ts sets staticDirectories: ["internals/static"], the ONLY served dir. A
  poster written to {SITE_DIR}/static is silently unpublished. The page URL is still /img/video_posters/{sha256}.jpg.
VIDEO_LIST_CSV is file {DOCS_DIR}/video_list.csv
PAGES_CSV is file {ROOT_DIR}/pages.csv
CK_FILE is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt
  (Real file; {ROOT_DIR}/Charlie_Kirk.txt is a symlink to it. Read the real path. READ-ONLY.)
ASSESS_MANUAL is file {ROOT_DIR}/prompts/Assess_Manual.md

MIRROR_DIR dir is ~/_Mirror/Politics/Charlie_Kirk_Mi
MIRROR_SIDECAR_DIR dir is ~/BGit/Bryan_git/personal_large_files_bridge/_Mirror/Politics/Charlie_Kirk_Mi
REPO_SIDECAR_DIR dir is {ROOT_DIR}/.lfbridge

IMAGE_PLANNING_DIR dir is {ROOT_DIR}/image_planning

MAX_AGENTS is ... = 12

============================
SCOPE — VIDEOS ONLY, ADDITIVE ONLY
============================

Both boundaries have been crossed before (every file here descends from the images pipeline).

1. THE ONLY INPUT IS THE VIDEO CORPUS: {HIERARCHY_FILE} plus the sidecars, manifest and investigation files it points at.
  * DO NOT READ OR WRITE {ROOT_DIR}/images (incl. images.yaml) or {IMAGE_PLANNING_DIR} (prior-art job is done; reading
    invites its data and wording back; copying from it reverts this directory's conversion).
  * DO NOT WRITE {DOCS_DIR}/Photos or {SITE_DIR}/static/img/evidence.
  * Reading a .jpg, describing a still, or resolving a path under images/ means something is wrong: stop and report.

2. THIS PROMPT ADDS VIDEO; IT NEVER REMOVES OR CHANGES IMAGES. The images pipeline still runs on the same topic pages
   and stylesheet:
  * Never delete, move, resize, retarget, reorder or reword an image, <img>, gallery, caption, figure or image block.
  * Never touch a CK_PLACED_IMAGES block on a topic page, or the CK_EVIDENCE_LAYOUT / CK_PLACED_IMAGES blocks in
    {SITE_DIR}/internals/src/css/custom.css (foreign territory).
  * Every image on an edited page is still there after the run, byte-identical, same place.
Ours: CK_PLACED_VIDEOS (topic pages), CK_VIDEO_LAYOUT + CK_PLACED_VIDEOS (stylesheet). Outside our markers and
{VIDEOS_L2_DIR}, this prompt only ADDS (plus ban removals of video).

============================
GOAL
============================

Generate, and keep regenerating, the video pages of {VIDEOS_L2_DIR} (rooted at {VIDEOS_L2_PAGE}) from {HIERARCHY_FILE}
(cluster tree; per video cid, ipfs_pinned, sha256, file_path, ai_description, transcription_file, ai_description_file,
ocr_file, on_pages, should_be_on_pages, also_filed_in, node site_level_2 / site_page). READ the YAML, WRITE pages; never
edit the YAML's data.

Under {VIDEOS_L2_DIR}:
  * Cluster pages: one .mdx per published YAML node (navigation TOC of peers, children, video pages).
  * Video pages: one .mdx per video: one player plus an account of what the footage shows, who speaks, what they assert,
    how it connects.
Outside, on topic pages in {DOCS_DIR}:
  * Stage 5: inline copies (on_pages) get a link to their video page.
  * Stage 6: videos in should_be_on_pages not yet on the page get a CARD in a regenerated block at the bottom. This makes
    the plan real; without it footage stays invisible to readers who never open Videos.
Runs MANY times: read each existing page, rewrite against current YAML and {LAYOUT_GUIDELINES}. Idempotent.

============================
THE STALE-DATA PRECONDITION (CHECK THIS BEFORE WRITING A SINGLE PAGE)
============================

Run against unconverted image data, this prompt would publish ~1,700 "video" pages with no playable CID describing stills.
HARD STOP gate before Stage 1 (never publish "just the good ones"):
  * Entries whose file_path ends .jpg .jpeg .png .gif .webp .heic: above zero = STOP; tell the operator to run
    {HIERARCHY_PROMPT} (its Stage 6 rebuild) first.
  * Entries whose ai_description begins "This image": same.
  * Fewer than half the entries with a non-empty cid: STOP (not reconciled against {VIDEO_MANIFEST}).
Status 2026-07-23: PASSES (400 videos in 1,559 nodes, 0 image paths, 0 "This image", 372 of 400 with a CID). Still run it
every time; a later hierarchy pass could regress.

============================
EMPTY NODES ARE NOT PUBLISHED
============================

Of 1,559 nodes only ~170 have a video in their subtree; publishing all would add ~1,390 empty-maze pages and slow every build.
  * number_of_videos_recursive == 0 (RECOMPUTED from the tree, not the stored field): NO page, NO TOC entry, NO {PAGES_CSV}
    row, at every level.
  * A node with videos somewhere below is published even if it owns none directly (a real waypoint).
  * Existing pages for now-empty nodes are removed by the orphan sweep and counted.
  * Report the skipped-empty count every run (a big swing = the hierarchy moved).
Empty nodes stay in the YAML as the map of where footage could go.

============================
KNOWLEDGE — READ FIRST, IN THIS ORDER
============================

  1. {LAYOUT_GUIDELINES}: video-page standards; grows; OVERRIDES this prompt. First, every run.
  2. {CK_FILE}: source of truth; write-ups are grounded in it. 400K+ lines: the orchestrator loads headers plus sections for
     the clusters in play; each agent loads the sections for ITS clusters before writing.
  3. {CHARTER_FILE} (audience, levels, schema, hard rules).
  4. {ASSESS_MANUAL} (all pages must meet it).
  5. {HIERARCHY_FILE}: parse fully; index nodes (_key, title, depth, parent) and videos (cid, ipfs_pinned, sha256, file_path,
     sidecars, video_page, on_pages, should_be_on_pages, also_filed_in).
  6. {PAGES_CSV}: link targets; kept in sync.

============================
KNOWLEDGE — THE PAGE MODEL
============================

Level 2 = {VIDEOS_L2_PAGE} (url /Videos, left-bar "Videos"); level_3 nodes under it, then level_4, level_5; video pages hang
off their owning node.

  {VIDEOS_L2_DIR}/overview.mdx                        the Level 2 landing page
  {VIDEOS_L2_DIR}/{L3_key}/overview.mdx               level_3 cluster page
  {VIDEOS_L2_DIR}/{L3_key}/{L4_key}/overview.mdx      level_4 cluster page
  {VIDEOS_L2_DIR}/{L3_key}/{L4_key}/{L5_key}/overview.mdx  level_5 cluster page
  {node dir}/Vid_{video_key}.mdx                      video page, in its node's dir

  * Node keys = YAML _key verbatim.
  * video_key from the video's human meaning (manifest description, speaker, claim), not the X-status-id filename
    ("2067372027623715212" is not a page key). Sanitize to [A-Za-z0-9_], four words or less, site-unique by appending the
    first 7 chars of the status id or cid. Vid_ prefix keeps video pages greppable and clear of Img_ pages. Never changes once
    minted (reuse on rerun; match by recorded cid / sha256).
  * Hand-written {VIDEOS_L2_DIR}/buckley-carlson-kash-patel-valhalla.mdx (page_key Videos_Buckley_Kash) has no ck_ frontmatter
    and is NOT an orphan: leave it. If its video appears in the YAML, record the collision in {FINDINGS_FILE} for a human; never
    overwrite or delete it.

A FILE PATH IS NOT A ROUTE (bites every link to a page this pipeline did not write: on_pages, site_page, "How It Connects"):
  * site/docs/index.md is served at "/", never "/index".
  * A hub may have a slug unlike its folder: the mirandize hub is /court/mirandize/mirandize-overview, not .../overview.
  * Section overviews are /X/overview, not bare /X.
So resolve links outside {VIDEOS_L2_DIR} through {PAGES_CSV} url_path; path-derived is only the fallback (it passes local
checks and fails the build). Our own pages under {VIDEOS_L2_DIR} route exactly as their path.

Navigation (never dead-end):
  * Every cluster page TOC: PEERS, PARENT, CHILD clusters, its video pages.
  * Every video page: link to parent cluster, previous/next peer videos.
  * {VIDEOS_L2_PAGE} keeps its prose; only the TOC between {/* VIDEOS_TOC_START */} and {/* VIDEOS_TOC_END */} regenerates
    (every level_3: title link, recursive video count).
  * Single-video nodes are bypassed (next section).
Both arrival paths must work: cold browse from the left bar; topic arrival wanting to WATCH the footage one click away.

============================
KNOWLEDGE — SINGLE-VIDEO NODES ARE BYPASSED IN NAVIGATION
============================

A node is BYPASSED when number_of_videos_recursive is 1 and no child cluster survives the same test (its whole subtree
resolves to one video page).
LINKS change only: the parent's TOC and sibling peer lists show the single VIDEO PAGE instead (its title; count 1); the video
page's back link points to the NEAREST NON-BYPASSED ANCESTOR; its previous/next come from the set the parent linked.
The page is still built: the bypassed cluster page is generated at its normal path with ck_node_key, concept paragraph and its
own TOC; keeps its {PAGES_CSV} row at its true level; is NEVER an orphan. The video page keeps its path under the bypassed node
and ck_node_key = that node's _key. Multi-video nodes link normally. Applies at every depth (a one-video level_3 is linked
straight from the Level 2 TOC).

============================
KNOWLEDGE — VIDEO PAGE LAYOUT SPEC
============================

This prompt writes the WORDS; the LAYOUT is owned by {NAV_PROMPT} (generator markup plus the marked CK_VIDEO_LAYOUT block in
{SITE_DIR}/internals/src/css/custom.css); {LAYOUT_GUIDELINES} wins on conflict. Recorded so prose suits the shape:
  * No right bar: hide_table_of_contents: true.
  * True aspect ratio, never stretch or crop. Opaque; controls always visible and reachable.
  * Never autoplay, never loop; preload="metadata" only. Poster set when one exists.
  * The player sits IN THE PAGE, floated beside the prose, scrolling with it (not pinned to the window). Prose WRAPS around it,
    full width below; no hand-capped prose width.
  * Bounding box: up to 85% of main-area width, max height one screen with the control bar inside. Vertical phone video comes
    out much narrower; that is correct.
  * Below the mobile breakpoint: full-width block above the prose.
  * Write ordinary paragraphs. After any layout change, test one landscape and one vertical video visually.

============================
KNOWLEDGE — HOSTING AND PLAYING THE VIDEO
============================

VIDEO BYTES ARE NEVER COPIED INTO {SITE_DIR}/static (0.5MB to 173MB, gitignored on purpose: {VIDEOS_DIR}/.gitignore excludes
*.mp4, *.mp3, *.mkv, *.avi, *.mov, *.wav, *.webm; GitHub Pages is no video host). A Level 5 page plays from PUBLIC IPFS
GATEWAYS by cid:

  sources   https://ipfs.orbitor.dev/ipfs/{cid}
            https://gateway.pinata.cloud/ipfs/{cid}
            https://ipfs.filebase.io/ipfs/{cid}
            https://gw.ipfs-lens.dev/ipfs/{cid}

One <source> per gateway, in this order, from the single list in videos_planning/generator/ipfs_gateways.py. dweb.link, ipfs.io
and w3s.link were retired in September 2026 (429 "switching to a service worker gateway only"; w3s.link redirects to dweb.link):
never emit them. After changing the list, run videos_planning/generator/rewrite_video_gateways.py --write.
{cid} here is the v1 base32 form computed at generation time by ipfs_gateways.base32(); the YAML keeps CIDv0.

  * cid "": write the page (title, write-up) with a plain "media pending" note and NO player element (a dead rectangle is worse).
  * ipfs_pinned FALSE ALSO GETS NO PLAYER. Most CIDs came from `ipfs add -n` (computed, never added or announced): as of
    2026-07-23 only 58 of 372 were on the node. Such a player is dead for every visitor and looks perfect here with IPFS
    Companion running: the trap this pipeline is most likely to fall into. Give it the FULL page (title, write-up, sources,
    links, poster when extractable) with this note instead of the player:

      Media pending. This footage is held locally and has not yet been
      published to IPFS, so it cannot be played here yet.
      CID (computed): Qm...

    Report the count and list the CIDs as the worklist for a later approved pinning job; the pages light up on the next run.
  * Never pin as a side effect (irreversible; separate approved job). Verify pin status at run time with
    `ipfs pin ls --type=recursive`, not the YAML field (written elsewhere, goes stale).
  * THIRD-PARTY VIDEO (YouTube, Rumble, X), no CID: the platform's own embed instead of our player, saying plainly where it is
    hosted and that the platform can remove it at any time. {VIDEO_LIST_CSV} indexes the YouTube material.
  * POSTER (small, may be local): ffmpeg one frame a few seconds in, longest side 1600px, quality ~85, to
    {POSTER_DIR}/{sha256}.jpg, referenced as /img/video_posters/{sha256}.jpg. Skip if it exists; skip when no local file.
  * Verify the built site in a CLEAN BROWSER PROFILE WITH NO IPFS COMPANION (it rewrites gateway URLs to your local node,
    hiding dead players). The single most likely way to ship broken pages.

============================
KNOWLEDGE — THE EXCLUSION GATE (NOT EVERYTHING IN THE YAML MAY BE PUBLISHED)
============================

BAN SET = UNION of:
  {BAN_VIDEOS_CSV}: the MASTER; rows sha256, cid, file_path, banned, reason, date_added. Match sha256, then cid, then file_path.
    banned=false is an explicit UN-BAN (row kept). New bans go here.
  {EXCLUDE_FILE}: older one-identifier-per-line list; still honoured; never emptied.
minus CSV rows marked false. If missing, create {BAN_VIDEOS_CSV} with header sha256,cid,file_path,banned,reason,date_added and
{EXCLUDE_FILE} with a header comment explaining the format, before the first page is written.

The repo charter ({ROOT_DIR}/claude.md, "Banned Media") owns the contract; {HIERARCHY_PROMPT} copies `banned:` onto every YAML
entry. This prompt does NOT trust or write that field: it re-checks every identity against the two files every run (the YAML is
regenerated elsewhere; a ban living only there is not a ban). The YAML value corroborates: disagreement = STOP and report
(usually {HIERARCHY_PROMPT} hasn't re-run since the CSV changed).

A banned video gets nothing:
  * NO page under {VIDEOS_L2_DIR} (DELETE an existing one and its {PAGES_CSV} row). NO poster under {POSTER_DIR} (delete it).
  * NO placement anywhere (dropped from Stage 6; existing placements, in or outside CK_PLACED_VIDEOS, removed).
  * NO LINK INTO IT (card, poster thumbnail, TOC row, "see also", Stage 5 link). Cluster counts reflect what is published.
  * NO PIN, ever; no pinning job runs over an unfiltered set.
The YAML entry is never removed (complete private record).

Why video needs this more: the images mirror swept in private material (dashboards, bookings, video calls with named faces;
eleven published in its first run). For video, prose care is no protection (the footage streams at a public URL; the media is
the payload); a clip exposes every bystander's face and voice for its whole duration; and IPFS publication is not reversible
(removing the page removes the link, not the content), so exclusion must precede pinning.
When a run finds non-public material, add a CSV row with reason and date BEFORE the run ends, record it in {FINDINGS_FILE}, and
delete the page and poster in the same run.

============================
KNOWLEDGE — WRITING THE WRITE-UP
============================

A write-up is not a caption: it handles a claim made out loud, over time, by a named person. Sources, all used:
  * THE TRANSCRIPTION (transcription_file): the most important input. Who speaks, what they assert, in what order, in their
    words. Quote it, attributed, in quotation marks, where a quote beats paraphrase.
  * ai_description and ai_description_file: what is SEEN versus said.
  * ocr_file when present: chyrons, slates, captions.
  * {VIDEO_MANIFEST} provenance (source_url, source_author, added_date): say where the clip came from (e.g. a phone capture of
    a broadcast reposted by an anonymous account).
  * Hosting pages (on_pages, plus the node's site_page / site_level_2): read each; explain the relationship to every one.
  * {CK_FILE}: the investigation area, described accurately.

Structure, in order:
  1. WHAT IS THIS: length, format, origin, who posted it.
  2. WHO IS SPEAKING AND WHAT DO THEY CLAIM: named, attributed, quoted; approximate timestamps ("about 1:10 in").
  3. WHAT THE FOOTAGE ACTUALLY SHOWS, separate from the narration. A clip often argues a thesis its frames don't show: say so
     plainly and record it in {FINDINGS_FILE}.
  4. HOW IT CONNECTS: links to related Level 2s and Level 3s as /X/overview, resolved against {PAGES_CSV}, routes known to build.

Safe-writing rules (mandatory):
  * The word "defamation" never appears in article text.
  * Never write that any person KNEW anything before the crime, or DID anything immoral or illegal. Check for exactly these.
  * Never state as fact that a living person committed a crime unless court-proven; attribution ("according to", "allegedly",
    "reportedly", "researchers have questioned"); suspicions as questions or reported claims.
  * THE SPEAKER'S ACCUSATION IS NOT OURS: report that the video contains the claim without adopting it. "In the clip, [speaker]
    states that ..." / "[speaker] alleges ...", never "[third party] did ...". Attribute every accusation to its speaker.
  * Maximum information within those limits (they constrain phrasing, not depth).
  * Raw claims stay private in {CK_FILE} and the planning layer.
  * The YAML is an input, not an authority: ai_description has been wrong about people, places, events; clustering sometimes
    files a video under a thesis the footage contradicts. Write what the footage shows; say so when it differs from the filing
    and the narration; record it in {FINDINGS_FILE}.
Style per {ASSESS_MANUAL}. MDX comments must be {/* ... */}; HTML <!-- --> breaks the compile and deploy.

============================
KNOWLEDGE — BOOKKEEPING FIELDS ON PAGES
============================

Frontmatter:
  * Cluster page: title, ck_node_key: <_key>
  * Video page: title, hide_table_of_contents: true,
      ck_video_cid: <cid>          the primary identity
      ck_video_sha256: <sha256>    "" when there is no local file
      ck_node_key: <owning node _key>
CID IS THE PRIMARY KEY (many entries have a manifest CID and empty sha256). Match existing pages by ck_video_cid, then
ck_video_sha256, then ck_node_key, then filename. Reruns REFRESH STRUCTURE BUT PRESERVE PROSE:
  * Regenerated every run: slug and mechanical frontmatter, back button, the player's src / poster / fallback source and
    attributes, layout classNames, "Where This Video Appears", "Related Areas", peer/child TOCs, previous/next.
  * Carried forward when present: title, sidebar_label, frontmatter description, prose under "## What This Video Shows",
    hand-placed transcript quotes and timestamps, the three paragraphs under "## About This Cluster".
The writing pass is far costlier and uses sources the generator never reads; never discard it or resurrect raw YAML over
scrubbed prose. Baseline boilerplate IS refreshed. Pages the YAML no longer accounts for are removed as orphans, counted and
reported; overview.mdx and buckley-carlson-kash-patel-valhalla.mdx are NEVER orphans.

============================
KNOWLEDGE — CLICKABLE VIDEOS ON HOST PAGES (LINK BACK TO THE VIDEO PAGE)
============================

A video appears on its own page (video_page) and often inline on topic pages (on_pages). Give a reader of, say, Mic/AES.mdx a way
to reach the video's page with its full write-up. Link-only; nothing else on the host changes; the YAML is not written.

URL: video_page e.g. ~/BGit/Bryan_git/charlie-kirk/site/docs/Videos/Mic_Thesis/Vid_Candace_Mic_2067372.mdx; routeBasePath "/",
so strip {DOCS_DIR}, drop .mdx: /Videos/Mic_Thesis/Vid_Candace_Mic_2067372. Site-relative, leading "/", no domain, no /docs.
Confirm against {PAGES_CSV} url_path; {PAGES_CSV} wins.

on_pages entries may be stringified dicts, e.g. "{'page': '~/BGit/Bryan_git/charlie-kirk/site/docs/Mic/AES.mdx'}": extract,
dedupe, skip and record paths that don't exist.

MATCH (only this video, never a neighbor), in order:
  1. IPFS CID in a <video> src, <source> src, or markdown link (https://ipfs.io/ipfs/{cid}, https://{cid}.ipfs.dweb.link/...,
     bare /ipfs/{cid}): strongest; host pages key on it.
  2. Third-party id (YouTube watch id, Rumble slug) in an <iframe src>.
  3. Filename stem or distinctive caption substring, only if unambiguous (bare X status ids mismatch easily).
No match on a claimed host: record it; never invent an embed.

VIDEO IS NOT AN IMAGE HERE: an anchor around a player doesn't work (clicks hit the controls).
  * <video> / <iframe>: do NOT wrap. Add on its own line immediately beneath:
        <p><a href="URL">Full write-up and sources for this video →</a></p>
    The player stays exactly as is.
  * A markdown link or poster IMAGE standing in for the video IS wrapped/retargeted normally: ![alt](src) becomes [![alt](src)](URL).
  * Never alter a src, poster, sizing, or caption.
IDEMPOTENT AND SAFE: link already beneath the embed = leave it; a human-placed different link (e.g. the original X post) is never
clobbered (add ours alongside, or record and skip); never point a video at another video's page; a BANNED video is never linked:
remove the embed and the poster, report with ban reason; N host pages = N edits.

============================
KNOWLEDGE — SHOULD_BE_ON_PAGES: PLACING VIDEOS ONTO TOPIC PAGES
============================

Per video: on_pages (where it IS shown; observed; mostly empty), should_be_on_pages (where it OUGHT to be; reasoned by
{HIERARCHY_PROMPT} Stage 13; the COMPLETE desired state, a superset of on_pages, ordered best-match first), video_page (its own
page). The work: should_be_on_pages minus what is already on that page. Brings the footage to the reader, one click from the
full write-up.

SHAPE: list of `page:` tilde paths, e.g.
    should_be_on_pages:
      - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/Suspicious/Cause_of_Death/entrance-or-exit.mdx"
Re-stat every path (pages get renamed); report non-resolving ones; never guess a neighbour.

A CARD, NOT A PLAYER (deliberate divergence from images: twelve players per page would mean many cross-origin gateway fetches of
up to 173MB on a page not about the video, slow, flaky, with dead rectangles for unpinned CIDs). A card is:
  * a poster thumbnail /img/video_posters/{sha256}.jpg (when it exists) wrapped in an anchor to the video's page; the only media a
    placement ever loads;
  * a title line linked to the same page;
  * a one-line caption (what the footage shows, who speaks);
  * a duration and source note when known ("4:19 · posted by @RealCandaceO, 17 Jun 2026").
The player lives on ONE page; everything else links to it.
  * No poster: text-only card (title link, caption, duration). Never an <img> that doesn't resolve; never embed the video instead.
  * Generate missing posters BEFORE editing pages (same ffmpeg settings, {POSTER_DIR}/{sha256}.jpg; skip if present; skip when no
    local media, which is normal on a fresh clone).
  * Every card carries data-cid.

LINK TARGET: video_page converted as in Stage 5, confirmed against {PAGES_CSV}. No video_page: skip and report.

BLOCK at the BOTTOM, between MDX markers:
    {/* CK_PLACED_VIDEOS_START — generated, do not hand-edit */}
    ## Videos
    ... cards ...
    {/* CK_PLACED_VIDEOS_END */}
  * A page may also carry the images pipeline's CK_PLACED_IMAGES block: NEVER read, rewrite, reorder or delete it.
  * Bottom placement keeps prose intact; regenerated wholesale (inside replaced, outside byte-identical). Markers absent: append at
    EOF (after a CK_PLACED_IMAGES block if present); present: replace in place. Empty list: REMOVE the block.
  * Never in pages under {VIDEOS_L2_DIR} or {DOCS_DIR}/Photos, {THIS_DIR}, or planning files. MDX comments only.

NO DUPLICATES: drop videos whose cid (v0 or base32 v1) or sha256 already appears in the page text with OUR block stripped
(covers inline players, IPFS and iframe embeds, older out-of-block placements). Stage 5 owns those.
PER-PAGE LOAD: cap SIX cards counting existing embeds, YAML order (best first); report overflow.
UNPINNED / EMPTY CID: the card still works (it lands on the page with the honest pending note). Place, count, report; never imply
the footage is watchable.
BAN GATE (checked against the two files, not the YAML): never placed; existing placements removed, including ones OUTSIDE a
CK_PLACED_VIDEOS block, found and cut explicitly. Removing a card does not unpublish IPFS content; the ban must precede pinning.
CAPTION: from title and ai_description first sentence; when the point is something a person SAYS, name and attribute ("Candace
Owens sets out a rigged-microphone theory"), never assert it. All safe-writing rules apply; a failing title/description is
rewritten for the caption and recorded in {FINDINGS_FILE}. Captions regenerate with the block; human commentary belongs above
the markers or on the video page.

============================
STAGE 1 — SETUP AND READ
============================

* Run the STALE-DATA PRECONDITION gate; stop on failure.
* Read in order: {LAYOUT_GUIDELINES}, {CK_FILE} (as in READ FIRST), {CHARTER_FILE}, {ASSESS_MANUAL}, {HIERARCHY_FILE},
  {PAGES_CSV}, {VIDEO_MANIFEST}. Index nodes and videos.
* Inventory existing pages under {VIDEOS_L2_DIR} (ck_node_key / ck_video_cid / ck_video_sha256); mark overview.mdx and
  buckley-carlson-kash-patel-valhalla.mdx protected.
* Ensure {POSTER_DIR} exists.
* BUILD THE BAN SET FIRST: parse {BAN_VIDEOS_CSV} with the python3 csv module (create if missing) plus {EXCLUDE_FILE} (create if
  missing); union minus un-bans; index by sha256, cid, expanded file_path; hand to every agent. Malformed banned column = STOP.
  Cross-check the YAML `banned:`; REPORT disagreements (files win).
* DELETION WORKLIST: existing {VIDEOS_L2_DIR} pages whose ck_video_cid or ck_video_sha256 is banned, and posters named for a
  banned sha256. Deleted in Stage 3 before any new page; {PAGES_CSV} rows in Stage 4. Non-empty = banned footage is live now:
  say so at the TOP of the report.

Output to stdout:
============================
STAGE 1 COMPLETE
Precondition gate: PASS (image file_paths 0, "This image" prose 0, cid coverage N%)
Layout guidelines lines: N
YAML nodes: N level_3 / N level_4 / N level_5   videos: N unique cid
Playable now: N (cid + pinned)   unpinned: N   no cid: N   third-party: N
Existing pages found: N cluster / N video / 2 protected
Ban set: N identities ({BAN_VIDEOS_CSV} N rows, {EXCLUDE_FILE} N lines, N un-bans)
YAML banned: disagreeing with the files: N (listed — the files win)
DELETION WORKLIST: N live pages + N posters for banned videos
should_be_on_pages: N videos planned onto N topic pages (N placements)
============================

============================
STAGE 2 — PARTITION THE WORK
============================

* Partition level_3 nodes (whole subtrees) into up to {MAX_AGENTS} partitions balanced by video count, not page count (one video
  with a 40-minute transcription costs more than five clips with none). Fewer for a small corpus. A subtree never splits.
* Each agent gets its OWN scratch subdirectory, never the shared root (agents invent the same helper names, apply.py, dump.py,
  out.json, and overwrite each other; this has happened).
* Every agent gets the YAML index and {PAGES_CSV} for cross-partition links.

Output to stdout:
============================
STAGE 2 COMPLETE
Partitions: N   (list: partition -> level_3 _keys -> recursive video count)
============================

============================
STAGE 3 — PARALLEL PAGE GENERATION (UP TO {MAX_AGENTS} AGENTS)
============================

Launch all partitions in one burst. Each agent receives its subtree(s), the full node index, the layout spec, {LAYOUT_GUIDELINES}
contents, the writing rules, the ban set, its existing-page map, and pointers to {CK_FILE}, {PAGES_CSV}, {ASSESS_MANUAL},
{VIDEO_MANIFEST}. Each agent, top-down:

* Read the {CK_FILE} sections for its clusters.
* Compute its bypass set first; build every TOC against it. Skip empty nodes entirely.
* Every published cluster node: create or rewrite overview.mdx (title, short concept paragraph grounded in {CK_FILE} under
  safe-writing, full TOC with bypassed nodes replaced by their video pages). Bypassed nodes get their own page the same way.
* Every video entry:
    * FIRST the ban check (sha256, then cid, then file_path). Banned: delete any existing page in this node dir and its poster,
      hand the {PAGES_CSV} row to the orchestrator, report with ban reason; write no page, extract no poster, mint no key, omit
      from every TOC. Check before the poster step so a banned video's frames never land in {POSTER_DIR}.
    * Ensure the poster (when a local file exists).
    * Existing page for this cid in this node dir: read it, then rewrite (BOOKKEEPING). Else mint the key and create.
    * LAYOUT SPEC exactly. Player ONLY when the cid is pinned on the node; platform embed for third-party; otherwise poster plus
      the "media pending" note (including computed-but-unpinned cids).
    * Write the account (WRITING THE WRITE-UP): transcription first, then description and OCR, then hosting pages.
    * Safe-writing check on the finished text, incl. every on-camera accusation attributed to its speaker.
* Return to the orchestrator (never write {PAGES_CSV} or {VIDEOS_L2_PAGE}): pages created / rewritten / unchanged with page_key
  (node _key or video_key), parent_key, level, url_path, file_path, title, sidebar_label, directory, extension, line_count; plus
  orphans, missing media, missing transcriptions, unpinned CIDs, unresolvable links.

Output to stdout (after all agents return):
============================
STAGE 3 COMPLETE
Agents run: N
Cluster pages: N created, N rewritten (N bypassed in navigation, N empty skipped)
Video pages: N created, N rewritten
Players emitted: N IPFS (pinned), N third-party embed, N media pending
Posters written: N   Banned videos skipped (no page written): N
Banned videos UN-PUBLISHED this run: N pages deleted, N posters deleted
  (each listed with cid/sha256, page path, and ban reason)
Media-pending pages awaiting a pinning job: N (CIDs listed)
Videos with no transcription (write-up is thin): N (listed)
Problems reported: N (list)
============================

============================
STAGE 4 — SHARED FILES: LANDING PAGE AND PAGES.CSV
============================

Orchestrator only, single-threaded:
* Regenerate {VIDEOS_L2_PAGE}'s TOC between VIDEOS_TOC_START / VIDEOS_TOC_END (first run: insert the markers directly under the
  H1): every published level_3 title linked with recursive count; a bypassed level_3 links straight to its video page. The
  existing prose about footage types stays untouched.
* Also link buckley-carlson-kash-patel-valhalla.mdx from the landing page so it is not stranded.
* Merge agent rows into {PAGES_CSV} per the schema in {ROOT_DIR}/claude.md (page_key = node _key or video_key; parent_key =
  parent node _key, video pages parent to their owning node; level = node depth, video pages depth + 1). Add new, update
  retitled/moved, remove rows of banned/orphaned pages deleted this run; report other vanished files rather than deleting blindly.

Output to stdout:
============================
STAGE 4 COMPLETE
Landing page TOC rows: N
pages.csv: N rows added, N updated, N flagged
============================

============================
STAGE 5 — MAKE HOST-PAGE VIDEOS CLICKABLE (LINK TO THE VIDEO PAGE)
============================

Video pages now exist. Follow CLICKABLE VIDEOS ON HOST PAGES exactly (a <video> gets a text link beneath it, never a wrapping
anchor). Work by host PAGE so each file is opened and rewritten once:
* Walk every video; banned ones are skipped and their host embeds REMOVED. Derive each URL from video_page (confirm against
  {PAGES_CSV}); parse on_pages into deduped host paths.
* Invert: host page -> [(cid, sha256, filename, video-page URL), ...].
* Per host page (up to {MAX_AGENTS} agents; never split a page): read it; match each video's embed (CID, third-party id,
  filename/caption); none = "claimed host, not embedded"; add the link per the idempotency rules; never touch a sibling embed;
  byte-identical elsewhere.
* Never modify {VIDEOS_L2_DIR} pages here, nor {HIERARCHY_FILE}. Creates, deletes and moves nothing beyond ban removals.

Output to stdout:
============================
STAGE 5 COMPLETE
Host pages scanned: N   host pages edited: N
Video embeds linked: N   already linked (skipped): N
Claimed hosts with no matching embed: N (list)
Pre-existing links left intact: N (list)
============================

============================
STAGE 6 — PLACE THE SHOULD_BE_ON_PAGES VIDEOS ONTO THEIR TOPIC PAGES
============================

Makes the plan real with CARDS. Follow SHOULD_BE_ON_PAGES exactly. Video pages exist (Stage 3) and {PAGES_CSV} is current (Stage 4).

Plan first:
* Walk every video. Skip and count banned; skip empty should_be_on_pages; skip and report missing video_page.
* Poster: reuse {POSTER_DIR}/{sha256}.jpg, extract it now if local media exists, else text-only. All extraction BEFORE any page edit.
* Derive and confirm the video-page URL.
* Re-stat every should_be_on_pages path; drop and report missing ones and any under {VIDEOS_L2_DIR} or {DOCS_DIR}/Photos.
* Invert: host page -> ordered (cid, sha256, poster src or none, video-page URL, title, caption, duration, source note), YAML order.

Per host page (up to {MAX_AGENTS} agents; never split a page):
* Read it; strip OUR block from the test text (leave CK_PLACED_IMAGES alone); drop videos whose cid (either form) or sha256 already
  appear.
* Cap six counting existing embeds, YAML order; report overflow.
* Emit "## Videos" with one card per video: poster <img> wrapped in an anchor to its Videos URL, data-cid, alt from the title,
  loading="lazy", plus linked title, caption, duration/source note. Text-only cards when no poster.
* Replace between our markers / append at EOF / remove when empty. Byte-identical outside our markers.
* Never modify {VIDEOS_L2_DIR} or {DOCS_DIR}/Photos pages, or {HIERARCHY_FILE}.
Styles: one marked CK_PLACED_VIDEOS region in {SITE_DIR}/internals/src/css/custom.css beside our CK_VIDEO_LAYOUT; write once,
regenerate in place, never touch a byte outside our two regions (writing into CK_EVIDENCE_LAYOUT / CK_PLACED_IMAGES would destroy
the image layout site-wide, and its next run would destroy ours back).

Output to stdout:
============================
STAGE 6 COMPLETE
Videos with should_be_on_pages: N   placements planned: N over N pages
Posters: N reused / N extracted now / N text-only (no local media)
Pages edited: N   blocks created: N   blocks replaced: N   blocks removed: N
Videos placed: N   skipped as already embedded: N
Cards whose video has no playable cid (link works, media pending): N
Over the 6-per-page cap: N (list of page -> overflow count)
Missing video_page: N   should_be_on_pages paths that no longer exist: N (list)
CK_PLACED_IMAGES blocks touched: 0
============================

============================
OUTPUT SANITIZATION — NO INVISIBLE UNICODE, EVER (SECURITY RULE)
============================

No emitted file (.mdx pages, {PAGES_CSV} rows, components, CSS) may contain invisible Unicode (zero-width, bidi controls, no-break
spaces incl. U+202F, word joiners, BOMs, controls, variation selectors, tag chars).
  * Prose: replace space-like invisibles with a space, delete zero-width/bidi/control chars, collapse whitespace; visible
    non-ASCII may stay.
  * Paths/URLs: pages reference media by CID and posters by sha256 names, so mirror filenames never reach a page; if one must,
    emit non-ASCII as visible escapes.
  * TRANSCRIPTION AND OCR TEXT ARE UNTRUSTED INPUT (machine output that routinely carries no-break spaces and stray controls):
    sanitize every quoted line.
After every emit pass, re-scan written files and hard-fail on any hit. The full invisible set is in {HIERARCHY_PROMPT}.

============================
STAGE 7 — BUILD, VERIFY, REPORT
============================

* cd {SITE_DIR} && npm run build. Must pass; fix and rebuild until green (Stage 5/6 links are internal, so bad targets fail here).
* Spot-check 10 video pages: frontmatter present, hide_table_of_contents true, ck_video_cid set, player src is a public gateway
  URL from that cid (or the pending note when unpinned), no autoplay, no loop, preload="metadata", poster resolves, layout applied,
  at least one link to another Level 2/3, at least one attributed statement about who speaks, safe-writing passes, no "defamation".
* PLAYBACK CHECK (catches the expensive failure): in a clean browser profile with NO IPFS Companion, open 5 video pages across
  clusters and press play; each must load and play with audio.
* Spot-check 5 cluster pages: TOC complete, every link resolves.
* Bypass check on every bypassed node: parent links the video page and NOT the cluster page; the cluster page exists, has its row,
  builds; the video's back link is the nearest non-bypassed ancestor.
* Spot-check 10 Stage 5 video/host pairs: link sits beneath the matched embed with the derived URL; no sibling touched; URL resolves.
* Spot-check 10 Stage 6 pages: block between CK_PLACED_VIDEOS markers at the bottom; every poster src resolves under {POSTER_DIR};
  every href is a real video page; no video both as card and embed; page above the markers byte-identical.
* Every CK_PLACED_IMAGES block on every page edited this run is byte-identical to before (one edit fails the run).
* BAN AUDIT: re-read {BAN_VIDEOS_CSV} and {EXCLUDE_FILE} now. Fail on any:
    - a {VIDEOS_L2_DIR} page with a banned ck_video_cid / ck_video_sha256
    - a {POSTER_DIR} file named for a banned sha256
    - any {DOCS_DIR} page referencing a banned video (grep cid, sha256, gateway URL, original basename; inside and outside blocks)
    - any page linking to a /Videos URL of a banned video's page
    - anything banned pinned by this run (nothing is pinned at all; state the zero explicitly)
  Grep for identity, not page path.
* {PAGES_CSV} row change matches pages created. Invisible-Unicode scan over everything written (incl. host pages).
* Nothing modified outside {VIDEOS_L2_DIR}, {POSTER_DIR}, {PAGES_CSV}, Stage 5 host pages (added links, ban removals), Stage 6 host
  pages (our block, ban removals), our marked CSS regions, {VIDEOS_L2_PAGE}'s marker section and its protected-page link.
  sidebars.ts, {DOCS_DIR}/Photos, {SITE_DIR}/static/img/evidence untouched; CK_EVIDENCE_LAYOUT and CK_PLACED_IMAGES in custom.css intact.

Output to stdout:
============================
STAGE 7 COMPLETE — FINAL REPORT
Build: PASS/FAIL
Pages now under /Videos: N cluster + N video = N total
Videos published: N of N in YAML (N media pending)
BANNED: N videos in the ban set — 0 have a page, 0 have a poster, 0 are placed
  on any page, 0 are linked to from anywhere, 0 pinned (all five required)
  Un-published this run: N pages + N posters + N placements removed
Playback check: N/5 played in a clean profile
Host pages linked: N   video embeds given links: N
Topic pages carrying placed video cards: N   videos placed: N
Publishing worklist remaining (planned but not placed): N (with reasons)
Spot-checks: video pages N/10 pass, cluster pages N/5 pass, host links N/10 pass,
             placement blocks N/10 pass
pages.csv in sync: yes   sidebars.ts untouched: yes   invisible scan: clean
Photos section untouched: yes   CK_EVIDENCE_LAYOUT intact: yes
CK_PLACED_IMAGES blocks unchanged: yes
============================

============================
HARD RULES
============================

* The STALE-DATA PRECONDITION is a hard stop before anything else.
* {LAYOUT_GUIDELINES} first every run; it overrides this prompt; never edit it from here. {CK_FILE} loaded at the start (relevant
  sections); every write-up is grounded in it.
* WRITES ONLY: pages under {VIDEOS_L2_DIR}; posters under {POSTER_DIR}; {VIDEOS_L2_PAGE}'s marked TOC (plus the protected-page link);
  our marked CSS regions; {PAGES_CSV} rows; on host topic pages, Stage 5 links and Stage 6 CK_PLACED_VIDEOS blocks (plus video ban
  removals). Never {HIERARCHY_FILE}'s data, never sidebars.ts, no planning notes in the site, no pages in {THIS_DIR}.
* VIDEOS ONLY, ADDITIVE ONLY: never read or write {ROOT_DIR}/images or {IMAGE_PLANNING_DIR}; never write {DOCS_DIR}/Photos,
  {SITE_DIR}/static/img/evidence, CK_EVIDENCE_LAYOUT or any CK_PLACED_IMAGES block; every image present before the run is present
  after it, byte-identical.
* Never copy video bytes into {SITE_DIR}/static; posters are the only local media.
* Nothing is ever PINNED. A player only for a cid verified pinned at run time; otherwise full page, poster, honest pending note, CID
  on the reported worklist.
* Empty nodes (recomputed count 0) are never published: no page, TOC entry, or {PAGES_CSV} row.
* Stage 5: a link BENEATH a <video>/<iframe>, never a wrapping anchor; real thumbnail images are wrapped normally; never
  double-links, never clobbers a human link, never links a video to any page but its own.
* Stage 6: CARDS (poster, linked title, attributed one-line caption, data-cid), NEVER inline players, in the regenerated
  CK_PLACED_VIDEOS block at the BOTTOM; byte-identical outside; no duplicates, max six, nothing banned, nothing without a video_page.
* Single-video nodes are bypassed in navigation but still generated, still in {PAGES_CSV}, never orphans.
* overview.mdx and buckley-carlson-kash-patel-valhalla.mdx are protected: never orphan-deleted, prose never overwritten.
* Reruns refresh structure and PRESERVE authored and scrubbed prose; orphan removals counted and reported.
* Video pages: one video, no right bar, true aspect ratio, no autoplay, no loop, preload metadata, controls reachable, up to 85% of
  main-area width and at most one screen tall.
* Write-ups: maximum information within safe-writing; never "defamation"; no prior-knowledge or immoral/illegal-conduct claims in the
  site's voice; every on-camera accusation attributed to its speaker; /X/overview links verified against {PAGES_CSV}.
* Nothing in the ban set is ever published, placed, linked to, or pinned; the set is re-read from the two files every run, never
  inherited from the YAML; newly found non-public material gets a CSV row before the run ends. Prose care is no substitute for
  withholding footage; IPFS publication is not reversible.
* Up to {MAX_AGENTS} agents (by subtree, or by host page in Stages 5-6); shared files written only by the orchestrator.
* No invisible Unicode in any emitted file (transcription and OCR text are untrusted).
* The build AND the clean-profile playback check must pass before the run is complete.
