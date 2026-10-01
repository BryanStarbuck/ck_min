backup_setup_connect — Page Spec
================================

Page ID: backup_setup_connect
URL: /setup/connect (also /setup)
Portal: main_site (authenticated, first-time setup)
ASCII Sources: Page_Setup_Connect_Web_UI.md, Page_Setup_Connect_Mobile_UI.md


OVERVIEW
========

Step 1 of the 3-step setup wizard. After creating an account (or arriving from the
Free Speech Defender wizard), users connect their social media account using one of
three methods: Chrome Extension, API Connection, or Manual Import.

This page is also reached by existing users who want to add another connected account
or reconnect a disconnected one.


PAGE LAYOUT — DESKTOP
=====================

1. Minimal authenticated header
   * Logo left, "Account ▾" dropdown + "Logout" right. No main nav links.
   * Height 64px, white bg, border-bottom 1px #EFF3F4.

2. Setup Progress Indicator
   * 3 steps in a horizontal stepper: Connect (active) → Options → Backup
   * Each step: filled circle (32px, #1D9BF0 bg active, #EFF3F4 bg inactive) +
     step label below (13px/500/#0F1419 active, #8B98A5 inactive)
   * Connecting lines between circles: 2px solid #1D9BF0 (completed), #EFF3F4 (future)
   * Centered horizontally, max-width 480px, margin 40px auto.

3. Page header
   * "Connect Your Social Media Account" — 23px/700/#0F1419, centered
   * "Choose how you'd like to back up your posts:" — 15px/400/#536471, centered
   * Margin-bottom 32px.

4. Three method cards (stacked vertically, max-width 680px, margin 0 auto, gap 16px)

   Card A — Chrome Extension (Recommended)
   * Card: white bg, border 1px #EFF3F4, radius 24px, padding 28px.
   * Header row: [Chrome/browser icon 32px] + "Chrome Extension (Recommended)" 17px/700
     + "Recommended" pill badge (#E8F9F2 bg, #00BA7C text, 9999px).
   * 4 benefit rows (green checkmark icon, 15px/400/#0F1419 text, gap 8px):
     "No API keys needed"
     "Works even if APIs are restricted"
     "Reads your profile page directly"
     "Most reliable method"
   * How it works description: 14px/400/#536471, margin-top 12px.
   * CTA: "Install Extension" — filled blue pill, height 44px, 15px/700, right-aligned
     in card.

   Card B — API Connection
   * Header row: [Key icon 32px] + "API Connection" 17px/700
   * "For developers with Twitter API access" — 13px/400/#536471
   * 2 benefit rows (green check): "Faster sync than extension" / "More complete data"
   * 2 warning rows (warning triangle icon #FFD400): "Requires developer credentials" /
     "Subject to API rate limits"
   * CTA: "Connect via API" — ghost pill button.
   * Expandable form (collapsed by default, expands on CTA click):
     - Platform dropdown: "Twitter/X ▾" (label: "Platform:", 15px/500)
     - Handle input: "Your Handle:" label + @[___] text input
     - API Key input (full-width)
     - API Secret input (full-width, type=password with show/hide toggle)
     - Access Token input (full-width, type=password)
     - Access Secret input (full-width, type=password)
     - Help link: "How to get API credentials →" 13px/400/#1D9BF0
     - Action row: "Cancel" ghost + "Connect" filled, right-aligned, gap 12px

   Card C — Manual Import
   * Header row: [Upload icon 32px] + "Manual Import" 17px/700
   * "Upload a data export file from your social network" — 13px/400/#536471
   * 2 benefits (green check): "Works with Twitter/X data exports" / "One-time import
     of historical data"
   * 2 warnings: "Does not support auto-sync" / "Must manually re-import for updates"
   * CTA: "Upload File" — ghost pill button.
   * Expandable file drop zone (collapsed by default):
     - Dashed border rectangle: 2px dashed #CFD9DE, radius 16px, padding 40px,
       min-height 160px, background #F7F9F9.
     - Centered: "Drag & drop your data export ZIP here" 15px/400/#536471
     - "or" in 13px/400/#8B98A5
     - "Browse Files" ghost button, 40px height
     - Below: "Accepted: .zip (Twitter data export) | Max size: 500 MB" 12px/400/#8B98A5
     - Help link: "How to download your Twitter data export →"

5. Skip action
   * "Skip for Now" — ghost pill button, 15px/500/#536471, margin-top 24px, centered.

6. Footer bar
   * "Need help? [Contact Support] | [Help Center]" — 13px/400/#8B98A5, centered.


PAGE LAYOUT — MOBILE
====================

* Minimal top bar: logo center, "Account ▾" right. Height 56px.
* Progress indicator: simplified dots (3 dots, active = #1D9BF0, inactive = #CFD9DE,
  labels below each dot), full-width row, padding 12px 20px.
* Page header: "Connect Your Account" (shortened), 20px/700, left-aligned, padding 0 20px.
* Method cards: full-width stacked, padding 20px, gap 12px.
* Expanded forms: accordion (only one open at a time). Form fields full-width stacked.
* "Skip for Now": full-width ghost button, 52px height.
* Footer: "Need help? [Contact] [Help Center]" — 13px, centered.


FORM STATES
===========

Chrome Extension — after install detected:
  Banner inside card: "Extension detected! Click Continue to connect." (#E8F9F2 bg,
  green border). "Continue" button replaces "Install Extension".

API form — validation states:
  Validating: "Connect" button shows spinner + "Validating..." text, disabled.
  Success: "✓ Connected!" green inline message, card collapses, auto-advance after 1s.
  Error: Inline error below Connect button: "Invalid credentials. Please check and try
  again." #F4212E text, 13px.

File upload states:
  Uploading: progress bar 4px height #1D9BF0, percentage text.
  Parsing: "Parsing data... this may take a minute" with spinner.
  Preview: "Found: 2,847 posts, 1,204 followers, 892 following. Continue?" with
  "Import" button and counts displayed as pills.
  Error: "Unable to read this file. Make sure it's an official Twitter data export ZIP."

Skip confirmation modal:
  Title: "Skip connecting an account?"
  Body: "You won't be able to back up posts until you connect an account. Are you sure?"
  Buttons: "Go Back" (ghost, default focus) + "Skip Anyway" (ghost, red text #F4212E)


ERROR STATES
============

Extension not detected: "Extension not detected. Please install it and refresh this page."
  shown as inline banner in Card A.
API rate limited: "Twitter API is currently rate limiting us. Please try again in 15 minutes."
File too large: "File exceeds 500MB limit. Please contact support for enterprise import."


COPY — EXACT TEXT
=================

Page title: "Connect Your Social Media Account"
Subtitle: "Choose how you'd like to back up your posts:"
Card A header: "Chrome Extension (Recommended)"
Card B header: "API Connection"
Card C header: "Manual Import"
Card A how it works: "Install our Chrome extension, and it will read your Twitter/X
  profile when you visit it. All data is sent securely to your backup account."
Skip button: "Skip for Now"
Skip modal title: "Skip connecting an account?"
Footer: "Need help? Contact Support | Help Center"


NAVIGATION
==========

Install Extension -> Chrome Web Store (new tab)
Connect (API form success) -> /setup/options
Upload + Import (file success) -> /setup/options
Skip Anyway -> /dashboard (empty state)
Back navigation: logo -> / (landing)
Contact Support -> /help | Help Center -> /help
