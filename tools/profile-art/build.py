#!/usr/bin/env python3
"""Regenerate every profile artwork SVG into the repository root.

    python3 tools/profile-art/build.py

Requires nothing but the standard library. The stats baked into the artwork
(repo count, stars, contributions, the weekly series, the language donut) are a
snapshot — see README.md in this folder for how to refresh them.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

from gen_a import hero, about          # noqa: E402
from gen_b import stack, connect       # noqa: E402
from gen_c import card_ids             # noqa: E402

FILES = {
    "hero.svg": hero,
    "about-life.svg": about,
    "stack.svg": stack,
    "connect.svg": connect,
    "id-dashboard.svg": card_ids,
}

if __name__ == "__main__":
    for name, fn in FILES.items():
        path = os.path.join(ROOT, name)
        svg = fn()
        with open(path, "w") as fh:
            fh.write(svg)
        print(f"wrote {name:20} {len(svg)/1024:6.1f} KB")
