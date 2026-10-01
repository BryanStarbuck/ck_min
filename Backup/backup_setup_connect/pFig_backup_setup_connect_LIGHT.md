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

# Figma Make Prompts — Setup: Connect Account (Light Mode)
# Page: backup_setup_connect | URL: /setup/connect

> **Navigation Note:** This is a standalone backup web application — NOT the JFKSocial social feed.
> There is NO JFKSocial left sidebar. Navigation is a minimal authenticated top bar (logo + account dropdown).
> This is Step 1 of a 3-step wizard.

---

## DESIGN TOKEN REFERENCE

### Colors (Light Mode)
* Page bg:              #FFFFFF
* Card bg:              #F7F9F9 (white cards on white page)
* Elevated surface:     #EFF3F4
* Border subtle:        #EFF3F4
* Border prominent:     #CFD9DE
* Primary text:         #0F1419
* Secondary text:       #536471
* Muted text:           #8B98A5
* Brand blue:           #1D9BF0
* Success green:        #00BA7C
* Success tint bg:      #E8F9F2
* Danger red:           #F4212E
* Warning yellow:       #FFD400
* Warning bg tint:      #FFFCE0

### Typography
* Font: "TwitterChirp", system-ui, -apple-system, BlinkMacSystemFont, sans-serif
* Page title:       23px / 700 / #0F1419
* Page subtitle:    15px / 400 / #536471
* Card title:       17px / 700 / #0F1419
* Card meta:        13px / 400 / #536471
* Benefit text:     15px / 400 / #0F1419
* Warning text:     14px / 400 / #536471
* Label text:       15px / 500 / #0F1419
* Small caption:    12px / 400 / #8B98A5
* Stepper label:    13px / 500

### Radii
* Cards: 24px | Buttons: 9999px | Inputs: 12px | Badge: 9999px

---

## PROMPT 1 — Minimal Authenticated Header

Create the minimal top navigation bar for an authenticated wizard page in light mode.

**Container:**
- Full-width, height 64px
- Background: #FFFFFF
- Border-bottom: 1px solid #EFF3F4
- z-index: 1000

**Left: Logo**
- Shield icon (24px, #1D9BF0) + "Backup Posts" wordmark 17px/700/#0F1419

**Right: Account Controls**
- "Account ▾" — 15px/500/#536471
- "Logout" — ghost link, 15px/400/#536471, hover #0F1419
- Gap: 20px

**Mobile (< 640px):**
- Logo center | "Account ▾" right | Height 56px

---

## PROMPT 2 — Setup Progress Indicator (Step 1 Active)

Create the horizontal step progress indicator showing 3 wizard steps.

**Container:**
- Max-width 480px, centered, margin 32px auto 40px

**Step 1 — Connect (ACTIVE):**
- Circle: 32px, bg #1D9BF0, label "1" 13px/700/#FFFFFF
- Label below: "Connect" 13px/700/#0F1419

**Step 2 — Options (UPCOMING):**
- Circle: 32px, bg #EFF3F4, label "2" 13px/400/#8B98A5
- Label below: "Options" 13px/400/#8B98A5

**Step 3 — Backup (UPCOMING):**
- Circle: 32px, bg #EFF3F4, label "3" 13px/400/#8B98A5
- Label below: "Backup" 13px/400/#8B98A5

**Connector lines:**
- Both connectors: 2px solid #EFF3F4

**Mobile:** 3 dots (12px). Active: #1D9BF0. Inactive: #CFD9DE.

---

## PROMPT 3 — Page Header

**Container:** Max-width 680px, centered, text-align center, margin-bottom 32px

- Title: "Connect Your Social Media Account" — 23px/700/#0F1419
- Subtitle: "Choose how you'd like to back up your posts:" — 15px/400/#536471, margin-top 8px

---

## PROMPT 4 — Method Cards (3 Cards)

Max-width 680px, centered, gap 16px. Cards are white on white page — use subtle border.

**Card A — Chrome Extension (Recommended):**
- Background: #FFFFFF, border 1px #EFF3F4, radius 24px, padding 28px

Header row:
- Browser icon 32px #1D9BF0 + "Chrome Extension" 17px/700/#0F1419
- "Recommended" badge: bg #E8F9F2, text #00BA7C, 11px/700, 9999px

4 benefit rows (margin-top 16px, gap 8px):
- Checkmark circle 16px #00BA7C + text 15px/400/#0F1419
- "No API keys needed" / "Works even if APIs are restricted" / "Reads your profile page directly" / "Most reliable method"

Description: "Install our Chrome extension, and it will read your Twitter/X profile when you visit it..." — 14px/400/#536471, margin-top 12px

CTA: "Install Extension" — filled blue pill, bg #1D9BF0, text #FFFFFF, height 44px, 15px/700, right-aligned

---

**Card B — API Connection:**
- Background: #FFFFFF, border 1px #EFF3F4, radius 24px, padding 28px

Header: Key icon 32px #536471 + "API Connection" 17px/700/#0F1419 + "For developers with Twitter API access" 13px/400/#536471

2 benefit rows (green checkmark): "Faster sync than extension" / "More complete data"
2 warning rows (warning triangle #FFD400): "Requires developer credentials" / "Subject to API rate limits" — 14px/400/#536471

CTA: "Connect via API" — ghost pill, border 1px #CFD9DE, text #1D9BF0, height 44px, 15px/700, right-aligned

Expandable form:
- Fields: bg #F7F9F9, border 1px #CFD9DE, radius 12px, height 44px, text #0F1419, placeholder #8B98A5
- Focus state: border-color #1D9BF0
- Fields: Platform dropdown, Handle, API Key, API Secret (password), Access Token, Access Secret
- Help link: "How to get API credentials →" 13px/400/#1D9BF0
- Action row: "Cancel" ghost + "Connect" filled blue, right-aligned, gap 12px

---

**Card C — Manual Import:**
- Background: #FFFFFF, border 1px #EFF3F4, radius 24px, padding 28px

Header: Upload icon 32px #536471 + "Manual Import" 17px/700/#0F1419 + description 13px/400/#536471

2 benefit rows (green checkmark) + 2 warning rows (yellow triangle)

CTA: "Upload File" — ghost pill, right-aligned

Expandable drop zone:
- Border: 2px dashed #CFD9DE, radius 16px, padding 40px, min-height 160px, bg #F7F9F9
- "Drag & drop your data export ZIP here" 15px/400/#536471, centered
- "or" — 13px/400/#8B98A5
- "Browse Files" ghost button 40px
- "Accepted: .zip | Max size: 500 MB" 12px/400/#8B98A5
- Help link: 13px/400/#1D9BF0

---

## PROMPT 5 — Skip Action & Footer

**Skip button:**
- "Skip for Now" — ghost pill, border 1px #CFD9DE, text #536471, height 44px, 15px/500, centered, margin-top 24px

**Footer:**
- "Need help? [Contact Support] | [Help Center]"
- 13px/400/#8B98A5, centered, links hover #1D9BF0

---

## PROMPT 6 — Form States & Banners

**Extension detected (success banner in Card A):**
- bg #E8F9F2, border 1px #00BA7C, radius 12px, padding 12px 16px
- Text: "Extension detected! Click Continue to connect." 14px/600/#00BA7C
- "Continue" button (green fill) replaces "Install Extension"

**API validation:**
- Validating: spinner on Connect, disabled (#EFF3F4 bg, #8B98A5 text)
- Success: "✓ Connected!" 13px/600/#00BA7C
- Error: 13px/400/#F4212E inline below button

**File upload:**
- Uploading: #1D9BF0 progress bar 4px, percentage text
- Parsing: "Parsing data..." + spinner
- Preview: counts as pills, "Import" button
- Error: 13px/400/#F4212E

---

## PROMPT 7 — Skip Confirmation Modal

**Overlay:** rgba(15,20,25,0.40)

**Modal card:**
- bg #FFFFFF, border 1px #EFF3F4, radius 24px, padding 32px, max-width 400px centered

**Content:**
- Title: "Skip connecting an account?" — 17px/700/#0F1419
- Body: 15px/400/#536471, margin-top 12px

**Buttons:**
- "Go Back" — ghost pill, border #CFD9DE, text #0F1419, height 44px, default focus
- "Skip Anyway" — ghost pill, border #F4212E, text #F4212E, height 44px

---

## COMPONENT VARIANTS

### 1. Method Card — Default
- bg #FFFFFF, border 1px #EFF3F4, radius 24px
- Hover: box-shadow 0 4px 12px rgba(15,20,25,0.06)

### 2. Benefit Row — Green Checkmark
- 16px #00BA7C circle + text 15px/400/#0F1419

### 3. Warning Row — Yellow Triangle
- Warning triangle #FFD400 + text 14px/400/#536471

### 4. "Recommended" Badge
- bg #E8F9F2, text #00BA7C, 11px/700, 9999px

### 5. Form Input — Light
- bg #F7F9F9, border 1px #CFD9DE, radius 12px, height 44px, text #0F1419, placeholder #8B98A5
- Focus: border-color #1D9BF0

### 6. Progress Stepper — Step States
- Active: 32px circle #1D9BF0 bg, white label
- Completed: 32px circle #1D9BF0 bg, white checkmark
- Upcoming: 32px circle #EFF3F4 bg, #8B98A5 label

### 7. Ghost Pill Button (Light)
- border 1px #CFD9DE, text #0F1419, hover bg #F7F9F9

### 8. Filled Blue Pill Button
- bg #1D9BF0, text #FFFFFF, hover bg #1A8CD8

### 9. File Drop Zone (Light)
- Border 2px dashed #CFD9DE, bg #F7F9F9, radius 16px
- Drag-over: border-color #1D9BF0, bg #EBF5FF

### 10. Success Banner
- bg #E8F9F2, border 1px #00BA7C, radius 12px
