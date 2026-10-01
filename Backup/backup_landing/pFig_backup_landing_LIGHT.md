dark_mode = false

# DESIGN MODE: LIGHT MODE
> This file specifies a **Light Mode** design.
> Every color, background, border, and text element MUST use the light mode
> color palette listed here. Do NOT use dark mode values anywhere in this file.
>
> Light Mode Color Palette:
>   Page background:       #FFFFFF
>   Card backgrounds:      #F7F9F9
>   Elevated surfaces:     #EFF3F4
>   Borders (subtle):      #EFF3F4
>   Borders (prominent):   #CFD9DE
>   Primary text:          #0F1419
>   Secondary text:        #536471
>   Accent blue:           #1D9BF0

---

# Figma Make Prompts — Backup Posts Landing Page (Light Mode)
# Page: backup_landing | URL: /

> **Navigation Note:** This is a standalone backup web application — NOT the JFKSocial social feed.
> There is NO JFKSocial left sidebar. Navigation is a minimal top bar with logo + CTA buttons.
> Mobile uses a hamburger drawer.

---

## DESIGN TOKEN REFERENCE

### Colors (Light Mode)
* Page bg:              #FFFFFF
* Card bg:              #F7F9F9
* Elevated surface:     #EFF3F4
* Border subtle:        #EFF3F4
* Border prominent:     #CFD9DE
* Primary text:         #0F1419
* Secondary text:       #536471
* Muted text:           #8B98A5
* Brand blue:           #1D9BF0 (hover #1A8CD8, pressed #1570B8)
* Success green:        #00BA7C
* Danger red:           #F4212E
* Warning yellow:       #FFD400
* Warning orange:       #FF7A00
* CTA band bg:          #EBF5FF

### Typography
* Font: "TwitterChirp", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif
* Hero headline:        48px / 800 / #0F1419
* Section titles:       31px / 700 / #0F1419
* Card titles:          20px / 700 / #0F1419
* Feature card titles:  17px / 700 / #0F1419
* Body copy:            15px / 400 / #536471
* Price:                32px / 800 / #0F1419
* Plan name:            20px / 700 / #0F1419
* Small / caption:      13px / 400 / #8B98A5
* Nav links:            15px / 500 / #0F1419
* Subheadline:          18px / 400 / #536471, max-width 560px

### Spacing
* Base unit: 4px
* xs: 4px | sm: 8px | md: 16px | lg: 24px | xl: 32px | xxl: 48px

### Radii
* Cards: 24px
* Buttons: 9999px (pill)
* Avatars: 50%
* Media: 20px

### Shadows
* Card hover: 0 4px 12px rgba(15,20,25,0.10)
* FAB: 0 0 0 1px rgba(15,20,25,0.08), 0 4px 12px rgba(15,20,25,0.15)

### Breakpoints
* Desktop: >= 1024px | max-width 1200px centered
* Tablet: 640px–1023px (2-column)
* Mobile: < 640px (single column, stacked)

---

## PROMPT 1 — App Shell & Top Navigation Bar

Create the fixed top navigation bar for the Backup Posts standalone web app in light mode.

**Container:**
- Full-width fixed bar, height 64px
- Background: #FFFFFF (solid)
- Border-bottom: 1px solid transparent initially; on scroll gains 1px solid #EFF3F4
- z-index 1000

**Left: Logo**
- Shield icon (24px, #1D9BF0 fill) + "Backup Posts" wordmark
- Font: 17px / 700 / #0F1419
- Gap 8px between icon and text

**Center: Nav Links**
- "Features" | "Pricing" | "FAQ"
- 15px / 500 / #536471
- Hover: #0F1419
- Gap 32px between links

**Right: Action Buttons**
- "Login" — ghost pill button: border 1px #CFD9DE, text #0F1419, height 36px, padding 0 16px, radius 9999px
- "Get Started Free" — filled blue pill: bg #1D9BF0, text #FFFFFF, height 36px, padding 0 20px, radius 9999px, font 15px/700
- Gap 12px between buttons

**Mobile (< 640px):**
- Left: hamburger menu icon (☰) 24px, #0F1419
- Center: Logo only (shield icon + wordmark)
- Right: "Login" text link, #1D9BF0, 15px/600
- Height 56px

---

## PROMPT 2 — Hero Section

Create the hero section, full-width white background.

**Layout:**
- Max-width 700px, centered horizontally
- Padding: 80px 24px 64px
- Text align: center

**Headline:**
- "Your Posts. Your Data. Always."
- 48px / 800 / #0F1419
- Line-height 1.1
- Margin-bottom 16px

**Subhead:**
- "Back up your Twitter/X posts before they're gone. Protect against censorship and account bans."
- 18px / 400 / #536471
- Max-width 520px, centered
- Margin-bottom 32px

**CTA Row:**
- Flex row, gap 12px, justify-content center
- "Get Started Free" — filled blue pill: bg #1D9BF0, text #FFFFFF, height 52px, padding 0 28px, font 17px/700, radius 9999px
- "Learn More" — ghost pill: border 1px #CFD9DE, text #0F1419, height 52px, padding 0 24px, font 17px/600, radius 9999px, hover bg #F7F9F9
- Mobile: stacked full-width, gap 12px

**Hero Illustration:**
- Placeholder screenshot/illustration card below CTAs
- Max-width 860px, margin 40px auto 0
- Card: bg #F7F9F9, border 1px #EFF3F4, radius 20px, padding 8px
- Inner area: full-width, height 460px, bg #EFF3F4, radius 16px

---

## PROMPT 3 — "How It Works" Section

Create the "How It Works" three-step horizontal card row.

**Section container:**
- Padding: 64px 24px
- Background: #F7F9F9
- Border-top: 1px solid #EFF3F4

**Section title:**
- "How It Works"
- 31px / 700 / #0F1419
- Text-align center
- Margin-bottom 40px

**Card row:**
- 3 cards in a horizontal row, gap 20px
- Max-width 900px, centered

**Each card:**
- Background: #FFFFFF
- Border: 1px solid #EFF3F4
- Border-radius: 24px
- Padding: 28px 24px

**Card 1 — Connect:**
- Icon: Chrome/browser icon, 40px, #1D9BF0
- Title: "1. Connect" — 17px / 700 / #0F1419, margin-top 12px
- Body: "Install our Chrome extension or use API" — 15px / 400 / #536471, margin-top 8px

**Card 2 — Configure:**
- Icon: Settings/gear icon, 40px, #1D9BF0
- Title: "2. Configure" — 17px / 700 / #0F1419
- Body: "Choose what to back up and how often to sync"

**Card 3 — Protected:**
- Icon: Shield icon, 40px, #00BA7C
- Title: "3. Protected" — 17px / 700 / #0F1419
- Body: "Your posts are safe, always accessible"

**Mobile:** Stack 3 cards vertically, full-width

---

## PROMPT 4 — Key Features Grid

Create the Key Features section with a 2×3 grid.

**Section container:**
- Padding: 64px 24px
- Background: #FFFFFF

**Section title:**
- "Key Features"
- 31px / 700 / #0F1419, text-align center, margin-bottom 40px

**Grid:**
- 3 columns × 2 rows = 6 cards, gap 16px
- Max-width 900px, centered

**Each feature card:**
- Background: #F7F9F9
- Border: 1px solid #EFF3F4
- Border-radius: 16px
- Padding: 20px
- Hover: box-shadow 0 4px 12px rgba(15,20,25,0.10), translateY(-2px)

**Card content:**
- Checkmark icon: 20px, #00BA7C
- Title: 17px / 700 / #0F1419, margin-top 8px
- Body: 15px / 400 / #536471, margin-top 4px

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
- Background: #F7F9F9
- Border-top: 1px solid #EFF3F4

**Stat bar:**
- "Backed up 2.4M posts for 50,000+ users"
- 23px / 700 / #0F1419
- Text-align center
- Margin-bottom 40px

**Testimonial cards — 3-column row:**
- Max-width 860px, centered, gap 20px

**Each testimonial card:**
- Background: #FFFFFF
- Border: 1px solid #EFF3F4
- Border-radius: 24px
- Padding: 24px

**Card content:**
- Avatar: 48px circle, #EFF3F4 bg (placeholder), 50% radius
- Quote: "Life saver" / "Highly secure" / "Best backup tool" — 15px / 400 / #0F1419, margin-top 12px
- Handle: "@user1" / "@user2" / "@user3" — 13px / 400 / #536471, margin-top 8px

**Mobile:** Stack 3 testimonials vertically

---

## PROMPT 6 — Pricing Section

Create the 4-plan pricing cards row. Section anchor: #pricing

**Section container:**
- Padding: 64px 24px
- Background: #FFFFFF

**Section title:**
- "Plans & Pricing"
- 31px / 700 / #0F1419, text-align center, margin-bottom 40px

**Card row:**
- 4 cards in a row, gap 16px, max-width 1040px, centered
- Mobile: horizontal swipe carousel with dot pagination "1 of 4"

**Each plan card:**
- Background: #F7F9F9
- Border: 1px solid #EFF3F4
- Border-radius: 24px
- Padding: 28px 24px
- Hover: box-shadow 0 4px 12px rgba(15,20,25,0.10), translateY(-2px), transition 200ms

**Creator card (highlighted):**
- Background: #FFFFFF
- Border: 2px solid #1D9BF0
- "Most Popular" pill: bg #EBF5FF, text #1D9BF0, 9999px, 11px/700

**Each card content:**
- Plan name: 20px / 700 / #0F1419, margin-bottom 8px
- Price: 32px / 800 / #0F1419
- Per-month label: "/ mo" — 15px / 400 / #536471
- Feature list: checkmark #00BA7C + text 14px/400/#536471, gap 8px, margin 20px 0
- CTA: "Get Started" (filled blue for highlighted), "Start Free" (ghost for others)

**Plans:**
1. Free: $0/mo
2. Creator: $9/mo (highlighted)
3. Studio: $29/mo
4. Enterprise: Custom

---

## PROMPT 7 — FAQ Accordion Section

Create the FAQ accordion. Section anchor: #faq

**Section container:**
- Padding: 64px 24px
- Background: #F7F9F9
- Border-top: 1px solid #EFF3F4

**Section title:**
- "Frequently Asked Questions"
- 31px / 700 / #0F1419, text-align center, margin-bottom 40px

**Accordion container:**
- Max-width 720px, centered
- 5 items, divider 1px #EFF3F4 between each

**Accordion item:**
- Row height: min 52px
- Question: 16px / 600 / #0F1419
- Chevron: 20px, #536471, rotates 90° when expanded, transition 200ms

**First item pre-expanded:**
- Q: "How does the backup work?"
- A: "We use a Chrome extension to read your profile when you visit Twitter/X. All data is securely sent to your backup account. No API keys needed."
- Answer text: 15px / 400 / #536471, padding 0 0 16px

---

## PROMPT 8 — Final CTA Band

Create the final call-to-action band.

**Container:**
- Full-width
- Background: #EBF5FF
- Border-top: 1px solid #CFD9DE
- Padding: 64px 24px
- Text-align: center

**Content:**
- Headline: "Ready to protect your posts?" — 31px / 700 / #0F1419, margin-bottom 20px
- CTA button: "Get Started Free Today" — filled blue pill, bg #1D9BF0, text #FFFFFF, height 56px, padding 0 36px, font 17px/700, radius 9999px, hover bg #1A8CD8
- Note: "No credit card required" — 13px / 400 / #536471, margin-top 12px

---

## PROMPT 9 — Footer

Create the 4-column footer.

**Container:**
- Background: #F7F9F9
- Border-top: 1px solid #EFF3F4
- Padding: 48px 24px 24px

**4-column grid:**
- Max-width 1100px, centered, gap 40px

**Column 1 — Brand:**
- Shield icon + "Backup Posts" — 17px/700/#0F1419
- Tagline: "Protect your social media presence." — 14px/400/#536471

**Column 2 — Product:**
- Heading: "Product" — 13px/700/#8B98A5 uppercase
- Links: Features, Pricing, FAQ — 14px/400/#0F1419, hover #1D9BF0

**Column 3 — Company:**
- Heading: "Company" — 13px/700/#8B98A5 uppercase
- Links: About, Blog, Contact

**Column 4 — Resources & Legal:**
- Heading: "Resources" — 13px/700/#8B98A5 uppercase
- Links: Docs, Help Center, Status, Privacy, Terms, Security

**Bottom bar:**
- Border-top: 1px solid #EFF3F4, padding-top 16px, margin-top 32px
- "© 2026 JFKSocial.com — Part of the Social Network Ecosystem" — 13px/400/#8B98A5, text-align center

---

## COMPONENT VARIANTS

### 1. CTA Button — Primary (Light Mode)
- Default: bg #1D9BF0, text #FFFFFF, radius 9999px, height 52px, font 17px/700
- Hover: bg #1A8CD8
- Pressed: bg #1570B8
- Disabled: bg #EFF3F4, text #8B98A5

### 2. CTA Button — Ghost
- Default: bg transparent, border 1px #CFD9DE, text #0F1419, radius 9999px
- Hover: bg #F7F9F9

### 3. Pricing Card — Default
- bg #F7F9F9, border 1px #EFF3F4, radius 24px
- Hover: box-shadow 0 4px 12px rgba(15,20,25,0.10), translateY(-2px)

### 4. Pricing Card — Highlighted (Creator)
- bg #FFFFFF, border 2px #1D9BF0, radius 24px
- "Most Popular" badge: bg #EBF5FF, text #1D9BF0

### 5. FAQ Accordion Item
- Collapsed: question #0F1419, chevron #536471
- Expanded: chevron rotated 90°, answer text #536471

### 6. Feature Card
- bg #F7F9F9, border 1px #EFF3F4, radius 16px
- Hover: box-shadow 0 4px 12px rgba(15,20,25,0.10)

### 7. How It Works Step Card
- bg #FFFFFF, border 1px #EFF3F4, radius 24px

### 8. Testimonial Card
- bg #FFFFFF, border 1px #EFF3F4, radius 24px
- Avatar placeholder: #EFF3F4 bg

### 9. Top Nav Bar (Light Mode)
- Scrolled state: bg #FFFFFF (solid), border-bottom 1px #EFF3F4

### 10. Mobile Drawer Nav
- Slide-out from left, bg #FFFFFF, border-right 1px #EFF3F4
- Items: 17px/500/#0F1419, 52px height
