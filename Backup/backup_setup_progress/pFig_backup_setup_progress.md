pFig — backup_setup_progress
Figma Make Prompts: Setup — Backup Progress (Step 3 of 3)
=========================================================

DESIGN TOKEN REFERENCE
=======================

Colors: page bg #FFFFFF | card bg #F7F9F9 | elevated #EFF3F4 |
border subtle #EFF3F4 | border prominent #CFD9DE | primary text #0F1419 |
secondary #536471 | muted #8B98A5 | brand blue #1D9BF0 | success #00BA7C |
danger #F4212E | warning #FFD400 | warning bg #FFFCE0

Typography: page title 23px/700 | account tag 15px/600 | percentage 20px/700 |
time estimate 14px/400/#536471 | category label 15px/600 | count 13px/500/#536471 |
pct label 13px/700 | assurance text 14px/400 | completion headline 31px/700

Spacing: card padding 24px | category rows gap 16px | buttons gap 16px

Radii: cards 24px | progress bars 9999px | buttons 9999px | icon circles 50%

Breakpoints: desktop >=1024px | mobile <640px


====================================================================
PROMPT 1 — Header, Progress Stepper (Step 3 Active), and Page Title
====================================================================

Create the minimal header and the 3-step stepper in its all-steps-active/complete state.
Reference Page_Setup_Progress_Web_UI.md stepper section.

Header: minimal authenticated header (same as steps 1 and 2).

Setup Progress Stepper (all complete / step 3 active):
* Max-width 480px, centered, margin 40px auto 0, padding-bottom 40px.
* Step 1 "Connect" — completed: circle 32px #1D9BF0 bg, white checkmark icon.
  Connector to step 2: 2px solid #1D9BF0.
* Step 2 "Options" — completed: circle 32px #1D9BF0 bg, white checkmark icon.
  Connector to step 3: 2px solid #1D9BF0.
* Step 3 "Backup" — active: circle 32px #1D9BF0 bg, white "3" 13px/700.
  Label: "Backup" 13px/700/#0F1419.

Mobile stepper: 3 dots. Dots 1+2: #1D9BF0 with checkmark. Dot 3: #1D9BF0 filled.
Connectors: both filled #1D9BF0.

Page title block (desktop):
* "Backing up your account..." — 23px/700/#0F1419, text-align center, margin-bottom 12px.
* Account identifier row (flex, justify-content center, align-items center, gap 8px):
  * Twitter/X icon: 24px circle, #000000 bg, white "X" letterform.
  * Handle: "@username" — 15px/600/#0F1419.
  * Platform: "(Twitter/X)" — 13px/400/#536471.

Mobile: title 20px/700, left-aligned. Account row left-aligned below, 14px/500.


====================================================================
PROMPT 2 — Overall Progress Bar and Time Estimate
====================================================================

Create the overall progress section: large progress bar + percentage + time estimate.
Reference the large progress bar section of the web and mobile ASCII mockups.

Desktop:
* Container: max-width 480px, margin 0 auto 32px, text-align center.
* Percentage label above bar: "62%" — 20px/700/#0F1419, text-align right,
  margin-bottom 4px.
* Progress bar:
  * Track: full-width, height 16px, #EFF3F4 bg, radius 9999px.
  * Fill: 62% width, #1D9BF0 bg, radius 9999px (fill has same radius, no flat right edge).
  * Animated: width transition 500ms ease-in-out when value changes.
  * Loading shimmer on fill: subtle animated gradient from #1D9BF0 to #1A8CD8 to #1D9BF0,
    traveling left to right, 1.5s loop.
* Time estimate below bar: "Estimated time remaining: 3 minutes" — 14px/400/#536471,
  text-align center, margin-top 12px.

Mobile:
* Container full-width, padding 0 20px.
* Progress bar height 12px. Percentage 18px/700. Time estimate 13px/400.


====================================================================
PROMPT 3 — Category Progress Cards (4 Items)
====================================================================

Create the 4-category progress breakdown card. Reference the category rows in both
web and mobile ASCII mockups (Posts, Followers, Following, Media with their respective
status icons and progress bars).

Card container (desktop):
* Max-width 640px, centered, bg white, border 1px #EFF3F4, radius 24px, padding 24px.

4 category rows inside (flex-direction column, gap 16px):

Row structure (for each category):
* Top line: flex row, align-items center, gap 12px.
  * Status icon: 20px circle. States below.
  * Category name: flex-grow, 15px/600/#0F1419.
  * Count "X of Y": 13px/500/#536471.
  * Percentage: 13px/700/#0F1419.
* Progress bar below top line (margin-top 6px, margin-left 32px to align with text):
  Height 8px, track #EFF3F4, radius 9999px.
  Fill color and width per state.

Category data (show in-progress state at 62% overall):
Posts (completed-in-progress):
  Icon: checkmark circle 20px, #00BA7C bg, white checkmark. (Posts being actively synced
  can show spinning, or use completed check for first batch done. Show spinning ⟳.)
  Use spinning state: 20px circle, #1D9BF0 border 2px, top-arc fill, rotating animation.
  Count: "2,104 of 2,847"  Pct: "73%"  Fill: 73% #1D9BF0.

Followers (in progress):
  Icon: spinning circle, #1D9BF0.
  Count: "847 of 1,204"  Pct: "70%"  Fill: 70% #1D9BF0.

Following (waiting):
  Icon: hourglass or pause circle 20px, #8B98A5 bg, white pause icon.
  Count: "0 of 892"  Pct: "0%"  Fill: 0% (bar shows empty track only).
  Suffix after count: "(waiting...)" 12px/400/#8B98A5 italic.

Media (waiting):
  Icon: same hourglass/pause, #8B98A5 bg.
  Count: "0 of 1,523"  Pct: "0%"  Fill: empty.
  Suffix: "(waiting...)" same style.

Dividers between rows: 1px #EFF3F4 horizontal rule, or just gap 16px (no divider).
Use gap only (no dividers) for clean look.

Mobile adaptation:
* Full-width card, padding 20px. Progress bar margin-left 28px. Count and pct wrap if needed.
* Category names 14px/600. Count 12px/400. Pct 12px/700.


====================================================================
PROMPT 4 — Action Buttons and What's Happening Panel
====================================================================

Create the action buttons row and the "What's Happening" reassurance panel.
Reference the action row and info panel sections of the web and mobile ASCII mockups.

Action buttons (desktop):
* Container: max-width 640px, margin 24px auto, display flex, gap 16px,
  justify-content center.
* "Run in Background":
  Ghost pill, height 44px, 15px/600/#536471, border 1px #CFD9DE.
  Hover: #F7F9F9 bg. Tooltip on hover: "Close this page. We'll email you when done."
* "Cancel":
  Ghost pill, height 44px, 15px/600/#F4212E, border 1px #F4212E.
  Hover: #FFF5F5 bg.

Cancel confirmation modal:
* Overlay: rgba(0,0,0,0.4) backdrop, z-index 200.
* Modal: white, radius 24px, max-width 400px centered, padding 32px.
* "⚠ Stop this backup?" — 20px/700/#0F1419, warning icon #FFD400 left.
* Body: "Are you sure? Your backup will be incomplete. Partial data will be saved."
  15px/400/#536471.
* Buttons (margin-top 24px, flex, gap 12px, justify-content flex-end):
  "Keep Backing Up" — filled blue pill (default focused).
  "Stop Backup" — ghost pill, #F4212E text/border.

What's Happening panel (desktop):
* Container: max-width 640px, centered, margin-top 24px.
* Card: #F7F9F9 bg, border 1px #EFF3F4, radius 24px, padding 24px.
* Title: "What's Happening" — 15px/700/#0F1419, margin-bottom 12px.
* Body paragraphs (14px/400/#536471, gap 8px):
  Para 1: "Your posts are being securely backed up to your account. This process may
  take several minutes depending on how much content you have."
  Para 2: "You can safely close this page and we'll email you when it's done."
* Assurance list (3 items, margin-top 12px, gap 8px):
  Each: checkmark circle 16px #00BA7C + 14px/400/#0F1419 text, flex row gap 8px.
  "Your data is encrypted during transmission"
  "Rate limits are automatically respected"
  "Progress will resume if interrupted"

Mobile adaptations:
* Action buttons: stacked full-width. "Run in Background" first (52px), "Cancel" (44px).
* What's Happening: padding 20px. Body text 14px. Assurance items 13px. 2 items (drop 3rd).
* Footer: "Questions? Contact Support | Help Center" 13px, centered.


====================================================================
PROMPT 5 — Completion State (All Done!)
====================================================================

Create the completion state that replaces the progress content after 100%.
Reference the COMPLETION STATE section of both web and mobile ASCII mockups.

This is shown as a separate Figma frame representing the post-backup success state.

Desktop completion frame:
* Replace the progress content area with the completion block (centered, max-width 500px).
* Success animation placeholder: circle 80px, #00BA7C bg, white checkmark icon 40px inside.
  Show as static for Figma. Note: animates scale-in on transition.
* Headline: "All done!" — 31px/800/#0F1419, text-align center, margin-top 24px.
* Subhead: "Your backup is complete and secure." — 15px/400/#536471, text-align center,
  margin-top 8px.
* 4 result rows (centered, flex-direction column, gap 8px, margin-top 24px):
  Each row: flex row, justify-content center, align-items center, gap 10px.
  Checkmark icon 20px #00BA7C, text 15px/500/#0F1419.
  Row 1: "2,847 posts backed up"
  Row 2: "1,204 followers saved"
  Row 3: "892 following accounts preserved"
  Row 4: "1,523 media files downloaded"
* Next backup notice (margin-top 16px):
  "Your next backup is scheduled for tomorrow at 3:00 PM." — 13px/400/#8B98A5,
  text-align center.
* "Go to Dashboard" button (margin-top 24px, centered):
  Filled blue pill, height 52px, 17px/700/#FFFFFF, #1D9BF0 bg, padding 0 40px.
  Hover: #1A8CD8.
* Auto-redirect notice below button: "Redirecting to dashboard in 5s..." — 12px/400/#8B98A5.

Mobile completion frame:
* Same structure, vertically stacked. Headline 28px/800. Result rows 14px.
* "Go to Dashboard" full-width, height 52px. Below: countdown 12px.


====================================================================
PROMPT 6 — Error State Variants
====================================================================

Create 3 error banner variants shown inside the category progress card.
These are inline banners — they appear at the top of the category card and do not
replace the progress content.

Error Banner 1 — Rate limited (warning, yellow):
* Full-width, border-left 4px #FFD400, bg #FFFCE0, radius 8px, padding 12px 16px.
* Flex row: warning triangle icon 18px #FFD400 + text block + countdown right.
* Text: "Rate limited. Waiting before retrying." 14px/500/#0F1419.
* Sub: "Retrying automatically in:" 13px/400/#536471.
* Countdown timer: "14:32" — 20px/700/#0F1419, right-aligned, monospace.

Error Banner 2 — Network error (amber):
* Border-left 4px #FF7A00, bg #FFF5EC. Icon: wifi-off 18px #FF7A00.
* Text: "Connection lost. Retrying..." + spinning indicator 14px.
* Sub: "Backup will resume automatically." 13px/400/#536471.

Error Banner 3 — Fatal error (red):
* Border-left 4px #F4212E, bg #FFF5F5. Icon: x-circle 18px #F4212E.
* Text: "Backup failed. Please try again." 14px/500/#0F1419.
* Buttons (margin-top 8px, flex, gap 12px):
  "Retry" filled blue pill 40px height | "Contact Support" ghost pill.

Place each error banner variant as a separate component state in Figma.


====================================================================
COMPONENT VARIANTS
====================================================================

Category Progress Row
* variant=completed: checkmark circle #00BA7C, filled bar #00BA7C
* variant=in-progress: spinning circle #1D9BF0, partial filled bar #1D9BF0
* variant=waiting: pause circle #8B98A5, empty bar, "(waiting...)" suffix
* variant=error: x-circle #F4212E, partial bar #F4212E

Progress Bar
* size=large (overall): height 16px
* size=medium (category): height 8px
* track: #EFF3F4 | fill: #1D9BF0 (default) | fill-success: #00BA7C | fill-error: #F4212E
* shimmer animation: traveling gradient on active fills

Status Icon Circle (20px)
* spinning: CSS rotation animation 1s linear infinite
* checkmark: static, #00BA7C bg, white icon
* hourglass/pause: static, #8B98A5 bg, white icon
* error x: static, #F4212E bg, white icon

Completion Success Block
* Isolated frame/component for the all-done state
* Contains: success circle, headline, subhead, results list, next-backup note, CTA

Error Banner
* variant=warning-yellow | variant=network-amber | variant=fatal-red
* All: border-left, icon, title, subtitle structure
