dark_mode = false

# DESIGN MODE: LIGHT MODE
> This file specifies a **Light Mode** design.
> The UX designer who implements this file must apply a light mode visual style.
> Light mode uses a white background (#FFFFFF) with dark text (#0F1419 / #536471).
> Do NOT use dark mode colors when implementing these requirements.

---

# Product Requirements — Setup: Backup Progress (Light Mode)
# Page: backup_setup_progress | URL: /setup/progress

---

## Page Purpose

Step 3 (final step) of the 3-step setup wizard. Shows real-time backup progress. Transitions to a success completion state when done.

---

## Navigation Requirements

- **Standalone backup web app — NO JFKSocial left sidebar.**
- Minimal authenticated top nav.
- Wizard stepper: Steps 1 and 2 completed (checkmarks), Step 3 active.

---

## Primary CTAs

- In-progress: "Run in Background" (ghost) + "Cancel" (danger ghost)
- Completion: "Go to Dashboard" (filled blue, height 52px)

---

## Required Sections (In-Progress)

### 1. Minimal Authenticated Header
### 2. Setup Progress Stepper (all steps complete/active, both connectors blue)
### 3. Page Header
- Title: "Backing up your account..."
- Account row: platform icon + "@username" + "(Twitter/X)"

### 4. Overall Progress Block
- Large progress bar (16px height), fill #1D9BF0, animated
- Percentage label (e.g., "62%")
- ETA: "Estimated time remaining: 3 minutes"

### 5. Category Progress Card
- 4 rows: Posts, Followers, Following, Media
- Each: status icon + name + count + % + small bar
- In-progress: spinner #1D9BF0; waiting: hourglass muted; completed: green check

### 6. Action Row
- "Run in Background" (ghost) + "Cancel" (danger ghost — red border, red text)

### 7. "What's Happening" Panel (card style, #F7F9F9 bg)
- Title: "What's Happening"
- Body: explanation + "you can close this page" note
- 3 assurance rows with green checkmarks

---

## Completion State

- Large 80px green circle with white checkmark (animated scale-in)
- Headline: "All done!"
- Subhead: "Your backup is complete and secure."
- 4 result rows with green checkmarks (exact counts)
- Next backup notice
- "Go to Dashboard" CTA (filled blue, 52px)
- "Redirecting in 5s..." countdown

---

## Error States

- Rate limited: yellow warning banner, countdown timer
- Network error: orange banner + spinner
- Extension disconnected: yellow banner
- Fatal error: red banner + Retry + Contact Support buttons

---

## Mobile Requirements

- 12px progress bar (thinner), stacked action buttons, condensed reassurance panel
- WebSocket update interval: 3s instead of 2s

---

## Navigation Destinations

- "Run in Background" → toast → /dashboard
- "Cancel" → /setup/options or /dashboard
- "Go to Dashboard" → /dashboard
- Help → /help
