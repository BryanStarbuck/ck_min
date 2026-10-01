/**
 * Swizzle of `DocItem/TOC/Mobile` — the collapsible "On this page" box shown
 * above the article on narrow viewports. It renders NOTHING.
 *
 * Same policy and same reasoning as ../Desktop/index.tsx: this site has no
 * table-of-contents widget on any page, the primary removal is the
 * `markdown.parseFrontMatter` hook in docusaurus.config.ts, and this null
 * component is the template-layer guarantee beneath it.
 *
 * LOCATION: must live under <siteDir>/src/theme/ — see src/README_THEME.md.
 */
export default function DocItemTOCMobile(): null {
  return null;
}
