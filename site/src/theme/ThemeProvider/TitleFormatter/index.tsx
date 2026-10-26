/**
 * Title formatter: keeps every <title> (and og:title) within 60 characters.
 *
 * Stock Docusaurus appends " | Who Assassinated Charlie Kirk" (32 characters)
 * to every page title, so any page title over 28 characters was cut off in
 * Google results (348 of 455 pages, SEO crawl 2026-10-26). The rule: keep the
 * site suffix when the full title still fits in 60 characters; otherwise show
 * the page's own title alone. A page's own title text is never changed.
 *
 * Lives under site/src/theme (not internals/) because Docusaurus only looks
 * for swizzled components there; see ../../README_THEME.md.
 */
import React, { type ReactNode } from "react";
import { TitleFormatterProvider } from "@docusaurus/theme-common/internal";

const MAX_TITLE = 60;

type FormatterParams = Parameters<
  React.ComponentProps<typeof TitleFormatterProvider>["formatter"]
>[0];

const formatter = (params: FormatterParams): string => {
  const full = params.defaultFormatter(params);
  const own = params.title?.trim();
  if (!own || own === params.siteTitle || full.length <= MAX_TITLE) {
    return full;
  }
  return own;
};

export default function ThemeProviderTitleFormatter({
  children,
}: {
  children: ReactNode;
}): ReactNode {
  return <TitleFormatterProvider formatter={formatter}>{children}</TitleFormatterProvider>;
}
