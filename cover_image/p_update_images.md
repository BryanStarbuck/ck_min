# Cover Image Update — Skill Prompt

## Purpose

Walk the Docusaurus site directory for this repo, understand its content and tone,
update the NanoBanana 2 image prompt, generate a new cover image, and wire it into
Docusaurus so that X.com, LinkedIn, and Facebook show the correct Open Graph image
when any page on the site is shared.

## Variables

```
REPO_ROOT         ~/BGit/Bryan_git/charlie-kirk
COVER_IMAGE_DIR   {REPO_ROOT}/cover_image
PROMPT_FILE       {COVER_IMAGE_DIR}/p_nb2_prompt.md
NANO_BANANA_JS    /Users/bryanstarbuck/BGit/work/tools/Nano_Banana/nano_b.js
SITE_DIR          {REPO_ROOT}/site
STATIC_IMG_DIR    {SITE_DIR}/internals/static/img
OG_IMAGE_FILE     {STATIC_IMG_DIR}/docusaurus-social-card.jpg
GENERATED_IMAGE   {COVER_IMAGE_DIR}/cover.jpg
```

## Step 1 — Understand the Docusaurus site

Read each of the following files. Extract the key facts noted in parentheses.

- `{SITE_DIR}/docusaurus.config.ts`
  → site title, tagline, siteUrl, staticDirectories, themeConfig.image path
- `{SITE_DIR}/docs/index.md`
  → landing page headline, primary investigation subject, tone
- `{SITE_DIR}/sidebars.ts`
  → top-level section names
- Three to five `overview.md` files from different topic directories under
  `{SITE_DIR}/docs/`
  → key themes, recurring subjects, investigative angle

Summarize what you learn: the site's topic, its emotional tone (investigative,
somber, journalistic, urgent, etc.), the domain URL, and any visual motifs already
referenced in existing `p_nb2_*.md` prompt files in `{COVER_IMAGE_DIR}`.

## Step 2 — Update the image prompt

Rewrite `{PROMPT_FILE}` with a refined NanoBanana 2 image generation prompt.

Rules for the prompt file content:
- **Single paragraph** — dense, comma-separated visual directives with no line breaks
  inside the paragraph. The file contains only this paragraph; no markdown, no headers,
  no comments.
- **16:9 cinematic cover image** — photorealistic, 2 megapixels, suitable as a website
  hero banner and social card.
- **Tone matches the site** — investigative journalism; somber, serious, dignified.
  Never sensationalist, never tabloid.
- **Site domain embedded** — the site's domain URL must appear as legible text inside
  the image: embossed plaque, brass plate, watermark, or document header. Always
  clearly readable.
- **No faces or violence** — no recognizable human likeness, no graphic violence,
  no weapons in foreground, no blood. Distant silhouettes are acceptable.
- **Use existing prompts as style reference** — read any other `p_nb2_*.md` files in
  `{COVER_IMAGE_DIR}` and match their level of visual specificity and comma density.

Write the new prompt to `{PROMPT_FILE}`, replacing any prior content.

## Step 3 — Generate the image

Run the NanoBanana 2 image generator:

```bash
node {NANO_BANANA_JS} {PROMPT_FILE} {GENERATED_IMAGE}
```

- Arg 1: absolute path to the prompt file
- Arg 2: absolute path for the output image (inside `{COVER_IMAGE_DIR}`)

The tool reads the API key from `~/.config/GoogleCloud/apikey.yaml` (field
`4k_apiKey` for Nano Banana Pro, fallback to `apiKey`). It writes the generated
image to `{GENERATED_IMAGE}`.

If the tool exits with an error, print the error and stop — do not proceed to
Step 4.

## Step 4 — Wire up the Docusaurus Open Graph image

Docusaurus reads `themeConfig.image` from `docusaurus.config.ts`. The value
`"img/docusaurus-social-card.jpg"` is resolved relative to the static directory
(`{STATIC_IMG_DIR}`), so Docusaurus expects the file at:

```
{OG_IMAGE_FILE}
```

When a page is shared on X.com, the platform fetches the page HTML, reads the
`og:image` meta tag that Docusaurus injects, and loads the image from that URL.
The image must exist in the static directory at build time.

To avoid duplicating the file, create a symlink using a **relative** path:

```bash
# Remove whatever exists at the target location
rm -f {OG_IMAGE_FILE}

# Create a relative symlink from the static img dir back to cover_image/
# Relative path: from site/internals/static/img/ up four levels to repo root,
# then into cover_image/
ln -s ../../../../cover_image/cover.jpg {OG_IMAGE_FILE}
```

Check before creating:
- If `{OG_IMAGE_FILE}` already exists as a symlink pointing to `{GENERATED_IMAGE}`:
  skip (already correct)
- If it exists as a symlink pointing elsewhere, or as a plain file: remove and recreate
- If it does not exist: create it

## Step 5 — Verify

1. Confirm `{GENERATED_IMAGE}` exists and is larger than 10 KB.
2. Confirm `{OG_IMAGE_FILE}` is a symlink that resolves to `{GENERATED_IMAGE}`.
3. Run `file {GENERATED_IMAGE}` to confirm it is a valid JPEG or PNG.
4. Check that `{SITE_DIR}/docusaurus.config.ts` still contains
   `image: "img/docusaurus-social-card.jpg"` — if the config was changed by
   someone else, note the discrepancy.

## Step 6 — Report

Print a short summary:
- Prompt used (first 200 characters)
- Output image path and file size
- Symlink status (created / updated / already correct)
- Any warnings or issues
