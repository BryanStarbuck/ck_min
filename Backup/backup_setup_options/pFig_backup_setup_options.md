pFig — backup_setup_options
Figma Make Prompts: Setup — Configure Options (Step 2 of 3)
===========================================================

DESIGN TOKEN REFERENCE
=======================

Colors: page bg #FFFFFF | card bg #F7F9F9 | border subtle #EFF3F4 |
border prominent #CFD9DE | primary text #0F1419 | secondary #536471 | muted #8B98A5 |
brand blue #1D9BF0 | success #00BA7C | warning #FFD400 | danger #F4212E |
warning bg tint #FFFCE0 | blue tint #EBF5FF

Typography: page title 23px/700 | card section label 11px/700 uppercase letter-spacing 0.08em |
checkbox label 15px–17px/600 | description 14px/400/#536471 | estimate 13px/500/#536471 |
radio label 15px/600/#0F1419 | radio sub 13px/400/#536471

Spacing: card padding 28px desktop | 20px mobile | gap between cards 16px

Radii: cards 24px | buttons 9999px | inputs 12px | warning block 8px | progress bar 9999px

Breakpoints: desktop >=1024px | mobile <640px


====================================================================
PROMPT 1 — Header, Progress Stepper (Step 2), and Page Title
====================================================================

Create the minimal header and setup progress stepper in its step-2-active state, plus
the page title. Reference Page_Setup_Options_Web_UI.md stepper section.

Header: same minimal authenticated header as backup_setup_connect page.
  Logo left, "Account ▾" + "Logout" right, 64px height, white, border-bottom #EFF3F4.

Setup Progress Stepper (step 2 active, desktop):
* Max-width 480px, centered, margin 40px auto 0, padding-bottom 40px.
* Step 1 "Connect" — completed: circle 32px #1D9BF0 bg, white checkmark icon.
  Label 13px/700/#0F1419.
* Step 2 "Options" — active: circle 32px #1D9BF0 bg, white "2" 13px/700.
  Label 13px/700/#0F1419.
* Step 3 "Backup" — upcoming: circle 32px #EFF3F4 bg, #8B98A5 "3".
  Label 13px/400/#8B98A5.
* Connector line 1→2: 2px solid #1D9BF0 (completed).
* Connector line 2→3: 2px solid #EFF3F4 (upcoming).

Mobile stepper (step 2 active):
* 3 dots + labels. Dot 1: 12px #1D9BF0 with checkmark. Dot 2: 12px #1D9BF0.
  Dot 3: 12px #EFF3F4 border only.
* Connector 1→2: filled #1D9BF0. Connector 2→3: #EFF3F4.

Page title (desktop): "What would you like to back up?" — 23px/700/#0F1419, centered,
margin-bottom 32px.
Page title (mobile): "What to back up?" — 20px/700/#0F1419, left-aligned, padding 0 20px.


====================================================================
PROMPT 2 — Backup Content Card (Posts with Advanced Options)
====================================================================

Create the Backup Content card with its primary checkbox, description, collapsible
advanced options panel, and count estimate. Reference the BACKUP CONTENT section of
the web and mobile ASCII mockups.

Card layout:
* Card: white bg, border 1px #EFF3F4, radius 24px, padding 28px.
* Section label: "BACKUP CONTENT" — 11px/700/#8B98A5 uppercase, letter-spacing 0.08em,
  margin-bottom 16px.
* Primary checkbox row (flex, align-items flex-start, gap 12px):
  * Checkbox: 18px square, #1D9BF0 bg (checked), white checkmark, radius 4px.
    Focus ring: 2px solid #1D9BF0, 2px offset.
  * Label: "Back up posts (tweets, threads, replies)" — 17px/600/#0F1419.
* Description (margin-left 30px to align with label, not checkbox):
  "Your original tweets, retweets, quote tweets, and replies. Includes images,
  videos, and GIFs." — 14px/400/#536471, margin-top 4px.
* Advanced Options panel (collapsible):
  * Toggle row (margin-top 16px): "Advanced Options" 13px/700/#0F1419 + chevron "▶"
    (rotates 90° when expanded). Tap/click anywhere to toggle.
  * When expanded (smooth 200ms height transition):
    4 nested checkbox rows, indented 20px, gap 8px:
    Each: 16px checkbox (#1D9BF0 checked), label 14px/400/#0F1419.
    Labels: "Include replies" | "Include quote tweets" | "Include retweets" |
    "Include media (images, videos, GIFs)"
  * Desktop: advanced options expanded by default if < 1,000 posts. Show expanded.
  * Mobile: collapsed by default. Show collapsed with "▶" chevron.
* Count estimate (margin-top 16px):
  "Estimated: ~2,847 posts" — 13px/500/#536471. Left-aligned.

Checkbox states:
* Checked: 18px, #1D9BF0 bg, white checkmark, 0px border.
* Unchecked: 18px, border 2px #CFD9DE, white bg.
* Disabled (parent unchecked): 18px, #EFF3F4 bg, #CFD9DE border.
* Intermediate (some nested checked): 18px, #1D9BF0 bg, white dash.


====================================================================
PROMPT 3 — Backup Followers and Backup Following Cards
====================================================================

Create the Backup Followers and Backup Following configuration cards. Reference the
BACKUP FOLLOWERS and BACKUP FOLLOWING sections of the ASCII mockups.

Both cards share the same visual structure as the Backup Content card but without
advanced options nesting.

Backup Followers Card:
* Section label: "BACKUP FOLLOWERS" — 11px/700/#8B98A5 uppercase.
* Primary checkbox row: [✓] "Back up followers (people who follow you)" 17px/600.
* Description: "Preserve your follower list with names, handles, and profiles.
  Track follower changes over time." 14px/400/#536471.
* Count estimate: "Estimated: ~1,204 followers" 13px/500/#536471.

Backup Following Card:
* Section label: "BACKUP FOLLOWING"
* Primary checkbox row: [✓] "Back up following (people you follow)" 17px/600.
* Description: "Keep a record of accounts you follow. Useful for rebuilding your
  network on other platforms." 14px/400/#536471.
* Count estimate: "Estimated: ~892 accounts" 13px/500/#536471.

Card hover state (desktop):
* Both cards: box-shadow 0 2px 8px rgba(15,20,25,0.06) on hover.

Mobile:
* Same structure, card padding 20px. Count estimate 12px.


====================================================================
PROMPT 4 — Sync Schedule Card
====================================================================

Create the Sync Schedule card with 4 radio button options. Reference the SYNC SCHEDULE
section of both web and mobile ASCII mockups.

Card:
* White bg, border 1px #EFF3F4, radius 24px, padding 28px.
* Section label: "SYNC SCHEDULE" — 11px/700/#8B98A5 uppercase.
* Intro: "How often should we automatically sync your backup?" 14px/400/#536471,
  margin-bottom 16px.
* 4 radio options in a fieldset, gap 12px:
  Radio row structure: radio button (18px circle) + label block (flex-direction column):
    Primary label 15px/600/#0F1419 + sub-label 13px/400/#536471 below.
  * Option 1 — selected (default):
    Primary: "Every 24 hours — Recommended"  Sub: "Your posts will be backed up once
    per day."
  * Option 2:
    Primary: "Every 12 hours"  Sub: "More frequent backups for active accounts."
  * Option 3 (locked — Creator plan required):
    Primary: "Every 6 hours"  Sub: "Maximum backup frequency (Creator plan or higher)."
    Locked state: radio disabled, padlock icon 14px #8B98A5 right of primary label,
    all text #8B98A5, cursor not-allowed.
    Tooltip on hover: "Upgrade to Creator plan" in 12px tooltip bubble.
  * Option 4:
    Primary: "Manual only"  Sub: "You trigger backups yourself (not recommended)."

Radio button states:
* Selected: 18px circle, #1D9BF0 filled dot (10px) center, border #1D9BF0.
* Unselected: 18px circle, border 2px #CFD9DE, white inside.
* Disabled/locked: 18px, #EFF3F4 bg, #CFD9DE border.
* Focus: 2px ring #1D9BF0 offset 2px.

Mobile:
* Sub-labels shortened or hidden to save space.
  Option 1: "Every 24 hours" + "Recommended" badge pill (#E8F9F2, #00BA7C, 9999px).
  Others: just primary label, sub hidden.


====================================================================
PROMPT 5 — Storage Estimate Card
====================================================================

Create the Storage Estimate card with usage breakdown and conditional warning.
Reference the STORAGE ESTIMATE section of both ASCII mockups.

Card:
* White bg, border 1px #EFF3F4, radius 24px, padding 28px.
* Section label: "STORAGE ESTIMATE" — 11px/700/#8B98A5 uppercase.
* Intro: "Based on your selections:" — 13px/400/#536471, margin-bottom 16px.
* Usage breakdown rows (3 rows + total, gap 8px):
  Row structure: left label 14px/400/#536471, right value 14px/600/#0F1419.
  Row 1: "Text + metadata" / "~42 MB"
  Row 2: "Media (images, videos)" / "~850 MB"
  Row 3: "Total estimated" / "~892 MB" — 15px/700/#0F1419 (bold total)
  Row 4: "Available (Free plan)" / "~10 GB remaining"
* Storage progress bar below rows:
  * Track: full-width, height 8px, #EFF3F4 bg, radius 9999px.
  * Fill: 89% width (892MB/10GB is actually small, but show warning scenario at 89%).
    Fill color: #FFD400 (60–80%) or #F4212E (> 80%). At 89%: fill color #F4212E.
  * Small label below bar right: "892 MB / 10 GB" 12px/400/#8B98A5.
* Warning block (visible because > 80%):
  * Container: #FFFCE0 bg, 3px border-left #FFD400, radius 8px, padding 12px 16px,
    margin-top 16px.
  * Flex row: warning triangle icon 18px #FFD400 + text block.
  * Text: "You may reach your storage limit after ~15 backups." 14px/500/#0F1419.
  * Link below text: "Upgrade to Creator plan for unlimited storage →" 13px/400/#1D9BF0.

Mobile:
* Breakdown rows as two-column grid (same style).
* Bar full-width.
* Warning block: same #FFFCE0 bg, full-width.


====================================================================
PROMPT 6 — Action Row (Back + Start First Backup Buttons)
====================================================================

Create the action row with Back and Start First Backup buttons. Also show the disabled
state for Start First Backup when no checkboxes are selected.

Desktop action row:
* Container: max-width 680px, margin 24px auto 0, display flex, gap 16px,
  justify-content flex-end.
* "Back" button:
  Ghost pill, height 44px, 15px/500/#536471, border 1px #CFD9DE, bg transparent.
  Hover: bg #F7F9F9.
* "Start First Backup" button:
  Filled pill, height 52px, 17px/700/#FFFFFF, bg #1D9BF0, padding 0 32px.
  Hover: #1A8CD8. Active: #1570B8.

Disabled state (when all checkboxes unchecked):
* "Start First Backup": bg #8B98A5, cursor not-allowed, no hover change.
* Tooltip on hover: "Select at least one type of data to back up" — 12px tooltip bubble
  (#0F1419 bg, white text, radius 6px, 8px padding, appears above button).

Mobile action row:
* Stacked full-width. "Start First Backup" on top (height 52px). "Back" below (height 44px,
  ghost). Gap 12px.

Footer bar (below action row):
* Border-top 1px #EFF3F4, padding 20px, text-align center.
* "Need help? " + "Contact Support" link + " | " + "Help Center" link. 13px/400/#8B98A5.


====================================================================
COMPONENT VARIANTS
====================================================================

Checkbox
* size=18px (primary options) | size=16px (nested advanced options)
* state=checked: #1D9BF0 fill | state=unchecked: #CFD9DE border |
  state=intermediate: #1D9BF0 fill, dash icon | state=disabled: #EFF3F4 bg

Radio Button
* state=selected: #1D9BF0 inner dot | state=unselected: #CFD9DE border |
  state=locked: disabled + padlock icon + tooltip

Advanced Options Accordion
* state=collapsed: "▶" chevron
* state=expanded: "▼" chevron, nested checkboxes visible, smooth height transition 200ms

Storage Progress Bar
* color=green (#00BA7C): fill < 60%
* color=yellow (#FFD400): fill 60–80%
* color=red (#F4212E): fill > 80%, triggers warning block

Warning Block
* bg #FFFCE0, left border 3px #FFD400
* Contains: triangle icon, message text, optional upgrade link

Storage Breakdown Row
* Two-column: label left (secondary text), value right (primary text bold)
* Separator between rows: none (gap only)

Plan Lock Indicator
* Padlock icon 14px #8B98A5 inline after locked option label
* Tooltip: "Upgrade to Creator plan" — appears on hover, 12px, dark bg
