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

# Figma Make Prompts — Setup: Configure Options (Dark Mode)
# Page: backup_setup_options | URL: /setup/options

> **Navigation Note:** This is a standalone backup web application — NOT the JFKSocial social feed.
> There is NO JFKSocial left sidebar. Minimal authenticated top nav only.
> This is Step 2 of the 3-step setup wizard.

---

## DESIGN TOKEN REFERENCE

### Colors (Dark Mode)
* Page bg:              #15202B
* Card bg:              #1E2732
* Elevated:             #253341
* Borders:              #2F3336
* Primary text:         #FFFFFF
* Secondary text:       #8B98A5
* Brand blue:           #1D9BF0
* Success green:        #00BA7C
* Danger red:           #F4212E
* Warning yellow:       #FFD400
* Warning bg tint:      #1A1800
* Upgrade link:         #1D9BF0
* Progress bar green:   #00BA7C
* Progress bar yellow:  #FFD400
* Progress bar red:     #F4212E

### Typography
* Font: "TwitterChirp", system-ui, -apple-system, sans-serif
* Page title:     23px / 700 / #FFFFFF
* Section label:  11px / 700 / #8B98A5 (uppercase)
* Card heading:   17px / 600 / #FFFFFF
* Description:    14px / 400 / #8B98A5
* Estimate:       13px / 500 / #8B98A5
* Radio label:    15px / 600 / #FFFFFF
* Radio sub:      13px / 400 / #8B98A5
* Table key:      14px / 400 / #8B98A5
* Table value:    14px / 400 / #FFFFFF
* Table total:    14px / 700 / #FFFFFF

---

## PROMPT 1 — Minimal Authenticated Header

Same as setup_connect header (Step 2 context).

**Container:** full-width, height 64px, bg #15202B, border-bottom 1px #2F3336

**Left:** Shield icon + "Backup Posts" 17px/700/#FFFFFF
**Right:** "Account ▾" 15px/500/#8B98A5 + "Logout" 15px/400/#8B98A5, gap 20px
**Mobile:** Logo center, Account ▾ right, height 56px

---

## PROMPT 2 — Setup Progress Indicator (Step 2 Active)

**Step 1 — Connect (COMPLETED):**
- Circle 32px: bg #1D9BF0, white checkmark icon (not number)
- Label below: "Connect" 13px/500/#8B98A5

**Step 2 — Options (ACTIVE):**
- Circle 32px: bg #1D9BF0, label "2" 13px/700/#FFFFFF
- Label below: "Options" 13px/700/#FFFFFF

**Step 3 — Backup (UPCOMING):**
- Circle 32px: bg #253341, label "3" 13px/400/#8B98A5
- Label below: "Backup" 13px/400/#8B98A5

**Connector line 1→2:** filled #1D9BF0
**Connector line 2→3:** #2F3336

**Container:** max-width 480px, centered, margin 32px auto 40px
**Mobile:** 3 dots; step 1 completed (#1D9BF0 checkmark), step 2 active (#1D9BF0), step 3 upcoming (#2F3336)

---

## PROMPT 3 — Page Header

**Title:** "What would you like to back up?" — 23px/700/#FFFFFF, text-align center
**Container:** max-width 680px, centered, margin-bottom 32px

---

## PROMPT 4 — Configuration Cards

Max-width 680px, centered, gap 16px (5 cards total).

---

**Card A — Backup Content (Posts):**
- bg #1E2732, border 1px #2F3336, radius 24px, padding 24px

Section label: "BACKUP CONTENT" — 11px/700/#8B98A5 uppercase, margin-bottom 12px

Primary checkbox row:
- Checkbox 18px: checked = #1D9BF0 bg, white checkmark
- "Back up posts (tweets, threads, replies)" 17px/600/#FFFFFF
- Flex row, gap 10px

Description: "Your original tweets, retweets, quote tweets, and replies. Includes images, videos, and GIFs." 14px/400/#8B98A5, margin-top 8px

Advanced Options (collapsible):
- Toggle row: "Advanced Options" 13px/700/#8B98A5 + "▶" chevron (rotates when open), margin-top 16px
- When expanded: 4 nested checkboxes indented 20px, gap 8px
  - [✓] Include replies
  - [✓] Include quote tweets
  - [✓] Include retweets
  - [✓] Include media (images, videos, GIFs)
  - Each row: 18px checkbox + 14px/400/#8B98A5 text

Count estimate: "Estimated: ~2,847 posts" — 13px/500/#8B98A5, margin-top 12px

---

**Card B — Backup Followers:**
- bg #1E2732, border 1px #2F3336, radius 24px, padding 24px

Primary checkbox: [✓] "Back up followers (people who follow you)" 17px/600/#FFFFFF
Description: "Preserve your follower list with names, handles, and profiles." 14px/400/#8B98A5
Count estimate: "Estimated: ~1,204 followers" 13px/500/#8B98A5

---

**Card C — Backup Following:**
- bg #1E2732, border 1px #2F3336, radius 24px, padding 24px

Primary checkbox: [✓] "Back up following (people you follow)" 17px/600/#FFFFFF
Description: "Keep a record of accounts you follow." 14px/400/#8B98A5
Count estimate: "Estimated: ~892 accounts" 13px/500/#8B98A5

---

**Card D — Sync Schedule:**
- bg #1E2732, border 1px #2F3336, radius 24px, padding 24px

Section label: "SYNC SCHEDULE" — 11px/700/#8B98A5 uppercase
Intro: "How often should we automatically sync your backup?" 14px/400/#8B98A5, margin-top 8px

4 radio options (gap 12px, margin-top 16px):
Each option row: flex, align-items flex-start, gap 10px
- Radio circle 18px: selected = #1D9BF0 filled center | unselected = border 2px #2F3336, bg #15202B | locked = #253341 + padlock icon

(●) "Every 24 hours" 15px/600/#FFFFFF — sub "Recommended for most users" 13px/400/#8B98A5
( ) "Every 12 hours" 15px/600/#FFFFFF — sub "More frequent backups for active accounts"
( ) "Every 6 hours" 15px/600/#FFFFFF — sub "Maximum frequency (Creator plan or higher)" + 🔒 padlock + "Creator plan required" tooltip
( ) "Manual only" 15px/600/#8B98A5 — sub "You trigger backups yourself (not recommended)"

---

**Card E — Storage Estimate:**
- bg #1E2732, border 1px #2F3336, radius 24px, padding 24px

Section label: "STORAGE ESTIMATE" — 11px/700/#8B98A5 uppercase
"Based on your selections:" 13px/400/#8B98A5, margin-top 8px

Usage table rows (flex, justify space-between, 14px, gap 8px, margin-top 12px):
- "Text + metadata" | "~42 MB" — key: #8B98A5, value: #FFFFFF
- "Media (images, videos)" | "~850 MB"
- "Total estimated" | "~892 MB" — bold 14px/700/#FFFFFF
- "Available (Free plan)" | "~10 GB"

Linear progress bar:
- Full-width, height 8px, radius 9999px
- Track: #253341
- Fill: <60% = #00BA7C | 60–80% = #FFD400 | >80% = #F4212E
- Shown here at ~9% fill: #00BA7C

Warning block (only shown when >80%):
- bg #1A1800, border-left 3px #FFD400, padding 12px 16px, radius 8px
- "[⚠] You may reach your storage limit after ~15 backups" 14px/400/#FFD400
- "Upgrade to Creator plan for unlimited storage →" 13px/400/#1D9BF0

---

## PROMPT 5 — Action Row & Footer

**Action row:**
- Max-width 680px, centered, margin 24px auto
- Flex, justify flex-end, gap 16px

- "Back" — ghost pill, border 1px #2F3336, text #8B98A5, height 44px, 15px/500
- "Start First Backup" — filled blue pill, bg #1D9BF0, text #FFFFFF, height 52px, 17px/700
  - Disabled state: bg #253341, text #8B98A5, cursor not-allowed
  - Disabled tooltip: "Select at least one type of data to back up"
- Mobile: stacked full-width, "Start First Backup" first (52px), "Back" below (44px)

**Footer:**
- "Need help? Contact Support | Help Center" — 13px/400/#8B98A5, centered
- Links hover: #1D9BF0

---

## COMPONENT VARIANTS

### 1. Checkbox — Dark Mode
- Checked: 18px, bg #1D9BF0, white checkmark, border #1D9BF0
- Unchecked: 18px, border 2px #2F3336, bg transparent
- Disabled (parent unchecked): 18px, bg #253341, border #2F3336
- Focus ring: 2px offset #1D9BF0

### 2. Radio Button — Dark Mode
- Selected: 18px circle, outer border #1D9BF0, inner dot #1D9BF0
- Unselected: 18px circle, border 2px #2F3336, bg #15202B
- Locked: gray #253341, padlock icon 12px #8B98A5, cursor not-allowed

### 3. Progress Bar — Storage
- Track: #253341, height 8px, radius 9999px
- Fill states: green #00BA7C (<60%) | yellow #FFD400 (60–80%) | red #F4212E (>80%)

### 4. Storage Warning Block
- bg #1A1800, border-left 3px #FFD400, radius 8px
- Text: 14px/400/#FFD400
- Link: #1D9BF0

### 5. Section Label (UPPERCASE)
- 11px/700/#8B98A5, letter-spacing 0.08em

### 6. Configuration Card
- bg #1E2732, border 1px #2F3336, radius 24px, padding 24px

### 7. Advanced Options Toggle
- "Advanced Options" 13px/700/#8B98A5 + chevron #8B98A5
- Expanded chevron rotates 90°, transition 200ms

### 8. Nested Checkbox Row
- Indented 20px, 14px/400/#8B98A5, checkbox 18px
- Parent unchecked: child checkboxes disabled (#253341)

### 9. Padlock Tooltip
- Trigger: hover over locked radio option
- Tooltip card: bg #253341, border 1px #2F3336, radius 8px, padding 6px 12px
- Text: "Creator plan required" 12px/400/#FFFFFF

### 10. Primary Button — Disabled
- bg #253341, text #8B98A5, cursor not-allowed
- Tooltip: "Select at least one type of data to back up"
