ROOT_DIR dir is ~/BGit/Bryan_git/charlie-kirk

IMAGES_DIR dir is {ROOT_DIR}/images

IMAGES_YAML is file {IMAGES_DIR}/images.yaml

PLANNING_DIR dir is {ROOT_DIR}/image_planning

GENERATOR_DIR dir is {PLANNING_DIR}/generator

SITE_DIR dir is {ROOT_DIR}/site

PHOTOS_DIR dir is {SITE_DIR}/docs/Photos

PAGES_CSV is file {ROOT_DIR}/pages.csv

EXCLUDE_FILE is file {PLANNING_DIR}/exclude_images.txt

MIRROR_DIR dir is ~/_Mirror/Politics/Charlie_Kirk_Mi


== What This Directory Is ==

{IMAGES_DIR} holds image files used by the investigation, and it is now also the
home of {IMAGES_YAML} — the master list of every image.


== images.yaml — The Master Image List ==

{IMAGES_YAML} is THE master location list of all images in the investigation,
and it carries a large amount of information about each one. It is the single
authoritative index. When anything needs to know what images exist, where they
are, what is in them, or which page they belong to, the answer comes from this
file.

=== Moved Here — New Name, New Location ===

This file used to be {PLANNING_DIR}/hierarchy_images.yaml. It was moved on
2026-07-22 and renamed:

  OLD: ~/BGit/Bryan_git/charlie-kirk/image_planning/hierarchy_images.yaml
  NEW: ~/BGit/Bryan_git/charlie-kirk/images/images.yaml

Both the old name and the old location are dead. Anything still referring to
"hierarchy_images.yaml", or looking for the YAML under image_planning/, is
stale and should be pointed at {IMAGES_YAML}.

The prompts and scripts that read and write it still live in {PLANNING_DIR} and
{GENERATOR_DIR} — only the data file moved.

=== What It Records ===

For every image it is the master record of:

  * Where the image lives — the file path, including images under {IMAGES_DIR}
    and the wider corpus under {MIRROR_DIR}.
  * Identity that survives moves, renames, and duplicates — sha256, content
    fingerprint, and the IPFS CID where one is assigned.
  * What is visually in the image — the AI description, plus the paths to the
    sidecar files (.ai_description, .ocr, .transcription) that Large File Bridge
    generates.
  * Where it belongs in the investigation — the concept cluster it sits in, and
    the site page that cluster maps to.

Videos are carried in the same tree with the same fields.

=== Shape ===

The file is a hierarchy of concept clusters starting at level_3 (level_1 is the
site home, level_2 is the /Photos landing page). Each cluster node carries
title, _key, number_of_images, an images array, and optionally a nested
level_4 / level_5 array. Each image entry carries the identity and description
fields listed above.

Full schema, clustering rules, and the six-to-twelve images-per-page rule are
documented in {PLANNING_DIR}/CLAUDE.md. That charter is the authority on
structure; this file is the authority on location.

=== Who Reads And Writes It ===

  * Written / grown by: {GENERATOR_DIR}/grow_hierarchy.py and
    {GENERATOR_DIR}/fixup_hierarchy.py, driven by
    {PLANNING_DIR}/p_create_image_hierarchy.md. Grow-only — nodes and image
    entries are never deleted.
  * Read by: {GENERATOR_DIR}/gen_photos_pages.py, which generates the published
    pages under {PHOTOS_DIR} and keeps {PAGES_CSV} in sync. The page generator
    treats {IMAGES_YAML} as READ-ONLY.
  * Publish gate: {EXCLUDE_FILE}. An sha256 listed there gets no page and no
    served copy, even though its entry stays in {IMAGES_YAML}. Exclusion is
    enforced at publish time so it survives every regeneration.


== Rules ==

  * {IMAGES_YAML} is data, not a published page. Never put Docusaurus pages in
    {IMAGES_DIR}, and never put planning prompts here — those belong in
    {PLANNING_DIR}.
  * The file only grows. Do not delete nodes or image entries.
  * It must never contain invisible Unicode characters, and it must always parse
    as valid YAML — verify with a yaml.safe_load after any write.
  * Anything published from it under {PHOTOS_DIR} follows the repo's defamation
    rules: no stating as fact that a living person committed a crime,
    attribution language throughout, presence only for named living people, and
    accusations cropped out of images.
