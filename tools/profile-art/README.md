# profile-art

Generator for the animated SVG cards used by the profile README.

```bash
python3 tools/profile-art/build.py     # rewrites the *.svg files in the repo root
```

## Card heights

Every card takes a height argument and recomposes its layout to fill it — taller
never means emptier. `build_final.py` shows the values currently in use:

| Card | Function | Current | What a taller card does |
|:---|:---|---:|:---|
| `hero.svg` | `hero(H)` | **640** | terminal earns extra `gh repo list` / `gist list` output, boot log appears, wordmark + equaliser scale |
| `about-life.svg` | `about(H)` | **560** | capability bars and life rows spread, footer pins to the bottom edge |
| `stack.svg` | `stack(H)` | **392** | the two marquees move to the top/bottom edges |
| `id-dashboard.svg` | `card_ids(H)` | **500** | *not currently linked* — ID card + dashboard, kept in reserve |
| `connect.svg` | `connect(H)` | **300** | contact tiles centre, footer pins to the bottom edge |

Any value from ~420 to ~800 works for the hero; the others scale proportionally.
Because the README sets `width="100%"` and the SVG carries no CSS height, the
rendered height follows the intrinsic aspect ratio — so changing `H` is all it takes.

* `gen_common.py` — design tokens (palette, fonts), SVG primitives, matrix-rain
  and odometer helpers.
* `gen_anim.py` — the CSS/keyframes library. Pure CSS animation, no JavaScript,
  which is what lets GitHub render these inside an `<img>`.
* `gen_a.py` → `hero.svg`, `about-life.svg`
* `gen_b.py` → `stack.svg`, `connect.svg`
* `gen_c.py` → `id-dashboard.svg` (ID card + dashboard) — **currently not
  linked from README.md**, see the note below

## Refreshing the numbers

The dashboard is a snapshot, not a live feed. To update it:

| Where | What |
|:---|:---|
| `gen_a.py` | the "12 public repos · 309 stars · 1,041 contributions" HUD line |
| `gen_c.py` | `REPOS`, `STARS`, `CONTRIB`, the `LANGS` donut and the `WEEKLY` series |

Grab the current values with:

```bash
gh api users/Graywizard888 --jq '{public_repos, followers}'
gh api "users/Graywizard888/repos?per_page=100" --jq '[.[].stargazers_count] | add'
gh api graphql -f query='{user(login:"Graywizard888"){contributionsCollection{contributionCalendar{
  totalContributions weeks{contributionDays{contributionCount}}}}}}'
```

## Design notes

Everything is drawn with plain shapes and mono/sans font stacks (`JetBrains Mono`
→ `Fira Code` → `Consolas` → `Liberation Mono` → `monospace`), so the cards look
right on GitHub without shipping a webfont. Bars, odometers and typed lines all
animate from a *translated* group, so their static state is the finished card.


## Mobile variants

`gen_m.py` builds a second set of cards at **720px wide** (`hero-mobile.svg`,
`about-life-mobile.svg`, `stack-mobile.svg`,
`connect-mobile.svg`). The README serves them through `<picture>`:

```html
<picture>
  <source media="(max-width: 820px)" srcset="./hero-mobile.svg?v=1">
  <img src="./hero.svg?v=1" alt="..." width="100%"/>
</picture>
```

Why they exist:

* **Legibility.** A 1200px card shown on a 360px phone is scaled to ~0.3x, which
  turns 12.5px text into ~4px. The 720px cards only scale ~0.5x, so the same
  nominal size renders roughly **twice as large**; body text sits at 20-28px.
* **Performance.** The heavy motion is gone: the rain is drawn once and never
  repainted, there are no marquees, and only two small dots blink. Everything
  else finishes within ~2s.
* **Whitespace.** Fewer rows per view, tighter leading, and stat tiles instead of
  a dense terminal.

GitHub keeps the `media` attribute and rewrites the relative `srcset` to a raw
URL on the rendered page, so this works on the profile without any hosting.
`media="(max-width: 820px)"` targets phones in portrait; tablets and desktop get
the full cards.


## Personal-build cards

`gen_p.py` renders one tappable card per repository into `builds/`. The
information layout follows the github-readme-stats pin card — repo name,
description, language, stars, forks — in the profile's terminal style, extended
with pull requests, licence and last-push age.

**Two shapes, one design:**

| Variant | Canvas | Used by | Notes |
|:---|:---|:---|:---|
| `p01.svg` … | **1012 x 212** | `<img width="100%">` | Wide card laid out for GitHub's full content column, so it renders ~1:1 and the type stays readable. Carries the shimmer sweep. |
| `p01-mobile.svg` … | **480 x 236** | `media="(max-width: 820px)"` | Narrow card, larger relative type; a 360px phone renders it at ~0.75x. Shimmer removed, so it has **zero perpetual animation**. |

Cards use `width="100%"`, are stacked one per row, and each is wrapped in its
own `<a href>` so tapping anywhere on it opens the repository (GitHub strips
`<map>`/`usemap`, so per-region taps inside a single image are not possible).

```html
<a href="https://github.com/Graywizard888/Enhancify"><picture><source media="(max-width: 820px)" srcset="./builds/p01-mobile.svg?v=1"><img src="./builds/p01.svg?v=1" alt="Enhancify — 201 stars, 11 forks, 30 PRs, Shell, unlicensed" width="100%"></picture></a>
```

> **Keep each card on a single line.** GitHub's markdown HTML-block handling
> breaks a multi-line `<a><picture>` apart: the `<picture>` inside the anchor
> comes out empty, the `<img>` lands outside the link, and GitHub then
> auto-links the orphaned image to the `.svg` file itself — so tapping a card
> opens the artwork instead of the repository. One line, no newlines inside the
> block, and the anchor wraps everything as intended.

## Card data: `builds.json`

`builds.json` is the single source of truth for every number a machine can know.
`card_data.py` loads it and `gen_common.py` re-exports it, so every generator
gets `PROFILE`, `BUILDS` and `fmt()` from its usual `from gen_common import *`.

| Field | Owner |
|:---|:---|
| `profile`: `public_repos`, `stars`, `contributions`, `gists`, `created`, `created_at` | **machine** — rewritten by `refresh_stats.py` |
| `repos`: `stars`, `forks`, `pulls`, `language`, `license`, `size_kb`, `pushed` | **machine** — rewritten by `refresh_stats.py` |
| `profile.login` | derived from the repository owner |
| `repos`: `repo`, `name`, `description`, `language_color` | **you** — editorial, hand-tuned for the canvas and the neon palette |

### The account numbers

`PROFILE` feeds the whoami banner (`hero.svg`, `hero-mobile.svg`). Three things
about it are deliberate:

* **`stars` includes forks.** Terminal_EX is a fork with 87 stars on it and is
  presented as one of the build cards, so its stars belong in the headline.
  Counting non-forks only would read 221 instead of 309.
* **`contributions` is all-time**, not the rolling 365-day figure — that is what
  the card has always shown. It is summed year by year with GraphQL, and
  `contributionsCollection` is capped at a one-year span whose **both endpoints
  are inclusive** (a query for `[D, D+1)` returns day D *and* day D+1), so the
  chunks step apart by a day. Overlapping them silently double-counts every
  anniversary day.
* **The hero's `gh repo list` block is generated from `BUILDS`** (top five by
  stars, ties in file order), so it can never contradict the cards below it.

* **`uptime N days`** is computed by `card_data.uptime_days()` from
  `profile.created_at`, not stored. It is the one number that changes with the
  clock rather than with the API, so it shifts by exactly one per day — the same
  cadence as the `pushed N ago` labels, meaning it never adds a commit the daily
  workflow was not already making.

Still hand-written, because they are prose or name specific items rather than
count things: the gist/script filenames, the commit hash and the `last push:`
line.

`refresh_stats.py` never touches the editorial fields, and `build.py` is
deterministic: cards whose facts did not change come out byte-identical, so a
refresh commit only contains the cards that actually moved.

```bash
# refresh the counts, then redraw (a token avoids API rate limits; the
# contributions total needs it - GraphQL cannot be called anonymously)
GITHUB_TOKEN=$(gh auth token) python3 tools/profile-art/refresh_stats.py
python3 tools/profile-art/build.py           # writes all 22 SVGs
python3 tools/profile-art/refresh_stats.py --dry-run    # preview the diff only
```

Without a token the repo counts still refresh but the contributions total is left
alone rather than reported as zero.

It also rewrites the `alt="…"` text of every card in `README.md`, which carries
the same counts for screen readers, so the artwork and the alt text cannot drift
apart. Two details it handles on purpose:

* **`Gists_Collection` reports `language: null`** on the API. A null language
  means "undetected", not "no language", so the refresher keeps whatever the
  card already says (Lua) rather than blanking it.
* **`language_color`** is a palette choice, not data: GitHub's own colours are
  unreadable on graphite (Lua is `#000080`). The colour is only re-picked from
  `LANG_COLORS` when the detected language itself changes.

`.github/workflows/refresh-cards.yml` runs the two commands daily at 04:20 UTC
and commits the result — that is what makes the counts live. Scheduled
workflows run on the default branch only, so it starts working once this branch
is merged; `workflow_dispatch` runs it by hand from the Actions tab.

To add or remove a repo: edit `repos` in `builds.json` (add the editorial fields
by hand, let the refresher fill the rest), re-run `build.py`, then add/remove the
matching single-line `<a href>` block in `README.md`. Delete any orphaned
`builds/pNN*.svg` files.

## The intro clip: its own card

`intro.svg` / `intro-mobile.svg` are the portfolio's ten-second intro clip as a
standalone card, sitting directly above the hero. GitHub strips every form of
`<video>` and `<iframe>` from markdown, so the clip is rebuilt as an SVG
one-shot: `gen_v.panel()` embeds the real frames as base64 `<image>` layers and
stacks them with per-frame `opacity` keyframes (`steps(1, end)`,
`iteration-count: 1`, `forwards`). The run ends on the last frame with a dimmed
shade and a centred play button, and the card is wrapped in a link so tapping it
reloads the README and replays the clip.

**Both variants really play.** The card used to live inside the hero and phones
were only ever given `mode="poster"` — a still with a play button on it — so on a
phone the clip looked broken. The phone card now plays its own lighter cut
(`variant="mobile"`, `assets/intro/mobile/`: 150 frames, 15 fps, q30) inside a
panel scaled from 532 to 656 px, drawn at 720 wide, so a 360 px screen renders it
at ~0.5x and the type still reads.

**Both cuts now run at the source file's own frame rate.** The clip is 1280x720 at
24 fps; the first cut decimated it to 8 fps (desktop) and 6 fps (phone), which is
what made playback look choppy. The desktop set is now the file's full 24 fps at
480x270 — exactly the panel size, so nothing is upscaled — and the phone set is
15 fps at 400x225.

**This is the one card that ignores `prefers-reduced-motion`.** Every other card
carries `style_block()`'s global `animation: none !important` guard; the intro
passes `reduced_motion=False`. Reason: a ten-second one-shot that settles on a
still is not the kind of motion that switch exists to stop, it was explicitly
asked to play, and with the guard on, a device that enables reduce-motion (quite
common on phones) silently showed a frozen poster — which is exactly what "the
video is not playing" looks like. Each SVG is its own document inside `<img>`, so
the exception cannot leak to other cards.

Frame sets:

| Variant | Directory | Frames | Size |
|:---|:---|:---|:---|
| desktop | `assets/intro/` | 240 @ 24 fps (the file's rate), 480x270 q30 | ~3.1 MB |
| mobile | `assets/intro/mobile/` | 150 @ 15 fps, 400x225 q30 | ~1.6 MB |

`gen_v.load(variant)` reads each set's `meta.json` for fps/frame count and falls
back to the desktop cut if a mobile one is missing, so re-cutting needs no code
change:

```bash
# only when the source clip changes; needs imageio-ffmpeg (system ffmpeg may be absent)
# desktop: the file's own 24 fps, cut at exactly the panel size (no upscale)
python3 tools/profile-art/make_frames.py --fps 24 --width 480 --height 270 --quality 30
# phone: lighter frame count, smaller canvas
python3 tools/profile-art/make_frames.py --fps 15 --width 400 --height 225 --quality 30 \
        --out assets/intro/mobile
python3 tools/profile-art/build.py
```

`make_frames.py` is a dev tool — `build.py` never touches the video, it only
reads the already-cut frames. Any renderer that ignores CSS animation shows the
poster frame with the play button, which is the state the sequence settles into.

Weight is the cost of this trick: one bitmap per frame means no temporal
compression, so `intro.svg` is ~3.1 MB and `intro-mobile.svg` ~1.6 MB, against a
hero that is back down to ~48 KB. Browsers cache them, and phones request the
lighter cut only. The levers, if that ever needs to shrink: `--fps`, `--quality`,
or the canvas size in `make_frames.py`.

## Cards that are kept but not linked

`id-dashboard.svg` / `id-dashboard-mobile.svg` — the developer-ID + dashboard
card, drawn by `gen_c.py` and `gen_m.ids_mobile()` — were removed from
`README.md` because the card sat directly under the tech-stack banner. `build.py`
no longer writes them, so nothing regenerates or re-commits them.

To bring the card back: re-add its two entries in `build.py`, run it, and paste
the matching `<picture>` block back into the README. Delete `gen_c.py` and
`ids_mobile()` instead if it is gone for good.
