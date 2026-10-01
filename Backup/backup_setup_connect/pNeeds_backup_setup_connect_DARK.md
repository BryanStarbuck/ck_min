dark_mode = true

# DESIGN MODE: DARK MODE
> This file specifies a **Dark Mode** design.
> The UX designer who implements this file must apply a dark mode visual style.
> Dark mode uses a dark background (#15202B) with light text (#FFFFFF / #8B98A5).
> Do NOT use light mode colors when implementing these requirements.

---

# Product Requirements — Setup: Connect Account (Dark Mode)
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
- Connector lines between circles indicate completion state
- Mobile: simplified dot indicators

---

## Required Sections

### 1. Minimal Authenticated Header
- Logo left, Account dropdown + Logout right
- No main nav links (wizard context)

### 2. Setup Progress Indicator
- 3-step stepper: Connect (active, step 1) → Options → Backup
- Centered, max-width 480px

### 3. Page Heading
- Title (exact): "Connect Your Social Media Account"
- Subtitle (exact): "Choose how you'd like to back up your posts:"

### 4. Three Method Cards (stacked, max-width 680px centered)

**Card A — Chrome Extension (Recommended)**
- Header: Chrome icon + "Chrome Extension (Recommended)" + "Recommended" badge (green)
- 4 benefit rows with green checkmarks:
  - "No API keys needed"
  - "Works even if APIs are restricted"
  - "Reads your profile page directly"
  - "Most reliable method"
- Description of how it works (1–2 sentences)
- CTA: "Install Extension" (filled blue, right-aligned)
- Post-install state: replace CTA with "Continue" when extension detected

**Card B — API Connection**
- Header: Key icon + "API Connection" + meta "For developers with Twitter API access"
- 2 benefit rows (green checkmarks) + 2 warning rows (yellow triangle)
- CTA: "Connect via API" (ghost, expands API credential form)
- Expandable form fields: Platform, Handle, API Key, API Secret, Access Token, Access Secret
- Help link: "How to get API credentials →"
- Form actions: "Cancel" + "Connect" (validate → /setup/options on success)

**Card C — Manual Import**
- Header: Upload icon + "Manual Import" + meta description
- 2 benefits + 2 warnings
- CTA: "Upload File" (ghost, expands file drop zone)
- Drop zone: drag-and-drop ZIP file target, "Browse Files" button
- File spec: "Accepted: .zip (Twitter data export) | Max size: 500 MB"
- On valid file: show found counts (posts, followers, following) + "Import" button

### 5. Skip Action
- "Skip for Now" — centered ghost button
- Click opens confirmation modal

### 6. Footer
- "Need help? Contact Support | Help Center" — centered, muted text

---

## Required States & Interactions

### Chrome Extension States
- Default: "Install Extension" button
- Detected: green success banner "Extension detected! Click Continue to connect."
- Not detected after install attempt: inline error banner

### API Form States
- Collapsed: only header + CTA visible
- Expanded: full form visible
- Validating: spinner on Connect button, disabled state
- Success: "✓ Connected!" message, auto-advance to /setup/options after 1s
- Error: inline red error below Connect button

### File Upload States
- Empty drop zone (default)
- Drag-over: highlighted border
- Uploading: progress bar + percentage
- Parsing: spinner + "Parsing data..." message
- Preview: shows found counts as pills, "Import" CTA
- Error: red error message

### Skip Modal
- Title: "Skip connecting an account?"
- Body: "You won't be able to back up posts until you connect an account. Are you sure?"
- Buttons: "Go Back" (default focus) + "Skip Anyway" (red text)

---

## Error Messages (Exact Copy)

- Extension not detected: "Extension not detected. Please install it and refresh this page."
- API rate limited: "Twitter API is currently rate limiting us. Please try again in 15 minutes."
- File too large: "File exceeds 500MB limit. Please contact support for enterprise import."
- Invalid API credentials: "Invalid credentials. Please check and try again."

---

## Navigation Destinations

- Install Extension → Chrome Web Store (new tab)
- API Connect success → /setup/options
- File Import success → /setup/options
- Skip Anyway → /dashboard (empty state)
- Logo → / (landing)
- Contact Support / Help Center → /help
