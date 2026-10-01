ROOT_DIR dir is ~/BGit/Bryan_git/charlie-kirk

THIS_DIR dir is {ROOT_DIR}/videos_planning
VIDEOS_DIR dir is {ROOT_DIR}/videos
HIERARCHY_FILE is file {VIDEOS_DIR}/videos.yaml
  Created 2026-07-23 as a copy of {ROOT_DIR}/images/images.yaml with only the
  SCHEMA converted to videos. Its DATA is replaced with the real video corpus by
  {HIERARCHY_PROMPT}. This prompt must not run for real until that has happened
  — see THE STALE-DATA PRECONDITION below.
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
  NOT {SITE_DIR}/static. docusaurus.config.ts sets
  staticDirectories: ["internals/static"], so that is the ONLY directory served.
  A poster written to {SITE_DIR}/static is silently not published and every
  media-pending page renders a broken image. The URL in the page is still
  /img/video_posters/{sha256}.jpg — only the on-disk location differs.
VIDEO_LIST_CSV is file {DOCS_DIR}/video_list.csv
PAGES_CSV is file {ROOT_DIR}/pages.csv
CK_FILE is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt
  (Real file. Moved 2026-09-19. ~/BGit/Bryan_git/charlie-kirk/Charlie_Kirk.txt is now a symlink to it —
   use that only to verify the location; always read and write the real path.)
ASSESS_MANUAL is file {ROOT_DIR}/prompts/Assess_Manual.md

MIRROR_DIR dir is ~/_Mirror/Politics/Charlie_Kirk_Mi
MIRROR_SIDECAR_DIR dir is ~/BGit/Bryan_git/personal_large_files_bridge/_Mirror/Politics/Charlie_Kirk_Mi
REPO_SIDECAR_DIR dir is {ROOT_DIR}/.lfbridge

IMAGE_PLANNING_DIR dir is {ROOT_DIR}/image_planning

MAX_AGENTS is ... = 12

============================
SCOPE — VIDEOS ONLY, ADDITIVE ONLY
============================

Two boundaries define this prompt. Both have been crossed before, because every
file in {THIS_DIR} is a converted descendant of the images pipeline.

=== 1. THE ONLY INPUT IS THE VIDEO CORPUS ===

The single source of page content is {HIERARCHY_FILE} —
~/BGit/Bryan_git/charlie-kirk/videos/videos.yaml — plus the sidecars, manifest
and investigation files it points at.

  * DO NOT READ and DO NOT WRITE {ROOT_DIR}/images or anything under it,
    including images/images.yaml. It is a different corpus with a different
    schema and nothing in it belongs on a video page.
  * DO NOT READ and DO NOT WRITE {IMAGE_PLANNING_DIR}. It was prior art while
    this prompt was being written; that job is finished. Reading it during a run
    only invites its data and its wording back into video pages, and copying any
    file out of it silently reverts this directory's conversion.
  * DO NOT WRITE {DOCS_DIR}/Photos or {SITE_DIR}/static/img/evidence.
  * Every page written by this prompt is about a video. If a run finds itself
    reading a .jpg, describing a still, or resolving a path under images/,
    something is wrong — stop and report rather than publish it.

=== 2. THIS PROMPT ADDS VIDEO; IT NEVER REMOVES OR CHANGES IMAGES ===

A separate pipeline owns images on this site and is still running. The two edit
the same topic pages and the same stylesheet. Our job is purely additive with
respect to images:

  * Never delete an image, an <img> tag, a gallery, a caption, a figure, or an
    image-bearing block from any page.
  * Never move, resize, retarget, reorder, or reword an image or its caption —
    not even to make room for a video card.
  * Never touch a CK_PLACED_IMAGES block on a topic page or the
    CK_EVIDENCE_LAYOUT / CK_PLACED_IMAGES blocks in
    {SITE_DIR}/internals/src/css/custom.css. Treat everything between their
    markers as foreign territory.
  * On any page this prompt edits, every image that was there before the run is
    still there after it, byte-identical, in the same place.

Our markers are CK_PLACED_VIDEOS (topic pages) and CK_VIDEO_LAYOUT +
CK_PLACED_VIDEOS (the stylesheet). Outside our own markers and the pages under
{VIDEOS_L2_DIR}, this prompt only ever ADDS.

============================
GOAL
============================

Generate and keep regenerating the published video pages of the site's videos
Level 2 ({VIDEOS_L2_DIR}, rooted at {VIDEOS_L2_PAGE}) from {HIERARCHY_FILE}. By
the time this prompt runs, the YAML is already built and holds all the data
needed: the cluster tree (level_3 / level_4 / level_5), and for every video its
cid, ipfs_pinned, sha256, file_path, inline ai_description, sidecar file paths
(transcription_file, ai_description_file, ocr_file), on_pages,
should_be_on_pages, also_filed_in, and site_level_2 / site_page bindings. This
prompt READS the YAML and WRITES pages. It does not grow or edit the YAML
(except recording published-page bookkeeping fields explicitly listed below).

Two kinds of pages get produced under {VIDEOS_L2_DIR}:

  * Cluster pages — one .mdx page per YAML node (level_3, level_4, level_5).
    Mostly navigation: a titled page with a table of contents linking to the
    node's peers, its child clusters, and its video pages.
  * Video pages — one .mdx page per video entry. Each hosts exactly one video
    player at the layout spec below, plus a written account of what the footage
    shows, who is speaking, what they assert, and how it connects to the rest
    of the investigation.

Two smaller outputs are produced OUTSIDE {VIDEOS_L2_DIR}, both on topic pages
elsewhere in {DOCS_DIR}:

  * The inline copies of each video on the pages that already host it (the
    YAML's on_pages) are made clickable so they link to that video's Videos
    page. See Stage 5.
  * Every video the YAML says BELONGS on a topic page and is not there yet (the
    YAML's should_be_on_pages) is placed on that page, inside one regenerated
    marked block at the bottom. See Stage 6. This is the stage that makes the
    hierarchy's plan real — without it the plan sits in the YAML forever and the
    footage stays invisible to a reader who never opens the Videos section.

This prompt runs MANY times. Pages will usually already exist from earlier
runs, written before additional data existed. Rerunning must read each
existing page in, then rewrite it against the current YAML data and the
current {LAYOUT_GUIDELINES}. The run is idempotent: same inputs, same pages,
same host-page anchors.

============================
THE STALE-DATA PRECONDITION (CHECK THIS BEFORE WRITING A SINGLE PAGE)
============================

{HIERARCHY_FILE} was created by copying images/images.yaml and converting the
KEYS to the video schema. Its DATA started out as the image corpus: file_paths
pointing at .jpg files, ai_description prose beginning "This image shows",
counts that count stills. {HIERARCHY_PROMPT} Stage 0 is what replaces that with
the real video corpus.

If this prompt runs against unconverted data it will publish roughly 1,700
pages that claim to be videos, carry no playable CID, and describe stills. That
is a large, public, hard-to-unwind mistake.

So before Stage 1 does anything, run this gate:

  * Count entries whose file_path ends in an image extension (.jpg .jpeg .png
    .gif .webp .heic). If that count is above zero, STOP. Report the count and
    tell the operator to run {HIERARCHY_PROMPT} Stage 0 first.
  * Count entries whose ai_description begins "This image". Same rule.
  * Count entries with a non-empty cid. If fewer than half the entries have
    one, STOP — the corpus has not been reconciled against {VIDEO_MANIFEST}.

The gate is a hard stop, not a warning. Do not publish "just the good ones" to
make progress.

STATUS AS OF 2026-07-23: {HIERARCHY_PROMPT} has run and the gate PASSES — 400
video entries in 1,559 nodes, 0 image file_paths, 0 "This image" prose, 372 of
400 entries carrying a CID. The gate still runs every time; a later hierarchy
pass could regress it.

============================
EMPTY NODES ARE NOT PUBLISHED
============================

The cluster tree in {HIERARCHY_FILE} mirrors the whole site's concept structure,
not just the parts that have footage. Most of it is empty: 1,559 nodes exist and
only about 170 have a video anywhere in their subtree. Generating a page for
every node would publish roughly 1,390 cluster pages whose entire table of
contents is a list of other empty pages — a maze with nothing at the end of it,
and a permanent drag on every build.

The rule:

  * A node with number_of_videos_recursive == 0 gets NO page, appears in NO
    table of contents, and gets NO row in {PAGES_CSV}. It is skipped, silently
    and consistently, at every level.
  * Recompute the count from the tree rather than trusting the stored field —
    the field is written by a different prompt and can go stale.
  * A node with videos somewhere below it is published even when it owns none
    directly; it is a real waypoint on the way to real footage.
  * If a page for a now-empty node exists from an earlier run, it is removed by
    the orphan sweep and counted as such.
  * The count of skipped-empty nodes is reported every run. A large swing in it
    between runs means the hierarchy moved and is worth a look.

This is a publishing decision, not a data decision. The empty nodes stay in the
YAML — they are the map of where footage could go, and {HIERARCHY_PROMPT} uses
them. They simply do not become pages until something fills them.

============================
KNOWLEDGE — READ FIRST, IN THIS ORDER
============================

At the very start of every run, read into the context window:

  1. {LAYOUT_GUIDELINES} — the standards file for video pages. It grows over
     time. Whatever rules it contains are followed and they OVERRIDE any
     conflicting rule in this prompt. Read it first, every run, before writing
     anything.
  2. {CK_FILE} — the master investigation file. This is very important
     knowledge for understanding the entire Charlie Kirk assassination, and it
     must be in the context window at the very start. It is the source of
     truth for what every concept, cluster, and open question actually is, and
     it is what the video write-ups are grounded in. It is 400K+ lines; the
     orchestrator loads the section headers plus the sections relevant to the
     clusters being processed, and each parallel agent loads the sections
     relevant to ITS clusters before writing a word.
  3. {CHARTER_FILE} — the videos_planning charter: audience model, level
     model, YAML schema, hard rules.
  4. {ASSESS_MANUAL} — the site-wide writing and layout guide. All published
     pages must meet it.
  5. {HIERARCHY_FILE} — parse fully. Index every node (_key, title, depth,
     parentage) and every video (cid, ipfs_pinned, sha256, file_path, sidecar
     paths, video_page, on_pages, should_be_on_pages, also_filed_in).
  6. {PAGES_CSV} — the master page index. Needed to resolve link targets and
     to keep in sync afterward.

============================
KNOWLEDGE — THE PAGE MODEL
============================

The site levels: Level 1 is the site home, Level 2 is the videos landing page
({VIDEOS_L2_PAGE}, url /Videos, left-bar label "Videos"). The YAML's level_3
nodes become the pages directly under it, level_4 under those, level_5 under
those. Video pages hang off whichever node owns the video.

Directory and file layout under {VIDEOS_L2_DIR}:

  {VIDEOS_L2_DIR}/overview.mdx                        the Level 2 landing page
  {VIDEOS_L2_DIR}/{L3_key}/overview.mdx               level_3 cluster page
  {VIDEOS_L2_DIR}/{L3_key}/{L4_key}/overview.mdx      level_4 cluster page
  {VIDEOS_L2_DIR}/{L3_key}/{L4_key}/{L5_key}/overview.mdx  level_5 cluster page
  {node dir}/Vid_{video_key}.mdx                      video page, in its node's dir

  * {L3_key} etc. are the node's _key from the YAML, used verbatim.
  * {video_key} is a stable per-video page key: derive it from the video's
    human meaning where one exists (the {VIDEO_MANIFEST} description, the
    speaker's name, the claim) rather than from the filename, because this
    corpus names files by X status id and "2067372027623715212" is not a page
    key. Sanitize to [A-Za-z0-9_], four words or less, and make it unique
    within the whole site by appending the first 7 chars of the status id or of
    the cid. Prefix the page filename with Vid_ so video pages are greppable
    and never collide with the images pipeline's Img_ pages.
  * Once minted, a video_key never changes across runs — on rerun, reuse the
    existing page's key (match existing pages to YAML entries by the cid /
    sha256 recorded in the page, see BOOKKEEPING below).
  * One hand-written page already lives at
    {VIDEOS_L2_DIR}/buckley-carlson-kash-patel-valhalla.mdx (page_key
    Videos_Buckley_Kash). It predates this pipeline, carries no ck_ frontmatter,
    and is NOT an orphan. Leave it alone. If its video appears in the YAML,
    record the collision in {FINDINGS_FILE} and let a human decide whether to
    fold it in; do not overwrite it and do not delete it.

A FILE PATH IS NOT A ROUTE. This bites every link that points at a page this
pipeline did not write — the on_pages entries, the node's site_page, and every
"How It Connects" target:

  * site/docs/index.md is served at "/", never at "/index".
  * A directory hub may carry a slug that differs from its folder name: the
    mirandize hub is /court/mirandize/mirandize-overview, not
    /court/mirandize/overview.
  * Section overviews are linked as /X/overview, not the bare /X.

So a link to any page outside {VIDEOS_L2_DIR} is resolved through the url_path
column of {PAGES_CSV}, and the path-derived form is only the fallback. Deriving
it from the path alone produces links that pass every local check and fail in
the build. Our own pages under {VIDEOS_L2_DIR} are the exception — this pipeline
chooses their layout, so their route is exactly their path.

Navigation rules (from the charter — a visitor never dead-ends):

  * Every cluster page carries a table of contents with hyperlinks to its
    PEERS (other nodes at its level under the same parent), its PARENT, its
    CHILD clusters, and its own video pages.
  * Every video page links to its parent cluster page, and to its peer video
    pages (previous / next within the cluster is enough).
  * The Level 2 landing page {VIDEOS_L2_PAGE} keeps its existing prose and
    gains/refreshes a table of contents section: a table linking to every
    level_3 page with its title and recursive video count. Regenerate only
    that TOC section between clear markers ({/* VIDEOS_TOC_START */} and
    {/* VIDEOS_TOC_END */}); never touch the prose outside the markers.
  * A cluster node that holds exactly ONE video and no child clusters is
    BYPASSED in every table of contents: its parent links straight to that one
    video page instead of to the cluster page. See the SINGLE-VIDEO NODES
    section below — this is a navigation rule, not a page-generation rule; the
    bypassed cluster page is still written.

Two arrival paths must both work (the charter's audience model): a visitor
browsing cold from the left bar down through the Level 2 page, and a visitor
arriving from a topic page elsewhere on the site who wants to WATCH the footage
for that topic, one click, already grouped.

============================
KNOWLEDGE — SINGLE-VIDEO NODES ARE BYPASSED IN NAVIGATION
============================

A cluster page earns its place only when it has something to choose between. A
level_4 that holds one video and nothing else is a page whose entire table of
contents is a single link — the visitor clicks it, reads one line, and clicks
again to reach the thing they came for. That middle click is removed.

The test — a cluster node is BYPASSED when both hold:

  * number_of_videos_recursive is 1, and
  * the node has no child clusters that survive this same test (a node whose
    only child is itself bypassed still resolves down to one video page).

Equivalently: the node's whole subtree resolves to exactly one video page.

What bypassing changes — LINKS ONLY:

  * The parent's table of contents does NOT list the bypassed node. In its
    place the parent lists the single VIDEO PAGE the node resolves to, linked
    directly, using the video page's title. Where the parent's TOC shows a
    count, the row shows 1 video.
  * Peer lists on sibling cluster pages apply the same substitution — a
    bypassed node never appears as a peer; its video page appears instead.
  * The bypassed node contributes its one video page to whatever TOC section
    the parent uses for videos, or to the child-cluster section with the video
    page in the slot; either is fine as long as the visitor sees one row that
    lands on the video.
  * The video page's back / parent link points to the NEAREST NON-BYPASSED
    ANCESTOR — not to the bypassed level_4. A visitor must never be sent onto a
    page the navigation just skipped.
  * Previous / next peer links for that video page are drawn from the same
    set the parent linked, so the video sits in the parent's sequence rather
    than alone in an empty cluster of one.

What bypassing does NOT change — the page is still built:

  * The bypassed cluster page is still generated at its normal path with its
    normal frontmatter (ck_node_key), its concept paragraph, and its own full
    TOC pointing at its parent and its one video page. It is reachable by URL
    and it builds; it simply has no inbound links from the hierarchy.
  * It still gets its row in {PAGES_CSV}, at its true level and parentage.
  * It is NOT an orphan and must never be deleted by the orphan sweep.
  * The video page keeps its real file path under the bypassed node's
    directory, and keeps ck_node_key set to the bypassed node's _key. The YAML
    binding is unchanged; only the links a visitor follows are.

Multi-video nodes are untouched. A level_4 with two or more videos is linked
from its parent exactly as before — that is the case the cluster page exists
for.

The rule applies at every depth by the same test: a level_5 holding one video
is bypassed by its level_4, and a level_3 holding one video is bypassed by the
Level 2 landing page's TOC, which then links straight to that video page.

============================
KNOWLEDGE — VIDEO PAGE LAYOUT SPEC
============================

Every video page hosts exactly one video. This prompt writes the WORDS on those
pages. The LAYOUT is owned by {NAV_PROMPT}, which implements it in the
generator's markup and in the marked CK_VIDEO_LAYOUT block in
{SITE_DIR}/internals/src/css/custom.css. {LAYOUT_GUIDELINES} is the authority
for what that layout must be; where it adds or contradicts anything below,
{LAYOUT_GUIDELINES} wins.

The spec is recorded here so prose written by this prompt suits the shape it
will be poured into:

  * No right bar. Set hide_table_of_contents: true in the frontmatter so the
    page renders without the right-hand TOC rail.
  * The player keeps the video's true aspect ratio. Never stretch, never crop.
  * The player sits IN THE PAGE, floated beside the prose, and scrolls up with
    the text. It is NOT pinned to the browser window.
  * The player is opaque and its controls are always visible and reachable.
  * Never autoplay, never loop. preload="metadata" only.
  * A poster frame is set when one exists.
  * The prose WRAPS AROUND the player: lines shorten beside it and resume full
    width below it. The prose column is not hand-capped to a percentage width,
    and nothing flows under or over the player.
  * The viewport defines the player's bounding box: up to 85% of the main-area
    width, and a max height of one screen with the control bar inside that
    ceiling. Much of this corpus is vertical phone video and will come out
    considerably narrower than 85%. That is correct.
  * Below the mobile breakpoint the player becomes a full-width block above the
    prose.
  * Because the prose wraps rather than sitting in a fixed narrow column, write
    normally: ordinary paragraphs, no manual line-length games.
  * Test at least one landscape video and one vertical video visually after any
    change to the layout implementation.

============================
KNOWLEDGE — HOSTING AND PLAYING THE VIDEO
============================

This is where the videos pipeline diverges hard from the images pipeline, and
getting it wrong is expensive.

VIDEO BYTES ARE NEVER COPIED INTO {SITE_DIR}/static. The images pipeline copies
each still to static/img/evidence/{sha256}.{ext}. Videos in this corpus run from
a few megabytes to 173MB, they are gitignored on purpose ({VIDEOS_DIR}/.gitignore
excludes *.mp4, *.mp3, *.mkv, *.avi, *.mov, *.wav, *.webm), and GitHub Pages is
not a video host. A Level 5 page plays its video from a PUBLIC IPFS GATEWAY,
addressed by the entry's cid:

  sources   https://ipfs.orbitor.dev/ipfs/{cid}
            https://gateway.pinata.cloud/ipfs/{cid}
            https://ipfs.filebase.io/ipfs/{cid}
            https://gw.ipfs-lens.dev/ipfs/{cid}

One <source> per gateway, in this order, from the single list in
videos_planning/generator/ipfs_gateways.py. dweb.link, ipfs.io and w3s.link were
retired in September 2026 (429 "switching to a service worker gateway only";
w3s.link just redirects to dweb.link) and must never be emitted again. After
changing the list, run videos_planning/generator/rewrite_video_gateways.py --write.

{cid} is the v1 base32 form, computed at generation time by ipfs_gateways.base32();
do not store it in the YAML, which keeps CIDv0.

Rules that follow:

  * An entry with cid "" gets its page written with the title, the write-up, and
    a plain "media pending" note where the player would be. No player element at
    all. A player pointed at an empty CID is a dead rectangle and is worse than
    an honest note.
  * AN ENTRY WITH ipfs_pinned FALSE GETS NO PLAYER EITHER. A CID alone does not
    make footage fetchable. Most of this corpus was hashed with `ipfs add -n`,
    which computes the CID without adding or announcing the blocks — as of
    2026-07-23, 58 of 372 CIDs are actually on the node and the other 314 exist
    nowhere on the network. A player pointed at one of those is dead for every
    visitor on earth, and looks perfect on this machine if IPFS Companion is
    running. That is the trap this pipeline is most likely to fall into.
    So an unpinned entry is treated exactly like a pending one, and gets the
    FULL page — title, complete write-up, sources, links, and its poster frame
    when one can be extracted — with an honest note in place of the player:

      Media pending. This footage is held locally and has not yet been
      published to IPFS, so it cannot be played here yet.
      CID (computed): Qm...

    The write-up is the point of the page and it publishes normally. Only the
    player waits. Report the count, and list the CIDs, so a later approved
    pinning job has its worklist; the same pages light up on the next run with
    no rewriting.
  * Do not pin as a side effect — pinning is irreversible in practice and is a
    separate, explicitly-approved job. Verify pin status against the node at run
    time (`ipfs pin ls --type=recursive`) rather than trusting the YAML field,
    which is written by a different prompt and goes stale as pinning happens.
  * THIRD-PARTY HOSTED VIDEO (YouTube, Rumble, X) has no CID. Its page carries
    the platform's own embed instead of our player, and says plainly where the
    video is hosted and that it can be removed by that platform at any time.
    {VIDEO_LIST_CSV} is the index of the YouTube-hosted material.
  * A POSTER FRAME may be served locally, because a poster is small: extract
    one frame (ffmpeg, a few seconds in, longest side 1600px, quality ~85) to
    {POSTER_DIR}/{sha256}.jpg and reference it as
    /img/video_posters/{sha256}.jpg. Skip when the target already exists
    (rerun-friendly). Skip entirely when there is no local file to extract from.
  * Verify the built site in a CLEAN BROWSER PROFILE WITH NO IPFS COMPANION
    EXTENSION. Companion silently rewrites gateway URLs to your local node, so a
    video that is not actually available to the public will look fine to you and
    be dead for every visitor. This is the single most likely way for this
    pipeline to ship broken pages.

============================
KNOWLEDGE — THE EXCLUSION GATE (NOT EVERYTHING IN THE YAML MAY BE PUBLISHED)
============================

The ban set is the UNION of two files, and both are read before anything is
generated:

  {BAN_VIDEOS_CSV} — {VIDEOS_DIR}/ban_videos.csv, the MASTER. One row per
    banned item: sha256, cid, file_path, banned, reason, date_added. Match an
    entry by sha256 first, then cid, then file_path; any match bans it. A row
    with banned=false is an explicit UN-BAN — the row stays as the record of
    the decision and the item publishes normally. New bans go here.
  {EXCLUDE_FILE} — the older one-identifier-per-line list. Still honoured.
    Never empty it to "move" an entry to the CSV; leave it and add the row.

The repo charter ({ROOT_DIR}/claude.md, "Banned Media") owns this contract and
also specifies a `banned:` boolean on every entry in {HIERARCHY_FILE}, synced
DOWN from the CSV by {HIERARCHY_PROMPT}. This prompt does not trust that field
and does not write it: it re-checks the identity against the two files itself,
every run, because the YAML is regenerated by a different prompt and a ban that
survives only in regenerated data is not a ban.

WHAT A BANNED VIDEO GETS — nothing, in every direction:

  * NO Level 5 page under {VIDEOS_L2_DIR}. If one exists it is DELETED, and its
    row is removed from {PAGES_CSV}.
  * NO poster frame under {POSTER_DIR}. Delete it if present.
  * NO placement on any other page. It is dropped from every should_be_on_pages
    worklist in Stage 6, and any existing placement — inside a CK_PLACED_VIDEOS
    block or hand-written — is removed from the host page.
  * NO LINK INTO IT from anywhere. No card, no poster thumbnail, no
    table-of-contents row, no "see also", no clickable-video wrapper in Stage 5.
    There is no Level 5 page to link to, so any surviving link is a broken link
    as well as an unwanted one. Cluster-page counts reflect what is actually
    published, not the raw YAML count.
  * NO PIN, ever, and no pinning job runs over a set that has not been filtered.

It is never removed from {HIERARCHY_FILE} — that file is the complete private
record and only grows. Banning is a publish-time gate, which is exactly why it
survives every regeneration of the hierarchy.

The images pipeline learned this the hard way: its mirror is a years-long
personal filing area and private material had been swept into it by accident —
bank and health-account dashboards, booking confirmations, video calls showing
named participants' faces. Eleven such entries were found published during its
first full run.

Video carries the same risk in a sharper form, and two additional ones:

  * Careful prose is NOT sufficient protection. A write-up can omit every name
    and the page is still an exposure, because the footage itself streams at a
    public URL. The media is the payload.
  * A video exposes bystanders continuously. A still catches one instant; a
    clip catches every face that walks through frame for its whole duration,
    plus every voice.
  * IPFS PUBLICATION IS NOT REVERSIBLE. Removing the page removes the link, not
    the content. Once a CID has been announced and fetched, it can be served by
    anyone who cached it. So exclusion has to happen BEFORE pinning, which is
    why nothing in this pipeline pins as a side effect.

The DECISION lives in the CSV, not in the YAML. {HIERARCHY_FILE} is read-only to
this prompt, so a ban recorded only there would be undone by the next hierarchy
pass. Recording it in {BAN_VIDEOS_CSV} makes it survive every regeneration, and
the YAML's `banned:` is a copy of that record — corroborating, never
authorising. If the YAML says banned and the files do not, or the reverse, STOP
and report the disagreement rather than publishing; it usually means
{HIERARCHY_PROMPT} has not been re-run since the CSV changed.

When a run finds material that should not be published, add a row to
{BAN_VIDEOS_CSV} with a reason and the date BEFORE the run ends, record it in
{FINDINGS_FILE}, and delete the page and the poster in the same run. Do not
leave it live until the next pass.

If {BAN_VIDEOS_CSV} does not exist yet, create it with the header row
sha256,cid,file_path,banned,reason,date_added and no data rows. If
{EXCLUDE_FILE} does not exist yet, create it with a header comment explaining
the format. Both before the first page is written.

============================
KNOWLEDGE — WRITING THE WRITE-UP
============================

Every video page gets a written account of what the footage is and what it is
related to. A video is not a still and the write-up is not a caption: it has to
handle a claim made out loud, over time, by a named person. Build it from ALL of
these sources:

  * THE TRANSCRIPTION — transcription_file is the most important input on the
    page. Read it. It gives you who speaks, what they assert, in what order, and
    in their own words. Quote from it, attributed and in quotation marks, where
    a quote carries the point better than a paraphrase.
  * The inline ai_description in the YAML and the ai_description_file sidecar —
    what is actually SEEN, as opposed to what is said. Read both when they
    exist.
  * The ocr_file when it exists — burned-in chyrons, slates, and captions.
  * The provenance in {VIDEO_MANIFEST} — source_url, source_author, added_date.
    Say where the clip came from. A visitor evaluating footage needs to know it
    is a phone capture of a broadcast reposted by an anonymous account, when
    that is what it is.
  * The hosting pages — this video often came from some other Level 2 or
    Level 3 document outside the videos Level 2. The YAML records these in
    on_pages (and the node's site_page / site_level_2). Read each hosting page,
    understand its topic, and explain how this video relates to the page(s) it
    was hosted on. A video may be hosted on multiple pages — cover each
    relationship.
  * {CK_FILE} — the bigger Charlie Kirk investigation. Use it to understand the
    footage, the area of the investigation it belongs to, and to describe that
    area accurately.

Structure every write-up around four questions, in this order:

  1. WHAT IS THIS — length, format, where it came from, who posted it.
  2. WHO IS SPEAKING AND WHAT DO THEY CLAIM — named, attributed, quoted.
     Approximate timestamps help a visitor find the moment ("about 1:10 in").
  3. WHAT THE FOOTAGE ACTUALLY SHOWS — separate from what is narrated over it.
     Very often a clip argues a thesis while its own frames show something
     narrower. Say so plainly when that is the case, and record it in
     {FINDINGS_FILE}.
  4. HOW IT CONNECTS — hyperlinks off to the other Level 2s and Level 3s of the
     site that this footage bears on. Link section overviews as /X/overview (not
     the bare /X); resolve every target against {PAGES_CSV} and prefer routes
     that are known to build.

Safe-writing rules for every write-up (mandatory, from the repo charter):

  * The word "defamation" must NOT appear anywhere in the article text.
  * Never write that any person KNEW anything before the crime, or DID
    anything immoral or illegal. Check the writing specifically for these two
    failure modes and remove them.
  * Never state as fact that a living person committed a crime unless
    court-proven. Use attribution language: "according to ...", "allegedly",
    "reportedly", "researchers have questioned ...". Frame suspicions as
    questions or reported claims, not conclusions.
  * THE SPEAKER'S ACCUSATION IS NOT OURS. This is the failure mode video adds
    that images do not have. A person in the footage says something defamatory
    about a third party; the page must report that the video contains the claim
    without adopting it. Write "In the clip, [speaker] states that ..." or
    "[speaker] alleges ...", never "[third party] did ...". Quote and attribute
    every accusation to the mouth it came out of.
  * Within those limits, include as MUCH information as possible. The rules
    constrain phrasing, not depth — do not solve the problem by writing less.
  * Raw unfiltered claims stay private in {CK_FILE} and the planning layer;
    only scrubbed writing is published.

Style: follow {ASSESS_MANUAL}. MDX gotcha: comments in .mdx must be
{/* ... */} — HTML <!-- --> comments fail the MDX compile and break deploy.

============================
KNOWLEDGE — BOOKKEEPING FIELDS ON PAGES
============================

So reruns can match pages to YAML entries and rewrite them safely, every
generated page embeds machine-readable frontmatter:

  * Cluster page frontmatter: title, plus custom fields
      ck_node_key: <_key>
  * Video page frontmatter: title, hide_table_of_contents: true, plus
      ck_video_cid: <cid>          the primary identity
      ck_video_sha256: <sha256>    "" when there is no local file
      ck_node_key: <owning node _key>

CID IS THE PRIMARY KEY, not sha256. Many entries in this corpus have a CID from
{VIDEO_MANIFEST} and an empty sha256, because the media file is gitignored and
absent on a fresh clone. Matching on sha256 first would strand those pages.

On rerun, an existing page is matched by ck_video_cid, then ck_video_sha256,
then ck_node_key, then filename. A rerun REFRESHES STRUCTURE BUT PRESERVES
PROSE:

  * Regenerated every run (always current, always safe to overwrite): slug and
    the mechanical frontmatter fields, the back button, the player element's
    src / poster / fallback source and its attributes, the layout classNames,
    the "Where This Video Appears" list, "Related Areas", the peer/child tables
    of contents, and the previous/next navigation.
  * Carried forward when the existing page has them: the page title,
    sidebar_label and frontmatter description, the prose under "## What This
    Video Shows", any transcript quotes and timestamps that were placed by
    hand, and the three paragraphs under "## About This Cluster" on cluster
    pages.

This matters because the writing pass costs far more than the generation pass
and is done against sources the generator never reads (transcription sidecars,
host pages, {CK_FILE}). A regeneration must never throw that away, and it must
never resurrect raw YAML text over prose that was deliberately scrubbed for
safe-writing reasons. Baseline (unenriched) prose IS replaced — the generator
recognizes its own boilerplate and refreshes it from current YAML data.

Pages under {VIDEOS_L2_DIR} that the current YAML no longer accounts for are
removed as orphans (they can only come from a renamed key or a removed node,
and leaving them strands dead pages in the build); their removal is counted and
reported every run. The two pre-existing hand-written pages — overview.mdx and
buckley-carlson-kash-patel-valhalla.mdx — are NEVER treated as orphans.

============================
KNOWLEDGE — CLICKABLE VIDEOS ON HOST PAGES (LINK BACK TO THE VIDEO PAGE)
============================

A video often appears twice on the site: once on its own Videos page (the
Level 5 page recorded in the YAML as video_page), and once — sometimes several
times — inline on the topic pages that first hosted it. Those topic pages are
recorded on the video entry as on_pages. The point of this knowledge is to give
a visitor reading Mic/AES.mdx who sees the clip a way to reach that exact
video's Videos page, where it is shown beside its full write-up and its place in
the hierarchy. It is the "topic arrival" path from the charter, wired at the
video level.

This is a link-only operation on the host pages. It changes nothing else on
them — not their prose, not their other embeds, not their captions, not their
layout — and it does NOT write {HIERARCHY_FILE}. The YAML is read-only here; the
stage only reads video_page and on_pages off each video and edits the host page.

Deriving the video page URL (the link target):

  * video_page is an absolute file path under {DOCS_DIR}, e.g.
    ~/BGit/Bryan_git/charlie-kirk/site/docs/Videos/Mic_Thesis/Vid_Candace_Mic_2067372.mdx
  * The site's routeBasePath is "/", so the site-relative URL is that path with
    the {DOCS_DIR} prefix removed and the .mdx suffix dropped:
      /Videos/Mic_Thesis/Vid_Candace_Mic_2067372
  * The link is site-relative: it starts with "/", carries no domain, and does
    NOT include /docs. Docusaurus resolves it; the build's broken-link checker
    validates it.
  * Confirm the derived URL against {PAGES_CSV} (the url_path recorded for the
    video page's page_key). If they disagree, trust {PAGES_CSV}.

Parsing on_pages:

  * on_pages is a list of hosting pages. Entries may be stored as stringified
    dicts, e.g. "{'page': '~/BGit/Bryan_git/charlie-kirk/site/docs/Mic/AES.mdx'}".
    Extract the page file path out of each entry. Deduplicate the list.
  * Each path is a real .mdx page under {DOCS_DIR}. Skip any path that does not
    resolve to a file on disk and record it as a problem.

Finding the right embed on the host page (the thing to link):

  Match in this priority order, and match ONLY this video, never a neighbor:

    1. IPFS CID — host pages embed video as https://ipfs.io/ipfs/{cid},
       https://{cid}.ipfs.dweb.link/..., or a bare /ipfs/{cid}. If the entry's
       cid appears in a <video> src, a <source> src, or a markdown link on the
       page, that is the match. CID is the strongest identity and host pages key
       on it today.
    2. Third-party video id — the YouTube watch id or Rumble slug in an
       <iframe src>.
    3. Original filename stem or a distinctive caption substring, as a last
       resort, only when it is unambiguous on that page. Be careful: this corpus
       names files by X status id, and a bare number is easy to mismatch.

  If none of these match on a page that on_pages claims hosts the video, the
  video is not actually embedded there — record it as a problem and move on. Do
  not invent an embed.

Making it clickable — VIDEO IS NOT AN IMAGE HERE:

  Wrapping a <video> element in an anchor does not work the way wrapping an
  <img> does. Clicking the player hits the controls, and browsers do not
  reliably fire the anchor. So:

  * <video> / <iframe> embeds: do NOT wrap the element. Add a short text link
    immediately beneath it instead, on its own line:
        <p><a href="URL">Full write-up and sources for this video →</a></p>
    Keep the player exactly as it is — every attribute, every source, unchanged.
  * A markdown link or a poster IMAGE standing in for the video (a thumbnail
    that links out) IS wrapped or retargeted the normal way, because that is a
    real image: ![alt](src) becomes [![alt](src)](URL).
  * Never alter a src, a poster, sizing, or a surrounding caption.

Idempotent and safe:

  * If the derived link already appears immediately beneath that embed, leave
    it — never add it twice.
  * If a human placed a different link there (e.g. to the original X post), do
    NOT clobber it; add ours alongside, or record it and skip. A deliberate
    external link is never destroyed.
  * Never point a video at a different video's page. One video, one target.
  * A BANNED video (in the ban set — {BAN_VIDEOS_CSV} or {EXCLUDE_FILE}) has no
    video page to link to, so it is never wrapped in an anchor. It is not just
    skipped: the footage must not be on the host page at all. Remove the embed
    and the poster, and report each removal with the ban reason.
  * A video hosted on N pages gets N host edits, one matched embed per page.

============================
KNOWLEDGE — SHOULD_BE_ON_PAGES: PLACING VIDEOS ONTO TOPIC PAGES
============================

Stage 5 makes a video clickable where it is ALREADY embedded. This knowledge
covers the far bigger job: putting the video on the pages where it belongs and
currently is not.

The YAML carries three properties per video that together describe the whole
picture:

  on_pages            where the video IS shown today. OBSERVED. Mostly empty.
  should_be_on_pages  where the video OUGHT to be shown. REASONED, produced by
                      Stage 13 of {HIERARCHY_PROMPT}. It is the COMPLETE desired
                      state and a superset of on_pages — never "extra pages
                      beyond on_pages".
  video_page          the video's own Level 5 page under {VIDEOS_L2_DIR}.

The work of this stage is exactly the set difference:

    should_be_on_pages  minus  what is already embedded on that page

Why it matters: almost every video in this corpus is published nowhere but its
own Videos page. A reader deep in Ballistics, or on the N1098L page, or on a
person's profile, should be offered the footage on the page they are reading.
That is the charter's "topic arrival" path served from the other direction —
instead of sending the visitor to the videos hierarchy, the evidence comes to
them, and one click takes them to the full write-up.

=== THE PROPERTY SHAPE ===

should_be_on_pages is a list of single-key mappings, each holding the full
tilde-rooted path to a real page file:

    should_be_on_pages:
      - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/Suspicious/Cause_of_Death/entrance-or-exit.mdx"
      - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/Suspicious/Five_Minutes/shirt-pull-at-the-shot.mdx"

The list is ordered best-match first. Every path was stat()-verified by Stage 13
before it was written. This stage re-stats anyway: a page can be renamed between
the two prompts. A path that no longer resolves is REPORTED, never guessed at
and never repaired by inventing a neighbour.

=== WHAT GETS PLACED: A CARD, NOT A PLAYER ===

THIS IS THE BIGGEST DIVERGENCE FROM THE IMAGES PIPELINE AND IT IS DELIBERATE.

The images pipeline places a gallery of up to twelve <img> elements at the
bottom of a topic page, each served from the site's own static directory. Doing
the equivalent with video would put up to twelve players on one page, each one
reaching a PUBLIC IPFS GATEWAY for a file that runs from 0.5MB to 173MB. Even at
preload="metadata" that is many cross-origin requests to a service we do not
control, on a page whose subject is not the video. It would be slow, it would be
flaky, and every unpinned CID among them renders as a dead rectangle.

So a placement is a CARD, not a player:

  * A poster thumbnail — /img/video_posters/{sha256}.jpg — when one exists,
    wrapped in an anchor to the video's own Videos page. A poster is a small
    local JPEG and is the only media a placement ever loads.
  * A title line, linked to the same Videos page.
  * A one-line caption saying what the footage shows and who is speaking.
  * A short duration and source note when the YAML has them ("4:19 · posted by
    @RealCandaceO, 17 Jun 2026").

The player itself lives on ONE page: the video's own Level 5 page. Everything
else links to it. That keeps the video hierarchy the single place a video is
actually served from, which is exactly what makes the hierarchy worth having.

  * NO POSTER AVAILABLE? Emit a text-only card — title link, caption, duration.
    Never emit an <img> whose src does not resolve, and never fall back to
    embedding the video to compensate for a missing thumbnail.
  * Generate missing posters BEFORE editing any page, the same way the Level 5
    pages do it: ffmpeg, a few seconds in, longest side 1600px, quality ~85, to
    {POSTER_DIR}/{sha256}.jpg. Skip when the file already exists. Skip entirely
    when there is no local media to extract a frame from — a gitignored corpus
    on a fresh clone will have many of these, and that is normal.
  * Every card carries the CID as a data-cid attribute so the content identity
    travels with the placement. A later pass that decides inline players are
    wanted somewhere can act on that attribute without re-deriving anything.

=== THE LINK TARGET ===

Clicking a card goes to that video's own Videos page — the Level 5 page recorded
on the entry as video_page. Derive the site-relative URL the same way Stage 5
does: strip the {DOCS_DIR} prefix, drop the .mdx suffix, keep the leading "/",
never include /docs and never a domain. Confirm against the url_path in
{PAGES_CSV}; where they disagree, {PAGES_CSV} wins.

A video with no video_page cannot be placed — there is nowhere for the click to
land, and the card would be a dead end offering footage a visitor cannot reach.
Skip it and report it.

=== WHERE ON THE PAGE (the bottom, in a marked block) ===

The cards go at the BOTTOM of the page, inside a generated block delimited by
MDX comment markers:

    {/* CK_PLACED_VIDEOS_START — generated, do not hand-edit */}
    ## Videos
    ... cards ...
    {/* CK_PLACED_VIDEOS_END */}

Rules for the block:

  * The marker name is CK_PLACED_VIDEOS. The images pipeline owns
    CK_PLACED_IMAGES on these same topic pages. A page may legitimately carry
    both blocks. NEVER read, rewrite, reorder, or delete the images pipeline's
    block — treat everything between its markers as foreign territory, exactly
    as the CSS blocks are treated.
  * Bottom placement is deliberate. The prose above was written by hand or by
    other prompts and must not be reflowed, re-sectioned, or interrupted.
    Appending is the only edit safe to repeat thousands of times.
  * The block is regenerated wholesale on every run: everything between OUR
    markers is replaced, everything outside them stays byte-identical. That is
    what makes the stage idempotent.
  * If our markers are absent, the block is appended at end of file. If they are
    present, it is replaced in place — it stays wherever a human moved it. If
    both blocks exist, ours goes after theirs on first write.
  * A page whose placement list comes out empty gets its block REMOVED, not left
    stale.
  * Never insert the block into a page under {VIDEOS_L2_DIR} (that Level 2 is
    the hierarchy itself), never under {DOCS_DIR}/Photos (the images pipeline's
    output), and never into {THIS_DIR} or any planning file.
  * MDX gotcha: comments must be {/* ... */}. An HTML <!-- --> comment fails the
    MDX compile and breaks the deploy.

=== NO DUPLICATES ===

A video already visible on a page is not placed again. Before building a page's
card list, read the page and drop any video whose cid (in either CIDv0 or base32
v1 form) or sha256 already appears anywhere in the file's text — that covers
existing inline players, IPFS embeds, iframe embeds, and anything a previous run
placed outside the markers. The check runs against the page text with OUR marked
block stripped out, so the block's own contents never suppress their own
regeneration. Stage 5 owns the linking of anything already embedded; this stage
must not double it up with a card.

=== PER-PAGE LOAD ===

Stage 13 aims at a ceiling of six videos per page but does not always land it.
Cap the block at SIX cards, keep the strongest (Stage 13 emits them best-first;
preserve YAML order), and report the overflow so the hierarchy pass can split
the page or drop the weak matches. Count videos already embedded on the page
against the cap.

=== UNPINNED AND MISSING CIDs ===

A card is a link, not a player, so a video with an unpinned or empty cid still
produces a WORKING card — the click lands on the Level 5 page, which is where
the honest "media pending" note already lives. Place it, and count it, and
report the number, but do not suppress the card: the write-up and the sources
are still worth reaching. Never let a card imply the footage is watchable when
the Level 5 page will say it is pending.

=== THE EXCLUSION GATE APPLIES HERE TOO ===

A video in the ban set — matched in {BAN_VIDEOS_CSV} by sha256, cid or
file_path, or listed in {EXCLUDE_FILE} — is never placed, whatever the YAML
says, and any existing placement of it is removed by the block regeneration. A
placement that sits OUTSIDE a CK_PLACED_VIDEOS block (hand-written, or left by
an older run) is removed too — block regeneration will not reach it, so it has
to be found and cut explicitly.

The gate is checked in this stage against those two files, not inherited on
trust from whatever wrote the YAML. The YAML's `banned:` corroborates; it does
not authorise. Nothing links into a banned video either: no card, no poster
thumbnail, no table-of-contents row. Removing a card does not unpublish the
footage — see the exclusion knowledge above; IPFS publication is not reversible,
which is why the ban must precede pinning.

=== THE CAPTION, AND SAFE WRITING ===

Each card gets a one-line caption so a reader knows what they are looking at
before they click. Build it from the entry's title and ai_description — first
sentence, trimmed — and, when the footage's point is something a person SAYS,
name the speaker and attribute it ("Candace Owens sets out a rigged-microphone
theory"), never assert it.

The caption is published text, so every safe-writing rule in WRITING THE
WRITE-UP binds it: no claim that a person knew anything beforehand, no claim of
immoral or illegal conduct in the site's own voice, every accusation attributed
to the speaker who made it, attribution language for anything contested, and the
word "defamation" never appears. An ai_description or a title that fails those
rules is rewritten for the caption, and the discrepancy is recorded in
{FINDINGS_FILE}.

Captions are generated text and are regenerated with the block. Nothing a human
writes inside the markers survives — that is the cost of a block that
regenerates, and it is why hand-written commentary about a video belongs above
the markers or on the video's own Videos page.

============================
STAGE 1 — SETUP AND READ
============================

* Run the STALE-DATA PRECONDITION gate. Stop if it fails.
* Read, in order: {LAYOUT_GUIDELINES}, {CK_FILE} (see READ FIRST for how),
  {CHARTER_FILE}, {ASSESS_MANUAL}, {HIERARCHY_FILE}, {PAGES_CSV},
  {VIDEO_MANIFEST}.
* Parse the YAML into an index: every node with depth, parent, _key, title,
  site bindings; every video with cid, ipfs_pinned, sha256, file_path,
  sidecars, video_page, on_pages, should_be_on_pages.
* Inventory the existing pages under {VIDEOS_L2_DIR}: for each, extract
  ck_node_key / ck_video_cid / ck_video_sha256 from frontmatter. Build the
  existing-page map. Mark overview.mdx and
  buckley-carlson-kash-patel-valhalla.mdx as protected.
* Verify {POSTER_DIR} exists (create if missing).
* BUILD THE BAN SET BEFORE ANYTHING ELSE IS PLANNED. Read {BAN_VIDEOS_CSV}
  (python3 csv module — the reason column contains commas and quoted text;
  create it with the header row if missing) and {EXCLUDE_FILE} (create it with a
  header comment if missing). The ban set is their union minus any CSV row
  explicitly marked banned=false. Index it three ways — by sha256, by cid, by
  expanded file_path — and hand it to every agent in Stage 2. Cross-check it
  against the YAML's `banned:` field and REPORT any disagreement; the files win.
  A malformed banned column is a STOP, not a guess.
* Then compute the DELETION WORKLIST: every existing page under {VIDEOS_L2_DIR}
  whose ck_video_cid or ck_video_sha256 is in the ban set, and every poster
  under {POSTER_DIR} named for a banned sha256. These are deleted in Stage 3
  before any new page is written, and their {PAGES_CSV} rows go in Stage 4. If
  this list is non-empty, banned footage is live on the site right now — say so
  at the top of the report, not buried in a count.

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

* Partition the level_3 nodes (each with its whole subtree) into up to
  {MAX_AGENTS} partitions, balanced by number_of_videos_recursive so the
  agents finish at roughly the same time. Fewer partitions when there are
  fewer level_3s or the corpus is small; up to 12 in parallel is expected and
  encouraged on full runs.
* A node subtree never splits across two agents — every video page and its
  cluster pages are written by one agent, so peer links within a subtree are
  consistent.
* Give every agent its OWN scratch subdirectory and tell it never to write to
  the shared scratchpad root. Agents independently invent the same helper
  filenames (apply.py, dump.py, out.json); in a 12-way parallel run those
  collide and one agent's file silently replaces another's mid-run. This has
  actually happened — isolate the directories up front.
* Cross-partition links (peer level_3s, links into other site sections) are
  resolvable from the YAML index and {PAGES_CSV}, which every agent receives.
* Balance by video count, not by page count. A single video with a 40-minute
  transcription costs an agent far more than five clips with none.

Output to stdout:
============================
STAGE 2 COMPLETE
Partitions: N   (list: partition -> level_3 _keys -> recursive video count)
============================

============================
STAGE 3 — PARALLEL PAGE GENERATION (UP TO {MAX_AGENTS} AGENTS)
============================

Launch the partitions as parallel agents in a single burst. Each agent
receives: its partition's YAML subtree(s), the full node index (for
cross-links), the layout spec, the {LAYOUT_GUIDELINES} contents, the writing
rules, the existing-page map for its subtree, and pointers to {CK_FILE},
{PAGES_CSV}, {ASSESS_MANUAL}, {VIDEO_MANIFEST}.

Each agent, for its subtree, working top-down:

* Read the {CK_FILE} sections relevant to its clusters.
* Compute the bypass set for its subtree first (see SINGLE-VIDEO NODES): every
  node whose subtree resolves to exactly one video page, and for each the video
  page it resolves to. Every TOC the agent writes is built against that set.
* For every cluster node: create or rewrite the cluster overview.mdx with
  title, a short concept paragraph (grounded in {CK_FILE}, safe-writing rules
  apply), and the full TOC — parent, peers, child clusters, video pages —
  with bypassed children and bypassed peers replaced by the video pages they
  resolve to. Bypassed nodes get their own page written exactly the same way;
  they are just absent from everyone else's TOC.
* For every video entry:
    * FIRST, check it against the ban set (the union of {BAN_VIDEOS_CSV} and
      {EXCLUDE_FILE}, matched by sha256, then cid, then file_path). A banned
      video gets NO page: if one exists in this node's dir, DELETE it, delete
      the poster under {POSTER_DIR}, hand the {PAGES_CSV} row to the
      orchestrator for Stage 4, and report the deletion with its ban reason.
      Then move to the next entry — write no page, extract no poster, mint no
      video_key, and leave the video out of every TOC the agent builds. Do this
      before the poster step, so a banned video's frames are never written into
      {POSTER_DIR} even momentarily.
    * Ensure the poster exists per HOSTING AND PLAYING THE VIDEO, when a local
      file is available to extract from.
    * If a page for this cid already exists in this node's dir, read it in
      first, then rewrite it. Otherwise mint the video_key and create it.
    * Apply the VIDEO PAGE LAYOUT SPEC exactly. Emit the player only when the
      entry has a cid AND that cid is pinned on the node; emit the platform
      embed for third-party video; emit the poster plus the "media pending" note
      in every other case, including a computed-but-unpinned cid.
    * Write the account per WRITING THE WRITE-UP — reading the transcription
      first, then the description and OCR sidecars, then the on_pages hosting
      pages, explaining the relationships, hyperlinking to related Level 2s and
      Level 3s.
    * Run the safe-writing check on the finished text: no "defamation" word,
      no prior-knowledge claims, no immoral/illegal-conduct claims in the
      site's own voice, every accusation in the footage attributed to the
      speaker who made it, attribution language throughout.
* Return to the orchestrator (do not write {PAGES_CSV} or {VIDEOS_L2_PAGE}
  directly — the orchestrator owns shared files to avoid write collisions):
    * The list of pages created / rewritten / unchanged, with for each: the
      page_key ( = node _key or video_key), parent_key, level, url_path,
      file_path, title, sidebar_label, directory, extension, line_count.
    * Any orphan pages, missing media, missing transcriptions, unpinned CIDs,
      or unresolvable links it hit.

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

* Regenerate the TOC section of {VIDEOS_L2_PAGE} between the
  VIDEOS_TOC_START / VIDEOS_TOC_END markers (insert the markers directly under
  the H1 if this is the first run). Table of every level_3: title linked to its
  page, recursive video count. A level_3 that is BYPASSED (whole subtree
  resolves to one video page) is listed with its title linked straight to that
  video page. Prose outside markers untouched — the existing overview prose
  about footage types and their limitations is good and it stays.
* The pre-existing buckley-carlson-kash-patel-valhalla.mdx is linked from the
  landing page as well, so it is not stranded, even though it is not a
  generated page.
* Merge every agent's page rows into {PAGES_CSV}: add rows for new pages,
  update rows for retitled/moved pages, following the CSV schema in
  {ROOT_DIR}/claude.md (page_key = node _key or video_key, parent_key = the
  parent node's _key — video pages parent to their owning node; level = node
  depth, or node depth + 1 for video pages). Never remove rows for pages that
  still exist; report rows whose files vanished instead of deleting blindly.

Output to stdout:
============================
STAGE 4 COMPLETE
Landing page TOC rows: N
pages.csv: N rows added, N updated, N flagged
============================

============================
STAGE 5 — MAKE HOST-PAGE VIDEOS CLICKABLE (LINK TO THE VIDEO PAGE)
============================

By this stage every video page under {VIDEOS_L2_DIR} exists (Stage 3 wrote
them), so the link targets are real. This stage walks the videos and wires each
one's inline copies on its host pages to point at its Videos page. See KNOWLEDGE
— CLICKABLE VIDEOS ON HOST PAGES for the URL derivation, the match order, and
the rule that a <video> element gets a text link beneath it rather than an
anchor wrapped around it; follow it exactly.

Work by host PAGE, not by video, so each file is opened and rewritten once even
when it hosts many videos. Build the plan first:

* Walk every video in the YAML index. Skip any in the ban set ({BAN_VIDEOS_CSV}
  or {EXCLUDE_FILE}) — and where such a video is embedded on a host page, remove
  the embed rather than merely leaving it unlinked. For the rest, derive the
  video-page URL from video_page
  (strip {DOCS_DIR}, drop .mdx; confirm against {PAGES_CSV}).
* Parse each video's on_pages into a deduplicated list of host .mdx file paths.
* Invert into a map: host page -> [ (cid, sha256, filename, video-page URL), ...]
  for every video that page hosts.

Then, for each host page in that map (partition across up to {MAX_AGENTS}
agents by host page; a host page is never split across agents):

* Read the page in.
* For each video the map assigns to this page, locate the one matching embed by
  the KNOWLEDGE match order (CID first, then third-party id, then
  filename/caption). If nothing matches, record it as "claimed host, not
  embedded" and skip.
* Add the link per the rules above. Obey the idempotency rules: skip if the
  link is already there; never clobber a pre-existing human-placed link to a
  different target (record those); never touch a sibling embed.
* Keep the page byte-identical everywhere else. The only edits are the added
  links.
* Do not modify pages under {VIDEOS_L2_DIR} here (those are Stage 3's), and do
  not modify {HIERARCHY_FILE}.

Host pages edited here live OUTSIDE {VIDEOS_L2_DIR} — this is the one stage that
writes elsewhere in {DOCS_DIR}, and it may only ever add a link near an
already-present embed. It creates no pages, deletes nothing, and moves nothing.

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

Stage 5 wired up the videos that were already embedded. This stage places the
ones that are not. It is the stage that makes the YAML's plan real: every video
the hierarchy says belongs on a topic page gets a card on that page, linked
through to its own Videos page. See KNOWLEDGE — SHOULD_BE_ON_PAGES for the card
format, the poster resolution, the link derivation, the block markers, the
dedupe rule, the per-page cap, and the caption rules; follow it exactly.

By this stage every video page under {VIDEOS_L2_DIR} exists (Stage 3 wrote them)
and {PAGES_CSV} is current (Stage 4), so both the link targets and their URLs
are real.

Build the plan first, working from the YAML index:

* Walk every video entry. Skip any in the ban set ({BAN_VIDEOS_CSV} or
  {EXCLUDE_FILE}) and count it. Skip any with an empty should_be_on_pages. Skip
  any with no video_page, and report it — a card with nowhere to land is not
  placed.
* Resolve each entry's poster: use {POSTER_DIR}/{sha256}.jpg when it exists;
  extract it now when there is local media to extract from; otherwise mark the
  card text-only. Do every extraction BEFORE any page is edited, so no page can
  end up referencing a poster that was never written.
* Derive the video-page URL from video_page and confirm it against {PAGES_CSV}.
* Re-stat every should_be_on_pages path. Drop and report any that no longer
  resolves, any under {VIDEOS_L2_DIR}, and any under {DOCS_DIR}/Photos.
* Invert into a map: host page -> ordered list of
  (cid, sha256, poster src or none, video-page URL, title, caption, duration,
  source note), YAML order preserved.

Then, for each host page in that map (partition across up to {MAX_AGENTS} agents
by host page; a host page is never split across agents):

* Read the page in. Strip OUR CK_PLACED_VIDEOS block from the text you test
  against — and leave any CK_PLACED_IMAGES block completely alone — then drop
  from the page's list every video whose cid (either form) or sha256 already
  appears in that stripped text. Those are already on the page and Stage 5 owns
  their linking.
* Apply the per-page cap of six, counting what is already embedded, keeping YAML
  order. Report the overflow.
* Emit the block: a "## Videos" heading and one card per video — the
  poster <img> wrapped in an anchor to the video's Videos URL, carrying
  data-cid, an alt drawn from the title, loading="lazy" — plus the linked title,
  the caption line, and the duration/source note. Text-only cards for entries
  with no poster.
* Replace the block between our markers if they exist; append it at end of file
  if they do not; remove it entirely if the page's list came out empty. Keep the
  page byte-identical everywhere outside our markers.
* Do not modify pages under {VIDEOS_L2_DIR} or {DOCS_DIR}/Photos, and do not
  modify {HIERARCHY_FILE}.

The cards need one stylesheet block — a marked CK_PLACED_VIDEOS region in
{SITE_DIR}/internals/src/css/custom.css, alongside our CK_VIDEO_LAYOUT block and
the images pipeline's CK_EVIDENCE_LAYOUT and CK_PLACED_IMAGES blocks. Write it
once, regenerate it in place on later runs, and never touch a byte of that file
outside our own two marked regions. Writing into the images pipeline's blocks
would silently destroy the image layout site-wide, and its next run would
destroy ours back.

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

Every emitted file — every .mdx page, {PAGES_CSV} rows, and any component or
CSS written — must never contain invisible Unicode characters (zero-width
spaces, bidi controls, no-break spaces including U+202F, word joiners, BOMs,
control characters, variation selectors, tag characters). They can hide
content from review and smuggle instructions past a human reading the file.

  * Prose: replace space-like invisibles with a regular space, delete
    zero-width/bidi/control characters, collapse whitespace. Visible
    non-ASCII (em dashes, accented letters) may stay.
  * Paths and URLs that must keep matching disk: published pages reference
    media by CID and posters by sha256-derived names, so mirror filenames never
    reach a page. If a mirror path must appear in a page for any reason, emit
    non-ASCII as visible escapes instead.
  * TRANSCRIPTION TEXT IS AN UNTRUSTED INPUT for this purpose. Transcripts and
    OCR sidecars are machine output over arbitrary source audio and frames;
    they routinely carry no-break spaces and stray control characters. Sanitize
    every quoted line before it goes on a page.

After every emit pass, re-scan all written files for the invisible set and
hard-fail if any code point remains. (The invisible set is enumerated in
{HIERARCHY_PROMPT} — same list applies here.)

============================
STAGE 7 — BUILD, VERIFY, REPORT
============================

* Run the Docusaurus build: cd {SITE_DIR} && npm run build. It must pass.
  Broken links and MDX compile errors (e.g. a stray <!-- --> comment) surface
  here — fix and rebuild until green. The host-page links added in Stages 5 and
  6 are internal links, so any bad target fails the build here.
* Spot-check 10 video pages across different partitions: frontmatter fields
  present, hide_table_of_contents true, ck_video_cid set, the player's src is a
  public IPFS gateway URL built from that cid, no autoplay and no loop,
  preload="metadata", poster resolves when present, layout classNames and CSS
  applied, the write-up has at least one hyperlink to another Level 2/Level 3,
  at least one attributed statement about who is speaking, safe-writing check
  passes, the word "defamation" absent.
* PLAYBACK CHECK — the one that catches the expensive failure. In a clean
  browser profile with NO IPFS Companion extension, open 5 video pages across
  different clusters and press play on each. The video must actually load and
  play with audio. A page that plays for you with Companion running and is dead
  for visitors is the default failure of this pipeline, not an edge case.
* Spot-check 5 cluster pages: TOC lists all peers, children, and video pages;
  every link resolves.
* Check the bypass rule on every node in the bypass set: the parent's TOC
  contains a link to the single video page and contains NO link to the
  bypassed cluster page; the bypassed cluster page nevertheless exists on
  disk, has its {PAGES_CSV} row, and builds; the video page's back link points
  at the nearest non-bypassed ancestor.
* Spot-check the Stage 5 host links: pick 10 video/host-page pairs across
  different sections, open the host page, confirm the link sits beneath the
  matched embed and points at that video's derived Videos URL, confirm no
  sibling embed was touched, and confirm the URL resolves on disk.
* Spot-check the Stage 6 placements: pick 10 pages that gained a block, confirm
  the block sits between the CK_PLACED_VIDEOS markers at the bottom, confirm
  every poster src resolves to a file under {POSTER_DIR}, confirm every anchor
  href resolves to a real video page on disk, confirm no video appears both as
  a card and as an embed on the same page, and confirm the page above the
  markers is byte-identical to before the run.
* Confirm every CK_PLACED_IMAGES block on every page edited this run is
  byte-identical to before the run. The images pipeline's blocks are foreign
  territory and a single edit to one is a failure of the run.
* BAN AUDIT — re-read {BAN_VIDEOS_CSV} and {EXCLUDE_FILE} here, at the end,
  rather than reusing the Stage 1 set; a row may have been added mid-run by this
  very run. Then assert all five, and fail the run on any of them:
    - No page under {VIDEOS_L2_DIR} carries a banned cid or sha256 in its
      ck_video_cid / ck_video_sha256 frontmatter.
    - No file under {POSTER_DIR} is named for a banned sha256.
    - No page anywhere under {DOCS_DIR} references a banned video — grep for the
      cid, the sha256, the gateway URL, and the original basename, inside and
      outside CK_PLACED_VIDEOS blocks.
    - No page anywhere links to a URL under /Videos that resolves to a banned
      video's page.
    - Nothing banned was pinned by this run. Nothing is pinned by this run at
      all, so the expected count is zero either way; state it explicitly.
  Grep for the identity, not for the page path: a stale link with no page behind
  it is still a link into banned material and is a broken link besides.
* Confirm {PAGES_CSV} row count change matches pages created.
* Run the invisible-Unicode scan over everything written this run (host pages
  edited in Stages 5 and 6 included).
* Confirm nothing outside {VIDEOS_L2_DIR}, {POSTER_DIR}, {PAGES_CSV}, the
  Stage 5 host pages (added links only), the Stage 6 host pages (our marked
  block only), and our marked CSS regions was modified. sidebars.ts untouched.
  {DOCS_DIR}/Photos untouched. {SITE_DIR}/static/img/evidence untouched.
* Confirm the CK_EVIDENCE_LAYOUT and CK_PLACED_IMAGES blocks in custom.css are
  intact — the images pipeline's layout must be exactly as it was.

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

* The STALE-DATA PRECONDITION gate runs before anything else and is a hard
  stop. Never publish pages from unconverted image data.
* {LAYOUT_GUIDELINES} is read at the very start of every run and its rules
  override this prompt where they conflict. It grows over time; never edit it
  from this prompt.
* {CK_FILE} is read into the context window at the very start — it is the
  knowledge base for understanding the entire assassination and every write-up
  is grounded in it.
* This prompt writes ONLY: pages under {VIDEOS_L2_DIR}, posters under
  {POSTER_DIR}, the marked TOC section of {VIDEOS_L2_PAGE}, our own marked
  regions of the shared CSS under {SITE_DIR}/internals/src/, {PAGES_CSV} rows,
  and — on the topic pages named in each video's on_pages /
  should_be_on_pages — links beside already-present video embeds (Stage 5) and
  the marked CK_PLACED_VIDEOS block (Stage 6). It never modifies
  {HIERARCHY_FILE}'s data (read-only input), never touches
  {SITE_DIR}/sidebars.ts, and never writes planning notes into the site or
  Docusaurus pages into {THIS_DIR}.
* Never write anything under {IMAGE_PLANNING_DIR}, {ROOT_DIR}/images,
  {DOCS_DIR}/Photos, or {SITE_DIR}/static/img/evidence. Never write into the
  CK_EVIDENCE_LAYOUT or CK_PLACED_IMAGES blocks in custom.css, and never into a
  CK_PLACED_IMAGES block on a topic page — ours are CK_VIDEO_LAYOUT and
  CK_PLACED_VIDEOS. Both pipelines edit the same topic pages and the same CSS
  file; each owns only its own markers and a single crossing destroys the other
  pipeline's output site-wide.
* NEVER copy video bytes into {SITE_DIR}/static. Video plays from a public IPFS
  gateway, addressed by cid. Posters are the only local media.
* Nothing is ever PINNED by this prompt. A player is emitted ONLY for a cid that
  is actually pinned on the node, verified at run time. A computed-but-unpinned
  cid gets the full page with a poster and an honest media-pending note, never a
  player, and its CID goes on the reported worklist.
* Empty nodes (number_of_videos_recursive == 0, recomputed from the tree) are
  never published: no page, no TOC entry, no {PAGES_CSV} row. They stay in the
  YAML as the map of where footage could go.
* VIDEOS ONLY, ADDITIVE ONLY (see SCOPE at the top). Never read or write
  {ROOT_DIR}/images or {IMAGE_PLANNING_DIR}. Never delete, move, resize,
  retarget, reorder, or reword an image, a caption, or an image block on any
  page this prompt edits — every image present before the run is present after
  it, byte-identical.
* Stage 5 adds a link BENEATH a <video>/<iframe>, never an anchor wrapped
  around it, because clicking a player hits its controls. Real images
  (thumbnails standing in for video) are wrapped the normal way. It changes no
  other content, creates and deletes nothing, never double-links, never
  clobbers a pre-existing link, and never links a video to any page but its own.
  Excluded videos are skipped.
* Stage 6 places every video the YAML's should_be_on_pages says belongs on a
  topic page and is not already embedded there, in a regenerated block between
  the CK_PLACED_VIDEOS markers at the BOTTOM of that page. Outside those markers
  the page stays byte-identical — the block is the only thing this prompt may
  add to a topic page's content. A placement is a CARD (poster thumbnail, linked
  title, one-line attributed caption) that links to the video's own Videos page,
  NEVER an inline player: the player lives on exactly one page and everything
  else links to it. Each card carries its CID as data-cid. Never duplicate a
  video already on the page, never exceed six per page, never place an excluded
  identity, and never place a video that has no video_page to land on.
  should_be_on_pages is the complete desired state and a superset of on_pages —
  not a list of extras.
* A cluster node whose subtree resolves to exactly ONE video page is bypassed
  in navigation: parents and peers link straight to that video page, never to
  the cluster page, and the video page's back link points at the nearest
  non-bypassed ancestor. The bypassed cluster page is still generated, still
  rows in {PAGES_CSV}, and is never treated as an orphan. Nodes with two or
  more videos are linked normally.
* overview.mdx and buckley-carlson-kash-patel-valhalla.mdx are protected. They
  are never deleted as orphans and their prose is never overwritten.
* Reruns refresh structure and PRESERVE authored prose (see BOOKKEEPING
  FIELDS ON PAGES). An enrichment pass's writing, and any safe-writing scrub
  applied to a page, must survive every later regeneration. Orphan removals
  are counted and reported.
* Every video page: one video, no right bar, aspect ratio true, no autoplay, no
  loop, preload metadata, controls reachable, up to 85% of main-area width and
  at most one screen of height.
* Every write-up: maximum information within the safe-writing rules; the word
  "defamation" never appears; no claims of prior knowledge or of
  immoral/illegal conduct in the site's own voice; every accusation made in the
  footage attributed to the speaker who made it; attribution language; links to
  related Level 2s and Level 3s as /X/overview-style routes verified against
  {PAGES_CSV}.
* Nothing in the ban set — the union of {BAN_VIDEOS_CSV} and {EXCLUDE_FILE},
  minus any CSV row marked banned=false — is ever published, placed, or pinned.
  The set is re-read from those two files every run, never inherited from the
  YAML. Anything found during a run that should not be public gets a row in
  {BAN_VIDEOS_CSV} with a reason before the run ends.
  Prose care does not substitute for withholding the footage, and IPFS
  publication is not reversible.
* The YAML is an input, not an authority on what is true or publishable. Its
  inline ai_description text is model output and has been wrong about people,
  places and events; its clustering sometimes files a video as supporting a
  thesis that the footage itself contradicts. Write what the footage actually
  shows, say so on the page when it differs from the filing and from what the
  speaker narrates, and record the discrepancy in {FINDINGS_FILE}.
* Up to {MAX_AGENTS} parallel agents, partitioned by YAML subtree; shared
  files ({PAGES_CSV}, {VIDEOS_L2_PAGE}) are written only by the orchestrator.
* No invisible Unicode in any emitted file — scan after every emit, and treat
  transcription and OCR text as untrusted input for that purpose.
* The build must pass, and the clean-profile playback check must pass, before
  the run is declared complete.

============================
BACKGROUND — ORIGINAL DIRECTIVE, KNOWLEDGE PRESERVED
============================

This section preserves the full intent of the directive this prompt was built
from, so no knowledge is lost even where a stage above already encodes it.

* Create this prompt file but do not run it yet. Learn from the entire
  videos_planning directory, and from {IMAGE_PLANNING_DIR} as prior art. By the
  time this prompt runs, the YAML file will already be built and it has all the
  data we need.
* In our charlie-kirk Docusaurus we have a Level 2 directory called videos
  ({VIDEOS_L2_DIR}). The goal is to create the .mdx pages under that videos
  Level 2 directory. The content comes from the YAML file.
* The goal is to host the video. These pages should not have a right bar. The
  video must be the right aspect ratio. There is a bounding area where the
  player goes; it fills however much is appropriate, no more than 85% of the
  width of the main area (the main area is the full browser width minus the
  left bar), and no taller than one screen with its controls inside that
  ceiling. The video often will not need the full width or the full height,
  depending on its aspect ratio — much of this corpus is vertical phone video.
* Each page carries a write-up: what the footage is, who is speaking, what they
  claim, what is actually shown, and what it is related to. The write-up has
  hyperlinks off to other Level 2s and Level 3s. The video often came from some
  other Level 2 or Level 3 document outside the videos Level 2; if that other
  page hosted this video, we want to understand that topic and explain this
  video and how it relates to the page it was hosted on. It might be hosted on
  multiple pages. The bigger Charlie Kirk investigation is used, to the best of
  our ability, to understand the footage and where it is hosted — that also
  gives context. We describe that area of the investigation.
* We make no defamatory claims. The word "defamation" should not appear in
  the article. The writing must not say anybody knew anything before the
  crime or did anything immoral or illegal — check the writing for exactly
  that — while including as much information as possible without causing
  those problems. Video adds one more: the person on camera makes accusations
  out loud. Report that the video contains the claim; never adopt it.
* When the YAML has pointers to the transcription file, the OCR file, the AI
  description file, or the inline AI description, we read those files to build
  the best write-up for the page. For video the transcription is the most
  important of them — it is what was said.
* layout_guidelines.txt lives in this directory. When this prompt runs, that
  file is read into the context window right away, and whatever rules it has
  are followed.
* When this prompt runs it can run up to 12 different agents in parallel, and
  it probably could and should: take different sections of the YAML file,
  partition them among the 12 agents, and each agent works its section —
  updating the pages under the Level 2 videos, making sure the video is
  playable on the page, the player size is correct, and the content written on
  the page is updated.
* This prompt will often run multiple times, so it has to rewrite pages. The
  pages are often pre-existing, written earlier before additional data was
  there, and the run needs to read them in.
* {CK_FILE} (~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt) is very
  important and must be read into the context window at the very start of the
  run. It is the knowledge needed to understand the entire Charlie Kirk
  assassination.
* The YAML carries a should_be_on_pages sub-hierarchy under every video, exactly
  parallel to on_pages: a list of `- page:` mappings holding full paths from ~.
  {HIERARCHY_PROMPT} figures out the right values and fills them in; THIS prompt
  reads them and gets those videos onto those websites' pages. Two prompts, one
  plan: one reasons, one publishes. The images pipeline established the split
  and this prompt reproduces it for video, with the one deliberate difference
  that a placed video is a card linking to its own page rather than a second
  player.
* This file was converted from the images page-generation prompt on 2026-07-23.
  The differences that matter and were NOT in the images version: video plays
  from IPFS and is never copied into the site; a missing or unpinned CID means
  no playable page; the transcription is the primary write-up source; a
  <video> gets a link beneath it rather than an anchor around it; the speaker's
  accusations are attributed and never adopted; and the two hand-written pages
  already under {VIDEOS_L2_DIR} are protected.
