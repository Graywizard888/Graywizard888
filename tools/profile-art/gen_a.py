"""hero.svg  (video-intro style name card)  +  about-life.svg  (build | life)"""
import random
from gen_common import *
from gen_anim import style_block, typing_line

# ---------------------------------------------------------------- icons (24x24, centred on 0,0)
def icon_gamepad(c):
    return (R(-14, -8, 28, 16, fill="none", rx=7, stroke=c, sw=1.6) +
            L(-9, 0, -4.6, 0, stroke=c, sw=1.6, cap="round") +
            L(-6.8, -2.2, -6.8, 2.2, stroke=c, sw=1.6, cap="round") +
            C(6.4, -2.2, 1.5, fill=c) + C(8.6, 1.4, 1.5, fill=c))


def icon_headphones(c):
    return (P("M-9.4 3.4 v-1.8 a9.4 9.4 0 0 1 18.8 0 v1.8", stroke=c, sw=1.6) +
            R(-12.4, 2.6, 5.4, 9.4, fill="none", rx=2.7, stroke=c, sw=1.6) +
            R(7.0, 2.6, 5.4, 9.4, fill="none", rx=2.7, stroke=c, sw=1.6))


def icon_flask(c):
    return (L(-4.2, -8.6, 4.2, -8.6, stroke=c, sw=1.6, cap="round") +
            P("M-2 -8.6 v5.4 L-7.8 5.2 a2.2 2.2 0 0 0 1.9 3.4 h11.8 a2.2 2.2 0 0 0 1.9 -3.4 L2 -3.2 v-5.4",
              stroke=c, sw=1.6) +
            P("M-5.6 3.4 h11.2", stroke=c, sw=1.3, opacity=.75))


def icon_moon(c):
    return P("M3 -8.6 A8.6 8.6 0 1 0 3 8.6 A6.7 6.7 0 1 1 3 -8.6 Z", stroke=c, sw=1.6)


# ---------------------------------------------------------------- HERO
def hero():
    rnd = random.Random(3)
    W, H = 1200, 470
    defs = [
        # gradients
        '<linearGradient id="hBg" x1="0" y1="0" x2=".7" y2="1">'
        f'<stop offset="0" stop-color="{BG1}"/><stop offset=".55" stop-color="#070c12"/>'
        f'<stop offset="1" stop-color="{BG0}"/></linearGradient>',
        '<linearGradient id="hName" x1="0" y1="0" x2="1" y2=".2">'
        f'<stop offset="0" stop-color="#8bf5b4"/><stop offset=".42" stop-color="{GREEN}"/>'
        f'<stop offset=".78" stop-color="{CYAN}"/><stop offset="1" stop-color="#60a5fa"/></linearGradient>',
        '<linearGradient id="hTerm" x1="0" y1="0" x2=".4" y2="1">'
        f'<stop offset="0" stop-color="#101a24"/><stop offset="1" stop-color="#080e15"/></linearGradient>',
        '<linearGradient id="hShine" x1="0" y1="0" x2="1" y2="0">'
        '<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".55"/>'
        '<stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>',
        '<linearGradient id="hScan" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset=".5" stop-color="{CYAN}" stop-opacity=".5"/>'
        f'<stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>',
        '<linearGradient id="hBar" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{GREEN_D}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>',
        '<radialGradient id="hGlow" cx=".5" cy=".5" r=".5">'
        f'<stop offset="0" stop-color="{GREEN}" stop-opacity=".22"/>'
        f'<stop offset="1" stop-color="{GREEN}" stop-opacity="0"/></radialGradient>',
        '<radialGradient id="hVig" cx=".5" cy=".45" r=".78">'
        '<stop offset=".45" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>',
        # scanline pattern
        '<pattern id="hScanLines" width="4" height="4" patternUnits="userSpaceOnUse">'
        '<rect width="4" height="1.1" fill="#000" opacity=".55"/></pattern>',
        f'<clipPath id="hClip"><rect width="{W}" height="{H}" rx="16"/></clipPath>',
        '<clipPath id="hTitle"><text x="58" y="228" font-size="82" font-weight="800" '
        f'letter-spacing="1.5" font-family="{MONO}">GRAYWIZARD</text></clipPath>',
        '<filter id="hBlur" x="-25%" y="-60%" width="150%" height="220%">'
        '<feGaussianBlur stdDeviation="9"/></filter>',
    ]

    L_ = []
    # --- background stack
    L_.append(R(0, 0, W, H, fill="url(#hBg)", rx=16))
    # grid
    for x in range(60, 1200, 60):
        L_.append(L(x, 0, x, H, stroke="#101d28", sw=1, opacity=.75))
    for y in range(40, 470, 47):
        L_.append(L(0, y, W, y, stroke="#101d28", sw=1, opacity=.75))
    # glow blob behind the name
    L_.append(f'<ellipse cx="300" cy="240" rx="360" ry="220" fill="url(#hGlow)"/>')
    # matrix rain
    L_.append(rain(W, H, cols=15, chars_per_block=14, x0=-30, seed=11))
    # floating code glyphs
    for gx, gy, s, op in [(560, 96, "$", .30), (620, 402, "#", .26), (500, 320, ">", .22),
                          (118, 120, "{", .20), (610, 200, "=", .18), (232, 430, "}", .20)]:
        L_.append(T(gx, gy, s, 22, GREEN, cls="float", opacity=op,
                    style=f"animation-duration:{rnd.uniform(5.5,8.5):.1f}s;animation-delay:-{rnd.uniform(0,4):.1f}s"))
    # CRT scanlines + travelling scan bar + vignette
    L_.append(R(0, 0, W, H, fill="url(#hScanLines)", opacity=.34))
    L_.append(R(0, -20, W, 26, fill="url(#hScan)", opacity=.55, cls="sweep"))
    L_.append(R(0, 0, W, H, fill="url(#hVig)"))

    # --- HUD chrome
    L_.append(hud_corners(10, 10, W - 20, H - 20, GREEN, 26, 2, .5))
    L_.append(R(60, 52, 192, 30, fill="#0b1a14", rx=15, stroke=GREEN_D, sw=1, opacity=.9))
    L_.append(C(78, 67, 9, fill="none", stroke=GREEN, sw=1, cls="pulse-soft"))
    L_.append(C(78, 67, 4.5, fill=GREEN, cls="pulse"))
    L_.append(T(93, 71.5, "SYSTEM.ONLINE", 11.5, GREEN, weight=500, ls=1.8))
    L_.append(C(1078, 67, 5, fill="#ff6b60", cls="pulse"))
    L_.append(T(1093, 71.5, "REC", 11.5, "#ff8f88", weight=500, ls=2.4))
    L_.append(T(288, 71.5, "12 public repos · 309 stars · 1,041 contributions · since Jun 2024",
                11, MUTED, ls=.6, cls="fade-in", style="animation-delay:2.2s"))

    # --- left column
    L_.append(T(62, 118, "graywizard@cyber:~$ whoami", 13, GREEN, opacity=.9))
    L_.append(T(58, 228, "GRAYWIZARD", 82, GREEN, weight=800, family=MONO, ls=1.5,
                opacity=.55, style='filter:url(#hBlur)'))
    L_.append(T(58, 228, "GRAYWIZARD", 82, "url(#hName)", weight=800, family=MONO, ls=1.5))
    L_.append(G(G(R(-320, 150, 200, 110, fill="url(#hShine)", opacity=.9), cls="shine"), clip="url(#hTitle)"))

    role_clip, role_body = typing_line("hRole", 62, 266,
                                       "Coder • Gamer • System Architect • Digital Phantom",
                                       17.5, "#d3e6f5", 540, delay=.65, dur=2.0)
    defs.append(role_clip)
    L_.append(role_body)
    L_.append(R(592, 252, 9, 18, fill=CYAN, cls="blink"))

    chips = [("Aditya", 76, GREEN, .45), ("he/him", 76, CYAN, .45),
             ("India • IST", 110, VIOLET, .45), ("terminal-first", 133, AMBER, .35)]
    cx = 62
    for label, w, col, op in chips:
        L_.append(R(cx, 292, w, 30, fill="#0d1a24", rx=15, stroke=col, sw=1.1, opacity=op))
        L_.append(T(cx + w / 2, 311.5, label, 12, SOFT, anchor="middle", family=MONO))
        cx += w + 14

    L_.append(T(62, 362, '> "Build. Break. Rebuild. Optimize."', 15, "#95f2b8", weight=500))

    # equaliser: bars live inside translate-groups so scaleY grows upward
    ex = 62
    for i in range(30):
        h = rnd.uniform(12, 42)
        col = CYAN if i % 7 == 3 else (GREEN if i % 3 else GREEN_D)
        L_.append(G(R(0, -h, 6, h, fill=col, rx=3, opacity=.85, cls="eq",
                      style=f"animation-duration:{rnd.uniform(.75,1.35):.2f}s;"
                            f"animation-delay:-{rnd.uniform(0,1.2):.2f}s"),
                    transform=f"translate({ex},{430})"))
        ex += 12
    L_.append(T(440, 412, "// ambient: mpv + lua audio pipeline", 11, MUTED))

    # --- terminal card
    L_.append(R(696, 96, 470, 300, fill="#000", rx=12, opacity=.4))
    L_.append(R(690, 88, 470, 300, fill="url(#hTerm)", rx=12, stroke=STROKE2, sw=1.2))
    L_.append(P("M690 100 a12 12 0 0 1 12 -12 h446 a12 12 0 0 1 12 12 v22 h-470 z", fill="#0b1219"))
    L_.append(L(690, 110, 1160, 110, stroke=STROKE, sw=1))
    for dx, col in ((712, RED), (730, AMBER), (748, "#28c840")):
        L_.append(C(dx, 99, 5, fill=col, opacity=.95))
    L_.append(T(925, 104, "graywizard@cyber: ~/profile — zsh", 11.5, MUTED, anchor="middle"))

    tl = [
        ("$ neofetch --short", GREEN, 140, True),
        ("os        Termux · Android 8+ · Linux", "#c3d3e2", 166.5, False),
        ("shell     bash · lua · python", "#c3d3e2", 193, False),
        ("toolkit   Android Studio · Kotlin · Java", "#c3d3e2", 219.5, False),
        ("delivers  scripts, TUIs, extensions, forks", "#c3d3e2", 246, False),
        ("uptime    840 days (since Jun 2024)", "#c3d3e2", 272.5, False),
        ("$ git log -1 --pretty=%s", GREEN, 299, True),
    ]
    d = 0.35
    for txt, col, base, typed in tl:
        if typed:
            cid = f"hT{int(base)}"
            clip, body = typing_line(cid, 712, base, txt, 12.5, col, len(txt) * 8 + 26, delay=d, dur=.75)
            defs.append(clip)
            L_.append(body)
            d += .75
        else:
            L_.append(T(712, base, txt, 12.5, col, cls="fade-up", style=f"animation-delay:{d + .25:.2f}s"))
            d += .12
    L_.append(T(712, 325.5, "f3a91c7", 12.5, DIM))
    L_.append(T(778, 325.5, "Build. Break. Rebuild. Optimize.", 12.5, AMBER, weight=500,
                cls="fade-up", style="animation-delay:1.55s"))
    L_.append(T(712, 352, "$", 12.5, GREEN))
    L_.append(R(726, 341, 8.5, 14.5, fill=GREEN, cls="blink"))
    L_.append(L(690, 366, 1160, 366, stroke=STROKE, sw=1))
    L_.append(T(712, 379, "status: online", 11, GREEN))
    L_.append(T(1148, 379, "id: GW-888", 11, MUTED, anchor="end"))

    # --- player / seek bar
    L_.append(P("M58 439 L71 446 L58 453 z", fill=GREEN))
    L_.append(T(82, 450.5, "00:00", 11, MUTED))
    L_.append(R(128, 444, 940, 4, fill="#16222e", rx=2))
    L_.append(G(R(0, 0, 940, 4, fill="url(#hBar)", rx=2, cls="grow-x",
                  style="animation-duration:14s;animation-delay:0s;animation-iteration-count:infinite;animation-direction:normal;animation-timing-function:cubic-bezier(.45,.05,.55,.95)"),
                transform="translate(128,444)"))
    L_.append(T(1082, 450.5, "∞", 13, GREEN))
    L_.append(T(1140, 424, "cyber-portfolio os v4.0.0 · profile reel", 11, DIM, anchor="end"))

    D, B = "\n".join(defs), "\n".join(L_)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}" role="img" aria-label="Graywizard — coder, gamer, system architect">'
            f'<defs>{D}' + style_block() + '</defs>' +
            G(B, clip="url(#hClip)") +
            R(0.5, 0.5, W - 1, H - 1, rx=16, stroke="#22303f", sw=1) + '</svg>')


# ---------------------------------------------------------------- ABOUT / LIFE
def about():
    W, H = 1200, 468
    defs = [
        '<linearGradient id="aBg" x1="0" y1="0" x2=".6" y2="1">'
        f'<stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG0}"/></linearGradient>',
        '<linearGradient id="aBar" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{GREEN_D}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>',
        '<pattern id="aScan" width="4" height="4" patternUnits="userSpaceOnUse">'
        '<rect width="4" height="1" fill="#000" opacity=".4"/></pattern>',
        '<radialGradient id="aGlow" cx=".5" cy=".5" r=".5">'
        f'<stop offset="0" stop-color="{CYAN}" stop-opacity=".18"/>'
        f'<stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>',
        f'<clipPath id="aClip"><rect width="{W}" height="{H}" rx="16"/></clipPath>',
    ]
    L_ = [R(0, 0, W, H, fill="url(#aBg)", rx=16)]
    for x in range(80, W, 80):
        L_.append(L(x, 0, x, H, stroke="#0f1a24", sw=1, opacity=.8))
    L_.append(R(0, 0, W, H, fill="url(#aScan)", opacity=.3))
    L_.append(hud_corners(10, 10, W - 20, H - 20, CYAN, 24, 2, .45))

    # ---- panel A : what I build
    L_.append(panel(40, 36, 536, 360, title="// system.capabilities", tag="live", accent=GREEN))
    L_.append(T(64, 108, "WHAT I BUILD", 23, TEXT, weight=700, family=SANS, ls=.4))
    L_.append(T(64, 130, "scripts · TUIs · extensions · forks", 11.5, MUTED))

    skills = [("Gaming", 95), ("Scripting / Automation", 88), ("Open Source", 82),
              ("Problem Solving", 90), ("Optimization", 85)]
    y = 156
    for i, (label, pct) in enumerate(skills):
        L_.append(T(64, y, label, 13, "#cfdcea", weight=500))
        L_.append(T(552, y, f"{pct}%", 13, CYAN, anchor="end", weight=600))
        L_.append(R(64, y + 11, 488, 7, fill="#16222e", rx=3.5))
        L_.append(G(R(0, 0, 488 * pct / 100, 7, fill="url(#aBar)", rx=3.5, cls="grow-x",
                      style=f"animation-duration:1.6s;animation-delay:{.25 + i * .17:.2f}s"),
                    transform=f"translate(64,{y + 11})"))
        y += 42
    L_.append(T(64, 366, "> everything here started as one personal annoyance.", 11.5, MUTED))

    # ---- panel B : life outside code
    L_.append(f'<ellipse cx="700" cy="250" rx="260" ry="170" fill="url(#aGlow)"/>')
    L_.append(panel(624, 36, 536, 360, title="// life.outside.code", tag="24 cycles", accent=CYAN))
    L_.append(T(648, 108, "LIFE OUTSIDE CODE", 23, TEXT, weight=700, family=SANS, ls=.4))
    L_.append(T(648, 130, "what happens when the terminal closes", 11.5, MUTED))

    life = [
        ("Gaming", "primary hobby — co-op nights & open worlds", GREEN, icon_gamepad),
        ("Audio pipeline tuning", "shipped an mpv equalizer: stereo / mono / 5.1 / 7.1", CYAN, icon_headphones),
        ("Relentless tinkering", "every annoyance becomes a script, then a repo", VIOLET, icon_flask),
        ("Coding when required", "free-time developer · usually required", AMBER, icon_moon),
    ]
    ry = 176
    for i, (title, desc, col, icon) in enumerate(life):
        L_.append(G(G(R(-22, -22, 44, 44, fill=col, rx=12, opacity=.1) +
                      R(-22, -22, 44, 44, fill="none", rx=12, stroke=col, sw=1.2, opacity=.55) +
                      icon(col),
                      cls="float", style=f"animation-duration:{6 + i * .8:.1f}s;animation-delay:-{i * 1.3:.1f}s"),
                    transform=f"translate(670,{ry - 8})", cls="fade-in"))
        L_.append(T(708, ry, title, 14.5, TEXT, weight=600, cls="fade-up",
                    style=f"animation-delay:{.15 + i * .12:.2f}s"))
        L_.append(T(708, ry + 21, desc, 11.5, MUTED, cls="fade-up",
                    style=f"animation-delay:{.22 + i * .12:.2f}s"))
        ry += 60

    # ---- footer strip
    L_.append(R(40, 412, 1120, 40, fill=PANEL2, rx=12, stroke=STROKE, sw=1.1))
    L_.append(T(66, 437, "> Build. Break. Rebuild. Optimize.", 12.5, GREEN, weight=600))
    L_.append(T(1134, 437, "India (IST) · terminal-first · open source · 12 public repos",
                11.5, MUTED, anchor="end"))

    D, B = "\n".join(defs), "\n".join(L_)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}" role="img" aria-label="What Graywizard builds, and life outside code">'
            f'<defs>{D}' + style_block() + '</defs>' +
            G(B, clip="url(#aClip)") +
            R(0.5, 0.5, W - 1, H - 1, rx=16, stroke="#22303f", sw=1) + '</svg>')
