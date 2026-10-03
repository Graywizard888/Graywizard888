"""Cyber repo cards — the github-readme-stats "pin card" information layout
(repo name, description, language, stars, forks) rendered in the profile's
terminal/neon style, with license, pull requests and last-push added.

Desktop cards carry a slow shimmer, a pulsing index chip and rolling counters.
Phone cards are condensed and permanently static.
"""
from gen_common import *
from gen_anim import style_block

# repo, display name, language, language colour, license, description,
# stars, forks, pulls, size_kb, updated(label)
BUILDS = [
    ("Enhancify", "Enhancify", "Shell", "#89E051", None,
     "The only custom Revancify with extra features and more customizations",
     201, 11, 30, 20450, "16d ago"),
    ("Terminal_EX", "Terminal_EX", "Java", "#F89820", "GPL-3.0",
     "Termux Monet fork — terminal for Android 8+, extendible by packages",
     87, 0, 0, 15560, "5mo ago"),
    ("GPlayDL-TUI", "GPlayDL-TUI", "Python", "#4B8BBE", "MIT",
     "Feature-rich Terminal UI for downloading Android APKs from Google Play",
     8, 2, 1, 1098, "2mo ago"),
    ("Gists_Collection", "Gists_Collection", "Lua", "#7C8FFF", "MIT",
     "The collection of Gists — mpv scripting and day-to-day hacks",
     5, 0, 0, 36, "5mo ago"),
    ("Gemini-Setup", "Gemini-Setup", "Shell", "#89E051", "MIT",
     "Installs and configures Gemini CLI while keeping privacy in mind",
     3, 0, 0, 19, "6mo ago"),
    ("Extension_Fetcher", "Extension_Fetcher", "Python", "#4B8BBE", "Apache-2.0",
     "Tries to download an extension by user specified extension id",
     3, 0, 0, 41, "1y ago"),
    ("MovieBox-Tui-Mastered", "MovieBox-Tui", "Rust", "#DEA584", "Apache-2.0",
     "Terminal interface to find, download and stream movies, TV and live TV",
     1, 0, 1, 33697, "4d ago"),
    ("Claude_code_setup", "Claude_code_setup", "Python", "#4B8BBE", "MIT",
     "Self-contained, one-command setup for Claude Code on Android Termux",
     1, 1, 0, 815, "1mo ago"),
]

ACCENTS = [GREEN, CYAN, VIOLET, AMBER, PINK, "#60a5fa", GREEN_D, CYAN]
CANVAS_W, CANVAS_H = 480, 236    # ~github-readme-stats pin proportions:
                                 # a 360px phone then renders it at ~0.75x, not 0.3x


def _wrap(text, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + 1 <= width:
            cur = (cur + " " + w).strip()
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines[:2]


def _metrics(x, y, size, accent, stars, forks, prs, uid, mobile=False):
    """★ stars · ⑂ forks · ⇄ pull requests — rolling counters."""
    out, defs = [], []
    gap = size * 3.4 if not mobile else size * 3.5
    for i, (glyph, val, col) in enumerate(((None, stars, accent),
                                           ("⑂", forks, SOFT),
                                           ("⇄", prs, CYAN))):
        bx = x + i * gap
        if glyph:
            out.append(T(bx, y, glyph, size * 0.62, col))
            nx = bx + size * 0.62
        else:
            out.append(T(bx, y, "★", size * 0.62, col))
            nx = bx + size * 0.70
        num, odef, _ = odometer(nx, y, val, size=size, color=TEXT,
                                delay=.25 + i * .12, dur=1.6, spins=2,
                                uid=f"{uid}{i}")
        out.append(num)
        defs.append(odef)
    return "".join(out), "".join(defs)


def build_card(i, d, mobile=False):
    (repo, disp, lang, lang_col, lic, desc, stars, forks, prs, kb, updated) = d
    accent = ACCENTS[i % len(ACCENTS)]
    W, H = CANVAS_W, CANVAS_H
    uid = f"{'m' if mobile else 'd'}{i}"

    defs = [
        '<linearGradient id="cBg" x1="0" y1="0" x2=".7" y2="1">'
        f'<stop offset="0" stop-color="{PANEL2}"/><stop offset="1" stop-color="{BG0}"/></linearGradient>',
        f'<linearGradient id="cAcc" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{accent}" stop-opacity=".15"/></linearGradient>',
        '<linearGradient id="cShine" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset=".5" stop-color="#fff" stop-opacity=".10"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>',
        '<radialGradient id="cGlow" cx=".5" cy=".5" r=".5">'
        f'<stop offset="0" stop-color="{accent}" stop-opacity=".22"/>'
        f'<stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient>',
        '<pattern id="cScan" width="4" height="4" patternUnits="userSpaceOnUse">'
        '<rect width="4" height="1" fill="#000" opacity=".3"/></pattern>',
        f'<clipPath id="cClip"><rect width="{W}" height="{H}" rx="14"/></clipPath>',
    ]
    L_ = [R(0, 0, W, H, fill="url(#cBg)", rx=14)]
    # grid + scanlines + accent rail (the cyber frame)
    for gx in range(40, W, 40):
        L_.append(L(gx, 0, gx, H, stroke="#101d28", sw=1, opacity=.55))
    L_.append(R(0, 0, W, H, fill="url(#cScan)", opacity=.26))
    L_.append(R(0, 0, W, 4.5, fill="url(#cAcc)", rx=2))
    L_.append(hud_corners(8, 8, W - 16, H - 16, accent, 16, 1.6, .38, cls=None))

    # ---- prompt line
    L_.append(T(22, 36, f"~/repos/{repo[:20].lower()}$", 13.5, DIM))
    L_.append(T(W - 22, 36, f"pushed {updated}", 13.5, DIM, anchor="end"))
    # repo name with a soft accent glow behind it
    nsize = 32 if len(disp) <= 14 else (27 if len(disp) <= 18 else 23)
    L_.append(f'<ellipse cx="120" cy="76" rx="190" ry="42" fill="url(#cGlow)"/>')
    L_.append(T(22, 86, disp, nsize, TEXT, weight=700))
    # index chip + open hint
    L_.append(R(W - 74, 58, 52, 32, fill=accent, rx=9, opacity=.13))
    L_.append(R(W - 74, 58, 52, 32, fill="none", rx=9, stroke=accent, sw=1.3, opacity=.7))
    L_.append(T(W - 48, 82, f"{i+1:02d}", 17, accent, weight=700, anchor="middle"))
    L_.append(T(W - 92, 82, "↗", 15, MUTED, anchor="end"))
    # description + last push
    for k, ln in enumerate(_wrap(desc, 46)):
        L_.append(T(22, 120 + k * 22, ln, 16.5, SOFT))
    L_.append(L(22, 166, W - 22, 166, stroke=STROKE, sw=1))
    # footer: language, counters, licence
    L_.append(C(28, 200, 6, fill=lang_col))
    L_.append(T(42, 205, lang, 16, SOFT, weight=500))
    mb, md = _metrics(120, 205, 22, accent, stars, forks, prs, uid)
    defs.append(md)
    L_.append(mb)
    label_lic = lic if lic else "unlicensed"
    cw = 28 + len(label_lic) * 8.6
    L_.append(R(W - 22 - cw, 186, cw, 27, fill="#101c26", rx=13.5, stroke=STROKE2, sw=1))
    L_.append(T(W - 22 - cw / 2, 204, label_lic, 13, MUTED if lic else DIM, anchor="middle"))
    # shimmer sweep — desktop only (phones stay static)
    if not mobile:
        L_.append(G(R(-190, 0, 160, H, fill="url(#cShine)", opacity=.9, cls="shimmer",
                      style=f"animation-duration:{8.5 + i * .7:.1f}s"),
                    clip="url(#cClip)"))

    D, B = "\n".join(defs), "\n".join(L_)
    label = (f"{disp} — {stars} stars, {forks} forks, {prs} pull requests, "
         f"{lang}, {lic or 'no licence'}")
    extra = ""
    if not mobile:
        extra = (".shimmer { animation-name: shim; animation-timing-function: ease-in-out;"
                 " animation-iteration-count: infinite; }"
                 " @keyframes shim { from { transform: translateX(0); }"
                 " to { transform: translateX(760px); } }")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="{label}">'
            f'<defs>{D}' + style_block(extra) + '</defs>' + G(B, clip="url(#cClip)") +
            R(.5, .5, W - 1, H - 1, rx=14, stroke="#22303f", sw=1) + '</svg>')
