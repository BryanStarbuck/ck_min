/**
 * Swizzle of `DocItem/TOC/Desktop` — the right-hand "On this page" table of
 * contents on desktop. It renders NOTHING.
 *
 * This site has no right-hand table of contents on any page. The only thing on
 * the right edge is the citizen notice rail (see src/theme/Root.tsx). The TOC
 * used to be suppressed page by page through `hide_table_of_contents: true` in
 * front matter, which is an allow-list, and allow-lists miss pages — it kept
 * coming back on pages a generator or a hand-written file forgot.
 *
 * The primary removal is `markdown.parseFrontMatter` in docusaurus.config.ts,
 * which forces the flag on every doc so DocItem/Layout never asks for this
 * component and lays the content out full width. This file is the template
 * layer beneath that: even if a page somehow reached this component, it draws
 * nothing. Keep both.
 *
 * LOCATION: must live under <siteDir>/src/theme/ — see src/README_THEME.md.
 */
export default function DocItemTOCDesktop(): null {
  return null;
}
