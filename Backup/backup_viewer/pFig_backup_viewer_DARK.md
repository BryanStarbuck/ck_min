dark_mode = true

# DESIGN MODE: DARK MODE
> This file specifies a **Dark Mode** design.
> Every color, background, border, and text element MUST use the dark mode
> color palette listed here. Do NOT use light mode values anywhere in this file.
>
> Dark Mode Color Palette:
>   Page background:       #15202B
>   Card backgrounds:      #1E2732
>   Hover / elevated:      #253341
>   Borders:               #2F3336
>   Primary text:          #FFFFFF
>   Secondary text:        #8B98A5
>   Accent blue:           #1D9BF0
>   Admin sidebar bg:      #15202B
>   Sidebar border:        #2F3336

---

# Figma Make Prompts — Backup Viewer (Dark Mode)
# Page: backup_viewer | URL: /view/:platform/:handle

> **Navigation Note:** Standalone backup web app — NO JFKSocial left sidebar.
> Full authenticated top nav (same as dashboard). This page has its OWN left sidebar
> (240px, utility filters/tabs) — this is a content sidebar, NOT a navigation sidebar.
> No right sidebar — content-utility flow.

---

## DESIGN TOKEN REFERENCE

### Colors (Dark Mode)
* Page bg:              #15202B
* Card bg:              #1E2732
* Sidebar bg:           #1E2732
* Hover surface:        #253341
* Borders:              #2F3336
* Primary text:         #FFFFFF
* Secondary text:       #8B98A5
* Muted text:           #8B98A5
* Brand blue:           #1D9BF0
* Active tab bg:        #1D9BF0
* Active tab text:      #FFFFFF
* Inactive tab bg:      #1E2732
* Hashtag/mention:      #1D9BF0
* Deleted badge bg:     #1A1000
* Deleted badge text:   #FF7A00
* Search highlight:     rgba(255,212,0,0.25)
* Success green:        #00BA7C

### Typography
* Breadcrumb:       13px / 400 / #8B98A5
* Breadcrumb link:  13px / 400 / #1D9BF0
* Account header:   17px / 700 / #FFFFFF
* Tab text:         15px / 600 / #FFFFFF (active) / #8B98A5 (inactive)
* Filter label:     13px / 700 / #8B98A5 uppercase
* Search input:     13px / 400
* Post date:        13px / 400 / #8B98A5
* Post time:        13px / 400 / #8B98A5
* Post body:        15px / 400 / #FFFFFF
* Engagement:       13px / 400 / #8B98A5
* Card actions:     12px / 700 / #1D9BF0

---

## PROMPT 1 — Full Authenticated Top Navigation

Same as backup_dashboard. "View" tab is active in mobile bottom tab bar.

**Top nav:** bg #15202B, border-bottom 1px #2F3336, height 64px
- Logo + "Dashboard" | "Export" | "Settings" (no active state here — breadcrumb shows context)
- "Account ▾" + "Logout" right

---

## PROMPT 2 — Breadcrumb

**Container:** max-width 1280px, centered, padding 16px 24px 0

- "Dashboard > View > @username"
- 13px / 400 / #8B98A5
- "Dashboard" link: #1D9BF0, hover underline
- "View" link: #1D9BF0, hover underline
- "@username": plain #8B98A5 (not a link)
- Separator ">": 13px / #8B98A5, margin 0 6px

---

## PROMPT 3 — Account Header Bar

**Container:** max-width 1280px, centered, padding 12px 24px

**Card:** bg #1E2732, border 1px #2F3336, radius 24px, padding 20px 24px

**Row** (flex, align-items center, gap 12px):
- Platform icon 32px (black circle, white X)
- "@username" 17px/700/#FFFFFF
- "Twitter/X" 13px/400/#8B98A5
- "2,847 posts backed up" 13px/400/#8B98A5
- "Last synced: 2 hours ago" 12px/#8B98A5
- "Sync Now" — ghost pill, border 1px #1D9BF0, text #1D9BF0, height 36px, 13px/700, right-aligned (margin-left auto)

---

## PROMPT 4 — 2-Column Content Layout

Below the account header: 2-column layout.

**Left sidebar:** 240px fixed-width, no explicit bg (inherits page), padding-right 16px
**Right content:** flex-grow, overflow-y auto

**Container:** max-width 1280px, centered, padding 20px 24px
**Layout:** flex, gap 24px, align-items flex-start

---

## PROMPT 5 — Left Sidebar: Tabs

**Tab group container:**
- Border: 1px #2F3336, radius 16px, overflow hidden
- Width: 100%

**3 tab items (stacked):**
- "Posts" (active) | "Followers" | "Following"
- Height: 44px, 15px/600, text-align center
- Active tab: bg #1D9BF0, text #FFFFFF
- Inactive tab: bg #1E2732, text #8B98A5
- Inactive hover: bg #253341
- Divider 1px #2F3336 between tabs

---

## PROMPT 6 — Left Sidebar: Filters (Posts Tab)

Below the tab group.

**"FILTERS" label:** 11px/700/#8B98A5 uppercase, margin 16px 0 8px

**Search input:**
- Full-width, height 40px, bg #15202B, border 1px #2F3336, radius 12px, padding 0 12px
- Search icon 16px #8B98A5 left, placeholder "Search posts..." 13px/400/#8B98A5
- Focus: border-color #1D9BF0

**"Date Range:" label:** 13px/700/#8B98A5, margin-top 12px

**Date inputs (2):**
- Full-width, height 40px, bg #15202B, border 1px #2F3336, radius 12px, padding 0 12px
- Text #8B98A5 placeholder "From date" / "To date"
- Gap 8px between

**"Sort by:" label:** 13px/700/#8B98A5, margin-top 12px

**Sort dropdown:**
- Full-width, height 40px, bg #15202B, border 1px #2F3336, radius 12px, padding 0 12px
- "Newest ▾" 13px/400/#FFFFFF
- Options: Newest, Oldest, Most Likes, Most Retweets

**"Apply" button:**
- Filled blue pill, full-width, height 40px, 15px/700/#FFFFFF, bg #1D9BF0, margin-top 8px

---

## PROMPT 7 — Left Sidebar: Actions Section

**"ACTIONS" label:** 11px/700/#8B98A5 uppercase, margin-top 16px

**Select All row:**
- Checkbox 16px (#1D9BF0 when checked) + "Select All" 14px/500/#FFFFFF, gap 8px

**"Export Selected" button:**
- Ghost pill, full-width, height 40px, 14px/700/#1D9BF0, border 1px #1D9BF0
- Disabled state: text #8B98A5, border #2F3336
- When selection ≥1: "Export Selected (42 posts)"

---

## PROMPT 8 — Right Content: Post Cards (Posts Tab)

Infinite scroll list of post cards in the right content area.

**Post card:**
- bg #1E2732, border 1px #2F3336, radius 16px, padding 16px 20px, margin-bottom 12px

**Row 1 (flex, align-items center, gap 6px):**
- "@username" 14px/700/#FFFFFF
- "·" separator 13px/#8B98A5
- "Jan 15, 2026" 13px/400/#8B98A5
- "3:45 PM" 13px/400/#8B98A5
- Checkbox 16px right-aligned (ml auto), hover-visible only at rest

**Post body:**
- 15px/400/#FFFFFF, margin-top 8px, line-height 1.5
- Max 4 lines with "Show more" expand link #1D9BF0
- Hashtags: #1D9BF0 inline
- Mentions: #1D9BF0 inline
- (Display only — not interactive links)

**"Deleted on source platform" badge (conditional):**
- bg #1A1000, text #FF7A00, 9999px, 11px/700, padding 3px 10px
- Shown when post no longer exists on source

**Media thumbnail (if present):**
- 80px × 80px rounded (radius 12px), object-fit cover
- Positioned right of text for images; below text for video

**Engagement stats row (margin-top 10px, flex, gap 16px):**
- 💬 reply count | 🔁 retweet count | ❤️ like count
- 13px/400/#8B98A5

**Action row (hover-visible, flex, gap 12px, margin-top 8px):**
- "View Original" — ghost pill, height 32px, 12px/700/#1D9BF0, border #1D9BF0
- Checkbox 16px #1D9BF0

**Loading state:**
- "⟳ Loading more..." centered, 14px/400/#8B98A5, 20px spinner

---

## PROMPT 9 — Follower/Following Tab Content

When "Followers" or "Following" tab active:

**Sidebar filters change to:**
- Search: "Search by name or handle..." placeholder
- Sort dropdown: "Newest Added ▾" options: Newest Added, Alpha A-Z, Z-A, Most Followers
- No date range

**Content area: user cards** (instead of post cards):
- Each: flex row, gap 12px, padding 12px 16px, border-bottom 1px #2F3336
- Avatar: 48px circle, bg #253341 (placeholder initials in #8B98A5)
- Info: name 14px/700/#FFFFFF + handle 13px/400/#8B98A5 + bio 13px/400/#8B98A5 1 line truncated
- Right: follower count 12px/400/#8B98A5

---

## PROMPT 10 — Search & Empty States

**Search active state:**
- Results count: "142 posts match" — 12px/400/#8B98A5, below search input
- Highlighted match text: bg rgba(255,212,0,0.25) on matched substrings

**No results (search):**
- Empty inbox icon (48px, #8B98A5 stroke)
- "No posts match your search. Try different keywords or clear filters." — 15px/400/#8B98A5, centered
- "Clear Filters" ghost pill button

**No results (date range):**
- "No posts in this date range. Try expanding your dates." + "Clear Filters"

**Posts tab empty:**
- "No posts backed up yet." + "Sync Now" or "Enable backup in Settings" link

**Failed to load:**
- "Unable to load posts. [Retry]" — 15px/400/#8B98A5

---

## PROMPT 11 — Mobile Layout

**Top bar:** "← Dashboard" (#1D9BF0 with back arrow) left + "@username" center + [⋮] right, height 56px

**Account summary card:** full-width, padding 16px 20px, platform icon + "@username" + "2,847 posts • 2h ago" + "Sync Now"

**Tab bar:** "Posts" | "Followers" | "Following" — horizontal, full-width, underline style
- Active: 2px underline #1D9BF0, 15px/700/#FFFFFF
- Inactive: #8B98A5

**Search bar:** full-width below tabs, height 44px, search icon, placeholder "Search posts..."

**Filter/Sort row:** "⚙ Filters" ghost pill (opens bottom sheet) + "⬇ Sort: Newest" pill toggle

**Post cards:** full-width, condensed engagement (icons only at rest)

**Bottom sheet (filter):**
- Slides up from bottom, bg #1E2732, border-top 1px #2F3336, height 60% screen
- Handle bar 32px × 4px #2F3336 centered at top
- Fields: Date From, Date To, Apply, Clear

**Selection mode (mobile):**
- Bottom action bar: bg #1E2732, border-top 1px #2F3336, height 56px
- "Cancel" ghost left | "Export Selected (X)" filled blue right

---

## COMPONENT VARIANTS

### 1. Post Card — Default (Dark)
- bg #1E2732, border 1px #2F3336, radius 16px

### 2. Post Card — Selected
- bg #1D2D3E, border 1px #1D9BF0

### 3. "Deleted on source" Badge
- bg #1A1000, text #FF7A00, 9999px, 11px/700

### 4. Media Thumbnail
- 80px × 80px, radius 12px, object-fit cover, bg #253341 placeholder

### 5. Tab — Active (Sidebar)
- bg #1D9BF0, text #FFFFFF, height 44px

### 6. Tab — Inactive (Sidebar)
- bg #1E2732, text #8B98A5, hover bg #253341

### 7. Search Highlight
- bg rgba(255,212,0,0.25) on matched text

### 8. User Card (Followers/Following)
- Flex row, padding 12px 16px, border-bottom 1px #2F3336
- Avatar 48px circle #253341

### 9. Filter Input (Dark)
- bg #15202B, border 1px #2F3336, radius 12px, text #FFFFFF

### 10. Bottom Sheet (Mobile, Dark)
- bg #1E2732, border-top 1px #2F3336, radius-top-left/right 24px
- Handle: 32×4px #2F3336, centered
