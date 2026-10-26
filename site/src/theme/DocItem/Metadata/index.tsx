/**
 * Wrap of DocItem/Metadata: keeps the stock per-page title/description/og tags
 * and adds ONE per-page JSON-LD node that ties the page to the site-wide
 * WebSite + Organization @graph emitted from headTags in docusaurus.config.ts.
 *
 *   * Topic pages -> Article (headline, description, dateModified, image).
 *   * Home page and generated Photos/Videos item and cluster pages -> WebPage.
 *
 * dateModified comes from the page's git date (showLastUpdateTime), which is
 * honest only because the Pages workflow checks out full history.
 *
 * NEVER add Review, Rating, AggregateRating or ClaimReview here: on this site
 * they would read as a verdict about named living people.
 */
import React from "react";
import Head from "@docusaurus/Head";
import OriginalMetadata from "@theme-original/DocItem/Metadata";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import { useDoc } from "@docusaurus/plugin-content-docs/client";

// Generated photo pages of a law that was set aside ("disabled"): leftovers,
// 166-238 words each. Kept published so links into them still work, but
// noindex so search engines drop them (SEO problem
// fix_laws_disabled_photo_pages_public, 2026-10-26). Also excluded from the
// sitemap in docusaurus.config.ts. Files and images are kept.
const NOINDEX_PATHS = [/^\/Photos\/Fix_Laws\/disabled(\/|$)/];

export default function DocItemMetadata(): React.ReactElement {
  const { metadata, frontMatter, assets } = useDoc();
  const { siteConfig } = useDocusaurusContext();
  const site = siteConfig.url.replace(/\/$/, "");
  const url = site + metadata.permalink;
  const isMedia =
    metadata.permalink === "/" || /^\/(Photos|Videos)\//.test(metadata.permalink);
  const rawImage = (assets.image ?? frontMatter.image) as string | undefined;
  const image = rawImage
    ? /^https?:\/\//.test(rawImage)
      ? rawImage
      : site + (rawImage.startsWith("/") ? rawImage : "/" + rawImage)
    : undefined;
  const modified = metadata.lastUpdatedAt
    ? new Date(metadata.lastUpdatedAt).toISOString()
    : undefined;

  const node: Record<string, unknown> = {
    "@context": "https://schema.org",
    "@type": isMedia ? "WebPage" : "Article",
    "@id": `${url}#page`,
    url,
    mainEntityOfPage: url,
    inLanguage: "en-US",
    isPartOf: { "@id": `${site}/#website` },
    publisher: { "@id": `${site}/#organization` },
    ...(isMedia ? { name: metadata.title } : { headline: metadata.title.slice(0, 110) }),
    ...(metadata.description ? { description: metadata.description } : {}),
    ...(modified ? { dateModified: modified } : {}),
    ...(image ? { image } : {}),
  };
  if (!isMedia) {
    node.author = { "@id": `${site}/#organization` };
  }

  return (
    <>
      <OriginalMetadata />
      <Head>
        <script type="application/ld+json">{JSON.stringify(node)}</script>
        {NOINDEX_PATHS.some((re) => re.test(metadata.permalink)) ? (
          <meta name="robots" content="noindex, follow" />
        ) : null}
      </Head>
    </>
  );
}
