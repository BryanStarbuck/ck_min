pFig — backup_setup_connect
Figma Make Prompts: Setup — Connect Account (Step 1 of 3)
=========================================================

DESIGN TOKEN REFERENCE
=======================

Colors: page bg #FFFFFF | card bg #F7F9F9 | elevated #EFF3F4 | border subtle #EFF3F4 |
border prominent #CFD9DE | primary text #0F1419 | secondary #536471 | muted #8B98A5 |
brand blue #1D9BF0 (hover #1A8CD8) | success #00BA7C | danger #F4212E | warn #FFD400 |
success bg #E8F9F2 | blue tint #EBF5FF

Typography: font "TwitterChirp", system-ui, sans-serif |
page title 23px/700/#0F1419 | subtitle 15px/400/#536471 |
card header 17px/700/#0F1419 | body 15px/400/#0F1419 | caption 13px/400/#8B98A5 |
label 15px/500/#0F1419

Spacing: 4px base | card padding desktop 28px | card padding mobile 20px | gap 16px

Radii: cards 24px | buttons 9999px | inputs 12px | file zone 16px

Breakpoints: desktop >=1024px | mobile <640px


====================================================================
PROMPT 1 — Minimal Header and Setup Progress Stepper
====================================================================

Create the minimal authenticated header and the 3-step setup progress indicator.
This is a focused task flow (not the main site nav) so the header is stripped down.

Header (desktop):
* Full width, height 64px, white bg, border-bottom 1px #EFF3F4.
* Left: shield icon 20px #1D9BF0 + "Backup Posts" 18px/700/#0F1419, gap 8px.
* Right: "Account ▾" dropdown trigger (avatar placeholder 32px circle #EFF3F4,
  handle text 15px/400/#0F1419, chevron icon #536471) then "Logout" ghost text link
  15px/500/#536471. Gap: 16px.

Header (mobile):
* Height 56px, border-bottom 1px #EFF3F4.
* Left: shield icon + "Backup Posts" 16px/700.
* Right: "Account ▾" 14px/500 with avatar 28px.

Setup Progress Stepper (desktop):
* Container: max-width 480px, margin 40px auto 0, padding-bottom 40px.
* 3 steps connected by horizontal lines.
* Step structure: circle + label below.
  * Step 1 "Connect" (active): circle 32px, #1D9BF0 bg, white "1" 13px/700.
    Label: 13px/700/#0F1419 below.
  * Step 2 "Options" (upcoming): circle 32px, #EFF3F4 bg, #8B98A5 "2" 13px/700.
    Label: 13px/400/#8B98A5.
  * Step 3 "Backup" (upcoming): same as step 2 but "3".
* Connector lines between circles: 2px, width fills gap, #EFF3F4 bg (all inactive
  at step 1).
* Whole stepper centered in page.

Setup Progress Stepper (mobile):
* Full width, padding 16px 20px.
* 3 dots + labels. Dots: 12px circle. Active #1D9BF0, inactive #EFF3F4.
* Labels below each dot: 11px/500 — "Connect" (active, #0F1419) | "Options" (#8B98A5) |
  "Backup" (#8B98A5).
* Connector lines: 2px, horizontal, stretch between dots.


====================================================================
PROMPT 2 — Page Header Text and Chrome Extension Card
====================================================================

Create the page header (title + subtitle) and the first method card: Chrome Extension.
Reference the Card A layout in the web ASCII mockup.

Page header (desktop):
* "Connect Your Social Media Account" — 23px/700/#0F1419, text-align center.
* "Choose how you'd like to back up your posts:" — 15px/400/#536471, text-align center,
  margin-top 8px.
* Margin-bottom 32px.

Mobile: "Connect Your Account" — 20px/700, text-align left, padding 0 20px.
  Subtitle: 14px/400/#536471.

Chrome Extension Card (desktop + mobile):
* Container: max-width 680px desktop (centered), full-width mobile with 20px padding.
* Card: white bg, border 1px #EFF3F4, radius 24px, padding 28px.
* Card header row (flex, align-items center, gap 12px, margin-bottom 16px):
  * Icon zone: 40px circle #EBF5FF bg, browser/chrome icon 24px #1D9BF0 inside.
  * Title: "Chrome Extension" 17px/700/#0F1419.
  * Badge: "Recommended" — 9999px pill, #E8F9F2 bg, #00BA7C text, 11px/700,
    padding 3px 10px, margin-left auto.
* Benefit list (gap 8px, margin-bottom 16px):
  * Each item: flex row, checkmark icon 16px #00BA7C, text 15px/400/#0F1419, gap 8px.
  * Items: "No API keys needed" | "Works even if APIs are restricted" |
    "Reads your profile page directly" | "Most reliable method"
* How it works description: 14px/400/#536471, line-height 1.5, margin-bottom 20px.
  Text: "Install our Chrome extension, and it will read your Twitter/X profile when
  you visit it. All data is sent securely to your backup account."
* CTA row (text-align right):
  * "Install Extension" — filled blue pill, height 44px, 15px/700/#FFFFFF,
    padding 0 24px, background #1D9BF0, radius 9999px.
  * Hover: #1A8CD8. Active: #1570B8.

Extension detected state variant (overlay replaces CTA):
* Banner inside card: #E8F9F2 bg, 1px border #00BA7C, radius 12px, padding 12px 16px.
  Flex row: checkmark icon 20px #00BA7C + "Extension detected! Click Continue to connect."
  15px/500/#0F1419 + "Continue" blue pill button right side.

Mobile adaptation:
* CTA button full-width, height 52px.
* Benefit items: 14px text.


====================================================================
PROMPT 3 — API Connection Card (Collapsed + Expanded States)
====================================================================

Create the API Connection card showing both its collapsed state and its expanded form.
Reference the API Connection section of the web ASCII mockup.

API Connection Card — Collapsed state:
* Card: white bg, border 1px #EFF3F4, radius 24px, padding 28px.
* Header row: key icon 40px circle (#F7F0FF bg, key icon #7856FF), title
  "API Connection" 17px/700, subtitle "For developers with Twitter API access"
  13px/400/#536471 below title.
* 2 benefit rows (green check): "Faster sync than extension" / "More complete data"
* 2 warning rows (triangle icon 16px #FFD400): "Requires developer credentials" /
  "Subject to API rate limits"
* CTA row: "Connect via API" — ghost pill, 1px border #1D9BF0, #1D9BF0 text,
  height 44px, 15px/700, right-aligned.

API Connection Card — Expanded state (add below collapsed):
* Expansion adds a form block inside the card with a subtle top border 1px #EFF3F4,
  margin-top 20px, padding-top 20px.
* Form fields stacked, gap 16px:
  * Platform dropdown: label "Platform" 13px/700/#0F1419, select control full-width,
    height 44px, border 1px #CFD9DE, radius 12px, "Twitter/X ▾" default text,
    15px/400/#0F1419, padding 0 12px. Chevron icon right.
  * Handle input: label "Your Handle", input with "@" prefix icon left,
    placeholder "username", height 44px, border 1px #CFD9DE, radius 12px.
  * API Key input: label "API Key", full-width, height 44px, 14px/400 monospace.
  * API Secret input: label "API Secret", type password, show/hide eye icon right,
    same style.
  * Access Token input: label "Access Token", same style.
  * Access Secret input: label "Access Secret", same style.
* Help link: "How to get API credentials →" 13px/400/#1D9BF0, margin-top 4px.
* Action row (margin-top 20px, flex, gap 12px, justify-content flex-end):
  * "Cancel" — ghost pill, height 40px, 15px/500/#536471, border #CFD9DE.
  * "Connect" — filled blue pill, height 40px, 15px/700/#FFFFFF, #1D9BF0 bg.

Input states:
* Default: border #CFD9DE, bg #FFFFFF.
* Focus: border #1D9BF0, box-shadow 0 0 0 3px #EBF5FF.
* Error: border #F4212E, bg #FFF5F5.
* Success: border #00BA7C.
* Disabled: bg #F7F9F9, text #8B98A5.

Validating state (Connect button):
* "Connect" shows spinner (16px rotating circle, white) + " Validating..." text, disabled.

Success state:
* Replace form with: green checkmark circle 32px #00BA7C + "Connected!" 17px/700/#0F1419,
  auto-advance countdown: "Proceeding in 1..." 13px/400/#536471.

Mobile adaptation:
* All inputs full-width. Cancel + Connect buttons full-width stacked (Connect first).


====================================================================
PROMPT 4 — Manual Import Card and Skip Action
====================================================================

Create the Manual Import card (collapsed + expanded) and the Skip for Now action.
Reference the Manual Import section of the web ASCII mockup.

Manual Import Card — Collapsed state:
* Header row: upload icon 40px circle (#FFF8F0 bg, upload-cloud icon 24px #FF7A00),
  title "Manual Import" 17px/700, subtitle "Upload a data export file from your
  social network" 13px/400/#536471.
* 2 benefits (green check): "Works with Twitter/X data exports" /
  "One-time import of historical data"
* 2 warnings (triangle icon, #FFD400): "Does not support auto-sync" /
  "Must manually re-import for updates"
* CTA: "Upload File" — ghost pill, height 44px, right-aligned.

Manual Import Card — Expanded state:
* Expansion adds file drop zone block (top border 1px #EFF3F4, margin-top 20px,
  padding-top 20px):
  * Drop zone rectangle: 2px dashed #CFD9DE, radius 16px, padding 40px 24px,
    min-height 160px, background #F7F9F9. Centered content:
    Upload icon 40px #8B98A5 (or drag indicator).
    "Drag & drop your data export ZIP here" 15px/400/#536471.
    "or" 13px/400/#8B98A5, margin 8px 0.
    "Browse Files" — ghost pill button, height 40px, 15px/700/#1D9BF0.
    Below: "Accepted: .zip (Twitter data export)  •  Max size: 500 MB" 12px/400/#8B98A5.
  * Drop zone hover state: border color #1D9BF0, bg #EBF5FF (dashed still), scale 1.01.
  * File dragging over state: same as hover.
* Help link: "How to download your Twitter data export →" 13px/400/#1D9BF0.

Upload progress state (replaces drop zone):
* Linear progress bar: full-width, 8px height, bg #EFF3F4, fill #1D9BF0, radius 9999px.
  "Uploading... 45%" text 14px/400/#536471 above bar.
* Parsing state: spinner + "Parsing data... this may take a minute" 14px/400/#536471.
* Preview state: green confirmation box, counts as pills:
  "Found: 2,847 posts  1,204 followers  892 following" — pill style #EFF3F4 bg,
  13px/700/#0F1419. Then: "Import" filled button + "Cancel" ghost button.

Skip Action:
* Below all cards, margin-top 32px, text-align center.
* "Skip for Now" — ghost pill, height 44px, 15px/500/#536471, border #CFD9DE.
  Hover: bg #F7F9F9.

Footer bar:
* Border-top 1px #EFF3F4, padding 20px, text-align center.
* "Need help? " then "Contact Support" and " | " and "Help Center" as #1D9BF0 links.
* 13px/400/#8B98A5 for static text.

Skip confirmation modal:
* Overlay: rgba(0,0,0,0.4) backdrop.
* Modal card: white, radius 24px, max-width 400px centered, padding 32px.
* Title: "Skip connecting an account?" 20px/700/#0F1419.
* Body: "You won't be able to back up posts until you connect an account. Are you sure?"
  15px/400/#536471, margin-top 8px.
* Buttons (margin-top 24px, flex gap 12px, justify-content flex-end):
  "Go Back" — filled blue pill (default focus ring).
  "Skip Anyway" — ghost pill, #F4212E text + border.

Mobile adaptation:
* Drop zone: "Tap to select file" instead of drag text. No drag-and-drop icon.
* Drop zone min-height 120px.
* Skip button: full-width, height 52px.


====================================================================
COMPONENT VARIANTS
====================================================================

Method Card
* variant=chrome-extension: blue icon circle, Recommended badge, green benefits
* variant=api-connection: purple icon circle, green+yellow mixed benefits
* variant=manual-import: orange icon circle, green+yellow mixed benefits
* state=collapsed: shows header + benefits + single CTA
* state=expanded: adds form or drop zone below with top divider

Setup Stepper Step
* variant=active: #1D9BF0 circle, bold label
* variant=completed: #1D9BF0 circle, checkmark icon, bold label
* variant=upcoming: #EFF3F4 circle, muted label

Form Input Field
* state=default: border #CFD9DE
* state=focus: border #1D9BF0, shadow #EBF5FF
* state=error: border #F4212E, error message below in #F4212E 12px
* state=success: border #00BA7C
* Special: password fields include show/hide eye icon toggle right side

File Drop Zone
* state=empty: dashed #CFD9DE, #F7F9F9 bg
* state=dragover: dashed #1D9BF0, #EBF5FF bg
* state=uploading: progress bar replaces content
* state=parsing: spinner + text
* state=preview: found counts + action buttons

Upload Progress Bar
* Track: #EFF3F4, height 8px, radius 9999px
* Fill: #1D9BF0, animated width transition
* Label above: "Uploading... 45%" 14px/400/#536471

API Validation Button
* state=idle: "Connect" filled blue
* state=loading: spinner + "Validating..." disabled
* state=success: replaced by success message
* state=error: re-enabled, error shown below
