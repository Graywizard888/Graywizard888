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
| `id-dashboard.svg` | `card_ids(H)` | **500** | ID card gains the activity record (commits per year), donut and 26-week chart grow |
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
* `gen_c.py` → `id-dashboard.svg` (ID card + dashboard)

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
`about-life-mobile.svg`, `stack-mobile.svg`, `id-dashboard-mobile.svg`,
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

`gen_p.py` renders one tappable card per repository into `builds/`
(`p01.svg` … `p08.svg`, plus `-mobile` variants). The information layout follows
the github-readme-stats pin card — repo name, description, language, stars,
forks — restyled in the profile's terminal/cyber look and extended with the
**pull-request count, licence and last-push age**.

* Canvas is **480 x 236**, close to the pin-card proportions, so a 360px phone
  renders the card at ~0.75x instead of shrinking a 1200px banner to 0.3x.
* Desktop cards add a slow shimmer sweep and a pulsing index chip.
* Phone cards are byte-for-byte the same artwork with the shimmer removed —
  **zero perpetual animation**; only the load-time counter roll plays.

GitHub strips `<map>`/`usemap` image maps, so per-region taps inside one banner
are impossible. Each card is linked individually instead, one per row at its
natural 480px width:

```html
<a href="https://github.com/Graywizard888/Enhancify"><picture>
  <source media="(max-width: 820px)" srcset="./builds/p01-mobile.svg?v=1">
  <img src="./builds/p01.svg?v=1" alt="Enhancify — 201 stars, 11 forks, 30 PRs, Shell, unlicensed">
</picture></a>
```

To refresh after a repo gains stars, edit `BUILDS` in `gen_p.py`
`(repo, name, language, language_colour, licence, description, stars, forks, pulls, size_kb, last_push)`,
re-run `build.py`, and update the `alt` text in the README.
