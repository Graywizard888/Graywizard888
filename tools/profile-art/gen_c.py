"""id-dashboard.svg — developer ID card + live system dashboard (real numbers)."""
import math, random
from gen_common import *
from gen_anim import style_block

# real data, pulled from the GitHub API on 2026-10-03
REPOS, STARS, CONTRIB = 12, 309, 1041
TILES = [("PUBLIC REPOS", REPOS, GREEN),
         ("STARS EARNED", STARS, CYAN),
         ("CONTRIBUTIONS", CONTRIB, VIOLET)]
LANGS = [("Python", 3, "#4B8BBE"), ("Shell", 2, "#89E051"), ("Java", 1, "#F89820"),
         ("Rust", 1, "#DEA584"), ("CMake", 1, "#22D3EE")]
WEEKLY = [40, 19, 11, 15, 12, 13, 1, 2, 1, 0, 0, 0, 1, 0, 0, 5, 0, 9, 1, 9, 2, 20, 21, 0, 1, 3]
CHIPS = ["Python", "Java", "Kotlin", "Bash", "Lua"]


def donut(cx, cy, r, sw, parts, gap_deg=2.6):
    total = sum(v for v, _ in parts)
    out, ang = [], -90.0
    for val, col in parts:
        sweep = 360.0 * val / total
        a0, a1 = ang + gap_deg / 2, ang + sweep - gap_deg / 2
        ang += sweep
        if a1 - a0 < 1.2:
            continue
        large = 1 if (a1 - a0) > 180 else 0
        x0 = cx + r * math.cos(math.radians(a0)); y0 = cy + r * math.sin(math.radians(a0))
        x1 = cx + r * math.cos(math.radians(a1)); y1 = cy + r * math.sin(math.radians(a1))
        circ = 2 * math.pi * r
        frac = val / total
        out.append(P(f"M{x0:.2f} {y0:.2f} A{r} {r} 0 {large} 1 {x1:.2f} {y1:.2f}",
                     stroke=col, sw=sw, opacity=.95,
                     style=f"stroke-dasharray:{frac*circ:.1f} {circ:.1f};"
                           f"animation-duration:1.5s;animation-delay:{.35 + .45*(1-frac):.2f}s"))
    return "".join(out)


def card_ids():
    W, H = 1200, 404
    defs = [
        '<linearGradient id="iBg" x1="0" y1="0" x2=".6" y2="1">'
        f'<stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG0}"/></linearGradient>',
        '<linearGradient id="iHead" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#122b22"/><stop offset=".6" stop-color="#0d1a26"/>'
        '<stop offset="1" stop-color="#101a26"/></linearGradient>',
        '<linearGradient id="iShine" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset=".5" stop-color="#fff" stop-opacity=".22"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>',
        '<pattern id="idScan" width="4" height="4" patternUnits="userSpaceOnUse">'
        '<rect width="4" height="1" fill="#000" opacity=".34"/></pattern>',
        f'<clipPath id="iClip"><rect width="{W}" height="{H}" rx="16"/></clipPath>',
        '<clipPath id="iPhotoClip"><rect x="38" y="92" width="132" height="132" rx="12"/></clipPath>',
        '<clipPath id="iCardClip"><rect x="40" y="60" width="532" height="304" rx="14"/></clipPath>',
        '<clipPath id="iHeadClip"><path d="M40 74 a14 14 0 0 1 14 -14 h504 a14 14 0 0 1 14 14 v70 h-532 z"/></clipPath>',
        '<filter id="iGlow" x="-60%" y="-60%" width="220%" height="220%">'
        f'<feGaussianBlur stdDeviation="7"/></filter>',
    ]
    L_ = [R(0, 0, W, H, fill="url(#iBg)", rx=16)]
    for x in range(60, W, 60):
        L_.append(L(x, 0, x, H, stroke="#0f1a24", sw=1, opacity=.7))
    L_.append(R(0, 0, W, H, fill="url(#idScan)", opacity=.28))
    L_.append(hud_corners(10, 10, W - 20, H - 20, GREEN, 22, 2, .45, cls=None))

    # ============================================================ ID CARD (left)
    L_.append(R(56, 46, 4, 12, fill=GREEN, rx=2))
    L_.append(T(68, 56, "// developer_id", 12.5, SOFT, ls=1.6))
    L_.append(T(584, 56, "GW-888 · IST 05:30", 11, MUTED, anchor="end", ls=1))
    L_.append(R(40, 60, 532, 304, fill=PANEL2, rx=14, stroke=STROKE2, sw=1.2))
    L_.append(G(R(0, 0, 532, 70, fill="url(#iHead)", opacity=.9), clip="url(#iHeadClip)"))
    # diagonal security strip inside the header
    L_.append(G(R(0, 0, 6, 70, fill=GREEN), transform="translate(300,60)",
                clip="url(#iHeadClip)"))
    for i in range(6):
        L_.append(G(R(0, 0, 3, 70, fill=GREEN_D, opacity=.22), transform=f"translate({320 + i*26},60)",
                    clip="url(#iHeadClip)"))

    # portrait block
    L_.append(R(38, 92, 132, 132, fill="#07120e", rx=12))
    L_.append(G("".join([T(58, 152, ">_", 46, GREEN, weight=700),
                         R(58, 170, 68, 3.5, fill=CYAN, rx=1.75, opacity=.75)]),
               clip="url(#iPhotoClip)"))
    L_.append(R(38, 92, 132, 132, fill="none", rx=12, stroke=GREEN_D, sw=1.4, opacity=.65))
    L_.append(G(G(R(-140, 92, 90, 132, fill="url(#iShine)", opacity=.7, cls="holo",
                   style="animation-duration:6s;animation-delay:1.2s"),
                 clip="url(#iPhotoClip)")))
    for i in range(8):
        L_.append(L(28, 88 + i * 4.2, 38, 88 + i * 4.2, stroke=GREEN_D, sw=1, opacity=.22))

    L_.append(T(190, 118, "ADITYA", 25, TEXT, weight=700, ls=1.2))
    L_.append(T(190, 141, "@Graywizard888", 13.5, GREEN, weight=500))
    L_.append(R(190, 152, 366, 1, fill=STROKE, rx=.5))
    rows = [("ROLE", "Script · Automation Developer", CYAN),
            ("STACK", "Python · Kotlin · Java · Bash · Lua", SOFT),
            ("ORIGIN", "India · UTC+05:30", VIOLET),
            ("MODE", "free-time developer — usually required", AMBER)]
    y = 176
    for k, v, col in rows:
        L_.append(T(190, y, k, 10, MUTED, ls=1.6))
        L_.append(T(248, y, v, 12.5, col, weight=500))
        y += 26
    cx = 190
    for i, c in enumerate(CHIPS):
        w = 22 + len(c) * 7.2
        L_.append(R(cx, 278, w, 26, fill="#101c26", rx=13, stroke=STROKE2, sw=1))
        L_.append(C(cx + 12, 291, 2.6, fill=GREEN, opacity=.9,
                    cls="pulse" if i < 2 else None,
                    style=f"animation-delay:{i * .3:.1f}s" if i < 2 else None))
        L_.append(T(cx + 20, 295.5, c, 11, SOFT))
        cx += w + 8

    # footer: signature strip + barcode
    L_.append(L(40, 314, 572, 314, stroke=STROKE, sw=1))
    L_.append(T(64, 334, "SIGNED", 8.5, MUTED, ls=2))
    L_.append(P("M64 348 q9 -8 18 0 q9 -8 18 0 q8 -7 17 0", stroke=GREEN, sw=1.2, opacity=.55))
    rr = random.Random(5)
    bx = 176
    for i in range(30):
        w = rr.choice([1.4, 2.4, 3.4])
        L_.append(R(bx, 324, w, 24, fill="#c9d8e6", opacity=rr.uniform(.4, .95), rx=.4))
        bx += w + rr.choice([2.0, 3.0])
    L_.append(T(556, 338, "member since Jun 2024", 10, MUTED, anchor="end", ls=.4))
    L_.append(T(556, 324, "ID · GW-888-2024-IST", 10, DIM, anchor="end", ls=.8))

    # ============================================================ DASHBOARD (right)
    L_.append(R(616, 60, 544, 304, fill=BG0, rx=14, stroke=STROKE, sw=1.1, opacity=.72))
    L_.append(R(636, 46, 4, 12, fill=CYAN, rx=2))
    L_.append(T(648, 56, "// system_dashboard", 12.5, SOFT, ls=1.6))
    L_.append(T(1180, 56, "snapshot · 03 Oct 2026", 11, MUTED, anchor="end", ls=1))

    tw = 166
    ododefs = []
    for i, (label, val, col) in enumerate(TILES):
        x = 636 + i * (tw + 12)
        L_.append(R(x, 74, tw, 78, fill=PANEL, rx=12, stroke=STROKE, sw=1.1))
        L_.append(R(x + 1, 74, tw - 2, 2.5, fill=col, rx=1.2, opacity=.85))
        L_.append(T(x + 16, 96, label, 9.5, MUTED, ls=1.5))
        num, od, wnum = odometer(x + 16, 140, val, size=33, color=TEXT,
                                 delay=.4 + i * .16, dur=2.4, spins=2, uid=f"o{i}")
        L_.append(num); ododefs.append(od)
    defs += ododefs
    L_.append(L(636, 170, 1180, 170, stroke=STROKE, sw=1))

    # donut + legend
    L_.append(C(716, 250, 46, fill="none", stroke="#16222e", sw=18))
    L_.append(donut(716, 250, 46, 18, [(v, c) for _, v, c in LANGS]))
    L_.append(T(716, 245, str(sum(v for _, v, _ in LANGS)), 26, TEXT, weight=700,
                anchor="middle", cls="fade-in", style="animation-delay:.9s"))
    L_.append(T(716, 264, "repos coded", 9.5, MUTED, anchor="middle", ls=.6))
    L_.append(T(790, 194, "// primary languages", 10.5, MUTED, ls=1.2))
    ly = 216
    for i, (name, val, col) in enumerate(LANGS):
        L_.append(C(796, ly - 4, 4.5, fill=col,
                    cls="pulse-soft" if i < 2 else None,
                    style=f"animation-duration:4s;animation-delay:{i * .4:.1f}s" if i < 2 else None))
        L_.append(T(810, ly, name, 12.5, SOFT, weight=500))
        L_.append(T(944, ly, f"{val}", 12.5, TEXT, weight=600, anchor="end"))
        ly += 25
    L_.append(T(1000, 194, "// weekly commits", 10.5, MUTED, ls=1.2))
    L_.append(T(1180, 216, "peak 40", 9.5, DIM, anchor="end"))

    # sparkline of the same weekly series (real data)
    pts, mn, mx = [], min(WEEKLY), max(WEEKLY)
    for i, v in enumerate(WEEKLY):
        px = 1000 + i * (180 / (len(WEEKLY) - 1))
        py = 300 - (v / mx) * 96
        pts.append((px, py))
    d = "M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in pts)
    area = d + f" L{pts[-1][0]:.1f} 304 L{pts[0][0]:.1f} 304 Z"
    L_.append(f'<linearGradient id="iArea" x1="0" y1="0" x2="0" y2="1">'
              f'<stop offset="0" stop-color="{GREEN}" stop-opacity=".45"/>'
              f'<stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></linearGradient>')
    L_.append(P(area, fill="url(#iArea)", cls="fade-in", style="animation-delay:.6s"))
    L_.append(P(d, stroke=GREEN, sw=1.8, cls="draw",
                style=f"--len:419;animation-duration:2.2s;animation-delay:.5s"))
    peak = WEEKLY.index(max(WEEKLY))
    px, py = pts[peak]
    L_.append(C(px, py, 3.0, fill=GREEN, cls="pulse", style="animation-delay:.2s"))
    L_.append(L(1000, 304, 1180, 304, stroke="#1a2a38", sw=1))
    L_.append(T(1000, 322, "Jul 2026", 9.5, MUTED))
    L_.append(T(1180, 322, "Oct 2026", 9.5, MUTED, anchor="end"))

    # footer strip inside the dashboard
    L_.append(L(636, 344, 1180, 344, stroke=STROKE, sw=1))
    L_.append(C(644, 360, 4, fill=GREEN, cls="pulse"))
    L_.append(T(656, 364, "12 repos · 309 stars · 1,041 contributions · 4 gists · since Jun 2024",
                10.5, MUTED))
    # closing rule under the dashboard
    L_.append(L(636, 378, 1180, 378, stroke="#182838", sw=1, opacity=.7))

    D, B = "\n".join(defs), "\n".join(L_)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="Graywizard developer ID and dashboard">'
            f'<defs>{D}' + style_block() + '</defs>' + G(B, clip="url(#iClip)") +
            R(0.5, 0.5, W - 1, H - 1, rx=16, stroke="#22303f", sw=1) + '</svg>')
