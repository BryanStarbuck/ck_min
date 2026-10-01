pFig — backup_landing
Figma Make Prompts: Backup Posts Landing Page
=============================================

DESIGN TOKEN REFERENCE
=======================

Colors
* Page bg: #FFFFFF
* Card bg: #F7F9F9
* Elevated surface: #EFF3F4
* Border subtle: #EFF3F4
* Border prominent: #CFD9DE
* Primary text: #0F1419
* Secondary text: #536471
* Muted text: #8B98A5
* Brand blue: #1D9BF0 (hover #1A8CD8, pressed #1570B8)
* Success green: #00BA7C
* Danger red: #F4212E
* Warning yellow: #FFD400
* CTA band bg: #EBF5FF

Typography
* Font: "TwitterChirp", system-ui, -apple-system, sans-serif
* Hero headline: 48px / 800 / #0F1419
* Section titles: 31px / 700 / #0F1419
* Card titles: 20px / 700 / #0F1419
* Feature card titles: 17px / 700 / #0F1419
* Body copy: 15px / 400 / #536471
* Price: 32px / 800 / #0F1419
* Plan name: 20px / 700 / #0F1419
* Small / caption: 13px / 400 / #8B98A5
* Nav links: 15px / 500 / #0F1419

Spacing
* Base unit: 4px
* xs: 4px | sm: 8px | md: 16px | lg: 24px | xl: 32px

Radii
* Cards: 24px
* Buttons: 9999px (pill)
* Avatars: 50%

Shadows
* Card hover: 0 4px 12px rgba(15,20,25,0.10)
* FAB: 0 0 0 1px rgba(15,20,25,0.08), 0 4px 12px rgba(15,20,25,0.15)

Breakpoints
* Desktop: >= 1024px (3-column, max-width 1200px centered)
* Tablet: 640px–1023px (2-column)
* Mobile: < 640px (1-column, full-width)


====================================================================
PROMPT 1 — App Shell and Top Navigation Bar
====================================================================

Create the app shell and fixed top navigation bar for the Backup Posts landing page.

The page background is #FFFFFF. Use font "TwitterChirp", system-ui, sans-serif throughout.

Navigation bar (desktop, >=1024px):
* Fixed position at top. Full page width. Height: 64px. Background #FFFFFF. 
  On scroll: add 1px bottom border #EFF3F4.
* Max content width: 1200px centered with auto left/right margins.
* Left: Shield icon (24x24, color #1D9BF0) followed by wordmark "Backup Posts" in
  20px/700/#0F1419. Together form the logo. Click target: entire left zone.
* Center: Three text links "Features" / "Pricing" / "FAQ". 15px/500/#0F1419.
  Hover: color #1D9BF0. Gap between links: 32px.
* Right: "Login" ghost pill button (transparent bg, 1px border #1D9BF0, #1D9BF0 text,
  9999px radius, height 40px, padding 0 20px, 15px/700) then "Get Started Free"
  filled pill button (#1D9BF0 bg, #FFFFFF text, 9999px radius, height 40px,
  padding 0 20px, 15px/700). Gap: 12px.

Navigation bar (mobile, <640px):
* Height: 56px. Background #FFFFFF. Border-bottom 1px #EFF3F4.
* Left: hamburger icon (☰), 24px, #0F1419, tap target 44x44px.
* Center: shield icon + "Backup Posts" wordmark (16px/700).
* Right: "Login" text link, 15px/700/#1D9BF0.
* Drawer (slides in from left, 280px wide, full height, white bg, z-index 100):
  Links stacked 56px each: Features, Pricing, FAQ, Login, Get Started Free.
  "Get Started Free" is a full-width blue pill button at bottom.

Authenticated state variant:
* Desktop right zone: user avatar (32px circle, 50% radius, border 1px #EFF3F4),
  handle text 15px/400/#0F1419, chevron, then "Go to Dashboard" filled pill button.
* "Login" and "Get Started Free" are replaced in this variant.


====================================================================
PROMPT 2 — Hero Section
====================================================================

Create the hero section immediately below the navigation bar. Reference the ASCII
layout in Page_Landing_Web_UI.md: centered text block with two CTAs and an
illustration below.

Desktop:
* Section: full page width, white bg, padding-top 96px, padding-bottom 80px.
* Max content width: 800px, centered.
* Headline: "Your Posts. Your Data. Always." — 48px/800/#0F1419, text-align center,
  line-height 1.2.
* Subhead (below headline, margin-top 16px): "Back up your Twitter/X posts before
  they're gone. Protect against censorship and account bans." — 18px/400/#536471,
  text-align center, max-width 560px, centered.
* CTA row (margin-top 32px, display flex, gap 16px, justify-content center):
  * Primary: "Get Started Free" — #1D9BF0 bg, #FFFFFF text, 9999px, height 52px,
    padding 0 28px, 17px/700. Hover: #1A8CD8. Active: #1570B8.
  * Secondary: "Learn More" — transparent bg, 1px solid #1D9BF0, #1D9BF0 text,
    9999px, height 52px, padding 0 28px, 17px/700.
* Illustration placeholder (margin-top 48px): rounded rectangle 860x480px,
  background #F7F9F9, border 1px #EFF3F4, radius 24px. Contains centered text
  "Product Screenshot" in 15px/400/#8B98A5.

Mobile (<640px):
* Padding-top 64px, padding-bottom 48px, horizontal padding 20px.
* Headline: 36px/800, text-align left (not centered).
* Subhead: 16px/400, text-align left.
* CTA buttons: full-width, stacked vertically (primary first, gap 12px), height 52px.
* Illustration: full-width, aspect-ratio 16/9, radius 16px.


====================================================================
PROMPT 3 — How It Works (3-Step Section)
====================================================================

Create the "How It Works" section. Reference the 3-card row in the web ASCII mockup
and the stacked single-column cards in the mobile ASCII mockup.

Desktop:
* Section: white bg, padding 80px 0. Max content width 1200px centered.
* Section title: "How It Works" — 31px/700/#0F1419, text-align center,
  margin-bottom 48px.
* 3 cards in a horizontal row, equal width, gap 24px.
* Each card: background #F7F9F9, border 1px #EFF3F4, radius 24px, padding 32px 28px.
  * Step number: "1." / "2." / "3." — 13px/700/#1D9BF0 pill tag (#EBF5FF bg,
    #1D9BF0 text, 9999px, height 24px, padding 0 10px).
  * Icon (48px circle, background #EBF5FF, icon color #1D9BF0, centered in circle):
    Card 1: Chrome/browser icon | Card 2: Settings gear icon | Card 3: Shield icon.
  * Card title: 20px/700/#0F1419, margin-top 16px.
  * Card body: 15px/400/#536471, margin-top 8px, line-height 1.5.
  * Titles and bodies:
    Card 1: "Connect" / "Install our Chrome extension or use API access"
    Card 2: "Configure" / "Choose what to back up and how often to sync"
    Card 3: "Protected" / "Your posts are safe and always accessible"

Mobile (<640px):
* Cards stacked vertically, full-width, padding 24px, gap 16px.
* Icon 40px circle. Card title 17px/700. Body 15px/400.


====================================================================
PROMPT 4 — Key Features Grid
====================================================================

Create the "Key Features" section with a 2×3 grid of feature cards. Reference the
6 feature cards listed in the web ASCII mockup.

Desktop:
* Section: #F7F9F9 bg, padding 80px 0. Max content width 1200px centered.
* Section title: "Key Features" — 31px/700/#0F1419, centered, margin-bottom 48px.
* Grid: 2 columns, 3 rows. Gap 20px.
* Each feature card: white (#FFFFFF) bg, border 1px #EFF3F4, radius 24px,
  padding 28px 24px, display flex, flex-direction row, align-items flex-start, gap 16px.
  * Icon: 40px circle, background #E8F9F2, border 1px #B7EDD8. Checkmark icon
    24px, color #00BA7C. Positioned left, flex-shrink 0.
  * Right side: title 17px/700/#0F1419, body 15px/400/#536471, margin-top 4px.
* Feature data (title / body):
  1. "Automatic Daily Backups" / "Set it and forget it. New posts backed up every 24 hours."
  2. "Your Data, Your Control" / "Open portable YAML format. Own your data forever."
  3. "Posts, Followers, Media" / "Everything you've shared — text, images, and videos."
  4. "Export Anywhere" / "Nostr, Mastodon, JSON, CSV. Move to any platform."
  5. "Censorship Detection" / "Know when your posts disappear from the platform."
  6. "Privacy & Encryption" / "AES-256 encrypted storage. Only you can access your data."
* Card hover: box-shadow 0 4px 12px rgba(15,20,25,0.08), translateY(-2px), 200ms ease.

Mobile (<640px):
* Single column, stacked. Cards full-width. Grid becomes flex-direction column.


====================================================================
PROMPT 5 — Trust Signals (Stats + Testimonials)
====================================================================

Create the Trust Signals section with a centered stat and 3 testimonial cards.
Reference the social proof section in both web and mobile ASCII mockups.

Desktop:
* Section: white bg, padding 80px 0. Max content width 1000px centered.
* Stat line: "Backed up 2.4M posts for 50,000+ users" — 23px/700/#0F1419,
  text-align center, margin-bottom 48px.
* 3 testimonial cards in a horizontal row, gap 24px.
* Each testimonial card: #F7F9F9 bg, border 1px #EFF3F4, radius 24px, padding 28px.
  * Avatar: 48px circle, background #EFF3F4, 50% radius. (placeholder initials)
  * Quote: 15px/400/#0F1419, line-height 1.5, margin-top 12px, in quotation marks.
    T1: "Life saver — best thing I did to protect my posts."
    T2: "Highly secure. Peace of mind knowing my data is safe."
    T3: "Best backup tool available. Exported everything to Nostr easily."
  * Handle: 13px/400/#536471, margin-top 8px.
    T1: @user1 | T2: @user2 | T3: @user3

Mobile (<640px):
* Stat: text-align left, 20px/700, padding 0 20px.
* Testimonials stacked vertically. Each card full-width, padding 20px, gap 12px.


====================================================================
PROMPT 6 — Pricing Section
====================================================================

Create the Pricing section with 4 plan cards. Reference the 4-column pricing grid
in the web ASCII mockup and the swipe carousel in the mobile ASCII mockup.

Desktop:
* Section: #F7F9F9 bg, padding 80px 0. Max content width 1200px centered.
  Anchor id="pricing".
* Section title: "Simple, Transparent Pricing" — 31px/700/#0F1419, centered.
* Subtitle: "Start free. Upgrade when you need more." — 15px/400/#536471, centered,
  margin-bottom 48px.
* 4 cards in a row, equal width ~270px, gap 20px, align-items flex-start.
* Base card style: white bg, border 1px #EFF3F4, radius 24px, padding 28px 24px.
* Creator card (highlighted): border 2px #1D9BF0, box-shadow 0 0 0 4px #EBF5FF.
  "Most Popular" pill badge: #1D9BF0 bg, #FFFFFF text, 9999px, 11px/700, centered
  above card.
* Each card content:
  * Plan name: 20px/700/#0F1419
  * Price: 32px/800/#0F1419, "/mo" suffix 15px/400/#536471
  * Feature list: 14px/400/#0F1419, 8px gap, each item prefixed with bullet "•" in
    #00BA7C
  * CTA button at bottom: full-width pill, height 44px, 15px/700
    Free: ghost button (#1D9BF0 border+text) | Creator: filled #1D9BF0 bg |
    Studio: filled #1D9BF0 bg | Enterprise: ghost button
  * CTA labels: Free: "Get Started" | Creator: "Get Started" | Studio: "Get Started" |
    Enterprise: "Contact Sales"

Plan data:
  Free: $0/mo | 1 account, 1,000 posts, 100MB storage, Chrome extension
  Creator: $9/mo | 3 accounts, unlimited posts, 10GB, all connection methods, email alerts
  Studio: $29/mo | 10 accounts, unlimited, 100GB, priority support, API access
  Enterprise: Custom | Unlimited accounts, 1TB+, custom retention, SLA, dedicated support

Mobile (<640px):
* Horizontal swipe carousel. Only one card visible at a time, peek of adjacent card.
  Dot pagination: "1 of 4". Dot indicator row: 4 dots, active dot filled #1D9BF0,
  inactive #CFD9DE.
* Cards: full-width minus 40px margin, same visual style as desktop.
* "Most Popular" badge on Creator card preserved.


====================================================================
PROMPT 7 — FAQ Accordion
====================================================================

Create the FAQ accordion section. Reference the expandable items in both web and
mobile ASCII mockups.

Desktop:
* Section: white bg, padding 80px 0. Max content width 760px centered.
  Anchor id="faq".
* Section title: "Frequently Asked Questions" — 31px/700/#0F1419, centered,
  margin-bottom 40px.
* 5 accordion items stacked vertically, gap 0 (bordered list style).
* Each item: border-bottom 1px #EFF3F4. Min-height 56px.
* Item row (collapsed): flex row, align-items center, padding 16px 0.
  * Left: question text 16px/500/#0F1419.
  * Right: chevron icon "▶" 20px, color #536471, flex-shrink 0. Rotates 90° on expand.
* Expanded item: chevron rotates 90°, answer block visible below question row.
  Answer: 15px/400/#536471, padding-bottom 16px, max-width 680px.
  Smooth height animation: 200ms ease-in-out.
* First item pre-expanded on page load.
* 5 items:
  Q1 "How does the backup work?"
  Q2 "Is my data secure?"
  Q3 "Can I export to other platforms?"
  Q4 "What happens if X/Twitter changes its policies?"
  Q5 "How much storage do I get?"
  (Answers: see spec file backup_landing.md COPY section)

Mobile (<640px):
* Same structure. Item min-height 60px (larger touch target).
* Question text 16px/500, padding 0 20px.


====================================================================
PROMPT 8 — Final CTA Band and Footer
====================================================================

Create the final CTA band and the footer. Reference the FINAL CTA and FOOTER sections
in the web ASCII mockup.

Final CTA band (desktop):
* Full-width section. Background #EBF5FF. Padding 80px 40px. Text centered.
* Headline: "Ready to protect your posts?" — 31px/700/#0F1419.
* CTA button (margin-top 24px): "Get Started Free Today" — #1D9BF0 bg, #FFFFFF,
  9999px, height 56px, padding 0 40px, 17px/700. Hover: #1A8CD8.
* Note below button (margin-top 12px): "No credit card required" — 13px/400/#8B98A5.

Footer (desktop):
* Background #FFFFFF, border-top 1px #EFF3F4, padding 56px 0 32px.
* Max content width 1200px centered.
* Top row: 5 columns. Left column 2x width.
  * Column 1: Logo (shield icon + "Backup Posts" wordmark) + tagline "Your social
    media data, safe and portable." 14px/400/#536471.
  * Column 2: "Product" header 13px/700/#0F1419 uppercase, links: Features, Pricing, FAQ
  * Column 3: "Company" header, links: About, Blog, Contact
  * Column 4: "Resources" header, links: Docs, Help Center, Status
  * Column 5: "Legal" header, links: Privacy, Terms, Security
  * All footer links: 14px/400/#536471, hover #1D9BF0, no underline by default.
  * Headers: 11px/700/#8B98A5 uppercase letter-spacing 0.08em.
* Bottom bar (margin-top 40px, border-top 1px #EFF3F4, padding-top 24px):
  "© 2026 JFKSocial.com — Part of the Social Network Ecosystem" — 13px/400/#8B98A5,
  centered.

Mobile (<640px):
* Final CTA: headline left-aligned, button full-width.
* Footer: single column. Logo block, then each column expanded (headers shown,
  links indented). Bottom bar same copy.


====================================================================
COMPONENT VARIANTS
====================================================================

Pricing Card
* variant=free: ghost CTA, no highlight
* variant=creator: highlighted (blue border, shadow), "Most Popular" badge, filled CTA
* variant=studio: filled CTA, no badge
* variant=enterprise: ghost CTA ("Contact Sales"), no price number

FAQ Item
* state=collapsed: question + "▶" chevron
* state=expanded: chevron rotated 90°, answer visible, smooth height transition

Feature Card
* size=default: 28px padding, row layout, 40px icon circle
* size=compact: 20px padding (mobile adaptation)

CTA Button (Primary Filled)
* state=default: #1D9BF0 bg
* state=hover: #1A8CD8 bg
* state=active/pressed: #1570B8 bg
* state=disabled: #8B98A5 bg, cursor not-allowed

CTA Button (Ghost)
* state=default: transparent bg, 1px #1D9BF0 border, #1D9BF0 text
* state=hover: #EBF5FF bg
* state=active: #D6ECFD bg

Testimonial Card
* Contains: avatar circle, quote, handle
* Hover: box-shadow 0 4px 12px rgba(15,20,25,0.08)

Mobile Pricing Carousel Dots
* Dot: 8px circle, inactive #CFD9DE, active #1D9BF0, gap 6px
* Shows position indicator: "1 of 4" in 13px/400/#8B98A5 below dots

Authenticated Nav Variant
* Desktop: avatar 32px circle + handle + chevron + "Go to Dashboard" pill
* Mobile: avatar replaces Login link in top bar header
