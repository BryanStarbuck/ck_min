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
      </Head>
    </>
  );
}
