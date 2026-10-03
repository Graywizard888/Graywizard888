"""Every card value a machine can know, loaded from builds.json.

    PROFILE  account-level numbers: public repos, stars earned, contributions, gists
    BUILDS   one tuple per repository card, in draw order
    fmt()    thousands separator - the cards draw 1,042, not 1042

`refresh_stats.py` rewrites the machine-owned fields from the GitHub API and
`build.py` redraws everything from here. gen_common star-imports this module, so
every generator can reach PROFILE without importing it explicitly.
"""
import json
import os

DATA_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "builds.json")

with open(DATA_JSON, encoding="utf-8") as _fh:
    _DOC = json.load(_fh)

PROFILE = _DOC["profile"]

# (repo, display name, language, language colour, licence, description,
#  stars, forks, pulls, size_kb, last push)
BUILDS = [(r["repo"], r["name"], r["language"], r["language_color"], r.get("license"),
           r["description"], r["stars"], r["forks"], r["pulls"], r["size_kb"], r["pushed"])
          for r in _DOC["repos"]]


def uptime_days():
    """Days on GitHub since the account was created.

    Computed at build time, so it is only as current as the last build - which is
    the daily workflow. Like the "pushed N ago" labels this shifts by one every
    day, so it never adds a commit the workflow was not already making.
    """
    from datetime import date

    return (date.today() - date.fromisoformat(PROFILE["created_at"])).days


def fmt(n):
    """934 -> '934', 1042 -> '1,042'. odometer() draws str(value) char by char,
    so counts must already carry their comma."""
    return f"{int(n):,}"
