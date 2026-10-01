dark_mode = true

# DESIGN MODE: DARK MODE
> This file specifies a **Dark Mode** design.
> The UX designer who implements this file must apply a dark mode visual style.
> Dark mode uses a dark background (#15202B) with light text (#FFFFFF / #8B98A5).
> Do NOT use light mode colors when implementing these requirements.

---

# Product Requirements — Setup: Configure Options (Dark Mode)
# Page: backup_setup_options | URL: /setup/options

---

## Page Purpose

Step 2 of the 3-step setup wizard. Users configure what content to back up, set their sync schedule, and see a live storage estimate. All selections auto-save. Primary CTA advances to Step 3 (backup progress).

---

## Navigation Requirements

- **Standalone backup web app — NO JFKSocial left sidebar.**
- Minimal authenticated top nav only.
- Wizard progress stepper: Step 1 completed (checkmark), Step 2 active, Step 3 upcoming.

---

## Primary CTA

- Label: **"Start First Backup"**
- Style: filled blue pill, bg #1D9BF0, text #FFFFFF, height 52px, 17px/700, radius 9999px
- Disabled when: no data types selected
- Disabled tooltip (exact): "Select at least one type of data to back up"

---

## Required Sections

### 1. Minimal Authenticated Header
- Same as setup_connect page

### 2. Setup Progress Stepper
- Step 1: completed (checkmark circle)
- Step 2: active ("Options" bold, filled circle)
- Step 3: upcoming
- Connector 1→2: blue (completed). Connector 2→3: gray.

### 3. Page Heading
- Title (exact): "What would you like to back up?"
- Mobile title (exact): "What to back up?"

### 4. Configuration Cards (5 cards, max-width 680px, stacked)

**Card A — Backup Content (Posts)**
- Section label: "BACKUP CONTENT" (uppercase, muted)
- Primary checkbox: "Back up posts (tweets, threads, replies)" — checked by default
- Description: includes original tweets, retweets, quote tweets, replies, images, videos, GIFs
- Advanced Options collapsible (default: expanded if < 1,000 posts):
  - Nested checkboxes (all checked by default): Include replies, Include quote tweets, Include retweets, Include media
  - Nested checkboxes disabled when parent unchecked
- Count estimate: "Estimated: ~2,847 posts"

**Card B — Backup Followers**
- Primary checkbox: "Back up followers (people who follow you)" — checked by default
- Description: preserve follower list with names, handles, profiles; track changes over time
- Count estimate: "Estimated: ~1,204 followers"

**Card C — Backup Following**
- Primary checkbox: "Back up following (people you follow)" — checked by default
- Description: keep record for rebuilding network on other platforms
- Count estimate: "Estimated: ~892 accounts"

**Card D — Sync Schedule**
- Section label: "SYNC SCHEDULE" (uppercase)
- Intro: "How often should we automatically sync your backup?"
- 4 radio options:
  - "Every 24 hours — Recommended" (default selected)
  - "Every 12 hours"
  - "Every 6 hours" — locked, shows padlock, "Creator plan required" tooltip
  - "Manual only — not recommended"

**Card E — Storage Estimate**
- Section label: "STORAGE ESTIMATE" (uppercase)
- "Based on your selections:" intro
- Usage table: Text + metadata (~42 MB), Media (~850 MB), Total (~892 MB bold), Available plan storage
- Linear progress bar colored by usage: green < 60%, yellow 60–80%, red > 80%
- Warning block shown when > 80%: "You may reach your storage limit after ~15 backups" + upgrade link

### 5. Action Row
- "Back" (ghost) + "Start First Backup" (filled blue primary)
- Flex, right-aligned
- Mobile: stacked full-width, primary first

### 6. Footer
- "Need help? Contact Support | Help Center"

---

## Required States & Interactions

### Checkbox Interactions
- Parent unchecked: nested advanced option checkboxes become disabled
- All selections auto-save (no explicit save needed)
- Storage estimate updates live when selections change

### Radio Options
- Locked "Every 6 hours": shows padlock icon, cursor not-allowed, tooltip on hover
- One option always selected (can't deselect all)

### Storage Warning Block
- Only visible when estimated usage > 80% of plan limit
- Contains upgrade link → /pricing or upgrade modal

### Primary CTA Button
- Enabled when: at least one content type selected (posts, followers, or following)
- Disabled state has tooltip

---

## Copy (Exact Text)

- Page title: "What would you like to back up?"
- Mobile title: "What to back up?"
- Advanced options toggle: "Advanced Options"
- Schedule intro: "How often should we automatically sync your backup?"
- Radio labels: "Every 24 hours — Recommended" / "Every 12 hours" / "Every 6 hours" / "Manual only"
- Storage warning: "You may reach your storage limit after ~15 backups"
- Upgrade link: "Upgrade to Creator plan for unlimited storage →"
- Primary CTA: "Start First Backup"
- Back button: "Back"
- Disabled tooltip: "Select at least one type of data to back up"

---

## Navigation Destinations

- Back → /setup/connect
- Start First Backup (valid) → /setup/progress
- Upgrade link → /pricing or upgrade modal
- Contact Support / Help Center → /help
