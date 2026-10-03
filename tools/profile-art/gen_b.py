"""stack.svg (tech marquee)  +  connect.svg (contact tiles)"""
import random
from gen_common import *
from gen_anim import style_block

# (glyph, name, brand colour) — everything he has actually shipped or built with
ROW1 = [("Py", "Python", "#4B8BBE"), ("Jv", "Java", "#F89820"), ("Kt", "Kotlin", "#A97BFF"),
        ("Cp", "Jetpack Compose", "#34A853"), ("As", "Android Studio", "#3DDC84"),
        ("$", "Bash", "#89E051"), ("Lua", "Lua", "#7C8FFF")]
ROW2 = [("Gt", "Git", "#F05032"), ("GH", "GitHub", "#E6EDF3"), ("Lx", "Linux", "#FCC624"),
        ("Tx", "Termux", "#4ADE80"), ("VS", "VS Code", "#3B9EFF"), ("Rs", "Rust", "#FF7043"),
        ("AI", "AI CLIs", "#A78BFA")]


def tile(x, y, glyph, name, col, i):
    return "".join([
        R(x, y, 124, 92, fill=PANEL, rx=14, stroke="#1a2836", sw=1.1),
        R(x + 44, y + 14, 36, 36, fill=col, rx=10, opacity=.14),
        R(x + 44, y + 14, 36, 36, fill="none", rx=10, stroke=col, sw=1.2, opacity=.7),
        T(x + 62, y + 38, glyph, 15 if glyph != "$" else 17, col, weight=700,
          anchor="middle", family=SANS),
        T(x + 62, y + 74, name, 11.5, SOFT, anchor="middle", weight=500,
          cls="fade-in", style=f"animation-delay:{.5 + i * .05:.2f}s"),
    ])


def stack():
    W, H = 1200, 332
    PITCH, N = 140, 7
    pattern = N * PITCH
    defs = [
        '<linearGradient id="sBg" x1="0" y1="0" x2=".6" y2="1">'
        f'<stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG0}"/></linearGradient>',
        '<linearGradient id="sFadeL" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{BG1}" stop-opacity="1"/><stop offset="1" stop-color="{BG1}" stop-opacity="0"/></linearGradient>',
        '<linearGradient id="sFadeR" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{BG0}" stop-opacity="0"/><stop offset="1" stop-color="{BG0}" stop-opacity="1"/></linearGradient>',
        '<pattern id="sScan" width="4" height="4" patternUnits="userSpaceOnUse">'
        '<rect width="4" height="1" fill="#000" opacity=".35"/></pattern>',
        f'<clipPath id="sClip"><rect width="{W}" height="{H}" rx="16"/></clipPath>',
    ]
    L_ = [R(0, 0, W, H, fill="url(#sBg)", rx=16)]
    for x in range(60, W, 60):
        L_.append(L(x, 0, x, H, stroke="#0f1a24", sw=1, opacity=.7))
    L_.append(R(0, 0, W, H, fill="url(#sScan)", opacity=.28))
    L_.append(hud_corners(10, 10, W - 20, H - 20, GREEN, 22, 2, .45, cls=None))
    L_.append(R(56, 30, 4, 12, fill=GREEN, rx=2))
    L_.append(T(68, 40, "// tech_stack  ·  worked_on", 12.5, SOFT, ls=1.6))
    L_.append(T(1144, 40, "built with · shipped in", 11, MUTED, anchor="end", ls=1))

    rows = [(ROW1, 96, "marquee-l", GREEN), (ROW2, 204, "marquee-r", CYAN)]
    for row, y, cls, col in rows:
        inner = []
        for rep in range(3):
            for i, (glyph, name, c) in enumerate(row):
                inner.append(tile(rep * pattern + i * PITCH, 0, glyph, name, c, i))
        L_.append(G("".join(inner), cls=cls,
                    style=f"--shift:-{pattern}px", transform=f"translate(0,{y})"))
    # edge fades so tiles slide in/out of the card cleanly
    L_.append(R(0, 78, 96, 232, fill="url(#sFadeL)"))
    L_.append(R(W - 96, 78, 96, 232, fill="url(#sFadeR)"))
    L_.append(L(40, 300, 1160, 300, stroke=STROKE, sw=1))
    L_.append(T(56, 319, "> 3 languages · Android tooling · shell automation · Lua scripts", 11.5, MUTED))
    L_.append(T(1144, 319, "release builds on request", 11.5, DIM, anchor="end"))

    D, B = "\n".join(defs), "\n".join(L_)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="Tech stack">'
            f'<defs>{D}' + style_block() + '</defs>' + G(B, clip="url(#sClip)") +
            R(0.5, 0.5, W - 1, H - 1, rx=16, stroke="#22303f", sw=1) + '</svg>')


# ---------------------------------------------------------------- CONNECT
def connect():
    W, H = 1200, 258
    defs = [
        '<linearGradient id="cBg" x1="0" y1="0" x2=".6" y2="1">'
        f'<stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG0}"/></linearGradient>',
        '<pattern id="cScan" width="4" height="4" patternUnits="userSpaceOnUse">'
        '<rect width="4" height="1" fill="#000" opacity=".35"/></pattern>',
        f'<clipPath id="cClip"><rect width="{W}" height="{H}" rx="16"/></clipPath>',
        '<filter id="cGlow" x="-50%" y="-50%" width="200%" height="200%">'
        '<feGaussianBlur stdDeviation="4"/></filter>',
    ]
    L_ = [R(0, 0, W, H, fill="url(#cBg)", rx=16)]
    for x in range(60, W, 60):
        L_.append(L(x, 0, x, H, stroke="#0f1a24", sw=1, opacity=.7))
    L_.append(R(0, 0, W, H, fill="url(#cScan)", opacity=.28))
    L_.append(hud_corners(10, 10, W - 20, H - 20, CYAN, 22, 2, .45, cls=None))
    L_.append(R(56, 28, 4, 12, fill=CYAN, rx=2))
    L_.append(T(68, 38, "// connect", 12.5, SOFT, ls=1.6))
    L_.append(T(1144, 38, "secure channels · open to collaboration", 11, MUTED, anchor="end", ls=1))

    cards = [
        ("TELEGRAM", "@Graywizard_projects", "https://t.me/Graywizard_projects", "#22A7E0", "chan"),
        ("GITHUB", "@Graywizard888", "https://github.com/Graywizard888", "#E6EDF3", "gh"),
        ("PORTFOLIO", "website-src-seven", "https://website-src-seven.vercel.app/", "#4ADE80", "web"),
        ("GISTS", "mpv · lua scripts", "https://gist.github.com/Graywizard888", "#FBBF24", "lua"),
    ]
    tw, gap = 265, 20
    for i, (label, handle, url, col, kind) in enumerate(cards):
        x = 40 + i * (tw + gap)
        L_.append(R(x, 60, tw, 118, fill=PANEL, rx=14, stroke="#1a2836", sw=1.1))
        L_.append(R(x, 60, tw, 3, fill=col, rx=1.5, opacity=.85))
        # icon
        if kind == "chan":
            L_.append(P(f"M{x+22} {98} L{x+52} {84} L{x+42} {116} L{x+33} {103} Z",
                        fill=col, opacity=.9))
            L_.append(P(f"M{x+33} {103} L{x+52} {84}", stroke=BG0, sw=1.3, opacity=.75))
            L_.append(C(x + 60, 96, 3, fill=col, cls="pulse"))
        elif kind == "gh":
            GH = ("M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49"
                  "-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82"
                  ".72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15"
                  "-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82"
                  ".44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2"
                  "0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z")
            L_.append(G(P(GH, fill=col), transform=f"translate({x+24},84) scale(1.75)"))
        elif kind == "web":
            L_.append(C(x + 36, 98, 12, stroke=col, sw=1.6))
            L_.append(P(f"M{x+24} 98 h24 M{x+36} 86 a16 16 0 0 1 0 24 a16 16 0 0 1 0 -24", stroke=col, sw=1.3))
        else:
            L_.append(P(f"M{x+40} 84 a14 14 0 1 0 0 28 a11.5 11.5 0 1 1 0 -28 z", fill=col, opacity=.95))
            L_.append(C(x + 30, 92, 1.6, fill=col, opacity=.8))
            L_.append(C(x + 27, 101, 1.1, fill=col, opacity=.5))
        L_.append(T(x + 74, 92, label, 11, MUTED, ls=1.8, weight=600))
        L_.append(T(x + 74, 116, handle, 13.5, col, weight=600))
        L_.append(T(x + 24, 150, url.replace("https://", "")[:34], 10.5, DIM))
        L_.append(P(f"M{x+tw-32} 158 l10 -10 M{x+tw-32} 148 h10 v10", stroke=col, sw=1.5, opacity=.8))

    L_.append(L(40, 200, 1160, 200, stroke=STROKE, sw=1))
    L_.append(C(56, 225, 4.5, fill=GREEN, cls="pulse"))
    L_.append(T(68, 229.5, "open to collaboration · issue reports and PRs welcome · every repo MIT or GPL-3.0",
                11.5, MUTED))
    L_.append(T(1144, 229.5, "reply window: IST evenings", 11.5, DIM, anchor="end"))

    D, B = "\n".join(defs), "\n".join(L_)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="Connect with Graywizard">'
            f'<defs>{D}' + style_block() + '</defs>' + G(B, clip="url(#cClip)") +
            R(0.5, 0.5, W - 1, H - 1, rx=16, stroke="#22303f", sw=1) + '</svg>')
