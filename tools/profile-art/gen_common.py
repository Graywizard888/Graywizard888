"""Shared design tokens + SVG helpers for Graywizard's profile artwork."""
import random

# ---- palette : "terminal green + cyan on graphite" ----
BG0      = "#05070b"
BG1      = "#0a1017"
PANEL    = "#0d141d"
PANEL2   = "#111b26"
STROKE   = "#1d2b3a"
STROKE2  = "#26394c"
GREEN    = "#4ade80"
GREEN_D  = "#22c55e"
CYAN     = "#22d3ee"
AMBER    = "#fbbf24"
VIOLET   = "#a78bfa"
PINK     = "#f472b6"
RED      = "#ff5f57"
TEXT     = "#dbe7f3"
SOFT     = "#a8bccd"
MUTED    = "#718799"
DIM      = "#4d6070"

MONO = "'JetBrains Mono','Fira Code','Cascadia Code',Consolas,'Liberation Mono',Menlo,monospace"
SANS = "'Inter','Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif"


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def T(x, y, s, size=13, fill=TEXT, weight=400, family=MONO, anchor="start",
      opacity=None, ls=None, cls=None, style=None):
    """Text node. y is the BASELINE (no dominant-baseline games -> max compatibility).
    Font stacks live in CSS classes (.fm / .fs) so we don't repeat a ~110 char
    font-family attribute on every one of a thousand text nodes."""
    a = [f'x="{x}"', f'y="{y}"', f'font-size="{size}"', f'fill="{fill}"']
    if weight != 400:
        a.append(f'font-weight="{weight}"')
    if family == MONO:
        cls = f"{cls} fm".strip()
    elif family == SANS:
        cls = f"{cls} fs".strip()
    elif family:
        a.append(f'font-family="{family}"')
    if anchor != "start":
        a.append(f'text-anchor="{anchor}"')
    if opacity is not None:
        a.append(f'opacity="{opacity}"')
    if ls:
        a.append(f'letter-spacing="{ls}"')
    if cls:
        a.append(f'class="{cls}"')
    if style:
        a.append(f'style="{style}"')
    return f'<text {" ".join(a)}>{esc(s)}</text>'


def R(x, y, w, h, fill="none", rx=0, stroke=None, sw=1, opacity=None, cls=None, style=None):
    a = [f'x="{x}"', f'y="{y}"', f'width="{w}"', f'height="{h}"']
    if rx:
        a.append(f'rx="{rx}"')
    a.append(f'fill="{fill}"')
    if stroke:
        a.append(f'stroke="{stroke}" stroke-width="{sw}"')
    if opacity is not None:
        a.append(f'opacity="{opacity}"')
    if cls:
        a.append(f'class="{cls}"')
    if style:
        a.append(f'style="{style}"')
    return f'<rect {" ".join(a)}/>'


def C(cx, cy, r, fill="none", stroke=None, sw=1, opacity=None, cls=None, style=None):
    a = [f'cx="{cx}"', f'cy="{cy}"', f'r="{r}"', f'fill="{fill}"']
    if stroke:
        a.append(f'stroke="{stroke}" stroke-width="{sw}"')
    if opacity is not None:
        a.append(f'opacity="{opacity}"')
    if cls:
        a.append(f'class="{cls}"')
    if style:
        a.append(f'style="{style}"')
    return f'<circle {" ".join(a)}/>'


def P(d, fill="none", stroke=None, sw=1, opacity=None, cls=None, style=None,
      cap="round", join="round"):
    a = [f'd="{d}"', f'fill="{fill}"']
    if stroke:
        a.append(f'stroke="{stroke}" stroke-width="{sw}" stroke-linecap="{cap}" stroke-linejoin="{join}"')
    if opacity is not None:
        a.append(f'opacity="{opacity}"')
    if cls:
        a.append(f'class="{cls}"')
    if style:
        a.append(f'style="{style}"')
    return f'<path {" ".join(a)}/>'


def L(x1, y1, x2, y2, stroke=STROKE, sw=1, opacity=None, cls=None, style=None, dash=None, cap="butt"):
    a = [f'x1="{x1}"', f'y1="{y1}"', f'x2="{x2}"', f'y2="{y2}"',
         f'stroke="{stroke}" stroke-width="{sw}"', f'stroke-linecap="{cap}"']
    if dash:
        a.append(f'stroke-dasharray="{dash}"')
    if opacity is not None:
        a.append(f'opacity="{opacity}"')
    if cls:
        a.append(f'class="{cls}"')
    if style:
        a.append(f'style="{style}"')
    return f'<line {" ".join(a)}/>'


def G(inner, transform=None, cls=None, style=None, opacity=None, clip=None):
    a = []
    if transform:
        a.append(f'transform="{transform}"')
    if cls:
        a.append(f'class="{cls}"')
    if clip:
        a.append(f'clip-path="{clip}"')
    if opacity is not None:
        a.append(f'opacity="{opacity}"')
    if style:
        a.append(f'style="{style}"')
    return f'<g {" ".join(a)}>{inner}</g>' if a else f'<g>{inner}</g>'


# ---------------------------------------------------------------- matrix rain
_RAIN_POOL = list("01") * 6 + list("ABCDEF0123456789") + list("$#*+=:/\\>|<>[]{}()!?.~-")

# (opacity scale, font size, colour pool, duration) — one entry per sheet.
# Columns keep their own x jitter, phase and opacity; only the *speed* is shared
# inside a sheet, so the rain reads the same while the engine moves 3 textures
# instead of re-rasterising ~400 text glyphs every frame.
_RAIN_SHEETS = [
    (0.60, 12.5, (GREEN_D, CYAN), 9.60),
    (0.82, 13.0, (GREEN_D, GREEN), 7.40),
    (1.00, 13.5, (GREEN, CYAN), 5.80),
]


def rain(width, height, cols=15, block_h=None, dt=33.6, seed=7, x0=0, chars_per_block=14,
         colors=None, keep=(0.34, 0.24, 0.42), sheets=3):
    """Seamless vertical rain as `sheets` composited layers.

    Every column holds 2 identical stacked blocks, so translating a sheet by
    exactly `block_h` loops perfectly. Keeping the sheets whole (instead of one
    animated group per column) means the engine moves 3 textures per frame
    rather than re-rasterising ~400 text glyphs."""
    rnd = random.Random(seed)
    block_h = block_h or height
    span = width / cols
    buckets = [[] for _ in range(sheets)]
    for c in range(cols):
        si = c % sheets
        oscale, fs, pool, _dur = _RAIN_SHEETS[si]
        if colors:
            pool = colors
        x = round(x0 + span * c + span / 2 + rnd.uniform(-span * 0.18, span * 0.18), 1)
        for b in range(2):   # two identical stacked blocks -> seamless -H..0 loop
            for i in range(chars_per_block):
                r = rnd.random()
                if r < keep[0]:
                    continue
                y = round(b * block_h + i * (block_h / chars_per_block), 1)
                ch = rnd.choice(_RAIN_POOL)
                if r < keep[1] + 0.6:
                    col, op = rnd.choice(pool), rnd.uniform(0.10, 0.26) * oscale
                else:
                    col, op = GREEN, rnd.uniform(0.30, 0.62) * oscale
                buckets[si].append(T(x, y, ch, fs, col, cls="fm",
                                     opacity=round(min(op, 1.0), 2)))
    out = []
    for i, chars in enumerate(buckets):
        dur = _RAIN_SHEETS[i][3]
        delay = -round(random.Random(seed + 41 + i * 7).uniform(0, dur), 2)
        out.append(G("".join(chars), cls="rain",
                     style=f"animation-duration:{dur:.2f}s;animation-delay:{delay:.2f}s"))
    return "".join(out)


def hud_corners(x, y, w, h, color=GREEN, size=22, sw=2, opacity=0.55, cls="breathe"):
    hx, hy = x + size, y + size
    d = []
    d.append(f"M{x} {y+hy} L{x} {y} L{x+hx} {y}")
    d.append(f"M{x+w-hx} {y} L{x+w} {y} L{x+w} {y+hy}")
    d.append(f"M{x+w} {y+h-hy} L{x+w} {y+h} L{x+w-hx} {y+h}")
    d.append(f"M{x+hx} {y+h} L{x} {y+h} L{x} {y+h-hy}")
    return P(" ".join(d), stroke=color, sw=sw, opacity=opacity, cls=cls)


# ---------------------------------------------------------------- odometer
def odometer(x, y, value, size=40, color=TEXT, delay=0.3, dur=2.6, lh=None,
             spins=2, weight=700, family=MONO, uid="odo", digit_w=None):
    """Rolling digits. Returns (body, defs, width).
    The clip lives on an untransformed outer group; the animated transform is on
    an inner group, so it is unambiguous in every renderer. Static fallback (no
    CSS support) shows the final value, which is what we want."""
    lh = lh or size * 1.06
    dw = digit_w or size * 0.62
    s = str(value)
    body, d = [], []
    for i, ch in enumerate(s):
        cx = x + i * dw + dw / 2
        if ch.isdigit():
            target = int(ch)
            rows = [str(k % 10) for k in range(10 * spins + target + 1)]
            col = "".join(T(round(cx, 1), round(r * lh, 2), ch2, size, color,
                            weight=weight, family=family, anchor="middle")
                          for r, ch2 in enumerate(rows))
            cid = f"{uid}d{i}"
            d.append(f'<clipPath id="{cid}"><rect x="{cx - dw * 0.60:.2f}" y="{y - size * 0.80:.2f}" '
                     f'width="{dw * 1.20:.2f}" height="{lh:.2f}"/></clipPath>')
            body.append(G(G(G(col, cls="odo",
                              style=f"animation-duration:{dur:.2f}s;animation-delay:{delay + i * 0.14:.2f}s;"
                                    f"--rows:{len(rows) - 1};--lh:{lh:.2f}px"),
                            transform=f"translate(0,{y - (len(rows) - 1) * lh:.2f})"),
                          clip=f"url(#{cid})"))
        else:
            body.append(T(round(cx, 1), y, ch, size, color, weight=weight,
                            family=family, anchor="middle"))
    return "".join(body), "".join(d), len(s) * dw


# ---------------------------------------------------------------- panel chrome
def panel(x, y, w, h, rx=14, fill=PANEL, stroke=STROKE, title=None, accent=GREEN,
          tag=None):
    """Rounded panel with an optional mono title + accent tick."""
    out = [R(x, y, w, h, fill=fill, rx=rx, stroke=stroke, sw=1.2)]
    if title:
        out.append(R(x + 20, y + 20.5, 4, 12, fill=accent, rx=2))
        out.append(T(x + 32, y + 30, title, 12.5, SOFT, ls=1.6, cls="mono-label"))
    if tag:
        out.append(T(x + w - 20, y + 30, tag, 11, MUTED, anchor="end", ls=1))
    return "".join(out)


def bar(x, y, w, h, pct, color_a=GREEN_D, color_b=CYAN, track="#16222e",
        delay=0.2, dur=1.5, rx=None, grad_id=None, cls="grow-x"):
    """Grow-from-left bar using nested translate groups (no transform-box needed)."""
    rx = h / 2 if rx is None else rx
    out = [R(x, y, w, h, fill=track, rx=rx)]
    fillrect = R(0, 0, w * pct, h, fill=f"url(#{grad_id})" if grad_id else color_a, rx=rx)
    out.append(G(G(fillrect, cls=cls, style=f"animation-duration:{dur:.2f}s;animation-delay:{delay:.2f}s"),
                 transform=f"translate({x},{y})", clip="url(#barclip)"))
    return "".join(out)
