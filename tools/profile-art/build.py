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

from gen_a import hero, about, VIDEO_SHIFT   # noqa: E402
from gen_b import stack, connect       # noqa: E402
from gen_m import (hero_mobile, about_mobile, stack_mobile,   # noqa: E402
                   connect_mobile)
from gen_p import build_card, BUILDS                    # noqa: E402

# 1200 x <height>. Hero is the headline; the supporting cards step up in proportion.
SIZES = {
    # hero = 640 of layout + the intro-video band above it
    "hero": 640 + VIDEO_SHIFT,
    "about-life": 560,
    "stack": 392,
    "connect": 300,
}

if __name__ == "__main__":
    cards = {
        "hero.svg":         hero(SIZES["hero"]),
        "about-life.svg":   about(SIZES["about-life"]),
        "stack.svg":        stack(SIZES["stack"]),
        "connect.svg":      connect(SIZES["connect"]),
    }
    # Phone variants: 720px wide (so text renders ~2x bigger on a 360px screen)
    # with the heavy motion removed. Served via <picture><source media="...">.
    mobile = {
        "hero-mobile.svg":         hero_mobile(),
        "about-life-mobile.svg":   about_mobile(),
        "stack-mobile.svg":        stack_mobile(),
        "connect-mobile.svg":      connect_mobile(),
    }
    # Personal-build cards: one tappable image per repo, desktop + phone variants
    for i, spec in enumerate(BUILDS):
        mobile[f"builds/p{i+1:02d}-mobile.svg"] = build_card(i, spec, wide=False)
        cards[f"builds/p{i+1:02d}.svg"] = build_card(i, spec, wide=True)

    for name, svg in list(cards.items()) + list(mobile.items()):
        with open(os.path.join(ROOT, name), "w") as fh:
            fh.write(svg)
        print(f"wrote {name:24} {len(svg)/1024:6.1f} KB")
