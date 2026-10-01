dark_mode = true

# DESIGN MODE: DARK MODE
> This file specifies a **Dark Mode** design.
> The UX designer who implements this file must apply a dark mode visual style.
> Dark mode uses a dark background (#15202B) with light text (#FFFFFF / #8B98A5).
> Do NOT use light mode colors when implementing these requirements.

---

# Product Requirements — Backup Dashboard (Dark Mode)
# Page: backup_dashboard | URL: /dashboard

---

## Page Purpose

Main hub for Backup Posts. Authenticated users land here after setup or login. Shows system status, all connected account cards, and recent activity. Users can trigger syncs and navigate to detailed views.

---

## Navigation Requirements

- **Standalone backup web app — NO JFKSocial left sidebar.**
- Full authenticated top nav: logo left, "Dashboard" (active) | "Export" | "Settings" center, "Account ▾" + "Logout" right.
- Mobile: hamburger drawer + fixed bottom tab bar (Dashboard / View / Export / Settings).

---

## Primary CTA

- Page-level: **"Sync All Now"** — filled blue pill, height 40px, in the status panel
- Account card level: **"Sync Now"** (ghost pill) + **"View"** (ghost pill)
- Empty state: **"Connect Account"** — filled blue pill, height 52px

---

## Required Sections

### 1. Full Authenticated Top Navigation
- Logo + "Dashboard" (active link) | "Export" | "Settings" + Account dropdown + Logout
- Mobile: fixed bottom tab bar (4 tabs)

### 2. Storage Warning Banner (Conditional)
- Shown when storage > 80% full
- "⚠ Storage 85% full (8.5 GB of 10 GB)" + "Upgrade Plan" link + "Manage Storage" button
- Yellow warning color scheme

### 3. Page Title
- "Your Backups" — 23px/700

### 4. Backup Status Panel
- Status dot (colored by operational state) + status text + last backup time
- "Next auto-sync in: 22 hours"
- "Sync All Now" blue CTA

**Status dot states:**
- Operational: green (#00BA7C)
- Warning: yellow (#FFD400)
- Error: red (#F4212E)
- Never synced: gray (#8B98A5)

### 5. Connected Accounts Section
- "Connected Accounts" section label
- 2-column grid (desktop): account card(s) left + "Add Another Account" dashed card right

**Account Card (@username / Twitter/X):**
- Platform icon + handle + platform name + status badge
- Stats: posts count, coverage progress bar, coverage date range, followers/following counts, last synced
- Actions: "Sync Now" (ghost) + "View" (ghost) + [⋮] more menu

**Status Badge variants:**
- "✓ Backup Complete" (green)
- "Syncing..." with spinner (blue)
- "⚠ Sync Failed" (red) + border color change
- "Disconnected" (orange) + "Reconnect" replaces "Sync Now"
- "3 gaps detected" orange badge + "Deep Sync" button

**"Add Another Account" dashed card:**
- Dashed border, centered content, "Add Account" blue CTA
- Links to /setup/connect

### 6. Recent Activity Section
- "Recent Activity" heading
- 5 activity rows (desktop); 3 on mobile
- Each row: status icon (green/yellow/red) + main text + sub-details + timestamp
- "View All" ghost button at bottom
- Row data:
  1. "Full backup completed for @username" / "2,847 posts, 1,204 followers, 892 following" / "2 hours ago"
  2. "Media download completed" / "1,523 images and videos saved" / "2 hours ago"
  3. "Incremental sync completed" / "14 new posts backed up" / "1 day ago"
  4. "Account connected: @username" / "" / "3 days ago"
  5. "Chrome extension installed" / "" / "3 days ago"

---

## Empty State (No Accounts Connected)

Replace status panel + accounts section with centered block:
- Illustration placeholder (200px circle)
- "Connect your first social media account to start backing up your posts."
- "Connect Account" filled blue pill

---

## Mobile Requirements

- Top bar: hamburger + logo + "Account ▾"
- Status panel: condensed (2-line status + next sync)
- Account cards: full-width stacked
- Swipe left on card: reveals "Sync", "Export", "Disconnect" actions
- Pull-to-refresh triggers sync check
- Recent Activity: 3 items only; "View All" full-width ghost button
- Bottom tab bar: fixed, 4 tabs

---

## More Menu (⋮) Contents

- "Edit Settings" | "Export Data" | "View Errors" | divider | "Disconnect Account" (red) | "Remove Account" (red, bold)

---

## Navigation Destinations

- "View" (account card) → /view/twitter/username
- "Add Account" → /setup/connect
- "View All" (activity) → /activity
- "Export" (nav) → /export
- "Settings" (nav) → /settings
- "Logout" → /login
