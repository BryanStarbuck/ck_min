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

# Figma Make Prompts — Setup: Connect Account (Dark Mode)
# Page: backup_setup_connect | URL: /setup/connect

> **Navigation Note:** This is a standalone backup web application — NOT the JFKSocial social feed.
> There is NO JFKSocial left sidebar. Navigation is a minimal authenticated top bar (logo + account dropdown).
> This is Step 1 of a 3-step wizard.

---

## DESIGN TOKEN REFERENCE

### Colors (Dark Mode)
* Page bg:              #15202B
* Card bg:              #1E2732
* Elevated surface:     #253341
* Borders:              #2F3336
* Primary text:         #FFFFFF
* Secondary text:       #8B98A5
* Muted text:           #8B98A5
* Brand blue:           #1D9BF0
* Success green:        #00BA7C
* Success tint bg:      #0D2818
* Danger red:           #F4212E
* Warning yellow:       #FFD400
* Warning bg tint:      #1A1800

### Typography
* Font: "TwitterChirp", system-ui, -apple-system, BlinkMacSystemFont, sans-serif
* Page title:       23px / 700 / #FFFFFF
* Page subtitle:    15px / 400 / #8B98A5
* Card title:       17px / 700 / #FFFFFF
* Card meta:        13px / 400 / #8B98A5
* Benefit text:     15px / 400 / #FFFFFF
* Warning text:     14px / 400 / #8B98A5
* Label text:       15px / 500 / #8B98A5
* Small caption:    12px / 400 / #8B98A5
* Stepper label:    13px / 500

### Spacing
* Base: 4px | xs: 4px | sm: 8px | md: 16px | lg: 24px | xl: 32px

### Radii
* Cards: 24px | Buttons: 9999px | Inputs: 12px | Badge: 9999px

---

## PROMPT 1 — Minimal Authenticated Header

Create the minimal top navigation bar for an authenticated wizard page.

**Container:**
- Full-width, height 64px
- Background: #15202B (solid)
- Border-bottom: 1px solid #2F3336
- z-index: 1000

**Left: Logo**
- Shield icon (24px, #1D9BF0) + "Backup Posts" wordmark 17px/700/#FFFFFF
- Logo links back to / (landing page)

**Right: Account Controls**
- "Account ▾" — 15px/500/#8B98A5, dropdown arrow
- "Logout" — ghost link, 15px/400/#8B98A5, hover #FFFFFF
- Gap: 20px between them

**No center nav links** — wizard flow, minimal chrome

**Mobile (< 640px):**
- Logo center
- "Account ▾" right, 15px/500/#8B98A5
- Height 56px

---

## PROMPT 2 — Setup Progress Indicator (Step 1 Active)

Create the horizontal step progress indicator showing 3 wizard steps.

**Container:**
- Max-width 480px, centered, margin 32px auto 40px
- Flex row, align-items flex-start

**Step structure (3 steps):**

Step 1 — Connect (ACTIVE):
- Circle: 32px diameter, bg #1D9BF0, label "1" 13px/700/#FFFFFF center
- Label below: "Connect" 13px/700/#FFFFFF
- State: active (current step)

Step 2 — Options (UPCOMING):
- Circle: 32px diameter, bg #253341, label "2" 13px/400/#8B98A5 center
- Label below: "Options" 13px/400/#8B98A5

Step 3 — Backup (UPCOMING):
- Circle: 32px diameter, bg #253341, label "3" 13px/400/#8B98A5 center
- Label below: "Backup" 13px/400/#8B98A5

**Connector lines between circles:**
- Line between step 1→2: 2px solid #2F3336 (not yet reached)
- Line between step 2→3: 2px solid #2F3336

**Mobile:** 3 dots (12px circles) with labels below. Active dot: #1D9BF0. Inactive: #2F3336. Full-width row.

---

## PROMPT 3 — Page Header

Create the page heading block.

**Container:**
- Max-width 680px, centered, text-align center
- Margin-bottom 32px

**Title:**
- "Connect Your Social Media Account"
- 23px / 700 / #FFFFFF

**Subtitle:**
- "Choose how you'd like to back up your posts:"
- 15px / 400 / #8B98A5
- Margin-top 8px

---

## PROMPT 4 — Method Cards (3 Cards)

Create three stacked method cards. Max-width 680px, centered, gap 16px.

**Card A — Chrome Extension (Recommended):**
- Background: #1E2732, border 1px #2F3336, radius 24px, padding 28px

Header row (flex, align-items center, gap 12px):
- Browser/Chrome icon: 32px, #1D9BF0
- "Chrome Extension" — 17px/700/#FFFFFF
- "Recommended" badge: bg #0D2818, text #00BA7C, 11px/700, 9999px, padding 3px 10px

4 benefit rows (gap 8px, margin-top 16px):
- Row layout: checkmark circle 16px #00BA7C + text 15px/400/#FFFFFF, gap 10px
- "No API keys needed"
- "Works even if APIs are restricted"
- "Reads your profile page directly"
- "Most reliable method"

How it works description:
- "Install our Chrome extension, and it will read your Twitter/X profile when you visit it. All data is sent securely to your backup account."
- 14px/400/#8B98A5, margin-top 12px

CTA:
- "Install Extension" — filled blue pill, bg #1D9BF0, text #FFFFFF, height 44px, 15px/700, radius 9999px, right-aligned

---

**Card B — API Connection:**
- Background: #1E2732, border 1px #2F3336, radius 24px, padding 28px

Header row:
- Key icon 32px #8B98A5 + "API Connection" 17px/700/#FFFFFF
- "For developers with Twitter API access" — 13px/400/#8B98A5, margin-top 4px

2 benefit rows (green checkmark):
- "Faster sync than extension"
- "More complete data"

2 warning rows (warning triangle icon 16px #FFD400):
- "Requires developer credentials"
- "Subject to API rate limits"
- Warning text: 14px/400/#8B98A5

CTA: "Connect via API" — ghost pill, border 1px #2F3336, text #1D9BF0, height 44px, 15px/700, right-aligned

Expandable form (hidden by default, expands on CTA click):
- All form fields on dark bg #15202B, border 1px #2F3336, radius 12px, padding 0 16px, height 44px
- Text: 15px/400/#FFFFFF, placeholder #8B98A5
- Fields: Platform dropdown, Handle input, API Key, API Secret (password + show/hide), Access Token, Access Secret
- Help link: "How to get API credentials →" 13px/400/#1D9BF0
- Action row: "Cancel" ghost + "Connect" filled, right-aligned, gap 12px

---

**Card C — Manual Import:**
- Background: #1E2732, border 1px #2F3336, radius 24px, padding 28px

Header row:
- Upload icon 32px #8B98A5 + "Manual Import" 17px/700/#FFFFFF
- "Upload a data export file from your social network" — 13px/400/#8B98A5

2 benefit rows (green checkmark): "Works with Twitter/X data exports" / "One-time import of historical data"
2 warning rows: "Does not support auto-sync" / "Must manually re-import for updates"

CTA: "Upload File" — ghost pill, right-aligned

Expandable drop zone:
- Border: 2px dashed #2F3336, radius 16px, padding 40px, min-height 160px, bg #15202B
- "Drag & drop your data export ZIP here" 15px/400/#8B98A5, text-align center
- "or" — 13px/400/#8B98A5
- "Browse Files" ghost button 40px height
- Below: "Accepted: .zip (Twitter data export) | Max size: 500 MB" 12px/400/#8B98A5
- Help link: "How to download your Twitter data export →" 13px/400/#1D9BF0

---

## PROMPT 5 — Skip Action & Footer

Create the skip button and page footer.

**Skip button:**
- "Skip for Now" — ghost pill, border 1px #2F3336, text #8B98A5, height 44px, 15px/500, radius 9999px
- Centered, margin-top 24px
- Click opens confirmation modal (see component variants)

**Footer bar:**
- "Need help? [Contact Support] | [Help Center]"
- 13px/400/#8B98A5, text-align center
- Links: #1D9BF0 underline on hover
- Margin-top 32px, padding-bottom 40px

---

## PROMPT 6 — Form States & Banners

Create inline state banners for method cards.

**Extension detected (Card A success banner):**
- Background: #0D2818, border 1px #00BA7C, border-radius 12px, padding 12px 16px
- Text: "Extension detected! Click Continue to connect." 14px/600/#00BA7C
- "Continue" button replaces "Install Extension" — filled green bg #00BA7C, text #FFFFFF

**API validation states:**
- Validating: spinner on Connect button, "Validating..." text, button disabled (#253341 bg)
- Success: "✓ Connected!" 13px/600/#00BA7C inline below button; card auto-collapses
- Error inline: "Invalid credentials. Please check and try again." 13px/400/#F4212E below Connect

**File upload states:**
- Uploading: progress bar 4px height inside drop zone, fill #1D9BF0, percentage label 13px/#8B98A5
- Parsing: "Parsing data... this may take a minute" + spinner 20px
- Preview: "Found: 2,847 posts, 1,204 followers, 892 following. Continue?" — counts as blue pills, "Import" button
- Error: "Unable to read this file." 13px/400/#F4212E

---

## PROMPT 7 — Skip Confirmation Modal

Create the modal that appears when user clicks "Skip for Now."

**Overlay:** full-screen, rgba(0,0,0,0.60)

**Modal card:**
- Background: #1E2732, border 1px #2F3336, radius 24px, padding 32px
- Max-width 400px, centered on screen

**Content:**
- Title: "Skip connecting an account?" — 17px/700/#FFFFFF
- Body: "You won't be able to back up posts until you connect an account. Are you sure?" — 15px/400/#8B98A5, margin-top 12px

**Buttons (flex row, gap 12px, margin-top 24px, justify flex-end):**
- "Go Back" — ghost pill, border 1px #2F3336, text #FFFFFF, height 44px, 15px/600, default focus
- "Skip Anyway" — ghost pill, border 1px #F4212E, text #F4212E, height 44px, 15px/600

---

## COMPONENT VARIANTS

### 1. Method Card — Default State
- bg #1E2732, border 1px #2F3336, radius 24px

### 2. Method Card — Expanded (form visible)
- Same card, form section slides in below header with smooth 200ms height animation

### 3. Benefit Row — Green Checkmark
- 16px circle #00BA7C fill, white checkmark; text 15px/400/#FFFFFF

### 4. Warning Row — Yellow Triangle
- Warning triangle icon 16px #FFD400; text 14px/400/#8B98A5

### 5. "Recommended" Badge
- bg #0D2818, text #00BA7C, 11px/700, 9999px radius

### 6. Form Input — Dark
- bg #15202B, border 1px #2F3336, radius 12px, height 44px, text #FFFFFF, placeholder #8B98A5
- Focus: border-color #1D9BF0, outline none

### 7. Progress Stepper — Step States
- Active: 32px circle #1D9BF0 bg, white label
- Completed: 32px circle #1D9BF0 bg, white checkmark
- Upcoming: 32px circle #253341 bg, #8B98A5 label

### 8. Ghost Pill Button (Dark)
- border 1px #2F3336, text #FFFFFF, hover bg #253341, radius 9999px

### 9. Filled Blue Pill Button
- bg #1D9BF0, text #FFFFFF, hover bg #1A8CD8, radius 9999px

### 10. File Drop Zone
- Border 2px dashed #2F3336, bg #15202B, radius 16px
- Drag-over state: border-color #1D9BF0, bg #1D2D3E
