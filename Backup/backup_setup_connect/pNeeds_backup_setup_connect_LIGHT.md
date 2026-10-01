dark_mode = false

# DESIGN MODE: LIGHT MODE
> This file specifies a **Light Mode** design.
> The UX designer who implements this file must apply a light mode visual style.
> Light mode uses a white background (#FFFFFF) with dark text (#0F1419 / #536471).
> Do NOT use dark mode colors when implementing these requirements.

---

# Product Requirements — Setup: Connect Account (Light Mode)
# Page: backup_setup_connect | URL: /setup/connect

---

## Page Purpose

Step 1 of the 3-step setup wizard. New users connect their social media account using one of three methods. Existing users reach this page to add another account or reconnect a disconnected one.

---

## Navigation Requirements

- **Standalone backup web app — NO JFKSocial left sidebar.**
- Minimal authenticated top nav: logo left, "Account ▾" + "Logout" right, no center links.
- Wizard progress indicator below the nav showing 3 steps (Step 1 active).

---

## Primary CTA

- Step 1 CTAs are per-method (not one global primary):
  - Card A: **"Install Extension"** — filled blue pill
  - Card B: **"Connect via API"** — ghost pill (expands form)
  - Card C: **"Upload File"** — ghost pill (expands drop zone)

---

## Wizard Progress Stepper Requirements

- 3 steps: Connect → Options → Backup
- Step 1 "Connect" is active (filled blue circle, bold label)
- Steps 2 and 3 are upcoming (gray circles, muted labels)
- Connector lines between circles: completed = blue, future = light gray (#EFF3F4)
- Mobile: simplified dot indicators

---

## Required Sections

### 1. Minimal Authenticated Header
- Logo left, Account dropdown + Logout right
- No main nav links

### 2. Setup Progress Indicator
- 3-step stepper: Connect (active) → Options → Backup
- Centered, max-width 480px

### 3. Page Heading
- Title (exact): "Connect Your Social Media Account"
- Subtitle (exact): "Choose how you'd like to back up your posts:"

### 4. Three Method Cards (stacked, max-width 680px centered)

**Card A — Chrome Extension (Recommended)**
- "Recommended" badge in green
- 4 benefit rows with green checkmarks
- Description of how it works
- CTA: "Install Extension" (filled blue)
- Post-install: green success banner replaces CTA with "Continue"

**Card B — API Connection**
- Meta: "For developers with Twitter API access"
- 2 benefits (green) + 2 warnings (yellow triangle icons)
- CTA: "Connect via API" (ghost) → expands API credential form
- Form: Platform dropdown, Handle, API Key, Secret, Access Token, Access Secret
- Help link, Cancel + Connect actions

**Card C — Manual Import**
- Meta: "Upload a data export file from your social network"
- 2 benefits + 2 warnings
- CTA: "Upload File" (ghost) → expands file drop zone
- Drop zone: drag & drop target, Browse Files, file format spec
- Preview state: show found counts, Import button

### 5. Skip Action
- "Skip for Now" — centered ghost button → opens confirmation modal

### 6. Footer
- "Need help? Contact Support | Help Center"

---

## Required States & Interactions

### Chrome Extension States
- Default → Detected (green success banner) → Not detected (error banner)

### API Form States
- Collapsed → Expanded → Validating (spinner) → Success (auto-advance) → Error (inline)

### File Upload States
- Empty → Drag-over (highlighted border) → Uploading (progress bar) → Parsing → Preview (counts + Import) → Error

### Skip Modal
- Title: "Skip connecting an account?"
- Body: warning about not being able to back up
- Buttons: "Go Back" (default focus) + "Skip Anyway" (red-styled)

---

## Error Messages (Exact Copy)

- "Extension not detected. Please install it and refresh this page."
- "Twitter API is currently rate limiting us. Please try again in 15 minutes."
- "File exceeds 500MB limit. Please contact support for enterprise import."
- "Invalid credentials. Please check and try again."

---

## Navigation Destinations

- Install Extension → Chrome Web Store (new tab)
- API Connect success → /setup/options
- File Import success → /setup/options
- Skip Anyway → /dashboard (empty state)
- Logo → / (landing)
- Help → /help
