backup_setup_options — Page Spec
================================

Page ID: backup_setup_options
URL: /setup/options
Portal: main_site (authenticated, setup wizard step 2)
ASCII Sources: Page_Setup_Options_Web_UI.md, Page_Setup_Options_Mobile_UI.md


OVERVIEW
========

Step 2 of the 3-step setup wizard. Users configure what to back up (posts, followers,
following), granular post options (replies, retweets, media), sync schedule, and see
a live storage estimate. All selections auto-save as user changes them. The primary
CTA is "Start First Backup" which initiates the backup and advances to step 3.


PAGE LAYOUT — DESKTOP
=====================

1. Minimal authenticated header (same as setup_connect page)

2. Setup Progress Stepper — step 2 active ("Options")
   * Step 1 Connect: filled circle with checkmark (completed, #1D9BF0 bg)
   * Step 2 Options: filled circle "2" (active, #1D9BF0 bg), label bold
   * Step 3 Backup: hollow circle "3" (upcoming, #EFF3F4 bg)
   * Connector line 1→2: filled #1D9BF0. Connector line 2→3: #EFF3F4.

3. Page header
   * "What would you like to back up?" — 23px/700/#0F1419, centered.
   * Margin-bottom 32px.

4. Configuration cards (max-width 680px, centered, gap 16px)

   Card A — Backup Content (Posts)
   * Section label: "BACKUP CONTENT" — 11px/700/#8B98A5 uppercase, margin-bottom 12px.
   * Primary checkbox row: [✓] checkbox + "Back up posts (tweets, threads, replies)"
     17px/600/#0F1419.
   * Description below: "Your original tweets, retweets, quote tweets, and replies.
     Includes images, videos, and GIFs." 14px/400/#536471.
   * Advanced Options panel (collapsible, default expanded if < 1,000 posts):
     * "Advanced Options" label 13px/700/#0F1419 + "▶" chevron toggle.
     * 4 nested checkboxes (indented 20px, gap 8px):
       [✓] Include replies
       [✓] Include quote tweets
       [✓] Include retweets
       [✓] Include media (images, videos, GIFs)
   * Count estimate: "Estimated: ~2,847 posts" — 13px/500/#536471, margin-top 12px.

   Card B — Backup Followers
   * Primary checkbox: [✓] "Back up followers (people who follow you)" 17px/600
   * Description: "Preserve your follower list with names, handles, and profiles.
     Track follower changes over time." 14px/400/#536471.
   * Count estimate: "Estimated: ~1,204 followers"

   Card C — Backup Following
   * Primary checkbox: [✓] "Back up following (people you follow)" 17px/600
   * Description: "Keep a record of accounts you follow. Useful for rebuilding your
     network on other platforms." 14px/400/#536471.
   * Count estimate: "Estimated: ~892 accounts"

   Card D — Sync Schedule
   * Section label: "SYNC SCHEDULE" — 11px/700/#8B98A5 uppercase.
   * Intro: "How often should we automatically sync your backup?" 14px/400/#536471.
   * 4 radio options (gap 12px):
     (●) Every 24 hours — Recommended (label 15px/600, sub 13px/400/#536471)
     ( ) Every 12 hours — More frequent backups for active accounts
     ( ) Every 6 hours — Maximum frequency (Creator plan or higher)
     ( ) Manual only — You trigger backups yourself (not recommended)
   * Locked options show padlock icon + "Creator plan required" tooltip on hover.

   Card E — Storage Estimate
   * Section label: "STORAGE ESTIMATE"
   * "Based on your selections:" — 13px/400/#536471.
   * Usage breakdown (table-like rows, left label / right value, 14px):
     "Text + metadata"  / "~42 MB"
     "Media (images, videos)" / "~850 MB"
     "Total estimated" / "~892 MB" (bold)
     "Available (Free plan)" / "~10 GB" with linear progress bar:
       bar width 100%, height 8px, fill = % used, color:
       < 60%: #00BA7C | 60–80%: #FFD400 | > 80%: #F4212E
   * Warning block (shows when > 80% of limit):
     [⚠] "You may reach your storage limit after ~15 backups" — #FFD400 bg tint
     (#FFFCE0), border-left 3px #FFD400, padding 12px 16px, radius 8px.
     Link: "Upgrade to Creator plan for unlimited storage →" #1D9BF0.

5. Action row (max-width 680px, margin 24px auto, flex, gap 16px, justify flex-end)
   * "Back" — ghost pill, height 44px, 15px/500/#536471, border #CFD9DE.
   * "Start First Backup" — filled blue pill, height 52px, 17px/700/#FFFFFF, #1D9BF0.
     Disabled state: #8B98A5 bg, cursor not-allowed.
     Disabled tooltip: "Select at least one type of data to back up"

6. Footer: same as setup_connect page.


PAGE LAYOUT — MOBILE
====================

* Header + progress stepper (step 2 dots active): same minimal style.
* Page header: "What to back up?" (shortened), 20px/700, left-aligned, padding 0 20px.
* Cards stacked, full-width, padding 20px.
* Advanced Options collapsed by default on mobile (saves space).
* Sync schedule radio labels shortened (no sub-descriptions, just "24 hours - Rec'd").
* Storage estimate condensed (no table, just pill-style breakdowns).
* Action buttons: stacked full-width. "Start First Backup" first (52px), "Back" below
  (44px ghost).


CHECKBOX STATES
===============

Checked (default): blue checkbox 18px, #1D9BF0 bg, white checkmark, border #1D9BF0.
Unchecked: 18px border 2px #CFD9DE, white bg.
Disabled (parent unchecked): 18px, #EFF3F4 bg, #8B98A5 border.
Focus ring: 2px offset #1D9BF0.

Radio button states:
Selected: 18px circle, #1D9BF0 fill dot center.
Unselected: 18px circle, border 2px #CFD9DE, white inside.
Locked: gray + padlock icon, cursor not-allowed.


STORAGE PROGRESS BAR STATES
============================

Green (#00BA7C fill): usage < 60% of plan limit.
Yellow (#FFD400 fill): 60–80%.
Red (#F4212E fill): > 80% — also shows warning block.


COPY — EXACT TEXT
=================

Page title: "What would you like to back up?"
Mobile title: "What to back up?"
Advanced options collapse label: "Advanced Options"
Schedule intro: "How often should we automatically sync your backup?"
Radio labels:
  "Every 24 hours — Recommended"
  "Every 12 hours"
  "Every 6 hours"
  "Manual only"
Storage warning: "You may reach your storage limit after ~15 backups"
Upgrade link: "Upgrade to Creator plan for unlimited storage →"
Primary CTA: "Start First Backup"
Back button: "Back"
Disabled tooltip: "Select at least one type of data to back up"


NAVIGATION
==========

Back -> /setup/connect
Start First Backup (valid) -> /setup/progress
Upgrade link -> /pricing or upgrade modal
Contact Support / Help Center -> /help
