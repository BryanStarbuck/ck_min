ROOT_DIR dir is ~/BGit/Bryan_git/charlie-kirk

THIS_DIR dir is {ROOT_DIR}/image_planning
IMAGES_DIR dir is {ROOT_DIR}/images
HIERARCHY_FILE is file {IMAGES_DIR}/images.yaml
  Moved 2026-07-22. It used to be {THIS_DIR}/hierarchy_images.yaml. That old
  name and that old location are both gone — the file is now images.yaml and it
  lives in {IMAGES_DIR}, not in {THIS_DIR}.
LAYOUT_GUIDELINES is file {THIS_DIR}/layout_guidelines.txt
CHARTER_FILE is file {THIS_DIR}/CLAUDE.md
EXCLUDE_FILE is file {THIS_DIR}/exclude_images.txt
BAN_IMAGES_CSV is file {IMAGES_DIR}/ban_images.csv
HIERARCHY_PROMPT is file {THIS_DIR}/p_update_image_hierarchy.md
FINDINGS_FILE is file {THIS_DIR}/findings_for_hierarchy.md

SITE_DIR dir is {ROOT_DIR}/site
DOCS_DIR dir is {SITE_DIR}/docs
PHOTOS_DIR dir is {DOCS_DIR}/Photos
IMAGES_L2_PAGE is file {PHOTOS_DIR}/overview.mdx
STATIC_IMG_DIR dir is {SITE_DIR}/static/img/evidence
PAGES_CSV is file {ROOT_DIR}/pages.csv
CK_FILE is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt
  (Real file. Moved 2026-09-19. ~/BGit/Bryan_git/charlie-kirk/Charlie_Kirk.txt is now a symlink to it —
   use that only to verify the location; always read and write the real path.)
ASSESS_MANUAL is file {ROOT_DIR}/prompts/Assess_Manual.md

MIRROR_DIR dir is ~/_Mirror/Politics/Charlie_Kirk_Mi
MIRROR_SIDECAR_DIR dir is ~/BGit/Bryan_git/personal_large_files_bridge/_Mirror/Politics/Charlie_Kirk_Mi
REPO_SIDECAR_DIR dir is {ROOT_DIR}/.lfbridge

The SIBLING VIDEO PIPELINE — read-only from here, never written by this prompt:
VIDEO_PLANNING_DIR dir is {ROOT_DIR}/videos_planning
VIDEOS_DIR dir is {ROOT_DIR}/videos
VIDEO_HIERARCHY_FILE is file {VIDEOS_DIR}/videos.yaml
VIDEOS_L2_DIR dir is {DOCS_DIR}/Videos

MAX_AGENTS is ... = 12

============================
GOAL
============================

Generate and keep regenerating the published image pages of the site's images
Level 2 (today the Photos section, rooted at {IMAGES_L2_PAGE}) from
{HIERARCHY_FILE}. By the time this prompt runs, the YAML is already built and
holds all the data needed: the cluster tree (level_3 / level_4 / level_5), and
for every image its sha256, file_path, inline ai_description, sidecar file
paths (ai_description_file, ocr_file, transcription_file), on_site_pages,
also_filed_in, and site_level_2 / site_page bindings. This prompt READS the
YAML and WRITES pages. It does not grow or edit the YAML (except recording
published-page bookkeeping fields explicitly listed below).

Two kinds of pages get produced under {PHOTOS_DIR}:

  * Cluster pages — one .mdx page per YAML node (level_3, level_4, level_5).
    Mostly navigation: a titled page with a table of contents linking to the
    node's peers, its child clusters, and its image pages.
  * Image pages — one .mdx page per image entry. Each hosts exactly one image
    at the layout spec below, plus a written description of what the image is,
    what it relates to, and hyperlinks into the rest of the investigation.

Every page this prompt writes hosts a STILL IMAGE. It never emits a media
player — see MEDIA-TYPE SCOPE below, which is a hard rule and is read before
any page is written.

Two smaller outputs are produced OUTSIDE {PHOTOS_DIR}, both driven off the YAML
and both read-only against it:

  * The inline copies of each image on its host topic pages (the YAML's
    on_pages) are made clickable so they link to that image's Photos image
    page. This is a link-only edit — a wrapping anchor around an already-present
    <img>. See Stage 5.
  * The images the YAML says OUGHT to appear on a topic page but do not yet
    (the YAML's should_be_on_pages) are PLACED on those pages, in a generated
    gallery block at the bottom of the page, each one clickable through to its
    Photos image page. See Stage 6. This is the stage that closes the gap
    between the plan and the site.

This prompt runs MANY times. Pages will usually already exist from earlier
runs, written before additional data existed. Rerunning must read each
existing page in, then rewrite it against the current YAML data and the
current {LAYOUT_GUIDELINES}. The run is idempotent: same inputs, same pages,
same host-page anchors.

============================
KNOWLEDGE — MEDIA-TYPE SCOPE: NEVER PUBLISH A VIDEO UNDER /Photos
============================

{PHOTOS_DIR} is the still-image Level 2. A page under it hosts one IMAGE. It
never hosts a playable video, because video has its own Level 2 with its own
plan, its own generator, and its own page layout:

  images                                videos
  ------                                ------
  {THIS_DIR}                            {VIDEO_PLANNING_DIR}
  {HIERARCHY_FILE}                      {VIDEO_HIERARCHY_FILE}
  {PHOTOS_DIR}                          {VIDEOS_L2_DIR}
  Img_*.mdx leaf pages                  Vid_*.mdx leaf pages
  ck_image_sha256 frontmatter           ck_video_cid + ck_video_sha256
  served from {STATIC_IMG_DIR}          played from a public IPFS gateway

THIS HAS ALREADY GONE WRONG, which is why the rule is stated this hard. Nine
pages under {PHOTOS_DIR}/Official_Narrative/Narrative_Shot_in_the_Heart/ are
published today as `Img_Photo_*.mdx`, carry `ck_image_cid: none` frontmatter,
render a `<video>` player off an IPFS gateway, and describe the footage under a
heading that reads "What This Image Shows." They are video pages living in the
image hierarchy. The cause is upstream — {HIERARCHY_FILE} carries 53 `video:`
items and 9 `image:` items whose CID is an .mp4 — and it is fixed upstream in
p_update_image_hierarchy.md. This prompt's job is to refuse to publish them
even if the YAML hands them over.

THE RULE.

  * Type every entry before writing its page. An entry is a video when its
    file_path or resolved src ends .mp4 / .mov / .webm / .m4v / .mkv / .avi;
    when its CID belongs to a VIDEO-FILENAMED record in
    {VIDEOS_DIR}/manifest.yaml or a video-filenamed block in
    {ROOT_DIR}/IPFS/ipfs.txt; or when the CID is embedded elsewhere on the site
    inside a <video>/<source> tag. Parse those two files by filename — both
    describe a mixed corpus, and scraping their CIDs wholesale types 70 image
    entries as video when only 9 are (measured 2026-07-23). Do NOT use
    {VIDEO_HIERARCHY_FILE} as an oracle yet: it is still a schema shell whose
    cids describe the inherited image corpus.
  * An entry typed as video gets NO page under {PHOTOS_DIR}, no static copy,
    no {PAGES_CSV} row, no TOC entry on its parent cluster page, and no
    placement by Stage 5 or Stage 6. It is skipped and counted.
  * NEVER emit a `<video>`, `<source>`, `<audio>`, or media-player `<iframe>`
    element into any file under {PHOTOS_DIR}. If the generator contains a code
    path that does, that code path is the defect — remove it rather than
    feeding around it. A generator that can render a video is a generator that
    will render a video the moment a mistyped entry reaches it.
  * An entry that cannot be typed confidently is UNKNOWN, and UNKNOWN is
    skipped, not published. An unresolvable extensionless IPFS CID with an
    empty sha256 is the exact shape of all 9 known bad entries; publishing it
    on the assumption it is an image is what produced them.
  * Never write anything under {VIDEOS_L2_DIR}, {VIDEOS_DIR}, or
    {VIDEO_PLANNING_DIR}. Read them freely — {VIDEO_HIERARCHY_FILE} is the
    best available oracle for whether a CID is a video.

ALREADY-PUBLISHED VIDEO PAGES. A page under {PHOTOS_DIR} that already contains
a `<video>` or `<source>` element is NOT treated as an orphan and is NOT
silently purged, even though the entry behind it is now skipped. Purging it
would delete a written, published page whose replacement under {VIDEOS_L2_DIR}
does not exist yet, and would leave every inbound link dead. Instead: leave the
file alone, count it, list each path in {FINDINGS_FILE} under

    == VIDEO PAGES PUBLISHED UNDER /Photos — HAND-OFF TO videos_planning ==

and report the count in the final summary. Migrating them to {VIDEOS_L2_DIR}
and removing them from {PHOTOS_DIR} is a separate, explicitly-approved job,
sequenced so the video pages exist before the image pages are withdrawn.

============================
KNOWLEDGE — READ FIRST, IN THIS ORDER
============================

At the very start of every run, read into the context window:

  1. {LAYOUT_GUIDELINES} — the standards file for images pages. It starts
     nearly empty and grows over time. Whatever rules it contains are followed
     and they OVERRIDE any conflicting rule in this prompt. Read it first,
     every run, before writing anything.
  2. {CK_FILE} — the master investigation file. This is very important
     knowledge for understanding the entire Charlie Kirk assassination, and it
     must be in the context window at the very start. It is the source of
     truth for what every concept, cluster, and open question actually is, and
     it is what the image descriptions are grounded in. It is 400K+ lines; the
     orchestrator loads the section headers plus the sections relevant to the
     clusters being processed, and each parallel agent loads the sections
     relevant to ITS clusters before writing a word.
  3. {CHARTER_FILE} — the image_planning charter: audience model, level
     model, YAML schema, hard rules.
  4. {ASSESS_MANUAL} — the site-wide writing and layout guide. All published
     pages must meet it.
  5. {HIERARCHY_FILE} — parse fully. Index every node (_key, title, depth,
     parentage) and every image (sha256, file_path, sidecar paths,
     on_site_pages, also_filed_in).
  6. {PAGES_CSV} — the master page index. Needed to resolve link targets and
     to keep in sync afterward.

============================
KNOWLEDGE — THE PAGE MODEL
============================

The site levels: Level 1 is the site home, Level 2 is the images landing page
({IMAGES_L2_PAGE}, url /Photos, left-bar label "Photos"). The YAML's level_3
nodes become the pages directly under it, level_4 under those, level_5 under
those. Image pages hang off whichever node owns the image.

Directory and file layout under {PHOTOS_DIR}:

  {PHOTOS_DIR}/overview.mdx                       the Level 2 landing page
  {PHOTOS_DIR}/{L3_key}/overview.mdx              level_3 cluster page
  {PHOTOS_DIR}/{L3_key}/{L4_key}/overview.mdx     level_4 cluster page
  {PHOTOS_DIR}/{L3_key}/{L4_key}/{L5_key}/overview.mdx   level_5 cluster page
  {node dir}/{image_key}.mdx                      image page, in its node's dir

  * {L3_key} etc. are the node's _key from the YAML, used verbatim.
  * {image_key} is a stable per-image page key: derive it from the image
    filename stem, sanitized to [A-Za-z0-9_], four words or less, made unique
    within the whole site by appending the first 8 hex chars of the sha256
    when the stem alone collides or is meaningless (screenshots, hash-named
    files). Once minted, an image_key never changes across runs — on rerun,
    reuse the existing page's key (match existing pages to YAML entries by
    the sha256 recorded in the page, see BOOKKEEPING below).

Navigation rules (from the charter — a visitor never dead-ends):

  * Every cluster page carries a table of contents with hyperlinks to its
    PEERS (other nodes at its level under the same parent), its PARENT, its
    CHILD clusters, and its own image pages.
  * Every image page links to its parent cluster page, and to its peer image
    pages (previous / next within the cluster is enough).
  * The Level 2 landing page {IMAGES_L2_PAGE} keeps its existing prose and
    gains/refreshes a table of contents section: a table linking to every
    level_3 page with its title and recursive image count. Regenerate only
    that TOC section between clear markers ({/* PHOTOS_TOC_START */} and
    {/* PHOTOS_TOC_END */}); never touch the prose outside the markers.
  * A cluster node that holds exactly ONE image and no child clusters is
    BYPASSED in every table of contents: its parent links straight to that one
    image page instead of to the cluster page. See the SINGLE-IMAGE NODES
    section below — this is a navigation rule, not a page-generation rule; the
    bypassed cluster page is still written.

Two arrival paths must both work (the charter's audience model): a visitor
browsing cold from the left bar down through the Level 2 page, and a visitor
arriving from a topic page elsewhere on the site who wants to SEE the evidence
for that topic, one click, already grouped.

============================
KNOWLEDGE — SINGLE-IMAGE NODES ARE BYPASSED IN NAVIGATION
============================

A cluster page earns its place only when it has something to choose between. A
level_4 that holds one image and nothing else is a page whose entire table of
contents is a single link — the visitor clicks it, reads one line, and clicks
again to reach the thing they came for. That middle click is removed.

The test — a cluster node is BYPASSED when both hold:

  * number_of_images_recursive is 1, and
  * the node has no child clusters that survive this same test (a node whose
    only child is itself bypassed still resolves down to one image page).

Equivalently: the node's whole subtree resolves to exactly one image page.

What bypassing changes — LINKS ONLY:

  * The parent's table of contents does NOT list the bypassed node. In its
    place the parent lists the single IMAGE PAGE the node resolves to, linked
    directly, using the image page's title. Where the parent's TOC shows a
    count, the row shows 1 image.
  * Peer lists on sibling cluster pages apply the same substitution — a
    bypassed node never appears as a peer; its image page appears instead.
  * The bypassed node contributes its one image page to whatever TOC section
    the parent uses for images, or to the child-cluster section with the image
    page in the slot; either is fine as long as the visitor sees one row that
    lands on the image.
  * The image page's back / parent link points to the NEAREST NON-BYPASSED
    ANCESTOR — the level_3 in the worked example below — not to the bypassed
    level_4. A visitor must never be sent onto a page the navigation just
    skipped.
  * Previous / next peer links for that image page are drawn from the same
    set the parent linked, so the image sits in the parent's sequence rather
    than alone in an empty cluster of one.

What bypassing does NOT change — the page is still built:

  * The bypassed cluster page is still generated at its normal path with its
    normal frontmatter (ck_node_key), its concept paragraph, and its own full
    TOC pointing at its parent and its one image page. It is reachable by URL
    and it builds; it simply has no inbound links from the hierarchy.
  * It still gets its row in {PAGES_CSV}, at its true level and parentage.
  * It is NOT an orphan and must never be deleted by the orphan sweep.
  * The image page keeps its real file path under the bypassed node's
    directory, and keeps ck_node_key set to the bypassed node's _key. The YAML
    binding is unchanged; only the links a visitor follows are.

Multi-image nodes are untouched. A level_4 with two or more images is linked
from its parent exactly as before — that is the case the cluster page exists
for.

Worked example (this is the shape that prompted the rule):

  level_3 "Table And Charlie" has a child
    level_4 "1776 Man" (_key Table_1776_Man, number_of_images_recursive: 1)
      one image, image_page .../Photos/Table_And_Charlie/Table_1776_Man/
      Img_Photo_24288a.mdx

  The Table_And_Charlie page links straight to Img_Photo_24288a.mdx, titled
  "1776 Man". It does not link to Table_1776_Man/overview.mdx. That overview
  page is still written, still in {PAGES_CSV}, still builds — it just is not
  in anybody's table of contents. Img_Photo_24288a.mdx's back link goes to
  Table_And_Charlie, skipping Table_1776_Man.

The rule applies at every depth by the same test: a level_5 holding one image
is bypassed by its level_4, and a level_3 holding one image is bypassed by the
Level 2 landing page's TOC, which then links straight to that image page.

============================
KNOWLEDGE — IMAGE PAGE LAYOUT SPEC
============================

Every image page hosts exactly one image. This prompt writes the WORDS on those
pages. The LAYOUT is owned by {THIS_DIR}/p_level2_update.md, which implements it
in the generator's markup and in the marked CK_EVIDENCE_LAYOUT block in
{SITE_DIR}/internals/src/css/custom.css. {LAYOUT_GUIDELINES} is the authority
for what that layout must be; where it adds or contradicts anything below,
{LAYOUT_GUIDELINES} wins.

The spec is recorded here so prose written by this prompt suits the shape it
will be poured into:

  * No right bar. Set hide_table_of_contents: true in the frontmatter so the
    page renders without the right-hand TOC rail.
  * The image keeps its true aspect ratio. Never stretch, never crop.
  * The image sits IN THE PAGE, floated to the right of the prose, and scrolls
    up with the text. It is NOT pinned to the browser window. An earlier
    version of this spec called for a viewport-fixed image at the bottom-right;
    that shipped, was wrong, and is superseded — the image stayed put while the
    page scrolled underneath it.
  * The image is opaque. Transparent source images get an opaque backing so
    page text is never visible through them.
  * The prose WRAPS AROUND the image: lines shorten beside it and resume full
    width below it. The prose column is not hand-capped to a percentage width,
    and nothing flows under or over the image.
  * The viewport still defines the image's bounding box, so it sizes sensibly:
    a share of the main-area width, and a max height under one screen so a tall
    image cannot swallow the page. Sizing by the viewport, anchored in the page.
  * Below the mobile breakpoint the image becomes a full-width block above the
    prose — there is no room for a side-by-side float.
  * Because the prose wraps rather than sitting in a fixed narrow column, write
    normally: ordinary paragraphs, no manual line-length games.
  * Test at least one wide image and one tall image visually after any change
    to the layout implementation (npm start, eyeball, or screenshot).

============================
KNOWLEDGE — THE EXCLUSION GATE (NOT EVERYTHING IN THE YAML MAY BE PUBLISHED)
============================

The BAN SET is the UNION of two files, and both are read before anything is
generated:

  {BAN_IMAGES_CSV} — {IMAGES_DIR}/ban_images.csv, the MASTER. One row per
    item: sha256, cid, file_path, banned, reason, date_added. Match an entry by
    sha256 first, then cid, then file_path; any match bans it. A row with
    banned=false is an explicit UN-BAN — the row stays as the record of the
    decision and its reason, and the item publishes normally. New bans go here.
  {EXCLUDE_FILE} — the older one-sha256-per-line list, with a comment saying
    why. Still honoured. Never empty it to "move" an entry into the CSV; leave
    it and add the row.

The repo charter ({ROOT_DIR}/claude.md, "Banned Media") owns this contract and
also specifies a `banned:` boolean on every entry in {HIERARCHY_FILE}, synced
DOWN from the CSV by {HIERARCHY_PROMPT} Stage 3B. This prompt does not trust
that field and does not write it: it re-checks each identity against the two
files itself, every run, because the YAML is regenerated by a different prompt
and a ban that survives only in regenerated data is not a ban. Treat a
`banned: true` in the YAML as a corroborating signal — if the YAML says banned
and the files do not, or the reverse, STOP and report the disagreement rather
than publishing.

WHAT A BANNED IMAGE GETS — nothing, in every direction:

  * NO Level 5 page under {PHOTOS_DIR}. If one exists it is DELETED, and its
    row is removed from {PAGES_CSV}.
  * NO served copy under {STATIC_IMG_DIR}. Delete it if present. A page that
    omits the accusation in its prose is not enough; the file itself must stop
    being served.
  * NO placement on any other page. It is dropped from every should_be_on_pages
    worklist in Stage 6, and any existing placement — inside a
    CK_PLACED_IMAGES block or hand-written — is removed from the host page.
  * NO LINK INTO IT from anywhere. No thumbnail, no card, no
    table-of-contents row, no "see also", no clickable-image wrapper in Stage 5.
    There is no Level 5 page to link to, so any surviving link is a broken link
    as well as an unwanted one. Cluster-page counts reflect what is actually
    published, not the raw YAML count.
  * NO PIN. Nothing here pins anyway, but any pinning job filters the ban set
    out before it runs. IPFS publication is not reversible in practice, so the
    gate holds before the pin, never after.

The entry itself is NEVER deleted from {HIERARCHY_FILE} — that file is the
complete private record and only grows. Banning is a publish-time gate, which
is exactly why it survives every regeneration of the hierarchy.

This gate exists because the mirror is a years-long personal filing area and
private material has been swept into it by accident — bank and health-account
dashboards, booking confirmations, billing portals, video calls showing named
participants' faces. Eleven such entries were found published during the first
full run. The second category is defamation: composite screenshots that stamp
an unproven criminal accusation about a named living person into the pixels,
where prose cannot soften it and cropping cannot remove it.

Two rules follow from that episode:

  * Careful prose is NOT sufficient protection. A description can omit every
    account number and name and the page is still an exposure, because the
    image itself is served full size at a public URL. The image is the payload.
  * The decision lives in the CSV, not in the YAML. {HIERARCHY_FILE} is
    read-only to this prompt, so a ban recorded only there would be undone by
    the next hierarchy pass. Recording it in {BAN_IMAGES_CSV} makes it survive
    every regeneration, and the YAML's `banned:` is a copy of that record.

When a run finds material that should not be published — private personal
documents, an unrelated third party's records, anything whose subject has no
connection to the investigation, an accusation burned into the image — add a
row to {BAN_IMAGES_CSV} with a reason and the date BEFORE the run ends, and
record it in {FINDINGS_FILE}. Then delete the page and the served copy in the
same run. Do not leave it live until the next pass.

============================
KNOWLEDGE — HOSTING THE IMAGE FILE
============================

The originals live outside the repo (mostly under {MIRROR_DIR}), so each
published image needs a servable copy:

  * Copy the original to {STATIC_IMG_DIR}/{sha256}.{ext} (lowercase original
    extension). The sha256 name is ASCII-safe, deduplicates automatically
    (cross-filed images copy once), and dodges the invisible-Unicode
    filenames the mirror contains (macOS screenshot names carry U+202F).
  * Reference it from the page as /img/evidence/{sha256}.{ext}.
  * Skip the copy when the target already exists (rerun-friendly).
  * If an entry has no local file but has an ipfs_url, embed the IPFS URL
    directly (ipfs.io primary; the site's existing IPFS embeds show the
    pattern). If it has neither, the image page is still generated with the
    description and a "media pending" note, so the hierarchy stays complete.
  * Do not commit multi-megabyte originals into {DOCS_DIR}; static assets go
    only under {STATIC_IMG_DIR}. If an original exceeds ~2MB, write a
    downscaled copy (longest side 2000px, quality ~85) instead — the page
    serves the web copy; the mirror keeps the original.

============================
KNOWLEDGE — WRITING THE DESCRIPTION
============================

Every image page gets a written description of what the image is and what it
is related to. Build it from ALL of these sources:

  * The inline ai_description in the YAML — the starting point.
  * The sidecar files pointed to by the YAML — when the entry has an
    ai_description_file, ocr_file, or transcription_file path, READ those
    files whenever they would improve the write-up. The OCR gives the literal
    on-screen text (screenshots, documents, chyrons) and is often the richest
    source; quote from it where it helps.
  * The hosting pages — this image often came from some other Level 2 or
    Level 3 document outside the images Level 2. The YAML records these in
    on_site_pages (and the node's site_page / site_level_2). Read each hosting
    page, understand its topic, and explain in the description how this image
    relates to the page(s) it was hosted on. An image may be hosted on
    multiple pages — cover each relationship.
  * {CK_FILE} — the bigger Charlie Kirk investigation. Use it to the best of
    our ability to understand the image, the area of the investigation it
    belongs to, and to describe that area accurately.

The description carries HYPERLINKS off to other Level 2s and Level 3s of the
site — the sections and pages this image connects to. Link section overviews
as /X/overview (not the bare /X); resolve every target against {PAGES_CSV}
and prefer routes that are known to build.

Safe-writing rules for every description (mandatory, from the repo charter):

  * The word "defamation" must NOT appear anywhere in the article text.
  * Never write that any person KNEW anything before the crime, or DID
    anything immoral or illegal. Check the writing specifically for these two
    failure modes and remove them.
  * Never state as fact that a living person committed a crime unless
    court-proven. Use attribution language: "according to ...", "allegedly",
    "reportedly", "researchers have questioned ...". Frame suspicions as
    questions or reported claims, not conclusions.
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
  * Image page frontmatter: title, hide_table_of_contents: true, plus
      ck_image_sha256: <sha256>
      ck_node_key: <owning node _key>

On rerun, an existing page is matched by ck_image_sha256 / ck_node_key first,
filename second. A rerun REFRESHES STRUCTURE BUT PRESERVES PROSE:

  * Regenerated every run (always current, always safe to overwrite): slug and
    the mechanical frontmatter fields, the back button, the image block's src
    and href, the layout classNames and the text column's maxWidth, the
    "Where This Image Appears" list, "Related Areas", the peer/child tables of
    contents, and the previous/next navigation.
  * Carried forward when the existing page has them: the page title,
    sidebar_label and frontmatter description, the img alt text, the prose
    under "## What This Image Shows" on image pages, and the three paragraphs
    under "## About This Cluster" on cluster pages.

This matters because the writing pass costs far more than the generation pass
and is done against sources the generator never reads (OCR sidecars, host
pages, {CK_FILE}). A regeneration must never throw that away, and it must
never resurrect raw YAML text over prose that was deliberately scrubbed for
safe-writing reasons. Baseline (unenriched) prose IS replaced — the generator
recognizes its own boilerplate and refreshes it from current YAML data.

Pages under {PHOTOS_DIR} that the current YAML no longer accounts for are
removed as orphans (they can only come from a renamed key or a removed node,
and leaving them strands dead pages in the build); their removal is counted
and reported every run.

============================
KNOWLEDGE — CLICKABLE IMAGES ON HOST PAGES (LINK BACK TO THE IMAGE PAGE)
============================

An image almost always appears twice on the site: once on its own Photos image
page (the Level 5 page recorded in the YAML as image_page), and once — often
several times — inline on the topic pages that first hosted it. Those topic
pages are recorded on the image entry as on_pages. The point of this knowledge
is to make that inline copy CLICKABLE: a visitor reading Mic/AES.mdx who sees
the evidence photo can click it and land on that exact image's Photos page,
where the image is shown full-size beside its full write-up and its place in the
hierarchy. It is the "topic arrival" path from the charter, wired at the image
level.

This is a link-only operation on the host pages. It changes nothing else on
them — not their prose, not their other images, not their captions, not their
layout — and it does NOT write {HIERARCHY_FILE}. The YAML is read-only here; the
stage only reads image_page and on_pages off each image and edits the host page.

Deriving the image page URL (the link target):

  * image_page is an absolute file path under {SITE_DIR}/docs, e.g.
    ~/BGit/Bryan_git/charlie-kirk/site/docs/Photos/FBI/Img_FBI_Shuts_down_b7009f.mdx
  * The site's routeBasePath is "/", so the site-relative URL is that path with
    the {SITE_DIR}/docs prefix removed and the .mdx suffix dropped:
      /Photos/FBI/Img_FBI_Shuts_down_b7009f
  * The link is site-relative: it starts with "/", carries no domain, and does
    NOT include /docs. Docusaurus resolves it; the build's broken-link checker
    validates it.
  * Confirm the derived URL against {PAGES_CSV} (the url_path recorded for the
    image page's page_key). If they disagree, trust {PAGES_CSV}.

Parsing on_pages:

  * on_pages is a list of hosting pages. Entries may be stored as stringified
    dicts, e.g. "{'page': '~/BGit/Bryan_git/charlie-kirk/site/docs/Mic/AES.mdx'}".
    Extract the page file path out of each entry. Deduplicate the list.
  * Each path is a real .mdx page under {SITE_DIR}/docs. Skip any path that does
    not resolve to a file on disk and record it as a problem.

Finding the right <img> on the host page (the thing to wrap):

  The same image can be embedded by different references on different pages.
  Match in this priority order, and match ONLY this image, never a neighbor:

    1. IPFS CID — host pages embed images as
         https://ipfs.io/ipfs/{cid}, https://{cid}.ipfs.dweb.link/...,
         or a bare /ipfs/{cid}. If the image entry's cid appears in an <img
         src> (or a markdown image URL) on the page, that is the match. CID is
         the strongest identity because host pages key on it today.
    2. Served static path — /img/evidence/{sha256}.{ext}.
    3. Original filename stem or a distinctive alt-text substring, as a last
       resort, only when it is unambiguous on that page.

  If none of these match on a page that on_pages claims hosts the image, the
  image is not actually embedded there — record it as a problem and move on. Do
  not invent an embed and do not add a bare text link.

Making it clickable (wrap, do not replace):

  * Markdown image:  ![alt](src)  becomes  [![alt](src)](URL)
  * MDX <img .../> :  wrap that single tag in an anchor, preserving every
    existing attribute and style verbatim:
        <a href="URL"><img ... /></a>
    Wrap only the one matched <img>; leave every sibling <img> in the same grid
    untouched.
  * Never alter the src, alt, sizing, or surrounding caption. The only change is
    the wrapping anchor.

Idempotent and safe:

  * If the matched <img> is already wrapped in an anchor whose href is exactly
    the derived URL, leave it — never double-wrap.
  * If it is wrapped in an anchor pointing somewhere else that a human placed
    (e.g. the original X post), do NOT clobber it; record it and skip, so a
    deliberate external link is never destroyed. (Report these for review.)
  * Never point an image at a different image's page. One image, one target.
  * A BANNED image (in the ban set — {BAN_IMAGES_CSV} or {EXCLUDE_FILE}) has no
    image page to link to, so it is never wrapped in an anchor. It is not just
    skipped: the image must not be on the host page at all. Remove the embed and
    the served copy, and report each removal with the ban reason.
  * An image hosted on N pages gets N host edits, one matched <img> per page.

============================
KNOWLEDGE — SHOULD_BE_ON_PAGES: PLACING IMAGES ONTO TOPIC PAGES
============================

Stage 5 makes an image clickable where it is ALREADY embedded. This knowledge
covers the far bigger job: putting the image on the pages where it belongs and
currently is not.

The YAML carries three properties per image that together describe the whole
picture:

  on_pages            where the image IS shown today. Observed. ~91% empty.
  should_be_on_pages  where the image OUGHT to be shown. Reasoned, produced by
                      Stage 11 of {THIS_DIR}/p_update_image_hierarchy.md. It is
                      the COMPLETE desired state and is a superset of on_pages —
                      never "extra pages beyond on_pages".
  image_page          the image's own Level 5 page under {PHOTOS_DIR}.

The work of this stage is exactly the set difference:

    should_be_on_pages  minus  what is already embedded on that page

Why it matters: most evidence images in this corpus are published nowhere but
their own Photos page. A reader deep in Ballistics, or on the N1098L page, or on
a person's profile, should SEE the evidence on the page they are reading. That
is the charter's "topic arrival" path served from the other direction — instead
of sending the visitor to the images hierarchy, the evidence comes to them, and
one click on it takes them to the full write-up.

=== THE PROPERTY SHAPE ===

should_be_on_pages is a list of single-key mappings, each holding the full
tilde-rooted path to a real page file:

    should_be_on_pages:
      - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/Suspicious/Cause_of_Death/entrance-or-exit.mdx"
      - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/Suspicious/Five_Minutes/shirt-pull-at-the-shot.mdx"

Every path is stat()-verified by Stage 11 before it is written. This stage
re-stats anyway: a page can be renamed between the two prompts. A path that no
longer resolves is REPORTED, never guessed at and never repaired by inventing a
neighbour.

=== WHERE THE IMAGE IS HOSTED (the src) ===

The image needs a URL that actually serves bytes to a visitor. Resolve the src
in this order, per image, and record which branch was taken:

  1. Served static copy — /img/evidence/{sha256}.{ext} — when the file exists
     under {STATIC_IMG_DIR}. This is the site's established convention (every
     existing evidence <img> outside {PHOTOS_DIR} already uses it) and it is
     what the Photos image pages themselves serve.
  2. The image's own local original, if a static copy is missing but file_path
     resolves on disk: copy it into {STATIC_IMG_DIR}/{sha256}.{ext} exactly as
     HOSTING THE IMAGE FILE describes (downscale over ~2MB), then use branch 1.
  3. The IPFS gateway — https://ipfs.io/ipfs/{cid} — when there is no local
     file at all. Entries with no file_path are IPFS-native; their bytes exist
     only on the network.
  4. Nothing resolves: skip the placement and report it. Never emit an <img>
     whose src cannot serve.

  THE CID CAVEAT, MEASURED, NOT ASSUMED. An unpinned CID does not resolve from
  a public gateway. Verified 2026-07-23: a pinned CID returned 200 from
  ipfs.io, an unpinned one timed out at 504. Only a small minority of entries
  carry ipfs_pinned: true. So the CID is NOT usable as the general src — it is
  correct only for pinned, file-less entries, which is exactly branch 3.
  Every emitted <img> nevertheless carries the CID as a data-cid attribute, so
  the content identity travels with the embed and a later pinning pass can
  switch the src over by rewriting one attribute pair. When the corpus is fully
  pinned, branch 3 may be promoted ahead of branch 1 by changing that order
  here — nothing else in the stage has to change.

=== THE LINK TARGET ===

Clicking the placed image goes to that image's own Photos page — the Level 5
page recorded on the entry as image_page. Derive the site-relative URL the same
way Stage 5 does: strip the {DOCS_DIR} prefix, drop the .mdx suffix, keep the
leading "/", never include /docs and never a domain. Confirm against the
url_path in {PAGES_CSV}; where they disagree, {PAGES_CSV} wins.

An image with no image_page cannot be placed — there is nowhere for the click
to land. Skip it and report it; do not place a dead-end image.

=== WHERE ON THE PAGE (the bottom, in a marked block) ===

The images go at the BOTTOM of the page, inside a generated block delimited by
MDX comment markers:

    {/* CK_PLACED_IMAGES_START — generated, do not hand-edit */}
    ## Images
    ... gallery ...
    {/* CK_PLACED_IMAGES_END */}

Rules for the block:

  * Bottom placement is deliberate. The prose above it was written by hand or
    by other prompts and must not be reflowed, re-sectioned, or interrupted.
    Appending is the only edit that is safe to repeat thousands of times.
  * The block is regenerated wholesale on every run: everything between the
    markers is replaced, everything outside them is left byte-identical. That
    is what makes the stage idempotent.
  * If the markers are absent, the block is appended at end of file. If they
    are present, it is replaced in place — it stays wherever a human moved it.
  * A page whose placement list comes out empty gets its block REMOVED, not
    left stale.
  * Never insert the block into a page under {PHOTOS_DIR} (that Level 2 is the
    hierarchy itself), and never into {THIS_DIR} or any planning file.
  * MDX gotcha: comments must be {/* ... */}. An HTML <!-- --> comment fails the
    MDX compile and breaks the deploy.

=== NO DUPLICATES ===

An image already visible on a page is not placed again. Before building a
page's gallery, read the page and drop any image whose sha256 OR cid already
appears anywhere in the file's text — that covers the existing inline
/img/evidence/{sha}.{ext} embeds, any IPFS embed, and anything a previous run of
this stage placed outside the markers. The check runs against the page text with
the marked block stripped out, so the block's own contents never suppress their
own regeneration.

=== PER-PAGE LOAD ===

Stage 11 aims at a ceiling of 12 images per page but does not always land it —
some pages carry 20+ assignments. A page is not an album. Cap the gallery at 12
placements, keep the strongest (Stage 11 emits them best-first; preserve YAML
order), and report the overflow so the hierarchy pass can split the page or drop
the weak matches. Count images already embedded on the page against the cap.

=== THE EXCLUSION GATE APPLIES HERE TOO ===

An image in the ban set — matched in {BAN_IMAGES_CSV} by sha256, cid or
file_path, or listed in {EXCLUDE_FILE} — is never placed, whatever the YAML
says, and any existing placement of it is removed by the block regeneration. A
placement that sits OUTSIDE a CK_PLACED_IMAGES block (hand-written, or left by
an older run) is removed too — block regeneration will not reach it, so it has
to be found and cut explicitly.

The gate is checked in this stage against those two files, not inherited on
trust from whatever wrote the YAML. The YAML's `banned:` corroborates; it does
not authorise. Nothing links into a banned image either: no card, no thumbnail,
no table-of-contents row.

=== THE CAPTION, AND SAFE WRITING ===

Each placed image gets a one-line caption so a reader knows what they are
looking at before they click. Build it from the entry's ai_description —
first sentence, trimmed — and end it with the link to the full write-up.
The caption is published text, so every safe-writing rule in WRITING THE
DESCRIPTION binds it: no claim that a person knew anything beforehand, no claim
of immoral or illegal conduct, attribution language for anything contested, and
the word "defamation" never appears. An ai_description that fails those rules is
rewritten for the caption, and the discrepancy is recorded in {FINDINGS_FILE}.

Captions are generated text and are regenerated with the block. Nothing a human
writes inside the markers survives — that is the cost of a block that
regenerates, and it is why hand-written commentary about an image belongs above
the markers or on the image's own Photos page.

============================
STAGE 1 — SETUP AND READ
============================

* Read, in order: {LAYOUT_GUIDELINES}, {CK_FILE} (see READ FIRST for how),
  {CHARTER_FILE}, {ASSESS_MANUAL}, {HIERARCHY_FILE}, {PAGES_CSV}.
* Parse the YAML into an index: every node with depth, parent, _key, title,
  site bindings; every image with sha256, file_path, sidecars, on_site_pages.
* Inventory the existing pages under {PHOTOS_DIR}: for each, extract
  ck_node_key / ck_image_sha256 from frontmatter. Build the existing-page map.
* Verify {STATIC_IMG_DIR} exists (create if missing).
* BUILD THE BAN SET BEFORE ANYTHING ELSE IS PLANNED. Read {BAN_IMAGES_CSV}
  (python3 csv module — the reason column contains commas and quoted text) and
  {EXCLUDE_FILE}. The ban set is their union minus any CSV row explicitly marked
  banned=false. Index it three ways — by sha256, by cid, by expanded file_path —
  and hand it to every agent in Stage 2. Cross-check it against the YAML's
  `banned:` field and REPORT any disagreement; the files win, and a
  disagreement usually means {HIERARCHY_PROMPT} has not been re-run since the
  CSV changed. A malformed banned column is a STOP, not a guess.
* Then compute the DELETION WORKLIST: every existing page under {PHOTOS_DIR}
  whose ck_image_sha256 is in the ban set, and every file under
  {STATIC_IMG_DIR} named for a banned sha256. These are deleted in Stage 3
  before any new page is written, and their {PAGES_CSV} rows go in Stage 4. If
  this list is non-empty, banned material is live on the site right now — say so
  at the top of the report, not buried in a count.

Output to stdout:
============================
STAGE 1 COMPLETE
Layout guidelines lines: N
YAML nodes: N level_3 / N level_4 / N level_5   images: N unique sha256
Existing pages found: N cluster / N image
Ban set: N identities ({BAN_IMAGES_CSV} N rows, {EXCLUDE_FILE} N lines, N un-bans)
YAML banned: disagreeing with the files: N (listed — the files win)
DELETION WORKLIST: N live pages + N served copies for banned images
============================

============================
STAGE 2 — PARTITION THE WORK
============================

* Partition the level_3 nodes (each with its whole subtree) into up to
  {MAX_AGENTS} partitions, balanced by number_of_images_recursive so the
  agents finish at roughly the same time. Fewer partitions when there are
  fewer level_3s or the corpus is small; up to 12 in parallel is expected and
  encouraged on full runs.
* A node subtree never splits across two agents — every image page and its
  cluster pages are written by one agent, so peer links within a subtree are
  consistent.
* Give every agent its OWN scratch subdirectory and tell it never to write to
  the shared scratchpad root. Agents independently invent the same helper
  filenames (apply.py, dump.py, out.json); in a 12-way parallel run those
  collide and one agent's file silently replaces another's mid-run. This has
  actually happened — isolate the directories up front.
* Cross-partition links (peer level_3s, links into other site sections) are
  resolvable from the YAML index and {PAGES_CSV}, which every agent receives.

Output to stdout:
============================
STAGE 2 COMPLETE
Partitions: N   (list: partition -> level_3 _keys -> recursive image count)
============================

============================
STAGE 3 — PARALLEL PAGE GENERATION (UP TO {MAX_AGENTS} AGENTS)
============================

Launch the partitions as parallel agents in a single burst. Each agent
receives: its partition's YAML subtree(s), the full node index (for
cross-links), the layout spec, the {LAYOUT_GUIDELINES} contents, the writing
rules, the existing-page map for its subtree, and pointers to {CK_FILE},
{PAGES_CSV}, {ASSESS_MANUAL}.

Each agent, for its subtree, working top-down:

* Read the {CK_FILE} sections relevant to its clusters.
* Compute the bypass set for its subtree first (see SINGLE-IMAGE NODES): every
  node whose subtree resolves to exactly one image page, and for each the image
  page it resolves to. Every TOC the agent writes is built against that set.
* For every cluster node: create or rewrite the cluster overview.mdx with
  title, a short concept paragraph (grounded in {CK_FILE}, safe-writing rules
  apply), and the full TOC — parent, peers, child clusters, image pages —
  with bypassed children and bypassed peers replaced by the image pages they
  resolve to. Bypassed nodes get their own page written exactly the same way;
  they are just absent from everyone else's TOC.
* For every image entry:
    * FIRST, check it against the ban set. A banned image gets NO page: if one
      exists in this node's dir, DELETE it, delete the served copy under
      {STATIC_IMG_DIR}, hand the {PAGES_CSV} row to the orchestrator for Stage 4,
      and report the deletion with its ban reason. Then move to the next entry —
      write no page, copy no file, mint no image_key, and leave the image out of
      every TOC the agent builds. Do this before the static copy, so a banned
      image is never written into {STATIC_IMG_DIR} even momentarily.
    * Ensure the static copy exists per HOSTING THE IMAGE FILE.
    * If a page for this sha256 already exists in this node's dir, read it in
      first, then rewrite it. Otherwise mint the image_key and create it.
    * Apply the IMAGE PAGE LAYOUT SPEC exactly.
    * Write the description per WRITING THE DESCRIPTION — reading the
      sidecar OCR / ai_description files when they help, reading the
      on_site_pages hosting pages, explaining the relationships, hyperlinking
      to related Level 2s and Level 3s.
    * Run the safe-writing check on the finished text: no "defamation" word,
      no prior-knowledge claims, no immoral/illegal-conduct claims about any
      person, attribution language throughout.
* Return to the orchestrator (do not write {PAGES_CSV} or {IMAGES_L2_PAGE}
  directly — the orchestrator owns shared files to avoid write collisions):
    * The list of pages created / rewritten / unchanged, with for each: the
      page_key ( = node _key or image_key), parent_key, level, url_path,
      file_path, title, sidebar_label, directory, extension, line_count.
    * Any orphan pages, missing originals, missing sidecars, or unresolvable
      links it hit.

Output to stdout (after all agents return):
============================
STAGE 3 COMPLETE
Agents run: N
Cluster pages: N created, N rewritten (N bypassed in navigation)
Image pages: N created, N rewritten
Banned images skipped (no page written): N
Banned images UN-PUBLISHED this run: N pages deleted, N served copies deleted
  (each listed with sha256, page path, and ban reason)
Static copies written: N (N downscaled)   IPFS embeds: N   media pending: N
Problems reported: N (list)
============================

============================
STAGE 4 — SHARED FILES: LANDING PAGE AND PAGES.CSV
============================

Orchestrator only, single-threaded:

* Regenerate the TOC section of {IMAGES_L2_PAGE} between the
  PHOTOS_TOC_START / PHOTOS_TOC_END markers (insert the markers before the
  final paragraph if this is the first run). Table of every level_3: title
  linked to its page, recursive image count. A level_3 that is BYPASSED (whole
  subtree resolves to one image page) is listed with its title linked straight
  to that image page. Prose outside markers untouched.
* Merge every agent's page rows into {PAGES_CSV}: add rows for new pages,
  update rows for retitled/moved pages, following the CSV schema in
  {ROOT_DIR}/claude.md (page_key = node _key or image_key, parent_key = the
  parent node's _key — image pages parent to their owning node; level = node
  depth, or node depth + 1 for image pages). Never remove rows for pages that
  still exist; report rows whose files vanished instead of deleting blindly.

Output to stdout:
============================
STAGE 4 COMPLETE
Landing page TOC rows: N
pages.csv: N rows added, N updated, N flagged
============================

============================
STAGE 5 — MAKE HOST-PAGE IMAGES CLICKABLE (LINK TO THE IMAGE PAGE)
============================

By this stage every image page under {PHOTOS_DIR} exists (Stage 3 wrote them),
so the link targets are real. This stage walks the images and wires each one's
inline copies on its host pages to point at its Photos image page. See KNOWLEDGE
— CLICKABLE IMAGES ON HOST PAGES for the URL derivation, the match order, and
the wrap rules; follow it exactly.

Work by host PAGE, not by image, so each file is opened and rewritten once even
when it hosts many images. Build the plan first:

* Walk every image in the YAML index. Skip any in the ban set ({BAN_IMAGES_CSV}
  or {EXCLUDE_FILE}) — and where such an image is embedded on a host page,
  remove the embed rather than merely leaving it unlinked. For the rest, derive
  the image-page URL from image_page
  (strip {SITE_DIR}/docs, drop .mdx; confirm against {PAGES_CSV}).
* Parse each image's on_pages into a deduplicated list of host .mdx file paths.
* Invert into a map: host page -> [ (cid, sha256, filename, image-page URL), ...]
  for every image that page hosts.

Then, for each host page in that map (partition across up to {MAX_AGENTS}
agents by host page; a host page is never split across agents):

* Read the page in.
* For each image the map assigns to this page, locate the one matching <img> /
  markdown image by the KNOWLEDGE match order (CID first, then the
  /img/evidence/{sha256}.{ext} static path, then filename/alt). If nothing
  matches, record it as "claimed host, not embedded" and skip.
* Wrap the matched embed in an anchor to that image's page URL, preserving all
  attributes and styles. Obey the idempotency rules: skip if already wrapped to
  the same URL; never clobber a pre-existing human-placed anchor to a different
  target (record those); never double-wrap; never touch a sibling image.
* Keep the page byte-identical everywhere else. The only edits are the wrapping
  anchors.
* Do not modify pages under {PHOTOS_DIR} here (those are Stage 3's; their own
  layout handles their single image), and do not modify {HIERARCHY_FILE}.

Host pages edited here live OUTSIDE {PHOTOS_DIR} — this is the one stage that
writes elsewhere in {DOCS_DIR}, and it may only ever add wrapping anchors around
already-present image embeds. It creates no pages, deletes nothing, and moves
nothing.

Output to stdout:
============================
STAGE 5 COMPLETE
Host pages scanned: N   host pages edited: N
Image embeds linked: N   already linked (skipped): N
Claimed hosts with no matching embed: N (list)
Pre-existing anchors left intact: N (list)
============================

============================
STAGE 6 — PLACE THE SHOULD_BE_ON_PAGES IMAGES ONTO THEIR TOPIC PAGES
============================

Stage 5 wired up the images that were already embedded. This stage places the
ones that are not. It is the stage that makes the YAML's plan real: every image
the hierarchy says belongs on a topic page gets put on that page, hosted, and
made clickable through to its own Photos page. See KNOWLEDGE — SHOULD_BE_ON_PAGES
for the src resolution order, the link derivation, the block markers, the dedupe
rule, the per-page cap, and the caption rules; follow it exactly.

By this stage every image page under {PHOTOS_DIR} exists (Stage 3 wrote them) and
{PAGES_CSV} is current (Stage 4), so both the link targets and their URLs are
real.

Build the plan first, working from the YAML index:

* Walk every image entry. Skip any that types as video or UNKNOWN per
  MEDIA-TYPE SCOPE, and report it — this block emits `<img>` only, so a video
  reaching it produces an <img> pointed at an .mp4. Skip any in the ban set
  ({BAN_IMAGES_CSV} or {EXCLUDE_FILE}) and count it. Skip any with an empty
  should_be_on_pages. Skip any with no image_page, and report it.
* Resolve the entry's src by the four-branch order in KNOWLEDGE (static copy /
  copy-then-static / pinned IPFS gateway / skip-and-report). Perform the copies
  into {STATIC_IMG_DIR} now, before any page is edited, so no page can end up
  referencing a file that was never written.
* Derive the image-page URL from image_page and confirm it against {PAGES_CSV}.
* Re-stat every should_be_on_pages path. Drop and report any that no longer
  resolves, and any that points under {PHOTOS_DIR}.
* Invert into a map: host page -> ordered list of
  (sha256, cid, src, image-page URL, alt text, caption), YAML order preserved.

Then, for each host page in that map (partition across up to {MAX_AGENTS}
agents by host page; a host page is never split across agents):

* Read the page in. Strip the existing CK_PLACED_IMAGES block from the text you
  test against, then drop from the page's list every image whose sha256 or cid
  already appears in that stripped text — those are already visible on the page
  and Stage 5 owns their linking.
* Apply the per-page cap of 12 counting what is already embedded, keeping YAML
  order. Report the overflow.
* Emit the block: a "## Images" heading and one figure per image — the
  <img> wrapped in an anchor to the image's Photos URL, carrying data-cid, an
  alt drawn from the description, loading="lazy" — plus the caption line and its
  "full write-up" link.
* Replace the block between the markers if they exist; append it at end of file
  if they do not; remove it entirely if the page's list came out empty. Keep the
  page byte-identical everywhere outside the markers.
* Do not modify pages under {PHOTOS_DIR}, and do not modify {HIERARCHY_FILE}.

The gallery needs one stylesheet block — a marked CK_PLACED_IMAGES region in
{SITE_DIR}/internals/src/css/custom.css, alongside the existing
CK_EVIDENCE_LAYOUT block. Write it once, regenerate it in place on later runs,
and never touch the rest of that file.

Output to stdout:
============================
STAGE 6 COMPLETE
Images with should_be_on_pages: N   placements planned: N over N pages
Src resolution: N static / N copied-then-static / N IPFS gateway / N unresolvable
Pages edited: N   blocks created: N   blocks replaced: N   blocks removed: N
Images placed: N   skipped as already embedded: N
Over the 12-per-page cap: N (list of page -> overflow count)
Missing image_page: N   should_be_on_pages paths that no longer exist: N (list)
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
  * Paths and URLs that must keep matching disk: this prompt sidesteps the
    problem by serving sha256-named static copies, so published pages never
    contain mirror filenames. If a mirror path must appear in a page for any
    reason, emit non-ASCII as visible escapes instead.

After every emit pass, re-scan all written files for the invisible set and
hard-fail if any code point remains. (The invisible set is enumerated in
{THIS_DIR}/p_create_image_hierarchy.md — same list applies here.)

============================
STAGE 7 — BUILD, VERIFY, REPORT
============================

* Run the Docusaurus build: cd {SITE_DIR} && npm run build. It must pass.
  Broken links and MDX compile errors (e.g. a stray <!-- --> comment) surface
  here — fix and rebuild until green. The host-page image links added in
  Stages 5 and 6 are internal links, so any bad target fails the build here.
* Spot-check 10 image pages across different partitions: frontmatter fields
  present, hide_table_of_contents true, image src resolves to an existing
  static file or IPFS URL, layout component/CSS applied, description has at
  least one hyperlink to another Level 2/Level 3, safe-writing check passes,
  the word "defamation" absent.
* Spot-check 5 cluster pages: TOC lists all peers, children, and image pages;
  every link resolves.
* Check the bypass rule on every node in the bypass set: the parent's TOC
  contains a link to the single image page and contains NO link to the
  bypassed cluster page; the bypassed cluster page nevertheless exists on
  disk, has its {PAGES_CSV} row, and builds; the image page's back link points
  at the nearest non-bypassed ancestor.
* Spot-check the Stage 5 host links: pick 10 image/host-page pairs across
  different sections, open the host page, confirm the matched <img> is wrapped
  in an anchor whose href is the image's derived Photos URL, confirm no sibling
  image was wrapped, and confirm that URL resolves to the image page on disk.
* Spot-check the Stage 6 placements: pick 10 pages that gained a block, confirm
  the block sits between its markers at the bottom, confirm every src resolves
  (the static file exists under {STATIC_IMG_DIR}, or the CID is one of the
  pinned ones), confirm every anchor href resolves to a real image page on
  disk, confirm no image appears twice on the page, and confirm the page above
  the markers is unchanged from before the run.
* MEDIA-TYPE AUDIT. Grep every file this run wrote under {PHOTOS_DIR} for
  `<video`, `<source`, `<audio`, and media-player `<iframe`. Expected count is
  ZERO; any hit fails the run. Then grep ALL of {PHOTOS_DIR}, including files
  this run did not touch, and report that count separately — it is the
  pre-existing contamination and it must not be rising. It was 9 on
  2026-07-23, all under Official_Narrative/Narrative_Shot_in_the_Heart/.
  Confirm each of those 9 is still listed in {FINDINGS_FILE} and was not
  purged as an orphan.
* BAN AUDIT — re-read {BAN_IMAGES_CSV} and {EXCLUDE_FILE} here, at the end,
  rather than reusing the Stage 1 set; a row may have been added mid-run by this
  very run. Then assert all four, and fail the run on any of them:
    - No page under {PHOTOS_DIR} carries a banned sha256 in ck_image_sha256.
    - No file under {STATIC_IMG_DIR} is named for a banned sha256 or cid.
    - No page anywhere under {DOCS_DIR} references a banned image — grep for the
      sha256, for the cid, and for the original basename, inside and outside
      CK_PLACED_IMAGES blocks.
    - No page anywhere links to a URL under /Photos that resolves to a banned
      image's page.
  Grep for the identity, not for the page path: a stale link with no page behind
  it is still a link into banned material and is a broken link besides.
* Confirm nothing was written under {VIDEOS_L2_DIR}, {VIDEOS_DIR}, or
  {VIDEO_PLANNING_DIR}, and that no {PAGES_CSV} row added this run has a
  url_path under /Videos.
* Confirm {PAGES_CSV} row count change matches pages created.
* Run the invisible-Unicode scan over everything written this run (host pages
  edited in Stages 5 and 6 included).
* Confirm nothing outside {PHOTOS_DIR}, {STATIC_IMG_DIR}, {PAGES_CSV}, the
  Stage 5 host pages (anchor wraps only), the Stage 6 host pages (marked block
  only), the marked CSS region, and (marker section only) {IMAGES_L2_PAGE} was
  modified. sidebars.ts untouched.

Output to stdout:
============================
STAGE 7 COMPLETE — FINAL REPORT
Build: PASS/FAIL
Pages now under /Photos: N cluster + N image = N total
Images published: N of N in YAML (N pending media)
BANNED: N images in the ban set — 0 have a page, 0 have a served copy,
  0 are placed on any page, 0 are linked to from anywhere (all four required)
  Un-published this run: N pages + N served copies + N placements removed
Video/UNKNOWN entries skipped, not published: N (handed off to findings)
Media players emitted into /Photos this run: 0 (required)
Pre-existing /Photos pages carrying a video player: N (was 9, must not rise)
Host pages linked: N   image embeds made clickable: N
Topic pages carrying placed images: N   images placed: N
Spot-checks: image pages N/10 pass, cluster pages N/5 pass, host links N/10 pass,
             placement blocks N/10 pass
pages.csv in sync: yes   sidebars.ts untouched: yes   invisible scan: clean
============================

============================
HARD RULES
============================

* {LAYOUT_GUIDELINES} is read at the very start of every run and its rules
  override this prompt where they conflict. It grows over time; never edit it
  from this prompt.
* {CK_FILE} is read into the context window at the very start — it is the
  knowledge base for understanding the entire assassination and every
  description is grounded in it.
* STILL IMAGES ONLY. Every entry is typed before its page is written; an entry
  typed as video or UNKNOWN is skipped, counted, and handed off — no page, no
  static copy, no {PAGES_CSV} row, no TOC link, no Stage 5 anchor, no Stage 6
  placement. No file under {PHOTOS_DIR} ever contains a `<video>`, `<source>`,
  `<audio>`, or media-player `<iframe>` element. Video publishes to
  {VIDEOS_L2_DIR} from {VIDEO_HIERARCHY_FILE}, and this prompt never writes
  there. Pages already published under {PHOTOS_DIR} with a video player are
  left in place, listed in {FINDINGS_FILE}, and never treated as orphans.
* This prompt writes ONLY: pages under {PHOTOS_DIR}, static copies under
  {STATIC_IMG_DIR}, the marked TOC section of {IMAGES_L2_PAGE}, a shared
  layout component/CSS under {SITE_DIR}/internals/src/ (marked regions only),
  {PAGES_CSV} rows, and — on the topic pages named in each image's on_pages /
  should_be_on_pages — wrapping anchors around already-present image embeds
  (Stage 5) and the marked CK_PLACED_IMAGES block (Stage 6). It never modifies
  {HIERARCHY_FILE}'s data (read-only input), never touches {SITE_DIR}/sidebars.ts,
  and never writes planning notes into the site or Docusaurus pages into
  {THIS_DIR}.
* Stage 5 makes each image's inline copies on its on_pages host pages clickable,
  linking to that image's Photos image page via a site-relative URL derived from
  image_page (strip {SITE_DIR}/docs, drop .mdx). It only adds a wrapping anchor
  around the one matched <img> per page — it changes no other content, creates
  and deletes nothing, never double-wraps, never clobbers a pre-existing anchor,
  and never links an image to any page but its own. Excluded images are skipped.
* Stage 6 places every image the YAML's should_be_on_pages says belongs on a
  topic page and is not already embedded there, in a regenerated block between
  the CK_PLACED_IMAGES markers at the BOTTOM of that page. Outside the markers
  the page stays byte-identical — the block is the only thing this prompt may
  add to a topic page's content. Each placed image is hosted from the served
  static copy (IPFS gateway only for pinned, file-less entries), carries its CID
  as data-cid, and is wrapped in an anchor to its own Photos image page. Never
  duplicate an image already on the page, never exceed 12 per page, never place
  anything in the ban set, and never place an image that has no image_page to
  land on. should_be_on_pages is the complete desired state and a superset of
  on_pages — not a list of extras.
* A cluster node whose subtree resolves to exactly ONE image page is bypassed
  in navigation: parents and peers link straight to that image page, never to
  the cluster page, and the image page's back link points at the nearest
  non-bypassed ancestor. The bypassed cluster page is still generated, still
  rows in {PAGES_CSV}, and is never treated as an orphan. Nodes with two or
  more images are linked normally.
* Reruns refresh structure and PRESERVE authored prose (see BOOKKEEPING
  FIELDS ON PAGES). An enrichment pass's writing, and any safe-writing scrub
  applied to a page, must survive every later regeneration. Orphan removals
  are counted and reported.
* Every image page: one image, no right bar, aspect ratio true, right edge
  5px from the browser's right edge, max 70% of main-area width, bounding box
  bottom 10px above the browser bottom.
* Every description: maximum information within the safe-writing rules; the
  word "defamation" never appears; no claims of prior knowledge or of
  immoral/illegal conduct; attribution language; links to related Level 2s
  and Level 3s as /X/overview-style routes verified against {PAGES_CSV}.
* Nothing in the ban set — the union of {BAN_IMAGES_CSV} and {EXCLUDE_FILE},
  minus any CSV row marked banned=false — is ever published, placed, linked to,
  or pinned. A banned image gets no Level 5 page, no served copy under
  {STATIC_IMG_DIR}, and no link into it from anywhere; whatever already exists
  for it is DELETED, including its {PAGES_CSV} row. The set is re-read from
  those two files every run, never inherited from the YAML's `banned:` field,
  which is a copy written by {HIERARCHY_PROMPT}. Anything found during a run
  that should not be public gets a row in {BAN_IMAGES_CSV} with a reason before
  the run ends. Prose care does not substitute for withholding the image.
* The YAML is an input, not an authority on what is true or publishable. Its
  inline ai_description text is model output and has been wrong about people,
  places and events; its clustering sometimes files an image as supporting a
  thesis that the image's own contents contradict. Write what the evidence
  actually shows, say so on the page when it differs from the filing, and
  record the discrepancy in {FINDINGS_FILE}.
* Up to {MAX_AGENTS} parallel agents, partitioned by YAML subtree; shared
  files ({PAGES_CSV}, {IMAGES_L2_PAGE}) are written only by the orchestrator.
* No invisible Unicode in any emitted file — scan after every emit.
* The build must pass before the run is declared complete.

============================
BACKGROUND — ORIGINAL DIRECTIVE, KNOWLEDGE PRESERVED
============================

This section preserves the full intent of the directive this prompt was built
from, so no knowledge is lost even where a stage above already encodes it.

* Create this prompt file but do not run it yet. Learn from the entire
  image_planning directory. By the time this prompt runs, the YAML file will
  already be built and it has all the data we need.
* In our charlie-kirk Docusaurus we have a Level 2 directory called images
  (today: Photos). The goal is to create the .mdx pages under that images
  Level 2 directory. The content comes from the YAML file.
* The goal is to host the image. These pages should not have a right bar. The
  image must be the right aspect ratio. The right side of the image aligns
  with the webpage's right side, 5px left of the right edge of the browser —
  that is where the image's right side is.
* There is an area where the image can go; it fills however much is
  appropriate, defined by: no more than 70% of the width of the main area
  (the main area is the full browser width minus the left bar); it won't be
  taller than the box; the bottom of the bounding rectangle is 10px up from
  the bottom of the browser page. That is the bounding box. The image often
  will not need the full width or the full height, depending on its aspect
  ratio.
* Each page carries a description of the content: what the image is and what
  it is related to. The description has hyperlinks off to other Level 2s and
  Level 3s. The image often came from some other Level 2 or Level 3 document
  outside the images Level 2; if that other page hosted this image, we want
  to understand that topic and explain this image and how it relates to the
  page it was hosted on. It might be hosted on multiple pages. The bigger
  Charlie Kirk investigation is used, to the best of our ability, to
  understand the image and where it is hosted — that also gives context. We
  describe that area of the investigation.
* We make no defamatory claims. The word "defamation" should not appear in
  the article. The writing must not say anybody knew anything before the
  crime or did anything immoral or illegal — check the writing for exactly
  that — while including as much information as possible without causing
  those problems.
* When the YAML has pointers to the OCR file, the AI description file, or the
  inline AI description, we sometimes read those files in order to build the
  best writing for the page's write-up.
* layout_guidelines.txt lives in this directory (created with three empty
  lines). Over time it will explain more standards for our images pages. When
  this prompt runs, that file is read into the context window right away, and
  whatever rules it has are followed.
* When this prompt runs it can run up to 12 different agents in parallel, and
  it probably could and should: take different sections of the YAML file,
  partition them among the 12 agents, and each agent works its section —
  updating the pages under the Level 2 images, making sure the image is
  hosted on the page, the image size is correct, and the content written on
  the page is updated.
* This prompt will often run multiple times, so it has to rewrite pages. The
  pages are often pre-existing, written earlier before additional data was
  there, and the run needs to read them in.
* {CK_FILE} (~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt) is very
  important and must be read into the context window at the very start of the
  run. It is the knowledge needed to understand the entire Charlie Kirk
  assassination.
