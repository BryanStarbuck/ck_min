dark_mode = false

# DESIGN MODE: LIGHT MODE
> This file specifies a **Light Mode** design.
> Every color, background, border, and text element MUST use the light mode
> color palette listed here. Do NOT use dark mode values anywhere in this file.
>
> Light Mode Color Palette:
>   Page background:       #FFFFFF
>   Card backgrounds:      #F7F9F9
>   Elevated surfaces:     #EFF3F4
>   Borders (subtle):      #EFF3F4
>   Borders (prominent):   #CFD9DE
>   Primary text:          #0F1419
>   Secondary text:        #536471
>   Accent blue:           #1D9BF0

---

# Figma Make Prompts — Backup Viewer (Light Mode)
# Page: backup_viewer | URL: /view/:platform/:handle

> **Navigation Note:** Standalone backup web app — NO JFKSocial left sidebar.
> Full authenticated top nav. This page has its OWN 240px left sidebar (utility filters/tabs).
> No right sidebar — content-utility flow.

---

## DESIGN TOKEN REFERENCE

### Colors (Light Mode)
* Page bg:              #FFFFFF
* Card bg:              #FFFFFF
* Sidebar bg:           #FFFFFF
* Hover surface:        #F7F9F9
* Border subtle:        #EFF3F4
* Border prominent:     #CFD9DE
* Primary text:         #0F1419
* Secondary text:       #536471
* Muted text:           #8B98A5
* Brand blue:           #1D9BF0
* Active tab bg:        #1D9BF0
* Active tab text:      #FFFFFF
* Inactive tab bg:      #F7F9F9
* Hashtag/mention:      #1D9BF0
* Deleted badge bg:     #FFF5EC
* Deleted badge text:   #FF7A00
* Search highlight:     rgba(255,212,0,0.30)

---

## PROMPT 1 — Full Authenticated Top Navigation (Light)

**Top nav:** bg #FFFFFF, border-bottom 1px #EFF3F4, height 64px
- Logo + nav links + Account + Logout

---

## PROMPT 2 — Breadcrumb (Light)

**Container:** max-width 1280px, centered, padding 16px 24px 0

- "Dashboard > View > @username"
- 13px/400/#536471
- "Dashboard" + "View" links: #1D9BF0, hover underline
- "@username": #536471 plain
- ">" separator: #8B98A5

---

## PROMPT 3 — Account Header Bar (Light)

**Card:** bg #FFFFFF, border 1px #EFF3F4, radius 24px, padding 20px 24px, max-width 1280px centered

**Row (flex, align-items center, gap 12px):**
- Platform icon 32px (black circle/white X) + "@username" 17px/700/#0F1419 + "Twitter/X" 13px/400/#536471
- "2,847 posts backed up" 13px/400/#536471 + "Last synced: 2 hours ago" 12px/#8B98A5
- "Sync Now" ghost pill: border #1D9BF0, text #1D9BF0, height 36px, 13px/700, right (ml auto)

---

## PROMPT 4 — 2-Column Content Layout

**Container:** max-width 1280px, centered, padding 20px 24px
**Layout:** flex, gap 24px, align-items flex-start
**Left:** 240px fixed | **Right:** flex-grow

---

## PROMPT 5 — Left Sidebar: Tabs (Light)

**Tab group:**
- Border 1px #EFF3F4, radius 16px, overflow hidden

3 stacked tabs:
- "Posts" (active): bg #1D9BF0, text #FFFFFF, height 44px, 15px/600
- "Followers" (inactive): bg #F7F9F9, text #536471, hover bg #EFF3F4
- "Following" (inactive): same as Followers
- Divider 1px #EFF3F4 between tabs

---

## PROMPT 6 — Left Sidebar: Filters (Light)

**"FILTERS" label:** 11px/700/#8B98A5 uppercase

**Search input:**
- Full-width, height 40px, bg #F7F9F9, border 1px #CFD9DE, radius 12px
- Search icon #8B98A5, placeholder "Search posts..." 13px/#8B98A5
- Focus: border-color #1D9BF0

**Date Range labels + 2 date inputs:**
- bg #F7F9F9, border 1px #CFD9DE, radius 12px, height 40px, text #0F1419

**Sort dropdown:**
- "Newest ▾" bg #F7F9F9, border 1px #CFD9DE, radius 12px, height 40px

**"Apply":** filled blue pill, full-width, height 40px, bg #1D9BF0, text #FFFFFF, margin-top 8px

---

## PROMPT 7 — Left Sidebar: Actions (Light)

**"ACTIONS" label:** 11px/700/#8B98A5 uppercase, margin-top 16px

**Select All:** checkbox 16px + "Select All" 14px/500/#0F1419

**"Export Selected":**
- Ghost pill, full-width, height 40px, 14px/700/#1D9BF0, border 1px #1D9BF0
- Disabled: #8B98A5 text, #EFF3F4 border
- When ≥1 selected: "Export Selected (42 posts)"

---

## PROMPT 8 — Right Content: Post Cards (Light)

**Post card:**
- bg #FFFFFF, border 1px #EFF3F4, radius 16px, padding 16px 20px, margin-bottom 12px
- Hover: box-shadow 0 2px 8px rgba(15,20,25,0.06)

**Row 1:** "@username" 14px/700/#0F1419 + "·" + "Jan 15, 2026" 13px/400/#536471 + "3:45 PM" 13px/#8B98A5 + checkbox right

**Post body:** 15px/400/#0F1419, margin-top 8px, line-height 1.5, max 4 lines
- Hashtags/mentions: #1D9BF0

**"Deleted on source platform" badge:**
- bg #FFF5EC, text #FF7A00, 9999px, 11px/700

**Media thumbnail:** 80px × 80px, radius 12px, object-fit cover

**Engagement row:** 💬 🔁 ❤️ counts, 13px/400/#536471

**Action row (hover-visible):**
- "View Original" ghost pill, height 32px, 12px/700/#1D9BF0, border #1D9BF0
- Checkbox 16px #1D9BF0

**Loading:** "⟳ Loading more..." centered, 14px/400/#536471

---

## PROMPT 9 — Follower/Following Tab (Light)

**Sidebar:** Search "Search by name or handle...", Sort "Newest Added ▾", no date range, Apply button

**User cards:**
- Flex row, padding 12px 16px, border-bottom 1px #EFF3F4
- Avatar: 48px circle #EFF3F4 bg (placeholder initials #536471)
- Name 14px/700/#0F1419 + handle 13px/400/#536471 + bio 13px/400/#8B98A5 (truncated 1 line)
- Follower count 12px/#8B98A5 right

---

## PROMPT 10 — Search & Empty States (Light)

**Active search:** "142 posts match" 12px/400/#536471 below input
**Highlight:** bg rgba(255,212,0,0.30) on matched text

**No results:**
- Icon + "No posts match your search." 15px/400/#536471 centered + "Clear Filters" ghost button

**Date range empty:** "No posts in this date range. Try expanding your dates." + "Clear Filters"

**Posts tab empty:** "No posts backed up yet." + "Sync Now" link

**Failed to load:** "Unable to load posts. [Retry]" 15px/400/#536471

---

## PROMPT 11 — Mobile Layout (Light)

**Top bar:** "← Dashboard" #1D9BF0 (with back arrow) + "@username" center + [⋮] right, height 56px, bg #FFFFFF, border-bottom 1px #EFF3F4

**Account summary card:** bg #FFFFFF, border 1px #EFF3F4, full-width, radius 16px, padding 16px 20px
- Platform icon + "@username" + stats + "Sync Now"

**Tab bar:** full-width horizontal, underline style
- Active: 2px underline #1D9BF0, text #0F1419, 15px/700
- Inactive: text #536471

**Search:** full-width, bg #F7F9F9, border 1px #CFD9DE, height 44px

**Filter row:** "⚙ Filters" ghost pill + "⬇ Sort: Newest" pill toggle

**Bottom sheet:** bg #FFFFFF, border-top 1px #EFF3F4, radius 24px top-left/right
- Handle: 32×4px #EFF3F4

**Selection mode bar:** bg #FFFFFF, border-top 1px #EFF3F4, "Cancel" + "Export Selected" blue

---

## COMPONENT VARIANTS

### 1. Post Card — Default (Light)
- bg #FFFFFF, border 1px #EFF3F4, radius 16px
- Hover: box-shadow 0 2px 8px rgba(15,20,25,0.06)

### 2. Post Card — Selected
- bg #EBF5FF, border 1px #1D9BF0

### 3. "Deleted on source" Badge
- bg #FFF5EC, text #FF7A00, 9999px, 11px/700

### 4. Tab — Active
- bg #1D9BF0, text #FFFFFF, height 44px

### 5. Tab — Inactive
- bg #F7F9F9, text #536471, hover bg #EFF3F4

### 6. Search Highlight
- bg rgba(255,212,0,0.30)

### 7. User Card (Followers/Following, Light)
- Flex row, border-bottom 1px #EFF3F4
- Avatar 48px circle #EFF3F4

### 8. Filter Input (Light)
- bg #F7F9F9, border 1px #CFD9DE, radius 12px

### 9. Bottom Sheet (Mobile, Light)
- bg #FFFFFF, border-top 1px #EFF3F4, radius 24px top

### 10. "View Original" Button
- Ghost pill, height 32px, border #1D9BF0, text #1D9BF0, 12px/700
