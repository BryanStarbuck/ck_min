// Swizzle (wrap) of the MDX component map. Must live in site/src/theme — see
// ../README_THEME.md. Adds components every .mdx page can use without an import.
import MDXComponents from '@theme-original/MDXComponents';
import UvuHouseReportCta from '@site/internals/src/components/UvuHouseReportCta';

export default {
  ...MDXComponents,
  UvuHouseReportCta,
};
