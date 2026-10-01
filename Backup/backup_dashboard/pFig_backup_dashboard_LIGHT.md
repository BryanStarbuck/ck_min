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

# Figma Make Prompts — Backup Dashboard (Light Mode)
# Page: backup_dashboard | URL: /dashboard

> **Navigation Note:** Standalone backup web app — NO JFKSocial left sidebar.
> Full authenticated top nav with Dashboard, Export, Settings links.
> Mobile has fixed bottom tab bar (4 tabs).

---

## DESIGN TOKEN REFERENCE

### Colors (Light Mode)
* Page bg:              #FFFFFF
* Card bg:              #FFFFFF
* Hover surface:        #F7F9F9
* Border subtle:        #EFF3F4
* Border prominent:     #CFD9DE
* Primary text:         #0F1419
* Secondary text:       #536471
* Muted text:           #8B98A5
* Brand blue:           #1D9BF0
* Success green:        #00BA7C
* Success tint:         #E8F9F2
* Danger red:           #F4212E
* Danger tint:          #FFF5F5
* Warning yellow:       #FFD400
* Warning tint:         #FFFCE0
* Warning orange:       #FF7A00
* Orange tint:          #FFF5EC
* Syncing blue tint:    #EBF5FF

---

## PROMPT 1 — Full Authenticated Top Navigation (Light)

**Container:** full-width, height 64px, bg #FFFFFF, border-bottom 1px #EFF3F4

**Left:** Shield icon + "Backup Posts" 17px/700/#0F1419

**Center Nav:**
- "Dashboard" (active) | "Export" | "Settings"
- 15px/500/#0F1419 (active) / #536471 (inactive)
- Active: 2px underline #1D9BF0

**Right:** "Account ▾" 15px/500/#536471 + "Logout" 15px/400/#536471, gap 20px

**Mobile:**
- Hamburger left, Logo center, Account ▾ right
- Bottom tab bar: bg #FFFFFF, border-top 1px #EFF3F4, height 56px
- Active: #1D9BF0 | Inactive: #536471

---

## PROMPT 2 — Storage Warning Banner (Conditional, Light)

Shown when storage > 80%.

**Container:** full-width, bg #FFFCE0, border-bottom 1px #FFD400, padding 12px 24px

**Content:** "⚠ Storage 85% full (8.5 GB of 10 GB)" 14px/600/#0F1419 + "Upgrade Plan" #1D9BF0 link + "Manage Storage" ghost pill

---

## PROMPT 3 — Page Title

**Container:** max-width 1000px, centered, margin 32px auto 24px

- "Your Backups" — 23px/700/#0F1419

---

## PROMPT 4 — Backup Status Panel (Light)

**Card:** bg #FFFFFF, border 1px #EFF3F4, radius 24px, padding 24px, max-width 1000px, centered

**Status row:**
- Status dot 12px #00BA7C + "All Systems Operational" 15px/700/#0F1419 + "Last backup: 2 hours ago" 13px/400/#536471

**Sub-row:** "Next auto-sync in: 22 hours" 13px/400/#536471

**"Sync All Now":** filled blue pill, bg #1D9BF0, text #FFFFFF, height 40px, 15px/700, margin-top 16px

---

## PROMPT 5 — Connected Accounts Section (Light)

**Container:** max-width 1000px, centered, margin-top 24px

**Section label:** "Connected Accounts" 15px/700/#0F1419

**2-column grid**, gap 20px

---

**Account Card:**
- bg #FFFFFF, border 1px #EFF3F4, radius 24px, padding 24px

**Platform header row:**
- Platform icon 32px circle (black bg, white X) + "@username" 15px/700/#0F1419 + "Twitter/X" 13px/400/#536471
- Badge: "✓ Backup Complete" — bg #E8F9F2, text #00BA7C, 9999px, 11px/700

**Stats:**
- "2,847 posts backed up" 14px/600/#0F1419
- Coverage bar: 95% fill #00BA7C, track #EFF3F4, height 8px, radius 9999px
- "Posts from Jan 2020 – Present" 12px/400/#8B98A5
- "1,204 followers" | "892 following" 13px/400/#536471
- "Last synced: 2 hours ago" 12px/400/#8B98A5

**Action row:**
- "Sync Now" ghost pill: border #1D9BF0, text #1D9BF0, height 36px, 13px/700
- "View" ghost pill: border #CFD9DE, text #536471, height 36px
- [⋮] 24px #536471, hover bg #F7F9F9

---

**Add Another Account Card:**
- Border: 2px dashed #CFD9DE, radius 24px, padding 24px
- Flex column, centered content
- [+] 48px circle bg #EFF3F4, "+" #536471
- "Add Another Account" 15px/700/#0F1419
- "Connect additional social media accounts" 13px/400/#536471
- "Add Account" filled blue pill, height 40px

---

## PROMPT 6 — Recent Activity (Light)

**Container:** max-width 1000px, centered, margin-top 24px

**Section heading:** "Recent Activity" 15px/700/#0F1419

**Card:** bg #FFFFFF, border 1px #EFF3F4, radius 24px, padding 24px

**5 activity rows** (divider 1px #EFF3F4):
- Icon 20px: ✓ #00BA7C | ⚠ #FFD400 | ✗ #F4212E
- Main 14px/600/#0F1419 + sub 13px/400/#536471 + timestamp 12px/#8B98A5

**"View All"** — ghost pill, border #EFF3F4, text #536471, height 36px, centered, margin-top 16px

---

## PROMPT 7 — Account Card State Variants (Light)

**Complete:** badge bg #E8F9F2 text #00BA7C, border #EFF3F4, bar #00BA7C
**Syncing:** badge bg #EBF5FF text #1D9BF0, semi-transparent overlay
**Error:** badge bg #FFF5F5 text #F4212E, border #F4212E, "View Error →" #F4212E
**Disconnected:** badge bg #FFF5EC text #FF7A00, "Reconnect" ghost orange pill

---

## PROMPT 8 — More Menu (⋮) Dropdown (Light)

**Card:** bg #FFFFFF, border 1px #EFF3F4, radius 16px, box-shadow 0 4px 12px rgba(15,20,25,0.15), width 180px

**Items:** 14px/400/#0F1419, height 36px, hover bg #F7F9F9
- "Edit Settings" | "Export Data" | "View Errors" | divider | "Disconnect Account" #F4212E | "Remove Account" #F4212E 700

---

## PROMPT 9 — Empty State (Light)

**Container:** max-width 480px, centered, text-align center, padding 60px 24px

- Illustration: 200px circle bg #EFF3F4
- "Connect your first social media account to start backing up your posts." 20px/700/#0F1419, margin-top 24px
- "Connect Account" filled blue pill, height 52px, margin-top 20px

---

## COMPONENT VARIANTS

### 1. Account Card — Default (Light)
- bg #FFFFFF, border 1px #EFF3F4, radius 24px

### 2. Status Dot
- 12px: green #00BA7C / yellow #FFD400 / red #F4212E / gray #8B98A5

### 3. Coverage Bar (Light)
- Track #EFF3F4, fill #00BA7C, height 8px

### 4. Badge — Backup Complete
- bg #E8F9F2, text #00BA7C, 11px/700, 9999px

### 5. Badge — Syncing
- bg #EBF5FF, text #1D9BF0, spinning dot

### 6. Badge — Error
- bg #FFF5F5, text #F4212E, 11px/700

### 7. Badge — Disconnected
- bg #FFF5EC, text #FF7A00, 11px/700

### 8. More Menu (⋮, Light)
- bg #FFFFFF, border #EFF3F4, radius 16px, shadow

### 9. Add Account Card (Dashed, Light)
- 2px dashed #CFD9DE, radius 24px

### 10. Bottom Tab Bar (Mobile, Light)
- bg #FFFFFF, border-top 1px #EFF3F4, height 56px
- Active: #1D9BF0 | Inactive: #536471
