backup_viewer — Page Spec
=========================

Page ID: backup_viewer
URL: /view/:platform/:handle
Portal: main_site (authenticated)
ASCII Sources: Page_Backup_Viewer_Web_UI.md, Page_Backup_Viewer_Mobile_UI.md


OVERVIEW
========

Browse and search backed-up posts, followers, and following for a specific connected
account. Uses a sidebar-left, content-right layout on desktop and a tabbed single-column
layout on mobile. Supports full-text search, date range filtering, sorting, and batch
selection for export.


PAGE LAYOUT — DESKTOP
=====================

1. Authenticated nav bar (same as dashboard: Dashboard, Export, Settings links).

2. Breadcrumb
   * "Dashboard > View > @username" — 13px/400/#536471.
   * "Dashboard" and "View" are links (#1D9BF0), "@username" is plain text.
   * Separator ">" 13px/#8B98A5.

3. Account header bar (full-width content area, below breadcrumb)
   * Card: white bg, border 1px #EFF3F4, radius 24px, padding 20px 24px.
   * Row: platform icon 32px + "@username" 17px/700 + "Twitter/X" 13px/400/#536471
     + "2,847 posts backed up" 13px/400/#536471 + "Last synced: 2 hours ago" 12px/#8B98A5
     + "Sync Now" ghost pill button right side.

4. Main content area — 2-column layout (below account header)
   * Left sidebar: 240px wide, fixed within scroll. Contains: tabs, filters, actions.
   * Right content: flex-grow. Infinite scroll list.

   LEFT SIDEBAR:

   Tab group (3 tabs, stacked pill-style):
   * Container: border 1px #EFF3F4, radius 16px, overflow hidden.
   * Tab items stacked. Active tab: #1D9BF0 bg, #FFFFFF text. Inactive: #F7F9F9 bg,
     #0F1419 text. Hover inactive: #EFF3F4 bg.
   * Tabs: "Posts" (default active) | "Followers" | "Following". 15px/600, height 44px.
   * Active indicator: filled blue bg on active tab.

   Filters section (context-sensitive, shown for Posts tab):
   * "FILTERS" label — 11px/700/#8B98A5 uppercase, margin 16px 0 8px.
   * Search input: full-width, height 40px, border 1px #CFD9DE, radius 12px, padding 0 12px.
     Search icon 16px #8B98A5 left, placeholder "Search posts..." 13px/400/#8B98A5.
   * "Date Range:" label — 13px/700/#0F1419.
   * From date picker: full-width, height 40px, border 1px #CFD9DE, radius 12px.
   * To date picker: same.
   * "Sort by:" label — 13px/700/#0F1419.
   * Sort dropdown: full-width, height 40px, border 1px #CFD9DE, radius 12px.
     Default: "Newest ▾". Options: Newest, Oldest, Most Likes, Most Retweets.
   * "Apply" — filled blue pill, height 40px, 15px/700, full-width, margin-top 8px.

   Actions section:
   * "ACTIONS" label — 11px/700/#8B98A5 uppercase, margin-top 16px.
   * "Select All" checkbox row: checkbox 16px + "Select All" 14px/500/#0F1419.
   * "Export Selected" button (enabled when ≥1 selected):
     Ghost pill, full-width, height 40px, 14px/700/#1D9BF0.
     Disabled: #8B98A5 text, border #EFF3F4.
     When enabled shows count: "Export Selected (42 posts)".

   RIGHT CONTENT (infinite scroll):

   Post cards (Posts tab, default view):
   * Each card: white bg, border 1px #EFF3F4, radius 16px, padding 16px 20px,
     margin-bottom 12px.
   * Row 1 (flex): "@username" 14px/700/#0F1419 + "·" + date "Jan 15, 2026" 13px/400/#536471
     + time "3:45 PM" 13px/400/#8B98A5. Checkbox 16px right-aligned.
   * Post body: 15px/400/#0F1419, margin-top 8px, line-height 1.5, max 4 lines (expand on click).
     Hashtags: #1D9BF0. Mentions: #1D9BF0. Display only (not interactive links).
   * "Deleted on source platform" badge (conditional): orange pill #FFF5EC bg, #FF7A00 text,
     9999px, 11px/700. Shown if post no longer exists.
   * Media thumbnail (if present): rounded 80px × 80px or wider strip, radius 12px,
     object-fit cover. Positioned right of text or below text if video.
   * Engagement stats row (margin-top 10px, flex, gap 16px):
     💬 reply count (13px/#8B98A5) | 🔁 retweet count | ❤️ like count.
   * Action row (margin-top 8px, flex, gap 12px):
     "View Original" — ghost pill 32px height, 12px/700/#1D9BF0, border #1D9BF0.
       Opens source platform in new tab.
     "Select" checkbox (16px, #1D9BF0) for batch actions.
     (On hover over card: action row becomes visible; hidden at rest to reduce noise.)

   Loading state: "⟳ Loading more..." — centered, 14px/400/#536471, spinner 20px.

5. No right sidebar on this page (content utility flow).


FOLLOWER / FOLLOWING TABS
==========================

When Followers or Following tab active, sidebar filters change to:
* Search input: "Search by name or handle..."
* Sort dropdown: "Newest Added ▾" (or Alpha A-Z, Z-A, Most Followers)
* No date range.

Content area shows user cards (instead of post cards):
* Each user card: flex row, gap 12px, padding 12px 16px, border-bottom 1px #EFF3F4.
* Avatar: 48px circle, #EFF3F4 bg (placeholder initials).
* Info block: name 14px/700/#0F1419, handle 13px/400/#536471, bio snippet 13px/400/#8B98A5
  1 line truncated.
* Right: follower count 12px/400/#8B98A5.


MOBILE LAYOUT
=============

* Top bar: "← Dashboard" (back arrow + text, #1D9BF0) left, "@username" center, [⋮] right.
  Height 56px.
* Account summary card: platform icon + "@username" + "2,847 posts • 2h ago" +
  "Sync Now" button. Full-width card, padding 16px 20px.
* Tab bar: "Posts" | "Followers" | "Following" — horizontal tab bar, full-width,
  underline style. Active: 2px underline #1D9BF0, 15px/700/#0F1419. Inactive: #536471.
* Search bar: full-width below tabs, height 44px, search icon, "Search posts..." placeholder.
* Filter/Sort row below search: "⚙ Filters" ghost pill (opens bottom sheet) +
  "⬇ Sort: Newest" pill toggle.
* Post cards: full-width stacked, padding 16px, radius 16px, border 1px #EFF3F4.
  Condensed: engagement stats use icons only (no counts visible at rest, tap to reveal).
* "View Original" button prominent (full-width). Checkbox inline to right of post.
* Infinite scroll: "Load more posts..." at bottom, pull-to-load.
* Bottom tab bar: same 4 tabs as dashboard (Dashboard / View / Export / Settings).
  "View" tab active.

Mobile filter bottom sheet:
* Slides up from bottom. Height 60% of screen. Handle bar at top.
* Contains: Date From, Date To, Apply, Clear filters buttons.
* Dismiss: swipe down or tap backdrop.

Mobile selection mode:
* First checkbox tap enters selection mode.
* Bottom action bar appears (56px, white, border-top #EFF3F4):
  "Cancel" ghost left | "Export Selected (X)" filled blue right.


SEARCH FUNCTIONALITY
====================

* Full-text search across post content (hashtags, mentions, body).
* Debounced 500ms after last keystroke.
* Matching text highlighted: bg #FFD400 at 30% opacity on matched substrings.
* Results count: "142 posts match" — 12px/400/#536471 below search input.
* No-results state: "No posts match your search. Try different keywords or clear filters."
  Centered, 15px/400/#536471. "Clear Filters" ghost button.

Date range no-results: "No posts in this date range. Try expanding your dates."
  Same centered style. "Clear Filters" ghost button.


ERROR / EMPTY STATES
====================

No posts (tab empty):
  Icon (empty inbox), "No posts backed up yet."
  "Sync Now" or "Enable backup in Settings" link.

No followers:
  "No followers backed up. Enable follower backup in Settings."
  Link to settings.

Failed to load:
  "Unable to load posts. [Retry]" — 15px/400, retry button.

Network error:
  "Connection lost. Please refresh the page." — 15px/400/#F4212E.


NAVIGATION
==========

"← Dashboard" (breadcrumb or back) -> /dashboard
Sync Now (header) -> stay on page, sync card updates.
Posts tab -> same URL, content area shows posts.
Followers tab -> same URL, content shows followers.
Following tab -> same URL, content shows following.
Apply filters -> content area reloads with filters applied.
View Original (post) -> external (Twitter/X) new tab.
Export Selected -> /export (pre-selected items).
Dashboard tab (mobile) -> /dashboard.
Export tab (mobile) -> /export.
Settings tab (mobile) -> /settings.
