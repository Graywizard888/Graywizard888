#!/usr/bin/env python3
"""intro.svg / intro-mobile.svg - the intro clip as its own card.

The clip used to sit inside the hero. It lives on its own now, directly above the
hero, for two reasons: the hero is a link target in its own right, and phones
were only ever shown a still poster of the clip (their card carried no frames at
all), so the video looked broken on a phone.

Both variants actually play:

    intro.svg         1200 x H   the 8 fps desktop sequence
    intro-mobile.svg   720 x H   a lighter 6 fps cut, panel scaled to the width

One-shot playback is CSS: every frame is a stacked <image> and a keyframe
animation with `iteration-count: 1` + `fill-mode: forwards` reveals them in
order, HOLDS on the last frame, and the play button fades back in over it.

This card is also the single exception to the reduced-motion kill switch - see
gen_anim.style_block(reduced_motion=False). It is a ten-second one-shot that ends
on a still, and it was explicitly asked to play; every other card still honours
the switch.
"""
from gen_common import (BG0, BG1, CYAN, DIM, GREEN, GREEN_D, MUTED, PANEL, STROKE,
                        TEXT, C, G, L, R, T, hud_corners, rain)
from gen_anim import style_block

import gen_v

# ------------------------------------------------------------------ desktop
DESKTOP_W = 1200
PANEL_W = gen_v.WINDOW_W          # 532
PANEL_H = gen_v.WINDOW_H          # 366


def _backdrop(W, H, accent=GREEN, rain_cols=15, seed=11, rx=16):
    """Same graphite-and-grid backdrop the other wide cards use."""
    defs = [
        '<linearGradient id="iBg" x1="0" y1="0" x2=".7" y2="1">'
        f'<stop offset="0" stop-color="{BG1}"/><stop offset=".55" stop-color="#070c12"/>'
        f'<stop offset="1" stop-color="{BG0}"/></linearGradient>',
        '<radialGradient id="iGlow" cx=".5" cy=".5" r=".5">'
        f'<stop offset="0" stop-color="{accent}" stop-opacity=".20"/>'
        f'<stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>',
        '<pattern id="iScanLines" width="4" height="4" patternUnits="userSpaceOnUse">'
        '<rect width="4" height="1.1" fill="#000" opacity=".5"/></pattern>',
        f'<clipPath id="iClip"><rect width="{W}" height="{H}" rx="{rx}"/></clipPath>',
    ]
    body = [R(0, 0, W, H, fill="url(#iBg)", rx=rx)]
    step = 60 if W > 800 else 48
    for x in range(step, W, step):
        body.append(L(x, 0, x, H, stroke="#101d28", sw=1, opacity=.75))
    for y in range(40, H, 47):
        body.append(L(0, y, W, y, stroke="#101d28", sw=1, opacity=.75))
    body.append(rain(W, H, cols=rain_cols, chars_per_block=14, x0=-30, seed=seed))
    body.append(R(0, 0, W, H, fill="url(#iScanLines)", opacity=.28))
    body.append(hud_corners(12, 12, W - 24, H - 24, accent, 26, 2, .5, cls=None))
    return defs, body


def _wrap(W, H, defs, body, label, css="", rx=16):
    D, B = "\n".join(defs), "\n".join(body)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}" role="img" aria-label="{label}">'
            f'<defs>{D}' + style_block(css, reduced_motion=False) + '</defs>' +
            G(B, clip="url(#iClip)") +
            R(0.5, 0.5, W - 1, H - 1, rx=rx, stroke="#22303f", sw=1) + '</svg>')


def intro(H=520):
    """Wide intro card: header row, the player, a one-line hint."""
    W = DESKTOP_W
    defs, L_ = _backdrop(W, H)
    panel_x = (W - PANEL_W) // 2
    panel_y = (H - PANEL_H) // 2 + 10

    v_body, v_css, v_defs, _ = gen_v.panel(panel_x, panel_y, mode="play")
    defs += v_defs
    L_.append(v_body)

    # header row
    y_head = panel_y - 34
    L_.append(C(46, y_head - 4, 8, fill="none", stroke=GREEN, sw=1.4, cls="pulse-soft"))
    L_.append(C(46, y_head - 4, 4, fill=GREEN, cls="pulse"))
    L_.append(T(62, y_head, "// intro.play", 15, GREEN, weight=600, ls=1.6))
    L_.append(T(W - 46, y_head, "graywizard.mp4 · silent · plays once on load",
                12, MUTED, anchor="end", ls=.8))

    # footer hint
    y_foot = panel_y + PANEL_H + 34
    L_.append(L(46, y_foot - 20, W - 46, y_foot - 20, stroke=STROKE, sw=1, opacity=.8))
    L_.append(T(46, y_foot, "▸ the play button stays in the middle — tap the card "
                            "to run the intro again", 12, DIM, ls=.4))
    L_.append(T(W - 46, y_foot, "tap = reload", 12, GREEN_D, anchor="end", ls=.8))

    return _wrap(W, H, defs, L_,
                 "Graywizard intro - a ten-second clip plays once, then shows a "
                 "play button in the middle; tap the card to replay it", v_css)


# ------------------------------------------------------------------ phone
MOB_W = 720


def intro_mobile():
    """Phone intro card: the clip plays here too, on its lighter frame set."""
    H = 672
    margin = 32
    scale = round((MOB_W - margin * 2) / PANEL_W, 4)     # 532 -> 656 wide
    panel_top = 118
    panel_x = (MOB_W - PANEL_W) // 2                     # drawn in its own space
    tx = margin - panel_x * scale                        # scales about the panel

    defs, L_ = _backdrop(MOB_W, H, rain_cols=9, seed=5, rx=20)

    v_body, v_css, v_defs, _ = gen_v.panel(panel_x, 0, mode="play", variant="mobile")
    defs += v_defs

    # header
    L_.append(C(54, 60, 11, fill="none", stroke=GREEN, sw=1.6, cls="pulse-soft"))
    L_.append(C(54, 60, 5.5, fill=GREEN, cls="pulse"))
    L_.append(T(78, 68, "// intro.play", 26, GREEN, weight=600, ls=1.2))
    L_.append(T(MOB_W - 32, 68, "silent", 20, MUTED, anchor="end", ls=1))

    L_.append(G(v_body, transform=f"translate({tx:.2f},{panel_top}) scale({scale})"))

    # footer
    y_foot = panel_top + PANEL_H * scale + 46
    L_.append(L(32, y_foot - 30, MOB_W - 32, y_foot - 30, stroke=STROKE, sw=1, opacity=.8))
    L_.append(T(32, y_foot, "▸ plays once · tap the card to replay", 21, DIM))
    L_.append(T(MOB_W - 32, y_foot + 30, "graywizard.mp4 · 10s · 60 frames", 18,
                MUTED, anchor="end", ls=.6))

    return _wrap(MOB_W, H, defs, L_,
                 "Graywizard intro - a ten-second clip plays once, then shows a "
                 "play button in the middle; tap the card to replay it", v_css, rx=20)
