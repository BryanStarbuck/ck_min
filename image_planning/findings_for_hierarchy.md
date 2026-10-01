FINDINGS FOR THE HIERARCHY PLAN

Raised by the page-generation run of p_images_level2.md (2026-07-22). These are
data and clustering problems in ~/BGit/Bryan_git/charlie-kirk/images/images.yaml
(formerly image_planning/hierarchy_images.yaml). p_images_level2.md treats
that file as read-only input, so nothing here was fixed by that run — these are
for p_create_image_hierarchy.md (or a manual pass) to resolve.


== 0. PRIVATE PERSONAL MATERIAL IN THE HIERARCHY — ACTED ON, READ THIS FIRST ==

Eleven entries under Unfiled_Backlog are private personal documents that were
swept into the mirror by accident and have nothing to do with the
investigation. They were published as evidence pages with the image served
full-size at a public URL:

  * health savings account dashboard (balance, contribution summary, payment
    card details)
  * university student billing portal (completed transaction) x2
  * airline booking confirmation (confirmation codes)
  * private investment platform (payment history, capital call)
  * insurance / claims billing table
  * video-call participant list naming 15 people
  * 20-tile video conference grid showing participants' faces
  * internal video-production app screen and task spreadsheets x3

The written descriptions had been composed carefully so as not to repeat the
account numbers, addresses or names — but that is not protection when the
IMAGE ITSELF is the payload and is displayed at full size on a public page.

ACTION TAKEN by the page generation run: the 11 pages and their static image
copies under site/internals/static/img/evidence/ were deleted, and their
sha256 values recorded in image_planning/exclude_images.txt. The generator now
reads that file on every run: an excluded sha256 gets no page and no static
copy, and any existing copy is purged. The exclusion therefore survives
regeneration.

STILL TO DO HERE: the entries remain in images/images.yaml (formerly
hierarchy_images.yaml). They should be
removed from the YAML too, and the mirror directory reviewed for other private
material that the same sweep may have collected. The exclusion file is a
publish-time gate, not a cleanup.


== 1. OCR sidecars missing from the YAML (large, mechanical, high value) ==

619 .ocr sidecar files exist on disk but are not recorded in any image entry's
ocr_file property. Cause: the sidecar is named with a DIFFERENT image extension
than the source file.

  source:  .../Google_Search/N1098L_NCSS_CIA/Michael_Harlan_1.jpg
  sidecar: .../Google_Search/N1098L_NCSS_CIA/Michael_Harlan_1.png.ocr

Current YAML coverage: ocr_file set on 793 of 1604 local-file images (49%).
Recoverable by globbing <stem>.*.ocr instead of <full filename>.ocr: +619,
which would take coverage to about 88%.

This matters because OCR is the richest source for the screenshot-heavy corpus
(it carries the literal on-screen text). The writing agents worked around it by
probing the disk themselves, but the YAML should record the paths.

Note also: ai_description_file coverage is already good (1592 of 1604, 99%).


== 2. Media type is not recorded — 9 videos are filed as images ==

69 entries have an ipfs_url and no local file. Nine of those CIDs are .mp4
videos, not images; they sit in Official_Narrative/Narrative_Shot_in_the_Heart.
The YAML has no field distinguishing them.

The page generator now infers the type by looking at how each CID is embedded
on the site's own non-generated pages (<video>/<source> vs <img>/![]()), giving
60 images and 9 videos, and emits a <video> player for the videos. That
inference works but is indirect. The YAML should carry the media type outright
(e.g. a media_type or kind property, or a separate videos: array as the charter
already contemplates).


== 3. Duplicate images across clusters ==

Same sha256 filed in more than one cluster, producing two separate image pages
for one picture:

  * The 13 images under People/Skyler_Baird are the same files as the first 13
    images on the People parent node.
  * G2KSrP7WQAAE3-r.jpeg — in both MonoPod_Camera and UVU_Venue.
  * G05HU0DaUAEccgl — in both UVU_Venue and Construction.
  * G05w2sHaEAUGIKh — in both UVU_Venue and UVU_more.
  * sha 8f79b2 (rifle in a field) — filed under BOTH
    Table_Hand_off/Blake_Harruff_Plaid_Light and Table_Hand_off/Table_Other,
    under two different filenames, with a DIFFERENT unconfirmed person label
    attached in each place. This is the worst case of the pattern: one
    unverified photo appears to corroborate two separate identifications.
    Both pages now state the duplication explicitly.

Cross-filing is deliberate per the charter and is recorded in also_filed_in,
but a duplicated image should probably resolve to ONE page that is linked from
both clusters, rather than two pages of different prose about one picture.
Decide the rule and record it.


== 4. Placeholder and inconsistent cluster keys ==

  * other, TBD, Person_X — placeholder keys that became real published pages.
  * Mercel_Hat_Bedarz — looks like a typo (Bedarz vs Bednarz).
  * Conor_Dority — conflicts with the site's own spelling in
    site/docs/People/connor-dority.mdx (Connor).


== 5. Clusters built on unrelated source images ==

The Sanchez and Conor_Dority clusters are built on Fort Sill "Best Redleg"
US Army competition photographs, which have no established connection to this
case. The installation that actually recurs in Charlie_Kirk.txt is Fort
Huachuca. The generated pages state this explicitly rather than letting the
implication stand, but the clustering itself should be revisited.


== 6. Wrong AI descriptions — a recurring, systematic problem ==

The inline ai_description text is model output and is NOT reliable for identity
or location claims. Confirmed errors found while writing pages:

  * Truck_and_Back_of_Tent/10_Back_Hatch.jpg (sha 0de48d) — identifies the man
    in the white shirt as a foreign head of government. Plainly wrong.
  * Table_Hand_off/Hand_Off (sha ff022f) — described as the July 2024 Butler,
    Pennsylvania rally. It is the UVU courtyard; canopy text, hillside seating
    and neighbouring frames from the same clip prove it.
  * Ballistics_Gun/2_Cause_of_Death (sha aae3bf, 076535, 4e1c13) — three more
    images read by the model as the 13 July 2024 Butler rally.
  * Security_Team/Brian_Harpole_Bald (sha e44ed9) — names the wrong
    commentator as the host of the Prove Me Wrong table.

Note the Butler-rally confusion appears at least four times: the model
generalizes any outdoor political-rally protective response to Butler. Every
one of these pages was written to describe only what is visible, and the
mistaken reading was stated and corrected rather than propagated. A sweep of
inline descriptions for "Butler" and for named-person claims is worthwhile.


== 8. Images that do not belong to their cluster ==

  * Security_Team/Dan_Flood_Raybands (sha 5bd9cb) — a press photo of Benjamin
    and Sara Netanyahu on an airport tarmac, with no established link to the
    cluster's subject.
  * The Sanchez and Conor_Dority Fort Sill photographs (see item 5).
  * The ROOT Aircraft cluster carries a large block of unrelated material:
      - 5 Namecheap domain-registrar dashboard screenshots (no aircraft
        content at all)
      - 9 scanned pages of an unrelated 2019 ROMANIAN LEGAL COMPLAINT
        containing untested criminal allegations against named individuals.
        This is the highest-risk misfiling found anywhere in the corpus. The
        published pages give document type, date and provenance only and
        reproduce neither the names nor the allegations. It should be removed
        from the hierarchy, not merely described carefully.
      - 2 private "investigation dossier" app screenshots that label living
        people with roles and status markers
      - 1 basketball headshot, 1 robotic-dog demo photo, and 4 crowd frames
        from what appears to be a different gathering than September 10

The published pages say so plainly rather than inventing a connection, but the
filing should be corrected.


== 10. Evidence the hierarchy files as support that actually cuts the other way ==

Several images were clustered as if they corroborate a thesis when reading
their contents shows the opposite. The pages now state the real finding, but
the CLUSTERING still implies support. Worth restructuring:

  * Aircraft/Says_Wrong is a DEBUNK AUDIT of the circulating Egyptian-flight
    claims: 43 of 65 claims (66%) were found inaccurate and 60% placed the
    aircraft on a different continent. Only the Sept 4 / Sept 10 / Sept 13
    Provo rows survive. This disciplines the Egyptian-armada narrative rather
    than supporting it.
  * Aircraft sha 95fe57 — an AI chat in which the assistant's own reply states
    the N1098L crew names were "as provided in the fabricated details." That
    undercuts the N1098L_NCSS_CIA Google Trends sub-cluster, which should be
    filed as a documented negative result.
  * Aircraft sha 5d2a71 / 3549c2 — the N888KG owner's own public statements
    (pre-scheduled flight plan, two pilots and no passengers outbound, Page AZ
    pickup). Exculpatory, and previously undescribed.
  * Aircraft sha 024e37 (Duncan Aviation's publicly announced Egyptian Air
    Force maintenance contract, in place since 1999) and sha f4c26f (CENTCOM
    BRIGHT STAR 25 release dated Sept 8, 2025) are the two strongest innocent
    explanations in the Egyptian-aircraft thread.
  * Aircraft/Nwq sha 85d7bb — the menacing grey "HADES" jet that circulates
    online is an ARTIST'S RENDERING, not the white Global 6500 that flew over
    Utah.

Unresolved data discrepancy for the investigation: the N1098L callsign appears
as AXEL10 in Flightradar24 captures but AXLE10 in the drop-off slide deck and
the Perplexity screenshot.


== 12. Synthetic and rendered images filed as photographic evidence ==

Some entries are not photographs of anything that happened, and an evidence
hierarchy must not present them as if they were:

  * Several Shot_Position/Real_Shooter identification collages are
    AI-generated or synthetic composites rather than camera images.
  * Aircraft/Nwq sha 85d7bb — the grey "HADES" jet is an artist's rendering.
  * A Stew Peters chatbot output circulating as a claim about a named living
    person is model output, not evidence, and is described as such.

Each affected page states this explicitly. A media_provenance property
(photograph / screenshot / rendering / AI-generated / document scan) would let
the hierarchy carry this rather than relying on each page's prose.

Related accuracy notes recorded on-page rather than repeated as fact: a
generated roof-access aerial carries an obvious "11:35 PM" typo for a.m., and
the Greg Shaffer / "Schaffer" spelling differs between the filename and the
firm's actual name.


== 11. Route case-sensitivity trap ==

Site section directories are inconsistently cased: maps, court, cameras,
intelligence, laws, gov, security_law_enforcement are lowercase, while
Locations, Photos, Planes, People, FBI, UVU are capitalized. Links are
case-sensitive. Non-existent routes that look plausible and were tried by
multiple agents: /CIA/overview, /security/overview, /Maps/overview,
/timeline_events/overview, /laws/explain/overview.


== 9. Filenames that assert an identification the image cannot support ==

Some mirror filenames encode a claim that nothing in the picture establishes,
and the filename then propagates into the cluster and page title:

  * CIA_Intelligence/.../Senator_Huachuga (sha c3baec) — an uncaptioned
    official portrait. The filename asserts "Senator"; nothing in the image
    supports identifying anyone. The page names no one.
  * Patsy / Table_Hand_off person-labelled filenames generally — several
    attach an unconfirmed name to a face.

Filenames are filing intent, not evidence. Where the only basis for an
identification is the filename, the hierarchy should not carry it forward as a
title, and the page must not adopt it.


== 7. Empty and malformed sidecars ==

  * Five .ocr sidecars parse but carry text: "" (the vision pass returned
    nothing): G3qyLIIWkAAv7Zz.jpg, G3LjM2AW4AAmPbg.jpeg,
    G3LjP1MXYAAIHKp (1).jpeg, G3LjM2MXEAAuebJ (1).jpeg,
    G3LjM2LXIAAtJu8 (1).jpeg
  * Two .ocr sidecars contain their own YAML header duplicated inside the
    text: block: G3qYIv0WQAAXmqb.jpg.ocr, G3qYVQGXQAAZyjK.jpg.ocr
  * 13 host-page-derived images (IPFS-only, empty file_path) have no
    ai_description sidecar at all. Content was recovered from the host page's
    alt text and caption.


== 8. VIDEO PUBLISHED INSIDE THE IMAGE HIERARCHY — HAND-OFF TO videos_planning ==

Raised 2026-07-23. The images pipeline harvested, bound, and published VIDEO.
/Photos is the still-image Level 2; video belongs to the sibling pipeline
(videos/videos.yaml -> site/docs/Videos, Vid_*.mdx). Fixed at the source in the
same pass: p_update_image_hierarchy.md, p_yaml_to_site.md and
p_level2_update.md all now carry a MEDIA-TYPE SCOPE section, and
gen_photos_pages.py + bind_image_pages.py now gate on it. What is listed below
is the contamination those fixes step over — it is NOT yet cleaned up.

--- 8a. THE CAUSE ---

p_update_image_hierarchy.md Stage 7 said, verbatim:

    "Videos found on pages get entries too, as `video:` items with the same
     fields (video_list.csv ... is a starting index; the page scan is
     authoritative)."

gen_photos_pages.py then carried an is_video_src() test whose only effect was
to choose <video> markup instead of <img> on an Img_*.mdx page under /Photos.
Typing happened at RENDER time instead of at HARVEST time, so a video that got
into the YAML was guaranteed to be published rather than rejected.

--- 8b. CONTAMINATION IN images/images.yaml (measured, not estimated) ---

  * 53 `video:` array items across the tree. Never published (the generator
    only ever walked `images:`), but they are enriched by every stage and they
    are what Stage 13's "video entries: N" line was counting.
  * 9 `image:` items whose CID is in fact an .mp4 — ALL under the level_4 node
    _key Narrative_Shot_in_the_Heart. Each has sha256 "", file_path "", an
    ipfs_url, and one should_be_on_pages row pointing at
    site/docs/Narrative/Shot_in_the_heart.mdx. These are the ones that got
    published.
  * 0 other entries type as video. Verified by running the new gate over all
    1,687 `image:` entries: 1,678 publish, 9 video, 0 unknown, 0 false
    positives.

--- 8c. THE 9 PUBLISHED VIDEO PAGES (still live, left in place) ---

All under site/docs/Photos/Official_Narrative/Narrative_Shot_in_the_Heart/.
Each renders <video controls> off https://ipfs.io/ipfs/<CID>, carries
`ck_image_cid: none` frontmatter (a video entry has no sha256 to stamp), and
heads its write-up "## What This Image Shows".

  Img_Photo_Narrative_Shot_in_the_Heart_1.mdx  QmZHropnv47SNw2XBeaNNTfB8RAqv4nPcE1AbVTQNvdZJV
      TV Witness: One Shot Directly to the Heart
  Img_Photo_Narrative_Shot_in_the_Heart_2.mdx  QmZ3a5nC4DNY4duWqoJjchf5ZPKWon34it9uxwgCETkb9p
      On-Scene Witness: Right Where His Heart Is
  Img_Photo_Narrative_Shot_in_the_Heart_3.mdx  QmXSWJzgm6R5j7rWbubZgVu7y6NeMbwGHgttYzPo9Yaxhh
      Contrast Account: Blood Gushing From His Neck
  Img_Photo_Narrative_Shot_in_the_Heart_4.mdx  QmZZ4FQHmQvaMrpm1rP2EetjNK4NNfdux3hfCTmz6fd6zR
      Why Did Every Eyewitness Say Heart or Chest
  Img_Photo_Narrative_Shot_in_the_Heart_5.mdx  Qmdupxi4TifTuoMz25qHPMUxP3DVz7btycwvJ1rfZZKBpq
      Glenn Beck on Megyn Kelly: He Has a Pulse
  Img_Photo_Narrative_Shot_in_the_Heart_6.mdx  QmachmgMpySvi4cGpvpeHTDwS85PugUMY1M4NUARgyEHF2
      Speaker Advances the Body-Armor Fragmentation Theory
  Img_Photo_Narrative_Shot_in_the_Heart_7.mdx  QmfRuCtidKQfFuQpimhNFhw2tNo8CajDkpHS3Fpz7Pkr3e
      Frame Analysis Reposted With a Planted Allegation
  Img_Photo_Narrative_Shot_in_the_Heart_8.mdx  QmT5j43eoZcg83huMrAWJswkQke5ki2EYt8MBbCYsFBzq2
      Slow Motion: Ricochet Off the Vest Claim
  Img_Photo_Narrative_Shot_in_the_Heart_9.mdx  QmVGU5Cajy4jzWY9hDaFKg8m8niF3vwxND6L9661Fg3fxJ
      Reported Request That He Wear a Vest

These 9 pages are PROTECTED, not orphans. Their entries are now skipped by the
gate, so the orphan sweep would otherwise delete them on the next run —
gen_photos_pages.py now explicitly excludes any /Photos page containing a
<video>/<source>/<audio> element from orphan removal. They are written,
published pages with inbound links and no replacement under /Videos yet.

The write-ups are good and should not be thrown away. They are grounded in the
transcripts, they attribute claims rather than asserting them, and #7 in
particular is a defamation-sensitive page that was carefully handled. Migrating
them means moving the PROSE, not just the CID.

--- 8d. WHAT IS STILL TO DO (needs approval, not done here) ---

Sequenced so nothing is dark at any point:

  1. videos_planning picks these 9 up: cluster them in videos/videos.yaml
     (they are one coherent cluster — the wound-location / "shot in the heart"
     thread), carry the prose across, publish under site/docs/Videos.
  2. Verify each CID actually resolves on a PUBLIC gateway in a clean browser
     profile with no IPFS Companion. All 9 carry ipfs_pinned: false in
     images.yaml, so several may already be dead players today.
  3. Only then: remove the 9 pages from /Photos, redirect or repoint inbound
     links, drop the 9 `image:` entries and the 53 `video:` entries from
     images.yaml, and update pages.csv.

Nothing in step 3 has been done. Deleting a published page and rewriting the
YAML is outside what a scope-fix pass should do on its own.

--- 8e. TYPING RULE, FOR WHOEVER AUTOMATES THIS ---

Do NOT scrape CIDs wholesale out of the video pipeline's records to decide what
is a video. Measured: doing that types 70 image entries as video when only 9
are. videos/manifest.yaml and IPFS/ipfs.txt both describe a MIXED corpus (the
latter lists .jpg, .txt and .pdf blocks alongside .mp4), so parse both by
FILENAME. And videos/videos.yaml is not usable as an oracle yet at all — per
videos_planning/CLAUDE.md it is still a schema shell carrying the inherited
image corpus, so every cid in it currently describes an image.
