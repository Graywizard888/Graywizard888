"""Mobile card variants: 720px wide so text lands at ~2x the rendered size of the
1200px cards on a phone, with the heavy motion removed (frozen rain, no marquees).

What stays is the motion that carries meaning: the stack card keeps its orbiting
medals and the pulse that walks along a row of chips, because on a phone those are
the only things saying "this is a live card, rebuilt from a real repo". Everything
animated here is revealed by CSS, so `prefers-reduced-motion` still turns the phone
cards fully static.

Served to phones via <picture><source media="(max-width: 700px)">.
"""
import math, random
from gen_common import *
from gen_stack import (GROUPS, N_CHIPS, ORBIT_KEYS, STACK_CSS, core, flow, orbit)
import gen_v
from gen_anim import style_block

W = 720
GROUP_GAP = 24                # between groups on the stack card (gen_stack)


def frame(H, accent=GREEN, rain_cols=9, seed=11):
    """Shared backdrop: gradient, grid, scanlines, frozen rain, HUD corners."""
    defs = [
        '<linearGradient id="mBg" x1="0" y1="0" x2=".6" y2="1">'
        f'<stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG0}"/></linearGradient>',
        '<pattern id="mScan" width="4" height="4" patternUnits="userSpaceOnUse">'
        '<rect width="4" height="1" fill="#000" opacity=".32"/></pattern>',
        f'<clipPath id="mClip"><rect width="{W}" height="{H}" rx="20"/></clipPath>',
    ]
    L_ = [R(0, 0, W, H, fill="url(#mBg)", rx=20)]
    for x in range(48, W, 48):
        L_.append(L(x, 0, x, H, stroke="#0f1a24", sw=1, opacity=.7))
    L_.append(rain(W, H, cols=rain_cols, chars_per_block=16, x0=-24, seed=seed, animate=False))
    L_.append(R(0, 0, W, H, fill="url(#mScan)", opacity=.3))
    L_.append(hud_corners(12, 12, W - 24, H - 24, accent, 30, 2.5, .5, cls=None))
    return defs, L_


def wrap(H, defs, body, label, extra_css=""):
    D, B = "\n".join(defs), "\n".join(body)
    # xmlns:xlink is declared even where nothing uses it: a stack card here puts
    # xlink:href on an <mpath> for Firefox's benefit, and an undeclared prefix is
    # a fatal XML error for an SVG loaded as an <img> — the card would not just
    # lose its animation, it would not render at all.
    return (f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="{label}">'
            f'<defs>{D}' + style_block(extra_css) + '</defs>' + G(B, clip="url(#mClip)") +
            R(1, 1, W - 2, H - 2, rx=20, stroke="#22303f", sw=2) + '</svg>')


# ------------------------------------------------------------------ HERO
def hero_mobile():
    H = 820
    defs, L_ = frame(H, GREEN, rain_cols=9, seed=5)
    defs += [
        '<linearGradient id="mName" x1="0" y1="0" x2="1" y2=".2">'
        f'<stop offset="0" stop-color="#8bf5b4"/><stop offset=".45" stop-color="{GREEN}"/>'
        f'<stop offset=".8" stop-color="{CYAN}"/><stop offset="1" stop-color="#60a5fa"/></linearGradient>',
        '<linearGradient id="mTerm" x1="0" y1="0" x2=".4" y2="1">'
        '<stop offset="0" stop-color="#101a24"/><stop offset="1" stop-color="#080e15"/></linearGradient>',
        '<linearGradient id="mBar" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{GREEN_D}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>',
        '<radialGradient id="mGlow" cx=".5" cy=".5" r=".5">'
        f'<stop offset="0" stop-color="{GREEN}" stop-opacity=".20"/>'
        f'<stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></radialGradient>',
    ]
    # status pill + REC
    L_.append(R(32, 34, 250, 46, fill="#0b1a14", rx=23, stroke=GREEN_D, sw=1.4, opacity=.92))
    L_.append(C(60, 57, 11, fill="none", stroke=GREEN, sw=1.4, cls="pulse-soft"))
    L_.append(C(60, 57, 5.5, fill=GREEN, cls="pulse"))
    L_.append(T(84, 64, "SYSTEM.ONLINE", 21, GREEN, weight=600, ls=1.4))
    L_.append(C(628, 57, 7, fill="#ff6b60"))
    L_.append(T(648, 64, "REC", 21, "#ff8f88", weight=600, ls=2))

    L_.append(T(32, 132, "graywizard@cyber:~$ whoami", 23, GREEN, opacity=.92))
    L_.append(f'<ellipse cx="300" cy="250" rx="330" ry="180" fill="url(#mGlow)"/>')
    L_.append(T(30, 226, "GRAYWIZARD", 76, "url(#mName)", weight=800, ls=1,
                cls="fade-in", style="animation-duration:1.2s"))
    L_.append(T(32, 288, "Coder · Gamer · System Architect", 30, "#d3e6f5",
                cls="fade-up", style="animation-delay:.3s"))
    L_.append(T(32, 332, "India (IST) · terminal-first", 26, MUTED,
                cls="fade-up", style="animation-delay:.45s"))

    # three stat tiles with the real numbers
    stats = [(fmt(PROFILE["public_repos"]), "public repos", GREEN),
             (fmt(PROFILE["stars"]), "stars earned", CYAN),
             (fmt(PROFILE["contributions"]), "contributions", VIOLET)]
    tw, gap = 208, 16
    for i, (val, label, col) in enumerate(stats):
        x = 32 + i * (tw + gap)
        L_.append(R(x, 380, tw, 104, fill=PANEL, rx=16, stroke=STROKE, sw=1.4))
        L_.append(R(x + 1, 380, tw - 2, 4, fill=col, rx=2, opacity=.85))
        L_.append(T(x + 20, 434, val, 40, TEXT, weight=700))
        L_.append(T(x + 20, 464, label, 19, MUTED))

    L_.append(T(32, 540, '> "Build. Break. Rebuild. Optimize."', 28, "#95f2b8", weight=500,
                cls="fade-up", style="animation-delay:.6s"))

    # compact terminal
    ty, th = 576, 186
    L_.append(R(32, ty, W - 64, th, fill="url(#mTerm)", rx=16, stroke=STROKE2, sw=1.4))
    L_.append(L(32, ty + 42, W - 32, ty + 42, stroke=STROKE, sw=1.2))
    for dx, col in ((54, RED), (76, AMBER), (98, "#28c840")):
        L_.append(C(dx, ty + 21, 7, fill=col))
    L_.append(T(W - 48, ty + 28, "zsh", 20, MUTED, anchor="end"))
    lines = [("$ neofetch --short", GREEN),
             ("os       Termux · Android 8+", "#c3d3e2"),
             ("shell    bash · lua · python", "#c3d3e2"),
             ("builds   scripts · TUIs · forks", "#c3d3e2")]
    for i, (txt, col) in enumerate(lines):
        L_.append(T(54, ty + 74 + i * 27, txt, 22, col, cls="fade-up",
                    style=f"animation-delay:{.5 + i * .12:.2f}s"))
    L_.append(T(54, ty + 176, "$", 22, GREEN))
    L_.append(R(72, ty + 160, 12, 20, fill=GREEN, cls="blink"))

    L_.append(L(32, 788, W - 32, 788, stroke=STROKE, sw=1))
    L_.append(T(32, 806, f"since {PROFILE['created']} · 4 mpv + lua scripts · MIT / GPL-3.0", 19, DIM))
    return wrap(H, defs, L_, "Graywizard — coder, gamer, system architect")


# ------------------------------------------------------------------ ABOUT / LIFE
def about_mobile():
    H = 1020
    defs, L_ = frame(H, CYAN, rain_cols=8, seed=9)
    defs += ['<linearGradient id="mBarA" x1="0" y1="0" x2="1" y2="0">'
             f'<stop offset="0" stop-color="{GREEN_D}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>']
    L_ += [panel(28, 28, W - 56, 446, title="// system.capabilities", tag="live", accent=GREEN)]
    L_.append(T(52, 122, "WHAT I BUILD", 38, TEXT, weight=700, family=None, cls="fs", ls=.3))
    L_.append(T(52, 156, "scripts · TUIs · extensions · forks", 21, MUTED))
    skills = [("Gaming", 95), ("Scripting / Automation", 88), ("Open Source", 82),
              ("Problem Solving", 90), ("Optimization", 85)]
    y = 190
    for i, (label, pct) in enumerate(skills):
        L_.append(T(52, y, label, 25, "#cfdcea", weight=500))
        L_.append(T(668, y, f"{pct}%", 25, CYAN, anchor="end", weight=600))
        L_.append(R(52, y + 16, 616, 12, fill="#16222e", rx=6))
        L_.append(G(R(0, 0, 616 * pct / 100, 12, fill="url(#mBarA)", rx=6, cls="grow-x",
                      style=f"animation-duration:1.4s;animation-delay:{.2 + i * .12:.2f}s"),
                    transform=f"translate(52,{y + 16})"))
        y += 54
    L_.append(T(52, 460, "> every one started as a personal annoyance.", 21, MUTED))

    L_ += [panel(28, 504, W - 56, 470, title="// life.outside.code", tag="24 cycles", accent=CYAN)]
    L_.append(T(52, 598, "LIFE OUTSIDE CODE", 38, TEXT, weight=700, family=None, cls="fs", ls=.3))
    L_.append(T(52, 632, "when the terminal closes", 21, MUTED))
    life = [("Gaming", "co-op nights & open worlds", GREEN),
            ("Audio pipeline tuning", "mpv equalizer: 5.1 / 7.1", CYAN),
            ("Relentless tinkering", "annoyance → script → repo", VIOLET),
            ("Coding when required", "free-time dev — usually required", AMBER)]
    ry = 686
    for i, (title, desc, col) in enumerate(life):
        L_.append(R(52, ry - 26, 56, 56, fill=col, rx=16, opacity=.14))
        L_.append(R(52, ry - 26, 56, 56, fill="none", rx=16, stroke=col, sw=1.6, opacity=.6))
        L_.append(C(80, ry + 2, 9, fill=col, opacity=.9))
        L_.append(T(128, ry, title, 27, TEXT, weight=600, cls="fade-up",
                    style=f"animation-delay:{.1 + i * .08:.2f}s"))
        L_.append(T(128, ry + 30, desc, 21, MUTED, cls="fade-up",
                    style=f"animation-delay:{.16 + i * .08:.2f}s"))
        ry += 76

    L_.append(L(28, 990, W - 28, 990, stroke=STROKE, sw=1))
    L_.append(T(28, 1012, "> Build. Break. Rebuild. Optimize.", 21, GREEN, weight=600))
    return wrap(H, defs, L_, "What Graywizard builds, and life outside code")


# ------------------------------------------------------------------ STACK
def stack_mobile():
    """The stack card for phones: same chips, stacked one group per row of the
    720px canvas, at sizes that survive being scaled to ~0.5x.

    The orbit does come across here — it just cannot sit *beside* the chips, so it
    takes a band of its own across the card: three flat rings (tilts of +-22
    rather than the desktop's 0/60/120, because a 720px card has no vertical room
    for a leaning ellipse) around the same core, medals travelling on them exactly
    as they do on the desktop. No caption under it — the header already says what
    the band is, and the lowest arc needs the room. Everything that made the phone card readable stays:
    16.5px labels, 54px chips, and the rain frozen.

    A group's rows wrap freely, and the card is measured from its own layout — the
    only way a wrapped row can never land on top of the footer.
    """
    ms, mh = 16.5, 54              # chip font size and height
    cgap, rgap = 10, 11            # chip gap, wrapped-row gap: a phone needs air
    mx, mw = 28, W - 56            # the column the chips flow inside
    head, foot = 152, 120
    # The band is sized from the rings, not the other way round: the widest
    # vertical reach of a tilted ellipse is sqrt((rx sin t)^2 + (ry cos t)^2),
    # plus the medal's own radius — which for the geometry below is 107, so a
    # 224px band leaves the groups 17px of clear air under the lowest arc.
    orb_h, orb_r = 224, 107
    ocx, ocy = W / 2, head + orb_h / 2 + 6
    cx0 = head + orb_h + 12        # where the groups start

    rows_h = []
    for _, _, keys in GROUPS:
        _, h, _ = flow(mx, 0, mw, keys, size=ms, h=mh, gap=cgap, row_gap=rgap,
                       animate=False)
        rows_h.append(30 + h)                       # label + chip rows
    body_h = sum(rows_h) + GROUP_GAP * (len(GROUPS) - 1)
    H = cx0 + body_h + foot

    defs, L_ = frame(H, GREEN, rain_cols=7, seed=13)
    core_defs, core_body = core(ocx, ocy, 32, 21)
    defs.append(core_defs)

    L_.append(R(28, 30, 6, 22, fill=GREEN, rx=3))
    L_.append(T(46, 50, "// tech_stack", 22, CYAN, weight=700, ls=2))
    L_.append(T(46, 88, "Tools I build with", 34, TEXT, weight=700, family=SANS, ls=-.5))
    L_.append(T(46, 116, f"{N_CHIPS} tools · {len(GROUPS)} groups · every one shipped in a public repo",
                19, MUTED))

    # ---- the shortlist, in its own band across the card
    ring_geom = [(200, 62, 0, CYAN, 34.0), (194, 58, 20, GREEN, 40.0),
                 (198, 60, -20, VIOLET, 46.0)]
    per = [[] for _ in ring_geom]
    n = len(ORBIT_KEYS)
    for i, key in enumerate(ORBIT_KEYS):
        per[i % len(ring_geom)].append((key, -1.5708 + i * 6.2832 / n))
    for i, (rx, ry, rot, col, dur) in enumerate(ring_geom):
        L_.append(G(orbit(ocx, ocy, rx, ry, rot, per[i], col, dur, f"mOrb{i}"),
                    cls="fade-in", style=f"animation-delay:{.1 + i * .18:.2f}s"))
    L_.append(C(ocx, ocy, 50, fill="none", stroke=GREEN, sw=1, opacity=.24,
                style="stroke-dasharray:3 6"))
    L_.append(core_body)

    y = cx0 + 8
    for i, (label, accent, keys) in enumerate(GROUPS):
        markup, _, _ = flow(mx, y + 38, mw, keys, size=ms, h=mh, gap=cgap, row_gap=rgap,
                            delay0=.4 + i * .3)
        L_.append(G(R(mx, y + 8, 18, 4, fill=accent, rx=2, opacity=.9) +
                    T(mx + 30, y + 18, label, 15.5, SOFT, weight=700, ls=2.4) +
                    markup,
                    cls="fade-in", style=f"animation-delay:{.1 + i * .1:.2f}s"))
        y += rows_h[i] + GROUP_GAP

    L_.append(T(mx, H - 76, "> 6 languages · android tooling · terminal automation",
                20, MUTED))
    L_.append(L(mx, H - 56, W - mx, H - 56, stroke=STROKE, sw=1.2))
    L_.append(T(mx, H - 22, "agents on call · release builds on request", 20, DIM))
    return wrap(H, defs, L_, "Tech stack", extra_css=STACK_CSS)


# ------------------------------------------------------------------ CONNECT
def ids_mobile():
    """Phone variant of the developer-ID/dashboard card - not linked from
    README.md at present (see gen_c.py); kept so the card can be restored."""
    H = 1080
    defs, L_ = frame(H, GREEN, rain_cols=8, seed=23)
    defs += ['<linearGradient id="mHead" x1="0" y1="0" x2="1" y2="1">'
             '<stop offset="0" stop-color="#122b22"/><stop offset="1" stop-color="#101a26"/></linearGradient>']
    # ID card
    L_.append(R(28, 28, W - 56, 396, fill=PANEL2, rx=18, stroke=STROKE2, sw=1.5))
    L_.append(R(28, 28, W - 56, 6, fill=GREEN, rx=3, opacity=.7))
    L_.append(R(52, 62, 104, 104, fill="#07120e", rx=16))
    L_.append(T(74, 128, ">_", 44, GREEN, weight=700))
    L_.append(R(52, 62, 104, 104, fill="none", rx=16, stroke=GREEN_D, sw=1.6, opacity=.65))
    L_.append(T(180, 100, "ADITYA", 42, TEXT, weight=700))
    L_.append(T(180, 138, "@Graywizard888", 24, GREEN, weight=500))
    rows = [("ROLE", "Script · Automation Developer", CYAN),
            ("STACK", "Python · Kotlin · Java · Bash", SOFT),
            ("ORIGIN", "India · UTC+05:30", VIOLET),
            ("MODE", "free-time dev — usually required", AMBER)]
    y = 196
    for k, v, col in rows:
        L_.append(T(52, y, k, 19, MUTED, ls=1.4))
        L_.append(T(140, y, v, 23, col, weight=500))
        y += 38
    cx = 52
    for c in ("Python", "Java", "Kotlin", "Bash", "Lua"):
        w = 34 + len(c) * 13
        L_.append(R(cx, 356, w, 40, fill="#101c26", rx=20, stroke=STROKE2, sw=1.2))
        L_.append(T(cx + 17, 382, c, 20, SOFT))
        cx += w + 10

    # stat tiles
    stats = [(fmt(PROFILE["public_repos"]), "repos", GREEN),
             (fmt(PROFILE["stars"]), "stars", CYAN),
             (fmt(PROFILE["contributions"]), "contributions", VIOLET)]
    tw = 208
    for i, (val, label, col) in enumerate(stats):
        x = 28 + i * (tw + 16)
        L_.append(R(x, 448, tw, 118, fill=PANEL, rx=16, stroke=STROKE, sw=1.4))
        L_.append(R(x + 1, 448, tw - 2, 4, fill=col, rx=2, opacity=.85))
        L_.append(T(x + 20, 508, val, 42, TEXT, weight=700))
        L_.append(T(x + 20, 544, label, 20, MUTED))

    # languages
    L_.append(R(28, 588, W - 56, 224, fill=PANEL, rx=16, stroke=STROKE, sw=1.3))
    L_.append(T(52, 622, "// primary languages", 20, MUTED, ls=1.1))
    L_.append(C(120, 706, 48, fill="none", stroke="#16222e", sw=19))
    parts = [("Python", 3, "#4B8BBE"), ("Shell", 2, "#89E051"), ("Java", 1, "#F89820"),
             ("Rust", 1, "#DEA584"), ("CMake", 1, "#22D3EE")]
    total = sum(v for _, v, _ in parts)
    ang = -90.0
    for val, col in [(v, c) for _, v, c in parts]:
        sweep = 360 * val / total
        a0, a1 = ang + 1.3, ang + sweep - 1.3
        ang += sweep
        if a1 - a0 < 1:
            continue
        x0 = 120 + 48 * math.cos(math.radians(a0)); y0 = 706 + 48 * math.sin(math.radians(a0))
        x1 = 120 + 48 * math.cos(math.radians(a1)); y1 = 706 + 48 * math.sin(math.radians(a1))
        L_.append(P(f"M{x0:.1f} {y0:.1f} A48 48 0 {1 if a1-a0>180 else 0} 1 {x1:.1f} {y1:.1f}",
                    stroke=col, sw=19, opacity=.95))
    L_.append(T(120, 712, "8", 30, TEXT, weight=700, anchor="middle"))
    ly = 646
    for name, val, col in parts:
        L_.append(C(226, ly - 7, 7, fill=col))
        L_.append(T(246, ly, name, 24, SOFT, weight=500))
        L_.append(T(600, ly, str(val), 24, TEXT, weight=600, anchor="end"))
        ly += 34

    # 26-week bar strip (real series)
    WEEKLY = [40, 19, 11, 15, 12, 13, 1, 2, 1, 0, 0, 0, 1, 0, 0, 5, 0, 9, 1, 9, 2, 20, 21, 0, 1, 3]
    L_.append(R(28, 828, W - 56, 190, fill=PANEL, rx=16, stroke=STROKE, sw=1.3))
    L_.append(T(52, 862, "// contributions by week · 26 weeks", 20, MUTED, ls=1))
    base = 976
    mx = max(WEEKLY)
    bw = (W - 56 - 48) / len(WEEKLY)
    for i, v in enumerate(WEEKLY):
        h = max(3, 96 * v / mx)
        col = GREEN if v >= 15 else (CYAN if v >= 5 else "#2b4459")
        L_.append(G(R(0, -h, bw - 5, h, fill=col, rx=2.5, opacity=.92, cls="grow-x",
                      style=f"animation-duration:1s;animation-delay:{.3 + i * .03:.2f}s"),
                    transform=f"translate({52 + i * bw:.1f},{base})"))
    L_.append(T(52, 1002, "peak 40 · Jul → Oct 2026", 19, DIM))
    L_.append(L(28, 1040, W - 28, 1040, stroke=STROKE, sw=1))
    L_.append(T(28, 1064,
                f"since {PROFILE['created']} · {fmt(PROFILE['gists'])} gists · refreshed daily", 19, DIM))
    return wrap(H, defs, L_, "Graywizard developer ID and dashboard")
