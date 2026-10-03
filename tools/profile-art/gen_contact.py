"""Contact cards — one tappable ticket per channel, the README's last section.

Same job as the build cards (`gen_p.py`) and deliberately the opposite look: the
repo cards are a terminal window — vertical grid, scanlines, top accent bar, HUD
corners, a holographic shimmer, and a footer of live counters. A contact card is a
ticket instead: a dotted field, a solid stub carrying the brand mark, a perforation
with punched notches, a serial, and an `open ↗` pill whose arrow keeps nudging out
of the card because "tap me" is the only call to action this section has.

Two shapes, like the build cards:
  * wide   — 1012 x 176, one per row at width="100%".
  * mobile — 480 x 214, larger relative type, served under 820px.

Nothing here is machine-refreshed: a handle does not change on a schedule, so this
module has no numbers to drift and no `builds.json` entry to keep honest.
"""
from gen_common import (AMBER, BG0, C, DIM, G, GREEN, L, MONO, MUTED, P, PANEL2, PINK, R,
                        SANS, SOFT, STROKE, STROKE2, T, TEXT, esc)
from gen_anim import style_block
from gen_icons import ICONS

# (file, channel, handle, target, accent, icon key, one-line why, what a tap does).
# The last two are the only copy of this information anywhere on the profile, and
# the "tap" line is deliberately different per card: a hint repeated on five tickets
# is a caption nobody reads twice.
CHANNELS = [
    ("telegram", "Telegram", "@Graywizard_projects", "t.me/Graywizard_projects",
     "#22a7e0", "telegram", "project channel · fastest replies, build logs live here",
     "join the channel"),
    ("github", "GitHub", "@Graywizard888", "github.com/Graywizard888",
     "#e6edf3", "github", "issues and pull requests welcome · MIT or GPL-3.0",
     "open the profile"),
    ("portfolio", "Portfolio", "website-src-seven", "website-src-seven.vercel.app",
     GREEN, "vercel", "the long versions — case studies, demos, screenshots",
     "view the work"),
    ("gists", "Gists", "mpv · lua scripts", "gist.github.com/Graywizard888",
     AMBER, "gists", "day-to-day scripts, kept current · 4 public gists",
     "read the scripts"),
    ("sponsors", "Sponsors", "Sponsor the work", "github.com/sponsors/Graywizard888",
     PINK, "githubsponsors", "funds build time, not a product · nothing is paywalled",
     "back a repo"),
]

WIDE_W, WIDE_H = 1012, 176
MOB_W, MOB_H = 480, 214

CSS = """
  /* the arrow in the pill: a short step out, a long pause. It is the only thing
     on the card that says "this is tappable", so it keeps saying it. */
  .nudge { animation: nudge 2.6s cubic-bezier(.3,.8,.3,1) infinite; }
  @keyframes nudge { 0%,58% { transform: translateX(0); }
                     72% { transform: translateX(5px); }
                     86%,100% { transform: translateX(0); } }

  /* the stub's accent bar grows down the card once, and the perforation punches
     itself in: both finish, so the static state is the finished ticket */
  .grow-y { animation: growy 1.1s cubic-bezier(.22,.8,.2,1) both;
            transform-origin: 0px 0px; }
  @keyframes growy { from { transform: scaleY(.001); } to { transform: scaleY(1); } }
  .perf { stroke-dasharray: 6 7; animation: perfin 1.4s ease-out .15s both; }
  @keyframes perfin { from { stroke-dashoffset: 90; } to { stroke-dashoffset: 0; } }
"""


def mark(key, color, size):
    """The brand mark on a tinted plate, centred on (0,0)."""
    ic = ICONS[key]
    box = size * .58
    if not ic["d"]:                                     # tile-only brand (gists)
        return (R(-size / 2, -size / 2, size, size, fill=color, rx=size * .24, opacity=.16) +
                R(-size / 2, -size / 2, size, size, fill="none", rx=size * .24,
                  stroke=color, sw=1.2, opacity=.55) +
                T(0, box * .34, ic["tile"], box, color, weight=700, anchor="middle",
                  family=SANS))
    s = box / 24.0 * ic["scale"]
    return (R(-size / 2, -size / 2, size, size, fill=color, rx=size * .24, opacity=.13) +
            R(-size / 2, -size / 2, size, size, fill="none", rx=size * .24,
              stroke=color, sw=1.2, opacity=.45) +
            G(P(d=ic["d"], fill=color), transform=f"scale({s:.4f}) translate(-12,-12)"))


def contact_card(i, ch, wide=True):
    """One ticket. `i` only picks the serial, so reordering the list cannot make
    the numbers lie about anything except their own order."""
    _, name, handle, target, accent, icon, why, cta = ch      # ch[0] is the stem
    W, H = (WIDE_W, WIDE_H) if wide else (MOB_W, MOB_H)
    stub = 208 if wide else 96                      # the perforated left hand of it
    body = stub + (26 if wide else 20)              # where the text starts
    serial = f"no. {i + 1:02d}/{len(CHANNELS):02d}"

    defs = [
        '<linearGradient id="kBg" x1="0" y1="0" x2=".8" y2="1">'
        f'<stop offset="0" stop-color="{PANEL2}"/><stop offset="1" stop-color="{BG0}"/></linearGradient>',
        f'<linearGradient id="kStub" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="{accent}" stop-opacity=".20"/>'
        f'<stop offset="1" stop-color="{accent}" stop-opacity=".04"/></linearGradient>',
        '<linearGradient id="kBar" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{accent}"/>'
        f'<stop offset="1" stop-color="{accent}" stop-opacity=".25"/></linearGradient>',
        f'<pattern id="kDots" width="16" height="16" patternUnits="userSpaceOnUse">'
        f'<circle cx="8" cy="8" r=".9" fill="#ffffff" opacity=".045"/></pattern>',
        f'<clipPath id="kClip"><rect width="{W}" height="{H}" rx="16"/></clipPath>',
    ]

    L_ = [
        R(0, 0, W, H, fill="url(#kBg)", rx=16),
        R(0, 0, W, H, fill="url(#kDots)"),
        # the stub, then the perforation, then the notches that make it a ticket
        R(0, 0, stub, H, fill="url(#kStub)"),
        R(0, 0, stub, H, fill="none", stroke=accent, sw=1, opacity=.16),
        R(0, 0, 5, H, fill="url(#kBar)", cls="grow-y"),
        L(stub, 18, stub, H - 18, stroke=accent, sw=1.4, opacity=.5, cls="perf"),
        C(stub, 0, 11, fill=BG0), C(stub, H, 11, fill=BG0),
    ]
    for nx in range(stub + 34, W - 34, 34):
        L_.append(C(nx, H - 9, 1, fill=STROKE2, opacity=.5))

    # ---- stub content: the mark, and the serial turned on its side
    msz = 84 if wide else 56
    L_.append(G(mark(icon, accent, msz), transform=f"translate({stub / 2},{H / 2 - (10 if wide else 22)})"))
    if wide:
        L_.append(T(stub / 2, H / 2 + 46, name.upper(), 11.5, accent, weight=600,
                    anchor="middle", ls=2.6, family=MONO))
        L_.append(G(T(0, 0, serial, 10.5, DIM, ls=1.6, family=MONO),
                    transform=f"translate(26,{H / 2 + 26}) rotate(-90) translate(-40,0)"))
    else:
        # under the mark, inside the stub: the top-right corner belongs to the pill
        L_.append(T(stub / 2, 152, serial, 11, DIM, anchor="middle", ls=1.2, family=MONO))

    # ---- the ticket face. The pill is placed first: its vertical centre is what
    # the wide card's text block and its "tap" hint both line up against.
    pw, ph = (138, 44) if wide else (112, 40)
    px, py = ((W - 26 - pw, H / 2 - ph / 2 - 6) if wide else (W - 18 - pw, 26))
    if wide:
        L_.append(T(body, 40, f"→ {name.lower()}", 12.5, MUTED, ls=2.2, family=MONO))
        L_.append(T(body, 84, handle, 30, TEXT, weight=700, family=SANS))
        L_.append(T(body, 112, target, 14, SOFT, family=MONO))
        L_.append(T(body, 140, why, 12.5, MUTED, family=MONO))
        L_.append(T(W - 26, py + ph + 20, f"tap anywhere · {cta}", 11, DIM,
                    anchor="end", ls=1, family=MONO))
    else:
        L_.append(T(body, 78, f"→ {name.lower()}", 13, MUTED, ls=2, family=MONO))
        L_.append(T(body, 118, handle, 27, TEXT, weight=700, family=SANS))
        L_.append(T(body, 148, target, 15, SOFT, family=MONO))
        L_.append(T(body, 176, why, 13, DIM, family=MONO))

    L_ += [
        R(px, py, pw, ph, fill=accent, rx=ph / 2, opacity=.13),
        R(px, py, pw, ph, fill="none", rx=ph / 2, stroke=accent, sw=1.2, opacity=.5),
        T(px + pw / 2 - 10, py + ph / 2 + 5, "open", 14.5, accent, weight=600,
          anchor="middle", family=MONO),
        # the arrow needs its own translated wrapper: `.nudge` sets `transform`,
        # and a CSS transform replaces the attribute on the same element rather
        # than adding to it — so the position lives outside the animated group.
        G(G(T(0, 5, "↗", 15, accent, weight=700, anchor="middle", family=MONO),
            cls="nudge"), transform=f"translate({px + pw - 28},{py + ph / 2})"),
    ]

    D, B = "\n".join(defs), "\n".join(L_)
    label = f"{name} — {handle} · {target}"
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}" role="img" aria-label="{esc(label)}">'
            f'<defs>{D}' + style_block(CSS) + '</defs>' + G(B, clip="url(#kClip)") +
            R(.5, .5, W - 1, H - 1, rx=16, stroke="#22303f", sw=1) + '</svg>')
