backup_landing — Page Spec
=========================

Page ID: backup_landing
URL: /
Portal: main_site (marketing / unauthenticated)
ASCII Sources: Page_Landing_Web_UI.md, Page_Landing_Mobile_UI.md


OVERVIEW
========

Marketing landing page for the Backup Posts feature. Unauthenticated users arrive here
from search, referrals, or the Free Speech Defender wizard. The page sells the product,
explains how it works, shows pricing, and drives signups.

Logged-in users see a "Go to Dashboard" CTA in place of "Get Started" and their avatar
replaces the Login button.


PAGE LAYOUT — DESKTOP
=====================

1. Fixed top navigation bar
   * Logo: shield icon + "Backup Posts" wordmark, left-aligned
   * Nav links: Features, Pricing, FAQ — center
   * Right: Login (ghost button), Get Started Free (filled blue pill button)
   * On scroll: bar gains 1px border-bottom #EFF3F4 and white bg solid

2. Hero section — full-width, white bg, vertically centered
   * Headline: "Your Posts. Your Data. Always." — 48px/800/#0F1419
   * Subhead: "Back up your Twitter/X posts before they're gone. Protect against
     censorship and account bans." — 18px/400/#536471, max-width 560px, centered
   * CTA row: "Get Started Free" (blue pill, 52px, primary) + "Learn More" (ghost pill)
   * Hero illustration/screenshot below CTAs, max-width 860px

3. How It Works — 3 step cards in a horizontal row
   * Section title: "How It Works" — 31px/700, centered
   * Card 1: Chrome Icon, "1. Connect", "Install our Chrome extension or use API"
   * Card 2: Settings Icon, "2. Configure", "Choose what to back up and how often to sync"
   * Card 3: Shield Icon, "3. Protected", "Your posts are safe, always accessible"
   * Card style: 24px radius, #F7F9F9 bg, 24px padding, border #EFF3F4

4. Key Features — 2×3 grid of feature cards
   * Section title: "Key Features" — 31px/700, centered
   * 6 cards, each: checkmark icon (#00BA7C), title 17px/700, body 15px/400/#536471
   * Features: Automatic Daily Backups / Your Data Your Control / Posts + Followers +
     Media / Export Anywhere / Censorship Detection / Privacy + Encryption

5. Trust Signals
   * Centered stat: "Backed up 2.4M posts for 50,000+ users" — 23px/700
   * 3 testimonial cards in a row: avatar (50% circle, 48px), quote, handle

6. Pricing — 4 plan cards in a row
   * Section anchor: #pricing
   * Cards: Free ($0/mo), Creator ($9/mo), Studio ($29/mo), Enterprise (Custom)
   * Each card: plan name 20px/700, price 32px/800, feature list, CTA button
   * Creator card highlighted with blue border #1D9BF0 + "Most Popular" pill badge

7. FAQ — accordion section
   * Section anchor: #faq
   * 5 Q&A items, first item pre-expanded
   * Chevron rotates on expand. Smooth 200ms height transition.
   * Questions: How does backup work? / Is my data secure? / Can I export? /
     What if X changes? / How much storage?

8. Final CTA band — light blue bg (#EBF5FF)
   * "Ready to protect your posts?" — 31px/700
   * "Get Started Free Today" — primary blue pill button, 56px height
   * "No credit card required" — 13px/400/#536471 below button

9. Footer — 4-column grid
   * Logo + tagline left column
   * Columns: Product (Features, Pricing, FAQ) | Company (About, Blog, Contact) |
     Resources (Docs, Help Center, Status) | Legal (Privacy, Terms, Security)
   * Bottom bar: "© 2026 JFKSocial.com — Part of the Social Network Ecosystem"


PAGE LAYOUT — MOBILE
====================

* Top bar: hamburger (☰) left, logo center, Login right
* Hamburger opens slide-out drawer with Features, Pricing, FAQ, Login, Get Started
* Hero: headline splits to 3 lines, buttons stacked full-width (primary then ghost)
* How It Works: 3 cards stacked vertically (full-width)
* Features: 1-column stacked cards
* Social proof: stacked testimonials
* Pricing: horizontal swipe carousel, dot pagination indicator "1 of 4"
* FAQ: same accordion, larger 52px touch targets
* Final CTA: stacked layout
* Footer: single column, links listed vertically


STATES & INTERACTIONS
=====================

Unauthenticated state
* Header shows: Login, Get Started Free
* Hero shows: "Get Started Free" + "Learn More"

Authenticated state
* Header shows: user avatar + handle dropdown, "Go to Dashboard" (replaces Get Started)
* Hero primary CTA changes to "Go to Dashboard"
* Pricing CTAs change to "Upgrade" or "Current Plan" depending on user's plan

FAQ accordion
* Collapsed: shows question + "▶" chevron — 48px row height minimum
* Expanded: chevron rotates 90°, answer fades in over 200ms
* First item pre-expanded on page load

Pricing card states
* Default: #F7F9F9 bg, 1px border #EFF3F4
* Highlighted (Creator): white bg, 2px border #1D9BF0
* Hover (desktop): box-shadow 0 4px 12px rgba(15,20,25,0.10), translateY(-2px)

CTA button states
* Primary default: #1D9BF0 bg, #FFFFFF text
* Primary hover: #1A8CD8 bg
* Primary pressed: #1570B8 bg
* Ghost default: transparent bg, #1D9BF0 border + text
* Ghost hover: #EBF5FF bg


COPY — EXACT TEXT
=================

Page title (browser tab): "Backup Posts — Protect Your Social Media Data"
Hero headline: "Your Posts. Your Data. Always."
Hero subhead: "Back up your Twitter/X posts before they're gone. Protect against censorship and account bans."
Primary CTA: "Get Started Free"
Secondary CTA: "Learn More"
Final CTA headline: "Ready to protect your posts?"
Final CTA button: "Get Started Free Today"
Final CTA note: "No credit card required"
Stats bar: "Backed up 2.4M posts for 50,000+ users"
Testimonial 1: "Life saver" — @user1
Testimonial 2: "Highly secure" — @user2
Testimonial 3: "Best backup tool" — @user3

FAQ items:
Q1: "How does the backup work?"
A1: "We use a Chrome extension to read your profile when you visit Twitter/X. All data is securely sent to your backup account. No API keys needed."
Q2: "Is my data secure?"
A2: "Yes. All data is encrypted with AES-256 during transmission and at rest. Only you can access your backups."
Q3: "Can I export to other platforms?"
A3: "Yes. Export to Nostr, Mastodon, JSON, CSV, or YAML. Your data in your format."
Q4: "What happens if X/Twitter changes its policies?"
A4: "Our Chrome extension reads your profile page directly, so API policy changes don't affect your backups."
Q5: "How much storage do I get?"
A5: "Free plan: 100MB. Creator: 10GB. Studio: 100GB. Enterprise: 1TB+."


NAVIGATION FROM THIS PAGE
=========================

Get Started Free (hero, pricing, final CTA) -> /signup (Main_UI)
Learn More -> smooth scroll to #features
Login -> /login (Main_UI)
Features nav -> smooth scroll to #features
Pricing nav -> smooth scroll to #pricing
FAQ nav -> smooth scroll to #faq
Enterprise Contact -> /help or sales contact form
Footer: Help Center -> /help | Privacy -> /privacy | Terms -> /terms | Status -> /status


NAVIGATION TO THIS PAGE
=======================

* Direct URL (feedbackup.com or jfksocial.com/backup)
* Search engine results
* Referral from Free Speech Defender wizard
* Logout redirect
* Logo click from any unauthenticated page
