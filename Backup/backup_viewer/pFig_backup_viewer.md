pFig — backup_viewer
Figma Make Prompts: Backup Viewer
==================================

DESIGN TOKEN REFERENCE
=======================

Colors: page bg #FFFFFF | card bg #F7F9F9 | elevated #EFF3F4 |
border subtle #EFF3F4 | border prominent #CFD9DE | primary text #0F1419 |
secondary #536471 | muted #8B98A5 | brand blue #1D9BF0 (hover #1A8CD8) |
success #00BA7C | danger #F4212E | warning orange #FF7A00 | warning bg #FFF5EC |
search highlight #FFD400 at 30% opacity | blue tint #EBF5FF

Typography: page title handled via breadcrumb | nav 15px/500 | account header 17px/700 |
post body 15px/400 | post handle 14px/700 | timestamp 13px/400/#536471 |
engagement stats 13px/400/#8B98A5 | sidebar labels 11px/700/#8B98A5 uppercase |
tab labels 15px/600

Spacing: sidebar width 240px | content flex-grow | card padding 16px–24px | gap 12px

Radii: page cards 24px | post cards 16px | user cards 0 (list rows) | inputs 12px |
action pills 9999px

Breakpoints: desktop >=1024px | mobile <640px


====================================================================
PROMPT 1 — Navigation Bar, Breadcrumb, and Account Header
====================================================================

Create the authenticated navigation bar, breadcrumb trail, and account header bar.
Reference Page_Backup_Viewer_Web_UI.md header sections.

Navigation bar: same authenticated nav as backup_dashboard.
* Dashboard (non-active link), Export (non-active), Settings (non-active).
  Note: "Dashboard" not active here — this is the viewer page, NOT the dashboard.
  All nav links: 15px/500/#536471, hover color #0F1419.
  No active underline on any link (viewer is not in main nav).

Breadcrumb (below nav):
* Full-width container, max-width 1000px centered, padding 16px 0 0.
* "Dashboard" link 13px/400/#1D9BF0 + " > " 13px/400/#8B98A5 + "View" link
  13px/400/#1D9BF0 + " > " + "@username" 13px/400/#536471 (plain, no link).
* Hover on breadcrumb links: underline.

Account Header Card (below breadcrumb, margin-top 12px):
* Full-width, max-width 1000px centered. White bg, border 1px #EFF3F4, radius 24px,
  padding 20px 24px.
* Single flex row, align-items center, gap 12px:
  * Platform icon: 32px circle, #000000 bg, white "X" letterform.
  * Handle: "@username" — 17px/700/#0F1419.
  * Platform: "Twitter/X" — 13px/400/#536471.
  * Separator dot "•" — 13px/#8B98A5.
  * Posts count: "2,847 posts backed up" — 13px/400/#536471.
  * Separator dot "•".
  * Last synced: "Last synced: 2 hours ago" — 12px/400/#8B98A5.
  * "Sync Now" button (margin-left auto): ghost pill, height 36px, 13px/700/#1D9BF0,
    border 1px #1D9BF0.

Mobile account header:
* Icon + "@username" 15px/700 + "2,847 posts • 2h ago" 13px/400/#536471 on one line.
* "Sync Now" full-width below, 44px height.


====================================================================
PROMPT 2 — Two-Column Layout: Sidebar (Tabs, Filters, Actions)
====================================================================

Create the two-column layout shell with the left sidebar containing tabs, filters,
and actions. Reference the sidebar layout in Page_Backup_Viewer_Web_UI.md.

Two-column shell (desktop only):
* Max-width 1000px, centered, margin-top 20px. Display flex, gap 20px, align-items flex-start.
* Left sidebar: 240px wide, flex-shrink 0. Position sticky, top 80px.
  (Sidebar stays fixed while content scrolls.)
* Right content: flex-grow 1. Min-width 0 (prevents overflow).

Sidebar content:

Tab group (3 tabs):
* Container: border 1px #EFF3F4, radius 16px, overflow hidden.
* 3 stacked tabs, each 44px height, flex row align-items center padding 0 16px.
* Active tab (Posts): bg #1D9BF0, text #FFFFFF, 15px/700.
* Inactive tabs: bg #F7F9F9, text #0F1419, 15px/500.
  Hover: bg #EFF3F4.
* Tabs top to bottom: "Posts" (active) | "Followers" | "Following".
* Top radius on first tab, bottom radius on last tab.

Filters section (Posts tab active state):
* "FILTERS" — 11px/700/#8B98A5 uppercase, letter-spacing 0.08em, margin 16px 0 8px.
* Search input (full-width):
  Height 40px, border 1px #CFD9DE, radius 12px, padding 0 12px 0 36px.
  Search icon 16px #8B98A5 positioned left 12px, absolute. Placeholder "Search posts..."
  13px/400/#8B98A5. Focus: border #1D9BF0, shadow 0 0 0 3px #EBF5FF.
* "Date Range" label — 13px/700/#0F1419, margin-top 12px.
* "From" date input: full-width, height 40px, border 1px #CFD9DE, radius 12px,
  padding 0 12px, 13px/400/#0F1419. Calendar icon 16px #8B98A5 right.
* "To" date input: same style as From, margin-top 8px.
* "Sort by" label — 13px/700/#0F1419, margin-top 12px.
* Sort dropdown: full-width, height 40px, border 1px #CFD9DE, radius 12px,
  padding 0 12px. "Newest ▾" default. Chevron icon right. 13px/400/#0F1419.
* "Apply" button: full-width, filled blue pill, height 40px, 14px/700/#FFFFFF,
  #1D9BF0 bg, margin-top 12px.

Actions section:
* "ACTIONS" — 11px/700/#8B98A5 uppercase, margin-top 20px.
* "Select All" row: checkbox 16px + "Select All" label 14px/500/#0F1419, gap 8px,
  flex row align-items center, margin-top 8px.
* "Export Selected" button:
  Disabled state: ghost pill full-width, height 40px, border 1px #EFF3F4,
  text "Export Selected" 14px/400/#8B98A5. Cursor not-allowed.
  Enabled state (after selection): border 1px #1D9BF0, text "Export Selected (42 posts)"
  14px/700/#1D9BF0.

Mobile: no sidebar. Tabs become horizontal tab bar. Filters become bottom sheet.
See Prompt 5 for mobile layout.


====================================================================
PROMPT 3 — Post Cards (Content Area)
====================================================================

Create the post card component with all its variants. This is the main content shown
in the right column when the Posts tab is active. Reference the post card sections
in Page_Backup_Viewer_Web_UI.md.

Post Card (default, desktop):
* Card: white bg, border 1px #EFF3F4, radius 16px, padding 16px 20px, margin-bottom 12px.
* Row 1 (flex, align-items center, gap 8px):
  * "@username" 14px/700/#0F1419.
  * "·" separator 13px/#8B98A5.
  * Date: "Jan 15, 2026" 13px/400/#536471.
  * Time: "3:45 PM" 13px/400/#8B98A5.
  * Checkbox: 16px right-aligned (margin-left auto), border 2px #CFD9DE unchecked.
    Checked: #1D9BF0 bg, white checkmark.
* Post body text (margin-top 8px): 15px/400/#0F1419, line-height 1.5.
  Example: "This is my tweet about AI filmmaking! It's pretty cool. #ACT3ai"
  Hashtags and @mentions: inline color #1D9BF0 (display only, not links).
  Max 4 lines, overflow hidden. "Show more" in 13px/#1D9BF0 if truncated.
* Media thumbnail (conditional, margin-top 10px):
  Rectangular strip: full-width, max-height 160px, radius 12px, object-fit cover,
  bg #F7F9F9.
* Engagement stats row (margin-top 10px, flex, gap 16px, align-items center):
  💬 icon 14px + count "24" 13px/400/#8B98A5.
  🔁 icon + count "12".
  ❤️ icon + count "156".
  All gaps 16px.
* Action row (margin-top 8px, flex, gap 10px, align-items center):
  * "View Original" — ghost pill, height 32px, 12px/700/#1D9BF0, border 1px #1D9BF0,
    padding 0 14px. Opens external. Hover: #EBF5FF bg.
  * Spacer (flex-grow).
  (Action row fades in on card hover via opacity 0→1 transition 150ms.)

Post card hover (desktop): bg #FAFBFB (very subtle), box-shadow 0 2px 8px rgba(15,20,25,0.06).

"Deleted on source platform" badge variant:
* Orange pill badge positioned in row 1 after the time: #FFF5EC bg, #FF7A00 text,
  9999px, 11px/700, padding 2px 8px. "⚠ Deleted on source"

Post card selected state:
* Border: 2px solid #1D9BF0.
* Checkbox: checked, #1D9BF0 bg.
* Subtle bg: #F7FBFF.

Loading indicator (at bottom of list):
* Centered flex row: spinning circle 20px #1D9BF0 + "Loading more..." 14px/400/#536471,
  gap 8px, padding 24px.

Mobile post card:
* Full-width, padding 16px. Card radius 16px. Border 1px #EFF3F4.
* Row 1: "@username" 14px/700 + date/time 12px. Checkbox right.
* Body: 14px/400, 3 lines max.
* Engagement: icons only (no count labels). Gap 12px.
* "View Original": full-width ghost pill, 44px height, prominent.


====================================================================
PROMPT 4 — Follower / Following User Cards
====================================================================

Create the user card component shown when the Followers or Following tab is active.
Reference the follower/following tab content described in the spec.

Followers / Following tab sidebar state:
* Filters section changes to: Search input only ("Search by name or handle...").
* Sort dropdown: "Newest Added ▾" (options: Newest, Oldest, A–Z, Z–A, Most Followers).
* No date range fields.
* "Export Selected" remains.

User card (list row style, inside content area):
* Container: flex row, align-items center, gap 12px, padding 14px 0.
* Separator: 1px #EFF3F4 border-bottom.
* Avatar: 48px circle, 50% radius, #EFF3F4 bg. Placeholder initials 16px/700/#8B98A5.
* Info block (flex-grow):
  * Name: 14px/700/#0F1419.
  * Handle: "@handle" 13px/400/#536471.
  * Bio snippet: 13px/400/#8B98A5, 1 line, text-overflow ellipsis.
* Right: follower count "1.2K followers" 12px/400/#8B98A5. Checkbox 16px.

No separator on last item. Wrap all items in a card (white bg, border 1px #EFF3F4,
radius 24px, padding 0 24px).

Mobile user card: same structure, condensed. Bio hidden. Avatar 40px. Name 14px, handle 12px.


====================================================================
PROMPT 5 — Mobile Layout (Tabs, Search Bar, Filter Bottom Sheet)
====================================================================

Create the mobile version of the backup viewer. Reference Page_Backup_Viewer_Mobile_UI.md.

Mobile top bar:
* Height 56px, border-bottom 1px #EFF3F4.
* Left: "← Dashboard" — back arrow icon 20px + "Dashboard" text 15px/400/#1D9BF0.
  Tap target: 44x44px minimum.
* Center: "@username" — 16px/700/#0F1419.
* Right: [⋮] icon 24px, 44x44px tap target.

Mobile tab bar (horizontal, below account header):
* Full-width, height 44px, border-bottom 1px #EFF3F4.
* 3 tabs: "Posts" | "Followers" | "Following". Equal width. 15px/600.
* Active: text #0F1419, 2px underline #1D9BF0 at bottom.
* Inactive: text #536471.
* Swipe between tabs with gesture.

Mobile search + filter row (below tab bar):
* Height 44px, padding 8px 16px, flex row, gap 8px.
* Search input: flex-grow, height 36px, border 1px #CFD9DE, radius 9999px (pill shape),
  padding 0 12px 0 32px. Search icon 14px #8B98A5 left inside.
  Placeholder: "Search posts..." 13px/400/#8B98A5.
* "⚙ Filters" pill button: height 36px, ghost pill, border 1px #CFD9DE,
  13px/500/#536471, padding 0 12px. Settings gear icon 14px left.
* "⬇ Newest" pill button: height 36px, same style. Sort icon + "Newest" text.

Mobile post cards (full-width, stacked with 8px gap):
* Card padding 16px. Same structure as desktop but condensed.
* Engagement stats: icons only (no text labels). 💬 🔁 ❤️ row.
* "View Original" full-width, 44px height, prominent position.
* Bottom action bar when in selection mode:
  Fixed bottom bar (above tab bar), height 56px, white bg, border-top 1px #EFF3F4.
  "Cancel" ghost link left | "Export Selected (X)" filled blue pill right.

Filter bottom sheet (mobile):
* Slides up from bottom on "Filters" tap.
* Half-screen height. White bg, radius 20px top corners.
* Handle bar: 36px wide, 4px tall, #CFD9DE, centered at top, margin 12px auto.
* Title: "Filter Posts" 17px/700/#0F1419.
* "Date From" date input, "Date To" date input (full-width, native mobile pickers).
* Action row at bottom: "Clear" ghost left + "Apply Filters" filled blue right.
* Dismiss: swipe down or tap outside.

Bottom tab bar: same as backup_dashboard mobile, "View" tab active.


====================================================================
PROMPT 6 — Search Highlight, Empty States, and Error States
====================================================================

Create the search results highlight style, empty states, and error state variants.

Search result highlight:
* Matching text in post body: wrapped in highlight span.
  bg: rgba(255,212,0,0.3) (#FFD400 at 30% opacity). Radius 3px. No padding change.
  Example: "This is my tweet about [AI filmmaking]! [#ACT3ai]" — highlighted portions.
* Results count below search input: "142 posts match" — 12px/400/#536471.

Empty States (3 variants):

Variant 1 — No posts match search/filters:
* Centered block in content area. Margin-top 60px.
* Search icon 48px #8B98A5 (outlined, no fill).
* Title: "No posts match your search." 20px/700/#0F1419.
* Sub: "Try different keywords or clear filters." 15px/400/#536471.
* "Clear Filters" ghost pill, height 40px, margin-top 16px.

Variant 2 — No data in tab (e.g., followers not backed up):
* Inbox icon 48px #8B98A5.
* Title: "No followers backed up yet." 20px/700/#0F1419.
* Sub: "Enable follower backup in settings to start saving your follower list."
  15px/400/#536471.
* "Go to Settings" ghost pill, height 40px.

Variant 3 — Date range no results:
* Calendar icon 48px #8B98A5.
* Title: "No posts in this date range." 20px/700/#0F1419.
* Sub: "Try expanding your date range."
* "Clear Filters" ghost pill.

Error state:
* Alert triangle icon 48px #F4212E.
* Title: "Unable to load posts." 20px/700/#0F1419.
* Sub: "Please check your connection and try again."
* "Retry" filled blue pill, height 40px.

Mobile: same states, full-width, padding 0 20px. Icons 40px.


====================================================================
COMPONENT VARIANTS
====================================================================

Post Card
* variant=default: normal borders
* variant=selected: blue border, checked checkbox, light blue bg
* variant=deleted: orange badge "⚠ Deleted on source"
* variant=with-media: media thumbnail strip below body text
* variant=expanded: full text visible (no 4-line truncation)

Sidebar Tab
* variant=active (Posts): #1D9BF0 bg, white text
* variant=active (Followers): #1D9BF0 bg, white text
* variant=active (Following): #1D9BF0 bg, white text
* variant=inactive: #F7F9F9 bg, #0F1419 text, hover #EFF3F4

Filter Input
* Search input with icon, date inputs, sort dropdown
* state=default | state=focus (blue border + shadow) | state=filled

Export Selected Button
* state=disabled: gray border + text, cursor not-allowed
* state=enabled: blue border + text, shows count
* state=hover: #EBF5FF bg

User Card (Follower/Following row)
* Contains: avatar, name, handle, bio, follower count, checkbox
* Row separator: 1px #EFF3F4

Mobile Filter Bottom Sheet
* slide-up animation from bottom: translate-y(100%) to translate-y(0), 250ms ease
* backdrop: rgba(0,0,0,0.4) fade-in

Search Highlight Span
* bg rgba(255,212,0,0.3) | radius 3px | inline-displayed

Selection Mode Action Bar (mobile)
* Fixed position above tab bar
* "Cancel" left (ghost), "Export Selected (X)" right (filled blue)
* Slides up from bottom on first selection, slides down on cancel
