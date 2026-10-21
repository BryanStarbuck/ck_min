# p_timeline_create — Site-wide likelihood timeline SVGs

**DO NOT RUN THIS PROMPT YET** (until Bryan asks). When run, the agent walks the public Docusaurus tree, decides per page whether a **likelihood-of-when** timeline belongs there, reuses a pre-built SVG when one already measures the same event, or creates a new SVG + registry row.

---

## Absolute paths and roots

| Symbol | Path |
|--------|------|
| `ROOT_DIR` | `~/BGit/Bryan_git/charlie-kirk` |
| `SITE_DOCS` | `{ROOT_DIR}/site/docs/` — **start walking here** |
| `TIMELINES_CSV` | `{ROOT_DIR}/timeslines.csv` — registry (create if missing). Filename is exactly **`timeslines.csv`** at repo root (not under `site/`). |
| `STATIC_IMG` | `{ROOT_DIR}/site/internals/static/img/` — **only** static root Docusaurus serves |
| `TIMELINE_SVG_DIR` | `{ROOT_DIR}/site/internals/static/img/km-timelines/` — established location for kill-me claim timelines; use this pattern for new event families |

### Critical static-asset rule

`site/docusaurus.config.ts` sets `staticDirectories: ["internals/static"]`. **Never** put SVGs under `site/static/` (not published). **One canonical copy only**, in `internals/static`: a second copy in `site/static/` invites someone to edit the dead copy and conclude SVGs are broken. The 13 byte-identical KM copies tracked under `site/static/img/km-timelines/` are stale dead weight: never add to, edit, or trust them.

Public URL `/img/<subdir>/<filename>.svg` = disk `{ROOT_DIR}/site/internals/static/img/<subdir>/<filename>.svg`. Live example: disk `site/internals/static/img/km-timelines/km-02-timeline.svg`, MDX `<img src="/img/km-timelines/km-02-timeline.svg" … />`, public `https://whoassassinatedcharliekirk.com/img/km-timelines/km-02-timeline.svg`.

Prefer SVG; convert to PNG/JPEG only after a proven rendering failure from `internals/static`.

---

## What these timelines are (and are not)

**Not** government-certified times. **Relative-likelihood charts** of when a claimed event most likely occurred, built from investigation notes (`Charlie_Kirk.txt` — **read-only**), named witnesses, interviews, recaps, **any X/Twitter claim or implication** about when ("day before," "weeks before," "Aug 13," "night of," "24 hours," minutes/hours), and web packaging dating the same claim. Bar **height** = relative likelihood for that time bin; x-axis = earliest to latest plausible, **aggressively trimmed**.

### Anti-pattern never to repeat (live bug: KM-06)

Page `https://whoassassinatedcharliekirk.com/Charlie/Text_Messages/kill-me-06-worried-israel-kill-me`, chart `km-06-timeline.svg` / `km_06_worried_israel_kill_me`: the claim peaks **SEPT 9** (range ~SEPT 8–9), but the SVG used a shared summer axis **AUG 1 → SEPT 10**, likelihood ~0 until ~SEPT 6, and MDX forced `width: '100%'`, stretching the empty left half across the column. **Hard failure** even with a correct peak label. Fix by **cropping the domain** and **not forcing full width** (rules below).

Every page with a chart gets prose **above** the image:

> **Best understanding of when [this happened / he said this]**
> …working date range, peak, sources of uncertainty…

and **below** (before Related Areas / author credit) a section of **exact X/Twitter (and other) quotes** about timing, in the wording people used.

Rules: **never remove** pre-existing claims or data; **do not soften** public pages for legal risk beyond what the page already does, and never invent court findings; grow information, don't shrink it.

---

## Registry: `{ROOT_DIR}/timeslines.csv`

Create if missing with header:

```csv
event_key,event,path_to_cvg,description
```

`path_to_cvg` is the registry's column name for the chart path (SVG, or PNG if conversion was required), including filename, in the form:

```text
site/internals/static/img/<family>/<filename>.svg
```

| Column | Meaning |
|--------|---------|
| **event_key** | Primary key. Few words, `snake_case`, **unique per row**. E.g. `km_02_harrison_smith_relay`, `uvu_shot_moment_2025_09_10`, `robinson_surrender_chain`. |
| **event** | Human name of the event **and sub-event**, specific to **one** time window (e.g. `KM-02 Harrison Smith relay — when Charlie’s underlying remark (if any) was made`, not just "kill me texts"). |
| **path_to_cvg** | Path under the served tree, **including filename**; must match where the site hosts it. |
| **description** | What is timed and **which aspect** of a larger meta-event; if similar to another row, how it differs, **citing that `event_key`**. |

### Reuse vs create

1. Open (or create) the CSV; search by meaning (same claim, same person-said-X, same physical event, same minute window).
2. Same time question already measured: **reuse** `path_to_cvg` (no duplicate SVGs).
3. A **different sub-event** (wording, recipient, day cluster): **new** `event_key`, SVG and row, cross-linked in `description`.
4. Append the row immediately after creating an SVG. Never reuse an `event_key` for a different question; never delete others' rows.

### Seed from existing work (kill-me claims)

Under `site/internals/static/img/km-timelines/`; register on first run if missing:

| event_key (suggested) | file | measures |
|----------------------|------|----------|
| `km_01_wiped_out_premonition` | `km-01-timeline.svg` | When the “wiped out at any time” premonition text was said (multi-year) |
| `km_02_harrison_smith_relay` | `km-02-timeline.svg` | When Charlie’s underlying Israel-kill fear was expressed (on/before AUG 13 Smith post) |
| `km_03_break_away_pro_israel` | `km-03-timeline.svg` | “They will kill me if I break away…” (AUG 13 index window) |
| `km_04_go_against_israel` | `km-04-timeline.svg` | “If I go against Israel I think they will kill me” (AUG 13 / AUG 16 bimodal) |
| `km_05_turek_want_me_dead` | `km-05-timeline.svg` | Turek “want me dead / under the gun” weeks-before vs day-before vs months-apart |
| `km_06_worried_israel_kill_me` | `km-06-timeline.svg` | “I’m worried Israel is going to kill me” (~one day before) |
| `km_07_sept9_all_caps` | `km-07-timeline.svg` | “THEY ARE GOING TO KILL ME” SEPT 9 meeting |
| `km_08_kolvet_they_will_kill_me` | `km-08-timeline.svg` | Kolvet-bound night-before kill-me |
| `km_09_three_people_warned` | `km-09-timeline.svg` | “I think they’re going to kill me” to ~three people SEPT 9 |
| `km_10_flood_executed_tomorrow` | `km-10-timeline.svg` | Flood “executed tomorrow” night SEPT 9 |
| `km_11_the_left_will_kill_me` | `km-11-timeline.svg` | Competing Flood wording (same night as `km_10_…`) |
| `km_12_security_exchange` | `km-12-timeline.svg` | Security exchange “I know they want me dead” |
| `km_13_donor_executed_tomorrow` | `km-13-timeline.svg` | Donor lane of execute/kill tomorrow multi-recipient claim |

Pages embedding them: `site/docs/Charlie/Text_Messages/kill-me-01-*.mdx` … `kill-me-13-*.mdx`.

---

## Orchestration: one agent per directory under `site/docs/`

1. List top-level directories and root-level `.md`/`.mdx` under `{ROOT_DIR}/site/docs/`.
2. One agent (or sequential workstream) per top-level directory (`Charlie/`, `FBI/`, `After/`, `Timeline/`, `People/`, …); root files are a small "root" workstream.
3. Each walks **all** pages under its tree recursively.
4. All share the one registry: read it before creating, write rows atomically where possible, no duplicate `event_key`s; reuse by `event_key`/description match before inventing a path.

### Per-page decision (exactly one)

| Decision | Action |
|----------|--------|
| **A. Already has a correct timeline** | Verify the SVG under `internals/static`, URL works, CSV row exists (add if missing), and run the emptiness check. Remove nothing. |
| **B. Needs a timeline — reuse** | Embed the matching registry chart's public path (prose + img + timing quotes if missing). If the reused chart has the KM-06 empty-tail disease, **rebuild it**. |
| **C. Needs a timeline — create** | Research → likelihood window → SVG to static path → CSV row → embed. |
| **D. No timeline** | Leave the page (internal note OK). Most index, law-text and non-temporal analysis pages. |

Add or reuse when the page is substantially about **when something happened or was said**: a dated claim, warning, text, call, flight, sighting, resignation, paving, surrender, hearing, leak or meeting; "day before," "48 hours," "weeks before," "night of SEPT 9"; competing date theories; especially **SEPT 8–12, 2025** (Charlie, Tyler Robinson, security, campus, FBI, medical, flights).
Skip pure navigation, glossary, undated opinion; pages where timing is no real open question; and a child page when its parent overview already hosts the chart and the child doesn't re-argue timing (a link to the parent is optional).

---

## How to build a likelihood timeline SVG

### 1. Research the time question (this sub-event only)

Read the page and linked pages; pull master-file date language (read-only); search X/web for **any** claim or implication of when; keep **exact quotes** with handles and status IDs; note **competing** datings (AUG 13 vs AUG 16; weeks-before vs months-apart). Write down the **support window** (where likelihood is non-trivial) **before** picking an axis. Never default to AUG 1–SEPT 10.

### 2. Choose resolution (driven by where the mass is)

| Context | Axis resolution |
|---------|-----------------|
| Multi-year premonition / long-running state | Years (see `km-01`) |
| Real mass across **weeks–months** | Days or day-clusters; labels like `AUG 13`, `SEPT 9` (year 2025 unless multi-year) |
| Mass in about **3–5 days** or less | Short window only, **4–6 bars per day** (6/day ≈ 4h windows: 00–04, 04–08, 08–12, 12–16, 16–20, 20–24); major ticks per day, optional second row for time |
| **1 day or same-day disputes** | Hour (or 1–2 hour) bins; minutes when claims support them |
| **SEPT 8–12, 2025** (two days before through two after SEPT 10), esp. Robinson, security, UVU, medical, surrender, flights | Hour / 4-hour / minute; time of day often matters more than the day |

Short-window rule: when ~≥80% of mass is within ~3–5 days, set the domain to that span plus a small margin, split days into 4–6 bars, and spread likelihood across sub-day bars (a soft evening hump beats one fat day-column on a blank month). KM-06 should have been ~SEPT 7–10 (or 8–10) with several bars per day.

### 3. Likelihood curve + hard trim rules (mandatory)

Bins only inside the trimmed domain; relative likelihood from public claims (no false precision); shape may be bell, **bimodal**, wide flat (high uncertainty) or spike; mark the best working peak (`AUG 13`, `SEPT 9 night`, `12:23 PM`).

A chart failing these is **not done**:
1. **Domain = support**: start near the first non-trivial bin, end near the last; no global default start.
2. **Cut near-zero tails** (under ~5–10% of peak, or flat empties after a clear rise elsewhere); never keep them "to show the month."
3. **Crop test**: from cumulative mass left and right, keep ~**≥95%** of mass visible (≥90% if the rest is a deliberately kept small distant secondary peak, still with no month of zeros between). If >~15–20% of the width is still bars under ~10% of peak, crop harder or use a finer short window.
4. **No silent zero padding** to match another chart's viewBox or range; each `event_key` picks its own domain.
5. **Distant competing dates**: a **bimodal** chart of two short neighborhoods with no drawn zero gap, or keep the primary window and mention the alternate in prose (preferred when it is tiny).
6. **Blur test**: if most of the rectangle would be empty, fail and re-trim or re-bin.

### 4. Axis labels

`AUG`, `SEPT` abbreviations (full names only for multi-year); day ticks like `AUG 13`, `SEPT 9`. Sub-day charts use **two rows**: date (`SEPT 10`), then time or slot (`12:23 PM`, `~8 PM`, `16–20`). Compact `12-AUG` is fine if consistent within a family. Label only ticks inside the trimmed domain.

### 5. Visual design + width policy (no forced full-page stretch)

Use the KM SVGs for **style only**, not their 920px domain (early `viewBox="0 0 920 220"` + MDX `width: '100%'` magnified empty tails).
1. **Intrinsic width follows the data**: 1–5 days of mass → narrower viewBox (~400–640 × ~200–220) or fewer, wider-pitched bars; real multi-week mass → ~720–920 is fine. Never add empty bins to match other charts.
2. Full page width is **not** a goal; empty page space beside a compact chart is preferred over a stretched desert of zeros.
3. Never bare `width: '100%'` on a short chart's `<img>`; use a wrapper `maxWidth` ≈ chart width with `style={{width:'auto', maxWidth:'100%', height:'auto', display:'block'}}` (or explicit img `maxWidth`, e.g. 560 for a SEPT 8–10 chart).
4. Modest height; density should show real mass, not whitespace.
Also: rounded card background, subtle gradient; vertical bars, color scaling cool → warm with height; optional smooth envelope stroke; peak dot + label; event title and a subtitle that bar height = relative likelihood; footer working range **matching the trimmed domain**; accessible (`role="img"`, `aria-label`, good contrast).

### 6. Write the file to the correct static location

| Family | Subdir | Notes |
|--------|--------|-------|
| Kill-me / KM claims | `km-timelines/` | **Established** — keep using |
| New families | `timelines/<topic>/` or a topic folder under `img/` | e.g. `timelines/robinson/`, `timelines/flights/`, `timelines/uvu/` |

Filename descriptive, stable, lowercase-hyphen, `.svg`. Set `path_to_cvg` to that repo-relative path.

### 7. Embed on the MDX page

Insert **after** the early orientation / "At a glance" section, deleting nothing:

```mdx
## Best understanding of when [this happened]

[Prose: peak, range, uncertainty, what the curve is measuring. Not a court finding.]

**Date range (working model):** …  {/* must match the SVG’s trimmed domain */}

The chart below is **not** a government finding. Bar height is **relative likelihood** from public claims …

{/* SHORT support (≈1–5 days of real mass): cap width — do NOT full-bleed empty months */}
<div className="ck-km-timeline" style={{margin:'1rem 0 1.5rem', maxWidth:560, overflowX:'auto'}}>
  <img
    src="/img/km-timelines/km-06-timeline.svg"
    alt="… likelihood timeline …"
    width="560"
    height="220"
    style={{width:'auto', maxWidth:'100%', height:'auto', display:'block'}}
  />
</div>

{/* LONGER multi-week support with real mass across the span: wider cap is fine */}
<div className="ck-km-timeline" style={{margin:'1rem 0 1.5rem', maxWidth:920, overflowX:'auto'}}>
  <img
    src="/img/km-timelines/km-02-timeline.svg"
    alt="… likelihood timeline …"
    width="920"
    height="220"
    style={{width:'auto', maxWidth:'100%', height:'auto', display:'block'}}
  />
</div>
```

Use the real public `/img/...` path. **Match `maxWidth`/`width` to the trimmed viewBox** (a 3-day chart with viewBox width 520 is never embedded at 920 / 100%).

#### MDX embed rules — JSX, not HTML

| Rule | Correct | Wrong — breaks build or image |
|------|---------|-------------------------------|
| Style must be a JS object, not a string | `style={{maxWidth:560}}` | `style="max-width:560px"` |
| CSS class attribute | `className="ck-km-timeline"` | `class="ck-km-timeline"` |
| `<img>` must be explicitly self-closed | `<img src="…" />` | `<img src="…">` |
| Comments | `{/* note */}` | `<!-- note -->` |
| Object keys are camelCase | `overflowX`, `maxWidth` | `overflow-x`, `max-width` |
| **Do not force full-column stretch on short charts** | `style={{width:'auto', maxWidth:'100%', …}}` + wrapper `maxWidth` ≈ chart width | Bare `style={{width:'100%'}}` on a few-day chart (KM-06 failure) |

**`<!-- -->` is the most common build-killer here**: one in an `.mdx` fails compilation, the Pages build goes red, and the site silently keeps the previous deploy (looks exactly like "my SVG did not render"). Blank line before and after the `<div>…</div>` so MDX parses it as a JSX block. Paths are **absolute from the site root** (`/img/km-timelines/foo.svg`), never relative (they 404 on nested pages) or filesystem paths.

Near the bottom (before defamation note / author credit / Related Areas):

```mdx
## X / Twitter posts on when this was likely said

Exact public claims and implications about **timing**:

- **[@handle](https://x.com/handle/status/ID)**: "exact quote…"
- **Source name**: "exact quote…"
```

Never strip prior claims to make room.

### 8. Update `timeslines.csv` (one row per new event_key).

---

## Example judgments (from KM work)

- **Tight post date, uncertain prior conversation** (KM-02): peak on/before the AUG 13 post; domain ~AUG 5–15, not through SEPT 10 if later mass is ~0; early-AUG tail only if claims support it.
- **Index vs public reel collision** (KM-04): **bimodal** AUG 13 and AUG 16, domain ~AUG 11–18.
- **"Weeks before" + counter-claim** (KM-05): if both have real mass, mid-AUG → SEPT 9; a tiny early-AUG months-apart theory goes in prose.
- **Night-before consensus** (KM-06, KM-07–10, 13): ~SEPT 7–10 or 8–10, 4–6 bars/day, compact SVG, MDX `maxWidth` ~480–640, peak SEPT 9 night (NOT AUG 1–SEPT 10 with a 920 viewBox at 100%).
- **Multi-year premonition** (KM-01): a year axis is right because the mass is multi-year.
- **Robinson / day-of** (later): 11:00 vs 12:23 vs evening disputes → hour/minute bins on SEPT 10 (and SEPT 9–11), two-line ticks, compact width.

Prefer many **specific** event_keys over one vague mega-chart; trim over wide empty axes (the highest-priority visual rule); compact over column-filling.

---

## Parallel agent checklist (per directory agent)

```text
[ ] Load timeslines.csv (create with header if missing)
[ ] Register any existing km-timelines SVGs missing from CSV
[ ] Enumerate all .md/.mdx under assigned directory
[ ] For each page: A / B / C / D decision
[ ] If C: research dates → **trim domain to mass** → pick bin size (4–6 bars/day if 3–5 day mass) → SVG in internals/static → CSV row → MDX embed + quotes
[ ] If B: embed existing path_to_cvg via /img/... URL; add prose/quotes if missing; **if reused chart has empty-tail disease (KM-06 style), rebuild that SVG** — reuse does not mean keep a bad chart
[ ] If A: verify asset + CSV row + **visual emptiness check** (no multi-week zero desert)
[ ] Write each SVG to internals/static ONLY — never a second copy in site/static/
[ ] MDX embed uses style={{}} / className / self-closed <img /> — no <!-- --> comments
[ ] MDX does **not** force short charts to full page width (`width:auto` + wrapper maxWidth ≈ viewBox)
[ ] Domain crop: ≥~95% of likelihood mass inside axis; no long <5–10%-of-peak tails
[ ] If mass is ≤~5 days: 4–6 bars per day (≈4h windows), not one bar per day on a month axis
[ ] Gate 1: every embed src resolves to a real, non-empty file on disk
[ ] Gate 2: `npm run build` exits clean AND chart appears in site/build/img/…
[ ] Gate 3: after deploy completes, svg=200 (image/svg+xml, non-zero) and page_refs >= 1
[ ] Before calling any chart broken: `gh run list` — in_progress means WAIT, not fix
[ ] Never write to Charlie_Kirk.txt
[ ] Never remove pre-existing page content
[ ] Do not run site-wide deploy unless operator asks
```

---

## Verification — prove the SVG is actually visible

Writing the file and embed is **not** done. Run three gates in order.

### Gate 1 — every embed points at a real file (instant, always)

```bash
cd {ROOT_DIR}/site/docs/Charlie/Text_Messages
for f in kill-me-*.mdx; do
  ref=$(grep -o '/img/km-timelines/[^"]*\.svg' "$f" | head -1)
  [ -z "$ref" ] && { echo "NO-IMG: $f"; continue; }
  [ -f "{ROOT_DIR}/site/internals/static$ref" ] \
    && echo "OK   $f -> $ref" || echo "MISS $f -> $ref"
done
```

Every line `OK` (catches typos like `km-3` vs `km-03` before a deploy cycle). Also confirm each SVG is non-empty and starts with `<svg` or `<?xml` (a zero-byte file returns 200 and renders nothing).

### Gate 2 — the site builds

```bash
cd {ROOT_DIR}/site && npm run build
ls {ROOT_DIR}/site/build/img/km-timelines/
```

MDX errors fail the deploy, not loudly. A chart missing from `site/build/img/…` is in the wrong static dir: fix the location, not the page.

### Gate 3 — live site; don't confuse "stale" with "broken"

GitHub Pages build+deploy takes ~**4 minutes**; meanwhile the live site serves the **previous** deploy (SVG 404 and no `<img>` in the HTML, indistinguishable from a real bug). Always check first:

```bash
cd {ROOT_DIR} && gh run list --limit 5
```

- `in_progress` → **nothing is wrong**; wait, re-test, fix nothing.
- `completed failure` → `gh run view <id> --log-failed`; suspect `<!-- -->` or a `style="…"` string in an `.mdx`.
- `completed success` → only now is a 404 a real bug.

After **your** commit's run succeeds:

```bash
for n in 01 02 03 04 05 06 07 08 09 10 11 12 13; do
  printf "km-%s: " "$n"
  curl -s -o /dev/null -w "svg=%{http_code}/%{size_download}b " \
    "https://whoassassinatedcharliekirk.com/img/km-timelines/km-$n-timeline.svg"
  page=$(basename $(ls {ROOT_DIR}/site/docs/Charlie/Text_Messages/kill-me-$n-*.mdx | head -1) .mdx)
  echo "page_refs=$(curl -s "https://whoassassinatedcharliekirk.com/Charlie/Text_Messages/$page" | grep -c "km-$n-timeline.svg")"
done
```

Pass: `svg=200` with non-zero bytes, content type `image/svg+xml` (`text/html` = the 404 page), and `page_refs` ≥ 1. `page_refs=0` on a successful deploy = the embed never reached the built page: re-check Gate 1 and the embed rules.

**Concurrent pushes cancel each other**: `.github/workflows/pages.yml` sets `concurrency: cancel-in-progress: true` on the `pages` group, so a quick second push kills the first deploy. If a change vanished, look for a `cancelled` run and push again (an empty commit suffices) rather than editing files.

---

## Acceptance criteria (when eventually run)

1. `{ROOT_DIR}/timeslines.csv` exists with columns `event_key,event,path_to_cvg,description`.
2. Every new chart lives under `site/internals/static/img/…` (one copy, no `site/static/` duplicate), reachable as `/img/…`.
2a. **Verified visible**: all three gates pass (file on disk; clean build with the chart in `site/build/img/…`; after deploy, live `200` `image/svg+xml` non-zero and the live page HTML references it). Unconfirmed on the live site = not done.
3. Every page needing a timeline embeds a registry SVG or has a documented **D** reason (internal log OK).
4. No duplicate `event_key`s; similar events cross-reference in `description`.
5. No existing investigative claims deleted.
6. Charts focused (**hard trim**): no near-zero deserts; ~≥95% of mass in the domain; ~3–5 day mass uses 4–6 bars/day and compact width; SEPT 8–12 operational pages use finer time when appropriate.
7. Chart pages have "best understanding" prose above and timing quotes below; the prose's working range matches the **trimmed** domain.
8. Embeds use `width:auto` + capped `maxWidth` (or equivalent).

---

## Related prior art

- Example MDX embeds: `site/docs/Charlie/Text_Messages/kill-me-*.mdx`
- Example SVGs: `site/internals/static/img/km-timelines/*.svg`
- First-pass research dumps: `tmp/kill_me_research/` (private)
- Site config: `site/docusaurus.config.ts` → `staticDirectories: ["internals/static"]`

END OF PROMPT — do not run until instructed.
