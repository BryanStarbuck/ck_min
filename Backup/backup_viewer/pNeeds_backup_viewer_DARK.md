dark_mode = true

# DESIGN MODE: DARK MODE
> This file specifies a **Dark Mode** design.
> The UX designer who implements this file must apply a dark mode visual style.
> Dark mode uses a dark background (#15202B) with light text (#FFFFFF / #8B98A5).
> Do NOT use light mode colors when implementing these requirements.

---

# Product Requirements — Backup Viewer (Dark Mode)
# Page: backup_viewer | URL: /view/:platform/:handle

---

## Page Purpose

Browse and search backed-up posts, followers, and following for a specific connected account. Users can search, filter by date, sort, and batch-select posts for export.

---

## Navigation Requirements

- **Standalone backup web app — NO JFKSocial left sidebar.**
- Full authenticated top nav (same as dashboard).
- This page has its **own 240px utility left sidebar** (tabs + filters + actions) — not a navigation sidebar.
- **No right sidebar** — content flows through the right column.
- Mobile: top back button (← Dashboard), horizontal tab bar, fixed bottom tab bar (4 tabs with "View" active).

---

## Primary CTA

- **"Apply"** — filled blue pill in sidebar filters, triggers filtered content reload
- **"Export Selected"** — ghost pill (enabled when ≥1 post selected)

---

## Required Layout

### 1. Full Authenticated Top Navigation
- Same as dashboard; "View" active in mobile bottom tab bar

### 2. Breadcrumb
- "Dashboard > View > @username"
- "Dashboard" and "View" are blue links; "@username" is plain text

### 3. Account Header Bar
- Platform icon + "@username" + "Twitter/X" + post count + last synced time + "Sync Now" ghost button (right-aligned)

### 4. Two-Column Content Area

**Left sidebar (240px, desktop only):**

Tab Group (3 stacked pill-style tabs):
- "Posts" (default active) | "Followers" | "Following"
- Active tab: #1D9BF0 bg, white text
- Inactive: dark surface bg, muted text
- One tab active at a time

Filters Section (Posts tab — context-sensitive):
- Search input: "Search posts..." placeholder, 40px height
- Date Range: "From" and "To" date pickers
- Sort dropdown: "Newest ▾" (options: Newest, Oldest, Most Likes, Most Retweets)
- "Apply" button: filled blue, full-width, 40px height

Actions Section:
- "Select All" checkbox row
- "Export Selected" ghost pill (disabled until ≥1 selected; shows count when active)

**Right content (infinite scroll):**

Posts Tab:
- Post cards with: handle, date, time, body text (max 4 lines with "Show more"), hashtags/mentions in blue, optional media thumbnail, engagement stats (replies/retweets/likes), "View Original" action button + selection checkbox
- Hover-visible actions (hidden at rest to reduce noise)
- "Deleted on source platform" badge (orange) shown on deleted posts
- Loading state: spinner + "Loading more..."

Followers/Following Tab:
- Sidebar filters: search by name/handle, sort (Newest Added / Alpha A-Z / Z-A / Most Followers), no date range
- Content: user cards with avatar (48px circle), name, handle, bio snippet (1 line), follower count

### 5. No Right Sidebar

---

## Search Functionality

- Full-text search across post content (hashtags, mentions, body text)
- Debounced 500ms after keystroke
- Matching text highlighted (yellow tint)
- Results count shown below search input: "142 posts match"

---

## Empty States

- No posts: "No posts backed up yet." + "Sync Now" or "Enable backup in Settings"
- No followers: "No followers backed up. Enable follower backup in Settings."
- Search no results: "No posts match your search. Try different keywords or clear filters." + "Clear Filters" button
- Date range no results: "No posts in this date range. Try expanding your dates." + "Clear Filters"
- Failed to load: "Unable to load posts. [Retry]"

---

## Mobile Layout

- Top bar: "← Dashboard" (back, blue) + "@username" center + [⋮] right
- Account summary card (full-width, condensed)
- Horizontal tab bar (Posts / Followers / Following), underline style
- Full-width search bar below tabs
- "⚙ Filters" ghost pill + Sort toggle below search
- Post cards: full-width, condensed (engagement icons only at rest)
- Filter bottom sheet: slides up 60% screen height with Date From/To, Apply, Clear
- Selection mode: bottom action bar with Cancel + Export Selected
- Fixed bottom tab bar: Dashboard / View (active) / Export / Settings

---

## Navigation Destinations

- "← Dashboard" / breadcrumb → /dashboard
- "Sync Now" → stays on page, sync updates
- Tab switches: stay on URL, content updates
- "View Original" → external Twitter/X (new tab)
- "Export Selected" → /export (pre-selected items)
- Dashboard / Export / Settings tabs → respective pages
