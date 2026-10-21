# Cover Image Update — Skill Prompt

## Purpose

Read the site's content and tone, update the Nano Banana image prompt, generate a new cover image, and wire it into Docusaurus as
the Open Graph image X.com, LinkedIn and Facebook show when any page is shared.

## Variables

```
REPO_ROOT         ~/BGit/Bryan_git/charlie-kirk
COVER_IMAGE_DIR   {REPO_ROOT}/cover_image
PROMPT_FILE       {COVER_IMAGE_DIR}/p_nb2_prompt.md
NANO_BANANA_JS    ~/BGit/all/tools/nano_banana_4k/nb_4k.js
SITE_DIR          {REPO_ROOT}/site
STATIC_IMG_DIR    {SITE_DIR}/internals/static/img
OG_IMAGE_FILE     {STATIC_IMG_DIR}/docusaurus-social-card.jpg
GENERATED_IMAGE   {COVER_IMAGE_DIR}/cover.jpg
```

## Step 1 — Understand the site

Read and extract:
- `{SITE_DIR}/docusaurus.config.ts`: title, tagline, siteUrl, staticDirectories, themeConfig.image
- `{SITE_DIR}/docs/index.md`: headline, primary subject, tone
- `{SITE_DIR}/sidebars.ts`: top-level sections
- three to five `overview.md` files from different topic dirs under `{SITE_DIR}/docs/`: themes, recurring subjects, angle

Summarize topic, emotional tone, domain URL, and visual motifs from existing `p_nb2_*.md` files in `{COVER_IMAGE_DIR}`.

## Step 2 — Update the image prompt

Rewrite `{PROMPT_FILE}` (replacing prior content):
- **Single paragraph** of dense, comma-separated visual directives; nothing else in the file (no markdown, headers, comments).
- **16:9 cinematic cover**, photorealistic, suitable as a hero banner and social card.
- **Tone**: investigative journalism; somber, serious, dignified; never sensationalist.
- **Domain embedded** as clearly legible text in the image (embossed plaque, brass plate, watermark, or document header).
- **No faces or violence**: no recognizable likeness, graphic violence, foreground weapons, or blood; distant silhouettes OK.
- Match the specificity and comma density of the other `p_nb2_*.md` files.

## Step 3 — Generate the image

```bash
node {NANO_BANANA_JS} {PROMPT_FILE} {GENERATED_IMAGE} --size 2K --aspect 16:9
```

The tool reads its key from `~/.config/GoogleCloud/apikey.yaml` (`4k_apiKey`, fallback `apiKey`; never print it). Run `--help` if
flags are unclear. On error, print it and stop before Step 4.

## Step 4 — Wire up the Open Graph image

`themeConfig.image: "img/docusaurus-social-card.jpg"` resolves against the static dir, so the file must exist at build time at
`{OG_IMAGE_FILE}` (platforms read the injected `og:image` tag and fetch that URL). Use a **relative** symlink to avoid duplication:

```bash
rm -f {OG_IMAGE_FILE}
# from site/internals/static/img/ up four levels to repo root, then into cover_image/
ln -s ../../../../cover_image/cover.jpg {OG_IMAGE_FILE}
```

Already a symlink to `{GENERATED_IMAGE}`: skip. A symlink elsewhere or a plain file: remove and recreate. Missing: create.

## Step 5 — Verify

1. `{GENERATED_IMAGE}` exists and is larger than 10 KB.
2. `{OG_IMAGE_FILE}` is a symlink resolving to `{GENERATED_IMAGE}`.
3. `file {GENERATED_IMAGE}` reports a valid JPEG or PNG.
4. `{SITE_DIR}/docusaurus.config.ts` still contains `image: "img/docusaurus-social-card.jpg"`; note any discrepancy.

## Step 6 — Report

Prompt used (first 200 characters), output path and size, symlink status (created / updated / already correct), warnings.
