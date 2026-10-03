"""Personal-build cards: one tappable image per repository, with real stars,
forks and pull-request counts.

Desktop variant: full motion (odometer metrics, sweep, pulsing dot, size bar).
Mobile variant: 340px canvas so it stays legible at ~half width on a phone,
with no perpetual animation at all.
"""
import math, random
from gen_common import *
from gen_anim import style_block

# repo, display name, short name (mobile), description, language, lang colour,
# stars, forks, pull requests, size in KB
BUILDS = [
    ("Enhancify", "Enhancify", "Enhancify", "Shell", "#89E051",
     "The only custom Revancify — extra features, more customizations", 201, 11, 30, 20450),
    ("Terminal_EX", "Terminal_EX", "Terminal EX", "Java", "#F89820",
     "Termux Monet fork — terminal for Android 8+, extendible by packages", 87, 0, 0, 15560),
    ("GPlayDL-TUI", "GPlayDL-TUI", "GPlayDL TUI", "Python", "#4B8BBE",
     "Feature-rich terminal UI for downloading Android APKs", 8, 2, 1, 1098),
    ("Gists_Collection", "Gists_Collection", "Gists Collection", "Lua", "#7C8FFF",
     "My mpv scripting, audio pipelines and day-to-day hacks", 5, 0, 0, 36),
    ("Gemini-Setup", "Gemini-Setup", "Gemini Setup", "Shell", "#89E051",
     "One-command setup for Gemini CLI, built with privacy in mind", 3, 0, 0, 19),
    ("Extension_Fetcher", "Extension_Fetcher", "Extension Fetcher", "Python", "#4B8BBE",
     "Download any browser extension by its ID — no browser needed", 3, 0, 0, 41),
    ("MovieBox-Tui-Mastered", "MovieBox-Tui", "MovieBox TUI", "Rust", "#DEA584",
     "Find, download and stream movies and live TV in your local player", 1, 0, 1, 33697),
    ("Claude_code_setup", "Claude_code_setup", "Claude Setup", "Python", "#4B8BBE",
     "Self-contained, one-command Claude Code setup for Android Termux", 1, 1, 0, 815),
]

ACCENTS = [GREEN, CYAN, VIOLET, AMBER, PINK, "#60a5fa", GREEN, CYAN]
MAX_KB = max(b[9] for b in BUILDS)

WD, HD = 580, 214      # desktop canvas
WM, HM = 340, 222      # mobile canvas


def _metrics(accent, stars, forks, prs, x, y, size, cls="odo", mobile=False):
    """Three metric blocks; y is the baseline of the number."""
    out, d = [], []
    for i, (glyph, val, label) in enumerate((("★", stars, "stars"),
                                             ("⑂", forks, "forks"),
                                             ("⇄", prs, "PRs"))):
        bx = x + i * (size * 3.1 if not mobile else size * 3.0)
        col = accent if i == 0 else (SOFT if i == 1 else CYAN)
        out.append(T(bx, y, glyph, size * 0.52, col, anchor="start"))
        num, odef, w = odometer(bx + size * 0.62, y, val, size=size, color=TEXT,
                                delay=.25 + i * .12, dur=1.6, spins=2,
                                uid=f"{'m' if mobile else 'd'}{id(out)}{i}")
        out.append(num)
        d.append(odef)
        out.append(T(bx + size * 0.66, y + size * 0.62, label, size * 0.42, MUTED))
    return "".join(out), "".join(d)


def build_card(i, d, mobile=False):
    name, disp, short, lang, lang_col, desc, stars, forks, prs, kb = d
    accent = ACCENTS[i % len(ACCENTS)]
    W, H = (WM, HM) if mobile else (WD, HD)
    rnd = random.Random(i * 7 + 3)

    defs = [
        '<linearGradient id="bBg" x1="0" y1="0" x2=".7" y2="1">'
        f'<stop offset="0" stop-color="{PANEL2}"/><stop offset="1" stop-color="{BG0}"/></linearGradient>',
        f'<linearGradient id="bAcc" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{accent}" stop-opacity=".25"/></linearGradient>',
        f'<linearGradient id="bShine" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset=".5" stop-color="#fff" stop-opacity=".10"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>',
        '<pattern id="bScan" width="4" height="4" patternUnits="userSpaceOnUse">'
        '<rect width="4" height="1" fill="#000" opacity=".3"/></pattern>',
        f'<clipPath id="bClip"><rect width="{W}" height="{H}" rx="14"/></clipPath>',
    ]
    L_ = [R(0, 0, W, H, fill="url(#bBg)", rx=14)]
    for gx in range(40, W, 40):
        L_.append(L(gx, 0, gx, H, stroke="#101d28", sw=1, opacity=.55))
    L_.append(R(0, 0, W, H, fill="url(#bScan)", opacity=.28))
    L_.append(R(0, 0, W, 4.5, fill="url(#bAcc)", rx=2))

    # repo mark + name
    L_.append(R(20, 26, 40, 40, fill=accent, rx=11, opacity=.14))
    L_.append(R(20, 26, 40, 40, fill="none", rx=11, stroke=accent, sw=1.4, opacity=.75))
    L_.append(T(40, 53, f"{i+1:02d}", 17, accent, weight=700, anchor="middle"))

    nsize = 27 if mobile else 25
    L_.append(T(74, 54, short if mobile else disp, nsize, TEXT, weight=700, ls=.2))
    if mobile:
        L_.append(T(74, 54 + nsize * 0.9, lang, 15, lang_col, weight=500, opacity=.95))
    else:
        # language chip pinned to the top-right
        cw = 26 + len(lang) * 8.4
        chip_x = W - 24 - cw
        L_.append(R(chip_x, 30, cw, 26, fill="#101c26", rx=13, stroke=STROKE2, sw=1))
        L_.append(C(chip_x + 14, 43, 4, fill=lang_col))
        L_.append(T(chip_x + 24, 47, lang, 12.5, SOFT))

    if not mobile:
        # description (single line, truncated to the card)
        cut = desc if len(desc) <= 62 else desc[:59].rstrip() + "…"
        L_.append(T(24, 100, cut, 15, SOFT))

    # metrics
    if mobile:
        m_body, m_defs = _metrics(accent, stars, forks, prs, 22, 132, 30, mobile=True)
        defs.append(m_defs)
        L_.append(m_body)
    else:
        L_.append(L(24, 122, W - 24, 122, stroke=STROKE, sw=1, opacity=.9))
        m_body, m_defs = _metrics(accent, stars, forks, prs, 30, 166, 30)
        defs.append(m_defs)
        L_.append(m_body)

    # code-weight bar (log scale of repo size) — real data
    frac = math.log10(max(kb, 1)) / math.log10(MAX_KB)
    if mobile:
        L_.append(T(22, 174, "code weight", 14, MUTED))
        L_.append(R(22, 184, W - 44, 8, fill="#16222e", rx=4))
        L_.append(G(R(0, 0, (W - 44) * frac, 8, fill=url_safe(accent), rx=4, cls="grow-x",
                      style="animation-duration:1.3s;animation-delay:.5s"),
                    transform="translate(22,184)"))
    else:
        bx, by = 366, 150
        L_.append(T(bx, by - 8, "code weight", 11.5, MUTED))
        L_.append(R(bx, by, 186, 9, fill="#16222e", rx=4.5))
        L_.append(G(R(0, 0, 186 * frac, 9, fill=url_safe(accent), rx=4.5, cls="grow-x",
                      style="animation-duration:1.3s;animation-delay:.5s"),
                    transform=f"translate({bx},{by})"))
        L_.append(T(bx, by + 30, f"{kb/1024:.1f} MB of source" if kb > 1024 else f"{kb} KB of source",
                    12, DIM))

    # call to action
    if mobile:
        L_.append(T(22, 212, "tap to open repository →", 16, accent, weight=500))
    else:
        L_.append(T(W - 24, 202, "open repository →", 13, accent, weight=600, anchor="end"))
        # slow shimmer sweep (the one bit of perpetual motion, desktop only)
        L_.append(G(R(-180, 0, 150, H, fill="url(#bShine)", opacity=.9, cls="shimmer",
                      style=f"animation-duration:{9 + i * .6:.1f}s"),
                    clip="url(#bClip)"))

    D, B = "\n".join(defs), "\n".join(L_)
    label = f"{disp} — {stars} stars, {forks} forks, {prs} pull requests"
    extra = ".shimmer { animation-name: shim; animation-timing-function: ease-in-out; animation-iteration-count: infinite; } @keyframes shim { from { transform: translateX(0); } to { transform: translateX(760px); } }" if not mobile else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="{label}">'
            f'<defs>{D}' + style_block(extra) + '</defs>' + G(B, clip="url(#bClip)") +
            R(.5, .5, W - 1, H - 1, rx=14, stroke="#22303f", sw=1) + '</svg>')


def url_safe(hex_col):
    """Plain colour is fine — gradients referenced by id would collide across cards."""
    return hex_col
