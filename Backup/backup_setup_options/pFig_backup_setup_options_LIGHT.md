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

# Figma Make Prompts — Setup: Configure Options (Light Mode)
# Page: backup_setup_options | URL: /setup/options

> **Navigation Note:** This is a standalone backup web application — NOT the JFKSocial social feed.
> There is NO JFKSocial left sidebar. Minimal authenticated top nav only.
> This is Step 2 of the 3-step setup wizard.

---

## DESIGN TOKEN REFERENCE

### Colors (Light Mode)
* Page bg:              #FFFFFF
* Card bg:              #FFFFFF (white cards, distinguished by border)
* Elevated surface:     #EFF3F4
* Border subtle:        #EFF3F4
* Border prominent:     #CFD9DE
* Primary text:         #0F1419
* Secondary text:       #536471
* Muted text:           #8B98A5
* Brand blue:           #1D9BF0
* Success green:        #00BA7C
* Danger red:           #F4212E
* Warning yellow:       #FFD400
* Warning bg tint:      #FFFCE0
* Upgrade link:         #1D9BF0

### Typography
* Font: "TwitterChirp", system-ui, sans-serif
* Page title:     23px / 700 / #0F1419
* Section label:  11px / 700 / #8B98A5 uppercase
* Card heading:   17px / 600 / #0F1419
* Description:    14px / 400 / #536471
* Estimate:       13px / 500 / #536471
* Radio label:    15px / 600 / #0F1419
* Radio sub:      13px / 400 / #536471
* Table key:      14px / 400 / #536471
* Table value:    14px / 400 / #0F1419
* Table total:    14px / 700 / #0F1419

---

## PROMPT 1 — Minimal Authenticated Header

**Container:** full-width, height 64px, bg #FFFFFF, border-bottom 1px #EFF3F4

**Left:** Shield icon + "Backup Posts" 17px/700/#0F1419
**Right:** "Account ▾" 15px/500/#536471 + "Logout" 15px/400/#536471, gap 20px
**Mobile:** Logo center, Account ▾ right, height 56px

---

## PROMPT 2 — Setup Progress Indicator (Step 2 Active)

**Step 1 — Connect (COMPLETED):**
- Circle 32px: bg #1D9BF0, white checkmark
- Label: "Connect" 13px/500/#536471

**Step 2 — Options (ACTIVE):**
- Circle 32px: bg #1D9BF0, "2" 13px/700/#FFFFFF
- Label: "Options" 13px/700/#0F1419

**Step 3 — Backup (UPCOMING):**
- Circle 32px: bg #EFF3F4, "3" 13px/400/#8B98A5
- Label: "Backup" 13px/400/#8B98A5

**Connector line 1→2:** filled #1D9BF0
**Connector line 2→3:** #EFF3F4

**Container:** max-width 480px, centered, margin 32px auto 40px

---

## PROMPT 3 — Page Header

**Title:** "What would you like to back up?" — 23px/700/#0F1419, text-align center
**Container:** max-width 680px, centered, margin-bottom 32px

---

## PROMPT 4 — Configuration Cards

Max-width 680px, centered, gap 16px.

**Card A — Backup Content:**
- bg #FFFFFF, border 1px #EFF3F4, radius 24px, padding 24px

Section label: "BACKUP CONTENT" — 11px/700/#8B98A5 uppercase

Primary checkbox row: [✓] #1D9BF0 + "Back up posts (tweets, threads, replies)" 17px/600/#0F1419

Description: "Your original tweets, retweets, quote tweets, and replies." 14px/400/#536471

Advanced Options (collapsible):
- Toggle: "Advanced Options" 13px/700/#536471 + chevron, margin-top 16px
- Expanded: 4 nested checkboxes indented 20px, 14px/400/#536471
  - Include replies / Include quote tweets / Include retweets / Include media

Count estimate: "Estimated: ~2,847 posts" 13px/500/#536471, margin-top 12px

---

**Card B — Backup Followers:**
- bg #FFFFFF, border 1px #EFF3F4, radius 24px, padding 24px
- [✓] "Back up followers (people who follow you)" 17px/600/#0F1419
- Description 14px/400/#536471
- "Estimated: ~1,204 followers" 13px/500/#536471

---

**Card C — Backup Following:**
- bg #FFFFFF, border 1px #EFF3F4, radius 24px, padding 24px
- [✓] "Back up following (people you follow)" 17px/600/#0F1419
- Description 14px/400/#536471
- "Estimated: ~892 accounts" 13px/500/#536471

---

**Card D — Sync Schedule:**
- bg #FFFFFF, border 1px #EFF3F4, radius 24px, padding 24px

Section label: "SYNC SCHEDULE" — 11px/700/#8B98A5 uppercase
Intro: "How often should we automatically sync your backup?" 14px/400/#536471

4 radio options (gap 12px, margin-top 16px):
- Radio 18px: selected = #1D9BF0 | unselected = border 2px #CFD9DE | locked = #EFF3F4 bg + padlock

(●) "Every 24 hours" 15px/600/#0F1419 — sub "Recommended for most users" 13px/400/#536471
( ) "Every 12 hours" 15px/600/#0F1419 — sub "More frequent backups for active accounts"
( ) "Every 6 hours" 15px/600/#0F1419 — sub "Maximum frequency (Creator plan or higher)" + 🔒 padlock
( ) "Manual only" 15px/600/#536471 — sub "You trigger backups yourself"

---

**Card E — Storage Estimate:**
- bg #FFFFFF, border 1px #EFF3F4, radius 24px, padding 24px

Section label: "STORAGE ESTIMATE" — 11px/700/#8B98A5 uppercase
"Based on your selections:" 13px/400/#536471

Table rows (flex justify space-between, 14px, gap 8px, margin-top 12px):
- "Text + metadata" | "~42 MB" — key: #536471, value: #0F1419
- "Media (images, videos)" | "~850 MB"
- "Total estimated" | "~892 MB" — 14px/700/#0F1419
- "Available (Free plan)" | "~10 GB"

Progress bar:
- Full-width, height 8px, radius 9999px
- Track: #EFF3F4
- Fill: <60% = #00BA7C | 60–80% = #FFD400 | >80% = #F4212E
- Current: ~9% fill, #00BA7C

Warning block (>80%):
- bg #FFFCE0, border-left 3px #FFD400, padding 12px 16px, radius 8px
- "[⚠] You may reach your storage limit after ~15 backups" 14px/400/#0F1419
- "Upgrade to Creator plan for unlimited storage →" 13px/400/#1D9BF0

---

## PROMPT 5 — Action Row & Footer

**Action row:**
- Max-width 680px, centered, margin 24px auto, flex, justify flex-end, gap 16px

- "Back" — ghost pill, border 1px #CFD9DE, text #536471, height 44px, 15px/500
- "Start First Backup" — filled blue pill, bg #1D9BF0, text #FFFFFF, height 52px, 17px/700
  - Disabled: bg #EFF3F4, text #8B98A5, cursor not-allowed
  - Tooltip: "Select at least one type of data to back up"
- Mobile: "Start First Backup" full-width first, "Back" below

**Footer:** "Need help? Contact Support | Help Center" — 13px/400/#8B98A5, centered

---

## COMPONENT VARIANTS

### 1. Checkbox — Light Mode
- Checked: 18px, bg #1D9BF0, white checkmark, border #1D9BF0
- Unchecked: 18px, border 2px #CFD9DE, white bg
- Disabled: 18px, bg #EFF3F4, border #EFF3F4
- Focus ring: 2px offset #1D9BF0

### 2. Radio Button — Light Mode
- Selected: outer border #1D9BF0, inner dot #1D9BF0
- Unselected: border 2px #CFD9DE, white inside
- Locked: #EFF3F4 bg, padlock icon #8B98A5, cursor not-allowed

### 3. Progress Bar — Storage
- Track: #EFF3F4, height 8px, radius 9999px
- Fill states: #00BA7C / #FFD400 / #F4212E

### 4. Storage Warning Block
- bg #FFFCE0, border-left 3px #FFD400, radius 8px
- Text: #0F1419 | Link: #1D9BF0

### 5. Section Label (UPPERCASE)
- 11px/700/#8B98A5

### 6. Configuration Card
- bg #FFFFFF, border 1px #EFF3F4, radius 24px, padding 24px

### 7. Advanced Options Toggle
- Label + chevron; chevron rotates 90° on expand, 200ms

### 8. Padlock Tooltip
- Trigger: hover over locked radio
- Tooltip: bg #0F1419, text #FFFFFF, radius 8px, 12px/400
- "Creator plan required"

### 9. Primary Button — Disabled
- bg #EFF3F4, text #8B98A5, cursor not-allowed

### 10. Count Estimate Row
- 13px/500/#536471
- Label left-aligned below checkbox card content
