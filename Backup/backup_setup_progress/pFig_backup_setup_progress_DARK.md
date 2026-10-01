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

# Figma Make Prompts — Setup: Backup Progress (Dark Mode)
# Page: backup_setup_progress | URL: /setup/progress

> **Navigation Note:** This is a standalone backup web application — NOT the JFKSocial social feed.
> There is NO JFKSocial left sidebar. Minimal authenticated top nav only.
> This is Step 3 (final step) of the 3-step setup wizard.

---

## DESIGN TOKEN REFERENCE

### Colors (Dark Mode)
* Page bg:              #15202B
* Card bg:              #1E2732
* Info panel bg:        #1E2732 (slightly elevated)
* Borders:              #2F3336
* Primary text:         #FFFFFF
* Secondary text:       #8B98A5
* Brand blue:           #1D9BF0
* Success green:        #00BA7C
* Danger red:           #F4212E
* Warning yellow:       #FFD400
* Warning bg tint:      #1A1800
* Network error:        #FF7A00
* Progress bar track:   #253341
* Spinner color:        #1D9BF0

### Typography
* Page title:      23px / 700 / #FFFFFF
* Account tag:     15px / 600 / #FFFFFF
* Platform meta:   13px / 400 / #8B98A5
* Progress %:      20px / 700 / #FFFFFF
* ETA text:        14px / 400 / #8B98A5
* Category label:  15px / 600 / #FFFFFF
* Count text:      13px / 500 / #8B98A5
* Category %:      13px / 700 / #FFFFFF
* Reassurance:     14px / 400 / #8B98A5
* Info title:      15px / 700 / #FFFFFF
* Success headline: 31px / 700 / #FFFFFF
* Success result:  15px / 500 / #FFFFFF

---

## PROMPT 1 — Minimal Authenticated Header

**Container:** full-width, height 64px, bg #15202B, border-bottom 1px #2F3336

**Left:** Shield icon + "Backup Posts" 17px/700/#FFFFFF
**Right:** "Account ▾" 15px/500/#8B98A5 + "Logout" 15px/400/#8B98A5, gap 20px
**Mobile:** Logo center, Account ▾ right, height 56px

---

## PROMPT 2 — Setup Progress Indicator (Step 3 Active, All Steps Active/Complete)

**Step 1 — Connect (COMPLETED):**
- Circle 32px: bg #1D9BF0, white checkmark
- Label: "Connect" 13px/500/#8B98A5

**Step 2 — Options (COMPLETED):**
- Circle 32px: bg #1D9BF0, white checkmark
- Label: "Options" 13px/500/#8B98A5

**Step 3 — Backup (ACTIVE):**
- Circle 32px: bg #1D9BF0, "3" 13px/700/#FFFFFF
- Label: "Backup" 13px/700/#FFFFFF

**Both connector lines:** filled #1D9BF0

**Container:** max-width 480px, centered, margin 32px auto 40px
**Mobile:** 3 dots, all active/complete #1D9BF0

---

## PROMPT 3 — Page Header

**Container:** max-width 480px, centered, text-align center, margin-bottom 32px

**Title:** "Backing up your account..." — 23px/700/#FFFFFF

**Account identifier row** (centered, flex, gap 8px, margin-top 12px, justify-content center):
- Twitter/X icon 24px (dark circle with white X letterform)
- "@username" — 15px/600/#FFFFFF
- "(Twitter/X)" — 13px/400/#8B98A5

---

## PROMPT 4 — Overall Progress Block

**Container:** max-width 480px, centered, margin-bottom 28px

**Overall progress bar:**
- Full-width, height 16px, radius 9999px
- Track: #253341
- Fill: #1D9BF0, animated smoothly (current: 62%)
- Fill transitions via CSS transition: width 500ms ease

**Percentage label:**
- "62%" — 20px/700/#FFFFFF, text-align right, margin-bottom 8px
- Positioned above or below bar (above preferred)

**Time estimate:**
- "Estimated time remaining: 3 minutes" — 14px/400/#8B98A5, text-align center, margin-top 12px

---

## PROMPT 5 — Category Progress Card

**Container:** max-width 640px, centered

**Card:** bg #1E2732, border 1px #2F3336, radius 24px, padding 24px

4 category rows inside card (gap 16px, divider 1px #2F3336 between rows):

**Each row structure:**
Row 1 (flex, align-items center, gap 8px):
- Status icon 20px (left)
- Category label 15px/600/#FFFFFF (flex-grow)
- Count "X of Y" 13px/500/#8B98A5
- Percentage 13px/700/#FFFFFF

Row 2: full-width progress bar, height 8px, radius 9999px, track #253341

**Status icons:**
- ✓ completed: 20px circle, bg #00BA7C, white checkmark
- ⟳ in-progress: 20px spinning circle, stroke #1D9BF0, animation: spin 1s linear infinite
- ⏳ waiting: 20px circle, bg #253341, hourglass icon #8B98A5

**Category data (in-progress state at 62% overall):**
1. Posts: ⟳ in-progress → "2,104 of 2,847" / "73%" / fill #1D9BF0
2. Followers: ⟳ in-progress → "847 of 1,204" / "70%" / fill #1D9BF0
3. Following: ⏳ waiting → "0 of 892" / "0%" / fill #253341 + "(waiting...)" suffix in #8B98A5 after count
4. Media: ⏳ waiting → "0 of 1,523" / "0%" / fill #253341 + "(waiting...)"

---

## PROMPT 6 — Action Row

**Container:** max-width 640px, centered, margin 24px auto, flex, gap 16px, justify-content center

- "Run in Background" — ghost pill, border 1px #2F3336, text #8B98A5, height 44px, 15px/600, radius 9999px
- "Cancel" — ghost pill, border 1px #F4212E, text #F4212E, height 44px, 15px/600, radius 9999px

**Mobile:** stacked full-width, "Run in Background" first, "Cancel" below

---

## PROMPT 7 — "What's Happening" Panel

**Container:** max-width 640px, centered, margin-top 24px

**Card:** bg #1E2732, border 1px #2F3336, radius 24px, padding 24px

**Title:** "What's Happening" — 15px/700/#FFFFFF, margin-bottom 12px

**Body text:**
- "Your posts are being securely backed up to your account. This process may take several minutes depending on how much content you have." — 14px/400/#8B98A5
- "You can safely close this page and we'll email you when it's done." — 14px/400/#8B98A5, margin-top 8px

**3 assurance rows** (margin-top 16px, gap 8px):
Each row: checkmark circle 16px #00BA7C + text 14px/400/#FFFFFF, gap 8px
- "Your data is encrypted during transmission"
- "Rate limits are automatically respected"
- "Progress will resume if interrupted"

---

## PROMPT 8 — Error State Banners

Create inline error/warning banners that appear above the category progress card.

**Rate limited banner:**
- bg #1A1800, border-left 3px #FFD400, padding 12px 16px, radius 8px, margin-bottom 16px
- "⚠ Rate limited. Waiting 15 minutes, then resuming automatically..." 14px/600/#FFD400
- Countdown: "Retrying in 14:32..." — 13px/400/#8B98A5

**Network error banner:**
- bg #1A1000, border-left 3px #FF7A00, padding 12px 16px, radius 8px
- "Connection lost. Retrying..." + 16px spinning indicator, 14px/600/#FF7A00

**Extension disconnected:**
- bg #1A1800, border-left 3px #FFD400
- "Chrome extension disconnected. Please keep the extension running." 14px/600/#FFD400

**Fatal error:**
- bg #1A0000, border-left 3px #F4212E
- Error message text, 14px/600/#F4212E
- Buttons: "Retry" (filled blue) + "Contact Support" (ghost), right-aligned, gap 12px

---

## PROMPT 9 — Completion State

Replace the in-progress content with this after backup reaches 100%.

**Container:** max-width 480px, centered, text-align center, padding 40px 24px

**Success animation:**
- 80px circle: bg #00BA7C, white checkmark icon 40px, scale-in animation (0→1 over 400ms)
- Margin-bottom 24px

**Headline:** "All done!" — 31px/700/#FFFFFF
**Subhead:** "Your backup is complete and secure." — 15px/400/#8B98A5, margin-top 8px

**4 result rows** (margin-top 24px, gap 8px, centered):
Each row: checkmark 20px #00BA7C + text 15px/500/#FFFFFF, flex, justify-content center, gap 8px
- "✓ 2,847 posts backed up"
- "✓ 1,204 followers saved"
- "✓ 892 following accounts preserved"
- "✓ 1,523 media files downloaded"

**Next backup notice:**
- "Your next backup is scheduled for tomorrow at 3:00 PM." — 13px/400/#8B98A5, margin-top 12px

**CTA:**
- "Go to Dashboard" — filled blue pill, bg #1D9BF0, text #FFFFFF, height 52px, 17px/700, margin-top 24px, radius 9999px

**Auto-redirect countdown:**
- "Redirecting in 5s..." — 13px/400/#8B98A5, margin-top 12px

---

## COMPONENT VARIANTS

### 1. Overall Progress Bar (Large)
- Track #253341, fill #1D9BF0, height 16px, radius 9999px
- Width animates via JS-driven inline style

### 2. Category Progress Bar (Small)
- Track #253341, fill #1D9BF0, height 8px, radius 9999px

### 3. Status Icon — In-Progress Spinner
- 20px circle border 2px #1D9BF0, border-top transparent, animation spin 1s linear infinite

### 4. Status Icon — Completed
- 20px filled circle #00BA7C, white checkmark 12px

### 5. Status Icon — Waiting
- 20px circle bg #253341, hourglass icon #8B98A5

### 6. Warning Banner
- bg #1A1800, border-left 3px #FFD400, radius 8px, padding 12px 16px

### 7. Error Banner
- bg #1A0000, border-left 3px #F4212E, radius 8px

### 8. Success Circle Animation
- 80px #00BA7C circle, white checkmark, scale-in 400ms ease-out

### 9. Action Button — Cancel (Danger)
- Ghost pill, border 1px #F4212E, text #F4212E, height 44px
- Hover: bg rgba(244,33,46,0.08)

### 10. "Run in Background" Button
- Ghost pill, border 1px #2F3336, text #8B98A5, height 44px
- Click: shows toast "Backup running. We'll email you when done." then navigate /dashboard
