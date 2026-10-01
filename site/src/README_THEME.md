# site/src/theme — why this directory exists here and nowhere else

This site keeps its source under `site/internals/src/`, not `site/src/`. There is
exactly one exception, and it is not a preference: **Docusaurus hardcodes the
component-swizzle lookup to `<siteDir>/src/theme`.** An override placed anywhere
else is silently ignored — the build succeeds, warns about nothing, and renders
nothing. That failure mode has already cost a day once. Do not "tidy" this
directory back under `internals/`.

## What is in here

    src/theme/Root.tsx                 the notice rail, as site chrome, on 100% of pages
    src/theme/DocItem/TOC/Desktop/     the "On this page" TOC, desktop — renders null
    src/theme/DocItem/TOC/Mobile/      the "On this page" TOC, mobile  — renders null
    src/theme/DocItem/Metadata/        wraps stock metadata; adds per-page Article/WebPage JSON-LD

`Root` is the Docusaurus wrapper that sits at the very top of the app, applied
constantly and independent of the current route. Declaring the rail there is
what makes it structural — the same layer as the navbar and the footer. There is
no page list, no front matter flag, and no generator, so there is no way for a
new page to miss it.

Supporting files, which live in the normal place:

    internals/src/components/CitizenNotice/   the rail's markup (no copy)
    internals/src/data/right_bar.json         the rail's wording, GENERATED
    internals/src/css/custom.css              CK_CITIZEN_NOTICE block: width,
                                              the reserved gutter, mobile shape

## Changing what the rail says

The wording has one source of truth, outside this repo:

    ~/BGit/all/politics/charlie_kirk/ck/docusaurus/right_bar.txt

Edit that file, then from the repo root run

    python3 tools/sync_right_bar.py

which rewrites `internals/src/data/right_bar.json`. Commit the JSON — the Pages
build cannot see the external file. The script only reads right_bar.txt; it never
writes to it. The first paragraph becomes the bold lead, the paragraph before the
email becomes the call to action, and the email becomes a `mailto:` link.

## There is no table of contents on this site — the rail is the only right-hand furniture

The Docusaurus "On this page" table of contents (the list of heading anchors
that used to scroll down the right side — "Claims from X posts", "Related",
"Images", ...) is removed on 100% of pages. It is NOT hidden page by page.
It used to be: `hide_table_of_contents: true` in front matter, which 5,157
pages carried and 1,575 did not, so the TOC kept reappearing on whichever pages
a generator or a hand-written file forgot the line (2026-09-15,
/Influencers/x/troofevades was one). A per-page flag is an allow-list, and
allow-lists miss pages. Three layers replace it, and all three stay:

  1. `markdown.parseFrontMatter` in `docusaurus.config.ts` forces
     `hide_table_of_contents: true` onto every doc at parse time. This is the
     one that matters for LAYOUT: `DocItem/Layout` only drops the 25%-wide right
     column when that flag is true, so this is what gives every page a
     full-width content column.
  2. `src/theme/DocItem/TOC/Desktop` and `.../Mobile` are swizzled to return
     null. Even a page that somehow reached the TOC component draws nothing.
  3. `internals/src/css/custom.css`, CK_NO_TOC block, hides
     `.theme-doc-toc-desktop` and `.theme-doc-toc-mobile`.

The `hide_table_of_contents: true` lines already in front matter are harmless
and were left alone; generators may keep writing them, but nothing depends on
them any more. Do not reintroduce a per-page mechanism for this.

The rail itself sits in a gutter reserved at the right edge of the page, outside
the content column, so nothing in the docs grid can push it or overlap it.

This replaced an earlier design (commit `635047b1`, 2026-09-04) that swizzled
`DocItem/Layout` and had the notice *take over* the TOC column on a generated
list of 100 pages — an allow-list that covered 100 of 5,916 pages. Both the
swizzle and its generator (`tools/gen_citizen_pages.py`,
`internals/src/citizenNoticePages.ts`) were deleted. Do not reintroduce a
per-page list for the rail either.

## On a Docusaurus upgrade

`Root.tsx` does not copy any upstream implementation — it renders `{children}`
plus the rail — so it does not drift with upstream and needs no re-diff. The
two TOC swizzles return null and copy nothing either. Things to re-check:

  * `.main-wrapper` and `.footer` are still the class names carrying the page
    body and the footer container, since the CSS reserves the gutter by
    padding them.
  * `DocItem/Layout` still keys the right column off
    `frontMatter.hide_table_of_contents`, and `DocItem/TOC/Desktop` and
    `DocItem/TOC/Mobile` are still the component paths it imports — if either
    moved, the TOC would come back on every page at once.
  * `markdown.parseFrontMatter` is still a supported config hook.

## MDXComponents.tsx (added 2026-09-27)

    src/theme/MDXComponents.tsx        wraps the stock MDX map; registers <UvuHouseReportCta />
                                       (internals/src/components/UvuHouseReportCta) so ~50 pages
                                       can use it with no import line.
