"""The tech-stack card's parts, shared by the 1200px and the 720px variant.

The layout language: a header line, an orbital "shortlist" on the left, and
grouped chips on the right — one group per discipline, one chip per tool. Chips
flow left to right and wrap when a row runs out of room, and the groups then
spread out to fill whatever height the card was given, so retuning the stack is
only ever an edit to `GROUPS` (and, if a tool needs a glyph, to `make_icons.py`).

Colour, fonts and the SVG primitives come from gen_common, so the card is on the
same palette as the hero, about and connect cards.
"""
from gen_common import (C, G, P, PANEL, R, STROKE, T, TEXT, SANS,
                       CYAN, GREEN, AMBER, VIOLET, MONO)
from gen_icons import ICONS

# ---------------------------------------------------------------- the stack
# (group label, accent, chips) — a chip is a key into gen_icons.ICONS, so its
# display name, colour and glyph all come from the icon table. Only tools that
# have shipped in a public repo (or that a repo is literally built on) belong
# here: the card is a list of receipts, not a wishlist.
GROUPS = [
    ("LANGUAGES", CYAN, ["python", "gnubash", "openjdk", "kotlin", "lua", "rust"]),
    ("ANDROID & DEVICE", GREEN, ["termux", "androidstudio", "android", "gradle",
                                 "jetpackcompose", "cmake"]),
    ("TERMINAL & MEDIA", VIOLET, ["linux", "mpv", "ffmpeg", "ndk"]),
    ("AUTOMATION & AI", AMBER, ["claude"]),
]

# The shortlist that rides the orbits: the tools that explain the rest, ordered so
# each ring gets a mix (a language, a platform, a workflow) rather than a cluster
# of relatives. The list is dealt round-robin into `ring_geom` and given an even
# share of the compass, so its length is free to change — 7 here, because that is
# one turn per medal with no two landing next to each other in the same band.
ORBIT_KEYS = ["python", "termux", "ffmpeg", "git", "gnubash", "lua", "mpv"]

N_CHIPS = sum(len(g[2]) for g in GROUPS)

# chip metrics: [pad | icon | gap | label | pad]
PAD_L, PAD_R, GAP = 9, 10, 7
CHIP_GAP = 7              # between chips in a row
ROW_GAP = 7               # between wrapped rows
MONO_ADV = 0.6            # JetBrains Mono advance width, in em
SIZE, H = 13, 40          # chip font size and height


def est_w(label, size):
    """Width of `label` in a monospace face. The chips are sized from this, which
    is what lets them stay true without shipping a font file with the card."""
    return len(label) * size * MONO_ADV


def box_of(size):
    """The mark's own square."""
    return round(size * 1.32, 1)


def plate_of(size):
    """The tinted plate behind the mark: a hair more room than the mark needs."""
    return box_of(size) + round(size * .55, 1)


def chip_w(label, size=SIZE):
    """[pad | plate | gap | label | pad], where the plate is `size` taller than
    the mark on each side — enough that a light brand on a dark card keeps a
    readable outline without needing a stroke."""
    return PAD_L + plate_of(size) + GAP + est_w(label, size) + PAD_R



def glyph(key, color, box, tile):
    """The mark itself, centred on (0,0): a brand path scaled into a `box` px
    square, or — for the brands simple-icons no longer carries — a mono tile."""
    ic = ICONS[key]
    if not ic["d"]:
        return (R(-box / 2, -box / 2, box, box, fill=color, rx=box * .22, opacity=.18) +
                R(-box / 2, -box / 2, box, box, fill="none", rx=box * .22,
                  stroke=color, sw=1, opacity=.6) +
                T(0, box * .31, ic["tile"], tile, color, weight=700, anchor="middle",
                  family=SANS))
    s = box / 24.0 * ic["scale"]
    return G(P(d=ic["d"], fill=color), transform=f"scale({s:.4f}) translate(-12,-12)")


def chip(x, y, key, size=SIZE, h=H, delay=0, animate=True, lead=False):
    """One tool chip: tinted plate, brand hairline, mark, label.

    `delay` is where this chip sits inside the slow pulse that walks along the
    row, so the row lights up one chip after the other instead of all at once.
    It is a *time*, and it has to stay a small one: at 7.2s a cycle, a delay
    measured in the hundreds of seconds is a chip that never blinks in the time
    anyone spends on the page. Returns (markup, width)."""
    ic = ICONS[key]
    col = ic["color"]
    w = chip_w(ic["label"], size)
    box, plate, tile = box_of(size), plate_of(size), size * .62
    out = [
        # an opaque plate first: the grid, the scanlines and (on phones) the rain
        # all live behind a chip, and a stray 17px glyph under "Gradle" reads as a
        # version number. Everything tinted below this is a wash, not a window.
        R(x, y, w, h, fill=PANEL, rx=12, opacity=.78),
        R(x, y, w, h, fill=col, rx=12, opacity=.17 if lead else .09),
        R(x + PAD_L - 1, y + (h - plate) / 2, plate, plate, fill=col,
          rx=plate * .28, opacity=.15),
        R(x, y + .5, w - 1, h - 1, fill="none", rx=12,
          stroke=col if lead else STROKE, sw=1.2 if lead else 1, opacity=.45 if lead else 1),
        G(glyph(key, col, box, tile),
          transform=f"translate({x + PAD_L + plate / 2:.1f},{y + h / 2:.1f})"),
        T(x + PAD_L + plate + GAP - 1, y + h / 2 + size * .35, ic["label"], size, TEXT,
          family=MONO),
    ]
    if animate:
        # index 2: above the tint, below the mark — the pulse must not be muted by
        # the wash it is lighting up
        out.insert(2, R(x - .5, y - .5, w + 1, h + 1, fill="none", rx=12.5, stroke=col,
                        sw=1.3, opacity=.28, cls="chip-hl",
                        style=f"animation-delay:{delay:.2f}s"))
    return "".join(out), w


def flow(x0, y, maxw, keys, size=SIZE, h=H, gap=CHIP_GAP, row_gap=ROW_GAP, delay0=.4,
         hl_step=.45, animate=True):
    """Chips, wrapped into rows inside `maxw`. Returns (markup, height, rows).

    The pulse delay counts from the *start of the row* (`n`), not from the chip's
    index in the group or its x position: a row is what the eye follows, and this
    keeps every delay inside a fraction of the 7.2s cycle. `delay0` shifts whole
    groups against each other so the four rows blink as a diagonal, not as one
    column."""
    out, cx, cy, n, rows = [], x0, y, 0, 1
    for i, key in enumerate(keys):
        frag, w = chip(cx, cy, key, size, h, delay0 + n * hl_step, animate, lead=(i == 0))
        if cx > x0 and cx + w > x0 + maxw + .5:              # wrap to the next row
            n, rows = 0, rows + 1
            cx, cy = x0, cy + h + row_gap
            frag, w = chip(cx, cy, key, size, h, delay0 + n * hl_step, animate,
                           lead=(i == 0))
        out.append(frag)
        cx += w + gap
        n += 1
    return "".join(out), (cy + h) - y, rows


# ---------------------------------------------------------------- orbits
def ellipse_path(cx, cy, rx, ry, rot):
    """An ellipse as two arcs, written the way a path is written so it can be
    referenced by <mpath> (how the medals ride the ring) and normalised with
    `pathLength=100` (how the ring draws itself in with one shared keyframe)."""
    import math
    a = math.radians(rot)
    dx, dy = rx * math.cos(a), rx * math.sin(a)
    return (f"M{cx - dx:.1f} {cy - dy:.1f}A{rx} {ry} {rot} 1 1 {cx + dx:.1f} {cy + dy:.1f}"
            f"A{rx} {ry} {rot} 1 1 {cx - dx:.1f} {cy - dy:.1f}Z")


def orbit_point(cx, cy, rx, ry, rot, t):
    """A point on that ellipse at parameter t — where a medal that has no SMIL to
    move it should sit, so the static card still reads as a finished design."""
    import math
    a = math.radians(rot)
    x, y = rx * math.cos(t), ry * math.sin(t)
    c, s = math.cos(a), math.sin(a)
    return cx + x * c - y * s, cy + x * s + y * c


def angle_to_param(rx, ry, rot, phi):
    """The parameter t whose point on the tilted ellipse lies on the ray `phi`.

    Medals are handed a *world* angle — where they should sit around the core —
    and this converts it, so an even spread still looks even whatever the ring's
    squash and tilt are doing underneath."""
    import math
    a = math.radians(-rot)
    dx = math.cos(phi) * math.cos(a) - math.sin(phi) * math.sin(a)
    dy = math.cos(phi) * math.sin(a) + math.sin(phi) * math.cos(a)
    return math.atan2(ry * dy, rx * dx)


def medal(key, r=17, box=23, tile=10):
    """Circular brand medal: dark disc, hairline in the brand colour, the mark."""
    r = max(r, (box + 9) / 2)
    col = ICONS[key]["color"]
    return (C(0, 0, r, fill=PANEL) +
            C(0, 0, r, fill="none", stroke=col, sw=1.35, opacity=.65) +
            G(glyph(key, col, box, tile), transform="translate(0,0)"))


def orbit(cx, cy, rx, ry, rot, items, color, dur, bid, spin=True):
    """One ring plus the medals that ride it.

    Each medal is drawn twice: a SMIL copy that travels the ring, and a static
    copy parked on the ring that switches itself off at 0s. A renderer without
    SMIL never sees the travelling one and shows the parked one, which is the
    same rule the bars and odometers follow — the static state *is* the finished
    card. `spin=False` keeps only the static copy (phone cards)."""
    out = [f'<path id="{bid}" d="{ellipse_path(cx, cy, rx, ry, rot)}" pathLength="100" '
           f'fill="none" stroke="{color}" stroke-opacity=".34" stroke-width="1.7" '
           f'class="orbit-draw"/>']
    for i, (key, phi) in enumerate(items):
        sx, sy = orbit_point(cx, cy, rx, ry, rot, angle_to_param(rx, ry, rot, phi))
        if not spin:
            out.append(G(medal(key), transform=f"translate({sx:.1f},{sy:.1f})"))
            continue
        # The travelling copy is *revealed* by CSS and only *moved* by SMIL, which
        # is what keeps the card honest under "reduce motion": the switch kills the
        # reveal, so the parked copy stays and nothing orbits. The motion starts at
        # `-phi/turn` so a medal takes off from where it was parked — the handover
        # has nothing to move, which is why the card does not twitch at 0.55s.
        out.append(G(f'<animateMotion dur="{dur}s" begin="-{phi / 6.2832 * dur:.2f}s" '
                     f'repeatCount="indefinite" rotate="0">'
                     f'<mpath href="#{bid}" xlink:href="#{bid}"/></animateMotion>'
                     + medal(key), opacity=0, cls="fade-in",
                     style=f"animation-delay:{.55 + i * .12:.2f}s"))
        out.append(G(medal(key), transform=f"translate({sx:.1f},{sy:.1f})",
                     cls="medal-park"))
    return "".join(out)


# ---------------------------------------------------------------- core
def core(cx, cy, r=42, glyph_size=26, pulse=True, hue=GREEN):
    """The nucleus: a halo, a radial disc, one ring pulsing out of it, `>_`.

    Returns (defs, body). The pulse is a CSS scale on a translated group and the
    disc's breathe is `transform-box: fill-box`, so both settle back into the
    drawn positions the moment animation is switched off."""
    defs = (
        f'<radialGradient id="sCoreG" cx=".36" cy=".3" r=".85">'
        f'<stop offset="0" stop-color="#a9f6c6"/><stop offset=".5" stop-color="{hue}"/>'
        f'<stop offset="1" stop-color="#0b3f2a"/></radialGradient>'
        f'<radialGradient id="sHalo"><stop offset="0" stop-color="{hue}" stop-opacity=".26"/>'
        f'<stop offset="1" stop-color="{hue}" stop-opacity="0"/></radialGradient>')
    body = [
        C(cx, cy, r * 2.7, fill="url(#sHalo)"),
        C(cx, cy, r, fill="url(#sCoreG)", cls="core-breathe" if pulse else None),
    ]
    if pulse:
        body.append(G(C(0, 0, r, fill="none", stroke=hue, sw=1.5, opacity=.7),
                      cls="ring-out", transform=f"translate({cx},{cy})"))
    body.append(T(cx, cy + glyph_size * .35, ">_", glyph_size, "#061a10", weight=700,
                  anchor="middle", family=MONO))
    return "".join(defs), "".join(body)


# the CSS the animated cards add on top of gen_anim's library
STACK_CSS = """
  /* the pulse that walks along a row of chips: each chip's highlight rect is
     only ever drawn as a hairline, so this is one attribute per frame */
  .chip-hl { animation: chipHl 7.2s cubic-bezier(.2,.8,.2,1) infinite; }
  @keyframes chipHl { 0%,100% { opacity: .28; } 3% { opacity: 1; } 13% { opacity: .28; } }

  /* the parked medals hand over to the travelling ones; with reduce-motion this
     never runs, which is exactly what that fallback wants */
  .medal-park { animation: park 1ms steps(1,end) .55s both; }
  @keyframes park { to { opacity: 0; } }

  /* orbit rings draw in once: pathLength=100 makes one keyframe fit every ring */
  .orbit-draw { stroke-dasharray: 100; animation: drawRing 2.2s cubic-bezier(.3,.9,.25,1) both; }
  @keyframes drawRing { from { stroke-dashoffset: 100; } to { stroke-dashoffset: 0; } }

  /* one expanding ring under the core, drawn from a translated group so
     0 0 is its own centre and no transform-box is needed */
  .ring-out { animation: ringOut 2.9s ease-out infinite; transform-origin: 0px 0px; }
  @keyframes ringOut { 0% { transform: scale(1); opacity: .7; }
                       70%,100% { transform: scale(1.72); opacity: 0; } }

  .core-breathe { animation: coreBreathe 4s ease-in-out infinite;
                  transform-box: fill-box; transform-origin: center; }
  @keyframes coreBreathe { 0%,100% { transform: scale(1); } 50% { transform: scale(1.045); } }
"""
