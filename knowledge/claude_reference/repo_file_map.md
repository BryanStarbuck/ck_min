# Repo File & Directory Map (full)

Moved verbatim out of {ROOT_DIR}/CLAUDE.md on 2026-09-24. ROOT_DIR = ~/BGit/Bryan_git/charlie-kirk. Planes/flight-data entries live in flight_data_recovery.md.

================================================================================
== File & Directory Map — What Does What ==
================================================================================

A map of the files and directories in this repo that DO something — generators,
registries, charters, pipelines, and master data — as opposed to ordinary
content. Read this before hunting for "where is the thing that builds X".

Paths are relative to {ROOT_DIR} (~/BGit/Bryan_git/charlie-kirk) unless a full
path from ~ is given.


=== Nested CLAUDE.md Charters ===

Several directories carry their OWN CLAUDE.md. These are area charters and they
GOVERN work inside that directory. Read the nested charter before touching
anything in its subtree — the root CLAUDE.md does not repeat their rules.

DIR:
* images/CLAUDE.md: Charter for the image pipeline. Defines IMAGES_YAML,
  PLANNING_DIR, GENERATOR_DIR, PHOTOS_DIR and how they relate.
* image_planning/CLAUDE.md: Charter for the image hierarchy planning pipeline.
  Records that the hierarchy YAML MOVED to images/images.yaml on 2026-07-22 —
  anything still saying "hierarchy_images.yaml" is stale.
* videos_planning/CLAUDE.md: Charter for the video pipeline. Opens with a
  self-check banner: if its first variable line says "image_planning", this file
  was clobbered by a copy from the images side and must be restored. The two
  pipelines are siblings, never copies of each other.
* site/docs/laws/CLAUDE.md: Charter for the four-federal-laws drafting project —
  the Epstein Files Transparency Act (PL 119-38) model, case 251403576, and what
  the laws must force disclosed.
* site/docs/Charlie/CLAUDE.md: Directory tree map for the Charlie section,
  including the Comments/ subtree of per-remark pages.
* site/docs/Planes/following/CLAUDE.md: Charter for the public page-per-location
  follow log. Two rules: everything here is PUBLIC Docusaurus (no scratchpads,
  no raw dumps), and ALL info that can safely be public SHOULD go here — do not
  hold material back for tidiness or because it is only a fragment.
* site/docs/Planes/following/apis/CLAUDE.md: Charter for how flight data is
  actually fetched. Declares the variable block (FLIGHTS_CSV, OVERLAPS_CSV,
  OVERLAP_DIR) used by the four API-source subdirectories.
* site/docs/After/house/CLAUDE.md: Charter for 691 W 925 S St, Orem UT 84058 —
  the staging-house line of inquiry. One .mdx per topic, parent Level 2 = After.


=== Root-Level Master Data Files ===

FILE:
* pages.csv: Master index of every public page. See the "Pages CSV" section
  above for the column contract. ~2 MB — grep it, do not read it whole.
* interesting_pages.csv: Ranked shortlist of the most compelling pages, with a
  why_interesting column holding the single strongest hook for each page and a
  use_count tracking how often it has been surfaced. This is the file to pull
  from when picking what to feature, tweet, or link.
* people.csv: person_key → name → url_path → file_path for every person page
  under site/docs/People/. The lookup table for people cross-linking.
* planes.csv: plane_key, phrase, aliases, target page, aircraft type, operator,
  category, autolink_terms, link_enabled. Drives tail-number autolinking across
  the site — add a row here to make a tail number link itself everywhere.
* planes.yaml: Long-form per-aircraft record (type, program, operator, observed
  behavior). The narrative companion to planes.csv.
* aircraft_costs.csv: Per-tail FAA registration facts (type, year, serial,
  registered owner, status, seats) plus in-production status, nearest comparable
  new aircraft, and today's new-build cost. Feeds the Planes/Aircraft-Costs page
  and answers "who could afford to fly this".
* videos.csv: Every video → its IPFS CID, gateway URL, the page it appears on,
  its Level 2 parent, a not_on_any_page flag, description, and source X URL.
* timeslines.csv: Registry of the "likelihood-of-when" timeline SVGs
  (km-*-timeline.svg) — event_key, event, path to the SVG, and what the curve
  actually claims. Written and consumed by prompts/p_timeline_create.md.
* file_list.yaml: Maps each Large File Bridge "One Repo → Metrics" tile to the
  exact absolute file paths behind it.
* missing_videos.txt: Report of IPFS video embeds on the site whose bytes could
  NOT be pulled from the network and are not in the repo. Broken-evidence list.
* 404_Investigation_Report.txt: Google Search Console 404 investigation for
  whoassassinatedcharliekirk.com — which URLs Google has that the site does not.
* ck_main_progress.txt: Running progress notes on the Level 2 build-out.
* Charlie_Kirk_AI_Inbox.txt: SYMLINK to {CK_INBOX}. Append-only staging file for new
  investigation content. AI writes HERE, never to Charlie_Kirk.txt. Bryan merges
  by hand. See the ABSOLUTE RULE at the top of this file.
* .gitignore: Carries a warning banner at the bottom. If ~1,950 per-image lines
  reappear, Large File Bridge re-added them — delete them, do not work around
  them with `git add -f`. See "Images Are Tracked In Git" above.


=== Image Pipeline ===

DIR:
* images/: The image files themselves plus their master data. Tracked in git —
  never gitignore an image.
* images/GPT_Imagine/, images/laws/, images/ico/: Generated/illustrative art —
  law card images, favicons, and GPT-generated law graphics.
* image_planning/generator/: The Python/JS toolchain that turns images.yaml into
  live pages. ~20 scripts, each one stage of the pipeline.

FILE:
* images/images.yaml: {IMAGES_YAML}. Master hierarchy of every image — its
  placement, its cluster, its should_be_on_pages list, and its banned flag.
  Edit programmatically via bind_image_pages.py's emit/recount helpers so the
  file round-trips byte-for-byte.
* images/manifest.yaml: Per-image provenance — filename, IPFS CID, gateway URL,
  source X post URL, source author, description. The chain-of-custody record.
  Note: most CIDs here came from `ipfs add -n` and are NOT retrievable from a
  gateway — serve images from the repo path, keep the CID in data-cid only.
* images/ban_images.csv: {BAN_IMAGES_CSV}. MASTER never-publish list for images.
  See "Banned Media" above. Edits go here, never into images.yaml.
* image_planning/exclude_images.txt: Legacy sha256-per-line never-publish list.
  Still honoured — the ban set is the UNION of this and ban_images.csv.
* image_planning/layout_guidelines.txt: Authoritative standard for how an image
  sits on its Level 5 /Photos page and how big it gets. Every rule in it was
  written after a real visible defect shipped — treat it as a defect log, not a
  style preference.
* image_planning/findings_for_hierarchy.md: Open data/clustering problems in
  images.yaml, raised by page-generation runs that treat the YAML as read-only.
* image_planning/generator/audit_image_publication.py: Repo-wide check that every
  image a visitor should see is actually reachable. Exit 0 clean, 1 broken.
  `--gateway` also probes any remaining ipfs.io <img> embeds. Run by ck_add_text
  at step 9H-6b.
* image_planning/generator/bind_image_pages.py: Binds images to pages and holds
  the emit/recount helpers that keep images.yaml byte-stable.
* image_planning/generator/gen_photos_pages.py: Generates the Level 5 one-image
  pages under site/docs/Photos/, deleting pages for newly banned images.
* image_planning/generator/ban_set.py: Computes the effective ban set (CSV ∪
  exclude_images.txt) that every other stage filters against.
* image_planning/generator/plan_should_be.py / place_should_be_images.py:
  Decide which pages an image SHOULD appear on, then actually place it.
* image_planning/generator/grow_hierarchy.py / update_hierarchy.py /
  fixup_hierarchy.py: Grow, refresh, and repair the images.yaml tree.
* image_planning/generator/add_orphan_images.py: Files images that exist on disk
  but appear in no hierarchy entry.
* image_planning/generator/refresh_pages_csv.py: Re-syncs pages.csv after the
  image pipeline creates or deletes pages.
* image_planning/generator/verify_photos.py / verify_on_pages.py /
  verify_stage_12_13.py: Verification passes for the Photos tree.


=== Video Pipeline ===

DIR:
* videos/: The video files (gitignored — pulled from IPFS) plus their master
  data and .transcription / .ai_description sidecars.
* videos_transcription/: One .md transcript per video, named by the X status ID.
  114 files. This is where to grep for "who said what on video".
* videos_planning/generator/: The Python toolchain for the video pipeline, plus
  its stage report JSONs (stage2/3/10_report.json, verify_report.json) which are
  the audit trail of the last run.

FILE:
* videos/videos.yaml: {VIDEOS_YAML}. Master video hierarchy — the video-side
  twin of images.yaml, carrying placement and the banned flag.
* videos/manifest.yaml: Per-video provenance — filename, CID, gateway URL,
  source X URL, source author, description.
* videos/videos.md: Human-readable video evidence index with access instructions.
* videos/ban_videos.csv: {BAN_VIDEOS_CSV}. MASTER never-publish list for videos.
* videos_planning/exclude_videos.txt: Legacy sha256 never-publish list for
  videos. Union with the CSV, same as the image side.
* videos_planning/generator/emit_yaml.py: The safe programmatic writer for
  videos.yaml — use it instead of hand-editing.
* videos_planning/generator/audit_video_registration.py: Checks every video on
  the site is registered, hosted, and not banned.
* videos_planning/generator/compute_cids.py: Computes IPFS CIDs; hash_cache.json
  caches the expensive hashing between runs.
* videos_planning/generator/harvest_sidecars.py: Pulls .transcription and
  .ai_description sidecars produced by Large File Bridge into the pipeline.
* videos_planning/generator/gen_videos_pages.py / bind_video_pages.py /
  stage56_host_pages.py: Generate and bind the Level 5 video pages.
* videos_planning/layout_guidelines.txt: Video-page layout standard, same role
  as the image one.


=== Site Build & Page Tooling ===

FILE:
* site/_ck_mdxcheck.mjs: Compiles pages exactly the way the real Docusaurus
  build does, so MDX breakage is caught locally. Deliberately does NOT enable
  @slorber/remark-comment — adding it once made every laws/*.md page pass
  locally and fail the deploy. `node site/_ck_mdxcheck.mjs <files...>`.
* tools/sync_right_bar.py: Generates the wording of the right bar (the notice
  rail shown on every page by site/src/theme/Root.tsx) from
  ~/BGit/all/politics/charlie_kirk/ck/docusaurus/right_bar.txt into
  site/internals/src/data/right_bar.json. READS the txt, never writes it. Edit
  the txt, run `python3 tools/sync_right_bar.py`, commit the JSON. The email
  at the end of the txt renders as a mailto: link.
* site/inject_nav_gallery.py: Idempotently injects two-column nav galleries into
  every non-root overview.mdx under Photos/ and Videos/, between CK_NAV_GALLERY
  markers, above "Related Areas" and below the in-body TOC. Computes real aspect
  ratios from the actual pixels.
* site/sidebars.ts: Navigation structure.
* site/docusaurus.config.ts: Site config — domain, navbar, OG social card.
* .github/workflows/pages.yml: GitHub Pages deploy. The live site is built from
  the REPO, not from any one machine — an untracked image 404s for every visitor.

DIR:
* site/internals/static/img/evidence/: Served evidence images, /img/evidence/<sha>.jpg.
* site/internals/static/img/video_posters/: Video poster frames.
* site/internals/static/img/km-timelines/: The likelihood-of-when timeline SVGs
  registered in timeslines.csv.
* site/internals/static/img/infographics/: Published infographic outputs.
* site/internals/static/court/: Court exhibit assets (bindover/, mirandize/).
* site/internals/static/data/: Site-served datasets, e.g.
  apple-podcast-removed-episodes.csv.
* site/internals/src/: The site's React/CSS layer — custom.css, HomepageFeatures,
  and the 404 page.
* site/Content_Structure/: CS_After.yaml, CS_Before.yaml, Describe.yaml — the
  planned content structure for those Level 2 areas.
* site/keywords/: Per-topic .keywords files (Israel, Media, People, TPUSA,
  Tyler_Robinson) used for search/keyword mapping.
* site/Download_Transcript/: Self-contained transcription tool with its own
  README/USAGE/QUICK_START, a script/ dir, and to_transcribe/ + transcribed_out/
  working directories.


=== Prompts ===

DIR:
* prompts/: The prompt library that drives most site-wide work.
* prompts/four_squares/: The live working state of the four-squares card build —
  ledger.csv, card_index.csv, routes.txt, teasers/, batches/, plus ~15 repair
  scripts. This is a RUN IN PROGRESS, not a finished artifact.
* prompts/2_Level/, prompts/Change_Levels/, prompts/Grow_Content_Structure/,
  prompts/Download_Transcript/: Prompt sets for building Level 2 pages, moving
  pages between levels, growing the content structure, and transcription.
* prompts/backup/: Superseded prompt versions kept for reference.

FILE:
* prompts/Assess_Manual.md: {ASSESS_MANUAL}. The authoritative writing and layout
  guide. Read it into context at the START of any task that creates, edits,
  reviews, or restructures a page.
* prompts/p_4_squares.md: The four-squares card-block system — adds four
  standard blocks to every page. Run by 12 parallel agents.
* prompts/four_squares/AGENT_BRIEF.md: Operational summary handed to each of the
  12 agents running p_4_squares.md.
* prompts/four_squares/RESUME.md: Checkpoint state — pages complete, cards on
  site, teasers banked. Read this to know where the run stopped.
* prompts/four_squares/GOLDEN_EXAMPLE.mdx: The reference output every generated
  page is matched against.
* prompts/p_timeline_create.md: Builds the site-wide likelihood-of-when timeline
  SVGs and their registry rows. Marked DO NOT RUN YET at the top — check that
  line before running it.
* prompts/p_Mirandize.md: The Miranda-timing line of inquiry (the 6:25 PM bodycam
  vs the 8:02 PM identification call).
* prompts/p_more_level_2.txt + prompts/more_level_2.yaml: Mines sources for
  proposed new Level 2 sections and Level 3 pages. The YAML only GROWS and
  nothing in it is applied to the site automatically — it is a proposal queue.
* prompts/grok_write.mdx: Staged writing prompt; the runner passes INPUT_TEXT to
  say what this run focuses on.
* prompts/Create_Topic_Pages.txt / Write_Level_2_page.txt: Page-creation prompts.


=== Infographics ===

DIR:
* site/internals/static/img/infographics/{Topic}/: One directory per infographic
  — goals.mdx (the plan), nana_banana_pro_prompt.txt (the generation prompt
  written FROM goals.mdx), and the generated .jpg/.png, served at
  /img/infographics/{Topic}/. See the "Infographics" section above. MOVED here
  from {ROOT_DIR}/info_graphics/ on 2026-08-28; that directory is gone.
* site/internals/static/img/infographics/Overlap_Timeline/: Also carries
  generate_overlap_timeline.py — a deterministic Python renderer, showing an
  infographic can be CODE-generated rather than model-generated when the data
  must be exact. The published artefact is the SVG one level up at
  /img/infographics/Overlap_Timeline.svg; the .jpg beside the script is a DESIGN
  REFERENCE ONLY — the 2026-08-26 model render spelled every string correctly and
  got every bar wrong.
* site/docs/Planes/info_graphic/: Infographic TEMPLATES for the Planes section —
  _goals_template.mdx and _nana_banana_pro_prompt_template.txt. Templates only;
  underscore-prefixed so Docusaurus never publishes them. No finished infographic
  ever lives under site/docs/ — it cannot be served from there.


=== Pushing This Repo ===

FILE:
* tools/push.sh: **Use this instead of a bare `git push`.** A plain push here
  fails intermittently with `cannot lock ref 'refs/heads/main': is at <A> but
  expected <B>`. That is a lost compare-and-swap on the remote ref — NOT a size
  problem, NOT a non-fast-forward, and NOT lost data. This repo uploads ~180 MB
  of gzipped ADS-B evidence at a few MB/s, so a push holds the connection open
  for most of a minute, and the external auto-commit job on the other machine
  ("Bryan 26 Tower" / "Bryan 27 Laptop") can land its own push inside that
  window. GitHub then rejects the entire upload even though every object arrived.
  The script retries: it first checks whether HEAD is already contained in
  origin/main and says so plainly (the usual answer — nothing was lost), and only
  rebases and re-pushes if we are genuinely behind. It never force-pushes and
  never creates or switches a branch.
      sh tools/push.sh [max_attempts]     # default 5
  **Before concluding a push failed, run `git fetch origin` and compare HEAD to
  origin/main.** The rejection message says nothing about whether the content
  landed, and it usually did.
* .gitattributes: marks the ~15,500 already-compressed tracked files (`*.gz`,
  `*.jpg`, `*.png`, `*.pdf`, ...) as `binary -delta`. Git cannot shrink a gzip or
  JPEG stream: measured over 3,000 geo_sweep `.json.gz` traces, the default pack
  was 146,283,926 bytes and one with compression and delta search disabled was
  146,284,199 — a 273-byte difference across 146 MB, bought with double the
  packing CPU. On a single `.gz` blob git's zlib pass makes the object 0.04%
  LARGER. `binary` also stops any text/eol conversion from ever touching a byte
  of evidence. This does not rewrite history and produces no diff on tracked
  files. Do NOT "fix" push failures by migrating to Git LFS — that rewrites
  history, needs a force-push, and would break the auto-push machine.

=== Credentials & Secrets ===

**No credential of ours has ever lived in this repo, and none may.** API keys for
the flight-tracking vendors live OUTSIDE every git repo, in the house credential
store, and are read at run time.

FILE:
* ~/.credentials/charlie_kirk.json: THE credential store for this investigation.
  Mode 600, outside every repo, same one-file-per-app shape the other apps on this
  machine use. Keys sit under `charlie_kirk.flight_apis`: `FR24_API_TOKEN`,
  `AEROAPI_KEY`, `ADSBX_RAPIDAPI_KEY`, `OPENSKY_CLIENT_ID`, `OPENSKY_CLIENT_SECRET`.
  An empty string means "not held", and the client then reports BLOCKED on
  credential — which is itself a publishable finding, not a failure to hide.
* site/docs/Planes/following/apis/public_open_source/code/lib/credentials.js: the
  ONLY thing that knows where credentials live. `cred(NAME)` reads the environment
  first, then the store; `have(...)` and `report(...)` let a script say what it is
  missing without putting the value anywhere near stdout. Set `CK_CREDENTIALS_FILE`
  to point it at a different store. Warns if the store is group- or world-readable.
* security/scan_secrets.py: scans tracked (or `--staged`) files for credentials and
  prints the file and line number, NEVER the value. Exit 0 clean, 1 findings.
  Archived flight-tracker HTML under `*/data/recovered/` USED to be skipped on the
  grounds that the keys in it are the vendor's own and were already public. That
  changed on 2026-08-24: GitHub push protection does not care whose key it is, and
  it rejected the push of the whole investigation over FlightAware's Mapbox token
  in a captured N102DZ page. Captures are now scanned — with the SHAPE patterns
  only, since raw ADS-B traces are full of random-looking values that are position
  data, not secrets.
* security/scrub_vendor_tokens.py: the fix for that class. Redacts THIRD-PARTY
  vendor keys inside captures (FlightAware's Mapbox / Stadia / Vicinity tokens,
  Flightradar24's Firebase web key) by replacing just the VALUE with
  `__REDACTED_VENDOR_CREDENTIAL_sha256_<16 hex>__`. The key name, the markup and
  every byte of flight data are untouched, and the fingerprint is one-way but
  stable — so "this page served the same key as that page" is still provable. We
  lose the secret, not the proof. `--check` reports without writing.
  Run it over everything: `python3 security/scrub_vendor_tokens.py`
* site/docs/Planes/following/apis/public_open_source/code/lib/scrub.js: the
  write-time twin of the above, so a capture is redacted on its way to disk rather
  than after the fact. Wired into `save()` in recover_erased.js and into
  recover_adsbx_samples.js; each capture's `.meta.json` records
  `vendor_credentials_redacted: <count>`, so an altered capture says so plainly.
  Keep it in step with the Python: same patterns, same marker.
* security/pre-commit + security/install_hooks.sh: the hook that blocks a commit
  carrying a credential, and the installer. **.git/hooks/ is not cloned — run
  `sh security/install_hooks.sh` once on every machine that checks this repo out.**
  Emergency escape is `git commit --no-verify`, and it should never be needed.

Rules:
* Never paste a key into a script, a page, a prompt file, a CSV, or a commit. Put
  it in the store and let the loader find it.
* `.gitignore` carries a SECRETS block (`.env*`, `*.pem`, `*.key`, `id_rsa*`,
  service-account JSON, `.netrc`, …) as the backstop. It is not the policy.
* A missing credential is reported by NAME. No script ever prints a value.
* A THIRD-PARTY key inside an archived capture is NOT deleted and NOT skipped —
  it is redacted in place by security/scrub_vendor_tokens.py. Never "fix" a
  blocked push by deleting the capture; the capture is the evidence.
* If GitHub push protection ever blocks a push again, do not click the allow-secret
  link. Run the scrubber, and check whether the offending value is only in unpushed
  commits — if it is, resetting to origin/main and recommitting removes it from
  history entirely, with no force-push.

=== IPFS & Large Files ===

DIR:
* IPFS/: Evidence files published to IPFS so they cannot be taken down.
* IPFS/videos/: Large source videos (gitignored) — the Blake Bednarz UVU
  original and its transcription, chain_of_evil.mp4.
* .lfbridge/: Large File Bridge quarantine mirror. Sidecars for files inside
  this repo land here, mirroring the path — e.g. videos/X.mp4 →
  .lfbridge/videos/X.mp4.transcription. Not hand-maintained.

FILE:
* IPFS/ipfs.txt: The pull-and-pin command blocks for every published file.
* IPFS/ipfs.sh: Runnable version of the same — `ipfs pin add <CID>` per file,
  with notes on `ipfs get -o` if you also want the bytes on disk.


=== Research & Private Layer ===

DIR:
* Research/raw/, Research/x_posts/, Research/Topics/, Research/PDFs/,
  Research/evidence/: Raw sources → organized topics → hosted PDFs.
  PDFs we host on a page go in Research/PDFs/.
* knowledge/: Synthesized long-form analysis (FULL_WRITE_UP.md, the per-model
  Big_Write_up_*.md files, INTEL_Connections.md).
* Details/: Private per-person profiles. See the template above.
* ck/people/: Older per-person location, superseded by Details/.
* tmp/: Per-question research runs, one directory per line of inquiry
  (kill_me_research/, future_president_research/, groyper_research/,
  leader_of_churches_research/, ...). tmp/kill_me_research/ holds the KM-01..13
  research files behind the km-*-timeline.svg registry in timeslines.csv.
* SEO analysis, plans and prompts are PRIVATE and live outside this public repo in ~/BGit/all/politics/charlie_kirk/marketing/seo/ (moved 2026-09-26; analysis/seo.txt went there).
* Backup/: STALE — UX design page specs for an unrelated "backup viewer" app
  that drifted into this repo. Not part of the investigation.
* cover_image/: NanoBanana prompts and the generated OG social card. The site's
  docusaurus-social-card.jpg symlinks back to cover_image/cover.jpg.


=== External Tooling (outside this repo) ===

DIR:
* ~/BGit/all/politics/charlie_kirk/: The working/tooling side of this
  investigation. Holds prompts/, research/ (Google_Searches, podcast and Discord
  transcripts, Egyptoin_Flights, Shootings_Political), laws/ (law_fixes.txt,
  thomas_massey/), Letters/ (Tyler, Defense_Attorneys, Amicus), emails/,
  defemation/ (scan output + progress.txt), tweets/, podcasts/, info_graphics/,
  fort_hauchuca/, aiattorney/, ck_Marketing_Videos/, and offline/.
* ~/_Mirror/Politics/Charlie_Kirk_Mi/: Original source media files.
* ~/BGit/Bryan_git/personal_large_files_bridge/_Mirror/Politics/Charlie_Kirk_Mi/:
  The matching transcriptions, AI descriptions, and OCR text for those files.


