#!/usr/bin/env python3
"""Regenerate every profile artwork SVG into the repository root.

    python3 tools/profile-art/build.py

Requires nothing but the standard library. Card sizes live in SIZES below —
each card recomposes its layout to fill whatever height it is given, so tuning
one is a one-line change.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, HERE)

from gen_a import hero, about          # noqa: E402
from gen_b import stack, connect       # noqa: E402
from gen_c import card_ids             # noqa: E402

# 1200 x <height>. Hero is the headline; the supporting cards step up in proportion.
SIZES = {
    "hero": 640,
    "about-life": 560,
    "stack": 392,
    "id-dashboard": 500,
    "connect": 300,
}

if __name__ == "__main__":
    cards = {
        "hero.svg":         hero(SIZES["hero"]),
        "about-life.svg":   about(SIZES["about-life"]),
        "stack.svg":        stack(SIZES["stack"]),
        "id-dashboard.svg": card_ids(SIZES["id-dashboard"]),
        "connect.svg":      connect(SIZES["connect"]),
    }
    for name, svg in cards.items():
        with open(os.path.join(ROOT, name), "w") as fh:
            fh.write(svg)
        print(f"wrote {name:20} {len(svg)/1024:6.1f} KB")
