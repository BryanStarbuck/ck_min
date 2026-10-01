dark_mode = false

# DESIGN MODE: LIGHT MODE
> This file specifies a **Light Mode** design.
> The UX designer who implements this file must apply a light mode visual style.
> Light mode uses a white background (#FFFFFF) with dark text (#0F1419 / #536471).
> Do NOT use dark mode colors when implementing these requirements.

---

# Product Requirements — Backup Dashboard (Light Mode)
# Page: backup_dashboard | URL: /dashboard

---

## Page Purpose

Main hub for Backup Posts. Authenticated users land here after setup or login. Shows system status, connected account cards, and recent activity.

---

## Navigation Requirements

- **Standalone backup web app — NO JFKSocial left sidebar.**
- Full authenticated top nav: logo + "Dashboard" (active) | "Export" | "Settings" + Account dropdown + Logout.
- Mobile: fixed bottom tab bar (Dashboard / View / Export / Settings).

---

## Primary CTA

- "Sync All Now" — filled blue pill, height 40px, in the status panel
- Account card: "Sync Now" (ghost) + "View" (ghost)
- Empty state: "Connect Account" (filled blue, 52px)

---

## Required Sections

### 1. Full Authenticated Top Navigation
- Logo + nav links (Dashboard active) + Account + Logout
- Mobile: bottom tab bar (4 tabs, active #1D9BF0)

### 2. Storage Warning Banner (Conditional)
- Shown when >80% full: yellow warning stripe
- "Storage 85% full" + upgrade link + manage storage button

### 3. Page Title
- "Your Backups" — 23px/700

### 4. Backup Status Panel
- Status dot (green/yellow/red/gray) + status label + last backup time
- "Next auto-sync in: 22 hours"
- "Sync All Now" CTA

### 5. Connected Accounts Section
- "Connected Accounts" label
- 2-column desktop grid: account card(s) + "Add Another Account" dashed card

**Account Card:**
- Platform icon, handle, platform name, status badge
- Stats: post count, coverage bar (green fill), date range, followers/following, last synced
- Actions: "Sync Now" (ghost blue border) + "View" (ghost) + [⋮] more menu

**Status Badges:**
- "✓ Backup Complete" (green tint)
- "Syncing..." (blue tint + spinner)
- "⚠ Sync Failed" (red tint + red card border)
- "Disconnected" (orange tint + "Reconnect" orange ghost button)

**Add Another Account Card:** dashed border, centered, "Add Account" blue CTA

### 6. Recent Activity Section
- 5 rows desktop / 3 mobile
- Icon (green/yellow/red) + main text + sub + timestamp
- "View All" ghost button

---

## Empty State

- Illustration + "Connect your first social media account to start backing up your posts."
- "Connect Account" filled blue pill

---

## Mobile Requirements

- Bottom tab bar fixed
- Swipe left on card: action buttons
- Pull-to-refresh triggers sync check
- 3 activity rows

---

## More Menu Contents

- Edit Settings | Export Data | View Errors | [divider] | Disconnect Account (red) | Remove Account (red bold)

---

## Navigation Destinations

- "View" → /view/twitter/username
- "Add Account" → /setup/connect
- "View All" → /activity
- Export → /export | Settings → /settings
