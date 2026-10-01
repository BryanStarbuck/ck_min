dark_mode = true

# DESIGN MODE: DARK MODE
> This file specifies a **Dark Mode** design.
> The UX designer who implements this file must apply a dark mode visual style.
> Dark mode uses a dark background (#15202B) with light text (#FFFFFF / #8B98A5).
> Do NOT use light mode colors when implementing these requirements.

---

# Product Requirements — Setup: Backup Progress (Dark Mode)
# Page: backup_setup_progress | URL: /setup/progress

---

## Page Purpose

Step 3 (final step) of the 3-step setup wizard. Shows real-time progress of the first backup. Displays overall progress percentage, per-category progress bars, estimated time remaining, and a reassurance panel. Transitions to a completion success state when done.

---

## Navigation Requirements

- **Standalone backup web app — NO JFKSocial left sidebar.**
- Minimal authenticated top nav only.
- Wizard progress stepper: Steps 1 and 2 completed (checkmarks), Step 3 active.

---

## Primary CTA

- In-progress state: **"Run in Background"** (ghost) + **"Cancel"** (danger ghost)
- Completion state: **"Go to Dashboard"** — filled blue pill, height 52px, 17px/700

---

## Required Sections (In-Progress State)

### 1. Minimal Authenticated Header

### 2. Setup Progress Stepper
- Step 1: completed (checkmark)
- Step 2: completed (checkmark)
- Step 3: active ("Backup" bold, filled circle)
- Both connector lines filled blue (all steps at or past active)

### 3. Page Header
- Title (exact): "Backing up your account..."
- Account identifier row: platform icon + "@username" + "(Twitter/X)"

### 4. Overall Progress Block
- Large progress bar (height 16px), fill animated as % increases
- Percentage label: shown numerically (e.g., "62%")
- Estimated time: "Estimated time remaining: 3 minutes"
- Updates via WebSocket every 2s (desktop) / 3s (mobile)

### 5. Category Progress Card
- One card containing 4 category rows
- Each row: status icon + category name + count "X of Y" + percentage + per-category progress bar

**Categories and in-progress example state:**
- Posts: in-progress spinner → "2,104 of 2,847" / 73%
- Followers: in-progress spinner → "847 of 1,204" / 70%
- Following: waiting → "0 of 892" / 0% / "(waiting...)"
- Media: waiting → "0 of 1,523" / 0% / "(waiting...)"

**Status icons:**
- Completed: green checkmark circle (#00BA7C)
- In-progress: animated spinning circle (#1D9BF0)
- Waiting: hourglass/pause circle (muted gray)

### 6. Action Row
- "Run in Background" — ghost pill (navigates to /dashboard, toast: "Backup running. We'll email you when done.")
- "Cancel" — danger ghost pill (red border + text; opens confirmation before canceling)

### 7. "What's Happening" Reassurance Panel
- Title (exact): "What's Happening"
- Body para 1 (exact): "Your posts are being securely backed up to your account. This process may take several minutes depending on how much content you have."
- Body para 2 (exact): "You can safely close this page and we'll email you when it's done."
- 3 assurance rows with green checkmarks:
  - "Your data is encrypted during transmission"
  - "Rate limits are automatically respected"
  - "Progress will resume if interrupted"

---

## Completion State (Replaces Progress Content)

Triggered when backup reaches 100%.

### Completion Content (centered):
- Large animated success circle (80px, green #00BA7C, scale-in animation)
- Headline (exact): "All done!"
- Subhead (exact): "Your backup is complete and secure."
- 4 result rows with green checkmarks:
  - "2,847 posts backed up"
  - "1,204 followers saved"
  - "892 following accounts preserved"
  - "1,523 media files downloaded"
- Next backup notice (exact): "Your next backup is scheduled for tomorrow at 3:00 PM."
- CTA: "Go to Dashboard" — filled blue pill, height 52px
- Auto-redirect after 5s with countdown: "Redirecting in 5s..."

---

## Error States

### Rate Limited
- Yellow banner above category card
- "⚠ Rate limited. Waiting 15 minutes, then resuming automatically..."
- Countdown timer: "Retrying in 14:32..."

### Network Error
- Amber/orange banner: "Connection lost. Retrying..." + spinner

### Extension Disconnected
- Yellow banner: "Chrome extension disconnected. Please keep the extension running."

### Fatal Error
- Red banner + error message text
- Action buttons: "Retry" (filled blue) + "Contact Support" (ghost)

---

## Mobile-Specific Requirements

- Progress stepper: dots, all 3 active/complete
- Page header: "Backing up your account..." 20px/700 left-aligned
- Overall progress bar: full-width, 12px height (reduced from 16px)
- Action buttons: stacked full-width ("Run in Background" first)
- "What's Happening" panel: condensed — shorter body, 2 assurance items
- WebSocket updates every 3s (battery optimization)

---

## Navigation Destinations

- "Run in Background" → toast → /dashboard
- "Cancel" (confirmed) → /setup/options or /dashboard
- "Go to Dashboard" → /dashboard
- Contact Support → /help
