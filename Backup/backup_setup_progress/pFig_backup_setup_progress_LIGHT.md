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

# Figma Make Prompts — Setup: Backup Progress (Light Mode)
# Page: backup_setup_progress | URL: /setup/progress

> **Navigation Note:** Standalone backup web app — NO JFKSocial left sidebar.
> Minimal authenticated top nav. Step 3 of the 3-step wizard.

---

## DESIGN TOKEN REFERENCE

### Colors (Light Mode)
* Page bg:              #FFFFFF
* Card bg:              #FFFFFF
* Info panel bg:        #F7F9F9
* Border subtle:        #EFF3F4
* Border prominent:     #CFD9DE
* Primary text:         #0F1419
* Secondary text:       #536471
* Muted text:           #8B98A5
* Brand blue:           #1D9BF0
* Success green:        #00BA7C
* Danger red:           #F4212E
* Warning yellow:       #FFD400
* Warning bg tint:      #FFFCE0
* Network error:        #FF7A00
* Progress bar track:   #EFF3F4

---

## PROMPT 1 — Minimal Authenticated Header

**Container:** full-width, height 64px, bg #FFFFFF, border-bottom 1px #EFF3F4

**Left:** Shield icon + "Backup Posts" 17px/700/#0F1419
**Right:** "Account ▾" 15px/500/#536471 + "Logout" 15px/400/#536471
**Mobile:** Logo center, Account ▾ right, height 56px

---

## PROMPT 2 — Setup Progress Indicator (Step 3 Active)

**Step 1:** bg #1D9BF0, white checkmark, label "Connect" 13px/500/#536471
**Step 2:** bg #1D9BF0, white checkmark, label "Options" 13px/500/#536471
**Step 3 (ACTIVE):** bg #1D9BF0, "3" 13px/700/#FFFFFF, label "Backup" 13px/700/#0F1419

**Both connectors:** filled #1D9BF0

**Container:** max-width 480px, centered, margin 32px auto 40px

---

## PROMPT 3 — Page Header

**Container:** max-width 480px, centered, text-align center, margin-bottom 32px

**Title:** "Backing up your account..." — 23px/700/#0F1419

**Account row** (centered, flex, gap 8px, justify-content center):
- Platform icon 24px + "@username" 15px/600/#0F1419 + "(Twitter/X)" 13px/400/#536471

---

## PROMPT 4 — Overall Progress Block

**Container:** max-width 480px, centered, margin-bottom 28px

**Percentage label:** "62%" — 20px/700/#0F1419, text-align right, margin-bottom 8px

**Progress bar:**
- Full-width, height 16px, radius 9999px
- Track: #EFF3F4
- Fill: #1D9BF0, animated via CSS transition width 500ms ease

**Time estimate:** "Estimated time remaining: 3 minutes" — 14px/400/#536471, centered, margin-top 12px

---

## PROMPT 5 — Category Progress Card

**Container:** max-width 640px, centered

**Card:** bg #FFFFFF, border 1px #EFF3F4, radius 24px, padding 24px

4 category rows (gap 16px, divider 1px #EFF3F4 between):

**Each row:**
Row 1: [status icon 20px] [label 15px/600/#0F1419 flex-grow] [count 13px/500/#536471] [% 13px/700/#0F1419]
Row 2: progress bar, height 8px, track #EFF3F4

**Status icons:**
- ✓ completed: 20px circle #00BA7C bg, white checkmark
- ⟳ in-progress: 20px circle border 2px #1D9BF0 spinning, top border transparent
- ⏳ waiting: 20px circle #EFF3F4 bg, hourglass #8B98A5

**Category data (62% overall):**
1. Posts: ⟳ → "2,104 of 2,847" / "73%" / fill #1D9BF0
2. Followers: ⟳ → "847 of 1,204" / "70%" / fill #1D9BF0
3. Following: ⏳ → "0 of 892" / "0%" / fill #EFF3F4 + "(waiting...)" #8B98A5
4. Media: ⏳ → "0 of 1,523" / "0%" / fill #EFF3F4 + "(waiting...)"

---

## PROMPT 6 — Action Row

**Container:** max-width 640px, centered, margin 24px auto, flex, gap 16px, justify-content center

- "Run in Background" — ghost pill, border 1px #CFD9DE, text #536471, height 44px, 15px/600
- "Cancel" — ghost pill, border 1px #F4212E, text #F4212E, height 44px, 15px/600

**Mobile:** stacked full-width

---

## PROMPT 7 — "What's Happening" Panel

**Container:** max-width 640px, centered, margin-top 24px

**Card:** bg #F7F9F9, border 1px #EFF3F4, radius 24px, padding 24px

**Title:** "What's Happening" — 15px/700/#0F1419

**Body text:** two paragraphs 14px/400/#536471

**3 assurance rows** (margin-top 16px, gap 8px):
- Checkmark 16px #00BA7C + text 14px/400/#0F1419
- "Your data is encrypted during transmission"
- "Rate limits are automatically respected"
- "Progress will resume if interrupted"

---

## PROMPT 8 — Error State Banners

**Rate limited:**
- bg #FFFCE0, border-left 3px #FFD400, padding 12px 16px, radius 8px
- Text: 14px/600/#0F1419 | Countdown: 13px/400/#536471

**Network error:**
- bg #FFF5EC, border-left 3px #FF7A00, 14px/600/#0F1419

**Extension disconnected:**
- bg #FFFCE0, border-left 3px #FFD400, 14px/600/#0F1419

**Fatal error:**
- bg #FFF5F5, border-left 3px #F4212E, 14px/600/#F4212E
- "Retry" filled blue + "Contact Support" ghost, right-aligned

---

## PROMPT 9 — Completion State

**Container:** max-width 480px, centered, text-align center, padding 40px 24px

**Success circle:** 80px, bg #00BA7C, white checkmark 40px, scale-in animation

**Headline:** "All done!" — 31px/700/#0F1419
**Subhead:** "Your backup is complete and secure." — 15px/400/#536471, margin-top 8px

**4 result rows** (centered, flex justify-content center, gap 8px, margin-top 24px):
- Checkmark 20px #00BA7C + text 15px/500/#0F1419
- "2,847 posts backed up" / "1,204 followers saved" / "892 following accounts preserved" / "1,523 media files downloaded"

**Next backup:** "Your next backup is scheduled for tomorrow at 3:00 PM." — 13px/400/#536471, margin-top 12px

**CTA:** "Go to Dashboard" — filled blue pill, height 52px, 17px/700, margin-top 24px

**Countdown:** "Redirecting in 5s..." — 13px/400/#8B98A5

---

## COMPONENT VARIANTS

### 1. Overall Progress Bar (Large, Light)
- Track #EFF3F4, fill #1D9BF0, height 16px, radius 9999px

### 2. Category Progress Bar (Small, Light)
- Track #EFF3F4, fill #1D9BF0 or #00BA7C (completed), height 8px

### 3. Status Icon — In-Progress Spinner
- 20px circle, border 2px #1D9BF0, border-top transparent, spin 1s

### 4. Status Icon — Completed (Light)
- 20px #00BA7C circle, white checkmark

### 5. Status Icon — Waiting (Light)
- 20px #EFF3F4 bg, #8B98A5 hourglass

### 6. Warning Banner (Light)
- bg #FFFCE0, border-left 3px #FFD400, radius 8px

### 7. Error Banner (Light)
- bg #FFF5F5, border-left 3px #F4212E, radius 8px

### 8. Success Circle Animation
- 80px #00BA7C, white checkmark, scale 0→1 400ms ease-out

### 9. Cancel Button (Danger, Light)
- Ghost pill, border #F4212E, text #F4212E
- Hover: bg rgba(244,33,46,0.06)

### 10. "What's Happening" Card (Light)
- bg #F7F9F9, border 1px #EFF3F4, radius 24px
