THIS IS THE VIDEOS CHARTER. It is NOT a copy of image_planning/CLAUDE.md and it
must never be overwritten by one. If the line below this block says
"THIS_DIR dir is {ROOT_DIR}/image_planning", this file has been clobbered by a
copy from the images pipeline and the videos charter has been lost — restore it
before doing any work. The sibling images charter lives at
{IMAGE_PLANNING_DIR}/CLAUDE.md and is read-only from here.

ROOT_DIR dir is ~/BGit/Bryan_git/charlie-kirk

THIS_DIR dir is {ROOT_DIR}/videos_planning

VIDEOS_DIR dir is {ROOT_DIR}/videos

HIERARCHY_FILE is file {VIDEOS_DIR}/videos.yaml

  The full path is ~/BGit/Bryan_git/charlie-kirk/videos/videos.yaml and the file
  already exists there. It sits beside the video files, exactly the way
  {IMAGE_PLANNING_DIR}'s YAML sits at {ROOT_DIR}/images/images.yaml beside the
  image files. There is no copy of it in {THIS_DIR} and there never should be.

  Created 2026-07-23 as a copy of {ROOT_DIR}/images/images.yaml with the SCHEMA
  converted to videos. Only the keys were converted. The DATA it carries is still
  the inherited image corpus and is known-stale — every file_path, sha256, cid,
  ai_description, on_pages value and every count still describes an image.
  Replacing that data with the real video corpus is the job of
  {THIS_DIR}/p_update_video_hierarchy.md. Treat anything in the file today as a
  placeholder, not as fact.

  It is tracked in git. The root .gitignore excludes the {VIDEOS_DIR} directory
  so the media never lands in the repo; the metadata files (videos.yaml,
  manifest.yaml, videos.md, .gitignore) are re-included by explicit negation
  rules. If a new metadata file in {VIDEOS_DIR} needs to be committed, add a
  matching negation rather than force-adding it by hand.

VIDEO_MANIFEST is file {VIDEOS_DIR}/manifest.yaml
VIDEO_INDEX_MD is file {VIDEOS_DIR}/videos.md

CK_FILE is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt
  (Real file. Moved 2026-09-19. ~/BGit/Bryan_git/charlie-kirk/Charlie_Kirk.txt is now a symlink to it —
   use that only to verify the location; always read and write the real path.)

SITE_DIR dir is {ROOT_DIR}/site

VIDEO_LIST_CSV is file {SITE_DIR}/docs/video_list.csv

VIDEOS_L2_DIR dir is {SITE_DIR}/docs/Videos

VIDEOS_L2_PAGE is file {VIDEOS_L2_DIR}/overview.mdx

PAGES_CSV is file {ROOT_DIR}/pages.csv

IPFS_DIR dir is {ROOT_DIR}/IPFS

MIRROR_DIR dir is ~/_Mirror/Politics/Charlie_Kirk_Mi

MIRROR_SIDECAR_DIR dir is ~/BGit/Bryan_git/personal_large_files_bridge/_Mirror/Politics/Charlie_Kirk_Mi

REPO_SIDECAR_DIR dir is {ROOT_DIR}/.lfbridge

IMAGE_PLANNING_DIR dir is {ROOT_DIR}/image_planning


== What This Directory Is ==

videos_planning is the private planning workspace for the VIDEOS hierarchy of the
public Docusaurus site. It is NOT a Docusaurus directory. Nothing here is
published. It holds the plan — {HIERARCHY_FILE} — that the public video pages
under {VIDEOS_L2_DIR} are generated from and kept in sync with.

Two layers, same rule as the rest of the repo:

  * Planning layer (here): the prompts, the charter, the layout standards, the
    exclusion list, the findings file, and generator/. Private.
  * Published layer ({VIDEOS_L2_DIR}): the actual Level 2/3/4/5 video pages
    visitors see. Public. Defamation rules apply.

The plan itself — {HIERARCHY_FILE} — lives in {VIDEOS_DIR}, not here. This
directory holds the things that read and write it.

This directory is the SIBLING of {IMAGE_PLANNING_DIR}, which does the same job
for still images against {ROOT_DIR}/images/images.yaml and publishes to
{SITE_DIR}/docs/Photos. The two pipelines share a shape and share nothing else:

  images                                videos
  ------                                ------
  {IMAGE_PLANNING_DIR}                  {THIS_DIR}
  images/images.yaml                    videos/videos.yaml
  site/docs/Photos                      site/docs/Videos
  Img_*.mdx leaf pages                  Vid_*.mdx leaf pages
  ck_image_sha256 frontmatter           ck_video_cid + ck_video_sha256
  PHOTOS_TOC_START/END markers          VIDEOS_TOC_START/END markers
  CK_EVIDENCE_LAYOUT css block          CK_VIDEO_LAYOUT css block
  ck-evidence-* classes                 ck-video-* classes
  gen_photos_pages.py                   gen_videos_pages.py
  exclude_images.txt                    exclude_videos.txt
  served from static/img/evidence       played from a public IPFS gateway

Never let one pipeline write the other's files. Both generators write into the
same {SITE_DIR}/internals/src/css/custom.css, so each owns its OWN marked block
and touches nothing outside it — if the video generator wrote the
CK_EVIDENCE_LAYOUT block it would silently destroy the image layout, and the
next image run would destroy the video layout back.

The same hazard applies to this directory's own files. Every file in {THIS_DIR}
began as a copy of its {IMAGE_PLANNING_DIR} counterpart and was converted on
2026-07-23. Re-copying any of them from the images side silently reverts that
conversion — it has already happened once to this charter. Copy nothing in;
edit in place.

{IMAGE_PLANNING_DIR} is still useful as PRIOR ART. Its generator, its exclusion
list, and its findings file solved these same problems once already; read them
before reinventing. Just never edit them from here, and never copy them here.


== Always Read First ==

Before doing anything in this directory, read into the context window:

  * {CK_FILE} — the master investigation file (400K+). It is the source of
    truth for what the investigation's concepts, clusters, and open questions
    actually are. The video hierarchy must mirror the investigation's real
    concept structure, not an arbitrary video-library structure.
  * {ROOT_DIR}/prompts/Assess_Manual.md — writing and layout guide for every
    published page.
  * {ROOT_DIR}/claude.md — the repo charter (pages.csv schema, defamation
    rules, site structure).
  * {THIS_DIR}/layout_guidelines.txt — how a video sits on its Level 5 page.
    Every point in it was written after a real, visible defect shipped.


== The Audience (Think About This First) ==

Every structural decision starts with who is looking and why. There are two
arrival paths into the videos hierarchy, and both must work:

  1. Left-bar arrival. The visitor clicks "Videos" in the left sidebar and
     lands on the Level 2 videos page cold. They have no topic in mind yet.
     They are browsing. The Level 2 page must present the concept clusters so
     they can pick the thread they care about.

  2. Topic arrival. The visitor is deep in some other Level 2 section of the
     site — Ballistics, Drones, Israel, Tyler Robinson, the Mic — and they want
     to WATCH the footage for that topic. They click through to videos. They
     land in the deep video hierarchy at the cluster for that topic, not at the
     top. The hierarchy exists so this landing is possible.

Path 2 is why the hierarchy is clustered by investigation concept rather than
by date, source account, or upload batch. A visitor reading about the exploding-
mic thesis wants the mic videos, one click, already grouped.

There is a third thing a video does that an image cannot, and it drives the
whole write-up: a video makes a CLAIM OUT LOUD, over time. The page has to say
who is speaking, what they assert, at roughly what timestamp, and what is
actually shown versus merely narrated. The .transcription sidecar is what makes
that possible, which is why transcription is the load-bearing sidecar here.


== Page Hierarchy Model ==

The site's videos section behaves like every other section of the site:

  Level 2  — the videos landing page. One page. Reached from the left bar.
             {VIDEOS_L2_PAGE} (sidebar label "Videos", url /Videos,
             _category_.json position 20). It is the root of everything below.
  Level 3  — top-level concept clusters under videos. These are the array
             items in {HIERARCHY_FILE}.
  Level 4  — sub-clusters under a Level 3.
  Level 5  — the individual VIDEO PAGES: one video, one write-up. Where the YAML
             nests a level_5 cluster node instead, that node is a cluster page
             and its videos are its leaves.

Rules that hold at every level:

  * Six videos per page is the target. Twelve is the ceiling. If a page needs
    more than twelve, it is not one concept — split it into child pages one
    level down. (A page carrying many IPFS video embeds is heavy; prefer the
    low end of that range and split earlier than the image hierarchy would.)
  * Every page carries a table of contents with hyperlinks to its peers (the
    other pages at its level, under the same parent) and to its children (the
    sub-areas beneath it). A visitor should never hit a dead end or have to use
    the browser back button to move sideways.
  * Clusters are concept clusters. The question is always "what does this
    footage show or claim," never "when was it downloaded" or "who posted it."
  * Titles may use spaces and full words. Keys use underscores and aim for four
    words or less.


== videos.yaml ==

{HIERARCHY_FILE} — ~/BGit/Bryan_git/charlie-kirk/videos/videos.yaml — is the
single planning artifact. It sits in {VIDEOS_DIR} with the videos themselves.
It does two jobs:

  1. It defines the hierarchical clusters — the Level 3, Level 4, and Level 5
     pages — including the table of contents each level needs (peer links and
     sub-area links are derivable from the tree structure itself).
  2. It binds every video to the cluster it belongs in, carrying enough identity
     (CID, sha256, path) that the video can be located and played from any
     machine.

=== Structure ===

The file is hierarchical and starts at level_3. There is no level_1 and no
level_2 in this file — level_1 is the site home and level_2 is the videos
landing page itself, so the top-level video cluster tree begins at level_3.

  * `level_3` is a tree and an array. Each array item is also called `level_3`.
  * A level_3 item may contain a `level_4` array; a level_4 item may contain a
    `level_5` array. Same shape at every depth, down to level_7 today.

Fields on each cluster node (level_3 / level_4 / level_5 / deeper):

  title                         Human-readable page title. Spaces allowed. May
                                run longer than the key.
  _key                          Same idea as the title but with underscores for
                                spaces. Four words or less. Unique across the
                                whole file. This is the page_key used in
                                {PAGES_CSV}.
  site_level_2                  List of site docs dirs this cluster covers.
                                Empty list when the node is corpus-only.
  site_page                     The written page this cluster mirrors.
  number_of_videos              Videos owned directly by this node.
  number_of_videos_recursive    Videos in this node's whole subtree.
  needs_split                   true when the node is over the twelve ceiling.
  videos                        Array. Each item is a `video`.

Fields on each `video` — every one is always present; a value that does not
exist is emitted as "" rather than dropped, so a later pass can tell "not looked
up yet" from "looked up, does not exist". The two typed exceptions are
on_pages (a list, emits []) and ipfs_pinned (a boolean, emits false):

  cid                  The IPFS CID, CIDv0 "Qm..." form. (Spoken as "SID" — it
                       means the CID.) For videos this is the PRIMARY identity,
                       because the site plays video off public IPFS gateways and
                       never from a copy in the repo. Many entries have a cid
                       and an empty sha256, because the media file is gitignored
                       and absent on a fresh clone.
  ipfs_pinned          Whether the local IPFS node pins those blocks. A CID
                       exists whether or not it is pinned.
  sha256               Content identity of the local file, when there is one.
  file_path            Path to the video file — usually {VIDEOS_DIR} for videos
                       pulled from X, or {MIRROR_DIR} for older captures.
  ai_description       Short inline prose: what is SEEN in the footage.
  ai_description_file  Path to the .ai_description sidecar, or "".
  ocr_file             Path to the .ocr sidecar, or "". Rare for video.
  transcription_file   Path to the .transcription sidecar, or "". This is the
                       important one for video — what was SAID.
  video_page           Full path from ~ to the published Level 5 page that hosts
                       this one video under {VIDEOS_L2_DIR}. "" when no page
                       exists yet. It must never point under
                       {SITE_DIR}/docs/Photos — that is the images pipeline's
                       output.
  on_pages             List of `- page:` mappings: every OTHER page in the repo
                       that embeds this video. [] when none.
  ipfs_url             Optional. Present on entries harvested from a site embed
                       that have no local file.
  also_filed_in        Optional. Other concept dirs the same content legitimately
                       lives in. Cross-filing is deliberate and kept.

=== Skeleton ===

  level_3:
    - level_3:
        title: "The Exploding Microphone Thesis"
        _key: Mic_Thesis
        site_level_2: ["Mic"]
        site_page: "site/docs/Mic/overview.mdx"
        number_of_videos: 6
        number_of_videos_recursive: 14
        videos:
          - video:
              cid: "QmThpacy26yaTjsRcPSVegJQTNzRRSyXt23tKWjPZcyn3s"
              ipfs_pinned: true
              sha256: ""
              file_path: "~/BGit/Bryan_git/charlie-kirk/videos/2067372027623715212.mp4"
              ai_description: "..."
              ai_description_file: "~/BGit/Bryan_git/charlie-kirk/.lfbridge/videos/2067372027623715212.mp4.ai_description"
              ocr_file: ""
              transcription_file: "~/BGit/Bryan_git/charlie-kirk/.lfbridge/videos/2067372027623715212.mp4.transcription"
              video_page: ""
              on_pages: []
        level_4:
          - level_4:
              title: "Shaped Charge Counterarguments"
              _key: Mic_Shaped_Charge
              number_of_videos: 8
              number_of_videos_recursive: 8
              videos:
                - video:
                    cid: "QmbDwwYuPmjPjL84jM2XCum7EFrtc33pjWBhMdKMFCdPXt"
                    ...


== Where The Inputs Come From ==

=== {VIDEOS_DIR} — the repo's own video corpus ===

The primary source. About 46 .mp4 files with matching .mp3 audio extractions,
pulled from X/Twitter posts by the /ck_add_text skill and pinned to IPFS. The
media itself is GITIGNORED — {VIDEOS_DIR}/.gitignore excludes *.mp4, *.mp3,
*.mkv, *.avi, *.mov, *.wav, *.webm, and the root .gitignore excludes the
directory with explicit negations for the metadata files. Only the metadata is
committed, and anyone who wants the bytes pulls them from IPFS. Three committed
files describe the corpus and all three are inputs:

  {VIDEO_MANIFEST}    per-file: filename, ipfs_cid, ipfs_gateway_url,
                      source_url, source_author, description, added_date,
                      pinned. This is the richest machine-readable source and
                      the best seed for cid / file_path / provenance.
  {VIDEO_INDEX_MD}    the same corpus as a human-readable markdown table.
  {IPFS_DIR}/ipfs.txt the pull-and-pin commands, three per file
                      (ipfs get / ipfs add / ipfs pin add). {IPFS_DIR}/videos
                      holds larger forensic originals such as the Blake Bednarz
                      UVU footage.

=== {MIRROR_DIR} — the older concept-filed capture area ===

Years of manual filing by concept across ~300 directories. It is mostly stills,
but it does hold video, and its directory names are the strongest available
signal for what the clusters should be. Read them as proposed clusters. Treat
__TO_FILE, backup, Old, Organized, TO_TRANSCRIBE, and Other as work queues, not
concepts — their contents get clustered by transcription and description, not by
folder name.

=== {VIDEO_LIST_CSV} and the site's existing embeds ===

{VIDEO_LIST_CSV} is a small hand-kept index (about 12 rows) of YouTube links and
IPFS CIDs with title, description, date, and location columns. It is a starting
index only; the page scan is authoritative. Videos are today embedded ad hoc
inside topic pages across the site (GoogleSearches, Security_Team,
distraction_people, and others) — those embeds stay where they are. This
hierarchy is the browsable index over the video corpus, not a relocation of
every inline embed.

=== AI Descriptions and Transcriptions ===

Descriptions and transcriptions are sidecar text files written by Large File
Bridge (~/BGit/Bryan_git/LargeFileBridge/, understood by reading its pm/ specs).
Same base filename, second-level extension appended:

  something.mp4.transcription     what is SAID in it — the primary one for video
  something.mp4.ai_description    what is SEEN in the footage
  something.mp4.ocr               literal on-screen text; rare on video

Two pairing rules, depending on whether the original lives inside a git repo:

  * Inside this git repo — sidecars live under {REPO_SIDECAR_DIR}, mirroring the
    repo-relative path. This is the NORMAL case here, because the video corpus
    lives in the repo:
      {VIDEOS_DIR}/X.mp4  →  {REPO_SIDECAR_DIR}/videos/X.mp4.transcription
    {REPO_SIDECAR_DIR} currently holds videos/, IPFS/videos/, images/,
    cover_image/, and site/ sidecars. Under videos/ today there are roughly 74
    .transcription files, 44 .ai_description files, and 2 .ocr files — so
    transcription coverage over the 46-video corpus is good, and it is the
    richest input this pipeline has. Note that .lfbridge/ is explicitly
    re-included in the root .gitignore, so the sidecars travel with the repo
    even though the media does not.

  * Outside any git repo (the mirror) — there is no .lfbridge/ segment. The
    dedicated bridge repo IS the tracking area and the mirror hangs directly off
    it:
      {MIRROR_DIR}/Teachers_Lounge/X.mp4
        →  {MIRROR_SIDECAR_DIR}/Teachers_Lounge/X.mp4.transcription

Older files may still sit under a .lfbridge/_Mirror/ path until Large File
Bridge migrates them. Check both locations before concluding a sidecar is
missing. Re-count coverage at run time; these grow constantly.


== How Clustering Is Done ==

  1. Read {CK_FILE} for the investigation's real concepts and open questions.
  2. Read the transcriptions for the videos (generate missing ones first). What
     the speaker CLAIMS is usually what decides the cluster.
  3. Read the AI descriptions for what is actually shown, and reconcile: a video
     is frequently filed under the thesis it argues while its own footage shows
     something narrower. Say so on the page when that happens.
  4. Read the {MIRROR_DIR} directory or the {VIDEO_MANIFEST} description a given
     video came with — it carries filing intent and usually names the cluster.
  5. Cluster by concept. The folder proposes, the transcription decides,
     {CK_FILE} arbitrates.
  6. Enforce six-to-twelve. Over twelve means split one level deeper.
  7. Write the tree to {HIERARCHY_FILE} with accurate number_of_videos and
     number_of_videos_recursive.
  8. Generate or update the pages under {VIDEOS_L2_DIR} from the tree, each with
     its peer + child table of contents.
  9. Update {PAGES_CSV} for every page created, moved, retitled, or deleted —
     page_key matches the node's _key, parent_key matches the parent node's
     _key, level matches the node's level.


== Playing The Video On A Page ==

This is the one place where the video pipeline diverges hard from the image
pipeline, and getting it wrong is expensive.

Video bytes are NEVER copied into {SITE_DIR}/static. The images pipeline copies
each still to static/img/evidence/{sha256}.{ext}; videos in this corpus run from
single megabytes to 173MB, they are gitignored on purpose, and GitHub Pages is
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

Consequences that must be respected:

  * cid is required to publish a playable video page. An entry with cid "" gets
    its page written with the write-up and a "media pending" note, and no player.
  * ipfs_pinned false means no public gateway can reliably serve it. Publishing
    it produces a dead player. Report those; do not pin as a side effect of a
    page run — pinning is irreversible in practice and is a separate,
    explicitly-approved job.
  * Test the built site in a clean browser profile with no IPFS Companion
    extension. Companion silently rewrites gateway URLs to your local node, so a
    video that is not actually available to the public will look fine to you and
    be dead for every visitor.
  * A poster frame MAY be served locally — {SITE_DIR}/static/img/video_posters/
    {sha256}.jpg — because a poster is small. Nothing else about the video is.


== Current State (2026-07-23) ==

  * {HIERARCHY_FILE} exists at ~/BGit/Bryan_git/charlie-kirk/videos/videos.yaml
    and is tracked in git. It is a schema shell: its keys are the video schema
    described above; its 1,740 entries and 1,365 nodes are still the inherited
    image data. Every video_page is "". Nothing in it has been verified against
    the real video corpus yet.
  * {VIDEOS_L2_PAGE} exists (131 lines, url /Videos, sidebar position 20). It is
    prose about the role of video evidence — footage types, uses for timeline and
    shooter-location analysis, claims about unreleased or deleted footage. It has
    no cluster cards. {VIDEOS_L2_DIR} contains only overview.mdx,
    _category_.json, and one topic page (buckley-carlson-kash-patel-valhalla.mdx,
    page_key Videos_Buckley_Kash). Both .mdx pages are PROTECTED: they are never
    treated as orphans and their prose is never overwritten by the generator.
  * {VIDEO_LIST_CSV} has 12 rows. {SITE_DIR}/docs/image_list.csv is empty.
  * A second, unrelated Videos page exists at /Topics3/Videos (page_key
    Topics3_Videos). It is template scaffolding under the Topics3 tree, not part
    of this hierarchy. Do not confuse the two.
  * {THIS_DIR} holds the charter (this file), layout_guidelines.txt, and the
    three prompts: p_update_video_hierarchy.md (builds the YAML),
    p_yaml_to_site.md (writes the page words), p_level2_update.md (writes the
    navigation and owns Level 5 layout). It does NOT yet hold generator/,
    exclude_videos.txt, or findings_for_hierarchy.md — the prompts reference all
    three and each creates or seeds the ones it needs on first run. Until
    generator/ exists, read {IMAGE_PLANNING_DIR}/generator as prior art.


== Hard Rules ==

  * Never modify {SITE_DIR}/sidebars.ts unless explicitly asked. The videos
    section already has its left-bar entry; Level 3+ pages are reached by
    navigating into the Level 2 page, matching how every other section works.
  * Keep {PAGES_CSV} in sync on every page create, move, retitle, or delete.
  * Everything published under {VIDEOS_L2_DIR} follows the repo's defamation
    rules: no stating as fact that a living person committed a crime,
    attribution language throughout, presence only for named living people.
    Video adds a failure mode images do not have — a speaker in the footage
    makes an accusation out loud. Reporting that a video contains a claim is
    fine; repeating the claim in the site's own voice is not. Quote and
    attribute. Raw claims stay private, here or in {CK_FILE}.
  * {HIERARCHY_FILE} is the plan, not the published output. Do not put
    Docusaurus pages in {THIS_DIR}, and do not put planning notes in
    {VIDEOS_L2_DIR}. Do not put a copy of the YAML in {THIS_DIR} — it lives in
    {VIDEOS_DIR}.
  * Never write anything under {IMAGE_PLANNING_DIR}, {ROOT_DIR}/images,
    {SITE_DIR}/docs/Photos, or {SITE_DIR}/static/img/evidence from this
    pipeline. Read them freely as prior art. Never copy a file FROM there to
    here — every file in {THIS_DIR} is a converted descendant of one, and a
    re-copy silently reverts the conversion.
  * Never copy video bytes into {SITE_DIR}/static. IPFS gateways serve the video.
  * Nothing in this pipeline ever pins to IPFS as a side effect. Pin status is
    recorded; changing what is public is a separate, approved job.
  * MDX comments must be {/* ... */}. An HTML <!-- --> comment fails the MDX
    compile and breaks the deploy.
