"""Cyber repo cards — the github-readme-stats "pin card" information layout
(repo name, description, language, stars, forks) rendered in the profile's
terminal/neon style, extended with pull requests, licence and last-push age.

Two shapes:
  * wide   — 1012 x 212, laid out for the full content column. Used at
             width="100%" on desktop, so it renders ~1:1 and the type stays sane.
  * mobile — 480 x 236, a narrow card with larger relative type, used below
             820px. On a 360px phone it scales to ~0.75x, which keeps it legible.

The mobile card also drops the shimmer, so phones get zero perpetual animation.
"""
from gen_common import *
from gen_anim import style_block

# BUILDS / PROFILE / fmt come from card_data via the gen_common star
# import: builds.json holds every value a machine can refresh.

ACCENTS = [GREEN, CYAN, VIOLET, AMBER, PINK, "#60a5fa", GREEN_D, CYAN]

WIDE_W, WIDE_H = 1012, 212
MOB_W, MOB_H = 480, 236


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
    return lines


def _metrics(x, y, size, accent, stars, forks, prs, uid):
    """★ stars · ⑂ forks · ⇄ pull requests — rolling counters."""
    out, defs = [], []
    gap = size * 3.4
    for i, (glyph, val, col) in enumerate(((None, stars, accent),
                                           ("⑂", forks, SOFT),
                                           ("⇄", prs, CYAN))):
        bx = x + i * gap
        out.append(T(bx, y, glyph or "★", size * 0.64, col))
        num, odef, _ = odometer(bx + size * 0.72, y, val, size=size, color=TEXT,
                                delay=.25 + i * .12, dur=1.6, spins=2, uid=f"{uid}{i}")
        out.append(num)
        defs.append(odef)
    return "".join(out), "".join(defs)


def build_card(i, d, wide=True):
    (repo, disp, lang, lang_col, lic, desc, stars, forks, prs, kb, updated) = d
    accent = ACCENTS[i % len(ACCENTS)]
    W, H = (WIDE_W, WIDE_H) if wide else (MOB_W, MOB_H)
    uid = f"{'w' if wide else 'm'}{i}"

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
    for gx in range(40, W, 40):
        L_.append(L(gx, 0, gx, H, stroke="#101d28", sw=1, opacity=.55))
    L_.append(R(0, 0, W, H, fill="url(#cScan)", opacity=.26))
    L_.append(R(0, 0, W, 4.5, fill="url(#cAcc)", rx=2))
    L_.append(hud_corners(8, 8, W - 16, H - 16, accent, 16, 1.6, .38, cls=None))

    label_lic = lic if lic else "unlicensed"

    if wide:
        # ---------------------------------------------------------------- wide
        # row 1 — prompt + last push
        L_.append(T(26, 36, f"~/repos/{repo.lower()}$", 13.5, DIM))
        L_.append(T(W - 26, 36, f"pushed {updated}", 13.5, DIM, anchor="end"))
        # row 2 — name (left) + index chip (right)
        nsize = 34 if len(disp) <= 14 else (29 if len(disp) <= 18 else 25)
        L_.append(f'<ellipse cx="180" cy="80" rx="240" ry="46" fill="url(#cGlow)"/>')
        L_.append(T(26, 92, disp, nsize, TEXT, weight=700))
        chip_x = W - 26 - 58
        L_.append(R(chip_x, 60, 58, 36, fill=accent, rx=10, opacity=.13))
        L_.append(R(chip_x, 60, 58, 36, fill="none", rx=10, stroke=accent, sw=1.3, opacity=.7))
        L_.append(T(chip_x + 29, 85, f"{i+1:02d}", 17, accent, weight=700, anchor="middle"))
        # row 3 — description beside the name, never reaching the chip
        for k, ln in enumerate(_wrap(desc, 48)[:2]):
            L_.append(T(380, 82 + k * 23, ln, 18, SOFT))
        # rule + footer
        L_.append(L(26, 140, W - 26, 140, stroke=STROKE, sw=1))
        L_.append(C(32, 178, 6, fill=lang_col))
        L_.append(T(46, 183, lang, 17, SOFT, weight=500))
        mb, md = _metrics(220, 183, 25, accent, stars, forks, prs, uid)
        defs.append(md)
        L_.append(mb)
        lcw = 30 + len(label_lic) * 9
        L_.append(R(W - 26 - lcw, 162, lcw, 28, fill="#101c26", rx=14, stroke=STROKE2, sw=1))
        L_.append(T(W - 26 - lcw / 2, 181, label_lic, 13.5, MUTED if lic else DIM, anchor="middle"))
        L_.append(T(W - 26 - lcw - 18, 183, "$ open repo ↗", 14, accent, weight=500, anchor="end"))
        L_.append(G(R(-240, 0, 200, H, fill="url(#cShine)", opacity=.9, cls="shimmer",
                      style=f"animation-duration:{9 + i * .7:.1f}s"),
                    clip="url(#cClip)"))
    else:
        # -------------------------------------------------------------- compact
        L_.append(T(22, 36, f"~/repos/{repo[:20].lower()}$", 13.5, DIM))
        L_.append(T(W - 22, 36, f"pushed {updated}", 13.5, DIM, anchor="end"))
        nsize = 32 if len(disp) <= 14 else (27 if len(disp) <= 18 else 23)
        L_.append(f'<ellipse cx="120" cy="76" rx="190" ry="42" fill="url(#cGlow)"/>')
        L_.append(T(22, 86, disp, nsize, TEXT, weight=700))
        L_.append(R(W - 74, 58, 52, 32, fill=accent, rx=9, opacity=.13))
        L_.append(R(W - 74, 58, 52, 32, fill="none", rx=9, stroke=accent, sw=1.3, opacity=.7))
        L_.append(T(W - 48, 82, f"{i+1:02d}", 17, accent, weight=700, anchor="middle"))
        L_.append(T(W - 92, 82, "↗", 15, MUTED, anchor="end"))
        for k, ln in enumerate(_wrap(desc, 46)):
            L_.append(T(22, 120 + k * 22, ln, 16.5, SOFT))
        L_.append(L(22, 166, W - 22, 166, stroke=STROKE, sw=1))
        L_.append(C(28, 200, 6, fill=lang_col))
        L_.append(T(42, 205, lang, 16, SOFT, weight=500))
        mb, md = _metrics(120, 205, 22, accent, stars, forks, prs, uid)
        defs.append(md)
        L_.append(mb)
        cw = 28 + len(label_lic) * 8.6
        L_.append(R(W - 22 - cw, 186, cw, 27, fill="#101c26", rx=13.5, stroke=STROKE2, sw=1))
        L_.append(T(W - 22 - cw / 2, 204, label_lic, 13, MUTED if lic else DIM, anchor="middle"))

    D, B = "\n".join(defs), "\n".join(L_)
    label = (f"{disp} — {stars} stars, {forks} forks, {prs} pull requests, "
             f"{lang}, {lic or 'no licence'}")
    extra = ""
    if wide:
        extra = (".shimmer { animation-name: shim; animation-timing-function: ease-in-out;"
                 " animation-iteration-count: infinite; }"
                 " @keyframes shim { from { transform: translateX(0); }"
                 " to { transform: translateX(1300px); } }")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
            f'role="img" aria-label="{label}">'
            f'<defs>{D}' + style_block(extra) + '</defs>' + G(B, clip="url(#cClip)") +
            R(.5, .5, W - 1, H - 1, rx=14, stroke="#22303f", sw=1) + '</svg>')
