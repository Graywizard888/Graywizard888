"""stack.svg — the tech-stack card: orbit shortlist + grouped chips.

The contact banner used to live here as one card of four tiles; it is four tappable
tickets now, in gen_contact.py.
"""
from gen_common import *
from gen_anim import style_block
from gen_stack import GROUPS, N_CHIPS, ORBIT_KEYS, STACK_CSS, core, flow, orbit

W_SIDEBAR = 386            # x of the divider; the chips own everything right of it
CLUSTER_X = 214            # the shortlist's centre
COL_X, COL_W = 404, 752    # right column: origin and the wrap width chips flow in


def stack(H=540):
    """One card, two readings.

    Left: the shortlist — six medals on three rings around a terminal core, for
    "who is this guy at a glance". Right: the receipts — every tool, grouped by
    discipline, sized from the monospace advance so nothing has to be measured by
    a browser at paint time.

    The card is drawn at whatever height it is handed: the groups are laid out
    first and then spread to fill the column, so a taller card means more air,
    never an empty band at the bottom.
    """
    W = 1200
    top, bot = 124, H - 52                      # the band both columns live in
    cy = (top + bot) / 2 + 6                    # the cluster sits a hair low: the
                                                # caption under it is part of it
    defs = [
        '<linearGradient id="sBg" x1="0" y1="0" x2=".6" y2="1">'
        f'<stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG0}"/></linearGradient>',
        '<linearGradient id="sEdge" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{GREEN}" stop-opacity=".55"/>'
        f'<stop offset=".35" stop-color="#22303f"/><stop offset=".65" stop-color="#22303f"/>'
        f'<stop offset="1" stop-color="{CYAN}" stop-opacity=".5"/></linearGradient>',
        '<pattern id="sScan" width="4" height="4" patternUnits="userSpaceOnUse">'
        '<rect width="4" height="1" fill="#000" opacity=".35"/></pattern>',
        f'<clipPath id="sClip"><rect width="{W}" height="{H}" rx="16"/></clipPath>',
    ]
    core_defs, core_body = core(CLUSTER_X, cy, 44, 27)
    defs.append(core_defs)

    L_ = [R(0, 0, W, H, fill="url(#sBg)", rx=16)]
    for x in range(60, W, 60):
        L_.append(L(x, 0, x, H, stroke="#0f1a24", sw=1, opacity=.7))
    L_.append(R(0, 0, W, H, fill="url(#sScan)", opacity=.28))
    L_.append(hud_corners(10, 10, W - 20, H - 20, GREEN, 22, 2, .45, cls=None))

    # ---- header
    L_.append(R(40, 33, 5, 16, fill=GREEN, rx=2.5))
    L_.append(T(58, 47, "// tech_stack", 12.5, CYAN, weight=700, ls=2.2))
    L_.append(T(58, 88, "Tools I build with", 30, TEXT, weight=700, family=SANS, ls=-.4))
    L_.append(T(58, 110, "every chip below has shipped in a public repo", 11.5, MUTED))
    L_.append(T(W - 40, 47, "built with · shipped in", 11, MUTED, anchor="end", ls=1))
    L_.append(T(W - 40, 88, f"{N_CHIPS} tools · {len(GROUPS)} groups", 13, SOFT,
                anchor="end", weight=600))
    L_.append(L(W_SIDEBAR, top - 4, W_SIDEBAR, bot + 4, stroke=STROKE, sw=1))

    # ---- left: the shortlist, orbiting
    # (rx, ry, tilt, colour, seconds per lap). The three rings are the same shape
    # at three tilts, which is what makes the group read as one system. The widest
    # ring plus a medal has to stop short of both the divider and the card edge,
    # which is what fixes rx at 146 for CLUSTER_X = 214.
    ring_geom = [(146, 90, 0, CYAN, 34.0), (140, 84, 60, GREEN, 40.0),
                 (134, 78, 120, VIOLET, 46.0)]
    # The medals are dealt round-robin over the rings and given an even share of
    # the compass, starting at the top — so the count is free to change without
    # the layout needing a second thought.
    per = [[] for _ in ring_geom]
    n = len(ORBIT_KEYS)
    for i, key in enumerate(ORBIT_KEYS):
        per[i % len(ring_geom)].append((key, -1.5708 + i * 6.2832 / n))
    for i, (rx, ry, rot, col, dur) in enumerate(ring_geom):
        L_.append(G(orbit(CLUSTER_X, cy, rx, ry, rot, per[i], col, dur, f"sOrb{i}"),
                    cls="fade-in", style=f"animation-delay:{.1 + i * .18:.2f}s"))
    # the dashed circle the medals are "launched" from, and the core
    L_.append(C(CLUSTER_X, cy, 74, fill="none", stroke=GREEN, sw=1,
                opacity=.24, style="stroke-dasharray:3 6"))
    L_.append(core_body)
    L_.append(T(CLUSTER_X, bot + 2, "the shortlist · everything else is on the right",
                11, MUTED, anchor="middle"))

    # ---- right: the groups, laid out then spread to fill the column
    rows_h = []
    for _, _, keys in GROUPS:
        _, h, _ = flow(COL_X, 0, COL_W, keys, animate=False)
        rows_h.append(24 + h)                                # label + chip rows
    # One gap size for the whole column, capped so a tall card breathes rather
    # than sprouting canyons, then the block is centred in the band it was given.
    free = (bot - top) - sum(rows_h)
    gap = min(26.0, max(12.0, free / (len(GROUPS) - 1)))
    y0 = top + (free - gap * (len(GROUPS) - 1)) / 2
    for i, (hgt, (label, accent, keys)) in enumerate(zip(rows_h, GROUPS)):
        y = y0 + gap * i + sum(rows_h[:i])
        markup, _, _ = flow(COL_X, y + 26, COL_W, keys, delay0=.4 + i * .3)
        L_.append(G(
            R(COL_X, y + 4, 14, 3, fill=accent, rx=1.5, opacity=.9) +
            T(COL_X + 22, y + 11, label, 11, SOFT, weight=700, ls=1.8) +
            markup,
            cls="fade-up", style=f"animation-delay:{.25 + i * .14:.2f}s"))

    # ---- footer
    L_.append(L(40, H - 34, W - 40, H - 34, stroke=STROKE, sw=1))
    L_.append(T(56, H - 14,
                "> 6 languages · android tooling · terminal automation · agents on call",
                11.5, MUTED))
    L_.append(T(W - 56, H - 14, "release builds on request", 11.5, DIM, anchor="end"))

    D, B = "\n".join(defs), "\n".join(L_)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Tech stack">'
            f'<defs>{D}' + style_block(extra=STACK_CSS) + '</defs>' + G(B, clip="url(#sClip)") +
            R(0.5, 0.5, W - 1, H - 1, rx=16, stroke="url(#sEdge)", sw=1) + '</svg>')
