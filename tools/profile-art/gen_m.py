"""Mobile card variants: 720px wide so text lands at ~2x the rendered size of the
1200px cards on a phone, with the heavy motion removed (frozen rain, no marquees,
no continuous tweens beyond two tiny blinking dots).

Served to phones via <picture><source media="(max-width: 700px)">.
"""
import math, random
from gen_common import *
import gen_v
from gen_anim import style_block

W = 720


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
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="{label}">'
            f'<defs>{D}' + style_block(extra_css) + '</defs>' + G(B, clip="url(#mClip)") +
            R(1, 1, W - 2, H - 2, rx=20, stroke="#22303f", sw=2) + '</svg>')


# ------------------------------------------------------------------ HERO
# Poster band: phones get the still + play button, never the frame sequence (it
# would be ~700 KB on a phone connection for something they can't replay).
MOB_VIDEO_X = (720 - gen_v.WINDOW_W) // 2
MOB_VIDEO_Y = 96
MOB_SHIFT = 356


def hero_mobile():
    H = 820
    HT = H + MOB_SHIFT
    defs, L_ = frame(HT, GREEN, rain_cols=9, seed=5)
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

    # ------------------------------------------------- intro poster (no frames)
    v_body, _, v_defs, _ = gen_v.panel(MOB_VIDEO_X, MOB_VIDEO_Y, mode="poster")
    defs += v_defs
    L_.append(v_body)
    L_.append(f'<g transform="translate(0,{MOB_SHIFT})">')

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
    L_.append("</g>")
    return wrap(HT, defs, L_, "Graywizard — coder, gamer, system architect, "
                "with a still from the ten-second intro animation")


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
    H = 620
    defs, L_ = frame(H, GREEN, rain_cols=7, seed=13)
    L_.append(R(28, 30, 5, 20, fill=GREEN, rx=2.5))
    L_.append(T(46, 48, "// tech_stack", 22, SOFT, ls=1.4))
    L_.append(T(W - 28, 48, "14 tools", 20, MUTED, anchor="end"))
    ROW1 = [("Py", "Python", "#4B8BBE"), ("Jv", "Java", "#F89820"), ("Kt", "Kotlin", "#A97BFF"),
            ("Cp", "Jetpack Compose", "#34A853"), ("As", "Android Studio", "#3DDC84"),
            ("$", "Bash", "#89E051"), ("Lua", "Lua", "#7C8FFF")]
    ROW2 = [("Gt", "Git", "#F05032"), ("GH", "GitHub", "#E6EDF3"), ("Lx", "Linux", "#FCC624"),
            ("Tx", "Termux", "#4ADE80"), ("VS", "VS Code", "#3B9EFF"), ("Rs", "Rust", "#FF7043"),
            ("AI", "AI CLIs", "#A78BFA")]
    pw, ph = 320, 58
    for col, items in enumerate((ROW1, ROW2)):
        for i, (glyph, name, colr) in enumerate(items):
            x = 28 + col * (pw + 16)
            y = 84 + i * 72
            L_.append(R(x, y, pw, ph, fill=PANEL, rx=14, stroke="#1a2836", sw=1.3))
            L_.append(R(x + 12, y + 11, 36, 36, fill=colr, rx=10, opacity=.16))
            L_.append(T(x + 30, y + 36, glyph, 20, colr, weight=700, anchor="middle",
                        family=None, cls="fs"))
            L_.append(T(x + 60, y + 37, name, 24, SOFT, weight=500, cls="fade-in",
                        style=f"animation-delay:{.2 + i * .05:.2f}s"))
    L_.append(L(28, H - 40, W - 28, H - 40, stroke=STROKE, sw=1))
    L_.append(T(28, H - 16, "> built with · shipped in · release builds on request", 20, MUTED))
    return wrap(H, defs, L_, "Tech stack")


# ------------------------------------------------------------------ CONNECT
def connect_mobile():
    H = 700
    defs, L_ = frame(H, CYAN, rain_cols=7, seed=17)
    L_.append(R(28, 30, 5, 20, fill=CYAN, rx=2.5))
    L_.append(T(46, 48, "// connect", 22, SOFT, ls=1.4))
    L_.append(T(W - 28, 48, "open to collaboration", 20, MUTED, anchor="end"))
    cards = [("TELEGRAM", "@Graywizard_projects", "t.me/Graywizard_projects", "#22A7E0"),
             ("GITHUB", "@Graywizard888", "github.com/Graywizard888", "#E6EDF3"),
             ("PORTFOLIO", "cyber portfolio", "website-src-seven.vercel.app", "#4ADE80"),
             ("GISTS", "mpv · lua scripts", "gist.github.com/Graywizard888", "#FBBF24")]
    cw, ch = 320, 216
    for i, (label, handle, url, col) in enumerate(cards):
        x = 28 + (i % 2) * (cw + 16)
        y = 84 + (i // 2) * (ch + 18)
        L_.append(R(x, y, cw, ch, fill=PANEL, rx=16, stroke="#1a2836", sw=1.3))
        L_.append(R(x, y, cw, 4, fill=col, rx=2, opacity=.9))
        if i == 1:      # GitHub mark, drawn
            GH = ("M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49"
                  "-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82"
                  ".72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15"
                  "-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82"
                  ".44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2"
                  "0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z")
            L_.append(G(P(GH, fill=col), transform=f"translate({x+28},{y+26}) scale(2.1)"))
        else:
            L_.append(C(x + 45, y + 43, 17, fill="none", stroke=col, sw=2))
            if i == 0:
                L_.append(P(f"M{x+38} {y+43} L{x+58} {y+33} L{x+50} {y+57} L{x+44} {y+47} Z", fill=col, opacity=.95))
            elif i == 2:
                L_.append(T(x + 45, y + 50, "WWW", 15, col, anchor="middle", weight=700, family=None, cls="fs"))
            else:
                L_.append(C(x + 45, y + 43, 7, fill=col, opacity=.9))
        L_.append(T(x + 26, y + 96, label, 21, MUTED, ls=1.6, weight=600))
        hsize = 25 if len(handle) <= 17 else (22 if len(handle) <= 20 else 20)
        L_.append(T(x + 26, y + 134, handle, hsize, col, weight=600))
        L_.append(T(x + 26, y + 176, url, 17, DIM))
        L_.append(P(f"M{x+cw-38} {y+ch-20} l14 -14 M{x+cw-38} {y+ch-34} h14 v14", stroke=col, sw=2, opacity=.85))
    L_.append(L(28, 660, W - 28, 660, stroke=STROKE, sw=1))
    L_.append(C(40, 684, 6, fill=GREEN, cls="pulse"))
    L_.append(T(58, 691, "every repo MIT or GPL-3.0 · reply window: IST evenings", 20, MUTED))
    return wrap(H, defs, L_, "Connect with Graywizard")


# ------------------------------------------------------------------ ID + DASHBOARD
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
