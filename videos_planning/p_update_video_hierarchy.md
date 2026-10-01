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
  (Real file. Moved 2026-09-19. ~/BGit/Bryan_git/charlie-kirk/Charlie_Kirk.txt is now a symlink to it —
   use that only to verify the location; always read and write the real path.)
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

Build {HIERARCHY_FILE} — the master video data file for the investigation — so
that it is the single, complete, accurate record of every video we hold: what it
is, where its bytes are, what its IPFS CID is, what was SAID in it, what is SEEN
in it, what text is burned into it, which concept cluster it belongs to, and
which pages show it.

{HIERARCHY_FILE} is the MASTER DATA. It is not a by-product of the site and it
is not a copy of anything. Every later prompt in this pipeline reads it and none
of them re-derives the corpus.

The single most important thing this prompt does is FILL IN THE SIDECAR DATA.
Large File Bridge has already done the expensive work — it transcribed the
speech, it ran a vision model over the footage, and it OCR'd the burned-in text.
That work sits in text files on disk right now and none of it is in the YAML.
Getting it in — transcription_file, ai_description_file, ocr_file, and the
parsed values behind them — is the point of this run. Everything else in this
prompt is structure around that.

THE FIRST RUN IS A REBUILD, NOT AN UPDATE.

{HIERARCHY_FILE} today holds ~1,740 entries and ~1,365 nodes inherited from
{ROOT_DIR}/images/images.yaml. Only the KEYS were converted to the video schema
on 2026-07-23. Every value in it describes an IMAGE: file_paths ending .jpg /
.jpeg / .png under {MIRROR_DIR}, sha256 and cid computed over image bytes,
ai_description prose that literally begins "This image shows...", on_pages
bindings harvested for images, and counts that count images. There is no useful
data in it to preserve and no reconcile pass is worth writing.

So Stage 6 REPLACES the file wholesale from the corpus index built in Stages
2-5. Do not try to salvage entries. The only thing worth reading out of the old
file first is its TREE SHAPE — the cluster titles and _keys — as a proposal for
what the concept clusters might be, and even that is a proposal the
transcriptions are free to overrule.

From the SECOND run onward the file only grows: entries are updated in place,
never duplicated, and never deleted. The rebuild is a one-time event and Stage 6
detects which mode it is in (see Stage 6, MODE DETECTION).

Convergence priority order (if context runs short, complete in this order):
   1. Stage 2  — the corpus index (what videos exist)
   2. Stage 3  — the sidecar harvest (transcription / ai_description / ocr)
   3. Stage 4  — CID and pin status
   4. Stage 5  — clustering
   5. Stage 6  — rebuild {HIERARCHY_FILE}
   6. Stage 6B — banned: sync the ban set from {BAN_VIDEOS_CSV} onto every entry
   7. Stage 14 — counts, publishable gate, integrity
   8. Stage 7  — site Level 2 sweep into the level_3 superset
   9. Stage 9  — site Level 3/4 pages into level_4/level_5 nodes
  10. Stage 10 — page video sweep
  11. Stage 11 — on_pages
  12. Stage 8  — home page tables of contents
  13. Stage 12 — video_page binding
  14. Stage 13 — should_be_on_pages (where each video OUGHT to appear)
  15. Stage 15 — verify

Stages 2 through 6B produce a correct, useful master data file on their own. If
the run stops after Stage 6B plus Stage 14, the result is still a win. Stages 7
through 12 add the site's structure on top of it, and Stage 13 turns the whole
file into a publishing plan.

Stage 6B is high in that order for a reason. It is cheap — one CSV, a few
lookups per entry — and everything after it is gated on it: Stage 12 refuses to
bind a Level 5 page to a banned video, Stage 13 refuses to plan a banned video
onto a topic page, and {THIS_DIR}/p_yaml_to_site.md deletes any page or poster
that already exists for one. A run that skips 6B produces a publishing plan that
plans banned footage.

Stage 13 depends on Stage 11 having run and being CLEAN — it unions on_pages
into should_be_on_pages, so a fabricated observation becomes a fabricated
publishing instruction. Never run 13 on an unverified 11.

============================
KNOWLEDGE — THE CORPUS CENSUS (VERIFIED ON DISK 2026-07-23)
============================

These numbers were counted directly. Re-count them at run time — they grow every
week — but a run that produces wildly different numbers without an obvious cause
has a bug, so treat these as the expected order of magnitude and report any
delta.

  {VIDEOS_DIR}
      46  .mp4          the primary corpus
      30  .mp3          audio extractions, siblings of some of the mp4s
       2  .txt          stray notes, not media
       3  metadata      manifest.yaml, videos.md, videos.yaml
      .gitignore excludes *.mp4 *.mp3 *.mkv *.avi *.mov *.wav *.webm

  {VIDEO_MANIFEST}
      63  records. NOT the same set as the disk. Specifically:
      18  manifest records name an .mp4 that is NOT on disk. Several of those
          have the matching .mp3 on disk instead (2046414464447287296,
          2046416264562921472, 2046416264567140352, 2068463186668605858,
          2069185145555255370, 2072814926133866634) — the video was fetched,
          the audio was extracted and kept, the video itself was not retained.
          These are REAL videos with real CIDs. They belong in the YAML.
       1  file on disk is NOT in the manifest: _QwGo0LyZ3I.mp4 (130MB, a
          YouTube-id filename, not an X status id). It needs a CID computed and
          an entry created.

  {REPO_VIDEO_SIDECAR_DIR}   ({ROOT_DIR}/.lfbridge/videos/)
      74  .transcription   = 44 named *.mp4.transcription
                           + 30 named *.mp3.transcription
      44  .ai_description  all named *.mp4.ai_description
       2  .ocr             2079054276320440416.mp4.ocr
                           2079275082648809861.mp4.ocr

      44 of the 46 mp4s have BOTH a transcription and an ai_description.
      The 2 with neither: 2079560806690324910.mp4, 2079684519762993659.mp4.
      Neither has an .mp3 sibling, so neither has a fallback. They are the
      transcription work list — report them, do not guess at their content.

       7  of the 30 .mp3.transcription files have NO .mp4 on disk at all:
          2046414464447287296, 2046416264562921472, 2046416264567140352,
          2068463186668605858, 2069185145555255370, 2071736376215920842_extracted,
          2072814926133866634.
          For those, the .mp3.transcription IS the only record of what was said.
          See THE AUDIO SIBLING RULE below — this is not an edge case, it is
          seven real videos.

  {REPO_IPFS_SIDECAR_DIR}   ({ROOT_DIR}/.lfbridge/IPFS/videos/)
       2  videos, each with transcription AND ai_description:
          "Blake Bednarz UVU original.MP4"   (uppercase extension, SPACES in
                                              the filename, ~3GB forensic
                                              original, CID in {IPFS_DIR}/ipfs.txt)
          "chain_of_evil.mp4"

  {REPO_SIDECAR_DIR} also holds images/, cover_image/, and site/ subtrees.
  Those belong to the images pipeline. Read nothing from them for this run
  except to confirm you are not accidentally walking them.

  Local IPFS: kubo 0.42.0 is installed at /opt/homebrew/bin/ipfs. Pin checks
  work. A spot check of Qmb49X85Y7wRdMEi7EgvEvjN3A8rdpZVvLfu2CuiSZwbwR returned
  "recursive", i.e. pinned.

  So the realistic corpus size is roughly 46 mp4 on disk + ~7 audio-only
  survivors + 2 IPFS forensic originals + any third-party-hosted video found on
  site pages — on the order of 55-65 video entries, not 1,740. If the rebuilt
  YAML has hundreds of video entries, something is wrong.

============================
KNOWLEDGE — SIDECAR FILES: WHAT THEY ARE, WHERE THEY ARE, WHAT IS INSIDE THEM
============================

This is the most important knowledge section in this prompt. The sidecars are
the data. Everything the site will eventually say about a video traces back to
one of these three files.

Large File Bridge (the web app at {LFB_DIR}) writes three sidecar text files per
media file. They answer three different questions:

  .transcription   "what was SAID"        — verbatim speech, from a local ASR
                                            model. THE PRIMARY SIDECAR FOR
                                            VIDEO. A video's claim is spoken,
                                            not shown, so this is what the
                                            clustering reasons over.
  .ai_description  "what is SEEN"          — a hosted vision model's structured,
                                            hyper-detailed prose about the
                                            footage, INCLUDING A TIMESTAMPED
                                            SHOT LIST.
  .ocr             "what does it SAY on
                    screen"                — chyrons, slates, burned-in captions.
                                            Rare on video (2 files today); when
                                            present the source is usually a
                                            screen-recorded post rather than
                                            filmed footage.

ALL THREE GET A YAML PROPERTY ON EVERY VIDEO ENTRY, ALWAYS. transcription_file,
ai_description_file, ocr_file. A sidecar that does not exist emits "" — never a
missing key, never null. A later pass must be able to tell "not looked up yet"
from "looked up, does not exist", and only an always-present key makes that
possible.

=== Naming rule ===

The sidecar keeps the media file's FULL filename — original extension included —
and APPENDS the second-level extension:

  2067372027623715212.mp4  →  2067372027623715212.mp4.transcription
                           →  2067372027623715212.mp4.ai_description
                           →  2067372027623715212.mp4.ocr

Case is PRESERVED, not normalised. "Blake Bednarz UVU original.MP4" produces
"Blake Bednarz UVU original.MP4.transcription" with the uppercase .MP4 intact. A
lookup that lowercases the extension will miss it. Filenames also contain SPACES
— quote every path in every shell command and never build a path by string
concatenation without quoting.

=== Placement rule — where the sidecar lives ===

Placement is keyed on the STORAGE KIND of the root the original sits in. The
authoritative spec is {LFB_PM_DIR}/artifact_placement_policy.mdx section 0;
{LFB_PM_DIR}/Transcribe.mdx, ai_description.mdx, ocr.mdx, and
repo_tracking_scheme.mdx carry the per-feature detail.

  * Original INSIDE A WORKING GIT REPO — the sidecar is path-mirrored under
    that repo's committed .lfbridge/ tracking directory. THIS IS THE NORMAL CASE
    FOR THIS PIPELINE, because the video corpus lives inside the charlie-kirk
    repo:

      {VIDEOS_DIR}/X.mp4
        →  {REPO_SIDECAR_DIR}/videos/X.mp4.transcription
      {IPFS_VIDEOS_DIR}/X.MP4
        →  {REPO_SIDECAR_DIR}/IPFS/videos/X.MP4.transcription

    The rule is: take the path of the original relative to the repo root, and
    reproduce it under {REPO_SIDECAR_DIR}. There is no analysis/ subdirectory
    and no .transcribe/ subdirectory. The tracking directory is committed, so
    the sidecars travel with the repo even though the media does not.

  * Original OUTSIDE any working git repo (the mirror) — there is NO .lfbridge/
    segment. A dedicated Large File Bridge file repo (an "SDL": a Personal,
    Company, or Community repo that exists only to hold these files) IS the
    tracking area, so the mirror hangs straight off its root:

      {MIRROR_DIR}/Teachers_Lounge/X.mp4
        →  {MIRROR_SIDECAR_DIR}/Teachers_Lounge/X.mp4.transcription

      Personal SDL: {PERSONAL_BRIDGE_DIR}
      Company SDL:  {COMPANY_BRIDGE_DIR}

  * Legacy fallback: older files may still sit under a .lfbridge/_Mirror/ path
    until Large File Bridge migrates them. Check that location before concluding
    a sidecar does not exist.

Do not infer this mapping. Verify it in Stage 1 against real files on disk.

=== THE AUDIO SIBLING RULE ===

Many videos in this corpus have an .mp3 audio extraction beside them, and Large
File Bridge transcribed the .mp3 rather than (or as well as) the .mp4. 30 of the
74 transcriptions in {REPO_VIDEO_SIDECAR_DIR} are .mp3.transcription files.

For a video entry, resolve transcription_file in this order:

  1. <base>.mp4.transcription   — the video's own transcription. Preferred.
  2. <base>.mp3.transcription   — the audio sibling's transcription. SAME
                                  CONTENT, same speech, same duration. It is a
                                  legitimate transcription of that video and it
                                  must be used.
  3. ""                         — genuinely absent. Report it.

When the value comes from the .mp3 sibling, record that fact:

    transcription_file: "~/BGit/.../.lfbridge/videos/2069185145555255370.mp3.transcription"
    transcription_source: "audio_sibling"

For the 7 basenames whose .mp4 is gone entirely, the .mp3 and its transcription
are ALL that survive locally — but the manifest still holds the CID, so the
video is still playable from IPFS and still belongs in the hierarchy. Set
file_path to the .mp3 path, media_present to "audio_only", and keep the CID.
Never drop one of these because the .mp4 is missing.

Also record audio_file (the path to the .mp3 sibling, or "") on every entry.
It is the cheap input for any future re-transcription.

=== INSIDE A .transcription FILE — exact format ===

Plain text. A five-line header, a divider line of 60 equals signs, a blank line,
then the transcript BODY AS ONE SINGLE VERY LONG LINE (a 4-minute transcript is
6 lines total in the file — the body is not wrapped and carries no timestamps).

    Transcription of: 2067372027623715212.mp4
    Generated on: 2026-07-14 13:18:36
    Engine: apple-speechanalyzer (device: on-device, language: en)
    Source duration: 00:04:19   ·   Transcript covers: 00:04:19  ✓ full
    ============================================================

    And when you run this theory that Charlie's microphone was rigged, ...

Parse it as:

  line 1  "Transcription of: "   → the source media filename. Use it to confirm
                                   you paired the right sidecar to the right
                                   media file. A mismatch is a bug — report it,
                                   do not silently accept.
  line 2  "Generated on: "       → transcription_generated (YYYY-MM-DD HH:MM:SS)
  line 3  "Engine: "             → transcription_engine, e.g.
                                   "apple-speechanalyzer (device: on-device,
                                   language: en)"
  line 4  two fields separated by U+00B7 MIDDLE DOT surrounded by spaces:
            "Source duration: HH:MM:SS"   → duration
            "Transcript covers: HH:MM:SS" → transcript_covers
          and a trailing marker, "✓ full" when the transcript reaches the end of
          the media. Anything other than "✓ full" (a partial marker, or the
          marker absent) means the ASR stopped early and the transcript is
          INCOMPLETE → set transcript_complete: false and report it. A partial
          transcript that is treated as complete produces a page that confidently
          describes a video it only heard half of.
  line 5  the ==== divider. Everything after it, trimmed, is the body.

DURATION IS ONLY AVAILABLE HERE. There is no duration in the manifest and none
in videos.md. The transcription header is the only place the corpus records how
long a video is, and duration drives real decisions: how many videos a page can
carry, whether a 173MB file is worth embedding from a public gateway at all,
and what the write-up promises the visitor. Harvest it.

The body carries no timestamps. Do not fabricate any. When the page needs "who
says what at roughly what time", the timing comes from the ai_description's
shot list — see the pairing rule below.

=== INSIDE AN .ai_description FILE — exact format ===

A self-contained YAML document. Seven top-level keys, and all 44 files have all
seven:

    source: videos/2067372027623715212.mp4
    status: done
    engine: gemini-flash-latest
    provider: gemini
    generated: 2026-07-14T16:50:03.564Z
    kind: video
    description: >-
      ## Overview
      ...

Parse the scalars into:

  source     → cross-check against the media file, same as line 1 of the
               transcription. Note it is REPO-RELATIVE ("videos/X.mp4"), not
               tilde-rooted.
  status     → only "done" carries usable content. Any other status means the
               description is absent or failed; treat the sidecar as missing
               content while still recording its path.
  engine     → ai_description_engine
  provider   → ai_description_provider
  generated  → ai_description_generated (ISO 8601)
  kind       → "video" here. A sidecar with kind "image" under videos/ is
               misfiled — report it.

`description` is a YAML folded block containing MARKDOWN with twelve sections.
All 44 files carry all twelve, in this order:

    ## Overview                  2-5 sentences. What the video IS. This is the
                                 field that becomes the inline ai_description.
    ## Hyper-Detail              a dense paragraph of everything in frame
    ## Shot-by-shot / Timeline   A TIMESTAMPED SHOT LIST — bullets of the form
                                 "* **00:39 - 00:55** | Split-screen. Candace on
                                 left; screenshot of a National Library of
                                 Medicine page on right. Static."
                                 THIS IS THE MOST VALUABLE SECTION IN THE WHOLE
                                 CORPUS. It is the only structured timing data
                                 that exists.
    ## People                    who is in frame, head to toe
    ## Setting & Place           indoor/outdoor, venue type
    ## Location                  best-guess city / country
    ## Composition               framing
    ## Cinematography            shot classification
    ## Lighting
    ## Colors & Mood
    ## Objects, Text & Brands    on-screen text a vision model could read —
                                 overlaps .ocr but is not a substitute for it
    ## Audio & Speech            what the model heard, in summary — NOT a
                                 transcript, do not use it as one

Extract at minimum:

  ai_description        the ## Overview section, collapsed to a single
                        paragraph: join its lines with single spaces, collapse
                        runs of whitespace, strip the "## Overview" header
                        itself. This mirrors the readDesc() convention in
                        {IMAGE_GENERATOR_DIR}/gen_hierarchy.js — read it and
                        reuse the same collapsing, so the two pipelines produce
                        comparable prose.
  shot_timeline         the ## Shot-by-shot / Timeline section, verbatim, as a
                        block scalar. Keep the timestamps. This is what lets a
                        later prompt write "at 1:20 an interview insert of Dan
                        Merrill appears" without watching the video.
  people_seen           the ## People section, collapsed. Feeds the defamation
                        review — you cannot apply the named-living-person rules
                        to a page if you do not know who is on screen.
  onscreen_text         the ## Objects, Text & Brands section, collapsed.

Keep the full sidecar on disk and keep ai_description_file pointing at it. The
YAML carries the extracted, useful subset; the sidecar remains the source.

=== INSIDE AN .ocr FILE ===

Only two exist today (2079054276320440416.mp4.ocr, 2079275082648809861.mp4.ocr).
Read both in Stage 1 and record the actual format observed rather than assuming
one. Set ocr_file on those two entries and "" everywhere else. If the format
turns out to carry a header like the transcription's, parse the same fields;
if it is bare text, take it as bare text. Report what you found in
{FINDINGS_FILE} so the next run does not have to re-discover it.

=== THE PAIRING RULE — why both sidecars are needed ===

The transcription has the WORDS but no timing. The ai_description has the TIMING
but only a summary of the speech. Neither alone answers the question the charter
says every video page must answer: who is speaking, what they assert, at roughly
what timestamp, and what is actually SHOWN versus merely NARRATED.

So on every entry, keep both, and keep them distinguishable. A recurring and
important finding in this corpus is that a video is filed under the thesis it
ARGUES while its own footage shows something much narrower — a host at a desk
talking over slides. The transcription is the claim; the shot list is the
evidence; the gap between them is often the story. Record both so the page can
say so honestly.

============================
KNOWLEDGE — THE VIDEO ENTRY SCHEMA (EXPANDED FOR VIDEO)
============================

The inherited schema came from images and is missing everything that makes a
video a video. This is the schema to emit. Every key appears on every entry.
Empty scalars emit "" (never null, never omitted); empty lists emit []; booleans
emit true/false.

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

FIELD NOTES — what each new field is for and where it comes from.

  title                  A short human title for this one video. Becomes the
                         Level 5 page title and the link text in every table of
                         contents above it. Compose it from the manifest
                         description and the ## Overview; keep it under about
                         nine words; name the speaker when there is one. Never
                         put an accusation in a title (see the defamation rule).
  media_present          "video"      the .mp4 is on this machine
                         "audio_only" only the .mp3 survives locally
                         "none"       neither; known from the manifest or from a
                                      site embed only
                         This is what lets a fresh clone — where the .gitignore
                         means NO media is present — behave correctly instead of
                         concluding the corpus is empty.
  file_size_bytes        From stat, when the file is present. It matters: this
                         corpus runs from 0.5MB to 173MB and a public IPFS
                         gateway serving a 173MB file to a cold visitor is a
                         different proposition from serving 3MB. The page
                         generator needs this to decide what to warn about.
  duration               From the transcription header. See above.
  audio_file             The .mp3 sibling, or "".
  transcription_source   "video" | "audio_sibling" | "" — provenance of the
                         transcription, per THE AUDIO SIBLING RULE.
  transcript_complete    false whenever the header's "✓ full" marker is absent.
  shot_timeline          Block scalar, timestamps preserved.
  banned                 Boolean, always present, default false. true means this
                         video must never be published: no Level 5 page, no
                         poster, no placement on any other page, no pin. Its
                         value is NOT reasoned out here — it is COPIED DOWN from
                         {BAN_VIDEOS_CSV} by Stage 6B, which is the only stage
                         allowed to write it. See the BANNED knowledge section.
  people_seen            Feeds the defamation review.
  onscreen_text          From the vision model; complements .ocr, replaces
                         nothing.
  source_url             From {VIDEO_MANIFEST}. The provenance of a video is
  source_author          part of the evidence — "who posted this and when" is a
  added_date             question every visitor asks and the manifest already
  manifest_description   answers it. The images pipeline had no equivalent and
                         losing it would be a real regression.
  source_platform        "x" | "youtube" | "rumble" | "ipfs" | "local" | ""
  cid                    The IPFS CID, CIDv0 "Qm..." form. Spoken as "SID"; it
                         means the CID. For video this is the PRIMARY IDENTITY,
                         because the site plays video from public gateways and
                         never from a copy in the repo. Many entries will have a
                         cid and an empty sha256 — that is normal and correct
                         when the bytes are not on this machine.
  sha256                 Content identity of the local file when there is one.
  video_page             Full path from ~ to the Level 5 page that hosts this
                         one video under {VIDEOS_L2_DIR}. "" until Stage 12
                         binds it. Never a path under {DOCS_DIR}/Photos.
  on_pages               Every OTHER page in the repo that embeds this video
                         TODAY. OBSERVED — read off the pages by Stage 11.
  should_be_on_pages     Every page in the repo this video OUGHT to appear on —
                         the planned end state. REASONED, not observed, by
                         Stage 13. Same shape as on_pages (a list of single-key
                         `page:` mappings holding a full tilde-rooted path), and
                         it is a SUPERSET of on_pages, never "extra pages beyond
                         on_pages". Empty emits []. The set difference
                         should_be_on_pages minus on_pages is exactly the
                         publishing worklist {THIS_DIR}/p_yaml_to_site.md
                         consumes in its Stage 6.

RETAINED FROM THE OLD SCHEMA: ipfs_url (optional, on entries harvested from a
site embed with no local file) and also_filed_in (optional; other concept nodes
the same content legitimately lives in — cross-filing is deliberate and kept).

CLUSTER NODE FIELDS are unchanged from the charter, plus one addition:

  title, _key, site_level_2, site_page, number_of_videos,
  number_of_videos_recursive, needs_split, videos, and the child level_N array.

  publishable           NEW. true when this node's subtree contains at least one
                        NOT-BANNED video, false when it does not. See the EMPTY
                        NODE PROBLEM below. The page generator publishes only
                        publishable nodes. A node whose every video is banned is
                        publishable: false — otherwise the generator writes a
                        cluster page with no players on it.

============================
KNOWLEDGE — THE BANNED PROPERTY (COPIED DOWN FROM {BAN_VIDEOS_CSV})
============================

Every video entry carries `banned:`. It is a real boolean, always present, never
null, never a missing key — same rule as every other field. The default is
false. An entry is banned: true only because a row for it exists in the ban CSV.

WHAT BANNED MEANS. Banned is a PUBLISH-TIME GATE, not a delete. A banned video:

  * Gets NO Level 5 page under {VIDEOS_L2_DIR}. If one already exists it is
    deleted by {THIS_DIR}/p_yaml_to_site.md — not by this prompt, which never
    touches a page.
  * Gets NO poster frame under {SITE_DIR}/static/img/video_posters.
  * Is NEVER placed on any other page anywhere on the site. No topic page, no
    cluster page, no table of contents, no card, no link. Nothing links INTO it,
    because there is nothing to link into.
  * Is NEVER pinned. Any pinning job filters banned entries out before it runs.
    IPFS publication is not reversible in practice — a CID that has been
    announced and fetched can be served by anyone who cached it — so the gate
    has to hold BEFORE the pin, not after.
  * Keeps its entry in {HIERARCHY_FILE} forever. This file is the complete
    private record and it only grows. Banning changes what is published; it
    never changes what is known.

WHERE THE DECISION LIVES. {BAN_VIDEOS_CSV} is the MASTER. The repo charter
({ROOT_DIR}/claude.md, "Banned Media") owns the contract. The YAML property is
DOWNSTREAM — it exists so the rest of the pipeline can read the decision out of
the data it already has, but it is a copy and never the source:

    ban_videos.csv  ──▶  videos.yaml (banned:)  ──▶  site/docs/Videos/ pages

Edits go in the CSV. Never hand-edit `banned:` in the YAML — the next run of
this prompt overwrites it. Never treat the YAML as the place where the ban was
decided.

CSV FORMAT. Header row, then one row per item:

  sha256        sha256 hex digest of the media file. Primary identity for a
                local file — survives renames, moves, duplicate copies.
  cid           The IPFS CID ("Qm..." CIDv0) when one is assigned, else empty.
                For video this is frequently the ONLY identity present, because
                the bytes are gitignored and absent on this machine.
  file_path     Full path from ~. For humans reading the CSV and as a
                last-resort match key. Not authoritative — files move.
  banned        true or false. Normally true. A row set to false is an explicit
                UN-BAN: the row stays as the record of the decision and its
                reason, and the item publishes normally.
  reason        Short plain-text reason. Required.
  date_added    YYYY-MM-DD the row was added.

MATCH ORDER: sha256 first, then cid, then file_path. Any match sets the entry's
banned to that row's banned value. An entry matched by no row gets banned: false.

THE OLDER LIST. {EXCLUDE_FILE} is the previous one-identifier-per-line
never-publish list and it still counts. The BAN SET is the UNION of the two,
minus any CSV row explicitly marked banned=false. New bans go in the CSV; do not
empty {EXCLUDE_FILE} to "move" entries into the CSV, and do not delete lines
from it — leave them and add the row.

WHY VIDEO NEEDS THIS MORE THAN IMAGES DO. The images pipeline learned the gate
the hard way: its mirror is a years-long personal filing area, private material
was swept into it by accident, and eleven such entries were found published
during its first full run. Video carries the same risk in a sharper form:

  * Careful prose is NOT sufficient protection. A write-up can omit every name
    and the page is still an exposure, because the footage itself streams from a
    public URL. The media is the payload.
  * A still catches one instant; a clip catches every face that walks through
    frame for its whole duration, plus every voice.

WHEN A RUN FINDS SOMETHING THAT SHOULD NOT BE PUBLIC — private personal
documents, an unrelated third party's records, footage of bystanders with no
connection to the investigation, an unproven criminal accusation about a named
living person burned into the frames — add a row to {BAN_VIDEOS_CSV} with a
reason and the date BEFORE the run ends, and note it in {FINDINGS_FILE}. Do not
wait for a later pass. The next stage of this same run may otherwise plan it
onto a page.

============================
CONCERN — THE EMPTY NODE PROBLEM (READ BEFORE STAGES 7-9)
============================

Stages 7, 8, and 9 mirror the site's structure into the YAML with every level
number incremented by one: site Level 2 → YAML level_3, site Level 3 → YAML
level_4, site Level 4 → YAML level_5. That is the design and this prompt
implements it in full.

State the arithmetic plainly, because it changes what the later prompts must do:
the site has about 70 Level 2 directories and 364 pages, and this corpus has
roughly 55-65 videos. Mirroring the whole site produces several hundred cluster
nodes, and the overwhelming majority of them will contain zero videos. If the
page generator publishes a page per node, the site gains hundreds of empty
"Videos → FBI → Search Warrants" pages that say nothing, dilute the section, and
give a visitor arriving from Path 2 (topic arrival, per the charter's audience
model) a dead end where they expected footage.

The fix is a gate, not a smaller hierarchy:

  * Build the full mirrored tree. It is genuinely useful as a plan — it shows
    exactly which parts of the investigation have NO video coverage, and that
    gap list is itself a research output. Write it to {FINDINGS_FILE}.
  * Set publishable: false on every node whose number_of_videos_recursive is 0.
  * State in the YAML header comment that publishable: false nodes must not
    generate a page. {THIS_DIR}/p_yaml_to_site.md and
    {THIS_DIR}/p_level2_update.md are the prompts that must honour it; note the
    requirement in {FINDINGS_FILE} so they pick it up.
  * Report the counts both ways: total nodes, and publishable nodes.

Nothing is dropped. The plan stays complete; only publication is gated.

============================
KNOWLEDGE — THE TWO LEVEL SYSTEMS
============================

Do not confuse them.

The SITE (filesystem) levels:
  * Level 1 — the site home page ({HOME_PAGE}).
  * Level 2 — the top-level sections: directories directly under {DOCS_DIR}.
    Examples: TPUSA, FBI, UVU, Israel, Mic, Planes, Timeline. Videos and Photos
    are also Level 2s.
  * Level 3 — pages inside a Level 2 directory (overview.mdx, the individual
    analysis pages, and first-level subdirectory overviews).
  * Level 4 — pages one directory deeper.

The YAML ({HIERARCHY_FILE}) levels:
  * There is no level_1 and no level_2 in the file. Level 1 is the site home and
    Level 2 is the videos landing page itself, so the YAML's cluster tree begins
    at level_3. The entire YAML hangs under the videos Level 2 page.
  * `level_3:` is a tree and an array; each array item is itself keyed
    `level_3:`. A level_3 may contain a `level_4:` array; a level_4 may contain
    a `level_5:` array. Same shape at every depth.

THE CORE MAPPING RULE — increment by one:

    site filesystem Level 2  →  YAML level_3
    site filesystem Level 3  →  YAML level_4
    site filesystem Level 4  →  YAML level_5

The YAML's level_3 list is a SUPERSET that includes the site's Level 2s (minus
the exclusions in Stage 7). Corpus-derived clusters that came from the videos
themselves also live at level_3 and level_4; the site-derived nodes MERGE into
that tree rather than replacing it.

Site Level 2 snapshot (enumerate live at run time; this is what to expect):

  After, analysis_documentation, Before, cameras, campus_university,
  Cause_of_Death, Censorship, Charlie, Companies_Organizations, court, CoverUp,
  Defamation, distraction_people, Drones, Electrocution, FBI, Fix,
  GoogleSearches, gov, Gov_Mind_Control, government_organizations, Gun_Bullet,
  Influencers, intelligence, Iran, Israel, Israel_Main_Suspect, key_individuals,
  Killer, Law_Enforcement, laws, Legal, legal_investigation, Locations, maps,
  Media, Medical, Mic, Motive, Narrative, organizations_groups, Other,
  other_topics, People, Photos, Planes, political_context,
  Proof_Intel_Services, Proof_Not_Tyler, security_law_enforcement,
  Security_Team, social_media_analysis, Suspects, Suspicious,
  technology_surveillance, Tent, Theories, Timeline, Topic-Analyses, Topics3,
  TPUSA, Tyler_Robinson, Tyler_Robinson_Not_Assassin, US_Intelligence,
  US_Intelligence_Assisted, UVU, Videos, Vote, Witnesses, Your_Actions_Fix_It

Cluster sizing rules (from {CHARTER_FILE}):
  * Six videos per page is the target. Twelve is the ceiling. Over twelve means
    the node is not one concept — set needs_split: true and split one level
    deeper on a later pass. A page carrying many IPFS video embeds is heavy;
    prefer the low end and split earlier than the image hierarchy would.
  * Clusters are CONCEPT clusters. The question is always "what does this
    footage show or claim", never "when was it downloaded" or "who posted it".
  * Titles may use spaces and full words. _keys use underscores, four words or
    less, and are unique across the WHOLE file — they are the future page_keys
    in {PAGES_CSV}, so treat them like database primary keys.

============================
STAGE 1 — READ, VERIFY THE MAPPING, PREPARE
============================

* Read {CHARTER_FILE} — the videos_planning charter. It is the authority on the
  audience model, the level model, the schema, and the hard rules.
* Read {ASSESS_MANUAL} — the writing and layout guide. This prompt writes no
  pages, but the fields it harvests are what the pages are written from, so know
  what they will be used for.
* Read these Large File Bridge specs in {LFB_PM_DIR} (the frontmatter
  description paragraph plus the placement sections are enough):
    artifact_placement_policy.mdx   section 0 — the owner of the placement rule
    Transcribe.mdx                  the .transcription feature
    ai_description.mdx              the .ai_description feature, and section 0's
                                    symmetry contract with Transcribe
    ocr.mdx                         the .ocr feature
    repo_tracking_scheme.mdx        how a repo's tracking area is resolved
  These specs are the reason the mapping in this prompt is what it is. If a spec
  and this prompt disagree, the spec wins and this prompt gets corrected.
* VERIFY THE MAPPING AGAINST DISK, do not assume it:
    * Pick 5 .mp4 files under {VIDEOS_DIR}, compute their expected sidecar paths
      under {REPO_VIDEO_SIDECAR_DIR}, and confirm existence.
    * Do the same for "Blake Bednarz UVU original.MP4" under {IPFS_VIDEOS_DIR}
      against {REPO_IPFS_SIDECAR_DIR} — this is the case-and-spaces test.
    * Do the same for one video under {MIRROR_DIR} against {MIRROR_SIDECAR_DIR},
      confirming there is NO .lfbridge segment in that path.
    * If a sample misses, check the legacy .lfbridge/_Mirror/ location before
      concluding the sidecar does not exist.
* Read both .ocr files end to end and record their actual format.
* Read {VIDEO_MANIFEST}, {VIDEO_INDEX_MD}, {IPFS_DIR}/ipfs.txt, {VIDEO_LIST_CSV}.
* Read {HIERARCHY_FILE}'s TREE SHAPE ONLY — the cluster titles and _keys. Do not
  read its 1,740 entries; they are image data and reading them wastes context.
  `grep -n '_key:\|title:' {HIERARCHY_FILE}` is enough.
* Read {PAGES_CSV}.
* Read the prior art in {IMAGE_GENERATOR_DIR} — gen_hierarchy.js (its readDesc()
  collapsing convention and its unique-_key minting), bind_image_pages.py (its
  emit_node/recount round-trip, which rewrites a large YAML byte-for-byte except
  where a value actually changed), and sanitize_common.py (the invisible-Unicode
  scrubbing). Read only. NEVER edit anything under {IMAGE_PLANNING_DIR}, and
  never copy a file from there into {THIS_DIR} — every file here is a converted
  descendant of one and a re-copy silently reverts the conversion.
* Create {GENERATOR_DIR} if it does not exist. This run's scripts live there.
* Create {EXCLUDE_FILE} if it does not exist, with a header comment explaining
  that it lists — one per line, by cid or sha256 — video that must never be
  published or pinned. Seed it empty. Nothing in this run publishes or pins, but
  later prompts read it and it must exist.
* Create {BAN_VIDEOS_CSV} if it does not exist, with the header row
  sha256,cid,file_path,banned,reason,date_added and no data rows. This is the
  MASTER record of what must never be published — Stage 6B copies it down onto
  every entry as `banned:`. Read it now and report the row count, so a run that
  is about to plan hundreds of placements knows up front what is off limits.
* Reference {CK_FILE} throughout. It is the source of truth for what the
  investigation's concepts actually are, and the hierarchy must mirror the
  investigation's real concept structure rather than an arbitrary video-library
  structure. Do not read all 400K+ lines up front — consult sections when a
  clustering decision needs arbitration.

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

Build one flat index of every video this investigation holds, from every source,
before touching the YAML. Write it to {INVENTORY_TSV} so the run is inspectable
and resumable.

SOURCES, in order of authority:

  1. {VIDEOS_DIR} on disk — walk it for .mp4 .mov .m4v .mkv .avi .webm. Record
     filename, absolute path, size, mtime. Also record every .mp3 as a potential
     audio sibling, keyed by basename.
  2. {VIDEO_MANIFEST} — 63 records with filename, ipfs_cid, ipfs_gateway_url,
     source_url, source_author, description, added_date, pinned. This is the
     richest machine-readable source and it seeds cid, provenance, and pin
     status in one read. It is AUTHORITATIVE for CIDs of X-sourced video.
  3. {IPFS_DIR}/ipfs.txt plus {IPFS_VIDEOS_DIR} — the larger forensic originals
     and their CIDs.
  4. {REPO_VIDEO_SIDECAR_DIR} and {REPO_IPFS_SIDECAR_DIR} — every sidecar whose
     base filename ends in a video OR audio extension. A SIDECAR PROVES A VIDEO
     EXISTED even when the media file is gitignored, deleted, or moved. This is
     how the 7 audio-only survivors are found.
  5. {MIRROR_DIR} — walk for video extensions; pair against {MIRROR_SIDECAR_DIR}.
  6. {VIDEO_LIST_CSV} — 12 rows of YouTube links and IPFS CIDs. YouTube-only
     rows have no CID and no local file; carry them with cid "",
     source_platform "youtube", and the watch URL in source_url. Never invent a
     CID for one.

RECONCILE INTO ONE ROW PER VIDEO, keyed by basename (the X status id, or the
filename stem for non-X material). Each row records:

  basename, media_path, media_present, size, audio_path,
  transcription_path, transcription_source, ai_description_path, ocr_path,
  manifest_cid, manifest_pinned, source_url, source_author, added_date,
  manifest_description, origin (videos_dir | ipfs_dir | mirror | manifest_only |
  video_list_csv | site_embed)

HANDLE THE KNOWN DISCREPANCIES EXPLICITLY — they are not errors:

  * 18 manifest records name an .mp4 that is not on disk. For each, check for
    an .mp3 sibling and for sidecars. If either exists, media_present is
    "audio_only"; if neither, "none". Keep the row either way — the CID makes
    it playable.
  * _QwGo0LyZ3I.mp4 is on disk with no manifest record. Create a row,
    origin "videos_dir", manifest fields empty, and let Stage 4 compute its CID.
    Its filename is a YouTube video id — record source_platform "youtube" and
    note that the source URL is unknown rather than guessing one.
  * 2079560806690324910.mp4 and 2079684519762993659.mp4 have no transcription
    and no audio sibling. Keep them. They get entries with empty sidecar fields
    and they head the transcription work list.
  * Do NOT create a row for an .mp3 that has a .mp4 sibling — that is one video,
    not two. Only an .mp3 with no video sibling anywhere becomes its own row.

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

For every row in the corpus index, resolve and PARSE all three sidecars. Write
the parsed result to {SIDECAR_INDEX} as JSON keyed by basename, so Stage 6 emits
from data rather than re-reading files.

RESOLVE THE PATHS using the placement rule and the audio sibling rule:

  transcription_file   <base>.<videoext>.transcription, else
                       <base>.mp3.transcription (set transcription_source
                       "audio_sibling"), else ""
  ai_description_file  <base>.<videoext>.ai_description, else ""
  ocr_file             <base>.<videoext>.ocr, else ""

  Preserve case exactly. Quote every path. Check the legacy .lfbridge/_Mirror/
  location as a fallback for mirror-side originals.

PARSE EVERY TRANSCRIPTION → transcription_engine, transcription_generated,
duration, transcript_covers, transcript_complete, and the body. Confirm line 1's
"Transcription of:" filename matches the media file you paired it to; a mismatch
is a pairing bug and gets reported, not accepted.

PARSE EVERY AI_DESCRIPTION → the seven scalars, then split the `description`
folded block on its `## ` headers and extract ai_description (from ## Overview,
collapsed), shot_timeline (## Shot-by-shot / Timeline, verbatim), people_seen
(## People, collapsed), onscreen_text (## Objects, Text & Brands, collapsed).
Only status "done" yields content.

PARSE EVERY OCR per the format recorded in Stage 1.

REPORT THE COVERAGE GAPS. These are the work list for the next Large File Bridge
run and they are a deliverable of this prompt, not an afterthought:

  * videos with no transcription of any kind (expected: 2)
  * videos whose transcription came from the audio sibling (expected: ~7 where
    it is the only source, more where it is a duplicate of the video's own)
  * videos with transcript_complete false — partial ASR, the dangerous ones
  * videos with no ai_description (expected: 2 of the 46 on disk)
  * videos with a sidecar whose "Transcription of:" or "source:" line does not
    match the media file it was paired to

Write the gap lists to {FINDINGS_FILE} as well as stdout. That file is where a
human picks up the work.

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

This stage runs before any page work on purpose. Site pages embed video almost
exclusively as an IPFS gateway URL, so the on_pages sweep in Stage 11 has to
recognise a video BY ITS CID, and the page generator needs the CID to build a
player at all. Populate the CID column first or every embed on the site is
unmatchable.

For video the CID is not merely an identifier — it is the DELIVERY MECHANISM. An
image can fall back to a static copy in the repo; a video cannot, because the
bytes are gitignored and GitHub Pages is not a video host. No CID means no
playable page.

HOW A CID IS OBTAINED. A CID is a content address COMPUTED from the file's
bytes. It needs no network, no daemon, and no prior publication. Every video
with a local file can always get one:

    ipfs add -n -Q "<file>"       # -n/--only-hash: compute, do not store
                                  # -Q/--quiet: print just the CID

USE THE DEFAULT CID VERSION — CIDv0, the base58 "Qm..." form. That is what
{VIDEO_MANIFEST} records, what {IPFS_DIR}/ipfs.txt pins, and what the site
already embeds. `--cid-version=1` produces a DIFFERENT string (bafy.../bafk...)
for the same bytes because v1 also switches the leaf codec; it would match no
URL on the site and Stage 11 would resolve nothing. If a v1 form is needed for a
dweb.link subdomain URL, convert at use time with `ipfs cid base32 <cid>` — do
not store it. Chunking settings change the CID, so use identical flags on every
run, always.

PINNING IS A SEPARATE QUESTION from having a CID. Pinned means the local node
holds the blocks and rebroadcasts them so a public gateway can serve the file.

    ipfs pin ls --type=all <cid>   # prints the cid and "recursive" when pinned
    ipfs block stat <cid>          # blocks present locally

WHAT TO DO:

* Seed from {VIDEO_MANIFEST} first — its ipfs_cid and pinned fields are
  authoritative for the X-sourced corpus. Then seed from {IPFS_DIR}/ipfs.txt for
  the forensic originals.
* For every row with a local file and no CID yet, compute it with the flags
  above and write it. Unconditional: a readable file always yields a CID, so a
  row with a readable media_path must never end this stage with cid "".
* For every CID, ask the local node for pin status and record ipfs_pinned
  true/false.
* For rows with no local file, take the CID from the manifest or parse it out of
  the gateway URL. Ask the node for pin status; if the node does not have it,
  false.
* For rows with neither a file nor a manifest CID, leave cid "" and report the
  row. NEVER invent a CID.
* Where a recorded CID and a recomputed CID disagree, the file's bytes changed.
  Report the mismatch, keep the recomputed value, and note the old one. Never
  overwrite a non-empty cid with "".
* Build a CID → row index in memory and hold it for Stage 11, which must resolve
  an IPFS URL found on a page back to the video it belongs to. Index both the v0
  and the base32 v1 form of each CID so a page carrying either form matches.

DO NOT PIN ANYTHING. Pinning publishes content to the public IPFS network and is
irreversible in practice — an announced CID can be fetched and cached by anyone.
Some material in this corpus must never be published (that is what {EXCLUDE_FILE}
is for). This stage RECORDS state; it does not change what is public. Pinning the
publishable set is a separate, explicitly-approved job that must first filter out
every entry in {EXCLUDE_FILE}.

Report the unpinned set prominently. Every unpinned CID is a video page that
renders a dead player for visitors even though it plays perfectly on this
machine — the local IPFS node and any IPFS Companion browser extension will
silently make it look fine here.

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

Now decide where each video belongs. This is the judgment stage and the
sidecars are what make it possible.

The method, in priority order:

  1. Read {CK_FILE} for the investigation's real concepts, clusters, and open
     questions. The hierarchy mirrors the investigation, not a video library.
  2. Read each video's TRANSCRIPTION. What the speaker CLAIMS usually decides
     the cluster. This is the deciding input.
  3. Read each video's ## Overview and ## Shot-by-shot. What is actually SHOWN
     often differs from what is claimed — a video is frequently filed under the
     thesis it argues while its footage shows a host at a desk. Note the gap on
     the entry; a later prompt must say so on the page.
  4. Read the manifest description and, for mirror-side video, the directory it
     was filed in. Both carry filing intent and usually name the cluster. Treat
     __TO_FILE, backup, Old, Organized, TO_TRANSCRIBE, and Other as work queues,
     not concepts — their contents cluster by transcription and description.
  5. Cluster. The folder proposes, the transcription decides, {CK_FILE}
     arbitrates.
  6. Enforce six-to-twelve. Over twelve direct videos means split one level
     deeper.

Reuse the old file's tree shape as a PROPOSAL where it fits the real corpus, and
discard it where it does not. Its cluster names came from the image corpus's
concepts, which overlap the video corpus's concepts but are not identical.

Mint _keys: underscores, four words or less, unique across the whole file. Where
a cluster corresponds to a site section, prefer that section's page_key from
{PAGES_CSV} when it is free — it makes Stage 9's merge trivial.

Cross-filing: when one video legitimately belongs under two concepts, file it in
both and record also_filed_in on each copy. Same cid under DIFFERENT nodes is
legitimate; same cid TWICE under ONE node is a bug.

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

MODE DETECTION. Decide which mode this run is in before writing anything:

  REBUILD MODE — the file's entries are the inherited image corpus. Detect it:
    more than 100 entries whose file_path ends .jpg/.jpeg/.png/.gif/.webp, or
    more than 100 ai_description values beginning "This image". In rebuild mode,
    the old entries and the old counts are DISCARDED and the file is written
    fresh from Stages 2-5. This is expected to happen exactly once.

  UPDATE MODE — the file already holds real video data. Detect it: the entries'
    file_paths are video files and their cids match the corpus index. In update
    mode the file ONLY GROWS: existing entries are matched by cid (then sha256,
    then file_path) and their properties are updated IN PLACE; new videos are
    added; nothing is deleted; no duplicate is ever created.

  Print which mode was chosen and the evidence for it, and if the evidence is
  ambiguous, STOP and report rather than guessing. Guessing wrong in one
  direction discards good data.

BEFORE WRITING IN REBUILD MODE: copy the current file to
{GENERATOR_DIR}/videos.yaml.pre_rebuild.bak. It is a 2.6MB file that is tracked
in git, so the git history is the real safety net, but a local copy makes the
diff reviewable without git gymnastics.

WRITE THE FILE:

* Emit the header comment block. It must state: what the file is, that it is the
  MASTER DATA for video, when it was rebuilt and from what, the meaning of
  publishable, the meaning of media_present and transcription_source, that a
  value with nothing in it is "" and never null, and that cid is the primary
  identity for video because the site plays from public gateways.
* Emit the tree from Stage 5 with the full expanded schema from the KNOWLEDGE
  section above. Every video entry carries every key.
* Emit deterministically — stable key order, stable node order, stable video
  order within a node (by cid, or by basename when cid is empty). A rerun that
  changes nothing must produce a byte-identical file. Reuse the emit_node
  approach from {IMAGE_GENERATOR_DIR}/bind_image_pages.py, which round-trips a
  large YAML byte-for-byte.
* Use block scalars (`|`) for shot_timeline. Use double-quoted scalars for every
  path and identity field. Escape internal quotes.
* Apply OUTPUT SANITIZATION (see the section below) on the way out, then
  validate the written file.
* Verify the file parses: `python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" {HIERARCHY_FILE}`

Do this with a script in {GENERATOR_DIR}, never by hand. Hand-editing a
30,000-line YAML is how silent corruption gets in.

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

Read the BANNED knowledge section before running this. This stage is the ONLY
place in the whole pipeline that writes `banned:`. It reasons about nothing. It
copies a decision that was already made in {BAN_VIDEOS_CSV} down onto the data,
so every later stage and every later prompt can see it.

Run it on every run, immediately after Stage 6, and re-run it any time the CSV
changes. It is cheap and it is idempotent.

STEP 1 — READ THE BAN SET.

  * Read {BAN_VIDEOS_CSV}. Parse it as a real CSV (python3 csv module — the
    reason column contains commas and quoted text). Expected header:
    sha256,cid,file_path,banned,reason,date_added
  * If the file does not exist, CREATE it with that header row and zero data
    rows, then continue. A missing CSV means "nothing is banned", not "skip the
    gate" — and the file needs to exist so the next person can add a row.
  * Parse the banned column strictly: "true" (any case) is true, "false" (any
    case) is false. Anything else is a malformed row — STOP and report it rather
    than guessing. Guessing "false" on a malformed row publishes banned footage.
  * Build three lookup dicts from the rows: by sha256, by cid, by expanded
    file_path (expand ~ on both sides before comparing).
  * Read {EXCLUDE_FILE} too. Every identifier in it (cid and/or sha256, one per
    line, "#" comments ignored) joins the ban set with banned=true, unless a CSV
    row for that same identity says banned=false — an explicit CSV un-ban wins,
    because it is the newer and more deliberate record.

STEP 2 — SET banned ON EVERY ENTRY.

  * Walk every video entry in {HIERARCHY_FILE}, at every depth.
  * Look the entry up in the ban set: sha256 first, then cid, then file_path.
    First match wins and supplies the value.
  * No match → banned: false.
  * Write the key on EVERY entry, including the false ones. Never omit it,
    never emit null. A missing key is indistinguishable from "not checked yet"
    and this is exactly the field where that ambiguity is dangerous.
  * Never delete an entry because it is banned. The file only grows.

STEP 3 — REPORT THE ROWS THAT MATCHED NOTHING.

  A CSV row that matches no entry is a real finding, not noise. It usually means
  one of three things and each needs a different fix:

    * The identity is stale (the file was re-encoded, so its sha256 moved).
    * The item is an image, filed in the wrong CSV — check {ROOT_DIR}/images/
      ban_images.csv and say so.
    * The item is genuinely not in this corpus yet, and the row is pre-emptive.
      That is legitimate. Keep the row.

  List every unmatched row with its reason text. Do not delete unmatched rows.

STEP 4 — RECOMPUTE publishable.

  A node's publishable is true when its subtree holds at least one NOT-BANNED
  video. Recompute it here rather than leaving Stage 14 to discover it, because
  a node whose entire contents just got banned must stop being publishable in
  the same run that banned them.

STEP 5 — RE-EMIT AND VALIDATE.

  Use the same deterministic emitter Stage 6 used, so a run that changes no
  banned value produces a byte-identical file. Verify the YAML parses. Apply
  OUTPUT SANITIZATION — the reason column is human-typed text and is a plausible
  carrier of invisible Unicode, so treat it as untrusted even though this stage
  does not copy the reason into the YAML.

DO NOT, IN THIS STAGE:

  * Do not delete, move, or edit any page. This prompt never touches a page.
    Page and poster deletion for a newly banned video is
    {THIS_DIR}/p_yaml_to_site.md's job.
  * Do not clear video_page, on_pages, or should_be_on_pages on a banned entry.
    on_pages is an OBSERVATION — "this video is on that page today" stays true
    and is exactly what tells the page prompt what to go delete. Stages 12 and
    13 handle the forward-looking fields.
  * Do not pin, unpin, or touch IPFS in any way.

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

The YAML's level_3 list must include every one of the website's Level 2
sections, except:

  * Videos — the videos Level 2 itself; this YAML IS its content.
  * Photos — the images pipeline's territory, a media Level 2 not a concept.
  * Topics3 — template scaffolding. The /Topics3/Videos page is unrelated to
    this hierarchy; do not confuse the two.
  * Unfiltered / queue / catch-all categories, EXCEPT that we keep exactly ONE
    "Other" level_3 as the catch-all. Fold other_topics-style catch-alls into
    that single node rather than creating several.
  * Non-page files at the docs root (index.mdx, Topics.mdx, image_list.csv,
    video_list.csv, index.html) — not sections.

For every remaining site Level 2:

* Check whether a YAML level_3 already covers that CONCEPT — match by _key, by
  title, and by meaning. Existing "TPUSA" covers site TPUSA; "The UVU Venue"
  covers site UVU; "Ballistics and the Gun" covers site Gun_Bullet; "Aircraft
  and Flight Evidence" covers site Planes; "CIA and US Intelligence" covers site
  intelligence and US_Intelligence; "Court and Legal Proceedings" covers site
  court, Legal, and legal_investigation. Do NOT create a duplicate concept under
  a second name.
* Record the mapping on the node: site_level_2 is a LIST of the site dirs that
  node covers; an empty list means the node is corpus-only.
* If no level_3 covers it, append one: title from the section's human-readable
  name, unique _key, number_of_videos 0, number_of_videos_recursive 0, videos
  [], site_level_2 [<dirname>], publishable false.
* Never remove or rename an existing level_3. Grow only; update in place.

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

{HOME_PAGE} is the site's Level 1 and it carries MORE THAN ONE table of
contents — the three-column flex divs under "Biggest Question Marks", the
"## Table of Contents" section, "## Areas of Investigation", the "Related Areas"
and "Related" sections, and the per-thesis link clusters (Tyler Robinson Not
Assassin, Cause of Death, Mossad / Israel Top Suspect, US Intelligence Assisted,
and others). These reflect how the investigation actually organizes itself and
they surface areas the directory sweep alone will miss.

* Read {HOME_PAGE} fully. Extract EVERY table of contents and EVERY link
  cluster — all of them, not just the first.
* Resolve each linked area to its site section and check whether a level_3
  already covers that concept.
* Add a level_3 for each one not covered, same rules and fields as Stage 7. No
  dupes — a concept already covered under any name is skipped, though you may
  improve that node's title or append to its site_level_2 when the TOC reveals a
  better human-readable name.
* This stage is EXPECTED to add nodes beyond the earlier stages. That is its
  purpose: the YAML must be the fullest and most complete hierarchy possible.

Output to stdout:
============================
STAGE 8 COMPLETE
TOC sections parsed on home page: N    Concepts found: N
Already covered: N    New level_3 nodes added: N (list _keys)
============================

============================
STAGE 9 — SITE LEVEL 3/4 PAGES → LEVEL_4/LEVEL_5 NODES
============================

Apply the increment-by-one mapping to the pages inside each site Level 2.

For every site Level 2 that maps to a YAML level_3 (via site_level_2):

* Enumerate its Level 3 pages: overview.mdx, every other page file directly in
  the directory, and first-level subdirectory overviews. Use {PAGES_CSV}'s level
  and parent_key columns as the guide and the filesystem as the check; when they
  disagree, the filesystem is what actually exists.
* For each site Level 3 page, ensure a level_4 node exists under the correct
  level_3 parent:
    title             the page's frontmatter title or first H1
    _key              unique file-wide, four words max; prefer the page's
                      page_key from {PAGES_CSV} when free
    site_page         repo-relative path of the page
    number_of_videos, number_of_videos_recursive, videos: [], publishable
* For each site Level 4 page, ensure a level_5 node under the correct level_4
  parent, same fields.
* MERGE, do not duplicate: where a site page and an existing corpus-derived node
  are the same concept, keep the existing node and add site_page to it.
* Skip a pure-navigation page only when adding it would create an empty
  duplicate of its parent. When in doubt, include it — the EMPTY NODE PROBLEM is
  handled by the publishable gate, not by omission.
* Never remove existing nodes or video entries.

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

Every page on the site that shows a video must have that video represented in
the YAML.

* Scan every page under {DOCS_DIR} and {SITE_DIR}/blog for embedded video:
  <video> src and poster attributes, <iframe src> embeds (YouTube, Rumble,
  Odysee, X), IPFS gateway URLs, markdown links to media files, and
  require()/import forms in JSX. Resolve each src to what it actually is.
* For each video found:
    * Take its CID from the URL when it is an IPFS embed — that is exact
      identity. Otherwise resolve to a local file and compute sha256. Match back
      to the corpus index by cid first, then sha256, then filename.
    * If that identity already exists in the YAML: do NOT add a duplicate.
      Update the existing entry in place and append the page to its on_pages.
    * If it does not exist: add a new entry under the level_4 (or level_5) node
      that correlates to the page it was found on — per the level model, a video
      found on a site Level 3 page parents onto the level_4 node that mirrors
      that page. Fill every schema key; Stage 3's harvest fills the sidecar
      fields if a sidecar exists for it, otherwise they are "".
* THIRD-PARTY HOSTED VIDEO (YouTube, Rumble, X) is recorded with cid "",
  source_platform set accordingly, and the watch URL in source_url. It is real
  evidence and it belongs in the hierarchy, but it cannot be served from IPFS
  and its page will carry an external embed rather than our player. Mark it so
  the page generator knows which kind it is. {VIDEO_LIST_CSV} is the starting
  index for these; the page scan is authoritative.
* Videos already embedded ad hoc inside topic pages STAY on those pages. This
  hierarchy is the browsable index over the corpus, not a relocation of every
  inline embed.

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

Two properties record two different relationships and must not be confused:

  video_page   "which page IS this video" — the ONE Level 5 page under
               {VIDEOS_L2_DIR} that exists to host this single video. Stage 12
               sets it. Exactly one, or "".
  on_pages     "where ELSE is this video shown" — every OTHER page anywhere in
               the repo that embeds it. Zero to many. Set here.

THE PROPERTY SHAPE — a list of mappings, each with a single `page:` key holding
the full path from ~, the same tilde-rooted convention every other path property
uses:

    on_pages:
      - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/Mic/overview.mdx"
      - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/Killer/israel-mossad.mdx"

Not a flat list of strings. Not repo-relative. Not URLs. A video shown on no
other page emits `on_pages: []`.

HOW TO FIND THE REFERENCES — one linear pass. This is a reverse index: for every
file in the repo, what videos does it show. Read each file exactly ONCE. O(n)
over the repo's text, not O(videos × pages).

* Enumerate every text file under {ROOT_DIR}: .md .mdx .html .tsx .jsx .ts .js
  .json .csv .yaml — skipping node_modules/, build/, .git/, .docusaurus/, and
  binary static assets.
* Extract every video reference from each file, in every form the site uses:
    - <video> src and poster attributes
    - <iframe src="..."> — YouTube, Rumble, Odysee, X
    - IPFS gateway URLs:  https://ipfs.io/ipfs/<CID>[/name]
                          https://<CID>.ipfs.dweb.link/[name]
                          ipfs://<CID>
    - markdown links to media files: [label](/videos/xxx.mp4)
    - require()/import forms in JSX
* Resolve each reference to a video entry, in this precedence order:
    1. IPFS CID → the Stage 4 index. EXACT. Normalise both sides first: a page
       may carry the base32 v1 form of a CID stored as v0. Compare against both
       forms.
    2. Third-party video id (YouTube watch id, Rumble slug) → the entry recorded
       in Stage 10. Exact.
    3. Local media file → sha256 → the entry's sha256. Exact.
    4. Filename basename against file_path basenames. AMBIGUOUS — this corpus
       names files by X status id, so a numeric basename mismatches easily.
       Accept only when it resolves to exactly ONE entry; otherwise report it
       unresolved.
* Append the referencing page's tilde-rooted path to that entry's on_pages.
  Deduplicate — a page embedding the same video twice is recorded once.

SCOPE RULE — what does NOT go in on_pages:

  * Pages under {VIDEOS_L2_DIR}. That is the videos Level 2 itself: the video's
    own page belongs in video_page, and a cluster overview listing its children
    is structure, not an outside reference.
  * Files in {THIS_DIR}, {GENERATOR_DIR}, {HIERARCHY_FILE} itself,
    {VIDEO_MANIFEST}, {VIDEO_INDEX_MD}, and {PAGES_CSV}. Those reference videos
    as data, not as a page showing them.
  * Anything outside {ROOT_DIR}.

INHERITED BINDINGS ARE GONE. In rebuild mode every on_pages list starts empty
because the file was rewritten, so there is nothing stale to clear. In update
mode, re-verify each existing binding against the page's actual current text and
drop any the sweep cannot confirm — report every drop.

PARALLELISM. Script the mechanical extraction; a script reads each file once and
is exact. Use parallel agents only for the RESIDUAL — references the script could
not resolve (ambiguous basenames, relative paths needing page context, videos
behind a component indirection, hand-written embeds with no recognisable asset
path).

  * Partition the repo's directories recursively across up to 12 agents. Map
    WHOLE directories to agents — never split a directory — so no file is read
    twice and none is missed. Balance by file count, not directory count.
  * Agents RETURN rows of (page_path, resolved_identity, evidence). Agents do
    NOT edit {HIERARCHY_FILE}. Concurrent writers to one YAML corrupt it. A
    single writer merges everything in one pass.

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

Under {VIDEOS_L2_DIR} the site publishes one page per video: the player, a
title, and prose describing what the footage shows, who is speaking, what they
claim, and why it matters. That is the VIDEO PAGE, the Level 5 page, the leaf of
the published hierarchy — the same way a video entry is the leaf of this YAML.

  Videos                            ← site Level 2 (the videos landing page)
    Mic_Thesis                      ← site Level 3 (a cluster overview page)
      Vid_Candace_Mic_2067372.mdx   ← the VIDEO PAGE

THESE PAGES DO NOT EXIST YET. {VIDEOS_L2_DIR} today holds overview.mdx,
_category_.json, and one hand-written topic page
(buckley-carlson-kash-patel-valhalla.mdx). They are generated by
{GENERATOR_DIR}/gen_videos_pages.py, driven by {THIS_DIR}/p_yaml_to_site.md and
{THIS_DIR}/p_level2_update.md. This stage does NOT create, rename, or edit them.
It READS whatever exists and records where each one is. On the first several runs
this stage correctly sets every video_page to "". Reading site pages is allowed;
the no-page-modification hard rule still holds.

THE PROPERTY — the full path from ~, not a URL and not repo-relative:

    video_page: "~/BGit/Bryan_git/charlie-kirk/site/docs/Videos/Mic_Thesis/Vid_Candace_Mic_2067372.mdx"

HOW TO MATCH. Each generated page carries the binding in its frontmatter:

    ck_video_cid: QmZdFUWDekCDBZcETphabnmTW4Y9vYk7EyPUJECsBXuDfo
    ck_video_sha256: 9044e164a9c6e76fbe9e1746d11bbc155b2fbfbbfc310b6631017c6e5998945d
    ck_node_key: Mic_Thesis

  * Walk every .mdx under {VIDEOS_L2_DIR}; index the ones declaring ck_video_cid
    or ck_video_sha256, keyed by (identity, ck_node_key).
  * CID IS THE PRIMARY KEY, not sha256. Many entries have a CID from the
    manifest and an empty sha256 because the media file is gitignored and absent.
    Match on cid first, fall back to sha256.
  * Look up (identity, the _key of the node the entry sits under). That pair is
    the exact match, and it is what makes cross-filing work — the same video
    legitimately appears under several nodes and each publishes its own page.
  * If the exact pair is not found, fall back to identity alone. Exactly one hit
    → use it. Several → choose the page whose ck_node_key is nearest in the tree
    (same parent first, then same level_3 subtree) and leave the others alone.
  * No page carries that identity → video_page: "".
  * Hand-written pages carry no ck_ frontmatter. Do not guess them by filename.
    Count them and report them; they resolve once the generator restamps them.

RULES:

  * video_page is set on EVERY entry. No entry is left without the key.
  * Never invent a path. Verify the file exists on disk before writing the value;
    write "" if it does not.
  * Never write a path outside {VIDEOS_L2_DIR}, and NEVER one under
    {DOCS_DIR}/Photos — that is the images pipeline's output and binding to it
    would cross the two hierarchies. Ad-hoc embeds elsewhere belong in on_pages.
  * Never replace an existing non-empty video_page with "". If a recorded page
    has vanished from disk, REPORT it rather than silently clearing it.
  * video_page is an IDENTITY field for sanitization — non-ASCII is emitted as a
    visible \uXXXX escape, never replaced.
  * A BANNED ENTRY GETS NO video_page. banned: true means there is no Level 5
    page for that video and there never will be while the ban stands, so the
    field is "". Two cases and they are handled differently:
      - No page exists → write "" and move on. Normal.
      - A page DOES exist on disk carrying that identity → this is a page that
        should not be there. Do NOT bind it, do NOT delete it (this prompt never
        touches a page). Write "" and REPORT it loudly, listing the page path and
        the ban reason, so {THIS_DIR}/p_yaml_to_site.md deletes it on its next
        run. Count these separately in the output — a non-zero number here means
        banned footage is live on the site right now.
    The "never replace a non-empty video_page with empty" rule above does not
    apply to a banned entry: clearing it is the correct action, not a regression.

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

KNOWLEDGE — what should_be_on_pages answers.

Stage 11 recorded where a video IS shown today. This stage records where it
SHOULD be shown — the plan. It is the one property in the whole file that is
REASONED rather than observed: nothing on disk tells you the answer. You work it
out from what the video SAYS, what it SHOWS, and what each page is about.

Why it exists: almost every video in this corpus is published nowhere but its
own Level 5 page under {VIDEOS_L2_DIR}. A reader deep in Ballistics, or on the
N1098L page, or on the exploding-mic thesis, should be offered the FOOTAGE for
that topic on the page they are reading rather than having to go find it. This
property is the worklist {THIS_DIR}/p_yaml_to_site.md Stage 6 consumes to put
each video onto its topic pages. This prompt only RECORDS the plan. It places
nothing, edits no page, and creates no page.

THE THREE PROPERTIES, AND HOW THEY DIFFER:

  video_page          "which page IS this video" — its own Level 5 page under
                      {VIDEOS_L2_DIR}. Exactly one, or "". Stage 12.
  on_pages            "where ELSE is it shown TODAY" — observed. Stage 11.
  should_be_on_pages  "where SHOULD it be shown" — reasoned. This stage.

THE UNION RULE:

    should_be_on_pages  is a superset of  on_pages

  Every page already in on_pages is repeated in should_be_on_pages unless the
  video genuinely does not belong there (a wrong placement made by an earlier
  pass — record every such subtraction with its reason). The set difference —
  should_be_on_pages minus on_pages — is exactly the work still to do. Never
  treat should_be_on_pages as "additional pages beyond on_pages"; it is the
  COMPLETE desired state.

  THIS UNION IS WHY STAGE 11 MUST RUN FIRST AND MUST BE CLEAN. The images
  pipeline learned this expensively: one of its on_pages runs carried 946
  fabricated bindings, 89% of its total. Unioning those in would have converted
  every fabricated observation into a fabricated publishing instruction, and the
  next prompt would have acted on it. Before unioning, confirm Stage 11 reported
  zero unresolved or unverified bindings. If Stage 11 did not run in this
  session, re-verify each on_pages entry by reopening the page rather than
  trusting the file.

THE PROPERTY SHAPE.

Identical in shape to on_pages: a LIST OF MAPPINGS, each with a single `page:`
key holding the full path from ~ to the page file.

    should_be_on_pages:
      - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/Suspicious/Cause_of_Death/entrance-or-exit.mdx"
      - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/Suspicious/Five_Minutes/shirt-pull-at-the-shot.mdx"

Not a flat list of strings. Not repo-relative. Not URLs. Not a video-page path.
Every video entry carries the key; a video that belongs on no topic page emits:

    should_be_on_pages: []

BANNED ENTRIES ARE SKIPPED ENTIRELY, AND THE UNION RULE IS OVERRIDDEN FOR THEM.

An entry with banned: true gets should_be_on_pages: [] and nothing else. Do not
reason about where it ought to go. Do not union its on_pages in — that is the
one place where the union rule is deliberately broken, and it has to be, because
on_pages for a banned video is a list of pages the footage must be REMOVED from,
not pages it should stay on. Unioning them would turn a ban into an instruction
to publish it more widely.

Handle it this way:

  * Set should_be_on_pages: [] on every banned entry. If it previously held
    pages, clear them — this is the one property where clearing is correct, and
    report each cleared page.
  * If a banned entry's on_pages is NOT empty, that footage is live on the site
    today. Report it as a REMOVAL WORKLIST, listed page by page with the ban
    reason, so {THIS_DIR}/p_yaml_to_site.md strips those placements. Leave
    on_pages itself untouched — it is the observation that drives the removal.
  * Nothing links into a banned video from anywhere: no card, no thumbnail, no
    table-of-contents row, no "see also" link. There is no Level 5 page to link
    to, so any link that exists is broken as well as unwanted.

EVERY PATH MUST BE REAL, FULL, AND VERIFIED — NO PLACEHOLDERS.

This is the rule that matters most in this stage, because the value is reasoned
rather than read off disk, which makes it the one place a plausible but
fictional path can slip in. A path here is only ever COPIED from a real row of
{PAGES_CSV} or from a real filesystem walk of {DOCS_DIR}. It is never composed,
guessed, abbreviated, or typed from memory of what a page is probably called.

  * FORBIDDEN, and a hard failure if any of these reach the file:
      - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/....mdx"
      - page: "~/BGit/Bryan_git/charlie-kirk/site/docs/Mic/....mdx"
      - page: ".../site/docs/Mic/overview.mdx"
      - page: "site/docs/Mic/overview.mdx"             (repo-relative)
      - page: "/Mic/overview"                          (a URL path)
      - page: "~/.../charlie-kirk/site/docs/Mic/rigged-mic.mdx"  (invented file)
    Any value containing an ellipsis, "...", "TODO", "TBD", "<", ">", or any
    other placeholder token is invalid. Any value that is not an absolute
    tilde-rooted path ending in .md or .mdx is invalid.

  * THE ONLY LEGAL WAY TO PRODUCE A VALUE. Build a candidate index once, up
    front, and select from it. Nothing outside the index may ever be written:
      1. Read {PAGES_CSV}. Its file_path column is repo-relative
         (site/docs/Mic/overview.mdx). Expand each to {ROOT_DIR}/<file_path> in
         tilde-rooted form.
      2. Walk {DOCS_DIR} for every .md/.mdx on disk. Union it with the CSV set —
         the CSV can lag, the filesystem is what actually exists.
      3. stat() every candidate. Drop any that does not exist. Keep the
         surviving set as THE candidate index, keyed by its tilde-rooted path.
      4. Every value written to should_be_on_pages must be a key of that index,
         byte for byte. Selecting a page means selecting an index key — there is
         no code path that constructs a string.

  * VERIFY BEFORE WRITE, then VERIFY AFTER WRITE. Before emitting, re-stat every
    path in every should_be_on_pages list. After emitting, re-parse the YAML,
    expanduser every should_be_on_pages page value, and stat it again. If any
    single path does not resolve to an existing file, the stage FAILS — do not
    write a partial file with bad paths, do not "best effort" it, and do not
    degrade a bad path to "". Fix the selection and re-emit.

  * Never invent a page because the video obviously deserves one. If the right
    page does not exist yet, that is a FINDING, not a path: record it in this
    stage's stdout under "Wanted pages that do not exist" with the video's cid
    and a suggested title, append it to {FINDINGS_FILE}, and leave the video's
    should_be_on_pages holding only the real pages that do exist. Page creation
    is a later prompt's job.

HOW TO DECIDE WHICH PAGES A VIDEO BELONGS ON.

This is where video diverges from images, and the divergence is the whole point.
An image is matched on what it LOOKS like. A video is matched primarily on what
is SAID in it, over time, by a named person — and the transcription is what
makes that possible. Inputs to the decision, in order of weight:

  1. THE TRANSCRIPTION (transcription_file). The heaviest input by a wide
     margin. Read the sidecar, not a truncated summary. What the speaker
     ASSERTS is usually what decides the page: a name, a tail number, a case
     number, a time stamp, a thesis stated out loud. A four-minute monologue
     about the microphone belongs on the Mic pages even when the footage on
     screen is a talking head.
  2. ai_description plus shot_timeline, people_seen, and onscreen_text — what
     is actually SEEN, as opposed to narrated. RECONCILE THE TWO. A video is
     frequently filed under the thesis it argues while its own footage shows
     something much narrower. When they disagree, both facts matter: the claim
     decides the topical page, the footage decides whether the page can honestly
     present it as evidence. Note the discrepancy in {FINDINGS_FILE}.
  3. The YAML node the video already sits under — its _key and title are the
     concept cluster, and that node's site_level_2 / site_page properties (set
     in Stages 7 and 9) already point at the site pages for that concept. This
     is the cheapest strong signal: a video under the level_4 whose site_page is
     site/docs/Planes/N1098L.mdx almost certainly should_be_on that page.
  4. The provenance fields — source_url, source_author, manifest_description —
     and, for older captures, the {MIRROR_DIR} directory the file sits in. They
     carry the filing intent the video arrived with.
  5. {PAGES_CSV} columns: title, description, page_type, level, level2_section,
     url_path. The description column is a one-sentence summary of what the page
     covers and is the best cheap matcher. page_type (person / organization /
     topic / index / …) tells you whether a page is about a PERSON — in which
     case the video must actually feature or substantially concern that person,
     not merely mention their name once.
  6. {CK_FILE} arbitrates when the transcription and the cluster disagree about
     which investigative thread the video really belongs to.

Targeting rules:

  * Aim at Level 3 pages — the specific analysis pages inside a section. That is
    where footage does its work. Level 4 pages are equally good when the concept
    lives that deep.
  * Level 2 overview pages get a video only when it is emblematic of the whole
    section — the one clip a reader landing cold should be offered. Expect this
    to be rare: at most one per Level 2 overview, because a video is heavy.
  * NEVER target a page under {VIDEOS_L2_DIR}. That whole Level 2 is the video
    hierarchy itself: the video's own page there is video_page, and a cluster
    overview listing its children is structure, not a topical placement.
  * NEVER target a page under {DOCS_DIR}/Photos. That is the images pipeline's
    output and targeting it would cross the two hierarchies.
  * Nothing in {THIS_DIR}, nothing in {GENERATOR_DIR}, not {HIERARCHY_FILE}, not
    {VIDEO_MANIFEST}, not {VIDEO_INDEX_MD}, not {PAGES_CSV}, nothing outside
    {ROOT_DIR}. Same scope rule as Stage 11.
  * Do not target Topics3 scaffolding pages, and do not target /Topics3/Videos —
    that page is template scaffolding, not part of this hierarchy.

Quantity rules — TIGHTER THAN THE IMAGES PIPELINE, DELIBERATELY.

  A placed still costs a reader a few hundred kilobytes off the site's own
  static directory. A placed video costs a public IPFS gateway fetch, and this
  corpus runs from 0.5MB to 173MB. The numbers below are lower than the image
  pipeline's for that reason and are not to be relaxed to hit a coverage target.

  * One to three pages per video is the norm. FOUR is the ceiling. A video that
    seems to belong on ten pages is a generic clip (a news segment, a rally
    wide shot, a logo sting) — give it the one or two pages where it is actually
    evidence, not every page it could decorate.
  * Many videos belong on zero topic pages, and [] is a correct and common
    answer. Do not pad. A weak topical match is worse than none: it puts an
    unexplained heavy embed on a page and makes the page look padded.
  * PER-PAGE LOAD: no page is assigned more than SIX videos across the whole
    corpus. After the full pass, count assignments per page; for any page over
    six, keep the strongest six by match quality and report the rest as overflow
    (they are candidates for a new child page — report them under "Wanted pages
    that do not exist").
  * An entry with cid "" and ipfs_pinned false cannot be served to a visitor at
    all. Still plan it — the plan outlives the pin status — but count and report
    those separately, because every one of them is a placement that will render
    as a dead or pending card until it is pinned.

DEFAMATION GATE — applies before any page is added.

should_be_on_pages is a publishing instruction, so the repo's defamation rules
bind here even though this stage writes no page. Video carries the sharper form
of the risk, because the accusation is made OUT LOUD and the media is the
payload:

  * A video whose cid or sha256 appears in {EXCLUDE_FILE} is never assigned to
    any page. Emit should_be_on_pages: [] for it, unconditionally, regardless of
    how good the topical match is.
  * A video that shows or names a living person is assigned only to pages where
    that person's presence is the point. Consult people_seen — it exists partly
    so this gate knows who a placement will put on a page.
  * A video whose speaker accuses a living person of a crime is not assigned to
    that person's own profile page. Reporting that a video CONTAINS a claim is
    fine on a topical page that frames it; parking the accusation on the
    accused's profile is not.
  * A video that catches uninvolved bystanders' faces or voices continuously is
    a candidate for {EXCLUDE_FILE}, not for wider placement. Flag it.
  * When unsure, leave it out and note it.

ACCEPTANCE TARGETS — the run is not done until these hold.

Measure them over ALL video entries (not just the planned ones) after the write,
and print the table. A run that misses any of them is retuned, not shipped:

    should_be_on_pages empty []              >= 5%   and <= 25%
    should_be_on_pages with >= 1 page        >= 75%
    should_be_on_pages with >= 2 pages       >= 20%
    on_pages empty []                        < 100%  (all-empty means broken)

The empty floor matters as much as the ceiling: [] is the correct answer for a
video that genuinely belongs on no topic page, and a run that assigns everything
has stopped discriminating. The bands are wider than the images pipeline's
because this corpus is two orders of magnitude smaller — with 50-odd videos a
single cluster swings the percentage several points. The on_pages check is only
a liveness test: that property is observed, it is legitimately mostly empty, and
it must never be tuned toward these numbers.

HOW TO RUN IT.

  * The candidate index (pages.csv + filesystem walk + stat) and the mechanical
    filters ({EXCLUDE_FILE}, the Videos/Photos scope exclusions, the per-page
    load counts) are SCRIPTED — they are exact and cheap. Put them in
    {GENERATOR_DIR}/plan_should_be.py, modelled on
    {IMAGE_GENERATOR_DIR}/plan_should_be.py, which solved this once already for
    stills. Read that script before writing this one; never edit it.
  * THE SELECTION ITSELF IS DIFFERENT HERE, AND THE DIFFERENCE IS THE POINT. The
    images pipeline scores lexically and measured its own topical precision at
    only 65-70% by hand audit — strong on exact tokens (a name, a tail number, a
    case number), weak on generic geography, because lexical matching has no idea
    which investigative thread a map belongs to. That corpus had ~1,700 entries
    and could not afford judgment. THIS corpus has 50-odd videos, each with a
    transcription that states its thesis in words. Read them. Judgment over 50
    transcriptions is affordable, it is far more accurate than scoring, and it is
    the right call here.
  * Use lexical scoring only as a CANDIDATE GENERATOR — it produces a shortlist
    of ~12 pages per video that a reader then accepts or rejects. If you do
    score, carry over the rules the images pipeline learned the hard way: drop
    bare digit runs from the token stream (a transcript full of times and dates
    scores high on IDF and means nothing); use sublinear term frequency
    (1 + log tf) on the video side, since a transcript repeats its subject
    dozens of times; give a title-match bonus for a distinctive shared token
    (idf >= 4), which is the strongest single signal available; make the
    structural prior PROPORTIONAL to the entry's own best score (0.75x for the
    nearest ancestor node's site_page, 0.35x for further ancestors) rather than
    flat; and gate person pages on the WHOLE name appearing, not any one token.
  * PARALLELISM. Partition the corpus across up to 12 agents by cluster subtree,
    never splitting a video across agents. Each agent is given its videos'
    transcriptions and the shortlist of candidate index keys, and RETURNS rows of
    (cid, node_key, selected_index_key, confidence, one-line reason). An agent
    returning a path that is not in the candidate index has its row REJECTED and
    counted — it never reaches the file. AGENTS DO NOT EDIT {HIERARCHY_FILE}. A
    single writer merges every row in one pass; concurrent writers to one YAML
    corrupt it.
  * The writer applies the quantity and defamation rules, unions in every page
    already present in on_pages, dedupes, sorts each list, re-stats every path,
    and writes once.

RULES.

  * should_be_on_pages is set on EVERY video entry — no entry is left without
    the key. Empty is [], never "" and never a missing key.
  * Grow, do not clobber. An existing non-empty should_be_on_pages from an
    earlier run is MERGED with this run's selections, not replaced. Remove an
    existing entry only when the page no longer exists on disk or the video is
    newly excluded, and report every such removal with its reason.
  * Order each list best-match first. The publishing prompt's per-page cap keeps
    the head of the list and drops the tail, so the order is load-bearing.
  * Page values are IDENTITY fields for sanitization — see OUTPUT SANITIZATION.
    Non-ASCII is emitted as a visible \uXXXX escape, never replaced, so the path
    keeps resolving.
  * This stage creates, moves, and edits NO page. It records a plan.

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

The emitted {HIERARCHY_FILE} must NEVER contain invisible Unicode characters.
Invisible characters (zero-width spaces, bidi controls, no-break spaces, word
joiners, BOMs, control characters, variation selectors, tag characters) are a
security problem: they hide content from review, spoof strings, and smuggle
instructions past a human reading the file. Every byte of the emitted YAML must
be visible in a text editor.

The invisible set includes at minimum: U+0000-U+0008, U+000B-U+001F,
U+007F-U+009F, U+00A0, U+00AD, U+034F, U+061C, U+115F, U+1160, U+17B4, U+17B5,
U+180B-U+180E, U+2000-U+200F, U+2028-U+202F (U+202F NARROW NO-BREAK SPACE is the
one macOS puts in screenshot filenames before AM/PM — it WILL appear in the
inputs), U+205F-U+206F, U+3000, U+3164, U+FE00-U+FE0F, U+FEFF, U+FFA0,
U+FFF9-U+FFFB, and U+E0000-U+E007F.

Note that VISIBLE non-ASCII legitimately appears in the sidecar inputs and is
fine in prose: the transcription header uses U+00B7 MIDDLE DOT as a field
separator and U+2713 CHECK MARK in "✓ full", and the ai_description prose uses em
dashes and curly quotes. Those are visible characters. Leave them alone.

Two treatments, chosen by field kind:

  * PROSE fields (title, ai_description, shot_timeline, people_seen,
    onscreen_text, manifest_description, node titles) — sanitize the CONTENT:
    replace space-like invisibles (U+00A0, U+2000-U+200A, U+202F, U+205F,
    U+3000) with a regular space, DELETE zero-width / bidi / control / joiner
    characters outright, then collapse runs of whitespace. Visible non-ASCII
    stays.

  * IDENTITY fields (file_path, audio_file, transcription_file,
    ai_description_file, ocr_file, video_page, ipfs_url, source_url, on_pages
    page values, should_be_on_pages page values, cid, sha256, also_filed_in,
    site_page, site_level_2) — the
    value must keep matching the real file on disk, so its characters cannot be
    replaced. Emit them as visible ASCII escapes inside YAML double-quoted
    scalars: a U+202F inside a path is written as the SIX VISIBLE CHARACTERS
    backslash, lowercase u, 2, 0, 2, F. YAML's double-quoted style decodes that
    escape on parse, so the parsed value is unchanged and still resolves the
    real file, while the emitted file's own bytes contain nothing invisible.
    Escape ALL non-ASCII in identity fields this way.

    Do NOT paste a literal example of the character itself anywhere — writing
    this very rule is the moment an invisible character gets introduced. The
    validation scan below is what catches it. Heed the scan; never assume the
    emitter is clean because the rule is written down.

MANDATORY after every emit: re-scan the written file and HARD FAIL if any code
point from the invisible set remains anywhere in it. Then re-parse the YAML and
spot-check that an escaped file_path still resolves to an existing file on disk.
{IMAGE_GENERATOR_DIR}/sanitize_common.py implements this for the images
pipeline; read it and reuse the approach rather than reinventing the character
tables.

============================
STAGE 14 — COUNTS, PUBLISHABLE, NEEDS_SPLIT, INTEGRITY
============================

* Recompute number_of_videos (direct) and number_of_videos_recursive (subtree)
  on every node. They count EVERY entry, banned included — the YAML is the
  complete private record and its counts describe what is held, not what is
  published. publishable is where the ban shows up, not the counts.
* Set publishable on every node: true when the subtree holds at least one video
  with banned false, false otherwise. A node with videos in it that are ALL
  banned is publishable: false — report that case separately, because it is the
  one where the counts and the publishable flag disagree and a reader of the
  YAML will otherwise think it is a bug.
* Re-evaluate needs_split: over 12 direct videos → true; at or under 12 → remove
  the flag.
* Verify every _key is unique across the whole file.
* Verify no node contains the same cid twice. Same cid under DIFFERENT nodes is
  legitimate cross-filing — keep it and keep also_filed_in accurate.
* Verify every video entry carries the FULL property set from the schema. No key
  is ever missing; "" stands in for any scalar with no value, [] for on_pages and
  should_be_on_pages, false for the booleans.
* Verify on_pages is a subset of should_be_on_pages on every entry, or the entry
  is listed with the reason its on_pages page was deliberately subtracted.
* Verify every should_be_on_pages page value: it is an absolute tilde-rooted path
  ending .md or .mdx, it EXISTS on disk, it carries no placeholder token, and it
  lies outside {VIDEOS_L2_DIR} and {DOCS_DIR}/Photos. Any failure is a hard fail,
  not a warning.
* Verify every entry carries a banned key holding a real boolean — not null, not
  a string "true", not missing. Any failure is a hard fail.
* Verify the banned values still agree with {BAN_VIDEOS_CSV} as it stands right
  now. Re-read the CSV here rather than trusting that Stage 6B ran; the CSV may
  have been edited mid-run, and this is the last cheap chance to catch it.
* Verify no banned entry has a non-empty should_be_on_pages and none has a
  non-empty video_page. Both must be 0. A banned video with a planned placement
  or a bound Level 5 page is the exact failure this whole gate exists to prevent.
* Verify no entry in {EXCLUDE_FILE} has a non-empty should_be_on_pages.
* Count assignments per page; report every page over the six-video load.
* Verify every non-empty transcription_file, ai_description_file, ocr_file,
  audio_file, and file_path resolves to a file that EXISTS on disk. A path that
  does not resolve is worse than "" — it makes a later pass fail silently.
  Report every one.
* Verify every non-empty video_page exists and lives under {VIDEOS_L2_DIR}. Zero
  may live under {DOCS_DIR}/Photos.
* Verify NO entry has a file_path ending in an image extension. Any that do are
  inherited placeholders that survived the rebuild — report them; the count must
  be 0.
* Verify no ai_description value begins "This image" — same test, from the prose
  side. The count must be 0.
* Verify the YAML parses.
* Run the OUTPUT SANITIZATION validation and fail hard on any hit.

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

* Confirm every non-excluded site Level 2 maps to exactly one level_3
  (site_level_2 present somewhere).
* Confirm the Other level_3 exists.
* Confirm every home-page TOC concept resolves to a level_3.
* Confirm every record in {VIDEO_MANIFEST} appears in the YAML exactly once
  (cross-filed copies excepted, and those carry also_filed_in).
* Confirm every .mp4 in {VIDEOS_DIR} appears exactly once.
* Confirm every .transcription and .ai_description under
  {REPO_VIDEO_SIDECAR_DIR} and {REPO_IPFS_SIDECAR_DIR} is referenced by exactly
  one entry — an unreferenced sidecar means a video was missed by Stage 2.
* Spot-check 10 entries end to end: open the media file (or confirm the CID),
  open the transcription, open the ai_description, and confirm the YAML's
  duration, engine, ai_description prose, and shot_timeline actually match the
  sidecars.
* Spot-check 10 should_be_on_pages assignments BY HAND: open the page, read what
  it is about, read the video's transcription, and judge whether the footage
  genuinely belongs there. Report the hit rate honestly — this is the only
  measurement of the stage's real precision, and the images pipeline's equivalent
  audit came back at 65-70%, not the 100% the scores implied.
* Print the final tree: each level_3 _key with its recursive video count, child
  count, and publishable flag.
* Append everything notable to {FINDINGS_FILE}: the transcription work list, the
  unpinned list, the unresolved-reference list, the no-video-coverage node list,
  and the .ocr format discovered in Stage 1.

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

* {HIERARCHY_FILE} is the MASTER DATA for video. Stage 6 in REBUILD mode is the
  single time it may be replaced wholesale. In UPDATE mode it only grows: no
  node and no video entry is ever deleted, no duplicate is ever created, and
  existing items get their properties updated in place.
* EVERY video entry carries EVERY key in the schema. A scalar with no value is
  "", never null and never omitted; on_pages and should_be_on_pages emit [];
  booleans emit false. This is what lets a later pass distinguish "not looked up
  yet" from "looked up, does not exist".
* on_pages is OBSERVED, should_be_on_pages is REASONED, and should_be_on_pages
  is a SUPERSET of on_pages — the complete desired state, not a list of extras.
  Never let topical reasoning write on_pages, and never let should_be_on_pages
  inherit an on_pages binding that was not verified against the page itself.
  The ONE exception to the superset rule is a banned entry: it gets
  should_be_on_pages: [] and its on_pages is a removal worklist, never a source
  of placements.
* banned IS COPIED DOWN, NEVER DECIDED HERE. {BAN_VIDEOS_CSV} is the master and
  the repo charter ({ROOT_DIR}/claude.md, "Banned Media") owns the contract.
  Stage 6B is the only stage that writes the key; every other stage reads it.
  Every entry carries it as a real boolean and the default is false. A banned
  video gets no Level 5 page, no poster, no placement on any page, no link into
  it from anywhere, and is never pinned — and its entry is never deleted from
  {HIERARCHY_FILE}, because banning is a publish-time gate over a file that only
  grows. When a run finds material that should not be public, add the row to
  {BAN_VIDEOS_CSV} with a reason before the run ends.
* Every path this prompt writes — file_path, the sidecar paths, video_page,
  on_pages, should_be_on_pages — is an absolute tilde-rooted path to a file that
  EXISTS on disk at the moment of writing. Placeholders, ellipses, repo-relative
  paths and URL paths are hard failures, not warnings. A page that ought to exist
  and does not is a finding for {FINDINGS_FILE}, never an invented path.
* transcription_file, ai_description_file, and ocr_file are REQUIRED properties
  and filling them is the primary purpose of this prompt. A non-empty value must
  resolve to a file that exists on disk.
* This prompt creates, moves, or edits NO page under {SITE_DIR}. It does not
  touch {SITE_DIR}/sidebars.ts and it does not modify {PAGES_CSV}. The YAML is
  the plan; publishing is a later prompt.
* Never write anything under {IMAGE_PLANNING_DIR}, {ROOT_DIR}/images, or
  {DOCS_DIR}/Photos. Read them freely as prior art. Never copy a file FROM there
  into {THIS_DIR} — every file here is a converted descendant of one and a
  re-copy silently reverts the conversion.
* Never copy video bytes into {SITE_DIR}/static. Public IPFS gateways serve the
  video. A poster frame MAY later be served locally from
  {SITE_DIR}/static/img/video_posters/ because a poster is small; nothing else
  about a video is.
* NOTHING IS EVER PINNED by this prompt. Recording pin status is this prompt's
  job; changing what is public is not. Any pinning job must first filter out
  every entry in {EXCLUDE_FILE}.
* _key uniqueness is file-wide; _keys are the future page_keys. ASCII only.
* {HIERARCHY_FILE} must never contain invisible Unicode. Prose is cleaned;
  identity fields are emitted with visible \uXXXX escapes; every emit is
  followed by the validation scan. Security rule, not a style rule.
* Clusters are concept clusters. The folder proposes, the transcription decides,
  {CK_FILE} arbitrates.
* DEFAMATION. This prompt writes nothing public, but what it harvests becomes
  public later, so the fields must be safe to publish. Video adds a failure mode
  images do not have: a speaker in the footage makes an accusation OUT LOUD, and
  the transcription captures it verbatim. Reporting that a video CONTAINS a
  claim is fine; repeating the claim in the site's own voice is not. So: never
  put an accusation in a `title` or an `ai_description` — those are the fields
  the page generator copies into headings and link text. Keep raw claims in the
  transcription sidecar and in {CK_FILE}, where they are private, and let the
  later prompt quote and attribute them deliberately. people_seen exists partly
  so the defamation pass knows which living people a page will name.
* Do not put Docusaurus pages in {THIS_DIR} and do not put planning notes in
  {VIDEOS_L2_DIR}. Do not put a copy of the YAML in {THIS_DIR} — it lives in
  {VIDEOS_DIR}.

============================
BACKGROUND — ORIGINAL DIRECTIVE, KNOWLEDGE PRESERVED
============================

This section preserves the full intent of the directives this prompt was built
from, so no knowledge is lost even where a stage above already encodes it.

* {HIERARCHY_FILE} is where the master data belongs. The file was copied from
  the images pipeline, which built images.yaml; the video pipeline needs its own
  master data and this prompt produces it. The data the file carries today has
  no value and is to be completely replaced; the schema is to be improved where
  video needs fields that images did not.
* Large File Bridge ({LFB_DIR}) is the web app that produces the AI
  descriptions, the transcriptions, and the OCR of files. Reading its product
  management specifications and its code is how the mapping between an original
  file's path and its sidecar's path is learned. The files that map to the .mp4
  videos are what this pipeline reads to understand each video and build the
  content of the YAML.
* Storage rule (git repo case): charlie-kirk is a working git repo, so Large
  File Bridge quarantines all sidecars in .lfbridge/ and mirrors the original
  directory path underneath it. The sidecar keeps the full original filename and
  appends a second extension:
      ~/BGit/Bryan_git/charlie-kirk/videos/<name>.mp4
        →  ~/BGit/Bryan_git/charlie-kirk/.lfbridge/videos/<name>.mp4.transcription
        →  ~/BGit/Bryan_git/charlie-kirk/.lfbridge/videos/<name>.mp4.ai_description
  Mirrored subdirectories present under .lfbridge/: videos/, images/,
  cover_image/, IPFS/, site/. Worked example, a video both transcribed and
  AI-described:
      /Users/bryan/BGit/Bryan_git/charlie-kirk/videos/_QwGo0LyZ3I.mp4
      /Users/bryan/BGit/Bryan_git/charlie-kirk/.lfbridge/videos/_QwGo0LyZ3I.mp4.transcription
* These directories hold the OCR, transcription, and AI-description text files:
      {COMPANY_BRIDGE_DIR}
      {PERSONAL_BRIDGE_DIR}
      {REPO_SIDECAR_DIR}
  Every video entry gets YAML properties holding the file path to each sidecar
  that correlates to it — that requirement is the reason this prompt exists.
* "Level 2" refers to the fact that we will eventually put a video-hosted page
  for every video under a Level 2 directory called videos ({VIDEOS_L2_DIR}). The
  YAML's level_3 list is a superset that includes the website's Level 2s —
  except videos and images and any unfiltered or catch-all category — plus an
  "Other" entry. We then take every other Level 2 and its Level 3 pages and make
  a level_4 for each, parented hierarchically. We create a level_5 per video: a
  video found on a site Level 3 page becomes a level_5 entry parented on the
  level_4 that correlates to that Level 3 page. We are reproducing the site's
  hierarchy inside the YAML with every level incremented by one.
* A further stage goes through all the pages and makes sure every page that has
  one or more videos gets those videos into the hierarchy. No duplicates — it
  does not add one that already exists, but it DOES update the properties.
* The YAML must be built into the most full and complete hierarchy possible.
  The home page carries more than one table of contents; all of them become
  level_3s. That is expected to add items the earlier stages did not find. Never
  create dupes, but always look for more that can be added.
* The end goal: the list-of-videos page (the top level of the videos area) will
  be mostly a table of contents — a table with links into the videos directory's
  Level 3 pages, which come directly from this YAML's level_3 nodes.
* video_page holds the full path from ~ to the Level 5 page that hosts one video
  and carries its write-up, so the YAML can find the published page for any
  video later. All YAML properties are kept up to date on every entry so that
  everything is findable later; a property with no value is written as "" rather
  than dropped.
* There is a property called should_be_on_pages, a sub-hierarchy under each
  video exactly like on_pages: a list of `- page:` mappings, each holding the
  full path from ~ to a real page file. on_pages says where the video IS shown;
  should_be_on_pages says where it OUGHT to be shown. Filling it in — figuring
  out the right values — is this prompt's job; putting the videos onto those
  pages is {THIS_DIR}/p_yaml_to_site.md's job. That split is deliberate: one
  prompt reasons about the plan and writes it into the YAML, the other reads the
  plan and builds the pages, and neither does the other's work. The images
  pipeline established this pattern for stills and it is reproduced here in full.
* Learn from the existing YAML's structure and conventions, and from the images
  pipeline in {IMAGE_PLANNING_DIR} as prior art — it solved these same problems
  once already for stills. Read it; never edit it.
* Rewritten 2026-07-23 after auditing the real corpus and the real sidecar
  formats on disk. The census, the sidecar formats, the audio sibling rule, the
  expanded schema, and the publishable gate in this prompt are all verified
  facts rather than assumptions inherited from the images pipeline.
