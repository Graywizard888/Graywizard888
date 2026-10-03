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
def hero(H=470):
    """Animated hero banner.

    H is the banner height. The layout adapts rather than leaving dead space:
    the terminal grows and earns extra `gh repo list` / `gist list` rows, the
    left column gains a boot-log block, and the equaliser scales with the room.
    """
    import math
    W = 1200
    rnd = random.Random(3)

    # ---------------------------------------------------------------- layout
    NAME_SIZE = round(82 + (H - 470) * 0.05, 1)
    y_whoami = 118
    y_name = y_whoami + 110 + (H - 470) * 0.28
    y_role = y_name + NAME_SIZE * 0.46
    y_chips = y_role + 26
    y_quote = y_chips + 70
    y_eq = H - 40                                    # equaliser baseline
    y_eq_cap = H - 58
    y_seek = H - 26                                  # seek-bar track
    y_credit = H - 47
    t_y, t_h = 88, H - 170                           # terminal panel
    t_sep = t_y + t_h - 22                           # rule above the status bar
    t_stat = t_y + t_h - 9                           # status-bar baseline
    room = int((t_y + 58 + H - t_y - 234) / 26.5)    # rows that still clear the rule
    room = max(9, int((H - 118) / 26.5) + 4)
    eq_scale = 1 + (H - 470) / 470 * 0.55

    defs = [
        '<linearGradient id="hBg" x1="0" y1="0" x2=".7" y2="1">'
        f'<stop offset="0" stop-color="{BG1}"/><stop offset=".55" stop-color="#070c12"/>'
        f'<stop offset="1" stop-color="{BG0}"/></linearGradient>',
        '<linearGradient id="hName" x1="0" y1="0" x2="1" y2=".2">'
        f'<stop offset="0" stop-color="#8bf5b4"/><stop offset=".42" stop-color="{GREEN}"/>'
        f'<stop offset=".78" stop-color="{CYAN}"/><stop offset="1" stop-color="#60a5fa"/></linearGradient>',
        '<linearGradient id="hTerm" x1="0" y1="0" x2=".4" y2="1">'
        f'<stop offset="0" stop-color="#101a24"/><stop offset="1" stop-color="#080e15"/></linearGradient>',
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
        '<pattern id="hScanLines" width="4" height="4" patternUnits="userSpaceOnUse">'
        '<rect width="4" height="1.1" fill="#000" opacity=".55"/></pattern>',
        f'<clipPath id="hClip"><rect width="{W}" height="{H}" rx="16"/></clipPath>',
        '<filter id="hBlur" x="-25%" y="-60%" width="150%" height="220%">'
        '<feGaussianBlur stdDeviation="9"/></filter>',
    ]

    L_ = []
    # ---------------------------------------------------------------- backdrop
    L_.append(R(0, 0, W, H, fill="url(#hBg)", rx=16))
    for x in range(60, W, 60):
        L_.append(L(x, 0, x, H, stroke="#101d28", sw=1, opacity=.75))
    for y in range(40, H, 47):
        L_.append(L(0, y, W, y, stroke="#101d28", sw=1, opacity=.75))
    L_.append(f'<ellipse cx="300" cy="{H*0.5:.0f}" rx="360" ry="{H*0.47:.0f}" fill="url(#hGlow)"/>')
    L_.append(rain(W, H, cols=15, chars_per_block=14, x0=-30, seed=11))
    glyphs = [(560, 96, "$", .30), (118, 120, "{", .20), (500, y_quote - 42, ">", .22)]
    if H >= 560:
        glyphs.append((604, H - 150, "#", .24))
    for gx, gy, s, op in glyphs:
        L_.append(T(gx, gy, s, 22, GREEN, cls="float", opacity=op,
                    style=f"animation-duration:{rnd.uniform(5.5,8.5):.1f}s;animation-delay:-{rnd.uniform(0,4):.1f}s"))
    L_.append(R(0, 0, W, H, fill="url(#hScanLines)", opacity=.34))
    L_.append(R(0, -20, W, 26, fill="url(#hScan)", opacity=.55, cls="sweep"))
    L_.append(R(0, 0, W, H, fill="url(#hVig)"))

    # ---------------------------------------------------------------- HUD
    L_.append(hud_corners(10, 10, W - 20, H - 20, GREEN, 26, 2, .5))
    L_.append(R(60, 52, 192, 30, fill="#0b1a14", rx=15, stroke=GREEN_D, sw=1, opacity=.9))
    L_.append(C(78, 67, 9, fill="none", stroke=GREEN, sw=1, cls="pulse-soft"))
    L_.append(C(78, 67, 4.5, fill=GREEN, cls="pulse"))
    L_.append(T(93, 71.5, "SYSTEM.ONLINE", 11.5, GREEN, weight=500, ls=1.8))
    L_.append(T(288, 71.5,
                f"{fmt(PROFILE['public_repos'])} public repos · {fmt(PROFILE['stars'])} stars · "
                f"{fmt(PROFILE['contributions'])} contributions · since {PROFILE['created']}",
                11, MUTED, ls=.6, cls="fade-in", style="animation-delay:2.2s"))
    L_.append(C(1078, 67, 5, fill="#ff6b60"))
    L_.append(T(1093, 71.5, "REC", 11.5, "#ff8f88", weight=500, ls=2.4))

    # ---------------------------------------------------------------- left column
    L_.append(T(62, y_whoami, "graywizard@cyber:~$ whoami", 13, GREEN, opacity=.9))
    L_.append(T(58, y_name, "GRAYWIZARD", NAME_SIZE, GREEN, weight=800, ls=1.5,
                opacity=.55, style='filter:url(#hBlur)'))
    L_.append(T(58, y_name, "GRAYWIZARD", NAME_SIZE, "url(#hName)", weight=800, ls=1.5))

    role_w = len("Coder • Gamer • System Architect • Digital Phantom") * 8.8 + 30
    role_clip, role_body = typing_line("hRole", 62, y_role,
                                       "Coder • Gamer • System Architect • Digital Phantom",
                                       17.5, "#d3e6f5", role_w, delay=.65, dur=2.0)
    defs.append(role_clip)
    L_.append(role_body)

    chips = [("Aditya", 76, GREEN, .45), ("he/him", 76, CYAN, .45),
             ("India • IST", 110, VIOLET, .45), ("terminal-first", 133, AMBER, .35)]
    cx = 62
    for label, w, col, op in chips:
        L_.append(R(cx, y_chips, w, 30, fill="#0d1a24", rx=15, stroke=col, sw=1.1, opacity=op))
        L_.append(T(cx + w / 2, y_chips + 19.5, label, 12, SOFT, anchor="middle"))
        cx += w + 14

    L_.append(T(62, y_quote, '> "Build. Break. Rebuild. Optimize."', 15, "#95f2b8", weight=500))

    # boot log — fills whatever vertical room the chosen height leaves
    LOG = [
        "// 840 days on GitHub — first commit Jun 2024",
        "// 4 mpv + lua scripts running in daily use",
        "// last push: Custom-Enhancify-aapt2-binary",
        "// scope: Android tooling · shell automation · TUIs",
        "// currently: whatever annoyed me this week",
    ]
    log_top = y_quote + 34
    log_room = int((y_eq_cap - 22 - log_top) / 27)
    if log_room >= 1:
        L_.append(L(62, log_top - 20, 640, log_top - 20, stroke=STROKE, sw=1, opacity=.8))
        for i, line in enumerate(LOG[:log_room]):
            y = log_top + i * 27
            L_.append(T(62, y, "›", 13, GREEN_D, opacity=.8, cls="fade-up",
                        style=f"animation-delay:{1.2 + i * .14:.2f}s"))
            L_.append(T(80, y, line, 12, MUTED, cls="fade-up",
                        style=f"animation-delay:{1.26 + i * .14:.2f}s"))

    # equaliser + caption
    ex = 62
    for i in range(15):
        h = rnd.uniform(16, 46) * eq_scale
        col = CYAN if i % 7 == 3 else (GREEN if i % 3 else GREEN_D)
        L_.append(G(R(0, -h, 8, h, fill=col, rx=4, opacity=.85, cls="eq",
                      style=f"animation-duration:{rnd.uniform(.85,1.45):.2f}s;"
                            f"animation-delay:-{rnd.uniform(0,1.2):.2f}s"),
                    transform=f"translate({ex},{y_eq})"))
        ex += 15
    L_.append(T(316, y_eq_cap, "// ambient: mpv + lua audio pipeline", 11, MUTED))

    # ---------------------------------------------------------------- terminal
    L_.append(R(696, t_y + 8, 470, t_h, fill="#000", rx=12, opacity=.4))
    L_.append(R(690, t_y, 470, t_h, fill="url(#hTerm)", rx=12, stroke=STROKE2, sw=1.2))
    L_.append(P(f"M690 {t_y+12} a12 12 0 0 1 12 -12 h446 a12 12 0 0 1 12 12 v22 h-470 z", fill="#0b1219"))
    L_.append(L(690, t_y + 22, 1160, t_y + 22, stroke=STROKE, sw=1))
    for dx, col in ((712, RED), (730, AMBER), (748, "#28c840")):
        L_.append(C(dx, t_y + 11, 5, fill=col, opacity=.95))
    L_.append(T(925, t_y + 16, "graywizard@cyber: ~/profile — zsh", 11.5, MUTED, anchor="middle"))

    # Top repos by stars, drawn from the same live data as the build cards so
    # the two can never disagree. Sorted descending; ties keep BUILDS order.
    repo_rows = [(f"{name:<25}★ {stars:>3}   {lang.lower()}", "#c3d3e2", "")
                 for _repo, name, lang, _col, _lic, _desc, stars, _f, _p, _kb, _push
                 in sorted(BUILDS, key=lambda b: -b[6])[:5]]

    rows = [("$ neofetch --short", GREEN, "type"),
            ("os        Termux · Android 8+ · Linux", "#c3d3e2", ""),
            ("shell     bash · lua · python", "#c3d3e2", ""),
            ("toolkit   Android Studio · Kotlin · Java", "#c3d3e2", ""),
            ("delivers  scripts, TUIs, extensions, forks", "#c3d3e2", ""),
            ("uptime    840 days (since Jun 2024)", "#c3d3e2", ""),
            ("$ gh repo list Graywizard888 --sort stars", GREEN, "type"),
            *repo_rows,
            ("$ gist list --user Graywizard888", GREEN, "type"),
            ("audio_enhancer.lua   stereo / 5.1 / 7.1 EQ", "#c3d3e2", ""),
            ("auto_skip.lua        chapter skipper", "#c3d3e2", ""),
            ("Duration_OSD.lua     duration overlay", "#c3d3e2", ""),
            ("Up_next.lua          episode overlay", "#c3d3e2", ""),
            ("$ git log -1 --pretty=%s", GREEN, "type"),
            ("f3a91c7  Build. Break. Rebuild. Optimize.", "#c3d3e2", "commit"),
            ("$", GREEN, "prompt")]
    # compose the terminal as blocks so no height cuts a command off from its
    # output; the closing block (git log + commit + blinking prompt) is reserved
    D = rows[-3:]                                     # closing block, always shown
    blocks = [rows[0:6], rows[6:12], rows[12:17]]     # neofetch / repos / gists
    room_rows = max(9, int((t_sep - 14 - (t_y + 52)) / 26.5) + 1)
    budget, shown = room_rows - len(D), []
    for b in blocks:
        if len(b) <= budget:
            shown += b
            budget -= len(b)
        else:
            if budget >= 2:
                shown += b[:budget]
            break
    shown += D
    d = 0.35
    for i, (txt, col, kind) in enumerate(shown):
        base = t_y + 52 + i * 26.5
        if kind == "type":
            cid = f"hT{i}"
            clip, body = typing_line(cid, 712, base, txt, 12.5, col, len(txt) * 8 + 26, delay=d, dur=.75)
            defs.append(clip)
            L_.append(body)
            d += .5
        elif kind == "commit":
            L_.append(T(712, base, "f3a91c7", 12.5, DIM))
            L_.append(T(778, base, "Build. Break. Rebuild. Optimize.", 12.5, AMBER, weight=500,
                        cls="fade-up", style=f"animation-delay:{d:.2f}s"))
            d += .25
        elif kind == "prompt":
            L_.append(T(712, base, "$", 12.5, GREEN))
            L_.append(R(726, base - 11, 8.5, 14.5, fill=GREEN, cls="blink"))
        else:
            L_.append(T(712, base, txt, 12.5, col, cls="fade-up",
                        style=f"animation-delay:{d:.2f}s"))
            d += .1
    L_.append(L(690, t_sep, 1160, t_sep, stroke=STROKE, sw=1))
    L_.append(T(712, t_stat, "status: online", 11, GREEN))
    L_.append(T(1148, t_stat, "id: GW-888", 11, MUTED, anchor="end"))

    # ---------------------------------------------------------------- player bar
    L_.append(P(f"M58 {y_seek+5} L71 {y_seek+12} L58 {y_seek+19} z", fill=GREEN))
    L_.append(T(82, y_seek + 16.5, "00:00", 11, MUTED))
    L_.append(R(128, y_seek + 10, 940, 4, fill="#16222e", rx=2))
    L_.append(G(R(0, 0, 940, 4, fill="url(#hBar)", rx=2, cls="grow-x",
                  style="animation-duration:14s;animation-delay:0s;animation-iteration-count:infinite;"
                        "animation-direction:alternate;animation-timing-function:cubic-bezier(.45,.05,.55,.95)"),
                transform=f"translate(128,{y_seek+10})"))
    L_.append(T(1082, y_seek + 16.5, "∞", 13, GREEN))
    L_.append(T(1140, y_credit, "cyber-portfolio os v4.0.0 · profile reel", 11, DIM, anchor="end"))

    D = "\n".join(defs)
    B = "\n".join(L_)
    extra_css = (f"@keyframes fall {{ from {{ transform: translateY(-{H}px); }} to {{ transform: translateY(0px); }} }}"
                 f"@keyframes sweep {{ 0% {{ transform: translateY(-{H*0.36:.0f}px); }} "
                 f"100% {{ transform: translateY({H}px); }} }}")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}" role="img" aria-label="Graywizard — coder, gamer, system architect">'
            f'<defs>{D}' + style_block(extra_css) + '</defs>' +
            G(B, clip="url(#hClip)") +
            R(0.5, 0.5, W - 1, H - 1, rx=16, stroke="#22303f", sw=1) + '</svg>')


def about(H=468):
    W = 1200
    d = H - 468
    panel_y, panel_h = 36, 360 + d
    panel_b = panel_y + panel_h
    foot_y = H - 56
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
    L_.append(hud_corners(10, 10, W - 20, H - 20, CYAN, 24, 2, .45, cls=None))

    # ---- panel A : what I build
    L_.append(panel(40, panel_y, 536, panel_h, title="// system.capabilities", tag="live", accent=GREEN))
    L_.append(T(64, 108, "WHAT I BUILD", 23, TEXT, weight=700, family=SANS, ls=.4))
    L_.append(T(64, 130, "scripts · TUIs · extensions · forks", 11.5, MUTED))

    skills = [("Gaming", 95), ("Scripting / Automation", 88), ("Open Source", 82),
              ("Problem Solving", 90), ("Optimization", 85)]
    s_top, s_bot = 156, panel_b - 58                 # bars fill the panel
    s_pitch = (s_bot - s_top) / (len(skills) - 1)
    for i, (label, pct) in enumerate(skills):
        y = s_top + i * s_pitch
        L_.append(T(64, y, label, 13, "#cfdcea", weight=500))
        L_.append(T(552, y, f"{pct}%", 13, CYAN, anchor="end", weight=600))
        L_.append(R(64, y + 11, 488, 7, fill="#16222e", rx=3.5))
        L_.append(G(R(0, 0, 488 * pct / 100, 7, fill="url(#aBar)", rx=3.5, cls="grow-x",
                      style=f"animation-duration:1.6s;animation-delay:{.25 + i * .17:.2f}s"),
                    transform=f"translate(64,{y + 11})"))
    L_.append(T(64, panel_b - 20, "> everything here started as one personal annoyance.", 11.5, MUTED))

    # ---- panel B : life outside code
    L_.append(f'<ellipse cx="700" cy="{H*0.53:.0f}" rx="260" ry="{max(170, H*0.4):.0f}" fill="url(#aGlow)"/>')
    L_.append(panel(624, panel_y, 536, panel_h, title="// life.outside.code", tag="24 cycles", accent=CYAN))
    L_.append(T(648, 108, "LIFE OUTSIDE CODE", 23, TEXT, weight=700, family=SANS, ls=.4))
    L_.append(T(648, 130, "what happens when the terminal closes", 11.5, MUTED))

    life = [
        ("Gaming", "primary hobby — co-op nights & open worlds", GREEN, icon_gamepad),
        ("Audio pipeline tuning", "shipped an mpv equalizer: stereo / mono / 5.1 / 7.1", CYAN, icon_headphones),
        ("Relentless tinkering", "every annoyance becomes a script, then a repo", VIOLET, icon_flask),
        ("Coding when required", "free-time developer · usually required", AMBER, icon_moon),
    ]
    l_top, l_bot = 176, panel_b - 47                 # 26px margin + desc offset
    l_pitch = (l_bot - l_top) / (len(life) - 1)
    for i, (title, desc, col, icon) in enumerate(life):
        ry = l_top + i * l_pitch
        icon_cls = "float" if i < 2 else ""
        icon_style = f"animation-duration:{6 + i * .8:.1f}s;animation-delay:-{i * 1.3:.1f}s" if i < 2 else None
        L_.append(G(G(R(-22, -22, 44, 44, fill=col, rx=12, opacity=.1) +
                      R(-22, -22, 44, 44, fill="none", rx=12, stroke=col, sw=1.2, opacity=.55) +
                      icon(col),
                      cls=icon_cls or None, style=icon_style),
                    transform=f"translate(670,{ry - 8})", cls="fade-in"))
        L_.append(T(708, ry, title, 14.5, TEXT, weight=600, cls="fade-up",
                    style=f"animation-delay:{.15 + i * .12:.2f}s"))
        L_.append(T(708, ry + 21, desc, 11.5, MUTED, cls="fade-up",
                    style=f"animation-delay:{.22 + i * .12:.2f}s"))

    # ---- footer strip
    L_.append(R(40, foot_y, 1120, 40, fill=PANEL2, rx=12, stroke=STROKE, sw=1.1))
    L_.append(T(66, foot_y + 25, "> Build. Break. Rebuild. Optimize.", 12.5, GREEN, weight=600))
    L_.append(T(1134, foot_y + 25,
                f"India (IST) · terminal-first · open source · {fmt(PROFILE['public_repos'])} public repos",
                11.5, MUTED, anchor="end"))

    D, B = "\n".join(defs), "\n".join(L_)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}" role="img" aria-label="What Graywizard builds, and life outside code">'
            f'<defs>{D}' + style_block() + '</defs>' +
            G(B, clip="url(#aClip)") +
            R(0.5, 0.5, W - 1, H - 1, rx=16, stroke="#22303f", sw=1) + '</svg>')
