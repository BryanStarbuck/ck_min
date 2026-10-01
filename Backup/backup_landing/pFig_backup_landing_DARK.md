dark_mode = true

# DESIGN MODE: DARK MODE
> This file specifies a **Dark Mode** design.
> Every color, background, border, and text element MUST use the dark mode
> color palette listed here. Do NOT use light mode values anywhere in this file.
>
> Dark Mode Color Palette:
>   Page background:       #15202B
>   Card backgrounds:      #1E2732
>   Hover / elevated:      #253341
>   Borders:               #2F3336
>   Primary text:          #FFFFFF
>   Secondary text:        #8B98A5
>   Accent blue:           #1D9BF0
>   Admin sidebar bg:      #15202B
>   Sidebar border:        #2F3336

---

# Figma Make Prompts — Backup Posts Landing Page (Dark Mode)
# Page: backup_landing | URL: /

> **Navigation Note:** This is a standalone backup web application — NOT the JFKSocial social feed.
> There is NO JFKSocial left sidebar. Navigation is a minimal top bar with logo + CTA buttons.
> Mobile uses a hamburger drawer.

---

## DESIGN TOKEN REFERENCE

### Colors (Dark Mode)
* Page bg:              #15202B
* Card bg:              #1E2732
* Elevated surface:     #253341
* Hover surface:        #253341
* Border:               #2F3336
* Primary text:         #FFFFFF
* Secondary text:       #8B98A5
* Muted text:           #8B98A5 (60% opacity variant)
* Brand blue:           #1D9BF0 (hover #1A8CD8, pressed #1570B8)
* Success green:        #00BA7C
* Danger red:           #F4212E
* Warning yellow:       #FFD400
* Warning orange:       #FF7A00
* CTA band bg:          #1A2942 (dark blue tint)
* Ghost button border:  #2F3336

### Typography
* Font: "TwitterChirp", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif
* Hero headline:        48px / 800 / #FFFFFF
* Section titles:       31px / 700 / #FFFFFF
* Card titles:          20px / 700 / #FFFFFF
* Feature card titles:  17px / 700 / #FFFFFF
* Body copy:            15px / 400 / #8B98A5
* Price:                32px / 800 / #FFFFFF
* Plan name:            20px / 700 / #FFFFFF
* Small / caption:      13px / 400 / #8B98A5
* Nav links:            15px / 500 / #FFFFFF
* Subheadline:          18px / 400 / #8B98A5, max-width 560px

### Spacing
* Base unit: 4px
* xs: 4px | sm: 8px | md: 16px | lg: 24px | xl: 32px | xxl: 48px

### Radii
* Cards: 24px
* Buttons: 9999px (pill)
* Avatars: 50%
* Media: 20px

### Shadows
* Card hover: 0 4px 12px rgba(0,0,0,0.30)
* FAB: 0 0 0 1px rgba(0,0,0,0.20), 0 4px 12px rgba(0,0,0,0.40)

### Breakpoints
* Desktop: >= 1024px | max-width 1200px centered
* Tablet: 640px–1023px (2-column)
* Mobile: < 640px (single column, stacked)

---

## PROMPT 1 — App Shell & Top Navigation Bar

Create the fixed top navigation bar for the Backup Posts standalone web app in dark mode.

**Container:**
- Full-width fixed bar, height 64px
- Background: #15202B (solid, no transparency until scroll)
- Border-bottom: 1px solid transparent initially; on scroll gains 1px solid #2F3336
- z-index 1000

**Left: Logo**
- Shield icon (24px, #1D9BF0 fill) + "Backup Posts" wordmark
- Font: 17px / 700 / #FFFFFF
- Gap 8px between icon and text

**Center: Nav Links**
- "Features" | "Pricing" | "FAQ"
- 15px / 500 / #8B98A5
- Hover: #FFFFFF
- Letter-spacing: normal
- Gap 32px between links

**Right: Action Buttons**
- "Login" — ghost pill button: border 1px #2F3336, text #FFFFFF, height 36px, padding 0 16px, radius 9999px
- "Get Started Free" — filled blue pill: bg #1D9BF0, text #FFFFFF, height 36px, padding 0 20px, radius 9999px, font 15px/700
- Gap 12px between buttons

**Mobile (< 640px):**
- Left: hamburger menu icon (☰) 24px, #FFFFFF
- Center: Logo only (shield icon + wordmark)
- Right: "Login" text link, #1D9BF0, 15px/600
- Height 56px

---

## PROMPT 2 — Hero Section

Create the hero section, full-width, page background #15202B, vertically centered content.

**Layout:**
- Max-width 700px, centered horizontally
- Padding: 80px 24px 64px
- Text align: center

**Headline:**
- "Your Posts. Your Data. Always."
- 48px / 800 / #FFFFFF
- Line-height 1.1
- Margin-bottom 16px

**Subhead:**
- "Back up your Twitter/X posts before they're gone. Protect against censorship and account bans."
- 18px / 400 / #8B98A5
- Max-width 520px, centered
- Margin-bottom 32px

**CTA Row:**
- Flex row, gap 12px, justify-content center
- "Get Started Free" — filled blue pill: bg #1D9BF0, text #FFFFFF, height 52px, padding 0 28px, font 17px/700, radius 9999px
- "Learn More" — ghost pill: border 1px #2F3336, text #FFFFFF, height 52px, padding 0 24px, font 17px/600, radius 9999px, hover bg #253341
- Mobile: stacked full-width, gap 12px

**Hero Illustration:**
- Placeholder screenshot/illustration card below CTAs
- Max-width 860px, margin 40px auto 0
- Card: bg #1E2732, border 1px #2F3336, radius 20px, padding 8px
- Inner image/screenshot area: full-width, height 460px, bg #253341, radius 16px
- Subtle glow: box-shadow 0 0 40px rgba(29,155,240,0.12)

---

## PROMPT 3 — "How It Works" Section

Create the "How It Works" three-step horizontal card row.

**Section container:**
- Padding: 64px 24px
- Background: #15202B
- Border-top: 1px solid #2F3336

**Section title:**
- "How It Works"
- 31px / 700 / #FFFFFF
- Text-align center
- Margin-bottom 40px

**Card row:**
- 3 cards in a horizontal row, gap 20px
- Max-width 900px, centered

**Each card:**
- Background: #1E2732
- Border: 1px solid #2F3336
- Border-radius: 24px
- Padding: 28px 24px

**Card 1 — Connect:**
- Icon: Chrome/browser icon, 40px, #1D9BF0
- Title: "1. Connect" — 17px / 700 / #FFFFFF, margin-top 12px
- Body: "Install our Chrome extension or use API" — 15px / 400 / #8B98A5, margin-top 8px

**Card 2 — Configure:**
- Icon: Settings/gear icon, 40px, #1D9BF0
- Title: "2. Configure" — 17px / 700 / #FFFFFF
- Body: "Choose what to back up and how often to sync"

**Card 3 — Protected:**
- Icon: Shield icon, 40px, #00BA7C
- Title: "3. Protected" — 17px / 700 / #FFFFFF
- Body: "Your posts are safe, always accessible"

**Mobile:** Stack 3 cards vertically, full-width

---

## PROMPT 4 — Key Features Grid

Create the Key Features section with a 2×3 grid.

**Section container:**
- Padding: 64px 24px
- Background: #1E2732 (slightly lighter than page bg for section contrast)

**Section title:**
- "Key Features"
- 31px / 700 / #FFFFFF, text-align center, margin-bottom 40px

**Grid:**
- 3 columns × 2 rows = 6 cards, gap 16px
- Max-width 900px, centered

**Each feature card:**
- Background: #15202B
- Border: 1px solid #2F3336
- Border-radius: 16px
- Padding: 20px
- Hover: border-color #1D9BF0, box-shadow 0 4px 12px rgba(0,0,0,0.20)

**Card content:**
- Checkmark icon: 20px, #00BA7C
- Title: 17px / 700 / #FFFFFF, margin-top 8px
- Body: 15px / 400 / #8B98A5, margin-top 4px

**Features (6 cards):**
1. "Automatic Daily Backups" — "Never lose a post. Daily sync keeps your archive fresh."
2. "Your Data Your Control" — "Export anytime to Nostr, JSON, CSV, or YAML."
3. "Posts + Followers + Media" — "Complete backup of your entire social presence."
4. "Export Anywhere" — "Seamlessly port your data to any platform."
5. "Censorship Detection" — "We flag when your content is removed or suppressed."
6. "Privacy + Encryption" — "AES-256 encryption. Only you can access your backups."

**Mobile:** 1 column stacked, full-width cards

---

## PROMPT 5 — Trust Signals (Stats + Testimonials)

Create the social proof section.

**Section container:**
- Padding: 64px 24px
- Background: #15202B
- Border-top: 1px solid #2F3336

**Stat bar:**
- "Backed up 2.4M posts for 50,000+ users"
- 23px / 700 / #FFFFFF
- Text-align center
- Margin-bottom 40px

**Testimonial cards — 3-column row:**
- Max-width 860px, centered, gap 20px

**Each testimonial card:**
- Background: #1E2732
- Border: 1px solid #2F3336
- Border-radius: 24px
- Padding: 24px

**Card content:**
- Avatar: 48px circle, #253341 bg (placeholder), 50% radius
- Quote: "Life saver" / "Highly secure" / "Best backup tool" — 15px / 400 / #FFFFFF, margin-top 12px, italic
- Handle: "@user1" / "@user2" / "@user3" — 13px / 400 / #8B98A5, margin-top 8px

**Mobile:** Stack 3 testimonials vertically

---

## PROMPT 6 — Pricing Section

Create the 4-plan pricing cards row. Section anchor: #pricing

**Section container:**
- Padding: 64px 24px
- Background: #1E2732

**Section title:**
- "Plans & Pricing"
- 31px / 700 / #FFFFFF, text-align center, margin-bottom 40px

**Card row:**
- 4 cards in a row, gap 16px, max-width 1040px, centered
- Mobile: horizontal swipe carousel with dot pagination "1 of 4"

**Each plan card:**
- Background: #15202B
- Border: 1px solid #2F3336
- Border-radius: 24px
- Padding: 28px 24px

**Creator card (highlighted):**
- Background: #1E2732 (slightly elevated)
- Border: 2px solid #1D9BF0
- Box-shadow: 0 0 0 1px #1D9BF0 at 30% opacity
- "Most Popular" pill: bg #1D2D3E, text #1D9BF0, 9999px, 11px/700, positioned top-right inside card

**Each card content:**
- Plan name: 20px / 700 / #FFFFFF, margin-bottom 8px
- Price: 32px / 800 / #FFFFFF
- Per-month label: "/ mo" — 15px / 400 / #8B98A5
- Feature list: 3–5 items, checkmark #00BA7C + text 14px/400/#8B98A5, gap 8px, margin 20px 0
- CTA button (filled blue or ghost depending on plan)

**Plans:**
1. Free: $0/mo — "100MB storage, 1 account, Daily sync"
2. Creator: $9/mo — "10GB storage, 5 accounts, Every 12h sync" (highlighted)
3. Studio: $29/mo — "100GB storage, 20 accounts, Every 6h sync"
4. Enterprise: Custom — "1TB+ storage, Unlimited accounts, SLA"

---

## PROMPT 7 — FAQ Accordion Section

Create the FAQ accordion. Section anchor: #faq

**Section container:**
- Padding: 64px 24px
- Background: #15202B
- Border-top: 1px solid #2F3336

**Section title:**
- "Frequently Asked Questions"
- 31px / 700 / #FFFFFF, text-align center, margin-bottom 40px

**Accordion container:**
- Max-width 720px, centered
- 5 accordion items, divider 1px #2F3336 between each

**Accordion item (default collapsed):**
- Row height: min 52px (touch-safe)
- Question: 16px / 600 / #FFFFFF
- Chevron "›" icon: 20px, #8B98A5, rotates 90° when expanded, transition 200ms

**First item pre-expanded:**
- Q: "How does the backup work?"
- A: "We use a Chrome extension to read your profile when you visit Twitter/X. All data is securely sent to your backup account. No API keys needed."
- Answer text: 15px / 400 / #8B98A5, padding 0 0 16px
- Height transition: smooth 200ms ease-out

**Remaining questions:**
- Q2: "Is my data secure?" → A2: AES-256 encryption, only you can access
- Q3: "Can I export to other platforms?" → A3: Nostr, Mastodon, JSON, CSV, YAML
- Q4: "What happens if X/Twitter changes its policies?" → A4: Chrome extension reads profile page directly
- Q5: "How much storage do I get?" → A5: Free 100MB, Creator 10GB, Studio 100GB, Enterprise 1TB+

---

## PROMPT 8 — Final CTA Band

Create the final call-to-action band.

**Container:**
- Full-width
- Background: #1A2942 (dark blue tint)
- Border-top: 1px solid #2F3336
- Padding: 64px 24px
- Text-align: center

**Content:**
- Headline: "Ready to protect your posts?" — 31px / 700 / #FFFFFF, margin-bottom 20px
- CTA button: "Get Started Free Today" — filled blue pill, bg #1D9BF0, text #FFFFFF, height 56px, padding 0 36px, font 17px/700, radius 9999px, hover bg #1A8CD8
- Note below button: "No credit card required" — 13px / 400 / #8B98A5, margin-top 12px

---

## PROMPT 9 — Footer

Create the 4-column footer.

**Container:**
- Background: #1E2732
- Border-top: 1px solid #2F3336
- Padding: 48px 24px 24px

**4-column grid:**
- Max-width 1100px, centered, gap 40px

**Column 1 — Brand:**
- Shield icon + "Backup Posts" — 17px/700/#FFFFFF
- Tagline: "Protect your social media presence." — 14px/400/#8B98A5, margin-top 8px

**Column 2 — Product:**
- Heading: "Product" — 13px/700/#8B98A5 uppercase, margin-bottom 16px
- Links: Features, Pricing, FAQ — 14px/400/#FFFFFF, gap 8px, hover #1D9BF0

**Column 3 — Company:**
- Heading: "Company" — 13px/700/#8B98A5 uppercase
- Links: About, Blog, Contact

**Column 4 — Resources & Legal:**
- Heading: "Resources" — 13px/700/#8B98A5 uppercase
- Links: Docs, Help Center, Status, Privacy, Terms, Security

**Bottom bar:**
- Border-top: 1px solid #2F3336, padding-top 16px, margin-top 32px
- "© 2026 JFKSocial.com — Part of the Social Network Ecosystem" — 13px/400/#8B98A5
- Text-align center

**Mobile:** Single column, links listed vertically, reduced padding

---

## COMPONENT VARIANTS

### 1. CTA Button — Primary (Dark Mode)
- Default: bg #1D9BF0, text #FFFFFF, radius 9999px, height 52px, font 17px/700
- Hover: bg #1A8CD8
- Pressed: bg #1570B8
- Disabled: bg #253341, text #8B98A5, cursor not-allowed

### 2. CTA Button — Ghost (Dark Mode)
- Default: bg transparent, border 1px #2F3336, text #FFFFFF, radius 9999px
- Hover: bg #253341
- Pressed: bg #2F3336

### 3. Pricing Card — Default (Dark Mode)
- bg #15202B, border 1px #2F3336, radius 24px
- Hover: box-shadow 0 4px 12px rgba(0,0,0,0.30), translateY(-2px), transition 200ms

### 4. Pricing Card — Highlighted (Creator)
- bg #1E2732, border 2px #1D9BF0, radius 24px
- "Most Popular" badge: bg #1D2D3E, text #1D9BF0

### 5. FAQ Accordion Item
- Collapsed: question #FFFFFF, chevron #8B98A5
- Expanded: question #1D9BF0, chevron rotated 90°, answer bg none, answer text #8B98A5

### 6. Feature Card (Dark Mode)
- bg #15202B, border 1px #2F3336, radius 16px
- Hover: border-color #1D9BF0

### 7. How It Works Step Card
- bg #1E2732, border 1px #2F3336, radius 24px
- Icon color: #1D9BF0 (first 2) / #00BA7C (step 3)

### 8. Testimonial Card
- bg #1E2732, border 1px #2F3336, radius 24px
- Avatar placeholder: #253341 bg

### 9. Top Nav Bar (Dark Mode)
- Scrolled state: bg #15202B (solid), border-bottom 1px #2F3336
- Logo text: #FFFFFF

### 10. Mobile Drawer Nav
- Slide-out from left, bg #1E2732, border-right 1px #2F3336
- Items: 17px/500/#FFFFFF, 52px height, dividers #2F3336
