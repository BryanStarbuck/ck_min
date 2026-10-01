dark_mode = true

# DESIGN MODE: DARK MODE
> This file specifies a **Dark Mode** design.
> The UX designer who implements this file must apply a dark mode visual style.
> Dark mode uses a dark background (#15202B) with light text (#FFFFFF / #8B98A5).
> Do NOT use light mode colors when implementing these requirements.

---

# Product Requirements — Backup Posts Landing Page (Dark Mode)
# Page: backup_landing | URL: /

**Product Manager Voice — UX Designer Note:** This document defines functional and content requirements. Visual implementation must use the dark mode palette. The UX designer is responsible for translating these requirements into polished visual designs.

---

## Page Purpose

Marketing landing page for the Backup Posts feature. Converts unauthenticated visitors (arriving from search, referrals, or the Free Speech Defender wizard) into signups. The page must communicate value quickly and drive the user to "Get Started Free."

---

## Navigation Requirements

- This is a **standalone backup web application** — NOT the JFKSocial social feed.
- **No JFKSocial left sidebar.** Do not include it.
- Top navigation bar only: logo left, nav links center (Features, Pricing, FAQ), action buttons right (Login + Get Started Free).
- On mobile: hamburger drawer containing Features, Pricing, FAQ, Login, Get Started.
- **Authenticated state:** Header shows user avatar + handle dropdown + "Go to Dashboard" in place of "Get Started Free."

---

## Primary CTA

- Label: **"Get Started Free"**
- Style: filled blue pill, bg #1D9BF0, text #FFFFFF, height 52px, radius 9999px, 17px/700
- Mobile: full-width button
- Authenticated variant: "Go to Dashboard"

---

## Required Sections (top to bottom)

### 1. Fixed Top Navigation
- Logo: shield icon + "Backup Posts" wordmark
- Nav links: Features, Pricing, FAQ
- Buttons: Login (ghost), Get Started Free (filled blue)
- Scroll behavior: gains solid dark background + border-bottom on scroll

### 2. Hero Section
- Headline (exact): "Your Posts. Your Data. Always."
- Subhead (exact): "Back up your Twitter/X posts before they're gone. Protect against censorship and account bans."
- CTA row: "Get Started Free" (primary) + "Learn More" (ghost, scrolls to #features)
- Hero illustration/screenshot showing the product below CTAs
- Unauthenticated primary CTA → /signup; Authenticated → /dashboard

### 3. How It Works — 3 Steps
- Section title: "How It Works"
- Step 1: "Connect" — Chrome extension or API
- Step 2: "Configure" — Choose what to back up and sync frequency
- Step 3: "Protected" — Posts safe, always accessible
- Horizontal 3-card row on desktop, stacked vertically on mobile

### 4. Key Features — 2×3 Grid
- Section title: "Key Features"
- 6 feature cards with checkmark icons (green #00BA7C), title, and 1-sentence body
- Features: Automatic Daily Backups, Your Data Your Control, Posts + Followers + Media, Export Anywhere, Censorship Detection, Privacy + Encryption

### 5. Social Proof / Trust Signals
- Stat line (exact): "Backed up 2.4M posts for 50,000+ users"
- 3 testimonial cards: quote + avatar + handle
  - "@user1": "Life saver"
  - "@user2": "Highly secure"
  - "@user3": "Best backup tool"

### 6. Pricing Plans — 4 Cards
- Section anchor: #pricing
- Plans: Free ($0/mo), Creator ($9/mo — highlighted as "Most Popular"), Studio ($29/mo), Enterprise (Custom)
- Creator card: highlighted with blue border + "Most Popular" pill badge
- Each card: plan name, price, feature list with checkmarks, CTA button
- Authenticated user: CTA changes to "Upgrade" or "Current Plan" per user's plan
- Mobile: swipe carousel with "1 of 4" pagination dots

### 7. FAQ Accordion
- Section anchor: #faq
- 5 questions, first pre-expanded
- Q1 (exact): "How does the backup work?"
- Q2: "Is my data secure?"
- Q3: "Can I export to other platforms?"
- Q4: "What happens if X/Twitter changes its policies?"
- Q5: "How much storage do I get?"
- Chevron rotates 90° on expand; 200ms height transition

### 8. Final CTA Band
- Headline (exact): "Ready to protect your posts?"
- Button (exact): "Get Started Free Today"
- Note below (exact): "No credit card required"
- Distinct background to separate from page

### 9. Footer — 4-Column Grid
- Column 1: Logo + tagline
- Column 2: Product (Features, Pricing, FAQ)
- Column 3: Company (About, Blog, Contact)
- Column 4: Resources + Legal (Docs, Help Center, Status, Privacy, Terms, Security)
- Bottom bar (exact): "© 2026 JFKSocial.com — Part of the Social Network Ecosystem"

---

## Interaction States Required

### Button States
- Primary button: default, hover, pressed, disabled
- Ghost button: default, hover

### Pricing Card States
- Default: standard card
- Highlighted (Creator): blue border + "Most Popular" badge
- Hover (all): lift shadow + translateY(-2px)

### FAQ Accordion
- Collapsed: shows question + chevron at minimum 48px row height
- Expanded: answer visible, chevron rotated 90°

### Navigation States
- Unauthenticated: Login + Get Started Free
- Authenticated: user avatar dropdown + Go to Dashboard
- Scrolled page: nav bar gains visible border-bottom

---

## Responsive Requirements

- Desktop (≥1024px): 3-column How It Works, 2×3 features grid, 4-column pricing row
- Tablet (640–1023px): 2-column grids
- Mobile (<640px): single column, stacked; pricing becomes swipe carousel with dots

---

## Navigation Destinations

- "Get Started Free" → /signup
- "Learn More" → smooth scroll to #features
- Login → /login
- Features nav → smooth scroll to #features
- Pricing nav → smooth scroll to #pricing
- FAQ nav → smooth scroll to #faq
- Footer: Help Center → /help | Privacy → /privacy | Terms → /terms | Status → /status
- Enterprise Contact → /help or sales form
