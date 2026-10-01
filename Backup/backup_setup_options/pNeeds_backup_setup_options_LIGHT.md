dark_mode = false

# DESIGN MODE: LIGHT MODE
> This file specifies a **Light Mode** design.
> The UX designer who implements this file must apply a light mode visual style.
> Light mode uses a white background (#FFFFFF) with dark text (#0F1419 / #536471).
> Do NOT use dark mode colors when implementing these requirements.

---

# Product Requirements — Setup: Configure Options (Light Mode)
# Page: backup_setup_options | URL: /setup/options

---

## Page Purpose

Step 2 of the 3-step setup wizard. Users configure what content to back up, set their sync schedule, and see a live storage estimate. All selections auto-save. Primary CTA advances to Step 3.

---

## Navigation Requirements

- **Standalone backup web app — NO JFKSocial left sidebar.**
- Minimal authenticated top nav only.
- Wizard progress stepper: Step 1 completed, Step 2 active, Step 3 upcoming.

---

## Primary CTA

- Label: **"Start First Backup"**
- Style: filled blue pill, bg #1D9BF0, text #FFFFFF, height 52px, 17px/700
- Disabled when: no data types selected
- Disabled tooltip (exact): "Select at least one type of data to back up"

---

## Required Sections

### 1. Minimal Authenticated Header
### 2. Setup Progress Stepper (Step 2 Active)
### 3. Page Heading
- Title (exact): "What would you like to back up?"
- Mobile (exact): "What to back up?"

### 4. Configuration Cards (5 cards stacked, max-width 680px)

**Card A — Backup Content**
- "BACKUP CONTENT" section label (uppercase, muted)
- Primary checkbox: "Back up posts (tweets, threads, replies)" — default checked
- Description: tweets, retweets, quote tweets, replies, images, videos, GIFs
- Advanced Options (collapsible): Include replies, quote tweets, retweets, media
- Count estimate: "Estimated: ~2,847 posts"

**Card B — Backup Followers**
- "Back up followers (people who follow you)" — default checked
- Description and count estimate

**Card C — Backup Following**
- "Back up following (people you follow)" — default checked
- Description and count estimate

**Card D — Sync Schedule**
- "SYNC SCHEDULE" section label
- Radio options: Every 24 hours (default, recommended), Every 12 hours, Every 6 hours (locked — Creator plan), Manual only
- Locked option: shows padlock, tooltip "Creator plan required"

**Card E — Storage Estimate**
- "STORAGE ESTIMATE" section label
- Usage breakdown table: text metadata, media, total, available
- Color-coded progress bar (green/yellow/red by % used)
- Warning block shown when >80% full with upgrade link

### 5. Action Row
- "Back" (ghost) + "Start First Backup" (primary blue)
- Right-aligned desktop, stacked full-width mobile (primary first)

### 6. Footer

---

## Interaction Requirements

- Checkboxes auto-save on change; storage estimate updates live
- Parent unchecked → nested options disabled
- Locked radio (Every 6h) → padlock + tooltip on hover
- CTA disabled until ≥1 content type selected

---

## Copy (Exact Text)

- Title: "What would you like to back up?" | Mobile: "What to back up?"
- Advanced toggle: "Advanced Options"
- Schedule intro: "How often should we automatically sync your backup?"
- Radios: "Every 24 hours — Recommended" / "Every 12 hours" / "Every 6 hours" / "Manual only"
- Storage warning: "You may reach your storage limit after ~15 backups"
- Upgrade link: "Upgrade to Creator plan for unlimited storage →"
- Primary CTA: "Start First Backup" | Back: "Back"
- Disabled tooltip: "Select at least one type of data to back up"

---

## Navigation Destinations

- Back → /setup/connect
- Start First Backup → /setup/progress
- Upgrade link → /pricing or upgrade modal
- Help → /help
