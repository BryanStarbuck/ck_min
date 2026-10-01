dark_mode = false

# DESIGN MODE: LIGHT MODE
> This file specifies a **Light Mode** design.
> The UX designer who implements this file must apply a light mode visual style.
> Light mode uses a white background (#FFFFFF) with dark text (#0F1419 / #536471).
> Do NOT use dark mode colors when implementing these requirements.

---

# Product Requirements — Backup Viewer (Light Mode)
# Page: backup_viewer | URL: /view/:platform/:handle

---

## Page Purpose

Browse and search backed-up posts, followers, and following for a specific connected account.

---

## Navigation Requirements

- **Standalone backup web app — NO JFKSocial left sidebar.**
- Full authenticated top nav.
- This page has its **own 240px utility left sidebar** (tabs + filters + actions).
- **No right sidebar.**
- Mobile: back button + horizontal tabs + fixed bottom tab bar ("View" active).

---

## Primary CTAs

- **"Apply"** — filled blue in sidebar (triggers filter)
- **"Export Selected"** — ghost (enabled when ≥1 selected)

---

## Required Layout

### 1. Full Authenticated Top Nav
### 2. Breadcrumb
- "Dashboard > View > @username" — links in blue, "@username" plain
### 3. Account Header Bar
- Platform icon + handle + platform + post count + last synced + "Sync Now" ghost right

### 4. Two-Column Layout (desktop)

**Left sidebar (240px):**

Tab Group (stacked, 3 tabs):
- "Posts" | "Followers" | "Following"
- Active: blue bg, white text; Inactive: #F7F9F9 bg, secondary text

Filters (Posts tab):
- Search input ("Search posts..."), Date From, Date To, Sort ("Newest ▾"), Apply button

Filters (Followers/Following tab):
- Search by name/handle, Sort (Newest Added / Alpha / Most Followers)

Actions:
- Select All checkbox
- "Export Selected" ghost pill (disabled until ≥1 selected)

**Right content (infinite scroll):**

Posts Tab:
- Post cards: handle + date/time + body (4 lines max, expand) + hashtags/mentions in blue + optional media thumbnail + engagement stats (💬 🔁 ❤️) + "View Original" + selection checkbox
- Hover-visible action row
- "Deleted on source platform" orange badge on deleted posts

Followers/Following Tab:
- User cards: avatar (48px) + name + handle + bio snippet + follower count

### 5. No Right Sidebar

---

## Search Functionality

- Full-text search, debounced 500ms
- Highlight matched text (yellow tint)
- Show results count: "142 posts match"
- No-results state + "Clear Filters" button

---

## Empty States

- No posts, no followers, search no results, date range no results, failed to load (all with helpful action links)

---

## Mobile Layout

- Top bar: "← Dashboard" blue + "@username" + [⋮]
- Account summary card (condensed)
- Horizontal tab bar (underline style)
- Full-width search + Filters pill + Sort toggle
- Filter bottom sheet (60% screen, slide up)
- Selection mode: bottom action bar
- Fixed bottom tab bar (4 tabs)

---

## Navigation Destinations

- Back → /dashboard
- "View Original" → external platform (new tab)
- "Export Selected" → /export
- Tab switches → same URL, content updates
