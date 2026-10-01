backup_setup_progress — Page Spec
=================================

Page ID: backup_setup_progress
URL: /setup/progress
Portal: main_site (authenticated, setup wizard step 3)
ASCII Sources: Page_Setup_Progress_Web_UI.md, Page_Setup_Progress_Mobile_UI.md


OVERVIEW
========

Step 3 of the 3-step setup wizard. Shows real-time progress of the first backup.
Displays overall progress (with percentage), per-category progress bars (Posts,
Followers, Following, Media), estimated time remaining, and a "What's Happening"
reassurance panel. After completion, transitions to a success state with final counts
and a "Go to Dashboard" button.

Progress updates via WebSocket every 2 seconds (desktop) / 3 seconds (mobile).


PAGE LAYOUT — DESKTOP
=====================

1. Minimal authenticated header.

2. Setup Progress Stepper — step 3 active ("Backup")
   * Step 1 Connect: completed (checkmark).
   * Step 2 Options: completed (checkmark).
   * Step 3 Backup: active (filled circle #1D9BF0 "3").
   * Both connector lines: filled #1D9BF0 (all steps either complete or active).

3. Page header
   * "Backing up your account..." — 23px/700/#0F1419, text-align center.
   * Account identifier row (centered, gap 8px):
     Twitter/X icon 24px + "@username" 15px/600/#0F1419 + "(Twitter/X)" 13px/400/#536471.
   * Margin-bottom 32px.

4. Overall progress block (max-width 480px, centered)
   * Overall progress bar: full-width, height 16px, track #EFF3F4, fill #1D9BF0,
     radius 9999px. Animates smoothly as value updates.
   * Percentage label: "62%" — 20px/700/#0F1419, text-align right, above or below bar.
   * Time estimate: "Estimated time remaining: 3 minutes" — 14px/400/#536471,
     text-align center, margin-top 12px.

5. Category progress cards (max-width 640px, centered, padding 24px,
   card: white bg, border 1px #EFF3F4, radius 24px)
   * 4 category rows inside the card, gap 16px.
   * Each row structure:
     [Status Icon 20px] [Category Label 15px/600/#0F1419 flex-grow]
     [Count "X of Y" 13px/500/#536471] [Percentage 13px/700/#0F1419]
     Progress bar below: full-width, height 8px, track #EFF3F4.
   * Status icons:
     ✓ (checkmark circle, #00BA7C bg) = completed
     ⟳ (spinning circle, #1D9BF0) = in progress
     ⏳ (hourglass or pause circle, #8B98A5) = waiting/queued
   * Category data (in-progress state at 62%):
     Posts:     ✓ in-prog → "2,104 of 2,847" / "73%" / fill #1D9BF0
     Followers: ⟳ in-prog → "847 of 1,204" / "70%" / fill #1D9BF0
     Following: ⏳ waiting → "0 of 892"     / "0%"  / fill #EFF3F4 + "(waiting...)" suffix
     Media:     ⏳ waiting → "0 of 1,523"   / "0%"  / fill #EFF3F4 + "(waiting...)" suffix

6. Action row (centered, gap 16px)
   * "Run in Background" — ghost pill, height 44px, 15px/600/#536471, border #CFD9DE.
   * "Cancel" — ghost pill, height 44px, 15px/600/#F4212E, border #F4212E.

7. What's Happening panel (max-width 640px, centered)
   * Card: #F7F9F9 bg, border 1px #EFF3F4, radius 24px, padding 24px.
   * Title: "What's Happening" — 15px/700/#0F1419.
   * Body: "Your posts are being securely backed up to your account. This process may
     take several minutes depending on how much content you have." 14px/400/#536471.
   * "You can safely close this page and we'll email you when it's done." 14px/400/#536471.
   * 3 assurance rows (green check icon + text, 14px/400/#0F1419, gap 8px):
     "Your data is encrypted during transmission"
     "Rate limits are automatically respected"
     "Progress will resume if interrupted"

8. Footer: same minimal footer with Contact Support + Help Center.


COMPLETION STATE (replaces progress content after 100%):

* Large success illustration: circular checkmark animation 80px, #00BA7C fill,
  white checkmark, scale-in animation.
* Headline: "All done!" — 31px/700/#0F1419, centered.
* Subhead: "Your backup is complete and secure." — 15px/400/#536471, centered.
* 4 result rows (centered, gap 8px):
  ✓ 2,847 posts backed up
  ✓ 1,204 followers saved
  ✓ 892 following accounts preserved
  ✓ 1,523 media files downloaded
  (Each row: checkmark 20px #00BA7C, text 15px/500/#0F1419)
* Next backup notice: "Your next backup is scheduled for tomorrow at 3:00 PM."
  13px/400/#536471, centered, margin-top 12px.
* "Go to Dashboard" — filled blue pill, height 52px, 17px/700, centered, margin-top 24px.
* Auto-redirect after 5 seconds with countdown: "Redirecting in 5s..."


ERROR STATES
============

Rate limited:
  Yellow banner at top of progress card:
  "Rate limited. Waiting 15 minutes, then resuming automatically..."
  #FFFCE0 bg, border-left 3px #FFD400.
  Countdown timer: "Retrying in 14:32..."

Network error:
  Amber banner: "Connection lost. Retrying..." with spinner.

Extension disconnected:
  Banner: "Chrome extension disconnected. Please keep the extension running."

Fatal error:
  Red banner: error message. Buttons: "Retry" (filled blue) + "Contact Support" (ghost).


MOBILE-SPECIFIC
===============

* Top header: logo + "Account ▾". Height 56px.
* Progress stepper: dots, all 3 active/complete.
* Page header: "Backing up your account..." 20px/700, left-aligned. Account tag below.
* Overall progress bar: full-width, 12px height.
* Category card: full-width, padding 20px.
* Action buttons: stacked full-width ("Run in Background" first, "Cancel" below).
* What's Happening panel: condensed (shorter body text, 2 assurance items).
* WebSocket updates every 3 seconds (battery optimization).
* Completion state: same structure, stacked vertical.


NAVIGATION
==========

Run in Background -> toast: "Backup running. We'll email you when done." + navigates to /dashboard.
Cancel (confirmed) -> /setup/options or /dashboard.
Go to Dashboard -> /dashboard.
Contact Support -> /help.
