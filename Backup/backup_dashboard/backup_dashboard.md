backup_dashboard — Page Spec
============================

Page ID: backup_dashboard
URL: /dashboard
Portal: main_site (authenticated)
ASCII Sources: Page_Dashboard_Web_UI.md, Page_Dashboard_Mobile_UI.md


OVERVIEW
========

The main hub for Backup Posts. Authenticated users land here after completing setup or
after login. Shows system status, all connected account cards, an "Add Another Account"
call-out, and a recent activity log. All sync operations can be triggered from here.


PAGE LAYOUT — DESKTOP
=====================

1. Full top navigation bar (authenticated)
   * Logo left.
   * Nav links: Dashboard (active), Export, Settings. 15px/500.
   * Right: "Account ▾" dropdown + "Logout" ghost link.
   * Height 64px, border-bottom 1px #EFF3F4.

2. Page title
   * "Your Backups" — 23px/700/#0F1419, margin 32px auto 24px, max-width 1000px.

3. Backup Status Panel (max-width 1000px, centered)
   * Card: white bg, border 1px #EFF3F4, radius 24px, padding 24px.
   * Status indicator row (flex, align-items center, gap 12px):
     * Dot (12px circle): operational = #00BA7C | warning = #FFD400 | error = #F4212E |
       never synced = #8B98A5.
     * "All Systems Operational" — 15px/700/#0F1419.
     * Right side: "Last backup: 2 hours ago" — 13px/400/#536471.
   * Sub-row: "Next auto-sync in: 22 hours" — 13px/400/#536471, margin-top 4px.
   * "Sync All Now" — filled blue pill, height 40px, 15px/700, margin-top 16px.
     On click: button shows spinner + "Syncing...", account cards show progress overlays.

4. Connected Accounts section (max-width 1000px, centered, margin-top 24px)
   * Section label: "Connected Accounts" — 15px/700/#0F1419 (not a section header,
     visually part of card).
   * 2-column grid (desktop), gap 20px.
   * Left: Account card(s). Right: Add Another Account card (dashed).

   Account Card (@username / Twitter/X):
   * Card: white bg, border 1px #EFF3F4, radius 24px, padding 24px.
   * Platform header row (flex, align-items center, gap 10px):
     * Platform icon: 32px circle, black bg, white X letterform.
     * Handle: "@username" 15px/700/#0F1419.
     * Platform name: "Twitter/X" 13px/400/#536471.
     * Right: badge "✓ Backup Complete" — #E8F9F2 bg, #00BA7C text, 9999px, 11px/700.
   * Stats section (margin-top 16px):
     * "2,847 posts backed up" — 14px/600/#0F1419.
     * Coverage progress bar: 95% fill, height 8px, #00BA7C fill (fully backed up),
       track #EFF3F4, radius 9999px.
     * Coverage label below bar: "Posts from Jan 2020 – Present" 12px/400/#8B98A5.
     * 2 stat rows below bar (gap 4px): "1,204 followers" | "892 following" —
       13px/400/#536471.
     * "Last synced: 2 hours ago" — 12px/400/#8B98A5, margin-top 8px.
   * Action row (margin-top 16px, flex, gap 10px, align-items center):
     * "Sync Now" — ghost pill, height 36px, 13px/700/#1D9BF0, border #1D9BF0.
     * "View" — ghost pill, height 36px, 13px/700/#536471, border #CFD9DE.
     * [⋮] more button (24px, #536471): opens dropdown.

   Add Another Account Card:
   * Card: border 2px dashed #CFD9DE, border-radius 24px, padding 24px,
     min-height same as account card. Display flex, flex-direction column,
     justify-content center, align-items center.
   * [+] icon: 48px circle, #EFF3F4 bg, #536471 "+" 24px inside.
   * Title: "Add Another Account" — 15px/700/#0F1419, margin-top 12px.
   * Description: "Connect additional social media accounts" — 13px/400/#536471,
     text-align center.
   * "Add Account" — filled blue pill, height 40px, 15px/700, margin-top 16px.

5. Recent Activity section (max-width 1000px, centered, margin-top 24px)
   * Section heading: "Recent Activity" — 15px/700/#0F1419, margin-bottom 16px.
   * Card: white bg, border 1px #EFF3F4, radius 24px, padding 24px.
   * 5 activity rows (gap 0, dividers 1px #EFF3F4 between rows):
     Each row: flex, align-items flex-start, padding 14px 0, gap 12px.
     * Icon (20px circle): ✓ = #00BA7C | ⚠ = #FFD400 | ✗ = #F4212E.
     * Text block (flex-grow):
       Main text: 14px/600/#0F1419.
       Sub text (details): 13px/400/#536471, margin-top 2px.
     * Timestamp: 12px/400/#8B98A5, flex-shrink 0.
   * Activity rows (desktop view):
     Row 1: ✓ "Full backup completed for @username" / "2,847 posts, 1,204 followers, 892 following" / "2 hours ago"
     Row 2: ✓ "Media download completed" / "1,523 images and videos saved" / "2 hours ago"
     Row 3: ✓ "Incremental sync completed" / "14 new posts backed up" / "1 day ago"
     Row 4: ✓ "Account connected: @username" / "" / "3 days ago"
     Row 5: ✓ "Chrome extension installed" / "" / "3 days ago"
   * "View All" — ghost pill button, height 36px, 13px/700, centered, margin-top 16px.


ACCOUNT CARD STATES
===================

Complete (default shown):
  Badge: "✓ Backup Complete" — #E8F9F2 bg, #00BA7C text.
  Progress bar: #00BA7C fill.

Syncing (while in progress):
  Badge: "Syncing..." — #EBF5FF bg, #1D9BF0 text, spinning dot.
  Progress overlay on card: semi-transparent #FFFFFF 80%, with progress bar and
  "Posts (2,104 / 2,847)" 13px/400/#536471.
  "Sync Now" button becomes "Syncing..." disabled.

Error:
  Badge: "⚠ Sync Failed" — #FFF5F5 bg, #F4212E text.
  Red border on card: border-color #F4212E.
  Below last-synced: "View Error →" 13px/400/#F4212E.

Disconnected:
  Badge: "Disconnected" — #FFFCE0 bg, #FF7A00 text.
  "Sync Now" replaced by "Reconnect" — orange ghost pill, border #FF7A00, text #FF7A00.

Gaps detected:
  Additional row in stats: "3 gaps detected" orange badge + "Deep Sync" ghost orange button.


MORE MENU (⋮) DROPDOWN
========================

* Dropdown: white card, border 1px #EFF3F4, radius 16px, shadow FAB, 180px wide.
* Items (4px gap, 14px/400/#0F1419, 36px row height, hover #F7F9F9):
  "Edit Settings" | "Export Data" | "View Errors" | divider 1px #EFF3F4 |
  "Disconnect Account" (#F4212E text) | "Remove Account" (#F4212E text, bold)


STORAGE WARNING BANNER (>80% full)
===================================

* Full-width banner at top of page (below nav, above page title).
* #FFFCE0 bg, border-bottom 1px #FFD400, padding 12px 24px.
* "Storage 85% full (8.5 GB of 10 GB)" + "Upgrade Plan" blue link + "Manage Storage" ghost.


EMPTY STATE (no accounts connected)
=====================================

* Full page centered block (replaces status panel + accounts section).
* Illustration placeholder: 200px circle, #F7F9F9 bg.
* "Connect your first social media account to start backing up your posts."
  20px/700/#0F1419, text-align center, margin-top 24px.
* "Connect Account" — filled blue pill, height 52px, 17px/700, margin-top 20px.


PAGE LAYOUT — MOBILE
====================

* Top bar: hamburger left, logo center, "Account ▾" right. Height 56px.
* Status panel: full-width card, condensed (Status dot + text + last/next on 2 lines).
  "Sync All Now" full-width button.
* Account cards: full-width stacked, padding 20px. Stats condensed.
* Action buttons inside card: "Sync" + "View" side by side + [⋮]. Smaller (32px height).
* Add Account card: full-width dashed, centered content.
* Recent Activity: 3 items (not 5). "View All" full-width ghost button.
* Bottom tab bar: fixed, 4 tabs: [🏠 Dashboard] [📋 View] [📤 Export] [⚙ Settings].
  Height 56px, border-top 1px #EFF3F4. Active tab text + icon: #1D9BF0. Inactive: #536471.

Mobile touch interactions:
* Swipe left on account card reveals: "Sync", "Export", "Disconnect" action buttons.
* Pull-to-refresh triggers sync check.


NAVIGATION
==========

Sync All Now -> stay on page, all account cards show syncing state.
Sync Now (card) -> stay on page, that card shows syncing state.
View (card) -> /view/twitter/username (backup_viewer).
Add Account -> /setup/connect.
View All (activity) -> /activity.
Account ▾ -> dropdown: Profile, API Keys, Help, Logout.
Export (nav) -> /export.
Settings (nav) -> /settings.
Go to Dashboard (from any page) -> /dashboard.
