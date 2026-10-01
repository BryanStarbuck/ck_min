This is the assessment manual. This is what we're going to assess everything against.
Every page on the site — level 2 and level 3 — must be evaluated against these rules before
it is considered complete.


============================
SITE CONTENT HIERARCHY
============================

Level 1: Home page
  * The root landing page.
  * Has three-column panels linking into Level 2 areas.
  * Each panel represents a major investigation category.

Level 2: Category overview pages (overview.md in each topic directory)
  * Reached from the home page panels or the left sidebar when you enter an area.
  * Purpose: orient the reader and let them self-select into what they care about.
  * Must have the three-column bullet list (see below).

Level 3: Individual analysis pages (specific .md files inside topic directories)
  * Reached by clicking a bullet in a Level 2 three-column list.
  * Purpose: deliver focused information on one specific sub-topic.
  * Must get straight to the point. No broad overview rehash.
  * Must have links off to related Level 2 or Level 3 pages at the bottom.


============================
LEVEL 2 PAGE REQUIREMENTS
============================

Every Level 2 page must open with a brief one- or two-sentence orientation paragraph,
then immediately present the three-column bullet list.

The three-column list is the primary navigation mechanism on a Level 2 page. Its job
is to let a reader scan quickly, spot what they care about, and click through.

* Each column is a bullet list of Level 3 page links.
* Each bullet is a short phrase or title — enough to understand the sub-topic.
* Bullets may have a one-line sub-description if needed for clarity, but keep it tight.
* The three columns must be the same height, plus or minus one row.
* Distribute entries left-to-right across columns as you add them so that column
  heights stay balanced. Do not fill column one before starting column two.
* If the total count does not divide evenly by three, put the extra item in column one,
  then column two — never leave column three taller than the others.

After the three-column list, every Level 2 page must have exactly three paragraphs that
explain the area in depth. These paragraphs come after the TOC, never before it. Think of
them as the "why this matters" body of the page — once a reader has scanned the TOC and
may not have clicked yet, these paragraphs give them enough context to understand the
section and confirm they are in the right place.

Guidelines for the three paragraphs:
  * Paragraph 1: What this area covers and why it is significant to the investigation.
  * Paragraph 2: The key evidence, patterns, or findings in this area — the substance.
  * Paragraph 3: What the reader should do next — which Level 3 pages to prioritize,
    or what questions this area is trying to answer.
  * Each paragraph: three to five sentences. No bullet lists inside these paragraphs.
  * Do not restate the bullet labels from the TOC verbatim — add new context and depth.

After the three paragraphs, every Level 2 page must end with the Related Areas section
(see RELATED AREAS SECTION below).

Docusaurus MDX syntax for three equal columns:

  <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem'}}>
  <div>

  * [Topic A](./topic-a)
  * [Topic B](./topic-b)
  * [Topic C](./topic-c)

  </div>
  <div>

  * [Topic D](./topic-d)
  * [Topic E](./topic-e)
  * [Topic F](./topic-f)

  </div>
  <div>

  * [Topic G](./topic-g)
  * [Topic H](./topic-h)
  * [Topic I](./topic-i)

  </div>
  </div>

Balance check: count bullets in each column after drafting. If any column is more than
one row taller than another, move the last bullet of the tall column to the top of the
next column.


============================
LEVEL 3 PAGE REQUIREMENTS
============================

* Open directly with the substance — no long preamble, no re-stating the site theme.
* Structured with clear sub-headings for each major point or category of evidence.
* Every factual claim attributed to a source (link or inline citation).
* Defamation rules apply for any living person (see CLAUDE.md).
* Status field required for any person profile page: Alive / Deceased (YYYY) / Unknown.

--- Back button ---

At the very top of every Level 3 page, immediately before any content, include a
back-navigation button that reads as the Level 2 topic name this page belongs to.
Clicking it returns the reader to the parent Level 2 overview page.

Use this MDX pattern (replace label and path as appropriate):

  <a href="../overview" style={{display:'inline-block', marginBottom:'1rem',
  padding:'0.35rem 0.9rem', background:'#1a73e8', color:'#fff',
  borderRadius:'4px', textDecoration:'none', fontSize:'0.9rem'}}>
  ← FBI Cover-Up
  </a>

The label should be the short title of the Level 2 area, prefixed with a left arrow.
Do not use a plain markdown link — it must render as a button so it is visually distinct
from body text.

--- Images and video on Level 3 pages ---

Level 3 pages may include up to three media items (images, real video files, or
YouTube embeds). Each media item:

  * Floats to the RIGHT half of the center content column only.
  * Body text wraps around the left side of the media.
  * Maximum width: 48% of the center content area. Never wider than half.
  * Never use .typ files — too rigid. Use .mdx (preferred) or .md with MDX enabled.

Float-right pattern for an image:

  <img src="/img/some-image.jpg"
    style={{float:'right', width:'48%', marginLeft:'1.5rem', marginBottom:'1rem'}}
    alt="Description of image" />

Float-right pattern for a YouTube embed:

  <div style={{float:'right', width:'48%', marginLeft:'1.5rem', marginBottom:'1rem'}}>
  <iframe width="100%" style={{aspectRatio:'16/9'}}
    src="https://www.youtube.com/embed/VIDEO_ID"
    frameborder="0" allowfullscreen />
  </div>

Float-right pattern for a local video file:

  <video controls style={{float:'right', width:'48%',
    marginLeft:'1.5rem', marginBottom:'1rem'}}>
    <source src="/video/some-file.mp4" type="video/mp4" />
  </video>

After the last media item on a page, add a clearfix so the next section starts below
all floated content:

  <div style={{clear:'both'}} />

Every Level 3 page must end with the Related Areas section (see RELATED AREAS SECTION below).


============================
RELATED AREAS SECTION
============================

Every Level 2 and every Level 3 page must end with a "Related Areas" section. This
appears at the very bottom of the page, after all body content.

Layout: six links arranged in two columns, three per column. Left column on the left,
right column on the right.

  ## Related Areas

  <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:'0.5rem 2rem',
  marginTop:'0.5rem'}}>
  <div>

  * [Phrase for Link 1](../path/to/page)
  * [Phrase for Link 2](../path/to/page)
  * [Phrase for Link 3](../path/to/page)

  </div>
  <div>

  * [Phrase for Link 4](../path/to/page)
  * [Phrase for Link 5](../path/to/page)
  * [Phrase for Link 6](../path/to/page)

  </div>
  </div>

Rules for choosing the six links:

  * Mix Level 2 and Level 3 destinations — do not use all of one type.
  * Do NOT link to pages within the current Level 2 section (those are already in
    the TOC or body). Jump to a different part of the site tree.
  * Lean toward pages that have few inbound links from other pages — this spreads
    link equity across the site and surfaces under-linked content.
  * Choose pages that share a thematic connection to the current page but come from
    a different angle — a reader who finished this page would likely find value there.
  * Phrase each link as a short, descriptive label (4-8 words). Not the raw page title
    if the title is vague — write a phrase that makes the destination clear.
  * Never use "click here" or generic labels. Every phrase must communicate the destination.

How to identify low-inbound-link pages:
  * Pages that are only reachable from one TOC are candidates.
  * Pages that are new or recently created are likely low-linked.
  * Pages that are deep in a rarely-visited section are candidates.
  * Prefer linking to these over linking to pages that already appear prominently
    in the navbar or the home page panels.

Do not list the same destination in Related Areas on two adjacent pages.


============================
PAGE CONTENT AUDIT CHECKLIST
============================

When assessing any page, go through each item:

Level 2 checklist:
  [ ] Opens with a short orientation paragraph (1-2 sentences).
  [ ] Three-column bullet list (TOC) present immediately after the orientation paragraph.
  [ ] Every existing Level 3 page in this section is linked from the TOC.
  [ ] TOC bullet phrases are clear enough to know the sub-topic without clicking.
  [ ] No missing sub-topics — all sub-areas a reader would expect are represented.
  [ ] No bullets in the TOC that point to non-existent or placeholder pages.
  [ ] Column heights are equal or off by at most one row.
  [ ] Bullets are distributed left-to-right to maintain balance.
  [ ] After the TOC: exactly three explanatory paragraphs (what, substance, next steps).
  [ ] Three paragraphs do not duplicate TOC bullet labels — they add context and depth.
  [ ] Related Areas section at the bottom: 6 links, two columns of three.
  [ ] Related Areas links jump to a different section of the site, not this section.
  [ ] Related Areas includes a mix of Level 2 and Level 3 destinations.
  [ ] No wall of prose before the three-column TOC.

Level 3 checklist:
  [ ] Back button at the very top linking to the parent Level 2 overview page.
  [ ] Back button label is the Level 2 topic name, prefixed with a left arrow.
  [ ] Gets straight to the specific sub-topic — no broad site overview rehash.
  [ ] Sub-headings break up the content into clear sections.
  [ ] All factual claims attributed to a source.
  [ ] Living persons: defamation-safe language throughout (see CLAUDE.md).
  [ ] Status field present on any person profile page.
  [ ] Media items (if any): max three, each floated right at 48% width, text wraps left.
  [ ] No .typ files — use .mdx or .md with MDX enabled.
  [ ] Clearfix div after the last media item.
  [ ] Related Areas section at the bottom: 6 links, two columns of three.
  [ ] Related Areas links jump to a different section of the site, not the current one.
  [ ] Related Areas includes a mix of Level 2 and Level 3 destinations.
  [ ] Does not duplicate content that belongs on a different Level 3 page.

Both levels:
  [ ] Page title and file name match the sub-topic focus.
  [ ] Internal links use correct Docusaurus relative paths.
  [ ] No broken links.
  [ ] No markdown rendering issues (escaped characters, unclosed tags).


============================
REBALANCING LEVEL 2 PAGES
============================

A Level 2 page is the owner of its Level 3 children. Every Level 2 must have a
hyperlink table of contents — two columns with links down to the Level 3 pages
underneath it. Every Level 3 page must have at least one Level 2 parent. If a
Level 3 page exists without an owning Level 2, either assign it to the correct
Level 2 or create a new Level 2 to house it.

Rebalancing means re-analyzing a Level 2 section and its children to determine
whether the current grouping still makes sense given the content that exists
today. Think of it as clustering. As new information flows in — new evidence,
new people, new documents — the original Level 3 breakdown may no longer fit
cleanly. Rebalancing asks: do the existing Level 3 pages still group naturally,
or has the section outgrown its structure?


============================
WHEN TO REBALANCE
============================

Rebalance a Level 2 section when any of these are true:

  * The Level 2 TOC has grown past roughly 15-20 Level 3 entries and the list
    feels unwieldy. A reader scanning 25+ bullets cannot orient quickly.
  * New content has arrived that does not fit neatly into any existing Level 3
    topic. It either gets shoe-horned somewhere awkward or sits homeless.
  * Several Level 3 pages share a clear sub-theme that would benefit from its
    own grouping — readers would expect to see them together.
  * The Level 2 page serves a broad category (People, Evidence, Timeline) where
    the children span diverse sub-areas with no visible structure.


============================
CLUSTERING — CREATING TOPIC GROUPS
============================

When a Level 2 section has too many Level 3 children, introduce topic clusters.
A topic cluster is a new intermediate grouping — effectively a new Level 3
directory that acts as a sub-section, pushing the former Level 3 pages down to
Level 4 underneath it.

The process:

  1. INVENTORY — List every Level 3 page under the Level 2. Read each one to
     understand what it covers.

  2. IDENTIFY CLUSTERS — Look for natural groupings. Ask: if a newcomer is
     trying to learn about this investigation area, what categories would they
     expect to see? What clusters make sense for this audience?

  3. NAME THE CLUSTERS — Each cluster needs a short, clear phrase name (3-6
     words) that communicates the grouping to someone unfamiliar with the
     investigation. The name should be appropriate for the audience coming in
     to view the content.

  4. ASSIGN PAGES — Place each existing Level 3 page into a cluster. Some
     pages may not fit any cluster — those stay as direct Level 3 children
     of the Level 2. Not everything must be clustered.

  5. CREATE THE STRUCTURE — Each cluster becomes a new subdirectory under the
     Level 2 directory, with its own overview.md (making it a nested Level 2).
     The former Level 3 pages move into that subdirectory and become Level 3
     children of the cluster.

  6. UPDATE THE PARENT TOC — The parent Level 2 TOC now lists the cluster
     names (linking to their overview pages) instead of listing every
     individual page. The count in the parent TOC shrinks to a manageable
     number.

Rules for clustering:

  * A cluster should contain at least 3 pages. Do not create a cluster for
    a single page — that adds a navigation layer with no benefit.
  * A cluster should not contain more than ~15 pages. If a cluster grows
    beyond that, it may need its own sub-clusters.
  * Unclustered pages are fine. Not every page needs to be in a group. A
    Level 2 TOC can mix cluster links and direct Level 3 links.
  * The cluster overview.md follows all Level 2 page requirements from this
    manual: orientation paragraph, three-column TOC of its children, three
    explanatory paragraphs, Related Areas.


============================
CLUSTERING — WORKED EXAMPLE: PEOPLE
============================

Suppose the Level 2 section is "People" and it has grown to 100 Level 3 pages,
each profiling one individual. A TOC of 100 names is unusable. A newcomer
cannot scan it and find what they need.

Step 1: Look at how these people cluster up. Read the profiles and identify
commonalities — organizational affiliation, role in the investigation, how
they connect to the event.

Step 2: Possible clusters emerge:

  * TPUSA — people affiliated with Turning Point USA, the non-profit Charlie
    Kirk founded. Board members, executives, employees, associated figures.
  * Law Enforcement — FBI agents, local police, detectives, prosecutors, and
    other officials involved in the investigation or cover-up.
  * Witnesses — people who were present at UVU on September 10, 2025, or who
    have firsthand testimony about events surrounding the assassination.
  * Influencers — media figures, podcasters, journalists, and online
    investigators who have covered or amplified the investigation.
  * Intelligence Connections — individuals linked to intelligence agencies or
    operations relevant to the case.
  * Family — Charlie Kirk's family members and their roles in the aftermath.

Step 3: The People/ directory restructures:

  Before (flat):
    People/
      overview.md          (Level 2 — 100 bullets in TOC)
      person_a.md          (Level 3)
      person_b.md          (Level 3)
      ... 98 more files

  After (clustered):
    People/
      overview.md          (Level 2 — ~8 entries: 6 cluster links + 2 unclustered)
      TPUSA/
        overview.md        (nested Level 2 — TOC of TPUSA-affiliated profiles)
        person_x.md        (now Level 3 under TPUSA)
        person_y.md
        ...
      Law_Enforcement/
        overview.md
        agent_a.md
        detective_b.md
        ...
      Witnesses/
        overview.md
        witness_1.md
        witness_2.md
        ...
      Influencers/
        overview.md
        podcaster_a.md
        journalist_b.md
        ...
      unclustered_person.md  (stays at Level 3 directly under People)

Step 4: The parent People/overview.md TOC now reads:

  * [TPUSA Affiliates](./TPUSA/overview)
  * [Law Enforcement Officials](./Law_Enforcement/overview)
  * [Witnesses at UVU](./Witnesses/overview)
  * [Influencers & Media](./Influencers/overview)
  * [Intelligence Connections](./Intelligence_Connections/overview)
  * [Kirk Family Members](./Family/overview)
  * [Person Who Doesn't Cluster](./unclustered_person)

A newcomer can now scan 7 items instead of 100 and immediately find the
group they care about. Each cluster overview then provides the detailed
list within that group.


============================
REBALANCING WITHOUT CLUSTERING
============================

Not every rebalance requires creating clusters. Sometimes the fix is simpler:

  * A Level 3 page belongs under a different Level 2 — move it.
  * Two Level 3 pages cover the same sub-topic — merge them.
  * A Level 3 page has grown so large it should split into multiple pages.
  * The TOC ordering no longer reflects importance or logical flow — reorder.
  * New Level 3 pages were added but never linked in the TOC — add them.
  * Dead links in the TOC point to pages that were removed — clean them up.

These are housekeeping rebalances and do not change the hierarchy depth.


============================
BALANCING THE THREE COLUMNS — WORKED EXAMPLE
============================

If you have 10 bullets to place across three columns:
  Column 1: 4 bullets  (gets the extra one)
  Column 2: 3 bullets
  Column 3: 3 bullets

If you have 11 bullets:
  Column 1: 4 bullets
  Column 2: 4 bullets
  Column 3: 3 bullets

If you have 9 bullets:
  Column 1: 3 bullets
  Column 2: 3 bullets
  Column 3: 3 bullets

When placing bullets, go across: first bullet of each column, then second bullet of
each column, and so on. This way if you stop mid-row, columns are naturally even.


============================
CONTENT COVERAGE AUDIT
============================

For every Level 2 page, ask:
  * Does this section have all the sub-topics a reader would expect to find here?
  * Are any sub-topics missing that deserve a Level 3 page?
  * Are any sub-topics covered here that actually belong under a different Level 2?
  * Is every existing Level 3 page in this section linked from the TOC?
  * Are TOC bullet phrases specific enough — short, descriptive, unambiguous?
  * Do the three explanatory paragraphs cover what, substance, and next steps?
  * Do the paragraphs add depth beyond what the TOC bullets already communicate?

For every Level 3 page, ask:
  * Is this the right home for this content, or does it belong under a different Level 2?
  * Does the page cover the full scope of its sub-topic, or is it thin?
  * Is the page doing too much — should it be split into two Level 3 pages?
  * Does the back button exist and point to the correct Level 2 overview?
  * Are media items (if present) floated right at max 48% width with text wrapping left?
  * Do the Related Areas links go outside the current section to under-linked pages?


============================
WRITING STYLE ON PAGES
============================

* Plain, direct writing. No filler phrases.
* Active voice preferred.
* Short paragraphs — three to five sentences max before a new sub-heading or break.
* Bullet lists for evidence, timelines, and enumerated facts.
* Bold for key names, dates, and terms on first use in a section.
* No markdown headers above H2 (##) inside page body — H1 is the page title only.
* No emojis unless explicitly requested.


============================
BOILERPLATE TEMPLATE REMOVAL
============================

The page will often have this boilerplate template below content. Assume that we want to get rid of that, but look at those and analyze if we really need them or not.



Key Areas
Podcast episodes
Host analysis
Coverage quality
Evidence presented
Audience reach
Status
 Initial research
 Evidence collection
 Analysis
 Documentation
Edit this page


============================
NO DOCUSAURUS AUTO-CATEGORY CARD PAGES
============================

Problem pattern we are preventing:

Example URL (the bug we do NOT want):
  https://whoassassinatedcharliekirk.com/category/planes

When you land on that URL today, Docusaurus renders an auto-generated category
page. It shows clickable card panels, one per Level 3 child page, with just
the page title inside each card. No orientation paragraph. No prose. No control
over layout. Every Level 2 section rendered this way looks the same — a grid
of boxes — and the reader has to click a card just to see what is inside.

This is wrong. Every Level 2 page must instead be a hand-authored overview
page with the multi-column bullet list described in this manual.

--- Root cause ---

Docusaurus generates the /category/{name} URL whenever a directory's
_category_.json (or sidebars.ts category entry) contains:

  "link": { "type": "generated-index" }

That single line tells Docusaurus: "do not use the overview page I wrote —
auto-render a card grid instead."

Example of the broken config (site/docs/Planes/_category_.json):

  {
    "label": "Planes",
    "position": 30,
    "collapsed": true,
    "link": {
      "type": "generated-index"
    }
  }

--- Fix ---

Point the category link at the hand-written overview page instead. For the
Planes example, the overview lives at site/docs/Planes/overview.md, and the
_category_.json should read:

  {
    "label": "Planes",
    "position": 30,
    "collapsed": true,
    "link": {
      "type": "doc",
      "id": "Planes/overview"
    }
  }

After this change, clicking "Planes" in the sidebar (or any link that used to
land on /category/planes) now loads the hand-authored overview page with its
multi-column bullet list and three explanatory paragraphs — not the card grid.

--- Audit rule ---

No page under site/docs/ may use "link": { "type": "generated-index" }. Grep
the repo for that string before publishing. Every hit must be replaced with
a "type": "doc" link that points at the matching overview page.

  [ ] Ran: grep -R "generated-index" site/docs/ — zero hits.
  [ ] Every _category_.json with a "link" field points at type: "doc".
  [ ] Every Level 2 directory has an overview.mdx (or overview.md) file.
  [ ] No /category/* URLs exist on the live site.


============================
LEVEL 2 USES TWO COLUMNS (NOT THREE)
============================

This section supersedes the earlier THREE-column guidance for Level 2 pages.
The home page (Level 1) continues to use three columns. Every Level 2 page
uses TWO columns.

Why different: the home page is the widest entry point and needs to surface
the most categories at a glance, so three columns fit. A Level 2 page is one
click deeper, has fewer Level 3 children, and reads better with two taller
columns than three short ones. Two columns also leave room in the page
gutters for the eye to rest, which matters when the reader is already
oriented inside a section.

--- Pattern reference ---

Mirror the exact multi-column layout used on the home page
(site/docs/index.md, lines 20-74). Copy that pattern, drop a column, and
use it on every Level 2 overview page. The bullet-list-inside-a-flex-div
style is the canonical layout — do not invent a new one.

--- MDX syntax for two equal columns on a Level 2 page ---

  <div style={{ display: "flex", justifyContent: "space-between", gap: "2rem" }}>
    <div style={{ flex: 1 }}>

  * [Topic A](./topic-a)
  * [Topic B](./topic-b)
  * [Topic C](./topic-c)
  * [Topic D](./topic-d)

    </div>
    <div style={{ flex: 1 }}>

  * [Topic E](./topic-e)
  * [Topic F](./topic-f)
  * [Topic G](./topic-g)
  * [Topic H](./topic-h)

    </div>
  </div>

--- Balance rules for two columns ---

  * Distribute bullets left-to-right as you add them. Do not fill the left
    column completely before starting the right column.
  * Column heights must be equal or off by at most one row.
  * If the bullet count is odd, put the extra bullet in the LEFT column.
  * Example: 9 bullets -> 5 left, 4 right. 10 bullets -> 5 and 5. 11 bullets
    -> 6 left, 5 right.

--- What else on the Level 2 page stays the same ---

The rest of the Level 2 spec earlier in this manual still applies, with the
single change that the TOC is TWO columns instead of three:

  * Opens with a one- to two-sentence orientation paragraph.
  * Two-column bullet list comes immediately after the orientation paragraph.
  * Exactly three explanatory paragraphs follow the two-column TOC (what,
    substance, next steps).
  * Related Areas section at the bottom (still two columns of three links).


============================
ALL UI PAGES MUST BE .MDX
============================

Every UI page under site/docs/ must use the .mdx extension, not .md. A .md
file cannot reliably render the inline JSX that the multi-column layout, the
float-right media blocks, and the styled back button all depend on. The
moment a page needs a <div style={{...}}>, it has to be .mdx.

Rule: when creating a new UI page, create it as .mdx from the start. When
encountering an existing .md page that needs any inline JSX (or already
contains inline JSX, even if it currently renders), convert it to .mdx.

--- How to convert .md to .mdx ---

  1. Rename the file: overview.md -> overview.mdx
  2. Update any internal link that hardcodes the .md extension. Docusaurus
     normally resolves by ID so most links will not need changes, but any
     link like (./overview.md) must become (./overview) or (./overview.mdx).
  3. Update pages.csv: change the file_path and the extension column for
     that row.
  4. If sidebars.ts or _category_.json references the page by file path
     rather than by doc ID, update that reference.
  5. Verify by running the dev server: cd site && npm start. The page
     should render identically, with all JSX blocks now active.

--- Audit rule ---

  [ ] No Level 2 overview page is a .md file. All Level 2 overviews are .mdx.
  [ ] No Level 3 page that contains inline JSX is a .md file.
  [ ] pages.csv extension column reflects reality for every row.
  [ ] No broken links after rename (dev server reports zero warnings).


============================
ROOT CAUSE CATALOG — PLANES LEVEL 2 WORKED EXAMPLE
============================

This section names the exact patterns in the Docusaurus source files that
produce the three most common Level 2 bugs. Use it as a diagnostic lookup:
if you see one of the visible symptoms below on the live site, go hunt for
the source-file fingerprint that causes it and replace it with the fix.

The Planes section (site/docs/Planes/) is the canonical example because on
the live site today it exhibits all three symptoms simultaneously. Use it
as the reference when teaching anyone what the broken state looks like.

--- Symptom 1: Auto-generated card-grid panel buttons ---

What a visitor sees:
  Navigating to /Planes (via the sidebar or a link that used to point at
  the overview) lands on a page titled by the category with a grid of
  clickable card buttons — one card per child page — and nothing else.
  No orientation paragraph, no two-column TOC, no body prose, no Related
  Areas. The hand-authored overview.md is never rendered.

Source-file fingerprint:
  site/docs/Planes/_category_.json contains:

    "link": { "type": "generated-index" }

  This single key tells Docusaurus to synthesize a /category/planes route
  and render a DocCardList of child pages instead of loading the directory's
  overview document. Every directory whose _category_.json carries this
  key will exhibit the same bug.

How to identify in source:
  grep -R '"type": "generated-index"' site/docs/
  Every hit is a broken Level 2. Zero hits is the target state.

Fix:
  Replace the generated-index link with a doc link that points at the
  directory's hand-authored overview:

    "link": { "type": "doc", "id": "Planes/overview" }

Prevention rule:
  No _category_.json under site/docs/ may contain
  "type": "generated-index". CI should fail the build if it finds one.

--- Symptom 2: Visible anchor tag with literal {{...}} in the rendered page ---

What a visitor sees:
  The back-navigation button at the top of the Level 2 page does not
  render as a styled blue pill. Instead the reader sees the raw HTML
  attribute text — including the double-curly-brace expression like
  style={{display:'inline-block', ...}} — leaking into the page body as
  visible characters next to the link. The link may still be clickable
  but the button styling is missing and the page looks broken.

Source-file fingerprint:
  The file is named overview.md (not overview.mdx) but its contents use
  JSX-style inline style objects, for example:

    <a href="/" style={{display:'inline-block', marginBottom:'1rem',
    padding:'0.35rem 0.9rem', background:'#1a73e8', color:'#fff',
    borderRadius:'4px', textDecoration:'none', fontSize:'0.9rem'}}>
    ← Home
    </a>

  Docusaurus parses .md files as Markdown + raw HTML only. The double-
  curly-brace expression inside style={{...}} is a JSX object literal
  and is NOT evaluated. The browser then receives style={{...}} as a
  literal attribute string and either discards the invalid CSS or renders
  the braces as visible text, depending on the surrounding context.
  Any <div style={{...}}>, <iframe style={{...}}>, or float-right media
  block in the same .md file breaks for the same reason.

How to identify in source:
  grep -REn 'style=\{\{' site/docs/ --include='*.md'
  Every hit is a .md file using JSX-only syntax. Zero hits is the target
  state. (Hits inside .mdx files are fine — that is where JSX belongs.)

Fix:
  Rename the file to .mdx (overview.md -> overview.mdx). Update any hard-
  coded .md references in sidebars.ts, _category_.json, or internal links.
  Update the corresponding row in pages.csv (file_path and extension
  columns). Re-run the dev server and confirm the back button renders as
  a styled pill.

Prevention rule:
  Any page containing the substring `style={{` must have the .mdx
  extension. No Level 2 overview page may be a .md file regardless of
  content — Level 2 overviews always need the multi-column layout, which
  requires JSX, which requires .mdx.

--- Symptom 3: Level 2 TOC shows a single bullet (under-populated section) ---

What a visitor sees:
  Under the "Pages in this Section" heading the multi-column TOC contains
  only one bullet — in the Planes case, just [N1098L Spy Plane] in the
  left column with an empty right column. The section looks abandoned.
  A reader who clicked into Planes expecting a survey of aircraft topics
  sees one link and nothing else.

Source-file fingerprint:
  site/docs/Planes/overview.md renders a two-column grid wrapper whose
  first column contains a single bullet and whose second column is empty:

    <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem'}}>
    <div>

    * [N1098L Spy Plane](./N1098L/overview)

    </div>
    <div>

    </div>
    </div>

  The section directory contains only one Level 3 child (N1098L/), so
  there is nothing else to link. This is a content-coverage problem, not
  a syntactic one: the Level 2 exists but has not been populated with the
  sub-topics a reader would expect.

How to identify in source:
  ls site/docs/{Section}/ — if the directory contains only one non-
  overview entry, the Level 2 TOC will be a single bullet. Cross-check
  against the Content Coverage Audit in this manual: what sub-topics
  would a reader expect to find under this Level 2?

Fix:
  Do NOT hide the problem by removing the two-column wrapper or by
  padding the TOC with placeholder links. Treat the thin TOC as a signal
  that the section needs more Level 3 pages. For Planes specifically,
  candidate Level 3 pages include: SAM flights, SU-BTT, foreign VIP
  arrivals, transponder anomalies, Utah Lake low-altitude passes, ISR
  program context, and each specific tail number mentioned in the
  investigation. Create those pages, then rebalance the TOC per the
  LEVEL 2 USES TWO COLUMNS rules earlier in this manual.

Prevention rule:
  A Level 2 TOC with fewer than 3 bullets is presumptively incomplete.
  Either the section is too narrow to justify its own Level 2 (merge it
  into a sibling Level 2) or it is missing content (add Level 3 pages).
  Never ship a Level 2 overview with a single-bullet TOC.

--- Symptom 4: Two-panel card grid showing the section's own overview as one of the cards ---

What a visitor sees:
  Navigating to /category/{section} (e.g. /category/planes) lands on an
  auto-generated card grid that shows EXACTLY TWO panels. One panel is
  labeled with the name of a child subdirectory (e.g. "N1098L"). The OTHER
  panel is labeled with the SAME name as the section itself (e.g. "Planes").
  Clicking the second panel ("Planes") navigates the reader to the section's
  own overview page — meaning the section is presenting its own overview as
  a sibling card next to its real children. This is disorienting: the reader
  arrived at the Planes page and is offered a card called "Planes" inside it.

Source-file fingerprint:
  This is the combination of THREE source-file properties at once:

    1. site/docs/{Section}/_category_.json contains
         "link": { "type": "generated-index" }
       which tells Docusaurus to render the directory as a card grid.

    2. The directory contains BOTH an overview.md (or overview.mdx) AND at
       least one child subdirectory. The card grid lists every child of the
       directory — files AND subdirectories — as separate cards.

    3. The overview file's frontmatter declares either a `sidebar_label` or
       a `title` that matches the section name (e.g. sidebar_label: "Planes"
       inside site/docs/Planes/overview.md). That label becomes the card
       title for the overview, producing a card named after the section
       sitting next to the section's other children.

  Concrete reproduction (Planes section, pre-fix):
    site/docs/Planes/_category_.json -> "type": "generated-index"
    site/docs/Planes/N1098L/         -> renders as card "N1098L"
    site/docs/Planes/overview.md     -> sidebar_label "Planes"
                                        renders as card "Planes"
    Result at /category/planes: two cards, "N1098L" and "Planes".

How to identify in source:
  For every directory under site/docs/ whose _category_.json uses
  "type": "generated-index", run:

    ls site/docs/{Section}/

  If the directory contains an overview.md or overview.mdx in addition to
  subdirectories, the auto card grid will include the overview as a card.
  This is always wrong — overviews are meant to be the destination, not a
  sibling card.

Fix:
  Same fix as Symptom 1 — replace generated-index with a doc link that
  points at the overview. Once the section's link goes directly to the
  overview, /category/{section} is no longer generated and the misleading
  two-panel grid disappears. Also follow Symptoms 2 and 3 for the overview
  itself (.mdx extension, populated TOC).

Prevention rule:
  Any directory that contains an overview.md or overview.mdx must have its
  _category_.json link set to "type": "doc" pointing at that overview.
  Never leave a directory with both an overview AND a generated-index link
  — the overview will leak into the card grid as a sibling of its children.

--- Symptom 5: Duplicate sibling directories with overlapping names ---

What a visitor sees:
  The left sidebar shows TWO entries with nearly identical names — for
  example both "Plane" and "Planes" appear at the same nesting level. The
  reader cannot tell which one is canonical. Clicking either one may lead
  to a card grid (Symptom 1 / 4) or a stub overview page. The investigation
  content is split across both directories with no clear ownership rule.

Source-file fingerprint:
  Two sibling directories under site/docs/ whose names differ only in
  pluralization, casing, or punctuation:

    site/docs/Plane/        (singular)
    site/docs/Planes/       (plural)

  OR a duplicate of the same name nested under a parent directory:

    site/docs/Planes/                  (top-level)
    site/docs/Topics3/Planes/          (nested)

  Both produce sidebar entries. Both may produce /category/{slug} URLs.
  When labels collide, Docusaurus disambiguates by appending -1, -2 to
  one of them (e.g. /category/planes and /category/planes-1) — neither
  URL is the one a reader would guess.

How to identify in source:
  ls site/docs/ and look for near-duplicate names: singular/plural pairs,
  CamelCase vs snake_case variants, or the same name appearing under
  Topics3/ as well as at the top level. Cross-check by grepping for the
  label string across all _category_.json files:

    grep -R '"label":' site/docs/ | sort | uniq -c -f1 | sort -rn | head

  Any label appearing more than once is a duplicate-sidebar candidate.

Fix:
  Pick ONE canonical directory per topic. Move all content from the
  duplicate into the canonical directory, update internal links, update
  pages.csv rows, then delete the duplicate directory. Update any
  _category_.json that referenced the deleted directory by id.

Prevention rule:
  Before creating a new top-level directory under site/docs/, grep for
  any existing directory whose name differs only in pluralization,
  casing, or location (e.g. Topics3/{Same}). If a near-duplicate exists,
  add to the existing directory instead of creating a new one.

--- Combined audit for any Level 2 page ---

  [ ] _category_.json uses "type": "doc", not "type": "generated-index".
  [ ] Overview file extension is .mdx, not .md.
  [ ] No style={{...}} substrings appear inside any .md file in the section.
  [ ] The multi-column TOC has at least 3 bullets distributed left-to-right.
  [ ] Clicking the sidebar entry lands on the hand-authored overview, not
      on a /category/{name} card grid.
  [ ] The back button at the top renders as a styled pill, with no raw
      {{...}} characters visible in the page body.
  [ ] If the directory has both an overview.md/.mdx AND child subdirectories,
      _category_.json link is "type": "doc" (otherwise the overview leaks
      into the auto card grid as a sibling of its children — Symptom 4).
  [ ] No sibling directory under site/docs/ shares the same name in
      singular/plural or near-duplicate form (Symptom 5). Pick one
      canonical directory per topic.
  [ ] No duplicate of this directory exists nested under Topics3/ or any
      other parent (Symptom 5).

--- Multi-page audit recipe ---

When fixing a Level 2 section, do not stop at the first matching directory.
Run all of these against the entire site/docs/ tree:

  1. List every directory whose name matches or near-matches the section
     name (singular/plural, casing variants, nested duplicates):

       Glob "**/{Section}*" inside site/docs/

  2. List every _category_.json with a label that matches or near-matches:

       grep -R '"label":' site/docs/ | grep -i {section}

  3. For every hit, check whether _category_.json uses generated-index.
     Every hit is a candidate page that needs fixing.

  4. Decide which one is canonical. Fix the canonical one per Symptoms 1-4.
     Either fix or delete the duplicates per Symptom 5.

  5. After deploying, verify on the live site that no /category/{slug}
     URL exists for the section name or any of its near-duplicates.

  6. Note that fixes to _category_.json do NOT take effect until the
     Docusaurus static site is rebuilt and redeployed. After merging,
     run `cd site && npm run build` and push so GitHub Pages picks up
     the change. A live page that still shows the card grid after a
     source fix usually means the deploy has not completed.


============================
PROBLEM PATTERNS AT A GLANCE
============================

This section is the quick-lookup index of every layout/structure anti-pattern
this manual bans. When assessing a page or section, scan this list first — if
any of these fingerprints match, stop and fix the pattern before continuing
with content work. Each pattern below has a full-detail section elsewhere in
this manual; this is the at-a-glance summary.

  1. CARD GRID — any rendered page that shows clickable card panels (one per
     child) instead of a hand-authored overview. We never want card grids
     anywhere on the site. Level 1 and Level 2 are always hand-authored
     multi-column bullet lists.

  2. GENERATED-INDEX _category_.json — any _category_.json file whose link
     block uses "type": "generated-index". This is the direct cause of the
     card grid pattern. Ban outright. See NO _CATEGORY_.JSON FILES below.

  3. _category_.json FILES IN GENERAL — we do not want these files shaping
     navigation. The sidebar should go to real Level 2 overview pages, not
     to synthesized /category/{slug} URLs. Prefer deleting _category_.json
     files entirely wherever possible. See NO _CATEGORY_.JSON FILES below.

  4. DUPLICATE-BY-PLURAL — two sibling directories differing only in
     pluralization, casing, or punctuation (e.g. site/docs/Plane/ and
     site/docs/Planes/). Pick one canonical directory and merge the other
     into it. See DUPLICATE DIRECTORY PATTERN below.

  5. UMBRELLA META-DIRECTORY — directory names like Topics2/, Topics3/,
     Meta/, Other/, Misc/, aircraft_flight_analysis/ that act as
     pseudo-parents holding topics which should instead live at the top
     level of site/docs/. These must not exist. See NO UMBRELLA
     DIRECTORIES below.

  6. SCATTERED TOPIC CONTENT — the same subject area spread across multiple
     top-level directories (e.g. plane/flight content under Planes/, Plane/,
     Topics3/Planes/, aircraft_flight_analysis/ all at once). Consolidate
     under ONE canonical Level 2 directory. See ONE LEVEL 2 PER TOPIC below.

  7. FILE-NAME ECHOES TOPIC-NAME — a Level 2 directory that contains
     overview.mdx AND another file with the same name as the directory
     (e.g. Planes/planes.md alongside Planes/overview.mdx). Either merge
     that file into overview.mdx or rename it to a distinct Level 3 topic.
     See FILE-NAME vs TOPIC-NAME COLLISION below.

  8. NON-STANDARD DIRECTORY NAMES — Level 2 directory names that contain
     spaces, hyphens, mixed punctuation, or special characters. Directory
     names must be alphanumeric with underscores only. See LEVEL 2 DIRECTORY
     NAMING below.

  9. STUB OVERVIEW — a Level 2 overview page with a TOC of fewer than 3
     bullets. Either the section is too narrow to stand alone (merge it)
     or it is under-populated (add Level 3 pages). See ROOT CAUSE CATALOG
     Symptom 3 above.

  10. RAW JSX LEAKING AS TEXT — a .md file containing style={{...}} JSX
      attributes. Fix by renaming to .mdx. See ROOT CAUSE CATALOG Symptom
      2 above.


============================
NO _CATEGORY_.JSON FILES
============================

Preferred state: site/docs/ contains NO _category_.json files at all.

Every _category_.json file we have ever touched has either introduced a card
grid (via generated-index), produced a ghost /category/{slug} URL, or split
the sidebar away from the real Level 2 overview page. The net value of these
files is negative. We are moving away from them.

--- Rules ---

  * Do not create new _category_.json files. When adding a new Level 2
    directory, just create the directory and its overview.mdx file. Docusaurus
    will resolve sidebar labels from the overview frontmatter.

  * When encountering an existing _category_.json, evaluate whether it can
    be deleted outright. If the only thing it does is set a label that
    duplicates the overview's sidebar_label, delete the json — the overview
    frontmatter is the source of truth.

  * If _category_.json must remain (e.g. it sets a position ordering that
    cannot be expressed in frontmatter), its link block must be either
    absent or exactly: "link": { "type": "doc", "id": "{Section}/overview" }
    and nothing else. NEVER "type": "generated-index".

  * The left sidebar entry for any Level 2 section must navigate directly
    to the hand-authored overview page for that section. It must never
    navigate to a /category/{slug} URL. Verify after any change by clicking
    the sidebar entry on the dev server.

--- Audit ---

  [ ] grep -R "generated-index" site/docs/ returns zero hits.
  [ ] No /category/{anything} URL is reachable from the live site sidebar.
  [ ] Any _category_.json that remains contains only layout metadata (position,
      collapsed) OR a "link": { "type": "doc", ... } entry — never generated-index.
  [ ] Where a _category_.json exists only to set a label, delete it and let
      the overview frontmatter carry the label.

--- Relationship to sidebars.ts ---

Sidebar navigation is driven by site/sidebars.ts. Do not modify sidebars.ts
unless the user explicitly asks to change the sidebar. If a broken sidebar
entry is caused by _category_.json, fix or delete the _category_.json
instead. The sidebars.ts file itself is off-limits for this class of fix.


============================
LEVEL 2 DIRECTORY NAMING
============================

Every Level 2 topic has its own directory directly under site/docs/. The
directory name IS the topic identifier on the filesystem. The user-facing
label (sidebar, page title) may differ slightly from the directory name —
the directory form is a strictly normalized version of the label.

--- Rules for directory names under site/docs/ ---

  * Alphanumeric characters and underscores only. No spaces. No hyphens.
    No dots (beyond the path separator). No punctuation. No emoji.
  * Replace every space in the human-readable label with an underscore.
  * Strip any special character that the label uses for readability
    (ampersands, slashes, apostrophes, colons, quotes).
  * Casing: preserve the capitalization of the human label where reasonable
    (e.g. "Cover Up" -> Cover_Up, "FBI" -> FBI). Do not force snake_case
    if the label is naturally capitalized.
  * Keep names compact — 1-3 words when possible. A long label may be
    abbreviated in the directory form if the abbreviation is unambiguous.
  * Every Level 2 directory contains an overview.mdx file. That file is
    the destination the sidebar entry navigates to.

--- Examples ---

  Label "Planes"                  -> site/docs/Planes/
  Label "Cover Up"                -> site/docs/Cover_Up/
  Label "FBI Cover-Up"            -> site/docs/FBI/                  (abbrev acceptable)
  Label "Proof Not Tyler"         -> site/docs/Proof_Not_Tyler/
  Label "Your Actions Fix It"     -> site/docs/Your_Actions_Fix_It/
  Label "Intelligence Services"   -> site/docs/Proof_Intel_Services/ (existing canonical)

--- Human label vs directory form ---

The label in the sidebar, the Level 2 page title, and any navbar entry MAY
contain spaces and readable punctuation. The filesystem path MUST NOT.
Frontmatter on the overview.mdx carries the human label via title or
sidebar_label. Example overview.mdx frontmatter:

    ---
    title: Cover Up
    sidebar_label: Cover Up
    ---

The directory is Cover_Up. The label is "Cover Up". Both are correct.


============================
FILE-NAME vs TOPIC-NAME COLLISION
============================

Problem pattern: a Level 2 directory contains its own overview (overview.mdx)
AND a separate file whose name matches the directory itself.

Example (anti-pattern):
  site/docs/Planes/
    overview.mdx
    planes.mdx          <-- name collides with the directory

That second file is almost always a symptom of one of these:

  1. Legacy content that was the old Level 2 page, never merged into
     overview.mdx when overview.mdx was introduced. Duplicate content.

  2. Level 2 content that the author intended to be the entry point but
     accidentally created alongside overview.mdx.

  3. Content that is genuinely Level 3 but was misnamed — the author
     meant to call it something more specific than the parent topic.

--- Fix ---

For each colliding file, decide which of the three applies:

  * If it is Level 2 content (orientation, TOC, explanatory paragraphs):
    merge its content into overview.mdx and delete the colliding file.

  * If it is Level 3 content about a specific sub-topic: rename it to a
    name that reflects the sub-topic, not the parent. For example,
    Planes/planes.mdx describing N1098L should become Planes/N1098L/overview.mdx
    (as its own subdirectory) or Planes/n1098l_analysis.mdx (as a direct
    Level 3 child).

  * If it duplicates content already in overview.mdx: delete it, then
    update any internal links that pointed at it to point at the
    overview instead.

--- Rule ---

A Level 2 directory must never contain a file whose base name (case-
insensitive, ignoring extension) matches the directory name. The single
entry-point file is overview.mdx. All other files in the directory are
Level 3 pages named after their specific sub-topic.

--- Audit ---

  [ ] For every Level 2 directory under site/docs/, no file besides
      overview.mdx has a name matching the directory name.
  [ ] Any previously colliding file has either been merged into overview.mdx
      or renamed to reflect its specific Level 3 sub-topic.


============================
NO UMBRELLA DIRECTORIES (TOPICS2 / TOPICS3 / META / MISC)
============================

Problem pattern: a pseudo-parent directory under site/docs/ that groups
multiple Level 2 topics under a meta-heading. Examples:

  site/docs/Topics3/Planes/          (Topics3 as a false parent)
  site/docs/Meta/Cameras/            (Meta as a false parent)
  site/docs/Other/Drones/            (Other as a false parent)
  site/docs/Topics2/                 (numbered meta-category)

These directories must not exist. They push real Level 2 topics down an
extra layer, break URL conventions, and cause duplicate sidebar entries
when the same topic also exists at the top level.

--- Why this pattern appears ---

  1. An author created Topics3/ to "organize" Level 2 topics during a
     restructure, then never moved the content back up to the top level.

  2. An auto-generated directory was created by a bulk import that
     grouped content thematically one level too deep.

  3. A human-readable meta-label (e.g. "More Topics") was implemented
     as a directory instead of as a sidebar grouping.

--- Rule ---

Every Level 2 topic lives directly under site/docs/. Period. There are no
numbered meta-parents (Topics2, Topics3, etc.), no generic catch-all parents
(Meta, Misc, Other, Extra), and no thematic super-categories. Sidebar
grouping, when needed, is expressed in sidebars.ts via categories — NOT by
adding filesystem directories.

--- Fix ---

When encountering an umbrella directory:

  1. For each subdirectory inside the umbrella, move it up to the top
     level of site/docs/. For example:
       site/docs/Topics3/Planes/   ->   site/docs/Planes/
     If the top-level destination already exists, this is ALSO a
     duplicate-directory problem — see the duplicate-by-plural rules.

  2. Update all internal links that referenced the umbrella path.

  3. Update pages.csv for every moved page (file_path, directory, and
     url_path columns).

  4. Delete the now-empty umbrella directory.

  5. Never modify sidebars.ts to fix the broken references caused by the
     move unless the user explicitly asks for a sidebar change. If links
     break there, report the needed change rather than making it.

--- Audit ---

  [ ] No directory under site/docs/ is named Topics, Topics2, Topics3,
      Topics4, Meta, Misc, Other, Extra, or any numbered/generic meta-parent.
  [ ] Every Level 2 topic directory sits directly at the site/docs/ depth.
  [ ] No Level 2 content is reachable only via a meta-parent path.


============================
ONE LEVEL 2 PER TOPIC — CONSOLIDATE RELATED CONTENT
============================

Problem pattern: content about one subject area is scattered across
multiple top-level directories under site/docs/, with no single canonical
home. The plane/flight subject is the textbook example of this anti-pattern.

Example scatter (anti-pattern):
  site/docs/Planes/                      (plural, has overview)
  site/docs/Plane/                       (singular duplicate)
  site/docs/Topics3/Planes/              (nested under umbrella)
  site/docs/aircraft_flight_analysis/    (different name, same subject)
  site/docs/planes-flights/              (hyphenated variant)

Every one of those directories is trying to host plane-related content.
A reader cannot find what they need. Content is duplicated, contradicted,
and orphaned.

--- Rule ---

For any broad subject area on the investigation, exactly ONE Level 2
directory exists as the canonical home. Every aspect of that subject —
sub-topics, analyses, people, timelines, documents — lives under that
canonical directory as Level 3 pages or as clusters (see CLUSTERING
section earlier in this manual).

For planes specifically: site/docs/Planes/ is canonical. Every Level 3
page about aircraft, flight tracking, transponder data, tail numbers, SAM
flights, ISR programs, foreign aircraft, low-altitude passes, etc., lives
under site/docs/Planes/. No other top-level directory under site/docs/
may host plane content.

--- Fix when scatter is found ---

  1. Pick the canonical directory. Default to the plural form that matches
     the existing sidebar convention (Planes, People, Drones, Cameras).

  2. Inventory every page in every scatter directory. For each page decide:
       * Is this content duplicated elsewhere? If yes, keep the best
         version and delete the duplicates.
       * Is this content a genuine Level 3 under the canonical Level 2?
         Move it into the canonical directory.
       * Is this content not actually about this subject? Move it to
         the correct Level 2 directory for its real subject.

  3. Merge. Update all internal links. Update pages.csv rows.

  4. Delete the scatter directories once empty.

  5. Verify the canonical Level 2 overview's TOC now lists everything.
     Rebalance using the CLUSTERING rules if the TOC exceeds ~15-20 bullets.

--- Audit ---

  [ ] Every broad subject on the investigation has exactly one Level 2
      home directory under site/docs/.
  [ ] No two top-level directories differ only in pluralization, casing,
      hyphenation, or near-synonyms (e.g. Planes/ and aircraft_flight_analysis/).
  [ ] The canonical Level 2 overview's TOC links to every Level 3 page on
      its subject.
  [ ] No orphan Level 3 page about the subject exists outside the canonical
      Level 2 directory.


============================
DUPLICATE DIRECTORY PATTERN (SINGULAR vs PLURAL)
============================

This is the specific, most common form of the scatter problem. It warrants
its own named pattern because it happens so often.

Problem pattern: two sibling directories under site/docs/ whose names
differ only in pluralization (or another trivial variation) and that both
host content on the same subject.

Examples:
  Plane/     vs Planes/
  Person/    vs People/
  Drone/     vs Drones/
  Camera/    vs Cameras/

--- Why this happens ---

  1. Two authors created directories independently and did not check for
     an existing canonical version.

  2. An early draft used the singular; a later reorganization switched to
     plural but did not delete the singular.

  3. A bulk import generated directories from source data that mixed
     singular and plural forms.

--- Rule ---

For any subject on the site, pick one form — plural by default — and use
it everywhere. The non-canonical form must be merged into the canonical
form and then deleted.

Default canonical form: PLURAL, capitalized, no special characters.

--- Fix ---

  1. Pick the canonical form (default plural).
  2. Move every page from the non-canonical directory into the canonical
     directory. Rename pages if their names collided with existing ones.
  3. Update every internal link that referenced the non-canonical path.
   4. Update pages.csv rows for every moved page.
  5. Delete the now-empty non-canonical directory.
  6. Verify the canonical Level 2 overview's TOC is complete after the merge.

--- Prevention ---

Before creating any new directory under site/docs/, run:

    ls site/docs/ | grep -i {singular_form}
    ls site/docs/ | grep -i {plural_form}

If either returns a hit, use the existing directory. Do NOT create a
parallel directory in the other form.

--- Audit ---

  [ ] No singular/plural pair of sibling directories exists under site/docs/.
  [ ] The canonical plural form is the only directory for its subject.
  [ ] pages.csv contains no rows referencing the non-canonical form.

