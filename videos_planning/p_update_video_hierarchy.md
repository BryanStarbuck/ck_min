ROOT_DIR dir is ~/BGit/Bryan_git/charlie-kirk

THIS_DIR dir is {ROOT_DIR}/videos_planning
VIDEOS_DIR dir is {ROOT_DIR}/videos
HIERARCHY_FILE is file {VIDEOS_DIR}/videos.yaml
VIDEO_MANIFEST is file {VIDEOS_DIR}/manifest.yaml
VIDEO_INDEX_MD is file {VIDEOS_DIR}/videos.md
IPFS_DIR dir is {ROOT_DIR}/IPFS
IPFS_VIDEOS_DIR dir is {IPFS_DIR}/videos
GENERATOR_DIR dir is {THIS_DIR}/generator
INVENTORY_TSV is file {GENERATOR_DIR}/inventory.tsv
SIDECAR_INDEX is file {GENERATOR_DIR}/sidecars.json
FINDINGS_FILE is file {THIS_DIR}/findings_for_hierarchy.md

SITE_DIR dir is {ROOT_DIR}/site
DOCS_DIR dir is {SITE_DIR}/docs
HOME_PAGE is file {DOCS_DIR}/index.mdx
VIDEOS_L2_DIR dir is {DOCS_DIR}/Videos
VIDEOS_L2_PAGE is file {VIDEOS_L2_DIR}/overview.mdx
VIDEO_LIST_CSV is file {DOCS_DIR}/video_list.csv
PAGES_CSV is file {ROOT_DIR}/pages.csv
CK_FILE is file ~/BGit/all/politics/charlie_kirk/Charlie_Kirk.txt
  (Real file; {ROOT_DIR}/Charlie_Kirk.txt is a symlink to it. Read the real path. READ-ONLY.)
CHARTER_FILE is file {THIS_DIR}/CLAUDE.md
ASSESS_MANUAL is file {ROOT_DIR}/prompts/Assess_Manual.md
EXCLUDE_FILE is file {THIS_DIR}/exclude_videos.txt
BAN_VIDEOS_CSV is file {VIDEOS_DIR}/ban_videos.csv

REPO_SIDECAR_DIR dir is {ROOT_DIR}/.lfbridge
REPO_VIDEO_SIDECAR_DIR dir is {REPO_SIDECAR_DIR}/videos
REPO_IPFS_SIDECAR_DIR dir is {REPO_SIDECAR_DIR}/IPFS/videos
MIRROR_DIR dir is ~/_Mirror/Politics/Charlie_Kirk_Mi
MIRROR_SIDECAR_DIR dir is ~/BGit/Bryan_git/personal_large_files_bridge/_Mirror/Politics/Charlie_Kirk_Mi

LFB_DIR dir is ~/BGit/Bryan_git/LargeFileBridge
LFB_PM_DIR dir is {LFB_DIR}/pm
COMPANY_BRIDGE_DIR dir is ~/BGit/act3/act3_large_files_bridge
PERSONAL_BRIDGE_DIR dir is ~/BGit/Bryan_git/personal_large_files_bridge

IMAGE_PLANNING_DIR dir is {ROOT_DIR}/image_planning
IMAGE_GENERATOR_DIR dir is {IMAGE_PLANNING_DIR}/generator

============================
GOAL
============================

Build {HIERARCHY_FILE}, the MASTER DATA for every video we hold: what it is, where its bytes are, its
IPFS CID, what was SAID, what is SEEN, burned-in text, its concept cluster, and which pages show it.
Every later prompt reads it; none re-derives the corpus.

THE POINT OF THIS RUN IS FILLING IN THE SIDECAR DATA. Large File Bridge already transcribed, described
and OCR'd the corpus; none of it is in the YAML yet. transcription_file, ai_description_file, ocr_file
and their parsed values are the deliverable; everything else is structure.

THE FIRST RUN IS A REBUILD. The file today holds ~1,740 entries and ~1,365 nodes inherited from
{ROOT_DIR}/images/images.yaml with only the KEYS converted (2026-07-23); every value describes an image
(.jpg/.png paths, image sha256/cid, "This image shows..." prose, image on_pages, image counts). Stage 6
REPLACES it wholesale from Stages 2-5. Only its TREE SHAPE (titles, _keys) is worth reading, as a
proposal the transcriptions may overrule. From the second run on, the file only grows (update in place,
no duplicates, no deletes). Stage 6 detects the mode.

Convergence priority (if context runs short, complete in this order):
   1. Stage 2 (corpus index)  2. Stage 3 (sidecar harvest)  3. Stage 4 (CID + pin)  4. Stage 5 (cluster)
   5. Stage 6 (write)  6. Stage 6B (banned sync)  7. Stage 14 (counts, publishable, integrity)
   8. Stage 7  9. Stage 9  10. Stage 10  11. Stage 11  12. Stage 8  13. Stage 12  14. Stage 13  15. Stage 15
Stages 2-6B plus 14 alone produce a correct, useful master file. 6B is cheap and gates Stage 12 (no
page for banned), Stage 13 (no placement for banned) and p_yaml_to_site.md (deletes existing banned
pages/posters); skipping it plans banned footage. Never run Stage 13 on an unverified Stage 11 (it unions
on_pages into should_be_on_pages).

============================
KNOWLEDGE — THE CORPUS CENSUS (VERIFIED ON DISK 2026-07-23)
============================

Re-count at run time; treat these as expected magnitudes and report deltas.

  {VIDEOS_DIR}: 46 .mp4 (primary corpus), 30 .mp3 (audio extractions), 2 stray .txt, 3 metadata
  (manifest.yaml, videos.md, videos.yaml). .gitignore excludes *.mp4 *.mp3 *.mkv *.avi *.mov *.wav *.webm.

  {VIDEO_MANIFEST}: 63 records, NOT the same set as disk:
    * 18 records name an .mp4 not on disk; several have the .mp3 on disk instead (2046414464447287296,
      2046416264562921472, 2046416264567140352, 2068463186668605858, 2069185145555255370,
      2072814926133866634). Real videos with real CIDs; they belong in the YAML.
    * 1 disk file not in the manifest: _QwGo0LyZ3I.mp4 (130MB, YouTube-id filename). Needs a CID and entry.

  {REPO_VIDEO_SIDECAR_DIR}: 74 .transcription (44 *.mp4.transcription + 30 *.mp3.transcription),
    44 .ai_description (all *.mp4), 2 .ocr (2079054276320440416.mp4.ocr, 2079275082648809861.mp4.ocr).
    * 44 of 46 mp4s have both transcription and ai_description. The 2 with neither and no .mp3 fallback:
      2079560806690324910.mp4, 2079684519762993659.mp4 (the transcription work list; never guess content).
    * 7 .mp3.transcription files have NO .mp4 on disk: 2046414464447287296, 2046416264562921472,
      2046416264567140352, 2068463186668605858, 2069185145555255370, 2071736376215920842_extracted,
      2072814926133866634. Their .mp3.transcription is the only record of what was said.

  {REPO_IPFS_SIDECAR_DIR}: 2 videos, each with transcription and ai_description:
    "Blake Bednarz UVU original.MP4" (uppercase ext, SPACES, ~3GB forensic original, CID in {IPFS_DIR}/ipfs.txt)
    "chain_of_evil.mp4"

  {REPO_SIDECAR_DIR} also holds images/, cover_image/, site/ (images pipeline): read nothing from them.
  Local IPFS: kubo 0.42.0 at /opt/homebrew/bin/ipfs; pin checks work.

  Realistic corpus: ~46 mp4 + ~7 audio-only + 2 IPFS originals + third-party video on site pages =
  roughly 55-65 entries. Hundreds means something is wrong.

============================
KNOWLEDGE — SIDECAR FILES: WHAT THEY ARE, WHERE THEY ARE, WHAT IS INSIDE THEM
============================

Large File Bridge ({LFB_DIR}) writes three sidecars per media file:
  .transcription   what was SAID: verbatim local ASR. THE PRIMARY SIDECAR FOR VIDEO (a video's claim is
                   spoken); clustering reasons over it.
  .ai_description  what is SEEN: hosted vision model's structured prose, INCLUDING A TIMESTAMPED SHOT LIST.
  .ocr             on-screen text (chyrons, slates, captions). Rare (2 files), usually screen-recorded posts.
ALL THREE get a YAML property on EVERY entry, always ("" when absent; never missing, never null).

NAMING: full filename kept, second extension appended:
  2067372027623715212.mp4 → 2067372027623715212.mp4.transcription / .ai_description / .ocr
Case is PRESERVED ("Blake Bednarz UVU original.MP4.transcription"); never lowercase the extension.
Filenames contain SPACES: quote every path in every shell command.

PLACEMENT, keyed on the storage kind of the original's root (authoritative: {LFB_PM_DIR}/
artifact_placement_policy.mdx section 0; detail in Transcribe.mdx, ai_description.mdx, ocr.mdx,
repo_tracking_scheme.mdx):
  * INSIDE a git repo (the NORMAL case here): reproduce the repo-relative path under {REPO_SIDECAR_DIR}
    (no analysis/ or .transcribe/ subdir; committed, so sidecars travel with the repo):
      {VIDEOS_DIR}/X.mp4 → {REPO_SIDECAR_DIR}/videos/X.mp4.transcription
      {IPFS_VIDEOS_DIR}/X.MP4 → {REPO_SIDECAR_DIR}/IPFS/videos/X.MP4.transcription
  * OUTSIDE any repo (the mirror): NO .lfbridge/ segment; the SDL bridge repo is the tracking area:
      {MIRROR_DIR}/Teachers_Lounge/X.mp4 → {MIRROR_SIDECAR_DIR}/Teachers_Lounge/X.mp4.transcription
      Personal SDL: {PERSONAL_BRIDGE_DIR}   Company SDL: {COMPANY_BRIDGE_DIR}
  * Legacy fallback: .lfbridge/_Mirror/ path. Check it before concluding a sidecar is missing.
Verify the mapping on disk in Stage 1; do not infer it.

THE AUDIO SIBLING RULE. LFB often transcribed the .mp3 extraction (30 of 74). transcription_file order:
  1. <base>.mp4.transcription (preferred)
  2. <base>.mp3.transcription (same speech; legitimate; must be used) -> transcription_source: "audio_sibling"
  3. "" (report it)
  e.g. transcription_file: "~/BGit/.../.lfbridge/videos/2069185145555255370.mp3.transcription"
       transcription_source: "audio_sibling"
For the 7 basenames whose .mp4 is gone: file_path = the .mp3 path, media_present "audio_only", keep the
manifest CID (still playable from IPFS). Never drop one. Record audio_file (.mp3 sibling or "") on every entry.

.transcription FORMAT: five header lines, a 60-equals divider, a blank line, then the body as ONE long
unwrapped line with no timestamps:
    Transcription of: 2067372027623715212.mp4
    Generated on: 2026-07-14 13:18:36
    Engine: apple-speechanalyzer (device: on-device, language: en)
    Source duration: 00:04:19   ·   Transcript covers: 00:04:19  ✓ full
    ============================================================

    And when you run this theory that Charlie's microphone was rigged, ...
Parse:
  line 1 "Transcription of: " -> confirm it matches the paired media file (mismatch = bug, report).
  line 2 "Generated on: " -> transcription_generated
  line 3 "Engine: " -> transcription_engine
  line 4 fields split by U+00B7 MIDDLE DOT with spaces: "Source duration: HH:MM:SS" -> duration;
         "Transcript covers: HH:MM:SS" -> transcript_covers. Anything other than a trailing "✓ full" =
         ASR stopped early -> transcript_complete: false, report it (a partial treated as complete yields a
         page confidently describing half a video).
  line 5 divider; everything after, trimmed, is the body.
DURATION EXISTS ONLY HERE (not in manifest or videos.md); it drives page load and gateway decisions.
Never fabricate timestamps; timing comes from the shot list.

.ai_description FORMAT: a YAML document with seven top-level keys (all 44 have all seven):
    source: videos/2067372027623715212.mp4
    status: done
    engine: gemini-flash-latest
    provider: gemini
    generated: 2026-07-14T16:50:03.564Z
    kind: video
    description: >-
      ## Overview
      ...
  source -> cross-check (REPO-RELATIVE). status: only "done" has content (else record the path, treat
  content as missing). engine -> ai_description_engine. provider -> ai_description_provider.
  generated -> ai_description_generated. kind must be "video" (an "image" under videos/ is misfiled; report).
  `description` is markdown with twelve sections, in order: ## Overview (2-5 sentences, what the video IS),
  ## Hyper-Detail, ## Shot-by-shot / Timeline (timestamped bullets like
  "* **00:39 - 00:55** | Split-screen. Candace on left; screenshot of a National Library of Medicine page
  on right. Static." — THE MOST VALUABLE SECTION, the only structured timing data), ## People,
  ## Setting & Place, ## Location, ## Composition, ## Cinematography, ## Lighting, ## Colors & Mood,
  ## Objects, Text & Brands (complements .ocr, not a substitute), ## Audio & Speech (summary, NOT a transcript).
  Extract at minimum:
    ai_description   ## Overview collapsed to one paragraph (join lines with spaces, collapse whitespace, strip
                     the header), same as readDesc() in {IMAGE_GENERATOR_DIR}/gen_hierarchy.js; reuse it.
    shot_timeline    ## Shot-by-shot / Timeline verbatim as a block scalar, timestamps kept.
    people_seen      ## People collapsed (feeds the defamation review).
    onscreen_text    ## Objects, Text & Brands collapsed.
  The sidecar stays the source; the YAML holds the useful subset.

.ocr: only the two above. Read both in Stage 1, record the actual format (header like the transcription's
or bare text), set ocr_file on those two and "" elsewhere, and write the format to {FINDINGS_FILE}.

PAIRING RULE: the transcription has WORDS without timing; the ai_description has TIMING with only a speech
summary. Keep both, distinguishable. A recurring finding: a video filed under the thesis it ARGUES shows
something narrower (a host at a desk over slides). Transcription = claim; shot list = evidence; the gap is
often the story.

============================
KNOWLEDGE — THE VIDEO ENTRY SCHEMA (EXPANDED FOR VIDEO)
============================

Emit this schema. Every key on every entry: "" for empty scalars (never null/omitted), [] for empty lists,
true/false for booleans.

    videos:
      - video:
          title: "Candace Owens — the rigged-microphone recap"
          cid: "QmThpacy26yaTjsRcPSVegJQTNzRRSyXt23tKWjPZcyn3s"
          ipfs_pinned: true
          sha256: ""
          file_path: "~/BGit/Bryan_git/charlie-kirk/videos/2067372027623715212.mp4"
          media_present: "video"
          file_size_bytes: 46196181
          duration: "00:04:19"
          audio_file: "~/BGit/Bryan_git/charlie-kirk/videos/2067372027623715212.mp3"

          transcription_file: "~/BGit/Bryan_git/charlie-kirk/.lfbridge/videos/2067372027623715212.mp4.transcription"
          transcription_source: "video"
          transcription_engine: "apple-speechanalyzer (device: on-device, language: en)"
          transcription_generated: "2026-07-14 13:18:36"
          transcript_covers: "00:04:19"
          transcript_complete: true

          ai_description_file: "~/BGit/Bryan_git/charlie-kirk/.lfbridge/videos/2067372027623715212.mp4.ai_description"
          ai_description_provider: "gemini"
          ai_description_engine: "gemini-flash-latest"
          ai_description_generated: "2026-07-14T16:50:03.564Z"
          ai_description: "A podcast segment from \"Candace\" featuring host Candace Owens. She outlines a theory involving a rigged microphone to explain inconsistencies in a high-profile incident. Political commentary using slides, interview inserts, and photographic evidence."
          shot_timeline: |
            * **00:00 - 00:10** | Medium close-up of Candace Owens speaking. Static camera.
            * **00:10 - 00:27** | Split-screen. Candace Owens on the left (~30% width); a text slide under "Rigged Mic Might Reasonably Explain:" on the right. Static.
          people_seen: "Candace Owens, seated in a studio ... inserts of two men identified on screen as Dan Merrill and Jimmy Rex."
          onscreen_text: "Slide title \"Rigged Mic Might Reasonably Explain\"; a National Library of Medicine page on PETN."

          ocr_file: ""

          banned: false

          source_url: "https://x.com/RealCandaceO/status/2067372027623715212"
          source_author: "@RealCandaceO"
          source_platform: "x"
          added_date: "2026-06-17"
          manifest_description: "Candace Owens rigged-mic recap"

          video_page: ""
          on_pages: []
          should_be_on_pages:
            - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/Mic/overview.mdx"
            - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/Suspicious/Five_Minutes/shirt-pull-at-the-shot.mdx"

FIELD NOTES:
  title                  Short human title (becomes Level 5 title and TOC link text): from manifest description
                         + ## Overview, under ~nine words, name the speaker. Never an accusation.
  media_present          "video" (.mp4 here) | "audio_only" (only .mp3) | "none" (manifest or site embed only).
                         Lets a fresh clone (no media, gitignored) behave correctly.
  file_size_bytes        From stat when present (0.5MB to 173MB; the page generator warns on big gateway loads).
  duration               From the transcription header.
  audio_file             .mp3 sibling or "".
  transcription_source   "video" | "audio_sibling" | "".
  transcript_complete    false whenever "✓ full" is absent.
  shot_timeline          Block scalar, timestamps preserved.
  banned                 Boolean, default false, COPIED DOWN from {BAN_VIDEOS_CSV} by Stage 6B only.
  people_seen            Defamation review input.  onscreen_text: complements .ocr.
  source_url / source_author / added_date / manifest_description
                         From {VIDEO_MANIFEST}; provenance is evidence ("who posted this and when").
  source_platform        "x" | "youtube" | "rumble" | "ipfs" | "local" | ""
  cid                    CIDv0 "Qm...", spoken "SID". PRIMARY IDENTITY for video (the site plays from public
                         gateways). cid with empty sha256 is normal when bytes are not on this machine.
  sha256                 Local file identity when present.
  video_page             Tilde path to the Level 5 page under {VIDEOS_L2_DIR}; "" until Stage 12. Never under
                         {DOCS_DIR}/Photos.
  on_pages               Every OTHER page embedding it TODAY, OBSERVED (Stage 11).
  should_be_on_pages     Where it OUGHT to appear, REASONED (Stage 13); same shape; SUPERSET of on_pages (the
                         complete desired state); minus on_pages = the worklist p_yaml_to_site.md Stage 6 consumes.
  Retained: ipfs_url (optional, embed-only entries), also_filed_in (optional, deliberate cross-filing).

CLUSTER NODE FIELDS: title, _key, site_level_2, site_page, number_of_videos, number_of_videos_recursive,
needs_split, videos, child level_N array, plus NEW publishable: true when the subtree holds at least one
NOT-banned video (see THE EMPTY NODE PROBLEM). Generators publish only publishable nodes.

============================
KNOWLEDGE — THE BANNED PROPERTY (COPIED DOWN FROM {BAN_VIDEOS_CSV})
============================

Every entry carries `banned:` as a real boolean (default false; true only because a ban row matches).

Banned is a PUBLISH-TIME GATE, not a delete. A banned video gets: no Level 5 page under {VIDEOS_L2_DIR}
(an existing one is deleted by {THIS_DIR}/p_yaml_to_site.md, never here); no poster under
{SITE_DIR}/static/img/video_posters; no placement or link anywhere; never pinned (irreversible, so the gate
holds BEFORE any pin). Its entry stays forever: banning changes what is published, not what is known.

{BAN_VIDEOS_CSV} is the MASTER; the repo charter ({ROOT_DIR}/claude.md, "Banned Media") owns the contract:
    ban_videos.csv  ──▶  videos.yaml (banned:)  ──▶  site/docs/Videos/ pages
Edit only the CSV; never hand-edit `banned:`.

CSV FORMAT (header row, then one row per item):
  sha256        hex digest of the media file; primary identity for a local file
  cid           IPFS CID ("Qm..." CIDv0) if assigned; often the ONLY identity for video (bytes gitignored)
  file_path     full path from ~; last-resort match key, not authoritative
  banned        true or false. A false row is an explicit UN-BAN.
  reason        short plain-text reason. Required.
  date_added    YYYY-MM-DD
MATCH ORDER: sha256, then cid, then file_path; no match = false.
{EXCLUDE_FILE} (one identifier per line) still counts: BAN SET = UNION minus CSV rows marked false. New bans
go in the CSV; never delete lines from {EXCLUDE_FILE}.

Why video needs this more: prose omitting names is not protection when the footage streams from a public
URL (the media is the payload), and a clip catches every face and voice for its whole duration. When a run
finds non-public material (private documents, unrelated third-party records, bystanders with no connection,
an unproven accusation about a named living person burned into frames), add a CSV row with reason and date
BEFORE the run ends and note it in {FINDINGS_FILE}.

============================
CONCERN — THE EMPTY NODE PROBLEM (READ BEFORE STAGES 7-9)
============================

Mirroring the site (~70 Level 2 dirs, 364 pages) over ~55-65 videos yields hundreds of nodes, most with
zero videos. Publishing one page per node would create hundreds of empty pages and dead ends for topic
arrivals. The fix is a gate, not a smaller tree:
  * Build the full mirrored tree (its zero-coverage list is a research output; write it to {FINDINGS_FILE}).
  * publishable: false on every node with number_of_videos_recursive 0.
  * State in the YAML header comment that publishable: false nodes must not generate a page, and note in
    {FINDINGS_FILE} that p_yaml_to_site.md and p_level2_update.md must honour it.
  * Report total nodes and publishable nodes.

============================
KNOWLEDGE — THE TWO LEVEL SYSTEMS
============================

SITE: Level 1 = {HOME_PAGE}; Level 2 = dirs directly under {DOCS_DIR} (TPUSA, FBI, UVU, Israel, Mic, Planes,
Timeline; Videos and Photos too); Level 3 = pages in a Level 2 (overview, analysis pages, first-level subdir
overviews); Level 4 = one dir deeper.
YAML: no level_1/level_2; the tree hangs under the videos Level 2 and begins at level_3. `level_3:` is an array
of items keyed `level_3:`, each may hold `level_4:`, which may hold `level_5:`; same shape at every depth.
CORE MAPPING, increment by one: site Level 2 -> level_3; Level 3 -> level_4; Level 4 -> level_5. level_3 is a
SUPERSET of site Level 2s (minus Stage 7 exclusions); corpus-derived clusters also live at level_3/level_4
and site nodes MERGE into them.
Site Level 2s: enumerate live (ls {DOCS_DIR}); ~70 dirs.
Sizing ({CHARTER_FILE}): six videos per page target, twelve ceiling (over = needs_split, split deeper later);
video pages are heavy, so prefer the low end. Concept clusters ("what does this footage show or claim").
_keys: underscores, four words or less, unique file-wide (future page_keys; treat as primary keys).

============================
STAGE 1 — READ, VERIFY THE MAPPING, PREPARE
============================

* Read {CHARTER_FILE} (authority on audience, levels, schema, hard rules) and {ASSESS_MANUAL} (what the
  harvested fields will be used for).
* Read the LFB specs in {LFB_PM_DIR} (frontmatter description plus placement sections):
  artifact_placement_policy.mdx (section 0, owner of the rule), Transcribe.mdx, ai_description.mdx (and its
  section 0 symmetry contract), ocr.mdx, repo_tracking_scheme.mdx. If a spec and this prompt disagree, the
  spec wins and this prompt gets corrected.
* VERIFY THE MAPPING ON DISK: 5 .mp4 under {VIDEOS_DIR} vs {REPO_VIDEO_SIDECAR_DIR}; "Blake Bednarz UVU
  original.MP4" under {IPFS_VIDEOS_DIR} vs {REPO_IPFS_SIDECAR_DIR} (case and spaces test); one video under
  {MIRROR_DIR} vs {MIRROR_SIDECAR_DIR} (confirm no .lfbridge segment). Check the legacy location on a miss.
* Read both .ocr files end to end; record their format.
* Read {VIDEO_MANIFEST}, {VIDEO_INDEX_MD}, {IPFS_DIR}/ipfs.txt, {VIDEO_LIST_CSV}, {PAGES_CSV}.
* Read {HIERARCHY_FILE}'s TREE SHAPE ONLY: `grep -n '_key:\|title:' {HIERARCHY_FILE}` (its entries are
  image data; reading them wastes context).
* Read prior art in {IMAGE_GENERATOR_DIR}, READ ONLY: gen_hierarchy.js (readDesc(), _key minting),
  bind_image_pages.py (emit_node/recount byte-for-byte round-trip), sanitize_common.py (invisible-Unicode
  scrub). Never edit {IMAGE_PLANNING_DIR}; never copy its files here (every file here is a converted
  descendant and a re-copy silently reverts the conversion).
* Create {GENERATOR_DIR} if missing. Create {EXCLUDE_FILE} if missing, with a header comment saying it lists,
  one per line by cid or sha256, video that must never be published or pinned; seed it empty.
* Create {BAN_VIDEOS_CSV} if missing with header sha256,cid,file_path,banned,reason,date_added; report its rows.
* Consult {CK_FILE} by section when clustering needs arbitration (not all 400K+ lines up front).

Output to stdout:
============================
STAGE 1 COMPLETE
LFB specs read: N of 5
Mapping verified: N/5 repo samples, IPFS sample yes/no, mirror sample yes/no
OCR format recorded: yes/no  (format: ...)
Old YAML tree shape read: N level_3 titles, N total _keys
Prior-art scripts read: N
generator/ ready: yes    exclude_videos.txt ready: yes
ban_videos.csv ready: yes    rows: N (N banned=true, N un-bans)
============================

============================
STAGE 2 — BUILD THE CORPUS INDEX (GROUND TRUTH: WHAT VIDEOS EXIST)
============================

Build one flat index of every video from every source before touching the YAML; write it to
{INVENTORY_TSV} (inspectable, resumable).

SOURCES, in order of authority:
  1. {VIDEOS_DIR}: walk for .mp4 .mov .m4v .mkv .avi .webm (filename, path, size, mtime); record every .mp3
     as a potential audio sibling by basename.
  2. {VIDEO_MANIFEST}: 63 records (filename, ipfs_cid, ipfs_gateway_url, source_url, source_author,
     description, added_date, pinned). AUTHORITATIVE for CIDs of X-sourced video.
  3. {IPFS_DIR}/ipfs.txt plus {IPFS_VIDEOS_DIR}: forensic originals and CIDs.
  4. {REPO_VIDEO_SIDECAR_DIR} and {REPO_IPFS_SIDECAR_DIR}: every sidecar whose base ends in a video OR audio
     extension. A SIDECAR PROVES A VIDEO EXISTED (how the 7 audio-only survivors are found).
  5. {MIRROR_DIR}: walk for video extensions; pair against {MIRROR_SIDECAR_DIR}.
  6. {VIDEO_LIST_CSV}: YouTube-only rows get cid "", source_platform "youtube", watch URL in source_url.
     Never invent a CID.

ONE ROW PER VIDEO, keyed by basename (X status id or filename stem), recording:
  basename, media_path, media_present, size, audio_path, transcription_path, transcription_source,
  ai_description_path, ocr_path, manifest_cid, manifest_pinned, source_url, source_author, added_date,
  manifest_description, origin (videos_dir | ipfs_dir | mirror | manifest_only | video_list_csv | site_embed)

KNOWN DISCREPANCIES (not errors):
  * The 18 manifest-only .mp4s: .mp3 sibling or sidecars present -> "audio_only", else "none". Keep the row.
  * _QwGo0LyZ3I.mp4: row with origin "videos_dir", empty manifest fields, source_platform "youtube", source
    URL unknown (never guess); Stage 4 computes its CID.
  * 2079560806690324910.mp4 and 2079684519762993659.mp4: keep, empty sidecar fields, head the work list.
  * An .mp3 with an .mp4 sibling is ONE video; only an .mp3 with no video sibling anywhere is its own row.

Output to stdout:
============================
STAGE 2 COMPLETE
Rows in corpus index: N
  from {VIDEOS_DIR} on disk: N          from {IPFS_VIDEOS_DIR}: N
  from manifest only (no local file): N from mirror: N
  from sidecar-only evidence: N         from video_list.csv: N
media_present: video N / audio_only N / none N
Manifest records with no disk file: N (expected ~18)
Disk files with no manifest record: N (expected ~1: _QwGo0LyZ3I.mp4)
Inventory written: {INVENTORY_TSV}
============================

============================
STAGE 3 — SIDECAR HARVEST (THE CORE OF THIS RUN)
============================

For every row, resolve and PARSE all three sidecars; write results to {SIDECAR_INDEX} (JSON keyed by
basename) so Stage 6 emits from data.

PATHS: transcription_file = <base>.<videoext>.transcription, else <base>.mp3.transcription (source
"audio_sibling"), else ""; ai_description_file = <base>.<videoext>.ai_description or ""; ocr_file =
<base>.<videoext>.ocr or "". Preserve case, quote paths, legacy fallback for mirror originals.
PARSE each transcription (engine, generated, duration, covers, complete, body; confirm line 1 matches the
media, report mismatches). PARSE each ai_description (seven scalars; split `description` on `## ` headers;
extract ai_description, shot_timeline, people_seen, onscreen_text; only status "done" yields content).
PARSE each OCR per the Stage 1 format.

COVERAGE GAPS are a deliverable; write them to {FINDINGS_FILE} and stdout: no transcription (expected 2);
transcription from audio sibling (~7 sole-source, more duplicates); transcript_complete false (the dangerous
ones); no ai_description (expected 2 of 46); "Transcription of:" / "source:" mismatches.

Output to stdout:
============================
STAGE 3 COMPLETE
Rows processed: N
transcription_file set: N (own video N / audio sibling N)   missing: N (listed)
  transcript_complete false: N (listed — PARTIAL TRANSCRIPTS)
ai_description_file set: N   missing: N (listed)
  ## Overview extracted: N   ## Shot-by-shot extracted: N
  ## People extracted: N     ## Objects/Text extracted: N
ocr_file set: N (expected 2)
Duration harvested for: N of N rows
Sidecar/media pairing mismatches: N (listed — BUGS)
Sidecar index written: {SIDECAR_INDEX}
Gap lists appended to: {FINDINGS_FILE}
============================

============================
STAGE 4 — CID AND PIN STATUS ON EVERY VIDEO
============================

Before any page work: pages embed video almost only by IPFS gateway URL (Stage 11 matches by CID) and the
CID is the DELIVERY MECHANISM (bytes gitignored; GitHub Pages is no video host). No CID = no playable page.

A CID is computed from bytes, no network needed:
    ipfs add -n -Q "<file>"       # -n/--only-hash: compute, do not store
                                  # -Q/--quiet: print just the CID
USE THE DEFAULT CIDv0 ("Qm..."): what the manifest records, ipfs.txt pins and the site embeds.
--cid-version=1 yields a different string (codec too) that matches no site URL. Convert at use time with
`ipfs cid base32 <cid>` if needed; never store it. Identical flags every run (chunking changes the CID).

Pinning is separate from having a CID:
    ipfs pin ls --type=all <cid>   # prints the cid and "recursive" when pinned
    ipfs block stat <cid>          # blocks present locally

* Seed from {VIDEO_MANIFEST} (ipfs_cid, pinned are authoritative for X-sourced), then {IPFS_DIR}/ipfs.txt.
* Every row with a readable local file and no CID: compute it (never end this stage with cid "" for such a row).
* Record ipfs_pinned for every CID from the local node.
* No local file: CID from manifest or gateway URL; pinned per node, else false.
* Neither file nor manifest CID: cid "", report. NEVER invent one.
* Recorded vs recomputed mismatch = bytes changed: report, keep recomputed, note old. Never overwrite a
  non-empty cid with "".
* Build a CID -> row index with both v0 and base32 v1 forms for Stage 11.

DO NOT PIN (irreversible). Pinning the publishable set is a separate approved job that first filters out the
ban set. Report the unpinned set prominently: each publishes as a dead player for visitors while looking fine
here (local node and IPFS Companion hide it).

Output to stdout:
============================
STAGE 4 COMPLETE
Seeded from manifest: N    from ipfs.txt: N
Rows with local file: N    CID computed: N    already present and matching: N
CID mismatches (bytes changed): N (listed)
Pinned on local node: N    NOT pinned: N (listed — THESE PUBLISH AS DEAD PLAYERS)
Rows left cid "": N (listed — no file, no manifest record)
CID index built: N v0 + N base32 forms
Nothing pinned by this stage: confirmed
============================

============================
STAGE 5 — CLUSTER THE CORPUS BY CONCEPT
============================

  1. {CK_FILE} for the investigation's real concepts and open questions.
  2. Each TRANSCRIPTION: what the speaker CLAIMS usually decides the cluster (the deciding input).
  3. ## Overview and ## Shot-by-shot: what is SHOWN often differs; note the claim-vs-footage gap on the entry.
  4. Manifest description, and for mirror video its folder (filing intent). __TO_FILE, backup, Old, Organized,
     TO_TRANSCRIBE, Other are work queues, not concepts.
  5. The folder proposes, the transcription decides, {CK_FILE} arbitrates.
  6. Six-to-twelve; over twelve direct = split deeper.
Reuse the old tree shape where it fits; discard where not (it came from image concepts). Mint _keys (prefer a
matching section's page_key from {PAGES_CSV} when free; it makes Stage 9 trivial). Cross-filing: file under
both concepts with also_filed_in on each; same cid twice under ONE node is a bug.

Output to stdout:
============================
STAGE 5 COMPLETE
Videos clustered: N     Clusters proposed: N level_3 / N level_4 / N level_5
Reused from old tree shape: N _keys      Newly minted: N
Cross-filed videos: N
Claim-vs-footage gaps noted: N
Nodes over the 12 ceiling (needs_split): N
Unclusterable (no transcription, no description): N (listed)
============================

============================
STAGE 6 — WRITE {HIERARCHY_FILE}
============================

MODE DETECTION (before writing):
  REBUILD — entries are inherited image data: more than 100 file_paths ending .jpg/.jpeg/.png/.gif/.webp, or
    more than 100 ai_description values beginning "This image". Discard old entries and counts; write fresh
    from Stages 2-5. Expected exactly once.
  UPDATE — entries are video files whose cids match the corpus index. Only grows: match by cid, then sha256,
    then file_path; update in place; add new; delete nothing; no duplicates.
  Print the mode and evidence. Ambiguous: STOP and report (a wrong guess discards good data).

REBUILD: first copy the file to {GENERATOR_DIR}/videos.yaml.pre_rebuild.bak (git history is the real net; the
copy makes the diff easy to review).

WRITE (by a script in {GENERATOR_DIR}, never by hand):
* Header comment: what the file is (MASTER DATA for video), when rebuilt and from what, meaning of publishable,
  media_present and transcription_source, that empty is "" never null, that cid is the primary identity
  because the site plays from public gateways, and that publishable: false nodes generate no page.
* The Stage 5 tree with the full schema; every entry carries every key.
* Deterministic: stable key, node and video order (by cid, else basename); rerun with no change = byte-identical.
  Reuse the emit_node approach from {IMAGE_GENERATOR_DIR}/bind_image_pages.py.
* `|` block scalars for shot_timeline; double-quoted scalars for every path and identity field; escape quotes.
* Apply OUTPUT SANITIZATION, then validate.
* Parse check: `python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" {HIERARCHY_FILE}`

Output to stdout:
============================
STAGE 6 COMPLETE
Mode: REBUILD | UPDATE   (evidence: ...)
Backup written: {GENERATOR_DIR}/videos.yaml.pre_rebuild.bak   (rebuild only)
Inherited image entries discarded: N   (rebuild only)
Video entries written: N
Nodes written: N level_3 / N level_4 / N level_5+
Every entry carries the full property set: yes
YAML parses: yes    Sanitization validation: passed
File size: N lines, N bytes (was N lines, N bytes)
============================

============================
STAGE 6B — BANNED: SYNC THE BAN SET ONTO EVERY ENTRY
============================

The ONLY stage that writes `banned:`; it copies a decision, reasons about nothing. Run every run right after
Stage 6, and again whenever the CSV changes (cheap, idempotent).

STEP 1 — READ: parse {BAN_VIDEOS_CSV} with the python3 csv module (header
  sha256,cid,file_path,banned,reason,date_added; create it if missing: missing = nothing banned, not skip).
  banned strictly "true"/"false" any case; else malformed: STOP and report. Lookups by sha256, cid, expanded
  file_path. Every identifier in {EXCLUDE_FILE} (cid and/or sha256, one per line, "#" comments ignored) joins
  as true unless a CSV row for it says false (CSV un-ban wins).
STEP 2 — SET on every entry at every depth: sha256, then cid, then file_path; first match wins; no match =
  false. Key on EVERY entry, never omitted or null. Never delete a banned entry.
STEP 3 — REPORT CSV rows matching nothing, with reason (stale identity after re-encode; an image in the wrong
  CSV, check {ROOT_DIR}/images/ban_images.csv; or legitimate pre-emptive). Never delete them.
STEP 4 — RECOMPUTE publishable now (a node whose contents just got banned stops being publishable this run).
STEP 5 — RE-EMIT with Stage 6's emitter (no change = byte-identical), verify it parses, apply OUTPUT
  SANITIZATION (treat the reason column as untrusted).
DO NOT here: touch any page or poster (p_yaml_to_site.md's job); clear video_page, on_pages or
should_be_on_pages (on_pages is the observation telling the page prompt what to delete; Stages 12-13 handle
the rest); touch IPFS.

Output to stdout:
============================
STAGE 6B COMPLETE
{BAN_VIDEOS_CSV}: N rows (N banned=true, N banned=false un-bans)
{EXCLUDE_FILE}: N identifiers
Entries marked banned: true : N   (by sha256: N, by cid: N, by file_path: N)
Entries marked banned: false: N
Every entry carries the banned key: yes
CSV rows matching no entry: N   (listed with reason)
Nodes flipped to publishable: false because all their videos are banned: N
YAML parses: yes    Byte-identical to Stage 6 output when nothing banned: yes/no
============================

============================
STAGE 7 — SITE LEVEL 2 SWEEP → THE LEVEL_3 SUPERSET
============================

level_3 must include every site Level 2 except: Videos (this YAML is its content), Photos (images
pipeline), Topics3 (scaffolding; /Topics3/Videos is unrelated), unfiltered/queue/catch-all categories (keep
exactly ONE "Other" level_3 and fold other_topics-style catch-alls into it), and docs-root non-page files
(index.mdx, Topics.mdx, image_list.csv, video_list.csv, index.html).

For each remaining site Level 2:
* Match an existing level_3 by _key, title and MEANING (TPUSA covers TPUSA; "The UVU Venue" UVU; "Ballistics
  and the Gun" Gun_Bullet; "Aircraft and Flight Evidence" Planes; "CIA and US Intelligence" intelligence and
  US_Intelligence; "Court and Legal Proceedings" court, Legal, legal_investigation). No duplicate concepts.
* site_level_2 = LIST of site dirs covered ([] = corpus-only).
* Uncovered: append one (title from section name, unique _key, number_of_videos 0,
  number_of_videos_recursive 0, videos [], site_level_2 [<dirname>], publishable false).
* Never remove or rename a level_3.

Output to stdout:
============================
STAGE 7 COMPLETE
Site Level 2s swept: N        Matched to existing level_3: N
New level_3 nodes added: N (list _keys)
Excluded: Videos, Photos, Topics3, non-page files
Other node present: yes       level_3 total: N (publishable N)
============================

============================
STAGE 8 — HOME PAGE TABLES OF CONTENTS → MORE LEVEL_3S
============================

{HOME_PAGE} has MORE THAN ONE TOC: the three-column flex divs under "Biggest Question Marks", "## Table of
Contents", "## Areas of Investigation", "Related Areas"/"Related", and per-thesis link clusters (Tyler
Robinson Not Assassin, Cause of Death, Mossad / Israel Top Suspect, US Intelligence Assisted, ...).
* Read it fully; extract EVERY TOC and link cluster; resolve each to its section.
* Add a level_3 (Stage 7 rules) for each uncovered concept; for covered ones you may improve the title or
  append to site_level_2. This stage is EXPECTED to add nodes.

Output to stdout:
============================
STAGE 8 COMPLETE
TOC sections parsed on home page: N    Concepts found: N
Already covered: N    New level_3 nodes added: N (list _keys)
============================

============================
STAGE 9 — SITE LEVEL 3/4 PAGES → LEVEL_4/LEVEL_5 NODES
============================

For every site Level 2 mapped via site_level_2:
* Enumerate its Level 3 pages (overview, every page file in the dir, first-level subdir overviews); {PAGES_CSV}
  level and parent_key guide, the filesystem decides.
* Each Level 3 page -> level_4 under the right level_3: title (frontmatter title or first H1), _key (unique,
  four words max; prefer the page_key when free), site_page (repo-relative), number_of_videos,
  number_of_videos_recursive, videos: [], publishable.
* Each Level 4 page -> level_5 under the right level_4, same fields.
* Same concept as an existing corpus node: MERGE (keep node, add site_page).
* Skip pure-navigation pages only when they'd duplicate their parent empty; when in doubt include (the
  publishable gate handles emptiness).
* Never remove nodes or entries.

Output to stdout:
============================
STAGE 9 COMPLETE
Site Level 3 pages processed: N → level_4 nodes (N new, N merged)
Site Level 4 pages processed: N → level_5 nodes (N new, N merged)
Nodes now in tree: N total, N publishable, N with zero videos
============================

============================
STAGE 10 — PAGE VIDEO SWEEP → VIDEO ENTRIES
============================

* Scan every page under {DOCS_DIR} and {SITE_DIR}/blog for <video> src and poster, <iframe src> (YouTube,
  Rumble, Odysee, X), IPFS gateway URLs, markdown links to media files, and require()/import in JSX.
* For each video: CID from an IPFS URL is exact identity; otherwise resolve the local file and sha256 it. Match
  to the corpus index by cid, then sha256, then filename.
    * Exists in YAML: no duplicate; update in place and append the page to on_pages.
    * New: add under the level_4 (or level_5) mirroring the page it was found on; fill every key (Stage 3 fills
      sidecars if present, else "").
* THIRD-PARTY VIDEO (YouTube, Rumble, X): cid "", source_platform set, watch URL in source_url; real evidence;
  its page gets an external embed, not our player; mark it so the generator knows. {VIDEO_LIST_CSV} is a
  starting index; the page scan is authoritative.
* Inline embeds stay where they are; this hierarchy is an index.

Output to stdout:
============================
STAGE 10 COMPLETE
Pages scanned: N     Videos found on pages: N (N matched to corpus)
IPFS-hosted: N    third-party hosted (YouTube/Rumble/X): N
New video entries added: N    Existing entries updated: N
Unresolvable embeds: N (listed with page + src)
============================

============================
STAGE 11 — ON_PAGES: WHERE ELSE IN THE REPO EACH VIDEO IS SHOWN
============================

video_page = which page IS this video (its one Level 5 page, Stage 12). on_pages = where ELSE it is shown
(every other page embedding it), set here, OBSERVED only.

SHAPE: list of `page:` mappings with tilde paths; [] when none (not flat strings, not repo-relative, not URLs):
    on_pages:
      - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/Mic/overview.mdx"

ONE LINEAR PASS (reverse index), each file read ONCE:
* Every text file under {ROOT_DIR} (.md .mdx .html .tsx .jsx .ts .js .json .csv .yaml), skipping node_modules/,
  build/, .git/, .docusaurus/, binary static assets.
* Extract every form: <video> src/poster; <iframe src> (YouTube, Rumble, Odysee, X); IPFS URLs
  (https://ipfs.io/ipfs/<CID>[/name], https://<CID>.ipfs.dweb.link/[name], ipfs://<CID>); markdown media links
  [label](/videos/xxx.mp4); require()/import. Match tags multi-line aware (the images pipeline found a
  line-oriented regex missed 72% of tags split across lines).
* Resolve, in order:
    1. CID -> Stage 4 index, EXACT; compare both v0 and base32 v1 forms.
    2. Third-party id (YouTube watch id, Rumble slug) -> Stage 10 entry. Exact.
    3. Local media file -> sha256. Exact.
    4. Basename vs file_path basenames: AMBIGUOUS (numeric X ids); accept only a unique match, else report.
* Append the page's tilde path; dedupe.

SCOPE — not in on_pages: pages under {VIDEOS_L2_DIR} (own page = video_page; cluster listings are structure);
{THIS_DIR}, {GENERATOR_DIR}, {HIERARCHY_FILE}, {VIDEO_MANIFEST}, {VIDEO_INDEX_MD}, {PAGES_CSV}; anything
outside {ROOT_DIR}.

INHERITED BINDINGS: rebuild mode starts every list empty. Update mode: re-verify each existing binding against
the page's current text; drop and report any the sweep cannot confirm. Never write a binding from topical
reasoning.

PARALLELISM: script the mechanical pass; agents (up to 12, whole directories each, balanced by file count) only
for the residual. Agents RETURN (page_path, resolved_identity, evidence) rows and never edit the YAML; a single
writer merges in one pass.

Output to stdout:
============================
STAGE 11 COMPLETE
Files read: N        Video references found: N
Resolved by CID: N   by third-party id: N   by sha256: N   by basename: N
Unresolved: N (listed with page + reference)
Entries with on_pages non-empty: N    Total page bindings: N
Pages excluded by scope rule: N
============================

============================
STAGE 12 — VIDEO_PAGE: BIND EVERY VIDEO TO ITS LEVEL 5 PAGE
============================

The VIDEO PAGE (Level 5) hosts the player, a title, and prose on what the footage shows, who speaks, what they
claim, why it matters:
  Videos (Level 2) > Mic_Thesis (Level 3 cluster overview) > Vid_Candace_Mic_2067372.mdx (video page)
Generated by {GENERATOR_DIR}/gen_videos_pages.py via p_yaml_to_site.md and p_level2_update.md; they may not
exist yet ({VIDEOS_L2_DIR} held only overview.mdx, _category_.json, and hand-written
buckley-carlson-kash-patel-valhalla.mdx). This stage only READS pages; early runs correctly set "".

video_page = tilde path, e.g.
    video_page: "~/BGit/Bryan_git/charlie-kirk/site/docs/Videos/Mic_Thesis/Vid_Candace_Mic_2067372.mdx"

MATCH via frontmatter:
    ck_video_cid: QmZdFUWDekCDBZcETphabnmTW4Y9vYk7EyPUJECsBXuDfo
    ck_video_sha256: 9044e164a9c6e76fbe9e1746d11bbc155b2fbfbbfc310b6631017c6e5998945d
    ck_node_key: Mic_Thesis
  * Index every .mdx under {VIDEOS_L2_DIR} declaring ck_video_cid or ck_video_sha256 by (identity, ck_node_key).
  * CID IS THE PRIMARY KEY (sha256 is often empty); fall back to sha256.
  * Exact pair (identity, enclosing node _key) first (makes cross-filing work); else identity alone: one hit =
    use; several = nearest ck_node_key (same parent, then same level_3 subtree). None = "".
  * Hand-written pages without ck_ frontmatter: never guess by filename; count and report.

RULES:
  * Set on EVERY entry. Verify the file exists at write time, else "".
  * Never a path outside {VIDEOS_L2_DIR}, and NEVER under {DOCS_DIR}/Photos. Embeds elsewhere are on_pages.
  * Never replace a non-empty video_page with ""; report vanished pages.
  * IDENTITY field: non-ASCII as visible \uXXXX escapes.
  * BANNED ENTRY: video_page "" always (clearing is correct). If a page carrying its identity exists: do not bind
    or delete it; write "", REPORT loudly with page path and ban reason so p_yaml_to_site.md deletes it; count
    separately (non-zero = banned footage is live now).

Output to stdout:
============================
STAGE 12 COMPLETE
Video pages indexed under Videos: N (N with ck_ frontmatter, N without)
Entries with video_page set: N   by (identity,node): N   by identity only: N
Entries with video_page "": N (no page exists yet)
Banned entries skipped: N   of those, LIVE PAGES FOUND NEEDING DELETION: N
  (each listed with page path and ban reason)
Recorded pages now missing from disk: N (listed)
Paths under /Photos rejected: 0
============================

============================
STAGE 13 — SHOULD_BE_ON_PAGES: WHERE EACH VIDEO OUGHT TO APPEAR
============================

The one REASONED property: worked out from what the video SAYS, SHOWS, and what each page is about. Almost
every video appears only on its own Level 5 page; a reader on Ballistics, N1098L or the mic thesis should be
offered that topic's footage where they are. This is the worklist p_yaml_to_site.md Stage 6 consumes. This
prompt only RECORDS it (places nothing, edits no page, creates no page).

UNION RULE: should_be_on_pages ⊇ on_pages, the COMPLETE desired state (repeat every on_pages page unless it is
a wrong placement; record each subtraction with its reason). Stage 11 must be clean first (the images
pipeline once carried 946 fabricated bindings, 89%; unioning them would have made fabricated publishing
instructions): confirm zero unresolved/unverified bindings, or re-verify on_pages by reopening pages if
Stage 11 did not run this session.

SHAPE: same as on_pages; [] when none. Not a video-page path.
    should_be_on_pages:
      - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/Suspicious/Cause_of_Death/entrance-or-exit.mdx"

BANNED ENTRIES: should_be_on_pages: [] and nothing else (no reasoning, NO union of on_pages, which for a banned
video lists pages it must be REMOVED from). Clear prior pages and report each. A banned entry with non-empty
on_pages = live footage: report a REMOVAL WORKLIST (page + ban reason) and leave on_pages untouched. Nothing
links into a banned video anywhere.

EVERY PATH MUST BE REAL, FULL, AND VERIFIED — NO PLACEHOLDERS.
  * Hard failures if they reach the file:
      - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/....mdx"
      - page: ".../site/docs/Mic/overview.mdx"
      - page: "site/docs/Mic/overview.mdx"             (repo-relative)
      - page: "/Mic/overview"                          (a URL path)
      - page: "~/.../charlie-kirk/site/docs/Mic/rigged-mic.mdx"  (invented file)
    Any "...", "TODO", "TBD", "<", ">" or other placeholder, or a value not an absolute tilde path ending
    .md/.mdx, is invalid.
  * ONLY LEGAL WAY — a candidate index built once:
      1. {PAGES_CSV} file_path (repo-relative) expanded to {ROOT_DIR}/<file_path> in tilde form.
      2. Union a walk of every .md/.mdx under {DOCS_DIR}.
      3. stat() every candidate; drop non-existent. That set is THE index.
      4. Every value is an index key byte for byte; nothing constructs a string.
  * VERIFY BEFORE AND AFTER WRITE (re-stat; after emit re-parse, expanduser, stat). Any miss FAILS the stage; no
    partial file, no degrading to "".
  * Missing right page: "Wanted pages that do not exist" (cid + suggested title) in stdout and {FINDINGS_FILE};
    write only real pages.

DECISION INPUTS, by weight (video matches on what is SAID by a named person over time):
  1. THE TRANSCRIPTION sidecar (heaviest by far): names, tail numbers, case numbers, times, a thesis stated
     aloud. A four-minute mic monologue belongs on Mic pages even over a talking head.
  2. ai_description, shot_timeline, people_seen, onscreen_text (what is SEEN). Reconcile: the claim picks the
     topical page; the footage decides whether the page can present it as evidence. Note discrepancies in
     {FINDINGS_FILE}.
  3. The enclosing node (_key, title, site_level_2 / site_page): cheapest strong signal (a video under the level_4
     whose site_page is site/docs/Planes/N1098L.mdx almost certainly belongs there).
  4. Provenance (source_url, source_author, manifest_description) and mirror folder.
  5. {PAGES_CSV} title, description (best cheap matcher), page_type (person pages need the video to feature or
     substantially concern the person), level, level2_section, url_path.
  6. {CK_FILE} arbitrates transcription vs cluster.

TARGETING: Level 3 analysis pages (Level 4 equally good). Level 2 overviews only for one emblematic clip at most
(videos are heavy). NEVER under {VIDEOS_L2_DIR} or {DOCS_DIR}/Photos; nothing in {THIS_DIR}, {GENERATOR_DIR},
{HIERARCHY_FILE}, {VIDEO_MANIFEST}, {VIDEO_INDEX_MD}, {PAGES_CSV}, outside {ROOT_DIR}; no Topics3 pages
(incl. /Topics3/Videos).

QUANTITY, tighter than images (a placed video is a gateway fetch of 0.5MB to 173MB; never relax to hit coverage):
  * One to three pages per video normal; FOUR ceiling (a generic clip gets the one or two where it is evidence).
  * [] is common and correct; never pad (a weak match puts an unexplained heavy embed on a page).
  * PER-PAGE LOAD max SIX videos across the corpus; keep the strongest six, report overflow under "Wanted pages
    that do not exist".
  * cid "" and ipfs_pinned false entries: still plan them, but count and report (dead or pending cards until pinned).

DEFAMATION GATE (accusations are made OUT LOUD; the media is the payload):
  * cid or sha256 in {EXCLUDE_FILE}: should_be_on_pages: [] unconditionally.
  * A video showing or naming a living person goes only where that person's presence is the point (consult people_seen).
  * A speaker accusing a living person of a crime: never on that person's own profile page. Reporting that a
    video CONTAINS a claim is fine on a topical page that frames it.
  * Continuous uninvolved bystanders' faces or voices: flag as an {EXCLUDE_FILE} candidate, not wider placement.
  * Unsure: leave it out and note it.

ACCEPTANCE TARGETS (over ALL entries after the write; print the table; retune on a miss):
    should_be_on_pages empty []              >= 5%   and <= 25%
    should_be_on_pages with >= 1 page        >= 75%
    should_be_on_pages with >= 2 pages       >= 20%
    on_pages empty []                        < 100%  (all-empty means broken)
  The empty floor matters (assigning everything = no discrimination). Bands are wider than images because ~50
  videos swing percentages. on_pages is a liveness check only; never tune it.

HOW TO RUN:
  * Candidate index and mechanical filters (ban set, Videos/Photos exclusions, per-page load) are SCRIPTED in
    {GENERATOR_DIR}/plan_should_be.py, modelled on {IMAGE_GENERATOR_DIR}/plan_should_be.py (read it, never edit).
  * SELECTION IS JUDGMENT HERE: lexical scoring measured only 65-70% precision for images (strong on exact
    tokens, weak on generic geography). ~50 transcriptions that state their thesis are affordable to read and
    far more accurate. Use scoring only as a CANDIDATE GENERATOR (~12 pages per video). If scoring, keep the
    images lessons: drop bare digit runs; sublinear tf (1 + log tf) on the video side; title-match bonus for a
    shared distinctive token (idf >= 4); structural prior PROPORTIONAL to the entry's best score (0.75x nearest
    ancestor's site_page, 0.35x further); person pages gated on the WHOLE name.
  * PARALLELISM: up to 12 agents partitioned by cluster subtree (never split a video). Each gets its videos'
    transcriptions and candidate index keys and RETURNS (cid, node_key, selected_index_key, confidence, one-line
    reason). Paths not in the index are REJECTED and counted. Agents never edit the YAML; one writer merges.
  * The writer applies quantity and defamation rules, unions on_pages, dedupes, sorts, re-stats, writes once.

RULES: key on EVERY entry ([] never "" or missing). Grow, do not clobber: merge with earlier selections; remove
only when the page is gone or the video newly excluded, and report why. Order each list BEST MATCH FIRST (the
publishing prompt's per-page cap keeps the head). Page values are IDENTITY fields (\uXXXX escapes).

Output to stdout:
============================
STAGE 13 COMPLETE
Candidate index: N pages (N from pages.csv, N from filesystem walk, N dropped as non-existent)
Video entries processed: N
Entries with should_be_on_pages non-empty: N   total page assignments: N
Assignments carried over from on_pages: N   new assignments proposed: N
Subtractions from on_pages (wrong placements, with reasons): N (listed)
Entries left [] : N (N banned, N excluded by {EXCLUDE_FILE}, N no topical match)
Banned entries with a non-empty on_pages — REMOVAL WORKLIST: N (listed with page + reason)
Banned entries whose should_be_on_pages was cleared this run: N (listed)
Level 2 overview assignments: N   Level 3: N   Level 4: N
Assignments whose video has no playable cid (planned but not servable): N
Agent rows rejected (path not in candidate index): N
Pages over the 6-video load: N (listed with overflow counts)
Wanted pages that do not exist: N (listed: suggested title + video cid)
Acceptance targets: [] N% / >=1 N% / >=2 N%   PASS/FAIL
Path validation: N/N resolve to an existing file on disk — placeholders found: 0
============================

============================
OUTPUT SANITIZATION — NO INVISIBLE UNICODE, EVER (SECURITY RULE)
============================

The emitted {HIERARCHY_FILE} must contain no invisible Unicode (hides content, spoofs strings, smuggles
instructions). The invisible set includes at minimum: U+0000-U+0008, U+000B-U+001F, U+007F-U+009F, U+00A0,
U+00AD, U+034F, U+061C, U+115F, U+1160, U+17B4, U+17B5, U+180B-U+180E, U+2000-U+200F, U+2028-U+202F (U+202F
NARROW NO-BREAK SPACE is what macOS puts before AM/PM in screenshot filenames; it WILL appear), U+205F-U+206F,
U+3000, U+3164, U+FE00-U+FE0F, U+FEFF, U+FFA0, U+FFF9-U+FFFB, U+E0000-U+E007F.
Visible non-ASCII in the inputs is fine in prose (U+00B7 middle dot and U+2713 check mark in transcription
headers; em dashes and curly quotes in descriptions).

  * PROSE fields (title, ai_description, shot_timeline, people_seen, onscreen_text, manifest_description, node
    titles): replace space-like invisibles (U+00A0, U+2000-U+200A, U+202F, U+205F, U+3000) with a space, DELETE
    zero-width/bidi/control/joiner chars, collapse whitespace. Visible non-ASCII stays.
  * IDENTITY fields (file_path, audio_file, transcription_file, ai_description_file, ocr_file, video_page,
    ipfs_url, source_url, on_pages and should_be_on_pages page values, cid, sha256, also_filed_in, site_page,
    site_level_2): must keep matching the real file, so emit ALL non-ASCII as visible escapes in YAML
    double-quoted scalars (a U+202F becomes the six characters backslash, u, 2, 0, 2, F). Parsed value unchanged.
  Never paste a literal invisible character anywhere, including when writing this rule; trust the scan, not the rule.

MANDATORY after every emit: re-scan and HARD FAIL on any invisible code point; re-parse and spot-check that an
escaped file_path resolves. Reuse the approach in {IMAGE_GENERATOR_DIR}/sanitize_common.py.

============================
STAGE 14 — COUNTS, PUBLISHABLE, NEEDS_SPLIT, INTEGRITY
============================

* Recompute number_of_videos and number_of_videos_recursive on every node, counting EVERY entry incl. banned
  (counts describe what is held; publishable is where bans show).
* publishable on every node: true when the subtree has at least one banned-false video. Report separately nodes
  whose videos are ALL banned (counts and flag disagree; otherwise looks like a bug).
* needs_split: over 12 direct -> true; at or under 12 -> remove.
* Every _key unique file-wide. No cid twice within a node (across nodes = cross-filing; keep also_filed_in accurate).
* Every entry has the FULL schema ("" / [] / false for empties).
* on_pages ⊆ should_be_on_pages, or the entry is listed with its subtraction reason.
* Every should_be_on_pages value: absolute tilde path, .md/.mdx, EXISTS, no placeholder, outside {VIDEOS_L2_DIR}
  and {DOCS_DIR}/Photos. Hard fail otherwise.
* banned is a real boolean on every entry (hard fail otherwise). Re-read {BAN_VIDEOS_CSV} now and confirm agreement.
* Banned entries with non-empty should_be_on_pages: 0; with non-empty video_page: 0.
* No {EXCLUDE_FILE} entry has a non-empty should_be_on_pages.
* Report every page over the six-video load.
* Every non-empty transcription_file, ai_description_file, ocr_file, audio_file, file_path EXISTS (a dangling path
  is worse than ""); report each.
* Every non-empty video_page exists under {VIDEOS_L2_DIR}; zero under {DOCS_DIR}/Photos.
* Zero file_paths with an image extension; zero ai_description values beginning "This image" (survivors of the rebuild).
* YAML parses. OUTPUT SANITIZATION scan passes.

Output to stdout:
============================
STAGE 14 COMPLETE
Counts recomputed: yes
Nodes: N total, N publishable, N with zero videos (not published)
Nodes not publishable because every video in them is banned: N (listed)
Entries banned: N   banned values disagreeing with {BAN_VIDEOS_CSV}: 0
Banned entries with a non-empty should_be_on_pages: 0   with a video_page: 0
needs_split nodes: N
Duplicate _keys: 0        Duplicate cid within a node: 0
Entries missing a schema key: 0
Sidecar paths that do not resolve on disk: N (must be 0, listed)
Entries with an image file_path: N (must be 0)
ai_description values starting "This image": N (must be 0)
should_be_on_pages paths validated: N/N exist on disk   placeholders: 0
on_pages not a subset of should_be_on_pages: N (each with a recorded reason)
Excluded entries with a non-empty should_be_on_pages: 0
Pages over the 6-video load: N (listed)
YAML parses: yes     Sanitization: passed
============================

============================
STAGE 15 — VERIFY AND REPORT
============================

* Every non-excluded site Level 2 maps to exactly one level_3; Other exists; every home-page TOC concept resolves.
* Every {VIDEO_MANIFEST} record and every .mp4 in {VIDEOS_DIR} appears exactly once (cross-filed copies carry
  also_filed_in).
* Every .transcription and .ai_description under {REPO_VIDEO_SIDECAR_DIR} and {REPO_IPFS_SIDECAR_DIR} is
  referenced by exactly one entry (an unreferenced one = a video Stage 2 missed).
* Spot-check 10 entries end to end (media or CID, transcription, ai_description; duration, engine, prose and
  shot_timeline match the sidecars).
* Spot-check 10 should_be_on_pages assignments BY HAND (page subject vs transcription); report the hit rate
  honestly (the images audit came back 65-70%, not the 100% scores implied).
* Print the final tree: each level_3 _key with recursive count, child count, publishable.
* Append to {FINDINGS_FILE}: transcription work list, unpinned list, unresolved references, no-coverage nodes,
  the .ocr format.

Output to stdout:
============================
STAGE 15 COMPLETE — FINAL REPORT
Nodes: N level_3 / N level_4 / N level_5+   (N publishable)
Total video entries: N
Corpus coverage:
  {VIDEOS_DIR} .mp4 in YAML:            N of N
  manifest records in YAML:             N of N
  {IPFS_VIDEOS_DIR} originals in YAML:  N of N
  sidecars referenced by an entry:      N of N
SIDECAR COVERAGE (the point of this run):
  transcription_file set:   N of N  (N%)   own video N / audio sibling N
  ai_description_file set:  N of N  (N%)
  ocr_file set:             N of N  (N%)
  duration harvested:       N of N  (N%)
  shot_timeline harvested:  N of N  (N%)
  transcript_complete true: N of N  (N%)
CID coverage: N% (N of N)      pinned: N% (N of N)
video_page coverage: N% (N of N bound to a Level 5 page)
BANNED: N entries banned (no Level 5 page, no placement, no pin)
  {BAN_VIDEOS_CSV} rows: N   {EXCLUDE_FILE} identifiers: N
  banned entries still live on the site (removal worklist): N (listed)
should_be_on_pages coverage: N% (N of N planned onto at least one topic page)
Publishing worklist (should_be_on_pages minus on_pages): N placements pending
Every should_be_on_pages path exists on disk: confirmed
Hand-audited assignment precision: N/10
Videos with NO transcription (work list): N (listed)
Findings written to: {FINDINGS_FILE}
============================

============================
HARD RULES
============================

* {HIERARCHY_FILE} is the MASTER DATA. Only Stage 6 REBUILD mode may replace it wholesale (once). In UPDATE mode it
  only grows: no deletes, no duplicates, update in place.
* EVERY entry carries EVERY schema key ("" / [] / false for empties).
* on_pages is OBSERVED, should_be_on_pages is REASONED and a SUPERSET of on_pages (complete desired state). Never
  let topical reasoning write on_pages or let an unverified binding flow into should_be_on_pages. Exception: a
  banned entry gets should_be_on_pages: [] and its on_pages is a removal worklist.
* banned is COPIED DOWN from {BAN_VIDEOS_CSV} by Stage 6B only; real boolean, default false. Banned = no Level 5
  page, no poster, no placement, no link, never pinned; entry never deleted. Add CSV rows for newly found
  non-public material before the run ends.
* Every path written (file_path, sidecar paths, video_page, on_pages, should_be_on_pages) is an absolute tilde path
  to a file that EXISTS at write time. Placeholders, ellipses, repo-relative and URL paths are hard failures. A
  missing page is a finding, never an invented path.
* transcription_file, ai_description_file, ocr_file are REQUIRED; filling them is the primary purpose.
* No page create/move/edit under {SITE_DIR}; no sidebars.ts; no {PAGES_CSV} edits.
* Never write under {IMAGE_PLANNING_DIR}, {ROOT_DIR}/images, or {DOCS_DIR}/Photos; never copy files from there here.
* Never copy video bytes into {SITE_DIR}/static (gateways serve video; only a small poster may later live in
  {SITE_DIR}/static/img/video_posters/).
* NOTHING IS EVER PINNED by this prompt; any pinning job first filters out the ban set.
* _keys unique file-wide, ASCII only. No invisible Unicode (scan after every emit).
* Clusters: the folder proposes, the transcription decides, {CK_FILE} arbitrates.
* DEFAMATION: harvested fields become public later. A speaker's out-loud accusation is captured verbatim in the
  transcription; reporting that a video CONTAINS a claim is fine, repeating it in the site's voice is not. Never
  put an accusation in `title` or `ai_description` (copied into headings and link text). Raw claims stay in the
  sidecar and {CK_FILE}; the later prompt quotes and attributes deliberately.
* No Docusaurus pages in {THIS_DIR}, no planning notes in {VIDEOS_L2_DIR}, no YAML copy in {THIS_DIR}.
