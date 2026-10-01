pFig — backup_dashboard
Figma Make Prompts: Backup Dashboard
=====================================

DESIGN TOKEN REFERENCE
=======================

Colors: page bg #FFFFFF | card bg #F7F9F9 | elevated #EFF3F4 |
border subtle #EFF3F4 | border prominent #CFD9DE | primary text #0F1419 |
secondary #536471 | muted #8B98A5 | brand blue #1D9BF0 (hover #1A8CD8) |
success #00BA7C | success bg #E8F9F2 | danger #F4212E | danger bg #FFF5F5 |
warning #FF7A00 | warning yellow #FFD400 | warning bg #FFFCE0 | blue tint #EBF5FF

Typography: page title 23px/700 | section label 15px/700 | card heading 15px/700 |
body 14px/400 | stats 14px/600 | small 13px/400/#536471 | badge 11px/700 |
timestamp 12px/400/#8B98A5 | caption 12px/400/#8B98A5

Spacing: page max-width 1000px | card padding desktop 24px | mobile 20px | gap 20px

Radii: cards 24px | buttons 9999px | badges 9999px | avatars 50% | dropdown 16px

Breakpoints: desktop >=1024px | mobile <640px


====================================================================
PROMPT 1 — Authenticated Navigation Bar and Page Title
====================================================================

Create the authenticated top navigation bar and the "Your Backups" page title.
Reference Page_Dashboard_Web_UI.md navigation row.

Navigation bar (desktop):
* Full width, height 64px, white bg, border-bottom 1px #EFF3F4.
* Left: shield icon 20px #1D9BF0 + "Backup Posts" 18px/700/#0F1419.
* Center: nav links with 32px gap.
  "Dashboard" — active state: 15px/700/#0F1419, border-bottom 2px #1D9BF0,
  padding-bottom 2px.
  "Export" — 15px/500/#536471, no underline, hover color #0F1419.
  "Settings" — 15px/500/#536471, hover color #0F1419.
* Right: "Account ▾" trigger (32px avatar circle #EFF3F4, "@username" 15px/400/#0F1419,
  chevron icon #536471) + "Logout" text link 15px/400/#536471.
  Gap between them: 20px.

Mobile navigation (top bar):
* Height 56px, border-bottom 1px #EFF3F4.
* Left: hamburger ☰ 24px #0F1419, 44x44px tap target.
* Center: shield + "Backup" 16px/700.
* Right: avatar 28px circle + chevron.

Page title block (desktop):
* Max-width 1000px, centered, margin 32px auto 24px.
* "Your Backups" — 23px/700/#0F1419.


====================================================================
PROMPT 2 — Backup Status Panel
====================================================================

Create the Backup Status Panel card. Reference the BACKUP STATUS PANEL section of the
web and mobile ASCII mockups. Show all 4 status variants as states.

Desktop status panel (default — all systems operational):
* Card: max-width 1000px, centered. White bg, border 1px #EFF3F4, radius 24px,
  padding 24px.
* Row 1 (flex, align-items center, gap 12px):
  * Status dot: 12px circle, #00BA7C fill (operational).
  * "All Systems Operational" — 15px/700/#0F1419.
  * Right side (margin-left auto): "Last backup: 2 hours ago" — 13px/400/#8B98A5.
* Row 2 (margin-top 4px): "Next auto-sync in: 22 hours" — 13px/400/#536471,
  margin-left 24px (aligns with text after dot).
* "Sync All Now" button (margin-top 16px):
  Filled blue pill, height 40px, 15px/700/#FFFFFF, #1D9BF0 bg, padding 0 24px.
  Hover: #1A8CD8.

Status dot variants (show 4 variant frames):
* Operational: 12px circle #00BA7C
* Warning: 12px circle #FFD400
* Error: 12px circle #F4212E
* Never synced: 12px circle #8B98A5

Syncing state (status panel variant):
* Dot: pulsing blue #1D9BF0 (animated glow ring).
* Text: "Syncing in progress..."
* "Sync All Now" button: replaced by "Syncing... X%" with spinner + progress bar.
  Small horizontal bar below button row, height 4px, #1D9BF0 animated fill.

Mobile:
* Status dot + text on first line. Last backup on second line. Next sync on third.
* "Sync All Now" full-width, height 52px.


====================================================================
PROMPT 3 — Connected Account Card
====================================================================

Create the account card for a connected Twitter/X account. Show all 5 states.
Reference the connected account card in both web and mobile ASCII mockups.

Account Card — Complete state (default):
* Card: white bg, border 1px #EFF3F4, radius 24px, padding 24px.
* Platform header row (flex, align-items center, gap 10px):
  * Icon: 32px circle, #000000 bg, white "X" letterform centered.
  * Handle: "@username" 15px/700/#0F1419.
  * Platform: "Twitter/X" 13px/400/#536471.
  * Badge right (margin-left auto): "✓ Backup Complete" —
    #E8F9F2 bg, #00BA7C text, 9999px, 11px/700, padding 3px 10px.
* Stats block (margin-top 16px):
  * "2,847 posts backed up" — 14px/600/#0F1419.
  * Coverage bar (margin-top 8px): full-width, 8px height, #00BA7C fill 95%,
    track #EFF3F4, radius 9999px.
  * Coverage label: "Posts from Jan 2020 – Present" — 12px/400/#8B98A5, margin-top 4px.
  * Two stat rows (gap 4px, margin-top 8px):
    "1,204 followers" 13px/400/#536471 | "892 following" 13px/400/#536471.
  * "Last synced: 2 hours ago" — 12px/400/#8B98A5, margin-top 8px.
* Action row (margin-top 16px, flex, align-items center, gap 10px):
  * "Sync Now" — ghost pill, height 36px, 13px/700/#1D9BF0, border 1px #1D9BF0.
    Hover: #EBF5FF bg.
  * "View" — ghost pill, height 36px, 13px/700/#536471, border 1px #CFD9DE.
    Hover: #F7F9F9 bg.
  * [⋮] icon button: 32px circle, border 1px #EFF3F4, #536471 dots icon. Hover: #F7F9F9.

Account Card — Syncing state:
* Badge: "Syncing..." — #EBF5FF bg, #1D9BF0 text, animated dot (pulsing).
* Overlay: rgba(255,255,255,0.85) fills card content area above action row.
  Overlay shows: progress bar (4px, #1D9BF0), "Posts (2,104 / 2,847)" 13px/#536471.
  "View Details" link 12px/#1D9BF0.
* "Sync Now" → "Syncing..." text, disabled, spinner replacing icon.

Account Card — Error state:
* Border: 1px #F4212E (entire card border changes).
* Badge: "⚠ Sync Failed" — #FFF5F5 bg, #F4212E text.
* Below last-synced: "View Error →" 13px/400/#F4212E.
* "Sync Now" → "Retry" button, keeps same ghost pill style.

Account Card — Disconnected state:
* Badge: "Disconnected" — #FFFCE0 bg, #FF7A00 text.
* "Sync Now" replaced by "Reconnect" — ghost pill, border #FF7A00, text #FF7A00.

Account Card — Gaps detected state:
* Badge: "Backup Complete" with gap sub-indicator: additional row in stats:
  "3 gaps detected" — orange pill badge + "Deep Sync" ghost button (12px/700/#FF7A00,
  border #FF7A00).

More menu dropdown:
* Opens when [⋮] tapped. Positioned below button, right-aligned.
* Card: white bg, border 1px #EFF3F4, radius 16px, padding 4px 0,
  shadow 0 4px 12px rgba(15,20,25,0.15), width 180px.
* Items (36px height each, flex, align-items center, padding 0 16px, 14px/400):
  "Edit Settings" #0F1419 | "Export Data" #0F1419 | "View Errors" #0F1419 |
  divider 1px #EFF3F4 | "Disconnect Account" #F4212E | "Remove Account" #F4212E 14px/700.
  Hover on each item: #F7F9F9 bg.

Mobile account card:
* Full-width. Action buttons "Sync" + "View" smaller (28px height, 12px text) + [⋮].
  Swipe-left hidden actions: "Sync", "Export", "Disconnect" as colored action buttons.


====================================================================
PROMPT 4 — Add Another Account Card
====================================================================

Create the "Add Another Account" dashed-border card. Reference the add account card
in both web and mobile ASCII mockups.

Desktop:
* Card: border 2px dashed #CFD9DE, radius 24px, padding 24px.
  Same min-height as account card for visual balance.
  Display flex, flex-direction column, justify-content center, align-items center.
* "+" icon zone: 48px circle, #EFF3F4 bg, #536471 "+" icon 28px inside.
* Title: "Add Another Account" — 15px/700/#0F1419, margin-top 16px.
* Description: "Connect additional social media accounts to back up" — 13px/400/#536471,
  text-align center, margin-top 8px, max-width 180px.
* "Add Account" — filled blue pill, height 40px, 15px/700, margin-top 20px.
* Hover on entire card: border-color #1D9BF0 (dashed stays), bg #F7FBFF, cursor pointer.

Mobile:
* Full-width dashed card. Centered content. "Add Account" full-width pill.


====================================================================
PROMPT 5 — Recent Activity Section
====================================================================

Create the Recent Activity section with 5 rows and a "View All" button.
Reference the RECENT ACTIVITY section of the web ASCII mockup and the 3-row
condensed mobile version.

Desktop:
* Section label: "Recent Activity" — 15px/700/#0F1419, margin-bottom 12px.
* Card: white bg, border 1px #EFF3F4, radius 24px, padding 0 24px.
* 5 rows inside card (separated by 1px #EFF3F4 dividers, no padding on first/last divider):
  Row structure (flex, align-items flex-start, padding 14px 0, gap 12px):
  * Icon: 20px circle. ✓ = #00BA7C bg white check | ⚠ = #FFD400 bg | ✗ = #F4212E bg.
  * Text block (flex-grow):
    Main: 14px/600/#0F1419.
    Sub (when present): 13px/400/#536471, margin-top 2px.
  * Timestamp: 12px/400/#8B98A5, flex-shrink 0, self-aligned top.

Row data:
  1: ✓ "Full backup completed for @username" / "2,847 posts, 1,204 followers, 892 following" / "2 hours ago"
  2: ✓ "Media download completed" / "1,523 images and videos saved" / "2 hours ago"
  3: ✓ "Incremental sync completed" / "14 new posts backed up" / "1 day ago"
  4: ✓ "Account connected: @username" / "" (no sub) / "3 days ago"
  5: ✓ "Chrome extension installed" / "" / "3 days ago"

"View All" button (below card):
* Ghost pill, height 36px, 13px/700/#536471, border 1px #CFD9DE, centered,
  margin-top 16px.

Mobile:
* 3 rows only (condensed for mobile space). Same row structure, 13px text.
* "View All" full-width ghost pill, height 44px.


====================================================================
PROMPT 6 — Empty State and Storage Warning Banner
====================================================================

Create two supplementary states: the empty dashboard (no accounts) and the storage
warning banner.

Empty State (no accounts connected):
* Shows when no accounts are connected. Replaces status panel + accounts section.
* Centered block: max-width 480px, margin 80px auto.
* Illustration: 200px circle #F7F9F9 bg, border 2px dashed #CFD9DE, flex center,
  cloud-upload icon 80px #8B98A5.
* Title: "Connect your first social media account" — 23px/700/#0F1419, text-align center,
  margin-top 24px.
* Body: "Start backing up your posts before they're gone." — 15px/400/#536471,
  text-align center, margin-top 8px.
* "Connect Account" — filled blue pill, height 52px, 17px/700, margin-top 24px, centered.

Storage Warning Banner:
* Full-width band between nav and page title (conditionally visible when >80% full).
* Height 48px, background #FFFCE0, border-bottom 1px #FFD400.
* Content (max-width 1000px, centered, flex row, align-items center, gap 16px):
  * Warning icon 18px #FFD400.
  * "Storage 85% full (8.5 GB of 10 GB)" — 14px/500/#0F1419.
  * "Upgrade Plan" — 14px/700/#1D9BF0 link.
  * "Manage Storage" — 14px/400/#536471 link.
  * Close "×" button: 24px, #8B98A5, right side (margin-left auto).

Mobile empty state: same structure, full-width, padding 0 20px. "Connect Account" full-width.
Mobile storage warning: two-line stacked (text on line 1, buttons on line 2).


====================================================================
PROMPT 7 — Mobile Bottom Tab Bar
====================================================================

Create the mobile bottom tab bar. Reference the bottom nav in both mobile ASCII mockups.

Bottom tab bar (mobile only):
* Fixed position, bottom 0, full width, height 56px.
* Background: #FFFFFF. Border-top: 1px #EFF3F4.
* Safe-area padding bottom for notch devices (env(safe-area-inset-bottom)).
* 4 tabs equally spaced (flex, justify-content space-around):
  Tab 1: Home icon + "Dashboard" label.
  Tab 2: Grid/list icon + "View" label.
  Tab 3: Upload icon + "Export" label.
  Tab 4: Gear icon + "Settings" label.
* Each tab: flex-direction column, align-items center, gap 2px.
  Icon: 24px. Label: 11px/500.
  Active tab (Dashboard): icon + label color #1D9BF0.
  Inactive: icon + label color #536471.
  Active indicator: 2px top border #1D9BF0 (on the tab item, at top of tab bar).
* Tap states: all tabs 44x44px minimum tap target.
* Tab transition: instant color change on tap.


====================================================================
COMPONENT VARIANTS
====================================================================

Account Card
* variant=complete: #00BA7C badge, green progress fill
* variant=syncing: #1D9BF0 badge, overlay with progress, disabled Sync button
* variant=error: red border, #F4212E badge, "Retry" button
* variant=disconnected: #FF7A00 badge, "Reconnect" button
* variant=gaps: "Backup Complete" badge + gap orange indicator row

Status Panel Dot
* variant=operational: #00BA7C
* variant=warning: #FFD400
* variant=error: #F4212E
* variant=never-synced: #8B98A5

Activity Row Icon
* variant=success: #00BA7C circle, white checkmark
* variant=warning: #FFD400 circle, white exclamation
* variant=error: #F4212E circle, white X

More Menu (⋮) Dropdown
* Items: Edit Settings | Export Data | View Errors | [divider] | Disconnect (red) |
  Remove (red bold)
* Shadow: 0 4px 12px rgba(15,20,25,0.15)

Mobile Bottom Tab
* variant=active: #1D9BF0 icon + label + 2px top indicator
* variant=inactive: #536471 icon + label
* Tabs: Dashboard, View, Export, Settings

Swipe Actions (mobile card)
* Revealed on swipe-left: Sync (blue), Export (gray), Disconnect (red)
* Each action: 64px wide, full card height, icon + label 11px
