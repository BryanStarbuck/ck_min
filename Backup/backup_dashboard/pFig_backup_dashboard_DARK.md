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

# Figma Make Prompts — Backup Dashboard (Dark Mode)
# Page: backup_dashboard | URL: /dashboard

> **Navigation Note:** This is a standalone backup web application — NOT the JFKSocial social feed.
> There is NO JFKSocial left sidebar. Full authenticated top nav with Dashboard, Export, Settings links.
> Mobile has a fixed bottom tab bar with 4 tabs.

---

## DESIGN TOKEN REFERENCE

### Colors (Dark Mode)
* Page bg:              #15202B
* Card bg:              #1E2732
* Hover surface:        #253341
* Borders:              #2F3336
* Primary text:         #FFFFFF
* Secondary text:       #8B98A5
* Muted text:           #8B98A5
* Brand blue:           #1D9BF0
* Success green:        #00BA7C
* Success tint bg:      #0D2818
* Danger red:           #F4212E
* Danger tint bg:       #1A0000
* Warning yellow:       #FFD400
* Warning tint bg:      #1A1800
* Warning orange:       #FF7A00
* Orange tint bg:       #1A1000
* Syncing blue tint:    #1D2D3E

### Typography
* Page title:       23px / 700 / #FFFFFF
* Card title:       15px / 700 / #FFFFFF
* Section label:    15px / 700 / #FFFFFF
* Body text:        14px / 600 / #FFFFFF
* Body sub:         13px / 400 / #8B98A5
* Meta small:       12px / 400 / #8B98A5
* Handle:           15px / 700 / #FFFFFF
* Platform name:    13px / 400 / #8B98A5
* Stats text:       14px / 600 / #FFFFFF
* Activity main:    14px / 600 / #FFFFFF
* Timestamp:        12px / 400 / #8B98A5

---

## PROMPT 1 — Full Authenticated Top Navigation

**Container:** full-width, height 64px, bg #15202B, border-bottom 1px #2F3336, z-index 1000

**Left:** Shield icon + "Backup Posts" wordmark 17px/700/#FFFFFF

**Center Nav Links:**
- "Dashboard" (active) | "Export" | "Settings"
- 15px/500/#FFFFFF (active bold #FFFFFF) / #8B98A5 (inactive), gap 32px
- Active indicator: 2px underline #1D9BF0 below active link

**Right:**
- "Account ▾" — 15px/500/#8B98A5, dropdown arrow
- "Logout" — ghost link, 15px/400/#8B98A5
- Gap: 20px

**Mobile:**
- Left: hamburger (☰) 24px #FFFFFF
- Center: Logo
- Right: "Account ▾"
- Bottom tab bar (fixed, 56px, bg #1E2732, border-top 1px #2F3336):
  - 4 tabs: 🏠 Dashboard | 📋 View | 📤 Export | ⚙ Settings
  - Active: icon + label #1D9BF0 | Inactive: #8B98A5

---

## PROMPT 2 — Storage Warning Banner (Conditional)

Shown only when storage > 80% full. Full-width banner between nav and page title.

**Container:** full-width, bg #1A1800, border-bottom 1px #FFD400, padding 12px 24px

**Layout:** flex, align-items center, gap 12px
- "⚠ Storage 85% full (8.5 GB of 10 GB)" — 14px/600/#FFD400
- "Upgrade Plan" — 14px/700/#1D9BF0, underline hover
- "Manage Storage" — ghost pill, 12px/700/#8B98A5, border #2F3336, height 28px, radius 9999px
- All right-aligned after text

---

## PROMPT 3 — Page Title

**Container:** max-width 1000px, centered, margin 32px auto 24px

- "Your Backups" — 23px/700/#FFFFFF

---

## PROMPT 4 — Backup Status Panel

**Container:** max-width 1000px, centered

**Card:** bg #1E2732, border 1px #2F3336, radius 24px, padding 24px

**Status row** (flex, align-items center, gap 12px):
- Status dot: 12px circle, bg #00BA7C (operational)
- "All Systems Operational" — 15px/700/#FFFFFF, flex-grow
- "Last backup: 2 hours ago" — 13px/400/#8B98A5, flex-shrink 0

**Sub-row:** "Next auto-sync in: 22 hours" — 13px/400/#8B98A5, margin-top 4px

**"Sync All Now" button:**
- Filled blue pill, bg #1D9BF0, text #FFFFFF, height 40px, 15px/700, margin-top 16px, radius 9999px
- On click: shows spinner + "Syncing..." text, disabled state

**Status dot colors:**
- Operational: #00BA7C
- Warning: #FFD400
- Error: #F4212E
- Never synced: #8B98A5

---

## PROMPT 5 — Connected Accounts Section

**Container:** max-width 1000px, centered, margin-top 24px

**Section label:** "Connected Accounts" — 15px/700/#FFFFFF, margin-bottom 16px

**2-column grid** (desktop), gap 20px:
- Left column: Account card(s)
- Right column: "Add Another Account" dashed card

---

**Account Card (@username / Twitter/X):**
- bg #1E2732, border 1px #2F3336, radius 24px, padding 24px

**Platform header row** (flex, align-items center, gap 10px):
- Platform icon: 32px circle, bg #FFFFFF, black X letterform (or platform icon)
- "@username" — 15px/700/#FFFFFF, flex-grow
- "Twitter/X" — 13px/400/#8B98A5
- Badge: "✓ Backup Complete" — bg #0D2818, text #00BA7C, 9999px, 11px/700, padding 3px 10px

**Stats section** (margin-top 16px):
- "2,847 posts backed up" — 14px/600/#FFFFFF
- Coverage progress bar: height 8px, fill #00BA7C (95%), track #253341, radius 9999px
- Below bar: "Posts from Jan 2020 – Present" — 12px/400/#8B98A5
- Stat rows: "1,204 followers" | "892 following" — 13px/400/#8B98A5, gap 4px
- "Last synced: 2 hours ago" — 12px/400/#8B98A5, margin-top 8px

**Action row** (margin-top 16px, flex, gap 10px, align-items center):
- "Sync Now" — ghost pill, border 1px #1D9BF0, text #1D9BF0, height 36px, 13px/700
- "View" — ghost pill, border 1px #2F3336, text #8B98A5, height 36px, 13px/700
- [⋮] — 24px icon button, text #8B98A5, hover bg #253341 rounded

---

**Add Another Account Card (dashed):**
- Border: 2px dashed #2F3336, radius 24px, padding 24px
- Display flex, column, justify-content center, align-items center, min-height same as account card

- [+] icon: 48px circle, bg #253341, "+" 24px #8B98A5
- "Add Another Account" — 15px/700/#FFFFFF, margin-top 12px
- "Connect additional social media accounts" — 13px/400/#8B98A5, text-align center
- "Add Account" — filled blue pill, bg #1D9BF0, text #FFFFFF, height 40px, 15px/700, margin-top 16px

---

## PROMPT 6 — Recent Activity Section

**Container:** max-width 1000px, centered, margin-top 24px

**Section heading:** "Recent Activity" — 15px/700/#FFFFFF, margin-bottom 16px

**Card:** bg #1E2732, border 1px #2F3336, radius 24px, padding 24px

**5 activity rows** (gap 0, divider 1px #2F3336 between rows):
Each row: flex, align-items flex-start, padding 14px 0, gap 12px

- Icon 20px circle: ✓ = #00BA7C | ⚠ = #FFD400 | ✗ = #F4212E
- Text block (flex-grow):
  - Main: 14px/600/#FFFFFF
  - Sub: 13px/400/#8B98A5, margin-top 2px
- Timestamp: 12px/400/#8B98A5, flex-shrink 0

**Activity rows:**
1. ✓ "Full backup completed for @username" / "2,847 posts, 1,204 followers, 892 following" / "2 hours ago"
2. ✓ "Media download completed" / "1,523 images and videos saved" / "2 hours ago"
3. ✓ "Incremental sync completed" / "14 new posts backed up" / "1 day ago"
4. ✓ "Account connected: @username" / "" / "3 days ago"
5. ✓ "Chrome extension installed" / "" / "3 days ago"

**"View All"** — ghost pill, bg transparent, border 1px #2F3336, text #8B98A5, height 36px, 13px/700, centered, margin-top 16px

---

## PROMPT 7 — Account Card State Variants

Illustrate the 4 card states side-by-side (or as a set):

**Complete (default):**
- Badge: bg #0D2818, text #00BA7C, "✓ Backup Complete"
- Border: 1px #2F3336
- Progress bar fill: #00BA7C

**Syncing:**
- Badge: bg #1D2D3E, text #1D9BF0, spinning dot + "Syncing..."
- Card has semi-transparent overlay (#1E2732 at 80% opacity) with inline progress
- "Sync Now" button → "Syncing..." disabled

**Error:**
- Badge: bg #1A0000, text #F4212E, "⚠ Sync Failed"
- Card border: 1px #F4212E
- Below last-synced: "View Error →" 13px/400/#F4212E

**Disconnected:**
- Badge: bg #1A1000, text #FF7A00, "Disconnected"
- "Sync Now" → "Reconnect" ghost pill, border #FF7A00, text #FF7A00

---

## PROMPT 8 — More Menu (⋮) Dropdown

**Dropdown card:**
- bg #1E2732, border 1px #2F3336, radius 16px, box-shadow 0 4px 12px rgba(0,0,0,0.40), width 180px
- Positioned below the ⋮ button

**Menu items** (14px/400/#FFFFFF, height 36px, hover bg #253341, padding 0 16px):
- "Edit Settings"
- "Export Data"
- "View Errors"
- Divider: 1px #2F3336
- "Disconnect Account" — text #F4212E
- "Remove Account" — text #F4212E, 700 weight

---

## PROMPT 9 — Empty State

When no accounts connected (replace status panel + accounts section):

**Container:** max-width 480px, centered, text-align center, padding 60px 24px

- Illustration: 200px circle, bg #1E2732 (placeholder icon)
- "Connect your first social media account to start backing up your posts." — 20px/700/#FFFFFF, margin-top 24px
- "Connect Account" — filled blue pill, height 52px, 17px/700, margin-top 20px

---

## COMPONENT VARIANTS

### 1. Account Card — Default (Dark)
- bg #1E2732, border 1px #2F3336, radius 24px

### 2. Status Dot
- 12px circle: green #00BA7C / yellow #FFD400 / red #F4212E / gray #8B98A5

### 3. Coverage Progress Bar (Account Card)
- Track #253341, fill #00BA7C, height 8px, radius 9999px

### 4. Badge — Backup Complete
- bg #0D2818, text #00BA7C, 11px/700, 9999px radius

### 5. Badge — Syncing
- bg #1D2D3E, text #1D9BF0, spinning dot 8px inline

### 6. Badge — Error
- bg #1A0000, text #F4212E, 11px/700

### 7. Badge — Disconnected
- bg #1A1000, text #FF7A00, 11px/700

### 8. More Menu (⋮)
- Trigger: 24px icon #8B98A5, hover bg #253341 12px radius
- Dropdown: #1E2732 bg, #2F3336 border, radius 16px, FAB shadow

### 9. Add Account Card (Dashed)
- 2px dashed #2F3336, radius 24px, centered content

### 10. Activity Row
- Flex row, 14px/600/#FFFFFF main + 13px/400/#8B98A5 sub + 12px/#8B98A5 timestamp
- Divider between rows: 1px #2F3336
