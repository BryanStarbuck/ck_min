ROOT_DIR dir is ~/BGit/Bryan_git/charlie-kirk

THIS_DIR dir is {ROOT_DIR}/image_planning

IMAGES_DIR dir is {ROOT_DIR}/images

HIERARCHY_FILE is file {IMAGES_DIR}/images.yaml

  Moved 2026-07-22. It used to be {THIS_DIR}/hierarchy_images.yaml. Both the old
  name and the old location are gone — the file is now named images.yaml and it
  lives in {IMAGES_DIR}, alongside the image files themselves, not in {THIS_DIR}.
  Anything that still says "hierarchy_images.yaml" or points at image_planning/
  for the YAML is stale.

CK_FILE is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt
  (Real file. Moved 2026-09-19. ~/BGit/Bryan_git/charlie-kirk/Charlie_Kirk.txt is now a symlink to it —
   use that only to verify the location; always read and write the real path.)

SITE_DIR dir is {ROOT_DIR}/site

IMAGES_L2_PAGE is file {SITE_DIR}/docs/Photos/overview.mdx

PAGES_CSV is file {ROOT_DIR}/pages.csv

MIRROR_DIR dir is ~/_Mirror/Politics/Charlie_Kirk_Mi

MIRROR_SIDECAR_DIR dir is ~/BGit/Bryan_git/personal_large_files_bridge/_Mirror/Politics/Charlie_Kirk_Mi

REPO_SIDECAR_DIR dir is {ROOT_DIR}/.lfbridge


== What This Directory Is ==

image_planning is the private planning workspace for the images hierarchy of the
public Docusaurus site. It is NOT a Docusaurus directory. Nothing here is
published. It holds the plan — {HIERARCHY_FILE} — that the public image pages
under {SITE_DIR}/docs/Photos/ are generated from and kept in sync with.

Two layers, same rule as the rest of the repo:

  * Planning layer (here): the YAML tree, notes, and prompts. Private.
  * Published layer ({SITE_DIR}/docs/Photos/): the actual Level 2/3/4/5 image
    pages visitors see. Public. Defamation rules apply.


== Always Read First ==

Before doing anything in this directory, read into the context window:

  * {CK_FILE} — the master investigation file (400K+). It is the source of
    truth for what the investigation's concepts, clusters, and open questions
    actually are. The image hierarchy must mirror the investigation's real
    concept structure, not an arbitrary photo-album structure.
  * {ROOT_DIR}/prompts/Assess_Manual.md — writing and layout guide for every
    published page.
  * {ROOT_DIR}/claude.md — the repo charter (pages.csv schema, defamation
    rules, site structure).


== The Audience (Think About This First) ==

Every structural decision starts with who is looking and why. There are two
arrival paths into the images hierarchy, and both must work:

  1. Left-bar arrival. The visitor clicks "Photos" in the left sidebar and
     lands on the Level 2 images page cold. They have no topic in mind yet.
     They are browsing. The Level 2 page must present the concept clusters so
     they can pick the thread they care about.

  2. Topic arrival. The visitor is deep in some other Level 2 section of the
     site — Ballistics, Drones, Israel, Tyler Robinson, the Mic — and they want
     to SEE the evidence for that topic. They click through to images. They
     land in the deep image hierarchy at the cluster for that topic, not at the
     top. The hierarchy exists so this landing is possible.

Path 2 is why the hierarchy is clustered by investigation concept rather than
by date, camera, or source. A visitor reading about the spy plane wants the
spy plane images, one click, already grouped.


== Page Hierarchy Model ==

The site's images section behaves like every other section of the site:

  Level 2  — the images landing page. One page. Reached from the left bar.
             Currently {IMAGES_L2_PAGE} (sidebar label "Photos", url /Photos).
             It is the root of everything below it.
  Level 3  — top-level concept clusters under images. These are the array
             items in {HIERARCHY_FILE}.
  Level 4  — sub-clusters under a Level 3.
  Level 5  — sub-clusters under a Level 4. Rare. Only when the concept genuinely
             splits three deep.

Rules that hold at every level:

  * Six images per page is the target. Twelve is the ceiling. If a page needs
    more than twelve, it is not one concept — split it into child pages one
    level down.
  * Every page carries a table of contents with hyperlinks to its peers (the
    other pages at its level, under the same parent) and to its children (the
    sub-areas beneath it). A visitor should never hit a dead end or have to use
    the browser back button to move sideways.
  * Clusters are concept clusters. The question is always "what is this
    evidence about," never "when was it downloaded" or "who posted it."
  * Titles may use spaces and full words. Keys use underscores and aim for four
    words or less.


== images.yaml (was hierarchy_images.yaml) ==

{HIERARCHY_FILE} — {IMAGES_DIR}/images.yaml — is the single planning artifact.
It formerly lived here as {THIS_DIR}/hierarchy_images.yaml; it now sits in
{IMAGES_DIR} with the images. It does two jobs:

  1. It defines the hierarchical clusters — the Level 3, Level 4, and Level 5
     pages — including the table of contents each level needs (peer links and
     sub-area links are derivable from the tree structure itself).
  2. It binds every image to the cluster it belongs in, carrying enough identity
     (CID, fingerprint, path) that the image can be located and published from
     any machine.

=== Structure ===

The file is hierarchical and starts at level_3. There is no level_1 and no
level_2 in this file — level_1 is the site home and level_2 is the images
landing page itself, so the top-level images cluster tree begins at level_3.

  * `level_3` is a tree and an array. Each array item is also called `level_3`.
  * A level_3 item may contain a `level_4` array; a level_4 item may contain a
    `level_5` array. Same shape at every depth.

Fields on each cluster node (level_3 / level_4 / level_5):

  title             Human-readable page title. Spaces allowed. May run longer
                    than the key.
  _key              Same idea as the title but with underscores for spaces. Four
                    words or less. Unique across the whole file. This is the
                    page_key used in {PAGES_CSV}.
  number_of_images  Count of images at that level. Tracked, kept accurate.
  images            Array. Each item is an `image`.

Fields on each `image`:

  cid               The IPFS CID. (Spoken as "SID" — it means the CID.)
  fingerprint       The Large File Bridge content fingerprint. Identifies the
                    file by content, independent of name and path, so an image
                    survives moves and renames and duplicates collapse.
  file_path         Path to the image file.
  ai_description    The AI-generated description of what is visually in the
                    image. This is what the clustering is reasoned from.

=== Skeleton ===

  level_3:
    - level_3:
        title: "The Spy Plane Over UVU"
        _key: Spy_Plane
        number_of_images: 6
        images:
          - image:
              cid: Qm...
              fingerprint: ...
              file_path: ~/_Mirror/Politics/Charlie_Kirk_Mi/Spy_Plane/example.jpg
              ai_description: "..."
        level_4:
          - level_4:
              title: "N1098L NCSS CIA Registration"
              _key: N1098L_NCSS
              number_of_images: 8
              images:
                - image:
                    cid: Qm...
                    fingerprint: ...
                    file_path: ...
                    ai_description: "..."


== Where The Inputs Come From ==

=== The Mirror (concept structure + the images themselves) ===

{MIRROR_DIR} holds roughly 1,666 images across ~300 directories. Its directory
names are not incidental — they are years of manual filing by concept, and they
are the strongest available signal for what the clusters should be. Read them as
proposed clusters and let them shape the hierarchy.

Directories there that already read as clusters, with rough image counts:

  __TO_FILE (301)          unfiled backlog — NOT a cluster, it is a queue
  Google_Search (73)       with Searches_By_Date and N1098L_NCSS_CIA beneath it
  CIA (many)               incl. Slides/VIDEO Drones_CIA_Israel (39), N1098L_NCSS_CIA (15)
  Truck_and_Back_of_Tent (35)
  Tyler_Robinson (33)      with Lance (21), Walking (16), Clothing (13) beneath it
  Ballistics (28)          and Acoustics_Ballistics, Bullet (17), Enter_Exit_bullet
  Mic (27)                 the exploding-mic thread
  Map (26)
  Planes (24)              and Plane_Egypt_SU_BTT (22), Plane_N888KG, Plane_Piper_N59906
  Israel (22)              and Israel_150m
  South_Side_Shot (20)
  Spy_Plane (13)           with N1098L_NCSS_CIA (19), Drop_Off, Cover Up, MEMEs beneath it
  Court (19)               with Mirandize (14)
  UVU_University (16 in more/)
  Sniper/Real_Shooter (16)
  Gun (15 in Drop Off Locations)
  Table_Hand_off/Blake_Harruff_Plaid_Light_Blue (14)
  Drone (14), Tent_Grass (13), Photos (13), Security_Team (11)
  Patsy_* family          Curly_Wave_Hands, Fake_Doctor, George_Zinn,
                          Gun_Medical_Clothing, Russell_Kennington, Sorenson_Building
  plus: Autopsy, Medical, FBI, TPUSA, Roof, Witnesses, Suspects, Teachers_Lounge,
        Security_Cameras, Huachuca_Fort, MKUltra, Censorship, Cover_Up, Iran,
        Utah, Influencers, Threats, To_Hospital, X_Shooter, Zach_Qureshi, and more.

Treat __TO_FILE, backup, Old, Organized, TO_TRANSCRIBE, and Other as work
queues, not concepts. Their contents get clustered by AI description, not by
folder name.

=== AI Descriptions and Transcriptions ===

Descriptions and transcriptions are sidecar text files written by Large File
Bridge. Same base filename, second-level extension appended:

  something.jpg.ai_description    what is visually in the image
  something.mp4.ai_description    what is visually in the video
  something.mp4.transcription     what is said in it

Two pairing rules, depending on whether the original lives inside a git repo:

  * Inside this git repo — sidecars live under {REPO_SIDECAR_DIR}, mirroring the
    repo-relative path:
      {ROOT_DIR}/videos/X.mp4  →  {REPO_SIDECAR_DIR}/videos/X.mp4.transcription
    {REPO_SIDECAR_DIR} currently holds videos/ and IPFS/videos/ sidecars.

  * Outside any git repo (the mirror) — there is no .lfbridge/ segment. The
    dedicated bridge repo IS the tracking area and the mirror hangs directly off
    it:
      {MIRROR_DIR}/Autopsy/X.jpg  →  {MIRROR_SIDECAR_DIR}/Autopsy/X.jpg.ai_description
    ~91 .ai_description files exist there today. Coverage is thin against 1,666
    images — generating the missing ones is prerequisite work for clustering,
    since the descriptions are what the clustering reasons over.

Older files may still sit under a .lfbridge/_Mirror/ path until Large File
Bridge migrates them. Check both locations before concluding a sidecar is
missing.


== How Clustering Is Done ==

  1. Read {CK_FILE} for the investigation's real concepts and open questions.
  2. Read the AI descriptions for the images (generate missing ones first).
  3. Read the {MIRROR_DIR} directory a given image sits in — the folder name
     carries filing intent and usually names the cluster.
  4. Cluster by concept. Reconcile the description against the folder: the
     folder proposes, the description decides, {CK_FILE} arbitrates.
  5. Enforce six-to-twelve. Over twelve means split one level deeper.
  6. Write the tree to {HIERARCHY_FILE} with accurate number_of_images.
  7. Generate or update the pages under {SITE_DIR}/docs/Photos/ from the tree,
     each with its peer + child table of contents.
  8. Update {PAGES_CSV} for every page created, moved, retitled, or deleted —
     page_key matches the node's _key, parent_key matches the parent node's
     _key, level matches the node's level.


== Current State ==

  * {HIERARCHY_FILE} exists and is built. It lives at {IMAGES_DIR}/images.yaml.
    It was moved there from {THIS_DIR}/hierarchy_images.yaml on 2026-07-22 —
    new name, new location. {THIS_DIR} now holds only the prompts, the charter,
    the exclusion list, the findings file, and generator/.
  * {IMAGES_L2_PAGE} exists (99 lines, url /Photos, sidebar position 25). It is
    prose about the role of photographic evidence — types, uses, limitations,
    access constraints. It has no cluster cards and no children.
    {SITE_DIR}/docs/Photos/ contains only overview.mdx and _category_.json.
  * {SITE_DIR}/docs/image_list.csv exists but is empty. {SITE_DIR}/docs/video_list.csv
    has 12 rows.
  * A second, unrelated Photos page exists at /Topics3/Photos (page_key
    Topics3_Photos). It is template scaffolding under the Topics3 tree, not part
    of this hierarchy. Do not confuse the two.
  * Images are today embedded ad hoc inside topic pages across the site (People,
    FBI, Suspects, Mic, Planes, and others). Those embeds stay where they are.
    This hierarchy is the browsable index over the image corpus, not a
    relocation of every inline image.


== Hard Rules ==

  * Never modify {SITE_DIR}/sidebars.ts unless explicitly asked. The images
    section already has its left-bar entry; Level 3+ pages are reached by
    navigating into the Level 2 page, matching how every other section works.
  * Keep {PAGES_CSV} in sync on every page create, move, retitle, or delete.
  * Everything published under {SITE_DIR}/docs/Photos/ follows the repo's
    defamation rules: no stating as fact that a living person committed a crime,
    attribution language throughout, presence only for named living people, and
    accusations cropped out of images. Raw claims stay private, here or in
    {CK_FILE}.
  * {HIERARCHY_FILE} is the plan, not the published output. Do not put
    Docusaurus pages in {THIS_DIR}, and do not put planning notes in
    {SITE_DIR}/docs/Photos/.
