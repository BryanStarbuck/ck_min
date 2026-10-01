# Media, Images, Infographics — Full Rules

Moved verbatim out of {ROOT_DIR}/CLAUDE.md on 2026-09-24. ROOT_DIR = ~/BGit/Bryan_git/charlie-kirk, SITE_DIR = {ROOT_DIR}/site.

== Images Are Tracked In Git (never gitignore an image) ==

Image files MUST be committed to the repo. The live site is built by GitHub
Pages from the repo, not from any one machine, so an image that exists on disk
but is ignored or untracked renders perfectly in local dev and 404s for every
real visitor. These directories stay fully tracked:

  {ROOT_DIR}/images/                                   source images
  {SITE_DIR}/internals/static/img/evidence/            served as /img/evidence/<sha>.jpg
  {SITE_DIR}/internals/static/img/video_posters/       served as /img/video_posters/...

Videos are the deliberate exception: videos/* stays ignored and is pulled from
IPFS instead. That rule does NOT extend to images.

Never add a per-file image line to {ROOT_DIR}/.gitignore. The Large File Bridge
app has done this automatically in the past — it appended ~1,950 per-file lines
for the three directories above. Those were harmless for files already committed
(git never un-tracks a tracked file) but silently dropped every NEW image, which
shipped two broken embeds on the Rifle_Site_Kia_Soul_Turnaround page on
2026-08-12. All 1,951 lines were removed and a warning banner now sits at the
bottom of .gitignore. If those lines reappear, Large File Bridge has re-added
them — delete them again rather than working around them with `git add -f`.

The three legitimate ways to withhold an image:

  {ROOT_DIR}/images/.gitignore        Keep the bytes out of the repo entirely.
                                      Hand-curated, small, for private material.
  {BAN_IMAGES_CSV}                    Keep it off the public site (publish-time
                                      gate — see the next section).
  image_planning/exclude_images.txt   Legacy sha256 never-publish list.

Before publishing a page that embeds an image, verify both:

  git ls-files --error-unmatch <path>   # must succeed
  git check-ignore -v <path>            # must produce no output


== Never Embed An Image By IPFS Gateway URL ==

An image <img> src must ALWAYS be the local repo path:

  <img src="/img/evidence/{sha256}.jpg" data-cid="{CID}" />

Never src="https://ipfs.io/ipfs/{CID}". Most CIDs in manifest.yaml and videos.yaml
were produced with `ipfs add -n`, which computes the hash WITHOUT putting the bytes
on any node — so the gateway 504s for real visitors while the page renders perfectly
on the machine that happens to hold the file. Keep the CID in data-cid as the
provenance record; serve the bytes from the repo. Videos are the exception and do
use the gateway as their primary src.

Repo-wide check that every image is actually reachable by a visitor:

  python3 image_planning/generator/audit_image_publication.py            # fast
  python3 image_planning/generator/audit_image_publication.py --gateway  # also
                                     probes remaining ipfs.io <img> embeds

Exit 0 = clean; 1 = at least one image is unserved, on no page, or banned-but-served.
Banned and privacy-listed images are reported as WITHHELD, never as failures.
ck_add_text runs this at Step 9H-6b.


== Banned Media (ban_images.csv / ban_videos.csv) ==

BAN_IMAGES_CSV is file {ROOT_DIR}/images/ban_images.csv
BAN_VIDEOS_CSV is file {ROOT_DIR}/videos/ban_videos.csv

IMAGES_YAML is file {ROOT_DIR}/images/images.yaml
VIDEOS_YAML is file {ROOT_DIR}/videos/videos.yaml

These two CSV files list the images and videos we do NOT want shown on the
public site. They are the MASTER location for that decision. The YAML master
data files carry the decision as a property, but they carry it because it was
copied down out of the CSV — the CSV is the source of truth and the YAML is
downstream of it.

=== The banned Property ===

Every image entry in {IMAGES_YAML} carries:

    banned: true | false

Every video entry in {VIDEOS_YAML} carries:

    banned: true | false

The key is always present on every entry, always a real boolean, never null and
never a missing key — same rule as every other field in those files. Default is
false. An entry is banned: true only because a row for it exists in the CSV.

=== Direction Of Flow ===

    ban_images.csv  ──▶  images/images.yaml  ──▶  site/docs/Photos/ pages
    ban_videos.csv  ──▶  videos/videos.yaml  ──▶  site/docs/Videos/ pages

Edits go in the CSV. Never hand-edit banned: in the YAML — the next sync
overwrites it. Never treat the YAML as the place where the ban was decided.

=== CSV Format ===

Header row, then one row per banned item. Columns:

  sha256        The sha256 hex digest of the media file. Primary identity —
                survives renames, moves, and duplicate copies.
  cid           The IPFS CID ("Qm..." CIDv0) when one is assigned, else empty.
                Secondary identity: a video may have a cid and an empty sha256
                when the bytes are not on this machine.
  file_path     Full path from ~ to the file. For humans reading the CSV and as
                a last-resort match key. Not authoritative — files move.
  banned        true or false. Normally true. A row set to false is an explicit
                un-ban: the row stays as a record of the decision and its
                reason, and the item publishes normally.
  reason        Short plain-text reason (why we will not show this). Required.
  date_added    YYYY-MM-DD the row was added.

Match an entry by sha256 first, then cid, then file_path. Any match bans it.
An item with no row in the CSV is banned: false.

=== No Level 5 Page When Banned ===

When banned is true, there is NO Level 5 page for that item:

  * No page under {SITE_DIR}/docs/Photos/ for a banned image.
  * No page under {SITE_DIR}/docs/Videos/ for a banned video.
  * If such a page already exists, the generator DELETES it.
  * No served copy under {SITE_DIR}/internals/static/img/evidence/ (images) —
    delete it if present. A page that omits the accusation in its prose is not
    enough; the file itself must stop being served.
  * The item is removed from should_be_on_pages and must not be embedded on any
    other page anywhere on the site.
  * Any IPFS pinning job filters banned entries out before it pins. Pinning is
    public and irreversible in practice.

The entry itself is NEVER deleted from {IMAGES_YAML} or {VIDEOS_YAML}. Those
files only grow. Banning is a publish-time gate, so it survives every
regeneration of the hierarchy.

=== Relationship To The exclude_*.txt Files ===

  {ROOT_DIR}/image_planning/exclude_images.txt
  {ROOT_DIR}/videos_planning/exclude_videos.txt

These are the older sha256-per-line never-publish lists and they still work.
The CSV files are the newer, richer form: they carry the cid, the path, the
reason, the date, and a true/false switch instead of presence-in-a-file.

Treat the union as the ban set — an item listed in EITHER the CSV or the
matching exclude_*.txt is banned. New bans go in the CSV. Do not remove entries
from the exclude_*.txt files to "move" them; leave them and add the CSV row.

=== Keeping Them In Sync ===

Whenever a CSV changes, re-sync before generating pages:

  1. Read {BAN_IMAGES_CSV} / {BAN_VIDEOS_CSV}.
  2. Walk every entry in {IMAGES_YAML} / {VIDEOS_YAML} and set banned to match.
     Entries with no CSV row get banned: false.
  3. Verify the YAML still parses (yaml.safe_load) and contains no invisible
     Unicode.
  4. Re-run the page generators, which delete pages and served copies for
     newly banned items and keep {PAGES_CSV} in sync.

Safe programmatic edits to {IMAGES_YAML} reuse the emit/recount helpers in
image_planning/generator/bind_image_pages.py so the file round-trips
byte-for-byte; the video side uses videos_planning/generator/emit_yaml.py.


== Infographics (site/internals/static/img/infographics/) ==

INFO_GRAPHICS_DIR dir is {SITE_DIR}/internals/static/img/infographics/
NANO_BANANA_4K is file ~/BGit/all/tools/Nano_Banana_4K/nb_4k.js

MOVED 2026-08-28. This used to be {ROOT_DIR}/info_graphics/, which sat OUTSIDE
the site tree and so could not serve its own image — the picture had to be copied
to a second place before any page could show it. Everything moved whole into
{SITE_DIR}/internals/static/img/infographics/ and {ROOT_DIR}/info_graphics/ no
longer exists. Anything still naming the old path is stale. Only the LOCATION
changed; the goals.mdx and prompt contract below is unchanged.

`docusaurus.config.ts` sets `staticDirectories: ["internals/static"]`, so every
file under there is copied verbatim into the build and served from the site root:

  file    {SITE_DIR}/internals/static/img/infographics/{topic}/{topic}.jpg
  URL     /img/infographics/{topic}/{topic}.jpg

That is the only place in this repo where dropping an image in a directory makes
it fetchable at a stable URL with no import and no copy. An image left under
{SITE_DIR}/docs/ is NOT served that way — a literal <img src="..."> in MDX is not
processed by webpack, so it 404s for every real visitor while looking fine
locally. The goals and prompt files travel with the image and become fetchable
too; that is intended, so never put anything in one of these directories that is
not safe to publish.

Infographics are planned here before any image is generated. They are used across
the whole public site. One directory per infographic topic:

  {INFO_GRAPHICS_DIR}{topic}/
    goals.mdx                     The plan: audience, concept, framing, numbers,
                                  sizing, ordering, and the exact on-image text.
    nana_banana_pro_prompt.txt    The generation prompt, written FROM goals.mdx.

TOPIC is the directory name and behaves like a page key: one or two words,
underscores between them, no spaces and no special characters. Examples:
Following_Planes, Bullet_vs_Explosive, Sept10_Timeline, Erika_Overlaps.

When the infographic is about ONE AIRCRAFT, the directory is {TAIL}_{Type} — the
tail number plus the infographic type, same rules. There is normally one type per
plane and a plane may gain more types over time; one directory each, never two
graphics in one directory. Examples: N1098L_Flight_Record, N102DZ_Erased_Record,
SU_BTT_Ground_Contacts. Templates to copy from live in
{SITE_DIR}/docs/Planes/info_graphic/ and the rules for them are in
{SITE_DIR}/docs/Planes/CLAUDE.md, including the PLOTTED vs MODEL-GENERATED rule
that a generative model draws a plausible chart, not a real one.

Always 16:9. Always 2K. Every infographic on this site uses that shape so they
sit together consistently on the pages, and 2K is the readable-but-not-enormous
tier for a wide graphic embedded in a Docusaurus page.

=== goals.mdx — what it must contain ===

The first line of real content is the FULL PATH to the page the infographic is
being made for — the file we are targeting, from ~ or from {ROOT_DIR}. If it
targets more than one page, list every one of them.

Then these sections, in this order. Each is a real planning section, not a label:

  * Audience — who is looking at this. What they already believe, what they
    already know, and what they are scanning for.
  * What they should learn — the takeaway, stated as the sentence the reader
    should be able to say out loud after four seconds of looking.
  * Conceptual framing — how we frame it. The metaphor, the structure, the
    shape of the argument the picture makes.
  * What we are educating on — the actual content being taught.
  * Perspective — what the reader gets perspective ON. What they currently
    cannot see that this image makes visible.
  * Polarity and scope — the size of the thing. Are we zooming IN on one
    detail, or widening OUT to show scale? Often both, and the tension between
    the two is the graphic. Say how the zoom level is expressed visually.
  * Numbers — every number that appears, what it means, and how it is
    communicated (a big numeral, a count of repeated marks, a bar, a ratio).
    Numbers we deliberately leave out get named here too.
  * Sizing — what is bigger and what is smaller, and why. Size carries
    importance; state the importance ranking that drives it.
  * Framing and placement — what is frame left, what is frame right, what sits
    higher and what sits lower. What is inside a frame/box/card and what is
    unframed and bleeds. Timelines: say explicitly how time is expressed —
    left-to-right axis, stacked bands, a spiral, converging lines.
  * Screen percentages — roughly what share of the frame each concept takes.
    One concept might be 33%, another 22%. Assign these and reconcile them
    against the frame-left / frame-right decision above.

  These are GENERAL guidelines, not hard constraints. They exist to force the
  planning, not to be obeyed to the pixel.

  * Order of understanding — a NUMBERED list, most important first. Number 1
    introduces the concept and the issue the reader should be trying to
    understand. Number 2 is the first thing they should actually understand.
    Then 3, 4, 5. This ordering is what drives sizing and placement above:
    higher priority gets larger and lands where the eye goes first.
  * On-image text — every word that appears in the image. The title across the
    top, the subline if there is one, section labels, callouts, the source
    line. People scan; the title alone has to tell them what this is about.
    Phrase it deliberately and write the final wording here, not a description
    of the wording.

=== nana_banana_pro_prompt.txt — how to write it ===

Written from goals.mdx, after goals.mdx is finished. It is raw text — the whole
file is sent to the model as the prompt, so no markdown syntax, no headers, no
code fences. Prose and plain lines only.

It must carry everything the model needs: the layout, the framing and placement,
the relative sizing, the percentages, the visual treatment, the timeline
mechanics if there is one, and the EXACT text strings to render, quoted so the
model spells them correctly. State 16:9 in the prompt itself as well as passing
it on the command line.

=== Generating the image ===

  node {NANO_BANANA_4K} \
    {INFO_GRAPHICS_DIR}{topic}/nana_banana_pro_prompt.txt \
    {INFO_GRAPHICS_DIR}{topic}/{topic}.jpg \
    --size 2K --aspect 16:9

The tool defaults to 4K and 16:9, so --size 2K must be passed explicitly.
Uppercase K is required by the API. Model defaults to nano-banana-pro
(gemini-3-pro-image), which is the one that honours 2K/4K.

Once generated, the image is committed like any other site image — see
"Images Are Tracked In Git" above — and embedded by local repo path, never by
an IPFS gateway URL.

== Pages CSV ==

PAGES_CSV is file {ROOT_DIR}/pages.csv

This is the master index of every publicly visible page on the Docusaurus site.
It acts like a database table where each row is one page. Every skill that
creates or modifies site pages must keep this file in sync.

Path: {ROOT_DIR}/pages.csv

Columns:

  page_key        Unique identifier for the page (like a database primary key).
                  String with words and underscores, no special characters.
                  Four words or less. Descriptive enough to distinguish it from
                  sibling pages. Examples: Home, FBI, Fix_Law1, Charlie_Autopsy,
                  Israel_Foreign_Leads, trash_flight_records.

  parent_key      The page_key of this page's parent page. Empty only for the
                  home page (Level 1). Every other page must have a parent.
                  The parent is normally one level lower (e.g., a Level 3 page's
                  parent is the Level 2 overview of the same directory).

  level           Numeric hierarchy level:
                    1 = Home page (site root index.md) — only one
                    2 = Section overview pages (overview.md at depth 1)
                        and root-level standalone pages (Topics.md, etc.)
                    3 = Section child pages (non-overview at depth 1) and
                        sub-section overviews (overview.md at depth 2)
                    4 = Sub-section children (non-overview at depth 2) and
                        deeper overviews (overview.md at depth 3+)
                    5+ = Deeper nesting (rare)
                  A page's parent should normally be one level lower than itself.

  url_path        The public URL path visitors see. Relative to the site root.
                  Examples: /, /FBI, /Fix/Law1, /People/candace-owens.
                  Overview pages use the directory path (no /overview suffix).

  file_path       Relative path from the repo root to the markdown file.
                  Examples: site/docs/index.md, site/docs/FBI/overview.md.

  title           Page title extracted from frontmatter title field or first H1.

  sidebar_label   The label shown in the sidebar navigation. Falls back to title.

  directory       Parent directory path relative to site/docs/. Empty string for
                  root-level files.

  extension       File extension: md or mdx.

  has_frontmatter Whether the file has YAML frontmatter (yes/no).

  line_count      Total line count of the file.

Maintaining pages.csv:

  * When a skill creates a new page under site/docs/, add a row to pages.csv
    with all columns filled in. Generate a unique page_key (4 words max,
    underscores, no special chars). Set parent_key to the page_key of the
    parent overview page.

  * When a skill modifies a page (title change, file rename, level change),
    update the corresponding row in pages.csv.

  * When a skill moves or deletes a page, update or remove the row and fix
    any other rows that reference it as parent_key.

  * The CSV can be regenerated from scratch by walking site/docs/ and
    extracting metadata from each file. But incremental updates are preferred
    during skill runs to avoid losing manually adjusted page_keys.

Current stats (as of generation): 364 pages total.
  Level 1: 1, Level 2: 59, Level 3: 157, Level 4: 147.


== Details Directory (People Pages) ==

The Details/ directory is for private people profiles — one subdirectory per person
being investigated. Currently the ck/people/ directory holds some profiles (e.g.
Dustin_Bednarz/) but the canonical location going forward is Details/.

Each person gets a subdirectory: Details/{Person_Name}/

Files inside each person directory:

  * {Person_Name}.md           — Main profile. Contains:
    - Full name, DOB, location, occupation
    - Connection to the Charlie Kirk case
    - Family members and relationships
    - Key findings and evidence
    - Open questions
    - Sources with URLs

  * Research_{Person_Name}.md  — Extended research. Contains:
    - Deep-dive research notes
    - Social media accounts found
    - Employment history
    - Extended family tree
    - Court records, FOIA results
    - Research gaps still to fill

  * p_{Person_Name}.md         — Prompt template for AI-assisted research.
    Uses the standard prompt format (ROOT_DIR, variables, sections).
    Specifies what to research and where to output.

=== Detail Profile Template ===

When creating a new person profile, use this structure:

  # {Full Name}

  | Field | Value |
  |-------|-------|
  | Full Name | ... |
  | DOB | ... |
  | Location | ... |
  | Occupation | ... |
  | Connection to CK Case | ... |
  | Evidence Rating | CONFIRMED / MODERATE / EMERGING / SPECULATIVE |
  | Status | Alive / Deceased (YYYY) / Unknown |

  ## Connection to Charlie Kirk Case
  (How this person relates to the investigation)

  ## Background
  (Bio, career, family)

  ## Key Findings
  (Evidence discovered, organized by category)

  ## Family & Associates
  (Relationships, family tree, known associates)

  ## Open Questions
  (Numbered list of unresolved research items)

  ## Sources
  (URLs, documents, references)

=== Cross-Linking Between Pages ===

Private pages (Details/) can link to each other:
  * Same directory: [Person B](../Person_B/Person_B.md)
  * To public site page: reference the docs/ path but note it is public

Public pages (site/docs/) can link to each other:
  * Same directory: [Related Topic](./related-topic)
  * Different directory: [FBI Cover-Up](/FBI/overview)

Private pages NEVER link directly into the public site with relative paths.
Public pages NEVER link into private directories.


