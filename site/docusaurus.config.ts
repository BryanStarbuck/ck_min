import { themes as prismThemes } from "prism-react-renderer";
import type { Config } from "@docusaurus/types";
import type * as Preset from "@docusaurus/preset-classic";

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const siteUrl = process.env.DOCUSAURUS_URL ?? "https://whoassassinatedcharliekirk.com";
const baseUrl = process.env.DOCUSAURUS_BASE_URL ?? "/";

const siteTitle = "Who Assassinated Charlie Kirk";
const siteTagline = "Investigating the September 10, 2025 assassination at Utah Valley University";
const siteDescription =
  "Citizen-led investigation into the September 10, 2025 assassination of Charlie Kirk at Utah Valley University: evidence, timelines, suspects, intelligence-service connections, and proposed legal reforms.";
const socialCard = "img/docusaurus-social-card.jpg";

const config: Config = {
  title: siteTitle,
  tagline: siteTagline,
  favicon: "img/favicon.ico",
  staticDirectories: ["internals/static"],
  // Skips an IPFS video to its next gateway when one stalls instead of erroring.
  clientModules: ["./internals/src/clientModules/ipfsVideoFallback.js"],

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
    // v4 defaults to the "git-eager" strategy: one `git log --name-status` over the
    // whole repo, read into a hardcoded 20 MB buffer. The 2026-10-01 commit that
    // removed 62 Level 2 sections (69,583 files) pushed that log to ~25 MB and
    // every build failed with MaxBufferError. "git-ad-hoc" runs git log per doc.
    experimental_vcs: "git-ad-hoc",
  },

  // future.v4 turns OFF the legacy admonition title form `:::caution Legal Disclaimer`
  // (space before the title). 742 pages use that form, and with it off they render as
  // raw ":::caution ..." paragraph text. Keep it on until every page uses
  // `:::caution[Legal Disclaimer]`.
  markdown: {
    mdx1Compat: {
      admonitions: true,
    },
    // NO RIGHT-HAND TABLE OF CONTENTS, ON ANY PAGE. This site's only right-hand
    // furniture is the citizen notice rail (site/src/theme/Root.tsx). The
    // Docusaurus "On this page" TOC used to be hidden per page with
    // `hide_table_of_contents: true` in front matter — 5,157 pages carried it
    // and 1,575 did not, so the TOC kept reappearing on whichever pages a
    // generator or a hand-written file forgot the line. This hook forces the
    // flag on every doc at parse time, so DocItem/Layout treats every page as
    // TOC-hidden (no TOC, full-width content column) with no per-page list to
    // fall out of date. Second and third layers: src/theme/DocItem/TOC/* render
    // null, and custom.css (CK_NO_TOC) hides the TOC classes.
    parseFrontMatter: async (params) => {
      const result = await params.defaultParseFrontMatter(params);
      result.frontMatter.hide_table_of_contents = true;
      return result;
    },
  },

  // Set the production url of your site here
  url: siteUrl,
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl,
  trailingSlash: false,

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: "ACT3ai", // Usually your GitHub org/user name.
  projectName: "charlie-kirk", // Usually your repo name.

  onBrokenLinks: "warn",

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: "en",
    locales: ["en"],
  },

  // Global head tags for SEO: language, JSON-LD structured data (Organization +
  // WebSite), and rich social cards. Per-page descriptions are set via
  // frontmatter and override these defaults. Canonical URLs are emitted
  // per-page by Docusaurus automatically — never add a site-wide canonical
  // here, or every page will canonicalize to the homepage and be deindexed.
  headTags: [
    // Snippet/preview directives ONLY — never "index, follow" here. index,follow is
    // the default, and a site-wide copy contradicts the per-page noindex Docusaurus
    // emits on /404 and on every client-redirect stub (two robots tags in one head).
    {
      tagName: "meta",
      attributes: {
        name: "robots",
        content: "max-image-preview:large, max-snippet:-1, max-video-preview:-1",
      },
    },
    {
      tagName: "meta",
      attributes: {
        property: "og:site_name",
        content: siteTitle,
      },
    },
    // No og:locale here: theme-classic already emits one per page.
    // One WebSite node + one Organization node. No SearchAction: the sitelinks
    // searchbox was retired (Nov 2024) and /search is disallowed in robots.txt.
    {
      tagName: "script",
      attributes: {
        type: "application/ld+json",
      },
      innerHTML: JSON.stringify({
        "@context": "https://schema.org",
        "@graph": [
          {
            "@type": "WebSite",
            "@id": `${siteUrl}/#website`,
            name: siteTitle,
            url: siteUrl,
            description: siteDescription,
            inLanguage: "en-US",
            publisher: { "@id": `${siteUrl}/#organization` },
          },
          {
            "@type": "Organization",
            "@id": `${siteUrl}/#organization`,
            name: siteTitle,
            url: siteUrl,
            logo: `${siteUrl}/img/Header_Charlie.jpeg`,
          },
        ],
      }),
    },
  ],

  plugins: [
    [
      "@docusaurus/plugin-client-redirects",
      {
        // Redirect every bare directory path to its overview page so external
        // backlinks like /Fix or /Tyler_Robinson land on real content instead
        // of GitHub Pages' 301-then-404 chain.
        createRedirects(existingPath: string) {
          const from: string[] = [];
          if (existingPath.endsWith("/overview")) {
            const parent = existingPath.replace(/\/overview$/, "");
            if (parent !== "") {
              from.push(parent);
            }
          }
          // The photo cluster formerly published under /Photos/Table_Hand_off.
          // It was renamed to /Photos/Table_And_Charlie (with the Hand_Off and
          // Lady_Hand_Off sub-clusters renamed too) to drop wording that implied
          // anyone deliberately passed an object. Map every old path forward so
          // existing backlinks keep resolving.
          if (existingPath.startsWith("/Photos/Table_And_Charlie")) {
            const old = existingPath
              .replace("/Photos/Table_And_Charlie", "/Photos/Table_Hand_off")
              .replace("/At_The_Table", "/Hand_Off")
              .replace("/Woman_At_Table", "/Lady_Hand_Off")
              .replace("/Img_Table_Item_60dcfa", "/Img_Hand_Off_Item_60dcfa");
            from.push(old);
            if (old.endsWith("/overview")) {
              from.push(old.replace(/\/overview$/, ""));
            }
          }
          return from.length ? from : undefined;
        },
        // Pages Google still has indexed but that have been moved or removed.
        // Each entry generates a static HTML stub that meta-refreshes to `to`.
        redirects: [
          // Cabot alibi moved under the new Fort Huachuca Level 3 cluster.
          // Autopsy cluster moved Charlie/Autopsy -> Medical/Autopsy (c9ecfe6de,
          // 2026-06-26). /Charlie/Autopsy is still in search indexes and was 404ing.
          // The two targets behind 33 of the build's 34 "Broken link" warnings
          // (19 generated Photos pages + 14 others link to them). Docusaurus strips
          // the "911-" filename prefix as a sidebar-ordering number, and the
          // mirandize hub's route is mirandize-overview.
          { from: "/court/mirandize/overview", to: "/court/mirandize/mirandize-overview" },
          // Duplicate video pages folded into one when the videos were upgraded to
          // higher-resolution copies (2026-09-26); the surviving page holds the same video.
        ],
      },
    ],
  ],

  presets: [
    [
      "classic",
      {
        docs: {
          routeBasePath: "/",
          sidebarPath: "./sidebars.ts",
          // Path to the source file inside the repo. Docs live in site/docs,
          // and the generated edit URL is appended with the relative path of
          // each source file. Without /edit/main/site/ every page emitted a
          // github.com 404 link that GSC was reporting as a broken outbound.
          editUrl: "https://github.com/ACT3ai/charlie-kirk/edit/main/site/",
          showLastUpdateTime: true,
          exclude: [
            "**/_*.{js,jsx,ts,tsx,md,mdx}",
            "**/_*/**",
            "**/*.test.{js,jsx,ts,tsx}",
            "**/__tests__/**",
            "**/prompts/**",
            "**/CLAUDE.md",
            // Prompt files (agent instruction sets) living inside docs
            // directories are private — never publish them as pages.
            "**/p_*.{md,mdx}",
            // Raw weekly Grok X-search dumps (speaking/week/{year}/week_NN.md).
            // Research files, not published pages — a tweet `{` would break MDX.
            "**/Planes/following/speaking/week/**",
          ],
        },
        blog: false,
        pages: {
          path: "internals/src/pages",
        },
        theme: {
          customCss: "./internals/src/css/custom.css",
        },
        sitemap: {
          // Google and Bing ignore changefreq/priority; uniform values carry no
          // information. lastmod is honest only because the Pages workflow does a
          // full-history checkout (fetch-depth: 0) — a shallow clone stamps every
          // URL with the build date.
          changefreq: null,
          priority: null,
          lastmod: "date",
          // /404 — noindex page, must never appear in sitemap.
          // /Tyler/**, /Plane/**, /Topics3/**, /CIA/** — old directory paths
          //   that only exist as plugin-client-redirects stubs; they carry
          //   noindex and a meta-refresh, so Google marks them as
          //   "Excluded by noindex" and "Page with redirect".
          // /aircraft_flight_analysis/**, /Killer/Planes_Drones_Theories,
          //   /Israel/israel-planes, /Before/PreEvent_Flights_And_Travel,
          //   /Influencers/podcasts-project-costa-2 — explicit redirect sources.
          ignorePatterns: [
            "/tags/**",
            "/404",
            "/404.html",
            "/404/",
            "/Tyler/**",
            "/Plane/**",
            "/Topics3/**",
            "/CIA/**",
            "/aircraft_flight_analysis/**",
            "/Killer/Planes_Drones_Theories",
            "/Israel/israel-planes",
            "/Before/PreEvent_Flights_And_Travel",
            "/Influencers/podcasts-project-costa-2",
            "/Charlie/Autopsy",
            "/Charlie/Autopsy/**",
            "/court/mirandize/overview",
            "/Witnesses/911-calls-rooftop-witness",
            "/Videos/Vid_Gov_Mind_Control/Vid_Mkultra_Mind_Control/Vid_Professor_Example_nUPwPTC",
            "/Videos/Vid_US_Intelligence/Vid_CIA_Archive_Video/Vid_Original_Fixed_High_Q_n4m8oYt",
            "/Videos/Vid_US_Intelligence/Vid_CIA_Footage/Vid_Full_Drone_2025_Oct_hoQ1YxX",
          ],
          // Filter out redirect stubs generated by plugin-client-redirects.
          // createRedirects creates a stub at every parent path of an /overview
          // page (e.g., /Fix → /Fix/overview). Those stubs carry noindex +
          // meta-refresh, so Google reports them as "Excluded by noindex" and
          // "Page with redirect". Exclude them from the sitemap so Google
          // does not surface them as submitted-URL errors.
          createSitemapItems: async (params) => {
            const { defaultCreateSitemapItems, ...rest } = params;
            const items = await defaultCreateSitemapItems(rest);
            const itemUrls = new Set(items.map((item) => item.url));
            return items.filter((item) => {
              // If path + "/overview" is itself a sitemap URL, this item is a
              // redirect stub (parent directory), not real content — exclude it.
              const candidateOverview = item.url.replace(/\/?$/, "/overview");
              return !itemUrls.has(candidateOverview);
            });
          },
          filename: "sitemap.xml",
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Default social card used by Open Graph / Twitter when a page has no own image
    image: socialCard,
    // ONLY values that are genuinely identical on every page belong here.
    // theme-classic renders themeConfig.metadata in a LATER <Head> than each
    // page's own tags, so anything per-page placed here overwrites every page.
    // Measured 2026-09-26: og:url was the homepage on 5,651 of 5,652 pages and
    // twitter:title/description were the site-wide strings, so every interior
    // page shared on X unfurled as the homepage. og:url, og:title, og:image,
    // twitter:image and description are emitted per page by Docusaurus; X falls
    // back to og:title/og:description when twitter:title/description are absent.
    metadata: [
      { name: "twitter:card", content: "summary_large_image" },
      { property: "og:type", content: "website" },
    ],
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: "Who Assassinated Charlie Kirk",
      logo: {
        alt: "Who Assassinated Charlie Kirk - investigation site logo",
        src: "img/Header_Charlie.jpeg",
      },
      items: [
        { to: "/Fix/overview", label: "Charlie Kirk Laws", position: "left" },
        { to: "/Cause_of_Death/overview", label: "Cause of Death", position: "left" },
        { to: "/Mic/overview", label: "The Microphone", position: "left" },
        { to: "/court/overview", label: "Court & Trial", position: "left" },
        { to: "/Your_Actions_Fix_It/overview", label: "Your Actions Fix It", position: "left" },
      ],
    },
    // Footer links render on every page (5,600+), so they are the strongest
    // internal links the hubs get, and they put the About/Methodology page (the
    // site's trust page for this YMYL topic) one click from everywhere.
    footer: {
      style: "dark",
      links: [
        {
          title: "The Evidence",
          items: [
            { label: "Timeline", to: "/Timeline/overview" },
            { label: "Cause of Death", to: "/Cause_of_Death/overview" },
            { label: "The Microphone", to: "/Mic/overview" },
            { label: "Maps", to: "/maps/overview" },
          ],
        },
        {
          title: "The Case",
          items: [
            { label: "Court & Trial", to: "/court/overview" },
            { label: "Legal", to: "/Legal/overview" },
            { label: "Media", to: "/Media/overview" },
            { label: "Google Searches", to: "/GoogleSearches/overview" },
          ],
        },
        {
          title: "Take Action",
          items: [
            { label: "New Laws (Fix)", to: "/Fix/overview" },
            { label: "Your Actions Fix It", to: "/Your_Actions_Fix_It/overview" },
          ],
        },
        {
          title: "About",
          items: [
            { label: "Report a Correction", href: "https://github.com/ACT3ai/charlie-kirk/issues" },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()}. All rights reserved.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
