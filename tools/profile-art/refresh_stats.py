#!/usr/bin/env python3
"""Refresh the Personal-build card data straight from the GitHub API.

    GITHUB_TOKEN=$(gh auth token) python3 tools/profile-art/refresh_stats.py
    python3 tools/profile-art/refresh_stats.py --dry-run     # show, don't write

What it updates in builds.json (the numbers a machine can know):

    stars, forks, pulls, language, license, size_kb, pushed

What it deliberately leaves alone (editorial, hand-tuned for the canvas):

    repo, name, description, language_color

  * `description` stays yours - the API blurbs are longer than the card can
    hold, and build_card draws the first two wrapped lines only.
  * `language_color` is a neon-palette choice; GitHub's official colours
    (Lua is #000080) are unreadable on the graphite background. When the
    detected language does change, the colour is re-picked from LANG_COLORS.
  * a repo whose language GitHub cannot detect (Gists_Collection reports null)
    keeps the language that is already on the card.

It also rewrites the `alt="..."` text of each card in README.md, which carries
the same counts for screen readers, so the two can never drift apart.

Only the standard library is required - no pip install in CI. Exit code is 0
when at least one repo refreshed, 1 when every request failed.
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
BUILDS_JSON = os.path.join(HERE, "builds.json")
README = os.path.abspath(os.path.join(HERE, "..", "..", "README.md"))
API = "https://api.github.com"

# GitHub's dark palette is unusable on this canvas, so each language gets an
# on-brand colour. Unknown languages fall back to the muted slate.
LANG_COLORS = {
    "Shell": "#89E051", "Bash": "#89E051", "Java": "#F89820", "Kotlin": "#A97BFF",
    "Python": "#4B8BBE", "Lua": "#7C8FFF", "JavaScript": "#F1E05A",
    "TypeScript": "#3178C6", "Rust": "#DEA584", "C": "#8B95A7", "C++": "#F34B7D",
    "CMake": "#DA3434", "Makefile": "#427819", "Go": "#00ADD8", "HTML": "#E34C26",
    "CSS": "#563D7C", "Ruby": "#701516", "PHP": "#4F5D95", "Dart": "#00B4AB",
}
LANG_DEFAULT = "#8B95A7"


def owner():
    """owner/repo of the current GitHub Actions run, else the profile owner."""
    slug = os.environ.get("GITHUB_REPOSITORY", "")
    return slug.split("/")[0] if "/" in slug else "Graywizard888"


def api_get(path, token=None):
    req = urllib.request.Request(
        API + path,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "refresh-stats",
            **({"Authorization": f"Bearer {token}"} if token else {}),
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def push_label(pushed_at, now=None):
    """'16d ago' / '4mo ago' / '1y ago', matching the existing card style."""
    if not pushed_at:
        return None
    now = now or datetime.now(timezone.utc)
    when = datetime.fromisoformat(pushed_at.replace("Z", "+00:00"))
    days = max(0, (now - when).days)
    if days < 1:
        return "today"
    if days < 30:
        return f"{days}d ago"
    if days < 365:
        return f"{max(1, round(days / 30.44))}mo ago"
    return f"{max(1, round(days / 365.25))}y ago"


def alt_text(row):
    return (f'{row["name"]} — {row["stars"]} stars, {row["forks"]} forks, '
            f'{row["pulls"]} PRs, {row["language"]}, {row.get("license") or "unlicensed"}')


def alt_pattern(repo):
    # one card == one line in README.md, so never let the match span a newline
    return re.compile(
        r'(<a href="https://github\.com/[^"]+/' + re.escape(repo) + r'"><picture>[^\n]*?alt=")[^"]*(")'
    )


def fetch(row, token):
    """Return the fresh values for one repo, or None if the request failed."""
    repo = row["repo"]
    try:
        data = api_get(f"/repos/{owner()}/{repo}", token)
        q = urllib.parse.urlencode({"q": f"repo:{owner()}/{repo} type:pr", "per_page": 1})
        pulls = api_get(f"/search/issues?{q}", token)["total_count"]
    except (urllib.error.URLError, urllib.error.HTTPError, KeyError, ValueError) as exc:
        print(f"  ! {repo}: {exc}")
        return None

    license_id = (data.get("license") or {}).get("spdx_id")
    if license_id in (None, "NOASSERTION"):
        license_id = None
    fresh = {
        "stars": data.get("stargazers_count", row["stars"]),
        "forks": data.get("forks_count", row["forks"]),
        "pulls": pulls,
        "license": license_id,
        "size_kb": data.get("size", row["size_kb"]),
        "pushed": push_label(data.get("pushed_at")) or row["pushed"],
    }
    # keep the card's language when GitHub reports null (mixed/unrecognised repo)
    lang = data.get("language")
    if lang:
        fresh["language"] = lang
        if lang != row["language"]:
            fresh["language_color"] = LANG_COLORS.get(lang, LANG_DEFAULT)
    return fresh


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="print the diff, write nothing")
    args = ap.parse_args()
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

    with open(BUILDS_JSON, encoding="utf-8") as fh:
        doc = json.load(fh)

    changed, failed = [], []
    for row in doc["repos"]:
        fresh = fetch(row, token)
        if fresh is None:
            failed.append(row["repo"])
            continue
        for key, value in fresh.items():
            if row.get(key) != value:
                changed.append(f'  {row["repo"]}.{key}: {row.get(key)!r} -> {value!r}')
                row[key] = value

    if len(failed) == len(doc["repos"]):
        print("every request failed - nothing written")
        return 1

    if not changed:
        print("all card stats already current")
    else:
        print(f"{len(changed)} field(s) changed:")
        print("\n".join(changed))

    if args.dry_run:
        print("(dry run - builds.json and README.md untouched)")
        return 0

    # Only touch builds.json when a value actually moved: rewriting it every run
    # would bump `generated` daily and commit noise on days nothing changed.
    # (A quiet day must produce an empty commit - see the workflow's diff check.)
    if changed:
        doc["generated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with open(BUILDS_JSON, "w", encoding="utf-8") as fh:
            json.dump(doc, fh, indent=2, ensure_ascii=False)
            fh.write("\n")

    # keep the screen-reader alt text in step with the drawn counts
    with open(README, encoding="utf-8") as fh:
        readme = fh.read()
    touched = 0
    for row in doc["repos"]:
        readme, n = alt_pattern(row["repo"]).subn(
            lambda m: m.group(1) + alt_text(row) + m.group(2), readme)
        if n == 0:
            print(f'  ! README.md: no card line found for {row["repo"]}')
        touched += n
    with open(README, "w", encoding="utf-8") as fh:
        fh.write(readme)
    print("builds.json updated" if changed else "builds.json untouched (counts unchanged)")
    print(f"README alt text: {touched} card(s) refreshed")

    return 0


if __name__ == "__main__":
    sys.exit(main())
