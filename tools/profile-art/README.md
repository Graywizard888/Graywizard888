# profile-art

Generator for the animated SVG cards used by the profile README.

```bash
python3 tools/profile-art/build.py     # rewrites the *.svg files in the repo root
```

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
